import discord
from discord.ext import commands
import youtube_dl
import requests
import json

# Discord bot token
TOKEN = 'YOUR_DISCORD_BOT_TOKEN'


# Twitch API credentials
TWITCH_CLIENT_ID = 'YOUR_TWITCH_CLIENT_ID'
TWITCH_CLIENT_SECRET = 'YOUR_TWITCH_CLIENT_SECRET'

# YouTube API credentials
YOUTUBE_API_KEY = 'YOUR_YOUTUBE_API_KEY'

# Streamer's Twitch channel name
STREAMER_CHANNEL = 'YOUR_STREAMER_CHANNEL'

# YouTube channel ID
YOUTUBE_CHANNEL_ID = 'YOUR_YOUTUBE_CHANNEL_ID'

# Discord channel ID where the bot will send messages
DISCORD_CHANNEL_ID = 'YOUR_DISCORD_CHANNEL_ID'


bot = commands.Bot(command_prefix='!')


@bot.event
async def on_ready():
    print(f'{bot.user} está conectado !')


# Twitch API request to check if the streamer is live
def is_streamer_live():
    headers = {
        'Client-ID': TWITCH_CLIENT_ID,
        'Authorization': f'Bearer {TWITCH_CLIENT_SECRET}'
    }

    response = requests.get(f'https://api.twitch.tv/helix/streams?user_login={STREAMER_CHANNEL}', headers=headers)
    data = json.loads(response.text)

    if data['data']:
        return True
    else:
        return False

# YouTube API request to check for new videos
def get_new_videos():
    response = requests.get(f'https://www.googleapis.com/youtube/v3/search?part=id,snippet&channelId={YOUTUBE_CHANNEL_ID}&order=date&maxResults=1&key={YOUTUBE_API_KEY}')
    data = json.loads(response.text)

    if data['items']:
        video_id = data['items'][0]['id']['videoId']
        video_title = data['items'][0]['snippet']['title']
        return video_id, video_title
    else:
        return None, None

# Check if the video is watchable (not a premier video)
def is_video_watchable(video_id):
    response = requests.get(f'https://www.googleapis.com/youtube/v3/videos?part=status&id={video_id}&key={YOUTUBE_API_KEY}')
    data = json.loads(response.text)
    if data['items'][0]['status']['privacyStatus'] == 'public':
        return True
    else:
        return False


# Send a message in Discord when the streamer is live on Twitch
@bot.event
async def on_streamer_live():
    channel = bot.get_channel(int(DISCORD_CHANNEL_ID))
    await channel.send(f'{STREAMER_CHANNEL} is live on Twitch!')

# Send a message in Discord when a new YouTube video is posted
@bot.event
async def on_new_video(video_id, video_title):
    channel = bot.get_channel(int(DISCORD_CHANNEL_ID))
    await channel.send(f'New video posted by {YOUTUBE_CHANNEL_ID}: {video_title} ({video_id})')


# Check for new videos and send a message if a new video is posted
async def check_for_new_videos():
    video_id, video_title = get_new_videos()
    if video_id and video_title:
        if is_video_watchable(video_id):
            await on_new_video(video_id, video_title)

# Check if the streamer is live and send a message if they are

async def check_for_streamer_live():
    if is_streamer_live():
        await on_streamer_live()

# Run the bot
bot.loop.create_task(check_for_new_videos())
bot.loop.create_task(check_for_streamer_live())

bot.run(TOKEN)