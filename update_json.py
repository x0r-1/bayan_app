import json
import os
import random
import uuid  # استيراد مكتبة الـ UUID

def update_json():
    # 1. استلام البيانات من GitHub Action
    file_id = os.getenv('FILE_ID')
    telegram_caption = os.getenv('VIDEO_TITLE')
    
    if not file_id:
        print("❌ لم يتم العثور على FILE_ID")
        return

    worker_url = "https://yellow-wind-75bb.ahhaga123456789.workers.dev/?file_id="
    file_path = 'videos.json'
    captions_path = 'captions.json'

    # 2. تحديد الوصف (من تليجرام أو عشوائي)
    is_empty = not telegram_caption or telegram_caption.strip() == "" or "فيديو جديد من أثر" in telegram_caption
    
    if is_empty:
        if os.path.exists(captions_path):
            with open(captions_path, 'r', encoding='utf-8') as f:
                random_captions = json.load(f)
                final_title = random.choice(random_captions)
        else:
            final_title = "اذكر الله" 
    else:
        final_title = telegram_caption

    # 3. قراءة بيانات الفيديوهات الحالية (القراءة الفورية لآخر نسخة)
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            try:
                videos = json.load(f)
            except:
                videos = []
    else:
        videos = []

    # 4. التأكد من عدم التكرار باستخدام الـ file_id في الرابط
    full_url = f"{worker_url}{file_id}"
    if any(v.get('url') == full_url for v in videos):
        print("⚠️ الفيديو موجود بالفعل!")
        return

    # 5. إضافة الفيديو الجديد باستخدام UUID فريد
    # استخدام الـ uuid4 بيضمن إن حتى لو 100 فيديو اترفعوا في نفس الثانية مفيش ID هيشبه التاني
    new_video = {
        "id": str(uuid.uuid4())[:8],  # بناخد أول 8 حروف من رقم فريد جداً
        "title": final_title,
        "url": full_url,
        "likes": 0
    }
    
    # نضع الفيديو الجديد في أول القائمة (عشان يظهر أحدث فيديو فوق في التطبيق)
    videos.insert(0, new_video)

    # 6. حفظ التعديلات
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(videos, f, ensure_ascii=False, indent=2)
    
    print(f"✅ تم إضافة الفيديو بنجاح! ID الجديد: {new_video['id']}")

if __name__ == "__main__":
    update_json()
