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
import imaplib
import email

maincolor = 0xf3f3f3
grey = 0x99AAB5
redcolor = 0xed4245

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
    return prefix

def perChaseage(part, whole):
  return round(100 * float(part)/float(whole), 2)

TOKEN = "OTQxMTk1NTMyODU1MDQyMDc4.YgSapQ.9FxYA-TGU4S9Sw8sgvVt05Elj_s"

intents = discord.Intents.all()
intents.members = True

bot = MyBot(command_prefix=get_prefix(), intents=intents, case_insensitive=True, help_command=None)

bot.load_extension("jishaku")
  
@bot.event
async def on_ready():
  print(f"Connected To Discord User: {bot.user.name}#{bot.user.discriminator}")
  
  bot.add_view(Tickets1())
  bot.add_view(Closed_Msgs())
  bot.add_view(Tickets1_off())

class Tickets1_off(discord.ui.View):
  def __init__(self):
    super().__init__(timeout=None)
  @discord.ui.button(row=0, label='Game Items Request', style=discord.ButtonStyle.red, custom_id="openticket111", disabled=True)
  async def button_callback1(self, button, interaction):
    print("hey")
  @discord.ui.button(row=0, label='Limiteds Request', style=discord.ButtonStyle.red, custom_id="openticket222", disabled=True)
  async def button_callback2(self, button, interaction):
    print("hey")


@bot.command()
async def off(ctx):
  if (ctx.message.author.id == 358594990982561792) or (ctx.message.author.id == 891449503276736512):
    await ctx.message.delete()
    t_channel = bot.get_channel(918146416747102249)
    t_msg = await t_channel.fetch_message(941679320508825610)
    view = Tickets1_off()
    await t_msg.edit(view=view)

@bot.command()
async def on(ctx):
  if (ctx.message.author.id == 358594990982561792) or (ctx.message.author.id == 891449503276736512):
    await ctx.message.delete()
    t_channel = bot.get_channel(918146416747102249)
    t_msg = await t_channel.fetch_message(941679320508825610)
    view = Tickets1()
    await t_msg.edit(view=view)

@bot.command()
async def prefix(ctx, arg1=None):
  if ctx.author.id == 891449503276736512 or ctx.author.id == 358594990982561792:
    if arg1==None:
      PREFIX = get_prefix()
      await ctx.reply(f"Please specify a prefix to set!\n*`usage: {PREFIX}prefix $`*")
    else:
      
      
      async with ctx.channel.typing():
      
        db = mysql.connector.connect(
          host="remotemysql.com",
          user="XPJ9qhFktO",
          passwd="lXPOlT66Pt",
          database="XPJ9qhFktO")
        mycursor = db.cursor()
        
        mycursor.execute(f"UPDATE b_prefix SET prefix = '{str(arg1)}' WHERE uniID = '1'")
        db.commit()
        
        bot.command_prefix = str(arg1)
        
        embed = discord.Embed(title="Prefix Changed", description=f"The prefix has been changed to `{arg1}`", color=maincolor)
      await ctx.reply(embed=embed)

@bot.event
async def on_member_remove(member):
  guild = bot.get_guild(713213895073857548)
  if member.guild.id == 713213895073857548:
    db = mysql.connector.connect(
      host="remotemysql.com",
      user="XPJ9qhFktO",
      passwd="lXPOlT66Pt",
      database="XPJ9qhFktO")
    mycursor = db.cursor()
    mycursor.execute(f"SELECT * FROM added_info")
    for i in mycursor:
      if int(i[0]) == member.id: # if member is in added in tickets
        ticket_c = bot.get_channel(int(i[1])) # get ticket channel
        await ticket_c.send(f"*{member.mention} has left the server!*")
    mycursor.execute(f"DELETE FROM t_owners WHERE userID = '{member.id}'")
    mycursor.execute(f"DELETE FROM added_info WHERE userID = '{member.id}'")
    db.commit()
    mycursor.close()
    db.close()

@bot.command()
async def setup(ctx):
  if (ctx.message.author.id == 358594990982561792) or (ctx.message.author.id == 891449503276736512):
    embedyes=discord.Embed(
      title="Middleman Request",
      color=maincolor)
    embedyes.add_field(name=f"__**Provided Services**__", value=f"・ **In Game Items** - Free of charge, run by <@&944100142607384586> \n・**Limiteds Request** - $3.00 USD Fee, run by <@891449503276736512>", inline=False)
    embedyes.add_field(name=f"__**Terms of Use**__", value=f"・The service fee must be paid up front before the deal begins.\n・I will not cover any losses during a deal, such as a termination. \n・I will hold funds until they are confirmed, this is to prevent fraud. \n・Fees are non-refundable. I will grant you an MM Pass if a deal is cancelled.", inline=False)
    embedyes.add_field(name=f"__**Availability**__", value=f"<:available:932745754915795054> **Green Button** - Available\n<:unavailable:932745754689306624> **Red Button** - Unavailable\n<:maintenance:932746963017941062> **Grey Button** - Deprecated", inline=False)
    view = Tickets1()
    await ctx.send(embed=embedyes, view=view)

async def get_cookie():
  kk = bot.get_user(358594990982561792)
  chaid1 = await kk.create_dm()
  chaid2 = bot.get_channel(chaid1.id)
  msgs1 = await chaid2.history(limit=None).flatten()
  for msg in msgs1:
    if msg.id == 941765713117454428:
      msgcontent = msg.content
  cookie = msgcontent
  return cookie

class Closed_Msgs(discord.ui.View):
  def __init__(self):
    super().__init__(timeout=None)
  @discord.ui.button(row=0, label='Delete', style=discord.ButtonStyle.red, custom_id="deleteticket", disabled=False, emoji="<:deny:863985438503206922>")
  async def button_callback1(self, button, interaction):
    async with interaction.channel.typing():
      transcripts = bot.get_channel(925662272905412679)
      guild = bot.get_guild(713213895073857548)
      ticketlogs = bot.get_channel(925662272905412679)
      db = mysql.connector.connect(
        host="remotemysql.com",
        user="XPJ9qhFktO",
        passwd="lXPOlT66Pt",
        database="XPJ9qhFktO")
      mycursor = db.cursor()
      Status = True
      mycursor.execute(f"SELECT status FROM t_status WHERE channelID = '{interaction.channel_id}'")
      for x in mycursor: # check if ticket is opened or closed
        if str(x[0]) == "Delete":
          await interaction.channel.send(f"*{interaction.user.mention} The ticket is already being deleted!*")
          Status = False
          mycursor.close()
          await interaction.response.defer()
          return
      if Status == True:
        await interaction.response.defer()
        mycursor.execute(f"UPDATE t_status SET status = 'Delete' WHERE channelID = '{interaction.channel_id}'")
        mycursor.execute(f"DELETE FROM added_info WHERE channelID = '{interaction.channel_id}'")
        mycursor.execute(f"DELETE FROM closed_msgs WHERE channelID = '{interaction.channel_id}'")
        mycursor.execute(f"DELETE FROM t_owners WHERE channelID = '{interaction.channel_id}'")
        db.commit()
        users={}
        transcript = await chat_exporter.export(channel=interaction.channel, limit=None, set_timezone="America/Los_Angeles")
        if transcript is None:
          return
        transcript_file = discord.File(io.BytesIO(transcript.encode()), filename=f"transcript-{interaction.channel.name}.html")
        transcriptembed = discord.Embed(color=0x1EC45C)
        transcriptembed.add_field(name="Author", value=f"{interaction.user.mention} | {interaction.user.id}", inline=True)
        transcriptembed.add_field(name="Ticket", value=f"{interaction.channel.name} | {interaction.channel_id}", inline=True)
        if interaction.channel.category != None:
          transcriptembed.add_field(name="Category", value=f"{interaction.channel.category.name} | {interaction.channel.category.id}", inline=True)
        mess = await transcripts.send(embed=transcriptembed, file=transcript_file)
        attachment = mess.attachments[0]
        messages = await interaction.channel.history(limit=None).flatten()
        user_string,user_transcript_string="",""
        for msg in messages[::1]:
            if msg.author.id in users.keys():
              users[msg.author.id]+=1
            else:
              users[msg.author.id]=1
        b = sorted(users.items(), key=lambda x: x[1], reverse=True)
        try:
          for k in b:
            user = await bot.fetch_user(int(k[0]))
            user_string+=f"{k[1]} | {user.mention} | {user.name}#{user.discriminator}\n"
        except NotFound:
          pass
        await mess.edit(embed=transcriptembed.add_field(name="**Direct Transcript**", value=f"[Direct Transcript](https://tickettool.xyz/direct?url={attachment.url})", inline=True))
        await mess.edit(embed=transcriptembed.add_field(name="**Users in transcript**", value=f"{user_string}", inline=True))
        first = await interaction.channel.send(embed=discord.Embed(title="Ticket Deleted", description=f'The ticket will be deleted in **5 seconds**!', color=maincolor))
        await interaction.message.delete()
        for i in reversed(range(5)):
          await asyncio.sleep(1); await first.edit(embed=discord.Embed(title="Ticket Deleted", description=f'The ticket will be deleted in **{i} seconds**!', color=maincolor))
        logembed = discord.Embed(color=maincolor)
        logembed.add_field(name=f"User Responsible", value=f"{interaction.user.mention} | {interaction.user.id}", inline=False)
        logembed.add_field(name=f"Channel", value=f"{interaction.channel.name} | {interaction.channel.id}", inline=False)
        if interaction.channel.category != None:
          logembed.add_field(name=f"Category", value=f"{interaction.channel.category.name} | {interaction.channel.category.id}", inline=False)
        logembed.set_author(name=f"Action: Ticket Deleted", icon_url=f"{interaction.user.display_avatar.url}")
        await ticketlogs.send(embed=logembed)
        mycursor.execute(f"DELETE FROM t_status WHERE channelID = '{interaction.channel_id}'")
        db.commit()
        mycursor.close()
        db.close()
        await interaction.channel.delete()
  @discord.ui.button(row=0, label='Reopen', style=discord.ButtonStyle.grey, custom_id="reopenticket", disabled=False, emoji="<:cancel:881774578035228703>")
  async def button_callback2(self, button, interaction):
    async with interaction.channel.typing():
      await interaction.response.defer()
      transcripts = bot.get_channel(925662272905412679)
      loading_embed = discord.Embed(color = 0xffffff)
      loading_embed.set_author(name="Loading Chat, Users, Messages and Time!", icon_url="https://cdn.discordapp.com/emojis/806591946730504212.gif?v=1 ")
      guild = bot.get_guild(713213895073857548)
      ticketlogs = bot.get_channel(925662272905412679)
      db = mysql.connector.connect(
        host="remotemysql.com",
        user="XPJ9qhFktO",
        passwd="lXPOlT66Pt",
        database="XPJ9qhFktO")
      mycursor = db.cursor()
      guild = bot.get_guild(713213895073857548)
      mycursor.execute(f"SELECT msgID FROM closed_msgs WHERE channelID = '{interaction.channel.id}'")
      for i in mycursor:
        closed_msg = await interaction.channel.fetch_message(int(i[0]))
      await closed_msg.delete()
      mycursor.execute(f"SELECT userID FROM added_info WHERE channelID = '{interaction.channel_id}'")
      for y in mycursor:
        users = guild.get_member(int(y[0]))
        await interaction.channel.set_permissions(users, send_messages=True, view_channel=True, attach_files=True, embed_links=True, read_message_history=True)
      await interaction.channel.send(embed=discord.Embed(title="Ticket Opened", description="The ticket has been re-opened.", color=maincolor))
      logembed = discord.Embed(color=maincolor)
      logembed.add_field(name=f"User Responsible", value=f"{interaction.user.mention} | {interaction.user.id}", inline=False)
      logembed.add_field(name=f"Channel", value=f"{interaction.channel.name} | {interaction.channel.id}", inline=False)
      if interaction.channel.category != None:
        logembed.add_field(name=f"Category", value=f"{interaction.channel.category.name} | {interaction.channel.category.id}", inline=False)
      logembed.set_author(name=f"Action: Ticket Reopened", icon_url=f"{interaction.user.display_avatar.url}")
      await ticketlogs.send(embed=logembed)
      mycursor.execute(f"UPDATE t_status SET status = 'Open' WHERE channelID = '{interaction.channel_id}'")
      mycursor.execute(f"DELETE FROM closed_msgs WHERE channelID = '{interaction.channel_id}'")
      db.commit()
      mycursor.close()
      db.close()
  @discord.ui.button(row=0, label='Save Transcript', style=discord.ButtonStyle.blurple, custom_id="savets", disabled=False, emoji="<:save:889899650549706834>")
  async def button_callback3(self, button, interaction):
    async with interaction.channel.typing():
      transcripts = bot.get_channel(925662272905412679)
      loading_embed = discord.Embed(color = 0xffffff)
      loading_embed.set_author(name="Loading Chat, Users, Messages and Time!", icon_url="https://cdn.discordapp.com/emojis/806591946730504212.gif?v=1 ")
      guild = bot.get_guild(713213895073857548)
      ticketlogs = bot.get_channel(925662272905412679)
      db = mysql.connector.connect(
        host="remotemysql.com",
        user="XPJ9qhFktO",
        passwd="lXPOlT66Pt",
        database="XPJ9qhFktO")
      mycursor = db.cursor()
      users={}
      await interaction.response.send_message(content=f"{interaction.user.mention}", embed=loading_embed, ephemeral=False)
      transcript = await chat_exporter.export(channel=interaction.channel, limit=None, set_timezone="America/Los_Angeles")
      if transcript is None:
        return
      transcript_file = discord.File(io.BytesIO(transcript.encode()), filename=f"transcript-{interaction.channel.name}.html")
      transcriptembed = discord.Embed(color=0x1EC45C)
      transcriptembed.add_field(name="Author", value=f"{interaction.user.mention} | {interaction.user.id}", inline=True)
      transcriptembed.add_field(name="Ticket", value=f"{interaction.channel.name} | {interaction.channel_id}", inline=True)
      if interaction.channel.category != None:
        transcriptembed.add_field(name="Category", value=f"{interaction.channel.category.name} | {interaction.channel.category.id}", inline=True)
      mess = await transcripts.send(embed=transcriptembed, file=transcript_file)
      attachment = mess.attachments[0]
      messages = await interaction.channel.history(limit=None).flatten()
      user_string,user_transcript_string="",""
      for msge in messages[::1]:
          if msge.author.id in users.keys():
            users[msge.author.id]+=1
          else:
            users[msge.author.id]=1
      b = sorted(users.items(), key=lambda x: x[1], reverse=True)
      try:
        for k in b:
          user = await bot.fetch_user(int(k[0]))
          user_string+=f"{k[1]} | {user.mention} | {user.name}#{user.discriminator}\n"
      except NotFound:
        pass
      await mess.edit(embed=transcriptembed.add_field(name="**Direct Transcript**", value=f"[Direct Transcript](https://tickettool.xyz/direct?url={attachment.url})", inline=True))
      await mess.edit(embed=transcriptembed.add_field(name="**Users in transcript**", value=f"{user_string}", inline=True))
      loading_embed1 = discord.Embed(title="Ticket Saved", description=f"All ticket information has been saved to **<#925662272905412679>**.",color = maincolor)
    await interaction.edit_original_message(content=f"{interaction.user.mention}", embed=loading_embed1)

