# Secure Container

from Timer import timer

from DataGetter import get_data

DAY = 4

data = get_data(DAY)
p_min, p_max = [i for i in map(int, data.strip().split('-'))]

def check1(pwd):
	pwd = str(pwd)
	flag = 0
	x = len(pwd)
	for i in range(x-1):
		if pwd[i] == pwd[i+1]:
			flag += 1
		if pwd[i] > pwd[i+1]: 
			return False
	if flag:
		return True
	else:
		return False

def check2(pwd):
	pwd = str(pwd)
	flag = 0
	x = len(pwd)
	for i in range(x-1):
		if pwd[i] == pwd[i+1]:
			if 0 < i < x-2:
				if pwd[i] != pwd[i-1] and pwd[i+1] != pwd[i+2]:
					flag += 1
			elif i > 0:
				if pwd[i] != pwd[i-1]:
					flag += 1
			elif i < x-2:
				if pwd[i+1] != pwd[i+2]:
					flag += 1
		if pwd[i] > pwd[i+1]: 
			return False
	if flag:
		return True
	else:
		return False

def inc_pass(pwd):
	pwd += 1
	pwd = list(str(pwd))
	s = sorted(pwd)[::-1]
	prev_loc = len(pwd)
	for i in s:
		try:
			loc = pwd.index(i)
		except ValueError:
			pass
		pwd[loc:prev_loc] = [i] * (prev_loc - loc)
		prev_loc = loc
	p = pwd.copy()
	pwd = int(''.join(pwd))
	return pwd if len(set(p)) < len(p) else inc_pass(pwd)

@timer
def count_pos_pwds(p_min, p_max, mode):
	counter = 0
	if mode == 1: 
		check = check1
	else: 
		check = check2
	i = p_min
	while i in range(p_min, p_max+1):
		if check(i): counter += 1
		i = inc_pass(i)
	return counter

print(count_pos_pwds(p_min, p_max, 1))
print(count_pos_pwds(p_min, p_max, 2))
