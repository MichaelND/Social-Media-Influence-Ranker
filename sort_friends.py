from __future__ import absolute_import
import tweepy
from collections import defaultdict
import random
from train import model
import numpy as np

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
	friends_info = [get_user_data(user)]

	friends = api.friends_ids(user)
	for friend in friends['ids']:
		try:
			friends_info.append(get_user_data(friend))
		except tweepy.error.TweepError:
			print("Friend account not found skipping... ", friends)
	friends_perms = []
	# print(friends_info)
	for u1 in range(len(friends_info)-1):
		for u2 in range(u1+1,len(friends_info)):
			temp_tuple = (friends_info[u1], friends_info[u2])
			friends_perms.append(temp_tuple)
	#print(friends_perms)
	data = []
	for friend_tuple in friends_perms:
		model_input = []
		for u in friend_tuple:
			model_input += [u['followers'], u['following'], u['listed'], u['posts']]
		data.append(model_input)
	model_output = M.predict(data)
	friends_win_counts = {(u['name'], u['following'], u['followers']): 0 for u in friends_info}
	for i, m in enumerate(model_output):
		if m:
			f = friends_perms[i][0]
		else:
			f = friends_perms[i][1]
		friends_win_counts[(f['name'],f['following'],f['followers'])] += 1


	unsorted_users = []
	for key,val in friends_win_counts.items():
		unsorted_users.append((val,key))
	sorted_users = sorted(unsorted_users, reverse=True)
	#print("sorted: ", sorted_users)
	return [(i[1][0], friends_win_counts[i[1]], i[1][1], i[1][2]) for i in sorted_users]

def sort_list(users, M):
	global api
	users_info = []
	for user in users:
		try:
			users_info.append(get_user_data(user))
		except tweepy.error.TweepError:
			print("User account not found skipping... ", user)
	if len(users_info) == 1:	
		u = users_info[0]
		return [(u["name"], 0, u['following'], u['followers'])]
	users_perms = []
	for u1 in range(len(users_info)-1):
		for u2 in range(u1+1,len(users_info)):
			temp_tuple = (users_info[u1], users_info[u2])
			users_perms.append(temp_tuple)
	#print(users_perms)
	data = []
	for user_tuple in users_perms:
		model_input = []
		for u in user_tuple:
			model_input += [u['followers'], u['following'], u['listed'], u['posts']]
		data.append(model_input)
	model_output = M.predict(data)
	users_win_counts = {(u['name'], u['following'], u['followers']): 0 for u in users_info}
	for i, m in enumerate(model_output):
		if m:
			f = users_perms[i][0]
		else:
			f = users_perms[i][1]
		users_win_counts[(f['name'],f['following'],f['followers'])] += 1


	unsorted_users = []
	for key,val in users_win_counts.items():
		unsorted_users.append((val,key))
	sorted_users = sorted(unsorted_users, reverse=True)
	#print("sorted: ", sorted_users)
	return [(i[1][0], users_win_counts[i[1]], i[1][1], i[1][2]) for i in sorted_users]

#if __name__ == '__main__':
# 	M = model()
# 	print("final: ", rank_friends('869387300291182592', M))
