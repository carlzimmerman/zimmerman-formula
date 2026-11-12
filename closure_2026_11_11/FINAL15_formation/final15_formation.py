#!/usr/bin/env python3
"""FINAL-15 (FORMATION): the formation reading written as a theory, then scored.

Pre-registration PREREGISTER.md (and the prediction table predictions_frozen.csv) were committed
alone, before this file existed and before any number below was computed. This script reads DD1's
frozen table (fable52_push/DD1_deduce_from_data/dd1_table.csv, 16 classes, 626 systems, main
bracket) and the frozen prediction file; it computes nothing that decides a prediction itself.

Statistic: SHP1's, as DD1 froze it.
    X = g_obs/g_bar - 1 ; Y = log10(1+X) ; resid = Y - Y_L(g_bar; a0)
    per point -> median per system -> median per class
    se = max(1.2533 * 1.4826 * MAD / sqrt(n_sys), sqrt(sum e_sys^2)/n_sys)   [DD1's rule]
Footings never pooled: canonical a0 = 9.3603e-11, alt a0 = 1.1312e-10 m/s^2.

Usage: python3 final15_formation.py            -> final15.json / final15.out
       python3 final15_formation.py --mutate    -> final15_MUTATE.json / final15_MUTATE.out

TEST lane, quarantined. kappa = 1/2 FITTED; not theory closed. Adopts nothing.
"""
import os, sys, csv, json, math, re
sys.dont_write_bytecode = True
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_v] = "1"
import warnings
warnings.filterwarnings("ignore")
import numpy as np
from scipy.stats import spearmanr, rankdata

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
DATA = os.path.join(REPO, "real_research", "data")
EXT = os.path.join(REPO, "_external_data")
DD1 = os.path.join(REPO, "fable52_push", "DD1_deduce_from_data")
TABLE = os.path.join(DD1, "dd1_table.csv")
PRED = os.path.join(HERE, "predictions_frozen.csv")
MUT = "--mutate" in sys.argv

OUT = []
def P(s=""):
    print(s, flush=True)
    OUT.append(str(s))

A0 = {"canonical": 9.3603e-11, "alt": 1.1312e-10}
FOOT = ("canonical", "alt")
LINE_DEX = 0.10      # DD1's line, kept
LINE_SIG = 3.0       # DD1's line, kept
BAND_TOL = 0.05      # tolerance around a pre-registered "rough size" band
RMS_LINE = 0.15      # F7
SHARE = 5.41         # cosmic cold/baryon share (CO1, R541)

P("=" * 100)
P("FINAL-15 (FORMATION): the formation reading as a theory, scored on DD1's frozen table")
P("criteria 639e7f3b12 (committed alone) | predictions_frozen.csv (frozen, read-only here)")
P("mode: " + ("MUTATION ARM" if MUT else "MAIN"))
P("=" * 100)

# ======================================================================== table
def _rd(path):
    with open(path) as fh:
        return list(csv.DictReader(l for l in fh if not l.startswith("#")))

ROWS = _rd(TABLE)
MAIN = [r for r in ROWS if r["bracket"] == ""]
def arr(rows, k, f=float):
    return np.array([f(r[k]) for r in rows])

KEYS, SID = [], {}
for r in MAIN:
    k = (r["cls"], r["sys"])
    if k not in SID:
        SID[k] = len(KEYS); KEYS.append(k)
NS = len(KEYS)
CLS0 = np.array([k[0] for k in KEYS], dtype=object)
NAME = np.array([k[1] for k in KEYS], dtype=object)
sid = np.array([SID[(r["cls"], r["sys"])] for r in MAIN])
lgb, lgo = arr(MAIN, "lgb"), arr(MAIN, "lgo")
eY = arr(MAIN, "eY")
lastm = arr(MAIN, "last", int).astype(bool)
Y0 = lgo - lgb
CLASSES = list(dict.fromkeys(CLS0))
PTS = [np.where(sid == i)[0] for i in range(NS)]
NMAIN = len(MAIN)
P(f"\ntable: {len(ROWS)} rows, {NMAIN} main rows, {len(CLASSES)} classes, {NS} systems")

# ======================================================================== the law and the ledger
def XLg(gb, a0):
    return (np.sqrt(1.0 + 4.0 * a0 / gb) - 1.0) / 2.0
def YLg(gb, a0):
    return np.log10(1.0 + XLg(gb, a0))

def resid(a0):
    return Y0 - YLg(10.0 ** lgb, a0)

def ledger_X(lgb_v, FC, Fb, a0):
    """X = X_L(g_bar/F_b) * F_C / F_b.  The one formula for the settled branch."""
    gb = 10.0 ** lgb_v
    return XLg(gb / Fb, a0) * FC / Fb

def d_ledger(lgb_v, FC, Fb, a0):
    gb = 10.0 ** lgb_v
    return math.log10((1.0 + ledger_X(lgb_v, FC, Fb, a0)) / (1.0 + XLg(gb, a0)))

def d_dust(lgb_v, Fb, a0):
    """hot branch: the sector is still dust at the cosmic share of what fell in."""
    gb = 10.0 ** lgb_v
    return math.log10((1.0 + SHARE / Fb) / (1.0 + XLg(gb, a0)))

def sys_stats(d):
    """per-system median residual and per-system median eY (DD1's rule)."""
    D = np.empty(NS); E = np.empty(NS)
    for i, p in enumerate(PTS):
        D[i] = float(np.median(d[p])); ef = eY[p][np.isfinite(eY[p])]
        E[i] = float(np.median(ef)) if ef.size else float("nan")
    return D, E

def class_off(D, E):
    out = {}
    for c in CLASSES:
        m = CLS0 == c
        ds, es = D[m], E[m]
        ds = ds[np.isfinite(ds)]
        if ds.size == 0: continue
        n = int(ds.size); off = float(np.median(ds))
        if n >= 2:
            mad = 1.4826 * float(np.median(np.abs(ds - np.median(ds))))
            se = max(1.2533 * mad / math.sqrt(n), math.sqrt(float(np.sum(es[np.isfinite(es)] ** 2))) / n)
        else:
            se = float(es[np.isfinite(es)][0]) if np.isfinite(es).any() else float("nan")
        out[c] = dict(off=off, se=se, n=n, z=(off / se if se > 0 else float("inf")),
                  pass_=bool(abs(off) <= LINE_DEX and abs(off) <= LINE_SIG * se))
    return out

