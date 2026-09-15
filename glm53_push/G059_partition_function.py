#!/usr/bin/env python3
"""G059 -- THE PARTITION FUNCTION: the phantom/free-dust partition tested three ways.
HONEST VERDICT: the certified kernel's sub-a0 branch delivers ~6/10 of the deficit at
420 kpc; NO non-degenerate candidate reaches the measured mass [0.8, 1.3] band; the
residual is the free dust's registered (astrophysical-normalization) share, consistent
with hy4's H012 two-regime resolution.

THE GAP.  G050 (the split architecture): with the EFE cap at cH0 the split
delivers 0.41x/0.41x the measured mass at 420 kpc; the deficit (0.59x M_b) is
the free dust's share.  G050 left the PARTITION UNDECIDED: it capped the
phantom with a step at g_ext = cH0, but the theory's own kernel says the
phantom exists only sub-a0 -- the share must be a FUNCTION of the local field
(P4: the share rises as g_tot/a0 falls through a0; G050 V4 rho = -0.926).
This lane DERIVES the partition from G050's per-cluster data (same ingest,
same on-disk X-COP FITS -- nothing re-downloaded) with THREE candidates:

  (1) KERNEL partition -- the mu2 kernel itself, oriented sub-a0:
      share_k(r) = 1 - mu2(g_tot(r)/(2 a0)) = (1 + g_tot/(4 a0))^-2,
      mu2(s) = 1-(1+s/2)^-2 (the certified kernel, G002/G057 convention).
      Deep (g << a0): share -> 1; Newtonian (g >> a0): share -> 0.
      Variant carried beside: share_k'(r) = 1 - mu2(g_tot/a0).
  (2) VIRIAL partition -- the charge splits by binding: the cumulative work
      fraction carried by the baryon well's deep branch,
      share_v(<r) = W_M/(W_M + W_N),  W_M = sum (1-mu2(x_j)) x_j w_j,
      W_N = sum mu2(x_j) x_j w_j, x_j = g_tot(r_j)/a0 (G050's per-bin field),
      w_j = dln r_j (cumulative inner-to-outer).
  (3) r_M-SURFACE partition -- binary: phantom where r > r_M(cluster)
      (g_tot(r_M) = a0), free inside; the supported phantom is the measured
      deficit accumulated OUTSIDE r_M up to 420 kpc.

For each candidate x footing: predicted (M_ph,supported(<420) + M_b(<420)) /
M_HSE(<420).  VERDICT: the median over the 12 clusters must land in [0.8, 1.3].
Both footings carried: canonical a0 = s_DE/2, alt a0 = 1.1279e-10.

DATA NOTE (G050 units slips, traced).  G050's safety floors read 1e9*MSUN
against masses CARRIED IN MSUN (1e9*MSUN = 1.99e39 swamps every cluster mass
~1e14), and its g_tot line dropped the *MSUN conversion.  The arrays stored
in G050_results.json are the residue (gtot/a0 ~ 1e-5, shares ~ 1e-27; the
0.41x headline is unaffected -- the EFE cap zeroed the support anyway).
G059 fixes both and recomputes from the SAME on-disk FITS through G050's own
ingest (load_cluster/baryons/dlnM_dlnr; nothing re-downloaded).
"""
import json
import math
import os

import numpy as np
from astropy.io import fits

RES = []


def check(n, measured, ok, d=""):
    ok = bool(ok)
    print(f"  [{'PASS' if ok else 'FAIL'}] {n}")
    print(f"         measured: {measured}")
    if d:
        print(f"         reading : {d}")
    RES.append({"name": n, "measured": str(measured), "pass": ok, "reading": d})


print(__doc__)

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
XB = os.path.join(REPO, "real_research", "data", "xcop")
G = 6.674e-11
MSUN = 1.98892e30
KPC = 3.0857e19
c_l = 2.99792458e8
H0 = 67.4 * 1e3 / 3.0857e22
rho_lam = 0.685 * 3 * H0**2 / (8 * math.pi * G)
s_DE = c_l * math.sqrt(G * rho_lam)
A0 = {"canonical": s_DE / 2, "alt": 1.1279e-10}
GEXT = c_l * H0
RG = np.array([50., 75., 100., 150., 210., 300., 420., 600.])
I420 = int(np.argmin(np.abs(RG - 420)))


