import json
from random import randint

def get_random_quote():
	quotes = json.loads(open('quotes.json').read())
	ind = randint(0, len(quotes))
	return quotes[ind]
