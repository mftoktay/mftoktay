# -*- coding: utf-8 -*-
"""
mftoktay.com sayfa ureticisi.

Kullanim:  python uret.py

Bu dosya sitenin TEK kaynagidir. Uretilen .html dosyalarini elle duzenleme —
bir sonraki calistirmada uzerine yazilir. Icerik degisikligi burada yapilir.

Ornek eklemek:
  * App Store uygulamasi  -> UYGULAMALAR listesine bir sozluk ekle
  * Yapilmis is / vaka    -> ISLER listesine bir sozluk ekle

Liste bosken ilgili bolum, liste sayfasi ve menu ogesi hic uretilmez;
bos sayfa yayina cikmaz. Ilk girdi eklendigi anda hepsi kendiliginden belirir.
"""

import os
import re
from datetime import date

KOK = os.path.dirname(os.path.abspath(__file__))
SITE = "https://mftoktay.com"
BUGUN = date.today().isoformat()

AD = "M. Fehmi Toktay"
ROL = "Shopify uygulama gelistiricisi"
TELEFON = "+905541386827"
TELEFON_YAZI = "+90 554 138 68 27"
INDEXNOW_ANAHTAR = "a4d17f2c9b6e485fa03c71d8e6b25904"


# ---------------------------------------------------------------------------
# VERI
# ---------------------------------------------------------------------------

# App Store'da yayinlanan / yayina hazirlanan uygulamalar.
#
# Sema (yildizli alanlar zorunlu):
# {
#   "slug":        "urun-etiket-yoneticisi",       # * URL parcasi, kucuk harf, tireli
#   "ad":          "Urun Etiket Yoneticisi",       # * uygulama adi
#   "ozet":        "Tek cumlede ne yapar.",        # * kart yazisi + meta description
#   "durum":       "yayinda",                      # * yayinda | inceleme | gelistirme
#   "app_store":   "https://apps.shopify.com/...", #   bossa buton basilmaz
#   "fiyat":       "Ucretsiz plan + $9/ay",        #   bossa satir basilmaz
#   "sorun":       "Hangi sorunu cozuyor...",      # * paragraf
#   "cozum":       ["Ne yapiyor", "..."],          # * madde listesi
#   "teknik":      ["Admin GraphQL API", "..."],   #   rozet listesi
#   "gorsel":      "/assets/uygulama-slug.png",    #   bossa gorsel basilmaz
#   "gorsel_alt":  "Ekran goruntusu: ...",         #   gorsel varsa zorunlu
#   "sss":         [("Soru?", "Cevap.")],          #   bossa SSS bolumu basilmaz
# }
UYGULAMALAR = []

# Yapilmis isler / vaka ornekleri.
#
# Sema:
# {
#   "slug":        "ornek-sabit-sepet-cubugu",     # *
#   "baslik":      "Varyant senkronlu sabit sepet cubugu",  # *
#   "musteri":     "Ornek Kuyumculuk",             # *
#   "musteri_url": "https://ornek.com/",           #   bossa link basilmaz
#   "tur":         "ozel-uygulama",                # * TUR_ADI anahtarlarindan biri
#   "ozet":        "Tek cumlede is.",              # * kart yazisi + meta description
#   "sorun":       "Baslangic durumu...",          # * paragraf
#   "yapilan":     ["Ne yapildi", "..."],          # * madde listesi
#   "sonuc":       ["1147 px -> 948 px", "..."],   #   olculmus sonuc; yoksa basilmaz
#   "teknik":      ["Liquid", "Admin API"],        #   rozet listesi
# }
ISLER = []

TUR_ADI = {
    "ozel-uygulama": "Mağazaya özel uygulama",
    "tema": "Tema geliştirme",
    "entegrasyon": "Entegrasyon",
    "otomasyon": "Otomasyon",
}

DURUM_ADI = {
    "yayinda": "App Store'da yayında",
    "inceleme": "Shopify incelemesinde",
    "gelistirme": "Geliştirme aşamasında",
}

MARKALAR = [
    ("BlackBörk USA", "https://blackborkusa.com/"),
    ("BlackBörk TR", "https://blackbork.com.tr/"),
    ("Ömerhas Kuyumculuk", "https://omerhaskuyumculuk.com/"),
    ("Nevam Kuyumculuk", "https://nevamkuyumculuk.com/"),
    ("Aşkın Concept", "https://askinconcept.com.tr/"),
    ("Numtex", "https://numtexco.com/"),
    ("Ahenk Kuruyemiş", "https://ahenkkuruyemis.com.tr/"),
    ("Armada Teknoloji", "https://armadateknoloji.com.tr/"),
    ("Moda Neslie", "https://modaneslie.com"),
    ("Variteks", "https://variteks.com/"),
    ("Moon Butik", "https://moonbutik.com/"),
    ("BodyHack", "https://www.bodyhack.com.tr/"),
    ("Tuncan Tekstil", "http://www.tuncantekstil.com/"),
]

ALANLAR = [
    ("Shopify App Store uygulamaları",
     "Herkese açık, mağazaya kurulup abonelikle kullanılan uygulamalar. Yetkilendirme, "
     "faturalama, webhook ve zorunlu veri uçları Shopify'ın kendi kurallarına göre "
     "yazılır — inceleme aşamasında en çok bu kısımlar geri döner."),
    ("Mağazaya özel uygulama",
     "App Store'a çıkmadan, tek mağaza için kurulan uygulama. Herkese uyması "
     "gerekmediği için çok daha dar ve hızlı olur; mağazanın kendi iş akışına göre yazılır."),
    ("Tema geliştirme",
     "Liquid tarafında bölüm ve blok yazımı, mevcut temaya özellik ekleme. Tema "
     "editöründen yönetilebilir olması şart — kod bilmeyen biri ayarı değiştiremiyorsa "
     "iş yarım kalmıştır."),
    ("Entegrasyon ve otomasyon",
     "Admin API üzerinden muhasebe, kargo, ERP ve pazaryeri bağlantıları; toplu ürün, "
     "fiyat ve stok işleri. Binlerce kayıtlık işler kaldığı yerden devam edebilen, "
     "loglayan script'lerle yürür."),
]

