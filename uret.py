# -*- coding: utf-8 -*-
"""
mftoktay.com sayfa ureticisi.

Kullanim:  python uret.py

Bu dosya sitenin TEK kaynagidir. Uretilen .html dosyalarini elle duzenleme —
bir sonraki calistirmada uzerine yazilir. Icerik degisikligi burada yapilir.

Yapi (her sayfada yapiskan ust menu + tam alt bilgi):

  /                       ana sayfa
  /gelistirme/            gelistirme alanlari — dort sayfaya dagitir
  /uygulama-gelistirme/   App Store uygulamasi
  /ozel-yazilim/          magazaya ozel uygulama
  /tema-gelistirme/       Liquid tema
  /entegrasyon/           Admin API, toplu veri, dis sistem
  /teknik/                teknik yaklasim
  /yontem/                surec ve olcum ornekleri
  /iletisim/              iletisim
  /uygulamalar/[slug]/    UYGULAMALAR listesi doluysa
  /projeler/[slug]/       PROJELER listesi doluysa

Ornek eklemek: UYGULAMALAR / PROJELER listesine bir sozluk ekle (sema asagida).
Liste bosken ilgili bolum, liste sayfasi ve menu ogesi hic uretilmez.
"""

import os
import re
from datetime import date

KOK = os.path.dirname(os.path.abspath(__file__))
SITE = "https://mftoktay.com"
BUGUN = date.today().isoformat()

AD = "M. Fehmi Toktay"
ROL = "Yazılım ve Shopify geliştiricisi"
TELEFON = "+905541386827"
TELEFON_YAZI = "+90 554 138 68 27"
INDEXNOW_ANAHTAR = "a4d17f2c9b6e485fa03c71d8e6b25904"


# ---------------------------------------------------------------------------
# IKONLAR — 24x24, stroke 1.5, currentColor
# ---------------------------------------------------------------------------

def _svg(ic):
    return ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" '
            'stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" '
            'aria-hidden="true" focusable="false">%s</svg>' % ic)


IKON = {
    "app": _svg('<rect x="3" y="3" width="7.5" height="7.5" rx="1.6"/>'
                '<rect x="13.5" y="3" width="7.5" height="7.5" rx="1.6"/>'
                '<rect x="3" y="13.5" width="7.5" height="7.5" rx="1.6"/>'
                '<path d="M17.25 13.9v6.7M13.9 17.25h6.7"/>'),
    "kutu": _svg('<path d="M12 2.8l8.2 4.1v10.2L12 21.2l-8.2-4.1V6.9z"/>'
                 '<path d="M3.8 6.9L12 11l8.2-4.1M12 11v10.2"/>'),
    "pencere": _svg('<rect x="2.8" y="4.2" width="18.4" height="15.6" rx="2.2"/>'
                    '<path d="M2.8 9.2h18.4"/><path d="M6.2 6.7h.01M9.1 6.7h.01"/>'),
    "baglanti": _svg('<circle cx="5.6" cy="12" r="2.6"/><circle cx="18.4" cy="12" r="2.6"/>'
                     '<path d="M8.2 12h7.6"/><path d="M13.2 9.2l2.8 2.8-2.8 2.8"/>'),
    "olcum": _svg('<path d="M3.5 20.5V9.8M9.8 20.5V4.4M16.1 20.5v-7.3M22 20.5H2"/>'),
    "kalkan": _svg('<path d="M12 2.9l7.4 2.9v5.6c0 4.4-3 8.1-7.4 9.7-4.4-1.6-7.4-5.3-7.4-9.7V5.8z"/>'
                   '<path d="M9.1 12.1l2 2 3.8-3.9"/>'),
    "geri": _svg('<path d="M3.5 8.6h6.1V2.5"/>'
                 '<path d="M4.6 15.2a8.3 8.3 0 1 0 .6-6"/>'),
    "surum": _svg('<path d="M6.6 4.2v10.1M6.6 21.1a2.9 2.9 0 1 0 0-5.8 2.9 2.9 0 0 0 0 5.8z"/>'
                  '<path d="M17.4 8.6a2.9 2.9 0 1 0 0-5.8 2.9 2.9 0 0 0 0 5.8z"/>'
                  '<path d="M17.4 8.6v3.1c0 2-1.6 3.6-3.6 3.6h-3"/>'),
    "katman": _svg('<path d="M12 2.9l9 4.6-9 4.6-9-4.6z"/>'
                   '<path d="M3 12.4l9 4.6 9-4.6M3 16.9l9 4.6 9-4.6"/>'),
}

HIZMET_IKON = {
    "web-gelistirme": "pencere",
    "uygulama-gelistirme": "app",
    "ozel-yazilim": "kutu",
    "tema-gelistirme": "katman",
    "entegrasyon": "baglanti",
}


# ---------------------------------------------------------------------------
# VERI — ORNEKLER
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
#   "kod":         ("Baslik", "graphql", "..."),   #   kod ornegi; bossa basilmaz
#   "kod_not":     "Kodun altina dusen aciklama.", #   opsiyonel
#   "gorsel":      "/assets/uygulama-slug.png",    #   bossa gorsel basilmaz
#   "gorsel_alt":  "Ekran goruntusu: ...",         #   gorsel varsa zorunlu
#   "sss":         [("Soru?", "Cevap.")],          #   bossa SSS bolumu basilmaz
# }
UYGULAMALAR = []

# Projeler / vaka ornekleri.
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
#   "kod":         ("Baslik", "js", "..."),        #   opsiyonel
# }
PROJELER = [
    {
        "slug": "blackbork-sapka-tasarim-kurucusu",
        "baslik": "Tarayıcıda çalışan şapka tasarım kurucusu",
        "musteri": "BlackBörk USA",
        "musteri_url": "https://blackborkusa.com/pages/make-your-cap",
        "tur": "tema",
        "ozet": ("Müşteri şapkayı ve patch'i seçiyor; önizleme patch'i cırt cırt pedinin "
                 "üstüne perspektifle oturtuyor."),
        "sorun": ("Türkiye mağazasındaki tasarım aracı bir Shopify uygulamasıydı ve ABD "
                  "mağazasında kurulu değildi; uygulama kurulumu API üzerinden yapılamıyor. "
                  "İlk denemede patch tek bir sabit yüzdeyle basılıyordu — şapka fotoğrafları "
                  "3/4 açıdan çekildiği için ön panel ekranda dikdörtgen değil, perspektifte "
                  "bir yamuk. Düz basılan patch pedin üstüne oturmuyordu."),
        "yapilan": [
            "Uygulama yerine tema içinde çalışan bir kurucu yazıldı; mağazada aylık ücretli "
            "uygulama bağımlılığı yok.",
            "Kurucudaki 112 şapka fotoğrafının her birinde cırt cırt pedinin dört köşesi "
            "ölçülüp ayrı bir veri dosyasına yazıldı; tarayıcı bu dörtgene homografi kurup "
            "patch'i matrix3d ile basıyor.",
            "Ölçüm için üç yöntem denenip elendi: boş/patch'li fotoğraf farkı (çiftler aynı "
            "çekim değil), serbest hizalama (dörtgeni bozup patch'i şapkanın dışına taşıyor) "
            "ve serbest şekil araması (32 fotoğrafta yanlış şekil kazandı). Çalışan yöntem "
            "şekli kilitleyip yalnız kaydırma ve ölçek aramak oldu.",
            "Patch fotoğrafları beyaz fonda geliyor; tarayıcıda kanvasla beyaz saydamlaştırılıp "
            "içeriğe kırpılıyor, kanvas reddedilirse sabit kırpma yedeğine düşüyor.",
            "Ürün sayfasındaki “tasarla” butonu sessizce ölüydü: koleksiyon eşlemeleri başka "
            "mağazanın adreslerini taşıyordu, URL alanları boştu ve adresin tamamı URL "
            "kodlandığı için JS yüklenmeden tıklanınca 404 veriyordu.",
            "Tek seçimli panelde ilk seçimden sonra bütün kartların artı butonu kilitleniyordu; "
            "müşteri seçimi değiştirmek için önce eskisini elle çıkarmak zorundaydı.",
        ],
        "sonuc": [
            "Önizlemede eski patch'in ekranda kaldığı süre 192 ms'den 0–16 ms'ye indi "
            "(masaüstü ve 375 px mobil).",
            "Izgara her tıkta baştan yazılmak yerine yerinde güncelleniyor; tıklamanın "
            "senkron maliyeti 65–69 ms.",
            "Patch kesimi ~39 ms sürüyor ve karta imleç gelince önceden yapılıp önbelleğe alınıyor.",
            "Kurucu tema dosyası olarak çalışıyor: dış uygulama, aylık ücret ve veri "
            "bağımlılığı yok.",
        ],
        "teknik": ["Liquid", "JavaScript", "Canvas", "matrix3d", "Shopify CDN"],
    },
    {
        "slug": "omerhas-urun-sayfasi-ve-katalog",
        "baslik": "Ürün sayfası, sepet çekmecesi ve katalog düzeni",
        "musteri": "Ömer Has Kuyumculuk",
        "musteri_url": "https://omerhaskuyumculuk.com/",
        "tur": "tema",
        "ozet": ("Satın alma butonu yukarı taşındı, sabit çubuğun yanlış varyant hatası "
                 "kapandı, katalog düzeni sadeleşti."),
        "sorun": ("Mobilde “Sepete Ekle” butonu 1147. pikseldeydi; müşteri bir buçuk ekran "
                  "boyunca hiçbir satın alma tetikleyicisi görmüyordu. Sabit sepet çubuğu "
                  "varyant kimliğini sayfa yüklenirken okuyup sabitliyordu, harf kolyede "
                  "müşteri “Ç” seçince sepete “A” giriyordu. Katalog tarafında ürün türü "
                  "alanında 71 farklı değer vardı ve sayılar gramaj değil sıra numarasıydı."),
        "yapilan": [
            "Fiyat kırılımı ve ürün künyesi bloklarının yeri değişti: bunlar karar öncesi "
            "değil karar sonrası bilgi, satın alma butonunun altına alındı.",
            "Sabit çubuk varyant kimliğini tıklama anında asıl ürün formundan okuyacak "
            "şekilde yeniden yazıldı; fiyat, varyant adı ve stok durumu da asıl alandan aynalanıyor.",
            "Sepet çekmecesinde sabit bloklar ürün listesinden yer çalıyordu; sabit kalması "
            "gerekmeyen her şey kaydırılabilir alanın içine alındı.",
            "95 ürünün tamamında gizli bir ikinci başlık vardı — ürünün kendi adresine link "
            "veren, yüksekliği sıfır bir <h2 class=\"h1\">. Kaldırıldı, sayfada tek H1 bırakıldı.",
            "Görünür kırıntı yolu ve BreadcrumbList birlikte kuruldu; ikisi aynı yolu gösteriyor.",
            "Ürün türü alanı 6 temiz kategoriye indirildi; eski değerler silinmeden önce geri "
            "dönüş için ayrı bir metafield'a yazıldı.",
            "Birebir aynı ürün kümesini gösteren altı kopya koleksiyon kapatıldı: önce 301 "
            "yönlendirmesi kuruldu, sonra silindi, sonra yönlendirmeler doğrulandı.",
            "Tasarım tarafında iki harfli monogram favicon, güven şeridi, eşikli hediye "
            "mekaniği ve kaynağın kendi panelini gömen canlı altın fiyat bölümü yapıldı.",
        ],
        "sonuc": [
            "Mobilde satın alma butonu 1147. pikselden 948. piksele çıktı.",
            "Çapraz satış bölümü 6749. pikselden 2552. piksele (masaüstünde 1733) taşındı.",
            "Ürün türü 71 farklı değerden 6 kategoriye indi; Google Shopping ve Meta katalog "
            "eşleştirmesi düzeldi.",
            "Menüdeki 32 linkin 11'i sıfır ürün döndürüyordu; boş kategoriler menüden çıkarıldı.",
            "95 ürüne SEO başlık ve açıklaması, 340 görsele alt metin yazıldı.",
        ],
        "teknik": ["Liquid", "JavaScript", "Admin GraphQL API", "Metafield",
                   "URL Redirect", "JSON-LD"],
        "kod": ("Sabit çubuk varyant kimliğini tıklama anında okur", "js",
                """// Kimlik sayfa yuklenirken sabitlenirse, musteri varyant
// degistirdiginde sepete ESKI varyant gider. Olculen kanit:
// formda 49143197565147, cubukta 48748885934299.
const form = document.querySelector('product-form form [name="id"]');

dugme.addEventListener('click', function () {
  const varyantId = form && form.value;
  if (!varyantId) return;              // form yoksa hic denemeyelim
  sepeteEkle(varyantId, adetAlani.value);
});"""),
        "kod_not": ("Bu hata sipariş gelene kadar kimseye görünmüyor. Kod okuyarak değil, "
                    "formdaki değerle çubuğun gönderdiği değeri karşılaştırarak bulunuyor."),
    },
    {
        "slug": "modaneslie-renk-varyanti-gorselleri",
        "baslik": "Renk varyantlarının ürün sayfasında ayrı görünmesi",
        "musteri": "Moda Neslie",
        "musteri_url": "https://modaneslie.com/",
        "tur": "tema",
        "ozet": ("Müşteri rengi seçince galeri o rengin fotoğrafına geçiyor; 22 fotoğraf "
                 "arasında gezinmiyor."),
        "sorun": ("Deri cüzdan ve kartlıklar tek üründe sekiz renk varyantıyla satılıyor, "
                  "ama her rengin kendi çekimi var. Bütün fotoğraflar tek galeride arka "
                  "arkaya sıralanıyordu: müşteri “Haki” seçiyor, ekranda siyah cüzdan "
                  "duruyordu. Doğru fotoğrafı görmek için yirmiden fazla görsel arasında "
                  "gezinmesi gerekiyordu — mobilde bu, satın alma öncesindeki en büyük "
                  "tereddüt kaynağı."),
        "yapilan": [
            "Her renk için öncü fotoğraf belirlendi ve doğrudan o renk varyantına bağlandı; "
            "renk seçildiği anda galeri o fotoğrafa geçiyor.",
            "Galerideki sıra renk gruplarına göre düzenlendi: her rengin öncü karesi kendi "
            "grubunun başında duruyor, detay çekimleri arkasından geliyor.",
            "Renk adları varyant başlığıyla birebir eşleştirildi; “Siyah / Bordo” gibi çift "
            "renkler ayrı varyant olarak kaldı, tek renge indirgenmedi.",
            "Bağlama Admin API üzerinden yapıldı — panelden tek tek sürükleme yerine kayıtla, "
            "böylece aynı düzen diğer ürünlere tekrarlanabiliyor.",
        ],
        "sonuc": [
            "Sekiz rengin sekizi de kendi fotoğrafına bağlandı; renk seçimi galeriyi anında "
            "değiştiriyor.",
            "Müşteri doğru rengi görmek için 22 fotoğrafın içinde gezinmiyor.",
        ],
        "teknik": ["Shopify Admin API", "Liquid", "Varyant medyası"],
    },
]

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


# ---------------------------------------------------------------------------
# VERI — OLCULMUS SAYILAR (serit)
# ---------------------------------------------------------------------------

# Hepsi gercek magazalarda olculdu. Uydurma sayi eklenmez.
SERIT = [
    ("1147 → 948", "px", "satın alma butonu mobilde yukarı taşındı"),
    ("1811 → 1064", "px", "detay paneli kapalı başlatılınca"),
    ("71 → 6", "kategori", "ürün türü alanı sadeleştirildi"),
    ("13", "marka", "birlikte çalışılan mağaza"),
]


