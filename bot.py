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
    print(f"[{lokasi_error}] Bukti kesalahan disimpan di folder '{folder}'")

# === ALAT HUMAN CLICK ===
def human_click(page, selector, nama_tombol):
    try:
        element = page.wait_for_selector(selector, timeout=15000)
        box = element.bounding_box()
        x = box['x'] + box['width'] * random.uniform(0.2, 0.8)
        y = box['y'] + box['height'] * random.uniform(0.2, 0.8)
        page.mouse.move(x, y, steps=random.randint(10, 20))
        page.mouse.click(x, y)
    except Exception as e:
        print(f"[ERROR] Gagal klik tombol: {nama_tombol}")
        simpan_bukti_kesalahan(page, f"gagal_klik_{nama_tombol}")
        raise e

# === SISTEM UTAMA INTEGRASI ===
def eksekusi_predator_2026(pin_url, caption, cookies_fb):
    ua = UserAgent(platforms='mobile')
    
    # --- BAGIAN 1: DOWNLOAD PINTEREST (ALAT LENGKAP) ---
    print("[*] Tahap 1: Mendownload Video Pinterest...")
    ydl_opts = {
        'format': 'bestvideo+bestaudio/best',
        'outtmpl': 'predator_final.%(ext)s',
        'quiet': True,
        'user_agent': ua.random
    }
    try:
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([pin_url])
        video_path = "predator_final.mp4"
    except Exception as e:
        print(f"[CRITICAL ERROR] Gagal di Pinterest: {e}")
        return

    # --- BAGIAN 2: UPLOAD FB (GOD MODE + AUDIT) ---
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, args=["--disable-blink-features=AutomationControlled"])
        context = browser.new_context(
            user_agent=ua.random,
            viewport={'width': 393, 'height': 852},
            has_touch=True
        )
        context.add_cookies(cookies_fb)
        page = context.new_page()

        try:
            # Step 1: Terapi Beranda
            print("[*] Tahap 2: Navigasi ke Facebook...")
            page.goto("https://m.facebook.com/", wait_until="networkidle")
            
            # Step 2: Menuju Reels
            print("[*] Tahap 3: Memasuki Menu Reels...")
            page.goto("https://m.facebook.com/reels/create/", wait_until="networkidle")
            
            # Step 3: Input File
            print("[*] Tahap 4: Mengunggah File...")
            try:
                page.set_input_files("input[type='file']", video_path)
            except Exception as e:
                simpan_bukti_kesalahan(page, "gagal_input_file")
                raise e

            time.sleep(random.randint(8, 12))

            # Step 4: Klik Selanjutnya
            print("[*] Tahap 5: Menekan Selanjutnya...")
            human_click(page, "text=Selanjutnya", "tombol_next_1")

            # Step 5: Ketik Caption
            print("[*] Tahap 6: Menulis Caption...")
            try:
                textarea = page.wait_for_selector("textarea")
                for char in caption:
                    textarea.type(char)
                    time.sleep(random.uniform(0.05, 0.2))
            except Exception as e:
                simpan_bukti_kesalahan(page, "gagal_ketik_caption")
                raise e

            # Step 6: Final Post
            print("[***] Tahap 7: EKSEKUSI TERBITKAN!")
            human_click(page, "text=Bagikan Sekarang", "tombol_publish")

            # Tunggu konfirmasi
            page.wait_for_load_state("networkidle")
            print("[SUCCESS] MISI BERHASIL!")

        except Exception as e:
            print(f"\n[!!!] TERJADI KESALAHAN FATAL: {e}")
            # Letak kesalahan sudah otomatis tersimpan di folder error_logs
        
        finally:
            time.sleep(5)
            browser.close()

# Contoh Cara Menjalankan:
if __name__ == "__main__":
    url_pin = "LINK_PINTEREST_BAPAK"
    teks = "Nuyul jam tayang lancar jaya! #viral #reels"
    # Cookies diambil dari extension 'EditThisCookie'
    data_cookie = [
        {'name': 'c_user', 'value': 'ID_BAPAK', 'domain': '.facebook.com', 'path': '/'},
        {'name': 'xs', 'value': 'TOKEN_BAPAK', 'domain': '.facebook.com', 'path': '/'}
    ]
    
    eksekusi_predator_2026(url_pin, teks, data_cookie)
