#!/usr/bin/env python3
"""q05: the SIZE of the vacuum energy from dimensional transmutation, rho ~ Lambda_YM^4 = mu^4 exp(-32 pi^2/(b0 g^2(mu))).

This is a different question from the coefficient 4 in G rho = 4 a0^2 and is reported as such.  Nothing here is a derivation:
b0 (discrete) and g (continuous) are two free numbers and one number (rho/M_P^4 ~ 1e-123) is fitted.

  E1  required exponent x = ln(c_vac mu^4/rho_L), implied b0 g^2, g^2, alpha for pure SU(N) at mu = M_P, reduced M_P, 2e16, 1e10, 1e3 GeV
  E2  exact mu-dependence: at fixed Lambda, x changes by 4 per e-fold = 9.21 per DECADE (not O(1)); the implied 1/g^2(mu) shifts by (b0/8 pi^2) ln 10
  E3  sensitivity: a factor 4 in rho is dx = 1.386, i.e. a 0.5% shift in g^2; two-loop term and one heavy flavour change rho by factors >> 4
  E4  decoys: targets 1e-100 ... 1e-150 are all hit by b0 g^2 within a +-20% band -> no discriminating power
  E5  the MM/dS coupling g^2 = 16 pi hbar G/L^2 gives x ~ 1e122 (excluded, lane A)
"""
import sys, math
import numpy as np
from scipy.optimize import brentq

ok = []
def chk(name, cond):
    ok.append(bool(cond)); print(("PASS " if cond else "FAIL ") + name)

pi = math.pi
Gv, hv, cv = 6.67430e-11, 1.054571817e-34, 299792458.0
Mpc = 3.0856775814913673e22
eV = 1.602176634e-19
def rho_GeV4(H0kms, OL):
    H0 = H0kms * 1e3 / Mpc
    rho = OL * 3 * H0**2 * cv**2 / (8 * pi * Gv)
    return (rho * (hv * cv)**3)**0.25 / eV / 1e9        # rho^(1/4) in GeV ; rho = this^4 GeV^4
MP = math.sqrt(hv * cv**5 / Gv) / eV / 1e9              # GeV
MPr = MP / math.sqrt(8 * pi)
print("     M_P = %.4e GeV, reduced M_P = %.4e GeV" % (MP, MPr))
rho14 = rho_GeV4(67.4, 0.685)
rho14_b = rho_GeV4(73.0, 0.70)
print("     rho_L^(1/4) = %.3e GeV (H0=67.4) / %.3e GeV (H0=73)  -> rho_L/M_P^4 = %.2e / %.2e ; rho_L/Mbar_P^4 = %.2e" % (rho14, rho14_b, (rho14 / MP)**4, (rho14_b / MP)**4, (rho14 / MPr)**4))
chk("E1 rho_L/M_P^4 ~ 1e-123 (1.1e-123 at H0 = 67.4) and ~8e-121 in reduced-Planck units: the brief's 'about 1e-122' is right to within the Planck-mass convention", 5e-124 < (rho14 / MP)**4 < 3e-123 and 1e-121 < (rho14 / MPr)**4 < 2e-120)

def b0_pure(N): return 11.0 * N / 3.0
def b1_pure(N): return 34.0 * N**2 / 3.0

def x_req(mu, cvac=1.0, rho14=rho14):
    return math.log(cvac * mu**4 / rho14**4)               # x = 32 pi^2/(b0 g^2)

# ------------------------------------------------------------------ E1
mus = {"M_P": MP, "Mbar_P": MPr, "M_GUT 2e16": 2e16, "1e10": 1e10, "1 TeV": 1e3}
print("     required exponent x = 32 pi^2/(b0 g^2) and implied couplings (one-loop, c_vac = 1):")
hdr = "       mu          x      b0 g^2  |  SU(2): g^2 alpha^-1 | SU(3): g^2 alpha^-1 | SU(5): g^2 alpha^-1"
print(hdr)
tab = {}
for k, mu in mus.items():
    x = x_req(mu)
    b0g2 = 32 * pi**2 / x
    row = "       %-10s %6.1f  %6.3f  | " % (k, x, b0g2)
    for N in (2, 3, 5):
        g2 = b0g2 / b0_pure(N); row += "%6.4f %7.1f | " % (g2, 4 * pi / g2)
    tab[k] = (x, b0g2)
    print(row)
