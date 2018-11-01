#!/usr/bin/env bash

pipenv run ampy --port /dev/ttyUSB0 put main.py
pipenv run ampy --port /dev/ttyUSB0 put config.json
pipenv run ampy --port /dev/ttyUSB0 put bme280.py
pipenv run ampy --port /dev/ttyUSB0 put ultrasonic.py
