#include<pybind11/pybind11.h>
#include<pybind11/pytypes.h>
#include<pybind11/numpy.h>
#include<string>
#include<Device.hh>
#include<Enum.hh>
#include<Error.hh>
#include<Packet.hh>

namespace py = pybind11;

//The purpose of this file is to bind libb6 via python.

PYBIND11_MODULE(libb6, m) {
	m.doc() = "PyBind11 libb6 plugin";//docstring

	//Binding from Enum.hh
	py::enum_<b6::BATTERY_TYPE>(m, "BATTERY_TYPE", py::arithmetic())	
		.value("LIPO", b6::BATTERY_TYPE::LIPO)
		.value("LIIO", b6::BATTERY_TYPE::LIIO)
		.value("LIFE", b6::BATTERY_TYPE::LIFE)
		.value("LIHV", b6::BATTERY_TYPE::LIHV)
		.value("NIMH", b6::BATTERY_TYPE::NIMH)
		.value("PB", b6::BATTERY_TYPE::PB)
		.export_values();

	py::class_<b6::SysInfo>(m, "SysInfo")
		.def(py::init<>())
		.def_readonly("cycleTime", & b6::SysInfo::cycleTime)
		.def_readonly("timeLimit", & b6::SysInfo::timeLimit)
		.def_readonly("capLimit", & b6::SysInfo::capLimit)
		.def_readonly("lowDCLimit", & b6::SysInfo::lowDCLimit)
		.def_readonly("tempLimit", & b6::SysInfo::tempLimit)
		.def_readonly("voltage", & b6::SysInfo::voltage)
		.def_property_readonly("cells", [](b6::SysInfo & s) -> py::list {
			return py::memoryview::from_buffer(
						s.cells, { 8 }, { sizeof(unsigned int) * 8 }
				);
			})
		.def_readonly("timeLimitOn", & b6::SysInfo::timeLimitOn)
		.def_readonly("capLimitOn", & b6::SysInfo::capLimitOn)
		.def_readonly("keyBuzzer", & b6::SysInfo::keyBuzzer)
		.def_readonly("systemBuzzer", & b6::SysInfo::systemBuzzer);

	py::class_<b6::ChargeInfo>(m, "ChargeInfo")
		.def(py::init<>())
		.def_readonly("state", & b6::ChargeInfo::state)
		.def_readonly("tempExt", & b6::ChargeInfo::tempExt)
		.def_readonly("tempInt", & b6::ChargeInfo::tempInt)
		.def_readonly("capacity", & b6::ChargeInfo::capacity)
		.def_readonly("time", & b6::ChargeInfo::time)
		.def_readonly("voltage", & b6::ChargeInfo::voltage)
		.def_readonly("current", & b6::ChargeInfo::current)
		.def_readonly("impendance", & b6::ChargeInfo::impendance)

		.def_property_readonly("cells", [](b6::SysInfo & s) -> py::list {
			return py::memoryview::from_buffer(
						s.cells, { 8 }, { sizeof(unsigned int) * 8 }
				);
			});

	py::class_<b6::ChargeProfile>(m, "ChargeProfile")
		.def(py::init<>())
		.def_readwrite("batteryType", & b6::ChargeProfile::batteryType)
		.def_readwrite("cellCount", & b6::ChargeProfile::cellCount)
		.def_readwrite("rPeakCount", & b6::ChargeProfile::rPeakCount)
		.def_readwrite("cycleType", & b6::ChargeProfile::cycleType)
		.def_readwrite("cycleCount", & b6::ChargeProfile::cycleCount)
		.def_readwrite("mode", & b6::ChargeProfile::mode)

		.def_readwrite("chargeCurrent", & b6::ChargeProfile::chargeCurrent)
		.def_readwrite("dischargeCurrent", & b6::ChargeProfile::dischargeCurrent)
		.def_readwrite("cellDischargeVoltage", & b6::ChargeProfile::cellDischargeVoltage)
		.def_readwrite("endVoltage", & b6::ChargeProfile::trickleCurrent);

	//Binds Device functions
	py::class_<b6::Device>(m, "Device")
		//.def(name of function), & makes pointer to function, py::arg sets argument names
		.def(py::init<>())
		.def(py::init<const std::string &>())
		//.def(py::init<const std::string &>())
		
		.def("getSysInfo", & b6::Device::getSysInfo)
		.def("getChargeInfo", & b6::Device::getChargeInfo)

		.def("getCoreType", & b6::Device::getCoreType)
		.def("getUpgradeType", & b6::Device::getUpgradeType)
		.def("getLanguageID", & b6::Device::getLanguageID)
		.def("getCustomerID", & b6::Device::getCustomerID)
		.def("getHWVersion", & b6::Device::getHWVersion)
		.def("getSWVersion", & b6::Device::getSWVersion)
		.def("isEncrypted", & b6::Device::isEncrypted)
		.def("getCellCount", & b6::Device::getCellCount)
		.def("getDefaultChargeProfile", [](b6::Device & d, b6::BATTERY_TYPE t) {
			return d.getDefaultChargeProfile(t);
				})

		.def("setCycleTime", & b6::Device::setCycleTime, py::arg("cycleTime"))
		.def("setTimeLimit", & b6::Device::setTimeLimit, py::arg("enabled"), py::arg("limit"))
		.def("setCapacityLimit", & b6::Device::setCapacityLimit, py::arg("enabled"), py::arg("limit"))
		.def("setTempLimit", & b6::Device::setTempLimit, py::arg("limit"))
		.def("setBuzzers", & b6::Device::setBuzzers, py::arg("system"), py::arg("key"))

		.def("stopCharging", & b6::Device::stopCharging)
		.def("startCharging", & b6::Device::startCharging, py::arg("profile"))

		.def("isBatteryLi", [](b6::Device & d, b6::BATTERY_TYPE t) {
			return d.isBatteryLi(t);
				})

		.def("isBatteryNi", [](b6::Device & d, b6::BATTERY_TYPE t) {
			return d.isBatteryNi(t);
				});

	//Binding from Error.hh
	py::register_exception<b6::ErrorConnectionBroken>(m, "ErrorConnectionBroken");
	py::register_exception<b6::ErrorCellVoltageInvalid>(m, "ErrorCellVoltageInvalid");
	py::register_exception<b6::ErrorBalanceConnection>(m, "ErrorBalanceConnection");
	py::register_exception<b6::ErrorNoBattery>(m, "ErrorNoBattery");
	py::register_exception<b6::ErrorCellNumberIncorrect>(m, "ErrorCellNumberIncorrect");
	py::register_exception<b6::ErrorConnectionMainPort>(m, "ErrorConnectionMainPort");
	py::register_exception<b6::ErrorBatteryFull>(m, "ErrorBatteryFull");
	py::register_exception<b6::ErrorChargeNotNeeded>(m, "ErrorChargeNotNeeded");
	py::register_exception<b6::ErrorCellHighVoltage>(m, "ErrorCellHighVoltage");
	py::register_exception<b6::ErrorIntTempTooHigh>(m, "ErrorIntTempTooHigh");
	py::register_exception<b6::ErrorExtTempTooHigh>(m, "ErrorExtTempTooHigh");
	py::register_exception<b6::ErrorDCInTooLow>(m, "ErrorDCInTooLow");
	py::register_exception<b6::ErrorOverTimeLimit>(m, "ErrorOverTimeLimit");
	py::register_exception<b6::ErrorOverCapacityLimit>(m, "ErrorOverCapacityLimit");
	py::register_exception<b6::ErrorReversePolarity>(m, "ErrorReversePolarity");
	
	py::register_exception<b6::ErrorControlFail>(m, "ErrorControlFail");
	py::register_exception<b6::ErrorBreakDown>(m, "ErrorBreakDown");
	py::register_exception<b6::ErrorInputFail>(m, "ErrorInputDown");
	py::register_exception<b6::ErrorUnknown>(m, "ErrorUnknown");

}



/*
Neat Python Tip:
 *def example(abc: str) -> float: #specifies return type float, abc is a string, print out that arg type is string
 	print(abc)
	return 1.5
 */

