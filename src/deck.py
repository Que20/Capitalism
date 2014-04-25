#Deck
from xmlCards import*
import random

class deck:
	def __init__(self, fileName):
		try:
			self.tmp = parseXML(fileName)
		except Exception as e:
			print(e)

	def load(self):
		self.deck = makeDeck(self.tmp)
		self.shuffleDeck()
	
	def pickUpCardFromDeck(self):
		if len(self.deck) > 0 :
			print("Card in deck : ", len(self.deck))
			return self.deck.pop()
		else :
			return None
		
	def shuffleDeck(self):
		random.shuffle(self.deck)
		pass
		
	def init(self, event_mouse, event_key, display_list):
		for card in self.deck:
			card.grap_card.init(event_mouse, event_key, display_list)
			card.grap_mincard.init(event_mouse, event_key, display_list)