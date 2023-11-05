# Local LLM Discord Bot for Hacker Spaces

![Python](https://img.shields.io/badge/python-3.11+-blue)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Build](https://github.com/francisduvivier/discord-local-llm-bot/actions/workflows/test.yml/badge.svg?branch=master)](https://github.com/francisduvivier/discord-local-llm-bot/actions/workflows/test.yml)
[![codecov](https://codecov.io/gh/francisduvivier/discord-local-llm-bot/branch/master/graph/badge.svg)](https://codecov.io/gh/francisduvivier/discord-local-llm-bot)

### Commands

```bash
# Build and Install (local)
pip install -e .
```

```bash
python -m pytest
```

```bash
# Code Coverage
python -m pytest --cov=discordbot tests --cov-report=html
```

## Features
- Built using discordjs and langchain.js
- Uses a local large language model by using [ollama](https://github.com/jmorganca/ollama) via [langchain](https://github.com/langchain-ai/langchainjs).
- Answers to messages when it's tagged in one of the allowed channels.
- Posts to a channel when it comes online.
- Streaming output: takes the streaming output of the LLM and then used the discord edit api to update the message every 5 seconds.

## TODO's
### Language
- Move to Python: Discord.js typing and documentation sucks and everything related to data and AI is better in Python, so first priority is to refactor to Python.
### Chatty
- Token output limit to avoid endless response.
- Provide the sender in the question to the llm and provide a system prompt to inform that it is now the KO-LAB LLM Discord bot.
- Back and forth conversations
- Maybe: Move to orange pi using MLC-AI
  - Remove Ollama depenency
- Maybe: Provide an api, messages starting with slash should trigger stuff like set temp and set system prompt.

### RAG
- Internet Browsing
- Index Whole Discord channel contents and let LLM search through that in it's answers
  - Find content in the discord channel: Hey @bot find message that talk about large language models. 
  - Impersonate Discord users: Hey @bot what would @FrancisD say to this question: ...
- Index the whole Ko-Lab Wiki and allow answering questions about the wiki:
  - Eg. Hey @bot is there an event on the wiki next friday? Or simpler, is there a project about 3D printing?
