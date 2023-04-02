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
#import packet

cur_deck = deck.new_deck(4)

dealer_cards = []
player_cards = []

player_total = 0
dealer_total = 0

card = cur_deck.pop()
player_cards.append(card)
player_total += card.number

card = cur_deck.pop()
player_cards.append(card)
player_total += card.number

card = cur_deck.pop()
dealer_cards.append(card)
dealer_total += card.number

active = True

while active:
	result = deck.result(player_cards, dealer_cards)
	print(result)
	if "active" not in result:
		if "win" in result:
			print("you won")
			print(f"\nYou ({player_total}):")
			for card in player_cards:
				print(card)
			print(f"\nDealer ({dealer_total}):")
			for card in dealer_cards:
				print(card)
			active = False
		elif "loss" in result:
			print("you lost")
			print(f"\nYou ({player_total}):")
			for card in player_cards:
				print(card)
			print(f"\nDealer ({dealer_total}):")
			for card in dealer_cards:
				print(card)
			active = False
		elif "push" in result:
			print("you tied - push")
			print(f"\nYou ({player_total}):")
			for card in player_cards:
				print(card)
			print(f"\nDealer ({dealer_total}):")
			for card in dealer_cards:
				print(card)
		else:
			print("error")
			active = False
	print(f"\nYou ({player_total}):")
	for card in player_cards:
		print(card)
	print(f"\nDealer ({dealer_total}):")
	for card in dealer_cards:
		print(card)
	choice = input(f'\n\nSay "hit" or "stand": ')
	if choice == "hit":
		while choice == "hit":
			card = cur_deck.pop()
			player_cards.append(card)
			player_total += card.number
			print(f"You ({player_total}):")
			for card in player_cards:
				print(card)
			print(f"Dealer ({dealer_total}):")
			for card in dealer_cards:
				print(card)
			choice = input(f'\n\nSay "hit" or "stand": ')
	elif choice == "stand":
		for card in dealer_cards:
			dealer_total += card.number
		while dealer_total < 17:
			card = cur_deck.pop()
			dealer_cards.append(card)
			dealer_total += card.number
		gameresult = deck.result(player_cards, dealer_cards, True)
		if "win" in gameresult:
			print("\nyou won")
			print(f"\nYou ({player_total}):")
			for card in player_cards:
				print(card)
			print(f"\nDealer ({dealer_total}):")
			for card in dealer_cards:
				print(card)
			active = False
		elif "loss" in gameresult:
			print("\nyou lost")
			print(f"\nYou ({player_total}):")
			for card in player_cards:
				print(card)
			print(f"\nDealer ({dealer_total}):")
			for card in dealer_cards:
				print(card)
			active = False
		elif "push" in gameresult:
			print("you won")
			print(f"\nYou ({player_total}):")
			for card in player_cards:
				print(card)
			print(f"\nDealer ({dealer_total}):")
			for card in dealer_cards:
				print(card)
			active = False
		else:
			print("error")
			active = False