# ---------------------------------------------------------------------------
# VERI — CALISILAN PLATFORM YUZEYLERI
# ---------------------------------------------------------------------------

YUZEYLER = [
    ("Admin GraphQL API", "ürün, varyant, sipariş, metafield okuma ve yazma"),
    ("Bulk Operations", "binlerce kayıtlık iş; sonuç JSONL olarak indirilir"),
    ("Webhooks", "olay yakalama, HMAC doğrulama, idempotent işleme"),
    ("OAuth · Billing API", "kurulum akışı, kapsam yönetimi, abonelik ücretlendirmesi"),
    ("App Bridge · Polaris", "yönetim paneli içinde açılan gömülü arayüz"),
    ("Liquid · Online Store 2.0", "bölüm ve blok yazımı, tema editöründen yönetim"),
    ("Storefront · Ajax API", "sepet işlemleri, tema içi dinamik davranış"),
    ("Metafield · Metaobject", "ürün künyesi ve yapılandırılmış veri"),
    ("URL Redirect", "geçişlerde yönlendirme haritası"),
    ("Theme CLI", "yayınlanmamış temada geliştirme, önizleme, canlıya alma"),
]


# ---------------------------------------------------------------------------
# KOD ORNEKLERI
# ---------------------------------------------------------------------------

KOD_HERO = """query VaryantDurumu($id: ID!) {
  productVariant(id: $id) {
    sku
    inventoryQuantity
    price
    product {
      title
      vendor
    }
  }
}"""

KOD_BULK = """mutation {
  bulkOperationRunQuery(
    query: \"\"\"
    {
      products {
        edges {
          node {
            id
            title
            variants { edges { node { id sku inventoryQuantity } } }
          }
        }
      }
    }
    \"\"\"
  ) {
    bulkOperation { id status }
    userErrors { field message }
  }
}"""

KOD_HMAC = """const gelen = req.get('X-Shopify-Hmac-Sha256') || '';
const hesaplanan = crypto
  .createHmac('sha256', process.env.SHOPIFY_API_SECRET)
  .update(hamGovde, 'utf8')
  .digest('base64');

const a = Buffer.from(hesaplanan, 'base64');
const b = Buffer.from(gelen, 'base64');

// uzunluk farkliysa timingSafeEqual firlatir, once onu ele
if (a.length !== b.length || !crypto.timingSafeEqual(a, b)) {
  return res.status(401).send();
}"""

KOD_BOLUM = """{%- comment -%}
  Isaret ettigi kayit yoksa blok hic basilmaz.
  Bos render eden blok aylarca fark edilmez.
{%- endcomment -%}

{%- assign hediye = all_products[section.settings.hediye_handle] -%}

{%- if hediye != blank and hediye.available -%}
  <div class="hediye" data-esik="{{ section.settings.esik }}">
    <p>{{ section.settings.mesaj }}</p>
  </div>
{%- endif -%}"""


# ---------------------------------------------------------------------------
# VERI — GELISTIRME SAYFALARI
# ---------------------------------------------------------------------------

HIZMETLER = [
    {
        "slug": "web-gelistirme",
        "ad": "Web sitesi ve uygulaması",
        "baslik": "Web sitesi ve web uygulaması geliştirme",
        "aciklama": ("Kurumsal site, açılış sayfası, panel ve iç araçlar. Arama motoru "
                     "altyapısı kurulu teslim edilir; içerik tek kaynaktan üretilir."),
        "ozet": "Kurumsal site, açılış sayfası, panel ve iç araçlar.",
        "giris": [
            "E-ticaret dışında kalan işler. Kurumsal site, açılış sayfası, iç kullanım için "
            "panel ve araçlar; bir de bunların arkasındaki içerik üretim düzeni.",
            "Site teslim edildiğinde arama motorunun ihtiyaç duyduğu her şey yerinde olur: "
            "site haritası, robots, yapısal veri, kırıntı yolu, özel 404 ve yeni sayfaları "
            "arama motorlarına anında bildiren <strong>IndexNow</strong> bağlantısı.",
        ],
        "kapsam_basligi": "Neleri kapsıyor",
        "kapsam": [
            ("Kurumsal site ve açılış sayfası",
             "Hızlı, mobil öncelikli, erişilebilir sayfalar. Dokunma hedefleri, kontrast "
             "oranları ve satır uzunlukları tahmine değil ölçüme göre ayarlanır."),
            ("Panel ve iç araçlar",
             "Ekibin her seferinde geliştirici çağırmadan iş görebildiği yönetim ekranları, "
             "raporlar ve toplu düzenleme araçları."),
            ("Arama motoru altyapısı",
             "Site haritası, robots, kanonik adres, JSON-LD yapısal veri, kırıntı yolu, özel "
             "404 sayfası ve IndexNow bildirimi. Bunlar sonradan eklenen süs değil, kurulumun "
             "parçası."),
            ("İçerik üretim düzeni",
             "Sayfalar tek kaynaktan üretilir; yeni bir kayıt eklendiğinde menü, liste sayfası, "
             "detay sayfası, site haritası ve makine okunur içerik dosyası kendiliğinden "
             "güncellenir. Elle bakım gerekmez."),
        ],
        "teknik": ["HTML · CSS · JavaScript", "Python", "JSON-LD", "Sitemap · robots",
                   "IndexNow", "Git"],
        "sss": [
            ("Hazır bir tema ya da site kurucusu kullanıyor musunuz?",
             "Hayır. Kurucuların ürettiği sayfalar hem ağır oluyor hem kontrol sizde olmuyor. "
             "Sayfalar tek kaynaktan üretiliyor ve kaynak sizde kalıyor."),
            ("Siteyi sonra kendim güncelleyebilir miyim?",
             "Evet. İçerik tek bir kaynak dosyada durur; oraya bir kayıt eklemek yeterli, "
             "gerisi kendiliğinden üretilir. Nasıl yapılacağı yazılı teslim edilir."),
            ("Nerede barındırılıyor?",
             "Statik sitelerde barındırma maliyeti pratikte sıfıra iniyor. Mevcut altyapınız "
             "varsa oraya kurulur; yoksa uygun olanı birlikte seçeriz."),
            ("Arama motoruna ne zaman girer?",
             "Yayına alındığı gün site haritası gönderilir ve IndexNow bildirimi yapılır. "
             "Sonrası arama motorunun kendi takvimi; kimse gün veremez."),
        ],
    },
    {
        "slug": "uygulama-gelistirme",
        "ad": "App Store uygulaması",
        "baslik": "Shopify App Store uygulaması geliştirme",
        "aciklama": ("Shopify App Store için uygulama geliştirme: OAuth, gömülü arayüz, "
                     "Admin GraphQL API, webhook, faturalama ve inceleme süreci."),
        "ozet": "Herkese açık, mağazaya kurulup abonelikle kullanılan uygulama.",
        "giris": [
            "App Store uygulaması tek bir mağazaya değil bütün mağazalara yazılır. "
            "İşin zor kısmı özellikte değil çerçevede: kurulum, yetkilendirme, faturalama "
            "ve zorunlu veri uçları Shopify'ın kendi kurallarına uymak zorunda.",
            "Aynı ihtiyaç birden çok mağazada varsa ve bunu satmayı düşünüyorsanız doğru "
            "yol budur. Tek mağazaya özel bir işse "
            "<a href=\"/ozel-yazilim/\">özel yazılım</a> hem daha hızlı hem daha ucuz olur.",
        ],
        "kapsam_basligi": "Neleri kapsıyor",
        "kapsam": [
            ("Yetkilendirme ve oturum",
             "OAuth akışı, erişim kapsamlarının dar tutulması, oturum saklama ve yenileme. "
             "Geniş kapsam isteyen uygulama hem inceleme aşamasında geri döner hem mağaza "
             "sahibini tedirgin eder — istenen her kapsamın kullanıldığı yer gösterilebilmeli."),
            ("Gömülü arayüz",
             "Yönetim panelinin içinde açılan arayüz. Panelin kendi görsel diliyle yazılır, "
             "oturum belirteci akışı App Bridge üzerinden yürür; müşteri uygulamadan "
             "çıktığını hissetmez."),
            ("Admin API ve toplu işlemler",
             "Ürün, varyant, sipariş ve metafield okuma-yazma. Binlerce kayıtlık işler tek "
             "tek istekle değil toplu işlem uçlarıyla yürür; sorgu maliyeti ve hız limiti "
             "yönetimi ile kaldığı yerden devam etme baştan kurulur."),
            ("Webhook ve zorunlu uçlar",
             "Sipariş, ürün ve uygulama kaldırma olayları için webhook; ayrıca üç zorunlu "
             "veri ucu: müşteri verisi talebi, müşteri verisi silme, mağaza verisi silme. "
             "Bu üçü olmadan uygulama yayına alınmıyor."),
            ("Faturalama",
             "Abonelik ya da kullanım bazlı ücretlendirme Shopify'ın kendi faturalama API'si "
             "üzerinden kurulur; deneme süresi ve plan değişimi dahil. Dışarıdan ödeme almak "
             "kural ihlali."),
            ("Listeleme ve inceleme",
             "Uygulama sayfasının metni, görselleri, kurulum akışının test edilmesi ve "
             "incelemeden dönen geri bildirimlerin kapatılması."),
        ],
        "teknik": ["Admin GraphQL API", "Bulk Operations", "OAuth", "App Bridge",
                   "Polaris", "Billing API", "Webhook"],
        "kod": ("Binlerce ürünü tek istekle çekmek", "graphql", KOD_BULK),
        "kod_not": ("Toplu işlem sonucu JSONL dosyası olarak indirilir. Aynı veriyi sayfa "
                    "sayfa çekmek hem hız limitini yakar hem yarıda kalırsa nereden devam "
                    "edeceğini bilemezsin."),
        "sss": [
            ("Uygulama ne kadar sürede yayına girer?",
             "Geliştirme süresi kapsama göre değişir. Yayın tarafında Shopify'ın kendi "
             "inceleme süreci var; süresi başvuruya göre değişiyor ve kimse tarafından "
             "garanti edilemez. Vakit kaybettiren şey genelde inceleme değil, incelemeden "
             "dönen eksikler oluyor."),
            ("Gömülü mü olmalı?",
             "Yönetim paneli içinde çalışan uygulamalar hem daha çok kuruluyor hem "
             "listelemede avantajlı. Panelin dışında çalışmasını gerektiren özel bir durum "
             "yoksa gömülü yazıyorum."),
            ("Uygulama kaldırılınca veriye ne oluyor?",
             "Kaldırma olayı webhook ile yakalanır, mağazanın verisi zorunlu süre içinde "
             "silinir. Bu hem kural gereği hem müşteriye açıkça söylenmesi gereken bir şey."),
            ("Kaynak kod kimde kalıyor?",
             "App Store uygulamalarında kaynak bende kalır, siz aboneliği kullanırsınız. "
             "Kaynağın size geçmesi gereken işler mağazaya özel uygulama olarak yürür."),
        ],
    },
    {
        "slug": "ozel-yazilim",
        "ad": "Mağazaya özel uygulama",
        "baslik": "Shopify özel yazılım geliştirme",
        "aciklama": ("Tek mağaza için Shopify uygulaması: özel iş akışları, bayi paneli, "
                     "fiyat ve stok senkronu. Kaynak kod teslim edilir."),
        "ozet": "App Store'a çıkmayan, tek mağaza için yazılan uygulama.",
        "giris": [
            "App Store'a çıkmayan, tek bir mağaza için yazılan uygulama. Herkese uyması "
            "gerekmediği için kapsam dar tutulur, inceleme süreci yoktur, iş hızlı biter.",
            "Kod sizindir: kaynak, kurulum belgesi ve hangi kapsamların neden istendiği "
            "yazılı olarak teslim edilir.",
        ],
        "kapsam_basligi": "Ne tür işler",
        "kapsam": [
            ("Özel iş akışları",
             "Sipariş sonrası otomatik adımlar, onay zincirleri, koşullu etiketleme, iç "
             "bildirimler. Mağazanın kendi çalışma biçimine göre yazılır — hazır "
             "uygulamaların yapamadığı kısım genelde burasıdır."),
            ("Bayi ve toptan paneli",
             "Müşteri grubuna göre fiyat, minimum adet, cari bakiye görünümü, kuruma özel "
             "katalog ve sipariş formu."),
            ("Fiyat ve stok senkronu",
             "Dış bir kaynaktan gelen fiyat ve stok verisinin düzenli aktarımı. Çakışma, "
             "kısmi başarısızlık ve yeniden deneme durumları baştan tanımlanır."),
            ("Panel içi araçlar",
             "Yönetim panelinden çalıştırılan toplu düzenleme, rapor ve kontrol araçları. "
             "Her seferinde geliştirici çağırmadan iş görülebilsin diye."),
        ],
        "teknik": ["Admin GraphQL API", "Webhook", "Metafield", "Bulk Operations",
                   "Custom App"],
        "sss": [
            ("App Store uygulaması mı, mağazaya özel mi gerekiyor?",
             "Aynı ihtiyaç birden çok mağazada varsa ve satmayı düşünüyorsanız App Store. "
             "Sadece sizin iş akışınıza özel bir şeyse mağazaya özel uygulama hem daha "
             "hızlı hem daha ucuz olur; inceleme süreci de yoktur."),
            ("İş uygulama gerektirmiyorsa ne olur?",
             "Çoğu istek tema içinde çözülebiliyor. Uygulama kurmadan çözülebilecek bir işe "
             "uygulama yazmam; her uygulama mağazaya kalıcı bir bağımlılık ekler."),
            ("Kodun sahibi kim?",
             "Mağazaya özel işlerde kod sizindir. Kaynak, kurulum belgesi ve gerekli erişim "
             "bilgileri teslim edilir."),
            ("Uygulamayı sonra App Store'a taşıyabilir miyiz?",
             "Taşınabilir, ama baştan öyle yazılmadıysa çerçeve kısmı yeniden kurulur. "
             "Böyle bir ihtimal varsa başlarken söyleyin; yapı ona göre kurulsun."),
        ],
    },
    {
        "slug": "tema-gelistirme",
        "ad": "Tema geliştirme",
        "baslik": "Shopify tema geliştirme — Liquid",
        "aciklama": ("Shopify temasına özellik ekleme, bölüm ve blok yazımı, hız ve dönüşüm "
                     "düzeltmeleri. Tema editöründen yönetilebilir kurulum."),
        "ozet": "Liquid tarafında bölüm ve blok yazımı, mevcut temaya özellik ekleme.",
        "giris": [
            "Mağazanın görünen tarafı. Uygulama kurmadan çözülebilecek işlerin çoğu burada "
            "çözülür — hem daha hızlı hem mağazaya kalıcı bağımlılık eklemez.",
            "Yazdığım her bölüm <strong>tema editöründen yönetilebilir</strong> olur. Kod "
            "bilmeyen biri metni, görseli, eşiği değiştiremiyorsa iş yarım kalmıştır.",
        ],
        "kapsam_basligi": "Neleri kapsıyor",
        "kapsam": [
            ("Ürün sayfası düzeni",
             "Blok sırası, satın alma butonunun konumu, künye ve fiyat kırılımı, sabit sepet "
             "çubuğu. Karar öncesi bilgi yukarı, karar sonrası bilgi aşağı. Sabit çubuk "
             "varyant kimliğini tıklama anında okur — yükleme anında sabitlerse müşteri "
             "başka varyant seçtiğinde sepete yanlış ürün girer."),
            ("Sepet ve çapraz satış",
             "Sepet çekmecesinde tamamlayıcı ürün önerisi, eşikli hediye mekaniği, kargo "
             "eşiği barı. Eşik yoksa uydurma bar koymam; eşiğin altına düşünce hediyenin "
             "sepetten otomatik çıkması bütün kurgunun en kritik satırıdır."),
            ("Bölüm ve blok yazımı",
             "Ayarları tema editöründen yönetilen yeni bölümler. İşaret ettiği kayıt "
             "silinmişse blok hiç basılmaz — sessizce boş render eden blok bırakmam."),
            ("Hız ve düzen kayması",
             "Görsel boyutlandırma, kart ızgarasına göre doğru boyut isteme, gereksiz üçüncü "
             "parti script temizliği, asenkron içeriğe yer ayırarak düzen kaymasının önlenmesi."),
        ],
        "teknik": ["Liquid", "Online Store 2.0", "Ajax API", "Theme CLI", "JSON şablon"],
        "kod": ("Boş render eden blok bırakmamak", "liquid", KOD_BOLUM),
        "kod_not": ("Bir mağazada silinmiş bir ürüne işaret eden hediye bloğu aylarca "
                    "sessizce boş basmıştı. Koşul olmadan yazılan her referanslı blok aynı "
                    "riski taşır."),
        "sss": [
            ("Tema güncellenince yaptıklarınız kaybolur mu?",
             "Temanın kendi dosyalarına yapılan yamalar güncellemede gider. Bu yüzden eklenen "
             "özellikler mümkün olduğunca ayrı bölüm ve snippet dosyalarında durur; hangi "
             "dosyaya hangi çapa ile yama yapıldığı yazılı teslim edilir."),
            ("Canlı temada mı çalışıyorsunuz?",
             "Hayır. Yayınlanmamış bir kopyada geliştirilir, önizleme adresinden doğrulanır, "
             "sonra canlıya alınır. Canlıya taşırken dosyalar düz kopyalanmaz — tema bu arada "
             "değişmiş olabilir, mevcut dosyalara çapa bazlı yama uygulanır."),
            ("Hangi temalarla çalışıyorsunuz?",
             "Online Store 2.0 temalarının hepsiyle. Eski nesil temalarda da çalışıyorum ama "
             "orada bölüm desteği kısıtlı olduğu için iş daha uzun sürüyor."),
            ("Değişikliğin işe yaradığını nasıl anlıyoruz?",
             "Öncesi ve sonrası aynı yöntemle ölçülüyor. Ne ölçtüğüm "
             "<a href=\"/yontem/\">yöntem sayfasında</a> yazılı."),
        ],
    },
    {
        "slug": "entegrasyon",
        "ad": "Entegrasyon ve otomasyon",
        "baslik": "Shopify entegrasyon ve toplu veri işleri",
        "aciklama": ("Muhasebe, kargo, ERP ve pazaryeri entegrasyonları; toplu ürün, fiyat, "
                     "stok ve metafield güncellemeleri; platform geçişi."),
        "ozet": "Admin API üzerinden dış sistem bağlantısı ve toplu veri işleri.",
        "giris": [
            "Mağazanın dışarıyla konuştuğu taraf. Muhasebe, kargo, ERP ve pazaryeri "
            "bağlantıları; bir de kimsenin görmediği ama katalog kalitesini belirleyen toplu "
            "veri işleri.",
            "Buradaki asıl risk hata değil, <strong>sessiz hata</strong>: bir alan yanlış "
            "yazılır, kimse fark etmez, aylar sonra Google eşleştirmesi tutmaz. Bu yüzden her "
            "toplu iş loglanır ve geri alınabilir kurulur.",
        ],
        "kapsam_basligi": "Neleri kapsıyor",
        "kapsam": [
            ("Dış sistem bağlantısı",
             "Muhasebe, e-fatura, kargo, ERP ve pazaryeri entegrasyonları. Webhook kurulumu, "
             "imza doğrulama, hata durumunda tekrar deneme, kuyruk ve log."),
            ("Toplu ürün ve fiyat işleri",
             "Binlerce kayıtta başlık, açıklama, etiket, fiyat, varyant ve metafield "
             "güncellemesi. İş gruplar hâlinde, log dosyasına yazarak yürür; yarıda kalırsa "
             "kaldığı yerden devam eder."),
            ("Platform geçişi",
             "Başka bir platformdan Shopify'a taşıma. Geçişte asıl mesele veri değil "
             "yönlendirme haritası — eski adresler yenisine bağlanmazsa arama sıralaması gider."),
            ("Katalog ve veri düzeni",
             "Ürün türü, kategori, etiket ve koleksiyon kuralları. Kopya içerik üreten "
             "koleksiyonların temizlenmesi, görsel alt metinleri, ürün künyesinin metaveriye "
             "bağlanması. Bir katalogda ürün türü alanında 71 farklı değer bulmuştum; sayılar "
             "gramaj değil sıra numarasıydı ve katalog eşleştirmesini kırıyordu."),
        ],
        "teknik": ["Admin GraphQL API", "Bulk Operations", "Webhook", "URL Redirect",
                   "Metafield", "CSV / feed"],
        "kod": ("Webhook imzası doğrulanmadan hiçbir şey işlenmez", "js", KOD_HMAC),
        "kod_not": ("İmza doğrulanmayan bir webhook ucu, herkesin veri yazabildiği açık bir "
                    "kapıdır. Ayrıca aynı olay birden çok kez gelebilir — işlem idempotent "
                    "yazılır, ikinci sefer bir şey değiştirmez."),
        "sss": [
            ("Kaç ürüne kadar çalışıyor?",
             "Sayı sınırı yok. Binlerce kayıtlık işlerde tek tek istek yerine toplu işlem "
             "uçları kullanılıyor, sorgu maliyeti ve hız limiti yönetimi baştan kuruluyor."),
            ("Bir şey yanlış giderse geri alınabilir mi?",
             "Evet. Değiştirilen alanların eski değerleri kimlikleriyle birlikte dosyaya "
             "yazılır ve geri yükleme script'i teslim edilir. Yedek almadan toplu iş başlatmam."),
            ("Koleksiyon veya sayfa silinecekse ne oluyor?",
             "Önce 301 yönlendirmesi kurulur, sonra silinir, sonra yönlendirmenin çalıştığı "
             "doğrulanır. Shopify bir yönlendirmeyi yalnız o adres başka türlü açılmadığında "
             "devreye sokar; sıra bozulursa yönlendirme uyur ya da adres bir süre 404 verir."),
            ("Entegrasyonun çalıştığını nasıl takip ediyoruz?",
             "Her iş log tutar. Hata durumunda tekrar deneme ve bildirim kurulur; sessizce "
             "duran entegrasyon en pahalı hatadır."),
        ],
    },
]

