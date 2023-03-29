# Blackjack - Server (Back-end) Program
# CSP Final Project
# Made by Connor Hayden, Dylan Lovell (I'm working on this module), Mateus Rudzki and Lance Hinojosa

# start logger
import logging
from datetime import datetime

# logging configuration
today = datetime.today()
logging.basicConfig(level=logging.DEBUG, filename=f'logs/serverlog-{str(today.month)}.{str(today.day)}-{str(today.hour)}:{str(today.minute)}:{str(today.second)}.txt', filemode='w', format='%(name)s - %(levelname)s - %(message)s')

# dependencies (not at start b/c i need 
# logging to start before files are loaded)
from deck import card
import deck
import balance
import packet
import threading