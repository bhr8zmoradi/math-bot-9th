# main.py
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext
import os
import logging

# تنظیم لاگ‌گیری
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

TOKEN = os.getenv('BOT_TOKEN')

# --- ساختار داده‌های آموزشی ---
CHAPTERS = {
    1: {
        'title': 'مجموعه‌ها',
        'lessons': {
            1: {'title': 'مفهوم مجموعه', 'content': 'تعریف مجموعه...', 'video': 'https://example.com/video1'},
            2: {'title': 'انواع مجموعه', 'content': 'متناهی/نامتناهی...', 'video': 'https://example.com/video2'}
        },
        'questions': [
            {'text': 'کدام گزینه مجموعه است؟', 'options': ['الف) {1,2,3}', 'ب) 1,2,3'], 'answer': 0}
        ]
    }
}

# --- مدیریت منوها ---
def start(update: Update, context: CallbackContext):
    keyboard = [
        [InlineKeyboardButton("📖 درسنامه", callback_data="menu_lessons_1")],
        [InlineKeyboardButton("✏️ تمرین", callback_data="menu_practice_1")],
        [InlineKeyboardButton("📝 آزمون", callback_data="menu_exam_1")]
    ]
    update.message.reply_text(
        "فصل 1: مجموعه‌ها\nلطفا بخش مورد نظر را انتخاب کنید:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

def handle_menu(update: Update, context: CallbackContext):
    query = update.callback_query
    data = query.data.split('_')
    
    if data[1] == 'lessons':
        show_lessons_menu(update, int(data[2]))
    elif data[1] == 'practice':
        start_practice(update, int(data[2]))
    elif data[1] == 'exam':
        start_exam(update, int(data[2]))

def show_lessons_menu(update: Update, chapter: int):
    lessons = CHAPTERS[chapter]['lessons']
    keyboard = [
        [InlineKeyboardButton(lessons[i]['title'], callback_data=f"lesson_{chapter}_{i}")] 
        for i in lessons
    ]
    keyboard.append([InlineKeyboardButton("🔙 برگشت", callback_data="back_to_main")])
    
    update.callback_query.edit_message_text(
        f"درسنامه‌های فصل {chapter}:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# --- اجرای ربات ---
def main():
    updater = Updater(TOKEN)
    dp = updater.dispatcher
    
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CallbackQueryHandler(handle_menu, pattern="^menu_"))
    dp.add_handler(CallbackQueryHandler(show_lessons_menu, pattern="^lesson_"))
    
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
