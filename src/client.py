import discord
from discord.ext.commands import Bot
import os, random
import command_helper, covid_helper

BOT_PREFIX = '>'
BOT_TOKEN = os.environ.get('DISCORD_BOT_TOKEN')

client = Bot(command_prefix=BOT_PREFIX)

# Runs when bot starts 
@client.event
async def on_ready():

    print('------')
    print(client.user.name + ' is now online.')
    print('')
    print('------')

# Process messages sent to chat
@client.event
async def on_message(message):
    await client.process_commands(message)

@client.command()
async def covid(ctx):
    stats = covid_helper.get_covid_json()
    us = covid_helper.get_covid_us_json()
    embed = discord.Embed(
        title = "Coronavirus Statistics",
        description = "-----= U.S. Totals =------\nCases: {:,}\nDeaths: {:,}".format(us[0]['positive'], us[0]['death']),
        colour = discord.Color.red()
    )

    states = covid_helper.get_states()

    numbered = 1
    for i in stats:
        header1 = "{}. {}".format(numbered, states[i['state']])
        val = "Cases: {:,}\nDeaths: {:,}".format(int(i['positive']), int(i['death']))
        embed.add_field(name = header1, value = val, inline=True)
        numbered += 1

    await ctx.send(embed = embed)
    

# Changes role color if user is in that role.    
@client.command()
async def rolecolor(ctx, role: str, r: int, g: int, b: int):
    # role is case sensitive
    if not command_helper.verify_role(role, ctx.message.author.roles):
        await ctx.send("You are not in {}. Please try again".format(role))
        return

    guild_role = discord.utils.get(ctx.guild.roles, name = role)
    await guild_role.edit(colour=discord.Color.from_rgb(r, g, b))
    await ctx.send("{}: {}'s color has now changed.".format(ctx.message.author.mention, role))

# Send random images of carl wheezer
@client.command()
async def carl(ctx):
    image = command_helper.get_carl()
    await ctx.send(image) 

# Perform x amount of y-dice roles in the format of "xdy"
# where x and y are positive integers
@client.command()
async def roll(ctx, arg: str):
    xdy = arg
    kh = False  # keep highest

    if xdy[-2:] == 'kh':
        kh = True
        xdy = xdy[:-2]

    rolls = command_helper.get_rolls(xdy)
    if isinstance(rolls, bool):
        await ctx.send("Argument is missing or is in the wrong format. Please try again")
        return

    if kh:
        max_val = max(rolls)
        await ctx.send("{}: Your dice rolls are: {}. Highest Value: {}.".format(ctx.message.author.mention, str(rolls), str(max_val)))
        return

    await ctx.send("{}: Your dice rolls are: {}.".format(ctx.message.author.mention, str(rolls)))
    return

client.run(BOT_TOKEN)