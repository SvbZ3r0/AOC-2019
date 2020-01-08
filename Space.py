
class SpaceObj():
	# todo ugly class variable. find a better way to do this.
	tmp_centre = None

	def __init__(self, name, parent=None):
		self.name = name
		self.set_parent(parent)
		self.children = {}

	def set_parent(self, parent):
		self.parent = parent
		if self.parent:
			# todo raise exception if object w/ name already exists
			self.parent.children[self.name] = self

	def has_child(self):
		if self.count_direct_children():
			return True
		return False

	# get total number of directly orbiting objects
	def count_direct_children(self):
		return len(self.children)

	# get total number of directly and indirectly orbiting objects
	def count_indirect_children(self):
		n_indirect_children = 0
		for child_name in self.children:
			n_indirect_children += self.children[child_name].count_indirect_children()
		return n_indirect_children + self.count_direct_children()

	# get orbiting object by name
	def get_child_by_name(self, child_name):
		try:
			return self.children[child_name]
		except KeyError:
			child = None
			for dir_child in self.children:
				child = self.children[dir_child].get_child_by_name(child_name)
				if child:
					return child
			return child

	# returns distance of object from spaceobj
	def get_dist_from(self, spaceobj, check_children = False):
		# distance from self is 0. edge case.
		if self == spaceobj:
			return 0
		if check_children:
			if self.get_child_by_name(spaceobj.name):
				return spaceobj.get_dist_from(self, check_children)
		# spaceobj hasn't been found up the chain
		if not self.parent:
			# todo handle this in a better way
			print('{} is not linked to {}.'.format(spaceobj.name, self.name))
			return -1
		# dist to spaceobj = dist of parent to spaceobj + 1
		elif self.parent != spaceobj:
			return self.parent.get_dist_from(spaceobj, check_children) + 1
		# immediate parent is spaceobj
		else:
			return 0
		print('{} is not linked to {}.'.format(spaceobj.name, self.name))
		return -1

	def orbit_count_checksum(self):
		# set tmp_centre to og calling object
		if not SpaceObj.tmp_centre:
			SpaceObj.tmp_centre = self

		chksm = 0
		for child_name in self.children:
			# if there's more down the line, get dist of each from og calling object
			if self.children[child_name].has_child():
				chksm += self.children[child_name].orbit_count_checksum()
				chksm += self.children[child_name].get_dist_from(SpaceObj.tmp_centre) + 1
			# if not, get dist of self and move to next child
			else:
				chksm += self.children[child_name].get_dist_from(SpaceObj.tmp_centre) + 1

		# reset tmp_centre
		if SpaceObj.tmp_centre == self:
			SpaceObj.tmp_centre = None
		return chksm 
