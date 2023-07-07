#include "libb6/Device.hh"
#include "libb6/Packet.hh"
#include "libb6/Enum.hh"
#include "Charger.h"

#define BOOL(b) ((b) ? "True" : "False")

// The main charger object
//
//  ██████ ██   ██  █████  ██████   ██████  ███████ ██████
// ██      ██   ██ ██   ██ ██   ██ ██       ██      ██   ██
// ██      ███████ ███████ ██████  ██   ███ █████   ██████
// ██      ██   ██ ██   ██ ██   ██ ██    ██ ██      ██   ██
//  ██████ ██   ██ ██   ██ ██   ██  ██████  ███████ ██   ██
//
PyMemberDef Charger_members[] = {
  {"number", T_INT, offsetof(ChargerObject, number), 0,
     "charger number"},
  {NULL}
};

PyMethodDef Charger_methods[] = {
  {"test"                     , (PyCFunction) Charger_test                     , METH_NOARGS,  "Testit Now"                   },
  {"getSysInfo"               , (PyCFunction) Charger_getSysInfo               , METH_NOARGS,  "func getSysInfo"              },
  {"getChargeInfo"            , (PyCFunction) Charger_getChargeInfo            , METH_NOARGS,  "func getChargeInfo"           },
  {"getCoreType"              , (PyCFunction) Charger_getCoreType              , METH_NOARGS,  "func getCoreType"             },
  {"getUpgradeType"           , (PyCFunction) Charger_getUpgradeType           , METH_NOARGS,  "func getUpgradeType"          },
  {"getLanguageID"            , (PyCFunction) Charger_getLanguageID            , METH_NOARGS,  "func getLanguageID"           },
  {"getCustomerID"            , (PyCFunction) Charger_getCustomerID            , METH_NOARGS,  "func getCustomerID"           },
  {"getHWVersion"             , (PyCFunction) Charger_getHWVersion             , METH_NOARGS,  "func getHWVersion"            },
  {"getSWVersion"             , (PyCFunction) Charger_getSWVersion             , METH_NOARGS,  "func getSWVersion"            },
  {"isEncrypted"              , (PyCFunction) Charger_isEncrypted              , METH_NOARGS,  "func isEncrypted"             },
  {"getCellCount"             , (PyCFunction) Charger_getCellCount             , METH_NOARGS,  "func getCellCount"            },
  {"getDefaultChargeProfile"  , (PyCFunction) Charger_getDefaultChargeProfile  , METH_VARARGS, "func getDefaultChargeProfile" },
  {"setCycleTime"             , (PyCFunction) Charger_setCycleTime             , METH_VARARGS, "func setCycleTime"            },
  {"setTimeLimit"             , (PyCFunction) Charger_setTimeLimit             , METH_VARARGS, "func setTimeLimit"            },
  {"setCapacityLimit"         , (PyCFunction) Charger_setCapacityLimit         , METH_VARARGS, "func setCapacityLimit"        },
  {"setTempLimit"             , (PyCFunction) Charger_setTempLimit             , METH_VARARGS, "func setTempLimit"            },
  {"setBuzzers"               , (PyCFunction) Charger_setBuzzers               , METH_VARARGS, "func setBuzzers"              },
  {"startCharging"            , (PyCFunction) Charger_startCharging            , METH_VARARGS, "func startCharging"           },
  {"stopCharging"             , (PyCFunction) Charger_stopCharging             , METH_VARARGS, "func stopCharging"            },
  {NULL}
};

PyTypeObject ChargerType = {
    PyVarObject_HEAD_INIT(NULL, 0)
    .tp_name = "b6mini.Charger",
    .tp_basicsize = sizeof(ChargerObject),
    .tp_itemsize = 0,
    .tp_dealloc = (destructor) Charger_dealloc,
    .tp_str = (reprfunc) Charger_str,
    .tp_flags = Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE,
    .tp_doc = PyDoc_STR("Charger object"),
    .tp_methods = Charger_methods,
    .tp_members = Charger_members,
    .tp_init = (initproc) Charger_init,
    .tp_new = Charger_new,
};

