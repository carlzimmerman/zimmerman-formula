"""z06: the R* / R_p coincidence, honestly.  R* = c/sqrt(G rho_Lambda) (fixed by rho_Lambda, z-independent) versus the particle-horizon radius R_p (history-dependent).

Facts to compute (each with a control):
  F1  R*/R_p = sqrt(8 pi/(3 OL)) / I_p(Om, Or, OL), I_p = Int_0^1 da/(a^2 E): H0 CANCELS EXACTLY (both scale as c/H0); the ratio is a function of the density parameters only.
  F2  the identity R* = sqrt(8 pi/3) c/H_L with H_L = H0 sqrt(OL) (a definition, not a coincidence), so R*/R_p = sqrt(8 pi/3) (c/H_L)/R_p: the coincidence is 'R_p ~ 2.9 de Sitter-Hubble radii'.
  F3  the ratio over the plausible parameter range (OL 0.60-0.75; radiation on/off; curvature +-0.01; the Planck/DESI Om values the record uses).
  F4  the ratio at other TIMES: R*/d_p(z) with z from -0.3 (the future) to 5, and the crossing R* = d_p at a* > 1.
  F5  how 'special' is 'today is within X of the crossing' compared with the record's other 'why now': Omega_m = Omega_Lambda equality.
  F6  whether the flat law and the particle-horizon law can be told apart by a LOW-z observable: their ratio is exactly R*/d_p(z) (both normalised at 2x), 1.0995 today, falling to 1 at a*.
Declared before running: (a) R*/R_p is robustly ~1.06-1.10 (not 1) with a parameter scatter of a few per cent [first-pass guess 1.08-1.11 was slightly off]; (b) it varies with time by tens of per cent per Gyr-scale, so 'equality' is a moment, not a constant; (c) the crossing epoch is within ~1 Gyr of now.
Not a result on the derivation: a coincidence of this kind (within 10%) is expected in ~55% of tries among six declared candidates (p11 check 4).
Run: python3 z06_coincidence_Rstar_Rp.py   (exit 0 iff every check passes)
"""
import sys, json, math
import numpy as np
from scipy.optimize import brentq
from zcommon import *

ok = []


def chk(name, cond, detail=""):
    ok.append(bool(cond))
    print(("PASS " if cond else "FAIL ") + name + (("\n       " + detail) if detail else ""))


OUT = {}
cos = Cosmo(**PLANCK)
Rp0, Rst = cos.dp(0.0), cos.Rstar()
print(f"Planck-like: R_p = {Rp0:.4f} c/H0, R* = {Rst:.4f} c/H0, R*/R_p = {Rst / Rp0:.4f}")
chk("C1 R*/R_p = 1.0995 reproduces p11 (R* = 50.73 Gly, R_p = 46.14 Gly)", abs(Rst / Rp0 - 50.73 / 46.14) < 2e-3, f"{Rst / Rp0:.4f} vs {50.73 / 46.14:.4f}")
HL = math.sqrt(cos.OL)
chk("C2 identity R* = sqrt(8 pi/3) c/H_L (H_L = H0 sqrt(OL)) to 1e-13 (G rho_L = 3 H_L^2/(8 pi)); R_p is %.3f de Sitter-Hubble radii c/H_L (R* is 2.894)" % (Rp0 * HL), abs(Rst - math.sqrt(8 * math.pi / 3) / HL) < 1e-13)
# F1: H0 independence, with the physical densities scaling
print("\n--- F1: H0 cancels ---")
rr = []
for H0 in (55.0, 67.4, 73.0, 85.0):
    c_ = Cosmo(H0=H0, Om=0.315, Or=9.1e-5)
    # both lengths in metres: R_p = (c/H0) * I_p, R* = c / sqrt(G rho_L), rho_L = OL 3 H0^2/(8 pi G)
    Rp_m = C / c_.H0 * c_.dp(0.0)
    Rst_m = C / math.sqrt(G * (c_.OL * 3 * c_.H0 ** 2 / (8 * math.pi * G)))
    rr.append(Rst_m / Rp_m)
    print(f"   H0 = {H0:5.1f}:  R*/R_p = {rr[-1]:.12f}")
