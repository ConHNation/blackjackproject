# This module contains all the functions, data and classes related to cards and the dealing of the deck.

# requirements
from random import shuffle
import logging
import threading

# all possible cards
all_card_nums = [2, 3, 4, 5, 6, 7, 8, 9, 10, "J", "K", "Q", "A"]
all_card_types = ["♠", "♣", "♦", "♥"]

# Defines card class, which allows me to make the cards Python objects, which makes them easier to compare, print, and reduces errors.
class card:
	'''
  This is a Python class I made
	to simplify the evaluation, printing, and 
 	calculation of cards during games.

 	The __str__ function returns what should
	be printed when a deck.card object is printed.

 	The __init__ function defines the different parameters
	of a card class.

 	The __eq__ function allows multiple card objects to be 
	evaluated against each other or added up. 
 	'''
	# Sets the suit and number of the card
	def __init__(self, card_type, card_num):
		self.type = card_type
		self.number = card_num

	# Returns what should be shown when a card object is printed.
	def __str__(self):
		return f"{self.type} {self.number}"

	# Returns True if two cards are equal to each other
	def __eq__(self, other):
		if self.__class__ != other.__class__:
			return NotImplementedError
		return (self.number == other.number)

	# Another way of setting what should be shown when a
	# card object is printed.
	def __repr__(self):
		return f"{self.type} {self.number}"

# Calculates the total of a given hand.
def gettotal(hand):
	total1 = 0
	total2 = 0
	for x in hand:
		if type(x) != card:
			return TypeError(f"expected card object, not {type(x)}")
		elif x.number == "A":
			total2 = total1+1
			total1 += 11
		elif x.number in ["J", "K", "Q"]:
			total1 += 10
			if total2 > 0:
				total2 += 10
		elif type(x.number) != int:
			return TypeError(f"card number should be integer or face card, not {type(x.number)}.")
		elif x.number > 11:
			return Exception("stop cheating")
		else:
			total1 += x.number
			if total2 > 0:
				total2 += x.number
	if total2 > 0:
		return [total1, total2]
	else:
		return total1

# Gets the total of a hand that should be printed.
# Mostly used when aces appear.
def getprintedtotal(deck, finish = False):
	total1 = 0
	total2 = 0
	for x in deck:
		if type(x) != card:
			return TypeError(f"expected card object, not {type(x)}")
		elif x.number == "A":
			total2 = total1+1
			total1 += 11
		elif x.number in ["J", "K", "Q"]:
			total1 += 10
			if total2 > 0:
				total2 += 10
		elif type(x.number) != int:
			return TypeError(f"card number should be integer or face card, not {type(x.number)}.")
		elif x.number > 11:
			return Exception("stop cheating")
		else:
			total1 += x.number
			if total2 > 0:
				total2 += x.number
	if total2 > 0:
		if finish:
			if total1 == 21:
				return total1
			if total1 <= 21 and total2 < total1:
				return total1
			elif total2 <= 21 and total1 < total2:
				return total2
			else:
				return total2
		elif total1 == 21 and total1 > total2:
			return total1
		elif total1 > 21 and total2 < 21:
			return total2
		elif total2 > 21:
			return total1
		else:
			return [total1, total2]
	elif total1 > 21 and total2 != 0:
		return total2
	else:
		return total1

# Determines whether the game should use the +1 total or
# +11 total when an ace appears.
def getacetotal(total):
	if type(total) == int:
		return total
	elif type(total) == list:
		print(total)
		if (total[0] > 21) and (total[1] <= 21):
			logging.debug("1st total over 21, using 2nd total.")
			return total[1]
		elif (total[0] > 21) and (total[1] > 21):
			logging.debug("Both totals over 21, using 2nd total.")
			return total[1]
		else:
			return total[0]
	else:
		logging.error(f"The correct total to use could not be calculated with total {total}.")
		return Exception(f"The correct total to use could not be calculated with the total {total}")
		
# An error for when more than 8 decks are generated.
class TooManyDecksError(Exception):
  "Too many decks were requested."
  pass

# Generates a new deck by generating a card of each suit 
# and number and shuffling the result.
def new_deck(num):
	logging.info("Generating new deck...")
	if type(num) != int:
		logging.error("TypeError: new_deck function was given a non-integer but requires an integer.")
		raise TypeError("new_deck function was given a non-integer but requires an integer.")
		return None
	if int(num) > 8 or int(num) <= 0:
		return TooManyDecksError
	else:
		num = int(num)
		global all_card_types, all_card_nums
		deck = []
		for _ in range(num):
			for _ in range(4):
				for x in all_card_types:
					for y in all_card_nums:
						deck.append(card(x, y))
		shuffle(deck)
		logging.info("New deck has been generated successfully.")
		return deck