Device.cc is where the function is that I need to edit, using libusb functions.

The current goal is to play around with https://github.com/libusb/libusb/blob/master/examples/listdevs.c along with https://libusb.sourceforge.io/api-1.0/group__libusb__dev.html#gaa4b7b2b50a9ce2aa396b0af2b979544d

The C backend must be fixed in the aforementioned manner so that the python frontend that operates the battery chargers can actually work.

The libusb_open_with_vid_pid function will ultimately be replaced with the libusb_open function (I think). At the very least, vid pid only opens one charger so it is completely useless unless we only want to use one charger.
