import urllib
import requests
import json

def analyzeSentiments(text):
	url = "http://text-processing.com/api/sentiment/"
	proxy = urllib.getproxies()
	data_text = requests.get(url, proxies=proxy, params={'text': text}).text
	data = json.load(data_text)

	# probabilities are in data["probability"][label]
	# label can be "neg", "neutral" or "pos"

	return data["label"]