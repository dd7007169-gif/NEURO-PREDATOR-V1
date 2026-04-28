import cloudscraper
from bs4 import BeautifulSoup
import time
import random
import sys

# DATA TETAP JOHN
EMAIL_USER = "dd7007169@gmail.com" 
ALAMAT_LTC = "MSKfncNgWar33W4Vj4b6nBERo2vVHr5Na8"

class AutoCuanV12:
    def __init__(self):
        self.total = 0
        self.scraper = cloudscraper.create_scraper(
            browser={'browser': 'chrome', 'platform': 'android', 'desktop': False}
        )
        self.targets = [
            "https://faucetpay-coins.xyz", "https://cryptofuture.co.in",
            "https://888bit.xyz", "https://constantinova.net"
        ]

    def serang_dan_tarik(self, url):
        try:
            # 1. KLAIM SALDO
            res = self.scraper.get(url, timeout=30)
            soup = BeautifulSoup(res.text, 'html.parser')
            payload = {}
            for tag in soup.find_all('input'):
                name = tag.get('name')
                if name:
                    if any(x in name.lower() for x in ['address', 'wallet', 'user', 'ltc']):
                        payload[name] = ALAMAT_LTC
                    elif 'email' in name.lower():
                        payload[name] = EMAIL_USER
                    else:
                        payload[name] = tag.get('value', '')

            time.sleep(random.randint(20, 40))
            post = self.scraper.post(url, data=payload, timeout=30)
            
            # 2. FITUR BARU: CARI TOMBOL WITHDRAW OTOMATIS
            if "withdraw" in post.text.lower():
                # Jika ada tombol tarik saldo, bot akan otomatis klik
                self.scraper.post(url + "/withdraw", data=payload)
                return "DONE (SALDO TERKIRIM KE FP)"
            
            if "sent" in post.text.lower() or "satoshi" in post.text.lower():
                self.total += 1
                return "DONE (INSTANT PAY)"
            
            return "SUKSES (MASUK SALDO INTERNAL)"
        except:
            return "KONEKSI PADAT"

    def jalankan(self):
        print("=== NEURO-PREDATOR V12: AUTO-WITHDRAW EDITION ===")
        while True:
            for s in self.targets:
                sys.stdout.write(f"[*] Menyerang {s}... ")
                sys.stdout.flush()
                hasil = self.serang_dan_tarik(s)
                print(f"[{hasil}]")
                time.sleep(random.randint(60, 100))
            time.sleep(600)

if __name__ == "__main__":
    AutoCuanV12().jalankan()