void Charger_dealloc(ChargerObject* self) {
  delete self->charger;
  Py_TYPE(self)->tp_free((PyObject*) self);
}

PyObject* Charger_str(PyObject *self) {
  b6::Device* d = ((ChargerObject*) self)->charger;
  char str[255];
  sprintf(str, "b6mini.Charger {CoreType: %.8s, UpgradeType: %d, LanguageID: %d, CustomerID: %d, HWVersion: %lf, SWVersion: %lf, Encrypted: %s, CellCount: %d}",
  d->getCoreType().c_str(), d->getUpgradeType(), d->getLanguageID(), d->getCustomerID(), d->getHWVersion(), d->getSWVersion(), (d->isEncrypted() ? "True" : "False"), d->getCellCount());
  return PyUnicode_FromString(str);
}

PyObject* Charger_new(PyTypeObject* type, PyObject* args, PyObject* kwds) {
  ChargerObject* self;
  self = (ChargerObject*) type->tp_alloc(type, 0);
  if(self != NULL) {
    // Maybe don't actually need anything here? I don't know
    self->number = 0;
  }
  return (PyObject*) self;
}

int Charger_init(ChargerObject* self, PyObject* args, PyObject* kwds) {
  self->charger = new b6::Device();
  return 0;
}

PyObject* Charger_test(ChargerObject* self, PyObject *Py_UNUSED(ignored)) {
  printf("This is a test\n");
  return PyFloat_FromDouble(self->charger->getSWVersion());
}

PyObject* Charger_getSysInfo(ChargerObject* self, PyObject *Py_UNUSED(ignored)) {
  PyObject* rw = PyObject_CallObject((PyObject *) &SysInfoType, NULL);
  SysInfoObject* r = (SysInfoObject*) rw;
  if(r != NULL) {
    b6::SysInfo si = self->charger->getSysInfo();

    r->cycleTime = si.cycleTime;
    r->timeLimit = si.timeLimit;
    r->capLimit = si.capLimit;
    r->lowDCLimit = si.lowDCLimit;
    r->tempLimit = si.tempLimit;
    r->voltage = si.voltage;
    for(int i = 0; i < 8; i++) {
      PyList_SetItem((PyObject*) r->cells, i, PyLong_FromLong(si.cells[i]));
    }
    // self->cells[8];
    r->timeLimitOn = si.timeLimitOn;
    r->capLimitOn = si.capLimitOn;
    r->keyBuzzer = si.keyBuzzer;
    r->systemBuzzer = si.systemBuzzer;
  }

  return (PyObject*) r;
}

// state, tempExt, tempInt, capacity, time, voltage, current, impendance, cells[8]

PyObject* Charger_getChargeInfo(ChargerObject* self, PyObject *Py_UNUSED(ignored)) {
  PyObject* rw = PyObject_CallObject((PyObject *) &ChargeInfoType, NULL);
  ChargeInfoObject* r = (ChargeInfoObject*) rw;
  if(r != NULL) {
    b6::ChargeInfo ci = self->charger->getChargeInfo();

    r->state = ci.state;
    r->tempExt = ci.tempExt;
    r->tempInt = ci.tempInt;
    r->capacity = ci.capacity;
    r->time = ci.time;
    r->voltage = ci.voltage;
    r->impendance = ci.impendance;
    r->voltage = ci.voltage;

    for(int i = 0; i < 8; i++) {
      PyList_SetItem((PyObject*) r->cells, i, PyLong_FromLong(ci.cells[i]));
    }
  }
  return (PyObject*) r;
}

PyObject* Charger_getCoreType(ChargerObject* self, PyObject *Py_UNUSED(ignored)) {
  return PyUnicode_FromString(self->charger->getCoreType().c_str());
}

