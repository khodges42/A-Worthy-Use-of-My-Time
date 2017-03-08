from yelp.client import Client
from yelp.oauth1_authenticator import Oauth1Authenticator
from operator import itemgetter, attrgetter, methodcaller
import io, json, sys


res = []

# read API keys
with io.open('config_secret.json') as cred:
    creds = json.load(cred)
    auth = Oauth1Authenticator(**creds)

client = Client(auth)

params = {
    'term': sys.argv[1],
    'lang': 'en'
}

response = client.search('Cape Canaveral', **params)

for business in sorted(response.businesses):
    res.append([business.name,str(business.rating)])
    
for result in sorted(res,key=itemgetter(1),reverse=True):
    print result[0] + " " + result[1]