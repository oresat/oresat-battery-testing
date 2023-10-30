LIBB6_SRC = libb6

LINK_TARGET = b6

INC_DIRS = \
	-I$(LIBB6_SRC)

BUILD_DIR = build

LIBB6_SOURCES = \
	$(LIBB6_SRC)/Device.cc \
	$(LIBB6_SRC)/Packet.cc \
	main.cc

CFLAGS = -std=c++11 -fPIC $(INC_DIRS) $(shell pkg-config --cflags --libs libusb-1.0) 
CFLAGS += -g

OBJS = $(LIBB6_SOURCES:%.cc=$(BUILD_DIR)/%.o)

LDFLAGS = -lusb-1.0 

.PHONY: all clean

$(BUILD_DIR)/%.o: %.cc
	@mkdir -p $(BUILD_DIR)/$(LIBB6_SRC)
	$(CXX) -c $< -o $@ $(CFLAGS)

$(LINK_TARGET): $(OBJS)
	@mkdir -p $(BUILD_DIR)
	$(CXX) -o $@ $^ $(LDFLAGS)

all: $(LINK_TARGET)

clean:
	rm -rf $(BUILD_DIR) $(LINK_TARGET)