# Ana sayfadaki "Nasil calisiyorum" bolumu: olculmus, gercek vakalar.
YONTEM = [
    ['Bir kuyum mağazasında “Sepete Ekle” butonu mobilde <span class="sayi">1147.</span> '
     'pikseldeydi. Müşteri bir buçuk ekran boyunca hiçbir satın alma tetikleyicisi görmüyordu.',
     'Fiyat kırılımı ve ürün künyesi karar öncesi değil, karar sonrası bilgi. İkisini de '
     'butonun altına aldık; buton <span class="sayi">948.</span> piksele çıktı.'],
    ['Aynı mağazada sabit sepet çubuğu, varyant kimliğini sayfa yüklenirken okuyup '
     'sabitliyordu. Müşteri harf kolyede “Ç” seçiyor, çubuk sepete “A” ekliyordu.',
     'Kimliği asıl ürün formundan tıklama anında okuyacak şekilde değiştirdik. Böyle bir '
     'hata sipariş gelene kadar kimseye görünmüyor — kod okuyarak değil, formdaki değerle '
     'çubuğun gönderdiği değeri karşılaştırarak bulunuyor.'],
    ['Bir katalogda ürün türü alanında <span class="sayi">71</span> farklı değer vardı: '
     '“Yüzük 8”, “Bileklik 15”, “Kolye-5”. Sayılar gramaj değil, sıra numarasıydı.',
     'Google Shopping eşleştirmesi bu yüzden tutmuyordu. <span class="sayi">6</span> '
     'kategoriye indirdik; eski değerleri silmeden önce geri dönüş için ayrı bir '
     'metafield\'a yazdık.'],
]

# Ozel yazilim sayfasindaki surec adimlari.
SUREC = [
    ("Ne olduğunu ölçerim",
     "İlk iş mevcut durumu rakamla tespit etmek. Hangi sayfada, hangi adımda, kaç "
     "kayıtta sorun var — bu bilinmeden yazılacak kod tahmine dayanır."),
    ("Kapsamı yazılı veririm",
     "Ne yapılacağı, neyin dışarıda kaldığı ve teslim biçimi baştan yazılır. "
     "Sonradan büyüyen iş ikimize de pahalıya patlar."),
    ("Ayrı temada geliştiririm",
     "Tema işleri yayınlanmamış bir kopyada yazılır, önizleme adresiyle doğrulanır, "
     "sonra canlıya alınır. Uygulama işlerinde geliştirme mağazası kullanılır."),
    ("Ölçerek teslim ederim",
     "Teslimde “yapıldı” demek yetmez; öncesi ve sonrası aynı yöntemle ölçülür. Toplu "
     "veri işlerinde eski değerlerin yedeği ve geri alma script'i bırakılır."),
]

OZEL_KAPSAM = [
    ("Mağazaya özel uygulama",
     "Tek mağaza için kurulan, App Store'a çıkmayan uygulama. Sipariş sonrası iş "
     "akışları, özel fiyatlandırma, bayi paneli, stok ve fiyat senkronu gibi işler."),
    ("Tema özelliği",
     "Sabit sepet çubuğu, ürün künyesi, çapraz satış şeridi, eşikli hediye mekaniği, "
     "favoriler — uygulama kurmadan tema içinde çözülebilen özellikler."),
    ("Veri ve katalog işleri",
     "Toplu ürün, varyant, fiyat ve metafield güncellemeleri; başka platformdan "
     "aktarım; kategori ve etiket düzeni; yönlendirme haritası."),
    ("Dış sistem bağlantısı",
     "Muhasebe, kargo, ERP ve pazaryeri entegrasyonları. Webhook kurulumu, hata "
     "durumunda tekrar deneme ve log."),
]


# ---------------------------------------------------------------------------
# YARDIMCILAR
# ---------------------------------------------------------------------------

URETILEN = []


def yaz(yol, icerik):
    tam = os.path.join(KOK, yol)
    klasor = os.path.dirname(tam)
    if klasor:
        os.makedirs(klasor, exist_ok=True)
    with open(tam, "w", encoding="utf-8", newline="\n") as f:
        f.write(icerik)
    URETILEN.append(yol)
    return yol


def kacir(s):
    return (s.replace("&", "&amp;").replace("<", "&lt;")
             .replace(">", "&gt;").replace('"', "&quot;"))


def duz(s):
    """HTML etiketlerini soker — meta description ve JSON-LD icin."""
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", s)).strip()


def json_kacir(s):
    return duz(s).replace("\\", "\\\\").replace('"', '\\"')


def menu(aktif):
    ogeler = [("/", "Ana sayfa")]
    if UYGULAMALAR:
        ogeler.append(("/uygulamalar/", "Uygulamalar"))
    ogeler.append(("/ozel-yazilim/", "Özel yazılım"))
    if ISLER:
        ogeler.append(("/isler/", "İşler"))
    satirlar = []
    for yol, ad in ogeler:
        gecerli = ' aria-current="page"' if yol == aktif else ""
        satirlar.append('<a href="%s"%s>%s</a>' % (yol, gecerli, ad))
    return ('<nav class="ust" aria-label="Ana menü"><div class="sarmal">'
            '<a class="ust__ad" href="/">%s</a>'
            '<div class="ust__ler">%s</div></div></nav>'
            % (AD, "".join(satirlar)))


def kirinti(parcalar):
    """parcalar: [(ad, url ya da None)] — sonuncusu link olmaz."""
    gorunur, kayit = [], []
    for i, (ad, url) in enumerate(parcalar):
        if url:
            gorunur.append('<li><a href="%s">%s</a></li>' % (url, kacir(ad)))
        else:
            gorunur.append('<li aria-current="page">%s</li>' % kacir(ad))
        kayit.append('{"@type":"ListItem","position":%d,"name":"%s"%s}'
                     % (i + 1, json_kacir(ad),
                        (',"item":"%s%s"' % (SITE, url)) if url else ""))
    html = ('<nav aria-label="Neredesiniz"><ol class="crumbs">%s</ol></nav>'
            % "".join(gorunur))
    ld = ('{"@context":"https://schema.org","@type":"BreadcrumbList",'
          '"itemListElement":[%s]}' % ",".join(kayit))
    return html, ld


def rozetler(liste):
    if not liste:
        return ""
    return ('<div class="rozetler">%s</div>'
            % "".join('<span class="rozet">%s</span>' % kacir(t) for t in liste))


def maddeler(liste):
    return ('<ul class="maddeler">%s</ul>'
            % "".join("<li>%s</li>" % m for m in liste))


