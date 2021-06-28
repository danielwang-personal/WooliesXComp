import json
import requests
from textblob import TextBlob
import networkx as nx

def create_url():
    # (supermarket OR food OR grocery OR retail) lang:en 
    query = "(supermarket%20OR%20food%20OR%20grocery%20OR%20retail)%20lang%3Aen%20"
    tweet_fields = "tweet.fields=public_metrics,author_id"
    url = "https://api.twitter.com/2/tweets/search/recent?query={}&{}".format(query, tweet_fields)
    return url


def create_headers(bearer_token):
    headers = {"Authorization": "Bearer {}".format(bearer_token)}
    return headers


def connect_to_endpoint(url, headers):
    response = requests.request("GET", url, headers=headers)
    print(response.status_code)
    if response.status_code != 200:
        raise Exception(
            "Request returned an error: {} {}".format(
                response.status_code, response.text
            )
        )
    return response.json()

def get_author_ids(dump):
    data = dump['data']
    author_id = []
    for tweet in data:
        author_id.append(tweet['author_id'])
    return author_id

# def get_friends_list(user_id):

def connectivity(network):
    nw_graph = {user.id:user.follows for user in network}
    G = nx.graph(nw_graph)
    nx.centre(G)
    pr = nx.pagerank(G)
    nodes = sorted([(node, pagerank) for node, pagerank in pr.items()], key=lambda x:pr[x[0]])
    

    bearer_token = "AAAAAAAAAAAAAAAAAAAAALP7QwEAAAAAILlOlUyBZKqKiOmhwghZe4xQTzw%3DeAcDSNrGucfsV9LPyU01Y2cxObLspZfeJoCQ94pzld9MaEIUXI"
    url = create_url()
    headers = create_headers(bearer_token)
    json_response = connect_to_endpoint(url, headers)
    dump = json.loads(json.dumps(json_response, indent=4, sort_keys=True))
    print(dump)
    author_id = get_author_ids(dump)
    print(author_id)



if __name__ == "__main__":
    main()



# import tweepy
# from textblob import TextBlob

# consumer_key = 'J5bnTFdRb2XkGXPkPVh7Gfm7U'
# consumer_key_secret = 'Rgpk2UI7R1RGK4J6BNOmMRILNT2kGoyHFIj7aGvXgglO39uYo4'
# access_token = '3269418074-r5XJHj6qPNrSOCVnXyShiqwfPsdotEBDkee9hAA'
# access_token_secret = '7G3HQxFdkidpihfP4RFmbdVlYS0cyNFt1BZMFH987CJWg'
# auth = tweepy.OAuthHandler(consumer_key, consumer_key_secret)
# auth.set_access_token(access_token, access_token_secret)
# api = tweepy.API(auth)

# query = 'COVID-19'
# max_tweets = 2000
# searched_tweets = [status for status in tweepy.Cursor(api.search, q=query).items(max_tweets)]

# pos = 0
# neg = 0
# neu = 0
# for tweet in searched_tweets:
#     analysis = TextBlob(tweet.text)
#     if analysis.sentiment[0]>0:
#        pos = pos +1
#     elif analysis.sentiment[0]<0:
#        neg = neg + 1
#     else:
#        neu = neu + 1
# print("Total Positive = ", pos)
# print("Total Negative = ", neg)
# print("Total Neutral = ", neu)