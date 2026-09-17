"""ICONGreen (Ops) portal pages."""
from gen import OUT, page, kpi, card, badge, icon, kv

def write(path, html):
    p = OUT / 'ops' / path
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(html, encoding='utf-8')
    print('wrote ops/' + path)

def dot_badge(text, kind):
    return f'<span class="badge badge--{kind}"><span class="dot"></span>{text}</span>'

def chip(num, label, kind, active=False):
    return f'<div class="chip chip--{kind}{" is-active" if active else ""}"><span class="num">{num}</span><span>{label}</span></div>'

def stepper(steps, current_idx):
    # steps: list of labels; current_idx 0-based index of current (in-progress) step
    out = '<div class="stepper">'
    for i, label in enumerate(steps):
        if i < current_idx:
            cls, num = 'is-done', '✓'
        elif i == current_idx:
            cls, num = 'is-current', str(i+1)
        else:
            cls, num = '', str(i+1)
        line = ''
        if i > 0:
            line_cls = ' is-done' if i <= current_idx else ''
            line = f'<div class="stepper__line{line_cls}"></div>'
        out += f'{line}<div class="stepper__step {cls}"><div class="stepper__num">{num}</div><div class="stepper__label">{label}</div></div>'
    out += '</div>'
    return out

def pbar_labeled(actual, planned, delta_txt, color):
    return f'''<div class="flex justify-between items-center" style="margin-bottom:6px">
      <span class="sub">Actual <b style="color:var(--slate-900);font-weight:700">{actual}%</b> &middot; Planned <b style="color:var(--slate-900);font-weight:700">{planned}%</b></span>
      <span style="font:700 13px var(--font-head);color:{color}">{delta_txt}</span>
    </div><div class="pbar"><span style="width:{actual}%;background:{color}"></span></div>'''

# ------------------------------------------------------------ Dashboard
def build_dashboard():
    kpis = f'''<div class="kpi-row" style="grid-auto-columns:1fr">
      {kpi('Active Work Order', '7', 'green', '📋')}
      {kpi('Need Action', '3', 'amber', '⚠')}
      {kpi('Active Project', '3', 'blue', '🏗')}
      {kpi('Delayed Project', '0', 'red', '⏰')}
      {kpi('Pending Survey', '2', 'purple', '📍')}
      {kpi('Pending Quotation', '2', 'cyan', '💼')}
    </div>'''
    rows = [
        ('WO-2024-0047', 'PT Indofood CBP Sukses Makmur', 'Survey', 'blue', 'Jadwal survey belum dikonfirmasi oleh Mitra', '2024-09-20'),
        ('WO-2024-0044', 'PLN Persero UP3 Bandung', 'Partner Selection', 'blue', 'Mitra belum dipilih, batas waktu terlewat 3 hari', '2024-09-15'),
        ('WO-2024-0040', 'PT Gudang Garam', 'WO Received', 'blue', 'Belum ada tindakan sejak WO diterima 2 hari lalu', '2024-09-30'),
    ]
    trs = ''
    for wo, cust, stage, skind, isu, due in rows:
        trs += f'''<tr>
          <td class="mono strong" style="padding-left:20px">{wo}</td>
          <td>{cust}</td>
          <td>{badge(stage, skind)}</td>
          <td style="color:var(--amber-600)">{isu}</td>
          <td style="color:{'var(--red-600)' if wo=='WO-2024-0044' else 'var(--slate-700)'}">{due}</td>
          <td style="padding-right:20px"><button class="btn btn--primary btn--sm">Tindak Lanjut</button></td>
        </tr>'''
    wo_table = f'''<table class="tbl" style="margin:0">
      <thead><tr><th style="padding-left:20px">WO</th><th>CUSTOMER</th><th>STAGE</th><th>ISU</th><th>DUE DATE</th><th style="padding-right:20px">AKSI</th></tr></thead>
      <tbody>{trs}</tbody></table>'''
    wo_card = card('Work Order Perlu Tindakan', wo_table, '<a href="work-orders.html" class="link">Lihat Semua &rarr;</a>')

    activity = [
        ('#DCFCE7', '✓', 'Memverifikasi Mitra PT Alpha Solar Energi', 'Admin Budi &middot; Hari ini, 09:45'),
        ('#DBEAFE', '+', 'Membuat user baru: Bambang Nugroho (Mitra)', 'Admin Budi &middot; Hari ini, 09:12'),
        ('#F3E8FF', '📍', 'WO-2024-0047 &ndash; Mengajukan jadwal survey ke Alpha Solar', 'Rina Kusumawati &middot; Hari ini, 08:55'),
        ('#FFF5F5', '✕', 'Menonaktifkan user Sari Indah', 'Admin Fitri &middot; Kemarin, 16:30'),
        ('#FEF3C7', '↑', 'WO-2024-0046 &ndash; Progress proyek RSUD diperbarui: 42%', 'Agus Pratama &middot; Kemarin, 15:44'),
    ]
    items = ''.join(f'''<div class="timeline__item"><div class="timeline__dot" style="background:{bg}">{icon(ic,13)}</div>
      <div class="timeline__body"><div class="t">{t}</div><div class="d">{d}</div></div></div>''' for bg, ic, t, d in activity)
    activity_card = card('Recent Activity', f'<div class="mt-16">{items}</div>')

    content = f'''      <div class="page-head-row"><div><h1 class="h1">Dashboard ICONGreen</h1><p class="sub mt-4">Gambaran kondisi operasional Work Order dan proyek PLTS &middot; 11 Sep 2024</p></div>
        <button class="btn btn--primary">{icon('🔄',13)} Sync Data</button></div>
      {kpis}
      <div class="grid-2 mt-24" style="grid-template-columns:1.6fr 1fr">{wo_card}{activity_card}</div>'''
    write('dashboard.html', page('ops', 'dashboard.html', 'Dashboard', 'Dashboard ICONGreen', content))

