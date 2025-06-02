import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext

# تنظیمات لاگ
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

TOKEN = os.getenv('BOT_TOKEN') or "توکن_ربات_شما"

# ساختار داده‌های آموزشی کامل شده
CHAPTERS = {
    1: {
        'title': 'مجموعه‌ها و احتمال',
        'lessons': {
            1: {
                'title': 'مفهوم مجموعه',
                'content': '📖 مجموعه به گروهی از اشیا گفته می‌شود که ویژگی مشترکی دارند.\n\nمثال:\n• مجموعه اعداد طبیعی کمتر از ۵: {1,2,3,4}',
                'video': 'https://example.com/set-theory'
            },
            2: {
                'title': 'مجموعه‌های برابر',
                'content': '📖 دو مجموعه وقتی برابرند که:\n1. عضوهای یکسان داشته باشند\n2. ترتیب اعضا مهم نیست\n\nمثال:\n• {1,2,3} = {3,2,1}\n• {a,b} ≠ {a,b,c}',
                'video': 'https://example.com/equal-sets'
            },
            3: {
                'title': 'زیرمجموعه',
                'content': '📖 مجموعه A زیرمجموعه B است اگر همه اعضای A در B باشند.\n\nنماد: A ⊆ B\n\nمثال:\n• {1,2} ⊆ {1,2,3}\n• {1,4} ⊈ {1,2,3}',
                'video': 'https://example.com/subset'
            },
            4: {
                'title': 'اجتماع، اشتراک و تفاضل',
                'content': '📖 عملیات اصلی مجموعه‌ها:\n\n1. اجتماع (A∪B): همه اعضای A و B\n2. اشتراک (A∩B): اعضای مشترک\n3. تفاضل (A-B): اعضای A که در B نیستند\n\nمثال:\n• {1,2} ∪ {2,3} = {1,2,3}\n• {1,2} ∩ {2,3} = {2}\n• {1,2} - {2,3} = {1}',
                'video': 'https://example.com/set-operations'
            },
            5: {
                'title': 'مجموعه‌ها و احتمال',
                'content': '📖 احتمال = تعداد حالت‌های مطلوب / تعداد کل حالت‌ها\n\nبا مجموعه‌ها:\n• فضای نمونه (S): همه نتایج ممکن\n• پیشامد: زیرمجموعه‌ای از S\n\nمثال:\n• احتمال آمدن عدد زوج در تاس: P = |{2,4,6}| / |{1,2,3,4,5,6}| = 3/6 = 0.5',
                'video': 'https://example.com/sets-probability'
            }
        },
        'exercises': {
            1: {
                'question': 'کدام گزینه یک مجموعه است؟',
                'options': ['الف) {1,2,3}', 'ب) 1,2,3'],
                'answer': 0,
                'explanation': 'پاسخ صحیح گزینه الف است چون مجموعه باید با آکولاد مشخص شود.'
            },
            2: {
                'question': 'کدام گزینه نشان‌دهنده مجموعه‌های برابر است؟',
                'options': ['الف) {1,2} و {2,1}', 'ب) {1,2} و {1,2,3}'],
                'answer': 0,
                'explanation': 'پاسخ صحیح گزینه الف است چون ترتیب در مجموعه‌ها مهم نیست.'
            },
            3: {
                'question': 'اگر A = {1,2} و B = {1,2,3} باشد، کدام عبارت درست است؟',
                'options': ['الف) A ⊆ B', 'ب) B ⊆ A'],
                'answer': 0,
                'explanation': 'پاسخ صحیح گزینه الف است چون همه اعضای A در B وجود دارند.'
            },
            4: {
                'question': 'حاصل {1,2} ∪ {2,3} چیست؟',
                'options': ['الف) {1,2,3}', 'ب) {2}'],
                'answer': 0,
                'explanation': 'پاسخ صحیح گزینه الف است چون اجتماع شامل همه اعضاست.'
            },
            5: {
                'question': 'احتمال انتخاب عدد اول از {1,2,3,4,5} چقدر است؟',
                'options': ['الف) 3/5', 'ب) 2/5'],
                'answer': 0,
                'explanation': 'پاسخ صحیح گزینه الف است چون اعداد اول {2,3,5} هستند (3 عدد از 5).'
            }
        },
        'exams': {
            1: {
                'title': 'آزمون جامع مجموعه‌ها',
                'description': 'آزمون 10 سوالی از تمام مباحث مجموعه‌ها',
                'questions': [
                    {
                        'text': 'کدام یک مجموعه نیست؟',
                        'options': ['الف) {a,b,c}', 'ب) a,b,c'],
                        'answer': 1
                    },
                    {
                        'text': 'اگر A = {1,2} و B = {2,1} باشد، کدام درست است؟',
                        'options': ['الف) A = B', 'ب) A ≠ B'],
                        'answer': 0
                    },
                    {
                        'text': 'کدام زیرمجموعه {1,2,3} نیست؟',
                        'options': ['الف) {1,2}', 'ب) {1,4}'],
                        'answer': 1
                    },
                    {
                        'text': 'حاصل {1,2} ∩ {2,3} چیست؟',
                        'options': ['الف) {2}', 'ب) {1,2,3}'],
                        'answer': 0
                    },
                    {
                        'text': 'حاصل {1,2,3} - {2} چیست؟',
                        'options': ['الف) {1,3}', 'ب) {2}'],
                        'answer': 0
                    },
                    {
                        'text': 'فضای نمونه پرتاب سکه چیست؟',
                        'options': ['الف) {شیر،خط}', 'ب) {شیر}'],
                        'answer': 0
                    },
                    {
                        'text': 'احتمال آمدن عدد زوج با تاس چقدر است؟',
                        'options': ['الف) 1/2', 'ب) 1/6'],
                        'answer': 0
                    },
                    {
                        'text': 'اگر A ⊆ B و B ⊆ A باشد، نتیجه چیست؟',
                        'options': ['الف) A = B', 'ب) A ≠ B'],
                        'answer': 0
                    },
                    {
                        'text': 'حاصل (A ∪ B) ∩ C برابر است با:',
                        'options': ['الف) (A ∩ C) ∪ (B ∩ C)', 'ب) (A ∪ B) ∪ C'],
                        'answer': 0
                    },
                    {
                        'text': 'احتمال انتخاب یک مربع از مجموعه {مربع،دایره،مثلث} چقدر است؟',
                        'options': ['الف) 1/3', 'ب) 1'],
                        'answer': 0
                    }
                ]
            }
        }
    }
}

