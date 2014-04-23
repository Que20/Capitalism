
# === Enumérations === #

class Type:
	CARD   = 1
	ACTION = 2

	def get_string(type):
		if type == Type.CARD :
			return "Carte"
		elif type == Type.ACTION :
			return "Action"
		else :
			return ""

# Type de carte possible
class CardType:
	PRODUCT  = 1    # Type produit
	CONTRACT = 2    # Type contrat
	EMPLOYEE = 3    # Type employé

	def get_string(type):
		if type == CardType.PRODUCT :
			return "Produit"
		elif type == CardType.CONTRACT :
			return "Contrat"
		elif type == CardType.EMPLOYEE :
			return "Employé"
		else :
			return ""

# Type de carte action possible
class ActionType:
	EVENT  = 1      # Type event, touche toutes les cartes
	ACTION = 2      # Type action, touche une seule carte

	def get_string(type):
		if type == ActionType.EVENT :
			return "Event"
		elif type == ActionType.ACTION :
			return "Action"
		else :
			return ""

# Type de valeur affectée possible
class AffectableValue:
	COST_PER_TURN             = 1     # Coût par tours
	COST_PER_TURN_MODIFIER    = 2     # Modificateur du coût par tours
	INCOME_PER_TURN           = 3     # Revenus par tours
	INCOME_PER_TURN_MODIFIER  = 4     # Modificateur des revenus par tours
	DISCARD_COST              = 5     # Coût de suppresion
	LIFE                      = 6     # Durée de vie de la carte

	def get_string(type):
		if type == AffectableValue.COST_PER_TURN :
			return "Coût par tours"
		elif type == AffectableValue.COST_PER_TURN_MODIFIER :
			return "Modif. coût par tours"
		elif type == AffectableValue.INCOME_PER_TURN :
			return "Revenus par tours"
		elif type == AffectableValue.INCOME_PER_TURN_MODIFIER :
			return "Modif. revenus par tours"
		elif type == AffectableValue.DISCARD_COST :
			return "Coût de défaussement"
		elif type == AffectableValue.LIFE :
			return "Durée de vie"
		else :
			return ""

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
