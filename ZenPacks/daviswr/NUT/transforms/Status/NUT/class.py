from Products.ZenEvents.ZenEventClasses import (
    Clear,
    Info,
    Warning,
    Error,
    Critical
    )

from ZenPacks.daviswr.NUT.lib.util import decode_status

if 'upsc|upsc_ups_status|UPS Status' == evt.eventKey:
    status = decode_status(evt.current)
    flags = status['flags']
    descr = status['descr']

    evt.summary = 'UPS status is {0}'.format(descr)

    if 'FSD' in flags:
        evt.severity = Critical
    elif ('LB' in flags
            or 'RB' in flags
            or 'BYPASS' in flags
            or 'OFF' in flags
            or 'OVER' in flags):
        evt.severity = Error
    elif ('OB' in flags
            or 'DISCHRG' in flags
            or 'CAL' in flags
            or 'TRIM' in flags
            or 'BOOST' in flags):
        evt.severity = Warning
    elif 'HB' in flags:
        evt.severity = Info
    elif 'OL' in flags or 'CHRG' in flags:
        evt.severity = Clear

    if component and hasattr(component, 'UpsStatus'):
        @transact
        def updateDb():
            component.UpsStatus = flags
        updateDb()

evt.eventClass = '/Status'