HIZMET_SLUG = {h["slug"]: h for h in HIZMETLER}

# Alt bilgide "Shopify" basligi altinda listelenecek alanlar.
SHOPIFY_ALANLARI = {"uygulama-gelistirme", "ozel-yazilim", "tema-gelistirme"}

# (ad, adres, sektor, monogram) — sektorler markalarin kendi sitelerinden okundu.
MARKALAR = [
    ("BlackBörk USA", "https://blackborkusa.com/", "Şapka · ABD", "BB"),
    ("BlackBörk TR", "https://blackbork.com.tr/", "Şapka · Türkiye", "BB"),
    ("Ömer Has Kuyumculuk", "https://omerhaskuyumculuk.com/", "Kuyum", "ÖH"),
    ("Nevam Kuyumculuk", "https://nevamkuyumculuk.com/", "Kişiye özel takı", "NV"),
    ("Aşkın Concept", "https://askinconcept.com.tr/", "Parti konsepti", "AC"),
    ("Numtex", "https://numtexco.com/", "Baskılı tekstil", "NX"),
    ("Ahenk Kuruyemiş", "https://ahenkkuruyemis.com.tr/", "Kuruyemiş ve bitki çayı", "AK"),
    ("Armada Teknoloji", "https://armadateknoloji.com.tr/", "Bilgisayar ve güvenlik", "AT"),
    ("Moda Neslie", "https://modaneslie.com/", "Deri aksesuar", "MN"),
    ("Variteks", "https://variteks.com/", "Ortopedi", "VT"),
    ("Moon Butik", "https://moonbutik.com/", "Kadın giyim", "MB"),
    ("BodyHack", "https://www.bodyhack.com.tr/", "Spor salonu", "BH"),
    ("Tuncan Tekstil", "http://www.tuncantekstil.com/", "Paracord ve kordon", "TT"),
]

SUREC = [
    ("Ne olduğunu ölçerim",
     "İlk iş mevcut durumu rakamla tespit etmek. Hangi sayfada, hangi adımda, kaç kayıtta "
     "sorun var — bu bilinmeden yazılacak kod tahmine dayanır."),
    ("Kapsamı yazılı veririm",
     "Ne yapılacağı, neyin dışarıda kaldığı ve teslim biçimi baştan yazılır. Sonradan "
     "büyüyen iş ikimize de pahalıya patlar."),
    ("Ayrı temada geliştiririm",
     "Tema işleri yayınlanmamış bir kopyada yazılır, önizleme adresiyle doğrulanır, sonra "
     "canlıya alınır. Uygulama işlerinde geliştirme mağazası kullanılır."),
    ("Ölçerek teslim ederim",
     "Teslimde “yapıldı” demek yetmez; öncesi ve sonrası aynı yöntemle ölçülür. Toplu veri "
     "işlerinde eski değerlerin yedeği ve geri alma script'i bırakılır."),
]

TEKNIK_ILKELER = [
    ("surum", "API sürümü koda gömülü kalmaz",
     "Shopify API'si dönemsel sürümler yayınlıyor ve her sürüm sınırlı süre destekleniyor. "
     "Uygulama bir sürüme kilitlenir, yükseltme planlı yapılır. Sürüm adı kodun içine "
     "dağılmışsa bir gün sessizce kırılır — tek yerden yönetilir."),
    ("olcum", "Hız limiti baştan hesaba katılır",
     "Admin GraphQL API sorgu maliyeti hesaplayıp bütçeye göre sınırlıyor. Toplu işlerde "
     "sayfa sayfa gezmek yerine toplu işlem uçları kullanılır; sınıra yaklaşıldığında geri "
     "çekilme ve yeniden deneme mantığı kurulur."),
    ("kalkan", "Her webhook doğrulanır, her işlem idempotent yazılır",
     "Gelen isteğin imzası uygulama gizli anahtarıyla doğrulanmadan hiçbir şey işlenmez. "
     "Aynı olay birden çok kez gelebilir; ikinci işlem bir şey değiştirmemeli."),
    ("kalkan", "Kapsam dar istenir",
     "İstenen her erişim kapsamının kullanıldığı yer gösterilebilmeli. Geniş kapsam hem "
     "incelemede geri döner hem mağaza sahibini tedirgin eder. Yeni kapsam gerektiğinde "
     "yeniden yetkilendirme istenir."),
    ("geri", "Toplu iş loglanır ve geri alınabilir",
     "İş gruplar hâlinde yürür, her adım satır satır log dosyasına yazılır, yarıda kalırsa "
     "kaldığı yerden devam eder. Değişen alanların eski değerleri kimlikleriyle saklanır."),
    ("olcum", "Doğrulama kaynağın kendisinden yapılır",
     "Başarı çıktısına güvenilmez: yazılan değişiklik geri çekilip aranır. Sayfa önbelleği "
     "kaynakla aynı değildir; doğrulama panelden ya da API'den yapılır, tarayıcıdan değil."),
    ("geri", "Silmeden önce yönlendirme kurulur",
     "Koleksiyon, sayfa ya da ürün silinecekse önce 301 kurulur, sonra silinir, sonra "
     "yönlendirmenin çalıştığı doğrulanır. Sıra bu değilse adres bir süre 404 verir."),
    ("olcum", "Ölçüm CSS okuyarak değil, tarayıcıdan yapılır",
     "Hangi kuralın kazandığı özgüllük yarışıyla belirlenir; kaynağa bakarak tahmin etmek "
     "yanıltır. Konum ve boyut değerleri çalışan sayfadan okunur."),
]

# Olculmus, gercek vakalar. (baslik, [paragraflar], (onceki, sonraki, birim))
VAKALAR = [
    ("Satın alma butonu bir buçuk ekran aşağıdaydı",
     ["Bir kuyum mağazasında “Sepete Ekle” butonu mobilde <b>1147.</b> pikseldeydi. Müşteri "
      "bir buçuk ekran boyunca hiçbir satın alma tetikleyicisi görmüyordu.",
      "Fiyat kırılımı ve ürün künyesi karar öncesi değil, karar sonrası bilgi. İkisini de "
      "butonun altına aldık."],
     ("1147", "948", "px")),
    ("Sabit çubuk sepete yanlış varyantı atıyordu",
     ["Sabit sepet çubuğu varyant kimliğini sayfa yüklenirken okuyup sabitliyordu. Müşteri "
      "harf kolyede “Ç” seçiyor, çubuk sepete “A” ekliyordu; ölçülen kanıt formda "
      "<b>49143197565147</b>, çubukta <b>48748885934299</b>.",
      "Kimliği asıl ürün formundan tıklama anında okuyacak şekilde değiştirdik. Böyle bir "
      "hata sipariş gelene kadar kimseye görünmüyor — kod okuyarak değil, formdaki değerle "
      "çubuğun gönderdiği değeri karşılaştırarak bulunuyor."],
     None),
    ("Açık başlayan panel butonu aşağı itiyordu",
     ["Bir şapka markasında ürün sayfasındaki “Detaylar” paneli mobilde açık başlıyordu. Tek "
      "başına <b>845</b> piksel yer kaplıyor, satın alma butonunu <b>1811.</b> piksele itiyordu.",
      "Kapalı başlatınca <b>747</b> piksel kazanıldı. Masaüstünde eski davranışı bozmadık; "
      "orada yer sıkıntısı yoktu."],
     ("1811", "1064", "px")),
    ("Ürün türü alanı 71 sahte kategori üretiyordu",
     ["Bir katalogda ürün türü alanında <b>71</b> farklı değer vardı: “Yüzük 8”, “Bileklik 15”, "
      "“Kolye-5”. Sayılar gramaj değil, sıra numarasıydı.",
      "Google Shopping eşleştirmesi bu yüzden tutmuyor, mağazanın kendi filtresi onlarca "
      "sahte kategori üretiyordu. Eski değerleri silmeden önce geri dönüş için ayrı bir "
      "metafield'a yazdık."],
     ("71", "6", "kategori")),
    ("Sepet çekmecesinde ürüne 39 piksel kalıyordu",
     ["Sabit bloklar ürün listesinden yer çalıyordu: özet <b>234</b> + başlık <b>66</b> + "
      "çapraz satış <b>243</b> + alt bölüm <b>228</b> piksel.",
      "Ürün satırı <b>159</b> piksel olduğu için taşıp çapraz satış şeridinin altında "
      "kayboluyordu. Sabit kalması gerekmeyen her blok kaydırılabilir alanın içine alındı."],
     ("39", "406", "px")),
]

