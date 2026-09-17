// PV Solution — Admin / ICONGreen / Mitra portals — vanilla JS, no deps.

document.addEventListener('click', function (e) {
  // ---- Modal open ----
  var opener = e.target.closest('[data-modal-open]');
  if (opener) {
    var id = opener.getAttribute('data-modal-open');
    var overlay = document.getElementById(id);
    if (overlay) overlay.hidden = false;
    return;
  }
  // ---- Modal close (button or overlay click) ----
  var closer = e.target.closest('[data-modal-close]');
  if (closer) {
    var overlay2 = closer.closest('.modal-overlay');
    if (overlay2) overlay2.hidden = true;
    return;
  }
  if (e.target.classList && e.target.classList.contains('modal-overlay')) {
    e.target.hidden = true;
    return;
  }
  // ---- Tabs ----
  var tab = e.target.closest('[data-tab]');
  if (tab) {
    var group = tab.closest('[data-tabs]');
    if (!group) return;
    var target = tab.getAttribute('data-tab');
    group.querySelectorAll('[data-tab]').forEach(function (t) { t.classList.remove('is-active'); });
    tab.classList.add('is-active');
    var panelGroup = group.getAttribute('data-tabs');
    document.querySelectorAll('[data-tab-panel][data-tabs-for="' + panelGroup + '"]').forEach(function (p) {
      p.hidden = p.getAttribute('data-tab-panel') !== target;
    });
  }
});

document.addEventListener('keydown', function (e) {
  if (e.key === 'Escape') {
    document.querySelectorAll('.modal-overlay').forEach(function (o) { o.hidden = true; });
  }
});
