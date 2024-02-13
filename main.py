import os
try:
    import discord, sys, asyncio, shelve, oyaml, json, atexit, glob, filecmp, requests, os.path, shutil, datetime, platform
    from discord.utils import get
    from discord import app_commands, Interaction
    from pyprobs import Probability as pr
    import random as rand
    from typing import Literal
    from discord.app_commands import AppCommandError
    from googletrans import Translator
    translator = Translator()
except ModuleNotFoundError:
    print('not all packages have been installed')
print('Loading intents and discord client')
intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = discord.app_commands.CommandTree(client)
try:
    with open("private.yml", "r") as f:
        private = oyaml.safe_load(f)
except:
    try:
        with open("/private.yml", "r") as f:
            private = oyaml.safe_load(f)
    except:
        print('Cant load private file')
        raise AttributeError('Cant find private file')
def ifemptycreate(dict, var, value = {}):
    # Create the var if it does not exist
    if not var in dict:
        dict[var] = value
        return True
    return False
print('Loading stats')
statsdefvars = {'scores': {}, 'item': {'laptop': {}, 'shovel': {}}, 'usersettings': {}}
try:
    with open("stats.json", "r") as f:
        stats = json.load(f)
    for key, value in statsdefvars.items():
        if ifemptycreate(stats, key, value):
            print('Created ' + key)
        if isinstance(value, dict):
            for key2, value2 in value.items():
                if ifemptycreate(stats[key], key2, value2):
                    print('Created ' + key + '.' + key2)
except FileNotFoundError:
    print('Creating stats file')
    stats = statsdefvars
    with open("stats.json", "w") as f:
        json.dump(stats , f, sort_keys=False, indent=4)
    with open("stats.json", "r") as f:
        stats = json.load(f)
    if os.path.isfile('points.dir'):
        print('Legacy points found, items will not be moved')
        legacy = shelve.open("points") 
        print(legacy)
        for key, value in legacy.items():
            stats['scores'][key] = value
            print('Moved ' + str(key) + ': ' + str(value))
        os.remove("points.dir")
        print('Points moved, old scores have been deleted.')
global loaded
loaded = False
global langmsg
langmsg = {}
sys.path.insert(1, '/')
from base import uwu, num
# generic commands

@client.event
async def on_ready():
    print(f'Logged on as {client.user.name}, attempting to sync commands')
    await client.change_presence(activity=discord.Game('Loading'))
    await tree.sync()
    print("Commands synced, you may need to wait up to an hour for commands to appear in your server.")
    loaded = True
    if platform.node() == 'agbdocker':
        await client.change_presence(activity=discord.Game(f'in {len(client.guilds)} servers'))
    else:
        await client.change_presence(activity=discord.Game('in test mode'))
    while True:
        backupres = await backupstats()
        if not backupres == False:
            print('Backup created')
            await asyncio.sleep(600)
        else:
            await asyncio.sleep(300)

async def backupstats():
    with open("stats.json", "w") as f:
        json.dump(stats, f, sort_keys=False, indent=4)
    newpath = r'backup' 
    if not os.path.exists(newpath):
        os.makedirs(newpath)
    else:
        search_dir = "backup/"
        files = list(filter(os.path.isfile, glob.glob(search_dir + "*")))
        files.sort(key=lambda x: os.path.getmtime(x))
        if filecmp.cmp('stats.json', files[-1]):
            print('No need to backup, files are the same')
            return False
    print('Sorting scores')
    try:
        stats['leadupdate']
    except:
        stats['leadupdate'] = 'Please wait'
    if not stats['leadupdate'] == 'Currently updating (scores may not be accurate)':
        stats['leadupdate'] = 'Currently updating (scores may not be accurate)'
        #sort scores
        sorted_scores = sorted(stats['scores'].items(), key=lambda item: item[1], reverse=True)
        stats['scores'] = {}
        for k, v in sorted_scores:
            stats['scores'][k] = v
        #set last update
        stats['leadupdate'] = round((datetime.datetime.now(datetime.timezone.utc) - datetime.datetime(1970, 1, 1, tzinfo=datetime.timezone.utc)).total_seconds())
        with open("stats.json", "w") as f:
            json.dump(stats, f, sort_keys=False, indent=4)
    else:
        print('Leaderboard update seems to already be running')
    with open("stats.json", "w") as f:
        json.dump(stats, f, sort_keys=False, indent=4)
    date = datetime.datetime.today().strftime('%Y-%m-%d %H.%M.%S')
    backuploc = f'backup/automatic {date}.json'
    shutil.copy2('stats.json', backuploc)
    print('Backup created (automatic)')
    return backuploc

