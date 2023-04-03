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
import logic
#import packet

cur_deck = deck.new_deck(4)

active = True

difficulty = input("Select difficulty (easy, medium, hard): ")

if difficulty == "easy":
	payout = 2
elif difficulty == "medium":
	payout = 1.75
elif difficulty == "hard":
	payout = 1.5
else:
	payout = 1.5

userbalance = balance.create_balance("main", difficulty.lower())

wager = ""

while active:
	if userbalance <= 100:
		print("--------------------")
		print("\nyou lost all your money...")
		print("\ngambling is an addiction")
		print("get some help")
		break
	print("--------------------")
	print(f"Your balance: {userbalance}")

	wager = input(f"Table pays {payout}x\nSay amount to wager or 'q' to quit (Min bet: 100): ")
	while float(wager) < 100:
		wager = input("Below minimum bet.\nSay amount to wager or 'q' to quit (Min bet: 100): ")
	while not balance.has_wager("main", int(wager)):
		wager = input(f"You don't have enough money. Balance: {userbalance}\n\nSay amount to wager or 'q' to quit (Min bet: 100): ")

	if "q" in wager.lower():
		break
	else:
		wager = float(wager)
		
	userbalance = balance.remove_balance("main", wager)

	print("\nGood luck.")

	dealer_cards = []
	player_cards = []

	player_cards.append(cur_deck.pop())
	player_cards.append(cur_deck.pop())

	dealer_cards.append(cur_deck.pop())
	
	print("--------------------")
	result = logic.result(player_cards, dealer_cards)
	if "active" not in result:
		if "win" in result:
			print("--------------------")
			print("you won")
			print(f"\nYou ({deck.gettotal(player_cards)}):")
			for card in player_cards:
				print(card)
			print(f"\nDealer ({deck.gettotal(dealer_cards)}):")
			for card in dealer_cards:
				print(card)
			userbalance = balance.add_balance("main", wager*payout)
		elif "loss" in result:
			print("--------------------")
			print("you lost")
			print(f"\nYou ({deck.gettotal(player_cards)}):")
			for card in player_cards:
				print(card)
			print(f"\nDealer ({deck.gettotal(dealer_cards)}):")
			for card in dealer_cards:
				print(card)
		elif "push" in result:
			print("--------------------")
			print("you tied - push")
			print(f"\nYou ({deck.gettotal(player_cards)}):")
			for card in player_cards:
				print(card)
			print(f"\nDealer ({deck.gettotal(dealer_cards)}):")
			for card in dealer_cards:
				print(card)
			userbalance = balance.add_balance("main", wager*payout)
		else:
			print("error")
			active = False
	print(f"You ({deck.gettotal(player_cards)}):")
	for card in player_cards:
		print(card)
	print(f"\nDealer ({deck.gettotal(dealer_cards)}):")
	for card in dealer_cards:
		print(card)
	choice = input('\nSay "hit" or "stand": ')
	while choice == "hit":
		card = cur_deck.pop()
		player_cards.append(card)
		if logic.result(player_cards, dealer_cards) == "bust":
			print("\nyou busted")
			choice = "stand"
		else:
			print("--------------------")
			print(f"You ({deck.gettotal(player_cards)}):")
			for card in player_cards:
				print(card)
			print(f"\nDealer ({deck.gettotal(dealer_cards)}):")
			for card in dealer_cards:
				print(card)
			choice = input('\nSay "hit" or "stand": ')
	if choice == "stand":
		dealer_total = deck.gettotal(dealer_cards)
		while dealer_total < 17:
			card = cur_deck.pop()
			dealer_cards.append(card)
			dealer_total = deck.gettotal(dealer_cards)
		game_result = logic.result(player_cards, dealer_cards, True)
		if game_result == "win":
			print("--------------------")
			print("you won")
			print(f"\nYou ({deck.gettotal(player_cards)}):")
			for card in player_cards:
				print(card)
			print(f"\nDealer ({deck.gettotal(dealer_cards)}):")
			for card in dealer_cards:
				print(card)
			userbalance = balance.add_balance("main", wager*payout)
		elif game_result == "loss":
			print("--------------------")
			print("you lost")
			print(f"\nYou ({deck.gettotal(player_cards)}):")
			for card in player_cards:
				print(card)
			print(f"\nDealer ({deck.gettotal(dealer_cards)}):")
			for card in dealer_cards:
				print(card)
		elif game_result == "push":
			print("--------------------")
			print("you tied - push")
			print(f"\nYou ({deck.gettotal(player_cards)}):")
			for card in player_cards:
				print(card)
			print(f"\nDealer ({deck.gettotal(dealer_cards)}):")
			for card in dealer_cards:
				print(card)
			userbalance = balance.add_balance("main", wager)
		else:
			print("error")
	else:
		print("error")
		active = False