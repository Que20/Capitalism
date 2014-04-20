import card as card

# Actions possibles du joueur
class PlayerAction:
	PASS  = 1       # Passe le tour
	PLACE_CARD = 2  # Pose une nouvelle carte, action ou card
	REMOVE_CARD = 3 # Retire une carte posée
	GET_INFO = 4    # Information sur une de ses cartes


# === Classes === #

# Joueur
class Player:
	"""Représente un des deux joueurs"""

	# Constructeur
	def __init__(self, name, startingMoney=10000):
		self.name = name                                   # Nom du joueur
		self.money = startingMoney                         # Argent de départ
		self.deck = []                                     # Cartes en main
		self.gameboard = [[None, None, None, None], 
		                  [None, None, None, None], 
		                  [None, None, None, None], 
		                  [None, None, None, None]]        # Plateau du joueur
		self.deleted = []                                  # Cartes supprimées

	# Combien a le joueur ?
	def getMoney(self):
		return self.money

	# Débute un tour
	def startTurn(self, deck):
		# Pas besoin de recalculer, les calculs s'effectuent en fin de tour

		# On pioche une carte
		self.deck.append(choice(deck))

	# Action du joueur, retourne la carte affectée ou None si impossible
	def playerAction(self, action, cardNumber, events, line=-1, otherPlayer=None, card=None):
		try:
			# Placement de carte
			if action == PlayerAction.PLACE_CARD and card != None :
				# Placement sur le joueur adverse
				if otherPlayer != None :
					if card.type == Type.ACTION and otherPlayer.gameboard[line][cardNumber] != None :
						otherPlayer.gameboard[line][cardNumber].addActionCard(card)
						return otherPlayer.gameboard[line][cardNumber]
					else :
						return None
				# Placement sur son gameboard/event
				else :
					# Placement sur son terrain
					if cardNumber >= 0 :
						# Placement carte action
						if card.type == Type.ACTION :
							if self.gameboard[line][cardNumber] != None :
								self.gameboard[line][cardNumber].addActionCard(card)
								return self.gameboard[line][cardNumber]
							else :
								return None
						# carte normale
						else :
							if self.gameboard[line][cardNumber] == None :
								self.gameboard[line][cardNumber] = card
								# Calcul des nouveaux effets
								self.calculateLine(line, self.gameboard[line])
								return card
							else :
								return None
					# Carte event (prend effet au tour suivant)
					else :
						events.append(card)
			# Retirer une carte
			elif action == PlayerAction.REMOVE_CARD :
				return removeCard(line, cardNumber)
			# Retirer une carte
			elif action == PlayerAction.GET_INFO :
				# Carte d'un autre joueur (forcément sur sa board)
				if otherPlayer != None :
					return otherPlayer.gameboard[line][cardNumber]
				# Une carte à nous (ou event)
				else :
					# Une carte posée sur le gameboard
					if line >= 0 :
						return self.gameboard[line][cardNumber]
					# Une carte de notre main
					elif cardNumber >= 0 :
						return self.deck[cardNumber]
					# Une carte des events
					else :
						return events[-cardNumber]
			else :
				return None
		except Exception as e:
			return None

	# Supprime une carte, retourne la carte supprimée ou None si impossible
	def removeCard(self, line, cardNumber):
		try:
			if self.gameboard[line][cardNumber].computedCard.discardCost < self.money :
				self.money = self.money - self.gameboard[line][cardNumber].computedCard.discardCost
				return self.gameboard[line].pop(cardNumber)
			else :
				return None
		except Exception as e:
			return None

	# Calcul les effets pour une ligne du gameboard
	def calculateLine(self, line, events):
		for card in line :
			# Si on a des effets sur la carte
			if len(card.effects) > 0 :
				# Pour chaque carte
				for other_card in line :
					# Différente de card & affectée
					if other_card != card and card.affectedType == other_card.type :
						other_card.computeEffects(card)

			# Calcul avec les cartes event
			for event in events :
				card.computeEffects(event)

	# Termine un tour
	def endTurn(self, events):
		# récupération des revenus
		for line in self.gameboard:
			i = 0
			# Calcul des revenus et suppresion si carte trop ancienne
			for card in line:
				i = i + 1
				self.money += card.nexTurn()

				# Si la carte n'a plus de vie après le tour
				if card.isAlive() == 0 :
					self.deleted.append(line.pop(i)) # On met dans la liste deleted

			# Calcul des effet des cartes entres elles
			for card in line:
				self.calculateLine(line, events)

