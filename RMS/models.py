from otree.api import (
	models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
	Currency as c, currency_range
)

# to import the randomizer
import random
# to use decimals
import decimal
# to round up
from math import ceil



author = 'Mikhail Freer'

doc = """
Part of the experimental design for the Revealed Markov Strategies project.
Experiment for 2 person infinitely repeated prisoners dilemma.
"""


class Constants(BaseConstants):
	name_in_url = '2PPD'
	players_per_group = 2
	num_rounds = 10 # the total is 160 periods with random rematching at \delta = .8 (!!!)
	# set to 10 in the test mode, move to 160 in the real mode!

	delta = .8 # continuation probability (in the same matching)


class Subsession(BaseSubsession):
	match_number = models.IntegerField(initial=1) # counting the mathes (to compute the payoffs in the end)
	rematched = models.BooleanField(initial=0) # whether you are rematched
	random_number = models.FloatField() # to track the random number
	CC_payoff = models.IntegerField()
	DD_payoff = models.IntegerField()
	DC_payoff = models.IntegerField()
	CD_payoff = models.IntegerField()

	def before_session_starts(self):
		"""Initialize values at the start of the session"""
		# defining game structure
		if self.session.config['game_matrix'] == '2PPD':
			self.CC_payoff = 40  # payoff for each player if both cooperate
			self.DD_payoff = 25  # payoff to the palyer if both defect
			self.CD_payoff = 10  # payoff to (C,D) profile (to the player who cooperates)
			self.DC_payoff = 60  # payoff to (D,C) profile (to the player who defects)
		elif self.session.config['game_matrix'] == '2PCG':
			self.CC_payoff = 100  # payoff for each player if both cooperate
			self.DD_payoff = 60  # payoff to the palyer if both defect
			self.CD_payoff = 0  # payoff to (C,D) profile (to the player who cooperates)
			self.DC_payoff = 0  # payoff to (D,C) profile (to the player who defects)

class Group(BaseGroup):
	pass


class Player(BasePlayer):
	action = models.BooleanField() # action taken in the current round
	payoff_in_round = models.IntegerField(initial=0) #payoff received in the current round
	total_payoff = models.IntegerField(initial=0) #total payoff in the entire game


	#getting current partner
	def other_player(self):
		return self.get_others_in_group()[0]



	# setting the payoff earned in the current round
	def set_payoff_in_round(self):

		payoff_matrix = {
			1:
				{
					1: self.subsession.CC_payoff,
					0: self.subsession.CD_payoff
				},
			0:
				{
					1: self.subsession.DC_payoff,
					0: self.subsession.DD_payoff
				}
		}

		self.payoff_in_round = payoff_matrix[self.action][self.other_player().action]
		if self.subsession.round_number>1:
			self.total_payoff = self.in_round(self.subsession.round_number-1).total_payoff+self.payoff_in_round 
		else:
			self.total_payoff = self.payoff_in_round

		self.participant.payoff=c(5+ceil(4*self.total_payoff*.004)/4)







