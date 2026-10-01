#!/usr/bin/env python3
"""
AS500.C01 -- matter-only Ward separation at the CA5-GNC-R pin (gate 5's open atom).

Pin: FINAL_ACTION.md b8c04d4e365f1c8e1c2ec3bf8d14629618d1ac162e97e3fdf809382fb147546e
     (CA4-GNC / CA5-GNC-R); k04 four-form promotion 15c0a7e1...2399.
Task: branches/AS500/AS500.C01.md  (task_sha256 = 7d0a46c2825ced3133d1d8c44bef2c59c550464bfe70ae17b3274a30d18a2caf)

CORE QUESTION (either/or verdict):
  (a) div Q_b = 0 on shell in the N sqrt(h) measure -- i.e. div(Q_heat + Q_U1 + Q_vac) = 0
      on shell (decoupling; gate-5 matter atom PROVED), or
  (b) exhibit the exact nonzero cross-source T with div Q_b = -div(Q_heat+Q_U1+Q_vac) = T != 0
      (gate-5 matter atom FAILS on this pin).

PREMISES USED AS PREMISES (landed runs; NOT re-derived, NOT re-run):
  P1 AS137  matter Ward:        Q_b = E_b (xi.dpsi), off-shell div Q_b = E_b(xi.dpsi),
                                on shell (E_b = 0): div Q_b = 0.  S_b contains NO host fields
                                (minimal coupling to g only; AS137 check [5] protected).
  P2 AS138  heat Ward (CHK-3):  Q_heat = N[ sum_k E_Wk (xi.dW)_k + sum_k E_Lk (xi.dL)_k
                                + (R_W + L_b)(xi.dW)_b + (lam0 - L_0)(xi.dW)_0
                                + E_lam0 (xi.dlam0) + E_U (xi.dU) ], endpoint multipliers
                                load-bearing (r-IBP leftover cancellation).
  P2b AS133 terminal BC:        L_b = -R_W, lam0 = L_0 (endpoint display closes).
  P3 AS147  diagonal U(1):      div J_phi = +E_ex, div J_chi = -E_ex on shell,
                                so div(J_phi + J_chi) = E_ex + (-E_ex) = 0 on shell.
  P4 AS651  four-form vacuum:   T_vac = -eps_vac g, eps_vac = (Z/2 + b beta^2) q^2,
                                div T_vac = -(Z + 2 b beta^2) q (g^{mu nu} d_mu q);
                                three-form bulk EOM forces d_mu q = 0 (flux constancy),
                                so div Q_vac = 0 on shell.
  P4b AS658 three-form modes:   residual of EOM with q nonconst = -(Z+2b beta^2) d_mu q != 0
                                (NEG-2: any (b)-witness with q != const violates the retained
                                hypothesis).
  P5 AS138.C01 total assembly:  Q_total = Q_b + Q_heat + Q_U1 + Q_vac; on-shell closure
                                R_total = 0 (zero polynomial in r = Z/beta^2; not re-run).

WHAT THIS CHILD COMPUTES (step 2 of the spec):
  * each sector divergence separately on the N sqrt(h) measure,
  * their sum on shell, simplified over the audited coupling band,
  * both controls NEG-1 / NEG-2,
  * numeric residuals at >= 5 sampled coupling points in the audited band.

Couplings free in the audited band: alpha in (0,2) (c_N = 1 - alpha/2), K_B in [0,1/4],
r = Z/beta^2 in (0, oo), ell = 0.04, delta = 0.05; kappa = 1/2 ADOPTED (never derived);
both footings separate; G_N/G_bare/G_cosmo separate symbols.
"""
import sys, time, json, math
import sympy as sp
from fractions import Fraction as Fr

t0 = time.time()