def build_executive_dashboard():
    def bars(vals, color='var(--brand)'):
        mx = max(vals)
        cols = ''.join(f'<div class="col"><div class="bar" style="height:{v/mx*100:.0f}%;background:{color}"></div><div class="lbl">{l}</div></div>' for v, l in zip(vals, ['Jan','Feb','Mar','Apr','Mei','Jun','Jul','Agt','Sep']))
        return f'<div class="barchart">{cols}</div>'

    kap_vals = [95, 130, 88, 175, 150, 205, 165, 230, 190]
    nilai_vals = [720, 900, 650, 1150, 980, 1400, 1080, 1550, 1250]

    kpis = f'''<div class="kpi-row">
      {kpi('Total Kapasitas Terpasang', '27.4 MWp', 'green', '⚡', '&uarr; 18% dari bulan lalu', 'pos')}
      {kpi('Total Nilai Project', 'Rp 198.6 M', 'blue', '💰', 'YTD 2024')}
      {kpi('Active Projects', '3', 'cyan', '🏗', 'Sedang berjalan')}
      {kpi('Completed Projects', '1', 'purple', '✅', 'Selesai 2024')}
    </div>'''
    charts = f'''<div class="grid-2 mt-24">
      {card('Kapasitas Terpasang per Bulan (kWp)', bars(kap_vals))}
      {card('Nilai Proyek per Bulan (Miliar Rp)', bars(nilai_vals))}
    </div>'''

    pipeline_rows = [
        ('WO-2024-0047', 'PT Indofood CBP', '500 kWp', 'Survey', 'Need Attention', 'amber', 'Rp 3.2 M'),
        ('WO-2024-0045', 'PT Astra International', '1.2 MWp', 'Quotation', 'On Track', 'green', 'Rp 7.2 M'),
        ('WO-2024-0044', 'PLN Persero Bandung', '750 kWp', 'Partner Selection', 'Overdue', 'red', 'Rp 5.1 M'),
    ]
    ptr = ''.join(f'''<tr><td class="mono strong" style="padding-left:20px">{wo}</td><td>{cust}</td><td>{cap}</td><td>{badge(stage,'cyan')}</td><td>{dot_badge(status,skind)}</td><td style="padding-right:20px">{val}</td></tr>''' for wo, cust, cap, stage, status, skind, val in pipeline_rows)
    pipeline = card('Project Pipeline', f'''<table class="tbl" style="margin:0"><thead><tr><th style="padding-left:20px">WO</th><th>CUSTOMER</th><th>KAPASITAS</th><th>STAGE</th><th>STATUS</th><th style="padding-right:20px">EST. VALUE</th></tr></thead><tbody>{ptr}</tbody></table>''')

    bar_b2b = '<div class="pbar"><span style="width:62%;background:#2563EB"></span></div>'
    bar_gov = '<div class="pbar"><span style="width:38%;background:#7C3AED"></span></div>'
    dist = f'''<div style="margin-bottom:18px"><div class="flex justify-between" style="margin-bottom:6px"><span style="font:600 13px var(--font-head)">B2B Swasta</span><span class="sub">5 (62%)</span></div>{bar_b2b}</div>
      <div style="margin-bottom:20px"><div class="flex justify-between" style="margin-bottom:6px"><span style="font:600 13px var(--font-head)">Pemerintah/BUMN</span><span class="sub">3 (38%)</span></div>{bar_gov}</div>
      <div class="muted" style="font:700 11px var(--font-head);letter-spacing:.4px;text-transform:uppercase;border-top:1px solid var(--slate-200);padding-top:14px;margin-bottom:10px">By Tipe</div>
      <div class="flex-col gap-8" style="font:400 13px var(--font-body)">
        <div class="flex justify-between"><span>&#9679; PLTS Atap Industri</span><span class="strong">45%</span></div>
        <div class="flex justify-between"><span>&#9679; PLTS Atap Pemerintah</span><span class="strong">25%</span></div>
        <div class="flex justify-between"><span>&#9679; PLTS Ground Mounted</span><span class="strong">18%</span></div>
        <div class="flex justify-between"><span>&#9679; PLTS Komunal</span><span class="strong">12%</span></div>
      </div>'''
    right = card('Distribusi Project', dist)

    content = f'''      <div class="page-head"><h1 class="h1">Executive Dashboard</h1><p class="sub">Performa bisnis PV Solution &middot; September 2024</p></div>
      {kpis}{charts}
      <div class="grid-2 mt-24" style="grid-template-columns:1.6fr 1fr">{pipeline}{right}</div>'''
    write('executive-dashboard.html', page('ops', 'executive-dashboard.html', 'Executive Dashboard', 'Executive Dashboard', content))