def sss_blok(ciftler, baslik_id):
    if not ciftler:
        return "", None
    govde = "".join(
        '<div class="sss"><h3>%s</h3><p>%s</p></div>' % (kacir(s), kacir(c))
        for s, c in ciftler)
    ld = ('{"@context":"https://schema.org","@type":"FAQPage","mainEntity":[%s]}'
          % ",".join(
              '{"@type":"Question","name":"%s","acceptedAnswer":'
              '{"@type":"Answer","text":"%s"}}' % (json_kacir(s), json_kacir(c))
              for s, c in ciftler))
    html = ("""
  <section aria-labelledby="%s">
    <div class="sarmal">
      <h2 class="bolum-basligi" id="%s">Sık sorulanlar</h2>
      %s
    </div>
  </section>""" % (baslik_id, baslik_id, govde))
    return html, ld


def sayfa(baslik, aciklama, kanonik, aktif_menu, govde, ld_bloklari=(), robots=None):
    ld = "".join('\n<script type="application/ld+json">%s</script>' % b
                 for b in ld_bloklari if b)
    rb = '\n<meta name="robots" content="%s" />' % robots if robots else ""
    return """<!doctype html>
<html lang="tr">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>%(baslik)s</title>
<meta name="description" content="%(aciklama)s" />
<link rel="canonical" href="%(kanonik)s" />%(rb)s
<meta property="og:type" content="website" />
<meta property="og:url" content="%(kanonik)s" />
<meta property="og:title" content="%(baslik)s" />
<meta property="og:description" content="%(aciklama)s" />
<meta property="og:locale" content="tr_TR" />
<meta name="twitter:card" content="summary" />
<link rel="icon" href="/favicon.svg" type="image/svg+xml" />
<link rel="preconnect" href="https://fonts.googleapis.com" />
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Newsreader:opsz,wght@6..72,400;6..72,500;6..72,600&family=Karla:wght@400;500;600&display=swap" />
<link rel="stylesheet" href="/assets/stil.css" />%(ld)s
</head>
<body>
%(menu)s
%(govde)s
<footer>
  <div class="sarmal">
    <div>&copy; <span id="yil">%(yil)s</span> %(ad)s</div>
    <div>
      <a href="/kvkk.html">KVKK</a> &middot;
      <a href="/gizlilik.html">Gizlilik</a>
    </div>
  </div>
</footer>
<script>document.getElementById('yil').textContent=new Date().getFullYear();</script>
</body>
</html>
""" % {"baslik": kacir(baslik), "aciklama": kacir(aciklama), "kanonik": kanonik,
       "rb": rb, "ld": ld, "menu": menu(aktif_menu), "govde": govde,
       "yil": BUGUN[:4], "ad": AD}


def iletisim_bolumu():
    return """
  <section aria-labelledby="iletisim-h">
    <div class="sarmal">
      <h2 class="bolum-basligi" id="iletisim-h">İletişim</h2>
      <p class="bolum-giris">Bir fikir ya da tıkanmış bir iş varsa yazın. Yapılması
        gerekenin ne olduğunu söylemek çoğu zaman kısa sürüyor.</p>
      <div class="iletisim-satir">
        <div>
          <span>WhatsApp</span>
          <a href="https://wa.me/%(t)s" target="_blank" rel="noopener">%(ty)s</a>
        </div>
        <div>
          <span>Telefon</span>
          <a href="tel:%(tp)s">%(ty)s</a>
        </div>
      </div>
    </div>
  </section>""" % {"t": TELEFON.lstrip("+"), "tp": TELEFON, "ty": TELEFON_YAZI}


def kart(url, ust, baslik, ozet, alt=""):
    return ("""<a class="kart" href="%s">
          <span class="kart__ust">%s</span>
          <span class="kart__baslik">%s</span>
          <span class="kart__ozet">%s</span>%s
        </a>""" % (url, kacir(ust), kacir(baslik), kacir(ozet),
                   ('<span class="kart__alt">%s</span>' % kacir(alt)) if alt else ""))


# ---------------------------------------------------------------------------
# STIL
# ---------------------------------------------------------------------------