@client.event
async def on_message(message):
    if not message.author.bot:
        if pr.prob(3/10):
            if pr.prob(9/10):
                print('giving point to ' + message.author.name)
                try:
                    score = stats['scores'][str(message.author.id)]
                except:
                    score = 0
                stats['scores'][str(message.author.id)] = score + 1
            else:
                print('giving 10 points to ' + message.author.name)
                try:
                    score = stats['scores'][str(message.author.id)]
                except:
                    score = 0
                stats['scores'][str(message.author.id)] = score + 10
    if f'{message.guild}' == 'None':
        if not {message.author} == {client.user}:
            if message.content == ':newspaper:' or message.content == '<a:RPS_paper:1175245811282628628>' or message.content == '📰' or message.content == '📄' or message.content == '🪨' or message.content == '<a:RPS_rock:1175245831398510704>' or message.content == ':rock:' or message.content == '✂️' or message.content == '<a:RPS_scissors:1175245784380346549>' or message.content == ':scissors:':
                rpscore = rand.randrange(1,4)
                if rpscore == 1:
                    await message.channel.send('✂️')
                elif rpscore == 2:
                    await message.channel.send('📄')
                elif rpscore == 3:
                    await message.channel.send('🪨')
            elif not message.content == '3' and not message.content == '2' and not message.content == '1' and not message.content == 'rps' and not message.content == 'rock paper scissors':
                async with message.channel.typing():
                    await asyncio.sleep(3)
                await message.channel.send(f'Not a valid command, please use slash commands', reference=message)
    if f'<@{client.user.id}>' in message.content:
        if not message.guild == None:
            if not message.author.bot:
                async with message.channel.typing():
                    await asyncio.sleep(2)
                await message.channel.send('Please use slash commands', reference=message)

@tree.error
async def cooldown(interaction: discord.Interaction, error: app_commands.AppCommandError):
    if isinstance(error, app_commands.CommandOnCooldown):
        embed = discord.Embed(
            title="Slow down!",
            description=f"Please wait {str(round(error.retry_after))} seconds to use {interaction.command.name} again",
            color=discord.Color.red()
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)

@tree.command(name = "about", description = f"About the bot")
async def aboutbot(interaction: discord.Interaction):
        embed = discord.Embed(
            title="About",
            description=f"About {client.user.name}",
            color=discord.Color.green(),
        )
        lan = str(interaction.locale)[:2]
        try:
            if not lan == 'en':
                text = 'Your language is not available'
                translation = translator.translate(text, dest=lan)
                embed.add_field(name='⚠️', value=translation.text, inline=False)
        except ValueError:
            embed.add_field(name='⚠️', value='Your language may not be supported', inline=False)
        embed.set_thumbnail(url=client.user.avatar.url)
        leaderboard = list(stats['scores'].keys())
        top = await client.fetch_user(leaderboard[0])
        embed.add_field(name="Top user", value=top.name, inline=True)
        embed.add_field(name="User count", value=await num(len(stats['scores'])), inline=True)
        embed.add_field(name="About", value='This bot is based on AGB, which is a bot made by trwy, and was made fully in python', inline=False)
        view = discord.ui.View() # Establish an instance of the discord.ui.View class
        item = discord.ui.Button(style=discord.ButtonStyle.green, label="Invite", url=f"https://discord.com/api/oauth2/authorize?client_id={client.user.id}&permissions=1024&scope=bot")
        view.add_item(item=item)
        item = discord.ui.Button(style=discord.ButtonStyle.grey, label="Github", url=f"https://github.com/trwy7/AGB")
        view.add_item(item=item)
        if platform.node() == 'agbdocker':
            await interaction.response.send_message(embed=embed, view=view,  ephemeral=True)
        else:
            await interaction.response.send_message('The bot is in testing mode, scores are not saved and may not be accurate', embed=embed, view=view, ephemeral=True)

# fun commands
        
@tree.command(name='uwu', description='uwuify your message')
async def uwucmd(interaction: discord.Interaction, message: str):
    if len(message) < 200:
        await interaction.response.defer(ephemeral=True)
        try:
            webhooks = await interaction.channel.webhooks()
            for webhook in webhooks:
                improvehook = webhook
                break
            try:
                improvehook
            except:
                improvehook = await interaction.channel.create_webhook(name='improv')
            newmsg = await uwu(message)
            await improvehook.send(username=interaction.user.display_name, avatar_url=interaction.user.avatar.url, content=newmsg)
            await interaction.followup.send('Done')
        except:
            await interaction.followup.send('Something went wrong, the bot may not have webhook permissions')
    else:
        await interaction.response.send_message('Too long', ephemeral=True)

# admininstration commands

@tree.command(name='sync', description='Owner only', guild=discord.Object(id=private["guildid"]))
async def sync(interaction: discord.Interaction):
    if interaction.user.id == private["ownerid"]:
        print('Starting sync')
        await interaction.response.send_message(f"Syncing", ephemeral=True)
        await tree.sync()
        print('Command tree synced.')
    else:
        await interaction.response.send_message('You must be trwy to use this command!', ephemeral=True)

@tree.command(name='shutdown', description='Shutdown', guild=discord.Object(id=private["guildid"]))
async def shutdown(interaction: discord.Interaction):
    if interaction.user.id == private["ownerid"]:
        try:
            await interaction.response.send_message("Shutting down", ephemeral=True)
        except:
            print('Couldnt respond to /shutdown')
        with open("stats.json", "w") as f:
            json.dump(stats , f) 
        print('Saving (got /shutdown)')
        await client.close()
    else:
        await interaction.response.send_message('how did you get to this command', ephemeral=True)

@tree.command(name='dm', description='DM someone', guild=discord.Object(id=private["guildid"]))
async def dm(interaction: discord.Interaction, user: discord.User, message: str):
    if interaction.user.id == private["ownerid"]:
        try:
            await user.send(message)
            await interaction.response.send_message(f'Sent to {user.mention}: {message}', ephemeral=True)
        except:
            await interaction.response.send_message(f'It no work :(\n(trying to send to {user.mention})', ephemeral=True)
    else:
        await interaction.response.send_message("nah", ephemeral=True)

# main bot commands

