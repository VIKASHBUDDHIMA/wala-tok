import json
import re
import requests

# ඔබට අවශ්‍ය වීඩියෝ වර්ග මෙතනට දෙන්න (ඉංග්‍රීසි අකුරෙන්, හිස්තැන් නැතිව).
# මේවා TikTok එකේ සර්ච් වෙන Hashtags විදිහටයි වැඩ කරන්නේ.
TAGS = ["srilanka", "trending", "dance"]

# නොමිලේ වීඩියෝ හොයාගන්න පාවිච්චි කරන Public Servers
INSTANCES = [
    "https://proxitok.pussthecat.org",
    "https://tok.adminforge.de",
    "https://proxitok.privacydev.net",
    "https://tt.opnxng.com"
]

def fetch_fresh_videos():
    video_ids = []
    
    for tag in TAGS:
        for instance in INSTANCES:
            url = f"{instance}/tag/{tag}/rss"
            try:
                print(f"Searching #{tag} from: {instance}")
                response = requests.get(url, timeout=15)
                if response.status_code == 200:
                    ids = re.findall(r'/video/(\d+)', response.text)
                    if ids:
                        video_ids.extend(ids) # වීඩියෝ ටික ලැයිස්තුවට එකතු කිරීම
                        print(f"Found {len(ids)} videos for #{tag}!")
                        break # එක සර්වර් එකකින් හම්බුනා නම් ඊළඟ ටැග් එකට යනවා
            except Exception as e:
                print(f"Server {instance} failed.")
                continue
                
    if video_ids:
        # ඩූප්‍ලිකේට් අයින් කරලා අලුත්ම ලිස්ට් එක සේව් කිරීම
        final_ids = list(set(video_ids))
        with open("videos.json", "w") as f:
            json.dump(final_ids, f, indent=4)
        print(f"Success! Saved {len(final_ids)} fresh videos.")
    else:
        print("Error: Could not fetch videos right now.")

if __name__ == "__main__":
    fetch_fresh_videos()
