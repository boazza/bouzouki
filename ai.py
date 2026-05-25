# اسم الملف: ai.py

from groq import Groq

# 🔑 مفتاح الـ API الخاص بـ Groq
GROQ_API_KEY = "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"

# تهيئة عميل Groq
client = Groq(api_key=GROQ_API_KEY)

def generate_response(user_message):
    """توليد مواصفات الهاتف مع نظام فلترة ذكي لحظر الكلمات السيئة"""
    
    # تحويل النص إلى حروف صغيرة وتنظيف الفراغات لضمان دقة الفحص
    msg = user_message.lower().strip()

    # 🛡️ قائمة الكلمات السيئة المحظورة
    bad_words = [
        "غبي",
        "حمار",
        "يدك فيه",
        "لعبلي بيه ",
        "اعطني نيك ",
        "سوة تاع مك ",
        "زبي",
        "ترمتك"
    ]

    # 🚫 الفحص الفوري: إذا احتوت الرسالة على أي كلمة محظورة يتم حظر الرد مباشرة
    for word in bad_words:
        if word in msg:
            return "أنا بوت محترم 🤖 ولن أسبك."

    # 🧠 إذا كانت الرسالة نظيفة، نمررها لموديل Llama 3.1 عبر Groq
    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {
                    "role": "system",
                    "content": """
أنت بوت مواصفات هواتف فقط.

إذا أرسل المستخدم اسم هاتف:
أعطه:
📱 الشاشة
⚙️ المعالج
📸 الكاميرا
🔋 البطارية
🎮 هل يصلح ألعاب
🔥 هل يسخن
⭐ تقييم الهاتف

إذا لم يرسل اسم هاتف:
قل فقط:
أرسل اسم هاتف فقط 📱
"""
                },
                {
                    "role": "user",
                    "content": user_message
                }
            ],
            temperature=0.2, # درجة حرارة منخفضة لضمان الثبات الصارم على القالب
            max_tokens=200   # حجم كافي لمنع انقطاع النص
        )

        return response.choices[0].message.content.strip()

    except Exception as e:
        print(f"خطأ في Groq API: {e}")
        return "حدث خطأ، أرسل اسم الهاتف مرة أخرى 📱"
