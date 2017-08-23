import discord
from discord.ext import commands
import datetime
import time
import platform
import json
import aiohttp




class Yumiboat(commands.Bot):
    def __init__(self):
        self.owner = None
        self.command_message = {}
        self.session = aiohttp.ClientSession()

    async def on_ready(self):
        print("Loading YumiBot...")
        print("Using account {0.name}#{0.discriminator}".format(self.user))
        print("Bot ID is {0.id}".format(self.user))
        print("====================")


    @commands.command(pass_context=True)
    async def ping(self, ctx):
        try:
            before = datetime.datetime.utcnow()
            ping_msg = await self.send_message(ctx.message.channel, content=":mega: **Pinging...**")
            ping = (datetime.datetime.utcnow() - before) * 1000
            before2 = time.monotonic()
            await (await self.ws.ping())
            after = time.monotonic()
            ping2 = (after - before2) * 1000
            await self.edit_message(ping_msg, new_content=":mega: Pong! The message took **{:.2f}ms**!".format(
                ping.total_seconds()) + " `Websocket: {0:.0f}ms` :thinking:".format(ping2))
        except Exception as e:
            await self.say(
                "{0.mention}: I recieved an error when trying to run the command! `{1}`\nYou shouldn't receive an error like this. \nContact Desiree#3658 in the support server, link in `{2}about`.".format(
                    ctx.message.author, e, bot.command_prefix))


    @commands.command(pass_context=True)
    async def about(self, ctx):
        try:
            server_count = 0
            member_count = 0
            for server in self.servers:
                server_count += 1
                for member in server.members:
                    member_count += 1
            embed = discord.Embed(title='About Yumi!', description="Nothing to see here.",
                                  color=ctx.message.author.color).add_field(name='Version Number', value=str(botVersion),
                                                                            inline=False).add_field(name='Servers',
                                                                                                    value=str(
                                                                                                        server_count)).add_field(
                name='Users', value=str(member_count) + '\n\nJoin the [support guild](https://discord.gg/T2pyUvf)',
                inline=False).set_footer(text="Made with love <3").set_thumbnail(url=ctx.message.server.me.avatar_url)
            await self.send_message(ctx.message.channel, content=None, embed=embed)
        except Exception as e:
            await self.say(
                "{0.mention}: I recieved an error when trying to run the command! `{1}`\nYou shouldn't receive an error like this. \nContact Desiree#3658 in the support server, link in `{2}about`.".format(
                    ctx.message.author, e, self.command_prefix))


    @commands.command(pass_context=True)
    async def info(self, ctx):
        try:
            commands = len(self.commands)
            botVersion = '1_0_0_DEV'
            dpyVersion = discord.__version__
            pyVersion = platform.python_version()
            server_count = 0
            member_count = 0
            for server in self.servers:
                server_count += 1
                for member in server.members:
                    member_count += 1
            em = discord.Embed(title="Information", color=ctx.message.author.color)
            em.add_field(name="Versions",
                         value="**Bot**: {0}\n**DiscordPY**: {1}\n**Python**: {2}".format(botVersion, dpyVersion,
                                                                                          pyVersion), inline=False)
            em.add_field(name="Bot",
                         value="**Commands**: {0}\n**Guilds:** {1}\n**Users**: {2}".format(commands, server_count,
                                                                                           member_count), inline=False)
            await self.send_message(ctx.message.channel, content=None, embed=em)
        except Exception as e:
            await self.say(
                "{0.mention}: I recieved an error when trying to run the command! `{1}`\nYou shouldn't receive an error like this. \nContact Desiree#3658 in the support server, link in `{2}about`.".format(
                    ctx.message.author, e, bot.command_prefix))




    async def dlistupdate(self, ctx):
        uri = 'https://discordbots.org/api'
        channel = ctx.message.channel
        dump = json.dumps({
            'shard_id': str(self.shard_id),
            'shard_count': str(self.shard_count),
            'server_count': len(self.servers)
        })
        head = {
            'authorization': 'your key lawd',
            'content-type' : 'application/json'
        }

        url = '{0}/bots/(your id)/stats'.format(uri)

        async with self.session.post(url, data=dump, headers=head) as resp:
            await self.bot.send_message(channel, 'returned {0.status} for {1}'.format(resp, dump))

    async def on_server_join(self):
        self.dlistupdate()

    async def on_server_remove(self):
        self.dlistupdate()

        
bot = Yumiboat(command_prefix="y/")

bot.run('token')
