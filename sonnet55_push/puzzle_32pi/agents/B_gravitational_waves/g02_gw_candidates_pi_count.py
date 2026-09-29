#!/usr/bin/env python3
"""g02_gw_candidates_pi_count.py -- lane B: is the puzzle a statement about a gravitational-wave / graviton quantity?  (c = 1; a0 = X sqrt(G rho_L))

PRE-DECLARATION (written before any number below is computed; the pi-counting rule):
  Target: a0 = (1/2) sqrt(G rho_L)  ->  X^2 = 1/4, no pi.   In terms of H_L (Friedmann H^2 = 8 pi G rho_L/3): a0 = H_L/Z, Z = sqrt(32 pi/3).
  Candidate quantities are fixed by physics (listed here), not by the target.  Each is assigned a predicted pi-content of X^2 BEFORE evaluation:
    Q1  classical Isaacson background, energy rho_GW = f rho_L, peak tidal (geodesic-deviation) acceleration at the reduced wavelength   predicted X^2 = 8 pi f
    Q2  memory kick of a burst carrying the Hubble-sphere energy: a = eta H, eta = normalised angular integral (pi cancels)            predicted X^2 = eta^2 (8 pi/3), eta pi-free (needs eta = 1/Z)
    Q3  de Sitter Bunch-Davies tensor amplitude (needs hbar): a = (1/2) H h_rms                                                       predicted X^2 = (32/3) hbar G H^2  (pi^0, hbar-dependent, ~1e-121)
    Q4  canonical graviton bath x horizon entropy (the record's chain)                                                                -> g03
    Q5  equation of state of a GW/graviton gas (enthalpy ratio, the '4/3' of formulation 6)                                          predicted (rho+p)/rho = D/(D-1)
  Two classes:  E (energy route, X^2 = 8 pi f) and K (kinematic route, a = r_K H with r_K algebraic).  To hit a0:  E needs f = 1/(32 pi);  K needs r_K = 1/Z (not algebraic).
Exit 0 iff every check (including controls) behaves as declared.
"""
import sys, math
import sympy as sp
import mpmath as mp

ok = []
def chk(n, c):
    ok.append(bool(c)); print(("PASS " if c else "FAIL ") + n)

G, rho, H, w, h0, f_, kap = sp.symbols('G rho_L H omega h0 f kappa', positive=True)
Xtarget2 = sp.Rational(1, 4)

def pi_exponent(expr):
    """k such that expr = rational * pi^k  (None if not of that form)"""
    e = sp.simplify(expr)
    for k in range(-3, 4):
        r = sp.simplify(e / sp.pi**k)
        if r.is_rational:
            return k, r
    return None

# ---------------------------------------------------------------- Q1
print("Q1  classical Isaacson background with rho_GW = f rho_L")
rho_GW = w**2 * h0**2 / (32 * sp.pi * G)              # Isaacson (g01 B2)
a_tid = w * h0 / 2                                     # peak tidal acceleration at r = 1/w (g01 D1)
X2_Q1 = sp.simplify(a_tid**2 / (G * rho))
fsol = sp.solve(sp.Eq(rho_GW, f_ * rho), h0)[0]
X2_f = sp.simplify(X2_Q1.subs(h0, fsol))
chk("Q1a  X^2 = 8 pi f  (predicted)", sp.simplify(X2_f - 8 * sp.pi * f_) == 0)
k_, r_ = pi_exponent(X2_f.subs(f_, 1))
chk("Q1b  f = 1 (GW energy = vacuum energy): X^2 = 8 pi, pi^1 -- predicted exponent 1 matches; X = %.4f  vs target 0.5" % float(sp.sqrt(8 * sp.pi)), k_ == 1 and r_ == 8)
fneed = sp.solve(sp.Eq(X2_f, Xtarget2), f_)[0]
chk("Q1c  to hit a0 the GW energy fraction must be f = 1/(32 pi) = %.5f (pi^-1: a solid-angle-type factor, not a rational energy ratio)" % float(fneed), sp.simplify(fneed - 1 / (32 * sp.pi)) == 0)
chk("C1  CONTROL: f = 1/32 (rational) does NOT reproduce a0", sp.simplify(X2_f.subs(f_, sp.Rational(1, 32)) - Xtarget2) != 0)
# the puzzle written in GW variables (a 'formulation 11')
X_of_kappa = sp.symbols('kappa', positive=True)
rate = sp.symbols('rate', positive=True)          # omega*h0 in units of sqrt(G rho_L)
sol = sp.solve(sp.Eq(rate / 2, X_of_kappa), X_of_kappa)[0]        # a_tid = (rate/2) sqrt(G rho_L) = kappa sqrt(G rho_L)
chk("Q1d  GW form of the puzzle: a_tid = a0 <=> omega h0 = sqrt(G rho_L) = 1/t_L  (strain rate = vacuum free-fall rate); unique root kappa = 1/2 at rate 1",
    sp.simplify(sol.subs(rate, 1) - sp.Rational(1, 2)) == 0)