STIL = """:root{
  --kagit:#F7F5F0;
  --kagit-2:#FFFFFF;
  --murekkep:#23241F;
  --murekkep-2:#565851;
  --murekkep-3:#6A6C62;
  --cizgi:#E2DED3;
  --yesil:#3D5A4A;
  --yesil-2:#527060;
  --yesil-yumusak:#E7EDE7;
  --genislik:680px;
  --genislik-genis:900px;
}

*{box-sizing:border-box;margin:0;padding:0}
html{scroll-behavior:smooth}
@media (prefers-reduced-motion:reduce){
  html{scroll-behavior:auto}
  *,*::before,*::after{animation-duration:.01ms!important;transition-duration:.01ms!important}
}

body{
  background:var(--kagit);
  color:var(--murekkep);
  font-family:'Karla',ui-sans-serif,system-ui,'Segoe UI',sans-serif;
  font-size:17px;
  line-height:1.65;
  -webkit-font-smoothing:antialiased;
}

.sarmal{max-width:var(--genislik);margin:0 auto;padding:0 24px}
.sarmal--genis{max-width:var(--genislik-genis)}

a{
  color:var(--yesil);
  text-decoration:none;
  border-bottom:1px solid rgba(61,90,74,.3);
  transition:border-color .2s ease,color .2s ease;
}
a:hover{color:var(--yesil-2);border-bottom-color:var(--yesil-2)}
a:focus-visible{outline:2px solid var(--yesil);outline-offset:3px;border-radius:2px}

/* ust menu */
.ust{border-bottom:1px solid var(--cizgi);background:var(--kagit)}
.ust .sarmal{
  display:flex;align-items:center;justify-content:space-between;
  gap:10px 24px;flex-wrap:wrap;padding-top:16px;padding-bottom:16px;
}
.ust__ad{
  font-family:'Newsreader',Georgia,serif;font-size:17px;font-weight:600;
  color:var(--murekkep);border-bottom:0;letter-spacing:-.01em;
}
.ust__ad:hover{color:var(--yesil)}
.ust__ler{display:flex;flex-wrap:wrap;gap:6px 20px;font-size:15px}
.ust__ler a{color:var(--murekkep-2);border-bottom-color:transparent}
.ust__ler a:hover{color:var(--yesil);border-bottom-color:var(--yesil)}
.ust__ler a[aria-current="page"]{color:var(--murekkep);font-weight:600;border-bottom-color:var(--cizgi)}

/* kirinti yolu */
.crumbs{
  list-style:none;display:flex;flex-wrap:wrap;gap:4px 8px;
  font-size:13.5px;color:var(--murekkep-3);padding:26px 0 0;
}
.crumbs li+li::before{content:"\\203A";margin-right:8px;color:var(--cizgi)}
.crumbs a{color:var(--murekkep-3);border-bottom-color:transparent}
.crumbs a:hover{color:var(--yesil);border-bottom-color:var(--yesil)}

/* giris */
.giris{padding:72px 0 0}
.giris--ic{padding:20px 0 0}
.ad{
  font-family:'Newsreader',Georgia,serif;
  font-size:clamp(34px,6vw,46px);
  font-weight:500;letter-spacing:-.015em;line-height:1.12;
}
.ad--ic{font-size:clamp(28px,5vw,38px)}
.rol{
  margin-top:10px;font-size:14px;letter-spacing:.07em;text-transform:uppercase;
  color:var(--murekkep-3);font-weight:600;
}
.giris--ic .rol{margin-top:0;margin-bottom:8px}
.giris p:not(.rol){margin-top:26px;font-size:19px;line-height:1.7;color:var(--murekkep-2);max-width:56ch}
.giris p:not(.rol)+p{margin-top:16px}
.giris strong{font-weight:600;color:var(--murekkep)}

section{padding:60px 0}
.bolum-basligi{
  font-family:'Newsreader',Georgia,serif;font-size:14px;font-weight:600;
  letter-spacing:.13em;text-transform:uppercase;color:var(--murekkep-3);
  padding-bottom:12px;border-bottom:1px solid var(--cizgi);margin-bottom:30px;
}
.bolum-giris{color:var(--murekkep-2);max-width:60ch;margin-bottom:26px}

.alan{padding:22px 0;border-bottom:1px solid var(--cizgi)}
.alan:last-child{border-bottom:0;padding-bottom:0}
.alan h3{
  font-family:'Newsreader',Georgia,serif;font-size:21px;font-weight:500;
  letter-spacing:-.01em;margin-bottom:6px;
}
.alan p{color:var(--murekkep-2);max-width:60ch}

.ornek{padding:26px 0;border-bottom:1px solid var(--cizgi)}
.ornek:last-child{border-bottom:0;padding-bottom:0}
.ornek p{color:var(--murekkep-2);max-width:62ch}
.ornek p+p{margin-top:12px}
.sayi{
  font-family:'Newsreader',Georgia,serif;font-variant-numeric:tabular-nums;
  font-weight:600;color:var(--murekkep);white-space:nowrap;
}

/* kartlar */
.kartlar{display:grid;gap:14px;grid-template-columns:repeat(auto-fill,minmax(258px,1fr))}
.kart{
  display:flex;flex-direction:column;gap:6px;padding:22px 24px;
  background:var(--kagit-2);border:1px solid var(--cizgi);border-radius:8px;
  color:inherit;transition:border-color .2s ease,box-shadow .2s ease,transform .2s ease;
}
.kart:hover{border-color:var(--yesil-2);box-shadow:0 2px 14px rgba(35,36,31,.06);transform:translateY(-1px)}
.kart__ust{
  font-size:12.5px;letter-spacing:.07em;text-transform:uppercase;
  color:var(--murekkep-3);font-weight:600;
}
.kart__baslik{
  font-family:'Newsreader',Georgia,serif;font-size:20px;font-weight:500;
  line-height:1.25;color:var(--murekkep);
}
.kart__ozet{color:var(--murekkep-2);font-size:16px;line-height:1.6}
.kart__alt{margin-top:4px;font-size:13.5px;color:var(--murekkep-3)}

/* rozetler */
.rozetler{display:flex;flex-wrap:wrap;gap:8px 10px;margin-top:20px}
.rozet{
  font-size:14px;padding:5px 12px;border:1px solid var(--cizgi);border-radius:999px;
  color:var(--murekkep-2);background:var(--kagit-2);
}

.markalar{display:flex;flex-wrap:wrap;gap:8px 10px}
.marka{
  font-size:15px;padding:7px 14px;border:1px solid var(--cizgi);border-radius:999px;
  color:var(--murekkep-2);background:var(--kagit-2);
  transition:border-color .2s ease,color .2s ease,background .2s ease;
}
a.marka:hover{color:var(--yesil);border-color:var(--yesil-2);background:var(--yesil-yumusak)}

.maddeler{list-style:none;margin-top:4px}
.maddeler li{position:relative;padding-left:20px;color:var(--murekkep-2);max-width:62ch;margin-top:8px}
.maddeler li::before{content:"";position:absolute;left:2px;top:12px;width:7px;height:1px;background:var(--yesil)}

.durum{
  display:inline-block;font-size:13px;font-weight:600;letter-spacing:.05em;
  text-transform:uppercase;padding:4px 11px;border-radius:999px;
  background:var(--yesil-yumusak);color:var(--yesil);margin-top:14px;
}

.btn{
  display:inline-block;margin-top:22px;padding:11px 22px;border-radius:6px;
  background:var(--yesil);color:#fff;font-weight:600;font-size:16px;border-bottom:0;
  transition:background .2s ease;
}
.btn:hover{background:var(--yesil-2);color:#fff;border-bottom:0}

.gorsel{margin-top:26px;width:100%;height:auto;border:1px solid var(--cizgi);border-radius:8px}

.sss{padding:20px 0;border-bottom:1px solid var(--cizgi)}
.sss:last-child{border-bottom:0;padding-bottom:0}
.sss h3{font-family:'Newsreader',Georgia,serif;font-size:19px;font-weight:500;margin-bottom:6px}
.sss p{color:var(--murekkep-2);max-width:62ch}

.taftri{
  padding:28px 30px;background:var(--yesil-yumusak);
  border-left:2px solid var(--yesil);border-radius:0 6px 6px 0;
}
.taftri h3{font-family:'Newsreader',Georgia,serif;font-size:20px;font-weight:500;margin-bottom:8px}
.taftri p{color:var(--murekkep-2);max-width:56ch}
.taftri a{font-weight:500}

.iletisim-satir{display:flex;flex-wrap:wrap;gap:14px 32px;font-size:17px}
.iletisim-satir span{
  color:var(--murekkep-3);font-size:13px;display:block;margin-bottom:2px;
  letter-spacing:.06em;text-transform:uppercase;font-weight:600;
}

.devam{margin-top:22px;margin-bottom:0}

footer{
  padding:40px 0 56px;border-top:1px solid var(--cizgi);
  color:var(--murekkep-3);font-size:14px;
}
footer .sarmal{display:flex;flex-wrap:wrap;gap:8px 20px;justify-content:space-between}
footer a{color:var(--murekkep-3);border-bottom-color:transparent}
footer a:hover{color:var(--yesil);border-bottom-color:var(--yesil)}

@media (max-width:600px){
  body{font-size:16px}
  .giris{padding-top:48px}
  .giris p:not(.rol){font-size:17.5px}
  section{padding:44px 0}
  .taftri{padding:24px 22px}
  .kart{padding:20px}
}
"""


