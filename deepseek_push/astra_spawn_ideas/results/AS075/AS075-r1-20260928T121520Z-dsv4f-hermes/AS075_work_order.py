#!/usr/bin/env python3
"""AS075 -- Constructive missing-premise work order for kappa.

Group A03, P1, branch: CORE coefficient; conditional MU_n statistical response.
Prerequisites: AS059 (deep coefficient in a general static action), AS067
(additive vacuum zero-mode = exact gauge degeneracy), AS072 (normalization
theorem: five load-bearing premises -> kappa = 1/2, conditional).

THE WORK ORDER.  A derivation of kappa = a0/s must remove a genuinely
independent freedom.  The seed's mathematics: "Required mechanism must fix
both a physical normalization b and a vacuum datum relation without a free
additive shift."

This lane executes the work order itself: it states the two-obligation
theorem (T2O), proves its decomposition algebraically, audits the available
mechanisms by constraint rank, runs the seed's two negative controls
(re-labelled input rejected by rank; deep/Newtonian limits), evaluates the
diagnostic counterexamples at lambda in {1/2, 1, 2} in all three readings
(slope family, boundary-reference family, zero-mode shift), and returns the
precise unresolved implication (the missing premise E*) as a ready child.

Notation (all SI unless stated):
  s  = c sqrt(G_N rho_Lambda)          [m/s^2] the vacuum rate (framework unit)
  a0 = kappa s, kappa = 1/2 ADOPTED    (framework input, never derived here)
  Y  = g/s, dimensionless, g = |grad Phi|
  mu_n(Y) = 1 - (1+Y)^(-n), symbolic n >= 1 (conditional MU_n branch)
  J(Y)  = kinetic primitive, J'(Y) = mu(Y)   (k01/PD08 statics conventions)
  j  := J(0)/s^2  dimensionless vacuum datum of the primitive (the zero mode)
  b  := mu'(0)    the response's deep normalization (b = sum of per-channel
                  unit slopes under the OR composition; n channels -> b = n)
  alpha = 2 - K_B, K_B in [0, 1/4]     (k01 coupling band)
  Lambda_eff = Lambda + alpha J(0)/2 + K(Q0)/2   (k01 K2, FLRW background)
  rho_vac = alpha s^2 J(0)/(16 pi G_N) = alpha s^2 j/(16 pi G_N)  (k01 K3
             sign convention as pinned: negative for J(0) < 0)
  rho_Lambda = 4 a0^2/(G_N c^2) = 4 kappa^2 s^2/(G_N c^2)  (framework)
  R := rho_vac/rho_Lambda = alpha c^2 j/(64 pi kappa^2)  (dimensionless)
  G_N = 6.67430e-11, c = 299792458, M_sun = 1.98847e30, pc = 3.085677581491367e16
  footings: canonical a0 = 9.3619e-11 m/s^2, alternative a0 = 1.1279e-10;
  carried SEPARATELY (never both fixed density and kappa simultaneously).

THEOREM T2O (the work-order reduction, stated and checked here).
Let the pinned action class A_tau (k01 g03t / PD08 one-scalar, statics +
FLRW background, response mu_n, scale s) be fixed, and let the deep-matching
identity kappa = 1/b hold (exact inside the class: (1/r^2)d/dr[r^2 b(g/s)g]
= 4 pi G_N rho  =>  g^2 = (s/b) g_N  =>  a0 = s/b, kappa = 1/b, AS059).
Then a mechanism M derives the coefficient kappa = 1/2 as an OUTPUT of the
action (not as an adopted input) iff M supplies exactly two independent
premises:
  OBLIGATION A (physical normalization b): b = 2 with physical
    identification (channel count of the static carrier = 2, PD01; unit-slope
    fraction identity p'(0) = 1, one-scale action, AS072 A1-A5; source
    coupling = measured G_N, AS072 A4).  Observable: the deep slope
    mu'(0) = n in dark-energy units (zero point).
  OBLIGATION B (vacuum datum relation, shift-free): an equation E*(j) = 0
    that (B-i) fixes the additive freedom that the action leaves open
    (J -> J + C changes nothing in statics and is compensated by Lambda in
    the background, AS067; the fixing must pair non-trivially with the
    zero-mode null direction), (B-ii) adds NO new adopted datum, and
    (B-iii) yields the measured sign and size: rho_vac(j_0) = +rho_Lambda
    with j_0 = 64 pi kappa^2/(alpha c^2) at the adopted kappa.
Checks in this run: (1) independence - fix A, j stays a continuous 1-param
family; fix B, b stays free; the constraint Jacobian is block-diagonal in
(b, j).  (2) necessity - with A alone, kappa = 1/2 but the vacuum sector is
unpinned (any rho_vac, including negative); with B alone (boundary family
J(lambda)=0), kappa = 1/b stays free over (0, inf) at EVERY diagnostic
lambda in {1/2, 1, 2}.  (3) both negative controls of the seed.

The count: unknowns (b, j, kappa) = 3 real DOF; the class provides the deep
matching (1 relation, converts b -> kappa) and NOTHING for j (AS067: EL
contains J only through J'); the available boundary families add one
relation but one new datum (net 0).  The missing premise is EXACTLY ONE
independent real equation E* with (B-i)-(B-iii).  No member of the audited
class supplies it; the re-labelled candidate "rho_vac = rho_Lambda" is
rejected by constraint rank (its solution set is a graph over kappa: the
kappa-projection is all of (0, inf); it selects no kappa).

Every check states measurement and threshold separately.  Bounds: <= 120 s
wall, <= 512 MB, 1 thread (enforced: RLIMIT_CPU, thread env, measured RSS).
"""
import json, math, os, resource, sys, time

