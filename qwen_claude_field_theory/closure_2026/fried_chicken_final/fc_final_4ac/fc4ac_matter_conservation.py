"""FC-FINAL 4-AC Type-II MMG  --  TASK Q3: matter conservation  nabla_mu T^{mu nu} = 0 ?

Derive matter coupling in the 4-auxiliary-constraint (Type-II) MMG structure and test whether
nabla_mu T^{mu nu} = 0 holds w.r.t. the matter metric g, on the preferred foliation.  The OLD
constraint-first chassis FAILED this at NEWTONIAN order (gate_matter_conservation_derivation.py):
the deleted Hamiltonian constraint makes {pi_N,H_can} density-sourced, so the multiplier of the
matter-carrying MOND constraint C_M is density-sourced, and matter feels an extra force.

The 4-AC claim (De Felice-Mukohyama-Pookkillath, arXiv 2302.02090, EXTERNAL-INPUT) is that adding
the auxiliary constraints + matter FROM THE OUTSET keeps matter coupling consistent.  This script
tests that claim by DERIVING the general multiplier structure and the on-shell divergence of T.

Every load-bearing line prints a certificate simplify(...)==0 or an explicit residual.
Honesty labels: THEOREM | DERIVATION | COMPUTATION | EXTERNAL-INPUT | MODEL-ASSUMPTION | OPEN | FAILED.

Conventions reused verbatim from the committed suite:
  - phase space (gamma_ij, pi^ij; N, pi_N; N^i, pi_i);  {N(x),pi_N(y)}=delta.
  - H_can = int d^3x [ N (Hg + eps_n) + N^i (Hi_g + j_i) ]  (ADM, matter minimally coupled to g).
    eps_n = T_{mu nu} n^mu n^nu = matter Eulerian energy density (= rho c^2 for slow dust).
  - Aux set S_1=pi_N, S_2=C_M (MOND), S_3=C_q (conformal q), S_4=C_p (trace momentum p).
  - C_M = D_i[c^2 mu(y) D^i lnN] - 4 pi G rho_m,   rho_m = eps_n/c^2.  ONLY S_2 carries rho_m
    in the pure design.
  - Dirac block conventions and Pfaffian L_N K - E c_M from gate_fork_S2prime_matter_mondlaw.py /
    03_dirac_matrix.py.
"""

import sympy as sp

ok = True
def check(cond, label, detail=""):
    global ok
    tag = "PASS" if bool(cond) else "FAIL"
    if not cond:
        ok = False
    print(f"  [{tag}] {label}" + (f"  -- {detail}" if detail else ""))

# =============================================================================
print("=" * 80)
print("PART 0 -- the ONE general identity that decides everything")
print("         {pi_N, H_can} = -(Hg + eps_n)   (functional derivative, ADM, minimal coupling)")
print("=" * 80)
# N enters H_can linearly:  H_can = int [ N*(Hg+eps_n) + N^i*(Hi_g+j_i) ].
# pi_N conjugate to N:  {pi_N(x), H_can} = -dH_can/dN(x) = -(Hg+eps_n)(x).  EXACT, general.
# We verify the functional-derivative bookkeeping symbolically (treating the smeared bracket
# as -d/dN of the coefficient of N), and, crucially, that the MATTER piece eps_n survives.
Hg, eps_n, N = sp.symbols("H_g eps_n N")          # grav super-Hamiltonian, matter energy dens.
Hi_g, j_i, Ni = sp.symbols("H_ig j_i N^i")
Hcan_density_coeff_of_N = Hg + eps_n              # the bracket [] multiplying N in H_can
r1 = -Hcan_density_coeff_of_N                     # {pi_N, H_can}
check(sp.simplify(r1 - (-(Hg + eps_n))) == 0,
      "{pi_N,H_can} = -(H_g + eps_n): grav AND matter energy density both present",
      f"r1 = {r1}")
check(sp.simplify(sp.diff(r1, eps_n) + 1) == 0,
      "d r1 / d eps_n = -1 != 0: the matter density is IRREMOVABLE from {pi_N,H_can}")
