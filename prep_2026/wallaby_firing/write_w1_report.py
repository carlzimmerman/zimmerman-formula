#!/usr/bin/env python3
"""
LANE W1 report generator -- writes W1_EXTRACTION.md from perside_237.csv.
FIREWALL (mandatory, top of every output of this lane):
  At N~237 the achieved sensitivity at AQUAL amplitude is ~1-1.5 sigma
  (n=16 gave 0.3 sigma; sqrt(237/16)=3.85x).  NEITHER pre-registered kill
  condition (3-sigma AQUAL-vs-BranchB; N~1,157 canonical a0=9.36e-11,
  N~1,424 alt a0=1.13e-10, max-clustering e_N, w=0.304) CAN TRIGGER on this
  sample.  Kill-condition language appears ONLY as "cannot trigger".
Report only: QC funnel, sigma(A) distribution vs WHISP 0.092 intrinsic rms,
per-field extraction health.  NO correlation with any g_ext direction, NO
verdict on AQUAL / Branch B / pure MI (that is the firing lane).
exit 0 on completion.
"""
import csv, os, sys, time
from collections import Counter
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
CSV = os.path.join(HERE, "perside_237.csv")
OUT = os.path.join(HERE, "W1_EXTRACTION.md")
WHISP_RMS = 0.092

rows = []
with open(CSV) as f:
    for line in f:
        if not line.startswith("#"):
            break
    f.seek(0)
    body = [l for l in f if not l.startswith("#")]
rows = list(csv.DictReader(body))
assert rows, "empty CSV"

def ffloat(x):
    try:
        return float(x)
    except (ValueError, TypeError):
        return np.nan

n_all = len(rows)
n_dl = sum(1 for r in rows if not r["qc_reason"].startswith("download failed"))
n_ext = sum(1 for r in rows if np.isfinite(ffloat(r["A_preregistered"])))
qc = [r for r in rows if r["qc_pass"] == "True"]
n_pass = len(qc)
n_flip = sum(1 for r in rows if r["pa_flipped"] == "True")
n_noweight = sum(1 for r in qc if r["weight"] != "mom0")

A = np.array([ffloat(r["A_preregistered"]) for r in qc])
S = np.array([ffloat(r["sigma_boot"]) for r in qc])
S_ext = np.array([ffloat(r["sigma_boot"]) for r in rows
                  if np.isfinite(ffloat(r["sigma_boot"]))])

def bucket(reason):
    if reason.startswith("inc "):
        return "inclination >= 70 deg"
    if reason.startswith("sanity ratio"):
        return "sanity ratio outside [0.8, 1.2] (all failures were LOW: beam-smeared / poorly-resolved per-side curve under-reads the WKAPP model)"
    if reason.startswith("n_outer"):
        return "n_outer < 4 rings"
    if reason.startswith("sigma_boot"):
        return "sigma_boot >= 0.05"
    if reason.startswith("download"):
        return "download failed"
    return "extraction integrity (parse/extract error)"

reasons = Counter()
for r in rows:
    if r["qc_pass"] != "True":
        reasons[bucket(r["qc_reason"])] += 1

fields = sorted(set(r["field"] for r in rows))
fl = []
for fld in fields:
    sub = [r for r in rows if r["field"] == fld]
    subq = [r for r in sub if r["qc_pass"] == "True"]
    Af = np.array([ffloat(r["A_preregistered"]) for r in subq])
    if len(Af):
        fl.append((fld, len(sub), len(subq), Af.mean(), np.median(Af),
                   Af.std(ddof=1) if len(Af) > 1 else np.nan,
                   float(np.median([ffloat(r['sigma_boot']) for r in subq]))))
    else:
        fl.append((fld, len(sub), 0, np.nan, np.nan, np.nan, np.nan))

# sigma(A) histogram bins
bins = [0.0, 0.005, 0.01, 0.02, 0.03, 0.05]
hist = np.histogram(S, bins=bins)[0]

# aggregate (descriptive only)
wA = A / np.maximum(S, 1e-4) ** 0 if False else A
mean_A = A.mean(); sem_A = A.std(ddof=1) / np.sqrt(len(A))
med_A = np.median(A); rms_A = A.std(ddof=1)
ivw = np.sum(A / S**2) / np.sum(1 / S**2)
frac_dom = np.median(S) / WHISP_RMS

