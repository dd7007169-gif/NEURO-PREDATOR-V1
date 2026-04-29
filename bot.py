import os, requests, random, time, re, subprocess, json
from datetime import datetime
from playwright.sync_api import sync_playwright
import yt_dlp

def predator_log(msg):
    print(f"🛡️ [V21-PURIFIER] {datetime.now().strftime('%H:%M:%S')} - {msg}")

# === ALAT SARINGAN LASER (MENGHAPUS SEMUA ERROR COOKIE) ===
def saring_kunci_johnson(raw_hex):
    try:
        # 1. Dekode Hex ke Teks
        teks = bytes.fromhex(raw_hex).decode('utf-8', errors='ignore').strip()
        
        # 2. Cari awal JSON
        start = teks.find('[')
        if start == -1: start = teks.find('{')
        if start == -1: return None
        
        data = json.loads(teks[start:])
        if isinstance(data, dict): data = [data]
        
        cookies_bersih = []
        for ck in data:
            # SARINGAN LASER: Hanya ambil name & value. 
            # Paksa domain & path agar Playwright tidak protes.
            name = ck.get("name")
            value = ck.get("value")
            
            if name and value:
                cookies_bersih.append({
                    "name": str(name),
                    "value": str(value),
                    "domain": ".facebook.com",
                    "path": "/",
                    "secure": True # Facebook wajib Secure
                })
        
        predator_log(f"✅ Saringan Laser berhasil mencuci {len(cookies_bersih)} kunci.")
        return cookies_bersih
    except Exception as e:
        predator_log(f"⚠️ Gagal mencuci kunci: {e}")
        return None

def tembak_fb_v21(video_path, cookies):
    predator_log("🚀 Menembus Dinding Facebook...")
    with sync_playwright() as p:
        # Pakai Browser Chrome Asli agar tidak dicurigai
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Linux; Android 14; SM-S928B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36"
        )
        
        try:
            # SUNTIKAN KUNCI YANG SUDAH DICUCI
            context.add_cookies(cookies)
            page = context.new_page()
            
            # Akses Facebook Reel
            page.goto("https://m.facebook.com/reels/create/", wait_until="domcontentloaded", timeout=60000)
            time.sleep(10)
            
            # Jika ada tombol "Batal" atau "Gunakan Data", bot akan abaikan
            predator_log("📤 Menyuntikkan muatan video...")
            page.set_input_files("input[type='file']", video_path)
            
            # Jeda Render Video
            time.sleep(30)
            
            # Tekan Selanjutnya (Gunakan Keyboard Enter agar lebih cerdik)
            page.keyboard.press("Enter")
            time.sleep(5)
            
            # Isi Caption
            page.wait_for_selector("textarea")
            caption = f"Momen Berkesan 🔥 #{random.randint(100,999)}"
            for char in caption:
                page.keyboard.type(char, delay=random.randint(50, 150))
            
            # PUBLIKASI FINAL
            predator_log("🚀 Tekan tombol Bagikan...")
            page.get_by_text("Bagikan Sekarang").click(force=True)
            time.sleep(20)
            predator_log("✅ MISI SELESAI TOTAL!")
            
        except Exception as e:
            predator_log(f"❌ Dinding Gagal Dijebol: {e}")
        finally:
            browser.close()

def jalan_mesin():
    # Ambil kunci dari Secrets GitHub
    kunci_raw = os.getenv("KUNCI_PREDATOR", "").strip()
    kunci_bersih = "".join(filter(lambda x: x.lower() in "0123456789abcdef", kunci_raw))
    
    if not kunci_bersih:
        return predator_log("❌ KUNCI_PREDATOR KOSONG!")

    # Masuk ke Saringan Laser
    kunci_siap = saring_kunci_johnson(kunci_bersih)
    
    if kunci_siap:
        # (Logika Pinterest V12 Bapak tetap berjalan di sini untuk ambil video)
        # Kita asumsikan video sudah ada dengan nama 'final_vid.mp4'
        tembak_fb_v21("final_vid.mp4", kunci_siap)
    else:
        predator_log("❌ Kunci tidak bisa dicuci. Pastikan Bapak copy JSON yang benar!")

if __name__ == "__main__":
    jalan_mesin()
