# Clone https://github.com/maciek134/libb6 to the same directory as oresat-battery-testing
# Also sudo apt install libusb-dev pkg-config
# If you still have missing stuff, you can try messing with the stuff below, good luck!

PYLIB_SRC = .
LIBB6_SRC = libb6

LINK_TARGET = b6mini.so

INC_DIRS = \
					 -I$(PYLIB_SRC) \
					 -I$(LIBB6_SRC)

PYLIB_SOURCES = \
					$(PYLIB_SRC)/b6mini.cpp \
					$(PYLIB_SRC)/Charger.cpp

LIBB6_SOURCES = \
					$(LIBB6_SRC)/Device.cc \
					$(LIBB6_SRC)/Packet.cc

CFLAGS = -std=c++11 -fPIC $(INC_DIRS) $(shell pkg-config --cflags --libs libusb-1.0) $(shell python-config --cflags)
LDFLAGS = -lusb-1.0 $(shell python-config --ldflags)

OBJS = $(PYLIB_SOURCES:%.cpp=%.o) $(LIBB6_SOURCES:%.cc=%.o)

.PHONY: all clean

%.o: %.cc
					$(CXX) -c $< -o $@ $(CFLAGS)

%.o: %.cpp
					$(CXX) -c $< -o $@ $(CFLAGS)

$(LINK_TARGET): $(OBJS)
					$(CXX) -shared -o $@ $^ $(LDFLAGS)

all: $(LINK_TARGET)

clean:
					rm -rf $(OBJS) b6mini.so
