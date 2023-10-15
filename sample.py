import discord
from discord import app_commands

intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

@client.event
async def on_ready():
    print(f'Logged on as {client.user.name}!')
    await client.change_presence(activity=discord.Game('Loading'))
    await tree.sync()
    print("Ready!")
    await client.change_presence(activity=None)

@tree.command(name='sample', description='sample command')
async def sample(interaction: discord.Interaction):
    await interaction.response.send_message(f"Hello!")

class ListSample(discord.ui.View):
    @discord.ui.select( 
        placeholder = "Pick an item", 
        min_values = 1, 
        max_values = 1, 
        options = [ 
            discord.SelectOption(
                label="1",
                description="item 1"
            ),
            discord.SelectOption(
                label="2",
                description="item 2"
            ),
            discord.SelectOption(
                label="3",
                description="item 3"
            )
        ]
    )
    async def select_callback(self, interaction, select): # https://discordpy.readthedocs.io/en/stable/interactions/api.html#discord.Interaction
        await interaction.response.send_message(f"You picked {select.values[0]}", ephemeral=True)

@tree.command(name='list', description='a list demo')
async def listf(interaction: discord.Interaction):
    await interaction.response.send_message(f"Pick an option", view=ListSample())

@tree.command(name='embed', description='a embed demo')
async def embed(interaction: discord.Interaction):
    embed = discord.Embed(
        title="Sample",
        description="Sample code for embeds",
        color=discord.Color.green()
    )
    embed.set_thumbnail(url=interaction.user.avatar.url)
    embed.add_field(name="Section 1", value='hello')
    embed.add_field(name="Section 2", value='These can have up to 3 sections')
    await interaction.response.send_message(embed=embed)

client.run(input('input bot token: '))