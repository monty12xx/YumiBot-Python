import discord
from discord.ext import commands
import datetime
import time
import platform

bot = commands.Bot(command_prefix="y/")

botVersion = "1.0.0_DEV"

@bot.event
async def on_ready():
    print("Loading YumiBot...")
    print("Using account {0.name}#{0.discriminator}".format(bot.user))
    print("Bot ID is {0.id}".format(bot.user))
    print("====================")

@bot.command(pass_context=True)
async def ping(ctx):
    try:
        before = datetime.datetime.utcnow()
        ping_msg = await bot.send_message(ctx.message.channel, content=":mega: **Pinging...**")
        ping = (datetime.datetime.utcnow() - before) * 1000
        before2 = time.monotonic()
        await (await bot.ws.ping())
        after = time.monotonic()
        ping2 = (after - before2) * 1000
        await bot.edit_message(ping_msg, new_content=":mega: Pong! The message took **{:.2f}ms**!".format(ping.total_seconds())+" `Websocket: {0:.0f}ms` :thinking:".format(ping2))
    except Exception as e:
        await bot.say("{0.mention}: I recieved an error when trying to run the command! `{1}`\nYou shouldn't receive an error like this. \nContact Desiree#3658 in the support server, link in `{2}about`.".format(ctx.message.author, e, bot.command_prefix))

@bot.command(pass_context = True)
async def about(ctx):
    try:
        server_count = 0
        member_count = 0
        for server in bot.servers:
            server_count += 1
            for member in server.members:
                member_count += 1
        embed = discord.Embed(title='About Yumi!', description = "Nothing to see here.", color=ctx.message.author.color).add_field(name='Version Number', value=str(botVersion), inline=False).add_field(name='Servers', value=str(server_count)).add_field(name='Users',value=str(member_count) + '\n\nJoin the [support guild](https://discord.gg/T2pyUvf)', inline=False).set_footer(text="Made with love <3").set_thumbnail(url=ctx.message.server.me.avatar_url)
        await bot.send_message(ctx.message.channel, content=None, embed=embed)
    except Exception as e:
        await bot.say("{0.mention}: I recieved an error when trying to run the command! `{1}`\nYou shouldn't receive an error like this. \nContact Desiree#3658 in the support server, link in `{2}about`.".format(ctx.message.author, e, bot.command_prefix))

@bot.command(pass_context=True)
async def info(ctx):
    try:
        commands = len(bot.commands)
        dpyVersion = discord.__version__
        pyVersion = platform.python_version()
        server_count = 0
        member_count = 0
        for server in bot.servers:
            server_count += 1
            for member in server.members:
                member_count += 1
        em = discord.Embed(title="Information",color=ctx.message.author.color)
        em.add_field(name="Versions",value="**Bot**: {0}\n**DiscordPY**: {1}\n**Python**: {2}".format(botVersion, dpyVersion, pyVersion),inline=False)
        em.add_field(name="Bot",value="**Commands**: {0}\n**Guilds:** {1}\n**Users**: {2}".format(commands, server_count, member_count),inline=False)
        await bot.send_message(ctx.message.channel, content=None, embed=em)
    except Exception as e:
        await bot.say("{0.mention}: I recieved an error when trying to run the command! `{1}`\nYou shouldn't receive an error like this. \nContact Desiree#3658 in the support server, link in `{2}about`.".format(ctx.message.author, e, bot.command_prefix))

        @bot.event
async def update():

    payload = json.dumps({
        'shard_id': 0,
        'shard_count': 1,
        'server_count': len(bot.servers)
    })

    headers = {
        'authorization': 'Your Key',
        'content-type': 'application/json'
    }

    headers2 = {
        'authorization': 'Your Key',
        'content-type': 'application/json'
    }

    DISCORD_BOTS_API = 'https://bots.discord.pw/api'
    Oliy_api = 'https://discordbots.org/api'

# discordbots.org
    url = '{0}/bots/205224819883638785/stats'.format(Oliy_api)
    async with session.post(url, data=payload, headers=headers2) as resp:
        logger.info('SERVER COUNT UPDATED.\ndiscordbots.org statistics returned {0.status} for {1}\n'.format(resp, payload))

# bots.discord.pw
    url = '{0}/bots/205224819883638785/stats'.format(DISCORD_BOTS_API)
    async with session.post(url, data=payload, headers=headers) as resp:
        logger.info('SERVER COUNT UPDATED.\nbots.discord.pw statistics returned {0.status} for {1}\n'.format(resp, payload))
        
bot.run('token')