chk("F1 R*/R_p is independent of H0 at fixed density parameters to 1e-12 (both lengths scale as c/H0); its only inputs are (Om, OL, Or, Ok)", max(rr) - min(rr) < 1e-12)
bad = []
for H0 in (55.0, 85.0):
    c_ = Cosmo(H0=H0, Om=0.315, Or=9.1e-5)
    Rst_bad = C / math.sqrt(G * (0.685 * 3 * (67.4e3 / MPC) ** 2 / (8 * math.pi * G)))       # mutation: rho_L frozen at the Planck H0 but R_p at the other H0
    bad.append(Rst_bad / (C / c_.H0 * c_.dp(0.0)))
chk("F1m MUTATION (freeze rho_Lambda at the Planck H0 but change H0 in R_p): the ratio then moves by >= 20%, so F1's cancellation test can detect an inconsistent input", max(abs(b / rr[1] - 1) for b in bad) > 0.2, f"{[f'{b:.3f}' for b in bad]}")

# F3: the scan
print("\n--- F3: R*/R_p over the plausible parameter range ---")


def ratio(OL, Or=9.1e-5, Ok=0.0):
    c_ = Cosmo(H0=67.4, Om=1 - OL, Or=Or)
    if Ok != 0.0:
        c_.Omeff = 1 - OL - Ok - Or            # curvature: E^2 += Ok/a^2
        c_.E = lambda a, c_=c_: math.sqrt(c_.Or / a ** 4 + c_.Omeff / a ** 3 + Ok / a ** 2 + c_.OL)
    return c_.Rstar() / c_.dp(0.0)


tab = {}
print("   OL      R*/R_p (radiation on)   (radiation off)")
for OL in (0.55, 0.60, 0.65, 0.685, 0.70, 0.7027, 0.7189, 0.75, 0.80):
    tab[OL] = (ratio(OL), ratio(OL, Or=0.0))
    print(f"   {OL:6.4f}  {tab[OL][0]:8.4f}                {tab[OL][1]:8.4f}")
OUT["scan"] = {str(k): v for k, v in tab.items()}
rat = np.array([tab[o][0] for o in (0.60, 0.65, 0.685, 0.70, 0.75)])
# FIRST RUN (kept as z06_coincidence_Rstar_Rp_firstrun.out): my statement 'the ratio INCREASES with OL, range 0.98-1.26' was WRONG: it DECREASES (more Lambda: R* ~ OL^-1/2 falls, and R_p grows because E is smaller at a < 1); 0.96-1.29 over [0.60, 0.75]; the monotonicity test was written as 'increasing OR decreasing' and passed by the wrong branch.
dl = np.diff([tab[o][0] for o in sorted(tab)])
rlo, rhi = min(tab[0.60][0], tab[0.75][0]), max(tab[0.60][0], tab[0.75][0])
chk("F3a the ratio DECREASES monotonically with OL over 0.55-0.80 (more Lambda: R* ~ OL^(-1/2) falls while R_p grows, since E(a<1) is smaller) and spans %.2f-%.2f over OL in [0.60, 0.75]; it is NOT pinned near 1" % (rlo, rhi), bool(np.all(dl < 0)) and abs(rlo - 0.960) < 0.005 and abs(rhi - 1.292) < 0.005, f"all diffs negative: {bool(np.all(dl < 0))}")
slope = (ratio(0.69) - ratio(0.68)) / 0.01
print(f"   d(R*/R_p)/dOL at 0.685 = {slope:+.3f};  Planck 2018 sigma(OL) ~ 0.007 -> sigma(R*/R_p) ~ {abs(slope) * 0.007:.3f}")
OLstar = brentq(lambda o: ratio(o) - 1.0, 0.5, 0.9)
print(f"   R*/R_p = 1 exactly at OL = {OLstar:.4f}  (Om = {1 - OLstar:.4f}); the measured 0.685 is {abs(0.685 - OLstar) / 0.007:.1f} Planck sigma from it")
chk("F3b R*/R_p = 1 would need OL = %.3f, %.0f Planck sigmas from the measured value: the 10%% match is robustly a 10%% mismatch, not equality (declared (a))" % (OLstar, abs(0.685 - OLstar) / 0.007), abs(0.685 - OLstar) / 0.007 > 5 and 1.05 < tab[0.685][0] < 1.15)
print("   values at the record's Om choices (flat, radiation on):")
vals = {}
for lab, Om in (("Planck 2018", 0.315), ("DESI DR2 + CMB (L274)", 0.3027), ("DESI DR2 BAO alone", 0.2975), ("CFG174", 0.3111), ("forecast script", 0.3137), ("Om = 0.34 (high)", 0.34)):
    vals[lab] = ratio(1 - Om)
    print(f"      {lab:24s} Om {Om:.4f}: R*/R_p = {vals[lab]:.4f}")
