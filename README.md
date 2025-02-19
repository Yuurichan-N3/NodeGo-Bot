# NodeGo Automation Bot

## 📌 Deskripsi
NodeGo Automation Bot adalah skrip Python untuk otomatisasi check-in dan penyelesaian tugas pada platform NodeGo. Skrip ini menggunakan multi-threading untuk menangani banyak akun sekaligus dan mendukung penggunaan proxy untuk meningkatkan anonimitas.

## 🛠️ Fitur
- **Check-in otomatis** untuk akun NodeGo.
- **Otomatis menyelesaikan tugas** yang tersedia di platform.
- **Dukungan proxy** (gratis atau pribadi) untuk koneksi anonim.
- **Multi-threading** untuk eksekusi lebih cepat.
- **Progress bar & logging** untuk memantau proses eksekusi.

## 🏗️ Instalasi
Sebelum menjalankan skrip, pastikan Anda memiliki Python 3.10 dan menginstal dependensi berikut:

```sh
pip install -r requirements.txt


🚀 Cara Penggunaan

1. Siapkan akun & token

Simpan token akun NodeGo di file data.txt, satu token per baris.



2. Menjalankan skrip
Jalankan skrip dengan perintah:

python bot.py


3. Pilih mode proxy

Gunakan proxy gratis

Gunakan proxy pribadi

Jalankan tanpa proxy



4. Pilih jumlah thread

Masukkan jumlah thread untuk mempercepat proses.



5. Proses otomatisasi berjalan

Bot akan mulai melakukan check-in dan menyelesaikan tugas untuk setiap akun.




📌 Catatan

Pastikan file data.txt berisi token akun yang valid.

Untuk menggunakan proxy pribadi, simpan daftar proxy di proxy.txt.

Untuk menggunakan proxy gratis, simpan daftar proxy di proxyshare.txt (not working).


📜 Lisensi

Proyek ini dibuat oleh t.me/sentineldiscus. Silakan gunakan dengan bijak.


---

💡 Disclaimer: Penggunaan bot ini sepenuhnya tanggung jawab pengguna. Kami tidak bertanggung jawab atas penyalahgunaan skrip ini.