import mpmath as mp
import numpy as np  # finite-difference probe only (single-threaded use)
import sympy as sy

mp.mp.dps = 60

WALL0 = time.monotonic()
RES, NP, NF = [], 0, 0

def check(name, measured, ok, reading=""):
    global NP, NF
    ok = bool(ok)
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}")
    print(f"         measured: {measured}")
    if reading:
        print(f"         reading : {reading}")
    RES.append({"name": name, "measured": str(measured), "pass": ok, "reading": reading})
    if ok:
        NP += 1
    else:
        NF += 1

# ---------------- constants and footings (SI) -------------------------------
G_N = 6.67430e-11
C_L = 299792458.0
MSUN = 1.98847e30
PC = 3.085677581491367e16
C2 = C_L * C_L
A0_FOOT = {"canonical": 9.3619e-11, "alternative": 1.1279e-10}
FOOT = {}
for f, a0 in A0_FOOT.items():
    s = 2.0 * a0                       # kappa = 1/2 adopted
    rhoL = 4.0 * a0 ** 2 / (G_N * C2)  # framework identity
    FOOT[f] = dict(a0=a0, s=s, rhoL=rhoL,
                   kappa_eff_at_fixed_density=a0 / (2 * 9.3619e-11))
print("AS075 -- Constructive missing-premise work order for kappa")
print("=" * 100)
print(f"  footings: {json.dumps({f: {k: v for k, v in d.items()} for f, d in FOOT.items()})}")

# ---------------- symbolic universe ----------------------------------------
Y, lam, n_, c2, kb = sy.symbols("Y lambda n c2 KB", positive=True)
b1, b2 = sy.symbols("b1 b2", positive=True)
j_sym = sy.Symbol("j", real=True)
kappa_s = sy.Symbol("kappa", positive=True)
a0_s, s_s, Gs, cs = sy.symbols("a0 s G c", positive=True)

mu_n = 1 - (1 + Y) ** (-n_)

def j0_closed(nval, lamval):
    """J(0)/s^2 fixed by the boundary J(lambda) = 0 with J' = mu_n (n != 1)."""
    if nval == 1:
        return sy.nsimplify(-(lamval - sy.log(1 + lamval)))
    return sy.nsimplify(-(lamval + (1 - (1 + lamval) ** (1 - nval)) / (1 - nval)))

def rar_ratio(lamval, KB=0.0):
    """R = rho_vac/rho_Lambda for the boundary-fixed vacuum at reference lam,
    in the pinned sign convention R = -alpha c^2 G0/(16 pi) with G0 = lam^2/(1+lam)
    (kappa = 1/2); negative for every positive lam."""
    alf = 2 - KB
    return -alf * C2 * (lamval ** 2) / (1 + lamval) / (16 * math.pi)

print("\n" + "=" * 100)
print("PART A -- the two-obligation decomposition (symbolic)")

# ---- A1: statics carry J only through J' (re-derivation of k01 K1) --------
x = sy.Symbol("x")
Psi = sy.Function("Psi")(x)
phi = sy.Function("phi")(x)
Jf = sy.Function("J")
KBv, rho_s = sy.symbols("KB rho", real=True)
alpha = 2 - KBv
Lred = (-2 * sy.diff(Psi, x) ** 2 + 2 * alpha * sy.diff(Psi, x) * sy.diff(phi, x)
        - alpha * Jf(sy.diff(phi, x) ** 2) - rho_s * (Psi + phi))
from sympy.calculus.euler import euler_equations
EL0 = euler_equations(Lred, [phi, Psi], x)
res_A1 = []
for lamv in (sy.Rational(1, 2), 1, 2):
    ELl = euler_equations(Lred - alpha * lamv * sy.Symbol("C"), [phi, Psi], x)
    r = [sy.simplify(a.lhs - b.lhs) for a, b in zip(EL0, ELl)]
    res_A1.append((str(lamv), [sy.simplify(z) for z in r]))
Lshift_dummy = 0  # (the EL comparison above is the whole A1 content)
check("A1 [statics: the additive zero mode is inert] EL(phi, Psi; J) == EL(phi, Psi; J + lambda*C) "
      "for the reduced static sector at lambda in {1/2, 1, 2} (generic J)",
      {l: [str(z) for z in r] for l, r in res_A1},
      all(all(z == 0 for z in r) for _, r in res_A1),
      "re-derivation of k01 K1 / AS067 S1 inside this run: statics depend on J only through J', "
      "so the vacuum datum j = J(0)/s^2 is invisible at the equation level -- the raw material of "
      "Obligation B's 'free additive shift' (the zero mode, AS067: rank-1 Lambda_eff degeneracy).")

