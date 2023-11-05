import dotenv

import io
import os
import time
from typing import Any, Iterator, List
import discord
from discord.ext import commands
import re

from langchain.schema.messages import BaseMessageChunk, BaseMessage

from discordbot import model_manager
from discordbot.memory_manager import get_message_history

dotenv.load_dotenv()
DISCORD_BOT_TOKEN = os.getenv('DISCORD_BOT_TOKEN')
DISCORD_ANNOUNCEMENT_CHANNELS = os.getenv('DISCORD_ANNOUNCEMENT_CHANNELS').split(',') if os.getenv(
    'DISCORD_ANNOUNCEMENT_CHANNELS') else []
DISCORD_ANNOUNCEMENT_CHANNELS = list(map(int, DISCORD_ANNOUNCEMENT_CHANNELS))
DISCORD_ANSWER_CHANNELS = os.getenv('DISCORD_ANSWER_CHANNELS').split(',') if os.getenv(
    'DISCORD_ANSWER_CHANNELS') else []
DISCORD_ANSWER_CHANNELS = list(map(int, DISCORD_ANSWER_CHANNELS))
DISCORD_MESSAGE_UPDATE_INTERVAL = int(os.getenv('DISCORD_MESSAGE_UPDATE_INTERVAL')) if os.getenv(
    'DISCORD_MESSAGE_UPDATE_INTERVAL') else 5
DISCORD_CHAR_LIMIT = int(os.getenv('DISCORD_CHAR_LIMIT')) if os.getenv('DISCORD_CHAR_LIMIT') else 2000
MAX_INFERENCE_DURATION_SECONDS = int(os.getenv('MAX_INFERENCE_DURATION_SECONDS')) \
    if os.getenv('MAX_INFERENCE_DURATION_SECONDS') else 600  # 10 minutes by default

intents = discord.Intents.default()
intents.guilds = True
intents.messages = True

bot = commands.Bot(command_prefix='!', intents=intents)
BOT_TITLE = model_manager.BOT_TITLE


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
                async with channel.typing():
                    startup_announcement = BOT_TITLE + " is starting up...\n"
                    announcement_message = await channel.send(startup_announcement)
                    streaming_llm_response = model_manager.stream('Please announce your presence here in the channel.')
                    await add_response_streaming(announcement_message, streaming_llm_response, startup_announcement)


async def referenced_message_is_from_bot(message):
    channel = message.channel
    if message.reference is None or message.reference.message_id is None:
        return False
    referenced_message_id = message.reference.message_id
    referenced_message = await channel.fetch_message(referenced_message_id)
    return (
        bot.user.mentioned_in(referenced_message)  # this was a reply to a message from the bot
        or referenced_message.author.id == bot.user.id
        # this was a reply to a message towards the bot, so it's an addition
    )


@bot.event
async def on_message(message: discord.message.Message):
    if message.author == bot.user:
        return

    print(f'Received message: {message.content}')

    if not is_supported_channel(message.channel.id):
        return
    if ((bot.user.mentioned_in(message) and message.author.id != bot.user.id)  # Prevent accidental endless reply loop
        or not message.author.bot and await referenced_message_is_from_bot(message)
    ):
        pattern = '((?P<salute>[^@]*)<@.*>)?[^a-zA-Z]*(?P<question>.*)'
        (_, salute, question) = re.search(pattern, message.content).groups()
        if salute is None:
            salute = ''
        response_prefix = f'{salute}<@{message.author.id}>, '
        print(f'extracted question: {question}')
        async with message.channel.typing():
            message_history = await get_message_history(message)
            streaming_llm_response = model_manager.stream(question, message_history)
            answer_message = await message.reply(response_prefix)
            await add_response_streaming(answer_message, streaming_llm_response, response_prefix)


async def add_response_streaming(bot_message: discord.message.Message,
                                 streaming_llm_response: Iterator[BaseMessageChunk],
                                 response_prefix: str) -> Any:
    """

    :param bot_message:
    :param streaming_llm_response:
    """
    message_buffer = io.StringIO()
    message_buffer.write(response_prefix)
    start_time = time.time()
    last_updated_time = start_time
    message_content_len = len(response_prefix)
    for chunk in streaming_llm_response:
        message_buffer.write(str(chunk.content))
        timeout_reached = False
        if (time.time() - start_time) > MAX_INFERENCE_DURATION_SECONDS:
            timeout_reached = True
            message_buffer.write('\nTimeout reached after ' + str(time.time() - start_time) + ' seconds.')
        if (time.time() - last_updated_time) > DISCORD_MESSAGE_UPDATE_INTERVAL:
            last_updated_time = time.time()
            print('updating answer via edit call')
            new_content = message_buffer.getvalue()
            if len(new_content) > DISCORD_CHAR_LIMIT:
                embed = discord.Embed(description=message_buffer.getvalue()[message_content_len:])
                await bot_message.edit(embed=embed)
            else:
                message_content_len = len(new_content)
                await bot_message.edit(content=new_content)
        if timeout_reached:
            break

    if len(message_buffer.getvalue()) > DISCORD_CHAR_LIMIT:
        embed = discord.Embed(description=message_buffer.getvalue()[message_content_len:])
        await bot_message.edit(embed=embed)
    else:
        await bot_message.edit(content=message_buffer.getvalue())
    print('\nDone answering.')


def main():
    bot.run(DISCORD_BOT_TOKEN)


if __name__ == "__main__":
    main()
