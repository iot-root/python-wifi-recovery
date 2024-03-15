#!/usr/bin/env python3
import RPi.GPIO as GPIO
import time
import subprocess
import logging
import os 

# Configure logging
logging.basicConfig(filename='/var/log/gpio_monitor.log', level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')
# Get the path to the current script
script_path = os.path.realpath(__file__)

    # Get the directory of the current script
script_dir = os.path.dirname(script_path)

    # Get the path to the other script
other_script_path = os.path.join(script_dir, "run.sh")
print(other_script_path)
# Set up GPIO pin
pin = 13
GPIO.setmode(GPIO.BCM)
GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

button_pressed_time = None

def button_pushed_callback(channel):
    global button_pressed_time
    if GPIO.input(pin) == 0:  # Button is pressed
        if button_pressed_time is None:
            button_pressed_time = time.time()
            logging.info("Button press detected")
    else:  # Button is released
        if button_pressed_time is not None:
            elapsed = time.time() - button_pressed_time
            button_pressed_time = None
            if elapsed >= 3:  # Button was pressed for 3 or more seconds
                logging.info("Button was pressed for 3 seconds, switching modes...")
                print("calling script")
                subprocess.run([other_script_path])
                print("script run completed")
            else:
                logging.info("Button was pressed but not long enough, ignoring.")

GPIO.add_event_detect(pin, GPIO.BOTH, callback=button_pushed_callback, bouncetime=200)

try:
    logging.info("Starting GPIO monitoring service")
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    GPIO.cleanup()
    logging.info("GPIO monitoring service stopped")
