#!/usr/bin/sh

# Update system
sudo apt-get -y update
sudo apt-get -y upgrade
sudo apt-get install -y csh mpich gfortran gcc m4 make zlib1g-dev git

# Install libraries, WRF, and WPS with Python
python3 script/install_libraries.py
python3 script/install_WRF.py
python3 script/install_WPS.py