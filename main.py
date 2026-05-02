from pyrogram import Client, filters
from pytgcalls import PyTgCalls
from pytgcalls.types.input_stream import InputAudioStream, InputStream
from yt_dlp import YoutubeDL
import asyncio

API_ID = int("30625353")
API_HASH="c87aeeba1c838ace1d313009dbfbf277"
BOT_TOKEN= "8426776965:AAEApcJVhVHLdUAGktkRZn1A3jTLsoTibFI"

app = Client("multi_lang_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
call_py = PyTgCalls(app)

ydl_opts = {
    "format": "bestaudio",
    "quiet": True
}

def yt_search(query):
    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(f"ytsearch:{query}", download=False)
        return info["entries"][0]["url"]

# 🔊 PLAY COMMAND (3 LANGUAGE)
@app.on_message(filters.command(["play", "አጫውት", "تشغيل"]))
async def play(_, message):
    if len(message.command) < 2:
        return await message.reply(
            "❗ ርዕስ ጻፍ\n"
            "Example:\n"
            "/play surah rahman\n"
            "/play ሱራ ያሲን\n"
            "/play سورة الرحمن"
        )

    query = " ".join(message.command[1:])

    # 🌍 Language detection
    if any("\u1200" <= c <= "\u137F" for c in query):
        search = query + " ቁርአን ወይም ሀዲስ ድምፅ"
        msg = "⏳ እየፈለገ ነው..."
    elif any("\u0600" <= c <= "\u06FF" for c in query):
        search = query + " تلاوة قرآن أو حديث صوتي"
        msg = "⏳ جاري البحث..."
    else:
        search = query + " quran recitation or hadith audio"
        msg = "⏳ Searching..."

    await message.reply(msg)

    try:
        url = yt_search(search)

        await call_py.join_group_call(
            message.chat.id,
            InputStream(InputAudioStream(url))
        )

        await message.reply(f"▶️ Now Playing:\n{query}")

    except Exception as e:
        await message.reply(f"❌ Error:\n{str(e)}")

@app.on_message(filters.command(["start"]))
async def start(_, message):
    await message.reply(
        "🤖 Quran & Hadith Bot\n\n"
        "Commands:\n"
        "/play ሱራ ያሲን\n"
        "/play surah rahman\n"
        "/play سورة الرحمن\n\n"
        "🎧 ድምፅ በLive ይጫወታል"
    )

app.start()
call_py.start()
print("Bot Started ✅")
asyncio.get_event_loop().run_forever()
