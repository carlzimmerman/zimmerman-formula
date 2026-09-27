#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
CFG5 (3/6) -- THE FOSSIL ON SPARC: the RAR (which nu?), the BTFR, the scatter, and a0(z).

WHY.  CFG5_1 derived the cap (the dark field's stress <= a0^2/8piG, written at coherent crossing) and CFG5_2 ran the collapse:
the dark collapse realizes a cap on the dark field's own pull g_cr(M_h) = 0.16-0.46 a0 on galaxy hosts (below the relaxed
0.918 a0), hollows the centre, and, when the galaxy condenses inside, the phase-mixed survivors contract.  Here the fossil is
built around every SPARC galaxy's own baryons and scored against its rotation curve.

THE FOSSIL AROUND A GALAXY (no per-galaxy parameter).
  * The halo the cold dark field forms before the cap acts: NFW, M_h from the declared stellar-to-halo relation at the
    galaxy's M* (Upsilon_d = 0.5, the record's), c from the declared concentration-mass relation.  The SAME halo is the LCDM
    control, so every difference below is the principle's.
  * The cap, written at collapse (inside out, removal only): g_d <= g_cap.  Two readings, both from the record of this lane:
      F_eq : the relaxed (SIS) cap sqrt(1 - f_b) a0 (CFG5_1 P3);
      F_cr : the collapse-realized cap g_cr(M_h) of CFG5_2 H2d (per footing, interpolated in log M_h, flat outside its range).
  * The galaxy condensing inside: none (the same assumption as the plain LCDM control) or adiabatic contraction of the dark
    survivors onto the galaxy's observed baryons (the circular-orbit invariant; the same treatment as the contracted LCDM
    control).  CFG5_2 H2e says the principle's collapse is followed by contraction; F_cr + AC is therefore the principle's
    reading closest to the refined dynamics, and it is the primary.
  * Daughters: every SPARC host is <= ~1e12.5 Msun; the converted mass is removed (CFG5_2 H2b: escape; the bound part at
    1e12-1e12.5 is spread beyond the rotation curves; its return is reported by CFG5_2 and ignored here).
HYPOTHESES (declared before the first committed run; the scratch explorations disclosed in CFG5_1 ran F_eq, F_eq + AC and
the controls, not F_cr).
  H3a  THE RAR: the principle's primary fossil (F_cr + AC) fits the SPARC RAR within 0.02 dex (rms) of nu_RAR's 0.1453 /
       0.1421 on both footings, with no per-galaxy parameter.
  H3b  THE PRINCIPLE IMPROVES ON ITS OWN CONTROL: with the same baryonic response, the fossil's rms is below the LCDM
       control's: F_cr + AC < LCDM + AC and F_eq < LCDM, on both footings.
  H3c  THE DEEP BRANCH IS INHERITED (the design constraint, declared as expected): at y < 0.1 the fossil's median residual
       equals the LCDM control's within 0.02 dex -- the principle does not write the deep branch.
  H3d  THE BTFR: the primary fossil's model BTFR (V_flat from its rotation curve at the data's flat radii) has slope in
       [3.5, 4.5] and zero point a0_eff = median V_f^4/(G M_b) within 0.15 dex of the footing's a0, on both footings.
  H3e  (reported) the tightness: the intrinsic RAR scatter the halo population puts into the fossil (Monte Carlo over the
       declared 0.15 dex stellar-to-halo and 0.11 dex concentration scatter) against the observed residual rms, per y band.
  H3f  (reported) a0(z): the cap is exactly constant (P_c is set by the unimodular Lambda); the BTFR zero point of a model
       population at z = 1 and 2.5 relative to z = 0, fossil and LCDM, against the framework's flat law and the record's
       LCDM number.
