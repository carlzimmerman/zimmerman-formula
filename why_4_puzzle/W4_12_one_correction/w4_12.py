#!/usr/bin/env python3
"""W4-12 -- can one universal stellar-mass factor k and gas-mass factor f reconcile the four kappa facts?
F1 gas-RC kappa (p64 B E2), F2 blue lenses (W4-06), F3 within-galaxy gas-vs-star Delta_g (p64 A), F4 red vs blue lenses (W4-10).

Criteria: FROZEN_CRITERIA.md (committed alone, fb52868b4). p64's functions are copied (K1 checks them against p64's numbers);
W4-06's loader is imported and its chi2(kappa) is vectorised over the same grid (K1 checks blue 0.520 / red 1.293).
Light: numpy, one process. Run from the repo root:
    OMP_NUM_THREADS=1 nice -n 10 python3 why_4_puzzle/W4_12_one_correction/w4_12.py > why_4_puzzle/W4_12_one_correction/w4_12.out
    W4_12_MUTATE=1 ... > .../w4_12_MUTATE.out    (M1 mock early-type IMF; M2 mock radial M/L; exit 1 when they bite)
kappa = 1/2 FITTED. Not theory closed.
"""
import contextlib, importlib.util, io, json, math, os, sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, os.path.join(REPO, "campaign_fresh_gravity"))
with contextlib.redirect_stdout(io.StringIO()):
    import CFG4_common as C
spec = importlib.util.spec_from_file_location("w4_06", os.path.join(REPO, "why_4_puzzle", "W4_06_lensing_kappa", "w4_06.py"))
w6 = importlib.util.module_from_spec(spec); spec.loader.exec_module(w6)
MUT = os.environ.get("W4_12_MUTATE") == "1"
SUF = "_MUTATE" if MUT else ""
KPC = 3.0857e19
S_RHO = w6.S["rho_DE"]                         # c sqrt(G rho_L), the same s for every fact
OUT, checks = [], []


def P(s=""):
    print(s); OUT.append(str(s))


def check(name, detail, ok):
    checks.append({"name": name, "detail": detail, "pass": bool(ok)})
    P(f"[{'PASS' if ok else 'FAIL'}] {name}: {detail}")


# ---------------------------------------------------------------- p64's functions (copied; K1 checks them)
def accel(g, U=0.5, fgas=1.0, star_boost=None):
    R = g["R"] * KPC
    vs2 = U * g["Vdisk"] ** 2 + 1.4 * U * g["Vbul"] ** 2
    if star_boost is not None:
        vs2 = vs2 * star_boost
    gb = (fgas * np.sign(g["Vgas"]) * g["Vgas"] ** 2 + vs2) * 1e6 / R
    go = (g["Vobs"] * 1e3) ** 2 / R
    return go, gb


def classes(g):
    vg2 = np.sign(g["Vgas"]) * g["Vgas"] ** 2
    vs2 = 0.5 * g["Vdisk"] ** 2 + 0.7 * g["Vbul"] ** 2
    vb2 = vg2 + vs2
    ok = (vb2 > 0) & (g["Vobs"] > 0) & (g["R"] > 0)
    return ok & (vg2 >= 0.7 * vb2), ok & (vs2 >= 0.7 * vb2)


def la_pts(g, mask, U=0.5, fgas=1.0, star_boost=None):
    go, gb = accel(g, U, fgas, star_boost)
    m = mask & (gb > 0) & (go > gb)
    return np.log10(go[m] * (go[m] - gb[m]) / gb[m])


def sel_points(g):
    vg2 = np.sign(g["Vgas"]) * g["Vgas"] ** 2
    vb2 = vg2 + 0.5 * g["Vdisk"] ** 2 + 0.7 * g["Vbul"] ** 2
    return (vg2 >= 0.7 * vb2) & (vb2 > 0) & (g["Vobs"] > 0)


