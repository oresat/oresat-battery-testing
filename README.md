# oresat-battery-testing

Battery testing software and circuitry for testing cells and batteries to fly on the ISS

V1.0 of the PCB layout:
![The PCB layout V1.0](https://github.com/oresat/oresat-battery-testing/raw/master/pcd-layout.png)

### Software

### Setup
- Clone oresat-battery-testing.
- Install dependencies: `$ sudo apt install libusb-1.0-0-dev pkg-config python3-dev`
- Build Python extension for libb6: `$ make -C libraries`

### Udev Setup
Copy the .rules files (from the Battery Tester folder) into the folder on your computer which contains rules files for udev.

For example on an Ubuntu system: /etc/udev/rules.d

This will allow you to run [filename].py without requiring sudo.

Note that you will have to find the correct devpaths again if you use your own device, then modify 99-b6mini.rules accordingly.

Choose a USB port on your computer to plug the battery board into and do not change it.

### Run
cd main
python battery_test_jig

If you get an import error about libb6:
...run the Makefile in main/libb6 to make an object file.