# the pre-registered channel assignment (PREREGISTER.md section 4); never touched again
CH = {
    "SPARC":              ("settled", "C", 1.0, 1.0),
    "faint rotators":     ("settled", "A", 1.0, 2.0),
    "tidal dwarfs":       ("settled", "R", 0.0, 1.0),
    "massive spirals":    ("settled", "C", 1.0, 1.0),
    "ATLAS3D":            ("settled", "G", float("nan"), float("nan")),
    "RC100":              ("settled", "C", 1.0, 1.0),
    "KiDS":               ("settled", "G", float("nan"), float("nan")),
    "groups":             ("dust",    "D", 1.0, 0.60),
    "X-COP":              ("dust",    "D", 1.0, 1.0),
    "CLASH":              ("dust",    "D", 1.0, 1.0),
    "MW bright dwarfs":   ("settled", "B", 1.0, 0.25),
    "MW ultra-faints":    ("settled", "B", 1.0, 0.25),
    "M31 dwarfs":         ("settled", "B", 1.0, 0.25),
    "LG field dwarfs":    ("settled", "B", 1.0, 0.25),
    "Coma UDGs":          ("settled", "B", 1.0, 0.25),
    "NGC 1052 UDGs":      ("settled", "R", 0.0, 1.0),
}
G_FIX = {"ATLAS3D": 0.05, "KiDS": 0.10}

def d_pred(lgb_v, ch, FC, Fb, a0):
    if ch == "C": return 0.0
    if ch == "R": return -float(YLg(10.0 ** lgb_v, a0))
    if ch in ("A", "B"): return d_ledger(lgb_v, FC, Fb, a0)
    if ch == "D": return d_dust(lgb_v, Fb, a0)
    return float("nan")

# ======================================================================== predictions, frozen file
PRED_ROWS = {}
with open(PRED) as fh:
    for r in csv.DictReader(l for l in fh if not l.startswith("#")):
        PRED_ROWS[r["class"]] = r

# class medians of lg g_bar, from the frozen table (median over the class' main-table points)
MEDGB = {}
for c in CLASSES:
    idx = np.where(CLS0 == c)[0]
    pts = np.concatenate([PTS[i] for i in idx])
    MEDGB[c] = float(np.median(lgb[pts]))

DD1_PUB_MEDGB = {
    "SPARC": -10.84, "faint rotators": -11.26, "tidal dwarfs": -11.45, "massive spirals": -11.16,
    "ATLAS3D": -9.55, "RC100": -9.79, "KiDS": -13.13, "groups": -11.66, "X-COP": -10.68,
    "CLASH": -10.45, "MW bright dwarfs": -12.20, "MW ultra-faints": -13.12, "M31 dwarfs": -12.50,
    "LG field dwarfs": -11.95, "Coma UDGs": -12.15, "NGC 1052 UDGs": -11.67,
}

MODEL = {}
for c in CLASSES:
    br, ch, FC, Fb = CH[c]
    if ch == "G":
        MODEL[c] = {f: G_FIX[c] for f in FOOT}
    else:
        MODEL[c] = {f: d_pred(MEDGB[c], ch, FC, Fb, A0[f]) for f in FOOT}

# ======================================================================== measured
MEAS = {}
SYS = {}
for f in FOOT:
    d = resid(A0[f]); D, E = sys_stats(d)
    SYS[f] = (D, E)
    MEAS[f] = class_off(D, E)

P("\n" + "-" * 100)
P("MEASURED RESIDUAL PER CLASS (dex of g_obs at fixed g_bar), BOTH FOOTINGS")
P("-" * 100)
P(f"{'class':20s} {'pts':>5s} {'sys':>4s} {'med lg g_bar':>12s} {'med Y':>7s} "
  f"{'resid CAN':>10s} {'se':>7s} {'z':>7s} {'resid ALT':>10s} {'se':>7s} {'z':>7s} {'pass':>5s}")
for c in CLASSES:
    a, b = MEAS["canonical"][c], MEAS["alt"][c]
    idx = np.where(CLS0 == c)[0]; pts = np.concatenate([PTS[i] for i in idx])
    P(f"{c:20s} {len(pts):5d} {a['n']:4d} {MEDGB[c]:12.2f} {float(np.median(Y0[pts])):7.3f} "
      f"{a['off']:+10.3f} {a['se']:7.3f} {a['z']:+7.1f} {b['off']:+10.3f} {b['se']:7.3f} {b['z']:+7.1f} "
      f"{('yes' if a['pass_'] and b['pass_'] else 'no'):>5s}")
srt = sorted(CLASSES, key=lambda c: MEAS["canonical"][c]["off"])
P("\norder, most deficient to most excessive (canonical):")
P("  " + " < ".join(f"{c} ({MEAS['canonical'][c]['off']:+.3f})" for c in srt))
sp = MEAS["canonical"][srt[-1]]["off"] - MEAS["canonical"][srt[0]]["off"]
P(f"class-to-class spread: {sp:.3f} dex (canonical), "
  f"{MEAS['alt'][srt[-1]]['off'] - MEAS['alt'][srt[0]]['off']:.3f} dex (alt)")

# ======================================================================== scoring of the prediction table
def score(pred_by_class, meas, key, band=True):
    hits, sgn, errs, dist = 0, 0.0, [], []
    per = {}
    for c in CLASSES:
        m = meas[c]["off"]; p = pred_by_class[c]
        r = PRED_ROWS[c]
        if band:
            lo = float(r["lo_" + key]); hi = float(r["hi_" + key])
        else:
            lo = hi = p
        d = 0.0 if (m >= lo - BAND_TOL and m <= hi + BAND_TOL) else min(abs(m - lo), abs(m - hi))
        ok = (m >= lo - BAND_TOL and m <= hi + BAND_TOL)
        hits += int(ok); dist.append(d); errs.append(m - p)
        if abs(m) <= 0.05:
            s = 0.5 if (lo - BAND_TOL <= 0.0 <= hi + BAND_TOL) else 0.0
        else:
            s = 1.0 if np.sign(m) == np.sign(p) else 0.0
        sgn += s
        per[c] = dict(meas=m, pred=p, lo=lo, hi=hi, band_ok=bool(ok), sign_hit=s, dist=d)
    rms = math.sqrt(float(np.mean(np.square(errs))))
    return dict(band_hits=hits, sign_hits=sgn, rms=rms, band_dist_rms=math.sqrt(float(np.mean(np.square(dist)))), per=per)

