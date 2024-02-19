#!/bin/bash

# Update package lists
sudo apt update

# Get a list of installed packages and remove them one by one
for package in $(dpkg --get-selections | grep -v deinstall | cut -f1); do
    sudo apt-get remove --purge -y $package
done

# Clean up any residual configuration files
sudo apt-get autoremove -y
