import abc

# This doesn't seem to be python 2 compatible
# class Light(abc.ABC):
#     @abc.abstractmethod
#     def dmx_update(self):
#         pass
class Light():
    def dmx_update(self):
        pass

class Bulb(Light):

    def __init__(self, dmx_port=None, dmx_root=0, value=100, x=0, y=0, size=50, tag=''):
        self.dmx_port = dmx_port
        self.dmx_root = dmx_root
        self.value = value

        self.x = x
        self.y = y
        self.size = size
        self.tag = tag

    def dmx_update(self):
        try:
            self.dmx_port.setChannel(self.dmx_root, self.value)
        except Exception as error:
            print('Error setting dmx port {}, '.format(self.dmx_port) +
                  'channel {} to {}'.format(self.dmx_root, self.value))
            raise(error)


class Par3RGB(Light):

    def __init__(self, dmx_port=None, dmx_root=0, rgb_value=[100,0,0], x=0, y=0, size=50, tag=''):
        self.dmx_port = dmx_port
        self.dmx_root = dmx_root
        self.rgb_value = rgb_value

        self.x = x
        self.y = y
        self.size = size
        self.tag = tag

    def dmx_update(self):
        try:
            for offset, value in self.rgb_value:
                self.dmx_port.setChannel(self.dmx_root + offset, value)
        except Exception as error:
            print('Error setting dmx port {}, channels '.format(self.dmx_port) + 
                  '{}-{} to {}'.format(self.dmx_root, self.dmx_root+3, self.rgb_value))
            raise(error)