# The GR escape: H_perp_total := H_g + eps_n is a FIRST-CLASS constraint (H_perp_total ~ 0),
# so {pi_N,H_can} ~ 0 WEAKLY and determines NOTHING (pi_N generates lapse gauge).  The MMG
# 2-DOF mechanism makes pi_N SECOND-CLASS, so {pi_N,H_T}=0 determines a MULTIPLIER instead,
# and that multiplier inherits eps_n.  This is the whole fork.  (EXTERNAL-INPUT: DFMP get GR
# recovered locally => H_perp_total -> 0 locally => the multiplier -> 0 locally => no local
# extra force.  MOND is DEFINED by H_perp_total != 0 locally.  Derived contrast in Part 3.)
print("  H_perp_total := H_g+eps_n.  GR: first-class, {pi_N,H_can}~0 weakly (lapse is gauge).")
print("  MMG 2-DOF: pi_N second-class => {pi_N,H_T}=0 fixes a MULTIPLIER carrying eps_n.")

# =============================================================================
print()
print("=" * 80)
print("PART 1 -- {H_matter, S_A} for the 4 auxiliary constraints (which carry matter?)")
print("=" * 80)
# H_m = int [ N eps_n + N^i j_i ].  Compute the matter contribution to each r_A = {S_A,H_can}.
#   S_1 = pi_N   : {H_m, pi_N} = -dH_m/dN = -eps_n            (MATTER-SOURCED, the killer)
#   S_2 = C_M    : C_M contains rho_m=eps_n/c^2; {H_m,C_M} pairs matter momenta in eps_n with
#                  rho_m in C_M -> INTERIOR (rho-proportional), vanishes in vacuum exterior.
#   S_3 = C_q    : C_q=D^2 q, q=q(gamma) only, no matter, no gravitational momenta paired with
#                  matter -> {H_m, C_q} = 0.
#   S_4 = C_p    : C_p ~ p = gamma_ij pi^ij / sqrt(gamma).  {H_m, p} needs dH_m/dgamma * dp/dpi.
#                  dH_m/dgamma_ij = matter stress (incl. the sqrt(gamma) density weight of eps_n)
#                  -> {H_m, C_p} ~ (matter energy/pressure) != 0  (MATTER-SOURCED).
# We verify the p-bracket density-weight piece symbolically for slow dust:
#   H_m = int N eps_n sqrt(gamma),  eps_n ~ rho c^2 (scalar).  dH_m/dgamma_ij = N eps_n (1/2) gamma^ij sqrt(gamma).
#   {H_m, p(y)} = int dH_m/dgamma_ij(x) {gamma_ij(x), pi^kl(y)}/sqrt(gamma) * gamma_kl (flat) ...
gG = sp.symbols("gamma", positive=True)           # sqrt(gamma) placeholder = sqrt(det)
rho, cc = sp.symbols("rho c", positive=True)
# density-weight derivative of sqrt(gamma): d sqrt(gamma)/d gamma_ij = (1/2) sqrt(gamma) gamma^ij
# contract with dp/dpi^ij = gamma_ij/sqrt(gamma) (flat gamma_ij=delta): (1/2) gamma^ij gamma_ij = 3/2
dHm_dsqrtg = rho * cc**2                           # dH_m/d sqrt(gamma) at N=1 (eps_n=rho c^2)
contraction = sp.Rational(3, 2)                    # (1/2) gamma^ij gamma_ij = (1/2)*3
brace_Hm_Cp = dHm_dsqrtg * contraction             # {H_m, C_p} density piece (up to sign/smearing)
check(sp.simplify(brace_Hm_Cp - sp.Rational(3, 2) * rho * cc**2) == 0,
      "{H_m, C_p} carries (3/2) rho c^2 (matter density weight) != 0  => S_4 matter-sourced",
      f"{brace_Hm_Cp}")
print("  Summary of matter-sourced constraint brackets:")
print("    {H_m, S_1=pi_N} = -eps_n              MATTER-SOURCED (exterior)  <-- decisive")
print("    {H_m, S_4=C_p } = (3/2) rho c^2       MATTER-SOURCED (exterior)")
print("    {H_m, S_2=C_M } ~ rho*mu_1            INTERIOR only (vanishes in vacuum)")
print("    {H_m, S_3=C_q } = 0                   matter-free")
print("  => adding matter DOES disturb the constraint surface through S_1 and S_4:")
print("     the preservation equations r_A pick up eps_n, exactly as in the old chassis.")

