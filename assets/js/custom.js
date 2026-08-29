/* FAU Cyber Security Club — site behaviour.
 * Loaded with `defer` by the theme's custom-header.html partial. */

/* --------------------------------------------------------------------
 * Dark / light toggle (topbar button)
 *
 * Goes through window.relearn.changeVariant rather than setting the data
 * attribute directly: that function also writes localStorage and fires
 * `themeVariantLoaded`, which mermaid and the OpenAPI embeds listen for
 * to re-render themselves. Skipping it repaints the CSS and leaves every
 * diagram on the page stuck in the old palette.
 * -------------------------------------------------------------------- */
(function () {
  'use strict';

  var DARK = 'hacker';
  var LIGHT = 'hacker-light';

  function current() {
    return document.documentElement.dataset.rThemeVariant || DARK;
  }

  function paintToggle() {
    var dark = current() !== LIGHT;
    var label = dark ? 'Switch to light' : 'Switch to dark';
    document.querySelectorAll('.wf-variant-toggle i').forEach(function (icon) {
      icon.classList.remove('fa-moon', 'fa-sun', 'fa-circle-half-stroke');
      /* the icon shows where the button TAKES you, not where you are */
      icon.classList.add(dark ? 'fa-sun' : 'fa-moon');
    });
    document.querySelectorAll('.wf-variant-toggle button, .wf-variant-toggle a')
      .forEach(function (el) {
        el.setAttribute('title', label);
        el.setAttribute('aria-label', label);
      });
  }

  window.wfToggleVariant = function () {
    if (!window.relearn || !window.relearn.changeVariant) return;
    window.relearn.changeVariant(current() === LIGHT ? DARK : LIGHT);
    paintToggle();
  };

  /* The theme renders topbar buttons as <button>, not <a href>, so the
     javascript: URL in the partial never fires. Bind the click here. */
  function bind() {
    document.querySelectorAll('.wf-variant-toggle').forEach(function (box) {
      if (box.dataset.wfBound) return;
      box.dataset.wfBound = '1';
      box.addEventListener('click', function (ev) {
        ev.preventDefault();
        window.wfToggleVariant();
      });
    });
    paintToggle();
  }

  document.addEventListener('themeVariantLoaded', paintToggle);
  if (document.readyState !== 'loading') bind();
  else document.addEventListener('DOMContentLoaded', bind);
})();

/* --------------------------------------------------------------------
 * Scramble-reveal
 *
 * Headings resolve out of random glyphs as they scroll into view. Opted
 * in per page by custom-footer.html, which sets data-wf-scramble on
 * <html> for the home page and section landings only.
 *
 * Three things keep this cheap:
 *   1. IntersectionObserver, not a scroll handler — the browser tells us
 *      when an element arrives instead of us asking 60 times a second.
 *   2. ONE requestAnimationFrame loop shared by every element currently
 *      animating, which stops itself the moment the queue empties. Not
 *      one loop per heading.
 *   3. Only the element's first TEXT NODE is touched. Relearn puts a
 *      copy-link <span> inside every heading; rewriting innerHTML would
 *      destroy and rebuild that button on every frame.
 *
 * Every target is monospace, so a scrambled string occupies exactly the
 * width of the real one and nothing reflows.
 * -------------------------------------------------------------------- */
(function () {
  'use strict';

  if (!document.documentElement.dataset.wfScramble) return;
  if (!('IntersectionObserver' in window)) return;
  if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;

  var GLYPHS = '!<>-_\\/[]{}=+*^?#$%&01';
  var MAX_LEN = 90;          /* past this it reads as noise, not a reveal */
  var SELECTOR = [
    '.wf-hero-title', '.wf-hero-kicker', '.wf-card-title',
    '#R-body-inner h1', '#R-body-inner h2'
  ].join(', ');

  var active = [];
  var running = false;
  var frame = 0;

  function tick(now) {
    frame++;
    for (var i = active.length - 1; i >= 0; i--) {
      var it = active[i];
      var p = (now - it.start) / it.dur;
      if (p >= 1) {
        it.node.nodeValue = it.text;
        active.splice(i, 1);
        continue;
      }
      /* re-randomise on every other frame only — half the DOM writes for
         a churn rate the eye cannot tell apart */
      if (frame % 2 && it.painted) continue;
      var out = '';
      var edge = p * 1.35 * it.text.length;   /* the reveal front */
      for (var c = 0; c < it.text.length; c++) {
        var ch = it.text[c];
        if (c < edge || ch === ' ') out += ch;
        else out += GLYPHS[(Math.random() * GLYPHS.length) | 0];
      }
      it.node.nodeValue = out;
      it.painted = true;
    }
    if (active.length) requestAnimationFrame(tick);
    else running = false;
  }

  function scramble(el) {
    var node = el.firstChild;
    if (!node || node.nodeType !== 3) return;
    var text = node.nodeValue;
    if (!text.trim() || text.length > MAX_LEN) return;

    active.push({
      node: node,
      text: text,
      start: performance.now(),
      dur: Math.min(700, Math.max(320, text.length * 24)),
      painted: false
    });
    if (!running) { running = true; requestAnimationFrame(tick); }
  }

  var io = new IntersectionObserver(function (entries) {
    entries.forEach(function (e) {
      if (!e.isIntersecting) return;
      io.unobserve(e.target);      /* once per element, ever */
      scramble(e.target);
    });
  }, { rootMargin: '0px 0px -12% 0px', threshold: 0.25 });

  function observeAll() {
    document.querySelectorAll(SELECTOR).forEach(function (el) {
      io.observe(el);
    });
  }

  if (document.readyState !== 'loading') observeAll();
  else document.addEventListener('DOMContentLoaded', observeAll);
})();
