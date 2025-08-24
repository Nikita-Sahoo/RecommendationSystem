from flask import Flask, request, render_template
import pandas as pd
import pickle
import requests

# Load Data
df = pickle.load(open('content_music_data.pkl', 'rb'))
similarity = pickle.load(open('similar_data.pkl', 'rb'))

# Initialize Flask App
app = Flask(__name__)
new_music = df

# Function to fetch album art from iTunes
def get_album_art(song_name, artist_name, movie_name):
    query = f"{movie_name} {song_name} ".replace(' ', '+')
    url = f"https://itunes.apple.com/search?term={query}&media=music&limit=1"
    try:
        response = requests.get(url, timeout=5)
        data = response.json()
        if data['resultCount'] > 0:
            return data['results'][0]['artworkUrl100'].replace('100x100', '300x300')
        else:
            return "https://via.placeholder.com/300x300?text=No+Image"
    except Exception as e:
        print(f"Error fetching album art: {e}")
        return "https://via.placeholder.com/300x300?text=Error"

# Recommendation logic
def recommendation(song_name=None, genre=None, movie=None, artists=None):
    if song_name:
        filtered_songs = new_music[new_music['SongName'].str.lower() == song_name.lower()]
    elif movie:
        filtered_songs = new_music[new_music['Movie'].str.lower() == movie.lower()]
    elif artists:
        filtered_songs = new_music[new_music['Artists'].str.lower().str.contains(artists.lower(), regex=False)]
    elif genre:
        filtered_songs = new_music[new_music['Genre'].str.lower().str.contains(genre.lower(), regex=False)]
    else:
        return [{"song": "No matching songs found!", "artist": "", "image_url": "https://via.placeholder.com/300x300?text=No+Image"}]

    if filtered_songs.empty:
        return [{"song": "No matching songs found!", "artist": "", "image_url": "https://via.placeholder.com/300x300?text=No+Image"}]

    all_distances = []
    for idx in filtered_songs.index:
        if idx < len(similarity):
            all_distances.extend([(song_idx, score) for song_idx, score in enumerate(similarity[idx])])

    all_distances = sorted(all_distances, key=lambda x: x[1], reverse=True)
    recommended_songs = []
    seen_songs = set()

    for _, row in filtered_songs.iterrows():
        song = row['SongName']
        artist = row['Artists']
        movie = row['Movie']
        if song not in seen_songs:
            image_url = get_album_art(song, artist, movie)
            recommended_songs.append({"song": song, "artist": artist, "movie": movie, "image_url": image_url})
            seen_songs.add(song)
        if len(recommended_songs) == 6:
            return recommended_songs

    for song_idx, _ in all_distances:
        if song_idx >= len(new_music):
            continue
        song = new_music.iloc[song_idx]['SongName']
        artist = new_music.iloc[song_idx]['Artists']
        movie = new_music.iloc[song_idx]['Movie']
        if song not in seen_songs:
            image_url = get_album_art(song, artist, movie)
            recommended_songs.append({"song": song, "artist": artist, "movie": movie, "image_url": image_url})
            seen_songs.add(song)
        if len(recommended_songs) == 6:
            break

    return recommended_songs

# Home route
@app.route('/')
def index():
    song_names = set(new_music['SongName'].dropna())
    movie_names = set(new_music['Movie'].dropna())

    artists = set()
    new_music['Artists'].dropna().apply(lambda x: artists.update(a.strip() for a in x.split(',')))

    genres = set()
    new_music['Genre'].dropna().apply(lambda x: genres.update(g.strip() for g in x.split(',')))

    names = list(song_names | movie_names | artists | genres)

    return render_template('index.html', name=names)

# Predict route
@app.route('/predict', methods=['POST'])
def predict():
    user_input = request.form.get('names', '').strip().lower()

    if user_input in new_music['SongName'].dropna().str.lower().values:
        songs = recommendation(song_name=user_input)
    elif user_input in new_music['Movie'].dropna().str.lower().values:
        songs = recommendation(movie=user_input)
    elif user_input in new_music['Artists'].dropna().str.lower().values:
        songs = recommendation(artists=user_input)
    elif user_input in new_music['Genre'].dropna().str.lower().values:
        songs = recommendation(genre=user_input)
    else:
        songs = [{"song": "No results", "artist": "", "movie": "", "image_url": "https://via.placeholder.com/300x300?text=No+Match"}]

    song_names = set(new_music['SongName'].dropna())
    movie_names = set(new_music['Movie'].dropna())

    artists = set()
    new_music['Artists'].dropna().apply(lambda x: artists.update(a.strip() for a in x.split(',')))

    genres = set()
    new_music['Genre'].dropna().apply(lambda x: genres.update(g.strip() for g in x.split(',')))

    names = list(song_names | movie_names | artists | genres)

    return render_template('index.html', name=names, songs=songs, movie_names=movie_names,user_input=user_input)

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