@tree.command(name = "stats", description = "Check stats for a person")
@app_commands.describe(private= "Will the window be private")
@app_commands.describe(user= "The person to check")
async def userstats(interaction, user: discord.User=None, private: bool=False):
    persontemp = user
    if persontemp == None:
        persontemp = interaction.user
    if not persontemp.bot:
        try:
            stats['scores'][str(persontemp.id)]
        except:
            stats['scores'][str(persontemp.id)] = 0
        embed = discord.Embed(
            title="Stats",
            description="Stats for " + persontemp.name,
            color=discord.Color.green(),
        )
        lan = str(interaction.locale)[:2]
        try:
            if not lan == 'en':
                text = 'Your language is not available'
                translation = translator.translate(text, dest=lan)
                embed.add_field(name='⚠️', value=translation.text, inline=False)
        except:
            embed.add_field(name='⚠️', value='Your language may not be supported', inline=False)
        embed.set_thumbnail(url=persontemp.avatar.url)
        embed.add_field(name="Points", value=str(stats['scores'][str(persontemp.id)]))
        leaderboard = stats['scores']
        placeint = [i for i,x in enumerate(leaderboard) if x == str(persontemp.id)][0] +1
        if int(str(placeint)[-1]) == 1:
            placeend = 'st'
        elif int(str(placeint)[-1]) == 2:
            placeend = 'nd'
        elif int(str(placeint)[-1]) == 3:
            placeend = 'rd'
        else:
            placeend = 'th'
        embed.add_field(name="Place", value=f'{persontemp.name} is in the top {str(round(100*round(placeint/len(leaderboard), 3), 1))}% of people, and is in {placeint}{placeend} place (last updated <t:{stats["leadupdate"]}:R>)', inline=False)
        if platform.node() == 'agbdocker':
            await interaction.response.send_message(embed=embed, ephemeral=private)
        else:
            await interaction.response.send_message('The bot is in testing mode, scores are not saved and may not be accurate', embed=embed, ephemeral=True)
        
    else:
        await interaction.response.send_message("Bots cannot get points", ephemeral=True)

@tree.command(name='shop', description='A nice shop')
async def shop(interaction: discord.Interaction):
    await interaction.response.send_message('Item Shop', view=ItemShop(), ephemeral=True)

