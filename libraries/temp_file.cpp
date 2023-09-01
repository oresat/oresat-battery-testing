#include "libb6/Device.hh"
#include<string>
#include<iostream>
#include<stdint.h>


Device::Device(const std::string & location) {
	int loc_i = 0;//tracker for location index
	int path_i = 0;//tracker for path index
	bool flag = false;//check if we've found the correct charger
	libusb_device *dev;
	libusb_device **devs;
	int i = 0, j = 0;
	uint8_t path[8];//the device we're on
	uint8_t loc_path[8];//the device we want

	while (location[loc_i]) {
		if (location[loc_i] != '.' || location[loc_i] != '-') {
			std::cout << location[loc_i] << " AND " << path[path_i] << std::endl;
			++loc_i;
			loc_path[path_i] = std::stoi(location.c_str()[loc_i]);
			++path_i;
		}
		else ++loc_i;
	}

}