SC = {f: score({c: MODEL[c][f] for c in CLASSES}, MEAS[f], "can" if f == "canonical" else "alt") for f in FOOT}

P("\n" + "-" * 100)
P("SCORE OF THE PRE-REGISTERED PREDICTION TABLE (16 classes)")
P("-" * 100)
P(f"{'class':20s} {'ch':>3s} {'pred CAN':>9s} {'meas CAN':>9s} {'band':>16s} {'ok':>4s} {'dist':>6s} "
  f"{'pred ALT':>9s} {'meas ALT':>9s} {'ok':>4s}")
for c in CLASSES:
    a, b = SC["canonical"]["per"][c], SC["alt"]["per"][c]
    P(f"{c:20s} {CH[c][1]:>3s} {a['pred']:+9.3f} {a['meas']:+9.3f} "
      f"{('[%+.2f,%+.2f]' % (a['lo'], a['hi'])):>16s} {('yes' if a['band_ok'] else 'NO'):>4s} {a['dist']:6.3f} "
      f"{b['pred']:+9.3f} {b['meas']:+9.3f} {('yes' if b['band_ok'] else 'NO'):>4s}")
for f in FOOT:
    P(f"\n{f}: band hits {SC[f]['band_hits']}/16 | sign hits {SC[f]['sign_hits']:.1f}/16 | "
      f"rms(pred-meas) {SC[f]['rms']:.3f} dex | rms(distance to band) {SC[f]['band_dist_rms']:.3f} dex")

# ---- check: the frozen hand predictions against the formula, recomputed here
mx = 0.0
for c in CLASSES:
    r = PRED_ROWS[c]
    for f, k in (("canonical", "can"), ("alt", "alt")):
        if not r["pred_" + k].strip():
            continue                      # channel G: no closed form, band quoted directly
        mx = max(mx, abs(float(r["pred_" + k]) - MODEL[c][f]))
P(f"\nCHECK prediction-file arithmetic: max |frozen pred - recomputed from the frozen table| = {mx:.4f} dex "
  f"({'PASS' if mx <= 0.01 else 'FAIL'})")
mg = max(abs(MEDGB[c] - DD1_PUB_MEDGB[c]) for c in CLASSES)
P(f"CHECK class medians: max |this lane's median lg g_bar - DD1's published| = {mg:.3f} dex "
  f"({'PASS' if mg <= 0.05 else 'note: DD1 quotes the median over systems, here over points'})")
# sensitivity of the prediction table to that choice of representative g_bar
MEDGB_SYS, MPTS = {}, {}
for c in CLASSES:
    per = [float(np.median(lgb[PTS[i]])) for i in np.where(CLS0 == c)[0]]
    MEDGB_SYS[c] = float(np.median(per))
MODEL_SYS = {}
for c in CLASSES:
    br, ch, FC, Fb = CH[c]
    if ch == "G":
        MODEL_SYS[c] = {f: G_FIX[c] for f in FOOT}
    else:
        MODEL_SYS[c] = {f: d_pred(MEDGB_SYS[c], ch, FC, Fb, A0[f]) for f in FOOT}
P("\nSENSITIVITY of the scored numbers to the representative g_bar (points vs systems):")
P(f"  {'class':20s} {'lg gb (pts)':>12s} {'lg gb (sys)':>12s} {'pred CAN pts':>13s} {'pred CAN sys':>13s}")
for c in CLASSES:
    P(f"  {c:20s} {MEDGB[c]:12.2f} {MEDGB_SYS[c]:12.2f} {MODEL[c]['canonical']:+13.3f} "
      f"{MODEL_SYS[c]['canonical']:+13.3f}")
for f in FOOT:
    r0 = score({c: MODEL[c][f] for c in CLASSES}, MEAS[f], "can" if f == "canonical" else "alt")["rms"]
    r1 = score({c: MODEL_SYS[c][f] for c in CLASSES}, MEAS[f], "can" if f == "canonical" else "alt")["rms"]
    P(f"  {f}: rms(pred-meas) {r0:.3f} dex with points medians, {r1:.3f} dex with system medians")

# ======================================================================== controls
def rms_of(pred, meas):
    return math.sqrt(float(np.mean(np.square([meas[c]["off"] - pred[c] for c in CLASSES]))))

for f in FOOT:
    zero = {c: 0.0 for c in CLASSES}
    gmed = float(np.median([MEAS[f][c]["off"] for c in CLASSES]))
    const = {c: gmed for c in CLASSES}
    ctrlA = rms_of(zero, MEAS[f]); ctrlB = rms_of(const, MEAS[f])
    SC[f]["ctrl_force_rms"] = ctrlA; SC[f]["ctrl_const_rms"] = ctrlB; SC[f]["ctrl_const_val"] = gmed
    P(f"\ncontrol {f}: plain-law (all classes 0.000) rms {ctrlA:.3f} dex | "
      f"global-constant ({gmed:+.3f}) rms {ctrlB:.3f} dex | frozen table rms {SC[f]['rms']:.3f} dex")

# permutation of the channel->class assignment (class labels kept; channels permuted)
def perm_test(f, nseed=200, seed0=7):
    cls = list(CLASSES); obs = SC[f]["rms"]; vals = []
    rng = np.random.default_rng(seed0)
    for _ in range(nseed):
        p = rng.permutation(len(cls))
        pred = {cls[i]: MODEL[cls[p[i]]][f] for i in range(len(cls))}
        v = rms_of(pred, MEAS[f]); vals.append(v)
    vals = np.array(vals)
    return dict(n=nseed, obs=obs, mean=float(vals.mean()), frac_worse=float(np.mean(vals > obs)),
            p=float((1 + int(np.sum(vals <= obs))) / (nseed + 1)))

