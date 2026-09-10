# -*- coding: utf-8 -*-
"""
mftoktay.com sayfa ureticisi.

Kullanim:  python uret.py

Bu dosya sitenin TEK kaynagidir. Uretilen .html dosyalarini elle duzenleme —
bir sonraki calistirmada uzerine yazilir. Icerik degisikligi burada yapilir.

Yapi (her sayfada ust menu + tam alt bilgi; tek sayfa yigini yok):

  /                       ana sayfa
  /gelistirme/            gelistirme alanlari — dort sayfaya dagitir
  /uygulama-gelistirme/   App Store uygulamasi
  /ozel-yazilim/          magazaya ozel uygulama
  /tema-gelistirme/       Liquid tema
  /entegrasyon/           Admin API, toplu veri, dis sistem
  /teknik/                teknik yaklasim — API surumu, hiz limiti, webhook, geri alma
  /yontem/                surec ve olcum ornekleri
  /iletisim/              iletisim
  /uygulamalar/[slug]/    UYGULAMALAR listesi doluysa
  /isler/[slug]/          ISLER listesi doluysa

Ornek eklemek:
  * App Store uygulamasi  -> UYGULAMALAR listesine bir sozluk ekle
  * Yapilmis is / vaka    -> ISLER listesine bir sozluk ekle
Liste bosken ilgili bolum, liste sayfasi ve menu ogesi hic uretilmez.
"""

import os
import re
from datetime import date

KOK = os.path.dirname(os.path.abspath(__file__))
SITE = "https://mftoktay.com"
BUGUN = date.today().isoformat()

AD = "M. Fehmi Toktay"
ROL = "Shopify uygulama geliştiricisi"
TELEFON = "+905541386827"
TELEFON_YAZI = "+90 554 138 68 27"
INDEXNOW_ANAHTAR = "a4d17f2c9b6e485fa03c71d8e6b25904"


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
#   "kod":         ("Baslik", "js", "..."),        #   kod ornegi; bossa basilmaz
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


# ---------------------------------------------------------------------------
# VERI — CALISILAN PLATFORM YUZEYLERI
# ---------------------------------------------------------------------------

YUZEYLER = [
    ("Admin GraphQL API", "ürün, varyant, sipariş, metafield okuma ve yazma"),
    ("Bulk Operations", "binlerce kayıtlık iş; sonuç JSONL olarak indirilir"),
    ("Webhooks", "olay yakalama, HMAC doğrulama, idempotent işleme"),
    ("OAuth ve Billing API", "kurulum akışı, kapsam yönetimi, abonelik ücretlendirmesi"),
    ("App Bridge ve Polaris", "yönetim paneli içinde açılan gömülü arayüz"),
    ("Liquid / Online Store 2.0", "bölüm ve blok yazımı, tema editöründen yönetim"),
    ("Storefront ve Ajax API", "sepet işlemleri, tema içi dinamik davranış"),
    ("Metafield ve Metaobject", "ürün künyesi ve yapılandırılmış veri"),
    ("URL Redirect", "geçişlerde yönlendirme haritası"),
    ("Theme CLI", "yayınlanmamış temada geliştirme, önizleme, canlıya alma"),
]


# ---------------------------------------------------------------------------
# VERI — GELISTIRME SAYFALARI
# ---------------------------------------------------------------------------

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

if (a.length !== b.length || !crypto.timingSafeEqual(a, b)) {
  return res.status(401).send();   // imza tutmuyor, istek Shopify'dan gelmiyor
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

HIZMETLER = [
    {
        "slug": "uygulama-gelistirme",
        "ad": "App Store uygulaması",
        "baslik": "Shopify App Store uygulaması geliştirme",
        "aciklama": ("Shopify App Store için uygulama geliştirme: OAuth, gömülü arayüz, "
                     "Admin GraphQL API, webhook, faturalama ve inceleme süreci."),
        "ozet": "Herkese açık, mağazaya kurulup abonelikle kullanılan uygulama.",
        "giris": [
            "App Store uygulaması tek bir mağazaya değil bütün mağazalara yazılır. "
            "İşin zor kısmı özellikte değil çerçevede: kurulum, yetkilendirme, "
            "faturalama ve zorunlu veri uçları Shopify'ın kendi kurallarına uymak zorunda.",
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
        "kod": ("Binlerce ürünü tek istekle çekmek — toplu işlem", "graphql", KOD_BULK),
        "kod_not": ("Toplu işlem sonucu JSONL dosyası olarak indirilir. Aynı veriyi "
                    "sayfa sayfa çekmek hem hız limitini yakar hem yarıda kalırsa "
                    "nereden devam edeceğini bilemezsin."),
        "sss": [
            ("Uygulama ne kadar sürede yayına girer?",
             "Geliştirme süresi kapsama göre değişir. Yayın tarafında Shopify'ın kendi "
             "inceleme süreci var; süresi başvuruya göre değişiyor ve kimse tarafından "
             "garanti edilemez. Vakit kaybettiren şey genelde inceleme değil, incelemeden "
             "dönen eksikler oluyor."),
            ("Gömülü mü olmalı?",
             "Yönetim paneli içinde çalışan uygulamalar hem daha çok kuruluyor hem "
             "listelemede avantajlı. Panelin dışında çalışmasını gerektiren özel bir "
             "durum yoksa gömülü yazıyorum."),
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
             "bildirimler. Mağazanın kendi çalışma biçimine göre yazılır — hazır uygulamaların "
             "yapamadığı kısım genelde burasıdır."),
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
             "Taşınabilir, ama baştan öyle yazılmadıysa çerçeve kısmı yeniden kurulur. Böyle "
             "bir ihtimal varsa başlarken söyleyin; yapı ona göre kurulsun."),
        ],
    },
    {
        "slug": "tema-gelistirme",
        "ad": "Tema geliştirme",
        "baslik": "Shopify tema geliştirme — Liquid",
        "aciklama": ("Shopify temasına özellik ekleme, bölüm ve blok yazımı, hız ve "
                     "dönüşüm düzeltmeleri. Tema editöründen yönetilebilir kurulum."),
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
                    "sessizce boş basmıştı. Koşul olmadan yazılan her referanslı blok "
                    "aynı riski taşır."),
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
            "bağlantıları; bir de kimsenin görmediği ama katalog kalitesini belirleyen "
            "toplu veri işleri.",
            "Buradaki asıl risk hata değil, <strong>sessiz hata</strong>: bir alan yanlış "
            "yazılır, kimse fark etmez, aylar sonra Google eşleştirmesi tutmaz. Bu yüzden "
            "her toplu iş loglanır ve geri alınabilir kurulur.",
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
             "bağlanması. Bir katalogda ürün türü alanında 71 farklı değer bulmuştum; "
             "sayılar gramaj değil sıra numarasıydı ve katalog eşleştirmesini kırıyordu."),
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

