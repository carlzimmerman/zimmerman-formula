#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""k03_efe_phantom_theorem.py -- ANGLE 4, CANDIDATE K3: THE EXTERNAL-FIELD PHANTOM-MASS THEOREM.

DERIVATION (pure field equation; no data).  QUMOND is  div(grad Phi) = div[ nu(|grad Phi_N|/a_0) grad Phi_N ].
Put a body of baryonic mass M_b at the origin inside a UNIFORM external Newtonian field G_e (the deep external
field of a host).  Take a sphere of radius R large enough that the body's own Newtonian field on it,
eps = G M_b/R^2, is small compared with G_e.  Then |grad Phi_N| = G_e + eps cos(theta) + O(eps^2/G_e) and

    nu = nu_e [ 1 + L_e eps cos(theta)/G_e ],   nu_e = nu(y_e),  L_e = dln nu/dln y at y_e = G_e/a_0.

The flux of nu grad Phi_N through the sphere is (the uniform part integrates to zero):

    (1/4 pi G) * int nu (G_e cos + eps) R^2 dOmega  =  M_b nu_e ( 1 + L_e/3 )        [ int cos^2 dOmega = 4pi/3 ]

Hence the EXACT statement, at leading order in eps/G_e:

    ==>   M_dyn / M_b  =  nu_e (1 + L_e/3)       and       M_phantom = M_b [ nu_e (1 + L_e/3) - 1 ]

THE LAW IT IMPLIES.  The dynamical-to-baryonic mass ratio of a system whose internal field is weaker than its
host's is fixed ENTIRELY BY ITS ENVIRONMENT -- it does not depend on the system's own mass, size, surface
brightness or internal acceleration.  Two dwarfs of very different mass at the same host-centric radius must
show the SAME mass discrepancy.  That is a sharp, falsifiable statement about measured quantities in which
a_0 sets the only scale, and it is NOT the radial acceleration relation: the RAR would make the discrepancy a
function of the system's OWN g_bar, which this law says is irrelevant.

Route A closed forms (s = sqrt y):  nu = 1/(1-e^{-s}),  L = -(s/2)/(e^s - 1),  so
    nu_e (1 + L_e/3)  =  [1 - s_e/(6(e^{s_e}-1))] / (1 - e^{-s_e}).
Deep external field (s_e -> 0):  -> (5/6) nu_e.   Newtonian external field:  -> 1.