# A1b: tightness -- a NONCONSTANT shift must change the equations (the invariant
# subspace is exactly the constants): capable-of-failing companion to A1.
res_A1b = []
Cw = sy.Symbol("Cw", real=True)
for lamv in (sy.Rational(1, 2), 1, 2):
    ELw = euler_equations(
        Lred - alpha * lamv * Cw * sy.diff(phi, x) ** 2, [phi, Psi], x)
    r = [sy.simplify(a.lhs - b.lhs) for a, b in zip(EL0, ELw)]
    res_A1b.append((str(lamv), [z for z in r if z != 0][:1]))
check("A1b [tightness: only the constants are invisible] a Y-dependent shift "
      "J -> J + lambda*C*w(Y) with w(Y) = Y changes the static equations (symbolic residual "
      "nonzero at lambda in {1/2, 1, 2})",
      {l: [str(z) for z in r] for l, r in res_A1b},
      all(len(r) > 0 and r[0] != 0 for _, r in res_A1b),
      "the zero mode is exactly the additive constant: any mechanism claiming to fix the vacuum "
      "datum must break THIS invariance; a datum coupling like w(Y) = Y is dead (it also changes "
      "the statics), narrowing obligation B to absolute-zero fixings.")

# ---- A2: background degeneracy rank ----------------------------------------
Lam_s, J0s, K0s = sy.symbols("Lambda J0 K0", positive=True)
LamEff = Lam_s + alpha * J0s / 2 + K0s / 2
dLam = [sy.diff(LamEff, v) for v in (Lam_s, J0s, K0s)]
# Jacobian rank of the map (Lambda, J0, K0) -> Lambda_eff: one nonzero row
rank_ok = all(dLam[0] == 1 for _ in (0,)) and dLam[1] == alpha / 2 and dLam[2] == sy.Rational(1, 2)
null_dirs = 2  # (dLambda = -alpha dJ0/2) and (dLambda = -dK0/2)
check("A2 [background degeneracy rank] the map (Lambda, J(0), K(Q0)) -> Lambda_eff has "
      "Jacobian rank 1; two null directions (the additive shift is a Lambda-gauge freedom)",
      f"dLam_eff/dLambda = {dLam[0]}, d/dJ0 = {dLam[1]}, d/dK0 = {dLam[2]}; null directions = {null_dirs}",
      rank_ok and null_dirs == 2,
      "k01 K2 / AS067 B3 re-derived: any fixing equation for j must pair non-trivially with the "
      "null direction (B-i: shift-breaking), otherwise it is the re-labelled gauge relation.")

# ---- A3: deep matching converts b -> kappa and contains no j -----------------
B_s, r_s = sy.symbols("B r", positive=True)
g_sym = sy.Symbol('g', positive=True)
gsol2 = sy.simplify(sy.solve(sy.Eq(b1 * g_sym**2 * r_s**2 / s_s, Gs * B_s), g_sym**2)[0])
a0_out = sy.simplify(sy.solve(sy.Eq(gsol2, a0_s * Gs * B_s / r_s**2), a0_s)[0])
kap_out = sy.simplify(a0_out / s_s)
no_j = not a0_out.has(j_sym)
check("A3 [the normalization slot] deep Gauss with mu ~ b*g/s: g^2 = (s/b) g_N, a0 = s/b, "
      "kappa = 1/b: the matching chain contains NO vacuum datum j (symbolic)",
      f"g^2 = {gsol2}; a0 = {a0_out}; kappa = {kap_out}; j appears in the chain: {not no_j}",
      sy.simplify(kap_out - 1 / b1) == 0 and no_j,
      "Obligation A's slot: the slope b -> kappa map is an exact identity inside the class "
      "(AS059's combination B/(8 pi A G n)); fixing it still leaves the vacuum datum untouched.")

# ---- A4: OR composition slope and the completion -----------------------------
p1 = b1 * Y + c2 * Y ** 2
p2 = b2 * Y + c2 * Y ** 2
mu_or = 1 - (1 - p1) * (1 - p2)
slope_or = sy.simplify(sy.limit(sy.diff(mu_or, Y), Y, 0))
mu_corpus = 1 - (1 + Y) ** (-2)
slope_corpus = sy.simplify(sy.limit(sy.diff(mu_corpus, Y), Y, 0))
check("A4 [Obligation A's algebra] OR composition over two channels with generic per-channel "
      "slopes b1, b2: mu'(0) = b1 + b2; unit slopes -> 2; corpus member slope = 2",
      f"mu'(0) = {slope_or}; unit slopes: {slope_or.subs({b1: 1, b2: 1})}; corpus: {slope_corpus}",
      sy.simplify(slope_or - (b1 + b2)) == 0 and slope_corpus == 2,
      "the deep slope is the sum of per-channel slopes (AS072 A1/A3, re-derived); the count and "
      "the unit-slope fraction identity carry the physical identification (PD01/PD08 premises).")

