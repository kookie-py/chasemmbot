#-*- coding:utf-8 -*-
import os
from re import I
import discord
import discord.ui
import asyncio
from discord import NotFound, Forbidden
from discord.channel import CategoryChannel
from discord.embeds import Embed
from discord.ext.commands import errors
from discord.utils import get
from discord.ext.commands.errors import CommandNotFound
import pytz
from datetime import datetime, timedelta, tzinfo
from discord import CategoryChannel
#Subimports.
from discord.ext import commands
from discord.ext import tasks
from discord.ext import pages
from rbxapiyes.exceptions import PlayerNotFound, Unauthorized
from rbxapiyes.Client import Client as Client1
from ro_py import Client as Client2
import time
import chat_exporter
import io
from io import *
import json
import requests
import csv
import arrow
import math
import mysql.connector
import humanfriendly
import DiscordUtils
import difflib

maincolor = 0xf3f3f3
grey = 0x99AAB5
redcolor = maincolor

#Username: XPJ9qhFktO
#Database name: XPJ9qhFktO
#Password: lXPOlT66Pt
#Server: remotemysql.com
#Port: 3306

#import mysql.connector
#db = mysql.connector.connect(
#    host="remotemysql.com",
#    user="XPJ9qhFktO",
#    passwd="lXPOlT66Pt",
#    database="XPJ9qhFktO")
#mycursor = db.cursor()
#mycursor.execute("CREATE Table added_info (userID bigint UNSIGNED, channelID bigint UNSIGNED, uniID bigint UNSIGNED PRIMARY KEY AUTO_INCREMENT)")
#mycursor.execute("CREATE Table closed_msgs (msgID bigint UNSIGNED, channelID bigint UNSIGNED, uniID bigint UNSIGNED PRIMARY KEY AUTO_INCREMENT)")
#mycursor.execute("CREATE Table t_cd (userID bigint UNSIGNED, cd VARCHAR(50), uniID bigint UNSIGNED PRIMARY KEY AUTO_INCREMENT, channelID bigint UNSIGNED)")
#mycursor.execute("CREATE Table t_count (count bigint UNSIGNED, uniID bigint UNSIGNED PRIMARY KEY AUTO_INCREMENT)")
#mycursor.execute("CREATE Table b_prefix (prefix VARCHAR(50), uniID bigint UNSIGNED PRIMARY KEY AUTO_INCREMENT)")
#mycursor.execute("CREATE Table t_owners (userID bigint UNSIGNED, channelID bigint UNSIGNED, uniID bigint UNSIGNED PRIMARY KEY AUTO_INCREMENT)")
#mycursor.execute("CREATE Table t_status (channelID bigint UNSIGNED, status VARCHAR(50), uniID bigint UNSIGNED PRIMARY KEY AUTO_INCREMENT)")
#mycursor.execute("CREATE Table f_id (id bigint UNSIGNED, uniID bigint UNSIGNED PRIMARY KEY AUTO_INCREMENT)")
#mycursor.execute("CREATE Table logs_info (userID bigint UNSIGNED, username VARCHAR(50), count bigint UNSIGNED, role_id bigint UNSIGNED, uniID bigint UNSIGNED PRIMARY KEY AUTO_INCREMENT)")
#mycursor.execute("ALTER TABLE logs_info ADD loa VARCHAR(50) DEFAULT 'No'")
#db.commit()

class MyBot(commands.Bot):
    async def is_owner(self, user: discord.User):
        if user.id == 358594990982561792 or user.id == 891449503276736512:
            return True
        return await super().is_owner(user)

def get_prefix():
    db = mysql.connector.connect(
      host="remotemysql.com",
      user="XPJ9qhFktO",
      passwd="lXPOlT66Pt",
      database="XPJ9qhFktO")
    mycursor = db.cursor()
    mycursor.execute(f"SELECT prefix FROM b_prefix WHERE uniID = 1")
    for i in mycursor:
      prefix = str(i[0])
    mycursor.close()
    db.close()
    return prefix

def perChaseage(part, whole):
  return round(100 * float(part)/float(whole), 2)

