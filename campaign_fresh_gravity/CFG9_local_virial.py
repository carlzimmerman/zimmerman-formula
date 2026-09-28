#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
CFG9 -- THE FRAMEWORK'S LAW P2 IS THE LOCALLY VIRIALIZED COLD COMPONENT (around a point mass), AND WHAT THAT LEAVES INSIDE
GALAXIES.

THE RESULT (derived here, checked numerically).  Around a point baryonic mass M, let a cold component sit in isotropic Jeans
equilibrium in the total field with the LOCAL VIRIAL dispersion

      sigma(r)^2 = V_c(r)^2 / 2 ,      V_c^2 = r g_tot    (every shell virialized in its own circular speed).

The Jeans equation d(rho sigma^2)/dr = -rho g_tot then gives rho r V_c^2 = C / r^2 ... exactly: rho = C / (r^3 g_tot), and with
u = G M_tot(<r) = r^2 g_tot the mass equation u' = 4 pi G r^2 rho integrates to

      u^2 = (G M)^2 + 4 pi G C r^2    =>    g_tot = sqrt(g_N^2 + a0 g_N) ,   a0 = 4 pi C / M .

That is EXACTLY the framework's law P2 (nu = sqrt(1 + 1/y)), at every radius, with a0 the cold component's charge per unit
baryonic mass (C = a0 M / 4 pi).  Conversely, for any law nu the point-mass phantom is locally virialized at every radius only
if nu is P2 (the ODE's solution is unique).  Equivalent statement: the P2 phantom's Jeans pressure is P = a0 g_N / (8 pi G) at
every radius (CFG7 FG004 found this only in the deep limit).  So P2's SHAPE follows from one kinematic statement; a0 is the
charge-to-mass ratio of the cold component, which the framework ties to the vacuum (a0 = kappa c sqrt(G rho_Lambda)).

WHAT IT LEAVES.  Inside extended baryons the same closure with a constant charge makes the cold component a central
singular isothermal sphere (V_c flat down to r -> 0), which the RAR's Newtonian inner points forbid.  The law instead needs
the local charge to TRACK the enclosed baryons.  This lane measures that on SPARC.

PRE-DECLARED (before this script's first run)
  D1  CONTROL/THEOREM  for a point mass, P2's phantom has sigma^2_Jeans / (V_c^2/2) = 1 and P / [a0 g_N/(8 pi G)] = 1 to 1e-6
      at every g_N/a0 from 1e-4 to 1e4, on both footings.
  D2  UNIQUENESS  within the record's family nu_beta = (1 + y^-beta)^(1/(2 beta)) (P2 is beta = 1), only beta = 1 is locally
      virialized: at beta = 0.5, 0.75, 1.5, 2 the ratio departs from 1 by > 1% somewhere in 1e-4 <= y <= 1e4; nu_mono departs
      as well (reported).
  D3  CONTROL  the constant-charge closure integrated for a point mass reproduces P2 to 1e-6 (the ODE and the algebra agree).
  S1  (reported) on SPARC (175 galaxies, CFG4_galaxy_law's committed Upsilon), the committed law's phantom: median
      sigma^2_Jeans / (V_c^2/2) in bins of g_bar/a0 -- how close to locally virialized the law is inside real baryons.
  S2  THE INNER DEMAND: the constant-charge closure (C = a0 M_b,total / 4 pi) solved on SPARC fails the inner RAR: its median
      residual at g_bar > a0 exceeds +0.1 dex on both footings.  Pre-declared EXPECT TRUE -- it states what the inner
      mechanism must do.
  S3  (reported) the ENCLOSED-charge closure (C(r) = a0 M_b(<r)/4 pi, the local charge tracking the enclosed baryons; identical
      to P2 for a point mass): its SPARC RAR rms against the law's, both footings.
MUTATE=1: nu_beta at beta = 2 replaces P2 in D1 -- the local-virial identity must FAIL (rc = 1).
Run: python3 campaign_fresh_gravity/CFG9_local_virial.py   (MUTATE=1 for the control; ~1 min)
"""
import os, sys, math, json
import numpy as np
from scipy.integrate import quad, solve_ivp

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import CFG7_common as C
C4 = C.C4

MUTATE = os.environ.get("MUTATE", "0") == "1"
R = C.Report("CFG9_local_virial", MUTATE)
P, check = R.P, R.check
P(__doc__.split("Run: python3")[0].strip())
if MUTATE:
    P("\n  *** MUTATE=1: nu_beta(beta = 2) in place of P2 in D1 -- the identity must FAIL ***")

G_KPC = 4.30091727e-6
ACC = 1e6 / 3.0856775814913673e19
A0K = {f: v / ACC for f, v in C.A0_SI.items()}


def nu_beta(beta):
    return lambda y: (1.0 + np.maximum(np.asarray(y, float), 1e-300) ** (-beta)) ** (1.0 / (2.0 * beta))


def point_ratios(kf, a0, y, M=1e10):
    """for a point mass: sigma^2_Jeans/(V_c^2/2) and P/[a0 g_N/(8 pi G)] at g_N/a0 = y (exact Jeans integral, log-substituted)."""
    r = math.sqrt(G_KPC * M / (y * a0))
    gN = lambda x: G_KPC * M / x ** 2
    gt = lambda x: float(kf(gN(x) / a0)) * gN(x)
    Mph = lambda x: x ** 2 * (gt(x) - gN(x)) / G_KPC

    def rho(x, h=1e-5):
        return (Mph(x * (1 + h)) - Mph(x * (1 - h))) / (2 * h * x) / (4 * math.pi * x ** 2)

    Pj = quad(lambda lx: rho(math.exp(lx)) * gt(math.exp(lx)) * math.exp(lx), math.log(r), math.log(r) + 30, limit=500,
              epsabs=0, epsrel=1e-11)[0]
    s2 = Pj / rho(r)
    return s2 / (r * gt(r) / 2.0), Pj / (a0 * gN(r) / (8 * math.pi * G_KPC))


# ================================================================================================ D1
R.banner("D1  THE THEOREM ON A POINT MASS: P2's phantom is locally virialized at every radius")
YS = np.geomspace(1e-4, 1e4, 17)
dev1 = 0.0; rows = []
for foot in C.FOOTS:
    kf = nu_beta(2.0) if MUTATE else C.nu_p2
    for y in YS:
        a, b = point_ratios(kf, A0K[foot], y)
        dev1 = max(dev1, abs(a - 1), abs(b - 1)); rows.append((foot, y, a, b))
for foot, y, a, b in rows[::4]:
    P(f"    {foot:9s} g_N/a0 = {y:9.2e}: sigma^2/(V_c^2/2) = {a:.8f}; P/[a0 g_N/8 pi G] = {b:.8f}")
check("D1 THEOREM: for a point mass P2's phantom has sigma^2_Jeans = V_c^2/2 and P = a0 g_N/(8 pi G) to 1e-6 at every g_N/a0 in "
      "[1e-4, 1e4], both footings" + ("  [MUTATE: beta = 2]" if MUTATE else ""), f"max deviation {dev1:.2e}", dev1 <= 1e-6)
R.num("D1", dict(max_dev=dev1))

# ================================================================================================ D2 uniqueness
R.banner("D2  UNIQUENESS: only beta = 1 (P2) in the family nu_beta is locally virialized")
D2 = {}
for lab, kf in (("beta=0.5", nu_beta(0.5)), ("beta=0.75", nu_beta(0.75)), ("beta=1 (P2)", nu_beta(1.0)), ("beta=1.5", nu_beta(1.5)),
                ("beta=2", nu_beta(2.0)), ("nu_mono", C.nu_mono)):
    devs = [abs(point_ratios(kf, A0K["canonical"], y)[0] - 1) for y in YS]
    D2[lab] = dict(max_dev=float(max(devs)), y_at_max=float(YS[int(np.argmax(devs))]))
    P(f"    {lab:12s}: max |sigma^2/(V_c^2/2) - 1| = {max(devs):.4f} (at g_N/a0 = {YS[int(np.argmax(devs))]:.1e})")
uniq = D2["beta=1 (P2)"]["max_dev"] <= 1e-6 and all(D2[k]["max_dev"] > 0.01 for k in ("beta=0.5", "beta=0.75", "beta=1.5", "beta=2"))
check("D2 UNIQUENESS: within nu_beta only beta = 1 (P2) is locally virialized; beta = 0.5, 0.75, 1.5, 2 depart by > 1%",
      "; ".join(f"{k}: {v['max_dev']:.2e}" for k, v in D2.items()), uniq)
R.num("D2", D2)

# ================================================================================================ D3 the closure as an ODE
R.banner("D3  CONTROL: the constant-charge closure integrated as an ODE for a point mass reproduces P2")


def closure_point(M, a0, rmax):
    Cc = a0 * M / (4 * math.pi)
    rhs = lambda r, u: [4 * math.pi * G_KPC * Cc * r / u[0]]
    r0 = 1e-6 * rmax
    u0 = math.sqrt((G_KPC * M) ** 2 + 4 * math.pi * G_KPC * Cc * r0 ** 2)
    sol = solve_ivp(rhs, (r0, rmax), [u0], dense_output=True, rtol=1e-12, atol=1e-14)
    return sol


dev3 = 0.0
for foot in C.FOOTS:
    M = 3e10; a0 = A0K[foot]
    sol = closure_point(M, a0, 500.0)
    for r in (0.5, 5.0, 50.0, 400.0):
        g = sol.sol(r)[0] / r ** 2
        gp2 = float(C.nu_p2(G_KPC * M / r ** 2 / a0)) * G_KPC * M / r ** 2
        dev3 = max(dev3, abs(g / gp2 - 1))
check("D3 CONTROL: the constant-charge closure (C = a0 M/4 pi) integrated as an ODE equals P2 for a point mass to 1e-6",
      f"max deviation {dev3:.2e}", dev3 <= 1e-6)

# ================================================================================================ S1-S3 SPARC
R.banner("S1-S3  ON SPARC: how locally virialized is the law inside real baryons, and what the two closures predict")
GL = json.load(open(os.path.join(HERE, "CFG4_galaxy_law_results.json")))["numbers"]["H2"]
GAL = C4.load_sparc()


def curve(g, U):
    Vb2 = g["Vgas"] * np.abs(g["Vgas"]) + U * g["Vdisk"] ** 2 + 1.4 * U * g["Vbul"] ** 2
    ok = (g["R"] > 0) & (Vb2 > 0) & (g["Vobs"] > 0)
    return g["R"][ok], Vb2[ok], g["Vobs"][ok], np.maximum(g["eV"][ok], 1.0)


S = {}
for foot in C.FOOTS:
    for kn in ("P2", "nu_mono"):
        U = GL[f"{foot}|{kn}"]["U"]; a0 = A0K[foot]; kf = C.KERNELS[kn]
        vir_bins = {"gb>a0": [], "0.1<gb<a0": [], "gb<0.1": []}
        res_const = {"gb>a0": [], "0.1<gb<a0": [], "gb<0.1": []}
        res_law, res_encl, w_all = [], [], []
        vflat_ratio, const_minus_law = [], []
        for g in GAL:
            R_, Vb2, Vo, eV = curve(g, U)
            if len(R_) < 5:
                continue
            rg = np.geomspace(R_[0], R_[-1], 300)
            Mb = np.maximum(np.interp(rg, R_, Vb2) * rg / G_KPC, 1e-3)
            Mb = np.maximum.accumulate(Mb)                                        # the enclosed baryonic mass is non-decreasing
            gN = G_KPC * Mb / rg ** 2
            gt = kf(gN / a0) * gN
            # S1: Jeans sigma^2 of the law's phantom vs V_c^2/2 (tail beyond R_last: a point mass)
            Mph = rg ** 2 * (gt - gN) / G_KPC
            rho = np.gradient(Mph, rg) / (4 * math.pi * rg ** 2)
            integ = rho * gt
            tail = 0.0
            Mt = Mb[-1]
            for lx0, lx1 in ((math.log(rg[-1]), math.log(rg[-1]) + 30),):
                gNt = lambda x: G_KPC * Mt / x ** 2
                gtt = lambda x: float(kf(gNt(x) / a0)) * gNt(x)
                Mpt = lambda x: x ** 2 * (gtt(x) - gNt(x)) / G_KPC
                rhot = lambda x: (Mpt(x * 1.00001) - Mpt(x * 0.99999)) / (2e-5 * x) / (4 * math.pi * x ** 2)
                tail = quad(lambda lx: rhot(math.exp(lx)) * gtt(math.exp(lx)) * math.exp(lx), lx0, lx1, limit=300)[0]
            Pr = tail + np.concatenate([np.cumsum((0.5 * (integ[1:] + integ[:-1]) * np.diff(rg))[::-1])[::-1], [0.0]])
            okr = rho > 0
            ratio = (Pr / np.where(okr, rho, np.nan)) / (rg * gt / 2.0)
            for k, m in (("gb>a0", gN > a0), ("0.1<gb<a0", (gN > 0.1 * a0) & (gN <= a0)), ("gb<0.1", gN <= 0.1 * a0)):
                mm = m & okr & np.isfinite(ratio)
                if mm.any():
                    vir_bins[k].append(float(np.median(ratio[mm])))
            if g["meta"] and g["meta"]["Vflat"] > 0:                              # S1b: FG004's reference and sample
                deep = (gN < 0.1 * a0) & okr
                if deep.sum() >= 3:
                    vflat_ratio.append(float(np.median((Pr[deep] / rho[deep]) / (g["meta"]["Vflat"] ** 2 / 2))))
            # S2: the constant-charge closure u u' = G M_b' u + 4 pi G C r, C = a0 M_b,total/4 pi
            Cc = a0 * Mb[-1] / (4 * math.pi)
            dMb = np.gradient(Mb, rg)
            fM = lambda r: np.interp(r, rg, dMb)
            sol = solve_ivp(lambda r, u: [G_KPC * fM(r) + 4 * math.pi * G_KPC * Cc * r / max(u[0], 1e-30)], (rg[0], rg[-1]),
                            [G_KPC * Mb[0] + 1e-12], t_eval=rg, rtol=1e-8, atol=1e-10)
            gc = sol.y[0] / rg ** 2
            # S3: the enclosed-charge closure (u^2)' = 2 G M_b' u + 2 a0 G M_b(<r) r
            sol2 = solve_ivp(lambda r, u: [G_KPC * fM(r) + a0 * G_KPC * np.interp(r, rg, Mb) * r / max(u[0], 1e-30)],
                             (rg[0], rg[-1]), [math.sqrt((G_KPC * Mb[0]) ** 2 + a0 * G_KPC * Mb[0] * rg[0] ** 2)], t_eval=rg,
                             rtol=1e-8, atol=1e-10)
            ge = sol2.y[0] / rg ** 2
            # residuals at the data points
            go = Vo ** 2 / R_
            gN_d = np.interp(R_, rg, gN)
            lc = np.log10(np.interp(R_, rg, gc)); le = np.log10(np.interp(R_, rg, ge)); ll = np.log10(np.interp(R_, rg, gt))
            w = (Vo / eV) ** 2
            for k, m in (("gb>a0", gN_d > a0), ("0.1<gb<a0", (gN_d > 0.1 * a0) & (gN_d <= a0)), ("gb<0.1", gN_d <= 0.1 * a0)):
                if m.any():
                    res_const[k].append(float(np.median(lc[m] - np.log10(go[m]))))
            if (gN_d > a0).any():
                const_minus_law.append(float(np.median(lc[gN_d > a0] - ll[gN_d > a0])))
            res_law.append(np.sum(w * (np.log10(go) - ll) ** 2)); res_encl.append(np.sum(w * (np.log10(go) - le) ** 2)); w_all.append(np.sum(w))
        rms_law = math.sqrt(sum(res_law) / sum(w_all)); rms_encl = math.sqrt(sum(res_encl) / sum(w_all))
        S[(foot, kn)] = dict(virial={k: (float(np.median(v)) if v else float("nan"), len(v)) for k, v in vir_bins.items()},
                             const={k: (float(np.median(v)) if v else float("nan"), len(v)) for k, v in res_const.items()},
                             rms_law=rms_law, rms_encl=rms_encl, vflat=(float(np.median(vflat_ratio)), len(vflat_ratio)),
                             const_minus_law_inner=float(np.median(const_minus_law)))
        P(f"    {foot:9s} {kn:8s}: S1 sigma^2/(V_c^2/2) medians " + ", ".join(f"{k} {v[0]:.3f}" for k, v in S[(foot, kn)]['virial'].items())
          + f" | S2 constant-charge closure minus data " + ", ".join(f"{k} {v[0]:+.3f}" for k, v in S[(foot, kn)]['const'].items())
          + f" | S3 rms: law {rms_law:.4f}, enclosed-charge closure {rms_encl:.4f} dex")
check("S1 (reported) inside real baryons the committed law's phantom is close to locally virialized (medians by g_bar/a0)",
      "; ".join(f"{k[0][:3]}/{k[1]}: " + "/".join(f"{v[0]:.2f}" for v in S[k]['virial'].values()) for k in S), True, load_bearing=False)
FG4 = json.load(open(os.path.join(HERE, "CFG7_groundstate_fg004_results.json")))["numbers"]["H1"]
s1b = {k: (S[k]["vflat"][0], FG4[f"{k[0]}|{k[1]}"]["med_sigma"]) for k in S}
check("S1b CONTROL (added after the first run, to reconcile with FG004): against V_flat^2/2 on FG004's sample (V_flat > 0, >= 3 "
      "points below 0.1 a0) the same Jeans sigma^2 reproduces FG004's committed H1 medians within 0.03",
      "; ".join(f"{k[0][:3]}/{k[1]}: {v[0]:.3f} vs FG004 {v[1]:.3f}" for k, v in s1b.items()),
      all(abs(v[0] - v[1]) <= 0.03 for v in s1b.values()))
R.num("S1b", {f"{k[0]}|{k[1]}": dict(cfg9=v[0], fg004=v[1]) for k, v in s1b.items()})
s2 = all(S[(f, "P2")]["const"]["gb>a0"][0] > 0.1 for f in C.FOOTS)
check("S2 THE INNER DEMAND: the constant-charge closure over-predicts the inner RAR by > +0.1 dex at g_bar > a0 (the cold component "
      "becomes a central isothermal sphere), both footings -- so the local charge must track the enclosed baryons",
      "; ".join(f"{k[0][:3]}/{k[1]}: {S[k]['const']['gb>a0'][0]:+.3f} dex" for k in S), s2)
check("S2b (reported; added after the first run) the constant-charge closure minus the committed law at data points with "
      "g_bar > a0 (comparable with FG004 H2's +0.13-0.15 dex)",
      "; ".join(f"{k[0][:3]}/{k[1]}: {S[k]['const_minus_law_inner']:+.3f} dex" for k in S), True, load_bearing=False)
check("S3 (reported) the enclosed-charge closure's SPARC rms against the law's",
      "; ".join(f"{k[0][:3]}/{k[1]}: law {S[k]['rms_law']:.4f}, closure {S[k]['rms_encl']:.4f}" for k in S), True, load_bearing=False)
R.num("S", {f"{k[0]}|{k[1]}": v for k, v in S.items()})
nf = R.write()
sys.exit(1 if nf else 0)