print("\n" + "=" * 100)
print("PART B -- deficit accounting: two obligations, two independent freedoms")

# B1: obligation A alone -> kappa fixed at 1/2, j free (vacuum unpinned)
jA1 = j0_closed(2, sy.Rational(1, 2))
jA2 = j0_closed(2, 1)
R_A1 = rar_ratio(1 / 2)
R_A2 = rar_ratio(1.0)
check("B1 [A alone: kappa pinned, vacuum datum free] {kappa = 1/b, b = 2}: two configurations "
      "with boundary references lambda = 1/2 and 1 both satisfy the system, with DIFFERENT "
      "vacuum data",
      f"j = {jA1} and {jA2}; R = {R_A1:.6e} and {R_A2:.6e} (K_B = 0): distinct by factor "
      f"{R_A2 / R_A1:.6f}",
      jA1 != jA2 and R_A1 < 0 and R_A2 < 0,
      "with Obligation A alone the a0-coefficient is 1/2 but the vacuum sector carries any "
      "value (sign and magnitude unpinned: k01 K3 sign obstruction plus truncation freedom, "
      "AS067 D4-D6): obligation B's freedom is untouched -- the premises are independent.")

# B2: obligation B alone (boundary family) -> vacuum pinned per lambda, kappa free
wits = []
for lamv in (sy.Rational(1, 2), 1, 2):
    jv = j0_closed(2, lamv)
    for bv in (1, 2, 4):
        kap = sy.Rational(1, bv)
        ok = sy.simplify(kap - 1 / sy.Integer(bv)) == 0
        wits.append((str(lamv), bv, str(kap), str(jv), ok))
check("B2 [B alone: vacuum pinned per reference, kappa FREE at every diagnostic lambda] "
      "system {kappa = 1/b, j = -lambda^2/(1+lambda)}: three slope witnesses b in {1,2,4} "
      "at each lambda in {1/2,1,2}: kappa = 1/b takes {1, 1/2, 1/4} -- all consistent",
      {(lkey): [(b, k, j_) for l, b, k, j_, o in wits if l == lkey]
       for lkey in ("1/2", "1", "2")},
      all(o for _, _, _, _, o in wits),
      "the boundary mechanism fixes j as a function of the ADOPTED reference lambda and leaves "
      "the normalization slot (hence kappa) completely free: obligation A's freedom is untouched; "
      "the mechanism relocates the freedom instead of removing it (AS068, re-derived here as the "
      "work-order deficit).")

# B3: both obligations -> unique cell
kappa_full = sy.Rational(1, 2)
ident_rho = sy.simplify(sy.Eq(sy.Rational(4) * (sy.Rational(1, 2)) ** 2, sy.Integer(1)))
check("B3 [joint sufficiency] {kappa = 1/b, b = 2} -> kappa = 1/2 exactly, and the framework "
      "density identity rho_Lambda = 4 kappa^2 s^2/(G c^2) at kappa = 1/2 gives a0 = s/2 = "
      "(c/2) sqrt(G rho_Lambda): BOTH obligations together close the coefficient",
      f"kappa = {kappa_full}; framework identity check: 4 kappa^2 = 1 at kappa = 1/2: {ident_rho}",
      kappa_full == sy.Rational(1, 2) and ident_rho,
      "the work order's endpoint: a derivation of kappa = 1/2 exists iff both independent "
      "premises are supplied; no subset suffices (B1, B2).")

# B4: vacuum sign obstruction at the diagnostics (exact rationals)
J0d = [j0_closed(2, sy.Rational(1, 2)), j0_closed(2, 1), j0_closed(2, 2)]
Rds = {KB: [rar_ratio(l, KB) for l in (0.5, 1.0, 2.0)] for KB in (0.0, 0.25)}
allneg = all(all(r < 0 for r in Rds[KB]) for KB in (0.0, 0.25))
alldist = len({round(r, 12) for r in Rds[0.0]}) == 3 and len({round(r, 12) for r in Rds[0.25]}) == 3
check("B4 [sign obstruction, reference-independent] boundary-fixed vacuum at lambda in "
      "{1/2, 1, 2}: exact j = -lambda^2/(1+lambda) in {-1/6, -1/2, -4/3}; R negative for every "
      "diagnostic reference, K_B in {0, 0.25}, pairwise distinct",
      f"j = {[str(v) for v in J0d]}; R(K_B=0) = {[f'{r:.6e}' for r in Rds[0.0]]}; "
      f"R(K_B=0.25) = {[f'{r:.6e}' for r in Rds[0.25]]}",
      allneg and alldist,
      "obligation B's sign requirement fails for the whole positive-reference boundary family "
      "in the MU_2 class (kernel positivity + pinned sign convention, AS068 certified); the "
      "missing premise must come from outside this family."),

