#!/usr/bin/env bash
# Kurye sitesini sezerabikurye.surge.sh adresine yükler.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
DOMAIN="${SURGE_DOMAIN:-sezerabikurye.surge.sh}"

# Surge yalnız token ile kimlik doğrular (--token). SURGE_LOGIN gerekmez.
[ -n "${SURGE_TOKEN:-}" ] || { echo "SURGE_TOKEN tanımlı değil." >&2; exit 1; }

bash "$ROOT/tools/build_site.sh"

# Yayın paketi eksikse boş site yayınlamak yerine dur.
for f in index.html version.json; do
  [ -f "$ROOT/dist/$f" ] || { echo "Yayın paketinde $f yok; yükleme durduruldu." >&2; exit 1; }
done

cd "$ROOT/dist"
printf '%s\n' "$DOMAIN" > CNAME

npx --yes surge . "$DOMAIN" --token "$SURGE_TOKEN"

echo "Yayınlandı: https://$DOMAIN"
