import os
import random
import time
import re
import json
import asyncio
import requests
import yt_dlp
import librosa
import numpy as np
from bs4 import BeautifulSoup
from datetime import datetime
from moviepy.editor import *
from PIL import Image
import soundfile as sf
from pyppeteer import launch

# ================= KONFIGURASI UTAMA =================
FOLDER_GAMBAR = "./gambar_hewan"      # Folder berisi gambar hewan
FOLDER_MUSIK = "./musik_trending"     # Folder untuk nyimpen audio trending
FOLDER_VIDEO = "./video_hasil"        # Folder hasil video
FOLDER_LOGS = "./logs"                # Folder logs

# Judul pencarian dan keyword pencarian dangdut viral
KEYWORD_SEARCH = "dangdut koplo viral reels"
TARGET_UPLOAD_PER_HARI = 10
LOG_FILE = f"{FOLDER_LOGS}/bot_log.txt"

# Untuk upload: file browser session biar ga login ulang
SESSION_FILE = "fb_session.json"

# Buat folder jika belum ada
for folder in [FOLDER_GAMBAR, FOLDER_MUSIK, FOLDER_VIDEO, FOLDER_LOGS]:
    os.makedirs(folder, exist_ok=True)

# ================= FUNGSI LOG =================
def tulis_log(pesan):
    waktu = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"[{waktu}] {pesan}\n")
    print(f"[{waktu}] {pesan}")

# ================= 1. DAPATKAN URL REELS TRENDING DARI FACEBOOK =================
def scrape_trending_reels(keyword=KEYWORD_SEARCH, limit=5):
    """Mencari dan mendapatkan URL reels dangdut trending tanpa API."""
    
    # Encode keyword untuk URL
    encoded_keyword = keyword.replace(" ", "+").lower()
    
    # List URL Facebook yang mungkin menampilkan reels trending
    search_urls = [
        f"https://www.facebook.com/search/top?q={encoded_keyword}",
        f"https://www.facebook.com/reels/search/{encoded_keyword}",
        "https://www.facebook.com/reels_tab",
    ]
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    reels_urls = []
    
    for url in search_urls:
        try:
            tulis_log(f"Mencari reels di: {url}")
            response = requests.get(url, headers=headers, timeout=30)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Cari link yang mengandung /reel/ atau /watch
            for a in soup.find_all('a', href=True):
                href = a['href']
                if '/reel/' in href or '/watch/?v=' in href:
                    if 'facebook.com' not in href:
                        full_url = 'https://www.facebook.com' + href.split('?')[0]
                    else:
                        full_url = href.split('?')[0]
                    
                    if full_url not in reels_urls and 'facebook.com' in full_url:
                        reels_urls.append(full_url)
                    
                    if len(reels_urls) >= limit:
                        break
            
            if len(reels_urls) >= limit:
                break
                
        except Exception as e:
            tulis_log(f"Error scraping: {e}")
            continue
        
        time.sleep(2)
    
    # Fallback: jika tidak dapat URL dari scraping, beri URL populer dangdut
    if not reels_urls:
        tulis_log("⚠️ Tidak dapat URL fresh, pakai URL populer dangdut...")
        # URL ini adalah contoh reels dangdut publik yang trending
        reels_urls = [
            "https://www.facebook.com/watch?v=1059815859753951",
            "https://www.facebook.com/reel/1523836417786597",
        ]
    
    tulis_log(f"Ditemukan {len(reels_urls)} URL reels: {reels_urls}")
    return reels_urls

# ================= 2. DOWNLOAD AUDIO DARI URL REELS =================
def download_audio_from_reels(reel_url):
    """Download audio dari URL reels menggunakan yt-dlp."""
    audio_path = None
    
    try:
        tulis_log(f"Download audio dari: {reel_url}")
        
        # Konfigurasi yt-dlp untuk ekstrak audio terbaik
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': f'{FOLDER_MUSIK}/audio_%(title).50s_%(id)s.%(ext)s',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'quiet': True,
            'no_warnings': True,
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(reel_url, download=True)
            audio_path = ydl.prepare_filename(info)
            # Ubah ekstensi ke .mp3 jika belum
            audio_path = os.path.splitext(audio_path)[0] + '.mp3'
            tulis_log(f"✅ Audio tersimpan: {audio_path}")
            
            return audio_path
            
    except Exception as e:
        tulis_log(f"❌ Gagal download audio: {e}")
        return None