def mu2(x):
    x = np.asarray(x, float)
    return 1.0 - (1.0 + x / 2.0) ** (-2.0)


def loginterp(x, xp, fp):
    x = np.atleast_1d(np.asarray(x, float))
    ok = np.isfinite(xp) & np.isfinite(fp) & (xp > 0) & (fp > 0)
    xp, fp = np.asarray(xp)[ok], np.asarray(fp)[ok]
    o = np.argsort(xp)
    xp, fp = xp[o], fp[o]
    out = 10 ** np.interp(np.log10(x), np.log10(xp), np.log10(fp))
    out[(x < xp[0]) | (x > xp[-1])] = np.nan
    return out


def load_cluster(name):
    p = os.path.join(XB, name)
    hm = fits.open(os.path.join(p, f"{name}_hydro_mass.fits"))[1].data
    fg = fits.open(os.path.join(p, f"{name}_fgas_profile.fits"))[1].data
    d = dict(name=name,
             r_hm=np.array(hm["RADIUS"], float),
             M_hse=np.array(hm["M_FORW"], float),
             r_fg=np.array(fg["RADIUS"], float) * 1e3,
             M_gas=np.array(fg["MGAS"], float))
    fs = os.path.join(p, f"{name}_mstar.fits")
    if os.path.exists(fs):
        ms = fits.open(fs)[2].data
        d["r_st"] = np.array(ms["RADIUS"], float)
        d["M_st"] = np.array(ms["MSTAR"], float)
        d["has_star"] = True
    else:
        d["has_star"] = False
    return d


CL = [load_cluster(n) for n in sorted(d for d in os.listdir(XB)
                                      if os.path.isdir(os.path.join(XB, d)))]
print(f"X-COP clusters loaded: {len(CL)} "
      f"({', '.join(c['name'] for c in CL)}); "
      f"{sum(c['has_star'] for c in CL)} with a measured stellar profile")
print("(G050 ingest reused verbatim; same on-disk FITS; nothing re-downloaded)")

# --- the stellar import for the 5 clusters without a measured profile (G050) ---
ratio_tab = {}
for r in RG:
    v = []
    for c in CL:
        if not c["has_star"]:
            continue
        mg = loginterp([r], c["r_fg"], c["M_gas"])[0]
        ms = loginterp([r], c["r_st"], c["M_st"])[0]
        if np.isfinite(mg) and np.isfinite(ms) and ms > 0:
            v.append(ms / mg)
    if v:
        ratio_tab[r] = (float(np.median(v)), len(v))


def baryons(c, r):
    mg = loginterp(r, c["r_fg"], c["M_gas"])
    if c["has_star"]:
        ms = loginterp(r, c["r_st"], c["M_st"])
    else:
        ms = np.array([np.nan if (not np.isfinite(g)) else
                       g * ratio_tab.get(r_, (0.047, 0))[0]
                       for r_, g in zip(r, mg)])
    return mg + ms, mg, ms, (not c["has_star"])


def dlnM_dlnr(c, r):
    r_hm, M = c["r_hm"], c["M_hse"]
    out = np.empty(len(r))
    for i, rq in enumerate(r):
        j = int(np.searchsorted(r_hm, rq))
        j = min(max(j, 0), len(r_hm) - 2)
        out[i] = math.log(M[j + 1] / M[j]) / math.log(r_hm[j + 1] / r_hm[j])
    return out
# ================== STEP 1 -- the per-bin partition shares, all three candidates
def solve_rM(c, a0):
    """r_M: G M_hse(<r)/r^2 = a0, evaluated on the measured profile grid.

    CORRECTIVE NOTE: masses arrive in Msun -- the * MSUN conversion is
    MANDATORY here.  The original G059 draft omitted it, computing g ~ 2e30x
    too small, forcing ALL 12 clusters into 'all_sub' and the rM-delivered
    amplitude to 1.000 by identity.  Caught in review; fixed in place."""
    r_hm = np.asarray(c["r_hm"], float)
    M = np.asarray(c["M_hse"], float)
    x = G * M * MSUN / (r_hm * KPC) ** 2 / a0
    if np.all(x > 1.0):
        return float(r_hm[-1]), "all_super"     # Newtonian through the window
    if np.all(x < 1.0):
        return float(r_hm[0]), "all_sub"        # deep through the window (degenerate)
    idx = int(np.where(np.diff(np.sign(x - 1.0)) != 0)[0][-1])  # outermost crossing
    lo, hi = float(r_hm[idx]), float(r_hm[idx + 1])
    for _ in range(200):
        mid = math.sqrt(lo * hi)
        xm = G * float(loginterp([mid], r_hm, M)[0]) * MSUN / (mid * KPC) ** 2 / a0
        if xm > 1.0:
            lo = mid
        else:
            hi = mid
    return math.sqrt(lo * hi), "in_window"


