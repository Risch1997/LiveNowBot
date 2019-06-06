import requests
import pprint

# This script can be used to get the id of games from Twitch's API.

# Include the name of any games you'd like the ID for in the games array. Max of 100.
games = ["Mega Man Battle Network", "Mega Man Battle Network 2"]

pretty = pprint.PrettyPrinter(indent=4)

clientId = "va1fvp0e01a9v8lm5o3lpwrs92r6i9"
url = "https://api.twitch.tv/helix/games?"

for game in games:
	url = url + "name=" + game + "&"
# Removes the final character, which will be '?' if no games are whitelisted, or '&' if there is at least one
# game whitelisted
url = url[:-1]

response = requests.get(
	url,
	headers={"Client-ID": clientId},
)

pretty.pprint(response.json())