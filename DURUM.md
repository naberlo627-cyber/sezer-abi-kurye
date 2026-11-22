# Sezar Abi Kurye — Durum Defteri

Bu dosya "nerede kaldık" sorusunun tek cevabıdır. Yeni oturumda **önce bunu oku**.

Son güncelleme: 2026-11-14 · **v1.4 yayında**

## Nerede kaldık

v1.4 yayında. Tasarım sıfırdan kuruldu: **saf siyah–beyaz**, sahte harita
yerine rota şeridi, sadeleşmiş görev kartı, tek yüzeyde gruplanmış listeler.
Kontrast WCAG AA üstü (ölçüldü).

Kullanıcı geri bildirimi v1.3'te şuydu: "Yeşil rengi kullanma. Gereksiz aktif
yazılarını kapat. Tasarım dili rezalet. Siyah ve beyaz renklerden oluşsun."
Üçü de karşılandı. Sıradaki iş: **Surge yayını** (token bekliyor).

## Adresler

| Ne | Adres | Durum |
|---|---|---|
| GitHub | https://github.com/naberlo627-cyber/sezer-abi-kurye | public, master |
| GitHub Pages | https://naberlo627-cyber.github.io/sezer-abi-kurye/ | ✓ çalışıyor |
| Cloudflare Pages | https://sezer-abi-kurye.pages.dev/ | ✓ çalışıyor |
| Surge | https://sezerabikurye.surge.sh/ | ✓ çalışıyor (birincil) |
| APK (son sürüm) | https://github.com/naberlo627-cyber/sezer-abi-kurye/releases/latest/download/Kurye.apk | ✓ v1.1 · 2.853.475 bayt |

## Sürümler

- Uygulama sürümü: **1.4** (`index.html` içinde `var SURUM='1.4'`)
- versionCode: **10400**
- Paket adı: `com.sezerabi.kurye`
- APK boyutu: 2.853.475 bayt (2,8 MB)
- Service worker önbelleği: `sezar-v1.4`
- Release: **v1.1** (id 452323570) · v1.0 (id 452315067)

## v1.1 — gerçek işlevler (bu turda eklendi)

Her düğme artık gerçek bir iş yapıyor; uygulamada tek bir "(demo)" kalmadı.

| Düğme | Ne yapıyor |
|---|---|
| Navigasyonu Başlat | Google Maps yol tarifi; aşamaya göre alış veya varış noktası |
| Google Maps | Haritada konum göster (`maps/search`) |
| Müşteriyi ara | `tel:` ile gerçek arama ekranı |
| WhatsApp | `wa.me` ile hazır mesaj |
| İşletmeyi ara | `tel:` işletme numarası |
| Paylaş | Native paylaşım sayfası, yoksa panoya kopyalar |
| Adres kopyala | Panoya kopyalar (eski tarayıcı yedeği var) |
| Hatırlat | Bildirim izni ister, izin varsa bildirim gönderir |
| Ana ekrana ekle | `beforeinstallprompt` ile gerçek kurulum |
| Sürümü denetle | `version.json` ile karşılaştırır, güncelleme katmanı açar |
| Güncelle | APK'yı indirir; APK içinde native kurulum ekranı açılır |
| Mesajlar | Balonlu sohbet ekranı, gönderilen mesaj kalıcı |
| Kişisel bilgiler / Belgeler / Ödeme | Gerçek içerikli alt katmanlar |
| Çıkış yap | Onay katmanı, sonra çevrimdışı duruma geçer |

Ayrıca: aşağı çekip yenileme, çevrimdışı şeridi, donanım geri tuşu (katmanı
kapatır), titreşim geri bildirimi, günde bir sessiz sürüm denetimi.

## Kapanan işler

