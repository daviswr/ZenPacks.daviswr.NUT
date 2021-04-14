""" Parses performance data from upsc """

from Products.ZenRRD.CommandParser import CommandParser
from Products.ZenUtils.Utils import prepId


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
