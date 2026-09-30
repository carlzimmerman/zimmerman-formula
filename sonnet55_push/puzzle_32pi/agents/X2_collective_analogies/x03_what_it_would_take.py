#!/usr/bin/env python3
"""x03_what_it_would_take.py -- computed AFTER the target is known (the task asks for it): what a linear response of the medium would have to be to give a MOND-like
1/r force, and what the plasma-analogy nonlinear scale is.  Every input below is labelled INPUT; nothing here is a result about the puzzle.
c = 1.  Reference R* = 1/sqrt(G rho_Lambda), a0 = 1/(2R*) (target), r_M(M) = sqrt(G M/a0), deep-MOND force g = sqrt(G M a0)/r.

 G1  anti-screening (Jeans) medium: far-field force envelope G M k / r.  Matching to deep MOND at a single mass M_xi (r_M = xi R*) needs
     k = 1/(xi R*), i.e. (rho+p)/(c_s^2 rho_Lambda) = 1/(4 pi xi^2)  (= 1/pi at xi = 1/2): an INPUT containing pi, and w != -1.
     The mass with r_M = xi R* has r_s = xi^2 R*  (r_M/r_s = 1/xi): at xi = 1/2 the 'deep-MOND radius' is 2 r_s (relativistic, the Newtonian derivation is out of range).
 G2  Yukawa force has no 1/r term (series): (1+mr)e^{-mr} = 1 - (mr)^2/2 + ...
 G3  a long-range susceptibility eps^{-1}(k) = 1 + 1/(k ell) gives g = G M/r^2 + (2/pi) G M/(ell r); matching MOND at one mass needs ell = (2/pi) r_M (ell proportional to sqrt(M): no fixed ell works)
 G4  cold-plasma wave breaking: E_wb = m v_ph omega_p/e (Lagrangian: density n0/(1+dxi/dx0) diverges at k A = 1); acceleration a_wb = omega_p v_ph; with v_ph = c and the
     gravity dictionary omega_p^2 -> 4 pi G rho:  c omega_J = 4 sqrt(pi) a0 = 7.09 a0
 G5  target-known coincidence check: dust exponent s = a0 needs rho_c/rho_Lambda = (2Z+1)/(16 pi) = 0.2502 (close to 1/4); its false-positive rate is computed.
 G6  scales relative to a0 (definitions only; the menu table is x04)
Exit 0 = all pass.
"""
import mpmath as mp
import sympy as sp
from common import Ledger

L = Ledger("x03")
ck, must = L.check, L.must_fail

print("G1  anti-screening medium: what the far-field envelope needs (INPUT: matching at one mass)")
Grho, xi, Gk, cs2, rp, r = sp.symbols("Grho xi Gk cs2 rho_plus_p_over_rhoL r", positive=True)   # Grho = G rho_Lambda ; rp = (rho+p)/(rho_Lambda c_s^2)
Rstar = 1 / sp.sqrt(Grho)
a0 = sp.sqrt(Grho) / 2
GM = sp.symbols("GM", positive=True)
rM = sp.sqrt(GM / a0)
GM_xi = sp.solve(sp.Eq(rM, xi * Rstar), GM)[0]
ck("G1a  the mass with r_M = xi R* has G M = xi^2 R*/2 and Schwarzschild radius r_s = 2 G M = xi^2 R*  (r_M/r_s = 1/xi)",
   sp.simplify(GM_xi - xi**2 * Rstar / 2) == 0 and sp.simplify(2 * GM_xi - xi**2 * Rstar) == 0)
k_need = sp.solve(sp.Eq(GM_xi * sp.Symbol("k", positive=True), sp.sqrt(GM_xi * a0)), sp.Symbol("k", positive=True))[0]   # G M k = sqrt(G M a0)
ck("G1b  envelope amplitude G M k = sqrt(G M a0) needs k = 1/r_M = 1/(xi R*)", sp.simplify(k_need - 1 / (xi * Rstar)) == 0)
susc = sp.simplify(k_need**2 / (4 * sp.pi * Grho))                       # k^2 = 4 pi G (rho+p)/c_s^2 = 4 pi G rho_L * rp
ck("G1c  required (rho+p)/(c_s^2 rho_Lambda) = 1/(4 pi xi^2);  = 1/pi at xi = 1/2, 1/(4 pi) at xi = 1",
   sp.simplify(susc - 1 / (4 * sp.pi * xi**2)) == 0 and sp.simplify(susc.subs(xi, sp.Rational(1, 2)) - 1 / sp.pi) == 0)
must("G1d-mut  the required susceptibility at xi = 1/2 is 1/(2 pi)", sp.simplify(susc.subs(xi, sp.Rational(1, 2)) - 1 / (2 * sp.pi)) == 0)
w_needed = sp.symbols("w_needed")
sol_w = sp.solve(sp.Eq((1 + w_needed) / 1, 1 / sp.pi), w_needed)[0]      # c_s^2 = 1 (canonical scalar-like) for illustration only
print(f"   illustration (INPUT, one mass only): c_s^2 = 1 needs 1 + w = 1/pi -> w = {float(sol_w):.4f}; the same medium fails for every other mass (E6).")
print("   note: r_M = R*/2 = 2 r_s for that mass: the deep-MOND region begins at twice the Schwarzschild radius, outside the weak-field (Newtonian) hydrostatic derivation.")