# توابع مدیریت آزمون
def calculate_exam_score(user_answers, correct_answers):
    score = 0
    for i in range(len(user_answers)):
        if user_answers[i] == correct_answers[i]:
            score += 1
    return score

# بقیه توابع مانند قبل (با بهبودهای لازم)
# [این قسمت شامل تمام توابعی است که قبلاً تعریف کردیم]
# فقط تابع handle_exam_answer را به این شکل اصلاح کنید:

def handle_exam_answer(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    
    # مدیریت پاسخ‌های آزمون و محاسبه نمره
    if 'user_answers' not in context.user_data:
        context.user_data['user_answers'] = []
    
    data = query.data.split('_')
    context.user_data['user_answers'].append(int(data[4]))
    
    # اگر به آخرین سوال رسیدیم
    if len(context.user_data['user_answers']) == len(CHAPTERS[1]['exams'][1]['questions']):
        correct_answers = [q['answer'] for q in CHAPTERS[1]['exams'][1]['questions']]
        score = calculate_exam_score(context.user_data['user_answers'], correct_answers)
        
        # نمایش نتیجه
        result_text = f"🏆 نتیجه آزمون\n\nنمره شما: {score}/10\n\n"
        for i, (user_ans, correct_ans) in enumerate(zip(context.user_data['user_answers'], correct_answers)):
            result_text += f"سوال {i+1}: {'✅' if user_ans == correct_ans else '❌'}\n"
        
        keyboard = [
            [InlineKeyboardButton("🔙 منوی اصلی", callback_data="back_to_main")],
            [InlineKeyboardButton("📖 درسنامه", callback_data="menu_lessons_1")]
        ]
        
        query.edit_message_text(
            result_text,
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
        del context.user_data['user_answers']
    else:
        # نمایش سوال بعدی
        next_question = len(context.user_data['user_answers'])
        start_exam_question(update, context, 1, 1, next_question)

def main():
    updater = Updater(TOKEN)
    dp = updater.dispatcher
    
    # هندلرهای اصلی
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CallbackQueryHandler(handle_menu, pattern="^menu_"))
    dp.add_handler(CallbackQueryHandler(show_lesson, pattern="^show_lesson_"))
    dp.add_handler(CallbackQueryHandler(show_practice_menu, pattern="^menu_practice_"))
    dp.add_handler(CallbackQueryHandler(start_practice, pattern="^start_practice_"))
    dp.add_handler(CallbackQueryHandler(handle_practice_answer, pattern="^submit_answer_"))
    dp.add_handler(CallbackQueryHandler(show_exam_menu, pattern="^menu_exam_"))
    dp.add_handler(CallbackQueryHandler(start_exam, pattern="^start_exam_"))
    dp.add_handler(CallbackQueryHandler(handle_exam_answer, pattern="^exam_answer_"))
    dp.add_handler(CallbackQueryHandler(start, pattern="^back_to_main"))
    
    updater.start_polling()
    logger.info("✅ ربات آموزشی مجموعه‌ها با موفقیت فعال شد!")
    updater.idle()

if __name__ == "__main__":
    main()
