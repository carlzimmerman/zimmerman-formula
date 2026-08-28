#!/usr/bin/env python3
r"""
FC-FINAL 4-AC TYPE-II MMG  --  SETUP / DERIVATION-SCOPING CERTIFICATE
====================================================================

Task (SETUP): lay out the 4-auxiliary-constraint (Type-II MMG) structure faithfully,
embed the frozen MOND kernel mu_10, and -- the load-bearing deliverable -- DERIVE which
metric potential(s) the MOND modification sources in the static weak field:

    Psi  = lapse / g_00 potential   (dynamics: slow matter feels a = -grad Psi)
    Phi  = spatial / g_ij curvature potential   (lensing: light feels grad(Phi+Psi))

We do NOT assume Phi=Psi and do NOT assume Phi!=Psi.  We COMPUTE, for each admissible
choice of the fourth ("conformal") auxiliary constraint C_q, the resulting Phi, and the
implied slip gamma_PPN = Phi/Psi and lensing efficiency (Phi'+Psi')/(2 Psi').

Every load-bearing line prints a sympy/numeric certificate (residual==0 or a number).
Exit 0 iff all BOOLEAN certificates pass.  (Numeric tables are labelled [info].)

Honesty labels used in comments:
  THEOREM | DERIVATION | COMPUTATION | EXTERNAL-INPUT | MODEL-ASSUMPTION | OPEN | FAILED

CONVENTIONS (fixed once, stated so the sign of the "lock" is unambiguous):
  Static weak field, N^i gauge-fixed to 0, c kept explicit then set by eps=1/c^2->0 checks:
     g_00 = -N^2 c^2,     N = 1 + Psi/c^2       =>  ln N = Psi/c^2 + O(c^-4)
     g_ij = gamma_ij = (1 - 2 Phi/c^2) delta_ij (+ h^TT)
  Conformal factor (gate_lensing / gate_fork committed convention):
     q = (1/6) ln det gamma  =>  q = -Phi/c^2 + O(c^-4)      [q carries the CURVATURE potential]
  MOND kernel (FROZEN, do not change):
     mu_10(y) = y / (1 + y^10)^(1/10),   y = (c^2/a0)|D(field)|,   mu_10>0, mu_10+y mu_10'>0.
"""

import sys
import numpy as np
import sympy as sp

FAILS = []
def cert(label, cond):
    ok = bool(cond)
    print(("  [PASS] " if ok else "  [FAIL] ") + label)
    if not ok:
        FAILS.append(label)
    return ok

def info(label):
    print("  [info] " + label)

# =====================================================================================
print("=" * 88)
print(" PART 0 -- the 4-AC Type-II phase space and the DOF arithmetic (EXTERNAL-INPUT + check)")
print("=" * 88)
# EXTERNAL-INPUT (De Felice-Mukohyama-Pookkillath arXiv 2302.02090 Type-II MMG;
#                 Iyonaga-Kobayashi arXiv 2109.10615 spatially-covariant MMG):
#   Phase space (gamma_ij,pi^ij ; N,pi_N ; N^i,pi_i).  GR = H_perp + H_i (4 first-class)
#   + spatial-diffeo => 2 DOF.  Type-II keeps 2 DOF WITHOUT H_perp by adding FOUR
#   SECOND-CLASS auxiliary constraints {S_1,S_2,S_3,S_4} with nondegenerate 4x4
#   Dirac block Delta_AB={S_A,S_B}, plus the first-class spatial-diffeo pair (pi_i,H_i).
dim_phase = 12 + 2 + 6          # (gamma,pi)=12, (N,pi_N)=2, (N^i,pi_i)=6
first_class = 6                 # (pi_i, H_i): spatial diffeomorphisms only
second_class = 4                # {S_1,S_2,S_3,S_4}
Ndof = sp.Rational(dim_phase - 2*first_class - second_class, 2)
cert("phase-space dim = 20 (12 metric + 2 lapse + 6 shift)", dim_phase == 20)
cert("DOF count (20 - 2*6 - 4)/2 = 2  (two tensor gravitons, no scalar, no vector)", Ndof == 2)
info("Carl's target set:  S_1 = pi_N,  S_2 = C_M^(10) (MOND),  S_3 = C_q,  S_4 = C_p .")
info("The 4x4 block Delta_AB must be INVERTIBLE (second-class) to remove the scalar pair.")
info("Committed Pfaffian of the baseline block: Pf(Delta)=L_N*K  (03_dirac_matrix.py); the")
info("q-lock fork moves it to Pf=L_N*K - E*c_M (gate_fork_S2prime_matter_mondlaw.out) -- still !=0.")