def build_work_orders():
    rows = [
        ('WO-2024-0047', 'PT Indofood CBP Sukses Makmur', 'Bpk. Rudi Hermawan', 'Cikampek, Jawa Barat', '500 kWp', 'Survey', 'Alpha Solar Energi', '2024-09-20', 'Need Attention', 'amber'),
        ('WO-2024-0046', 'RSUD Dr. Soetomo', 'Ibu Retno Wulandari', 'Surabaya, Jawa Timur', '200 kWp', 'Project', 'Beta EPC Indonesia', '2024-12-15', 'On Track', 'green'),
        ('WO-2024-0045', 'PT Astra International', 'Bpk. Denny Sutrisno', 'Karawang, Jawa Barat', '1.2 MWp', 'Quotation', 'Alpha Solar Energi', '2024-09-25', 'On Track', 'green'),
        ('WO-2024-0044', 'PLN Persero UP3 Bandung', 'Bpk. Ahmad Fauzi', 'Bandung, Jawa Barat', '750 kWp', 'Partner Selection', '-', '2024-09-15', 'Overdue', 'red'),
        ('WO-2024-0043', 'PT Bank Mandiri (Persero)', 'Ibu Sri Wahyuni', 'Jakarta Pusat', '300 kWp', 'BAST', 'Zeta Renewable', '2024-09-10', 'On Track', 'green'),
        ('WO-2024-0042', 'PT Sinarmas Land', 'Bpk. Tonny Tanaka', 'Tangerang Selatan, Banten', '800 kWp', 'Billing', 'Alpha Solar Energi', '2024-08-30', 'Completed', 'slate'),
        ('WO-2024-0041', 'Universitas Indonesia', 'Bpk. Prof. Darmawan', 'Depok, Jawa Barat', '400 kWp', 'Survey', 'Beta EPC Indonesia', '2024-09-18', 'On Track', 'green'),
        ('WO-2024-0040', 'PT Gudang Garam', '-', 'Kediri, Jawa Timur', '2 MWp', 'WO Received', '-', '2024-09-30', 'On Track', 'green'),
    ]
    trs = ''
    for wo, cust, pic, loc, cap, stage, mitra, due, status, skind in rows:
        due_style = 'color:var(--red-600);font-weight:600' if status == 'Overdue' else ''
        href = 'wo-detail.html' if wo == 'WO-2024-0044' else '#'
        trs += f'''<tr>
          <td class="mono strong" style="padding-left:20px">{wo}</td>
          <td><div class="strong">{cust}</div><div class="sub">{pic}</div></td>
          <td>{loc}</td>
          <td>{cap}</td>
          <td>{badge(stage,'cyan')}</td>
          <td>{mitra}</td>
          <td style="{due_style}">{due}</td>
          <td>{dot_badge(status, skind)}</td>
          <td style="padding-right:20px"><a href="{href}" style="font:600 13px var(--font-head);color:var(--green-700)">Detail &rarr;</a></td>
        </tr>'''
    content = f'''      <div class="page-head-row"><div><h1 class="h1">Work Order</h1><p class="sub mt-4">8 WO terdaftar</p></div>
        <button class="btn btn--primary">{icon('🔄',13)} Sync Data P4B</button></div>
      <div class="filterbar"><div class="search">{icon('🔍',15)}<input class="input" placeholder="Cari WO atau customer..."></div><select class="select select--sm"><option>Semua Status</option></select></div>
      <div class="chip-row">
        {chip(4,'On Track','green')}{chip(2,'Need Attention','amber')}{chip(1,'Overdue','red')}{chip(1,'Completed','slate')}
      </div>
      <div class="card" style="padding:0"><table class="tbl" style="margin:0">
        <thead><tr><th style="padding-left:20px">NO. WO</th><th>CUSTOMER</th><th>LOKASI</th><th>KAPASITAS</th><th>STAGE</th><th>MITRA</th><th>DUE DATE</th><th>STATUS</th><th style="padding-right:20px">AKSI</th></tr></thead>
        <tbody>{trs}</tbody></table></div>'''
    write('work-orders.html', page('ops', 'work-orders.html', 'Work Order', 'Work Order', content))

def build_wo_detail():
    stage_steps = ['WO Received', 'Partner Selection', 'Survey', 'Quotation', 'Project', 'BAST', 'Billing']
    st = stepper(stage_steps, 1)
    banner = f'''<div class="stage-banner">
      <div><div class="label">Current Stage</div><div class="val">Partner Selection</div></div>
      <div><div class="label">Tindakan Saat Ini</div><div class="sub2">Memilih mitra secara langsung (direct assignment).</div></div>
      <div><div class="label">Penanggung Jawab</div><div class="val" style="font-size:14px">ICONGreen</div></div>
      <div><div class="label">Next Action</div><div class="sub2">Konfirmasi penunjukan mitra</div><div class="due">Due: 2024-09-15</div></div>
    </div>'''
    tabs = ['Overview','Partner','Survey','Quotation','Project','Dokumen','Billing','Aktivitas']
    tab_html = ''.join(f'<a href="#" class="tab{" is-active" if i==0 else ""}" data-tab="t{i}">{t}</a>' for i, t in enumerate(tabs))

    overview_left = card(None, f'''<div class="muted" style="font:700 11px var(--font-head);letter-spacing:.4px;text-transform:uppercase;margin-bottom:16px">Informasi Work Order</div>
      <div class="kv-grid">
        {kv('WO ID','WO-2024-0044')}{kv('Customer','PLN Persero UP3 Bandung')}
        {kv('Segment','Pemerintah/BUMN')}{kv('Lokasi','Bandung, Jawa Barat')}
        {kv('Kapasitas','750 kWp')}{kv('Tipe Proyek','PLTS Atap BUMN')}
        {kv('Contact Person','Bpk. Ahmad Fauzi')}{kv('Tanggal Masuk','2024-07-20')}
      </div>''')
    overview_right = card(None, f'''<div class="muted" style="font:700 11px var(--font-head);letter-spacing:.4px;text-transform:uppercase;margin-bottom:16px">Status &amp; Mitra</div>
      <div class="kv-grid" style="grid-template-columns:1fr">
        {kv('Status WO', dot_badge('Overdue','red'))}
        {kv('Mitra Terpilih','-')}
        {kv('Segmen Customer', badge('Pemerintah/BUMN','purple'))}
      </div>
      <div class="alert alert--warn mt-16">{icon('⚠',15)}<span><strong>Perlu Tindakan</strong><br>Mitra belum dipilih, batas waktu terlewat 3 hari</span></div>''')

    other_tabs = ''
    for i, t in enumerate(tabs[1:], start=1):
        placeholder = f'<p class="sub">Detail {t.lower()} untuk WO-2024-0044 akan tampil di sini.</p>'
        other_tabs += f'<div data-tab-panel="t{i}" data-tabs-for="wo" hidden>{card(t, placeholder)}</div>'

    content = f'''      <a class="back-link" href="work-orders.html">{icon('←',13)} Kembali</a>
      <div class="page-head-row"><div><h1 class="h1">WO-2024-0044</h1><p class="sub mt-4">PLN Persero UP3 Bandung &middot; Bandung, Jawa Barat &middot; 750 kWp</p></div>
        <div class="flex gap-8 items-center">{dot_badge('Overdue','red')}<button class="btn btn--primary">Assign Mitra</button></div></div>
      {st}
      {banner}
      <div class="tabs" data-tabs="wo">{tab_html}</div>
      <div data-tab-panel="t0" data-tabs-for="wo"><div class="grid-2">{overview_left}{overview_right}</div></div>
      {other_tabs}'''
    write('wo-detail.html', page('ops', 'work-orders.html', 'Work Order', 'WO-2024-0044', content))

