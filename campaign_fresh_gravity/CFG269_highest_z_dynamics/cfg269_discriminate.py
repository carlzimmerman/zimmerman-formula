#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
CFG269 -- FLAT a0 against the rival a0 x E(z) at z >= 4 to z ~ 14: a two-law DISCRIMINATION pre-flight (scoping lane).

kappa = 1/2 is FITTED.  a0(z) FLAT is the framework's distinctive law, a0 proportional to H(z) the rival; LambdaCDM has no a0 and its line is
CFG222's effective-a0 PROXY (reported only).  Nothing printed here is a measurement of a0: it is a discrimination between two a0(z) laws under a
declared dynamical estimator and a declared baryon calibration.  No sentence says the data favour the framework.

Criteria: FROZEN_CRITERIA.md (written before any observed D of this lane was computed; its sha256 is printed and checked to exist).

Stages
  A  predictions only: y, D_pred(FLAT), D_pred(RIVAL), the gap G and the power P for every row.  For census rows P comes from a Monte Carlo of
     the FRACTIONAL kinematic errors around a dummy central value, so stage A never uses an observed line width or dynamical mass.
  B  D_obs, residuals r_L, positions z_L, verdicts, gates G1-G5, pooled bins.
Reused rows read the committed points/README numbers of CFG220, CFG228, CFG271, CFG273, CFG276, CFG277 (CFG229 and CFG272 have no z >= 4 row).
Census rows (z >~ 8 and the z 6-8 / 4-6 papers found by the census) are typed in CENSUS below with their sources; see SCOPING.md.

Run:   python3 cfg269_discriminate.py            -> cfg269_discriminate.out, cfg269_results.json, cfg269_rows.csv
       MUTATE=1 python3 cfg269_discriminate.py   -> *_MUTATE.* (every line width x 1.7, every D x 2.89)