# ---------------------------------------------------------------------------
# JSON-LD
# ---------------------------------------------------------------------------

def ld_kisi():
    return ('{"@context":"https://schema.org","@type":"Person",'
            '"name":"%s","jobTitle":"Shopify uygulama geliştiricisi",'
            '"url":"%s/","telephone":"%s",'
            '"knowsAbout":["Shopify uygulama geliştirme","Shopify App Store",'
            '"Shopify Admin API","Liquid tema geliştirme","E-ticaret entegrasyonu",'
            '"Katalog ve veri düzeni"],"sameAs":["https://taftri.com/"]}'
            % (AD, SITE, TELEFON))


def ld_site():
    return ('{"@context":"https://schema.org","@type":"WebSite",'
            '"name":"%s","url":"%s/","inLanguage":"tr-TR"}' % (AD, SITE))


# ---------------------------------------------------------------------------
# SAYFALAR
# ---------------------------------------------------------------------------

def ana_sayfa():
    baslik = "%s — Shopify uygulama geliştiricisi" % AD
    aciklama = ("Shopify için yazılım geliştiriyorum: App Store uygulamaları, mağazaya "
                "özel uygulamalar, Liquid tema geliştirme ve Admin API entegrasyonları.")

    alan_html = "".join('<div class="alan"><h3>%s</h3><p>%s</p></div>' % (kacir(b), m)
                        for b, m in ALANLAR)

    parcalar = ["""
  <header class="giris">
    <div class="sarmal">
      <h1 class="ad">%(ad)s</h1>
      <p class="rol">Shopify uygulama geliştiricisi</p>
      <p>Shopify için yazılım geliştiriyorum. Bir kısmı App Store'da herkese açık
        uygulama olarak çıkıyor, bir kısmı tek bir mağaza için yazılıp orada kalıyor.</p>
      <p>İkisinin ortak yanı şu: iş yeni bir şey icat etmekle değil,
        <strong>ölçmekle</strong> başlıyor. Bir butonun sayfanın kaçıncı pikselinde
        durduğunu bilmeden onu yukarı almanın anlamı yok.</p>
    </div>
  </header>

  <section aria-labelledby="alanlar-h">
    <div class="sarmal">
      <h2 class="bolum-basligi" id="alanlar-h">Ne geliştiriyorum</h2>
      %(alanlar)s
    </div>
  </section>""" % {"ad": AD, "alanlar": alan_html}]

    if UYGULAMALAR:
        kartlar = "".join(
            kart("/uygulamalar/%s/" % u["slug"],
                 DURUM_ADI.get(u.get("durum", ""), "Uygulama"),
                 u["ad"], u["ozet"], u.get("fiyat", ""))
            for u in UYGULAMALAR[:6])
        parcalar.append("""
  <section aria-labelledby="uygulamalar-h">
    <div class="sarmal">
      <h2 class="bolum-basligi" id="uygulamalar-h">Uygulamalar</h2>
      <div class="kartlar">%s</div>
      <p class="devam"><a href="/uygulamalar/">Tüm uygulamalar</a></p>
    </div>
  </section>""" % kartlar)

    if ISLER:
        kartlar = "".join(
            kart("/isler/%s/" % i["slug"], TUR_ADI.get(i.get("tur", ""), "İş"),
                 i["baslik"], i["ozet"], i.get("musteri", ""))
            for i in ISLER[:6])
        parcalar.append("""
  <section aria-labelledby="isler-h">
    <div class="sarmal">
      <h2 class="bolum-basligi" id="isler-h">Yapılmış işler</h2>
      <div class="kartlar">%s</div>
      <p class="devam"><a href="/isler/">Tüm işler</a></p>
    </div>
  </section>""" % kartlar)

    yontem_html = "".join('<div class="ornek">%s</div>' % "".join("<p>%s</p>" % p for p in vaka)
                          for vaka in YONTEM)
    parcalar.append("""
  <section aria-labelledby="nasil-h">
    <div class="sarmal">
      <h2 class="bolum-basligi" id="nasil-h">Nasıl çalışıyorum</h2>
      %s
    </div>
  </section>""" % yontem_html)

    parcalar.append("""
  <section aria-labelledby="ozel-h">
    <div class="sarmal">
      <h2 class="bolum-basligi" id="ozel-h">Özel geliştirme</h2>
      <p class="bolum-giris">App Store'a çıkmayan, tek mağaza için yazılan işler ayrı
        yürüyor. Kapsam, süreç ve teslim biçimi ayrı sayfada.</p>
      <p style="margin:0"><a href="/ozel-yazilim/">Özel yazılım sayfasına git</a></p>
    </div>
  </section>""")

    marka_html = "".join('<a class="marka" href="%s" target="_blank" rel="noopener">%s</a>'
                         % (u, kacir(a)) for a, u in MARKALAR)
    parcalar.append("""
  <section aria-labelledby="markalar-h">
    <div class="sarmal">
      <h2 class="bolum-basligi" id="markalar-h">Birlikte çalıştığım markalar</h2>
      <div class="markalar">%s</div>
    </div>
  </section>""" % marka_html)

    parcalar.append("""
  <section aria-labelledby="taftri-h">
    <div class="sarmal">
      <h2 class="bolum-basligi" id="taftri-h">Ajans işleri</h2>
      <div class="taftri">
        <h3>Taftri</h3>
        <p>Ekip gerektiren işler — sürekli reklam yönetimi, içerik üretimi, uzun soluklu
          mağaza operasyonu — <a href="https://taftri.com/" rel="noopener">taftri.com</a>
          üzerinden yürüyor. Hizmet kapsamı ve teklif orada.</p>
      </div>
    </div>
  </section>""")

    parcalar.append(iletisim_bolumu())

    govde = "<main>%s\n</main>" % "".join(parcalar)
    return sayfa(baslik, aciklama, SITE + "/", "/", govde, [ld_kisi(), ld_site()])