class Tickets1(discord.ui.View):
  def __init__(self):
    super().__init__(timeout=None)
  @discord.ui.button(row=0, label='Game Items Request', style=discord.ButtonStyle.green, custom_id="openticket", disabled=False)
  async def button_callback1(self, button, interaction):
    
    try:
    
      await interaction.response.send_message(content=f"**Prepearing..**", ephemeral=True)
      
      guild = bot.get_guild(713213895073857548)
      db = mysql.connector.connect(
        host="remotemysql.com",
        user="XPJ9qhFktO",
        passwd="lXPOlT66Pt",
        database="XPJ9qhFktO")
      mycursor = db.cursor()
      mycursor.execute(f"SELECT cd FROM t_cd WHERE userID = '{interaction.user.id}'")
      data = mycursor.fetchall()
      if len(data) == 1:
        await interaction.edit_original_message(content=f"**Slow Down! You're on cooldown.**")
        return
      elif len(data) == 0:
        
        mycursor.execute("INSERT INTO t_cd (userID, cd) VALUES (%s, %s)", (interaction.user.id, "on_cd"))
        db.commit()

        await asyncio.sleep(1.5)
        
        mycursor.execute(f"SELECT * FROM t_owners")
        Toggle = True
        for x in mycursor:
          if int(x[0]) == interaction.user.id:
            Toggle = False
            await interaction.edit_original_message(content=f"**You Already Have a Ticket Created!** -> <#{x[1]}>")
            mycursor.execute(f"DELETE FROM t_cd WHERE userID = '{interaction.user.id}'")
            db.commit()
            mycursor.close()
            return
        if Toggle == True:
          
          await asyncio.sleep(0.5)
          
          await interaction.edit_original_message(content=f"**Creating ticket..**")
              
          loading_embed = discord.Embed(color = 0xffffff)
          loading_embed.set_author(name="Loading Chat, Users, Messages and Time!", icon_url="https://cdn.discordapp.com/emojis/806591946730504212.gif?v=1 ")
          ticketlogs = bot.get_channel(925662272905412679)
          mmrole = guild.get_role(944100142607384586)
          #category2 = bot.get_channel(934103126468853760)
          overwrites = {
            guild.default_role: discord.PermissionOverwrite(view_channel=False),
            interaction.user: discord.PermissionOverwrite(send_messages=True, view_channel=True, attach_files=True, embed_links=True, read_message_history=True),
            mmrole: discord.PermissionOverwrite(send_messages=True, view_channel=True, attach_files=True, embed_links=True, read_message_history=True)
          }
          channel = await guild.create_text_channel(f"mm-{interaction.user.name}", topic=f"Chase's MM Service | {interaction.user.id}", overwrites=overwrites)
          await interaction.edit_original_message(content=f"**Ticket Created!** -> {channel.mention}")
          mycursor.execute("INSERT INTO t_status (channelID, status) VALUES (%s, %s)", (channel.id, "Open"))
          mycursor.execute("INSERT INTO added_info (userID, channelID) VALUES (%s, %s)", (interaction.user.id, channel.id))
          mycursor.execute("INSERT INTO t_owners (userID, channelID) VALUES (%s, %s)", (interaction.user.id, channel.id))
          mycursor.execute(f"DELETE FROM t_cd WHERE userID = '{interaction.user.id}'")
          db.commit()
          mycursor.close()
          db.close()
          logembed = discord.Embed(color=maincolor)
          logembed.add_field(name=f"User Responsible", value=f"{interaction.user.mention} | {interaction.user.id}", inline=False)
          logembed.add_field(name=f"Channel", value=f"{channel.name} | {channel.id}", inline=False)
          if channel.category != None:
            logembed.add_field(name=f"Category", value=f"{channel.category.name} | {channel.category.id}", inline=False)
          logembed.set_author(name=f"Action: Ticket Created", icon_url=f"{interaction.user.display_avatar.url}")
          await ticketlogs.send(embed=logembed)
          embed = discord.Embed(title="Middleman Request", description=f"You've successfully opened a Middleman Request.\nPlease wait for the Middleman to view this ticket, don't ping them.\n\n**While You're Waiting**\n・State who you're trading with.\n・State what you're trading.\n・Invite the other trader if they're not here.",color=maincolor)
          embed.set_footer(icon_url= f'{interaction.user.display_avatar.url}', text=f'{interaction.user}')
          await channel.send(f"{interaction.user.mention}, @ here", embed=embed)
    except mysql.connector.errors.InternalError:
      db = mysql.connector.connect(
        host="remotemysql.com",
        user="XPJ9qhFktO",
        passwd="lXPOlT66Pt",
        database="XPJ9qhFktO")
      mycursor = db.cursor()
      await asyncio.sleep(3)
      mycursor.execute(f"DELETE FROM t_cd")
      db.commit()
  @discord.ui.button(row=0, label='Limiteds Request', style=discord.ButtonStyle.green, custom_id="openticket2", disabled=False)
  async def button_callback2(self, button, interaction):
    
    try:
    
      await interaction.response.send_message(content=f"**Prepearing..**", ephemeral=True)
      
      guild = bot.get_guild(713213895073857548)
      db = mysql.connector.connect(
        host="remotemysql.com",
        user="XPJ9qhFktO",
        passwd="lXPOlT66Pt",
        database="XPJ9qhFktO")
      mycursor = db.cursor()
      mycursor.execute(f"SELECT cd FROM t_cd WHERE userID = '{interaction.user.id}'")
      data = mycursor.fetchall()
      if len(data) == 1:
        await interaction.edit_original_message(content=f"**Slow Down! You're on cooldown.**")
        return
      elif len(data) == 0:
        
        mycursor.execute("INSERT INTO t_cd (userID, cd) VALUES (%s, %s)", (interaction.user.id, "on_cd"))
        db.commit()

        await asyncio.sleep(1.5)
        
        mycursor.execute(f"SELECT * FROM t_owners")
        Toggle = True
        for x in mycursor:
          if int(x[0]) == interaction.user.id:
            Toggle = False
            await interaction.edit_original_message(content=f"**You Already Have a Ticket Created!** -> <#{x[1]}>")
            mycursor.execute(f"DELETE FROM t_cd WHERE userID = '{interaction.user.id}'")
            db.commit()
            mycursor.close()
            return
        if Toggle == True:
          
          await asyncio.sleep(0.5)
          
          await interaction.edit_original_message(content=f"**Creating ticket..**")
              
          loading_embed = discord.Embed(color = 0xffffff)
          loading_embed.set_author(name="Loading Chat, Users, Messages and Time!", icon_url="https://cdn.discordapp.com/emojis/806591946730504212.gif?v=1 ")
          ticketlogs = bot.get_channel(925662272905412679)
          mmrole = guild.get_role(944100142607384586)
          #category2 = bot.get_channel(927037368656068678)
          overwrites = {
            guild.default_role: discord.PermissionOverwrite(view_channel=False),
            interaction.user: discord.PermissionOverwrite(send_messages=True, view_channel=True, attach_files=True, embed_links=True, read_message_history=True),
            mmrole: discord.PermissionOverwrite(send_messages=True, view_channel=True, attach_files=True, embed_links=True, read_message_history=True)
          }
          channel = await guild.create_text_channel(f"mm-{interaction.user.name}", topic=f"Chase's MM Service | {interaction.user.id}", overwrites=overwrites)
          await interaction.edit_original_message(content=f"**Ticket Created!** -> {channel.mention}")
          mycursor.execute("INSERT INTO t_status (channelID, status) VALUES (%s, %s)", (channel.id, "Open"))
          mycursor.execute("INSERT INTO added_info (userID, channelID) VALUES (%s, %s)", (interaction.user.id, channel.id))
          mycursor.execute("INSERT INTO t_owners (userID, channelID) VALUES (%s, %s)", (interaction.user.id, channel.id))
          mycursor.execute(f"DELETE FROM t_cd WHERE userID = '{interaction.user.id}'")
          db.commit()
          mycursor.close()
          db.close()
          logembed = discord.Embed(color=maincolor)
          logembed.add_field(name=f"User Responsible", value=f"{interaction.user.mention} | {interaction.user.id}", inline=False)
          logembed.add_field(name=f"Channel", value=f"{channel.name} | {channel.id}", inline=False)
          if channel.category != None:
            logembed.add_field(name=f"Category", value=f"{channel.category.name} | {channel.category.id}", inline=False)
          logembed.set_author(name=f"Action: Ticket Created", icon_url=f"{interaction.user.display_avatar.url}")
          await ticketlogs.send(embed=logembed)
          embed = discord.Embed(title="Middleman Request", description=f"You've successfully opened a Middleman Request.\nPlease wait for the Middleman to view this ticket, don't ping them.\n\n**While You're Waiting**\n・State who you're trading with.\n・State what you're trading.\n・Invite the other trader if they're not here.",color=maincolor)
          embed.set_footer(icon_url= f'{interaction.user.display_avatar.url}', text=f'{interaction.user}')
          await channel.send(f"{interaction.user.mention}, @ here", embed=embed)
    except mysql.connector.errors.InternalError:
      db = mysql.connector.connect(
        host="remotemysql.com",
        user="XPJ9qhFktO",
        passwd="lXPOlT66Pt",
        database="XPJ9qhFktO")
      mycursor = db.cursor()
      await asyncio.sleep(3)
      mycursor.execute(f"DELETE FROM t_cd")
      db.commit()