PyObject* Charger_getUpgradeType(ChargerObject* self, PyObject *Py_UNUSED(ignored)) {
  return PyLong_FromLong(self->charger->getUpgradeType());
}

PyObject* Charger_getLanguageID(ChargerObject* self, PyObject *Py_UNUSED(ignored)) {
  return PyLong_FromLong(self->charger->getLanguageID());
}

PyObject* Charger_getCustomerID(ChargerObject* self, PyObject *Py_UNUSED(ignored)) {
  return PyLong_FromLong(self->charger->getCustomerID());
}

PyObject* Charger_getHWVersion(ChargerObject* self, PyObject *Py_UNUSED(ignored)) {
  return PyFloat_FromDouble(self->charger->getHWVersion());
}

PyObject* Charger_getSWVersion(ChargerObject* self, PyObject *Py_UNUSED(ignored)) {
  return PyFloat_FromDouble(self->charger->getSWVersion());
}

PyObject* Charger_isEncrypted(ChargerObject* self, PyObject *Py_UNUSED(ignored)) {
  return PyBool_FromLong(self->charger->isEncrypted());
}

PyObject* Charger_getCellCount(ChargerObject* self, PyObject *Py_UNUSED(ignored)) {
  return PyLong_FromLong(self->charger->getCellCount());
}

PyObject* Charger_getDefaultChargeProfile(ChargerObject* self, PyObject* args) {
  // return PyLong_FromLong(self->charger->getCellCount());
  char *typestr;

  if (!PyArg_ParseTuple(args, "s", &typestr)) {
    return NULL;
  }

  // Prepare the string using fancy c string magic
  char* readhead = typestr;
  char* writehead = typestr;
  int i = 0;
  while(*readhead != '\0' && i < 4) {
    if(*readhead >= 'A' && *readhead <= 'Z') {
      *writehead++ = *readhead++; i++;// Valid character, copy exactly
    } else if(*readhead >= 'a' && *readhead <= 'z') {
      *writehead++ = *readhead++ + ('A' -'a'); i++;// Convert to uppercase
    } else {
      readhead++; // Invalid char, ignore it
    }
  }
  *writehead = '\0';

  uint8_t type = 255;
  // Figure out which mode this is
       if(!strcmp(typestr, "LIPO")) { type = 0x00; }
  else if(!strcmp(typestr, "LIIO")) { type = 0x01; }
  else if(!strcmp(typestr, "LIFE")) { type = 0x02; }
  else if(!strcmp(typestr, "LIHV")) { type = 0x03; }
  else if(!strcmp(typestr, "NIMH")) { type = 0x04; }
  else if(!strcmp(typestr, "NICD")) { type = 0x05; }
  else if(!strcmp(typestr, "NICA")) { type = 0x05; } // So you can also use NiCad
  else if(!strcmp(typestr, "PB"  )) { type = 0x06; }
  else if(!strcmp(typestr, "LEAD")) { type = 0x06; } // So you can also use Lead Acid
  else {
    printf("Invalid battery type");
    Py_RETURN_NONE;
  }

  PyObject* po = PyObject_CallObject((PyObject *) &ChargeProfileType, NULL);
  ChargeProfileObject* cpo = (ChargeProfileObject*) po;
  if(cpo != NULL) {
    b6::ChargeProfile cp = self->charger->getDefaultChargeProfile((b6::BATTERY_TYPE) type);

    cpo->batteryType          = (uint8_t) cp.batteryType;
    cpo->cellCount            = cp.cellCount;
    cpo->rPeakCount           = cp.rPeakCount;
    cpo->cycleType            = cp.cycleType;
    cpo->cycleCount           = cp.cycleCount;
    cpo->mode                 = (uint8_t) cp.mode.li;
    cpo->chargeCurrent        = cp.chargeCurrent;
    cpo->dischargeCurrent     = cp.dischargeCurrent;
    cpo->cellDischargeVoltage = cp.cellDischargeVoltage;
    cpo->endVoltage           = cp.endVoltage;
    cpo->trickleCurrent       = cp.trickleCurrent;
  }
  return (PyObject*) po;
}