"""
import os, sys, io, csv, json, math, hashlib, contextlib
import numpy as np
from scipy.optimize import brentq

LANE = os.path.dirname(os.path.abspath(__file__))
CFG = os.path.dirname(LANE)
REPO = os.path.dirname(CFG)
MUT = os.environ.get("MUTATE", "").strip() == "1"
SFX = "_MUTATE" if MUT else ""
MUTF = 1.7 ** 2 if MUT else 1.0                      # factor on D (= on M_dyn) under MUTATE
sys.path.insert(0, os.path.join(REPO, "sonnet55_push", "puzzle_32pi", "agents", "Z1_causal_horizon_a0z"))
with contextlib.redirect_stdout(io.StringIO()):
    import zcommon as Z1                              # CFG222's PROXY (lcdm_native), read-only

OUT = []


def P(s=""):
    print(s, flush=True)
    OUT.append(s)


CHK = {}


def check(name, ok, val=""):
    CHK[name] = bool(ok)
    P(f"  [{'PASS' if ok else 'FAIL'}] {name}: {val}")


# ------------------------------------------------------------------ constants, laws, kernels
A0 = {"canonical": 9.3603e-11, "alt": 1.1312e-10}
G_SI, MSUN, KPC = 6.674e-11, 1.989e30, 3.0857e19
C_IN, C_OUT = 0.15, 0.30                              # calibration band half-widths (dex): primary, gate G1
SIG_K = 0.15                                          # lognormal scatter on the estimator coefficient (factor 2 = 2 sigma)
NMC, SEED = 20000, 269


def E(z, om=0.3):
    return math.sqrt(om * (1 + z) ** 3 + 1 - om)


sys.path.insert(0, CFG)
with contextlib.redirect_stdout(io.StringIO()):
    import CFG4_common as K4                          # the record's kernels, read-only (Addendum 1 of the criteria)
nu_mono = K4.nu_mono                                  # FP1's committed monotone repair of nu_RAR (the 09-26 kernel)


def nu_p2(y):
    y = np.maximum(np.asarray(y, float), 1e-300)
    return np.sqrt(1.0 + 1.0 / y)


def nu_rar(y):                                        # reported-only cell (Addendum 1)
    y = np.maximum(np.asarray(y, float), 1e-300)
    return 1.0 / (1.0 - np.exp(-np.sqrt(y)))


KER = {"nu_mono": nu_mono, "P2": nu_p2, "nu_RAR": nu_rar}
CELLS = [("nu_mono", "canonical"), ("nu_mono", "alt"), ("P2", "canonical"), ("P2", "alt")]
REPORT_CELLS = CELLS + [("nu_RAR", "canonical")]
PRIMARY = ("nu_mono", "canonical")


def proxy(z):
    return Z1.lcdm_native(z)


def beta(y, ker):
    """-dlog nu/dlog y at y (numerical)."""
    h = 1e-4
    f = KER[ker]
    return -(math.log(float(f(y * (1 + h)))) - math.log(float(f(y * (1 - h))))) / (math.log(1 + h) - math.log(1 - h))


def r_shift(logD, y, Ez, ker, x):
    """residual of law with factor Ez after a common baryon shift x (dex): log D - x - log nu(10^x y / Ez)."""
    return logD - x - math.log10(float(KER[ker](10 ** x * y / Ez)))


def x_star(logD, y, Ez, ker):
    f = lambda x: r_shift(logD, y, Ez, ker, x)
    return brentq(f, -6.0, 6.0)


# ------------------------------------------------------------------ the criteria file must exist (written before stage B)
CRIT = os.path.join(LANE, "FROZEN_CRITERIA.md")
if not os.path.exists(CRIT):
    sys.exit("FROZEN_CRITERIA.md missing: stage B refuses to run")
CRIT_SHA = hashlib.sha256(open(CRIT, "rb").read()).hexdigest()

P("CFG269 -- FLAT vs RIVAL a0(z) discrimination pre-flight, z >= 4 to ~14%s" % ("   [MUTATE=1: line widths x 1.7, D x 2.89]" if MUT else ""))
P("kappa = 1/2 FITTED. A discrimination between two a0(z) laws under declared estimators; NOT an a0 measurement. LambdaCDM: PROXY only.")
P(f"criteria FROZEN_CRITERIA.md sha256 {CRIT_SHA}")
P("")

# ------------------------------------------------------------------ controls on the machinery
P("CONTROLS ON THE MACHINERY")
check("C3 nu_mono(1) = 1.581977, P2(1) = sqrt 2", abs(float(nu_mono(1.0)) - 1.581977) < 1e-6 and abs(float(nu_p2(1.0)) - math.sqrt(2)) < 1e-12,
      f"{float(nu_mono(1.0)):.6f}, {float(nu_p2(1.0)):.6f}")
check("C4 E(14) = 31.8308 (Om 0.3)", abs(E(14) - 31.8308) < 1e-4, f"{E(14):.4f}")
pv = [proxy(z) for z in (1, 2, 2.5, 4.5, 5.5)]
check("C5 PROXY reproduces CFG222 (1.23, 1.77, 2.16, 4.52, 6.20)", all(abs(a - b) < 0.006 for a, b in zip(pv, (1.23, 1.77, 2.16, 4.52, 6.20))),
      ", ".join(f"{v:.3f}" for v in pv))
P("")

# ------------------------------------------------------------------ reused rows
ROWS = []          # every scored row (dicts)


def add_reused(lane, obj, z, y, D, cls, sig_lo, sig_hi, role, pool_key, notes, cal=None, branch=None, sigma_kind="68% interval of delta_FLAT"):
    """sig_lo / sig_hi: committed log-D widths below / above the committed D.  cal: optional dict {'in': S_in, 'out': S_out} on delta_FLAT (CFG228)."""
    ROWS.append(dict(src="reused", lane=lane, obj=obj, z=float(z), y=float(y), D=float(D) * MUTF, D_committed=float(D), cls=cls, sig_lo=float(sig_lo),
                     sig_hi=float(sig_hi), role=role, pool_key=pool_key, notes=notes, cal=cal, branch=branch, sigma_kind=sigma_kind))


def floats(r, *keys):
    return [float(r[k]) for k in keys]


# --- HZQ lanes (CFG271/273/276/277): committed D, y, delta_FLAT and its 68% interval; C1 recomputes delta_FLAT
C1_dev = []
C1_single = []
HZQ = {"CFG271": "CFG271_hz9_three_rings/cfg271_points_stageB.csv", "CFG273": "CFG273_danhaive_gold41/cfg273_points_stageB.csv",
       "CFG276": "CFG276_gn20/cfg276_points_stageB.csv", "CFG277": "CFG277_roman_oliveira_four_discs/cfg277_points_stageB.csv"}
for lane, rel in HZQ.items():
    for r in csv.DictReader(open(os.path.join(CFG, rel))):
        if r["y"] in ("", "nan") or r["D"] in ("", "nan") or float(r["z"]) < 4.0:
            continue
        if "pooled" in r["object"].lower():
            continue
        z, y, D, dF, lo, hi = floats(r, "z", "y", "D", "delta_FLAT", "delta_FLAT_lo68", "delta_FLAT_hi68")
        C1_dev.append(abs(math.log10(D / float(nu_mono(y))) - dF))
        gc = r["gas_class"]
        if lane == "CFG271":
            cls, branch = "LOWER-LIMIT", r["object"].split("[")[1].split("]")[0].split(";")[0]
            role = r["role"]
            key = "HZ9" if role == "headline" else None
            note = "stars only (two M* branches M986 / M103, never pooled); beam-limited; rotation interpretation weak (CFG271)"
        elif lane == "CFG273":
            cls, branch, role, key = "LOWER-LIMIT", None, "headline", r["object"]
            note = "stars only; authors' M_dyn (Danhaive+25)" + ("; sigma0 UPPER LIMIT (M_dyn at face value)" if r.get("sigma0_limit", "0") == "1" else "") + \
                   ("; CRISTAL-08 z-candidate" if r.get("cristal08_candidate", "0") == "1" else "")
        elif lane == "CFG276":
            br = r["branch"]
            cls = "COMPLETE" if br in ("stars+H12", "stars+RT") else "LOWER-LIMIT"
            rec = "RECOMMENDED" in r["quality"]
            role = "recommended" if rec else r["role"]
            key = "GN20" if rec else None
            branch = f"{br}; {r['radius']}"
            note = "GN20; g_obs a DysmalPy model output; " + ("RECOMMENDED CHART ROW (frozen rule of CFG276)" if rec else r["role"])
        else:  # CFG277
            obj = r["object"]
            complete = "+M*" in obj
            cls = "COMPLETE" if complete else "LOWER-LIMIT"
            role = r["role"]
            name = obj.split(" [")[0]
            branch = obj.split("[")[1].rstrip("]")
            if role == "headline":
                key = name if (complete or name != "J081740") else None      # J081740: the more complete [gas+M*] row is pooled
            else:
                key = None
            note = gc + ("; corpus M* (source unrecorded in CFG277)" if complete else "; stars missing (gas only)") + ("; QUASAR HOST" if "quasar" in gc else "")
        multi = "/" in r.get("R_kpc", "")
        if multi:
            note += "; MULTI-RADIUS SET (R = %s kpc): the committed (D, y) are not one point and delta_FLAT is the set median; position not interpretable" % r["R_kpc"]
        add_reused(lane, r["object"], z, y, D, cls, dF - lo, hi - dF, role, key, note, branch=branch)
        ROWS[-1]["multi"] = multi
        if not multi:
            C1_single.append(C1_dev[-1])
check("C1 HZQ rows: delta_FLAT recomputed from committed (D, y) equals the committed value (<= 1e-4)", max(C1_dev) <= 1e-4,
      f"{len(C1_dev)} rows, max |dev| {max(C1_dev):.2e}")
P(f"  POST HOC (labelled; not a frozen check): the deviations come only from the two CFG271 multi-radius sensitivity rows; single-radius rows: {len(C1_single)}, max |dev| {max(C1_single):.2e}")

# --- CFG228 (six ALPINE rotators + SPT0418-47): committed D, y, dFLAT, dHz (Om 0.315), per-galaxy SD and S_inner / S_outer
pf = json.load(open(os.path.join(CFG, "CFG228_alma_cubes", "cfg228_preflight_results.json")))
c228 = []
for r in csv.DictReader(open(os.path.join(CFG, "CFG228_alma_cubes", "cfg228_points.csv"))):
    z, y, D, dF, dH = floats(r, "z", "y", "D", "dFLAT", "dHz")
    c228.append(max(abs(math.log10(D / float(nu_mono(y))) - dF), abs(math.log10(D / float(nu_mono(y / E(z, 0.315)))) - dH)))
    g = r["gid"]
    sd = pf["PG"][g]["sd"]
    S = pf["RES"][g]["S"]
    dup = g == "DC494057"
    add_reused("CFG228", g, z, y, D, "COMPLETE", sd, sd, "headline", None if dup else g,
               f"gas class {r['gas_class']}; " + ("DUPLICATE of CRISTAL-20 (HZ4): not pooled, CFG220 row used" if dup else "ALPINE [CII] rotator" if g != "SPT0418-47" else "lensed [CII] disc (Rizzo+20 curve)"),
               cal={"in": S["inner"], "out": S["outer"]}, sigma_kind="committed per-galaxy SD of delta_FLAT (mocks)")
check("C1b CFG228: dFLAT and dHz (Om 0.315) recomputed from committed (D, y) (<= 1e-4)", max(c228) <= 1e-4, f"max |dev| {max(c228):.2e}")

# --- CFG220 (CRISTAL, independent route, table R_out): committed per-disc block of cfg220_outer_independent.out
c220 = []
for line in open(os.path.join(CFG, "CFG220_cristal_outer_independent", "cfg220_outer_independent.out")):
    s = line.split()
    if len(s) > 10 and s[1] == "z" and "D_ind" in line and "delta_flat" in line:
        did, z = s[0], float(s[2])
        y = float(s[line.split().index("g_bar/A0") + 1]) if "g_bar/A0" in s else float("nan")
        D = float(s[s.index("D_ind") + 1])
        dfl = float(s[s.index("delta_flat") + 1])
        drv = float(s[s.index("delta_rival") + 1])
        c220.append(max(abs(math.log10(D / float(nu_mono(y))) - dfl), abs(math.log10(D / float(nu_mono(y / E(z, 0.315)))) - drv)))
        add_reused("CFG220", f"CRISTAL-{did}", z, y, D, "COMPLETE", 0.25, 0.25, "headline", f"CRISTAL-{did}",
                   "CRISTAL independent route (SED M* + dust gas), table R_out; sigma 0.25 = CFG220's realised per-disc scatter" + ("; = HZ4 = DC494057" if did == "20" else ""),
                   sigma_kind="CFG220 realised per-disc scatter 0.25 dex")
check("C2 CFG220 per-disc delta_flat / delta_rival (Om 0.315) reproduced from the printed D_ind and g_bar/A0 (<= 0.006)", len(c220) == 6 and max(c220) <= 0.006,
      f"{len(c220)} discs, max |dev| {max(c220):.4f}")
P("  CFG229: no row at z >= 4 (all seven class-M rows are z 2.0-2.9).  CFG272: no row at z >= 4 (ALPAKA rows z 2.10-3.63).")
P("")

# ------------------------------------------------------------------ census rows (typed from the papers; sources in SCOPING.md)
# kin = ("sigma", value, +err, -err, K)      : M_dyn,tot = K sigma^2 r / G ; enclosed = half
#       ("mdyn", log10, +err, -err, kind)    : kind 'total' (enclosed = half) or 'enclosed'
#       ("vrot", value, +err, -err, i_deg, +ei, -ei) : M_dyn(<r) = (V/sin i)^2 r / G
# mstar = (log10, +err, -err); gas = None or (log10, +err, -err); r = (kpc, +err, -err)
CENSUS = []
try:
    from cfg269_census_inputs import CENSUS as _C
    CENSUS = list(_C)
except ImportError:
    P("  (no census input file found: census rows skipped)")


def sn(rng, v, ehi, elo, n):
    g = rng.normal(size=n)
    return v + np.where(g > 0, g * ehi, g * elo)


def census_draws(row, kfac=1.0, kscatter=True, zero=False, dummy=False, n=NMC):
    """returns arrays (logD, y_canonical) for one census row.  zero: no errors (C7).  dummy: stage-A blind (central kinematic value replaced by a
    dummy, fractional errors kept)."""
    rng = np.random.default_rng(SEED + sum(map(ord, row["id"])))
    nn = 1 if zero else n
    e = 0.0 if zero else 1.0
    lm, lmp, lmm = row["mstar"]
    Ms = 10 ** sn(rng, lm, e * lmp, e * lmm, nn)
    Mg, fg = 0.0, 0.5
    if row.get("gas") is not None:
        lg, lgp, lgm = row["gas"][:3]
        fg = row["gas"][3] if len(row["gas"]) > 3 else 0.5
        Mg = 10 ** sn(rng, lg, e * lgp, e * lgm, nn)
    fs = row.get("fenc_star", 0.5)
    Mb_in = fs * Ms + fg * Mg                                  # baryons enclosed within r (half-light = half-mass unless declared)
    rk, rp, rm = row["r"]
    r = np.maximum(sn(rng, rk, e * rp, e * rm, nn), 0.01 * rk)
    kin = row["kin"]
    ks = 10 ** (rng.normal(0, SIG_K, nn)) if (kscatter and not zero) else 1.0
    if kin[0] == "sigma":
        v, vp, vm, K = kin[1:5]
        if dummy:
            v, vp, vm = 100.0, 100.0 * vp / v, 100.0 * vm / v
        sg = np.maximum(sn(rng, v * math.sqrt(MUTF), e * vp * math.sqrt(MUTF), e * vm * math.sqrt(MUTF), nn), 1.0)
        Mdyn_in = 0.5 * K * kfac * ks * (sg * 1e3) ** 2 * (r * KPC) / G_SI / MSUN
    elif kin[0] == "mdyn":
        lmd, lmdp, lmdm, kind = kin[1:5]
        if dummy:
            lmd = 10.0
        Md = 10 ** sn(rng, lmd, e * lmdp, e * lmdm, nn) * MUTF * kfac * ks
        Mdyn_in = Md * (0.5 if kind == "total" else 1.0)
    else:
        v, vp, vm, inc, ip, im = kin[1:7]
        if dummy:
            v, vp, vm = 100.0, 100.0 * vp / v, 100.0 * vm / v
        vv = np.maximum(sn(rng, v * math.sqrt(MUTF), e * vp * math.sqrt(MUTF), e * vm * math.sqrt(MUTF), nn), 1.0)
        ii = np.clip(sn(rng, inc, e * ip, e * im, nn), 5.0, 90.0)
        Mdyn_in = kfac * ks * (vv * 1e3 / np.sin(np.radians(ii))) ** 2 * (r * KPC) / G_SI / MSUN
    D = Mdyn_in / Mb_in
    gbar = G_SI * Mb_in * MSUN / (r * KPC) ** 2
    return np.log10(D), gbar / A0["canonical"]


# ------------------------------------------------------------------ per-row evaluation
def evaluate(row, cell, c, stageA=False, kfac=1.0, kscatter=True):
    """returns a dict with the predictions and (unless stageA) the residuals, sigmas, z, P for one row in one cell at calibration c."""
    ker, foot = cell
    z = row["z"]
    EzR, EzP = E(z), proxy(z)
    if row["src"] == "reused":
        y0 = row["y"] * A0["canonical"] / A0[foot]
        logD = math.log10(row["D"])
        lsig_lo, lsig_hi = row["sig_lo"], row["sig_hi"]
        mc = None
    else:
        lD, yc = census_draws(row, kfac=kfac, kscatter=kscatter, dummy=stageA)
        lD0, yc0 = census_draws(row, kfac=kfac, kscatter=False, zero=True, dummy=stageA)
        y0 = float(yc0[0]) * A0["canonical"] / A0[foot]
        logD = float(lD0[0])
        mc = (lD, yc * A0["canonical"] / A0[foot])
    dF, dR = float(KER[ker](y0)), float(KER[ker](y0 / EzR))
    G = math.log10(dR / dF)
    out = dict(y=y0, DpredF=dF, DpredR=dR, DpredP=float(KER[ker](y0 / EzP)), G=G, EzR=EzR, EzP=EzP)
    res, sig = {}, {}
    for L, Ez in (("F", 1.0), ("R", EzR), ("P", EzP)):
        rL = r_shift(logD, y0, Ez, ker, 0.0)
        if row["src"] == "reused":
            s_st = lsig_lo if rL > 0 else lsig_hi          # side facing the prediction (for z_L)
            s_sym = 0.5 * (lsig_lo + lsig_hi)               # symmetric (for P and pooling weights: independent of the central D)
        else:
            draws = mc[0] - np.log10(KER[ker](mc[1] / Ez))
            p16, p84 = np.percentile(draws, [16, 84])
            s_st = (rL - p16) if rL > 0 else (p84 - rL)
            s_sym = 0.5 * (p84 - p16)
            if stageA:
                s_st = s_sym
        if row.get("cal") is not None:
            S = row["cal"]["in" if c == C_IN else "out"]
            bF = beta(y0, ker)
            bL = beta(y0 / Ez, ker)
            s_cal = S * (1 - bL) / (1 - bF)
        else:
            s_cal = abs(r_shift(logD, y0, Ez, ker, +c) - r_shift(logD, y0, Ez, ker, -c)) / 2.0
        tot = math.sqrt(s_st ** 2 + s_cal ** 2)
        res[L] = rL
        sig[L] = dict(stat=s_st, stat_sym=s_sym, cal=s_cal, tot=tot, tot_sym=math.sqrt(s_sym ** 2 + s_cal ** 2))
    out["P"] = G / max(sig["F"]["tot_sym"], sig["R"]["tot_sym"])     # criteria section 2: P does not depend on the central D
    out["sig"] = sig
    if not stageA:
        out["r"] = res
        out["z"] = {L: res[L] / sig[L]["tot"] for L in res}
        out["xstar"] = {L: x_star(logD, y0, Ez, ker) for L, Ez in (("F", 1.0), ("R", EzR))}
        out["logD"] = logD
        out["D"] = 10 ** logD
        # dominant term of max(sigma_F, sigma_R)
        Lm = "F" if sig["F"]["tot"] >= sig["R"]["tot"] else "R"
        out["dominant"] = "calibration (baryon shift)" if sig[Lm]["cal"] > sig[Lm]["stat"] else ("statistical/estimator" if row["src"] == "census" else "statistical (committed)")
    return out


def verdict_P(Pv):
    return "SEPARATES" if Pv >= 2 else ("MARGINAL" if Pv >= 1 else "NOT POSSIBLE")


def statement(ev):
    zF, zR = abs(ev["z"]["F"]), abs(ev["z"]["R"])
    if zR >= 2 and zF < 2:
        return "RIVAL DISFAVOURED"
    if zF >= 2 and zR < 2:
        return "FLAT DISFAVOURED"
    if zF >= 2 and zR >= 2:
        return "BOTH DISFAVOURED"
    return "BETWEEN"


def position(ev):
    return "closer to FLAT" if abs(ev["z"]["F"]) < abs(ev["z"]["R"]) else "closer to RIVAL"


# ------------------------------------------------------------------ stage A (predictions only)
P("STAGE A -- predictions only (no observed D used): y, D_pred, gap G, power P (primary cell nu_mono / canonical, c = 0.15)")
P(f"  {'lane':7s} {'object':34s} {'z':>6s} {'E(z)':>6s} {'PROXY':>6s} {'y':>8s} {'D_F':>6s} {'D_R':>6s} {'G':>6s} {'P':>5s} verdict")
for row in sorted(ROWS + [dict(src="census", **c) for c in CENSUS], key=lambda r: -r["z"]):
    if row["src"] == "census":
        row.setdefault("lane", "CFG269")
        row.setdefault("obj", row["id"])
        row.setdefault("pool_key", row["id"])
    ev = evaluate(row, PRIMARY, C_IN, stageA=True)
    row["stageA"] = dict(y=ev["y"], DpredF=ev["DpredF"], DpredR=ev["DpredR"], G=ev["G"], P=ev["P"], verdict=verdict_P(ev["P"]))
    P(f"  {row['lane']:7s} {row['obj'][:34]:34s} {row['z']:6.2f} {ev['EzR']:6.2f} {ev['EzP']:6.2f} {ev['y']:8.3f} {ev['DpredF']:6.3f} {ev['DpredR']:6.3f} {ev['G']:6.3f} {ev['P']:5.2f} {verdict_P(ev['P'])}")
    if row["src"] == "census" and row not in ROWS:
        ROWS.append(row)
P("")

# ------------------------------------------------------------------ C7: census MC with zero errors equals the closed form
c7 = []
for row in [r for r in ROWS if r["src"] == "census"]:
    lD, yc = census_draws(row, kscatter=False, zero=True)
    lm = row["mstar"][0]
    Mb_in = row.get("fenc_star", 0.5) * 10 ** lm + ((row["gas"][3] if len(row["gas"]) > 3 else 0.5) * 10 ** row["gas"][0] if row.get("gas") else 0.0)
    rk = row["r"][0]
    kin = row["kin"]
    if kin[0] == "sigma":
        Md = 0.5 * kin[4] * (kin[1] * math.sqrt(MUTF) * 1e3) ** 2 * rk * KPC / G_SI / MSUN
    elif kin[0] == "mdyn":
        Md = 10 ** kin[1] * MUTF * (0.5 if kin[4] == "total" else 1.0)
    else:
        Md = (kin[1] * math.sqrt(MUTF) * 1e3 / math.sin(math.radians(kin[4]))) ** 2 * rk * KPC / G_SI / MSUN
    cf = math.log10(Md / Mb_in)
    yy = G_SI * Mb_in * MSUN / (rk * KPC) ** 2 / A0["canonical"]
    c7.append(max(abs(cf - float(lD[0])), abs(yy / float(yc[0]) - 1)))
if c7:
    check("C7 census MC with zero errors returns the closed-form D_obs and y", max(c7) < 1e-9, f"{len(c7)} rows, max dev {max(c7):.1e}")

# ------------------------------------------------------------------ C8: paper M_dyn against the recomputation from sigma (flag only)
P("C8 (flag only): paper M_dyn vs K sigma^2 r / G recomputed with the paper's K")
for row in [r for r in ROWS if r["src"] == "census" and r.get("c8")]:
    K, sg, rk, lpaper, kind = row["c8"]
    Mrec = K * (sg * 1e3) ** 2 * rk * KPC / G_SI / MSUN
    dv = math.log10(Mrec) - lpaper
    row["c8_dev"] = dv
    P(f"  {row['obj']:30s} recomputed log M {math.log10(Mrec):.2f} vs paper {lpaper:.2f} ({kind}): {dv:+.2f} dex {'FLAG (> 0.1 dex)' if abs(dv) > 0.1 else 'ok'}")
P("")

# ------------------------------------------------------------------ stage B
P("STAGE B -- observed D, residuals and positions (primary cell nu_mono / canonical, c = 0.15; census rows at the paper's K with 0.15 dex scatter)")
P(f"  {'lane':7s} {'object':34s} {'z':>6s} {'cls':5s} {'D_obs':>7s} {'r_F':>7s} {'r_R':>7s} {'sF':>5s} {'sR':>5s} {'z_F':>6s} {'z_R':>6s} {'P':>5s} {'verdict':12s} {'position':16s} statement / labels")
for row in sorted(ROWS, key=lambda r: -r["z"]):
    evs = {cell: {c: evaluate(row, cell, c) for c in (C_IN, C_OUT)} for cell in REPORT_CELLS}
    ev = evs[PRIMARY][C_IN]
    row["ev"] = ev
    row["verdict"] = verdict_P(ev["P"])
    row["position"] = position(ev)
    row["statement"] = statement(ev) if row["verdict"] == "SEPARATES" else "-"
    labels = []
    if row["src"] == "census":
        if row.get("role") == "sensitivity":
            labels.append("sensitivity row (not pooled)")
        fl = row.get("flags", "")
        if fl and not fl.startswith("none"):
            labels.append("FLAG: " + fl)
    if row.get("multi"):
        labels.append("MULTI-RADIUS SET: (D, y) not one point; position NOT interpretable (sensitivity row, never pooled)")
    floor = ev["D"] < 1.0
    row["floor"] = floor
    if floor:
        restored = (r_shift(ev["logD"], ev["y"], ev["EzR"], "nu_mono", -C_OUT) >= 0) or \
                   abs(r_shift(ev["logD"], ev["y"], ev["EzR"], "nu_mono", -C_OUT) / ev["sig"]["R"]["tot"]) < 2
        row["floor_restored_by_outer_band"] = bool(restored)
        labels.append("FLOOR (" + ("the outer band restores the rival: the floor does not discriminate" if restored else "outer band does NOT restore the rival; still never counted") + ")")
    # gates
    g = {}
    g["G1"] = verdict_P(evs[PRIMARY][C_OUT]["P"]) == "SEPARATES" and statement(evs[PRIMARY][C_OUT]) == row["statement"] if row["verdict"] == "SEPARATES" else None
    g["G2"] = all(verdict_P(evs[cl][C_IN]["P"]) == "SEPARATES" and statement(evs[cl][C_IN]) == row["statement"] for cl in CELLS) if row["verdict"] == "SEPARATES" else None
    if row["src"] == "census":
        ks = {}
        for kf in (0.5, 2.0):
            e2 = evaluate(row, PRIMARY, C_IN, kfac=kf, kscatter=False)
            ks[kf] = dict(P=e2["P"], verdict=verdict_P(e2["P"]), statement=statement(e2) if verdict_P(e2["P"]) == "SEPARATES" else "-", position=position(e2),
                          zF=e2["z"]["F"], zR=e2["z"]["R"], D=e2["D"])
        row["K_bracket"] = ks
        g["G3"] = all(ks[k]["statement"] == row["statement"] for k in ks) if row["verdict"] == "SEPARATES" else None
    if row["cls"] == "LOWER-LIMIT":
        gl = []
        for L in ("F", "R"):
            if ev["r"][L] > 0:
                gl.append(L)
        row["gas_limited_laws"] = gl
        if row["statement"] in ("RIVAL DISFAVOURED", "FLAT DISFAVOURED", "BOTH DISFAVOURED"):
            hit = {"RIVAL DISFAVOURED": ["R"], "FLAT DISFAVOURED": ["F"], "BOTH DISFAVOURED": ["F", "R"]}[row["statement"]]
            g["G4"] = all(ev["r"][L] < 0 for L in hit)
        labels.append("LOWER-LIMIT baryons: " + ("GAS-LIMITED for " + "/".join({"F": "FLAT", "R": "RIVAL"}[L] for L in gl) if gl else "both laws over-predict (r < 0): robust to missing baryons"))
    if floor:
        g["G5"] = False
    row["gates"] = g
    applicable = [v for v in g.values() if v is not None]
    row["robust"] = bool(row["statement"] not in ("-", "BETWEEN") and applicable and all(applicable) and not floor)
    row["labels"] = labels
    row["cells"] = {f"{k}|{f}": {str(c): dict(P=evs[(k, f)][c]["P"], zF=evs[(k, f)][c]["z"]["F"], zR=evs[(k, f)][c]["z"]["R"], rF=evs[(k, f)][c]["r"]["F"],
                                             rR=evs[(k, f)][c]["r"]["R"], verdict=verdict_P(evs[(k, f)][c]["P"])) for c in (C_IN, C_OUT)} for (k, f) in REPORT_CELLS}
    gs = " ".join(f"{k}:{'-' if v is None else ('pass' if v else 'FAIL')}" for k, v in g.items())
    P(f"  {row['lane']:7s} {row['obj'][:34]:34s} {row['z']:6.2f} {row['cls'][:5]:5s} {ev['D']:7.3f} {ev['r']['F']:+7.3f} {ev['r']['R']:+7.3f} {ev['sig']['F']['tot']:5.2f} {ev['sig']['R']['tot']:5.2f} "
      f"{ev['z']['F']:+6.2f} {ev['z']['R']:+6.2f} {ev['P']:5.2f} {row['verdict']:12s} {row['position']:16s} {row['statement']} {gs} {'ROBUST' if row['robust'] else ''} {'; '.join(labels)}")
P("")

# ------------------------------------------------------------------ census detail: K bracket, x*, proxy, dominant term
P("CENSUS DETAIL (paper's K; K/2; 2K) and every row's baryon shifts x*_F, x*_R that zero each law's residual (dex), PROXY residual, dominant term")
for row in sorted(ROWS, key=lambda r: -r["z"]):
    ev = row["ev"]
    extra = ""
    if row["src"] == "census":
        kb = row["K_bracket"]
        extra = f" | K/2: D {kb[0.5]['D']:.2f} z_F {kb[0.5]['zF']:+.2f} z_R {kb[0.5]['zR']:+.2f} {kb[0.5]['verdict']} | 2K: D {kb[2.0]['D']:.2f} z_F {kb[2.0]['zF']:+.2f} z_R {kb[2.0]['zR']:+.2f} {kb[2.0]['verdict']}"
    P(f"  {row['obj'][:34]:34s} z {row['z']:5.2f}  x*_F {ev['xstar']['F']:+.2f}  x*_R {ev['xstar']['R']:+.2f}  r_PROXY {ev['r']['P']:+.3f}  dominant: {ev['dominant']}{extra}")
P("")

# ------------------------------------------------------------------ pooled bins
BINS = [("B1 4<=z<6", 4.0, 6.0), ("B2 6<=z<8", 6.0, 8.0), ("B3 8<=z<=15", 8.0, 15.1)]


def pool(rows, cell, c):
    if not rows:
        return None
    evs = [evaluate(r, cell, c) for r in rows]
    w = np.array([1.0 / max(e["sig"]["F"]["stat_sym"], e["sig"]["R"]["stat_sym"]) ** 2 for e in evs])
    out = {}
    for L in ("F", "R", "P"):
        rl = np.array([e["r"][L] for e in evs])
        sc = float(np.mean([e["sig"][L]["cal"] for e in evs]))
        rb = float(np.sum(w * rl) / np.sum(w))
        sp = math.sqrt(1.0 / np.sum(w) + sc ** 2)
        out[L] = dict(rbar=rb, sig=sp, z=rb / sp, median=float(np.median(rl)), cal=sc, stat=math.sqrt(1.0 / np.sum(w)))
    Gw = float(np.sum(w * np.array([e["G"] for e in evs])) / np.sum(w))
    Pb = Gw / max(out["F"]["sig"], out["R"]["sig"])
    zF, zR = abs(out["F"]["z"]), abs(out["R"]["z"])
    st = ("RIVAL DISFAVOURED" if zR >= 2 and zF < 2 else "FLAT DISFAVOURED" if zF >= 2 and zR < 2 else "BOTH DISFAVOURED" if zF >= 2 and zR >= 2 else "BETWEEN")
    return dict(n=len(rows), G=Gw, P=Pb, verdict=verdict_P(Pb), statement=st if verdict_P(Pb) == "SEPARATES" else "-", pos=("closer to FLAT" if zF < zR else "closer to RIVAL"),
                F=out["F"], R=out["R"], PROXY=out["P"], members=[r["obj"] for r in rows],
                dominant="calibration (common-mode)" if max(out["F"]["cal"], out["R"]["cal"]) > max(out["F"]["stat"], out["R"]["stat"]) else "statistical")


POOLS = {}
P("POOLED BINS (one row per object; COMPLETE and LOWER-LIMIT never pooled together; calibration common-mode, does not average down)")
for bname, z0, z1 in BINS:
    inbin = [r for r in ROWS if z0 <= r["z"] < z1 and r.get("pool_key")]
    # census rows: pool key = id (one row per object)
    for r in inbin:
        pass
    for cls in ("COMPLETE", "LOWER-LIMIT"):
        sel = [r for r in inbin if r["cls"] == cls]
        # branch variants: objects with >1 pooled row (two equally complete branches) -> one variant per branch
        keys = {}
        for r in sel:
            keys.setdefault(r["pool_key"], []).append(r)
        multi = [k for k, v in keys.items() if len(v) > 1]
        variants = {}
        import itertools
        for combo in itertools.product(*[range(len(keys[k])) for k in multi]):
            pick = dict(zip(multi, combo))
            name = "main" if not multi else "+".join(f"{k}:{keys[k][pick[k]].get('branch')}" for k in multi)
            variants[name] = [v[pick.get(k, 0)] for k, v in keys.items()]
        for vname, members in variants.items():
            for floors in ("with floors", "floors excluded"):
                mem = members if floors == "with floors" else [m for m in members if not m["floor"]]
                res = {}
                for cell in CELLS:
                    for c in (C_IN, C_OUT):
                        res[f"{cell[0]}|{cell[1]}|{c}"] = pool(mem, cell, c)
                pr = res[f"nu_mono|canonical|{C_IN}"]
                POOLS[f"{bname}|{cls}|{vname}|{floors}"] = res
                if pr is None:
                    P(f"  {bname:13s} {cls:11s} {vname[:60]:60s} {floors:16s} n = 0")
                    continue
                g1 = res[f"nu_mono|canonical|{C_OUT}"]
                g2 = all(res[f"{k}|{f}|{C_IN}"]["verdict"] == pr["verdict"] and res[f"{k}|{f}|{C_IN}"]["statement"] == pr["statement"] for k, f in CELLS)
                g4 = ""
                if cls == "LOWER-LIMIT" and pr["statement"] in ("RIVAL DISFAVOURED", "FLAT DISFAVOURED", "BOTH DISFAVOURED"):
                    hit = {"RIVAL DISFAVOURED": ["R"], "FLAT DISFAVOURED": ["F"], "BOTH DISFAVOURED": ["F", "R"]}[pr["statement"]]
                    g4 = " G4 " + ("pass (the disfavoured law over-predicts: robust to missing baryons)" if all(pr[L]["rbar"] < 0 for L in hit) else "FAIL: GAS-LIMITED (r > 0; missing gas can remove it)")
                pr["G1"] = dict(P=g1["P"], verdict=g1["verdict"], statement=g1["statement"])
                pr["G2"] = g2
                pr["G4"] = g4.strip()
                P(f"  {bname:13s} {cls:11s} {vname[:60]:60s} {floors:16s} n = {pr['n']:2d}  G {pr['G']:.3f}  rbar_F {pr['F']['rbar']:+.3f} (sd {pr['F']['sig']:.3f}, z {pr['F']['z']:+.2f})  "
                  f"rbar_R {pr['R']['rbar']:+.3f} (sd {pr['R']['sig']:.3f}, z {pr['R']['z']:+.2f})  P {pr['P']:.2f} {pr['verdict']:12s} {pr['pos']:16s} {pr['statement']:18s} "
                  f"| c=0.30: P {g1['P']:.2f} {g1['verdict']} {g1['statement']} | G2 four cells same: {g2}{g4} | median r_F {pr['F']['median']:+.3f} r_R {pr['R']['median']:+.3f} | r_PROXY {pr['PROXY']['rbar']:+.3f} | dominant {pr['dominant']}")
P("BIN VERDICTS (frozen rule, section 5: the COMPLETE pool decides; every branch variant, floors included and excluded, must agree; G1 = c 0.30)")
BINV = {}
for bname, z0, z1 in BINS:
    for cls in ("COMPLETE", "LOWER-LIMIT"):
        ks = [k for k in POOLS if k.startswith(f"{bname}|{cls}|")]
        prs = [POOLS[k][f"nu_mono|canonical|{C_IN}"] for k in ks if POOLS[k][f"nu_mono|canonical|{C_IN}"] is not None]
        if not prs:
            BINV[f"{bname}|{cls}"] = dict(n=0, verdict="NO ROWS")
            P(f"  {bname:13s} {cls:11s} no rows")
            continue
        g1s = [POOLS[k][f"nu_mono|canonical|{C_OUT}"] for k in ks if POOLS[k][f"nu_mono|canonical|{C_IN}"] is not None]
        verds = sorted(set(p["verdict"] for p in prs))
        stmts = sorted(set(p["statement"] for p in prs))
        g1v = sorted(set(p["verdict"] for p in g1s))
        g2 = all(p.get("G2", True) for p in prs)
        g4s = sorted(set(p.get("G4", "") for p in prs) - {""})
        agree = len(verds) == 1 and len(stmts) == 1
        robust = agree and stmts[0] not in ("-", "BETWEEN") and g1v == ["SEPARATES"] and g2 and not any("FAIL" in g for g in g4s)
        verdict = verds[0] if len(verds) == 1 else "VARIANT-DEPENDENT (" + " / ".join(verds) + ")"
        BINV[f"{bname}|{cls}"] = dict(n=max(p["n"] for p in prs), P_range=[min(p["P"] for p in prs), max(p["P"] for p in prs)], verdicts=verds, statements=stmts,
                                       G1_verdicts=g1v, G2_all=g2, G4=g4s, robust_statement=robust, verdict=verdict,
                                       zF_range=[min(p["F"]["z"] for p in prs), max(p["F"]["z"] for p in prs)], zR_range=[min(p["R"]["z"] for p in prs), max(p["R"]["z"] for p in prs)],
                                       dominant=sorted(set(p["dominant"] for p in prs)))
        P(f"  {bname:13s} {cls:11s} n <= {BINV[f'{bname}|{cls}']['n']:2d}  P {min(p['P'] for p in prs):.2f}-{max(p['P'] for p in prs):.2f}  verdict {verdict}  statements {stmts}  "
          f"z_F {BINV[f'{bname}|{cls}']['zF_range'][0]:+.2f}..{BINV[f'{bname}|{cls}']['zF_range'][1]:+.2f}  z_R {BINV[f'{bname}|{cls}']['zR_range'][0]:+.2f}..{BINV[f'{bname}|{cls}']['zR_range'][1]:+.2f}  "
          f"G1 {g1v}  G2 {g2}  {('G4 ' + '; '.join(g4s)) if g4s else ''}  ROBUST statement: {robust}  dominant {BINV[f'{bname}|{cls}']['dominant']}")
P("")
P("POST HOC (labelled; not in the frozen criteria): census rows carrying an AGN / merger / outflow flag removed, reused rows kept (BRI1335-0417, a quasar host, removed)")
FLAGWORDS = ("AGN", "merger", "outflow", "QUASAR")
for bname, z0, z1 in BINS:
    for cls in ("COMPLETE", "LOWER-LIMIT"):
        sel = [r for r in ROWS if z0 <= r["z"] < z1 and r.get("pool_key") and r["cls"] == cls and
               not (r.get("flagged", False) if r["src"] == "census" else "QUASAR" in r.get("notes", ""))]
        keys = {}
        for r in sel:
            keys.setdefault(r["pool_key"], []).append(r)
        for vname, members in ({"first branch": [v[0] for v in keys.values()], "last branch": [v[-1] for v in keys.values()]} if keys else {"-": []}).items():
            pr = pool(members, PRIMARY, C_IN)
            if pr is None:
                P(f"  {bname:13s} {cls:11s} n = 0")
                continue
            g1 = pool(members, PRIMARY, C_OUT)
            POOLS[f"POSTHOC-unflagged|{bname}|{cls}|{vname}"] = {"primary": pr, "c=0.30": g1}
            P(f"  {bname:13s} {cls:11s} {vname:12s} n = {pr['n']:2d}  G {pr['G']:.3f}  rbar_F {pr['F']['rbar']:+.3f} (z {pr['F']['z']:+.2f})  rbar_R {pr['R']['rbar']:+.3f} (z {pr['R']['z']:+.2f})  "
              f"P {pr['P']:.2f} {pr['verdict']:12s} {pr['pos']:16s} {pr['statement']} | c=0.30: P {g1['P']:.2f} {g1['verdict']} {g1['statement']} | members {', '.join(pr['members'])[:160]}")
P("")

# ------------------------------------------------------------------ C6 MUTATE expectations (the script checks the shift against the unmutated results file)
base_json = os.path.join(LANE, "cfg269_results.json")
if MUT and os.path.exists(base_json):
    B = json.load(open(base_json))
    target = math.log10(2.89)
    reused_sh, census_sh, dP = [], [], []
    for row in ROWS:
        b = B["rows"].get(f"{row['lane']}|{row['obj']}")
        if b is None:
            continue
        for L, k in (("F", "rF"), ("R", "rR")):
            (reused_sh if row["src"] == "reused" else census_sh).append(row["ev"]["r"][L] - b[k])
        if row["src"] == "reused":
            dP.append(abs(row["ev"]["P"] - b["P"]))
    okA = all(abs(s - target) < 1e-9 for s in reused_sh)
    okB = all(abs(s - target) < 0.01 for s in census_sh)
    okP = (max(dP) if dP else 0.0) < 1e-9
    moved = sum(1 for row in ROWS if f"{row['lane']}|{row['obj']}" in B["rows"] and position(row["ev"]) != B["rows"][f"{row['lane']}|{row['obj']}"]["position"])
    check("C6 MUTATE: every reused r_L shifts by log10(2.89) exactly, census within 0.01, reused P unchanged", okA and okB and okP,
          f"reused max |shift-0.4609| {max([abs(s - target) for s in reused_sh] + [0]):.1e}, census max {max([abs(s - target) for s in census_sh] + [0]):.3f}, max |dP| {max(dP) if dP else 0:.1e}; positions changed in {moved} rows")
    P("  MUTATE verdict moves (row: unmutated position -> mutated position, statement):")
    for row in sorted(ROWS, key=lambda r: -r["z"]):
        b = B["rows"].get(f"{row['lane']}|{row['obj']}")
        if b and (b["position"] != row["position"] or b["statement"] != row["statement"]):
            P(f"    {row['obj'][:34]:34s} {b['position']} / {b['statement']} -> {row['position']} / {row['statement']}")
elif MUT:
    P("  C6 needs the unmutated cfg269_results.json; run without MUTATE first")
P("")

# ------------------------------------------------------------------ write
ok_all = all(CHK.values())
P(f"CHECKS: {sum(CHK.values())}/{len(CHK)} pass" + ("" if ok_all else "  -- FAILURES: " + ", ".join(k for k, v in CHK.items() if not v)))


def jc(o):
    if isinstance(o, dict):
        return {str(k): jc(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)):
        return [jc(v) for v in o]
    if isinstance(o, (np.floating, float)):
        return None if not np.isfinite(o) else float(o)
    if isinstance(o, (np.integer,)):
        return int(o)
    if isinstance(o, np.bool_):
        return bool(o)
    if isinstance(o, np.ndarray):
        return jc(o.tolist())
    return o


res_rows = {}
for row in ROWS:
    ev = row["ev"]
    res_rows[f"{row['lane']}|{row['obj']}"] = dict(lane=row["lane"], obj=row["obj"], z=row["z"], cls=row["cls"], src=row["src"], y=ev["y"], DpredF=ev["DpredF"],
                                                  DpredR=ev["DpredR"], DpredPROXY=ev["DpredP"], G=ev["G"], D=ev["D"], rF=ev["r"]["F"], rR=ev["r"]["R"], rPROXY=ev["r"]["P"],
                                                  sig=ev["sig"], zF=ev["z"]["F"], zR=ev["z"]["R"], P=ev["P"], verdict=row["verdict"], position=row["position"],
                                                  statement=row["statement"], gates=row["gates"], robust=row["robust"], labels=row["labels"], xstar=ev["xstar"],
                                                  floor=row["floor"], pool_key=row.get("pool_key"), stageA=row["stageA"], cells=row["cells"],
                                                  K_bracket=row.get("K_bracket"), notes=row.get("notes"), dominant=ev["dominant"], c8_dev=row.get("c8_dev"))
json.dump(jc(dict(criteria_sha256=CRIT_SHA, mutate=MUT, checks=CHK, rows=res_rows, pools=POOLS, bins=BINV)), open(os.path.join(LANE, f"cfg269_results{SFX}.json"), "w"), indent=1)
with open(os.path.join(LANE, f"cfg269_rows{SFX}.csv"), "w", newline="") as fh:
    w = csv.writer(fh)
    w.writerow(["lane", "object", "z", "class", "y_canonical", "D_pred_FLAT", "D_pred_RIVAL", "G_dex", "D_obs", "r_FLAT", "r_RIVAL", "r_PROXY", "sigma_FLAT", "sigma_RIVAL",
                "z_FLAT", "z_RIVAL", "P", "verdict", "position", "statement", "robust", "floor", "xstar_FLAT", "xstar_RIVAL", "labels"])
    for row in sorted(ROWS, key=lambda r: -r["z"]):
        ev = row["ev"]
        w.writerow([row["lane"], row["obj"], f"{row['z']:.4f}", row["cls"], f"{ev['y']:.4g}", f"{ev['DpredF']:.4f}", f"{ev['DpredR']:.4f}", f"{ev['G']:.4f}", f"{ev['D']:.4g}",
                    f"{ev['r']['F']:+.4f}", f"{ev['r']['R']:+.4f}", f"{ev['r']['P']:+.4f}", f"{ev['sig']['F']['tot']:.4f}", f"{ev['sig']['R']['tot']:.4f}", f"{ev['z']['F']:+.3f}",
                    f"{ev['z']['R']:+.3f}", f"{ev['P']:.3f}", row["verdict"], row["position"], row["statement"], row["robust"], row["floor"], f"{ev['xstar']['F']:+.3f}",
                    f"{ev['xstar']['R']:+.3f}", "; ".join(row["labels"])])
open(os.path.join(LANE, f"cfg269_discriminate{SFX}.out"), "w").write("\n".join(OUT) + "\n")
sys.exit(0 if ok_all else 1)
