import abc
import math

# Scaling functions
def float_to_int8_linear(value):
    scaled_value = int(value * 255)
    scaled_value = max(0, scaled_value)
    scaled_value = min(255, scaled_value)
    return scaled_value

max_scaling = 0.4
def exp_scaling_fn(exp_rate, value_0_1):
    # scales from 0 to max_val exponentially so more control in low end
    return  ( math.pow(exp_rate, value_0_1) - 1 ) /(exp_rate - 1)

def float_to_int8_exp(value, exp_rate=1.7):
    scaled_value = exp_scaling_fn(exp_rate, value)
    scaled_value = scaled_value * 255
    scaled_value = max(0, scaled_value)
    scaled_value = min(255, scaled_value)
    scaled_value = int(scaled_value * max_scaling)
    return scaled_value

# This doesn't seem to be python 2 compatible
# class Light(abc.ABC):
#     @abc.abstractmethod
#     def dmx_update(self):
#         pass
class Light():
    def dmx_update(self):
        pass

class Bulb(Light):

    def __init__(self, dmx_port=None, dmx_root=0, value=0.4, x=0, y=0, size=50, tag=''):
        self.dmx_port = dmx_port
        self.dmx_root = dmx_root
        self.value = value

        self.x = x
        self.y = y
        self.size = size
        self.tag = tag

    def dmx_update(self):
        try:
            self.dmx_port.setChannel(self.dmx_root, 
                                     float_to_int8_exp(self.value))
        except Exception as error:
            print('Error setting dmx port {}, '.format(self.dmx_port) +
                  'channel {} to {}'.format(self.dmx_root, self.value))
            raise(error)


class Par3RGB(Light):

    def __init__(self, dmx_port=None, dmx_root=0, rgb_value=[0.4,0,0], x=0, y=0, size=50, tag=''):
        self.dmx_port = dmx_port
        self.dmx_root = dmx_root
        self.rgb_value = rgb_value

        self.x = x
        self.y = y
        self.size = size
        self.tag = tag

    def dmx_update(self):
        try:
            for offset, value in enumerate(self.rgb_value):
                self.dmx_port.setChannel(self.dmx_root + offset, 
                                         float_to_int8_exp(value))
        except Exception as error:
            print('Error setting dmx port {}, channels '.format(self.dmx_port) + 
                  '{}-{} to {}'.format(self.dmx_root, self.dmx_root+3, self.rgb_value))
            raise(error)