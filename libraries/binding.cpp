#include<pybind11/pybind11.h>
#include<pybind11/pytypes.h>
#include<pybind11/numpy.h>
#include<string>
#include<libb6/Device.hh>
#include<libb6/Enum.hh>
#include<libb6/Error.hh>
#include<libb6/Packet.hh>

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
		.def_readwrite("cycleTime", & b6::SysInfo::cycleTime)
		.def_readwrite("timeLimit", & b6::SysInfo::timeLimit)
		.def_readwrite("capLimit", & b6::SysInfo::capLimit)
		.def_readwrite("lowDCLimit", & b6::SysInfo::lowDCLimit)
		.def_readwrite("tempLimit", & b6::SysInfo::tempLimit)
		.def_readwrite("voltage", & b6::SysInfo::voltage)
		.def_property("cells", [](b6::SysInfo & s) -> py::array
		{
			auto dtype = py::dtype(py::format_descriptor<unsigned int>::format());	
			auto base = py::array(dtype, {8}, sizeof(unsigned int));
			return py::array(dtype, {8}, {sizeof(unsigned int)}, b6::SysInfo.cells, base);
		}, [](b6::SysInfo & s) {})

		.def_readwrite("timeLimitOn", & b6::SysInfo::timeLimitOn)
		.def_readwrite("capLimitOn", & b6::SysInfo::capLimitOn)
		.def_readwrite("keyBuzzer", & b6::SysInfo::keyBuzzer)
		.def_readwrite("systemBuzzer", & b6::SysInfo::systemBuzzer);
/*
	py::class_<b6::ChargeInfo>(m, "ChargeInfo")
		.def(py::init<>())
		.def_readwrite("state", & b6::ChargeInfo::state)
		.def_readwrite("tempExt", & b6::ChargeInfo::tempExt)
		.def_readwrite("tempInt", & b6::ChargeInfo::tempInt)
		.def_readwrite("capacity", & b6::ChargeInfo::capacity)
		.def_readwrite("time", & b6::ChargeInfo::time)
		.def_readwrite("voltage", & b6::ChargeInfo::voltage)
		.def_readwrite("current", & b6::ChargeInfo::current)
		.def_readwrite("impendance", & b6::ChargeInfo::impendance);
		//.def_readwrite("cells", & b6::ChargeInfo::cells);

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
		.def("getDefaultChargeProfile", & b6::Device::getDefaultChargeProfile, py::arg("type"))

		.def("setCycleTime", & b6::Device::setCycleTime, py::arg("cycleTime"))
		.def("setTimeLimit", & b6::Device::setTimeLimit, py::arg("enabled"), py::arg("limit"))
		.def("setCapacityLimit", & b6::Device::setCapacityLimit, py::arg("enabled"), py::arg("limit"))
		.def("setTempLimit", & b6::Device::setTempLimit, py::arg("limit"))
		.def("setBuzzers", & b6::Device::setBuzzers, py::arg("system"), py::arg("key"))

		.def("stopCharging", & b6::Device::stopCharging)
		.def("startCharging", & b6::Device::startCharging, py::arg("profile"))

		.def("isBatteryLi", & b6::Device::isBatteryLi, py::arg("type"))
		.def("isBatteryNi", & b6::Device::isBatteryNi, py::arg("type"));

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

	*/
}



/*
 *def example(abc: str) -> float: #specifies return type float, abc is a string, print out that arg type is string
 	print(abc)
	return 1.5
 */

/*
  enum class BATTERY_TYPE : uint8_t {
    LIPO                    = 0x00,
    LIIO                    = 0x01,
    LIFE                    = 0x02,
    LIHV                    = 0x03,
    NIMH                    = 0x04,
    NICD                    = 0x05,
    PB                      = 0x06,
  };
*/
