#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
CFG7 / FG004 -- IS THE MAX RULE A GROUND STATE?  (Is CFG4's T5 -- "in a bound region the cold component IS the phantom" --
the relaxed state of a collisionless cold component in the law's own field?)

THE QUESTION.  A self-gravitating collisionless component that has relaxed (violent relaxation: the maximum-entropy state at
fixed mass and energy) is ISOTHERMAL in the potential it sits in: rho ~ exp(-Phi/sigma^2).  If the law's phantom density is
that state, T5 is derived (the cold component settles where the law says, with no new rule).  If it is not, the size and place
of the mismatch is the next target.

TWO RESULTS DERIVED HERE (analytic, checked numerically):
  D1  Around a point baryonic mass, in the law's deep regime (g_N << a0), the phantom rho_ph = -div[(nu - 1) g_N]/4 pi G is an
      isotropic, isothermal sphere in hydrostatic (Jeans) equilibrium in the TOTAL field, with sigma^2 = V_f^2 / 2 and pressure
          P_ph = rho_ph sigma^2 = a0 g_N / (8 pi G)        (a local identity: the phantom's pressure is set by the Newtonian field)
      -- the relaxed (maximum-entropy) configuration of a tracer in the flat-rotation-curve potential.
  D2  No LOCAL equation of state P = Pi(g_N) can hold wherever baryons sit: in spherical symmetry the Jeans condition splits into
      a term in dg_N/dr (which fixes Pi') and a term without it (2 h nu g_N / r with h = (nu - 1) g_N), which vanishes only where
      the phantom does.  So inside the baryons the ground state cannot be a local fluid of g_N alone.
SPARC TEST (175 galaxies; the law at its committed global Upsilon from CFG4_galaxy_law; both footings; P2 and nu_mono; the
spherical-equivalent phantom M_ph(r) = r^2 (g_obs,law - g_N)/G along each rotation curve):
  S1  the phantom's Jeans dispersion sigma^2(r) = (1/rho_ph) Int_r^oo rho_ph g_tot dr' (the tail beyond the last point: the
      galaxy's baryons as a point mass, integrated to 100 R_last).
  S2  the maximum-entropy alternative: the SAME cold mass inside the last measured radius (T5's amount there), distributed
      isothermally at the outer sigma^2 in the law's potential, rho_iso = C exp(-Phi_tot / sigma^2_out); with the max rule
      the rotation it implies, against the law, point by point.

PRE-DECLARED (before this script's first run)
  C1  CONTROL  CFG4_galaxy_law's committed SPARC fit (rms and Upsilon, P2 and nu_mono, both footings) is reproduced by this
      script's own statistic to 1e-6 dex (the RAR the phantom is built on).
  C2  CONTROL  D1 numerically: for a point mass, the Jeans pressure of the phantom equals a0 g_N/(8 pi G) within 1% at
      g_N/a0 <= 1e-3, and sigma^2 -> V_f^2/2 within 1% (P2 and nu_mono, both footings).
  H1  THE OUTER PHANTOM IS RELAXED: at SPARC points with g_bar < 0.1 a0 the phantom's Jeans sigma^2 lies within 20% of
      V_flat^2/2 (median over galaxies), both footings, both kernels.  EXPECT TRUE.
  H2  THE INNER PHANTOM IS THE GROUND STATE: the isothermal (maximum-entropy) cold component, with T5's amount inside the last
      point, in the law's potential and under the max rule, stays within 0.1 dex of the law (median residual) at g_bar > a0.
      Pre-declared UNCERTAIN: a relaxed cold component concentrates where the baryons deepen the potential.
  H3  (reported) THE DEEP IDENTITY ON DATA: at the points with g_bar < 0.1 a0, the Jeans pressure over a0 g_N/(8 pi G) has
      median within 30% of 1.
  H4  (reported) NO UNIVERSAL BAROTROPIC EQUATION OF STATE: the cross-galaxy scatter of log P at fixed log rho_ph exceeds
      0.1 dex (D2 on data).
MUTATE=1: the phantom is computed with a0 x 10 while the rotation data stay: the outer sigma^2 no longer matches V_flat^2/2,
H1 must FAIL (rc = 1).

SCOPE: spherical-equivalent masses from rotation curves (the record's convention); the law's field, not a fit of a halo; the
cold component's self-gravity inside the max rule enters through the law's mass, not re-solved (first iteration: a lower bound
on how much a relaxed component concentrates).  kappa = 1/2 fitted; both footings.
Run: python3 campaign_fresh_gravity/CFG7_groundstate_fg004.py   (MUTATE=1 for the control; ~20 s)
"""
import os, sys, math, json
import numpy as np
from scipy.integrate import quad

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import CFG7_common as C
C4 = C.C4

MUTATE = os.environ.get("MUTATE", "0") == "1"
R = C.Report("CFG7_groundstate_fg004", MUTATE)
P, check = R.P, R.check
P(__doc__.split("SCOPE:")[0].strip())
if MUTATE:
    P("\n  *** MUTATE=1: the phantom built with a0 x 10 against the same data -- H1 must FAIL ***")

G_KPC = 4.30091727e-6                                                                  # kpc (km/s)^2 / Msun
KPC_M = 3.0856775814913673e19
ACC = 1e6 / KPC_M                                                                      # (km/s)^2/kpc -> m/s^2
A0K = {f: v / ACC for f, v in C.A0_SI.items()}                                         # (km/s)^2/kpc
KERN = C.KERNELS
GL = json.load(open(os.path.join(HERE, "CFG4_galaxy_law_results.json")))["numbers"]["H2"]
GAL = C4.load_sparc()

# ================================================================================================ C1 the committed fit
R.banner("C1  CONTROL: CFG4_galaxy_law's committed SPARC fit reproduced (the record's statistic)")


def rar_points(g, U):
    Vb2 = g["Vgas"] * np.abs(g["Vgas"]) + U * g["Vdisk"] ** 2 + 1.4 * U * g["Vbul"] ** 2
    ok = (g["R"] > 0) & (Vb2 > 0) & (g["Vobs"] > 0)
    R_ = g["R"][ok]; gb = Vb2[ok] / R_; go = g["Vobs"][ok] ** 2 / R_
    w = (np.maximum(g["Vobs"][ok], 1.0) / np.maximum(g["eV"][ok], 1.0)) ** 2
    return R_, gb, go, w, ok


dev1 = 0.0
for foot in C.FOOTS:
    for kn in ("P2", "nu_mono"):
        U = GL[f"{foot}|{kn}"]["U"]
        S = Wt = 0.0
        for g in GAL:
            R_, gb, go, w, _ = rar_points(g, U)
            r_ = np.log10(go) - np.log10(KERN[kn](gb / A0K[foot]) * gb)
            S += float(np.sum(w * r_ ** 2)); Wt += float(np.sum(w))
        rms = math.sqrt(S / Wt)
        dev1 = max(dev1, abs(rms - GL[f"{foot}|{kn}"]["rms"]))
        P(f"    {foot:9s} {kn:8s}: Upsilon_disk {U:.2f}: rms {rms:.6f} dex (committed {GL[f'{foot}|{kn}']['rms']:.6f})")
check("C1 CONTROL: CFG4_galaxy_law's committed SPARC rms at its committed Upsilon reproduced to 1e-6 dex (P2, nu_mono, both footings)",
      f"max |d rms| = {dev1:.2e}", dev1 <= 1e-6)

# ================================================================================================ C2 the deep identity for a point mass
R.banner("C2  CONTROL / D1: the phantom of a point mass is a Jeans-isothermal sphere with P = a0 g_N / (8 pi G) in the deep regime")


def point_phantom_jeans(M, a0, kf, r):
    """Jeans pressure (integral of rho_ph g_tot to infinity) and rho_ph for a point mass at radius r (kpc units)."""
    gN = lambda x: G_KPC * M / x ** 2
    Mph = lambda x: x ** 2 * (float(kf(gN(x) / a0)) - 1.0) * gN(x) / G_KPC
    def rho(x, h=1e-4):
        return (Mph(x * (1 + h)) - Mph(x * (1 - h))) / (2 * h * x) / (4 * math.pi * x ** 2)
    gt = lambda x: float(kf(gN(x) / a0)) * gN(x)
    Pint = quad(lambda lx: rho(math.exp(lx)) * gt(math.exp(lx)) * math.exp(lx), math.log(r), math.log(r) + 25, limit=400, epsabs=0, epsrel=1e-10)[0]
    return Pint, rho(r), gt(r)


dev2 = 0.0
for foot in C.FOOTS:
    for kn, kf in KERN.items():
        a0 = A0K[foot]; M = 1e10
        for y in (1e-3, 1e-4):
            r = math.sqrt(G_KPC * M / (y * a0))
            Pj, rh, gt = point_phantom_jeans(M, a0, kf, r)
            Pid = a0 * (G_KPC * M / r ** 2) / (8 * math.pi * G_KPC)
            Vf2 = gt * r
            s2 = Pj / rh
            dev2 = max(dev2, abs(Pj / Pid - 1), abs(s2 / (Vf2 / 2) - 1))
            P(f"    {foot:9s} {kn:8s} g_N/a0 = {y:.0e}: P_Jeans / [a0 g_N/(8 pi G)] = {Pj / Pid:.5f}; sigma^2 / (V_f^2/2) = {s2 / (Vf2 / 2):.5f}")
check("C2 CONTROL / D1: for a point mass the phantom's Jeans pressure equals a0 g_N/(8 pi G) and sigma^2 = V_f^2/2 within 1% at "
      "g_N/a0 <= 1e-3 (P2, nu_mono, both footings)", f"max deviation {dev2:.2e}", dev2 <= 0.01)
# added after the first run (reported): the first run's C2 failed only for nu_mono at g_N/a0 = 1e-3 (1.05%); nu_RAR carries a
# sub-leading constant (nu - 1/sqrt(y) -> 1/2), so the identity is asymptotic with a sqrt(y) correction -- checked here, not re-tuned
dv = {}
for y in (1e-3, 1e-4, 1e-5, 1e-6):
    M = 1e10; a0 = A0K["canonical"]; r = math.sqrt(G_KPC * M / (y * a0))
    Pj, rh, gt = point_phantom_jeans(M, a0, C.nu_mono, r)
    dv[y] = Pj / (a0 * (G_KPC * M / r ** 2) / (8 * math.pi * G_KPC)) - 1
P("    nu_mono: P_Jeans / [a0 g_N/(8 pi G)] - 1 = " + ", ".join(f"{v:+.2e} at {y:.0e}" for y, v in dv.items()))
ratios_dv = [dv[1e-3] / dv[1e-4], dv[1e-4] / dv[1e-5]]
check("C2b (reported; added after the first run) the nu_mono deviation from D1 falls as sqrt(g_N/a0) (a factor 10^0.5 = 3.16 per decade "
      "within 15%) -- the identity is exact for P2 and asymptotic for nu_mono",
      f"deviation ratios per decade {ratios_dv[0]:.2f}, {ratios_dv[1]:.2f}", all(abs(x / 3.1623 - 1) <= 0.15 for x in ratios_dv), load_bearing=False)

# ================================================================================================ the SPARC phantoms
R.banner("S1  THE PHANTOM ALONG EACH SPARC ROTATION CURVE: rho_ph, its Jeans sigma^2 and pressure")


def galaxy_phantom(g, U, a0, kf):
    """on a fine radial grid spanning the rotation curve: baryonic g_N (interpolated V_bar^2), the law's total field, the
    spherical-equivalent phantom mass and density, the Jeans pressure (tail: the baryons as a point mass beyond R_last)."""
    R_, gb, go, w, ok = rar_points(g, U)
    if len(R_) < 5:
        return None
    Vb2 = gb * R_
    rg = np.geomspace(R_[0], R_[-1], 400)
    Vb2g = np.interp(rg, R_, Vb2)
    gN = np.maximum(Vb2g, 1e-6) / rg
    gt = kf(gN / a0) * gN
    Mph = rg ** 2 * (gt - gN) / G_KPC
    dM = np.gradient(Mph, rg)
    rho = dM / (4 * math.pi * rg ** 2)
    # the tail beyond R_last: a point mass M_b(R_last)
    Mb_last = Vb2g[-1] * rg[-1] / G_KPC
    Ptail = point_phantom_jeans(Mb_last, a0, kf, rg[-1])[0]
    integrand = rho * gt
    Pr = Ptail + np.concatenate([np.cumsum((0.5 * (integrand[1:] + integrand[:-1]) * np.diff(rg))[::-1])[::-1], [0.0]])
    Phi = -np.concatenate([np.cumsum((0.5 * (gt[1:] + gt[:-1]) * np.diff(rg))[::-1])[::-1], [0.0]])     # Phi(r) - Phi(R_last)
    return dict(r=rg, gN=gN, gt=gt, Mph=Mph, rho=rho, P=Pr, Phi=Phi, Mb=Vb2g * rg / G_KPC, R_pts=R_, gb_pts=gb, go_pts=go)


RES = {}
for foot in C.FOOTS:
    for kn, kf in KERN.items():
        U = GL[f"{foot}|{kn}"]["U"]
        a0 = A0K[foot] * (10.0 if MUTATE else 1.0)
        out = []
        for g in GAL:
            ph = galaxy_phantom(g, U, a0, kf)
            if ph is None or not g["meta"] or g["meta"]["Vflat"] <= 0:
                continue
            ph["name"] = g["name"]; ph["Vflat"] = g["meta"]["Vflat"]
            out.append(ph)
        RES[(foot, kn)] = out
        P(f"    {foot:9s} {kn:8s}: {len(out)} galaxies with a flat velocity and >= 5 points")

# ================================================================================================ H1 the outer phantom is relaxed
R.banner("H1  THE OUTER PHANTOM IS RELAXED: Jeans sigma^2 at g_bar < 0.1 a0 against V_flat^2/2")
H1 = {}
for (foot, kn), gals in RES.items():
    a0 = A0K[foot]
    ratios, ratios_P = [], []
    for ph in gals:
        deep = (ph["gN"] < 0.1 * a0) & (ph["rho"] > 0)
        if deep.sum() < 3:
            continue
        s2 = ph["P"][deep] / ph["rho"][deep]
        ratios.append(float(np.median(s2 / (ph["Vflat"] ** 2 / 2))))
        ratios_P.append(float(np.median(ph["P"][deep] / (a0 * ph["gN"][deep] / (8 * math.pi * G_KPC)))))
    H1[(foot, kn)] = dict(n=len(ratios), med_sigma=float(np.median(ratios)), iqr_sigma=[float(np.percentile(ratios, 25)), float(np.percentile(ratios, 75))],
                          med_P=float(np.median(ratios_P)), iqr_P=[float(np.percentile(ratios_P, 25)), float(np.percentile(ratios_P, 75))])
    P(f"    {foot:9s} {kn:8s}: {len(ratios)} galaxies with deep points: sigma^2/(V_flat^2/2) median {H1[(foot, kn)]['med_sigma']:.3f} "
      f"(IQR {H1[(foot, kn)]['iqr_sigma'][0]:.2f}-{H1[(foot, kn)]['iqr_sigma'][1]:.2f}); P/[a0 g_N/(8 pi G)] median {H1[(foot, kn)]['med_P']:.3f} "
      f"(IQR {H1[(foot, kn)]['iqr_P'][0]:.2f}-{H1[(foot, kn)]['iqr_P'][1]:.2f})")
h1 = all(abs(v["med_sigma"] - 1) <= 0.20 for v in H1.values())
check("H1 THE OUTER PHANTOM IS RELAXED: at g_bar < 0.1 a0 the phantom's Jeans sigma^2 is within 20% of V_flat^2/2 (median over "
      "galaxies), both footings, both kernels", "; ".join(f"{k[0][:3]}/{k[1]}: {v['med_sigma']:.3f} (N = {v['n']})" for k, v in H1.items()), h1)
h3 = all(abs(v["med_P"] - 1) <= 0.30 for v in H1.values())
check("H3 (reported) THE DEEP IDENTITY ON DATA: P_Jeans / [a0 g_N/(8 pi G)] has median within 30% of 1 at g_bar < 0.1 a0",
      "; ".join(f"{k[0][:3]}/{k[1]}: {v['med_P']:.3f}" for k, v in H1.items()), h3, load_bearing=False)
R.num("H1", {f"{k[0]}|{k[1]}": v for k, v in H1.items()})

# ================================================================================================ H2 the isothermal ground state inside
R.banner("H2  THE INNER TEST: the maximum-entropy (isothermal) cold component with T5's amount, under the max rule")
H2 = {}
for (foot, kn), gals in RES.items():
    a0 = A0K[foot]
    res_bins = {k: [] for k in ("gb>a0", "0.1<gb<a0", "gb<0.1")}
    frac_iso_wins = []
    for ph in gals:
        r = ph["r"]
        deep = (ph["gN"] < 0.1 * a0) & (ph["rho"] > 0)
        s2_out = float(np.median(ph["P"][deep] / ph["rho"][deep])) if deep.sum() >= 3 else ph["Vflat"] ** 2 / 2
        Mcold = ph["Mph"][-1]                                                            # T5's amount inside the last point
        if Mcold <= 0:
            continue
        w_ = np.exp(-(ph["Phi"] - ph["Phi"][-1]) / s2_out)
        shell = 4 * math.pi * r ** 2 * w_
        cum = np.concatenate([[0.0], np.cumsum(0.5 * (shell[1:] + shell[:-1]) * np.diff(r))])
        # the innermost radius: a uniform core inside r[0] at the first density (small)
        cum = cum + 4 * math.pi / 3 * r[0] ** 3 * w_[0]
        Miso = Mcold * cum / cum[-1]
        Mlaw = ph["Mb"] + ph["Mph"]
        Meff = np.maximum(Mlaw, ph["Mb"] + Miso)                                          # the max rule
        resid = np.log10(Meff / Mlaw)                                                     # = log10(g_eff / g_law)
        frac_iso_wins.append(float(np.mean(ph["Mb"] + Miso > Mlaw)))
        for k, m in (("gb>a0", ph["gN"] > a0), ("0.1<gb<a0", (ph["gN"] > 0.1 * a0) & (ph["gN"] <= a0)), ("gb<0.1", ph["gN"] <= 0.1 * a0)):
            if m.any():
                res_bins[k].append(float(np.median(resid[m])))
    H2[(foot, kn)] = {k: dict(n=len(v), median=float(np.median(v)) if v else float("nan"), p84=float(np.percentile(v, 84)) if v else float("nan"))
                      for k, v in res_bins.items()}
    H2[(foot, kn)]["frac_points_iso_exceeds_law"] = float(np.median(frac_iso_wins))
    P(f"    {foot:9s} {kn:8s}: the isothermal cold component (max rule) over the law, median per galaxy: " +
      "; ".join(f"{k}: {v['median']:+.3f} dex (84th pct {v['p84']:+.3f}, N {v['n']})" for k, v in H2[(foot, kn)].items() if isinstance(v, dict)) +
      f"; median fraction of radii where the relaxed component exceeds the law {H2[(foot, kn)]['frac_points_iso_exceeds_law']:.2f}")
h2 = all(abs(v["gb>a0"]["median"]) <= 0.1 for v in H2.values())
check("H2 (pre-declared UNCERTAIN) THE INNER PHANTOM IS THE GROUND STATE: the isothermal cold component with T5's amount stays within "
      "0.1 dex of the law at g_bar > a0 (median over galaxies), both footings, both kernels",
      "; ".join(f"{k[0][:3]}/{k[1]}: {v['gb>a0']['median']:+.3f} dex" for k, v in H2.items()), h2)
R.num("H2", {f"{k[0]}|{k[1]}": v for k, v in H2.items()})

# ================================================================================================ H4 no universal EOS
R.banner("H4  (reported) A UNIVERSAL BAROTROPIC EQUATION OF STATE?  log P at fixed log rho_ph across galaxies")
H4 = {}
for (foot, kn), gals in RES.items():
    lr, lp, gid = [], [], []
    for i, ph in enumerate(gals):
        m = ph["rho"] > 0
        lr.extend(np.log10(ph["rho"][m])); lp.extend(np.log10(ph["P"][m])); gid.extend([i] * int(m.sum()))
    lr, lp = np.array(lr), np.array(lp)
    edges = np.linspace(np.percentile(lr, 5), np.percentile(lr, 95), 11)
    sc = []
    for lo, hi in zip(edges[:-1], edges[1:]):
        m = (lr >= lo) & (lr < hi)
        if m.sum() > 50:
            sc.append(float(np.std(lp[m])))
    H4[(foot, kn)] = dict(scatter_median=float(np.median(sc)), scatter_bins=sc)
    P(f"    {foot:9s} {kn:8s}: the cross-galaxy scatter of log P at fixed log rho: median {np.median(sc):.3f} dex over {len(sc)} bins")
h4 = all(v["scatter_median"] > 0.1 for v in H4.values())
check("H4 (reported) NO UNIVERSAL BAROTROPIC EQUATION OF STATE: the cross-galaxy scatter of log P at fixed log rho_ph exceeds 0.1 dex "
      "(D2 on data)", "; ".join(f"{k[0][:3]}/{k[1]}: {v['scatter_median']:.3f} dex" for k, v in H4.items()), h4, load_bearing=False)
R.num("H4", {f"{k[0]}|{k[1]}": v for k, v in H4.items()})

# ================================================================================================ verdict
R.banner("VERDICT")
P(f"    Outer phantom: sigma^2/(V_flat^2/2) = " + ", ".join(f"{k[0][:3]}/{k[1]} {v['med_sigma']:.2f}" for k, v in H1.items()) +
  " -- the relaxed isothermal state (D1: P = a0 g_N / 8 pi G exactly in the deep regime).")
P(f"    Inner phantom: a relaxed cold component with T5's amount would exceed the law at g_bar > a0 by " +
  ", ".join(f"{k[0][:3]}/{k[1]} {v['gb>a0']['median']:+.2f} dex" for k, v in H2.items()) + " (max rule).")
nf = R.write()
sys.exit(1 if nf else 0)