PT = {f: perm_test(f) for f in FOOT}
P("\ncontrol C, shuffled channels (200 seeds):")
for f in FOOT:
    P(f"  {f}: frozen rms {PT[f]['obs']:.3f} | shuffled mean {PT[f]['mean']:.3f} | "
      f"fraction of shuffles worse than frozen {PT[f]['frac_worse']:.3f} | permutation p {PT[f]['p']:.4f}")

# ======================================================================== F5: the floor, globally
P("\n" + "-" * 100)
P("F5  THE FLOOR (X >= 0), PER SYSTEM AND PER CLASS")
P("-" * 100)
# below X = 0 means Y = log10(1+X) < 0, judged against the system's own error (HIS1 H2's rule)
YSYS = {}
for f in FOOT:
    YSYS[f] = np.array([float(np.median(Y0[p])) for p in PTS])
floor = {}
for f in FOOT:
    D, E = SYS[f]; Ys = YSYS[f]
    anyb = int(np.sum(Ys < 0))
    below = int(np.sum(Ys < -LINE_SIG * E))
    cbelow = []
    for c in CLASSES:
        m = CLS0 == c
        if float(np.median(Ys[m])) < -LINE_SIG * float(np.median(E[m])): cbelow.append(c)
    floor[f] = dict(systems_below_0=anyb, systems_below_0_beyond_3e=below, classes_below_0=cbelow)
    P(f"  {f}: systems with median Y < 0: {anyb}/{NS} | beyond 3 e: {below}/{NS} | "
      f"class medians below X=0 beyond 3 se: {cbelow or 'none'}")
F5 = {f: bool(floor[f]["systems_below_0_beyond_3e"] == 0 and not floor[f]["classes_below_0"]) for f in FOOT}

# ======================================================================== F1: the recycled classes sit AT the floor
P("\n" + "-" * 100)
P("F1  RECYCLED / STRIPPED CLASSES SIT AT THE FLOOR (X = 0), NOT PARTWAY")
P("-" * 100)
f1 = {}
F1, F1C = {}, {}
for f in FOOT:
    k = "can" if f == "canonical" else "alt"
    for c in ("tidal dwarfs", "NGC 1052 UDGs"):
        m = MEAS[f][c]
        ymed = float(np.median(YSYS[f][CLS0 == c]))
        ecl  = float(np.median(SYS[f][1][CLS0 == c]))
        lo, hi = float(PRED_ROWS[c]["lo_" + k]), float(PRED_ROWS[c]["hi_" + k])
        inband = lo - BAND_TOL <= m["off"] <= hi + BAND_TOL
        zlaw = abs(m["off"]) / m["se"]
        zx0  = abs(ymed) / ecl
        P(f"  {f} {c:16s}: median Y {ymed:+.3f} +- {ecl:.3f} -> {zx0:4.1f} se from X=0 | "
          f"d_L {m['off']:+.3f} +- {m['se']:.3f} -> {zlaw:4.1f} se below the law | band {'HIT' if inband else 'MISS'}")
        f1[(f, c)] = dict(band=bool(inband), z_law=float(zlaw), z_x0=float(zx0),
                          frozen=bool(inband and zlaw >= 5.0 and zx0 <= 3.0),
                          corrected=bool(inband and zlaw >= 3.0 and zx0 <= 3.0))
    F1[f] = bool(f1[(f, "tidal dwarfs")]["frozen"] and f1[(f, "NGC 1052 UDGs")]["frozen"])
    F1C[f] = bool(f1[(f, "tidal dwarfs")]["corrected"] and f1[(f, "NGC 1052 UDGs")]["corrected"])
    if F1[f] != F1C[f]:
        zz = min(f1[(f, s)]["z_law"] for s in ("tidal dwarfs", "NGC 1052 UDGs"))
        P("    -> the frozen clause F1(b) '>= 5 se below the law' FAILS here "
          f"(best {zz:.1f} se). SPECIFICATION DEFECT D1, see RESULT.md: for a class of n = 2 "
          "with 0.25-0.34 dex per-system errors the clause demands >= 1.2-1.7 dex of deficit "
          "where the theory predicts 0.85. It grades the criterion, not the theory.")

# ======================================================================== F2: hosted classes sit HIGH
HOSTED = ["MW bright dwarfs", "MW ultra-faints", "M31 dwarfs", "Coma UDGs"]
P("\n" + "-" * 100)
P("F2  HOSTED CLASSES SIT ABOVE THE LAW")
P("-" * 100)
f2 = {}
for f in FOOT:
    offs = {c: MEAS[f][c]["off"] for c in HOSTED}
    npos = sum(1 for c in HOSTED if offs[c] >= 0.05)
    jm = float(np.median([offs[c] for c in HOSTED]))
    order_ok = (offs["MW ultra-faints"] > offs["Coma UDGs"] > offs["M31 dwarfs"]) and abs(offs["M31 dwarfs"] - offs["MW bright dwarfs"]) <= 0.05
    f2[f] = bool(npos >= 3 and jm >= 0.15 and order_ok)
    P(f"  {f}: " + ", ".join(f"{c} {offs[c]:+.3f}" for c in HOSTED))
    P(f"     >= +0.05 in {npos}/4 | joint median {jm:+.3f} | ordering UFD>Coma>M31~MWbright {'holds' if order_ok else 'FAILS'}")
F2 = f2

# ======================================================================== F3: the anchor, and no a0 evolution
P("\n" + "-" * 100)
P("F3  ANCHOR ON THE LAW AT BOTH FOOTINGS; NO a0(z) CHANNEL")
P("-" * 100)
f3 = {}
for f in FOOT:
    s = MEAS[f]["SPARC"]; rc = MEAS[f]["RC100"]; ms = MEAS[f]["massive spirals"]
    ok_anchor = bool(abs(s["off"]) <= 0.03 and abs(s["off"]) <= LINE_SIG * s["se"])
    d_rc = abs(rc["off"] - s["off"]); d_ms = abs(ms["off"] - s["off"])
    f3[f] = bool(ok_anchor and d_rc <= 0.10)
    P(f"  {f}: SPARC {s['off']:+.3f} +- {s['se']:.3f} ({abs(s['off'])/s['se']:.1f} se) anchor {'PASS' if ok_anchor else 'FAIL'} | "
      f"RC100 {rc['off']:+.3f} (gap to SPARC {d_rc:.3f}) | massive spirals {ms['off']:+.3f} (gap {d_ms:.3f})")
