from discord.ext import commands
import discord
import commands.db.db as db

# -- Command -- #

@commands.command(name="watch_thread",pass_context=True)
async def watch_thread(ctx,action="list",*threads):

	guild = ctx.guild.id


	if action == "add":
		ths = []
		for th in threads:
			ths.append((th,guild))
		add_watch_thread(ths)
		await ctx.send("Thread successfully added to the list of watched threads.")

	elif action == "list":
		ths = get_watch_thread(guild)
		liste = ""
		for th in ths:
			thread = await ctx.guild.fetch_channel(th[0])
			liste += """**{}** : {} \n""".format(thread.name,thread.id)
		embedVar = discord.Embed(title="List of watched threads", description="""{}""".format(liste), color=int(str("64679e"),16))
		await ctx.send(embed=embedVar)

	elif action == "rm":
		delete_watch_thread(threads)
		await ctx.send("Thread successfully removed to the list of watched threads.")

	await ctx.message.delete()




# -- BDD -- #

def create_watch_thread_table():
	db.exe("""SELECT count(name) FROM sqlite_master WHERE type='table' AND name='watch_thread'""")
	if db.fetch_one()[0]==0:
		db.exe("""CREATE TABLE IF NOT EXISTS `watch_thread` (
			`id_thread` int(11) NOT NULL,
			`id_guild` int(11) NOT NULL,
			PRIMARY KEY (`id_thread`)
			)""")
		db.commit()


def get_watch_thread(guild):
	create_watch_thread_table()
	return db.exe("SELECT id_thread FROM 'watch_thread' WHERE id_guild={}".format(guild))

def add_watch_thread(threads):
	create_watch_thread_table()
	db.exe_many("""INSERT OR IGNORE INTO `watch_thread` (`id_thread`, `id_guild`) VALUES (?, ?)""",threads)
	db.commit()

def delete_watch_thread(threads):
	create_watch_thread_table()
	db.exe("""DELETE FROM 'watch_thread' WHERE id_thread IN({})""".format(",".join(threads)))
	db.commit()