# ================= 3. ANALISIS MUSIK (GET BEAT TIMES) =================
def get_beat_times(audio_path):
    """Melakukan beat tracking pada audio menggunakan librosa."""
    try:
        tulis_log("Menganalisis beat musik...")
        
        # Load audio
        y, sr = librosa.load(audio_path)
        
        # Dapatkan beat frames dan tempo
        tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr)
        
        # Konversi frames ke waktu (detik)
        beat_times = librosa.frames_to_time(beat_frames, sr=sr)
        
        # Hitung durasi total audio
        duration = librosa.get_duration(y=y, sr=sr)
        
        tulis_log(f"✅ Tempo: {tempo:.2f} BPM, Jumlah beat: {len(beat_times)}, Durasi: {duration:.2f} Detik")
        
        return {
            'beat_times': beat_times.tolist(),
            'tempo': tempo,
            'duration': duration,
            'sample_rate': sr
        }
        
    except Exception as e:
        tulis_log(f"❌ Gagal analisis beat: {e}")
        return None

# ================= 4. GENERATE HEWAN JOGET VIDEO (DENGAN GERAKAN SINKRON) =================
def generate_sync_video(gambar_path, beat_info, output_video_path):
    """Membuat video hewan joget dengan gerakan sesuai setiap beat."""
    try:
        tulis_log(f"🎬 Membuat video sinkron dari {gambar_path}...")
        
        # Load gambar
        img = Image.open(gambar_path).convert("RGB")
        img = img.resize((1080, 1920))
        img_array = np.array(img)
        
        # Dapatkan beat times
        beat_times = beat_info['beat_times']
        duration = beat_info['duration']
        tempo = beat_info['tempo']
        
        # Hitung interval antar beat
        if len(beat_times) > 1:
            avg_interval = np.mean(np.diff(beat_times))
        else:
            avg_interval = 60 / tempo if tempo > 0 else 0.5
        
        # Buat sequence klip (setiap klip = interval antar beat)
        clips = []
        start_time = 0
        
        for i in range(len(beat_times)):
            end_time = beat_times[i] if i < len(beat_times) else duration
            
            duration_klip = min(end_time - start_time, avg_interval * 2)
            if duration_klip <= 0:
                duration_klip = avg_interval
            
            # Buat gerakan berbeda untuk setiap klip (sesuai beat)
            # 4 jenis gerakan: zoom in/out, rotate, pan, shake
            anim_type = i % 5
            
            if anim_type == 0:
                # Zoom In
                clip = ImageClip(img_array, duration=duration_klip).resize(lambda t: 1 + t*0.5)
            elif anim_type == 1:
                # Zoom Out
                clip = ImageClip(img_array, duration=duration_klip).resize(lambda t: 1.5 - t*0.5)
            elif anim_type == 2:
                # Rotate sedikit
                clip = ImageClip(img_array, duration=duration_klip).rotate(lambda t: np.sin(t*20)*3)
            elif anim_type == 3:
                # Shake
                clip = ImageClip(img_array, duration=duration_klip).fx(vfx.resize, lambda t: 1 + np.sin(t*30)*0.05)
            else:
                # Pan horizontal
                clip = ImageClip(img_array, duration=duration_klip).resize(lambda t: 1 + t*0.3).set_position(lambda t: (np.sin(t)*50, 'center'))
            
            clips.append(clip)
            start_time = end_time
            
            if start_time >= duration:
                break
        
        # Gabungkan semua klip
        if clips:
            final_clip = concatenate_videoclips(clips, method="compose")
            
            # Loop jika durasi video kurang dari durasi musik
            if final_clip.duration < duration:
                final_clip = final_clip.loop(duration=duration)
            elif final_clip.duration > duration:
                final_clip = final_clip.subclip(0, duration)
            
            # Render video tanpa audio
            final_clip.write_videofile(
                output_video_path,
                fps=24,
                codec='libx264',
                audio=False,
                verbose=False,
                logger=None
            )
            
            tulis_log(f"✅ Video selesai: {output_video_path}")
            return output_video_path
        else:
            tulis_log("❌ Tidak ada klip yang dibuat")
            return None
            
    except Exception as e:
        tulis_log(f"❌ Gagal generate video: {e}")
        return None

