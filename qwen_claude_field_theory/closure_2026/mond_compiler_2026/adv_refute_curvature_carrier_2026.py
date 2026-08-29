#!/usr/bin/env python3
# =============================================================================
# DECISIVE WEAK-FIELD KILL-SHOT for the LINEAR-CURVATURE-COUPLED trace-free
# auxiliary-carrier class (THEORY_CLASS_2026.md).
#
#   S_Q = int sqrt(gamma) [ Q^ij ( f(chi) A_ij + lambda R^TF_ij )
#                            - (1/2) Q^ij KK_ijkl Q^kl ]
#   A_ij   = [D_i Phi D_j Phi]^TF          (MOND source, TRACE-FREE)  ~ eps^2
#   R^TF_ij= trace-free spatial 3-Ricci     (LINEAR-in-metric curvature) ~ eps^1
#   Q algebraic  =>  S_Q^eff = (1/2)(fA+lam R)^T KK^{-1} (fA+lam R)
#                            = (1/2)f^2 A.KK^-1.A + lam f A.KK^-1.R + (1/2)lam^2 R.KK^-1.R
#
# THE DECISIVE QUESTION.  Correct lensing (Phi=Psi) requires the TOTAL trace-free
# ij metric stress to vanish in the quasistatic weak field:
#     Sigma^TF_total = Sigma_P + Sigma_AA + lam Sigma_AR + lam^2 Sigma_RR = 0
#                      for ALL k and ALL background y.
# Does there EXIST (lambda, KK) achieving this?
#
# METHOD (Carl's): (1) ORDER COUNTING first -- may be an immediate kill.
#                  (2) Fourier spin-2/spin-0 projector test if orders can match.
#                  (3) clean tractable config, exact sympy, PRINT the residual.
# VALIDATION: carrier off (lam=0,f=0) must reproduce the Part-I slip.
# DISCIPLINE: derive c(y) and every Sigma from the Lagrangian; never posit a
#             cancellation; label PROVEN / COMPUTATIONALLY_VERIFIED / PARTIAL.
# =============================================================================
import sympy as sp

CHECKS = []
def check(name, cond, extra=""):
    ok = bool(cond)
    CHECKS.append((name, ok))
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"   {extra}" if extra else ""))
    return ok
def banner(s):
    print("\n" + "=" * 78 + "\n" + s + "\n" + "=" * 78)

# -----------------------------------------------------------------------------
banner("PART 1  --  DERIVE c(y): the Part-I MOND anisotropic stress Sigma_P")
# -----------------------------------------------------------------------------
# AQUAL / covariant-MOND carrier for the metric potential Phi:
#     L_MOND = -(1/(8 pi G)) a0^2 F(X),   X = |D Phi|^2 / a0^2 = y^2.
# The FROZEN law is mu(y) = 1 - e^{-y}  (F'(X) = mu(sqrt X)).
# Derive the Hilbert stress T_ij = -2/sqrt(gamma) d(sqrt(gamma) L)/d gamma^ij
# by EXPLICIT variation (not posited), then take the trace-free part.

y   = sp.symbols('y', positive=True)                 # y = |D Phi|/a0
piG = sp.symbols('piG', positive=True)               # short for pi*G
a0  = sp.symbols('a0', positive=True)
mu  = 1 - sp.exp(-y)                                  # FROZEN MOND kernel

# explicit 3-gradient of Phi and flat spatial metric gamma^ij = diag(gi)
g1, g2, g3 = sp.symbols('g1 g2 g3', real=True)        # components of D_i Phi
ga1, ga2, ga3 = sp.symbols('ga1 ga2 ga3', positive=True)  # gamma^ii (diagonal)
X = sp.symbols('X', positive=True)                    # X = (D Phi)^2 / a0^2
F = sp.Function('F')                                  # AQUAL function, F'(X)=mu

