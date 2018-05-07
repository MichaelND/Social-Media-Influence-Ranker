import klout 
from train import model
from sort_friends import sort_list

user_list = ["enlighter2016", "BarackObama", "Oprah", "kanyewest", "kendricklamar", "realDonaldTrump"]

#http://mediakix.com/2018/03/top-influencers-social-media-instagram-youtube/#gs.Fa_7Tvs
youtube_list = ["pewdiepie", "whindersson", "LoganPaul", "Rubiu5", "DudePerfect"]

k = klout.Klout('d7u56pdjufz5hntyu7utbnzy')

def get_score(user):
	kloutId = k.identity.klout(screenName=user).get('id')
	score = k.user.score(kloutId=kloutId).get('score')
	return (user, score)

def compare_results(input_list):

	print(sorted([get_score(u) for u in input_list], key = lambda x: x[1], reverse = True))

	M = model()
	print([(u[0], u[1]) for u in sort_list(input_list, M)])

compare_results(user_list)
