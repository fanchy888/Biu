class FSM(object):
	def __init__(self):
		self.states={}
		self.current_state=None
	def add_state(self, state):
		self.states[state.name]=state
	def think(self):
		if self.current_state is None:
			return
		self.current_state.run()
		next_state=self.current_state.check()
		if next_state is not None and self.current_state.name!=next_state:
			self.change_state(next_state)
	def change_state(self, next_state):
		if self.current_state is not None:
			self.current_state.stop()
		self.current_state=self.states[next_state]
		self.current_state.start()
		

class State():
	def __init__(self,name):
		self.name=name
	def start(self):
		pass
	def check(self):
		pass
	def stop(self):
		pass
	def run(self):
		pass
		
		

	
	