#!/usr/bin/env python3
"""AG4 — the rest-state law from the frozen S2 action (law-form adjudication).

Derives, machine-checked, which interpolation is the unique static rest state of

    L = -|grad Phi - K P|^2/(2K) - rho_b Phi - W_rem(u) - (gamma/2)|grad P|^2
    K = 4 pi G,  u = K|P|,  K W_rem'(u) = u^2/(a0 - u),  gamma = K L*^2/2

(THEORY_CANONICAL_2026-10-14 S2, asserted verbatim at runtime). Spherical static ansatz,
point baryon mass M_b. G1 derives BOTH field equations by jet-total-derivative
Euler-Lagrange of the full radial action density with W_rem built explicitly as the
antiderivative of the frozen W_rem' (amendment A). Physical premises NOT certified here
(declared): Gauss for A on the point source; P parallel A at rest; gamma = 0 outside the
screening core (bounded numerically in G4, tiered per amendment A).

Hand derivation (verified by sympy below):
  dL/dPhi:  div(A) = 4 pi G rho_b,  A := grad Phi - K P    => |A| = gbar = G M_b/r^2
  dL/dP  :  A - (u^2/(a0-u)) Phat + gamma lap(P) = 0       => (gamma=0) gbar = u^2/(a0-u)
  grad Phi = A + K P  =>  g = gbar + u,  u = g_ph = K|P| (the tether variable)
  => u^2 + gbar u = a0 gbar  =>  g^2 = gbar (g + a0)   [canonical S2 law]
Capacity family: K W_rem' = u^2/(a0 - n u) => u^2 + n gbar u = a0 gbar;
  n=1 canonical, n=2 quadratic g^2 - gbar^2 = a0 gbar.

Frozen criteria: FROZEN_CRITERIA.md (93e579ec1) + AMENDMENT_A (c80cdb5fd).
Exit 0 iff gates pass and (MUTATE=1) mutations behave as designed.
"""
import json
import math
import os
import sys

import numpy as np
import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
MUTATE = os.environ.get("MUTATE", "0") == "1"

# ---------------- constants (SI anchors from runtime files) ----------------
a0_SI = json.load(open(os.path.join(REPO, "deepseek_push", "G081_results.json")))["constants"]["a0"]
G_SI = 6.674e-11
MSUN_KG = 1.98892e30
PC_M = 3.0856775814913673e16
MSUN_PC2_KGM2 = MSUN_KG / PC_M**2          # 1 Msun/pc^2 in kg/m^2

# assert the S2 lines verbatim (kill test 3)
S2_PATH = os.path.join(REPO, "campaign_fresh_gravity", "THEORY_CANONICAL_2026-10-14.md")
s2_text = open(S2_PATH).read()
for line in ["L = −|∇Φ − K P|²/(2K) − ρ_b Φ − W_rem(u) − (γ/2)|∇P|²",
             "K W_rem′(u) = u²/(a₀ − u)",
             "g_N = g²/(g + a₀)"]:
    assert line in s2_text, f"S2 line changed — criteria void (kill test 3): {line}"

print("=" * 100)
print("AG4 — rest-state law from the frozen S2 action (FROZEN 93e579ec1 + AMD-A c80cdb5fd)")
print(f"a0 = {a0_SI} m/s^2 (runtime, G081 JSON); S2 lines asserted verbatim; MUTATE={MUTATE}")
print("=" * 100)

# ---------------- G1: variational derivation (sympy jet EL, explicit W_rem) ----------------
r, K, a0, gam, n_cap = sp.symbols("r K a0 gamma n", positive=True)
Phi, Phi1, Phi2, P, P1, P2 = sp.symbols("Phi Phi1 Phi2 P P1 P2")
rho_b = sp.Function("rho_b")