def build_surveys():
    rows = [
        ('SVY-2024-034', 'WO-2024-044', 'PLN Persero UP3 Bandung', 'PT Alpha Solar Energi', 'Bandung, Jawa Barat', '&mdash;', 'Requested', 'blue'),
        ('SVY-2024-033', 'WO-2024-048', 'PT Holcim Indonesia', 'PT Delta Surya Power', 'Bogor, Jawa Barat', 'Mitra &middot; 2024-09-16', 'Mitra Proposed', 'amber'),
        ('SVY-2024-031', 'WO-2024-047', 'PT Indofood CBP Sukses Makmur', 'PT Alpha Solar Energi', 'Cikampek, Jawa Barat', 'ICONGreen &middot; 2024-09-20', 'ICONGreen Counter', 'purple'),
        ('SVY-2024-029', 'WO-2024-041', 'Universitas Indonesia', 'PT Beta EPC Indonesia', 'Depok, Jawa Barat', 'ICONGreen &middot; 2024-09-22', 'Confirmed', 'green'),
        ('SVY-2024-030', 'WO-2024-046', 'RSUD Dr. Soetomo', 'PT Beta EPC Indonesia', 'Surabaya, Jawa Timur', 'Mitra &middot; 2024-08-28', 'Completed', 'slate'),
    ]
    trs = ''
    for sid, wo, cust, mitra, loc, usulan, status, skind in rows:
        href = 'survey-detail.html' if sid == 'SVY-2024-033' else '#'
        action = f'<a href="{href}" style="font:600 13px var(--font-head);color:var(--amber-600)">Tinjau &rarr;</a>' if skind == 'amber' else f'<a href="{href}" style="font:600 13px var(--font-head);color:var(--green-700)">Detail</a>'
        trs += f'''<tr><td class="mono strong" style="padding-left:20px">{sid}</td><td>{wo}</td><td>{cust}</td><td>{mitra}</td><td>{loc}</td><td>{usulan}</td><td>{dot_badge(status,skind)}</td><td style="padding-right:20px">{action}</td></tr>'''
    banner = f'''<div class="alert alert--warn mt-24" style="margin-bottom:18px;justify-content:space-between;align-items:center;display:flex">
      <div class="flex items-center gap-8">{icon('📬',16)}<strong>1 Usulan Tanggal dari Mitra Menunggu Konfirmasi Anda</strong></div>
    </div>
    <div class="card" style="background:#FFFBEB;border-color:#FDE68A;margin-bottom:20px">
      <div class="flex justify-between items-center">
        <div><span class="mono strong" style="color:var(--amber-600)">SVY-2024-0033</span> <strong>PT Holcim Indonesia</strong> &rarr; <span class="sub">2024-09-16 &middot; 09:00 WIB</span></div>
        <a href="survey-detail.html" class="btn btn--primary btn--sm">Tinjau &rarr;</a>
      </div>
    </div>'''
    content = f'''      <div class="page-head"><h1 class="h1">Survey</h1><p class="sub">5 survey terdaftar</p></div>
      {banner}
      <div class="filterbar"><select class="select select--sm"><option>Semua Status</option></select></div>
      <div class="card" style="padding:0"><table class="tbl" style="margin:0">
        <thead><tr><th style="padding-left:20px">ID SURVEY</th><th>WO</th><th>CUSTOMER</th><th>MITRA</th><th>LOKASI</th><th>USULAN TERAKHIR</th><th>STATUS</th><th style="padding-right:20px">AKSI</th></tr></thead>
        <tbody>{trs}</tbody></table></div>'''
    write('surveys.html', page('ops', 'surveys.html', 'Survey', 'Survey', content))

