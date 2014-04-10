# === Enumérations === #

class Type:
	CARD   = 1
	ACTION = 2

# Type de carte possible
class CardType:
	PRODUCT  = 1    # Type produit
	CONTRACT = 2    # Type contrat
	EMPLOYEE = 3    # Type employé

# Type de carte action possible
class ActionType:
	EVENT  = 1      # Type event, touche toutes les cartes
	ACTION = 2      # Type action, touche une seule carte

# Type de valeur affectée possible
class AffectableValue:
	COST_PER_TURN             = 1     # Coût par tours
	COST_PER_TURN_MODIFIER    = 2     # Modificateur du coût par tours
	INCOME_PER_TURN           = 3     # Revenus par tours
	INCOME_PER_TURN_MODIFIER  = 4     # Modificateur des revenus par tours
	DISCARD_COST              = 5     # Coût de suppresion
	LIFE                      = 6     # Durée de vie de la carte

# Type de carte action possible
class ModifierType:
	PERCENT = 1       # Modificateur par pourcentage
	FIXED   = 2       # Modificateur fixe

	def computeModifiedValue(value, modifier, modifierType):
		if modifierType == ModifierType.PERCENT :
			return value * modifier
		elif modifierType == ModifierType.FIXED :
			return value + modifier
		else :
			return value


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
	def __init__(self, id, name, desc, type, life, affectedType, effects):
		self.id = id                         # ID unique de la carte
		self.actionType = Type.ACTION        # type Action
		self.name = name                     # Nom de la carte
		self.desc = desc                     # Description catre
		self.type = type                     # Type de la carte (ActionType)
		self.life = life                     # Durée de vie de la carte ( -1 = infinie )
		self.affectedType = affectedType     # Type affecté (CardType)
		self.effects = effects               # Tableau d'effets (Effect[])

	# Tour suivant
	def nextTurn(self):
		self.life = self.life - 1;

	# Si la carte à de la vie
	def isAlive(self):
		return (self.life > 0)

# Carte de valeur calculé
class CardData:
	"""Classe représentant les valeurs calculée pour une carte"""
	def __init__(self, costPerTurn, costPerTurnModifier, incomePerTurn, incomePerTurnModifier, discardCost, life, cardData=None):
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
	def __init__(self, id, cardType, name, desc, type, cardData, effects, affectedType):
		self.id = id                                          # ID unique de la carte
		self.cardType = Type.CARD                             # type de la carte (CardType)
		self.name = name                                      # Nom de la carte
		self.desc = desc                                      # Description catre
		self.type = type                                      # Type de la carte 
		self.cardData = cardData                              # Données de la carte
		self.effects = effects                                # Tableau d'effets (Effect[])
		self.affectedType = affectedType                      # Type affecté (CardType)
		self.computedCard = CardData(cardData=self.cardData)  # Données calculé de la carte

	# Si cette carte est affectée par celle-ci
	def isAffectedBy(self, actionCard):
		return (actionCard.affectedType == self.type)

	# Remet les effets de la carte à zéro
	def resetEffects(self):
		self.computedCard.reset(self.cardData)

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
		# Remise à zéro des effets
		self.resetEffects()

		return income # On retourne ce que la carte fait gagner / perdre comme argent

	# Si la carte à de la vie
	def isAlive(self):
		return (self.life > 0)

print("hello")