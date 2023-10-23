# discord-llm-bot
connect-and-send-message

To install dependencies:

```bash
bun install
```

To run:

```bash
bun run index.ts
```
## TODO's
### Chatty
- Streaming output: Add a callback manager to ollama and then add a setCallBackReceiverMethod that then get's called every time there is an update. Or refactor so taht the getAnwser returns an iterator and then interate over the answer and use .edit to update the message.
- Answer to messages instead of create an unrelated message.
- Provide the sender in the question to the llm and provide a system prompt to inform that it is now the KO-LAB LLM Discord bot.
- provide an api, messages starting with slash should trigger stuff like set temp and set system prompt.

### RAG
- Index Whole discord channel contents and let LLM search through that in it's answers 
- Index the whole Wiki and allow answering questions about the wiki: eg, hey is there an event on the wiki next friday? Or simpler, is there a project about 3D printing?

This project was created using `bun init` in bun v1.0.1. [Bun](https://bun.sh) is a fast all-in-one JavaScript runtime.
