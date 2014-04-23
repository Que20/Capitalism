from cap_graph import *
from card_type import *

# === Classes === #

class Effect:
	"""Classe représentant un effet"""

	# Constructeur
	def __init__(self, value, modifierType, affectedValue):
		self.value = value                   # Valeur de la modification
		self.modifierType = modifierType     # Type du modifieur (ModifierType)
		self.affectedValue = affectedValue   # Valeur affectée par l'effet (AffectableValue)

# Carte de type action (Event / Action)
class Action:
	"""Classe représentant une carte action"""

	# Constructeur
	def __init__(self, id, name, colorname, image, desc, type, life, affectedType, effects, deploymentCost):
		self.id = id                                          # ID unique de la carte
		self.cardType = Type.ACTION                           # type Action
		self.name = name                                      # Nom de la carte
		self.colorname = colorname                            # Couleur name
		self.desc = desc                                      # Description catre
		self.type = type                                      # Type de la carte (ActionType)
		self.life = life                                      # Durée de vie de la carte ( -1 = infinie )
		self.affectedType = affectedType                      # Type affecté (CardType)
		self.effects = effects                                # Tableau d'effets (Effect[])
		self.grap_card = cap_Graph_card(image, self)          # Image de la carte
		self.grap_mincard = cap_Graph_mincard(image, self)    # Miniature de l'image de la carte

	# Tour suivant
	def nextTurn(self):
		self.life = self.life - 1;

	# Si la carte à de la vie
	def isAlive(self):
		return (self.life > 0)

# Carte de valeur calculé
class CardData:
	"""Classe représentant les valeurs calculée pour une carte"""
	def __init__(self, deploymentCost=0, costPerTurn=0, costPerTurnModifier=0, incomePerTurn=0, incomePerTurnModifier=0, discardCost=0, life=0, cardData=None):
		if cardData :
			self.reset(cardData)                 
		else :
			self.deploymentCost = deploymentCost                     # Cout de pose calculé
			self.costPerTurn = costPerTurn                           # Coût par tour de la carte calculé
			self.costPerTurnModifier = costPerTurnModifier           # Modificateur du coût par tours calculé
			self.incomePerTurn = incomePerTurn                       # Revenus par tours calculé                
			self.incomePerTurnModifier = incomePerTurnModifier       # Modificateur des revenus par tours calculé
			self.discardCost = discardCost                           # Coût de retrait calculé
			self.life = life                                         # Durée de vie de la carte

	def reset(self, cardData):
		self.deploymentCost = cardData.deploymentCost
		self.costPerTurn = cardData.costPerTurn
		self.costPerTurnModifier = cardData.costPerTurnModifier
		self.incomePerTurn = cardData.incomePerTurn
		self.incomePerTurnModifier = cardData.incomePerTurnModifier
		self.discardCost = cardData.discardCost
		self.life = cardData.life

# Carte du jeu
class Card:
	"""Classe représentant une carte du jeu"""
	def __init__(self, id, name, colorname, image, desc, type, cardData, effects, affectedType):
		self.id = id                                          # ID unique de la carte
		self.cardType = Type.CARD                             # type de la carte (Type)
		self.name = name                                      # Nom de la carte
		self.colorname = colorname                            # couleur nom
		self.desc = desc                                      # Description catre
		self.type = type                                      # Type de la carte (CardType)
		self.cardData = cardData                              # Données de la carte
		self.effects = effects                                # Tableau d'effets (Effect[])
		self.affectedType = affectedType                      # Type affecté (CardType)
		self.computedCard = CardData(cardData=self.cardData)  # Données calculé de la carte
		self.actions = []                                     # Cartes actions affectées sur cette carte
		self.grap_card = cap_Graph_card(image, self)          # Image de la carte
		self.grap_mincard = cap_Graph_mincard(image, self)    # Miniature de l'image de la carte

	# Ajout d'une carte action
	def addActionCard(self, actionCard):
		# Ajout et màj valeurs
		self.actions.append(actionCard)
		computeEffects(actionCard)

	# Si cette carte est affectée par celle-ci
	def isAffectedBy(self, actionCard):
		return (actionCard.affectedType == self.type)

	# Remet les effets de la carte à zéro
	def resetEffects(self):
		self.computedCard.reset(self.cardData)
		# Pour chaque carte action liée
		for card in self.actions :
			computeEffects(card)

	# Calcul les effets d'une carte sur notre carte
	def computeEffects(self, actionCard):
		if self.isAffectedBy(actionCard):
			# Pour chaque effect de la carte
			for effect in actionCard.effects :
				if effect.affectedValue == AffectableValue.COST_PER_TURN :
	 				self.computedCard.costPerTurn = modifierType.computeModifiedValue(self.computedCard.costPerTurn, effect.value, effect.modifierType)
				elif effect.affectedValue == AffectableValue.COST_PER_TURN_MODIFIER :
	 				self.computedCard.costPerTurnModifier = modifierType.computeModifiedValue(self.computedCard.costPerTurnModifier, effect.value, effect.modifierType)
				elif effect.affectedValue == AffectableValue.INCOME_PER_TURN :
					self.computedCard.incomePerTurn = modifierType.computeModifiedValue(self.computedCard.incomePerTurn, effect.value, effect.modifierType)
				elif effect.affectedValue == AffectableValue.INCOME_PER_TURN_MODIFIER :
					self.computedCard.incomePerTurnModifier = modifierType.computeModifiedValue(self.computedCard.incomePerTurnModifier, effect.value, effect.modifierType)
				elif effect.affectedValue == AffectableValue.DISCARD_COST :
					self.computedCard.discardCost = modifierType.computeModifiedValue(self.computedCard.discardCost, effect.value, effect.modifierType)
				elif effect.affectedValue == AffectableValue.LIFE :
					self.computedCard.life = modifierType.computeModifiedValue(self.computedCard.life, effect.value, effect.modifierType)

	# Passe un tour sur notre carte
	def nexTurn(self):
		# Revenus du tour
		income = self.computedCard.incomePerTurn - self.computedCard.costPerTurn
		# Modification des coût par tours
		self.cardData.costPerTurn = self.computedCard.costPerTurnModifier * self.cardData.costPerTurn
		# Modification des revenus par tours
		self.cardData.incomePerTurn = self.computedCard.incomePerTurnModifier * self.cardData.incomePerTurn
		# Vie --
		self.cardData.life = self.cardData.life - 1;
		for card in self.actions :
			card.life = card.life - 1;
			# Si plus de vie, suppression
			if card.life < 0 :
				self.actions.remove(card)
		# Remise à zéro des effets
		self.resetEffects()

		return income # On retourne ce que la carte fait gagner / perdre comme argent

	# Si la carte à de la vie
	def isAlive(self):
		return (self.life > 0)
