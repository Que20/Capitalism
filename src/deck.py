#Deck
from xmlCards import*
import random

class deck:
	def __init__(self, fileName):
		#try:
		self.deck = makeDeck(parseXML(fileName))
		self.shuffleDeck()
		#except Exception as e:
		#	print(e)
	
	def pickUpCardFromDeck(self):
		return deck.pop()
		
	def shuffleDeck(self):
		random.shuffle(self.deck)
		
	def init(self, event_mouse, event_key, display_list):
		for card in self.deck:
			card.grap_card.init(event_mouse, event_key, display_list)