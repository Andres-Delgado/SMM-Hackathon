#Takes in a list of statuses, extracts info from the status and places into dictionart
def extract_data(statuses, mydictionary, day_number):
    '''
    Parameters:
    Statuses(list) - Iterates over a list of statuses
    mydictionary - Dictionary to be filled in
    day_number - Day number to be filled in dictionary
    
    I excluded the code for searching all the statuses for a given day, since Logan is doing this.
    All this function serves to do is extract the information and fill in the corresponding fields
    in the dictionary.
    
    '''
    day_number = 'day' + str(day_number)
    for i in statuses:
        try:
            mydictionary[day_number]['created_at'].append(i['created_at'])
            mydictionary[day_number]['followers_count'].append(i['user']['followers_count'])
            mydictionary[day_number]['retweets_count'].append(i['retweet_count'])
            mydictionary[day_number]['lang'].append(i['user']['lang'])
            mydictionary[day_number]['favorite_count'].append(i['favorite_count'])
        except (KeyError):
            continue