def uygulama_listesi():
    baslik = "Shopify uygulamaları — %s" % AD
    aciklama = ("Shopify App Store için geliştirdiğim uygulamalar: hangi sorunu "
                "çözdükleri, ne yaptıkları ve kurulum bilgileri.")
    kb, kld = kirinti([("Ana sayfa", "/"), ("Uygulamalar", None)])
    kartlar = "".join(
        kart("/uygulamalar/%s/" % u["slug"],
             DURUM_ADI.get(u.get("durum", ""), "Uygulama"),
             u["ad"], u["ozet"], u.get("fiyat", ""))
        for u in UYGULAMALAR)
    liste_ld = ('{"@context":"https://schema.org","@type":"ItemList",'
                '"itemListElement":[%s]}' % ",".join(
                    '{"@type":"ListItem","position":%d,"name":"%s","url":"%s/uygulamalar/%s/"}'
                    % (n + 1, json_kacir(u["ad"]), SITE, u["slug"])
                    for n, u in enumerate(UYGULAMALAR)))
    govde = """<main>
  <div class="sarmal">%s</div>
  <header class="giris giris--ic">
    <div class="sarmal">
      <h1 class="ad ad--ic">Uygulamalar</h1>
      <p>Shopify App Store için geliştirdiğim uygulamalar. Her birinin sayfasında hangi
        sorunu çözdüğü, ne yaptığı ve hangi uçları kullandığı yazılı.</p>
    </div>
  </header>
  <section aria-label="Uygulama listesi">
    <div class="sarmal"><div class="kartlar">%s</div></div>
  </section>
%s
</main>""" % (kb, kartlar, iletisim_bolumu())
    return sayfa(baslik, aciklama, SITE + "/uygulamalar/", "/uygulamalar/",
                 govde, [kld, liste_ld])


def uygulama_sayfasi(u):
    baslik = "%s — Shopify uygulaması" % u["ad"]
    aciklama = duz(u["ozet"])[:155]
    yol = "/uygulamalar/%s/" % u["slug"]
    kb, kld = kirinti([("Ana sayfa", "/"), ("Uygulamalar", "/uygulamalar/"), (u["ad"], None)])

    durum = DURUM_ADI.get(u.get("durum", ""))
    parcalar = ["""
  <header class="giris giris--ic">
    <div class="sarmal">
      <h1 class="ad ad--ic">%s</h1>
      %s
      <p>%s</p>
      %s
    </div>
  </header>""" % (
        kacir(u["ad"]),
        ('<p class="durum">%s</p>' % durum) if durum else "",
        kacir(u["ozet"]),
        ('<p><a class="btn" href="%s" target="_blank" rel="noopener">App Store\'da aç</a></p>'
         % u["app_store"]) if u.get("app_store") else "")]

    if u.get("gorsel"):
        parcalar.append('\n  <div class="sarmal"><img class="gorsel" src="%s" alt="%s" '
                        'loading="lazy" /></div>'
                        % (u["gorsel"], kacir(u.get("gorsel_alt", u["ad"]))))

    parcalar.append("""
  <section aria-labelledby="sorun-h">
    <div class="sarmal">
      <h2 class="bolum-basligi" id="sorun-h">Hangi sorunu çözüyor</h2>
      <p class="bolum-giris" style="margin-bottom:0">%s</p>
    </div>
  </section>""" % kacir(u["sorun"]))

    parcalar.append("""
  <section aria-labelledby="cozum-h">
    <div class="sarmal">
      <h2 class="bolum-basligi" id="cozum-h">Ne yapıyor</h2>
      %s
      %s
      %s
    </div>
  </section>""" % (
        maddeler([kacir(m) for m in u["cozum"]]),
        rozetler(u.get("teknik", [])),
        ('<p style="margin-top:18px;color:var(--murekkep-3);font-size:15px">Fiyat: %s</p>'
         % kacir(u["fiyat"])) if u.get("fiyat") else ""))

    sss_html, sss_ld = sss_blok(u.get("sss", []), "sss-h")
    if sss_html:
        parcalar.append(sss_html)
    parcalar.append(iletisim_bolumu())

    yazilim_ld = ('{"@context":"https://schema.org","@type":"SoftwareApplication",'
                  '"name":"%s","applicationCategory":"BusinessApplication",'
                  '"operatingSystem":"Shopify","description":"%s",'
                  '"author":{"@type":"Person","name":"%s"}%s}'
                  % (json_kacir(u["ad"]), json_kacir(u["ozet"]), AD,
                     (',"url":"%s"' % u["app_store"]) if u.get("app_store") else ""))

    govde = '<main>\n  <div class="sarmal">%s</div>%s\n</main>' % (kb, "".join(parcalar))
    ldler = [kld, yazilim_ld]
    if sss_ld:
        ldler.append(sss_ld)
    return sayfa(baslik, aciklama, SITE + yol, "/uygulamalar/", govde, ldler)


def is_listesi():
    baslik = "Yapılmış işler — %s" % AD
    aciklama = ("Shopify mağazaları için yazdığım özel uygulamalar, tema özellikleri ve "
                "entegrasyonlar; her birinde başlangıç durumu ve ölçülmüş sonuç.")
    kb, kld = kirinti([("Ana sayfa", "/"), ("İşler", None)])
    kartlar = "".join(
        kart("/isler/%s/" % i["slug"], TUR_ADI.get(i.get("tur", ""), "İş"),
             i["baslik"], i["ozet"], i.get("musteri", ""))
        for i in ISLER)
    liste_ld = ('{"@context":"https://schema.org","@type":"ItemList",'
                '"itemListElement":[%s]}' % ",".join(
                    '{"@type":"ListItem","position":%d,"name":"%s","url":"%s/isler/%s/"}'
                    % (n + 1, json_kacir(i["baslik"]), SITE, i["slug"])
                    for n, i in enumerate(ISLER)))
    govde = """<main>
  <div class="sarmal">%s</div>
  <header class="giris giris--ic">
    <div class="sarmal">
      <h1 class="ad ad--ic">Yapılmış işler</h1>
      <p>Her kayıtta işin başlangıç durumu, ne yapıldığı ve mümkün olduğunda ölçülmüş
        sonucu yazılı. Rakam yoksa rakam yazılmıyor.</p>
    </div>
  </header>
  <section aria-label="İş listesi">
    <div class="sarmal"><div class="kartlar">%s</div></div>
  </section>
%s
</main>""" % (kb, kartlar, iletisim_bolumu())
    return sayfa(baslik, aciklama, SITE + "/isler/", "/isler/", govde, [kld, liste_ld])