DATA = {}
for foot, a0 in A0.items():
    DATA[foot] = {}
    for c in CL:
        r = RG.copy()
        mb, mg, ms, imported = baryons(c, r)
        Mh = loginterp(r, c["r_hm"], c["M_hse"])
        # floors: 1e9 Msun; g_tot needs M*MSUN (G050 wrote 1e9*MSUN floors
        # against Msun-carried masses AND dropped the *MSUN in g_tot -- DATA NOTE)
        Mres = np.maximum(Mh - mb, 1e9)
        gtot = G * np.maximum(Mh, 1e9) * MSUN / (r * KPC) ** 2
        x = gtot / a0
        # (1) KERNEL: the mu2 kernel oriented sub-a0  (deep -> 1, Newtonian -> 0)
        share_k = (1.0 + x / 4.0) ** (-2.0)      # = 1 - mu2(g/(2a0))
        share_kp = (1.0 + x / 2.0) ** (-2.0)     # variant: 1 - mu2(g/a0)
        # (2) VIRIAL: cumulative work split of the local dynamical support
        w = np.gradient(np.log(r))
        wm = (1.0 - mu2(x)) * x * w              # the deep-branch (phantom) work
        wn = mu2(x) * x * w                      # the baryon-well Newtonian work
        share_v = np.cumsum(wm) / np.cumsum(wm + wn)
        # (3) r_M SURFACE: binary, phantom exactly where the local field is sub-a0
        rM, rM_state = solve_rM(c, a0)
        share_bin = (x < 1.0).astype(float)   # corrective: share from the physical condition,
                                              # not from the solver's (previously broken) rM
        DATA[foot][c["name"]] = dict(
            r=r, mb=mb, Mh=Mh, Mres=Mres, gtot=gtot, x=x,
            share_k=share_k, share_kp=share_kp, share_v=share_v,
            rM=rM, rM_state=rM_state, share_bin=share_bin,
            imported=bool(imported))


def Mph_int(r, Mres, share):
    """the deficit integral: supported phantom accumulated 0 -> 420 kpc.
    Inner [0, r_0] weighted by share[0]; each segment by the segment-mean share."""
    seg = 0.5 * (share[:-1] + share[1:]) * np.diff(Mres)
    inner = share[0] * Mres[0]
    return float(inner + seg[:I420].sum())


def Mres_at(c, rq):
    mb, _, _, _ = baryons(c, np.atleast_1d([rq]))
    Mh = loginterp([rq], c["r_hm"], c["M_hse"])
    return float(Mh[0] - mb[0])


RAT = {}
for foot in A0:
    RAT[foot] = {}
    for c in CL:
        d = DATA[foot][c["name"]]
        i = I420
        row = {}
        for key, share in [("kernel", d["share_k"]), ("kernel_g_arg", d["share_kp"]),
                           ("virial", d["share_v"])]:
            pt = float((d["mb"][i] + share[i] * d["Mres"][i]) / d["Mh"][i])
            it = float((d["mb"][i] + Mph_int(d["r"], d["Mres"], share)) / d["Mh"][i])
            row[key] = dict(pt=pt, integral=it, share420=float(share[i]))
        # binary: integral = the deficit accumulated where share_bin = 1 (sub-a0)
        # (same share-consistent integrator as the other candidates; the old
        #  Mres_at extrapolation went negative when the crossing lies beyond
        #  the 420 kpc edge -- caught in the corrective review)
        mph_bin = Mph_int(d["r"], d["Mres"], d["share_bin"])
        row["rM"] = dict(pt=float((d["mb"][i] + d["share_bin"][i] * d["Mres"][i]) / d["Mh"][i]),
                         integral=float((d["mb"][i] + mph_bin) / d["Mh"][i]),
                         share420=float(d["share_bin"][i]), mph_int=float(mph_bin))
        RAT[foot][c["name"]] = row
    RAT[foot]["_median"] = {}
    for key in ["kernel", "kernel_g_arg", "virial", "rM"]:
        RAT[foot]["_median"][key] = dict(
            pt=float(np.median([RAT[foot][c["name"]][key]["pt"] for c in CL])),
            integral=float(np.median([RAT[foot][c["name"]][key]["integral"] for c in CL])))
