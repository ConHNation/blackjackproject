# We were originally gonna make this multiplayer
# but couldn't figure it out. Here's the code for
# it though.

'''
# Packet reviever, sender and translator

# dependencies
import logging
import socket
import datetime
import threading
import tkinter as tk

# config
server = None
HOST_ADDR = "127.0.0.1"
HOST_PORT = 1250

# local variables
clients = []
clients_names = []

# packet reciever
logging.info("Initializing packet reciever.")

# gui panel to control server
panel = tk.Tk()
panel.title("Blackjack - Server Panel")

header = tk.Frame(panel)

#header
startButton = tk.Button(header, text="Start", command=lambda: start_server())
startButton.pack(side=tk.LEFT)

stopButton = tk.Button(header, text="Stop", command=lambda: stop_server(), state=tk.DISABLED)
stopButton.pack(side=tk.LEFT)

header.pack(side=tk.TOP, pady=(5, 0))

# function to start server
def start_server():
	global HOST_PORT, HOST_ADDR, server, startButton, stopButton

	# sets server object
	logging.debug("Creating server socket object.")
	server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	# starts a thread that listens for new players
	logging.info("Moving listener to seperate thread.")
	threading._start_new_thread(accept_clients, (server, " "))
	logging.info("Listener online.")
	

def accept_clients(server, yeah):
	global server, HOST_PORT, HOST_ADDR, startButton, stopButton
	
	# starts server process
	logging.info("Initializing listener for new players.")
	server.bind((HOST_ADDR, HOST_PORT))
	server.listen()
	
	# flips the start and stop buttons
	startButton.config(state=tk.DISABLED)
	stopButton.config(state=tk.NORMAL)


def stop_server():
	global server
	startButton.config(state=tk.NORMAL)
	stopButton.config(state=tk.DISABLED)

	
# runs the panel
logging.info("Loading admin panel...")
panel.mainloop()
logging.info("Admin panel loaded.")
'''