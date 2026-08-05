# bot.py
import os
import asyncio
from dotenv import load_dotenv
import discord
from discord import app_commands
from agent import run_agent  # <- your existing agent

load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True  # enable in Dev Portal too

class AgentClient(discord.Client):
    def __init__(self):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        await self.tree.sync()

client = AgentClient()

# ---- NEW: per-channel memory store ----
conversation_history: dict[int, list] = {}

def _call_agent_with_history(prompt: str, channel_id: int) -> str:
    # Load this channel's history into the agent's in-memory buffer
    run_agent._history = conversation_history.get(channel_id, [])
    # DEBUG: show history before call
    print(f"[bot] channel={channel_id} history_in={len(run_agent._history)}")
    reply = run_agent(prompt, verbose=False)  # turn on verbose in agent for now
    # Save updated history back for this channel
    conversation_history[channel_id] = getattr(run_agent, "_history", [])
    # DEBUG: show history after call
    print(f"[bot] channel={channel_id} history_out={len(conversation_history[channel_id])}")
    return reply
# --------------------------------------

def _chunks(text: str, size: int = 2000):
    while text:
        yield text[:size]
        text = text[size:]

@client.tree.command(name="ask", description="Ask the AI agent")
@app_commands.describe(prompt="Your question or instruction")
async def ask(interaction: discord.Interaction, prompt: str):
    await interaction.response.defer(thinking=True)
    loop = asyncio.get_running_loop()
    channel_id = interaction.channel_id
    reply = await loop.run_in_executor(None, _call_agent_with_history, prompt, channel_id)
    reply = reply or "(empty response)"
    for chunk in _chunks(reply, 2000):
        await interaction.followup.send(chunk)

# ---- NEW: /reset to clear channel memory ----
@client.tree.command(name="reset", description="Clear this channel's conversation memory")
async def reset(interaction: discord.Interaction):
    conversation_history.pop(interaction.channel_id, None)
    # also clear the agent's global cache to be safe
    run_agent._history = []
    await interaction.response.send_message("🧹 Memory cleared for this channel.", ephemeral=True)
# --------------------------------------------

@client.event
async def on_message(message: discord.Message):
    if message.author.bot:
        return
    if client.user in message.mentions:
        # handle <@123> and <@!123>
        mention_plain = f"<@{client.user.id}>"
        mention_bang  = f"<@!{client.user.id}>"
        prompt = (message.content.replace(mention_plain, "")
                                .replace(mention_bang, "")
                                .strip())
        if not prompt:
            return await message.reply("Tag me *and* say something 😅")
        loop = asyncio.get_running_loop()
        channel_id = message.channel.id
        reply = await loop.run_in_executor(None, _call_agent_with_history, prompt, channel_id)
        reply = reply or "(empty response)"
        for chunk in _chunks(reply, 2000):
            await message.reply(chunk)


if __name__ == "__main__":
    if not DISCORD_TOKEN:
        raise SystemExit("DISCORD_TOKEN not set in environment.")
    client.run(DISCORD_TOKEN)
