import os, requests, random, time, re, subprocess, json, socket
from datetime import datetime
from playwright.sync_api import sync_playwright
from yt_dlp import YoutubeDL

def ghost_log(msg):
    print(f"🛰️  [PREDATOR-V6-FULL] {datetime.now().strftime('%H:%M:%S')} - {msg}")

# === ALAT 1: RADAR SOCKET & IP (DETEKSI JALUR) ===
def radar_jalur():
    ghost_log("📡 Membuka Radar Socket & Jalur IP...")
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip_internal = s.getsockname()[0]
        s.close()
        info = requests.get('https://ipapi.co/json/', timeout=20).json()
        print(f"    [!] INTERNAL IP : {ip_internal}")
        print(f"    [!] PUBLIC IP   : {info.get('ip')}")
        print(f"    [!] PROVIDER    : {info.get('org')}")
        ghost_log("✅ Jalur Terverifikasi.")
    except: ghost_log("⚠️ Radar IP terhalang, tetap lanjut.")

# === ALAT 2: DEEP PINTEREST PENETRATOR (ANTI-404) ===
def tembus_pinterest_v6(topik):
    ghost_log(f"🕵️  Operasi Penembusan Pinterest: {topik}...")
    try:
        # Gunakan yt-dlp untuk bypass pencarian video Pinterest secara langsung
        with YoutubeDL({'quiet': True, 'no_warnings': True, 'extract_flat': True}) as ydl:
            search_res = ydl.extract_info(f"https://id.pinterest.com/search/pins/?q={topik}", download=False)
            if 'entries' in search_res:
                # Ambil 1 video secara acak dari hasil pencarian
                target = random.choice(search_res['entries'])
                video_url = target['url']
                ghost_log(f"✅ Target Terkunci: {video_url}")
                return video_url
    except Exception as e:
        ghost_log(f"❌ Pinterest Gagal: {e}")
    return None

# === ALAT 3: REVOLUTION ENCODING (FFMPEG) ===
def perkuat_video_v6(input_file):
    output_file = "reels_predator.mp4"
    ghost_log("🛠️  ENCODING: Mengubah Metadata & Hash Video...")
    try:
        # Menambah noise dan metadata unik agar tidak terdeteksi konten lama
        cmd = [
            'ffmpeg', '-i', input_file,
            '-vf', f'eq=brightness={random.uniform(-0.02, 0.02)}:contrast=1.05,scale=720:1280',
            '-c:v', 'libx264', '-preset', 'ultrafast', '-crf', '28',
            '-metadata', f'title=Rev_{random.getrandbits(32)}',
            '-metadata', 'model=Samsung S24 Ultra', '-y', output_file
        ]
        subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return output_file if os.path.exists(output_file) else input_file
    except: return input_file

# === ALAT 4: INJECT FB REELS (PRIVATE PROFILE) ===
def tembak_fb_private(video_path, cookies):
    ghost_log("🚀 Menembus Facebook via Injeksi Browser...")
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        # Samaran Mobile Sempurna
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Linux; Android 14; SM-S928B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36",
            viewport={'width': 412, 'height': 915},
            has_touch=True,
            locale="id-ID",
            timezone_id="Asia/Makassar"
        )
        context.add_cookies(cookies)
        page = context.new_page()

        try:
            page.goto("https://m.facebook.com/reels/create/", wait_until="networkidle", timeout=90000)
            
            if "login" in page.url:
                ghost_log("❌ COOKIES MATI! Silakan ambil Cookie baru di browser.")
                return

            ghost_log("📤 Menyuntikkan Video ke Server FB...")
            page.set_input_files("input[type='file']", video_path)
            time.sleep(30) # Tunggu render video

            ghost_log("➡️ Klik Selanjutnya...")
            page.get_by_text("Selanjutnya").click()
            time.sleep(5)

            ghost_log("✍️ Mengetik Caption (Mode Manusia)...")
            page.wait_for_selector("textarea")
            caption = f"Lucu bangeet! 😂🔥 #{random.randint(1000,9999)}"
            for char in caption:
                page.keyboard.type(char, delay=random.randint(100, 400))
            
            ghost_log("🚀 PUBLIKASIKAN SEKARANG!")
            page.get_by_text("Bagikan Sekarang").click()
            
            time.sleep(20)
            ghost_log("✅ BERHASIL TOTAL! Misi Selesai.")
            
        except Exception as e:
            ghost_log(f"⚠️ Kegagalan: {e}")
            page.screenshot(path="failed_mission.png")
        finally:
            browser.close()

def engine_v6():
    radar_jalur()
    c_hex = os.getenv("COOKIE_HEX", "").strip()
    if not c_hex: return ghost_log("❌ Secrets COOKIE_HEX Belum Diisi!")

    try:
        # Parser Cookie HEX ke format Playwright
        raw_cookie = bytes.fromhex(c_hex).decode('utf-8')
        fb_cookies = []
        for item in raw_cookie.split('; '):
            if '=' in item:
                name, value = item.split('=', 1)
                fb_cookies.append({'name': name, 'value': value, 'domain': '.facebook.com', 'path': '/'})

        # Jalankan Pencarian
        video_url = tembus_pinterest_v6("funny animal shorts viral")
        if video_url:
            # Download Video
            with YoutubeDL({'outtmpl': 'raw_video.mp4', 'quiet': True}) as ydl:
                ydl.download([video_url])
            
            # Olah & Tembak
            final_vid = perkuat_video_v6("raw_video.mp4")
            tembak_fb_private(final_vid, fb_cookies)
            
            # Bersihkan Jejak
            for f in ["raw_video.mp4", "reels_predator.mp4"]:
                if os.path.exists(f): os.remove(f)
        else:
            ghost_log("❌ Gagal menembus Pinterest.")
    except Exception as e:
        ghost_log(f"⚠️ Masalah: {e}")

if __name__ == "__main__":
    engine_v6()
