# اسم الملف: admin.py

import database

# ⚠️ استبدل هذا الرقم بمعرف حسابك الشخصي على إنستغرام (Instagram User ID)
# يمكنك معرفة الـ ID الخاص بك عبر مواقع مثل instagramidfinder.com أو طباعته من ملف bot.py عند مراسلة البوت
ADMIN_ID = "1234567890" 

def is_admin(user_id):
    """التحقق مما إذا كان مرسل الرسالة هو المشرف"""
    return str(user_id) == ADMIN_ID

def is_admin_command(text):
    """التحقق مما إذا كانت الرسالة تبدأ بكلمة الماستر للأوامر"""
    return text.strip().startswith("أضف هاتف:")

def handle_command(text):
    """تفكيك نص الرسالة وإضافة الهاتف إلى قاعدة البيانات"""
    try:
        # إزالة كلمة "أضف هاتف:" من البداية
        command_body = text.replace("أضف هاتف:", "").strip()
        
        # تفكيك النص بناءً على الفاصلة "|"
        # الصيغة المتوقعة: الماركة | الموديل | المواصفات | السعر
        parts = [part.strip() for part in command_body.split("|")]
        
        if len(parts) != 4:
            return (
                "❌ خطأ في صيغة الأمر!\n"
                "الصيغة الصحيحة هي:\n"
                "أضف هاتف: الماركة | الموديل | المواصفات | السعر\n\n"
                "مثال:\n"
                "أضف هاتف: Apple | iPhone 15 | شاشة 6.1, كاميرا 48MP | 800 دولار"
            )
            
        brand, model, specs, price = parts
        
        # محاولة إدخال البيانات في قاعدة البيانات عبر ملف database.py
        success = database.insert_phone(brand, model, specs, price)
        
        if success:
            return f"✅ تم إضافة الهاتف بنجاح!\n📱 {brand.title()} {model.title()}\n💰 السعر: {price}"
        else:
            return f"⚠️ هذا الموديل ({model}) موجود بالفعل في قاعدة البيانات!"
            
    except Exception as e:
        return f"❌ حدث خطأ أثناء المعالجة: {e}"