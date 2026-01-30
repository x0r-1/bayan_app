import json
import os

def merge_all():
    main_file = 'videos.json'
    queue_dir = 'queue'
    
    # التأكد من وجود المجلد
    if not os.path.exists(queue_dir) or not os.listdir(queue_dir):
        print("🚀 المجلد فارغ، لا توجد مهام حالياً.")
        return

    # 1. قراءة الملف الرئيسي
    if os.path.exists(main_file):
        with open(main_file, 'r', encoding='utf-8') as f:
            try:
                videos = json.load(f)
            except:
                videos = []
    else:
        videos = []

    # 2. قراءة كل الملفات في الطابور
    new_files = [f for f in os.listdir(queue_dir) if f.endswith('.json')]
    new_video_entries = []
    like_requests = []

    for filename in new_files:
        path = os.path.join(queue_dir, filename)
        with open(path, 'r', encoding='utf-8') as f:
            try:
                item = json.load(f)
                if 'file_id' in item:
                    new_video_entries.append(item)
                elif 'video_id' in item:
                    like_requests.append(item)
            except:
                continue

    # 3. تنفيذ اللايكات أولاً
    for req in like_requests:
        v_id = str(req.get('video_id'))
        v_action = req.get('action')
        for v in videos:
            if str(v['id']) == v_id:
                if v_action == "add":
                    v['likes'] = v.get('likes', 0) + 1
                elif v_action == "remove":
                    v['likes'] = max(0, v.get('likes', 0) - 1)

    # 4. دمج الفيديوهات الجديدة
    # استخدام .get لضمان عدم حدوث KeyError لو التايم ستامب مش موجود
    new_video_entries.sort(key=lambda x: x.get('timestamp', 0))
    
    for entry in new_video_entries:
        f_id = entry.get('file_id')
        url = f"https://yellow-wind-75bb.ahhaga123456789.workers.dev/?file_id={f_id}"
        
        # # التأكد من عدم التكرار
        # if any(v.get('url') == url for v in videos):
        #     continue
        
        # حساب الـ ID الجديد
        try:
            max_id = max([int(v['id']) for v in videos if str(v['id']).isdigit()] + [0])
        except:
            max_id = len(videos)

        # الحل الجذري لمشكلة الـ Title: بيجرب يقرأ title ولو ملهاش بيقرأ video_title
        final_title = entry.get('title') or entry.get('video_title') or "اذكر الله"
        
        new_video = {
            "id": str(max_id + 1),
            "title": final_title,
            "url": url,
            "likes": 0
        }
        # إضافة الفيديو في أول القائمة
        videos.insert(0, new_video)

    # 5. حفظ وتنظيف
    with open(main_file, 'w', encoding='utf-8') as f:
        json.dump(videos, f, ensure_ascii=False, indent=2)
    
    for filename in new_files:
        try:
            os.remove(os.path.join(queue_dir, filename))
        except:
            pass
            
    print(f"✅ تم دمج {len(new_video_entries)} فيديوهات و {len(like_requests)} طلبات لايك.")

if __name__ == "__main__":
    merge_all()
