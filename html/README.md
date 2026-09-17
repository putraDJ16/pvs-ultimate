# PV Solution — Admin / ICONGreen / Mitra — HTML + CSS statis

Hasil konversi file Figma **PV Solution** (`2hT4RGbMYDIXKTKqqF3BMy`) ke HTML + CSS
statis. Tidak ada framework, tidak ada build step — buka `screens.html` langsung
di browser.

File Figma ini punya 3 page: **Admin**, **IconGreen Admin** (portal operasional
ICONGreen), dan **Mitra** (portal mitra EPC) — total 50 frame. Ketiganya
dikonversi jadi 3 portal terpisah dengan sidebar & warna yang berbeda per role,
tapi satu design system yang sama.

## Cara pakai

Buka **`index.html`** — halaman "login" dengan 3 tombol portal (Admin ICON /
ICONGreen / Mitra), klik salah satu untuk masuk langsung ke dashboard-nya. Atau
buka **`screens.html`** untuk daftar semua 33 layar dikelompokkan per role.
Semua navigasi antar halaman dalam satu portal sudah terhubung lewat sidebar &
tombol aksi.

## Struktur

```
index.html                "login" — 3 tombol portal (bukan bagian desain Figma — halaman masuk)
screens.html             daftar semua layar (bukan bagian desain Figma — bantuan navigasi)
admin/                    Portal Admin ICON (Budi Santoso)
  dashboard.html
  users.html              User Management
  user-detail.html        Detail user (+ tab)
  partners.html           Partner Management
  partner-add.html        Tambah Mitra (+ tab)
  master-data.html        Master Data
  audit-log.html          Audit Log
ops/                       Portal ICONGreen / Operasional (Rina Kusumawati)
  dashboard.html
  executive-dashboard.html
  work-orders.html
  wo-detail.html           Stepper 7 tahap + 8 tab
  surveys.html
  survey-detail.html       Alur negosiasi tanggal
  quotations.html
  quotation-detail.html
  projects.html
  project-detail.html      + 6 tab
  partners.html             Partner Directory
  partner-detail.html      + 4 tab
  billing.html
mitra/                     Portal Mitra EPC (Dewi Lestari, PT Alpha Solar Energi)
  dashboard.html
  opportunities.html
  surveys.html
  survey-negotiation.html  Stepper 6 tahap + usulkan tanggal
  survey-report.html       Estimasi biaya + rating otomatis
  quotations.html
  quotation-form.html      2 tab: Technical Proposal / Bill of Quantity
  projects.html
  project-detail.html      + 5 tab
  update-progress.html     Input progress per item, 3 tahap
  rating.html               Rating Proyek
  rating-form.html          5 kriteria bintang + komentar
  company-profile.html     + 5 tab
assets/
  styles.css                design token + seluruh komponen (33 section)
  app.js                    modal + tab switching (± 40 baris, tanpa dependensi)
gen.py                      helper generator: sidebar, topbar, kartu, dst.
pages_admin.py               generator halaman Admin
pages_ops.py                 generator halaman ICONGreen
pages_mitra.py               generator halaman Mitra
```

## Cakupan per tab

Beberapa halaman detail punya banyak tab (mis. `wo-detail.html` punya 8 tab,
`project-detail.html` di Ops punya 6 tab). Tab pertama/utama dibangun lengkap
dan sudah diverifikasi terhadap Figma; tab-tab sekunder (Partner, Dokumen,
Issues, Aktivitas, dll.) ditandai jelas judulnya tapi isinya placeholder —
ini pilihan sadar supaya seluruh 33 layar bisa selesai dengan rapi dalam satu
proses konversi. Kalau perlu detail penuh di tab tertentu, kasih tahu saja.

## Design token

Palet portal ini beda dari desain PV Solution yang pertama — nuansa
**dark slate + green ("IconGreen")**, bukan biru terang:

| Token | Nilai | Dipakai untuk |
|---|---|---|
| `--brand` | `#16A34A` | tombol primary, link, active state |
| `--sidebar-bg` | `#0F172A` | sidebar semua portal |
| `--page-bg` | `#F1F5F9` | latar halaman |
| `--font-head` | DM Sans | heading |
| `--font-body` | Inter | body |
| radius | 6 / 8 / 10 px, full untuk avatar/badge | |

Skala abu-abu mengikuti Tailwind Slate (`#F1F5F9` = slate-100, `#94A3B8` =
slate-400, dst.), warna status (blue/cyan/amber/red/purple/green) juga
palet Tailwind standar.

## Catatan implementasi

- **Ikon adalah karakter emoji**, bukan SVG — desain Figma-nya sendiri memakai
  emoji sebagai ikon (☀ 🎯 📍 💼 🏗 🔔 dst.), jadi dipertahankan apa adanya
  untuk akurasi visual, bukan diganti vektor.
- **Font** di-load dari Google Fonts lewat `<link>`. Kalau jaringan memblokir
  `fonts.googleapis.com`, halaman jatuh ke font sistem dan spacing bergeser
  sedikit.
- **Layout pakai flex/grid**, bukan absolute positioning, supaya lebih mudah
  diterjemahkan ke komponen Angular/React nanti.
- **Desain hanya punya breakpoint desktop** (~1329&ndash;1441px sesuai frame
  Figma). Tidak dibuat responsive karena tidak ada acuan mobile.
- **Tidak ada logika bisnis** — form tidak memvalidasi dan tidak mengirim apa
  pun. Tab pakai JavaScript murni (`data-tab` / `data-tabs`), modal pakai pola
  yang sama seperti proyek PV Solution sebelumnya.
- Satu frame Figma (`8:5518`, work order sync state) tidak bisa di-render jadi
  PNG lewat Figma API meski sudah dicoba berkali-kali (masalah di sisi Figma).
  `ops/work-orders.html` dibangun memakai frame kembarannya (`108:1118`) yang
  isinya nyaris identik sebagai acuan visual.

## Kalau desainnya berubah

Semua halaman di-generate dari `gen.py` + `pages_admin.py` / `pages_ops.py` /
`pages_mitra.py` supaya sidebar & topbar tidak pernah beda antar halaman.
Untuk ubah navigasi, warna, atau isi halaman: edit file generator terkait lalu
jalankan `python pages_admin.py` (atau `pages_ops.py` / `pages_mitra.py`) dari
dalam folder ini — halaman-halaman portal itu ditulis ulang. `assets/` dan
`screens.html` ditulis manual, tidak tersentuh script.

## Keamanan token Figma

Script PowerShell yang dipakai untuk mengambil data & gambar dari Figma
(`fetch-figma.ps1`, `fetch-images.ps1`, `fetch-images-retry.ps1`) menyimpan
personal access token Figma dalam bentuk teks biasa. Setelah selesai, **hapus
ketiga file ini** dari folder kerja dan pertimbangkan untuk **revoke token**
tersebut di pengaturan akun Figma (Settings → Personal access tokens), supaya
token tidak tertinggal di mesin dalam bentuk yang bisa dibaca siapa saja.