def is_sayfasi(i):
    baslik = "%s — %s" % (i["baslik"], i["musteri"])
    aciklama = duz(i["ozet"])[:155]
    yol = "/isler/%s/" % i["slug"]
    kb, kld = kirinti([("Ana sayfa", "/"), ("İşler", "/isler/"), (i["baslik"], None)])

    musteri_html = kacir(i["musteri"])
    if i.get("musteri_url"):
        musteri_html = ('<a href="%s" target="_blank" rel="noopener">%s</a>'
                        % (i["musteri_url"], musteri_html))

    parcalar = ["""
  <header class="giris giris--ic">
    <div class="sarmal">
      <p class="rol">%s</p>
      <h1 class="ad ad--ic">%s</h1>
      <p>%s</p>
      <p style="font-size:16px">Müşteri: %s</p>
    </div>
  </header>""" % (kacir(TUR_ADI.get(i.get("tur", ""), "İş")), kacir(i["baslik"]),
                  kacir(i["ozet"]), musteri_html)]

    parcalar.append("""
  <section aria-labelledby="durum-h">
    <div class="sarmal">
      <h2 class="bolum-basligi" id="durum-h">Başlangıç durumu</h2>
      <p class="bolum-giris" style="margin-bottom:0">%s</p>
    </div>
  </section>""" % kacir(i["sorun"]))

    parcalar.append("""
  <section aria-labelledby="yapilan-h">
    <div class="sarmal">
      <h2 class="bolum-basligi" id="yapilan-h">Yapılan</h2>
      %s
      %s
    </div>
  </section>""" % (maddeler([kacir(m) for m in i["yapilan"]]),
                   rozetler(i.get("teknik", []))))

    if i.get("sonuc"):
        parcalar.append("""
  <section aria-labelledby="sonuc-h">
    <div class="sarmal">
      <h2 class="bolum-basligi" id="sonuc-h">Sonuç</h2>
      %s
    </div>
  </section>""" % maddeler([kacir(m) for m in i["sonuc"]]))

    parcalar.append(iletisim_bolumu())

    is_ld = ('{"@context":"https://schema.org","@type":"CreativeWork",'
             '"name":"%s","description":"%s","inLanguage":"tr-TR",'
             '"creator":{"@type":"Person","name":"%s"},'
             '"about":{"@type":"Organization","name":"%s"%s}}'
             % (json_kacir(i["baslik"]), json_kacir(i["ozet"]), AD,
                json_kacir(i["musteri"]),
                (',"url":"%s"' % i["musteri_url"]) if i.get("musteri_url") else ""))

    govde = '<main>\n  <div class="sarmal">%s</div>%s\n</main>' % (kb, "".join(parcalar))
    return sayfa(baslik, aciklama, SITE + yol, "/isler/", govde, [kld, is_ld])


def ozel_yazilim():
    baslik = "Shopify özel yazılım geliştirme — %s" % AD
    aciklama = ("Tek mağaza için Shopify uygulaması, tema özelliği, Admin API "
                "entegrasyonu ve toplu veri işleri. Kapsam, süreç ve teslim biçimi.")
    kb, kld = kirinti([("Ana sayfa", "/"), ("Özel yazılım", None)])

    kapsam_html = "".join('<div class="alan"><h3>%s</h3><p>%s</p></div>' % (kacir(b), kacir(m))
                          for b, m in OZEL_KAPSAM)
    surec_html = "".join('<div class="alan"><h3>%s</h3><p>%s</p></div>' % (kacir(b), kacir(m))
                         for b, m in SUREC)

    sss = [
        ("App Store uygulaması mı, mağazaya özel uygulama mı gerekiyor?",
         "Aynı ihtiyaç birden çok mağazada varsa ve satmayı düşünüyorsanız App Store. "
         "Sadece sizin iş akışınıza özel bir şeyse mağazaya özel uygulama hem daha hızlı "
         "hem daha ucuz olur; inceleme süreci de yoktur."),
        ("İş uygulama gerektirmiyorsa ne olur?",
         "Çoğu istek tema içinde çözülebiliyor. Uygulama kurmadan çözülebilecek bir işe "
         "uygulama yazmam; her uygulama mağazaya kalıcı bir bağımlılık ekler."),
        ("Canlı mağazada mı çalışıyorsunuz?",
         "Hayır. Tema işleri yayınlanmamış bir kopyada geliştirilir, önizleme adresinden "
         "doğrulanır, sonra canlıya alınır. Uygulama tarafında geliştirme mağazası kullanılır."),
        ("Toplu veri işlerinde geri dönüş var mı?",
         "Var. Değiştirilen alanların eski değerleri kimlikleriyle birlikte dosyaya yazılır "
         "ve geri yükleme script'i teslim edilir."),
        ("Kodun sahibi kim?",
         "Mağazaya özel işlerde kod sizindir; tema dosyaları ve uygulama kaynağı teslim "
         "edilir. App Store uygulamalarında kaynak bende kalır, siz aboneliği kullanırsınız."),
    ]
    sss_html, sss_ld = sss_blok(sss, "sss-h")

    hizmet_ld = ('{"@context":"https://schema.org","@type":"Service",'
                 '"name":"Shopify özel yazılım geliştirme",'
                 '"serviceType":"Shopify uygulama ve tema geliştirme",'
                 '"provider":{"@type":"Person","name":"%s","url":"%s/"},'
                 '"areaServed":"TR","description":"%s"}'
                 % (AD, SITE, json_kacir(aciklama)))

    govde = """<main>
  <div class="sarmal">%(kb)s</div>
  <header class="giris giris--ic">
    <div class="sarmal">
      <h1 class="ad ad--ic">Özel yazılım</h1>
      <p>App Store'a çıkmayan, tek bir mağaza için yazılan işler. Herkese uyması
        gerekmediği için kapsam dar tutulur, iş hızlı biter.</p>
    </div>
  </header>

  <section aria-labelledby="kapsam-h">
    <div class="sarmal">
      <h2 class="bolum-basligi" id="kapsam-h">Ne tür işler</h2>
      %(kapsam)s
    </div>
  </section>

  <section aria-labelledby="surec-h">
    <div class="sarmal">
      <h2 class="bolum-basligi" id="surec-h">Nasıl yürüyor</h2>
      %(surec)s
    </div>
  </section>
%(sss)s
%(iletisim)s
</main>""" % {"kb": kb, "kapsam": kapsam_html, "surec": surec_html,
              "sss": sss_html, "iletisim": iletisim_bolumu()}

    return sayfa(baslik, aciklama, SITE + "/ozel-yazilim/", "/ozel-yazilim/",
                 govde, [kld, hizmet_ld, sss_ld])


