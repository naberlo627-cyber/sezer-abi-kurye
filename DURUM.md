# Sezar Abi Kurye — Durum Defteri

Bu dosya "nerede kaldık" sorusunun tek cevabıdır. Yeni oturumda **önce bunu oku**.

Son güncelleme: 2026-11-20

## Nerede kaldık

v1.0 yayında. Tasarım (kullanıcının gönderdiği tek ekran) birebir aktarıldı.
Kullanıcı **A + C** seçti: (A) yayına al + APK, (C) diğer 4 sekmenin tasarımını
gönderince uyarla. **A tamamlandı. C bekliyor.**

## Adresler

| Ne | Adres | Durum |
|---|---|---|
| GitHub | https://github.com/naberlo627-cyber/sezer-abi-kurye | public, master |
| GitHub Pages | https://naberlo627-cyber.github.io/sezer-abi-kurye/ | ✓ çalışıyor |
| Cloudflare Pages | https://sezer-abi-kurye.pages.dev/ | ✓ çalışıyor |
| Surge | https://sezer-abi-kurye.surge.sh/ | ✗ 404 — sır yok |
| APK (son sürüm) | https://github.com/naberlo627-cyber/sezer-abi-kurye/releases/latest/download/Kurye.apk | ✓ 2.846.341 bayt |

## Sürümler

- Uygulama sürümü: **1.0** (`index.html` içinde `var SURUM='1.0'`)
- versionCode: **10000**
- Paket adı: `com.sezerabi.kurye`
- APK boyutu: 2.846.341 bayt (2,8 MB)
- Service worker önbelleği: `sezar-v1`
- Release: **v1.0** (release id 452315067)

## Kapanan işler

- Tasarımdan birebir UI: zemin `#F1F7F7`, kart beyaz, buton `#141F31`, yeşil `#309048`
- Görevler: haritalı kart (SVG rota), Paketi Aldım → Teslim Ettim → Tamamlandı
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

1. **Surge 404** — `sezer-abi-kurye.surge.sh` yayınlanmadı. Surge sırları
   Genç deposunda var ama GitHub sır değerleri okunamaz. Çözüm: kullanıcıdan
   Surge token/login al (form ile) ya da Surge'u tamamen bırak (iki adres yeter).
2. **C maddesi** — Kazanç/Mesajlar/Profil/Yardım sekmelerinin tasarımı
   kullanıcıdan bekleniyor. Şu anki hâli benim tasarımım.
3. Gerçek veri kaynağı belirsiz (şimdilik demo veri, localStorage).

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
