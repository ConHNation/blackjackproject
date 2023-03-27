# Packet reviever, sender and translator

# dependencies
import logging
import socket
import threading
import tkinter as tk

# config
server = None
HOST_ADDR = "127.0.0.1"
HOST_PORT = 1250

# initialize logger
log = logging.getLogger("Packet Manager")

# packet reciever
log.info("Initializing packet reciever.")

# gui panel to control server
panel = tk.Tk()
panel.title = "Blackjack - Administrator Panel"

header = tk.Frame(panel)

#header
startButton = tk.Button(header, text="Start", command=lambda: start_server())
startButton.pack(side=tk.LEFT)

stopButton = tk.Button(header, text="Stop", command=lambda: stop_server(), state=tk.DISABLED)
stopButton.pack(side=tk.LEFT)

header.pack(side=tk.TOP, pady=(5, 0))

# function to start server
def start_server():
	global HOST_PORT, HOST_ADDR, log, server, startButton, stopButton

	# sets server object
	log.debug("Creating server socket object.")
	server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	print(socket.AF_INET)
	print(socket.SOCK_STREAM)

	# starts listening for new players
	log.info("Initializing listener for new players.")
	server.bind((HOST_ADDR, HOST_PORT))
	server.listen(5)
	log.info("Listener online.")

  # starts a thread that listens for new players
def accept_clients():
	log.info("Moving listener to seperate thread.")
	threading._start_new_thread(accept_clients, (server, ""))

	# flips the start and stop buttons
	startButton.state = tk.DISABLED
	stopButton.state = tk.ENABLED

def stop_server():
	pass