class ItemShop(discord.ui.View):
    @discord.ui.select( 
        placeholder = "Pick an item", 
        min_values = 1, 
        max_values = 1, 
        options = [ 
            discord.SelectOption(
                label="Shovel",
                description="Lets you use /dig (300 points)",
                emoji='⛏️'
            ),
            discord.SelectOption(
                label="Laptop",
                description="No use yet (500 points)",
                emoji='💻'
            )
        ]
    )
    async def select_callback(self, interaction, select): # https://discordpy.readthedocs.io/en/stable/interactions/api.html#discord.Interaction
        try:
            print(f'{interaction.user.name} picked {select.values[0]}')
            if select.values[0] == "Shovel":
                amount = 300
                try:
                    score = stats['scores'][str(interaction.user.id)]
                except:
                    score = 0
                endbalance = score - amount
                if not (endbalance < 0):
                    stats['scores'][str(interaction.user.id)] = score - amount
                    # Give shovel
                    try:
                        stats['item']['shovel'][str(interaction.user.id)] = stats['item']['shovel'][str(interaction.user.id)] + 1
                    except:
                        stats['item']['shovel'][str(interaction.user.id)] = 1
                    # Show confirmation
                    if stats['item']['shovel'][str(interaction.user.id)] == 1:
                        await interaction.response.send_message("You now have a shovel", ephemeral=True)
                    else:
                        await interaction.response.send_message(f"You now have {str(stats['item']['shovel'][str(interaction.user.id)])} shovels", ephemeral=True)
                else:
                    await interaction.response.send_message("Not enough points", ephemeral=True)
            elif select.values[0] == "Laptop":
                amount = 500
                try:
                    score = stats['scores'][str(interaction.user.id)]
                except:
                    score = 0
                endbalance = score - amount
                if not (endbalance < 0):
                    stats['scores'][str(interaction.user.id)] = score - amount
                    # Give shovel
                    try:
                        stats['item']['laptop'][str(interaction.user.id)] = stats['item']['laptop'][str(interaction.user.id)] + 1
                    except:
                        stats['item']['laptop'][str(interaction.user.id)] = 1
                    # Confirm action
                    if stats['item']['laptop'][str(interaction.user.id)] == 1:
                        await interaction.response.send_message("You now have a laptop", ephemeral=True)
                    else:
                        await interaction.response.send_message(f"You now have {str(stats['item']['laptop'][str(interaction.user.id)])} laptops", ephemeral=True)
                else:
                    await interaction.response.send_message("Not enough points", ephemeral=True)
            else:
                await interaction.response.send_message(f"you picked {select.values[0]}, which has not been set up yet", ephemeral=True)
            
        except Exception as exception:
            await interaction.response.send_message(f"Something went wrong", ephemeral=True)
            print(f"Something went wrong: {exception}")
            modlogs = client.get_channel(1156049697195171850)
            await modlogs.send(f"Something went wrong with a list selector: {exception}")
    @discord.ui.button(label="Exit", style=discord.ButtonStyle.red)
    async def shopexit(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.edit_message(view=None, content='Shop closed')
        self.stop()

@tree.command(name='settings', description='Personal settings')
async def settings(interaction: discord.Interaction):
    embed = discord.Embed(
        title="Settings",
        description="Personal settings",
        color=discord.Color.green(),
    )
    await interaction.response.send_message(embed=embed, view=UserSettings.UserSettingsMenu(), ephemeral=True)

class UserSettings:
    class UserSettingsMenu(discord.ui.View):
        @discord.ui.select( 
            placeholder = "Pick a setting", 
            min_values = 1, 
            max_values = 1, 
            options = [ 
                discord.SelectOption(
                    label="Notifications",
                    description="Notifies you of /steal",
                    emoji='🔔'
                ),
                discord.SelectOption(
                    label="Consent",
                    description="Allows usage of the bot",
                    emoji='✅'
                )
            ]
        )
        async def select_callback(self, interaction, select): # https://discordpy.readthedocs.io/en/stable/interactions/api.html#discord.Interaction
            if select.values[0] == "Notifications":
                # Create embed
                embed = discord.Embed(
                    title="Settings",
                    description="Notifications",
                    color=discord.Color.green(),
                )
                try:
                    stats['usersettings'][str(interaction.user.id)]['notifications']
                    if stats['usersettings'][str(interaction.user.id)]['notifications'] == 0:
                        embed.add_field(name="Status", value="Disabled", inline=False)  
                    elif stats['usersettings'][str(interaction.user.id)]['notifications'] == 1:
                        embed.add_field(name="Status", value="Enabled when offline", inline=False)
                    elif stats['usersettings'][str(interaction.user.id)]['notifications'] == 2:
                        embed.add_field(name="Status", value="Enabled", inline=False)
                except KeyError:
                    embed.add_field(name="Status", value="Disabled", inline=False)
                    stats['usersettings'][str(interaction.user.id)] = {'notifications': 0}
                # Edit message
                await interaction.response.edit_message(view=UserSettings.Notifications(), embed=embed)
                
        @discord.ui.button(label="Exit", style=discord.ButtonStyle.red, row=2)
        async def settingsexit(self, interaction: discord.Interaction, button: discord.ui.Button):
            # Create embed
            embed = discord.Embed(
                title="Settings",
                description="Personal settings (dismissed)",
                color=discord.Color.red(),
            )
            # Disable all buttons
            view = UserSettings.UserSettingsMenu()
            for item in view.children:
                item.disabled = True
            # Send message
            await interaction.response.edit_message(view=view, embed=embed)
            # Stop view
            self.stop()

    class Notifications(discord.ui.View):
        @discord.ui.button(label="Enable", style=discord.ButtonStyle.green)
        async def enable(self, interaction: discord.Interaction, button: discord.ui.Button):
            # Check if user can be notified
            try:
                await interaction.user.send(f"This is a test notification to demonstrate the bot's ability to notify you of /steal: {client.user.mention} has stolen 10 points from you in {interaction.guild.name} at {interaction.channel.mention}")
                # Set notifications to 2
                try:
                    stats['usersettings'][str(interaction.user.id)]['notifications'] = 2
                except KeyError:
                    stats['usersettings'][str(interaction.user.id)] = {'notifications': 2}
            except discord.errors.Forbidden:
                embed = discord.Embed(
                    title="Settings",
                    description="Notifications",
                    color=discord.Color.red(),
                )
                embed.add_field(name="Status", value="Disabled", inline=False)
                await interaction.response.edit_message("You cannot be notified, please enable DMs in Server > Privacy settings > Direct messages", ephemeral=True)
                try:
                    stats['usersettings'][str(interaction.user.id)]['notifications'] = 0
                except KeyError:
                    stats['usersettings'][str(interaction.user.id)] = {'notifications': 0}
                return
            # Create embed
            embed = discord.Embed(
                title="Settings",
                description="Notifications",
                color=discord.Color.green(),
            )
            # Edit message
            embed.add_field(name="Status", value="Enabled", inline=False)
            await interaction.response.edit_message(embed=embed)
        @discord.ui.button(label="While offline", style=discord.ButtonStyle.blurple)
        async def notifsoffline(self, interaction: discord.Interaction, button: discord.ui.Button):
            # Check if user can be notified
            try:
                await interaction.user.send(f"This is a test notification to demonstrate the bot's ability to notify you of /steal: {client.user.mention} has stolen 10 points from you in {interaction.guild.name} at {interaction.channel.mention}")
                # Set notifications to 2
                try:
                    stats['usersettings'][str(interaction.user.id)]['notifications'] = 1
                except KeyError:
                    stats['usersettings'][str(interaction.user.id)] = {'notifications': 1}
            except discord.errors.Forbidden:
                embed = discord.Embed(
                    title="Settings",
                    description="Notifications",
                    color=discord.Color.red(),
                )
                embed.add_field(name="Status", value="Disabled", inline=False)
                await interaction.response.edit_message("You cannot be notified, please enable DMs in Server > Privacy settings > Direct messages", ephemeral=True)
                try:
                    stats['usersettings'][str(interaction.user.id)]['notifications'] = 0
                except KeyError:
                    stats['usersettings'][str(interaction.user.id)] = {'notifications': 0}
                return
            # Create embed
            embed = discord.Embed(
                title="Settings",
                description="Notifications",
                color=discord.Color.yellow(),
            )
            # Edit message
            embed.add_field(name="Status", value="Enabled when offline", inline=False)
            await interaction.response.edit_message(embed=embed)
        @discord.ui.button(label="Disable", style=discord.ButtonStyle.red)
        async def disabled(self, interaction: discord.Interaction, button: discord.ui.Button):
            # Set notifications to 0
            try:
                stats['usersettings'][str(interaction.user.id)]['notifications'] = 0
            except KeyError:
                stats['usersettings'][str(interaction.user.id)] = {'notifications': 0}
            # Create embed
            embed = discord.Embed(
                title="Settings",
                description="Notifications",
                color=discord.Color.red(),
            )
            # Edit message
            embed.add_field(name="Status", value="Disabled", inline=False)
            await interaction.response.edit_message(embed=embed)
        @discord.ui.button(label="Back", style=discord.ButtonStyle.red, row=2)
        async def back(self, interaction: discord.Interaction, button: discord.ui.Button):
            # Create embed
            embed = discord.Embed(
                title="Settings",
                description="Personal settings",
                color=discord.Color.green(),
            )
            # Disable all buttons
            view = UserSettings.UserSettingsMenu()
            # Send message
            await interaction.response.edit_message(view=view, embed=embed)

@tree.command(name='beg', description='Beg for money')
@app_commands.checks.cooldown(1, 25, key=lambda i: (i.user.id))
async def beg(interaction: discord.Interaction):
    stealamount = rand.randrange(-2,10)
    print('beg (' + str(stealamount) + '): ' + interaction.user.name)
    try:
        score = stats['scores'][str(interaction.user.id)] 
    except:
        score = 0
    if stealamount > 0:
        embed = discord.Embed(
            title="Beg",
            color=discord.Color.green(),
        )
        embed.add_field(name="Win", value=f"you pretend to be homeless, and some guy gives you " + str(stealamount) + ' points', inline=False)
    elif stealamount == 0:
        embed = discord.Embed(
            title="Beg",
            color=discord.Color.yellow(),
        )
        embed.add_field(name="Loss", value=f"Nobody gave you anything", inline=False)
    elif stealamount < 0:
        embed = discord.Embed(
            title="Beg",
            color=discord.Color.red(),
        )
        embed.add_field(name="Loss", value=f"Someone stole {abs(stealamount)} from your wallet", inline=False) 
    stats['scores'][str(interaction.user.id)] = score + stealamount
    await interaction.response.send_message(embed=embed)

@tree.command(name='dig', description='Dig for money')
@app_commands.checks.cooldown(1, 25, key=lambda i: (i.user.id))
async def dig(interaction: discord.Interaction):
    try:
        stats['item']['shovel'][str(interaction.user.id)]
    except:
        stats['item']['shovel'][str(interaction.user.id)] = 0
    if stats['item']['shovel'][str(interaction.user.id)] > 0:
        if pr.prob(1/40):
            stealamount = rand.randrange(30,150)
        else:
            stealamount = rand.randrange(0,25)
        print('dig (' + str(stealamount) + '): ' + interaction.user.name)
        try:
            score = stats['scores'][str(interaction.user.id)] 
        except:
            score = 0
        if stealamount > 0:
            if stealamount > 27:
                embed = discord.Embed(
                    title="Dig",
                    color=discord.Color.gold(),
                )
                embed.add_field(name="Win", value=f"You found a gold mine and got " + str(stealamount) + ' points', inline=False)
            else:
                embed = discord.Embed(
                    title="Dig",
                    color=discord.Color.green(),
                )
                embed.add_field(name="Win", value=f"You dug near a house and found " + str(stealamount) + ' points', inline=False)
        elif stealamount == 0:
            embed = discord.Embed(
                title="Dig",
                color=discord.Color.red(),
            )
            embed.add_field(name="Loss", value=f"You found dirt!", inline=False)
            if pr.prob(1/10):
                stats['item']['shovel'][str(interaction.user.id)] = stats['item']['shovel'][str(interaction.user.id)] - 1
                embed.add_field(name="Loss", value=f"You hit a stone and your shovel broke", inline=False)
        elif stealamount < 0:
            embed = discord.Embed(
                title="Dig",
                color=discord.Color.red(),
            )
            embed.add_field(name="Loss", value=f"You somehow lost {stealamount} points", inline=False) 
        stats['scores'][str(interaction.user.id)] = score + stealamount
        await interaction.response.send_message(embed=embed)
        
    else:
        await interaction.response.send_message("Buy a shovel with </shop:1162898171068944445>, (your hands will thank you)", ephemeral=True)

@tree.command(name='steal', description='Steal from someone')
@app_commands.guild_only()
@app_commands.describe(user= "Who to rob")
@app_commands.checks.cooldown(1, 50, key=lambda i: (i.user.id))
async def steal(interaction: discord.Interaction, user: discord.Member):
    if not isinstance(interaction.channel, discord.DMChannel):
            persontemp = user
            if not persontemp.bot:
                try:
                    stats['scores'][str(persontemp.id)]
                except:
                    await interaction.response.send_message('Something went wrong, this person does not have a "score" value (Try another person)', ephemeral=True)
                    return
                if pr.prob(3/4):
                    if stats['scores'][str(persontemp.id)] > 10:
                        stealmax = round(stats['scores'][str(persontemp.id)] * 0.25)
                        stealamount = rand.randrange(2,stealmax)
                        #await user.send(f'{interaction.user.name} stole {stealamount} points from you')
                        print('steal win (' + str(stealamount) + '): ' + interaction.user.name + ' - from - ' + persontemp.name)
                        try:
                            score = stats['scores'][str(interaction.user.id)]
                        except:
                            score = 0
                        stats['scores'][str(interaction.user.id)] = score + stealamount
                        # take from stolen
                        try:
                            score = stats['scores'][str(persontemp.id)]
                        except:
                            score = 0
                        stats['scores'][str(persontemp.id)] = score - stealamount
                        embed = discord.Embed(
                            title="Steal",
                            color=discord.Color.green(),
                        )
                        embed.add_field(name="Win", value="You successfully stole " + str(stealamount) + ' points from ' + persontemp.mention, inline=False)
                        await interaction.response.send_message(embed=embed)
                    elif stats['scores'][str(persontemp.id)] < 0:
                        stealamount = rand.randrange(3,15)
                        print('steal debt loss (' + str(stealamount) + '): ' + interaction.user.name + ' - from - ' + persontemp.name)
                        try:
                            score = stats['scores'][str(interaction.user.id)]
                        except:
                            score = 0
                        # give to stolen
                        stats['scores'][str(interaction.user.id)] = score - stealamount
                        try:
                            score = stats['scores'][str(persontemp.id)]
                        except:
                            score = 0
                        stats['scores'][str(persontemp.id)] = score + stealamount
                        if stats['scores'][str(interaction.user.id)] < 0:
                            await interaction.response.send_message("Somehow they are in debt, so you give them " + str(stealamount) + ' points, which also means you are in debt too')
                        else:
                            await interaction.response.send_message("Somehow they are in debt, so you give them " + str(stealamount) + ' points')
                    else:
                        await interaction.response.send_message('Stop stealing from the poor (nothing changed)', ephemeral=True)
                else:
                    stealmax = round(stats['scores'][str(persontemp.id)] * 0.3)
                    stealamount = rand.randrange(2,stealmax)
                    print('steal loss (' + str(stealamount) + '): ' + interaction.user.name + ' - from - ' + persontemp.name)
                    try:
                        score = stats['scores'][str(interaction.user.id)]
                    except:
                        score = 0
                    # give to stolen
                    stats['scores'][str(interaction.user.id)] = score - stealamount
                    try:
                        score = stats['scores'][str(persontemp.id)]
                    except:
                        score = 0
                    stats['scores'][str(persontemp.id)] = score + stealamount
                    if stats['scores'][str(interaction.user.id)] < 0:
                        embed = discord.Embed(
                            title="Steal",
                            color=discord.Color.red(),
                        )
                        embed.add_field(name="Loss", value=f"You were fined " + str(stealamount) + ' points for robbery, which means you are now in debt', inline=False)
                        await interaction.response.send_message(embed=embed)
                    else:
                        embed = discord.Embed(
                            title="Steal",
                            color=discord.Color.red(),
                        )
                        embed.add_field(name="Loss", value=f"You were fined " + str(stealamount) + ' points for robbery', inline=False)
                        await interaction.response.send_message(embed=embed)
                
                
            else:
                await interaction.response.send_message("Bots cannot get points", ephemeral=True)
    else:
        await interaction.response.send_message("This is a DM, try again in a server", ephemeral=True)

@steal.error
async def on_steal_error(interaction: Interaction, error: AppCommandError): # https://discord.com/channels/336642139381301249/1166170085795319868
    if isinstance(error, discord.app_commands.errors.TransformerError):
        await interaction.response.send_message('This person is not in your server, please try someone else', ephemeral=True)

@tree.command(name='give', description='Give someone points')
@app_commands.describe(user= "Who to give to")
@app_commands.describe(amount= "How many points to give them")
@app_commands.checks.cooldown(2, 45, key=lambda i: (i.user.id))
async def give(interaction: discord.Interaction, user: discord.User, amount: int, private: bool=False):
    persontemp = user
    if not persontemp.bot:
        try:
            amount = round(int(amount))
        except:
            await interaction.response.send_message("not a number", ephemeral=True)
            return
        if not (amount <= 0):
            try:
                score = stats['scores'][str(interaction.user.id)]
            except:
                score = 0
            endbalance = score - amount
            if not (endbalance < 0):
                print('giving (' + str(amount) + '): ' + interaction.user.name + ' - to - ' + persontemp.name)
                try:
                    score = stats['scores'][str(interaction.user.id)]
                except:
                    score = 0
                # give to stolen
                stats['scores'][str(interaction.user.id)] = score - amount
                try:
                    score = stats['scores'][str(persontemp.id)]
                except:
                    score = 0
                stats['scores'][str(persontemp.id)] = score + amount
                await interaction.response.send_message("You successfully gave " + str(amount) + ' points to ' + persontemp.mention, ephemeral=private)
                
                
            else:
                await interaction.response.send_message("Debt is not a good thing (you dont have enough money)", ephemeral=True)
        else:
            await interaction.response.send_message("im sorry what", ephemeral=True)
    else:
        await interaction.response.send_message("Bots cannot get points", ephemeral=True)

@tree.command(name='crime', description='Commit a crime')
@app_commands.checks.cooldown(1, 90, key=lambda i: (i.user.id))
async def crime(interaction: discord.Interaction):
    await interaction.response.defer()
    if pr.prob(9/10):
        view = CrimeMenuTotal.CrimeMenu(interaction.user.id)
    else:
        view = CrimeMenuTotal.SpecialCrimeMenu(interaction.user.id)
    await interaction.followup.send(f"{interaction.user.mention} is running a command", view=view)

class CrimeMenuTotal(discord.ui.View):
    class CrimeMenu(discord.ui.View):
        def __init__(self, author):
            self.author = author
            super().__init__()
        @discord.ui.button(label="eat hotdog sideways", style=discord.ButtonStyle.blurple)
        async def SidewaysHotdog(self, interaction: discord.Interaction, button: discord.ui.Button):
            if interaction.user.id == self.author:
                good = pr.prob(3/4)
                if good:
                    embed = discord.Embed(
                        title="Sideways hotdog",
                        color=discord.Color.green(),
                    )
                    amnt = rand.randrange(1,25)
                    embed.add_field(name="Win", value=f"You successfully got {amnt} points from people begging you to go away", inline=False)
                else:
                    embed = discord.Embed(
                        title="Sideways hotdog",
                        color=discord.Color.red(),
                    )
                    amnt = 0
                    embed.add_field(name="Loss", value=f"Nobody cared", inline=False)
                try:
                    score = stats['scores'][str(interaction.user.id)]
                except:
                    score = 0
                stats['scores'][str(interaction.user.id)] = score + amnt
                await interaction.response.edit_message(embed=embed, view=None, content=None)
                print('crime (' + str(amnt) + '): ' + interaction.user.name)
                
                self.stop()
            else:
                await interaction.response.send_message('Not your prompt', ephemeral=True)
        @discord.ui.button(label="bite full kitkat", style=discord.ButtonStyle.blurple)
        async def arson(self, interaction: discord.Interaction, button: discord.ui.Button):
            if interaction.user.id == self.author:
                good = pr.prob(3/4)
                if good:
                    embed = discord.Embed(
                        title="bite full kitkat",
                        color=discord.Color.green(),
                    )
                    amnt = rand.randrange(1,35)
                    embed.add_field(name="Win", value=f"Someone gave {amnt} points for you being brave", inline=False)
                else:
                    embed = discord.Embed(
                        title="bite full kitkat",
                        color=discord.Color.red(),
                    )
                    amnt = -2 
                    embed.add_field(name="Loss", value=f"You spent 2 points on the kitkat, and nobody cared", inline=False)
                try:
                    score = stats['scores'][str(interaction.user.id)]
                except:
                    score = 0
                stats['scores'][str(interaction.user.id)] = score + amnt
                await interaction.response.edit_message(embed=embed, view=None, content=None)
                print('crime (' + str(amnt) + '): ' + interaction.user.name)
                
                self.stop()
            else:
                await interaction.response.send_message('Not your prompt', ephemeral=True)

    class SpecialCrimeMenu(discord.ui.View):
        def __init__(self, author):
            self.author = author
            super().__init__()
        @discord.ui.button(label="eat hotdog sideways", style=discord.ButtonStyle.blurple)
        async def SidewaysHotdog(self, interaction: discord.Interaction, button: discord.ui.Button):
            if interaction.user.id == self.author:
                good = pr.prob(3/4)
                if good:
                    embed = discord.Embed(
                        title="Sideways hotdog",
                        color=discord.Color.green(),
                    )
                    amnt = rand.randrange(5,30)
                    embed.add_field(name="Win", value=f"You successfully got {amnt} points from people begging you to go away", inline=False)
                else:
                    embed = discord.Embed(
                        title="Sideways hotdog",
                        color=discord.Color.red(),
                    )
                    amnt = 0
                    embed.add_field(name="Loss", value=f"Nobody cared", inline=False)
                try:
                    score = stats['scores'][str(interaction.user.id)]
                except:
                    score = 0
                stats['scores'][str(interaction.user.id)] = score + amnt
                await interaction.response.edit_message(embed=embed, view=None, content=None)
                print('crime special (' + str(amnt) + '): ' + interaction.user.name)
                
                self.stop()
            else:
                await interaction.response.send_message('Not your prompt', ephemeral=True)
        @discord.ui.button(label="bite full kitkat", style=discord.ButtonStyle.blurple)
        async def arson(self, interaction: discord.Interaction, button: discord.ui.Button):
            if interaction.user.id == self.author:
                good = pr.prob(3/4)
                if good:
                    embed = discord.Embed(
                        title="bite full kitkat",
                        color=discord.Color.green(),
                    )
                    amnt = rand.randrange(1,35)
                    embed.add_field(name="Win", value=f"Someone gave {amnt} points for you being brave", inline=False)
                else:
                    embed = discord.Embed(
                        title="bite full kitkat",
                        color=discord.Color.red(),
                    )
                    amnt = -2 
                    embed.add_field(name="Loss", value=f"You spent 2 points on the kitkat, and nobody cared", inline=False)
                try:
                    score = stats['scores'][str(interaction.user.id)]
                except:
                    score = 0
                stats['scores'][str(interaction.user.id)] = score + amnt
                await interaction.response.edit_message(embed=embed, view=None, content=None)
                print('crime (' + str(amnt) + '): ' + interaction.user.name)
                
                self.stop()
            else:
                await interaction.response.send_message('Not your prompt', ephemeral=True)
        @discord.ui.button(label="finding who asked", style=discord.ButtonStyle.green)
        async def special(self, interaction: discord.Interaction, button: discord.ui.Button):
            if interaction.user.id == self.author:
                good = pr.prob(2/3)
                if good:
                    embed = discord.Embed(
                        title="who asked",
                        color=discord.Color.green(),
                    )
                    amnt = rand.randrange(30,85)
                    embed.add_field(name="Win", value=f"You found who asked, and got {str(amnt)} points", inline=False)
                else:
                    embed = discord.Embed(
                        title="who asked",
                        color=discord.Color.red(),
                    )
                    amnt = 0
                    embed.add_field(name="Loss", value=f"Nobody asked, and you got nothing.", inline=False)
                try:
                    score = stats['scores'][str(interaction.user.id)]
                except:
                    score = 0
                stats['scores'][str(interaction.user.id)] = score + amnt
                await interaction.response.edit_message(embed=embed, view=None, content=None)
                print('crime special option (' + str(amnt) + '): ' + interaction.user.name)
                
                self.stop()
            else:
                await interaction.response.send_message('Not your prompt', ephemeral=True)

@tree.command(name = "leaderboard", description = "Global leaderboard") #int(str(x)[-1]) gives the last digit of the int 'x'
@app_commands.checks.cooldown(2, 75, key=lambda i: (i.user.id))
async def leaderboardcmd(interaction):
    await interaction.response.defer(ephemeral=False)
    leaderboard = list(stats['scores'].keys())
    embed = discord.Embed(
        title="Global leaderboard",
        color=discord.Color.green(),
    )
    try:
        if type(stats["leadupdate"]) == int:
            embed.add_field(name='Last updated', value=f'Last updated <t:{stats["leadupdate"]}:R>', inline=False)
        else:
            print('Leaderboard does not have int for update')
            embed.set_footer(text=stats['leadupdate'])
        person1 = await client.fetch_user(leaderboard[0])
        person2 = await client.fetch_user(leaderboard[1])
        person3 = await client.fetch_user(leaderboard[2])
        embed.add_field(name='🥇 1st: ' + person1.name, value=str(await num(stats['scores'][leaderboard[0]])))
        embed.add_field(name='🥈 2nd: ' + person2.name, value=str(await num(stats['scores'][leaderboard[1]])))
        embed.add_field(name='🥉 3rd: ' + person3.name, value=str(await num(stats['scores'][leaderboard[2]])))
        if not interaction.user.name == person1.name and not interaction.user.name == person2.name and not interaction.user.name == person3.name:
            placeint = [i for i,x in enumerate(leaderboard) if x == str(interaction.user.id)][0] +1
            if int(str(placeint)[-1]) == 1:
                placeend = 'st: '
            elif int(str(placeint)[-1]) == 2:
                placeend = 'nd: '
            elif int(str(placeint)[-1]) == 3:
                placeend = 'rd: '
            else:
                placeend = 'th: '
            if placeint == 4 or placeint == 5:
                embed.add_field(name='🔶 ' + str(placeint) + placeend + interaction.user.name, value=str(stats['scores'][str(interaction.user.id)]), inline=False)
            else:
                embed.add_field(name='🔷 ' + str(placeint) + placeend + interaction.user.name, value=str(stats['scores'][str(interaction.user.id)]), inline=False)
        await interaction.followup.send(embed=embed)
    except IndexError:
        await interaction.followup.send('Not enough people have used the bot')

@tree.command(name='giveadm', description='Add balance', guild=discord.Object(id=private["guildid"]))
async def giveadm(interaction: discord.Interaction, user: discord.User, amount: int):
    if interaction.user.id == private["ownerid"]:
        persontemp = user
        try:
            score = stats['scores'][str(persontemp.id)]
        except:
            score = 0
        stats['scores'][str(persontemp.id)] = score + amount
        await interaction.response.send_message(" You forcefully gave " + str(amount) + ' points to ' + persontemp.mention, ephemeral=True)
    else:
        await interaction.response.send_message("nah", ephemeral=True)

@tree.command(name='backup', description='backup points', guild=discord.Object(id=private["guildid"]))
async def backup(interaction: discord.Interaction, upload: bool):
    if interaction.user.id == private["ownerid"]:
        backuploc = await backupstats()
        if not backuploc == False:
            if upload:
                await interaction.response.send_message(f"Keep this in a safe place, you can restore with </restore:1171940382049845321>, a backup has also been made on the PC running AGB.", file=discord.File(backuploc), ephemeral=True)
            else:
                await interaction.response.send_message(f"Saved as {backuploc} on the PC running the bot", ephemeral=True)
        else:
            await interaction.response.send_message('Nothing to back up', ephemeral=True)
    else:
        await interaction.response.send_message('You must be trwy to use this command!', ephemeral=True)

@tree.command(name='restore', description='DANGER', guild=discord.Object(id=private["guildid"]))
async def restore(interaction: discord.Interaction, backup: discord.Attachment, pin: int):
    if interaction.user.id == private["ownerid"] and pin == private["restore-pin"]:
        file_request = requests.get(backup)
        content = file_request.content.decode('utf-8')
        newtemp = json.loads(content)
        global stats
        stats = newtemp
        await interaction.response.send_message('Complete', ephemeral=True)
    else:
        await interaction.response.send_message('You must be trwy to use this command!', ephemeral=True)

@tree.command(name='getbackup', description='get most recent backup', guild=discord.Object(id=private["guildid"]))
@app_commands.checks.cooldown(2, 90, key=lambda i: (i.user.id))
async def getbackup(interaction: discord.Interaction):
    if interaction.user.id == private["ownerid"]:
        search_dir = "backup/"
        files = list(filter(os.path.isfile, glob.glob(search_dir + "*")))
        files.sort(key=lambda x: os.path.getmtime(x))
        await interaction.response.send_message(f"This is the most recent backup", file=discord.File(files[-1]), ephemeral=True)
    else:
        await interaction.response.send_message('You must be trwy to use this command!', ephemeral=True)

def save_stats():
    with open("stats.json", "w") as f:
        json.dump(stats, f, sort_keys=False, indent=4)
    print('Saving (file closed)')

print('starting scripts')

atexit.register(save_stats)

client.run(private['tokens']['agb'])