chk("Q1e  equivalently <hdot_ab hdot_ab> = G rho_L, i.e. rho_L = 32 pi rho_GW : the 32 pi is exactly the canonical Isaacson normalisation of the a0-wave",
    sp.simplify((w * h0)**2 / (32 * sp.pi * G) - rho / (32 * sp.pi)).subs(h0, sp.sqrt(G * rho) / w) == 0)
# Omega_GW is pi-free in omega h0 / H
OmGW = sp.simplify(rho_GW / (3 * H**2 / (8 * sp.pi * G)))
chk("Q1f  Omega_GW = (omega h0)^2/(12 H^2): pi cancels between Isaacson 1/(32 pi G) and Friedmann 3H^2/(8 pi G)", sp.simplify(OmGW - (w * h0)**2 / (12 * H**2)) == 0)

# validity / data
print("   numbers (Planck-like flat LCDM, H0 = 67.4, Omega_L = 0.685; radiation Omega_r h^2 = 4.18e-5 incl. 3.046 neutrinos):")
H0 = 67.4; OL = 0.685; hh = H0 / 100
Omega_r = 4.18e-5 / hh**2; Omega_gam = 2.47e-5 / hh**2
f_need = 1 / (32 * math.pi)
Om_GW_need = f_need * OL
print("   f_needed = 1/(32 pi) = %.5f  -> Omega_GW(today) = %.4f" % (f_need, Om_GW_need))
dNeff_bound = 0.5                                     # generous; any bound >= 0.01 gives the same conclusion
rho_bound_over_gam = 0.1354 * dNeff_bound              # (7/8)(4/11)^(4/3) dNeff
ratio = (Om_GW_need / Omega_gam) / rho_bound_over_gam
# frequency at which a mode re-enters the horizon at BBN (T = 1 MeV, g* = 10.75), in units of H0
T_BBN_eV = 1.0e6; T0_eV = 2.725 * 8.617333e-5
zBBN = T_BBN_eV / T0_eV
H_BBN = 1.66 * math.sqrt(10.75) * (T_BBN_eV * 1e-9)**2 / 1.22e19 * 1.519e24      # 1/s
H0_s = H0 * 1000 / 3.0857e22
w_over_H0_BBN = H_BBN / (1 + zBBN) / H0_s
print("   BBN horizon: 1+z = %.2e, H_BBN = %.2f /s  -> a GW is radiation-like at BBN only if omega/H0 >~ %.1e today" % (zBBN, H_BBN, w_over_H0_BBN))
print("   for such a background: rho_GW/rho_gamma = %.1f vs allowed %.3f  -> excess x%.1e" % (Om_GW_need / Omega_gam, rho_bound_over_gam, ratio))
chk("Q1g  for omega/H0 >~ 1e8 (inside the horizon at BBN) a w = 1/3 background carrying f = 1/(32 pi) of rho_L exceeds the generous N_eff allowance by > 1e3", ratio > 1e3 and w_over_H0_BBN < 1e9)
chk("Q1h  and f = 1 (energy = rho_L) by > 1e5", (OL / Omega_gam) / rho_bound_over_gam > 1e5)
print("   NOT EVALUATED: 10 < omega/H0 < 1e8 (enters the horizon after BBN). There the background is still a w = 1/3 component of Omega = %.4f inside the horizon today,\n"
      "   i.e. dark radiation, not Lambda-like; I did not test it against the expansion history / CMB / BAO, so no exclusion is claimed for that window." % Om_GW_need)
