#!/usr/bin/env bash
# Sezar Abi Kurye APK derleme betiği.
# Web varlıklarını Android assets'e kopyalar, imzalı sürüm APK'sını üretir.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
ANDROID_DIR="$ROOT/android"
ASSETS="$ANDROID_DIR/app/src/main/assets/www"
export ANDROID_HOME="${ANDROID_HOME:-/home/openhands/android-sdk}"
export ANDROID_SDK_ROOT="$ANDROID_HOME"
GRADLE="${GRADLE:-/home/openhands/gradle-8.7/bin/gradle}"

# Sürüm tek kaynaktan: index.html içindeki SURUM.
VER="$(sed -n "s/.*var SURUM='\([0-9.]*\)'.*/\1/p" "$ROOT/index.html" | head -1)"
[ -z "$VER" ] && VER="1.0"
IFS='.' read -r V_MAJOR V_MINOR V_PATCH <<< "$VER"
V_MAJOR="${V_MAJOR:-0}"; V_MINOR="${V_MINOR:-0}"; V_PATCH="${V_PATCH:-0}"
VCODE=$(( V_MAJOR * 10000 + V_MINOR * 100 + V_PATCH ))
echo "Sürüm: $VER (versionCode $VCODE)"

mkdir -p "$ASSETS/icons"
cp "$ROOT/index.html" "$ROOT/manifest.json" "$ROOT/sw.js" "$ASSETS/"
cp "$ROOT"/icons/*.png "$ASSETS/icons/"

# Notlar version.json'da elle yazılır; betik onları korur.
# apkVersion, derlenen APK'nın sürümüdür: web sürümü ileri olabilir ama
# kullanıcıya önerilen güncelleme daima gerçekten indirilebilen APK'dır.
NOTES="$(python3 -c "
import json,sys
try:
    print(json.load(open('$ROOT/version.json',encoding='utf-8')).get('notes',''))
except Exception:
    print('')
" 2>/dev/null)"
[ -z "$NOTES" ] && NOTES="Sezar Abi Kurye güncellemesi."
python3 - "$ROOT/version.json" "$VER" "$VCODE" "$NOTES" <<'PYEOF'
import json, sys
yol, ver, vcode, notlar = sys.argv[1], sys.argv[2], int(sys.argv[3]), sys.argv[4]
json.dump({
    "version": ver,
    "versionCode": vcode,
    "notes": notlar,
    "apk": "https://github.com/naberlo627-cyber/sezer-abi-kurye/releases/latest/download/Kurye.apk",
    "apkVersion": ver
}, open(yol,'w',encoding='utf-8'), ensure_ascii=False, indent=2)
PYEOF
cp "$ROOT/version.json" "$ASSETS/"

sed -i "s/versionCode [0-9]*/versionCode $VCODE/" "$ANDROID_DIR/app/build.gradle"
sed -i "s/versionName \"[^\"]*\"/versionName \"$VER\"/" "$ANDROID_DIR/app/build.gradle"

cd "$ANDROID_DIR"
"$GRADLE" --no-daemon "${1:-assembleRelease}"

OUT="$ANDROID_DIR/app/build/outputs/apk"
mkdir -p "$ROOT/indir"
cp "$OUT/release/app-release.apk" "$ROOT/indir/Kurye.apk"
echo "APK hazır: $ROOT/indir/Kurye.apk ($(stat -c%s "$ROOT/indir/Kurye.apk") bayt)"
