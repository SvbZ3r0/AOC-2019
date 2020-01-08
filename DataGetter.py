import os
import sys
import json
import requests
from bs4 import BeautifulSoup

cred_file = './creds/aoc_cookie.json'

def get_data(day, cred_file = cred_file):
	dat_file = './data/day {:02} dat.txt'.format(day)
	if os.path.isfile(dat_file):
		with open(dat_file, 'r') as f:
			dat = f.read()
	else:
		with open(cred_file, 'r') as f:
			creds = json.load(f)
		cookies = {'session': creds['github']}
		r = requests.get('https://adventofcode.com/2019/day/{}/input'.format(day), cookies=cookies)
		r.raise_for_status()
		soup = BeautifulSoup(r.text, "html.parser")
		dat = soup.get_text()
		with open(dat_file, 'w') as f:
			f.write(dat)
	return dat

if __name__ == '__main__':
	pass