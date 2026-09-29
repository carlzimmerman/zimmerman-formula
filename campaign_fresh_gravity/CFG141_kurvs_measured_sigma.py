#!/usr/bin/env python3
"""CFG141 -- KURVS a0(z) WITH EACH GALAXY'S MEASURED OUTER DISPERSION: the pressure-support correction from sigma(R) at R_max.
CFG140 was NON-DIAGNOSTIC because the outer pressure support was unmeasured.  Here the constant sigma0 is replaced by each galaxy's own
Halpha sigma at R_max, read from the paper's plotted major-axis profiles (the data chat's extraction, 94e4a5181; observed sigma, both sides).

Criteria frozen and committed before the extraction was opened: campaign_fresh_gravity/CFG141_FROZEN_CRITERIA.md (4da622ccf).
  physics  isotropic isothermal self-gravitating layer: rho sigma^2 ~ Sigma^2, so V_c^2 = V^2 + 2 sigma(R)^2 R/R_d with the LOCAL sigma (P2);
           fixed-scale-height variant V_c^2 = V^2 + sigma^2 R/R_d - R dsigma^2/dR, capped at >= 0 (P3).
  sigma_out interpolated at R_max on each side that reaches it (sides averaged); else the error-weighted mean of the outermost three
           points; dropped if the profile does not reach 0.5 R_max.  Error from the plotted bars.
  pipeline CFG140's, exec'd read-only (samples, baryons, grid mu x delta x footing, SPARC anchor at sigma = 10 km/s, pooling, errors).
PRE-DECLARED (from the frozen file)
  C1 CONTROL  P2 with sigma_out = the tabulated sigma0 reproduces CFG140's committed P1 grid exactly (1e-12).
  C2 CONTROL  every selected profile finite and positive, its radius range consistent with R_max; per galaxy: reaches R_max / 0.5 R_max / dropped.
  R0 POWER    (printed before any g_obs) as CFG140, with sigma_out's error under P2.
  H1 [HEADLINE; MUTATE must change it] under P2 flat a0 NOT disfavoured: NOT (Delta'_flat > +2 sigma in every one of the 24 P2 cells).
  H2          (reported verdict) under P2 the rival disfavoured: Delta'_H < -2 sigma in every P2 cell.
  R1-R4 (reported): the P2 and P3 grids; per galaxy; sigma_out/sigma0; the P3 verdicts.
MUTATE=1: every KURVS v_last x 10^0.3 (inherited from CFG140's exec'd prefix) -- H1 must FAIL (rc = 1).
Run: python3 campaign_fresh_gravity/CFG141_kurvs_measured_sigma.py   (MUTATE=1 for the control)
"""
import os, sys, io, csv, math, json, contextlib
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import CFG7_common as C
MUTATE = os.environ.get("MUTATE", "0") == "1"
R = C.Report("CFG141_kurvs_measured_sigma", MUTATE)
P, check = R.P, R.check
P(__doc__.split("Run: python3")[0].strip())
if MUTATE:
    P("\n  *** MUTATE=1: every KURVS v_last x 10^0.3 (g_obs x 4) -- H1 must FAIL ***")

F140 = os.path.join(HERE, "CFG140_kurvs_a0z.py")
src = open(F140).read()
g140 = {"__file__": F140, "__name__": "cfg140"}
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(src[:src.index("# ================================================================== C1-C3")], "CFG140", "exec"), g140)
_i = src.index("\ndef power(objs, mu, dlt, Pv, foot):")                       # CFG140 defines power() after its controls marker:
exec(compile(src[_i:src.index("\nPW = {}", _i)], "CFG140-power", "exec"), g140)  # its committed source, exec'd read-only into the same namespace
KU, SP, A0, E = g140["KU"], g140["SP"], g140["A0"], g140["E"]
gbar, gobs, dlog_gobs, gpred, slope, pooled, score, power = (g140[k] for k in ("gbar", "gobs", "dlog_gobs", "gpred", "slope", "pooled", "score", "power"))
MUS, DELS, FOOTS, KPC = g140["MUS"], g140["DELS"], g140["FOOTS"], g140["KPC"]

