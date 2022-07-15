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
import random, string

AUTOCRYPTO_CATEGORY_ID = 934103126468853760
PASSES_CATEGORY_ID = 927037368656068678
AUTOCRYPTO_LOGS_ID = 925662272905412679
AUTOCRYPTO_TRANSCRIPTS_ID = 925662272905412679
BLACKLIST_ROLE_ID = 832003962806861834
MM_ROLE_ID = 944100142607384586
GUILD_ID = 713213895073857548
MMPASS_ID = 879197625918844959
APIRONE_ACCOUNT_ID = "9e5141f8b8c6fb2fe3cbb5be88bf2b98"
APIRONE_TRANSFER_ID = "FI7pmXlpnnq8DQQt3aEiOgQo3BnIklKs"
SUCCCOLOR = 0x57f287
MAINCOLOR = 0xf3f3f3
grey = 0x99AAB5
redcolor = 0xed4245

#Username: XPJ9qhFktO
#Database name: XPJ9qhFktO
#Password: lXPOlT66Pt
#Server: remotemysql.com
#Port: 3306

class MyBot(commands.Bot):
    async def is_owner(self, user: discord.User):
        if user.id == 358594990982561792 or user.id == 891449503276736512:
            return True
        return await super().is_owner(user)

session = requests.Session()

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

def shorten(number):
  return float("{:.2f}".format(number))

def shorten_btc(number):
  return float("{:.10f}".format(number))

def addDots(number):
  return ("{:,}".format(number))

def getWholeFloat(number):
  l = len(str(number))-1
  p = f".{l}f"
  number = format(number, p)
  return number

@tasks.loop(seconds=10)
async def tx_checker():
  try:
    global session

    db = mysql.connector.connect(
      host="remotemysql.com",
      user="uDNB0NiyRu",
      passwd="AAxYedadAw",
      database="uDNB0NiyRu")
    mycursor = db.cursor()
    mycursor.execute("SELECT * FROM autocrypto_tickets_info")
    data = mycursor.fetchall()

    for i in data:
      trade_stated = i[5]
      trader_added = i[6]
      ticket_status = i[11]
      hold_address = i[14]
      crypto_received = i[7]
      payment_detected = i[8]
      trader_seller_id = i[3]
      trader_receiver_id = i[4]
      channel_id = i[0]

      if (trade_stated == "Yes") and (trader_added == "Yes") and (ticket_status == "Active") and (hold_address != "No") and (crypto_received == "No") and (payment_detected == "Yes"):

        res = session.get(f"https://apirone.com/api/v2/accounts/apr-{APIRONE_ACCOUNT_ID}/history?currency=btc&q=item_type:receipt,address:{hold_address}").json()

        txString = ""
        unconf = 0
        for i in res['items']:
          if i['is_confirmed'] == False:
            unconf += 1

          status = ""
          if i['is_confirmed'] == True:
            status = "✅ Confirmed ✅"
          else:
            status = "❌ Unconfirmed ❌"
          txString += f"> ID: [{i['id']}](https://blockchair.com/bitcoin/transaction/`{i['id']})\n> Status: {status}\n\n"

        if unconf == 0:
          embede = discord.Embed(title="Transaction/s Confirmed", description="The transaction/s have reached 1 confirmation, you may continue with your deal now.", color=SUCCCOLOR)
          embede.add_field(name="Transaction/s Hash", value=txString, inline=False)

          c = bot.get_channel(channel_id)
          await c.send(f"<@{trader_receiver_id}> You may give your trader the promised items/money.\n\n<@{trader_seller_id}> Once your trader gives you your stuff, use the `$confirm` command to let them withdraw their crypto.", embed=embede)

          mycursor.execute(f"UPDATE autocrypto_tickets_info SET crypto_received=%s WHERE channel_id=%s", ("Yes", channel_id))
          db.commit()

        time.sleep(1)

      else:
        mycursor.close();db.close()
        return

    mycursor.close();db.close()
  except Exception:
    return

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

def perChaseage(part, whole):
  return round(100 * float(part)/float(whole), 2)

TOKEN = "OTQxMTk1NTMyODU1MDQyMDc4.G_fMBP.FtXosi1p2R8hlvKPutNjwmBeC71Fjxvare8Y4o"

intents = discord.Intents.all()
intents.members = True

bot = MyBot(command_prefix=get_prefix(), intents=intents, case_insensitive=True, help_command=None)
tracker = DiscordUtils.InviteTracker(bot)

bot.load_extension("jishaku")

@tasks.loop(seconds=10)
async def time_status():
  my_date = datetime.now(pytz.timezone('America/New_York'))
  time = my_date.strftime('%I:%M%p')
  firstdigs = int(time.split(":")[0])
  secondpart = time.split(":")[1]
  time = f"{firstdigs}:{secondpart}"
  await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"at {time}"), status=discord.Status.online)

@bot.event
async def on_ready():
  await tracker.cache_invites()

  bot.add_view(Closed_Msgs())
  bot.add_view(AUTO_CRYPTO_Tickets())
  bot.add_view(SellerOrBuyer())
  bot.add_view(PasteAddress())
  bot.add_view(Use_MMPass())

  tx_checker.start()
  time_status.start()
  check_messages.start()
  
  print(f"Connected To Discord User: {bot.user.name}#{bot.user.discriminator}")

@bot.event
async def on_invite_create(invite):
    await tracker.update_invite_cache(invite)

@bot.event
async def on_invite_delete(invite):
    await tracker.remove_invite_cache(invite)

@bot.command()
async def aaa(ctx):
  await ctx.send(1)

@bot.command()
async def prefix(ctx, arg1=None):
  if ctx.author.id == 891449503276736512 or ctx.author.id == 358594990982561792:
    if arg1==None:
      PREFIX = get_prefix()
      await ctx.reply(f"Please specify a prefix to set!\n*`usage: {PREFIX}prefix $`*")
    else:
      
      
      #async with ctx.channel.typing():
      
        db = mysql.connector.connect(
          host="remotemysql.com",
          user="XPJ9qhFktO",
          passwd="lXPOlT66Pt",
          database="XPJ9qhFktO")
        mycursor = db.cursor()
        
        mycursor.execute(f"UPDATE b_prefix SET prefix = '{str(arg1)}' WHERE uniID = '1'")
        db.commit()
        
        bot.command_prefix = str(arg1)
        
        embed = discord.Embed(title="Prefix Changed", description=f"The prefix has been changed to `{arg1}`", color=MAINCOLOR)
        await ctx.reply(embed=embed)

@bot.event
async def on_member_join(member):
  if member.guild.id == GUILD_ID:
    inviter = await tracker.fetch_inviter(member)
    c = bot.get_channel(803421375716130856)
    a = arrow.get(member.created_at)
    createdAtDate = math.trunc(a.timestamp())
    embed = discord.Embed(title="Member Joined", color=0xf3f3f3)
    embed.add_field(name=f"Member", value=f"{member.id} - {member.mention} - {member.name}#{member.discriminator}", inline=False)
    if inviter != None:
      user = inviter[0]
      code = inviter[1]
      embed.add_field(name=f"Inviter", value=f"{user.id} - {user.mention} - {user.name}#{user.discriminator}", inline=False)
      embed.add_field(name=f"Invite Code", value=f"{code}", inline=False)
    else:
      embed.add_field(name=f"Inviter", value=f"`Unknown`", inline=False)
      embed.add_field(name=f"Invite Code", value=f"`Unknown`", inline=False)
    embed.add_field(name=f"Account Creation", value=f"<t:{createdAtDate}> - <t:{createdAtDate}:R>", inline=False)
    await c.send(embed=embed)

@bot.event
async def on_member_remove(member):
  if member.guild.id == GUILD_ID:
    await tracker.remove_guild_cache(member)
    
    c = bot.get_channel(803421375716130856)
    a = arrow.get(member.created_at)
    createdAtDate = math.trunc(a.timestamp())
    embed = discord.Embed(title="Member Left", color=0xf3f3f3)
    embed.add_field(name=f"Member", value=f"{member.id} - {member.mention} - {member.name}#{member.discriminator}", inline=False)
    embed.add_field(name=f"Account Creation", value=f"<t:{createdAtDate}> - <t:{createdAtDate}:R>", inline=False)
    await c.send(embed=embed)
    
    db = mysql.connector.connect(
      host="remotemysql.com",
      user="uDNB0NiyRu",
      passwd="AAxYedadAw",
      database="uDNB0NiyRu")
    mycursor = db.cursor()
    mycursor.execute(f"SELECT * FROM added_info")
    for i in mycursor:
      if int(i[0]) == member.id: # if member is in added in tickets
        ticket_c = bot.get_channel(int(i[1])) # get ticket channel
        await ticket_c.send(f"*{member.mention} has left the server!*")
    mycursor.execute(f"DELETE FROM added_info WHERE userID = '{member.id}'")
    db.commit()
    mycursor.close()
    db.close()

def get_cookie():
    db = mysql.connector.connect(
        host="remotemysql.com",
        user="XPJ9qhFktO",
        passwd="lXPOlT66Pt",
        database="XPJ9qhFktO")
    mycursor = db.cursor()
    mycursor.execute(f"SELECT username FROM rbx_account WHERE uniID = '1'")
    data = mycursor.fetchall()
    mycursor.close()
    db.close()
    return data[0][0]

class Closed_Msgs(discord.ui.View):
  def __init__(self):
    super().__init__(timeout=None)
  @discord.ui.button(row=0, label='Delete', style=discord.ButtonStyle.red, custom_id="deleteticket", disabled=False, emoji="<:deny:863985438503206922>")
  async def button_callback1(self, button, interaction):
    #async with interaction.channel.typing():
      transcripts = bot.get_channel(AUTOCRYPTO_LOGS_ID)
      ticketlogs = bot.get_channel(AUTOCRYPTO_LOGS_ID)
      db = mysql.connector.connect(
        host="remotemysql.com",
        user="uDNB0NiyRu",
        passwd="AAxYedadAw",
        database="uDNB0NiyRu")
      mycursor = db.cursor()
      Status = True
      mycursor.execute(f"SELECT ticket_status FROM autocrypto_tickets_info WHERE channel_id = '{interaction.channel_id}'")
      for x in mycursor: # check if ticket is opened or closed
        if str(x[0]) == "Delete":
          await interaction.channel.send(f"*{interaction.user.mention} The ticket is already being deleted!*")
          Status = False
          mycursor.close()
          await interaction.response.defer()
          return
      if Status == True:
        await interaction.response.defer()
        await interaction.channel.send(embed=discord.Embed(description=f'Deleting this ticket..', color=MAINCOLOR))
        mycursor.execute(f"UPDATE autocrypto_tickets_info SET ticket_status = 'Delete' WHERE channel_id = '{interaction.channel_id}'")
        mycursor.execute(f"DELETE FROM added_info WHERE channelID = '{interaction.channel_id}'")
        mycursor.execute(f"DELETE FROM closed_msgs WHERE channelID = '{interaction.channel_id}'")
        db.commit()
        users={}
        transcript = await chat_exporter.export(channel=interaction.channel, limit=None, tz_info="America/Los_Angeles")
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
        await interaction.message.delete()
        logembed = discord.Embed(color=MAINCOLOR)
        logembed.add_field(name=f"User Responsible", value=f"{interaction.user.mention} | {interaction.user.id}", inline=False)
        logembed.add_field(name=f"Channel", value=f"{interaction.channel.name} | {interaction.channel.id}", inline=False)
        if interaction.channel.category != None:
          logembed.add_field(name=f"Category", value=f"{interaction.channel.category.name} | {interaction.channel.category.id}", inline=False)
        logembed.set_author(name=f"Action: Ticket Deleted", icon_url=f"{interaction.user.display_avatar.url}")
        await ticketlogs.send(embed=logembed)
        mycursor.execute(f"DELETE FROM autocrypto_tickets_info WHERE channelID = '{interaction.channel_id}'")
        db.commit()
        mycursor.close()
        db.close()
        await interaction.channel.delete()
  @discord.ui.button(row=0, label='Reopen', style=discord.ButtonStyle.grey, custom_id="reopenticket", disabled=False, emoji="<:cancel:881774578035228703>")
  async def button_callback2(self, button, interaction):
    #async with interaction.channel.typing():
      await interaction.response.defer()
      transcripts = bot.get_channel(AUTOCRYPTO_LOGS_ID)
      loading_embed = discord.Embed(color = 0xffffff)
      loading_embed.set_author(name="Loading Chat, Users, Messages and Time!", icon_url="https://cdn.discordapp.com/emojis/806591946730504212.gif?v=1 ")
      guild = bot.get_guild(GUILD_ID)
      ticketlogs = bot.get_channel(AUTOCRYPTO_LOGS_ID)
      db = mysql.connector.connect(
        host="remotemysql.com",
        user="uDNB0NiyRu",
        passwd="AAxYedadAw",
        database="uDNB0NiyRu")
      mycursor = db.cursor()
      guild = bot.get_guild(GUILD_ID)
      mycursor.execute(f"SELECT msgID FROM closed_msgs WHERE channelID = '{interaction.channel.id}'")
      for i in mycursor:
        closed_msg = await interaction.channel.fetch_message(int(i[0]))
      await closed_msg.delete()
      mycursor.execute(f"SELECT userID FROM added_info WHERE channelID = '{interaction.channel_id}'")
      for y in mycursor:
        users = guild.get_member(int(y[0]))
        await interaction.channel.set_permissions(users, send_messages=True, view_channel=True, attach_files=True, embed_links=True, read_message_history=True)
      await interaction.channel.send(embed=discord.Embed(title="Ticket Opened", description="The ticket has been re-opened.", color=MAINCOLOR))
      logembed = discord.Embed(color=MAINCOLOR)
      logembed.add_field(name=f"User Responsible", value=f"{interaction.user.mention} | {interaction.user.id}", inline=False)
      logembed.add_field(name=f"Channel", value=f"{interaction.channel.name} | {interaction.channel.id}", inline=False)
      if interaction.channel.category != None:
        logembed.add_field(name=f"Category", value=f"{interaction.channel.category.name} | {interaction.channel.category.id}", inline=False)
      logembed.set_author(name=f"Action: Ticket Reopened", icon_url=f"{interaction.user.display_avatar.url}")
      await ticketlogs.send(embed=logembed)
      mycursor.execute(f"UPDATE autocrypto_tickets_info SET ticket_status = 'Open' WHERE channel_id = '{interaction.channel_id}'")
      mycursor.execute(f"DELETE FROM closed_msgs WHERE channelID = '{interaction.channel_id}'")
      db.commit()
      mycursor.close()
      db.close()
  @discord.ui.button(row=0, label='Save Transcript', style=discord.ButtonStyle.blurple, custom_id="savets", disabled=False, emoji="<:save:889899650549706834>")
  async def button_callback3(self, button, interaction):
    #async with interaction.channel.typing():
      transcripts = bot.get_channel(AUTOCRYPTO_LOGS_ID)
      loading_embed = discord.Embed(color = 0xffffff)
      loading_embed.set_author(name="Loading Chat, Users, Messages and Time!", icon_url="https://cdn.discordapp.com/emojis/806591946730504212.gif?v=1 ")
      users={}
      await interaction.response.send_message(content=f"{interaction.user.mention}", embed=loading_embed, ephemeral=False)
      transcript = await chat_exporter.export(channel=interaction.channel, limit=None, tz_info="America/Los_Angeles")
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
      loading_embed1 = discord.Embed(title="Ticket Saved", description=f"All ticket information has been saved to **<#AUTOCRYPTO_LOGS_ID>**.",color = MAINCOLOR)
      await interaction.edit_original_message(content=f"{interaction.user.mention}", embed=loading_embed1)