# ================= 5. GABUNG VIDEO + AUDIO (FINAL) =================
def merge_video_audio(video_path, audio_path, output_final_path):
    """Menggabungkan video yang sudah dibuat dengan audio trending."""
    try:
        tulis_log("Menggabungkan video dengan audio...")
        
        video_clip = VideoFileClip(video_path)
        audio_clip = AudioFileClip(audio_path)
        
        # Sesuaikan durasi
        if video_clip.duration > audio_clip.duration:
            video_clip = video_clip.subclip(0, audio_clip.duration)
        elif video_clip.duration < audio_clip.duration:
            video_clip = video_clip.loop(duration=audio_clip.duration)
        
        final_clip = video_clip.set_audio(audio_clip)
        
        final_clip.write_videofile(
            output_final_path,
            fps=24,
            codec='libx264',
            audio_codec='aac',
            verbose=False,
            logger=None
        )
        
        # Tutup clip untuk hemat memori
        video_clip.close()
        audio_clip.close()
        final_clip.close()
        
        tulis_log(f"✅ Video final siap: {output_final_path}")
        return output_final_path
        
    except Exception as e:
        tulis_log(f"❌ Gagal merge: {e}")
        return None

# ================= 6. UPLOAD KE FACEBOOK (Tanpa Token - Pyppeteer) =================
async def upload_to_facebook(video_path, caption="Hewan Joget Dangdut Viral! 🔥 #hewanjoget #dangdutviral #fyp"):
    """Upload video ke Facebook Reels menggunakan pyppeteer (login manual sekali)."""
    
    tulis_log("🚀 Memulai proses upload...")
    
    # Cek apakah session sudah tersimpan
    if os.path.exists(SESSION_FILE):
        tulis_log("📁 Session file ditemukan, mencoba muat ulang...")
        browser = await launch(headless=False, args=['--no-sandbox'])
        page = await browser.newPage()
        
        # Load cookies jika ada
        with open(SESSION_FILE, 'r') as f:
            cookies = json.load(f)
            await page.setCookie(*cookies)
    else:
        browser = await launch(headless=False, args=['--no-sandbox'])
        page = await browser.newPage()
    
    try:
        # Buka Facebook dan login jika perlu
        tulis_log("📄 Membuka Facebook...")
        await page.goto('https://www.facebook.com/reels/your_reels', {'waitUntil': 'networkidle2'})
        
        # Login manual jika session belum ada
        if not os.path.exists(SESSION_FILE):
            tulis_log("⚠️ SESSION BELUM ADA! Silakan login MANUAL di browser yang terbuka.")
            input("Setelah login sukses di browser, tekan ENTER di sini untuk melanjutkan upload...")
            
            # Simpan session/cookies setelah login manual
            cookies = await page.cookies()
            with open(SESSION_FILE, 'w') as f:
                json.dump(cookies, f)
            tulis_log("✅ Session tersimpan! Upload berikutnya tidak perlu login lagi.")
        
        # Cari tombol "Create a reel" atau "Create"
        tulis_log("🔍 Mencari tombol upload...")
        
        # Percobaan beberapa selector umum untuk tombol create/post
        selectors = [
            'div[aria-label="Create a reel"]',
            'div[aria-label="Create"]',
            'div[aria-label="Buat Reel"]',
            'div[aria-label="Buat"]',
            'div[data-testid="reels_create_button"]',
            'div[data-testid="create_reel_button"]',
            'div[role="button"][aria-label*="Create"]',
            'div[role="button"][aria-label*="Buat"]',
            'div[aria-label="Tambah Reel"]',
        ]
        
        create_button = None
        for selector in selectors:
            try:
                create_button = await page.querySelector(selector)
                if create_button:
                    tulis_log(f"✅ Tombol create ditemukan dengan selector: {selector}")
                    break
            except:
                continue
        
        if create_button:
            await create_button.click()
            await asyncio.sleep(3)
        else:
            tulis_log("⚠️ Tombol create tidak ditemukan, mencoba alternatif...")
            # Fallback: buka URL create reel langsung
            await page.goto('https://www.facebook.com/reels/create/', {'waitUntil': 'networkidle2'})
        
        # Upload video
        tulis_log("📤 Uploading video...")
        
        # Cari input file
        file_input_selectors = [
            'input[type="file"]',
            'input[accept*="video"]',
            'div[role="button"] input[type="file"]',
            'div[aria-label*="upload"] input[type="file"]',
        ]
        
        file_input = None
        for selector in file_input_selectors:
            try:
                file_input = await page.querySelector(selector)
                if file_input:
                    tulis_log(f"✅ Input file ditemukan dengan selector: {selector}")
                    break
            except:
                continue
        
        if file_input:
            await file_input.uploadFile(video_path)
            tulis_log("✅ Video telah dipilih, menunggu proses upload selesai...")
        else:
            tulis_log("❌ Input file tidak ditemukan!")
            return False
        
        # Tunggu upload selesai (proses upload bisa lama)
        await asyncio.sleep(15)
        
        # Cari field caption
        caption_selectors = [
            'textarea[aria-label*="caption"]',
            'textarea[aria-label*="description"]',
            'div[role="textbox"][contenteditable="true"]',
            'div[aria-label*="Caption"]',
        ]
        
        caption_field = None
        for selector in caption_selectors:
            try:
                caption_field = await page.querySelector(selector)
                if caption_field:
                    tulis_log(f"✅ Caption field ditemukan dengan selector: {selector}")
                    break
            except:
                continue
        
        if caption_field:
            await caption_field.type(caption)
            tulis_log("✅ Caption ditambahkan")
        
        # Cari tombol share/publish/share now
        share_selectors = [
            'div[aria-label="Share now"]',
            'div[aria-label="Share"]',
            'div[aria-label="Bagikan"]',
            'div[aria-label="Publish"]',
            'div[aria-label="Terbitkan"]',
            'div[aria-label="Post"]',
            'div[role="button"][aria-label*="Share"]',
        ]
        
        share_button = None
        for selector in share_selectors:
            try:
                share_button = await page.querySelector(selector)
                if share_button:
                    tulis_log(f"✅ Share button ditemukan dengan selector: {selector}")
                    break
            except:
                continue
        
        if share_button:
            await share_button.click()
            tulis_log("✅ Tombol share diklik, menunggu konfirmasi...")
            await asyncio.sleep(5)
            tulis_log("🏁 Upload selesai!")
        else:
            tulis_log("⚠️ Tombol share/publish tidak ditemukan, video mungkin perlu diproses manual.")
            input("Silakan klik Share/Publish secara MANUAL di browser, lalu tekan ENTER...")
        
        await browser.close()
        return True
        
    except Exception as e:
        tulis_log(f"❌ Proses upload gagal: {e}")
        await browser.close()
        return False

