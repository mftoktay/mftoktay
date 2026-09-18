(function () {
  var y = document.getElementById('yil');
  if (y) y.textContent = new Date().getFullYear();

  var dugme = document.querySelector('.menu-dugme');
  var menu = document.getElementById('ana-menu');
  if (dugme && menu) {
    var kapat = function () {
      menu.classList.remove('acik');
      dugme.setAttribute('aria-expanded', 'false');
    };
    dugme.addEventListener('click', function () {
      var acik = menu.classList.toggle('acik');
      dugme.setAttribute('aria-expanded', acik ? 'true' : 'false');
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && menu.classList.contains('acik')) { kapat(); dugme.focus(); }
    });
    var sorgu = window.matchMedia('(min-width: 921px)');
    var dinle = function (e) { if (e.matches) kapat(); };
    if (sorgu.addEventListener) sorgu.addEventListener('change', dinle);
    else if (sorgu.addListener) sorgu.addListener(dinle);
  }

  // ---- perde: ana sayfadaki sinematik zemin ----
  var c = document.getElementById('perde');
  if (!c || !c.getContext) return;
  var x = c.getContext('2d');
  var azHareket = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var w = 0, h = 0, dpr = 1, sutunlar = [];

  var tohum = 20260918;
  function rnd() { tohum = (tohum * 1664525 + 1013904223) % 4294967296; return tohum / 4294967296; }

  function kur() {
    dpr = Math.min(window.devicePixelRatio || 1, 2);
    w = c.clientWidth; h = c.clientHeight;
    if (!w || !h) return false;
    c.width = Math.round(w * dpr); c.height = Math.round(h * dpr);
    x.setTransform(dpr, 0, 0, dpr, 0, 0);
    tohum = 20260918; sutunlar = [];
    var adet = Math.max(5, Math.round(w / 165));
    for (var i = 0; i < adet; i++) {
      sutunlar.push({
        k: (i + rnd() * 0.7) / adet,
        g: 0.05 + rnd() * 0.12,
        p: 0.16 + rnd() * 0.12,
        e: (rnd() - 0.5) * 0.28,
        hiz: 0.012 + rnd() * 0.03
      });
    }
    return true;
  }

  function ciz(t) {
    if (!w || !h) return;
    var zemin = x.createLinearGradient(0, 0, 0, h);
    zemin.addColorStop(0, '#12140F');
    zemin.addColorStop(0.55, '#0C0D0A');
    zemin.addColorStop(1, '#080907');
    x.fillStyle = zemin; x.fillRect(0, 0, w, h);

    for (var i = 0; i < sutunlar.length; i++) {
      var s = sutunlar[i];
      var kay = azHareket ? 0 : Math.sin(t * s.hiz + i) * 26;
      var cx = s.k * w + kay;
      var gen = s.g * w;
      var g = x.createLinearGradient(cx - gen, 0, cx + gen, 0);
      var renk = (i % 4 === 0) ? '201,162,39' : '110,156,124';
      g.addColorStop(0, 'rgba(' + renk + ',0)');
      g.addColorStop(0.5, 'rgba(' + renk + ',' + s.p.toFixed(3) + ')');
      g.addColorStop(1, 'rgba(' + renk + ',0)');
      x.save();
      x.translate(cx, h / 2); x.transform(1, 0, s.e, 1, 0, 0); x.translate(-cx, -h / 2);
      x.fillStyle = g; x.fillRect(cx - gen, -12, gen * 2, h + 24);
      x.restore();
    }

    x.strokeStyle = 'rgba(230,233,224,.09)'; x.lineWidth = 1;
    x.beginPath();
    x.moveTo(0, Math.round(h * 0.72) + 0.5);
    x.lineTo(w, Math.round(h * 0.72) + 0.5);
    x.stroke();

    var v = x.createRadialGradient(w / 2, h / 2, Math.min(w, h) * 0.18, w / 2, h / 2, Math.max(w, h) * 0.78);
    v.addColorStop(0, 'rgba(8,9,7,0)');
    v.addColorStop(1, 'rgba(8,9,7,.9)');
    x.fillStyle = v; x.fillRect(0, 0, w, h);

    var n = Math.round(w * h / 450);
    x.fillStyle = 'rgba(230,233,224,.05)';
    for (var j = 0; j < n; j++) x.fillRect((Math.random() * w) | 0, (Math.random() * h) | 0, 1, 1);
  }

  var son = 0, gorunur = true;
  function dongu(zaman) {
    if (gorunur && zaman - son > 66) { ciz(zaman / 1000); son = zaman; }
    requestAnimationFrame(dongu);
  }

  if (kur()) { ciz(0); if (!azHareket) requestAnimationFrame(dongu); }

  if ('IntersectionObserver' in window) {
    new IntersectionObserver(function (girisler) {
      gorunur = girisler[0].isIntersecting;
    }).observe(c);
  }

  var bekle;
  window.addEventListener('resize', function () {
    clearTimeout(bekle);
    bekle = setTimeout(function () { if (kur()) ciz(performance.now() / 1000); }, 160);
  });
})();