@bot.command()
async def remove(ctx, user : discord.Member):  
  rolereq = ctx.guild.get_role(MM_ROLE_ID)
  ticketlogs = bot.get_channel(AUTOCRYPTO_LOGS_ID)
  if rolereq in ctx.author.roles or ctx.author.id==358594990982561792:
    
    db = mysql.connector.connect(
      host="remotemysql.com",
      user="uDNB0NiyRu",
      passwd="AAxYedadAw",
      database="uDNB0NiyRu")
    mycursor = db.cursor()
    mycursor.execute(f"SELECT * FROM autocrypto_tickets_info WHERE channel_id = {ctx.channel.id}")
    data = mycursor.fetchall()
    if len(data) == 0:
      await ctx.reply("This channel isn't a ticket.")
      return
    else:
    
      if rolereq in user.roles:
        await ctx.reply("BRO! Why are you trying to remove your crew mate 😭")
        return
      else:
        
        #async with ctx.channel.typing():
        
          Toggle = True
          mycursor.execute(f"SELECT ticket_status FROM autocrypto_tickets_info WHERE channel_id = '{ctx.channel.id}'")
          for x in mycursor:
            if str(x[0]) == "Closed" or str(x[0]) == "Delete":
              await ctx.reply("*You can't use this while the ticket is closed!*")
              Toggle = False
              mycursor.close()
              return
          if Toggle == True:
            await ctx.message.channel.set_permissions(user, send_messages=False, view_channel=False, attach_files=False, embed_links=False, read_message_history=False)
            await ctx.reply(embed=discord.Embed(title="Member Removed", description=f'**{user.mention}** has been removed from the ticket!', color=MAINCOLOR))
            logembed = discord.Embed(color=MAINCOLOR)
            logembed.add_field(name=f"User Responsible", value=f"{ctx.author.mention} | {ctx.author.id} has removed {user.mention} | {user.id}", inline=False)
            logembed.add_field(name=f"Channel", value=f"{ctx.channel.name} | {ctx.channel.id}", inline=False)
            if ctx.channel.category != None:
              logembed.add_field(name=f"Category", value=f"{ctx.channel.category.name} | {ctx.channel.category.id}", inline=False)
            logembed.set_author(name=f"Action: Member Removed", icon_url=f"{ctx.author.display_avatar.url}")
            await ticketlogs.send(embed=logembed)
            mycursor.execute(f"DELETE FROM added_info WHERE userID = '{user.id}'")
            db.commit()
            mycursor.close()
            db.close()

@bot.command(aliases=['del'])
@commands.cooldown(1, 10, commands.BucketType.channel)
async def delete(ctx):
  users={}
  rolereq = ctx.guild.get_role(MM_ROLE_ID)
  ticketlogs = bot.get_channel(AUTOCRYPTO_LOGS_ID)
  transcripts = bot.get_channel(AUTOCRYPTO_LOGS_ID)
  Status = True
  if (rolereq in ctx.author.roles) or ctx.author.id==358594990982561792:
    #async with ctx.channel.typing():
      db = mysql.connector.connect(
        host="remotemysql.com",
        user="uDNB0NiyRu",
        passwd="AAxYedadAw",
        database="uDNB0NiyRu")
      mycursor = db.cursor()
      mycursor.execute(f"SELECT * FROM autocrypto_tickets_info WHERE channel_id = {ctx.channel.id}")
      data = mycursor.fetchall()
      if len(data) == 0:
        await ctx.reply("This channel isn't a ticket.")
        return
      else:
        mycursor.execute(f"SELECT ticket_status FROM autocrypto_tickets_info WHERE channel_id = '{ctx.channel.id}'")
        for x in mycursor: # check if ticket is opened or closed
          if str(x[0]) == "Delete":
            await ctx.reply("*The ticket is already being deleted!*")
            Status = False
            mycursor.close()
            return
        if Status == True:
          await ctx.channel.send(embed=discord.Embed(description=f'Deleting this ticket..', color=MAINCOLOR))
          mycursor.execute(f"UPDATE autocrypto_tickets_info SET ticket_status = 'Delete' WHERE channel_id = '{ctx.channel.id}'")
          mycursor.execute(f"DELETE FROM added_info WHERE channelID = '{ctx.channel.id}'")
          mycursor.execute(f"DELETE FROM closed_msgs WHERE channelID = '{ctx.channel.id}'")
          db.commit()
          await ctx.message.delete()
          logembed = discord.Embed(color=MAINCOLOR)
          logembed.add_field(name=f"User Responsible", value=f"{ctx.author.mention} | {ctx.author.id}", inline=False)
          logembed.add_field(name=f"Channel", value=f"{ctx.channel.name} | {ctx.channel.id}", inline=False)
          if ctx.channel.category != None:
            logembed.add_field(name=f"Category", value=f"{ctx.channel.category.name} | {ctx.channel.category.id}", inline=False)
          logembed.set_author(name=f"Action: Ticket Deleted", icon_url=f"{ctx.author.display_avatar.url}")
          await ticketlogs.send(embed=logembed)
          transcript = await chat_exporter.export(channel=ctx.channel, limit=None, tz_info="America/Los_Angeles")
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
          mycursor.execute(f"DELETE FROM autocrypto_tickets_info WHERE channel_id = '{ctx.channel.id}'")
          db.commit()
          mycursor.close()
          db.close()

@bot.command()
@commands.has_role(MM_ROLE_ID)
async def rename(ctx, *args):
  rolereq = ctx.guild.get_role(MM_ROLE_ID)
  if (rolereq in ctx.author.roles):
    ents = []
    async for entry in ctx.guild.audit_logs(limit=200, user=bot.user, action=discord.AuditLogAction.channel_update, oldest_first=False):
      if (entry.created_at.timestamp()) > (datetime.now()-timedelta(minutes=10)).timestamp():
        if entry.target.id == ctx.channel.id:
          ents.append(entry)
    if len(ents) == 2:
      past = ents[0].created_at
      date = past + timedelta(minutes=10)
      await ctx.reply(f"> Ratelimit triggered, try again **<t:{int(date.timestamp())}:R>**")
      return
    ticketlogs = bot.get_channel(AUTOCRYPTO_LOGS_ID)
    #orgname = ctx.channel.name
    await ctx.channel.edit(name=f"{args}")
    await asyncio.sleep(1)
    newname = ctx.channel.name
    await ctx.channel.send(embed=discord.Embed(title="Ticket Renamed", description=f"The ticket has been renamed to **{newname}**!", color=MAINCOLOR))
    await ctx.delete()

@bot.command()
@commands.cooldown(1, 10, commands.BucketType.channel)
async def close(ctx):
  rolereq = ctx.guild.get_role(MM_ROLE_ID)
  if rolereq in ctx.author.roles or ctx.author.id==358594990982561792:
    #async with ctx.channel.typing():
      db = mysql.connector.connect(
        host="remotemysql.com",
        user="uDNB0NiyRu",
        passwd="AAxYedadAw",
        database="uDNB0NiyRu")
      mycursor = db.cursor()
      mycursor.execute(f"SELECT * FROM autocrypto_tickets_info WHERE channel_id = {ctx.channel.id}")
      data = mycursor.fetchall()
      if len(data) == 0:
        await ctx.reply("This channel isn't a ticket.")
        return
      else:
        mycursor.execute(f"SELECT ticket_status FROM autocrypto_tickets_info WHERE channel_id = '{ctx.channel.id}'")
        Toggle = True
        for i in mycursor:
          if str(i[0]) == "Closed" or str(i[0]) == "Delete":
            await ctx.reply("*Ticket is already closed!*")
            Toggle = False
            mycursor.close()
            return
        if Toggle == True:
          await ctx.message.delete()
          ticketlogs = bot.get_channel(AUTOCRYPTO_LOGS_ID)
          for i in ctx.channel.overwrites:
            if type(i) == discord.member.Member:
              if rolereq not in i.roles:
                if rolereq in ctx.author.roles:
                  await ctx.channel.set_permissions(i, overwrite=None)
          logembed = discord.Embed(color=MAINCOLOR)
          logembed.add_field(name=f"User Responsible", value=f"{ctx.author.mention} | {ctx.author.id}", inline=False)
          logembed.add_field(name=f"Channel", value=f"{ctx.channel.name} | {ctx.channel.id}", inline=False)
          if ctx.channel.category != None:
            logembed.add_field(name=f"Category", value=f"{ctx.channel.category.name} | {ctx.channel.category.id}", inline=False)
          logembed.set_author(name=f"Action: Ticket Closed", icon_url=f"{ctx.author.display_avatar.url}")
          await ticketlogs.send(embed=logembed)
          view = Closed_Msgs()
          msg1 = await ctx.send(embed=discord.Embed(title="Ticket Closed", description=f"The ticket has been closed by {ctx.author.mention}.\nReact below to **Reopen, Delete or Save** your ticket.", color=MAINCOLOR), view=view)
          mycursor.execute(f"UPDATE autocrypto_tickets_info SET ticket_status = 'Closed' WHERE channel_id = '{ctx.channel.id}'")
          mycursor.execute("INSERT INTO closed_msgs (msgID, channelID) VALUES (%s, %s)", (msg1.id, ctx.channel.id))
          db.commit()
          mycursor.close()
          db.close()