def build_survey_detail():
    steps = ['Requested', 'Mitra Proposed', 'ICONGreen Counter', 'Confirmed', 'Scheduled', 'Completed']
    st = stepper(steps, 1)
    left = card('Riwayat Negosiasi Tanggal', f'''
      <div style="background:#FFFBEB;border:1px solid #FDE68A;border-radius:10px;padding:16px">
        <div class="flex justify-between items-center" style="margin-bottom:8px">
          <div class="flex items-center gap-8"><span class="avatar-sm" style="background:var(--amber-600)">M</span><strong>Mitra</strong></div>
          <div class="flex items-center gap-8"><span class="sub">2024-09-12</span>{badge('Menunggu respons','amber')}</div>
        </div>
        <div style="font:600 13px var(--font-head);margin-bottom:4px">{icon('📅',14)} 2024-09-16 &middot; {icon('⏰',14)} 09:00 WIB</div>
        <div class="sub">Tim kami siap pada tanggal ini.</div>
      </div>''')
    right = card('Detail Survey', f'''<div class="kv-grid" style="grid-template-columns:1fr">
      {kv('WO','WO-2024-0048')}{kv('Customer','PT Holcim Indonesia')}{kv('Mitra','PT Delta Surya Power')}
      {kv('Lokasi','Bogor, Jawa Barat')}{kv('Deadline','2024-09-20')}{kv('Confirmed Date','-')}
    </div>''')
    content = f'''      <a class="back-link" href="surveys.html">{icon('←',13)} Kembali</a>
      <div class="page-head-row"><div><h1 class="h1">SVY-2024-0033</h1><p class="sub mt-4">PT Holcim Indonesia &middot; PT Delta Surya Power &middot; Bogor, Jawa Barat</p></div>
        <div class="flex gap-8 items-center">{dot_badge('Mitra Proposed','amber')}<button class="btn btn--primary">{icon('✓',13)} Konfirmasi Tanggal</button><button class="btn btn--outline">{icon('↩',13)} Ajukan Tanggal Lain</button></div></div>
      {st}
      <div class="alert alert--warn mt-24" style="margin-bottom:20px">{icon('📧',16)}<span><strong>Mitra mengusulkan tanggal survey</strong><br>Usulan: <strong>2024-09-16 pukul 09:00 WIB</strong> &middot; Konfirmasi atau ajukan tanggal lain.</span></div>
      <div class="grid-2">{left}{right}</div>'''
    write('survey-detail.html', page('ops', 'surveys.html', 'Survey', 'SVY-2024-0033', content))

def build_quotations():
    rows = [
        ('QUO-2024-0028', 'WO-2024-0045', 'PT Astra International', 'Alpha Solar Energi', 'Rp 7.20 M', '2024-09-05', 'Under Review', 'amber'),
        ('QUO-2024-0027', 'WO-2024-0045', 'PT Astra International', 'Beta EPC Indonesia', 'Rp 7.68 M', '2024-09-06', 'Under Review', 'amber'),
        ('QUO-2024-0026', 'WO-2024-0046', 'RSUD Dr. Soetomo', 'Beta EPC Indonesia', 'Rp 1.35 M', '2024-09-01', 'Accepted', 'green'),
    ]
    trs = ''
    for qid, wo, cust, mitra, val, tgl, status, skind in rows:
        href = 'quotation-detail.html' if qid == 'QUO-2024-0028' else '#'
        trs += f'''<tr><td class="mono strong" style="padding-left:20px">{qid}</td><td class="mono">{wo}</td><td>{cust}</td><td>{mitra}</td><td class="mono" style="color:var(--green-700);font-weight:600">{val}</td><td>{tgl}</td><td>{dot_badge(status,skind)}</td><td style="padding-right:20px"><a href="{href}" style="font:600 13px var(--font-head);color:var(--green-700)">Detail</a></td></tr>'''
    content = f'''      <div class="page-head"><h1 class="h1">Quotation</h1><p class="sub">3 quotation terdaftar</p></div>
      <div class="filterbar"><select class="select select--sm"><option>Semua Status</option></select></div>
      <div class="card" style="padding:0"><table class="tbl" style="margin:0">
        <thead><tr><th style="padding-left:20px">ID</th><th>WO</th><th>CUSTOMER</th><th>MITRA</th><th>NILAI PENAWARAN</th><th>TGL SUBMIT</th><th>STATUS</th><th style="padding-right:20px">AKSI</th></tr></thead>
        <tbody>{trs}</tbody></table></div>'''
    write('quotations.html', page('ops', 'quotations.html', 'Quotation', 'Quotation', content))