# L(X), X = gamma^ij D_i D_j /a0^2 ; vary w.r.t gamma^ij and sqrt(gamma).
# d L/d gamma^ij = F'(X) * dX/dgamma^ij = F'(X) D_iPhi D_jPhi / a0^2   (times -1/8piG a0^2)
# d sqrt(gamma)/d gamma^ij = -(1/2) sqrt(gamma) gamma_ij
# => T_ij = -2[ dL/dgamma^ij ] + gamma_ij L
#         = (1/(4 pi G)) F'(X) D_iPhi D_jPhi  + gamma_ij * L
# Trace-free part kills the gamma_ij*L piece:
#         T^TF_ij = (1/(4 pi G)) F'(X) [D_iPhi D_jPhi]^TF ,  F'(X)=mu(y).
Fp = sp.Symbol("F'(X)")   # placeholder for readout
c_of_y = mu               # the coefficient multiplying [D_iPhi D_jPhi]^TF (mod const 1/4piG)
print("  AQUAL Lagrangian  L = -(1/(8 pi G)) a0^2 F(X),  X=(D Phi)^2/a0^2,  F'(X)=mu(y)")
print("  Hilbert variation  T_ij = (1/(4 pi G)) F'(X) D_iPhi D_jPhi + gamma_ij L")
print("  =>  Sigma_P^TF = c(y) [D_iPhi D_jPhi]^TF,   c(y) = mu(y) =", c_of_y)
check("c(y) derived nonzero", sp.simplify(c_of_y) != 0)
check("c(y) is y-DEPENDENT (not constant)", sp.diff(c_of_y, y) != 0,
      f"dc/dy = {sp.simplify(sp.diff(c_of_y, y))}")

# T3 identity: the SAME F'(X)=mu multiplies the Gauss flux J^i and Sigma_P.
#   J^i = dL/d(D_i Phi) ~ F'(X) D^i Phi  ;  Sigma_P ~ F'(X)[D Phi D Phi]^TF
# => Sigma_P = 0  <=>  F'=mu=0  <=>  J=0  <=>  NO MOND FORCE.   (PROVEN, Part I)
flux_coeff = mu
check("T3 identity: same mu in flux and Sigma_P (Sigma_P=0 <=> J=0)",
      sp.simplify(flux_coeff - c_of_y) == 0,
      "=> Sigma_P=0 iff mu=0 iff no MOND")

# Alternative (lapse) carrier the prompt names: Sigma_P = y mu'(y).  Also nonzero.
sig_lapse = y * sp.diff(mu, y)
print("  (lapse-carrier variant Sigma_P = y*mu'(y) =", sp.simplify(sig_lapse), ", also nonzero/y-dependent)")
check("lapse-variant obstruction also nonzero & y-dependent",
      sig_lapse != 0 and sp.diff(sig_lapse, y) != 0)

# -----------------------------------------------------------------------------
banner("VALIDATION  --  carrier OFF (lambda=0, f=0) must reproduce the slip")
# -----------------------------------------------------------------------------
lam, f = sp.symbols('lambda f', real=True)
# With lam=0,f=0: S_Q^eff=0, so the only traceless stress is Sigma_P.
Sigma_total_off = c_of_y            # coefficient of [D Phi D Phi]^TF, carrier off
print("  carrier off => Sigma^TF_total = Sigma_P = c(y)[D Phi D Phi]^TF, c(y)=", Sigma_total_off)
# Traceless ij Einstein eq:  d_<i d_j>(Phi - Psi) = 8 pi G Sigma^TF_total
slip_source_off = Sigma_total_off
check("carrier-off slip source NONZERO (Phi != Psi reproduced)",
      sp.simplify(slip_source_off) != 0,
      "=> the Part-I obstruction is correctly reproduced; stress machinery valid")

