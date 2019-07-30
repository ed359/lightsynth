# Note that the yaml folder contains the python2 source of pyyaml 5.1
import yaml
from utils.types import Bulb, Par3RGB
import os

def load_lights(yaml_file):
    with open('/Users/ewan/git/lightsynth/vlight/light_demo/default_lights.yaml') as f:
        lights = yaml.load(f, Loader=yaml.FullLoader)
    return lights

def save_lights(lights, yaml_file):
    with open(yaml_file, 'w') as f:
        yaml.dump(lights, f)
