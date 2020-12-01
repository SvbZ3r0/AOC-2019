import time
import queue
import operator
import logging
import functools

class IntcodeComputer:
	def __init__(self, instructions, propogative_feedback=False):
		self.orig_instructions = instructions
		self.instructions = self.orig_instructions.copy()
		self.intr_ptr = 0
		self.rel_base = 0
		self.memory = {
						'i': queue.Queue(),
						'o': queue.Queue()
						}
		self.propogative_feedback = propogative_feedback
		self.is_running = True
		self.output = 0
		self.OPCODES = {
						'1': [3, lambda x,y: self._arith(operator.add, x, y)],
						'2': [3, lambda x,y: self._arith(operator.mul, x, y)],
						'3': [1, self._put_instruction],
						'4': [1, self._get_instruction],
						'5': [2, lambda x,y: self._jump(True, x, y)],
						'6': [2, lambda x,y: self._jump(False, x, y)],
						'7': [3, lambda x,y: self._arith(operator.lt, x, y)],
						'8': [3, lambda x,y: self._arith(operator.eq, x, y)],
						'9': [1, self._update_rel_base],
						'99': [1, self._quit]
						}
		self.verbose = True

	# parse opcode into modes and function
	def parse_opcode(self, code):
		opcode = code % 100
		n_para, func = self.OPCODES[str(opcode)]
		# print(code)
		modes = [int(i) for i in str(code)[:-2][::-1]]
		modes += '0' * (n_para - len(modes))
		# print(opcode, modes, func.__name__)
		# input()
		return opcode, modes, func

	# set instruction pointer to ptr_dest
	def set_intr_ptr(self, ptr_dest):
		if ptr_dest > len(self.instructions) or ptr_dest < 0:
			print('Stack Overflow: intr')
			exit(1)
		self.intr_ptr = ptr_dest

	# resets computer to fresh state
	def reset(self):
		self.instructions = self.orig_instructions.copy()
		self.intr_ptr = 0
		self.rel_base = 0
		self.is_running = True
		for channel in self.memory:
			self.clear_memory(channel)
		self.output = 0

	# retrieve instruction from index
	def retr_intr(self, index, orig=False):
		if orig:
			instructions = self.orig_instructions
		else:
			instructions = self.instructions
		return instructions[index]

	# change instruction at loc to val
	def overwrite_intr(self, val, loc):
		try:
			self.instructions[loc] = val
		except IndexError:
			self.instructions += [0] * (loc - len(self.instructions) + 1)
			self.instructions[loc] = val

	# add val to memory channel queue
	def set_memory(self, val, channel='i'):
		if channel == 'o':
			self.output = val
		if not isinstance(val, int):
			print('Value Error!')
			exit(1)
		self.memory[channel].put(val)

	# pop val from memory channel queue
	def retr_memory(self, channel='o'):
		try:
			val = self.memory[channel].get(self.propogative_feedback)
		except queue.Empty:
			print('Stack Underflow!')
			exit(1)
		return val

	# check if memory channel is empty
	def memory_empty(self, channel='o'):
		return self.memory[channel].empty()

	# clear memory channel
	def clear_memory(self, channel='o'):
		self.memory[channel] = queue.Queue()

	# perform arithmetic operations as defined by func on given pars
	def _arith(self, func, pars, loc):
		val = func(pars[0], pars[1])
		self.overwrite_intr(val, loc)
		if loc != self.intr_ptr:
			self.set_intr_ptr(self.intr_ptr + 4)

	def _put_instruction(self, pars, loc):
		val = self.retr_memory(channel='i')
		self.overwrite_intr(val, loc)
		if loc != self.intr_ptr:
			self.set_intr_ptr(self.intr_ptr + 2)

	def _get_instruction(self, pars, loc):
		self.set_memory(loc, channel='o')
		self.set_intr_ptr(self.intr_ptr + 2)

	def _jump(self, truth, pars, loc):
		truth_ = bool(pars[0]) == truth
		if truth_:
			self.set_intr_ptr(loc)
		else:
			self.set_intr_ptr(self.intr_ptr + 3)

	def _update_rel_base(self, pars, loc):
		self.rel_base += loc
		if loc != self.intr_ptr:
			self.set_intr_ptr(self.intr_ptr + 2)

	def _quit(self, *_):
		self.is_running = False

	def get_vals(self, opcode, modes):
		pars = self.instructions[self.intr_ptr+1:self.intr_ptr+len(modes)+1]
		if not pars:
			return None, None
		loc = pars[-1]
		for i, par in enumerate(pars):
			try:
				if int(modes[i]) == 0:
					val = self.instructions[par]
				elif int(modes[i]) == 1:
					val = par
				elif int(modes[i]) == 2:
					val = self.instructions[self.rel_base+par]
			except IndexError:
				val = 0
			pars[i] = val
		if opcode in [4, 5, 6, 9]:
			loc = pars[-1]
		elif modes[-1] == 2:
			loc += self.rel_base
		else:
			assert 'Something wrong'
		parameters = pars[:-1]
		return parameters, loc

	def compute(self):
		while self.is_running:
			opcode, modes, operation = self.parse_opcode(self.instructions[self.intr_ptr])
			pars, loc = self.get_vals(opcode, modes)
			operation(pars, loc)
		if self.verbose: print('Computation successful.')