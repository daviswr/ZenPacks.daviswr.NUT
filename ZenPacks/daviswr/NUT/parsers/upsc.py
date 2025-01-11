""" Parses performance data from upsc """

from Products.ZenEvents import Event
from Products.ZenRRD.CommandParser import CommandParser
from Products.ZenUtils.Utils import prepId

from ZenPacks.daviswr.NUT.lib.util import encode_status


class upsc(CommandParser):
    """ Parses performance data from upsc """

    def processResults(self, cmd, result):
        """ Returns metrics from command output """
        components = dict()
        devices = cmd.result.output.split('--------')

        for device in devices:
            dev_map = dict()
            dev_name = ''
            dev_type = ''
            alarm = ''
            for line in device.splitlines():
                if ': ' in line:
                    key, value = line.split(': ', 1)
                    key = key.replace('.', '_')
                    if 'device_name' == key:
                        dev_name = value
                    elif 'device_type' == key:
                        dev_type = value
                    elif 'ups_status' == key:
                        dev_map[key] = encode_status(value)
                    elif key.endswith('alarm'):
                        alarm = line.replace('.', ' ')
                    elif value.isdigit():
                        dev_map[key] = int(value)
                    else:
                        try:
                            dev_map[key] = float(value)
                        except ValueError:
                            continue

            if dev_name:
                components[prepId(dev_name)] = dev_map
                if 'ups' == dev_type:
                    alarm = alarm.replace('ups', 'UPS')
                    evt_cls = '/HW/Power/UPS'
                else:
                    evt_cls = '/HW/Power'

                result.events.append({
                    'device': cmd.deviceConfig.device,
                    'component': dev_name,
                    'severity': Event.Warning if alarm else Event.Clear,
                    'eventKey': 'upsc',
                    'eventClass': evt_cls,
                    'summary': alarm if alarm else 'No alarms present',
                    })

        for point in cmd.points:
            if point.component in components:
                values = components[point.component]
                if point.id in values:
                    result.values.append((point, values[point.id]))
