""" Library of misc NUT ZenPack-related values and methods """

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
    'ALARM': 16384,
    }


def decode_status(current):
    """ Decodes ups.status string from integer value """

    flag_states = dict((value, key) for key, value in STATUS_FLAGS.items())
    flag_order = [
        ['ALARM', ],
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
        'ALARM': 'Alarm',
        }

    current = int(float(current))
    states = sorted(flag_states.keys(), reverse=True)
    ups_flags = list()
    ups_flags_ordered = list()
    ups_descr = list()

    for state in states:
        if current - state >= 0 and state in flag_states:
            ups_flags.append(flag_states[state])
            current = current - state

    for section in flag_order:
        for flag in section:
            if flag in ups_flags:
                ups_flags_ordered.append(flag)
                ups_descr.append(flag_descr[flag])

    return {
        'flags': ' '.join(ups_flags_ordered),
        'descr': ', '.join(ups_descr),
        }


def encode_status(ups_status):
    """ Encodes ups.status string to integer value """
    return sum(STATUS_FLAGS[flag] for flag in set(ups_status.split(' ')))
