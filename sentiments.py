import urllib
import requests
import json
import sys

def analyze_sentiment(text):
	url = "http://text-processing.com/api/sentiment/"
	proxy = urllib.getproxies()
	data_text = requests.post(url, proxies=proxy, data={'text': text}).text

	# probabilities are in data["probability"][label]
	# label can be "neg", "neutral" or "pos"

	try:
		data = json.loads(data_text)
		#return data["label"]
		return data["probability"]["pos"]
	except ValueError:
		return None

if __name__ == '__main__':
	print analyze_sentiment(sys.argv[1])