TOKEN = "OTQxMTk1NTMyODU1MDQyMDc4.YgSapQ.9FxYA-TGU4S9Sw8sgvVt05Elj_s"

intents = discord.Intents.all()
intents.members = True

bot = MyBot(command_prefix=get_prefix(), intents=intents, case_insensitive=True, help_command=None)
tracker = DiscordUtils.InviteTracker(bot)

bot.load_extension("jishaku")

@tasks.loop(minutes=30)
async def check_messages():
  db = mysql.connector.connect(
    host="remotemysql.com",
    user="XPJ9qhFktO",
    passwd="lXPOlT66Pt",
    database="XPJ9qhFktO")
  mycursor = db.cursor()

  mycursor.execute(f"SELECT * FROM snipe_info")
  data = mycursor.fetchall()

  for i in data:
    timestamp = i[3]
    if time.time() - timestamp > 43200:
      mycursor.execute(f"DELETE FROM snipe_info WHERE uni_id = '{i[4]}'")
  db.commit()
  mycursor.close()
  db.close()

@bot.event
async def on_ready():    
  print(f"Connected To Discord User: {bot.user.name}#{bot.user.discriminator}")

@bot.listen()
async def on_command_error(ctx, error):
  if isinstance(error, CommandNotFound):
    pass
  elif isinstance(error, commands.CommandOnCooldown):
    hours = int(time.time() + error.retry_after)
    await ctx.reply(f"> You're doing that too quickly, try again **<t:{hours}:R>**")

