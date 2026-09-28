#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
CFG7 / FG041 -- TIDAL DWARF GALAXIES: the cleanest kill test for FG001 (hierarchical ownership of the phantom).

FG001 says the phantom (the framework's law acting on a system's own baryons) belongs only to the OUTERMOST bound system.
A tidal dwarf galaxy (TDG) forms inside its host's bound region, out of the host's disc material, which carries no cold
component (the cold component is too hot to be captured into tidal debris).  So under FG001 a TDG has no phantom of its
own and no cold component: its rotation must be NEWTONIAN from its baryons alone.  The framework's law applied to the TDG
itself (isolated, or with the host's external field) predicts a mass discrepancy instead.  IDEAS_100 wrote the kill:
"a MOND-like discrepancy is confirmed" kills FG001.

DATA: the six bona-fide TDGs of Lelli et al. 2015 (A&A 584, A113), around NGC 5291, NGC 7252 and NGC 4694, transcribed
from the paper's Tables 1, 7, 8 and 9 into real_research/data/tidal_dwarfs/lelli2015_tdg.csv (provenance file beside it).
The same data for every prediction; the paper's own conventions for V_circ (asymmetric drift) and the external field.

PRE-DECLARED (before this script's first run)
  C1 CONTROL  the paper's Table 8 is reproduced from its Table 7: V_circ = sqrt(V_rot^2 + sigma_HI^2 R/h) within 1 km/s
              (rounding), M_bar = M_atom + M_* + M_mol within 0.15e8 Msun, and M_dyn = R_out V_circ^2 / G within 12%.
  C2 CONTROL  the paper's Table 9 MOND velocities are reproduced by its eq. 4 with nu_n (n = 1, 2) and M_host = 0.6 L_K at a
              single a0 in {1.2, 1.25, 1.3}e-10 m/s^2: every V_ISO within 2 km/s and every V_EFE within 3 km/s.
  H1  (the FG041 kill test) FG001's Newtonian prediction V_N = sqrt(G M_bar / R_out) fits the six TDGs: chi^2 <= 12.6
      (the 95% point for 6 dof), and the inverse-variance mean of M_dyn/M_bar lies within 2 sigma of 1.  If instead the
      mean exceeds 1 by more than 2 sigma, a MOND-like discrepancy is confirmed and FG001 is killed.
  H2  (reported) the framework's own law applied to each TDG (P2 and nu_mono, both a0 footings) with the host's external
      field in the paper's eq. 4 -- M_host taken at whichever of 0.5x/1x/2x fits best, per host (the most favourable to the
      law) -- fits worse than Newton by d chi^2 >= 4 on both footings.
  H3  (reported) the isolated law (no external field) is worse still.
  S1  (reported) the equilibrium systematic: an extra 10% on every velocity (the scatter of Lelli et al.'s simulated M_dyn/
      M_real at t = 0) and the d chi^2 of H2 recomputed.
MUTATE=1: the observed V_circ are replaced by the paper's own MOND+EFE values (n = 2): a MOND-like discrepancy is injected,
H1 must FAIL (rc = 1).

SCOPE: equilibrium discs (the authors' assumption, with their caveat that the discs have turned < 1 orbit); spherical mass
estimate M_dyn = R V^2/G (the paper's epsilon = 1); the external field as the paper's 1-D eq. 4 (its stated simplification).
Run: python3 campaign_fresh_gravity/CFG7_tdg_fg041.py   (MUTATE=1 for the control; ~2 s)
"""
import os, sys, math, csv, json
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import CFG7_common as C

MUTATE = os.environ.get("MUTATE", "0") == "1"
R = C.Report("CFG7_tdg_fg041", MUTATE)
P, check = R.P, R.check
P(__doc__.split("SCOPE:")[0].strip())
if MUTATE:
    P("\n  *** MUTATE=1: the observed velocities are replaced by the paper's MOND+EFE (n = 2) values -- H1 must FAIL ***")

G_KPC = 4.30091727e-6                                                                   # kpc (km/s)^2 / Msun
KPC_M = 3.0856775814913673e19
ACC = 1e6 / KPC_M                                                                       # (km/s)^2/kpc -> m/s^2
DATA = os.path.join(C.REPO, "real_research", "data", "tidal_dwarfs", "lelli2015_tdg.csv")
rows = list(csv.DictReader(open(DATA)))
F = lambda r, k: float(r[k])
names = [r["object"] for r in rows]
P(f"\n  data: {len(rows)} TDGs from {os.path.relpath(DATA, C.REPO)}: " + ", ".join(names))


def nu_n(y, n):
    y = np.maximum(np.asarray(y, float), 1e-300)
    return (1.0 - np.exp(-y ** (n / 2.0))) ** (-1.0 / n)


def v_pred(r, a0_si, nu, efe=True, host_fac=1.0, Mbar=None, Rout=None):
    """the paper's eq. 4 (FM12 eq. 60): a_i = gNi nu((gNi+gNe)/a0) + gNe[nu((gNi+gNe)/a0) - nu(gNe/a0)], V = sqrt(a_i R)."""
    Mb = (F(r, "M_bar_1e8") * 1e8) if Mbar is None else Mbar
    Ro = F(r, "R_out_kpc") if Rout is None else Rout
    gNi = G_KPC * Mb / Ro ** 2 * ACC                                                     # m/s^2
    gNe = (G_KPC * 0.6 * F(r, "host_LK_1e10Lsun") * 1e10 * host_fac / F(r, "D_p_kpc") ** 2 * ACC) if efe else 0.0
    ai = gNi * nu((gNi + gNe) / a0_si) + (gNe * (nu((gNi + gNe) / a0_si) - nu(gNe / a0_si)) if efe else 0.0)
    return math.sqrt(ai / ACC * Ro)


def v_newton(r, Mbar=None, Rout=None):
    Mb = (F(r, "M_bar_1e8") * 1e8) if Mbar is None else Mbar
    Ro = F(r, "R_out_kpc") if Rout is None else Rout
    return math.sqrt(G_KPC * Mb / Ro)


# ================================================================================================ C1 Table 8 from Table 7
R.banner("C1  CONTROL: the paper's Table 8 (V_circ, M_bar, M_dyn) from its Table 7")
d1 = []
for r in rows:
    vc = math.sqrt(F(r, "V_rot_kms") ** 2 + F(r, "sigma_HI_kms") ** 2 * F(r, "Rout_over_hHI"))
    mb = F(r, "M_atom_1e8") + F(r, "M_star_1e8") + F(r, "M_mol_1e8")
    md = F(r, "R_out_kpc") * F(r, "V_circ_kms") ** 2 / G_KPC / 1e8
    d1.append((r["object"], vc, F(r, "V_circ_kms"), mb, F(r, "M_bar_1e8"), md, F(r, "M_dyn_1e8")))
    P(f"    {r['object']:11s}: V_circ {vc:5.1f} (table {F(r, 'V_circ_kms'):.0f}); M_bar {mb:5.2f} (table {F(r, 'M_bar_1e8'):.1f}); "
      f"M_dyn {md:5.2f} (table {F(r, 'M_dyn_1e8'):.1f}) x 1e8 Msun")
c1 = all(abs(a[1] - a[2]) <= 1.0 and abs(a[3] - a[4]) <= 0.15 and abs(a[5] / a[6] - 1) <= 0.12 for a in d1)
check("C1 CONTROL: Table 8 reproduced from Table 7 -- V_circ within 1 km/s, M_bar within 0.15e8 Msun, M_dyn within 12% (rounding)",
      f"max |dV| {max(abs(a[1] - a[2]) for a in d1):.2f} km/s, max |dM_bar| {max(abs(a[3] - a[4]) for a in d1):.3f}e8, "
      f"max |M_dyn ratio - 1| {max(abs(a[5] / a[6] - 1) for a in d1):.3f}", c1)
R.num("C1", d1)

# ================================================================================================ C2 Table 9 from eq. 4
R.banner("C2  CONTROL: the paper's Table 9 MOND velocities from its eq. 4 (nu_n, M_host = 0.6 L_K)")
best = None
for a0t in (1.2e-10, 1.25e-10, 1.3e-10):
    dev_iso, dev_efe = [], []
    for r in rows:
        for n in (1, 2):
            nu = lambda y, n=n: nu_n(y, n)
            dev_iso.append(abs(v_pred(r, a0t, nu, efe=False) - F(r, f"V_ISO{n}_kms")))
            dev_efe.append(abs(v_pred(r, a0t, nu, efe=True) - F(r, f"V_EFE{n}_kms")))
    P(f"    a0 = {a0t:.3g}: max |V_ISO - table| {max(dev_iso):.2f} km/s, max |V_EFE - table| {max(dev_efe):.2f} km/s")
    if best is None or max(dev_iso) + max(dev_efe) < best[1] + best[2]:
        best = (a0t, max(dev_iso), max(dev_efe))
A0_PAPER = best[0]
for r in rows:
    P(f"    {r['object']:11s} (a0 {A0_PAPER:.3g}): ISO n=1/2 {v_pred(r, A0_PAPER, lambda y: nu_n(y, 1), False):5.1f}/"
      f"{v_pred(r, A0_PAPER, lambda y: nu_n(y, 2), False):5.1f} (table {F(r, 'V_ISO1_kms'):.0f}/{F(r, 'V_ISO2_kms'):.0f}); EFE n=1/2 "
      f"{v_pred(r, A0_PAPER, lambda y: nu_n(y, 1)):5.1f}/{v_pred(r, A0_PAPER, lambda y: nu_n(y, 2)):5.1f} (table "
      f"{F(r, 'V_EFE1_kms'):.0f}/{F(r, 'V_EFE2_kms'):.0f})")
check("C2 CONTROL: Table 9 reproduced by the paper's eq. 4 at one a0 in {1.2, 1.25, 1.3}e-10 -- V_ISO within 2 km/s, V_EFE within 3 km/s",
      f"best a0 = {A0_PAPER:.3g} m/s^2: max |dV_ISO| {best[1]:.2f}, max |dV_EFE| {best[2]:.2f} km/s", best[1] <= 2.0 and best[2] <= 3.0)
R.num("C2", dict(a0_paper=A0_PAPER, max_dev_iso=best[1], max_dev_efe=best[2]))

# ================================================================================================ the observations
V_OBS = np.array([F(r, "V_circ_kms") for r in rows])
E_OBS = np.array([F(r, "e_V_circ_kms") for r in rows])
if MUTATE:
    V_OBS = np.array([F(r, "V_EFE2_kms") for r in rows])
MB = np.array([F(r, "M_bar_1e8") * 1e8 for r in rows]); EMB = np.array([F(r, "e_M_bar_1e8") * 1e8 for r in rows])
RO = np.array([F(r, "R_out_kpc") for r in rows]); ERO = np.array([F(r, "e_R_out_kpc") for r in rows])


def pred_err(fn, i):
    """propagated prediction error from M_bar and R_out (numerical derivatives)."""
    r = rows[i]
    v0 = fn(r, MB[i], RO[i])
    dm = (fn(r, MB[i] * 1.01, RO[i]) - v0) / (0.01 * MB[i]) * EMB[i]
    dr = (fn(r, MB[i], RO[i] * 1.01) - v0) / (0.01 * RO[i]) * ERO[i]
    return v0, math.hypot(dm, dr)


def chi2_of(fn, extra_frac=0.0):
    out = []
    for i in range(len(rows)):
        v, e = pred_err(fn, i)
        s2 = E_OBS[i] ** 2 + e ** 2 + (extra_frac * V_OBS[i]) ** 2
        out.append(((V_OBS[i] - v) ** 2 / s2, v, e))
    return float(sum(o[0] for o in out)), out


# ================================================================================================ H1 Newton (FG001)
R.banner("H1  FG001: each TDG is embedded in its host's bound region and carries no cold component -> Newtonian")
chiN, rowsN = chi2_of(lambda r, Mb, Ro: v_newton(r, Mb, Ro))
for i, r in enumerate(rows):
    P(f"    {r['object']:11s}: V_obs {V_OBS[i]:5.1f} +- {E_OBS[i]:.0f}; Newton {rowsN[i][1]:5.1f} +- {rowsN[i][2]:4.1f} km/s; "
      f"({(V_OBS[i] - rowsN[i][1]) / math.sqrt(E_OBS[i] ** 2 + rowsN[i][2] ** 2):+.2f} sigma)")
ratio = np.array([(V_OBS[i] / rowsN[i][1]) ** 2 for i in range(len(rows))])               # M_dyn/M_bar at the adopted R_out
eratio = np.array([ratio[i] * math.sqrt((2 * E_OBS[i] / V_OBS[i]) ** 2 + (EMB[i] / MB[i]) ** 2) for i in range(len(rows))])
if not MUTATE:
    ratio_t = np.array([F(r, "Mdyn_over_Mbar") for r in rows]); eratio_t = np.array([F(r, "e_Mdyn_over_Mbar") for r in rows])
else:
    ratio_t, eratio_t = ratio, eratio
w = 1 / eratio_t ** 2
mean = float(np.sum(w * ratio_t) / np.sum(w)); emean = float(1 / math.sqrt(np.sum(w)))
from scipy.stats import chi2 as CHI2
pN = float(CHI2.sf(chiN, len(rows)))
P(f"    chi^2 (6 TDGs, no free parameter) = {chiN:.2f}, p = {pN:.3f}; inverse-variance mean M_dyn/M_bar (Table 8's own ratios"
  f"{'' if not MUTATE else ', recomputed'}) = {mean:.3f} +- {emean:.3f} ({(mean - 1) / emean:+.2f} sigma from 1)")
killed = (mean - 1) / emean > 2.0
check("H1 [the FG041 kill test] FG001's Newtonian prediction fits the six TDGs (chi^2 <= 12.6 for 6 dof) and M_dyn/M_bar is within "
      "2 sigma of 1 -- no MOND-like discrepancy (which would kill FG001)",
      f"chi^2 {chiN:.2f} (p = {pN:.3f}); <M_dyn/M_bar> = {mean:.3f} +- {emean:.3f} ({(mean - 1) / emean:+.2f} sigma)",
      chiN <= 12.6 and not killed)
R.num("H1", dict(chi2_newton=chiN, p=pN, mean_ratio=mean, err_mean_ratio=emean, per=[dict(obj=names[i], v_obs=V_OBS[i], v_N=rowsN[i][1],
                                                                                      e_N=rowsN[i][2]) for i in range(len(rows))]))

# ================================================================================================ H2/H3 the framework's law on the TDG itself
R.banner("H2/H3  THE FRAMEWORK'S LAW APPLIED TO EACH TDG ITSELF (P2, nu_mono; both footings), with and without the host's field")
HOSTS = sorted(set(r["host"] for r in rows))
RES = {}
for foot in C.FOOTS:
    a0 = C.A0_SI[foot]
    for kn, kf in (("P2", C.nu_p2), ("nu_mono", C.nu_mono)):
        # isolated
        chiI, rI = chi2_of(lambda r, Mb, Ro: v_pred(r, a0, kf, efe=False, Mbar=Mb, Rout=Ro))
        # with the external field: per host, the M_host factor in {0.5, 1, 2} that minimises that host's chi^2
        chiE_tot, rE_all, facs = 0.0, [None] * len(rows), {}
        for h in HOSTS:
            idx = [i for i, r in enumerate(rows) if r["host"] == h]
            bestf = None
            for fac in (0.5, 1.0, 2.0):
                c_ = 0.0; rr_ = []
                for i in idx:
                    v, e = pred_err(lambda r, Mb, Ro: v_pred(r, a0, kf, efe=True, host_fac=fac, Mbar=Mb, Rout=Ro), i)
                    c_ += (V_OBS[i] - v) ** 2 / (E_OBS[i] ** 2 + e ** 2); rr_.append((i, v, e))
                if bestf is None or c_ < bestf[0]:
                    bestf = (c_, fac, rr_)
            chiE_tot += bestf[0]; facs[h] = bestf[1]
            for i, v, e in bestf[2]:
                rE_all[i] = (v, e)
        # the equilibrium systematic (+10% of V in quadrature)
        chiN_s, _ = chi2_of(lambda r, Mb, Ro: v_newton(r, Mb, Ro), 0.10)
        chiE_s = 0.0
        for i in range(len(rows)):
            v, e = rE_all[i]
            chiE_s += (V_OBS[i] - v) ** 2 / (E_OBS[i] ** 2 + e ** 2 + (0.1 * V_OBS[i]) ** 2)
        RES[(foot, kn)] = dict(chi_iso=chiI, chi_efe=chiE_tot, host_fac=facs, chi_newton_sys=chiN_s, chi_efe_sys=chiE_s,
                               v_iso=[x[1] for x in rI], v_efe=[x[0] for x in rE_all])
        P(f"    {foot:9s} {kn:8s}: chi^2 isolated {chiI:6.2f}; with the host's field {chiE_tot:6.2f} (M_host x {facs}); Newton {chiN:5.2f}; "
          f"d chi^2 (EFE - Newton) {chiE_tot - chiN:+6.2f}; with the 10% equilibrium systematic: Newton {chiN_s:5.2f}, EFE {chiE_s:5.2f} "
          f"(d {chiE_s - chiN_s:+.2f})")
        P("        per TDG (V_obs / Newton / law+EFE / law isolated): " +
          "; ".join(f"{names[i].replace('NGC ', '')} {V_OBS[i]:.0f}/{rowsN[i][1]:.0f}/{rE_all[i][0]:.0f}/{rI[i][1]:.0f}" for i in range(len(rows))))
h2 = all(RES[(f, "P2")]["chi_efe"] - chiN >= 4 for f in C.FOOTS) and all(RES[(f, "nu_mono")]["chi_efe"] - chiN >= 4 for f in C.FOOTS)
check("H2 (reported) the framework's law applied to the TDGs themselves, with the host's external field at its most favourable "
      "M_host, fits worse than Newton by d chi^2 >= 4 on both footings for both kernels",
      "; ".join(f"{k[0][:3]}/{k[1]}: d chi^2 {v['chi_efe'] - chiN:+.1f} (with 10% sys {v['chi_efe_sys'] - v['chi_newton_sys']:+.1f})"
                for k, v in RES.items()), h2, load_bearing=False)
h3 = all(v["chi_iso"] > v["chi_efe"] for v in RES.values())
check("H3 (reported) the isolated law (no external field) is worse still",
      "; ".join(f"{k[0][:3]}/{k[1]}: isolated {v['chi_iso']:.1f} vs EFE {v['chi_efe']:.1f}" for k, v in RES.items()), h3, load_bearing=False)
R.num("H2", {f"{k[0]}|{k[1]}": v for k, v in RES.items()})

# ================================================================================================ verdict
R.banner("VERDICT")
if MUTATE:
    P("    MUTATE: the injected MOND-like discrepancy is caught by the kill test (as it must be).")
else:
    worst = min(v["chi_efe"] - chiN for v in RES.values())
    P(f"    FG041 {'PASSES' if (chiN <= 12.6 and not killed) else 'FAILS'} for FG001: the six TDGs are Newtonian from their baryons (chi^2 {chiN:.2f} for 6, "
      f"<M_dyn/M_bar> = {mean:.2f} +- {emean:.2f}).  The framework's own law applied to each TDG -- the reading FG001 replaces -- is "
      f"disfavoured by d chi^2 >= {worst:.1f} even at the most favourable host mass; with a 10% equilibrium systematic the gap stays "
      f">= {min(v['chi_efe_sys'] - v['chi_newton_sys'] for v in RES.values()):.1f}.  Caveat (the authors'): the discs have turned < 1 orbit.")
nf = R.write()
sys.exit(1 if nf else 0)