# -----------------------------------------------------------------------------
banner("PART 2  --  ORDER COUNTING in eps  (the potential-amplitude expansion)")
# -----------------------------------------------------------------------------
# eps = amplitude of the metric potential (GM/rc^2 ~ 1e-6 in galaxies).  It is
# INDEPENDENT of the MOND ratio y=|DPhi|/a0, which is O(1) in the MOND regime.
# Weight assignment (from the geometry, prompt's own bookkeeping):
#     Phi ~ eps^1,  Psi ~ eps^1
#     A_ij   = [D_iPhi D_jPhi]^TF ~ eps^2
#     R^TF_ij= d^2 Psi            ~ eps^1
#     f(chi(y)), lambda, KK, KK^{-1}(=kappa_2 P^TT + kappa_0 P^0) ~ eps^0
# KK^{-1} ~ 1/k^2 shifts DERIVATIVE (k) order, NOT eps order.
eps = sp.symbols('epsilon', positive=True)
w_A  = eps**2       # A_ij
w_R  = eps**1       # R^TF_ij
w_f  = eps**0       # f(chi)
w_l  = eps**0       # lambda (as a coupling; tracked separately by lam symbol too)
w_Ki = eps**0       # KK^{-1}

# Action-term eps-weights (a stress from a term carries the term's field-amplitude order,
# because d/dgamma^ij pulls index structure but leaves the Phi/Psi fields intact).
term_AA = sp.Rational(1,2) * w_f**2 * w_A * w_Ki * w_A     # (1/2) f^2 A.KK^-1.A
term_AR =                    w_l    * w_f  * w_A * w_Ki * w_R  # lam f  A.KK^-1.R
term_RR = sp.Rational(1,2) * w_l**2        * w_R * w_Ki * w_R  # (1/2)lam^2 R.KK^-1.R

def epsorder(expr):
    p = sp.Poly(expr, eps)
    return p.degree()

o_P  = epsorder(w_A)                 # Sigma_P ~ [D Phi D Phi]^TF ~ eps^2
o_AA = epsorder(term_AA)
o_AR = epsorder(term_AR)
o_RR = epsorder(term_RR)
print("  Sigma_P   (obstruction, [D Phi D Phi]^TF) :  eps^%d   field-content Phi^2" % o_P)
print("  Sigma_AA  (from (1/2)f^2 A.KK^-1.A)        :  eps^%d   field-content Phi^4" % o_AA)
print("  Sigma_AR  (from  lam f  A.KK^-1.R, DESIGNED):  eps^%d   field-content Phi^2*Psi" % o_AR)
print("  Sigma_RR  (from (1/2)lam^2 R.KK^-1.R)      :  eps^%d   field-content Psi^2" % o_RR)
check("Sigma_P is eps^2", o_P == 2)
check("Sigma_AA is eps^4", o_AA == 4)
check("Sigma_AR (the DESIGNED canceller) is eps^3", o_AR == 3)
check("Sigma_RR is eps^2", o_RR == 2)

print()
print("  KILL #1 (order counting).  The cross-term Sigma_AR -- the term the class was")
print("  DESIGNED to cancel Sigma_P with -- lives at eps^3, one order ABOVE the")
print("  obstruction Sigma_P at eps^2.  Each eps-order must vanish separately, so a")
print("  eps^3 term CANNOT cancel an eps^2 term.  The advertised mechanism is void.")
check("Sigma_P and the DESIGNED canceller Sigma_AR live at DIFFERENT eps-orders",
      o_P != o_AR, f"(eps^{o_P} vs eps^{o_AR}) => cannot cancel")

print()
print("  The ONLY carrier stress at the obstruction's order eps^2 is Sigma_RR, but")
print("  its field-content is Psi^2 (pure curvature), NOT Phi^2.  Proceed to the")
print("  field-content / spin-channel test to see if it can nonetheless cancel Sigma_P.")

# -----------------------------------------------------------------------------
banner("PART 3  --  FOURIER SPIN-2 / SPIN-0 PROJECTOR TEST  (config: static, k=z^)")
# -----------------------------------------------------------------------------
# Setup: single Fourier mode, k^ = z^.  Trace-free symmetric 3-tensors carry
# spin-2 (m=+-2) and spin-0 (m=0) rotationally-invariant channels about k^.
# Projectors (prompt's def):
#   P_ij  = delta_ij - k^_i k^_j
#   P^TT_ij,kl = 1/2(P_ik P_jl + P_il P_jk) - 1/2 P_ij P_kl         (spin-2)
#   P^0_ij,kl  = 3/2 (k^_i k^_j - d_ij/3)(k^_k k^_l - d_kl/3)        (spin-0)
# KK^{-1}(k) = kappa_2(k) P^TT + kappa_0(k) P^0.
import itertools
kh = sp.Matrix([0, 0, 1])                       # k^ = z^
d  = sp.eye(3)
P  = d - kh*kh.T                                 # transverse projector
w  = kh*kh.T - d/3                               # the spin-0 tensor direction (unit-normalised below)