@bot.command()
async def whois(ctx, user : discord.User=None):
  guild = bot.get_guild(713213895073857548)
  rolelist = []
  
  
  if user == None: # If no user was provided
        
    member1 = guild.get_member(ctx.author.id)
    memberfetch = await bot.fetch_user(ctx.author.id)
    
    banner = memberfetch.banner
    
    highestrole_color = member1.roles[-1].color
    
    embed = discord.Embed(color=maincolor)
    embed.set_author(name=f"{member1.name}#{member1.discriminator}")
    embed.set_thumbnail(url=member1.display_avatar.url)
        
    createddate = member1.created_at
    created_date = int(createddate.timestamp())
    
    joineddate = member1.joined_at
    joined_date = int(joineddate.timestamp())
    
    roles = member1.roles[1:]
    for i in roles:
      if i.id == 810934999703355402 or i.id == 810935095589863474:
        pass
      else:
        rolelist.append(i.mention)
    rolelist.reverse()
    var2 = f"\n".join(rolelist)
    
    embed.add_field(name=f"**Display Name**", value=member1.display_name, inline=False)
    embed.add_field(name=f"**Developer ID**", value=member1.id, inline=False)
    
    embed.add_field(name=f"**Server Join Date**", value=f"<t:{joined_date}:f>", inline=False)
    embed.add_field(name=f"**Account Creation Date**", value=f"<t:{created_date}:f>", inline=False)
      
    embed.add_field(name=f"**Role(s) [{len(rolelist)}]**", value=f"{var2}", inline=False)
    
    
    fetchauthor = await bot.fetch_user(ctx.author.id)
    
    embed.set_footer(text=f"Command Author: {member1.name}#{member1.discriminator} • {member1.id}", icon_url=fetchauthor.display_avatar.url)
        
    if banner != None:
      class Google(discord.ui.View):
        def __init__(self):
          super().__init__(timeout=None)
          self.add_item(discord.ui.Button(label="View User's Banner", url=banner.url))
      await ctx.reply(embed=embed, view=Google())
    elif banner == None:
      await ctx.reply(embed=embed)
  elif user != None: # If user was provided
    
    if user.bot == True: # If user is bot
      member1 = guild.get_member(user.id)
      author = guild.get_member(ctx.author.id)
            
      highestrole_color = member1.roles[-1].color
      
      embed = discord.Embed(color=maincolor)
      embed.set_author(name=f"{member1.name}#{member1.discriminator}")
      embed.set_thumbnail(url=member1.display_avatar.url)
          
      createddate = member1.created_at
      created_date = int(createddate.timestamp())
      
      joineddate = member1.joined_at
      joined_date = int(joineddate.timestamp())
      
      roles = member1.roles[1:]
      for i in roles:
        if i.id == 810934999703355402 or i.id == 810935095589863474:
          pass
        else:
          rolelist.append(i.mention)
      rolelist.reverse()
      var2 = f"\n".join(rolelist)
      
      embed.add_field(name=f"**Display Name**", value=member1.display_name, inline=False)
      embed.add_field(name=f"**Developer ID**", value=member1.id, inline=False)
      
      embed.add_field(name=f"**Server Join Date**", value=f"<t:{joined_date}:f>", inline=False)
      embed.add_field(name=f"**Account Creation Date**", value=f"<t:{created_date}:f>", inline=False)
      
      embed.add_field(name=f"**Role(s) [{len(rolelist)}]**", value=f"{var2}", inline=False)
      
      
      fetchauthor = await bot.fetch_user(ctx.author.id)
      
      embed.set_footer(text=f"Command Author: {author.name}#{author.discriminator} • {author.id}", icon_url=fetchauthor.display_avatar.url)
          
      await ctx.reply(embed=embed)
    elif user.bot == False: # If user is not a bot
      
      checkmember = guild.get_member(user.id)
      if checkmember != None: # If member is in the server
        member2 = guild.get_member(user.id)
        memberfetch2 = await bot.fetch_user(user.id)
        author2 = guild.get_member(ctx.author.id)
        
        banner2 = memberfetch2.banner
        
        highestrole_color = member2.roles[-1].color

        embed1 = discord.Embed(color=maincolor)
        embed1.set_author(name=f"{member2.name}#{member2.discriminator}")
        embed1.set_thumbnail(url=memberfetch2.display_avatar.url)
            
        createddate = member2.created_at
        created_date1 = int(createddate.timestamp())
        
        joineddate = member2.joined_at
        joined_date1 = int(joineddate.timestamp())
        
        roles = member2.roles[1:]
        for i in roles:
          if i.id == 810934999703355402 or i.id == 810935095589863474:
            pass
          else:
            rolelist.append(i.mention)
        rolelist.reverse()
        var2 = f"\n".join(rolelist)
        
        embed1.add_field(name=f"**Display Name**", value=member2.display_name, inline=False)
        embed1.add_field(name=f"**Developer ID**", value=member2.id, inline=False)
        
        embed1.add_field(name=f"**Server Join Date**", value=f"<t:{joined_date1}:f>", inline=False)
        embed1.add_field(name=f"**Account Creation Date**", value=f"<t:{created_date1}:f>", inline=False)
        
        embed1.add_field(name=f"**Role(s) [{len(rolelist)}]**", value=f"{var2}", inline=False)
        
        
        fetchauthor = await bot.fetch_user(ctx.author.id)
                
        embed1.set_footer(text=f"Command Author: {author2.name}#{author2.discriminator} • {author2.id}", icon_url=fetchauthor.display_avatar.url)
        if banner2 != None:
          class Google1(discord.ui.View):
            def __init__(self):
              super().__init__(timeout=None)
              self.add_item(discord.ui.Button(label="View User's Banner", url=banner2.url))
          await ctx.reply(embed=embed1, view=Google1())
        elif banner2 == None:
          await ctx.reply(embed=embed1)
      elif checkmember == None: # If member is not in the server
        
        memberfetch2 = await bot.fetch_user(user.id)
        author2 = guild.get_member(ctx.author.id)
        
        banner2 = memberfetch2.banner
        
        embed1 = discord.Embed(color=maincolor)
        embed1.set_author(name=f"{memberfetch2.name}#{memberfetch2.discriminator}")
        embed1.set_thumbnail(url=memberfetch2.display_avatar.url)
            
        createddate = memberfetch2.created_at
        created_date1 = int(createddate.timestamp())
        
        embed1.add_field(name=f"**Display Name**", value=memberfetch2.display_name, inline=False)
        embed1.add_field(name=f"**Developer ID**", value=memberfetch2.id, inline=False)
        
        embed1.add_field(name=f"**Account Creation Date**", value=f"<t:{created_date1}:f>", inline=False)
        
        fetchauthor = await bot.fetch_user(ctx.author.id)
                
        embed1.set_footer(text=f"Command Author: {author2.name}#{author2.discriminator} • {author2.id}", icon_url=fetchauthor.display_avatar.url)
        if banner2 != None:
          class Google1(discord.ui.View):
            def __init__(self):
              super().__init__(timeout=None)
              self.add_item(discord.ui.Button(label="View User's Banner", url=banner2.url))
          await ctx.reply(embed=embed1, view=Google1())
        elif banner2 == None:
          await ctx.reply(embed=embed1)

