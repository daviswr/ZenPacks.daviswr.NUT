from Products.ZenEvents.ZenEventClasses import (
    Clear,
    Info,
    Warning,
    Error,
    Critical
    )

from ZenPacks.daviswr.NUT.parsers.upsc import STATUS_FLAGS

if 'upsc|upsc_ups_status|UPS Status' == evt.eventKey:
    flag_states = dict(map(reversed, STATUS_FLAGS.items()))
    flag_order = [
        ['FSD', ],
        ['OL', 'OB', 'OFF'],
        ['CHRG', 'DISCHRG'],
        ['OVER', ],
        ['LB', 'HB'],
        ['RB', ],
        ['TRIM', 'BOOST'],
        ]
    flag_descr = {
        'OL': 'Online',
        'OB': 'On Battery',
        'LB': 'Low Battery',
        'HB': 'High Battery',
        'RB': 'Replace Battery',
        'CHRG': 'Charging',
        'DISCHRG': 'Discharging',
        'BYPASS': 'Bypass Active',
        'CAL': 'Runtime Calibration',
        'OFF': 'Offline',
        'OVER': 'Overloaded',
        'TRIM': 'Trimming Voltage',
        'BOOST': 'Boosting Voltage',
        'FSD': 'Forced Shutdown',
        }

    current = int(float(evt.current))
    states = list(flag_states.keys())
    states.sort()
    states.reverse()
    ups_flags = list()
    ups_flags_ordered = list()
    ups_descr = list()

    for state in states:
        if current - state >= 0 and state in flag_states:
            flag = flag_states[state]
            ups_flags.append(flag)
            current = current - state

    for section in flag_order:
        for flag in section:
            if flag in ups_flags:
                ups_flags_ordered.append(flag)
                ups_descr.append(flag_descr[flag])

    evt.summary = 'UPS status is {0}'.format(', '.join(ups_descr))

    if 'FSD' in ups_flags:
        evt.severity = Critical
    elif ('LB' in ups_flags
            or 'RB' in ups_flags
            or 'BYPASS' in ups_flags
            or 'OFF' in ups_flags
            or 'OVER' in ups_flags):
        evt.severity = Error
    elif ('OB' in ups_flags
            or 'DISCHRG' in ups_flags
            or 'CAL' in ups_flags
            or 'TRIM' in ups_flags
            or 'BOOST' in ups_flags):
        evt.severity = Warning
    elif 'HB' in ups_flags:
        evt.severity = Info
    elif 'OL' in ups_flags or 'CHRG' in ups_flags:
        evt.severity = Clear

    @transact
    def updateDb():
        component.UpsStatus = ' '.join(ups_flags_ordered)
    updateDb()

evt.eventClass = '/Status'
