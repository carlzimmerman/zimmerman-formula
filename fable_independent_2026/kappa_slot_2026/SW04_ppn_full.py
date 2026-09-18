#!/usr/bin/env python3
"""SW04 -- THE FULL PPN OF THE SW03 ACTION, ALL COUPLINGS INCLUDED (the gate SW03 left unverified).

Setting.  In the solar neighbourhood the switch field is the Yukawa average of H(S) over l >> r_M(Sun) = 0.03 pc, so it is set by
the GALACTIC field: psi = H(eta^2), y = eta = g_gal/a0 ~ 2.2-2.5, and the MOND scalar carries a UNIFORM fraction nu(eta) - 1 of the
Newtonian force (19-26%).  It is not switched off.  The reduced theory in the solar system is therefore:
    Einstein-aether (c_1..c_4; its own PPN alpha_1^ae, alpha_2^ae kept SYMBOLIC; gamma = beta = 1)
  + a scalar phi with CONSTANT kinetic coefficient mu_s = 1/(nu(eta) - 1), static solution phi = -U_E/mu_s (times the source's
    aether-velocity factor, derived below)
  + matter on the TeVeS disformal metric  g~ = e^{-2 phi} g - 2 sinh(2 phi) u u.
We compute the physical PPN parameters of g~ for a static source with the aether moving at velocity -w in the PPN frame,
symbolically, to O(epsilon^4) in g~_00 and O(epsilon^3) in g~_0i, with U ~ eps^2 and w ~ eps.  The preferred-frame parameters are
read from g~_00 (the w^2 U and w^i w^j U_ij coefficients, gauge-invariant for a static source) and independently from g~_0i
(the w_i U and w^j U_ij coefficients); the two extractions must agree.  gamma~ is read from g~_ij, the beta-structure from the
U^2 term.  Then the numbers at the solar eta, both kernels, both footings, against |alpha_1| < 1e-4 and |alpha_2| < 4e-7; the
aether cancellation condition and whether it lies inside the aether's stability region; and the l-scan showing that the
quadrupole suppression (l >> r_M) and the preferred-frame activation are the SAME condition.
A FAIL is a finding; no literal-True checks."""
import os, json, math
import sympy as sp
CH, OUT = [], {}
def check(n, ok, d=""):
    CH.append(bool(ok)); print(f"  [{'PASS' if ok else 'FAIL'}] {n}" + (f"\n           ({d})" if d else ""), flush=True)
print("SW04 -- the full PPN of the SW03 action\n")

# ================================================================== 1. the scalar's source with a moving aether
print("=" * 100); print("1. the scalar's matter source with the aether moving: the factor (1 + 2 w^2)"); print("=" * 100)
phi, U, w2, eps = sp.symbols('phi U w2 epsilon', real=True)
# for dust at rest in the PPN frame, g~_00 = e^{-2phi} g_00 - 2 sinh(2phi) u_0^2 with g_00 = -1 + 2U, u_0^2 = 1 - 2U + w^2 (aether at -w)
g00E = -1 + 2 * U
u0sq = 1 - 2 * U + w2
gt00 = sp.exp(-2 * phi) * g00E - 2 * sp.sinh(2 * phi) * u0sq
ut0sq = -1 / gt00                                   # (u~^0)^2 from g~_00 (u~^0)^2 = -1
uut_sq = ut0sq * u0sq                                # (u . u~)^2 = (u_0 u~^0)^2
source = 2 - 4 * sp.exp(2 * phi) * uut_sq             # T~^{mu nu} d g~_{mu nu}/d phi / rho~  (derived in the docstring of SW03/SW04)
# order bookkeeping: phi, U, w2 all O(eps^2)
ser = sp.series(source.subs({phi: eps ** 2 * phi, U: eps ** 2 * U, w2: eps ** 2 * w2}), eps, 0, 4).removeO().subs(eps, 1)
print(f"    source / rho~ = {sp.simplify(ser)}   (to O(eps^2))")
check("1a the scalar's source is -2 rho~ (1 + 2 w^2) + O(eps^4): no phi-linear term (TeVeS's e^{-2phi}-free source), a w^2 factor from the aether's motion",
      sp.simplify(ser + 2 * (1 + 2 * w2)) == 0, f"{sp.simplify(ser)}")

