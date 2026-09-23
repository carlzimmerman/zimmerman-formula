#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
L333 -- THE c_2 CHANNEL, COMPUTED: the khronon's K^2 term DOES carry a moving galaxy's phantom -- and the price is paid by
the aether's own acceleration, which is exactly the field the MOND sector reads.

THE QUESTION (named open by L330 M5 and by real_research/reviews/THE_THEORY_AS_IT_STANDS_2026-09-22.md sec. 4)
  L330 showed that a MOND sector with no shift dependence cannot carry its phantom's momentum: with GR's kinetic term the
  divergence of the momentum constraint gives d_t[R3 - 16 pi G rho_m] = 0, so the phantom is initial data.  The one momentum
  channel on the record is the khronon's c_2 (div n)^2 term (khronometric lambda = c_2, ~1e-5 .. 2.5e-5 at the record's PPN
  corner, THE_ACTION_2026-09-05 sec. 5.11 and the alpha_2 analysis there).  "The first computation is whether it can carry a
  galaxy's phantom at 100-300 km/s inside the alpha_1 and alpha_2 bounds."  This lane does it.

METHOD (every step a check that can fail)
  A1 THE ACTION.  The khronometric action with beta = c_13 = 0 in the unitary gauge (Yagi, Blas, Barausse & Yunes 2014,
     PRD 89 084067, eqs. 15, 17: lambda = c_2, alpha = c_14):
         S = (1/16 pi G_ae) Int N sqrt(gamma) [ K_ij K^ij - (1 + c_2) K^2 + R3 + c_14 a_i a^i ] + S_m ,  a_i = d_i ln N
     with N = e^n, gamma_ij = e^{-2 psi} delta_ij, N_i = d_i B (+ a transverse S_i).  The quadratic Lagrangian and its
     Euler-Lagrange equations are derived SYMBOLICALLY here (Christoffels -> K_ij, R3 from the Ricci tensor, second
     derivative in a bookkeeping parameter); nothing is typed in by hand.  Matter enters through (1/2) T^{mu nu} h_{mu nu}.
     The phantom enters as L330 M1 established for a shift-independent MOND sector: a lapse source rho_ph with NO momentum.
  A2 THE MOVING SOURCE.  A source moving at v through the khronon frame is a steady solution f(x - v t); the linear system
     is solved exactly in Fourier space and transformed to the source's rest frame (Lorentz boost, Jacobian, contraction).
  CONTROLS.  C1 GR (c_2, c_14 -> 0): the rest-frame h'_00 of a moving mass equals the static one to O(v^2) -- Lorentz
     invariance of the whole pipeline.  C2 LITERATURE: the same pipeline must return alpha_1 = -4 c_14 and
     alpha_2 = c_14 (c_14 - c_2 + 2 c_14 c_2) / (c_2 (2 - c_14))  (Yagi+14 eqs. 48-49 at beta = 0), EXACTLY.  C3 L330:
     at c_2 = 0 the momentless source cannot move without a lapse n = 8 pi G gamma M_ph/(c14 k^2) (no solution at c_14 = 0).  C4 the
     O(v^2) series against the exact finite-v solution.
RESULTS.  R1 THE CHANNEL CARRIES THE PHANTOM: for any c_2 > 0 the co-moving solution exists; the potential matter feels
     and the lensing potential both carry the full phantom (O(1) coefficient exactly 1), with a preferred-frame anisotropy
     alpha_2^eff = (2 c14 c2 + c14 - c2)(c14 f - c14 - 2f) / (c2 (c14 - 2)) -- the enhanced part is proportional to c_14,
     so |alpha_2^eff| v^2 ~ 1e-6: invisible.  At f = 0 it is the literature alpha_2: the Solar System is untouched.
  R2 THE PRICE: the khronon's ACCELERATION a_i = d_i n (the MOND sector's input -- the clock's J^mu in the 09-05 action,
     a_mu in C-H) is distorted by
         delta n = C_ph v^2 (v.grad)^2 lap^{-1} Phi_ph ,   C_ph = (4 + 4 c2 + c14 c2) / (c2 (2 - c14)) ~ 2 / c_2 ,
     while baryons' own distortion is suppressed by c_14/c_2.  This is not a gauge artefact: a_i is the covariant
     acceleration of the aether congruence, and it differs from the gravitational field matter feels by -grad(dB/dt), the
     aether's own acceleration as the moving phantom drags it.  Define D = 2 v^2 / (c^2 c_2).
  R3 A REAL GALAXY (nu_RAR phantom of a Hernquist baryonic sphere, both footings): the radial input distortion
     delta a_r / g_obs and the tilt delta a_theta / g_obs, versus radius and angle to v.  Deep-MOND closed form: the radial
     phantom input is enhanced ISOTROPICALLY by D/3 and tilted by (D/3) sin 2 theta (verified numerically).
  R4 THE BRANCHES: at the record's alpha_2-allowed corner (c_14 = 1e-5, c_2 ~ c_2* = 1.0e-5) and the Local Group's 620 km/s
     through the CMB frame, D/3 = 0.29 (0.11 at the closure-locus c_2 = 2.5e-5, which alpha_2 excludes at that c_14): an
     O(10-30%) CMB-velocity-dependent distortion of what the MOND sector sees.  Either
     a0 tracks each galaxy's speed through the CMB frame (a new, falsifiable prediction), or c_2 >> 1e-4, which the PPN
     alpha_2 bound then allows only for c_14 <~ 8e-7.
