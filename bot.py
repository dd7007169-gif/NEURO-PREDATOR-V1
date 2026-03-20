import os
import subprocess
import random
import requests
import time

# --- KONFIGURASI MUTASI (FFMPEG) ---
def mutate_video(input_file, output_file):
    hook_texts = [
        "Kejadian di akhir gak masuk akal! 😱",
        "Nungguin apa ya? 🤔",
        "Hanya ada di China lucu banget 😂",
        "Tonton sampai habis! 😱"
    ]
    selected_hook = random.choice(hook_texts)
    
    # Perintah FFmpeg: Mirror, Zoom, Color Shift, FPS Jitter, & Metadata iPhone
    cmd = [
        'ffmpeg', '-i', input_file,
        '-vf', (
            f"hflip,scale=1084:1926,"
            f"zoompan=z='min(zoom+0.001,1.05)':d=1:s=1084x1926,"
            f"eq=gamma=1.02:contrast=1.03,"
            f"drawtext=text='{selected_hook}':fontcolor=white:fontsize=50:x=(w-text_w)/2:y=150:box=1:boxcolor=black@0.5"
        ),
        '-af', "rubberband=tempo=1.01,lowshelf=f=100:g=-5",
        '-r', '29.97',
        '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '24',
        '-metadata', 'make=Apple', '-metadata', 'model=iPhone 17 Pro',
        '-y', output_file
    ]
    
    subprocess.run(cmd, check=True)
    print(f"✅ Mutasi Selesai: {output_file}")

# --- DOWNLOADER SEDERHANA (PINTEREST) ---
def download_video(url, filename):
    r = requests.get(url, stream=True)
    with open(filename, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)
    print(f"📥 Download Selesai: {filename}")

# --- MAIN LOGIC ---
if __name__ == "__main__":
    # Buat folder jika belum ada
    os.makedirs('raw', exist_ok=True)
    os.makedirs('ready_to_upload', exist_ok=True)

    # CONTOH URL VIDEO (Ganti dengan hasil scraping atau manual list)
    # Di GitHub Actions, Anda bisa kembangkan bagian ini untuk ambil dari API Pinterest
    video_urls = [
        "https://example.com/video1.mp4", # Masukkan link video Pinterest di sini
    ]

    for i, url in enumerate(video_urls):
        raw_file = f"raw/video_{i}.mp4"
        final_file = f"ready_to_upload/final_{i}.mp4"
        
        try:
            # Jika Anda belum punya scraper otomatis, taruh file video di folder 'raw' manual
            # download_video(url, raw_file) 
            
            # Cari file di folder raw untuk dimutasi
            for f in os.listdir('raw'):
                if f.endswith(".mp4"):
                    mutate_video(f"raw/{f}", f"ready_to_upload/mutated_{f}")
                    
        except Exception as e:
            print(f"❌ Error: {e}")
