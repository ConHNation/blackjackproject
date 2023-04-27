# This module creates and manages user balances.

# Dependencies
import logging

# Variable that stores user balances.
user_balances = {}

# Creates a balance for a new user.
def create_balance(username, difficulty):
	global user_balances
	if difficulty not in ["easy","medium","hard", "debug"]:
		return TypeError
  # Gives the user $2000 if on easy difficulty
	elif difficulty == "easy":
		user_balances[username] = 2000
		logging.info(f"User {username} balance successfully created.")
		return 2000
  # Gives the user $1000 if on medium difficulty
	elif difficulty == "medium":
		user_balances[username] = 1000
		logging.info(f"User {username} balance successfully created.")
		return 1000
	# Gives the user $500 if on hard difficulty
	elif difficulty == "hard":
		user_balances[username] = 500
		logging.info(f"User {username} balance successfully created.")
		return 500
  # Debug difficulty is designed to make testing the program
	# easier by giving the user $1,000,000 and showing
	# the user more info in the /logs file
	elif difficulty == "debug":
		user_balances[username] = 1000000
		logging.info(f"User {username} has activated debug mode with a balance of $1000000.")
		return 1000000
	# Returns an error if the difficulty doesn't exist
	else:
		logging.error(f"Error when creating user {username}'s balance on {difficulty} difficulty.")
		return Exception(f"Error when creating user {username}'s balance on {difficulty} difficulty.")

# Retuns the balance for the given username
def get_balance(username):
	global user_balances
	return user_balances[username]

# Removes an amount from the user's balance and returns their updated balance.
def remove_balance(username, amount):
	user_balances[username] -= amount
	logging.debug(f"Removed {amount} from user {username}'s balance.")
	return user_balances[username]

# Adds an amount to the user's balance and returns 
# their updated balance
def add_balance(username, amount):
	user_balances[username] += amount
	logging.debug(f"Added {amount} to user {username}'s balance.")
	return user_balances[username]

# Returns True if the user has the amount to gamele, otherwise
# returns False.
def has_wager(username, amount):
	if user_balances[username] >= amount:
		return True
	else:
		return False