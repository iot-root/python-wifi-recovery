import RPi.GPIO as GPIO
import time
import subprocess
import os

# Set up GPIO 13 as an input
GPIO.setmode(GPIO.BCM)
GPIO.setup(13, GPIO.IN)
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
        time.sleep(3)
        if GPIO.input(13) == 0:
            # Execute the script
            subprocess.run([other_script_path])

# Clean up GPIO
GPIO.cleanup()