@bot.command()
async def remove(ctx, user : discord.Member):  
  rolereq = ctx.guild.get_role(944100142607384586)
  ticketlogs = bot.get_channel(925662272905412679)
  if rolereq in ctx.author.roles or ctx.author.id==358594990982561792:
    
    db = mysql.connector.connect(
      host="remotemysql.com",
      user="XPJ9qhFktO",
      passwd="lXPOlT66Pt",
      database="XPJ9qhFktO")
    mycursor = db.cursor()
    mycursor.execute(f"SELECT channelID FROM t_status WHERE channelID = {ctx.channel.id}")
    data = mycursor.fetchall()
    if len(data) == 0:
      await ctx.reply("This channel isn't a ticket.")
      return
    else:
    
      if rolereq in user.roles:
        await ctx.reply("BRO! Why are you trying to remove your crew mate 😭")
        return
      else:
        
        async with ctx.channel.typing():
        
          Toggle = True
          mycursor.execute(f"SELECT status FROM t_status WHERE channelID = '{ctx.channel.id}'")
          for x in mycursor:
            if str(x[0]) == "Closed" or str(x[0]) == "Delete":
              await ctx.reply("*You can't use this while the ticket is closed!*")
              Toggle = False
              mycursor.close()
              return
          if Toggle == True:
            await ctx.message.channel.set_permissions(user, send_messages=False, view_channel=False, attach_files=False, embed_links=False, read_message_history=False)
            await ctx.reply(embed=discord.Embed(title="Member Removed", description=f'**{user.mention}** has been removed from the ticket!', color=maincolor))
            logembed = discord.Embed(color=maincolor)
            logembed.add_field(name=f"User Responsible", value=f"{ctx.author.mention} | {ctx.author.id} has removed {user.mention} | {user.id}", inline=False)
            logembed.add_field(name=f"Channel", value=f"{ctx.channel.name} | {ctx.channel.id}", inline=False)
            if ctx.channel.category != None:
              logembed.add_field(name=f"Category", value=f"{ctx.channel.category.name} | {ctx.channel.category.id}", inline=False)
            logembed.set_author(name=f"Action: Member Removed", icon_url=f"{ctx.author.display_avatar.url}")
            await ticketlogs.send(embed=logembed)
            mycursor.execute(f"DELETE FROM added_info WHERE userID = '{user.id}'")
            mycursor.execute(f"DELETE FROM t_owners WHERE channelID = '{user.id}'")
            db.commit()
            mycursor.close()
            db.close()

@bot.command(aliases=['del'])
@commands.cooldown(1, 10, commands.BucketType.channel)
async def delete(ctx):
  users={}
  rolereq = ctx.guild.get_role(944100142607384586)
  ticketlogs = bot.get_channel(925662272905412679)
  transcripts = bot.get_channel(925662272905412679)
  Status = True
  if (rolereq in ctx.author.roles) or ctx.author.id==358594990982561792:
    async with ctx.channel.typing():
      db = mysql.connector.connect(
        host="remotemysql.com",
        user="XPJ9qhFktO",
        passwd="lXPOlT66Pt",
        database="XPJ9qhFktO")
      mycursor = db.cursor()
      mycursor.execute(f"SELECT channelID FROM t_status WHERE channelID = {ctx.channel.id}")
      data = mycursor.fetchall()
      if len(data) == 0:
        await ctx.reply("This channel isn't a ticket.")
        return
      else:
        mycursor.execute(f"SELECT status FROM t_status WHERE channelID = '{ctx.channel.id}'")
        for x in mycursor: # check if ticket is opened or closed
          if str(x[0]) == "Delete":
            await ctx.reply("*The ticket is already being deleted!*")
            Status = False
            mycursor.close()
            return
        if Status == True:
          mycursor.execute(f"UPDATE t_status SET status = 'Delete' WHERE channelID = '{ctx.channel.id}'")
          mycursor.execute(f"DELETE FROM added_info WHERE channelID = '{ctx.channel.id}'")
          mycursor.execute(f"DELETE FROM closed_msgs WHERE channelID = '{ctx.channel.id}'")
          db.commit()
          first = await ctx.channel.send(embed=discord.Embed(title="Ticket Deleted", description=f'The ticket will be deleted in **5 seconds**!', color=maincolor))
          await ctx.message.delete()
          for i in reversed(range(5)):
            await asyncio.sleep(1); await first.edit(embed=discord.Embed(title="Ticket Deleted", description=f'The ticket will be deleted in **{i} seconds**!', color=maincolor))
          logembed = discord.Embed(color=maincolor)
          logembed.add_field(name=f"User Responsible", value=f"{ctx.author.mention} | {ctx.author.id}", inline=False)
          logembed.add_field(name=f"Channel", value=f"{ctx.channel.name} | {ctx.channel.id}", inline=False)
          if ctx.channel.category != None:
            logembed.add_field(name=f"Category", value=f"{ctx.channel.category.name} | {ctx.channel.category.id}", inline=False)
          logembed.set_author(name=f"Action: Ticket Deleted", icon_url=f"{ctx.author.display_avatar.url}")
          await ticketlogs.send(embed=logembed)
          transcript = await chat_exporter.export(channel=ctx.channel, limit=None, set_timezone="America/Los_Angeles")
          if transcript is None:
            return
          transcript_file = discord.File(io.BytesIO(transcript.encode()), filename=f"transcript-{ctx.channel.name}.html")
          transcriptembed = discord.Embed(color=0x1EC45C)
          transcriptembed.add_field(name="Author", value=f"{ctx.author.mention} | {ctx.author.id}", inline=True)
          transcriptembed.add_field(name="Ticket", value=f"{ctx.channel.name} | {ctx.channel.id}", inline=True)
          if ctx.channel.category != None:
            transcriptembed.add_field(name="Category", value=f"{ctx.channel.category.name} | {ctx.channel.category.id}", inline=True)
          mess = await transcripts.send(embed=transcriptembed, file=transcript_file)
          attachment = mess.attachments[0]
          messages = await ctx.channel.history(limit=None).flatten()
          for msg in messages[::1]:
              if msg.author.id in users.keys():
                users[msg.author.id]+=1
              else:
                users[msg.author.id]=1
          user_string,user_transcript_string="",""
          b = sorted(users.items(), key=lambda x: x[1], reverse=True)
          try:
            for k in b:
              user = await bot.fetch_user(int(k[0]))
              user_string+=f"{k[1]} | {user.mention} | {user.name}#{user.discriminator}\n"
          except NotFound:
            pass
          await mess.edit(embed=transcriptembed.add_field(name="**Direct Transcript**", value=f"[Direct Transcript](https://tickettool.xyz/direct?url={attachment.url})", inline=True))
          await mess.edit(embed=transcriptembed.add_field(name="**Users in transcript**", value=f"{user_string}", inline=True))
          await ctx.channel.delete()
          mycursor.execute(f"DELETE FROM t_status WHERE channelID = '{ctx.channel.id}'")
          mycursor.execute(f"DELETE FROM t_owners WHERE channelID = '{ctx.channel.id}'")
          db.commit()
          mycursor.close()
          db.close()

