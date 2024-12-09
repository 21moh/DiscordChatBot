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

    # Listen for messages
    @commands.Cog.listener()
    async def on_message(self, message):
        # Avoid responding to the bot's own messages
        if message.author == self.client.user:
            return
        
        # Check if the message is sent via DM
        if isinstance(message.channel, nextcord.DMChannel):
            try:
                # Use OpenAI API to generate a response
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
                await message.channel.send(completion.choices[0].message.content)
            except Exception as e:
            # Handle any errors
                await message.channel.send("Something went wrong. Please try again later.")
                print(f"Error: {e}")

        else: 
            if self.client.user in message.mentions:
                try:
                    # Use OpenAI API to generate a response
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

                    # Send the response as a DM to the user
                    response = "Query: " + message.content + "\n\n" + completion.choices[0].message.content
                    await message.author.send(response)
                    # Optionally notify in the channel that the user received a DM
                    await message.reply("I've sent you a DM with the response!")
                except nextcord.Forbidden:
                    # Handle the case where DMs are blocked by the user
                    await message.reply("I couldn't send you a DM. Please check your privacy settings.")
            else:
                return

def setup(client):
    client.add_cog(User(client))



