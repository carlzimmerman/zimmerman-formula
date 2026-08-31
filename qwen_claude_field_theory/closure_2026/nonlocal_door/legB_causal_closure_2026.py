#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
legB_causal_closure_2026.py
TRICHOTOMY LEG B (NONLOCAL/CAUSAL) -- CLOSE OR BREAK.

Question (Layer C): can a scalar functional q[g] of the metric alone give a0(z) ~ H(z)
inside bound systems with (i) no new propagating DOF, (ii) no independent Cauchy data,
(iii) no conserved dark charge?  This script settles the NONLOCAL leg at kernel-level
generality (not just the DW box^-1 construction):

S1  Naive variation of a retarded bilinear action symmetrizes the kernel:
      grad S = (1/2)(K_ret + K_adv) phi.   [advanced adjoint appears -- confirmed]
S2  Helmholtz variational-integrability: E = K_ret phi - J is an EL equation of ANY
      action  <=>  K_ret symmetric  <=>  K_ret time-LOCAL.  A genuinely retarded EOM
      is NEVER Euler-Lagrange => Noether's theorems do not apply to it directly.
S3  The in-in/CTP repair at FULL GENERALITY: for an ARBITRARY retarded kernel K_ret
      the doubled action S = phi_D^T K_ret phi_c + (1/2) phi_D^T K_K phi_D is a genuine
      (symmetric-Hessian) action whose Delta-variation at Delta->0 is EXACTLY the
      retarded EOM; the advanced adjoint acts only on the response sector phi_D -> 0.
S4  Conservation UPGRADE: in the localized (auxiliary-field) form the theory is a
      local reparametrization/diffeo-invariant action; second Noether theorem =>
      the constraint (energy) identity holds on EVERY solution -- retarded-data
      solutions included.  Verified symbolically in a lapse-N reparametrization-
      invariant toy carrying the exact xi(Box X - S) structure.
      => The "causality-vs-conservation trade" is ESCAPABLE.  The true price is S5.
S5  LOCALIZATION IS GENERIC, i.e. the price of S3+S4 is FIELDS:
      (a) rational-symbol causal kernels  = Green functions of local operators
          => finite set of auxiliary fields (X, xi) with SLAVED (zero) Cauchy data;
          explicit matrix elimination shows the response field xi propagates with the
          ADVANCED kernel in the naive EL form (this is where the adjoint hides) and
          is re-routed to retarded only by the CTP boundary structure (sf47/sf48).
      (b) NON-rational causal kernels: spectral (Kallen-Lehmann-type) representation
          => a CONTINUUM of slaved fields.  Verified: the memory kernel with Laplace
          symbol s^(-1/2) = integral of first-order retarded kernels over a mass
          continuum (sympy-evaluated identity).
      Either way the cosmological information enters the bound system carried by
      a nonzero scalar PROFILE X(x) whose gradients gravitate: an effective dark
      stress, deterministic but present.
S6  EVENT-HORIZON (teleological) functionals close OUTRIGHT:
      R_h(t) = c*int_t^inf dt'/a  has functional derivative with STRICTLY FUTURE
      support (computed); the EOM at t responds to perturbations at t' > t
      (computed: advanced response), and R_h is NOT a functional of histories on the
      CTP contour [t0, t_max] (needs a(t) beyond t_max) => the in-in repair does not
      exist for it.  Also: at the exact dS point the proper horizon degenerates to
      the CONSTANT c/H (computed) -- exactly where it becomes quasi-local it stops
      carrying any z-evolution (Layer A only).
S7  Exhaustive kernel-support classification + verdict.

