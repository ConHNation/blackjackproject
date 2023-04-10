# Made by Lance Hinojosa
# Module to manage balances.

# dependencies
import logging

user_balances = {}

# creates balance for user
def create_balance(username, difficulty):
	global user_balances
	if difficulty not in ["easy","medium","hard"]:
		return TypeError
    # if balance is easy, you'll get 2000
	elif difficulty == "easy":
		user_balances[username] = 2000
		logging.info(f"User {username} balance successfully created.")
		return 2000
    # if balance 
	elif difficulty == "medium":
		user_balances[username] = 1000
		logging.info(f"User {username} balance successfully created.")
		return 1000
	elif difficulty == "hard":
		user_balances[username] = 500
		logging.info(f"User {username} balance successfully created.")
		return 500
	else:
		logging.error(f"Error when creating user {username} balance.")
		return Exception

def get_balance(username):
	global user_balances
	return user_balances[username]

def remove_balance(username, amount):
	user_balances[username] -= amount
	return user_balances[username]

def add_balance(username, amount):
	user_balances[username] += amount
	return user_balances[username]

def has_wager(username, amount):
	if user_balances[username] >= amount:
		return True
	else:
		return False
  