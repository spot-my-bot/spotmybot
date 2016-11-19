import sys
import time
import telepot

# local modules
from messages import messages
import sentiments
import traceback
import spotify
import lyrics
import textanalysis
from luis_api import parseEntities
BOT_NAME = "SpotMyBot"
SENTIMENT_THRESHOLD = 0.2
SPEED_THRESHOLD = 15
MAX_FAILS = 5

chats = {}

def handle_message(msg):
	content_type, chat_type, chat_id = telepot.glance(msg)
	response = ""
	sentiment = None
	faster_than = None
	slower_than = None
	task = messages["not_understood"]

	if content_type == "text":
		try:
			message = msg["text"]
			print "Handling message: %s" % message

			if chat_id not in chats:
				chats[chat_id] = { "last_song": None }
				response = messages["introduction"]
				task = "info"

			if task != "info":
				tags = textanalysis.get_speech_tags(message)
				comparatives = tags["comparatives"]
				if len(comparatives) > 0:
					if "faster" in comparatives:
						faster_than = chats[chat_id]['last_song']['tempo']
						task = "improve_song"
						response = messages["faster"]
					if "slower" in comparatives:
						slower_than = chats[chat_id]['last_song']['tempo']
						task = "improve_song"
						response = messages["slower"]
				else:
					sentiment = sentiments.analyze_sentiment(message)
					if sentiment is None:
						response = messages["not_understood"]
					else:
						if sentiment > 0.6:
							response = messages["pos"]
						elif sentiment < 0.2:
							response = messages["neg"]
						else:
							response = messages["neutral"]
							sentiment = None

						task = "find_song"

			first_name = msg["from"]["first_name"]
			emotion=parseEntities(message, 'Emotion')
			
			response = response.replace("<NAME>", first_name)
			response = response.replace("<BOTNAME>", BOT_NAME)
			response = response.replace("<MOOD>", emotion)

			bot.sendMessage(chat_id, response)

			if task == "info":
				return

			search_terms = tags["nouns"]

			if len(search_terms) < 1 or task is "improve_song":
				if 'last_search_terms' in chats[chat_id]:
					search_terms = chats[chat_id]['last_search_terms']
				else:
					bot.sendMessage(chat_id, messages["not_found"])
					return
			if sentiment is None and 'last_sentiment' in chats[chat_id]:
				sentiment = chats[chat_id]['last_sentiment']

			song = find_song(search_terms, sentiment, faster_than, slower_than)
			if song:
				chats[chat_id]['last_search_terms'] = search_terms
				chats[chat_id]['last_song'] = song
				chats[chat_id]['last_sentiment'] = sentiment
				bot.sendMessage(chat_id, song["url"])
			else:
				song = find_song([search_terms[0]], sentiment, faster_than, slower_than)
				if song:
					bot.sendMessage(chat_id, song["url"])
				else:
					bot.sendMessage(chat_id, messages["not_found"])
		except:
			print "Error!"
			print traceback.format_exc()

def find_song(search_words, sentiment=None, faster_than=None, slower_than=None):

	print search_words, sentiment, faster_than, slower_than

	spotify_data = None
	try:
		spotify_data = spotify.get_tracks(spotify_token, search_words, 20)
	except:
		print "No data from spotify! New key?"
		return None

	if len(spotify_data) < 1:
		return None

	selected_song = spotify_data[0]
	fail_counter = 0

	for song in spotify_data:
		song_fits = True

		print "Checking song %s - %s" % (song["artist"].encode('utf-8'), song["name"].encode('utf-8'))

		if not faster_than is None:
			tempo = song["tempo"]
			if tempo <= faster_than:
				song_fits = False
			elif abs(faster_than - tempo) <= SPEED_THRESHOLD:
				song_fits = False
		elif not slower_than is None:
			tempo = song["tempo"]
			if tempo >= slower_than:
				song_fits = False
			elif abs(slower_than - tempo) <= SPEED_THRESHOLD:
				song_fits = False
		elif not sentiment is None:
			text = lyrics.get_lyrics(song["artist"], song["name"])
			song_sentiment = sentiments.analyze_sentiment(text)
			if song_sentiment is None:
				fail_counter += 1
				if fail_counter > MAX_FAILS:
					break
				continue
			if abs(song_sentiment - sentiment) >= SENTIMENT_THRESHOLD:
				song_fits = False

		if song_fits:
			selected_song = song
			break

	return selected_song

def main():
	global telegram_token, spotify_token, bot

	if len(sys.argv) < 3:
		print "Usage: python %s <TELEGRAM_TOKEN> <SPOTIFY_TOKEN>" % sys.argv[0]
		sys.exit(1)

	telegram_token = sys.argv[1]
	spotify_token = sys.argv[2]
	bot = telepot.Bot(telegram_token)
	bot.message_loop(handle_message)
	print 'Waiting for messages...'

	while 1:
		sys.stdout.flush()
		time.sleep(1)

if __name__ == '__main__':
	main()