VERDICT SHAPE (honest): Leg B does NOT close as a clean no-go against the LITERAL
conditions (i)-(iii) -- the in-in metric-only retarded functional passes all three
as literally stated.  It closes in a SHARPENED form: every causal+conserved Leg B
realization is equivalent to a local dark-FIELD theory (finite or continuum of
auxiliary scalars) restricted to a slaved-data surface, with (1) a negative-energy
direction in the auxiliary sector held off only by that data constraint (sf43/sf48;
nonlinear re-excitation gate G3 open) and (2) an O(1) gravitating scalar profile
inside the bound system.  "No free dark STATE" is achievable; "no dark FIELD/stress"
is not.  The teleological subclass (event horizons) closes with no escape.
"""
import sys
import sympy as sp

FAIL, NCHK = [], [0]

def check(cond, label, detail=""):
    NCHK[0] += 1
    ok = bool(cond)
    print(f"  [{'ok' if ok else 'FAIL'}] {NCHK[0]:02d} {label}" + (f"\n         {detail}" if detail else ""))
    if not ok:
        FAIL.append(f"{NCHK[0]:02d} {label}")

def hdr(s):
    print("\n" + "=" * 88)
    print(s)
    print("=" * 88)

# ============================================================================
hdr("S1: NAIVE VARIATION OF A RETARDED ACTION SYMMETRIZES THE KERNEL (advanced adjoint)")
# ============================================================================
# Discrete time, 4 steps.  A retarded (causal) translation-invariant kernel is a
# lower-triangular Toeplitz matrix K_ret; its transpose is the ADVANCED kernel.
k0, k1, k2, k3 = sp.symbols('k0 k1 k2 k3', real=True)
N = 4
K_ret = sp.Matrix(N, N, lambda i, j: [k0, k1, k2, k3][i - j] if i >= j else 0)
K_adv = K_ret.T
phi = sp.Matrix(sp.symbols('phi0:4', real=True))

S_naive = sp.Rational(1, 2) * (phi.T * K_ret * phi)[0, 0]
gradS = sp.Matrix([sp.diff(S_naive, p) for p in phi])
sym_part = sp.Rational(1, 2) * (K_ret + K_adv) * phi

check(sp.simplify(gradS - sym_part) == sp.zeros(N, 1),
      "grad of (1/2) phi^T K_ret phi  ==  (1/2)(K_ret + K_adv) phi  EXACTLY",
      "the honest variation of a retarded functional contains the ADVANCED adjoint -- confirmed")

adv_present = any(sp.simplify(gradS[i].diff(phi[j])) != 0 for i in range(N) for j in range(i + 1, N))
check(adv_present,
      "EOM at time t_i depends on phi(t_j), j>i: acausal (advanced) response in the naive EL eq")

# ============================================================================
hdr("S2: HELMHOLTZ CONDITION -- A RETARDED EOM IS NEVER EULER-LAGRANGE")
# ============================================================================
# E(phi) = K phi - J is the gradient of some action  <=>  Jacobian dE_i/dphi_j = K
# is SYMMETRIC (Helmholtz integrability).  For a causal Toeplitz kernel:
sym_conditions = sp.simplify(K_ret - K_ret.T)
sols = sp.solve([sym_conditions[i, j] for i in range(N) for j in range(N)], [k1, k2, k3], dict=True)
check(sols == [{k1: 0, k2: 0, k3: 0}],
      "K_ret variational (symmetric) <=> k1=k2=k3=0 <=> kernel is TIME-LOCAL",
      "a genuinely retarded (memory) EOM is not the EL equation of ANY action of phi alone;"
      " => Noether's 2nd theorem does not apply to the hand-imposed retarded EOM"
      " (aligns with committed DW 'conservation NOT-COMPUTED' on the nonlocal form)")

# ============================================================================
hdr("S3: THE CTP/IN-IN REPAIR AT ARBITRARY-KERNEL GENERALITY")
# ============================================================================
# Doubled variables (phi_c, phi_D).  For ANY retarded kernel K_ret define
#   S_CTP = phi_D^T K_ret phi_c + (1/2) phi_D^T K_K phi_D    (K_K symmetric)
# This IS a genuine action: its Hessian on (phi_c, phi_D) is symmetric.
phic = sp.Matrix(sp.symbols('pc0:4', real=True))
phid = sp.Matrix(sp.symbols('pd0:4', real=True))
kk = sp.symbols('kk0:4', real=True)
K_K = sp.Matrix(N, N, lambda i, j: kk[abs(i - j)])  # symmetric
S_ctp = (phid.T * K_ret * phic)[0, 0] + sp.Rational(1, 2) * (phid.T * K_K * phid)[0, 0]

allv = list(phic) + list(phid)
Hess = sp.Matrix(2 * N, 2 * N, lambda i, j: sp.diff(S_ctp, allv[i], allv[j]))
check(sp.simplify(Hess - Hess.T) == sp.zeros(2 * N, 2 * N),
      "S_CTP has a SYMMETRIC Hessian: it is a genuine action (variational principle restored)")

E_c = sp.Matrix([sp.diff(S_ctp, pd) for pd in phid]).subs({pd: 0 for pd in phid})
check(sp.simplify(E_c - K_ret * phic) == sp.zeros(N, 1),
      "delta S_CTP / delta phi_D |_{D->0}  ==  K_ret phi_c  (EXACTLY the retarded EOM)",
      "holds for ARBITRARY retarded K_ret -- generality beyond the DW box^-1 case established")

E_d = sp.Matrix([sp.diff(S_ctp, pc) for pc in phic])
check(sp.simplify(E_d - K_adv * phid) == sp.zeros(N, 1),
      "delta S_CTP / delta phi_c  ==  K_adv phi_D: the advanced adjoint acts ONLY on the"
      " response sector, which the classical limit sets to zero (phi_D -> 0)")

# ============================================================================
hdr("S4: CONSERVATION UPGRADE -- LOCALIZED FORM IS EL + NOETHER ON EVERY SOLUTION")
# ============================================================================
# Reparametrization-invariant lapse-N toy carrying the exact localized structure
#   L = xi' X'/N - N xi sigma(q) + q'^2/(2N) - N V(q)
# (xi = multiplier/response field, X = localized nonlocal scalar, q = matter, N = lapse).
# Second Noether theorem: invariance under t -> t + eps(t), i.e.
#   delta f = eps f' (scalars),  delta N = (eps N)'  gives the identity
#   E_X X' + E_xi xi' + E_q q'  -  N (E_N)'  ==  0   IDENTICALLY (off shell).
# => on ANY solution of the field EOMs (retarded-data solution included), (E_N)'=0:
#    the constraint/conservation law propagates automatically.
t, eps = sp.symbols('t', real=True), sp.Function('eps')
X, xi, q, Nl = (sp.Function(n) for n in ('X', 'xi', 'q', 'Nlapse'))
sig, V = sp.Function('sigma'), sp.Function('V')

L = (sp.diff(xi(t), t) * sp.diff(X(t), t) / Nl(t)
     - Nl(t) * xi(t) * sig(q(t))
     + sp.diff(q(t), t) ** 2 / (2 * Nl(t))
     - Nl(t) * V(q(t)))

# (A) invariance: delta L == d/dt (eps L)
def delta_scalar(f):
    return eps(t) * sp.diff(f, t)

dL = sp.S(0)
for f in (X(t), xi(t), q(t)):
    df = delta_scalar(f)
    dL += sp.diff(L, f) * df + sp.diff(L, sp.diff(f, t)) * sp.diff(df, t)
dN = sp.diff(eps(t) * Nl(t), t)
dL += sp.diff(L, Nl(t)) * dN
check(sp.simplify(dL - sp.diff(eps(t) * L, t)) == 0,
      "toy is reparametrization invariant: delta L == d/dt(eps L) identically")

# (B) the off-shell Noether identity
def EL(f):
    return sp.diff(L, f) - sp.diff(sp.diff(L, sp.diff(f, t)), t)

E_X, E_xi, E_q = EL(X(t)), EL(xi(t)), EL(q(t))
E_N = sp.diff(L, Nl(t))  # N has no derivative in L
ident = (E_X * sp.diff(X(t), t) + E_xi * sp.diff(xi(t), t) + E_q * sp.diff(q(t), t)
         - Nl(t) * sp.diff(E_N, t))
check(sp.simplify(ident) == 0,
      "OFF-SHELL identity: E_X X' + E_xi xi' + E_q q' - N (E_N)' == 0",
      "=> on ANY solution of the X, xi, q equations -- including the slaved/retarded-data"
      " one -- the constraint E_N is conserved. Conservation is AUTOMATIC once localized:"
      " choosing retarded data selects a SOLUTION, it does not deform the equations."
      " UPGRADES the committed 'conservation NOT-COMPUTED': the trade causality-vs-"
      "conservation is ESCAPED by localization + CTP; the price moves to S5 (fields).")

# ============================================================================
hdr("S5a: LOCALIZATION (rational kernels) -- WHERE THE ADVANCED ADJOINT HIDES")
# ============================================================================
# Local retarded operator L_op (lower-triangular, invertible). Nonlocal functional
#   S_nl = c^T L_op^{-1} J     (a lightcone-integral observable coupled linearly).
# Localized:  S_loc = xi^T (L_op X - J) + c^T X.
l0, l1, l2 = sp.symbols('l0 l1 l2', real=True, nonzero=True)
M3 = 3
L_op = sp.Matrix(M3, M3, lambda i, j: [l0, l1, l2][i - j] if i >= j else 0)
Jv = sp.Matrix(sp.symbols('J0:3', real=True))
cv = sp.Matrix(sp.symbols('c0:3', real=True))
Xv = sp.Matrix(sp.symbols('XX0:3', real=True))
xiv = sp.Matrix(sp.symbols('xx0:3', real=True))

S_loc = (xiv.T * (L_op * Xv - Jv))[0, 0] + (cv.T * Xv)[0, 0]
solX = sp.solve([sp.diff(S_loc, w) for w in xiv], list(Xv), dict=True)[0]
solXi = sp.solve([sp.diff(S_loc, w) for w in Xv], list(xiv), dict=True)[0]

X_sol = sp.Matrix([solX[v] for v in Xv])
xi_sol = sp.Matrix([solXi[v] for v in xiv])
check(sp.simplify(X_sol - L_op.inv() * Jv) == sp.zeros(M3, 1),
      "xi-variation enforces X = L^{-1} J: X is the RETARDED lightcone integral, data SLAVED")
check(sp.simplify(xi_sol + (L_op.T).inv() * cv) == sp.zeros(M3, 1),
      "X-variation gives xi = -(L^T)^{-1} c: the response xi propagates with the ADVANCED"
      " kernel in the naive EL form -- this is exactly where the advanced adjoint hides;"
      " the CTP boundary structure (sf47/sf48) is what re-routes xi_c to retarded")
S_elim = sp.simplify(S_loc.subs(solX))
check(sp.simplify(S_elim - (cv.T * L_op.inv() * Jv)[0, 0]) == 0,
      "eliminating (X, xi) reproduces the nonlocal functional c^T L^{-1} J exactly",
      "=> rational-symbol causal kernel  <=>  FINITE set of auxiliary fields (X, xi)")

# ============================================================================
hdr("S5b: NON-RATIONAL CAUSAL KERNELS = CONTINUUM OF SLAVED FIELDS (spectral rep)")
# ============================================================================
# Memory kernel with Laplace symbol s^(-1/2) (i.e. K(t) = theta(t)/sqrt(pi t)):
# NOT the Green function of any finite-order local operator (non-rational symbol).
# Spectral identity:  integral_0^inf dmu mu^(-1/2)/(s+mu) = pi/sqrt(s)
# i.e. s^(-1/2) = (1/pi) int dmu mu^(-1/2) * [1/(s+mu)]  -- a continuum of FIRST-ORDER
# retarded kernels 1/(s+mu), each localizable by ONE slaved auxiliary pair.
s_, mu_ = sp.symbols('s mu', positive=True)
spec = sp.integrate(1 / (sp.sqrt(mu_) * (s_ + mu_)), (mu_, 0, sp.oo))
check(sp.simplify(spec - sp.pi / sp.sqrt(s_)) == 0,
      "int_0^inf dmu / (sqrt(mu)(s+mu)) == pi/sqrt(s)  (sympy-evaluated)",
      "=> a causal kernel with non-rational symbol is a mass-CONTINUUM of first-order"
      " retarded kernels: localization needs infinitely many slaved fields, not zero."
      " Generic Leg B kernel => MORE field content, never less.")

# ============================================================================
hdr("S6: EVENT-HORIZON FUNCTIONALS -- TELEOLOGY => ADVANCED RESPONSE, NO IN-IN REPAIR")
# ============================================================================
# Discrete: R_i = h * sum_{j>=i} 1/a_j  (comoving future horizon).
h = sp.Symbol('h', positive=True)
av = sp.Matrix(sp.symbols('a1:5', positive=True))
R_h = [h * sum(1 / av[j] for j in range(i, N)) for i in range(N)]

Jac = sp.Matrix(N, N, lambda i, j: sp.diff(R_h[i], av[j]))
future_only = all(Jac[i, j] == 0 for i in range(N) for j in range(i))
nonzero_future = all(Jac[i, j] != 0 for i in range(N) for j in range(i, N))
check(future_only and nonzero_future,
      "delta R_h(t)/delta a(t') has support ONLY on t' >= t (strictly teleological)",
      "continuum form: delta R_h(t)/delta a(t') = -c theta(t'-t)/a(t')^2")

Phi_f, w_f = sp.Function('Phi'), sp.Function('w')
S_h = sum(Phi_f(R_h[i]) * w_f(av[i]) for i in range(N))
E_1 = sp.diff(S_h, av[0])
check(sp.simplify(sp.diff(E_1, av[3])) != 0,
      "EOM at the EARLIEST time depends on a at the LATEST time: ADVANCED response outright",
      "any action containing Phi[R_h] answers perturbations from its future; hyperbolic"
      " initial-value formulation impossible")

print("  [structural] IN-IN NON-REPAIRABILITY: the CTP contour runs over histories on"
      "\n     [t0, t_max]; R_h(t) requires a(t') for ALL t' > t including t' > t_max, so"
      "\n     Phi[R_h] is NOT a functional of contour histories at all. The S3 repair is"
      "\n     therefore UNAVAILABLE: no doubled action exists whose Delta-variation gives"
      "\n     a causal EOM for an event-horizon functional. Teleological subclass CLOSES.")

# dS degeneration: exactly where R_h becomes quasi-local it becomes CONSTANT (Layer A).
tt, tp, H = sp.symbols('t tprime H', positive=True)
Rh_dS = sp.exp(H * tt) * sp.integrate(sp.exp(-H * tp), (tp, tt, sp.oo))  # proper horizon, a=e^{Ht}
check(sp.simplify(Rh_dS - 1 / H) == 0,
      "exact dS: proper event horizon a(t) int_t^inf dt'/a == 1/H == CONSTANT",
      "the 'in dS the horizon is instantaneous' escape (Stone-type) buys locality only at"
      " the fixed point where the functional carries NO z-evolution: Layer A, not Layer C")

# ============================================================================
hdr("S7: EXHAUSTIVE KERNEL-SUPPORT CLASSIFICATION + VERDICT")
# ============================================================================
print(r"""
  Any scalar q[g](x) is classified by the support of delta q(x)/delta g(x'):
  (1) support = {x} (point/quasi-local, incl. derivative-of-delta on the cone vertex)
        => LOCAL curvature invariant => LEG A (constant a0 or environment-dependent;
           SPARC environmental null applies; McVittie needs an H-carrying medium).
  (2) support in J^-(x), kernel = Green fn of a local operator (rational symbol)
        => S5a: finite auxiliary fields (X, xi), Cauchy data SLAVED to zero by CTP
           (sf48); conservation automatic (S4); no free radiative modes.
  (3) support in J^-(x), generic covariant causal kernel (non-rational symbol)
        => S5b: CONTINUUM of slaved fields. Strictly more field content.
  (4) support on the initial slice / asymptotic past average
        => either a CONSTANT of the solution (Layer A only, no z-evolution) or
           explicit dependence on a chosen slice + transported frame = Cauchy data
           + foliation = LEG C.
  (5) support intersecting J^+(x) (event horizons, future averages, boundary terms
      at future infinity)
        => S6: advanced response, no variational or in-in formulation: CLOSED outright.
  The list is exhaustive (supports partition into vertex/past/future/slice components).

  VERDICT -- LEG B: PARTIALLY OPEN AS LITERALLY STATED, CLOSED IN SHARPENED FORM.
  * The teleological subclass (5) closes with NO escape.
  * The retarded subclass (2)-(3) admits the in-in construction, which LITERALLY
    satisfies (i) no new propagating DOF (data slaved, ghost mode projected: sf48),
    (ii) no independent Cauchy data, (iii) no conserved dark charge generically
    (DW's ratio-lock charge came from its mimetic CLOCK -- a Leg C ingredient --
    not from box^-1 itself). So the trichotomy's Leg B closure AS STATED is too
    strong: an escape-construction exists on paper (metric-only in-in retarded
    functional, DW-2009-f(box^-1 R)-type, no clock field).
  * BUT the escape is a dark-FIELD theory in all but name:
      - localization is GENERIC (S5): the H(z)-information is carried into the bound
        system by a nonzero scalar profile X(x) whose gradients and couplings
        gravitate -- an O(1) effective dark stress in the MOND regime by design
        (if the X-sector stress were negligible there, the MOND modification it is
        built to produce would be too);
      - the auxiliary sector contains a negative-energy direction v=(X-xi)/sqrt(2)
        (sf43) kept off only by the slaved-data surface; nonlinear re-excitation
        (gate G3) is OPEN -- the standard failure mode of nonlocal localizations;
      - the in-in construction itself requires a preferred initial slice t_0 and
        state -- Leg C-adjacent structure smuggled in at one point;
      - the ONLY exhibited MOND+a0(z) realization in this class (DW 2026) needed a
        dynamical clock field and pays the conserved-charge price (ratio-lock,
        committed): the paper-escape has never been exhibited as a working theory.
  * CONSEQUENCE (sharpened, and it still flips MUSE the same way): evolving a0(z)
    inside bound systems via Leg B requires a gravitating dark scalar PROFILE --
    slaved or free. "No free dark STATE" is achievable; "no dark FIELD" is not.
    A measured rising a0(z) remains evidence FOR a dark field penetrating bound
    systems, exactly as in the dark-fluid leg. Layer A untouched.
""")

if FAIL:
    print(f"FAILED {len(FAIL)} checks: {FAIL}")
    sys.exit(1)
else:
    print(f"ALL {NCHK[0]} LEG-B CHECKS PASSED.")
    sys.exit(0)
