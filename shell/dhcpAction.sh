#! /bin/bash 

var="$2" 

cd /home/pi/Dev
sudo python dashControl.py $var
cd