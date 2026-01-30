import json
import os
import random

def update_json():
    file_id = os.getenv('FILE_ID')
    telegram_caption = os.getenv('VIDEO_TITLE')
    if not file_id: return

    file_path = 'videos.json'
    
    # 1. قراءة أحدث نسخة من الملف "حالاً"
    videos = []
    if os.path.exists(file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                videos = json.load(f)
        except: videos = []

    full_url = f"https://yellow-wind-75bb.ahhaga123456789.workers.dev/?file_id={file_id}"
    
    # منع التكرار
    if any(v.get('url') == full_url for v in videos):
        return

    # حساب الـ ID بناءً على الموجود فعلياً
    max_id = 0
    if videos:
        ids = [int(v['id']) for v in videos if str(v['id']).isdigit()]
        max_id = max(ids) if ids else len(videos)
    
    new_id = str(max_id + 1)
    final_title = telegram_caption if (telegram_caption and telegram_caption.strip()) else "اذكر الله"

    new_video = {
        "id": new_id,
        "title": final_title,
        "url": full_url,
        "likes": 0
    }

    # إضافة الفيديو في أول القائمة
    videos.insert(0, new_video)

    # الحفظ
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(videos, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    update_json()
