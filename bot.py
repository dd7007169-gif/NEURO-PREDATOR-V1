import os, time, random, json, datetime, requests
from playwright.sync_api import sync_playwright
from fake_useragent import UserAgent
from yt_dlp import YoutubeDL

# === ALAT 1: DETEKSI IDENTITAS & IP ===
def cek_identitas_palsu():
    try:
        res = requests.get('https://api.ipify.org?format=json', timeout=10).json()
        print(f"\n[!] MEMULAI SAMARAN PADA IP: {res['ip']}")
        print(f"[!] BROWSER: Google Chrome (Official Build) - Windows 10\n")
    except: pass

# === ALAT 2: GERAKAN MOUSE & KEYBOARD MANUSIA ===
def aksi_manusia(page, aksi, selector=None, teks=None):
    # Jeda berpikir sebelum bertindak
    time.sleep(random.uniform(1.5, 3.5))
    
    if aksi == "ketik" and selector and teks:
        element = page.wait_for_selector(selector)
        element.click()
        for char in teks:
            page.keyboard.type(char, delay=random.randint(100, 300))
    elif aksi == "klik" and selector:
        # Gerakan mouse acak ke elemen sebelum klik
        box = page.locator(selector).bounding_box()
        if box:
            page.mouse.move(box['x'] + random.randint(5, 10), box['y'] + random.randint(5, 10), steps=20)
            page.mouse.click(box['x'] + box['width']/2, box['y'] + box['height']/2)

# === ALAT 3: PENCARIAN PINTEREST (GAYA MANUSIA) ===
def cari_konten_aman_pinterest(keyword):
    print(f"[*] Pinterest: Masuk sebagai Pengguna Chrome...")
    ua = UserAgent(platforms='mobile') # Pakai mobile karena lebih mudah ditembus
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, args=[
            "--disable-blink-features=AutomationControlled",
            "--no-sandbox"
        ])
        context = browser.new_context(user_agent=ua.random)
        page = context.new_page()
        
        # 1. Masuk Beranda Dulu (Bukan langsung Search)
        page.goto("https://id.pinterest.com/", wait_until="networkidle")
        time.sleep(random.randint(3, 5))
        
        # 2. Cari di Kotak Pencarian
        page.goto(f"https://id.pinterest.com/search/pins/?q={keyword}&rs=typed", wait_until="networkidle")
        time.sleep(5)
        
        # 3. Scroll layar layaknya orang nyari video
        page.mouse.wheel(0, 1500)
        time.sleep(3)
        
        links = page.locator('a[href^="/pin/"]').all_attribute_values("href")
        full_links = [f"https://id.pinterest.com{l}" for l in links if "/pin/" in l]
        browser.close()
        return random.choice(full_links[:12]) if full_links else None

# === EKSEKUSI UTAMA: PREDATOR GHOST MODE ===
def eksekusi_misi_ghost(topik, caption, cookies_fb):
    cek_identitas_palsu()
    video_file = "predator_clean.mp4"
    
    # STEP 1: CARI & DOWNLOAD
    link_target = cari_konten_aman_pinterest(topik)
    if not link_target: return print("[!] Konten tidak ditemukan.")
    
    with YoutubeDL({'format': 'best', 'outtmpl': video_file, 'quiet': True}) as ydl:
        ydl.download([link_target])

    # STEP 2: UPLOAD KE FB (FULL CHROME MIMIC)
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, args=["--disable-blink-features=AutomationControlled"])
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Linux; Android 13; SM-S918B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36",
            viewport={'width': 393, 'height': 852},
            has_touch=True
        )
        context.add_cookies(cookies_fb)
        page = context.new_page()

        try:
            print("[*] FB: Membuka Beranda...")
            page.goto("https://m.facebook.com/", wait_until="networkidle")
            time.sleep(4) # Scrolling beranda sebentar
            
            print("[*] FB: Menuju Halaman Reels...")
            page.goto("https://m.facebook.com/reels/create/", wait_until="networkidle")
            
            print("[*] FB: Input Video...")
            page.set_input_files("input[type='file']", video_file)
            time.sleep(15) 

            print("[*] FB: Navigasi Tombol...")
            aksi_manusia(page, "klik", "text=Selanjutnya")
            
            print("[*] FB: Mengetik Caption Gaya Manusia...")
            aksi_manusia(page, "ketik", "textarea", caption)

            print("[***] FB: EKSEKUSI TERBITKAN!")
            aksi_manusia(page, "klik", "text=Bagikan Sekarang")
            
            time.sleep(15)
            print("[SUCCESS] MISI SELESAI: Video Berhasil Terbit tanpa Terdeteksi!")
            
        except Exception as e:
            print(f"[!] Gagal: {e}")
            if not os.path.exists("error_logs"): os.makedirs("error_logs")
            page.screenshot(path="error_logs/failed_ghost_mode.png")
        finally:
            browser.close()
            if os.path.exists(video_file): os.remove(video_file)

if __name__ == "__main__":
    # KONTEN BERSIH & AMAN (LUCU)
    search_term = "funny kids and cats" 
    caption_reels = "Bikin ngakak terus! 😂 #lucu #viral #reels"

    raw_cookies = os.getenv('FB_COOKIES')
    if raw_cookies:
        eksekusi_misi_ghost(search_term, caption_reels, json.loads(raw_cookies))
    else:
        print("[!] Secrets Belum Diisi!")