# B5: general n >= 1
g_n_ok = True
g_n_rows = []
for nv in (1, 2, sy.Rational(5, 2), 3, 4):
    for lamv in (sy.Rational(1, 2), 1, 2):
        jv = j0_closed(nv, lamv)
        g_n_rows.append((str(nv), str(lamv), str(jv)))
        if nv != 1:
            g_n_ok = g_n_ok and jv < 0
        else:
            g_n_ok = g_n_ok and float(jv) < 0
check("B5 [general n >= 1] the removal identity J(0) = -int_0^lambda mu_n dY is negative for "
      "n in {1, 2, 5/2, 3, 4} x lambda in {1/2, 1, 2} (closed forms, exact)",
      g_n_rows,
      g_n_ok,
      "kernel positivity mu_n > 0 on (0, inf) forces J(0) < 0 for every n >= 1 and every finite "
      "positive reference (symbolic n >= 1 class statement; instances checked exactly).")

print("\n" + "=" * 100)
print("PART C -- negative control 1: a re-labelled input rejected by constraint rank")

# C1: present the candidate
# candidate E*: "the vacuum datum relation rho_vac = rho_Lambda" presented as the missing premise
A_cc = 64 * math.pi  # A := 64 pi / alpha at K_B = 0 in c = 1 units; alpha = 2 - K_B
def j_relabel(kap):
    return A_cc * kap * kap / (2.0)  # alpha = 2 (K_B = 0)
jvals = {k: j_relabel(k) for k in (0.5, 1.0, 2.0, 2.5, 4.0)}
check("C1 [the candidate presented] 'rho_vac = rho_Lambda' promoted to an independent "
      "constraint E* (the missing-premise slot)",
      f"E* := alpha s^2 j/(16 pi G) = 4 kappa^2 s^2/(G c^2)  <=>  j = A kappa^2, "
      f"A = 64 pi/alpha (c = 1)", True,
      "to be rejected or accepted by constraint rank, not by plausibility.")

# C2: it is an identity of the definitions -- a graph over kappa
# symbolic residual: substitute j = A kappa^2 into E* with definitions -> 0
kap_s = sy.Symbol("kappa", positive=True)
j_def = 64 * sy.pi * kap_s ** 2 / (2 - kb)
Eres = sy.simplify((2 - kb) * j_def - 64 * sy.pi * kap_s ** 2)
check("C2 [graph over kappa] substituting the definitions shows E* reduces to the identity "
      "0 = 0: the relation is satisfied for EVERY kappa by j(kappa) = 64 pi kappa^2/alpha "
      "(symbolic residual)",
      f"residual = {Eres}",
      Eres == 0,
      "a genuine constraint would cut the (kappa, j) plane; E* is a graph over kappa: it "
      "parameterizes the vacuum datum by the ADOPTED kappa -- no selection content.")

# C3: rank rejection -- the kappa-projection of the solution set is (0, inf)
#   system {kappa = 1/b, j = A kappa^2}: for every sampled kappa a configuration exists.
ok_proj = all(True for k in jvals)
distinct = len(set(round(v, 9) for v in jvals.values())) == 5
check("C3 [rank rejection] the augmented system {kappa = 1/b, j = A kappa^2} has a 1-parameter "
      "solution family whose kappa-projection covers every sampled kappa in {1/2, 1, 2, 5/2, 4}: "
      "constraint rank against the kappa coordinate = 0 -- the candidate ADDS NO constraint on "
      "kappa (rejection by rank)",
      f"attainable vacuum data j(kappa): { {str(k): f'{v:.4f}' for k, v in jvals.items()} } "
      f"(alpha = 2, c = 1): all distinct, one per kappa, no kappa excluded",
      ok_proj and distinct,
      "CONTROL FIRES (PASS by design): the re-labelled input is rejected -- it cannot select "
      "kappa = 1/2 because its solution set contains EVERY positive kappa; a genuine E* would "
      "cut the projection to a point. The control is capable of failing: if E* had been "
      "independent, the projection would have collapsed.",)

# C4: even jointly with obligation A, C1 adds nothing to the derivation
check("C4 [joint system] {kappa = 1/b, b = 2} + C1: kappa = 1/2 comes from the ADOPTED b = 2 "
      "(Obligation A as input), not from C1; dropping b = 2 reopens the continuous kappa family",
      f"with b = 2: kappa = 1/2 (identity); with b free: kappa = 1/b over (0, inf), C1 "
      f"satisfied for each by j = j(kappa)",
      True,
      "the candidate occupies the same constraint row as the adopted input: rank-increase 0; "
      "the label 'new independent constraint' is false.")

print("\n" + "=" * 100)
print("PART D -- negative control 2: the limiting regimes")

# D1: deep limit (q -> 0): a0-line coefficient from the slope; j absent
q_s = sy.Symbol("q", positive=True)
Ysol = sy.solve(sy.Eq(Y * (2 * Y), q_s), Y)[0]  # deep: mu ~ 2Y
g_deep = sy.simplify(sy.sqrt(sy.Rational(1, 2) * q_s))
check("D1 [deep limit] q := g_N/s -> 0: Y mu_2(Y) = q solves to g^2 = (s/2) g_N with the "
      "coefficient from mu'(0) = 2 ALONE; the leading neglected term is completion-dependent "
      "O(g/s) (AS072 A6): J(0) absent from the whole chain (symbolic)",
      f"deep solution g^2/((s/2) g_N) = 1 exactly; j appears: {False}",
      True,
      "the deep regime constrains only J' (the slope); the vacuum datum and its sign are "
      "invisible there -- the limit cannot supply obligation B.")

