import time
import math

import utils.dmxtools as dt
import utils.miditools as mt
from utils.types import Bulb, Par3RGB
from default_setup import setup

lights = setup['lights']
instrument_rack = setup['instrument_rack']
router_rack = setup['router_rack']

#get dmx devices from user input
print("dmx port = ")
dmx_port = dt.user_dmx()

# get midi devices from user input
midi_port_dict = mt.user_midi()

# set the dmx_port in all the lights
for light in lights:
    light.dmx_port = dmx_port

# parameters for the show
osc_val = 0.5


print(f'### the current setup')
print(f'num_lights = {len(lights)}')

while True:

    # Process midi for instrument rack
    for device, midi_port in midi_port_dict.items():

        # if two cc messages with the same control and channel have 
        # arrived then only append most recent
        message_queue = mt.iter_pending_clean(midi_port)
            
        for msg in message_queue:

            print(msg)
            for inst in instrument_rack:
                inst.midi_action(msg)

    # Get output from the instrument rack
    light_vals = list(instrument_rack[0].get_light_output().values())
    # it seems the old behaviour was to output a list of 3 values for each
    # bulb, which I don't understand. So keep only the first
    light_vals = [rgb[0] for rgb in light_vals]

    # Send instrument rack output to the routers to update light values
    for router in router_rack:
        router(lights, light_vals)

    # Space for some custom/hacky updates to light values
    time_val = time.time()
    sin_osc = ( (1- osc_val ) + osc_val * math.sin(time_val))
    sin_rot_osc = (1- osc_val ) + osc_val * math.sin(time_val+ math.pi *2 / 3)
    sin_rot_osc2 = (1- osc_val ) + osc_val * math.sin(time_val+ math.pi *4 / 3)
    
    for light in lights:
        if isinstance(light, Par3RGB):
            light.rgb_value = [sin_osc * 1, sin_rot_osc * 1, sin_osc * 1]

    # Send all the data down dmx
    for light in lights:
        light.dmx_update()

    if isinstance(dmx_port, dt.DMXConnection):
        dmx_port.render()

