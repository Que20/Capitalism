import xml.etree.ElementTree as et
import card as c
import re

# Parsage du fichier XML fournis en paramètre
def parseXML(filename) :
	xmlFile = et.parse(filename)
	root = xmlFile.getroot()
	cards = []
	for child in root:
		#print("\t"+child.tag)
		cardDict = {}
		for card in child :
			# Nom
			if card.tag == "name" :
				cardDict["color"] = "black"

				for key,value in card.attrib.items():
					if key == "color" :
						cardDict["color"] = card.attrib["color"]

				cardDict[card.tag] = str(card.text).replace("\t", "")
			# Description et image
			elif card.tag == "description" or card.tag == "image" :
				#print("\t\t"+card.tag+" : "+str(card.text))
				cardDict[card.tag] = str(card.text).replace("\t", "")
			# CardData
			elif card.tag == "cardData" :
				cardData = {}
				for data in card :
					#print("\t\t\t"+data.tag+" : "+str(data.text))
					cardData[data.tag] = float(data.text)
				cardDict[card.tag] = cardData
			#Effects
			elif card.tag == "effects" :
				cardEffects = []
				for effect in card :
					anEffect = {}
					for eff in effect :
						#print("\t\t\t"+eff.tag+" : "+str(eff.text))
						anEffect[eff.tag] = float(eff.text)
					cardEffects.append(anEffect)
				cardDict[card.tag] = cardEffects
			# Autre
			else :
				#print("\t\t>"+card.tag+" : "+str(card.text))
				cardDict[card.tag] = float(card.text)
		cards.append(cardDict)
	return cards

# Fabrication d'un deck à partir de cartes parsés d'un fichier XML - Création des objets Card, Effect et CardData
def makeDeck(cards) :
	deck = []
	for card in cards :
		effects = []
		for effect in card['effects'] :
			effects.append(c.Effect(effect['value'], effect['modifierType'], effect['affectedValue']))
		if card['cardType'] == 1 :
			data = card['cardData']
			cardData = c.CardData(card['deploymentCost'], data['costPerTurn'], data['costPerTurnModifier'], data['incomePerTurn'], data['incomePerTurnModifier'], data['discardCost'], card['life'])
			deck.append(c.Card(card['id'], card['name'], card['color'], card['image'], card['description'], card['type'], cardData, effects, card['affectedType']))
		if card['cardType'] == 2 :
			deck.append(c.Action(card['id'], card['name'], card['color'], card['image'], card['description'], card['type'], card['life'], card['affectedType'], effects, card['deploymentCost']))
	return deck

# Retourne une carte choisie au hasard sur un deck construit
def pickDeck(deck) :
	return choice(deck)
