Skip to content
Chats
Archived
New Chat
just now
New chat with Assistant
Assistant answers questions, refines code, and makes precise edits.
Assistant mode

advanced
Claude 3.5 Sonnet V2

Ask Assistant, use @ to include specific files...
import os
import openai
import aiosqlite
import nest_asyncio
import asyncio
from datetime import datetime, timedelta
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import (
    ApplicationBuilder, ContextTypes, MessageHandler, filters,
    CommandHandler
)

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ADMIN_ID = int(os.getenv("ADMIN_ID"))
LOG_CHANNEL_ID = int(os.getenv("LOG_CHANNEL_ID"))
ADMIN_GROUP_ID = int(os.getenv("ADMIN_GROUP_ID"))
FORCE_CHANNEL = os.getenv("FORCE_CHANNEL")

client = openai.OpenAI(api_key=OPENAI_API_KEY)
DB_NAME = "bixx_light.db"
banned_users = set()

# عضویت اجباری
async def is_member(user_id, context):
    try:
        member = await context.bot.get_chat_member(FORCE_CHANNEL, user_id)
        return member.status in ["member", "administrator", "creator"]
    except:
        return False

# دیتابیس
async def init_db():
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            plan TEXT DEFAULT 'free',
            used_messages INTEGER DEFAULT 0,
            vip_start TEXT,
            last_reset TEXT
        )""")
        await db.execute("""
        CREATE TABLE IF NOT EXISTS memory (
            user_id INTEGER,
            role TEXT,
            content TEXT
        )""")
        await db.commit()

async def fix_db_column():
    async with aiosqlite.connect(DB_NAME) as db:
        cursor = await db.execute("PRAGMA table_info(users)")
        columns = await cursor.fetchall()
        if not any(col[1] == "last_reset" for col in columns):
            await db.execute("ALTER TABLE users ADD COLUMN last_reset TEXT")
            await db.commit()

# ثبت کاربر
async def ensure_user(user_id, username, full_name, context):
    async with aiosqlite.connect(DB_NAME) as db:
        cursor = await db.execute("SELECT 1 FROM users WHERE user_id = ?", (user_id,))
        if not await cursor.fetchone():
            now = datetime.now().strftime("%Y-%m-%d")
            await db.execute("INSERT INTO users (user_id, plan, used_messages, last_reset) VALUES (?, 'free', 0, ?)", (user_id, now))

Results of your code will appear here when you run
Default
Workflows