print("\nG2  Yukawa force: no 1/r piece")
rr, mm = sp.symbols("rr mm", positive=True)
gy = (1 + mm * rr) * sp.exp(-mm * rr)
ser = sp.series(gy, rr, 0, 4).removeO()
ck("G2a  (1+mr)e^{-mr} = 1 - (mr)^2/2 + (mr)^3/3 + ...: the force GM/r^2 (1 + O(m^2 r^2)) has no G M m/r term",
   sp.simplify(ser - (1 - (mm * rr)**2 / 2 + (mm * rr)**3 / 3)) == 0)
kk = sp.symbols("kk", positive=True)
go = sp.cos(kk * rr) + kk * rr * sp.sin(kk * rr)                         # r^2 g/(GM) for the anti-screened potential
sero = sp.series(go, rr, 0, 4).removeO()
ck("G2b  anti-screened: r^2 g/(GM) = 1 + (kr)^2/2 + ...  near the mass: no 1/r term at small kr; the 1/r envelope appears only for kr >> 1",
   sp.simplify(sero - (1 + (kk * rr)**2 / 2)) == 0)

print("\nG3  a long-range susceptibility eps^{-1}(k) = 1 + 1/(k ell)")
kx, e_ = sp.symbols("kx e_", positive=True)
I1 = sp.integrate(sp.sin(kx * r) * sp.exp(-e_ * kx), (kx, 0, sp.oo))
Isin = sp.limit(I1, e_, 0)
ck("G3a  Abel-regularised int_0^inf sin(kr) dk = 1/r", sp.simplify(Isin - 1 / r) == 0)
# normalisation control: FT of 4 pi/k^2 is 1/r : (4 pi/(2 pi^2 r)) int_0^inf sin(kr)/k dk = 1/r
I2 = sp.integrate(sp.sin(kx * r) / kx, (kx, 0, sp.oo))
ck("G3b  normalisation: int d^3k/(2pi)^3 e^{ikr} 4 pi/k^2 = (2/(pi r)) int sin(kr)/k dk = 1/r", sp.simplify(2 / (sp.pi * r) * I2 - 1 / r) == 0)
ell, Mm, Gs = sp.symbols("ell M G", positive=True)
rho_eff = (Mm / ell) * (1 / (2 * sp.pi**2)) * sp.Abs(Isin) / r                    # int d^3k/(2pi)^3 e^{ikr}/k = (1/(2 pi^2 r)) int sin(kr) dk = 1/(2 pi^2 r^2)
ck("G3c  rho_eff(r) = M/(2 pi^2 ell r^2)", sp.simplify(rho_eff - Mm / (2 * sp.pi**2 * ell * r**2)) == 0)
Meff = sp.integrate(4 * sp.pi * r**2 * Mm / (2 * sp.pi**2 * ell * r**2), r)       # from 0 to r
g_eff = sp.simplify(Gs * Meff / r**2)
ck("G3d  g_eff = (2/pi) G M/(ell r)   (the 2/pi is a 3-D Fourier-transform factor)", sp.simplify(g_eff - 2 * Gs * Mm / (sp.pi * ell * r)) == 0)
must("G3d-mut  g_eff = G M/(pi ell r)", sp.simplify(g_eff - Gs * Mm / (sp.pi * ell * r)) == 0)
ell_need = sp.solve(sp.Eq(2 * Gs * Mm / (sp.pi * ell), sp.sqrt(Gs * Mm * sp.Symbol("a0s", positive=True))), ell)[0]
ck("G3e  matching deep MOND at one mass: ell = (2/pi) sqrt(G M/a0) = (2/pi) r_M : ell scales as sqrt(M); no fixed ell reproduces the M-scaling",
   sp.simplify(ell_need - 2 / sp.pi * sp.sqrt(Gs * Mm / sp.Symbol("a0s", positive=True))) == 0)

print("\nG4  cold-plasma wave breaking (Lagrangian) and the gravity dictionary")
x0, tt, A, kw, wp, v = sp.symbols("x0 t A k omega_p v", positive=True)
xi_disp = A * sp.cos(kw * x0 - wp * tt)                                       # Lagrangian displacement of a Langmuir wave: omega = omega_p (cold)
n_ratio = 1 / (1 + sp.diff(xi_disp, x0))                                     # n/n0 = 1/(1 + d xi/d x0)
jac = 1 + sp.diff(xi_disp, x0)                                                # dx/dx0 = 1/(n/n0); zero <=> density diverges
jac_min = sp.simplify(jac.subs(x0, (sp.pi / 2 + wp * tt) / kw))               # phase pi/2: sin = 1, the most compressive point
ck("G4a  n/n0 = 1/(1 + d xi/dx0): the Jacobian at the most compressive phase is 1 - kA, which vanishes exactly at kA = 1 (trajectory crossing)",
   sp.simplify(jac_min - (1 - kw * A)) == 0 and sp.simplify(jac_min.subs(A, 1 / kw)) == 0)
