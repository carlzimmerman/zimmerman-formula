#!/bin/bash
# CFG316 data stage: fetch three files (owner go 2026-10-03, "yeah do both").
# Run from the directory that contains _external_data (e.g. ~/new_physics).
# Hard caps: stop if free disk on /System/Volumes/Data would fall below 60 GB,
# or if the server's Content-Length exceeds the CFG314 size by more than 20%.
set -u
ROOT="${1:-.}"
cd "$ROOT" || exit 1
fetch () { # url dest cfg314_bytes
  url=$1; dest=$2; ref=$3
  len=$(curl -sSIL --max-time 60 "$url" | awk 'tolower($1)=="content-length:"{v=$2} END{gsub("\r","",v); print v}')
  have=0; [ -f "$dest" ] && have=$(stat -f %z "$dest")
  need=$(( len - have ))
  freek=$(df -k /System/Volumes/Data | awk 'NR==2{print $4}')
  echo "[$(date -u +%FT%TZ)] $url len=$len have=$have need=$need free_kB=$freek"
  if [ $(( len * 10 )) -gt $(( ref * 12 )) ]; then echo "STOP: size cap exceeded"; return 2; fi
  if [ $(( freek*1024 - need )) -lt $(( 60*1024*1024*1024 )) ]; then echo "STOP: disk floor"; return 3; fi
  curl -sS -L --retry 20 --retry-delay 10 --retry-all-errors -C - -o "$dest" "$url"
  rc=$?
  echo "[$(date -u +%FT%TZ)] done rc=$rc size=$(stat -f %z "$dest")"
}
fetch https://kids.strw.leidenuniv.nl/DR4/data_files/KiDS_DR4.1_ugriZYJHKs_SOM_gold_WL_cat.fits \
      _external_data/kids_lensing_zsplit/KiDS_DR4.1_ugriZYJHKs_SOM_gold_WL_cat.fits 17711426880 &
fetch https://data.desi.lbl.gov/public/dr1/survey/catalogs/dr1/LSS/iron/LSScats/v1.5/BGS_BRIGHT_full_HPmapcut.dat.fits \
      _external_data/desi_dr1_bgs/BGS_BRIGHT_full_HPmapcut.dat.fits 5186908800 &
wait
fetch https://data.desi.lbl.gov/public/dr1/vac/dr1/cigale/iron/v1.2/IronPhysProp_v1.2.fits \
      _external_data/desi_dr1_cigale/IronPhysProp_v1.2.fits 7322716800
