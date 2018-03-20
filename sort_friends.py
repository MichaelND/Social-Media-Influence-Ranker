from __future__ import absolute_import
import tweepy
from collections import defaultdict
import random
from train import model

CONSUMER_KEY = 'ezeJc9OIdOfQqCeIh3L6oZhyv'
CONSUMER_SECRET = 'WYtZpuAGjAzVYrlNFtMfyX9N7pbfQNWv86ddagimPTtFF3XIMF'
ACCESS_TOKEN = '869387300291182592-LwanuzQPOfrLU7upuc1L5kDIujXowvZ'
ACCESS_TOKEN_SECRET = 'KYTch9vCYCiGN585yTY9rOablnGmrSgtpWdM6sARi6Z2p'



auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth, parser=tweepy.parsers.JSONParser())

def get_user_data(user1):
	global api
	user1_info = {}
	u1 = api.get_user(user1)
	user1_info['name'] = u1['screen_name']
	user1_info['followers'] = u1['followers_count']
	user1_info['following'] = u1['friends_count']
	user1_info['listed'] = u1['listed_count']
	user1_info['posts'] = u1['statuses_count']
	#print(user1_info)
	return user1_info

def model_function(temp_list):
	return [random.getrandbits(1) for i in temp_list]

def rank_friends(user, M):
	global api
	
	friends_win_counts = defaultdict(lambda: 0)
	friends_info = [get_user_data(user)]
	friends = api.friends_ids()
	for friend in friends['ids']:
		try:
			friends_info.append(get_user_data(friend))
		except tweepy.error.TweepError:
			print("Friend account not found skipping... ", friends)
	friends_perms = []
	for u1 in range(len(friends_info)-1):
		for u2 in range(u1+1,len(friends_info)):
			temp_tuple = (friends_info[u1], friends_info[u2])
			friends_perms.append(temp_tuple)

	data = []
	for friend_tuple in friends_perms:
		model_input = []
		for user in friend_tuple:
			model_input += [user['followers'], user['following'], user['listed'], user['posts']]
		data.append(model_input)
	
	model_output = model_function(data)

	for i, m in enumerate(model_output):
		if not m:
			f = friends_perms[i][0]
		else:
			f = friends_perms[i][1]
		friends_win_counts[(f['name'],f['following'],f['followers'])] += 1


	unsorted_users = []
	for key,val in friends_win_counts.items():
		unsorted_users.append((val,key))
	sorted_users = sorted(unsorted_users, reverse=True)
	#print("sorted: ", sorted_users)
	return [i[1] for i in sorted_users]


if __name__ == '__main__':
	M = model()
	print("final: ", rank_friends('869387300291182592', M))