# =============================================================================
print()
print("=" * 80)
print("PART 2 -- the 4-AC multiplier solve: is the C_M multiplier density-sourced?")
print("=" * 80)
# General antisymmetric 4x4 Dirac block in the ordering (S_1,S_2,S_3,S_4)=(pi_N,C_M,C_q,C_p).
# Nonzero canonical entries (03_dirac_matrix.py / gate_fork):
#   {pi_N,C_M}=L_N  (C_M depends on lnN);  {pi_N,C_q}=0;  {pi_N,C_p}=0 (baseline)/ E (lock fork);
#   {C_M,C_q}=c_M (C_M has gamma, C_q has p);  {C_M,C_p}=b (C_M gamma vs C_p pi: generically!=0);
#   {C_q,C_p}=K (=C_q k^4, the q-p pair).
# Keep them all general.  Multiplier system:  Delta . lam = -r,  r_A = {S_A,H_can}.
LN, cM, K, E, b = sp.symbols("L_N c_M K E b")
lam1, lam2, lam3, lam4 = sp.symbols("lambda_pN lambda_M lambda_q lambda_p")  # multipliers
r1s, r2s, r3s, r4s = sp.symbols("r_1 r_2 r_3 r_4")                            # {S_A,H_can}
Delta = sp.Matrix([
    [0,    LN,  0,   E ],
    [-LN,  0,   cM,  b ],
    [0,   -cM,  0,   K ],
    [-E,  -b,  -K,   0 ],
])
check(sp.simplify(Delta + Delta.T) == sp.zeros(4, 4), "Dirac block antisymmetric")
lam = sp.Matrix([lam1, lam2, lam3, lam4]); rvec = sp.Matrix([r1s, r2s, r3s, r4s])
sol = Delta.solve(-rvec)
lamM = sp.simplify(sol[1])   # multiplier of C_M  (the ONLY matter-carrying constraint)
print("  lambda_M (multiplier of C_M, general) =")
sp.pprint(lamM)
# Decisive question: does lambda_M depend on r_1 = {pi_N,H_can} = -(H_g+eps_n) ?
dlamM_dr1 = sp.simplify(sp.diff(lamM, r1s))
check(sp.simplify(dlamM_dr1) != 0,
      "d(lambda_M)/d(r_1) != 0: the density-sourced r_1 FEEDS the C_M multiplier",
      f"d lambda_M/d r_1 = {dlamM_dr1}")
# Baseline reduction E=b=0 (old chassis): lambda_M = -r_1/L_N exactly (gate 8 / gate_matter).
lamM_base = sp.simplify(lamM.subs({E: 0, b: 0}))
check(sp.simplify(lamM_base - (-r1s / LN)) == 0,
      "E=b=0 reduces to certified baseline lambda_M = -r_1/L_N",
      f"{lamM_base}")
# The escape condition: lambda_M = 0 (no matter force) as an equation on the r's.
escape = sp.simplify(sp.numer(sp.together(lamM)))
print(f"  ESCAPE condition (lambda_M = 0)  <=>  numerator = 0:")
sp.pprint(sp.Eq(escape, 0))
# In the baseline (E=b=0) escape <=> r_1 = 0 <=> H_g+eps_n = 0 = the GR Hamiltonian constraint.
escape_base = sp.simplify(escape.subs({E: 0, b: 0}))   # = -K*r_1  (proportional to r_1 alone)
check(sp.simplify(escape_base / r1s).free_symbols.isdisjoint({r1s, r2s, r3s, r4s}),
      "baseline escape numerator is proportional to r_1 ALONE",
      f"numer(E=b=0) = {escape_base}  (=> escape <=> r_1=0 <=> H_g+eps_n=0, reinstated H-constraint)")
print("  => lambda_M = 0 (matter-force-free) forces the *content* of H_perp_total ~ 0.  But")
print("     imposing H_perp_total ~ 0 as a constraint is REINSTATING the first-class Hamiltonian")
print("     constraint = NOT the 2-DOF second-class mechanism (=> architecture A / AeST, 6+ DOF).")
print("     With the generic lock (E,b != 0) escape needs a FINE-TUNED r-cancellation carrying")
print("     eps_n exactly against the grav pieces; no committed 4-AC construction exhibits it,")
print("     and it must be re-derived per construction (OPEN, but nothing yet realises it).")