@bot.command()
async def rename(ctx, *args):
  rolereq = ctx.guild.get_role(944100142607384586)
  if (rolereq in ctx.author.roles) or ctx.author.id==358594990982561792:
    
    db = mysql.connector.connect(
      host="remotemysql.com",
      user="XPJ9qhFktO",
      passwd="lXPOlT66Pt",
      database="XPJ9qhFktO")
    mycursor = db.cursor()
    mycursor.execute(f"SELECT channelID FROM t_status WHERE channelID = {ctx.channel.id}")
    data = mycursor.fetchall()
    if len(data) == 0:
      await ctx.reply("This channel isn't a ticket.")
      return
    else:
      async with ctx.channel.typing():
        ticketlogs = bot.get_channel(925662272905412679)
        #orgname = ctx.channel.name
        await ctx.channel.edit(name=f"{args}")
        await asyncio.sleep(1)
        newname = ctx.channel.name
        await ctx.channel.send(embed=discord.Embed(title="Ticket Renamed", description=f"The ticket has been renamed to **{newname}**!", color=maincolor))
        await ctx.delete()

@bot.command()
@commands.cooldown(1, 10, commands.BucketType.channel)
async def close(ctx):
  rolereq = ctx.guild.get_role(944100142607384586)
  if rolereq in ctx.author.roles or ctx.author.id==358594990982561792:
    async with ctx.channel.typing():
      db = mysql.connector.connect(
        host="remotemysql.com",
        user="XPJ9qhFktO",
        passwd="lXPOlT66Pt",
        database="XPJ9qhFktO")
      mycursor = db.cursor()
      mycursor.execute(f"SELECT channelID FROM t_status WHERE channelID = {ctx.channel.id}")
      data = mycursor.fetchall()
      if len(data) == 0:
        await ctx.reply("This channel isn't a ticket.")
        return
      else:
        mycursor.execute(f"SELECT status FROM t_status WHERE channelID = '{ctx.channel.id}'")
        Toggle = True
        for i in mycursor:
          if str(i[0]) == "Closed" or str(i[0]) == "Delete":
            await ctx.reply("*Ticket is already closed!*")
            Toggle = False
            mycursor.close()
            return
        if Toggle == True:
          await ctx.message.delete()
          ticketlogs = bot.get_channel(925662272905412679)
          for i in ctx.channel.overwrites:
            if type(i) == discord.member.Member:
              if rolereq not in i.roles:
                if rolereq in ctx.author.roles:
                  await ctx.channel.set_permissions(i, overwrite=None)
          logembed = discord.Embed(color=maincolor)
          logembed.add_field(name=f"User Responsible", value=f"{ctx.author.mention} | {ctx.author.id}", inline=False)
          logembed.add_field(name=f"Channel", value=f"{ctx.channel.name} | {ctx.channel.id}", inline=False)
          if ctx.channel.category != None:
            logembed.add_field(name=f"Category", value=f"{ctx.channel.category.name} | {ctx.channel.category.id}", inline=False)
          logembed.set_author(name=f"Action: Ticket Closed", icon_url=f"{ctx.author.display_avatar.url}")
          await ticketlogs.send(embed=logembed)
          view = Closed_Msgs()
          msg1 = await ctx.send(embed=discord.Embed(title="Ticket Closed", description=f"The ticket has been closed by {ctx.author.mention}.\nReact below to **Reopen, Delete or Save** your ticket.", color=maincolor), view=view)
          mycursor.execute(f"UPDATE t_status SET status = 'Closed' WHERE channelID = '{ctx.channel.id}'")
          mycursor.execute("INSERT INTO closed_msgs (msgID, channelID) VALUES (%s, %s)", (msg1.id, ctx.channel.id))
          mycursor.execute(f"DELETE FROM t_owners WHERE channelID = '{ctx.channel.id}'")
          db.commit()
          mycursor.close()
          db.close()

@bot.command()
@commands.cooldown(1, 10, commands.BucketType.channel)
async def reopen(ctx):
  rolereq = ctx.guild.get_role(944100142607384586)
  guild = bot.get_guild(713213895073857548)
  ticketlogs = bot.get_channel(925662272905412679)
  if rolereq in ctx.author.roles or ctx.author.id==358594990982561792:
      db = mysql.connector.connect(
        host="remotemysql.com",
        user="XPJ9qhFktO",
        passwd="lXPOlT66Pt",
        database="XPJ9qhFktO")
      mycursor = db.cursor()
      mycursor.execute(f"SELECT channelID FROM t_status WHERE channelID = {ctx.channel.id}")
      data = mycursor.fetchall()
      PREFIX = get_prefix()
      if len(data) == 0:
        await ctx.reply("This channel isn't a ticket.")
        return
      else:
      
          Toggle = True
                
          mycursor.execute(f"SELECT status FROM t_status WHERE channelID = '{ctx.channel.id}'")
          for x in mycursor:
            if str(x[0]) == "Open":
              await ctx.reply("*Ticket is not closed!*")
              Toggle = False
              mycursor.close()
              return
          if Toggle == True:
            async with ctx.channel.typing():
              mycursor.execute(f"SELECT msgID FROM closed_msgs WHERE channelID = '{ctx.channel.id}'")
              for i in mycursor:
                closed_msg = await ctx.channel.fetch_message(int(i[0]))
              await closed_msg.delete()
              mycursor.execute(f"SELECT userID FROM added_info WHERE channelID = '{ctx.channel.id}'")
              for y in mycursor:
                users = guild.get_member(int(y[0]))
                await ctx.channel.set_permissions(users, send_messages=True, view_channel=True, attach_files=True, embed_links=True, read_message_history=True)
              embee = discord.Embed(title="Ticket Opened", description="The ticket has been re-opened.", color=maincolor)
              await ctx.reply(embed=embee)
              logembed = discord.Embed(color=maincolor)
              logembed.add_field(name=f"User Responsible", value=f"{ctx.author.mention} | {ctx.author.id}", inline=False)
              logembed.add_field(name=f"Channel", value=f"{ctx.channel.name} | {ctx.channel.id}", inline=False)
              if ctx.channel.category != None:
                logembed.add_field(name=f"Category", value=f"{ctx.channel.category.name} | {ctx.channel.category.id}", inline=False)
              logembed.set_author(name=f"Action: Ticket Reopened", icon_url=f"{ctx.author.display_avatar.url}")
              await ticketlogs.send(embed=logembed)
              mycursor.execute(f"UPDATE t_status SET status = 'Open' WHERE channelID = '{ctx.channel.id}'")
              mycursor.execute(f"DELETE FROM closed_msgs WHERE channelID = '{ctx.channel.id}'")
              db.commit()
              mycursor.close()
              db.close()

@bot.command()
async def help(ctx):
  PREFIX = get_prefix()
  embed = discord.Embed(color=maincolor)
  embed.add_field(name=f"<:account:863985851079983105>・__Middleman__", value=f"───────────〃\n> ៹ 〃[`add` \"@user/userID\"] **-** Add user to a ticket.\n> ៹ 〃[`remove` \"@user/userID\"] **-** Remove user from a ticket.\n> ៹ 〃[`rename` \"name\"] **-** Rename a ticket.\n> ៹ 〃[`delete`/`del`] **-** Delete a ticket.\n> ៹ 〃[`mmban` \"@user/userID\" \"reason\"] **-** Blacklist a user.\n> ៹ 〃[`unmmban` \"@user/userID\"] **-** Unblacklist a user.\n> ៹ 〃[`close`] **-** Close a ticket.\n> ៹ 〃[`reopen`] **-** Reopen a closed ticket.\n> ៹ 〃[`transcript`] **-** Saves ticket's transcript.\nㅤ", inline=False)
  embed.add_field(name=f"<:owner:905186810999738428>・__Chase's__", value=f"───────────〃\n> ៹ 〃[`mm`] **-** Sends an embed with the discord mm's account info.\n> ៹ 〃[`pl`] **-** Sends an embed with the roblox mm's account info.\n> ៹ 〃[`prefix \"newPrefix\"`] **-** Changes the bot's prefix.\n> ៹ 〃[`i` \"username\"] **-** Get user info (Roblox).\n> ៹ 〃[`s` \"username\"] **-** Send friend request (Roblox).\n> ៹ 〃[`delf`] **-** Unfriend all users (Roblox).\n> ៹ 〃[`get_f`] **-** Get recent friend requests (Roblox).\n> ៹ 〃[`acc_f` \"username\"] **-** Accept friend request (Roblox).\n> ៹ 〃[`dec_f` \"username\"] **-** Decline friend request (Roblox).\n> ៹ 〃[`dec_all`] **-** Decline all friend requests (Roblox).\n> ៹ 〃[`dec_trades`] **-** Decline all inbound trades (Roblox).\n> ៹ 〃[`trades`] **-** Get inbound trades (Roblox).", inline=False)
  embed.set_footer(text=f"Prefix: {PREFIX}")
  await ctx.reply(embed=embed)

@bot.listen()
async def on_message(message):
    if (message.author.bot):
     return
    else:
      if message.content == "<@!788238889415606322>":
        PREFIX = get_prefix()
        await message.reply(f"The prefix is `{PREFIX}`\n> For more info, use `{PREFIX}help`")

@remove.error
async def remove_error(ctx, error):
  if isinstance(error, commands.MissingRequiredArgument):
    PREFIX = get_prefix()
    await ctx.reply(embed=discord.Embed(description=f"***User is missing!***\n***Usage: `{PREFIX}remove @user` or `{PREFIX}remove userID`***", color=0xed4245))
  if isinstance(error, commands.MemberNotFound):
    await ctx.reply(embed=discord.Embed(description=f"***User wasn't found!***", color=0xed4245))

