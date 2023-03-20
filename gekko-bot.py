import discord
import random
import csv
import datetime
import asyncio

intents = discord.Intents.all()
client = discord.Client(command_prefix='!', intents=intents)

glizzys_dict = dict()
current_dict = dict()
original_dict = dict()

def read_file(guild: str):
    try:
        with open(guild+".txt") as glizzys_file:
            glizzys_reader = csv.reader(glizzys_file, delimiter=',')
            line_count = 0
            for row in glizzys_reader:
                if (len(row) == 7):
                    name = row[0]
                    glizzys = int(row[1])
                    last_collected = datetime.datetime.fromisoformat(row[2])
                    steal_chance = int(row[3])
                    last_stolen = datetime.datetime.fromisoformat(row[4])
                    glizzy_milk = int(row[5])
                    last_hunted = datetime.datetime.fromisoformat(row[6])
                    glizzys_dict.update({name:[glizzys, last_collected, steal_chance, last_stolen, glizzy_milk, last_hunted]})
                    original_dict.update({name:[glizzys, last_collected, steal_chance, last_stolen, glizzy_milk, last_hunted]})
            glizzys_file.close()
    except FileNotFoundError:
        glizzys_file = open(guild+".txt",'w')
        glizzys_file.close()

def read_current_file(guild: str):
    try:
        with open(guild+".txt") as glizzys_file:
            glizzys_reader = csv.reader(glizzys_file, delimiter=',')
            line_count = 0
            for row in glizzys_reader:
                if (len(row) == 7):
                    name = row[0]
                    glizzys = int(row[1])
                    last_collected = datetime.datetime.fromisoformat(row[2])
                    steal_chance = int(row[3])
                    last_stolen = datetime.datetime.fromisoformat(row[4])
                    glizzy_milk = int(row[5])
                    last_hunted = datetime.datetime.fromisoformat(row[6])
                    current_dict.update({name:[glizzys, last_collected, steal_chance, last_stolen, glizzy_milk, last_hunted]})
            glizzys_file.close()
    except FileNotFoundError:
        glizzys_file = open(guild+".txt",'w')
        glizzys_file.close()