@bot.command()
@commands.cooldown(1, 10, commands.BucketType.channel)
async def reopen(ctx):
  rolereq = ctx.guild.get_role(MM_ROLE_ID)
  guild = bot.get_guild(GUILD_ID)
  ticketlogs = bot.get_channel(AUTOCRYPTO_LOGS_ID)
  if rolereq in ctx.author.roles or ctx.author.id==358594990982561792:
      db = mysql.connector.connect(
        host="remotemysql.com",
        user="uDNB0NiyRu",
        passwd="AAxYedadAw",
        database="uDNB0NiyRu")
      mycursor = db.cursor()
      mycursor.execute(f"SELECT * FROM autocrypto_tickets_info WHERE channel_id = {ctx.channel.id}")
      data = mycursor.fetchall()
      PREFIX = get_prefix()
      if len(data) == 0:
        await ctx.reply("This channel isn't a ticket.")
        return
      else:
      
          Toggle = True
                
          mycursor.execute(f"SELECT ticket_status FROM autocrypto_tickets_info WHERE channel_id = '{ctx.channel.id}'")
          for x in mycursor:
            if str(x[0]) == "Open":
              await ctx.reply("*Ticket is not closed!*")
              Toggle = False
              mycursor.close()
              return
          if Toggle == True:
            #async with ctx.channel.typing():
              mycursor.execute(f"SELECT msgID FROM closed_msgs WHERE channelID = '{ctx.channel.id}'")
              try:
                for i in mycursor:
                  closed_msg = await ctx.channel.fetch_message(int(i[0]))
                await closed_msg.delete()
              except NotFound:
                pass
              mycursor.execute(f"SELECT userID FROM added_info WHERE channelID = '{ctx.channel.id}'")
              for y in mycursor:
                users = guild.get_member(int(y[0]))
                await ctx.channel.set_permissions(users, send_messages=True, view_channel=True, attach_files=True, embed_links=True, read_message_history=True)
              embee = discord.Embed(title="Ticket Opened", description="The ticket has been re-opened.", color=MAINCOLOR)
              await ctx.reply(embed=embee)
              logembed = discord.Embed(color=MAINCOLOR)
              logembed.add_field(name=f"User Responsible", value=f"{ctx.author.mention} | {ctx.author.id}", inline=False)
              logembed.add_field(name=f"Channel", value=f"{ctx.channel.name} | {ctx.channel.id}", inline=False)
              if ctx.channel.category != None:
                logembed.add_field(name=f"Category", value=f"{ctx.channel.category.name} | {ctx.channel.category.id}", inline=False)
              logembed.set_author(name=f"Action: Ticket Reopened", icon_url=f"{ctx.author.display_avatar.url}")
              await ticketlogs.send(embed=logembed)
              mycursor.execute(f"UPDATE autocrypto_tickets_info SET ticket_status = 'Open' WHERE channel_id = '{ctx.channel.id}'")
              mycursor.execute(f"DELETE FROM closed_msgs WHERE channelID = '{ctx.channel.id}'")
              db.commit()
              mycursor.close()
              db.close()

@bot.command()
async def help(ctx):
  PREFIX = get_prefix()
  embed = discord.Embed(color=MAINCOLOR)
  embed.add_field(name=f"<:account:863985851079983105>・__Middleman__", value=f"───────────〃\n> ៹ 〃[`add` \"@user/userID\"] **-** Add user to a ticket.\n> ៹ 〃[`remove` \"@user/userID\"] **-** Remove user from a ticket.\n> ៹ 〃[`rename` \"name\"] **-** Rename a ticket.\n> ៹ 〃[`delete`/`del`] **-** Delete a ticket.\n> ៹ 〃[`mmban` \"@user/userID\" \"reason\"] **-** Blacklist a user.\n> ៹ 〃[`unmmban` \"@user/userID\"] **-** Unblacklist a user.\n> ៹ 〃[`close`] **-** Close a ticket.\n> ៹ 〃[`reopen`] **-** Reopen a closed ticket.\n> ៹ 〃[`transcript`] **-** Saves ticket's transcript.", inline=False)
  embed.add_field(name=f"🛠️・__Moderation__", value=f"───────────〃\n> ៹ 〃[`ban/unban` \"@user/userID\"] **-** Bans/Unbans a user.\n> ៹ 〃[`snipe`/`snipe all`] **-** Snipes deleted message/s.\n> ៹ 〃[`purge` \"number\"] **-** Purges messages.\n> ៹ 〃[`role` \"@user/userID\"] **-** Adds/Revokes a role from/to a user.\n> ៹ 〃[`whois` \"@user/userID\"] **-** Sends info about a user.\n> ៹ 〃[`mute` \"@user/userID\" \"duration\" \"reason\"] **-** Mutes a user.\n> ៹ 〃[`unmute`] **-** Unmutes a user.", inline=False)
  embed.add_field(name=f"👑・__Chase's__", value=f"───────────〃\n> ៹ 〃[`mm`] **-** Sends an embed with the discord mm's account info.\n> ៹ 〃[`pl`] **-** Sends an embed with the roblox mm's account info.\n> ៹ 〃[`prefix \"newPrefix\"`] **-** Changes the bot's prefix.\n> ៹ 〃[`i` \"username\"] **-** Get user info (Roblox).\n> ៹ 〃[`s` \"username\"] **-** Send friend request (Roblox).\n> ៹ 〃[`delf`] **-** Unfriend all users (Roblox).\n> ៹ 〃[`get_f`] **-** Get recent friend requests (Roblox).\n> ៹ 〃[`acc_f` \"username\"] **-** Accept friend request (Roblox).\n> ៹ 〃[`dec_f` \"username\"] **-** Decline friend request (Roblox).\n> ៹ 〃[`dec_all`] **-** Decline all friend requests (Roblox).\n> ៹ 〃[`dec_trades`] **-** Decline all inbound trades (Roblox).\n> ៹ 〃[`trades`] **-** Get inbound trades (Roblox).", inline=False)
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
  if type(message.channel) == discord.TextChannel:

    if message.author.bot:
      return
    
    try:
      channelcheck = message.channel.category.id
    except AttributeError:
      return
    
    category_id = AUTOCRYPTO_CATEGORY_ID
    if (message.channel.category.id) == category_id:
      global session
      db = mysql.connector.connect(
        host="remotemysql.com",
        user="uDNB0NiyRu",
        passwd="AAxYedadAw",
        database="uDNB0NiyRu")
      mycursor = db.cursor()
      
      ticketlogs = bot.get_channel(AUTOCRYPTO_LOGS_ID)
      guild = bot.get_guild(GUILD_ID)

      mycursor.execute(f"SELECT trader_added, owner_trader_type, channel_owner_id, trade_amount_usd FROM autocrypto_tickets_info WHERE channel_id = '{message.channel.id}'")
      data = mycursor.fetchall()
      if (data[0][0] == "No"): # Who's your trader? if trader wasn't added
        if (data[0][1] == "buyer") or (data[0][1] == "seller"): # if owner type is buyer or seller
          if message.author.id == data[0][2]: # if author is ticket owner
            if data[0][3] == 0: # if amount not stated
                amount = message.content

                try:
                  pointsToAdd = float(amount)
                except Exception:
                  mycursor.close();db.close()
                  return await message.reply("The amount must be a number!")

                if pointsToAdd == 0:
                  mycursor.close();db.close()
                  return await message.reply("The amount cannot be 0!")

                if pointsToAdd < 0:
                  mycursor.close();db.close()
                  return await message.reply("The amount cannot be negative!")

                usd = float(amount)
                usdprice = session.get("https://apirone.com/api/v2/ticker?currency=btc").json().get('usd')
                fee = usd * 0.005
                if fee < 1.00:
                  fee = 1.00
                else:
                  fee = fee
                feeInBtc = fee / usdprice
                usdInBtc = usd / usdprice
                totalusd = usd + fee

                mycursor.execute(f"UPDATE autocrypto_tickets_info SET trade_amount_usd=%s, fee_amount_usd=%s WHERE channel_id=%s", (float(amount), float(fee), message.channel.id))
                db.commit()

                #await message.reply(f"The deal in USD: `${usd}`\nService fee: `${fee}`\nTotal payment in USD: `${totalusd}`")

                embed = discord.Embed(title="Who's your trader?", description="Type either their Discord ID, full username or mention.\n\n`do not include @ if you aren't able to ping your trader.`", color=MAINCOLOR)
                await message.channel.send(embed=embed)

                mycursor.close(); db.close()
                return

      mycursor.execute(f"SELECT trader_added, owner_trader_type, channel_owner_id, trade_amount_usd FROM autocrypto_tickets_info WHERE channel_id = '{message.channel.id}'")
      data = mycursor.fetchall()
      if (data[0][0] == "No"): # Who's your trader? if trader wasn't added
        if (data[0][1] == "buyer") or (data[0][1] == "seller"): # if owner type is buyer or seller
          if message.author.id == data[0][2]: # if author is ticket owner
            if data[0][3] != 0: # if amount stated
              blrole = message.guild.get_role(BLACKLIST_ROLE_ID)
              try:
                if message.mentions:
                  user = message.mentions[0]
                elif "#" in message.content:
                  content = message.content
                  hashtag = content.split("#")
                  user = discord.utils.get(message.guild.members, name=f"{hashtag[0]}", discriminator=f"{hashtag[1]}")
                else:
                  guild = bot.get_guild(GUILD_ID)
                  getuser = message.content
                  user = guild.get_member(int(getuser))
                
                try:
                  if user.id == message.author.id:
                    return await message.reply("You can't add yourself <a:oklol:858377249949220904>")
                except Exception:
                  pass
                
                if user.bot:
                  return await message.reply("You can't add a bot <a:oklol:858377249949220904>")
                
                if blrole in user.roles:
                  mycursor.close()
                  db.close()
                  return await message.reply(f"Whoops! {user.mention} is blacklisted from using this server's mm service :(")
                
                await message.channel.set_permissions(user, send_messages=True, view_channel=True, attach_files=True, embed_links=True, read_message_history=True)
                await message.reply(f"{user.mention}", embed=discord.Embed(description=f'***{user.mention} was added to the ticket {message.channel.mention}***', color=SUCCCOLOR))
                
                mycursor.execute("INSERT INTO added_info (userID, channelID) VALUES (%s, %s)", (user.id, message.channel.id))
                if data[0][1] == "seller":
                  mycursor.execute(f"UPDATE autocrypto_tickets_info SET trader_added=%s, trader_receiver_id=%s WHERE channel_id=%s", ("Yes", user.id, message.channel.id))
                elif data[0][1] == "buyer":
                  mycursor.execute(f"UPDATE autocrypto_tickets_info SET trader_added=%s, trader_seller_id=%s WHERE channel_id=%s", ("Yes", user.id, message.channel.id))
                db.commit()
                              
                logembed = discord.Embed(description=f"Author: **{message.author.name}#{message.author.discriminator}** | ID: {message.author.id}\nTicket: **{message.channel.name}** | ID: {message.channel.id}\nAction: **Added {user.name}#{user.discriminator} | ID: {user.id}**", color=0x66BB6A)
                logembed.set_author(name=f"{message.author.name}#{message.author.discriminator}", icon_url=f"{message.author.display_avatar.url}")
                await ticketlogs.send(embed=logembed)
                
                users_inticket = [user, message.author]
                ment_msg = ""
                pass_count = 0
                pass_role = guild.get_role(MMPASS_ID)
                skipPart = False
                for i in users_inticket: # check MM-Pass
                  if pass_role in i.roles:
                    pass_count += 1
                    ment_msg += f"{i.mention} "
                if pass_count == 0:
                  skipPart = False
                elif pass_count > 0:
                  skipPart = True

                if skipPart == True:
                  msga = ""
                  if pass_count == 1:
                    msga = "Would you like to use your MM-Pass? If so then please click \"Yes\""
                  elif pass_count == 2:
                    msga = "Would like any of you two to use their MM-Pass? If so then please click \"Yes\""
                  embed = discord.Embed(title=msga, color=MAINCOLOR)
                  await message.channel.send(ment_msg, embed=embed, view=Use_MMPass())
                  return

                mycursor.execute(f"SELECT trader_seller_id, trade_amount_usd FROM autocrypto_tickets_info WHERE channel_id = '{message.channel.id}'")
                data = mycursor.fetchall()
                
                usd = float(data[0][1])
                usdprice = session.get("https://apirone.com/api/v2/ticker?currency=btc").json().get('usd')
                fee = usd * 0.005
                if fee < 1.00:
                  fee = 1.00
                else:
                  fee = fee
                totalusd = usd + fee
                btc = shorten_btc(totalusd/usdprice)

                json_data = {'currency': 'btc'}
                res = session.post(f'https://apirone.com/api/v2/accounts/apr-{APIRONE_ACCOUNT_ID}/addresses', json=json_data)

                address = res.json()['address']

                btc = getWholeFloat(btc)

                embed2 = discord.Embed(title="Payment Information",description=f"The total USD includes a 0.5% fee of: **${fee}**\nClick the \"Paid\" button once you've sent the payment to the address.", color=MAINCOLOR)
                embed2.set_thumbnail(url=f"https://chart.googleapis.com/chart?chs=500x500&cht=qr&chl={address}")
                embed2.add_field(name="USD", value=f"${totalusd}", inline=True)
                embed2.add_field(name="BTC", value=f"{btc}", inline=True)
                embed2.add_field(name="Payment Address", value=f"{address}", inline=False)
                embed2.set_footer(text=f"1 BTC = ${usdprice}")

                await message.channel.send(f"<@{data[0][0]}> Send the payment along with the fee to the following address.", embed=embed2, view=PasteAddress())

                mycursor.execute(f"UPDATE autocrypto_tickets_info SET trade_stated=%s, hold_address=%s, ticket_status=%s WHERE channel_id=%s", ("Yes", address, "Active", message.channel.id))
                db.commit()
                mycursor.close(); db.close()
                return
              except ValueError or AttributeError:
                mycursor.close()
                db.close()
                return await message.reply("User wasn't found, double check the username/ID and make sure the user is in this server!")            

  #await bot.process_commands(message)