GAL = [g for g in C.load_sparc() if g["meta"]]
A_S = []
for g in GAL:
    if g["meta"]["Q"] > 2 or g["meta"]["Inc"] < 30:
        continue
    gm, sm = classes(g)
    if len(la_pts(g, gm)) >= 3 and len(la_pts(g, sm)) >= 3:
        A_S.append((g, gm, sm))
S0 = [g for g in GAL if g["meta"]["Q"] <= 2 and g["meta"]["fD"] in (2, 3, 5) and sel_points(g).sum() >= 3]


def F3(U, fgas, nb=500, mut_m2=False):
    dg = []
    for g, gm, sm in A_S:
        boost = None
        if mut_m2:                                        # M2: star-dominated points' stellar terms x 10^0.43
            boost = np.where(sm, 10 ** 0.43, 1.0)
        a, b = la_pts(g, gm, U, fgas, boost), la_pts(g, sm, U, fgas, boost)
        if len(a) >= 2 and len(b) >= 2:
            dg.append(float(np.median(a) - np.median(b)))
    dg = np.array(dg)
    rng = np.random.default_rng(64)
    bs = [np.median(dg[rng.integers(0, len(dg), len(dg))]) for _ in range(nb)]
    return float(np.median(dg)), float(np.std(bs)), len(dg)


def F1(U, fgas, nb=500):
    per = np.array([float(np.median(la_pts(g, sel_points(g), U, fgas))) for g in S0])
    rng = np.random.default_rng(64)
    bs = [np.median(per[rng.integers(0, len(per), len(per))]) for _ in range(nb)]
    return float(np.median(per)), float(np.std(bs))


# ---------------------------------------------------------------- lensing, vectorised chi2 over W4-06's grid
LENS = {"blue": w6.load(*w6.BLUE), "red": w6.load("Fig-8_RAR-KiDS-isolated_Colorbin_2.txt",
                                                   "Fig-8_RAR-KiDS-isolated_Colorbins_covmatrix.txt", 2.5)}
if MUT:
    gb, go, Cm = LENS["red"]
    LENS["red"] = (gb * 10 ** 0.4, go, Cm)                # M1: mock early-type IMF on red lenses


def fit_vec(gb, go, Cm):
    m = (gb >= w6.W[0]) & (gb < w6.W[1])
    if m.sum() < 3:
        return None
    Ci = np.linalg.inv(Cm[np.ix_(m, m)])
    g, o = gb[m], go[m]
    K = w6.KGRID[:, None]
    model = g[None, :] * w6.nu_s(g[None, :] / (K * S_RHO))
    r = o[None, :] - model
    chi = np.einsum("ki,ij,kj->k", r, Ci, r)
    i = int(np.argmin(chi)); cmin = chi[i]
    left = np.where(chi[:i] >= cmin + 1)[0]; right = np.where(chi[i:] >= cmin + 1)[0]
    if len(left) == 0 or len(right) == 0 or i in (0, len(chi) - 1):
        return None
    lo, hi = w6.KGRID[left[-1]], w6.KGRID[i + right[0]]
    k = float(w6.KGRID[i])
    return k, 0.5 * (math.log10(hi) - math.log10(lo))   # kappa, sigma in dex


def lens_kappa(name, k, f, S):
    gb, go, Cm = LENS[name]
    return fit_vec(gb * (S * k + (1 - S) * f), go, Cm)


# ---------------------------------------------------------------- K1 identities
P("W4-12  one universal correction (k stellar, f gas) for the four kappa facts?" + ("  [MUTATE: M1 red IMF x10^0.4; M2 star points x10^0.43]" if MUT else ""))
P("obs lane. kappa = 1/2 FITTED. Not theory closed.\n")
d0, s0, n0 = F3(0.5, 1.0, nb=2000)
e0, _ = F1(0.5, 1.0)
b0 = lens_kappa("blue", 1, 1, 1.0)
r0 = fit_vec(*w6.load("Fig-8_RAR-KiDS-isolated_Colorbin_2.txt", "Fig-8_RAR-KiDS-isolated_Colorbins_covmatrix.txt", 2.5))
check("K1 p64 fiducial Delta_g and E2 reproduced", f"Delta_g {d0:+.4f} (p64 -0.408, n {n0}), E2 {e0:+.4f} (p64 -9.9816)",
      abs(d0 + 0.408) < 1e-3 and abs(e0 + 9.9816) < 1e-3)