SUREC = [
    ("Ne olduğunu ölçerim",
     "İlk iş mevcut durumu rakamla tespit etmek. Hangi sayfada, hangi adımda, kaç kayıtta "
     "sorun var — bu bilinmeden yazılacak kod tahmine dayanır."),
    ("Kapsamı yazılı veririm",
     "Ne yapılacağı, neyin dışarıda kaldığı ve teslim biçimi baştan yazılır. Sonradan "
     "büyüyen iş ikimize de pahalıya patlar."),
    ("Ayrı temada / geliştirme mağazasında geliştiririm",
     "Tema işleri yayınlanmamış bir kopyada yazılır, önizleme adresiyle doğrulanır, sonra "
     "canlıya alınır. Uygulama işlerinde geliştirme mağazası kullanılır."),
    ("Ölçerek teslim ederim",
     "Teslimde “yapıldı” demek yetmez; öncesi ve sonrası aynı yöntemle ölçülür. Toplu veri "
     "işlerinde eski değerlerin yedeği ve geri alma script'i bırakılır."),
]

TEKNIK_ILKELER = [
    ("API sürümü koda gömülü kalmaz",
     "Shopify API'si dönemsel sürümler yayınlıyor ve her sürüm sınırlı süre destekleniyor. "
     "Uygulama bir sürüme kilitlenir, yükseltme planlı yapılır. Sürüm adı kodun içine "
     "dağılmışsa bir gün sessizce kırılır — tek yerden yönetilir."),
    ("Hız limiti baştan hesaba katılır",
     "Admin GraphQL API sorgu maliyeti hesaplayıp bütçeye göre sınırlıyor. Toplu işlerde "
     "sayfa sayfa gezmek yerine toplu işlem uçları kullanılır; sınıra yaklaşıldığında "
     "geri çekilme ve yeniden deneme mantığı kurulur."),
    ("Her webhook doğrulanır, her işlem idempotent yazılır",
     "Gelen isteğin imzası uygulama gizli anahtarıyla doğrulanmadan hiçbir şey işlenmez. "
     "Aynı olay birden çok kez gelebilir; ikinci işlem bir şey değiştirmemeli."),
    ("Kapsam dar istenir",
     "İstenen her erişim kapsamının kullanıldığı yer gösterilebilmeli. Geniş kapsam hem "
     "incelemede geri döner hem mağaza sahibini tedirgin eder. Yeni kapsam gerektiğinde "
     "yeniden yetkilendirme istenir."),
    ("Toplu iş loglanır ve geri alınabilir",
     "İş gruplar hâlinde yürür, her adım satır satır log dosyasına yazılır, yarıda kalırsa "
     "kaldığı yerden devam eder. Değişen alanların eski değerleri kimlikleriyle saklanır."),
    ("Doğrulama kaynağın kendisinden yapılır",
     "Başarı çıktısına güvenilmez: yazılan değişiklik geri çekilip aranır. Sayfa önbelleği "
     "kaynakla aynı değildir; doğrulama panelden ya da API'den yapılır, tarayıcıdan değil."),
    ("Silmeden önce yönlendirme kurulur",
     "Koleksiyon, sayfa ya da ürün silinecekse önce 301 kurulur, sonra silinir, sonra "
     "yönlendirmenin çalıştığı doğrulanır. Sıra bu değilse adres bir süre 404 verir."),
    ("Ölçüm CSS okuyarak değil, tarayıcıdan yapılır",
     "Hangi kuralın kazandığı özgüllük yarışıyla belirlenir; kaynağa bakarak tahmin etmek "
     "yanıltır. Konum ve boyut değerleri çalışan sayfadan okunur."),
]