def build_quotation_detail():
    left = card('Detail Penawaran', f'''<div class="kv-grid" style="grid-template-columns:1fr">
      {kv('Quotation ID','QUO-2024-0028')}{kv('WO','WO-2024-0045')}{kv('Customer','PT Astra International')}
      {kv('Mitra','PT Alpha Solar Energi')}{kv('Kapasitas','1.2 MWp')}{kv('Nilai Penawaran', '<span style="color:var(--green-600)">Rp 7.20 Miliar</span>')}
      {kv('Harga per Wp','Rp 6.000/Wp')}{kv('Durasi Proyek','120 hari')}{kv('Validity','30 hari')}{kv('Tanggal Submit','2024-09-05')}
    </div>''')
    right = card(None, f'''<div class="muted" style="font:700 11px var(--font-head);letter-spacing:.4px;text-transform:uppercase;margin-bottom:16px">Technical Proposal</div>
      <div class="kv-grid" style="grid-template-columns:1fr;margin-bottom:20px">
        {kv('Panel Solar','Tier 1 Monocrystalline 550Wp &ndash; 2.182 pcs')}
        {kv('Inverter','String Inverter 100kW &ndash; 5 unit')}
        {kv('Mounting System','Ground mounting galvanized steel')}
        {kv('Kabel','Solar PV Cable 6mm&sup2; &amp; 16mm&sup2;')}
        {kv('Proteksi','MCB, RCCB, Surge Arrester')}
      </div>
      <div class="muted" style="font:700 11px var(--font-head);letter-spacing:.4px;text-transform:uppercase;margin-bottom:12px;border-top:1px solid var(--slate-200);padding-top:16px">BOQ Ringkasan</div>
      <div class="flex-col" style="font:400 13px var(--font-body)">
        <div class="flex justify-between" style="padding:6px 0"><span>Material</span><span class="mono">Rp 4.320.000.000</span></div>
        <div class="flex justify-between" style="padding:6px 0"><span>Jasa Instalasi</span><span class="mono">Rp 1.800.000.000</span></div>
        <div class="flex justify-between" style="padding:6px 0"><span>Engineering</span><span class="mono">Rp 720.000.000</span></div>
        <div class="flex justify-between" style="padding:6px 0"><span>Commissioning</span><span class="mono">Rp 360.000.000</span></div>
        <div class="flex justify-between" style="padding:10px 0 0;border-top:1px solid var(--slate-200);margin-top:6px"><strong>Total</strong><strong class="mono" style="color:var(--green-600)">Rp 7.20 M</strong></div>
      </div>''')
    content = f'''      <a class="back-link" href="quotations.html">{icon('←',13)} Kembali</a>
      <div class="page-head-row"><div><h1 class="h1">QUO-2024-0028</h1><p class="sub mt-4">PT Astra International &middot; PT Alpha Solar Energi</p></div>
        <div class="flex gap-8 items-center">{dot_badge('Under Review','amber')}<button class="btn btn--soft-red">Tolak</button><button class="btn" style="background:var(--amber-100);color:#B45309">Minta Revisi</button><button class="btn btn--primary">Setujui</button></div></div>
      <div class="grid-2">{left}{right}</div>'''
    write('quotation-detail.html', page('ops', 'quotations.html', 'Quotation', 'QUO-2024-0028', content))

def build_projects():
    rows = [
        ('PRJ-2024-0019', 'RSUD Dr. Soetomo', 'Beta EPC Indonesia', '200 kWp', 42, 48, -6, 'Procurement', 'At Risk', 'amber', 'red'),
        ('PRJ-2024-0018', 'PT Bank Mandiri (Persero)', 'Zeta Renewable', '300 kWp', 91, 88, 3, 'BAST', 'On Track', 'green', 'green'),
        ('PRJ-2024-0017', 'PT Sinarmas Land', 'Alpha Solar Energi', '800 kWp', 100, 100, 0, 'BAST', 'Completed', 'slate', 'green'),
        ('PRJ-2024-0016', 'Universitas Indonesia', 'Beta EPC Indonesia', '400 kWp', 8, 5, 3, 'Engineering', 'On Track', 'green', 'green'),
    ]
    trs = ''
    for pid, cust, mitra, cap, actual, planned, delta, phase, status, skind, barcolor in rows:
        href = 'project-detail.html' if pid == 'PRJ-2024-0019' else '#'
        color = 'var(--red-600)' if delta < 0 else 'var(--green-600)'
        delta_txt = f'{"+" if delta>=0 else ""}{delta}%'
        prog = f'''<div style="min-width:220px"><div class="flex justify-between" style="font-size:12px;margin-bottom:4px"><span>Actual <b>{actual}%</b> &middot; Planned <b>{planned}%</b></span><span style="color:{color};font-weight:700">{delta_txt}</span></div><div class="pbar"><span style="width:{actual}%;background:{'var(--red-600)' if delta<0 else 'var(--green-600)'}"></span></div></div>'''
        trs += f'''<tr><td class="mono strong" style="padding-left:20px">{pid}</td><td>{cust}</td><td>{mitra}</td><td>{cap}</td><td>{prog}</td><td>{badge(phase,'cyan')}</td><td>{dot_badge(status,skind)}</td><td style="padding-right:20px"><a href="{href}" style="font:600 13px var(--font-head);color:var(--green-700)">Detail</a></td></tr>'''
    content = f'''      <div class="page-head"><h1 class="h1">Projects</h1><p class="sub">4 proyek terdaftar</p></div>
      <div class="filterbar"><select class="select select--sm"><option>Semua Status</option></select></div>
      <div class="card" style="padding:0"><table class="tbl" style="margin:0">
        <thead><tr><th style="padding-left:20px">PROJECT ID</th><th>CUSTOMER</th><th>MITRA</th><th>KAPASITAS</th><th>PROGRESS VS PLAN</th><th>PHASE</th><th>STATUS</th><th style="padding-right:20px">AKSI</th></tr></thead>
        <tbody>{trs}</tbody></table></div>'''
    write('projects.html', page('ops', 'projects.html', 'Projects', 'Projects', content))

