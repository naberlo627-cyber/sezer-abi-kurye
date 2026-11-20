#!/usr/bin/env bash
# Statik yayın paketini hazırlar: dist/ içine yayın dosyalarını toplar.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
OUT="$ROOT/dist"

rm -rf "$OUT"
mkdir -p "$OUT"

for f in index.html manifest.json sw.js version.json; do
  [ -f "$ROOT/$f" ] && cp "$ROOT/$f" "$OUT/"
done
[ -d "$ROOT/icons" ] && cp -r "$ROOT/icons" "$OUT/"

# APK de yayına girer: bazı ağlarda GitHub indirme sunucusu engellidir.
if [ -f "$ROOT/indir/Kurye.apk" ]; then
  cp "$ROOT/indir/Kurye.apk" "$OUT/"
fi

# GitHub Pages / Cloudflare Pages için kök dizin: index.html zaten var.
echo "Yayın paketi hazır: $OUT ($(find "$OUT" -type f | wc -l) dosya)"