PyObject* Charger_setCycleTime(ChargerObject* self, PyObject* args) {
  // return PyLong_FromLong(self->charger->getCellCount());
  int cycleTime;

  if (!PyArg_ParseTuple(args, "i", &cycleTime)) {
    return NULL;
  }

  bool result = self->charger->setCycleTime(cycleTime);
  return PyBool_FromLong(result);
}

PyObject* Charger_setTimeLimit(ChargerObject* self, PyObject* args) {
  // return PyLong_FromLong(self->charger->getCellCount());
  bool enabled;
  int limit;

  if (!PyArg_ParseTuple(args, "pi", &enabled, &limit)) {
    return NULL;
  }

  bool result = self->charger->setTimeLimit(enabled, limit);
  return PyBool_FromLong(result);
}

PyObject* Charger_setCapacityLimit(ChargerObject* self, PyObject* args) {
  // return PyLong_FromLong(self->charger->getCellCount());
  bool enabled;
  int limit;

  if (!PyArg_ParseTuple(args, "pi", &enabled, &limit)) {
    return NULL;
  }

  bool result = self->charger->setCapacityLimit(enabled, limit);
  return PyBool_FromLong(result);
}

PyObject* Charger_setTempLimit(ChargerObject* self, PyObject* args) {
  // return PyLong_FromLong(self->charger->getCellCount());
  int limit;

  if (!PyArg_ParseTuple(args, "i", &limit)) {
    return NULL;
  }

  bool result = self->charger->setTempLimit(limit);
  return PyBool_FromLong(result);
}

PyObject* Charger_setBuzzers(ChargerObject* self, PyObject* args) {
  // return PyLong_FromLong(self->charger->getCellCount());
  bool sys;
  bool key;

  if (!PyArg_ParseTuple(args, "pp", &sys, &key)) {
    return NULL;
  }

  bool result = self->charger->setBuzzers(sys, key);
  return PyBool_FromLong(result);
}

PyObject* Charger_stopCharging(ChargerObject* self, PyObject *Py_UNUSED(ignored)) {
  self->charger->stopCharging();
  Py_RETURN_NONE;
}

PyObject* Charger_startCharging(ChargerObject* self, PyObject* args) {
  // return PyLong_FromLong(self->charger->getCellCount());
  ChargeProfileObject* pcp;

  if (!PyArg_ParseTuple(args, "O!", &ChargeProfileType, &pcp)) {
    return NULL;
  }

  b6::ChargeProfile cp;

  cp.batteryType          = (b6::BATTERY_TYPE) pcp->batteryType;
  cp.cellCount            = pcp->cellCount;
  cp.rPeakCount           = pcp->rPeakCount;
  cp.cycleType            = pcp->cycleType;
  cp.cycleCount           = pcp->cycleCount;
  cp.mode.li              = (b6::CHARGING_MODE_LI) pcp->mode;
  cp.chargeCurrent        = pcp->chargeCurrent;
  cp.dischargeCurrent     = pcp->dischargeCurrent;
  cp.cellDischargeVoltage = pcp->cellDischargeVoltage;
  cp.endVoltage           = pcp->endVoltage;
  cp.trickleCurrent       = pcp->trickleCurrent;

  bool result = self->charger->startCharging(cp);
  return PyBool_FromLong(result);
}

// System Info Object
//
// ███████ ██    ██ ███████ ██ ███    ██ ███████  ██████
// ██       ██  ██  ██      ██ ████   ██ ██      ██    ██
// ███████   ████   ███████ ██ ██ ██  ██ █████   ██    ██
//      ██    ██         ██ ██ ██  ██ ██ ██      ██    ██
// ███████    ██    ███████ ██ ██   ████ ██       ██████

