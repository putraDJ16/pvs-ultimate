#!/usr/bin/env python3
"""Generator untuk portal Admin / ICONGreen (Ops) / Mitra — PV Solution.
Jalankan: python gen.py
Semua halaman di admin/, ops/, mitra/ ditulis ulang dari sini supaya
sidebar & topbar konsisten. index.html (katalog) juga di-generate.
"""
import pathlib

OUT = pathlib.Path(__file__).parent

# --------------------------------------------------------------- Icons
# Desain Figma-nya sendiri memakai karakter emoji sebagai ikon (bukan
# vector/SVG) — jadi kita pertahankan apa adanya untuk akurasi visual.
def icon(ch, size=14):
    return f'<span class="ic" style="font-size:{size}px;line-height:1;display:inline-flex">{ch}</span>'

# ---------------------------------------------------------- Nav config
NAVS = {
    'admin': [
        ('OVERVIEW', [('⊞', 'Dashboard', 'dashboard.html')]),
        ('ADMINISTRASI', [
            ('👥', 'User Management', 'users.html'),
            ('🏢', 'Partner Management', 'partners.html'),
            ('🗄', 'Master Data', 'master-data.html'),
            ('📋', 'Audit Log', 'audit-log.html'),
        ]),
    ],
    'ops': [
        ('OVERVIEW', [
            ('⊞', 'Dashboard', 'dashboard.html'),
            ('📊', 'Executive Dashboard', 'executive-dashboard.html'),
        ]),
        ('OPERASIONAL', [
            ('📋', 'Work Order', 'work-orders.html'),
            ('📍', 'Survey', 'surveys.html'),
            ('💼', 'Quotation', 'quotations.html'),
            ('🏗', 'Projects', 'projects.html'),
        ]),
        ('MITRA & DOKUMEN', [
            ('🤝', 'Partners', 'partners.html'),
            ('📄', 'Documents', None),
            ('💰', 'Billing', 'billing.html'),
        ]),
        ('LAINNYA', [
            ('📈', 'Reports', None),
            ('🔔', 'Notifications', None),
        ]),
    ],
    'mitra': [
        ('OVERVIEW', [('⊞', 'Dashboard', 'dashboard.html')]),
        ('BISNIS', [
            ('🎯', 'Opportunities', 'opportunities.html'),
            ('📍', 'Survey', 'surveys.html'),
            ('💼', 'Quotation', 'quotations.html'),
            ('🏗', 'My Projects', 'projects.html'),
        ]),
        ('ADMINISTRASI', [
            ('📄', 'Documents', None),
            ('💰', 'Invoice', None),
            ('⭐', 'Rating Proyek', 'rating.html'),
            ('🏢', 'Company Profile', 'company-profile.html'),
        ]),
        ('LAINNYA', [
            ('🔔', 'Notifications', None),
        ]),
    ],
}

USERS = {
    'admin': ('Budi Santoso', 'Admin ICON', 'A', '#38BDF8', '#6366F1'),
    'ops':   ('Rina Kusumawati', 'ICONGreen', 'I', '#34D399', '#0EA5E9'),
    'mitra': ('Dewi Lestari', 'Mitra', 'M', '#38BDF8', '#6366F1'),
}

def sidebar(role, active_href):
    u_name, u_role, u_init, c1, c2 = USERS[role]
    groups = []
    for label, items in NAVS[role]:
        rows = []
        for ic, text, href in items:
            is_active = href == active_href
            cls = 'sidebar__item' + (' is-active' if is_active else '')
            if href:
                rows.append(f'<a class="{cls}" href="{href}">{icon(ic)}<span>{text}</span></a>')
            else:
                rows.append(f'<a class="{cls}" href="#" onclick="return false" style="opacity:.55;cursor:default">{icon(ic)}<span>{text}</span></a>')
        groups.append(f'<div class="sidebar__group"><div class="sidebar__group-label">{label}</div>{"".join(rows)}</div>')
    return f'''<aside class="sidebar">
  <div class="sidebar__brand">
    <span class="sidebar__mark">{icon('☀', 18)}</span>
    <div><div class="name">PV Solution</div><div class="tag">PLTS Management</div></div>
  </div>
  <nav class="sidebar__nav">{"".join(groups)}</nav>
  <div class="sidebar__foot">
    <span class="sidebar__avatar" style="background:linear-gradient(135deg,{c1},{c2})">{u_init}</span>
    <div><div class="name">{u_name}</div><div class="role">{u_role}</div></div>
  </div>
</aside>'''

def topbar(crumb, bell=3, init='A', c1='#38BDF8', c2='#6366F1', depth='../'):
    return f'''<header class="topbar">
    <div class="topbar__crumb"><span>PV Solution</span><span>&rsaquo;</span><span class="current">{crumb}</span></div>
    <div class="topbar__right">
      <span class="topbar__bell">{icon('🔔', 18)}<span class="dot">{bell}</span></span>
      <span class="topbar__avatar" style="background:linear-gradient(135deg,{c1},{c2})">{init}</span>
      <a class="topbar__logout" href="{depth}index.html">{icon('⏻', 13)}<span>Logout</span></a>
    </div>
  </header>'''

HEAD_TPL = '''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} &middot; PV Solution</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{depth}assets/styles.css">
</head>
<body>
'''

FOOT_TPL = '''
<script src="{depth}assets/app.js"></script>
</body>
</html>
'''

def page(role, active_href, crumb, title, content, depth='../', modals=''):
    u_name, u_role, u_init, c1, c2 = USERS[role]
    head = HEAD_TPL.format(title=title, depth=depth)
    body = f'''<div class="app">
  {sidebar(role, active_href)}
  <div class="shell-main">
    {topbar(crumb, init=u_init, c1=c1, c2=c2, depth=depth)}
    <main class="content">
{content}
    </main>
  </div>
</div>
{modals}'''
    foot = FOOT_TPL.format(depth=depth)
    return head + body + foot

# ------------------------------------------------------- small helpers
def badge(text, kind='slate'):
    return f'<span class="badge badge--{kind}">{text}</span>'

def kpi(label, value, kind, ic, delta=None, delta_kind=''):
    d = f'<div class="d {delta_kind}">{delta}</div>' if delta else ''
    return f'''<div class="kpi">
      <div><div class="k">{label}</div><div class="n">{value}</div>{d}</div>
      <div class="kpi__icon kpi__icon--{kind}">{icon(ic, 18)}</div>
    </div>'''

def card(title_html, body_html, right_html=''):
    head = f'<div class="card__head"><h3 class="h3">{title_html}</h3>{right_html}</div>' if title_html else ''
    return f'<div class="card">{head}{body_html}</div>'

def kv(k, v):
    return f'<div class="kv"><div class="k">{k}</div><div class="v">{v}</div></div>'

def pbar(pct, color=None):
    style = f' style="width:{pct}%"' + (f';background:{color}' if color else '')
    return f'<div class="pbar"><span{style}></span></div>'

if __name__ == '__main__':
    print('gen.py loaded ok — helper functions ready. Page builders are appended below in the same file as this project grows.')