# ================================================================== 2. the physical metric to PPN order
print("\n" + "=" * 100); print("2. g~ to PPN order; PPN parameters from g~_00 and from g~_0i independently"); print("=" * 100)
a1e, a2e, mus = sp.symbols('alpha1_ae alpha2_ae mu_s', real=True)
Q = sp.Symbol('Q')        # formal:  w^i w^j U_ij   (O(eps^4))
P1, P2 = sp.symbols('P1 P2')   # formal: w_i U and w^j U_ij in g_0i (O(eps^3))
# Einstein-frame PPN metric (Einstein-aether: gamma = beta = 1, xi = zeta = alpha3 = 0), static source, aether moving:
g00_E = -1 + 2 * U - 2 * U ** 2 - (a1e - a2e) * w2 * U - a2e * Q
g0i_E = -sp.Rational(1, 2) * (a1e - 2 * a2e) * P1 - a2e * P2
# the scalar: static solution with the source factor of part 1:  phi = -(U/mu_s)(1 + 2 w^2)
phi_sol = -(U / mus) * (1 + 2 * w2)
# aether covariant components (PPN frame): u_0 = -1 + U - w^2/2 ;  u_0 u_i = w_i (so the disformal g~_0i piece is -4 phi w_i -> -4 phi P1/U)
u0 = -1 + U - w2 / 2
gt00 = sp.exp(-2 * phi_sol) * g00_E - 2 * sp.sinh(2 * phi_sol) * u0 ** 2
gt0i = sp.exp(-2 * phi_sol) * g0i_E - 2 * sp.sinh(2 * phi_sol) * (P1 / U)     # u_0 u_i = w_i, and w_i U == P1
gtij = sp.exp(-2 * phi_sol) * (1 + 2 * U)                                    # coefficient of delta_ij
def trunc(expr, order):
    e = expr.subs({U: eps ** 2 * U, w2: eps ** 2 * w2, Q: eps ** 4 * Q, P1: eps ** 3 * P1, P2: eps ** 3 * P2})
    return sp.expand(sp.series(e, eps, 0, order + 1).removeO().subs(eps, 1))
gt00_4 = trunc(gt00, 4); gt0i_3 = trunc(gt0i, 3); gtij_2 = trunc(gtij, 2)
nu = 1 + 1 / mus                       # the physical potential U~ = nu U (G_eff = nu G)
Ut = sp.Symbol('U_t')
# --- gamma~ and the U~ normalisation
cU = gt00_4.coeff(U, 1).subs({w2: 0, Q: 0})
cUij = gtij_2.coeff(U, 1)
check("2a g~_00 = -1 + 2 nu U and g~_ij = (1 + 2 nu U) delta_ij: the physical potential is U~ = nu U with nu = 1 + 1/mu_s, and gamma~ = 1 exactly",
      sp.simplify(cU - 2 * nu) == 0 and sp.simplify(cUij - 2 * nu) == 0, f"coeff(U) in g~_00 = {sp.simplify(cU)}, in g~_ij = {sp.simplify(cUij)}")
cU2 = gt00_4.coeff(U, 2).subs({w2: 0, Q: 0})
check("2b the U^2 term is -2 (nu U)^2 = -2 U~^2: beta~ = 1 at the level of the metric map (the nonlinear source correction is the TeVeS one, beta = 1)",
      sp.simplify(cU2 + 2 * nu ** 2) == 0, f"coeff(U^2) = {sp.simplify(cU2)}")
# --- preferred-frame parameters from g~_00 (static source: gauge-invariant)
c_w2U = sp.simplify(gt00_4.coeff(w2, 1).coeff(U, 1))           # coefficient of w^2 U  = -(alpha1~ - alpha2~) nu   (in terms of U = U~/nu)
c_Q = sp.simplify(gt00_4.coeff(Q, 1))                            # coefficient of w^i w^j U_ij = -alpha2~ nu
a2_from00 = sp.simplify(-c_Q / nu)
a1_from00 = sp.simplify(a2_from00 - c_w2U / nu)
print(f"    from g~_00:  alpha1~ = {a1_from00},   alpha2~ = {a2_from00}")
# --- preferred-frame parameters from g~_0i
c_P1 = sp.simplify(gt0i_3.coeff(P1, 1)); c_P2 = sp.simplify(gt0i_3.coeff(P2, 1))
a2_from0i = sp.simplify(-c_P2 / nu)
a1_from0i = sp.simplify(2 * a2_from0i - 2 * c_P1 / nu)
print(f"    from g~_0i:  alpha1~ = {a1_from0i},   alpha2~ = {a2_from0i}")
check("2c the two independent extractions agree: alpha1~ = [alpha1_ae - 8 (nu - 1)]/nu,  alpha2~ = alpha2_ae/nu",
      sp.simplify(a1_from00 - a1_from0i) == 0 and sp.simplify(a2_from00 - a2_from0i) == 0
      and sp.simplify(a1_from00 - (a1e - 8 * (nu - 1)) / nu) == 0 and sp.simplify(a2_from00 - a2e / nu) == 0)