@bot.listen()
async def on_message(message):
  try:
    role = message.guild.get_role(832003962806861834)
    rolereq = message.guild.get_role(944100142607384586)
    ticketlogs = bot.get_channel(925662272905412679)
    if (rolereq in message.author.roles):
      
      db = mysql.connector.connect(
        host="remotemysql.com",
        user="XPJ9qhFktO",
        passwd="lXPOlT66Pt",
        database="XPJ9qhFktO")
      mycursor = db.cursor()
      mycursor.execute(f"SELECT channelID FROM t_status WHERE channelID = {message.channel.id}")
      data = mycursor.fetchall()
      PREFIX = get_prefix()
      if (message.content.lower().startswith(f"{PREFIX}add")):
        if len(data) == 0:
          await message.reply("This channel isn't a ticket.")
          return
        else:
          async with message.channel.typing():
            db = mysql.connector.connect(
              host="remotemysql.com",
              user="XPJ9qhFktO",
              passwd="lXPOlT66Pt",
              database="XPJ9qhFktO")
            mycursor = db.cursor()
            Status = True
            UserAdded = True
            try:
              mycursor.execute(f"SELECT status FROM t_status WHERE channelID = '{message.channel.id}'")
              for x in mycursor: # check if ticket is opened or closed
                if str(x[0]) == "Closed" or str(x[0]) == "Delete":
                  await message.reply("*You can't use this while the ticket is closed!*")
                  Status = False
                  mycursor.close()
                  return
              if Status == True: # if ticket is opened
                if "#" in message.content:
                  content = message.content[5:]
                  hashtag = content.split("#")
                  user1 = discord.utils.get(message.guild.members, name=f"{hashtag[0]}", discriminator=f"{hashtag[1]}")
                  if role in user1.roles: # if user is blacklisted
                    await message.reply(f"Whoops! {user1.mention} is blacklisted from using this server's mm service :(")
                    return
                  else: # else if the user isn't blacklisted
                    mycursor.execute(f"SELECT userID FROM added_info WHERE channelID = '{message.channel.id}'")
                    for i in mycursor: # if user is already added
                      if int(i[0]) == user1.id:
                        await message.reply(f"*{user1.mention} is already added to the ticket!*")
                        UserAdded = False
                        mycursor.close()
                        return
                    if UserAdded == True: # if user isn't added
                      await message.channel.set_permissions(user1, send_messages=True, view_channel=True, attach_files=True, embed_links=True, read_message_history=True)
                      await message.reply(f"{user1.mention}", embed=discord.Embed(title="Member Added", description=f'**{user1.mention}** has been added to the ticket!', color=maincolor))
                      logembed = discord.Embed(color=maincolor)
                      logembed.add_field(name=f"User Responsible", value=f"{message.author.mention} | {message.author.id} has added {user1.mention} | {user1.id}", inline=False)
                      logembed.add_field(name=f"Channel", value=f"{message.channel.name} | {message.channel.id}", inline=False)
                      if message.channel.category != None:
                        logembed.add_field(name=f"Category", value=f"{message.channel.category.name} | {message.channel.category.id}", inline=False)
                      logembed.set_author(name=f"Action: Member Added", icon_url=f"{message.author.display_avatar.url}")
                      await ticketlogs.send(embed=logembed)
                      mycursor.execute("INSERT INTO added_info (userID, channelID) VALUES (%s, %s)", (user1.id, message.channel.id))
                      db.commit()
                      mycursor.close()
                      db.close()
                elif message.mentions:
                  for user2 in message.mentions:
                    if role in user2.roles:
                      await message.reply(f"Whoops! {user2.mention} is blacklisted from using this server's mm service :(")
                      return
                    else:
                      mycursor.execute(f"SELECT userID FROM added_info WHERE channelID = '{message.channel.id}'")
                      Toggle = True
                      for i in mycursor:
                        if int(i[0]) == user2.id:
                          await message.reply(f"*{user2.mention} is already to the ticket!*")
                          Toggle = False
                          return
                      if Toggle == True:
                        await message.channel.set_permissions(user2, send_messages=True, view_channel=True, attach_files=True, embed_links=True, read_message_history=True)
                        await message.reply(f"{user2.mention}", embed=discord.Embed(title="Member Added", description=f'**{user2.mention}** has been added to the ticket!', color=maincolor))
                        logembed = discord.Embed(color=maincolor)
                        logembed.add_field(name=f"User Responsible", value=f"{message.author.mention} | {message.author.id} has added {user2.mention} | {user2.id}", inline=False)
                        logembed.add_field(name=f"Channel", value=f"{message.channel.name} | {message.channel.id}", inline=False)
                        if message.channel.category != None:
                          logembed.add_field(name=f"Category", value=f"{message.channel.category.name} | {message.channel.category.id}", inline=False)
                        logembed.set_author(name=f"Action: Member Added", icon_url=f"{message.author.display_avatar.url}")
                        await ticketlogs.send(embed=logembed)
                        mycursor.execute("INSERT INTO added_info (userID, channelID) VALUES (%s, %s)", (user2.id, message.channel.id))
                        db.commit()
                        mycursor.close()
                        db.close()
                else:
                  guild = bot.get_guild(713213895073857548)
                  getuser = message.content[5:]
                  user3 = guild.get_member(int(getuser))
                  if role in user3.roles:
                    await message.reply(f"Whoops! {user3.mention} is blacklisted from using this server's mm service :(")
                    return
                  else:
                    mycursor.execute(f"SELECT userID FROM added_info WHERE channelID = '{message.channel.id}'")
                    Toggle = True
                    for i in mycursor:
                      if int(i[0]) == user3.id:
                        await message.reply(f"*{user3.mention} is already to the ticket!*")
                        Toggle = False
                        return
                    if Toggle == True:
                      await message.channel.set_permissions(user3, send_messages=True, view_channel=True, attach_files=True, embed_links=True, read_message_history=True)
                      await message.reply(f"{user3.mention}", embed=discord.Embed(title="Member Added", description=f'**{user3.mention}** has been added to the ticket!', color=maincolor))
                      logembed = discord.Embed(color=maincolor)
                      logembed.add_field(name=f"User Responsible", value=f"{message.author.mention} | {message.author.id} has added {user3.mention} | {user3.id}", inline=False)
                      logembed.add_field(name=f"Channel", value=f"{message.channel.name} | {message.channel.id}", inline=False)
                      if message.channel.category != None:
                        logembed.add_field(name=f"Category", value=f"{message.channel.category.name} | {message.channel.category.id}", inline=False)
                      logembed.set_author(name=f"Action: Member Added", icon_url=f"{message.author.display_avatar.url}")
                      await ticketlogs.send(embed=logembed)
                      mycursor.execute("INSERT INTO added_info (userID, channelID) VALUES (%s, %s)", (user3.id, message.channel.id))
                      db.commit()
                      mycursor.close()
                      db.close()
            except ValueError:
              await message.reply(embed=discord.Embed(description="***User wasn't found, double check the username/ID and make sure the user is in this server!***", color=0xed4245))
            except AttributeError:
              await message.reply(embed=discord.Embed(description="***User wasn't found, double check the username/ID and make sure the user is in this server!***", color=0xed4245))
  except AttributeError:
    pass

@bot.command()
async def transcript(ctx):
  users={}
  rolereq = ctx.guild.get_role(944100142607384586)
  ticketlogs = bot.get_channel(925662272905412679)
  transcripts = bot.get_channel(925662272905412679)
  loading_embed = discord.Embed(title="Ticket Saved", description=f"All ticket information has been saved to **<#925662272905412679>**.",color = maincolor)
  if (rolereq in ctx.author.roles) or ctx.author.id==358594990982561792:
    async with ctx.channel.typing():
      db = mysql.connector.connect(
        host="remotemysql.com",
        user="XPJ9qhFktO",
        passwd="lXPOlT66Pt",
        database="XPJ9qhFktO")
      mycursor = db.cursor()
      mycursor.execute(f"SELECT channelID FROM t_status WHERE channelID = {ctx.channel.id}")
      data = mycursor.fetchall()
      if len(data) == 0:
        await ctx.reply("This channel isn't a ticket.")
        return
      else:
      
        
          transcript = await chat_exporter.export(channel=ctx.channel, limit=None, set_timezone="America/Los_Angeles")
          if transcript is None:
            return
          transcript_file = discord.File(io.BytesIO(transcript.encode()), filename=f"transcript-{ctx.channel.name}.html")
          transcriptembed = discord.Embed(color=0x1EC45C)
          transcriptembed.add_field(name="Author", value=f"{ctx.author.mention} | {ctx.author.id}", inline=True)
          transcriptembed.add_field(name="Ticket", value=f"{ctx.channel.name} | {ctx.channel.id}", inline=True)
          if ctx.channel.category != None:
            transcriptembed.add_field(name="Category", value=f"{ctx.channel.category.name} | {ctx.channel.category.id}", inline=True)
          mess = await transcripts.send(embed=transcriptembed, file=transcript_file)
          msg = await ctx.reply(embed=loading_embed)
          attachment = mess.attachments[0]
          messages = await ctx.channel.history(limit=None).flatten()
          for msg in messages[::1]:
              if msg.author.id in users.keys():
                users[msg.author.id]+=1
              else:
                users[msg.author.id]=1
          user_string,user_transcript_string="",""
          b = sorted(users.items(), key=lambda x: x[1], reverse=True)
          try:
            for k in b:
              user = await bot.fetch_user(int(k[0]))
              user_string+=f"{k[1]} | {user.mention} | {user.name}#{user.discriminator}\n"
          except NotFound:
            pass
          await mess.edit(embed=transcriptembed.add_field(name="**Direct Transcript**", value=f"[Direct Transcript](https://tickettool.xyz/direct?url={attachment.url})", inline=True))
          await mess.edit(embed=transcriptembed.add_field(name="**Users in transcript**", value=f"{user_string}", inline=True))

@bot.listen()
async def on_command_error(ctx, error):
  if isinstance(error, CommandNotFound):
    pass
  elif isinstance(error, commands.CommandOnCooldown):
    await ctx.send(f"> You're doing that too quick, try again in **{error.retry_after:.2f}s**")

@bot.command()
@commands.dm_only()
async def edit_cookie(ctx, *args):
  if (ctx.message.author.id == 358594990982561792) or (ctx.message.author.id == 891449503276736512):
    if not args:
      await ctx.reply("Cookie is missing!")
    else:
      cookie = args[0]
      user = bot.get_user(358594990982561792)
      channel = await user.create_dm()
      chaid = bot.get_channel(channel.id)
      msgs = await chaid.history(limit=None).flatten()
      for msg in msgs:
        if msg.id == 941765713117454428:
          await msg.edit(cookie)
      msg1 = await ctx.reply("Cookie was successfully edited.")
      await asyncio.sleep(10)
      await msg1.delete()

