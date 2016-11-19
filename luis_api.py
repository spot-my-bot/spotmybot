import os, sys
import requests
from config import *


def callLUIS(queryText):
	headers = {
    # Request headers
    'Ocp-Apim-Subscription-Key': SUBSCRIPTION_KEY,
	}
	params={'q': queryText,
		   'verbose' : 'True',
		   'subscription-key' : SUBSCRIPTION_KEY}
	base_url='https://api.projectoxford.ai/luis/v2.0/apps/{appId}'.format(appId=LUIS_APP_ID)
	req= requests.get(base_url, params=params)
	print req.text
	if req.status_code==200:
		resp=req.json()
	else:
		resp=None
	return resp



def parseIntent(resp):
	intent=''
	score=0.0
	if resp is not None:
		print resp['topScoringIntent']
		try:
			intent=resp['topScoringIntent']['intent']
			score=resp['topScoringIntent']['score']
		except KeyError, ke:
			print 'intent not found'
	return intent, score

"""
USAGE:
emotion=parseEntities(message, 'Emotion')
genre=parseEntities(message, 'Genre')
"""
def parseEntities(message, entity_type):
	entity=''
	entities=[]
	resp=callLUIS(message)
	if resp is not None:
		try:
			#print "entities" + str(resp['entities'])
			#print type(resp['entities']), len(resp['entities'])
			for ent in resp['entities']:
				if ent['type']==entity_type:
					entities.append(ent['entity'])
			if len(entities)>0: entity=' '.join(entities)
		except KeyError ,ke:
			print 'entities not found'
	return entity

