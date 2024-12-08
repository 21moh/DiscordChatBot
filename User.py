import nextcord
from nextcord.ext import commands
from decouple import config
from openai import OpenAI
import os


client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"), 
)



class User(commands.Cog):
    def __init__(self, client) -> None:
        self.client = client

    # for the message
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author==self.client.user:
            return
        if self.client.user in message.mentions:
            completion = client.chat.completions.create(
                messages=[
                    {"role": "system", "content": "You are a helpful discord application assistant."},
                    {
                        "role": "user",
                        "content": message.content
                    }
                ],
                model="gpt-3.5-turbo",
            )
            await message.reply(completion.choices[0].message.content) #message.content
        else:
            return

def setup(client):
    client.add_cog(User(client))


# openAI API Key: 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
