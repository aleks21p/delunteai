import discord
from discord.ext import commands
import ollama

TOKEN = "[REDACTED_TOKEN]"

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