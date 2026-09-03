/* FAU Cybersecurity Club — site behaviour.
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

  /* One entry per variant, in cycle order. The icon names the variant you
     are IN; the label names the one the button moves you TO.

     It used to paint the destination icon instead, which reads backwards:
     sitting in dark mode you saw a sun and had no way to tell whether that
     meant "you are in light" or "tap for light". With two variants you
     could guess; with three you cannot. The icon is now state and the
     tooltip is the action, which is the only split that stays legible.

     Font Awesome Free only; the theme bundles FA Free 7.1.0 and a class it
     does not ship renders as an empty box. fa-terminal reads as a screen,
     which is what `cyber` is. */
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
  function indexOf(id) {
    for (var i = 0; i < CYCLE.length; i++) {
      if (CYCLE[i].id === id) return i;
    }
    return -1;
  }

  /* An unknown variant — someone hand-set localStorage, or a variant was
     removed from hugo.toml — gives -1. next() steps that to 0, restarting
     at the default; here() clamps it to 0 so the button still paints. */
  function next() { return CYCLE[(indexOf(current()) + 1) % CYCLE.length]; }
  function here() { return CYCLE[Math.max(indexOf(current()), 0)]; }

  function paintToggle() {
    var at = here(), to = next();
    document.querySelectorAll('.wf-variant-toggle i').forEach(function (icon) {
      icon.classList.remove.apply(icon.classList, ICONS);
      icon.classList.add(at.icon);
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
    else sync();
  });

  /* The variant can change under us — repaint with the new token. */
  /* Cyber only. The rain is that variant's own signature, not a site-wide
     effect: in dark it fought the blue linework and in daylight it was a
     grey haze behind body copy. The other two variants get the lit panel
     edge instead (section 6.1), which is static and reads at any size.

     Gated here rather than in the Hugo partial because the variant is a
     client-side choice — the template cannot know it, and the reader can
     change it without a page load. */
  function isCyber() {
    return document.documentElement.dataset.rThemeVariant === 'cyber';
  }

  function sync() {
    if (!isCyber()) { stop(); canvas.style.display = 'none'; return; }
    canvas.style.display = '';
    readColour();
    start();
  }

  document.addEventListener('themeVariantLoaded', sync);

  function init() {
    document.body.appendChild(canvas);
    resize();
    sync();
  }

  if (document.readyState !== 'loading') init();
  else document.addEventListener('DOMContentLoaded', init);
})();


/* --------------------------------------------------------------------
 * Breadcrumb fit
 *
 * The topbar path is a single clipped line. When the full path is wider
 * than the slot it has, drop leading segments one at a time — the root
 * end (leftmost) first — and stand a "…/" in their place, keeping the
 * current directory and as much of its tail as fits. When the whole path
 * fits, it shows with no ellipsis. Runs on load and on resize; every
 * crumb is restored first, so widening the window brings segments back.
 *
 * scrollWidth > clientWidth is a real overflow test here because the ol
 * carries the theme's .breadcrumbs rule (width:100%, min-width:0,
 * overflow:hidden) and is a flex child bounded by the fixed topbar areas
 * on either side. Reading scrollWidth after each class change forces the
 * reflow that makes the next read accurate.
 * -------------------------------------------------------------------- */
(function () {
  'use strict';

  var CUT = 'wf-crumb-cut';        /* a dropped segment (display:none)     */
  var MARK = 'wf-crumbs-truncated'; /* on the ol -> the leading "…/" shows */

  function fit() {
    var ol = document.querySelector('#R-topbar .topbar-breadcrumbs');
    if (!ol) return;
    var li = ol.querySelectorAll('li');
    if (li.length < 2) return;      /* home alone -> nothing to trim */

    /* back to the full path first, so a wider window re-shows segments */
    ol.classList.remove(MARK);
    for (var i = 0; i < li.length; i++) li[i].classList.remove(CUT);
    if (ol.scrollWidth <= ol.clientWidth) return;   /* it fits — done */

    /* overflowing: show the …/ and hide leading crumbs until it fits,
       never the last one (the current directory) */
    ol.classList.add(MARK);
    for (var j = 0; j < li.length - 1; j++) {
      li[j].classList.add(CUT);
      if (ol.scrollWidth <= ol.clientWidth) break;
    }
  }

  var raf = 0;
  function schedule() {
    if (raf) cancelAnimationFrame(raf);
    raf = requestAnimationFrame(fit);
  }

  window.addEventListener('resize', schedule);
  window.addEventListener('load', fit);   /* web font settles -> widths move */
  if (document.readyState !== 'loading') fit();
  else document.addEventListener('DOMContentLoaded', fit);
})();

/* ---------------------------------------------------------------------
 * Game of Life
 *
 * The board's background: Conway's Life on a toroidal grid the size of the
 * viewport, one generation at a time. Opted in per page by custom-footer.html
 * setting data-wf-life on <html>. Same four rules as the rain, same reasons:
 * colour from --wf-life at run time, reduced motion draws one generation and
 * never steps, the generation rate is capped, hidden tabs stop.
 *
 * Life dies: most random seeds settle into still lifes and blinkers in a few
 * hundred generations. When the population goes flat for a while, a random
 * sprinkle is dropped onto the field instead of a wipe, so the old structures
 * stay and something new grows through them.
 *
 * WHAT CANNOT GROW. Nothing here accumulates: the three grids are allocated
 * once per resize and swapped, never appended to, and a "sprinkle" flips bits
 * inside the existing grid rather than adding cells. A glider gun would still
 * only ever fill the fixed field. The two costs that DO scale with the
 * viewport are bounded on purpose:
 *
 *   MAX_CELLS  caps the grid. Past it the cell size grows instead of the
 *              array, so a 6K display gets bigger cells, not a longer loop.
 *              The per-generation work is O(cells) and runs on the main
 *              thread, so this is a frame-time budget as much as a memory one.
 *   dpr 1      the canvas backing store is width x height x dpr^2 x 4 bytes.
 *              The rain needs a retina store because glyphs are strokes;
 *              these are axis-aligned blocks, so 1x costs a quarter of the
 *              memory and looks the same.
 * -------------------------------------------------------------------- */
