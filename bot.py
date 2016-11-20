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
BOT_NAME = "Mozart"
SENTIMENT_THRESHOLD = 0.3

chats = {}

def handle_message(msg):
	content_type, chat_type, chat_id = telepot.glance(msg)
	response = ""
	sentiment = ""
	task = "info"

	if content_type == "text":
		try:
			message = msg["text"]
			print "Handling message: %s" % message

			if chat_id not in chats:
				chats[chat_id] = { "history": [] }
				response = messages["introduction"]
				sentiment = "neutral"
			else:
				sentiment = sentiments.analyze_sentiment(message)
				print sentiment
				if sentiment is None:
					response = messages["not_understood"]
				else:
					if sentiment > 0.7:
						response = messages["pos"]
					elif sentiment < 0.3:
						response = messages["neg"]
					else:
						response = messages["neutral"]
					task = "find_song"
			
			chats[chat_id]['history'].append(message)
			first_name = msg["from"]["first_name"]
			emotion=parseEntities(message, 'Emotion')
			
			response = response.replace("<NAME>", first_name)
			response = response.replace("<BOTNAME>", BOT_NAME)
			response = response.replace("<MOOD>", emotion)

			bot.sendMessage(chat_id, response)

			if task != "find_song":
				return

			link = find_song([message.split()[0]], sentiment)
			if link:
				bot.sendMessage(chat_id, link)
		except:
			print "Error!"
			print traceback.format_exc()

def find_song(search_words, sentiment):
	spotify_data = spotify.get_tracks(spotify_token, search_words, 20)

	if len(spotify_data) < 1:
		return None

	selected_song = spotify_data[0]
	for song in spotify_data:
		text = lyrics.get_lyrics(song["artist"], song["name"])
		song_sentiment = sentiments.analyze_sentiment(text)

		if song_sentiment is None:
			continue

		if abs(song_sentiment - sentiment) <= SENTIMENT_THRESHOLD:
			selected_song = song
			break

	return selected_song["url"]

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