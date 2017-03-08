from yelp.client import Client
from yelp.oauth1_authenticator import Oauth1Authenticator
import io, json, sys
from sklearn import tree


res = []
features = []
classifiers = []
with open('likes.json') as likesfile:
    likes=json.load(likesfile)
# read API keys
with io.open('config_secret.json') as cred:
    creds = json.load(cred)
    auth = Oauth1Authenticator(**creds)
client = Client(auth)
params = {
    'term': sys.argv[1],
    'lang': 'en'
}


response = client.search(sys.argv[2], **params)



for business in sorted(response.businesses):
        if business.name in likes:
            res.append([business.name,str(business.rating),str(business.review_count),likes[business.name]])
        else:
            res.append([business.name,str(business.rating),str(business.review_count),0])
    #cat = ''.join(business.categories[Category])
    #res.append([business.name,str(business.rating),str(business.review_count)])

for item in res:
    features.append([float(item[1]),int(item[2])])
    classifiers.append(item[3])
    
clf = tree.DecisionTreeClassifier()
clf = clf.fit(features,classifiers)
print clf.predict([4.0,20])

for result in sorted(res,key=itemgetter(1),reverse=True):
    if result[0] in likes:
        
        if likes[result[0]] == '1':           
            print "--- "+result[0] + " " + result[1] + " (" + result[2] + ")"
            print clf.predict([result[1],result[2]])
        if likes[result[0]] == '2':           
            print "+++ "+result[0] + " " + result[1] + " (" + result[2] + ")"
            print clf.predict([result[1],result[2]])
    else:
        print "  "+result[0] + " " + result[1] + " (" + result[2] + ")"
        print clf.predict([result[1],result[2]])
        


