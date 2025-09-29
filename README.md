# oresat-battery-testing

Battery testing software and circuitry for testing cells and batteries to fly on the ISS

General Project Documentation aimed at newcomers:
https://docs.google.com/document/d/1XBeL89PfLqN40TnOpgzCtq_2dRlRgkeDnu8u4CYXgOA/edit

V1.0 of the PCB layout:
![The PCB layout V1.0](https://github.com/oresat/oresat-battery-testing/raw/master/pcd-layout.png)

### Software
### Setup
- Clone oresat-battery-testing.
- Install dependencies: `$ sudo apt install libusb-1.0-0-dev pkg-config python3-dev`
- Install pyusb: "pip install pyusb" or if that doesn't work, use "pip install pyusb --break-system-packages"
- Build Python extension for libb6: `$ make -C libraries`

### More Dependencies
To get u6 to work (import u6) you must install the labjack-ljm python library which is different from the labjack-ljm package

sudo pip install labjack-ljm --break-system-packages 
The above line installed labjack-ljm

You need to install Exodriver in order for u6 to work

git clone https://github.com/labjack/exodriver.git
cd exodriver
sudo ./install.sh

You will also need LabJackPython:
sudo pip install LabJackPython --break-system-packages

### Udev Setup
Copy the .rules files (from the Battery Tester folder) into the folder on your computer which contains rules files for udev.

For example on an Ubuntu system: /etc/udev/rules.d

This will allow you to run [filename].py without requiring sudo.

Note that you will have to find the correct devpaths again if you use your own device, then modify 99-b6mini.rules accordingly.

Choose a USB port on your computer to plug the battery board into and do not change it.

### Run
cd battery_tester
python battery_test_jig.py
or better yet: python testing_bay.py

If you get an import error about libb6:
...run the Makefile in battery_tester/libb6 to make an object file.

### Battery Cells
In each bank are four battery slots. The battery slot on each bank that is closest to the LabJack is slot D, then up from there is C, B, and A. Each battery slot corresponds to the charger of the same designation. If Battery A (on whichever battery bank currently selected) is not charging, something may be wrong with Charger A, for instance.
