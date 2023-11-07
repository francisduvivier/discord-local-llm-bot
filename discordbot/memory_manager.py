from typing import List

import discord
from langchain.schema import BaseMessage, HumanMessage, AIMessage


async def get_message_history(message: discord.Message) -> List[BaseMessage]:
    messages: List[BaseMessage] = []
    current_message = message

    while current_message.reference:
        referenced_message_id = current_message.reference.message_id
        channel = current_message.channel
        referenced_message = await channel.fetch_message(referenced_message_id)
        message_content = referenced_message.clean_content
        for embed in referenced_message.embeds:
            message_content += embed.description
        if referenced_message.author.bot:
            messages.append(AIMessage(content=message_content))
        else:
            messages.append(HumanMessage(content=message_content))
        current_message = referenced_message

    # Last appended messages should be first in the list since they are the oldest
    messages.reverse()
    return messages