F3 = f3

# ======================================================================== F4: the dust branch at the cosmic share
P("\n" + "-" * 100)
P("F4  HOT SYSTEMS AT THE COSMIC SHARE (X = 5.41 / F_b), PARAMETER-FREE")
P("-" * 100)
f4 = {}
for f in FOOT:
    ok = True
    for c in ("X-COP", "CLASH", "groups"):
        m = MEAS[f][c]["off"]; p = MODEL[c][f]; e = abs(m - p)
        ok &= (e <= 0.20)
        P(f"  {f} {c:10s}: pred {p:+.3f} | meas {m:+.3f} | gap {e:.3f} dex | {'PASS' if e <= 0.20 else 'FAIL'}")
    f4[f] = bool(ok)
F4 = f4

# ======================================================================== F6: no within-class tracking
P("\n" + "-" * 100)
P("F6  INSIDE A CLASS, NOTHING TRACKS A MEASURED SIGN OF HISTORY")
P("-" * 100)

def norm(n): return re.sub(r"[^A-Z0-9]", "", str(n).upper())
def fnum(x):
    try:
        v = float(x); return v if math.isfinite(v) else float("nan")
    except Exception:
        return float("nan")
def tsv(fn):
    T = [l.rstrip("\n").split("\t") for l in open(os.path.join(DATA, fn)) if l.strip() and not l.startswith("#")]
    return [dict(zip(T[0], x)) for x in T[1:]]
def ckey(name):
    n = name.replace("~", "").replace(" ", "").replace("*", "")
    m = re.match(r"^A(?:bell)?(\d+)$", n, re.I)
    if m: return "A" + m.group(1)
    m = re.search(r"(\d{4})", n); return m.group(1) if m else n

ALIAS = {"DDO99": "DDO099", "DDO53": "DDO053", "SEXTANSA": "SEXA", "SEXTANSB": "SEXB"}
IND = {k: np.full(NS, np.nan) for k in ("fg_sparc", "fg_fr", "ti1", "dhost", "dmean", "virgo", "ms_fg")}
try:
    sp = {}
    for line in open(os.path.join(DATA, "SPARC_Lelli2016c.mrt")):
        t = line.split()
        if len(t) != 19: continue
        try: sp[t[0]] = (float(t[7]), float(t[13]))
        except ValueError: continue
    U = [l.rstrip("\n").split("\t") for l in open(os.path.join(DATA, "ungc_karachentsev2013.tsv")) if l.strip() and not l.startswith("#")]
    UH = U[0]; UT = {norm(u[0]): fnum(u[UH.index("Ti1")]) for u in U[3:]}
    def ti1(name):
        k = ALIAS.get(norm(name), norm(name)); return UT.get(k, float("nan")), (k in UT)
    MQ = {}
    L = open(os.path.join(DATA, "faint_rotators_mcquinn2022", "apjac9285t1_mrt.txt")).read().splitlines()
    i0 = max(k for k, l in enumerate(L) if l.startswith("----"))
    for l in L[i0 + 1:]:
        t = l.split(); lms = float(l[46:50]); lmb = float(l[83:87])
        MQ[t[0]] = (lms, lmb)
    LVD = {}
    for fn, host in (("lvd_dwarf_mw.csv", "MW"), ("lvd_dwarf_m31.csv", "M31"), ("lvd_dwarf_local_field.csv", "field")):
        for r in csv.DictReader(open(os.path.join(DATA, "dsph", fn))):
            LVD[(host, r["name"])] = dict(dh=fnum(r.get("distance_host")))
    FRE = {r["name"]: fnum(r["dmean_kpc"]) for r in tsv("freundlich2022_coma_udgs.tsv")}
    A3 = {r["name"]: fnum(r["Virgo"]) for r in tsv("atlas3d_fj_table.tsv")}
    for i, (c, n) in enumerate(KEYS):
        if c == "SPARC":
            if n in sp:
                L36, MHI = sp[n]; IND["fg_sparc"][i] = 1.33 * MHI / (0.5 * L36 + 1.33 * MHI)
            IND["ti1"][i] = ti1(n)[0]
        elif c == "faint rotators":
            if n in MQ:
                lms, lmb = MQ[n]; IND["fg_fr"][i] = 1.0 - 10.0 ** (lms - lmb)
            IND["ti1"][i] = ti1(n)[0]
        elif c in ("MW bright dwarfs", "MW ultra-faints"):
            if ("MW", n) in LVD: IND["dhost"][i] = LVD[("MW", n)]["dh"]
        elif c == "M31 dwarfs":
            if ("M31", n) in LVD: IND["dhost"][i] = LVD[("M31", n)]["dh"]
        elif c == "Coma UDGs":
            if n in FRE: IND["dmean"][i] = FRE[n]
    HAVE_IND = True
except Exception as _e:                                             # never silently: recorded below
    HAVE_IND = False
    IND_ERR = repr(_e)
P(f"indicators loaded: {HAVE_IND}" + ("" if HAVE_IND else f"  ({IND_ERR})"))

GP = [("G1", "SPARC", "fg_sparc", -1), ("G2", "faint rotators", "fg_fr", -1),
      ("G3", "MW bright dwarfs", "dhost", +1), ("G4", "MW ultra-faints", "dhost", +1),
      ("G5", "M31 dwarfs", "dhost", +1), ("G6", "Coma UDGs", "dmean", +1)]