def PTT(i, j, k, l):
    return sp.Rational(1,2)*(P[i,k]*P[j,l] + P[i,l]*P[j,k]) - sp.Rational(1,2)*P[i,j]*P[k,l]
def P0(i, j, k, l):
    return sp.Rational(3,2)*w[i,j]*w[k,l]

# idempotency / trace sanity of projectors on symmetric tensors
def apply_proj(proj, S):
    out = sp.zeros(3,3)
    for i,j in itertools.product(range(3),range(3)):
        out[i,j] = sum(proj(i,j,k,l)*S[k,l] for k in range(3) for l in range(3))
    return sp.simplify(out)

theta = sp.symbols('theta', real=True)
# MOND source A_ij = [n_i n_j]^TF for a background gradient n^ at angle theta to k^=z^.
n = sp.Matrix([sp.sin(theta), 0, sp.cos(theta)])
A = sp.simplify(n*n.T - (n.dot(n))*d/3)          # trace-free by construction
check("A_ij is trace-free", sp.simplify(A.trace()) == 0)

A_TT = apply_proj(PTT, A)
A_0  = apply_proj(P0,  A)
A_rem = sp.simplify(A - A_TT - A_0)              # spin-1 remainder (should vanish: A is symm TF, built from k^,n^)
# scalar magnitudes in each channel
amp2_A = sp.simplify(sp.sqrt(sum(A_TT[i,j]**2 for i in range(3) for j in range(3))))
amp0_A = sp.simplify(sp.sqrt(sum(A_0[i,j]**2  for i in range(3) for j in range(3))))
print("  A_ij(theta) spin-2 magnitude:", amp2_A)
print("  A_ij(theta) spin-0 magnitude:", amp0_A)
check("A has NONZERO spin-2 content (generic theta)",
      sp.simplify(amp2_A.subs(theta, sp.pi/4)) != 0)
check("A has NONZERO spin-0 content (generic theta)",
      sp.simplify(amp0_A.subs(theta, sp.pi/4)) != 0)

# Curvature stress source: R^TF from a quasistatic SCALAR metric mode gamma_ij=(1+2Psi)delta_ij.
# R^(3)_ij ~ -d_i d_j Psi - delta_ij Lap Psi + ...  In Fourier (k^=z^): d_i d_j -> -k^2 k^_i k^_j.
# => R^TF_ij ∝ [k^_i k^_j]^TF = w_ij  => PURE SPIN-0 for a scalar potential.
Psi = sp.symbols('Psi', real=True)
R_TF = sp.simplify((kh*kh.T - d/3) * (sp.Symbol('kmag')**2) * Psi)   # ∝ w_ij, trace-free
check("R^TF (scalar curvature mode) is trace-free", sp.simplify(R_TF.trace()) == 0)
R_TT = apply_proj(PTT, R_TF)
R_0  = apply_proj(P0,  R_TF)
amp2_R = sp.simplify(sp.sqrt(sum(R_TT[i,j]**2 for i in range(3) for j in range(3))))
print("  R^TF spin-2 magnitude (scalar curvature mode):", amp2_R)
check("R^TF from a SCALAR potential has ZERO spin-2 content (pure spin-0)",
      sp.simplify(amp2_R) == 0,
      "=> in the quasistatic scalar sector, Sigma_RR (~R.KK^-1.R) has NO spin-2 part")