# ================= MAIN LOOP (PROSES 1 VIDEO LENGKAP) =================
async def proses_satu_video():
    """Proses 1 video lengkap: dapat musik → bikin video → upload."""
    
    tulis_log("\n" + "="*50)
    tulis_log("🎯 MEMULAI PROSES VIDEO BARU")
    
    # Step 1: Dapatkan URL reels trending dangdut
    reel_urls = scrape_trending_reels(KEYWORD_SEARCH, limit=3)
    if not reel_urls:
        tulis_log("❌ Gagal dapat URL reels")
        return False
    
    # Step 2: Pilih satu URL secara acak
    selected_url = random.choice(reel_urls)
    tulis_log(f"🎵 URL reels terpilih: {selected_url}")
    
    # Step 3: Download audio dari URL tersebut
    audio_path = download_audio_from_reels(selected_url)
    if not audio_path or not os.path.exists(audio_path):
        tulis_log("❌ Gagal download audio")
        return False
    
    # Step 4: Analisis beat dari audio
    beat_info = get_beat_times(audio_path)
    if not beat_info:
        tulis_log("❌ Gagal analisis audio")
        return False
    
    # Step 5: Pilih gambar hewan secara acak
    gambar_list = [f for f in os.listdir(FOLDER_GAMBAR) 
                   if f.endswith(('.jpg', '.jpeg', '.png'))]
    
    if not gambar_list:
        tulis_log("❌ Tidak ada gambar hewan di folder!")
        return False
    
    selected_gambar = random.choice(gambar_list)
    gambar_path = os.path.join(FOLDER_GAMBAR, selected_gambar)
    tulis_log(f"🐱 Gambar terpilih: {selected_gambar}")
    
    # Step 6: Generate video sinkron dengan beat
    temp_video_path = os.path.join(FOLDER_VIDEO, f"temp_video_{int(time.time())}.mp4")
    video_path = generate_sync_video(gambar_path, beat_info, temp_video_path)
    
    if not video_path:
        tulis_log("❌ Gagal generate video")
        return False
    
    # Step 7: Gabungkan video dengan audio
    final_video_path = os.path.join(FOLDER_VIDEO, f"final_{int(time.time())}.mp4")
    final_video = merge_video_audio(video_path, audio_path, final_video_path)
    
    if not final_video:
        tulis_log("❌ Gagal merge video-audio")
        return False
    
    # Step 8: Upload ke Facebook
    caption = f"Hewan joget dangdut viral! 🐱🕺 #hewanjoget #dangdutviral #fyp #reels"
    success = await upload_to_facebook(final_video, caption)
    
    if success:
        tulis_log("✅ SUKSES! Video telah terupload.")
        return True
    else:
        tulis_log("❌ GAGAL upload.")
        return False

