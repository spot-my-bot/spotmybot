import os, sys
import requests
from config import *

luis_http_service ='https://api.projectoxford.ai/luis/v2.0/apps/ee569a80-115b-439f-a93d-3bfcdea54888?subscription-key=784bddb1f33f41adb474f784d12b3c0a&q=I%20feel%20sad&verbose=true'

def callLUIS(queryText):
	# Request headers
	headers = {
    	'Ocp-Apim-Subscription-Key': SUBSCRIPTION_KEY,
	}
	params={'q': queryText,
		   'verbose' : 'True',
		   'subscription-key' : SUBSCRIPTION_KEY}
	base_url='https://api.projectoxford.ai/luis/v2.0/apps/{appId}'.format(appId=LUIS_APP_ID)
	req= requests.get(base_url, params=params)
	print req.text
	return req.json()

"""
try:
    conn = httplib.HTTPSConnection('api.projectoxford.ai')
    conn.request("GET", "/luis/v1.0/prog/apps/{appId}/actions/{actionId}?%s" % params, "{body}", headers)
    response = conn.getresponse()
    data = response.read()
    print(data)
    conn.close()
except Exception as e:
    print("[Errno {0}] {1}".format(e.errno, e.strerror))
	"""