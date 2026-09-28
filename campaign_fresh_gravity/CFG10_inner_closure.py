#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
CFG10 -- WHAT SETS THE COLD COMPONENT INSIDE THE BARYONS?  Two zero-constant principles, each exact for a point mass (CFG9),
scored on SPARC with the record's own statistic.

CFG9 showed: around a point mass, a locally virialized cold component with charge K = a0 M / 4 pi IS the law P2; inside
real baryons a constant charge overshoots (the component becomes a central isothermal sphere).  Two principles extend the
point-mass result into the baryons without any new constant (spherical-equivalent baryons, u = r^2 g, u_N = G M_b(<r)):

  (i)  THE PRESSURE GAUSS LAW   4 pi r^2 P = (a0/2) M_b(<r),  i.e.  P = a0 g_N / (8 pi G)  at every radius; Jeans gives
       rho_c = - a0 g_N' / (8 pi G g).  ODE: u u' = u u_N' + a0 r u_N - (a0 r^2 / 2) u_N'.
       It demands NEGATIVE cold density wherever the Newtonian field rises outward (M_b growing faster than r^2).
  (ii) THE SHELL THEOREM FOR THE CHARGE   only the baryons inside r carry charge at r:  rho_c = a0 g_N / (4 pi G r g)
       (= a0 M_b(<r) / (4 pi r^3 g); positive definite).  ODE: u u' = u u_N' + a0 r u_N.
  P2 itself, differentiated: u u' = u_N u_N' + a0 r u_N + (a0 r^2/2) u_N'.  EXACT IDENTITY: P2's phantom density = (ii)'s
       density + rho_b (u_N + a0 r^2/2 - u)/u, and the second term is >= 0 (AM-GM), vanishing where the baryons end.
  All three coincide outside the baryons (u_N' = 0).  Principle (i) subtracts the local term, (ii) omits it, P2 adds it.

THE STATISTIC.  CFG4 H2's (the record's rar_framework_a0_mlfit statistic): weighted rms of log10(g_obs/g_pred) over all 175
SPARC galaxies at one global Upsilon_disk (bulge 1.4 Upsilon), grid 0.30-1.20.  A closure's prediction at a data point is
g_bar(point) + G M_c(<R)/R^2, with the cold mass from its ODE integrated on the monotone envelope of the spherical-
equivalent baryonic mass (inside R_0: V_bar^2 proportional to r, a constant central surface density -- declared).  The fair
baseline is P2 computed in the SAME additive-envelope form ('P2-env'); P2 algebraic is CFG4's committed number.

