# DamnCRUD Automated UI Testing

Repositori ini mengatur otomasi pengujian Fungsional dan UI untuk aplikasi PHP **DamnCRUD**. Skenario uji menggunakan ekosistem canggih dari **Selenium WebDriver** dan **Pytest**, serta telah dilatih untuk berjalan secara paralel di pipeline **GitHub Actions CI/CD**.

## 🚀 Fitur Utama

- **Otomasi End-to-End (E2E):** Menjalankan 5 fungsionalitas utama (*Read Dashboard, Create, Update, Delete, Search DataTables*) sepenuhnya dengan mensimulasikan gerak-gerik pengguna.
- **Tahan Banting terhadap XSS:** Skenario uji telah didesain khusus agar kebal dari kemunculan *Alert Javascript* jahat jika sewaktu-waktu aplikasi menampilkan kerentanan _Cross-Site Scripting_ tanpa membuat skrip gagal.
- **Eksekusi Pytest Paralel (`pytest-xdist`):** Kerangka kerja di-konfigurasi untuk menguji semua *Test Case* secara bersamaan (Multi-Threading) dan sangat cepat, sekaligus menghindari isolasi *Race-Condition* (tabrakan manipulasi data antar pekerja bot).
- **Integrasi CI/CD Otomatis:** Diperkuat dengan resep *Workflow GitHub Actions* siap pakai. Setiap pembaruan kode akan memicu Robot Server Ubuntu untuk merakit modul PHP, MySQL Docker, dan simulasi skrip *Headless Browser* secara mandiri.

## 🛠️ Persyaratan Lingkungan (Lokal)

- **Python 3.9+** & Package Manager (`pip`)
- **PHP 8.x** (Bisa melalui Laragon / XAMPP)
- **MySQL Database Server** 
- **Google Chrome** Peramban

## 💻 Cara Menjalankan Pengujian di Lokal

1. Persiapkan skema *Database* dan data dumyy awal. Impor berkas SQL bawaan berikut pada *MySQL Client* Anda:
   ```bash
   mysql -u root damncrud < DamnCRUD/db/damncrud.sql
   ```
2. Nyalakan peladen web PHP di belakang terminal layar utama Anda:
   ```bash
   php -S localhost:8000
   ```
3. Instal dukungan modul pustaka untuk Python:
   ```bash
   pip install -r requirements.txt
   ```
4. Jalankan pengujian Selenium secara berbarengan (*auto workers*) dan amati _browser_ Chrome di laptop Anda saling berkerumun melakukan pengujian mandiri:
   ```bash
   pytest test_crud_pytest.py -n auto -v
   ```

## 🌐 Pipeline GitHub Actions

Pemeriksaan keamanan terpadu di repositori ini otomatis terpicu begitu *Developer* men-_push_ perubahan di _branch_ apapun atau saat mengajukan mekanisme `Pull Request` kepada *Branch* Utama (`main`). 

Pekerja (Runner) GitHub yang ditugaskan akan mengkonfigurasi lingkungan Ubuntu _Virtual Machine_, mengalokasikan parameter peladen *PHP Multiplayer Concurrency* (`PHP_CLI_SERVER_WORKERS: 5`), membangun koneksi MySQL dan mensimulasikan navigasi antarmuka dalam mode transparan (_Headless Chrome_). Anda dapat mengejawantahkan statusnya secara langsung pada log *Tab Actions* di antarmuka Web GitHub atas repositori kode Anda.