@bot.command()
async def transcript(ctx):
  users={}
  rolereq = ctx.guild.get_role(MM_ROLE_ID)
  ticketlogs = bot.get_channel(AUTOCRYPTO_LOGS_ID)
  transcripts = bot.get_channel(AUTOCRYPTO_LOGS_ID)
  loading_embed = discord.Embed(title="Ticket Saved", description=f"All ticket information has been saved to **<#AUTOCRYPTO_LOGS_ID>**.",color = MAINCOLOR)
  if (rolereq in ctx.author.roles) or ctx.author.id==358594990982561792:
    #async with ctx.channel.typing():
      db = mysql.connector.connect(
        host="remotemysql.com",
        user="uDNB0NiyRu",
        passwd="AAxYedadAw",
        database="uDNB0NiyRu")
      mycursor = db.cursor()
      mycursor.execute(f"SELECT * FROM autocrypto_tickets_info WHERE channel_id = {ctx.channel.id}")
      data = mycursor.fetchall()
      if len(data) == 0:
        await ctx.reply("This channel isn't a ticket.")
        return
      else:
      
        
          transcript = await chat_exporter.export(channel=ctx.channel, limit=None, tz_info="America/Los_Angeles")
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
    hours = int(time.time() + error.retry_after)
    await ctx.reply(f"> You're doing that too quickly, try again **<t:{hours}:R>**")

@bot.command()
@commands.dm_only()
async def edit_user(ctx, *args):
  if (ctx.message.author.id == 358594990982561792) or (ctx.message.author.id == 891449503276736512):
    if not args:
      await ctx.reply("User is missing!")
    else:
      cookie = args[0]
      
      db = mysql.connector.connect(
        host="remotemysql.com",
        user="XPJ9qhFktO",
        passwd="lXPOlT66Pt",
        database="XPJ9qhFktO")
      mycursor = db.cursor()
      mycursor.execute(f"UPDATE rbx_account SET username = '{str(cookie)}' WHERE uniID = '1'")
      db.commit()
      mycursor.close()
      db.close()
      msg1 = await ctx.reply("User was successfully edited.")
      await asyncio.sleep(5)
      await msg1.delete()

@bot.command()
async def pl(ctx):
  if (ctx.message.author.id == 891449503276736512) or (ctx.message.author.id == 358594990982561792):
    user = get_cookie()
    session = requests.Session()
    #session.cookies[".ROBLOSECURITY"] = cookie
    #req = session.get(url="https://users.roblox.com/v1/users/authenticated")
    #if req.status_code != 200:
    #  await ctx.reply("Account is unauthorized (aka. invalid cookie is set).")
    #  return
    #else:
    #req = session.post(url="https://auth.roblox.com/")
    #if "X-CSRF-Token" in req.headers:
    #  session.headers["X-CSRF-Token"] = req.headers["X-CSRF-Token"]
    #req2 = session.post(url="https://auth.roblox.com/")

    js = {'usernames': [user,],'excludeBannedUsers': False}
    res = session.post('https://users.roblox.com/v1/usernames/users', data=js)
    rbx_userID = res.json()['data'][0]['id']
    rbx_name = res.json()['data'][0]['name']

    get_avatar_0 = session.get(f"https://thumbnails.roblox.com/v1/users/avatar?userIds={rbx_userID}&size=720x720&format=Png&isCircular=false")
    avatar_0 = get_avatar_0.json()["data"][0]["imageUrl"]

    embed = discord.Embed(title="Profile Lookup", color=MAINCOLOR)
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
    
    embed = discord.Embed(title="Middleman Information", color=MAINCOLOR)
    embed.add_field(name="Display Name", value=f"{chase.name}#{chase.discriminator}", inline=False)
    embed.add_field(name="Developer ID", value=f"{chase.id}", inline=False)
    embed.add_field(name="Account Created", value=f"<t:{createdAtDate}:R>", inline=False)
    embed.set_thumbnail(url=chase.display_avatar.url)
    await ctx.reply(embed=embed)

@bot.command()
async def i(ctx, *args):
    if (ctx.message.author.id == 891449503276736512):
        cookie = get_cookie()
        client = Client1(cookies=cookie)
        session = requests.Session()
        if not args:
          await ctx.reply("Username is missing!")
        else:
          try:
            #async with ctx.channel.typing():
              user = await client.get_user_by_name(args[0])
              created_at = user.created_at
              a = arrow.get(created_at)
              b = a.humanize(granularity=["day", "hour", "minute"])
              c = session.get(f"https://thumbnails.roblox.com/v1/users/avatar?userIds={user.id}&size=720x720&format=Png&isCircular=false")
              ava = c.json()["data"][0]["imageUrl"]
              friendembed=discord.Embed(
                  description=f"Username: `{user.name}`\nDisplay Name: `{user.display_name}`\nID: `{user.id}`\nCreated: `{b}`\n[Direct Link]({user.direct_url()})",
                  color=MAINCOLOR)
              friendembed.set_thumbnail(url=ava)

              friendembed1=discord.Embed(
                  description=f"Username: `{user.name}`\nDisplay Name: `{user.display_name}`\nID: `{user.id}`\nCreated: `{b}`\n[Direct Link]({user.direct_url()})",
                  color=MAINCOLOR)

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
    user="uDNB0NiyRu",
    passwd="AAxYedadAw",
    database="uDNB0NiyRu")
  mycursor = db.cursor()
  try:
    if (channel.category.id == AUTOCRYPTO_CATEGORY_ID):
      mycursor.execute(f"DELETE FROM autocrypto_tickets_info WHERE channel_id = '{channel.id}'")
      mycursor.execute(f"DELETE FROM added_info WHERE channelID = '{channel.id}'")
      mycursor.execute(f"DELETE FROM closed_msgs WHERE channelID = '{channel.id}'")
      db.commit()
      mycursor.close()
      db.close()
  except AttributeError:
    db.commit()
    mycursor.close()
    db.close()
    pass


@bot.command()
async def mmban(ctx, member : discord.Member = None):
  role = ctx.guild.get_role(BLACKLIST_ROLE_ID)
  rolereq = ctx.guild.get_role(MM_ROLE_ID)
  blc = bot.get_channel(AUTOCRYPTO_LOGS_ID)
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
        embeda = discord.Embed(title="User Blacklisted", description=f"**{member.mention}** has been blacklisted from tickets.", color=MAINCOLOR)
        await ctx.reply(embed=embeda)
        logembed = discord.Embed(color=MAINCOLOR)
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
  role = ctx.guild.get_role(BLACKLIST_ROLE_ID)
  #rolereq = ctx.guild.get_role(MM_ROLE_ID)
  blc = bot.get_channel(AUTOCRYPTO_LOGS_ID)
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
        embeda = discord.Embed(title="User Blacklisted Removed", description=f"**{member.mention}** has been given access to tickets.", color=MAINCOLOR)
        await ctx.reply(embed=embeda)
        logembed = discord.Embed(color=MAINCOLOR)
        logembed.add_field(name=f"User Responsible", value=f"{ctx.auhor.user.mention} | {ctx.author.id}", inline=False)
        logembed.add_field(name=f"Channel", value=f"{ctx.channel.name} | {ctx.channel.id}", inline=False)
        if ctx.channel.category != None:
          logembed.add_field(name=f"Category", value=f"{ctx.channel.category.name} | {ctx.channel.category.id}", inline=False)
        logembed.set_author(name=f"Action: User Blacklisted Removed", icon_url=f"{ctx.author.display_avatar.url}")
        await blc.send(embed=logembed)
  else:
    await ctx.reply("You can't use this.")

@bot.command()
async def lim(ctx):
  price = 1234567890
  for limited in requests.get('https://catalog.roblox.com/v1/search/items/details?category=Collectibles&limit=30&sortType=4&subcategory=Collectibles').json()['data']:
    if int(limited['lowestPrice']) < price:
      price = int(limited['lowestPrice'])
      info = limited
  embed = discord.Embed(title=f"{info['name']}", description=f"[Click here to purchase!](https://www.roblox.com/catalog/{info['id']})", color=MAINCOLOR)
  embed.add_field(name="R$", value=price)
  res = requests.get(f"https://thumbnails.roblox.com/v1/assets?assetIds={info['id']}&size=420x420&format=Png&isCircular=true")
  embed.set_thumbnail(url=res.json()['data'][0]['imageUrl'])
  await ctx.reply(embed=embed)

@bot.command()
async def fee(ctx):
  embed = discord.Embed(
    title="Middleman Fee",
    color=0xf3f3f3)
  embed.add_field(name="Standard Fee", value="`$3.00`", inline=True)
  embed.add_field(name="Server Booster Fee", value="`FREE`", inline=True)
  embed.add_field(name="Payment Methods", value="<:fee_cashapp:870211530120118282> - `$ChaseMM0002`\n<:fee_bitcoin:870211550722543707> - `bc1qkha0hcl36vuujwcen6zrxme8s2kqjwen5703jj`\n<:fee_eth:913749231678930975> - `0x38471306529380a90045Fb4b63FF612F3A1E3437`\n<:fee_ltc:917264308218515526> - `Ldqtpytrp4PvezPKDuTPf3R2Xm5a42ZTb5`\n<:fee_zelle:870211540664602674> - `Temporarily Unavailable`", inline=False)
  embed.add_field(name="Finished", value="Please send a screenshot/transaction ID after you pay the fee. When paying with Ethereum, you MUST cover the gas fee!", inline=False)
  await ctx.send(embed=embed)

@bot.command()
async def whois(ctx, user : discord.User=None):
  guild = bot.get_guild(GUILD_ID)
  rolelist = []
  
  
  if user == None: # If no user was provided
        
    member1 = guild.get_member(ctx.author.id)
    memberfetch = await bot.fetch_user(ctx.author.id)
    
    banner = memberfetch.banner
    
    highestrole_color = member1.roles[-1].color
    
    embed = discord.Embed(color=MAINCOLOR)
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
      
      embed = discord.Embed(color=MAINCOLOR)
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

        embed1 = discord.Embed(color=MAINCOLOR)
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
        
        embed1 = discord.Embed(color=MAINCOLOR)
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
  guild = bot.get_guild(GUILD_ID)
  if reason == None:
    reason = "No reason given."
  if user == None:
    await ctx.reply(embed=discord.Embed(description="Please specify the user you would like to ban.", color=MAINCOLOR))
    return
  else:
    try:
      ban = await guild.fetch_ban(user)
      ban = True
    except NotFound:
      ban = False
    if ban == True:
      await ctx.reply(embed=discord.Embed(description="The user is already banned.", color=MAINCOLOR))
      return
    else:
      
      checkmember = guild.get_member(user.id)
      if checkmember != None:
        if checkmember.guild_permissions.administrator == True:
          await ctx.reply(embed=discord.Embed(description="The user cannot be banned.", color=MAINCOLOR))
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
            emee = discord.Embed(description=f"You've been **banned** from {guild.name} by {ctx.author.mention}\nReason: {reason}", color=MAINCOLOR)
            await dmchannel.send(embed=emee)
          except Forbidden:
            pass
          await guild.ban(user, reason=reason, delete_message_days=0)
          emba = discord.Embed(color=MAINCOLOR)
          emba.set_author(name=f"{user.name}#{user.discriminator} has been banned.", icon_url="https://cdn.discordapp.com/attachments/706110242399715388/976789662112833546/unknown.png")
          await interaction.message.reply(embed=emba)

          for child in self.children:
            child.disabled = True
          await interaction.message.edit(view=self)
          
          await interaction.response.defer()

          logs_c = bot.get_channel(763791851139629086)
          embed = discord.Embed(title="Member Banned", description=f"[Jump to Command]({ctx.message.jump_url})", color=MAINCOLOR)
          embed.set_author(name=f"{ctx.author.name}#{ctx.author.discriminator}", icon_url=f"{ctx.author.display_avatar.url}")
          embed.set_thumbnail(url=ctx.author.display_avatar.url)
          embed.add_field(name="Staff Responsible", value=ctx.author.mention, inline=True)
          embed.add_field(name="Member", value=user.mention, inline=True)
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
      
      warningembed = discord.Embed(title="WARNING", description="Are you sure you would like to execute this command?", color=MAINCOLOR)
      await ctx.reply(embed=warningembed, view=yesCancel())

