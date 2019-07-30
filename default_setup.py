import lightsynth.light_instrument as inst
from utils.types import Bulb, Par3RGB
import random

### First create a list of lights
# TODO: figure out what to do with dmx_port at this stage


# Helper function to generate lights in a grid
def gen_gs_grid(rows=4, cols=5, size=50,
                x_start=50, x_space=100,
                y_start=50, y_space=100,
                dmx_start=0, val=100):
    """
    Returns a list of gs lights with x and y positions as layed out in a grid
    with given number of rows and columns. The dmx roots are given in order
    starting from dmx_start, and the lights are initially assigned value val
    """
    gs_lights = [Bulb(None, 0, val, x, y, size)
                 for y in range(y_start, y_start + rows*y_space, y_space)
                 for x in range(x_start, x_start + cols*x_space, x_space)]
    for i, light in enumerate(gs_lights, dmx_start):
        light.dmx_root = i

    return gs_lights

# Helper function to generate lights in a grid
def gen_rgb_grid(rows=1, cols=3, size=50,
                 x_start=50, x_space=100,
                 y_start=50, y_space=100,
                 dmx_start=0, r=100, g=0, b=0):
    """
    Returns a list of rgb lights with x and y positions as layed out in a grid
    with given number of rows and columns. The dmx roots are given in order
    starting from dmx_start, and the lights are initially assigned given rgb 
    values
    """
    # y_start = gs_rows*y_space + 50

    rgb_lights = [Par3RGB(None, 0, [r,g,b], x, y, size)
                  for y in range(y_start, y_start + rows*y_space, y_space)
                  for x in range(x_start, x_start + cols*x_space, x_space)]
    for i, light in enumerate(rgb_lights):
        light.dmx_root = dmx_start + 3*i
    return rgb_lights

# A default layout of lights
def default_lights():
    gs_lights = gen_gs_grid(rows=4, cols=5, size=50,
                            x_start=50, x_space=100,
                            y_start=50, y_space=100,
                            dmx_start=0, val=100)
    rgb_lights = gen_rgb_grid(rows=1, cols=5, size=50,
                              x_start=50, x_space=100,
                              y_start=450, y_space=100,
                              dmx_start=0, r=100, g=0, b=0)
    return gs_lights + rgb_lights



### Second create a light instrument to add to the rack
def default_rack(lights):
    # Create one instrument for the default rack
    max_length_decay = 8
    decay_exp_scaling_pair = (0.5, 2.8)
    envelope_params = {
        'type': 'envelope',
        'level': 1,
        'attack': 0.1,
        'decay': 2,
        'sustain': 1,
        'release': 2,
        'lfo_level': 0.2,
        'lfo_rate': 1,
        'env_mode': "exponential"
    }
    cc_controls = {
        1: "attack",
        2: "decay",
        4: "sustain",
        3: "release"}

    instrument = inst.LightInstrument(
        note_channel=0,
        light_list=[light.dmx_root
                    for light in lights if isinstance(light, Bulb)],
        cc_controls=cc_controls,
        envelope_params=envelope_params,
        mode="cycle",
        max_length_attack=5,  attack_exp_scaling_pair=(0.5, 1.38),
        max_length_release=max_length_decay,  decay_exp_scaling_pair=decay_exp_scaling_pair,
        max_length_decay=max_length_decay,  release_exp_scaling_pair=decay_exp_scaling_pair)
    
    for _, light in instrument.light_envs.items():
        light.env.lfo_rate = random.uniform(1, 4)

    return [instrument]

# the simple router wants a list of values that correspond to the bulbs first,
# then the rgb pars
def simple_router(lights, values):
    # potential performance issue, these numbers do not change but aren't 
    # necessarily fast to compute
    num_bulbs = sum(1 for light in lights if isinstance(light, Bulb))
    num_pars = sum(1 for light in lights if isinstance(light, Par3RGB))
        
    # make values at least the right length
    values += [0] * (num_bulbs + 3*num_pars - len(values)) 

    gs_index = 0
    rgb_index = num_bulbs
    for light in lights:
        if isinstance(light, Bulb):
            light.val = values[gs_index]
            gs_index += 1
        elif isinstance(light, Par3RGB):
            light.val = tuple(values[rgb_index:rgb_index+3])
            rgb_index += 3

lights = default_lights()
setup = {
    'lights': lights,
    'instrument_rack': default_rack(lights),
    'router_rack': [simple_router],
}