PRE-DECLARED (before this script's first run)
  C1  CONTROL  CFG4 H2's committed rms and Upsilon for P2 and nu_mono, both footings, reproduced to < 1e-9 (rms) / exact (U).
  C2  CONTROL  P2 integrated as an ODE through the same machinery equals P2-env at every data point to 1e-4 (relative in g).
  C3  CONTROL  point mass: closures (i) and (ii) reproduce P2 to 1e-6 over three decades in radius, both footings.
  C4  CONTROL  the identity: P2's cold density minus (ii)'s is >= 0 at every grid radius of every galaxy (relative 1e-9).
  H1  PRINCIPLE (i): at its own best Upsilon its rms is within +0.005 dex of P2-env's best rms, both footings.
      Declared EXPECTATION: FAIL (rising Newtonian fields in dwarfs demand negative cold density).  KILL LINE: > +0.02 dex.
  H2  PRINCIPLE (ii): at its own best Upsilon its rms is within +0.005 dex of P2-env's best rms, both footings.
      Declared EXPECTATION: PASS (CFG9 S3: within 0.003 dex at P2's Upsilon in CFG9's statistic).
  R1  (reported) where (i) demands rho_c < 0: fraction of grid radii and of galaxies.
  R2  (reported) the median inner residual (data minus prediction, g_bar > a0) for every law at its best Upsilon.
MUTATE=1: the closures' a0 is doubled inside the ODEs (the statistic's a0 unchanged) -- C3 must FAIL (rc = 1).
Run: python3 campaign_fresh_gravity/CFG10_inner_closure.py   (MUTATE=1 for the control; ~2 min)
"""
import os, sys, math, json
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import CFG7_common as C
C4 = C.C4

MUTATE = os.environ.get("MUTATE", "0") == "1"
R = C.Report("CFG10_inner_closure", MUTATE)
P, check = R.P, R.check
P(__doc__.split("Run: python3")[0].strip())
if MUTATE:
    P("\n  *** MUTATE=1: the closures' a0 doubled inside the ODEs -- C3 must FAIL ***")
np.seterr(all="ignore")
FMUT = 2.0 if MUTATE else 1.0

# ================================================================================================ CFG4 H2's statistic, exactly
GAL = C4.load_sparc()
NG = len(GAL)
UPS = np.round(np.arange(0.30, 1.2001, 0.01), 2)
KPC_S = 3.0857e19
Rm = np.concatenate([g["R"] for g in GAL]) * KPC_S
Vo = np.concatenate([g["Vobs"] for g in GAL])
eV = np.concatenate([g["eV"] for g in GAL])
Vg = np.concatenate([g["Vgas"] for g in GAL])
Vd = np.concatenate([g["Vdisk"] for g in GAL])
Vb = np.concatenate([g["Vbul"] for g in GAL])
GI = np.concatenate([np.full(len(g["R"]), i) for i, g in enumerate(GAL)])
VB2 = np.sign(Vg)[:, None] * Vg[:, None] ** 2 + UPS[None, :] * Vd[:, None] ** 2 + 1.4 * UPS[None, :] * Vb[:, None] ** 2
GB = VB2 * 1e6 / Rm[:, None]
GO = ((Vo * 1e3) ** 2 / Rm)[:, None] * np.ones_like(GB)
OK = (GB > 0) & (GO > 0) & np.isfinite(GB) & np.isfinite(GO) & (Vo > 0)[:, None]
WPT = (1.0 / (np.clip(eV, 1, None) / np.clip(Vo, 1, None)) ** 2)
WW = np.where(OK, WPT[:, None], 0.0)
ONEHOT = np.zeros((NG, len(Rm)))
ONEHOT[GI, np.arange(len(Rm))] = 1.0
CONV = 1e6 / KPC_S                                                      # (km/s)^2/kpc -> m/s^2


def sums_pred(gpred):
    with np.errstate(all="ignore"):
        ok = OK & (gpred > 0) & np.isfinite(gpred)
        r_ = np.log10(np.where(ok, GO, 1.0)) - np.log10(np.where(ok, gpred, 1.0))
        w = np.where(ok, WW, 0.0)
    return ONEHOT @ (w * r_ ** 2), ONEHOT @ w, r_, ok


def best(S, W):
    mse = S.sum(0) / W.sum(0)
    i = int(np.argmin(mse))
    return math.sqrt(mse[i]), float(UPS[i]), i


GL = json.load(open(os.path.join(HERE, "CFG4_galaxy_law_results.json")))["numbers"]["H2"]

# ================================================================================================ C1
R.banner("C1  CONTROL: CFG4 H2's committed rms and Upsilon, reproduced")
c1 = []
ALG = {}
for foot in C.FOOTS:
    a0 = C4.A0[foot]
    for kn in ("P2", "nu_mono"):
        gp = C.KERNELS[kn](np.where(OK, GB, 1.0) / a0) * np.where(OK, GB, 1.0)
        S_, W_, r_, ok_ = sums_pred(gp)
        rr, uu, iu = best(S_, W_)
        ALG[(foot, kn)] = dict(rms=rr, U=uu, iu=iu, r=r_, ok=ok_)
        ref = GL[f"{foot}|{kn}"]
        c1.append((foot, kn, rr, uu, ref["rms"], ref["U"]))
        P(f"    {foot:9s} {kn:8s}: rms {rr:.10f} at U {uu:.2f}  (CFG4 committed {ref['rms']:.10f} at {ref['U']:.2f})")
check("C1 CONTROL: CFG4 H2's committed rms (< 1e-9) and Upsilon (exact) for P2 and nu_mono on both footings",
      "; ".join(f"{a[:3]}/{b}: d rms {abs(c - e):.1e}, U {d:.2f}/{f:.2f}" for a, b, c, d, e, f in c1),
      all(abs(c - e) < 1e-9 and abs(d - f) < 1e-9 for a, b, c, d, e, f in c1))

# ================================================================================================ the closures
NIN, NOUT = 60, 900


def galaxy_grid(g):
    Rg = g["R"]
    vA = np.sign(g["Vgas"]) * g["Vgas"] ** 2
    vB = g["Vdisk"] ** 2 + 1.4 * g["Vbul"] ** 2
    rin = np.geomspace(Rg[0] / 100.0, Rg[0], NIN, endpoint=False)
    rout = np.geomspace(Rg[0], Rg[-1], NOUT)
    rg = np.concatenate([rin, rout])
    vAg = np.where(rg < Rg[0], vA[0] * rg / Rg[0], np.interp(rg, Rg, vA))
    vBg = np.where(rg < Rg[0], vB[0] * rg / Rg[0], np.interp(rg, Rg, vB))
    uB = UPS[None, :] * (vBg * rg)[:, None]
    uN = (vAg * rg)[:, None] + uB
    # the gas's negative V^2 (central HI holes) is disc geometry, not negative mass: the enclosed baryonic mass is floored at
    # the stellar part (added after the first -- MUTATE -- run, which exposed a singular start where the total was <= 0)
    uN = np.maximum(uN, uB)
    uN = np.maximum.accumulate(np.maximum(uN, 0.0), axis=0)                # the monotone envelope of G M_b(<r)
    return rg, uN


def rhs(kind, r, uN, dN, w, a0k):
    u = np.maximum(uN + w, np.maximum(1e-3 * uN, 1e-30))                  # a floor where a closure's total mass breaks down
    if kind == "P2ode":
        return (uN * dN + a0k * r * uN + 0.5 * a0k * r * r * dN) / u - dN
    if kind == "gauss":
        return 0.5 * a0k * (2.0 * uN / r - dN) * r * r / u
    if kind == "encl":
        return a0k * r * uN / u
    raise ValueError(kind)


def integrate(kind, rg, uN, a0k, w0):
    """RK4 on the grid; u_N piecewise linear between grid points (its slope constant on each interval)."""
    w = np.empty_like(uN); w[0] = w0
    broke = np.zeros(uN.shape[1], bool)
    for i in range(len(rg) - 1):
        h = rg[i + 1] - rg[i]; dN = (uN[i + 1] - uN[i]) / h
        um = 0.5 * (uN[i] + uN[i + 1]); rm_ = rg[i] + 0.5 * h
        k1 = rhs(kind, rg[i], uN[i], dN, w[i], a0k)
        k2 = rhs(kind, rm_, um, dN, w[i] + 0.5 * h * k1, a0k)
        k3 = rhs(kind, rm_, um, dN, w[i] + 0.5 * h * k2, a0k)
        k4 = rhs(kind, rg[i + 1], uN[i + 1], dN, w[i] + h * k3, a0k)
        w[i + 1] = w[i] + h * (k1 + 2 * k2 + 2 * k3 + k4) / 6.0
        broke |= (uN[i + 1] + w[i + 1]) < 1e-3 * uN[i + 1]
    integrate.broke = broke
    return w


def at_points(rg, arr, Rpts):
    return np.stack([np.interp(Rpts, rg, arr[:, j]) for j in range(arr.shape[1])], axis=1)


# ================================================================================================ C3 point mass
R.banner("C3  CONTROL: point mass -- the closures reproduce P2")
dev3 = 0.0
for foot in C.FOOTS:
    a0k = C4.A0[foot] / CONV
    for M in (1e8, 1e10, 1e12):
        u0 = 4.30091727e-6 * M
        rM = math.sqrt(u0 / a0k)
        rg = np.geomspace(rM * 1e-2, rM * 1e2, 1200)
        uN = np.full((len(rg), 1), u0)
        wP2 = np.sqrt(uN ** 2 + a0k * uN * rg[:, None] ** 2) - uN
        for kind in ("gauss", "encl"):
            w = integrate(kind, rg, uN, a0k * FMUT, wP2[0])
            dev3 = max(dev3, float(np.max(np.abs((uN + w) / (uN + wP2) - 1.0))))
check("C3 CONTROL: for a point mass (i) and (ii) reproduce P2 to 1e-6 from 0.01 to 100 r_M, both footings"
      + ("  [MUTATE: a0 x 2 in the ODEs]" if MUTATE else ""), f"max relative deviation {dev3:.2e}", dev3 <= 1e-6)

# ================================================================================================ SPARC
R.banner("SPARC: every law at its own best Upsilon")
PRED = {}
nfloor = {}
c2dev, c4min, neg_frac, neg_gal = 0.0, np.inf, [], 0
for foot in C.FOOTS:
    a0 = C4.A0[foot]; a0k = a0 / CONV
    gp = {k: np.zeros_like(GB) for k in ("P2env", "P2ode", "gauss", "encl")}
    for k in gp:
        nfloor[(foot, k)] = np.zeros(len(UPS), int)
    off = 0
    for gi, g in enumerate(GAL):
        n = len(g["R"])
        rg, uN = galaxy_grid(g)
        wP2 = np.sqrt(uN ** 2 + a0k * uN * rg[:, None] ** 2) - uN
        res = {"P2env": wP2}
        for kind in ("P2ode", "gauss", "encl"):
            w0 = wP2[0] if kind == "P2ode" else np.zeros(len(UPS))
            res[kind] = integrate(kind, rg, uN, a0k * (1.0 if kind == "P2ode" else FMUT), w0)
        # C4: P2's density minus (ii)'s on P2's own u (the identity's second term, rho_b (u_N + a0 r^2/2 - u)/u >= 0)
        dNg = np.gradient(uN, rg, axis=0)
        uP = uN + wP2
        term = dNg * (uN + 0.5 * a0k * rg[:, None] ** 2 - uP) / np.maximum(uP, 1e-30)
        scale = np.maximum(a0k * rg[:, None] * uN / np.maximum(uP, 1e-30), 1e-30)
        c4min = min(c4min, float(np.min(term / scale)))
        # R1: where (i) demands negative density (inside the data range)
        inside = rg >= g["R"][0]
        negm = (2.0 * uN / rg[:, None] - dNg) < 0
        if foot == "canonical":
            j07 = int(np.argmin(np.abs(UPS - 0.70)))
            neg_frac.append(float(np.mean(negm[inside, j07])))
            neg_gal += int(np.any(negm[inside, j07]))
        Rpts = g["R"]
        for k, w in res.items():
            wp = at_points(rg, w, Rpts)
            raw = GB[off:off + n] + wp / Rpts[:, None] ** 2 * CONV
            floor = 1e-3 * np.abs(GB[off:off + n])
            nfloor[(foot, k)] += ((raw <= floor) & OK[off:off + n]).sum(0)
            gp[k][off:off + n] = np.maximum(raw, floor)
        okp = OK[off:off + n]
        rel = np.abs(gp["P2ode"][off:off + n] / gp["P2env"][off:off + n] - 1.0)
        c2dev = max(c2dev, float(np.max(np.where(okp, rel, 0.0))))
        off += n
    for k in gp:
        S_, W_, r_, ok_ = sums_pred(gp[k])
        rr, uu, iu = best(S_, W_)
        PRED[(foot, k)] = dict(rms=rr, U=uu, iu=iu, r=r_, ok=ok_, n_floor=int(nfloor[(foot, k)][iu]))
    P(f"    {foot:9s}: P2 algebraic {ALG[(foot, 'P2')]['rms']:.4f} (U {ALG[(foot, 'P2')]['U']:.2f}); P2-env {PRED[(foot, 'P2env')]['rms']:.4f} "
      f"(U {PRED[(foot, 'P2env')]['U']:.2f}); (i) Gauss pressure {PRED[(foot, 'gauss')]['rms']:.4f} (U {PRED[(foot, 'gauss')]['U']:.2f}); "
      f"(ii) shell-theorem charge {PRED[(foot, 'encl')]['rms']:.4f} (U {PRED[(foot, 'encl')]['U']:.2f}); nu_mono {ALG[(foot, 'nu_mono')]['rms']:.4f}")
check("C2 CONTROL: P2 integrated as an ODE equals P2-env at every data point to 1e-4 (relative in g), both footings",
      f"max relative deviation {c2dev:.2e}", c2dev <= 1e-4)
check("C4 CONTROL: the identity -- P2's cold density minus (ii)'s is >= 0 at every grid radius of every galaxy (relative 1e-9)",
      f"min (term / (ii)'s density) = {c4min:.2e}", c4min >= -1e-9)
dH1 = {f: PRED[(f, "gauss")]["rms"] - PRED[(f, "P2env")]["rms"] for f in C.FOOTS}
dH2 = {f: PRED[(f, "encl")]["rms"] - PRED[(f, "P2env")]["rms"] for f in C.FOOTS}
check("H1 PRINCIPLE (i) the pressure Gauss law: best rms within +0.005 dex of P2-env's, both footings [declared expectation: FAIL]",
      "; ".join(f"{f}: {dH1[f]:+.4f} dex" for f in C.FOOTS), all(v <= 0.005 for v in dH1.values()))
kill1 = any(v > 0.02 for v in dH1.values())
P(f"    H1 kill line (> +0.02 dex on either footing): {'CROSSED -- the pressure Gauss law is excluded as the inner principle' if kill1 else 'not crossed'}")
check("H2 PRINCIPLE (ii) the shell theorem for the charge: best rms within +0.005 dex of P2-env's, both footings [expectation: PASS]",
      "; ".join(f"{f}: {dH2[f]:+.4f} dex" for f in C.FOOTS), all(v <= 0.005 for v in dH2.values()))
check("R0 (reported; added with the fix) data points where a law's total mass breaks down (prediction floored at 1e-3 g_bar and "
      "kept in the statistic as a failure), at its best U",
      "; ".join(f"{k[0][:3]}/{k[1]}: {v['n_floor']}" for k, v in PRED.items()), True, load_bearing=False)
check("R1 (reported) where (i) demands negative cold density (canonical, U = 0.70, inside each galaxy's data range)",
      f"median fraction of radii {np.median(neg_frac):.3f}, mean {np.mean(neg_frac):.3f}; galaxies with any such region {neg_gal}/{NG}",
      True, load_bearing=False)
inner = {}
for foot in C.FOOTS:
    a0 = C4.A0[foot]
    for lab, dd in (("P2 alg", ALG[(foot, "P2")]), ("nu_mono", ALG[(foot, "nu_mono")]), ("P2-env", PRED[(foot, "P2env")]),
                    ("(i)", PRED[(foot, "gauss")]), ("(ii)", PRED[(foot, "encl")])):
        iu = dd["iu"]; meds = []
        for gi in range(NG):
            m = (GI == gi) & dd["ok"][:, iu] & (GB[:, iu] > a0)
            if m.sum() >= 1:
                meds.append(float(np.median(dd["r"][m, iu])))
        inner[(foot, lab)] = (float(np.median(meds)), len(meds))
check("R2 (reported) median inner residual log10(g_obs/g_pred) at g_bar > a0 (per galaxy, then median), each law at its best U",
      "; ".join(f"{k[0][:3]}/{k[1]}: {v[0]:+.3f} (N {v[1]})" for k, v in inner.items()), True, load_bearing=False)
R.num("fits", {f"{k[0]}|{k[1]}": dict(rms=v["rms"], U=v["U"], n_floor=v.get("n_floor", 0)) for k, v in {**ALG, **PRED}.items()})
R.num("H", dict(dH1=dH1, dH2=dH2, kill1=kill1, c2dev=c2dev, c3dev=dev3, c4min=c4min,
                neg_frac_median=float(np.median(neg_frac)), neg_gal=neg_gal,
                inner={f"{k[0]}|{k[1]}": v for k, v in inner.items()}))
nf = R.write()
sys.exit(1 if nf else 0)
