(function () {
  var y = document.getElementById('yil');
  if (y) y.textContent = new Date().getFullYear();

  var dugme = document.querySelector('.menu-dugme');
  var menu = document.getElementById('ana-menu');
  if (!dugme || !menu) return;

  function kapat() {
    menu.classList.remove('acik');
    dugme.setAttribute('aria-expanded', 'false');
  }

  dugme.addEventListener('click', function () {
    var acik = menu.classList.toggle('acik');
    dugme.setAttribute('aria-expanded', acik ? 'true' : 'false');
  });

  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape' && menu.classList.contains('acik')) {
      kapat();
      dugme.focus();
    }
  });

  // genis ekrana gecince acik menu kalintisi kalmasin
  var sorgu = window.matchMedia('(min-width: 901px)');
  var dinle = function (e) { if (e.matches) kapat(); };
  if (sorgu.addEventListener) sorgu.addEventListener('change', dinle);
  else if (sorgu.addListener) sorgu.addListener(dinle);
})();
