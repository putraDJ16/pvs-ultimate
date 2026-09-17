#!/usr/bin/env python3
"""Generator untuk portal Admin / ICONGreen (Ops) / Mitra — PV Solution.
Jalankan: python gen.py
Semua halaman di admin/, ops/, mitra/ ditulis ulang dari sini supaya
sidebar & topbar konsisten. index.html (katalog) juga di-generate.
"""
import pathlib

OUT = pathlib.Path(__file__).parent

# --------------------------------------------------------------- Icons
# SVG inline gaya Lucide/Feather (stroke currentColor) — desain Figma-nya
# memakai emoji, tapi di sini diganti vector supaya konsisten di semua
# platform/browser dan warnanya ikut mewarisi CSS `color`.
S = 'fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"'
ICONS = {
 "sun":        (S, '<circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.93 4.93l1.41 1.41M17.66 17.66l1.41 1.41M2 12h2M20 12h2M4.93 19.07l1.41-1.41M17.66 6.34l1.41-1.41"/>'),
 "grid":       (S, '<rect x="3" y="3" width="7" height="7" rx="1"/><rect x="14" y="3" width="7" height="7" rx="1"/><rect x="3" y="14" width="7" height="7" rx="1"/><rect x="14" y="14" width="7" height="7" rx="1"/>'),
 "users":      (S, '<path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/>'),
 "building":   (S, '<rect x="4" y="2" width="16" height="20" rx="1"/><path d="M9 22v-4h6v4"/><path d="M9 6h.01M15 6h.01M9 10h.01M15 10h.01M9 14h.01M15 14h.01"/>'),
 "database":   (S, '<ellipse cx="12" cy="5" rx="8" ry="3"/><path d="M4 5v14c0 1.66 3.58 3 8 3s8-1.34 8-3V5"/><path d="M4 12c0 1.66 3.58 3 8 3s8-1.34 8-3"/>'),
 "clipboard":  (S, '<rect x="7" y="2" width="10" height="4" rx="1"/><path d="M15 4h3a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h3"/>'),
 "mapPin":     (S, '<path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 1 1 16 0Z"/><circle cx="12" cy="10" r="3"/>'),
 "briefcase":  (S, '<rect x="2" y="7" width="20" height="14" rx="2"/><path d="M16 21V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v16"/>'),
 "hardHat":    (S, '<path d="M4 15v-1a8 8 0 0 1 16 0v1"/><path d="M2 15h20"/><path d="M12 3v5"/><path d="M6 15v-3a1 1 0 0 1 1-1h1v4"/><path d="M16 15v-4h1a1 1 0 0 1 1 1v3"/>'),
 "handshake":  (S, '<path d="M8 12l3 3 5-5"/><path d="M2 10l4-4 4 4-4 4Z"/><path d="M22 10l-4-4-4 4 4 4Z"/>'),
 "dollarSign": (S, '<path d="M12 1v22"/><path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 1 1 0 7H6"/>'),
 "barChart":   (S, '<path d="M3 3v18h18"/><rect x="7" y="13" width="3" height="5"/><rect x="12" y="9" width="3" height="9"/><rect x="17" y="5" width="3" height="13"/>'),
 "trendingUp": (S, '<path d="m23 6-9.5 9.5-5-5L1 18"/><path d="M17 6h6v6"/>'),
 "target":     (S, '<circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="5"/><circle cx="12" cy="12" r="1"/>'),
 "bell":       (S, '<path d="M6 8a6 6 0 0 1 12 0c0 7 3 9 3 9H3s3-2 3-9"/><path d="M10.3 21a1.94 1.94 0 0 0 3.4 0"/>'),
 "settings":   (S, '<circle cx="12" cy="12" r="3"/><path d="M12 2v4M12 18v4M4.2 4.2l2.8 2.8M17 17l2.8 2.8M2 12h4M18 12h4M4.2 19.8l2.8-2.8M17 7l2.8-2.8"/>'),
 "zap":        ('fill="currentColor"', '<path d="M13 2 3 14h9l-1 8 10-12h-9l1-8Z"/>'),
 "inbox":      (S, '<path d="M22 12h-6l-2 3h-4l-2-3H2"/><path d="M5.45 5.11 2 12v6a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2v-6l-3.45-6.89A2 2 0 0 0 16.76 4H7.24a2 2 0 0 0-1.79 1.11Z"/>'),
 "arrowLeft":  (S, '<path d="M19 12H5"/><path d="m12 19-7-7 7-7"/>'),
 "arrowRight": (S, '<path d="M5 12h14"/><path d="m12 5 7 7-7 7"/>'),
 "arrowUp":    (S, '<path d="M12 19V5"/><path d="m5 12 7-7 7 7"/>'),
 "arrowUpDown":(S, '<path d="m21 16-4 4-4-4"/><path d="M17 20V4"/><path d="m3 8 4-4 4 4"/><path d="M7 4v16"/>'),
 "hourglass":  (S, '<path d="M6 2h12"/><path d="M6 22h12"/><path d="M6 2c0 5 12 5 12 10s-12 5-12 10"/><path d="M18 2c0 5-12 5-12 10s12 5 12 10"/>'),
 "paperclip":  (S, '<path d="M21.44 11.05 12.25 20.24a5.5 5.5 0 0 1-7.78-7.78l9.19-9.19a3.5 3.5 0 0 1 4.95 4.95L9.41 17.42a1.5 1.5 0 0 1-2.12-2.12l7.19-7.19"/>'),
 "lock":       (S, '<rect x="3" y="11" width="18" height="11" rx="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/>'),
 "calendar":   (S, '<rect x="3" y="4" width="18" height="18" rx="2"/><path d="M16 2v4M8 2v4M3 10h18"/>'),
 "reply":      (S, '<path d="M9 17l-5-5 5-5"/><path d="M4 12h10a6 6 0 0 1 6 6v1"/>'),
 "mail":       (S, '<rect x="2" y="4" width="20" height="16" rx="2"/><path d="m2 6 10 7 10-7"/>'),
 "lightbulb":  (S, '<path d="M9 18h6"/><path d="M10 22h4"/><path d="M12 2a6 6 0 0 0-4 10.5c.5.5.5 1.5.5 2.5h7c0-1 0-2 .5-2.5A6 6 0 0 0 12 2Z"/>'),
 "alarmClock": (S, '<circle cx="12" cy="13" r="8"/><path d="M12 9v4l2.5 2.5"/><path d="M5 3 3 5M19 3l2 2"/><path d="M9 1h6"/>'),
 "star":       ('fill="currentColor"', '<path d="M12 2.5l2.7 6.02 6.55.63-4.93 4.37 1.42 6.43L12 16.6l-5.74 3.35 1.42-6.43L2.75 9.15l6.55-.63L12 2.5z"/>'),
 "starOutline":(S, '<path d="M12 2.5l2.7 6.02 6.55.63-4.93 4.37 1.42 6.43L12 16.6l-5.74 3.35 1.42-6.43L2.75 9.15l6.55-.63L12 2.5z"/>'),
 "fileText":   (S, '<path d="M14 3v5h5"/><path d="M19 8v11a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h7z"/><path d="M9 13h6M9 17h4"/>'),
 "alert":      (S, '<path d="M10.3 3.9 1.8 18a2 2 0 0 0 1.7 3h17a2 2 0 0 0 1.7-3L13.7 3.9a2 2 0 0 0-3.4 0z"/><path d="M12 9v4M12 17h.01"/>'),
 "logout":     (S, '<path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"/><path d="m16 17 5-5-5-5"/><path d="M21 12H9"/>'),
 "search":     (S, '<circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/>'),
 "check":      (S, '<path d="M20 6 9 17l-5-5"/>'),
 "plus":       (S, '<path d="M12 5v14M5 12h14"/>'),
 "x":          (S, '<path d="M18 6 6 18M6 6l12 12"/>'),
 "checkCircle":(S, '<circle cx="12" cy="12" r="9"/><path d="m8.5 12.5 2.5 2.5 4.5-5"/>'),
 "info":       (S, '<circle cx="12" cy="12" r="9"/><path d="M12 11v5M12 7.5h.01"/>'),
 "refresh":    (S, '<path d="M21 12a9 9 0 1 1-2.6-6.4"/><path d="M21 3v6h-6"/>'),
 "clock":      (S, '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3.5 2"/>'),
}

