# Discord TTS Bot

I made a simple discord bot that joins a voice channel and reads messages aloud using Google Text-to-Speech (gTTS). Good for those who cannot speak.

## Features
- Reads messages aloud in a voice channel (`!read <message>` or `!r <message>`).
- Joins your current voice channel (`!join` or `!j`).
- Leaves the voice channel (`!leave` or `!l`).
- Shutdown command for the owner(`!shutdown` or `!s`). This command will SHUTDOWN the bot, making it go offline!
- Help command listing available commands (`!helpme`).

## Requirements
- Python 3.9+
- FFmpeg (installed separately and available in your system PATH)
- A Discord bot token from the [Discord Developer Portal](https://discord.com/developers/applications)

### Python Dependencies
Install dependencies with:

```
pip install -r requirements.txt
```

## Installation

1. Clone the repository:

```
git clone <url>
cd speak-bot
```

2. In case it does not activate a virtual environment automatically:

```
python -m venv venv
source venv/bin/activate   # Linux/macOS
venv\Scripts\activate      # Windows
```

## Configuration

Create a `.env` file in the project root and add:

```
DISCORD_TOKEN=your-bot-token-here
```

## Running the Bot

```
python main.py
```

When ready, the bot will log:

```
YourBotName is ready!
```

## Notes
- The bot automatically deletes the generated `tts_output.mp3` after playback.  
- Make sure the bot has permission to join and speak in your Discord server.