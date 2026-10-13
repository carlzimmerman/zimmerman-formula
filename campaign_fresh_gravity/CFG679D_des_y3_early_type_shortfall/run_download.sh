#!/bin/sh
# CFG679D: keep the metacal download going through DES server timeouts (resumable; finished pieces are skipped).
cd "$(dirname "$0")"
for i in $(seq 1 500); do
  nice -n 10 python3 cfg679_download.py mcal --threads 2 --max-gb 30 --light-guard >> download_mcal.out 2>&1
  grep -q "mcal: COMPLETE" ../_external_data/cfg679_des/download_mcal.log 2>/dev/null && break
  sleep 120
done
echo "RUN_DOWNLOAD_EXIT attempts=$i" >> download_mcal.out