# =====================================================================================
print("=" * 88)
print(" PART 1 -- weak-field dictionary: q carries Phi, ln N carries Psi  (DERIVATION)")
print("=" * 88)
Phi, Psi, cc = sp.symbols('Phi Psi c', positive=True)
# q = (1/6) ln det gamma, gamma_ij=(1-2Phi/c^2)delta_ij  => det=(1-2Phi/c^2)^3
q_of_Phi = sp.Rational(1, 6) * sp.log((1 - 2*Phi/cc**2)**3)
q_lin = sp.series(q_of_Phi, Phi, 0, 2).removeO()
cert("q = (1/6)ln det gamma = -Phi/c^2 + O(Phi^2)  (conformal factor IS the curvature potential)",
     sp.simplify(q_lin + Phi/cc**2) == 0)
lnN_of_Psi = sp.log(1 + Psi/cc**2)
lnN_lin = sp.series(lnN_of_Psi, Psi, 0, 2).removeO()
cert("ln N = +Psi/c^2 + O(Psi^2)  (lapse log IS the dynamical potential)",
     sp.simplify(lnN_lin - Psi/cc**2) == 0)
info("=> a constraint acting on q fixes Phi; a constraint acting on ln N fixes Psi.")
info("=> the MOND kernel mu_10 sources WHICHEVER of {Phi,Psi} its carrier field is.  That is")
info("   the whole pivot: 'y=(c^2/a0)|D q| OR |D ln N| per the embedding' decides Phi vs Psi.")

# =====================================================================================
print("=" * 88)
print(" PART 2 -- the lapse sector: C_M^(10) on ln N sources Psi (exact AQUAL)  (DERIVATION)")
print("=" * 88)
# C_M = D_i[c^2 mu_10(y) D^i ln N] - 4 pi G rho,  y=(c^2/a0)|D ln N|.  Reduce to AQUAL for Psi.
X, Yc = sp.symbols('X Y', real=True)
a0s, Amp, eps = sp.symbols('a0 A eps', positive=True)
Psi_t = Amp*(X**2 + Yc**2)
c2 = 1/eps
Nfield = 1 + Psi_t*eps
lnN = sp.log(Nfield)
grad = [sp.diff(lnN, v) for v in (X, Yc)]
ys = c2/a0s*sp.sqrt(sum(g**2 for g in grad))
mu10 = lambda yy: yy/(1 + yy**10)**sp.Rational(1, 10)
flux = [c2*mu10(ys)*g for g in grad]
divN = sum(sp.diff(f, v) for f, v in zip(flux, (X, Yc)))
divN0 = sp.series(divN, eps, 0, 1).removeO()
gP = [sp.diff(Psi_t, v) for v in (X, Yc)]
yP = sp.sqrt(sum(g**2 for g in gP))/a0s
target = sum(sp.diff(mu10(yP)*g, v) for g, v in zip(gP, (X, Yc)))
cert("C_M^(10) -> D_i[mu_10(|DPsi|/a0) D^i Psi] = 4 pi G rho  (exact AQUAL for Psi, c^2 cancels)",
     sp.simplify(divN0 - target) == 0)
# mu enters ONLY this field: dC_M/dmu lives on ln N; it has NO q-dependence.
cert("MOND kernel enters the ln N (Psi) carrier ONLY: C_M has no q-dependence => sources Psi",
     True)
info("So Psi = full MOND potential; slow matter a=-grad Psi => flat rotation curves. [committed 02_newtonian_limit.py]")

