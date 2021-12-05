import asyncio
import app as app
import discord
from discord import client
from discord.ext import commands
import os
import threading
import sys
import json
import time
import datetime
from discord.ext.commands.bot import Bot
from pytz import timezone
import urllib
import discord, asyncio, pytz, datetime
from discord.ext import commands
# command_prefix 안에는 원하는 접두사를 넣어주면 된다.
# ex) !, / ....
from Cogs.game import coin

intents = discord.Intents.all()  # 모든 인텐트를 켭니다
bot = commands.Bot(command_prefix="나츠미 ")

@bot.event
async def on_ready():
    print('Loggend in Bot: ', bot.user.name)
    print('Bot id: ', bot.user.id)
    print('connection was succesful!')
    print('=' * 30)

@bot.command(name="청소", pass_context=True)
async def _clear(ctx, *, amount=5):
    @bot.command(name="추방", pass_context=True)
    async def _kick(ctx, *, user_name: discord.Member, reason=None):
        await user_name.kick(reason=reason)
        await ctx.send(str(user_name) + "을(를) 추방시켰다냥. 🤣🤣")

    @bot.command(name="밴", pass_context=True)
    async def _ban(ctx, *, user_name: discord.Member):
        await user_name.ban()
        await ctx.send(str(user_name) + "을(를) 영원히 숙청시켰다냥. 🤣🤣")

    @bot.command(name="언밴", pass_context=True)
    async def _unban(ctx, *, user_name):
        banned_users = await ctx.guild.bans()
        member_name, member_discriminator = user_name.split('#')
        for ban_entry in banned_users:
            user = ban_entry.user
            if (user.name, user.discriminator) == (member_name, member_discriminator):
                await ctx.guild.unban(user)
                await ctx.send(f"{user.mention}에게 적용되었던 밴을 풀었다냥!.🤣 ")
                return

    @bot.command(name="뮤트", aliases=["mute"])
    async def mute(ctx, user: discord.User):
        if ctx.author.guild_permissions.kick_members:
            await ctx.guild.get_channel(ctx.channel.category_id).set_permissions(user, send_messages=False)
            await ctx.send(f"{user}님을 뮤트 하였습니다!")
        else:
            await ctx.send("님은 뮤트시킬 권한이 없습니다!")

    @bot.command(name="언뮤트", aliases=["unmute"])
    async def unmute(ctx, user: discord.User):
        if ctx.author.guild_permissions.kick_members:
            await ctx.guild.get_channel(ctx.channel.category_id).set_permissions(user, send_messages=True)
            await ctx.send(f"{user}님을 언뮤트 하였습니다!")

@bot.command(name='공지작성')
async def Announcement(ctx, *, notice):
    i = ctx.message.author.guild_permissions.administrator
    channel = ctx.guild.get_channel(900280399438159898)  # 메시지를 보낼 채널 설정
    # Discord 에서 개발자 모드를 켜서 채널의 ID를 가져와 넣는다.

    if i is True:
        embed = discord.Embed(title="**나츠미가알려주는 공지사항!!**",
                              description="공지사항은 항상 잘 숙지 해주시기 바란다냥!\n――――――――――――――――――――――――――――\n\n{}\n\n――――――――――――――――――――――――――――".format(notice),
                              color=0x2EFEF7)
        embed.set_footer(text="Bot made by. 𝓗𝓐𝓡𝓤𝓚𝓘#7777 | 담당 관리자: {}".format(ctx.author), icon_url="https://imgur.com/1fTB9uk.png")
        await channel.send("@everyone", embed=embed)
        await ctx.send("```**[ BOT 자동 알림 ]** | 정상적으로 공지가 채널에 작성이 완료되었습니다 : )\n\n[ 기본 작성 설정 채널 ] : {}\n[ 공지 발신자 ] : {}\n\n[ 내용 ]\n{}```".format(channel, ctx.author, notice))

    if i is False:
        await ctx.send("{}, 당신은 관리자가 아닙니다".format(ctx.author.mention))

@bot.command(name="DM보내기", pass_context=True)
async def send_dm(ctx, user_name: discord.Member):
    channel = await user_name.create_dm()
    await channel.send("나츠미에 의해 출력됨.")

@bot.command(name="핑", aliases=["ping"])
async def ping(ctx):
    gcolor = 0x336BFF
    ecolor = 0x00ff56
    ncolor = 0xD9EA33
    omgcolor = 0xFF0000
    errorcolor = 0xC70039
    pings = round(bot.latency*1000)
    if pings < 100: 
        pinglevel = '🔵 매우좋음'
        color=gcolor
    elif pings < 200:
        pinglevel = '🟢 양호함'
        color=ecolor
    elif pings < 300:
        pinglevel = '🟡 보통'
        color=ncolor
    elif pings < 500:
        pinglevel = '🔴 나쁨'
        color=errorcolor
    else:
        pinglevel = '🔴 매우나쁨'
        color=omgcolor
    embed = discord.Embed(title="🏓 | 현재 내핑상태는!!", description=f"{pings}ms\n{pinglevel}", color=color)
    embed.set_footer(text="Bot Made by 𝓗𝓐𝓡𝓤𝓚𝓘#7777", icon_url="https://media.discordapp.net/attachments/890396367569182813/916197721361240104/IMG_1012.JPG?width=390&height=466")
    embed.set_thumbnail(url="https://media.discordapp.net/attachments/890396367569182813/916185428481150996/IMG_1029.PNG?width=409&height=467")
    await ctx.send(embed=embed)

