import json
import re
import requests

# ලංකාවේ trending දේවල් ගන්න සුදුසු Tag එකක් 
TAG = "srilanka"

# වැඩ කරන පොදු ProxiTok සර්වර් ලැයිස්තුවක් (එකක් වැඩ නොකලොත් අනෙකෙන් ඔටෝම වැඩේ කරයි)
INSTANCES = [
    "https://proxitok.pussthecat.org",
    "https://tok.adminforge.de",
    "https://proxitok.privacydev.net",
    "https://tt.opnxng.com"
]

def fetch_fresh_videos():
    video_ids = []
    
    for instance in INSTANCES:
        url = f"{instance}/tag/{TAG}/rss"
        try:
            print(f"Trying to fetch from: {instance}")
            response = requests.get(url, timeout=15)
            if response.status_code == 200:
                # Regex මඟින් RSS එකේ තියෙන වීඩියෝ ID සියල්ල වෙන් කර ගැනීම
                ids = re.findall(r'/video/(\d+)', response.text)
                if ids:
                    video_ids = list(set(ids)) # ඩූප්‍ලිකේට් අයින් කිරීම
                    print(f"Successfully fetched {len(video_ids)} fresh videos!")
                    break
        except Exception as e:
            print(f"Server {instance} failed or timed out: {e}")
            continue
            
    if video_ids:
        # පැරණි වීඩියෝ තියා ගන්නේ නැතිව හැමවිටම අලුත්ම ලිස්ට් එකෙන් Overwrite කරයි
        with open("videos.json", "w") as f:
            json.dump(video_ids, f, indent=4)
        print("videos.json successfully updated with 100% fresh content.")
    else:
        print("Error: Could not fetch any videos from public proxies this time.")

if __name__ == "__main__":
    fetch_fresh_videos()
