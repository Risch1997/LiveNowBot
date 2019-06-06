# LiveNowBot
A Python Discord bot to let people know when certain channels go live.

## How to set up
Before using the bot, perform the following setup.
1. Create a clientid.txt file with a valid Client ID for a Twitch application.
1. Create a token.txt with a valid Discord bot token.
1. Update livenow.py line 56 with the channel ID you want the bot to send messages to.
1. (Optional) If you want select roles to have access to commands such as !add_user and !add_game, update roles.txt with role ids from Discord. Each role id should be on a separate line.
1. (Optional) Run the bot with the setup mode equal to True. This will allow you to setup the game and user whitelists easily using the !add_user and !add_game commands without the bot spamming live now messages on first start up.

## How to use
Requires at least Python 3.6.0 (Have not yet tested with newer versions of Python).

Run the following command to start the bot:
* python livenow.py
  
The bot will immediately check for all live streams based on the user and games whitelist, and post messages to the appropriate channel. It will then check every 5 minutes to see who is live, and send messages anytime a new channel has gone live.

## Commands
* !add_user: Adds 1 or more users to the user whitelist. If the user whitelist is empty, all streams will be considered whitelisted. Example usage: !add_user Account1 Account2 Account3 ...
* !add_game: Adds a game from the Twitch directory to the games whitelist. If the game whitelist is empty, all games will be considered whitelisted. Example usage: !add_game Example Game

### TestGame.py
TestGame.py is a script that can be used as an alternative method to getting game IDs from the Twitch API to add to the game whitelist. Simply update the games array on line 7 with the games you'd like to get the IDs for, and run "python testGame.py" to get an output of each game object from the Twitch API.