def dort_yuz_dort():
    ekler = ""
    if UYGULAMALAR:
        ekler += ' &middot; <a href="/uygulamalar/">Uygulamalar</a>'
    ekler += ' &middot; <a href="/ozel-yazilim/">Özel yazılım</a>'
    if ISLER:
        ekler += ' &middot; <a href="/isler/">İşler</a>'
    govde = """<main>
  <header class="giris">
    <div class="sarmal">
      <h1 class="ad">Sayfa bulunamadı</h1>
      <p>Aradığınız adres taşınmış ya da hiç var olmamış olabilir. Aşağıdakiler yerinde:</p>
      <p style="font-size:17px"><a href="/">Ana sayfa</a>%s</p>
    </div>
  </header>
</main>""" % ekler
    return sayfa("Sayfa bulunamadı — %s" % AD, "Aradığınız sayfa bulunamadı.",
                 SITE + "/404.html", "", govde, (), robots="noindex, follow")


# ---------------------------------------------------------------------------
# DESTEK DOSYALARI
# ---------------------------------------------------------------------------

def adresler():
    yollar = ["/", "/ozel-yazilim/"]
    if UYGULAMALAR:
        yollar.append("/uygulamalar/")
        yollar += ["/uygulamalar/%s/" % u["slug"] for u in UYGULAMALAR]
    if ISLER:
        yollar.append("/isler/")
        yollar += ["/isler/%s/" % i["slug"] for i in ISLER]
    return yollar


def sitemap():
    satirlar = ['<?xml version="1.0" encoding="UTF-8"?>',
                '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for yol in adresler():
        oncelik = "1.0" if yol == "/" else ("0.8" if yol.strip("/").count("/") == 0 else "0.7")
        satirlar += ["  <url>",
                     "    <loc>%s%s</loc>" % (SITE, yol),
                     "    <lastmod>%s</lastmod>" % BUGUN,
                     "    <changefreq>monthly</changefreq>",
                     "    <priority>%s</priority>" % oncelik,
                     "  </url>"]
    satirlar.append("</urlset>")
    return "\n".join(satirlar) + "\n"


def robots():
    return "User-agent: *\nAllow: /\n\nSitemap: %s/sitemap.xml\n" % SITE


def llms():
    satirlar = [
        "# %s" % AD,
        "",
        "> Shopify için yazılım geliştiricisi. App Store uygulamaları, mağazaya özel",
        "> uygulamalar, Liquid tema geliştirme ve Admin API entegrasyonları.",
        "",
        "## Sayfalar",
        "",
        "- [Ana sayfa](%s/): kim, ne geliştiriyor, çalışma yöntemi, markalar." % SITE,
        "- [Özel yazılım](%s/ozel-yazilim/): tek mağaza için geliştirme; kapsam, süreç, sık sorulanlar." % SITE,
    ]
    if UYGULAMALAR:
        satirlar.append("- [Uygulamalar](%s/uygulamalar/): App Store uygulamaları." % SITE)
        for u in UYGULAMALAR:
            satirlar.append("  - [%s](%s/uygulamalar/%s/): %s"
                            % (u["ad"], SITE, u["slug"], duz(u["ozet"])))
    if ISLER:
        satirlar.append("- [İşler](%s/isler/): yapılmış işler ve ölçülmüş sonuçları." % SITE)
        for i in ISLER:
            satirlar.append("  - [%s](%s/isler/%s/): %s — %s"
                            % (i["baslik"], SITE, i["slug"], i["musteri"], duz(i["ozet"])))
    satirlar += ["",
                 "## İletişim",
                 "",
                 "- WhatsApp / telefon: %s" % TELEFON_YAZI,
                 "- Ajans işleri: https://taftri.com/",
                 ""]
    return "\n".join(satirlar)


def favicon():
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64">'
            '<rect width="64" height="64" rx="12" fill="#3D5A4A"/>'
            '<text x="32" y="43" font-family="Georgia,serif" font-size="28" '
            'font-weight="600" fill="#F7F5F0" text-anchor="middle">MF</text></svg>\n')


# ---------------------------------------------------------------------------
# CALISTIR
# ---------------------------------------------------------------------------

def main():
    yaz("assets/stil.css", STIL)
    yaz("favicon.svg", favicon())

    yaz("index.html", ana_sayfa())
    yaz("ozel-yazilim/index.html", ozel_yazilim())

    if UYGULAMALAR:
        yaz("uygulamalar/index.html", uygulama_listesi())
        for u in UYGULAMALAR:
            yaz("uygulamalar/%s/index.html" % u["slug"], uygulama_sayfasi(u))

    if ISLER:
        yaz("isler/index.html", is_listesi())
        for i in ISLER:
            yaz("isler/%s/index.html" % i["slug"], is_sayfasi(i))

    yaz("404.html", dort_yuz_dort())
    yaz("sitemap.xml", sitemap())
    yaz("robots.txt", robots())
    yaz("llms.txt", llms())
    yaz("%s.txt" % INDEXNOW_ANAHTAR, INDEXNOW_ANAHTAR)

    print("Uretilen dosya: %d" % len(URETILEN))
    for y in URETILEN:
        print("  " + y)
    print("Sitemap adresi : %d" % len(adresler()))
    print("Uygulama: %d   Is: %d" % (len(UYGULAMALAR), len(ISLER)))


if __name__ == "__main__":
    main()
