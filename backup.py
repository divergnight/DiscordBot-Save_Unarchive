from discord.ext import commands,tasks
import discord
import os
from os.path import basename,realpath,isfile,join
from os import walk,listdir
from dotenv import load_dotenv

class DocBot(commands.Bot):
    """
        There is a bot class for run bot in discord
    """

    def __init__(self,prefix):
        super().__init__(command_prefix=prefix)
        self.add_command(save)

    async def on_ready(self):
        print("Le bot est prêt.")



async def export_all():
    """
        Export all active channels and threads from all guilds with Tyrrrz's DiscordChatExporter
    """

    #Export all channels from all the guilds
    os.system("dotnet {}/DiscordChatExporter.Cli.dll exportall -t {} -o \"{}/%G/%T/%C/%C.html\" {} --include-dm false --dateformat \"dd/MM/yyyy HH:mm:ss\"".format(EXEPATH,TOKEN,EXPORTDIRECTORY,OTHER))


    #Export all active threads from all the guilds
    for guild in bot.guilds:    #Collect all guilds
        await export_all_threads(guild.id)




async def export_all_threads(guild_id):
    """
        Export all active and archived threads from a guild
    """

    guild = bot.get_guild(guild_id)

    #Collect all active threads from the guild
    ths = guild.threads
    for th in ths:
        export_thread(th)

     #Collect all archived threads from the guild
    channels = await guild.fetch_channels()
    for channel in channels:
        if str(channel.type) == 'text' and channel.members != []:
            threads = channel.archived_threads()
            async for th in threads :
                await th.edit(archived=False,auto_archive_duration=1440)
                export_thread(th)



def export_thread(th):
    """
        Export a active thread from a guild with Tyrrrz's DiscordChatExporter
    """
    CHANNEL = th.id
    FILENAME = th.name
    EXPORTDIRECTORY_L = "{}/{}/{}/{}".format(EXPORTDIRECTORY,th.guild,th.category,th.parent)

    #Export one of the guild's threads
    os.system("dotnet {}/DiscordChatExporter.Cli.dll export -t {} -c {} -o \"{}/{}.html\" {} --dateformat \"dd/MM/yyyy HH:mm:ss\"".format(EXEPATH,TOKEN,CHANNEL,EXPORTDIRECTORY_L,FILENAME,OTHER))




def edit_all():
    """
        Remove parent reference and add theme for all html file in directory.
    """
    for y in listdir(EXPORTDIRECTORY):
        global guild_nav_path
        guild_nav_path = create_guild_nav_path(join(EXPORTDIRECTORY,y))
        for (repertoire, sousRepertoires, fichiers) in walk(join(EXPORTDIRECTORY,y)):   #List all files
            for x in filter(lambda k: k[-5:] == ".html", fichiers):                     #Keep only html files
                edit(repertoire,basename(x))                                            #Edit file




