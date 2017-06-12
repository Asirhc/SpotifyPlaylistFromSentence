from itertools import combinations
import requests
import base64

# Enter these so that you can connect to the spotify API
CLIENT_ID = #<enter client ID here> 
CLIENT_SECRET = #<enter client secret here>

def get_api_access_token(client_id, client_secret):
    headers = {'Authorization':'Basic ' + convert_to_b64(client_id, client_secret)}
    data = {'grant_type':'client_credentials'}
    r = requests.post('https://accounts.spotify.com/api/token', headers=headers, data=data)
    return r.json()['access_token']

	
def convert_to_b64(client_id, client_secret):
    auth_str = client_id + ':' + client_secret
    b64_auth_str = base64.urlsafe_b64encode(auth_str.encode()).decode()
    return b64_auth_str
	
	
# This is generated from the client id and client secret, and typically will last for an hour	
ACCESS_TOKEN = get_api_access_token(CLIENT_ID, CLIENT_SECRET)

	
# Save API call results in these dictionaries so that we don't repeat ourselves
FOUND_TRACK = {}
NO_TRACK = {}


def get_playlist_urls(list_of_titles):
    urls = [get_url_if_track_exists(t) for t in list_of_titles]
    return urls

	
def get_url_if_track_exists(track_title):
    global FOUND_TRACK
    global NO_TRACK
    if track_title.lower() in FOUND_TRACK.keys():
        return FOUND_TRACK[track_title.lower()]
    if track_title.lower() in NO_TRACK.keys():
        return None
    r = requests.get("https://api.spotify.com/v1/search?q={}&type=track".format('"{}"'.format(track_title)),
                      headers = {'Authorization': 'Bearer {}'.format(ACCESS_TOKEN)})
    r = r.json()
    spotify_data = r['tracks']['items']
    if spotify_data:
        for track in spotify_data:
            tname = track['name'].lower()
            if tname==track_title.lower() and track['disc_number']==1:    
                FOUND_TRACK[tname]=track['external_urls']['spotify']
                return track['external_urls']['spotify']
        NO_TRACK[track_title.lower()] = 'No exact match'
    else:
        NO_TRACK[track_title.lower()]='No search results'
        return None
    
	
# Perform a breadth-first search (where depth of the search tree is the number of tracks required)
# through the space of titles we could use to create a playlist
def find_spotify_tracks(s):
    s = clean_string(s)
    word_list = s.split(' ')
    for i in range(0,len(word_list)):
        combs = combinations(range(1,len(word_list)),i)
        for c in combs:
            splits = [0,]
            splits += list(c)
            playlist = [' '.join(x) for x in split_into_sublists(word_list, splits)]
            urls = get_playlist_urls(playlist)
            if None not in urls:
                return urls
    return 'No valid playlist found :('

	
# remove punctuation
def clean_string(s):
    return s.translate({ord(c):None for c in '!@?#$%^&*.;,'}) 
	
	
# helper function to split a list based on a list of splitting indices
def split_into_sublists(l, splits):
    output = []
    for i, index in enumerate(splits):
        if i!=len(splits)-1: 
            next_spot = splits[i+1]
            output += [l[index:next_spot]]
        else:
            output += [l[index:]]
    return output
	
	
def main():
    s=''
    while s != 'quit':
        s = input("What sentence would you like to create a playlist for? Type 'quit' to exit. ")
        if s=='quit':
            return
        print(find_spotify_tracks(s))
    
    
if __name__=='__main__':
    main()