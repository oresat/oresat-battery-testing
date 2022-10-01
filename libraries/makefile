# Clone https://github.com/maciek134/libb6 to the same directory as oresat-battery-testing
# Also sudo apt install libusb-dev
# This builds on Python 3.8
# If you still have missing stuff, you can try messing with the stuff below, good luck!

# Directories where some things live
LIBUSB_INC = /usr/include/libusb-1.0
PYTHON_INC = /usr/include/python3.8
LIBB6_INC = ../../ # Don't include the actual libb6 folder here, it breaks the library if you do. It will be automatically added and included later

ODIR=obj
CC=g++

LIBB6_DIR = $(LIBB6_INC)/libb6
LIBB6_ITEMS = Device Packet
LIBB6_HITEMS = $(LIBB6_ITEMS) Enum Error

CFLAGS = -I$(LIBB6_DIR) -I$(LIBUSB_INC) -I$(PYTHON_INC) -I$(LIBB6_INC) -std=c++11 -lusb-1.0 -Wall

LIBB6_FILES = $(patsubst %,$(LIBB6_DIR)/%,$(LIBB6_ITEMS))
LIBB6_HFILES = $(patsubst %,$(LIBB6_DIR)/%,$(LIBB6_HITEMS))
LIBB6_OBJS = $(patsubst %,$(ODIR)/%.o,$(LIBB6_FILES))
LIBB6_SOURCES = $(patsubst %,%.cc,$(LIBB6_FILES))
LIBB6_HEADERS = $(patsubst %,%.hh,$(LIBB6_FILES))

$(ODIR)/$(LIBB6_DIR)/%.o : $(LIBB6_DIR)/%.cc $(LIBB6_HEADERS)
	@mkdir -p $(@D)
	$(CC) -fPIC -c -o $@ $< $(CFLAGS)

$(ODIR)/%.o: %.cpp # Charger.h
	@mkdir -p $(@D)
	$(CC) -fPIC -c -o $@ $< $(CFLAGS)

b6mini.so: b6mini.cpp $(ODIR)/*.o $(LIBB6_OBJS)
	$(CC) -fPIC -shared -o $@ $^ $(CFLAGS)

.PHONY: clean

clean:
	rm -f obj -r
