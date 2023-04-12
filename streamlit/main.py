import streamlit as st
from spotify import sp, genius, get_song_lyrics, extractor, driver

from PIL import Image
import requests
from io import BytesIO

st.title("MusicID")

test = st.text_input("URI Spotify", placeholder="Entrez votre choix...", key="uri_key")


def handle_button(artist, track, lyrics, themes):
    query = "CREATE (a:ns1__Artiste {ns1__Nom: $artist_name})-[:ns1__aSortie]->(m:ns1__music {ns1__songname: $name, ns1__BPM: $bpm, ns1__Duration: $dur, ns1__Contenu: $paroles}), (m)-[:aPourCreateur]->(a)"

    with driver.session(database="neo4j") as session:
        session.run(
            query,
            artist_name=artist["name"],
            name=track["name"],
            bpm=track["tempo"],
            dur=track["duration_ms"],
            paroles=lyrics,
        )


if st.session_state["uri_key"]:
    with st.spinner("Chargement..."):
        features = sp.audio_features(st.session_state["uri_key"])

        track = sp.track(st.session_state["uri_key"])

        if len(features) > 0:
            track = track | features[0]

        fullname = f"{track['artists'][0]['name']} - {track['name']}"

        lyrics = get_song_lyrics(genius, fullname)

        img_bytes = requests.get(track["album"]["images"][0]["url"])
        img = Image.open(BytesIO(img_bytes.content))

        st.header(fullname, anchor=False)
        st.image(img, width=125)

        themes = extractor.get_themes(lyrics)

    st.button(
        "Ajouter aux graphes",
        on_click=handle_button,
        args=[track["artists"][0], track, lyrics, themes],
    )

    tab_lyrics, tab_themes = st.tabs(["Paroles", "Themes"])

    with tab_lyrics:
        st.text(lyrics)
    with tab_themes:
        container = st.container()
        st.write(themes)