# ================= JOB SCHEDULER (10 VIDEO/HARI) =================
async def run_jadwal_24jam():
    """Menjalankan bot dengan jadwal 10 video per hari."""
    
    # Hitung jeda antar video (24 jam / 10 = 2.4 jam = 8640 detik)
    JEDA_DETIK = int(24 * 3600 / TARGET_UPLOAD_PER_HARI)
    
    tulis_log("="*60)
    tulis_log(f"🤖 BOT DANGDUT VIRAL AKTIF")
    tulis_log(f"🎯 Target: {TARGET_UPLOAD_PER_HARI} video per hari")
    tulis_log(f"⏱️  Jeda antar video: {JEDA_DETIK} detik ({JEDA_DETIK/3600:.1f} jam)")
    tulis_log("="*60)
    
    while True:
        try:
            # Proses 1 video
            success = await proses_satu_video()
            
            if success:
                tulis_log(f"⏳ Selesai 1 video. Menunggu {JEDA_DETIK} detik sebelum video berikutnya...")
            else:
                tulis_log(f"⚠️ Video gagal upload. Menunggu {JEDA_DETIK} detik lalu coba lagi...")
            
            # Tunggu hingga waktu upload berikutnya
            await asyncio.sleep(JEDA_DETIK)
            
        except Exception as e:
            tulis_log(f"🔥 ERROR di main loop: {e}")
            await asyncio.sleep(300)  # Jika error, tunggu 5 menit lalu coba lagi

# ================= MAIN =================
if __name__ == "__main__":
    asyncio.run(run_jadwal_24jam())
