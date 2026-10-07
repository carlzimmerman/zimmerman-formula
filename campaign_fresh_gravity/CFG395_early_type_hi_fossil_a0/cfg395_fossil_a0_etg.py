#!/usr/bin/env python3
"""CFG395 -- fossil a0 in early-type HI discs (criteria: FROZEN_CRITERIA.md, committed 7ee1f29dc before this script).

Headline: 16 ATLAS3D rotating ETGs, one outer HI point each (V_HI, R_HI from Serra+2016 Table 1 = den Heijer+2015's measurement),
baryons from Lelli+2017's [3.6] luminosity / exponential-disc decomposition at Upsilon_[3.6] = 0.8, against SPARC T >= 8 at matched g_bar.
Residual r = log g_obs - log[nu_mono(g_bar/a0) g_bar]; Delta = median(r_ETG) - median(r_late); both footings.
Secondary arms S1 (SPARC T <= 1), S2 (Di Teodoro+2023 T <= 0), S3 sensitivities: reported only.

Run: python3 cfg395_fossil_a0_etg.py            -> cfg395_fossil_a0_etg.out / _results.json
     python3 cfg395_fossil_a0_etg.py --mutate   -> _MUTATE.out / _MUTATE_results.json (-0.04 dex on every ETG residual; exit 1 when detected)
"""
import os, sys, io, json, math, contextlib
import numpy as np
from scipy.special import i0, i1, k0, k1

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, os.path.join(REPO, "campaign_fresh_gravity"))
with contextlib.redirect_stdout(io.StringIO()):
    import CFG4_common as C          # read-only: nu_mono (FP1) and the SPARC loader
MUT = "--mutate" in sys.argv
TAG = "_MUTATE" if MUT else ""
OUT = []
def P(s=""):
    print(s); OUT.append(str(s))

FOOT = (("canonical", 9.3603e-11), ("alt", 1.1312e-10))
G = 4.30091e-6                       # kpc (km/s)^2 / Msun
KPC = 3.0857e19
ACC = 1e6 / KPC                      # (km/s)^2/kpc -> m/s^2
AS = math.pi / 180 / 3600
UPS_ETG, F_GAS, XHE = 0.8, 0.5, 1.33
NBOOT, SEED = 4000, 395
DATA = os.path.join(REPO, "real_research", "data")
checks = {}

def rd_tsv(p):
    rows, hdr = [], None
    for l in open(p):
        if l.startswith("#") or not l.strip():
            continue
        t = l.rstrip("\n").split("\t")
        if hdr is None:
            hdr = t; continue
        rows.append(dict(zip(hdr, t)))
    return rows

# ------------------------------------------------------------------ ETG input
E = rd_tsv(os.path.join(HERE, "etg16_serra16_lelli17.tsv"))
DH = {r["name"]: r for r in rd_tsv(os.path.join(DATA, "denheijer2015_etg_hi_tfr.tsv"))}
names = [r["name"] for r in E]

# C1: Serra V_HI == den Heijer v_circ
c1 = all(n in DH and float(DH[n]["vcirc"]) == float(r["VHI"]) for n, r in zip(names, E))
checks["C1_VHI_equals_denHeijer"] = c1
# C2: R_HI at Cappellari+2011 distances vs den Heijer's stated 8-28 kpc (mean 15), R/Re 3.4-13.7 (mean 7.3)
rk = np.array([float(r["RHI_as"]) * AS * float(DH[r["name"]]["D_Mpc"]) * 1e3 for r in E])
rr = np.array([float(r["RHI_as"]) / float(r["Re_as"]) for r in E])
c2v = dict(Rmin=rk.min(), Rmax=rk.max(), Rmean=rk.mean(), RRmin=rr.min(), RRmax=rr.max(), RRmean=rr.mean())
c2 = (abs(c2v["Rmin"] - 8) <= 0.6 and abs(c2v["Rmax"] - 28) <= 0.6 and abs(c2v["Rmean"] - 15) <= 0.6 and
      abs(c2v["RRmin"] - 3.4) <= 0.15 and abs(c2v["RRmax"] - 13.7) <= 0.15 and abs(c2v["RRmean"] - 7.3) <= 0.15)
checks["C2_RHI_reproduces_denHeijer_ranges"] = c2

