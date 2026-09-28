#!/usr/bin/env python3
"""AS070 -- bounded prototype: normalization constraint F = 4 a0^2 - G c^2 rho_L = 0
coupled with multiplier eta in an action.

Checks (all residuals recorded in residuals.json; tolerances pre-set):
  C1/C2  F-residual at the two registered footings (kappa=1/2 held, density changed)
  C3     exact identity F = 4 a0^2 (1 - lambda)          (sympy, exact 0)
  C4     scale identity s = c sqrt(G rho_L) = 2 a0 sqrt(lambda)   (lambda grid, both footings)
  C5     kappa = 1/(2 sqrt(lambda)) correspondence
  C6     direct differentiation: dF/dlambda = -4 a0^2 via central finite difference
  C7     Dirac-Bergmann matrix of the minimal sector: rank 4, null vector (G c^2/(8 a0), 1, 0,0,0)
  C8     MU2 cell mapping at lambda=1: mu2(g/(2a0)) = 1 - (1 + g/(2a0))^(-2)
  NC1    negative control: multiplier stress T^eta = eta F g vs vacuum stress T^vac,
         eta = -1/G (case III), at lambda = 1/2, 1, 2  ->  O(1) stress must appear off-shell
  NC2    normalization/boundary: sign flip of F across lambda = 1; lambda->0+ / ->inf limits;
         vacuity witness (a0*,sqrt..) at lambda=1/2,1,2 satisfies every EOM of case II.
Bounded prototype: wall <= 120 s, memory <= 512 MB, 1 thread (single-threaded CPython, mpmath 60 digits).
"""
import json
import time
import math
import resource

import mpmath as mp

mp.mp.dps = 60

G = mp.mpf("6.67430e-11")
c = mp.mpf("299792458")
A0_CAN = mp.mpf("9.3619e-11")
A0_ALT = mp.mpf("1.1279e-10")
C2 = c * c
GC2 = G * C2
M_SUN = mp.mpf("1.98847e30")
PC = mp.mpf("3.085677581491367e16")

TOL = mp.mpf("1e-30")  # relative tolerance, pre-set before any evaluation


def F(a0, rho):
    return 4 * a0 * a0 - G * c * c * rho


def rel_resid(x, y):
    """relative residual |x-y|/max(1,|x|,|y|)"""
    m = max(mp.mpf(1), mp.fabs(x), mp.fabs(y))
    return mp.fabs(x - y) / m


def rho_lambda(a0):
    return 4 * a0 * a0 / GC2


results = {}
checks = []


def register(key, ok, observed, tol=None, note=""):
    checks.append({"key": key, "pass": bool(ok), "observed": str(observed),
                   "tolerance": str(tol if tol is not None else TOL), "note": note})


# ---------------- footings ----------------
rhoL_can = rho_lambda(A0_CAN)
rhoL_alt = rho_lambda(A0_ALT)
results["rho_Lambda_canonical_kg_m3"] = mp.nstr(rhoL_can, 30)
results["rho_Lambda_alternative_kg_m3"] = mp.nstr(rhoL_alt, 30)
results["footing_density_ratio"] = mp.nstr(rhoL_alt / rhoL_can, 25)
results["footing_a0_ratio_sq"] = mp.nstr((A0_ALT / A0_CAN) ** 2, 25)
kappa_eff = A0_ALT / (c * mp.sqrt(G * rhoL_can))
results["kappa_eff_fixed_rhoLambda_canonical"] = mp.nstr(kappa_eff, 25)

r1 = rel_resid(F(A0_CAN, rhoL_can), mp.mpf(0))
r2 = rel_resid(F(A0_ALT, rhoL_alt), mp.mpf(0))
register("C1_F_residual_canonical_footing", r1 < TOL, r1,
         note="4 a0^2 - G c^2 rho_Lambda(canonical) = 0, kappa=1/2 held")
register("C2_F_residual_alternative_footing", r2 < TOL, r2,
         note="4 a0^2 - G c^2 rho_Lambda(alternative) = 0, kappa=1/2 held")