# ------------------------------------------------------------------ sigma_out from the extracted profiles
PROF = {}
for r in csv.DictReader(open(os.path.join(REPO, "data_assembly", "arxiv_tables", "kurvs_sigma_profiles", "kurvs_sigma_profiles.csv"))):
    PROF.setdefault(int(r["kurvs_id"]), []).append((float(r["R_kpc"]), float(r["sigma_obs_kms"]), float(r["err_up_kms"]), float(r["err_lo_kms"]),
                                                    int(r["clipped_white_marker"])))


def sigma_out(kid, Rmax, include_clipped=False):
    pts = [(abs(Rk), s, 0.5 * (eu + el), Rk >= 0) for Rk, s, eu, el, cl in PROF.get(kid, []) if include_clipped or not cl]
    if not pts:
        return None
    ok = all(np.isfinite([p[0], p[1], p[2]]).all() and p[1] > 0 and p[2] > 0 for p in pts)
    rprof = max(p[0] for p in pts)
    if rprof < 0.5 * Rmax:
        return dict(status="dropped", ok=ok, rprof=rprof)
    vals = []
    for side in (True, False):
        sp = sorted((p[0], p[1], p[2]) for p in pts if p[3] == side)
        if sp and sp[-1][0] >= Rmax and sp[0][0] <= Rmax:
            rr, ss, ee = zip(*sp)
            vals.append((float(np.interp(Rmax, rr, ss)), float(np.interp(Rmax, rr, ee))))
    out3 = sorted(pts, key=lambda p: -p[0])[:3]
    rr3 = np.array([p[0] for p in out3]); s3 = np.array([p[1] for p in out3]); e3 = np.array([p[2] for p in out3])
    grad = float(np.polyfit(rr3, s3 ** 2, 1)[0]) if len(out3) >= 2 and np.ptp(rr3) > 0 else 0.0     # d sigma^2 / dR, outermost three
    if vals:
        s = float(np.mean([v[0] for v in vals])); e = float(math.sqrt(sum(v[1] ** 2 for v in vals)) / len(vals)); status = "reaches R_max"
    else:
        w = 1 / e3 ** 2
        s = float(np.sum(w * s3) / np.sum(w)); e = float(1 / math.sqrt(np.sum(w))); status = "outermost three (inside R_max)"
    return dict(status=status, ok=ok, rprof=rprof, s=s, e=e, grad=grad)


def with_sigma(objs, include_clipped=False):
    out, info = [], {}
    for o in objs:
        kid = int(o["name"].split("-")[1])
        so = sigma_out(kid, o["R"], include_clipped)
        info[kid] = so
        if so is None or so["status"] == "dropped":
            continue
        out.append(dict(o, sig=so["s"], esig=so["e"], grad=so["grad"]))
    return out, info


KU2, INFO = with_sigma(KU)
KU2c, INFOc = with_sigma(KU, include_clipped=True)


# ------------------------------------------------------------------ P3: fixed scale height with the gradient (capped at >= 0)
def gobs3(o, V=None):
    V = o["V"] if V is None else V
    corr = max(0.0, o["sig"] ** 2 * o["R"] / o["Rd"] - o["R"] * o.get("grad", 0.0))
    vc2 = V ** 2 + corr
    return vc2 * 1e6 / (o["R"] * KPC), vc2, corr


def dlog3(o, V=None):
    V = o["V"] if V is None else V
    _, vc2, corr = gobs3(o, V)
    tv = 2 * V * o["eV"]
    ts = (2 * o["sig"] * o["esig"] * o["R"] / o["Rd"]) if corr > 0 else 0.0
    inc = math.radians(o["inc"]) if np.isfinite(o["inc"]) and o["inc"] > 1 else math.radians(60)
    ti = 2 * V ** 2 * o["einc"] / math.tan(inc)
    return math.sqrt(tv ** 2 + ts ** 2 + ti ** 2) / vc2 / math.log(10)


