# main.py
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext
import sqlite3
import os

# تنظیمات پایه
TOKEN = os.getenv('BOT_TOKEN') or "توکن_ربات_شما"
DB_NAME = "math_bot.db"

# --- پایگاه داده ---
def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY,
        current_chapter INTEGER DEFAULT 1,
        current_lesson INTEGER DEFAULT 1
    )
    ''')
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS progress (
        user_id INTEGER,
        chapter INTEGER,
        score INTEGER,
        passed BOOLEAN DEFAULT FALSE,
        FOREIGN KEY (user_id) REFERENCES users (user_id)
    )
    ''')
    
    conn.commit()
    conn.close()

# --- درسنامه فصل ۱ ---
CHAPTER_1_LESSONS = {
    1: {
        "title": "مفهوم مجموعه",
        "content": "در ریاضیات، مجموعه به گروهی از اشیا گفته می‌شود...",
        "video": "https://example.com/set-theory"
    },
    2: {
        "title": "انواع مجموعه‌ها",
        "content": "1. مجموعه متناهی\n2. مجموعه نامتناهی\n3. مجموعه تهی",
        "video": "https://example.com/set-types"
    }
}

# --- تمرینات فصل ۱ ---
CHAPTER_1_QUESTIONS = {
    1: {
        "question": "کدام گزینه مجموعه اعداد فرد کمتر از ۱۰ را نمایش می‌دهد؟",
        "options": ["{1,3,5,7,9}", "{2,4,6,8}", "{0,1,2}"],
        "answer": 0
    }
}

# --- دستورات ربات ---
def start(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("INSERT OR IGNORE INTO users (user_id) VALUES (?)", (user_id,))
    conn.commit()
    conn.close()
    
    keyboard = [
        [InlineKeyboardButton("📖 درسنامه", callback_data="lessons_1")],
        [InlineKeyboardButton("✏️ تمرین", callback_data="practice_1")],
        [InlineKeyboardButton("📝 آزمون", callback_data="exam_1")]
    ]
    update.message.reply_text(
        "📚 فصل ۱: مجموعه‌ها\nلطفا بخش مورد نظر را انتخاب کنید:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

def show_lesson(update: Update, context: CallbackContext, chapter: int, lesson: int):
    lesson_data = CHAPTER_1_LESSONS[lesson]
    keyboard = [
        [InlineKeyboardButton("🎥 ویدیو آموزشی", url=lesson_data["video"])],
        [InlineKeyboardButton("🔙 برگشت", callback_data=f"chapter_{chapter}")]
    ]
    update.callback_query.edit_message_text(
        f"📖 {lesson_data['title']}\n\n{lesson_data['content']}",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# --- اجرای ربات ---
def main():
    init_db()
    updater = Updater(TOKEN)
    dp = updater.dispatcher
    
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CallbackQueryHandler(lambda u,c: show_lesson(u, c, 1, 1), pattern="^lessons_1_1"))
    
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
