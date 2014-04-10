import xml.etree.ElementTree as et
import card as c

# Parsage du fichier XML fournis en paramètre
def parseXML(filename) :
	xmlFile = et.parse(filename)
	root = xmlFile.getroot()
	cards = []
	for child in root:
		#print("\t"+child.tag)
		cardDict = {}
		for card in child :
			#print("\t\t"+card.tag+" : "+str(card.text))
			cardDict[card.tag] = str(card.text)
			if card.tag == "cardData" :
				cardData = {}
				for data in card :
					#print("\t\t\t"+data.tag+" : "+str(data.text))
					cardData[data.tag] = str(data.text)
				cardDict[card.tag] = cardData
			if card.tag == "effects" :
				cardEffects = []
				for effect in card :
					for eff in effect :
						anEffect = {}
						#print("\t\t\t"+eff.tag+" : "+str(eff.text))
						anEffect[eff.tag] = str(eff.text)
						cardEffects.append(anEffect)
				cardDict[card.tag] = cardEffects
		cards.append(cardDict)
	return cards

# Fabrication d'un deck à partir de cartes parsés d'un fichier XML - Création des objets Card, Effect et CardData
def makeDeck(cards) :
	deck = []
	for card in cards :
		effects = []
		for effect in card['effects'] :
			effects.append(c.Effect(effect['value'], effect['modifierType'], effect['affectedValue']))
		if card['type'] == 1 :
			data = card['cardData']
			cardData = c.CardData(data['costPerTurn'], data['costPerTurnModifier'], data['incomePerTurn'], data['incomePerTurnModifier'], data['discardCost'], data['life'])
			deck.append(c.Card(card['id'], card['name'], card['desc'], cardData, effects, card['affectedType']))
		if card['type'] == 2 :
			dock.append(c.Action(card['id'], card['name'], card['desc'], card['type'], card['life'], card['affectedType'], effects))
	return deck

# Retourne une carte choisie au hasard sur un deck construit
def pickDeck(deck) :
	return choice(deck)

# Affiche une carte choisie au hasard sur le deck construit du fichier XML fournis en paramètre
print(pickDeck(makeDeck(parseXML("file.xml"))))
