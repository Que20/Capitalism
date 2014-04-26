import pygame
from pygame.locals import *

from cap_graph import *
from deck import *
from player import *

class game_engine:

	class cap_clickDetector:

		def __init__(self):
			# Moitié haute
			self.up = cap_Rect(0, 0, 1280, 400)

			# Zone de carte haute
			self.up_hand = cap_Rect(60, 0, 1160, 86)

			# Gameboard haute
			self.up_gameboard = cap_Rect(350, 120, 580, 240)

			# Deck
			self.up_deck = cap_Rect(50, 188, 200, 143)

			# Event
			self.up_event = cap_Rect(50, 107, 145, 60)

			# Zone de carte basse
			self.low_hand = cap_Rect(60, 712, 1160, 88)

			# Gameboard basse
			self.low_gameboard = cap_Rect(350, 441, 580, 240)

			# Deck
			self.low_deck = cap_Rect(1037, 552, 200, 143)

		def get_zone(self, x, y):
			# Haut
			if self.up.isIn(x,y) :
				if self.up_hand.isIn(x, y) :				
					return ("up", "hand", int((x - self.up_hand.x) / 145))
				elif self.up_gameboard.isIn(x, y) :
					x = int((x - self.up_gameboard.x) / 145)
					y = int((y - self.up_gameboard.y) / 60)
					if x > 3 : x = 3
					if y > 3 : y = 3
					return ("up", "gameboard", x, 3 - y)
				elif self.up_deck.isIn(x, y) :
					return ("up", "deck")
				elif self.up_event.isIn(x, y) :
					return ("up", "event")
				else:
					return ("up")
			# Bas
			else :
				if self.low_hand.isIn(x, y) :				
					return ("low", "hand", int((x - self.low_hand.x) / 145))
				elif self.low_gameboard.isIn(x, y) :
					x = int((x - self.low_gameboard.x) / 145)
					y = int((y - self.low_gameboard.y) / 60)
					if x > 3 : x = 3
					if y > 3 : y = 3
					return ("low", "gameboard", x, y)
				elif self.low_deck.isIn(x, y) :
					return ("low", "deck")
				else :
					return ("low")

	def __init__(self):
		self.clicker_detector = self.cap_clickDetector()
		self.deck = deck("card/cards.xml")

	def new_game(self, player1_name, player2_name):

		# Fenêtre
		pygame.display.set_caption('Capitalism - Jeu')
		window = pygame.display.set_mode((1280, 800))

		# En attendant le load
		window.blit(background, (0,0))
		pygame.display.flip()

		# Chargement des cartes
		self.deck.load()

		events = [ None ]

		self.quit = False

		# Events
		event_mouse = []
		event_modal_mouse = []

		event_key   = []
		event_modal_key   = []

		display_list  = []


		# Chargement graphique du deck
		self.deck.init(event_mouse, event_key, display_list)

		# Zone de défaussement
		deck_defausse = cap_Graph_discard([])
		deck_defausse.init(event_mouse, event_key, display_list)
		deck_defausse.visibility(True)

		# Zone de pioche
		deck_deck = cap_Graph_deck(self.deck)
		deck_deck.init(event_mouse, event_key, display_list)
		deck_deck.visibility(True)

		# Log
		log = cap_Graph_msg()
		log.init(event_mouse, event_key, display_list)
		log.visibility(True)

		# Fenêtre modale
		modal = cap_graph_Modal()

		# Joueurs
		self.player1 = Player(player1_name, log, modal, 1)
		self.player1.graph_player.init(event_mouse, event_key, display_list)
		self.player1.graph_player.visibility(True)

		self.player2 = Player(player2_name, log, modal, 2)
		self.player2.graph_player.init(event_mouse, event_key, display_list)
		self.player2.graph_player.visibility(True)

		def yes_end():
			# Un peu bourrin mais ça marche
			self.new_game(self.player1.name, self.player2.name)
			self.quit = True

		def no_end():
			self.quit = True

		def yes_opa():

			tirage = random.randrange(0, 100)
			chance = (((self.player1.money / self.player2.money) / 2) - 0.5) * 100

			if tirage <= chance :
				self.player1.log.log("["+self.player1.name+"] OPA réussie !", green)

				modal.set_msg("Le joueur "+self.player1.name+" gagne la partie en achetant l'entreprise du\njoueur "+self.player2.name+" durant une OPA !\n\nVoulez-vous relancer une partie ?", yes_end, no_end, True)
			else :
				self.player1.graph_player.changeMoney(-(self.player1.money*0.25))
				self.player1.money *= 0.75
				self.player1.graph_player.update()
				self.player1.log.msg("Echec de votre OPA !")
				self.player1.log.log("["+self.player1.name+"] OPA raté : malus de "+('%.2f' % (self.player1.money*0.25))+"$", red)


		def no_opa():
			pass

		# Boutons
		def opa():
			self.player1.OPA(self.player2, yes_opa, no_opa)


		button_OPA = cap_graph_Button(cap_Rect(350,373,247,59), cap_Rect(22,7,199,38), opa_but, opa_but_hovered, opa_but, opa)
		button_OPA.init(event_mouse, event_key, display_list)
		button_OPA.visibility(True)

		def endturn():
			if self.player1.endTurn(events) :
				if self.player1.money <= 0 :
					self.player2.startTurn(self.deck)
					# Plus de sous, fin de la partie
					modal.set_msg("Le joueur "+self.player1.name+" est en banqueroute ("+('%.2f$' % self.player1.money)+") !\nLe joueur "+self.player2.name+" gagne la partie avec "+('%.2f$' % self.player2.money)+" !\n\nVoulez-vous relancer une partie ?", yes_end, no_end)
				else :
					self.player2.startTurn(self.deck)
					self.player1, self.player2 = self.player2, self.player1

		button_pass = cap_graph_Button(cap_Rect(720,373,247,59), cap_Rect(47,7,145,38), pass_turn_but, pass_turn_but_hovered, pass_turn_but, endturn)
		button_pass.init(event_mouse, event_key, display_list)
		button_pass.visibility(True)

		modal.init(event_modal_mouse, event_modal_key, display_list)

		# Cartes de départ
		for i in range(1, 3):
			self.player1.addCardDeck(self.deck.pickUpCardFromDeck())
			self.player2.addCardDeck(self.deck.pickUpCardFromDeck())
		# Carte en plus pour valoir la pioche du joueur 2
		self.player1.addCardDeck(self.deck.pickUpCardFromDeck())

		def yes():
			self.quit = True

		def no():
			pass

		# Boucle d'affichage / évenements
		while not self.quit :
			window.blit(background, (0,0))

			# Affichage des choses à afficher
			for clbk in display_list :
				clbk(window)

			# Refresh
			pygame.display.flip()

			# Events de la fenêtre
			for event in pygame.event.get():

				# Boutons fenêtre
				if event.type == QUIT:
					modal.set_msg("Êtes vous certain de vouloir quitter le jeu ?\nLa partie en cours sera perdue.", yes, no)

				# Modal
				if modal.visible :

					# Clavier
					if event.type == KEYDOWN:

						for clbk in event_modal_key :
							if clbk[2](event.type, event.key, 0, 0):
									break
					# Souris
					if event.type == MOUSEBUTTONDOWN or event.type == MOUSEBUTTONUP or event.type == MOUSEMOTION :

						for clbk in event_modal_mouse :
							# Si l'event se passe dans notre range
							if clbk[0] == event.type and ( not hasattr(event, 'button') or clbk[1] == event.button ) :
								if hasattr(event, 'button') :
									button = event.button
								else :
									button = 0
								if clbk[2](event.type, button, event.pos[0], event.pos[1]):
									break
				# Jeu
				else :

					# Clavier
					if event.type == KEYDOWN:
						if event.key == K_ESCAPE:
							modal.set_msg("Êtes vous certain de vouloir quitter le jeu ?\nLa partie en cours sera perdu.", yes, no)
						elif event.key == K_SPACE:
							endturn()
						elif event.key == K_p:
							self.player1.addCardDeck(self.deck.pickUpCardFromDeck())

					# Souris
					if event.type == MOUSEBUTTONDOWN or event.type == MOUSEBUTTONUP or event.type == MOUSEMOTION :

						if event.type == MOUSEBUTTONDOWN :
							print(self.clicker_detector.get_zone(event.pos[0], event.pos[1]))
							self.player1.playerAction(self.clicker_detector.get_zone(event.pos[0], event.pos[1]), events, self.player2)

						for clbk in event_mouse :
							# Si l'event se passe dans notre range
							if clbk[0] == event.type and ( not hasattr(event, 'button') or clbk[1] == event.button ) :
								if hasattr(event, 'button') :
									button = event.button
								else :
									button = 0
								if clbk[2](event.type, button, event.pos[0], event.pos[1]):
									break

			pass
