"""Admin portal pages. Imported and run by gen.py's __main__ block."""
from gen import OUT, page, kpi, card, badge, icon, kv

def write(path, html):
    p = OUT / 'admin' / path
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(html, encoding='utf-8')
    print('wrote admin/' + path)

def build_dashboard():
    kpis = f'''<div class="kpi-row">
      {kpi('Total User', '8', 'purple', '👥')}
      {kpi('Active User', '6', 'green', '✅', '2 non-aktif')}
      {kpi('Total Mitra', '6', 'cyan', '🏢')}
      {kpi('Menunggu Verifikasi', '2', 'amber', '⏳', 'Perlu tindakan')}
    </div>'''

    user_card = card(
        'User Management',
        f'''<div class="flex" style="gap:24px;margin-bottom:16px">
          <div><div style="font:700 26px var(--font-head);color:#6B7280">8</div><div class="sub">Total</div></div>
          <div><div style="font:700 26px var(--font-head);color:var(--green-600)">6</div><div class="sub">Aktif</div></div>
          <div><div style="font:700 26px var(--font-head);color:var(--red-600)">1</div><div class="sub">Nonaktif</div></div>
          <div><div style="font:700 26px var(--font-head);color:var(--blue-600)">1</div><div class="sub">Pending</div></div>
        </div>
        <div style="border-top:1px solid var(--slate-200);padding-top:14px" class="role-list">
          <div class="role-list__row"><span class="role-list__label">Admin ICON</span><span class="role-list__bar">{'<div class="pbar"><span style="width:25%;background:#7C3AED"></span></div>'}</span><span class="role-list__num" style="color:#7C3AED">2</span></div>
          <div class="role-list__row"><span class="role-list__label">ICONGreen</span><span class="role-list__bar">{'<div class="pbar"><span style="width:38%;background:var(--green-600)"></span></div>'}</span><span class="role-list__num" style="color:var(--green-600)">3</span></div>
          <div class="role-list__row"><span class="role-list__label">Mitra</span><span class="role-list__bar">{'<div class="pbar"><span style="width:38%;background:#0891B2"></span></div>'}</span><span class="role-list__num" style="color:#0891B2">3</span></div>
        </div>''',
        '<span class="sub">Distribusi Role</span>'
    )

    partner_card = card(
        'Partner Management',
        f'''<div class="flex" style="gap:24px;margin-bottom:16px">
          <div><div style="font:700 26px var(--font-head);color:#6B7280">6</div><div class="sub">Registered</div></div>
          <div><div style="font:700 26px var(--font-head);color:var(--green-600)">3</div><div class="sub">Verified</div></div>
          <div><div style="font:700 26px var(--font-head);color:var(--amber-600)">2</div><div class="sub">Pending</div></div>
          <div><div style="font:700 26px var(--font-head);color:var(--red-600)">1</div><div class="sub">Suspended</div></div>
        </div>
        <div class="muted" style="font:700 11px var(--font-head);letter-spacing:.4px;text-transform:uppercase;border-top:1px solid var(--slate-200);padding-top:14px;margin-bottom:10px">Menunggu Verifikasi</div>
        <div class="flex justify-between items-center" style="padding:8px 0;border-bottom:1px solid var(--slate-100)">
          <div><div style="font:600 13px var(--font-head)">PT Gamma Solar</div><div class="sub">PV Developer &middot; Bandung</div></div>
          {badge('Menunggu Verifikasi', 'amber')}
        </div>
        <div class="flex justify-between items-center" style="padding:8px 0">
          <div><div style="font:600 13px var(--font-head)">PT Delta Energi Nusantara</div><div class="sub">Vendor &middot; Medan</div></div>
          {badge('Menunggu Verifikasi', 'amber')}
        </div>'''
    )

    activity = [
        ('#DCFCE7', '✓', 'Memverifikasi Mitra PT Alpha Solar Energi', 'Admin Budi &middot; Hari ini, 09:45'),
        ('#DBEAFE', '+', 'Membuat user baru: Bambang Nugroho (Mitra)', 'Admin Budi &middot; Hari ini, 09:12'),
        ('#CFFAFE', '📍', 'WO-2024-0047 &ndash; Mengajukan jadwal survey ke Alpha Solar', 'Rina Kusumawati &middot; Hari ini, 08:55'),
        ('#FFF5F5', '✕', 'Menonaktifkan user Sari Indah', 'Admin Fitri &middot; Kemarin, 16:30'),
        ('#FEF3C7', '↑', 'WO-2024-0046 &ndash; Progress proyek RSUD diperbarui: 42%', 'Agus Pratama &middot; Kemarin, 15:44'),
        ('#F3E8FF', '⚙', 'Master Data Project Type diperbarui', 'Admin Fitri &middot; Kemarin, 14:22'),
    ]
    items = ''
    for bg, ic, t, d in activity:
        items += f'''<div class="timeline__item">
          <div class="timeline__dot" style="background:{bg}">{icon(ic, 13)}</div>
          <div class="timeline__body"><div class="t">{t}</div><div class="d">{d}</div></div>
        </div>'''
    activity_card = card('Recent Activity', f'<div class="mt-16">{items}</div>')

    content = f'''      <div class="page-head"><h1 class="h1">Dashboard Admin</h1><p class="sub">Ringkasan administrasi sistem PV Solution &middot; Kamis, 11 September 2024</p></div>
      {kpis}
      <div class="grid-2 mt-24">{user_card}{partner_card}</div>
      <div class="mt-24">{activity_card}</div>'''

    write('dashboard.html', page('admin', 'dashboard.html', 'Dashboard', 'Dashboard Admin', content))

