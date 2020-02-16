import threading
import time
import RPi.GPIO as GPIO

from utils import *

from nfc_service import NFCScanner
from rotor_service import RotorEncoder
from audio.medley_chat import *

BT_PIN = 27
BT_DEBOUNCE_MILLIS = 200


nfc_scanner = NFCScanner()
rotor_encoder = RotorEncoder(GPIO)

# def run_nfc_service():
	

def main():
	# GPIO Configuration
	GPIO.setup(BT_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
	button_db_millis = millis()

	# Thread Configuration
	nfc_scanner_thread = threading.Thread(target=nfc_scanner.run_nfc_listener, daemon=True)
	nfc_scanner_thread.start()

	rotor_encoder_thread = threading.Thread(target=rotor_encoder.run_rotor_listener, daemon=True)
	rotor_encoder_thread.start()

	print("highhhh")
	while True:
		if millis() - button_db_millis > BT_DEBOUNCE_MILLIS and not GPIO.input(BT_PIN):
			button_db_millis = millis()
			# print("target pos {}, current pos {}".format(rotor_encoder.target_rotor_pos, rotor_encoder.rotor_pos))
			# rotor_encoder.increment_rotor_pos()
			start_chat()
		# 	if motor_pwm_duty_cycle < 100:
		# 		motor_pwm_duty_cycle += 0.1
		# else:
		# 	motor_pwm_duty_cycle = 0
		# motor_pwm.ChangeDutyCycle(motor_pwm_duty_cycle)

	# NFC Test
	print("running nfc service")
	nfc_scanner.card_detected_ev.wait()
	print('Found card with UID: 0x{}{}{}{}'.format(
		nfc_scanner.card_id[0],
		nfc_scanner.card_id[1],
		nfc_scanner.card_id[2],
		nfc_scanner.card_id[3]))

if __name__ == '__main__':
	main()
	# try:
	# 	main()
	# except:
	# 	GPIO.cleanup()