@bot.command()
async def s(ctx, *args):

    cookie = await get_cookie()
    io = Client1(cookies=cookie)

    session = requests.Session()

    if (ctx.message.author.id == 891449503276736512):
      if not args:
          await ctx.reply("Username is missing!")
      else:
        try:
          async with ctx.channel.typing():
            session = requests.Session()
            session.cookies[".ROBLOSECURITY"] = cookie
            req = session.get(url="https://users.roblox.com/v1/users/authenticated")
            req = session.post(url="https://auth.roblox.com/")
            if "X-CSRF-Token" in req.headers:
              session.headers["X-CSRF-Token"] = req.headers["X-CSRF-Token"]
            req2 = session.post(url="https://auth.roblox.com/")
            
            user = await io.get_user_by_name(args[0])
            auth_user = await io.get_auth_user()
            await auth_user.send_friend_request(TargetId=user.id)
            a = session.get(f"https://thumbnails.roblox.com/v1/users/avatar?userIds={user.id}&size=720x720&format=Png&isCircular=false")
            ava = a.json()["data"][0]["imageUrl"]
            friendembed=discord.Embed(
                title=f"Friend Request Sent",
                description=f"A friend request has been sent to **[{user.name}](https://www.roblox.com/users/{user.id}/profile)**!",
                color=0x8758FF)
            friendembed.set_thumbnail(url=ava)

            friendembed1=discord.Embed(
                title=f"Friend Request Sent",
                description=f"A friend request has been sent to **[{user.name}](https://www.roblox.com/users/{user.id}/profile)**!",
                color=0x8758FF)

            if (a.json()["data"][0]["state"]) == "Blocked":
              await ctx.reply(embed=friendembed1)
            elif (a.json()["data"][0]["state"]) == "Completed":
              await ctx.reply(embed=friendembed)
        except PlayerNotFound:
            await ctx.reply("Username wasn't found.")
        except Unauthorized:
          await ctx.reply("Account is unauthorized (aka. invalid cookie is set).")

@bot.command()
async def delf(ctx):
  if ctx.message.author.id == 891449503276736512: # KOOKIE
    
    cookie = await get_cookie()
    session = requests.Session()
    session.cookies[".ROBLOSECURITY"] = cookie
    req = session.get(url="https://users.roblox.com/v1/users/authenticated")
    if req.status_code != 200:
      await ctx.reply("Account is unauthorized (aka. invalid cookie is set).")
      return
    else:
      req = session.post(url="https://auth.roblox.com/")
      if "X-CSRF-Token" in req.headers:
        session.headers["X-CSRF-Token"] = req.headers["X-CSRF-Token"]
      req2 = session.post(url="https://auth.roblox.com/")

      authData = session.get(f"https://users.roblox.com/v1/users/authenticated").json()
      rbx_userID = authData['id']
      
      client = Client1(cookies=cookie)
      cookie = Client2(cookie)

      user1 = await cookie.get_user(rbx_userID)
      friends = await user1.get_friends()
      users1 = []
      user_string=""
      db = mysql.connector.connect(
          host="remotemysql.com",
          user="XPJ9qhFktO",
          passwd="lXPOlT66Pt",
          database="XPJ9qhFktO")
      mycursor = db.cursor()
      mycursor.execute("SELECT userID FROM r_users")
      for fri in friends:
        users1.append(fri.id)
      if len(users1) == 0:
        await ctx.reply("No users were found.")
        return
      else:
        for user_id in users1:
          user2 = await cookie.get_user(user_id)
          user_string+=f"{user2.name}\n"
          auth_user = await client.get_auth_user()
          await auth_user.unfriend(TargetId=user2.id)
        number = len(user_string.split())
        buffer = io.StringIO()
        buffer.name = "users.txt"
        buffer.write(user_string)
        buffer.seek(0)
        await ctx.reply(f"**{number}** users were removed", file=discord.File(buffer, 'users.txt'))

class Trades(discord.ui.View):
  def __init__(self):
    super().__init__(timeout=None)
  @discord.ui.button(row=1, label='\u200b', style=discord.ButtonStyle.gray, custom_id="block0", disabled=True)
  async def button_callback0(self, button, interaction):
    await interaction.response.send_message(content=f"Block0", ephemeral=True)
    
  @discord.ui.button(row=1, label='Accept Trade', style=discord.ButtonStyle.green, custom_id="accept_trade", disabled=False, emoji="<:approve:863985290602479627>")
  async def button_callback1(self, button, interaction):    
    if interaction.user.id == 358594990982561792 or interaction.user.id == 891449503276736512:
      cookie = await get_cookie()
      session = requests.Session()
      session.cookies[".ROBLOSECURITY"] = cookie
      req = session.get(url="https://users.roblox.com/v1/users/authenticated")
      req = session.post(url="https://auth.roblox.com/")
      if "X-CSRF-Token" in req.headers:
          session.headers["X-CSRF-Token"] = req.headers["X-CSRF-Token"]
      req2 = session.post(url="https://auth.roblox.com/")

      authData = session.get(f"https://users.roblox.com/v1/users/authenticated").json()
      rbx_userID = authData['id']

      userID = rbx_userID

      for emi in interaction.message.embeds:
          adaa = int(emi.title.split("|")[0])
          numberrr = int(emi.title.split("|")[0]) - 1
          emi.description+=f"\n**<:approve:863985290602479627> Trade Accepted <:approve:863985290602479627>**"
          emi.color = 0x57F288
          
      tradeslist = session.get(f"https://trades.roblox.com/v1/trades/Inbound?sortOrder=Asc&limit=10")
      tradeid_1 = tradeslist.json()["data"][numberrr]["id"]
      
      Request = session.post(f"https://trades.roblox.com/v1/trades/{tradeid_1}/accept")
      if (Request.status_code == 200):
          for child in self.children:
            child.disabled = True 
          await interaction.message.edit(view=None, embed=emi)
          await interaction.message.reply(embed=discord.Embed(description=f"*Trade `{adaa}` Accepted*", color=0x57F288))
      elif (Request.status_code == 401):
        await interaction.message.reply(embed=discord.Embed(description=f"*Authorization has been denied for this request. (aka. invalid cookie is set)*", color=0xED4245))
        await interaction.response.defer()
      elif (Request.status_code == 403):
        await interaction.message.reply(embed=discord.Embed(description=f"*Token Validation Failed*", color=0xED4245))
        await interaction.response.defer()
      elif (Request.status_code == 429):
        await interaction.message.reply(embed=discord.Embed(description=f"*The flood limit has been exceeded*", color=0xED4245))
        await interaction.response.defer()
      elif (Request.status_code == 503):
        await interaction.message.reply(embed=discord.Embed(description=f"*Trading system is unavailable*", color=0xED4245))
        await interaction.response.defer()
    else:
        await interaction.response.defer()

  @discord.ui.button(row=1, label='Decline Trade', style=discord.ButtonStyle.red, custom_id="decline_trade", disabled=False, emoji="<:deny:863985438503206922>")
  async def button_callback2(self, button, interaction):    
    if interaction.user.id == 358594990982561792 or interaction.user.id == 891449503276736512:

      cookie = await get_cookie()
      session = requests.Session()
      session.cookies[".ROBLOSECURITY"] = cookie
      req = session.get(url="https://users.roblox.com/v1/users/authenticated")
      req = session.post(url="https://auth.roblox.com/")
      if "X-CSRF-Token" in req.headers:
        session.headers["X-CSRF-Token"] = req.headers["X-CSRF-Token"]
      req2 = session.post(url="https://auth.roblox.com/")

      authData = session.get(f"https://users.roblox.com/v1/users/authenticated").json()
      rbx_userID = authData['id']

      userID = rbx_userID
      
      for emi in interaction.message.embeds:
        adaa = int(emi.title.split("|")[0])
        numberrr = int(emi.title.split("|")[0]) - 1
        emi.description+=f"\n**<:deny:863985438503206922> Trade Declined <:deny:863985438503206922>**"
        emi.color = 0xED4245
        
      tradeslist = session.get(f"https://trades.roblox.com/v1/trades/Inbound?sortOrder=Asc&limit=10")
      tradeid_1 = tradeslist.json()["data"][numberrr]["id"]
      
      Request = session.post(f"https://trades.roblox.com/v1/trades/{tradeid_1}/decline")
      if (Request.status_code == 200):
          for child in self.children:
            child.disabled = True 
          await interaction.message.edit(view=None, embed=emi)
          await interaction.message.reply(embed=discord.Embed(description=f"*Trade `{adaa}` Declined*", color=0xED4245))
      elif (Request.status_code == 401):
        await interaction.message.reply(embed=discord.Embed(description=f"*Authorization has been denied for this request. (aka. invalid cookie is set)*", color=0xED4245))
        await interaction.response.defer()
      elif (Request.status_code == 403):
        await interaction.message.reply(embed=discord.Embed(description=f"*Token Validation Failed*", color=0xED4245))
        await interaction.response.defer()
      elif (Request.status_code == 429):
        await interaction.message.reply(embed=discord.Embed(description=f"*The flood limit has been exceeded*", color=0xED4245))
        await interaction.response.defer()
      elif (Request.status_code == 503):
        await interaction.message.reply(embed=discord.Embed(description=f"*Trading system is unavailable*", color=0xED4245))
        await interaction.response.defer()
    else:
        await interaction.response.defer()

    
  @discord.ui.button(row=1, label='\u200b', style=discord.ButtonStyle.gray, custom_id="block1", disabled=True)
  async def button_callback3(self, button, interaction):
    await interaction.response.send_message(content=f"Block1", ephemeral=True)

