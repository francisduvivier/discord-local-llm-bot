import {Client} from "discord.js";

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


async function startBot() {
    client.on("ready", () => {
        console.log(`Logged in as ${client.user?.tag}!`);
        client.channels.cache.forEach((channel) => {
            if (DISCORD_CHANNELS.includes(channel.id)) {
                channel.send("Hello, LLM_PLAYGROUND_CHANNEL! I just started up.");
            }
        });
    });

    client.on("message", (message) => {
        if (message.author === client.user) return; // Don't respond to messages sent by the bot itself

        // Write your message here
        console.log(`Received message: ${message.content}`);
    });
    await client.login(DISCORD_BOT_TOKEN); // Replace with your bot token
}

startBot();
