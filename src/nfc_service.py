import threading
import board
import serial
import subprocess

from drivers.adafruit_pn532_uart import PN532_UART

card_uid_dict = { \
	"41021318": 0, \
	"419018818": 1}

class NFCScanner:
	def __init__(self, verbose=0):
		self.uart = serial.Serial("/dev/ttyS0", baudrate=115200, timeout=0.001)
		self.pn532 = PN532_UART(self.uart, debug=False)
		self.ic, self.ver, self.rev, self.support = self.pn532.get_firmware_version()
		# Configure PN532 to communicate with MiFare cards
		self.pn532.SAM_configuration()
		if (verbose):
			print("Configured NFC Scanner")

		self.card_detected_ev = threading.Event()
		self.card_id = 0xDEADBEEF

	def run_nfc_listener(self):
		while True:
			 # Check if a card is available to read
			uid = self.pn532.read_passive_target(timeout=0.1)
			# Try again if no card is available.
			if uid is None:
				continue
			# Store the card ID and awaken all waiting threads
			self.card_id = uid
			self.card_detected_ev.set()

	def scan_card(self):
		# wait for a new card to be scanned
		self.card_detected_ev.clear()
		self.card_detected_ev.wait()

		card_uid_str = "{}{}{}{}".format(
			self.card_id[0],
			self.card_id[1],
			self.card_id[2],
			self.card_id[3])

		print('Found card with UID: {}'.format(card_uid_str))
		subprocess.call(["aplay", "../media/beedooboop.wav"])

		# print(str(self.card_id))
		user_num = -1
		if card_uid_str in card_uid_dict:
			user_num = card_uid_dict[card_uid_str]
			print("User: {}".format(user_num))

		else:
			print("User not found")
		# play beep sound?
		return user_num