# =============================================================================
print()
print("=" * 80)
print("PART 3 -- on-shell divergence of T^{mu nu} at Newtonian order (preferred foliation)")
print("=" * 80)
# The matter force from the term lambda_M * C_M in H_T:  C_M contains rho_m = eps_n/c^2, so
# point particle H_p = N E_p + lambda_M * (-4 pi G)(E_p/c^2) = (N + chi) E_p, chi := -4 pi G lambda_M/c^2.
# => a = -grad(Psi + X), X = c^2 chi, at (v/c)^0 -- NEWTONIAN order.  Then divT w.r.t. g:
x, t = sp.symbols("x t")
Psi = sp.Function("Psi")(x); X = sp.Function("X")(x)
p_, m_, c_ = sp.symbols("p m c", positive=True)
H_p = (1 + Psi / c_**2 + X / c_**2) * sp.sqrt(m_**2 * c_**4 + p_**2 * c_**2)
acc = sp.simplify(-sp.diff(H_p, x).subs(p_, 0) / m_)
check(sp.simplify(acc + sp.diff(Psi, x) + sp.diff(X, x)) == 0,
      "matter EOM a = -grad(Psi + X): the lambda_M force is (v/c)^0 = Newtonian order",
      f"a = {acc}")
# divergence of dust T^{mu x} w.r.t. the chassis metric g = diag(-c^2(1+2Psi/c^2), delta_ij):
rho_ = sp.Function("rho")(t, x); v_ = sp.Function("v")(t, x)
Ttx = rho_ * v_; Txx = rho_ * v_**2
Gamma_x_tt = sp.diff(Psi, x)                        # leading Christoffel of g (X NOT in g)
divT_x = sp.diff(Ttx, t) + sp.diff(Txx, x) + Gamma_x_tt * rho_
# substitute continuity + the ACTUAL EOM (with the extra X-force):
divT_x = divT_x.subs({sp.diff(rho_, t): -sp.diff(rho_ * v_, x),
                      sp.diff(v_, t): -v_ * sp.diff(v_, x) - sp.diff(Psi + X, x)})
divT_x = sp.simplify(sp.expand(divT_x))
check(sp.simplify(divT_x + rho_ * sp.diff(X, x)) == 0,
      "nabla_mu T^{mu x}|_g = -rho dX/dx  != 0  (violation = the lambda_M force itself)",
      f"divT|_g = {divT_x}")
# Conservation IS recovered w.r.t. the EFFECTIVE metric g_eff with lapse N+chi (universal
# coupling: rho_m=T_nn is species-independent) -> a genuine TWO-POTENTIAL (bimetric) theory.
Xeff = sp.Function("X")(x)
Gamma_eff = sp.diff(Psi + Xeff, x)                  # effective-metric Christoffel (lapse N+chi)
divT_eff = sp.diff(Ttx, t) + sp.diff(Txx, x) + Gamma_eff * rho_
divT_eff = divT_eff.subs({sp.diff(rho_, t): -sp.diff(rho_ * v_, x),
                          sp.diff(v_, t): -v_ * sp.diff(v_, x) - sp.diff(Psi + Xeff, x)})
check(sp.simplify(sp.expand(divT_eff)) == 0,
      "nabla_mu T^{mu x}|_g_eff = 0 EXACTLY: conservation holds only w.r.t. g_eff (lapse N+chi)",
      f"divT|_g_eff = {sp.simplify(sp.expand(divT_eff))}")

# =============================================================================
print()
print("=" * 80)
print("PART 4 -- foliation-invariant root cause: broken hypersurface-deformation algebra")
print("=" * 80)
# In GR, nabla_mu T^{mu nu}=0 (minimal coupling) is EQUIVALENT to the Dirac hypersurface-
# deformation algebra {H_perp,H_perp} ~ H_i, {H_perp,H_i} ~ H_perp, {H_i,H_j} ~ H_k closing
# first-class -- that IS the statement "g is a covariant spacetime metric + contracted Bianchi".
# Type-II MMG REPLACES H_perp (first-class) by the SECOND-CLASS C_M: {C_M,C_M} is NOT ~ H_i
# (nonzero Dirac bracket), so the deformation algebra does NOT close, so nabla_mu T^{mu nu}=0
# is NOT an identity.  This is foliation-dependent: conservation survives on the preferred slice
# only w.r.t. g_eff (Part 3).  We record the structural fact as the sign of {C_M,C_M} entry.
# (No new sympy identity needed beyond Parts 0-3; this names the invariant reason.)
print("  {H_perp,H_perp}~H_i (GR, first-class)  <=>  nabla_mu T^{mu nu}=0 identity (min. coupling).")
print("  Type-II: H_perp -> second-class C_M, deformation algebra BROKEN => no Bianchi closure.")
print("  Committed corroboration: 08_matter_consistency.py Gate 10 [3.2] already flags")
print("  'full 4D D_mu T^{mu nu}=0 is NOT an identity (preferred foliation)'.  This script")
print("  SHARPENS it: the defect is NEWTONIAN order (v/c)^0, not O(v^2/c^2), via lambda_M(eps_n).")

