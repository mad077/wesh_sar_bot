# نظام مراقبة البوت وإعادة تشغيله تلقائيًا
import subprocess
import time
import logging
from datetime import datetime

# إعداد السجل
logging.basicConfig(
    filename='bot_monitor.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def monitor_bot():
    """مراقبة البوت وإعادة تشغيله إذا توقف"""
    max_restarts = 5
    restart_count = 0
    last_restart = None
    
    while True:
        try:
            # تشغيل البوت
            process = subprocess.Popen(
                ['python', 'telegram_bot_وش_صار.py'],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            
            logging.info("✅ البوت يعمل الآن")
            print(f"[{datetime.now()}] ✅ البوت يعمل الآن")
            
            # انتظر حتى ينتهي البوت (يجب ألا ينتهي!)
            stdout, stderr = process.communicate()
            
            # إذا وصل هنا، البوت توقف
            restart_count += 1
            current_time = datetime.now()
            
            # تحقق من عدد إعادة التشغيل
            if last_restart and (current_time - last_restart).seconds < 300:
                # إذا أعيد التشغيل خلال 5 دقائق، انتظر أكثر
                logging.warning(f"⚠️ البوت توقف بعد وقت قصير. إعادة التشغيل #{restart_count}")
                print(f"[{datetime.now()}] ⚠️ البوت توقف. إعادة التشغيل #{restart_count}")
            else:
                restart_count = 1
                last_restart = current_time
                logging.info(f"🔄 إعادة تشغيل البوت. المرة #{restart_count}")
                print(f"[{datetime.now()}] 🔄 إعادة تشغيل البوت. المرة #{restart_count}")
            
            if restart_count >= max_restarts:
                logging.error("❌ تجاوز حد إعادة التشغيل. توقف المراقبة.")
                print(f"[{datetime.now()}] ❌ تجاوز حد إعادة التشغيل. توقف المراقبة.")
                break
            
            # انتظر 10 ثواني قبل إعادة التشغيل
            time.sleep(10)
            
        except Exception as e:
            logging.error(f"❌ خطأ في المراقبة: {e}")
            print(f"[{datetime.now()}] ❌ خطأ في المراقبة: {e}")
            time.sleep(30)

if __name__ == "__main__":
    print("🔍 جاري بدء نظام مراقبة البوت...")
    logging.info("🔍 بدء نظام المراقبة")
    monitor_bot()
