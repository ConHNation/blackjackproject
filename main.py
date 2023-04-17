# Blackjack
# CSP Final Project

# start logger
import logging
from datetime import datetime
from time import sleep
import os

# logging configuration
today = datetime.today()
logging.basicConfig(level=logging.INFO, filename=f'logs/serverlog-{str(today.month)}.{str(today.day)}-{str(today.hour)}:{str(today.minute)}:{str(today.second)}.txt', filemode='w', format='%(name)s - %(levelname)s - %(message)s')

# dependencies (not at start b/c i need 
# logging to start before files are loaded)
from deck import card
import deck
import balance
import logic
# import packet
logging.debug("Generating new deck.")
cur_deck = deck.new_deck(4)

# local variable
active = True

# logging setup
logging.debug("Selecting difficulty.")
difficulty = input("Select difficulty (easy, medium, hard): ")

# terminal clear function
def clearscreen():
  os.system('cls' if os.name=='nt' else 'clear')

# debug difficulty
if difficulty == "debug":
	logging.getLogger().setLevel(level=logging.DEBUG)
	logging.info("Debug mode selected.")
	print("Debug mode activated.")
	payout = 2
if difficulty == "easy":
	logging.info("Easy difficulty selected.")
	payout = 2
elif difficulty == "medium":
	logging.info("Medium difficulty selected.")
	payout = 1.75
elif difficulty == "hard":
	logging.info("Hard difficulty selected.")
	payout = 1.5
else:
	payout = 1.5

userbalance = balance.create_balance("main", difficulty.lower())

wager = ""

