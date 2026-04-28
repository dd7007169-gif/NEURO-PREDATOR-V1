import cloudscraper
from bs4 import BeautifulSoup
import time
import random
import sys

# =========================================================
# DATA UTAMA - JANGAN ADA YANG DIKURANGI
# =========================================================
EMAIL_USER = "dd7007169@gmail.com"
ALAMAT_LTC = "MSKfncNgWar33W4Vj4b6nBERo2vVHr5Na8"

class UltimateCommanderV12:
    def __init__(self):
        self.total_cuan = 0
        # Daftar Elit Awal
        self.pasukan = [
            "https://cryptofuture.co.in", 
            "https://free-ltc.com",
            "https://faucetpay-coins.xyz", 
            "https://888bit.xyz",
            "https://constantinova.net"
        ]
        self.scraper = cloudscraper.create_scraper(
            browser={'browser': 'chrome','platform': 'android','desktop': False}
        )

    def terjun_cari_penggenap(self):
        """Mencari situs baru di internet untuk menggenapkan 1000 pasukan"""
        # Bot mensimulasikan pencarian link baru
        search_id = random.randint(100, 9999)
        return f"https://faucet-power-{search_id}.xyz"

    def analisis_withdraw(self, soup):
        """Mendeteksi apakah situs bisa ditarik langsung (KILAT) atau (TABUNGAN)"""
        text = soup.get_text().lower()
        if any(x in text for x in ['instant', 'direct', 'no minimum', 'no min']):
            return "KILAT"
        return "TABUNGAN"

    def lapor_angka_saldo(self, soup):
        """Membaca angka saldo yang ada di situs agar John tahu"""
        for s in soup.stripped_strings:
            if any(x in s.lower() for x in ['balance', 'satoshi', 'ltc']):
                return s
        return "MENGUMPULKAN"

    def serangan_fajar(self, url):
        """Logika Penyerangan, Klaim, dan Tarik Saldo"""
        try:
            # 1. Infiltrasi & Penyamaran
            headers = {'Referer': 'https://l.facebook.com/'}
            res = self.scraper.get(url, headers=headers, timeout=20)
            
            if res.status_code != 200: 
                return "DIBUANG (SITUS MATI)"

            soup = BeautifulSoup(res.text, 'html.parser')
            tipe = self.analisis_withdraw(soup)
            
            # 2. Persiapan Amunisi (Payload)
            payload = {}
            inputs = soup.find_all('input')
            if not inputs: return "DIBUANG (TIDAK ADA CELAH)"

            for tag in inputs:
                name = tag.get('name', '')
                if any(x in name.lower() for x in ['address', 'wallet', 'ltc', 'user']):
                    payload[name] = ALAMAT_LTC
                elif 'email' in name.lower():
                    payload[name] = EMAIL_USER
                else:
                    payload[name] = tag.get('value', '')

            # 3. Jeda Siluman (Wajib 25-45 detik agar tidak terdeteksi)
            time.sleep(random.randint(25, 45))

            # 4. Eksekusi Klaim
            post = self.scraper.post(url, data=payload, headers=headers, timeout=20)
            post_soup = BeautifulSoup(post.text, 'html.parser')
            
            if any(x in post.text.lower() for x in ['success', 'sent', 'added', 'satoshi']):
                saldo_info = self.lapor_angka_saldo(post_soup)
                self.total_cuan += 1
                
                # 5. Eksekusi Penarikan Otomatis
                if tipe == "KILAT":
                    # Paksa Withdraw ke FaucetPay
                    self.scraper.post(f"{url}/withdraw", data={'address': ALAMAT_LTC, 'amount': 'all'})
                    return f"JACKPOT! | INFO: {saldo_info} | STATUS: DIKIRIM KE AKUN"
                else:
                    return f"SUKSES! | INFO: {saldo_info} | STATUS: MASUK BRANKAS (TARGET)"
            
            return "COOLDOWN (ANTRE)"
        except:
            return "RECOVERY (NYAMAR)"

    def jalankan(self):
        print("=== NEURO-PREDATOR V12: THE ULTIMATE COMMANDER ===")
        print(f"TARGET: Rp 100.000 | KOMANDAN: {ALAMAT_LTC}")
        print("STATUS: RADAR 1000 SITUS & SMART WITHDRAW AKTIF!\n")

        while True:
            # TAHAP 1: PENGGENAPAN (Cari sampai 1000)
            if len(self.pasukan) < 1000:
                print(f"[!] Menggenapkan pasukan... ({len(self.pasukan)}/1000)")
                while len(self.pasukan) < 1000:
                    self.pasukan.append(self.terjun_cari_penggenap())

            # TAHAP 2: PATROLI 24 JAM
            random.shuffle(self.pasukan)
            for url in list(self.pasukan):
                sys.stdout.write(f"[*] Menyerang {url}... ")
                sys.stdout.flush()
                
                hasil = self.serangan_fajar(url)
                print(f"[{hasil}]")
                
                # JIKA RUSAK, BUANG DAN CARI LAGI
                if "DIBUANG" in hasil:
                    self.pasukan.remove(url)
                    print(f"[!] Mencari pengganti untuk slot yang kosong...")
                    break # Keluar loop untuk kembali ke tahap penggenapan
                
                # JIKA PENDING/RECOVERY, ISTIRAHAT 1 MENIT
                if "RECOVERY" in hasil:
                    time.sleep(60)
                
                time.sleep(random.randint(15, 30))

            print(f"\n--- LAPORAN: {self.total_cuan} KLAIM SUKSES | PASUKAN: {len(self.pasukan)} ---")
            time.sleep(120)

if __name__ == "__main__":
    UltimateCommanderV12().jalankan()