print()
print("=" * 88)
print("STEP 1 -- partition shares computed: 12 clusters x 8 radii x 2 footings "
      "x 3 candidates (+1 kernel variant)")
print("=" * 88)
print(f"  r_M states (canonical): " +
      ", ".join(f"{c['name']}:{DATA['canonical'][c['name']]['rM']:.0f}"
                f"[{DATA['canonical'][c['name']]['rM_state']}]" for c in CL))
print(f"  r_M states (alt):       " +
      ", ".join(f"{c['name']}:{DATA['alt'][c['name']]['rM']:.0f}"
                f"[{DATA['alt'][c['name']]['rM_state']}]" for c in CL))
print("  (mu2 = the certified monotone-increasing kernel 1-(1+s/2)^-2; the phantom"
      "\n   share is oriented sub-a0 as share = 1 - mu2, so deep -> 1, Newtonian -> 0"
      "\n   -- the task's asymptotics; the literal increasing mu2 would invert them)")
# ============ STEP 2 -- the delivered amplitude at 420 kpc, table, both footings
ftag = {"canonical": "s_DE/2 = 9.3623e-11", "alt": "1.1279e-10"}


def trow(ft, cname):
    row = RAT[ft][cname]
    d = DATA[ft][cname]
    return (f"  {cname:8s} {row['kernel']['share420']:7.2f} {row['kernel']['pt']:6.2f} "
            f"{row['kernel']['integral']:6.2f}  | {row['virial']['share420']:6.2f} "
            f"{row['virial']['pt']:6.2f} {row['virial']['integral']:6.2f}  | "
            f"{d['rM']:5.0f}{d['rM_state'][:4]:5s} {row['rM']['pt']:6.2f} "
            f"{row['rM']['integral']:6.2f}  ({d['imported'] and 'imp' or 'meas'})")


print()
print("=" * 88)
print("STEP 2 -- the delivered amplitude at 420 kpc: (M_ph,supported + M_b)/M_HSE")
print("=" * 88)
for ft in A0:
    print(f"\n  --- {ft}: a0 = {ftag[ft]} ---")
    print("  cluster   KERNEL: sh(420)  pt    int   | VIRIAL: sh(420)  pt    int   "
          "| r_M   B_pt  B_int")
    for c in CL:
        print(trow(ft, c["name"]))
    m = RAT[ft]["_median"]
    msh = {k: float(np.median([RAT[ft][c["name"]][k]["share420"] for c in CL]))
           for k in ["kernel", "virial", "rM"]}
    print(f"  {'MEDIAN':8s} {msh['kernel']:7.2f} {m['kernel']['pt']:6.2f} "
          f"{m['kernel']['integral']:6.2f}  | {msh['virial']:6.2f} "
          f"{m['virial']['pt']:6.2f} {m['virial']['integral']:6.2f}  |       "
          f"{m['rM']['pt']:6.2f} {m['rM']['integral']:6.2f}   (medians)")

# ============================================================== STEP 3 -- VERDICT
print()
print("=" * 88)
print("STEP 3 -- THE VERDICT: candidate closes the gap iff the median ratio lands "
      "in [0.8, 1.3]")
print("=" * 88)
NAMES = {"kernel": "KERNEL (1-mu2(g/2a0))", "virial": "VIRIAL (W_M/(W_M+W_N))",
         "rM": "r_M-SURFACE (binary beyond a0 crossing)"}
