import json
import os
import time

def create_temp_video():
    file_id = os.getenv('FILE_ID')
    telegram_caption = os.getenv('VIDEO_TITLE')
    if not file_id: return

    new_video = {
        "temp_id": file_id, 
        "title": telegram_caption if (telegram_caption and telegram_caption.strip()) else "اذكر الله",
        "url": f"https://yellow-wind-75bb.ahhaga123456789.workers.dev/?file_id={file_id}",
        "likes": 0,
        "timestamp": time.time()
    }

    os.makedirs('temp_videos', exist_ok=True)

    with open(f'temp_videos/{file_id}.json', 'w', encoding='utf-8') as f:
        json.dump(new_video, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    create_temp_video()
