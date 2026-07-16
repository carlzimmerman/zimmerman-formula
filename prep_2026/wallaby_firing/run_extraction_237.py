#!/usr/bin/env python3
"""
LANE W1 -- BULK PER-SIDE EXTRACTION over ALL 237 per-side-capable WALLABY galaxies
===================================================================================
FIREWALL (mandatory, top of every output of this lane):
  At N~237 the achieved sensitivity at AQUAL amplitude is ~1-1.5 sigma
  (n=16 gave 0.3 sigma; sqrt(237/16)=3.85x).  NEITHER pre-registered kill
  condition (3-sigma AQUAL-vs-BranchB; N~1,157 canonical a0=9.36e-11,
  N~1,424 alt a0=1.13e-10, max-clustering e_N, w=0.304) CAN TRIGGER on this
  sample.  Kill-condition language appears ONLY as "cannot trigger".
  a0 does not enter this extractor; both footings enter at confrontation only.

QC: frozen BEFORE any real A value in this lane -- see QC_FROZEN.md (2026-07-16).
  Cuts: inc < 70 deg; sanity ratio in [0.8,1.2]; n_outer >= 4; sigma_boot < 0.05;
  extraction integrity.  Model choice: highest TR, tie -> High-Res.  Receding
  side determined EMPIRICALLY per galaxy (median deprojected v_rot > 0), never
  assumed; anti-aligned PA -> labels swapped + pa_flipped flag.

SIGN CONVENTION (THE SIGN TRAP, handled explicitly):
  extractor raw:     A_ext  = 2(v_app - v_rec)/(v_app + v_rec)   [pilot printout]
  PRE-REGISTERED:    A_i    = 2(v_rec - v_appr)/(v_rec + v_appr) [receding-side tied]
  Both recorded per galaxy; A_preregistered is formed from the EMPIRICALLY
  determined receding side, so it equals -A_ext when the WKAPP PA points at the
  receding side (the fitter convention) and +A_ext when the PA is anti-aligned.

PA source (verified from Deg+2022 arXiv:2211.07333, Table 4 -- not assumed):
  PA_model_g = "Position angle in equatorial coordinates (East of North)";
  PA_model   = "Position angle in pixel coordinates (counterclockwise from x=0)".
  We use PA_model_g on the WCS sky grid.  Deg+22 does not restate the
  receding-side anchoring (that is the TiRiFiC/FAT + 3DBarolo tilted-ring
  convention), hence the frozen empirical check above.

Machinery: byte-identical extractor to the gate-validated
  wallaby_prep/perside_extractor.py (imported, not copied).  Gate PASS on file:
  injected +2% recovered +0.0187+-0.0024 (6-beam), null 0.0018+-0.0024.

exit 0 on completion.  Outputs: data/ (downloads), perside_237.csv,
perside_237_curves.json, extraction_progress.log.
"""
import os, sys, json, csv, math, re, time, urllib.request, urllib.parse
from concurrent.futures import ThreadPoolExecutor, as_completed
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
PREP = "/Users/carlzimmerman/new_physics/prep_2026/wallaby_prep"
DATA = os.path.join(HERE, "data")
PILOT_DATA = os.path.join(PREP, "pilot_data")
LOG = os.path.join(HERE, "extraction_progress.log")
RAVEN = "https://ws.cadc-ccda.hia-iha.nrc-cnrc.gc.ca/raven/files/cadc:WALLABY/"
TAP = "https://ws.cadc-ccda.hia-iha.nrc-cnrc.gc.ca/argus/sync"
JRE = re.compile(r"(J\d{6}[+-]\d{6})")

sys.path.insert(0, PREP)
import perside_extractor as pe          # gate-validated machinery, imported not copied
from astropy.io import fits
from astropy.wcs import WCS

C_KMS = 299792.458
F0_HI = 1420405751.77


def log(msg):
    line = f"[{time.strftime('%H:%M:%S')}] {msg}"
    print(line, flush=True)
    with open(LOG, "a") as f:
        f.write(line + "\n")