def icon(name, size=14):
    attrs, body = ICONS[name]
    return (f'<span class="ic" style="width:{size}px;height:{size}px;line-height:1;display:inline-flex">'
            f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" {attrs} aria-hidden="true">{body}</svg></span>')

def status_dot(color, size=6):
    return f'<span class="status-dot" style="width:{size}px;height:{size}px;background:{color}"></span>'

# ---------------------------------------------------------- Nav config
NAVS = {
    'admin': [
        ('OVERVIEW', [('grid', 'Dashboard', 'dashboard.html')]),
        ('ADMINISTRASI', [
            ('users', 'User Management', 'users.html'),
            ('building', 'Partner Management', 'partners.html'),
            ('database', 'Master Data', 'master-data.html'),
            ('clipboard', 'Audit Log', 'audit-log.html'),
        ]),
    ],
    'ops': [
        ('OVERVIEW', [
            ('grid', 'Dashboard', 'dashboard.html'),
            ('barChart', 'Executive Dashboard', 'executive-dashboard.html'),
        ]),
        ('OPERASIONAL', [
            ('clipboard', 'Work Order', 'work-orders.html'),
            ('mapPin', 'Survey', 'surveys.html'),
            ('briefcase', 'Quotation', 'quotations.html'),
            ('hardHat', 'Projects', 'projects.html'),
        ]),
        ('MITRA & DOKUMEN', [
            ('handshake', 'Partners', 'partners.html'),
            ('fileText', 'Documents', None),
            ('dollarSign', 'Billing', 'billing.html'),
        ]),
        ('LAINNYA', [
            ('trendingUp', 'Reports', None),
            ('bell', 'Notifications', None),
        ]),
    ],
    'mitra': [
        ('OVERVIEW', [('grid', 'Dashboard', 'dashboard.html')]),
        ('BISNIS', [
            ('target', 'Opportunities', 'opportunities.html'),
            ('mapPin', 'Survey', 'surveys.html'),
            ('briefcase', 'Quotation', 'quotations.html'),
            ('hardHat', 'My Projects', 'projects.html'),
        ]),
        ('ADMINISTRASI', [
            ('fileText', 'Documents', None),
            ('dollarSign', 'Invoice', None),
            ('star', 'Rating Proyek', 'rating.html'),
            ('building', 'Company Profile', 'company-profile.html'),
        ]),
        ('LAINNYA', [
            ('bell', 'Notifications', None),
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
    <span class="sidebar__mark">{icon('sun', 18)}</span>
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
      <span class="topbar__bell">{icon('bell', 18)}<span class="dot">{bell}</span></span>
      <span class="topbar__avatar" style="background:linear-gradient(135deg,{c1},{c2})">{init}</span>
      <a class="topbar__logout" href="{depth}index.html">{icon('logout', 13)}<span>Logout</span></a>
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
