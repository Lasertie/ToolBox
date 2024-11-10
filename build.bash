#!/usr/bin/bash

cd ..
sudo dpkg-deb --build ToolBox/
sudo dpkg -i ToolBox*.deb