import mido
from pprint import pprint
import utils.miditools as mt
from utils.midi_arpegiator import arpeggiator 
import time
import random
import utils.generate_scale_mapping as scalemap


## to do
# parameter change does not turn off auto
# get note bend to come through
# velocity effects light levels

out_dict = mt.user_midi_output()

note_store = mt.note_store()
note_store_auto = mt.note_store()
rand_note_time = 1
arp_on = True

time_before_random = 0

mapping = scalemap.generate_scale_mapping(scalemap.scales['roro'])


arp = arpeggiator(rate = 120*4)

program_int = 0
n_sounds = 32 + 1

def cc_scaler(xmin,xmax):
    return (lambda x: (float(x)/127) * (xmax - xmin) + xmin)

arp_rate = cc_scaler(120,120*12)

print(arp_rate(100))
#arp.randomise_order()

def send_msg(midi_out_port, msg):
    print(msg)
    midi_out_port.send(msg)

sustain = 1
gap = 0.5
t_note_on = time.time()-sustain
t_note_off = time.time()
note = 40
note_on = False

while True:
    for device, midi_out_port in out_dict.items():
        if not note_on and t_note_off + gap < time.time():
            msg = mido.Message("note_on", note=note, velocity=100)
            msg = mt.map_note(mapping, msg)
            send_msg(midi_out_port, msg)
            t_note_on = time.time()
            note_on = True

        if note_on and t_note_on + sustain < time.time():
            msg = mido.Message("note_off", note=note)
            msg = mt.map_note(mapping, msg)
            send_msg(midi_out_port, msg)
            t_note_off = time.time()
            note_on = False