def build_project_detail():
    tabs = ['Overview','Progress','S-Curve','Dokumen','Issues','Aktivitas']
    tab_html = ''.join(f'<a href="#" class="tab{" is-active" if i==0 else ""}" data-tab="t{i}">{t}</a>' for i, t in enumerate(tabs))
    overview = card('Project Overview', f'''
      <div style="margin-bottom:16px">{dot_badge('At Risk','amber')}</div>
      {pbar_labeled(42, 48, '-6%', 'var(--red-600)')}
      <div class="kv-grid mt-24">
        {kv('Project ID','PRJ-2024-0019')}{kv('WO','WO-2024-0046')}
        {kv('Customer','RSUD Dr. Soetomo')}{kv('Mitra','PT Beta EPC Indonesia')}
        {kv('Kapasitas','200 kWp')}{kv('Phase','Procurement')}
        {kv('Start Date','2024-09-10')}{kv('End Date','2024-12-08')}
      </div>''')
    right = f'''{card(None, f'<div class="sub">Nilai Kontrak</div><div style="font:700 26px var(--font-head);color:var(--green-600);margin-top:4px">Rp 1.35 M</div>')}
      {card(None, f'{icon("⚠",15)} <strong style="color:#B45309">Status Proyek</strong><p class="mt-8" style="font-size:13px;color:#92400E">Actual Progress <b>42%</b>, Planned <b>48%</b>. Variance <b>-6%</b>. Monitor progress lebih ketat.</p>')}'''
    other_tabs = ''
    for i, t in enumerate(tabs[1:], start=1):
        placeholder = f'<p class="sub">Detail {t.lower()} untuk PRJ-2024-0019 akan tampil di sini.</p>'
        other_tabs += f'<div data-tab-panel="t{i}" data-tabs-for="prj" hidden>{card(t, placeholder)}</div>'
    content = f'''      <a class="back-link" href="projects.html">{icon('←',13)} Kembali</a>
      <div class="page-head-row"><div><h1 class="h1">PRJ-2024-0019</h1><p class="sub mt-4">RSUD Dr. Soetomo &middot; PT Beta EPC Indonesia &middot; 200 kWp</p></div>{dot_badge('At Risk','amber')}</div>
      <div class="tabs mt-24" data-tabs="prj">{tab_html}</div>
      <div data-tab-panel="t0" data-tabs-for="prj"><div class="grid-2" style="grid-template-columns:1.6fr 1fr">{overview}<div class="flex-col gap-12">{right}</div></div></div>
      {other_tabs}'''
    write('project-detail.html', page('ops', 'projects.html', 'Projects', 'PRJ-2024-0019', content))

def build_partners():
    partners = [
        ('Alpha Solar Energi', 'Jakarta Selatan', 4.8, 18, 3, '12.4 MWp'),
        ('Beta EPC Indonesia', 'Surabaya', 4.5, 12, 2, '8.2 MWp'),
        ('Zeta Renewable', 'Bali', 4.6, 9, 1, '5.8 MWp'),
    ]
    cards = ''
    for i, (name, loc, rating, selesai, aktif, kap) in enumerate(partners):
        href = 'partner-detail.html' if i == 0 else '#'
        cards += f'''<a href="{href}" class="card" style="display:block">
          <div class="flex items-center gap-12" style="margin-bottom:14px">
            <span style="width:44px;height:44px;border-radius:10px;background:var(--green-100);display:flex;align-items:center;justify-content:center;font-size:20px">🏢</span>
            <div><div style="font:700 15px var(--font-head);color:var(--slate-900)">{name}</div><div class="sub">{loc}</div></div>
          </div>
          <div class="flex gap-8" style="margin-bottom:16px">{badge('EPC','cyan')}{dot_badge('Terverifikasi','green')}</div>
          <div class="flex justify-between">
            <div><div style="font:700 18px var(--font-head);color:#F59E0B">&#9733; {rating}</div><div class="sub">Rating</div></div>
            <div><div style="font:700 18px var(--font-head)">{selesai}</div><div class="sub">Selesai</div></div>
            <div><div style="font:700 18px var(--font-head);color:var(--blue-600)">{aktif}</div><div class="sub">Aktif</div></div>
            <div><div style="font:700 18px var(--font-head);color:var(--green-600)">{kap}</div><div class="sub">Kapasitas</div></div>
          </div>
        </a>'''
    content = f'''      <div class="page-head-row"><div><h1 class="h1">Partner Directory</h1><p class="sub mt-4">3 mitra terverifikasi</p></div></div>
      <div class="filterbar"><select class="select select--sm"><option>Semua Kategori</option></select></div>
      <div class="catalog__grid" style="grid-template-columns:repeat(3,1fr)">{cards}</div>'''
    write('partners.html', page('ops', 'partners.html', 'Partner Directory', 'Partner Directory', content))