check("K1 W4-06/W4-10 lensing reproduced (vectorised)", f"blue {b0[0]:.3f} (0.520), red (unmutated) {r0[0]:.3f} (1.293)",
      abs(b0[0] - 0.520) < 2e-3 and abs(r0[0] - 1.293) < 2e-3)

LK = np.round(np.arange(-0.2, 0.6001, 0.05), 3)
LF = np.round(np.arange(-0.6, 0.2001, 0.05), 3)
maps, cells = {}, []
for S in (1.0, 0.7):
    c1 = np.zeros((len(LK), len(LF)), bool); c2 = c1.copy(); c3 = c1.copy()
    for i, lk in enumerate(LK):
        for j, lf in enumerate(LF):
            k, f = 10 ** lk, 10 ** lf
            if S == 1.0:                                    # SPARC facts do not depend on S
                d, sd, _ = F3(0.5 * k, f, mut_m2=MUT)
                e, se = F1(0.5 * k, f)
                cells.append(dict(lk=float(lk), lf=float(lf), d=d, sd=sd, e=e, se=se))
            cell = next(x for x in cells if x["lk"] == float(lk) and x["lf"] == float(lf))
            bl, rd = lens_kappa("blue", k, f, S), lens_kappa("red", k, f, S)
            cell[f"blue_S{S}"] = bl; cell[f"red_S{S}"] = rd
            c1[i, j] = abs(cell["d"]) < 2 * cell["sd"]
            kF1 = 10 ** cell["e"] / S_RHO
            if bl is not None:
                c2[i, j] = abs(math.log10(kF1) - math.log10(bl[0])) < 2 * math.hypot(cell["se"], bl[1])
                if rd is not None:
                    c3[i, j] = abs(math.log10(rd[0]) - math.log10(bl[0])) < 2 * math.hypot(rd[1], bl[1])
    maps[S] = (c1, c2, c3)


def show(mask, title):
    P(f"  {title}   (rows log k {LK[0]:+.2f}..{LK[-1]:+.2f}, cols log f {LF[0]:+.2f}..{LF[-1]:+.2f}; '#' = pass)")
    for i, lk in enumerate(LK):
        P(f"    {lk:+.2f} " + "".join("#" if mask[i, j] else "." for j in range(len(LF))))


