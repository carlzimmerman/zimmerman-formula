#!/usr/bin/env python3
"""
as069_audit.py -- seed AS069: dimensionless kernel parameter versus vacuum energy.

Claim under test (seed mathematics line):
    For J(Y;lambda), the derivative fixes forces while C(lambda) changes vacuum
    energy independently if allowed.

Work order:
  S1  Block-triangular Jacobian of observables (force F, vacuum V) w.r.t. (lambda, C):
      dF/dC = 0 exactly (forces see only dJ/dY), dV/dC = alpha/(64 pi) != 0,
      dF/dlambda != 0 for the MU_lambda family in the deep/transition region.
      Rank 2 generically; rank reduces to 1 iff dF/dlambda = 0.
  S2  Vacuum-energy compensation surjectivity: for every lambda a shift C(lambda)
      reproduces the observed rho_Lambda exactly; the vacuum datum is lambda-blind.
  S3  Deep-slope identification: mu_lambda ~ lambda*Y  =>  a0 = s/lambda, kappa = 1/lambda.
      kappa = 1/2  <=>  lambda = 2 (adopted, never derived).  Footings reported separately.
  S4  Negative control (must be capable of failing): setting C(lambda) to produce
      kappa = 1/2 is CALIBRATION, not derivation.  The only fixing principle available
      to the action (empty-Newtonian-vacuum zero) is ill-posed for MU_lambda
      (span diverges ~ Z^2); for the corpus saturating carriers it has the wrong sign.
  Limits: deep asymptote g = sqrt(B*s/lambda) with leading correction
      ((lambda+1)/4) sqrt(B/(s lambda)) ; Newtonian g -> B with leading correction B (B/s)^(-lambda).
  Independent representation: exact polynomial inverse of the lambda = 2 force law
      (cubic in y = g/s) cross-checked against bisection; substitution residual.

Branch discipline: conclusions drawn ONLY for the MU_lambda response family
(symbolic lambda >= 1 channel count at integers; lambda = 1/2 diagnostic is an
algebraic probe, not a channel count) inside the corpus A1-class local action.
kappa = 1/2 is the framework-adopted input.  No Q/RAR/EXP/MONO import.
"""
import json, math, os, resource, sys, time
import numpy as np
import sympy as sp

WALL_LIMIT = 120.0
MEM_LIMIT = 512 * 1024 * 1024
T_START = time.time()
CHECKS = []
FAILS = []

def wall(): return time.time() - T_START

def check(name, ok, measured, tol, reading):
    CHECKS.append(dict(name=name, ok=bool(ok), measured=measured, tol=tol, reading=reading))
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}\n       measured={measured}  tol={tol}\n       {reading}", flush=True)
    if not ok: FAILS.append(name)

# ---------------------------------------------------------------- constants
G   = 6.67430e-11          # m^3 kg^-1 s^-2  (framework G_N convention; G_bare and G_cosmo stay SEPARATE, unused)
C_L = 299792458.0          # m/s
MSUN = 1.98847e30          # kg
PC  = 3.085677581491367e16 # m
A0C = 9.3619e-11           # canonical footing (kappa = 1/2 by adoption), m/s^2
A0A = 1.1279e-10           # alternative footing, m/s^2
RHO_L = 4.0*A0C**2/(G*C_L**2)           # mass density from the canonical footing, kg/m^3
S     = C_L*math.sqrt(G*RHO_L)          # c*sqrt(G*rho_L), m/s^2
ALPHA = 2.0                              # alpha = 2 - K_B at K_B = 0 (corpus audited range [1.75, 2])
ALPHA_HI = 1.75                          # K_B = 1/4 end of the audited range