PyMemberDef SysInfo_members[] = {
  //  name         type         offset                                 flags     docstring
  {"cycleTime",    T_UINT,      offsetof(SysInfoObject, cycleTime),    READONLY, "cycleTime"   },
  {"timeLimit",    T_UINT,      offsetof(SysInfoObject, timeLimit),    READONLY, "timeLimit"   },
  {"capLimit",     T_UINT,      offsetof(SysInfoObject, capLimit),     READONLY, "capLimit"    },
  {"lowDCLimit",   T_UINT,      offsetof(SysInfoObject, lowDCLimit),   READONLY, "lowDCLimit"  },
  {"tempLimit",    T_UINT,      offsetof(SysInfoObject, tempLimit),    READONLY, "tempLimit"   },
  {"voltage",      T_UINT,      offsetof(SysInfoObject, voltage),      READONLY, "voltage"     },
  {"cells",        T_OBJECT_EX, offsetof(SysInfoObject, cells),        READONLY, "cells"       },
  {"timeLimitOn",  T_BOOL,      offsetof(SysInfoObject, timeLimitOn),  READONLY, "timeLimitOn" },
  {"capLimitOn",   T_BOOL,      offsetof(SysInfoObject, capLimitOn),   READONLY, "capLimitOn"  },
  {"keyBuzzer",    T_BOOL,      offsetof(SysInfoObject, keyBuzzer),    READONLY, "keyBuzzer"   },
  {"systemBuzzer", T_BOOL,      offsetof(SysInfoObject, systemBuzzer), READONLY, "systemBuzzer"},
  {NULL}
};

PyMethodDef SysInfo_methods[] = {
  // {"test"          , (PyCFunction) Charger_test          , METH_NOARGS, "Testit Now"   },
  {NULL, NULL, 0, NULL}
};

PyTypeObject SysInfoType = {
    PyVarObject_HEAD_INIT(NULL, 0)
    .tp_name = "b6mini.SysInfo",
    .tp_basicsize = sizeof(SysInfoObject),
    .tp_itemsize = 0,
    .tp_dealloc = (destructor) SysInfo_dealloc,
    .tp_str = (reprfunc) SysInfo_str,
    .tp_flags = Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE,
    .tp_doc = PyDoc_STR("System Info object"),
    .tp_methods = SysInfo_methods,
    .tp_members = SysInfo_members,
    .tp_init = (initproc) SysInfo_init,
    .tp_new = SysInfo_new,
};

void SysInfo_dealloc(SysInfoObject* self) {
  Py_DECREF(self->cells);
  Py_TYPE(self)->tp_free((PyObject*) self);
}

PyObject* SysInfo_str(PyObject *self) {
  char str[255];
  SysInfoObject* me = (SysInfoObject*) self;
  sprintf(str, "b6mini.SysInfo {cycleTime: %d, timeLimit: %d, capLimit: %d, lowDCLimit: %d, tempLimit: %d, voltage: %d, timeLimitOn: %s, capLimitOn: %s, keyBuzzer: %s, systemBuzzer: %s, cells: [",
  me->cycleTime, me->timeLimit, me->capLimit, me->lowDCLimit, me->tempLimit, me->voltage, BOOL(me->timeLimitOn), BOOL(me->capLimitOn), BOOL(me->keyBuzzer), BOOL(me->systemBuzzer));
  for(int i = 0; i < 8; i++) {
    char tmp[16];
    sprintf(tmp, "%s%ld", (i!=0) ? ", " : "", PyLong_AsLong(PyList_GetItem((PyObject*) me->cells, i)));
    strcat(str, (const char*) tmp);
  }
  strcat(str, "]}");
  return PyUnicode_FromString(str);
}

