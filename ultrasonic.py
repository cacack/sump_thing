"""
Micropython module for RadioShack 2760342 ultrasonic ranging module.
Based on RadioShack's Arduino code:
https://github.com/RadioShackCorp/2760342-Range-Sensor/blob/master/UltrasonicRangeSensor.ino
"""
from machine import Pin, time_pulse_us
from time import sleep_us


class Ultrasonic:
    """RS 2760342 ultrasonic ranging module class."""

    def __init__(self, sig_Pin):
       """Initialize with signal pin."""
       self._sig = sig_Pin
       self._sound_speed = 340  # m/s

    def _pulse(self):
        """Trigger ultrasonic pulse."""
        self._sig.init(Pin.OUT)
        self._sig.low()
        sleep_us(2)
        self._sig.high()
        sleep_us(5)
        self._sig.low()
        self._sig.init(Pin.IN)

    def _duration(self):
        """Measure pulse length."""
        self._pulse()
        pulse_width_s = time_pulse_us(self._sig, Pin.high)
        return float(pulse_width)

    def distance_cm(self):
        """Measure pulse length and return calculated distance in centimeters."""
        pulse_width = self._duration()
        dist_cm = (pulse_width / 29 / 2)
        return float(dist_cm)

    def distance_in(self):
        """Measure pulse length and return calculated distance in inches."""
        pulse_width = self._duration()
        dist_in = (pulse_width / 74 / 2)
        return float(dist_in)

    def calibration(self, known_dist_m):
        """Calibrate speed of sound."""
        self._sound_speed = known_dist_m / self.distance() * self._sound_speed
        print("Speed of sound was successfully calibrated! \n" +
              "Current value: " + str(self._sound_speed) + " m/s")