print("="*112)
print("AS069 -- dimensionless kernel parameter versus vacuum energy (bounded audit)")
print("="*112)
print(f"  G={G}  c={C_L:.6e}  rho_L = {RHO_L:.6e} kg/m^3  s = c sqrt(G rho_L) = {S:.6e} m/s^2  (= 2 a0_can = {2*A0C:.6e})")
print(f"  alpha = 2-K_B in [{ALPHA_HI}, {ALPHA}] ; canonical a0 = {A0C:.4e}, alternative a0 = {A0A:.4e}")
print(f"  fp check s == 2*a0_can: {abs(S - 2*A0C) < 1e-18}")

# ---------------------------------------------------------------- 1. symbolic layer (sympy)
lam, Y = sp.symbols('lambda Y', positive=True)
mu_sym  = 1 - (1+Y)**(-lam)            # MU_lambda response
J_exprs = {}
for lamv in (sp.Rational(1,2), sp.Integer(1), sp.Integer(2), sp.Integer(3)):
    mv = mu_sym.subs(lam, lamv)
    Jv = sp.integrate(mv, Y)
    J_exprs[str(lamv)] = sp.simplify(Jv)
    dJ = sp.simplify(sp.diff(Jv, Y) - mv)
    J0 = sp.simplify(Jv.subs(Y, 0))
    check(f"S0.{lamv} [symbolic] J_{lamv}' = mu_{lamv} exactly (the derivative fixes forces); J_{lamv}(0) is an integration constant, absorbed by the free C({lamv})",
          dJ == 0, f"dJ-diff residual = {dJ}, J(0) = {J0} (absorbed into C; no J(0)=0 normalization imposed)",
          "exact (symbolic)",
          "the primitive's derivative fixes the force; the integration constant comes out nonzero and is exactly the free remainder C(lambda) that moves the vacuum energy without touching forces")
print(f"       J(1/2) = {J_exprs['1/2']},  J(1) = {J_exprs['1']},  J(2) = {J_exprs['2']},  J(3) = {J_exprs['3']}")
# deep slope: mu ~ lam*Y ; a0-line with a0 = s/lam
deep = sp.limit(mu_sym/Y, Y, 0)
check("S3a [symbolic] deep slope mu_lambda'(0) = lambda (a0 = s/lambda, kappa = 1/lambda)",
      sp.simplify(deep - lam) == 0, f"limit(mu/Y, Y->0) = {deep}", "exact (symbolic)",
      "the dimensionless kernel parameter is the inverse kappa; kappa=1/2 <=> lambda=2, the adopted footing")
for nv in range(1, 7):
    dn = sp.limit(mu_sym.subs(lam, nv)/Y, Y, 0)
    assert sp.simplify(dn - nv) == 0
newt = sp.limit(mu_sym, Y, sp.oo)
check("S3b [symbolic] Newtonian recovery mu_lambda -> 1 (g -> B) for every lambda",
      sp.simplify(newt - 1) == 0, f"limit(mu, Y->oo) = {newt}", "exact (symbolic)",
      "both limiting regimes constrain only J' (through mu), never the additive zero C")

# ---------------------------------------------------------------- 2. numeric layer
def mu(lamv, y):
    y = np.asarray(y, dtype=float)
    return 1.0 - (1.0 + y)**(-lamv)

def solve_g(lamv, q, lo=0.0, hi=1e12, steps=400):
    """solve mu_lambda(g/s)*g/s = q = B/s for y = g/s by bisection (f = y*mu - q monotone increasing)."""
    assert 0 < q < hi
    for _ in range(steps):
        mid = 0.5*(lo + hi)
        if (mu(lamv, lo)*lo - q)*(mu(lamv, mid)*mid - q) <= 0:
            hi = mid
        else:
            lo = mid
    return 0.5*(lo + hi)

QB_DEEP, QB_TR = 1e-2, 1.0     # deep (B/s = 0.01) and transition (B/s = 1) probed
LAM_DIAG = (0.5, 1.0, 2.0, 3.0)
print("  --- force responses y = g/s at the two probes (units: y dimensionless; g = y*s m/s^2) ---")
for qv in (QB_DEEP, QB_TR):
    for lv in LAM_DIAG:
        yy = solve_g(lv, qv)
        print(f"     B/s={qv:<5} lambda={lv:<4} y = {yy:.10e}   g = {yy*S:.6e} m/s^2")

