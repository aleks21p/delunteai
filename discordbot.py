import discord
import ollama

TOKEN = "[REDACTED_TOKEN]"

system_prompt = "Your name is Delunte. Give short simple answers."

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    response = ollama.chat(
        model='llama3',
        messages=[
            {'role': 'system', 'content': system_prompt},
            {'role': 'user', 'content': message.content}
        ]
    )

    await message.channel.send(response['message']['content'])

client.run(TOKEN)
