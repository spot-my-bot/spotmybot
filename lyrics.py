from bs4 import BeautifulSoup
import urllib
import requests
import sys
import re

def get_lyrics(artist, song):
	functions = [get_lyrics_genius, get_lyrics_songlyrics]
	lyrics = ""
	proxy = urllib.getproxies()

	for f in functions:
		print("bla")
		lyrics = f(artist, song, proxy)
		if lyrics != "":
			break

	return lyrics.encode('utf-8')

def get_lyrics_songlyrics(artist, song, proxy):
	lyrics = ""
	try:
		url = "http://songlyrics.com/%s/%s-lyrics" % (artist.replace(" ", "-"), song.replace(" ", "-"))
		page = requests.get(url, proxies=proxy)
		parser = BeautifulSoup(page.text, 'html.parser')
		lyrics = parser.find(id='songLyricsDiv').get_text()
	except:
		lyrics = ""
	if "We do not have" in lyrics:
		lyrics = ""
	if "Sorry, we have no" in lyrics:
		lyrics = ""

	return lyrics

def get_lyrics_genius(artist, song, proxy):
	lyrics = ""
	try:
		search_url = "http://genius.com/search?q=%s %s" % (artist, song)
		results = requests.get(search_url, proxies=proxy)
		parser = BeautifulSoup(results.text, 'html.parser')
		url = str(parser).split('song_link" href="')[1].split('" title=')[0]
		page = requests.get(url, proxies=proxy)
		parser = BeautifulSoup(page.text, 'html.parser')
		lyrics = parser.find(attrs={'class': 'lyrics'}).get_text().strip()
		if artist.lower().replace(" ", "") not in parser.text.lower().replace(" ", ""):
			lyrics = ""
	except:
		lyrics = ""

	return lyrics

def get_artist_song(info_string):
	parts = info_string.split(" - ")
	artist = parts[0]
	song = re.sub(' \(.*?\)', '', parts[1], flags=re.DOTALL)
	return (artist, song)

if __name__ == "__main__":
	if len(sys.argv) < 3:
		print "Usage: python %s <artist> <song>" % sys.argv[0]
	else:
		print get_lyrics(sys.argv[1], sys.argv[2])