from config import load_lights
from utils.types import Bulb, Par3RGB

add_library('oscP5')

# setup some global variables
osc = None
loc = None

# load the light config from a file

lights = load_lights('default_lights.yaml')
num_gs_lights = sum(1 for light in lights if isinstance(light, Bulb))
num_rgb_lights = sum(1 for light in lights if isinstance(light, Par3RGB))
num_indices = num_gs_lights + 3*num_rgb_lights
cur_index = 0

# TODO: calculate window width and height from the given grid of lights
win_width = 500
win_height = 500

framerate = 25
osc_port = 12000
font = None
font_height = 10
text_color = 255


def setup():
    global osc, loc, oscEvent, font
                    
    size(win_width, win_height)
    frameRate(framerate)
    font = createFont("Arial", 16, True)
    textFont(font, font_height)
 
    # start oscP5 by default listening on port 12000
    osc = OscP5(this, osc_port)
    loc = NetAddress('127.0.0.1', osc_port)
    
def draw_light(light):
    
    if isinstance(light, Bulb):
        fill(light.value)
    elif isinstance(light, Par3RGB):
        fill(*light.rgb_value)
    else:
        print('ERROR: I do not know how to draw this light type %s' % light)
        return
        
    ellipse(light.x, light.y, light.size, light.size)  
    fill(text_color)
    textAlign(CENTER)
    text(light.tag, light.x, light.y+font_height/2)
    
def draw():
    background(0)
    
    for light in lights:
         draw_light(light)
         
def mousePressed():
    global cur_index
    print('### mouse pressed')
    print('### toggling light %d' % cur_index)
    
    msg = OscMessage("/dmx") 
    msg.add(cur_index) 
    msg.add(200)
    
    print('sending message: %s' % msg)
    osc.send(msg, loc) 
    cur_index = (cur_index + 1) % num_indices
    
# declare oscEvent first so it's caught in the setup phase
def oscEvent(msg):
    if msg.checkAddrPattern('/dmx') and msg.checkTypetag('ii'):
        channel = msg.get(0).intValue()
        value = msg.get(1).intValue()

        print('### received osc message: set channel %3d to %3d' % (channel, value))
        
        for light in lights:
            if isinstance(light, Bulb):
                if light.dmx_root == channel:
                    light.value = value
            elif isinstance(light, Par3RGB):
                if light.dmx_root <= channel and channel < light.dmx_root + 3:
                    rgb_offset = channel - light.dmx_root
                    light.rgb_value[rgb_offset] = value
           
# This function is important else the OSC listening server doesn't shut down
# and blocks any new instance from listening on the same port
def stop():
    print('### quitting...')
    osc.stop()
    print('### done.')
    
def keyPressed():
    global lights
    if key == 'r':
        print('### resetting')
        lights = load_lights('default_lights.yaml')
        cur_index = 0
