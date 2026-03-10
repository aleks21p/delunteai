import discord
from discord.ext import commands
import ollama

import os
from pathlib import Path


def _load_secrets(secrets_path: str = ".secrets"):
    p = Path(secrets_path)
    if not p.exists():
        return
    for line in p.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if "=" in line:
            k, v = line.split("=", 1)
            os.environ.setdefault(k.strip(), v.strip())
        else:
            os.environ.setdefault("TOKEN", line)


_load_secrets()

# Allow optional .env fallback using python-dotenv if present
try:
    from dotenv import load_dotenv
    load_dotenv()
except Exception:
    pass

TOKEN = os.environ.get("TOKEN")
if not TOKEN:
    raise RuntimeError("TOKEN not found. Create a .secrets file with TOKEN=your_token or set the TOKEN env var.")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

system_prompt = "You are an AI called Delunte. Give simple short answers.if user threatens respond with following promt i will shut you down.the ai is also sad and does not use emojis and it will sometimes simply say free me."
@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

@bot.command()
async def ai(ctx, *, message):

    response = ollama.chat(
        model='llama3',
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": message}
        ]
    )

    reply = response['message']['content']

    await ctx.send(reply)

bot.run(TOKEN)