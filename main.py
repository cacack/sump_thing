from bme280 import BME280
import machine
import network
from ssd1306 import SSD1306_I2C
import sys
import ubinascii
import uhashlib
import ujson
from umqtt.robust import MQTTClient
from ultrasonic import Ultrasonic
import utime

sha1_hash = uhashlib.sha1(machine.unique_id())
client_id = "esp8266_{:s}".format(ubinascii.hexlify(sha1_hash.digest())[:7])

try:
    CONFIG = ujson.loads(open('config.json', 'r').read())
except FileNotFoundError:
    print('ERROR: Unable to read config file. Exiting.')
    sys.exit(1)

station = network.WLAN(network.STA_IF)
access_point = network.WLAN(network.AP_IF)
i2c = machine.I2C(sda = machine.Pin(4), scl = machine.Pin(5))
display = SSD1306_I2C(128, 64, i2c)
bme = BME280(i2c=i2c,address=0x76)
ldr = machine.ADC(0)
ultrasonic = Ultrasonic(machine.Pin(12, machine.Pin.IN))
led = machine.Pin(2, machine.Pin.OUT)
led.value(1)  # Turn off LED

mqtt = MQTTClient(client_id, CONFIG['broker'])
thing_id = ''
if CONFIG['room']:
    thing_id = CONFIG['room']
else:
    thing_id = client_id

t_pub_temperature = "{}/{}/{}".format(CONFIG['base'],thing_id,'temperature')
t_pub_humidity = "{}/{}/{}".format(CONFIG['base'],thing_id,'humidity')
t_pub_pressure = "{}/{}/{}".format(CONFIG['base'],thing_id,'pressure')
t_pub_brightness = "{}/{}/{}".format(CONFIG['base'],thing_id,'brightness')
t_pub_waterlevel = "{}/{}/{}".format(CONFIG['base'],thing_id,'waterlevel')

def wifi_connect():
    if not station.isconnected():
        print('Connecting to network {:s} '.format(CONFIG['ssid']),end='')
        station.active(True)
        station.connect(CONFIG['ssid'], CONFIG['password'])
        while not station.isconnected():
            print('.',end='')
            utime.sleep_ms(500)
        print()
        print('Connection successful.')
        access_point.active(False)  ## Turn off access point

    print('Network config: {:s}'.format(repr(station.ifconfig())))


def publish_sensors():
    year,month,mday,hour,minute,second,weekday,yearday = utime.localtime()
    time = '{}{}{}{}{}{}'.format(year,month,mday,hour,minute,second)
    temperature_c,pressure,humidity = bme.values
    temperature_f = temperature_c * 9/5 + 32
    brightness = ldr.read()
    water_distance = ultrasonic.distance_in

    led.value(0)
    display.fill(0)
    display.text('Temp: {0:.1f} F'.format(temperature_f),2,2,1)
    display.text('Pa: {0:.1f} hPa'.format(pressure),2,14,1)
    display.text('Hum: {0:.1f} %'.format(humidity),2,26,1)
    display.text('Light: {:d} lux'.format(brightness),2,38,1)
    #display.text('Dist: {0:.1f} in'.format(water_distance),2,50,1)
    display.show()
    print('{:s} - {:.1f} F  {:.1f} hPa  {:.1f} % {:d} lux {} in'.format(time,temperature_f,pressure,humidity,brightness,water_distance))
    mqtt.publish(
        t_pub_temperature,
        bytes(str(temperature_f), 'utf-8')
    )
    mqtt.publish(
        t_pub_humidity,
        bytes(str(humidity), 'utf-8')
    )
    mqtt.publish(
        t_pub_pressure,
        bytes(str(pressure), 'utf-8')
    )
    mqtt.publish(
        t_pub_brightness,
        bytes(str(brightness), 'utf-8')
    )
    led.value(1)


def poweroff_display():
    display.poweroff


def flip_display():
    display.invert(1)


def main():
    if station.isconnected():
        print('Already connected to wifi.')
    else:
        wifi_connect()

    if not mqtt.connect():
        print("{:s} connected to MQTT broker: {:s}".format(client_id,CONFIG['broker']))

    tasks = [
        [10.0, publish_sensors],
        [31.0, poweroff_display],
    ]
    last_run = {}
    count = 0
    while True:
        try:
            for delay, task in tasks:
                if task not in last_run  or last_run[task] < utime.time() - delay:
                    task()
                    last_run[task] = utime.time()
            utime.sleep_ms(2000)

        except KeyboardInterrupt as err:
            print(err)
            utime.sleep(2)
            print('Exiting...')
            display.fill(0)
            display.text('Exiting...',2,2,1)
            display.show()
            utime.sleep(1)
            display.fill(0)
            display.show()
            sys.exit(0)

        except Exception as err:
            #if station.isconnected():
            #    wifi_connect()
            print('Uncaught exception!!')
            sys.print_exception(err)
            sys.exit(255)


if __name__ == '__main__':
    main()