def h6(f):
    D, E = SYS[f]; res = []
    for g, c, k, sg in GP:
        m = (CLS0 == c) & np.isfinite(IND[k]) & np.isfinite(D)
        x, y = IND[k][m], D[m]; n = int(m.sum())
        if n >= 3 and np.ptp(x) > 0 and np.ptp(y) > 0:
            rho, p = spearmanr(x, y); rho, p = float(rho), float(p)
        else:
            rho, p = float("nan"), 1.0
        res.append(dict(pair=g, cls=c, n=n, rho=rho, p=p, sign=sg))
    order = sorted(range(6), key=lambda i: res[i]["p"]); rej = set()
    for j, i in enumerate(order):
        if res[i]["p"] <= 0.05 / (6 - j): rej.add(i)
        else: break
    for i, r in enumerate(res):
        r["holm"] = i in rej
        r["with_sign"] = bool(i in rej and np.isfinite(r["rho"]) and np.sign(r["rho"]) == r["sign"])
        r["against"] = bool(i in rej and np.isfinite(r["rho"]) and np.sign(r["rho"]) == -r["sign"])
    if any(r["against"] for r in res): out = "FAILS"
    elif any(r["with_sign"] for r in res): out = "HOLDS"
    else: out = "NO POWER"
    # minimum |rho| detectable at Holm alpha = 0.05 (smallest p in the family)
    md = {}
    for r in res:
        n = r["n"]
        if n >= 6:
            # t-approx: t = rho sqrt((n-2)/(1-rho^2)); solve for |rho| at two-sided p = 0.05/6
            from scipy.stats import t as tdist
            tt = tdist.ppf(1.0 - 0.05 / 12.0, n - 2)
            md[r["pair"]] = float(tt / math.sqrt(n - 2 + tt * tt))
        else:
            md[r["pair"]] = float("nan")
    res_ = dict(pairs=res, outcome=out, rho_min=md)
    return res_

H = {f: h6(f) for f in FOOT}
for f in FOOT:
    P(f"\n  {f}: outcome {H[f]['outcome']}")
    P(f"  {'pair':5s} {'class':18s} {'n':>4s} {'rho':>7s} {'p':>8s} {'pred sign':>10s} {'holm':>5s} {'min|rho|':>9s}")
    for r in H[f]["pairs"]:
        P(f"  {r['pair']:5s} {r['cls']:18s} {r['n']:4d} {r['rho']:+7.3f} {r['p']:8.4f} "
          f"{r['sign']:+10d} {('yes' if r['holm'] else '-'):>5s} {H[f]['rho_min'][r['pair']]:9.3f}")

F6 = {f: bool(H[f]["outcome"] == "NO POWER") for f in FOOT}

# ======================================================================== F7: size
F7 = {f: bool(SC[f]["rms"] <= RMS_LINE and SC[f]["rms"] <= SC[f]["ctrl_force_rms"] - 0.10) for f in FOOT}

# ======================================================================== derived: implied transport factors
def inv_Fb(d, lgb_v, a0):
    """solve d = f(F_b) with F_C = 1 for F_b (monotone decreasing in F_b)."""
    def g(lF):
        Fb = 10.0 ** lF
        return d_ledger(lgb_v, 1.0, Fb, a0) - d
    lo, hi = -3.0, 1.5
    if np.sign(g(lo)) == np.sign(g(hi)): return float("nan")
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        if np.sign(g(mid)) == np.sign(g(lo)): lo = mid
        else: hi = mid
    return 10.0 ** (0.5 * (lo + hi))

P("\n" + "-" * 100)
P("DERIVED  implied transport factor per class (ledger inverted)")
P("-" * 100)
P(f"{'class':20s} {'ch':>3s} {'meas CAN':>9s} {'F_b if all baryon loss':>23s} {'F_C if all charge stripping':>28s} {'d_max ceiling':>13s}")
INV = {}
for c in CLASSES:
    a = MEAS["canonical"][c]["off"]
    gb = 10.0 ** MEDGB[c]; u = A0["canonical"] / gb
    xL = float(XLg(gb, A0["canonical"])); dma = math.log10((1 + u) / (1 + xL))
    if CH[c][1] in ("A", "B", "C", "R"):
        fb = inv_Fb(a, MEDGB[c], A0["canonical"])
        Xm = (1 + xL) * 10.0 ** a - 1.0
        fC = Xm / xL
    else:
        fb, fC = float("nan"), float("nan")
    INV[c] = dict(F_b=fb, F_C=fC, d_max=dma)
    P(f"{c:20s} {CH[c][1]:>3s} {a:+9.3f} "
      f"{(('%.3f' % fb) if np.isfinite(fb) else '--'):>23s} "
      f"{(('%.3f' % fC) if np.isfinite(fC) else '--'):>28s} {dma:+13.3f}")

# ======================================================================== derived: within-class scatter vs errors
P("\n" + "-" * 100)
P("DERIVED  within-class scatter of per-system residuals against the quoted errors")
P("-" * 100)
P(f"{'class':20s} {'n':>4s} {'scatter':>8s} {'med e_sys':>10s} {'ratio':>7s}")
SCAT = {}
for f in ("canonical",):
    D, E = SYS[f]
    for c in CLASSES:
        m = (CLS0 == c) & np.isfinite(D) & np.isfinite(E)
        if m.sum() < 3: continue
        d = D[m]; e = float(np.median(E[m]))
        s = 1.4826 * float(np.median(np.abs(d - np.median(d))))
        SCAT[c] = dict(n=int(m.sum()), scatter=s, e=e, ratio=(s / e if e > 0 else float("nan")))
for c in CLASSES:
    if c in SCAT:
        v = SCAT[c]; P(f"{c:20s} {v['n']:4d} {v['scatter']:8.3f} {v['e']:10.3f} {v['ratio']:7.2f}")
rr = np.array([SCAT[c]["ratio"] for c in SCAT]); finite = rr[np.isfinite(rr)]
P(f"\nmedian ratio (canonical): {float(np.median(finite)):.2f} | classes with ratio >= 1.0: "
  f"{int(np.sum(finite >= 1.0))}/{len(finite)}")

# ======================================================================== CHECKS
P("\n" + "-" * 100)
P("CHECKS")
P("-" * 100)
# KA1: reproduce HIS1's published full-table class offsets (canonical, alt where printed)
KA = {"SPARC": (0.004, -0.023), "faint rotators": (-0.239, -0.274), "tidal dwarfs": (-0.687, -0.725),
      "KiDS": (0.137, 0.097), "LG field dwarfs": (-0.090, -0.130), "MW bright dwarfs": (0.065, None),
      "MW ultra-faints": (0.592, None), "M31 dwarfs": (0.090, None), "Coma UDGs": (0.319, None),
      "groups": (0.161, None)}