print("   validity at omega = H (needed for the amplitude to be Hubble-scale):  h0 = sqrt(12 f) = %.3f for f = 1/(32 pi);  %.3f for f = 1" % (math.sqrt(12 * f_need), math.sqrt(12)))
chk("Q1i  at omega = H the needed amplitude h0 = 2/Z = %.4f is not << 1 and there is no scale separation (omega/H = 1): the Isaacson average is outside its validity; for omega/H >= 10 it is a w = 1/3 component (Q1g,h cover omega/H0 >~ 1e8; the window 10..1e8 is not evaluated, see above)" % (math.sqrt(12 * f_need)),
    abs(math.sqrt(12 * f_need) - 2 / math.sqrt(32 * math.pi / 3)) < 1e-12 and math.sqrt(12 * f_need) > 0.3)

# polarisation-state dependence of the identity rho = a^2/(8 pi G): linear vs circular at the same peak tidal acceleration
import numpy as np
def peak_tidal_and_energy(Aamp, Bamp, phase):
    tt = np.linspace(0, 2 * np.pi, 4001)
    fx_ = Aamp * np.cos(tt); gx_ = Bamp * np.cos(tt + phase)
    # tidal acceleration vector at radius r=1/omega: a = (1/2) omega^2 h_ij n_j r ; peak over time and direction n = sqrt of the largest eigenvalue magnitude of h
    lam = np.sqrt(fx_**2 + gx_**2)            # eigenvalues of [[f,g],[g,-f]] are +-sqrt(f^2+g^2)
    a_pk = 0.5 * lam.max()                     # in units omega * (1)  (omega=1, r=1)
    rho_ = (Aamp**2 + Bamp**2) / (32 * np.pi)  # Isaacson (g01 B2), omega = G = 1
    return a_pk, rho_
a_lin, r_lin = peak_tidal_and_energy(1.0, 0.0, 0.0)
a_cir, r_cir = peak_tidal_and_energy(1.0, 1.0, np.pi / 2)
ratio_lin = r_lin / (a_lin**2 / (8 * np.pi)); ratio_cir = r_cir / (a_cir**2 / (8 * np.pi))
print("   rho/(a_pk^2/(8 pi G)): linear = %.4f, circular = %.4f" % (ratio_lin, ratio_cir))
chk("Q1k  the identity rho_GW = a_pk^2/(8 pi G) holds for LINEAR polarisation (ratio 1); for CIRCULAR polarisation with the same peak tidal acceleration the ratio is 2, so 'the needed f' is 1/(32 pi) or 1/(64 pi) depending on the polarisation state: the GW reading of 32 pi is not even state-independent",
    abs(ratio_lin - 1) < 1e-6 and abs(ratio_cir - 2) < 1e-6)
chk("C1b CONTROL: the check distinguishes them (ratio_cir != ratio_lin)", abs(ratio_cir - ratio_lin) > 0.5)

# choice of length: natural radii r = lambdabar * pi^m (lambdabar = 1/omega, lambda/2 = pi lambdabar, lambda = 2 pi lambdabar)
exps = []
for m_, lbl in [(0, "lambdabar"), (1, "lambda/2"), (1, "lambda")]:
    rr_ = {"lambdabar": 1, "lambda/2": sp.pi, "lambda": 2 * sp.pi}[lbl]
    X2 = sp.simplify(8 * sp.pi * rr_**2)
    kk, _ = pi_exponent(X2)
    exps.append(kk)
    print("   radius r = %-9s : X^2 = %s  (pi^%d)  vs target 1/4" % (lbl, X2, kk))