SCOPE AND CAVEATS.  Linear in the metric (|Phi| ~ 1e-6; delta n ~ D Phi_ph stays linear even for D ~ 1); leading order in
  v^2 beyond the enhanced terms; the phantom is a fixed co-moving lapse source -- the MOND sector's feedback on the distorted
  input changes the O(1) factor, not the scaling D; v is the velocity relative to the LOCAL khronon frame, taken to be the
  CMB frame (it would differ where larger-scale momentless phantoms drag the aether: the drag fraction is ~ (2/c_2) Phi_ph).
MUTATE=1 gives the phantom the baryons' momentum (a shift-coupled MOND sector): the 1/c_2 term of C_ph must then vanish as
c_14 -> 0 and R2 FAILS (rc = 1).

Run from the repository root:  python3 real_research/g03_audit_2026/L333_c2_channel_carries_the_phantom.py
"""
import os, sys, json, math, time
import numpy as np
import sympy as sp
from sympy.calculus.euler import euler_equations

HERE = os.path.dirname(os.path.abspath(__file__))
MUTATE = os.environ.get("MUTATE", "0") == "1"
LANE, SLUG = "L333", "L333_c2_channel_carries_the_phantom"
P_ = lambda *a: print(*a, flush=True)
CH, OUT = [], {"lane": LANE, "mutate": MUTATE, "checks": {}, "numbers": {}}


def check(name, measured, ok, reading="", load_bearing=True):
    ok = bool(ok)
    CH.append((name, ok, load_bearing))
    OUT["checks"][name] = {"ok": ok, "measured": str(measured), "load_bearing": load_bearing}
    P_(f"  [{'PASS' if ok else 'FAIL'}] {name}")
    P_(f"         measured: {measured}")
    if reading:
        P_(f"         reading:  {reading}")
    return ok


def banner(t):
    P_("\n" + "=" * 110); P_(t); P_("=" * 110)


P_(__doc__)
T0 = time.time()
if MUTATE:
    P_("  MUTATE: the phantom is given the baryons' momentum (a shift-coupled MOND sector)")

# ================================================================================================ A1 the action
banner("A1  THE QUADRATIC ACTION, DERIVED SYMBOLICALLY (khronometric, beta = 0, unitary gauge)")
t, x, y, z = sp.symbols('t x y z', real=True)
X = (x, y, z)
eb, al, ep = sp.symbols('e_b alpha epsilon')
nf, pf, Bf, Sf = [sp.Function(s)(t, x, y, z) for s in ('n', 'psi', 'B', 'S')]
N = sp.exp(eb * nf)
gam = sp.diag(*[sp.exp(-2 * eb * pf)] * 3)
gin = gam.inv()
Ni = [eb * (sp.diff(Bf, X[0]) + Sf), eb * sp.diff(Bf, X[1]), eb * sp.diff(Bf, X[2])]      # S along x, used with k along z
Gam = [[[sum(gin[a, d] * (sp.diff(gam[d, b], X[c]) + sp.diff(gam[d, c], X[b]) - sp.diff(gam[b, c], X[d])) for d in range(3)) / 2
         for c in range(3)] for b in range(3)] for a in range(3)]
DN = [[sp.diff(Ni[j], X[i]) - sum(Gam[k][i][j] * Ni[k] for k in range(3)) for j in range(3)] for i in range(3)]
Kij = sp.Matrix(3, 3, lambda i, j: (sp.diff(gam[i, j], t) - DN[i][j] - DN[j][i]) / (2 * N))
Kup = gin * Kij * gin
KK = sum(Kij[i, j] * Kup[i, j] for i in range(3) for j in range(3))
trK = sum(gin[i, j] * Kij[i, j] for i in range(3) for j in range(3))


def Ric(b, c):
    return sum(sp.diff(Gam[a][b][c], X[a]) - sp.diff(Gam[a][b][a], X[c]) +
               sum(Gam[a][a][d] * Gam[d][b][c] - Gam[a][c][d] * Gam[d][b][a] for d in range(3)) for a in range(3))


R3 = sum(gin[b, c] * Ric(b, c) for b in range(3) for c in range(3))
ai = [sp.diff(sp.log(N), xi) for xi in X]
aa = sum(gin[i, j] * ai[i] * ai[j] for i in range(3) for j in range(3))
Lfull = N * sp.exp(-3 * eb * pf) * (KK - (1 + ep) * trK ** 2 + R3 + al * aa)
L2 = sp.expand((sp.diff(Lfull, eb, 2) / 2).subs(eb, 0))
EL = euler_equations(L2, [nf, pf, Bf, Sf], [t, x, y, z])
k, w, v, GA, mu = sp.symbols('k omega v G_ae mu', real=True)
An, Ap, AB, AS = sp.symbols('A_n A_psi A_B A_S')
ph = sp.exp(sp.I * (k * z - w * t))
fsub = {nf: An * ph, pf: Ap * ph, Bf: AB * ph, Sf: AS * ph}
ELk = [sp.expand(sp.simplify((e.lhs - e.rhs).subs(fsub).doit() / ph)) for e in EL]
names = ["dL/dn", "dL/dpsi", "dL/dB", "dL/dS"]
for nm, e in zip(names, ELk):
    P_(f"    {nm:8s} (Fourier, k along z, S transverse): {sp.factor(e)}")
lam = 1 + ep
hand = [2 * k ** 2 * (al * An - 2 * Ap),
        -6 * (1 - 3 * lam) * (-w ** 2) * Ap - 2 * (1 - 3 * lam) * (-k ** 2) * (-sp.I * w) * AB - 4 * (-k ** 2) * Ap + 4 * (-k ** 2) * An,
        2 * (1 - 3 * lam) * (-k ** 2) * (-sp.I * w) * Ap + 2 * (1 - lam) * k ** 4 * AB,
        k ** 2 * AS]
diffs = [sp.simplify(sp.expand(a - b)) for a, b in zip(ELk, hand)]
check("A1 the Euler-Lagrange equations of the symbolically derived quadratic action equal the documented linear system "
      "(Hamiltonian, trace-evolution, momentum, transverse-shift), term by term",
      f"residuals {diffs}; built in {time.time() - T0:.1f}s", all(d == 0 for d in diffs),
      "the documented forms: 2k^2(c14 n - 2 psi); the psi equation with (1 - 3 lambda) kinetic terms; the momentum constraint "
      "2(1 - 3 lambda) lap d_t psi + 2(1 - lambda) lap^2 B; and -lap S -> +k^2 S (GR's vector sector, beta = 0)")

# ================================================================================================ A2 the moving-source solver
Pf = 1 / (16 * sp.pi * GA)
gm = 1 / sp.sqrt(1 - v ** 2)
GN = GA / (1 - al / 2)
kp = sp.symbols('kp', positive=True)
BOOST = {k: kp * sp.sqrt(1 + (gm ** 2 - 1) * mu ** 2), w: gm * kp * mu * v}


def solve(rho_m, rho_ph, eps=ep, alp=al, ph_momentum=False):
    """exact Fourier solution for a source moving at v (aether frame): rho_m carries momentum rho_m v (and stress rho_m v^2);
    rho_ph enters the Hamiltonian constraint only -- unless ph_momentum (the MUTATE control)."""
    J_long = (rho_m + (rho_ph if ph_momentum else 0)) * w          # k.J along the steady flow
    Pi = (rho_m + (rho_ph if ph_momentum else 0)) * v ** 2
    sb = {ep: eps, al: alp}
    eqs = [sp.Eq(Pf * ELk[0].subs(sb), rho_m + rho_ph),            # P EL_n - (rho) = 0
           sp.Eq(Pf * ELk[1].subs(sb), Pi),                          # P EL_psi - Pi = 0
           sp.Eq(Pf * ELk[2].subs(sb), sp.I * J_long)]               # P EL_B - i k.J = 0  (d_i J^i = -d_t rho)
    s = sp.solve(eqs, [An, Ap, AB], dict=True)
    return s[0] if s else None


def h00_rest(sol, rho_m, ph_momentum_rho=0):
    """rest-frame h'_00 = gamma^2 (h_00 + 2 v^i h_0i + v^i v^j h_ij) in k' space (Jacobian gamma, k_par = gamma k'_par)."""
    PhiB = sol[An] - sp.I * w * sol[AB]                                  # n + dB/dt, gauge invariant
    Jt = rho_m + ph_momentum_rho
    S_dot_v = S_PER_J * Jt * (v ** 2 - w ** 2 / k ** 2)                   # transverse shift from the derived P EL_S + J_T = 0
    h = gm ** 2 * (-2 * PhiB - 2 * v ** 2 * sol[Ap] + 2 * S_dot_v)
    return sp.simplify(gm * h.subs(BOOST))


def v2_parts(expr):
    s = sp.expand(sp.simplify(sp.series(expr, v, 0, 3).removeO()))
    return sp.simplify(s.coeff(v, 0)), sp.factor(sp.simplify(s.coeff(v, 2).subs(mu, 0))), sp.factor(sp.simplify(s.coeff(v, 2).coeff(mu, 2)))


S_PER_J = sp.solve(sp.Eq(Pf * ELk[3] + 1, 0), AS)[0]                 # transverse shift per unit transverse current
P_(f"    transverse shift per unit current (derived): S = {S_PER_J} x J_T   (GR: -16 pi G/k^2)")
M, Mb, Mp = sp.symbols('M M_b M_p', positive=True)
banner("CONTROLS")
# C1 GR
solg = solve(gm * M, 0)
hg = h00_rest(solg, gm * M)
rg = sp.limit(sp.limit(hg / (8 * sp.pi * GA * M / kp ** 2), al, 0), ep, 0)
o0, iso, ani = v2_parts(rg)
check("C1 GR LIMIT (c_2, c_14 -> 0): the rest-frame h'_00 of a mass moving through the frame equals the static 8 pi G M/k^2 "
      "at O(v^0) and O(v^2) -- the pipeline (boost, Jacobian, contraction, vector sector, stresses) is Lorentz invariant",
      f"O(1) {o0}; O(v^2) isotropic {iso}, anisotropic {ani}", o0 == 1 and iso == 0 and ani == 0)
# C2 literature
rk = h00_rest(solg, gm * M) / (8 * sp.pi * GN * M / kp ** 2)
o0, A, C = v2_parts(rk)
alpha2_lit = al * (al - ep + 2 * al * ep) / (ep * (2 - al))
alpha1_mine = sp.simplify(C - 2 * A - C) if False else sp.simplify(-2 * A)     # Will: h00 ⊃ -(a1 - a2) w^2 U - a2 w^i w^j U_ij
# (k-space -> x-space: 8piG_N M/k^2 [1 + A v^2 + C v^2 mu^2]  <->  2U + (2A + C) v^2 U - C U (v.x)^2/r^2)
d2 = sp.simplify(C - alpha2_lit); d1 = sp.simplify(alpha1_mine + 4 * al)
OUT["numbers"]["C2"] = dict(alpha2=str(sp.factor(C)), alpha1=str(alpha1_mine))
check("C2 LITERATURE: the same pipeline returns the khronometric PPN parameters of Yagi, Blas, Barausse & Yunes 2014 "
      "(eqs. 48-49, beta = 0) EXACTLY: alpha_2 = c14 (c14 - c2 + 2 c14 c2)/(c2 (2 - c14)) and alpha_1 = -4 c14",
      f"alpha_2 = {sp.factor(C)} (minus literature: {d2}); alpha_1 = {alpha1_mine} (+4 c14: {d1}); O(1) = {o0}",
      d2 == 0 and d1 == 0 and o0 == 1, "Will's convention: g_00 contains -(alpha_1 - alpha_2) w^2 U - alpha_2 w^i w^j U_ij")
# C3 L330 at c_2 = 0
s0 = sp.solve([sp.Eq(Pf * ELk[0].subs(ep, 0), gm * Mb + gm * Mp), sp.Eq(Pf * ELk[2].subs(ep, 0), sp.I * gm * Mb * w)],
              [An, Ap], dict=True)[0]
s00 = sp.solve([sp.Eq(Pf * ELk[0].subs({ep: 0, al: 0}), gm * Mb + gm * Mp), sp.Eq(Pf * ELk[2].subs({ep: 0, al: 0}), sp.I * gm * Mb * w)],
               [An, Ap], dict=True)
n0 = sp.simplify(s0[An])
check("C3 L330 REPRODUCED: at c_2 = 0 a moving momentless source can sit only in the lapse, n = 8 pi G gamma M_ph/(c14 k^2) "
      "(amplified 1/c14 ~ 1e5), and at c_14 = 0 there is no solution at all -- the frozen-phantom identity",
      f"n = {n0}; solutions at c14 = 0: {len(s00)}",
      sp.simplify(n0 - 8 * sp.pi * GA * Mp * gm / (al * k ** 2)) == 0 and len(s00) == 0)
# C4 series vs exact (numbers)
ph_m = MUTATE
solp = solve(0, gm * Mp, ph_momentum=ph_m)
n_ratio_exact = sp.lambdify((v, mu, al, ep), sp.simplify(gm * solp[An].subs(BOOST) / (-4 * sp.pi * GN * Mp / kp ** 2)), "numpy")
o0p, An_iso, Cph = v2_parts(sp.simplify(gm * solp[An].subs(BOOST) / (-4 * sp.pi * GN * Mp / kp ** 2)))
Cph_f = sp.lambdify((al, ep), Cph, "numpy"); Aiso_f = sp.lambdify((al, ep), An_iso, "numpy")
errs = []
for vv in (1e-3, 2e-3):
    for mm in (0.0, 0.5, 1.0):
        ex = complex(n_ratio_exact(vv, mm, 1e-5, 2.5e-5)).real
        se = 1 + vv ** 2 * (float(Aiso_f(1e-5, 2.5e-5)) + float(Cph_f(1e-5, 2.5e-5)) * mm ** 2)
        errs.append(abs(ex - se))
check("C4 the O(v^2) series of the phantom's aether response matches the exact finite-v solution (c14 = 1e-5, c2 = 2.5e-5, "
      "v = 300-600 km/s, three angles) to < 1e-4",
      f"max |exact - series| = {max(errs):.2e}", max(errs) < 1e-4)

# ================================================================================================ R1 carried
banner("R1  THE c_2 CHANNEL CARRIES THE PHANTOM: what matter feels and what light sees")
f = sp.symbols('f', positive=True)
solmix = solve(gm * Mb, gm * Mp, ph_momentum=MUTATE)
hmix = h00_rest(solmix, gm * Mb, ph_momentum_rho=(gm * Mp if MUTATE else 0))
rmix = sp.simplify(hmix / (8 * sp.pi * GN * (Mb + Mp) / kp ** 2))
o1, A1, C1_ = v2_parts(rmix)
C1f = sp.factor(sp.simplify(C1_.subs(Mp, f * Mb / (1 - f))))
lead_dyn = sp.factor(sp.limit(sp.simplify(C1f * ep), ep, 0))
lens = sp.simplify(gm * (solmix[An] - sp.I * w * solmix[AB] + solmix[Ap]).subs(BOOST) / (-8 * sp.pi * GN * (Mb + Mp) / kp ** 2))
ol, _, Cl = v2_parts(lens)
Clf = sp.factor(sp.simplify(Cl.subs(Mp, f * Mb / (1 - f))))
P_(f"    dynamics: alpha_2^eff(f) = {C1f};  leading in 1/c2: {lead_dyn}/c2")
lead_lens = sp.factor(sp.limit(sp.simplify(Clf * ep), ep, 0))
P_(f"    lensing (n + psi)/2 rest frame: O(1) {ol}; mu^2 v^2 coefficient {Clf};  leading in 1/c2: {lead_lens}/c2")
a2num = [abs(float(C1f.subs({al: a_, ep: e_, f: ff}))) for a_, e_ in ((1e-5, 1e-5), (1e-5, 2.5e-5)) for ff in (0.3, 0.6, 0.9)]
v620 = 620 / 299792.458
OUT["numbers"]["R1"] = dict(alpha2_eff=str(C1f), leading=str(lead_dyn), max_alpha2eff=max(a2num))
check("R1 CARRIED: the co-moving solution exists for c_2 > 0; the potential matter feels and the lensing potential carry the "
      "full phantom (O(1) coefficient 1), with a preferred-frame anisotropy alpha_2^eff whose enhanced part is proportional to "
      "c_14 -- at the record's corner |alpha_2^eff| (620 km/s / c)^2 < 1e-5, and at f = 0 it is the literature alpha_2",
      f"O(1) dyn {o1}, lens {ol}; max |alpha_2^eff| {max(a2num):.2f} -> x v^2 = {max(a2num) * v620 ** 2:.1e}; "
      f"f=0 minus literature: {sp.simplify(C1f.subs(f, 0) - alpha2_lit)}; enhanced lensing minus enhanced dynamics: "
      f"{sp.simplify(lead_lens - lead_dyn)}",
      o1 == 1 and ol == 1 and max(a2num) * v620 ** 2 < 1e-5 and sp.simplify(C1f.subs(f, 0) - alpha2_lit) == 0
      and sp.simplify(lead_lens - lead_dyn) == 0,
      "the answer to L330's open question: YES, the channel carries the phantom inside the alpha_1/alpha_2 bounds")

# ================================================================================================ R2 the price
banner("R2  THE PRICE: the aether's acceleration a_i = d_i n (the MOND sector's input) is distorted ~ 2/c_2")
solb = solve(gm * Mb, 0)
_, Ab_iso, Cb = v2_parts(sp.simplify(gm * solb[An].subs(BOOST) / (-4 * sp.pi * GN * Mb / kp ** 2)))
Cph_s = sp.factor(Cph); Cb_s = sp.factor(Cb)
lead_ph = sp.factor(sp.limit(sp.simplify(Cph * ep), ep, 0)); lead_b = sp.factor(sp.limit(sp.simplify(Cb * ep), ep, 0))
P_(f"    phantom: C_ph = {Cph_s}  (leading {lead_ph}/c2);  isotropic {sp.factor(An_iso)}")
P_(f"    baryons: C_b  = {Cb_s}  (leading {lead_b}/c2)")
# covariance: a_i - grad Phi_B = -grad dB/dt exactly (the aether's own acceleration)
cov = sp.simplify((solp[An]) - (solp[An] - sp.I * w * solp[AB]) - sp.I * w * solp[AB])
target = (4 + 4 * ep + al * ep) / (ep * (2 - al))
OUT["numbers"]["R2"] = dict(C_ph=str(Cph_s), C_b=str(Cb_s), leading_ph=str(lead_ph), leading_b=str(lead_b))
check("R2 THE PRICE: the phantom's aether-acceleration distortion is delta n = C_ph v^2 (v.grad)^2 lap^-1 Phi_ph with "
      "C_ph = (4 + 4 c2 + c14 c2)/(c2 (2 - c14)) -> 2/c_2 NOT suppressed by c_14, while baryons' own is (c14/c2)-suppressed",
      f"C_ph - target = {sp.simplify(Cph - target)}; c2 C_ph -> {lead_ph} at c2 -> 0 (at c14 = 0: {sp.limit(lead_ph, al, 0)}); "
      f"c2 C_b -> {lead_b}",
      sp.simplify(Cph - target) == 0 and sp.limit(lead_ph, al, 0) != 0 and sp.limit(lead_b, al, 0) == 0,
      "a_i is the covariant acceleration of the aether congruence; a_i - grad Phi_B = -grad(dB/dt), the aether's own "
      "acceleration as it is dragged (the identity holds identically in the solution: residual %s)" % cov)

# ================================================================================================ R3 a real galaxy
banner("R3  A REAL GALAXY: nu_RAR phantom of a Hernquist baryonic sphere; the input distortion vs radius and angle to v")
G, MSUN, KPC = 6.6743e-11, 1.98892e30, 3.0856775814913673e19
A0 = {"canonical": 9.3619e-11, "alt": 1.1279e-10}
nu = lambda y: 1.0 / (1.0 - np.exp(-np.sqrt(y)))
r = np.geomspace(0.05, 300, 40000) * KPC


def galaxy(Mbar, a_h, a0):
    gN = G * Mbar * MSUN / (r + a_h * KPC) ** 2
    gobs = nu(gN / a0) * gN; gph = gobs - gN
    Phi = np.concatenate([[0], np.cumsum(0.5 * (gph[1:] + gph[:-1]) * np.diff(r))])      # Phi_ph up to a constant
    m = np.concatenate([[0], np.cumsum(0.5 * (Phi[1:] * r[1:] ** 2 + Phi[:-1] * r[:-1] ** 2) * np.diff(r))]) + Phi[0] * r[0] ** 3 / 3
    c1 = m / r ** 2; c2_ = Phi - 2 * m / r ** 3; c3 = gph - 2 * Phi / r + 6 * m / r ** 4
    rad_par = c3                              # d_r of (z.grad)^2 chi along v (theta = 0)
    rad_perp = c2_ / r - c1 / r ** 2          # perpendicular (theta = 90)
    tang = (c2_ - c1 / r) / r                 # |delta a_theta| / sin 2theta
    return gN, gobs, gph, rad_par, rad_perp, tang


rows = {}
for foot, a0 in A0.items():
    for Mbar, a_h in ((1e10, 1.0), (5e10, 2.0), (2e11, 4.0)):
        gN, gobs, gph, rpar, rperp, tang = galaxy(Mbar, a_h, a0)
        # per unit D (= C_ph v^2): distortion of the radial input relative to g_obs
        sel = [np.argmin(abs(r / KPC - R)) for R in (2, 5, 10, 20, 50)]
        rows[f"{foot}_{Mbar:.0e}"] = dict(R=[2, 5, 10, 20, 50], f_ph=[float(gph[i] / gobs[i]) for i in sel],
                                          par=[float(rpar[i] / gobs[i]) for i in sel], perp=[float(rperp[i] / gobs[i]) for i in sel],
                                          avg=[float((rpar[i] + 2 * rperp[i]) / 3 / gobs[i]) for i in sel],
                                          tang=[float(tang[i] / gobs[i]) for i in sel])
        if foot == "canonical":
            P_(f"    M_b {Mbar:.0e}: R = 2/5/10/20/50 kpc  phantom share " + "/".join(f"{rows[f'{foot}_{Mbar:.0e}']['f_ph'][j]:.2f}" for j in range(5))
               + ";  delta a_r/g_obs per unit D: along v " + "/".join(f"{rows[f'{foot}_{Mbar:.0e}']['par'][j]:.3f}" for j in range(5))
               + ", across v " + "/".join(f"{rows[f'{foot}_{Mbar:.0e}']['perp'][j]:.3f}" for j in range(5))
               + ";  tilt " + "/".join(f"{rows[f'{foot}_{Mbar:.0e}']['tang'][j]:.3f}" for j in range(5)))
# deep-MOND closed form: at large r both radial directions -> f/3, tilt -> f/3
big = rows["canonical_1e+10"]
deep_ok = abs(big["par"][4] / big["f_ph"][4] - 1 / 3) < 0.03 and abs(big["perp"][4] / big["f_ph"][4] - 1 / 3) < 0.03 \
    and abs(big["tang"][4] / big["f_ph"][4] - 1 / 3) < 0.03
OUT["numbers"]["R3"] = rows
check("R3 A REAL GALAXY: in the deep-MOND region the radial input distortion is ISOTROPIC, (D/3) x phantom share, and the tilt "
      "is (D/3) sin 2theta x share (closed form: Phi_ph = V^2 ln r -> lap^-1 = V^2 r^2 (ln r - 5/6)/6), reproduced numerically",
      f"M_b 1e10 at 50 kpc: along v {big['par'][4]/big['f_ph'][4]:.3f}, across {big['perp'][4]/big['f_ph'][4]:.3f}, tilt "
      f"{big['tang'][4]/big['f_ph'][4]:.3f} (x share; closed form 1/3 each)", deep_ok,
      "an isotropic enhancement acts on the MOND sector like a larger a0; the tilt is a quadrupole aligned with the CMB-frame velocity")

# ================================================================================================ R4 the branches
banner("R4  THE BRANCHES: D = C_ph v^2 at 300 and 620 km/s (the Local Group through the CMB frame), with PPN alpha_2")
branches = [(1e-5, 1e-5), (1e-5, 2.5e-5), (8e-7, 1e-4), (8e-7, 1e-3), (8e-7, 0.05)]
tab = []
for c14, c2v in branches:
    a2 = c14 * (c14 - c2v + 2 * c14 * c2v) / (c2v * (2 - c14))
    Cv = float(Cph_f(c14, c2v))
    D300, D620 = Cv * (300 / 299792.458) ** 2, Cv * (620 / 299792.458) ** 2
    tab.append(dict(c14=c14, c2=c2v, alpha2=a2, alpha2_ok=abs(a2) < 4e-7, D300=D300, D620=D620))
    P_(f"    c14 {c14:.0e}, c2 {c2v:.1e}: alpha_2 {a2:+.2e} ({'ok' if abs(a2) < 4e-7 else 'VIOLATES 4e-7'});  D(300) {D300:.3f}, "
       f"D(620) {D620:.3f};  deep-MOND radial input +{D620/3:.1%} at 620 km/s")
OUT["numbers"]["R4"] = tab
corner = [b for b in tab if b["c14"] == 1e-5]
far = [b for b in tab if b["c2"] >= 1e-3]
P_("    (at c14 = 1e-5 alpha_2 confines c2 to within 8% of c2* = c14/(1 - 2 c14) = 1.0e-5; c2 = 2.5e-5 is the closure-locus value "
   "at |K_2| = 3.2e5 and violates alpha_2 -- shown for reference)")
check("R4 THE DICHOTOMY: at the record's corner (c14 = 1e-5, c2 = 1e-5 .. 2.5e-5) the Local Group's 620 km/s gives a deep-MOND "
      "input distortion D/3 >= 0.10; the branches with D/3 < 0.01 at 620 km/s (c2 >= 1e-3) pass alpha_2 only with c14 <~ 8e-7",
      "corner D/3 = " + ", ".join(f"{b['D620']/3:.2f}" for b in corner) + "; far branches: " +
      ", ".join(f"c2 {b['c2']:.0e}: D/3 {b['D620']/3:.4f}, alpha_2 {b['alpha2']:+.1e}" for b in far),
      min(b["D620"] for b in corner) / 3 >= 0.10 and all(b["D620"] / 3 < 0.01 and b["alpha2_ok"] for b in far),
      "either a0 tracks each galaxy's speed through the CMB frame (falsifiable), or c2 >> 1e-4 with c14 <~ 8e-7")

# ================================================================================================ verdict
banner("VERDICT")
P_(f"""  L330 asked whether the khronon's c_2 channel can carry a moving galaxy's phantom.  It can.  With the action derived here and
  the pipeline certified on GR (Lorentz invariance) and on the published khronometric alpha_1, alpha_2 (exact), the co-moving
  solution exists for any c_2 > 0: dynamics and lensing carry the full phantom, with preferred-frame corrections ~ v^2.
  THE PRICE is in the aether's own acceleration -- the MOND sector's input -- distorted by C_ph v^2 ~ 2 v^2 / c_2 times the
  phantom: at the record's corner and the Local Group's 620 km/s that is D/3 = {corner[0]['D620']/3:.2f} .. {corner[1]['D620']/3:.2f} in
  deep MOND, isotropic in the radial input plus a quadrupolar tilt along the CMB-frame velocity.  So the one momentum
  channel on the record turns the moving-source gate into a SPEED-DEPENDENT a0: a0_eff ~ a0 (1 + 2 v_CMB^2/(3 c^2 c_2))^O(1),
  a prediction ΛCDM and velocity-blind MOND do not make -- or, if the data show no such dependence, c_2 >= 1e-3 and then
  c_14 <~ 8e-7 by alpha_2.  NOT computed here: the MOND sector's nonlinear feedback (the O(1) exponent), and the local
  khronon frame where larger-scale momentless phantoms drag it (drag fraction ~ (2/c_2) Phi_ph).""")

n_fail = sum(1 for _, ok_, lb in CH if lb and not ok_)
OUT["n_checks"], OUT["n_fail_load_bearing"] = len(CH), n_fail
outname = f"{SLUG}_results{'_MUTATE' if MUTATE else ''}.json"
json.dump(OUT, open(os.path.join(HERE, outname), "w"), indent=1, default=str)
P_(f"\n  {sum(1 for _, ok_, _ in CH if ok_)}/{len(CH)} checks pass; load-bearing failures: {n_fail}; wrote {outname}; {time.time()-T0:.0f}s")
sys.exit(0 if n_fail == 0 else 1)