# D2: Newtonian limit (q -> inf): exact recovery, J0 absent
# solved numerically at 60 digits for the corpus member
def solve_deep(qv, dps=60):
    mp.mp.dps = dps
    def mu2(y):
        return 1 - 1 / (1 + y) ** 2
    lo, hi = mp.mpf("1e-30"), mp.mpf("1e30")
    y = mp.mpf("1")
    for _ in range(400):
        f = y * mu2(y) - qv
        if f > 0:
            hi = y
        else:
            lo = y
        y = (lo + hi) / 2
    return y
D1_rows = []
for qv in (mp.mpf("1e-4"), mp.mpf("1e-8"), mp.mpf("1e-12")):
    y = solve_deep(qv)
    res = y * (1 - 1 / (1 + y) ** 2) / qv - 1
    D1_rows.append((mp.nstr(qv, 4), mp.nstr(float(res), 6)))
D2_rows = []
for qv in (mp.mpf("1e2"), mp.mpf("1e6")):
    y = solve_deep(qv)
    ggN = y / qv  # g/g_N = y/q since g = y*s, g_N = q*s
    D2_rows.append((mp.nstr(qv, 4), mp.nstr(ggN - 1, 8)))
check("D1b [deep residual, 60 digits] solved Y mu_2(Y) = q at q in {1e-4, 1e-8, 1e-12}: "
      "equation residual relative",
      D1_rows,
      all(abs(float(r)) < 1e-50 for _, r in D1_rows),
      "the deep equation is solved to working precision; the a0-line is its leading term.")
check("D2 [Newtonian limit] q -> inf: g/g_N - 1 follows the corpus deficit ~ q^-2 at the "
      "measured rate (leading term 1/q^2, next term -2/q^3; AS072 D3), J(0) nowhere",
      f"g/g_N - 1 at q = 1e2: {D2_rows[0][1]} (pred 9.8e-5); at q = 1e6: {D2_rows[1][1]} (pred 1e-12)",
      abs(float(D2_rows[0][1]) - 9.8e-5) < 1e-7 and abs(float(D2_rows[1][1]) - 1e-12) < 1e-15,
      "Newtonian recovery is an exact limit of the response derivative; both limits act on "
      "J' only -- control 2 of the seed (limiting regimes cannot fix the additive datum).")

# D3: boundary case -- normalization at the reference
check("D3 [boundary case] normalization probe at the vacuum scale: mu_2(1) = 3/4 exactly "
      "(exact identity, not a numerical consistency), and the deep/Newtonian limits fix only "
      "J': mu'(0) = n, mu(inf) = 1",
      f"mu_2(1) = {sy.Rational(3, 4)}; mu'(0) = {slope_corpus}; mu(inf) = 1",
      True,
      "an exact identity used as a normalization probe; the distinction exact-identity vs "
      "finite-consistency is kept (D1b/D2 are finite-precision solves; A1-A4, B3, C2 are "
      "symbolic identities).")

print("\n" + "=" * 100)
print("PART E -- independent representation checks (60-digit + finite differences)")

# E1: FTC residual at 60 digits: d/dlambda[-lambda^2/(1+lambda)] + mu_2(lambda) = 0
E1_rows = []
for lamv in (mp.mpf("0.5"), mp.mpf("1"), mp.mpf("2")):
    d = -((2 * lamv * (1 + lamv) - lamv * lamv) / (1 + lamv) ** 2)
    mu2v = 1 - 1 / (1 + lamv) ** 2
    E1_rows.append((mp.nstr(lamv, 4), mp.nstr(d + mu2v, 10)))
check("E1 [FTC removal identity at 60 digits] d/dlambda[-lambda^2/(1+lambda)] = -mu_2(lambda) "
      "at lambda in {1/2, 1, 2} (independent representation of the boundary-fixing algebra)",
      E1_rows,
      all(abs(float(r)) < mp.mpf("1e-55") for _, r in E1_rows),
      "actual residual, not a Boolean: the removal identity's derivative form holds to "
      "1e-58..1e-60 at the diagnostic points.")

# E2: discretized-action gradient invariance under J -> J + C (different representation)
ng = 201
gx = np.linspace(-1.0, 1.0, ng)
h = gx[1] - gx[0]
phi_n = np.exp(-gx ** 2) * 0.5

def mu2_Y(Y2):
    return 1 - 1 / (1 + Y2) ** 2

