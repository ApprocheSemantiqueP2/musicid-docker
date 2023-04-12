import os
from ast import literal_eval

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from lyricsgenius import Genius

import openai

from neo4j import GraphDatabase

openai.api_key = "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"

username = os.environ["SPOTIFY_USERNAME"]
cid = os.environ["SPOTIFY_CID"]
secret = os.environ["SPOTIFY_SECRET"]
token = os.environ["GENIUS_TOKEN"]


client_credentials_manager = SpotifyClientCredentials(
    client_id=cid, client_secret=secret
)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

genius = Genius(token)


def get_song_lyrics(g, name):
    search = g.search_song(name)

    if search is not None:
        return search.lyrics


class LyricsThemeExtractor:
    def __init__(self):
        self.system_prompt = """"
        Tu es un assistant textuel qui extrait les thèmes en un seul mot correspondants aux paroles d'une chanson mot par mot, les extrayant dans une liste python au format suivant: ["<theme1>", "<theme2>", ...].
        Retourne moi seulement la liste, aucun texte autour sinon c'est invalide.
        Extrait le plus de thèmes possible.
        Essaye de te restreindre aux thèmes suivants: ["Amitié", "Amour", "Amusement", "Animosité", "Argent", "Armes", "Drogue", "Energie", "Epreuve", "Fantasy", "Histoire", "Joie", "Peine", "Religion", "Trahison"] mais tu peux en rajouter si besoin.
        """

    def get_themes(self, paroles, max_retries=3):
        user_prompt = f'Extrait les themes EN FRANÇAIS SEULEMENT des paroles suivantes en UN SEUL MOT sinon invalide "{paroles}"'
        res = None
        retries = 0

        while res == None and retries < max_retries:
            try:
                completion = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": self.system_prompt},
                        {"role": "user", "content": user_prompt},
                    ],
                )
                res = literal_eval(completion["choices"][0]["message"]["content"])
            except:
                retries += 1

        return res


extractor = LyricsThemeExtractor()

driver = GraphDatabase.driver("bolt://neo4j:7687/", auth=("neo4j", "adminadmin"))
