import discord

client = discord.Client()

category = 0
room = {}
players = {}

@client.event
async def on_ready():
    print(f'{client.user.name}이 구동 준비되었습니다!')

@client.event
async def on_message(message):
    global category, room
    if message.content == '!게임설정':
        category = await message.guild.create_category('마피아게임')
        room['설정'] = await message.guild.create_text_channel('설정', category=category)
        room['마피아'] = await message.guild.create_text_channel('마피아', category=category)
        room['낮'] = await message.guild.create_text_channel('낮', category=category)
        room['유령'] = await message.guild.create_text_channel('유령', category=category)
        for i in range(1,9):
            room[f'플레이어{i}'] = await message.guild.create_text_channel(f'플레이어{i}', category=category)


    if message.content == '!게임종료':
        for room_number in room:
            await room[room_number].delete()
        await category.delete()

    if message.content.starts_with('!참가자등록'):

        

client.run("ODIwNjgzNjMzNjM5NTU1MTAy.YE4vMQ.5Gk-EtzAEzgICFoh7KmTtk_zh4Y")