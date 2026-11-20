# Sezar Abi Kurye — Ajan Notları

**Önce `DURUM.md` oku.** Nerede kaldığımız, adresler ve açık işler orada.

## Proje

Türkçe kurye uygulaması: tek dosya PWA (`index.html`) + Android APK.
Sahibi: Sezer abi. Kardeş proje: Genç (`/workspace/project`, ayrı depo).

## Yapı

- `index.html` — tüm uygulama (HTML+CSS+JS), ~38 KB, sürüm `var SURUM='1.0'`
- `manifest.json` — 4 kısayol, standalone, tema `#F1F7F7`
- `sw.js` — çevrimdışı; sayfa ağ öncelikli, varlık önbellek öncelikli
- `icons/` — PWA simgeleri (192/512/maskable/apple + 4 kısayol)
- `android/` — Gradle projesi, `com.sezerabi.kurye`
- `tools/build-apk.sh` — sürüm tek kaynaktan (`SURUM`), imzalı APK
- `tools/build_site.sh` — `dist/` yayın paketi
- `tools/web_ikon.py`, `tools/android_ikon.py` — ikon üreticileri

## Kurallar

- **Sürüm tek kaynak:** sadece `index.html` içindeki `SURUM`. Başka yerde tekrarlama.
  `build-apk.sh` bundan `versionCode` üretir ve `version.json`'ı günceller;
  `version.json`'daki `notes` alanı elle yazılır, betik onu korur.
- **Service worker önbellek adı** `sw.js` içindeki `CACHE`; her sürümde artır.
  Aksi hâlde eski dosyalar önbellekten servis edilir.
- **`version.json` ağ öncelikli olmalı** (sw.js). Önbellekten verilirse
  güncelleme denetimi eski sürümü görür ve güncelleme hiç görünmez.
- **Keystore depoya girmez.** `android/app/*.jks` .gitignore'da.
- **Remote URL'de token olmaz.** `credential.helper` kullan.
- Tasarım sadakati: renkler `#F1F7F7` zemin, `#FFFFFF` kart, `#141F31` buton,
  `#309048` yeşil aksan. Sapma yapma; kullanıcı tasarımı önemser.
- Test: gerçek UI üzerinden (tıklama/seçici). İç fonksiyonlar IIFE'de gizli;
  `S` ve iç fonksiyonlar `page.evaluate` ile erişilemez, `localStorage` kullan.
- **Veri nesnesine alan eklerken** `gorevAl()` gibi kopyalama yerlerini denetle.
  Alan alan kurmak (`{id:o.id, ...}`) yeni alanları düşürür; nesneyi kopyala.
  Eski kayıtlar için `gocEttir()` içine tamamlama ekle.
- **Her düğme gerçek iş yapmalı.** "(demo)" metni kullanıcıya "bu sahte" der;
  yayına çıkmadan önce `grep "(demo)"` sıfır olmalı.

## Test

```bash
python3 -m http.server 12000 --bind 0.0.0.0   # yerel
bash tools/build-apk.sh                        # APK
```
