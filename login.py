import constants
import oauth2
import urllib.parse as urlparse
import json

consumer = oauth2.Consumer(constants.CONSUMER_KEY, constants.CONSUMER_SECRET)
client = oauth2.Client(consumer)

if constants.ACCESS_TOKEN == '':
    response, content = client.request(constants.REQUEST_TOKEN_URL, 'POST')
    if response.status!= 200:
        print("An error occurred getting the request form twitter!")

    request_token = dict(urlparse.parse_qsl(content.decode('utf-8')))

    print("Go to Site:")
    print("{}?oauth_token={}".format(constants.AUTHORIZATION_URL, request_token['oauth_token']))

    oauth_verifier = input("What is the Pin?")
    token = oauth2.Token(request_token['oauth_token'], request_token['oauth_token_secret'])
    token.set_verifier(oauth_verifier)
    client = oauth2.Client(consumer, token)

    response, content = client.request(constants.ACCESS_TOKEN_URL, 'POST')
    a = dict(urlparse.parse_qsl(content.decode('utf-8')))
    print(a)

else:

    search_term = input("What do you want to search?\n> ")
    # Create an authorized token to perform API calls on behalf of user
    authorized_token = oauth2.Token(constants.ACCESS_TOKEN['oauth_token'], constants.ACCESS_TOKEN['oauth_token_secret'])
    authorized_client = oauth2.Client(consumer, authorized_token)


response, content = authorized_client.request('https://api.twitter.com/1.1/search/tweets.json?q={}+filter:images'.format(search_term))
if response.status != 200:
    print(response.status)
else:
    print(json.loads(content.decode("utf-8")))