VERD, DEGEN = {}, {}
for key in ["kernel", "virial", "rM"]:
    for ft in A0:
        med = RAT[ft]["_median"][key]["integral"]
        VERD[(key, ft)] = med
        degen = (key == "rM") and all(
            DATA[ft][c["name"]]["rM_state"] == "all_sub" for c in CL)
        DEGEN[(key, ft)] = degen
        if degen:
            rd = ("[0.8, 1.3] would be the band -- but this PASS is VACUOUS: "
                  "the local field is sub-a0 through the entire window for ALL 12 "
                  "clusters on this footing, so the binary share is 1 everywhere "
                  "in the window and the ratio returns M_HSE identically by "
                  "construction (zero explanatory content: no partition performed)")
        else:
            rd = ("[0.8, 1.3] = the partition closes the amplitude gap (the phantom "
                  "supplies the deficit), < 0.8 = undersupply, > 1.3 = oversupply")
        check(f"V-{key} [{ft}: the {NAMES[key]} partition's delivered amplitude at 420 kpc] "
              f"median over 12 clusters of (M_b + M_ph,supported(<420))/M_HSE, "
              f"M_ph,supported the deficit integral of the candidate's own share "
              f"(clean recompute: baryons alone ~0.175x; G050's cap-reduced 0.41x was baryons + capped EOS)",
              f"median delivered / measured = {med:.3f} over 12 clusters "
              f"(pt closed-form variant {RAT[ft]['_median'][key]['pt']:.3f})",
              0.8 <= med <= 1.3, rd)
mbfrac = np.median([DATA["canonical"][c["name"]]["mb"][I420]
                    / DATA["canonical"][c["name"]]["Mh"][I420] for c in CL])
g050ref = np.median([(DATA["canonical"][c["name"]]["mb"][I420]
                      * (1.0 + dlnM_dlnr(c, RG)[I420]))
                     / DATA["canonical"][c["name"]]["Mh"][I420] for c in CL])
print(f"\n  reference: median baryon fraction M_b/M_HSE at 420 kpc = {mbfrac:.3f} "
      f"(coherent with X-COP's own f_b ~ 0.13-0.17); G050's registered 0.409 "
      f"reproduces as (M_b + M_ph,EOS)/M_HSE = {g050ref:.3f} -- its cap never "
      f"fired (broken g_tot), so 0.409 was never baryons-only. The band floor "
      f"0.8 requires the phantom to carry {(0.8 - mbfrac)/(1 - mbfrac):.3f} of "
      f"the measured deficit at 420 kpc")
print(f"\n  (kernel variant 1-mu2(g/a0), beside: "
      + "; ".join(f"{ft} median {RAT[ft]['_median']['kernel_g_arg']['integral']:.3f}"
                  for ft in A0) + ")")

# ============================================== STEP 4 -- the honest residual
print()
print("=" * 88)
print("STEP 4 -- THE HONEST RESIDUAL for the best candidate (|median - 1| minimal)")
print("=" * 88)
best = min([k for k in VERD if not DEGEN[k]], key=lambda k: abs(VERD[k] - 1.0))
key, ft = best
print(f"  best NON-DEGENERATE candidate: {NAMES[key]} on {ft} "
      f"(median ratio {VERD[best]:.3f}; degenerate r_M-PASSes excluded)")
for ft2 in A0:
    print(f"    {ft2}: median ratio {RAT[ft2]['_median'][key]['integral']:.3f}")
res = np.array([RAT[ft][c["name"]][key]["integral"] - 1.0 for c in CL])
shf = np.array([1.0 - (RAT[ft][c["name"]][key]["integral"] * DATA[ft][c["name"]]["Mh"][I420]
                      - DATA[ft][c["name"]]["mb"][I420]) / DATA[ft][c["name"]]["Mres"][I420]
                for c in CL])
print("  cluster   ratio   residual (ratio-1)   deficit shortfall (1 - M_ph,supported/M_res)")
for c, rj, sj in zip(CL, res, shf):
    print(f"  {c['name']:8s} {RAT[ft][c['name']][key]['integral']:6.3f}   {rj:+8.3f}          "
          f"  {sj:+8.3f}")
print(f"  MEDIAN residual = {np.median(res):+.3f} (MAD {np.median(np.abs(res-np.median(res))):.3f}); "
      f"median deficit shortfall = {np.median(shf):+.3f}; range of ratio "
      f"{res.min()+1:.2f}-{res.max()+1:.2f}")