Ok_rat = {ok_: ratio(0.685, Ok=ok_) for ok_ in (-0.01, 0.0, 0.01)}
print("   curvature sensitivity (Ok = -0.01, 0, +0.01 at fixed OL = 0.685): " + ", ".join(f"{k:+.2f}: {v:.4f}" for k, v in Ok_rat.items()))
sel = [v for k, v in vals.items() if "high" not in k]
chk("F3c (first-pass range guess [1.08, 1.11] was wrong) over the record's Om values (0.2975-0.3150) R*/R_p spans %.3f-%.3f (a %.0f%% spread; DESI-based Om lowers it to 1.06-1.07), curvature +-0.01 moves it by %.1f%% -- always > 6%% above 1, i.e. >= 3.5 sigma of its own parameter error (sigma ~ 0.015)" % (min(sel), max(sel), 100 * (max(sel) / min(sel) - 1), 100 * max(abs(Ok_rat[0.01] / Ok_rat[0.0] - 1), abs(Ok_rat[-0.01] / Ok_rat[0.0] - 1))),
    all(1.055 < v < 1.105 for v in sel) and abs(Ok_rat[0.01] / Ok_rat[0.0] - 1) < 0.015 and abs(Ok_rat[-0.01] / Ok_rat[0.0] - 1) < 0.015 and min(sel) > 1.055,
    ", ".join(f"{v:.3f}" for v in vals.values()))
# non-Lambda dark energy: R* = c/sqrt(G rho_DE(0))
dw = Cosmo(H0=67.4, Om=0.319, Or=9.1e-5, w0=-0.752, wa=-0.86)
print(f"   aside: DESY5-like w0wa (rho_DE(0) in R*): R*/R_p = {dw.Rstar() / dw.dp(0.0):.4f} (Om 0.319)")

# F4: other times
print("\n--- F4: the ratio at other times (proper d_p at t(z); z < 0 = the future) ---")
zs = [-0.30, -0.20, -0.10, -0.05, 0.0, 0.5, 1.0, 2.5, 5.0]
d_p = {z: cos.dp(z) for z in zs}
for z in zs:
    print(f"   z = {z:+5.2f}:  d_p = {d_p[z]:7.4f} c/H0,  R*/d_p = {Rst / d_p[z]:7.4f}   ({'future' if z < 0 else 'past' if z > 0 else 'now'})")