@bot.command(aliases=['b'])
@commands.has_permissions(ban_members=True)
async def ban(ctx, user:discord.User=None, *, reason=None):
  guild = bot.get_guild(713213895073857548)
  if reason == None:
    reason = "No reason given."
  if user == None:
    await ctx.reply("Please specify a user to ban.")
    return
  else:
    try:
      ban = await guild.fetch_ban(user)
      ban = True
    except NotFound:
      ban = False
    if ban == True:
      await ctx.reply("The user is already banned.")
      return
    else:
      
      checkmember = guild.get_member(user.id)
      if checkmember != None:
        if checkmember.guild_permissions.administrator == True:
          await ctx.reply("You don't have perms to ban this user.")
          return
      
      class yesCancel(discord.ui.View):
        def __init__(self):
          super().__init__(timeout=None)
        @discord.ui.button(row=0, label='Yes', style=discord.ButtonStyle.green, custom_id="yes", disabled=False)
        async def button_callback1(self, button, interaction):
          
          if interaction.user.id != ctx.author.id:
            return await interaction.response.send_message(content=f"You can't use this.", ephemeral=True)
          
          try:
            dmchannel = await user.create_dm()
            emee = discord.Embed(description=f"You've been **banned** from {guild.name} by {ctx.author.mention}\nReason: {reason}", color=maincolor)
            await dmchannel.send(embed=emee)
          except Forbidden:
            pass
          await guild.ban(user, reason=reason, delete_message_days=0)
          emba = discord.Embed(color=maincolor)
          emba.add_field(name=f"{user.name}#{user.discriminator} has been banned.", value=f"Reason: {reason}")
          await interaction.message.reply(embed=emba)

          for child in self.children:
            child.disabled = True
          await interaction.message.edit(view=self)
          
          await interaction.response.defer()

          logs_c = bot.get_channel(763791851139629086)
          embed = discord.Embed(title="Member Banned", description=f"[Jump to Command]({ctx.message.jump_url})", color=maincolor)
          embed.set_author(name=f"{ctx.author.name}#{ctx.author.discriminator}", icon_url=f"{ctx.author.display_avatar.url}")
          embed.add_field(name="Staff Responsible", value=ctx.author.mention, inline=True)
          embed.add_field(name="User", value=user.mention, inline=True)
          embed.add_field(name="Reason", value=reason, inline=True)
          embed.add_field(name="Channel", value=ctx.channel.mention, inline=True)
          await logs_c.send(embed=embed)

          
        @discord.ui.button(row=0, label='Cancel', style=discord.ButtonStyle.red, custom_id="cancel", disabled=False)
        async def button_callback2(self, button, interaction):
      
          if interaction.user.id != ctx.author.id:
            return await interaction.response.send_message(content=f"You can't use this.", ephemeral=True)
          
          await interaction.message.reply("Cancelled.")
          
          for child in self.children:
            child.disabled = True
          await interaction.message.edit(view=self)
          
          await interaction.response.defer()
      
      warningembed = discord.Embed(title="WARNING", description="Are you sure you would like to execute this command?", color=maincolor)
      await ctx.reply(embed=warningembed, view=yesCancel())

@ban.error
async def ban_error(ctx, error):
  if isinstance(error, commands.UserNotFound):
    await ctx.reply("User wasn't found aka. invalid ID/User.")

