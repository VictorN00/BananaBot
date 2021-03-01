import discord
import json
import re
import random
import shlex
import glob
import smtplib
import time
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from google_images_search import GoogleImagesSearch
from itertools import permutations

CREDENTIALS_FILE = open('credentials.json', 'r')
CREDENTIALS_JSON = json.loads(CREDENTIALS_FILE.read())

PREFIX = CREDENTIALS_JSON['prefix']
TOKEN = CREDENTIALS_JSON['token']
BOT_ID = int(CREDENTIALS_JSON['bot_id'])
OWNER_ID = int(CREDENTIALS_JSON['owner_id'])
BOT_EMAIL = CREDENTIALS_JSON['bot_email']
BOT_EMAIL_PASSWORD = CREDENTIALS_JSON['bot_email_password']
API_KEY = CREDENTIALS_JSON['api_key']
CSE_CX = CREDENTIALS_JSON['cse_cx']

CREDENTIALS_FILE.close()

class BananaClient(discord.Client):
    loaf_perms = [''.join(p) for p in permutations('loaf')]
    
    async def on_ready(self):
        print('Logged on as', self.user)
        await self.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="banana"))
    
    async def on_message(self, message):
        if message.author == self.user or message.author.bot:
            return
        content = message.content
        if len(content) > 0 and content[0] == PREFIX:
            content = content[len(PREFIX):]
            # args = re.split(" +", content)
            args = shlex.split(content)
            noexec = ["on_ready", "on_message", "on_message_edit", "react"]
            if args[0] in noexec:
                return
            convert = {"8ball" : "eightball"}
            cmd_name = convert.get(args[0], args[0])
            command = getattr(self, cmd_name, None)
            if command != None:
                await command(message=message, args=args)
        else:
            await self.react(message)
    
    async def on_message_edit(self, message_old, message_new):
        await self.on_message(message_new)
    
    async def test(self, message, args):
        await message.channel.send("<:michaelreeves:731317531079475291>")
    
    async def help(self, message, args):
        await message.channel.send("help")
            
    async def rogersiq(self, message, args):
        await message.channel.send('Roger has 2000 IQ')
        
    async def iq(self, message, args):
        await message.channel.send("<@!{}>, you have {} IQ.".format(message.author.id, random.randrange(0, 301)))
    
    async def bsay(self, message, args):
        del args[0]
        await message.delete()
        if len(args) == 0:
            await message.channel.send('nothing to say')
        else:
            await message.channel.send(message.content[len('bsay ') + len(PREFIX):])
    
    async def gs(self, message, args):
        del args[0]
        if len(args) == 0:
            await message.channel.send('no text to search')
        else:
            await message.channel.send('https://www.google.com/search?q=' + '+'.join(args))
    
    async def gis(self, message, args):
        """
        try:
            del args[0]
            if len(args) == 0:
                await message.channel.send('no text to search')
                return
            gis = GoogleImagesSearch(API_KEY, CSE_CX)
            gis.search({'q': ' '.join(args), 'num': 20})
            for image in gis.results():
                # image.download('./')
                await message.channel.send(image.url)
                # print(image.url)
        except:
            await message.channel.send('something went wrong')
        """
        del args[0]
        if len(args) == 0:
            await message.channel.send('no text to search')
        else:
            await message.channel.send('https://www.google.com/search?q=' + '+'.join(args) + '&tbm=isch')
            
    async def ys(self, message, args):
        del args[0]
        if len(args) == 0:
            await message.channel.send('no text to search')
        else:
            await message.channel.send("https://www.youtube.com/results?search_query=" + '+'.join(args))
    
    async def join(self, message, args):
        #if message.author.id != OWNER_ID:
         #   return
        if message.author.voice == None:
            await message.channel.send('You are not connected a voice channel in this server!')
            return
        channel = message.author.voice.channel
        connections = self.voice_clients
        for conn in connections:
            if conn.guild.id == message.author.guild.id:
                if conn.channel.id == channel.id:
                    # await message.channel.send('I am already in this voice channel!')
                    if conn.is_playing():
                        conn.stop()
                    conn.play(discord.FFmpegPCMAudio(executable="C:/ffmpeg/bin/ffmpeg.exe", source="Windows Logon.wav"))
                    return
                else:
                    await self.leave(message, args)
                    break
        conn = await channel.connect()
        conn.play(discord.FFmpegPCMAudio(executable="C:/ffmpeg/bin/ffmpeg.exe", source="Windows Logon.wav"))
    
    async def leave(self, message, args, play=True):
        #if message.author.id != OWNER_ID:
         #   return
        connections = self.voice_clients
        for conn in connections:
            if conn.guild.id == message.author.guild.id:
                if conn.is_playing():
                    conn.stop()
                if play:
                    conn.play(discord.FFmpegPCMAudio(executable="C:/ffmpeg/bin/ffmpeg.exe", source="Windows Shutdown.wav"))
                    time.sleep(2.5)
                    """
                    while conn.is_playing():
                        pass
                    """
                await conn.disconnect()
                return
        await message.channel.send('I am not connected to a voice channel in this server!')
    
    async def email(self, message, args):
        try:
            # args = shlex.split(message.content)
            if len(args) <= 1:
                await message.channel.send('too little arguments')
                return
            content = message.content
            receiver = args[1]
            subject = None
            if args[2].startswith('subject='):
                subject = args[2][len('subject='):]
                body = content[content.find('subject=') + len(args[2]) + 2 + 1:] # the plus one is for the space
            else:
                body = content[content.find(args[1]) + len(args[1]) + 1:] # plus one for same reason ^^^
            # body = content[content.find(' ', content.find('subject=') if content.find('subject=') != -1 else content.find(' ') + 1) + 1:]
            # print(body)
            
            smtp = "smtp.gmail.com" 
            port = 587
            server = smtplib.SMTP(smtp,port)
            server.starttls()
            server.login(BOT_EMAIL, BOT_EMAIL_PASSWORD)
            
            msg = MIMEMultipart()
            msg['From'] = BOT_EMAIL
            msg['To'] = receiver
            if subject != None:
                msg['Subject'] = subject
            msg.attach(MIMEText(body, 'plain'))
            msgstr = msg.as_string()
            
            server.sendmail(BOT_EMAIL, re.split(",", receiver), msgstr)
            server.quit()
            
            await message.channel.send('email sent')
        except:
            await message.channel.send('something went wrong')
            # raise
    
    async def box(self, message, args):
        if message.content == "~box":
            await message.channel.send('nothing to box')
            return
        content = message.content[len(PREFIX) + len("box"):] # Discord will remove the space between ~box and the msg
        message_box = ""
        nums = ['zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine']
        for c in content:
            if ord(c) >= 65 and ord(c) <= 90:
                message_box += ":regional_indicator_{}:".format(chr(ord(c) + 32))
            elif ord(c) >= 97 and ord(c) <= 122:
                message_box += ":regional_indicator_{}:".format(c)
            elif ord(c) >= 48 and ord(c) <= 57:
                message_box += ":{}:".format(nums[ord(c) - 48])
            else:
                message_box += c
        await message.delete()
        await message.channel.send(message_box)
        
    async def mra(self, message, args):
        files = glob.glob(".\\mra\\*")
        index = random.randrange(0, len(files))
        await message.channel.send(file=discord.File(files[index]))
    
    async def banana(self, message, args):
        files = glob.glob(".\\banana\\*")
        index = random.randrange(0, len(files))
        await message.channel.send(file=discord.File(files[index]))
        
    async def eightball(self, message, args):
        if message.content == "~8ball":
            await message.channel.send("pls ask a question")
            return
        answers = []
        with open(".\\8ball\\8ball_responses.txt", "r") as file:
            for line in file:
                answers.append(line.strip())
        response = answers[random.randrange(len(answers))]
        await message.channel.send(":8ball: **Question:** {}\n**Answer:** {}".format(message.content[len("~8ball "):], response))
        
    async def pfp(self, message, args):
        mentions = message.mentions
        if len(mentions) == 0:
            await message.channel.send("give me mention")
            return
        for ment in mentions:
            embed = discord.Embed(
              title = ment.nick if not ment.nick == None else ment.name,
              #description = 'hello',
              color = 0xF0E800
            )
            embed.set_image(url=ment.avatar_url)
            await message.channel.send(embed=embed)
            
    async def bruh(self, message, args):
        #if message.author.id != OWNER_ID:
            #   return
        if message.author.voice == None:
            await message.channel.send('You are not connected a voice channel in this server!')
            return
        channel = message.author.voice.channel
        connections = self.voice_clients
        existing = False
        for conn in connections:
            if conn.guild.id == message.author.guild.id:
                if conn.channel.id == channel.id:
                    # await message.channel.send('I am already in this voice channel!')
                    if conn.is_playing():
                        conn.stop()
                    existing = True
                else:
                    await self.leave(message, args)
                    break
        if not existing:
            conn = await channel.connect()
        conn.play(discord.FFmpegPCMAudio(executable="C:/ffmpeg/bin/ffmpeg.exe", source="bruh.mp3"))
        time.sleep(1)
        """
        while conn.is_playing():
            pass
        """
        await self.leave(message, args, False)
    
    async def dm(self, message, args):
        pass
    
    async def react(self, message):
        content = message.content.lower()
        try:
            if "roger" in content:
                await message.add_reaction('<:roger:712156542593400872>')
            if re.compile('.*\\bn+i+c+e+\\b.*').match(content) != None:
                await message.add_reaction('👌')
            if "bread" in content:
                await message.add_reaction('🍞')
            for loaf in self.loaf_perms:
                if loaf in content:
                    await message.add_reaction('🥖')
            if re.compile('.*\\bmo{2,}\\b.*').match(content) != None:
                await message.add_reaction('<:moo2:713848866213986356>')
            if re.compile('.*y+u+h+.*').match(content) != None:
                await message.add_reaction('🗿')
            if "coke" in content:
                await message.add_reaction('<:whitepowder:712157037185728571>')
            if "i love you" in content:
                await message.add_reaction('❤️')
            if "hot" in content or "fire" in content:
                await message.add_reaction('🔥')
            if "doughnut" in content or "donut" in content:
                await message.add_reaction('🍩')
        except:
            print('something went wrong with react')

client = BananaClient()
client.run(TOKEN)
