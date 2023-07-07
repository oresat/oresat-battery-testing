# oresat-battery-testing

Battery testing software and circuitry for testing cells and batteries to fly on the ISS

V1.0 of the PCB layout:
![The PCB layout V1.0](https://github.com/oresat/oresat-battery-testing/raw/master/pcd-layout.png)

## Software

### Setup

- Install dependencies: `$ sudo apt install libusb-1.0-0-dev pkg-config python3-dev`
- Initialize libb6 submodule: `$ git submodule update --init`
- Build Python extension for libb6: `$ make -C libraries`

### Udev Setup
Copy the .rules file (from the Documentation folder) into the folder on your computer which contains rules files for udev.

For me it is: Computer/etc/udev/rules.d

This will allow you to run test.py without requiring sudo.

### Run

"python test.py"