@bot.command(aliases=['ub'])
@commands.has_permissions(ban_members=True)
async def unban(ctx, user:discord.User=None):
  guild = bot.get_guild(713213895073857548)
  if user == None:
    await ctx.reply("Please specify a user to unban.")
    return
  else:
    try:
      ban = await guild.fetch_ban(user)
      ban = True
    except NotFound:
      ban = False
    if ban == False:
      await ctx.reply("The user is not banned.")
      return
    else:
      await guild.unban(user)
      emba = discord.Embed(description=f"{user.name}#{user.discriminator} has been unbanned.", color=maincolor)
      await ctx.reply(embed=emba)
                
      logs_c = bot.get_channel(763791851139629086)
      embed = discord.Embed(title="Member Unbanned", description=f"[Jump to Command]({ctx.message.jump_url})", color=maincolor)
      embed.set_author(name=f"{ctx.author.name}#{ctx.author.discriminator}", icon_url=f"{ctx.author.display_avatar.url}")
      embed.add_field(name="Staff Responsible", value=ctx.author.mention, inline=True)
      embed.add_field(name="User", value=user.mention, inline=True)
      embed.add_field(name="Channel", value=ctx.channel.mention, inline=True)
      await logs_c.send(embed=embed)

@unban.error
async def unban_error(ctx, error):
  if isinstance(error, commands.UserNotFound):
    await ctx.reply("User wasn't found aka. invalid ID/User.")

@bot.command()
@commands.cooldown(1, 5, commands.BucketType.user)
async def snipe(ctx, arg1=None):
  snipeall = False
  if arg1 != None:
    if arg1 == "all":
     snipeall = True

  db = mysql.connector.connect(
    host="remotemysql.com",
    user="XPJ9qhFktO",
    passwd="lXPOlT66Pt",
    database="XPJ9qhFktO")
  mycursor = db.cursor()
  
  if snipeall == False:
    mycursor.execute(f"SELECT * FROM snipe_info WHERE channel_id = '{ctx.channel.id}' ORDER BY time DESC")
    data = mycursor.fetchall()
    if len(data) == 0:
      return await ctx.reply("There are no messages to snipe!")
    
    time = f"<t:{data[0][3]}:R>"
    
    embed=discord.Embed(description=f"__**Deleted Since:** {time}__\n>>> {data[0][2]}", color=maincolor)
    user = await bot.fetch_user(int(data[0][1]))
    embed.set_author(name=f"{user.name}#{user.discriminator}", icon_url=f"{user.display_avatar.url}")
    embed.set_footer(text="Latest deleted message.")
    
  elif snipeall == True:
    mycursor.execute(f"SELECT * FROM snipe_info WHERE channel_id = '{ctx.channel.id}' ORDER BY time DESC")
    data = mycursor.fetchall()
    if len(data) == 0:
      return await ctx.reply("There are no messages to snipe!")
    
    embed=discord.Embed(color=maincolor)
    embed.set_footer(text=f"Latest {len(data[:10])} deleted messages.")
    
    for i in data[:10]:
      time = f"<t:{i[3]}:R>"
      user = await bot.fetch_user(int(i[1]))
      embed.add_field(name=f"From: `{user.name}#{user.discriminator}`", value=f"__**Deleted Since:** {time}__\n>>> {i[2]}", inline=False)
    
  await ctx.reply(embed=embed)

@bot.event
async def on_message_delete(message):
  
  if message.guild.id == 713213895073857548:
    if len(message.content) == 0:
      return
    if len(message.content) < 1000:
      content = message.content
      userid = message.author.id
      channelid = message.channel.id
      time = math.trunc(datetime.now().timestamp())

      db = mysql.connector.connect(
        host="remotemysql.com",
        user="XPJ9qhFktO",
        passwd="lXPOlT66Pt",
        database="XPJ9qhFktO")
      mycursor = db.cursor()
      
      mycursor.execute("INSERT INTO snipe_info (channel_id, user_id, content, time) VALUES (%s, %s, %s, %s)", (channelid, userid, content, time))
      db.commit()
      
      mycursor.close()
      db.close()
      
      c = bot.get_channel(763791851139629086)
      embed = discord.Embed(title="Message Deleted", color=maincolor)
      embed.set_author(name=f"{message.author.name}#{message.author.discriminator}", icon_url=f"{message.author.display_avatar.url}")
      embed.add_field(name="User", value=message.author.mention, inline=True)
      embed.add_field(name="Message Content", value=message.content, inline=True)
      embed.add_field(name="Channel", value=message.channel.mention, inline=True)
      await c.send(embed=embed)

