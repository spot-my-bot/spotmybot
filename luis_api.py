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

def getEmotion(message):
	resp=callLUIS(message)
	entities=parseEntities(resp)
	if len(entities)>0 :
		return entities[0]
	else:
		return ''

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

def parseEntities(resp):
	entities=[]
	if resp is not None:
		try:
			#print "entities" + str(resp['entities'])
			#print type(resp['entities']), len(resp['entities'])
			for ent in resp['entities']:
				if ent['type']=='Emotion':
					entities.append(ent['entity'])
		except KeyError ,ke:
			print 'entities not found'
	return entities

print getEmotion("find something heroic")
