import os, requests, random, time, re, subprocess, json
from datetime import datetime
from playwright.sync_api import sync_playwright

def predator_log(msg):
    print(f"👻 [V23-GHOST] {datetime.now().strftime('%H:%M:%S')} - {msg}")

# === ALAT DETEKSI KUNCI JOHNSON (VERSI ANTI-GAGAL) ===
def bedah_kunci_v23(raw_hex):
    try:
        # Dekode Hex dengan pengaman ekstra
        teks = bytes.fromhex(raw_hex).decode('utf-8', errors='ignore').strip()
        
        # Cari pola JSON [ ... ] secara paksa di dalam teks
        match = re.search(r'\[.*\]', teks, re.DOTALL)
        if not match:
            # Kalau tidak ada kurung siku, coba kurung kurawal
            match = re.search(r'\{.*\}', teks, re.DOTALL)
        
        if match:
            json_data = json.loads(match.group(0))
            if isinstance(json_data, dict): json_data = [json_data]
            
            cookies_final = []
            for item in json_data:
                # AMBIL INTI SAJA: Nama dan Value
                # Buang expirationDate dan sameSite yang bikin ERROR di log sebelumnya
                if item.get("name") and item.get("value"):
                    cookies_final.append({
                        "name": str(item.get("name")),
                        "value": str(item.get("value")),
                        "domain": ".facebook.com",
                        "path": "/"
                    })
            
            if cookies_final:
                predator_log(f"🎯 Mata Elang menemukan {len(cookies_final)} data valid!")
                return cookies_final
        
        # Jika gagal deteksi JSON, coba deteksi format string biasa (Semi-Auto)
        predator_log("⚠️ Format JSON tidak utuh, mencoba teknik String-Scraping...")
        cookies_backup = []
        for pair in teks.split(';'):
            if '=' in pair:
                n, v = pair.strip().split('=', 1)
                cookies_backup.append({"name": n, "value": v, "domain": ".facebook.com", "path": "/"})
        return cookies_backup if cookies_backup else None

    except Exception as e:
        predator_log(f"❌ Otak Bot Blank: {e}")
        return None

def tembak_fb_v23(video_path, cookies):
    predator_log("🚀 Memulai Infiltrasi Facebook...")
    with sync_playwright() as p:
        # Gunakan Chrome Tanpa Jejak
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Linux; Android 14; SM-S928B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36"
        )
        try:
            context.add_cookies(cookies)
            page = context.new_page()
            
            # Langsung ke sasaran
            page.goto("https://m.facebook.com/reels/create/", wait_until="domcontentloaded", timeout=60000)
            time.sleep(7)
            
            predator_log("📤 Menyuntikkan video ke sistem...")
            page.set_input_files("input[type='file']", video_path)
            
            # Jeda 35 detik: Biar FB tidak curiga (Anti-Blokir)
            time.sleep(35)
            
            # Bypass tombol dengan Keyboard (Lebih Aman dari Deteksi Bot)
            page.keyboard.press("Enter")
            time.sleep(5)
            
            # Ketik Caption
            page.wait_for_selector("textarea")
            msg = f"Keren Abis! 😂 #{random.randint(100,999)}"
            for char in msg:
                page.keyboard.type(char, delay=random.randint(50, 150))
            
            # PUBLIKASI
            predator_log("🚀 Menekan tombol Publikasi...")
            page.get_by_text("Bagikan Sekarang").click(force=True)
            time.sleep(15)
            predator_log("✅ BERHASIL! Dinding Facebook dijebol.")
            
        except Exception as e:
            predator_log(f"❌ Gagal di lapangan: {e}")
        finally:
            browser.close()

def jalan_mesin():
    # Ambil kunci mentah dari Secrets
    kunci_raw = os.getenv("KUNCI_PREDATOR", "").strip()
    # Bersihkan karakter non-Hex agar tidak rusak saat di-decode
    kunci_hex = re.sub(r'[^0-9a-fA-F]', '', kunci_raw)
    
    if not kunci_hex:
        return predator_log("❌ KUNCI_PREDATOR KOSONG DI GITHUB!")

    kunci_siap = bedah_kunci_v23(kunci_hex)
    
    if kunci_siap:
        # Pastikan file video Bapak namanya 'final_vid.mp4'
        if os.path.exists("final_vid.mp4"):
            tembak_fb_v23("final_vid.mp4", kunci_siap)
        else:
            predator_log("❌ File 'final_vid.mp4' tidak ditemukan!")
    else:
        predator_log("❌ Gagal total! Kunci Bapak hancur atau salah salin.")

if __name__ == "__main__":
    jalan_mesin()
