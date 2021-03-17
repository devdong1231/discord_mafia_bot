import discord
from discord.ext import commands
from discord.ext.commands import MemberConverter, Bot
from discord.utils import get
import random, time

# 1: 마피아 2: 마피아 3: 스파이 4: 경찰 5: 의사 6: 특직1 7: 특직2 8: 특직3
# 특수직업 - 1: 군인 2: 건달 3: 기자 4: 영매 5: 정치인

bot = commands.Bot(command_prefix='!')

category = 0
room = {}
role = {}
join_member = ''
member_list = []
member_list_copy = []
member_dic = {}
job = [1, 2, 3, 4, 5, 6, 7, 8]

@bot.event
async def on_ready():
    print(f'{bot.user.name}이 구동 준비되었습니다!')

@bot.command()
async def 역할(ctx):
    await ctx.guild.create_role(name="asdf")

@bot.command()
async def 게임세팅(ctx):
    global category, room, role
    for i in range(0,3): # 플레이어의 수 만큼의 역할 생성
        role[f"플레이어{i+1}"] = await ctx.guild.create_role(name=f"플레이어{i+1}")
    overwrites ={ctx.guild.default_role: discord.PermissionOverwrite(read_messages = False)} # 채팅방 권한 설정
    category = await ctx.guild.create_category('마피아게임') # '마피아게임'이라는 카테고리 만들기
    room['설정'] = await ctx.guild.create_text_channel('설정', category=category, overwrites=overwrites) # '설정' 채팅방 만들기
    room['마피아'] = await ctx.guild.create_text_channel('마피아', category=category, overwrites=overwrites) # '마피아' 채팅방 만들기
    room['낮'] = await ctx.guild.create_text_channel('낮', category=category) # '낮' 채팅방 만들기
    room['유령'] = await ctx.guild.create_text_channel('유령', category=category, overwrites=overwrites) # '유령' 채팅방 만들기
    for i in range(0,8): # 플레이어의 수만큼의 채팅방 생성, 각각의 플레이어에게 자신의 채널을 볼 수 있는 권한 부여
        overwrites = {
            ctx.guild.default_role: discord.PermissionOverwrite(read_messages = False),
            role[f"플레이어{i+1}"]: discord.PermissionOverwrite(read_messages = True)
        }
        room[f'플레이어{i+1}'] = await ctx.guild.create_text_channel(f'플레이어{i+1}', category=category, overwrites=overwrites)
    

@bot.command()
async def 게임종료(ctx):
    for role_number in role: # 역할 삭제
        await role[role_number].delete()
    for room_number in room: # 채팅방 삭제
        await room[room_number].delete()
    await category.delete() # 카테고리 삭제

@bot.command()
async def 참가자등록(ctx, *, join_member: str):
    global member_list
    converter = MemberConverter() # string을 discord.member으로 바꿔주는 converter
    member_list = [str(i) for i in join_member.split(" ")] # ' '를 기준으로 멤버를 나눠 리스트에 저장
    for i in range(0,8): # 각 리스트에 있는 string들을 converter으로 discord.member로 바꿔줌
        tmp = member_list[i]
        member_list[i] = await converter.convert(ctx, tmp[0:])
    print("참가자등록 완료")

@bot.command()
async def 게임시작(ctx):
    global room, member_list_copy, member_list, member_dic
    random.shuffle(job) # 직업 섞기
    for i in range(0,8):
        await member_list[i].add_roles(role[f"플레이어{i+1}"]) # 플레이어들에게 각각의 역할 부여(채팅방 보기 권한)
        member_dic[member_list[i]] = job[i] # 딕셔너리의 key에는 플레이어의 정보, value에는 직업이 들어있음
    print(member_dic)
    member_dic = dict(map(reversed,member_dic.items())) # 딕셔너리의 key와 value를 바꿈
    print(member_dic)
    special_job_list = [1, 2, 3, 4, 5]
    random.shuffle(special_job_list)
    await room['마피아'].set_permissions(member_list[0], read_messages=True)
    await room['마피아'].set_permissions(member_list[1], read_messages=True)
    status_message = await room['낮'].send('밤이 되었습니다. 25초 후 낮이 됩니다.')
    time.sleep(1)
    for i in range(1,25):
        await status_message.edit(content = f"밤이 되었습니다. {25-i}초 후 낮이 됩니다.")
        time.sleep(1)
    await status_message.edit(content = f"낮이 되었습니다.")

@bot.command()
async def 경찰(ctx, choice: str):
    choice = choice[4:]
    choice = int(choice)
    #print(member_dic[choice])
    # if member_dic[choice] == 4:
    #     await ctx.send('자기 자신은 지목할 수 없습니다.')
    # elif member_dic[choice] == 1 or member_dic[choice] == 2:
    #     await ctx.send(f'플레이어{choice}은 마피아입니다.')
    # else:
    #     await ctx.send(f'플레이어{choice}은 마피아가 아닙니다.')


bot.run("ODIwNjgzNjMzNjM5NTU1MTAy.YE4vMQ.VvX9M3rIuyIVO5e1-BJbAcn2JVs")

# 랜덤으로 직업 생성, 타이머