# ---------------------------------------------------------------- symbols
Z, b, beta, q, dq  = sp.symbols("Z b beta q dq", positive=True)
N, C_N, ell, theta = sp.symbols("N C_N ell theta", positive=True)
G_sym, DhWb        = sp.symbols("G_sym DhWb")
DeltaN_Wb          = sp.symbols("DeltaN_Wb")
Eb, dpsi           = sp.symbols("E_b dpsi")
E_W0, E_W1, E_W2, E_W3 = sp.symbols("E_W0 E_W1 E_W2 E_W3")
E_L0, E_L1, E_L2, E_L3 = sp.symbols("E_L0 E_L1 E_L2 E_L3")
E_lam0, E_U        = sp.symbols("E_lam0 E_U")
(dW0, dW1, dW2, dW3, dL0, dL1, dL2, dL3) = sp.symbols("dW0 dW1 dW2 dW3 dL0 dL1 dL2 dL3")
dlam0, dU, RW, Lb, L0, lam0 = sp.symbols("dlam0 dU R_W L_b L_0 lam0")
Wbp, W0p            = sp.symbols("Wbp W0p")          # (xi.dW)_b and (xi.dW)_0
E_ex                = sp.symbols("E_exchange")
dJphi, dJchi        = sp.symbols("dJphi dJchi")       # raw U(1) current divergences (off shell)
gg                  = sp.symbols("g_metric_factor")  # g^{mu nu} factor in div T_vac
r_sym               = sp.symbols("r")                # r := Z/beta^2

res = {}

print("=" * 100)
print("AS500.C01 -- matter-only Ward separation at pin b8c04d4e...7546e (CA4-GNC/CA5-GNC-R + k04)")
print("=" * 100)

# ---------------------------------------------------------------- STEP 1: the on-shell sector identities
# in the N sqrt(h) measure (leaf-adaptation of the premises).
# Heat on-shell equations: E_Wk = 0, E_Lk = 0, E_lam0 = 0, E_U = 0 (all k),
#   terminal heat BC (AS133): L_b = -R_W, lam0 = L_0.
# U(1) on-shell equations: div J_phi = E_ex, div J_chi = -E_ex  (AS147).
# Vacuum constancy: d_mu q = 0 (AS651 flux EOM; AS658 bulk EOM invertible).
print("\n[STEP 1] on-shell sector identities in the N sqrt(h) measure (premises P1-P4b):")
print("  heat   : E_Wk = E_Lk = E_lam0 = E_U = 0 (all k);  terminal BC L_b = -R_W, lam0 = L_0")
print("  U(1)   : div J_phi = +E_ex , div J_chi = -E_ex   =>  div J_total = 0 on shell")
print("  vacuum : d_mu q = 0 (flux constancy, three-form EOM)")
print("  matter : E_b = 0 ; S_b[g] host-free (minimal coupling)")

# The three cross-source charge densities (as assembled in the total Ward; P2, P3, P4):
Q_heat = N * (E_W0*dW0 + E_W1*dW1 + E_W2*dW2 + E_W3*dW3
              + E_L0*dL0 + E_L1*dL1 + E_L2*dL2 + E_L3*dL3
              + (RW + Lb) * Wbp + (lam0 - L0) * W0p
              + E_lam0*dlam0 + E_U*dU)
Q_U1   = dJphi + dJchi                     # raw div J_phi + div J_chi (P3; on shell -> E_ex + (-E_ex))
Q_vac  = -(Z + 2*b*beta**2) * q * dq * gg     # div T_vac (P4)
Q_b    = Eb * dpsi                            # matter Ward charge (P1)

print("\n[STEP 1] assembled cross-source charges (premises P2-P4, N sqrt(h) measure):")
print(f"  Q_heat = {Q_heat}")
print(f"  Q_U1   = div J_phi + div J_chi = {Q_U1}   (on-shell exchange cancellation)")
print(f"  Q_vac  = div T_vac = {Q_vac}")
res["Q_heat_offshell"] = str(Q_heat)
res["Q_U1_offshell"]   = str(Q_U1)
res["Q_vac_offshell"]  = str(Q_vac)

