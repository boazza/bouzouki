# اسم الملف: bot.py

import time
import os
from instagrapi import Client
import phones
import ai
import voice
import database
import admin

# 1. إعدادات حساب إنستغرام البوت
USERNAME = "hafid.phons"
PASSWORD = "Faryal Boughzala51"

cl = Client()
print("جاري تسجيل الدخول إلى إنستغرام...")
cl.load_settings("settings.json")
cl.login(USERNAME, PASSWORD)
print("تم تسجيل الدخول بنجاح! البوت يعمل الآن...")

# قائمة لحفظ الـ ID الخاص بكل رسالة تم الرد عليها نهائياً لمنع التكرار
processed_messages = set()

while True:
    try:
        # جلب آخر 20 محادثة
        threads = cl.direct_threads(amount=20)
        
        for thread in threads:
            if not thread.messages:
                continue
                
            last_message = None
            for msg in thread.messages:
                if msg.user_id != cl.user_id:
                    last_message = msg
                    break

            if not last_message:
                continue
            
            user_id = last_message.user_id
            thread_id = thread.id
            
            # منع التكرار
            if last_message.id in processed_messages:
                continue
                
            processed_messages.add(last_message.id)

            # الشرط المزدوج والذكي للتحقق من الرسائل الصوتية
            is_voice = (
                hasattr(last_message, "voice_media") and last_message.voice_media
            ) or (
                hasattr(last_message, "media_type") and last_message.media_type == 2
            )

            # 2. معالجة الرسائل النصية العادية
            if last_message.text and not is_voice:
                user_text = last_message.text.strip()
                print(f"رسالة نصية جديدة من {user_id}: {user_text}")
                
                if admin.is_admin(user_id) and admin.is_admin_command(user_text):
                    reply = admin.handle_command(user_text)
                else:
                    reply = phones.get_phone_info(user_text)
                    if not reply:
                        reply = ai.generate_response(user_text)
                    
                if not reply:
                    continue
                
                cl.direct_send(reply, [user_id])
                print(f"تم الرد بنجاح والسكوت: {reply}")

            # 3. معالجة الرسائل الصوتية 
            elif is_voice:
                print(f"تم استلام رسالة صوتية من {user_id}...")

                try:
                    # 👇 تم التبديل للدالة الأكثر استقراراً وقوة بناءً على طلبك
                    voice_file = cl.media_download(last_message.pk)

                    if not voice_file:
                        print("فشل تحميل الصوت")
                        continue

                    # تحويل الفويس إلى نص
                    user_text = voice.speech_to_text(voice_file)

                    if not user_text:
                        print("لم يتم فهم الصوت")
                        continue

                    user_text = user_text.strip()
                    reply = phones.get_phone_info(user_text)

                    if not reply:
                        reply = ai.generate_response(user_text)

                    if not reply:
                        continue

                    # توليد البصمة الصوتية للرد (m4a)
                    voice_reply_path = voice.text_to_speech(reply)
                    
                    if voice_reply_path and os.path.exists(voice_reply_path):
                        try:
                            # إرسال الفويس عبر الـ thread_id لضمان ظهوره كبصمة صوتية حقيقية
                            cl.direct_send_voice(voice_reply_path, thread_id=thread_id)
                            print(f"🚀 تم إرسال الرد الصوتي بنجاح والسكوت!")
                        except Exception as send_error:
                            print(f"فشل إرسال الفويس، جاري الإرسال ككتابة احتياطياً: {send_error}")
                            cl.direct_send(reply, [user_id])
                        
                        # حذف ملف الرد الصوتي المؤقت بعد الإرسال
                        if os.path.exists(voice_reply_path):
                            os.remove(voice_reply_path)
                    else:
                        # احتياطي: إذا فشل نظام توليد الصوت يرسل الرد كتابة
                        cl.direct_send(reply, [user_id])
                        print(f"تم الرد على الصوت ككتابة: {reply}")

                except Exception as e:
                    print(f"خطأ الصوت: {e}")

    except Exception as e:
        print(f"حدث خطأ أثناء فحص الرسائل: {e}")
    
    # فحص الرسائل كل 10 ثوانٍ لحماية الحساب من الحظر
    time.sleep(10)
