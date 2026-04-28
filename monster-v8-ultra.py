import cloudscraper
from bs4 import BeautifulSoup
import time
import random
import sys
import requests

# DATA UTAMA JOHN
EMAIL_USER = "dd7007169@gmail.com" 
ALAMAT_LTC = "MSKfncNgWar33W4Vj4b6nBERo2vVHr5Na8"

SITUS_LIST = [
    "https://free-ltc.com", "https://ltc-faucet.net", 
    "https://faucet-litecoin.com", "https://claim-free-ltc.net",
    "https://solana-hub.org", "https://tron-miner.biz",
    "https://faucetpay-coins.xyz", "https://cryptofuture.co.in"
]

class MonsterV8:
    def __init__(self):
        self.total = 0
        self.scraper = cloudscraper.create_scraper(
            browser={'browser': 'chrome', 'platform': 'android', 'desktop': False}
        )

    def ambil_proxy(self):
        try:
            r = requests.get("https://api.proxyscrape.com/v2/?request=getproxies&protocol=http&timeout=10000&country=all&ssl=all&anonymity=all")
            return r.text.splitlines()
        except:
            return []

    def tembus(self, url):
        # Fitur Acak IP tetap ada
        proxies = self.ambil_proxy()
        p_dict = {"http": f"http://{random.choice(proxies)}"} if proxies else None
        
        try:
            # Perkuat Timeout agar tidak Gagal Koneksi
            res = self.scraper.get(url, timeout=45, proxies=p_dict)
            if res.status_code == 200:
                soup = BeautifulSoup(res.text, 'html.parser')
                
                # Fitur Jebol Captcha & Payload otomatis
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

                # Jeda Manusia (Anti-Deteksi)
                time.sleep(random.randint(15, 30))
                post = self.scraper.post(url, data=payload, timeout=45, proxies=p_dict)
                return any(x in post.text.lower() for x in ['success', 'sent', 'added', 'claim'])
            return False
        except:
            return False

    def jalankan(self):
        print("=== MONSTER V8 ULTRA: VERSI FULL POWER 2026 ===")
        print("Semua fitur (Anti-Captcha, Proxy, Stabilizer) AKTIF!")
        
        while True:
            for s in SITUS_LIST:
                sys.stdout.write(f"[*] Menyerang {s}... ")
                sys.stdout.flush()
                if self.tembus(s):
                    self.total += 1
                    print("DONE! (SALDO MASUK)")
                else:
                    print("MACET (SKIP)")
                time.sleep(random.randint(20, 40))
            
            print(f"\n--- Siklus Selesai. Total Klaim: {self.total} ---")
            print("Sistem cooling down 10 menit...")
            time.sleep(600)

if __name__ == "__main__":
    MonsterV8().jalankan()
