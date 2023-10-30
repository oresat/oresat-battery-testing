#include "libb6/Device.hh"
#include<string>


int main() {
	b6::SysInfo obj;
	//b6::Device devObj;
	auto devA = b6::Device("1-2");

	auto devB = b6::Device("1-1.3");

	auto devC = b6::Device("1-4");

	auto devD = b6::Device("1-1.4");

	//printf("\n%d\n", devObj.getCellCount());
	
	return 0;
}
