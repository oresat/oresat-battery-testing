/*
 * The purpose of this document is to get the device list (of chargers),
 * with the ultimate intention of being able to pass in the device path
 * into the libusb_open function (in Device.cc?). This will let the udev
 * work with python.
 * 
 * The algorithm: find the usb port number for each charger and save them in memory.
 * Then to call the chargers, compare the port number in memory to the port number we
 * find.
 *
 * Note that port numbers are fixed (according to where the usb cords are 
 * plugged into on the board, and eventually on the compter).
 *
 * Compile with: "cc confusion.c `pkg-config --libs --cflags libusb-1.0`"
 */

#include<stdio.h>

#include<libusb.h>

static void print_devs(libusb_device **devs)
{
	libusb_device *dev;
	int i = 0, j = 0;
	uint8_t path[8]; 

	while ((dev = devs[i++]) != NULL) {
		struct libusb_device_descriptor desc;
		int r = libusb_get_device_descriptor(dev, &desc);
		if (r < 0) {
			fprintf(stderr, "failed to get device descriptor");
			return;
		}

		printf("%04x:%04x (bus %d, device %d)",
			desc.idVendor, desc.idProduct,
			libusb_get_bus_number(dev), libusb_get_device_address(dev));

		r = libusb_get_port_numbers(dev, path, sizeof(path));
		if (r > 0) {
			printf(" path: %d", path[0]);
			for (j = 1; j < r; j++)
				printf(".%d", path[j]);
		}
		printf("\n");
	}
}

int main(void)
{
	libusb_device **devs;
	int r;
	ssize_t cnt;

	r = libusb_init(NULL);//_context
	if (r < 0)
		return r;

	cnt = libusb_get_device_list(NULL, &devs);
	if (cnt < 0){
		libusb_exit(NULL);
		return (int) cnt;
	}

	print_devs(devs);
	libusb_free_device_list(devs, 1);

	libusb_exit(NULL);
	return 0;
}