def dot_badge(text, kind):
    return f'<span class="badge badge--{kind}"><span class="dot"></span>{text}</span>'

def avatar(letter, kind):
    colors = {'purple': ('#F3E8FF', '#7C3AED'), 'green': ('#DCFCE7', '#15803D'), 'cyan': ('#CFFAFE', '#0E7490')}
    bg, fg = colors[kind]
    return f'<span class="avatar-sm" style="background:{bg};color:{fg}">{letter}</span>'

def build_users():
    rows_data = [
        ('B', 'purple', 'Budi Santoso', 'USR-001', 'budi.santoso@icon.co.id', 'PT ICON+', 'Admin ICON', 'purple', 'Aktif', 'green', '2024-09-11 08:32'),
        ('R', 'green', 'Rina Kusumawati', 'USR-002', 'rina.k@icongreen.co.id', 'PT ICONGreen', 'ICONGreen', 'green', 'Aktif', 'green', '2024-09-11 09:15'),
        ('A', 'green', 'Agus Pratama', 'USR-003', 'agus.p@icongreen.co.id', 'PT ICONGreen', 'ICONGreen', 'green', 'Aktif', 'green', '2024-09-10 16:44'),
        ('D', 'cyan', 'Dewi Lestari', 'USR-004', 'dewi.l@alphasolar.co.id', 'PT Alpha Solar Energi', 'Mitra', 'cyan', 'Aktif', 'green', '2024-09-11 07:58'),
        ('H', 'cyan', 'Hendra Wijaya', 'USR-005', 'hendra@betaepc.co.id', 'PT Beta EPC Indonesia', 'Mitra', 'cyan', 'Aktif', 'green', '2024-09-09 14:20'),
        ('S', 'green', 'Sari Indah', 'USR-006', 'sari.indah@icongreen.co.id', 'PT ICONGreen', 'ICONGreen', 'green', 'Nonaktif', 'red', '2024-08-01 10:00'),
        ('B', 'cyan', 'Bambang Nugroho', 'USR-007', 'bambang@gammasolar.co.id', 'PT Gamma Solar', 'Mitra', 'cyan', 'Pending', 'blue', '-'),
        ('F', 'purple', 'Fitri Handayani', 'USR-008', 'fitri@icon.co.id', 'PT ICON+', 'Admin ICON', 'purple', 'Aktif', 'green', '2024-09-10 11:30'),
    ]
    trs = ''
    for init, akind, name, uid, email, company, role, rkind, status, skind, login in rows_data:
        detail_href = 'user-detail.html' if uid == 'USR-001' else '#'
        trs += f'''<tr>
          <td><div class="flex items-center gap-12">{avatar(init, akind)}<div><div class="strong">{name}</div><div class="sub">{uid}</div></div></div></td>
          <td>{email}</td>
          <td>{company}</td>
          <td>{badge(role, rkind)}</td>
          <td>{dot_badge(status, skind)}</td>
          <td>{login}</td>
          <td><a href="{detail_href}" style="font:600 13px var(--font-head);color:var(--green-700)">Detail</a></td>
        </tr>'''

    content = f'''      <div class="page-head-row">
        <div><h1 class="h1">User Management</h1><p class="sub mt-4">8 pengguna terdaftar dalam sistem</p></div>
        <button class="btn btn--primary">{icon('+',13)} Tambah User</button>
      </div>
      <div class="filterbar">
        <div class="search">{icon('🔍',15)}<input class="input" placeholder="Cari nama atau email..."></div>
        <select class="select select--sm"><option>Semua Role</option></select>
      </div>
      <div class="card" style="padding:0">
        <table class="tbl" style="margin:0">
          <thead><tr><th style="padding-left:20px">NAMA</th><th>EMAIL</th><th>PERUSAHAAN</th><th>ROLE</th><th>STATUS</th><th>LAST LOGIN</th><th style="padding-right:20px">AKSI</th></tr></thead>
          <tbody>{trs}</tbody>
        </table>
      </div>'''
    write('users.html', page('admin', 'users.html', 'User Management', 'User Management', content))