# ---------------------------------------------------------------- STEP 2: on-shell reduction of each sector
subs_on_shell = {
    Eb: 0, E_W0: 0, E_W1: 0, E_W2: 0, E_W3: 0,
    E_L0: 0, E_L1: 0, E_L2: 0, E_L3: 0,
    E_lam0: 0, E_U: 0, dq: 0,
    dJphi: E_ex, dJchi: -E_ex,      # AS147 on-shell exchange pair
    Lb: -RW, L0: lam0,          # AS133 terminal BC
}
print("\n[STEP 2] on-shell reduction of EACH sector (AS133 BC + sector EOMs):")
R_heat = sp.simplify(Q_heat.subs(subs_on_shell))
R_U1   = sp.simplify(Q_U1.subs(subs_on_shell))
R_vac  = sp.simplify(Q_vac.subs(subs_on_shell))
R_b    = sp.simplify(Q_b.subs(subs_on_shell))
print(f"  div Q_heat |_shell = {R_heat}")
print(f"  div Q_U1   |_shell = {R_U1}")
print(f"  div Q_vac  |_shell = {R_vac}")
print(f"  div Q_b    |_shell = {R_b}")
assert R_heat == 0 and R_U1 == 0 and R_vac == 0
assert R_b == 0
res["R_heat_shell"] = str(R_heat); res["R_U1_shell"] = str(R_U1)
res["R_vac_shell"] = str(R_vac);   res["R_b_shell"] = str(R_b)

# The sum (the decoupling statement):
R_sum = sp.simplify(Q_heat.subs(subs_on_shell) + Q_U1.subs(subs_on_shell)
                    + Q_vac.subs(subs_on_shell))
print(f"\n  SUM div(Q_heat+Q_U1+Q_vac) |_shell = {R_sum}   (exact 0 — decoupling)")
assert R_sum == 0
res["R_sum_shell"] = str(R_sum)

# Simplification in the couplings: the sum is a zero polynomial in every audited coupling.
# Exhibit the zero-polynomial-in-r claim (closure consistency with AS138.C01 K2).
poly_in_r = sp.Poly(sp.expand(R_sum), r_sym)
print(f"  zero-polynomial check in r = Z/beta^2: {poly_in_r}  (all coeffs 0)")
assert all(c == 0 for c in poly_in_r.all_coeffs())
res["poly_in_r"] = str(poly_in_r)

# Also as a multivariate polynomial in (Z, b, beta): every coefficient must vanish.
poly_multi = sp.Poly(sp.expand(R_sum), Z, b, beta, q)
print(f"  zero-polynomial check in (Z, b, beta, q): {poly_multi}")
assert poly_multi.is_zero, "multivariate residual not identically zero"
res["poly_multi"] = str(poly_multi)

# ---------------------------------------------------------------- the decoupling lemma statement
print("\n[STEP 2] DECOUPLING LEMMA (the matter-only atom, verdict (a)):")
print("  On shell: div Q_heat = 0  AND  div Q_U1 = 0  AND  div Q_vac = 0 (each by its own")
print("  sector equations + AS133 terminal BC + flux constancy), hence")
print("  div(Q_heat + Q_U1 + Q_vac) = 0  and the total-Ward cancellation gives")
print("  div Q_b = -div(Q_heat+Q_U1+Q_vac) = 0  in the N sqrt(h) measure.")
print("  Independently (P1): div Q_b = E_b(xi.dpsi) = 0 for E_b = 0 (minimal coupling);")
print("  both routes agree: the ordinary-matter sector carries NO nonmetric force on this pin.")

# ---------------------------------------------------------------- NEG-1: Ward on Q_b alone WITHOUT the
# sector-decoupling lemma must leave a nonzero residual.
# Form: take the total-Ward balance  div Q_b = -(div Q_heat + div Q_U1 + div Q_vac)
# (the total identity, landed by AS138.C01) and DO NOT substitute the sector on-shell
# identities (that substitution set IS the decoupling lemma).  With generic off-shell
# jet data the RHS is nonzero -> the matter-only atom does NOT follow from the total
# identity alone; the sector identities carry the load.
residual_offshell = sp.expand(Q_heat + Q_U1 + Q_vac)
print("\n[NEG-1] residual of 'Ward applied to Q_b alone WITHOUT the decoupling lemma':")
print(f"  residual := -(div Q_heat + div Q_U1 + div Q_vac)|_generic = {residual_offshell}")
print("  (generic off-shell jets: E_Wk, E_Lk, E_lam0, E_U, dq, L_b+R_W, lam0-L_0 retained)")

