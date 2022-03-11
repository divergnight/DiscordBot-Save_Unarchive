from discord.ext import commands,tasks
import discord
import os
from os.path import basename,realpath,isfile,join
from os import walk,listdir
from dotenv import load_dotenv
import cmds.watch_thread as wt

class DocBot(commands.Bot):
	"""
		There is a bot class for run bot in discord
	"""

	def __init__(self,prefix):
		super().__init__(command_prefix=prefix)
		self.add_command(status)
		self.add_command(link)
		self.add_command(clean)
		self.add_command(wt.watch_thread)

	async def on_ready(self):
		print("Le bot est prêt.")
		if not self.unarchive_thread.is_running():
			self.unarchive_thread.start()


	#Unarchive thread archived
	async def on_thread_update(self,before, after):
		#Unarchive thread archived
		unarchive_thread = [row[0] for row in wt.get_watch_thread(after.guild.id)]
		if after.archived and after.id in unarchive_thread:
			await after.edit(archived=False)
			print('Thread Update at',after.archive_timestamp)
		
	@tasks.loop(hours=12.0)
	async def unarchive_thread(self):
		"""
			#Unarchive all threads from all guilds
		"""
		for guild in bot.guilds:
			channels = await guild.fetch_channels()

			unarchive_thread = [row[0] for row in wt.get_watch_thread(guild.id)]
			for channel in channels:
				if str(channel.type) == 'text' and channel.members != []:
					threads = channel.archived_threads()
					async for th in threads :
						if th.id in unarchive_thread:
							await th.edit(archived=False)

		print('Thread Unarchive')



load_dotenv()
TOKEN = os.getenv('TOKEN')
PREFIX = "!"


@commands.command(name="status",pass_context=True)
async def status(ctx):
	await ctx.send("Server on.")
	await ctx.message.delete()



@commands.command(name="clean",pass_context=True)
async def clean(ctx,mode=None,arg=None):
	guild = ctx.guild
	ch = ctx.channel

	if mode in ["-i","-n","--all"]:
		if mode != "--all" and arg == None:
			await ctx.send("An argument is expected.")
			return

		if mode == "-i":
			arg = await ch.fetch_message(int(arg))
		if mode == "-n":
			arg = int(arg)+1

		await ch.purge(limit=(None,arg)[mode == "-n"], after=(None,arg)[mode == "-i"])

		if mode == "-i":
			await arg.delete()
	else:
		await ctx.send("Unknown mode : **{}**".format(mode))
						


@commands.command(name="link",pass_context=True)
async def link(ctx,title="Title",color="64679e",*args):
	liste = ""
	for arg in args:
		liste += arg + "\n"
	embedVar = discord.Embed(title=title, description="""{}""".format(liste), color=int(str(color),16))
	await ctx.send(embed=embedVar)
	await ctx.message.delete()


bot = DocBot(PREFIX)
bot.run(TOKEN)