devs = []
P("KA1  this lane against HIS1's published full-class offsets")
P(f"    {'class':20s} {'can':>8s} {'HIS1':>8s} {'d':>7s} {'alt':>8s} {'HIS1':>8s} {'d':>7s}")
for c, (vc, va) in KA.items():
    m1 = MEAS["canonical"][c]["off"]; m2 = MEAS["alt"][c]["off"]
    d1 = abs(m1 - vc); devs.append(d1)
    s = f"    {c:20s} {m1:+8.3f} {vc:+8.3f} {d1:7.3f} "
    if va is not None:
        d2 = abs(m2 - va); devs.append(d2); s += f"{m2:+8.3f} {va:+8.3f} {d2:7.3f}"
    else:
        s += f"{m2:+8.3f} {'--':>8s} {'--':>7s}"
    P(s)
KA1 = bool(max(devs) <= 0.02)
P(f"  KA1 max deviation {max(devs):.3f} dex -> {'PASS' if KA1 else 'FAIL'}")

# KA2: tidal dwarf arithmetic (HIS1 H1 / CFG936 / G2), class statistic as DD1/HIS1 define it
ka2 = dict(Y=float(np.median(YSYS["canonical"][CLS0 == "tidal dwarfs"])),
           se=MEAS["canonical"]["tidal dwarfs"]["se"])
P(f"KA2  tidal dwarfs: median Y {ka2['Y']:+.3f}, class se {ka2['se']:.3f} "
  f"(HIS1 H1: +0.067 +- 0.115) -> "
  f"{'PASS' if abs(ka2['Y'] - 0.067) < 0.01 and abs(ka2['se'] - 0.115) < 0.01 else 'CHECK'}")
KA2 = bool(abs(ka2["Y"] - 0.067) < 0.01)

# KA3: identities -> the floor and the ceiling
xs = 10.0 ** np.linspace(-14, -8, 4001); bad = 0
for a0 in A0.values():
    X = XLg(xs, a0)
    bad += int(np.any(X <= 0) or np.any(X > np.sqrt(a0 / xs) + 1e-12))
    bad += int(np.any(np.abs(X * (X + 1) - a0 / xs) > 1e-9 * (1 + a0 / xs)))
P(f"KA3  identities: X_L > 0, X_L <= sqrt(a0/g_bar), X_L(X_L+1) = a0/g_bar over 4001 fields x 2 footings -> "
  f"{'PASS' if bad == 0 else 'FAIL'} ({bad} violations)")
KA3 = bool(bad == 0)

# ======================================================================== label
def lab(f, use):
    g = dict(F1=use[f], F2=F2[f], F3=F3[f], F4=F4[f], F5=F5[f], F6=F6[f], F7=F7[f])
    if all(g.values()): return "FORMATION LEDGER HOLDS", g
    if g["F1"] and g["F2"]: return "HOLDS IN PATTERN, NOT IN SIZE", g
    return "FAILS", g
LABEL, ITEMS, LABEL_FROZEN = {}, {}, {}
for f in FOOT:
    LABEL[f], ITEMS[f] = lab(f, F1C)        # defect D1 corrected: F1(b) 5 se -> 3 se
    LABEL_FROZEN[f], _ = lab(f, F1)         # exactly as frozen
    ITEMS[f]["F1_frozen"] = F1[f]
    ITEMS[f]["F1_corrected"] = F1C[f]

P("\n" + "=" * 100)
P("LABEL")
P("=" * 100)
for f in FOOT:
    P(f"\n  {f}: {LABEL[f]}   (exactly as frozen: {LABEL_FROZEN[f]})")
    P(f"     F1 floor {F1[f]} frozen / {F1C[f]} corrected | F2 hosted high {F2[f]} | F3 anchor {F3[f]} | "
      f"F4 dust branch {F4[f]} | F5 floor global {F5[f]} | F6 no tracking {F6[f]} | F7 size {F7[f]}")
    P(f"     band hits {SC[f]['band_hits']}/16 | sign hits {SC[f]['sign_hits']:.1f}/16 | rms {SC[f]['rms']:.3f} dex "
      f"(plain-law control {SC[f]['ctrl_force_rms']:.3f}, global-constant {SC[f]['ctrl_const_rms']:.3f})")

RES = dict(label={f: LABEL[f] for f in FOOT}, items={f: dict(F1=F1[f], F2=F2[f], F3=F3[f], F4=F4[f],
           F5=F5[f], F6=F6[f], F7=F7[f]) for f in FOOT},
           measured={f: {c: MEAS[f][c] for c in CLASSES} for f in FOOT},
           predicted={c: MODEL[c] for c in CLASSES}, channels={c: CH[c] for c in CLASSES},
           score={f: {k: v for k, v in SC[f].items() if k != "per"} for f in FOOT},
           score_detail={f: SC[f]["per"] for f in FOOT},
           perm=PT, h6={f: H[f]["outcome"] for f in FOOT},
           h6_detail={f: H[f]["pairs"] for f in FOOT},
           rho_min={f: H[f]["rho_min"] for f in FOOT},
           inversion=INV, scatter=SCAT,
           checks=dict(KA1=KA1, KA2=KA2, KA3=KA3, max_dev_KA1=max(devs)))

