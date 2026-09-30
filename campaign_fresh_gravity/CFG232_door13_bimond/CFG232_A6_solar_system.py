#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
CFG232_A6_solar_system -- G5b: Q2 (CFG7 H1 recipe: tide = max(|dg_ph/dR|, g_ph/R); (a) the Sun's own field at Saturn, isolated; (b) the Milky Way's
phantom tide at the Sun) and gamma - 1 at Saturn from the designed slip.  Control C6.

C6 AS FROZEN said: 'the CFG7 H1 Milky-Way strict-law ratio 4.0-5.7x reproduced'.  The door-11 lane (CFG172 A2, control C5) already found that the H1 recipe
gives the MW phantom tide at 6e-5 x the bound and the Sun's own field at Saturn 6.3e3 x the bound; the '4.0-5.7' has another origin (a Q2 tidal quadrupole of
the strict law with an external field, different quantity).  My frozen expectation was wrong; the control is run as (i) reproduce H1's own numbers, (ii)
the frozen 4.0-5.7 statement, which FAILS and is kept.
"""
import os, sys, math
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import CFG232_common as C

R = C.Run("CFG232_A6_solar_system")
MUT = R.mutate
P = R.P
bite = []

GSI = 6.67430e-11
GMSUN = 1.32712440018e20
AU = 1.495978707e11
KPC = 3.0856775814913673e19
MSUN = 1.98847e30
Q2B = 5.2e-27
DES = {kn: C.Design(C.KERNELS[kn], 1.0, 1.0, +1) for kn in ("P2", "nu_mono")}


def bimond_phantom(kn, gN_si, a0):
    """phantom acceleration (Phi' - g_N) of the designed BIMOND law at Newtonian source acceleration gN_si (m/s^2)"""
    y = gN_si / a0
    f = C.forward(DES[kn].mfun, 1.0, 1.0, +1, float(y))
    return (f["Phi"] - y) * a0 if f["ok"] else float("nan")


def tide(gph_fun, Rm):
    d = (gph_fun(Rm * 1.01) - gph_fun(Rm * 0.99)) / (0.02 * Rm)
    return max(abs(d), gph_fun(Rm) / Rm)


R.banner("gamma_PPN at Saturn from the designed slip (Psi'/Phi' - 1) and the Cassini window (2.1 +- 2.3)e-5 (2 sigma)")
RS = 9.537 * AU
gs = GMSUN / RS ** 2
gam = {}
for foot, a0 in C.FOOTS.items():
    for kn in ("P2", "nu_mono"):
        y = gs / a0
        f = C.forward(DES[kn].mfun, 1.0, 1.0, +1, float(y))
        gam[f"{foot}/{kn}"] = f["Psi"] / f["Phi"] - 1
        P(f"  {foot:9s} {kn:8s}: y = g_N/a0 = {y:.3e}, Psi'/Phi' - 1 = {gam[f'{foot}/{kn}']:+.3e}")
lo, hi = 2.1e-5 - 2 * 2.3e-5, 2.1e-5 + 2 * 2.3e-5
ok_gam = all(lo <= v <= hi for v in gam.values())
R.check("G5b gamma: |Psi'/Phi' - 1| at Saturn inside the Cassini 2-sigma window (2.1 +- 2.3)e-5", ok_gam, f"values {[f'{v:+.1e}' for v in gam.values()]}, window [{lo:+.1e}, {hi:+.1e}]", kind="result")
R.num("gamma_saturn", gam)

R.banner("Q2: (a) the Sun's own phantom at Saturn (isolated, no external field), (b) the Milky Way's phantom tide at the Sun (CFG7 H1 recipe)")
MD, RD, MBUL, ABUL, MGAS, RGAS = 4.5e10, 2.6, 0.9e10, 0.5, 1.2e10, 5.0


def M_exp(Md, Rd, Rk):
    s = Rk / Rd
    return Md * (1 - (1 + s) * math.exp(-s))


def gN_MW(Rm):
    Rk = Rm / KPC
    M = M_exp(MD, RD, Rk) + M_exp(MGAS, RGAS, Rk) + MBUL * Rk ** 2 / (Rk + ABUL) ** 2
    return GSI * M * MSUN / Rm ** 2


R0 = 8.2 * KPC
Q2a, Q2b = {}, {}
for foot, a0 in C.FOOTS.items():
    for kn in ("P2", "nu_mono"):
        kern = C.KERNELS[kn]
        ref_a = lambda Rm, a0=a0, kern=kern: (float(kern(GMSUN / Rm ** 2 / a0)) - 1.0) * GMSUN / Rm ** 2
        bim_a = lambda Rm, a0=a0, kn=kn: bimond_phantom(kn, GMSUN / Rm ** 2, a0)
        ref_b = lambda Rm, a0=a0, kern=kern: (float(kern(gN_MW(Rm) / a0)) - 1.0) * gN_MW(Rm)
        bim_b = lambda Rm, a0=a0, kn=kn: bimond_phantom(kn, gN_MW(Rm), a0)
        Q2a[f"{foot}/{kn}"] = dict(ref=tide(ref_a, RS) / Q2B, bimond=tide(bim_a, RS) / Q2B)
        Q2b[f"{foot}/{kn}"] = dict(ref=tide(ref_b, R0) / Q2B, bimond=tide(bim_b, R0) / Q2B, tide=tide(ref_b, R0), gN=gN_MW(R0))
        P(f"  {foot:9s} {kn:8s}: (a) Sun@Saturn Q2/bound = {Q2a[f'{foot}/{kn}']['bimond']:.3e} (kernel {Q2a[f'{foot}/{kn}']['ref']:.3e});  (b) MW@Sun Q2/bound = {Q2b[f'{foot}/{kn}']['bimond']:.3e} (kernel {Q2b[f'{foot}/{kn}']['ref']:.3e})")
R.num("Q2_a_sun_saturn", Q2a); R.num("Q2_b_mw_sun", Q2b)

# controls: reproduce H1's committed numbers; the frozen C6 statement (4.0-5.7) is kept as a failed expectation
h1 = {"canonical/P2": 1.56e-31, "canonical/nu_mono": 2.20e-31, "alt/P2": 1.83e-31, "alt/nu_mono": 2.56e-31}
okh1 = all(abs(Q2b[k]["tide"] / v - 1) < 0.03 for k, v in h1.items()) and abs(Q2b["canonical/P2"]["gN"] / 1.055e-10 - 1) < 5e-3
R.check("C6a reproduces CFG7 H1's committed MW phantom-tide numbers (canonical P2 g_N(R0) = 1.055e-10, tide 1.56e-31 s^-2; nu_mono 2.20e-31; alt 1.83e-31 / 2.56e-31)", okh1,
        {k: f"{Q2b[k]['tide']:.3e}" for k in h1})
R.check("C6 (AS FROZEN) 'the strict-law MW ratio is 4.0-5.7x the ceiling' -- NOT what the H1 recipe gives (6e-5 x the bound); the 4.0-5.7 of gate 4.01 is a different quantity; KEPT as a failed expectation (declared: my frozen sentence was wrong, as in CFG172's C5)",
        4.0 <= Q2b["canonical/P2"]["bimond"] <= 5.7, f"H1-recipe MW@Sun / bound = {Q2b['canonical/P2']['bimond']:.2e}")
same = all(abs(v["bimond"] / v["ref"] - 1) < 1e-3 for v in list(Q2a.values()) + list(Q2b.values()))
R.check("the designed BIMOND law's phantom equals the strict kernel's to 1e-3 at Solar-System and Milky-Way accelerations (so Q2 is a property of the law, not of the mechanism)", same, "max ratio deviation < 1e-3")
a_fail = all(v["bimond"] > 1.0 for v in Q2a.values())
b_pass = all(v["bimond"] < 1.0 for v in Q2b.values())
R.check("G5b Q2 (a) Sun's own phantom at Saturn (isolated, no ownership): exceeds the 5.2e-27 s^-2 ceiling by >= 1e3 for both kernels and footings", a_fail, f"{min(v['bimond'] for v in Q2a.values()):.2e}..{max(v['bimond'] for v in Q2a.values()):.2e} x bound", kind="result")
R.check("G5b Q2 (b) MW phantom tide at the Sun: below the ceiling (passes only if the Sun's OWN phantom is absent = ownership, which BIMOND does not supply)", b_pass, f"{max(v['bimond'] for v in Q2b.values()):.1e} x bound", kind="result")
R.verdict("G5b Q2 (13a/13b/13c as a bare law)", "FAIL", "the Sun's own field at Saturn is 6e3..1.6e4 x the bound; the MW-tide reading passes only under an ownership rule that no sub-variant contains (Gap 1). A full 3D external-field solution is not computed.")
R.verdict("G5b gamma", "PASS" if ok_gam else "FAIL", f"Psi'/Phi' - 1 = {gam['canonical/P2']:+.1e} (P2, canonical) inside the window" if ok_gam else "outside the window")

R.finish(bite if MUT else None)
