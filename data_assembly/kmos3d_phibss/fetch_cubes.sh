#!/usr/bin/env bash
# Fetch (or resume) the KMOS3D cube tarballs. Sizes from the server's Content-Length on 2026-09-28:
#   COSMOS 1,154,934,387 B   GOODSS 996,771,994 B   UDS 996,315,607 B   (sum 3,148,021,988 B;
#   the all-fields KMOS3D_cubes.tar.gz is 3,152,906,479 B and is NOT needed).
# Usage: ./fetch_cubes.sh DEST_DIR      (re-run to resume; curl -C - continues a partial file)
set -euo pipefail
DEST="${1:?usage: fetch_cubes.sh DEST_DIR}"
mkdir -p "$DEST"
cd "$DEST"
for f in KMOS3D_cubes_COSMOS.tar.gz KMOS3D_cubes_GOODSS.tar.gz KMOS3D_cubes_UDS.tar.gz; do
  curl -fL -C - -O "https://www.mpe.mpg.de/resources/KMOS3D/$f" &
done
wait
ls -l KMOS3D_cubes_*.tar.gz
echo "then:  python3 build.py --cubes $DEST   (records sha256 and size of each tarball in manifest.json)"
