import discord
from discord.ext import commands
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import requests
import re

ints = discord.Intents.all()

spotify = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id='SPOTIFY_ID',
                                                    client_secret='SPOTIFY_SECRET',
                                                    redirect_uri='http://localhost:8888/callback',
                                                    ))


def run_bot():

    token = 'DISCORD_TOKEN'
    bot = commands.Bot(command_prefix='!', intents=ints, permissions=274877959168)
    name = 'Link Viewer'

    @bot.event
    async def on_ready():
        print(f'Logged in as {name}!')

    @bot.event
    async def on_message(message):
        if message.author == bot.user:
            return
        if 'https://spotify.link' in message.content:
            pattern = r'https://\S+'
            short_link = re.findall(pattern, message.content)
            r = requests.head(short_link[0], allow_redirects=True)
            link = r.url
            track_id = link.split('open_spotify.com/track/*?')[0].split('/track/')[1].split('?')[0]
            spotify_uri = f'spotify:track:{track_id}'
            track = spotify.track(spotify_uri)

            image_url = f'{track["album"]["images"][0]["url"]}'
            embed = discord.Embed()
            embed_img = embed.set_image(url=image_url)

            await message.channel.send(f'Song: `{track["name"]}`\n'
                                       f'Artist: `{track["artists"][0]["name"]}`\n\n',
                                       embed=embed_img)

    bot.run(token)