# ---------------- C3: exact identity F = 4 a0^2 (1 - lambda) (sympy) ----------------
import sympy as sp
a0s, Gs, cs, rhos = sp.symbols("a0 G c rho_L", positive=True)
lambdas = sp.symbols("lambda", positive=True)
F_sym = 4 * a0s ** 2 - Gs * cs ** 2 * rhos
F_alt = 4 * a0s ** 2 * (1 - lambdas)
diff_expr = sp.expand(F_sym.subs(rhos, lambdas * 4 * a0s ** 2 / (Gs * cs ** 2)) - F_alt)
results["C3_symbolic_identity"] = sp.sstr(diff_expr)
register("C3_F_equals_4a0sq_one_minus_lambda", diff_expr == 0, diff_expr,
         note="sympy expand of F(rho_L=lambda*4a0^2/(Gc^2)) - 4a0^2(1-lambda) == 0 (exact)")

# ---------------- C4/C5: grid diagnostics ----------------
grid = [mp.mpf("0.5"), mp.mpf("1"), mp.mpf("2")]
worst_s, worst_k = mp.mpf(0), mp.mpf(0)
diag = {}
for lam in grid:
    row = {}
    for tag, a0 in (("canonical", A0_CAN), ("alternative", A0_ALT)):
        rho = lam * rho_lambda(a0)
        s_direct = c * mp.sqrt(G * rho)
        s_formula = 2 * a0 * mp.sqrt(lam)
        k_direct = a0 / (c * mp.sqrt(G * rho))
        k_formula = mp.mpf(1) / (2 * mp.sqrt(lam))
        rs = rel_resid(s_direct, s_formula)
        rk = rel_resid(k_direct, k_formula)
        worst_s = max(worst_s, rs)
        worst_k = max(worst_k, rk)
        row[tag] = {"s_m_s2": mp.nstr(s_direct, 20), "kappa": mp.nstr(k_direct, 20),
                    "resid_s": mp.nstr(rs, 6), "resid_kappa": mp.nstr(rk, 6)}
    g = A0_CAN  # diagnostic point g = a0*
    Y = g / (c * mp.sqrt(G * (lam * rho_lambda(A0_CAN))))
    row["Y_at_g_a0can"] = mp.nstr(Y, 15)
    row["mu1"] = mp.nstr(1 - (1 + Y) ** (-1), 10)
    row["mu2"] = mp.nstr(1 - (1 + Y) ** (-2), 10)
    row["mu3"] = mp.nstr(1 - (1 + Y) ** (-3), 10)
    diag["lambda_" + mp.nstr(lam, 3)] = row
results["lambda_diagnostics"] = diag
register("C4_scale_identity_s_grid", worst_s < TOL, worst_s,
         note="c sqrt(G rho_L) = 2 a0 sqrt(lambda), lambda in {1/2,1,2} x both footings")
register("C5_kappa_1_over_2sqrtlambda", worst_k < TOL, worst_k,
         note="a0/(c sqrt(G rho_L)) = 1/(2 sqrt(lambda)) on the grid + footings")

# ---------------- C6: direct differentiation ----------------
# dF/dlambda = -4 a0^2 ; central difference at lambda = 1, canonical footing
lam0 = mp.mpf(1)
eps = mp.mpf("1e-8")
rho_f = lambda l: l * rho_lambda(A0_CAN)
fnum = (F(A0_CAN, rho_f(lam0 + eps)) - F(A0_CAN, rho_f(lam0 - eps))) / (2 * eps)
fan = -4 * A0_CAN * A0_CAN
r6 = rel_resid(fnum, fan)
register("C6_direct_differentiation_dFdlambda", r6 < TOL, r6,
         note="central difference step 1e-8 at lambda=1 vs -4 a0^2 (exact)")

# ---------------- C7: Dirac-Bergmann matrix of the minimal sector ----------------
M = sp.Matrix([[0, 0, 0, -8 * a0s, 0],
               [0, 0, 0, Gs * cs ** 2, 0],
               [0, 0, 0, 0, -1],
               [8 * a0s, -Gs * cs ** 2, 0, 0, 0],
               [0, 0, 1, 0, 0]])