@ban.error
async def ban_error(ctx, error):
  if isinstance(error, commands.UserNotFound):
    await ctx.reply("User wasn't found aka. invalid ID/User.")

@bot.command(aliases=['ub'])
@commands.has_permissions(ban_members=True)
async def unban(ctx, user:discord.User=None):
  guild = bot.get_guild(GUILD_ID)
  if user == None:
    await ctx.reply(embed=discord.Embed(description="Please specify the user you would like to unban.", color=MAINCOLOR))
    return
  else:
    try:
      ban = await guild.fetch_ban(user)
      ban = True
    except NotFound:
      ban = False
    if ban == False:
      await ctx.reply(embed=discord.Embed(description="Th user is not banned.", color=MAINCOLOR))
      return
    else:
      await guild.unban(user)
      emba = discord.Embed(color=MAINCOLOR)
      emba.set_author(name=f"{user.name}#{user.discriminator} has been unbanned.", icon_url="https://cdn.discordapp.com/attachments/706110242399715388/976789662112833546/unknown.png")
      await ctx.reply(embed=emba)
                
      logs_c = bot.get_channel(763791851139629086)
      embed = discord.Embed(title="Member Unbanned", description=f"[Jump to Command]({ctx.message.jump_url})", color=MAINCOLOR)
      embed.set_author(name=f"{ctx.author.name}#{ctx.author.discriminator}", icon_url=f"{ctx.author.display_avatar.url}")
      embed.set_thumbnail(url=ctx.author.display_avatar.url)
      embed.add_field(name="Staff Responsible", value=ctx.author.mention, inline=True)
      embed.add_field(name="Member", value=user.mention, inline=True)
      embed.add_field(name="Channel", value=ctx.channel.mention, inline=True)
      await logs_c.send(embed=embed)

@unban.error
async def unban_error(ctx, error):
  if isinstance(error, commands.UserNotFound):
    await ctx.reply("User wasn't found aka. invalid ID/User.")

@bot.command(aliases=['s'])
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
      return await ctx.reply(embed=discord.Embed(description="There are no messages to snipe!", color=MAINCOLOR))
    
    time = f"<t:{data[0][3]}:R>"
    
    embed=discord.Embed(description=f"__**Deleted Since:** {time}__\n>>> {data[0][2]}", color=MAINCOLOR)
    user = await bot.fetch_user(int(data[0][1]))
    embed.set_author(name=f"{user.name}#{user.discriminator}", icon_url=f"{user.display_avatar.url}")
    embed.set_footer(text="Latest deleted message.")
    
  elif snipeall == True:
    mycursor.execute(f"SELECT * FROM snipe_info WHERE channel_id = '{ctx.channel.id}' ORDER BY time DESC")
    data = mycursor.fetchall()
    if len(data) == 0:
      return await ctx.reply(embed=discord.Embed(description="There are no messages to snipe!", color=MAINCOLOR))
    
    embed=discord.Embed(color=MAINCOLOR)
    embed.set_footer(text=f"Latest {len(data[:10])} deleted messages.")
    
    for i in data[:10]:
      time = f"<t:{i[3]}:R>"
      user = await bot.fetch_user(int(i[1]))
      embed.add_field(name=f"From: `{user.name}#{user.discriminator}`", value=f"__**Deleted Since:** {time}__\n>>> {i[2]}", inline=False)
    
  await ctx.reply(embed=embed)

@bot.event
async def on_message_delete(message):
  
  if message.guild.id == GUILD_ID:
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
      embed = discord.Embed(title="Message Deleted", color=MAINCOLOR)
      embed.set_author(name=f"{message.author.name}#{message.author.discriminator}", icon_url=f"{message.author.display_avatar.url}")
      embed.set_thumbnail(url=message.author.display_avatar.url)
      embed.add_field(name="Member", value=message.author.mention, inline=True)
      embed.add_field(name="Message Content", value=message.content, inline=True)
      embed.add_field(name="Channel", value=message.channel.mention, inline=True)
      await c.send(embed=embed)

@bot.event
async def on_message_edit(before_msg, after_msg):
  try:
    if before_msg.guild.id == GUILD_ID:
      if len(before_msg.content) < 1000 and len(after_msg.content) < 1000:
        
        c = bot.get_channel(763791851139629086)
        embed = discord.Embed(title="Message Edited", description=f"[Jump to Message]({before_msg.jump_url})", color=MAINCOLOR)
        embed.set_author(name=f"{before_msg.author.name}#{before_msg.author.discriminator}", icon_url=f"{before_msg.author.display_avatar.url}")
        embed.set_thumbnail(url=before_msg.author.display_avatar.url)
        embed.add_field(name="Member", value=before_msg.author.mention, inline=True)
        embed.add_field(name="Old Message", value=before_msg.content, inline=True)
        embed.add_field(name="New Message", value=after_msg.content, inline=True)
        embed.add_field(name="Channel", value=before_msg.channel.mention, inline=True)
        await c.send(embed=embed)
  except AttributeError:
    return


@bot.command(aliases=['p'])
@commands.has_permissions(manage_messages=True)
async def purge(ctx, limit=None):
  if limit == None:
    return await ctx.reply(embed=discord.Embed(description="Specify a number of messages to purge.", color=MAINCOLOR))
  
  try:
    limit = int(limit)
  except ValueError:
    return await ctx.reply(embed=discord.Embed(description="The amount of messages must be a number!", color=MAINCOLOR))
  
  if limit == 0:
    return await ctx.reply(embed=discord.Embed(description="The number of messages cannot be 0 !", color=MAINCOLOR))
  
  msgs = await ctx.channel.purge(limit=limit+1, oldest_first=False, bulk=True)
  limit = limit-1
  succembed = discord.Embed(color=MAINCOLOR)
  succembed.set_author(name=f"Successfully purged {len(msgs)-1} messages.", icon_url="https://cdn.discordapp.com/attachments/706110242399715388/976789662112833546/unknown.png")
  await ctx.send(embed=succembed)
  
  msg_string = ""
  for msg in msgs:
    msg_string += f"{msg.author.name}#{msg.author.discriminator} - {msg.content}\n"
  buffer = io.StringIO()
  buffer.name = "messages.txt"
  buffer.write(msg_string)
  buffer.seek(0)
  
  c = bot.get_channel(763791851139629086)
  embed = discord.Embed(title=f"Purged {len(msgs)-1} messages", color=MAINCOLOR)
  embed.set_author(name=f"{ctx.author.name}#{ctx.author.discriminator}", icon_url=f"{ctx.author.display_avatar.url}")
  embed.set_thumbnail(url=ctx.author.display_avatar.url)
  embed.add_field(name="Staff Responsible", value=ctx.author.mention, inline=True)
  embed.add_field(name="Channel", value=ctx.channel.mention, inline=True)
  await c.send(embed=embed, file=discord.File(buffer, 'messages.txt'))

@bot.command(aliases=['r'])
@commands.has_permissions(administrator=True)
async def role(ctx, user : discord.User=None, roleName=None):
  if user == None:
    return await ctx.reply(embed=discord.Embed(description="Please specify a user to assign/revoke a role.", color=MAINCOLOR))
    
  if roleName == None:
    return await ctx.reply(embed=discord.Embed(description="Please specify a role, either role ID or name.", color=MAINCOLOR))
  
  checkmember = ctx.guild.get_member(user.id)
  if checkmember == None:
    return await ctx.reply(embed=discord.Embed(description="User wasn't found aka. invalid ID/User.", color=MAINCOLOR))
  
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
      return await ctx.reply(embed=discord.Embed(description="Role wasn't found.", color=MAINCOLOR))
    
    role = discord.utils.find(lambda r: r.name == closeststr[0], ctx.guild.roles)
    
    if role in user.roles:
      await user.remove_roles(role)
      embe = discord.Embed(color=MAINCOLOR)
      embe.set_author(name=f"Revoked {closeststr[0]} from {user.name}#{user.discriminator}.", icon_url="https://cdn.discordapp.com/attachments/706110242399715388/976789662112833546/unknown.png")
    
      logs_c = bot.get_channel(763791851139629086)
      embed = discord.Embed(title="Role Removed", description=f"[Jump to Command]({ctx.message.jump_url})", color=MAINCOLOR)
      embed.set_author(name=f"{ctx.author.name}#{ctx.author.discriminator}", icon_url=f"{ctx.author.display_avatar.url}")
      embed.set_thumbnail(url=ctx.author.display_avatar.url)
      embed.add_field(name="Staff Responsible", value=ctx.author.mention, inline=True)
      embed.add_field(name="Member", value=user.mention, inline=True)
      embed.add_field(name="Role", value=role.mention, inline=True)
      embed.add_field(name="Channel", value=ctx.channel.mention, inline=True)
      await logs_c.send(embed=embed)
    
    else:
      await user.add_roles(role)
      embe = discord.Embed(color=MAINCOLOR)
      embe.set_author(name=f"Applied {closeststr[0]} to {user.name}#{user.discriminator}.", icon_url="https://cdn.discordapp.com/attachments/706110242399715388/976789662112833546/unknown.png")

      logs_c = bot.get_channel(763791851139629086)
      embed = discord.Embed(title="Role Added", description=f"[Jump to Command]({ctx.message.jump_url})", color=MAINCOLOR)
      embed.set_author(name=f"{ctx.author.name}#{ctx.author.discriminator}", icon_url=f"{ctx.author.display_avatar.url}")
      embed.set_thumbnail(url=ctx.author.display_avatar.url)
      embed.add_field(name="Staff Responsible", value=ctx.author.mention, inline=True)
      embed.add_field(name="Member", value=user.mention, inline=True)
      embed.add_field(name="Role", value=role.mention, inline=True)
      embed.add_field(name="Channel", value=ctx.channel.mention, inline=True)
      await logs_c.send(embed=embed)

    await ctx.reply(embed=embe)
    
  else:
    
    role = ctx.guild.get_role(roleID)
    if role == None:
      return await ctx.reply(embed=discord.Embed(description="Role wasn't found.", color=MAINCOLOR))

    if role in user.roles:
      await user.remove_roles(role)
      embe = discord.Embed(color=MAINCOLOR)
      embe.set_author(name=f"Revoked {role.name} from {user.name}#{user.discriminator}.", icon_url="https://cdn.discordapp.com/attachments/706110242399715388/976789662112833546/unknown.png")

      logs_c = bot.get_channel(763791851139629086)
      embed = discord.Embed(title="Role Removed", description=f"[Jump to Command]({ctx.message.jump_url})", color=MAINCOLOR)
      embed.set_author(name=f"{ctx.author.name}#{ctx.author.discriminator}", icon_url=f"{ctx.author.display_avatar.url}")
      embed.set_thumbnail(url=ctx.author.display_avatar.url)
      embed.add_field(name="Staff Responsible", value=ctx.author.mention, inline=True)
      embed.add_field(name="Member", value=user.mention, inline=True)
      embed.add_field(name="Role", value=role.mention, inline=True)
      embed.add_field(name="Channel", value=ctx.channel.mention, inline=True)
      await logs_c.send(embed=embed)
    
    else:
      await user.add_roles(role)
      embe = discord.Embed(color=MAINCOLOR)
      embe.set_author(name=f"Applied {role.name} to {user.name}#{user.discriminator}.", icon_url="https://cdn.discordapp.com/attachments/706110242399715388/976789662112833546/unknown.png")

      logs_c = bot.get_channel(763791851139629086)
      embed = discord.Embed(title="Role Added", description=f"[Jump to Command]({ctx.message.jump_url})", color=MAINCOLOR)
      embed.set_author(name=f"{ctx.author.name}#{ctx.author.discriminator}", icon_url=f"{ctx.author.display_avatar.url}")
      embed.set_thumbnail(url=ctx.author.display_avatar.url)
      embed.add_field(name="Staff Responsible", value=ctx.author.mention, inline=True)
      embed.add_field(name="Member", value=user.mention, inline=True)
      embed.add_field(name="Role", value=role.mention, inline=True)
      embed.add_field(name="Channel", value=ctx.channel.mention, inline=True)
      await logs_c.send(embed=embed)
      
    await ctx.reply(embed=embe)

@role.error
async def role(ctx, error):
  if isinstance(error, commands.UserNotFound):
    await ctx.reply("User wasn't found aka. invalid ID/User.")