CHECKS
  C1 CONTROL [load-bearing]: nu_RAR on the record's loader reproduces 0.1453 / 0.1421 with the charter footings' own values
     printed alongside (the record's 9.3619e-11 / 1.1279e-10 give 0.1453 / 0.1421 exactly -- CFG5_1 C2).
  C2 CONTROL [load-bearing]: CFG5_2's committed realized caps are read (not recomputed) and are finite on both footings.
  H3a-H3d [load-bearing]; H3e, H3f, N (which nu?) reported; W the ledger.
MUTATE=1 sets a0 -> 0 inside the cap: every dark gram converts; H3a must FAIL (rc = 1).

Run from the repository root:  python3 campaign_fresh_gravity/CFG5_3_sparc.py
"""
import os, sys, math, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from scipy.optimize import brentq
import CFG5_common as C

L = C.Lane("CFG5_3_sparc", "CFG5.3")
P, banner, check = L.P, L.banner, L.check
MUT = L.MUTATE
P(__doc__.split("CHECKS")[0].strip())
if MUT:
    P("\n  *** MUTATE=1: a0 -> 0 inside the cap -- H3a must FAIL ***")
FOOT = C.FOOT
A0CAP = {f: (0.0 if MUT else a) for f, a in FOOT.items()}
GAL = C.load_sparc()
GB = np.concatenate([g["gb"] for g in GAL]); GO = np.concatenate([g["go"] for g in GAL])
GID = np.concatenate([np.full(len(g["r"]), i) for i, g in enumerate(GAL)])

# ============================================================================================ C1 / C2
banner("C1  CONTROL: nu_RAR on the record's loader (and on the charter footings)")
c1 = {}
for lab, feet in (("record", C.FOOT_REC), ("charter", FOOT)):
    for f, a0 in feet.items():
        res = np.log10(GO / (GB * C.nu_rar(GB / a0)))
        c1[f"{lab}|{f}"] = (float(np.sqrt(np.mean(res ** 2))), float(np.median(res)))
P("    " + "; ".join(f"{k}: rms {v[0]:.4f}, median {v[1]:+.4f}" for k, v in c1.items()))
L.OUT["numbers"]["C1"] = c1
check("C1 CONTROL: nu_RAR reproduces the record's 0.1453 / 0.1421 on the record's footings (155 galaxies, 2786 points)",
      f"{c1['record|canonical'][0]:.4f} / {c1['record|alt'][0]:.4f}; N = {len(GAL)} / {len(GB)}",
      f"{c1['record|canonical'][0]:.4f}" == "0.1453" and f"{c1['record|alt'][0]:.4f}" == "0.1421" and len(GB) == 2786)
NU_RMS = {f: c1[f"charter|{f}"][0] for f in FOOT}

banner("C2  CONTROL: CFG5_2's committed realized caps (read, not recomputed)")
J2 = json.load(open(os.path.join(C.HERE, "CFG5_2_collapse_results.json")))
H2d = J2["numbers"]["H2d"]
GCR = {}
for f in FOOT:
    ms = sorted((float(k), v["h"]) for k, v in H2d[f].items() if float(k) <= 1.01e13)
    GCR[f] = (np.log10([m for m, _ in ms]), np.array([h for _, h in ms]))
    P(f"    [{f:9s}] g_cr/a0 on galaxy hosts: " + ", ".join(f"{m:.1e}: {h:.3f}" for m, h in ms))
check("C2 CONTROL: CFG5_2's realized caps are read and finite on both footings (galaxy hosts <= 1e13)",
      {f: [round(x, 3) for x in GCR[f][1]] for f in FOOT}, all(np.all(np.isfinite(GCR[f][1])) and len(GCR[f][1]) >= 4 for f in FOOT))


def g_cr(f, Mh):
    x, y = GCR[f]
    return float(np.interp(math.log10(Mh), x, y)) * A0CAP[f]


# ============================================================================================ the fossil around each galaxy
def mb_final_fn(g):
    rr = g["r"]; Mbr = g["gb"] * rr ** 2 / C.G
    Mb_tot = max(g["Mb"] * C.MSUN, Mbr[-1])

    def f_(r):
        r = np.asarray(r, float)
        inside = np.interp(r, rr, Mbr)
        inside = np.where(r < rr[0], Mbr[0] * (r / rr[0]) ** 2, inside)
        outer = Mb_tot - (Mb_tot - Mbr[-1]) * (rr[-1] / np.maximum(r, rr[-1]))
        return np.where(r > rr[-1], outer, inside)
    return f_


def fossil_models(g, f, Mh=None, c=None, which=("LCDM", "LCDM+AC", "F_eq", "F_eq+AC", "F_cr", "F_cr+AC")):
    """g_obs model at the galaxy's radii for each variant [m/s^2]."""
    Ms = C.UPS_D * g["L36"] * 1e9
    Mh = C.mh_of_ms(Ms) if Mh is None else Mh
    halo = C.nfw_halo(Mh, 0.0, c)
    R = np.geomspace(0.01 * C.KPC, halo["r200"], 900)
    Mtot0 = halo["M_of"](R)
    Md0 = (1 - C.F_B) * Mtot0
    Mbf = mb_final_fn(g)
    Mb_diffuse = g["Mb"] * C.MSUN * Mtot0 / Mtot0[-1]
    rr = g["r"]
    out = {}

    def at(Rd, Md):
        return g["gb"] + C.G * np.interp(rr, Rd, Md, left=0.0) / rr ** 2
    caps = {"eq": C.g_cap(A0CAP[f]), "cr": g_cr(f, Mh)}
    for w in which:
        if w == "LCDM":
            out[w] = at(R, Md0)
        elif w == "LCDM+AC":
            out[w] = at(*C.blumenthal(R, Md0, Mb_diffuse, Mbf))
        else:
            cap = caps["eq" if "eq" in w else "cr"]
            Mc = C.cap_inside_out(R, Md0, cap * R ** 2 / C.G)
            out[w] = at(*C.blumenthal(R, Mc, Mb_diffuse, Mbf)) if w.endswith("+AC") else at(R, Mc)
    return out, Mh, halo["c"]


banner("RUNS  the fossil variants around all 155 galaxies, both footings")
VARS = ("LCDM", "LCDM+AC", "F_eq", "F_eq+AC", "F_cr", "F_cr+AC")
PRED = {f: {v: [] for v in VARS} for f in FOOT}
MHC = []
for f in FOOT:
    for i, g in enumerate(GAL):
        o, Mh, cc = fossil_models(g, f)
        for v in VARS:
            PRED[f][v].append(o[v])
        if f == "canonical":
            MHC.append((Mh, cc))
    P(f"    [{f}] done   {L.el()}")
STATS = {}
for f in FOOT:
    a0 = FOOT[f]; y = GB / a0
    for v in VARS:
        pr = np.concatenate(PRED[f][v]); res = np.log10(GO / pr)
        bins = {}
        for lab, s in (("y<0.1", y < 0.1), ("0.1-1", (y >= 0.1) & (y < 1)), ("1-5", (y >= 1) & (y < 5)), (">5", y >= 5)):
            bins[lab] = float(np.median(res[s]))
        STATS[f"{f}|{v}"] = dict(rms=float(np.sqrt(np.mean(res ** 2))), median=float(np.median(res)), bins=bins)
    P(f"\n    [{f:9s}] nu_RAR: rms {NU_RMS[f]:.4f}")
    for v in VARS:
        s = STATS[f"{f}|{v}"]
        P(f"    [{f:9s}] {v:8s}: rms {s['rms']:.4f}  median {s['median']:+.4f}  | medians y<0.1 / 0.1-1 / 1-5 / >5: "
          + " / ".join(f"{s['bins'][b]:+.3f}" for b in ("y<0.1", "0.1-1", "1-5", ">5")))
L.OUT["numbers"]["stats"] = STATS

# ============================================================================================ H3a
banner("H3a THE RAR: the principle's primary fossil (F_cr + AC) against nu_RAR")
d3a = {f: STATS[f"{f}|F_cr+AC"]["rms"] - NU_RMS[f] for f in FOOT}
check("H3a the primary fossil (F_cr + AC) fits the SPARC RAR within 0.02 dex of nu_RAR's rms on both footings (no per-galaxy "
      "parameter)", {f: f"{STATS[f'{f}|F_cr+AC']['rms']:.4f} vs {NU_RMS[f]:.4f} (d = {d3a[f]:+.4f})" for f in FOOT},
      all(d <= 0.02 for d in d3a.values()))

# ============================================================================================ H3b
banner("H3b THE PRINCIPLE AGAINST ITS OWN LCDM CONTROL (same halos, same baryonic response)")
cmp_ = {f: dict(AC=(STATS[f"{f}|F_cr+AC"]["rms"], STATS[f"{f}|LCDM+AC"]["rms"]),
                none=(STATS[f"{f}|F_eq"]["rms"], STATS[f"{f}|LCDM"]["rms"]),
                none_cr=(STATS[f"{f}|F_cr"]["rms"], STATS[f"{f}|LCDM"]["rms"])) for f in FOOT}
P("    " + "; ".join(f"{f}: AC {v['AC'][0]:.4f} vs {v['AC'][1]:.4f}, no response F_eq {v['none'][0]:.4f} vs {v['none'][1]:.4f} "
                    f"(F_cr {v['none_cr'][0]:.4f})" for f, v in cmp_.items()))
check("H3b with the same baryonic response the fossil beats its LCDM control: F_cr + AC < LCDM + AC and F_eq < LCDM, both footings",
      {f: f"AC {v['AC'][0]:.4f} < {v['AC'][1]:.4f}; none {v['none'][0]:.4f} < {v['none'][1]:.4f}" for f, v in cmp_.items()},
      all(v["AC"][0] < v["AC"][1] and v["none"][0] < v["none"][1] for v in cmp_.values()))

# ============================================================================================ H3c
banner("H3c THE DEEP BRANCH IS INHERITED: y < 0.1 medians, fossil against its LCDM control")
d3c = {}
for f in FOOT:
    for fv, lv in (("F_cr+AC", "LCDM+AC"), ("F_eq", "LCDM"), ("F_cr", "LCDM")):
        d3c[f"{f}|{fv}"] = STATS[f"{f}|{fv}"]["bins"]["y<0.1"] - STATS[f"{f}|{lv}"]["bins"]["y<0.1"]
P("    " + ", ".join(f"{k}: {v:+.4f}" for k, v in d3c.items()))
check("H3c (the design constraint) at y < 0.1 the fossil's median residual equals its LCDM control's within 0.02 dex: the principle "
      "does not write the deep branch", {k: round(v, 4) for k, v in d3c.items()}, all(abs(v) <= 0.02 for v in d3c.values()),
      "the deep branch comes from the cosmological halo population the cold field inherits, not from a0")

# ============================================================================================ N which nu?
banner("N   (reported) WHICH nu?  the fossil's effective nu (binned median g_obs,model/g_bar) against the named kernels")
YB = np.array([0.01, 0.03, 0.1, 0.3, 1.0, 3.0, 10.0, 30.0])
nu_tab = {}
for f in FOOT:
    a0 = FOOT[f]; y = GB / a0
    rows = []
    for lo, hi in zip(YB[:-1], YB[1:]):
        s = (y >= lo) & (y < hi)
        if s.sum() < 10:
            continue
        ym = float(np.median(y[s]))
        row = dict(y=ym, N=int(s.sum()), obs=float(np.median(GO[s] / GB[s])))
        for v in ("LCDM", "F_eq", "F_cr+AC"):
            row[v] = float(np.median(np.concatenate(PRED[f][v])[s] / GB[s]))
        row.update(nu_RAR=float(C.nu_rar(ym)), nu_mono=float(C.nu_mono(ym)), nu_simple=float(C.nu_simple(ym)), P2=float(C.nu_p2(ym)))
        rows.append(row)
    nu_tab[f] = rows
    P(f"    [{f}]   y      obs    LCDM   F_eq  F_cr+AC | nu_RAR nu_mono simple  P2")
    for r in rows:
        P(f"           {r['y']:6.3f} {r['obs']:6.2f} {r['LCDM']:6.2f} {r['F_eq']:6.2f} {r['F_cr+AC']:6.2f} | {r['nu_RAR']:6.2f} "
          f"{r['nu_mono']:6.2f} {r['nu_simple']:6.2f} {r['P2']:5.2f}")
L.OUT["numbers"]["nu_table"] = nu_tab
closest = {}
for f in FOOT:
    dev = {k: float(np.sqrt(np.mean([math.log10(r["F_cr+AC"] / r[k]) ** 2 for r in nu_tab[f]]))) for k in ("nu_RAR", "nu_mono", "nu_simple", "P2")}
    closest[f] = dev
P("    rms log distance of F_cr+AC's effective nu from each kernel: " + "; ".join(f"{f}: " + ", ".join(f"{k} {v:.3f}" for k, v in d.items()) for f, d in closest.items()))
check("N (reported) which nu: the fossil's effective nu is not a universal function; its distance from each named kernel",
      {f: {k: round(v, 3) for k, v in d.items()} for f, d in closest.items()}, True, load_bearing=False)

# ============================================================================================ H3d the BTFR
banner("H3d THE BTFR from the fossil's rotation curves (V_flat at the data's flat radii)")


def vflat_idx(Vo, tol=0.10):
    """L92's rule: the largest outermost run of >= 3 points flat to 10% of its mean."""
    n = len(Vo)
    for k in range(n, 2, -1):
        seg = Vo[n - k:]
        if np.all(np.abs(seg / seg.mean() - 1) <= tol):
            return k
    return 0


btfr = {}
sel_idx = []
for i, g in enumerate(GAL):
    if g["Q"] >= 3 or g["inc"] < 30:
        continue
    k = vflat_idx(g["Vo"])
    if k >= 3:
        sel_idx.append((i, k))
for f in FOOT:
    for lab in ("data", "F_cr+AC", "LCDM", "F_eq"):
        V, Mb = [], []
        for i, k in sel_idx:
            g = GAL[i]
            vv = g["Vo"][-k:] if lab == "data" else np.sqrt(PRED[f][lab][i][-k:] * g["r"][-k:])
            V.append(float(np.mean(vv))); Mb.append(g["Mb"] * C.MSUN)
        V, Mb = np.array(V), np.array(Mb)
        lx, ly = np.log10(V / 1e3), np.log10(Mb / C.MSUN)
        A = np.vstack([lx, np.ones_like(lx)]).T
        (sl, ic), *_ = np.linalg.lstsq(A, ly, rcond=None)
        a0eff = float(10 ** np.median(np.log10(V ** 4 / (C.G * Mb))))
        scat = float(np.std(ly - (sl * lx + ic)))
        btfr[f"{f}|{lab}"] = dict(N=len(V), slope=float(sl), a0_eff=a0eff, dex_from_footing=math.log10(a0eff / FOOT[f]), scatter=scat)
    P(f"    [{f:9s}] " + "; ".join(f"{lab}: slope {btfr[f'{f}|{lab}']['slope']:.2f}, a0_eff {btfr[f'{f}|{lab}']['a0_eff']:.3e} "
                                     f"({btfr[f'{f}|{lab}']['dex_from_footing']:+.3f} dex), scatter {btfr[f'{f}|{lab}']['scatter']:.3f}"
                                     for lab in ("data", "F_cr+AC", "LCDM", "F_eq")))
L.OUT["numbers"]["BTFR"] = btfr
check("H3d the primary fossil's BTFR has slope 3.5-4.5 and a0_eff within 0.15 dex of the footing, both footings",
      {f: f"slope {btfr[f'{f}|F_cr+AC']['slope']:.2f}, {btfr[f'{f}|F_cr+AC']['dex_from_footing']:+.3f} dex" for f in FOOT},
      all(3.5 <= btfr[f"{f}|F_cr+AC"]["slope"] <= 4.5 and abs(btfr[f"{f}|F_cr+AC"]["dex_from_footing"]) <= 0.15 for f in FOOT),
      f"N = {len(sel_idx)} galaxies (Q < 3, i >= 30, a flat outer run); the data's own BTFR on the same V_flat is printed beside it")

# ============================================================================================ H3e tightness (MC)
banner("H3e (reported) THE TIGHTNESS: the halo population's intrinsic RAR scatter in the fossil (canonical footing)")
rng = np.random.default_rng(7)
NREAL = 0 if MUT else 24
sd_pts = [[] for _ in GAL]
for i, g in enumerate(GAL):
    if NREAL == 0:
        break
    Ms = C.UPS_D * g["L36"] * 1e9
    Mh0 = C.mh_of_ms(Ms)
    lm = math.log10(Mh0)
    slope = (math.log10(C.ms_of_mh(10 ** (lm + 0.05))) - math.log10(C.ms_of_mh(10 ** (lm - 0.05)))) / 0.1
    s_mh = 0.15 / max(slope, 0.2)
    c0 = float(C.c200_dm14(Mh0))
    reals = []
    for _ in range(NREAL):
        Mh = 10 ** (lm + s_mh * rng.standard_normal())
        cc = c0 * 10 ** (0.11 * rng.standard_normal())
        o, _, _ = fossil_models(g, "canonical", Mh=Mh, c=cc, which=("F_cr+AC", "LCDM+AC"))
        reals.append((np.log10(o["F_cr+AC"]), np.log10(o["LCDM+AC"])))
    sd_pts[i] = (np.std([r[0] for r in reals], axis=0), np.std([r[1] for r in reals], axis=0))
tight = {}
if NREAL:
    y = GB / FOOT["canonical"]
    sdF = np.concatenate([s[0] for s in sd_pts]); sdL = np.concatenate([s[1] for s in sd_pts])
    resF = np.log10(GO / np.concatenate(PRED["canonical"]["F_cr+AC"]))
    for lab, s in (("y<0.1", y < 0.1), ("0.1-1", (y >= 0.1) & (y < 1)), ("1-5", (y >= 1) & (y < 5)), (">5", y >= 5)):
        tight[lab] = dict(model_intrinsic_F=float(np.sqrt(np.mean(sdF[s] ** 2))), model_intrinsic_LCDM=float(np.sqrt(np.mean(sdL[s] ** 2))),
                          observed_rms_around_F=float(np.sqrt(np.mean(resF[s] ** 2))))
        P(f"    {lab:6s}: intrinsic scatter the halo population puts in (fossil / LCDM+AC) {tight[lab]['model_intrinsic_F']:.3f} / "
          f"{tight[lab]['model_intrinsic_LCDM']:.3f} dex; observed rms around the fossil {tight[lab]['observed_rms_around_F']:.3f} dex")
L.OUT["numbers"]["H3e"] = tight
check("H3e (reported) the fossil's intrinsic scatter from the halo population, per y band, against the observed rms around it",
      {k: f"{v['model_intrinsic_F']:.3f} vs {v['observed_rms_around_F']:.3f}" for k, v in tight.items()}, True, load_bearing=False,
      reading="where the model's intrinsic scatter approaches the observed total, the data leave no room for measurement errors")

# ============================================================================================ H3f a0(z)
banner("H3f (reported) a0(z): the cap is constant; the BTFR zero point of a model population at z = 1 and 2.5")


def model_pop(z, f, variant):
    """a declared model population: M* grid, M_h from the stellar-to-halo relation at z, c(M, z), an exponential disc of
    R_d = 0.012 r200(z) with gas fraction 0.5 (z = 0) rising to 0.7 (z = 2.5) (declared); V_flat = v_c at 4 R_d."""
    out = []
    for lms in np.linspace(9.0, 11.0, 9):
        Ms = 10 ** lms; Mh = C.mh_of_ms(Ms, z)
        halo = C.nfw_halo(Mh, z)
        fg = 0.5 + 0.08 * z
        Mb = Ms / (1 - fg)
        Rd = 0.012 * halo["r200"]
        R = np.geomspace(0.01 * C.KPC, halo["r200"], 900)
        x = R / Rd
        Mb_r = Mb * C.MSUN * (1 - (1 + x) * np.exp(-x))
        Md0 = (1 - C.F_B) * halo["M_of"](R)
        if variant == "F_cr+AC":
            Mc = C.cap_inside_out(R, Md0, g_cr(f, Mh) * R ** 2 / C.G)
        else:
            Mc = Md0
        Mb_diff = Mb * C.MSUN * halo["M_of"](R) / halo["M_of"](R[-1])
        Rd_, Md_ = C.blumenthal(R, Mc, Mb_diff, lambda r: np.interp(r, R, Mb_r))
        rf = 4 * Rd
        v2 = C.G * (np.interp(rf, R, Mb_r) + np.interp(rf, Rd_, Md_)) / rf
        out.append((Mb * C.MSUN, math.sqrt(v2)))
    Mb = np.array([o[0] for o in out]); V = np.array([o[1] for o in out])
    return float(10 ** np.median(np.log10(V ** 4 / (C.G * Mb))))


a0z = {}
for f in FOOT:
    for variant in ("F_cr+AC", "LCDM+AC"):
        z0 = model_pop(0.0, f, variant)
        a0z[f"{f}|{variant}"] = {str(z): math.log10(model_pop(z, f, variant) / z0) for z in (1.0, 2.5)}
    P(f"    [{f:9s}] BTFR zero-point shift [dex] at z = 1 / 2.5: fossil {a0z[f'{f}|F_cr+AC']['1.0']:+.3f} / {a0z[f'{f}|F_cr+AC']['2.5']:+.3f}; "
      f"LCDM {a0z[f'{f}|LCDM+AC']['1.0']:+.3f} / {a0z[f'{f}|LCDM+AC']['2.5']:+.3f}; framework flat law 0.000; a0 ~ H(z): "
      f"{math.log10(C.Ez(1.0)):+.3f} / {math.log10(C.Ez(2.5)):+.3f}")
L.OUT["numbers"]["H3f"] = a0z
check("H3f (reported) a0(z): the cap is exactly constant; the fossil's BTFR zero point evolves with its halo population",
      {k: {z: round(v, 3) for z, v in d.items()} for k, d in a0z.items()}, True, load_bearing=False)

banner("W   THE LEDGER")
L.ledger("L3a", "DERIVED", "the fossil around each SPARC galaxy from the principle, the collapse's realized cap and the declared halo population", "H3a, H3b")
L.ledger("L3b", "CONSTRAINT", "the deep branch (y < 0.1) is the halo population's, not written by a0: the next step must read the baryons", "H3c")
L.ledger("L3c", "DECLARED", "the halo population: stellar-to-halo relation (2013 abundance matching), concentration-mass relation, Upsilon_d = 0.5", "shared with the LCDM control")
L.ledger("L3d", "DECLARED", "the galaxy's response: none or adiabatic contraction (circular-orbit invariant), the same for the fossil and LCDM", "rule 3: same treatment")
check("W the ledger (reported)", f"{len(L.OUT['ledger'])} links", True, load_bearing=False)

banner("VERDICT")
P(f"""  On SPARC (155 galaxies, 2786 points, no per-galaxy parameter) the principle's primary fossil -- the collapse-realized cap,
  then the galaxy condensing inside it -- scores rms {STATS['canonical|F_cr+AC']['rms']:.4f} / {STATS['alt|F_cr+AC']['rms']:.4f} dex (canonical / alt) against nu_RAR's
  {NU_RMS['canonical']:.4f} / {NU_RMS['alt']:.4f}; the same halos without the principle score {STATS['canonical|LCDM+AC']['rms']:.4f} / {STATS['alt|LCDM+AC']['rms']:.4f} with the same
  contraction and {STATS['canonical|LCDM']['rms']:.4f} / {STATS['alt|LCDM']['rms']:.4f} without it.  The deep branch is the halo population's (H3c).  kappa stays
  fitted; nothing here is closed.""")
sys.exit(L.finish())