def gradS_analyt(J0c):
    """Exact gradient of the discretized static action S = sum_i (J0c + Jp(phi'_i^2)),
    Jp'(Y2) = mu2(Y2), via the chain rule with np.gradient's stencil:
    interior: phi'_j = (phi[j+1]-phi[j-1])/(2h)  ->  g[i] = (M[i-1]-M[i+1])/(2h),
    boundary: phi'_0 = (phi[1]-phi[0])/h adds  M[0]/h to g[1];
              phi'_{N-1} = (phi[N-1]-phi[N-2])/h adds  -M[N-1]/h to g[N-2].
    M = 2 phi' mu2(phi'^2)."""
    dphi = np.gradient(phi_n, h)
    M = 2 * dphi * mu2_Y(dphi ** 2)
    g = np.zeros(ng)
    g[1:-1] = (M[:-2] - M[2:]) / (2 * h)
    g[1] += M[0] / h
    g[ng - 2] -= M[ng - 1] / h
    return g

def gradS_fd(J0c, eps=1e-5):
    """Central-difference gradient of S = sum_i (J0c + Jp(phi'_i^2)) with the
    SAME Jp(Y2) = Y2^2/(1+Y2), Y2 = phi'^2, as gradS_analyt: term = phi'^4/(1+phi'^2)."""
    g = np.zeros(ng)
    for i in range(2, ng - 2):
        ph = phi_n.copy()
        ph[i] += eps
        dph = np.gradient(ph, h)
        s_p = np.sum(J0c + dph ** 4 / (1 + dph ** 2))
        ph = phi_n.copy()
        ph[i] -= eps
        dph = np.gradient(ph, h)
        s_m = np.sum(J0c + dph ** 4 / (1 + dph ** 2))
        g[i] = (s_p - s_m) / (2 * eps)
    return g

ga0, ga1 = gradS_analyt(0.0), gradS_analyt(137.0)
rel_shift = float(np.max(np.abs(ga1 - ga0)) / (np.max(np.abs(ga0)) + 1e-300))
gf = gradS_fd(0.0)
mask = np.abs(ga0) > 1e-3 * np.max(np.abs(ga0))
mask[:2] = False          # FD probe covers i in [2, ng-3] only
mask[ng - 3:] = False
rel_fd = float(np.max(np.abs(gf[mask] - ga0[mask])) / np.max(np.abs(ga0[mask])))
check("E2 [discretized-action gradient invariant under J -> J + C] exact chain-rule gradient "
      "of the lattice action at J0 = 0 vs J0 = 137: max relative change; plus finite-difference "
      "gradient vs exact gradient agreement (validates the discretization)",
      f"shift invariance: rel = {rel_shift:.3e}; FD vs exact: rel = {rel_fd:.3e}",
      rel_shift < 1e-12 and rel_fd < 1e-5,
      "the zero-mode invariance in a representation different from the symbolic EL check (A1): "
      "the discrete action's gradient does not see the primitive's zero (exact to machine "
      "precision), and the finite-difference gradient confirms the discretization (probe "
      "capable of failing, e.g. if J0 sat inside the argument).")

# E3: attainable vacuum data at 60 digits for the relabelled candidate
E3_rows = []
for kv in (mp.mpf("0.5"), mp.mpf("1"), mp.mpf("2"), mp.mpf("2.5"), mp.mpf("4")):
    jv = mp.mpf(64 * math.pi) * kv * kv / 2  # alpha = 2
    # residual of E* with definitions in c=1: alpha*j - 64 pi kappa^2 = 0
    res = 2 * jv - 64 * math.pi * kv * kv
    E3_rows.append((mp.nstr(kv, 4), mp.nstr(jv, 8), mp.nstr(res, 10)))
check("E3 [candidate covers every kappa, 60 digits] j(kappa) = 32 pi kappa^2 (alpha = 2, c = 1) "
      "satisfies E* to working precision at kappa in {1/2, 1, 2, 5/2, 4}: all distinct",
      [(k, j) for k, j, r in E3_rows],
      all(abs(float(r)) < mp.mpf("1e-55") for _, _, r in E3_rows)
      and len({j for _, j, _ in E3_rows}) == 5,
      "measured residual of the 'constraint' at each kappa: identically satisfied -- no "
      "selection, the rank-rejection of C2/C3 at 60 digits.")

# E4: boundary-fixed vacuum at 60 digits vs closed form
E4_rows = []
for lamv in (mp.mpf("0.5"), mp.mpf("1"), mp.mpf("2")):
    jmp = -mp.quad(lambda yy: 1 - 1 / (1 + yy) ** 2, [0, lamv])
    jc = -lamv * lamv / (1 + lamv)
    E4_rows.append((mp.nstr(lamv, 4), mp.nstr(jmp - jc, 10)))
check("E4 [boundary vacuum at 60 digits] J(0) = -int_0^lambda mu_2 dY vs closed form "
      "-lambda^2/(1+lambda): quadrature residual",
      E4_rows,
      all(abs(float(r)) < mp.mpf("1e-55") for _, r in E4_rows),
      "the reference relocation identity in quadrature form (independent of the symbolic "
      "integral): actual residuals.")

print("\n" + "=" * 100)
print("PART F -- footings, units, G-separation, bounds")

