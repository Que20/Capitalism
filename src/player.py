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
		self.selected = None                               # Carte selectionnée
		self.selected_zone = 0                             # Zone selectionnée
		self.playing = True

	def addCardDeck(self, card):
		if card != None :
			# Graphique
			card.grap_mincard.animate(len(self.deck)*145 + 60, 712, 2000, True)
			card.grap_mincard.visibility(True)

			# Ajout carte
			self.deck.append(card)

	def addCardGameboard(self, card, line, pos):
		if card != None :
			if line >= 0 and line < 4 and self.gameboard[line][pos] == None :
				# Graphique
				card.grap_mincard.animate(line * 145 + 350, pos * 60 + 438, 2000, True)
				card.grap_mincard.visibility(True)

				self.gameboard[line][pos] = card

	# Combien a le joueur ?
	def getMoney(self):
		return self.money

	# Débute un tour
	def startTurn(self, deck):
		# Pas besoin de recalculer, les calculs s'effectuent en fin de tour

		# On pioche une carte
		self.deck.append(choice(deck))

	# Action du joueur, retourne la carte affectée ou None si impossible
	def playerAction(self, action):
		if len(action) > 2 :
			# Si l'action se passe chez nous
			if self.playing and action[0] == "low" :
				# Selection d'une carte de jeu
				if action[1] == "gameboard" :
					# Si on a selectionné aucune carte, on selectione
					if self.selected == None :
						pass
					else :
						pass
				# Selection d'une carte de la main
				elif action[1] == "hand" :
					pass
				# Selection du deck de defaussement
				elif action[1] == "deck" :
					pass


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

