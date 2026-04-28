import cloudscraper
from bs4 import BeautifulSoup
import time
import random
import sys
import requests
import re

# DATA ALAT TEMPUR JOHN
EMAIL_USER = "dd7007169@gmail.com" 
ALAMAT_LTC = "MSKfncNgWar33W4Vj4b6nBERo2vVHr5Na8"

class NeuroPredatorV10:
    def __init__(self):
        self.total_jebol = 0
        self.scraper = cloudscraper.create_scraper(
            browser={'browser': 'chrome', 'platform': 'android', 'desktop': False}
        )
        # Daftar awal untuk memancing
        self.daftar_situs = [
            "https://free-ltc.com", "https://ltc-faucet.net", 
            "https://faucet-litecoin.com", "https://claim-free-ltc.net",
            "https://solana-hub.org", "https://tron-miner.biz"
        ]

    def terjun_ke_internet(self):
        # Fitur otomatis mencari link baru jika yang lama macet
        print("\n[!] RADAR AKTIF: Terjun ke internet mencari target baru...")
        try:
            # Mencari di daftar publik/forum secara otomatis
            search_url = "https://www.google.com/search?q=litecoin+faucet+pay+list+2026"
            res = self.scraper.get(search_url, timeout=30)
            links = re.findall(r'(https?://\S+)', res.text)
            
            # Filter situs yang mengandung kata kunci faucet
            new_targets = [l for l in links if "faucet" in l or "claim" in l]
            return list(set(new_targets))[:5]
        except:
            return []

    def hantam(self, url):
        try:
            # Tembus "Kaca" Proteksi
            res = self.scraper.get(url, timeout=45)
            if res.status_code != 200: return "MACET"
            
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

            # Jeda Manusia agar tidak dicurigai admin
            time.sleep(random.randint(20, 40))
            
            post = self.scraper.post(url, data=payload, timeout=45)
            if any(x in post.text.lower() for x in ['success', 'sent', 'added', 'claim']):
                self.total_jebol += 1
                return "DONE"
            return "SKIP (GAGAL)"
        except:
            return "ERROR (KONEKSI)"

    def jalankan(self):
        print("=== NEURO-PREDATOR V10: THE WORLD CRAWLER AKTIF ===")
        print(f"Target: Rp 100.000/hari | LTC: {ALAMAT_LTC}\n")
        
        while True:
            for situs in self.daftar_situs:
                sys.stdout.write(f"[*] Menyerang: {situs}... ")
                sys.stdout.flush()
                
                hasil = self.hantam(situs)
                print(f"[{hasil}]")
                
                # Jika macet, langsung cari link baru di internet
                if hasil != "DONE":
                    temuan = self.terjun_ke_internet()
                    if temuan:
                        for link in temuan:
                            if link not in self.daftar_situs:
                                self.daftar_situs.append(link)
                
                time.sleep(random.randint(30, 60))
            
            print(f"\n--- SIKLUS SELESAI | TOTAL SUKSES: {self.total_jebol} ---")
            print("Istirahat 10 menit agar mesin tetap dingin...")
            time.sleep(600)

if __name__ == "__main__":
    NeuroPredatorV10().jalankan()
