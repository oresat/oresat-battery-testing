import usb.core
import usb.util
import sys
import u6

"""
PyUSB is mostly to talk to chargers. LabJack functions through u6. LabJack doesn't need pyusb.
In other words, just use u6.function() to talk to LabJack. Write PyUSB to replace libb6 and talk
to the chargers.

"""

"""__USB Hierarchy__
Device: The hardware device plugged in with a USB cable. A software object representing it.
Configuration: The mode the hardware device is in. The labjack only has one config. 
               The active configuration is whichever config you're currently using.
Interface: The specific feature within the configuration you are utilizing. For example:
           audio channel versus video channel versus some sort of debugging channel.
Endpoint: The endpoint (badly named imo) simply refers to a data transfer conduit. Software term
          is a "pipe". An endpoint is unidirectional: either OUT or IN.

          Notably, the endpoint requires a specific interface.
"""

#Find the labjack device.
labjack = usb.core.find(idVendor = 0x0CD5, idProduct = 0x0006)

#Throw error if no device.
if labjack is None:
  raise ValueError("Labjack device not found!")

#Set configuration to to the first config found. I believe the labjack U6 only has one anyway.
labjack.set_configuration()

#Get the endpoint --> where specifically we will send data to the usb device.
#Remember the configuration we chose above.
labjack_config = labjack.get_active_configuration()

#Theoretically we could have said "labjack_config = labjack.set_configuration()" same result.

#Establish interface - specifically we are getting the first interface.
labjack_interface = labjack_config[(0,0)] 

#Find the first endpoint that lets us talk to the labjack. The lambda function checks each
#potential endpoint.
labjack_endpoint = usb.util.find_descriptor(labjack_interface, custom_match = lambda endp:
                                            usb.util.endpoint_direction(endp.bEndpointAddress)
                                            == usb.util.ENDPOINT_OUT)

"""
#This function accomplishes the same task as the lambda function above, for clarity.
def find_out_endpoint(device):
    for endp in device:
        if usb.util.endpoint_direction(endp.bEndpointAddress) == usb.util.ENDPOINT_OUT:
            return 
    return None

#And then you would find the endpoint below as follows.

labjack_endpoint = usb.util.find_descriptor(labjack_interface, custom_match = 
                                            find_out_endpoint(labjack_interface))
"""

#Send a message to the labjack.
if labjack_endpoint is not None:
  labjack_endpoint.write("Hello, Labjack! We come in peace!")
else print("The endpoint is null.")