PyObject* SysInfo_new(PyTypeObject* type, PyObject* args, PyObject* kwds) {
  SysInfoObject* self;
  self = (SysInfoObject*) type->tp_alloc(type, 0);
  if(self != NULL) {
    // Init everything to 0s?
    self->cycleTime = 0;
    self->timeLimit = 0;
    self->capLimit = 0;
    self->lowDCLimit = 0;
    self->tempLimit = 0;
    self->voltage = 0;

    self->cells = (PyListObject*) PyList_New(8);
    Py_INCREF(self->cells);
    if(self->cells != NULL) {
      for(int i = 0; i < 8; i++) {
        PyList_SetItem((PyObject*) self->cells, i, PyLong_FromLong(0));
      }
    }

    self->timeLimitOn = false;
    self->capLimitOn = false;
    self->keyBuzzer = false;
    self->systemBuzzer = false;
  }

  return (PyObject*) self;
}

int SysInfo_init(SysInfoObject* self, PyObject* args, PyObject* kwds) {

  return 0;
}

// Charge Info Object
//
//  ██████ ██   ██  █████  ██████   ██████  ███████ ██ ███    ██ ███████  ██████
// ██      ██   ██ ██   ██ ██   ██ ██       ██      ██ ████   ██ ██      ██    ██
// ██      ███████ ███████ ██████  ██   ███ █████   ██ ██ ██  ██ █████   ██    ██
// ██      ██   ██ ██   ██ ██   ██ ██    ██ ██      ██ ██  ██ ██ ██      ██    ██
//  ██████ ██   ██ ██   ██ ██   ██  ██████  ███████ ██ ██   ████ ██       ██████
PyMemberDef ChargeInfo_members[] = {
//  name         type         offset                                  flags     docstring
  {"state",      T_UINT,      offsetof(ChargeInfoObject, state),      READONLY, "state"     },
  {"tempExt",    T_UINT,      offsetof(ChargeInfoObject, tempExt),    READONLY, "tempExt"   },
  {"tempInt",    T_UINT,      offsetof(ChargeInfoObject, tempInt),    READONLY, "tempInt"   },
  {"capacity",   T_UINT,      offsetof(ChargeInfoObject, capacity),   READONLY, "capacity"  },
  {"time",       T_UINT,      offsetof(ChargeInfoObject, time),       READONLY, "time"      },
  {"voltage",    T_UINT,      offsetof(ChargeInfoObject, voltage),    READONLY, "voltage"   },
  {"current",    T_UINT,      offsetof(ChargeInfoObject, current),    READONLY, "current"   },
  {"impendance", T_UINT,      offsetof(ChargeInfoObject, impendance), READONLY, "impendance"},
  {"cells",      T_OBJECT_EX, offsetof(ChargeInfoObject, cells),      READONLY, "cells"     },
  {NULL}
};

PyMethodDef ChargeInfo_methods[] = {
  // {"test"          , (PyCFunction) Charger_test          , METH_NOARGS, "Testit Now"   },
  {NULL, NULL, 0, NULL}
};

PyTypeObject ChargeInfoType = {
    PyVarObject_HEAD_INIT(NULL, 0)
    .tp_name = "b6mini.ChargeInfo",
    .tp_basicsize = sizeof(ChargeInfoObject),
    .tp_itemsize = 0,
    .tp_dealloc = (destructor) ChargeInfo_dealloc,
    .tp_str = (reprfunc) ChargeInfo_str,
    .tp_flags = Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE,
    .tp_doc = PyDoc_STR("Charger Info object"),
    .tp_methods = ChargeInfo_methods,
    .tp_members = ChargeInfo_members,
    .tp_init = (initproc) ChargeInfo_init,
    .tp_new = ChargeInfo_new,
};

void ChargeInfo_dealloc(ChargeInfoObject* self) {
  Py_DECREF(self->cells);
  Py_TYPE(self)->tp_free((PyObject*) self);
}