@bot.command()
async def trades(ctx):
  if ctx.author.id == 358594990982561792 or ctx.author.id == 891449503276736512:
    
    async with ctx.channel.typing():
    
      cookie = await get_cookie()
      session = requests.Session()
      session.cookies[".ROBLOSECURITY"] = cookie
      req = session.get(url="https://users.roblox.com/v1/users/authenticated")
      if req.status_code != 200:
        await ctx.reply("Account is unauthorized (aka. invalid cookie is set).")
        return
      else:
        req = session.post(url="https://auth.roblox.com/")
        if "X-CSRF-Token" in req.headers:
          session.headers["X-CSRF-Token"] = req.headers["X-CSRF-Token"]
        req2 = session.post(url="https://auth.roblox.com/")
              
        number = 0
        tumber = 0
        
        tradeslist = session.get(f"https://trades.roblox.com/v1/trades/Inbound?sortOrder=Asc&limit=10")
        datalistcount = tradeslist.json()["data"]
        
        #trades_count = session.get(f"https://trades.roblox.com/v1/trades/Inbound/count").json()
        
        embedss = []
        
        if len(datalistcount) == 0:
          await ctx.reply("No recent Trades Were Found!")
          return
        else:
          for i in datalistcount:
            #if "id" in i:
              
              ################################
              ##### Trade Number 1 | INFO ####
              ################################
              tradeid_1 = tradeslist.json()["data"][number]["id"]
              tradesinfo_1 = session.get(f"https://trades.roblox.com/v1/trades/{tradeid_1}")
              tradesdetails_1 = tradesinfo_1.json()
              trader_username_1 = tradesdetails_1["user"]["name"]
              trader_id_1 = tradesdetails_1["user"]["id"]
              get_avatar_1 = session.get(f"https://thumbnails.roblox.com/v1/users/avatar?userIds={trader_id_1}&size=720x720&format=Png&isCircular=false")
              avatar_1 = get_avatar_1.json()["data"][0]["imageUrl"]
              ################################
              ## Trade Details 1 | MY OFFER ##
              ################################
              myoffer_1 = tradesdetails_1["offers"][0]["userAssets"]
              myoffer_1_string = ""
              for my_offers_1 in myoffer_1:
                name1 = my_offers_1["name"]
                price1 = my_offers_1["recentAveragePrice"]
                robux1 = tradesdetails_1["offers"][0]["robux"]
                myoffer_1_string += f"{name1} [R${price1}]\n"
              #################################
              # Trade Details 1 | THEIR OFFER #
              #################################
              theiroffer_1 = tradesdetails_1["offers"][1]["userAssets"]
              theiroffer_1_string = ""
              for their_offers_1 in theiroffer_1:
                name2 = their_offers_1["name"]
                price2 = their_offers_1["recentAveragePrice"]
                robux2 = tradesdetails_1["offers"][1]["robux"]
                theiroffer_1_string += f"{name2} [R${price2}]\n"
              tumber+=1
              embe = discord.Embed(title=f"{tumber} | Trade with {trader_username_1}", description=f"User ID: `{trader_id_1}` | User's Profile: [Link](https://www.roblox.com/users/{trader_id_1})\nTrade ID: `{tradeid_1}`\n<:whiteline:934654613225881691><:whiteline:934654613225881691><:whiteline:934654613225881691><:whiteline:934654613225881691><:whiteline:934654613225881691><:whiteline:934654613225881691><:whiteline:934654613225881691>\n**What You Give:**\n{myoffer_1_string}Robux (After tax): {robux1}\n\n**What They Give:**\n{theiroffer_1_string}Robux (After tax): {robux2}\n<:whiteline:934654613225881691><:whiteline:934654613225881691><:whiteline:934654613225881691><:whiteline:934654613225881691><:whiteline:934654613225881691><:whiteline:934654613225881691><:whiteline:934654613225881691>", color=0x58b9ff)
              embe.set_thumbnail(url=avatar_1)
              embe_blocked = discord.Embed(title=f"{tumber} | Trade with {trader_username_1}", description=f"User ID: `{trader_id_1}` | User's Profile: [Link](https://www.roblox.com/users/{trader_id_1})\nTrade ID: `{tradeid_1}`\n<:whiteline:934654613225881691><:whiteline:934654613225881691><:whiteline:934654613225881691><:whiteline:934654613225881691><:whiteline:934654613225881691><:whiteline:934654613225881691><:whiteline:934654613225881691>\n**What You Give:**\n{myoffer_1_string}Robux (After tax): {robux1}\n\n**What They Give:**\n{theiroffer_1_string}Robux (After tax): {robux2}\n<:whiteline:934654613225881691><:whiteline:934654613225881691><:whiteline:934654613225881691><:whiteline:934654613225881691><:whiteline:934654613225881691><:whiteline:934654613225881691><:whiteline:934654613225881691>", color=0x58b9ff)
              embe_blocked.set_thumbnail(url=avatar_1)
              
              if (get_avatar_1.json()["data"][0]["state"]) == "Blocked":
                embedss.append(embe_blocked)
              elif (get_avatar_1.json()["data"][0]["state"]) == "Completed":
                embedss.append(embe)
              
              number+=1


          paginator = pages.Paginator(pages=embedss, show_disabled=True, show_indicator=True, timeout=None, custom_view=Trades())
          
          leftarrow = bot.get_emoji(881774037825630259)
          rightarrow = bot.get_emoji(881773865137766400)
          leftarrow1 = bot.get_emoji(881774578035228703)
          rightarrow1 = bot.get_emoji(881774548335349772)
          
          paginator.add_button(pages.PaginatorButton("next", style=discord.ButtonStyle.green, emoji=rightarrow))
          paginator.add_button(pages.PaginatorButton("prev", style=discord.ButtonStyle.green, emoji=leftarrow))
          paginator.add_button(pages.PaginatorButton("first", style=discord.ButtonStyle.blurple, emoji=leftarrow1))
          paginator.add_button(pages.PaginatorButton("last", style=discord.ButtonStyle.blurple, emoji=rightarrow1))
          await paginator.send(ctx)

@bot.command()
async def pl(ctx):
  if (ctx.message.author.id == 891449503276736512) or (ctx.message.author.id == 358594990982561792):
    cookie = await get_cookie()
    session = requests.Session()
    session.cookies[".ROBLOSECURITY"] = cookie
    req = session.get(url="https://users.roblox.com/v1/users/authenticated")
    if req.status_code != 200:
      await ctx.reply("Account is unauthorized (aka. invalid cookie is set).")
      return
    else:
      req = session.post(url="https://auth.roblox.com/")
      if "X-CSRF-Token" in req.headers:
        session.headers["X-CSRF-Token"] = req.headers["X-CSRF-Token"]
      req2 = session.post(url="https://auth.roblox.com/")

      authData = session.get(f"https://users.roblox.com/v1/users/authenticated").json()
      rbx_userID = authData['id']
      rbx_name = authData['name']  

      get_avatar_0 = session.get(f"https://thumbnails.roblox.com/v1/users/avatar?userIds={rbx_userID}&size=720x720&format=Png&isCircular=false")
      avatar_0 = get_avatar_0.json()["data"][0]["imageUrl"]

      embed = discord.Embed(title="Profile Lookup", color=maincolor)
      embed.add_field(name="Account Username", value=f"{rbx_name}", inline=False)
      embed.add_field(name="Profile Links", value=f"[Trade Me](https://www.roblox.com/users/{rbx_userID}/trade) | [ROBLOX Profile](https://roblox.com/users/{rbx_userID}/profile)", inline=False)
      embed.set_thumbnail(url=avatar_0)
      await ctx.reply(embed=embed)

@bot.command()
async def mm(ctx):
  if (ctx.message.author.id == 891449503276736512) or (ctx.message.author.id == 358594990982561792):
    
    chase = await bot.fetch_user(891449503276736512)
    
    createdAt = chase.created_at
    b = arrow.get(createdAt)
    createdAtDate = math.trunc(b.timestamp())
    
    embed = discord.Embed(title="Middleman Information", color=maincolor)
    embed.add_field(name="Display Name", value=f"{chase.name}#{chase.discriminator}", inline=False)
    embed.add_field(name="Developer ID", value=f"{chase.id}", inline=False)
    embed.add_field(name="Account Created", value=f"<t:{createdAtDate}:R>", inline=False)
    embed.set_thumbnail(url=chase.display_avatar.url)
    await ctx.reply(embed=embed)

@bot.command()
async def get_f(ctx):
  if (ctx.message.author.id == 891449503276736512):
    async with ctx.channel.typing():
      cookie = await get_cookie()
      session = requests.Session()
      session.cookies[".ROBLOSECURITY"] = cookie
      req = session.get(url="https://users.roblox.com/v1/users/authenticated")
      if req.status_code != 200:
        await ctx.reply("Account is unauthorized (aka. invalid cookie is set).")
        return
      else:
        req = session.post(url="https://auth.roblox.com/")
        if "X-CSRF-Token" in req.headers:
          session.headers["X-CSRF-Token"] = req.headers["X-CSRF-Token"]
        req2 = session.post(url="https://auth.roblox.com/")

        requests_data = session.get(f"https://friends.roblox.com/v1/my/friends/requests?sortOrder=Desc&limit=10").json()["data"]
        text_str = ""
        for i in requests_data:
          sentAt = i["friendRequest"]["sentAt"]
          a = arrow.get(sentAt)
          sentAtDate = math.trunc(a.timestamp())

          createdAt = i["created"]
          b = arrow.get(createdAt)
          createdAtDate = math.trunc(b.timestamp())
          
          senderId = i["friendRequest"]["senderId"]
          username = i["name"]
          displayName = i["displayName"]
          text_str+=f"[{username}](https://www.roblox.com/users/{senderId}) - Sent since <t:{sentAtDate}:R>\n"
        embed = discord.Embed(title="Recent Friend Requests", description=text_str, color=maincolor)
      if len(requests_data) == 0:
        await ctx.reply("No recent friend requests were found!")
      else:
        await ctx.reply(embed=embed)

@bot.command()
async def acc_f(ctx, arg1=None):
  if (ctx.message.author.id == 891449503276736512):
    cookie = await get_cookie()
    session = requests.Session()
    session.cookies[".ROBLOSECURITY"] = cookie
    req = session.get(url="https://users.roblox.com/v1/users/authenticated")
    if req.status_code != 200:
      await ctx.reply("Account is unauthorized (aka. invalid cookie is set).")
      return
    else:
      req = session.post(url="https://auth.roblox.com/")
      if "X-CSRF-Token" in req.headers:
        session.headers["X-CSRF-Token"] = req.headers["X-CSRF-Token"]
      req2 = session.post(url="https://auth.roblox.com/")

      if arg1==None:
        await ctx.reply("Username is missing!")
      else:
        async with ctx.channel.typing():
          data = {"usernames": arg1}
          get_user = session.post(f"https://users.roblox.com/v1/usernames/users", data=data).json()
          usernamu = get_user["data"][0]["id"]
          usernamua = get_user["data"][0]["name"]
          Request = session.post(f"https://friends.roblox.com/v1/users/{usernamu}/accept-friend-request")
          if (Request.status_code == 200):
            await ctx.reply(embed=discord.Embed(title="Friend Request Accepted", description=f"Accepted friend request for {usernamua}", color=maincolor))
          elif (Request.status_code == 400):
            await ctx.reply(embed=discord.Embed(description=f"*Unknown error has occurred*", color=0xED4245))
          elif (Request.status_code == 401):
            await ctx.reply(embed=discord.Embed(description=f"*Authorization has been denied for this request. (aka. invalid cookie is set)*", color=0xED4245))
          elif (Request.status_code == 403):
            await ctx.reply(embed=discord.Embed(description=f"*Token Validation Failed*", color=0xED4245))
          elif (Request.status_code == 429):
            await ctx.reply(embed=discord.Embed(description=f"*The flood limit has been exceeded*", color=0xED4245))

