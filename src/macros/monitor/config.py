import os
from configobj import ConfigObj
from evdev import InputDevice, list_devices

CONFIG_DIR = os.path.expanduser("~/.config/rdt")
CONFIG_FILE = os.path.join(CONFIG_DIR, 'rdt.ini')


def write_default_cfg(config: ConfigObj):
    config['left_k'] = 30
    config['center_k'] = 48
    config['right_k'] = 46
    config.write()
    print(" * config saved")


def get_footswitch_keys():
    try:
        os.path.exists(CONFIG_FILE)
    except:
        write_default_cfg()

    config = ConfigObj(CONFIG_FILE)

    try:
        os.makedirs(CONFIG_DIR)
        config = write_default_cfg(config)
    except FileExistsError:
        print(' * config file found')

    try:
        left_k = config['left_k']
        center_k = config['center_k']
        right_k = config['right_k']
    except:
        write_default_cfg(config)
    finally:
        left_k = config.as_int('left_k')
        center_k = config.as_int('center_k')
        right_k = config.as_int('right_k')
    return left_k, center_k, right_k


def get_footswitch_device():
    devices = [InputDevice(path) for path in list_devices()]
    for device in devices:
        if 'keyboard' in device.name.lower():
            device = device
            return device