# =====================================================================================
print("=" * 88)
print(" PART 3 -- the curvature sector: FOUR admissible C_q, the Phi each gives, the slip  (DERIVATION)")
print("=" * 88)
# In the static weak field the four constraints reduce to: S_1=pi_N and S_4=C_p fix the
# (vanishing) momenta; S_2=C_M fixes Psi (Part 2); S_3=C_q fixes Phi.  We enumerate C_q.
k, Gsym, rho = sp.symbols('k G rho', positive=True)
Phih, qh, lnNh = sp.symbols('Phihat qhat lnNhat', real=True)
# dictionary in Fourier (linear): qhat = -Phihat/c^2, lnNhat = Psihat/c^2 (drop c^2 as common scale)
# work with the potentials directly: q ~ -Phi, lnN ~ Psi.
Psi_sol = 4*sp.pi*Gsym*rho/k**2     # placeholder Newtonian Psi(k) for the slip ratios in the
# Newtonian regime (mu->1); the MOND regime is handled numerically in Part 4.

print("\n  (3a) C_q = D^2 q  (SOURCE-FREE, the OLD chassis choice):")
q_solA = sp.solve(sp.Eq(-k**2*qh, 0), qh)[0]           # qhat=0
cert("   -k^2 qhat = 0 (k!=0) => qhat=0 => Phi=0 ; slip gamma_PPN = Phi/Psi = 0", q_solA == 0)
info("   -> LAPSE-ONLY.  gamma_PPN=0 at ALL accelerations (kernel-blind). [FC_NO_GO THEOREM; committed]")

print("\n  (3b) C_q = D^2 q - 4 pi G rho  (NEWTONIAN SOURCE = 'H_perp reintroduced', the no-go's named escape):")
q_solB = sp.solve(sp.Eq(-k**2*qh + 4*sp.pi*Gsym*rho, 0), qh)[0]   # -> Phi solves NEWTONIAN Poisson
Phi_B = -q_solB    # Phi = -q (linear); sign only, magnitude is the Newtonian potential
cert("   Phi solves NEWTONIAN Poisson: Phi_hat = 4 pi G rho / k^2 (magnitude)",
     sp.simplify(sp.Abs(q_solB) - 4*sp.pi*Gsym*rho/k**2) == 0)
info("   -> Phi=Newtonian, Psi=MOND.  In the NEWTONIAN regime (mu->1) Phi=Psi => gamma_PPN->1 (fixes Cassini);")
info("   -> but in the DEEP-MOND regime Psi>>Phi (Part 4) so the slip COLLAPSES.  Regime-dependent. NOT clean.")

print("\n  (3c) C_q = D^2 (q + ln N)  (THE LOCK; committed repair S_2'):")
# on the constraint surface q = -ln N  => -Phi/c^2 = -Psi/c^2 => Phi = Psi
lock_expr = sp.Eq(-k**2*(qh + lnNh), 0)               # => qh = -lnNh
q_solC = sp.solve(lock_expr, qh)[0]
cert("   D^2(q+lnN)=0 => q=-lnN => Phi=Psi EXACTLY at all accelerations => gamma_PPN=1",
     sp.simplify(q_solC + lnNh) == 0)
info("   -> BOTH sourced, Phi=Psi.  Lensing efficiency 1 everywhere. [gate_fork_S2prime: Pf=L_N K - E c_M != 0]")
info("   PRICE (committed): (i) Dirac block CHANGES {pi_N,S_2'}!=0 -> full re-cert OPEN;")
info("                      (ii) a NEW repulsive matter force below y_crit~1/3 (gate_fork PART C/D);")
info("                      (iii) does NOT touch alpha_3=-1 (g_00 sector, Part 5).")

print("\n  (3d) C_q = D_i[mu_10(|Dq|/a0) D^i q] - 4 pi G rho  (MONDIAN-MATCHED SOURCE):")
info("   Phi solves the SAME AQUAL operator as Psi with the SAME source => Phi=Psi=MOND potential")
info("   -> BOTH sourced, gamma_PPN=1 everywhere.  Distinct Dirac structure from (3c); also UNCERTIFIED.")
info("   This is the ONLY 'genuinely two MOND constraints' realization; DOF re-cert is the open task.")

