import requests
import discord
from discord.ext import commands
from discord.utils import get
import random
import asyncio

description = '''Discord bot for notifying servers when certain streams go live.'''
bot = commands.Bot(command_prefix='!', description=description)
channel = discord.Object(id="286881621939060739")

# File opens
client_id_file = open("clientid.txt", "r")
token_file = open("token.txt", "r")
games_file_r = open("games.txt", "r")
users_file_r = open("users.txt", "r")
roles_file = open("roles.txt", "r")
games_file_a = open("games.txt", "a")
users_file_a= open("users.txt", "a")

# Be sure to create a clientid.txt file, and include your Twitch API client id in it.
clientId = client_id_file.read()

# Be sure to create token.txt file, and include your Discord bot's token in it.
token = token_file.read()

# Important variables for checking whitelisted games/users/roles
games = games_file_r.read().split()
users = users_file_r.read().split()
roles = roles_file.read().split()
live = []
gamesDict = {}

# Set gamesDict with each game's name per id.
url = "https://api.twitch.tv/helix/games?"

for game in games:
	url = url + "id=" + game + "&"
# Removes the final character, which will be '?' if no games are whitelisted, or '&' if there is at least one
# game whitelisted
url = url[:-1]
	
response = requests.get(
	url,
	headers={"Client-ID": clientId},
)
game_objs = response.json()["data"]
for game in game_objs:
	gamesDict[game["id"]] = game["name"]

#################################################
################ CUSTOMIZATION ##################
#################################################

# Specify which channel the bot should write messages to.
channel = discord.Object(id="286881621939060739")

# Important modes to indicate how you want the bot to operate
# Set Up mode: Will not post live channels so you can set up the games and users whitelist before using the bot for real.
setup = True

# You should also update roles.txt with the Discord role ids for any roles that are allowed to use commands like 
# !add_user and !add_game. If roles.txt is empty, all roles have access to these commands.

#################################################

# Function to check what streams are live. Makes a Twitch Helix API request based on the whitelisted games,
# and gets a list of stream objects in response. Checks each stream to see if the user is whitelisted. If the
# streamer is whitelisted (or no whitelist is specified), adds them to an array of live streamers. If they were
# not already in the array of live streamers, send a message to a specified channel indicating this user is live.
async def checkLive():
	global live
	await bot.wait_until_ready()
	url = "https://api.twitch.tv/helix/streams?"
	
	# Add each game id to the API request URL. If no games are whitelisted, request will pull top 100 streams of
	# any game.
	for game in games:
		url = url + "game_id=" + game + "&"
	# Removes the final character, which will be '?' if no games are whitelisted, or '&' if there is at least one
	# game whitelisted
	url = url[:-1]

	response = requests.get(
		url,
		headers={"Client-ID": clientId},
	)
	streams = response.json()["data"]
	
	# New array to help keep track of when streams end.
	newLive = []
	
	for stream in streams:
		if stream["user_name"] in users or not users and stream["user_name"] not in live:
			message = stream["user_name"] + " is now streaming " + gamesDict[stream["game_id"]] + "!\n\"" + stream["title"] + "\"\nWatch them here: https://twitch.tv/" + stream["user_name"]
			await bot.send_message(channel, message)
			newLive.append(stream["user_name"])
		elif stream["user_name"] in users or not users and stream["user_name"] in live:
			newLive.append(stream["user_name"])
			
	live = newLive
			
	await asyncio.sleep(300)

# Command for adding a user to the whitelist. If any role ids are specified in roles.txt, only those roles can use 
# this command.
@bot.command(pass_context = True)
async def add_user(ctx):
	for role in roles:
		if role in [x.id for x in ctx.message.author.roles]:
			newUsers = ctx.message.content.split()
			for user in newUsers:
				if user != "!add_user" and user not in users:
					print("Adding user: " + user)
					users.append(user)
					users_file_a.write(user + "\n")
					
			await bot.send_message(channel, "Successfully added user(s).")
	
# Command for adding a game to the whitelist. If any role ids are specified in roles.txt, only those roles can use 
# this command.
@bot.command(pass_context = True)
async def add_game(ctx):
	for role in roles:
		if role in [x.id for x in ctx.message.author.roles] :
			message = ctx.message.content.replace("!add_game ", "")
			
			url = "https://api.twitch.tv/helix/games?name=" + message
			response = requests.get(
				url,
				headers={"Client-ID": clientId},
			)
				
			game_id = response.json()["data"][0]["id"]
				
			if game_id not in games:
				print("Adding game: " + game_id)
				games.append(game_id)
				games_file_a.write(game_id + "\n")
					
			await bot.send_message(channel, "Successfully added game: " + message + ".")

# Sets up gamesDict with appropriate key value pairs, and outputs information about the bot on startup.
@bot.event
async def on_ready():
	print('Logged in as')
	print(bot.user.name) 
	print(bot.user.id)
	print('------')


if not setup:
	bot.loop.create_task(checkLive())
bot.run(token)