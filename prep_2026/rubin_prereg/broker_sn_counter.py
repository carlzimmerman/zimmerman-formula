#!/usr/bin/env python3
"""
BROKER SN-Ia READINESS TRACKER (committed 2026-07-21) -- NOT a cosmology measurement.
Purpose: poll a PUBLIC alert broker to count how many Type-Ia SN candidates have been
classified from the (public, real-time) LSST/ZTF alert stream, and compare that running
count to the forecast sample-size thresholds -- i.e. track WHEN the pre-registered a0(z)
gate (a0z_gate_estimator.py) will have enough weight to spring. It does cosmology with
NONE of them: no light-curve fits, no redshifts, no w(z). A count, nothing more.

FORECAST THRESHOLDS (from forecast_rubin_a0z.py / LSST-DESC):
  ~4,400  spectroscopically-confirmed-quality SNe Ia  -> FoM~150-class (interim tracker)
  ~400,000 photometric light-curve SNe Ia (z<1)       -> LSST baseline (full-power target)
  the DESC CALIBRATED cosmology sample (systematics-controlled) is the PRIMARY input and
  is separate from any raw broker count (arrives ~2027+); this tracker is INTERIM ONLY.
"""
import json, sys, urllib.request, urllib.error

def alerce_snia_count():
    # ALeRCE ZTF/LSST object API: count objects whose ML classifier calls them SNIa.
    url="https://api.alerce.online/ztf/v1/objects?classifier=lc_classifier&class=SNIa&page_size=1&count=true"
    req=urllib.request.Request(url, headers={"User-Agent":"Mozilla/5.0","Accept":"application/json"})
    with urllib.request.urlopen(req, timeout=30) as r:
        d=json.loads(r.read().decode())
    return d.get("total") or d.get("count") or (d.get("meta",{}) or {}).get("total")

print("BROKER SN-Ia READINESS TRACKER (interim; NOT cosmology)")
print("="*66)
n=None
try:
    n=alerce_snia_count()
    print(f"  ALeRCE lc_classifier SNIa objects: {n:,}" if isinstance(n,int) else f"  ALeRCE returned: {n}")
except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError, Exception) as e:
    print(f"  (live broker query unavailable here: {type(e).__name__}: {str(e)[:80]})")
    print("  -> script is READY-TO-RUN; endpoint api.alerce.online/ztf/v1/objects (SNIa, count=true).")
    print("     Fallback brokers: Fink (fink-portal.org/api), Lasair, ANTARES, Pitt-Google.")

TH_SPEC, TH_PHOT = 4400, 400000
print("\n  Readiness vs forecast thresholds:")
if isinstance(n,int):
    print(f"    spectroscopic-quality (~{TH_SPEC:,}): {'REACHED' if n>=TH_SPEC else f'{100*n/TH_SPEC:.1f}% ({n:,}/{TH_SPEC:,})'}")
    print(f"    LSST photometric target (~{TH_PHOT:,}): {'REACHED' if n>=TH_PHOT else f'{100*n/TH_PHOT:.2f}% ({n:,}/{TH_PHOT:,})'}")
    print("    (NOTE: this is a broker-classifier count -- includes ZTF legacy + early LSST, unvetted,")
    print("     no redshifts. It is a READINESS gauge, not the DESC cosmology sample.)")
else:
    print(f"    thresholds: {TH_SPEC:,} (spec-quality) / {TH_PHOT:,} (LSST photometric). Run when a broker responds.")
print("\n  HARD RULE (frozen): this count NEVER feeds the gate verdict. The gate takes ONLY a")
print("  calibrated (w0,wa) posterior (DESC primary; published Rubin w0wa interim). Counts track")
print("  timing, not cosmology. Doing otherwise = manufacturing a result. Do not.")
print("EXIT 0")