def create_guild_nav_path(server_directory):

    guild_nav_path = """<nav>"""

    category_index = 0
    for nav_category in listdir(server_directory):
        #Add category
        guild_nav_path += """
    <div class="category-nav">
        <label for="{}" class="category-box">
            <svg class="arrow-gKvcEx icon-2yIBmh" width="24" height="24" viewBox="0 0 24 24"><path fill="currentColor" fill-rule="evenodd" clip-rule="evenodd" d="M16.59 8.59004L12 13.17L7.41 8.59004L6 10L12 16L18 10L16.59 8.59004Z"></path></svg>
            <span class="category-text">{}</span>
        </label>
        <input type=checkbox id="{}">""".format(nav_category+"_"+str(category_index),nav_category,nav_category+"_"+str(category_index))

        for nav_channel in listdir(server_directory+"/"+nav_category):
            channel_directory = server_directory+"/"+nav_category+"/"+nav_channel
            relative_channel_path = """../../{}/{}""".format(nav_category,nav_channel)

            #Add channel
            guild_nav_path += """<div><a href="{}" class="channel-link"><svg></svg><span class="text-link">{}</span></a></div>""".format(relative_channel_path+'/'+nav_channel+'.html',nav_channel)

            #Add threads
            threads = [f for f in listdir(channel_directory) if isfile(join(channel_directory,f))]
            threads = [f for f in threads if f[:-5] != nav_channel]

            if len(threads) > 0:
                guild_nav_path += """<div class="threads-link"><div class="svg">"""

                if len(threads) == 1:
                    guild_nav_path += """<svg class="spine--Wla_O" width="12" height="11" viewBox="0 0 12 11" fill="none">
    <path d="M11 9H4C2.89543 9 2 8.10457 2 7V1C2 0.447715 1.55228 0 1 0C0.447715 0 0 0.447715 0 1V7C0 9.20914 1.79086 11 4 11H11C11.5523 11 12 10.5523 12 10C12 9.44771 11.5523 9 11 9Z" fill="currentColor"></path>
    </svg>"""
                elif len(threads) == 2:
                    guild_nav_path += """<svg class="spine--Wla_O" width="12" height="45" viewBox="0 0 12 45" fill="none">
    <path d="M2 1C2 0.447715 1.55228 0 1 0C0.447715 0 0 0.447715 0 1V41C0 43.2091 1.79086 45 4 45H11C11.5523 45 12 44.5523 12 44C12 43.4477 11.5523 43 11 43H4C2.89543 43 2 42.1046 2 41V13C2 11.8954 2.89543 11 4 11H11C11.5523 11 12 10.5523 12 10C12 9.44771 11.5523 9 11 9H4C2.89543 9 2 8.10457 2 7V1Z" fill="currentColor"></path>
    </svg>"""
                else:
                    for i in range(len(threads)-2):
                        guild_nav_path += """<svg class="spine--Wla_O" width="12" height="79" viewBox="0 0 12 79" fill="none" style="top: {}px;">
        <path d="M1 0C0.447715 0 0 0.447713 0 0.999998V75C0 77.2091 1.79086 79 4 79H11C11.5523 79 12 78.5523 12 78C12 77.4477 11.5523 77 11 77H4C2.89543 77 2 76.1046 2 75V47C2 45.8954 2.89543 45 4 45H11C11.5523 45 12 44.5523 12 44C12 43.4477 11.5523 43 11 43H4C2.89543 43 2 42.1046 2 41V13C2 11.8954 2.89543 11 4 11H11C11.5523 11 12 10.5523 12 10C12 9.44771 11.5523 9 11 9H4C2.89543 9 2 8.10457 2 7V1C2 0.447715 1.55228 0 1 0Z" fill="currentColor"></path>
    </svg>""".format(34*i)


                guild_nav_path += """</div><div>"""
                for thread in threads:
                    guild_nav_path += """<div><a href="{}" class="thread-link"><span class="text-link">{}</span></a></div>""".format(relative_channel_path+'/'+thread,thread[:-5])

                guild_nav_path += """</div></div>"""

        guild_nav_path += """</div>"""
        category_index += 1
    guild_nav_path += """</nav>"""

    return guild_nav_path




def edit(repertoire,filename):
    """
        Remove parent reference and add theme for a html file
    """
    with open("{}/{}".format(repertoire,filename),'r+',encoding='utf-8') as file:
        html = file.read()

        html = remove_parent_reference(html,repertoire)
        html = add_theme(html,repertoire,filename)

        file.seek(0)
        file.write(html)




def remove_parent_reference(html,repertoire):
    """
        Remove an html reference to the parent on the file
    """
    #Parent reference
    title = html.find("""class="preamble__entry">""")+24
    start = html[title:].find("""<div class="preamble__entry">""")+title
    end = html[start:].find("</div>")+start+6

    html = html[:start] +  html[end:]

    return html