chk("E1 at mu = M_P the required exponent is 283 (b0 g^2 = 1.12): SU(3) pure glue needs alpha = g^2/4pi = 1/124", abs(tab["M_P"][0] - 283) < 3 and abs(4 * pi / (tab["M_P"][1] / 11) - 124) < 3)
chk("E1 one number (b0 g^2 ~ 1.1 at M_P, ~1.2-1.4 at lower mu) is fixed; b0 and g separately are NOT: pure SU(N) all fit with g^2 N = 0.30 ('t Hooft coupling), i.e. a 1-parameter family", abs(tab["M_P"][1] * 3 / 11 - 0.304) < 0.01)
# other common b0 values (one-loop, mu = M_P): all sit on the same hyperbola b0 g^2 = 1.116
named = {"SU(3), nf=6 (QCD above m_t)": 7.0, "SM SU(2)_L (b0 = 19/6)": 19.0 / 6.0, "SU(3) N=1 SYM (b0 = 3N = 9)": 9.0, "SU(5) pure glue": b0_pure(5), "SU(3) nf=13 (near loss of AF)": 11 - 26.0 / 3.0}
for lab, bb in named.items():
    g2 = tab["M_P"][1] / bb
    print("       %-34s b0 = %6.3f: g^2 = %.4f, alpha^-1 = %.1f" % (lab, bb, g2, 4 * pi / g2))
chk("E1 every common b0 (7, 19/6, 9, 55/3, 2.33) has a coupling that fits, alpha^-1 between 30 and 210: no b0 is preferred", all(20 < 4 * pi / (tab["M_P"][1] / bb) < 400 for bb in named.values()))
# c_vac and H0 footing sensitivity
dx_c = x_req(MP, 2.0) - x_req(MP, 1.0)
dx_H = x_req(MP, 1.0, rho14_b) - x_req(MP, 1.0, rho14)
print("     c_vac x2 shifts x by %.3f ; the H0 = 73 footing shifts x by %.3f (both << 283)" % (dx_c, dx_H))
chk("E1 an O(1) c_vac or the H0/Omega_L footing change x by <1, i.e. b0 g^2 by <0.4%", abs(dx_c) < 1 and abs(dx_H) < 1)

# ------------------------------------------------------------------ E2
Lam_fixed = rho14                                            # fixed Lambda = rho^(1/4) (c_vac = 1)
xs = {k: 4 * math.log(mu / Lam_fixed) for k, mu in mus.items()}
per_decade = (xs["1e10"] - xs["1 TeV"]) / 7.0
chk("E2 at fixed Lambda: x(mu) = 4 ln(mu/Lambda); the change per decade of mu is 4 ln 10 = 9.21 (measured %.3f)  [the brief's 'O(1) per decade' is really 9.2 per decade]" % per_decade, abs(per_decade - 4 * math.log(10)) < 1e-9)
chk("MUT E2 a wrong power (mu^3 rather than mu^4) would give 6.91 per decade and is rejected", abs(3 * math.log(10) - per_decade) > 1)
d_invg2 = b0_pure(3) / (8 * pi**2) * math.log(10)
print("     implied 1/g^2(mu) (SU(3)) moves by %.4f per decade of mu, against 1/g^2(M_P) = %.2f: %.2f%% per decade" % (d_invg2, 11 / tab["M_P"][1], 100 * d_invg2 / (11 / tab["M_P"][1])))
chk("E2 the implied coupling at a given scale drifts ~3%/decade (SU(3)); hence 'the coupling that hits 1e-123' is a statement about a scale choice", 0.02 < d_invg2 / (11 / tab["M_P"][1]) < 0.05)

# ------------------------------------------------------------------ E3 sensitivity
dx4 = math.log(4.0)
rel_g2 = dx4 / tab["M_P"][0]
print("     a factor 4 in rho is dx = ln 4 = %.3f, i.e. a %.2f%% change of g^2 at M_P (pure glue, any N)" % (dx4, 100 * rel_g2))
chk("E3 distinguishing rho by the coefficient 4 needs g^2(M_P) known to 0.5%", abs(100 * rel_g2 - 0.49) < 0.02)
def g2_from_lnratio(N, lnratio, loops):
    b0, b1 = b0_pure(N), b1_pure(N)
    f = lambda g2: 8 * pi**2 / (b0 * g2) + (b1 / (2 * b0**2) * math.log(b0 * g2 / (16 * pi**2)) if loops == 2 else 0.0) - lnratio
    return brentq(f, 1e-3, 3.0)
print("     two-loop effect (Lambda defined by the standard two-loop invariant), mu = M_P:")
res2 = {}
for N in (2, 3, 4, 5):
    lnr = x_req(MP) / 4
    g1, g2v = g2_from_lnratio(N, lnr, 1), g2_from_lnratio(N, lnr, 2)
    b0, b1 = b0_pure(N), b1_pure(N)
    fac = (b0 * g1 / (16 * pi**2)) ** (-2 * b1 / b0**2)          # rho_2loop/rho_1loop at fixed g
    res2[N] = (g1, g2v, fac)
    print("       SU(%d): g^2 one-loop %.4f, two-loop %.4f (shift %.1f%%); at FIXED g^2, rho changes by x%.3g" % (N, g1, g2v, 100 * (g2v / g1 - 1), fac))