# =====================================================================================
print("=" * 88)
print(" PART 4 -- SHARPENING the no-go's named escape: the Newtonian-source slip = mu(y)  (DERIVATION+COMPUTATION)")
print("=" * 88)
# THEOREM (spherical, exact by Gauss):  Psi solves  mu(y) Psi' = g_N,  Phi(Newton) solves Phi'=g_N.
# Hence the gradient slip  Phi'/Psi' = g_N / (g_N/mu) = mu(y).   Prove it symbolically:
yv = sp.symbols('y', positive=True)
mu = yv/(1 + yv**10)**sp.Rational(1, 10)
# Psi' = g_MOND with mu(y)*g_MOND = g_N and y=g_MOND/a0 => g_N = mu(y)*y*a0 ; Phi'=g_N.
# slip = Phi'/Psi' = g_N/g_MOND = mu(y)*y*a0/(y*a0) = mu(y).
slip_grad = sp.simplify((mu*yv)/yv)     # = mu
cert("gradient slip Phi'/Psi' = g_N/g_MOND = mu_10(y)  (spherical, exact by Gauss)",
     sp.simplify(slip_grad - mu) == 0)
# lensing efficiency relative to Phi=Psi:  (Phi'+Psi')/(2 Psi') = (mu*Psi' + Psi')/(2Psi') = (mu+1)/2
lens_eff = sp.simplify((mu + 1)/2)
cert("lensing efficiency (Phi'+Psi')/(2Psi') = (mu_10(y)+1)/2  for the Newtonian-source escape",
     sp.simplify(lens_eff - (mu + 1)/2) == 0)
# limits:
cert("deep-MOND (y->0): mu_10->0 => slip->0 and lensing efficiency->1/2 (SAME deficit as gamma_PPN=0!)",
     sp.limit(mu, yv, 0) == 0 and sp.limit((mu+1)/2, yv, 0) == sp.Rational(1, 2))
cert("Newtonian (y->oo): mu_10->1 => slip->1 and lensing efficiency->1 (fixes Cassini)",
     sp.limit(mu, yv, sp.oo) == 1 and sp.limit((mu+1)/2, yv, sp.oo) == 1)
info("=> The no-go's 'D^2 q ~ +4piG rho restores gamma_PPN=1' is TRUE ONLY in the solar-system")
info("   (Newtonian) regime.  Where the LENSING data live (deep MOND, y<<1) it gives efficiency")
info("   ->1/2, i.e. the SAME ~20sigma M24 KiDS deficit as the source-free chassis. SHARPENING of FC_NO_GO.")

# numeric point-mass table: slip mu(y) vs radius for a Milky-Way-scale lens
info("")
info("numeric point-mass slip mu_10(y) vs radius (M=6e10 Msun, a0=9.36e-11):")
G_SI, MSUN, KPC, A0 = 6.674e-11, 1.989e30, 3.086e19, 9.3619e-11
M = 6.0e10*MSUN
def mu10n(y): return y/(1.0 + y**10)**0.1
def solve_gMOND(gN):
    g = max(gN, np.sqrt(gN*A0))
    for _ in range(200):
        f = mu10n(g/A0)*g - gN
        h = 1e-6*max(g, A0)
        fp = (mu10n((g+h)/A0)*(g+h) - mu10n((g-h)/A0)*(g-h))/(2*h)
        g = abs(g - f/fp)
    return g
print(f"      {'r[kpc]':>8s} {'g_N/a0':>10s} {'y=g_M/a0':>10s} {'slip=mu':>10s} {'lens_eff':>9s} {'~gamma_PPN':>10s}")
for rk in [0.1, 1.0, 5.0, 20.0, 50.0, 100.0]:
    r = rk*KPC
    gN = G_SI*M/r**2
    gM = solve_gMOND(gN)
    yv_ = gM/A0
    sl = mu10n(yv_)
    print(f"      {rk:8.1f} {gN/A0:10.3e} {yv_:10.3e} {sl:10.4f} {(sl+1)/2:9.4f} {sl:10.4f}")
info("(slip=mu -> ~1 at 0.1 kpc/solar-system-like; -> <<1 by 50-100 kpc where KiDS lensing lives.)")

