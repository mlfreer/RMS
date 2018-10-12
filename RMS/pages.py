from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants

import random 



class Welcome(Page):
	def is_displayed(self):
		return self.round_number == 1
	def vars_for_template(self):
		return { 
		'prob' : Constants.delta*100,
		'rounds': Constants.num_rounds,
		'CC_payoff': self.subsession.CC_payoff,
		'DC_payoff': self.subsession.DC_payoff,
		'CD_payoff': self.subsession.CD_payoff,
		'DD_payoff': self.subsession.DD_payoff
		}

#class necessary to determine whether you are rematched
class ShuffleWaitPage(WaitPage):
	wait_for_all_groups = True

	def after_all_players_arrive(self):
		if self.subsession.round_number>1:
			self.subsession.match_number = self.subsession.in_round(self.subsession.round_number-1).match_number

	#checking whether to continue with the same person or not
			r = random.uniform(0,1)
			self.subsession.random_number = r
	# shuffling upon the rnadom number exceeding the continuation probability
			if r> Constants.delta:
				self.subsession.group_randomly(fixed_id_in_group=True) # shuffle groups
				self.subsession.match_number = self.subsession.match_number+1 # increase the match number in the next period
				self.subsession.rematched = True # indicate that players will be rematched






class Decision(Page):
	form_model = 'player'
	form_fields = ['action']

	def vars_for_template(self):
		me = self.player
		return {
			'rematched': me.subsession.rematched,
			'continue': me.subsession.round_number>1,
			'round_number': me.subsession.round_number,
			'CC_payoff': self.subsession.CC_payoff,
			'DC_payoff': self.subsession.DC_payoff,
			'CD_payoff': self.subsession.CD_payoff,
			'DD_payoff': self.subsession.DD_payoff
		}


class ResultsWaitPage(WaitPage):

	def after_all_players_arrive(self):
		for p in self.group.get_players():
			p.set_payoff_in_round()


class Results(Page):
	def vars_for_template(self):
		me = self.player
		opponent = me.other_player()
		return {
			'my_decision': me.action,
			'opponent_decision': opponent.action,
			'same_choice': me.action == opponent.action,
		}


class FinalResults(Page):
	def is_displayed(self):
		return self.round_number == Constants.num_rounds


page_sequence = [
	Welcome,
	ShuffleWaitPage,
	Decision,
	ResultsWaitPage,
	Results,
	FinalResults

]