# --- the rest-frame cross-check: the gauge-invariant V_i + W_i coefficient sum in the aether frame is -(8 + alpha1_ae)/(2 nu) = -(4 + alpha1~/2)
a1_rest = sp.simplify((8 + a1e) / nu - 8)
check("2d rest-frame route (V_i + W_i sum invariant): alpha1~ = (8 + alpha1_ae)/nu - 8, identical to the moving-frame value",
      sp.simplify(a1_rest - a1_from00) == 0)
check("2e the Brans-Dicke control: with a CONFORMAL coupling only, gamma_BD = (2 - nu)/nu compensates the 1/nu gravitomagnetic deficit and alpha1 = 0",
      sp.simplify(-(2 * ((2 - nu) / nu) + 2) - (-4 / nu)) == 0, "-(2 gamma + 2) = -4/nu: the disformal term forces gamma~ = 1 and moves the deficit into alpha1~")
OUT["formulas"] = dict(alpha1=str(a1_from00), alpha2=str(a2_from00))

# ================================================================== 3. numbers at the solar eta
print("\n" + "=" * 100); print("3. the numbers: the smoothed switch at the Sun, nu(eta), alpha1~, alpha2~ vs the bounds; the cancellation condition"); print("=" * 100)
from scipy.optimize import brentq
KMS, KPC = 1e3, 3.0857e19
g_gal = (230 * KMS) ** 2 / (8.2 * KPC)
nu_rar = lambda y: 1.0 / (1.0 - math.exp(-math.sqrt(y)))
mu2 = lambda u: 1.0 - (1.0 + u) ** -2
def nu_mu2(y): return brentq(lambda g: g * mu2(g / 2.0) - y, y, 50 * y + 50) / y
KERN = {"nu_RAR": nu_rar, "mu_2": nu_mu2}
BOUND_A1, BOUND_A2 = 1e-4, 4e-7
for foot, a0 in (("canonical", 9.3619e-11), ("alt", 1.1279e-10)):
    eta = g_gal / a0
    psi = eta ** 2 / (1 + eta ** 2)                    # the smoothed switch at the Sun for l >> r_M(Sun): H(eta^2)
    y = math.sqrt(psi / (1 - psi))
    for kn, nuf in KERN.items():
        nv = nuf(y); a1 = -8 * (nv - 1) / nv; a2 = 0.0
        c14_needed = -2 * (nv - 1)                     # alpha1_ae = -4 c14 (c13 = 0) must equal 8 (nu - 1)
        etaN = -a1                                     # Nordtvedt eta_N = 4 beta - gamma - 3 - alpha1 + (2/3) alpha2 with beta = gamma = 1
        print(f"    {foot:9s} {kn:6s}: eta = {eta:.2f}, psi = {psi:.3f}, y = {y:.2f}, nu = {nv:.3f} (scalar {100*(nv-1):.0f}% on) -> alpha1~ = {a1:+.3f} ({abs(a1)/BOUND_A1:.0e} x bound), "
              f"alpha2~ = {a2:+.1e} (with alpha2_ae = 0); Nordtvedt eta_N = {etaN:+.2f} (bound 4e-4); cancellation needs alpha1_ae = {8*(nv-1):.2f} -> c14 = {c14_needed:+.2f}")
        OUT.setdefault("numbers", {})[f"{foot}/{kn}"] = dict(eta=eta, nu=nv, alpha1=a1, alpha2=a2, over_bound=abs(a1) / BOUND_A1, c14_needed=c14_needed)
check("3a |alpha1~| < 1e-4 (LLR / pulsar bound) with the aether on its alpha1_ae = alpha2_ae = 0 subspace, on any footing and kernel",
      any(v["over_bound"] < 1 for v in OUT["numbers"].values()), f"min |alpha1~| = {min(abs(v['alpha1']) for v in OUT['numbers'].values()):.2f}: violated by 4 orders. [FAIL is the finding]")
