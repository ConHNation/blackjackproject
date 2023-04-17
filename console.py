# Module to manage console-related changes and processes
# dependencies
from threading import Thread
from logging import info, debug
from time import wait
from inspect import currentframe

# functions
# function to get current line
def getcurrentline():
  frame = currentframe()
  return frame.f_back.f_lineno

# functions to manage color changing line
def updateline(line, length, startline):
	while int(20 - getcurrentline()) > 0:
		line = print("\033[0;31m-\033[0m-"*length, end="\r")
		wait(1)
		line = print("\033[0m-\033[0;31m"*length, end="\r")
def line(length):
	line = print("\033[0m-\033[0;31m"*length, end="\r")
	thread = Thread(target = updateline, args = (line, length, getcurrentline()))
	thread.start()
	thread.join()