import json
import os

def merge_all():
    main_file = 'videos.json'
    queue_dir = 'queue'
    
    if not os.path.exists(queue_dir) or not os.listdir(queue_dir):
        return

    # 1. قراءة الملف الرئيسي
    if os.path.exists(main_file):
        with open(main_file, 'r', encoding='utf-8') as f:
            try: videos = json.load(f)
            except: videos = []
    else: videos = []

    # 2. قراءة كل الملفات في الطابور
    new_files = [f for f in os.listdir(queue_dir) if f.endswith('.json')]
    
    # مصفوفات لفرز الطلبات
    new_video_entries = []
    like_requests = [] # [{ "video_id": "1", "action": "add" }]

    for filename in new_files:
        path = os.path.join(queue_dir, filename)
        with open(path, 'r', encoding='utf-8') as f:
            item = json.load(f)
            if 'file_id' in item: # ده فيديو جديد
                new_video_entries.append(item)
            elif 'video_id' in item: # ده طلب لايك
                like_requests.append(item)

    # 3. تنفيذ اللايكات أولاً على البيانات الحالية
    for req in like_requests:
        v_id = str(req['video_id'])
        v_action = req['action']
        for v in videos:
            if str(v['id']) == v_id:
                if v_action == "add": v['likes'] = v.get('likes', 0) + 1
                elif v_action == "remove": v['likes'] = max(0, v.get('likes', 0) - 1)

    # 4. دمج الفيديوهات الجديدة
    new_video_entries.sort(key=lambda x: x['timestamp'])
    for entry in new_video_entries:
        url = f"https://yellow-wind-75bb.ahhaga123456789.workers.dev/?file_id={entry['file_id']}"
        if any(v['url'] == url for v in videos): continue
        
        max_id = max([int(v['id']) for v in videos if str(v['id']).isdigit()] + [0])
        new_video = {
            "id": str(max_id + 1),
            "title": entry['title'] if entry['title'] else "اذكر الله",
            "url": url,
            "likes": 0
        }
        videos.insert(0, new_video)

    # 5. حفظ وتنظيف
    with open(main_file, 'w', encoding='utf-8') as f:
        json.dump(videos, f, ensure_ascii=False, indent=2)
    
    for filename in new_files:
        os.remove(os.path.join(queue_dir, filename))

if __name__ == "__main__":
    merge_all()