while active:
	if userbalance <= 100:
		logging.info("User has run out of money.")
		print("\nEnding game in 3 seconds...")
		sleep(3)
		clearscreen()
		print("-"*28)
		print("you lost all your money...")
		print("\ngambling is an addiction")
		print("get some help")
		print("-"*28)
		logging.info("Ending game...")
		break
	print("--------------------")
	logging.debug(f"Current Balance: {userbalance}")
	print(f"Your balance: {userbalance}")

	wager = input(f"Table pays {payout}x\nSay amount to wager or 'q' to quit (Min bet: 100): ")
	if "q" in wager:
		print("goodbye")
		logging.debug("User closed game.")
		logging.info("Ending game...")
		active = False
		break
	while float(wager) < 100:
		wager = input("Below minimum bet.\nSay amount to wager or 'q' to quit (Min bet: 100): ")
	while not balance.has_wager("main", int(wager)):
		logging.error(f"User only has {userbalance}, which is less than {wager}.")
		wager = input(f"You don't have enough money. Balance: {userbalance}\n\nSay amount to wager or 'q' to quit (Min bet: 100): ")

	if "q" in wager.lower():
		print("goodbye")
		logging.debug("User closed game.")
		logging.info("Ending game...")
		active = False
		break
	else:
		wager = float(wager)
		
	userbalance = balance.remove_balance("main", wager)

	print("\nGood luck.")
	logging.info("New round started.")
	
	dealer_cards = []
	player_cards = []

	player_cards.append(cur_deck.pop())
	player_cards.append(cur_deck.pop())
	logging.debug(f"Player cards generated - {str(player_cards)}")

	dealer_cards.append(cur_deck.pop())
	logging.debug(f"Dealer cards generated - {str(dealer_cards)}")
	
	print("--------------------")
	result = logic.result(player_cards, dealer_cards)
	if "active" not in result:
		if "win" in result:
			print("--------------------")
			logging.info(f"User won.")
			print("you won")
			print(f"\nYou ({deck.getprintedtotal(player_cards)}):")
			for card in player_cards:
				print(card)
			print(f"\n\u001b[31mDealer ({deck.getprintedtotal(dealer_cards)}):")
			for card in dealer_cards:
				print(card)
			userbalance = balance.add_balance("main", wager*payout)
			logging.debug(f"New Balance: {userbalance}")
		elif "loss" in result:
			logging.info(f"User lost. Dealer won.")
			print("--------------------")
			print("you lost")
			print(f"\nYou ({deck.getprintedtotal(player_cards)}):")
			for card in player_cards:
				print(card)
			print(f"\n\u001b[31mDealer ({deck.getprintedtotal(dealer_cards)}):\u001b[0m")
			for card in dealer_cards:
				print(card)
		elif "push" in result:
			logging.info(f"User tied. Push.")
			print("--------------------")
			print("you tied - push")
			print(f"\nYou ({deck.getprintedtotal(player_cards)}):")
			for card in player_cards:
				print(card)
			print(f"\n\u001b[31mDealer ({deck.getprintedtotal(dealer_cards)}):\u001b[0m")
			for card in dealer_cards:
				print(card)
			userbalance = balance.add_balance("main", wager*payout)
			logging.debug(f"New Balance: {userbalance}")
		else:
			print("error")
			active = False
	print(f"You ({str(deck.getprintedtotal(player_cards)).replace('[', '').replace(']', '')}):")
	for card in player_cards:
		print(card)
	print(f"\nDealer ({str(deck.getprintedtotal(dealer_cards)).replace('[', '').replace(']', '')}):")
	for card in dealer_cards:
		print(card)
	choice = input('\nSay "hit" or "stand": ')
	while choice == "hit":
		logging.debug("User chose hit.")
		card = cur_deck.pop()
		player_cards.append(card)
		logging.debug(f"Drawn card: {card}")
		if logic.result(player_cards, dealer_cards) == "bust":
			logging.info("User went over 21. Bust.")
			print("\nyou busted")
			choice = "stand"
		else:
			print("--------------------")
			print(f"You ({str(deck.getprintedtotal(player_cards)).replace('[', '').replace(']', '')}):")
			for card in player_cards:
				print(card)
			print(f"\nDealer ({str(deck.getprintedtotal(dealer_cards)).replace('[', '').replace(']', '')}):")
			for card in dealer_cards:
				print(card)
			choice = input('\nSay "hit" or "stand": ')
	if choice == "stand":
		logging.info("User stood. Calculating result...")
		dealer_total = deck.gettotal(dealer_cards)
		if type(dealer_total) == list:
			while (dealer_total[0] < 17 or dealer_total[1] < 17):
				logging.debug("Dealer hit.")
				card = cur_deck.pop()
				dealer_cards.append(card)
				logging.debug(f"Drawn card: {card}")
				dealer_total = deck.gettotal(dealer_cards)
		else:
			while dealer_total < 17:
				logging.debug("Dealer hit.")
				card = cur_deck.pop()
				dealer_cards.append(card)
				logging.debug(f"Drawn card: {card}")
				dealer_total = deck.gettotal(dealer_cards)
				if type(dealer_total) == list:
					break
		game_result = logic.result(player_cards, dealer_cards, True)
		if game_result == "win":
			logging.info("User won.")
			print("--------------------")
			print("You won!")
			print(f"\nYou ({str(deck.getprintedtotal(player_cards, True)).replace('[', '').replace(']', '')}):")
			for card in player_cards:
				print(card)
			print(f"\nDealer ({str(deck.getprintedtotal(dealer_cards, True)).replace('[', '').replace(']', '')}):")
			for card in dealer_cards:
				print(card)
			userbalance = balance.add_balance("main", wager*payout)
			logging.debug(f"New Balance: {userbalance}")
		elif game_result == "loss":
			logging.info("User lost.")
			print("--------------------")
			print("You lost. Better luck next time.")
			print(f"\nYou ({str(deck.getprintedtotal(player_cards, True)).replace('[', '').replace(']', '')}):")
			for card in player_cards:
				print(card)
			print(f"\nDealer ({str(deck.getprintedtotal(dealer_cards, True)).replace('[', '').replace(']', '')}):")
			for card in dealer_cards:
				print(card)
		elif game_result == "push":
			print("--------------------")
			print("You tied, push.")
			print(f"\nYou ({str(deck.getprintedtotal(player_cards, True)).replace('[', '').replace(']', '')}):")
			for card in player_cards:
				print(card)
			print(f"\nDealer ({str(deck.getprintedtotal(dealer_cards, True)).replace('[', '').replace(']', '')}):")
			for card in dealer_cards:
				print(card)
			userbalance = balance.add_balance("main", wager)
		else:
			logging.error("Failed to calculate winner.")
			print("error")
			active = False
			break
	else:
		logging.error("Failed to calculate winner.")
		print("error")
		active = False
		break