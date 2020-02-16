import threading
import board
import serial

from drivers.adafruit_pn532_uart import PN532_UART

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
			uid = self.pn532.read_passive_target(timeout=0.01)
			# Try again if no card is available.
			if uid is None:
				continue
			# Store the card ID and awaken all waiting threads
			self.card_id = uid
			self.card_detected_ev.set()