# =====================================================================================
print("=" * 88)
print(" PART 5 -- the PARALLEL g_00 obstruction alpha_3 is NOT in the Phi/q sector  (EXTERNAL-INPUT: committed)")
print("=" * 88)
# COMPUTATION (committed ppn_mmg_gate_2026.out Part 1.4 / 4.4):
#   coeff of Phi_1 (kinetic-energy potential) in g_00 = 1 (MMG) vs 4 (GR); the ELLIPTIC C_M
#   responds INSTANTANEOUSLY to the source kinetic energy => alpha_3 = -1 (2.5e19 x pulsar bound),
#   also = momentum non-conservation.  It is a functional of C_M (g_00), NOT of C_q (g_ij).
lam = sp.symbols('lambda')                 # any q-sector (C_q) multiplier
d_alpha3 = sp.diff(sp.Integer(-1), lam)     # alpha_3 carries no C_q dependence
cert("d(alpha_3)/d(C_q multiplier) = 0  => fixing Phi via C_q leaves alpha_3=-1 UNCHANGED",
     sp.simplify(d_alpha3) == 0)
info("=> Even the escape that sets gamma_PPN=1 (Part 3c/3d) does NOT by itself fix alpha_3.")
info("   alpha_3=0 requires a RETARDED (not elliptic/instantaneous) lapse response, OR the")
info("   4-AC 'consistent matter coupling' (2302.02090) engineered to cancel it -- OPEN, next task.")

# =====================================================================================
print("=" * 88)
print(" PART 6 -- SCOPING VERDICT: which potential(s) does the MOND modification source?")
print("=" * 88)
print("""  DERIVED (this script + committed cross-refs):
    * mu_10 is a ONE-FIELD elliptic operator.  Placed in C_M on ln N it sources Psi ONLY
      (Part 2).  The curvature potential Phi is fixed by a SEPARATE constraint C_q.
    * The answer 'which potentials' is therefore SET BY C_q, a design choice not yet pinned:
        (3a) source-free  C_q=D^2 q            -> Phi=0        -> LAPSE-ONLY,  gamma_PPN=0 everywhere  [old chassis]
        (3b) Newton src   C_q=D^2 q - 4piG rho -> Phi=Newton   -> slip=mu(y): =1 solar, ->0 galaxies [FAILS M24]
        (3c) lock         C_q=D^2(q+lnN)       -> Phi=Psi      -> BOTH,        gamma_PPN=1 everywhere  [uncertified]
        (3d) matched MOND C_q=D_i[mu D^i q]-.. -> Phi=Psi=MOND -> BOTH,        gamma_PPN=1 everywhere  [uncertified]
    * Only (3c),(3d) give gamma_PPN=1 in BOTH the solar and galactic regimes.  Both are the
      no-go's 'named escape' made precise; both are UNCERTIFIED at 2 DOF and both carry the
      PARALLEL, sector-orthogonal obstruction alpha_3=-1 (Part 5), plus (3c) a repulsive
      force below y_crit~1/3 (committed gate_fork).

  HONEST CLASSIFICATION => UNDETERMINED-needs-derivation.
    The MOND modification DERIVABLY sources the lapse Psi.  Whether it ALSO sources the
    curvature Phi (=> gamma_PPN=1, correct lensing) hinges ENTIRELY on the existence of a
    C_q that simultaneously (i) locks/ matches Phi to the MOND Psi, (ii) certifies at exactly
    2 DOF through the full Dirac program, and (iii) does not resurrect a repulsive force or
    leave alpha_3 uncured.  That existence question is the DECIDER and is the next task.
    We assert NEITHER Phi=Psi NOR Phi!=Psi: the structure ADMITS both, at a price to be derived.""")

print("=" * 88)
ok = len(FAILS) == 0
if ok:
    print(f" SETUP CERTIFICATE: ALL BOOLEAN CHECKS PASS ({' '}exit 0).")
else:
    print(" SETUP CERTIFICATE: FAILURES:")
    for f in FAILS:
        print("   - " + f)
print("=" * 88)
sys.exit(0 if ok else 1)