A_r = Phi1 - K * P                            # radial A = grad Phi - K P
uu = sp.Symbol("u", positive=True)
# K W_rem(u): antiderivative of u^2/(a0 - n u); at n=1 equals the ArgonClues-certified
# a0^2(-ln(1-u/a0) - u/a0 - u^2/(2a0^2)) up to a constant.
KWu = (-a0**2 * sp.log(a0 - n_cap * uu) / n_cap**3
       + 2 * a0 * (a0 - n_cap * uu) / n_cap**3
       - (a0 - n_cap * uu)**2 / (2 * n_cap**3))
wrem_prime_chk = sp.simplify(sp.diff(KWu, uu) - uu**2 / (a0 - n_cap * uu))
assert wrem_prime_chk == 0, "W_rem antiderivative does not reproduce frozen W_rem'"
KW = KWu.subs(uu, K * P)

# radial action density (x r^2, up to 4pi); |grad P|^2 for P = P(r) rhat: P1^2 + 2P^2/r^2
L2 = (-A_r**2 * r**2 / (2 * K) - rho_b(r) * Phi * r**2 - (KW / K) * r**2
      - (gam / 2) * (P1**2 * r**2 + 2 * P**2))

def D_r(e):
    """Total d/dr along the jet."""
    return (sp.diff(e, r) + sp.diff(e, Phi) * Phi1 + sp.diff(e, Phi1) * Phi2
            + sp.diff(e, P) * P1 + sp.diff(e, P1) * P2)

eomPhi = sp.simplify(sp.diff(L2, Phi) - D_r(sp.diff(L2, Phi1)))
A_rp = Phi2 - K * P1                          # total dA_r/dr
expected_Phi = sp.simplify(-rho_b(r) * r**2 + (2 * r * A_r + r**2 * A_rp) / K)
res_Phi = sp.simplify(eomPhi - expected_Phi)
g1a = res_Phi == 0
print("\nG1a  dL/dPhi:  (r^2 A_r)' = K r^2 rho_b  <=>  div A = K rho_b (K = 4 pi G)")
print(f"     EL residual vs expected form: {res_Phi}  -> {'PASS' if g1a else 'FAIL'}")
print("     => point baryon mass, regular at infinity:  A_r = G M_b/r^2 = gbar (declared premise)")

eomP = sp.simplify(sp.diff(L2, P) - D_r(sp.diff(L2, P1)))
lap_P_r = P2 + 2 * P1 / r - 2 * P / r**2
expected_P = sp.simplify(r**2 * (A_r - (K * P)**2 / (a0 - n_cap * K * P) + gam * lap_P_r))
res_P = sp.simplify(sp.expand(eomP - expected_P))
g1b = res_P == 0
print("G1b  dL/dP:  A - (u^2/(a0 - n u)) Phat + gamma lap(P) = 0   (radial, u = K P)")
print(f"     EL residual vs physics form: {res_P}  -> {'PASS' if g1b else 'FAIL'}")

gbar_s, u_s = sp.symbols("gbar u", positive=True)
rest_poly = sp.simplify(sp.together(gbar_s - u_s**2 / (a0 - n_cap * u_s)) * (a0 - n_cap * u_s))
g1c = sp.expand(rest_poly) == sp.expand(-(u_s**2 + n_cap * gbar_s * u_s - a0 * gbar_s))
print("G1c  rest state (gamma=0):  gbar(a0 - n u) = u^2  <=>  u^2 + n gbar u = a0 gbar")
print(f"     cleared form matches: {g1c}  -> {'PASS' if g1c else 'FAIL'}")

# ---------------- G2: canonical rest state (n = 1) ----------------
gbar0 = sp.symbols("gbar0", positive=True)
u1 = (sp.sqrt(gbar0**2 + 4 * a0 * gbar0) - gbar0) / 2
res_u1 = sp.simplify(u1**2 + gbar0 * u1 - a0 * gbar0)
g2a = res_u1 == 0
law_res = sp.simplify((gbar0 + u1)**2 - gbar0 * ((gbar0 + u1) + a0))
g2b = law_res == 0
print(f"\nG2a  n=1 explicit root solves rest state: residual {res_u1} -> {'PASS' if g2a else 'FAIL'}")
print(f"G2b  g := gbar + u satisfies g^2 = gbar(g + a0) [canonical S2 law]: residual {law_res}"
      f" -> {'PASS' if g2b else 'FAIL'}")

