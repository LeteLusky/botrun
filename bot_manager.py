import discord
from discord.ext import commands
import asyncio
import threading
import logging
import random
import math
import json
import datetime
import re
from typing import Tuple, Dict, Any

class BotManager:
    """Manages Discord bot instances"""
    
    def __init__(self):
        self.bot = None
        self.bot_thread = None
        self.is_bot_running = False
        self.current_token = None
        self.bot_info = {}
        
    def create_bot(self) -> commands.Bot:
        """Create and configure a Discord bot with pre-programmed commands"""
        
        # Set up intents (message content is needed to read commands)
        intents = discord.Intents.default()
        intents.message_content = True
        intents.members = True
        
        # Create bot instance
        bot = commands.Bot(command_prefix='!', intents=intents, help_command=None)
        
        @bot.event
        async def on_ready():
            """Called when the bot is ready"""
            logging.info(f'{bot.user} has connected to Discord!')
            self.bot_info = {
                'name': str(bot.user),
                'id': bot.user.id,
                'guilds': len(bot.guilds),
                'users': sum(guild.member_count for guild in bot.guilds if guild.member_count)
            }
            self.is_bot_running = True
        
        @bot.event
        async def on_disconnect():
            """Called when the bot disconnects"""
            logging.info('Bot disconnected from Discord')
            self.is_bot_running = False
        
        @bot.event
        async def on_message(message):
            """Process messages"""
            # Don't respond to bot messages
            if message.author == bot.user:
                return
            
            # Process commands
            await bot.process_commands(message)
        
        @bot.command(name='ping')
        async def ping_command(ctx):
            """Check if the bot is responsive"""
            latency = round(bot.latency * 1000)
            embed = discord.Embed(
                title="🏓 Pong!",
                description=f"Bot latency: {latency}ms",
                color=0x00ff00
            )
            await ctx.send(embed=embed)
        
        @bot.command(name='help')
        async def help_command(ctx, category=None):
            """Show available commands"""
            if category is None:
                embed = discord.Embed(
                    title="📖 Bot Commands Categories",
                    description="Use `!help <category>` for specific commands",
                    color=0x0099ff
                )
                embed.add_field(name="🛠️ Basic", value="`!help basic`", inline=True)
                embed.add_field(name="🎮 Fun", value="`!help fun`", inline=True)
                embed.add_field(name="🎯 Games", value="`!help games`", inline=True)
                embed.add_field(name="⚙️ Utility", value="`!help utility`", inline=True)
                embed.add_field(name="👤 User", value="`!help user`", inline=True)
                embed.add_field(name="🔧 Tools", value="`!help tools`", inline=True)
                embed.add_field(name="🎲 Random", value="`!help random`", inline=True)
                embed.add_field(name="📊 Math", value="`!help math`", inline=True)
                embed.add_field(name="🔤 Text", value="`!help text`", inline=True)
                embed.add_field(name="🔒 Security", value="`!help security`", inline=True)
                embed.add_field(name="🎵 Music", value="`!help music`", inline=True)
                embed.add_field(name="💰 Economy", value="`!help economy`", inline=True)
                embed.set_footer(text="🎉 Acceso GRATIS a funciones premium durante mantenimiento - ¡Disfrútalo!")
                await ctx.send(embed=embed)
            else:
                category = category.lower()
                embed = discord.Embed(color=0x0099ff)
                
                if category == "basic":
                    embed.title = "🛠️ Basic Commands"
                    embed.add_field(name="!ping", value="Check bot latency", inline=False)
                    embed.add_field(name="!info", value="Show bot information", inline=False)
                    embed.add_field(name="!server", value="Show server information", inline=False)
                    embed.add_field(name="!avatar [@user]", value="Show user's avatar", inline=False)
                elif category == "fun":
                    embed.title = "🎮 Fun Commands"
                    embed.add_field(name="!joke", value="Get a random joke", inline=False)
                    embed.add_field(name="!fact", value="Get a random fact", inline=False)
                    embed.add_field(name="!quote", value="Get an inspirational quote", inline=False)
                    embed.add_field(name="!roast [@user]", value="Roast someone (friendly)", inline=False)
                    embed.add_field(name="!compliment [@user]", value="Give a compliment", inline=False)
                elif category == "games":
                    embed.title = "🎯 Game Commands"
                    embed.add_field(name="!rps <choice>", value="Rock, Paper, Scissors", inline=False)
                    embed.add_field(name="!dice [sides]", value="Roll dice (default 6 sides)", inline=False)
                    embed.add_field(name="!coinflip", value="Flip a coin", inline=False)
                    embed.add_field(name="!8ball <question>", value="Magic 8-ball answers", inline=False)
                    embed.add_field(name="!trivia", value="Random trivia question", inline=False)
                elif category == "utility":
                    embed.title = "⚙️ Utility Commands"
                    embed.add_field(name="!poll <question>", value="Create a yes/no poll", inline=False)
                    embed.add_field(name="!timer <seconds>", value="Set a timer", inline=False)
                    embed.add_field(name="!remind <time> <message>", value="Set reminder (e.g., !remind 5m message)", inline=False)
                    embed.add_field(name="!weather <city>", value="Get weather info", inline=False)
                elif category == "user":
                    embed.title = "👤 User Commands"
                    embed.add_field(name="!userinfo [@user]", value="Get user information", inline=False)
                    embed.add_field(name="!joined [@user]", value="When user joined server", inline=False)
                    embed.add_field(name="!created [@user]", value="When user created account", inline=False)
                elif category == "tools":
                    embed.title = "🔧 Tool Commands"
                    embed.add_field(name="!shorten <url>", value="Create short URL", inline=False)
                    embed.add_field(name="!password [length]", value="Generate secure password", inline=False)
                    embed.add_field(name="!qr <text>", value="Generate QR code", inline=False)
                    embed.add_field(name="!base64 <encode/decode> <text>", value="Base64 encoding/decoding", inline=False)
                elif category == "random":
                    embed.title = "🎲 Random Commands"
                    embed.add_field(name="!random <min> <max>", value="Random number", inline=False)
                    embed.add_field(name="!choose <option1> <option2> ...", value="Choose from options", inline=False)
                    embed.add_field(name="!color", value="Random color", inline=False)
                    embed.add_field(name="!name", value="Random name", inline=False)
                elif category == "math":
                    embed.title = "📊 Math Commands"
                    embed.add_field(name="!calc <expression>", value="Calculate math expressions", inline=False)
                    embed.add_field(name="!convert <value> <from> <to>", value="Unit conversion", inline=False)
                    embed.add_field(name="!fibonacci <n>", value="Fibonacci sequence", inline=False)
                elif category == "text":
                    embed.title = "🔤 Text Commands"
                    embed.add_field(name="!reverse <text>", value="Reverse text", inline=False)
                    embed.add_field(name="!upper <text>", value="Convert to uppercase", inline=False)
                    embed.add_field(name="!lower <text>", value="Convert to lowercase", inline=False)
                    embed.add_field(name="!count <text>", value="Count characters/words", inline=False)
                elif category == "security":
                    embed.title = "🔒 Security/Moderation Commands"
                    embed.add_field(name="!kick [@user] [reason]", value="Kick a user (Admin only)", inline=False)
                    embed.add_field(name="!ban [@user] [reason]", value="Ban a user (Admin only)", inline=False)
                    embed.add_field(name="!unban <user_id>", value="Unban a user (Admin only)", inline=False)
                    embed.add_field(name="!mute [@user] [time]", value="Mute a user (Admin only)", inline=False)
                    embed.add_field(name="!clear <amount>", value="Delete messages (Admin only)", inline=False)
                    embed.add_field(name="!warn [@user] <reason>", value="Warn a user (Admin only)", inline=False)
                elif category == "music":
                    embed.title = "🎵 Music Commands"
                    embed.add_field(name="!play <song>", value="Play music (Demo)", inline=False)
                    embed.add_field(name="!pause", value="Pause music (Demo)", inline=False)
                    embed.add_field(name="!stop", value="Stop music (Demo)", inline=False)
                    embed.add_field(name="!queue", value="Show music queue (Demo)", inline=False)
                elif category == "economy":
                    embed.title = "💰 Economy Commands"
                    embed.add_field(name="!balance [@user]", value="Check coin balance", inline=False)
                    embed.add_field(name="!daily", value="Claim daily coins", inline=False)
                    embed.add_field(name="!give [@user] <amount>", value="Give coins to user", inline=False)
                    embed.add_field(name="!shop", value="View the coin shop", inline=False)
                else:
                    embed.title = "❌ Unknown Category"
                    embed.description = "Use `!help` to see all categories"
                
                await ctx.send(embed=embed)
        
        @bot.command(name='info')
        async def info_command(ctx):
            """Show bot information"""
            embed = discord.Embed(
                title="🤖 Bot Information",
                color=0x9932cc
            )
            embed.add_field(name="Bot Name", value=bot.user.name, inline=True)
            embed.add_field(name="Bot ID", value=bot.user.id, inline=True)
            embed.add_field(name="Servers", value=len(bot.guilds), inline=True)
            
            total_users = sum(guild.member_count for guild in bot.guilds if guild.member_count)
            embed.add_field(name="Total Users", value=total_users, inline=True)
            embed.add_field(name="Latency", value=f"{round(bot.latency * 1000)}ms", inline=True)
            embed.add_field(name="Discord.py Version", value=discord.__version__, inline=True)
            
            embed.set_thumbnail(url=bot.user.avatar.url if bot.user.avatar else bot.user.default_avatar.url)
            embed.set_footer(text="Powered by Discord Bot Runner")
            await ctx.send(embed=embed)
        
        @bot.command(name='server')
        async def server_command(ctx):
            """Show server information"""
            guild = ctx.guild
            if not guild:
                await ctx.send("This command can only be used in a server!")
                return
            
            embed = discord.Embed(
                title=f"🏠 {guild.name}",
                description="Server Information",
                color=0xff6b35
            )
            embed.add_field(name="Server ID", value=guild.id, inline=True)
            embed.add_field(name="Owner", value=guild.owner.mention if guild.owner else "Unknown", inline=True)
            embed.add_field(name="Members", value=guild.member_count, inline=True)
            embed.add_field(name="Text Channels", value=len(guild.text_channels), inline=True)
            embed.add_field(name="Voice Channels", value=len(guild.voice_channels), inline=True)
            embed.add_field(name="Created", value=guild.created_at.strftime("%B %d, %Y"), inline=True)
            
            if guild.icon:
                embed.set_thumbnail(url=guild.icon.url)
            
            await ctx.send(embed=embed)
        
        @bot.event
        async def on_command_error(ctx, error):
            """Handle command errors"""
            if isinstance(error, commands.CommandNotFound):
                embed = discord.Embed(
                    title="❌ Command Not Found",
                    description=f"The command `{ctx.message.content.split()[0]}` was not found.\nUse `!help` to see available commands.",
                    color=0xff0000
                )
                await ctx.send(embed=embed)
            else:
                logging.error(f"Command error: {error}")
                embed = discord.Embed(
                    title="❌ Error",
                    description="An error occurred while executing the command.",
                    color=0xff0000
                )
                await ctx.send(embed=embed)
        
        # =============== FUN COMMANDS ===============
        @bot.command(name='joke')
        async def joke_command(ctx):
            """Get a random joke"""
            jokes = [
                "Why don't scientists trust atoms? Because they make up everything!",
                "Why did the scarecrow win an award? He was outstanding in his field!",
                "Why don't eggs tell jokes? They'd crack each other up!",
                "What do you call a fake noodle? An impasta!",
                "Why did the coffee file a police report? It got mugged!",
                "What's the best thing about Switzerland? I don't know, but the flag is a big plus!",
                "Why don't programmers like nature? It has too many bugs!",
                "How does a penguin build its house? Igloos it together!",
                "What do you call a bear with no teeth? A gummy bear!",
                "Why did the math book look so sad? Because it had too many problems!"
            ]
            embed = discord.Embed(
                title="😂 Random Joke",
                description=random.choice(jokes),
                color=0xffff00
            )
            await ctx.send(embed=embed)
        
        @bot.command(name='fact')
        async def fact_command(ctx):
            """Get a random fact"""
            facts = [
                "Honey never spoils. Archaeologists have found pots of honey in ancient Egyptian tombs that are over 3,000 years old and still perfectly edible.",
                "A group of flamingos is called a 'flamboyance'.",
                "The shortest war in history was between Britain and Zanzibar on August 27, 1896. Zanzibar surrendered after 38 minutes.",
                "Bananas are berries, but strawberries aren't.",
                "A day on Venus is longer than its year.",
                "There are more possible games of chess than there are atoms in the observable universe.",
                "Octopuses have three hearts and blue blood.",
                "The Great Wall of China isn't visible from space with the naked eye.",
                "Sharks have been around longer than trees.",
                "Your brain uses about 20% of your body's total energy."
            ]
            embed = discord.Embed(
                title="🧠 Fun Fact",
                description=random.choice(facts),
                color=0x00ffff
            )
            await ctx.send(embed=embed)
        
        @bot.command(name='quote')
        async def quote_command(ctx):
            """Get an inspirational quote"""
            quotes = [
                "The only way to do great work is to love what you do. - Steve Jobs",
                "Innovation distinguishes between a leader and a follower. - Steve Jobs",
                "Life is what happens to you while you're busy making other plans. - John Lennon",
                "The future belongs to those who believe in the beauty of their dreams. - Eleanor Roosevelt",
                "It is during our darkest moments that we must focus to see the light. - Aristotle",
                "Success is not final, failure is not fatal: it is the courage to continue that counts. - Winston Churchill",
                "The only impossible journey is the one you never begin. - Tony Robbins",
                "In the end, we will remember not the words of our enemies, but the silence of our friends. - Martin Luther King Jr.",
                "The way to get started is to quit talking and begin doing. - Walt Disney",
                "Don't let yesterday take up too much of today. - Will Rogers"
            ]
            embed = discord.Embed(
                title="💭 Inspirational Quote",
                description=random.choice(quotes),
                color=0xff69b4
            )
            await ctx.send(embed=embed)
        
        @bot.command(name='roast')
        async def roast_command(ctx, member: discord.Member = None):
            """Roast someone (friendly)"""
            target = member or ctx.author
            roasts = [
                f"{target.mention} is so bright, they could light up a room... if someone turned off the sun first!",
                f"{target.mention} is like a software update. Whenever I see them, I think 'not now'.",
                f"{target.mention} brings everyone so much joy... when they leave the room!",
                f"{target.mention} is proof that even mistakes can be amazing!",
                f"{target.mention} is like a Monday morning - nobody's happy to see them!",
                f"{target.mention} has a face for radio... and a voice for silent movies!",
                f"{target.mention} is so unique, just like everybody else!",
                f"{target.mention} is living proof that anyone can be extraordinary... extraordinarily ordinary!"
            ]
            embed = discord.Embed(
                title="🔥 Friendly Roast",
                description=random.choice(roasts),
                color=0xff4500
            )
            embed.set_footer(text="Just kidding! You're awesome! 😄")
            await ctx.send(embed=embed)
        
        @bot.command(name='compliment')
        async def compliment_command(ctx, member: discord.Member = None):
            """Give a compliment"""
            target = member or ctx.author
            compliments = [
                f"{target.mention} has an amazing personality that lights up any room!",
                f"{target.mention} is incredibly thoughtful and kind!",
                f"{target.mention} has a great sense of humor that makes everyone smile!",
                f"{target.mention} is such a positive influence on everyone around them!",
                f"{target.mention} is incredibly talented and creative!",
                f"{target.mention} has such a warm and welcoming presence!",
                f"{target.mention} is an amazing friend who always knows what to say!",
                f"{target.mention} is absolutely awesome and deserves all the best things in life!"
            ]
            embed = discord.Embed(
                title="💝 Compliment",
                description=random.choice(compliments),
                color=0x00ff00
            )
            await ctx.send(embed=embed)
        
        # =============== GAME COMMANDS ===============
        @bot.command(name='rps')
        async def rps_command(ctx, choice=None):
            """Rock, Paper, Scissors game"""
            if not choice:
                embed = discord.Embed(
                    title="✋ Rock Paper Scissors",
                    description="Usage: `!rps <rock/paper/scissors>`",
                    color=0xff0000
                )
                await ctx.send(embed=embed)
                return
            
            choice = choice.lower()
            if choice not in ['rock', 'paper', 'scissors']:
                await ctx.send("Choose rock, paper, or scissors!")
                return
            
            bot_choice = random.choice(['rock', 'paper', 'scissors'])
            
            if choice == bot_choice:
                result = "It's a tie!"
                color = 0xffff00
            elif (choice == 'rock' and bot_choice == 'scissors') or \
                 (choice == 'paper' and bot_choice == 'rock') or \
                 (choice == 'scissors' and bot_choice == 'paper'):
                result = "You win! 🎉"
                color = 0x00ff00
            else:
                result = "I win! 😄"
                color = 0xff0000
            
            embed = discord.Embed(
                title="✋ Rock Paper Scissors",
                description=f"You: {choice.title()}\nMe: {bot_choice.title()}\n\n{result}",
                color=color
            )
            await ctx.send(embed=embed)
        
        @bot.command(name='dice')
        async def dice_command(ctx, sides: int = 6):
            """Roll a dice"""
            if sides < 2 or sides > 100:
                await ctx.send("Dice must have between 2 and 100 sides!")
                return
            
            result = random.randint(1, sides)
            embed = discord.Embed(
                title="🎲 Dice Roll",
                description=f"You rolled a {result} on a {sides}-sided dice!",
                color=0x9932cc
            )
            await ctx.send(embed=embed)
        
        @bot.command(name='coinflip')
        async def coinflip_command(ctx):
            """Flip a coin"""
            result = random.choice(['Heads', 'Tails'])
            emoji = '🪙' if result == 'Heads' else '🥈'
            embed = discord.Embed(
                title=f"{emoji} Coin Flip",
                description=f"The coin landed on **{result}**!",
                color=0xffd700
            )
            await ctx.send(embed=embed)
        
        @bot.command(name='8ball')
        async def eight_ball_command(ctx, *, question=None):
            """Magic 8-ball answers"""
            if not question:
                await ctx.send("Ask me a question! Usage: `!8ball <question>`")
                return
            
            responses = [
                "It is certain", "Reply hazy, try again", "Don't count on it",
                "It is decidedly so", "Ask again later", "My reply is no",
                "Without a doubt", "Better not tell you now", "My sources say no",
                "Yes definitely", "Cannot predict now", "Outlook not so good",
                "You may rely on it", "Concentrate and ask again", "Very doubtful",
                "As I see it, yes", "Most likely", "Outlook good", "Yes", "Signs point to yes"
            ]
            
            embed = discord.Embed(
                title="🎱 Magic 8-Ball",
                description=f"**Question:** {question}\n**Answer:** {random.choice(responses)}",
                color=0x000000
            )
            await ctx.send(embed=embed)
        
        @bot.command(name='trivia')
        async def trivia_command(ctx):
            """Random trivia question"""
            trivia_questions = [
                {"q": "What is the capital of Japan?", "a": "Tokyo"},
                {"q": "Which planet is known as the Red Planet?", "a": "Mars"},
                {"q": "What is the largest mammal in the world?", "a": "Blue whale"},
                {"q": "In which year did World War II end?", "a": "1945"},
                {"q": "What is the chemical symbol for gold?", "a": "Au"},
                {"q": "Which ocean is the largest?", "a": "Pacific Ocean"},
                {"q": "What is the smallest country in the world?", "a": "Vatican City"},
                {"q": "Who painted the Mona Lisa?", "a": "Leonardo da Vinci"},
                {"q": "What is the fastest land animal?", "a": "Cheetah"},
                {"q": "How many continents are there?", "a": "7"}
            ]
            
            question = random.choice(trivia_questions)
            embed = discord.Embed(
                title="🧩 Trivia Question",
                description=f"**{question['q']}**",
                color=0x4169e1
            )
            embed.set_footer(text=f"Answer: {question['a']}")
            await ctx.send(embed=embed)
        
        # =============== USER COMMANDS ===============
        @bot.command(name='avatar')
        async def avatar_command(ctx, member: discord.Member = None):
            """Show user's avatar"""
            target = member or ctx.author
            embed = discord.Embed(
                title=f"🖼️ {target.display_name}'s Avatar",
                color=target.color
            )
            embed.set_image(url=target.display_avatar.url)
            await ctx.send(embed=embed)
        
        @bot.command(name='userinfo')
        async def userinfo_command(ctx, member: discord.Member = None):
            """Get user information"""
            target = member or ctx.author
            embed = discord.Embed(
                title=f"👤 User Info: {target.display_name}",
                color=target.color
            )
            embed.set_thumbnail(url=target.display_avatar.url)
            embed.add_field(name="Username", value=target.name, inline=True)
            embed.add_field(name="Discriminator", value=f"#{target.discriminator}", inline=True)
            embed.add_field(name="ID", value=target.id, inline=True)
            embed.add_field(name="Status", value=str(target.status).title(), inline=True)
            embed.add_field(name="Highest Role", value=target.top_role.mention, inline=True)
            embed.add_field(name="Joined Server", value=target.joined_at.strftime("%B %d, %Y"), inline=True)
            embed.add_field(name="Account Created", value=target.created_at.strftime("%B %d, %Y"), inline=True)
            await ctx.send(embed=embed)
        
        @bot.command(name='joined')
        async def joined_command(ctx, member: discord.Member = None):
            """When user joined server"""
            target = member or ctx.author
            embed = discord.Embed(
                title="📅 Join Date",
                description=f"{target.mention} joined on {target.joined_at.strftime('%B %d, %Y at %I:%M %p')}",
                color=0x00ff00
            )
            await ctx.send(embed=embed)
        
        @bot.command(name='created')
        async def created_command(ctx, member: discord.Member = None):
            """When user created account"""
            target = member or ctx.author
            embed = discord.Embed(
                title="🎂 Account Creation",
                description=f"{target.mention}'s account was created on {target.created_at.strftime('%B %d, %Y at %I:%M %p')}",
                color=0x0099ff
            )
            await ctx.send(embed=embed)
        
        # =============== UTILITY COMMANDS ===============
        @bot.command(name='poll')
        async def poll_command(ctx, *, question=None):
            """Create a yes/no poll"""
            if not question:
                await ctx.send("Usage: `!poll <question>`")
                return
            
            embed = discord.Embed(
                title="📊 Poll",
                description=question,
                color=0x0099ff
            )
            embed.set_footer(text=f"Poll created by {ctx.author.display_name}")
            
            message = await ctx.send(embed=embed)
            await message.add_reaction('👍')
            await message.add_reaction('👎')
        
        @bot.command(name='timer')
        async def timer_command(ctx, seconds: int = None):
            """Set a timer"""
            if not seconds or seconds <= 0 or seconds > 3600:
                await ctx.send("Set a timer between 1 and 3600 seconds! Usage: `!timer <seconds>`")
                return
            
            embed = discord.Embed(
                title="⏰ Timer Started",
                description=f"Timer set for {seconds} seconds!",
                color=0xff9900
            )
            await ctx.send(embed=embed)
            
            await asyncio.sleep(seconds)
            
            embed = discord.Embed(
                title="⏰ Timer Finished",
                description=f"{ctx.author.mention} Your {seconds} second timer is done!",
                color=0x00ff00
            )
            await ctx.send(embed=embed)
        
        @bot.command(name='remind')
        async def remind_command(ctx, time_str=None, *, message=None):
            """Set a reminder"""
            if not time_str or not message:
                await ctx.send("Usage: `!remind <time> <message>`\nExample: `!remind 5m Take a break`")
                return
            
            # Parse time string
            time_match = re.match(r'(\d+)([smhd])', time_str.lower())
            if not time_match:
                await ctx.send("Invalid time format! Use: 5s, 10m, 2h, 1d")
                return
            
            amount = int(time_match.group(1))
            unit = time_match.group(2)
            
            if unit == 's':
                seconds = amount
            elif unit == 'm':
                seconds = amount * 60
            elif unit == 'h':
                seconds = amount * 3600
            elif unit == 'd':
                seconds = amount * 86400
            
            if seconds > 86400 * 7:  # Max 1 week
                await ctx.send("Maximum reminder time is 7 days!")
                return
            
            embed = discord.Embed(
                title="⏰ Reminder Set",
                description=f"I'll remind you in {time_str}: {message}",
                color=0xff9900
            )
            await ctx.send(embed=embed)
            
            await asyncio.sleep(seconds)
            
            embed = discord.Embed(
                title="⏰ Reminder",
                description=f"{ctx.author.mention} {message}",
                color=0x00ff00
            )
            await ctx.send(embed=embed)
        
        @bot.command(name='weather')
        async def weather_command(ctx, *, city=None):
            """Get weather info (placeholder)"""
            if not city:
                await ctx.send("Usage: `!weather <city>`")
                return
            
            # This is a placeholder - in a real bot you'd use a weather API
            embed = discord.Embed(
                title=f"🌤️ Weather in {city.title()}",
                description="Weather API integration needed for real data.\nThis is a demo bot!",
                color=0x87ceeb
            )
            embed.add_field(name="Temperature", value="22°C / 72°F", inline=True)
            embed.add_field(name="Condition", value="Partly Cloudy", inline=True)
            embed.add_field(name="Humidity", value="65%", inline=True)
            embed.set_footer(text="Demo data - not real weather!")
            await ctx.send(embed=embed)
        
        # =============== RANDOM COMMANDS ===============
        @bot.command(name='random')
        async def random_command(ctx, min_val: int = 1, max_val: int = 100):
            """Generate random number"""
            if min_val >= max_val:
                await ctx.send("Minimum value must be less than maximum!")
                return
            
            result = random.randint(min_val, max_val)
            embed = discord.Embed(
                title="🎲 Random Number",
                description=f"Random number between {min_val} and {max_val}: **{result}**",
                color=0x9932cc
            )
            await ctx.send(embed=embed)
        
        @bot.command(name='choose')
        async def choose_command(ctx, *choices):
            """Choose from multiple options"""
            if len(choices) < 2:
                await ctx.send("Give me at least 2 options to choose from!")
                return
            
            choice = random.choice(choices)
            embed = discord.Embed(
                title="🎯 Choice Made",
                description=f"I choose: **{choice}**",
                color=0xff6347
            )
            embed.add_field(name="Options were", value=", ".join(choices), inline=False)
            await ctx.send(embed=embed)
        
        @bot.command(name='color')
        async def color_command(ctx):
            """Generate random color"""
            r = random.randint(0, 255)
            g = random.randint(0, 255)
            b = random.randint(0, 255)
            hex_color = f"#{r:02x}{g:02x}{b:02x}"
            
            embed = discord.Embed(
                title="🎨 Random Color",
                description=f"**Hex:** {hex_color}\n**RGB:** ({r}, {g}, {b})",
                color=int(hex_color[1:], 16)
            )
            await ctx.send(embed=embed)
        
        @bot.command(name='name')
        async def name_command(ctx):
            """Generate random name"""
            first_names = ["Alex", "Sam", "Jordan", "Casey", "Riley", "Avery", "Quinn", "Blake", "Cameron", "Devon", "Emery", "Finley", "Harper", "Kai", "Logan", "Sage", "Taylor", "River"]
            last_names = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis", "Rodriguez", "Martinez", "Hernandez", "Lopez", "Gonzalez", "Wilson", "Anderson", "Thomas", "Taylor", "Moore"]
            
            name = f"{random.choice(first_names)} {random.choice(last_names)}"
            embed = discord.Embed(
                title="📝 Random Name",
                description=f"Generated name: **{name}**",
                color=0xdda0dd
            )
            await ctx.send(embed=embed)
        
        # =============== MATH COMMANDS ===============
        @bot.command(name='calc')
        async def calc_command(ctx, *, expression=None):
            """Calculate math expressions"""
            if not expression:
                await ctx.send("Usage: `!calc <expression>`\nExample: `!calc 2 + 2 * 3`")
                return
            
            try:
                # Basic security: only allow certain characters
                allowed_chars = set('0123456789+-*/().^ ')
                if not all(c in allowed_chars for c in expression.replace(' ', '')):
                    await ctx.send("Invalid characters in expression!")
                    return
                
                # Replace ^ with ** for power
                expression = expression.replace('^', '**')
                
                result = eval(expression)
                embed = discord.Embed(
                    title="🧮 Calculator",
                    description=f"**Expression:** {expression}\n**Result:** {result}",
                    color=0x32cd32
                )
                await ctx.send(embed=embed)
            except:
                await ctx.send("Invalid math expression!")
        
        @bot.command(name='fibonacci')
        async def fibonacci_command(ctx, n: int = None):
            """Generate fibonacci sequence"""
            if not n or n <= 0 or n > 20:
                await ctx.send("Please provide a number between 1 and 20!")
                return
            
            fib = [0, 1]
            for i in range(2, n):
                fib.append(fib[i-1] + fib[i-2])
            
            sequence = ', '.join(map(str, fib[:n]))
            embed = discord.Embed(
                title="🔢 Fibonacci Sequence",
                description=f"First {n} numbers: {sequence}",
                color=0xffd700
            )
            await ctx.send(embed=embed)
        
        # =============== TEXT COMMANDS ===============
        @bot.command(name='reverse')
        async def reverse_command(ctx, *, text=None):
            """Reverse text"""
            if not text:
                await ctx.send("Usage: `!reverse <text>`")
                return
            
            reversed_text = text[::-1]
            embed = discord.Embed(
                title="🔄 Text Reverser",
                description=f"**Original:** {text}\n**Reversed:** {reversed_text}",
                color=0x40e0d0
            )
            await ctx.send(embed=embed)
        
        @bot.command(name='upper')
        async def upper_command(ctx, *, text=None):
            """Convert to uppercase"""
            if not text:
                await ctx.send("Usage: `!upper <text>`")
                return
            
            embed = discord.Embed(
                title="🔠 Uppercase",
                description=f"**Original:** {text}\n**Uppercase:** {text.upper()}",
                color=0xff7f50
            )
            await ctx.send(embed=embed)
        
        @bot.command(name='lower')
        async def lower_command(ctx, *, text=None):
            """Convert to lowercase"""
            if not text:
                await ctx.send("Usage: `!lower <text>`")
                return
            
            embed = discord.Embed(
                title="🔡 Lowercase",
                description=f"**Original:** {text}\n**Lowercase:** {text.lower()}",
                color=0x98fb98
            )
            await ctx.send(embed=embed)
        
        @bot.command(name='count')
        async def count_command(ctx, *, text=None):
            """Count characters and words"""
            if not text:
                await ctx.send("Usage: `!count <text>`")
                return
            
            char_count = len(text)
            word_count = len(text.split())
            
            embed = discord.Embed(
                title="📊 Text Counter",
                description=f"**Text:** {text}",
                color=0xdda0dd
            )
            embed.add_field(name="Characters", value=char_count, inline=True)
            embed.add_field(name="Words", value=word_count, inline=True)
            await ctx.send(embed=embed)
        
        # =============== TOOL COMMANDS ===============
        @bot.command(name='password')
        async def password_command(ctx, length: int = 12):
            """Generate secure password"""
            if length < 4 or length > 50:
                await ctx.send("Password length must be between 4 and 50 characters!")
                return
            
            import string
            chars = string.ascii_letters + string.digits + "!@#$%^&*"
            password = ''.join(random.choice(chars) for _ in range(length))
            
            embed = discord.Embed(
                title="🔐 Password Generator",
                description=f"Generated password: `{password}`",
                color=0xff6b6b
            )
            embed.set_footer(text="Keep this password safe!")
            await ctx.send(embed=embed)
        
        @bot.command(name='base64')
        async def base64_command(ctx, operation=None, *, text=None):
            """Base64 encode/decode"""
            if not operation or not text:
                await ctx.send("Usage: `!base64 <encode/decode> <text>`")
                return
            
            import base64
            try:
                if operation.lower() == 'encode':
                    result = base64.b64encode(text.encode()).decode()
                    title = "📤 Base64 Encode"
                elif operation.lower() == 'decode':
                    result = base64.b64decode(text.encode()).decode()
                    title = "📥 Base64 Decode"
                else:
                    await ctx.send("Operation must be 'encode' or 'decode'!")
                    return
                
                embed = discord.Embed(
                    title=title,
                    description=f"**Input:** {text}\n**Output:** {result}",
                    color=0x6495ed
                )
                await ctx.send(embed=embed)
            except:
                await ctx.send("Invalid input for base64 operation!")
        
        # =============== SECURITY/MODERATION COMMANDS ===============
        @bot.command(name='kick')
        @commands.has_permissions(kick_members=True)
        async def kick_command(ctx, member: discord.Member = None, *, reason="No reason provided"):
            """Kick a user from the server"""
            if not member:
                await ctx.send("Please specify a user to kick!")
                return
            
            if member.top_role >= ctx.author.top_role:
                await ctx.send("You cannot kick someone with a higher or equal role!")
                return
            
            try:
                await member.kick(reason=reason)
                embed = discord.Embed(
                    title="👢 User Kicked",
                    description=f"{member.mention} has been kicked from the server.",
                    color=0xff6b35
                )
                embed.add_field(name="Reason", value=reason, inline=False)
                embed.add_field(name="Moderator", value=ctx.author.mention, inline=True)
                await ctx.send(embed=embed)
            except discord.Forbidden:
                await ctx.send("I don't have permission to kick this user!")
        
        @bot.command(name='ban')
        @commands.has_permissions(ban_members=True)
        async def ban_command(ctx, member: discord.Member = None, *, reason="No reason provided"):
            """Ban a user from the server"""
            if not member:
                await ctx.send("Please specify a user to ban!")
                return
            
            if member.top_role >= ctx.author.top_role:
                await ctx.send("You cannot ban someone with a higher or equal role!")
                return
            
            try:
                await member.ban(reason=reason)
                embed = discord.Embed(
                    title="🔨 User Banned",
                    description=f"{member.mention} has been banned from the server.",
                    color=0xff0000
                )
                embed.add_field(name="Reason", value=reason, inline=False)
                embed.add_field(name="Moderator", value=ctx.author.mention, inline=True)
                await ctx.send(embed=embed)
            except discord.Forbidden:
                await ctx.send("I don't have permission to ban this user!")
        
        @bot.command(name='unban')
        @commands.has_permissions(ban_members=True)
        async def unban_command(ctx, user_id: int = None):
            """Unban a user from the server"""
            if not user_id:
                await ctx.send("Please provide a user ID to unban!")
                return
            
            try:
                user = await bot.fetch_user(user_id)
                await ctx.guild.unban(user)
                embed = discord.Embed(
                    title="✅ User Unbanned",
                    description=f"{user.mention} has been unbanned from the server.",
                    color=0x00ff00
                )
                embed.add_field(name="Moderator", value=ctx.author.mention, inline=True)
                await ctx.send(embed=embed)
            except:
                await ctx.send("Could not unban that user!")
        
        @bot.command(name='clear')
        @commands.has_permissions(manage_messages=True)
        async def clear_command(ctx, amount: int = None):
            """Clear messages from the channel"""
            if not amount or amount <= 0 or amount > 100:
                await ctx.send("Please specify a number between 1 and 100!")
                return
            
            deleted = await ctx.channel.purge(limit=amount + 1)
            embed = discord.Embed(
                title="🧹 Messages Cleared",
                description=f"Deleted {len(deleted) - 1} messages from {ctx.channel.mention}",
                color=0x00ff00
            )
            embed.add_field(name="Moderator", value=ctx.author.mention, inline=True)
            
            msg = await ctx.send(embed=embed)
            await asyncio.sleep(5)
            await msg.delete()
        
        @bot.command(name='warn')
        @commands.has_permissions(manage_messages=True)
        async def warn_command(ctx, member: discord.Member = None, *, reason="No reason provided"):
            """Warn a user"""
            if not member:
                await ctx.send("Please specify a user to warn!")
                return
            
            embed = discord.Embed(
                title="⚠️ User Warning",
                description=f"{member.mention} has been warned.",
                color=0xffa500
            )
            embed.add_field(name="Reason", value=reason, inline=False)
            embed.add_field(name="Moderator", value=ctx.author.mention, inline=True)
            await ctx.send(embed=embed)
            
            try:
                dm_embed = discord.Embed(
                    title="⚠️ Warning",
                    description=f"You have been warned in {ctx.guild.name}",
                    color=0xffa500
                )
                dm_embed.add_field(name="Reason", value=reason, inline=False)
                await member.send(embed=dm_embed)
            except:
                pass
        
        # =============== MUSIC COMMANDS (Demo) ===============
        @bot.command(name='play')
        async def play_command(ctx, *, song=None):
            """Play music (Demo)"""
            if not song:
                await ctx.send("Please specify a song to play!")
                return
            
            embed = discord.Embed(
                title="🎵 Now Playing (Demo)",
                description=f"**{song}**",
                color=0x1db954
            )
            embed.add_field(name="Duration", value="3:45", inline=True)
            embed.add_field(name="Requested by", value=ctx.author.mention, inline=True)
            embed.set_footer(text="🎉 Función premium disponible GRATIS durante mantenimiento!")
            await ctx.send(embed=embed)
        
        @bot.command(name='pause')
        async def pause_command(ctx):
            """Pause music (Demo)"""
            embed = discord.Embed(
                title="⏸️ Music Paused",
                description="Music playback has been paused.",
                color=0xffa500
            )
            embed.set_footer(text="🎉 Función premium disponible GRATIS durante mantenimiento!")
            await ctx.send(embed=embed)
        
        @bot.command(name='stop')
        async def stop_command(ctx):
            """Stop music (Demo)"""
            embed = discord.Embed(
                title="⏹️ Music Stopped",
                description="Music playback has been stopped.",
                color=0xff0000
            )
            embed.set_footer(text="🎉 Función premium disponible GRATIS durante mantenimiento!")
            await ctx.send(embed=embed)
        
        @bot.command(name='queue')
        async def queue_command(ctx):
            """Show music queue (Demo)"""
            embed = discord.Embed(
                title="🎵 Music Queue",
                description="**Now Playing:** Demo Song - 3:45\n\n**Up Next:**\n1. Another Demo Song - 4:12\n2. Third Demo Song - 2:58",
                color=0x1db954
            )
            embed.set_footer(text="🎉 Sistema de música premium disponible GRATIS!")
            await ctx.send(embed=embed)
        
        # =============== ECONOMY COMMANDS ===============
        user_balances = {}  # Simple in-memory storage
        daily_claims = {}
        
        @bot.command(name='balance')
        async def balance_command(ctx, member: discord.Member = None):
            """Check coin balance"""
            target = member or ctx.author
            balance = user_balances.get(target.id, 0)
            
            embed = discord.Embed(
                title="💰 Coin Balance",
                description=f"{target.mention} has **{balance}** coins!",
                color=0xffd700
            )
            await ctx.send(embed=embed)
        
        @bot.command(name='daily')
        async def daily_command(ctx):
            """Claim daily coins"""
            user_id = ctx.author.id
            today = datetime.datetime.now().date()
            
            if user_id in daily_claims and daily_claims[user_id] == today:
                embed = discord.Embed(
                    title="💰 Daily Reward",
                    description="You've already claimed your daily reward today! Come back tomorrow.",
                    color=0xff0000
                )
                await ctx.send(embed=embed)
                return
            
            reward = random.randint(50, 200)
            user_balances[user_id] = user_balances.get(user_id, 0) + reward
            daily_claims[user_id] = today
            
            embed = discord.Embed(
                title="💰 Daily Reward Claimed!",
                description=f"You received **{reward}** coins!\nNew balance: **{user_balances[user_id]}** coins",
                color=0x00ff00
            )
            await ctx.send(embed=embed)
        
        @bot.command(name='give')
        async def give_command(ctx, member: discord.Member = None, amount: int = None):
            """Give coins to another user"""
            if not member or not amount:
                await ctx.send("Usage: `!give @user <amount>`")
                return
            
            if amount <= 0:
                await ctx.send("Amount must be positive!")
                return
            
            if member == ctx.author:
                await ctx.send("You can't give coins to yourself!")
                return
            
            sender_balance = user_balances.get(ctx.author.id, 0)
            if sender_balance < amount:
                await ctx.send("You don't have enough coins!")
                return
            
            user_balances[ctx.author.id] = sender_balance - amount
            user_balances[member.id] = user_balances.get(member.id, 0) + amount
            
            embed = discord.Embed(
                title="💰 Coins Transferred",
                description=f"{ctx.author.mention} gave **{amount}** coins to {member.mention}!",
                color=0x00ff00
            )
            await ctx.send(embed=embed)
        
        @bot.command(name='shop')
        async def shop_command(ctx):
            """View the coin shop"""
            embed = discord.Embed(
                title="🛒 Coin Shop",
                description="Welcome to the coin shop! (Demo)",
                color=0x9932cc
            )
            embed.add_field(name="🎭 Custom Role", value="500 coins", inline=True)
            embed.add_field(name="🏆 VIP Status", value="1000 coins", inline=True)
            embed.add_field(name="🌟 Special Badge", value="750 coins", inline=True)
            embed.set_footer(text="🎉 Tienda premium disponible GRATIS durante mantenimiento!")
            await ctx.send(embed=embed)
        
        # =============== MORE GAMES ===============
        @bot.command(name='hangman')
        async def hangman_command(ctx):
            """Play hangman"""
            words = ["python", "discord", "computer", "programming", "challenge", "amazing", "awesome", "fantastic"]
            word = random.choice(words).upper()
            guessed = ["_"] * len(word)
            
            embed = discord.Embed(
                title="🎮 Hangman Game",
                description=f"Word: {' '.join(guessed)}\nTries left: 6\n\nGuess letters by typing them!",
                color=0x9932cc
            )
            embed.set_footer(text=f"Answer: {word} - This is a simplified demo version!")
            await ctx.send(embed=embed)
        
        @bot.command(name='wordguess')
        async def wordguess_command(ctx):
            """Guess the scrambled word"""
            words = {"PYTHON": "NYTHOP", "DISCORD": "CDODSIR", "COMPUTER": "PMOCTURE", "PROGRAMMING": "GRAMPGMORIN"}
            word, scrambled = random.choice(list(words.items()))
            
            embed = discord.Embed(
                title="🔤 Word Scramble",
                description=f"Unscramble this word: **{scrambled}**",
                color=0xff6347
            )
            embed.set_footer(text=f"Answer: {word}")
            await ctx.send(embed=embed)
        
        @bot.command(name='numguess')
        async def numguess_command(ctx):
            """Number guessing game"""
            number = random.randint(1, 100)
            embed = discord.Embed(
                title="🔢 Number Guessing Game",
                description="I'm thinking of a number between 1 and 100!\nTry to guess it!",
                color=0x32cd32
            )
            embed.set_footer(text=f"The number was: {number}")
            await ctx.send(embed=embed)
        
        # =============== MORE UTILITY COMMANDS ===============
        @bot.command(name='qr')
        async def qr_command(ctx, *, text=None):
            """Generate QR code (placeholder)"""
            if not text:
                await ctx.send("Usage: `!qr <text>`")
                return
            
            embed = discord.Embed(
                title="📱 QR Code Generator",
                description=f"QR code for: **{text}**\n\n(Real QR generation requires additional libraries)",
                color=0x000000
            )
            embed.set_footer(text="🎉 Generador QR premium disponible GRATIS durante mantenimiento!")
            await ctx.send(embed=embed)
        
        @bot.command(name='shorten')
        async def shorten_command(ctx, url=None):
            """Create short URL (placeholder)"""
            if not url:
                await ctx.send("Usage: `!shorten <url>`")
                return
            
            short_id = ''.join(random.choices('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=6))
            
            embed = discord.Embed(
                title="🔗 URL Shortener",
                description=f"**Original:** {url}\n**Shortened:** https://short.ly/{short_id}",
                color=0x0099ff
            )
            embed.set_footer(text="🎉 Acortador de URLs premium disponible GRATIS durante mantenimiento!")
            await ctx.send(embed=embed)
        
        @bot.command(name='convert')
        async def convert_command(ctx, value=None, from_unit=None, to_unit=None):
            """Unit conversion (basic)"""
            if not all([value, from_unit, to_unit]):
                await ctx.send("Usage: `!convert <value> <from_unit> <to_unit>`\nExample: `!convert 100 cm m`")
                return
            
            try:
                val = float(value)
            except:
                await ctx.send("Invalid number!")
                return
            
            # Simple conversions
            conversions = {
                ("cm", "m"): 0.01,
                ("m", "cm"): 100,
                ("kg", "lb"): 2.20462,
                ("lb", "kg"): 0.453592,
                ("c", "f"): lambda x: x * 9/5 + 32,
                ("f", "c"): lambda x: (x - 32) * 5/9
            }
            
            key = (from_unit.lower(), to_unit.lower())
            if key in conversions:
                factor = conversions[key]
                if callable(factor):
                    result = factor(val)
                else:
                    result = val * factor
                
                embed = discord.Embed(
                    title="🔄 Unit Converter",
                    description=f"**{val} {from_unit}** = **{result:.2f} {to_unit}**",
                    color=0x32cd32
                )
                await ctx.send(embed=embed)
            else:
                await ctx.send("Conversion not supported! Try: cm↔m, kg↔lb, c↔f")
        
        return bot
    
    def run_bot(self, token: str):
        """Run the bot in an asyncio event loop"""
        try:
            # Create new event loop for this thread
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
            # Create bot instance
            self.bot = self.create_bot()
            
            # Run the bot
            loop.run_until_complete(self.bot.start(token))
        except discord.LoginFailure:
            logging.error("Invalid Discord bot token")
            self.is_bot_running = False
        except discord.HTTPException as e:
            logging.error(f"HTTP exception: {e}")
            self.is_bot_running = False
        except Exception as e:
            logging.error(f"Bot error: {e}")
            self.is_bot_running = False
        finally:
            self.is_bot_running = False
    
    def start_bot(self, token: str) -> Tuple[bool, str]:
        """Start the Discord bot with the given token"""
        if self.is_bot_running:
            return False, "Bot is already running"
        
        try:
            # Validate token format (basic check)
            if not token or len(token.strip()) < 50:
                return False, "Invalid token format"
            
            self.current_token = token.strip()
            
            # Start bot in a separate thread
            self.bot_thread = threading.Thread(
                target=self.run_bot,
                args=(self.current_token,),
                daemon=True
            )
            self.bot_thread.start()
            
            # Give it a moment to start
            import time
            time.sleep(2)
            
            if self.bot_thread.is_alive():
                return True, "Bot started successfully"
            else:
                return False, "Failed to start bot - check token validity"
                
        except Exception as e:
            logging.error(f"Error starting bot: {e}")
            return False, f"Error: {str(e)}"
    
    def stop_bot(self) -> Tuple[bool, str]:
        """Stop the running Discord bot"""
        if not self.is_bot_running and not self.bot_thread:
            return False, "No bot is currently running"
        
        try:
            if self.bot:
                # Create a task to close the bot
                if hasattr(self.bot, 'loop') and self.bot.loop:
                    asyncio.run_coroutine_threadsafe(self.bot.close(), self.bot.loop)
                
            # Wait for thread to finish (with timeout)
            if self.bot_thread and self.bot_thread.is_alive():
                self.bot_thread.join(timeout=5)
            
            # Reset state
            self.is_bot_running = False
            self.bot = None
            self.bot_thread = None
            self.current_token = None
            self.bot_info = {}
            
            return True, "Bot stopped successfully"
            
        except Exception as e:
            logging.error(f"Error stopping bot: {e}")
            # Force reset state even if there was an error
            self.is_bot_running = False
            self.bot = None
            self.bot_thread = None
            self.current_token = None
            self.bot_info = {}
            return False, f"Error stopping bot: {str(e)}"
    
    def is_running(self) -> bool:
        """Check if the bot is currently running"""
        return self.is_bot_running and (self.bot_thread and self.bot_thread.is_alive())
    
    def get_status(self) -> Dict[str, Any]:
        """Get current bot status and information"""
        return {
            'running': self.is_running(),
            'info': self.bot_info if self.is_running() else {},
            'has_token': bool(self.current_token)
        }
