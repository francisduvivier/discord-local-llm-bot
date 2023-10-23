import {Client} from "discord.js";
import * as util from "util";
import {channel} from "diagnostics_channel";

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
    client.on("messageCreate", message => {
        if (message.author === client.user) return; // Don't respond to messages sent by the bot itself
        if(isSupportedChannel(message.channelId) && message.content?.includes(client.user!.id)){
            const channel = client.channels.cache.find(channel=>channel.id == message.channelId)!;
            channel.send("hi there! thanks for tagging me, with your message that said `"+message.content+"`")
        }
    });
    await client.login(DISCORD_BOT_TOKEN); // Replace with your bot token
}

startBot();
