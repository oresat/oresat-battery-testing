//The purpose of this file is to test the code in Device.cc that compares port numbers.
#include "Device.hh"
#include<string>
#include<iostream>
#include<stdint.h>
#include <string>
#include <vector>
#include <libusb.h>
#include <stdexcept>
#include "Packet.hh"
#include "Enum.hh"
#include "Error.hh"



	while (location[loc_i]) {
		if (location[loc_i] != '.' || location[loc_i] != '-') {
			std::cout << location[loc_i] << " AND " << path[path_i] << std::endl;
			++loc_i;
			loc_path[path_i] = std::stoi(location.c_str()[loc_i]);
			++path_i;
		}
		else ++loc_i;
		}
