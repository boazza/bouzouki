# اسم الملف: voice.py

import os
import speech_recognition as sr
from pydub import AudioSegment
from gtts import gTTS  # type: ignore

def speech_to_text(audio_file):
    """تحويل الصوت إلى نص باستخدام نظام المحاولات الذكي المتعدد اللغات (عربي/فرنسي/إنجليزي)"""
    wav_file = "temp.wav"
    try:
        # قراءة الملف الصوتي مهما كانت صيغته (.opus, .ogg, .m4a) وتحويله إلى wav
        audio = AudioSegment.from_file(audio_file)
        audio.export(wav_file, format="wav")

        recognizer = sr.Recognizer()

        with sr.AudioFile(wav_file) as source:
            audio_data = recognizer.record(source)

        # 👇 تطبيق حلك الذكي والمرن للتعرف على الكلام بمختلف اللغات
        try:
            # المحاولة الأولى: اللهجة الجزائرية والعربية
            text = recognizer.recognize_google(audio_data, language="ar-DZ")
        except:
            try:
                # المحاولة الثانية: الكلمات الفرنسية المدمجة في الكلام
                text = recognizer.recognize_google(audio_data, language="fr-FR")
            except:
                try:
                    # المحاولة الثالثة والاحتياطية: المصطلحات الإنجليزية
                    text = recognizer.recognize_google(audio_data, language="en-US")
                except:
                    return None

        return text

    except Exception as e:
        print(f"خطأ تحويل الصوت: {e}")
        return None
        
    finally:
        # تنظيف ملف الـ wav المؤقت فقط لضمان عدم تضارب البيانات والحفاظ على الذاكرة
        if os.path.exists(wav_file):
            os.remove(wav_file)

def text_to_speech(text, output_filename="reply_voice.m4a"):
    """تحويل نص المواصفات الصارم إلى ملف صوتي m4a متوافق مع إنستغرام باستعمال الفصحى المضمونة"""
    temp_mp3 = "temp_voice.mp3"
    try:
        # الاعتماد الكلي على السطر المستقر والفولاذي للنطق
        tts = gTTS(text=text, lang='ar', slow=False)
        tts.save(temp_mp3)
        
        # تحويل ملف الـ mp3 إلى صيغة m4a الأكثر قبولاً في ميديا إنستغرام
        audio = AudioSegment.from_mp3(temp_mp3)
        audio.export(output_filename, format="m4a")
        return output_filename
        
    except Exception as e:
        print(f"خطأ أثناء توليد صوت الرد: {e}")
        return None
        
    finally:
        # مسح الـ mp3 المؤقت مباشرة بعد التحويل للحفاظ على نظافة مجلد المشروع
        if os.path.exists(temp_mp3):
            os.remove(temp_mp3)