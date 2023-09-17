#include<iostream>
#include <string>
#include <vector>
#include <libusb.h>
#include <stdexcept>


int main() {

    libusb_context *m_libusbCtx{};
    libusb_device_handle *m_dev;
    bool m_hadKernelDriver = false;
  std::string location = "1-1.4";
  int loc_i{0};                   // tracker for location index
  int path_i{0};                  // tracker for path index
  libusb_device *b6dev = nullptr; // check if we've b6dev the correct charger
  libusb_device *dev;
  libusb_device **devs;
  int i = 0, j = 0;
  uint8_t path[8];     // the device we're on
  uint8_t loc_path[8]; // the device we want

  // Put string nums into path array.

  /*
          if (location[1] == '-') bus_num = location[0];//for 1 digit bus
     numbers else bus_num = (10 * (location[0] - '0')) + (location[1] - '0');
          //if bus number is more than two digits, program won't wor
  */
  while (location[loc_i]) {
    if (location[loc_i] != '.' && location[loc_i] != '-') {
      int to_add = location[loc_i] - '0';
      loc_path[path_i] = to_add;
      ++loc_i;
      ++path_i;
    } else
      ++loc_i;
  }

  int err = libusb_init(&m_libusbCtx);
  if (err != 0) {
    throw std::runtime_error("libusb err: " + std::to_string(err));
  }

  err = libusb_get_device_list(NULL, &devs); // list is OPEN
  if (err < 0) {
    throw std::runtime_error("libusb err: " + std::to_string(err));
  }

  while ((dev = devs[i++]) != NULL) {
    struct libusb_device_descriptor desc;
    err = libusb_get_device_descriptor(dev, &desc);
    if (err < 0) {
      throw std::runtime_error("libusb err: " + std::to_string(err));
    }

    err = libusb_get_port_numbers(dev, path,
                                  path_i /* Ryan's version path_i is k */);
    if (err < 0)
      continue;
    uint8_t bus_num = libusb_get_bus_number(dev);

    if (bus_num != loc_path[0] || bus_num == 0)
      continue; // go to next device
                // bus num does not match

    // arg for libusb_get_bus_number ???
    for (j = 1; j < err; j++) {
      if (path[j] != loc_path[j]) {
        b6dev = nullptr;
        break;
      }
      b6dev = dev;
    }
    if (b6dev != nullptr)
      break;
  }

  // free_device_list expects all unwanted devices to be unreferenced
  while ((dev = devs[i++]) != NULL) {
    if (b6dev != dev) {
      libusb_unref_device(dev);
    }
  }

  libusb_free_device_list(devs, 0);

  if (b6dev == nullptr) {
    throw std::runtime_error("DID NOT FIND USB DEVICE AT ALL!");
  }

  dev = b6dev; // dev is device last accessed, but b6dev is the correct device

  if (dev == nullptr)
    throw std::runtime_error("libusb did not find device");
  err = libusb_open(dev, &m_dev); // Device_Names.c contents will be in here
  if (err < 0) {
    throw std::runtime_error("cannot find/open b6 device");
  }

  if (libusb_kernel_driver_active(m_dev, 0) == 1) {
    m_hadKernelDriver = true;
    err = libusb_detach_kernel_driver(m_dev, 0);
    if (err != 0) {
      throw std::runtime_error("cannot detach kernel driver, err: " +
                               std::to_string(err));
    }
  }
  err = libusb_claim_interface(m_dev, 0);
  if (err != 0) {
    throw std::runtime_error("cannot claim interface 0, err: " +
                             std::to_string(err));
  }

	std::cout << m_dev << std::endl;
  // deconstructor
  if (m_dev != nullptr) {
    libusb_release_interface(m_dev, 0);
    if (m_hadKernelDriver) {
      libusb_attach_kernel_driver(m_dev, 0);
    }
    libusb_close(m_dev);
  }
  libusb_exit(m_libusbCtx);

  return 0;
}