def score3(objs, mu, dlt, foot, measured_gas=False, rival=False):
    D, S = [], []
    for o in objs:
        a = A0[foot] * (E(o["z"]) if rival else 1.0)
        gb = gbar(o, mu, dlt, measured_gas)
        gp = gpred(gb, a)
        go, _, _ = gobs3(o)
        D.append(math.log10(go / gp)); S.append(math.hypot(dlog3(o), slope(gb, a) * o["sm"]))
    return pooled(D, S)


# ================================================================== C1 / C2
R.banner("C1 / C2  CONTROLS")
c140 = json.load(open(os.path.join(HERE, "CFG140_kurvs_a0z" + ("_MUTATE" if MUTATE else "") + "_results.json")))["numbers"]["grid"]
dev = 0.0
for mu in MUS:
    for dlt in DELS:
        for foot in FOOTS:
            (kf, _), _, _ = score(KU, mu, dlt, "P1", foot)
            (kh, _), _, _ = score(KU, mu, dlt, "P1", foot, rival=True)
            ref = c140[f"{mu}|{dlt}|P1|{foot}"]
            dev = max(dev, abs(kf - ref["kf"]), abs(kh - ref["kh"]))
check("C1 CONTROL: P2 with sigma_out = the tabulated sigma0 reproduces CFG140's committed P1 grid exactly (1e-12)",
      f"max |difference| {dev:.1e} over 24 cells" + ("  [against CFG140's MUTATE grid]" if MUTATE else ""), dev < 1e-12)
rows = []
for o in KU:
    kid = int(o["name"].split("-")[1]); so = INFO[kid]
    rows.append(f"{kid}: {so['status'] if so else 'no profile'} (profile to {so['rprof']:.1f} kpc vs R_max {o['R']:.1f})" if so else f"{kid}: no profile")
okc = all(INFO[int(o['name'].split('-')[1])] is not None and INFO[int(o['name'].split('-')[1])]["ok"] for o in KU)
check("C2 CONTROL: every selected profile finite and positive and consistent with R_max; per galaxy status",
      "; ".join(rows) + f"; used N = {len(KU2)} of 10", okc)

# ================================================================== R0
R.banner("R0  POWER (baryons, sigma_out and quoted errors only; no observed velocity enters)")
PW = {(mu, dlt, foot): power(KU2, mu, dlt, "P1", foot) for mu in MUS for dlt in DELS for foot in FOOTS}
s0, e0 = PW[(0.67, 0.0, "canonical")]
check("R0 (reported) POWER under P2: expected separation flat vs rival over the pooled error",
      f"central cell {s0:+.3f} dex / {e0:.3f} = {s0 / e0:.2f} sigma; range {min(v[0] / v[1] for v in PW.values()):.2f}-{max(v[0] / v[1] for v in PW.values()):.2f} sigma "
      "(CFG52's correlated floor about 2.3 sigma)", True, load_bearing=False)

# ================================================================== H1 / H2 (P2) and the P3 grid
R.banner("H1 / H2  UNDER P2 (the measured outer sigma), anchor-corrected")
G2, G3 = {}, {}
for mu in MUS:
    for dlt in DELS:
        for foot in FOOTS:
            (kf, ekf), _, _ = score(KU2, mu, dlt, "P1", foot)
            (kh, ekh), _, _ = score(KU2, mu, dlt, "P1", foot, rival=True)
            (af, eaf), _, _ = score(SP, mu, dlt, "P1", foot, measured_gas=True)
            (ah, eah), _, _ = score(SP, mu, dlt, "P1", foot, measured_gas=True, rival=True)
            G2[(mu, dlt, foot)] = dict(df=kf - af, edf=math.hypot(ekf, eaf), dh=kh - ah, edh=math.hypot(ekh, eah))
            kf3, ekf3 = score3(KU2, mu, dlt, foot); kh3, ekh3 = score3(KU2, mu, dlt, foot, rival=True)
            af3, eaf3 = score3(SP, mu, dlt, foot, measured_gas=True); ah3, eah3 = score3(SP, mu, dlt, foot, measured_gas=True, rival=True)
            G3[(mu, dlt, foot)] = dict(df=kf3 - af3, edf=math.hypot(ekf3, eaf3), dh=kh3 - ah3, edh=math.hypot(ekh3, eah3))
