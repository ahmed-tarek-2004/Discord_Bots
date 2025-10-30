import discord
from discord.ext import commands , tasks
import logging
from dotenv import load_dotenv
import os

load_dotenv()
token = os.getenv('DISCORD_TOKEN')

handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)

secret_role = "Gamer"

@bot.event
async def on_ready():
    print(f"bot now is ready, {bot.user.name}")
    channel = bot.get_channel(1201678020235251735) 
    if channel:
        await channel.send("🤖 استعنا علي الشقي بالله... معانا يارب ")
    send_message.start()

@bot.event
async def on_member_join(member):
     channel = discord.utils.get(member.guild.text_channels, name="general")
     await member.send(f"Welcome to the server {member.name}")
     if channel:
         await channel.send(f"اهلا بيك ياخويا في العالم بتاعنا, {member.mention}!")
     else:
         print(f"No channel named 'general' found in {member.guild.name}")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if "shit" in message.content.lower():
        await message.delete()
        await message.channel.send(f"{message.author.mention} - dont use that word!")
    elif "صل علي النبي" in message.content.lower() or "صلي علي النبي" in message.content.lower():
        await message.channel.send(f"عليه الصلاة و السلام")
    await bot.process_commands(message)


@tasks.loop(minutes=60)  
async def send_message():
    channel = bot.get_channel(1201678020235251735)
    print("Starting loop")
    if channel:
        await channel.send("صلوا علي النبي ياخوانا @everyone ")


@bot.command()
async def hello(ctx):
    await ctx.send(f"Hello {ctx.author.mention}!")

@bot.command()
async def assign(ctx):
    role = discord.utils.get(ctx.guild.roles, name=secret_role)
    if role:
        await ctx.author.add_roles(role)
        await ctx.send(f"{ctx.author.mention} is now assigned to {secret_role}")
    else:
        await ctx.send("Role doesn't exist")

@bot.command()
async def remove(ctx):
    role = discord.utils.get(ctx.guild.roles, name=secret_role)
    if role:
        await ctx.author.remove_roles(role)
        await ctx.send(f"{ctx.author.mention} has had the {secret_role} removed")
    else:
        await ctx.send("Role doesn't exist")

@bot.command()
async def dm(ctx, *, msg):
    await ctx.author.send(f"You said {msg}")

@bot.command()
async def reply(ctx):
    await ctx.reply("This is a reply to your message!")

@bot.command()
async def poll(ctx, *, question):
    embed = discord.Embed(title="New Poll", description=question)
    poll_message = await ctx.send(embed=embed)
    await poll_message.add_reaction("👍")
    await poll_message.add_reaction("👎")

@bot.command()
@commands.has_role(secret_role)
async def secret(ctx):
    await ctx.send("Welcome to the club!")

@secret.error
async def secret_error(ctx, error):
    if isinstance(error, commands.MissingRole):
        await ctx.send("You do not have permission to do that!")

bot.run(token, log_handler=handler, log_level=logging.DEBUG)