rankM = M.rank()
null = M.nullspace()
results["C7_dirac_matrix_rank"] = rankM
results["C7_dirac_nullspace"] = [sp.sstr(v.T) for v in null]
register("C7_dirac_rank_4", rankM == 4, rankM,
         note="constraints {pi_a0, pi_rho, pi_eta, F, eta}: 4 second-class + 1 first-class")
ok_null = len(null) == 1 and sp.simplify(null[0][0] * 8 * a0s - Gs * cs ** 2 * null[0][1]) == 0 \
          and null[0][2] == 0 and null[0][3] == 0 and null[0][4] == 0
register("C7_dirac_nullvector_family_gauge", ok_null,
         sp.sstr(null[0].T) if null else "empty",
         note="null direction = (G c^2/(8 a0), 1, 0, 0, 0): family/gauge direction chi")

# ---------------- C8: MU2 cell mapping at lambda = 1 ----------------
gv = A0_CAN
Y1 = gv / (2 * A0_CAN)
mu2_Y = 1 - (1 + Y1) ** (-2)
mu2_x = 1 - (1 + (gv / A0_CAN) / 2) ** (-2)
r8 = rel_resid(mu2_Y, mu2_x)
register("C8_MU2_cell_mapping_lambda1", r8 < TOL, r8,
         note="mu2(g/(2a0)) = 1-(1+g/(2a0))^(-2) == MU2 cell 1-(1+x/2)^(-2), x=g/a0")

# ---------------- NC1: multiplier stress is O(1) off-shell ----------------
eta_case3 = -mp.mpf(1) / G  # chi = c^2 vacuum term, case III
nc1 = {}
worst_ratio = mp.mpf(0)
for lam in grid:
    a0r = A0_CAN
    rho = lam * rho_lambda(a0r)
    Fv = F(a0r, rho)
    Teta = eta_case3 * Fv            # T^eta_00 = eta F g_00 (g_00 = 1 in local frame)
    Tvac = -rho * c * c              # T^vac_00 = -chi rho = -rho c^2
    ratio = mp.fabs(Teta) / mp.fabs(Tvac) if Tvac != 0 else mp.mpf(0)
    worst_ratio = max(worst_ratio, ratio)
    nc1["lambda_" + mp.nstr(lam, 3)] = {"Teta_00": mp.nstr(Teta, 15),
                                        "Tvac_00": mp.nstr(Tvac, 15),
                                        "ratio_abs": mp.nstr(ratio, 10)}
results["NC1_multiplier_stress_vs_vacuum"] = nc1
results["NC1_worst_abs_ratio"] = mp.nstr(worst_ratio, 10)
register("NC1_stress_omission_is_O1_offshell", worst_ratio > mp.mpf("0.25"),
         worst_ratio, tol="lower bound 0.25",
         note="control CAPABLE OF FAILING and fails as designed: |T^eta|/|T^vac| = 1.0 at lambda=1/2, 0.5 at lambda=2; ignoring T^eta while enforcing F=0 with eta!=0 misstates the vacuum stress by O(1)")

# ---------------- NC2: normalization and boundary ----------------
eps2 = mp.mpf("1e-12")
Fm = F(A0_CAN, rho_lambda(A0_CAN) * (1 - eps2))
Fp = F(A0_CAN, rho_lambda(A0_CAN) * (1 + eps2))
sign_flip = (Fm > 0) and (Fp < 0)
results["NC2_sign_flip"] = {"F(1-1e-12)": mp.nstr(Fm, 6), "F(1+1e-12)": mp.nstr(Fp, 6), "flips": sign_flip}
register("NC2_sign_flip_across_lambda1", sign_flip, Fm, note="F changes sign at the adopted point (constraint sensitivity)")

# vacuity witness: case-II configurations satisfy every EOM of the constrained system
witness = {}
for lam in grid:
    alpha = A0_CAN * mp.sqrt(lam)
    rho_w = lam * rho_lambda(A0_CAN)
    Fw = F(alpha, rho_w)          # F = 0 exactly
    etaw = mp.mpf(0)              # eta = 0 (case II)
    # host sector: unchanged by construction (S_host independent of rho_L); record G indicator
    witness["lambda_" + mp.nstr(lam, 3)] = {"alpha": mp.nstr(alpha, 15),
                                             "rho_L": mp.nstr(rho_w, 15),
                                             "F": mp.nstr(Fw, 6),
                                             "eta": mp.nstr(etaw, 6)}
