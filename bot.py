import os, subprocess, random, requests, json, time
from playwright.sync_api import sync_playwright

# --- CONFIG & VIRAL DATABASE ---
HOOK_PHRASES = [
    "Gak nyangka endingnya bakal gini... 😱",
    "Hanya 1% orang yang sadar keanehan di detik ke-5 🤔",
    "Nyesel kalau gak nonton sampai habis! 🔥",
    "Ini beneran atau editan ya? 🤯",
    "Kejadian langka yang terekam kamera 🌏"
]

def get_history():
    if not os.path.exists('history.txt'): return []
    with open('history.txt', 'r') as f: return f.read().splitlines()

def save_history(url):
    with open('history.txt', 'a') as f: f.write(url + '\n')

# --- ALGORITMA V5: VIRAL MUTATOR ---
def viral_mutate(input_file, output_file):
    print("🧠 Memproses Algoritma V5 Viral-Engine...")
    r_gamma = round(random.uniform(1.02, 1.07), 3)
    r_sharp = random.uniform(0.5, 1.5)
    hook_text = random.choice(HOOK_PHRASES)
    p_color = random.choice(['yellow', 'red', 'lime'])

    cmd = [
        'ffmpeg', '-i', input_file,
        '-vf', (
            f"hflip,scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,"
            f"unsharp=5:5:{r_sharp}:5:5:0,eq=gamma={r_gamma}:contrast=1.1:brightness=0.02:saturation=1.2,"
            f"zoompan=z='if(lte(it,1),1.5,min(zoom+0.001,1.1))':d=1:s=1080x1920:x='iw*0.01*sin(t)':y='ih*0.01*cos(t)',"
            f"drawtext=text='{hook_text}':fontcolor=white:fontsize=55:x=(w-text_w)/2:y=180:box=1:boxcolor=black@0.7,"
            f"drawbox=y=ih-15:color={p_color}:width=iw*t/20:height=15:t=fill" # Bar 20 detik
        ),
        '-af', "bass=g=5,atempo=1.01", 
        '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-preset', 'faster', '-crf', '20',
        '-y', output_file
    ]
    subprocess.run(cmd, check=True)

# --- UPLOADER KE FACEBOOK ---
def upload_to_fb(video_path):
    fb_cookies = os.environ.get('FB_COOKIES_JSON')
    if not fb_cookies: return print("❌ Cookies Tidak Ditemukan!")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(user_agent="Mozilla/5.0 (iPhone; CPU iPhone OS 17_4 like Mac OS X) AppleWebKit/605.1.15")
        context.add_cookies(json.loads(fb_cookies))
        page = context.new_page()
        
        try:
            page.goto('https://m.facebook.com/reels/create/')
            time.sleep(10)
            page.set_input_files("input[type='file']", video_path)
            
            caption = f"Menurut kalian ini asli atau settingan? 🤔👇 \n\n #fyp #viral #reels"
            page.wait_for_selector("text=Next")
            page.click("text=Next")
            page.fill("textarea", caption)
            time.sleep(5)
            page.click("text=Share")
            print("🚀 Video Berhasil Upload!")
        except Exception as e:
            print(f"❌ Gagal: {e}")
        finally:
            browser.close()

if __name__ == "__main__":
    os.makedirs('raw', exist_ok=True)
    os.makedirs('temp', exist_ok=True)
    history = get_history()
    videos = sorted([f for f in os.listdir('raw') if f.endswith('.mp4')])
    
    for v in videos:
        if v not in history:
            viral_mutate(f"raw/{v}", f"temp/final_{v}")
            upload_to_fb(f"temp/final_{v}")
            save_history(v)
            break