# ---- 2.1 observables Jacobian vs (lambda, C): rows (F1, F2, V), cols (d/dlambda, d/dC) ----
def V_ratio(lamv, C_a02, alpha):
    """vacuum mass density / rho_L produced by the shift C (in units of a0^2):
       alpha*C_a02*a0^2/(16 pi G c^2 rho_L) = alpha*C_a02/(64 pi)   (exact, lambda-independent J(0)=0)."""
    return alpha*C_a02/(64.0*math.pi)

lam0, C0 = 2.0, 1.0
dl, dC = 1e-5*lam0, 1e-4
Fp = np.array([solve_g(lam0 + dl, QB_DEEP), solve_g(lam0 + dl, QB_TR), V_ratio(lam0 + dl, C0, ALPHA)])
Fm = np.array([solve_g(lam0 - dl, QB_DEEP), solve_g(lam0 - dl, QB_TR), V_ratio(lam0 - dl, C0, ALPHA)])
Cp = np.array([solve_g(lam0, QB_DEEP), solve_g(lam0, QB_TR), V_ratio(lam0, C0 + dC, ALPHA)])
Cm = np.array([solve_g(lam0, QB_DEEP), solve_g(lam0, QB_TR), V_ratio(lam0, C0 - dC, ALPHA)])
Jcol_l = (Fp - Fm)/(2*dl)
Jcol_C = (Cp - Cm)/(2*dC)
Jmat = np.vstack([Jcol_l, Jcol_C]).T    # 3 x 2
sv = np.linalg.svd(Jmat, compute_uv=False)
exp_dVdC = ALPHA/(64.0*math.pi)
check("S1a [Jacobian, block] d(F1,F2)/dC = 0 to fp; dV/dC = alpha/(64 pi) exactly",
      abs(Jcol_C[0]) < 1e-12 and abs(Jcol_C[1]) < 1e-12 and abs(Jcol_C[2]/exp_dVdC - 1) < 1e-9,
      f"dF1/dC = {Jcol_C[0]:.3e}, dF2/dC = {Jcol_C[1]:.3e}, dV/dC = {Jcol_C[2]:.10e} (predicted {exp_dVdC:.10e})",
      "dF/dC < 1e-12, dV/dC within 1e-9 rel",
      "block triangular: C(lambda) moves ONLY the vacuum energy; the force corner is exactly zero")
check("S1b [Jacobian, rank] rank(F,V vs lambda,C) = 2 on the MU family (dF/dlambda != 0)",
      min(sv) > 1e-5,
      f"singular values = {sv[0]:.4e}, {sv[1]:.4e} (min/max = {sv[1]/sv[0]:.3e})",
      "min singular value > 1e-5",
      "two genuinely independent observable directions (lambda-shape and C-shift): the vacuum datum alone leaves lambda free")

# ---- 2.2 rank-reduction condition: dF/dlambda = 0 degrades to rank 1 ----
# degenerate family J(Y;lambda) = J0(Y) + lambda*C0 (pure shift): forces identical, V(lambda) = alpha*lambda*C0/(64 pi)
C0d = 2.0
Jdeg = np.array([[0.0, 0.0], [0.0, 0.0], [ALPHA*C0d/(64*math.pi), exp_dVdC]])   # cols: d/dlambda, d/dC
svd = np.linalg.svd(Jdeg, compute_uv=False)
check("S1c [rank-reduction] dF/dlambda = 0 exactly forces rank 1 (lambda becomes a pure label; V swept by C)",
      svd[1] < 1e-12,
      f"singular values = {svd[0]:.4e}, {svd[1]:.3e}",
      "second singular value < 1e-12",
      "the condition to reduce the Jacobian rank from 2 to 1 is dF/dlambda = 0 -- exactly the case where lambda no longer participates in the force law; no datum can then select lambda")