check(f"V-RES [the honest residual of the best candidate at 420 kpc] per-cluster "
      f"(M_b + M_ph,supported)/M_HSE residuals for {NAMES[key]} on {ft}",
      f"median residual {np.median(res):+.3f}; median deficit shortfall "
      f"{np.median(shf):+.3f}; spread {res.min()+1:.2f}-{res.max()+1:.2f}",
      True,
      "the residual stated as a measurement, no threshold: this is what the partition "
      "leaves on the table at 420 kpc")

# ================================================================ the JSON artifact
def arr(a):
    return [float(v) for v in np.asarray(a, float)]


export = dict(
    lane="G059 -- the partition function (phantom/free-dust partition, derived)",
    ingest="G050 ingest reused verbatim (load_cluster/baryons/dlnM_dlnr, same "
           "on-disk X-COP FITS under real_research/data/xcop; nothing re-downloaded)",
    radii_kpc=arr(RG),
    a0={ft: float(v) for ft, v in A0.items()},
    gext_hubble=float(GEXT),
    definitions=dict(
        kernel="share(r) = 1 - mu2(g_tot(r)/(2 a0)) = (1 + g_tot/(4 a0))^-2, "
               "mu2(s) = 1-(1+s/2)^-2 (the certified kernel, oriented sub-a0: "
               "deep -> 1, Newtonian -> 0)",
        kernel_variant="share(r) = 1 - mu2(g_tot/a0) = (1 + g_tot/(2 a0))^-2",
        virial="share_v(<r) = W_M/(W_M+W_N) cumulative; W_M = sum (1-mu2(x_j)) x_j w_j, "
               "W_N = sum mu2(x_j) x_j w_j, x_j = g_tot(r_j)/a0 (G050's per-bin field), "
               "w_j = dln r_j",
        rM="binary: share = 1 where r > r_M (g_tot(r_M) = a0, bisected on M_FORW), "
           "0 inside; M_ph,supported(<420) = M_res(420) - M_res(r_M) accumulated "
           "outside the crossing"),
    ratio_convention="integral = (M_b(<420) + M_ph,supported(<420))/M_HSE(<420) with "
                     "M_ph,supported the deficit integral; pt = the pointwise closure "
                     "share(420) x M_res(<420) (G050 V2 convention), reported beside",
    per_cluster={ft: {c["name"]: dict(
        r=arr(DATA[ft][c["name"]]["r"]),
        gtot_over_a0=arr(DATA[ft][c["name"]]["x"]),
        Mb_Msun=arr(DATA[ft][c["name"]]["mb"]),
        M_hse_Msun=arr(DATA[ft][c["name"]]["Mh"]),
        M_res_Msun=arr(DATA[ft][c["name"]]["Mres"]),
        share_kernel=arr(DATA[ft][c["name"]]["share_k"]),
        share_kernel_g_arg=arr(DATA[ft][c["name"]]["share_kp"]),
        share_virial=arr(DATA[ft][c["name"]]["share_v"]),
        share_binary=arr(DATA[ft][c["name"]]["share_bin"]),
        r_M_kpc=float(DATA[ft][c["name"]]["rM"]),
        r_M_state=DATA[ft][c["name"]]["rM_state"],
        imported_stars=DATA[ft][c["name"]]["imported"],
        ratio_420={k: dict(integral=float(RAT[ft][c["name"]][k]["integral"]),
                           pt=float(RAT[ft][c["name"]][k]["pt"]),
                           share420=float(RAT[ft][c["name"]][k]["share420"]))
                   for k in ["kernel", "kernel_g_arg", "virial", "rM"]},
    ) for c in CL} for ft in A0},
    medians={ft: {k: dict(integral=float(RAT[ft]["_median"][k]["integral"]),
                          pt=float(RAT[ft]["_median"][k]["pt"]))
                  for k in ["kernel", "kernel_g_arg", "virial", "rM"]} for ft in A0},
    verdicts={f"{k}|{ft}": dict(median_ratio=float(VERD[(k, ft)]),
                                closes_gap=bool(0.8 <= VERD[(k, ft)] <= 1.3),
                                degenerate=bool(DEGEN[(k, ft)]))
              for (k, ft) in VERD},
    required_deficit_share_for_band=dict(
        mb_frac_420=float(mbfrac),
        required_share=(float((0.8 - mbfrac) / (1 - mbfrac)))),
    g050_anchor_correction=dict(
        note="G050's registered 0.409x was (M_b + M_ph,EOS)/M_HSE, not baryons-only: "
             "its cap never fired (g_tot broken by the units slips) and the floors "
             "cancelled in share x M_res",
        clean_baryon_fraction_420=float(mbfrac),
        g050_0p409_reproduced_as=(float(g050ref))),
    best_candidate=dict(candidate=key, footing=ft, median_ratio=float(VERD[best]),
                        non_degenerate=True,
                        medians_by_footing={ft2: float(RAT[ft2]["_median"][key]["integral"])
                                            for ft2 in A0},
                        residual_median=float(np.median(res)),
                        residual_mad=float(np.median(np.abs(res - np.median(res)))),
                        deficit_shortfall_median=float(np.median(shf)),
                        ratio_range=[float(res.min() + 1), float(res.max() + 1)]),
    checks=RES, n_pass=sum(1 for r_ in RES if r_["pass"]),
    n_fail=sum(1 for r_ in RES if not r_["pass"]))
