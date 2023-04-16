import discord
import random
import csv
import datetime
import asyncio
import socket
import time
from mcstatus import JavaServer

intents = discord.Intents.all()
client = discord.Client(command_prefix='?', intents=intents)

glizzys_dict = dict()
current_dict = dict()
#original_dict = dict()
server_dict = dict()
react_list = list()
current_server_dict = dict()
current_react_list = list()

# ^^^^^^^^^ Code from https://gist.github.com/Fmstrat -> https://gist.github.com/betrcode/0248f0fda894013382d7^^^^^^^^^^^^^
retry = 2
delay = 2
timeout = 3

def isOpen(ip, port):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(timeout)
        try:
                s.connect((ip, int(port)))
                s.shutdown(socket.SHUT_RDWR)
                return True
        except:
                return False
        finally:
                s.close()

def checkHost(ip, port):
        ipup = False
        for i in range(retry):
                if isOpen(ip, port):
                        ipup = True
                        break
                else:
                        time.sleep(delay)
        return ipup
# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

def read_prop(guild: str):
    try:
        server_dict.clear()
        react_list.clear()
        with open(guild+"_properties.txt") as prop_file:
            prop_reader = csv.reader(prop_file, delimiter=',')
            for row in prop_reader:
                if (len(row) > 0):
                    if (row[0] == "server" and len(row) == 4):
                        name = row[1]
                        ip = row[2]
                        port = row[3]
                        server_dict.update({"name":name})
                        server_dict.update({"ip":ip})
                        server_dict.update({"port":port})
                    elif (row[0] == "react_role" and len(row) == 5):
                        channel = row[1]
                        message = row[2]
                        emoji = row[3]
                        role = row[4]
                        react_list.append([channel, message, emoji, role])
            prop_file.close()
    except FileNotFoundError:
        prop_file = open(guild+"_properties.txt",'w')
        prop_file.close()

