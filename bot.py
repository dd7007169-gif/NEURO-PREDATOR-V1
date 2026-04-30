import os, time, random, subprocess, requests, signal, json
from datetime import datetime
from contextlib import contextmanager

# ================= KONFIGURASI UTAMA =================
FB_TOKEN = os.environ["FB_TOKEN"]
PAGE_ID = os.environ["FB_PAGE_ID"]

JUMLAH_VIDEO_PER_HARI = 5
MAX_DURATION = 15                    # Detik per video
TIMEOUT_GENERATE = 900               # 15 menit timeout bikin video
TIMEOUT_UPLOAD = 300                 # 5 menit timeout upload
MAX_RETRY = 3                        # Maksimal 3x coba kalau gagal
RETRY_DELAY = 60                     # Jeda 60 detik antar percobaan

FOLDER_HASIL_AI = "./video_ai_mentah"      # Folder video hasil AI
FOLDER_SIAP_UPLOAD = "./video_siap_upload" # Folder video siap tayang
LOG_FILE = "bot_log.txt"
# =====================================================

# ================= FUNGSI ANTI-MACET =================

class TimeoutError(Exception):
    """Error khusus untuk timeout."""
    pass

@contextmanager
def time_limit(seconds):
    """Membatasi waktu eksekusi. Kalau lebih, lempar TimeoutError."""
    def signal_handler(signum, frame):
        raise TimeoutError("⏰ Proses terlalu lama, dilewati.")
    signal.signal(signal.SIGALRM, signal_handler)
    signal.alarm(seconds)
    try:
        yield
    finally:
        signal.alarm(0)

def tulis_log(pesan):
    """Mencatat semua kejadian penting ke file log."""
    sekarang = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a") as f:
        f.write(f"[{sekarang}] {pesan}\n")
    print(pesan)

def retry_with_timeout(func, timeout, max_retry, *args, **kwargs):
    """Menjalankan fungsi dengan timeout & retry otomatis."""
    for percobaan in range(1, max_retry + 1):
        try:
            with time_limit(timeout):
                hasil = func(*args, **kwargs)
            return hasil
        except TimeoutError:
            tulis_log(f"⚠️ Percobaan ke-{percobaan}: Timeout ({timeout} detik).")
        except Exception as e:
            tulis_log(f"⚠️ Percobaan ke-{percobaan}: Error - {e}")
        
        if percobaan < max_retry:
            tulis_log(f"🔄 Coba lagi dalam {RETRY_DELAY} detik...")
            time.sleep(RETRY_DELAY)
    
    tulis_log("❌ Semua percobaan gagal. Dilewati.")
    return None

# ================= FUNGSI UTAMA BOT =================

def buat_video_ai(video_ke):
    """Membuat 1 video hewan joget dengan AI gratis (template)."""
    # ⚠️ GANTI BAGIAN INI dengan API AI motion transfer gratis pilihanmu.
    # Untuk sekarang, kita buat template dulu. Kamu tinggal sisipkan API-nya.
    
    output_path = os.path.join(FOLDER_HASIL_AI, f"temp_{video_ke}_{int(time.time())}.mp4")
    
    # CONTOH: Panggil API AI gratis di sini.
    # Misal pakai Replicate dengan model gratis:
    # import replicate
    # client = replicate.Client(api_token=os.environ["REPLICATE_TOKEN"])
    # output = client.run("model_gratis_anda", input={...})
    
    tulis_log(f"🎬 Membuat video AI ke-{video_ke}...")
    time.sleep(2)  # Simulasi proses (hapus nanti setelah API asli terpasang)
    
    # Simulasi: buat file kosong sebagai placeholder
    with open(output_path, "wb") as f:
        f.write(b"placeholder")
    
    return output_path

def ambil_musik_dari_facebook():
    """Mengambil 1 musik dangdut remix dari Meta Sound Collection."""
    # Gunakan Facebook Audio Recommendations API
    url = f"https://graph.facebook.com/v19.0/{PAGE_ID}/audio_recommendations"
    params = {
        'access_token': FB_TOKEN,
        'type': 'FACEBOOK_POPULAR_MUSIC',
        'limit': 10
    }
    
    try:
        response = requests.get(url, params=params, timeout=30)
        data = response.json()
        
        if 'data' in data and len(data['data']) > 0:
            # Pilih acak dari 10 lagu teratas
            lagu = random.choice(data['data'])
            tulis_log(f"🎵 Musik terpilih: {lagu.get('title', 'Tidak diketahui')}")
            return lagu.get('id')  # ID musik untuk ditanam saat upload
        else:
            tulis_log("⚠️ Tidak ada musik ditemukan, upload tanpa musik.")
            return None
    except Exception as e:
        tulis_log(f"⚠️ Gagal ambil musik: {e}")
        return None