for foot in FOOTS:
    P(f"    {foot} P2 (delta 0): " + "; ".join(f"mu {mu}: D'_flat {G2[(mu, 0.0, foot)]['df']:+.3f}+-{G2[(mu, 0.0, foot)]['edf']:.3f}, D'_H {G2[(mu, 0.0, foot)]['dh']:+.3f}+-{G2[(mu, 0.0, foot)]['edh']:.3f}" for mu in MUS))


def verdicts(Gd):
    fd = sum(1 for v in Gd.values() if v["df"] > 2 * v["edf"]); rd_ = sum(1 for v in Gd.values() if v["dh"] < -2 * v["edh"])
    fin = sum(1 for v in Gd.values() if abs(v["df"]) <= 2 * v["edf"]); rin = sum(1 for v in Gd.values() if abs(v["dh"]) <= 2 * v["edh"])
    return fd, rd_, fin, rin, len(Gd)


fd, rd_, fin, rin, n = verdicts(G2)
cen = (0.67, 0.0, "canonical")
check("H1 [HEADLINE] UNDER P2 THE FRAMEWORK'S FLAT a0 IS NOT DISFAVOURED: NOT (Delta'_flat > +2 sigma in every one of the 24 P2 cells)" + ("  [MUTATE: v x 2]" if MUTATE else ""),
      f"cells flat > +2 sigma: {fd}/{n}; flat within 2 sigma: {fin}/{n}; central Delta'_flat {G2[cen]['df']:+.3f} +- {G2[cen]['edf']:.3f}", fd < n)
check("H2 (reported verdict) UNDER P2 THE RIVAL a0 ~ H(z) IS DISFAVOURED: Delta'_H < -2 sigma in every P2 cell",
      f"cells rival < -2 sigma: {rd_}/{n}; rival within 2 sigma: {rin}/{n}; central Delta'_H {G2[cen]['dh']:+.3f} +- {G2[cen]['edh']:.3f}", rd_ == n, load_bearing=False)

# ================================================================== reported rows
R.banner("REPORTED ROWS")
check("R1 (reported) the P2 and P3 grids (anchor-corrected): ranges and cell counts",
      f"P2: Delta'_flat {min(v['df'] for v in G2.values()):+.3f} .. {max(v['df'] for v in G2.values()):+.3f}, Delta'_H {min(v['dh'] for v in G2.values()):+.3f} .. {max(v['dh'] for v in G2.values()):+.3f}; "
      f"P3: Delta'_flat {min(v['df'] for v in G3.values()):+.3f} .. {max(v['df'] for v in G3.values()):+.3f}, Delta'_H {min(v['dh'] for v in G3.values()):+.3f} .. {max(v['dh'] for v in G3.values()):+.3f}",
      True, load_bearing=False)
_, Dk, _ = score(KU2, 0.67, 0.0, "P1", "canonical")
_, Dkh, _ = score(KU2, 0.67, 0.0, "P1", "canonical", rival=True)
rows2 = []
for o, d, dh in zip(KU2, Dk, Dkh):
    kid = int(o["name"].split("-")[1]); so = INFO[kid]; s0t = next(q for q in KU if q["name"] == o["name"])["sig"]
    fac = (o["V"] ** 2 + 2 * o["sig"] ** 2 * o["R"] / o["Rd"]) / o["V"] ** 2
    rows2.append(f"{kid}: sigma0 {s0t:.0f}, sigma_out {so['s']:.0f}+-{so['e']:.0f} ({so['status']}), R/R_d {o['R'] / o['Rd']:.1f}, V_c^2/V^2 {fac:.2f}, D_flat {d:+.2f}, D_H {dh:+.2f}")
