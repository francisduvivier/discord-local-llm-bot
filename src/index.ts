import { Client } from "discord.js";
import * as util from "util";
import { channel } from "diagnostics_channel";
import { getAnswer } from "./langchain-ollama.ts";

const DISCORD_BOT_TOKEN = process.env.DISCORD_BOT_TOKEN;
if (!DISCORD_BOT_TOKEN) {
    throw new Error('DISCORD_BOT_TOKEN needs to be set in environment!');
}

const DISCORD_CHANNELS = process.env.DISCORD_CHANNELS?.split(',') ?? [];
console.log('DISCORD_CHANNELS from env', DISCORD_CHANNELS);

const client = new Client({
    intents: ["Guilds",
        "GuildMessages",
        "MessageContent"
    ], // Set the intents for your bot
});


function isSupportedChannel(channelId: string) {
    return DISCORD_CHANNELS.includes(channelId);
}

async function startBot() {
    client.on("ready", () => {
        console.log(`Logged in as ${client.user?.tag}!`);
        console.log('client.user', util.inspect(client.user));

        client.channels.cache.forEach((channel) => {
            if (isSupportedChannel(channel.id)) {
                channel.send("Hello, LLM_PLAYGROUND_CHANNEL! I just started up.");
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
            const answerMessage = await message.reply(reply);
            let busy = false;
            const answer = getAnswer(question, async (token: string) => {
                reply += token;
                if (busy) return;
                busy = true;
                try {
                    await answerMessage.edit(reply)
                } finally {
                    busy = false;
                }
            });
            const channel = client.channels.cache.find(channel => channel.id == message.channelId)!;
            await channel.send(answer);
        }
    });
    await client.login(DISCORD_BOT_TOKEN); // Replace with your bot token
}

startBot();
