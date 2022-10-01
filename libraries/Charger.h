#ifndef CHARGER_H
#define CHARGER_H

#include <python3.8/Python.h>
#include <python3.8/structmember.h>
#include "Device.hh"
#include "Enum.hh"

// Charger type
typedef struct {
    PyObject_HEAD
    /* Type-specific fields go here. */
    b6::Device* charger;
    int number;
} ChargerObject;

void Charger_dealloc(ChargerObject* self);
PyObject* Charger_str(PyObject *self);
PyObject* Charger_new(PyTypeObject* type, PyObject* args, PyObject* kwds);
int Charger_init(ChargerObject* self, PyObject* args, PyObject* kwds);

PyObject* Charger_test(ChargerObject* self, PyObject *Py_UNUSED(ignored));

PyObject* Charger_getSysInfo(ChargerObject* self, PyObject *Py_UNUSED(ignored));
PyObject* Charger_getChargeInfo(ChargerObject* self, PyObject *Py_UNUSED(ignored));

PyObject* Charger_getCoreType(ChargerObject* self, PyObject *Py_UNUSED(ignored));
PyObject* Charger_getUpgradeType(ChargerObject* self, PyObject *Py_UNUSED(ignored));
PyObject* Charger_getLanguageID(ChargerObject* self, PyObject *Py_UNUSED(ignored));
PyObject* Charger_getCustomerID(ChargerObject* self, PyObject *Py_UNUSED(ignored));
PyObject* Charger_getHWVersion(ChargerObject* self, PyObject *Py_UNUSED(ignored));
PyObject* Charger_getSWVersion(ChargerObject* self, PyObject *Py_UNUSED(ignored));
PyObject* Charger_isEncrypted(ChargerObject* self, PyObject *Py_UNUSED(ignored));
PyObject* Charger_getCellCount(ChargerObject* self, PyObject *Py_UNUSED(ignored));
PyObject* Charger_getDefaultChargeProfile(ChargerObject* self, PyObject* args);

PyObject* Charger_setCycleTime(ChargerObject* self, PyObject* args);
PyObject* Charger_setTimeLimit(ChargerObject* self, PyObject* args);
PyObject* Charger_setCapacityLimit(ChargerObject* self, PyObject* args);
PyObject* Charger_setTempLimit(ChargerObject* self, PyObject* args);
PyObject* Charger_setBuzzers(ChargerObject* self, PyObject* args);

PyObject* Charger_stopCharging(ChargerObject* self, PyObject* args);
PyObject* Charger_startCharging(ChargerObject* self, PyObject* args);

// std::string getCoreType() { return m_coreType; };
// int getUpgradeType() { return m_upgradeType; };
// int getLanguageID() { return m_languageID; };
// int getCustomerID() { return m_customerID; };
// double getHWVersion() { return m_hwVersion; };
// double getSWVersion() { return m_swVersion; };
// bool isEncrypted() { return m_isEncrypted; };
// int getCellCount() { return m_cellCount; };
// ChargeProfile getDefaultChargeProfile(BATTERY_TYPE type);

extern PyMemberDef Charger_members[];
extern PyMethodDef Charger_methods[];
extern PyTypeObject ChargerType;

// System Info Object

typedef struct {
    PyObject_HEAD
    /* Type-specific fields go here. */
    unsigned int cycleTime, timeLimit, capLimit, lowDCLimit, tempLimit, voltage;
    bool timeLimitOn, capLimitOn, keyBuzzer, systemBuzzer;
    PyListObject* cells;
} SysInfoObject;

void SysInfo_dealloc(SysInfoObject* self);
PyObject* SysInfo_str(PyObject *self);
PyObject* SysInfo_new(PyTypeObject* type, PyObject* args, PyObject* kwds);
int SysInfo_init(SysInfoObject* self, PyObject* args, PyObject* kwds);

extern PyMemberDef SysInfo_members[];
extern PyMethodDef SysInfo_methods[];
extern PyTypeObject SysInfoType;

// Charge Info Object

typedef struct {
    PyObject_HEAD
    /* Type-specific fields go here. */
    unsigned int state, tempExt, tempInt, capacity, time, voltage, current, impendance;
    PyListObject* cells;
} ChargeInfoObject;

void ChargeInfo_dealloc(ChargeInfoObject* self);
PyObject* ChargeInfo_str(PyObject *self);
PyObject* ChargeInfo_new(PyTypeObject* type, PyObject* args, PyObject* kwds);
int ChargeInfo_init(ChargeInfoObject* self, PyObject* args, PyObject* kwds);

extern PyMemberDef ChargeInfo_members[];
extern PyMethodDef ChargeInfo_methods[];
extern PyTypeObject ChargeInfoType;

// Charge profile Object

typedef struct {
    PyObject_HEAD
    /* Type-specific fields go here. */
    uint8_t batteryType, cellCount, rPeakCount, cycleType, cycleCount, mode;
    uint16_t chargeCurrent, dischargeCurrent, cellDischargeVoltage, endVoltage, trickleCurrent;
} ChargeProfileObject;

void ChargeProfile_dealloc(ChargeProfileObject* self);
PyObject* ChargeProfile_str(PyObject *self);
PyObject* ChargeProfile_new(PyTypeObject* type, PyObject* args, PyObject* kwds);
int ChargeProfile_init(ChargeProfileObject* self, PyObject* args, PyObject* kwds);

PyObject* ChargeProfile_getTypeString(ChargeProfileObject* self, PyObject *Py_UNUSED(ignored));

extern PyMemberDef ChargeProfile_members[];
extern PyMethodDef ChargeProfile_methods[];
extern PyTypeObject ChargeProfileType;

#endif
