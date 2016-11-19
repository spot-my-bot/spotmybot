import spotipy as sy

def get_songs(auth, words, limit=50):
	if limit > 50:
		limit = 50
	return get_tracks(words, limit)

def get_tracks(auth, words, limit):
	sp = sy.Spotify(auth=auth)
	tracks = sp.search(q=' '.join(words), type='track', limit=limit)['tracks']['items']
	tracks = {t['id']: t for t in tracks}
	try:
		features = get_audio_features(tracks.keys(), sp)
		for f in features:
			tracks[f['id']].update(f)
	except:
		pass
	return map(get_relevant_data, tracks.values())

def get_audio_features(tracks, sp):
	return sp.audio_features(list(tracks))

def get_relevant_data(track):
	return {
		'artist': track['artists'][0]['name'],
		'album': track['album']['name'],
		'id': track['id'],
		'name': track['name'],
		'url': track['external_urls']['spotify'],
		'key': track.get('key'),
		'loudness': track.get('loudness'),
		'tempo': track.get('tempo'),
	}