def update_roles(guild, channel, message, emoji, role):
    current_server_dict.clear()
    current_react_list.clear()
    current_react_list.append([channel, message, emoji, role])
    with open(guild+"_properties.txt", "r") as prop_file:
        prop_reader = csv.reader(prop_file, delimiter=',')
        for row in prop_reader:
            if (len(row) > 0):
                if (row[0] == "server" and len(row) == 4):
                    name = row[1]
                    ip = row[2]
                    port = row[3]
                    current_server_dict.update({"name":name})
                    current_server_dict.update({"ip":ip})
                    current_server_dict.update({"port":port})
                elif (row[0] == "react_role" and len(row) == 5):
                    channel = row[1]
                    message = row[2]
                    emoji = row[3]
                    role = row[4]
                    current_react_list.append([channel, message, emoji, role])
        prop_file.close()
    with open(guild+"_properties.txt", "w") as prop_file:
        prop_writer = csv.writer(prop_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        server_name = current_server_dict.get("name")
        server_ip = current_server_dict.get("ip")
        server_port = current_server_dict.get("port")
        if (server_name != None and server_ip != None and server_port != None):
            prop_writer.writerow(["server",server_name,server_ip,server_port])
        for ls in current_react_list:
            ls.insert(0, "react_role")
            prop_writer.writerow(ls)
        prop_file.close()

def update_server(guild, name, ip, port):
    current_server_dict.clear()
    current_react_list.clear()
    current_server_dict.update({"name":name})
    current_server_dict.update({"ip":ip})
    current_server_dict.update({"port":port})
    with open(guild+"_properties.txt", "r") as prop_file:
        prop_reader = csv.reader(prop_file, delimiter=',')
        for row in prop_reader:
            if (len(row) > 0):
                if (row[0] == "react_role" and len(row) == 5):
                    channel = row[1]
                    message = row[2]
                    emoji = row[3]
                    role = row[4]
                    current_react_list.append([channel, message, emoji, role])
        prop_file.close()
    with open(guild+"_properties.txt", "w") as prop_file:
        prop_writer = csv.writer(prop_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        server_name = current_server_dict.get("name")
        server_ip = current_server_dict.get("ip")
        server_port = current_server_dict.get("port")
        if (server_name != None and server_ip != None and server_port != None):
            prop_writer.writerow(["server",server_name,server_ip,server_port])
        for ls in current_react_list:
            ls.insert(0, "react_role")
            prop_writer.writerow(ls)
        prop_file.close()

def read_file(guild: str):
    try:
        glizzys_dict.clear()
        with open(guild+".txt") as glizzys_file:
            glizzys_reader = csv.reader(glizzys_file, delimiter=',')
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
                    #original_dict.update({name:[glizzys, last_collected, steal_chance, last_stolen, glizzy_milk, last_hunted]})
            glizzys_file.close()
    except FileNotFoundError:
        glizzys_file = open(guild+".txt",'w')
        glizzys_file.close()

# deprecated
def read_current_file(guild: str):
    try:
        with open(guild+".txt") as glizzys_file:
            glizzys_reader = csv.reader(glizzys_file, delimiter=',')
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

# deprecated
def update_file(guild: str):
    with open(guild+".txt", mode='w') as glizzys_file:
        glizzys_writer = csv.writer(glizzys_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for key in glizzys_dict.keys():
            glizzys_writer.writerow([key, glizzys_dict.get(key)[0], glizzys_dict.get(key)[1], glizzys_dict.get(key)[2], glizzys_dict.get(key)[3], glizzys_dict.get(key)[4], glizzys_dict.get(key)[5]])
        glizzys_file.close()
 
# depreciated
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
 
def new_user(message):
    with open(str(message.guild.id)+".txt", "a") as glizzys_file:
        glizzys_writer = csv.writer(glizzys_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        glizzys_writer.writerow([message.author.name, 0, datetime.datetime.min, 50, datetime.datetime.min, 0, datetime.datetime.min])
        glizzys_file.close()

def update_values(guild, username, glizzys = 0, collect_time = datetime.timedelta(seconds=0), steal_chance = 0, steal_time = datetime.timedelta(seconds=0), milk = 0, hunt_time = datetime.timedelta(seconds=0)):
    current_dict.clear()
    with open(guild+".txt", "r") as glizzys_file:
        glizzys_reader = csv.reader(glizzys_file, delimiter=',')
        for row in glizzys_reader:
            if (len(row) == 7):
                name = row[0]
                if (name == username):
                    glizzys_count = int(row[1]) + glizzys
                    last_collected = datetime.datetime.fromisoformat(row[2]) + collect_time
                    steal_percent = int(row[3]) + steal_chance
                    if (steal_percent > 100):
                        steal_percent = 100
                    elif (steal_percent < 10):
                        steal_percent = 10
                    last_stolen = datetime.datetime.fromisoformat(row[4]) + steal_time
                    glizzy_milk = int(row[5]) + milk
                    last_hunted = datetime.datetime.fromisoformat(row[6]) + hunt_time
                else:
                    glizzys_count = int(row[1])
                    last_collected = datetime.datetime.fromisoformat(row[2])
                    steal_percent = int(row[3])
                    last_stolen = datetime.datetime.fromisoformat(row[4])
                    glizzy_milk = int(row[5])
                    last_hunted = datetime.datetime.fromisoformat(row[6])
                current_dict.update({name:[glizzys_count,last_collected,steal_percent,last_stolen,glizzy_milk,last_hunted]})
        glizzys_file.close()
    with open(guild+".txt", "w") as glizzys_file:
        glizzys_writer = csv.writer(glizzys_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for key in current_dict.keys():
            content = current_dict.get(key)
            glizzys_writer.writerow([key,content[0],content[1],content[2],content[3],content[4],content[5]])
        glizzys_file.close()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
 
@client.event
async def on_message(message):
    if message.author == client.user:
        return

    #FETCH DICTIONARY -> SERVER PROPERTIES
    if message.content.startswith('!'):
        read_prop(str(message.guild.id))

    #HELP (!)
    if message.content.startswith('!help'):
        help_text = "- !help :\t\t\t\t\t\t\t\t\t\t\tDisplay this screen.\n"
        server_text = "- !server :\t\t\t\t\t\t\t\t\t\t  Display whether the Minecraft server setup for monitoring is online.\n"
        players_text = "- !players :\t\t\t\t\t\t\t\t\t\t Display how many players are on the Minecraft server setup for monitoring.\n"
        set_server_text = "- !setserver <name> <ip> <port> :\t\t\t\t\tSet the Minecraft server to monitor. Must provide a name, IP address and port (default is 25565 for Java and 19132 for Bedrock). MUST BE ADMINISTRATOR TO USE!\n"
        role_react_text = "- !rolereact <message link> <emoji> <role name> :\tSet a message to give a certain role when reacted to with a specified emoji. Must provide a link to the message, an emoji, and the name of a role in the server to add to a player (must be below there current highest role). MUST BE ADMINISTRATOR TO USE!\n"
        await message.channel.send(f"**Commands available:**\n```{help_text}{server_text}{players_text}{set_server_text}{role_react_text}```")

    #SET ROLE ON REACTION
    if message.content.startswith('!rolereact'):
        if (message.author.guild_permissions.administrator):
            content = message.content.split()
            if (len(content) < 4):
                await message.channel.send(":x: Command must be in the format '!rolereact <message link> <emoji> <role name>'!")
            else:
                message_location = content[1].split("/")
                if (len(message_location) != 7):
                    await message.channel.send(":x: Please use a message link as the first argument of this command!")
                else:
                    try:
                        message_channel_id = message_location[5]
                        message_id = message_location[6]
                        message_channel = message.guild.get_channel_or_thread(int(message_channel_id))
                        if (message_channel != None):
                            message_to_use = await message_channel.fetch_message(int(message_id))
                        emoji = ascii(content[2])
                        role_list = list()
                        for i in range(3, len(content)):
                            role_list.append(content[i])
                        role_name = " ".join(role_list)
                        role = discord.utils.get(message.guild.roles, name=role_name)
                        if (role == None):
                            await message.channel.send(":x: Please use the name of a valid role as the last argument of this command!")
                        else:
                            update_roles(str(message.guild.id), message_channel_id, message_id, emoji, role_name)
                            await message.channel.send(f":white_check_mark: Successfully set reacting with {content[2]} to the message with ID {message_id} to cause a member to be given {role_name} role.")
                    except (ValueError, discord.errors.NotFound) as error:
                        await message.channel.send(":x: Please use a message link as the first argument of this command!")
                    except TypeError:
                        await message.channel.send(":x: Please use an emoji as the second argument of this command!")
        else:
            await message.channel.send(":x: You must be an administrator on this Discord server to use this command!")

    #SET MC SERVER
    if message.content.startswith('!setserver'):
        if (message.author.guild_permissions.administrator):
            content = message.content.split()
            if (len(content) < 4):
                await message.channel.send(":x: Command must be in the format '!setserver <server name> <server ip> <server port>'!")
            else:
                try:
                    int(content[3])
                    update_server(str(message.guild.id), content[1], content[2], content[3])
                    await message.channel.send(f":white_check_mark: Gekko will now check {content[1]} with the ip {content[2]} and port {content[3]} for any Minecraft status commands.")
                except ValueError:
                    await message.channel.send(f":x: The server port must be numeric! You entered {content[3]}!")
        else:
            await message.channel.send(":x: You must be an administrator on this Discord server to use this command!")
    
    #MC SERVER STATUS
    if message.content.startswith('!server'):
        server_name = server_dict.get("name")
        ip = server_dict.get("ip")
        port = server_dict.get("port")
        if (server_name != None and ip != None and port != None):
            if (checkHost(ip, port)):
                await message.channel.send(f":white_check_mark: {server_name} is up!")
            else:
                await message.channel.send(f":x: {server_name} is down!")
        else:
            await message.channel.send(":x: An admin must set a Minecraft server to check using !setserver.")

    #MC PLAYERS
    if message.content.startswith('!players'):
        server_name = server_dict.get("name")
        ip = server_dict.get("ip")
        port = server_dict.get("port")
        if (server_name != None and ip != None and port != None):
            if (checkHost(ip, port)):
                server = JavaServer.lookup(f"{ip}:{port}", 3)
                online_amount = server.query().players.online
                online_players = server.status().players.sample
                online_names = list()
                if (online_players != None):
                    for player in online_players:
                        online_names.append(player.name)
                names_string = ", ".join(online_names)
                if (online_amount > 0):
                    await message.channel.send(f":smile: There are {online_amount} players online. They are: {names_string}.")
                else:
                    await message.channel.send(":sob: No players are currently online.")
            else:
                await message.channel.send(f":x: {server_name} is down!")
        else:
            await message.channel.send(":x: An admin must set a Minecraft server to check using !setserver.")

    #FETCH DICTIONARY -> GLIZZYS
    if message.content.startswith('$'):
        read_file(str(message.guild.id))
        if message.author.name not in glizzys_dict.keys():
            new_user(message)
    
    #LEADERBOARD
    if message.content.startswith('$leaderboard'):
        leaderboard = dict()
        read_file(str(message.guild.id))
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
        help_text = "- $help :\t\t\t\t\tDisplay this screen.\n"
        collect_text = "- $collect :\t\t\t\t Collect your Glizzys from Gekko. You must collect first in order to join the game. You can perform this command once a day.\n"
        donate_text = "- $donate @user amount :\t Donate a specified amount of Glizzys to the mentioned user.\n"
        steal_text = "- $steal @user :\t\t\t Attempt to rob the mentioned user. A lot like $donate in many ways. You can only steal once every two hours.\n"
        milk_text = "- $milk :\t\t\t\t\tMilk your Glizzys in order to have enough energy to hunt for more. WARNING: some Glizzys might leave in horror.\n"
        hunt_text = "- $hunt :\t\t\t\t\tFollow in the footsteps of Gekko and attempt to hunt for more Glizzys. Costs 1 Glizzy Milk to hunt. You can only hunt once every half an hour.\n"
        leaderboard_text = "- $leaderboard :\t\t\t View the current top five players and their Glizzy count.\n"
        me_text = "- $me :\t\t\t\t\t  View how many Glizzys you have, your chances of successfully stealing and your countdowns for the $collect and $steal commands."
        await message.channel.send(f"**Commands available:**\n```{help_text}{collect_text}{donate_text}{steal_text}{milk_text}{hunt_text}{leaderboard_text}{me_text}```")

    #MILK
    if message.content.startswith('$milk'):
        read_file(str(message.guild.id))
        if glizzys_dict.get(message.author.name)[0] >= 5:
            glizzys_lost = random.randrange(1, 5)
            milk_gained = 1
            for i in range(0, glizzys_lost):
                milk_gained += random.randrange(0, 2)
            update_values(str(message.guild.id),message.author.name,glizzys=(-1)*glizzys_lost,milk=milk_gained)
            new_message = await message.channel.send(":sweat_drops: Washing hands...")
            await asyncio.sleep(1)
            await new_message.edit(content=":notes: Calming Glizzys...")
            await asyncio.sleep(1)
            await new_message.edit(content=f":milk: <@{message.author.id}> successfully milked {glizzys_lost} Glizzys and gained {milk_gained} Glizzy Milk. The milked Glizzys ran away.")
        else:
            await message.channel.send(f":weary: <@{message.author.id}> failed to milk any Glizzys as they don't have enough Glizzys to risk it.")

    #HUNT
    if message.content.startswith('$hunt'):
        hunt_delay = 1800
        read_file(str(message.guild.id))
        if datetime.timedelta(seconds=hunt_delay) <= datetime.datetime.now() - glizzys_dict.get(message.author.name)[5]:
            glizzy_milk = glizzys_dict.get(message.author.name)[4]
            if glizzy_milk >= 1:
                hunt_chance = random.randrange(0,5)
                caught_glizzys = hunt_chance * random.randrange(1,5)
                time_delta = datetime.datetime.now() - glizzys_dict.get(message.author.name)[5]
                update_values(str(message.guild.id),message.author.name,glizzys=caught_glizzys,milk=-1,hunt_time=time_delta)
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
                    update_values(str(message.guild.id),mentioned.name,glizzys=as_int)
                    update_values(str(message.guild.id),message.author.name,glizzys=(-1)*as_int)
                    await message.channel.send(f":sunglasses: <@{message.author.id}> successfully donated {as_int} Glizzys to <@{mentioned.id}>!")
                except ValueError:
                    await message.channel.send(":x: Please input the amount of Glizzys to donate as whole number. E.g. 5.")
       
    #ME
    if message.content.startswith('$me'):
        read_file(str(message.guild.id))
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
        steal_delay = 7200
        min_steal = 1
        max_steal = 20
        read_file(str(message.guild.id))
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
                    odds = random.randrange(1,10)
                    time_delta = datetime.datetime.now() - glizzys_dict.get(message.author.name)[3]
                    update_values(str(message.guild.id),message.author.name,steal_chance=odds,steal_time=time_delta)
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
                    odds = random.randrange(1,20)
                    victim_odds = random.randrange(1,5)
                    time_delta = datetime.datetime.now() - glizzys_dict.get(message.author.name)[3]
                    update_values(str(message.guild.id),mentioned.name,glizzys=(-1)*steal,steal_chance=victim_odds)
                    update_values(str(message.guild.id),message.author.name,glizzys=steal,steal_chance=(-1)*odds,steal_time=time_delta)
                    new_message = await message.channel.send(":busts_in_silhouette: Sneaking up behind target...")
                    await asyncio.sleep(1)
                    await new_message.edit(content=":bubbles: Blinding target...")
                    await asyncio.sleep(1)
                    await new_message.edit(content=":disguised_face: Picking pockets...")
                    await asyncio.sleep(1)
                    await new_message.edit(content=f":spy: <@{message.author.id}> successfully stole {steal} Glizzys from <@{mentioned.id}>!")
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
        read_file(str(message.guild.id))
        if datetime.timedelta(seconds=collect_delay) <= datetime.datetime.now() - glizzys_dict.get(message.author.name)[1]:
            collected = random.randrange(min_collect,max_collect)
            total = glizzys_dict.get(message.author.name)[0] + collected
            time_delta = datetime.datetime.now() - glizzys_dict.get(message.author.name)[1]
            update_values(str(message.guild.id),message.author.name,glizzys=collected,collect_time=time_delta)
            await message.channel.send(f':cyclone: Collected {collected} Glizzys! <@{message.author.id}> now has {total} Glizzys!')
        else:
            total_seconds = (datetime.timedelta(seconds=collect_delay) - (datetime.datetime.now() - glizzys_dict.get(message.author.name)[1])).total_seconds()
            hours = int(total_seconds // (60 * 60))
            minutes = int((total_seconds - (hours * 60 * 60)) // 60)
            seconds = int((total_seconds - (hours * 60 * 60) - (minutes * 60))//1)
            await message.channel.send(f':hourglass: <@{message.author.id}> must wait {hours:02d}:{minutes:02d}:{seconds:02d} until they can collect more Glizzys!')

@client.event
async def on_raw_reaction_add(payload):
    read_prop(str(payload.guild_id))

    for react_role in react_list:
        if (payload.channel_id == int(react_role[0])):
            if (payload.message_id == int(react_role[1])):
                if (ascii(payload.emoji.name) == react_role[2]):
                    role = discord.utils.get(payload.member.guild.roles, name=react_role[3])
                    await payload.member.add_roles(role)

client.run('CENSORED')