chk("E3 the two-loop term shifts the required g^2 by 2-4%% (>> 0.5%%) and rho at fixed g by x%.0f (SU(3)), 3-4 orders of magnitude: it swamps the factor 4" % res2[3][2], all(abs(res2[N][1] / res2[N][0] - 1) > 0.015 for N in res2) and res2[3][2] > 1e3)
# threshold: one heavy Dirac fundamental fermion between m and M_P (b_high = b_low - 2/3) at fixed g^2(M_P)
def ln_ratio_threshold(N, g2P, m, dbeta):
    b_low = b0_pure(N)
    return (8 * pi**2 / g2P - dbeta * math.log(MP / m)) / b_low        # ln(M_P/Lambda)
g2P = res2[3][0]
print("     threshold effects at fixed g^2(M_P) = %.4f (SU(3)): one extra heavy Dirac fundamental (Delta b0 = -2/3) between m and M_P:" % g2P)
th = {}
for m in (2e16, 1e13, 1e10):
    l0 = ln_ratio_threshold(3, g2P, m, 0.0)
    l1 = ln_ratio_threshold(3, g2P, m, -2.0 / 3.0)
    th[m] = math.exp(-4 * (l1 - l0))                               # rho(with)/rho(without)
    print("       m = %.0e GeV: rho changes by x%.3f  (= e^{-%.2f})" % (m, th[m], 4 * (l1 - l0)))
chk("E3 a single heavy flavour at the GUT scale changes rho by x0.21 (4.7x): the same size as the coefficient 4 = e^1.39 that the puzzle asks about", abs(th[2e16] - 0.212) < 0.01)
chk("MUT E3 with the sign of Delta b0 reversed (a vector-like gauge boson instead of a fermion) rho would go UP: sign check", ln_ratio_threshold(3, g2P, 2e16, +2.0 / 3.0) < ln_ratio_threshold(3, g2P, 2e16, 0.0))

# ------------------------------------------------------------------ E4 decoys
print("     decoy targets rho/mu^4 at mu = M_P: required b0 g^2 (one-loop)")
decs = [1e-100, 1e-110, 1e-122, 1e-123, 1e-140, 1e-150]
vals = [32 * pi**2 / (-math.log(t)) for t in decs]
for t, v in zip(decs, vals):
    print("       target %.0e -> b0 g^2 = %.3f  (SU(3): alpha^-1 = %.1f)" % (t, v, 4 * pi / (v / 11)))
band = (max(vals) - min(vals)) / np.mean(vals)
chk("E4 six decoy magnitudes spanning 50 orders (1e-100 ... 1e-150) all land in b0 g^2 in [0.9, 1.4]: full spread %.0f%% -> the fit has no discriminating power" % (100 * band), 0.85 < min(vals) and max(vals) < 1.45)
chk("MUT E4 a hypothetical predictor 'b0 g^2 = 1.116 +- 1%' would separate rho_L (1e-123) from 1e-110 (the required b0 g^2 differs by 12 percent): any such claim needs g known to a few percent, and the two-loop term alone moves it by 3 percent", abs(vals[1] / vals[3] - 1) > 0.10)
# natural GUT-like coupling
g2_gut = 4 * pi / 25
print("     for alpha = 1/25 (GUT-like) the needed b0 is %.2f; for SU(3) with n_f flavours b0 = 11 - 2 n_f/3 (n_f = %.1f)" % (tab["M_P"][1] / g2_gut, (11 - tab["M_P"][1] / g2_gut) * 1.5))
chk("E4 a GUT-like alpha = 1/25 hits 1e-123 for b0 = 2.2, i.e. SU(3) with ~13 flavours: another discrete choice; the requirement is (b0, g) on a hyperbola, not a point", abs(tab["M_P"][1] / g2_gut - 2.2) < 0.1)

# ------------------------------------------------------------------ E5 MM coupling
Pi2 = 2.85e-122
g2_MM = 16 * pi / 3 * Pi2
x_MM = 32 * pi**2 / (11 * g2_MM)
print("     MM/dS gauge coupling g^2 = 16 pi hbar G/L^2 = %.2e gives x = 32 pi^2/(b0 g^2) = %.2e (b0 = 11): Lambda_YM/mu = exp(-x/4) = exp(-%.1e)" % (g2_MM, x_MM, x_MM / 4))
chk("E5 with the gauge-gravity coupling the exponent is ~1e122 instead of 283: that gauge theory does not transmute (lane A)", x_MM > 1e121)

print("\nsummary: the magnitude 1e-123 fixes ONE combination, b0 g^2(M_P) ~ 1.1 (= 32 pi^2/283); (b0, g) are two free numbers; the exponent moves 9.2 per decade of mu;")
print("         two-loop and a single GUT-scale flavour move rho by x4e3 and x0.21, i.e. more than the coefficient 4 the puzzle asks about. Fit, not derivation.")
print("\n%d/%d" % (sum(ok), len(ok)))
sys.exit(0 if all(ok) else 1)
