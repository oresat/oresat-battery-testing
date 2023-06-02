#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include <structmember.h>
#include <iostream>
#include "libb6/Device.hh"
#include "libb6/Packet.hh"
#include "libb6/Enum.hh"
#include "Charger.h"

static PyMethodDef b6miniMethods[] = {
    // {"print",  b6mini_print, METH_VARARGS,
    //   "Prints stuff."},
    {NULL, NULL, 0, NULL}        /* Sentinel */
};

static struct PyModuleDef b6minimodule = {
    PyModuleDef_HEAD_INIT,
    "b6mini",   /* name of module */
    NULL, /* module documentation, may be NULL */
    -1,       /* size of per-interpreter state of the module,
                 or -1 if the module keeps state in global variables. */
    b6miniMethods
};

PyMODINIT_FUNC PyInit_b6mini(void) {
    // return PyModule_Create(&b6minimodule);
    PyObject *m;
    if (PyType_Ready(&ChargerType) < 0)
        return NULL;
    if (PyType_Ready(&SysInfoType) < 0)
        return NULL;
    if (PyType_Ready(&ChargeInfoType) < 0)
        return NULL;
    if (PyType_Ready(&ChargeProfileType) < 0)
        return NULL;
    // Duplicate above

    m = PyModule_Create(&b6minimodule);
    if (m == NULL)
        return NULL;

    Py_INCREF(&ChargerType);
    if (PyModule_AddObject(m, "Charger", (PyObject *) &ChargerType) < 0) {
        Py_DECREF(&ChargerType);
        Py_DECREF(m);
        return NULL;
    }
    Py_INCREF(&SysInfoType);
    if (PyModule_AddObject(m, "SysInfo", (PyObject *) &SysInfoType) < 0) {
        Py_DECREF(&SysInfoType);
        Py_DECREF(m);
        return NULL;
    }
    Py_INCREF(&ChargeInfoType);
    if (PyModule_AddObject(m, "ChargeInfo", (PyObject *) &ChargeInfoType) < 0) {
        Py_DECREF(&ChargeInfoType);
        Py_DECREF(m);
        return NULL;
    }
    Py_INCREF(&ChargeProfileType);
    if (PyModule_AddObject(m, "ChargeProfile", (PyObject *) &ChargeInfoType) < 0) {
        Py_DECREF(&ChargeProfileType);
        Py_DECREF(m);
        return NULL;
    }
    // Duplucate Above

    return m;
}

int main(int argc, char *argv[]) {

    wchar_t *program = Py_DecodeLocale(argv[0], NULL);
    if (program == NULL) {
        fprintf(stderr, "Fatal error: cannot decode argv[0]\n");
        exit(1);
    }

    /* Add a built-in module, before Py_Initialize */
    if (PyImport_AppendInittab("b6mini", PyInit_b6mini) == -1) {
        fprintf(stderr, "Error: could not extend in-built modules table\n");
        exit(1);
    }

    /* Pass argv[0] to the Python interpreter */
    Py_SetProgramName(program);

    /* Initialize the Python interpreter.  Required.
       If this step fails, it will be a fatal error. */
    Py_Initialize();

    /* Optionally import the module; alternatively,
       import can be deferred until the embedded script
       imports it. */
    PyObject *pmodule = PyImport_ImportModule("b6mini");
    if (!pmodule) {
        PyErr_Print();
        fprintf(stderr, "Error: could not import module 'b6mini'\n");
    }

    PyMem_RawFree(program);
    return 0;
}
