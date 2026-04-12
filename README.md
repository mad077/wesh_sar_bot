# 🤖 بوت تلقرام: وش صار

بوت أخباري يسحب آخر الأخبار العربية لحظيًا من مصادر RSS مجانية.

## 📋 المميزات

- ✅ 7 مجالات إخبارية (أخبار عامة، رياضة، سياسة، اقتصاد، تكنولوجيا، ترفيه، أخبار العالم)
- ✅ 5 أخبار لكل مجال
- ✅ تاريخ هجري + ميلادي
- ✅ عرض اليوم والساعة
- ✅ تحديث لحظي من مصادر عربية
- ✅ مجاني تمامًا (بدون API Key)

## 🚀 التثبيت المحلي

### 1. تثبيت المتطلبات
```bash
pip install -r requirements.txt
```

### 2. إعداد التوكن
انسخ ملف `.env.example` إلى `.env` وعدل التوكن:
```bash
# على Windows
copy .env.example .env

# على Mac/Linux
cp .env.example .env
```

ثم افتح `.env` وضع توكن البوت:
```
TELEGRAM_BOT_TOKEN=1234567890:ABCdefGHIjklMNOpqrsTUVwxyz
```

### 3. تشغيل البوت
```bash
python telegram_bot_وش_صار.py
```

## 🌐 الرفع على Render.com

### الخطوات:

1. **ارفع المشروع على GitHub**
```bash
git init
git add .
git commit -m "بوت وش صار"
git branch -M main
git remote add origin https://github.com/USERNAME/wesh_sar_bot.git
git push -u origin main
```

2. **في Render.com:**
   - اضغط **New +** → **Web Service**
   - اربط حساب GitHub
   - اختر مشروع `wesh_sar_bot`

3. **الإعدادات:**
   | الحقل | القيمة |
   |-------|--------|
   | Name | `wesh-sar-bot` |
   | Region | `Bahrain` أو `UAE` |
   | Branch | `main` |
   | Runtime | `Python 3` |
   | Build Command | `pip install -r requirements.txt` |
   | Start Command | `python telegram_bot_وش_صار.py` |
   | Instance Type | `Free` |

4. **أضف متغير البيئة:**
   - اضغط **Advanced**
   - **Add Environment Variable**
   - Key: `TELEGRAM_BOT_TOKEN`
   - Value: التوكن من @BotFather

5. **اضغط Create Web Service**

## 📱 استخدام البوت

1. افتح تلقرام وابحث عن بوتك
2. أرسل `/start` أو `/ابدأ`
3. اختر المجال المطلوب
4. استمتع بآخر الأخبار!

## 📰 مصادر الأخبار

| المجال | المصادر |
|--------|---------|
| أخبار عامة | الجزيرة، BBC عربي |
| رياضة | الجزيرة رياضية، كورة |
| سياسة | الجزيرة، العربية |
| اقتصاد | الجزيرة، العربية |
| تكنولوجيا | الجزيرة، العربية |
| ترفيه | الجزيرة، العربية |
| أخبار العالم | الجزيرة، BBC عربي |

## 🔧 حل المشاكل

| المشكلة | الحل |
|---------|------|
| البوت لا يرد | تحقق من التوكن في Environment Variables |
| خطأ في البناء | تأكد من requirements.txt |
| الأخبار لا تظهر | راجع روابط RSS في الكود |
| البوت ينام | الخطة المجانية تنام بعد 15 دقيقة، أي رسالة توقظه |

## 📞 الدعم

للمساعدة، راجع ملف README أو افتح Issue في GitHub.

---

**تم التطوير بواسطة:** مساعد الذكاء الاصطناعي
**الرخصة:** مجاني للاستخدام الشخصي
