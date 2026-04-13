import os
import logging
import requests
import xml.etree.ElementTree as ET
from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# إعداد السجل
logging.basicConfig(level=logging.INFO)

# الحصول على التوكن
import os
TELEGRAM_BOT_TOKEN = os.getenv("8762858117:AAE0jACensGIe8EXi-tloIP7I95_ZgHiPjk")

if not TELEGRAM_BOT_TOKEN:
    print("❌ ERROR: TELEGRAM_BOT_TOKEN not set!")
    exit(1)

# مصادر الأخبار RSS
NEWS_SOURCES = {
    "📰 أخبار عامة": "https://www.aljazeera.net/xml/rss/all.xml",
    "⚽ الرياضة": "https://www.aljazeera.net/xml/rss/sports.xml",
    "🏛️ السياسة": "https://www.aljazeera.net/xml/rss/politics.xml",
    "💰 الاقتصاد": "https://www.aljazeera.net/xml/rss/economy.xml",
    "📱 التكنولوجيا": "https://www.aljazeera.net/xml/rss/technology.xml",
    "🎬 الترفيه": "https://www.aljazeera.net/xml/rss/entertainment.xml",
    "🌍 أخبار العالم": "https://www.aljazeera.net/xml/rss/world.xml",
}

def get_hijri_date():
    now = datetime.now()
    hijri_year = now.year - 622
    hijri_month = now.month + 1
    hijri_day = now.day
    if hijri_month > 12:
        hijri_month -= 12
        hijri_year += 1
    
    hijri_months = [
        "محرم", "صفر", "ربيع الأول", "ربيع الثاني",
        "جمادى الأولى", "جمادى الآخرة", "رجب", "شعبان",
        "رمضان", "شوال", "ذو القعدة", "ذو الحجة"
    ]
    
    return f"{hijri_day} {hijri_months[hijri_month-1]} {hijri_year} هـ"

def fetch_news_from_rss(url, limit=5):
    news_items = []
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        root = ET.fromstring(response.content)
        
        for item in root.findall('.//item')[:limit]:
            title = item.find('title')
            link = item.find('link')
            pub_date = item.find('pubDate')
            
            if title is not None and link is not None:
                news_items.append({
                    "title": title.text,
                    "link": link.text,
                    "published": pub_date.text if pub_date is not None else "غير متوفر"
                })
    except Exception as e:
        logging.error(f"خطأ في جلب الأخبار: {e}")
    
    return news_items

def format_news_message(category, news_items):
    now = datetime.now()
    gregorian_date = now.strftime("%Y-%m-%d")
    hijri_date = get_hijri_date()
    day_name = now.strftime("%A")
    current_time = now.strftime("%H:%M:%S")
    
    message = f"""
📢 *وش صار - آخر الأخبار*

✅ حسناً، هذه أهم الأخبار لهذه اللحظة:

📅 *التاريخ:*
├ ميلادي: {gregorian_date}
├ هجري: {hijri_date}
├ اليوم: {day_name}
└ الساعة: {current_time}

📌 *المجال: {category}*
━━━━━━━━━━━━━━━━━━━━
"""
    
    for i, news in enumerate(news_items, 1):
        message += f"""
{i}️⃣ *{news['title']}*
📎 الرابط: {news['link']}
⏰ نشر: {news['published']}
"""
    
    message += "\n━━━━━━━━━━━━━━━━━━━━"
    message += "\n🔄 لتحديث الأخبار أرسل: /ابدأ"
    
    return message

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton(cat, callback_data=cat)] for cat in NEWS_SOURCES.keys()]
    await update.message.reply_text(
        "👋 *أهلاً بك في بوت وش صار* 🎉\n\n"
        "أنا بوت أخباري أسحب لك آخر الأخبار لحظيًا من مصادر عربية موثوقة.\n\n"
        "📌 *اختر المجال اللي تبي أخباره:*\n",
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode="Markdown"
    )

async def select_category(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    category = query.data
    news_url = NEWS_SOURCES.get(category, "")
    
    await query.edit_message_text("🔄 جاري جلب الأخبار... لحظة من فضلك...")
    
    news_items = fetch_news_from_rss(news_url, limit=5)
    
    if news_items:
        message = format_news_message(category, news_items)
        keyboard = [
            [InlineKeyboardButton("🔄 تحديث", callback_data=category)],
            [InlineKeyboardButton("📋 قائمة المجالات", callback_data="BACK_TO_MENU")],
        ]
        await query.edit_message_text(message, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown")
    else:
        await query.edit_message_text("❌ عذراً، لم نتمكن من جلب الأخبار حاليًا.\n\n🔄 لإعادة المحاولة: /ابدأ", parse_mode="Markdown")

async def back_to_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    keyboard = [[InlineKeyboardButton(cat, callback_data=cat)] for cat in NEWS_SOURCES.keys()]
    await query.edit_message_text("📌 *اختر المجال اللي تبي أخباره:*\n", reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown")

def main():
    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("ابدأ", start))
    app.add_handler(CallbackQueryHandler(select_category))
    app.add_handler(CallbackQueryHandler(back_to_menu, pattern="^BACK_TO_MENU$"))
    print("✅ Bot started successfully!")
    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