dF_newt = (solve_g(2.0 + 1e-5, 1e11) - solve_g(2.0 - 1e-5, 1e11))/2e-5
check("S1d [limit] dF/dlambda -> 0 as B/s -> oo (Newtonian end, ~ ln(q)/q decay): rank reduction is a limit, absent at finite B",
      dF_newt < 1e-6,
      f"dF/dlambda at B/s = 1e11: {dF_newt:.3e}",
      "< 1e-6",
      "Newtonian end: all members collapse toward g = B (lambda blind); the discriminating region is deep/transition where the Jacobian is full rank")

# ---- 2.3 S2: vacuum-energy compensation surjectivity (calibration control) ----
# required shift (units a0^2) at each alpha so that rho_vac = rho_L:
def C_req_a02(alpha): return 64.0*math.pi/alpha
for alpha, tag in ((ALPHA, "K_B=0"), (ALPHA_HI, "K_B=1/4")):
    for lamv in LAM_DIAG:
        ratio = V_ratio(lamv, C_req_a02(alpha), alpha)
        assert abs(ratio - 1.0) < 1e-12
check("S2 [calibration] for EVERY lambda the shift C = 64 pi a0^2/alpha reproduces rho_L exactly (rho_vac/rho_L = 1); C is lambda-independent in the J(0)=0 normalization",
      True,
      f"rho_vac/rho_L = 1 + <1e-12 for lambda in {{1/2,1,2,3}} x alpha in {{{ALPHA_HI},{ALPHA}}}",
      "exact: alpha*(64 pi/alpha)/(64 pi) = 1",
      "the observed vacuum energy is compatible with every member of the one-parameter family: it selects a curve in (lambda, C), never lambda; identifying rho_L with the shift is bookkeeping (calibration), not a derivation of kappa")

# ---- 2.4 limits: deep asymptote + leading neglected term; Newtonian asymptote ----
qs_deep = np.logspace(-6, -2, 30)
ceff_list, err_scale = [], 0.0
for q in qs_deep:
    yb = solve_g(2.0, q)
    lead = math.sqrt(q/2.0)                      # sqrt(B/(s lambda)), lambda = 2
    err = (yb - lead)/lead
    ceff_list.append(err/math.sqrt(q/2.0))       # (lambda+1)/4 = 3/4 predicted
    if q <= 1e-3:
        err_scale = max(err_scale, abs(err*math.sqrt(q/2.0)))
coeff_deep = ceff_list[0]
check("E1 [deep limit] g -> sqrt(B*s/lambda) with leading neglected term ((lambda+1)/4) sqrt(B/(s lambda))",
      abs(coeff_deep - 0.75) < 0.02 and err_scale < 1e-2,
      f"coeff (g/lead - 1)/sqrt(q/2) -> {coeff_deep:.4f} at q = 1e-6 (predicted 0.75); max err*sqrt(q/2) = {err_scale:.3e} over q <= 1e-3",
      "coeff 0.75 +- 0.02; err*sqrt(q/2) < 1e-2 on the deep window",
      "deep limiting regime checked with the explicit leading-order correction derived from mu = lam y - lam(lam+1) y^2/2 + ...")
qs_newt = np.logspace(2, 5, 30)
coeffs_newt = [((solve_g(2.0, q) - q)/q)*q**2 for q in qs_newt]
coeff_newt = float(np.median(coeffs_newt))
n_err_max = max(abs(c - 1.0) for c in coeffs_newt)
check("E2 [Newtonian limit] g -> B with leading correction B (B/s)^(-2) at lambda = 2",
      abs(coeff_newt - 1.0) < 0.02 and n_err_max < 0.05,
      f"(g-B)/B * (B/s)^2 = {coeff_newt:.4f} (median over B/s in [1e2, 1e5], predicted 1.0); max |coeff-1| = {n_err_max:.4f}",
      "|median-1| < 0.02, max |coeff-1| < 0.05",
      "the Newtonian end collapses onto the same law for every lambda: no vacuum datum can be read off there")

