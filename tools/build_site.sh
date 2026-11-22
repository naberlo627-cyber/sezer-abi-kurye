#!/usr/bin/env bash
# Statik yayın paketini hazırlar: dist/ içine yayın dosyalarını toplar.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
OUT="$ROOT/dist"

rm -rf "$OUT"
mkdir -p "$OUT"

for f in index.html giris.html kurye.html renk.html tasarim.html manifest.json sw.js version.json; do
  [ -f "$ROOT/$f" ] && cp "$ROOT/$f" "$OUT/"
done
[ -d "$ROOT/icons" ] && cp -r "$ROOT/icons" "$OUT/"
[ -d "$ROOT/assets" ] && cp -r "$ROOT/assets" "$OUT/"

# APK de yayına girer: bazı ağlarda GitHub indirme sunucusu engellidir.
# APK depoda tutulmaz (.gitignore); yayın anında release'den çekilir.
APK_KAYNAK="$ROOT/indir/Kurye.apk"
APK_RELEASE="https://github.com/naberlo627-cyber/sezer-abi-kurye/releases/latest/download/Kurye.apk"

apk_gecerli() {
  # HTML hata sayfasını APK sanmamak için zip imzası ara.
  [ -f "$1" ] || return 1
  [ "$(head -c 2 "$1")" = "PK" ] || return 1
  return 0
}

if ! apk_gecerli "$APK_KAYNAK"; then
  echo "APK yerelde yok; release'den indiriliyor…"
  mkdir -p "$ROOT/indir"
  curl -sSL --max-time 120 -o "$APK_KAYNAK.tmp" "$APK_RELEASE" || true
  if apk_gecerli "$APK_KAYNAK.tmp"; then
    mv "$APK_KAYNAK.tmp" "$APK_KAYNAK"
  else
    rm -f "$APK_KAYNAK.tmp"
    echo "UYARI: APK indirilemedi; site APK'sız yayınlanacak." >&2
  fi
fi

if apk_gecerli "$APK_KAYNAK"; then
  cp "$APK_KAYNAK" "$OUT/Kurye.apk"
  # apkWeb yalnız dosya gerçekten yayındayken yazılır; aksi hâlde
  # kullanıcı bozuk bağlantıya gider.
  python3 - "$OUT/version.json" <<'PYEOF'
import json, sys
yol = sys.argv[1]
d = json.load(open(yol, encoding='utf-8'))
d['apkWeb'] = 'Kurye.apk'
json.dump(d, open(yol, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
PYEOF
  echo "APK yayına eklendi: $(stat -c%s "$OUT/Kurye.apk") bayt"
else
  echo "APK yayına eklenmedi; version.json GitHub adresini kullanır."
fi

# GitHub Pages / Cloudflare Pages için kök dizin: index.html zaten var.
echo "Yayın paketi hazır: $OUT ($(find "$OUT" -type f | wc -l) dosya)"