PyObject* ChargeInfo_str(PyObject *self) {
  char str[255];
  ChargeInfoObject* me = (ChargeInfoObject*) self;
  sprintf(str, "b6mini.ChargeInfo {state: %d, tempExt: %d, tempInt: %d, capacity: %d, voltage: %d, current: %d, impendance: %d, cells: [",
  me->state, me->tempExt, me->tempInt, me->capacity, me->voltage, me->current, me->impendance);
  for(int i = 0; i < 8; i++) {
    char tmp[16];
    sprintf(tmp, "%s%ld", (i!=0) ? ", " : "", PyLong_AsLong(PyList_GetItem((PyObject*) me->cells, i)));
    strcat(str, (const char*) tmp);
  }
  strcat(str, "]}");
  return PyUnicode_FromString(str);
}

PyObject* ChargeInfo_new(PyTypeObject* type, PyObject* args, PyObject* kwds) {
  ChargeInfoObject* self;
  self = (ChargeInfoObject*) type->tp_alloc(type, 0);
  if(self != NULL) {
    // Init everythin to 0s?
    self->state = 0;
    self->tempExt = 0;
    self->tempInt = 0;
    self->capacity = 0;
    self->time = 0;
    self->voltage = 0;
    self->impendance = 0;
    self->voltage = 0;

    self->cells = (PyListObject*) PyList_New(8);
    Py_INCREF(self->cells);
    if(self->cells != NULL) {
      for(int i = 0; i < 8; i++) {
        PyList_SetItem((PyObject*) self->cells, i, PyLong_FromLong(0));
      }
    }
  }
  return (PyObject*) self;
}

int ChargeInfo_init(ChargeInfoObject* self, PyObject* args, PyObject* kwds) {

  return 0;
}

//  ██████ ██   ██  █████  ██████   ██████  ███████ ██████  ██████   ██████  ███████ ██ ██      ███████
// ██      ██   ██ ██   ██ ██   ██ ██       ██      ██   ██ ██   ██ ██    ██ ██      ██ ██      ██
// ██      ███████ ███████ ██████  ██   ███ █████   ██████  ██████  ██    ██ █████   ██ ██      █████
// ██      ██   ██ ██   ██ ██   ██ ██    ██ ██      ██      ██   ██ ██    ██ ██      ██ ██      ██
//  ██████ ██   ██ ██   ██ ██   ██  ██████  ███████ ██      ██   ██  ██████  ██      ██ ███████ ███████

PyMemberDef ChargeProfile_members[] = {
//  name                   type      offset                                         flags  docstring
  {"batteryType",          T_UBYTE,  offsetof(ChargeProfileObject, batteryType),          0, "batteryType"         },
  {"cellCount",            T_UBYTE,  offsetof(ChargeProfileObject, cellCount),            0, "cellCount"           },
  {"rPeakCount",           T_UBYTE,  offsetof(ChargeProfileObject, rPeakCount),           0, "rPeakCount"          },
  {"cycleType",            T_UBYTE,  offsetof(ChargeProfileObject, cycleType),            0, "cycleType"           },
  {"cycleCount",           T_UBYTE,  offsetof(ChargeProfileObject, cycleCount),           0, "cycleCount"          },
  {"mode",                 T_UBYTE,  offsetof(ChargeProfileObject, mode),                 0, "mode"                },
  {"chargeCurrent",        T_USHORT, offsetof(ChargeProfileObject, chargeCurrent),        0, "chargeCurrent"       },
  {"dischargeCurrent",     T_USHORT, offsetof(ChargeProfileObject, dischargeCurrent),     0, "dischargeCurrent"    },
  {"cellDischargeVoltage", T_USHORT, offsetof(ChargeProfileObject, cellDischargeVoltage), 0, "cellDischargeVoltage"},
  {"endVoltage",           T_USHORT, offsetof(ChargeProfileObject, endVoltage),           0, "endVoltage"          },
  {"trickleCurrent",       T_USHORT, offsetof(ChargeProfileObject, trickleCurrent),       0, "trickleCurrent"      },
  {NULL}
};

