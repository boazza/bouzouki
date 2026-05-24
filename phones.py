# اسم الملف: phones.py

import database

def contains_phone_keyword(text):
    """التحقق مما إذا كان الهاتف مطلوباً وموجوداً في قاعدة البيانات"""
    # نبحث في قاعدة البيانات، إذا عثرنا على نتيجة يعني أن الهاتف متوفر لدينا
    phone = database.search_phone_in_db(text)
    if phone:
        return True
    return False

def get_phone_info(text):
    """استرجاع بيانات الهاتف من قاعدة البيانات وتنسيقها للمستخدم بخط مرتب وعريض"""
    phone = database.search_phone_in_db(text)
    
    if phone:
        response = (
            f"📱 *{phone['brand']} {phone['model']}*\n\n"
            f"🛠️ *المواصفات:* {phone['specs']}\n"
            f"💰 *السعر التقريبي:* {phone['price']}"
        )
        return response
    
    # إذا لم يجد الهاتف، يعيد None لكي يتدخل الذكاء الاصطناعي ai.py للرد
    return None