eps = 1e-4
gbar_num = eps * a0_SI
u_num = (math.sqrt(gbar_num**2 + 4 * a0_SI * gbar_num) - gbar_num) / 2
nu_num = (gbar_num + u_num) / gbar_num
g2c = abs(nu_num - 100.5) < 0.01
print(f"G2c  PAPER49 anchor: nu(gbar=1e-4 a0) = {nu_num:.5f} vs 100.5 -> {'PASS' if g2c else 'FAIL'}")

x_s, rM_s = sp.symbols("x rM", positive=True)
gbar_x = a0 / x_s**2
u_x = sp.simplify((sp.sqrt(gbar_x**2 + 4 * a0 * gbar_x) - gbar_x) / 2)
M_ratio = sp.simplify(x_s**2 * u_x / a0)
g2d = sp.simplify(M_ratio - (sp.sqrt(1 + 4 * x_s**2) - 1) / 2) == 0
print(f"G2d  ARGON02 P1 identity: M_ph/M_b = x^2 u/a0 = {M_ratio} == (sqrt(1+4x^2)-1)/2"
      f" -> {'PASS' if g2d else 'FAIL'}")
# density profile in units M_b/rM^3: rho = dM_ratio/dx / (4 pi x^2); target 1/(2 pi x sqrt(1+4x^2))
rho_derived = sp.simplify(sp.diff(M_ratio, x_s) / (4 * sp.pi * x_s**2))
rho_target = sp.simplify(1 / (2 * sp.pi * x_s * sp.sqrt(1 + 4 * x_s**2)))
g2e = sp.simplify(rho_derived - rho_target) == 0
print(f"G2e  ARGON02 density profile (M_b/r_M^3 units): {rho_derived} == {rho_target}"
      f" -> {'PASS' if g2e else 'FAIL'}")
deep_u = sp.limit(u_x / sp.sqrt(a0 * gbar_x), x_s, sp.oo)
g2f = deep_u == 1
print(f"G2f  deep limit u/sqrt(a0 gbar) -> {deep_u} (g_ph -> C/r, A/r^2 chain) -> {'PASS' if g2f else 'FAIL'}")

# ---------------- G3: capacity family / law-form split ----------------
u2s = sp.symbols("u2s", positive=True)
u2_root = sp.simplify(-gbar_s + sp.sqrt(gbar_s**2 + a0 * gbar_s))   # root of u^2+2 gbar u = a0 gbar
g3a_sym = sp.simplify((gbar_s + u2_root)**2 - gbar_s**2 - a0 * gbar_s) == 0
g3a_can = sp.simplify((gbar_s + u2_root)**2 - gbar_s * ((gbar_s + u2_root) + a0)) != 0
g3a = g3a_sym and g3a_can
print(f"\nG3a  n=2 rest state <=> quadratic g^2-gbar^2 = a0 gbar (and NOT canonical): {g3a}"
      f" -> {'PASS' if g3a else 'FAIL'}")
gn_id = sp.expand(((gbar_s + u_s)**2 - gbar_s**2 - (a0 * gbar_s + (2 - n_cap) * gbar_s * u_s))
                  - (u_s**2 + n_cap * gbar_s * u_s - a0 * gbar_s))
g3b = gn_id == 0
print(f"G3b  general capacity identity g^2-gbar^2 = a0 gbar + (2-n) gbar u on-shell: {g3b}"
      f" -> {'PASS' if g3b else 'FAIL'}")