PyMethodDef ChargeProfile_methods[] = {
  {"getTypeString"          , (PyCFunction) ChargeProfile_getTypeString          , METH_NOARGS, "getTypeString"   },
  {NULL, NULL, 0, NULL}
};

PyTypeObject ChargeProfileType = {
    PyVarObject_HEAD_INIT(NULL, 0)
    .tp_name = "b6mini.ChargeProfile",
    .tp_basicsize = sizeof(ChargeProfileObject),
    .tp_itemsize = 0,
    .tp_dealloc = (destructor) ChargeProfile_dealloc,
    .tp_str = (reprfunc) ChargeProfile_str,
    .tp_flags = Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE,
    .tp_doc = PyDoc_STR("Charger Profile object"),
    .tp_methods = ChargeProfile_methods,
    .tp_members = ChargeProfile_members,
    .tp_init = (initproc) ChargeProfile_init,
    .tp_new = ChargeProfile_new,
};

void ChargeProfile_dealloc(ChargeProfileObject* self) {
  // Py_DECREF(self->cells);
  Py_TYPE(self)->tp_free((PyObject*) self);
}

PyObject* ChargeProfile_str(PyObject *self) {
  char str[255];
  ChargeProfileObject* me = (ChargeProfileObject*) self;
  sprintf(str, "b6mini.ChargeInfo {batteryType: %d, cellCount: %d, rPeakCount: %d, cycleType: %d, cycleCount: %d, mode: %d, chargeCurrent: %d, dischargeCurrent: %d, cellDischargeVoltage: %d, endVoltage: %d, trickleCurrent: %d }",
  me->batteryType, me->cellCount, me->rPeakCount, me->cycleType, me->cycleCount, me->mode, me->chargeCurrent, me->dischargeCurrent, me->cellDischargeVoltage, me->endVoltage, me->trickleCurrent);

  return PyUnicode_FromString(str);
}

PyObject* ChargeProfile_new(PyTypeObject* type, PyObject* args, PyObject* kwds) {
  ChargeProfileObject* self;
  self = (ChargeProfileObject*) type->tp_alloc(type, 0);
  if(self != NULL) {
    // uint8_t batteryType, cellCount, rPeakCount, cycleType, cycleCount, mode;
    // uint16_t chargeCurrent, dischargeCurrent, cellDischargeVoltage, endVoltage, trickleCurrent;
    self->batteryType          = 0;
    self->cellCount            = 0;
    self->rPeakCount           = 0;
    self->cycleType            = 0;
    self->cycleCount           = 0;
    self->mode                 = 0;
    self->chargeCurrent        = 0;
    self->dischargeCurrent     = 0;
    self->cellDischargeVoltage = 0;
    self->endVoltage           = 0;
    self->trickleCurrent       = 0;
  }
  return (PyObject*) self;
}

int ChargeProfile_init(ChargeProfileObject* self, PyObject* args, PyObject* kwds) {
  return 0;
}

PyObject* ChargeProfile_getTypeString(ChargeProfileObject* self, PyObject *Py_UNUSED(ignored)) {
  std::string ts = "";
  switch(self->batteryType) {
    case 0x00: { //LiPo
      ts = "Lithium Polymer";
    } break;
    case 0x01: { //LiIo
      ts = "Lithium Ion";
    } break;
    case 0x02: { //LiFe
      ts = "Lithium Iron Phosphate";
    } break;
    case 0x03: { //LiHV
      ts = "Lithium Polymer High Voltage";
    } break;
    case 0x04: { //NiMh
      ts = "Nickel-metal Hydride";
    } break;
    case 0x05: { //NiCd
      ts = "Nickel-Cadnium";
    } break;
    case 0x06: { //PB
      ts = "Lead Acid";
    } break;
    default: {
      ts = "Unknown";
    } break;
  }
  return PyUnicode_FromString(ts.c_str());
}