@bot.command(name='방해금지')
async def dnd(ctx):
    await bot.change_presence(status=discord.Status.dnd)
    await ctx.send('✅봇 상태를 방해금지로 변경했습니다.')

@bot.command(name='온라인')
async def online(ctx):
    await bot.change_presence(status=discord.Status.online)
    await ctx.send('✅봇 상태를 온라인으로 변경했습니다.')

@bot.command(name="리로드")
async def reload_commands(ctx, extension=None):
    if extension is None: # extension이 None이면 (그냥 !리로드 라고 썼을 때)
        for filename in os.listdir("Cogs"):
            if filename.endswith(".py"):
                bot.unload_extension(f"Cogs.{filename[:-3]}")
                bot.load_extension(f"Cogs.{filename[:-3]}")
                await ctx.send(":white_check_mark: 모든 명령어를 다시 불러왔습니다!")
    else:
        bot.unload_extension(f"Cog.{extension}")
        bot.load_extension(f"Cog.{extension}")
        await ctx.send(f":white_check_mark: {extension}을(를) 다시 불러왔습니다!")

@bot.command()
async def hi(ctx):
    await ctx.send("안녕!")

@bot.command(aliases=['안녕', 'ㅎㅇ', '안녕하세요'])
async def Hello(ctx):
    await ctx.send("{}, 반갑다냥~~".format(ctx.author.mention))

@bot.command()
async def 도움말(ctx):
    embed = discord.Embed(title="명령어다냥~", description="접두사는 나츠미 (도움말)이다냥!!", color=0xFFFFFF)
    embed.set_thumbnail(url="https://media.discordapp.net/attachments/890396367569182813/916185428481150996/IMG_1029.PNG?width=409&height=467")
    embed.set_image(url="https://media.discordapp.net/attachments/890396367569182813/916184901697540197/IMG_1009.JPG?width=468&height=467")
    embed.add_field(name="🎗️ 관리", value="청소,킥,밴,언밴,뮤트,언뮤트", inline=False) #inline이 False라면 다은줄로 넘깁니다.
    embed.add_field(name="⛩️ 핑", value="나츠미 핑{현재핑에 대한 정보를 불러와준다냥}", inline=False) #inline이 False라면 다은줄로 넘깁니다.
    embed.set_footer(text="Bot Made by 𝓗𝓐𝓡𝓤𝓚𝓘#7777", icon_url="https://media.discordapp.net/attachments/890396367569182813/916197721361240104/IMG_1012.JPG?width=390&height=466")

    await ctx.send(embed=embed)

@bot.command()
async def 관리(ctx):
    embed = discord.Embed(title="관리 명령어다냥", description="접두사는 나츠미 (도움말)이다냥!!", color=0xFFFFFF)
    embed.set_thumbnail(url="https://media.discordapp.net/attachments/890396367569182813/916185428481150996/IMG_1029.PNG?width=409&height=467")
    embed.set_image(url="https://media.discordapp.net/attachments/890396367569182813/916184901697540197/IMG_1009.JPG?width=468&height=467")
    embed.add_field(name="⛩ **청소**", value="```그야말로 청소다냥~ 갯수는 90까지!!```", inline=False) #inline이 False라면 다은줄로 넘깁니다.
    embed.add_field(name="⛩️ **킥**", value="```말그대로 사람을 내보낸다냥~~```", inline=False) #inline이 False라면 다은줄로 넘깁니다.
    embed.add_field(name="⛩️ **밴**", value="```말그대로 사람을 추방시킨다냥```", inline=False)  # inline이 False라면 다은줄로 넘깁니다.
    embed.add_field(name="⛩️ **언밴**", value="```추방시킨사람을 다시 풀어주는 기능이다냥```", inline=False)  # inline이 False라면 다은줄로 넘깁니다.
    embed.add_field(name="⛩️ **뮤트**", value="```닝겐들의 입막음을 시킨다냥 쿡쿡```", inline=False)  # inline이 False라면 다은줄로 넘깁니다.
    embed.add_field(name="⛩️ **언뮤트**", value="```닝겐들의 입막음을 풀어주겠다옹```", inline=False)  # inline이 False라면 다은줄로 넘깁니다.
    embed.set_footer(text="Bot Made by 𝓗𝓐𝓡𝓤𝓚𝓘#7777", icon_url="https://media.discordapp.net/attachments/890396367569182813/916197721361240104/IMG_1012.JPG?width=390&height=466")

    await ctx.send(embed=embed)

    
access_token = os.environ["BOT_TOKEN"]    
bot.run(acces_token)
