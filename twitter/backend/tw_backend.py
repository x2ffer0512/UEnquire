import tweepy
from twitter.models import Tweets
from django.core.exceptions import ObjectDoesNotExist

def open_acct():
	# TWITTER ACCOUNT ACCESS
	secret = []
	file = open("secret.txt", "r")
	for line in file:
		secret.append(line.rstrip())	
	file.close() 
	
	consumer_key = secret [0]
	consumer_secret = secret[1]
	access_token = secret[2]
	access_token_secret = secret[3]

	auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_token,access_token_secret)
	api = tweepy.API(auth, wait_on_rate_limit=True)
	return api

# Classifying data in the Table
def data_cleaning(acct):
	# lists
	posts = []
	likes = []
	dates = []
	times = []
	hashtags = []
	links =[]
	
	for post in acct:
		# URL lists
		current_urls = [] 
		for url in post.entities['urls']:
			current_urls.append(url['expanded_url'])
		links.append(current_urls)
		# Hashtags lists 
		current_tags = []
		for ht in post.entities['hashtags']:
			current_tags.append(ht['text'])
		hashtags.append(current_tags)
		
		tweet = post.full_text
		num_like = post.favorite_count
		date = str(post.created_at)[:10]
		time = str(post.created_at)[11:]
		
		posts.append(tweet)
		likes.append(num_like)
		dates.append(date)
		times.append(time)
	
	return posts, likes, dates, times, hashtags, links 

def cursoring(api,i,num_post):
	return tweepy.Cursor(api.user_timeline, id = i.source_acct, tweet_mode = "extended").items(num_post)

def output(accounts, api, num_post):	
	sources = []
	accts = []
	for i in accounts:
		accts.append(i.source_acct)
		sources.append(cursoring(api,i,num_post))
	for i in range(len(sources)):
		posts, likes, dates, time, tags, links = data_cleaning(sources[i])
		source = accts[i]
		for i in range(num_post):
			twitt = Tweets.objects.all()
			try:
				twitt[0]
			except IndexError:
				entry = Tweets(source=source, posts=posts[i], likes=likes[i], dates=dates[i], time=time[i], tags =tags[i], links = links[i])
				entry.save()
			try:
				n = Tweets.objects.get(posts=posts[i])
			except ObjectDoesNotExist:
				entry = Tweets(source=source, posts=posts[i], likes=likes[i], dates=dates[i], time=time[i], tags =tags[i], links = links[i])
				entry.save()
	return accounts