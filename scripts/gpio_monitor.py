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
print(other_script_path)
# Check the status of GPIO 13 every second
while True:
    # If GPIO 13 is pressed for 3 seconds, execute the script
    if GPIO.input(13) == 0:
        print("button pressed")
        button_pressed_time = time.time()
        logging.info("Button press detected")
        while GPIO.input(13) == 0:
            time.sleep(0.1)
        elapsed = time.time() - button_pressed_time
        if elapsed >= 3:
            print("button pressed for more than 3 seconds")
            logging.info("Button was pressed for 3 seconds, switching modes...")
            print("calling script")
            subprocess.run([other_script_path])
            print("script run completed")
        else:
            logging.info("Button was pressed but not long enough, ignoring.")
            print("button pressed less than 3 seconds")

# Clean up GPIO
GPIO.cleanup()
