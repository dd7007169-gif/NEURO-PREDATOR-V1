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

SITUS_LIST = [
    "https://free-ltc.com", "https://ltc-faucet.net", 
    "https://claim-tron.com", "https://sol-miner.com",
    "https://doge-clicker.com", "https://faucet-litecoin.com",
    "https://claim-free-ltc.net", "https://solana-hub.org",
    "https://tron-miner.biz", "https://faucetpay-coins.xyz"
]

class MonsterV8:
    def __init__(self):
        self.scraper = cloudscraper.create_scraper(
            browser={'browser': 'chrome', 'platform': 'android', 'desktop': False}
        )
        self.total_claim = 0

    def log(self, pesan):
        print(f"[{time.strftime('%H:%M:%S')}] {pesan}")

    def eksekusi(self, url):
        try:
            # Bypass proteksi awal
            res = self.scraper.get(url, timeout=20)
            soup = BeautifulSoup(res.text, 'html.parser')
            
            payload = {}
            for tag in soup.find_all('input'):
                name = tag.get('name')
                if name:
                    if any(x in name.lower() for x in ['address', 'wallet', 'user']):
                        payload[name] = ALAMAT_LTC
                    elif 'email' in name.lower():
                        payload[name] = EMAIL_FAUCETPAY
                    else:
                        payload[name] = tag.get('value', '')

            form = soup.find('form')
            action = form.get('action') if form else '/index.php'
            target = url.rstrip('/') + '/' + action.lstrip('/') if not action.startswith('http') else action

            # Simulasi waktu tunggu manusia
            time.sleep(random.randint(8, 15))

            post_res = self.scraper.post(target, data=payload, headers={'Referer': url})
            return any(x in post_res.text.lower() for x in ['success', 'sent', 'added'])
        except:
            return False

    def jalankan(self):
        self.log("=== MONSTER V8 ULTRA: STARTING ATTACK ===")
        while True:
            berhasil = 0
            for i, situs in enumerate(SITUS_LIST, 1):
                sys.stdout.write(f"[*] Menjebol ({i}/{len(SITUS_LIST)}): {situs}...")
                sys.stdout.flush()
                
                if self.eksekusi(situs):
                    berhasil += 1
                    self.total_claim += 1
                    print(" [BERHASIL]")
                else:
                    print(" [GAGAL]")
                
                time.sleep(random.randint(20, 40)) # Jeda aman agar tidak terbanned
            
            self.log(f"Putaran Selesai. Total Klaim Hari Ini: {self.total_claim}")
            # Istirahat 10 menit
            time.sleep(600)

if __name__ == "__main__":
    MonsterV8().jalankan()
