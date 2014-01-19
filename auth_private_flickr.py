#!/usr/bin/env python

# This script generates a permanent token so you can download photos from your private flickr account.
# Use the auth token generated at the end in the download_private_flickr.py script.

import flickrapi
import json
import hashlib

api_key = '********'
api_secret = '*******'
perms = 'read'

flickr = flickrapi.FlickrAPI(api_key, api_secret)
flickr.token.path = '/tmp/flickrtokens'

responseFrob = flickr.auth_getFrob()
frobToken = responseFrob.find('frob').text
sig = '%sapi_key%sfrob%sperms%s' % (api_secret, api_key, frobToken,perms)
m = hashlib.md5()
m.update(sig)
sigmd5 = m.hexdigest()


url = 'http://flickr.com/services/auth/?api_key=%s&perms=%s&frob=%s&api_sig=%s' % (api_key,perms,frobToken,sigmd5)
print 'Go to this url and authorise your application:\n %s' % url

raw_input("Press ENTER after you authorized this program:")

authResponse = flickr.get_token(frobToken)
authToken = authResponse.find('token')
print "AUTH_TOKEN=%s" % authToken