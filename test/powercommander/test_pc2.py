#!/usr/bin/python

import usb.core
import usb.util
import time

# find our device
dev = usb.core.find(idVendor=0x10b6, idProduct=0x0001)

# was it found?
if dev is None:
    raise ValueError('Device not found')

if dev.is_kernel_driver_active(0):
    reattach = True
    dev.detach_kernel_driver(0)

# set the active configuration. With no arguments, the first
# configuration will be the active one
dev.set_configuration()

# get an endpoint instance
cfg = dev.get_active_configuration()
intf = cfg[(0,0)]

ep = usb.util.find_descriptor(
    intf,
    # match the first OUT endpoint
    custom_match = \
    lambda e: \
        usb.util.endpoint_direction(e.bEndpointAddress) == \
        usb.util.ENDPOINT_OUT)

assert ep is not None

msg = '\x00\xE1\x00\x00\x03'
print dev.ctrl_transfer(0x21, 0x9, 0x300, 0, msg) # == len(msg)

time.sleep(0.5)

msg = '\x00\xE1\x00\x00\x03'
print dev.ctrl_transfer(0x21, 0x9, 0x300, 0, msg) # == len(msg)

while True:
    try:
        #print dev.read(0x81,20)
        ep.write('\x81')
        print ep.read(32)
    except:
        pass

    time.sleep(0.1)


# write the data
#print ep.write('\x00\xE1\x00\x00\x03')
#print ep.write('\x21\x09\x00\x03\x00\x00\x05\x00')
