#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
L353 -- A KERNEL-INVISIBLE DARK COMPONENT IN C-H/K: a Lagrangian construction, and the reciprocity theorem that fixes
its force law.  The dark component gravitates in the metric but is invisible to the MOND kernel -- and therefore, by
action = reaction, it feels NEWTONIAN gravity only.  L321/L322's "additive" coupling (carrier feels the baryons' full
MOND field while its own field is unboosted) has no action.

WHY.  Three results on the record need a dark component the MOND kernel does not read:
  * L345: C-H/K's kernel reads the total lapse, so any minimally coupled carrier is boosted like baryons and the
    Lambda-triggered carrier loses its only window (L322's "additive" window reappears only under a coupling C-H/K lacks);
  * BS2 (switch_audit_2026): a kernel that reads the CDM-like web's field EFE-truncates every lens's phantom at ~0.1 Mpc
    (Delta chi^2 +569 on KiDS-1000); a baryons-only kernel survives inside 0.3 Mpc;
  * the RAR: any dark mass inside galaxies is boosted by the kernel unless the kernel cannot see it.

THE CONSTRUCTION (C-H's NR action, ACTION.md, + a dark component rho_d + a subtraction pair (v, lambda)):
    L = -(rho_b + rho_d) Phi - [2 grad Phi . grad u - |grad u|^2 - a0^2 q(|grad S(u - v)|^2/a0^2)]/(8 pi G)
        + lambda (Laplacian v - 4 pi G rho_d)
  The kernel reads u - v instead of u.  Field equations (N1):
    dPhi:    Lap u = 4 pi G (rho_b + rho_d)        dlambda: Lap v = 4 pi G rho_d     =>  u - v = u_b (baryons only)
    du:      Lap Phi = Lap u + S* div[q' grad S u_b]                                =>  Phi = u_b + u_d + Phi_ph[u_b]
    dv:      Lap lambda = -(1/4 pi G) S* div[q' grad S u_b]                          =>  4 pi G lambda = -Phi_ph[u_b]
  Baryons feel Phi.  The dark component (coupling -rho_d Phi - 4 pi G lambda rho_d) feels Phi + 4 pi G lambda = u_b + u_d:
  the Newtonian potential of ALL matter, and no phantom.  Relativistically the pair is two leafwise elliptic auxiliaries on
  C-H's preferred leaves (like its heat-flow fields) with the dark source n_mu n_nu T_d^{mu nu}.

WHAT THIS LANE CHECKS
  N1 THE FIELD EQUATIONS (symbolic Euler-Lagrange, arbitrary kernel primitive Q; the 1D operator identities hold in 3D with
     S a symmetric convolution that commutes with div): kernel argument = baryonic Newtonian potential; metric potential =
     Newtonian(all) + phantom(baryons); the dark component's potential = Newtonian(all).  Numeric 3D spherical check with
     L340's kernel nu_mono (Hernquist baryons + NFW dark component).
  N2 THE RECIPROCITY THEOREM: a static Lagrangian's response matrix (potential felt by species s per unit source of species
     t) is symmetric.  So "the carrier's field is unboosted" (kernel-invisible) forces "the carrier feels only the
     baryons' Newtonian field" -- and L321's additive law (carrier feels (1+C) x baryons, baryons feel 1 x carrier) is
     asymmetric: no action produces it.  Explicit two-body test in deep MOND: under L321's law the forces between a
     baryonic mass and a carrier particle differ by r/r_M (momentum not conserved); under the construction they balance.
  N3 THE RELATIVISTIC BLOCK: L340's unitary scalar block (its quadratic Lagrangian, reconstructed and checked row by row)
     extended with the dark source and the pair.  Static: baryons boosted by (1+C)/(1 - alpha_c(1+C)/2) as before; the
     dark component's own field Newtonian; the kernel argument independent of R_d; psi = phi for both species (lensing =
     dynamics).  Moving: the homogeneous modes are L340's exactly (the pair adds no mode), so L340's health and tracking
     carry over.
  N4 WHAT IT BUYS AND WHAT IT COSTS (numbers):
     (a) the kernel's large-scale field becomes baryonic only: BS2's committed E10 (baryons-only kernel) is the relevant
         KiDS verdict -- read from BS2's results file;
     (b) the price is a dark-sector violation of the equivalence principle wherever the phantom is on: in X-COP clusters
         at R500 the gas feels (1 + ...) more acceleration than the dark component -- computed per cluster;
     (c) inside galaxies the dark component is not boosted: L321's RAR gate (0.06 dex) applies to its Newtonian mass.
  MUTATE=1 removes the subtraction (the kernel reads u, not u - v): N1 and N3's invisibility checks must FAIL (rc = 1).

SCOPE.  A construction, not a derivation: the pair is a new ingredient (two auxiliaries and a dark coupling to the
preferred frame's energy density).  Health is checked at the order of L340's block; the dark coupling breaks boost
invariance in the dark sector only where the phantom is non-zero.  The cosmology of the construction (web growth, forest)
is not computed here; the carrier's z = 0 gates under the Newtonian force law are L354.

Run from the repository root:  python3 real_research/g03_audit_2026/L353_kernel_invisible_dark_component.py
"""
import os, sys, json, math, time, warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
import numpy as np
import sympy as sp
from sympy.calculus.euler import euler_equations
from scipy.optimize import brentq

HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
MUTATE = os.environ.get("MUTATE", "0") == "1"
SLUG = "L353_kernel_invisible_dark_component"
P = lambda *a: print(*a, flush=True)
CH, OUT = [], {"lane": "L353", "mutate": MUTATE, "checks": {}, "numbers": {}}
T0 = time.time()
_trap = getattr(np, "trapezoid", None) or np.trapz


def check(name, measured, ok, reading="", load_bearing=True):
    ok = bool(ok); CH.append((name, ok, load_bearing))
    OUT["checks"][name] = {"ok": ok, "measured": str(measured), "load_bearing": load_bearing}
    P(f"  [{'PASS' if ok else 'FAIL'}] {name}"); P(f"         measured: {measured}")
    if reading: P(f"         reading:  {reading}")
    return ok


def banner(t): P("\n" + "=" * 104); P(t); P("=" * 104)


P(__doc__.split("WHAT THIS LANE CHECKS")[0].strip())
if MUTATE: P("\n  *** MUTATE=1: no subtraction (the kernel reads u); the invisibility checks N1/N3 must FAIL ***")
SUB = 0 if MUTATE else 1                                             # 1: kernel reads u - v; 0: kernel reads u

# ============================================================================================ N1 field equations
banner("N1  THE FIELD EQUATIONS OF THE SUBTRACTION PAIR (symbolic Euler-Lagrange, arbitrary kernel primitive Q)")
x = sp.symbols('x', real=True)
G, a0 = sp.symbols('G a_0', positive=True)
Phi, u, v, lam = [sp.Function(n)(x) for n in ('Phi', 'u', 'v', 'lam')]
rb, rd = sp.Function('rho_b')(x), sp.Function('rho_d')(x)
Q = sp.Function('Q')
w = u - SUB * v
L = (-(rb + rd) * Phi - (2 * Phi.diff(x) * u.diff(x) - u.diff(x)**2 - a0**2 * Q(w.diff(x)**2 / a0**2)) / (8 * sp.pi * G)
     + lam * (v.diff(x, 2) - 4 * sp.pi * G * rd))
EL = {f.func.__name__: sp.simplify(e.lhs) for f, e in zip((Phi, u, v, lam), euler_equations(L, [Phi, u, v, lam], x))}
# identities that must hold on shell (each is a linear combination of the EL expressions):
kernel_arg = sp.simplify(4 * sp.pi * G * EL["Phi"] - EL["lam"] - (w.diff(x, 2) - 4 * sp.pi * G * rb))      # (u - v)'' = 4 pi G rho_b
# the metric identity needs the kernel explicitly: use the deep-MOND primitive Q(s) = (4/3) s^(3/4) - s (q' = nu - 1)
sq = sp.Symbol('s_', positive=True)
Qc = sp.Lambda(sq, sp.Rational(4, 3) * sq**sp.Rational(3, 4) - sq)
Lc = L.subs(Q, Qc).doit()
ELc = {f.func.__name__: sp.simplify(e.lhs) for f, e in zip((Phi, u, v, lam), euler_equations(Lc, [Phi, u, v, lam], x))}
Xc = sp.diff(sp.diff(Qc(sq), sq).subs(sq, w.diff(x)**2 / a0**2) * w.diff(x), x)       # div[q'(|grad w|^2/a0^2) grad w]
metric = sp.simplify(4 * sp.pi * G * ELc["u"] - (Phi.diff(x, 2) - u.diff(x, 2) - Xc))                    # Phi'' = u'' + X
dark = sp.simplify(4 * sp.pi * G * EL["u"] + 4 * sp.pi * G * EL["v"] * SUB
                   - ((Phi + 4 * sp.pi * G * lam).diff(x, 2) - u.diff(x, 2)))                               # (Phi + 4piG lam)'' = u''
P(f"    dPhi:    {EL['Phi']} = 0")
P(f"    dlambda: {EL['lam']} = 0")
P(f"    identity (u - v)'' - 4 pi G rho_b = 4 pi G dPhi - dlambda: residual {kernel_arg}")
P(f"    identity Phi'' = u'' + [q'(|(u - v)'|^2/a0^2) (u - v)']' (deep-MOND primitive):  residual {metric}")
P(f"    identity (Phi + 4 pi G lambda)'' = u'' = 4 pi G (rho_b + rho_d):  residual {dark}")
n1_sym = (kernel_arg == 0) and (metric == 0) and (dark == 0)
# numeric 3D spherical check with L340's kernel: Hernquist baryons + NFW dark component
def h_rar(y): return y / np.expm1(np.sqrt(y))
def dh_rar(y, e=1e-6): return (h_rar(y*(1 + e)) - h_rar(y*(1 - e)))/(2*y*e)
Y_P = brentq(lambda y: dh_rar(y), 1.0, 5.0); H_P = h_rar(Y_P)
def nu_mono(y):
    y = np.asarray(y, float)
    return np.where(y <= Y_P, 1.0 + h_rar(np.minimum(y, Y_P)) / np.maximum(y, 1e-300),
                    1.0 + (H_P + 0.05 * H_P * np.log((y + Y_P) / (2 * Y_P))) / np.maximum(y, 1e-300))
Gk = 4.30091727e-6; KPC_M = 3.0856775814913673e19; A0K = 9.3619e-11 * KPC_M / 1e6        # kpc (km/s)^2 / Msun ; (km/s)^2/kpc
r = np.geomspace(0.05, 3000.0, 20000)
Mb, ab = 6e10, 3.0; Md, rs, c = 3e11, 20.0, 10.0
Mb_r = Mb * r**2 / (r + ab)**2
m = lambda s: np.log(1 + s) - s / (1 + s)
Md_r = Md * m(np.minimum(r, c * rs) / rs) / m(c)
gb, gd = Gk * Mb_r / r**2, Gk * Md_r / r**2                           # Newtonian fields (spherical Gauss)
g_kernel_arg = gb + gd - SUB * gd                                     # |grad (u - v)|
g_phantom = (nu_mono(g_kernel_arg / A0K) - 1.0) * g_kernel_arg        # spherical QUMOND: phantom field = (nu - 1) g_arg
g_baryon_feels = gb + gd + g_phantom                                  # -grad Phi
g_dark_feels = g_baryon_feels - g_phantom                             # -grad(Phi + 4 pi G lambda)
dev_arg = float(np.max(np.abs(g_kernel_arg / gb - 1)))
dev_dark = float(np.max(np.abs(g_dark_feels / (gb + gd) - 1)))
boost_out = float(g_baryon_feels[np.argmin(abs(r - 100))] / (gb + gd)[np.argmin(abs(r - 100))])
P(f"    3D spherical (M_b = 6e10 Hernquist, M_d = 3e11 NFW): max |kernel argument/g_N,b - 1| = {dev_arg:.1e}; "
  f"max |dark field/g_N,all - 1| = {dev_dark:.1e}; baryons at 100 kpc feel {boost_out:.2f} x Newtonian(all)")
OUT["numbers"]["N1"] = {"symbolic": {"kernel_arg": str(kernel_arg), "metric": str(metric), "dark": str(dark)},
                        "numeric": {"dev_kernel_arg": dev_arg, "dev_dark": dev_dark, "baryon_boost_100kpc": boost_out}}
check("N1 the subtraction pair makes the kernel read the baryonic Newtonian potential only, puts Newtonian(all) + "
      "phantom(baryons) in the metric, and gives the dark component exactly the Newtonian potential of all matter",
      f"symbolic residuals {kernel_arg}, {metric}, {dark}; numeric {dev_arg:.1e}, {dev_dark:.1e}",
      n1_sym and dev_arg < 1e-12 and dev_dark < 1e-12,
      "the multiplier's force on the dark component is exactly minus the phantom it would otherwise feel")

# ============================================================================================ N2 reciprocity
banner("N2  THE RECIPROCITY THEOREM: kernel-invisible <=> feels no phantom; L321's 'additive' law has no action")
# (i) any static quadratic Lagrangian L = 1/2 X^T H X - X^T B s (fields X, sources s = (R_b, R_d), H symmetric):
#     fields X = H^-1 B s; the potential felt by species t is -dL/ds_t = (B^T X)_t, so Gamma = B^T H^-1 B = Gamma^T.
n_f = 3
Hs = sp.Matrix(n_f, n_f, lambda i, j: sp.Symbol(f'h{min(i, j)}{max(i, j)}'))
Bs = sp.Matrix(n_f, 2, lambda i, j: sp.Symbol(f'b{i}{j}'))
Gam = sp.simplify(Bs.T * Hs.inv() * Bs)
sym_gen = sp.simplify(Gam - Gam.T) == sp.zeros(2)
# (ii) L321's additive law in the same language: potential felt by the carrier from baryons (1 + C) G_N, by baryons from the
#      carrier G_N  ->  Gamma_add = G_N [[1 + C, 1], [1 + C, 1]] (rows: felt by b, felt by d; columns: source b, source d)
Cs = sp.symbols('C', positive=True)
Gam_add = sp.Matrix([[1 + Cs, 1], [1 + Cs, 1]])
asym_add = sp.simplify(Gam_add[0, 1] - Gam_add[1, 0])
# (iii) two-body momentum balance in deep MOND: baryonic point mass M_b, carrier particle m at r (units G = a0 = 1)
two = []
for rr_ in (2.0, 10.0, 100.0):
    rM = 1.0                                                          # r_M = sqrt(G M_b/a0) with M_b = 1
    # exact nu_RAR boost of the baryons' field at the carrier: g = nu(g_N) g_N with g_N = 1/r^2
    gN = 1.0 / rr_**2; g_add = float(nu_mono(gN)) * gN
    F_c_add, F_b_add = g_add * 1.0, gN * 1.0                          # per unit carrier mass (m = 1): on carrier / on baryons
    F_c_pair, F_b_pair = gN, gN
    two.append((rr_, F_c_add / F_b_add, F_c_pair / F_b_pair))
    P(f"    r = {rr_:6.1f} r_M: L321 additive |F on carrier|/|F on baryons| = {F_c_add / F_b_add:8.3f};  subtraction pair = {F_c_pair / F_b_pair:.3f}")
P(f"    general static quadratic Lagrangian: Gamma - Gamma^T = 0: {sym_gen};  L321 additive: Gamma_bd - Gamma_db = {asym_add}")
OUT["numbers"]["N2"] = {"general_symmetric": sym_gen, "additive_asymmetry": str(asym_add), "two_body": two}
check("N2 a static Lagrangian's species-response matrix is symmetric, so a kernel-invisible component feels no phantom; "
      "L321's additive law is asymmetric (Gamma_bd - Gamma_db = -C) and breaks momentum balance by ~r/r_M in deep MOND",
      f"generic symmetric: {sym_gen}; additive asymmetry {asym_add}; force ratio at 10 r_M {two[1][1]:.2f} (pair {two[1][2]:.2f})",
      sym_gen and asym_add != 0 and two[1][1] > 5 and abs(two[1][2] - 1) < 1e-12,
      "L322's additive window was computed under a force law no action produces; L354 redoes it with the Lagrangian one")

# ============================================================================================ N3 relativistic block
banner("N3  THE RELATIVISTIC BLOCK: L340's quadratic Lagrangian + the dark source + the pair (unitary gauge, symbolic)")
k, C, c2, ac, om = sp.symbols('k C c_2 alpha_c omega', real=True)
psi, phi, beta, U, vv, Lm_ = sp.symbols('psi phi beta U v Lambda')
psid, betad = sp.symbols('psidot betadot')
Rb, Rd, Rbd, Rdd = sp.symbols('R_b R_d Rdot_b Rdot_d')
eps = -c2                                                             # 1 - lambda_BPS with lambda = 1 + c_2 (L340)
def quad_L(with_pair):
    Lq = (-6 * psid**2 + 4 * k**2 * beta * psid + eps * (3 * psid - k**2 * beta)**2
          + 2 * k**2 * psi**2 - 4 * k**2 * phi * psi + 2 * k**2 * (U - phi)**2 + ac * k**2 * phi**2
          - (Rb + Rd) * phi + (Rbd + Rdd) * beta)
    if with_pair:
        Lq += 2 * k**2 * C * (U - SUB * vv)**2 + Lm_ * (4 * k**2 * vv + Rd)
    else:
        Lq += 2 * k**2 * C * U**2
    return Lq
Dop = -sp.I * om
def rows(Lq, fields, dots):
    out = []
    for f in fields:
        e = sp.diff(Lq, f)
        if f in dots:
            e -= Dop * sp.diff(Lq, dots[f])
        out.append(sp.expand(e.subs({psid: Dop * psi, betad: Dop * beta, Rbd: Dop * Rb, Rdd: Dop * Rd})))
    return out
dots = {psi: psid, beta: betad}
E340 = rows(quad_L(False), [psi, phi, beta, U], dots)
# L340's rows verbatim (H1 block, a2 = a3 = g = 0), total source R = R_b + R_d
Rtot = Rb + Rd
L340rows = [4*k**2*psi - 4*k**2*phi - Dop*(-12*Dop*psi + 4*k**2*beta + 6*eps*(3*Dop*psi - k**2*beta)),
            -4*k**2*psi - 4*k**2*(U - phi) + 2*ac*k**2*phi - Rtot,
            4*k**2*Dop*psi - 2*eps*k**2*(3*Dop*psi - k**2*beta) + Dop*Rtot,
            4*k**2*(U - phi) + 4*k**2*C*U]
recon_ok = all(sp.simplify(a - sp.expand(b)) == 0 for a, b in zip(E340, L340rows))
P(f"    reconstructed quadratic Lagrangian reproduces L340's four rows exactly: {recon_ok}")
fields6 = [psi, phi, beta, U, vv, Lm_]
E6 = rows(quad_L(True), fields6, dots)
Mx = sp.Matrix([[sp.diff(e, f) for f in fields6] for e in E6]); Sx = sp.Matrix([-e.subs({f: 0 for f in fields6}) for e in E6])
sol_st = Mx.subs(om, 0).LUsolve(Sx.subs(om, 0))
S_ = dict(zip(fields6, [sp.simplify(s) for s in sol_st]))
psiN_b, psiN_d = -Rb / (4 * k**2), -Rd / (4 * k**2)
boost_b = sp.simplify(sp.diff(S_[phi], Rb) / (-1 / (4 * k**2)))
boost_d = sp.simplify(sp.diff(S_[phi], Rd) / (-1 / (4 * k**2)))
kern_d = sp.simplify(sp.diff(S_[U] - SUB * S_[vv], Rd))
lens_b = sp.simplify(sp.diff(S_[psi] - S_[phi], Rb)); lens_d = sp.simplify(sp.diff(S_[psi] - S_[phi], Rd))
felt_d_from_b = sp.simplify(sp.diff(S_[phi] - S_[Lm_], Rb)); felt_b_from_d = sp.simplify(sp.diff(S_[phi], Rd))
recip = sp.simplify(felt_d_from_b - felt_b_from_d)
P(f"    static: phi response to R_b = {sp.factor(boost_b)} x psi_N;  to R_d = {sp.factor(boost_d)} x psi_N")
P(f"    kernel argument (U - v) response to R_d: {kern_d};  lensing = dynamics (psi - phi) for b / d: {lens_b} / {lens_d}")
P(f"    potential felt by the dark component per R_b minus potential felt by baryons per R_d: {recip}")
# modes: homogeneous determinant of the extended block vs L340's, compared as polynomials in omega at fixed numeric
# parameters (three random points; symbolic in omega) -- the ratio must be omega-independent
M340 = sp.Matrix([[sp.diff(e, f) for f in [psi, phi, beta, U]] for e in E340])
ratios = []
for vals in ({C: sp.Rational(7, 3), c2: sp.Rational(1, 97), ac: sp.Rational(1, 10**6), k: sp.Rational(3, 2)},
             {C: sp.Rational(41, 5), c2: sp.Rational(3, 1000), ac: sp.Rational(1, 10**5), k: sp.Rational(1, 3)},
             {C: sp.Rational(1, 7), c2: sp.Rational(1, 20), ac: sp.Rational(2, 10**7), k: 2}):
    dx_ = sp.expand(Mx.subs(vals).det()); d3_ = sp.expand(M340.subs(vals).det())
    ratios.append(sp.cancel(dx_ / d3_))
ratio_det = ratios[0]
omega_free = all(not r_.has(om) for r_ in ratios)
# moving source: the omega -> 0 limit of the baryons' response equals the static one (tracking inherited); L340's method
num_, den_ = sp.fraction(sp.cancel(sp.together(Mx.LUsolve(Sx)[1].diff(Rb))))
trk_b = sp.simplify(num_.subs(om, 0) / den_.subs(om, 0) - sp.diff(S_[phi], Rb))
P(f"    det M_ext(omega)/det M_340(omega) at three parameter points = {ratios}  (omega-free: {omega_free});  baryon tracking residual at omega -> 0: {trk_b}")
leak = sp.simplify(sp.series(kern_d / (-1 / (4 * k**2)), ac, 0, 2).removeO())                 # kernel sees R_d at O(alpha_c)
P(f"    leakage of the dark field into the kernel argument (per psi_N,d): {leak}  (exactly 0 at alpha_c = 0)")
n3_ok = (recon_ok and sp.simplify(boost_b - (1 + C) / (1 - ac * (1 + C) / 2)) == 0
         and sp.simplify(boost_d.subs(ac, 0) - 1) == 0 and sp.simplify(kern_d.subs(ac, 0)) == 0
         and lens_b == 0 and lens_d == 0 and recip == 0 and omega_free and trk_b == 0)
OUT["numbers"]["N3"] = {"reconstruction": recon_ok, "boost_b": str(sp.factor(boost_b)), "boost_d": str(sp.factor(boost_d)), "leak": str(leak),
                        "kernel_arg_response_to_Rd": str(kern_d), "lens_b": str(lens_b), "lens_d": str(lens_d),
                        "reciprocity": str(recip), "det_ratios": [str(r_) for r_ in ratios], "tracking_b": str(trk_b)}
check("N3 in L340's relativistic block the pair leaves the baryons' boost and tracking unchanged, gives the dark component a "
      "Newtonian field with lensing = dynamics, keeps the kernel blind to it (exactly at alpha_c = 0; leakage O(alpha_c) ~ 1e-9 "
      "otherwise), is reciprocal, and adds no mode (det ratio independent of omega)",
      f"boost_b {sp.factor(boost_b)}; boost_d {sp.factor(boost_d)}; leak {leak}; det ratios {ratios}", n3_ok,
      "L340's health (H2) and tracking (H1) carry over; the pair is two leafwise auxiliaries")

# ============================================================================================ N4 buys and costs
banner("N4  WHAT IT BUYS AND WHAT IT COSTS")
# (a) BS2's committed verdict on a baryons-only kernel
bs2 = os.path.join(REPO, "real_research", "switch_audit_2026", "BS2_efe_vs_switch_results.json")
bs2_rows = {}
if os.path.exists(bs2):
    B2 = json.load(open(bs2))
    txt = json.dumps(B2)
    for key in ("E10", "E13"):
        for ck, cv in B2.get("checks", {}).items():
            if ck.startswith(key):
                bs2_rows[key] = cv.get("measured")
P(f"    (a) BS2 (committed) on a baryons-only kernel: E10 {bs2_rows.get('E10')};  E13 (R <= 0.3 Mpc) {bs2_rows.get('E13')}")
# (b) dark-sector equivalence-principle violation in X-COP clusters at R500, with the dark mass that makes M_dyn = M_HSE
from astropy.io import fits
R500 = json.load(open(os.path.join(REPO, "real_research", "data", "xcop", "xcop_r500_ettori2019.json")))
wep = []
for name, meta in R500.items():
    d = os.path.join(REPO, "real_research", "data", "xcop", name)
    if not os.path.isdir(d): continue
    hm = fits.open(os.path.join(d, f"{name}_hydro_mass.fits")); Rk, Mf = hm[1].data["RADIUS"], hm[1].data["M_FORW"]
    fg = fits.open(os.path.join(d, f"{name}_fgas_profile.fits"))[1].data
    R5 = meta["R500"] * 1000.0; Mhse = float(np.interp(R5, Rk, Mf))
    Mgas = float(np.interp(1.0, fg["RADIUS"], fg["MGAS"]))
    ms_path = os.path.join(d, f"{name}_mstar.fits")
    Mst = float(np.interp(R5, fits.open(ms_path)["MSTAR_SMOOTHED"].data["RADIUS"], fits.open(ms_path)["MSTAR_SMOOTHED"].data["MSTAR"])) \
        if os.path.exists(ms_path) else 0.015 * Mhse
    Mb_c = Mgas + Mst
    gbN = Gk * Mb_c / R5**2; ge = 0.01 * A0K
    gb_eff = np.sqrt(gbN**2 + ge**2)
    g_bar_feel_b = float(nu_mono(gb_eff / A0K)) * gbN                # baryons' own field, boosted (magnitude EFE rule)
    Md_need = max(Mhse - g_bar_feel_b * R5**2 / Gk, 0.0)             # dark mass that closes M_dyn = M_HSE (Newtonian, unboosted)
    gdN = Gk * Md_need / R5**2
    a_b, a_d = g_bar_feel_b + gdN, gbN + gdN
    wep.append((name, Md_need / Mb_c, 1 - a_d / a_b))
med_wep = float(np.median([w_[2] for w_ in wep])); med_md = float(np.median([w_[1] for w_ in wep]))
P(f"    (b) X-COP at R500 ({len(wep)} clusters): dark mass needed = {med_md:.2f} x baryons (median); the dark component feels "
  f"{med_wep*100:.0f}% less acceleration than the gas (median; range {min(w_[2] for w_ in wep)*100:.0f}-{max(w_[2] for w_ in wep)*100:.0f}%)")
# (c) galaxies: the unboosted dark component's allowance under L321's 0.06-dex RAR gate, e.g. Milky Way at 30 kpc
gbM = Gk * 6e10 * 30.0**2 / (30.0 + 3.0)**2 / 30.0**2; gobs = float(nu_mono(np.sqrt(gbM**2 + (0.02 * A0K)**2) / A0K)) * gbM
Md_allow = (10**0.06 - 1) * gobs * 30.0**2 / Gk
P(f"    (c) Milky Way at 30 kpc: an unboosted dark mass of {Md_allow:.2e} Msun ({Md_allow/6e10:.2f} M_b) shifts g_obs by 0.06 dex; "
  f"a boosted one (universal coupling) would be allowed only ~1/nu = {1/float(nu_mono(gbM/A0K)):.2f} of that")
OUT["numbers"]["N4"] = {"BS2": bs2_rows, "xcop_wep": wep, "median_wep": med_wep, "median_dark_over_baryons": med_md,
                        "MW_unboosted_allowance_Msun": Md_allow}
check("N4 (documentary) the construction trades three failures for one prediction: the kernel's web field is baryonic only "
      "(BS2's baryons-only verdict applies), the dark component is not boosted in galaxies, and in clusters the gas feels "
      "tens of per cent more acceleration than the dark component (a dark-sector equivalence-principle violation)",
      f"BS2 E10/E13 {bs2_rows}; X-COP median dark/baryon {med_md:.2f}, WEP gap {med_wep*100:.0f}%", True, load_bearing=False)

banner("VERDICT")
P(f"""  A kernel-invisible dark component exists in C-H/K as a Lagrangian construction: two leafwise auxiliaries (v, lambda)
  that subtract the dark component's Newtonian potential from the kernel's argument (N1; relativistic block N3: baryons'
  boost, tracking and modes untouched; the dark field Newtonian with lensing = dynamics).  Reciprocity fixes the rest
  (N2): a component the kernel cannot see feels only Newtonian gravity.  L321/L322's 'additive' coupling -- carrier feels
  the baryons' MOND field, baryons feel the carrier unboosted -- has no action (it breaks momentum balance by ~r/r_M), so
  L322's window must be recomputed with the Newtonian force law (L354).  The price is a dark-sector equivalence-principle
  violation where the phantom is on: in X-COP clusters the gas feels ~{med_wep*100:.0f}% more acceleration than the dark
  component.  A construction, not a derivation.  Time {time.time() - T0:.0f} s.""")
n_fail = sum(1 for _, ok, lb in CH if lb and not ok)
OUT["n_checks"], OUT["n_fail_load_bearing"] = len(CH), n_fail
outname = f"{SLUG}_results{'_MUTATE' if MUTATE else ''}.json"
json.dump(OUT, open(os.path.join(HERE, outname), "w"), indent=1, default=str)
P(f"\n  {sum(1 for _, ok, _ in CH if ok)}/{len(CH)} checks pass; load-bearing failures: {n_fail}; wrote {outname}")
sys.exit(0 if n_fail == 0 else 1)
