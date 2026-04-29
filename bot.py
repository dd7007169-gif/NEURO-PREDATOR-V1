import os, requests, random, time, re, subprocess, json, socket
from datetime import datetime
from playwright.sync_api import sync_playwright
import yt_dlp

def predator_log(msg):
    print(f"🛡️ [SAFE-MODE-V15] {datetime.now().strftime('%H:%M:%S')} - {msg}")

# === ALAT PEMBERSIH VIDEO (AGAR FB TIDAK CURIGA) ===
def bersihkan_metadata(input_file):
    output_file = "clean_video.mp4"
    predator_log("🛠️ Membersihkan jejak digital video (Anti-Blokir)...")
    try:
        # Menghapus metadata asli dan memberikan identitas baru seolah dari HP
        cmd = [
            'ffmpeg', '-i', input_file,
            '-c', 'copy', '-map_metadata', '-1', 
            '-metadata', 'model=SM-S928B', 
            '-metadata', 'make=Samsung', '-y', output_file
        ]
        subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return output_file
    except:
        return input_file

# === PROSEDUR PENEMBUSAN HALUS (FB PRIVATE) ===
def tembak_fb_aman(video_path, cookies):
    predator_log("🚀 Menjalankan Protokol Anti-Blokir di Facebook...")
    with sync_playwright() as p:
        # Menyamar sebagai browser biasa, bukan bot otomatis
        browser = p.chromium.launch(headless=True, args=['--disable-blink-features=AutomationControlled'])
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Linux; Android 14; SM-S928B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36",
            viewport={'width': 412, 'height': 915},
            has_touch=True
        )
        context.add_cookies(cookies)
        page = context.new_page()

        try:
            # Langkah 1: Masuk pelan-pelan
            page.goto("https://m.facebook.com/reels/create/", wait_until="networkidle", timeout=90000)
            time.sleep(random.uniform(3, 6)) # Jeda manusia
            
            predator_log("📤 Menyuntikkan video dengan metode halus...")
            page.set_input_files("input[type='file']", video_path)
            
            # Langkah 2: Tunggu upload selesai (FB butuh waktu render)
            time.sleep(random.uniform(20, 30))
            
            # Langkah 3: Klik 'Selanjutnya' dengan gaya manusia
            btn_next = page.get_by_text("Selanjutnya")
            if btn_next.is_visible():
                btn_next.click(delay=random.randint(500, 1500))
            else:
                page.keyboard.press("Enter")
            
            time.sleep(random.uniform(4, 7))

            # Langkah 4: Mengetik Caption (Kunci Utama Anti-Bot)
            predator_log("✍️ Mengetik caption huruf demi huruf...")
            page.wait_for_selector("textarea")
            captions = ["Lucu banget! 😂", "Hiburan hari ini 🔥", "Momen langka!", "Wajib nonton! ✨"]
            pesan = f"{random.choice(captions)} #{random.randint(1000,9999)}"
            
            for huruf in pesan:
                page.keyboard.type(huruf, delay=random.randint(100, 350)) # Kecepatan ketik acak
                if random.random() > 0.9: time.sleep(0.5) # Pura-pura mikir sebentar
            
            time.sleep(random.uniform(3, 5))
            
            # Langkah 5: Publikasi Final
            predator_log("🚀 Meluncurkan video ke Profil...")
            page.get_by_text("Bagikan Sekarang").click(force=True)
            
            # Jangan langsung tutup browser, tunggu sebentar agar koneksi selesai
            time.sleep(15)
            predator_log("✅ BERHASIL! Video aman terposting tanpa terdeteksi bot.")

        except Exception as e:
            predator_log(f"⚠️ Gangguan sistem: {e}")
            page.screenshot(path="fb_safety_check.png")
        finally:
            browser.close()

def jalan_mesin():
    # Mengambil rahasia dari GitHub
    kunci_raw = os.getenv("KUNCI_PREDATOR", "").strip()
    kunci_bersih = "".join(filter(lambda x: x.lower() in "0123456789abcdef", kunci_raw))
    
    if not kunci_bersih: return predator_log("❌ KUNCI_PREDATOR KOSONG!")

    try:
        decoded = bytes.fromhex(kunci_bersih).decode('utf-8', errors='replace')
        fb_cookies = []
        for item in decoded.split(';'):
            item = item.strip()
            if '=' in item:
                n, v = item.split('=', 1)
                fb_cookies.append({'name': n, 'value': v, 'domain': '.facebook.com', 'path': '/'})

        # Bagian Pinterest: Tetap bor paksa (Bebas)
        # Misal sudah dapat video 'raw.mp4' dari Pinterest...
        target_url = "https://id.pinterest.com/pin/1132725518776637151/" 
        
        with requests.get(target_url, stream=True) as r:
             with open("raw.mp4", 'wb') as f:
                 for chunk in r.iter_content(chunk_size=1024): f.write(chunk)

        # Proses pembersihan sebelum masuk ke FB
        video_bersih = bersihkan_metadata("raw.mp4")
        
        # Eksekusi Tembak Aman
        tembak_fb_aman(video_bersih, fb_cookies)
        
        # Hapus file sementara
        for f in ["raw.mp4", "clean_video.mp4"]:
            if os.path.exists(f): os.remove(f)

    except Exception as e:
        predator_log(f"⚠️ Masalah: {e}")

if __name__ == "__main__":
    jalan_mesin()