def build_user_detail():
    info_tab = card(None, f'''<div class="muted" style="font:700 11px var(--font-head);letter-spacing:.4px;text-transform:uppercase;margin-bottom:16px">Data Pribadi</div>
      <div class="kv-grid" style="grid-template-columns:1fr">
        {kv('Nama Lengkap', 'Budi Santoso')}
        {kv('Email', 'budi.santoso@icon.co.id')}
        {kv('Perusahaan', 'PT ICON+')}
        {kv('Role', 'Admin ICON')}
        {kv('Status', 'Aktif')}
        {kv('Dibuat', '2023-01-15')}
        {kv('Last Login', '2024-09-11 08:32')}
      </div>''')

    activities = [
        ('2024-09-11 09:15', 'Login ke sistem'),
        ('2024-09-11 09:20', 'Membuka halaman Work Order'),
        ('2024-09-10 16:44', 'Memperbarui progress proyek PRJ-2024-0019'),
        ('2024-09-10 14:30', 'Mengkonfirmasi jadwal survey SVY-2024-0031'),
        ('2024-09-09 10:12', 'Login ke sistem'),
    ]
    rows = ''.join(f'<div class="flex gap-12" style="padding:12px 0;border-bottom:1px solid var(--slate-100);font-size:13px"><span class="mono" style="color:var(--slate-400);font-weight:400;width:150px;flex:none">{d}</span><span>{t}</span></div>' for d, t in activities)
    activity_tab = card(None, f'<div class="muted" style="font:700 11px var(--font-head);letter-spacing:.4px;text-transform:uppercase;margin-bottom:12px">Riwayat Aktivitas</div>{rows}')

    content = f'''      <a class="back-link" href="users.html">{icon('←',13)} Kembali</a>
      <div class="page-head-row">
        <div><h1 class="h1">Budi Santoso</h1><p class="sub mt-4">USR-001 &middot; PT ICON+ &middot; Admin ICON</p></div>
        <div class="flex gap-8">
          <button class="btn btn--outline">Edit User</button>
          <button class="btn btn--outline">Reset Password</button>
          <button class="btn btn--soft-red">Nonaktifkan</button>
        </div>
      </div>
      <div class="flex gap-8 mt-16" style="margin-bottom:20px">{dot_badge('Aktif','green')}{badge('Admin ICON','purple')}</div>
      <div class="tabs" data-tabs="user">
        <a href="#" class="tab is-active" data-tab="info">Informasi User</a>
        <a href="#" class="tab" data-tab="act">Aktivitas User</a>
      </div>
      <div data-tab-panel="info" data-tabs-for="user">{info_tab}</div>
      <div data-tab-panel="act" data-tabs-for="user" hidden>{activity_tab}</div>'''
    write('user-detail.html', page('admin', 'users.html', 'User Management', 'Budi Santoso', content))

