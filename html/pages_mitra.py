"""Mitra (Partner) portal pages."""
from gen import OUT, page, kpi, card, badge, icon, kv

def write(path, html):
    p = OUT / 'mitra' / path
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(html, encoding='utf-8')
    print('wrote mitra/' + path)

def dot_badge(text, kind):
    return f'<span class="badge badge--{kind}"><span class="dot"></span>{text}</span>'

def stepper(steps, current_idx):
    out = '<div class="stepper">'
    for i, label in enumerate(steps):
        if i < current_idx:
            cls, num = 'is-done', '✓'
        elif i == current_idx:
            cls, num = 'is-current', str(i + 1)
        else:
            cls, num = '', str(i + 1)
        line = ''
        if i > 0:
            line_cls = ' is-done' if i <= current_idx else ''
            line = f'<div class="stepper__line{line_cls}"></div>'
        out += f'{line}<div class="stepper__step {cls}"><div class="stepper__num">{num}</div><div class="stepper__label">{label}</div></div>'
    out += '</div>'
    return out

def stars(n, of=5, small=False):
    cls = 'stars stars--sm' if small else 'stars'
    out = f'<div class="{cls}">'
    for i in range(of):
        out += f'<span class="star{" is-on" if i < n else ""}">★</span>'
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
      {kpi('Available Opportunities', '2', 'green', '🎯')}
      {kpi('Undangan', '1', 'blue', '📬')}
      {kpi('Pending Survey', '1', 'purple', '📍')}
      {kpi('Quotation Due', '1', 'amber', '💼', '3 hari lagi')}
      {kpi('Active Projects', '2', 'cyan', '🏗')}
    </div>'''

    actions = [
        ('red', '💼', 'Submit Quotation', 'WO-2024-0045 &ndash; Quotation due dalam 3 hari (25 Sep 2024)', 'Buat Quotation'),
        ('amber', '📍', 'Konfirmasi Survey', 'SVY-2024-0031 &ndash; Menunggu konfirmasi jadwal dari ICONGreen', 'Lihat Survey'),
        ('red', '📊', 'Update Progress', 'PRJ-2024-0019 &ndash; Progress report W9 belum dikirim (due hari ini)', 'Update Progress'),
        ('amber', '📄', 'Upload Dokumen', 'PRJ-2024-0016 &ndash; DED Engineering perlu diupload', 'Upload'),
    ]
    action_items = ''.join(f'''<div class="action-item action-item--{kind}">
      <div class="flex items-center gap-12">{icon(ic,18)}<div><div class="t">{t}</div><div class="d">{d}</div></div></div>
      <button class="btn {'btn--danger' if kind=='red' else 'btn--primary'} btn--sm">{cta}</button>
    </div>''' for kind, ic, t, d, cta in actions)
    action_card = card('🔴 Action Required', f'<div class="mt-8">{action_items}</div>', '<span class="sub">4 item</span>')

    activity = [
        ('#DBEAFE', '📍', 'Survey SVY-2024-0031 dijadwalkan ulang ke 20 Sep 2024', 'ICONGreen &middot; Kemarin, 14:45'),
    ]
    items = ''.join(f'''<div class="timeline__item"><div class="timeline__dot" style="background:{bg}">{icon(ic,13)}</div>
      <div class="timeline__body"><div class="t">{t}</div><div class="d">{d}</div></div></div>''' for bg, ic, t, d in activity)
    activity_card = card('Recent Activity', f'<div class="mt-16">{items}</div>')

    projects = [
        ('PRJ-2024-0019', 'RSUD Dr. Soetomo', 42, 48, 'At Risk', 'amber'),
        ('PRJ-2024-0016', 'Universitas Indonesia', 8, 5, 'On Track', 'green'),
    ]
    prow = ''.join(f'''<tr><td class="mono strong" style="padding-left:20px">{pid}</td><td>{cust}</td>
      <td style="min-width:200px">{pbar_labeled(a,p,("+" if a>=p else "")+str(a-p)+"%", "var(--green-600)" if a>=p else "var(--red-600)")}</td>
      <td>{dot_badge(status,skind)}</td>
      <td style="padding-right:20px"><a href="projects.html" style="font:600 13px var(--font-head);color:var(--green-700)">Detail</a></td></tr>''' for pid, cust, a, p, status, skind in projects)
    my_projects = card('My Projects', f'<table class="tbl" style="margin:0"><thead><tr><th style="padding-left:20px">PROJECT ID</th><th>CUSTOMER</th><th>PROGRESS VS PLAN</th><th>STATUS</th><th style="padding-right:20px">AKSI</th></tr></thead><tbody>{prow}</tbody></table>', '<a href="projects.html" class="link">Lihat Semua &rarr;</a>')

    content = f'''      <div class="page-head"><h1 class="h1">Dashboard Mitra</h1><p class="sub mt-4">PT Alpha Solar Energi &middot; 11 September 2024</p></div>
      {kpis}
      <div class="grid-2 mt-24" style="grid-template-columns:1.6fr 1fr">{action_card}{activity_card}</div>
      <div class="mt-24">{my_projects}</div>'''
    write('dashboard.html', page('mitra', 'dashboard.html', 'Dashboard', 'Dashboard Mitra', content))

# --------------------------------------------------------- Opportunities
def build_opportunities():
    banner = f'''<div class="alert mt-24" style="margin-bottom:20px;background:#DCFCE7;color:#15803D">{icon('💡',16)}<span>Ada <strong>2 peluang</strong> yang tersedia. Submit keminatan sebelum deadline untuk mengikuti seleksi.</span></div>'''
    opps = [
        ('WO-2024-0040', 'PT Gudang Garam', 'Kediri, Jawa Timur', 'PLTS Ground Mounted', '2024-09-20', '2 MWp'),
        ('WO-2024-0048', 'PT Holcim Indonesia', 'Bogor, Jawa Barat', 'PLTS Atap Industri', '2024-09-22', '600 kWp'),
    ]
    cards = ''
    for wo, cust, loc, tipe, due, cap in opps:
        cards += f'''<div class="card">
          <div class="flex justify-between items-start">
            <div><div class="mono strong" style="color:var(--green-700)">{wo}</div>
              <div style="font:700 18px var(--font-head);color:var(--slate-900);margin-top:4px">{cust}</div>
              <div class="sub mt-4">{loc}</div></div>
            <div style="text-align:right"><div style="font:700 22px var(--font-head);color:var(--green-600)">{cap}</div>{badge('B2B Swasta','blue')}</div>
          </div>
          <div class="kv-grid mt-24">{kv('Tipe Proyek', tipe)}{kv('Deadline', due)}</div>
          <div class="flex gap-8 mt-24"><button class="btn btn--outline">Lihat Detail</button><button class="btn btn--primary">Submit Keminatan</button></div>
        </div>'''
    content = f'''      <div class="page-head"><h1 class="h1">Opportunities</h1><p class="sub">Work Order yang tersedia dan undangan dari ICONGreen</p></div>
      <div class="tabs"><a href="#" class="tab is-active">Available (2)</a><a href="#" class="tab">Submitted (1)</a><a href="#" class="tab">Closed (1)</a></div>
      {banner}
      <div class="row-2">{cards}</div>'''
    write('opportunities.html', page('mitra', 'opportunities.html', 'Opportunities', 'Opportunities', content))

# ----------------------------------------------------------- Quotations
def build_quotations():
    banner = f'''<div class="action-item action-item--amber mt-24" style="margin-bottom:20px">
      <div><div class="t">⚠ Quotation Perlu Dibuat</div><div class="d">WO-2024-0045 &ndash; PT Astra International (750 kWp) &middot; Deadline: 2024-09-22</div></div>
      <a href="quotation-form.html" class="btn btn--primary btn--sm">Buat Quotation</a>
    </div>'''
    rows = [
        ('QUO-2024-0028', 'WO-2024-0045', 'PT Astra International', '1.2 MWp', '', '2024-09-05', 'Need Quotation', 'amber'),
        ('QUO-2024-0026', 'WO-2024-0046', 'RSUD Dr. Soetomo', '200 kWp', 'Rp 1.35 M', '2024-09-01', 'Accepted', 'green'),
    ]
    trs = ''
    for qid, wo, cust, cap, val, tgl, status, skind in rows:
        href = 'quotation-form.html' if status == 'Need Quotation' else '#'
        action = 'Buat Quotation' if status == 'Need Quotation' else 'Detail'
        val_html = f'<span class="mono strong" style="color:var(--green-700)">{val}</span>' if val else ''
        trs += f'''<tr><td class="mono strong" style="padding-left:20px">{qid}</td><td class="mono">{wo}</td><td>{cust}</td><td>{cap}</td><td>{val_html}</td><td>{tgl}</td><td>{dot_badge(status,skind)}</td><td style="padding-right:20px"><a href="{href}" style="font:600 13px var(--font-head);color:var(--green-700)">{action}</a></td></tr>'''
    content = f'''      <div class="page-head"><h1 class="h1">Quotation</h1><p class="sub">Kelola penawaran proyek</p></div>
      {banner}
      <div class="tabs"><a href="#" class="tab is-active">Semua</a><a href="#" class="tab">Under Review</a><a href="#" class="tab">Accepted</a><a href="#" class="tab">Rejected</a></div>
      <div class="card" style="padding:0"><table class="tbl" style="margin:0">
        <thead><tr><th style="padding-left:20px">ID</th><th>WO</th><th>CUSTOMER</th><th>KAPASITAS</th><th>NILAI</th><th>SUBMIT DATE</th><th>STATUS</th><th style="padding-right:20px">AKSI</th></tr></thead>
        <tbody>{trs}</tbody></table></div>'''
    write('quotations.html', page('mitra', 'quotations.html', 'Quotation', 'Quotation', content))

def build_quotation_form():
    tabs = ['Technical Proposal', 'Bill of Quantity']
    tab_html = ''.join(f'<a href="#" class="tab{" is-active" if i==0 else ""}" data-tab="t{i}">{t}</a>' for i, t in enumerate(tabs))

    tp_left = card(None, f'''<div class="muted" style="font:700 11px var(--font-head);letter-spacing:.4px;text-transform:uppercase;margin-bottom:16px">Technical Proposal</div>
      <div class="flex-col gap-16">
        <div><label class="sub" style="display:block;margin-bottom:6px">Kapasitas</label><input class="input" value="750 kWp"></div>
        <div><label class="sub" style="display:block;margin-bottom:6px">Panel Solar</label><input class="input" value="Tier 1 Monocrystalline 550Wp"></div>
        <div><label class="sub" style="display:block;margin-bottom:6px">Jumlah Panel</label><input class="input" value="1.364 pcs"></div>
        <div><label class="sub" style="display:block;margin-bottom:6px">Inverter</label><input class="input" value="String Inverter 100kW &ndash; 3 unit"></div>
        <div><label class="sub" style="display:block;margin-bottom:6px">Mounting System</label><input class="input" value="Ground Mounting Galvanized Steel"></div>
      </div>''')
    tp_right = card(None, f'''<div class="muted" style="font:700 11px var(--font-head);letter-spacing:.4px;text-transform:uppercase;margin-bottom:16px">Rencana Proyek</div>
      <div class="flex-col gap-16">
        <div><label class="sub" style="display:block;margin-bottom:6px">Durasi Proyek</label><input class="input" value="120 hari kalender"></div>
        <div><label class="sub" style="display:block;margin-bottom:6px">Validity Penawaran</label><input class="input" value="30 hari"></div>
        <div><label class="sub" style="display:block;margin-bottom:6px">Garansi Panel</label><input class="input" value="25 tahun output"></div>
        <div><label class="sub" style="display:block;margin-bottom:6px">Garansi Inverter</label><input class="input" value="5 tahun"></div>
        <div><label class="sub" style="display:block;margin-bottom:6px">Garansi Instalasi</label><input class="input" value="1 tahun"></div>
        <div><label class="sub" style="display:block;margin-bottom:6px">Catatan Tambahan</label><textarea class="input" rows="3" placeholder="Catatan atau syarat khusus..."></textarea></div>
      </div>''')
    tp_panel = f'<div class="grid-2">{tp_left}{tp_right}</div>'

    boq_rows = [
        ('Solar Panel Monocrystalline 550Wp', 'pcs', '1.364', 'Rp 2.850.000', 'Rp 3.887.400.000'),
        ('String Inverter 100kW', 'unit', '3', 'Rp 185.000.000', 'Rp 555.000.000'),
        ('Mounting System Ground', 'set', '1', 'Rp 620.000.000', 'Rp 620.000.000'),
        ('Kabel &amp; Aksesoris', 'lot', '1', 'Rp 287.000.000', 'Rp 287.000.000'),
        ('Jasa Instalasi &amp; Engineering', 'lot', '1', 'Rp 399.800.000', 'Rp 399.800.000'),
    ]
    btrs = ''.join(f'''<tr><td style="padding-left:20px">{item}</td><td>{unit}</td><td>{qty}</td><td class="mono">{harga}</td><td class="mono strong" style="padding-right:20px">{total}</td></tr>''' for item, unit, qty, harga, total in boq_rows)
    boq_table = f'''<table class="tbl" style="margin:0">
      <thead><tr><th style="padding-left:20px">ITEM</th><th>SATUAN</th><th>QTY</th><th>HARGA SATUAN</th><th style="padding-right:20px">TOTAL</th></tr></thead>
      <tbody>{btrs}</tbody></table>
      <div style="padding:14px 20px;border-top:1px solid var(--slate-200)"><button class="btn btn--outline btn--sm">+ Tambah Item</button></div>'''
    boq_total = f'''<div class="stage-banner" style="grid-template-columns:1fr auto;align-items:center">
      <div><div class="label">Total Penawaran</div><div class="val" style="font-size:24px">Rp 5.749.200.000</div></div>
    </div>'''
    boq_panel = f'<div data-tab-panel="t1" data-tabs-for="quo" hidden>{card("Bill of Quantity", boq_table)}<div class="mt-24">{boq_total}</div></div>'

    content = f'''      <a class="back-link" href="quotations.html">{icon('←',13)} Kembali</a>
      <div class="page-head-row"><div><h1 class="h1">Buat Quotation</h1><p class="sub mt-4">WO-2024-0045 &ndash; PT Astra International &middot; 750 kWp</p></div>
        <div class="flex gap-8"><button class="btn btn--outline">Simpan Draft</button><button class="btn btn--primary">Submit Quotation</button></div></div>
      <div class="tabs" data-tabs="quo">{tab_html}</div>
      <div data-tab-panel="t0" data-tabs-for="quo">{tp_panel}</div>
      {boq_panel}'''
    write('quotation-form.html', page('mitra', 'quotations.html', 'Quotation', 'Buat Quotation', content))

# ------------------------------------------------------------- Projects
def build_projects():
    projects = [
        ('PRJ-2024-0019', 'RSUD Dr. Soetomo', 'Surabaya, Jawa Timur', '200 kWp', 42, 48, 'At Risk', 'amber'),
        ('PRJ-2024-0016', 'Universitas Indonesia', 'Depok, Jawa Barat', '400 kWp', 8, 5, 'On Track', 'green'),
    ]
    cards = ''
    for pid, cust, loc, cap, actual, planned, status, skind in projects:
        delta = actual - planned
        color = 'var(--green-600)' if delta >= 0 else 'var(--red-600)'
        cards += f'''<div class="card">
          <div class="flex justify-between items-start" style="margin-bottom:14px">
            <div><div class="mono strong" style="color:var(--green-700)">{pid}</div>
              <div style="font:700 17px var(--font-head);color:var(--slate-900);margin-top:4px">{cust}</div>
              <div class="sub mt-4">{loc} &middot; {cap}</div></div>
            {dot_badge(status, skind)}
          </div>
          {pbar_labeled(actual, planned, ('+' if delta>=0 else '')+str(delta)+'%', color)}
          <div class="flex gap-8 mt-24"><a href="project-detail.html" class="btn btn--outline">Lihat Detail</a><a href="update-progress.html" class="btn btn--primary">Update Progress</a></div>
        </div>'''
    content = f'''      <div class="page-head"><h1 class="h1">My Projects</h1><p class="sub">Proyek yang ditugaskan kepada PT Alpha Solar Energi</p></div>
      <div class="row-2">{cards}</div>'''
    write('projects.html', page('mitra', 'projects.html', 'My Projects', 'My Projects', content))

def build_project_detail():
    tabs = ['Overview', 'Progress Update', 'Dokumen', 'Issues', 'Aktivitas']
    tab_html = ''.join(f'<a href="#" class="tab{" is-active" if i==0 else ""}" data-tab="t{i}">{t}</a>' for i, t in enumerate(tabs))
    overview = card('Project Overview', f'''
      <div style="margin-bottom:16px">{dot_badge('At Risk','amber')}</div>
      {pbar_labeled(42, 48, '-6%', 'var(--red-600)')}
      <div class="kv-grid mt-24">
        {kv('Project ID','PRJ-2024-0019')}{kv('Customer','RSUD Dr. Soetomo')}
        {kv('Kapasitas','200 kWp')}{kv('Phase','Procurement')}
        {kv('Start Date','2024-09-10')}{kv('Next Update','Hari ini')}
      </div>''')
    right = f'''{card(None, f'<div class="sub">Nilai Kontrak</div><div style="font:700 26px var(--font-head);color:var(--green-600);margin-top:4px">Rp 1.35 M</div>')}
      {card(None, f'{icon("⚠",15)} <strong style="color:#B45309">Status Proyek</strong><p class="mt-8" style="font-size:13px;color:#92400E">Actual Progress <b>42%</b>, Planned <b>48%</b>. Variance <b>-6%</b>. Segera update progress terbaru.</p><a href="update-progress.html" class="btn btn--primary btn--sm mt-16" style="display:inline-block">Update Progress</a>')}'''
    other_tabs = ''
    for i, t in enumerate(tabs[1:], start=1):
        placeholder = f'<p class="sub">Detail {t.lower()} untuk PRJ-2024-0019 akan tampil di sini.</p>'
        other_tabs += f'<div data-tab-panel="t{i}" data-tabs-for="prj" hidden>{card(t, placeholder)}</div>'
    content = f'''      <a class="back-link" href="projects.html">{icon('←',13)} Kembali</a>
      <div class="page-head-row"><div><h1 class="h1">PRJ-2024-0019</h1><p class="sub mt-4">RSUD Dr. Soetomo &middot; 200 kWp</p></div>{dot_badge('At Risk','amber')}</div>
      <div class="tabs mt-24" data-tabs="prj">{tab_html}</div>
      <div data-tab-panel="t0" data-tabs-for="prj"><div class="grid-2" style="grid-template-columns:1.6fr 1fr">{overview}<div class="flex-col gap-12">{right}</div></div></div>
      {other_tabs}'''
    write('project-detail.html', page('mitra', 'projects.html', 'My Projects', 'PRJ-2024-0019', content))

def build_update_progress():
    tabs = [('Engineering', 2), ('Procurement', 3), ('Construction', 2)]
    tab_html = ''.join(f'<a href="#" class="tab{" is-active" if i==0 else ""}" data-tab="t{i}">{label}<span class="badge badge--slate" style="margin-left:8px">{n}</span></a>' for i, (label, n) in enumerate(tabs))

    def item_card(title, planned, actual, variance):
        return f'''<div class="card mt-16">
          <div class="flex justify-between items-start" style="margin-bottom:14px">
            <div style="font:700 15px var(--font-head)">{title}</div>
            <div style="text-align:right"><div class="sub">Variance</div><div style="font:700 14px var(--font-head);color:var(--green-600)">{variance}</div></div>
          </div>
          <div class="flex justify-between" style="font-size:12px;margin-bottom:6px"><span class="sub">Planned {planned}%</span><span class="sub">Actual baru {actual}%</span></div>
          <div class="pbar"><span style="width:{actual}%"></span></div>
          <div class="row-2 mt-16">
            <div><label class="sub" style="display:block;margin-bottom:6px">Progress Terkini (%)</label><input class="input" value="{actual}"></div>
            <div><label class="sub" style="display:block;margin-bottom:6px">Catatan</label><input class="input" placeholder="Keterangan kemajuan..."></div>
          </div>
        </div>'''
    eng_panel = item_card('Detailed Engineering Design', 100, 100, '+0%') + item_card('Single Line Diagram', 100, 100, '+0%')
    eng_panel += f'<div class="card mt-16" style="text-align:center;color:var(--slate-500);cursor:pointer">+ Tambah Item Engineering</div>'

    other_panels = ''
    for i, (label, n) in enumerate(tabs[1:], start=1):
        placeholder = f'<p class="sub mt-16">Item progress {label.lower()} akan tampil di sini.</p>'
        other_panels += f'<div data-tab-panel="t{i}" data-tabs-for="upd" hidden>{placeholder}</div>'

    content = f'''      <a class="back-link" href="projects.html">{icon('←',13)} Kembali</a>
      <div class="page-head-row"><div><h1 class="h1">Update Progress</h1><p class="sub mt-4">PRJ-2024-0019 &middot; RSUD Dr. Soetomo</p></div>
        <div class="flex gap-8"><button class="btn btn--outline">Simpan Draft</button><button class="btn btn--primary">Review &amp; Submit →</button></div></div>
      <div class="tabs mt-24" data-tabs="upd">{tab_html}</div>
      <div data-tab-panel="t0" data-tabs-for="upd">{eng_panel}</div>
      {other_panels}'''
    write('update-progress.html', page('mitra', 'projects.html', 'My Projects', 'Update Progress', content))

# -------------------------------------------------------- Company Profile
def build_company_profile():
    tabs = ['Company Information', 'Legal & Certification', 'Technical Capability', 'Portfolio', 'Dokumen Perusahaan']
    tab_rows = ''.join(f'<a href="#" class="sidebar__item{" is-active" if i==0 else ""}" data-tab="t{i}" style="justify-content:flex-start;color:var(--slate-700)">{t}</a>' for i, t in enumerate(tabs))
    left_nav = f'<div class="card" style="padding:8px" data-tabs="prof">{tab_rows}</div>'

    info = card(None, f'''<div class="muted" style="font:700 11px var(--font-head);letter-spacing:.4px;text-transform:uppercase;margin-bottom:20px">Company Information</div>
      <div class="kv-grid">
        {kv('Nama Perusahaan','PT Alpha Solar Energi')}{kv('Kategori','EPC')}
        {kv('NPWP','01.234.567.8-901.000')}{kv('Tahun Berdiri','2015')}
        {kv('Jumlah Karyawan','85 orang')}{kv('Telepon','021-7654321')}
        {kv('Email','info@alphasolar.co.id')}{kv('Website','www.alphasolar.co.id')}
        {kv('Alamat','Jl. Sudirman Kav. 52-53, Jakarta Selatan 12190')}
      </div>''')
    other_tabs = ''
    for i, t in enumerate(tabs[1:], start=1):
        placeholder = f'<p class="sub">{t} PT Alpha Solar Energi akan tampil di sini.</p>'
        other_tabs += f'<div data-tab-panel="t{i}" data-tabs-for="prof" hidden>{card(t, placeholder)}</div>'
    content = f'''      <div class="page-head-row"><div><h1 class="h1">Company Profile</h1><p class="sub mt-4">PT Alpha Solar Energi &middot; PTR-001</p></div>
        <button class="btn btn--outline">Edit Profil</button></div>
      <div class="grid-2" style="grid-template-columns:280px 1fr;align-items:start">
        {left_nav}
        <div><div data-tab-panel="t0" data-tabs-for="prof">{info}</div>{other_tabs}</div>
      </div>'''
    write('company-profile.html', page('mitra', 'company-profile.html', 'Company Profile', 'Company Profile', content))

# ----------------------------------------------------------------- Rating
def build_rating():
    stat = f'''<div class="kpi-row" style="grid-auto-columns:1fr">
      <div class="stat-box stat-box--amber"><div class="n">1</div><div class="l">Menunggu Rating</div></div>
      <div class="stat-box stat-box--green"><div class="n">2</div><div class="l">Sudah Dirating</div></div>
      <div class="stat-box"><div class="n">4.5 ★</div><div class="l">Rating Rata-rata</div></div>
      <div class="stat-box"><div class="n">3</div><div class="l">Total Proyek Selesai</div></div>
    </div>'''
    item = f'''<div class="card">
      <div class="flex justify-between items-center">
        <div><div class="mono strong" style="color:var(--green-700)">PRJ-2024-0016</div>{badge('Belum Dirating','amber')}
          <div style="font:700 17px var(--font-head);color:var(--slate-900);margin-top:6px">RSUD Dr. Soetomo</div>
          <div class="sub mt-4">Surabaya, Jawa Timur &middot; 200 kWp &middot; Selesai: 2024-09-02</div></div>
        <div style="text-align:right"><div style="font:700 18px var(--font-head);color:var(--green-600);margin-bottom:10px">Rp 1.35 M</div>
          <a href="rating-form.html" class="btn btn--primary btn--sm">★ Beri Rating</a></div>
      </div></div>'''
    content = f'''      <div class="page-head"><h1 class="h1">Rating Proyek</h1><p class="sub">Berikan penilaian untuk proyek yang telah selesai</p></div>
      {stat}
      <div class="tabs mt-24"><a href="#" class="tab is-active">Belum Dirating <span class="badge badge--amber" style="margin-left:6px">1</span></a><a href="#" class="tab">Sudah Dirating (2)</a></div>
      {item}'''
    write('rating.html', page('mitra', 'rating.html', 'Rating Proyek', 'Rating Proyek', content))

def build_rating_form():
    info = f'''<div class="kpi-row" style="grid-auto-columns:1fr;margin-bottom:24px">
      <div class="stat-box"><div class="l" style="margin:0 0 6px">Project</div><div style="font:700 15px var(--font-head)">PRJ-2024-0016</div></div>
      <div class="stat-box"><div class="l" style="margin:0 0 6px">Customer</div><div style="font:700 15px var(--font-head)">RSUD Dr. Soetomo</div></div>
      <div class="stat-box"><div class="l" style="margin:0 0 6px">Lokasi</div><div style="font:700 15px var(--font-head)">Surabaya, Jawa Timur</div></div>
      <div class="stat-box"><div class="l" style="margin:0 0 6px">Kapasitas</div><div style="font:700 15px var(--font-head)">200 kWp</div></div>
      <div class="stat-box"><div class="l" style="margin:0 0 6px">Selesai</div><div style="font:700 15px var(--font-head)">2024-09-02</div></div>
      <div class="stat-box"><div class="l" style="margin:0 0 6px">Nilai Kontrak</div><div style="font:700 15px var(--font-head);color:var(--green-600)">Rp 1.35 M</div></div>
    </div>'''
    criteria = [
        ('Koordinasi &amp; Komunikasi', 'Kemudahan komunikasi dan respons dari tim ICONGreen'),
        ('Dukungan Teknis', 'Kualitas panduan teknis dan bantuan selama proyek'),
        ('Ketepatan Pembayaran', 'Ketepatan waktu pembayaran sesuai milestone'),
        ('Kejelasan Dokumen', 'Kelengkapan dan kejelasan dokumen kontrak dan teknis'),
        ('Fleksibilitas Scope', 'Kemampuan menyesuaikan scope jika ada perubahan lapangan'),
    ]
    crit_html = ''.join(f'''<div style="margin-bottom:24px">
      <div style="font:700 14px var(--font-head);color:var(--slate-900)">{t}</div>
      <div class="sub mt-4" style="margin-bottom:10px">{d}</div>
      {stars(0)}
    </div>''' for t, d in criteria)
    left = card('Penilaian per Kriteria', crit_html)
    right = f'''{card('Rating Keseluruhan', '<p class="sub" style="text-align:center;padding:20px 0">Isi semua kriteria untuk melihat rating keseluruhan</p>')}
      {card('Komentar &amp; Saran', '<textarea class="input" rows="5" placeholder="Tuliskan pengalaman Anda bekerja sama dengan ICONGreen pada proyek ini. Saran dan masukan sangat diapresiasi..."></textarea><div class="sub mt-8">0 karakter</div>')}
      <div class="alert alert--info mt-16">{icon('ℹ',15)}<span>Rating bersifat anonim dan hanya digunakan untuk peningkatan layanan ICONGreen. Rating tidak dapat diubah setelah disubmit.</span></div>'''
    content = f'''      <a class="back-link" href="rating.html">{icon('←',13)} Kembali</a>
      <div class="page-head-row"><div><h1 class="h1">Berikan Rating</h1><p class="sub mt-4">PRJ-2024-0016 &middot; RSUD Dr. Soetomo &middot; 200 kWp</p></div>
        <div class="flex gap-8"><button class="btn btn--outline">Batal</button><button class="btn btn--primary">Submit Rating</button></div></div>
      {info}
      <div class="grid-2" style="grid-template-columns:1.6fr 1fr">{left}<div class="flex-col gap-16">{right}</div></div>'''
    write('rating-form.html', page('mitra', 'rating.html', 'Rating Proyek', 'Berikan Rating', content))

# ----------------------------------------------------------------- Survey
def build_surveys():
    banner = f'''<div class="alert alert--warn mt-24" style="margin-bottom:18px">{icon('⏰',16)}<strong>2 Survey Memerlukan Tindakan Anda</strong></div>'''
    quick = ''
    for sid, cust, loc, status, skind in [('SVY-2024-0034', 'PLN Persero UP3 Bandung', 'Bandung, Jawa Barat', 'Requested', 'blue'), ('SVY-2024-0033', 'PT Holcim Indonesia', 'Bogor, Jawa Barat', 'ICONGreen Counter', 'purple')]:
        quick += f'''<div class="card" style="margin-bottom:12px"><div class="flex justify-between items-center">
          <div><span class="mono strong" style="color:var(--green-700)">{sid}</span> <strong>{cust}</strong> <span class="sub">{loc}</span></div>
          <div class="flex items-center gap-12">{dot_badge(status,skind)}<a href="survey-negotiation.html" class="btn btn--primary btn--sm">Tindak Lanjut →</a></div>
        </div></div>'''

    rows = [
        ('SVY-2024-0034', 'Requested', 'blue', 'PLN Persero UP3 Bandung', 'Bandung, Jawa Barat', 'Deadline: 2024-09-22', None),
        ('SVY-2024-0033', 'ICONGreen Counter', 'purple', 'PT Holcim Indonesia', 'Bogor, Jawa Barat', 'Deadline: 2024-09-20', 'Usulan terakhir (ICONGreen): 2024-09-18 &middot; 10:00 WIB &middot; <span style="color:#7C3AED">● Menunggu respons</span>'),
        ('SVY-2024-0031', 'Mitra Proposed', 'slate', 'PT Indofood CBP Sukses Makmur', 'Cikampek, Jawa Barat', 'Deadline: 2024-09-25', 'Usulan terakhir (Mitra): 2024-09-20 &middot; 09:00 WIB &middot; <span style="color:#D97706">● Menunggu respons</span>'),
    ]
    list_html = ''
    for sid, status, skind, cust, loc, due, extra in rows:
        border = 'action-item--amber' if skind in ('blue', 'purple') else ''
        list_html += f'''<div class="card {border}" style="margin-bottom:16px">
          <div class="flex justify-between items-start">
            <div><span class="mono strong" style="color:var(--green-700)">{sid}</span> {dot_badge(status, skind)}
              <div style="font:700 16px var(--font-head);color:var(--slate-900);margin-top:8px">{cust}</div>
              <div class="sub mt-4">{loc}</div>
              {f'<div class="sub mt-8">{extra}</div>' if extra else ''}</div>
            <div style="text-align:right"><div class="sub" style="margin-bottom:8px">{due}</div><a href="survey-negotiation.html" class="btn btn--outline btn--sm">Detail →</a></div>
          </div></div>'''

    content = f'''      <div class="page-head"><h1 class="h1">Survey</h1><p class="sub">Negosiasi dan konfirmasi jadwal survey bersama ICONGreen</p></div>
      {banner}
      {quick}
      <div class="mt-24">{list_html}</div>'''
    write('surveys.html', page('mitra', 'surveys.html', 'Survey', 'Survey', content))

def build_survey_negotiation():
    steps = ['Requested', 'Mitra Proposed', 'ICONGreen Counter', 'Confirmed', 'Scheduled', 'Completed']
    st = stepper(steps, 0)
    left = card('Riwayat Negosiasi Tanggal', f'''
      <p class="sub" style="text-align:center;padding:24px 0">Belum ada usulan tanggal.<br>Usulkan tanggal survey untuk memulai.</p>
      <div class="card" style="background:var(--page-bg)">
        <div style="font:700 14px var(--font-head);margin-bottom:16px">Usulkan Tanggal Survey</div>
        <div class="row-2">
          <div><label class="sub" style="display:block;margin-bottom:6px">Tanggal *</label><input class="input" placeholder=""></div>
          <div><label class="sub" style="display:block;margin-bottom:6px">Jam Mulai *</label><input class="input" placeholder=""></div>
        </div>
        <div class="mt-16"><label class="sub" style="display:block;margin-bottom:6px">Catatan (opsional)</label><input class="input" placeholder="Alasan atau kondisi khusus..."></div>
        <div class="flex gap-8 mt-16"><button class="btn btn--outline">Batal</button><button class="btn btn--primary">Kirim Usulan</button></div>
      </div>''')
    checklist = ''.join(f'<div class="flex items-center gap-8" style="padding:6px 0">{icon("✓",13)}<span>{c}</span></div>' for c in ['Kondisi atap/lahan', 'Orientasi &amp; kemiringan', 'Potensi shading', 'Akses instalasi', 'Infrastruktur listrik', 'Kapasitas daya terpasang'])
    detail_survey_body = f'''<div class="kv-grid" style="grid-template-columns:1fr">
      {kv('WO','WO-2024-0044')}{kv('Customer','PLN Persero UP3 Bandung')}{kv('Lokasi','Bandung, Jawa Barat')}
      {kv('Deadline','2024-09-22')}{kv('Confirmed Date','-')}
    </div>'''
    right = f'''{card('Detail Survey', detail_survey_body)}
    {card('Checklist Survey', checklist)}'''
    content = f'''      <a class="back-link" href="surveys.html">{icon('←',13)} Kembali</a>
      <div class="page-head-row"><div><h1 class="h1">SVY-2024-0034</h1><p class="sub mt-4">PLN Persero UP3 Bandung &middot; Bandung, Jawa Barat</p></div>{dot_badge('Requested','blue')}</div>
      <div class="card mt-24" style="margin-bottom:24px"><div class="muted" style="font:700 11px var(--font-head);letter-spacing:.4px;text-transform:uppercase;margin-bottom:16px">Alur Negosiasi Tanggal Survey</div>{st}</div>
      <div class="grid-2">{left}<div class="flex-col gap-16">{right}</div></div>'''
    write('survey-negotiation.html', page('mitra', 'surveys.html', 'Survey', 'SVY-2024-0034', content))

def build_survey_report():
    info = f'''<div class="kpi-row" style="grid-auto-columns:1fr;margin-bottom:24px">
      <div class="stat-box"><div class="l" style="margin:0 0 6px">Survey ID</div><div style="font:700 15px var(--font-head)">SVY-2024-0029</div></div>
      <div class="stat-box"><div class="l" style="margin:0 0 6px">Customer</div><div style="font:700 15px var(--font-head)">Universitas Indonesia</div></div>
      <div class="stat-box"><div class="l" style="margin:0 0 6px">Lokasi</div><div style="font:700 15px var(--font-head)">Depok, Jawa Barat</div></div>
      <div class="stat-box"><div class="l" style="margin:0 0 6px">Tgl Survey</div><div style="font:700 15px var(--font-head)">2024-09-22</div></div>
    </div>'''
    teknis = card('Estimasi Teknis &amp; Biaya', f'''
      <div class="row-2" style="grid-template-columns:1fr 1fr 1fr">
        <div><label class="sub" style="display:block;margin-bottom:6px">Kapasitas Rekomendasi (kWp) *</label><input class="input" value="1300"></div>
        <div><label class="sub" style="display:block;margin-bottom:6px">Estimasi Biaya (juta Rp) *</label><input class="input" value="1000"></div>
        <div><label class="sub" style="display:block;margin-bottom:6px">Estimasi Durasi (minggu) *</label><input class="input" value="1000"></div>
      </div>
      <div class="alert alert--info mt-16" style="justify-content:space-between"><span>Harga per Wp (otomatis)</span><span class="mono strong">Rp 769/Wp</span></div>''')
    spek = card('Spesifikasi Teknis', f'''<div class="row-2">
      <div><label class="sub" style="display:block;margin-bottom:6px">Tipe Panel Rekomendasi *</label><select class="select"><option>Polycrystalline</option></select></div>
      <div><label class="sub" style="display:block;margin-bottom:6px">Tipe Inverter</label><select class="select"><option>String Inverter</option></select></div>
    </div>''')
    penilaian = card('Penilaian &amp; Kelayakan', f'''
      <div style="margin-bottom:20px"><label class="sub" style="display:block;margin-bottom:8px">Tingkat Risiko Proyek *</label>
      <div class="pill-select"><div class="pill is-selected--green">🟢 Rendah</div><div class="pill">🟡 Sedang</div><div class="pill">🔴 Tinggi</div></div></div>
      <div><label class="sub" style="display:block;margin-bottom:8px">Rekomendasi Kelayakan *</label>
      <div class="pill-select"><div class="pill is-selected--green">Layak</div><div class="pill">Layak Bersyarat</div><div class="pill">Tidak Layak</div></div></div>''')

    rating_box = card('Rating Otomatis', f'''
      {stars(4)}
      <div style="font:700 15px var(--font-head);color:#B45309;margin:8px 0 16px">Kompetitif</div>
      <div class="muted" style="font:700 11px var(--font-head);letter-spacing:.4px;text-transform:uppercase;margin-bottom:10px">Breakdown Skor</div>
      <div class="flex-col gap-8">
        <div class="flex justify-between items-center"><span>💰 Harga/Wp</span>{stars(5, small=True)}</div>
        <div class="flex justify-between items-center"><span>⏱ Durasi/Kapasitas</span>{stars(1, small=True)}</div>
        <div class="flex justify-between items-center"><span>⚡ Kapasitas</span>{stars(5, small=True)}</div>
      </div>''')
    reco = f'<div class="stat-box stat-box--green mt-16">✅ <strong>Rekomendasi Mitra</strong><div style="font:700 18px var(--font-head);color:var(--green-600);margin-top:4px">Layak</div></div>'
    submit_btn = '<button class="btn btn--primary" style="width:100%;margin-top:16px">Submit Laporan →</button>'

    content = f'''      <a class="back-link" href="surveys.html">{icon('←',13)} Kembali</a>
      <div class="page-head-row"><div><h1 class="h1">Laporan Hasil Survey</h1><p class="sub mt-4">SVY-2024-0029 &middot; Universitas Indonesia &middot; Depok, Jawa Barat</p></div>
        <div class="flex gap-8"><button class="btn btn--outline">Batal</button><button class="btn btn--primary">Submit Laporan</button></div></div>
      {info}
      <div class="grid-2" style="grid-template-columns:1.6fr 1fr">
        <div class="flex-col gap-16">{teknis}{spek}{penilaian}</div>
        <div>{rating_box}{reco}{submit_btn}</div>
      </div>'''
    write('survey-report.html', page('mitra', 'surveys.html', 'Survey', 'Laporan Hasil Survey', content))

if __name__ == '__main__':
    build_dashboard()
    build_opportunities()
    build_quotations()
    build_quotation_form()
    build_projects()
    build_project_detail()
    build_update_progress()
    build_company_profile()
    build_rating()
    build_rating_form()
    build_surveys()
    build_survey_negotiation()
    build_survey_report()