@bot.event
async def on_message_edit(before_msg, after_msg):
  
  if before_msg.guild.id == 713213895073857548:
    if len(before_msg.content) < 1000 and len(after_msg.content) < 1000:
      
      c = bot.get_channel(763791851139629086)
      embed = discord.Embed(title="Message Deleted", description=f"[Jump to Message]({before_msg.jump_url})", color=maincolor)
      embed.set_author(name=f"{before_msg.author.name}#{before_msg.author.discriminator}", icon_url=f"{before_msg.author.display_avatar.url}")
      embed.add_field(name="User", value=before_msg.author.mention, inline=True)
      embed.add_field(name="Old Message", value=before_msg.content, inline=True)
      embed.add_field(name="New Message", value=after_msg.content, inline=True)
      embed.add_field(name="Channel", value=before_msg.channel.mention, inline=True)
      await c.send(embed=embed)


@bot.command()
@commands.has_permissions(manage_messages=True)
async def purge(ctx, limit=None):
  if limit == None:
    return await ctx.reply(embed=discord.Embed(description="Specify a number of messages to purge.", color=maincolor))
  
  try:
    limit = int(limit)
  except ValueError:
    return await ctx.reply(embed=discord.Embed(description="The amount of messages must be a number!", color=maincolor))
  
  if limit == 0:
    return await ctx.reply(embed=discord.Embed(description="The number of messages cannot be 0 !", color=maincolor))
  
  msgs = await ctx.channel.purge(limit=limit+1, oldest_first=False, bulk=True)
  limit = limit-1
  succembed = discord.Embed(description=f"Successfully purged {len(msgs)-1} messages.", color=maincolor)
  await ctx.send(embed=succembed)
  
  msg_string = ""
  for msg in msgs:
    msg_string += f"{msg.author.name}#{msg.author.discriminator} - {msg.content}\n"
  buffer = io.StringIO()
  buffer.name = "messages.txt"
  buffer.write(msg_string)
  buffer.seek(0)
  
  c = bot.get_channel(763791851139629086)
  embed = discord.Embed(title=f"Purged {len(msgs)-1} messages", color=maincolor)
  embed.set_author(name=f"{ctx.author.name}#{ctx.author.discriminator}", icon_url=f"{ctx.author.display_avatar.url}")
  embed.add_field(name="Staff Responsible", value=ctx.author.mention, inline=True)
  embed.add_field(name="Channel", value=ctx.channel.mention, inline=True)
  await c.send(embed=embed, file=discord.File(buffer, 'messages.txt'))