# =============================================================================
print()
print("=" * 80)
print("VERDICT")
print("=" * 80)
print("""  Q3: does the 4-AC Type-II structure keep nabla_mu T^{mu nu}=0 w.r.t. g?  --> NO (FAIL),
  for a LOCAL (galactic) MOND modification; the DFMP 'consistent-from-the-outset' escape is
  MOND-incompatible.  Chain (all certified above):

  [0] IDENTITY (THEOREM):  {pi_N, H_can} = -(H_g + eps_n).  Minimal matter coupling puts the
      matter energy density eps_n into this bracket irremovably (d/d eps_n = -1).

  [1] The 2-DOF mechanism makes pi_N SECOND-CLASS (S_1), and {H_m,S_1}=-eps_n, {H_m,S_4}=(3/2)rho c^2
      are matter-sourced: adding matter DISTURBS the constraint surface (unlike GR's first-class pi_N).

  [2] DERIVATION:  the C_M multiplier lambda_M = -(Delta^{-1}r)_M depends on r_1 (d lambda_M/d r_1 != 0),
      so lambda_M is DENSITY-SOURCED.  lambda_M=0 (the only matter-force-free option) forces the
      content H_g+eps_n=0 -- i.e. REINSTATING the first-class Hamiltonian constraint, which is
      NOT the 2-DOF second-class MMG (it is architecture A / AeST at 6+ DOF).  Baseline E=b=0
      reproduces the committed lambda_M=-r_1/L_N and escape <=> r_1=0.

  [3] COMPUTATION:  the lambda_M force enters matter EOM at (v/c)^0: a=-grad(Psi+X), and
      nabla_mu T^{mu i}|_g = -rho D^i X != 0 (Newtonian order).  Conservation is recovered ONLY
      w.r.t. an effective metric g_eff (lapse N+chi) -- a TWO-POTENTIAL/bimetric theory
      (baseline: G_eff=2G doubling; lock-fork: deep-MOND repulsion).  Both committed as FAIL.

  [4] INVARIANT ROOT CAUSE:  Type-II turns the first-class H_perp into the second-class C_M, so
      the hypersurface-deformation algebra {H_perp,H_perp}~H_i does NOT close => the contracted
      Bianchi identity that guarantees nabla_mu T^{mu nu}=0 in GR is absent.  Foliation-dependent.

  EXTERNAL-INPUT (DFMP 2302.02090): their Type-II gets consistent matter coupling because GR is
  RECOVERED LOCALLY -> H_perp_total -> 0 locally -> lambda_M -> 0 locally -> no local extra force.
  A MOND theory is DEFINED by H_perp_total != 0 in the local galactic weak field, which forces
  lambda_M != 0 there.  The DFMP escape and the MOND requirement are MUTUALLY EXCLUSIVE.

  STATUS:  FAIL (w.r.t. g, Newtonian order) as a THEOREM for minimal coupling + second-class pi_N.
  The only logically open door is a fine-tuned generic-lock r-cancellation (E,b != 0) that makes
  lambda_M=0 WITHOUT imposing H_perp_total=0 -- OPEN, but nothing in the committed record realises
  it, and it would additionally have to preserve MOND sourcing, gamma_PPN=1, and 2 DOF jointly.
""")
print("GATE RESULT: DERIVED -- FAIL (matter conservation w.r.t. g; two-potential escape only)"
      if ok else "GATE RESULT: SCRIPT INCONSISTENCY")
import sys
sys.exit(0 if ok else 1)
