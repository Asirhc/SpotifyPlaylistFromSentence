# SpotifyPlaylistFromSentence

This python script finds a list of Spotify tracks whose titles spell out a sentence specified by the user.

### Example:

input: 'Hello world this is a test'
output: ['https://open.spotify.com/track/5q1dFcN3ZZ0QwkYcPhkPvd', 'https://open.spotify.com/track/6wRYqERzrGEJDCXXOq1EFN']

### Usage:
To use this script, first make sure you activate a python 3.x environment, navigate to the directory of playlist_maker.py.  Edit playlist_maker.py and fill in the CLIENT_ID and CLIENT_SECRET variables.  Type "python playlist_maker.py" on your command line prompt to begin the script.  It only uses standard python libraries so you shouldn't have to install anything into your environment.


### Explanation:

For this project, it is preferable to find shorter playlists over longer ones.  This makes it appropriate to do a breadth-first search through the space of possible sequences of song titles (where depth of the node is the number of tracks).  For a sentence with N words, there are 2**N - 1 possible partitions of the sentence into sets of candidate title tracks. For each partition we need to know the results of several API calls in order to know if the partition has a corresponding Spotify playlist.  In order to speed up the script, I save the results of API calls in dictionaries so that I avoid ever having to make the same API call twice.  This optimization limits the total number of calls to at most N(N+1)/2.  Since the Spotify Web API does not include an "exact match" option to their track search endpoint, I am forced to linearly search through the response of my search requests to find an exact match to the desired title.