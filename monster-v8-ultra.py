import cloudscraper
from bs4 import BeautifulSoup
import time
import random
import sys

# DATA TETAP JOHN
EMAIL_USER = "dd7007169@gmail.com"
ALAMAT_LTC = "MSKfncNgWar33W4Vj4b6nBERo2vVHr5Na8"

class SniperPredatorV12:
    def __init__(self):
        self.total_jebol = 0
        # Browser sidik jari 2026
        self.scraper = cloudscraper.create_scraper(
            browser={
                'browser': 'chrome',
                'platform': 'android',
                'desktop': False
            }
        )

    def analisis_celah(self, url):
        try:
            # 1. Masuk dan Cari Celah (Micro-Gap Search)
            res = self.scraper.get(url, timeout=35)
            if res.status_code != 200: return "RECOVERY"

            soup = BeautifulSoup(res.text, 'html.parser')
            payload = {}
            
            # Mencari celah di semua input (termasuk yang tersembunyi/hidden)
            for tag in soup.find_all(['input', 'select', 'textarea']):
                name = tag.get('name')
                if name:
                    n_low = name.lower()
                    # Memasukkan alamat dompet ke celah yang tepat
                    if any(x in n_low for x in ['address', 'wallet', 'user', 'ltc', 'coin', 'token']):
                        payload[name] = ALAMAT_LTC
                    elif 'email' in n_low:
                        payload[name] = EMAIL_USER
                    else:
                        # Mengambil nilai default yang disediakan situs untuk memicu celah
                        payload[name] = tag.get('value', '')

            # 2. CAPCAY HARDENER (Simulasi Jeda Manusia)
            # Menunggu seolah-olah manusia sedang melihat gambar captcha
            time.sleep(random.randint(20, 45))

            # 3. Eksekusi Tembusan
            post = self.scraper.post(url, data=payload, timeout=35)
            respon = post.text.lower()

            if any(x in respon for x in ['success', 'sent', 'added', 'claim', 'satoshi']):
                self.total_jebol += 1
                return "DONE (JEBOL!)"
            return "SKIP (CELAH TERTUTUP)"
            
        except:
            return "RECOVERY"

    def jalankan(self):
        print("=== NEURO-PREDATOR V12: SNIPER EDITION 2026 ===")
        print(f"Target: Rp 100.000 | Mencari Celah Sekecil Mungkin...")
        print(f"Dompet: {ALAMAT_LTC}\n")

        targets = [
            "https://cryptofuture.co.in", "https://888bit.xyz",
            "https://faucetpay-coins.xyz", "https://constantinova.net",
            "https://free-ltc.com", "https://ltc-faucet.net"
        ]

        while True:
            random.shuffle(targets)
            for s in targets:
                sys.stdout.write(f"[*] Menganalisis Celah di {s}... ")
                sys.stdout.flush()
                
                hasil = self.analisis_celah(s)
                print(f"[{hasil}]")

                if hasil == "RECOVERY":
                    print("[!] KONEKSI PADAT, ISTIRAHAT 1 MENIT (60s)...")
                    time.sleep(60)
                
                # Jeda antar target diperketat (25-45 detik)
                time.sleep(random.randint(25, 45))

            print(f"\n--- TOTAL KLAIM SUKSES: {self.total_jebol} ---")
            time.sleep(300)

if __name__ == "__main__":
    SniperPredatorV12().jalankan()
