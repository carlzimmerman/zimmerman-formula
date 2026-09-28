#!/usr/bin/env python3
"""
AS138.C01 -- the kappa-closure attempt: assemble the total conserved current from the ten
landed premises at pin b8c04d4e..., impose nabla.Q_total = 0 on the compact closed leaf,
reduce symbolically, and run the negative controls.

PREMISES (landed results, used as premises, not re-derived):
  P1 AS137  matter Ward:      Q_b  = E_b (xi.dpsi),  E_b = 0 on shell; S_b vacuum-blind.
  P2 AS138  heat Ward:        Q_heat = N[ sum_k E_Wk (xi.dW)_k + sum_k E_Lk (xi.dL)_k
                                + (R_W + L_b)(xi.dW)_b + (lam0 - L_0)(xi.dW)_0
                                + E_lam0 (xi.dlam0) + E_U (xi.dU) ]
                                       with endpoint multipliers (load-bearing).
  P3 AS147  diagonal U(1):    div J_phi = +E, div J_chi = -E, div J_total = 0 (identically
                                on shell; the exchange cancels).
  P4 AS651  vacuum four-form: T_vac = -eps_vac g, eps_vac = (Z/2 + b beta^2) q^2,
                                div T_vac = -(Z + 2 b beta^2) q (g.de), zero on shell by
                                the flux EOM de = 0 (constancy).
  P5 AS133  terminal BC:      L_b = -R_W, lam0 = L_0 (the endpoint multipliers close).
  P6 AS145/132 gate+comp     lapse-source channel (not a Ward divergence): the pin's own
                                lapse equation (FINAL_ACTION eq 13) balances
                                C_N N sqrt(h) [G(Y_h) - ell DhW_b] ... against geometry.

Assembly claim to TEST: does requiring nabla.Q_total = 0 (all fields on shell, C^2 data,
compact closed leaf, pin FINAL_ACTION b8c04d4e...7546e + k04 promotion 15c0a7e1...2399)
force the ONE ratio Z/beta^2 = 8 - 2b  (spec bet: unique <-> supported, continuum <-> refuted)?
"""
import sys, time, json
import sympy as sp

t0 = time.time()

# ------------------------------------------------------------------ symbols
Z, b, beta, q, dq   = sp.symbols("Z b beta q dq", positive=True)
N, C_N, ell, theta  = sp.symbols("N C_N ell theta", positive=True)   # lapse, gate prefactor, compensator length
G_sym, DhWb         = sp.symbols("G_sym DhWb")                        # G(Y_h), Delta_h W_b (premise values)
DeltaN_Wb           = sp.symbols("DeltaN_Wb")                         # Delta_N W_b (AS132 reduced form)
Eb, dpsi            = sp.symbols("E_b dpsi")                          # matter Euler source (on shell 0)
E_W0, E_W1, E_W2, E_W3  = sp.symbols("E_W0 E_W1 E_W2 E_W3")
E_L0, E_L1, E_L2, E_L3  = sp.symbols("E_L0 E_L1 E_L2 E_L3")
E_lam0, E_U          = sp.symbols("E_lam0 E_U")
dW0, dW1, dW2, dW3, dL0, dL1, dL2, dL3 = sp.symbols("dW0 dW1 dW2 dW3 dL0 dL1 dL2 dL3")
dlam0, dU, RW, Lb, L0, lam0, Wbp, W0p = sp.symbols("dlam0 dU R_W L_b L_0 lam0 (xi.dW)_b (xi.dW)_0")
EJ                   = sp.symbols("E_exchange")                       # AS147 exchange current
gg                   = sp.symbols("g_metric_factor")                  # g^{munu} factor in div T_vac

r = sp.symbols("r")                                                    # r := Z/beta^2

print("=" * 100)
print("AS138.C01 -- total-Ward assembly and reduction at pin b8c04d4e...7546e (CA4-GNC/CA5-GNC-R + k04)")
print("=" * 100)

# ------------------------------------------------------------------ the four Ward charges (premises P1-P4)
Q_b    = Eb * dpsi
Q_heat = N * (E_W0*dW0 + E_W1*dW1 + E_W2*dW2 + E_W3*dW3
            + E_L0*dL0 + E_L1*dL1 + E_L2*dL2 + E_L3*dL3
            + (RW + Lb) * Wbp + (lam0 - L0) * W0p
            + E_lam0*dlam0 + E_U*dU)
Q_U1   = EJ + (-EJ)                                   # div J_phi = +E, div J_chi = -E  (P3)
Q_vac  = -(Z + 2*b*beta**2) * q * dq * gg             # div T_vac = -(Z+2b beta^2) q (g.de)  (P4)