# ----------------------------------------------------------------------------
# 1. Census -> manifest (frozen pairing + model-choice rules, QC_FROZEN.md)
# ----------------------------------------------------------------------------
def load_census():
    """Live CADC TAP first (same query as wallaby_census.py); cache fallback."""
    q = """SELECT Artifact.uri FROM caom2.Artifact AS Artifact
JOIN caom2.Plane AS Plane ON Artifact.planeID=Plane.planeID
JOIN caom2.Observation AS Observation ON Plane.obsID=Observation.obsID
WHERE Observation.collection='WALLABY'
AND (Artifact.uri LIKE '%AvgMod.txt' OR Artifact.uri LIKE '%mom1.fits')"""
    try:
        url = TAP + "?" + urllib.parse.urlencode(
            {"LANG": "ADQL", "FORMAT": "csv", "QUERY": " ".join(q.split())})
        with urllib.request.urlopen(url, timeout=180) as r:
            rows = [l for l in r.read().decode().splitlines()[1:] if l.strip()]
        log(f"census: LIVE CADC TAP, {len(rows)} artifact rows")
    except Exception as e:
        cache = json.load(open(os.path.join(PREP, "census_cache.json")))
        rows = cache["uris"]
        log(f"census: TAP unreachable ({e}); using cache "
            f"(source={cache['source']}, {len(rows)} rows)")
    return [r.split("cadc:WALLABY/")[-1] for r in rows]


def field_of(avgmod_name):
    """Normalized field + resolution tag from the AvgMod filename."""
    mid = JRE.split(avgmod_name)[-1]           # e.g. _NGC_4808_High-Res_Kin_TR1_AvgMod.txt
    mid = mid.replace("_AvgMod.txt", "")
    m = re.match(r"_(.+?)_Kin_TR(\d+)$", mid)
    raw_field, tr = m.group(1), int(m.group(2))
    hires = "High-Res" in raw_field
    fld = raw_field.replace("_High-Res", "").replace("High-Res", "")
    fld = fld.replace("NGC_", "NGC").replace("_", "").strip()
    return fld, hires, tr


def build_manifest(rows):
    avg = sorted(r for r in rows if r.endswith("AvgMod.txt"))
    mom1 = set(r for r in rows if r.endswith("mom1.fits"))

    def to_mom1(a):
        m = a.replace("_Kin", "").replace("_AvgMod.txt", "_mom1.fits")
        if m not in mom1:
            m = m.replace("NGC5044", "NGC_5044")   # frozen naming normalization
        return m if m in mom1 else None

    cand = {}
    unmatched = []
    for a in avg:
        m = to_mom1(a)
        if m is None:
            unmatched.append(a)
            continue
        j = JRE.search(a).group(1)
        fld, hires, tr = field_of(a)
        cand.setdefault(j, []).append(
            dict(jname=j, avgmod=a, mom1=m, mom0=m.replace("mom1", "mom0"),
                 field=fld, hires=hires, tr=tr))
    manifest = []
    for j in sorted(cand):
        # FROZEN choice: highest TR; TR tie -> High-Res preferred
        best = sorted(cand[j], key=lambda d: (d["tr"], d["hires"]))[-1]
        best["n_models_available"] = len(cand[j])
        manifest.append(best)
    log(f"manifest: {len(manifest)} galaxies "
        f"({sum(m['n_models_available'] > 1 for m in manifest)} had >1 model; "
        f"frozen rule: max TR, tie->High-Res); unmatched AvgMod files: {unmatched}")
    return manifest


# ----------------------------------------------------------------------------
# 2. Downloads (<=4-way, retry x3, reuse pilot files)
# ----------------------------------------------------------------------------
def local_path(fn):
    p = os.path.join(PILOT_DATA, fn)
    if os.path.exists(p) and os.path.getsize(p) > 0:
        return p
    return os.path.join(DATA, fn)


def fetch_one(fn):
    p = local_path(fn)
    if os.path.exists(p) and os.path.getsize(p) > 0:
        return fn, "cached", 0
    url = RAVEN + urllib.parse.quote(fn)
    for attempt in range(3):
        try:
            tmp = p + ".part"
            urllib.request.urlretrieve(url, tmp)
            os.replace(tmp, p)
            return fn, "ok", os.path.getsize(p)
        except Exception as e:
            err = str(e)
            time.sleep(2.0 * (attempt + 1))
    return fn, f"FAIL: {err}", 0


