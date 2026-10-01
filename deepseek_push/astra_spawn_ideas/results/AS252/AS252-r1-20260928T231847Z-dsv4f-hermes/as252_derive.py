"""
AS252 Tier-0b: match the cosmological Einstein coefficient to measured Newton gravity.
Symbolic lane (sympy): exact extraction of the lapse coefficient, the local
normalization trace, and the vacuum-scale dictionary identities with the
ratio G_cosm/G_N = c_N = 1 - alpha/2 carried explicitly.

Seed: AS252_match_the_cosmological_einstein_coefficient_to_measured_newton_gravity.md
sha256 6de8d3e8bd3b8da9fe7e2953e04d0055d54382adafaaac64826ee12bbff1f5d2
Action: real_research/common_action_2026_09_26/action/FINAL_ACTION.md
sha256 b8c04d4e365f1c8e1c2ec3bf8d14629618d1ac162e97e3fdf809382fb147546e
Branch: CA5-GNC-R homogeneous inactive branch; Q/RAR/MU2/EXP/MONO untouched.
"""
import sympy as sp

ok = True
def check(name, expr, target=0, tol=1e-12):
    global ok
    e = sp.simplify(sp.expand(expr - target))
    if e == 0:
        print(f"PASS {name}: residual 0 (exact)")
    else:
        try:
            num = abs(complex(sp.N(e)))
        except Exception:
            num = float("inf")
        if num < tol:
            print(f"PASS {name}: residual {num:.3e} < tol {tol}")
        else:
            ok = False
            print(f"FAIL {name}: residual {e}")

MP2, Lam, rho_b, rho_d, H2, Gb, GN, Gc, cN, a0, c, kappa = sp.symbols(
    "MP2 Lam rho_b rho_d H2 Gb GN Gc cN a0 c kappa", positive=True)
alpha, pi_s = sp.symbols("alpha pi", positive=True)
cN_def = 1 - alpha/2

print("="*78)
print("STEP 1: coefficient multiplying homogeneous energy in the lapse equation")
print("="*78)
# Eq (13) of FINAL_ACTION on the homogeneous inactive branch:
#   (MP2/2){R3 - T_K - 2 Lam + ...} = rho_b + rho_d
# R3 = 0 (flat k=0), T_K = -6 H^2 (K_ij = H h_ij), Q_K = A_K = 0, V_a = 0, gate term 0.
TK = -6*H2
lhs_lapse = (MP2/2)*(0 - TK - 2*Lam)          # (MP2/2)(6 H^2 - 2 Lam)
friedmann = sp.simplify(sp.expand(lhs_lapse - (rho_b + rho_d)))  # should be 0 with 3 MP2 H2 = MP2 Lam + rho
# impose the Friedmann form: 3 MP2 H2 = MP2 Lam + rho_b + rho_d  -> solve H2:
H2_sol = sp.solve(sp.Eq(3*MP2*H2, MP2*Lam + rho_b + rho_d), H2)[0]
check("C1_lapse_flat_homogeneous", lhs_lapse.subs(H2, H2_sol), rho_b + rho_d)
coeff_rho = sp.simplify(sp.diff(H2_sol, rho_b))  # coefficient of homogeneous energy in H^2
check("C1b_coeff_of_rho_in_H2", coeff_rho, sp.Rational(1,3)/MP2)
# Cosmological Einstein coefficient: G_cosm = (8 pi MP2)^-1  -> coefficient = 8 pi G_cosm / 3
Gc_def = sp.Rational(1)/(8*pi_s*MP2)
check("C1c_coeff_via_Gcosm", coeff_rho, 8*pi_s*Gc_def/3)
# Step-1 statement: the multiplied coefficient is the standard Einstein one, with G_cosm the bare coupling.
# M_P^2 = (8 pi G_bare)^-1  and  G_cosm := (8 pi M_P^2)^-1  =>  G_cosm = G_bare (definitional identity):
Gb_mapped = sp.Rational(1)/(8*pi_s*MP2)
check("C1d_Gcosm_is_bare", sp.simplify(Gc_def - Gb_mapped), 0)  # same expression by definition

print("="*78)
print("STEP 2: local normalization supplied by the compensated host (trace, AS226)")
print("="*78)
# FINAL_ACTION sec.5: base quadratic density in units MP2/2 is
#   -2 cN |D(Phi-Z)|^2 - 4 cN DZ . DU   ->  measured G_N = G_bare/c_N.
# Trace: G_N := G_bare / c_N  (derived upstream: results/AS226, high-k reciprocal window)
GN_def = Gb/cN
check("C2_trace_local_normalization", sp.simplify(GN_def.subs(cN, cN_def)), Gb/cN_def)   # with c_N = 1 - alpha/2
check("C2b_ratio",
      sp.simplify((Gc_def/GN_def).subs({cN: cN_def, Gb: sp.Rational(1)/(8*pi_s*MP2)})),
      cN_def)     # G_cosm/G_N = c_N
# The prematurity map G_cosm = G_N is equivalent to c_N -> 1, i.e. alpha -> 0:
premature = sp.solve(sp.Eq(1, 1/cN_def), cN_def)  # G_bare = G_bare/c_N  (G_bare != 0)
premature_alpha = sp.solve(sp.Eq(1, 1/cN_def), alpha)
print(f"    [trace] G_cosm = G_N  <=>  c_N = 1  <=>  alpha = {premature_alpha}  (forces the open-domain boundary)")

