from bs4 import BeautifulSoup
import urllib
import sys

def get_lyrics(artist, song):
	functions = [get_lyrics_songlyrics, get_lyrics_musixmatch]
	lyrics = ""
	proxy = urllib.request.getproxies()

	for f in functions:
		lyrics = f(artist, song, proxy)
		if lyrics != "":
			break

	return lyrics

def get_lyrics_songlyrics(artist, song, proxy):
	lyrics = ""
	try:
		url = "http://songlyrics.com/%s/%s-lyrics" % (artist.replace(" ", "-"), song.replace(" ", "-"))
		page = requests.get(url, proxies=proxy)
		parser = BeautifulSoup(page.text, 'html.parser')
		lyrics = parser.find(id='songLyricsDiv').get_text()
	except Exception:
		lyrics = ""
	if "We do not have" in lyrics:
		lyrics = ""
	if "Sorry, we have no" in lyrics:
		lyrics = ""

	return lyrics

def get_lyrics_musixmatch(artist, song, proxy):
	lyrics = ""
	try:
		url_search = "http://musicmatch.com/search/%s %s" % (artist, song)
		results = requests.get(url_search, proxies = proxy)
		parser = BeautifulSoup(results.text, 'html.parser')
		urls = re.findall('"track_share_url":"(http[s?]://www\.musixmatch\.com/lyrics/.+?","', parser.text)
		page = requests.get(urls[0], proxies=proxy)
		parser = BeautifulSoup(page.text, 'html.parser')
		lyrics = soup.text.split('"body":"')[1].split('","language"')[0]
		lyrics = lyrics.replace("\\n", "\n")
		lyrics = lyrics.replace("\\", "")
	except Exception:
		lyrics = ""

	return lyrics

def get_artist_song(info_string):
	parts = info_string.split(" - ")
	artist = parts[0]
	song = re.sub(' \(.*?\)', '', parts[1], flags=re.DOTALL)
	return (artist, song)

if __name__ == "__main__":
	if len(sys.argv) < 3:
		print "Usage: python %s <artist> <song>"
	else:
		print get_lyrics(sys.argv[1], sys.argv[2])