u1_inf = sp.limit(u1 / a0, gbar0, sp.oo)
u2_cap = sp.limit(u2_root / a0, gbar_s, sp.oo)
g3c = u1_inf == 1
g3d = u2_cap == sp.Rational(1, 2)
sig1 = a0_SI / math.pi / G_SI / MSUN_PC2_KGM2
sig2 = a0_SI / 2 / math.pi / G_SI / MSUN_PC2_KGM2
print(f"G3c  n=1 tether capacity: lim g_ph/a0 = {u1_inf} (Sigma_max = a0/(pi G) = {sig1:.1f}"
      f" Msun/pc^2 — PAPER49's 214) -> {'PASS' if g3c else 'FAIL'}")
print(f"G3d  n=2 tether capacity: lim g_ph/a0 = {u2_cap} (Sigma_max = {sig2:.1f} Msun/pc^2)"
      f" -> {'PASS' if g3d else 'FAIL'}")

# ---------------- G4: gamma-reduction bound (numeric, tiered per AMD-A) ----------------
print("\nG4  gamma-term ratio |gamma lap P| / (u^2/(a0-u)) on the exact rest-state profile:")
du_expr = sp.diff((sp.sqrt(1 + 4 * x_s**2) - 1) / (2 * x_s**2), x_s)
d2u_expr = sp.diff(du_expr, x_s)
f1 = sp.lambdify(x_s, du_expr, "numpy")
f2 = sp.lambdify(x_s, d2u_expr, "numpy")
xx = np.logspace(-3, 1.7, 200)
s_arr = np.sqrt(1 + 4 * xx**2)
uu_arr = (s_arr - 1) / (2 * xx**2)                      # u/a0 in (0,1)
lapU = f2(xx) + 2 * f1(xx) / xx - 2 * uu_arr / xx**2    # x-units radial vector Laplacian

g4_rows = []
for Lstar_pc, rM_kpc in [(5.75, 10.0), (1000.0, 10.0), (5.75, 1.0), (1000.0, 1.0)]:
    Ldim = (Lstar_pc / 1e6) / (rM_kpc / 1e3)            # L*/r_M (both in Mpc)
    ratio = (Ldim**2 / 2) * np.abs(lapU) * (1 - np.clip(uu_arr, 0, 1 - 1e-12)) / uu_arr**2
    rs = Ldim**2                                        # r_s/r_M = (L*/r_M)^2
    m10 = xx >= 10 * rs
    r10 = float(np.max(ratio[m10])) if np.any(m10) else float("nan")
    below = np.where(ratio < 0.01)[0]
    r1pct = float(xx[below[0]]) if len(below) and np.all(ratio[below[0]:] < 0.01) else float("nan")
    g4_rows.append(dict(Lstar_pc=Lstar_pc, rM_kpc=rM_kpc, Ldim=Ldim, rs=rs,
                        max_ratio_ge10rs=r10, r_1pct_in_rM=r1pct))
    print(f"    L*={Lstar_pc:7.1f} pc, r_M={rM_kpc:4.1f} kpc (L*/r_M={Ldim:.2e}, r_s/r_M={rs:.1e}):"
          f" max ratio (r>=10rs) = {r10:.2e}; r(<1% ever after) = {r1pct:.3g} r_M")
