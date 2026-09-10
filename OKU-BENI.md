# mftoktay.com

Statik site. GitHub Pages üzerinden `CNAME` ile yayında.

## Kural

Sitedeki `.html` dosyalarını **elle düzenleme.** Hepsi `uret.py` tarafından
üretiliyor; bir sonraki çalıştırmada elle yapılan değişiklik silinir.

İçerik değişikliği `uret.py` içinde yapılır, sonra:

```bash
python uret.py
```

Elle bakımı yapılan tek istisna: `kvkk.html` ve `gizlilik.html`.

## Sayfa yapısı

Her sayfanın kendi üst menüsü ve tam alt bilgisi var; tek sayfa yığını yok.

```
/                       ana sayfa
/gelistirme/            geliştirme alanları — dört sayfaya dağıtır
/uygulama-gelistirme/   App Store uygulaması
/ozel-yazilim/          mağazaya özel uygulama
/tema-gelistirme/       Liquid tema
/entegrasyon/           Admin API, toplu veri, dış sistem
/teknik/                teknik yaklaşım — API sürümü, hız limiti, webhook, geri alma
/yontem/                süreç ve ölçüm örnekleri
/iletisim/              iletişim
/uygulamalar/<slug>/    UYGULAMALAR listesi doluysa
/isler/<slug>/          ISLER listesi doluysa
```

## Örnek eklemek

`uret.py` içinde iki boş liste var. Liste boşken ilgili bölüm, liste sayfası ve
menü öğesi hiç üretilmez — boş sayfa yayına çıkmaz. İlk kayıt eklendiği anda
menü, ana sayfa bölümü, liste sayfası, detay sayfası, sitemap ve llms.txt
kendiliğinden belirir.

### App Store uygulaması

`UYGULAMALAR` listesine ekle:

```python
{
    "slug": "urun-etiket-yoneticisi",
    "ad": "Ürün Etiket Yöneticisi",
    "ozet": "Binlerce ürünün etiketini kurala göre topluca düzenler.",
    "durum": "yayinda",                 # yayinda | inceleme | gelistirme
    "app_store": "https://apps.shopify.com/...",   # boşsa buton basılmaz
    "fiyat": "Ücretsiz plan + $9/ay",              # boşsa satır basılmaz
    "sorun": "Etiket düzeni bozulduğunda koleksiyon kuralları sessizce boşalır...",
    "cozum": ["Kural yazıp önizleme alır", "Geri alma kaydı tutar"],
    "teknik": ["Admin GraphQL API", "Bulk Operations", "webhook"],
    "kod": ("Kural motoru", "graphql", KOD_ORNEK),  # opsiyonel kod bloğu
    "kod_not": "Kod bloğunun altına düşen açıklama.",
    "gorsel": "/assets/uygulama-urun-etiket-yoneticisi.png",   # boşsa basılmaz
    "gorsel_alt": "Ekran görüntüsü: kural düzenleyici",
    "sss": [("Kaç ürüne kadar çalışır?", "Sınır yok, toplu işlem uçları kullanılıyor.")],
},
```

### Yapılmış iş / vaka

`ISLER` listesine ekle:

```python
{
    "slug": "kuyumcu-sabit-sepet-cubugu",
    "baslik": "Varyant senkronlu sabit sepet çubuğu",
    "musteri": "Ömer Has Kuyumculuk",
    "musteri_url": "https://omerhaskuyumculuk.com/",
    "tur": "ozel-uygulama",             # ozel-uygulama | tema | entegrasyon | otomasyon
    "ozet": "Sabit çubuk yanlış varyantı sepete atıyordu.",
    "sorun": "Çubuk varyant kimliğini sayfa yüklenirken okuyup sabitliyordu...",
    "yapilan": ["Kimlik asıl ürün formundan tıklama anında okunuyor"],
    "sonuc": ["Form 49143197565147, çubuk 48748885934299 — fark kapandı"],
    "teknik": ["Liquid", "Shopify Ajax API"],
    "kod": ("Kimlik okuma", "js", KOD_ORNEK),   # opsiyonel
},
```

`sonuc` alanı boş bırakılabilir; ölçülmüş rakam yoksa bölüm hiç basılmaz.
Uydurma rakam yazma.

### Kod bloğu

Kod örnekleri dosyanın üstünde `KOD_` ile başlayan sabitlerde tutuluyor
(`KOD_BULK`, `KOD_HMAC`, `KOD_BOLUM`). Yeni bir örnek eklerken oraya bir sabit
yaz, sonra `"kod": ("Başlık", "graphql", KOD_YENI)` biçiminde bağla.
Dil etiketi serbest metin: `graphql`, `js`, `liquid`, `bash`, `json`.

## Diğer içerik listeleri

| Sabit | Ne besliyor |
|---|---|
| `HIZMETLER` | dört geliştirme sayfası; yeni bir alan eklemek için buraya bir sözlük |
| `YUZEYLER` | "Çalıştığım platform yüzeyleri" listesi |
| `TEKNIK_ILKELER` | `/teknik/` sayfasındaki ilkeler |
| `SUREC` | her geliştirme sayfasındaki "Nasıl yürüyor" adımları |
| `VAKALAR` | `/yontem/` sayfasındaki ölçüm örnekleri |
| `YAPMADIKLARIM` | `/yontem/` sayfasındaki kırmızı çizgiler |
| `MARKALAR` | ana sayfadaki marka şeridi |

## Üretilen dosyalar

Sayfalar + `assets/stil.css` · `favicon.svg` · `404.html` · `sitemap.xml` ·
`robots.txt` · `llms.txt` · IndexNow anahtar dosyası · üç eski adres yönlendirmesi
(`iletisim.html`, `hizmetler.html`, `iade.html`).

## Yayınlama

```bash
python uret.py
git add -A
git commit -m "feat: ..."
git push
```
