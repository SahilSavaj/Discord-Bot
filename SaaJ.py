#%%

import discord
import os
import requests
import json
import random
from discord.ext import commands, tasks
import youtube_dl

client=commands.Bot(command_prefix=">")
client.remove_command("help")

welcome=["Holaa","Hieee","Namaste","Heyyy","Kem Palty"]
rules=[":one: Avoid making your chat highlighted by use of any other fonts/ capital letters",
":two: Avoid interfering in matters which do not directly affect or involve you",
":three: Avoid any religious/ political/ sexual discussions that may lead to heated arguments",
":four: Do not share any personal information with any other fellow member of the server (including , bank account, address, email, password, bank password and credit card information, etc).",
":five: Use of any offensive language against any fellow member is not permitted",
":six: Moderators reserve the right to delete any post/message",
":seven: No voice chat channel hopping.",
":eight: No annoying, loud or high pitch noises.",
":nine: Reduce the amount of background noise,if possible.",
":keycap_ten: Moderators reserve the right to disconnect, mute, deafen or move members to and from voice channel"]
status=['Jamming out to music','Sleeping..!']

def get_quote():
    response=requests.get("https://zenquotes.io/api/random")
    json_data=json.loads(response.text)
    quote=json_data[0]['q'] + " -" + json_data[0]['a']
    return(quote)

#STARTING OF BOT
@client.event
async def on_ready():
    print("{0.user} is up and ready".format(client))

'''#ERROR
@client.event
async def on_command_error(msg,error):
    if isinstance(error,commands.MissingPermissions):
        await msg.channel.send("You dont have Permissions")
    elif isinstance(error,commands.MissingRequiredArgument):
        await msg.channel.send("Please enter all the req Arguments")
    else:
        try:
            raise error
        except:
            await msg.channel.send("Incorrect Command")'''

#HELP
@client.group(invoke_without_command=True)
async def help(msg):
    embed=discord.Embed(title="HELP",description="*Use >help <command> for extended information on a command.*",color=msg.author.color)
    embed.add_field(name="MODERATION",value="*kick, ban, unban, clear*")
    embed.add_field(name="FUN",value="*whois, inspire*")
    embed.set_footer(icon_url=msg.author.avatar_url,text=f"Requested by {msg.author.name}")
    await msg.channel.send(embed=embed)
@help.command()
async def kick(msg):
    em=discord.Embed(title="Kick",description="Kicks a member from the server",color=msg.author.color)
    em.add_field(name="SYNTAX",value=">kick/k <member> [reason]")
    await msg.channel.send(embed=em)
@help.command()
async def ban(msg):
    em=discord.Embed(title="Ban",description="Bans a member from the server",color=msg.author.color)
    em.add_field(name="SYNTAX",value=">ban/b <member> [reason]")
    await msg.channel.send(embed=em)
@help.command()
async def clear(msg):
    em=discord.Embed(title="Clear",description="Deletes messages from server",color=msg.author.color)
    em.add_field(name="SYNTAX",value=">clear/c {number of messages to be deleted}")
    await msg.channel.send(embed=em)
@help.command()
async def inspire(msg):
    em=discord.Embed(title="Inspire",description="Gives an Inspiring Quote",color=msg.author.color)
    em.add_field(name="SYNTAX",value=">inspire")
    await msg.channel.send(embed=em)
@help.command()
async def unban(msg):
    em=discord.Embed(title="Unban",description="Unbans a member from the server",color=msg.author.color)
    em.add_field(name="SYNTAX",value=">unban/ub <name>#<tag>")
    await msg.channel.send(embed=em)
@help.command()
async def whois(msg):
    em=discord.Embed(title="Whois",description="Describes the mentioned user",color=msg.author.color)
    em.add_field(name="SYNTAX",value=">whois/info/about/user <member>")
    await msg.channel.send(embed=em)

#COMMANDS
@client.command(aliases=['rules'])
async def rule(msg,*,num):
    await msg.channel.send(rules[int(num)-1])
@client.command()
async def hello(msg):
    await msg.channel.send(random.choice(welcome))
@client.command(aliases=['c'])
@commands.has_permissions(manage_messages=True)
async def clear(msg,amount=2):
    await msg.channel.purge(limit=amount)
@client.command(aliases=['k'])
@commands.has_permissions(kick_members=True)
async def kick(msg,member:discord.Member,*,reason="Not provided"):
    try:
        await member.send("You have been Kicked, Reason-" + reason)
    except:
        await msg.channel.send("Member have their DM's closed")    
    await member.kick(reason=reason)
@client.command(aliases=['b'])
@commands.has_permissions(ban_members=True)
async def ban(msg,member:discord.Member,*,reason="Not provided"):
    await msg.channel.send(member.name + " has been Banned, Reason-" + reason)
    await member.ban(reason=reason)
@client.command(aliases=['ub'])
@commands.has_permissions(ban_members=True)
async def unban(msg,*,member):
    banned_users=await msg.guild.bans()
    member_name,member_tag=member.split('#')
    for banned_member in banned_users:
        user=banned_member.user
        if (user.name,user.discriminator)==(member_name,member_tag):
            await msg.guild.unban(user)
            await msg.channel.send(member_name + " has been Unbanned..!")
            return    
    await msg.channel.send(member_name +" Not Found ")
@client.command(aliases=['user','info','about'])
@commands.has_permissions(kick_members=True)
async def whois(msg,member:discord.Member):
    embed=discord.Embed(title=member.name,description=member.mention,color=discord.Color.red())
    embed.add_field(name="ID",value=member.id,inline=True)
    embed.set_thumbnail(url=member.avatar_url)
    embed.set_footer(icon_url=msg.author.avatar_url,text=f"Requested by {msg.author.name}")
    await msg.channel.send(embed=embed)
@client.command()
async def inspire(msg):
    await msg.channel.send(get_quote())

#MUSIC
@client.command()
async def play(msg,url:str):
    voiceChannel=discord.utils.get(msg.guild.voice_channels, name='Music [Groovy]')
    voice=discord.utils.get(client.voice_clients, guild=msg.guild)
    if not voice.is_connected():
        await voiceChannel.connect()
@client.command()
async def leave(msg):
    voice=discord.utils.get(client.voice_clients, guild=msg.guild)
    if voice.is_connected():
        await voice.disconnect()
    else:
        await msg.channel.send("the bot is not connected")
@client.command()
async def pause(msg):
    voice=discord.utils.get(client.voice_clients, guild=msg.guild)
    if voice.is_playing():
        await voice.pause()
    else:
        await msg.channel.send("Audio isn't playing")
@client.command()
async def resume(msg):
    voice=discord.utils.get(client.voice_clients, guild=msg.guild)
    if voice.is_paused():
        await voice.resume()
    else:
        await msg.channel.send("already Playing")
@client.command()
async def stop(msg):
    voice=discord.utils.get(client.voice_clients, guild=msg.guild)
    await voice.stop()


client.run('ODQ1MjUzMjc1MDcwODg5OTk2.YKeRdA.G2Crs71SVEOfwgxJgOJ37mFFUyY')


# %%