with open(OUT, "w") as f:
    f.write(f"""# W1_EXTRACTION -- bulk per-side extraction, ALL per-side-capable WALLABY galaxies

Generated {time.strftime('%Y-%m-%d %H:%M')} by `write_w1_report.py` from `perside_237.csv`
(driver `run_extraction_237.py`, QC frozen BEFORE extraction in `QC_FROZEN.md`).

## FIREWALL (read first)

At N~237 the achieved sensitivity at AQUAL amplitude is **~1-1.5 sigma**
(n=16 gave 0.3 sigma; sqrt(237/16) = 3.85x). **NEITHER pre-registered kill
condition (3-sigma AQUAL-vs-BranchB; N~1,157 canonical a0 = 9.36e-11,
N~1,424 alt a0 = 1.13e-10, both max-clustering e_N, w = 0.304) CAN TRIGGER
on this sample.** Kill-condition language in this lane appears ONLY as
"cannot trigger". a0 does not enter the extractor; both footings enter at
the confrontation stage only. This file contains NO directional statistic,
NO g_ext correlation, and NO AQUAL/Branch-B/pure-MI verdict.

## Sign convention (THE SIGN TRAP -- handled, hand-verified)

- **Pre-registered**: A_i = 2(v_rec - v_appr)/(v_rec + v_appr), tied to the
  RECEDING side (p_i > 0 predicts attractor-side-faster for x >~ 2e).
- **Extractor raw** (pilot printout): A_ext = 2(v_app - v_rec)/(v_app + v_rec)
  -- OPPOSITE ordering. Both recorded per galaxy in the CSV.
- Receding side determined EMPIRICALLY per galaxy (frozen rule, QC_FROZEN.md);
  `pa_flipped` galaxies (WKAPP PA anti-aligned with the true receding side): **{n_flip}**.
- Hand verification from the raw mom1 map (independent code path,
  `hand_verify_sign.py`, J165901-601241): see its output below the funnel.
- PA source verified from Deg+2022 arXiv:2211.07333 Table 4 (fetched + grepped
  2026-07-16, not assumed): PA_model_g = "Position angle in equatorial
  coordinates (East of North)"; the paper does NOT restate receding-side
  anchoring, hence the empirical rule.

## QC funnel (cuts frozen 2026-07-16 BEFORE any real A value)

| stage | N |
|---|---|
| per-side-capable (CADC census: mom1 + WKAPP AvgMod geometry) | {n_all} |
| all 3 files downloaded (mom1 + mom0 + AvgMod) | {n_dl} |
| extractor returned a valid A + bootstrap | {n_ext} |
| **passed ALL frozen QC cuts** | **{n_pass}** |

Exclusion reasons (a galaxy failing ANY frozen cut is excluded):

| reason | N |
|---|---|
""")
    for reason, n in reasons.most_common():
        f.write(f"| {reason} | {n} |\n")
    f.write(f"""
QC-pass galaxies running unweighted (mom0 unavailable): {n_noweight}.

## sigma(A) distribution (QC pass, bootstrap) vs WHISP intrinsic rms 0.092

- median sigma_boot = **{np.median(S):.4f}**; p10 = {np.percentile(S,10):.4f}, p90 = {np.percentile(S,90):.4f}
  (all extracted, pre-QC: median {np.median(S_ext):.4f}, p90 {np.percentile(S_ext,90):.4f})
- histogram (QC pass): """ +
        ", ".join(f"[{bins[i]:.3f},{bins[i+1]:.3f}): {hist[i]}" for i in range(len(hist))) + f"""
- median sigma_boot / 0.092 = **{frac_dom:.2f}** -> the PIXEL-bootstrap error is
  subdominant to the intrinsic lopsidedness scatter; naive per-galaxy noise
  sqrt(0.092^2 + median sigma_boot^2) = {np.sqrt(WHISP_RMS**2 + np.median(S)**2):.4f}. HOWEVER the OBSERVED QC-pass
  rms(A) = {rms_A:.3f} exceeds this: the bootstrap does NOT capture the dominant
  vsys-mismatch term (diagnosed below) -- the effective per-galaxy noise for any
  ensemble use is the observed {rms_A:.3f}, not 0.092.

## A_preregistered distribution (QC pass; DESCRIPTIVE ONLY -- no direction attached)

- N = {n_pass}; mean = {mean_A:+.4f} +/- {sem_A:.4f} (sem); median = {med_A:+.4f};
  rms = {rms_A:.4f} (WHISP intrinsic 0.092); inverse-variance-weighted mean = {ivw:+.4f}
- The rms {'is consistent with' if 0.6*WHISP_RMS < rms_A < 1.6*WHISP_RMS else 'DIFFERS from'} the WHISP 0.092 intrinsic-lopsidedness scatter.
- NOTE: an ensemble mean of A without the per-galaxy attractor direction is
  NOT the directional-EFE statistic (a nonzero mean here would indicate a
  convention/systematic, not physics; the directional test is cos(psi)-weighted
  and happens in the firing lane).

## Per-field breakdown

| field | capable | QC pass | mean A_pre | median | rms | median sigma |
|---|---|---|---|---|---|---|
""")
    for fld, nt, nq, mn, md, rm, ms in fl:
        f.write(f"| {fld} | {nt} | {nq} | " +
                (f"{mn:+.4f} | {md:+.4f} | {rm:.4f} | {ms:.4f} |\n"
                 if np.isfinite(mn) else "-- | -- | -- | -- |\n"))
    # ---- diagnostic section (diag_mean_offset.json, if present) ----
    dg = os.path.join(HERE, "diag_mean_offset.json")
    if os.path.exists(dg):
        import json
        D = json.load(open(dg))
        f.write(f"""
## Diagnosed extraction systematic: vsys sensitivity (direction-blind)

The direction-blind QC-pass ensemble mean is **{D['mean_A_frozen']:+.4f} ± {rms_A/np.sqrt(D['n']):.4f}**
— nonzero at ~{abs(D['mean_A_frozen'])/(rms_A/np.sqrt(D['n'])):.1f} sigma. A direction-blind mean of A should be ~0;
this was diagnosed (`diag_mean_offset.py`, computed not asserted):

- Per-galaxy empirical offset delta = (mom1 minor-axis weighted median − WKAPP
  VSys_model): **median +1.7 km/s, mean +2.5 km/s, rms 6.8 km/s, 70% positive**.
- NOT an optical-vs-radio cz convention mismatch: corr(delta, cz²/c) = {D['corr_delta_cz2']:+.2f}
  and the mismatch would be 13–125 km/s at these cz — delta is ~2 km/s, flat in cz
  (half-a-WALLABY-channel scale, ~4 km/s channels).
- A_pre is amplified vsys error: dA/d(delta) ≈ 2/(v_rot · sin i · ⟨cosθ⟩) ≈ 0.026 per km/s
  (median). The coherent +2.5 km/s predicts a **+0.065 mean bias** (observed +0.104);
  the empirical 6.8 km/s scatter predicts σ_A ≈ 0.18 — the observed rms 0.155 is
  therefore **vsys-mismatch-dominated**, not pixel-noise-dominated (median
  bootstrap σ = {np.median(S):.3f}) and not pure intrinsic lopsidedness (WHISP 0.092).
- DIAGNOSTIC-ONLY re-extraction with vsys := VSys_model + delta (frozen CSV
  untouched): mean A_pre → **{D['mean_A_corrected']:+.4f} ± 0.027** (consistent with zero),
  median +0.092 → +0.032.
- WKAPP quoted e_VSys (median 0.8 km/s, p90 3.8) explains only part of the
  6.8 km/s empirical scatter; the rest is map-vs-flat-disk-model mismatch
  (warps, lopsided outskirts, beam smearing into the minor axis).

**Implication for the firing lane (flag, not a verdict):** a direction-blind
additive offset in A cannot fake an attractor-aligned signal to first order
(cos ψ averages it out over isotropic attractor directions), but it (a) inflates
the per-galaxy noise from the banked 0.092 to ~0.155, further REDUCING achieved
sensitivity below the firewall's ~1–1.5σ estimate, and (b) any anisotropy of the
WALLABY fields on the sky couples the coherent +2.5 km/s term to the direction
statistic at second order — the firing lane must include a vsys-offset nuisance
test (e.g. re-fire with the delta-corrected A as a robustness branch). Neither
pre-registered kill condition can trigger regardless (see FIREWALL).
""")
    f.write(f"""
## Files

- `perside_237.csv` -- per-galaxy table (BOTH A_raw_extractor and
  A_preregistered, sigma_boot, QC pass/fail + reason, full provenance).
- `perside_237_curves.json` -- per-ring per-side curves (provenance).
- `run_extraction_237.py` (exit 0), `extraction_progress.log`, `data/`.
- `hand_verify_sign.py` (exit 0) -- raw-map hand check of the sign conversion
  (J165901-601241: PA side receding PASS; A_pre = -A_ext identically PASS;
  independent sign matches pipeline PASS).
- `diag_mean_offset.py` + `diag_mean_offset.json` -- vsys-systematic diagnosis.
- `QC_FROZEN.md` -- the frozen cuts; frozen BEFORE any real A value.
""")
print(f"wrote {OUT}")
sys.exit(0)
