import json
import os
import random
import time

def update_json():
    file_id = os.getenv('FILE_ID')
    telegram_caption = os.getenv('VIDEO_TITLE')
    
    if not file_id: return

    file_path = 'videos.json'
    captions_path = 'captions.json'

    # قراءة البيانات مع محاولة التأكد إن مفيش حد تاني فاتح الملف
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            try:
                videos = json.load(f)
            except:
                videos = []
    else:
        videos = []

    full_url = f"https://yellow-wind-75bb.ahhaga123456789.workers.dev/?file_id={file_id}"
    if any(v.get('url') == full_url for v in videos):
        print("الفيديو موجود!")
        return

    # --- حساب الـ ID العددي بطريقة أمنة ---
    # بنشوف أكبر ID موجود ونزود عليه 1، لو مفيش بنبدأ بـ 1
    try:
        max_id = max([int(v['id']) for v in videos if str(v['id']).isdigit()] + [0])
    except:
        max_id = len(videos)
    
    new_id = str(max_id + 1)

    # تحديد العنوان
    if not telegram_caption or telegram_caption.strip() == "":
        final_title = "اذكر الله"
    else:
        final_title = telegram_caption

    new_video = {
        "id": new_id, # رجعنا للـ ID اللي بتحبه
        "title": final_title,
        "url": full_url,
        "likes": 0
    }

    # إضافة في البداية
    videos.insert(0, new_video)

    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(videos, f, ensure_ascii=False, indent=2)
    
    print(f"✅ تم إضافة فيديو جديد بـ ID: {new_id}")

if __name__ == "__main__":
    update_json()
