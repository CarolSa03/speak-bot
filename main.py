import discord
from discord.ext import commands
import logging
from dotenv import load_dotenv
from gtts import gTTS
from discord import FFmpegPCMAudio
import os

load_dotenv()
token = os.getenv('DISCORD_TOKEN')

handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.voice_states = True
intents.presences = True

bot = commands.Bot(command_prefix='!', intents=intents)


@bot.event
async def on_ready():
    print(f"We are ready to go in, {bot.user.name}")


@bot.command()
async def call(ctx):
    if ctx.author.voice:
        channel = ctx.author.voice.channel
        try:
            if ctx.voice_client is not None:
                await ctx.voice_client.move_to(channel)
                await ctx.send(f"Moved to {channel.name}")
            else:
                voice_client = await channel.connect()
                if voice_client:
                    await ctx.send(f"Joined {channel.name}")
                else:
                    await ctx.send("Failed to join the voice channel.")
        except Exception as e:
            await ctx.send(f"Error connecting to voice: {e}")
            print(f"Error connecting to voice: {e}")
    else:
        await ctx.send("You are not connected to a voice channel.")


@bot.command()
async def read(ctx, *, message: str):
    await ctx.send("Starting text-to-speech process...")  # Debug message

    if ctx.voice_client is None:
        if ctx.author.voice:
            channel = ctx.author.voice.channel
            await ctx.send(f"Bot not connected. Connecting to {channel.name}...")  # Debug message
            await channel.connect()
        else:
            await ctx.send("You need to be in a voice channel or use !call first!")
            return

    try:
        await ctx.send("Generating TTS audio...")
        tts = gTTS(text=message, lang='en')
        tts.save("tts_output.mp3")
        await ctx.send("TTS audio generated successfully.")

        source = FFmpegPCMAudio('tts_output.mp3')
        voice_client = ctx.voice_client

        if voice_client.is_playing():
            voice_client.stop()
            await ctx.send("Stopped previous audio.")

        voice_client.play(source)
        await ctx.send(f"Speaking: {message}")

    except Exception as e:
        await ctx.send(f"Error during TTS or playback: {e}")
        print(f"[ERROR] {e}")

bot.run(token, log_handler=handler, log_level=logging.DEBUG)
