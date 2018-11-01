# sump-thing

## Components

* NodeMCU (ESP8266): http://a.co/d/fYVz4CV
* BME280, temperature sensor: http://a.co/d/dGsapW6
* SSD1306, 0.96" i2C OLED: http://a.co/d/9HEjrm8
* Light sensitive resitor: http://a.co/d/9iC4TZW 


## Installing micropython on NodeMCU

1. Downlaod the firmware
```
wget http://micropython.org/resources/firmware/esp8266-20180511-v1.9.4.bin
```

2. Wipe the ESP8266
```
esptool.py --port /dev/ttyUSB0 erase_flash
```

3. Install mircopython
```
esptool.py --port /dev/ttyUSB0 --baud 460800 write_flash --flash_size=detect 0 esp8266-20180511-v1.9.4.bin
```

4. Install python tools.
```
pipenv install
```


## Installing scripts

I use `ampy` to *upload* the scripts to the ESP8266 which is all in the
`upload.sh` script.

## Testing

```
pipenv run mpfshell -o ttyUSB0
mpfs [/]> repl
```
