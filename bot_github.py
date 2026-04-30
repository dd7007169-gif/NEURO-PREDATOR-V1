#!/usr/bin/env python3
# bot_github.py - FOR GITHUB ACTIONS (HEADLESS LOGIN WITH EMAIL/PASSWORD)

import os
import sys
import subprocess
import asyncio
import random
import tempfile
import json
import base64
import requests
from bs4 import BeautifulSoup
import yt_dlp
import librosa
import numpy as np
from PIL import Image
from io import BytesIO

# Force install moviepy versi 1.0.3
try:
    from moviepy.editor import *
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "moviepy==1.0.3"])
    from moviepy.editor import *

from pyppeteer import launch

# ================= KONFIGURASI =================
FB_EMAIL = os.environ.get("FB_EMAIL")
FB_PASSWORD = os.environ.get("FB_PASSWORD")
PAGE_ID = os.environ.get("FB_PAGE_ID")
KEYWORD_SEARCH = "dangdut koplo viral reels"
SESSION_FILE = "fb_session.json"

# Gambar hewan (base64 minimal)
IMAGES_BASE64 = {
    "kucing": "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg==",
    "anjing": "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg==",
    "bebek": "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg=="
}

def simpan_gambar():
    files = []
    for nama, b64 in IMAGES_BASE64.items():
        img_data = base64.b64decode(b64)
        img = Image.open(BytesIO(img_data))
        img = img.resize((1080, 1920))
        f = tempfile.NamedTemporaryFile(delete=False, suffix=".jpg")
        img.save(f.name)
        files.append(f.name)
    return files

def tulis_log(pesan):
    print(f"[{__import__('time').strftime('%Y-%m-%d %H:%M:%S')}] {pesan}")

def scrape_trending_reels():
    tulis_log("Mencari reels dangdut viral...")
    return ["https://www.facebook.com/reel/1523836417786597"]

def download_audio_from_reels(reel_url):
    tulis_log(f"Download audio dari {reel_url}")
    out_template = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3").name.replace('.mp3','')
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': out_template,
        'postprocessors': [{'key': 'FFmpegExtractAudio', 'preferredcodec': 'mp3'}],
        'quiet': True,
        'no_warnings': True,
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.extract_info(reel_url, download=True)
        return out_template + '.mp3'
    except Exception as e:
        tulis_log(f"Gagal download: {e}")
        return None

def get_beat_times(audio_path):
    try:
        y, sr = librosa.load(audio_path, duration=30)
        tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr)
        beat_times = librosa.frames_to_time(beat_frames, sr=sr).tolist()
        duration = librosa.get_duration(y=y, sr=sr)
        return {'beat_times': beat_times or [0,1,2], 'tempo': tempo, 'duration': duration}
    except:
        return {'beat_times': [0,1,2], 'tempo': 120, 'duration': 30}

def generate_sync_video(gambar_path, beat_info, output_video):
    img = Image.open(gambar_path).convert("RGB")
    img = img.resize((1080, 1920))
    img_array = np.array(img)
    duration = beat_info['duration']
    clip = ImageClip(img_array, duration=duration).resize(lambda t: 1 + 0.1*np.sin(t*5))
    clip.write_videofile(output_video, fps=24, codec='libx264', audio=False, verbose=False)
    return output_video

def merge_video_audio(video_path, audio_path, output_final):
    video = VideoFileClip(video_path)
    audio = AudioFileClip(audio_path)
    if video.duration > audio.duration:
        video = video.subclip(0, audio.duration)
    else:
        video = video.loop(duration=audio.duration)
    final = video.set_audio(audio)
    final.write_videofile(output_final, fps=24, codec='libx264', audio_codec='aac', verbose=False)
    return output_final

async def login_facebook(page):
    tulis_log("Login otomatis ke Facebook...")
    await page.goto('https://www.facebook.com/')
    await page.waitForSelector('input[name="email"]')
    await page.type('input[name="email"]', FB_EMAIL)
    await page.type('input[name="pass"]', FB_PASSWORD)
    await page.click('button[name="login"]')
    await asyncio.sleep(5)
    cookies = await page.cookies()
    if any(c['name'] == 'c_user' for c in cookies):
        tulis_log("Login berhasil")
        return True
    tulis_log("Login gagal")
    return False

async def upload_to_facebook(video_path):
    tulis_log("Memulai upload...")
    browser = await launch(headless=True, args=['--no-sandbox', '--disable-setuid-sandbox'])
    page = await browser.newPage()
    await page.setViewport({'width': 1280, 'height': 720})
    
    if os.path.exists(SESSION_FILE):
        with open(SESSION_FILE, 'r') as f:
            cookies = json.load(f)
            await page.setCookie(*cookies)
        tulis_log("Cookies dimuat")
    else:
        if not await login_facebook(page):
            await browser.close()
            return False
        cookies = await page.cookies()
        with open(SESSION_FILE, 'w') as f:
            json.dump(cookies, f)
    
    await page.goto('https://www.facebook.com/reels/create/')
    await asyncio.sleep(3)
    
    file_input = await page.querySelector('input[type="file"]')
    if not file_input:
        tulis_log("Tidak ada input file")
        await browser.close()
        return False
    
    await file_input.uploadFile(video_path)
    tulis_log("Video diupload")
    await asyncio.sleep(15)
    
    caption = "Hewan joget dangdut viral! 🔥 #hewanjoget #dangdutviral"
    try:
        await page.waitForSelector('textarea[aria-label*="caption"], div[role="textbox"]', timeout=10000)
        await page.type('textarea[aria-label*="caption"]', caption)
    except:
        pass
    
    try:
        await page.waitForSelector('div[aria-label="Share now"], div[aria-label="Publish"]', timeout=10000)
        await page.click('div[aria-label="Share now"]')
        tulis_log("Share diklik")
    except:
        tulis_log("Share button tidak ditemukan")
    
    await asyncio.sleep(10)
    await browser.close()
    return True

async def proses():
    gambar_files = simpan_gambar()
    try:
        audio = download_audio_from_reels(scrape_trending_reels()[0])
        if not audio:
            return False
        beat = get_beat_times(audio)
        gambar = random.choice(gambar_files)
        temp_vid = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4").name
        vid = generate_sync_video(gambar, beat, temp_vid)
        final_vid = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4").name
        final = merge_video_audio(vid, audio, final_vid)
        success = await upload_to_facebook(final)
        for f in [audio, temp_vid, final, *gambar_files]:
            try: os.unlink(f)
            except: pass
        return success
    except Exception as e:
        tulis_log(f"Error: {e}")
        return False

if __name__ == "__main__":
    tulis_log("Bot dimulai di GitHub Actions")
    result = asyncio.run(proses())
    if not result:
        sys.exit(1)
