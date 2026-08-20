/* ============================================================
   TBN — shared behaviour
   Progressive enhancement only. Every page is fully readable and
   navigable with this file blocked; nothing here is load-bearing.
   ============================================================ */
(function () {
  'use strict';

  var reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ---------- Mobile navigation ------------------------------
     Pages hide .nav__links below ~1000px with no replacement, which
     leaves a phone with no way to move around the site. Rather than
     hand-editing nav markup in 24 files, clone whatever links that
     page already has into a drawer. Adding a link to a page's nav
     automatically adds it here too. */
  function buildNav() {
    var bar = document.querySelector('.nav__inner');
    if (!bar || document.querySelector('.nav__burger')) return;

    var links = document.querySelectorAll('.nav__links a');
    if (!links.length) return;

    var burger = document.createElement('button');
    burger.className = 'nav__burger';
    burger.setAttribute('aria-label', 'Open menu');
    burger.setAttribute('aria-expanded', 'false');
    burger.setAttribute('aria-controls', 'tbn-drawer');
    burger.innerHTML =
      '<svg class="ico-menu" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" aria-hidden="true"><path d="M3 6h18M3 12h18M3 18h18"/></svg>' +
      '<svg class="ico-x" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" aria-hidden="true"><path d="M6 6l12 12M18 6L6 18"/></svg>';

    var right = bar.querySelector('.nav__right');
    if (right) right.appendChild(burger); else bar.appendChild(burger);

    var drawer = document.createElement('div');
    drawer.className = 'tbn-drawer';
    drawer.id = 'tbn-drawer';
    drawer.setAttribute('role', 'dialog');
    drawer.setAttribute('aria-label', 'Site menu');

    var inner = document.createElement('div');
    inner.className = 'tbn-drawer__inner';

    var heading = document.createElement('div');
    heading.className = 'tbn-drawer__group';
    heading.textContent = 'Menu';
    inner.appendChild(heading);

    Array.prototype.forEach.call(links, function (a) {
      var copy = document.createElement('a');
      copy.href = a.getAttribute('href');
      copy.textContent = (a.textContent || '').trim();
      if (a.hasAttribute('target')) {
        copy.setAttribute('target', a.getAttribute('target'));
        copy.setAttribute('rel', 'noopener');
      }
      inner.appendChild(copy);
    });

    /* Phone and WhatsApp are the two actions that matter on a phone,
       and both are hidden by the desktop nav's media query. */
    var contact = document.createElement('div');
    contact.className = 'tbn-drawer__contact';

    var wa = document.querySelector('.nav__cta');
    if (wa) {
      var waCopy = document.createElement('a');
      waCopy.href = wa.getAttribute('href');
      waCopy.className = 'is-wa';
      waCopy.textContent = (wa.textContent || 'WhatsApp').trim();
      waCopy.setAttribute('target', '_blank');
      waCopy.setAttribute('rel', 'noopener');
      contact.appendChild(waCopy);
    }
    var tel = document.querySelector('.nav__phone');
    if (tel) {
      var telCopy = document.createElement('a');
      telCopy.href = tel.getAttribute('href');
      telCopy.textContent = 'Call ' + (tel.textContent || '').trim();
      contact.appendChild(telCopy);
    }
    if (contact.children.length) inner.appendChild(contact);

    drawer.appendChild(inner);
    document.body.appendChild(drawer);

    function setOpen(open) {
      drawer.classList.toggle('is-open', open);
      document.body.classList.toggle('tbn-nav-open', open);
      burger.setAttribute('aria-expanded', String(open));
      burger.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
    }

    burger.addEventListener('click', function () {
      setOpen(burger.getAttribute('aria-expanded') !== 'true');
    });
    drawer.addEventListener('click', function (e) {
      if (e.target.tagName === 'A') setOpen(false);
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && drawer.classList.contains('is-open')) {
        setOpen(false);
        burger.focus();
      }
    });
    /* Resizing to desktop while open would otherwise strand a locked body. */
    window.addEventListener('resize', function () {
      if (window.innerWidth > 1000 && drawer.classList.contains('is-open')) setOpen(false);
    });
  }

  /* ---------- Copy buttons on command blocks -----------------
     The Linux install instructions are worthless if the commands
     can't be copied cleanly on a phone. */
  function buildCopyButtons() {
    var blocks = document.querySelectorAll('.cmd');
    Array.prototype.forEach.call(blocks, function (block) {
      if (block.querySelector('.cmd__copy')) return;

      var btn = document.createElement('button');
      btn.className = 'cmd__copy';
      btn.type = 'button';
      btn.setAttribute('aria-label', 'Copy command');
      btn.innerHTML =
        '<svg class="ico-copy" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" aria-hidden="true"><rect x="9" y="9" width="12" height="12" rx="2"/><path d="M5 15V5a2 2 0 0 1 2-2h10"/></svg>' +
        '<svg class="ico-tick" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M4 12l5 5L20 6"/></svg>';

      btn.addEventListener('click', function () {
        var text = (block.textContent || '').trim();
        var done = function () {
          btn.classList.add('is-done');
          btn.setAttribute('aria-label', 'Copied');
          setTimeout(function () {
            btn.classList.remove('is-done');
            btn.setAttribute('aria-label', 'Copy command');
          }, 1600);
        };
        if (navigator.clipboard && navigator.clipboard.writeText) {
          navigator.clipboard.writeText(text).then(done).catch(function () {});
        } else {
          var ta = document.createElement('textarea');
          ta.value = text;
          ta.style.position = 'fixed';
          ta.style.opacity = '0';
          document.body.appendChild(ta);
          ta.select();
          try { document.execCommand('copy'); done(); } catch (e) {}
          document.body.removeChild(ta);
        }
      });

      block.appendChild(btn);
    });
  }

  /* ---------- Reading progress ------------------------------- */
  function buildProgress() {
    if (reduced) return;
    if (document.body.scrollHeight < window.innerHeight * 2.2) return;

    var bar = document.createElement('div');
    bar.className = 'tbn-progress';
    bar.setAttribute('aria-hidden', 'true');
    document.body.appendChild(bar);

    var ticking = false;
    function update() {
      var max = document.documentElement.scrollHeight - window.innerHeight;
      var pct = max > 0 ? (window.scrollY / max) * 100 : 0;
      bar.style.width = Math.min(100, Math.max(0, pct)) + '%';
      ticking = false;
    }
    window.addEventListener('scroll', function () {
      if (!ticking) { ticking = true; window.requestAnimationFrame(update); }
    }, { passive: true });
    update();
  }

  /* ---------- Scroll reveals ---------------------------------
     Only applied where IntersectionObserver exists and motion is
     welcome. Elements are never hidden unless we can guarantee
     they'll be shown again. */
  function buildReveals() {
    if (reduced || !('IntersectionObserver' in window)) return;

    var targets = document.querySelectorAll(
      '.cap-card, .pain, .fgroup, .milestone, .trust-item, .flow-item, .post-card, .term, .tool'
    );
    if (!targets.length) return;

    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add('is-in');
          io.unobserve(entry.target);
        }
      });
    }, { rootMargin: '0px 0px -8% 0px', threshold: 0.06 });

    Array.prototype.forEach.call(targets, function (el, i) {
      var box = el.getBoundingClientRect();
      if (box.top < window.innerHeight) return;   // already on screen — leave alone
      el.classList.add('tbn-reveal');
      el.style.transitionDelay = (Math.min(i % 4, 3) * 55) + 'ms';
      io.observe(el);
    });
  }

  function init() {
    try { buildNav(); } catch (e) {}
    try { buildCopyButtons(); } catch (e) {}
    try { buildProgress(); } catch (e) {}
    try { buildReveals(); } catch (e) {}
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
