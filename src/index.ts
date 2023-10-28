import { Client } from "discord.js";
import * as util from "util";
import { getAnswer } from "./langchain-ollama.ts";

const DISCORD_BOT_TOKEN = process.env.DISCORD_BOT_TOKEN;
if (!DISCORD_BOT_TOKEN) {
    throw new Error('DISCORD_BOT_TOKEN needs to be set in environment!');
}

const DISCORD_ANNOUNCEMENT_CHANNELS = process.env.DISCORD_ANNOUNCEMENT_CHANNELS?.split(',');
const DISCORD_ANSWER_CHANNELS = process.env.DISCORD_ANSWER_CHANNELS?.split(',');
console.log('DISCORD_CHANNELS from env', DISCORD_ANNOUNCEMENT_CHANNELS);

const client = new Client({
    intents: ["Guilds",
        "GuildMessages",
        "MessageContent"
    ], // Set the intents for your bot
});


function isSupportedChannel(channelId: string) {
    if (!DISCORD_ANSWER_CHANNELS) {
        return true;
    }
    return DISCORD_ANSWER_CHANNELS.includes(channelId);
}

async function startBot() {
    client.on("ready", () => {
        console.log(`Logged in as ${client.user?.tag}!`);
        console.log('client.user', util.inspect(client.user));

        client.channels.cache.forEach(async (channel) => {
            if (DISCORD_ANNOUNCEMENT_CHANNELS?.includes(channel.id)) {
                const message = await channel.send("Hello, LLM_PLAYGROUND_CHANNEL! I just started up.");
                message.edit('Hello, LLM_PLAYGROUND_CHANNEL! I just started up. I can edit messages.')

            }
        });
    });

    client.on("message", (message) => {
        if (message.author === client.user) return; // Don't respond to messages sent by the bot itself
        console.log(`Received message: ${message.content}`);

        // Write your message here
    });
    client.on("messageCreate", async message => {
        if (message.author === client.user) return; // Don't respond to messages sent by the bot itself
        if (!isSupportedChannel(message.channelId)) return; // Don't respond to messages sent by the bot itself
        const botId = client.user!.id;
        const mentionedBotId = message.mentions.users.has(botId);
        const messageContent = message.content;
        const messageMatch = messageContent?.match(`.*@[^>]+>[^a-zA-Z]*(?<question>.*)`);

        console.log(`message received: ${messageContent}`);
        if (mentionedBotId && messageMatch?.groups) {
            const question = messageMatch.groups.question
            console.log(`extracted question: ${question}`);
            // Reply to the message
            let reply = `Hi ${message.author.username}, `;
            let answerMessage = await message.reply(reply);
            let currentReplyMessage = reply;
            let busy = false;
            let finished = false;
            const answer = await getAnswer(question, async (token: string) => {

                reply += token;
                if (busy) return;
                busy = true;
                try {
                    while (currentReplyMessage !== reply || finished) {
                        currentReplyMessage = reply;
                        while (currentReplyMessage.length + 4 > 2000) {
                            await answerMessage.edit(currentReplyMessage.slice(0, 2000));
                            reply = currentReplyMessage.slice(2000);
                            currentReplyMessage = reply;
                            answerMessage = await message.reply(currentReplyMessage.slice(0, 1996) + ' <->');
                        }
                        await answerMessage.edit(currentReplyMessage + (finished ? '' : ' <->'));
                        await new Promise((resolve) => setTimeout(resolve, 5000));
                    }
                } finally {
                    busy = false;
                }
            });
            finished = true;
        }
    });
    await client.login(DISCORD_BOT_TOKEN); // Replace with your bot token
}

startBot();
