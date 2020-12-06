import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
cid = '4e350361cbce4f5a9ec55a10bf91e390'
secret = '080dae78a694473faea84d3df3ae38dc'
import pandas as pd
client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret)
sp = spotipy.Spotify(client_credentials_manager
=
client_credentials_manager)

user1 = input("input the first user of the playlist you want to use")
url1 = input("input the link of the first playlist you want to use")
user2 = input("input the second user of the playlist you want to use")
url2 = input("input the link of the second playlist you want to use")


def getTrackIDs(user, playlist_id):
    ids = []
    playlist = sp.user_playlist(user, playlist_id)
    for item in playlist['tracks']['items']:
        track = item['track']
        ids.append(track['id'])
    return ids

ids = getTrackIDs(user1, url1[url1.find('playlist')+9:])
def getTrackFeatures(id):
  meta = sp.track(id)
  features = sp.audio_features(id)

  # meta
  name = meta['name']
  album = meta['album']['name']
  artist = meta['album']['artists'][0]['name']
  release_date = meta['album']['release_date']
  length = meta['duration_ms']
  popularity = meta['popularity']

  # features
  acousticness = features[0]['acousticness']
  danceability = features[0]['danceability']
  energy = features[0]['energy']
  instrumentalness = features[0]['instrumentalness']
  liveness = features[0]['liveness']
  loudness = features[0]['loudness']
  speechiness = features[0]['speechiness']
  tempo = features[0]['tempo']
  time_signature = features[0]['time_signature']

  track = [name, album, artist, release_date, length, popularity, danceability, acousticness, danceability, energy, instrumentalness, liveness, loudness, speechiness, tempo, time_signature]
  return track
tracks = []
for i in range(len(ids)):
  track = getTrackFeatures(ids[i])
  tracks.append(track)

# create dataset
df = pd.DataFrame(tracks, columns = ['name', 'album', 'artist', 'release_date', 'length', 'popularity', 'danceability', 'acousticness', 'danceability', 'energy', 'instrumentalness', 'liveness', 'loudness', 'speechiness', 'tempo', 'time_signature'])
#df.to_csv("spotify3.csv", sep = ',')
ids = getTrackIDs(user2, url2[url1.find('playlist')+9:])
tracks = []
for i in range(len(ids)):
  track = getTrackFeatures(ids[i])
  tracks.append(track)

# create dataset
df2 = pd.DataFrame(tracks, columns = ['name', 'album', 'artist', 'release_date', 'length', 'popularity', 'danceability', 'acousticness', 'danceability', 'energy', 'instrumentalness', 'liveness', 'loudness', 'speechiness', 'tempo', 'time_signature'])
#df2.to_csv("spotify2.csv", sep = ',')

columns = [ 'acousticness', 'energy', 'instrumentalness', 'liveness', 'speechiness']
j=[]
for c in columns:
    j.append(abs(df[c].mean() - df2[c].mean()))

j2 = []
for c in columns:
    j2.append(abs(df[c].median() - df2[c].median()))



comp = ((1-sum(j)/len(j))**2 + (1-sum(j2)/len(j2))**2)/2
artists = []

dflist = df['artist'].tolist()

for i in df2['artist']:
    if i in dflist:
        artists.append(i)

songs = []

dflist = df['name'].tolist()

for i in df2['name']:
    if i in dflist:
        songs.append(i)


comp3 = 1+(len(set(songs))/100)

comp2 = 1+(len(set(artists))/100)



genres1 = []

for i in df['artist']:
    result = sp.search(i)
    track = result['tracks']['items'][0]

    artist = sp.artist(track["artists"][0]["external_urls"]["spotify"])
    genres1.append(artist["genres"])

genres2 = []

for i in df2['artist']:
    result = sp.search(i)
    track = result['tracks']['items'][0]

    artist = sp.artist(track["artists"][0]["external_urls"]["spotify"])
    genres2.append(artist["genres"])




album = sp.album(track["album"]["external_urls"]["spotify"])

genre_1 = []
for i in genres1:
    for j in i:
        genre_1.append(j)

common_genre = []

for i in genres2:
    for j in i:
        if j in genre_1:
            common_genre.append(j)

#print(common_genre)

print("Genre Compatibility: "+str(len(set(common_genre))/len(set(genre_1))))

f = list(set(common_genre))

for i in f:
    print("* "+i)


print("Vibe Compatibility: "+str(comp))
print("Shared artists: ",end='')
if(len(artists)!=0):
    print(*list(set(artists)))
else:
    print("No Shared artists :(")

print("Shared songs: ",end='')
if(len(songs)!=0):
    print(*list(set(songs)))
else:
    print("No Shared songs :(")

print("Overall Compatibility: "+str((len(set(common_genre))/len(set(genre_1))*.65 + comp*.35)*comp2*comp3))
