#########################################
##### Name: Hisamitsu Maeda         #####
##### Uniqname: himaeda             #####
#########################################

from requests_oauthlib import OAuth1
import json
import requests
from collections import Counter

import hw6_secrets_starter as secrets # file that contains your OAuth credentials

CACHE_FILENAME = "twitter_cache.json"
CACHE_DICT = {}

client_key = secrets.TWITTER_API_KEY
client_secret = secrets.TWITTER_API_SECRET
access_token = secrets.TWITTER_ACCESS_TOKEN
access_token_secret = secrets.TWITTER_ACCESS_TOKEN_SECRET

oauth = OAuth1(client_key,
            client_secret=client_secret,
            resource_owner_key=access_token,
            resource_owner_secret=access_token_secret)

# http://xpo6.com/list-of-english-stop-words/
stopwords = ["a", "about", "above", "above", "across", "after",
                "afterwards", "again", "against", "all", "almost",
                "alone", "along", "already", "also", "although",
                "always", "am", "among", "amongst", "amoungst",
                "amount",  "an", "and", "another", "any", "anyhow",
                "anyone", "anything", "anyway", "anywhere", "are",
                "around", "as",  "at", "back","be","became",
                "because","become","becomes", "becoming",
                "been", "before", "beforehand", "behind",
                "being", "below", "beside", "besides", "between",
                "beyond", "bill", "both", "bottom","but", "by",
                "call", "can", "cannot", "cant", "co", "con",
                "could", "couldnt", "cry", "de", "describe",
                "detail", "do", "done", "down", "due", "during",
                "each", "eg", "eight", "either", "eleven", "else",
                "elsewhere", "empty", "enough", "etc", "even",
                "ever", "every", "everyone", "everything",
                "everywhere", "except", "few", "fifteen",
                "fify", "fill", "find", "fire", "first",
                "five", "for", "former", "formerly", "forty",
                "found", "four", "from", "front", "full",
                "further", "get", "give", "go", "had", "has",
                "hasnt", "have", "he", "hence", "her", "here",
                "hereafter", "hereby", "herein", "hereupon",
                "hers", "herself", "him", "himself", "his",
                "how", "however", "hundred", "ie", "if", "in",
                "inc", "indeed", "interest", "into", "is", "it",
                "its", "itself", "keep", "last", "latter",
                "latterly", "least", "less", "ltd", "made", "many",
                "may", "me", "meanwhile", "might", "mill", "mine",
                "more", "moreover", "most", "mostly", "move", "much",
                "must", "my", "myself", "name", "namely", "neither",
                "never", "nevertheless", "next", "nine", "no", "nobody",
                "none", "noone", "nor", "not", "nothing", "now",
                "nowhere", "of", "off", "often", "on", "once", "one",
                "only", "onto", "or", "other", "others", "otherwise",
                "our", "ours", "ourselves", "out", "over", "own","part",
                "per", "perhaps", "please", "put", "rather", "re", "same",
                "see", "seem", "seemed", "seeming", "seems", "serious",
                "several", "she", "should", "show", "side", "since",
                "sincere", "six", "sixty", "so", "some", "somehow",
                "someone", "something", "sometime", "sometimes",
                "somewhere", "still", "such", "system", "take",
                "ten", "than", "that", "the", "their", "them",
                "themselves", "then", "thence", "there", "thereafter",
                "thereby", "therefore", "therein", "thereupon",
                "these", "they", "thickv", "thin", "third",
                "this", "those", "though", "three", "through",
                "throughout", "thru", "thus", "to", "together",
                "too", "top", "toward", "towards", "twelve",
                "twenty", "two", "un", "under", "until", "up",
                "upon", "us", "very", "via", "was", "we", "well",
                "were", "what", "whatever", "when", "whence",
                "whenever", "where", "whereafter", "whereas",
                "whereby", "wherein", "whereupon", "wherever",
                "whether", "which", "while", "whither", "who",
                "whoever", "whole", "whom", "whose", "why", "will",
                "with", "within", "without", "would", "yet", "you",
                "your", "yours", "yourself", "yourselves", "the"]

def test_oauth():
    ''' Helper function that returns an HTTP 200 OK response code and a
    representation of the requesting user if authentication was
    successful; returns a 401 status code and an error message if
    not. Only use this method to test if supplied user credentials are
    valid. Not used to achieve the goal of this assignment.'''

    url = "https://api.twitter.com/1.1/account/verify_credentials.json"
    auth = OAuth1(client_key, client_secret, access_token,
                    access_token_secret)
    authentication_state = requests.get(url, auth=auth).json()
    return authentication_state


def open_cache():
    ''' Opens the cache file if it exists and loads the JSON into
    the CACHE_DICT dictionary.
    if the cache file doesn't exist, creates a new cache dictionary

    Parameters
    ----------
    None

    Returns
    -------
    The opened cache: dict
    '''
    try:
        cache_file = open(CACHE_FILENAME, 'r')
        cache_contents = cache_file.read()
        cache_dict = json.loads(cache_contents)
        cache_file.close()
    except:
        cache_dict = {}
    return cache_dict


def save_cache(cache_dict):
    ''' Saves the current state of the cache to disk

    Parameters
    ----------
    cache_dict: dict
        The dictionary to save

    Returns
    -------
    None
    '''
    dumped_json_cache = json.dumps(cache_dict)
    fw = open(CACHE_FILENAME, "w")
    fw.write(dumped_json_cache)
    fw.close()