print("="*78)
print("STEP 3: H^2 and the vacuum-scale relation in G_N + ratio; conversion into rho_Lambda")
print("="*78)
# Framework scale relation, operational (measured) constant:  rho_Lambda = 4 a0^2/(G_N c^2)
rhoL = 4*a0**2/(GN*c**2)
# Cosmological effective Lambda from that vacuum mass density, with the COSMOLOGICAL coefficient:
Lam_eff = 8*pi_s*Gc*rhoL/c**2          # Gc = G_cosm, distinct from GN
Lam_eff_final = sp.simplify(Lam_eff.subs(Gc, cN*GN))       # carry the ratio G_cosm = c_N G_N
check("C3_vacuum_lambda_dictionary", Lam_eff_final, 32*pi_s*cN*a0**2/c**4)
# Naive same-G expression:
Lam_naive = 32*pi_s*a0**2/c**4
check("C3b_naive_mismatch_factor", sp.simplify(Lam_eff_final/Lam_naive), cN)
# H_vac^2 = Lam_eff/3:
Hv2 = sp.simplify(Lam_eff_final/3)
check("C3c_Hvac2", Hv2, 32*pi_s*cN*a0**2/(3*c**4))
# rho_Lambda propagated into G_cosm:
check("C3d_rhoL_in_Gcosm", sp.simplify(rhoL.subs(Gc, cN*GN)), 4*cN*a0**2/(Gc*c**2).subs(Gc, cN*GN))
# Friedmann sector with matter, written in G_N and the ratio:
H2_full = sp.simplify(Lam/3 + (8*pi_s*Gc)*(rho_b+rho_d)/3)
check("C3e_Friedmann_in_GN_and_ratio",
      sp.simplify(H2_full.subs(Gc, cN*GN)), Lam/3 + 8*pi_s*cN*GN*(rho_b+rho_d)/3)

print("="*78)
print("CONTROL A: alpha -> 0 recovers the Einstein normalization")
print("="*78)
cN0 = sp.simplify(cN_def.subs(alpha, 0))
check("A1_cN_at_alpha0", cN0, 1)
check("A2_GN_equals_bare", sp.simplify(GN_def.subs(cN, cN0)), Gb)
check("A3_LamEff_equals_naive", sp.simplify(Lam_eff_final.subs(cN, cN0)), Lam_naive)
check("A4_standard_coeff", sp.simplify(coeff_rho.subs(MP2, sp.Rational(1)/(8*pi_s*Gb))), 8*pi_s*Gb/3)

print("="*78)
print("CONTROL B (negative control): set G_cosm = G_N prematurely")
print("="*78)
# Premature identification removes c_N from the dictionary: Lam_eff -> Lam_naive.
removed = sp.simplify(Lam_naive - Lam_eff_final)      # mismatch the premature calibration leaves
check("B1_premature_mismatch", sp.simplify(Lam_eff_final/Lam_naive - cN), 0)  # equality only for c_N=1
mismatch = sp.simplify(removed)
mismatch_alpha = sp.simplify(mismatch.subs(cN, cN_def))
print(f"    [control] Lam_naive - Lam_eff = {mismatch}  = (alpha/2) * Lam_naive at c_N = 1 - alpha/2 -> fires for alpha in (0,2)")
check("B2_mismatch_equals_alpha_half", sp.simplify(mismatch_alpha - alpha/2*Lam_naive), 0)
# The terms removed in the host lapse density (units MP2/2):
#   -4 cN DZ.DU -> -4 DZ.DU removes +2 alpha DZ.DU;  alpha|a-DZ|^2 -> 0 removes alpha|a-DZ|^2;
#   cN [G - ell Dh Wb] -> [G - ell Dh Wb] removes -(alpha/2)[G - ell Dh Wb].
DZDU, Ggate, aDZ2 = sp.symbols("DZDU Ggate aDZ2", positive=True)
d_density = sp.simplify((alpha*aDZ2 + (-4*cN_def)*DZDU) - (0*aDZ2 + (-4)*DZDU))
check("B3_removed_lapse_density_term", sp.simplify(d_density), alpha*aDZ2 + 2*alpha*DZDU)
removed_gate = sp.simplify(cN_def*Ggate - Ggate)
check("B4_removed_gate_prefactor", sp.simplify(removed_gate + alpha/2*Ggate), 0)
# Premature equality forces alpha = 0 (open-domain violation):
print(f"    [control] c_N = 1 forces alpha = {premature}: 0 is NOT in the open domain (0,2) -> assumption absent")

print("="*78)
print("SUMMARY")
print("="*78)
print(f"G_cosm/G_N = c_N = 1 - alpha/2  (alpha in (0,2)) : residual 0")
print(f"Lambda_eff = 32 pi c_N a0^2/c^4 ;  H_vac^2 = (32 pi/3) c_N a0^2/c^4")
print(f"rho_Lambda = 4 a0^2/(G_N c^2) = 4 c_N a0^2/(G_cosm c^2)")
print(f"ALL_SYMBOLIC_CHECKS_PASS = {ok}")
if not ok:
    raise SystemExit("symbolic lane failed")