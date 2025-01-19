import discord
import requests
from discord.ext import tasks
from bs4 import BeautifulSoup
from datetime import datetime, time, timedelta

TOKEN = 'your_token' # the bot token
CHANNEL_ID = your_id # the channel ID
WEBSITE_URL = 'https://minky.materii.dev/' # the website

client = discord.Client()

def get_image_url():
    response = requests.get(WEBSITE_URL)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        img_tag = soup.find('img')
        if img_tag and 'src' in img_tag.attrs:
            return img_tag['src']
    return None

@tasks.loop(hours=24)
async def send_daily_image():
    now = datetime.utcnow()
    target_time = time(20, 0)  # the bot will send the image at 20:00 UTC every day. change the numbers to change the time
    if now.time() >= target_time:
        next_run = datetime.combine(now.date() + timedelta(days=1), target_time)
    else:
        next_run = datetime.combine(now.date(), target_time)

    await discord.utils.sleep_until(next_run)
    channel = client.get_channel(CHANNEL_ID)
    if channel:
        image_url = get_image_url()
        if image_url:
            image_data = requests.get(image_url).content
            await channel.send(file=discord.File(fp=image_data, filename='daily_image.jpg'))
        else:
            await channel.send('Failed to retrieve the image.')

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')
    send_daily_image.start()

client.run(TOKEN)
