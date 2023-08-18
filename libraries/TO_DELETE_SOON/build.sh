echo "Building ..."
# g++ -Wall -shared -lusb-1.0 -I"./libb6/"-o b6mini.so -fPIC b6mini.cpp
make
if [ $? -eq 0 ]; then
   echo "Running Python ..."
   echo "--------------------------------"
   python test.py
else
   echo -e "\033[0;31mBuild failed, aborting.\033[0m"
fi