def add_theme(html,repertoire,filename):
    """
        Add an theme reference of the file
    """

    #Add Theme
    libs_path = realpath("./libs/")
    index = html.find("""</style>""")+8
    html = html[:index] + '<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/divergnight/DiscordBotAesir@master/theme-online.css">'.format(libs_path) + html[index:]
    html = html[:index-8] + """nav{display:none;}""" + html[index-8:]
    index = html.find("""<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/9.15.6/styles/solarized-dark.min.css">""")
    html = html[:index] + '<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/highlightjs/cdn-release@11.5.0/build/styles/atom-one-light.min.css">'.format(libs_path) + html[index+119:]
    index = html.find("""<script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/9.15.6/highlight.min.js"></script>""")
    html = html[:index] + '<script src="https://cdn.jsdelivr.net/gh/highlightjs/cdn-release@11.5.0/build/highlight.min.js"></script>'.format(libs_path) + html[index+99:]

    #Create chatlog section
    index = html.find("""<div class="chatlog">""")
    html = html[:index] + '<div class="chatlog-all">' + html[index:]
    index = html.find("""</body>""")
    html = html[:index] + '</div>'.format(libs_path) + html[index:]

    #Create link section
    index = html.find("""<div class="preamble">""")
    html = html[:index] + '<div class="preamble-all">' + html[index:]

    #Create hide and show categeory
    gnp = ""+guild_nav_path

    index = gnp.find("""<span class="text-link">{}</span>""".format(filename[:-5]))
    index = gnp[:index].rfind("""<div>""")
    gnp = gnp[:index] + '<div class="nav-select">' + gnp[index+5:]

    if(basename(repertoire) != filename[:-5]):
        index = gnp[:index].rfind("""<div class="threads-link">""")+25
        gnp = gnp[:index] + ' style="display:flex;"' + gnp[index:]

        index = gnp[:index].rfind("""<a href=""")
        index = gnp[:index].rfind("""<div>""")
        gnp = gnp[:index] + '<div style="display:block;">' + gnp[index+5:]  
    else:
        index = gnp[index:].find("""</div>""")+6+index
        index = gnp[index:].find("""<div""")+4+index
        if (gnp[index:index+22] == ' class="threads-link">'):
            index += 21
            gnp = gnp[:index] + ' style="display:flex;"' + gnp[index:]

    #Add arrow hide and show animation
    index = html.rfind("""</html>""")
    html = html[:index] + """<script>myStorage = window.localStorage;
    document.querySelectorAll(".category-box").forEach(categ=>{
        if(myStorage.getItem(categ.getAttribute("for")) === "true"){ categ.setAttribute("class","category-box category-show zero-time") }
        categ.addEventListener("click",function(){
            if(this.getAttribute("class") === "category-box"){ this.setAttribute("class","category-box category-show"); myStorage.setItem(this.getAttribute("for"),true);}
            else{ this.setAttribute("class","category-box"); myStorage.setItem(this.getAttribute("for"),false);} }) })</script>""" + html[index:]

    index = html.find("""<div class="chatlog-all">""")
    html = html[:index] + '{}</div>'.format(gnp) + html[index:]

    #Remove edited tag
    while(True):
        index = html.find("""<span class="chatlog__edited-timestamp""")
        if (index == -1):
            break

        end = html[index:].find("""(edited)</span>""")+15+index
        html = html[:index] + '' + html[end:]

    #Add username theme
    glb = 0
    counter = 0
    while(True):
        counter+=1
        index = html[glb:].find("""<span class="chatlog__author-name""")+glb
        if (index-glb == -1):
            break
        if (counter > 100):
            print("Counter overflow :",join(repertoire,filename))
            break

        html = html[:index] + """<span class="chatlog__author-name-date">""" + html[index:]

        index = html[glb:].find("""<span class="chatlog__timestamp">""")+33+glb
        index = html[index:].find("""</span>""")+7+index
        html = html[:index] + """</span>""" + html[index:]

        glb = index+7

    #Remove title tag
    glb = 0
    counter = 0
    while(True):
        counter+=1
        index = html[glb:].find("""title=\"""")+glb
        if (index-glb == -1):
            break

        end = html[index:].find("""">""")+index+1
        html = html[:index] + html[end:]

        glb = end+1

    return html




async def backup():
    """
        Create a server backup
    """
    os.system("[ -d ./ExportDiscord ] || mkdir ./ExportDiscord")

    await export_all()          #Export all active channels and threads from all guilds with Tyrrrz's DiscordChatExporter

    edit_all()                  #Create an html reference for all parent and child files of the files

    return "Backup completed"



load_dotenv()
TOKEN = os.getenv('BACKUP_TOKEN')                                      #Your token
EXEPATH = "./DiscordChatExporter.CLI"                                   #Path to exe directory
EXPORTDIRECTORY = "./ExportDiscord"                                     #Path to export directory
OTHER = "--media --reuse-media"                                         #Add other parameters to export (--media, --reuse-media, --filter, ...)

GUILD_ID = 0                                                            #Guild ID (leave empty if you use 'exportall')

PREFIX = "!"                                                            #Change this prefix for use bot commands with another prefix


@commands.command(name="save",pass_context=True)
async def save(ctx):

    state = await backup() #Create a server backup

    print("\n{}\n".format(state))

    if (state != "Backup completed"):
        await ctx.send("Error while backup.")
    else:
        await ctx.send("All channels and threads have been backed up.")

    await ctx.message.delete()

bot = DocBot(PREFIX)
bot.run(TOKEN)