- ~~Tasarımdan birebir UI: yeşil `#309048`~~ → **v1.4'te kaldırıldı** (kullanıcı istemedi)
- Görevler: rota şeridi (Alış → Teslim), Paketi Aldım → Teslim Ettim → Tamamlandı
- Bekleyen siparişler: 6 kayıt, karta dokun → alt panel → Görevi Al
- Aktif/Kapalı rozeti, durum şeridi canlı sayı
- Kazanç: günlük/hafta/ay, 7 günlük çubuk grafik, son işlemler
- Mesajlar: okunmamış işareti, dokununca okundu
- Profil: puan 4,9, 1284 teslimat, belgeler onaylı
- Yardım: 5 SSS açılır-kapanır + destek/telefon
- localStorage kalıcılığı (`sezar.v1`)
- Çevrimdışı çalışma (sw.js) — test edildi
- 4 kısayol: görevler, kazanç, mesajlar, yardım (`?git=<sekme>`)
- Android APK: WebViewAssetLoader, konum izni, kamera, dosya seçici
- Launcher ikonları (adaptive, 5 yoğunluk), 4 kısayol çizimi
- CI: GitHub Pages + Cloudflare Pages (Surge sır gelirse)
- Sırlar: `CLOUDFLARE_API_TOKEN`, `CLOUDFLARE_ACCOUNT_ID` depoya yazıldı

## Açık işler

1. **C maddesi** — Kazanç/Mesajlar/Profil/Yardım sekmelerinin tasarımı
   kullanıcıdan bekleniyor. Şu anki hâli benim tasarımım.
2. **Surge otomatik yayın** — site yayında ama kurye deposunda `SURGE_TOKEN`
   sırrı yok. Şu an elle/tek seferlik yayınlandı. Kalıcı çözüm için Genç
   deposundaki token'ı kurye deposuna ekle (GitHub sırları okunamaz, yeniden
   girilmeli): `npx surge login` → `npx surge token` → kurye deposuna
   `SURGE_TOKEN` olarak ekle. Sonrasında her push otomatik yayınlanır.
3. **Sunucu yok** — siparişler/mesajlar cihazda (localStorage). Gerçek kurye
   dağıtımı için API gerekir. Kod buna hazır: `gonder()` ve `gorevAl()` tek yer.

## Doğrulama komutları

```bash
# canlı siteler
curl -s -o /dev/null -w "%{http_code}\n" https://sezer-abi-kurye.pages.dev/
curl -s -o /dev/null -w "%{http_code}\n" https://naberlo627-cyber.github.io/sezer-abi-kurye/

# APK
curl -sL -o /tmp/k.apk https://github.com/naberlo627-cyber/sezer-abi-kurye/releases/latest/download/Kurye.apk
/home/openhands/android-sdk/build-tools/34.0.0/aapt2 dump badging /tmp/k.apk | head -1

# yerel derleme
bash tools/build-apk.sh

# yerel sunum
python3 -m http.server 12000 --bind 0.0.0.0
```

## Ortam notları

- Araç zinciri: `/home/openhands/android-sdk`, `/home/openhands/gradle-8.7`, JDK 21
- Keystore: `android/app/kurye-release.jks` — **depoda yok** (.gitignore).
  Parola `kurye12345`, alias `kurye`. Kaybedilirse güncelleme yayınlanamaz.
- Git kimlik bilgisi: `credential.helper=store --file=/workspace/.git-credentials-kurye`
  (remote URL'de token YOK — Genç'teki hata tekrarlanmadı)
- Test yöntemi: uygulama IIFE içinde; `page.evaluate` iç fonksiyonları göremez,
  gerçek UI (tıklama/seçici) üzerinden test et.

## 2026-11-21 — harita gerçek veriye bağlandı (kurye.html)

- Karo: OpenStreetMap (gri filtre). Yol tarifi OSRM, adres çözümleme Nominatim.
- Siparişler artık üretiliyor: 6 dükkân + 7 müşteri adresi (`YERLER`), her teklif
  gerçek koordinat, gerçek km/dk ve km bazlı ücret alıyor.
- Ücret 18 ₺ + 11 ₺/km; teslim süresi yol süresi + 8 dk. Kod, sipariş kimliği,
  telefonlar da sipariş başına üretiliyor.
- Konum: gerçek GPS; İzmir dışı fix yok sayılır, demo konuma düşer.
- Ekran metinleri (`#d1Addr`, `#d2Addr`, `#tFromAddr`, `#tToAddr`, `#gId`, `#sonLine`)
  siparişe göre yazılıyor.
