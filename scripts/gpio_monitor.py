import RPi.GPIO as GPIO
import time
import subprocess
import os
import logging


# Configure logging
logging.basicConfig(filename='/var/log/gpio_monitor.log', level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')


# Set up GPIO 13 as an input
GPIO.setmode(GPIO.BCM)
GPIO.setup(13, GPIO.IN, pull_up_down=GPIO.PUD_UP)
button_pressed_time = None
# Get the path to the current script
script_path = os.path.realpath(__file__)

# Get the directory of the current script
script_dir = os.path.dirname(script_path)

# Get the path to the other script
other_script_path = os.path.join(script_dir, "run.sh")

# Check the status of GPIO 13 every second
while True:
    # If GPIO 13 is pressed for 3 seconds, execute the script
    if GPIO.input(13) == 0:
        if button_pressed_time == None:
            button_pressed_time = time.time
            logging.log("Button Press Detected")
        time.sleep(3)
        if GPIO.input(13) == 0:
            # Execute the script
            logging.log("Button Pressed for 3 seconds")
            subprocess.run(["sleep","15",other_script_path])
        else:
            # Execute the script
            logging.log("Button Pressed but not for 3 seconds")
    else:
        logging.log("Button Not Pressed ")

# Clean up GPIO
GPIO.cleanup()