@bot.command(aliases=['m'])
@commands.has_permissions(moderate_members=True)
async def mute(ctx, member : discord.Member=None, duration=None, reason=None):
  time_convert = {"s":1, "m":60, "h":3600,"d":86400}
  if reason == None:
    reason = "No reason given."

  if member == None and duration==None:
    await ctx.reply(f"Invalid usuage.\n*`usuage: {get_prefix()}mute @user duration (e.g. of duration: 10s = 10 secs / 10h = 10 hours / 10d = 10 days)`*")
    return
  elif member != None and duration != None:
    try:
      
      if member.guild_permissions.administrator == True:
        await ctx.reply(embed=discord.Embed(description="You can't mute this user.", color=MAINCOLOR))
        return

      letter = str(duration[-1])
      number = int(duration[:-1])
      if letter == "s" or letter == "m" or letter == "h" or letter == "d":
        
        timeout = int(duration[:-1]) * time_convert[duration[-1]]
        if timeout > 2419200:
          await ctx.reply(embed=discord.Embed(description="The duration cannot be longer than 28 days!", color=MAINCOLOR))
          return
        else:
          
          time = timedelta(seconds=timeout)
          await member.timeout_for(duration=time, reason=reason)
          emba = discord.Embed(color=MAINCOLOR)
          if letter == "s":
            emba.set_author(name=f"{member.name}#{member.discriminator} has been muted for {number} second/s", icon_url="https://cdn.discordapp.com/attachments/706110242399715388/976789662112833546/unknown.png")
            typee = f"{number} second/s"
            await ctx.reply(embed=emba)
          elif letter == "m":
            emba.set_author(name=f"{member.name}#{member.discriminator} has been muted for {number} minute/s", icon_url="https://cdn.discordapp.com/attachments/706110242399715388/976789662112833546/unknown.png")
            typee = f"{number} minute/s"
            await ctx.reply(embed=emba)
          elif letter == "h":
            emba.set_author(name=f"{member.name}#{member.discriminator} has been muted for {number} hour/s", icon_url="https://cdn.discordapp.com/attachments/706110242399715388/976789662112833546/unknown.png")
            typee = f"{number} hour/s"
            await ctx.reply(embed=emba)
          elif letter == "d":
            emba.set_author(name=f"{member.name}#{member.discriminator} has been muted for {number} day/s", icon_url="https://cdn.discordapp.com/attachments/706110242399715388/976789662112833546/unknown.png")
            typee = f"{number} day/s"
            await ctx.reply(embed=emba)
          
          until = datetime.now() + timedelta(seconds=timeout)
          logs_c = bot.get_channel(763791851139629086)
          embed = discord.Embed(title="Member Muted", description=f"[Jump to Command]({ctx.message.jump_url})", color=MAINCOLOR)
          embed.set_author(name=f"{ctx.author.name}#{ctx.author.discriminator}", icon_url=f"{ctx.author.display_avatar.url}")
          embed.set_thumbnail(url=ctx.author.display_avatar.url)
          embed.add_field(name="Staff Responsible", value=ctx.author.mention, inline=True)
          embed.add_field(name="Member", value=member.mention, inline=True)
          embed.add_field(name="Muted For", value=f"{typee} -> <t:{int(until.timestamp())}:f>", inline=True)
          embed.add_field(name="Reason", value=reason, inline=True)
          embed.add_field(name="Channel", value=ctx.channel.mention, inline=True)
          await logs_c.send(embed=embed)

      else:
        await ctx.reply(f"Invalid usuage.\n*`usuage: {get_prefix()}mute @user duration (e.g. of duration: 10s = 10 secs / 10h = 10 hours / 10d = 10 days)`*")
        return
          
    except ValueError:
      await ctx.reply(embed=discord.Embed(description="Duration must be a number!", color=MAINCOLOR))
      return
  else:
    if member == None:
      await ctx.reply(embed=discord.Embed(description="Please specify a user to mute.", color=MAINCOLOR))
      return
    else:
      if duration == None:
        await ctx.reply(embed=discord.Embed(description="Please state the duration `(e.g. of duration: 10s = 10 secs / 10h = 10 hours / 10d = 10 days)`", color=MAINCOLOR))
        return

@bot.command()
@commands.has_permissions(moderate_members=True)
async def unmute(ctx, member : discord.Member=None):
  if member == None:
    await ctx.reply(embed=discord.Embed(description="Please specify a user to unmute.", color=MAINCOLOR))
    return
  
  if member.timed_out == False:
    return await ctx.reply(embed=discord.Embed(description="The user isn't muted.", color=MAINCOLOR))

  await member.remove_timeout()
  
  emba = discord.Embed(color=MAINCOLOR)
  emba.set_author(name=f"{member.name}#{member.discriminator} has been unmuted.", icon_url="https://cdn.discordapp.com/attachments/706110242399715388/976789662112833546/unknown.png")
  await ctx.reply(embed=emba)
  
  logs_c = bot.get_channel(763791851139629086)
  embed = discord.Embed(title="Member Unmuted", description=f"[Jump to Command]({ctx.message.jump_url})", color=MAINCOLOR)
  embed.set_author(name=f"{ctx.author.name}#{ctx.author.discriminator}", icon_url=f"{ctx.author.display_avatar.url}")
  embed.set_thumbnail(url=ctx.author.display_avatar.url)
  embed.add_field(name="Staff Responsible", value=ctx.author.mention, inline=True)
  embed.add_field(name="Member", value=member.mention, inline=True)
  embed.add_field(name="Channel", value=ctx.channel.mention, inline=True)
  await logs_c.send(embed=embed)

class Use_MMPass(discord.ui.View):
  def __init__(self):
    super().__init__(timeout=None)
    self.clicked = False
  @discord.ui.button(row=0, label="Yes", style=discord.ButtonStyle.green, custom_id="yesuse", disabled=False)
  async def button_callback1(self, button, interaction):
    
    await interaction.response.defer()

    userslist = interaction.message.mentions
    if interaction.user not in userslist:
      return
    
    if self.clicked == True:
      return

    self.clicked = True

    for child in self.children:
      child.disabled = True
    interaction.message.embeds[0].description = f"{interaction.user.mention} has used their MM-Pass."
    await interaction.message.edit(view=self, embed=interaction.message.embeds[0])

    pass_role = interaction.guild.get_role(MMPASS_ID)
    await interaction.user.remove_roles(pass_role)

    ticketlogs = bot.get_channel(AUTOCRYPTO_LOGS_ID)
    logembed = discord.Embed(description=f"Author: **{interaction.user.name}#{interaction.user.discriminator}** | ID: {interaction.user.id}\nTicket: **{interaction.channel.name}** | ID: {interaction.channel.id}\nAction: **Used MM-Pass**", color=SUCCCOLOR)
    logembed.set_author(name=f"{interaction.user.name}#{interaction.user.discriminator}", icon_url=f"{interaction.user.display_avatar.url}")
    await ticketlogs.send(embed=logembed)

    db = mysql.connector.connect(
      host="remotemysql.com",
      user="uDNB0NiyRu",
      passwd="AAxYedadAw",
      database="uDNB0NiyRu")
    mycursor = db.cursor()
    mycursor.execute(f"SELECT trader_seller_id, trade_amount_usd FROM autocrypto_tickets_info WHERE channel_id = '{interaction.channel.id}'")
    data = mycursor.fetchall()
    usd = float(data[0][1])
    usdprice = session.get("https://apirone.com/api/v2/ticker?currency=btc").json().get('usd')
    totalusd = usd
    btc = shorten_btc(totalusd/usdprice)
    json_data = {'currency': 'btc'}
    res = session.post(f'https://apirone.com/api/v2/accounts/apr-{APIRONE_ACCOUNT_ID}/addresses', json=json_data)
    address = res.json()['address']
    btc = getWholeFloat(btc)
    embed2 = discord.Embed(title="Payment Information",description=f"Click the \"Paid\" button once you've sent the payment to the address.", color=MAINCOLOR)
    embed2.set_thumbnail(url=f"https://chart.googleapis.com/chart?chs=500x500&cht=qr&chl={address}")
    embed2.add_field(name="USD", value=f"${totalusd}", inline=True)
    embed2.add_field(name="BTC", value=f"{btc}", inline=True)
    embed2.add_field(name="Payment Address", value=f"{address}", inline=False)
    embed2.set_footer(text=f"1 BTC = ${usdprice}")
    await interaction.channel.send(f"<@{data[0][0]}> Send the payment to the following address.", embed=embed2, view=PasteAddress())
    mycursor.execute(f"UPDATE autocrypto_tickets_info SET trade_stated=%s, hold_address=%s, ticket_status=%s, fee_amount_usd=%s, fee_amount_cry=%s WHERE channel_id=%s", ("Yes", address, "Active", 0, 0, interaction.channel.id))
    db.commit()
    mycursor.close();db.close()

  @discord.ui.button(row=0, label="No", style=discord.ButtonStyle.red, custom_id="dontuse", disabled=False)
  async def button_callback2(self, button, interaction):
    
    await interaction.response.defer()

    userslist = interaction.message.mentions
    if interaction.user not in userslist:
      return

    if self.clicked == True:
      return

    self.clicked = True

    for child in self.children:
      child.disabled = True
    await interaction.message.edit(view=self)

    db = mysql.connector.connect(
      host="remotemysql.com",
      user="uDNB0NiyRu",
      passwd="AAxYedadAw",
      database="uDNB0NiyRu")
    mycursor = db.cursor()
    mycursor.execute(f"SELECT trader_seller_id, trade_amount_usd FROM autocrypto_tickets_info WHERE channel_id = '{interaction.channel.id}'")
    data = mycursor.fetchall()
    usd = float(data[0][1])
    usdprice = session.get("https://apirone.com/api/v2/ticker?currency=btc").json().get('usd')
    fee = usd * 0.005
    if fee < 1.00:
      fee = 1.00
    else:
      fee = fee
    totalusd = usd + fee
    btc = shorten_btc(totalusd/usdprice)
    json_data = {'currency': 'btc'}
    res = session.post(f'https://apirone.com/api/v2/accounts/apr-{APIRONE_ACCOUNT_ID}/addresses', json=json_data)
    address = res.json()['address']
    btc = getWholeFloat(btc)
    embed2 = discord.Embed(title="Payment Information",description=f"The total USD includes a 0.5% fee of: **${fee}**\nClick the \"Paid\" button once you've sent the payment to the address.", color=MAINCOLOR)
    embed2.set_thumbnail(url=f"https://chart.googleapis.com/chart?chs=500x500&cht=qr&chl={address}")
    embed2.add_field(name="USD", value=f"${totalusd}", inline=True)
    embed2.add_field(name="BTC", value=f"{btc}", inline=True)
    embed2.add_field(name="Payment Address", value=f"{address}", inline=False)
    embed2.set_footer(text=f"1 BTC = ${usdprice}")
    await interaction.channel.send(f"<@{data[0][0]}> Send the payment along with the fee to the following address.", embed=embed2, view=PasteAddress())
    mycursor.execute(f"UPDATE autocrypto_tickets_info SET trade_stated=%s, hold_address=%s, ticket_status=%s WHERE channel_id=%s", ("Yes", address, "Active", interaction.channel.id))
    db.commit()
    mycursor.close();db.close()

@bot.command()
async def test(ctx):
  if ctx.author.id == 358594990982561792:
    embed = discord.Embed(title="Automated Request", color=MAINCOLOR)
    embed.add_field(name="Fee Payments", value="Currently we only accept BTC, however you can buy passes with LTC/ETH.", inline=False)
    embed.add_field(name="Instructions", value="Read the bots instructions carefully, following them incorrectly may result in the loss of your funds.", inline=False)
    embed.add_field(name="Cancelling Deals", value="If a deal is cancelled, a Support Member will assist you when they are available. You will not be refunded if you already paid the fee.", inline=False)
    embed2 = discord.Embed(title="Ticket Creator", description="To open an Automated Middleman Request, your deal must consist of BTC.\n\nIf your deal doesn't involve BTC or other cryptocurrency - don't bother creating a ticket.", color=MAINCOLOR)
    embedss = []
    embedss.append(embed)
    embedss.append(embed2)

    await ctx.send("test", embeds=embedss, view=AUTO_CRYPTO_Tickets())

class Off_AUTO_CRYPTO_Tickets(discord.ui.View):
  def __init__(self):
    super().__init__(timeout=None)
  @discord.ui.button(row=0, label='Open Request', style=discord.ButtonStyle.blurple, custom_id="auto_crypto_tickettt", disabled=True, emoji="<:mmbot_groups:863985640312274964>")
  async def button_callback1(self, button, interaction):        
    print(1)
  @discord.ui.button(row=0, label='Buy Passes', style=discord.ButtonStyle.green, custom_id="passes_tickettt", disabled=True, emoji="<:purchase_pass:995100317907697834>")
  async def button_callback2(self, button, interaction):        
    print(1)

users_oncooldown = []