def gabung_video_musik(video_path, musik_id, output_path):
    """Menggabungkan video AI dengan musik Facebook via FFmpeg + tagging."""
    if musik_id:
        tulis_log("🎵 Menanam musik ke video...")
        # Gabungkan dengan FFmpeg (musik dari file MP3 lokal kalau ada)
        # Untuk sekarang, musik akan ditanam sebagai metadata saat upload
    # Pindahkan file ke folder siap upload
    final_path = os.path.join(FOLDER_SIAP_UPLOAD, os.path.basename(video_path))
    os.rename(video_path, final_path)
    return final_path

def upload_facebook_reels(video_path, musik_id, caption):
    """Upload video ke Facebook Reels dengan tagging musik."""
    tulis_log(f"📤 Upload: {os.path.basename(video_path)}")
    
    url = f"https://graph-video.facebook.com/v19.0/{PAGE_ID}/videos"
    payload = {
        'access_token': FB_TOKEN,
        'description': caption,
        'title': 'Hewan Joget Dangdut Viral',
    }
    
    # Jika ada musik ID, tanamkan sebagai tag
    if musik_id:
        payload['audio_id'] = musik_id
    
    with open(video_path, 'rb') as f:
        response = requests.post(url, data=payload, files={'source': f}, timeout=TIMEOUT_UPLOAD)
    
    hasil = response.json()
    
    if 'id' in hasil:
        tulis_log(f"✅ Sukses upload! ID Video: {hasil['id']}")
        return hasil['id']
    else:
        tulis_log(f"❌ Gagal upload: {hasil}")
        return None

def proses_satu_video(video_ke):
    """Memproses 1 video lengkap: buat → gabung musik → upload."""
    tulis_log(f"\n{'='*50}")
    tulis_log(f"🎯 MEMPROSES VIDEO KE-{video_ke}")
    
    # Langkah 1: Bikin video AI (dengan timeout & retry)
    video_mentah = retry_with_timeout(
        buat_video_ai, TIMEOUT_GENERATE, MAX_RETRY, video_ke
    )
    if not video_mentah:
        return False
    
    # Langkah 2: Ambil musik dari Facebook
    musik_id = ambil_musik_dari_facebook()
    
    # Langkah 3: Gabung video + musik
    video_siap = gabung_video_musik(video_mentah, musik_id, f"ready_{video_ke}.mp4")
    
    # Langkah 4: Upload ke Facebook
    caption = f"Hewan joget dangdut viral! 🐱🕺 #dangdutremix #hewanjoget #viral"
    hasil_upload = retry_with_timeout(
        upload_facebook_reels, TIMEOUT_UPLOAD, MAX_RETRY,
        video_siap, musik_id, caption
    )
    
    if hasil_upload:
        tulis_log(f"🏁 Video ke-{video_ke} selesai & tayang!")
        return True
    return False

# ================= MAIN =================

def main():
    tulis_log("🤖 BOT HEWAN JOGET 24 JAM DIMULAI")
    
    # Buat folder kalau belum ada
    os.makedirs(FOLDER_HASIL_AI, exist_ok=True)
    os.makedirs(FOLDER_SIAP_UPLOAD, exist_ok=True)
    
    sukses = 0
    for i in range(1, JUMLAH_VIDEO_PER_HARI + 1):
        if proses_satu_video(i):
            sukses += 1
        
        # Jeda antar video biar tidak dibanjiri request
        if i < JUMLAH_VIDEO_PER_HARI:
            tulis_log("⏳ Jeda 5 menit sebelum video berikutnya...")
            time.sleep(300)
    
    tulis_log(f"\n✅ BOT SELESAI: {sukses}/{JUMLAH_VIDEO_PER_HARI} video berhasil tayang.")

if __name__ == "__main__":
    main()
