from transitions import Machine


class Bot_transition(object):
    states = ['start', 'new',
              'big', 'little',
              'card', 'cash',
              'asked_for_payment_method_big',
              'asked_for_payment_method_little',
              'big_card', 'big_cash',
              'little_card', 'little_cash']

    def __init__(self):
        self.machine = Machine(model=self, states=Bot_transition.states, initial='start')

        self.machine.add_transition(trigger='big', source='start', dest='asked_for_payment_method_big')
        self.machine.add_transition(trigger='little', source='start', dest='asked_for_payment_method_little')
        self.machine.add_transition('card', 'asked_for_payment_method_big', 'big_card')
        self.machine.add_transition('cash', 'asked_for_payment_method_big', 'big_cash')
        self.machine.add_transition('card', 'asked_for_payment_method_little', 'little_card')
        self.machine.add_transition('cash', 'asked_for_payment_method_little', 'little_cash')

        self.machine.add_transition('new', '*', 'start')