@bot.command()
@commands.has_permissions(manage_roles=True)
async def role(ctx, user : discord.User=None, roleName=None):
  if user == None:
    return await ctx.reply("Specfiy a user.")
    
  if roleName == None:
    return await ctx.reply("Specify a role, either role name or id.")
  
  checkmember = ctx.guild.get_member(user.id)
  if checkmember == None:
    return await ctx.reply("User wasn't found aka. invalid ID/User.")
  
  user = ctx.guild.get_member(user.id)
  
  isID = True
  
  try:
    roleID = int(roleName)
  except ValueError:
    isID = False
    
  if isID == False:
    
    rolename = roleName
    rolenames = []
    for i in ctx.guild.roles:
      if i != ctx.guild.default_role:
        rolenames.append(i.name)
    closeststr = difflib.get_close_matches(rolename, rolenames)
    if len(closeststr) == 0:
      return await ctx.reply("Role wasn't found.")
    
    role = discord.utils.find(lambda r: r.name == closeststr[0], ctx.guild.roles)
    
    if role in user.roles:
      await user.remove_roles(role)
      embe = discord.Embed(color=maincolor)
      embe.set_author(name=f"Revoked {closeststr[0]} from {user.name}#{user.discriminator}.", icon_url="https://images-ext-1.discordapp.net/external/Aue9ejC5ry1-iQKF7q5AxHAirITlIse3vKlanl4kfMo/%3Fsize%3D80%26quality%3Dlossless/https/cdn.discordapp.com/emojis/926397583981686814.png")
    
      logs_c = bot.get_channel(763791851139629086)
      embed = discord.Embed(title="Role Removed", description=f"[Jump to Command]({ctx.message.jump_url})", color=maincolor)
      embed.set_author(name=f"{ctx.author.name}#{ctx.author.discriminator}", icon_url=f"{ctx.author.display_avatar.url}")
      embed.add_field(name="Staff Responsible", value=ctx.author.mention, inline=True)
      embed.add_field(name="User", value=user.mention, inline=True)
      embed.add_field(name="Role", value=role.mention, inline=True)
      embed.add_field(name="Channel", value=ctx.channel.mention, inline=True)
      await logs_c.send(embed=embed)
    
    else:
      await user.add_roles(role)
      embe = discord.Embed(color=maincolor)
      embe.set_author(name=f"Applied {closeststr[0]} to {user.name}#{user.discriminator}.", icon_url="https://images-ext-1.discordapp.net/external/Aue9ejC5ry1-iQKF7q5AxHAirITlIse3vKlanl4kfMo/%3Fsize%3D80%26quality%3Dlossless/https/cdn.discordapp.com/emojis/926397583981686814.png")

      logs_c = bot.get_channel(763791851139629086)
      embed = discord.Embed(title="Role Added", description=f"[Jump to Command]({ctx.message.jump_url})", color=maincolor)
      embed.set_author(name=f"{ctx.author.name}#{ctx.author.discriminator}", icon_url=f"{ctx.author.display_avatar.url}")
      embed.add_field(name="Staff Responsible", value=ctx.author.mention, inline=True)
      embed.add_field(name="User", value=user.mention, inline=True)
      embed.add_field(name="Role", value=role.mention, inline=True)
      embed.add_field(name="Channel", value=ctx.channel.mention, inline=True)
      await logs_c.send(embed=embed)

    await ctx.reply(embed=embe)
    
  else:
    
    role = ctx.guild.get_role(roleID)
    if role == None:
      return await ctx.reply("Role wasn't found.")

    if role in user.roles:
      await user.remove_roles(role)
      embe = discord.Embed(color=maincolor)
      embe.set_author(name=f"Revoked {role.name} from {user.name}#{user.discriminator}.", icon_url="https://images-ext-1.discordapp.net/external/Aue9ejC5ry1-iQKF7q5AxHAirITlIse3vKlanl4kfMo/%3Fsize%3D80%26quality%3Dlossless/https/cdn.discordapp.com/emojis/926397583981686814.png")

      logs_c = bot.get_channel(763791851139629086)
      embed = discord.Embed(title="Role Removed", description=f"[Jump to Command]({ctx.message.jump_url})", color=maincolor)
      embed.set_author(name=f"{ctx.author.name}#{ctx.author.discriminator}", icon_url=f"{ctx.author.display_avatar.url}")
      embed.add_field(name="Staff Responsible", value=ctx.author.mention, inline=True)
      embed.add_field(name="User", value=user.mention, inline=True)
      embed.add_field(name="Role", value=role.mention, inline=True)
      embed.add_field(name="Channel", value=ctx.channel.mention, inline=True)
      await logs_c.send(embed=embed)
    
    else:
      await user.add_roles(role)
      embe = discord.Embed(color=maincolor)
      embe.set_author(name=f"Applied {role.name} to {user.name}#{user.discriminator}.", icon_url="https://images-ext-1.discordapp.net/external/Aue9ejC5ry1-iQKF7q5AxHAirITlIse3vKlanl4kfMo/%3Fsize%3D80%26quality%3Dlossless/https/cdn.discordapp.com/emojis/926397583981686814.png")

      logs_c = bot.get_channel(763791851139629086)
      embed = discord.Embed(title="Role Added", description=f"[Jump to Command]({ctx.message.jump_url})", color=maincolor)
      embed.set_author(name=f"{ctx.author.name}#{ctx.author.discriminator}", icon_url=f"{ctx.author.display_avatar.url}")
      embed.add_field(name="Staff Responsible", value=ctx.author.mention, inline=True)
      embed.add_field(name="User", value=user.mention, inline=True)
      embed.add_field(name="Role", value=role.mention, inline=True)
      embed.add_field(name="Channel", value=ctx.channel.mention, inline=True)
      await logs_c.send(embed=embed)
      
    await ctx.reply(embed=embe)

