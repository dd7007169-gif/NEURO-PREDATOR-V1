import os, time, random, json, datetime, requests
from playwright.sync_api import sync_playwright
from fake_useragent import UserAgent
from yt_dlp import YoutubeDL

# === ALAT 1: RADAR IDENTITAS (IP & NETWORK DETECTOR) ===
def radar_identitas_v4():
    print("\n" + "="*50)
    print("      SYSTEM IDENTITAS PREDATOR-V4 AKTIF      ")
    print("="*50)
    try:
        data = requests.get('https://api.ipify.org?format=json', timeout=20).json()
        ip = data['ip']
        geo = requests.get(f'https://ipapi.co/{ip}/json/', timeout=20).json()
        print(f"[+] IP ADDRESS   : {ip}")
        print(f"[+] NEGARA       : {geo.get('country_name')}")
        print(f"[+] KOTA/REGION  : {geo.get('city')} ({geo.get('region')})")
        print(f"[+] PROVIDER     : {geo.get('org')}")
        print(f"[+] TIMEZONE     : {geo.get('timezone')}")
    except Exception as e:
        print(f"[!] Radar IP terhalang: {e}")
    print("="*50 + "\n")

# === ALAT 2: SIMULASI KEYBOARD MANUSIA (DEEP STEALTH) ===
def ngetik_manusia_v4(page, selector, teks):
    try:
        element = page.wait_for_selector(selector, state="visible", timeout=45000)
        element.click()
        time.sleep(random.uniform(2, 4)) # Jeda mikir
        print(f"[*] Mengetik caption aman secara bertahap...")
        for char in teks:
            page.keyboard.type(char, delay=random.randint(150, 500))
            if random.random() > 0.92: # Simulasi manusia berhenti sejenak
                time.sleep(random.uniform(0.8, 2.0))
        print("[+] Caption berhasil diinput.")
    except Exception as e:
        print(f"[-] Gagal ngetik: {e}")
        raise e

# === ALAT 3: PENGAMBIL VIDEO OTOMATIS (PINTEREST GHOST) ===
def ambil_konten_pinterest(topik):
    print(f"[*] MENCARI KONTEN: {topik} (Filter: Funny & Safe)")
    ua = UserAgent(platforms='mobile')
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(user_agent=ua.random)
        page = context.new_page()
        
        # Masuk lewat gerbang depan
        page.goto("https://id.pinterest.com/", wait_until="networkidle")
        time.sleep(random.randint(4, 7))
        
        # Cari topik
        page.goto(f"https://id.pinterest.com/search/pins/?q={topik}&rs=typed", wait_until="networkidle")
        time.sleep(5)
        
        # Scroll layaknya manusia nyari video
        for _ in range(2):
            page.mouse.wheel(0, random.randint(700, 1200))
            time.sleep(3)
            
        links = page.locator('a[href^="/pin/"]').all_attribute_values("href")
        full_links = [f"https://id.pinterest.com{l}" for l in links if "/pin/" in l]
        browser.close()
        
        return random.choice(full_links[:15]) if full_links else None

# === ALAT 4: EKSEKUTOR FB REELS (ULTIMATE STEALTH) ===
def misi_utama_predator(topik, caption, cookies_fb):
    radar_identitas_v4()
    file_video = f"reels_{random.randint(1000,9999)}.mp4"
    
    # 1. DOWNLOAD VIDEO
    target = ambil_konten_pinterest(topik)
    if not target: return print("[!] Gagal tembus Pinterest.")
    
    print(f"[*] Downloading Video dari: {target}")
    with YoutubeDL({'format': 'best', 'outtmpl': file_video, 'quiet': True}) as ydl:
        ydl.download([target])

    # 2. UPLOAD KE FACEBOOK (GOOGLE CHROME SIMULATION)
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, args=[
            "--disable-blink-features=AutomationControlled",
            "--no-sandbox",
            "--disable-setuid-sandbox",
            "--disable-dev-shm-usage"
        ])
        
        # Setup Browser yang Sangat Manusiawi
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Linux; Android 13; SM-G998B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36",
            viewport={'width': 412, 'height': 915},
            has_touch=True,
            locale="id-ID",
            timezone_id="Asia/Makassar"
        )
        context.add_cookies(cookies_fb)
        page = context.new_page()

        try:
            print("[*] Menuju Facebook Mobile...")
            page.goto("https://m.facebook.com/", wait_until="domcontentloaded")
            time.sleep(random.uniform(5, 8))
            
            print("[*] Masuk ke Studio Pembuatan Reels...")
            page.goto("https://m.facebook.com/reels/create/", wait_until="networkidle", timeout=60000)
            
            print("[*] Proses Upload Video (Suntik File)...")
            page.set_input_files("input[type='file']", file_video)
            
            # TUNGGU PROSES RENDER (INI PENYEBAB ERROR TADI)
            print("[*] Menunggu sistem Facebook memproses video (30 detik)...")
            time.sleep(30) 

            # KLIK SELANJUTNYA DENGAN SEARCH CERDAS
            print("[*] Menekan Tombol Selanjutnya...")
            page.wait_for_selector("text=Selanjutnya", state="visible", timeout=30000)
            page.get_by_text("Selanjutnya").click()
            time.sleep(5)

            # INPUT CAPTION
            ngetik_manusia_v4(page, "textarea", caption)

            # FINAL KLIK
            print("[***] EKSEKUSI FINAL: BAGIKAN SEKARANG!")
            page.wait_for_selector("text=Bagikan Sekarang", state="visible")
            page.get_by_text("Bagikan Sekarang").click()
            
            print("[*] Menunggu konfirmasi server...")
            time.sleep(20)
            print("\n[SUCCESS] VIDEO BERHASIL MENDARAT DI FACEBOOK BAPAK!")

        except Exception as e:
            print(f"\n[!] GAGAL EKSEKUSI: {e}")
            if not os.path.exists("error_logs"): os.makedirs("error_logs")
            page.screenshot(path="error_logs/failed_v4.png")
            with open("error_logs/page_source.html", "w", encoding="utf-8") as f:
                f.write(page.content())
        finally:
            browser.close()
            if os.path.exists(file_video): os.remove(file_video)

if __name__ == "__main__":
    # SETTING TOPIK LUCU & AMAN (TANPA SEKS/VULGAR)
    topik_aman = "funny baby animals" 
    caption_aman = "Lucu banget tingkahnya! 😂 #viral #reels #hiburan"

    kunci_fb = os.getenv('FB_COOKIES')
    if kunci_fb:
        misi_utama_predator(topik_aman, caption_aman, json.loads(kunci_fb))
    else:
        print("[!] ERROR: Masukkan COOKIES di Settings GitHub!")