def build_partner_detail():
    tabs = ['Profil','Kapabilitas','Portfolio','Performance']
    tab_html = ''.join(f'<a href="#" class="tab{" is-active" if i==0 else ""}" data-tab="t{i}">{t}</a>' for i, t in enumerate(tabs))
    left = card('Company Profile', f'''<div class="kv-grid" style="grid-template-columns:1fr">
      {kv('PIC','Dewi Lestari')}{kv('Phone','021-7654321')}{kv('Email','info@alphasolar.co.id')}
      {kv('Alamat','Jl. Sudirman Kav. 52-53, Jakarta Selatan')}{kv('Berdiri','2015')}{kv('Karyawan','85 orang')}
    </div>''')
    right = card('Statistik', f'''<div class="row-2" style="gap:14px">
      <div class="card" style="text-align:center;padding:18px"><div style="font:700 22px var(--font-head);color:#F59E0B">4.8/5.0</div><div class="sub mt-4">Rating</div></div>
      <div class="card" style="text-align:center;padding:18px"><div style="font:700 22px var(--font-head);color:var(--blue-600)">3</div><div class="sub mt-4">Aktif</div></div>
      <div class="card" style="text-align:center;padding:18px"><div style="font:700 22px var(--font-head);color:var(--green-600)">18</div><div class="sub mt-4">Selesai</div></div>
      <div class="card" style="text-align:center;padding:18px"><div style="font:700 22px var(--font-head);color:var(--blue-600)">12.4 MWp</div><div class="sub mt-4">Total Kapasitas</div></div>
    </div>''')
    other_tabs = ''
    for i, t in enumerate(tabs[1:], start=1):
        placeholder = f'<p class="sub">{t} PT Alpha Solar Energi akan tampil di sini.</p>'
        other_tabs += f'<div data-tab-panel="t{i}" data-tabs-for="ptr" hidden>{card(t, placeholder)}</div>'
    content = f'''      <a class="back-link" href="partners.html">{icon('←',13)} Kembali</a>
      <div class="page-head"><h1 class="h1">PT Alpha Solar Energi</h1><p class="sub mt-4">EPC &middot; Jakarta Selatan &middot; 12.4 MWp total kapasitas</p></div>
      <div class="tabs" data-tabs="ptr">{tab_html}</div>
      <div data-tab-panel="t0" data-tabs-for="ptr"><div class="grid-2">{left}{right}</div></div>
      {other_tabs}'''
    write('partner-detail.html', page('ops', 'partners.html', 'Partner Directory', 'PT Alpha Solar Energi', content))

def build_billing():
    kpis = f'''<div class="kpi-row" style="grid-auto-columns:1fr">
      <div class="card"><div class="sub">Total Invoice</div><div style="font:700 26px var(--font-head);margin-top:8px">5</div><div class="sub mt-4">semua invoice</div></div>
      <div class="card"><div class="sub">Issued</div><div style="font:700 26px var(--font-head);color:var(--blue-600);margin-top:8px">Rp 1245 Jt</div><div class="sub mt-4">2 invoice</div></div>
      <div class="card"><div class="sub">Paid</div><div style="font:700 26px var(--font-head);color:var(--green-600);margin-top:8px">Rp 1.26 M</div><div class="sub mt-4">2 invoice</div></div>
      <div class="card"><div class="sub">Overdue</div><div style="font:700 26px var(--font-head);color:var(--red-600);margin-top:8px">Rp 1.68 M</div><div class="sub mt-4">1 invoice</div></div>
    </div>'''
    def project_block(name, pid, mitra, cap, kontrak, pct, color, invs):
        rows = ''.join(f'''<tr><td class="mono strong" style="padding-left:20px">{inv}</td><td>{ms}</td><td class="mono">{val}</td><td>{idate}</td><td>{ddate}</td><td>{dot_badge(status,skind)}</td><td style="padding-right:20px"><a href="#" style="font:600 13px var(--font-head);color:var(--green-700)">Detail</a></td></tr>''' for inv, ms, val, idate, ddate, status, skind in invs)
        return f'''<div style="margin-bottom:20px">
          <div class="flex justify-between items-center" style="margin-bottom:8px">
            <div><div style="font:700 15px var(--font-head)">{name}</div><div class="sub">{pid} &middot; {mitra} &middot; {cap}</div></div>
            <div style="text-align:right"><div class="sub">Nilai Kontrak</div><div style="font:700 16px var(--font-head);color:var(--green-600)">{kontrak}</div></div>
          </div>
          <div class="pbar" style="margin-bottom:6px"><span style="width:{pct}%;background:{color}"></span></div>
          <div class="sub text-right" style="margin-bottom:10px">{pct}% terbayar</div>
          <table class="tbl" style="margin:0"><thead><tr><th style="padding-left:20px">INVOICE</th><th>MILESTONE</th><th>NILAI</th><th>INVOICE DATE</th><th>DUE DATE</th><th>STATUS</th><th style="padding-right:20px">AKSI</th></tr></thead><tbody>{rows}</tbody></table>
        </div>'''
    p1 = project_block('RSUD Dr. Soetomo', 'PRJ-2024-0019', 'Beta EPC Indonesia', '200 kWp', 'Rp 1.35 M', 0, 'var(--slate-300)',
        [('INV-2024-0043', 'Milestone 1 - DP 30%', 'Rp 405 Jt', '2024-09-12', '2024-10-12', 'Issued', 'blue')])
    p2 = project_block('PT Bank Mandiri (Persero)', 'PRJ-2024-0018', 'Zeta Renewable', '300 kWp', 'Rp 2.10 M', 60, 'var(--green-600)',
        [('INV-2024-0044', 'Milestone 1 - DP 30%', 'Rp 630 Jt', '2024-05-20', '2024-06-20', 'Paid', 'green')])
    billing_card = card('Project Billing Detail', p1 + '<div style="border-top:1px solid var(--slate-200);margin:20px 0"></div>' + p2, '<select class="select select--sm"><option>Semua Project</option></select>')
    content = f'''      <div class="page-head"><h1 class="h1">Billing</h1><p class="sub">Kelola invoice dan pembayaran proyek</p></div>
      {kpis}<div class="mt-24">{billing_card}</div>'''
    write('billing.html', page('ops', 'billing.html', 'Billing', 'Billing', content))

if __name__ == '__main__':
    build_dashboard()
    build_executive_dashboard()
    build_work_orders()
    build_wo_detail()
    build_surveys()
    build_survey_detail()
    build_quotations()
    build_quotation_detail()
    build_projects()
    build_project_detail()
    build_partners()
    build_partner_detail()
    build_billing()