@role.error
async def role(ctx, error):
  if isinstance(error, commands.UserNotFound):
    await ctx.reply("User wasn't found aka. invalid ID/User.")

@bot.command()
@commands.has_permissions(moderate_members=True)
async def mute(ctx, member : discord.Member=None, duration=None):
  time_convert = {"s":1, "m":60, "h":3600,"d":86400}
  if member == None and duration==None:
    await ctx.reply(f"Invalid usuage.\n*`usuage: {get_prefix()}mute @user duration (e.g. of duration: 10s = 10 secs / 10h = 10 hours / 10d = 10 days)`*")
    return
  elif member != None and duration != None:
    try:
      
      if member.guild_permissions.administrator == True:
        await ctx.reply("You don't have perms to mute this user.")
        return

      letter = str(duration[-1])
      number = int(duration[:-1])
      if letter == "s" or letter == "m" or letter == "h" or letter == "d":
        
        timeout = int(duration[:-1]) * time_convert[duration[-1]]
        if timeout > 2419200:
          await ctx.reply("The duration cannot be longer than 28 days!")
          return
        else:
          
          time = timedelta(seconds=timeout)
          await member.timeout_for(time)
          
          if letter == "s":
            emba = discord.Embed(description=f"{member.name}#{member.discriminator} has been muted for {number} second/s", color=maincolor)
            typee = f"{number} second/s"
            await ctx.reply(embed=emba)
          elif letter == "m":
            emba = discord.Embed(description=f"{member.name}#{member.discriminator} has been muted for {number} minute/s", color=maincolor)
            typee = f"{number} minute/s"
            await ctx.reply(embed=emba)
          elif letter == "h":
            emba = discord.Embed(description=f"{member.name}#{member.discriminator} has been muted for {number} hour/s", color=maincolor)
            typee = f"{number} hour/s"
            await ctx.reply(embed=emba)
          elif letter == "d":
            emba = discord.Embed(description=f"{member.name}#{member.discriminator} has been muted for {number} day/s", color=maincolor)
            typee = f"{number} day/s"
            await ctx.reply(embed=emba)
          
          until = datetime.now() + timedelta(seconds=timeout)
          logs_c = bot.get_channel(763791851139629086)
          embed = discord.Embed(title="Role Added", description=f"[Jump to Command]({ctx.message.jump_url})", color=maincolor)
          embed.set_author(name=f"{ctx.author.name}#{ctx.author.discriminator}", icon_url=f"{ctx.author.display_avatar.url}")
          embed.add_field(name="Staff Responsible", value=ctx.author.mention, inline=True)
          embed.add_field(name="User", value=member.mention, inline=True)
          embed.add_field(name="Muted For", value=f"{typee} -> <t:{int(until.timestamp())}:f>", inline=True)
          embed.add_field(name="Channel", value=ctx.channel.mention, inline=True)
          await logs_c.send(embed=embed)

      else:
        await ctx.reply(f"Invalid usuage.\n*`usuage: {get_prefix()}mute @user duration (e.g. of duration: 10s = 10 secs / 10h = 10 hours / 10d = 10 days)`*")
        return
          
    except ValueError:
      await ctx.reply("Duration must be a number!")
      return
  else:
    if member == None:
      await ctx.reply("Please specify a user to timeout.")
      return
    else:
      if duration == None:
        await ctx.reply("Please state the duration `(e.g. of duration: 10s = 10 secs / 10h = 10 hours / 10d = 10 days)`")
        return

bot.run(TOKEN)