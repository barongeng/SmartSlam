#!/usr/bin/env python3

import time
import RPi.GPIO as GPIO
import json
import logging
import os
import subprocess


#####################

def led_on():
    """ Turns on LED """
    logging.info('Turning LED ON...')
    GPIO.output(pin_led, GPIO.HIGH)


def led_off():
    """ Turns off LED """
    logging.info('Turning LED OFF...')
    GPIO.output(pin_led, GPIO.LOW)


def led_switch():
    """ Switch LED status """
    if GPIO.input(pin_led) == 0:
        GPIO.output(pin_led, GPIO.HIGH)
    else:
        GPIO.output(pin_led, GPIO.LOW)


def record():
    """ Records sound """
    logging.info('Start RECORDING...duration:' + str(settings['sample_duration']))
    subprocess.call([
        "sh",
        "mic.sh",
        str(settings['audio_device_hw_number']),
        str(settings['sample_duration']),
        settings['samples_dir']
    ])
    logging.info('End RECORDING')


def get_user():
    """ Get the user who is running the script """
    # logging.info('Getting user...') #  Not possible because the command is run before log configuration
    return subprocess.check_output(["whoami"], universal_newlines=True).splitlines()[0]


#####################
# SETUP
os.chdir(os.path.join('home', get_user(), 'SmartSlam', 'RaspberryScripts'))
# LOG setup
log_dir = os.path.join(os.getcwd(), 'LOG')
if not os.path.exists(log_dir):
    os.makedirs(log_dir)
logging.basicConfig(filename=os.path.join(log_dir, 'INFO.log'),
                    level=logging.INFO,
                    format='%(asctime)-15s '
                           '%(levelname)s '
                           '--%(filename)s-- '
                           '%(message)s')

logging.info('START')
logging.info('Working Directory: ' + str(os.path.join('home', get_user(), 'SmartSlam', 'RaspberryScripts')))
logging.info('LOG Directory: ' + log_dir)
logging.info('Setting Up...')

settings = json.load(open('settings.json'))

# Raspberry
GPIO.setmode(GPIO.BOARD)

pin_pir_input = settings['pir_pin_board']
GPIO.setup(pin_pir_input, GPIO.IN)

pin_led = settings['led_pin_board']
GPIO.setup(pin_led, GPIO.OUT)

pir_time_interval = settings['pir_time_interval']

#####################
# PIR cycle

logging.info('Starting PIR waiting cycle...')

while True:
    i = GPIO.input(pin_pir_input)
    if i == 1:  # detection
        logging.info('PIR detection')
        led_on()
        record()
        led_off()

    time.sleep(0.1)