chk("Q1j  for every natural radius r = (rational) x pi^m x lambdabar the exponent of pi in X^2 = 8 pi f (r/lambdabar)^2 is ODD (1+2m): the radius choice cannot reach pi^0; only a sqrt(pi) length scale (a Gaussian volume/norm, cf. p09) could", all(e % 2 == 1 for e in exps))

# ---------------------------------------------------------------- Q2  memory kick
print("\nQ2  memory: burst carrying the Hubble-sphere energy")
R = 1 / H
E_H = sp.Rational(4, 3) * sp.pi * rho * R**3
rho_L = 3 * H**2 / (8 * sp.pi * G)
dh = sp.simplify((4 * G * E_H / R).subs(rho, rho_L))
chk("Q2a  Hubble-sphere energy E = (4 pi/3) rho_L R^3 gives 4 G E/R = 2 : Delta h_max = 2 (nonperturbative; the Hubble sphere sits at its Schwarzschild radius)", dh == 2)
eta = sp.symbols('eta', positive=True)
a_mem = sp.Rational(1, 2) * (eta * dh) * H**2 * R        # (1/2) Delta h omega^2 r at omega = H, r = 1/H
X2_mem = sp.simplify(a_mem**2 / (G * rho_L))
chk("Q2b  a = eta H  and X^2 = eta^2 (8 pi/3)  (predicted)", sp.simplify(a_mem - eta * H) == 0 and sp.simplify(X2_mem - eta**2 * 8 * sp.pi / 3) == 0)
etaneed = sp.solve(sp.Eq(X2_mem, Xtarget2), eta)[0]
# OWN ERROR, caught by this check: my first hand estimate of the needed eta was 3/(16 pi); a = eta*H and a0 = H/Z give eta = 1/Z = sqrt(3/(32 pi)).
chk("Q2c  hitting a0 needs eta = 1/Z = sqrt(3/(32 pi)) = %.4f: eta^2 = 3/(32 pi) is pi^-1, so eta is not algebraic (Lindemann: pi is transcendental)" % float(etaneed),
    sp.simplify(etaneed - sp.sqrt(3 / (32 * sp.pi))) == 0 and sp.simplify(etaneed**2 - 3 / (32 * sp.pi)) == 0)
# eta is a ratio of angular integrals over the SAME sphere: test with random rational trig-polynomial weights
th, ph_ = sp.symbols('theta phi', real=True)
import random
random.seed(7)
xs, ys, zs = sp.sin(th) * sp.cos(ph_), sp.sin(th) * sp.sin(ph_), sp.cos(th)
mons = [xs**2 - ys**2, xs * ys, zs * (xs**2 - ys**2), zs * xs * ys, (xs**2 - ys**2) * zs**2, xs**2 * ys**2, zs, zs**2, xs, xs * zs]
def memfactor(weight):
    """N = z axis.  [n_j n_k]^TT/(1 - n.N): h_+ = (1/2)(n_x^2 - n_y^2)/(1 - z) = (1/2)(1+z) cos2phi, h_x = n_x n_y/(1-z)"""
    hp = sp.Rational(1, 2) * (1 + zs) * sp.cos(2 * ph_)
    hx = sp.Rational(1, 2) * (1 + zs) * sp.sin(2 * ph_)
    def I(e):
        return sp.integrate(sp.integrate(sp.expand(e) * sp.sin(th), (ph_, 0, 2 * sp.pi)), (th, 0, sp.pi))
    norm = I(weight)
    return sp.simplify(I(weight * hp) / norm), sp.simplify(I(weight * hx) / norm)
allrat = True
for trial in range(6):
    wgt = 1 + sum(sp.Rational(random.randint(-3, 3), random.randint(1, 6)) * m for m in random.sample(mons, 4)) * sp.Rational(1, 7)
    mp_, mx_ = memfactor(wgt)
    allrat = allrat and mp_.is_rational and mx_.is_rational