L = np.array([float(r["L36"]) * 1e9 for r in E])
Rd = np.array([float(r["Rd_kpc"]) for r in E])
Sd = np.array([float(r["SBd"]) * 1e6 for r in E])            # Lsun/kpc^2
Ld_raw = 2 * math.pi * Sd * Rd ** 2
c3_bad = [n for n, a, b in zip(names, Ld_raw, L) if a > b]
checks["C3_disc_luminosity_le_total"] = len(c3_bad) == 0
Ld = np.minimum(Ld_raw, L)                                    # declared departure if C3 fails: cap the disc at the total
Lb = L - Ld
Reff = np.array([float(r["Reff_kpc"]) for r in E])

def etg_points(dist="lelli", ups=UPS_ETG, fgas=F_GAS, bulge="hernquist", model="lelli"):
    D = np.array([float(r["D"]) for r in E]) if dist == "lelli" else np.array([float(DH[r["name"]]["D_Mpc"]) for r in E])
    Dl = np.array([float(r["D"]) for r in E])
    R = np.array([float(r["RHI_as"]) for r in E]) * AS * D * 1e3
    V = np.array([float(r["VHI"]) for r in E])
    gobs = V ** 2 / R * ACC
    s = (D / Dl) ** 2                                          # luminosities scale as D^2 when the distance changes
    Dc = np.array([float(DH[r["name"]]["D_Mpc"]) for r in E])
    Mgas = XHE * 10 ** np.array([float(DH[r["name"]]["logMHI"]) for r in E]) * (D / Dc) ** 2
    if model == "lelli":
        Rds = Rd * D / Dl
        y = R / (2 * Rds)
        Md = ups * Ld * s
        Sig0 = Md / (2 * math.pi * Rds ** 2)
        v2d = 4 * math.pi * G * Sig0 * Rds * y ** 2 * (i0(y) * k0(y) - i1(y) * k1(y))
        Mb = ups * Lb * s
        if bulge == "hernquist":
            a = Reff * D / Dl / 1.8153
            gb = G * Mb / (R + a) ** 2
        else:
            gb = G * Mb / R ** 2
        gbar = (v2d / R + gb + G * fgas * Mgas / R ** 2) * ACC
    else:                                                      # S3: ATLAS3D r-band L x (M/L)_SFH x 10^-0.25, point mass
        Lr = 10 ** np.array([float(DH[r["name"]]["logLr"]) for r in E]) * (D / Dc) ** 2
        ML = 10 ** (np.array([float(DH[r["name"]]["logML_SFH"]) for r in E]) - 0.25)
        gbar = (G * (ML * Lr + fgas * Mgas) / R ** 2) * ACC
    return gbar, gobs

def resid(gbar, gobs, a0):
    return np.log10(gobs) - np.log10(C.nu_mono(gbar / a0) * gbar)

# ------------------------------------------------------------------ SPARC
with contextlib.redirect_stdout(io.StringIO()):
    SP = [g for g in C.load_sparc() if g["meta"] and g["meta"]["Q"] <= 2]

def sparc_pts(sel, ud=0.5, ub=0.7):
    out = []
    for g in SP:
        if not sel(g["meta"]["T"]):
            continue
        R = g["R"]
        vb2 = np.sign(g["Vgas"]) * g["Vgas"] ** 2 + ud * g["Vdisk"] ** 2 + ub * g["Vbul"] ** 2
        gb = vb2 / R * ACC; go = g["Vobs"] ** 2 / R * ACC
        ok = (R > 0) & (gb > 0) & (go > 0)
        out.append((g["name"], gb[ok], go[ok]))
    return out

# C4: session-06 count (T >= 8 with >= 3 gas-dominated deep points)
n4 = 0
for g in SP:
    if g["meta"]["T"] < 8:
        continue
    R = g["R"] * KPC; vg2 = np.sign(g["Vgas"]) * g["Vgas"] ** 2
    vb2 = vg2 + 0.5 * g["Vdisk"] ** 2 + 0.7 * g["Vbul"] ** 2
    b = vb2 * 1e6 / R; o = (g["Vobs"] * 1e3) ** 2 / R
    ok = (b > 0) & (o > 0) & (np.log10(np.where(b > 0, b, 1)) < -10.5) & (vg2 >= 0.7 * vb2)
    n4 += int(ok.sum() >= 3)
checks["C4_session06_late_count_27"] = (n4 == 27)

