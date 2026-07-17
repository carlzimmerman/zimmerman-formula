#!/bin/bash
# download_maps.sh -- fetch the frozen-rule MAPS subsample (maps_subsample.csv), 4-way
# parallel, resumable (curl -C -). Files land in data/maps/. exit 0 only if all present.
set -u
HERE="$(cd "$(dirname "$0")" && pwd)"
OUT="$HERE/data/maps"
mkdir -p "$OUT"

fetch() {
  u="$1"; f="$OUT/$(basename "$u")"
  curl -sS -C - --retry 3 -o "$f" "$u" && echo "OK  $(basename "$u")" || echo "FAIL $(basename "$u")"
}

n=0
while IFS= read -r u; do
  fetch "$u" &
  n=$((n + 1))
  [ $((n % 4)) -eq 0 ] && wait
done < <(tail -n +2 "$HERE/maps_subsample.csv" | cut -d, -f7)
wait

n_want=$(($(wc -l < "$HERE/maps_subsample.csv") - 1))
n_have=$(ls "$OUT"/*.fits.gz 2>/dev/null | wc -l | tr -d ' ')
echo "have $n_have / $n_want MAPS files"
[ "$n_have" -eq "$n_want" ] && exit 0 || exit 1