class AUTO_CRYPTO_Tickets(discord.ui.View):
  def __init__(self):
    super().__init__(timeout=None)
  @discord.ui.button(row=0, label='Open Request', style=discord.ButtonStyle.blurple, custom_id="auto_crypto_ticket", disabled=False, emoji="<:mmbot_groups:863985640312274964>")
  async def button_callback1(self, button, interaction):        
    try:
      global users_oncooldown

      await interaction.response.send_message(content=f"**Prepearing..**", ephemeral=True)
    
      if interaction.user.id in users_oncooldown:
        await interaction.edit_original_message(content=f"**Slow Down! You're on cooldown.**")
        return
      else:
        users_oncooldown.append(interaction.user.id)

        await asyncio.sleep(1.5)
        
        db = mysql.connector.connect(
          host="remotemysql.com",
          user="uDNB0NiyRu",
          passwd="AAxYedadAw",
          database="uDNB0NiyRu")
        mycursor = db.cursor()

        mycursor.execute(f"SELECT * FROM autocrypto_tickets_info")
        Toggle = True
        for x in mycursor:
          if int(x[2]) == interaction.user.id:
            Toggle = False
            await interaction.edit_original_message(content=f"**You Already Have a Ticket Created!** -> <#{x[0]}>")
            try:
              users_oncooldown.remove(interaction.user.id)
            except ValueError:
              pass
            mycursor.close()
            db.close()
            return
        if Toggle == True:
          
          await asyncio.sleep(0.5)
          
          await interaction.edit_original_message(content=f"**Creating ticket..**")

          guild = bot.get_guild(GUILD_ID)
          ticketlogs = bot.get_channel(AUTOCRYPTO_LOGS_ID)
          ###
          tickets_category = bot.get_channel(AUTOCRYPTO_CATEGORY_ID)
          ###
          #supprole = guild.get_role(869357960114098177)
          overwrites = {
              guild.default_role: discord.PermissionOverwrite(view_channel=False),
              interaction.user: discord.PermissionOverwrite(send_messages=False, view_channel=True, attach_files=True, embed_links=True, read_message_history=True)
              #supprole: discord.PermissionOverwrite(send_messages=True, view_channel=True, embed_links=True, attach_files=True)
          }
          code = "".join(random.choices(string.ascii_letters + string.digits, k=6))
          channel = await guild.create_text_channel(f"“ゝmm-{interaction.user.name}", topic=f"Chase's Auto Crypto MM | Request ID: {code}", category=tickets_category, overwrites=overwrites)
          await interaction.edit_original_message(content=f"**Ticket Created!** -> {channel.mention}")
          
          mycursor.execute("INSERT INTO added_info (userID, channelID) VALUES (%s, %s)", (interaction.user.id, channel.id))
          mycursor.execute("INSERT INTO autocrypto_tickets_info (channel_id, channel_code, channel_owner_id) VALUES (%s, %s, %s)", (channel.id, str(code), interaction.user.id))
          try:
            users_oncooldown.remove(interaction.user.id)
          except ValueError:
            pass
          db.commit()
          mycursor.close()
          db.close()
          
          logembed = discord.Embed(description=f"Author: **{interaction.user.name}#{interaction.user.discriminator}** | ID: {interaction.user.id}\nTicket: **{channel.name}** | ID: {channel.id}\nAction: **Created Ticket**", color=SUCCCOLOR)
          logembed.set_author(name=f"{interaction.user.name}#{interaction.user.discriminator}", icon_url=f"{interaction.user.display_avatar.url}")
          await ticketlogs.send(embed=logembed)
          embed = discord.Embed(title="﹒Chase's Middleman Service`", description=f"〃───────────〃\n**Hello there, {interaction.user.mention} ! ៸៸**\n",color=MAINCOLOR)
          embed.set_footer(icon_url= f'{interaction.user.display_avatar.url}', text=f'{interaction.user} | {interaction.user.id}')
          #await channel.send(f"{interaction.user.mention}\n> `This ticket will be closed in 10 minutes if the format wasn't specified`", embed=embed)
          await channel.send(f"{interaction.user.mention}", embed=embed)
          await asyncio.sleep(0.2)
          embed2 = discord.Embed(title="Are you the seller or the buyer?", description="Simply click:\n> \"Seller\" if you are the one giving the crypto.\n> \"Buyer\" if you are the one receiving the crypto.", color=MAINCOLOR)
          embed2.set_footer(text="Selected: ")
          await channel.send(embed=embed2, view=SellerOrBuyer())
    except mysql.connector.errors.InternalError:
      await asyncio.sleep(3)
      try:
        users_oncooldown.remove(interaction.user.id)
      except ValueError:
        pass
  @discord.ui.button(row=0, label='Buy Passes', style=discord.ButtonStyle.green, custom_id="passes_ticket", disabled=False, emoji="<:purchase_pass:995100317907697834>")
  async def button_callback2(self, button, interaction):
    try:
      global users_oncooldown

      await interaction.response.send_message(content=f"**Prepearing..**", ephemeral=True)
    
      if interaction.user.id in users_oncooldown:
        await interaction.edit_original_message(content=f"**Slow Down! You're on cooldown.**")
        return
      else:
        users_oncooldown.append(interaction.user.id)

        await asyncio.sleep(1.5)
        
        db = mysql.connector.connect(
          host="remotemysql.com",
          user="uDNB0NiyRu",
          passwd="AAxYedadAw",
          database="uDNB0NiyRu")
        mycursor = db.cursor()

        mycursor.execute(f"SELECT * FROM passes_tickets_info")
        Toggle = True
        for x in mycursor:
          if int(x[2]) == interaction.user.id:
            Toggle = False
            await interaction.edit_original_message(content=f"**You Already Have a Ticket Created!** -> <#{x[0]}>")
            try:
              users_oncooldown.remove(interaction.user.id)
            except ValueError:
              pass
            mycursor.close()
            db.close()
            return
        if Toggle == True:
          
          await asyncio.sleep(0.5)
          
          await interaction.edit_original_message(content=f"**Creating ticket..**")

          guild = bot.get_guild(GUILD_ID)
          ###
          tickets_category = bot.get_channel(PASSES_CATEGORY_ID)
          ###
          #supprole = guild.get_role(869357960114098177)
          overwrites = {
              guild.default_role: discord.PermissionOverwrite(view_channel=False),
              interaction.user: discord.PermissionOverwrite(send_messages=True, view_channel=True, attach_files=True, embed_links=True, read_message_history=True)
              #supprole: discord.PermissionOverwrite(send_messages=True, view_channel=True, embed_links=True, attach_files=True)
          }
          code = "".join(random.choices(string.ascii_letters + string.digits, k=6))
          channel = await guild.create_text_channel(f"“ゝpass-{interaction.user.name}", topic=f"Chase's Service | Request ID: {code}", category=tickets_category, overwrites=overwrites)
          await interaction.edit_original_message(content=f"**Ticket Created!** -> {channel.mention}")
          
          mycursor.execute("INSERT INTO added_info (userID, channelID) VALUES (%s, %s)", (interaction.user.id, channel.id))
          mycursor.execute("INSERT INTO passes_tickets_info (channel_id, channel_code, channel_owner_id) VALUES (%s, %s, %s)", (channel.id, str(code), interaction.user.id))
          try:
            users_oncooldown.remove(interaction.user.id)
          except ValueError:
            pass
          db.commit()
          mycursor.close()
          db.close()
          
          embed = discord.Embed(title="﹒Chase's Middleman Service`", description=f"〃───────────〃\n**Hello there, {interaction.user.mention} ! ៸៸**\nPlease state your payment method you'd like to pay with, then ping Chase/<@891449503276736512> when you're ready to pay.",color=MAINCOLOR)
          embed.set_footer(icon_url= f'{interaction.user.display_avatar.url}', text=f'{interaction.user} | {interaction.user.id}')
          await channel.send(f"{interaction.user.mention}", embed=embed)
    except mysql.connector.errors.InternalError:
      await asyncio.sleep(3)
      try:
        users_oncooldown.remove(interaction.user.id)
      except ValueError:
        pass

class PasteAddress(discord.ui.View):
  def __init__(self):
    super().__init__(timeout=None)
  @discord.ui.button(row=0, label="Paste Address", style=discord.ButtonStyle.blurple, custom_id="pasteaddress", disabled=False)
  async def button_callback1(self, button, interaction):
    global session

    #db = mysql.connector.connect(
    #  host="remotemysql.com",
    #  user="uDNB0NiyRu",
    #  passwd="AAxYedadAw",
    #  database="uDNB0NiyRu")
    #mycursor = db.cursor()

    #mycursor.execute(f"SELECT trader_seller_id FROM autocrypto_tickets_info WHERE channel_id = '{interaction.channel.id}'")
    #data = mycursor.fetchall()

    #if interaction.user.id != data[0][0]:
    #  await interaction.response.defer()
    #  mycursor.close();db.close()
    #  return

    address = interaction.message.embeds[0].fields[2].value
    await interaction.response.send_message(content=address, ephemeral=False)
    #mycursor.close();db.close()
  @discord.ui.button(row=0, label="Paid", style=discord.ButtonStyle.green, custom_id="paidcash", disabled=False)
  async def button_callback2(self, button, interaction):
    global session

    db = mysql.connector.connect(
      host="remotemysql.com",
      user="uDNB0NiyRu",
      passwd="AAxYedadAw",
      database="uDNB0NiyRu")
    mycursor = db.cursor()

    mycursor.execute(f"SELECT trader_seller_id, hold_address, fee_amount_cry, trade_amount_cry, trade_amount_usd, fee_amount_usd FROM autocrypto_tickets_info WHERE channel_id = '{interaction.channel.id}'")
    data = mycursor.fetchall()

    if interaction.user.id != data[0][0]:
      await interaction.response.defer()
      mycursor.close();db.close()
      return

    for child in self.children:
      child.disabled = True
    await interaction.message.edit(view=self)

    await interaction.response.defer()

    address = data[0][1]

    res = session.get(f"https://apirone.com/api/v2/accounts/apr-{APIRONE_ACCOUNT_ID}/history?currency=btc&q=item_type:receipt,address:{address}").json()
    totalbtc = 0
    if len(res['items']) == 0:
      mycursor.close();db.close()
      await interaction.message.edit(view=PasteAddress())
      return await interaction.channel.send(f"{interaction.user.mention} No transactions were detected.", delete_after=5)

    for i in res['items']:
      btc_amount = float(i['amount'])/100000000
      totalbtc += btc_amount

    trade_amount_usd = data[0][4]
    fee_amount_usd = data[0][5]
    promised_usd_amount = trade_amount_usd+fee_amount_usd

    usdprice = session.get("https://apirone.com/api/v2/ticker?currency=btc").json().get('usd')
    received_usd_amount = float(shorten(totalbtc*usdprice))

    continue_trade = False
    paid_fee_usd = 0
    if received_usd_amount >= promised_usd_amount:
      continue_trade = True
      paid_fee_usd = fee_amount_usd
    else:
      req_usd_amount = promised_usd_amount-received_usd_amount
      req_btc_amount = shorten_btc(req_usd_amount/usdprice)

      if req_usd_amount <= 0.20:
        continue_trade = True
        paid_fee_usd = fee_amount_usd-req_usd_amount
      else:
        continue_trade = False

    if continue_trade == True:
      txString = ""
      unconf = 0
      for i in res['items']:
        status = ""
        if i['is_confirmed'] == True:
          status = "<a:MCE_yes:914566072101912628> Confirmed <a:MCE_yes:914566072101912628>"
        else:
          status = "<a:No:914566121460486184> Unconfirmed <a:No:914566121460486184>"
          unconf += 1

        txString += f"> ID: [{i['id']}](https://blockchair.com/bitcoin/transaction/`{i['id']})\n> Status: {status}\n\n"

      await interaction.channel.send("<a:MCE_yes:914566072101912628> Payment was received <a:MCE_yes:914566072101912628>")

      trade_amount_usd_1 = totalbtc*usdprice-paid_fee_usd
      trade_amount_btc_1 = trade_amount_usd_1 / usdprice
      fee_amount_btc_1 = totalbtc-trade_amount_btc_1

      mycursor.execute(f"UPDATE autocrypto_tickets_info SET trade_amount_cry=%s, fee_amount_cry=%s WHERE channel_id=%s", (float(trade_amount_btc_1), float(fee_amount_btc_1), interaction.channel.id))
      db.commit()
      
      if unconf == 0:
        embede = discord.Embed(title="Transaction/s", description="The transaction/s have already confirmed.", color=MAINCOLOR)
        mycursor.execute(f"UPDATE autocrypto_tickets_info SET payment_detected=%s, crypto_received=%s WHERE channel_id=%s", ("Yes", "Yes", interaction.channel.id))
        db.commit()
      else:
        embede = discord.Embed(title="Transaction/s", description="The bot will ping both of you once the transaction/s reaches 1 confirmation.", color=MAINCOLOR)
        mycursor.execute(f"UPDATE autocrypto_tickets_info SET payment_detected=%s WHERE channel_id=%s", ("Yes", interaction.channel.id))
        db.commit()

      embede.add_field(name="Transaction/s Hash", value=txString, inline=False)
      await interaction.channel.send(embed=embede)

      if unconf != 0:
        await interaction.channel.send("Please wait until the transaction/s reaches 1 confirmation.")

      mycursor.close();db.close()

    else:
      req_usd_amount = promised_usd_amount-received_usd_amount
      req_btc_amount = shorten_btc(req_usd_amount/usdprice)

      usd = shorten(totalbtc*usdprice)

      totalbtc = getWholeFloat(totalbtc)

      req_btc_amount = getWholeFloat(req_btc_amount)

      await interaction.channel.send(f"You have sent only `{totalbtc}` btc which is `${usd}`, please send `{req_btc_amount}` btc more.")
      mycursor.close();db.close()
      await interaction.message.edit(view=PasteAddress())
      return

