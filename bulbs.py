import mido
import lightsynth.light_instrument as inst
import pysimpledmx
import utils.miditools as mt
from utils.dmxtools import * 
from collections import OrderedDict
import copy

from pprint import pprint

note_old = []
light_dict = {0:20}#,1:30,2:40}

#get dmx devices from user input
dmx_port = user_dmx()

#dmx_port = pysimpledmx.DMXConnection("COM11")

set_light_cheap(dmx_port, 20, (1,0,0))

lights = {}
for i in range(8):
    lights[i] = {'root_dmx': i, 'func': set_light_bulb}


print("on")

# get midi devices from user input
midi_devices = mido.get_input_names()
port_dict = mt.user_midi()

envelope_params = {
    'type':'envelope', 
    'level':1, 
    'attack':0.1, 
    'decay':2, 
    'sustain':1, 
    'release':2,
    'lfo_level':0,
    'lfo_rate':1,
    'env_mode':"exponential"
}
cc_controls = {
    1: "lfo_rate",
    2: "lfo_level",
    3: "saturation",
    4: "hue",
    6: "level",
    
    103: "attack",
    104: "decay",
    107: "sustain",
    108: "release",
    106: 'mode'}

instrument = inst.LightInstrument( 
    #note_list=[48,37],#,38,39,44,45,46], 
    note_list=lights.keys(),
    light_list=lights.keys(), 
    cc_controls = cc_controls,
    envelope_params = envelope_params,
    mode = "single" )

instrument_rack = [instrument]

while 1:
    for device, midi_port in port_dict.iteritems():

        # if two cc messages with the same control and channel have come then only append most recent
        message_queue = mt.iter_pending_clean(midi_port)
            
        for msg in message_queue:
            
            print(msg)
            for inst in instrument_rack:
                if msg.type in ["note_on", "note_off"]:
                    msg.note = msg.note % len(lights)
                inst.midi_action(msg)

            
    light_vals = instrument_rack[0].get_light_output()
    
    for light_key, light in lights.iteritems():
        val = light_vals[light_key] # [ light_vals2[light_key][i] + light_vals[light_key][i] for i in range(3)] 
        
        #val = [col/max_val for col in val]
        light['func'](dmx_port, light['root_dmx'], val)
    
    dmx_port.render()