import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
from ollama import get_answer
import re

load_dotenv()
DISCORD_BOT_TOKEN = os.getenv('DISCORD_BOT_TOKEN')
DISCORD_ANNOUNCEMENT_CHANNELS = os.getenv('DISCORD_ANNOUNCEMENT_CHANNELS').split(',') if os.getenv('DISCORD_ANNOUNCEMENT_CHANNELS') else []
DISCORD_ANNOUNCEMENT_CHANNELS = list(map(int, DISCORD_ANNOUNCEMENT_CHANNELS))
DISCORD_ANSWER_CHANNELS = os.getenv('DISCORD_ANSWER_CHANNELS').split(',') if os.getenv('DISCORD_ANSWER_CHANNELS') else []
DISCORD_ANSWER_CHANNELS = list(map(int, DISCORD_ANSWER_CHANNELS))

intents = discord.Intents.default()
intents.guilds = True
intents.messages = True

bot = commands.Bot(command_prefix='!', intents=intents)

def is_supported_channel(channel_id):
    if len(DISCORD_ANSWER_CHANNELS) == 0:
        # Allow all channels if the channel list is empty
        return True
    return channel_id in DISCORD_ANSWER_CHANNELS

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}!')
    for guild in bot.guilds:
        for channel in guild.channels:
            if channel.id in DISCORD_ANNOUNCEMENT_CHANNELS:
                message = await channel.send("Hello, LLM_PLAYGROUND_CHANNEL! I just started up.")
                await message.edit(content='Hello, LLM_PLAYGROUND_CHANNEL! I just started up. I can edit messages.')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    print(f'Received message: {message.content}')

    if not is_supported_channel(message.channel.id):
        return

    if bot.user.mentioned_in(message):
        pattern = '(?P<salute>[^@]*)<@.*>[^a-zA-Z]*(?P<question>.*)'
        (salute, question)  = re.search(pattern, message.content).groups()

        print(f'extracted question: {question}')
        start_reply = f'{salute}<@{message.author.id}>, '
        answer_message = await message.reply(start_reply)
        llm_answer = get_answer(question)
        await answer_message.edit(content=start_reply+llm_answer)

bot.run(DISCORD_BOT_TOKEN)
