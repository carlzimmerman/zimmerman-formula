#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
CFG3_principle -- THE FOUNDING PRINCIPLE AND WHAT IT FORCES (sympy derivations; lane CFG3, campaign fresh gravity).

THE PRINCIPLE, in plain words.  "The vacuum answers matter that has fallen behind it."
  Empty space has two properties of its own: an energy density rho_Lambda and the expansion rate it would have alone,
  H_Lambda = sqrt(8 pi G rho_Lambda / 3).  (i) Matter that still expands at least as fast as empty space (local expansion
  rate theta/3 >= H_Lambda) is carried along by it: gravity there is GR.  (ii) Matter that has fallen behind (theta/3 has
  dropped below H_Lambda at some time -- every bound system and its infall zone) holds the vacuum back, and the vacuum answers
  its gravity: as a bath whose rate is the vacuum's own free-fall rate a0/c = kappa sqrt(G rho_Lambda), it amplifies each
  free-fall mode of that matter by the mode's Bose occupation.  (iii) The answer belongs to the whole held-back region and is
  read in the region's own free fall.  (iv) The dark component is a state of the vacuum itself and is not answered.  (v) The
  answer is coherent only above a length l*, the vacuum state's own Airy length at a0 (tied to the dark field's mass).

WHAT IS DERIVED HERE (each a sympy identity or a numerical check that can fail):
  D1  a0's form: the unique acceleration from (G, c, rho) (det = 2, the record's theorem), a0/c = H_Lambda/Z, XR30's
      a0 = (kappa/sqrt(24 pi)) c^2 K_inf with K_inf = sqrt(3 Lambda); FP0's committed a0 pair and Z reproduced (controls).
  D2  the kernel: x = t_vac/t_dyn = sqrt(g_N/a0) (the length cancels); nu = 1 + n_BE(x) = 1/(1 - e^-sqrt(y)); the deep
      (Rayleigh-Jeans) limit gives g = sqrt(g_N a0) with coefficient exactly 1; the Newtonian (Wien) tail is e^-sqrt(y);
      g(g_N) is strictly increasing (XC2's uniqueness condition); the phantom x^2/(e^x - 1) turns over at y_p = x_p^2 =
      2.5396 -- the record's own y_p (control) -- so the Bose kernel carries the non-monotone phantom L340 A1 forbids in the
      record's two-field completion (flagged).  The kernel is the record's nu_RAR = McGaugh et al. 2016's RAR function
      (overlap, labelled).
  D3  the field equations: a bi-potential action with the gate G(x) and the coherence filter S inside the vacuum's term;
      Euler-Lagrange (sympy, 3-D) gives lap psi = 4 pi G rho and lap Phi = div{S[G (nu - 1) S grad psi]} + lap psi: the
      double filter is forced by putting S in the action (S symmetric => S^T = S, checked).  [Form = QUMOND's (Milgrom 2010):
      overlap, labelled.]  The baryons-only reading (iv) with a dark field present is stated at field-equation level; its
      action is OPEN.
  D4  gamma = 1: the answer is a static, pressureless gravitating source (T_ij = 0), so the linearised Einstein equations
      (sympy, general static Phi, Psi) give Phi = Psi: light bending follows the dynamical potential.
  D5  THE LINEAR WEB IS GR, DERIVED: H^2 - H_Lambda^2 = 8 pi G rho_m / 3 > 0 at every z, so the background is never behind
      the vacuum; linearly theta/3 = H (1 - f delta/3) < H_Lambda needs delta > delta_th(z) = 3 (1 - H_Lambda/H)/f >= 0.99
      at every z <= 1100: the gate indicator is identically 0 at first order in delta -> the linear equations are GR + the
      dark field (XR26's primary CMB and linear lensing are LCDM's exactly).  Top-hat: the gate opens at a linear delta close
      to turnaround's (table).
  D6  compensation (Gauss): the answer vanishes on the region's boundary, so each region carries ZERO net phantom mass: a
      negative surface layer -M_b (nu(r_g) - 1) at r_g; a thin shell's excess surface density at R << r_g is O(R^2/r_g^2).
  D7  the free-fall frame: a uniform external field is removed exactly (equivalence principle); only the external TIDAL
      field survives, at O(r/D) of the external field.
  D8  the coherence length: coarse-graining that composes (semigroup, isotropic, finite variance) is the heat kernel; the
      Airy length l_A = (hbar^2/(2 m^2 a0))^(1/3) (sympy, Schroedinger in a linear potential); FP17's B2 numbers reproduced
      in FP17's convention (control); ONE_NEW_THING's 2e-22 eV <-> 0.032 pc reproduced.
  D9  FP17's theorem recap (control): (GM, r, a0, c, Lambda) have rank 2 -> 3 groups; the Solar System needs a length, and
      the principle's l* is that length.
  D10 the constant count (fitted / declared / tied / derived).

PRE-DECLARED HYPOTHESES (written before the first run of this script):
  H1 every sympy identity in D1-D4, D6, D8 holds exactly; the controls (FP0's a0 pair and Z to 1e-12; the record's y_p =
     2.5396 to 1e-6; FP17's B2 lengths to 1e-3) reproduce.  EXPECT TRUE.
  H2 [load-bearing; the MUTATE must fail] D5: min over z in [0, 1100] of delta_th(z) >= 0.9, i.e. the gate is closed on
     the linear web at first order.  EXPECT TRUE (min ~0.99 at z = 0).
  H3 the Bose kernel's phantom is non-monotone above y_p (C_L < 0 there; min C_L ~ -0.03): EXPECT TRUE (a flagged liability
     for any future two-field completion, harmless for the static law since dg/dg_N = 1 + C_L > 0).
  H4 the top-hat gate opens (theta/3 = H_Lambda) at a linear delta below turnaround's at z = 0 and approaching it at z >= 1.
     UNCERTAIN in detail.
MUTATE=1: the principle made active in expanding matter (the vacuum answers ALL matter; threshold theta_* -> infinity).  H2's
check must FAIL (the gate is open on the linear web), rc = 1.  Outputs CFG3_principle_MUTATE.out / _results_MUTATE.json.
Run from the repository root:  MUTATE=1 python3 campaign_fresh_gravity/CFG3_principle.py; python3 campaign_fresh_gravity/CFG3_principle.py
"""
import os, sys, math, json
sys.dont_write_bytecode = True
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import CFG3_common as C
import numpy as np
import sympy as sp
from scipy.integrate import solve_ivp
from scipy.optimize import brentq

R = C.Run("CFG3_principle", __doc__)
P, check = R.P, R.check
if C.MUTATE:
    P("\n  *** MUTATE=1: the vacuum answers ALL matter (threshold theta_* -> infinity): H2's check D5 must FAIL, rc = 1 ***")

# ================================================================================================ D1
R.banner("D1  a0's FORM AND THE VACUUM'S TWO RATES")
a_, b_, d_ = sp.symbols("alpha beta gamma")
Mdim = sp.Matrix([[0, -1, 1], [1, 3, -3], [-1, -2, 0]])      # rows M, L, T; columns: exponents of c, G, rho
sol = sp.solve([-b_ + d_, a_ + 3 * b_ - 3 * d_ - 1, -a_ - 2 * b_ + 2], [a_, b_, d_])
detM = Mdim.det()
P(f"    a0 = c^alpha G^beta rho^gamma: {sol}; |det| = {abs(detM)}")
kap, Gs, rhoL, cs, Lam = sp.symbols("kappa G rho_Lambda c Lambda", positive=True)
a0_expr = kap * cs * sp.sqrt(Gs * rhoL)
HL = sp.sqrt(8 * sp.pi * Gs * rhoL / 3)
Zs = sp.simplify(cs * HL / a0_expr)
Z_half = sp.nsimplify(Zs.subs(kap, sp.Rational(1, 2)))
Kinf = sp.sqrt(3 * Lam)
xr30 = sp.simplify((kap / sp.sqrt(24 * sp.pi)) * cs ** 2 * Kinf - a0_expr.subs(rhoL, Lam * cs ** 2 / (8 * sp.pi * Gs)))
a0_can = 0.5 * C.C_SI * math.sqrt(C.G_SI * C.RHO_L)
a0_alt = 0.5 * C.C_SI * math.sqrt(C.G_SI * C.RHO_L / C.OML_FP0)
dev1 = max(abs(a0_can / C.A0["canonical"] - 1), abs(a0_alt / C.A0["alt"] - 1), abs(float(Z_half) / C.Z_FP0 - 1))
P(f"    Z = c H_Lambda / a0 = {Zs} -> {Z_half} = {float(Z_half):.9f} at kappa = 1/2;  XR30 identity residual: {xr30}")
P(f"    a0 = (c/2) sqrt(G rho_Lambda) = {a0_can:.10e} (FP0 {C.A0['canonical']:.10e}); alt (c/2) sqrt(G rho_crit) = {a0_alt:.10e} (FP0 {C.A0['alt']:.10e})")
P(f"    the vacuum's rates: H_Lambda = {C.H_L:.4e} 1/s (expansion alone); a0/c = {C.A0['canonical'] / C.C_SI:.4e} 1/s = H_Lambda/Z (free fall)")
check("D1 CONTROL + IDENTITY: a0 = kappa c sqrt(G rho) is the unique acceleration from (G, c, rho) (exponents 1, 1/2, 1/2; |det| = 2, "
      "the record's theorem); Z = c H_Lambda/a0 = sqrt(8 pi/3)/kappa = 2 sqrt(8 pi/3) at kappa = 1/2; XR30's (kappa/sqrt(24 pi)) c^2 "
      "sqrt(3 Lambda) is the same a0; FP0's committed a0 pair and Z are reproduced",
      f"exponents {sol}, |det| {abs(detM)}; Z {Z_half}; XR30 residual {xr30}; max rel dev vs FP0 {dev1:.1e}",
      sol == {a_: 1, b_: sp.Rational(1, 2), d_: sp.Rational(1, 2)} and abs(detM) == 2 and sp.simplify(Z_half - 2 * sp.sqrt(8 * sp.pi / 3)) == 0
      and xr30 == 0 and dev1 < 1e-12)
R.num("D1", dict(Z=float(Z_half), a0_canonical=a0_can, a0_alt=a0_alt, H_Lambda=C.H_L, a0_over_c=C.A0["canonical"] / C.C_SI))

# ================================================================================================ D2
R.banner("D2  THE KERNEL FROM THE BOSE OCCUPATION OF THE MATTER'S FREE-FALL MODE")
ell, gN, a0s, y, x = sp.symbols("ell g_N a_0 y x", positive=True)
t_dyn = sp.sqrt(2 * ell / gN)                                  # free fall over ell under the matter's Newtonian field
t_vac = sp.sqrt(2 * ell / a0s)                                 # the same length under the vacuum's acceleration
x_expr = sp.simplify(t_vac / t_dyn)
nBE = 1 / (sp.exp(x) - 1)
nu_x = sp.simplify(1 + nBE)
nu_y = nu_x.subs(x, sp.sqrt(y))
ident = sp.simplify(nu_y - 1 / (1 - sp.exp(-sp.sqrt(y))))
deep = sp.limit(nu_y * sp.sqrt(y), y, 0)                     # nu -> 1/sqrt(y)  =>  g = nu g_N -> sqrt(g_N a0)
g_deep = sp.simplify((deep / sp.sqrt(gN / a0s)) * gN)
wien = sp.limit((nu_y - 1) * sp.exp(sp.sqrt(y)), y, sp.oo)
fd_deep = sp.limit(1 + 1 / (sp.exp(sp.sqrt(y)) + 1), y, 0)     # Fermi-Dirac: no classical enhancement
P(f"    t_vac/t_dyn = {x_expr} (ell cancels);  nu = 1 + n_BE = {nu_x} = 1/(1 - e^-sqrt(y)): residual {ident}")
P(f"    deep (Rayleigh-Jeans) limit: nu sqrt(y) -> {deep}  =>  g -> {g_deep};  Wien tail (nu - 1) e^sqrt(y) -> {wien};  Fermi-Dirac at y -> 0: {fd_deep}")
ys = np.logspace(-8, 6, 20001)
gy = ys * C.nu_bose(ys)
dg = np.gradient(gy, ys)
hy = ys * (C.nu_bose(ys) - 1)
CL = np.gradient(hy, ys)
xp = brentq(lambda t: 2 * (math.exp(t) - 1) - t * math.exp(t), 1.0, 2.0)
yp = xp ** 2
P(f"    phantom h = y (nu - 1) = x^2/(e^x - 1) (the Planck number-spectrum shape) peaks at x_p = {xp:.6f}, y_p = {yp:.6f} "
  f"(the record's nu_RAR peak Y_P = {C.Y_PEAK:.6f});  min dg/dg_N = {dg.min():.4f}; min C_L = dh/dy = {CL.min():+.4f} at y = {ys[np.argmin(CL)]:.2f}")
dev_rar = float(np.max(np.abs(C.nu_bose(ys) / C.nu_rar(ys) - 1)))
check("D2 THE KERNEL IS DERIVED: the vacuum's free-fall time over any length divided by the matter's is x = sqrt(g_N/a0) (the length "
      "cancels); the Bose factor 1 + n_BE(x) is nu = 1/(1 - e^-sqrt(y)); its classical (Rayleigh-Jeans) limit gives g = sqrt(g_N a0) "
      "with coefficient exactly 1 (a0 is the deep-MOND scale, no extra factor); its quantum (Wien) tail is e^-sqrt(y)",
      f"x = {x_expr}; identity residual {ident}; deep g -> {g_deep}; Wien {wien}; |nu_Bose/nu_RAR - 1| <= {dev_rar:.1e}",
      x_expr == sp.sqrt(gN) / sp.sqrt(a0s) and ident == 0 and deep == 1 and sp.simplify(g_deep - sp.sqrt(gN * a0s)) == 0 and wien == 1
      and dev_rar < 1e-12,
      reading="the kernel is the record's nu_RAR, i.e. McGaugh, Lelli & Schombert 2016's RAR fitting function: the FORM overlaps a "
              "published fit; what is new is the reason (Bose occupation at the ratio of free-fall times).  Fermi-Dirac statistics would "
              f"give nu -> {fd_deep} at y -> 0 (no MOND): the Bose statistics is load-bearing (CFG3_sparc's MUTATE)")
check("D2b CONTROL + UNIQUENESS: the Bose kernel's phantom turns over at the Wien peak y_p = 2.5396 -- the record's own nu_RAR peak "
      "(FP1/L340's Y_P) -- and g(g_N) = g_N nu is strictly increasing at every y (XC2: the static law's constraint is then strictly "
      "convex, so the solution is unique)", f"y_p {yp:.6f} vs record {C.Y_PEAK:.6f}; min dg/dg_N {dg.min():.4f}",
      abs(yp - C.Y_PEAK) < 1e-5 and dg.min() > 0)
check("D2c (H3, reported liability) THE NON-MONOTONE PHANTOM: above y_p the Bose kernel's phantom h decreases (C_L = dh/dy < 0; the "
      "Wien suppression), which L340 A1 forbids in the record's two-field completion (FP1 B4: nu_RAR fails, nu_mono is its repair, "
      "<= 0.0104 dex away); harmless for this lane's static law (dg/dg_N = 1 + C_L > 0)",
      f"min C_L {CL.min():+.4f} at y = {ys[np.argmin(CL)]:.2f}; C_L < 0 for y > {ys[np.argmax(CL < 0)]:.4f}", CL.min() < 0 and CL.min() > -1,
      load_bearing=False)
R.num("D2", dict(x_p=xp, y_p=yp, min_dg=float(dg.min()), min_CL=float(CL.min()), y_at_min_CL=float(ys[np.argmin(CL)]), fermi_deep=float(fd_deep)))

# ================================================================================================ D3
R.banner("D3  THE FIELD EQUATIONS FROM A BI-POTENTIAL ACTION WITH THE GATE AND THE COHERENCE FILTER")
X, Y, Zc = sp.symbols("x y z", real=True)
G_ = sp.Symbol("G", positive=True)
Phi = sp.Function("Phi")(X, Y, Zc); psi = sp.Function("psi")(X, Y, Zc)
rho = sp.Function("rho")(X, Y, Zc); gate = sp.Function("Gg")(X, Y, Zc)
Q = sp.Function("Q")
gradsq = sum(sp.diff(psi, v) ** 2 for v in (X, Y, Zc))
# the vacuum's term: a0^2 [ s + G(x) (Q(s) - s) ], s = |grad psi|^2/a0^2  (G = 0: Newton; G = 1: the answer)
s_ = gradsq / a0s ** 2
Lag = -(1 / (8 * sp.pi * G_)) * (2 * sum(sp.diff(Phi, v) * sp.diff(psi, v) for v in (X, Y, Zc)) - a0s ** 2 * (s_ + gate * (Q(s_) - s_))) - rho * Phi
eqs = sp.euler_equations(Lag, [Phi, psi], [X, Y, Zc])
lap = lambda f: sum(sp.diff(f, v, 2) for v in (X, Y, Zc))
e_phi = sp.simplify(eqs[0].lhs - eqs[0].rhs)
res_phi = sp.simplify(e_phi * (4 * sp.pi * G_) - (lap(psi) - 4 * sp.pi * G_ * rho))


def _psi_check():
    """the psi-variation with an explicit nonlinear vacuum function Q(u) = u + u^3/21 (q = Q' = 1 + u^2/7): 8 pi G (EL_psi) must equal
    2 [lap Phi - div((1 + G(q - 1)) grad psi)] on a smooth test configuration (numerical residual)."""
    u_ = sp.Symbol("u")
    qf = sp.Lambda(u_, 1 + u_ ** 2 / 7); Qf = sp.Lambda(u_, u_ + u_ ** 3 / 21)
    Lc = Lag.replace(Q, Qf)
    f = {Phi: sp.sin(X) * sp.cos(2 * Y) + Zc ** 2, psi: sp.exp(-X ** 2 - Y ** 2 / 2 - Zc ** 2 / 3) + X * Y,
         gate: sp.Rational(1, 2) + sp.tanh(X + Y) / 3}
    el = sp.euler_equations(Lc, [Phi, psi], [X, Y, Zc])[1]
    lhs = (el.lhs - el.rhs) * 8 * sp.pi * G_
    tg = 2 * (lap(Phi) - sum(sp.diff((1 + gate * (qf(gradsq / a0s ** 2) - 1)) * sp.diff(psi, v), v) for v in (X, Y, Zc)))
    d = (lhs - tg).subs(f).doit()
    return max(abs(float(d.subs({X: 0.3 * i, Y: -0.2 * i + 0.1, Zc: 0.15 * i - 0.2, a0s: 1.3, G_: 0.7, rho: 1.0}).evalf())) for i in range(1, 4))


psi_dev = _psi_check()
P(f"    varying Phi:  lap psi = 4 pi G rho  (residual {res_phi})")
P(f"    varying psi:  lap Phi = div[(1 + G(x) (q(|grad psi|^2/a0^2) - 1)) grad psi],  q = Q' = nu(sqrt s)  (numerical residual on a test "
  f"configuration: {psi_dev:.1e})")
# the filter: S symmetric (heat kernel) => the action's filter appears on both sides (source and output)
n1 = 64; xs1 = np.linspace(-1, 1, n1); w1 = 0.15
Smat = np.exp(-(xs1[:, None] - xs1[None, :]) ** 2 / (2 * w1 ** 2)); Smat /= Smat.sum(axis=1).mean()
sym_dev = float(np.max(np.abs(Smat - Smat.T)))
P(f"    the coherence filter S (heat kernel) is symmetric (max |S - S^T| = {sym_dev:.1e}): with Q(|grad S psi|^2) in the action the psi "
  "equation reads lap Phi = lap psi + S div[G (nu - 1) grad S psi] -- source AND output filtered (the record's FP1 A3 / FP7 A1b "
  "'double filter forced', here from the principle's 'the answer is a coarse-grained property')")
check("D3 THE FIELD EQUATIONS FOLLOW FROM ONE ACTION: the bi-potential Lagrangian -(1/8 pi G)[2 grad Phi.grad psi - a0^2 (s + G(x)(Q(s) - "
      "s))] - rho Phi gives lap psi = 4 pi G rho and lap Phi = div[(1 + G (nu - 1)) grad psi]: GR/Newton where the gate G = 0, the "
      "answer where G = 1; the heat filter in the action is forced onto both source and output",
      f"Phi-variation residual {res_phi}; psi-variation numerical residual {psi_dev:.1e}; S symmetric {sym_dev:.1e}",
      res_phi == 0 and psi_dev < 1e-9 and sym_dev < 1e-12,
      reading="the bi-potential form is Milgrom 2010's QUMOND (overlap, labelled); the gate, the filter and the baryons-only reading "
              "are this lane's.  With a dark field present (clusters, the web inside gated regions) the principle's (iv) amplifies "
              "only the ordinary matter's field (nu read from the total field): stated at field-equation level; its action is OPEN")

# ================================================================================================ D4
R.banner("D4  LIGHT BENDING FOLLOWS THE SAME POTENTIAL (gamma = 1)")
t_ = sp.Symbol("t")
co = [t_, X, Y, Zc]
Phs = sp.Function("Phi")(X, Y, Zc); Pss = sp.Function("Psi")(X, Y, Zc)
eta = sp.diag(-1, 1, 1, 1)
h = sp.diag(-2 * Phs, -2 * Pss, -2 * Pss, -2 * Pss)
hup = eta * h                                                  # h^rho_nu = eta^{rho a} h_{a nu}
htr = sum(eta[i, i] * h[i, i] for i in range(4))


def Ric(m, n):
    s1 = sum(sp.diff(hup[r, n], co[r], co[m]) + sp.diff(hup[r, m], co[r], co[n]) for r in range(4))
    box = sum(eta[r, r] * sp.diff(h[m, n], co[r], 2) for r in range(4))
    return sp.Rational(1, 2) * (s1 - box - sp.diff(htr, co[m], co[n]))


Rsc = sum(eta[m, m] * Ric(m, m) for m in range(4))
Gein = lambda m, n: sp.simplify(Ric(m, n) - sp.Rational(1, 2) * eta[m, n] * Rsc)
G00 = Gein(0, 0); G12 = Gein(1, 2); G11 = Gein(1, 1)
ok00 = sp.simplify(G00 - 2 * lap(Pss)) == 0
ok12 = sp.simplify(G12 - sp.diff(Phs - Pss, X, Y)) == 0 or sp.simplify(G12 + sp.diff(Phs - Pss, X, Y)) == 0
P(f"    linearised Einstein tensor, static metric -(1 + 2 Phi) dt^2 + (1 - 2 Psi) dx^2:  G_00 = {G00};  G_xy = {G12}")
P("    T_ij = 0 for the answer (static, pressureless, as for the matter it answers) => d_i d_j (Phi - Psi) = 0 off the diagonal for all "
  "i != j => Phi - Psi harmonic and decaying => Phi = Psi; the null deflection is (1/c^2) Int grad_perp (Phi + Psi) = (2/c^2) Int grad_perp Phi")
check("D4 gamma = 1: the linearised Einstein equations for a static source give G_00 = 2 lap Psi and G_ij (i != j) = d_i d_j (Phi - Psi); "
      "the answer is a static pressureless source, so Phi = Psi and lensing reads the dynamical mass (M_lens = M_dyn, the record's "
      "category II)", f"G_00 = 2 lap Psi: {ok00}; G_xy = +-d_x d_y (Phi - Psi): {ok12}", ok00 and ok12,
      reading="a relativistic completion (dynamics, c_T, PPN beyond gamma) is OPEN, as for every static law of this kind")

# ================================================================================================ D5
R.banner("D5  THE LINEAR WEB IS NEVER BEHIND THE VACUUM: the gate is closed at first order, for a derived reason")
Hs, rm = sp.symbols("H rho_m", positive=True)
fried = sp.Eq(Hs ** 2, HL ** 2 + 8 * sp.pi * Gs * rm / 3)
gap = sp.simplify(sp.solve(fried, Hs)[0] ** 2 - HL ** 2)
P(f"    Friedmann with matter and vacuum: H^2 - H_Lambda^2 = {gap} > 0 for rho_m > 0  =>  the background expands faster than the vacuum at every z")
thr_fac = math.inf if C.MUTATE else 1.0                          # MUTATE: the vacuum answers all matter
zz = np.concatenate([np.linspace(0, 5, 501), np.geomspace(5.01, 1100, 400)])
aa = 1 / (1 + zz)
EE = np.sqrt((1 - C.OML_FP0) / aa ** 3 + C.OML_FP0)
fz = np.array([C.growth_f(a, 1 - C.OML_FP0, C.OML_FP0) for a in aa])
ratio = math.sqrt(C.OML_FP0) / EE                                # H_Lambda / H(z)
d_th = np.where(np.isinf(thr_fac), -np.inf, 3 * (1 - thr_fac * ratio) / fz)
imin = int(np.argmin(d_th))
P(f"    delta_th(z) = 3 (1 - H_Lambda/H)/f: z = 0: {d_th[0]:.3f}; 0.5: {np.interp(0.5, zz, d_th):.3f}; 1: {np.interp(1, zz, d_th):.3f}; "
  f"2: {np.interp(2, zz, d_th):.3f}; 10: {np.interp(10, zz, d_th):.3f}; 1100: {d_th[-1]:.3f};  min {d_th[imin]:.3f} at z = {zz[imin]:.2f}")
d5 = check("D5 [H2, load-bearing; MUTATE must fail] THE GATE IS CLOSED ON THE LINEAR WEB: the matter's local expansion theta/3 = H(1 - f "
           "delta/3) falls below the vacuum's rate only for delta > delta_th(z) = 3(1 - H_Lambda/H)/f, and min over 0 <= z <= 1100 of "
           "delta_th >= 0.9 -- so at first order in delta the gate indicator is identically zero and the linear equations are GR + the dark "
           "field: XR26's primary CMB and linear lensing are LCDM's exactly, with no tuned constant (H_Lambda is the vacuum's own rate)",
           f"min delta_th = {d_th[imin]:.3f} at z = {zz[imin]:.2f}; H^2 - H_Lambda^2 = {gap}", d_th[imin] >= 0.9,
           reading="the separation is derived: H > H_Lambda is Friedmann's equation with any matter at all; the gate opens only in "
                   "regions with delta_lin ~ 1-2, i.e. collapsing ones")
R.num("D5", dict(delta_th_z0=float(d_th[0]), delta_th_min=float(d_th[imin]), z_min=float(zz[imin]),
                 delta_th={str(z0): float(np.interp(z0, zz, d_th)) for z0 in (0, 0.25, 0.5, 1, 2, 5, 10, 100, 1100)}))


def tophat_open(delta_lin_obs, z_obs):
    """a top-hat of linear overdensity delta_lin_obs (extrapolated to z_obs): True if its theta/3 has dropped below H_Lambda by z_obs,
    and whether it has turned around (units H0 = 1, FP1 E / KiDS cosmology)."""
    om, ol = C.OM_K, C.OL_K
    ai, ao = 1e-3, 1 / (1 + z_obs)
    di = delta_lin_obs * C.growth_D(ai) / C.growth_D(ao)
    y0 = [ai * (1 - di / 3), float(C.E_of_a(ai)) * ai * (1 - di / 3) * (1 - di / 3)]
    def rhs(la, s):
        a = math.exp(la); E = math.sqrt(om / a ** 3 + ol); r, v = s
        return [v / E, (-(om / 2) / max(r, 1e-9) ** 2 + ol * r) / E]
    ts = np.linspace(math.log(ai), math.log(ao), 400)
    so = solve_ivp(rhs, (ts[0], ts[-1]), y0, t_eval=ts, rtol=1e-9, atol=1e-12)
    hsh = so.y[1] / so.y[0]
    return bool(np.min(hsh) < math.sqrt(ol)), bool(np.min(so.y[1]) <= 0)


rows5 = {}
for z0 in (0.0, 0.25, 0.5, 1.0, 2.0):
    d_open = brentq(lambda d: (0.5 if tophat_open(d, z0)[0] else -0.5), 0.2, 1.6, xtol=1e-4)
    d_ta = brentq(lambda d: (0.5 if tophat_open(d, z0)[1] else -0.5), 0.5, 1.6, xtol=1e-4)
    rows5[str(z0)] = (d_open, d_ta)
    P(f"    top-hat at z = {z0}: the gate opens at delta_lin = {d_open:.3f}; turnaround at delta_lin = {d_ta:.3f}")
check("D5b (H4, reported) the top-hat opens the gate (theta/3 = H_Lambda) at a linear overdensity below turnaround's at z = 0 and close to "
      "it at z >= 1: the gated regions are the collapsing ones and their infall zones",
      "; ".join(f"z {k}: open {v[0]:.3f} / ta {v[1]:.3f}" for k, v in rows5.items()),
      rows5["0.0"][0] < rows5["0.0"][1] and rows5["2.0"][1] - rows5["2.0"][0] < rows5["0.0"][1] - rows5["0.0"][0], load_bearing=False)
R.num("D5b", rows5)

# ================================================================================================ D6
R.banner("D6  COMPENSATION: each held-back region carries zero net phantom mass (Gauss)")
r_, rg, Mb, nu_r = sp.symbols("r r_g M_b nu_g", positive=True)
nuF = sp.Function("nu")
# 4 pi r^2 rho_ph = M_b d/dr[ Theta(r_g - r) (nu(r) - 1) ]  (Poisson on the gated answer g_ph = -Theta (nu - 1) G M_b / r^2 rhat)
dens = sp.diff(sp.Heaviside(rg - r_) * (nuF(r_) - 1), r_)
shell_part = sum(t for t in sp.Add.make_args(sp.expand(dens)) if t.has(sp.DiracDelta))
surface = sp.simplify(Mb * sp.integrate(shell_part, (r_, 0, sp.oo)))          # the negative surface layer at r_g
# net phantom mass = M_b [Theta (nu - 1)] from r = 0 (nu(0) = 1: Newtonian at the centre) to infinity (Theta = 0)
net = sp.simplify(Mb * ((sp.Heaviside(rg - r_) * (nuF(r_) - 1)).subs(r_, 2 * rg * 10) - (nuF(0) - 1)).subs(nuF(0), 1))
nu_r = nuF(rg)
Rr, m_ = sp.symbols("R m", positive=True)
Sig_shell = m_ / (2 * sp.pi * rg * sp.sqrt(rg ** 2 - Rr ** 2))
M2_shell = m_ * (1 - sp.sqrt(1 - Rr ** 2 / rg ** 2))
dS_shell = sp.series(sp.simplify(M2_shell / (sp.pi * Rr ** 2) - Sig_shell), Rr, 0, 4).removeO()
P(f"    enclosed phantom M_b (nu - 1) Theta(r_g - r): jump at r_g = {surface}; net beyond r_g = {net}")
P(f"    a thin shell (mass m, radius r_g) seen at R < r_g: Delta Sigma = {sp.simplify(dS_shell)} + O(R^4)")
check("D6 COMPENSATION IS DERIVED: the answer vanishes on the region's boundary, so by Gauss the region's net phantom mass is zero -- a "
      "negative surface layer -M_b (nu(r_g) - 1) at r_g cancels the interior phantom; the far field is the baryons' (and the dark "
      "field's) alone, so phantoms add NO mass to the linear web; a thin shell's excess surface density at R << r_g starts at O(R^2/r_g^2)",
      f"jump {surface}; net {net}; shell Delta Sigma leading term {sp.simplify(dS_shell)}",
      sp.simplify(surface + Mb * (nu_r - 1)) == 0 and net == 0 and sp.simplify(dS_shell.subs(Rr, 0)) == 0,
      reading="compensation at a switch edge is in the record (L346 / L352's Gauss compensation of the MOND-sector switch); here it "
              "follows from the principle's region, not from a chosen threshold")

# ================================================================================================ D7
R.banner("D7  THE REGION'S OWN FREE FALL: a uniform external field is removed exactly, a tidal remainder survives")
e_ = sp.symbols("e_x e_y e_z", real=True)
gint = [sp.Function(f"g{i}")(X, Y, Zc) for i in range(3)]
g_lab = [gint[i] + e_[i] for i in range(3)]
g_ff = [sp.simplify(g_lab[i] - e_[i]) for i in range(3)]      # the region falls with e: its frame subtracts e
Me, D_ = sp.symbols("M_e D", positive=True)
gx_ext = -G_ * Me * (X - D_) / ((X - D_) ** 2 + Y ** 2 + Zc ** 2) ** sp.Rational(3, 2)
tidal = sp.series(sp.simplify(gx_ext - gx_ext.subs({X: 0, Y: 0, Zc: 0})).subs({Y: 0, Zc: 0}), X, 0, 2).removeO()
P(f"    in the region's frame: g = {g_ff[0]}, ...;  an external point mass M_e at distance D leaves the tidal remainder {sp.simplify(tidal)} "
  "(order x/D of its field)")
check("D7 THE FREE-FALL FRAME: the principle reads the field of the region in the region's own free fall, so a uniform external field "
      "(the web's bulk flow, FP1 E5: 95% of the linear rms is bulk flow on > 60 Mpc) drops out exactly; an external source leaves only its "
      "tidal field, O(r/D) of its pull -- this is the environmental split FP1 E5 asked for (the LG's members see each other; an isolated "
      "lens sees only tides)", f"frame field {g_ff}; tidal remainder {sp.simplify(tidal)}",
      all(sp.simplify(g_ff[i] - gint[i]) == 0 for i in range(3)) and sp.simplify(tidal - 2 * G_ * Me * X / D_ ** 3) == 0)

# ================================================================================================ D8
R.banner("D8  THE COHERENCE LENGTH: the heat kernel, and the vacuum state's Airy length at a0 (the tie)")
k_, l1, l2 = sp.symbols("k ell_1 ell_2", positive=True)
semi = sp.simplify(sp.exp(-k_ ** 2 * l1 ** 2 / 2) * sp.exp(-k_ ** 2 * l2 ** 2 / 2) - sp.exp(-k_ ** 2 * (l1 ** 2 + l2 ** 2) / 2))
hb, mm, xi_, lA = sp.symbols("hbar m xi ell_A", positive=True)
psiF = sp.Function("chi")
schr = -(hb ** 2 / (2 * mm)) * sp.diff(psiF(xi_), xi_, 2) / lA ** 2 + mm * a0s * lA * xi_ * psiF(xi_)
airy_scale = sp.solve(sp.Eq(hb ** 2 / (2 * mm * lA ** 2), mm * a0s * lA), lA)[0]
P(f"    Gaussian coarse-grainings compose: residual {semi};  Schroedinger in the linear potential m a0 x is scale-free when "
  f"hbar^2/(2 m l^2) = m a0 l  =>  l_A = {airy_scale}")
m_eV = {"1.9e-19": 1.9e-19, "5.2e-19": 5.2e-19}
lA_num, lF17 = {}, {}
for mk, mv in m_eV.items():
    mkg = mv * C.EV / C.C_SI ** 2
    for f in C.FOOTS:
        lA_num[f"{mk}|{f}"] = (C.HBAR ** 2 / (2 * mkg ** 2 * C.A0[f])) ** (1 / 3) / C.PC
        lF17[f"{mk}|{f}"] = ((C.HBAR / mkg) ** 2 / C.A0[f]) ** (1 / 3) / C.PC
xi_one = C.HBAR * C.C_SI / (2e-22 * C.EV) / C.PC
P("    l_A = (hbar^2/(2 m^2 a0))^(1/3) [pc]: " + "; ".join(f"m = {k.split('|')[0]} eV, {k.split('|')[1]}: {v:.3f}" for k, v in lA_num.items()))
P("    FP17 B2's convention ((hbar/m)^2/a0)^(1/3) = 2^(1/3) l_A [pc]: " + "; ".join(f"{k}: {v:.3f}" for k, v in lF17.items())
  + "  (FP17 committed: can 3.28, can 1.68, alt 3.08, alt 1.57)")
P(f"    ONE_NEW_THING's coincidence: hbar c/(2e-22 eV) = {xi_one:.4f} pc (its 'xi = 0.03 pc')")
f17 = json.load(open(os.path.join(C.CHAIN, "FP17_screening_without_xi_results.json")))["numbers"]
f17_ref = [3.28, 1.68, 3.08, 1.57]
f17_now = [lF17["1.9e-19|canonical"], lF17["5.2e-19|canonical"], lF17["1.9e-19|alt"], lF17["5.2e-19|alt"]]
dev8 = max(abs(a / b - 1) for a, b in zip(f17_now, f17_ref))
check("D8 CONTROL + DERIVATION: coarse-graining that composes is the heat kernel (Gaussians compose exactly); the vacuum state's Airy length "
      "at a0 is l_A = (hbar^2/(2 m^2 a0))^(1/3); FP17 B2's committed lengths (its convention, 2^(1/3) l_A) are reproduced to their printed "
      "digits; ONE_NEW_THING's 2e-22 eV corresponds to 0.032 pc",
      f"semigroup residual {semi}; l_A = {airy_scale}; FP17 max rel dev {dev8:.1e} (printed to 3 digits); hbar c/(2e-22 eV) = {xi_one:.4f} pc",
      semi == 0 and sp.simplify(airy_scale ** 3 - hb ** 2 / (2 * mm ** 2 * a0s)) == 0 and dev8 < 4e-3 and abs(xi_one - 0.032) < 0.001)
R.num("D8", dict(l_A_pc=lA_num, l_FP17conv_pc=lF17, xi_one_new_thing_pc=xi_one))

# ================================================================================================ D9
R.banner("D9  FP17's THEOREM, AND WHICH LENGTH THE PRINCIPLE SUPPLIES")
GMs, rr9, a09, c9, L9 = sp.symbols("GM r a0 c Lambda", positive=True)
dimm = sp.Matrix([[3, 1, 1, 1, -2], [-2, 0, -2, -1, 0]])     # rows L, T; columns GM, r, a0, c, Lambda
rank9 = dimm.rank(); ns9 = dimm.nullspace()
P(f"    dimension matrix of (GM, r, a0, c, Lambda): rank {rank9}, {len(ns9)} dimensionless groups (FP17 M2: y, C, Lambda c^4/a0^2)")
check("D9 CONTROL (FP17 M2): (GM, r, a0, c, Lambda) have rank 2, hence 3 groups (y, C = GM/(r c^2), Lambda c^4/a0^2 = 8 pi/kappa^2): at fixed "
      "y only C ~ M^(1/2) tells the Sun from a galaxy, so the Solar System needs a mass or a length that (a0, Lambda, G, c) do not supply; "
      "the principle's l* (the vacuum state's Airy length) is that length -- TIED to the dark field's mass, not new",
      f"rank {rank9}; groups {len(ns9)}; FP17 committed rank/span: {f17.get('M2', {}).get('rank_span', 'see FP17 M2')}",
      rank9 == 2 and len(ns9) == 3)

# ================================================================================================ D10
R.banner("D10  THE CONSTANT COUNT")
count = [("kappa", "FITTED", "a0 = kappa c sqrt(G rho_Lambda), kappa = 1/2 (Z = 5.7888); underivable (the record)"),
         ("theta_* = 3 H_Lambda", "DERIVED", "the gate threshold is the vacuum's own expansion rate (D5); no new number"),
         ("nu(y)", "DERIVED", "Bose occupation at the ratio of free-fall times (D2) = nu_RAR"),
         ("compensation", "DERIVED", "Gauss on the region (D6)"),
         ("EFE rule", "DERIVED", "the region's free fall (D7): uniform external fields drop out, tides remain"),
         ("gamma", "DERIVED", "= 1 (D4)"),
         ("l*", "TIED", "l_A = (hbar^2/(2 m^2 a0))^(1/3): 1.2-2.6 pc at the dark field's mass floor 1.9-5.2e-19 eV (D8)"),
         ("m (dark field)", "DECLARED (dark sector)", "floor 1.9-5.2e-19 eV (FP10); l* shares it"),
         ("dark amount", "DECLARED (dark sector)", "Omega_c h^2 ~ 0.12 (CMB); required in clusters; must not sit in galaxies' gated regions")]
for k_, s_, t_ in count:
    R.ledger(k_, s_, t_)
check("D10 (reported) THE COUNT: fitted 1 (kappa); declared 0 new in the gravity sector (the dark sector's m and amount are its own); tied 1 "
      "(l* to m and a0); derived 5 (the threshold, nu, compensation, the EFE rule, gamma = 1)", "1 / 0 / 1 / 5", True, load_bearing=False)
R.num("D10", dict(fitted=1, declared_new=0, tied=1, derived=5, table=count))
sys.exit(R.finish())