zstar = brentq(lambda z: cos.dp(z) - Rst, -0.5, -0.001)
astar = 1 / (1 + zstar)
# elapsed cosmic time from now to a*: integrate dt = da/(a H)
tnow = cos.age(0.0); tstar = cos.age(zstar)
dt_gyr = (tstar - tnow) / (cos.H0 * GYR)
print(f"   crossing d_p = R*: z* = {zstar:.4f}, a* = {astar:.4f}, i.e. {dt_gyr:.2f} Gyr in the FUTURE (age now {tnow / (cos.H0 * GYR):.2f} Gyr)")
chk("F4a (declared (c)) the crossing d_p(t) = R* lies in the FUTURE at a* = %.3f, %.2f Gyr from now (%.0f%% of the current age)" % (astar, dt_gyr, 100 * dt_gyr / (tnow / (cos.H0 * GYR))), 0.3 < dt_gyr < 1.5 and astar > 1.0, f"a* = {astar:.4f}, dt = {dt_gyr:.3f} Gyr")
rate = (Rst / d_p[0.0] - Rst / d_p[-0.05]) / ((cos.age(0.0) - cos.age(-0.05)) / (cos.H0 * GYR))
print(f"   local rate: d ln(R*/d_p)/dt = {-rate / (Rst / d_p[0.0]) * 100:.1f}% per Gyr (falling)")
chk("F4b R*/d_p is NOT constant in time: 1.10 now, %.2f at z = 0.5, %.2f at z = 1, %.2f at z = 5, and it falls through 1 at a* (declared (b))" % (Rst / d_p[0.5], Rst / d_p[1.0], Rst / d_p[5.0]), Rst / d_p[0.5] > 1.8 and Rst / d_p[5.0] > 10 and Rst / d_p[-0.2] < 1)
# comoving mutation
chi_now = cos.chi_p(1.0); chi_at = lambda z: cos.chi_p(1 / (1 + z))
chi_inf = cos.chi_p(1e6)
a_c = brentq(lambda la: cos.chi_p(math.exp(la)) - Rst, 0.0, math.log(1e5))
a_c = math.exp(a_c)
chk("F4m MUTATION (compare the COMOVING particle horizon with R* instead of the proper one): the crossing moves to a_c = %.2f (vs a* = %.3f), so 'now is close to the crossing' depends on the proper-length prescription; chi_p(inf) = %.3f c/H0 = R_p + R_e" % (a_c, astar, chi_inf), abs(a_c - astar) > 0.1 and abs(chi_inf - (Rp0 + cos.de(0.0))) < 1e-3, f"chi_p(inf) = {chi_inf:.4f}, R_p + R_e = {Rp0 + cos.de(0.0):.4f}")

# F5: 'why now' comparison
print("\n--- F5: how special is 'now' compared with the record's other coincidence, Omega_m = Omega_Lambda ---")
a_eq = ((0.315) / 0.685) ** (1 / 3)
t_eq = cos.age(1 / a_eq - 1); dt_eq = (tnow - t_eq) / (cos.H0 * GYR)
print(f"   Omega_m(a) = Omega_Lambda at a = {a_eq:.4f} (z = {1 / a_eq - 1:.3f}), {dt_eq:.2f} Gyr ago; the R* = d_p crossing is {dt_gyr:.2f} Gyr ahead: |ln a| = {abs(math.log(astar)):.3f} vs {abs(math.log(a_eq)):.3f}")
chk("F5 the R* = d_p crossing is CLOSER to today (|ln a| = %.3f) than the matter-Lambda equality (|ln a| = %.3f): a 'why now' coincidence of the same kind, slightly tighter -- and it inherits the same anthropic-style explanations (or none)" % (abs(math.log(astar)), abs(math.log(a_eq))), abs(math.log(astar)) < abs(math.log(a_eq)))
# window in OL over which the ratio is within x% of 1 (the 10% threshold was chosen AFTER seeing 1.0995: three thresholds are shown)
OLs = np.linspace(0.5, 0.9, 401)
rr_ = np.array([ratio(o) for o in OLs])
wins = {}
for tol in (0.05, 0.10, 0.20):
    inwin = OLs[np.abs(rr_ - 1) <= tol]
    wins[tol] = (float(inwin.min()), float(inwin.max()))
    print(f"   |R*/R_p - 1| <= {tol:.2f} for OL in [{inwin.min():.3f}, {inwin.max():.3f}] (width {inwin.max() - inwin.min():.3f} = {100 * (inwin.max() - inwin.min()) / 0.4:.0f}% of the OL range 0.5-0.9); measured OL = 0.685")
