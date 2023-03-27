# Blackjack - Server (Back-end) Program
# CSP Final Project
# Made by Connor Hayden, Dylan Lovell (I'm working on this module), Mateus Rudzki and Lance Hinojosa

# dependencies
from deck import card
import deck
import balance
import packet
import threading
import tkthread
import logging

# initialize logging
log = logging.getLogger("main")
log.info("Starting game...")

# launch threading manager for tkinter
log.info("Launching Tkinter multithreading manager.")
try:
	tkthread.patch()
except Exception as e
:
	log.error(f"Error while starting Tkinter multithreading manager: {e}")
log.info("Started.")

# start panel thread
log.info("\nInitializing control panel...")
try:
	paneldisplaythread = threading.Thread(target=packet.panel.mainloop)
	paneldisplaythread.start()
except Exception as e:
	log.error(f"Error occured when starting panel file: {e}")
log.info("Panel started.")