g4i = all(row["max_ratio_ge10rs"] < 1e-6 for row in g4_rows if row["Lstar_pc"] == 5.75)
g4ii = all(row["max_ratio_ge10rs"] < 0.01 for row in g4_rows if row["Ldim"] <= 0.1 and row["Lstar_pc"] != 5.75)
g4iii = [row for row in g4_rows if row["Ldim"] > 0.1 and row["Lstar_pc"] != 5.75]
print(f"G4-i  (L*=5.75pc: <1e-6 for r>=10rs): {'PASS' if g4i else 'FAIL'}")
print(f"G4-ii (L*/r_M<=0.1: <1% for r>=10rs): {'PASS' if g4ii else 'FAIL'}")
print("     structural note: ratio -> (L*/r_M)^2 as x -> 0 (uu -> 1-x^2, lap -> -2/x^2):")
print("     the frozen thresholds (1e-6 / 1%) sit AT the structural asymptote of the boundary")
print("     corners (5.75pc/1kpc = 3.3e-5; 1kpc/10kpc = 1.0e-2): miscalibration, recorded as")
print("     FAILED-as-frozen, NOT re-adjudicated post-run. Physics: gamma=0 reduction holds at")
print("     O((L*/r_M)^2) <= 1.09% in every corner, <= 0.004% at the fiducial L* floor.")
for row in g4iii:
    intrudes = row["r_1pct_in_rM"] <= 3.0
    print(f"G4-iii (L*/r_M={row['Ldim']:.2f} corner): r_1% = {row['r_1pct_in_rM']:.3g} r_M"
          f" -> gamma=0 valid outside; {'*** INTRUDES on AG3 band regime (r~1-3 r_M): AG3 B2 gets a stiffness caveat ***' if intrudes else 'no intrusion on the AG3 annulus regime (r ~ 1-3 r_M)'}")
g4 = g4i and g4ii

# ---------------- G5-pre: precheck every Lean statement (before typing) ----------------
print("\nG5-pre  Lean statement prechecks (sympy, before typing any theorem):")
gb_, u_, a_, n_, u1s_, u2s_, s_, xs_, D_ = sp.symbols("gb u a n u1 u2 s x D", positive=True)
# NOTE: checks use the subtract-relation form: "rest state => law" means the law residual
# IS the rest-state residual as polynomials (subs with u on its own RHS cascades — sympy trap).
checks = {}
checks["T1 eom_bridge"] = sp.expand(gb_ * (a_ - u_) - u_**2 + (u_**2 + gb_ * u_ - a_ * gb_)) == 0
checks["T2 rest_to_law"] = sp.expand((gb_ + u_)**2 - gb_ * (gb_ + u_ + a_)
                                     - (u_**2 + gb_ * u_ - a_ * gb_)) == 0
checks["T3 law_to_rest"] = sp.expand((u_ + gb_)**2 - gb_ * (u_ + gb_ + a_)
                                     - (u_**2 + gb_ * u_ - a_ * gb_)) == 0
checks["T4 uniqueness_factor"] = (sp.expand((u1s_ - u2s_) * (u1s_ + u2s_ + gb_))
                                  == sp.expand((u1s_**2 + gb_ * u1s_) - (u2s_**2 + gb_ * u2s_)))
sd_ = sp.Symbol("sd", positive=True)
checks["T6 root_identity"] = (sp.simplify(((sd_ - gb_) / 2)**2 + gb_ * (sd_ - gb_) / 2
                                          - (sd_**2 - gb_**2) / 4) == 0
                              and sp.simplify(((gb_**2 + 4 * a_ * gb_) - gb_**2) / 4 - a_ * gb_) == 0)
checks["T7 capacity_family"] = sp.expand((gb_ + u_)**2 - gb_**2 - (a_ * gb_ + (2 - n_) * gb_ * u_)
                                         - (u_**2 + n_ * gb_ * u_ - a_ * gb_)) == 0
checks["T8 phantom_core"] = sp.expand((s_ - 1) * (s_ + 1) - 4 * xs_**2).subs(s_**2, 1 + 4 * xs_**2) == 0
for k, v in checks.items():
    print(f"    {k}: {'OK' if v else 'MIS-STATED — FIX BEFORE LEAN'}")
sw = []
for gv in [1e-6, 1e-3, 0.1, 1.0, 3.0, 10.0]:
    u0 = math.sqrt(a0_SI * gv + gv**2 / 4) - gv / 2
    sw.append(math.sqrt(a0_SI * gv) - gv / 2 - 1e-12 <= u0 <= math.sqrt(a0_SI * gv) + 1e-12)
checks["T9 sandwich_corners"] = all(sw)
print(f"    T9 sandwich corners: {'OK' if all(sw) else 'FAIL'}")
g5pre = all(checks.values())

