import discor
import json
import re
import youtube_dl
import smtplib 
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

CREDENTIALS_FILE = open('credentials.json', 'r')
CREDENTIALS_JSON = json.loads(CREDENTIALS_FILE.read())

PREFIX = CREDENTIALS_JSON['prefix']
TOKEN = CREDENTIALS_JSON['token']
BOT_ID = CREDENTIALS_JSON['bot_id']
OWNER_ID = CREDENTIALS_JSON['owner_id']
BOT_EMAIL = CREDENTIALS_JSON['bot_email']
BOT_EMAIL_PASSWORD = CREDENTIALS_JSON['bot_email_password']

CREDENTIALS_FILE.close()

class BananaClient(discord.Client):
    async def on_ready(self):
        print('Logged on as', self.user)
        await self.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="banana"))
    
    async def on_message(self, message):
        if message.author == self.user or message.author.bot:
            return
        content = message.content
        if len(content) > 0 and content[0] == PREFIX:
            content = content[1:]
            args = re.split(" +", content)
            if args[0] == 'rogersiq':
                await self.rogersiq(message)
            elif args[0] == 'bsay':
                await self.bsay(message, args)
            elif args[0] == 'gs':
                await self.gs(message, args)
            elif args[0] == 'gis':
                await self.gis(message, args)
            elif args[0] == 'ys':
                await self.ys(message, args)
            elif args[0] == 'join':
                await self.join(message)
            elif args[0] == 'leave':
                await self.leave(message)
            elif args[0] == 'email':
                await self.email(message, args)
        else:
            await self.react(message)
    
    async def on_message_edit(self, message_old, message_new):
        await self.on_message(message_new)
            
    async def rogersiq(self, message):
        await message.channel.send('Roger has 2000 IQ')
    
    async def bsay(self, message, args):
        del args[0]
        if len(args) == 0:
            await message.channel.send('nothing to say')
        else:
            await message.channel.send(message.content[len('bsay ') + len(PREFIX):])
        await message.delete()
    
    async def gs(self, message, args):
        del args[0]
        if len(args) == 0:
            await message.channel.send('no text to search')
        else:
            await message.channel.send('https://www.google.com/search?q=' + '+'.join(args))
    
    async def gis(self, message, args):
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
    
    async def join(self, message):
        #if message.author.id != OWNER_ID:
         #   return
        voice = message.author.voice
        if voice == None:
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
                    await self.leave(message)
                    break
        conn = await channel.connect()
        conn.play(discord.FFmpegPCMAudio(executable="C:/ffmpeg/bin/ffmpeg.exe", source="Windows Logon.wav"))
    
    async def leave(self, message):
        #if message.author.id != OWNER_ID:
         #   return
        connections = self.voice_clients
        for conn in connections:
            if conn.guild.id == message.author.guild.id:
                if conn.is_playing():
                    conn.stop()
                conn.play(discord.FFmpegPCMAudio(executable="C:/ffmpeg/bin/ffmpeg.exe", source="Windows Shutdown.wav"))
                while conn.is_playing():
                    pass
                await conn.disconnect()
                return
        await message.channel.send('I am not connected to a voice channel in this server!')
    
    async def play(self, message, args):
        del args[0]
        if len(args) == 0:
            message.channel.send('nothing to play')
            return
        connections = self.voice_clients
        for conn in connections:
            if conn.guild.id == message.author.guild.id:
                if conn.is_playing():
                    conn.stop()
                return
        message.channel.send('I am not connected to a voice channel in this server!')
    
    async def email(self, message, args):
        try:
            if len(args) <= 1:
                await message.channel.send('too little arguments')
                return
            content = message.content
            receiver = args[1]
            subject = None
            if args[2].startswith('subject='):
                subject = args[2][len('subject='):]
            body = content[content.find(' ', content.find('subject=') if content.find('subject=') != -1 else content.find(' ') + 1) + 1:]
            
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
    
    async def react(self, message):
        content = message.content.lower()
        try:
            if "roger" in content:
                await message.add_reaction('<:roger:712156542593400872>')
            if re.compile('.*\\bn+i+c+e+\\b.*').match(content) != None:
                await message.add_reaction('👌')
            if "bread" in content:
                await message.add_reaction('🍞')
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
