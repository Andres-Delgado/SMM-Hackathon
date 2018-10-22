## Setup
# import libraries
import matplotlib.pyplot as plt
import json as js
import numpy as np
import pycountry as pc

# Global variables
DAYS_PER_HASHTAG = 7
FILE_NAME = "../Data/Partition0.2-data.json"
IMAGE_OUTPUT = "../Data/Images/"
ITERATION_LIMIT= 15
DEBUG = True

## Helper Functions
def language_data(data):
	# Calculate language info
	lang = data['lang']
	for key in lang.keys():
		# insert lang key if not in pie chart labels insert it
		if key not in pie_lang.keys():
			pie_lang[key] = 0
		# update language counters
		pie_lang[key] += lang[key]

def avg_occurances(data, day):
	# We are gonna have a total and a count
	line_occurance[day]['total'] += data['occurrences']
	line_occurance[day]['count'] += 1

def avg_retweets(data, day):
	# We are gonna have a total and a count
	line_retweets[day]['total'] += sum(data['retweet_count'])
	line_retweets[day]['count'] +=1

def avg_favorite(data, day):
	# We are gonna have a total and a count
	line_favs[day]['total'] += sum(data['favorite_count'])
	line_favs[day]['count'] +=1

def avg_follower(data, day):
	# We are gonna have a total and a count
	line_follow[day]['total'] += sum(data['followers_count'])
	line_follow[day]['count'] +=1

def cleanup():
	# language clean up: flatten small slices into other
	sumation = sum(pie_lang.values())
	pie_lang['others'] = 0
	for key in list(pie_lang):
		if key == 'others':
			continue

		if (pie_lang[key] / sumation) * 100 < 3:
			pie_lang['others'] += pie_lang[key]
			pie_lang.pop(key, None)
		else:
			language = pc.languages.get(alpha_2=key)
			pie_lang[language.name] = pie_lang.pop(key, None)

	# clean up avg
	for day in range(DAYS_PER_HASHTAG):
		line_avg_data["day " + str(day)] = line_occurance["day " + str(day)]['total'] / line_occurance["day " + str(day)]['count']
		line_retweet_data["day " + str(day)] = line_retweets["day " + str(day)]['total'] / line_retweets["day " + str(day)]['count']
		line_fav_data["day " + str(day)] = line_favs["day " + str(day)]['total'] / line_favs["day " + str(day)]['count']
		line_follow_data["day " + str(day)] = line_follow["day " + str(day)]['total'] / line_follow["day " + str(day)]['count']

# Read JSON file
with open(FILE_NAME) as f:
	raw = js.load(f)

## Calculate Data
pie_lang = {"en": 0}
line_occurance = {"day 0": {"total": 0, "count":0}, "day 1": {"total": 0, "count":0}, "day 2": {"total": 0, "count":0}, "day 3": {"total": 0, "count":0}, "day 4": {"total": 0, "count":0}, "day 5": {"total": 0, "count":0}, "day 6": {"total": 0, "count":0}}
line_retweets = {"day 0": {"total": 0, "count":0}, "day 1": {"total": 0, "count":0}, "day 2": {"total": 0, "count":0}, "day 3": {"total": 0, "count":0}, "day 4": {"total": 0, "count":0}, "day 5": {"total": 0, "count":0}, "day 6": {"total": 0, "count":0}}
line_favs = {"day 0": {"total": 0, "count":0}, "day 1": {"total": 0, "count":0}, "day 2": {"total": 0, "count":0}, "day 3": {"total": 0, "count":0}, "day 4": {"total": 0, "count":0}, "day 5": {"total": 0, "count":0}, "day 6": {"total": 0, "count":0}}
line_follow = {"day 0": {"total": 0, "count":0}, "day 1": {"total": 0, "count":0}, "day 2": {"total": 0, "count":0}, "day 3": {"total": 0, "count":0}, "day 4": {"total": 0, "count":0}, "day 5": {"total": 0, "count":0}, "day 6": {"total": 0, "count":0}}
line_avg_data = {}
line_retweet_data = {}
line_follow_data = {}
line_fav_data = {}
break_counter = 0

for hashtag in raw:
	if DEBUG:
		print("Hashtag: " + hashtag)

	for day in range(DAYS_PER_HASHTAG):
		# break counter
		if break_counter > ITERATION_LIMIT:
			break
		else:
			break_counter +=1

		# temp data
		day_s = "day" + str(day)
		temp = raw[hashtag][day_s]

		# generate language data
		language_data(temp)

		# generate avg occurrences per day
		avg_occurances(temp, "day " + str(day))

		# avg number of retweets per day
		avg_retweets(temp, "day " + str(day))

		# avg number of favorite per day
		avg_favorite(temp, "day " + str(day))

		# avg number of followers per day
		avg_follower(temp, "day " + str(day))

# clean up data
cleanup()

# Of all hash tags how many followers 0-9,999, 10,000-99,000, and 100,000-above (pie chart)
	# avg number of followers per hashtag

## Plot Charts

# Language pie chart
fig1, ax1 = plt.subplots()
plt.title("Percentage of language across tweets")
ax1.pie(pie_lang.values(), labels=pie_lang.keys(), autopct='%1.1f%%')
plt.savefig(IMAGE_OUTPUT + 'pie_lang.png', bbox_inches='tight')

# Avg hashtag occurrence line chart
plt.figure()
plt.title("Average Hashtag Occurrence in one week")
plt.xlabel("Days")
plt.ylabel("# of Occurrence")
plt.plot([1,2,3,4,5,6,7], line_avg_data.values())
plt.savefig(IMAGE_OUTPUT + 'line_occurances.png', bbox_inches='tight')

# Avg hashtag retweets line chart
plt.figure()
plt.title("Average Hashtag Retweet in one week")
plt.xlabel("Days")
plt.ylabel("# of Retweets")
plt.plot([1,2,3,4,5,6,7], line_retweet_data.values())
plt.savefig(IMAGE_OUTPUT + 'line_retweets.png', bbox_inches='tight')

# Avg hashtag favorite line chart
plt.figure()
plt.title("Average Hashtag Favorite in one week")
plt.xlabel("Days")
plt.ylabel("# of Favorites")
plt.plot([1,2,3,4,5,6,7], line_fav_data.values())
plt.savefig(IMAGE_OUTPUT + 'line_favorites.png', bbox_inches='tight')

# Avg hashtag followers line chart
plt.figure()
plt.title("Average Hashtag Followers in one week")
plt.xlabel("Days")
plt.ylabel("# of Followers")
plt.plot([1,2,3,4,5,6,7], line_follow_data.values())
plt.savefig(IMAGE_OUTPUT + 'line_followers.png', bbox_inches='tight')

# Show graphs
plt.show()