check("3b the aether cancellation alpha1_ae = 8 (nu - 1) lies inside the aether's stability region 0 < c14 < 2 for some footing/kernel",
      any(0 < v["c14_needed"] < 2 for v in OUT["numbers"].values()), f"c14 needed = {[round(v['c14_needed'], 2) for v in OUT['numbers'].values()]}: negative on every footing (alpha1_ae = -4 c14 > 0 needs c14 < 0), and tuned to the Sun's eta. [FAIL is the finding]")

# ================================================================== 4. the l-scan: the quadrupole suppression and the preferred-frame activation are one condition
print("\n" + "=" * 100); print("4. the l-scan: anisotropy suppression at r_M (kills the quadrupole) versus the switch value at Saturn (sets alpha1~)"); print("=" * 100)
from scipy.integrate import quad
G, MSUN, PC, AU = 6.674e-11, 1.989e30, 3.0857e16, 1.496e11
a0 = 9.3619e-11; eta = g_gal / a0
rM = math.sqrt(G * MSUN / a0); r_sat = 9.5 * AU
gs = lambda r: G * MSUN / r ** 2
# monopole (angle-averaged) switch source: <|g_sun + g_gal|^2> = g_sun^2 + g_gal^2
Hs = lambda r: ((gs(r) ** 2 + g_gal ** 2) / a0 ** 2) / (1 + (gs(r) ** 2 + g_gal ** 2) / a0 ** 2)
def psi_mono(r, ell):
    f = lambda lr: (lambda rp: Hs(rp) * (math.exp(-abs(r - rp) / ell) - math.exp(-(r + rp) / ell)) / (2 * ell * r * rp) * rp ** 3)(math.exp(lr))
    rmin, rmax = 1e-3 * r_sat, 1e5 * rM
    pts = sorted(set(math.log(x) for x in (r, r + ell, max(r - ell, rmin * 1.01), r + 5 * ell, max(r - 5 * ell, rmin * 1.01), rM) if rmin < x < rmax))
    return quad(f, math.log(rmin), math.log(rmax), points=pts, limit=1500)[0]
# the l = 1 part of the LOCAL switch: H(S) with S = (x^2 + eta^2 + 2 x eta cos theta), x = g_sun/a0 -> amplitude dH/dS * 2 x eta at each r
def H1_local(r):
    x = gs(r) / a0; S0 = x ** 2 + eta ** 2
    return (1.0 / (1.0 + S0) ** 2) * 2 * x * eta            # coefficient of cos(theta) in H, first order in the cross term
# Yukawa smoothing of an l = 1 pattern f(r') cos(theta'): the exact multipole expansion of the Green's function of (1 - l^2 lap),
#   e^{-R/l}/(4 pi l^2 R) = (1/(2 pi^2 l^3)) sum_l (2l+1) i_l(r_</l) k_l(r_>/l) P_l(cos gamma),  so the l = 1 transfer is
#   psi_1(r) = (2/(pi l^3)) int r'^2 f(r') i_1(min/l) k_1(max/l) dr'   with i_1(x) = (x cosh x - sinh x)/x^2, k_1(x) = (pi/2)(1 + 1/x) e^{-x}/x.
def i1k1(a, b):                                   # i_1(a) k_1(b) for a <= b, exponentially scaled (no overflow)
    return (math.pi / 4.0) * ((a - 1.0) + (a + 1.0) * math.exp(-2.0 * a)) * (1.0 + 1.0 / b) * math.exp(a - b) / (a * a * b)
def psi_dipole(r, ell):
    def f(lr):
        rp = math.exp(lr); a, b = min(r, rp) / ell, max(r, rp) / ell
        return H1_local(rp) * i1k1(a, b) * rp ** 3
    rmin, rmax = 1e-3 * r_sat, 1e4 * rM
    pts = sorted(set(math.log(x) for x in (r, r + ell, max(r - ell, rmin * 1.01), r + 5 * ell, max(r - 5 * ell, rmin * 1.01), rM) if rmin < x < rmax))
    return (2.0 / (math.pi * ell ** 3)) * quad(f, math.log(rmin), math.log(rmax), points=pts, limit=1500)[0]
