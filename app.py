from flask import Flask, request, session, url_for, redirect
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import time
import yt_dlp


app = Flask(__name__)

clientid = "74382212368f478a9b8cd2028a43b4e5"
clientSecret = "a10611d0e4524e42a06869db76dafbbf"

app.secret_key = "OAHDBFiooqwbfBDEWCB"
app.config["SESSION_COOKIE_NAME"] = "my cookie"

@app.route("/")
def login():
    sp_oath = get_spotify_oath()
    auth_url = sp_oath.get_authorize_url()
    return redirect(auth_url)

@app.route("/redirectPage")
def redirectPage():
    sp_oath = get_spotify_oath()
    session.clear()
    code = request.args.get("code")
    token_info = sp_oath.get_access_token(code)
    session["token_info"] = token_info
    return redirect(url_for("getTracks", _external = True))

@app.route("/getTracks")
def getTracks():
    try:
        token_info = get_token_info()
    except Exception:
        print("user not logged in")
        redirect(url_for("login", _external = False))
    sp = spotipy.Spotify(auth = token_info['access_token'])
    playlists = sp.current_user_playlists()
    results = sp.playlist_tracks("0hK9vlm9gBRt29abivQICT")
    song_names = []
    for item in results['items']:
        track = item['track']
        song_names.append(f"{track['name']}\n")
    
    with open("song_links.txt", "a") as f: 
       for song in song_names:
            query = f"ytsearch:{song}"
            with yt_dlp.YoutubeDL({"quiet": True}) as ydl:
                info = ydl.extract_info(query, download= False)
                if "entries" in info and info['entries']:
                    first_result = info["entries"][0]
                    f.write(f"{first_result['webpage_url']}\n")

        

    return "success"


def get_token_info():
    token_info = session.get("token_info", None)
    if not token_info:
        raise Exception
    now = int(time.time())
    is_expired = token_info["expires_at"] - now < 60
    if is_expired:
        sp_oauth = get_spotify_oath()
        token_info = sp_oauth.refresh_access_token(token_info["refresh_token"])
    return token_info

def get_spotify_oath():
    print(url_for("redirectPage", _external = True))
    return SpotifyOAuth(
        client_id= clientid,
        client_secret= clientSecret,
        redirect_uri= url_for("redirectPage", _external = True),
        scope= "playlist-read-private"
    )

if __name__ == "__main__":
    app.run(debug=True)

