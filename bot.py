import os, time, random, json, requests
from playwright.sync_api import sync_playwright
from yt_dlp import YoutubeDL

# === ALAT 1: RADAR IP (WAJIB ADA) ===
def cek_radar_ip():
    print("\n" + "="*40)
    try:
        ip = requests.get('https://api.ipify.org?format=json').json()['ip']
        print(f"[!] IP PREDATOR: {ip} (Mode Ghost Aktif)")
    except: print("[!] Radar IP Off tapi tetap jalan.")
    print("="*40 + "\n")

# === ALAT 2: PENCARI VIDEO (VERSI RINGAN/ANTI-MACET) ===
def ambil_video_pinterest(topik):
    print(f"[*] Mencari video lucu: {topik}...")
    # Pakai API pencarian sederhana agar tidak dideteksi Pinterest
    search_url = f"https://www.pinterest.com/resource/BaseSearchResource/get/?data=%7B%22options%22%3A%7B%22query%22%3A%22{topik}%22%2C%22scope%22%3A%22pins%22%7D%7D"
    try:
        res = requests.get(search_url).json()
        pins = res['resource_response']['data']['results']
        # Ambil link video secara acak dari hasil
        pilihan = f"https://www.pinterest.com/pin/{random.choice(pins)['id']}/"
        print(f"[+] Konten ditemukan: {pilihan}")
        return pilihan
    except:
        # Jika cara canggih gagal, pakai link cadangan agar bot tidak mati
        return "https://id.pinterest.com/pin/1132725518776637151/"

# === ALAT 3: EKSEKUSI UTAMA (STABIL & MANUSIAWI) ===
def jalankan_misi_v5(topik, caption, cookies_fb):
    cek_radar_ip()
    file_mp4 = "reels_final.mp4"
    
    # 1. Download Tanpa Ribet
    link = ambil_video_pinterest(topik)
    with YoutubeDL({'format': 'best', 'outtmpl': file_mp4, 'quiet': True}) as ydl:
        ydl.download([link])

    # 2. Upload FB (Fokus ke Samaran Manusia)
    with sync_playwright() as p:
        # Pakai Browser standar tapi samaran diperkuat
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
            viewport={'width': 1280, 'height': 720}
        )
        context.add_cookies(cookies_fb)
        page = context.new_page()

        try:
            print("[*] Tahap: Memasuki FB Reels...")
            page.goto("https://m.facebook.com/reels/create/", wait_until="load", timeout=90000)
            
            # Cek apakah login masih valid
            if "login" in page.url:
                print("[!] ERROR: Cookie Bapak sudah basi/mati. Ganti Cookie baru!")
                return

            print("[*] Tahap: Upload file...")
            page.set_input_files("input[type='file']", file_mp4)
            
            # Jeda agar video tidak gagal proses
            time.sleep(25) 

            print("[*] Tahap: Klik Selanjutnya...")
            page.get_by_text("Selanjutnya").click()
            time.sleep(5)

            # --- KEYBOARD MANUSIA (ANTI-DETEKSI) ---
            print("[*] Tahap: Mengetik Caption (Sangat Pelan)...")
            page.wait_for_selector("textarea")
            for huruf in caption:
                page.keyboard.type(huruf, delay=random.randint(150, 400))
            
            print("[***] FINAL: KLIK BAGIKAN SEKARANG!")
            page.get_by_text("Bagikan Sekarang").click()
            
            time.sleep(15)
            print("[SUCCESS] MISI BERHASIL, PAK JOHN!")

        except Exception as e:
            print(f"[!] Gagal karena: {e}")
            if not os.path.exists("error_logs"): os.makedirs("error_logs")
            page.screenshot(path="error_logs/v5_fail.png")
        finally:
            browser.close()
            if os.path.exists(file_mp4): os.remove(file_mp4)

if __name__ == "__main__":
    topik = "funny baby animals"
    cap = "Hiburan sejenak, jangan stres! 😂 #lucu #viral #reels"
    
    kunci = os.getenv('FB_COOKIES')
    if kunci:
        jalankan_misi_v5(topik, cap, json.loads(kunci))
    else: print("[!] Kunci Cookies belum dipasang!")
