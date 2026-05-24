import sqlite3

DB_NAME = "phones_bot.db"

def create_tables():
    """إنشاء جدول الهواتف وسجل المحادثات إذا لم تكن موجودة"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # جدول مواصفات الهواتف
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS phones (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        brand TEXT NOT NULL,
        model TEXT NOT NULL UNIQUE,
        specs TEXT NOT NULL,
        price TEXT NOT NULL
    )
    """)
    
    conn.commit()
    conn.close()

def insert_phone(brand, model, specs, price):
    """دالة مخصصة لك (أو لملف admin.py) لإضافة هاتف جديد"""
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO phones (brand, model, specs, price) VALUES (?, ?, ?, ?)",
            (brand.lower(), model.lower(), specs, price)
        )
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        return False  # الهاتف موجود مسبقاً

def search_phone_in_db(text):
    """البحث في الجدول عن أي طراز يطابق نص رسالة المستخدم"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # جلب كل الهواتف لمقارنتها بنص الرسالة
    cursor.execute("SELECT model, brand, specs, price FROM phones")
    all_phones = cursor.fetchall()
    conn.close()
    
    text_lower = text.lower()
    for model, brand, specs, price in all_phones:
        if model in text_lower:
            return {
                "model": model.title(),
                "brand": brand.title(),
                "specs": specs,
                "price": price
            }
    return None

# تشغيل دالة إنشاء الجداول للتأكد من جاهزيتها فوراً
create_tables()