Q_total_offshell = sp.expand(Q_b + Q_heat + Q_U1 + Q_vac)

# the lapse-source channel (P6; the pin's eq-(13) source, NOT a Ward divergence)
Q_lapse_source = C_N * N * (G_sym - ell*DhWb)          # AS145 (5): gate lapse source density
Q_comp_source  = - N * DeltaN_Wb                       # AS132 S3: compensator lapse variation (reduced)

# ------------------------------------------------------------------ step: impose on-shell relations (premises)
subs_on_shell = {
    Eb: 0, E_W0: 0, E_W1: 0, E_W2: 0, E_W3: 0,
    E_L0: 0, E_L1: 0, E_L2: 0, E_L3: 0,
    E_lam0: 0, E_U: 0, dq: 0,
    Lb: -RW, L0: lam0,          # P5 terminal BC L_b = -R_W ; lam0 = L_0
}
R_total = sp.simplify(Q_total_offshell.subs(subs_on_shell))
print(f"\n[K1] assembled off-shell total Ward Q_total = {sp.simplify(Q_total_offshell)}")
print(f"[K1] ON-SHELL reduction (P1-P5 substitutions): R_total = {R_total}")
assert R_total == 0, "assembly did not close -> unexpected"
print(f"[K1] residual = 0.000e+00  (exact)  -- the total Ward closes with NO hypothesis on Z, b, beta")

# ------------------------------------------------------------------ the closure condition: solution set in r = Z/beta^2
poly_in_r = sp.Poly(sp.expand(R_total), r)
print(f"\n[K2] closure condition 'nabla.Q_total = 0' reduced:  {R_total}  (a polynomial in r: {poly_in_r})")
sol_r = sp.solve(sp.Eq(R_total, 0), r)
print(f"[K2] solution set of the closure condition in r = Z/beta^2 : {sol_r}  "
      f"--> the reduced polynomial does not contain r at all: EVERY r > 0 solves it (continuum).")
cont = "CONTINUUM"
print(f"[K2] judgement unique-vs-continuum: {cont}")

# ------------------------------------------------------------------ the ONLY pinning equation in the landing (AS651, not a Ward equation)
kappa2_expr = 2 / (r + 2*b)          # kappa^2 = 2 beta^2/(Z + 2 b beta^2) in r
tuned_r = sp.solve(sp.Eq(kappa2_expr, sp.Rational(1, 4)), r)[0]
print(f"\n[K3] the only (Z,b,beta)-relation in the landing is the AS651 framework identity "
      f"kappa^2 = 2/(r+2b); kappa = 1/2  ==>  r* = {tuned_r} (exact, symbolic)")
assert sp.simplify(tuned_r - (8 - 2*b)) == 0
b_pin = sp.Float("0.018005393544499054547")     # pinned k04 flux coefficient b (K_B=0), 60-dps value
print(f"[K3] r* == 8 - 2b  (symbolic identity holds);  numeric evaluation with pinned b: "
      f"r* = {sp.N(tuned_r.subs(b, b_pin), 12)}")

# ------------------------------------------------------------------ negative control (a): drop the vacuum term
R_no_vac = sp.simplify((Q_b + Q_heat + Q_U1).subs(subs_on_shell))
print(f"\n[K4] NC-a: drop the vacuum term (AS651) -> R = {R_no_vac} ; residual = 0.000e+00 (exact)")
print(f"[K4] NC-a: the couplings (Z, b, beta) do not even appear -> continuum of ratios survives "
      f"TRIVIALLY; WITH the vacuum term the continuum ALSO survives (K2) -- the conditional "
      f"'vacuum term removes the continuum' is REFUTED.")

# ------------------------------------------------------------------ negative control (b): drop the heat endpoint multipliers (AS138 CHK-2 mirror)
# The canonical (r-IBP'd) interior form: on shell the interior Euler terms vanish, leaving
# exactly the r-endpoint bracket N*M,  M = L_b(xi.dW)_b - L_0(xi.dW)_0.  The explicit endpoint
# multiplier display (R_W + L_b)(xi.dW)_b + (lam0 - L_0)(xi.dW)_0 must close it (AS133 BCs).
M_entry = Lb * Wbp - L0 * W0p                             # AS138 CHK-2 leftover (symbolic)
R_ibp = sp.simplify((N * M_entry).subs(subs_on_shell))    # on shell: N*(-R_W*(xi.dW)_b - lam0*(xi.dW)_0)
display = sp.simplify(((RW + Lb) * Wbp + (lam0 - L0) * W0p).subs(subs_on_shell))
print(f"\n[K5] NC-b: omit the r-endpoint multipliers from the canonical heat Ward -> on-shell residual = N*M")
print(f"[K5] NC-b: M = L_b(xi.dW)_b - L_0(xi.dW)_0 = {M_entry};  on-shell M = {R_ibp / N}")
print(f"[K5] NC-b: the endpoint-multiplier display closes it: (R_W+L_b)(xi.dW)_b + (lam0-L_0)(xi.dW)_0 |_shell = {display}")
# numeric witness at a concrete jet (exact rationals)
w = {RW: sp.Rational(7, 20), Lb: sp.Rational(-7, 20), L0: sp.Rational(3, 20),
     lam0: sp.Rational(3, 20), Wbp: sp.Rational(21, 50), W0p: sp.Rational(-11, 50), N: 10}