def late_window(lo, hi, a0, ud=0.5, ub=0.7):
    gals = []
    for n, gb, go in sparc_pts(lambda T: T >= 8, ud, ub):
        m = (gb >= lo) & (gb <= hi)
        if m.sum():
            gals.append(resid(gb[m], go[m], a0))
    return gals

def boot_delta(re_list, rl_list, rng):
    """re_list, rl_list: lists of per-galaxy residual arrays; galaxies resampled independently."""
    ne, nl = len(re_list), len(rl_list)
    bs = np.empty(NBOOT)
    for i in range(NBOOT):
        a = np.concatenate([re_list[j] for j in rng.integers(0, ne, ne)])
        b = np.concatenate([rl_list[j] for j in rng.integers(0, nl, nl)])
        bs[i] = np.median(a) - np.median(b)
    return float(np.std(bs))

def shift(gbar, a0, f):
    return np.log10(C.nu_mono(gbar / (f * a0))) - np.log10(C.nu_mono(gbar / a0))

def verdict(d, s):
    if s > 0.02:
        return "NON-DISCRIMINATING"
    if d < -0.02 and (d + 0.02) / s < -2:
        return "SLOW-SETTLING HINT"
    if d > -0.02 and (d + 0.02) / s > 2:
        return "FAST/NO FOSSIL"
    return "INCONCLUSIVE"

MUTSH = -0.04 if MUT else 0.0
RES = {"checks": None, "C2_values": c2v, "C3_capped": c3_bad, "C4_count": n4, "footings": {}}
P("CFG395 -- fossil a0 in early-type HI discs" + ("  [MUTATE: -0.04 dex on ETG residuals]" if MUT else ""))
P(f"C1 V_HI(Serra16) == v_circ(denHeijer15) all 16: {c1}")
P("C2 R_HI at Cappellari+11 distances: R %.1f-%.1f kpc (mean %.1f) vs 8-28 (15); R/Re %.2f-%.2f (mean %.2f) vs 3.4-13.7 (7.3): %s"
  % (c2v["Rmin"], c2v["Rmax"], c2v["Rmean"], c2v["RRmin"], c2v["RRmax"], c2v["RRmean"], c2))
P(f"C3 L_disc <= L_total for all 16: {len(c3_bad) == 0}" + (f"  (exceeds: {', '.join(c3_bad)}; disc capped at L, bulge 0 -- disclosed departure)" if c3_bad else ""))
P(f"C4 session-06 late count (T>=8, >=3 gas-dominated deep points): {n4} (expect 27): {n4 == 27}")