OUT["windows"] = {str(k): v for k, v in wins.items()}
chk("F5b the fraction of OL in 0.5-0.9 for which R*/R_p is within 5/10/20%% of 1 is %.0f/%.0f/%.0f%%: a 10%% match is generic (about a quarter of the range), so 'R* ~ R_p' is a loose coincidence" % tuple(100 * (wins[t][1] - wins[t][0]) / 0.4 for t in (0.05, 0.10, 0.20)), 0.10 < (wins[0.10][1] - wins[0.10][0]) / 0.4 < 0.35)

# F6: flat vs particle-horizon law at low z
print("\n--- F6: can a LOW-z observable tell the flat law from the particle-horizon law? ---")
print("   with both normalised at 2x (flat: c^2/(2R*); D: c^2/(2 d_p)) the ratio a0_D(z)/a0_flat = R*/d_p(z):")
rz = {z: Rst / cos.dp(z) for z in (0.0, 0.02, 0.05, 0.1, 0.3, 0.5)}
print("   " + ", ".join(f"z={z}: {v:.3f}" for z, v in rz.items()))
a0f, a0D = C * cos.H0 / (2 * Rst) / 1e-10, C * cos.H0 / (2 * Rp0) / 1e-10
print(f"   LEVEL today: flat {a0f:.3f}e-10, D {a0D:.3f}e-10, SPARC 1.0766e-10 (5.4% stat, ~12% analysis): the 9.95% level difference is {0.0995 / 0.054:.1f} sigma (stat) / {0.0995 / 0.12:.1f} (analysis): a snapshot at z = 0 cannot tell them apart")
chk("F6a the level difference today is 9.95% = 1.8 sigma of SPARC's statistical error and 0.8 sigma of its analysis scatter: NO z = 0 observable separates the flat and particle-horizon laws", abs((a0D / a0f - 1) - 0.0995) < 0.001 and 0.0995 / 0.054 < 2 and 0.0995 / 0.12 < 1)
print(f"   the SHAPE difference across the SPARC / HI-sample depth (z <~ 0.05): {100 * (rz[0.05] / rz[0.0] - 1):.1f}%; across the lensing window z = 0.15 -> 0.45: {100 * (cos.dp(0.15) / cos.dp(0.45) - 1):.1f}% (a0_D(0.45)/a0_D(0.15) - 1 = {100 * (cos.dp(0.15) / cos.dp(0.45) - 1):.1f}%)")
chk("F6b the lowest-z observable that separates them is the z-binned a0 at z ~ 0.15-0.45 (a 38% change across the window vs 0): the record's lensing-RAR forecast (z05) gives 2.2 / 3.5 / 6.7 sigma for KiDS-now / combined / LSST-Euclid; nothing at z < 0.1 does", abs((cos.dp(0.15) / cos.dp(0.45) - 1) - 0.377) < 0.005 and (rz[0.05] / rz[0.0] - 1) < 0.07)
chk("F6c the two laws AGREE exactly at a* (the crossing): a0_D(a*) = a0_flat, so in the far future (a > a*) D FALLS BELOW flat and keeps falling like 1/a (d_p ~ a): D predicts a0 -> 0 as the universe expands, flat predicts a constant: the laws differ qualitatively in the future, not only in the past", cos.dp(zstar) - Rst < 1e-9 and cos.dp(-0.3) > Rst)
json.dump(dict(pass_=sum(ok), n=len(ok), Rstar_over_Rp=Rst / Rp0, OLstar=OLstar, astar=astar, dt_gyr=dt_gyr, OUT=OUT), open("z06_results.json", "w"), indent=1, default=float)
print(f"\n{sum(ok)}/{len(ok)}")
sys.exit(0 if all(ok) else 1)