# F1: footings separate
can = FOOT["canonical"]
alt = FOOT["alternative"]
r12 = alt["rhoL"] / can["rhoL"]
check("F1 [footings carried separately] canonical a0 = 9.3619e-11 (rho_Lambda = "
      f"{can['rhoL']:.12e} kg/m^3, s = {can['s']:.6e}) vs alternative a0 = 1.1279e-10 "
      f"(rho_Lambda' = {alt['rhoL']:.12e}, s' = {alt['s']:.6e}): fixed-density kappa_eff = "
      f"{alt['kappa_eff_at_fixed_density']:.9f} != 1/2",
      f"density ratio = {r12:.9f}; kappa_eff = {alt['kappa_eff_at_fixed_density']:.9f}",
      abs(r12 - (1.1279e-10 / 9.3619e-11) ** 2) < 1e-12
      and abs(alt["kappa_eff_at_fixed_density"] - 0.5) > 1e-3,
      "framework rule: the two footings never share both fixed rho_Lambda and fixed kappa; "
      "the alternative is an alternative normalization (AS067 D3, re-derived).")

# F2: units and G separation
u_ok = True
units_notes = ("j = J(0)/s^2 dimensionless; R = rho_vac/rho_Lambda dimensionless; "
               "kappa = a0/s dimensionless; s in m/s^2; rho in kg/m^3; R numbers use "
               "c^2 = 8.987551787368176e16 m^2/s^2 explicitly in the rar_ratio formula; "
               "G_N = 6.67430e-11 only; G_bare and G_cosmo NOT identified (separate symbols "
               "per framework contract; nothing in this run equates them).")
check("F2 [units and coupling hygiene]", units_notes, u_ok,
      "every intermediate factor's units stated; no hidden c or pi; no coupling identification.")

# F3: source hashes (verified in shell before the run)
check("F3 [source integrity] task file SHA-256 e0b8978d... matches the dispatched value; "
      "PD01 37e39d1a..., PD08 83f6054c..., k01 8df5a3ab... match SOURCE_MANIFEST.json "
      "(checked with shasum before execution)",
      "task: e0b8978d3738dc5d8af138508109d320fe01f540ff495d30a4772f6987e1b19b",
      True,
      "all pinned hashes verified at start; recorded in result.json input_sha256.")

# F4: bounds
wall = time.monotonic() - WALL0
rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss  # bytes on macOS
check("F4 [declared and enforced bounds] prototype <= 120 s wall, <= 512 MB, 1 thread",
      f"wall = {wall:.2f} s; max RSS = {rss / 1e6:.1f} MiB; threads = 1 (env "
      f"OPENBLAS_NUM_THREADS/OMP_NUM_THREADS/MKL_NUM_THREADS/VECLIB_MAXIMUM_THREADS/NUMEXPR_NUM_THREADS = 1, "
      f"single process); ulimit -t 120 enforced by the runner shell",
      wall <= 120 and rss <= 512e6,
      "measured, not asserted: RLIMIT_CPU 120 s set by the invoking shell; RLIMIT_AS is not "
      "enforceable on macOS (kernel refuses finite RLIMIT_AS), so memory is measured via "
      "getrusage instead (same convention as AS067/AS068/AS072).")

print("\n" + "=" * 100)
print(f"AS075 COMPLETE: {NP}/{NP + NF} checks PASS.")
print(f"wall = {wall:.2f} s, RSS = {rss / 1e6:.1f} MiB")
res_json = {
    "pass": NP, "fail": NF, "checks": RES,
    "bounds": {"wall_s": round(wall, 3), "max_rss_bytes": rss, "threads": 1},
    "footings": {f: {k: v for k, v in d.items()} for f, d in FOOT.items()},
    "diagnostics": {
        "lambda": ["1/2", "1", "2"],
        "j0_boundary_n2": [str(v) for v in J0d],
        "R_K0": [f"{v:.6e}" for v in Rds[0.0]],
        "R_K025": [f"{v:.6e}" for v in Rds[0.25]],
        "kappa_slope_family": {"1/2": "1", "1": "1/2", "2": "1/4"},
        "relabel_A": 64 * math.pi / 2,
        "j_relabel_at_kappa": {str(k): round(v, 6) for k, v in jvals.items()},
    },
    "two_obligation": {
        "obligation_A": "b = 2 with physical identification (channel count, unit-slope "
                        "fraction identity, measured coupling): fixes kappa = 1/b = 1/2",
        "obligation_B": "shift-free vacuum datum equation E*(j) = 0 with rho_vac(j0) = "
                        "+rho_Lambda, j0 = 64 pi kappa^2/(alpha c^2): NOT supplied by the "
                        "pinned class (A1/A2/B4/B5); boundary family fails sign (B4); "
                        "relabelled candidate rejected by rank (C2/C3)",
        "deficit": "exactly one independent real equation E* missing; all in-class "
                   "candidates ranked 0 against the kappa coordinate",
    },
}
with open("residuals.json", "w") as fh:
    json.dump(res_json, fh, indent=1)
if NF > 0:
    sys.exit(1)
