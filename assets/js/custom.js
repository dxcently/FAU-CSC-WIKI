/* FAU Cyber Security Club — site behaviour.
 * Loaded with `defer` by the theme's custom-header.html partial. */

/* --------------------------------------------------------------------
 * Variant cycle (topbar button)
 *
 * Three variants, one button: hacker -> hacker-light -> cyber -> hacker.
 * The order matches params.themeVariant in hugo.toml. Adding a fourth
 * variant means adding it to CYCLE below AND to that config — the two
 * lists are not derived from each other.
 *
 * Goes through window.relearn.changeVariant rather than setting the data
 * attribute directly: that function also writes localStorage and fires
 * `themeVariantLoaded`, which mermaid and the OpenAPI embeds listen for
 * to re-render themselves. Skipping it repaints the CSS and leaves every
 * diagram on the page stuck in the old palette.
 * -------------------------------------------------------------------- */
(function () {
  'use strict';

  /* Each step names the variant it moves TO, plus the icon and label for
     that destination — the icon shows where the button TAKES you, not
     where you are. Font Awesome Free only; the theme bundles FA Free
     7.1.0 and a class it does not ship renders as an empty box.
     fa-terminal reads as a screen, which is what `cyber` is. */
  var CYCLE = [
    { id: 'hacker',       icon: 'fa-moon',     label: 'Switch to dark' },
    { id: 'hacker-light', icon: 'fa-sun',      label: 'Switch to light' },
    { id: 'cyber',        icon: 'fa-terminal', label: 'Switch to cyber' }
  ];
  /* Every icon the cycle can paint. The swap removes ALL of them before it
     adds one, so a stale icon cannot stack under the new one. Keep this in
     sync with CYCLE, and keep fa-circle-half-stroke: that is the icon the
     Hugo partial renders server-side, before this code runs. */
  var ICONS = ['fa-moon', 'fa-sun', 'fa-terminal', 'fa-circle-half-stroke'];

  var DEFAULT = CYCLE[0].id;

  function current() {
    return document.documentElement.dataset.rThemeVariant || DEFAULT;
  }

  /* Where the button goes from here. An unknown variant — someone hand-set
     localStorage, or a variant was removed from hugo.toml — lands on index
     -1, and -1 + 1 is 0, so the cycle restarts at the default rather than
     dead-ending. */
  function next() {
    var here = current();
    var at = -1;
    for (var i = 0; i < CYCLE.length; i++) {
      if (CYCLE[i].id === here) { at = i; break; }
    }
    return CYCLE[(at + 1) % CYCLE.length];
  }

  function paintToggle() {
    var to = next();
    document.querySelectorAll('.wf-variant-toggle i').forEach(function (icon) {
      icon.classList.remove.apply(icon.classList, ICONS);
      icon.classList.add(to.icon);
    });
    document.querySelectorAll('.wf-variant-toggle button, .wf-variant-toggle a')
      .forEach(function (el) {
        el.setAttribute('title', to.label);
        el.setAttribute('aria-label', to.label);
      });
  }

  window.wfToggleVariant = function () {
    if (!window.relearn || !window.relearn.changeVariant) return;
    window.relearn.changeVariant(next().id);
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

/* --------------------------------------------------------------------
 * Matrix rain
 *
 * A full-viewport texture behind the page: columns of glyphs falling at
 * different speeds, each with a short fading tail. Opted in per page by
 * custom-footer.html, which sets data-wf-rain on <html> for the home page
 * and section landings only. NOT on leaf pages — body copy stays clean.
 *
 * It is a TEXTURE, NOT A FEATURE. Everything below is arranged so it
 * cannot become one:
 *
 *   1. NO COLOUR LIVES HERE. The glyph colour is read from the --wf-rain
 *      custom property at run time, so the rain repaints with the variant
 *      and is near-invisible in the light one. A hex literal in this file
 *      would defeat all three variants at once.
 *   2. REDUCED MOTION RENDERS NOTHING. Not a slower rain, not a static
 *      one — no canvas is created at all. Someone who asked the OS to stop
 *      animations did not ask for a quieter animation.
 *   3. THE FRAME RATE IS CAPPED. An uncapped rAF loop would repaint a
 *      full-screen canvas 120 times a second on a high-refresh display to
 *      animate something nobody is looking at. FPS below is the budget.
 *   4. HIDDEN TABS STOP. visibilitychange cancels the loop. Browsers
 *      already throttle background rAF, but "throttled" is not "off" and
 *      this costs nothing to do properly.
 *
 * The canvas is built here rather than in the template because it carries
 * no content: an empty <canvas> in the HTML is markup a reader's screen
 * reader has to skip for a decoration that may never render.
 * -------------------------------------------------------------------- */
(function () {
  'use strict';

  if (!document.documentElement.dataset.wfRain) return;
  /* Reduced motion means no MOTION, not no texture. Returning here left the
     page with nothing at all, which is more than the setting asks for: the
     field is still drawn, once, and never animates. */
  var reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  var FPS = 12;              /* a texture does not need 60 */
  var FONT = 15;             /* glyph cell, px */
  var TAIL = 9;              /* glyphs behind the head, fading out */
  var GLYPHS = '01<>[]{}/\\|=+*^?#$%&ABCDEF';

  var canvas = document.createElement('canvas');
  canvas.className = 'wf-rain';
  /* Decoration. It says nothing, so it says nothing to a screen reader. */
  canvas.setAttribute('aria-hidden', 'true');

  var ctx = canvas.getContext('2d');
  if (!ctx) return;          /* no 2d context — no rain, no error */

  var columns = [];
  var w = 0, h = 0, dpr = 1;
  var colour = '';
  var raf = 0;
  var last = 0;

  /* The one place a colour enters this file, and it comes from CSS.
     getComputedStyle is called on <html>, which is where the variant
     attribute sits and therefore where --wf-rain resolves. */
  function readColour() {
    colour = getComputedStyle(document.documentElement)
      .getPropertyValue('--wf-rain').trim().replace(/\s+/g, ' ');
  }

  function resize() {
    dpr = Math.min(window.devicePixelRatio || 1, 2);   /* 3x buys nothing here */
    w = window.innerWidth;
    h = window.innerHeight;
    canvas.width = Math.floor(w * dpr);
    canvas.height = Math.floor(h * dpr);
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    ctx.font = FONT + 'px ' + 'ui-monospace, monospace';
    ctx.textBaseline = 'top';

    var count = Math.ceil(w / FONT);
    columns = [];
    for (var i = 0; i < count; i++) {
      columns.push({
        /* stagger the start above the fold so they do not arrive as a
           single rank marching down the screen */
        y: -Math.random() * h,
        speed: FONT * (0.5 + Math.random() * 0.9)
      });
    }
  }

  function draw() {
    ctx.clearRect(0, 0, w, h);
    ctx.fillStyle = colour;
    for (var i = 0; i < columns.length; i++) {
      var col = columns[i];
      var x = i * FONT;
      for (var t = 0; t < TAIL; t++) {
        var y = col.y - t * FONT;
        if (y < -FONT || y > h) continue;
        /* globalAlpha multiplies the token's own alpha, so the tail fades
           without this file ever constructing a colour of its own */
        ctx.globalAlpha = (1 - t / TAIL) * (t === 0 ? 1 : 0.65);
        ctx.fillText(GLYPHS[(Math.random() * GLYPHS.length) | 0], x, y);
      }
      col.y += col.speed;
      if (col.y - TAIL * FONT > h) {
        col.y = -Math.random() * FONT * 12;
        col.speed = FONT * (0.5 + Math.random() * 0.9);
      }
    }
    ctx.globalAlpha = 1;
  }

  function tick(now) {
    raf = requestAnimationFrame(tick);
    if (now - last < 1000 / FPS) return;
    last = now;
    draw();
  }

  function start() {
    if (reduced) { draw(); return; }
    if (raf) return;
    last = 0;
    raf = requestAnimationFrame(tick);
  }

  function stop() {
    if (!raf) return;
    cancelAnimationFrame(raf);
    raf = 0;
  }

  /* One timer, reset on every resize event: a drag across the screen fires
     dozens of them and each one reallocates every column. */
  var resizeTimer = 0;
  window.addEventListener('resize', function () {
    clearTimeout(resizeTimer);
    resizeTimer = setTimeout(resize, 150);
  });

  document.addEventListener('visibilitychange', function () {
    if (document.hidden) stop();
    else start();
  });

  /* The variant can change under us — repaint with the new token. */
  document.addEventListener('themeVariantLoaded', readColour);

  function init() {
    document.body.appendChild(canvas);
    readColour();
    resize();
    start();
  }

  if (document.readyState !== 'loading') init();
  else document.addEventListener('DOMContentLoaded', init);
})();