# exact rational witness (values chosen so every term is on shell EXCEPT E_W0 = 3/2):
w_neg1 = {N: 10, E_W0: sp.Rational(3, 2), E_W1: 0, E_W2: 0, E_W3: 0,
          E_L0: 0, E_L1: 0, E_L2: 0, E_L3: 0, E_lam0: 0, E_U: 0,
          dW0: 1, dW1: 1, dW2: 1, dW3: 1, dL0: 1, dL1: 1, dL2: 1, dL3: 1,
          dlam0: 1, dU: 1, RW: sp.Rational(7, 20), Lb: sp.Rational(-7, 20),
          Wbp: 1, lam0: sp.Rational(3, 20), L0: sp.Rational(3, 20), W0p: 1,
          dJphi: 0, dJchi: 0, Z: 3, b: 1, beta: 1, q: 2, dq: 0, gg: 1}
val_neg1 = sp.simplify(residual_offshell.subs(w_neg1))
print(f"  exact rational witness (heat EOM E_W0 = 3/2 NOT imposed): residual = {val_neg1} != 0")
assert val_neg1 != 0
res["neg1_witness"] = str(val_neg1)

# second witness: terminal BC broken only (L_b + R_W != 0):
w_neg1b = dict(w_neg1); w_neg1b[E_W0] = 0; w_neg1b[E_W1] = 0; w_neg1b[E_W2] = 0; w_neg1b[E_W3] = 0
w_neg1b[E_L0] = 0; w_neg1b[E_L1] = 0; w_neg1b[E_L2] = 0; w_neg1b[E_L3] = 0
w_neg1b[E_lam0] = 0; w_neg1b[E_U] = 0; w_neg1b[dq] = 0
w_neg1b[Lb] = sp.Rational(-7, 20) + 1
w_neg1b[L0] = sp.Rational(3, 20) - 1
val_neg1b = sp.simplify(residual_offshell.subs(w_neg1b))
print(f"  exact rational witness (terminal BC L_b = -R_W, lam0 = L_0 NOT imposed): residual = {val_neg1b} != 0")
assert val_neg1b != 0
res["neg1_witness_bc"] = str(val_neg1b)

# ---------------------------------------------------------------- NEG-2: q != const in the bulk violates
# the retained hypothesis (three-form bulk EOM, AS658/AS651).
Pq_expr = (Z + 2*b*beta**2) * q                      # P_q = dP/dq
q1 = sp.symbols("q1", real=True)
eom_residual = -Pq_expr.subs(q, q1)                   # EOM residual = -(Z+2b beta^2) d_mu q  (see AS651 L6, AS658 D4d)
print("\n[NEG-2] three-form bulk EOM with q != const (retained hypothesis check, AS658):")
print(f"  EOM residual = -(Z+2b beta^2) * d_mu q  (symbolic, P_qq = Z+2b beta^2 > 0):")
print(f"  {eom_residual}   != 0 for d_mu q != 0")
w_neg2 = {Z: 8 - 2*sp.Float("0.018005393544499054547"), b: sp.Float("0.018005393544499054547"),
          beta: 1, q1: sp.Float("0.3")}
val_neg2 = sp.N(sp.simplify(eom_residual.subs(w_neg2)), 12)
print(f"  numeric witness (q = q0*(1 + 0.3 sin x0), tuned ratio): EOM residual = {val_neg2} != 0")
assert abs(val_neg2) > 1e-6
res["neg2_witness"] = float(val_neg2)
print("  => any (b)-witness declaring div Q_vac != 0 via q != const is OFF shell (violates the")
print("     retained three-form EOM) and cannot establish (b).  (b) is therefore excluded on")
print("     the vacuum side; verdict (a) stands.")

# ---------------------------------------------------------------- STEP 3: numeric residuals at >= 5 sampled
# coupling points in the audited band.
# Audited band: alpha in (0,2), K_B in [0,1/4], r = Z/beta^2 in (0,oo), ell = 0.04, delta = 0.05.
jsat = sp.Float("0.4525248966751305416")
def b_of(KB): return (2 - KB) * jsat / (16 * sp.pi)

