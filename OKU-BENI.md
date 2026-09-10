# mftoktay.com

Statik site. GitHub Pages üzerinden `CNAME` ile yayında.

## Kural

Sitedeki `.html` dosyalarını **elle düzenleme.** Hepsi `uret.py` tarafından
üretiliyor; bir sonraki çalıştırmada elle yapılan değişiklik silinir.

İçerik değişikliği `uret.py` içinde yapılır, sonra:

```bash
python uret.py
```

Elle bakımı yapılan tek istisna: `kvkk.html`, `gizlilik.html` ve üç
yönlendirme sayfası (`hizmetler.html`, `iletisim.html`, `iade.html`).

## Örnek eklemek

`uret.py` içinde iki liste var. Liste boşken ilgili bölüm, liste sayfası ve
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
},
```

`sonuc` alanı boş bırakılabilir; ölçülmüş rakam yoksa bölüm hiç basılmaz.
Uydurma rakam yazma.

## Üretilen dosyalar

`index.html` · `ozel-yazilim/` · `404.html` · `assets/stil.css` · `favicon.svg` ·
`sitemap.xml` · `robots.txt` · `llms.txt` · IndexNow anahtar dosyası, ve liste
doluysa `uygulamalar/**` ile `isler/**`.

## Yayınlama

```bash
python uret.py
git add -A
git commit -m "feat: ..."
git push
```
