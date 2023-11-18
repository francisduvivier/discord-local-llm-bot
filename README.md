# Local LLM Discord Bot for Hacker Spaces

![Python](https://img.shields.io/badge/python-3.11+-blue)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Build](https://github.com/francisduvivier/discord-local-llm-bot/actions/workflows/test.yml/badge.svg?branch=master)](https://github.com/francisduvivier/discord-local-llm-bot/actions/workflows/test.yml)
[![codecov](https://codecov.io/gh/francisduvivier/discord-local-llm-bot/branch/master/graph/badge.svg)](https://codecov.io/gh/francisduvivier/discord-local-llm-bot)

## How to use
### Ollama and model
This bot is currently dependent on [ollama](https://github.com/jmorganca/ollama). In order for the bot to work, ollama needs to be running and the configured model needs to be pulled already.

### Required environment variables
The bot can be configured using environment variables, these can also be set by adding a .env file.

#### DISCORD_BOT_TOKEN=your_bot_token
The only thing that is really really required in you environment is the the bot token, this also means that you need to first make a bot by yourself in order to get the token.
I followed this guide for that: https://www.ionos.com/digitalguide/server/know-how/creating-discord-bot/

### Optional environment variables
#### BOT_TITLE=MakerMate, The Maker Space LLM Discord Bot
#### DISCORD_ANNOUNCEMENT_CHANNELS=1163955919164551300
Comma separated list of channels where the bot should announce itself every time that it starts up. If not set, it doesn't announce itself at startup.
#### DISCORD_ANSWER_CHANNELS=
Comma separated list of channels where the bot is allowed to answer. If not set, it will answer in any channel where it has access and is tagged.
#### MODEL=mistral
The ollama model to use. Not that this model already needs to be pulled and that ollama needs to already be running on your system
#### VERBOSE_DEBUG=False
### Commands

```bash
# Install the poetry package manager
pip install poetry
```

```bash
# Install the requirements
poetry install
```

```bash
# test
poetry run python -m pytest
```

```bash
# run the bot
poetry run python discordbot
```

```bash
# Code Coverage
poetry run python -m pytest --cov=discordbot tests --cov-report=html
```

## Features
- Built using the discord and langchain python libraries
- Uses a local large language model by using [ollama](https://github.com/jmorganca/ollama) via [langchain](https://github.com/langchain-ai/langchainjs).
- Answers to messages when it's tagged in one of the allowed channels.
- Posts to a channel when it comes online.
- Streaming output: takes the streaming output of the LLM and then uses the discord edit api to update the message every 5 seconds.
- Configurable via a .env file
- Supports back and forth conversations via replies to messages.

## TODO's
### RAG
- Internet Browsing
- Index Whole Discord channel contents and let LLM search through that in its answers
  - Find content in the discord channel: Hey @bot find message that talk about large language models. 
  - Impersonate Discord users: Hey @bot what would @FrancisD say to this question: ...
- Index the whole Ko-Lab Wiki and allow answering questions about the wiki:
  - Eg. Hey @bot is there an event on the wiki next friday? Or simpler, is there a project about 3D printing?

### Deployment
- Dockerize package
- Deployment using ansible

### Product/Architecture
- Move to MLC-LLM in order to be able to use orange pi.
- Redundancy: use kubernetes for redundancy and rolling upgrades
- Maybe: make this available as a bot that any server can integrate if they provide a openai key.
- Maybe: Provide an api, messages starting with slash should trigger stuff like set temp and set system prompt.