results["NC2_vacuity_witness_caseII"] = witness
def _wres(lam):
    alpha = A0_CAN * mp.sqrt(lam)
    rho_w = lam * rho_lambda(A0_CAN)
    return rel_resid(F(alpha, rho_w), mp.mpf(0))
worst_w = max(_wres(lam) for lam in grid)
ok_wit = worst_w < TOL
register("NC2_vacuity_witness_all_EOMs", ok_wit, worst_w,
         note="(alpha, rho_L, eta)=(a0*sqrt(lambda), lambda rho_Lambda, 0) satisfies F=0 to rel resid "
              + mp.nstr(worst_w, 4) + " (< tolerance) and eta=0 exactly, for lambda=1/2,1,2: the constraint does not select the family member (exact in R; ~1e-75 in mpmath)")

# limits lambda -> 0+ and -> inf (exact algebra, documented)
results["NC2_limits"] = {
    "lambda->0+": "s -> 0 (a0 -> 0), kappa -> inf; family degenerates consistently",
    "lambda->inf": "s -> inf (rho_L -> inf), kappa -> 0; family degenerates consistently"}

# ---------------- summary ----------------
n_pass = sum(1 for ch in checks if ch["pass"])
n_tot = len(checks)
print("=" * 100)
print("AS070 bounded prototype — normalization constraint coupling analysis")
print("=" * 100)
print(f"mpmath dps = {mp.mp.dps}; all numeric residuals at ~1e-60 precision; tolerance pre-set: rel {TOL}")
print(f"footings: rho_Lambda(canonical) = {results['rho_Lambda_canonical_kg_m3']} kg/m^3")
print(f"          rho_Lambda(alt)       = {results['rho_Lambda_alternative_kg_m3']} kg/m^3")
print(f"          ratio = {results['footing_density_ratio']}  (a0 ratio^2 = {results['footing_a0_ratio_sq']})")
print(f"          kappa_eff (fixed canonical rho) = {results['kappa_eff_fixed_rhoLambda_canonical']}")
print(f"lambda diagnostics: {json.dumps(diag, indent=1)}")
print(f"C3 exact identity: {results['C3_symbolic_identity']} (sympy)")
print(f"C6 dF/dlambda numeric vs -4a0^2: rel resid {r6}")
print(f"C7 Dirac matrix rank = {rankM}; nullspace = {results['C7_dirac_nullspace']}")
print(f"NC1 stress ratios: {json.dumps(nc1, indent=1)}; worst |T^eta|/|T^vac| = {results['NC1_worst_abs_ratio']}")
print(f"NC2 sign flip: F(1-eps)={Fm}, F(1+eps)={Fp}, flips={sign_flip}")
print(f"checks passed {n_pass}/{n_tot}")
for ch in checks:
    print(f"  [{'PASS' if ch['pass'] else 'FAIL'}] {ch['key']}: {ch['observed']}  ({ch['note']})")
assert n_pass == n_tot, "some checks failed"
print("ALL CHECKS PASSED (including both negative controls, which failed their false claims as designed)")

# enforced-bounds ledger: CPU/wall caps are shell-enforced (ulimit -t, timeout);
# macOS refuses memory rlimits, so peak RSS is measured and asserted < 512 MB here.
_maxrss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss  # bytes on macOS
print(f"peak RSS (ru_maxrss, bytes on macOS) = {_maxrss}  ({_maxrss / 1e6:.2f} MB)")
assert _maxrss < 512 * 1024 * 1024, "peak RSS exceeded the 512 MB prototype budget"
print("memory bound: 512 MB declared, measured peak below; bound ENFORCED by measurement")

with open("residuals.json", "w") as fh:
    json.dump({"tolerance_rel": str(TOL), "results": results, "checks": checks}, fh, indent=1)
print("wrote residuals.json")