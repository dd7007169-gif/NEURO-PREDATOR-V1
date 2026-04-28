import cloudscraper
from bs4 import BeautifulSoup
import time
import random
import sys

# =========================================================
# KONFIGURASI HARAM DIUBAH - DATA JOHN
# =========================================================
EMAIL_USER = "dd7007169@gmail.com"
ALAMAT_LTC = "MSKfncNgWar33W4Vj4b6nBERo2vVHr5Na8"

class MegaPredatorFinal:
    def __init__(self):
        self.total_cuan = 0
        self.pasukan = ["https://cryptofuture.co.in", "https://free-ltc.com", "https://888bit.xyz"]
        
        # PENYAMARAN ASAL TRAFIK (FACEBOOK, TIKTOK, GOOGLE, YOUTUBE)
        self.sumber_palsu = [
            'https://www.facebook.com/',
            'https://www.tiktok.com/',
            'https://www.google.com/search?q=free+ltc+faucet+direct+pay',
            'https://l.instagram.com/',
            'https://www.youtube.com/'
        ]
        
        # PENYAMARAN IDENTITAS HP
        self.agen_palsu = [
            'Mozilla/5.0 (Linux; Android 13; SM-S918B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Mobile Safari/537.36',
            'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1',
            'Mozilla/5.0 (Linux; Android 12; Pixel 6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Mobile Safari/537.36'
        ]
        self.scraper = cloudscraper.create_scraper(browser={'browser': 'chrome','platform': 'android','desktop': False})

    def terjun_cari_1000(self):
        """Mencari situs baru otomatis untuk menggenapkan 1000"""
        return f"https://faucet-king-{random.randint(100, 99999)}.net"

    def analisis_withdraw(self, soup):
        """Cek Tipe: Kilat (Langsung Bayar) vs Tabungan (Minimum Withdraw)"""
        text = soup.get_text().lower()
        if any(x in text for x in ['instant', 'direct', 'no minimum']): return "KILAT"
        return "TABUNGAN"

    def serang_total(self, url):
        try:
            # GANTI BAJU & ASAL MASUK (FB, TIKTOK, GOOGLE)
            sumber = random.choice(self.sumber_palsu)
            headers = {
                'User-Agent': random.choice(self.agen_palsu),
                'Referer': sumber
            }
            
            res = self.scraper.get(url, headers=headers, timeout=25)
            if res.status_code != 200: return "BUANG (MATI)"

            soup = BeautifulSoup(res.text, 'html.parser')
            tipe = self.analisis_withdraw(soup)
            
            payload = {}
            for tag in soup.find_all('input'):
                name = tag.get('name', '')
                if any(x in name.lower() for x in ['address', 'wallet', 'ltc', 'user']):
                    payload[name] = ALAMAT_LTC # SUNTIK ALAMAT JOHN
                elif 'email' in name.lower():
                    payload[name] = EMAIL_USER
                else: payload[name] = tag.get('value', '')

            time.sleep(random.randint(25, 45)) # Jeda Bypass
            post = self.scraper.post(url, data=payload, headers=headers, timeout=25)
            
            if any(x in post.text.lower() for x in ['success', 'sent', 'added', 'satoshi']):
                self.total_cuan += 1
                if tipe == "KILAT":
                    # TARIK PAKSA DETIK ITU JUGA
                    self.scraper.post(f"{url}/withdraw", data={'address': ALAMAT_LTC, 'amount': 'all'})
                    return f"JACKPOT! -> {sumber[:25]}..."
                return "SUKSES! (TABUNGAN)"
            return "COOLDOWN"
        except: return "RECOVERY (NYAMAR)"

    def jalankan(self):
        print("=== MEGA-PREDATOR V12: GHOST PROTOCOL ACTIVE ===")
        print(f"WALLET TARGET: {ALAMAT_LTC}")
        print("MENGGUNAKAN TRAFIK: FB, TIKTOK, GOOGLE, YOUTUBE\n")
        
        while True:
            # Pastikan 1000 pasukan siap
            while len(self.pasukan) < 1000:
                self.pasukan.append(self.terjun_cari_1000())

            for url in list(self.pasukan):
                sys.stdout.write(f"[*] Menyerang {url}... ")
                sys.stdout.flush()
                hasil = self.serang_total(url)
                print(f"[{hasil}]")
                if "BUANG" in hasil:
                    self.pasukan.remove(url)
                    break
                time.sleep(random.randint(15, 30))

if __name__ == "__main__":
    MegaPredatorFinal().jalankan()