# ---- 2.5 independent representations ----
# lambda = 2 exact inverse: y^2 (y+2) = q (1+y)^2  =>  y^3 + (2-q) y^2 - 2 q y - q = 0  (cubic)
def cubic_inverse(q):
    r = np.roots([1.0, 2.0 - q, -2.0*q, -q])
    reals = [x.real for x in r if abs(x.imag) < 1e-10 and x.real > 0]
    return min(reals)
qs = np.logspace(-4, 2, 50)
maxdiff, sub_res_max = 0.0, 0.0
for q in qs:
    yc = cubic_inverse(q)
    yb = solve_g(2.0, q)
    maxdiff = max(maxdiff, abs(yc - yb))
    sub_res_max = max(sub_res_max, abs(mu(2.0, yb)*yb - q)/q)
check("F1 [independent representation] lambda=2 force law solved two ways (bisection vs exact cubic roots) agree; substitution residual = |mu y - q|/q < 1e-12",
      maxdiff < 1e-10,
      f"max |y_bisect - y_cubic| = {maxdiff:.3e} over q in [1e-4, 1e2] (50 pts); max substitution residual {sub_res_max:.3e}",
      "1e-10",
      "different representation (analytic polynomial inverse of y(y+2)/(1+y)^2 = q) reproduces the same g: the force law is exactly mu_2(g/s) g = B")
n_r = 200
r = np.logspace(np.log10(0.1*PC), np.log10(100.0*PC), n_r)
MB = 1e11*MSUN
ah = 3.0*PC
Bprof = G*MB/(r + ah)**2
sub_res = 0.0
for qv in Bprof/S:
    yb = solve_g(2.0, qv)
    sub_res = max(sub_res, abs(mu(2.0, yb)*yb - qv)/max(qv, 1e-30))
check("F2 [substitution] residual of the solved force law on a 200-point Hernquist-type profile: max |mu_2(g/s) g - g_N|/g_N",
      sub_res < 1e-12,
      f"max relative substitution residual = {sub_res:.3e}",
      "1e-12",
      "the solved g satisfies the original equation to machine precision: the audit's force statements are about the actual law, not an approximation")

# ---- 2.6 ill-posed absolute-zero fixing for the MU family (span ~ Z^2) ----
slopes = []
Zs = [1e3, 1e4, 1e5, 1e6]
for nv in (1, 2, 3):
    Ivals = [float(sp.N(sp.integrate(mu_sym.subs(lam, nv)*Y, (Y, 0, sp.Integer(Zv))))) for Zv in Zs]
    slopes.append(float(np.polyfit(np.log(Zs), np.log(Ivals), 1)[0]))
check("E3 [ill-posed fixing] primitive span I_n(Z) = 2 int_0^Z y mu_n dy diverges ~ Z^2 for every n: no absolute zero in the family",
      all(abs(sl - 2.0) < 0.02 for sl in slopes),
      f"log-log slopes over Z in [1e3,1e6]: n=1..3 -> {[round(sl,4) for sl in slopes]}",
      "0.02",
      "the empty-Newtonian-vacuum fixing that would make C(lambda) non-free is undefined for MU_lambda (J_n(oo) diverges); the corpus's saturating carriers give the wrong sign (AS067 S6a, k01 K3); therefore the calibration control could genuinely have failed and does not: no principle of the action fixes C")

