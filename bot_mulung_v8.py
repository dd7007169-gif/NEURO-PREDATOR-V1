import cloudscraper
from bs4 import BeautifulSoup
import time
import random
import sys

# ==========================================
# DATA AKUN UTAMA JOHN
# ==========================================
EMAIL_FAUCETPAY = "dd7007169@gmail.com"
ALAMAT_LTC = "MSKfncNgWar33W4Vj4b6nBERo2vVHr5Na8"

# Daftar target (Bisa kamu tambah sampai ratusan situs)
SITUS_LIST = [
    "https://free-ltc.com", "https://ltc-faucet.net", 
    "https://claim-tron.com", "https://sol-miner.com",
    "https://doge-clicker.com", "https://faucet-litecoin.com",
    "https://claim-free-ltc.net", "https://solana-hub.org",
    "https://tron-miner.biz", "https://faucetpay-coins.xyz"
]

class MonsterV8:
    def __init__(self):
        # Menggunakan engine Android agar lebih sulit dideteksi server
        self.scraper = cloudscraper.create_scraper(
            browser={'browser': 'chrome', 'platform': 'android', 'desktop': False}
        )
        self.total_berhasil = 0

    def log(self, pesan):
        timestamp = time.strftime("%H:%M:%S")
        print(f"[{timestamp}] {pesan}")

    def tembus_kaca(self, url):
        try:
            # 1. Masuk ke situs (Bypass Cloudflare Waiting Room)
            response = self.scraper.get(url, timeout=20)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # 2. Ambil semua token keamanan (CSRF/Token/Session) secara otomatis
            payload = {}
            for tag in soup.find_all('input'):
                name = tag.get('name')
                if name:
                    # Isi address atau email secara otomatis pada kolom yang tepat
                    if any(x in name.lower() for x in ['address', 'wallet', 'user']):
                        payload[name] = ALAMAT_LTC
                    elif 'email' in name.lower():
                        payload[name] = EMAIL_FAUCETPAY
                    else:
                        payload[name] = tag.get('value', '')

            # 3. Cari URL pengiriman (Form Action)
            form = soup.find('form')
            action = form.get('action') if form else '/index.php'
            target_url = url.rstrip('/') + '/' + action.lstrip('/') if not action.startswith('http') else action

            # Jeda sebentar sebelum nembak (simulasi isi form)
            time.sleep(random.randint(3, 7))

            # 4. Eksekusi Serangan (POST Data)
            hasil = self.scraper.post(target_url, data=payload, headers={'Referer': url})
            
            if hasil.status_code == 200 and any(x in hasil.text.lower() for x in ['success', 'sent', 'added']):
                return True
            return False
        except Exception as e:
            return False

    def jalankan(self):
        self.log("=== BOT MONSTER V8: MODE TARGET RP 100.000 ===")
        self.log(f"Targeting {len(SITUS_LIST)} situs koin...")
        
        while True:
            putaran_berhasil = 0
            for i, situs in enumerate(SITUS_LIST, 1):
                sys.stdout.write(f"\r[*] Menjebol ({i}/{len(SITUS_LIST)}): {situs}...")
                sys.stdout.flush()
                
                if self.tembus_kaca(situs):
                    putaran_berhasil += 1
                    self.total_berhasil += 1
                    print(" [SUKSES]")
                else:
                    print(" [GAGAL/CAPTCHA]")
                
                # JEDAH PENTING: Antar situs 10-25 detik (Biar gak kena Banned IP)
                time.sleep(random.randint(10, 25))
            
            self.log(f"Laporan Putaran: {putaran_berhasil} Berhasil.")
            self.log(f"Total Klaim Hari Ini: {self.total_berhasil}")
            
            # ISTIRAHAT BESAR: 5-10 Menit (Supaya server lawan tidak curiga)
            istirahat = random.randint(300, 600)
            self.log(f"Siklus selesai. Istirahat {istirahat//60} menit agar akun aman...")
            time.sleep(istirahat)

if __name__ == "__main__":
    bot = MonsterV8()
    bot.jalankan()
