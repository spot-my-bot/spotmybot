import sys
import time
import telepot
from luis_api import *

"""
$ python2.7 skeleton.py <token>
A skeleton for your telepot programs.
"""

def handle(msg):
	content_type, chat_type, chat_id = telepot.glance(msg)
	print(content_type, chat_type, chat_id)

	if content_type == 'text':
		#bot.sendMessage(chat_id, msg['from']['first_name'])
		#print(msg['text'])
		input = str(msg['text']).lower()
		bot_resp= callLUIS(input)
		action,score=parseIntent(bot_resp)
		entities=parseEntities(bot_resp)
		#pass entities as search criteria
		
		bot.sendMessage(chat_id,'Hallo '+ msg['from']['first_name']+'!')
    	#bot.sendMessage(chat_id, action)
		#bot.sendMessage(chat_id, (entities))
		
		#display song 


TOKEN = sys.argv[1]  

bot = telepot.Bot(TOKEN)
bot.message_loop(handle)
print 'Listening ...'

# Keep the program running.
while 1:
	time.sleep(10)