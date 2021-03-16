import discord
from discord.ext import commands
from discord.ext.commands import MemberConverter, Bot

bot = commands.Bot(command_prefix='!')
category = 0
room = {}
players = {}
join_member = ''
member_list = []

@bot.event
async def on_ready():
    print(f'{bot.user.name}이 구동 준비되었습니다!')

@bot.command()
async def 게임설정(ctx):
    global category, room
    category = await ctx.guild.create_category('마피아게임')
    room['설정'] = await ctx.guild.create_text_channel('설정', category=category)
    room['마피아'] = await ctx.guild.create_text_channel('마피아', category=category)
    room['낮'] = await ctx.guild.create_text_channel('낮', category=category)
    room['유령'] = await ctx.guild.create_text_channel('유령', category=category)
    for i in range(1,9):
        room[f'플레이어{i}'] = await ctx.guild.create_text_channel(f'플레이어{i}', category=category)

@bot.command()
async def 게임종료(ctx):
    for room_number in room:
        await room[room_number].delete()
    await category.delete()

@bot.command()
async def 참가자등록(ctx, *, join_member: str):
    global member_list
    converter = MemberConverter()
    member_list = [str(i) for i in join_member.split(" ")]
    for i in range(0,8):
        tmp = member_list[i]
        member_list[i] = await converter.convert(ctx, tmp[0:])
    print(member_list)

@bot.command(pass_context=True)
async def 게임시작(ctx):
    print(member_list[0].name)
    await member_list[0].name.add_roles("asdf")
    

bot.run("ODIwNjgzNjMzNjM5NTU1MTAy.YE4vMQ.0-q5UbWG4QdsEYTIWMGSbxtX8Ek")