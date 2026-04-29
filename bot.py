import os, requests, random, time, re, json, subprocess, shutil
from datetime import datetime
from playwright.sync_api import sync_playwright

def predator_log(msg):
    print(f"💀 [V29-BRUTAL] {datetime.now().strftime('%H:%M:%S')} - {msg}")

# === SISTEM PENGACAK KAMAR (MENCARI VIDEO SAMPAI JEBOL) ===
def acak_acak_kamar_cari_video():
    predator_log("🧨 Download macet! Memulai aksi BRUTAL: Mengacak-acak isi kamar...")
    ekstensi_video = ('.mp4', '.mkv', '.mov', '.avi', '.ts', '.tmp')
    
    # Scan seluruh area kerja (kamar)
    for root, dirs, files in os.walk("."):
        for file in files:
            if file.lower().endswith(ekstensi_video):
                jalur_temuan = os.path.join(root, file)
                ukuran = os.path.getsize(jalur_temuan)
                
                # Kalau ketemu file video (bukan file kosong)
                if ukuran > 50000: # Minimal 50KB biar bukan file sampah
                    predator_log(f"🎯 KETEMU DI POJOK KAMAR! Mengambil: {file} ({ukuran} bytes)")
                    shutil.copy(jalur_temuan, "final_vid.mp4")
                    return True
    
    predator_log("❌ Kamar sudah hancur berantakan tapi video tidak ada. Mencoba jalur samping...")
    return False

# === AMBIL VIDEO DENGAN SEGALA CARA ===
def serbu_pinterest_v29(url):
    try:
        # Percobaan pertama: Jalan Normal
        predator_log("🗡️ Menyerang gerbang depan Pinterest...")
        subprocess.run(['yt-dlp', '-o', 'final_vid.mp4', url], capture_output=True)
        
        if os.path.exists("final_vid.mp4") and os.path.getsize("final_vid.mp4") > 10000:
            return True
            
        # Percobaan kedua: Jalur Belakang
        predator_log("🗡️ Gerbang depan tebal, coba lewat jendela (User-Agent Scrambler)...")
        subprocess.run(['yt-dlp', '--user-agent', 'Mozilla/5.0', '-o', 'final_vid.mp4', url], capture_output=True)
        
        # JIKA TETAP GAGAL: ACAK-ACAK KAMAR!
        if not os.path.exists("final_vid.mp4"):
            return acak_acak_kamar_cari_video()
            
    except:
        return acak_acak_kamar_cari_video()
    return False

# === EKSEKUSI JEBOL DINDING FB ===
def tembak_fb_brutal(video_path, cookies):
    predator_log("🚀 Menyerang Dinding Facebook dengan muatan hasil rampasan...")
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(user_agent="Mozilla/5.0 (Linux; Android 14; SM-S928B)")
        try:
            context.add_cookies(cookies)
            page = context.new_page()
            page.goto("https://m.facebook.com/reels/create/", wait_until="networkidle")
            
            # Injeksi File secara Paksa
            page.set_input_files("input[type='file']", video_path)
            time.sleep(45) # Biarkan sistem FB kewalahan memproses
            
            page.keyboard.press("Enter")
            time.sleep(5)
            
            # Caption Brutal
            page.wait_for_selector("textarea")
            page.keyboard.type(f"Hancurkan Semua! 💥 #{random.randint(1000,9999)}", delay=50)
            
            page.get_by_text("Bagikan Sekarang").click(force=True)
            predator_log("✅ SEMUA JEBOL! Video ter-upload lewat jalur belakang.")
            time.sleep(15)
        except Exception as e:
            predator_log(f"❌ Dinding FB terlalu kuat, butuh peledak lebih besar: {e}")
        finally:
            browser.close()

def jalan_mesin():
    # 1. Serbu Pinterest atau acak-acak kamar sampai dapat
    url_pin = "URL_PINTEREST_BAPAK"
    if serbu_pinterest_v29(url_pin):
        # 2. Cuci Cokelat (Cookies)
        kunci_raw = re.sub(r'[^0-9a-fA-F]', '', os.getenv("KUNCI_PREDATOR", ""))
        teks_kunci = bytes.fromhex(kunci_raw).decode('utf-8', errors='ignore')
        match = re.search(r'\[.*\]', teks_kunci, re.DOTALL)
        
        if match:
            data = json.loads(match.group(0))
            cookies = [{"name": c["name"], "value": c["value"], "domain": ".facebook.com", "path": "/"} for c in data]
            tembak_fb_brutal("final_vid.mp4", cookies)
        else:
            predator_log("❌ Cokelatnya busuk, tidak bisa buat kunci!")

if __name__ == "__main__":
    jalan_mesin()
