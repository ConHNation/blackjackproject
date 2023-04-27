# Module to manage console-related changes and processes.

# Dependencies
##from threading import Thread, Lock (unused)
from logging import debug
##from time import sleep (unused)
from os import system,name
##import sys (unused)
##import cursor (unused)

# Functions
'''
The following was code that was designed to have a color changing line.
I likely won't include this in the final submission, but I'll leave it
in case I ever come back to it.

# Variable for managing terminal.
terminal_lock = Lock()

# Function to get the current line number.
def getcurrentline():
	with terminal_lock:
		return cursor.get_position()[1]

# Function to update a color changing line.
def updateline(length, startline):
	while True:
		with terminal_lock:
			cursor.move(0, startline)
			sys.stdout.write("\033[0;31m-\033[0m-" * int(length/2) + '\033[0m', end='')
			sys.stdout.flush()
			sleep(1)

			cursor.move(0, startline)
			sys.stdout.write("\033[0m-\033[0;31m-" * int(length/2) + '\033[0m', end='')
			sys.stdout.flush()
			sleep(1)

# Prints a line and assigns and starts a thread to update it.
def line(length):
	sys.stdout.write("\n")
	sys.stdout.flush()
	startline = getcurrentline() - 1
	thread = Thread(target = updateline, args = (length, startline))
	thread.daemon = True
	thread.start()
	return thread
'''

# Function to clear all lines in the terminal.
def clearscreen():
	# Changes system command for clearing console based on OS.
	system('cls' if name=='nt' else 'clear')
	debug("Console cleared by function call.")