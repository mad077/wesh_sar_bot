# ============================================================================
# بوت تلقرام: وش صار
# مصدر الأخبار: RSS Feeds عربية مجانية (بدون API Key)
# ============================================================================

import logging
import requests
import feedparser
import re
import os
import time
import threading
from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# ============================================================================
# إعدادات البوت
# ============================================================================
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "8762858117:AAE0jACensGIe8EXi-tloIP7I95_ZgHiPjk")

# إعداد السجل
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# ============================================================================
# مصادر الأخبار العربية (RSS Feeds مجانية)
# ============================================================================
NEWS_SOURCES = {
    "📰 أخبار عامة": [
        "https://www.aljazeera.net/xml/rss/all.xml",
        "https://feeds.bbci.co.uk/arabic/rss.xml",
    ],
    "⚽ الرياضة": [
        "https://www.aljazeera.net/xml/rss/sports.xml",
        "https://www.kooora.com/rss.aspx",
    ],
    "🏛️ السياسة": [
        "https://www.aljazeera.net/xml/rss/politics.xml",
        "https://www.alarabiya.net/.mrss/ar/politics.xml",
    ],
    "💰 الاقتصاد": [
        "https://www.aljazeera.net/xml/rss/economy.xml",
        "https://www.alarabiya.net/.mrss/ar/economy.xml",
    ],
    "📱 التكنولوجيا": [
        "https://www.aljazeera.net/xml/rss/technology.xml",
        "https://www.alarabiya.net/.mrss/ar/technology.xml",
    ],
    "🎬 الترفيه": [
        "https://www.aljazeera.net/xml/rss/entertainment.xml",
        "https://www.alarabiya.net/.mrss/ar/entertainment.xml",
    ],
    "🌍 أخبار العالم": [
        "https://www.aljazeera.net/xml/rss/world.xml",
        "https://feeds.bbci.co.uk/arabic/world/rss.xml",
    ],
}

# ============================================================================
# تحويل التاريخ الميلادي إلى هجري (تقريبي)
# ============================================================================
def get_hijri_date():
    """تحويل التاريخ الميلادي إلى هجري بشكل تقريبي"""
    now = datetime.now()
    year = now.year
    month = now.month
    day = now.day
    
    # خوارزمية تقريبية للتحويل
    hijri_year = year - 622
    hijri_month = month + 1
    hijri_day = day
    
    if hijri_month > 12:
        hijri_month -= 12
        hijri_year += 1
    
    # أسماء الأشهر الهجرية
    hijri_months = [
        "محرم", "صفر", "ربيع الأول", "ربيع الثاني",
        "جمادى الأولى", "جمادى الآخرة", "رجب", "شعبان",
        "رمضان", "شوال", "ذو القعدة", "ذو الحجة"
    ]
    
    return f"{hijri_day} {hijri_months[hijri_month-1]} {hijri_year} هـ"

# ============================================================================
# جلب الأخبار من RSS
# ============================================================================
def fetch_news_from_rss(urls, limit=5):
    """جلب الأخبار من روابط RSS"""
    news_items = []
    
    for url in urls:
        try:
            feed = feedparser.parse(url)
            for entry in feed.entries[:limit]:
                news_items.append({
                    "title": entry.title,
                    "link": entry.link,
                    "published": entry.get("published", "غير متوفر"),
                    "summary": entry.get("summary", "")[:200] + "..." if len(entry.get("summary", "")) > 200 else entry.get("summary", "")
                })
        except Exception as e:
            logging.error(f"خطأ في جلب الأخبار من {url}: {e}")
    
    # ترتيب الأخبار حسب الأحدث
    news_items = news_items[:limit]
    return news_items

# ============================================================================
# تنسيق رسالة الأخبار
# ============================================================================
def format_news_message(category, news_items):
    """تنسيق رسالة الأخبار للعرض"""
    now = datetime.now()
    
    # التاريخ الميلادي
    gregorian_date = now.strftime("%Y-%m-%d")
    # التاريخ الهجري
    hijri_date = get_hijri_date()
    # اليوم
    day_name = now.strftime("%A")
    # الساعة
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

# ============================================================================
# معالجة أمر /start
# ============================================================================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """الرد على أمر /start"""
    keyboard = [
        [InlineKeyboardButton(cat, callback_data=cat)]
        for cat in NEWS_SOURCES.keys()
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "👋 *أهلاً بك في بوت وش صار* 🎉\n\n"
        "أنا بوت أخباري أسحب لك آخر الأخبار لحظيًا من مصادر عربية موثوقة.\n\n"
        "📌 *اختر المجال اللي تبي أخباره:*\n"
        "يمكنك اختيار أي من المجالات أدناه:",
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )

# ============================================================================
# معالجة اختيار المجال
# ============================================================================
async def select_category(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """معالجة اختيار المستخدم للمجال"""
    query = update.callback_query
    await query.answer()
    
    category = query.data
    news_urls = NEWS_SOURCES.get(category, [])
    
    # جلب الأخبار
    await query.edit_message_text("🔄 جاري جلب الأخبار... لحظة من فضلك...")
    
    news_items = fetch_news_from_rss(news_urls, limit=5)
    
    if news_items:
        message = format_news_message(category, news_items)
        
        # إضافة أزرار للتنقل
        keyboard = [
            [InlineKeyboardButton("🔄 تحديث", callback_data=category)],
            [InlineKeyboardButton("📋 قائمة المجالات", callback_data="BACK_TO_MENU")],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(message, reply_markup=reply_markup, parse_mode="Markdown")
    else:
        await query.edit_message_text(
            "❌ عذراً، لم نتمكن من جلب الأخبار حاليًا.\n"
            "حاول مرة أخرى لاحقًا.\n\n"
            "🔄 لإعادة المحاولة: /ابدأ",
            parse_mode="Markdown"
        )

# ============================================================================
# معالجة العودة للقائمة
# ============================================================================
async def back_to_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """العودة لقائمة المجالات"""
    query = update.callback_query
    await query.answer()
    
    keyboard = [
        [InlineKeyboardButton(cat, callback_data=cat)]
        for cat in NEWS_SOURCES.keys()
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        "📌 *اختر المجال اللي تبي أخباره:*\n",
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )

# ============================================================================
# معالجة أمر /ابدأ
# ============================================================================
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """معالجة أمر /ابدأ"""
    keyboard = [
        [InlineKeyboardButton(cat, callback_data=cat)]
        for cat in NEWS_SOURCES.keys()
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "📌 *اختر المجال اللي تبي أخباره:*\n",
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )

# ============================================================================
# دالة إبقاء البوت نشطًا
# ============================================================================
def keep_alive():
    """إبقاء البوت نشطًا على الاستضافة المجانية"""
    while True:
        time.sleep(300)  # كل 5 دقائق

# ============================================================================
# البرنامج الرئيسي
# ============================================================================
def main():
    """تشغيل البوت"""
    # تشغيل خيط الإبقاء على البوت نشطًا
    threading.Thread(target=keep_alive, daemon=True).start()
    
    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    
    # إضافة المعالجات
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("ابدأ", start_command))
    app.add_handler(CallbackQueryHandler(select_category, pattern="^📰|^⚽|^🏛️|^💰|^📱|^🎬|^🌍"))
    app.add_handler(CallbackQueryHandler(back_to_menu, pattern="^BACK_TO_MENU$"))
    
    # تشغيل البوت
    print("🤖 البوت يعمل الآن...")
    logging.info("✅ بوت وش صار بدأ العمل بنجاح")
    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
