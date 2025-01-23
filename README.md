# Tubetinho Bot
## DISCLAIMER
### This bot is not intended to be used in commercial context. I never wanted to infringe any youtube or google policy. Use at your own risk.

Tubetinho is a Discord bot that allows users to play and skip YouTube music within a voice channel. This bot uses the commands `play`, `skip`, `stop`, `loop` and `queue_` to manage music playback.

Please note that Tubetinho is a Discord bot that requires a host computer to function. The bot will run continuously on the host computer and must be connected to the internet in order to function properly. Additionally, depending on the usage of the bot, the host computer may require adequate processing power and memory to handle the tasks performed by the bot. It is recommended to host the bot on a dedicated server or on a computer that is capable of running the bot without impacting other tasks.

## Getting Started

To use Tubetinho, you will need to access Discord developer portal and create a new application, in the application page, copy the token provided and invite it to your server. Additionally, the bot requires Python and FFMPEG to be installed on your system.

Once you have the necessary token and the bot created, follow these steps to get started:

1.  Clone the repository and navigate to the bot folder.
2.  Open the `bot.py` file and replace `TOKEN` with your Discord bot's token.
3.  Open the `files.py` file and replace `PATH_TO_BOT_FOLDER` with the file path to the bot folder on your system.
4.  Install the required libraries using the following command:

`pip install -r requirements` 

5.  Start the bot using the following command:

`python bot.py` 

6.  Create a voice channel and join that channel.
7.  Use the `/play` command followed by a YouTube link or a song title to begin playing music in the voice channel.

## Commands

Here is a list of available commands:

-   `/play [query]`: Plays the audio from the provided YouTube song or link in the voice channel.
-   `/skip`: Skips the current song and plays the next song in the queue.
-   `/queue_`: Displays the number of song in the queue.
-   `/stop`: Stops the current song and clears the song queue.
-   `/loop [query]` : Plays the song provided in the command endlessly until the 'stop' comand is used.
