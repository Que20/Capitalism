import card as card
from card_type import *
from cap_graph import *

# Actions possibles du joueur
class PlayerAction:
	PASS  = 1       # Passe le tour
	PLACE_CARD = 2  # Pose une nouvelle carte, action ou card
	REMOVE_CARD = 3 # Retire une carte posée
	GET_INFO = 4    # Information sur une de ses cartes

red = (150, 0, 0)
green = (0, 150, 0)

# === Classes === #

# Joueur
class Player:
	"""Représente un des deux joueurs"""

	# Constructeur
	def __init__(self, name, log, number, startingMoney=100000):
		self.name = name                                   # Nom du joueur
		self.money = startingMoney                         # Argent de départ
		self.deck = []                                     # Cartes en main
		self.gameboard = [[None, None, None, None], 
		                  [None, None, None, None], 
		                  [None, None, None, None], 
		                  [None, None, None, None]]        # Plateau du joueur
		self.deleted = []                                  # Cartes supprimées
		self.selected = None                               # Carte selectionnée 1 = hand / 2 = gameboard                   
		self.log = log                                     # Log
		self.cost = 100                                    # Coût de départ de l'entreprise

		if number == 1 :
			self.graph_player = cap_Graph_playerinfo(cap_Rect(44, 555, 0, 0), self)
			self.playing = True   
		else :
			self.graph_player = cap_Graph_playerinfo(cap_Rect(1035, 110, 0, 0), self)
			self.playing = False   

	# A virer
	def addCardDeck(self, card):
		if card != None :
			# Graphique
			if self.playing :
				card.grap_mincard.animate(len(self.deck)*145 + 60, 712, 750, True)
			else :
				card.grap_mincard.animate(len(self.deck)*145 + 60, 25, 750, True)
			card.grap_mincard.visibility(True)

			# Ajout carte
			self.deck.append(card)

	# A virer
	def addCardGameboard(self, card, line, pos):
		if card != None :
			if line >= 0 and line < 4 and self.gameboard[line][pos] == None :
				# Graphique
				card.grap_mincard.animate(line * 145 + 350, pos * 60 + 438, 500, 1)
				card.grap_mincard.visibility(True)

				self.gameboard[line][pos] = card


	def _shiftDeck(self, i):
		while i < len(self.deck) :
			self.deck[i].grap_mincard.animate((i)*145 + 60, 712, 500)
			i += 1


	# Interverti deux cartes du gameboard
	def _invertGameboardCards(self, x1, y1, x2, y2):
		# Graphique
		if self.gameboard[x1][y1] != None :
			self.gameboard[x1][y1].grap_mincard.animate(x2 * 145 + 350, y2 * 60 + 438, 200)
		if self.gameboard[x2][y2] != None :
			self.gameboard[x2][y2].grap_mincard.animate(x1 * 145 + 350, y1 * 60 + 438, 200)
		# Inversement
		self.gameboard[x1][y1], self.gameboard[x2][y2] = self.gameboard[x2][y2], self.gameboard[x1][y1]


	# Pose une carte event
	def _posEventCard(self, events, hand, other_player):
		if events[0] == None :
			if self.deck[hand].cardType == Type.ACTION and self.deck[hand].type == ActionType.EVENT :
				# On a le bon type
				if self.deck[hand].deploymentCost < self.money :

					# Cout de pose
					self.money = self.money - self.deck[hand].deploymentCost 

					# Graphique
					self.deck[hand].grap_mincard.animate(50, 107, 500)

					# Log
					self.log.log("["+self.name+"] Carte posée : "+self.deck[hand].name+" dans event", green)

					# On change de zone
					events[0] = self.deck.pop(hand)
					self._shiftDeck(hand)
					self.graph_player.update()

					# Update de toutes les cartes
					for line in self.gameboard:
						self.calculateLine(line, events)
					for card in self.deck:
						for event in events :
							if card.cardType == Type.CARD and event != None : 
								card.computeEffects(event)
								# Update visuel après le calcul
								card.grap_card.update()
								card.grap_mincard.update()

					if other_player != None :
						for line in other_player.gameboard: 
							other_player.calculateLine(line, events)
						for card in other_player.deck:
							for event in events :
								if card.cardType == Type.CARD and event != None : 
									card.computeEffects(event)
									# Update visuel après le calcul
									card.grap_card.update()
									card.grap_mincard.update()
				else :
					print("Erreur : pas assez d'argent pour poser la carte")
					self.log.msg("Impossible de poser la carte : pas assez d'argent")
					self.log.log("["+self.name+"] Action impossible : pas assez d'argent", red)
			else :
				print("Erreur : type interdit de carte")
				self.log.msg("Impossible de poser la carte : mauvais type de carte")
				self.log.log("["+self.name+"] Action impossible : mauvais type", red)
		else :
			self.log.msg("Impossible de poser la carte : carte event déjà posée")
			self.log.log("["+self.name+"] Action impossible : pas de place", red)
			print("Erreur : carte event déjà posée")


	# Ajouter une action à une carte
	def _addAction(self, x, y):
		hand = self.deck[self.selected[1]]
		self.money = self.money - hand.deploymentCost # Coût de pose
		self.graph_player.update()
		# Glisse la carte sur la carte de type produit (erreur si pas produit)
		hand.grap_mincard.animate(x * 145 + 350, y * 60 + 438, 500, -1)
		# Shift du deck
		self.gameboard[x][y].actions.append(self.deck.pop(self.selected[1]))
		self._shiftDeck(self.selected[1])
		# Màj données carte
		self.gameboard[x][y].computeEffects(self.gameboard[x][y].actions[-1])
		# MàJ graphique de la carte
		self.gameboard[x][y].grap_card.update()
		self.gameboard[x][y].grap_mincard.update()


	# Pose la carte de la main dans le gameboard
	def _poseCard(self, events, hand, x, y):
		if self.deck[hand].cardType == Type.CARD :
			if self.gameboard[x][y] == None :
				if self.deck[hand].computedCard.deploymentCost < self.money :
					self.money = self.money - self.deck[hand].computedCard.deploymentCost # Cout de pose
					# Graphique
					self.deck[hand].grap_mincard.animate(x * 145 + 350, y * 60 + 438, 500)
					# On change de zone
					self.gameboard[x][y] = self.deck.pop(hand)
					self._shiftDeck(hand)
					self.graph_player.update()
					# Màj ligne
					self.calculateLine(self.gameboard[x], events)
					self.log.log("["+self.name+"] Carte posée : "+self.gameboard[x][y].name+" sur le board", green)
				else :
					self.log.msg("Impossible de poser la carte : pas assez d'argent")
					self.log.log("["+self.name+"] Action impossible : fond insuffisant", red)
					print("Erreur : pas assez d'argent pour poser la carte")
			else :
				self.log.msg("Impossible de poser la carte : case déjà occupée")
				self.log.log("["+self.name+"] Action impossible : case occupée", red)
				print("Erreur : case déjà occupée")
		elif self.deck[hand].type == ActionType.ACTION :
			if self.gameboard[x][y] != None :
				if self.deck[hand].affectedType == self.gameboard[x][y].type :
					if self.deck[hand].deploymentCost < self.money :
						self._addAction(x, y)
						self.log.log("["+self.name+"] Carte action posée : "+self.gameboard[x][y].actions[-1].name+" sur carte produit : "+self.gameboard[x][y].name, green)
					else :
						self.log.msg("Impossible de poser la carte : pas assez d'argent")
						self.log.log("["+self.name+"] Action impossible : fond insuffisant", red)
						print("Erreur : pas assez d'argent pour poser la carte")				
				else :
					self.log.msg("Impossible de poser la carte : type non-affecté")
					self.log.log("["+self.name+"] Action impossible : type non-affecté", red)
					print("Erreur : type non-affecté")
			else :
				self.log.msg("Impossible de poser la carte : case vide")
				self.log.log("["+self.name+"] Action impossible : case vide", (128, 0, 0))
				print("Erreur : impossible de poser une carte action sur une case vide")
		else :
			self.log.msg("Impossible de poser la carte : event interdit")
			self.log.log("["+self.name+"] Action impossible : event interdit", red)
			print("Erreur : impossible de placer des events ici")


	# Défausse le carte de la main
	def _discardHand(self, hand):
		# Log
		self.log.log("["+self.name+"] Carte défaussée : "+self.deck[hand].name+" depuis la main", green)
		# Graphique
		self.deck[hand].grap_mincard.animate(1087, 602, 750, -1)
		# On change de zone
		self.deleted.append(self.deck.pop(hand))
		# On déplace toutes les cartes après
		self._shiftDeck(hand)


	# Défausse le carte de la main
	def _discardGameboard(self, x, y):
		print(self.gameboard[x][y].name)
		if self.gameboard[x][y].computedCard.discardCost < self.money :
			self.money = self.money - self.gameboard[x][y].computedCard.discardCost # Coût défaussement
			self.graph_player.update()
			# Graphique
			self.gameboard[x][y].grap_mincard.animate(1087, 602, 750, -1)
			# Log
			self.log.log("["+self.name+"] Carte défaussée : "+self.gameboard[x][y].name+" depuis le board", green)

			# On change de zone
			self.deleted.append(self.gameboard[x][y])
			self.gameboard[x][y] = None
		else :
			self.log.msg("Impossible de supprimer la carte : pas assez d'argent")
			self.log.log("["+self.name+"] Action impossible : pas assez d'argent", red)
			print("Erreur : pas assez d'argent pour supprimer la carte")


	# Combien a le joueur ?
	def getMoney(self):
		return self.money


	# Action du joueur, retourne la carte affectée ou None si impossible
	def playerAction(self, action, events, other_player):
		if len(action) > 1 :
			# Si l'action se passe chez nous
			if self.playing and action[0] == "low" :

				# Selection d'une carte de jeu
				if action[1] == "gameboard" :

					# Si on a selectionné aucune carte, on selectione
					if self.selected == None :
						if self.gameboard[action[2]][action[3]] != None :
							self.selected = (2, action[2], action[3])
							return

					# Sinon on doit poser la carte de la main selectionnée
					elif self.selected[0] == 1 :
						self._poseCard(events, self.selected[1], action[2], action[3])

					# On échange les deux cartes de la même colonne
					elif self.selected[0] == 2 and self.selected[1] == action[2] :
						self._invertGameboardCards(action[2], action[3], self.selected[1], self.selected[2])

				# Selection d'une carte de la main
				elif action[1] == "hand" :
					# Si on a selectionné aucune carte, on selectione
					if self.selected == None and action[2] < len(self.deck) :
						self.selected = (1, action[2])
						return

				# Selection du deck de defaussement
				elif action[1] == "deck" :
					if self.selected != None :
						# On détruit une carte de la main
						if self.selected[0] == 1 :
							self._discardHand(self.selected[1])
						# On détuire une carte du gameboard
						elif self.selected[0] == 2 :
							self._discardGameboard(self.selected[1], self.selected[2])

			# Dans la zone adverse
			elif action[0] == "up" :
				# On clique sur les events
				if action[1] == "event" :
					# Si on a selectionné une carte de la main
					if self.selected != None and self.selected[0] == 1 :
						self._posEventCard(events, self.selected[1], other_player)


		self.selected = None


	# Calcul les effets pour une ligne du gameboard
	def calculateLine(self, line, events):

		# Reset des données
		for card in line :
			if card != None : card.resetEffects()

		# Calcul
		for card in line :
			if card != None :
				# Si on a des effets sur la carte
				if len(card.effects) > 0 :
					print("La carte "+card.name+" a des effets sur "+CardType.get_string(card.affectedType))
					# Pour chaque carte
					for other_card in line :
						if other_card != None :
							# Différente de card & affectée
							if other_card != card and card.affectedType == other_card.type :
								other_card.computeEffects(card)

				# Calcul avec les cartes event
				for event in events :
					if event != None :
						card.computeEffects(event)

		# Update visuel après le calcul
		for card in line :
			if card != None : 
				card.grap_card.update()
				card.grap_mincard.update()


	def getNextIncome(self):

		total = 0

		for line in self.gameboard:
			i = 0
			# Calcul des revenus et suppresion si carte trop ancienne
			for card in line:
				i = i + 1
				if card != None :
					total += card.nexTurn()

					# Si la carte n'a plus de vie après le tour
					if not card.isAlive() :
						self.deleted.append(line.pop(i)) # On met dans la liste deleted
						# Graphique
						self.gameboard[x][y].grap_mincard.animate(1087, 602, 750, -1)
						# Log
						self.log.log("["+self.name+"] Fin de vie : "+self.gameboard[x][y].name+" depuis le board")

		return total


	# Débute un tour
	def startTurn(self, deck):
		# Graphique, changement de cartes dans tout les sens
		j = 0
		for line in self.gameboard :
			i = 0
			for card in line :
				if card != None :
					card.grap_mincard.animate(j*145 + 350, i*60 + 438, 300)
					i += 1
			j += 1

		for card in self.deck :
			card.grap_mincard.animate(card.grap_mincard.rect.x, 712, 300)

		self.playing = True

		# On pioche une carte
		card = deck.pickUpCardFromDeck()
		# Log
		self.log.log("["+self.name+"] Pioche : "+card.name)
		self.addCardDeck(card)

		self.graph_player.rect.x = 1035
		self.graph_player.rect.y = 110


	# Termine un tour
	def endTurn(self, events):

		if len(self.deck) < 8:

			# récupération des revenus
			total = self.getNextIncome()

			# Log
			self.log.log("["+self.name+"] Coût entreprise ce tour : "+str(self.cost)+"$")
			self.log.log("["+self.name+"] Revenus du tour : "+str(total)+"$")
			
			# Coût total
			self.money += total - self.cost
			self.cost *= 2

			# Graphique, changement de cartes dans tout les sens
			j = 0
			for line in self.gameboard:
				i = 3
				for card in line :
					if card != None :
						card.grap_mincard.animate(j*145 + 350, i*60 + 120, 300)
						i -= 1
				j += 1

			i = 0
			for card in self.deck :
				card.grap_mincard.animate(i*145 + 60, 25, 300)
				i += 1

			self.graph_player.update()

			# Màj des cartes
			for line in self.gameboard:
				self.calculateLine(line, events)

			self.playing = False

			self.graph_player.rect.x = 44
			self.graph_player.rect.y = 555

			return True

		else:
			self.log.log("["+self.name+"] Impossible de finir le tour : trop de carte en main", red)
			self.log.msg("Impossible de finir le tour : trop de carte en main")

			return False


	