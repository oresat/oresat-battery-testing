LIBB6_SRC = .

INC_DIRS = \
	-I$(LIBB6_SRC)

LIBB6_SOURCES = \
	$(LIBB6_SRC)/Device.cc \
	$(LIBB6_SRC)/Packet.cc \
	$(LIBB6_SRC)/new_main.cc

CFLAGS = -std=c++11 $(INC_DIRS) $(shell pkg-config --cflags --libs libusb-1.0) 
LDFLAGS = -lusb-1.0 #$(shell python3-config --ldflags)

OBJS = $(LIBB6_SOURCES:%.cc=%.o)

.PHONY: all clean

%.o: %.cc
	$(CXX) -c $< -o $@ $(CFLAGS)

all: $(OBJS)
	$(CXX) -o $@ $^ $(LDFLAGS)

clean:
	rm -rf a.out
	