P("")
verdicts = {}
for S, (c1, c2, c3) in maps.items():
    P(f"lens stellar share S = {S}")
    show(c1, "C1 within-galaxy gap closes"); show(c2, "C2 gas-RC kappa = blue-lens kappa"); show(c3, "C3 red/blue split closes")
    allc = c1 & c2 & c3
    plaus = np.array([[0.8 <= 10 ** lk <= 1.6 and 0.85 <= 10 ** lf <= 1.15 for lf in LF] for lk in LK])
    best12 = np.argwhere(c1 & c2); best23 = np.argwhere(c2 & c3)
    verdicts[S] = dict(all=bool(allc.any()), all_plausible=bool((allc & plaus).any()), c3_any=bool(c3.any()),
                       c1c2=[(float(LK[i]), float(LF[j])) for i, j in best12][:10], c2c3=[(float(LK[i]), float(LF[j])) for i, j in best23][:10])
    P(f"  C1&C2&C3 anywhere: {verdicts[S]['all']} (plausible region: {verdicts[S]['all_plausible']}); C3 anywhere: {verdicts[S]['c3_any']}")
    P(f"  C1&C2 cells (log k, log f): {verdicts[S]['c1c2'] or 'none'}")
    P(f"  C2&C3 cells: {verdicts[S]['c2c3'] or 'none'}")
    # frozen report: the best C1&C2 cell (reading: the cell closest to k = f = 1 in (log k, log f)), kappa_F1 there, 1/2 within 2 sigma?
    if len(best12):
        i, j = min(best12, key=lambda ij: math.hypot(LK[ij[0]], LF[ij[1]]))
        cb = next(x for x in cells if x["lk"] == float(LK[i]) and x["lf"] == float(LF[j]))
        kF1 = 10 ** cb["e"] / S_RHO
        lo2, hi2 = 10 ** (cb["e"] - 2 * cb["se"]) / S_RHO, 10 ** (cb["e"] + 2 * cb["se"]) / S_RHO
        plaus_b = bool(plaus[i, j])
        verdicts[S]["best_c1c2"] = dict(lk=float(LK[i]), lf=float(LF[j]), k=float(10 ** LK[i]), f=float(10 ** LF[j]), kappa_F1=kF1,
                                        half_in_2sigma=bool(lo2 <= 0.5 <= hi2), plausible=plaus_b, blue=cb[f"blue_S{S}"])
        P(f"  best C1&C2 cell (closest to k = f = 1): k {10 ** LK[i]:.2f} (Upsilon_d {0.5 * 10 ** LK[i]:.2f}), f {10 ** LF[j]:.2f}; "
          f"plausible region {plaus_b}; kappa_F1 {kF1:.3f} [2 sigma {lo2:.3f}-{hi2:.3f}] -> 1/2 {'inside' if lo2 <= 0.5 <= hi2 else 'outside'}; "
          f"blue-lens kappa {cb[f'blue_S{S}'][0]:.3f}")
    P("")
fid = next(x for x in cells if x["lk"] == 0.0 and x["lf"] == 0.0)
P(f"fiducial cell (k = f = 1): Delta_g {fid['d']:+.3f} +- {fid['sd']:.3f}; kappa_F1 {10 ** fid['e'] / S_RHO:.3f}; "
  f"blue {fid['blue_S1.0'][0]:.3f}; red {fid['red_S1.0'][0] if fid['red_S1.0'] else float('nan'):.3f}")
one = all(v["all"] for v in verdicts.values())
lane = "ONE CORRECTION FITS ALL" if one else "NO SINGLE CORRECTION"
P(f"LANE VERDICT: {lane}")
json.dump(dict(mutate=MUT, LK=LK.tolist(), LF=LF.tolist(), cells=cells, verdicts={str(k): v for k, v in verdicts.items()},
               maps={str(S): [m.tolist() for m in v] for S, v in maps.items()}, lane_verdict=lane, checks=checks),
          open(os.path.join(HERE, f"w4_12_results{SUF}.json"), "w"), indent=1, default=float)
P(f"\nchecks: {sum(c['pass'] for c in checks)}/{len(checks)} pass")
if MUT:
    try:
        base = json.load(open(os.path.join(HERE, "w4_12_results.json")))
        c3_base = any(v["c3_any"] for v in base["verdicts"].values())
        c1_base = np.array(base["maps"]["1.0"][0])
        c1_mut = maps[1.0][0]
        m1 = any(v["c3_any"] for v in verdicts.values()) and not c3_base
        i0, j0 = int(np.where(LK == 0.0)[0][0]), int(np.where(LF == 0.0)[0][0])
        m2 = bool(c1_mut[i0, j0]) and not bool(c1_base[i0, j0])
        P(f"MUTATE: M1 (mock early-type IMF) makes C3 passable {m1}; M2 (mock radial M/L) closes C1 at k = f = 1 {m2}")
        sys.exit(1 if (m1 and m2) else 2)
    except OSError:
        sys.exit(2)
sys.exit(0 if all(c["pass"] for c in checks) else 1)
