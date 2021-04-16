""" Parses performance data from upsc """

from Products.ZenRRD.CommandParser import CommandParser
from Products.ZenUtils.Utils import prepId

STATUS_FLAGS = {
    # Clear
    'OL': 1,
    'CHRG': 2,
    # Info
    'HB': 4,
    # Warning
    'OB': 8,
    'DISCHRG': 16,
    'CAL': 32,
    'TRIM': 64,
    'BOOST': 128,
    # Error
    'LB': 256,
    'RB': 512,
    'BYPASS': 1024,
    'OFF': 2048,
    'OVER': 4096,
    # Critical
    'FSD': 8192,
    }


class upsc(CommandParser):
    """ Parses performance data from upsc """

    def processResults(self, cmd, result):
        components = dict()
        devices = cmd.result.output.split('--------')

        for device in devices:
            dev_map = dict()
            dev_name = ''
            for line in device.splitlines():
                if ': ' in line:
                    key, value = line.split(': ')
                    key = key.replace('.', '_')
                    if 'device_name' == key:
                        dev_name = value
                    elif 'ups_status' == key:
                        flags = set(value.split(' '))
                        dev_map[key] = sum(STATUS_FLAGS[flag] for flag in flags)  # noqa
                    elif value.isdigit():
                        dev_map[key] = int(value)
                    else:
                        try:
                            dev_map[key] = float(value)
                        except ValueError:
                            continue

            if dev_name:
                components[prepId(dev_name)] = dev_map

        for point in cmd.points:
            if point.component in components:
                values = components[point.component]
                if point.id in values:
                    result.values.append((point, values[point.id]))
