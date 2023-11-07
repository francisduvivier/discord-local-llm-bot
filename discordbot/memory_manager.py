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
        if current_message.author.bot:
            messages.append(AIMessage(content=referenced_message.content))
        else:
            messages.append(HumanMessage(content=referenced_message.content))
        current_message = referenced_message

    return messages