def build_partners():
    rows_data = [
        ('PT Alpha Solar Energi', 'PTR-001', 'EPC', 'Jakarta Selatan', 'Terverifikasi', 'green', 4.8, 5, 3, '2024-09-05', False),
        ('PT Beta EPC Indonesia', 'PTR-002', 'EPC', 'Surabaya', 'Terverifikasi', 'green', 4.5, 5, 2, '2024-09-03', False),
        ('PT Gamma Solar', 'PTR-003', 'PV Developer', 'Bandung', 'Menunggu Verifikasi', 'amber', None, 0, 0, '2024-09-08', True),
        ('PT Delta Energi Nusantara', 'PTR-004', 'Vendor', 'Medan', 'Menunggu Verifikasi', 'amber', None, 0, 0, '2024-09-07', True),
        ('PT Epsilon Surya Technik', 'PTR-005', 'EPC', 'Semarang', 'Suspended', 'red', 3.2, 3, 0, '2024-07-15', False),
        ('PT Zeta Renewable', 'PTR-006', 'EPC', 'Bali', 'Terverifikasi', 'green', 4.6, 5, 1, '2024-09-01', False),
    ]
    trs = ''
    for name, pid, cat, loc, status, skind, rating, stars_n, active_n, upd, need_verify in rows_data:
        rating_html = f'<span class="stars">{"★"*stars_n}{"☆"*(5-stars_n)}</span> {rating}' if rating else '-'
        verify_btn = '<button class="btn btn--primary btn--sm">Verifikasi</button>' if need_verify else ''
        trs += f'''<tr>
          <td><div class="strong">{name}</div><div class="sub">{pid}</div></td>
          <td>{badge(cat, 'cyan')}</td>
          <td>{loc}</td>
          <td>{dot_badge(status, skind)}</td>
          <td style="white-space:nowrap">{rating_html}</td>
          <td>{active_n}</td>
          <td>{upd}</td>
          <td><div class="flex gap-8"><a href="#" style="font:600 13px var(--font-head);color:var(--green-700)">Detail</a>{verify_btn}</div></td>
        </tr>'''
    content = f'''      <div class="page-head-row">
        <div><h1 class="h1">Partner Management</h1><p class="sub mt-4">6 mitra terdaftar dalam sistem</p></div>
        <a class="btn btn--primary" href="partner-add.html">{icon('+',13)} Tambah Mitra</a>
      </div>
      <div class="filterbar"><select class="select select--sm"><option>Semua Status</option></select></div>
      <div class="card" style="padding:0">
        <table class="tbl" style="margin:0">
          <thead><tr><th style="padding-left:20px">NAMA MITRA</th><th>KATEGORI</th><th>LOKASI</th><th>STATUS VERIFIKASI</th><th>RATING</th><th>PROJECT AKTIF</th><th>LAST UPDATE</th><th style="padding-right:20px">AKSI</th></tr></thead>
          <tbody>{trs}</tbody>
        </table>
      </div>'''
    write('partners.html', page('admin', 'partners.html', 'Partner Management', 'Partner Management', content))

def build_partner_add():
    identitas_body = f'''
        <div class="field"><label class="field__label">Nama Perusahaan <span class="req">*</span></label><input class="input" value="PT Contoh Energi Nusantara"></div>
        <div class="field"><label class="field__label">NPWP <span class="req">*</span></label><input class="input" placeholder="XX.XXX.XXX.X-XXX.000"></div>
        <div class="field"><label class="field__label">Alamat Lengkap <span class="req">*</span></label><input class="input" placeholder="Jl. Contoh No. 1, Kota"></div>
        <div class="field"><label class="field__label">Website</label><input class="input" placeholder="www.contoh.co.id"></div>
        <div class="row-2">
          <div class="field"><label class="field__label">Tahun Berdiri <span class="req">*</span></label><input class="input" placeholder="2015"></div>
          <div class="field" style="margin-bottom:0"><label class="field__label">Jumlah Karyawan <span class="req">*</span></label><input class="input" placeholder="50"></div>
        </div>'''
    klasifikasi_body = '''
        <div class="field"><label class="field__label">Kategori Mitra <span class="req">*</span></label><select class="select"><option>Pilih kategori...</option></select></div>
        <div class="field"><label class="field__label">Lokasi / Kota <span class="req">*</span></label><input class="input" placeholder="Jakarta Selatan"></div>
        <div class="field"><label class="field__label">Provinsi <span class="req">*</span></label><select class="select"><option>Pilih provinsi...</option></select></div>
        <div class="field" style="margin-bottom:0"><label class="field__label">Deskripsi Singkat</label><textarea class="input" rows="3" placeholder="Deskripsi singkat tentang perusahaan dan layanan utama..."></textarea></div>'''
    profil_tab = f'<div class="grid-2">{card("Identitas Perusahaan", identitas_body)}{card("Klasifikasi", klasifikasi_body)}</div>'

    dok_wajib_body = f'''<div class="grid-2">
        <div><div style="font:600 13px var(--font-head);margin-bottom:10px">Portofolio</div><div class="upload-box">{icon('📄',22)}<div>Upload PDF</div></div></div>
        <div>
          <div style="font:600 13px var(--font-head);margin-bottom:10px">NPWP Perusahaan <span class="req">*</span></div>
          <div class="field"><label class="field__label" style="font-weight:400;color:var(--slate-500)">Nomor NPWP</label><input class="input" placeholder="Nomor NPWP"></div>
          <div class="field"><label class="field__label" style="font-weight:400;color:var(--slate-500)">Masa Berlaku</label><input class="input"></div>
          <div class="upload-box">{icon('📄',22)}<div>Upload PDF</div></div>
        </div>
      </div>'''
    sertifikasi_body = f'''<div style="max-width:500px"><div style="font:600 13px var(--font-head);margin-bottom:10px">Sertifikasi Lainnya</div>
        <div class="field"><input class="input" placeholder="Nama &amp; Nomor"></div>
        <div class="field"><input class="input"></div>
        <div class="upload-box">{icon('📄',22)}<div>Upload Sertifikat</div></div>
      </div>'''
    dokumen_tab = f'''<div class="alert alert--info mt-16" style="margin-bottom:18px">{icon('📎',16)}<span>Upload dokumen legalitas dalam format PDF. Maksimal 10 MB per file.</span></div>
      {card('Dokumen Wajib', dok_wajib_body)}
      {card('Sertifikasi (Opsional)', sertifikasi_body)}'''

    content = f'''      <div class="page-head-row">
        <div>
          <a class="back-link" href="partners.html" style="margin-bottom:8px">{icon('←',13)} Kembali</a>
          <h1 class="h1">Tambah Mitra Baru</h1><p class="sub mt-4">Daftarkan mitra / EPC / PV Developer baru ke sistem</p>
        </div>
        <div class="flex gap-8"><button class="btn btn--outline">Batal</button><button class="btn btn--primary">Simpan &amp; Kirim untuk Verifikasi</button></div>
      </div>
      <div class="tabs" data-tabs="padd">
        <a href="#" class="tab is-active" data-tab="profil">Profil Perusahaan</a>
        <a href="#" class="tab" data-tab="dok">Dokumen</a>
      </div>
      <div data-tab-panel="profil" data-tabs-for="padd">{profil_tab}</div>
      <div data-tab-panel="dok" data-tabs-for="padd" hidden>{dokumen_tab}</div>'''
    write('partner-add.html', page('admin', 'partners.html', 'Partner Management', 'Tambah Mitra Baru', content))