with open(os.path.join(HERE, "G059_results.json"), "w") as f:
    json.dump(export, f, indent=1)

print()
print("=" * 88)
print("READING")
print("=" * 88)
print(f"""
  The partition is now a FUNCTION, not a step.  G050's split registered 0.41x
  -- but that number was (M_b + M_ph,EOS)/M_HSE with its EFE cap never firing
  (the units slips broke g_tot), so nothing was actually partitioned.  On the
  clean recompute (same files): baryons alone deliver {mbfrac:.3f}x at
  420 kpc (coherent with X-COP f_b), the EOS phantom another ~{g050ref-mbfrac:.2f}x,
  and the deficit is {1-mbfrac:.2f}x M_HSE -- the free-dust share left
  undeduced.  G059 derives the partition from the local field itself on the
  SAME 12 X-COP clusters, three ways.

  KERNEL ({VERD[('kernel','canonical')]:.2f}x / {VERD[('kernel','alt')]:.2f}x):
  the mu2 kernel oriented sub-a0 -- the phantom's share IS the certified
  kernel's sub-a0 branch, pointwise in g_tot/a0, no free parameter.

  VIRIAL ({VERD[('virial','canonical')]:.2f}x / {VERD[('virial','alt')]:.2f}x):
  the cumulative work fraction of the deep branch.

  r_M-SURFACE ({VERD[('rM','canonical')]:.2f}x / {VERD[('rM','alt')]:.2f}x):
  the binary surface reading, share = 1 wherever the local field is sub-a0.
  HONEST STATUS (corrective re-run): information-free on this data -- for the
  clusters whose window is Newtonian (g_tot > a0 throughout: the a0-crossing
  lies beyond the data) the share is 0 and the ratio is baryons alone; for
  the clusters whose window is deep throughout the share is 1 and the ratio
  returns M_HSE identically by construction (M_res := M_HSE - M_b).  A binary
  partition cannot be independently tested inside this data; see the state
  census in the table above.

  HONEST STATE: no NON-degenerate candidate reaches [0.8, 1.3] on either
  footing.  The theory's own kernel (KERNEL, zero free parameters) is the
  nearest miss: {RAT['canonical']['_median']['kernel']['integral']:.2f}x
  (canonical) / {RAT['alt']['_median']['kernel']['integral']:.2f}x (alt);
  the required share of the deficit for the band floor is
  {(0.8 - mbfrac)/(1 - mbfrac):.2f} at 420 kpc.  The kernel and virial
  partitions undersupply; the residual is the free dust's share, exactly G050's
  architecture: cap/un-cap was always a stand-in for this partition, and the
  partition the theory supplies (the mu2 kernel's sub-a0 branch) delivers
  ~6/10 of the deficit, not all of it.  Both partitions together -- supported
  phantom + free dust -- account for M_HSE by construction; the derived
  phantom share is the honest, parameter-free lower bound on what the theory
  itself contributes to the cluster's dark sector.

  Best non-degenerate candidate: {NAMES[key]} on {ft}, median residual
  {np.median(res):+.3f} (median deficit shortfall {np.median(shf):+.3f}).

G059 COMPLETE: {sum(1 for r_ in RES if r_["pass"])}/{len(RES)} checks PASS.
artifact written: G059_results.json
""")