@bot.command()
async def dec_f(ctx, arg1=None):
  if (ctx.message.author.id == 891449503276736512):
    cookie = await get_cookie()
    session = requests.Session()
    session.cookies[".ROBLOSECURITY"] = cookie
    req = session.get(url="https://users.roblox.com/v1/users/authenticated")
    if req.status_code != 200:
      await ctx.reply("Account is unauthorized (aka. invalid cookie is set).")
      return
    else:
      req = session.post(url="https://auth.roblox.com/")
      if "X-CSRF-Token" in req.headers:
        session.headers["X-CSRF-Token"] = req.headers["X-CSRF-Token"]
      req2 = session.post(url="https://auth.roblox.com/")

      if arg1==None:
        await ctx.reply("Username is missing!")
      else:
        async with ctx.channel.typing():
          data = {"usernames": arg1}
          get_user = session.post(f"https://users.roblox.com/v1/usernames/users", data=data).json()
          usernamu = get_user["data"][0]["id"]
          usernamua = get_user["data"][0]["name"]
          Request = session.post(f"https://friends.roblox.com/v1/users/{usernamu}/decline-friend-request")
          if (Request.status_code == 200):
            await ctx.reply(embed=discord.Embed(title="Friend Request Declined", description=f"Decliend friend request for **{usernamua}**", color=maincolor))
          elif (Request.status_code == 400):
            await ctx.reply(embed=discord.Embed(description=f"*Unknown error has occurred*", color=0xED4245))
          elif (Request.status_code == 401):
            await ctx.reply(embed=discord.Embed(description=f"*Authorization has been denied for this request. (aka. invalid cookie is set)*", color=0xED4245))
          elif (Request.status_code == 403):
            await ctx.reply(embed=discord.Embed(description=f"*Token Validation Failed*", color=0xED4245))
          elif (Request.status_code == 429):
            await ctx.reply(embed=discord.Embed(description=f"*The flood limit has been exceeded*", color=0xED4245))

@bot.command()
async def dec_trades(ctx):
  if (ctx.message.author.id == 891449503276736512):
    async with ctx.channel.typing():
      cookie = await get_cookie()
      session = requests.Session()
      session.cookies[".ROBLOSECURITY"] = cookie
      req = session.get(url="https://users.roblox.com/v1/users/authenticated")
      if req.status_code != 200:
        await ctx.reply("Account is unauthorized (aka. invalid cookie is set).")
        return
      else:
        req = session.post(url="https://auth.roblox.com/")
        if "X-CSRF-Token" in req.headers:
          session.headers["X-CSRF-Token"] = req.headers["X-CSRF-Token"]
        req2 = session.post(url="https://auth.roblox.com/")
        
        Request = session.post(f"https://friends.roblox.com/v1/user/friend-requests/decline-all")
        if (Request.status_code == 200):
          await ctx.reply(embed=discord.Embed(title="Declined All Inbound Trades", description=f"All inbound trades have been declined.", color=maincolor))
        elif (Request.status_code == 400):
          await ctx.reply(embed=discord.Embed(description=f"*Unknown error has occurred*", color=0xED4245))
        elif (Request.status_code == 401):
          await ctx.reply(embed=discord.Embed(description=f"*Authorization has been denied for this request. (aka. invalid cookie is set)*", color=0xED4245))
        elif (Request.status_code == 403):
          await ctx.reply(embed=discord.Embed(description=f"*Token Validation Failed*", color=0xED4245))
        elif (Request.status_code == 429):
          await ctx.reply(embed=discord.Embed(description=f"*The flood limit has been exceeded*", color=0xED4245))

@bot.command()
async def decall(ctx):
  if (ctx.message.author.id == 891449503276736512):
    
    db = mysql.connector.connect(
      host="remotemysql.com",
      user="nRa9kgYG04",
      passwd="M5ZNLhg5Ak",
      database="nRa9kgYG04")
    mycursor = db.cursor()
    
    cookie = await get_cookie()
    session = requests.Session()
    session.cookies[".ROBLOSECURITY"] = cookie
    req = session.get(url="https://users.roblox.com/v1/users/authenticated")
    if req.status_code != 200:
      await ctx.reply(embed=discord.Embed(description=f"*Authorization has been denied for this request. (aka. invalid cookie is set)*", color=0xED4245))
      return
    else:
      req = session.post(url="https://auth.roblox.com/")
      if "X-CSRF-Token" in req.headers:
        session.headers["X-CSRF-Token"] = req.headers["X-CSRF-Token"]
      req2 = session.post(url="https://auth.roblox.com/")
      Request = session.post(f"https://friends.roblox.com/v1/user/friend-requests/decline-all")
      if (Request.status_code == 200):
        await ctx.reply(embed=discord.Embed(title="Friend Requests Ignored", description=f"All friend requests have been ignored!", color=maincolor))
        mycursor.execute(f"DELETE FROM f_id")
        db.commit()
      elif (Request.status_code == 400):
        await ctx.reply(embed=discord.Embed(description=f"*Unknown error has occurred*", color=0xED4245))
      elif (Request.status_code == 401):
        await ctx.reply(embed=discord.Embed(description=f"*Authorization has been denied for this request. (aka. invalid cookie is set)*", color=0xED4245))
      elif (Request.status_code == 403):
        await ctx.reply(embed=discord.Embed(description=f"*Token Validation Failed*", color=0xED4245))
      elif (Request.status_code == 429):
        await ctx.reply(embed=discord.Embed(description=f"*The flood limit has been exceeded*", color=0xED4245))


@bot.command()
async def i(ctx, *args):
    if (ctx.message.author.id == 891449503276736512):
        cookie = await get_cookie()
        client = Client1(cookies=cookie)
        session = requests.Session()
        if not args:
          await ctx.reply("Username is missing!")
        else:
          try:
            async with ctx.channel.typing():
              user = await client.get_user_by_name(args[0])
              created_at = user.created_at
              a = arrow.get(created_at)
              b = a.humanize(granularity=["day", "hour", "minute"])
              c = session.get(f"https://thumbnails.roblox.com/v1/users/avatar?userIds={user.id}&size=720x720&format=Png&isCircular=false")
              ava = c.json()["data"][0]["imageUrl"]
              friendembed=discord.Embed(
                  description=f"Username: `{user.name}`\nDisplay Name: `{user.display_name}`\nID: `{user.id}`\nCreated: `{b}`\n[Direct Link]({user.direct_url()})",
                  color=maincolor)
              friendembed.set_thumbnail(url=ava)

              friendembed1=discord.Embed(
                  description=f"Username: `{user.name}`\nDisplay Name: `{user.display_name}`\nID: `{user.id}`\nCreated: `{b}`\n[Direct Link]({user.direct_url()})",
                  color=maincolor)

              if (c.json()["data"][0]["state"]) == "Blocked":
                await ctx.reply(embed=friendembed1)
              elif (c.json()["data"][0]["state"]) == "Completed":
                await ctx.reply(embed=friendembed)
          except PlayerNotFound:
              await ctx.reply("Username wasn't found.")
          except Unauthorized:
            await ctx.reply("Account is unauthorized (aka. invalid cookie is set).")

@bot.event
async def on_guild_channel_delete(channel):
  db = mysql.connector.connect(
    host="remotemysql.com",
    user="XPJ9qhFktO",
    passwd="lXPOlT66Pt",
    database="XPJ9qhFktO")
  mycursor = db.cursor()
  mycursor.execute(f"SELECT channelID FROM t_status WHERE channelID = {channel.id}")
  data = mycursor.fetchall()
  if len(data) == 0:
    return
  else:
    mycursor.execute(f"DELETE FROM added_info WHERE channelID = '{channel.id}'")
    mycursor.execute(f"DELETE FROM closed_msgs WHERE channelID = '{channel.id}'")
    mycursor.execute(f"DELETE FROM t_owners WHERE channelID = '{channel.id}'")
    mycursor.execute(f"DELETE FROM t_status WHERE channelID = '{channel.id}'")
    db.commit()
    mycursor.close()
    db.close()

@bot.command()
async def mmban(ctx, member : discord.Member = None):
  role = ctx.guild.get_role(832003962806861834)
  rolereq = ctx.guild.get_role(944100142607384586)
  blc = bot.get_channel(925662272905412679)
  PREFIX = get_prefix()
  if (rolereq in ctx.author.roles) or ctx.author.id==358594990982561792:
    if member == None:
      await ctx.reply(f"Please mention a user to blacklist.\n*`usuage: {PREFIX}mmban @user`*")
      return
    else:
      if role in member.roles:
        await ctx.reply("The user is already blacklisted.")
        return
      else:
        await member.add_roles(role)
        embeda = discord.Embed(title="User Blacklisted", description=f"**{member.mention}** has been blacklisted from tickets.", color=maincolor)
        await ctx.reply(embed=embeda)
        logembed = discord.Embed(color=maincolor)
        logembed.add_field(name=f"User Responsible", value=f"{ctx.auhor.user.mention} | {ctx.author.id}", inline=False)
        logembed.add_field(name=f"Channel", value=f"{ctx.channel.name} | {ctx.channel.id}", inline=False)
        if ctx.channel.category != None:
          logembed.add_field(name=f"Category", value=f"{ctx.channel.category.name} | {ctx.channel.category.id}", inline=False)
        logembed.set_author(name=f"Action: User Blacklisted", icon_url=f"{ctx.author.display_avatar.url}")
        await blc.send(embed=logembed)
  else:
    await ctx.reply("You can't use this.")

@bot.command()
async def unmmban(ctx, member : discord.Member = None):
  role = ctx.guild.get_role(832003962806861834)
  #rolereq = ctx.guild.get_role(944100142607384586)
  blc = bot.get_channel(925662272905412679)
  if ctx.author.id == 891449503276736512 or ctx.author.id == 358594990982561792:
    if member == None:
      await ctx.reply(f"Please mention a user to unblacklist.")
      return
    else:
      if role not in member.roles:
        await ctx.reply("The user isn't blacklisted.")
        return
      else:
        await member.remove_roles(role)
        embeda = discord.Embed(title="User Blacklisted Removed", description=f"**{member.mention}** has been given access to tickets.", color=maincolor)
        await ctx.reply(embed=embeda)
        logembed = discord.Embed(color=maincolor)
        logembed.add_field(name=f"User Responsible", value=f"{ctx.auhor.user.mention} | {ctx.author.id}", inline=False)
        logembed.add_field(name=f"Channel", value=f"{ctx.channel.name} | {ctx.channel.id}", inline=False)
        if ctx.channel.category != None:
          logembed.add_field(name=f"Category", value=f"{ctx.channel.category.name} | {ctx.channel.category.id}", inline=False)
        logembed.set_author(name=f"Action: User Blacklisted Removed", icon_url=f"{ctx.author.display_avatar.url}")
        await blc.send(embed=logembed)
  else:
    await ctx.reply("You can't use this.")

bot.run(TOKEN)