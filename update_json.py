import json
import os
import sys

def update_json():
    # استلام البيانات من GitHub Action
    file_id = os.getenv('FILE_ID')
    title = os.getenv('VIDEO_TITLE')
    # رابط الـ Worker بتاعك (Proxy)
    worker_url = "https://yellow-wind-75bb.ahhaga123456789.workers.dev/?file_id="
    
    file_path = 'videos.json'

    # 1. قراءة البيانات الحالية
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            try:
                videos = json.load(f)
            except:
                videos = []
    else:
        videos = []

    # 2. التأكد إن الفيديو مش موجود قبل كدة (عشان ميتكررش)
    full_url = f"{worker_url}{file_id}"
    if any(v.get('url') == full_url for v in videos):
        print("الفيديو موجود بالفعل!")
        return

    # 3. إضافة الفيديو الجديد
    new_video = {
        "id": str(len(videos) + 1),
        "title": title,
        "url": full_url
    }
    videos.append(new_video)

    # 4. حفظ التعديلات
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(videos, f, ensure_ascii=False, indent=2)
    print(f"تم إضافة الفيديو بنجاح: {title}")

if __name__ == "__main__":
    update_json()
