ODIR=obj
CC=g++



LIBB6_DIR = libb6
LIBB6_ITEMS = Device Packet
LIBB6_HITEMS = $(LIBB6_ITEMS) Enum Error

CFLAGS=-I$(LIBB6_DIR) -std=c++11 -lusb-1.0 -Wall

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
