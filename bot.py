import os, requests, random, time, re, subprocess, json, socket
from datetime import datetime
from playwright.sync_api import sync_playwright
from yt_dlp import YoutubeDL

def predator_log(msg):
    print(f"🛰️  [ULTRA-PREDATOR-V8] {datetime.now().strftime('%H:%M:%S')} - {msg}")

def cek_radar():
    predator_log("📡 Memeriksa Jalur Socket...")
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip_internal = s.getsockname()[0]
        s.close()
        pub_ip = requests.get('https://api.ipify.org?format=json', timeout=10).json()
        print(f"    [!] IP INTERNAL : {ip_internal}")
        print(f"    [!] IP PUBLIK   : {pub_ip.get('ip')}")
        predator_log("✅ Radar Berhasil Diverifikasi.")
    except: predator_log("⚠️ Radar terganggu, lanjut misi.")

def cari_target(topik):
    predator_log(f"🕵️  Operasi Pinterest: {topik}...")
    try:
        # Menggunakan yt-dlp untuk menghindari error 404
        with YoutubeDL({'quiet': True, 'no_warnings': True, 'extract_flat': True}) as ydl:
            res = ydl.extract_info(f"https://id.pinterest.com/search/pins/?q={topik}", download=False)
            if 'entries' in res:
                pilihan = random.choice(res['entries'])
                return pilihan['url']
    except: return None

def tembak_fb(video_path, cookies):
    predator_log("🚀 Memulai Injeksi ke Profil Facebook...")
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Linux; Android 14; SM-S928B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36",
            viewport={'width': 412, 'height': 915},
            has_touch=True
        )
        context.add_cookies(cookies)
        page = context.new_page()
        try:
            page.goto("https://m.facebook.com/reels/create/", wait_until="networkidle", timeout=90000)
            if "login" in page.url:
                predator_log("❌ COOKIES MATI! Ambil yang baru dari browser Chrome HP.")
                return
            predator_log("📤 Uploading Video...")
            page.set_input_files("input[type='file']", video_path)
            time.sleep(35) # Jeda upload
            page.get_by_text("Selanjutnya").click()
            time.sleep(5)
            predator_log("✍️ Mengetik Caption (Mode Manusia)...")
            page.wait_for_selector("textarea")
            page.keyboard.type(f"Hiburan BAN JAK! 😂🔥 #{random.randint(1000,9999)}", delay=200)
            predator_log("🚀 PUBLISH!")
            page.get_by_text("Bagikan Sekarang").click()
            time.sleep(20)
            predator_log("✅ MISI SUKSES!")
        except Exception as e:
            predator_log(f"⚠️ Gagal: {e}")
        finally: browser.close()

def jalan_mesin():
    cek_radar()
    kunci_raw = os.getenv("KUNCI_PREDATOR", "").strip()
    # Filter karakter Hex agar fromhex() tidak error
    kunci_bersih = "".join(filter(lambda x: x.lower() in "0123456789abcdef", kunci_raw))
    
    if not kunci_bersih or len(kunci_bersih) % 2 != 0:
        return predator_log("❌ ERROR: KUNCI_PREDATOR tidak valid atau panjangnya ganjil!")

    try:
        # Gunakan 'ignore' pada decode untuk menghindari error UTF-8
        decoded = bytes.fromhex(kunci_bersih).decode('utf-8', errors='ignore')
        fb_cookies = []
        for item in decoded.split(';'):
            item = item.strip()
            if '=' in item:
                n, v = item.split('=', 1)
                fb_cookies.append({'name': n, 'value': v, 'domain': '.facebook.com', 'path': '/'})

        target_url = cari_target("funny animal viral")
        if target_url:
            with YoutubeDL({'outtmpl': 'vid_raw.mp4', 'quiet': True}) as ydl:
                ydl.download([target_url])
            # FFmpeg untuk ubah sidik jari video
            subprocess.run(['ffmpeg', '-i', 'vid_raw.mp4', '-vf', 'scale=720:1280', '-y', 'vid_final.mp4'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            tembak_fb("vid_final.mp4", fb_cookies)
            # Bersihkan jejak
            for f in ["vid_raw.mp4", "vid_final.mp4"]:
                if os.path.exists(f): os.remove(f)
        else: predator_log("❌ Pinterest Gagal mendapatkan link.")
    except Exception as e: predator_log(f"⚠️ Masalah: {e}")

if __name__ == "__main__":
    jalan_mesin()