def download_all(manifest):
    os.makedirs(DATA, exist_ok=True)
    files = []
    for m in manifest:
        files += [m["avgmod"], m["mom1"], m["mom0"]]
    log(f"download: {len(files)} files queued (mom1+mom0+AvgMod x {len(manifest)})")
    status = {}
    done = 0
    with ThreadPoolExecutor(max_workers=4) as ex:
        futs = {ex.submit(fetch_one, fn): fn for fn in files}
        for fut in as_completed(futs):
            fn, st, size = fut.result()
            status[fn] = st
            done += 1
            if done % 50 == 0 or st.startswith("FAIL"):
                log(f"download: {done}/{len(files)} "
                    f"({'last: ' + fn + ' ' + st if st.startswith('FAIL') else 'ok'})")
    n_fail = sum(1 for s in status.values() if s.startswith("FAIL"))
    log(f"download: complete; {n_fail} failures / {len(files)} files")
    return status


# ----------------------------------------------------------------------------
# 3. Extraction (imported gate-validated machinery) + frozen QC
# ----------------------------------------------------------------------------
def extract_galaxy(m, dl_status):
    """Returns a result dict (always), with qc_pass / qc_reason filled."""
    r = dict(jname=m["jname"], field=m["field"],
             hires=m["hires"], tr=m["tr"], model_file=m["avgmod"],
             n_models_available=m["n_models_available"],
             ra=np.nan, dec=np.nan, cz=np.nan, inc=np.nan, pa_wkapp=np.nan,
             n_outer=0, v_rec=np.nan, v_appr=np.nan,
             A_raw_extractor=np.nan, A_preregistered=np.nan,
             sigma_boot=np.nan, sanity_ratio=np.nan,
             pa_flipped=False, weight="mom0", qc_pass=False, qc_reason="",
             curves=None)
    for key in ("avgmod", "mom1"):
        if dl_status.get(m[key], "").startswith("FAIL"):
            r["qc_reason"] = f"download failed: {m[key]}"
            return r
    try:
        geo, rc = pe.parse_avgmod(local_path(m["avgmod"]))
        pa = geo.get("PA_model_g", geo.get("PA_model"))
        r.update(ra=geo.get("RA_model", np.nan), dec=geo.get("DEC_model", np.nan),
                 cz=geo.get("VSys_model", np.nan), inc=geo.get("Inc_model", np.nan),
                 pa_wkapp=pa)
        if not rc or pa is None or "Inc_model" not in geo:
            r["qc_reason"] = "AvgMod parse incomplete (no RC/PA/inc)"
            return r
    except Exception as e:
        r["qc_reason"] = f"AvgMod parse error: {e}"
        return r
    try:
        hdu1 = fits.open(local_path(m["mom1"]))[0]
        vmap = np.squeeze(hdu1.data).astype(float)
        with np.errstate(invalid="ignore", divide="ignore"):
            vmap = C_KMS * (F0_HI / vmap - 1.0)     # Hz -> cz km/s
        w = WCS(hdu1.header).celestial
        x0, y0 = w.wcs_world2pix([[geo["RA_model"], geo["DEC_model"]]], 0)[0]
        cd1 = hdu1.header.get("CDELT1", -abs(hdu1.header.get("CD1_1", 0)) or None)
        cd2 = hdu1.header.get("CDELT2", hdu1.header.get("CD2_2", None))
        pix_as = (cd1 * 3600.0, cd2 * 3600.0)
        weight = None
        if not dl_status.get(m["mom0"], "").startswith("FAIL"):
            try:
                weight = np.squeeze(fits.open(local_path(m["mom0"]))[0].data).astype(float)
                if weight.shape != vmap.shape:
                    weight, r["weight"] = None, "none(shape)"
            except Exception:
                weight, r["weight"] = None, "none(read)"
        else:
            r["weight"] = "none(download)"
        rads = np.array([q[0] for q in rc])
        dr = np.median(np.diff(rads)) if len(rads) > 1 else 15.0
        ring_edges = np.concatenate([[max(rads[0] - dr / 2, 0.0)], rads + dr / 2])
        geom = {"x0": float(x0), "y0": float(y0), "pa_deg": float(pa),
                "inc_deg": float(geo["Inc_model"]), "vsys": float(geo["VSys_model"])}
        res = pe.extract(vmap, weight, geom, ring_edges, pix_as=pix_as, nboot=400)
    except Exception as e:
        r["qc_reason"] = f"extraction error: {type(e).__name__}: {e}"
        return r
    if res is None or res["sigma_A"] is None:
        r["qc_reason"] = "extractor returned no valid rings/bootstrap"
        return r

    # --- FROZEN empirical receding-side rule (QC_FROZEN.md) ---
    va_e, vr_e = res["v_app_outer"], res["v_rec_outer"]    # extractor labels
    # frozen rule: median deprojected v_rot < 0 -> PA anti-aligned with receding side
    ring_means = [0.5 * (c["v_app"] + c["v_rec"]) for c in res["curves"].values()]
    flipped = bool(np.median(ring_means) < 0)
    if flipped:
        v_rec_true, v_app_true = -va_e, -vr_e   # true receding side = extractor 'app'
    else:
        v_rec_true, v_app_true = vr_e, va_e
    A_ext = res["A"]                                        # 2(va-vr)/(va+vr) raw
    A_pre = 2.0 * (v_rec_true - v_app_true) / (v_rec_true + v_app_true)
    r.update(pa_flipped=bool(flipped), A_raw_extractor=float(A_ext),
             A_preregistered=float(A_pre), sigma_boot=float(res["sigma_A"]),
             v_rec=float(v_rec_true), v_appr=float(v_app_true),
             n_outer=len(res["outer_rings"]), curves=res["curves"])

    # sanity ratio vs released WKAPP azimuthal curve (matched rings, true speeds)
    sgn = -1.0 if flipped else 1.0
    both, wk = [], []
    for k, c in res["curves"].items():
        j = int(np.argmin(np.abs(rads - c["R_mid"])))
        if abs(rads[j] - c["R_mid"]) < dr:
            both.append(sgn * 0.5 * (c["v_app"] + c["v_rec"]))
            wk.append(rc[j][1])
    if both and all(v > 0 for v in wk):
        r["sanity_ratio"] = float(np.median(np.array(both) / np.array(wk)))

    # --- FROZEN QC cuts, in the frozen order ---
    if not (r["inc"] < 70.0):
        r["qc_reason"] = f"inc {r['inc']:.1f} >= 70"
    elif not (np.isfinite(r["sanity_ratio"]) and 0.8 <= r["sanity_ratio"] <= 1.2):
        r["qc_reason"] = f"sanity ratio {r['sanity_ratio']:.3f} outside [0.8,1.2]"
    elif r["n_outer"] < 4:
        r["qc_reason"] = f"n_outer {r['n_outer']} < 4"
    elif not (r["sigma_boot"] < 0.05):
        r["qc_reason"] = f"sigma_boot {r['sigma_boot']:.4f} >= 0.05"
    else:
        r["qc_pass"], r["qc_reason"] = True, "pass"
    return r