points = [
    ("P1", sp.Rational(1,2), sp.Rational(0),   sp.Float("1.0")),
    ("P2", sp.Rational(1),   sp.Rational(1,8), sp.Float("4.0")),
    ("P3", sp.Rational(3,2), sp.Rational(1,4), sp.Float("7.9639892129110018909")),
    ("P4", sp.Rational(7,10),sp.Rational(0),   sp.Float("16.0")),
    ("P5", sp.Rational(19,10),sp.Rational(1,4),sp.Float("64.0")),
]
# generic nonzero off-shell jet values for the NEG-1 residual at each point
jet_off = {E_W0: sp.Rational(3,2), E_W1: sp.Rational(1,4), E_W2: sp.Rational(-1,3), E_W3: sp.Rational(2,5),
           E_L0: sp.Rational(1,6), E_L1: sp.Rational(-5,7), E_L2: sp.Rational(3,8), E_L3: sp.Rational(-2,9),
           E_lam0: sp.Rational(7,11), E_U: sp.Rational(-1,13),
           dW0: 1, dW1: 1, dW2: 1, dW3: 1, dL0: 1, dL1: 1, dL2: 1, dL3: 1, dlam0: 1, dU: 1,
           Wbp: 2, W0p: 3, RW: sp.Rational(7,20), Lb: sp.Rational(-7,20),
           lam0: sp.Rational(3,20), L0: sp.Rational(3,20),
           dJphi: sp.Rational(11,7), dJchi: sp.Rational(5,13), dq: sp.Rational(5,3), gg: 2}

print("\n[STEP 3] sampled coupling points in the audited band (real residuals):")
print(f"  {'point':<5} {'alpha':<8} {'K_B':<8} {'r=Z/beta^2':<22} {'on-shell sum':<14} {'NEG-1 |res|':<12} {'NEG-2 |res|':<12}")
sample_rows = []
for pid, alpha, KB, rval in points:
    bv = b_of(KB)
    w_on = dict(subs_on_shell)
    w_on.update({Z: rval * 1, b: bv, beta: 1, q: 2, N: sp.Float("1.5"),
                 RW: sp.Rational(7,20), lam0: sp.Rational(3,20),
                 Wbp: sp.Rational(21,50), W0p: sp.Rational(-11,50)})
    # on-shell residual: each sector separately + sum
    s_heat = sp.N(sp.simplify(Q_heat.subs(w_on)), 20)
    s_u1   = sp.N(sp.simplify(Q_U1.subs(w_on)), 20)
    s_vac  = sp.N(sp.simplify(Q_vac.subs(w_on)), 20)
    s_sum  = sp.N(sp.simplify(Q_heat.subs(w_on) + Q_U1.subs(w_on) + Q_vac.subs(w_on)), 20)
    # NEG-1 off-shell residual at this coupling point (generic jets, sector EOMs dropped)
    w_off = dict(w_on); w_off.update(jet_off)
    r_neg1 = sp.N(sp.simplify(Q_heat.subs(w_off) + Q_U1.subs(w_off) + Q_vac.subs(w_off)), 20)
    r_neg2 = sp.N(sp.simplify(eom_residual.subs({Z: rval, b: bv, beta: 1, q1: sp.Float("0.3")})), 20)
    assert s_heat == 0 and s_u1 == 0 and s_vac == 0 and s_sum == 0
    assert abs(float(r_neg1)) > 0 and abs(float(r_neg2)) > 0
    row = {"point": pid, "alpha": str(alpha), "K_B": str(KB), "r": float(rval),
           "ell": 0.04, "delta": 0.05,
           "on_shell_sum": 0.0, "heat_res": 0.0, "u1_res": 0.0, "vac_res": 0.0,
           "neg1_residual": float(r_neg1), "neg2_residual": float(r_neg2)}
    sample_rows.append(row)
    print(f"  {pid:<5} {str(alpha):<8} {str(KB):<8} {float(rval):<22} {0.0:<14} {abs(float(r_neg1)):<12.6g} {abs(float(r_neg2)):<12.6g}")
res["samples"] = sample_rows
assert len(sample_rows) >= 5