chk("Q2d  memory angular factors of 6 random rational trig-polynomial normalised weights are RATIONAL (pi cancels: same sphere in numerator and normalisation)", allrat)
mw, mx = memfactor(1 + sp.Rational(1, 2) * (xs**2 - ys**2))
mpi, _ = memfactor(1 + sp.pi * (xs**2 - ys**2))
chk("C2b CONTROL (test is sensitive): a weight with a pi inside its coefficient gives a NON-rational memory factor %s" % mpi, not mpi.is_rational)
chk("Q2e  worked example: weight 1 + b (n_x^2 - n_y^2), b = 1/2 -> memory factor h_+ = b/6 = %s (rational; hand value b/6)" % mw, mw == sp.Rational(1, 12))
chk("C2  CONTROL: the needed eta^2 = 3/(32 pi) is not rational, so no rational memory factor (eta^2 rational) reaches it", not (etaneed**2).is_rational)
# the two candidates that the fixed-menu logic would 'try': a rational eta cannot give X^2 = 1/4
chk("Q2f  with rational eta: X^2 = eta^2 (8 pi/3) is a rational multiple of pi, never 1/4 (irrationality of pi)", not (X2_mem.subs(eta, sp.Rational(3, 50))).is_rational)

# ---------------------------------------------------------------- Q3  Bunch-Davies
print("\nQ3  de Sitter tensor modes (Bunch-Davies), canonical normalisation from g01 (h_hat = sqrt(32 pi G) phi per unit-norm polarisation)")
hb = sp.symbols('hbar', positive=True)
Hh = sp.symbols('H', positive=True)
var_per_pol = 32 * sp.pi * G * hb * (Hh / (2 * sp.pi))**2      # <phi^2> = (H/2pi)^2 per e-fold (massless minimally coupled)
PT = sp.simplify(2 * var_per_pol)
Mp2 = 1 / (8 * sp.pi * G)
chk("Q3a  P_T = 16 hbar G H^2/pi = 2 hbar H^2/(pi^2 M_p^2), M_p^2 = 1/(8 pi G)  (the standard tensor power, reproduced from the canonical 32 pi G)", sp.simplify(PT - 2 * hb * Hh**2 / (sp.pi**2 * Mp2)) == 0 and sp.simplify(PT - 16 * hb * G * Hh**2 / sp.pi) == 0)
a_bd = sp.sqrt(PT) * Hh / 2
X2_bd = sp.simplify(a_bd**2 / (G * (3 * Hh**2 / (8 * sp.pi * G)) * 1))
chk("Q3b  X^2 = (32/3) hbar G H^2 (pi^0, predicted) -- carries hbar; a0 does not", sp.simplify(X2_bd - sp.Rational(32, 3) * hb * G * Hh**2) == 0)
hbar_SI, c_SI, G_SI = 1.054571817e-34, 2.99792458e8, 6.6743e-11
Mpc = 3.0857e22
H_L = math.sqrt(OL) * H0 * 1000 / Mpc
tP = math.sqrt(hbar_SI * G_SI / c_SI**5)
X2num = 32 / 3 * (H_L * tP)**2
print("   H_L = %.3e /s, t_Planck = %.3e s, (H t_P)^2 = %.2e, X^2 = %.2e (X = %.1e) vs target 0.25" % (H_L, tP, (H_L * tP)**2, X2num, math.sqrt(X2num)))
chk("Q3c  the Bunch-Davies tensor 'acceleration' is ~1e-60 of a0-scale: 60 orders short (the same Planck suppression the record's graviton-bath lane found)", math.sqrt(X2num) < 1e-55)
Eratio = sp.simplify((PT * Hh**2 / (32 * sp.pi * G)) / (3 * Hh**2 / (8 * sp.pi * G)))     # Isaacson with hdot ~ H h at horizon crossing (order-of-magnitude)
chk("Q3d  tensor energy per e-fold / rho_L = (4/3) hbar G H^2/pi  (~1e-122; Isaacson with hdot ~ H h at crossing)", sp.simplify(Eratio - sp.Rational(4, 3) * hb * G * Hh**2 / sp.pi) == 0)