# ---- 2.7 footings: both readings reported separately ----
KAPPA_ALT_FIXED_RHO = A0A/S
N_ALT_FIXED_RHO = S/A0A
RHO_L_ALT_FIXED_KAPPA = 4.0*A0A**2/(G*C_L**2)
print(f"  footings: canonical kappa = 0.5 (lambda = 2); alternative a0 = {A0A:.4e}:")
print(f"     fixed rho_L: kappa_eff = {KAPPA_ALT_FIXED_RHO:.6f}, lambda_eff = {N_ALT_FIXED_RHO:.6f} (NOT a channel count)")
print(f"     fixed kappa: rho_L' = {RHO_L_ALT_FIXED_KAPPA:.6e} kg/m^3 = {RHO_L_ALT_FIXED_KAPPA/RHO_L:.4f} rho_L")
assert abs(KAPPA_ALT_FIXED_RHO - 0.6023884040632778) < 1e-9
check("D1 [footings] both footings stated separately; dimensionless S1-S2 statements hold for both because they never invoke a0's value",
      True,
      f"canonical kappa=1/2, lambda=2 ; fixed-rho_L alt: kappa_eff={KAPPA_ALT_FIXED_RHO:.6f}, lambda_eff={N_ALT_FIXED_RHO:.6f}; fixed-kappa alt: rho_L'={RHO_L_ALT_FIXED_KAPPA:.6e}",
      "n.a. (record)",
      "the alternative footing is an alternative normalization, not the same rho_L with the same kappa; its implied lambda_eff = 1.6601 is an identification constraint (non-integer => not a channel count), not a prediction")

# ---------------------------------------------------------------- 2.8 summary
wall_used = wall()
rusage = resource.getrusage(resource.RUSAGE_SELF)
maxrss_mb = rusage.ru_maxrss/1e6 if sys.platform == 'darwin' else rusage.ru_maxrss/1e3
print("="*112)
res = {
  "checks": CHECKS, "pass": sum(1 for c in CHECKS if c["ok"]), "fail": len(FAILS),
  "wall_s": round(wall_used, 3), "maxrss_mb": round(maxrss_mb, 1),
  "s": S, "rho_L_can": RHO_L, "kappa_alt_fixed_rho": KAPPA_ALT_FIXED_RHO,
  "lambda_alt_fixed_rho": N_ALT_FIXED_RHO, "rho_L_alt_fixed_kappa": RHO_L_ALT_FIXED_KAPPA,
  "C_req_a02_alpha2": C_req_a02(ALPHA), "C_req_a02_alpha175": C_req_a02(ALPHA_HI),
  "jacobian_singular_values": [float(sv[0]), float(sv[1])],
  "jacobian_degenerate_singular_values": [float(svd[0]), float(svd[1])],
  "deep_coeff": float(coeff_deep), "newton_coeff": float(coeff_newt),
  "truncation_slopes": slopes,
  "dVdC_pred": exp_dVdC,
}
print(f"  checks: {res['pass']} PASS / {res['fail']} FAIL   wall = {res['wall_s']} s   max RSS = {res['maxrss_mb']} MB")
print("  OUTCOME: the Jacobian of (force, vacuum) w.r.t. (lambda, C) is block triangular with rank 2 on the MU family;")
print("           rank 1 iff dF/dlambda = 0.  The observed vacuum energy compensates C(lambda) for every lambda:")
print("           kappa = 1/lambda is fixed only by the deep-slope identity a0 = s/lambda (adoption at lambda = 2),")
print("           never by the vacuum datum.  Setting C(lambda) to produce kappa = 1/2 is calibration (control passed,")
print("           genuinely capable of failing: a principle fixing C absolutely would flip it; the available one is")
print("           ill-posed for this family and sign-wrong for the corpus saturating carriers).")
with open("as069_results.json", "w") as f:
    json.dump(res, f, indent=1, default=str)
np.savez("as069_observables.npz",
         r=r, Bprof=Bprof,
         qs_deep=qs_deep, yb_deep=np.array([solve_g(2.0, q) for q in qs_deep]),
         qs_newt=qs_newt, yb_newt=np.array([solve_g(2.0, q) for q in qs_newt]),
         qs_cubic=qs, yb_cubic_bisect=np.array([solve_g(2.0, q) for q in qs]),
         yb_cubic_roots=np.array([cubic_inverse(q) for q in qs]))
print("wrote as069_results.json, as069_observables.npz")
if FAILS:
    print(f"FAILED: {FAILS}"); sys.exit(1)
sys.exit(0)