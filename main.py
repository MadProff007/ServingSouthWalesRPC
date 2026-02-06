## LIBRARIES
import discord
from discord.ext import commands
from discord import app_commands

class Client(commands.Bot):
    async def on_ready(self):
        print(f'Logged on as {self.user}!')
        try:
            guild = discord.Object(id=1461845376897388557)
            synced = await self.tree.sync(guild=guild)
            print(f'Synced {len(synced)} commands to guild {guild.id}')
            
        except exception as e:
            print(f'Error syncing commands: {e}')

    async def on_message(self, message):
        print(f'Message from {message.author}: {message.content}')


intents = discord.Intents.default()
intents.message_content = True
client = Client(command_prefix="!", intents=intents)

## / COMMANDS
GUILD_ID = discord.Object(id=1461845376897388557)
@client.tree.command(name="hello", description="Say Hello!", guild=GUILD_ID)
async def sayHello(interaction: discord.Interaction):
    await interaction.response.send_message("Hello there!")

@client.tree.command(name="printer", description="Print what you give me!", guild=GUILD_ID)
async def printer(interaction: discord.Interaction, printer: str):
    await interaction.response.send_message(printer)

### FORMAT
#@client.tree.command(name="xyz", description="xyz", guild=GUILD_ID)
#async def name(interaction: discord.Interaction):
#    await interaction.response.send_message(name or response)

## EMBEDS
@client.tree.command(name="welcome", description="Welcome Info", guild=GUILD_ID)
async def printer(interaction: discord.Interaction):
    welcome = discord.Embed(title="Welcome to Serving South Wales RPC", description="Thank you for joining us. We are a FiveM Community based on creating a realistic RPC based on South Wales services, run by those with the knowledge of South Wales and its services.", colour=discord.Color.blue())
    welcome.add_field(name="Title 1", value="Field 1", inline="false")
    welcome.add_field()
    await interaction.response.send_message(embed=welcome)

### FORMAT
#@client.tree.command(name="embed", description="EMBED DEMO", guild=GUILD_ID)
#async def printer(interaction: discord.Interaction):
#    embed = discord.Embed(title="Test Title", description="Test Description")
#    await interaction.response.send_message(embed=embed)
## ID's
client.run('MTQ2ODM3Mjc1MjQ3NzA2MTE5Mg.G-Cnrb.n8CvJNmw_70dfmcUdihyIQrDZD0JSX6LyzPyMY')