YAPMADIKLARIM = [
    "Uygulama kurmadan çözülebilecek bir işe uygulama yazmam.",
    "Ölçmediğim bir iyileştirmeyi “iyileşti” diye teslim etmem.",
    "Yedek almadan toplu veri işlemi başlatmam.",
    "Yönlendirme kurmadan koleksiyon, sayfa veya ürün silmem.",
    "İmza doğrulaması olmayan webhook ucu bırakmam.",
    "Uydurma rakam, sahte yorum ve doğrulanmamış rozet koymam.",
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
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", s)).strip()


def json_kacir(s):
    return duz(s).replace("\\", "\\\\").replace('"', '\\"')


def kod_boya(kacirilmis):
    """Kacirilmis kod metninde yorum satirlarini ve dizeleri renklendirir.

    Sadece yorum ve dize desenleri sarilir; baska hicbir sey degistirilmez,
    boylece kod metni bozulmaz."""
    s = kacirilmis
    s = re.sub(r"(&quot;[^&]*?&quot;|&#39;[^&]*?&#39;|'[^'\n]*')",
               r'<span class="k-dize">\1</span>', s)
    s = re.sub(r"(?m)(//[^\n]*)", r'<span class="k-yorum">\1</span>', s)
    s = re.sub(r"(?s)(\{%- comment -%\}.*?\{%- endcomment -%\})",
               r'<span class="k-yorum">\1</span>', s)
    return s


def menu_ogeleri():
    ogeler = [("/", "Ana sayfa"), ("/gelistirme/", "Geliştirme")]
    if UYGULAMALAR:
        ogeler.append(("/uygulamalar/", "Uygulamalar"))
    if PROJELER:
        ogeler.append(("/projeler/", "Projeler"))
    ogeler += [("/teknik/", "Teknik"), ("/yontem/", "Yöntem"), ("/iletisim/", "İletişim")]
    return ogeler


def ust(aktif):
    satirlar = []
    for yol, ad in menu_ogeleri():
        gecerli = ' aria-current="page"' if yol == aktif else ""
        satirlar.append('<a href="%s"%s>%s</a>' % (yol, gecerli, ad))
    return """<header class="ust">
  <div class="sarmal sarmal--genis ust__ic">
    <a class="ust__ad" href="/">%s<span class="ust__rol">%s</span></a>
    <button class="menu-dugme" type="button" aria-expanded="false" aria-controls="ana-menu">
      <span class="menu-dugme__cizgi"></span>
      <span class="menu-dugme__yazi">Menü</span>
    </button>
    <nav class="ust__menu" id="ana-menu" aria-label="Ana menü">%s</nav>
  </div>
</header>""" % (AD, ROL, "".join(satirlar))


def alt():
    def satir(yol, ad):
        return '<li><a href="%s">%s</a></li>' % (yol, kacir(ad))

    web_ler = [satir("/%s/" % h["slug"], h["ad"])
               for h in HIZMETLER if h["slug"] not in SHOPIFY_ALANLARI]
    shopify_ler = [satir("/%s/" % h["slug"], h["ad"])
                   for h in HIZMETLER if h["slug"] in SHOPIFY_ALANLARI]
    if UYGULAMALAR:
        shopify_ler.append(satir("/uygulamalar/", "App Store uygulamalarım"))
    if PROJELER:
        web_ler.append(satir("/projeler/", "Projeler"))
    web_ler.append(satir("/yontem/", "Yöntem"))
    shopify_ler.append(satir("/teknik/", "Teknik yaklaşım"))

    return """<footer class="alt">
  <div class="sarmal sarmal--genis">
    <div class="alt__izgara">
      <div class="alt__sutun alt__sutun--ilk">
        <p class="alt__ad">%(ad)s</p>
        <p class="alt__rol">%(rol)s</p>
        <p class="alt__metin">Web siteleri ve uygulamalar, işe özel araçlar, entegrasyon ve
          otomasyon geliştiriyorum. <strong>Shopify</strong> tarafında App Store uygulaması,
          mağazaya özel uygulama ve tema geliştirme.</p>
        <p class="alt__mono">Python · JavaScript · HTML/CSS · Shopify Admin GraphQL API · Liquid</p>
      </div>
      <div class="alt__sutun">
        <p class="alt__baslik">Web ve yazılım</p>
        <ul>%(webler)s</ul>
      </div>
      <div class="alt__sutun">
        <p class="alt__baslik">Shopify</p>
        <ul>%(shopifyler)s</ul>
      </div>
      <div class="alt__sutun">
        <p class="alt__baslik">İletişim</p>
        <ul>
          <li><a href="/iletisim/">İletişim sayfası</a></li>
          <li><a href="https://wa.me/%(t)s" target="_blank" rel="noopener">WhatsApp</a></li>
          <li><a href="tel:%(tp)s">%(ty)s</a></li>
          <li><a href="https://taftri.com/" target="_blank" rel="noopener">Taftri — ajans işleri</a></li>
        </ul>
      </div>
    </div>
    <div class="alt__satir">
      <div>&copy; <span id="yil">%(yil)s</span> %(ad)s · %(rol)s</div>
      <div><a href="/kvkk.html">KVKK</a> &middot; <a href="/gizlilik.html">Gizlilik</a></div>
    </div>
  </div>
</footer>""" % {"ad": AD, "rol": ROL, "webler": "".join(web_ler),
                "shopifyler": "".join(shopify_ler),
                "t": TELEFON.lstrip("+"), "tp": TELEFON, "ty": TELEFON_YAZI,
                "yil": BUGUN[:4]}


def kirinti(parcalar):
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


def maddeler(liste, ikonlu=False):
    sinif = "maddeler maddeler--isaret" if ikonlu else "maddeler"
    return '<ul class="%s">%s</ul>' % (sinif, "".join("<li>%s</li>" % m for m in liste))


def alanlar(ciftler):
    return "".join('<div class="alan"><h3>%s</h3><p>%s</p></div>' % (kacir(b), m)
                   for b, m in ciftler)


def adimlar(ciftler):
    ic = []
    for n, (b, m) in enumerate(ciftler, 1):
        ic.append('<li class="adim"><span class="adim__no">%02d</span>'
                  '<div class="adim__ic"><h3>%s</h3><p>%s</p></div></li>'
                  % (n, kacir(b), kacir(m)))
    return '<ol class="adimlar">%s</ol>' % "".join(ic)


def konsol(dil, kod, ad=""):
    return """<figure class="konsol">
        <figcaption class="konsol__ust">
          <span class="konsol__noktalar"><i></i><i></i><i></i></span>
          <span class="konsol__ad">%s</span>
          <span class="konsol__dil">%s</span>
        </figcaption>
        <pre><code>%s</code></pre>
      </figure>""" % (kacir(ad), kacir(dil), kod_boya(kacir(kod)))


def kod_blok(baslik, dil, kod, not_metni="", ad=""):
    return """
  <section class="bolum bolum--beyaz" aria-labelledby="kod-h">
    <div class="sarmal sarmal--genis">
      <h2 class="bolum-basligi" id="kod-h">%(baslik)s</h2>
      %(konsol)s
      %(not)s
    </div>
  </section>""" % {"baslik": kacir(baslik), "konsol": konsol(dil, kod, ad),
                   "not": ('<p class="kod__not">%s</p>' % kacir(not_metni)) if not_metni else ""}


def serit_bolumu():
    ic = "".join('<div class="serit__oge"><span class="serit__sayi">%s</span>'
                 '<span class="serit__birim">%s</span>'
                 '<span class="serit__not">%s</span></div>'
                 % (kacir(s), kacir(b), kacir(n)) for s, b, n in SERIT)
    return """
  <section class="serit" aria-label="Ölçülmüş sonuçlar">
    <div class="sarmal sarmal--genis">
      <div class="serit__izgara">%s</div>
      <p class="serit__kaynak">Hepsi gerçek mağazalarda ölçüldü ·
        <a href="/yontem/">nasıl ölçüldüğü</a></p>
    </div>
  </section>""" % ic


def sss_blok(ciftler, baslik_id="sss-h", beyaz=False):
    if not ciftler:
        return "", None
    govde = "".join('<details class="sss"><summary>%s</summary><p>%s</p></details>'
                    % (kacir(s), c) for s, c in ciftler)
    ld = ('{"@context":"https://schema.org","@type":"FAQPage","mainEntity":[%s]}'
          % ",".join('{"@type":"Question","name":"%s","acceptedAnswer":'
                     '{"@type":"Answer","text":"%s"}}' % (json_kacir(s), json_kacir(c))
                     for s, c in ciftler))
    html = """
  <section class="bolum%s" aria-labelledby="%s">
    <div class="sarmal">
      <h2 class="bolum-basligi" id="%s">Sık sorulanlar</h2>
      <div class="sss-liste">%s</div>
    </div>
  </section>""" % (" bolum--beyaz" if beyaz else "", baslik_id, baslik_id, govde)
    return html, ld


def kart(url, ust_yazi, baslik, ozet, alt_yazi="", ikon=""):
    return """<a class="kart" href="%s">
          %s
          <span class="kart__ust">%s</span>
          <span class="kart__baslik">%s</span>
          <span class="kart__ozet">%s</span>%s
          <span class="kart__ok" aria-hidden="true">→</span>
        </a>""" % (
        url,
        ('<span class="kart__ikon">%s</span>' % IKON[ikon]) if ikon else "",
        kacir(ust_yazi), kacir(baslik), kacir(ozet),
        ('<span class="kart__alt">%s</span>' % kacir(alt_yazi)) if alt_yazi else "")


def hizmet_kartlari():
    return "".join(kart("/%s/" % h["slug"], "Geliştirme", h["ad"], h["ozet"],
                        ikon=HIZMET_IKON.get(h["slug"], ""))
                   for h in HIZMETLER)


def marka_izgarasi():
    ler = []
    for ad, url, sektor, mono in MARKALAR:
        ler.append("""<a class="marka" href="%s" target="_blank" rel="noopener">
          <span class="marka__mono" aria-hidden="true">%s</span>
          <span class="marka__govde">
            <span class="marka__ad">%s</span>
            <span class="marka__sektor">%s</span>
          </span>
        </a>""" % (url, kacir(mono), kacir(ad), kacir(sektor)))
    return '<div class="markalar">%s</div>' % "".join(ler)


def cta(baslik, metin, buton="İletişime geç", hedef="/iletisim/"):
    return """
  <section class="cta" aria-labelledby="cta-h">
    <div class="sarmal sarmal--genis">
      <div class="cta__ic">
        <div>
          <h2 id="cta-h">%s</h2>
          <p>%s</p>
        </div>
        <div class="cta__butonlar">
          <a class="btn" href="%s">%s</a>
          <a class="btn btn--sade" href="https://wa.me/%s" target="_blank" rel="noopener">WhatsApp</a>
        </div>
      </div>
    </div>
  </section>""" % (kacir(baslik), kacir(metin), hedef, kacir(buton), TELEFON.lstrip("+"))


def sayfa_ici(baglar):
    """baglar: [(id, ad)] — sayfa ici hizli gecis seridi."""
    if not baglar:
        return ""
    ler = "".join('<a href="#%s">%s</a>' % (i, kacir(a)) for i, a in baglar)
    return ('<nav class="sayfa-ici" aria-label="Bu sayfada">'
            '<span class="sayfa-ici__etiket">Bu sayfada</span>%s</nav>' % ler)


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
<meta name="theme-color" content="#2F4F3E" />
<meta property="og:type" content="website" />
<meta property="og:url" content="%(kanonik)s" />
<meta property="og:title" content="%(baslik)s" />
<meta property="og:description" content="%(aciklama)s" />
<meta property="og:locale" content="tr_TR" />
<meta name="twitter:card" content="summary" />
<link rel="icon" href="/favicon.svg" type="image/svg+xml" />
<link rel="preconnect" href="https://fonts.googleapis.com" />
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Newsreader:opsz,wght@6..72,400;6..72,500;6..72,600&family=Karla:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" />
<link rel="stylesheet" href="/assets/stil.css" />%(ld)s
</head>
<body>
<a class="atla" href="#icerik">İçeriğe atla</a>
%(ust)s
<main id="icerik">
%(govde)s
</main>
%(alt)s
<script src="/assets/site.js" defer></script>
</body>
</html>
""" % {"baslik": kacir(baslik), "aciklama": kacir(aciklama), "kanonik": kanonik,
       "rb": rb, "ld": ld, "ust": ust(aktif_menu), "govde": govde, "alt": alt()}


# ---------------------------------------------------------------------------
# STIL
# ---------------------------------------------------------------------------

STIL = """:root{
  --kagit:#F4F2EC;
  --kagit-2:#FFFFFF;
  --murekkep:#1B1D18;
  --murekkep-2:#4B4E45;
  --murekkep-3:#666A5F;
  --cizgi:#E1DCD0;
  --cizgi-2:#CCC6B6;
  --yesil:#2F4F3E;
  --yesil-2:#3F6650;
  --yesil-yumusak:#E4EDE5;
  --koyu:#17190F;
  --koyu-2:#20231A;
  --koyu-metin:#E8EBE1;
  --koyu-soluk:#9BA292;
  --vurgu:#C9A227;
  --genislik:700px;
  --genislik-genis:1060px;
  --mono:'JetBrains Mono',ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;
  --gecis:.2s cubic-bezier(.22,.61,.36,1);
}

*{box-sizing:border-box;margin:0;padding:0}
html{scroll-behavior:smooth}
@media (prefers-reduced-motion:reduce){
  html{scroll-behavior:auto}
  *,*::before,*::after{animation-duration:.01ms!important;transition-duration:.01ms!important}
}

body{
  background:var(--kagit);color:var(--murekkep);
  font-family:'Karla',ui-sans-serif,system-ui,'Segoe UI',sans-serif;
  font-size:17px;line-height:1.65;-webkit-font-smoothing:antialiased;
  display:flex;flex-direction:column;min-height:100vh;
}
main{flex:1 0 auto}
:target{scroll-margin-top:88px}

.sarmal{max-width:var(--genislik);margin:0 auto;padding:0 24px;width:100%}
.sarmal--genis{max-width:var(--genislik-genis)}

a{color:var(--yesil);text-decoration:none;border-bottom:1px solid rgba(47,79,62,.26);transition:border-color var(--gecis),color var(--gecis)}
a:hover{color:var(--yesil-2);border-bottom-color:var(--yesil-2)}
a:focus-visible{outline:2px solid var(--yesil);outline-offset:3px;border-radius:2px}

.atla{position:absolute;left:-9999px;top:0;z-index:30;padding:12px 18px;background:var(--yesil);color:#fff;border-bottom:0}
.atla:focus{left:8px;top:8px;color:#fff}

/* ---------- ust ---------- */
.ust{
  position:sticky;top:0;z-index:20;
  border-bottom:1px solid var(--cizgi);
  background:rgba(255,255,255,.92);backdrop-filter:saturate(1.4) blur(8px);
}
.ust__ic{display:flex;align-items:center;justify-content:space-between;gap:10px 28px;padding-top:12px;padding-bottom:12px}
.ust__ad{font-family:'Newsreader',Georgia,serif;font-size:18px;font-weight:600;color:var(--murekkep);border-bottom:0;letter-spacing:-.01em;line-height:1.2;padding:4px 0}
.ust__ad:hover{color:var(--yesil)}
.ust__rol{display:block;font-family:var(--mono);font-size:10.5px;font-weight:400;letter-spacing:.06em;text-transform:uppercase;color:var(--murekkep-3);margin-top:3px}
.ust__menu{display:flex;flex-wrap:wrap;gap:2px 4px;font-size:15px}
.ust__menu a{
  color:var(--murekkep-2);border-bottom:0;border-radius:6px;
  padding:8px 11px;min-height:40px;display:inline-flex;align-items:center;
  transition:background var(--gecis),color var(--gecis);
}
.ust__menu a:hover{color:var(--murekkep);background:var(--kagit)}
.ust__menu a[aria-current="page"]{color:var(--yesil);background:var(--yesil-yumusak);font-weight:600}

.menu-dugme{
  display:none;align-items:center;gap:9px;
  font-family:var(--mono);font-size:13px;letter-spacing:.04em;text-transform:uppercase;
  color:var(--murekkep);background:var(--kagit-2);
  border:1px solid var(--cizgi-2);border-radius:7px;
  padding:0 14px;min-height:44px;cursor:pointer;
}
.menu-dugme__cizgi,.menu-dugme__cizgi::before,.menu-dugme__cizgi::after{
  display:block;width:16px;height:1.5px;background:var(--murekkep);
  transition:transform var(--gecis),opacity var(--gecis);
}
.menu-dugme__cizgi{position:relative}
.menu-dugme__cizgi::before,.menu-dugme__cizgi::after{content:"";position:absolute;left:0}
.menu-dugme__cizgi::before{top:-5px}
.menu-dugme__cizgi::after{top:5px}
.menu-dugme[aria-expanded="true"] .menu-dugme__cizgi{background:transparent}
.menu-dugme[aria-expanded="true"] .menu-dugme__cizgi::before{transform:translateY(5px) rotate(45deg)}
.menu-dugme[aria-expanded="true"] .menu-dugme__cizgi::after{transform:translateY(-5px) rotate(-45deg)}

@media (max-width:900px){
  .menu-dugme{display:inline-flex}
  .ust__menu{
    display:none;order:3;width:100%;flex-direction:column;gap:2px;
    padding:8px 0 12px;border-top:1px solid var(--cizgi);margin-top:12px;
  }
  .ust__menu.acik{display:flex}
  .ust__menu a{width:100%;min-height:46px;font-size:16px}
}

/* ---------- kirinti ---------- */
.crumbs{list-style:none;display:flex;flex-wrap:wrap;gap:2px 6px;font-family:var(--mono);font-size:12.5px;color:var(--murekkep-3);padding:22px 0 0}
.crumbs li{display:inline-flex;align-items:center;min-height:26px}
.crumbs li+li::before{content:"/";margin-right:6px;color:var(--cizgi-2)}
.crumbs a{color:var(--murekkep-3);border-bottom-color:transparent;padding:2px 0}
.crumbs a:hover{color:var(--yesil);border-bottom-color:var(--yesil)}

/* ---------- giris ---------- */
.giris{padding:56px 0 0}
.giris--ic{padding:16px 0 0}
.hero{display:grid;gap:38px 48px;grid-template-columns:1fr;align-items:center;padding:56px 0 8px}
@media (min-width:900px){.hero{grid-template-columns:1.05fr .95fr;padding:66px 0 10px}}
.ad{font-family:'Newsreader',Georgia,serif;font-size:clamp(33px,5.4vw,47px);font-weight:500;letter-spacing:-.018em;line-height:1.12}
.ad--ic{font-size:clamp(28px,4.6vw,38px)}
.rol{
  display:inline-flex;align-items:center;gap:8px;
  font-family:var(--mono);font-size:12px;letter-spacing:.06em;text-transform:uppercase;
  color:var(--yesil);background:var(--yesil-yumusak);
  padding:5px 12px;border-radius:999px;margin-bottom:16px;
}
.rol::before{content:"";width:6px;height:6px;border-radius:50%;background:var(--yesil);flex:none}
.hero p,.giris p:not(.rol){margin-top:22px;font-size:19px;line-height:1.7;color:var(--murekkep-2);max-width:56ch}
.hero p+p,.giris p:not(.rol)+p{margin-top:15px}
.giris strong,.hero strong{font-weight:700;color:var(--murekkep)}
.hero__butonlar{display:flex;flex-wrap:wrap;gap:12px;margin-top:30px}

/* ---------- bolumler ---------- */
.bolum{padding:58px 0}
.bolum--beyaz{background:var(--kagit-2);border-top:1px solid var(--cizgi);border-bottom:1px solid var(--cizgi)}
.bolum--beyaz+.bolum--beyaz{border-top:0}
.bolum-basligi{
  display:flex;align-items:center;gap:12px;
  font-family:var(--mono);font-size:12.5px;font-weight:500;letter-spacing:.09em;
  text-transform:uppercase;color:var(--murekkep-3);margin-bottom:26px;
}
.bolum-basligi::after{content:"";flex:1;height:1px;background:var(--cizgi)}
.bolum-giris{color:var(--murekkep-2);max-width:62ch;margin-bottom:26px}

.alan{padding:22px 0;border-bottom:1px solid var(--cizgi)}
.alan:last-child{border-bottom:0;padding-bottom:0}
.alan h3{font-family:'Newsreader',Georgia,serif;font-size:21px;font-weight:500;letter-spacing:-.01em;margin-bottom:6px}
.alan p{color:var(--murekkep-2);max-width:64ch}
.bolum--beyaz .alan{border-color:var(--cizgi)}

/* ---------- adimlar ---------- */
.adimlar{list-style:none;counter-reset:adim;display:grid;gap:2px}
.adim{display:grid;grid-template-columns:auto 1fr;gap:18px;padding:20px 0;border-bottom:1px solid var(--cizgi)}
.adim:last-child{border-bottom:0}
.adim__no{font-family:var(--mono);font-size:13px;color:var(--yesil);background:var(--yesil-yumusak);border-radius:6px;width:38px;height:38px;display:flex;align-items:center;justify-content:center;flex:none}
.adim__ic h3{font-family:'Newsreader',Georgia,serif;font-size:20px;font-weight:500;margin-bottom:4px}
.adim__ic p{color:var(--murekkep-2);max-width:62ch}

/* ---------- serit ---------- */
.serit{background:var(--koyu);color:var(--koyu-metin);padding:44px 0 40px}
.serit__izgara{display:grid;gap:26px 20px;grid-template-columns:repeat(auto-fit,minmax(190px,1fr))}
.serit__oge{border-left:2px solid rgba(232,235,225,.16);padding-left:16px}
.serit__sayi{display:block;font-family:var(--mono);font-size:clamp(21px,2.6vw,26px);font-weight:500;color:#fff;letter-spacing:-.01em}
.serit__birim{display:block;font-family:var(--mono);font-size:11.5px;letter-spacing:.1em;text-transform:uppercase;color:var(--vurgu);margin-top:5px}
.serit__not{display:block;font-size:14.5px;color:var(--koyu-soluk);margin-top:9px;line-height:1.5}
.serit__kaynak{margin-top:30px;font-size:14px;color:var(--koyu-soluk)}
.serit__kaynak a{color:var(--koyu-metin);border-bottom-color:rgba(232,235,225,.3);padding:4px 0;display:inline-block}
.serit__kaynak a:hover{color:#fff;border-bottom-color:#fff}

/* ---------- konsol / kod ---------- */
.konsol{border-radius:10px;overflow:hidden;background:var(--koyu-2);border:1px solid rgba(232,235,225,.1);box-shadow:0 14px 40px -22px rgba(23,25,15,.5)}
.konsol__ust{display:flex;align-items:center;gap:12px;padding:10px 14px;background:var(--koyu);border-bottom:1px solid rgba(232,235,225,.09)}
.konsol__noktalar{display:flex;gap:6px}
.konsol__noktalar i{width:9px;height:9px;border-radius:50%;background:rgba(232,235,225,.2)}
.konsol__ad{font-family:var(--mono);font-size:11.5px;color:var(--koyu-soluk);flex:1}
.konsol__dil{font-family:var(--mono);font-size:10.5px;letter-spacing:.09em;text-transform:uppercase;color:var(--vurgu)}
.konsol pre{margin:0;padding:18px 16px 20px;overflow-x:auto}
.konsol code{font-family:var(--mono);font-size:13.5px;line-height:1.68;color:var(--koyu-metin);white-space:pre;display:block}
.k-yorum{color:var(--koyu-soluk);font-style:italic}
.k-dize{color:#B7CDA8}
.kod__not{margin-top:18px;color:var(--murekkep-2);max-width:64ch;font-size:16px}

/* ---------- yuzeyler ---------- */
.yuzeyler{display:grid;gap:10px;grid-template-columns:repeat(auto-fill,minmax(268px,1fr))}
.yuzey{padding:14px 16px;background:var(--kagit-2);border:1px solid var(--cizgi);border-radius:8px;transition:border-color var(--gecis),transform var(--gecis)}
.yuzey:hover{border-color:var(--cizgi-2);transform:translateY(-1px)}
.bolum--beyaz .yuzey{background:var(--kagit)}
.yuzey__ad{font-family:var(--mono);font-size:13.5px;font-weight:500;color:var(--murekkep);display:block}
.yuzey__not{font-size:14.5px;color:var(--murekkep-3);margin-top:3px;display:block;line-height:1.5}

/* ---------- kartlar ---------- */
.kartlar{display:grid;gap:14px;grid-template-columns:repeat(auto-fill,minmax(252px,1fr))}
.kart{
  position:relative;display:flex;flex-direction:column;gap:6px;
  padding:24px 24px 46px;background:var(--kagit-2);
  border:1px solid var(--cizgi);border-radius:10px;color:inherit;
  transition:border-color var(--gecis),box-shadow var(--gecis),transform var(--gecis);
}
.bolum--beyaz .kart{background:var(--kagit)}
.kart:hover{border-color:var(--yesil-2);box-shadow:0 12px 30px -18px rgba(27,29,24,.4);transform:translateY(-2px)}
.kart__ikon{display:flex;align-items:center;justify-content:center;width:40px;height:40px;border-radius:9px;background:var(--yesil-yumusak);color:var(--yesil);margin-bottom:12px}
.kart__ikon svg{width:21px;height:21px}
.kart__ust{font-family:var(--mono);font-size:11px;letter-spacing:.08em;text-transform:uppercase;color:var(--murekkep-3)}
.kart__baslik{font-family:'Newsreader',Georgia,serif;font-size:20px;font-weight:500;line-height:1.25;color:var(--murekkep)}
.kart__ozet{color:var(--murekkep-2);font-size:16px;line-height:1.6}
.kart__alt{margin-top:4px;font-family:var(--mono);font-size:12.5px;color:var(--murekkep-3)}
.kart__ok{position:absolute;left:24px;bottom:20px;color:var(--yesil);font-size:17px;transition:transform var(--gecis)}
.kart:hover .kart__ok{transform:translateX(5px)}

.rozetler{display:flex;flex-wrap:wrap;gap:8px 9px;margin-top:24px}
.rozet{font-family:var(--mono);font-size:12.5px;padding:6px 11px;border:1px solid var(--cizgi-2);border-radius:6px;color:var(--murekkep-2);background:var(--kagit-2)}
.bolum--beyaz .rozet{background:var(--kagit)}

.markalar{display:grid;gap:10px;grid-template-columns:repeat(auto-fill,minmax(232px,1fr))}
.marka{
  display:flex;align-items:center;gap:13px;min-height:66px;padding:12px 14px;
  border:1px solid var(--cizgi);border-radius:10px;background:var(--kagit-2);
  color:inherit;
  transition:border-color var(--gecis),box-shadow var(--gecis),transform var(--gecis);
}
.bolum--beyaz .marka{background:var(--kagit)}
a.marka:hover{border-color:var(--yesil-2);box-shadow:0 10px 26px -18px rgba(27,29,24,.5);transform:translateY(-2px)}
.marka__mono{
  flex:none;display:flex;align-items:center;justify-content:center;
  width:42px;height:42px;border-radius:9px;background:var(--yesil);color:#fff;
  font-family:var(--mono);font-size:14px;font-weight:500;
  transition:background var(--gecis);
}
a.marka:hover .marka__mono{background:var(--yesil-2)}
.marka__govde{display:flex;flex-direction:column;gap:2px;min-width:0}
.marka__ad{font-family:'Newsreader',Georgia,serif;font-size:17px;font-weight:500;color:var(--murekkep);line-height:1.25}
.marka__sektor{font-family:var(--mono);font-size:11px;letter-spacing:.06em;text-transform:uppercase;color:var(--murekkep-3)}

.maddeler{list-style:none;margin-top:4px}
.maddeler li{position:relative;padding-left:22px;color:var(--murekkep-2);max-width:64ch;margin-top:10px}
.maddeler li::before{content:"";position:absolute;left:2px;top:11px;width:8px;height:1.5px;background:var(--yesil);border-radius:2px}
.maddeler--isaret li::before{content:"✕";width:auto;height:auto;background:none;top:0;color:var(--yesil);font-size:12px}

.durum{display:inline-flex;align-items:center;gap:7px;font-family:var(--mono);font-size:12px;letter-spacing:.05em;text-transform:uppercase;padding:5px 12px;border-radius:6px;background:var(--yesil-yumusak);color:var(--yesil);margin-top:14px}
.durum::before{content:"";width:6px;height:6px;border-radius:50%;background:var(--yesil)}

.btn{display:inline-flex;align-items:center;justify-content:center;min-height:46px;padding:12px 24px;border-radius:7px;background:var(--yesil);color:#fff;font-weight:600;font-size:16px;border-bottom:0;transition:background var(--gecis),transform var(--gecis);white-space:nowrap}
.btn:hover{background:var(--yesil-2);color:#fff;border-bottom:0;transform:translateY(-1px)}
.btn--sade{background:transparent;color:var(--yesil);border:1px solid var(--cizgi-2)}
.btn--sade:hover{background:var(--yesil-yumusak);color:var(--yesil);border-color:var(--yesil-2)}

.gorsel{margin-top:24px;width:100%;height:auto;border:1px solid var(--cizgi);border-radius:10px}

/* ---------- sss ---------- */
.sss-liste{border-top:1px solid var(--cizgi)}
.sss{border-bottom:1px solid var(--cizgi)}
.sss summary{
  display:flex;align-items:flex-start;gap:12px;
  list-style:none;cursor:pointer;padding:17px 0;min-height:48px;
  font-family:'Newsreader',Georgia,serif;font-size:19px;font-weight:500;
  color:var(--murekkep);transition:color var(--gecis);
}
.sss summary::-webkit-details-marker{display:none}
.sss summary::before{content:"+";font-family:var(--mono);font-size:17px;color:var(--yesil);line-height:1.5;flex:none;transition:transform var(--gecis)}
.sss[open] summary::before{content:"−"}
.sss summary:hover{color:var(--yesil)}
.sss p{color:var(--murekkep-2);max-width:64ch;padding:0 0 20px 27px}

/* ---------- sayfa ici gecis ---------- */
.sayfa-ici{display:flex;flex-wrap:wrap;align-items:center;gap:8px;margin-top:26px}
.sayfa-ici__etiket{font-family:var(--mono);font-size:11px;letter-spacing:.09em;text-transform:uppercase;color:var(--murekkep-3);margin-right:2px}
.sayfa-ici a{display:inline-flex;align-items:center;min-height:34px;padding:5px 13px;border:1px solid var(--cizgi);border-radius:999px;background:var(--kagit-2);color:var(--murekkep-2);font-size:14.5px;transition:border-color var(--gecis),color var(--gecis),background var(--gecis)}
.sayfa-ici a:hover{color:var(--yesil);border-color:var(--yesil-2);background:var(--yesil-yumusak)}

/* ---------- taftri ---------- */
.taftri{display:flex;flex-wrap:wrap;gap:16px 26px;align-items:center;justify-content:space-between;padding:26px 30px;background:var(--yesil-yumusak);border-left:3px solid var(--yesil);border-radius:0 10px 10px 0}
.taftri h3{font-family:'Newsreader',Georgia,serif;font-size:20px;font-weight:500;margin-bottom:6px}
.taftri p{color:var(--murekkep-2);max-width:52ch}

/* ---------- cta ---------- */
.cta{background:var(--koyu);color:var(--koyu-metin);padding:52px 0}
.cta__ic{display:flex;flex-wrap:wrap;align-items:center;justify-content:space-between;gap:24px 40px}
.cta__ic h2{font-family:'Newsreader',Georgia,serif;font-size:clamp(23px,3vw,29px);font-weight:500;letter-spacing:-.01em;color:#fff}
.cta__ic p{color:var(--koyu-soluk);max-width:50ch;margin-top:8px}
.cta__butonlar{display:flex;flex-wrap:wrap;gap:12px}
.cta .btn{background:var(--vurgu);color:var(--koyu)}
.cta .btn:hover{background:#DCB63D;color:var(--koyu)}
.cta .btn--sade{background:transparent;color:var(--koyu-metin);border-color:rgba(232,235,225,.28)}
.cta .btn--sade:hover{background:rgba(232,235,225,.08);color:#fff;border-color:rgba(232,235,225,.5)}

/* ---------- iletisim ---------- */
.iletisim-izgara{display:grid;gap:14px;grid-template-columns:repeat(auto-fit,minmax(230px,1fr))}
.iletisim-kart{display:flex;flex-direction:column;gap:4px;padding:22px 24px;background:var(--kagit-2);border:1px solid var(--cizgi);border-radius:10px;color:inherit;min-height:104px;justify-content:center;transition:border-color var(--gecis),transform var(--gecis)}
.iletisim-kart:hover{border-color:var(--yesil-2);transform:translateY(-2px)}
.iletisim-kart span{font-family:var(--mono);font-size:11.5px;letter-spacing:.08em;text-transform:uppercase;color:var(--murekkep-3)}
.iletisim-kart b{font-size:19px;font-weight:600;color:var(--murekkep)}
.devam{margin-top:24px;margin-bottom:0}
.devam a{display:inline-flex;align-items:center;gap:6px;min-height:32px}

/* ---------- alt ---------- */
.alt{flex-shrink:0;padding:52px 0 40px;border-top:1px solid var(--cizgi);background:var(--kagit-2);color:var(--murekkep-3);font-size:15px}
.alt__izgara{display:grid;gap:30px 32px;grid-template-columns:1fr}
.alt__sutun--ilk{min-width:0}
@media (min-width:620px){
  .alt__izgara{grid-template-columns:repeat(2,1fr)}
  .alt__sutun--ilk{grid-column:span 2}
}
@media (min-width:920px){
  .alt__izgara{grid-template-columns:1.75fr 1fr 1fr 1.05fr}
  .alt__sutun--ilk{grid-column:auto}
}
.alt__ad{font-family:'Newsreader',Georgia,serif;font-size:18px;font-weight:600;color:var(--murekkep)}
.alt__rol{font-family:var(--mono);font-size:11px;letter-spacing:.06em;text-transform:uppercase;color:var(--yesil);margin-top:3px}
.alt__metin{margin-top:12px;max-width:44ch;line-height:1.6}
.alt__metin strong{color:var(--murekkep);font-weight:600}
.alt__mono{margin-top:14px;font-family:var(--mono);font-size:11.5px;color:var(--murekkep-3);line-height:1.9}
.alt__baslik{font-family:var(--mono);font-size:11.5px;letter-spacing:.09em;text-transform:uppercase;color:var(--murekkep-2);margin-bottom:6px}
.alt__sutun ul{list-style:none}
.alt__sutun li{line-height:1.4}
.alt__sutun li a{display:inline-flex;align-items:center;min-height:32px;padding:4px 0}
.alt a{color:var(--murekkep-3);border-bottom-color:transparent}
.alt a:hover{color:var(--yesil);border-bottom-color:var(--yesil)}
.alt__satir{display:flex;flex-wrap:wrap;gap:6px 20px;justify-content:space-between;align-items:center;margin-top:36px;padding-top:18px;border-top:1px solid var(--cizgi);font-size:14px}
.alt__satir a{display:inline-flex;align-items:center;min-height:32px;padding:4px 0}

@media (max-width:600px){
  body{font-size:16px}
  .giris{padding-top:34px}
  .hero{padding-top:34px;gap:30px}
  .hero p,.giris p:not(.rol){font-size:17.5px}
  .bolum{padding:42px 0}
  .serit{padding:36px 0 32px}
  .cta{padding:40px 0}
  .taftri{padding:22px 20px}
  .kart{padding:20px 20px 44px}
  .kart__ok{left:20px}
  .konsol code{font-size:12.5px}
  .adim{gap:14px}
  .alt__izgara{gap:26px 24px}
}
"""

BETIK = """(function () {
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
"""


# ---------------------------------------------------------------------------
# JSON-LD
# ---------------------------------------------------------------------------

def ld_kisi():
    return ('{"@context":"https://schema.org","@type":"Person",'
            '"name":"%s","jobTitle":"Yazılım geliştirici",'
            '"url":"%s/","telephone":"%s",'
            '"knowsAbout":["Yazılım geliştirme","Web geliştirme","Web uygulaması",'
            '"Otomasyon","API entegrasyonu","Python","JavaScript",'
            '"Shopify uygulama geliştirme","Shopify Admin GraphQL API",'
            '"Liquid tema geliştirme","E-ticaret entegrasyonu"],'
            '"sameAs":["https://taftri.com/"]}' % (AD, SITE, TELEFON))


def ld_site():
    return ('{"@context":"https://schema.org","@type":"WebSite",'
            '"name":"%s","url":"%s/","inLanguage":"tr-TR"}' % (AD, SITE))


def ld_hizmet(h):
    return ('{"@context":"https://schema.org","@type":"Service",'
            '"name":"%s","serviceType":"%s",'
            '"provider":{"@type":"Person","name":"%s","url":"%s/"},'
            '"areaServed":"TR","url":"%s/%s/","description":"%s"}'
            % (json_kacir(h["baslik"]), json_kacir(h["ad"]), AD, SITE,
               SITE, h["slug"], json_kacir(h["aciklama"])))


# ---------------------------------------------------------------------------
# SAYFALAR
# ---------------------------------------------------------------------------

def yuzey_bolumu(beyaz=False):
    ler = "".join('<div class="yuzey"><span class="yuzey__ad">%s</span>'
                  '<span class="yuzey__not">%s</span></div>'
                  % (kacir(a), kacir(n)) for a, n in YUZEYLER)
    return """
  <section class="bolum%s" aria-labelledby="yuzey-h">
    <div class="sarmal sarmal--genis">
      <h2 class="bolum-basligi" id="yuzey-h">Shopify tarafında çalıştığım yüzeyler</h2>
      <div class="yuzeyler">%s</div>
    </div>
  </section>""" % (" bolum--beyaz" if beyaz else "", ler)


def ana_sayfa():
    baslik = "%s — Yazılım ve Shopify geliştiricisi" % AD
    aciklama = ("Web siteleri ve uygulamalar, işe özel yazılım, entegrasyon ve otomasyon "
                "geliştiriyorum. E-ticaret tarafında Shopify uygulama ve tema geliştirme.")

    parcalar = ["""
  <div class="sarmal sarmal--genis">
    <header class="hero">
      <div>
        <p class="rol">Yazılım ve Shopify geliştiricisi</p>
        <h1 class="ad">Yazılım geliştiriyorum</h1>
        <p>Web siteleri ve uygulamalar, işe özel araçlar, entegrasyonlar ve otomasyon.
          Bir kısmı e-ticaret tarafında — Shopify'da uygulama ve tema geliştiriyorum —
          ama tek yaptığım bu değil.</p>
        <p>Hepsinin ortak yanı şu: iş yeni bir şey icat etmekle değil,
          <strong>ölçmekle</strong> başlıyor.</p>
        <div class="hero__butonlar">
          <a class="btn" href="/gelistirme/">Ne geliştiriyorum</a>
          <a class="btn btn--sade" href="/iletisim/">İletişime geç</a>
        </div>
      </div>
      %s
    </header>
  </div>""" % konsol("graphql", KOD_HERO, "admin-api")]

    parcalar.append(serit_bolumu())

    parcalar.append("""
  <section class="bolum" aria-labelledby="alanlar-h">
    <div class="sarmal sarmal--genis">
      <h2 class="bolum-basligi" id="alanlar-h">Ne geliştiriyorum</h2>
      <div class="kartlar">%s</div>
      <p class="devam"><a href="/gelistirme/">Geliştirme alanlarının tamamı →</a></p>
    </div>
  </section>""" % hizmet_kartlari())

    parcalar.append(yuzey_bolumu(beyaz=True))

    if UYGULAMALAR:
        kartlar = "".join(
            kart("/uygulamalar/%s/" % u["slug"],
                 DURUM_ADI.get(u.get("durum", ""), "Uygulama"),
                 u["ad"], u["ozet"], u.get("fiyat", ""), ikon="app")
            for u in UYGULAMALAR[:3])
        parcalar.append("""
  <section class="bolum" aria-labelledby="uygulamalar-h">
    <div class="sarmal sarmal--genis">
      <h2 class="bolum-basligi" id="uygulamalar-h">Uygulamalar</h2>
      <div class="kartlar">%s</div>
      <p class="devam"><a href="/uygulamalar/">Tüm uygulamalar →</a></p>
    </div>
  </section>""" % kartlar)

    if PROJELER:
        kartlar = "".join(
            kart("/projeler/%s/" % i["slug"], TUR_ADI.get(i.get("tur", ""), "Proje"),
                 i["baslik"], i["ozet"], i.get("musteri", ""), ikon="olcum")
            for i in PROJELER[:3])
        parcalar.append("""
  <section class="bolum" aria-labelledby="projeler-h">
    <div class="sarmal sarmal--genis">
      <h2 class="bolum-basligi" id="projeler-h">Projeler</h2>
      <div class="kartlar">%s</div>
      <p class="devam"><a href="/projeler/">Tüm projeler →</a></p>
    </div>
  </section>""" % kartlar)

    parcalar.append(kod_blok("Binlerce kayıtlık iş nasıl yürür", "graphql", KOD_BULK,
                             "Toplu işlem sonucu JSONL dosyası olarak indirilir. Aynı veriyi "
                             "sayfa sayfa çekmek hem hız limitini yakar hem yarıda kalırsa "
                             "nereden devam edeceğini bilemezsin.", "bulk-operation"))

    b, paragraflar, _ = VAKALAR[0]
    parcalar.append("""
  <section class="bolum" aria-labelledby="yontem-h">
    <div class="sarmal">
      <h2 class="bolum-basligi" id="yontem-h">Nasıl çalışıyorum</h2>
      %s
      <p class="devam"><a href="/yontem/">Ölçüm örneklerinin tamamı →</a></p>
    </div>
  </section>""" % adimlar(SUREC))

    parcalar.append("""
  <section class="bolum bolum--beyaz" aria-labelledby="markalar-h">
    <div class="sarmal sarmal--genis">
      <h2 class="bolum-basligi" id="markalar-h">Birlikte çalıştığım markalar</h2>
      <p class="bolum-giris">%d marka, %d ayrı sektör. Şapkadan kuyuma, ortopediden
        kuruyemişe — ortak nokta ürün değil, aynı teknik sorunlar.</p>
      %s
      <div class="taftri" style="margin-top:34px">
        <div>
          <h3>Ajans işleri Taftri üzerinden</h3>
          <p>Ekip gerektiren işler — sürekli reklam yönetimi, içerik üretimi, uzun soluklu
            mağaza operasyonu.</p>
        </div>
        <a class="btn btn--sade" href="https://taftri.com/" rel="noopener">taftri.com</a>
      </div>
    </div>
  </section>""" % (len(MARKALAR), len({m[2].split(" · ")[0] for m in MARKALAR}),
                   marka_izgarasi()))

    parcalar.append(cta("Aklınızda bir şey var mı?",
                        "Ne yapılması gerektiğini söylemek çoğu zaman kısa sürüyor."))

    return sayfa(baslik, aciklama, SITE + "/", "/", "".join(parcalar),
                 [ld_kisi(), ld_site()])


def gelistirme_hub():
    baslik = "Geliştirme alanları — %s" % AD
    aciklama = ("Web sitesi ve uygulaması, Shopify App Store uygulaması, mağazaya özel "
                "yazılım, tema geliştirme ve entegrasyon. Hangisi hangi işe uygun.")
    kb, kld = kirinti([("Ana sayfa", "/"), ("Geliştirme", None)])
    liste_ld = ('{"@context":"https://schema.org","@type":"ItemList",'
                '"itemListElement":[%s]}' % ",".join(
                    '{"@type":"ListItem","position":%d,"name":"%s","url":"%s/%s/"}'
                    % (n + 1, json_kacir(h["ad"]), SITE, h["slug"])
                    for n, h in enumerate(HIZMETLER)))
    govde = """
  <div class="sarmal sarmal--genis">%(kb)s
    <header class="giris giris--ic">
      <p class="rol">Geliştirme</p>
      <h1 class="ad ad--ic">Geliştirme alanları</h1>
      <p>Beş ayrı iş kolu. Hangisinin gerektiği çoğu zaman baştan belli olmuyor — aynı
        istek bazen tema içinde, bazen uygulamayla çözülüyor. Kararı ölçtükten sonra
        veriyorum; genelde daha az bağımlılık getiren yol kazanıyor.</p>
    </header>
  </div>

  <section class="bolum" aria-label="Geliştirme alanları">
    <div class="sarmal sarmal--genis"><div class="kartlar">%(kartlar)s</div></div>
  </section>

  <section class="bolum bolum--beyaz" aria-labelledby="hangisi-h">
    <div class="sarmal">
      <h2 class="bolum-basligi" id="hangisi-h">Hangisi size uygun</h2>
      %(karar)s
    </div>
  </section>
%(yuzey)s
%(cta)s""" % {
        "kb": kb, "kartlar": hizmet_kartlari(), "yuzey": yuzey_bolumu(),
        "karar": alanlar([
            ("İşiniz e-ticaretle ilgili değilse",
             'Site, açılış sayfası, panel ya da iç araç — '
             '<a href="/web-gelistirme/">web tarafı</a>. Shopify bir uzmanlık alanı, '
             'tek çalıştığım yer değil.'),
            ("Aynı ihtiyaç birçok mağazada varsa",
             'Satılabilir bir ürün var demektir; <a href="/uygulama-gelistirme/">App Store '
             'uygulaması</a> doğru yol. Çerçeve işi — kurulum, faturalama, zorunlu uçlar — '
             'baştan doğru kurulmalı.'),
            ("İhtiyaç sadece sizin iş akışınıza özelse",
             '<a href="/ozel-yazilim/">Mağazaya özel uygulama</a> daha hızlı ve ucuz. '
             'İnceleme süreci yok, kod sizde kalıyor.'),
            ("Sorun mağazanın görünen tarafındaysa",
             'Çoğu istek uygulama kurmadan <a href="/tema-gelistirme/">tema içinde</a> '
             'çözülüyor. Uygulama, mağazaya kalıcı bir bağımlılık ekler.'),
            ("Sorun dışarıyla veri alışverişindeyse",
             '<a href="/entegrasyon/">Entegrasyon ve toplu veri</a> tarafı. Muhasebe, kargo, '
             'ERP, pazaryeri ve binlerce kayıtlık düzeltme işleri.'),
        ]),
        "cta": cta("Hangisi olduğundan emin değilseniz",
                   "Durumu anlatın; hangi yolun daha az iş ve daha az bağımlılık "
                   "getirdiğini söyleyeyim."),
    }
    return sayfa(baslik, aciklama, SITE + "/gelistirme/", "/gelistirme/", govde,
                 [kld, liste_ld])


def hizmet_sayfasi(h):
    baslik = "%s — %s" % (h["baslik"], AD)
    if len(baslik) > 65:
        baslik = h["baslik"]
    kb, kld = kirinti([("Ana sayfa", "/"), ("Geliştirme", "/gelistirme/"), (h["ad"], None)])

    digerleri = [d for d in HIZMETLER if d["slug"] != h["slug"]]
    diger_kartlar = "".join(kart("/%s/" % d["slug"], "Geliştirme", d["ad"], d["ozet"],
                                 ikon=HIZMET_IKON.get(d["slug"], ""))
                            for d in digerleri)
    sss_html, sss_ld = sss_blok(h.get("sss", []), beyaz=True)
    kod_html = ""
    baglar = [("kapsam-h", h["kapsam_basligi"]), ("surec-h", "Nasıl yürüyor")]
    if h.get("kod"):
        kod_html = kod_blok(h["kod"][0], h["kod"][1], h["kod"][2], h.get("kod_not", ""),
                            h["slug"])
        baglar.insert(1, ("kod-h", "Kod"))
    if h.get("sss"):
        baglar.append(("sss-h", "Sık sorulanlar"))

    govde = """
  <div class="sarmal sarmal--genis">%(kb)s
    <header class="giris giris--ic">
      <p class="rol">Geliştirme</p>
      <h1 class="ad ad--ic">%(h1)s</h1>
      %(giris)s
      %(ici)s
    </header>
  </div>

  <section class="bolum" aria-labelledby="kapsam-h">
    <div class="sarmal">
      <h2 class="bolum-basligi" id="kapsam-h">%(kapsam_basligi)s</h2>
      %(kapsam)s
      %(rozet)s
    </div>
  </section>
%(kod)s
  <section class="bolum" aria-labelledby="surec-h">
    <div class="sarmal">
      <h2 class="bolum-basligi" id="surec-h">Nasıl yürüyor</h2>
      %(surec)s
      <p class="devam"><a href="/teknik/">Teknik yaklaşım →</a></p>
    </div>
  </section>
%(sss)s
  <section class="bolum" aria-labelledby="diger-h">
    <div class="sarmal sarmal--genis">
      <h2 class="bolum-basligi" id="diger-h">Diğer geliştirme alanları</h2>
      <div class="kartlar">%(diger)s</div>
    </div>
  </section>
%(cta)s""" % {
        "kb": kb, "h1": kacir(h["baslik"]),
        "giris": "".join("<p>%s</p>" % p for p in h["giris"]),
        "ici": sayfa_ici(baglar),
        "kapsam_basligi": kacir(h["kapsam_basligi"]),
        "kapsam": alanlar(h["kapsam"]),
        "rozet": rozetler(h.get("teknik", [])),
        "kod": kod_html,
        "surec": adimlar(SUREC),
        "sss": sss_html,
        "diger": diger_kartlar,
        "cta": cta("Bu işin sizdeki karşılığı ne?",
                   "Mevcut durumu anlatın; ölçüp ne gerektiğini söyleyeyim."),
    }
    ldler = [kld, ld_hizmet(h)]
    if sss_ld:
        ldler.append(sss_ld)
    return sayfa(baslik, h["aciklama"], SITE + "/%s/" % h["slug"], "/gelistirme/",
                 govde, ldler)


def teknik_sayfasi():
    baslik = "Teknik yaklaşım — Shopify geliştirme"
    aciklama = ("API sürüm yönetimi, hız limiti, webhook imza doğrulama, idempotent işleme, "
                "geri alınabilir toplu iş ve doğrulama disiplini.")
    kb, kld = kirinti([("Ana sayfa", "/"), ("Teknik", None)])
    ilke_html = "".join(
        '<div class="alan" style="display:grid;grid-template-columns:auto 1fr;gap:16px">'
        '<span class="kart__ikon" style="margin:0">%s</span>'
        '<div><h3>%s</h3><p>%s</p></div></div>' % (IKON[ik], kacir(b), kacir(m))
        for ik, b, m in TEKNIK_ILKELER)
    govde = """
  <div class="sarmal sarmal--genis">%(kb)s
    <header class="giris giris--ic">
      <p class="rol">Teknik yaklaşım</p>
      <h1 class="ad ad--ic">Nasıl yazıyorum</h1>
      <p>Aşağıdakiler tercih değil, sahada bir kere kaybedip öğrenilmiş kurallar. Hepsi bir
        hataya mal olmuş; bu yüzden istisnasız uygulanıyor.</p>
      %(ici)s
    </header>
  </div>

  <section class="bolum" aria-labelledby="ilke-h">
    <div class="sarmal">
      <h2 class="bolum-basligi" id="ilke-h">İlkeler</h2>
      %(ilkeler)s
    </div>
  </section>
%(kod1)s
%(kod2)s
%(yuzey)s
%(cta)s""" % {
        "kb": kb, "ilkeler": ilke_html,
        "ici": sayfa_ici([("ilke-h", "İlkeler"), ("kod-h", "Kod"),
                          ("yuzey-h", "Shopify yüzeyleri")]),
        "kod1": kod_blok("Webhook imzası doğrulanmadan hiçbir şey işlenmez", "js", KOD_HMAC,
                         "İmza doğrulaması olmayan bir webhook ucu, herkesin veri yazabildiği "
                         "açık bir kapıdır.", "webhook.js"),
        "kod2": kod_blok("Boş render eden blok bırakmamak", "liquid", KOD_BOLUM,
                         "Bir mağazada silinmiş bir ürüne işaret eden hediye bloğu aylarca "
                         "sessizce boş basmıştı. Koşul olmadan yazılan her referanslı blok "
                         "aynı riski taşır.", "hediye-kutu.liquid"),
        "yuzey": yuzey_bolumu(),
        "cta": cta("Mevcut kurulumunuz bu ölçütleri karşılıyor mu?",
                   "Bakıp ne gördüğümü yazayım — mağazanın adresi yeterli."),
    }
    return sayfa(baslik, aciklama, SITE + "/teknik/", "/teknik/", govde, [kld])


def yontem_sayfasi():
    baslik = "Nasıl çalışıyorum — %s" % AD
    aciklama = ("Ölçerek teşhis, yazılı kapsam, ayrı temada geliştirme ve ölçülmüş teslim. "
                "Sahadan beş ölçüm örneği.")
    kb, kld = kirinti([("Ana sayfa", "/"), ("Yöntem", None)])

    vaka_html = []
    for b, paragraflar, olcum in VAKALAR:
        rakam = ""
        if olcum:
            rakam = ('<div class="vaka__olcum"><span class="vaka__once">%s</span>'
                     '<span class="vaka__ok">→</span>'
                     '<span class="vaka__sonra">%s</span>'
                     '<span class="vaka__birim">%s</span></div>'
                     % (kacir(olcum[0]), kacir(olcum[1]), kacir(olcum[2])))
        vaka_html.append('<article class="vaka"><h3>%s</h3>%s%s</article>'
                         % (kacir(b), rakam, "".join("<p>%s</p>" % p for p in paragraflar)))

    govde = """
  <div class="sarmal sarmal--genis">%(kb)s
    <header class="giris giris--ic">
      <p class="rol">Yöntem</p>
      <h1 class="ad ad--ic">Nasıl çalışıyorum</h1>
      <p>İşin büyük kısmı yeni bir şey icat etmekle değil, hâlihazırda para kaybettiren
        yeri bulmakla geçiyor. Bunun tek yolu <strong>ölçmek</strong>.</p>
      %(ici)s
    </header>
  </div>

  <section class="bolum" aria-labelledby="surec-h">
    <div class="sarmal">
      <h2 class="bolum-basligi" id="surec-h">Süreç</h2>
      %(surec)s
    </div>
  </section>

  <section class="bolum bolum--beyaz" aria-labelledby="vaka-h">
    <div class="sarmal sarmal--genis">
      <h2 class="bolum-basligi" id="vaka-h">Ölçüm örnekleri</h2>
      <p class="bolum-giris">Hepsi gerçek mağazalarda ölçüldü. Rakamlar tahmin değil,
        çalışan sayfadan okunan değerler.</p>
      <div class="vakalar">%(vakalar)s</div>
    </div>
  </section>

  <section class="bolum" aria-labelledby="yapmam-h">
    <div class="sarmal">
      <h2 class="bolum-basligi" id="yapmam-h">Yapmadıklarım</h2>
      %(yapmam)s
      <p class="devam"><a href="/teknik/">Teknik ilkelerin tamamı →</a></p>
    </div>
  </section>
%(cta)s""" % {"kb": kb, "surec": adimlar(SUREC), "vakalar": "".join(vaka_html),
              "ici": sayfa_ici([("surec-h", "Süreç"), ("vaka-h", "Ölçüm örnekleri"),
                                ("yapmam-h", "Yapmadıklarım")]),
              "yapmam": maddeler([kacir(m) for m in YAPMADIKLARIM], ikonlu=True),
              "cta": cta("Sizde ne ölçülmeli?",
                         "Mağazanın adresini yollayın; bakıp ne gördüğümü yazayım.")}
    return sayfa(baslik, aciklama, SITE + "/yontem/", "/yontem/", govde, [kld])


def iletisim_sayfasi():
    baslik = "İletişim — %s" % AD
    aciklama = ("Shopify uygulama, tema ve entegrasyon işleri için iletişim. WhatsApp ve "
                "telefon; ajans işleri Taftri üzerinden.")
    kb, kld = kirinti([("Ana sayfa", "/"), ("İletişim", None)])
    govde = """
  <div class="sarmal sarmal--genis">%(kb)s
    <header class="giris giris--ic">
      <p class="rol">İletişim</p>
      <h1 class="ad ad--ic">Yazın, bakalım</h1>
      <p>Bir fikir ya da tıkanmış bir iş varsa yazın. Ne yapılması gerektiğini söylemek
        çoğu zaman kısa sürüyor; bunun için ücret almıyorum.</p>
    </header>
  </div>

  <section class="bolum" aria-labelledby="kanal-h">
    <div class="sarmal sarmal--genis">
      <h2 class="bolum-basligi" id="kanal-h">Doğrudan</h2>
      <div class="iletisim-izgara">
        <a class="iletisim-kart" href="https://wa.me/%(t)s" target="_blank" rel="noopener">
          <span>WhatsApp</span><b>%(ty)s</b>
        </a>
        <a class="iletisim-kart" href="tel:%(tp)s">
          <span>Telefon</span><b>%(ty)s</b>
        </a>
        <a class="iletisim-kart" href="https://taftri.com/" target="_blank" rel="noopener">
          <span>Ajans işleri</span><b>taftri.com</b>
        </a>
      </div>
    </div>
  </section>

  <section class="bolum bolum--beyaz" aria-labelledby="ne-h">
    <div class="sarmal">
      <h2 class="bolum-basligi" id="ne-h">Yazarken şunlar işi hızlandırır</h2>
      %(ne)s
    </div>
  </section>

  <section class="bolum" aria-labelledby="alan-h">
    <div class="sarmal sarmal--genis">
      <h2 class="bolum-basligi" id="alan-h">Hangi konuda</h2>
      <div class="kartlar">%(kartlar)s</div>
    </div>
  </section>""" % {
        "kb": kb, "t": TELEFON.lstrip("+"), "tp": TELEFON, "ty": TELEFON_YAZI,
        "kartlar": hizmet_kartlari(),
        "ne": maddeler([
            "Mağazanın adresi.",
            "Ne olmasını istediğiniz — teknik terim gerekmiyor, düz anlatım yeterli.",
            "Şu an ne olduğu; varsa ekran görüntüsü.",
            "Hazır uygulama denediyseniz hangisi ve neden yetmediği.",
            "Aceleyse ne zamana kadar gerektiği.",
        ]),
    }
    kisi_ld = ('{"@context":"https://schema.org","@type":"ContactPage",'
               '"name":"İletişim","url":"%s/iletisim/",'
               '"mainEntity":{"@type":"Person","name":"%s","telephone":"%s"}}'
               % (SITE, AD, TELEFON))
    return sayfa(baslik, aciklama, SITE + "/iletisim/", "/iletisim/", govde,
                 [kld, kisi_ld])


def uygulama_listesi():
    baslik = "Shopify uygulamaları — %s" % AD
    aciklama = ("Shopify App Store için geliştirdiğim uygulamalar: hangi sorunu çözdükleri, "
                "ne yaptıkları ve kurulum bilgileri.")
    kb, kld = kirinti([("Ana sayfa", "/"), ("Uygulamalar", None)])
    kartlar = "".join(
        kart("/uygulamalar/%s/" % u["slug"],
             DURUM_ADI.get(u.get("durum", ""), "Uygulama"),
             u["ad"], u["ozet"], u.get("fiyat", ""), ikon="app")
        for u in UYGULAMALAR)
    liste_ld = ('{"@context":"https://schema.org","@type":"ItemList",'
                '"itemListElement":[%s]}' % ",".join(
                    '{"@type":"ListItem","position":%d,"name":"%s","url":"%s/uygulamalar/%s/"}'
                    % (n + 1, json_kacir(u["ad"]), SITE, u["slug"])
                    for n, u in enumerate(UYGULAMALAR)))
    govde = """
  <div class="sarmal sarmal--genis">%s
    <header class="giris giris--ic">
      <p class="rol">Uygulamalar</p>
      <h1 class="ad ad--ic">Shopify App Store uygulamaları</h1>
      <p>Her birinin sayfasında hangi sorunu çözdüğü, ne yaptığı ve hangi platform uçlarını
        kullandığı yazılı.</p>
    </header>
  </div>
  <section class="bolum" aria-label="Uygulama listesi">
    <div class="sarmal sarmal--genis"><div class="kartlar">%s</div></div>
  </section>
%s""" % (kb, kartlar, cta("Benzer bir uygulama mı gerekiyor?",
                          "Aynı ihtiyaç sizde de varsa yazın; mevcut uygulama işinizi görüyor "
                          "mu bakalım."))
    return sayfa(baslik, aciklama, SITE + "/uygulamalar/", "/uygulamalar/",
                 govde, [kld, liste_ld])


def uygulama_sayfasi(u):
    baslik = "%s — Shopify uygulaması" % u["ad"]
    aciklama = duz(u["ozet"])[:155]
    yol = "/uygulamalar/%s/" % u["slug"]
    kb, kld = kirinti([("Ana sayfa", "/"), ("Uygulamalar", "/uygulamalar/"), (u["ad"], None)])

    durum = DURUM_ADI.get(u.get("durum", ""))
    parcalar = ["""
  <div class="sarmal sarmal--genis">%s
    <header class="giris giris--ic">
      <p class="rol">Uygulama</p>
      <h1 class="ad ad--ic">%s</h1>
      %s
      <p>%s</p>
      %s
    </header>
  </div>""" % (
        kb, kacir(u["ad"]),
        ('<p class="durum">%s</p>' % durum) if durum else "",
        kacir(u["ozet"]),
        ('<div class="hero__butonlar"><a class="btn" href="%s" target="_blank" '
         'rel="noopener">App Store\'da aç</a></div>' % u["app_store"])
        if u.get("app_store") else "")]

    if u.get("gorsel"):
        parcalar.append('\n  <div class="sarmal sarmal--genis"><img class="gorsel" src="%s" '
                        'alt="%s" loading="lazy" /></div>'
                        % (u["gorsel"], kacir(u.get("gorsel_alt", u["ad"]))))

    parcalar.append("""
  <section class="bolum" aria-labelledby="sorun-h">
    <div class="sarmal">
      <h2 class="bolum-basligi" id="sorun-h">Hangi sorunu çözüyor</h2>
      <p class="bolum-giris" style="margin-bottom:0">%s</p>
    </div>
  </section>""" % kacir(u["sorun"]))

    parcalar.append("""
  <section class="bolum bolum--beyaz" aria-labelledby="cozum-h">
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

    if u.get("kod"):
        parcalar.append(kod_blok(u["kod"][0], u["kod"][1], u["kod"][2],
                                 u.get("kod_not", ""), u["slug"]))

    sss_html, sss_ld = sss_blok(u.get("sss", []))
    if sss_html:
        parcalar.append(sss_html)
    parcalar.append(cta("Mağazanıza uyar mı?",
                        "Emin değilseniz yazın; işinizi görüp görmediğine birlikte bakalım."))

    yazilim_ld = ('{"@context":"https://schema.org","@type":"SoftwareApplication",'
                  '"name":"%s","applicationCategory":"BusinessApplication",'
                  '"operatingSystem":"Shopify","description":"%s",'
                  '"author":{"@type":"Person","name":"%s"}%s}'
                  % (json_kacir(u["ad"]), json_kacir(u["ozet"]), AD,
                     (',"url":"%s"' % u["app_store"]) if u.get("app_store") else ""))
    ldler = [kld, yazilim_ld]
    if sss_ld:
        ldler.append(sss_ld)
    return sayfa(baslik, aciklama, SITE + yol, "/uygulamalar/", "".join(parcalar), ldler)


def proje_listesi():
    baslik = "Projeler — %s" % AD
    aciklama = ("Shopify mağazaları için yazdığım özel uygulamalar, tema özellikleri ve "
                "entegrasyonlar; başlangıç durumu ve ölçülmüş sonuçlarıyla.")
    kb, kld = kirinti([("Ana sayfa", "/"), ("Projeler", None)])
    kartlar = "".join(
        kart("/projeler/%s/" % i["slug"], TUR_ADI.get(i.get("tur", ""), "Proje"),
             i["baslik"], i["ozet"], i.get("musteri", ""), ikon="olcum")
        for i in PROJELER)
    liste_ld = ('{"@context":"https://schema.org","@type":"ItemList",'
                '"itemListElement":[%s]}' % ",".join(
                    '{"@type":"ListItem","position":%d,"name":"%s","url":"%s/projeler/%s/"}'
                    % (n + 1, json_kacir(i["baslik"]), SITE, i["slug"])
                    for n, i in enumerate(PROJELER)))
    govde = """
  <div class="sarmal sarmal--genis">%s
    <header class="giris giris--ic">
      <p class="rol">Projeler</p>
      <h1 class="ad ad--ic">Projeler</h1>
      <p>Her kayıtta işin başlangıç durumu, ne yapıldığı ve mümkün olduğunda ölçülmüş
        sonucu yazılı. Rakam yoksa rakam yazılmıyor.</p>
    </header>
  </div>
  <section class="bolum" aria-label="Proje listesi">
    <div class="sarmal sarmal--genis"><div class="kartlar">%s</div></div>
  </section>
%s""" % (kb, kartlar, cta("Benzer bir projeniz mi var?",
                         "Durumu anlatın; ölçüp ne gerektiğini söyleyeyim."))
    return sayfa(baslik, aciklama, SITE + "/projeler/", "/projeler/", govde,
                 [kld, liste_ld])


def proje_sayfasi(i):
    baslik = "%s — %s" % (i["baslik"], i["musteri"])
    if len(baslik) > 65:
        baslik = i["baslik"]
    aciklama = duz(i["ozet"])[:155]
    yol = "/projeler/%s/" % i["slug"]
    kb, kld = kirinti([("Ana sayfa", "/"), ("Projeler", "/projeler/"),
                       (i["baslik"], None)])

    musteri_html = kacir(i["musteri"])
    if i.get("musteri_url"):
        musteri_html = ('<a href="%s" target="_blank" rel="noopener">%s</a>'
                        % (i["musteri_url"], musteri_html))

    parcalar = ["""
  <div class="sarmal sarmal--genis">%s
    <header class="giris giris--ic">
      <p class="rol">%s</p>
      <h1 class="ad ad--ic">%s</h1>
      <p>%s</p>
      <p style="font-size:16px">Müşteri: %s</p>
    </header>
  </div>""" % (kb, kacir(TUR_ADI.get(i.get("tur", ""), "Proje")), kacir(i["baslik"]),
               kacir(i["ozet"]), musteri_html)]

    parcalar.append("""
  <section class="bolum" aria-labelledby="durum-h">
    <div class="sarmal">
      <h2 class="bolum-basligi" id="durum-h">Başlangıç durumu</h2>
      <p class="bolum-giris" style="margin-bottom:0">%s</p>
    </div>
  </section>""" % kacir(i["sorun"]))

    parcalar.append("""
  <section class="bolum bolum--beyaz" aria-labelledby="yapilan-h">
    <div class="sarmal">
      <h2 class="bolum-basligi" id="yapilan-h">Yapılan</h2>
      %s
      %s
    </div>
  </section>""" % (maddeler([kacir(m) for m in i["yapilan"]]),
                   rozetler(i.get("teknik", []))))

    if i.get("kod"):
        parcalar.append(kod_blok(i["kod"][0], i["kod"][1], i["kod"][2],
                                 i.get("kod_not", ""), i["slug"]))

    if i.get("sonuc"):
        parcalar.append("""
  <section class="bolum" aria-labelledby="sonuc-h">
    <div class="sarmal">
      <h2 class="bolum-basligi" id="sonuc-h">Sonuç</h2>
      %s
    </div>
  </section>""" % maddeler([kacir(m) for m in i["sonuc"]]))

    parcalar.append(cta("Sizde de benzer bir durum mu var?",
                        "Mağazanın adresini yollayın; bakıp ne gördüğümü yazayım."))

    proje_ld = ('{"@context":"https://schema.org","@type":"CreativeWork",'
             '"name":"%s","description":"%s","inLanguage":"tr-TR",'
             '"creator":{"@type":"Person","name":"%s"},'
             '"about":{"@type":"Organization","name":"%s"%s}}'
             % (json_kacir(i["baslik"]), json_kacir(i["ozet"]), AD,
                json_kacir(i["musteri"]),
                (',"url":"%s"' % i["musteri_url"]) if i.get("musteri_url") else ""))
    return sayfa(baslik, aciklama, SITE + yol, "/projeler/", "".join(parcalar),
                 [kld, proje_ld])


def dort_yuz_dort():
    govde = """
  <div class="sarmal sarmal--genis">
    <header class="giris">
      <p class="rol">404</p>
      <h1 class="ad">Sayfa bulunamadı</h1>
      <p>Aradığınız adres taşınmış ya da hiç var olmamış olabilir. Geliştirme alanları
        yerinde duruyor:</p>
    </header>
  </div>
  <section class="bolum" aria-label="Geliştirme alanları">
    <div class="sarmal sarmal--genis"><div class="kartlar">%s</div></div>
  </section>""" % hizmet_kartlari()
    return sayfa("Sayfa bulunamadı — %s" % AD, "Aradığınız sayfa bulunamadı.",
                 SITE + "/404.html", "", govde, (), robots="noindex, follow")


def yonlendirme(baslik, metin, hedef):
    return """<!doctype html>
<html lang="tr">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>%(baslik)s</title>
<meta name="robots" content="noindex, follow" />
<link rel="canonical" href="%(hedef)s" />
<meta http-equiv="refresh" content="0; url=%(hedef)s" />
<style>
  body{margin:0;min-height:100vh;display:flex;align-items:center;justify-content:center;
    background:#F4F2EC;color:#1B1D18;font-family:ui-sans-serif,system-ui,'Segoe UI',sans-serif;
    line-height:1.6;padding:24px}
  .kutu{max-width:420px;text-align:center}
  h1{font-family:Georgia,serif;font-size:22px;font-weight:500;margin:0 0 10px}
  p{margin:0 0 18px;color:#4B4E45;font-size:16px}
  a{color:#2F4F3E;font-weight:500}
  a:focus-visible{outline:2px solid #2F4F3E;outline-offset:3px}
</style>
</head>
<body>
  <div class="kutu">
    <h1>%(baslik)s</h1>
    <p>%(metin)s</p>
    <p><a href="%(hedef)s">Devam et</a></p>
  </div>
  <script>location.replace('%(hedef)s');</script>
</body>
</html>
""" % {"baslik": kacir(baslik), "metin": kacir(metin), "hedef": hedef}


# ---------------------------------------------------------------------------
# DESTEK DOSYALARI
# ---------------------------------------------------------------------------

def adresler():
    yollar = ["/", "/gelistirme/"]
    yollar += ["/%s/" % h["slug"] for h in HIZMETLER]
    yollar += ["/teknik/", "/yontem/", "/iletisim/"]
    if UYGULAMALAR:
        yollar.append("/uygulamalar/")
        yollar += ["/uygulamalar/%s/" % u["slug"] for u in UYGULAMALAR]
    if PROJELER:
        yollar.append("/projeler/")
        yollar += ["/projeler/%s/" % i["slug"] for i in PROJELER]
    return yollar


def sitemap():
    satirlar = ['<?xml version="1.0" encoding="UTF-8"?>',
                '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for yol in adresler():
        derinlik = yol.strip("/").count("/")
        oncelik = "1.0" if yol == "/" else ("0.8" if derinlik == 0 else "0.7")
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
        "> Yazılım geliştirici. Web siteleri ve uygulamalar, işe özel araçlar,",
        "> entegrasyon ve otomasyon. E-ticaret tarafında Shopify uygulama ve tema.",
        "",
        "## Sayfalar",
        "",
        "- [Ana sayfa](%s/): ne geliştirdiği, ölçülmüş sonuçlar, markalar." % SITE,
        "- [Geliştirme](%s/gelistirme/): beş geliştirme alanı ve hangisinin hangi işe uygun olduğu." % SITE,
    ]
    for h in HIZMETLER:
        satirlar.append("  - [%s](%s/%s/): %s" % (h["ad"], SITE, h["slug"], duz(h["ozet"])))
    satirlar += [
        "- [Teknik yaklaşım](%s/teknik/): API sürümü, hız limiti, webhook doğrulama, "
        "idempotent işleme, geri alınabilir toplu iş." % SITE,
        "- [Yöntem](%s/yontem/): süreç, sahadan ölçüm örnekleri, yapmadıkları." % SITE,
        "- [İletişim](%s/iletisim/): WhatsApp ve telefon." % SITE,
    ]
    if UYGULAMALAR:
        satirlar.append("- [Uygulamalar](%s/uygulamalar/): App Store uygulamaları." % SITE)
        for u in UYGULAMALAR:
            satirlar.append("  - [%s](%s/uygulamalar/%s/): %s"
                            % (u["ad"], SITE, u["slug"], duz(u["ozet"])))
    if PROJELER:
        satirlar.append("- [Projeler](%s/projeler/): projeler ve ölçülmüş sonuçları." % SITE)
        for i in PROJELER:
            satirlar.append("  - [%s](%s/projeler/%s/): %s — %s"
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
            '<rect width="64" height="64" rx="13" fill="#2F4F3E"/>'
            '<text x="32" y="43" font-family="Georgia,serif" font-size="28" '
            'font-weight="600" fill="#F4F2EC" text-anchor="middle">MF</text></svg>\n')


# ---------------------------------------------------------------------------
# EK STIL — vakalar
# ---------------------------------------------------------------------------

STIL += """
.vakalar{display:grid;gap:14px;grid-template-columns:repeat(auto-fit,minmax(320px,1fr))}
.vaka{padding:26px 26px 24px;background:var(--kagit);border:1px solid var(--cizgi);border-radius:10px}
.bolum--beyaz .vaka{background:var(--kagit)}
.vaka h3{font-family:'Newsreader',Georgia,serif;font-size:21px;font-weight:500;line-height:1.28;letter-spacing:-.01em}
.vaka p{color:var(--murekkep-2);font-size:16px;margin-top:12px}
.vaka b{font-family:var(--mono);font-size:.92em;font-weight:500;color:var(--murekkep)}
.vaka__olcum{display:flex;align-items:baseline;flex-wrap:wrap;gap:10px;margin-top:16px;padding:12px 16px;background:var(--koyu);border-radius:8px}
.vaka__once{font-family:var(--mono);font-size:18px;color:var(--koyu-soluk);text-decoration:line-through}
.vaka__ok{color:var(--koyu-soluk);font-size:14px}
.vaka__sonra{font-family:var(--mono);font-size:20px;color:#fff;font-weight:500}
.vaka__birim{font-family:var(--mono);font-size:11px;letter-spacing:.1em;text-transform:uppercase;color:var(--vurgu)}
"""


# ---------------------------------------------------------------------------
# CALISTIR
# ---------------------------------------------------------------------------

def main():
    yaz("assets/stil.css", STIL)
    yaz("assets/site.js", BETIK)
    yaz("favicon.svg", favicon())

    yaz("index.html", ana_sayfa())
    yaz("gelistirme/index.html", gelistirme_hub())
    for h in HIZMETLER:
        yaz("%s/index.html" % h["slug"], hizmet_sayfasi(h))
    yaz("teknik/index.html", teknik_sayfasi())
    yaz("yontem/index.html", yontem_sayfasi())
    yaz("iletisim/index.html", iletisim_sayfasi())

    if UYGULAMALAR:
        yaz("uygulamalar/index.html", uygulama_listesi())
        for u in UYGULAMALAR:
            yaz("uygulamalar/%s/index.html" % u["slug"], uygulama_sayfasi(u))

    if PROJELER:
        yaz("projeler/index.html", proje_listesi())
        for i in PROJELER:
            yaz("projeler/%s/index.html" % i["slug"], proje_sayfasi(i))

        # eski /isler/ adresleri icin yonlendirme
        yaz("isler/index.html", yonlendirme(
            "Bu sayfa Projeler oldu",
            "Yapılmış işler artık /projeler/ adresinde. Yönlendiriliyorsunuz.",
            "https://mftoktay.com/projeler/"))
        for i in PROJELER:
            yaz("isler/%s/index.html" % i["slug"], yonlendirme(
                "Bu sayfa taşındı",
                "Proje sayfası /projeler/ altına taşındı. Yönlendiriliyorsunuz.",
                "https://mftoktay.com/projeler/%s/" % i["slug"]))

    yaz("404.html", dort_yuz_dort())

    yaz("iletisim.html", yonlendirme(
        "İletişim sayfası taşındı",
        "İletişim bilgileri /iletisim/ adresine taşındı. Yönlendiriliyorsunuz.",
        "https://mftoktay.com/iletisim/"))
    yaz("hizmetler.html", yonlendirme(
        "Hizmetler Taftri'ye taşındı",
        "Ajans hizmetleri taftri.com üzerinden yürüyor. Yönlendiriliyorsunuz.",
        "https://taftri.com/#hizmetler"))
    yaz("iade.html", yonlendirme(
        "Bu sayfa kaldırıldı",
        "Site üzerinden satış yapılmadığı için iade politikası sayfası kaldırıldı.",
        "https://mftoktay.com/"))

    yaz("sitemap.xml", sitemap())
    yaz("robots.txt", robots())
    yaz("llms.txt", llms())
    yaz("%s.txt" % INDEXNOW_ANAHTAR, INDEXNOW_ANAHTAR)

    print("Uretilen dosya: %d" % len(URETILEN))
    for y in URETILEN:
        print("  " + y)
    print("Sitemap adresi : %d" % len(adresler()))
    print("Uygulama: %d   Is: %d" % (len(UYGULAMALAR), len(PROJELER)))


if __name__ == "__main__":
    main()