# ---------------- mutations ----------------
mut = {}
if MUTATE:
    print("\n--- MUTATE run ---")
    m1_quad = sp.simplify((gbar_s + u2_root)**2 - gbar_s**2 - a0 * gbar_s)
    m1_canon = sp.simplify((gbar_s + u2_root)**2 - gbar_s * ((gbar_s + u2_root) + a0))
    mut["M1"] = (m1_quad == 0) and (m1_canon != 0)
    print(f"M1 capacity-2 rest state: quadratic residual {m1_quad} (must be 0), "
          f"canonical residual {m1_canon} (must be nonzero) -> {mut['M1']}")
    m2_res = sp.simplify(u1**2 + 2 * gbar0 * u1 - a0 * gbar0)
    m2_expected = sp.simplify(gbar0 * u1)
    mut["M2"] = sp.simplify(m2_res - m2_expected) == 0 and m2_res != 0
    print(f"M2 canonical g_ph in n=2 rest equation: residual {sp.simplify(m2_res - m2_expected)}"
          f" beyond gbar*u -> equals gbar*u: {mut['M2']}")
    m3_res = sp.simplify(u1**2 / (a0 - u1) - gbar0)
    mut["M3"] = m3_res == 0
    print(f"M3 positive control (canonical g_ph in frozen EOM): residual {m3_res} -> {mut['M3']}")

# ---------------- verdict ----------------
gates = dict(G1=g1a and g1b and g1c, G2=g2a and g2b and g2c and g2d and g2e and g2f,
             G3=g3a and g3b and g3c and g3d, G4=g4, G5pre=g5pre)
if MUTATE:
    gates["MUT"] = all(mut.values())
gate_pass = all(gates.values())
BRANCH = "a" if (gates["G1"] and gates["G2"] and gates["G3"]) else "c"
print("\n" + "=" * 100)
print(f"BRANCH: ({BRANCH})  [pre-registered readings in FROZEN_CRITERIA.md]")
if BRANCH == "a":
    print("  The unique static rest state of the frozen S2 action (gamma=0, spherical, point baryon")
    print("  source) IS the canonical law:  gbar = g^2/(g + a0),  g_ph = u = K|P| < a0,")
    print("  u = (sqrt(gbar^2 + 4 a0 gbar) - gbar)/2.  PAPER49's claim is DERIVED, not assumed.")
    print("  The quadratic a0-line g^2 - gbar^2 = a0 gbar is the rest state of the capacity-")
    print("  halved variant K W_rem' = u^2/(a0 - 2u): a DIFFERENT theory (tether capacity a0/2,")
    print(f"  Sigma_max ~ {sig2:.0f} Msun/pc^2 vs PAPER49's cited {sig1:.0f}). Not this action's law.")
print(f"  gates: {gates}")
print(f"AG4 {'MUTATE' if MUTATE else 'MAIN'} COMPLETE: {'PASS' if gate_pass else 'FAIL'}")

out = dict(lane="AG4_law_from_action", frozen="93e579ec1 + AMD-A c80cdb5fd (both pre-run)",
           mode="MUTATE" if MUTATE else "MAIN", branch=BRANCH, gates={k: bool(v) for k, v in gates.items()},
           a0_SI=a0_SI, nu_anchor=float(nu_num),
           sigma_max_n1_Msun_pc2=float(sig1), sigma_max_n2_Msun_pc2=float(sig2),
           G4_rows=g4_rows, mutations={k: bool(v) for k, v in mut.items()} if MUTATE else None,
           lean_prechecks={k: bool(v) for k, v in checks.items()}, gate_pass=bool(gate_pass))
tag = "_MUTATE" if MUTATE else ""
with open(os.path.join(HERE, f"ag4_derive{tag}_results.json"), "w") as f:
    json.dump(out, f, indent=1, default=str)
print(f"results -> ag4_derive{tag}_results.json")
sys.exit(0 if gate_pass else 1)