# ----------------------------------------------------------------------------
def main():
    open(LOG, "w").close()
    log("LANE W1 bulk per-side extraction -- QC frozen in QC_FROZEN.md BEFORE this run")
    log("FIREWALL: N~237 -> ~1-1.5 sigma at AQUAL amplitude; neither pre-registered "
        "kill condition (N~1157 canonical / 1424 alt) can trigger on this sample")
    rows = load_census()
    manifest = build_manifest(rows)
    dl_status = download_all(manifest)

    results = []
    for i, m in enumerate(manifest, 1):
        r = extract_galaxy(m, dl_status)
        results.append(r)
        if i % 20 == 0 or not r["qc_reason"].startswith(("pass",)):
            log(f"extract {i}/{len(manifest)} {r['jname']}: "
                f"A_pre={r['A_preregistered']:+.4f} sig={r['sigma_boot']:.4f} "
                f"QC={'PASS' if r['qc_pass'] else 'FAIL(' + r['qc_reason'] + ')'}"
                if np.isfinite(r["A_preregistered"]) else
                f"extract {i}/{len(manifest)} {r['jname']}: FAIL({r['qc_reason']})")

    # ---- CSV ----
    cols = ["jname", "ra", "dec", "cz", "field", "hires", "tr", "inc", "pa_wkapp",
            "pa_flipped", "n_outer", "v_rec", "v_appr", "A_raw_extractor",
            "A_preregistered", "sigma_boot", "sanity_ratio", "weight",
            "n_models_available", "model_file", "qc_pass", "qc_reason"]
    csv_path = os.path.join(HERE, "perside_237.csv")
    with open(csv_path, "w", newline="") as f:
        f.write("# LANE W1 per-side asymmetries, ALL per-side-capable WALLABY galaxies\n")
        f.write("# FIREWALL: N~237 -> ~1-1.5 sigma at AQUAL amplitude; NEITHER pre-registered\n")
        f.write("#   kill condition (3-sigma AQUAL-vs-BranchB, N~1157 canonical a0=9.36e-11 /\n")
        f.write("#   N~1424 alt a0=1.13e-10) CAN TRIGGER on this sample. a0 does not enter\n")
        f.write("#   this extraction; both footings enter at the confrontation stage only.\n")
        f.write("# CONVENTION: A_preregistered = 2(v_rec - v_appr)/(v_rec + v_appr), receding-\n")
        f.write("#   side tied (side determined EMPIRICALLY; pa_flipped flags anti-aligned PA).\n")
        f.write("#   A_raw_extractor = 2(v_app - v_rec)/(v_app + v_rec) as printed by the pilot\n")
        f.write("#   extractor (OPPOSITE ordering). PA_wkapp = Deg+22 PA_model_g, 'Position\n")
        f.write("#   angle in equatorial coordinates (East of North)' (arXiv:2211.07333 Tab.4).\n")
        f.write("# QC frozen BEFORE extraction: see QC_FROZEN.md.\n")
        wcsv = csv.DictWriter(f, fieldnames=cols)
        wcsv.writeheader()
        for r in results:
            wcsv.writerow({k: r[k] for k in cols})

    # ---- curves JSON (provenance) ----
    with open(os.path.join(HERE, "perside_237_curves.json"), "w") as f:
        json.dump({r["jname"]: {"model_file": r["model_file"],
                                "pa_flipped": r["pa_flipped"],
                                "curves": r["curves"]} for r in results
                   if r["curves"] is not None}, f, indent=0)

    # ---- funnel + distribution summary ----
    n_all = len(manifest)
    n_dl = sum(1 for r in results if not r["qc_reason"].startswith("download failed"))
    n_ext = sum(1 for r in results if np.isfinite(r["A_preregistered"]))
    n_pass = sum(1 for r in results if r["qc_pass"])
    n_flip = sum(1 for r in results if r["pa_flipped"])
    log(f"FUNNEL: 237 capable -> {n_dl} downloaded -> {n_ext} extracted -> {n_pass} QC pass")
    log(f"pa_flipped (empirical receding side opposite to WKAPP PA): {n_flip}")
    A = np.array([r["A_preregistered"] for r in results if r["qc_pass"]])
    s = np.array([r["sigma_boot"] for r in results if r["qc_pass"]])
    if len(A):
        log(f"QC-pass A_preregistered: mean={A.mean():+.4f} median={np.median(A):+.4f} "
            f"rms={A.std(ddof=1):.4f} (WHISP intrinsic rms 0.092)")
        log(f"QC-pass sigma_boot: median={np.median(s):.4f} "
            f"p10={np.percentile(s,10):.4f} p90={np.percentile(s,90):.4f}")
    from collections import Counter
    reasons = Counter(r["qc_reason"].split(":")[0] for r in results if not r["qc_pass"])
    for reason, n in reasons.most_common():
        log(f"  excluded [{reason}]: {n}")
    fields = Counter((r["field"], r["qc_pass"]) for r in results)
    for fld in sorted(set(r["field"] for r in results)):
        log(f"  field {fld}: {fields[(fld, True)]} pass / "
            f"{fields[(fld, True)] + fields[(fld, False)]} total")
    log(f"CSV written: {csv_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