def build_master_data():
    nav_groups = [
        ('DATA REFERENSI', [('Customer Segment', True), ('Project Type', False), ('Region', False), ('Partner Category', False)]),
        ('WORKFLOW', [('Workflow Status', False), ('Project Status', False), ('Survey Status', False), ('Quotation Status', False)]),
        ('DOKUMEN', [('Document Template', False), ('Notification Template', False)]),
        ('HAK AKSES', [('Role', False)]),
    ]
    nav_html = ''
    for label, items in nav_groups:
        nav_html += f'<div class="md-nav__label">{label}</div>'
        for name, active in items:
            nav_html += f'<a href="#" class="{"is-active" if active else ""}">{name}</a>'

    table = f'''<table class="tbl" style="margin:0">
      <thead><tr><th style="padding-left:20px">KODE</th><th>STATUS</th><th>NAMA SEGMENT</th><th>DESKRIPSI</th><th>STATUS</th><th style="padding-right:20px">AKSI</th></tr></thead>
      <tbody>
        <tr><td class="mono" style="padding-left:20px">B2B-SWT</td><td>B2B Swasta</td><td>Pelanggan swasta / korporasi</td><td>{dot_badge('Aktif','green')}</td><td></td><td style="padding-right:20px"><a href="#" style="font:600 13px var(--font-head);color:var(--green-700);margin-right:14px">Edit</a><a href="#" style="font:600 13px var(--font-head);color:var(--slate-500)">Nonaktifkan</a></td></tr>
        <tr><td class="mono" style="padding-left:20px">GOV-BUMN</td><td>Pemerintah/BUMN</td><td>Instansi pemerintah dan BUMN</td><td>{dot_badge('Aktif','green')}</td><td></td><td style="padding-right:20px"><a href="#" style="font:600 13px var(--font-head);color:var(--green-700);margin-right:14px">Edit</a><a href="#" style="font:600 13px var(--font-head);color:var(--slate-500)">Nonaktifkan</a></td></tr>
      </tbody></table>'''

    content = f'''      <div class="page-head"><h1 class="h1">Master Data</h1><p class="sub">Kelola data referensi dan konfigurasi sistem</p></div>
      <div class="md-layout">
        <nav class="md-nav">{nav_html}</nav>
        <div class="card" style="padding:0">
          <div class="flex justify-between items-center" style="padding:20px 20px 0">
            <h3 class="h3">Customer Segment</h3>
            <button class="btn btn--primary btn--sm">{icon('+',12)} Tambah Data</button>
          </div>
          <div class="mt-16">{table}</div>
        </div>
      </div>'''
    write('master-data.html', page('admin', 'master-data.html', 'Master Data', 'Master Data', content))