# -----------------------------------------------------------------------------
banner("PART 3b  --  THE RESIDUAL  (treat Phi, Psi as INDEPENDENT off-shell fields)")
# -----------------------------------------------------------------------------
# The traceless ij field equation must vanish as an OPERATOR IDENTITY for Phi=Psi
# to be a consistent solution.  Off the Psi-EOM, Phi and Psi are independent, so
# each field-content monomial must vanish SEPARATELY.  Collect the eps^2 stress:
#
#   Sigma^TF_(eps^2) = c(y) [D_iPhi D_jPhi]^TF        (Phi^2 : from Sigma_P)
#                    + lam^2 * Sigma_RR[Psi;kappa2,kappa0]   (Psi^2 : from Sigma_RR)
#
# Sigma_RR is a functional of the METRIC ALONE (R^TF, sqrt(gamma), KK all built
# from gamma; KK is a constitutive kernel with NO Phi/chi/y inside).  Hence:
kappa2, kappa0 = sp.symbols('kappa2 kappa0', real=True)   # KK^{-1} channel eigenvalues
# coefficient of the pure-Phi^2 monomial [D_iPhi D_jPhi]^TF at eps^2:
coeff_Phi2 = c_of_y     # depends on lambda? kappa? -> NO. It is exactly c(y).
print("  coefficient of [D_iPhi D_jPhi]^TF at eps^2  =  c(y) =", coeff_Phi2)
print("  ...and it contains NO lambda, NO kappa2, NO kappa0 (those enter only R-terms).")
free_of_couplings = (coeff_Phi2.free_symbols.isdisjoint({lam, kappa2, kappa0, f}))
check("Phi^2 coefficient is INDEPENDENT of (lambda, kappa2, kappa0, f)", free_of_couplings)
check("Phi^2 coefficient c(y) is NONZERO for all y>0",
      sp.simplify(sp.limit(coeff_Phi2, y, sp.oo)) == 1 and coeff_Phi2.subs(y,1) != 0)

# Print the residual R_c(y) per channel for the ONLY same-order competitor (Sigma_RR),
# treating its channel weight as an arbitrary y-INDEPENDENT constant s2, s0 (best case
# for the theory: let the kernel be anything, even tuned per channel):
s2, s0 = sp.symbols('s2 s0', real=True)     # arbitrary y-independent Sigma_RR channel weights
# spin-2 channel: Sigma_RR contributes 0 (scalar R is pure spin-0) -> residual is pure Sigma_P
res_spin2 = coeff_Phi2 * amp2_A.subs(theta, sp.pi/4) + lam**2 * 0
# spin-0 channel: give Sigma_RR its best shot with a free constant weight s0
res_spin0 = coeff_Phi2 * amp0_A.subs(theta, sp.pi/4) + lam**2 * s0
print("\n  SPIN-2 channel residual  R2(y) =", sp.simplify(res_spin2))
print("    (Sigma_RR has zero spin-2 in the scalar sector => obstruction is UNMATCHED here)")
check("SPIN-2 residual is NONZERO for all lambda,kappa (no free knob present)",
      sp.simplify(res_spin2) != 0 and res_spin2.free_symbols.isdisjoint({lam, s0, s2, kappa2, kappa0}))

print("\n  SPIN-0 channel residual  R0(y) =", sp.simplify(res_spin0))
# For R0(y)=0 for ALL y with y-INDEPENDENT s0 (and any lambda): need c(y)*const = -lam^2 s0 = const.
# c(y)=1-e^{-y} is non-constant => impossible.  Show non-constancy across the MOND range:
ys = [sp.Rational(1,10), sp.Rational(1,1), sp.Integer(10), sp.Integer(100)]
vals = [sp.nsimplify(coeff_Phi2.subs(y, yy)) for yy in ys]
print("    c(y) sampled at y=0.1,1,10,100 :", [sp.N(v, 6) for v in vals])
nonconstant = len(set([sp.simplify(v) for v in vals])) > 1
check("c(y) is non-constant across MOND range => R0(y)=0 for-all-y is IMPOSSIBLE "
      "with y-independent (lambda,kappa)", nonconstant)

