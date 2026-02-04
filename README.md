# ZenPacks.daviswr.NUT

ZenPack to monitor uninterruptible power supplies managed by Network UPS Tools (NUT)

## Requirements
* Network UPS Tools
* An account on the monitored host, which can
  * Log in via SSH with a key
  * Execute the `upsc` utility
* [ZenPackLib](https://help.zenoss.com/in/zenpack-catalog/open-source/zenpacklib)

## Usage
This is will only model and monitor UPSes locally configured on the host. Remote NUT servers are not supported, please monitor those as individual devices in Zenoss.

I'm not going to make any assumptions about your device class organization, so it's up to you to configure the `daviswr.cmd.NUT` modeler on the appropriate class or device.