def construct_unique_key(baseurl, params):
    ''' constructs a key that is guaranteed to uniquely and
    repeatably identify an API request by its baseurl and params

    AUTOGRADER NOTES: To correctly test this using the autograder, use an underscore ("_")
    to join your baseurl with the params and all the key-value pairs from params
    E.g., baseurl_key1_value1

    Parameters
    ----------
    baseurl: string
        The URL for the API endpoint
    params: dict
        A dictionary of param:value pairs

    Returns
    -------
    string
        the unique key as a string
    '''
    #TODO Implement function
    unique_key = baseurl
    for k, v in params.items():
        unique_key += '_' + k + '_' + str(v)
    return unique_key


def make_request(baseurl, params):
    '''Make a request to the Web API using the baseurl and params

    Parameters
    ----------
    baseurl: string
        The URL for the API endpoint
    params: dictionary
        A dictionary of param:value pairs

    Returns
    -------
    dict
        the data returned from making the request in the form of
        a dictionary
    '''
    #TODO Implement function
    response = requests.get(baseurl, params=params, auth=oauth)
    return response.json()


def make_request_with_cache(baseurl, hashtag, count):
    '''Check the cache for a saved result for this baseurl+params:values
    combo. If the result is found, return it. Otherwise send a new
    request, save it, then return it.

    AUTOGRADER NOTES: To test your use of caching in the autograder, please do the following:
    If the result is in your cache, print "fetching cached data"
    If you request a new result using make_request(), print "making new request"

    Do no include the print statements in your return statement. Just print them as appropriate.
    This, of course, does not ensure that you correctly retrieved that data from your cache,
    but it will help us to see if you are appropriately attempting to use the cache.

    Parameters
    ----------
    baseurl: string
        The URL for the API endpoint
    hashtag: string
        The hashtag to search for
    count: integer
        The number of results you request from Twitter

    Returns
    -------
    dict
        the results of the query as a dictionary loaded from cache
        JSON
    '''
    #TODO Implement function
    params = {'q': hashtag.lower(), 'count': count}
    request_key = construct_unique_key(baseurl, params)
    if request_key in CACHE_DICT.keys():
        print("fetching cached data")
        return CACHE_DICT[request_key]
    else:
        print("making new request")
        CACHE_DICT[request_key] = make_request(baseurl, params)
        save_cache(CACHE_DICT)
        return CACHE_DICT[request_key]


def find_top3_common_cooccurring_hashtag(tweet_data, hashtag_to_ignore):
    ''' Finds the hashtag that top 3 commonly co-occurs with the hashtag
    queried in make_request_with_cache().

    Parameters
    ----------
    tweet_data: dict
        Twitter data as a dictionary for a specific query
    hashtag_to_ignore: string
        the same hashtag that is queried in make_request_with_cache()
        (e.g. "#MarchMadness2021")

    Returns
    -------
    None
    print out the top3 common co-occuring hashtag if they are found.

    '''
    # TODO: Implement function
    hashtag_list = []
    for tweet in tweet_data['statuses']:
        for hashtag_find in tweet['entities']['hashtags']:
            hashtag_list.append(hashtag_find['text'].lower())
    c = Counter(hashtag_list)
    # check whether there is cooccuring hashtag
    if len(c.most_common()) < 2:
        print(f"There is no cooccuring hashtag with {hashtag_to_ignore}.")
    else:
        hashtag_list = []
        for hashtag_co, _ in c.most_common():
            if hashtag_co == hashtag_to_ignore[1:].lower():
                pass
            else:
                hashtag_list.append(hashtag_co)
            if len(hashtag_list) == 3:
                break
        # Care when there are hashtags less than 3.
        print(f"The top {len(hashtag_list)} most commonly co-occuring ",
                f"hashtags with {hashtag_to_ignore}:")
        for tag in hashtag_list:
            print(tag)
    ''' Hint: In case you're confused about the hashtag_to_ignore
    parameter, we want to ignore the hashtag we queried because it would
    definitely be the most occurring hashtag, and we're trying to find
    the most commonly co-occurring hashtag with the one we queried (so
    we're essentially looking for the second most commonly occurring
    hashtags).'''


if __name__ == "__main__":
    # This is for just checking
    if not client_key or not client_secret:
        print("You need to fill in CLIENT_KEY and CLIENT_SECRET in secret_data.py.")
        exit()
    if not access_token or not access_token_secret:
        print("You need to fill in ACCESS_TOKEN and ACCESS_TOKEN_SECRET in secret_data.py.")
        exit()

    CACHE_DICT = open_cache()

    baseurl = "https://api.twitter.com/1.1/search/tweets.json"
    count = 100
    initial_comment = 'Please enter a hashtag(#***) you want to search, '
    initial_comment += 'or "exit" to quit: '

    while True:
        hashtag = input(initial_comment)
        if hashtag == 'exit':
            print("Bye!")
            break
        # To check whether the input is hashtag or not
        if hashtag[0] != '#':
            print('Hashtag must start from "#", please re-enter a hashtag.')
        else:
            tweet_data = make_request_with_cache(baseurl, hashtag, count)
            if len(tweet_data['statuses']) == 0:
                print("No results fetched, your hashtag may be nonsense.")
                print("Please reconsider a hashtag.")
            else:
                find_top3_common_cooccurring_hashtag(tweet_data, hashtag)
        print()
