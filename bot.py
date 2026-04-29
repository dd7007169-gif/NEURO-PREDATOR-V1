import os, requests, random, time, re, subprocess, json, socket
from datetime import datetime
from playwright.sync_api import sync_playwright
import yt_dlp

def predator_log(msg):
    print(f"🛰️ [V16-JSON-PREDATOR] {datetime.now().strftime('%H:%M:%S')} - {msg}")

# === ALAT PENDUKUNG: PEMBERSIH & PENYARING COOKIE JSON ===
def olah_cookie_json(raw_hex):
    try:
        # Dekode Hex ke teks asli
        decoded = bytes.fromhex(raw_hex).decode('utf-8', errors='replace')
        
        # OTAK: Mendeteksi apakah ini JSON atau teks biasa
        if decoded.strip().startswith('[') or decoded.strip().startswith('{'):
            predator_log("🧠 Otak mendeteksi format JSON. Melakukan konversi...")
            data = json.loads(decoded)
            # Jika JSON dalam bentuk list (hasil ekspor umum)
            if isinstance(data, list):
                for ck in data:
                    # Pastikan domainnya benar untuk Facebook
                    ck['domain'] = '.facebook.com'
                    ck.pop('sameSite', None) # Buang field yang sering bikin error
                    ck.pop('storeId', None)
                return data
        
        # Jika teks biasa, gunakan cara lama (cadangan)
        predator_log("🧠 Otak mendeteksi format String. Memproses manual...")
        cookies = []
        for item in decoded.split(';'):
            if '=' in item:
                n, v = item.strip().split('=', 1)
                cookies.append({'name': n, 'value': v, 'domain': '.facebook.com', 'path': '/'})
        return cookies
    except Exception as e:
        predator_log(f"⚠️ Gagal mengolah Cookie: {e}")
        return None

def tembak_fb_aman(video_path, cookies):
    predator_log("🚀 Memulai Penjebolan Dinding FB dengan Cookie JSON...")
    with sync_playwright() as p:
        # Alat Penyamaran: HP Samsung S24 Ultra
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Linux; Android 14; SM-S928B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36"
        )
        # Suntikkan Cookie hasil olahan otak
        context.add_cookies(cookies)
        page = context.new_page()

        try:
            page.goto("https://m.facebook.com/reels/create/", wait_until="networkidle", timeout=90000)
            
            # --- Jeda Manusia agar tidak Terblokir ---
            time.sleep(random.uniform(5, 8))
            
            predator_log("📤 Menyuntikkan video...")
            page.set_input_files("input[type='file']", video_path)
            
            # Tunggu render video di "kaca"
            time.sleep(25)
            
            # Cari tombol selanjutnya dengan kecerdikan
            btn = page.get_by_text("Selanjutnya")
            if btn.is_visible():
                btn.click(delay=random.randint(500, 1500))
            else:
                page.keyboard.press("Enter")
            
            time.sleep(5)
            # Ketik Caption pelan-pelan (Anti-Bot)
            page.wait_for_selector("textarea")
            caption = f"Momen Berharga! 🔥 #{random.randint(1000,9999)}"
            for char in caption:
                page.keyboard.type(char, delay=random.randint(100, 300))
            
            predator_log("🚀 Publikasi Final...")
            page.get_by_text("Bagikan Sekarang").click(force=True)
            time.sleep(15)
            predator_log("✅ MISI SELESAI! Dinding jebol, akun aman.")
            
        except Exception as e:
            predator_log(f"⚠️ Masalah: {e}")
        finally:
            browser.close()

def jalan_mesin():
    # Ambil KUNCI_PREDATOR dari GitHub
    kunci_raw = os.getenv("KUNCI_PREDATOR", "").strip()
    kunci_bersih = "".join(filter(lambda x: x.lower() in "0123456789abcdef", kunci_raw))
    
    if not kunci_bersih:
        return predator_log("❌ KUNCI KOSONG!")

    # Panggil Otak Pengolah Cookie JSON
    cookies_final = olah_cookie_json(kunci_bersih)
    
    if cookies_final:
        # Proses Pinterest (Bebas/Brutal)
        # Misal sudah ada 'final_vid.mp4'
        tembak_fb_aman("final_vid.mp4", cookies_final)
    else:
        predator_log("❌ Cookie tidak valid!")

if __name__ == "__main__":
    jalan_mesin()