@bot.command()
@commands.cooldown(1, 10, commands.BucketType.user)
async def confirm(ctx):
  if ctx.message.channel.category.id == AUTOCRYPTO_CATEGORY_ID:
    db = mysql.connector.connect(
      host="remotemysql.com",
      user="uDNB0NiyRu",
      passwd="AAxYedadAw",
      database="uDNB0NiyRu")
    mycursor = db.cursor()

    mycursor.execute(f"SELECT trader_seller_id, ticket_status, crypto_received, trade_confirmed, trader_receiver_id FROM autocrypto_tickets_info WHERE channel_id = '{ctx.channel.id}'")
    data = mycursor.fetchall()

    if data[0][1] != "Active":
      mycursor.close();db.close()
      return

    if ctx.author.id != data[0][0]:
      mycursor.close(); db.close()
      await ctx.reply("You don't have permission to use this command.")
      return

    if data[0][2] == "No":
      mycursor.close(); db.close()
      await ctx.reply("The bot has not received the payment yet.")
      return

    if data[0][3] == "Yes":
      mycursor.close(); db.close()
      await ctx.reply("The trade has already been confirmed.")
      return
      
    class haveYouBeenPaid(discord.ui.View):
      def __init__(self):
        super().__init__(timeout=None)
      @discord.ui.button(row=0, label="Yes", style=discord.ButtonStyle.green, custom_id="lolYes", disabled=False)
      async def button_callback1(self, button, interaction):
        
        await interaction.response.defer()
        
        if interaction.user.id != data[0][0]:
          return
        
        for child in self.children:
          child.disabled = True
        await interaction.message.edit(view=self)

        db = mysql.connector.connect(
          host="remotemysql.com",
          user="uDNB0NiyRu",
          passwd="AAxYedadAw",
          database="uDNB0NiyRu")
        mycursor = db.cursor()
        
        mycursor.execute(f"UPDATE autocrypto_tickets_info SET trade_confirmed=%s WHERE channel_id=%s", ("Yes", ctx.channel.id))
        db.commit()
        mycursor.close()
        db.close()
        
        await interaction.message.reply(content=f"**Your trader can now withdraw their crypto.**")
        await interaction.channel.send(f"<@{data[0][4]}> Use the command `$redeem Addy`\nAddy is your crypto address.")
        
      @discord.ui.button(row=0, label="No", style=discord.ButtonStyle.red, custom_id="Nopee", disabled=False)
      async def button_callback2(self, button, interaction):
        
        await interaction.response.defer()          
        
        if interaction.user.id != data[0][0]:
          return

        await interaction.message.delete()
      
    embed=discord.Embed(title="Are you sure you have received your items/money?", description="> By clicking \"Yes\", you will give your trader permission to withdraw their crypto.", color=MAINCOLOR)
    await ctx.reply(embed=embed, view=haveYouBeenPaid())

    mycursor.close(); db.close()

@bot.command()
@commands.cooldown(1, 10, commands.BucketType.user)
async def redeem(ctx, addy=None):
  if ctx.message.channel.category.id == AUTOCRYPTO_CATEGORY_ID:
    global session

    db = mysql.connector.connect(
      host="remotemysql.com",
      user="uDNB0NiyRu",
      passwd="AAxYedadAw",
      database="uDNB0NiyRu")
    mycursor = db.cursor()

    mycursor.execute(f"SELECT trader_seller_id, ticket_status, crypto_received, trade_confirmed, trader_receiver_id, has_paid, trade_amount_cry, hold_address FROM autocrypto_tickets_info WHERE channel_id = '{ctx.channel.id}'")
    data = mycursor.fetchall()

    if data[0][1] != "Active":
      mycursor.close();db.close()
      return

    if ctx.author.id != data[0][4]:
      mycursor.close(); db.close()
      await ctx.reply("You don't have permission to use this command.")
      return

    if data[0][5] == "Yes":
      mycursor.close(); db.close()
      await ctx.reply("The bot has already sent you the payment.")
      return

    if data[0][2] == "No":
      mycursor.close(); db.close()
      await ctx.reply("The bot has not received the payment yet.")
      return

    if data[0][3] == "No":
      mycursor.close(); db.close()
      await ctx.reply("Your trader has not used the `$confirm` command yet.")
      return

    if addy == None:
      mycursor.close(); db.close()
      await ctx.reply("Addy is missing, provide your crypto address.")
      return

    params = {'address': addy}
    res = session.get('https://apirone.com/api/v2/network/btc/is_valid_address', params=params).json()
    if res == False:
      mycursor.close(); db.close()
      await ctx.reply("The address you provided is invalid.")
      return

    class IsThisYourAddy(discord.ui.View):
      def __init__(self):
        super().__init__(timeout=None)
      @discord.ui.button(row=0, label="Yes", style=discord.ButtonStyle.green, custom_id="yesMyAddy", disabled=False)
      async def button_callback1(self, button, interaction):
        
        await interaction.response.defer()
        
        if interaction.user.id != data[0][4]:
          return
        
        for child in self.children:
          child.disabled = True
        await interaction.message.edit(view=self)

        json_data = {
            'currency': 'btc',
            'transfer-key': APIRONE_TRANSFER_ID,
            'addresses': [data[0][7]],
            'destinations': [
                {
                    'address': addy,
                    'amount': round(data[0][6]*100000000),
                },
            ],
            'fee': 'normal',
            'subtract-fee-from-amount': True,
        }

        res = session.post(f'https://apirone.com/api/v2/accounts/apr-{APIRONE_ACCOUNT_ID}/transfer', json=json_data)
        if res.status_code != 200:
          await interaction.message.reply(content=f"Unknown error has occured, please ping Chase or Kookie and let them know about this.")
          return

        txid = ""
        for i in res.json()['txs']:
          txid = i

        usdprice = session.get("https://apirone.com/api/v2/ticker?currency=btc").json().get('usd')

        totalam = res.json()['amount']/100000000
        useam = shorten(usdprice*totalam)

        db = mysql.connector.connect(
          host="remotemysql.com",
          user="uDNB0NiyRu",
          passwd="AAxYedadAw",
          database="uDNB0NiyRu")
        mycursor = db.cursor()
        
        mycursor.execute(f"UPDATE autocrypto_tickets_info SET has_paid=%s WHERE channel_id=%s", ("Yes", ctx.channel.id))
        db.commit()
        mycursor.close()
        db.close()
        
        await interaction.message.reply(content=f"**The bot has sent `${useam}` | `{data[0][6]}` to `{addy}`**\nTransaction: https://blockchair.com/bitcoin/transaction/{txid}")

      @discord.ui.button(row=0, label="No", style=discord.ButtonStyle.red, custom_id="noitsnot", disabled=False)
      async def button_callback2(self, button, interaction):
        
        await interaction.response.defer()          
        
        if interaction.user.id != data[0][4]:
          return

        await interaction.message.delete()
    
    usdprice = session.get("https://apirone.com/api/v2/ticker?currency=btc").json().get('usd')
    useame = shorten(usdprice*data[0][6])

    embed=discord.Embed(title="Are you sure that this is your address?", description=f"> By clicking \"Yes\", the bot will send `${useame}` | `{data[0][6]}` to that address.", color=MAINCOLOR)
    await ctx.reply(embed=embed, view=IsThisYourAddy())

    mycursor.close(); db.close()

class SellerOrBuyer(discord.ui.View):
  def __init__(self):
    super().__init__(timeout=None)
  @discord.ui.button(row=0, label="Seller", style=discord.ButtonStyle.blurple, custom_id="imseller", disabled=False)
  async def button_callback1(self, button, interaction):
    
    msgs = await interaction.channel.history(limit=None, oldest_first=True).flatten()
    user = msgs[0].mentions[0]

    if interaction.user.id != user.id:
      await interaction.response.defer()
      return

    for child in self.children:
      child.disabled = True
    await interaction.message.edit(view=self)

    await interaction.response.defer()

    db = mysql.connector.connect(
      host="remotemysql.com",
      user="uDNB0NiyRu",
      passwd="AAxYedadAw",
      database="uDNB0NiyRu")
    mycursor = db.cursor()

    mycursor.execute(f"UPDATE autocrypto_tickets_info SET trader_seller_id=%s, owner_trader_type=%s WHERE channel_id=%s", (interaction.user.id, "seller", interaction.channel.id))
    db.commit()
    embed = discord.Embed(title="What's the CryptoCurrency type?", description="Select the coin that you're giving to your trader.", color=MAINCOLOR)
    embed.set_footer(text="Selected: ")
    await interaction.channel.send(embed=embed, view=CryptoType())
    mycursor.close()
    db.close()

    editedembed = interaction.message.embeds[0]
    editedembed.set_footer(text="Selected: Seller")
    await interaction.message.edit(embed=editedembed)

  @discord.ui.button(row=0, label="Buyer", style=discord.ButtonStyle.blurple, custom_id="imbuyer", disabled=False)
  async def button_callback2(self, button, interaction):
    msgs = await interaction.channel.history(limit=None, oldest_first=True).flatten()
    user = msgs[0].mentions[0]

    if interaction.user.id != user.id:
      await interaction.response.defer()
      return

    for child in self.children:
      child.disabled = True
    await interaction.message.edit(view=self)

    await interaction.response.defer()

    db = mysql.connector.connect(
      host="remotemysql.com",
      user="uDNB0NiyRu",
      passwd="AAxYedadAw",
      database="uDNB0NiyRu")
    mycursor = db.cursor()

    mycursor.execute(f"UPDATE autocrypto_tickets_info SET trader_receiver_id=%s, owner_trader_type=%s WHERE channel_id=%s", (interaction.user.id, "buyer", interaction.channel.id))
    db.commit()
    embed = discord.Embed(title="What's the CryptoCurrency type?", description="Select the coin that you're going to receive from your trader.", color=MAINCOLOR)
    embed.set_footer(text="Selected: ")
    await interaction.channel.send(embed=embed, view=CryptoType())
    mycursor.close()
    db.close()

    editedembed = interaction.message.embeds[0]
    editedembed.set_footer(text="Selected: Buyer")
    await interaction.message.edit(embed=editedembed)

class CryptoType(discord.ui.View):
  def __init__(self):
    super().__init__(timeout=None)
  @discord.ui.button(row=0, label="BTC", style=discord.ButtonStyle.blurple, custom_id="btctype", disabled=False, emoji="<:fee_bitcoin:870211550722543707>")
  async def button_callback1(self, button, interaction):
    
    msgs = await interaction.channel.history(limit=None, oldest_first=True).flatten()
    user = msgs[0].mentions[0]

    if interaction.user.id != user.id:
      await interaction.response.defer()
      return

    for child in self.children:
      child.disabled = True
    await interaction.message.edit(view=self)

    await interaction.response.defer()

    db = mysql.connector.connect(
      host="remotemysql.com",
      user="uDNB0NiyRu",
      passwd="AAxYedadAw",
      database="uDNB0NiyRu")
    mycursor = db.cursor()

    mycursor.execute(f"UPDATE autocrypto_tickets_info SET crypto_type=%s WHERE channel_id=%s", ("BTC", interaction.channel.id))
    db.commit()
    embed = discord.Embed(title="How much is the deal in USD?", description="Reply with numbers.", color=MAINCOLOR)
    await interaction.channel.send(embed=embed)
    mycursor.close()
    db.close()

    editedembed = interaction.message.embeds[0]
    editedembed.set_footer(text="Selected: BTC")
    await interaction.message.edit(embed=editedembed)

    await interaction.channel.set_permissions(user, send_messages=True, view_channel=True, attach_files=True, embed_links=True, read_message_history=True)

  @discord.ui.button(row=0, label="ETH", style=discord.ButtonStyle.blurple, custom_id="ethtype", disabled=True, emoji="<:fee_eth:913749231678930975>")
  async def button_callback2(self, button, interaction):
    print(1)

  @discord.ui.button(row=0, label="LTC", style=discord.ButtonStyle.blurple, custom_id="ltctype", disabled=True, emoji="<:fee_ltc:917264308218515526>")
  async def button_callback3(self, button, interaction):
    print(1)

bot.run(TOKEN)