(function () {
  'use strict';

  if (!document.documentElement.dataset.wfLife) return;
  var reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  var GPS = 7;               /* generations per second */
  var CELL = 14;             /* px, the floor; grows to honour MAX_CELLS */
  var MAX_CELLS = 20000;     /* ~1080p at 14px. See the header note. */
  var SEED = 0.07;           /* fraction of cells alive at start */
  var FLAT = 40;             /* generations of unchanged population = stuck */
  var SPRINKLE = 0.03;       /* fraction re-seeded when stuck */

  var canvas = document.createElement('canvas');
  canvas.className = 'wf-life';
  canvas.setAttribute('aria-hidden', 'true');
  var ctx = canvas.getContext('2d');
  if (!ctx) return;

  var cols = 0, rows = 0, cell = CELL;
  var cells, next, age;      /* Uint8Array grids; age fades the freshly dead */
  var colour = '';
  var raf = 0, last = 0;
  var lastPop = -1, flat = 0;

  function readColour() {
    colour = getComputedStyle(document.documentElement)
      .getPropertyValue('--wf-life').trim().replace(/\s+/g, ' ');
  }

  function seed(fraction, keep) {
    for (var i = 0; i < cells.length; i++) {
      if (!keep) cells[i] = 0;
      if (Math.random() < fraction) cells[i] = 1;
    }
  }

  function resize() {
    /* A hidden or not-yet-laid-out viewport reports 0. Allocating a 0-cell
       grid leaves draw() with nothing and step() dividing by zero; bail and
       let the next resize event size it. */
    var w = window.innerWidth, h = window.innerHeight;
    if (w < 1 || h < 1) { cols = rows = 0; return; }

    /* Grow the cell until the grid fits the budget. sqrt because both axes
       scale together: doubling the cell quarters the count. */
    cell = CELL;
    var want = Math.ceil(w / cell) * Math.ceil(h / cell);
    if (want > MAX_CELLS) cell = Math.ceil(cell * Math.sqrt(want / MAX_CELLS));

    cols = Math.ceil(w / cell);
    rows = Math.ceil(h / cell);

    /* 1x backing store: these are blocks, not glyphs. */
    canvas.width = Math.floor(w);
    canvas.height = Math.floor(h);
    ctx.setTransform(1, 0, 0, 1, 0, 0);

    var n = cols * rows;
    cells = new Uint8Array(n);
    next = new Uint8Array(n);
    age = new Uint8Array(n);
    seed(SEED, false);
    lastPop = -1; flat = 0;
  }

  function step() {
    if (!cols) return;
    var pop = 0;
    for (var y = 0; y < rows; y++) {
      var up = ((y + rows - 1) % rows) * cols, mid = y * cols, dn = ((y + 1) % rows) * cols;
      for (var x = 0; x < cols; x++) {
        var l = (x + cols - 1) % cols, r = (x + 1) % cols;
        var n = cells[up + l] + cells[up + x] + cells[up + r]
              + cells[mid + l] + cells[mid + r]
              + cells[dn + l] + cells[dn + x] + cells[dn + r];
        var i = mid + x;
        var alive = cells[i] ? (n === 2 || n === 3) : n === 3;
        next[i] = alive ? 1 : 0;
        /* age counts down after death so a cell fades over three frames */
        age[i] = alive ? 3 : (age[i] ? age[i] - 1 : 0);
        pop += alive;
      }
    }
    var t = cells; cells = next; next = t;

    if (pop === lastPop) flat++; else flat = 0;
    lastPop = pop;
    if (flat >= FLAT || pop < cells.length * 0.01) {
      seed(SPRINKLE, true);
      flat = 0;
    }
  }

  function draw() {
    if (!cols) return;
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    ctx.fillStyle = colour;
    for (var i = 0; i < cells.length; i++) {
      var a = cells[i] ? 1 : age[i] / 6;   /* dead: .5, .33, .17, gone */
      if (!a) continue;
      ctx.globalAlpha = a;
      ctx.fillRect((i % cols) * cell + 1, ((i / cols) | 0) * cell + 1, cell - 2, cell - 2);
    }
    ctx.globalAlpha = 1;
  }

  function tick(now) {
    raf = requestAnimationFrame(tick);
    if (now - last < 1000 / GPS) return;
    last = now;
    readColour();              /* the variant can change under us */
    step();
    draw();
  }

  function start() {
    if (reduced) { readColour(); draw(); return; }
    if (raf) return;
    last = 0;
    raf = requestAnimationFrame(tick);
  }

  function stop() {
    if (!raf) return;
    cancelAnimationFrame(raf);
    raf = 0;
  }

  var resizeTimer = 0;
  window.addEventListener('resize', function () {
    clearTimeout(resizeTimer);
    resizeTimer = setTimeout(function () { resize(); if (reduced) draw(); }, 150);
  });
  document.addEventListener('visibilitychange', function () {
    if (document.hidden) stop(); else start();
  });

  function mount() {
    document.body.appendChild(canvas);
    resize();
    start();
  }
  if (document.body) mount(); else document.addEventListener('DOMContentLoaded', mount);
})();
