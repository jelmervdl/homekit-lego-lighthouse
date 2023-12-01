#!/usr/bin/env python3
import sys
import time
import signal
import buildhat
from pyhap.accessory import Accessory
from pyhap.accessory_driver import AccessoryDriver
from pyhap.const import CATEGORY_LIGHTBULB


# Docs:
#   - https://buildhat.readthedocs.io/en/latest/buildhat/light.html
#   - https://github.com/ikalchev/HAP-python

class Light(Accessory):
    category = CATEGORY_LIGHTBULB

    light: buildhat.Light
    motor: buildhat.PassiveMotor

    _speed: float
    _direction: int

    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._speed = 0
        self._direction = 1

        self.light = buildhat.Light('A')
        self.motor = buildhat.PassiveMotor('B')

        print("Buildhat initialised", file=sys.stderr)

        serv_light = self.add_preload_service('Lightbulb', chars=['On', 'Brightness'])
        self.char_on = serv_light.configure_char('On', setter_callback=self._set_on)
        self.char_brightness = serv_light.configure_char('Brightness', value=100, setter_callback=self._set_brightness)

        serv_fan = self.add_preload_service('Fan', chars=['RotationSpeed', 'RotationDirection'])
        self.char_rotation_on = serv_fan.configure_char('On', setter_callback=self._set_motor_on)
        self.char_rotation_speed = serv_fan.configure_char('RotationSpeed', setter_callback=self._set_rotation_speed)
        self.char_rotation_direction = serv_fan.configure_char('RotationDirection', setter_callback=self._set_rotation_direction)
    
    def _set_on(self, on:bool):
        if on:
            self.light.on()
            if self._speed > 0:
                self.char_rotation_on.value = True
            self._update_motor()
        else:
            self.light.off()
            self.char_rotation_on.value = False
            self.motor.stop()

    def _set_brightness(self, brightness:int):
        self.light.brightness(brightness)

    def _set_motor_on(self, on:bool):
        if on:
            self._update_motor()
        else:
            self.motor.stop()

    def _set_rotation_speed(self, speed:float):
        self._speed = speed
        self._update_motor()

    def _set_rotation_direction(self, direction):
        self._direction = 1 if direction == 1 else -1
        self._update_motor()

    def _update_motor(self):
        self.motor.start(self._direction * self._speed)

    def stop(self):
        self.light.off()
        self.motor.stop()

def main():
    # Start the accessory on port 51826
    driver = AccessoryDriver(port=51826)

    # Change `get_accessory` to `get_bridge` if you want to run a Bridge.
    driver.add_accessory(accessory=Light(driver, 'Lighthouse'))

    # We want SIGTERM (terminate) to be handled by the driver itself,
    # so that it can gracefully stop the accessory, server and advertising.
    signal.signal(signal.SIGTERM, driver.signal_handler)

    # Start it!
    driver.start()


retries = 5

while True:
    try:
        main()
    except (OSError, buildhat.exc.BuildHATError):
        if retries > 0:
            retries -= 1
            time.sleep(10)
        else:
            raise


