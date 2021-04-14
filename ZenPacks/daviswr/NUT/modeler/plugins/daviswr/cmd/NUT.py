""" Models NUT power devices via SSH """

from Products.DataCollector.plugins.CollectorPlugin import CommandPlugin
from Products.DataCollector.plugins.DataMaps import ObjectMap


class NUT(CommandPlugin):
    """ Models NUT power devices via SSH """

    relname = 'nutDevices'
    modname = 'ZenPacks.daviswr.NUT.NutDevice'

    commands = [
        '$ZENOTHING',
        'for UPS in $(upsc -l 2>/dev/null)',
        'do echo "device.name: $UPS"',
        'upsc $UPS 2>/dev/null',
        'echo "--------"',
        'done',
        ]

    command = ';'.join(commands)

    def process(self, device, results, log):
        """ Generates RelationshipMaps from Command output """

        log.info(
            'Modeler %s processing data for device %s',
            self.name(),
            device.id
            )
        rm = self.relMap()

        """ Example output

        device.name: rs1200
        battery.charge: 100
        battery.charge.low: 10
        battery.charge.warning: 50
        battery.date: 2001/09/25
        battery.mfr.date: 2007/09/05
        battery.runtime: 750
        battery.runtime.low: 120
        battery.type: PbAc
        battery.voltage: 26.6
        battery.voltage.nominal: 24.0
        device.mfr: American Power Conversion
        device.model: Back-UPS RS 1200
        device.serial: BB0736005619
        device.type: ups
        driver.name: usbhid-ups
        driver.parameter.pollfreq: 30
        driver.parameter.pollinterval: 2
        driver.parameter.port: /dev/usb/hiddev0
        driver.parameter.synchronous: no
        driver.version: 2.7.4
        driver.version.data: APC HID 0.96
        driver.version.internal: 0.41
        input.sensitivity: medium
        input.transfer.high: 132
        input.transfer.low: 97
        input.transfer.reason: input voltage out of range
        input.voltage: 120.0
        input.voltage.nominal: 120
        ups.beeper.status: enabled
        ups.delay.shutdown: 20
        ups.firmware: 8.g3 .D
        ups.firmware.aux: g3
        ups.load: 49
        ups.mfr: American Power Conversion
        ups.mfr.date: 2007/09/05
        ups.model: Back-UPS RS 1200
        ups.productid: 0002
        ups.realpower.nominal: 780
        ups.serial: BB0736005619
        ups.status: OL
        ups.test.result: No test initiated
        ups.timer.reboot: 0
        ups.timer.shutdown: -1
        ups.vendorid: 051d
        --------
        """

        devices = results.split('--------')

        for device in devices:
            dev_map = dict()
            for line in device.splitlines():
                if ': ' in line:
                    key = ''
                    key_raw, value = line.split(': ')
                    for term in key_raw.split('.'):
                        key += term.title()
                    if value.isdigit():
                        dev_map[key] = int(value)
                    else:
                        try:
                            dev_map[key] = float(value)
                        except ValueError:
                            dev_map[key] = value

            if 'DeviceName' in dev_map:
                if 'UpsFirmware' in dev_map:
                    dev_map['UpsFirmware'] = dev_map['UpsFirmware'].replace(
                        ' .',
                        '.'
                        )

                dev_type = dev_map.get('DeviceType', 'NutDevice')
                modname = 'ZenPacks.daviswr.NUT.'
                modname += (dev_type if 'NutDevice' == dev_type
                            else dev_type.upper())

                dev_map['id'] = self.prepId(dev_map['DeviceName'])
                dev_map['title'] = dev_map['DeviceName']
                rm.append(ObjectMap(
                    modname=modname,
                    data=dev_map
                    ))

        log.debug('%s RelMap:\n%s', self.name(), str(rm))
        return rm