def update_file(guild: str):
    with open(guild+".txt", mode='w') as glizzys_file:
        glizzys_writer = csv.writer(glizzys_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for key in glizzys_dict.keys():
            glizzys_writer.writerow([key, glizzys_dict.get(key)[0], glizzys_dict.get(key)[1], glizzys_dict.get(key)[2], glizzys_dict.get(key)[3], glizzys_dict.get(key)[4], glizzys_dict.get(key)[5]])
        glizzys_file.close()
 
def confirm_database(message, mentioned=None):
    read_current_file(str(message.guild.id))
    found = False
    for key in current_dict.keys():
        for keyG in glizzys_dict.keys():
            if key == keyG:
                found = True
                if (mentioned != None):
                    if not (key == message.author.name or key == mentioned.name):
                        glizzys_dict.update({key:[current_dict.get(key)[0],current_dict.get(key)[1],current_dict.get(key)[2],current_dict.get(key)[3],current_dict.get(key)[4],current_dict.get(key)[5]]})
                else:
                    if not (key == message.author.name):
                        glizzys_dict.update({key:[current_dict.get(key)[0],current_dict.get(key)[1],current_dict.get(key)[2],current_dict.get(key)[3],current_dict.get(key)[4],current_dict.get(key)[5]]})
        if found == False:
            glizzys_dict.update({key:[current_dict.get(key)[0],current_dict.get(key)[1],current_dict.get(key)[2],current_dict.get(key)[3],current_dict.get(key)[4],current_dict.get(key)[5]]})        
 
@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
 
@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    #FETCH DICTIONARY
    read_file(str(message.guild.id))
    
    #LEADERBOARD
    if message.content.startswith('$leaderboard'):
        if message.author.name not in glizzys_dict.keys():
            glizzys_dict.update({message.author.name:[0, datetime.datetime.min, 50, datetime.datetime.min, 0, datetime.datetime.min]})
            confirm_database(message)
            update_file(str(message.guild.id))
        leaderboard = dict()
        for key in glizzys_dict.keys():
            leaderboard.update({key:glizzys_dict.get(key)[0]})
        sorted_leaderboard = sorted(leaderboard.items(), key=lambda x:x[1], reverse=True)
        leaderboard_string = "**Leaderboard**\n```"
        i = 0
        while (i < len(sorted_leaderboard) and i < 5):
            if (i > 0):
                leaderboard_string += "\n"
            leaderboard_string += f"{i+1}. {sorted_leaderboard[i][0]} has {sorted_leaderboard[i][1]} Glizzys"
            i += 1
        leaderboard_string += "```"
        await message.channel.send(leaderboard_string)

    #HELP
    if message.content.startswith('$help'):
        if message.author.name not in glizzys_dict.keys():
            glizzys_dict.update({message.author.name:[0, datetime.datetime.min, 50, datetime.datetime.min, 0, datetime.datetime.min]})
            confirm_database(message)
            update_file(str(message.guild.id))
        await message.channel.send("**Commands available:**\n```- $help :\t\t\t\t\tDisplay this screen.\n- $collect :\t\t\t\t Collect your Glizzys from Gekko. You must collect first in order to join the game. You can perform this command once a day.\n- $donate @user amount :\t Donate a specified amount of Glizzys to the mentioned user.\n- $steal @user :\t\t\t Attempt to rob the mentioned user. A lot like $donate in many ways. You can only steal once every two hours.\n- $milk :\t\t\t\t\tMilk your Glizzys in order to have enough energy to hunt for more. WARNING: some Glizzys might leave in horror.\n- $hunt :\t\t\t\t\tFollow in the footsteps of Gekko and attempt to hunt for more Glizzys. Costs 1 Glizzy Milk to hunt. You can only hunt once every half an hour.\n- $leaderboard :\t\t\t View the current top five players and their Glizzy count.\n- $me :\t\t\t\t\t  View how many Glizzys you have, your chances of successfully stealing and your countdowns for the $collect and $steal commands.```")

    #MILK
    if message.content.startswith('$milk'):
        if message.author.name not in glizzys_dict.keys():
            glizzys_dict.update({message.author.name:[0, datetime.datetime.min, 50, datetime.datetime.min, 0, datetime.datetime.min]})
            confirm_database(message)
            update_file(str(message.guild.id))
        if glizzys_dict.get(message.author.name)[0] >= 5:
            glizzys_lost = random.randrange(1, 5)
            milk_gained = 1
            for i in range(0, glizzys_lost):
                milk_gained += random.randrange(0, 2)
            user_properties = glizzys_dict.get(message.author.name)
            glizzys_dict.update({message.author.name:[user_properties[0] - glizzys_lost, user_properties[1], user_properties[2], user_properties[3], user_properties[4] + milk_gained, user_properties[5]]})
            confirm_database(message)
            update_file(str(message.guild.id))
            new_message = await message.channel.send(":sweat_drops: Washing hands...")
            await asyncio.sleep(1)
            await new_message.edit(content=":notes: Calming Glizzys...")
            await asyncio.sleep(1)
            await message.channel.send(f":milk: <@{message.author.id}> successfully milked {glizzys_lost} Glizzys and gained {milk_gained} Glizzy Milk. The milked Glizzys ran away.")
        else:
            await message.channel.send(f":weary: <@{message.author.id}> failed to milk any Glizzys as they don't have enough Glizzys to risk it.")

    #HUNT
    if message.content.startswith('$hunt'):
        if message.author.name not in glizzys_dict.keys():
            glizzys_dict.update({message.author.name:[0, datetime.datetime.min, 50, datetime.datetime.min, 0, datetime.datetime.min]})
            confirm_database(message)
            update_file(str(message.guild.id))
        hunt_delay = 1800
        if datetime.timedelta(seconds=hunt_delay) <= datetime.datetime.now() - glizzys_dict.get(message.author.name)[5]:
            glizzy_milk = glizzys_dict.get(message.author.name)[4]
            if glizzy_milk >= 1:
                glizzy_milk -= 1
                hunt_chance = random.randrange(0,5)
                caught_glizzys = hunt_chance * random.randrange(1,5)
                user_properties = glizzys_dict.get(message.author.name)
                glizzys_dict.update({message.author.name:[user_properties[0] + caught_glizzys, user_properties[1], user_properties[2], user_properties[3], glizzy_milk, datetime.datetime.now()]})
                confirm_database(message)
                update_file(str(message.guild.id))
                new_message = await message.channel.send(f":milk: Drinking Glizzy Milk...")
                await asyncio.sleep(1)
                await new_message.edit(content=":deciduous_tree: Searching bushes...")
                await asyncio.sleep(1)
                await new_message.edit(content=":beach: Taking romantic walks on beaches...")
                await asyncio.sleep(1)
                if (caught_glizzys > 0):
                    await new_message.edit(content=f":cyclone: Success! <@{message.author.id}> managed to capture {caught_glizzys} Glizzys. Drinking 1 Glizzy Milk in the process.")
                else:
                    await new_message.edit(content=f":melting_face: Damn, <@{message.author.id}> was unsuccessul on their hunt, catching 0 Glizzys and wasting 1 Glizzy Milk.")
            else:
                await message.channel.send(f":weary: <@{message.author.id}> does not have enough Glizzy Milk to go hunting!")
        else:
            total_seconds = (datetime.timedelta(seconds=hunt_delay) - (datetime.datetime.now() - glizzys_dict.get(message.author.name)[5])).total_seconds()
            hours = int(total_seconds // (60 * 60))
            minutes = int((total_seconds - (hours * 60 * 60)) // 60)
            seconds = int((total_seconds - (hours * 60 * 60) - (minutes * 60))//1)
            await message.channel.send(f':hourglass: <@{message.author.id}> must wait {hours:02d}:{minutes:02d}:{seconds:02d} until they can attempt to hunt again!')

    #DONATE
    if message.content.startswith('$donate'):
        if message.author.name not in glizzys_dict.keys():
            glizzys_dict.update({message.author.name:[0, datetime.datetime.min, 50, datetime.datetime.min, 0, datetime.datetime.min]})
            confirm_database(message)
            update_file(str(message.guild.id))
        if message.mentions == []:
            await message.channel.send(':x: Please mention someone in order to donate from them.')
        else:
            mentioned = message.mentions[0]
            if (mentioned.name not in glizzys_dict.keys()):
                await message.channel.send(f":dizzy_face: <@{mentioned.id}> is a loser and is not playing the game at the moment.")
            elif len(message.content.split()) < 3:
                await message.channel.send(':x: Please input an amount of Glizzys to donate.')
            else:
                try:
                    as_int = int(message.content.split()[2])
                    user_properties = glizzys_dict.get(mentioned.name)
                    glizzys_dict.update({mentioned.name:[user_properties[0] + as_int, user_properties[1], user_properties[2], user_properties[3], user_properties[4], user_properties[5]]})
                    user_properties = glizzys_dict.get(message.author.name)
                    glizzys_dict.update({message.author.name:[user_properties[0] - as_int, user_properties[1], user_properties[2], user_properties[3], user_properties[4], user_properties[5]]})
                    await message.channel.send(f":sunglasses: <@{message.author.id}> successfully donated {as_int} Glizzys to <@{mentioned.id}>!")
                    confirm_database(message, mentioned=mentioned)
                    update_file(str(message.guild.id))
                except ValueError:
                    await message.channel.send(":x: Please input the amount of Glizzys to donate as whole number. E.g. 5.")
       
    #ME
    if message.content.startswith('$me'):
        if message.author.name not in glizzys_dict.keys():
            glizzys_dict.update({message.author.name:[0, datetime.datetime.min, 50, datetime.datetime.min, 0, datetime.datetime.min]})
            confirm_database(message)
            update_file(str(message.guild.id))
        # Get hunt timer
        hunt_delay = 1800
        hunt_total_seconds = (datetime.timedelta(seconds=hunt_delay) - (datetime.datetime.now() - glizzys_dict.get(message.author.name)[5])).total_seconds()
        if (hunt_total_seconds > 0):
            hunt_hours = int(hunt_total_seconds // (60 * 60))
            hunt_minutes = int((hunt_total_seconds - (hunt_hours * 60 * 60)) // 60)
            hunt_seconds = int((hunt_total_seconds - (hunt_hours * 60 * 60) - (hunt_minutes * 60))//1)
        else:
            hunt_hours = 0
            hunt_minutes = 0
            hunt_seconds = 0
        # Get steal timer
        steal_delay = 7200
        steal_total_seconds = (datetime.timedelta(seconds=steal_delay) - (datetime.datetime.now() - glizzys_dict.get(message.author.name)[3])).total_seconds()
        if (steal_total_seconds > 0):
            steal_hours = int(steal_total_seconds // (60 * 60))
            steal_minutes = int((steal_total_seconds - (steal_hours * 60 * 60)) // 60)
            steal_seconds = int((steal_total_seconds - (steal_hours * 60 * 60) - (steal_minutes * 60))//1)
        else:
            steal_hours = 0
            steal_minutes = 0
            steal_seconds = 0
        # Get collect timer
        collect_delay = 86400
        collect_total_seconds = (datetime.timedelta(seconds=collect_delay) - (datetime.datetime.now() - glizzys_dict.get(message.author.name)[1])).total_seconds()
        if (collect_total_seconds > 0):
            collect_hours = int(collect_total_seconds // (60 * 60))
            collect_minutes = int((collect_total_seconds - (collect_hours * 60 * 60)) // 60)
            collect_seconds = int((collect_total_seconds - (collect_hours * 60 * 60) - (collect_minutes * 60))//1)
        else:
            collect_hours = 0
            collect_minutes = 0
            collect_seconds = 0
        # Get leaderboard position
        leaderboard = dict()
        for key in glizzys_dict.keys():
            leaderboard.update({key:glizzys_dict.get(key)[0]})
        sorted_leaderboard = sorted(leaderboard.items(), key=lambda x:x[1], reverse=True)
        position = 0
        for i in range(0,len(leaderboard)):
            if (sorted_leaderboard[i][0] == message.author.name):
                position = i+1
        user_properties = glizzys_dict.get(message.author.name)
        await message.channel.send(f"<@{message.author.id}>\n```Glizzys:\t\t {user_properties[0]}\nGlizzy Milk:\t {user_properties[4]}\nSteal Chance:\t{user_properties[2]}%\nSteal Timer:\t {steal_hours:02d}:{steal_minutes:02d}:{steal_seconds:02d}\nHunt Timer:\t  {hunt_hours:02d}:{hunt_minutes:02d}:{hunt_seconds:02d}\nCollect Timer:   {collect_hours:02d}:{collect_minutes:02d}:{collect_seconds:02d}\nLeaderboard:\t #{position}```")

    #STEAL
    if message.content.startswith('$steal'):
        if message.author.name not in glizzys_dict.keys():
            glizzys_dict.update({message.author.name:[0, datetime.datetime.min, 50, datetime.datetime.min, 0, datetime.datetime.min]})
            confirm_database(message)
            update_file(str(message.guild.id))
        steal_delay = 7200
        min_steal = 1
        max_steal = 20
        if datetime.timedelta(seconds=steal_delay) <= datetime.datetime.now() - glizzys_dict.get(message.author.name)[3]:
            if message.mentions == []:
                await message.channel.send(':x: Please mention someone in order to steal from them.')
            else:
                mentioned = message.mentions[0]
                if (mentioned.name not in glizzys_dict.keys()):
                    await message.channel.send(f":dizzy_face: <@{mentioned.id}> is a loser and is not playing the game at the moment.")
                elif (glizzys_dict.get(mentioned.name)[0] < max_steal):
                    await message.channel.send(f":face_with_peeking_eye: <@{mentioned.id}> does not have enough Glizzys to steal from.")
                elif (random.randrange(0,100) > glizzys_dict.get(message.author.name)[2]):
                    odds = glizzys_dict.get(message.author.name)[2] + random.randrange(1,10)
                    if odds > 100:
                        odds = 100
                    user_properties = glizzys_dict.get(message.author.name)
                    glizzys_dict.update({message.author.name:[user_properties[0], user_properties[1], odds, datetime.datetime.now(), user_properties[4], user_properties[5]]})
                    new_message = await message.channel.send(":busts_in_silhouette: Sneaking up behind target...")
                    await asyncio.sleep(1)
                    await new_message.edit(content=":bubbles: Blinding target...")
                    await asyncio.sleep(1)
                    await new_message.edit(content=":disguised_face: Picking pockets...")
                    await asyncio.sleep(1)
                    await new_message.edit(content=f":melting_face: <@{message.author.id}> failed to steal Glizzys from <@{mentioned.id}>!")
                else:
                    steal = random.randrange(min_steal, max_steal)
                    total = glizzys_dict.get(message.author.name)[0] + steal
                    odds = glizzys_dict.get(message.author.name)[2] - random.randrange(1,20)
                    if odds < 10:
                        odds = 10
                    user_properties = glizzys_dict.get(mentioned.name)
                    glizzys_dict.update({mentioned.name:[user_properties[0]-steal, user_properties[1], user_properties[2], user_properties[3], user_properties[4], user_properties[5]]})
                    user_properties = glizzys_dict.get(message.author.name)
                    glizzys_dict.update({message.author.name:[total, user_properties[1], odds, datetime.datetime.now(), user_properties[4], user_properties[5]]})
                    new_message = await message.channel.send(":busts_in_silhouette: Sneaking up behind target...")
                    await asyncio.sleep(1)
                    await new_message.edit(content=":bubbles: Blinding target...")
                    await asyncio.sleep(1)
                    await new_message.edit(content=":disguised_face: Picking pockets...")
                    await asyncio.sleep(1)
                    await new_message.edit(content=f":spy: <@{message.author.id}> successfully stole {steal} Glizzys from <@{mentioned.id}>!")
                confirm_database(message, mentioned=mentioned)
                update_file(str(message.guild.id))
        else:
            total_seconds = (datetime.timedelta(seconds=steal_delay) - (datetime.datetime.now() - glizzys_dict.get(message.author.name)[3])).total_seconds()
            hours = int(total_seconds // (60 * 60))
            minutes = int((total_seconds - (hours * 60 * 60)) // 60)
            seconds = int((total_seconds - (hours * 60 * 60) - (minutes * 60))//1)
            await message.channel.send(f':hourglass: <@{message.author.id}> must wait {hours:02d}:{minutes:02d}:{seconds:02d} until they can attempt to steal again!')

    #COLLECT
    if message.content.startswith('$collect'):
        collect_delay = 86400
        min_collect = 10
        max_collect = 30
        if message.author.name not in glizzys_dict.keys():
            glizzys_dict.update({message.author.name:[0, datetime.datetime.min, 50, datetime.datetime.min, 0, datetime.datetime.min]})
            confirm_database(message)
            update_file(str(message.guild.id))
        if datetime.timedelta(seconds=collect_delay) <= datetime.datetime.now() - glizzys_dict.get(message.author.name)[1]:
            collected = random.randrange(min_collect,max_collect)
            total = glizzys_dict.get(message.author.name)[0] + collected
            odds = glizzys_dict.get(message.author.name)[2]
            last_thieved = glizzys_dict.get(message.author.name)[3]
            glizzy_milk = glizzys_dict.get(message.author.name)[4]
            hunt_chance = glizzys_dict.get(message.author.name)[5]
            glizzys_dict.update({message.author.name:[total, datetime.datetime.now(), odds, last_thieved, glizzy_milk, hunt_chance]})
            confirm_database(message)
            update_file(str(message.guild.id))
            await message.channel.send(f':cyclone: Collected {collected} Glizzys! <@{message.author.id}> now has {total} Glizzys!')
        else:
            total_seconds = (datetime.timedelta(seconds=collect_delay) - (datetime.datetime.now() - glizzys_dict.get(message.author.name)[1])).total_seconds()
            hours = int(total_seconds // (60 * 60))
            minutes = int((total_seconds - (hours * 60 * 60)) // 60)
            seconds = int((total_seconds - (hours * 60 * 60) - (minutes * 60))//1)
            await message.channel.send(f':hourglass: <@{message.author.id}> must wait {hours:02d}:{minutes:02d}:{seconds:02d} until they can collect more Glizzys!')

client.run('MTA4NTQyODkxMjY2MzgzNDY0NQ.GHFw7X.tZkKOX53pwDT1g3odwOegPfynklfTK5tpdL3a8')