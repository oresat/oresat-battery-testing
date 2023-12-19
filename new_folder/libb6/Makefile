
PYLIB_SRC = .
LIBB6_SRC = .

LINK_TARGET = libb6.so

INC_DIRS = \
	-I$(PYLIB_SRC) \
	-I$(LIBB6_SRC)

BUILD_DIR = build

PYLIB_SOURCES = \
	$(PYLIB_SRC)/binding.cpp

LIBB6_SOURCES = \
	$(LIBB6_SRC)/Device.cc \
	$(LIBB6_SRC)/Packet.cc

CFLAGS = -std=c++11 -fPIC $(INC_DIRS) $(shell pkg-config --cflags --libs libusb-1.0) $(shell python3 -m pybind11 --includes)
LDFLAGS = -lusb-1.0 #$(shell python3-config --ldflags)

OBJS = $(PYLIB_SOURCES:%.cpp=$(BUILD_DIR)/%.o) $(LIBB6_SOURCES:%.cc=$(BUILD_DIR)/%.o)

.PHONY: all clean

$(BUILD_DIR)/%.o: %.cc
	$(CXX) -c $< -o $@ $(CFLAGS)

$(BUILD_DIR)/%.o: %.cpp
	@mkdir -p $(BUILD_DIR)/$(LIBB6_SRC)
	$(CXX) -c $< -o $@ $(CFLAGS)

$(LINK_TARGET): $(OBJS)
	@mkdir -p $(BUILD_DIR)
	$(CXX) -shared -o $@ $^ $(LDFLAGS)

all: $(LINK_TARGET)

clean:
	rm -rf $(BUILD_DIR) $(LINK_TARGET)
