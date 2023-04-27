# Blackjack - CSP Final Project

# Import logging-related dependencies.
import logging
from datetime import datetime
from time import sleep
import sys
from os import _exit

# Sets the configuration for the logging module, which
# records most functions into a .txt file located
# in the /logs folder.
try:
	today = datetime.today()
	logging.basicConfig(level=logging.INFO, filename=f'logs/gamelog-{str(today.month)}.{str(today.day)}-{str(today.hour)}:{str(today.minute)}:{str(today.second)}.txt', filemode='w', format='%(name)s - %(levelname)s - %(message)s')
except:
	raise RuntimeError(f"An issue occured when starting the logger: {sys.exc_info()[0]}")
	_exit(0)

# Dependencies (These are not at the start, as
# I need to have the logging function started
# before the modules are initialized.)
from deck import card
import deck
import balance
import logic
import terminal
from hint import hasDone5Card

try:
	# Asks the user what difficulty they would like to
	# play at. Difficulty affects payout and starting
	# balance.
	logging.debug("Selecting difficulty.")
	difficulty = input("Select difficulty (easy, medium, hard): ")
	
	# Sets the payout based on user input for difficulty.
	# Checks for valid input.
	while difficulty.lower() not in ["easy", "medium", "hard", "debug"]:
		logging.error(f"difficulty option was not found: {difficulty}")
		terminal.clearscreen()
		difficulty = input("Uh oh, that's not a valid option. Please try again.\nSelect difficulty (easy, medium, hard): ")
	# If difficulty is debug, generates deck from 2 decks, sets payout to 2x
	# and sets logging level to DEBUG.
	if difficulty.lower() == "debug":
		logging.getLogger().setLevel(level=logging.DEBUG)
		logging.info("Debug mode selected.")
		print("Debug mode activated.")
		try:
			logging.debug("Generating initial deck.")
			cur_deck = deck.new_deck(2)
		except TooManyDecksError as e:
			logging.error("System tried to generate too many decks, falling back to 4.")
			try:
				cur_deck = deck.new_deck(4)
			except:
				raise RuntimeError(f"An issue occured when generating the decks: {sys.exc_info()[0]}")
				_exit(0)
		payout = 2
	# If difficulty is easy, generates deck from 2 decks and sets payout to 2x.
	if difficulty.lower() == "easy":
		logging.info("Easy difficulty selected.")
		try:
			logging.debug("Generating initial deck.")
			cur_deck = deck.new_deck(2)
		except TooManyDecksError as e:
			logging.error("System tried to generate too many decks, falling back to 4.")
			try:
				cur_deck = deck.new_deck(4)
			except:
				raise RuntimeError(f"An issue occured when generating the decks: {sys.exc_info()[0]}")
				_exit(0)
		payout = 2
	# If difficulty is medium, sets the payout to 1.75x and generates a 
	# deck with 4 different decks
	elif difficulty.lower() == "medium":
		logging.info("Medium difficulty selected.")
		payout = 1.75
		try:
			logging.debug("Generating initial deck.")
			cur_deck = deck.new_deck(4)
		except TooManyDecksError as e:
			logging.error("System tried to generate too many decks, falling back to 4.")
			try:
				cur_deck = deck.new_deck(4)
			except:
				raise RuntimeError(f"An issue occured when generating the decks: {sys.exc_info()[0]}")
				_exit(0)
	# If difficulty is hard, sets payout to 1.5x and generates a deck
	# with 8 decks.
	elif difficulty.lower() == "hard":
		logging.info("Hard difficulty selected.")
		payout = 1.5
		try:
			logging.debug("Generating initial deck.")
			cur_deck = deck.new_deck(8)
		except TooManyDecksError as e:
			logging.error("System tried to generate too many decks, falling back to 4.")
			try:
				cur_deck = deck.new_deck(4)
			except:
				raise RuntimeError(f"An issue occured when generating the decks: {sys.exc_info()[0]}")
				_exit()
		except:
			raise RuntimeError(f"An issue occured when generating the decks: {sys.exc_info()[0]}")
			_exit()
	
	# Creates the user balance based on user input.
	userbalance = balance.create_balance("main", difficulty.lower())
	starting_balance = userbalance
	
	# Defines the wager variable for later use.
	wager = ""
	
	# Game loop.
	while True:
		# Ends the game if the user has less than
		# the table minimum bet ($100).
		if userbalance <= 100:
			logging.info("User has run out of money.")
			print("\nEnding game in 3 seconds...")
			sleep(3)
			terminal.clearscreen()
			print("-"*28)
			print("You lost all your money...")
			print("\nGambling is an addiction.")
			print("Get some help.")
			print("-"*28)
			logging.info("Ending game...")
			break
		# Regenerates the deck if it is empty
		if not deck:
			print("-"*28)
			print("Shuffling deck...")
			logging.debug("Deck is empty. Generating new deck.")
			cur_deck = deck.new_deck(4)
			print("Deck shuffled.")
		# Displays the current user balance
		print("-"*28)
		logging.debug(f"Current Balance: {userbalance}")
		print("Your balance: ${:,.2f}".format(userbalance))
	
		# Asks the user for their wager amount.
		wager = input(f"Table pays {payout}x\nSay amount to wager or 'q' to quit (Min bet: $100): ")
		# Ends the game if the user quits.
		if "q" in wager.lower():
			logging.debug("User ended game via input.")
			print("-"*28)
			print(f"Game ended.")
			if starting_balance < userbalance:
				print("\nYou won - You finished with ${:,.2f} (+${:,.2f}).\n\nThanks for playing!".format(userbalance, userbalance-starting_balance))
			elif starting_balance > userbalance:
				print("\nHouse wins! - You finished with ${:,.2f} (-${:,.2f}).\n\nThanks for playing!".format(userbalance, userbalance-starting_balance))
			else:
				print("Goodbye o/")
			print("-"*28)
			logging.info("Ending game...")
			break
		while not wager.isdigit():
			print("-"*28)
			wager = input(f"Invalid amount. Please say a numerical value.\n\nTable pays {payout}x\nSay amount to wager or 'q' to quit (Min bet: $100): ")
		# Asks the user for a new wager while it is
		# less than $100.
		while float(wager) < 100:
			wager = input("Below minimum bet.\nSay amount to wager or 'q' to quit (Min bet: $100): ")
		# Asks the user for a new wager while they 
		# don't have that amount to bet.
		while not balance.has_wager("main", int(wager)):
			logging.error(f"User only has ${userbalance}, which is less than ${wager}.")
			wager = input(f"You don't have enough money. Balance: ${userbalance}\n\nSay amount to wager or 'q' to quit (Min bet: $100): ")
		# Checks once again if the user has quit to
		# avoid errors. If not, wager is converted
		# to a float.
		if "q" in wager.lower():
			print("goodbye o/")
			logging.debug("User closed game.")
			logging.info("Ending game...")
			active = False
			break
		else:
			wager = float(wager)
	
		# Removes the bet from the user's balance.
		userbalance = balance.remove_balance("main", wager)
	
		# Defines the game_result variable for later use.
		game_result = None
		turnEnded = False
	
		print("\nGood luck.")
		logging.info("New round started.")
	
		# Defines the variables for the dealer and player's
		# current hands.
		dealer_cards = []
		player_cards = []
	
		# Generates the initial two cards for the player.
		player_cards.append(cur_deck.pop())
		player_cards.append(cur_deck.pop())
		logging.debug(f"Player cards generated - {str(player_cards)}")
	
		# Generates the initial card for the dealer.
		dealer_cards.append(cur_deck.pop())
		logging.debug(f"Dealer cards generated - {str(dealer_cards)}")
		
		print("-"*28)
		# Calculates the current status of the game. (Finished, user won, user lost, etc.)
		result = logic.result(player_cards, dealer_cards)
		# If the game has already finished (either player had blackjack)
		if "active" not in result:
			# Adds wager * payout to user balance, shows user as winner and both hands are shown.
			if "win" in result:
				print("-"*28)
				logging.info(f"User won.")
				print("You won.")
				print(f"\nYou ({str(deck.getprintedtotal(player_cards)).replace('[', '').replace(']', '')}):")
				for card in player_cards:
					print(card)
				print(f"\nDealer ({str(deck.getprintedtotal(dealer_cards)).replace('[', '').replace(']', '')}):")
				for card in dealer_cards:
					print(card)
				userbalance = balance.add_balance("main", wager*payout)
				logging.debug(f"New Balance: ${userbalance}")
			# Shows dealer as winner and both hands are shown.
			elif "loss" in result:
				logging.info(f"User lost. Dealer won.")
				print("-"*28)
				print("You lost.")
				print(f"\nYou ({str(deck.getprintedtotal(player_cards)).replace('[', '').replace(']', '')}):")
				for card in player_cards:
					print(card)
				print(f"\nDealer ({str(deck.getprintedtotal(dealer_cards)).replace('[', '').replace(']', '')}):")
				for card in dealer_cards:
					print(card)
				logging.debug(f"New Balance: ${userbalance}")
			# Adds the wager back to the user's balance and both 
			# hands are shown.
			elif "push" in result:
				logging.info(f"User tied. Push.")
				print("-"*28)
				print("You tied, push.")
				print(f"\nYou ({str(deck.getprintedtotal(player_cards)).replace('[', '').replace(']', '')}):")
				for card in player_cards:
					print(card)
				print(f"\nDealer ({str(deck.getprintedtotal(dealer_cards)).replace('[', '').replace(']', '')}):")
				for card in dealer_cards:
					print(card)
				userbalance = balance.add_balance("main", wager*payout)
				logging.debug(f"New Balance: ${userbalance}")
			# Ends turn if blackjack.
			elif "bj" in result:
				logging.info(f"User has blackjack.")
				print("Blackjack. You won.")
				print(f"\nYou ({str(deck.getprintedtotal(player_cards)).replace('[', '').replace(']', '')}):")
				for card in player_cards:
					print(card)
				print(f"\nDealer ({str(deck.getprintedtotal(dealer_cards)).replace('[', '').replace(']', '')}):")
				for card in dealer_cards:
					print(card)

				userbalance = balance.add_balance("main", wager*payout)
			# Shows an error if the game ended but nobody won.
			else:
				raise RuntimeError("Game ended but no winner was found.")
				active = False
		else:
			# Shows player hand
			print(f"You ({str(deck.getprintedtotal(player_cards)).replace('[', '').replace(']', '')}):")
			for card in player_cards:
				print(card)
		
			# Shows dealer hand
			print(f"\nDealer ({str(deck.getprintedtotal(dealer_cards)).replace('[', '').replace(']', '')}):")
			for card in dealer_cards:
				print(card)
		
			# Asks the user for their turn choice
			if difficulty == "debug":
				print(f"\n(Next card: {cur_deck[-1]})")
			choice = input('\nSay "hit" or "stand": ')
			while choice not in ["hit", "stand"]:
				logging.error(f'turn option "{choice}" not found.')
				choice = input('\nInvalid option. Valid options are "hit" and "stand".\nSay "hit" or "stand": ')
			while choice == "hit":
				# Gets a card from the deck and adds it to the user's han
				logging.debug("User chose hit.")
				card = cur_deck.pop()
				player_cards.append(card)
				logging.debug(f"Drawn card: {card}")
				# Ends the user's turn if they are over 21.
				if logic.result(player_cards, dealer_cards) == "bust":
					logging.info("User went over 21. Bust.")
					print("-"*28)
					print("Over 21, you busted.")
					choice = "stand"
					break
				# Ends the user's turn if they have more than 5 cards.
				elif logic.result(player_cards, dealer_cards) == "win":
					logging.info("User was declared as winner mid-turn. This is likely due to the 5 card rule.")
					if hasDone5Card:
						print("\n5 card rule, turn over.")
					choice = "stand"
					game_result = "win"
					turnEnded = True
					break
				elif logic.result(player_cards, dealer_cards) == "bj":
					logging.info("User has blackjack mid-turn, ending turn.")
					print("\nBlackjack.")
					choice = "stand"
					break
				# Continues the user's turn if they are under 21.
				else:
					print("-"*28)
					# Prints the user's hand
					print(f"You ({str(deck.getprintedtotal(player_cards)).replace('[', '').replace(']', '')}):")
					for card in player_cards:
						print(card)
					# Prints the dealer's hand
					print(f"\nDealer ({str(deck.getprintedtotal(dealer_cards)).replace('[', '').replace(']', '')}):")
					for card in dealer_cards:
						print(card)
					if difficulty == "debug":
						print(f"\n(Next card: {cur_deck[-1]})")
					choice = input('\nSay "hit" or "stand": ')
					while choice not in ["hit", "stand"]:
						choice = input('\nInvalid option. Valid options are "hit" and "stand".\nSay "hit" or "stand": ')
			# Ends the user's turn and finishes the round if the 
			# user chose to stand.
			if choice == "stand":
				logging.info("User stood. Calculating result...")
				dealer_total = deck.gettotal(dealer_cards)
				# Dealer hits until they are at 17 or higher. 
				# (Only runs if total contains aces)
				if type(dealer_total) == list:
					while (dealer_total[0] < 17 or dealer_total[1] < 17):
						logging.debug("Dealer hit.")
						card = cur_deck.pop()
						dealer_cards.append(card)
						logging.debug(f"Drawn card: {card}")
						if logic.result(player_cards, dealer_cards) == "loss":
							logging.info("Dealer was declared as winner mid-turn. This is likely due to the 5 card rule.")
							game_result = "loss"
							turnEnded = True
							break
						else:
							dealer_total = deck.gettotal(dealer_cards)
				# Dealer hits until they are at 17 or higher.
				else:
					while dealer_total < 17:
						logging.debug("Dealer hit.")
						card = cur_deck.pop()
						dealer_cards.append(card)
						logging.debug(f"Drawn card: {card}")
						dealer_total = deck.gettotal(dealer_cards)
						if logic.result(player_cards, dealer_cards) == "loss":
							logging.info("Dealer was declared as winner mid-turn. This is likely due to the 5 card rule.")
							game_result = "loss"
							turnEnded = True
							break
						elif type(dealer_total) == list:
							break
				# Calculates the result of the game.
				if not turnEnded:
					game_result = logic.result(player_cards, dealer_cards, True)
				# Adds wager*payout to the user's balance, displays
				# the user as the winner and shows both hands
				if game_result == "win":
					logging.info("User won.")
					print("-"*28)
					print("You won!")
					print(f"\nYou ({str(deck.getprintedtotal(player_cards, True)).replace('[', '').replace(']', '')}):")
					for card in player_cards:
						print(card)
					print(f"\nDealer ({str(deck.getprintedtotal(dealer_cards, True)).replace('[', '').replace(']', '')}):")
					for card in dealer_cards:
						print(card)
					userbalance = balance.add_balance("main", wager*payout)
					logging.debug(f"New Balance: {userbalance}")
				# Displays the dealer as the winner and shows both hands.
				elif game_result == "loss":
					logging.info("User lost.")
					print("-"*28)
					print("You lost. Better luck next time.")
					print(f"\nYou ({str(deck.getprintedtotal(player_cards, True)).replace('[', '').replace(']', '')}):")
					for card in player_cards:
						print(card)
					print(f"\nDealer ({str(deck.getprintedtotal(dealer_cards, True)).replace('[', '').replace(']', '')}):")
					for card in dealer_cards:
						print(card)
				# Adds the wager back to the user's balance and displays
				# the game as a tie. Both hands are shown.
				elif game_result == "push":
					print("-"*28)
					print("You tied, push.")
					print(f"\nYou ({str(deck.getprintedtotal(player_cards, True)).replace('[', '').replace(']', '')}):")
					for card in player_cards:
						print(card)	
					print(f"\nDealer ({str(deck.getprintedtotal(dealer_cards, True)).replace('[', '').replace(']', '')}):")
					for card in dealer_cards:
						print(card)
					userbalance = balance.add_balance("main", wager)
				else:
					# Raises an error if the game finished but
					# no winner could be calculated
					logging.error("Failed to calculate winner.")
					raise RuntimeError("Something went wrong (Failed to calculate winner). Check /logs file for more info.")
					_exit(0)
			else:
				# Raises an error if no winner could be calculated.
				logging.error("Failed to calculate winner.")
				raise RuntimeError("Something went wrong when calculating the winner. Check /logs file for more info.")
				_exit(0)
except KeyboardInterrupt:
	logging.info("Game was force closed.")
	print('\n' + "-"*28)
	print(f"Game closed.")
	if starting_balance < userbalance:
		print("\nYou won! - You finished with ${:,.2f} (+${:,.2f}).\n\nThanks for playing!".format(userbalance, userbalance-starting_balance))
	elif starting_balance > userbalance:
		print("\nHouse wins! - You finished with ${:,.2f} (-${:,.2f}).\n\nThanks for playing!".format(userbalance, userbalance-starting_balance))
	else:
		print("Goodbye o/")
	print("-"*28)
	logging.info("Ending game...")
	_exit(0)
except:
	raise RuntimeError("Game process was interrupted. Check /logs for more info.")
	_exit(0)