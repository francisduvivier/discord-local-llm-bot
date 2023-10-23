import {Client} from "discord.js";

const client = new Client({
    intents: ["Guilds", "DirectMessages", "GuildMessages"], // Set the intents for your bot
});


async function startBot() {
    client.on("ready", () => {
        console.log(`Logged in as ${client.user?.tag}!`);
    });

    client.on("message", (message) => {
        if (message.author === client.user) return; // Don't respond to messages sent by the bot itself

        // Write your message here
        console.log(`Received message: ${message.content}`);
    });
    await client.login("MTE2Mzk1MTkwMDg0NTE2MjU4Ng.GHlJ0g.ffW2c6LAQYZzxBqaAb2cpBIu7FsNMrEe0-Ptfs"); // Replace with your bot token
}

startBot();