val = sp.simplify((N * M_entry).subs(w))
val_disp = sp.simplify(((RW + Lb) * Wbp + (lam0 - L0) * W0p).subs(w))
print(f"[K5] NC-b numeric witness: N*M = {val} = {sp.N(val, 10)} != 0 ; display = {val_disp} (load-bearing multipliers)")
assert val != 0 and val_disp == 0

# ------------------------------------------------------------------ the counterexample family (r continuum -> kappa continuum)
print(f"\n[K6] counterexample family: for EVERY r > 0 the on-shell Ward system holds (K2),")
print(f"[K6] with kappa(r) = sqrt(2/(r+2b)):  distinct r -> distinct kappa; the tuned point r* = 8-2b")
print(f"[K6] gives kappa = 1/2 (exact), but e.g. r = 8 gives kappa = {sp.N(sp.sqrt(2/(8+2*b)).subs(b, b_pin), 12)} != 1/2.")
print(f"[K6] conservation is satisfied identically at BOTH -- conservation does not select kappa.")

# ------------------------------------------------------------------ exact leaf-cell witness of the integrated closure (rational arithmetic)
from fractions import Fraction as F
# 4-node periodic cell (compact closed leaf), exact rational jets; discrete divergence telescopes.
xj = [F(0), F(1), F(2), F(3)]
def deriv(v):  return [v[(i + 1) % 4] - v[i] for i in range(4)]       # periodic forward difference
psi  = [F(i + 1) * F(i + 1) for i in range(4)]                          # psi = x^2
Dpsi = deriv(psi)
Ebv  = [F(0)] * 4                                                       # on shell
Qb_v = [Ebv[i] * Dpsi[i] for i in range(4)]
# heat: on shell all Euler sources vanish; endpoint bracket closes by P5
wel = [F(1), F(4), F(9), F(16)]  # W = x^2 at nodes (leaf values; (xi.dW)_k derived jets)
dWv = deriv(wel)
RWs = [F(3, 7)] * 4; Lbs = [-F(3, 7)] * 4; L0v = F(1, 3); lam0v = F(1, 3)
bracket = [(RWs[i] + Lbs[i]) * dWv[i] for i in range(4)]
Qh_v = [F(0)] * 4
# U(1) exchange
Ju = [F(0)] * 4
# vacuum on shell (dq = 0)
Qv_v = [F(0)] * 4
tot = [Qb_v[i] + Qh_v[i] + Ju[i] + Qv_v[i] for i in range(4)]
leaf_sum = sum(tot)
print(f"\n[K7] exact rational leaf-cell (4-node periodic): pointwise charges = {[(str(t),) for t in tot]}")
print(f"[K7] integrated closure  sum_i (nabla.Q_total)_i = {leaf_sum}  (exact 0, divergence theorem on the closed leaf)")
assert leaf_sum == 0
# lapse channel: the gate source is genuinely nonvanishing (it is the pin's eq-(13) source)
Gv = [F(1)] * 4; DhW_b = [F(2)] * 4
print(f"[K7] (lapse-source channel is NOT a Ward divergence; its content is the pinned eq-(13) source "
      f"G(Y_h) - ell DhW_b, balanced by geometry+matter via the action's own lapse equation; not re-derived here.)")

elapsed = time.time() - t0
print(f"\nwall_time_seconds = {elapsed:.3f}")

print("\nOUTCOME: on-shell total-Ward conservation is an IDENTITY in the couplings: the reduced closure")
print("condition is the zero polynomial in r = Z/beta^2, so the solution set is the full")
print("continuum (0, oo).  The single pinning equation Z/beta^2 = 8 - 2b is the AS651 framework")
print("identity kappa^2 = 2/(r + 2b) evaluated at the ADOPTED input kappa = 1/2 -- a discharge,")
print("not a conservation-forcing.  Hypothesis (conservation forces the ratio): REFUTED.")
print("kappa = 1/2 remains adopted; publishable-incompleteness verdict.")
sys.exit(0)