import sys
import time
import telepot
#from luis_api import *
from messages import messages
import sentiments
import traceback
import spotify
import lyrics
from luis_api import getEmotion

chats = {}
BOT_NAME = "SpotMyBot"

def handle_message(msg):
	content_type, chat_type, chat_id = telepot.glance(msg)
	response = ""
	sentiment = ""

	try:
		if content_type == "text":
			message = msg["text"]
			print "Handling message: %s" % message

			if chat_id not in chats:
				chats[chat_id] = { "history": [] }
				response = messages["introduction"]
				sentiment = "neutral"
			else:
				sentiment = sentiments.analyze_sentiment(message)
				if sentiment is None:
					response = messages["not_understood"]
				else:
					response = messages[sentiment]
			emotion=getEmotion(message)
			print emotion
			
			#chats[chat_id]['history'].append(message)
			first_name = msg["from"]["first_name"]

			
			response = response.replace("<NAME>", first_name)
			response = response.replace("<BOTNAME>", BOT_NAME)
			response = response.replace("<MOOD>", emotion)
			print response

			bot.sendMessage(chat_id, response)

			spotify_data = spotify.get_tracks(spotify_token, [message.split()[0]], 20)

			selected_song = spotify_data[0]
			for song in spotify_data:
				text = lyrics.get_lyrics(song["artist"], song["name"])
				song_sentiment = sentiments.analyze_sentiment(text)

				if song_sentiment == sentiment:
					selected_song = song
					break

			link = selected_song["url"]
			bot.sendMessage(chat_id, link)

	except Exception:
		print "Error!"
		print traceback.format_exc()

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