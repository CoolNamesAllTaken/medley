import threading
import time

from nfc_service import NFCScanner

nfc_scanner = NFCScanner()

# def run_nfc_service():
	

def main():
	nfc_scanner_thread = threading.Thread(target=nfc_scanner.run, daemon=True)
	nfc_scanner_thread.start()

	print("running nfc service")
	nfc_scanner.card_detected_ev.wait()
	print('Found card with UID: 0x{}{}{}{}'.format(
		nfc_scanner.card_id[0],
		nfc_scanner.card_id[1],
		nfc_scanner.card_id[2],
		nfc_scanner.card_id[3]))

if __name__ == '__main__':
	main()