H1_rM = H1_local(rM)
print(f"    the local switch's l = 1 anisotropy at r_M: amplitude {H1_rM:.4f} on H = {Hs(rM):.4f} ({100*H1_rM/Hs(rM):.1f}% -- the AQUAL quadrupole's source, 6.44x Cassini for mu_2)")
print(f"    {'l [pc]':>9s} {'psi(Saturn)':>12s} {'nu-1 (Saturn)':>14s} {'alpha1~':>9s} {'T1(r_M)':>9s}   reading")
rows = {}
for ell_pc in (1e-4, 3e-4, 1e-3, 3e-3, 1e-2, 3e-2, 0.1, 0.3, 1.0, 10.0):
    ell = ell_pc * PC
    ps = psi_mono(r_sat, ell); ps = min(max(ps, 1e-12), 1 - 1e-15)
    yv = math.sqrt(ps / (1 - ps)); nv = nu_rar(yv); a1 = -8 * (nv - 1) / nv
    T1 = psi_dipole(rM, ell) / H1_rM                            # fraction of the local l = 1 anisotropy surviving the smoothing at r_M
    rows[ell_pc] = dict(psi_sat=ps, nu=nv, alpha1=a1, T1=T1)
    ok_ppn = abs(a1) < BOUND_A1; ok_q = T1 < 1 / 6.44
    print(f"    {ell_pc:9.4f} {ps:12.6f} {nv-1:14.2e} {a1:+9.2e} {T1:9.4f}   PPN {'ok' if ok_ppn else 'FAIL'} / quadrupole {'ok' if ok_q else 'FAIL'}")
OUT["lscan"] = rows
check("4a for l << r_M(Sun) the switch at Saturn is the Sun's own field (psi -> 1, scalar off, |alpha1~| < 1e-4) -- the AQUAL/QUMOND regime whose quadrupole is 6.44x Cassini (T1 ~ 1)",
      abs(rows[1e-4]["alpha1"]) < BOUND_A1 and rows[1e-4]["T1"] > 0.9)
check("4b for l >> r_M(Sun) the switch at Saturn is the Galactic field (psi -> H(eta^2)): the anisotropy at r_M is suppressed (T1 << 1/6.44) and alpha1~ = -8(nu-1)/nu",
      rows[10.0]["T1"] < 1 / 6.44 and abs(rows[10.0]["alpha1"] + 8 * (nu_rar(eta) - 1) / nu_rar(eta)) < 0.02)
check("4c there is a smoothing length l where BOTH |alpha1~| < 1e-4 AND the anisotropy at r_M is suppressed below 1/6.44 (T1 < 0.155)",
      any(abs(v["alpha1"]) < BOUND_A1 and v["T1"] < 1 / 6.44 for v in rows.values()),
      "none: the largest l passing PPN and the smallest l passing the quadrupole are separated by ~2 orders of magnitude. One condition, two kills. [FAIL is the finding]")
l_ppn = max([e for e, v in rows.items() if abs(v["alpha1"]) < BOUND_A1], default=float('nan'))
l_q = min([e for e, v in rows.items() if v["T1"] < 1 / 6.44], default=float('nan'))
print(f"    largest l passing |alpha1| < 1e-4: {l_ppn} pc;  smallest l passing the quadrupole (T1 < 0.155): {l_q} pc;  r_M(Sun) = {rM/PC:.4f} pc")
OUT["windows"] = dict(l_ppn_max_pc=l_ppn, l_quadrupole_min_pc=l_q, rM_pc=rM / PC)

n, n_pass = len(CH), sum(CH)
print(f"\nSW04 COMPLETE: {n_pass}/{n} checks PASS.  VERDICT: the SW03 action FAILS the preferred-frame PPN bounds.  gamma~ = 1 and beta~ = 1 hold, but")
print("alpha1~ = [alpha1_ae - 8(nu(eta_gal) - 1)]/nu(eta_gal) = -1.3 to -1.7 with a healthy aether, four orders above |alpha1| < 1e-4 (and the Nordtvedt")
print("eta_N = -alpha1~ four orders above 4e-4).  THEOREM: a scalar that renormalises the Newtonian and light-bending potentials equally (gamma = 1,")
print("forced by Cassini and by lensing) but contributes nothing to gravitomagnetism produces alpha1 = -8(nu - 1)/nu; an isotropic external-field")
print("effect makes nu(eta_gal) - 1 = 0.19-0.26 uniform across the solar system; hence the isotropic-EFE + preferred-frame-lensing class is dead")
print("on alpha1 exactly where the local-switch class is dead on the quadrupole.  Cancellation needs c14 < 0 (unstable aether) tuned to the Sun's eta.")
json.dump(dict(pass_=n_pass, n=n, parts=OUT), open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "SW04_results.json"), "w"), indent=1, default=str)
