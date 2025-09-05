import os
import logging
import discord
from discord.ext import commands
from discord import FFmpegPCMAudio
from gtts import gTTS
from dotenv import load_dotenv


load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

handler = logging.FileHandler(
    filename="discord.log",
    encoding="utf-8",
    mode="w"
)

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.voice_states = True
intents.presences = True

bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    print(f"{bot.user.name} is ready!")


@bot.command(name="join", aliases=["j"])
async def call(ctx):
    if ctx.author.voice:
        channel = ctx.author.voice.channel
        try:
            if ctx.voice_client:
                await ctx.voice_client.move_to(channel)
                await ctx.send(f"Moved to {channel.name}")
            else:
                await channel.connect()
                await ctx.send(f"Joined {channel.name}")
        except Exception as e:
            await ctx.send(f"Error: {e}")
            print(f"[ERROR] Voice: {e}")
    else:
        await ctx.send("You are not in a voice channel.")


@bot.command(name="leave", aliases=["l"])
async def leave(ctx):
    voice = ctx.voice_client
    if voice and voice.is_connected():
        await voice.disconnect()
        await ctx.send("Disconnected.")
    else:
        await ctx.send("Not connected.")


@bot.command(name="read", aliases=["r"])
async def read(ctx, *, message: str):
    async def after_playback(error):
        if error:
            print(f"[AUDIO ERROR] {error}")
        else:
            print("[INFO] Playback finished")
        try:
            os.remove("tts_output.mp3")
            print("[INFO] Deleted tts_output.mp3")
        except Exception as e:
            print(f"[CLEANUP ERROR] {e}")

    if ctx.voice_client is None:
        if ctx.author.voice:
            try:
                await ctx.author.voice.channel.connect()
                await ctx.send(f"Connected to {ctx.author.voice.channel.name}")
            except Exception as e:
                print(f"[CONNECT ERROR] {e}")
                await ctx.send("Could not connect.")
                return
        else:
            await ctx.send("You must be in a voice channel.")
            return

    try:
        tts = gTTS(text=message, lang="en")
        tts.save("tts_output.mp3")
    except Exception as e:
        print(f"[GTTS ERROR] {e}")
        await ctx.send("Failed to generate TTS.")
        return

    voice = ctx.voice_client
    try:
        if voice.is_playing():
            voice.stop()

        audio_source = FFmpegPCMAudio("tts_output.mp3")
        voice.play(audio_source, after=lambda e: bot.loop.create_task(after_playback(e)))
    except Exception as e:
        print(f"[PLAYBACK ERROR] {e}")
        await ctx.send("Playback failed.")

@bot.command(name="shutdown", aliases=["s"])
@commands.is_owner()
async def shutdown(ctx):
    await ctx.send("Goodbye!")
    await bot.close()

@bot.command(name="helpme")
async def help(ctx):
    help_message = (
        "**Commands:**\n"
        "`!join` (`!j`): Speak joins your current voice channel.\n"
        "`!leave` (`!l`): Speak leaves the voice channel.\n"
        "`!read <message>` (`!r <message>`): Speak reads aloud the provided text in the voice channel.\n"
    )
    await ctx.send(help_message)

bot.run(TOKEN, log_handler=handler, log_level=logging.DEBUG)