must("G4a-mut  the Jacobian vanishes at kA = 2", sp.simplify(jac_min.subs(A, 2 / kw)) == 0)
a_wave = sp.simplify(sp.diff(xi_disp, tt, 2))                                # acceleration of the fluid element = -omega_p^2 xi (restoring force) => amplitude omega_p^2 A
ck("G4b  acceleration amplitude omega_p^2 A; at k A = 1: omega_p^2/k = omega_p v_ph  (v_ph = omega_p/k)", sp.simplify(sp.Abs(a_wave.subs(sp.cos(kw * x0 - wp * tt), 1)) / (wp**2 * A) - 1) == 0)
a_wb_c = wp * 1                                                              # v_ph = c = 1
Grho_s = sp.symbols("Grho_s", positive=True)
omegaJ = sp.sqrt(4 * sp.pi * Grho_s)
ratio_wb = sp.simplify(omegaJ / (sp.sqrt(Grho_s) / 2))
ck("G4c  gravity dictionary omega_p^2 -> 4 pi G rho with v_ph = c: a_wb = c omega_J = 4 sqrt(pi) a0 = 7.09 a0", sp.simplify(ratio_wb - 4 * sp.sqrt(sp.pi)) == 0)
print("   caveat: the dictionary flips the sign (like charges attract): the cold plasma oscillation becomes Jeans collapse e^{+-omega_J t}; the crossing condition maps to Zel'dovich shell crossing.")
print("           v_ph = c is an INPUT of the analogy (the only speed of a Lorentz-invariant vacuum), not derived.")

print("\nG5  target-known coincidence check: dust exponent s = a0 in dS")
mp.mp.dps = 30
Z = mp.sqrt(32 * mp.pi / 3)
X_need = (2 * Z + 1) / (16 * mp.pi)
print(f"   X = rho_c/rho_Lambda needed for s+ = a0:  (2Z+1)/(16 pi) = {mp.nstr(X_need, 8)}")
ck("G5a  the closed form equals (2/3)[(1+1/Z)^2 - 1] (numerically to 1e-25)", abs(X_need - mp.mpf(2) / 3 * ((1 + 1 / Z) ** 2 - 1)) < mp.mpf("1e-25"))
# nearest simple fraction (denominator <= 8)
fr = sorted({sp.Rational(p, q) for q in range(1, 9) for p in range(1, q)})
fr_f = [mp.mpf(f.p) / f.q for f in fr]
def rel_dev(x):
    return min(abs(x / f - 1) for f in fr_f)
dev1 = rel_dev(X_need)
print(f"   nearest fraction with denominator <= 8: 1/4, relative deviation {mp.nstr(dev1, 3)}")
ts = [mp.mpf(i) / 400 * (3 - mp.mpf("0.3")) + mp.mpf("0.3") for i in range(401)]      # target exponents t*a0, t in [0.3, 3]
devs = [rel_dev((mp.mpf(2) / 3) * ((1 + t / Z) ** 2 - 1)) for t in ts]
frac_better = sum(1 for d_ in devs if d_ <= dev1) / len(devs)
print(f"   fraction of target multipliers t in [0.3, 3] whose X_t is at least this close to a simple fraction: {float(frac_better):.3f}")
print(f"   (first version of this script asserted 'fraction >= 0.03'; that threshold was arbitrary, the measured fraction is {float(frac_better):.3f}; restated as a measurement)")
ck("G5b  measured single-criterion look-elsewhere fraction is between 0.5% and 10% (about a 2% event, not a rare one; it is a target-known inversion, so it counts as a coincidence, not a hint)",
   0.005 <= frac_better <= 0.10)
print("   physical objection as well: rho_c dilutes as a^-3 in dS, so 's at fixed X' is not a constant of motion; today rho_m/rho_Lambda = 0.46 (not 1/4).")

print("\nG6  scales relative to a0 (definitions only)")
tab = {"c omega_J (wave-breaking dictionary)": 4 * mp.sqrt(mp.pi), "c^2/lambda_J (Jeans, c_s = c)": 2 / mp.sqrt(mp.pi), "c H_Lambda": Z}
for kx_, vx in tab.items():
    print(f"   {kx_:40s} {mp.nstr(vx, 6)} a0")
ck("G6a  c H_Lambda / a0 = Z = sqrt(32 pi/3)", abs(tab["c H_Lambda"] - Z) < mp.mpf("1e-25"))
print("\nSUMMARY (x03): linear response needs (rho+p)/(c_s^2 rho_Lambda) = 1/(4 pi xi^2) and works for ONE mass only; the vacuum's exact value is 0; a0 is a nonlinearity scale;")
print("the plasma nonlinear scale is c omega_J = 4 sqrt(pi) a0, the Jeans acceleration c^2/lambda_J = (2/sqrt(pi)) a0.")
L.finish()