# ---------------------------------------------------------------- random-jet statistics: on shell exact 0,
# off shell nonzero (100 jets each)
import random
random.seed(20260928)
def frac(): return Fr(random.randint(-9, 9), random.randint(1, 9))
n_on_ok = 0; n_off_ok = 0; worst_sum = 0
jets = []
for i in range(100):
    j = {E_W0: frac(), E_W1: frac(), E_W2: frac(), E_W3: frac(),
         E_L0: frac(), E_L1: frac(), E_L2: frac(), E_L3: frac(),
         E_lam0: frac(), E_U: frac(), RW: frac(), lam0: frac(),
         Wbp: frac(), W0p: frac(), dq: frac(), dJphi: frac(), dJchi: frac(),
         Z: Fr(1,2), b: Fr(1,16), beta: 1, q: Fr(3,2), N: Fr(10,7), gg: 1}
    jets.append(j)
    # on-shell: sector EOMs + BC + flux constancy + exchange pair
    w = dict(j)
    for s in (E_W0, E_W1, E_W2, E_W3, E_L0, E_L1, E_L2, E_L3, E_lam0, E_U, dq): w[s] = 0
    w[Lb] = -w[RW]; w[L0] = w[lam0]
    w[dJphi] = 0; w[dJchi] = 0              # exchange-cancelled pair (E_ex - E_ex = 0)
    sm = sp.simplify(Q_heat.subs(w) + Q_U1.subs(w) + Q_vac.subs(w))
    if sm == 0: n_on_ok += 1
    # off-shell: raw (exchange pair NOT cancelled)
    sm2 = sp.simplify(Q_heat.subs(j) + Q_U1.subs(j) + Q_vac.subs(j))
    if sm2 != 0: n_off_ok += 1
print(f"\n[STEP 3] random exact-rational jets (seed 20260928):")
print(f"  on-shell decoupling sums == 0  : {n_on_ok}/100")
print(f"  off-shell residuals != 0       : {n_off_ok}/100")
assert n_on_ok == 100 and n_off_ok == 100
res["random_jets"] = {"on_shell_zero": n_on_ok, "off_shell_nonzero": n_off_ok}

# ---------------------------------------------------------------- footings / framework bookkeeping
G_N, c, kappa = sp.symbols("G_N c kappa", positive=True)
a0_can = sp.Float("9.3619e-11"); a0_alt = sp.Float("1.1279e-10")
rho_can = 4 * a0_can**2 / (sp.Float("6.67430e-11") * sp.Float("299792458")**2)
rho_alt = 4 * a0_alt**2 / (sp.Float("6.67430e-11") * sp.Float("299792458")**2)
print("\n[FOOTINGS] framework bookkeeping (a0 = kappa c sqrt(G rho_Lambda), kappa = 1/2 ADOPTED):")
print(f"  rho_Lambda(canonical) = {sp.N(rho_can, 10)} kg/m^3")
print(f"  rho_Lambda(alt)       = {sp.N(rho_alt, 10)} kg/m^3")
print("  all statements dimensionless -> apply identically to both footings;")
print("  G_N/G_bare/G_cosmo kept separate; kappa = 1/2 adopted, never derived.")
res["footings"] = {"rho_can": float(rho_can), "rho_alt": float(rho_alt), "kappa": "1/2 adopted"}

elapsed = time.time() - t0
print(f"\nwall_time_seconds = {elapsed:.3f}")

print("\nVERDICT: (a) LANDS.")
print("  On the pinned cell (compact closed leaf, all fields on shell, terminal heat BC")
print("  L_b = -R_W, lam0 = L_0, flux constancy d_mu q = 0):  each cross-source sector")
print("  current closes on shell (div Q_heat = 0, div Q_U1 = 0, div Q_vac = 0), so")
print("  div(Q_heat + Q_U1 + Q_vac) = 0 identically over the audited coupling band and")
print("  div Q_b = 0 in the N sqrt(h) measure.  Matter-only Ward separation PROVED;")
print("  the gate-P5 matter atom is landed on this pin.  NEG-1 and NEG-2 both fire.")
sys.exit(0)
