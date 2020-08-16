#!/bin/bash

rm /home/pi/watering/nohup.out
FLASK_APP=watering.py nohup flask run -h 0.0.0.0 &
