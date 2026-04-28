import cloudscraper
from bs4 import BeautifulSoup
import time
import random
import sys
import socket

# DATA AKUN
EMAIL_USER = "dd7007169@gmail.com" 
ALAMAT_LTC = "MSKfncNgWar33W4Vj4b6nBERo2vVHr5Na8"

# Gunakan situs yang lebih stabil untuk testing awal
SITUS_LIST = [
    "https://free-ltc.com", 
    "https://ltc-faucet.net", 
    "https://faucet-litecoin.com",
    "https://coinpayu.com"
]

class MonsterV8:
    def __init__(self):
        # Tambahkan header agar tidak terlihat seperti server
        self.scraper = cloudscraper.create_scraper(
            browser={
                'browser': 'chrome',
                'platform': 'android',
                'desktop': False
            }
        )
        self.total = 0

    def tembus(self, url):
        try:
            # Coba koneksi sampai 3 kali jika gagal DNS
            for attempt in range(3):
                try:
                    res = self.scraper.get(url, timeout=30)
                    if res.status_code == 200:
                        soup = BeautifulSoup(res.text, 'html.parser')
                        payload = {}
                        for tag in soup.find_all('input'):
                            name = tag.get('name')
                            if name:
                                if any(x in name.lower() for x in ['address', 'wallet', 'user']):
                                    payload[name] = ALAMAT_LTC
                                elif 'email' in name.lower():
                                    payload[name] = EMAIL_USER
                                else:
                                    payload[name] = tag.get('value', '')

                        time.sleep(random.randint(10, 15))
                        post = self.scraper.post(url, data=payload, timeout=30)
                        return post.status_code == 200
                except (socket.gaierror, Exception):
                    time.sleep(5) # Tunggu 5 detik sebelum coba lagi
                    continue
            return False
        except:
            return False

    def jalankan(self):
        print("=== MONSTER V8 ULTRA: STABILIZER MODE ===")
        while True:
            for s in SITUS_LIST:
                sys.stdout.write(f"[*] Menyerang {s}... ")
                sys.stdout.flush()
                if self.tembus(s):
                    self.total += 1
                    print("HASIL: TEMBUS!")
                else:
                    print("HASIL: GAGAL KONEKSI")
                time.sleep(random.randint(15, 30))
            
            print(f"Total Sukses: {self.total}")
            time.sleep(600)

if __name__ == "__main__":
    MonsterV8().jalankan()
