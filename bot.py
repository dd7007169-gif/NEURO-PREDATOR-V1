import os
import time
import random
import json
import datetime
from playwright.sync_api import sync_playwright
from fake_useragent import UserAgent
from yt_dlp import YoutubeDL

# === FUNGSI AUDIT: MELIHAT LETAK KESALAHAN ===
def simpan_bukti_kesalahan(page, lokasi_error):
    waktu = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    folder = "error_logs"
    if not os.path.exists(folder):
        os.makedirs(folder)
    
    # 1. Ambil Foto Layar (Visual)
    page.screenshot(path=f"{folder}/error_{lokasi_error}_{waktu}.png")
    # 2. Ambil Kode HTML (Struktur)
    with open(f"{folder}/source_{lokasi_error}_{waktu}.html", "w", encoding="utf-8") as f:
        f.write(page.content())
    print(f"[!] BUKTI TERSEDIA: Cek folder '{folder}' untuk file error_{lokasi_error}.png")

# === ALAT HUMAN CLICK ===
def human_click(page, selector, nama_tombol):
    try:
        element = page.wait_for_selector(selector, timeout=20000)
        element.scroll_into_view_if_needed()
        box = element.bounding_box()
        # Titik klik acak agar tidak terdeteksi robot
        x = box['x'] + box['width'] * random.uniform(0.3, 0.7)
        y = box['y'] + box['height'] * random.uniform(0.3, 0.7)
        page.mouse.move(x, y, steps=random.randint(15, 25))
        page.mouse.click(x, y)
        time.sleep(random.uniform(2, 4))
    except Exception as e:
        print(f"[ERROR] Tombol '{nama_tombol}' tidak ditemukan atau terhalang.")
        simpan_bukti_kesalahan(page, f"gagal_klik_{nama_tombol}")
        raise e

# === SISTEM UTAMA INTEGRASI ===
def eksekusi_predator_2026(pin_url, caption, cookies_fb):
    ua = UserAgent(platforms='mobile')
    video_path = "predator_final.mp4"
    
    # --- BAGIAN 1: DOWNLOAD PINTEREST ---
    print("[*] TAHAP 1: Menembus Pinterest...")
    ydl_opts = {
        'format': 'best',
        'outtmpl': video_path,
        'quiet': True,
        'no_warnings': True,
        'user_agent': ua.random
    }
    try:
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([pin_url])
        if not os.path.exists(video_path):
            raise Exception("File video tidak terunduh.")
        print("[+] Download Berhasil!")
    except Exception as e:
        print(f"[CRITICAL] Pinterest Gagal: {e}")
        return

    # --- BAGIAN 2: UPLOAD FB GOD MODE ---
    with sync_playwright() as p:
        # Gunakan --disable-blink-features agar tidak terdeteksi bot
        browser = p.chromium.launch(headless=True, args=["--disable-blink-features=AutomationControlled"])
        context = browser.new_context(
            user_agent=ua.random,
            viewport={'width': 393, 'height': 852},
            has_touch=True
        )
        
        # Masukkan Cookies
        if cookies_fb:
            context.add_cookies(cookies_fb)
        
        page = context.new_page()

        try:
            print("[*] TAHAP 2: Penyamaran di Beranda FB...")
            page.goto("https://m.facebook.com/", wait_until="networkidle")
            time.sleep(5) # Simulasi orang baca feed
            
            print("[*] TAHAP 3: Masuk ke Menu Reels...")
            page.goto("https://m.facebook.com/reels/create/", wait_until="networkidle")
            
            print("[*] TAHAP 4: Uploading File...")
            # Sembunyikan deteksi file chooser
            page.set_input_files("input[type='file']", video_path)
            
            # Tunggu proses render video (PENTING!)
            print("[*] Menunggu video diproses sistem FB...")
            time.sleep(15)

            print("[*] TAHAP 5: Navigasi Tombol...")
            human_click(page, "text=Selanjutnya", "Next_1")
            
            print("[*] TAHAP 6: Mengetik Caption (Human Style)...")
            try:
                # Cari textarea untuk caption
                page.wait_for_selector("textarea")
                page.focus("textarea")
                for char in caption:
                    page.keyboard.type(char)
                    time.sleep(random.uniform(0.05, 0.15))
            except:
                print("[!] Gagal ketik caption, lanjut tanpa caption.")

            print("[***] TAHAP 7: FINAL PUBLISH!")
            human_click(page, "text=Bagikan Sekarang", "Publish_Button")
            
            # Verifikasi Akhir
            page.wait_for_load_state("networkidle")
            print("[SUCCESS] NEURO-PREDICTOR Berhasil Menyelesaikan Misi!")

        except Exception as e:
            print(f"\n[!!!] MISI GAGAL: {e}")
            simpan_bukti_kesalahan(page, "fatal_error")
        
        finally:
            browser.close()
            # Hapus video setelah upload agar hemat ruang
            if os.path.exists(video_path):
                os.remove(video_path)

# === KONFIGURASI OTOMATIS ===
if __name__ == "__main__":
    # GANTI LINK INI SESUAI KEINGINAN
    target_pin = "https://id.pinterest.com/pin/1132725518776637151/" 
    caption_reels = "Predator-V1 Mode Aktif! #viral #reels #trending"

    # Ambil Cookie dari GitHub Secrets atau Lokal
    raw_cookies = os.getenv('FB_COOKIES')
    
    try:
        if raw_cookies:
            processed_cookies = json.loads(raw_cookies)
            print("[+] Mengambil kunci dari Secrets.")
        else:
            # Cadangan jika di Termux (Isi manual di sini)
            processed_cookies = [
                {'name': 'c_user', 'value': 'ID_ANDA', 'domain': '.facebook.com', 'path': '/'},
                {'name': 'xs', 'value': 'TOKEN_ANDA', 'domain': '.facebook.com', 'path': '/'}
            ]
            print("[!] Menggunakan Cookie manual.")
    except Exception as e:
        print(f"[ERROR] Format Cookie salah: {e}")
        processed_cookies = []

    # JALANKAN!
    eksekusi_predator_2026(target_pin, caption_reels, processed_cookies)