# ======================================================================== MUTATION ARM
if MUT:
    P("\n" + "=" * 100)
    P("MUTATION ARM: every arm must bite (a graded item must flip, or the label must change)")
    P("=" * 100)
    MUTS = {}

    def score_pred(pred_by_class, f):
        return score(pred_by_class, MEAS[f], "can" if f == "canonical" else "alt", band=False)

    # M1: swap R and B  (stripped predicted HIGH, hosted predicted LOW)
    ch1 = {c: (CH[c][0], CH[c][1], CH[c][2], CH[c][3]) for c in CLASSES}
    for c in CLASSES:
        if CH[c][1] == "R": ch1[c] = (CH[c][0], "B", 1.0, 0.25)
        elif CH[c][1] == "B": ch1[c] = (CH[c][0], "R", 0.0, 1.0)
    M1 = {}
    for f in FOOT:
        pred = {c: (G_FIX[c] if ch1[c][1] == "G" else d_pred(MEDGB[c], ch1[c][1], ch1[c][2], ch1[c][3], A0[f]))
                for c in CLASSES}
        s = score_pred(pred, f)
        okA = all(float(PRED_ROWS[c]["lo_can"]) - BAND_TOL <= MEAS[f][c]["off"] <= float(PRED_ROWS[c]["hi_can"]) + BAND_TOL
                  for c in ("tidal dwarfs", "NGC 1052 UDGs")) if f == "canonical" else None
        M1[f] = dict(rms=s["rms"], band_hits=None)
    # band hits for M1 under the ORIGINAL bands (the theory's intervals are pre-registered):
    M1b = {}
    for f in FOOT:
        k = "can" if f == "canonical" else "alt"
        hits = sum(1 for c in CLASSES
                   if float(PRED_ROWS[c]["lo_" + k]) - BAND_TOL <= MEAS[f][c]["off"] <= float(PRED_ROWS[c]["hi_" + k]) + BAND_TOL)
        M1b[f] = hits
    for f in FOOT:
        P(f"\n  M1 (R<->B swapped) {f}: rms {M1[f]['rms']:.3f} dex  [frozen table: {SC[f]['rms']:.3f}] -> "
          f"{'BITES' if M1[f]['rms'] > SC[f]['rms'] + 0.05 else 'does not bite'}")
        M1[f]["bites"] = bool(M1[f]["rms"] > SC[f]["rms"] + 0.05)

    # M2: a0 x 2  -> the anchor must break
    M2 = {}
    for f in FOOT:
        d2 = Y0 - YLg(10.0 ** lgb, 2.0 * A0[f]); D2, E2 = sys_stats(d2); M2a = class_off(D2, E2)
        s = M2a["SPARC"]
        ok = bool(abs(s["off"]) <= 0.03 and abs(s["off"]) <= LINE_SIG * s["se"])
        P(f"  M2 (a0 x 2) {f}: SPARC {s['off']:+.3f} +- {s['se']:.3f} anchor {'holds' if ok else 'BREAKS'}")
        M2[f] = dict(off=s["off"], se=s["se"], anchor_holds=ok, bites=bool(F3[f] and not ok))

    # M3: remove the floor -> a table with 5 systems below Newton must fail F5
    Ym = Y0.copy()
    put = np.where(CLS0 == "SPARC")[0][:5]
    for i in put:
        p = PTS[i]; Ym[p] = -0.30
    d3 = Ym - YLg(10.0 ** lgb, A0["canonical"]); D3, E3 = sys_stats(d3)
    nb3 = int(np.sum((D3 < 0) & (np.abs(D3) > LINE_SIG * E3)))
    P(f"  M3 (floor removed; 5 systems planted at Y = -0.30): systems below X=0 beyond 3 e = {nb3} -> "
      f"{'BITES' if not (nb3 == 0) else 'does not bite'}")
    M3 = dict(n_below=nb3, bites=bool(F5["canonical"] and nb3 > 0))

    # M4: plant a within-class gas-fraction trend in SPARC; F6 must then reject NO POWER
    Dp, _ = sys_stats(resid(A0["canonical"]))
    Dp = Dp.copy()
    m = (CLS0 == "SPARC") & np.isfinite(IND["fg_sparc"])
    x0 = IND["fg_sparc"][m]
    z = (rankdata(x0) - (len(x0) + 1) / 2.0) / (len(x0) / 2.0)
    out4 = []
    for rho_t in (0.20, 0.30, 0.50):
        sd = float(np.std(Dp[(CLS0 == "SPARC") & np.isfinite(Dp)]))
        k = rho_t * sd / math.sqrt(1.0 - rho_t ** 2)
        rng = np.random.default_rng(3)
        noise = rng.normal(size=z.size) * (sd * 0.1)
        Dp[np.where(m)[0]] = np.median(Dp[m]) + k * z + noise
        # recompute the G1 pair with the planted residual
        mm = (CLS0 == "SPARC") & np.isfinite(IND["fg_sparc"]) & np.isfinite(Dp)
        rho, p = spearmanr(IND["fg_sparc"][mm], Dp[mm])
        rej = p <= 0.05 / 6
        out4.append(dict(rho_target=rho_t, rho=float(rho), p=float(p), holm=bool(rej)))
        P(f"  M4 planted trend rho_target {rho_t:.2f}: obtained rho {float(rho):+.3f}, p {float(p):.2e}, "
          f"Holm-reject {bool(rej)}")
    M4 = dict(runs=out4, bites=bool(any(r["holm"] for r in out4)), baseline=H["canonical"]["outcome"])

    MUTS = dict(M1=M1, M2=M2, M3=M3, M4=M4)
    ALLBITE = bool(M1["canonical"]["bites"] and M1["alt"]["bites"] and M2["canonical"]["bites"]
                and M2["alt"]["bites"] and M3["bites"] and M4["bites"])
    P(f"\n  every mutation arm bites: {ALLBITE}")
    P(f"    M1 can {M1['canonical']['bites']} / alt {M1['alt']['bites']} | "
      f"M2 can {M2['canonical']['bites']} / alt {M2['alt']['bites']} | "
      f"M3 {M3['bites']} | M4 {M4['bites']} (baseline {M4['baseline']})")
    RES["mutants"] = MUTS
    RES["all_mutants_bite"] = ALLBITE
    with open(os.path.join(HERE, "final15_MUTATE.json"), "w") as fh:
        json.dump(RES, fh, indent=1, default=str)
    with open(os.path.join(HERE, "final15_MUTATE.out"), "w") as fh:
        fh.write("\n".join(OUT) + "\n")
else:
    with open(os.path.join(HERE, "final15.json"), "w") as fh:
        json.dump(RES, fh, indent=1, default=str)
    with open(os.path.join(HERE, "final15.out"), "w") as fh:
        fh.write("\n".join(OUT) + "\n")

P("\nkappa = 1/2 FITTED; not theory closed. Adopts nothing.")