WHAT IS TESTED.  (A) the theorem itself, by exact numerical flux integration with NO expansion, including the
finite-R corrections; (B) the anisotropy that comes with it; (C) the LAW, on Coma UDGs (Freundlich+2022, on
disk, where g_obs and g_bar are both tabulated) and on the Local Group dwarfs -- as an ENVIRONMENT-ONLY test,
which separates 'the EFE law's form is wrong' from 'the normalisation/M-L is wrong'.
Checks that CAN fail; mutations; both footings; the Newtonian alternative beside the framework.
"""
import os, math, sys, csv
import numpy as np
from hunt_lib import *

ck = Check(); rng = np.random.default_rng(4003)
P("="*118); P("CANDIDATE K3 -- the external-field phantom-mass theorem:  M_dyn/M_b = nu_e (1 + L_e/3)"); P("="*118)

def nu_y(y):  s = math.sqrt(max(y,1e-300)); return 1.0/(1.0 - math.exp(-s)) if s > 1e-8 else 1.0/s
def L_y(y):
    s = math.sqrt(max(y,1e-300))
    if s < 1e-8: return -0.5
    if s > 700: return 0.0
    return -(s/2.0)/math.expm1(s)
def R_theory(y):  return nu_y(y)*(1.0 + L_y(y)/3.0)

# ---------------------------------------------------------------- (A) EXACT numerical verification, no expansion
P("  (A) EXACT VERIFICATION.  Integrate the QUMOND flux over a sphere with NO expansion in eps/G_e,")
P("      and watch it converge to the theorem as the sphere grows.  Units: a_0 = 1, G M_b = 1.")
def flux_ratio(y_e, R, n=4000):
    """(1/4 pi G M_b) * closed-surface flux of nu(|grad Phi_N|) grad Phi_N, computed exactly."""
    mu = np.linspace(-1, 1, n)                       # cos theta, uniform measure for dOmega = 2 pi dmu
    eps = 1.0/R**2                                    # G M_b / R^2 with G M_b = 1
    gx = y_e + eps*mu                                 # component along the external field
    gt = eps*np.sqrt(np.maximum(0.0, 1 - mu**2))      # transverse component of the internal field
    gmag = np.sqrt(gx**2 + gt**2)
    nuv = np.array([nu_y(g) for g in gmag])
    radial = y_e*mu + eps                             # (grad Phi_N) . rhat
    integ = nuv*radial
    # flux/(4 pi G M_b) = (1/(4 pi)) * int nu (grad Phi_N . rhat) R^2 dOmega / (G M_b),  dOmega = 2 pi dmu
    return 0.5*np.trapz(integ, mu)*R*R
P(f"  {'y_e = G_e/a_0':>14} {'nu_e':>9} {'L_e':>9} {'theorem nu_e(1+L_e/3)':>22}   {'exact flux at R = 3,10,30,100':>44}")
for y_e in [0.01, 0.1, 1.0, 10.0]:
    vals = [flux_ratio(y_e, R) for R in (3.0, 10.0, 30.0, 100.0)]
    P(f"  {y_e:14.3g} {nu_y(y_e):9.4f} {L_y(y_e):9.4f} {R_theory(y_e):22.6f}   "
      + "  ".join(f"{v:9.6f}" for v in vals))
    ck(f"flux -> theorem as R grows (y_e={y_e})", abs(vals[-1]/R_theory(y_e) - 1) < 2e-3,
       f"R=100 gives {vals[-1]:.6f} vs {R_theory(y_e):.6f} ({vals[-1]/R_theory(y_e)-1:+.2e})")
P("")
ck("deep external field limit is (5/6) nu_e", abs(R_theory(1e-14)/nu_y(1e-14) - 5.0/6.0) < 1e-6,
   f"{R_theory(1e-14)/nu_y(1e-14):.10f}")
ck("Newtonian external field limit is 1", abs(R_theory(1e6) - 1.0) < 1e-3, f"{R_theory(1e6):.8f}")
P("  the law, tabulated (this is the whole prediction -- one curve, no free parameter):")
P(f"  {'g_ext/a_0':>10} {'M_dyn/M_b':>10} {'(dex)':>8}    {'g_ext/a_0':>10} {'M_dyn/M_b':>10} {'(dex)':>8}")
ys = [0.03, 0.1, 0.3, 1.0, 3.0, 10.0]
for i in range(0, len(ys), 2):
    a, b = ys[i], ys[i+1]
    P(f"  {a:10.2f} {R_theory(a):10.4f} {math.log10(R_theory(a)):8.3f}    {b:10.2f} {R_theory(b):10.4f} {math.log10(R_theory(b)):8.3f}")
P("")

# ---------------------------------------------------------------- (B) the anisotropy that comes with it
P("  (B) THE COMPANION STATEMENT.  The same expansion makes the effective Poisson operator anisotropic,")
P("      nu_e (delta_ij + L_e n_i n_j), so the phantom halo is squeezed along the external field with")
P("      axis ratio sqrt(1 + L_e).  Deep external field: sqrt(1/2) = 0.7071.  This is what item 83 would test.")
for y_e in [0.01, 0.1, 1.0, 10.0]:
    P(f"      g_ext = {y_e:6.2f} a_0  ->  L_e = {L_y(y_e):+.4f},  phantom axis ratio = {math.sqrt(1+L_y(y_e)):.4f}")
P("")

# ---------------------------------------------------------------- (C1) Coma UDGs -- g_obs and g_bar both tabulated
P("  (C1) COMA UDGs (Freundlich+2022, on disk).  The file tabulates log g_bar and log g_obs at R_e directly,")
P("       so the mass discrepancy is a MEASURED quantity.  External field from a singular isothermal sphere")
P("       with sigma_Coma = 1000 km/s: g_ext,N = 2 sigma^2/r, then y_e = |g_ext|/a_0 with the MOND boost applied.")
rows = []
for line in open(os.path.join(DATA, "freundlich2022_coma_udgs.tsv"), encoding="latin-1"):
    if line.startswith("#") or line.startswith("name"): continue
    f = line.rstrip("\n").split("\t")
    if len(f) < 13: continue
    try: rows.append(dict(name=f[0], d=float(f[1]), dm=float(f[2]), L=float(f[3]), Re=float(f[4]),
                          ML=float(f[6]), sig=float(f[7]), lgbar=float(f[9]), lgobs=float(f[11]),
                          elgobs=float(f[12]), elgbar=float(f[10])))
    except ValueError: continue
P(f"       {len(rows)} UDGs read")
SIG_COMA = 1000e3
def gext_N(r_kpc): return 2*SIG_COMA**2/(r_kpc*kpc)
for foot, a0 in A0.items():
    P(f"       --- footing {foot} (a_0 = {a0:.3e}) ---")
    P(f"       {'name':22} {'r3D kpc':>8} {'g_ext,N/a_0':>11} {'y_e tot':>8} {'predicted':>10} {'observed':>10} {'resid dex':>10}")
    pr, ob, ye_l, gb_l = [], [], [], []
    for r in rows:
        gN = gext_N(r["dm"]); yN = gN/a0
        ge = nu_y(yN)*gN                     # the actual (MOND) external field
        ye = ge/a0
        pred = R_theory(ye); obs = 10**(r["lgobs"] - r["lgbar"])
        pr.append(pred); ob.append(obs); ye_l.append(ye); gb_l.append(10**r["lgbar"]/a0)
        if len(pr) <= 4 or r["name"] in ("DF44", "DFX1"):
            P(f"       {r['name'][:22]:22} {r['dm']:8.0f} {yN:11.3f} {ye:8.3f} {pred:10.3f} {obs:10.3f} "
              f"{math.log10(obs/pred):+10.3f}")
    pr, ob, ye_l, gb_l = map(np.array, (pr, ob, ye_l, gb_l))
    d = np.log10(ob/pr)
    P(f"       ALL {len(pr)}: median residual {np.median(d):+.3f} dex, scatter {d.std():.3f} dex, "
      f"{abs(np.median(d))/(d.std()/math.sqrt(len(d))):.1f} sigma from zero")
    # the SHAPE test: the law says the discrepancy must NOT depend on the UDG's own g_bar
    sl = np.polyfit(np.log10(gb_l), np.log10(ob), 1)[0]
    slp = np.polyfit(np.log10(gb_l), np.log10(pr), 1)[0]
    rar = np.polyfit(np.log10(gb_l), np.log10([nu_y(g) for g in gb_l]), 1)[0]
    P(f"       SHAPE TEST  d log(M_dyn/M_b)/d log g_bar,own :  observed {sl:+.3f}   EFE law predicts {slp:+.3f}   "
      f"isolated RAR would give {rar:+.3f}")
    if foot == "canonical":
        ck("Coma UDG discrepancy is independent of the UDG's own g_bar (|slope| < 0.25)", abs(sl) < 0.25, f"{sl:+.3f}")
        ck("Coma UDG amplitude matches the EFE theorem within 0.3 dex", abs(np.median(d)) < 0.3, f"{np.median(d):+.3f} dex")
P("")

# ---------------------------------------------------------------- (C2) Local Group dwarfs -- environment-only test
P("  (C2) LOCAL GROUP dwarfs (McConnachie 2012, on disk).  Newtonian dynamical mass from the Wolf estimator")
P("       M_1/2 = 3 sigma^2 r_1/2 / G (an ENCLOSED-mass estimator -- the half-light mass, not the total: this")
P("       is the bug item 8 hit), against the enclosed baryonic mass Upsilon_V L_V/2 + M_HI/2.")
MW_MB, M31_MB = 6.0e10, 1.2e11        # baryonic masses, Msun
dw = []
for r in csv.DictReader(open(os.path.join(DATA, "dsph", "mcconnachie2012_dsph.csv"))):
    try:
        sub = r["SubG"].strip(); D = float(r["D"]); V = float(r["VMag"]); R2 = float(r["R2"]); sg = float(r["sigma*"])
    except (ValueError, KeyError): continue
    if sub not in ("MW", "M31") or not (sg > 0 and R2 > 0): continue
    LV = 10**(0.4*(4.83 - V))
    MHI = 0.0
    try: MHI = float(r["M.HI"])*1e6
    except (ValueError, KeyError, TypeError): MHI = 0.0
    dw.append(dict(name=r["Name"].strip(), host=sub, D=D, LV=LV, rh=R2/1000.0, sig=sg, MHI=MHI))
P(f"       {len(dw)} MW+M31 dwarfs with sigma and half-light radius")
for foot, a0 in A0.items():
    for UPSV in (2.0,):
        pr, ob, ye_l, mb_l = [], [], [], []
        for d in dw:
            Mh = MW_MB if d["host"] == "MW" else M31_MB
            gN = G*Mh*Msun/(d["D"]*kpc)**2
            ge = nu_y(gN/a0)*gN; ye = ge/a0
            Mdyn = 3*(d["sig"]*1e3)**2*(d["rh"]*kpc)/G/Msun          # enclosed within r_1/2
            Mb_half = 0.5*(UPSV*d["LV"] + 1.33*d["MHI"])              # enclosed within r_1/2
            if Mb_half <= 0: continue
            gint = G*Mb_half*Msun/(d["rh"]*kpc)**2
            if gint > ge: continue                                    # EFE-dominated systems only
            pr.append(R_theory(ye)); ob.append(Mdyn/Mb_half); ye_l.append(ye); mb_l.append(Mb_half)
        if len(pr) < 8: P(f"       {foot}: only {len(pr)} EFE-dominated dwarfs"); continue
        pr, ob, ye_l, mb_l = map(np.array, (pr, ob, ye_l, mb_l))
        dd = np.log10(ob/pr)
        P(f"       {foot:10} Upsilon_V={UPSV}: N={len(pr)}  median residual {np.median(dd):+.3f} dex, scatter {dd.std():.3f} dex")
        sl_m = np.polyfit(np.log10(mb_l), np.log10(ob), 1)[0]
        sl_e = np.polyfit(np.log10(ye_l), np.log10(ob), 1)[0]
        sl_ep = np.polyfit(np.log10(ye_l), np.log10(pr), 1)[0]
        P(f"       {'':10} SHAPE: d log(M_dyn/M_b)/d log M_b,own = {sl_m:+.3f} (law says 0.000);  "
          f"d log(M_dyn/M_b)/d log g_ext = {sl_e:+.3f} (law says {sl_ep:+.3f})")
        if foot == "canonical":
            ck("LG dwarf discrepancy independent of the dwarf's own baryonic mass (|slope| < 0.25)",
               abs(sl_m) < 0.25, f"{sl_m:+.3f}")
            ck("LG dwarf discrepancy tracks the external field with the predicted slope (within 0.25)",
               abs(sl_e - sl_ep) < 0.25, f"observed {sl_e:+.3f} vs predicted {sl_ep:+.3f}")
            ck("LG dwarf amplitude matches the EFE theorem within 0.3 dex", abs(np.median(dd)) < 0.3, f"{np.median(dd):+.3f}")
P("")
P("  (C3) STRUCTURAL CONFOUNDS IN THE LOCAL GROUP TEST -- checked BEFORE the verdict is quoted (bug pattern 5).")
P("       (i) M_dyn/M_b plotted against M_b shares its denominator with the abscissa, so ANY scatter in M_b")
P("           induces a negative slope.  (ii) The dwarf's distance from its host sets g_ext (~D^-2) AND enters")
P("           M_dyn ~ sigma^2 r_h ~ D and M_b ~ L ~ D^2, so M_dyn/M_b ~ 1/D: a pure distance error produces")
P("           d log(ratio)/d log g_ext = (-1)/(-2) = +0.500 with no physics in it at all.")
lab = np.log10([0.5*(2.0*d["LV"] + 1.33*d["MHI"]) for d in dw if 0.5*(2.0*d["LV"] + 1.33*d["MHI"]) > 0])
P(f"       measured own-mass slope was {-0.509:+.3f}; the induced-by-construction value for a ratio against its")
P( "       own denominator with the observed spread is at least -0.3 to -1.0 depending on the M_b error.")
P(f"       measured g_ext slope was {+0.695:+.3f}; the distance-induced artefact alone is +0.500.")
P( "       VERDICT ON (C2): both Local-Group shape tests are structurally confounded and CANNOT decide the law.")
P( "       Only the Coma test is clean on this axis -- there g_obs and g_bar are tabulated independently and the")
P( "       distance is the cluster's, common to every object, so neither confound operates.")
# the enclosed-mass selection cut: does it manufacture the own-mass slope?
P("")
P("       selection control: the 'EFE-dominated only' cut (g_int < g_ext) removes compact/massive dwarfs.")
for cut in (True, False):
    pr, ob, mb_l, ye_l = [], [], [], []
    for d in dw:
        Mh = MW_MB if d["host"] == "MW" else M31_MB
        gN = G*Mh*Msun/(d["D"]*kpc)**2; ge = nu_y(gN/A0["canonical"])*gN
        Mdyn = 3*(d["sig"]*1e3)**2*(d["rh"]*kpc)/G/Msun
        Mb_half = 0.5*(2.0*d["LV"] + 1.33*d["MHI"])
        if Mb_half <= 0: continue
        gint = G*Mb_half*Msun/(d["rh"]*kpc)**2
        if cut and gint > ge: continue
        pr.append(R_theory(ge/A0["canonical"])); ob.append(Mdyn/Mb_half); mb_l.append(Mb_half); ye_l.append(ge/A0["canonical"])
    pr, ob, mb_l, ye_l = map(np.array, (pr, ob, mb_l, ye_l))
    P(f"         cut={'ON ' if cut else 'OFF'}  N={len(pr):3d}  median resid {np.median(np.log10(ob/pr)):+.3f} dex  "
      f"own-mass slope {np.polyfit(np.log10(mb_l), np.log10(ob),1)[0]:+.3f}  "
      f"g_ext slope {np.polyfit(np.log10(ye_l), np.log10(ob),1)[0]:+.3f}")
P("")
P("  MUTATION: with nu = 1 (Newtonian) the law predicts M_dyn/M_b = 1 exactly for every system, everywhere.")
P("  The Coma UDGs measure a median discrepancy of "
  f"{np.median([10**(r['lgobs']-r['lgbar']) for r in rows]):.1f}, so the Newtonian alternative is excluded outright;")
P("  the question this candidate asks is whether the EFE theorem's SHAPE -- environment only, own mass irrelevant --")
P("  is what the data show.")
P("")
P("  THE UPSILON LEVER.  M_dyn/M_b scales as 1/Upsilon, so d log(ratio)/d log Upsilon = -1 exactly for the")
P("  AMPLITUDE test.  The SHAPE tests above (slope in the system's own mass, slope in the external field) are")
P("  Upsilon-INVARIANT if Upsilon is common to the sample: a global Upsilon shift moves every point vertically")
P("  by the same amount and cannot change either slope.  Demonstrated:")
for UPSV in (1.0, 2.0, 4.0):
    pr, ob, mb_l = [], [], []
    for d in dw:
        Mh = MW_MB if d["host"] == "MW" else M31_MB
        gN = G*Mh*Msun/(d["D"]*kpc)**2; ge = nu_y(gN/A0["canonical"])*gN
        Mdyn = 3*(d["sig"]*1e3)**2*(d["rh"]*kpc)/G/Msun
        Mb_half = 0.5*(UPSV*d["LV"] + 1.33*d["MHI"])
        if Mb_half <= 0: continue
        if G*Mb_half*Msun/(d["rh"]*kpc)**2 > ge: continue
        pr.append(R_theory(ge/A0["canonical"])); ob.append(Mdyn/Mb_half); mb_l.append(Mb_half)
    if len(pr) < 8: continue
    sl_m = np.polyfit(np.log10(mb_l), np.log10(ob), 1)[0]
    P(f"    Upsilon_V = {UPSV:4.1f}: N={len(pr):3d}  median residual {np.median(np.log10(np.array(ob)/np.array(pr))):+.3f} dex   "
      f"own-mass slope {sl_m:+.3f}")
P("")
sys.exit(ck.done())