for foot, a0 in FOOT:
    rng = np.random.default_rng(SEED)
    gb0, go0 = etg_points()
    lo, hi = gb0.min(), gb0.max()
    rE = resid(gb0, go0, a0) + MUTSH
    late = late_window(lo, hi, a0)
    rL = np.concatenate(late)
    d = float(np.median(rE) - np.median(rL))
    sb = boot_delta([np.array([x]) for x in rE], late, rng)
    def dE(**kw):
        gb, go = etg_points(**kw); return float(np.median(resid(gb, go, a0) + MUTSH) - np.median(rL))
    sml_e = abs(dE(ups=UPS_ETG * 10 ** 0.1) - dE(ups=UPS_ETG * 10 ** -0.1)) / 2
    lp = np.concatenate(late_window(lo, hi, a0, 0.5 * 10 ** 0.1, 0.7 * 10 ** 0.1))
    lm = np.concatenate(late_window(lo, hi, a0, 0.5 * 10 ** -0.1, 0.7 * 10 ** -0.1))
    sml_l = abs(np.median(lp) - np.median(lm)) / 2
    sgas = abs(dE(fgas=0.0) - dE(fgas=1.0)) / 2
    sbul = abs(d - dE(bulge="point")) / 2
    st = math.sqrt(sb ** 2 + sml_e ** 2 + sml_l ** 2 + sgas ** 2 + sbul ** 2)
    v = verdict(d, st)
    # expected signal at the actual g_bar
    late_gb = np.concatenate([gb[(gb >= lo) & (gb <= hi)] for _, gb, _ in sparc_pts(lambda T: T >= 8)])
    pred = {fl: float(np.median(shift(gb0, a0, 0.87)) - np.median(shift(late_gb, a0, fl))) for fl in (1.00, 1.06)}
    deep = {fl: 0.5 * math.log10(0.87 / fl) for fl in (1.00, 1.06)}
    # sensitivities (S3)
    sens = dict(cappellari_D=dE(dist="cappellari"), sfh_pointmass=dE(model="sfh"), ups_0p6=dE(ups=0.6), ups_1p0=dE(ups=1.0),
                gas0=dE(fgas=0.0), gas1=dE(fgas=1.0), bulge_point=dE(bulge="point"))
    perE = {n: dict(log_gbar=float(np.log10(a)), log_gobs=float(np.log10(b)), r=float(c)) for n, a, b, c in zip(names, gb0, go0, rE)}
    P("")
    P(f"=== {foot} footing, a0 = {a0:.4e} m/s^2")
    P(f"ETG headline: 16 outer HI points, log g_bar {np.log10(lo):.2f} .. {np.log10(hi):.2f} (median {np.median(np.log10(gb0)):.2f}); "
      f"y = g_bar/a0 {np.min(gb0) / a0:.2f}..{np.max(gb0) / a0:.2f}")
    P(f"  median r_ETG {np.median(rE):+.3f}  (spread rms {np.std(rE):.3f})")
    P(f"late (SPARC T>=8, Q<=2) in window: {len(late)} galaxies, {len(rL)} points, median r_late {np.median(rL):+.3f}")
    P(f"Delta = {d:+.3f}   sigma: boot {sb:.3f}, M/L ETG {sml_e:.3f}, M/L late {sml_l:.3f}, gas {sgas:.3f}, bulge {sbul:.3f} -> total {st:.3f}")
    P(f"expected fossil signal at these g_bar: {pred[1.0]:+.3f} (late f=1.00) / {pred[1.06]:+.3f} (late f=1.06); deep limit {deep[1.0]:+.3f} / {deep[1.06]:+.3f}")
    P(f"power: |pred|/sigma {abs(pred[1.0]) / st:.2f}-{abs(pred[1.06]) / st:.2f}; 0.04/sigma {0.04 / st:.2f}")
    P(f"VERDICT ({foot}): {v}   [(Delta+0.02)/sigma = {(d + 0.02) / st:+.2f}]")
    P("  S3 sensitivities (Delta): " + ", ".join(f"{k} {x:+.3f}" for k, x in sens.items()))
    # ---------- S1: SPARC T <= 1
    s1 = []
    for n, gb, go in sparc_pts(lambda T: T <= 1):
        m = gb < 10 ** -10.5
        if m.sum():
            s1.append((n, gb[m], go[m]))
    s1r = [resid(gb, go, a0) for _, gb, go in s1]
    s1g = np.concatenate([gb for _, gb, _ in s1])
    l1 = late_window(s1g.min(), s1g.max(), a0)
    d1 = float(np.median(np.concatenate(s1r)) - np.median(np.concatenate(l1)))
    sb1 = boot_delta(s1r, l1, np.random.default_rng(SEED + 1))
    def d1ml(f):
        rr_ = []
        for n, gb, go in sparc_pts(lambda T: T <= 1, 0.5 * f, 0.7 * f):
            m = gb < 10 ** -10.5
            if m.sum():
                rr_.append(resid(gb[m], go[m], a0))
        return np.median(np.concatenate(rr_))
    sm1 = abs(d1ml(10 ** 0.1) - d1ml(10 ** -0.1)) / 2
    st1 = math.sqrt(sb1 ** 2 + sm1 ** 2 + sml_l ** 2)
    P(f"S1 SPARC T<=1 (S0-Sa), g_bar<10^-10.5: {len(s1)} galaxies ({', '.join(n for n, _, _ in s1)}), {len(s1g)} points; "
      f"late {len(l1)} gal; Delta {d1:+.3f}  sigma boot {sb1:.3f}, M/L {sm1:.3f}(+late {sml_l:.3f}) -> {st1:.3f}  [reported only]")
    # ---------- S2: Di Teodoro+2023 T <= 0
    MS = {r["name"]: r for r in rd_tsv(os.path.join(DATA, "diteodoro2023_massive_spirals.tsv"))}
    MO = {r["name"]: r for r in rd_tsv(os.path.join(DATA, "diteodoro2023_morphology.tsv"))}
    RC = rd_tsv(os.path.join(DATA, "diteodoro2023_hi_rotation_curves.tsv"))
    keyR, keyV = [k for k in RC[0] if k != "name"][:2]
    s2, s2n = [], []
    BIAS_ACC = 2 * 0.076                                      # CFG41's bias is in log v; in log g it is twice that
    for n in MS:
        T = MO[n]["T"]
        if T == "nan" or float(T) > 0:
            continue
        M = 10 ** float(MS[n]["logMs_W1"]) + 10 ** float(MS[n]["logMgas"])
        R = np.array([float(r[keyR]) for r in RC if r["name"] == n]); V = np.array([float(r[keyV]) for r in RC if r["name"] == n])
        gb = G * M / R ** 2 * ACC; go = V ** 2 / R * ACC
        m = gb < 10 ** -10.5
        if m.sum():
            s2.append(resid(gb[m], go[m], a0) - BIAS_ACC); s2n.append((n, int(m.sum())))
    s2g = []
    for n, _ in s2n:
        M = 10 ** float(MS[n]["logMs_W1"]) + 10 ** float(MS[n]["logMgas"])
        R = np.array([float(r[keyR]) for r in RC if r["name"] == n]); gb = G * M / R ** 2 * ACC
        s2g.append(gb[gb < 10 ** -10.5])
    s2g = np.concatenate(s2g)
    l2 = late_window(s2g.min(), s2g.max(), a0)
    d2 = float(np.median(np.concatenate(s2)) - np.median(np.concatenate(l2))) if l2 else float("nan")
    sb2 = boot_delta(s2, l2, np.random.default_rng(SEED + 2)) if l2 else float("nan")
    st2 = math.sqrt(sb2 ** 2 + (0.5 * 0.2) ** 2 + (2 * 0.030) ** 2 + sml_l ** 2)   # deep-limit 0.5 x 0.2 dex M*; bias error x2
    P(f"S2 Di Teodoro T<=0, g_bar<10^-10.5: {s2n}; log g_bar {np.log10(s2g.min()):.2f}..{np.log10(s2g.max()):.2f}; late {len(l2)} gal; "
      f"Delta {d2:+.3f} (after -{BIAS_ACC:.3f} selection bias)  sigma boot {sb2:.3f}, M* ~0.100, bias 0.060 -> {st2:.3f}  [reported only]")
    RES["footings"][foot] = dict(a0=a0, n_etg=16, n_late_gal=len(late), n_late_pts=int(len(rL)), log_gbar_window=[float(np.log10(lo)), float(np.log10(hi))],
                                 median_etg=float(np.median(rE)), median_late=float(np.median(rL)), delta=d,
                                 sigma=dict(boot=sb, ml_etg=sml_e, ml_late=float(sml_l), gas=sgas, bulge=sbul, total=st),
                                 pred_signal=pred, deep_limit=deep, power_pred=[abs(pred[1.0]) / st, abs(pred[1.06]) / st], power_004=0.04 / st,
                                 verdict=v, sensitivities=sens, per_etg=perE,
                                 S1=dict(gals=[n for n, _, _ in s1], n_pts=int(len(s1g)), delta=d1, sigma=st1, sigma_boot=sb1),
                                 S2=dict(gals=s2n, delta=d2, sigma=st2, sigma_boot=sb2, bias_subtracted=BIAS_ACC))

RES["checks"] = checks
P("")
P("checks: " + ", ".join(f"{k}={'PASS' if x else 'FAIL'}" for k, x in checks.items()))
json.dump(RES, open(os.path.join(HERE, f"cfg395_fossil_a0_etg{TAG}_results.json"), "w"), indent=1, default=float)
rc = 0
if MUT:
    base = os.path.join(HERE, "cfg395_fossil_a0_etg_results.json")
    if os.path.exists(base):
        m = json.load(open(base))
        sh = RES["footings"]["canonical"]["delta"] - m["footings"]["canonical"]["delta"]
        det = abs(sh + 0.04) <= 0.005
        P(f"MUTATE: canonical Delta shift {sh:+.4f} (required -0.040 +- 0.005) -> {'DETECTED' if det else 'NOT detected'}")
        rc = 1 if det else 0
    else:
        P("MUTATE: base results missing; run the main script first")
open(os.path.join(HERE, f"cfg395_fossil_a0_etg{TAG}.out"), "w").write("\n".join(OUT) + "\n")
sys.exit(rc)
