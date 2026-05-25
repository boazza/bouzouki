# اسم الملف: ai.py

from groq import Groq

# 🔑 تم وضع مفتاح الـ API الخاص بك هنا بأمان
GROQ_API_KEY = "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"

# تهيئة عميل Groq
client = Groq(api_key=GROQ_API_KEY)

def generate_response(user_message):
    """توليد مواصفات الهاتف الصارمة باستعمال موديل Llama 3.1 عبر Groq API"""
    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {
                    "role": "system",
                    "content": """
أنت بوت خبير في الهواتف الذكية 📱 فقط.

القوانين الصارمة:

1) إذا الرسالة تحتوي على اسم هاتف (Samsung, iPhone, Redmi, Oppo, Xiaomi...):
رد بهذا الشكل فقط:

📱 اسم الهاتف:
- 📺 الشاشة:
- ⚙️ المعالج:
- 💾 الذاكرة:
- 📷 الكاميرا:
- 🔋 البطارية:
- 🧠 نظام التشغيل:
- 🎮 الأداء في الألعاب:
- 🌡️ الحرارة في الصيف:
- ⭐ التقييم من 10:

2) إذا الرسالة ليست اسم هاتف:
رد فقط:
أرسل اسم هاتف فقط 📱

قواعد مهمة:
- لا كلام إضافي نهائياً
- لا أسئلة
- لا ترحيب
- بعد الرد اسكت مباشرة
"""
                },
                {
                    "role": "user",
                    "content": user_message
                }
            ],
            temperature=0.1,  # درجة حرارة منخفضة لضمان الالتزام الصارم بالقالب ومنع التخريف
            max_tokens=180    # حجم كافي للمواصفات لمنع انقطاع النص
        )

        return response.choices[0].message.content.strip()

    except Exception as e:
        print(f"خطأ في Groq API: {e}")
        return "حدث خطأ، أرسل اسم الهاتف مرة أخرى 📱"
