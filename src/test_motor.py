import threading
import time
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)

from utils import *

from rotor_service import RotorEncoder
import medley_chat

BT_PIN = 27
BT_DEBOUNCE_MILLIS = 200

rotor_encoder = RotorEncoder(GPIO)

# def run_nfc_service():
	

def main():
	# GPIO Configuration
	GPIO.setup(BT_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
	button_db_millis = millis()


	rotor_encoder_thread = threading.Thread(target=rotor_encoder.run_rotor_listener, daemon=True)
	rotor_encoder_thread.start()

	print("Initialization Complete")
	
	while True:
		if millis() - button_db_millis > BT_DEBOUNCE_MILLIS and not GPIO.input(BT_PIN):
			button_db_millis = millis()
			print("target pos {}, current pos {}".format(rotor_encoder.target_rotor_pos, rotor_encoder.rotor_pos))
			rotor_encoder.increment_rotor_pos()

if __name__ == '__main__':
	main()
	# try:
	# 	main()
	# except:
	# 	GPIO.cleanup()