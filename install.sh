#!/bin/bash
cd "$(dirname "$0")"

# Install python3 and g++
sudo apt-get install python3
sudo apt-get install g++

# Install pip3
sudo apt-get install python3-pip

# Install termcolor
pip3 install termcolor

# Create symlink for src/main.py
sudo chmod +x $PWD/src/main.py
sudo ln -s $PWD/src/main.py /usr/local/bin/pystache

# Echo success message
echo ""
echo "Successfully installed pystache!"
echo "To run pystache, type 'pystache <filename>' in the terminal."