# ---------------------------------------------------------------- Q5  EOS
print("\nQ5  equation of state of a GW / graviton gas")
dsp = sp.symbols('d', positive=True, integer=True)
# t^{mu nu} = rho k^mu k^nu/omega^2 for a null wave (g01 B3); isotropic average: <n_i n_j> = delta_ij/d
for d in range(2, 7):
    p_over_rho = sp.Rational(1, d)         # sum_i <n_i^2> = 1 with d equal terms
    enth = 1 + p_over_rho
    D = d + 1
    chk("Q5  d = %d spatial dims: p = rho/%d, (rho+p)/rho = %s = D/(D-1) with D = %d" % (d, d, enth, D), enth == sp.Rational(D, D - 1))
n = sp.symbols('n1 n2 n3', real=True)
ang = sp.Rational(1, 4) / sp.pi * sp.integrate(sp.integrate(sp.sin(th)**2 * sp.cos(ph_)**2 * sp.sin(th), (ph_, 0, 2 * sp.pi)), (th, 0, sp.pi))
chk("Q5b  explicit sphere average <n_x^2> = 1/3 (so p = rho/3 in D = 4)", ang == sp.Rational(1, 3))
# what this does and does not give for formulation 6 (M1 = (2/3) t_L / kappa, record's premise M1/t_L = (rho+p)/rho)
kap_prem = sp.Rational(2, 3) / sp.Rational(4, 3)
chk("Q5c  IF M1/t_L = (rho+p)/rho (the record's premise, NOT derived here) then kappa = (2/3)/(4/3) = 1/2 for any null gas: the GW gas supplies the 4/3 exactly, the premise itself is not supplied", kap_prem == sp.Rational(1, 2))
chk("Q5d  the GW gas cannot BE the vacuum: w_GW = 1/3 vs w_L = -1, and rho_GW = rho_L is excluded (Q1g,h); the 4/3 belongs to a different component than the t_L that sets M1", sp.Rational(1, 3) != -1)

# ---------------------------------------------------------------- Q6  graviton-condensate counting (arXiv:1701.08776 abstract: N = horizon area in Planck units, quanta of frequency ~ H)
print("\nQ6  Hubble-frequency graviton quanta filling the Hubble sphere (hbar = 1)")
Nq = sp.symbols('N', positive=True)
V_H = sp.Rational(4, 3) * sp.pi / H**3
rho_cond = Nq * H / V_H
Nneed = sp.solve(sp.Eq(rho_cond, 3 * H**2 / (8 * sp.pi * G)), Nq)[0]
S_dS = sp.pi / (G * H**2)
chk("Q6a  N quanta of energy H in the Hubble sphere equal rho_L iff N = 1/(2 G H^2) = S_dS/(2 pi)  (Bekenstein S = 2 pi E R); N = R^2/l_P^2 gives 2 rho_L", sp.simplify(Nneed - 1 / (2 * G * H**2)) == 0 and sp.simplify(Nneed - S_dS / (2 * sp.pi)) == 0 and sp.simplify(rho_cond.subs(Nq, 1 / (G * H**2)) - 2 * 3 * H**2 / (8 * sp.pi * G)) == 0)
chk("Q6b  the classical amplitude of that condensate is h0 = 2 sqrt(3) (Q1, f = 1, omega = H): a coherent state at h ~ O(1), outside linear/Isaacson control -- consistent with the literature's 'quantum-critical' condensate, and not a derivation of a0", abs(math.sqrt(12) - 2 * math.sqrt(3)) < 1e-15)

print("\n%d/%d checks behaved as declared" % (sum(ok), len(ok)))
sys.exit(0 if all(ok) else 1)