def build_audit_log():
    rows_data = [
        ('#DCFCE7', '✓', '2024-09-11 09:45:22', 'Mitra Diverifikasi', 'Budi Santoso', 'Partner Management', 'PT Alpha Solar Energi (PTR-001)'),
        ('#DBEAFE', '+', '2024-09-11 09:12:05', 'User Dibuat', 'Budi Santoso', 'User Management', 'Bambang Nugroho (USR-007)'),
        ('#F3E8FF', '↕', '2024-09-10 16:30:44', 'Role User Diubah', 'Fitri Handayani', 'User Management', 'Sari Indah &rarr; Nonaktif (USR-006)'),
        ('#E2E8F0', '⚙', '2024-09-10 14:22:11', 'Master Data Diperbarui', 'Fitri Handayani', 'Master Data', 'Project Type &ndash; PLTS Ground Mounted'),
        ('#DCFCE7', '✓', '2024-09-10 11:05:33', 'Mitra Diverifikasi', 'Budi Santoso', 'Partner Management', 'PT Zeta Renewable (PTR-006)'),
        ('#FFF5F5', '✕', '2024-09-09 15:44:18', 'User Dinonaktifkan', 'Budi Santoso', 'User Management', 'Sari Indah (USR-006)'),
        ('#FEF3C7', '🔒', '2024-09-09 10:02:57', 'Data Permission Diperbarui', 'Fitri Handayani', 'Master Data', 'Role ICONGreen &ndash; Akses Billing'),
        ('#CFFAFE', '🏢', '2024-09-08 14:30:00', 'Mitra Didaftarkan', 'Budi Santoso', 'Partner Management', 'PT Gamma Solar (PTR-003)'),
    ]
    trs = ''
    for bg, ic, waktu, act, user, modul, obj in rows_data:
        trs += f'''<tr>
          <td class="mono" style="padding-left:20px;color:var(--slate-400);font-weight:400">{waktu}</td>
          <td><div class="flex items-center gap-12"><span class="audit-ico" style="background:{bg}">{icon(ic,13)}</span><span class="strong">{act}</span></div></td>
          <td>{user}</td>
          <td>{badge('Admin ICON','purple')}</td>
          <td>{modul}</td>
          <td style="padding-right:20px">{obj}</td>
        </tr>'''
    content = f'''      <div class="page-head"><h1 class="h1">Audit Log</h1><p class="sub">Riwayat seluruh aktivitas administrasi sistem &middot; Read-only</p></div>
      <div class="alert alert--warn mt-24" style="margin-bottom:18px">{icon('ℹ️',16)}<span>Audit Log bersifat <strong>read-only</strong>. Data tidak dapat diubah atau dihapus.</span></div>
      <div class="filterbar">
        <div class="search" style="flex:1;max-width:none">{icon('🔍',15)}<input class="input" placeholder="Cari user, aktivitas, atau objek..."></div>
        <select class="select select--sm"><option>Semua Modul</option></select>
        <input class="input" style="width:150px" type="text" placeholder="">
      </div>
      <div class="card" style="padding:0">
        <table class="tbl" style="margin:0">
          <thead><tr><th style="padding-left:20px">WAKTU</th><th>AKTIVITAS</th><th>USER</th><th>ROLE</th><th>MODUL</th><th style="padding-right:20px">OBJECT</th></tr></thead>
          <tbody>{trs}</tbody>
        </table>
        <div class="flex justify-between items-center" style="padding:16px 20px">
          <span class="sub">Menampilkan 8 dari 8 entri</span>
          <div class="flex gap-8"><button class="btn btn--outline btn--sm">&larr; Prev</button><button class="btn btn--outline btn--sm">Next &rarr;</button></div>
        </div>
      </div>'''
    write('audit-log.html', page('admin', 'audit-log.html', 'Audit Log', 'Audit Log', content))

if __name__ == '__main__':
    build_dashboard()
    build_users()
    build_user_detail()
    build_partners()
    build_partner_add()
    build_master_data()
    build_audit_log()