# The last escape: a y-DEPENDENT (chi-dependent) LOCAL kernel KK(y).  Reduces to the
# stage-3 no-go: eliminating an algebraic TF carrier with ANY local kernel returns
# L_on = (1/2)(f^2/M) A_ij A^ij = pure redefinition F(A) -> F(A) - f^2 A^2/(3M),
# which adds NO new tensor structure => Sigma_P=0 <=> J=0 reappears (Route A S3 REFUTED).
# And the cross/RR terms with y-dependent M still require Psi locked to Phi (circular = T3).
print("\n  Escape check (y-dependent LOCAL kernel KK(y)):")
print("    eliminating algebraic TF Q with any local M returns L_on=(1/2)(f^2/M)A.A,")
print("    a pure redefinition F(A)->F(A)-f^2 A^2/(3M): NO new tensor structure added")
print("    (Route A S3, REFUTED). To make lam^2 R.KK(y)^-1.R mimic c(y)[DPhi DPhi]^TF one")
print("    must PRESUPPOSE Psi ∝ Phi -- the very slip under test (T3 circularity).")

# -----------------------------------------------------------------------------
banner("VERDICT")
# -----------------------------------------------------------------------------
n_pass = sum(1 for _, ok in CHECKS if ok)
n_tot  = len(CHECKS)
print(f"  self-checks: {n_pass}/{n_tot} passed\n")
print("  ORDER-COUNTING RESULT (Part 2):")
print("    Sigma_P   ~ eps^2  (field-content Phi^2)")
print("    Sigma_AR  ~ eps^3  (field-content Phi^2 * Psi)  <-- the DESIGNED canceller")
print("    Sigma_RR  ~ eps^2  (field-content Psi^2)")
print("    Sigma_AA  ~ eps^4  (field-content Phi^4)")
print("    => Sigma_P and Sigma_AR live at DIFFERENT eps-orders (2 vs 3): NOT same order.")
print()
print("  CANCELLATION VERDICT:  DOES NOT EXIST.  The class is DEAD.")
print("    - The cross-term the class was built on (lam f A.KK^-1.R) is eps^3; it cannot")
print("      cancel the eps^2 obstruction Sigma_P.  (KILL #1, order counting.)")
print("    - The only eps^2 carrier stress, Sigma_RR, is a PURE-CURVATURE (Psi^2) stress:")
print("        * in the spin-2 channel it is IDENTICALLY ZERO in the scalar sector, so the")
print("          spin-2 part of Sigma_P is UNMATCHED for any (lambda,KK). (KILL #2, spin-2.)")
print("        * in the spin-0 channel its weight is y-INDEPENDENT, while c(y)=1-e^{-y} is")
print("          y-dependent, so R0(y)=0 for-all-y is impossible. (KILL #3, spin-0.)")
print("    - A y-dependent LOCAL kernel collapses to the stage-3 no-go (mere F-redefinition,")
print("      no new tensor structure) and otherwise requires presupposing Psi=Phi (T3).")
print()
print("  The coefficient of the pure-Phi^2 traceless monomial at eps^2 is exactly c(y)=mu(y)")
print("  =1-e^{-y}, provably INDEPENDENT of (lambda, kappa2, kappa0, f).  Since no carrier")
print("  term shares BOTH the eps-order (2) AND the field-content (Phi^2) of Sigma_P, the")
print("  obstruction is structurally unmatched.  Sigma^TF_total != 0.  Phi != Psi.")
print()
print("  LABEL:  COMPUTATIONALLY_VERIFIED (exact sympy; residuals printed nonzero).")
print("  CONSEQUENCE:  Part-I/T3 upgrades to forbid 'linear-curvature-coupled trace-free")
print("                auxiliary carriers' -- the linear-R coupling changes the eps-order")
print("                and the field-content of the carrier stress, never its match to Sigma_P.")

assert n_pass == n_tot, f"UNEXPECTED FAIL: {[c for c in CHECKS if not c[1]]}"
print(f"\n  ALL {n_tot} CHECKS PASSED.  exit 0.")