check("R2 (reported) per galaxy (central cell, P2, unanchored)", "; ".join(rows2), True, load_bearing=False)
rat = np.array([o["sig"] / next(q for q in KU if q["name"] == o["name"])["sig"] for o in KU2])
check("R3 (reported) sigma_out / sigma0 across the sample (the constant-sigma assumption at R_max)",
      f"median {np.median(rat):.2f}, range {rat.min():.2f}-{rat.max():.2f} (N {len(rat)})", True, load_bearing=False)
fd3, rd3, fin3, rin3, n3 = verdicts(G3)
check("R4 (reported) the verdicts under P3 (fixed scale height, gradient term, capped)",
      f"flat > +2 sigma in {fd3}/{n3}; rival < -2 sigma in {rd3}/{n3}; flat within 2 sigma {fin3}/{n3}; rival within 2 sigma {rin3}/{n3}; central D'_flat {G3[cen]['df']:+.3f}, D'_H {G3[cen]['dh']:+.3f}",
      True, load_bearing=False)
Gc = {}
for mu in MUS:
    for dlt in DELS:
        for foot in FOOTS:
            (kf, ekf), _, _ = score(KU2c, mu, dlt, "P1", foot); (kh, ekh), _, _ = score(KU2c, mu, dlt, "P1", foot, rival=True)
            ref = G2[(mu, dlt, foot)]
            (af, eaf), _, _ = score(SP, mu, dlt, "P1", foot, measured_gas=True); (ah, eah), _, _ = score(SP, mu, dlt, "P1", foot, measured_gas=True, rival=True)
            Gc[(mu, dlt, foot)] = dict(df=kf - af, edf=math.hypot(ekf, eaf), dh=kh - ah, edh=math.hypot(ekh, eah))
fdc, rdc, _, _, _ = verdicts(Gc)
check("R5 (reported; disclosed variant) the authors' clipped (white-marker) pixels INCLUDED in sigma_out",
      f"N {len(KU2c)}; flat > +2 sigma in {fdc}/24; rival < -2 sigma in {rdc}/24; central D'_flat {Gc[cen]['df']:+.3f}, D'_H {Gc[cen]['dh']:+.3f}", True, load_bearing=False)

if fd == n and all(v["df"] > 3 * v["edf"] for v in G2.values()):
    reading = "under P2 flat a0 is disfavoured beyond 3 sigma in every cell: a kill line for the framework's flat-a0 law at z ~ 1.5 (conditional on the isothermal layer; P3 the check)"
elif fd == n:
    reading = "under P2 flat a0 is disfavoured in every cell (> 2 sigma): conditional on the isothermal layer; P3 the check"
elif rd_ == n:
    reading = "under P2 the rival a0 ~ H(z) is disfavoured in every cell and flat a0 is not: conditional on the isothermal layer; P3 the check; CFG52's floor applies"
else:
    reading = "NON-DIAGNOSTIC under P2: the gas bracket (no measured gas exists) remains the dominant ambiguity"
P(f"\n    READING (declared): {reading}")
ser = lambda Gd: {f"{k[0]}|{k[1]}|{k[2]}": v for k, v in Gd.items()}
R.num("P2", ser(G2)); R.num("P3", ser(G3)); R.num("clipped_included", ser(Gc))
R.num("sigma_out", {k: v for k, v in INFO.items()}); R.num("power", {f"{k[0]}|{k[1]}|{k[2]}": list(v) for k, v in PW.items()}); R.num("reading", reading)
nf = R.write()
sys.exit(1 if nf else 0)