# Olculmus, gercek vakalar.
VAKALAR = [
    ["Bir kuyum mağazasında “Sepete Ekle” butonu mobilde <span class=\"sayi\">1147.</span> "
     "pikseldeydi. Müşteri bir buçuk ekran boyunca hiçbir satın alma tetikleyicisi görmüyordu.",
     "Fiyat kırılımı ve ürün künyesi karar öncesi değil, karar sonrası bilgi. İkisini de "
     "butonun altına aldık; buton <span class=\"sayi\">948.</span> piksele çıktı."],
    ["Aynı mağazada sabit sepet çubuğu, varyant kimliğini sayfa yüklenirken okuyup "
     "sabitliyordu. Müşteri harf kolyede “Ç” seçiyor, çubuk sepete “A” ekliyordu; ölçülen "
     "kanıt formda <span class=\"sayi\">49143197565147</span>, çubukta "
     "<span class=\"sayi\">48748885934299</span>.",
     "Kimliği asıl ürün formundan tıklama anında okuyacak şekilde değiştirdik. Böyle bir hata "
     "sipariş gelene kadar kimseye görünmüyor — kod okuyarak değil, formdaki değerle çubuğun "
     "gönderdiği değeri karşılaştırarak bulunuyor."],
    ["Bir şapka markasında ürün sayfasındaki “Detaylar” paneli mobilde açık başlıyordu. Tek "
     "başına <span class=\"sayi\">845</span> piksel yer kaplıyor, satın alma butonunu "
     "<span class=\"sayi\">1811.</span> piksele itiyordu.",
     "Kapalı başlatınca buton <span class=\"sayi\">1064.</span> piksele geldi, "
     "<span class=\"sayi\">747</span> piksel kazanç. Masaüstünde eski davranışı bozmadık; "
     "orada yer sıkıntısı yoktu."],
    ["Bir katalogda ürün türü alanında <span class=\"sayi\">71</span> farklı değer vardı: "
     "“Yüzük 8”, “Bileklik 15”, “Kolye-5”. Sayılar gramaj değil, sıra numarasıydı.",
     "Google Shopping eşleştirmesi bu yüzden tutmuyor, mağazanın kendi filtresi onlarca sahte "
     "kategori üretiyordu. <span class=\"sayi\">6</span> kategoriye indirdik; eski değerleri "
     "silmeden önce geri dönüş için ayrı bir metafield'a yazdık."],
    ["Bir sepet çekmecesinde sabit bloklar ürün listesinden yer çalıyordu: özet "
     "<span class=\"sayi\">234</span> + başlık <span class=\"sayi\">66</span> + çapraz satış "
     "<span class=\"sayi\">243</span> + alt bölüm <span class=\"sayi\">228</span> piksel. "
     "Ürün satırına <span class=\"sayi\">39</span> piksel kalıyordu.",
     "Ürün satırı <span class=\"sayi\">159</span> piksel olduğu için taşıp çapraz satış "
     "şeridinin altında kayboluyordu. Sabit kalması gereken bloklar dışındaki her şey "
     "kaydırılabilir alanın içine alındı."],
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
    """HTML etiketlerini soker — meta description ve JSON-LD icin."""
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", s)).strip()


def json_kacir(s):
    return duz(s).replace("\\", "\\\\").replace('"', '\\"')


def menu_ogeleri():
    ogeler = [("/", "Ana sayfa"), ("/gelistirme/", "Geliştirme")]
    if UYGULAMALAR:
        ogeler.append(("/uygulamalar/", "Uygulamalar"))
    if ISLER:
        ogeler.append(("/isler/", "İşler"))
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
    <nav class="ust__menu" aria-label="Ana menü">%s</nav>
  </div>
</header>""" % (AD, ROL, "".join(satirlar))


def alt():
    hizmet_ler = "".join('<li><a href="/%s/">%s</a></li>' % (h["slug"], kacir(h["ad"]))
                         for h in HIZMETLER)
    site_ler = []
    if UYGULAMALAR:
        site_ler.append('<li><a href="/uygulamalar/">Uygulamalar</a></li>')
    if ISLER:
        site_ler.append('<li><a href="/isler/">İşler</a></li>')
    site_ler += ['<li><a href="/teknik/">Teknik yaklaşım</a></li>',
                 '<li><a href="/yontem/">Yöntem</a></li>',
                 '<li><a href="/iletisim/">İletişim</a></li>']
    return """<footer class="alt">
  <div class="sarmal sarmal--genis">
    <div class="alt__izgara">
      <div class="alt__sutun alt__sutun--ilk">
        <p class="alt__ad">%(ad)s</p>
        <p class="alt__metin">Shopify için yazılım geliştiriyorum: App Store uygulamaları,
          mağazaya özel uygulamalar, Liquid tema ve Admin API entegrasyonları.</p>
        <p class="alt__mono">Admin GraphQL API · Liquid · Bulk Operations · Webhook</p>
      </div>
      <div class="alt__sutun">
        <p class="alt__baslik">Geliştirme</p>
        <ul>%(hizmetler)s</ul>
      </div>
      <div class="alt__sutun">
        <p class="alt__baslik">Site</p>
        <ul>%(siteler)s</ul>
      </div>
      <div class="alt__sutun">
        <p class="alt__baslik">İletişim</p>
        <ul>
          <li><a href="https://wa.me/%(t)s" target="_blank" rel="noopener">WhatsApp</a></li>
          <li><a href="tel:%(tp)s">%(ty)s</a></li>
          <li><a href="https://taftri.com/" target="_blank" rel="noopener">Taftri — ajans işleri</a></li>
        </ul>
      </div>
    </div>
    <div class="alt__satir">
      <div>&copy; <span id="yil">%(yil)s</span> %(ad)s</div>
      <div><a href="/kvkk.html">KVKK</a> &middot; <a href="/gizlilik.html">Gizlilik</a></div>
    </div>
  </div>
</footer>""" % {"ad": AD, "hizmetler": hizmet_ler, "siteler": "".join(site_ler),
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


def maddeler(liste):
    return '<ul class="maddeler">%s</ul>' % "".join("<li>%s</li>" % m for m in liste)


def alanlar(ciftler):
    return "".join('<div class="alan"><h3>%s</h3><p>%s</p></div>' % (kacir(b), m)
                   for b, m in ciftler)


def kod_blok(baslik, dil, kod, not_metni=""):
    return """
  <section class="kod-bolum" aria-labelledby="kod-h">
    <div class="sarmal sarmal--genis">
      <h2 class="bolum-basligi" id="kod-h">%(baslik)s</h2>
      <figure class="kod">
        <figcaption class="kod__ust"><span class="kod__dil">%(dil)s</span></figcaption>
        <pre><code>%(kod)s</code></pre>
      </figure>
      %(not)s
    </div>
  </section>""" % {"baslik": kacir(baslik), "dil": kacir(dil), "kod": kacir(kod),
                   "not": ('<p class="kod__not">%s</p>' % kacir(not_metni)) if not_metni else ""}


def sss_blok(ciftler, baslik_id="sss-h"):
    if not ciftler:
        return "", None
    govde = "".join('<div class="sss"><h3>%s</h3><p>%s</p></div>' % (kacir(s), c)
                    for s, c in ciftler)
    ld = ('{"@context":"https://schema.org","@type":"FAQPage","mainEntity":[%s]}'
          % ",".join('{"@type":"Question","name":"%s","acceptedAnswer":'
                     '{"@type":"Answer","text":"%s"}}' % (json_kacir(s), json_kacir(c))
                     for s, c in ciftler))
    html = """
  <section aria-labelledby="%s">
    <div class="sarmal">
      <h2 class="bolum-basligi" id="%s">Sık sorulanlar</h2>
      %s
    </div>
  </section>""" % (baslik_id, baslik_id, govde)
    return html, ld


def kart(url, ust_yazi, baslik, ozet, alt_yazi=""):
    return """<a class="kart" href="%s">
          <span class="kart__ust">%s</span>
          <span class="kart__baslik">%s</span>
          <span class="kart__ozet">%s</span>%s
        </a>""" % (url, kacir(ust_yazi), kacir(baslik), kacir(ozet),
                   ('<span class="kart__alt">%s</span>' % kacir(alt_yazi)) if alt_yazi else "")


def cta(baslik, metin, buton="İletişime geç", hedef="/iletisim/"):
    return """
  <section class="cta" aria-labelledby="cta-h">
    <div class="sarmal sarmal--genis">
      <div class="cta__kutu">
        <div>
          <h2 id="cta-h">%s</h2>
          <p>%s</p>
        </div>
        <a class="btn" href="%s">%s</a>
      </div>
    </div>
  </section>""" % (kacir(baslik), kacir(metin), hedef, kacir(buton))


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
<script>document.getElementById('yil').textContent=new Date().getFullYear();</script>
</body>
</html>
""" % {"baslik": kacir(baslik), "aciklama": kacir(aciklama), "kanonik": kanonik,
       "rb": rb, "ld": ld, "ust": ust(aktif_menu), "govde": govde, "alt": alt()}


# ---------------------------------------------------------------------------
# STIL
# ---------------------------------------------------------------------------

STIL = """:root{
  --kagit:#F6F4EF;
  --kagit-2:#FFFFFF;
  --murekkep:#1E201B;
  --murekkep-2:#4F5249;
  --murekkep-3:#6C6F64;
  --cizgi:#E0DCD1;
  --cizgi-2:#CFCABB;
  --yesil:#2F4F3E;
  --yesil-2:#456A56;
  --yesil-yumusak:#E5EDE6;
  --kod-zemin:#1A1C18;
  --kod-metin:#DCE3D6;
  --kod-soluk:#8B9384;
  --genislik:700px;
  --genislik-genis:980px;
  --mono:'JetBrains Mono',ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;
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
  display:flex;flex-direction:column;min-height:100vh;
}
main{flex:1 0 auto}

.sarmal{max-width:var(--genislik);margin:0 auto;padding:0 24px;width:100%}
.sarmal--genis{max-width:var(--genislik-genis)}

a{
  color:var(--yesil);text-decoration:none;
  border-bottom:1px solid rgba(47,79,62,.28);
  transition:border-color .18s ease,color .18s ease;
}
a:hover{color:var(--yesil-2);border-bottom-color:var(--yesil-2)}
a:focus-visible{outline:2px solid var(--yesil);outline-offset:3px;border-radius:2px}

.atla{position:absolute;left:-9999px;top:0;z-index:20;padding:10px 16px;background:var(--yesil);color:#fff;border-bottom:0}
.atla:focus{left:8px;top:8px;color:#fff}

/* ---- ust ---- */
.ust{border-bottom:1px solid var(--cizgi);background:var(--kagit-2)}
.ust__ic{display:flex;align-items:center;justify-content:space-between;gap:10px 28px;flex-wrap:wrap;padding-top:15px;padding-bottom:15px}
.ust__ad{font-family:'Newsreader',Georgia,serif;font-size:18px;font-weight:600;color:var(--murekkep);border-bottom:0;letter-spacing:-.01em;line-height:1.2}
.ust__ad:hover{color:var(--yesil)}
.ust__rol{display:block;font-family:var(--mono);font-size:11px;font-weight:400;letter-spacing:.06em;text-transform:uppercase;color:var(--murekkep-3);margin-top:3px}
.ust__menu{display:flex;flex-wrap:wrap;gap:4px 20px;font-size:15px}
.ust__menu a{color:var(--murekkep-2);border-bottom:2px solid transparent;padding-bottom:2px}
.ust__menu a:hover{color:var(--yesil);border-bottom-color:var(--yesil-yumusak)}
.ust__menu a[aria-current="page"]{color:var(--murekkep);font-weight:600;border-bottom-color:var(--yesil)}

/* ---- kirinti ---- */
.crumbs{list-style:none;display:flex;flex-wrap:wrap;gap:4px 8px;font-family:var(--mono);font-size:12.5px;color:var(--murekkep-3);padding:24px 0 0}
.crumbs li+li::before{content:"/";margin-right:8px;color:var(--cizgi-2)}
.crumbs a{color:var(--murekkep-3);border-bottom-color:transparent}
.crumbs a:hover{color:var(--yesil);border-bottom-color:var(--yesil)}

/* ---- giris ---- */
.giris{padding:64px 0 0}
.giris--ic{padding:22px 0 0}
.ad{font-family:'Newsreader',Georgia,serif;font-size:clamp(32px,5.4vw,45px);font-weight:500;letter-spacing:-.017em;line-height:1.13}
.ad--ic{font-size:clamp(28px,4.6vw,37px)}
.rol{font-family:var(--mono);font-size:12.5px;letter-spacing:.04em;text-transform:uppercase;color:var(--murekkep-3);margin-bottom:12px}
.giris p:not(.rol){margin-top:24px;font-size:19px;line-height:1.7;color:var(--murekkep-2);max-width:58ch}
.giris p:not(.rol)+p{margin-top:16px}
.giris strong{font-weight:700;color:var(--murekkep)}

section{padding:54px 0}
section:first-of-type{padding-top:50px}
.bolum-basligi{
  font-family:var(--mono);font-size:12.5px;font-weight:500;letter-spacing:.09em;
  text-transform:uppercase;color:var(--murekkep-3);
  padding-bottom:12px;border-bottom:1px solid var(--cizgi);margin-bottom:28px;
}
.bolum-giris{color:var(--murekkep-2);max-width:62ch;margin-bottom:26px}

.alan{padding:22px 0;border-bottom:1px solid var(--cizgi)}
.alan:last-child{border-bottom:0;padding-bottom:0}
.alan h3{font-family:'Newsreader',Georgia,serif;font-size:21px;font-weight:500;letter-spacing:-.01em;margin-bottom:6px}
.alan p{color:var(--murekkep-2);max-width:64ch}

.ornek{padding:26px 0;border-bottom:1px solid var(--cizgi)}
.ornek:last-child{border-bottom:0;padding-bottom:0}
.ornek p{color:var(--murekkep-2);max-width:64ch}
.ornek p+p{margin-top:12px}
.sayi{font-family:var(--mono);font-size:.94em;font-weight:500;color:var(--murekkep);white-space:nowrap}

/* ---- kod ---- */
.kod-bolum{padding-top:44px;padding-bottom:44px}
.kod{margin-top:2px;border-radius:8px;overflow:hidden;border:1px solid var(--kod-zemin);background:var(--kod-zemin)}
.kod__ust{display:flex;align-items:center;gap:8px;padding:9px 16px;border-bottom:1px solid rgba(220,227,214,.12)}
.kod__dil{font-family:var(--mono);font-size:11.5px;letter-spacing:.09em;text-transform:uppercase;color:var(--kod-soluk)}
.kod pre{margin:0;padding:18px 16px 20px;overflow-x:auto}
.kod code{font-family:var(--mono);font-size:13.5px;line-height:1.66;color:var(--kod-metin);white-space:pre;display:block}
.kod__not{margin-top:16px;color:var(--murekkep-2);max-width:64ch;font-size:16px}

/* ---- yuzeyler ---- */
.yuzeyler{display:grid;gap:0;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));border-top:1px solid var(--cizgi)}
.yuzey{padding:15px 0;border-bottom:1px solid var(--cizgi)}
.yuzey__ad{font-family:var(--mono);font-size:14px;font-weight:500;color:var(--murekkep);display:block}
.yuzey__not{font-size:15px;color:var(--murekkep-3);margin-top:2px;max-width:40ch}
@media (min-width:760px){
  .yuzeyler{column-gap:36px}
}

/* ---- kartlar ---- */
.kartlar{display:grid;gap:14px;grid-template-columns:repeat(auto-fill,minmax(258px,1fr))}
.kart{display:flex;flex-direction:column;gap:6px;padding:22px 24px;background:var(--kagit-2);border:1px solid var(--cizgi);border-radius:8px;color:inherit;transition:border-color .18s ease,box-shadow .18s ease,transform .18s ease}
.kart:hover{border-color:var(--yesil-2);box-shadow:0 2px 14px rgba(30,32,27,.07);transform:translateY(-1px)}
.kart__ust{font-family:var(--mono);font-size:11.5px;letter-spacing:.07em;text-transform:uppercase;color:var(--murekkep-3)}
.kart__baslik{font-family:'Newsreader',Georgia,serif;font-size:20px;font-weight:500;line-height:1.25;color:var(--murekkep)}
.kart__ozet{color:var(--murekkep-2);font-size:16px;line-height:1.6}
.kart__alt{margin-top:4px;font-family:var(--mono);font-size:12.5px;color:var(--murekkep-3)}

.rozetler{display:flex;flex-wrap:wrap;gap:8px 9px;margin-top:22px}
.rozet{font-family:var(--mono);font-size:12.5px;padding:5px 11px;border:1px solid var(--cizgi-2);border-radius:5px;color:var(--murekkep-2);background:var(--kagit-2)}

.markalar{display:flex;flex-wrap:wrap;gap:8px 10px}
.marka{font-size:15px;padding:7px 14px;border:1px solid var(--cizgi);border-radius:999px;color:var(--murekkep-2);background:var(--kagit-2);transition:border-color .18s ease,color .18s ease,background .18s ease}
a.marka:hover{color:var(--yesil);border-color:var(--yesil-2);background:var(--yesil-yumusak)}

.maddeler{list-style:none;margin-top:4px}
.maddeler li{position:relative;padding-left:20px;color:var(--murekkep-2);max-width:64ch;margin-top:8px}
.maddeler li::before{content:"";position:absolute;left:2px;top:12px;width:7px;height:1px;background:var(--yesil)}

.durum{display:inline-block;font-family:var(--mono);font-size:12px;letter-spacing:.05em;text-transform:uppercase;padding:4px 11px;border-radius:5px;background:var(--yesil-yumusak);color:var(--yesil);margin-top:14px}

.btn{display:inline-block;padding:11px 22px;border-radius:6px;background:var(--yesil);color:#fff;font-weight:600;font-size:16px;border-bottom:0;transition:background .18s ease;white-space:nowrap}
.btn:hover{background:var(--yesil-2);color:#fff;border-bottom:0}

.gorsel{margin-top:24px;width:100%;height:auto;border:1px solid var(--cizgi);border-radius:8px}

.sss{padding:20px 0;border-bottom:1px solid var(--cizgi)}
.sss:last-child{border-bottom:0;padding-bottom:0}
.sss h3{font-family:'Newsreader',Georgia,serif;font-size:19px;font-weight:500;margin-bottom:6px}
.sss p{color:var(--murekkep-2);max-width:64ch}

.taftri{padding:26px 28px;background:var(--yesil-yumusak);border-left:2px solid var(--yesil);border-radius:0 6px 6px 0}
.taftri h3{font-family:'Newsreader',Georgia,serif;font-size:20px;font-weight:500;margin-bottom:8px}
.taftri p{color:var(--murekkep-2);max-width:56ch}
.taftri a{font-weight:500}

.cta{padding-top:14px}
.cta__kutu{display:flex;flex-wrap:wrap;align-items:center;justify-content:space-between;gap:20px 32px;padding:30px 32px;background:var(--kagit-2);border:1px solid var(--cizgi);border-radius:10px}
.cta__kutu h2{font-family:'Newsreader',Georgia,serif;font-size:23px;font-weight:500;letter-spacing:-.01em}
.cta__kutu p{color:var(--murekkep-2);max-width:52ch;margin-top:6px}

.iletisim-satir{display:flex;flex-wrap:wrap;gap:18px 40px;font-size:18px;margin-top:4px}
.iletisim-satir span{font-family:var(--mono);color:var(--murekkep-3);font-size:12px;display:block;margin-bottom:3px;letter-spacing:.06em;text-transform:uppercase}
.devam{margin-top:22px;margin-bottom:0}

/* ---- alt ---- */
.alt{flex-shrink:0;margin-top:30px;padding:48px 0 40px;border-top:1px solid var(--cizgi);background:var(--kagit-2);color:var(--murekkep-3);font-size:15px}
.alt__izgara{display:grid;gap:30px 32px;grid-template-columns:repeat(auto-fit,minmax(178px,1fr))}
.alt__sutun--ilk{grid-column:span 2;min-width:240px}
.alt__ad{font-family:'Newsreader',Georgia,serif;font-size:18px;font-weight:600;color:var(--murekkep)}
.alt__metin{margin-top:8px;max-width:44ch;line-height:1.6}
.alt__mono{margin-top:12px;font-family:var(--mono);font-size:12px;color:var(--murekkep-3);line-height:1.8}
.alt__baslik{font-family:var(--mono);font-size:11.5px;letter-spacing:.09em;text-transform:uppercase;color:var(--murekkep-2);margin-bottom:10px}
.alt__sutun ul{list-style:none}
.alt__sutun li{margin-top:7px;line-height:1.45}
.alt a{color:var(--murekkep-3);border-bottom-color:transparent}
.alt a:hover{color:var(--yesil);border-bottom-color:var(--yesil)}
.alt__satir{display:flex;flex-wrap:wrap;gap:8px 20px;justify-content:space-between;margin-top:38px;padding-top:20px;border-top:1px solid var(--cizgi);font-size:14px}

@media (max-width:700px){
  .alt__sutun--ilk{grid-column:span 2}
}
@media (max-width:600px){
  body{font-size:16px}
  .ust__ic{padding-top:14px;padding-bottom:14px}
  .ust__menu{gap:4px 15px;font-size:14.5px}
  .giris{padding-top:40px}
  .giris p:not(.rol){font-size:17.5px}
  section{padding:38px 0}
  section:first-of-type{padding-top:36px}
  .taftri{padding:22px 20px}
  .kart{padding:20px}
  .cta__kutu{padding:24px 22px}
  .kod code{font-size:12.5px}
  .alt__izgara{gap:26px 24px}
  .alt__sutun--ilk{grid-column:span 1}
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
            '"Shopify Admin GraphQL API","Liquid tema geliştirme","Webhook",'
            '"E-ticaret entegrasyonu","Katalog ve veri düzeni"],'
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

def yuzey_bolumu():
    ler = "".join('<div class="yuzey"><span class="yuzey__ad">%s</span>'
                  '<span class="yuzey__not">%s</span></div>'
                  % (kacir(a), kacir(n)) for a, n in YUZEYLER)
    return """
  <section aria-labelledby="yuzey-h">
    <div class="sarmal sarmal--genis">
      <h2 class="bolum-basligi" id="yuzey-h">Çalıştığım platform yüzeyleri</h2>
      <div class="yuzeyler">%s</div>
    </div>
  </section>""" % ler


def ana_sayfa():
    baslik = "%s — Shopify uygulama geliştiricisi" % AD
    aciklama = ("Shopify için yazılım geliştiriyorum: App Store uygulamaları, mağazaya "
                "özel uygulamalar, Liquid tema geliştirme ve Admin API entegrasyonları.")

    hizmet_kartlari = "".join(
        kart("/%s/" % h["slug"], "Geliştirme", h["ad"], h["ozet"]) for h in HIZMETLER)

    parcalar = ["""
  <div class="sarmal">
    <header class="giris">
      <p class="rol">Shopify · Admin GraphQL API · Liquid</p>
      <h1 class="ad">Shopify için yazılım geliştiriyorum</h1>
      <p>Bir kısmı App Store'da herkese açık uygulama olarak çıkıyor, bir kısmı tek bir
        mağaza için yazılıp orada kalıyor. Tema ve entegrasyon işleri de aynı elden.</p>
      <p>İkisinin ortak yanı şu: iş yeni bir şey icat etmekle değil,
        <strong>ölçmekle</strong> başlıyor. Bir butonun sayfanın kaçıncı pikselinde
        durduğunu bilmeden onu yukarı almanın anlamı yok.</p>
    </header>
  </div>

  <section aria-labelledby="alanlar-h">
    <div class="sarmal sarmal--genis">
      <h2 class="bolum-basligi" id="alanlar-h">Ne geliştiriyorum</h2>
      <div class="kartlar">%s</div>
      <p class="devam"><a href="/gelistirme/">Geliştirme alanlarının tamamı</a></p>
    </div>
  </section>""" % hizmet_kartlari]

    parcalar.append(yuzey_bolumu())

    if UYGULAMALAR:
        kartlar = "".join(
            kart("/uygulamalar/%s/" % u["slug"],
                 DURUM_ADI.get(u.get("durum", ""), "Uygulama"),
                 u["ad"], u["ozet"], u.get("fiyat", ""))
            for u in UYGULAMALAR[:3])
        parcalar.append("""
  <section aria-labelledby="uygulamalar-h">
    <div class="sarmal sarmal--genis">
      <h2 class="bolum-basligi" id="uygulamalar-h">Uygulamalar</h2>
      <div class="kartlar">%s</div>
      <p class="devam"><a href="/uygulamalar/">Tüm uygulamalar</a></p>
    </div>
  </section>""" % kartlar)

    if ISLER:
        kartlar = "".join(
            kart("/isler/%s/" % i["slug"], TUR_ADI.get(i.get("tur", ""), "İş"),
                 i["baslik"], i["ozet"], i.get("musteri", ""))
            for i in ISLER[:3])
        parcalar.append("""
  <section aria-labelledby="isler-h">
    <div class="sarmal sarmal--genis">
      <h2 class="bolum-basligi" id="isler-h">Yapılmış işler</h2>
      <div class="kartlar">%s</div>
      <p class="devam"><a href="/isler/">Tüm işler</a></p>
    </div>
  </section>""" % kartlar)

    parcalar.append(kod_blok("Binlerce kayıtlık iş nasıl yürür", "graphql", KOD_BULK,
                             "Toplu işlem sonucu JSONL dosyası olarak indirilir. Aynı "
                             "veriyi sayfa sayfa çekmek hem hız limitini yakar hem yarıda "
                             "kalırsa nereden devam edeceğini bilemezsin."))

    parcalar.append("""
  <section aria-labelledby="yontem-h">
    <div class="sarmal">
      <h2 class="bolum-basligi" id="yontem-h">Nasıl çalışıyorum</h2>
      <div class="ornek">%s</div>
      <p class="devam"><a href="/yontem/">Ölçüm örneklerinin tamamı</a> &middot;
        <a href="/teknik/">teknik yaklaşım</a></p>
    </div>
  </section>""" % "".join("<p>%s</p>" % p for p in VAKALAR[0]))

    marka_html = "".join('<a class="marka" href="%s" target="_blank" rel="noopener">%s</a>'
                         % (u, kacir(a)) for a, u in MARKALAR)
    parcalar.append("""
  <section aria-labelledby="markalar-h">
    <div class="sarmal sarmal--genis">
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

    parcalar.append(cta("Aklınızda bir şey var mı?",
                        "Ne yapılması gerektiğini söylemek çoğu zaman kısa sürüyor."))

    return sayfa(baslik, aciklama, SITE + "/", "/", "".join(parcalar),
                 [ld_kisi(), ld_site()])


def gelistirme_hub():
    baslik = "Geliştirme alanları — %s" % AD
    aciklama = ("Shopify App Store uygulaması, mağazaya özel uygulama, Liquid tema "
                "geliştirme ve Admin API entegrasyonu. Hangisi hangi işe uygun.")
    kb, kld = kirinti([("Ana sayfa", "/"), ("Geliştirme", None)])
    kartlar = "".join(kart("/%s/" % h["slug"], "Geliştirme", h["ad"], h["ozet"])
                      for h in HIZMETLER)
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
      <p>Dört ayrı iş kolu. Hangisinin gerektiği çoğu zaman baştan belli olmuyor — aynı
        istek bazen tema içinde, bazen uygulamayla çözülüyor. Kararı ölçtükten sonra
        veriyorum; genelde daha az bağımlılık getiren yol kazanıyor.</p>
    </header>
  </div>

  <section aria-label="Geliştirme alanları">
    <div class="sarmal sarmal--genis"><div class="kartlar">%(kartlar)s</div></div>
  </section>

  <section aria-labelledby="hangisi-h">
    <div class="sarmal">
      <h2 class="bolum-basligi" id="hangisi-h">Hangisi size uygun</h2>
      %(karar)s
    </div>
  </section>
%(yuzey)s
%(cta)s""" % {
        "kb": kb, "kartlar": kartlar, "yuzey": yuzey_bolumu(),
        "karar": alanlar([
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
    diger_kartlar = "".join(kart("/%s/" % d["slug"], "Geliştirme", d["ad"], d["ozet"])
                            for d in digerleri)
    sss_html, sss_ld = sss_blok(h.get("sss", []))
    kod_html = ""
    if h.get("kod"):
        kod_html = kod_blok(h["kod"][0], h["kod"][1], h["kod"][2], h.get("kod_not", ""))

    govde = """
  <div class="sarmal">%(kb)s
    <header class="giris giris--ic">
      <p class="rol">Geliştirme</p>
      <h1 class="ad ad--ic">%(h1)s</h1>
      %(giris)s
    </header>
  </div>

  <section aria-labelledby="kapsam-h">
    <div class="sarmal">
      <h2 class="bolum-basligi" id="kapsam-h">%(kapsam_basligi)s</h2>
      %(kapsam)s
      %(rozet)s
    </div>
  </section>
%(kod)s
  <section aria-labelledby="surec-h">
    <div class="sarmal">
      <h2 class="bolum-basligi" id="surec-h">Nasıl yürüyor</h2>
      %(surec)s
      <p class="devam"><a href="/teknik/">Teknik yaklaşım</a> &middot;
        <a href="/yontem/">ölçüm örnekleri</a></p>
    </div>
  </section>
%(sss)s
  <section aria-labelledby="diger-h">
    <div class="sarmal sarmal--genis">
      <h2 class="bolum-basligi" id="diger-h">Diğer geliştirme alanları</h2>
      <div class="kartlar">%(diger)s</div>
    </div>
  </section>
%(cta)s""" % {
        "kb": kb, "h1": kacir(h["baslik"]),
        "giris": "".join("<p>%s</p>" % p for p in h["giris"]),
        "kapsam_basligi": kacir(h["kapsam_basligi"]),
        "kapsam": alanlar(h["kapsam"]),
        "rozet": rozetler(h.get("teknik", [])),
        "kod": kod_html,
        "surec": alanlar(SUREC),
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
    aciklama = ("API sürüm yönetimi, hız limiti, webhook imza doğrulama, idempotent "
                "işleme, geri alınabilir toplu iş ve doğrulama disiplini.")
    kb, kld = kirinti([("Ana sayfa", "/"), ("Teknik", None)])
    govde = """
  <div class="sarmal sarmal--genis">%(kb)s
    <header class="giris giris--ic">
      <p class="rol">Teknik yaklaşım</p>
      <h1 class="ad ad--ic">Nasıl yazıyorum</h1>
      <p>Aşağıdakiler tercih değil, sahada bir kere kaybedip öğrenilmiş kurallar.
        Hepsi bir hataya mal olmuş; bu yüzden istisnasız uygulanıyor.</p>
    </header>
  </div>

  <section aria-labelledby="ilke-h">
    <div class="sarmal">
      <h2 class="bolum-basligi" id="ilke-h">İlkeler</h2>
      %(ilkeler)s
    </div>
  </section>
%(kod1)s
%(kod2)s
%(yuzey)s
%(cta)s""" % {
        "kb": kb,
        "ilkeler": alanlar(TEKNIK_ILKELER),
        "kod1": kod_blok("Webhook imzası doğrulanmadan hiçbir şey işlenmez", "js", KOD_HMAC,
                         "İmza doğrulaması olmayan bir webhook ucu, herkesin veri "
                         "yazabildiği açık bir kapıdır."),
        "kod2": kod_blok("Boş render eden blok bırakmamak", "liquid", KOD_BOLUM,
                         "Bir mağazada silinmiş bir ürüne işaret eden hediye bloğu "
                         "aylarca sessizce boş basmıştı. Koşul olmadan yazılan her "
                         "referanslı blok aynı riski taşır."),
        "yuzey": yuzey_bolumu(),
        "cta": cta("Mevcut kurulumunuz bu ölçütleri karşılıyor mu?",
                   "Bakıp ne gördüğümü yazayım — mağazanın adresi yeterli."),
    }
    return sayfa(baslik, aciklama, SITE + "/teknik/", "/teknik/", govde, [kld])


def yontem_sayfasi():
    baslik = "Nasıl çalışıyorum — %s" % AD
    aciklama = ("Ölçerek teşhis, yazılı kapsam, ayrı temada geliştirme ve ölçülmüş "
                "teslim. Sahadan beş ölçüm örneği.")
    kb, kld = kirinti([("Ana sayfa", "/"), ("Yöntem", None)])
    vaka_html = "".join('<div class="ornek">%s</div>' % "".join("<p>%s</p>" % p for p in v)
                        for v in VAKALAR)
    govde = """
  <div class="sarmal">%(kb)s
    <header class="giris giris--ic">
      <p class="rol">Yöntem</p>
      <h1 class="ad ad--ic">Nasıl çalışıyorum</h1>
      <p>İşin büyük kısmı yeni bir şey icat etmekle değil, hâlihazırda para kaybettiren
        yeri bulmakla geçiyor. Bunun tek yolu <strong>ölçmek</strong>.</p>
    </header>
  </div>

  <section aria-labelledby="surec-h">
    <div class="sarmal">
      <h2 class="bolum-basligi" id="surec-h">Süreç</h2>
      %(surec)s
    </div>
  </section>

  <section aria-labelledby="vaka-h">
    <div class="sarmal">
      <h2 class="bolum-basligi" id="vaka-h">Ölçüm örnekleri</h2>
      <p class="bolum-giris">Hepsi gerçek mağazalarda ölçüldü. Rakamlar tahmin değil,
        çalışan sayfadan okunan değerler.</p>
      %(vakalar)s
    </div>
  </section>

  <section aria-labelledby="yapmam-h">
    <div class="sarmal">
      <h2 class="bolum-basligi" id="yapmam-h">Yapmadıklarım</h2>
      %(yapmam)s
      <p class="devam"><a href="/teknik/">Teknik ilkelerin tamamı</a></p>
    </div>
  </section>
%(cta)s""" % {"kb": kb, "surec": alanlar(SUREC), "vakalar": vaka_html,
              "yapmam": maddeler([kacir(m) for m in YAPMADIKLARIM]),
              "cta": cta("Sizde ne ölçülmeli?",
                         "Mağazanın adresini yollayın; bakıp ne gördüğümü yazayım.")}
    return sayfa(baslik, aciklama, SITE + "/yontem/", "/yontem/", govde, [kld])


def iletisim_sayfasi():
    baslik = "İletişim — %s" % AD
    aciklama = ("Shopify uygulama, tema ve entegrasyon işleri için iletişim. WhatsApp ve "
                "telefon; ajans işleri Taftri üzerinden.")
    kb, kld = kirinti([("Ana sayfa", "/"), ("İletişim", None)])
    govde = """
  <div class="sarmal">%(kb)s
    <header class="giris giris--ic">
      <p class="rol">İletişim</p>
      <h1 class="ad ad--ic">Yazın, bakalım</h1>
      <p>Bir fikir ya da tıkanmış bir iş varsa yazın. Ne yapılması gerektiğini söylemek
        çoğu zaman kısa sürüyor; bunun için ücret almıyorum.</p>
    </header>
  </div>

  <section aria-labelledby="kanal-h">
    <div class="sarmal">
      <h2 class="bolum-basligi" id="kanal-h">Doğrudan</h2>
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
  </section>

  <section aria-labelledby="ne-h">
    <div class="sarmal">
      <h2 class="bolum-basligi" id="ne-h">Yazarken şunlar işi hızlandırır</h2>
      %(ne)s
    </div>
  </section>

  <section aria-labelledby="taftri-h">
    <div class="sarmal">
      <h2 class="bolum-basligi" id="taftri-h">Ajans işleri</h2>
      <div class="taftri">
        <h3>Taftri</h3>
        <p>Sürekli reklam yönetimi, içerik üretimi ve uzun soluklu mağaza operasyonu
          <a href="https://taftri.com/" rel="noopener">taftri.com</a> üzerinden yürüyor.</p>
      </div>
    </div>
  </section>""" % {
        "kb": kb, "t": TELEFON.lstrip("+"), "tp": TELEFON, "ty": TELEFON_YAZI,
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
             u["ad"], u["ozet"], u.get("fiyat", ""))
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
      <p>Her birinin sayfasında hangi sorunu çözdüğü, ne yaptığı ve hangi platform
        uçlarını kullandığı yazılı.</p>
    </header>
  </div>
  <section aria-label="Uygulama listesi">
    <div class="sarmal sarmal--genis"><div class="kartlar">%s</div></div>
  </section>
%s""" % (kb, kartlar, cta("Benzer bir uygulama mı gerekiyor?",
                          "Aynı ihtiyaç sizde de varsa yazın; mevcut uygulama işinizi "
                          "görüyor mu bakalım."))
    return sayfa(baslik, aciklama, SITE + "/uygulamalar/", "/uygulamalar/",
                 govde, [kld, liste_ld])


def uygulama_sayfasi(u):
    baslik = "%s — Shopify uygulaması" % u["ad"]
    aciklama = duz(u["ozet"])[:155]
    yol = "/uygulamalar/%s/" % u["slug"]
    kb, kld = kirinti([("Ana sayfa", "/"), ("Uygulamalar", "/uygulamalar/"), (u["ad"], None)])

    durum = DURUM_ADI.get(u.get("durum", ""))
    parcalar = ["""
  <div class="sarmal">%s
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
        ('<p style="margin-top:20px"><a class="btn" href="%s" target="_blank" '
         'rel="noopener">App Store\'da aç</a></p>' % u["app_store"])
        if u.get("app_store") else "")]

    if u.get("gorsel"):
        parcalar.append('\n  <div class="sarmal sarmal--genis"><img class="gorsel" src="%s" '
                        'alt="%s" loading="lazy" /></div>'
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

    if u.get("kod"):
        parcalar.append(kod_blok(u["kod"][0], u["kod"][1], u["kod"][2], u.get("kod_not", "")))

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


def is_listesi():
    baslik = "Yapılmış işler — %s" % AD
    aciklama = ("Shopify mağazaları için yazdığım özel uygulamalar, tema özellikleri ve "
                "entegrasyonlar; başlangıç durumu ve ölçülmüş sonuçlarıyla.")
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
    govde = """
  <div class="sarmal sarmal--genis">%s
    <header class="giris giris--ic">
      <p class="rol">İşler</p>
      <h1 class="ad ad--ic">Yapılmış işler</h1>
      <p>Her kayıtta işin başlangıç durumu, ne yapıldığı ve mümkün olduğunda ölçülmüş
        sonucu yazılı. Rakam yoksa rakam yazılmıyor.</p>
    </header>
  </div>
  <section aria-label="İş listesi">
    <div class="sarmal sarmal--genis"><div class="kartlar">%s</div></div>
  </section>
%s""" % (kb, kartlar, cta("Benzer bir işiniz mi var?",
                         "Durumu anlatın; ölçüp ne gerektiğini söyleyeyim."))
    return sayfa(baslik, aciklama, SITE + "/isler/", "/isler/", govde, [kld, liste_ld])


def is_sayfasi(i):
    baslik = "%s — %s" % (i["baslik"], i["musteri"])
    if len(baslik) > 65:
        baslik = i["baslik"]
    aciklama = duz(i["ozet"])[:155]
    yol = "/isler/%s/" % i["slug"]
    kb, kld = kirinti([("Ana sayfa", "/"), ("İşler", "/isler/"), (i["baslik"], None)])

    musteri_html = kacir(i["musteri"])
    if i.get("musteri_url"):
        musteri_html = ('<a href="%s" target="_blank" rel="noopener">%s</a>'
                        % (i["musteri_url"], musteri_html))

    parcalar = ["""
  <div class="sarmal">%s
    <header class="giris giris--ic">
      <p class="rol">%s</p>
      <h1 class="ad ad--ic">%s</h1>
      <p>%s</p>
      <p style="font-size:16px">Müşteri: %s</p>
    </header>
  </div>""" % (kb, kacir(TUR_ADI.get(i.get("tur", ""), "İş")), kacir(i["baslik"]),
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

    if i.get("kod"):
        parcalar.append(kod_blok(i["kod"][0], i["kod"][1], i["kod"][2], i.get("kod_not", "")))

    if i.get("sonuc"):
        parcalar.append("""
  <section aria-labelledby="sonuc-h">
    <div class="sarmal">
      <h2 class="bolum-basligi" id="sonuc-h">Sonuç</h2>
      %s
    </div>
  </section>""" % maddeler([kacir(m) for m in i["sonuc"]]))

    parcalar.append(cta("Sizde de benzer bir durum mu var?",
                        "Mağazanın adresini yollayın; bakıp ne gördüğümü yazayım."))

    is_ld = ('{"@context":"https://schema.org","@type":"CreativeWork",'
             '"name":"%s","description":"%s","inLanguage":"tr-TR",'
             '"creator":{"@type":"Person","name":"%s"},'
             '"about":{"@type":"Organization","name":"%s"%s}}'
             % (json_kacir(i["baslik"]), json_kacir(i["ozet"]), AD,
                json_kacir(i["musteri"]),
                (',"url":"%s"' % i["musteri_url"]) if i.get("musteri_url") else ""))
    return sayfa(baslik, aciklama, SITE + yol, "/isler/", "".join(parcalar), [kld, is_ld])


def dort_yuz_dort():
    kartlar = "".join(kart("/%s/" % h["slug"], "Geliştirme", h["ad"], h["ozet"])
                      for h in HIZMETLER)
    govde = """
  <div class="sarmal">
    <header class="giris">
      <p class="rol">404</p>
      <h1 class="ad">Sayfa bulunamadı</h1>
      <p>Aradığınız adres taşınmış ya da hiç var olmamış olabilir. Geliştirme alanları
        yerinde duruyor:</p>
    </header>
  </div>
  <section aria-label="Geliştirme alanları">
    <div class="sarmal sarmal--genis"><div class="kartlar">%s</div></div>
  </section>""" % kartlar
    return sayfa("Sayfa bulunamadı — %s" % AD, "Aradığınız sayfa bulunamadı.",
                 SITE + "/404.html", "", govde, (), robots="noindex, follow")


def yonlendirme(baslik, metin, hedef):
    """Eski .html adresleri icin istemci tarafi yonlendirme sayfasi."""
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
    background:#F6F4EF;color:#1E201B;font-family:ui-sans-serif,system-ui,'Segoe UI',sans-serif;
    line-height:1.6;padding:24px}
  .kutu{max-width:420px;text-align:center}
  h1{font-family:Georgia,serif;font-size:22px;font-weight:500;margin:0 0 10px}
  p{margin:0 0 18px;color:#4F5249;font-size:16px}
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
    if ISLER:
        yollar.append("/isler/")
        yollar += ["/isler/%s/" % i["slug"] for i in ISLER]
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
        "> Shopify için yazılım geliştiricisi. App Store uygulamaları, mağazaya özel",
        "> uygulamalar, Liquid tema geliştirme ve Admin API entegrasyonları.",
        "",
        "## Sayfalar",
        "",
        "- [Ana sayfa](%s/): ne geliştirdiği, çalıştığı platform yüzeyleri, markalar." % SITE,
        "- [Geliştirme](%s/gelistirme/): dört geliştirme alanı ve hangisinin hangi işe uygun olduğu." % SITE,
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
            '<rect width="64" height="64" rx="12" fill="#2F4F3E"/>'
            '<text x="32" y="43" font-family="Georgia,serif" font-size="28" '
            'font-weight="600" fill="#F6F4EF" text-anchor="middle">MF</text></svg>\n')


# ---------------------------------------------------------------------------
# CALISTIR
# ---------------------------------------------------------------------------

def main():
    yaz("assets/stil.css", STIL)
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

    if ISLER:
        yaz("isler/index.html", is_listesi())
        for i in ISLER:
            yaz("isler/%s/index.html" % i["slug"], is_sayfasi(i))

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
    print("Uygulama: %d   Is: %d" % (len(UYGULAMALAR), len(ISLER)))


if __name__ == "__main__":
    main()
