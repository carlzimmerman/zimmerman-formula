#!/usr/bin/env python3
"""Q01 -- LEAN CERTIFICATION OF THE FIRST-FLIGHT LADDER via exact R-cores (door: P01 'PENDING').
Derives, in exact sympy rational arithmetic, for m in {1,2,4,6} the polynomial core
P~_m(R) with I_m = int_0^1 P~_m(R) dR (targets 3/4, 5/12, 1/4, 149/700), then
Lean-certifies all four as exact 1D polynomial integrals (FTC idiom of
N03_small_spine.lean). Kills pre-registered in QWAVE_BRIEF.md, written before this run.
Scope (K3): Lean certifies the 1D cores; the 2D->1D reduction is analytic (sympy exact
rational integration over t with artanh parts integrated by parts, V(1)=0 chosen so
V/(1-R^2) is polynomial) and numerically cross-checked at 40 dps by P01's two routes."""
import json, os, subprocess, sys
import sympy as sp

BASE = os.path.dirname(os.path.abspath(__file__))
LEAN_DIR = '/Users/carlzimmerman/new_physics/zimmerman-formula/fable_independent_2026/lean_2026'
targets = {1: sp.Rational(3,4), 2: sp.Rational(5,12), 4: sp.Rational(1,4), 6: sp.Rational(149,700)}
names = {1: 'Chord', 2: 'R2', 4: 'R4', 6: 'R6'}

R, t = sp.symbols('R t', positive=True)
mu = (1 - R**2 - t**2)/(2*R*t)

def g_m(m):
    ch = t
    if m == 1: return ch
    if m == 2:
        return R**2*ch + R*mu*ch**2 + ch**3/3
    if m == 4:
        return (R**4*ch + 2*R**3*mu*ch**2 + (2*R**2*mu**2 + R**2)*ch**3/3
                + R*mu*ch**4/2 + ch**5/5)
    if m == 6:
        return (R**6*ch + 3*R**5*mu*ch**2 + R**4*ch**3 + 4*R**4*mu**2*ch**3
                + 3*R**3*mu*ch**4 + sp.Rational(3,5)*R**2*ch**5
                + 2*R**3*mu**3*ch**4 + sp.Rational(12,5)*R**2*mu**2*ch**5
                + R*mu*ch**6 + ch**7/7)

def derive(m):
    """K1: exact rational core + mpmath 30-dps cross-check; returns (coeffs, ok)."""
    g = sp.expand(g_m(m))
    integrand = sp.Rational(3,4)*R*((t**2 + 1 - R**2)/t**2)*g
    inner = sp.integrate(integrand, (t, 1 - R, 1 + R))
    F = sp.expand(sp.expand_log(sp.expand(inner), force=True))
    h = sp.symbols('h')
    Fh = sp.expand(F.subs(sp.log(1 - R), -h).subs(sp.log(1 + R), h))
    poly = Fh.subs(h, 0)
    Q = sp.cancel(sp.expand((Fh - poly)/h))
    Vanti = sp.integrate(Q, R)
    V = sp.expand(Vanti - Vanti.subs(R, 1))
    qout, rem = sp.div(V, 1 - R**2, R)
    assert sp.simplify(rem) == 0, f"divisibility m={m}: {rem}"
    Ptil = sp.expand(poly - qout)
    I = sp.integrate(Ptil, (R, 0, 1))
    exact_ok = sp.cancel(I - targets[m]) == 0
    import mpmath as mp
    mp.mp.dps = 30
    num = mp.quad(sp.lambdify(R, Ptil, 'mpmath'), [0, 1])
    num_ok = abs(mp.mpf(I) - num) < mp.mpf('1e-28')
    P = sp.Poly(Ptil, R)
    coeffs = [P.coeff_monomial(R**k) for k in range(P.degree() + 1)]
    return coeffs, exact_ok and num_ok, I

checks = []
def check(name, ok, detail=""):
    checks.append({"name": name, "pass": bool(ok), "detail": detail})
    return bool(ok)

all_cores, k1 = {}, True
for m in [1, 2, 4, 6]:
    coeffs, ok, I = derive(m)
    k1 = k1 and ok
    all_cores[m] = coeffs
    check(f"K1 sympy exact core m={m} (target {targets[m]})", ok,
          f"I={I}; deg={len(coeffs)-1}; coeffs={[str(c) for c in coeffs]}")
check("K1 all four cores exact in sympy rational arithmetic", k1, "")

# ---- Lean generation (N03_small_spine FTC idiom, degree-8 engine)
def lean_rat(c):
    c = sp.Rational(c)
    return f"({c.p} : ℝ) / {c.q}" if c.q != 1 else f"({c.p} : ℝ)"

MAXDEG = 8
NCOEF = MAXDEG + 1
cargs = " ".join(f"c{k}" for k in range(NCOEF))
ctype = " ".join(f"c{k}" for k in range(NCOEF))  # FIX-FORWARD 2026-09-24: single binder group (c0 c1 ... : R), cf. N03_small_spine.lean; first run had (c0 : R c1 : R ...) -> parse errors

anti_terms = " +\n    ".join(
    (f"(fun y : ℝ => c0 * y)" if k == 0 else f"(fun y : ℝ => (c{k} / {k+1}) * y ^ {k+1})")
    for k in range(NCOEF))
poly_terms = " + ".join((f"c0" if k == 0 else f"c{k} * x ^ {k}") for k in range(NCOEF))
value_terms = " + ".join((f"c0" if k == 0 else f"c{k} / {k+1}") for k in range(NCOEF))

deriv_chain = []
for k in range(NCOEF - 1, 1, -1):
    prefix = " + ".join((f"(fun y : ℝ => c0 * y)" if j == 0 else f"(fun y : ℝ => (c{j} / {j+1}) * y ^ {j+1})")
                        for j in range(k))
    last = f"(fun y : ℝ => (c{k} / {k+1}) * y ^ {k+1})"
    deriv_chain.append(
        f"  rw [deriv_add (by fun_prop : DifferentiableAt ℝ ({prefix}) x)\n"
        f"                (by fun_prop : DifferentiableAt ℝ {last} x)]")
deriv_chain.append(
    f"  rw [deriv_add (by fun_prop : DifferentiableAt ℝ (fun y : ℝ => c0 * y) x)\n"
    f"                (by fun_prop : DifferentiableAt ℝ (fun y : ℝ => (c1 / 2) * y ^ 2) x)]")
deriv_chain_str = "\n".join(deriv_chain)

lean = f"""import Mathlib

/-!
# Q01 — the first-flight ladder certified as exact R-core polynomial integrals

Companion to deepseek_push/Q01_r6_lean.py (P01's E[int r^6 ds] = 149/700, M05's
3/4 / 5/12 / 1/4).  For each first-flight moment I_m the lane derives, in exact
sympy rational arithmetic, an explicit even polynomial P~_m(R) on [0,1] with
I_m = ∫₀¹ P~_m dR (route: per-R exact mu->t change of variables t = chord, the
log/atanh terms integrated by parts with the V(1)=0 antiderivative so V/(1-R²)
is polynomial — the divisibility is CHECKED, not assumed).  Lean certifies the
four one-dimensional polynomial integrals below EXACTLY (FTC engine of
N03_small_spine.lean).

SCOPE (pre-registered K3): Lean certifies the 1D cores.  The 2D->1D reduction is
analytic (sympy exact rationals, recorded in Q01_r6_lean.py) and numerically
cross-checked at 40 dps by P01's two independent routes (agreement 2.87e-42,
P01_r6_moment.py/.json) — it is NOT a 2D Lean certification.
-/

namespace Q01

noncomputable section

open scoped intervalIntegral

/-- Antiderivative of a degree-8 polynomial (function-level sum). -/
def coreAnti ({ctype} : ℝ) : ℝ → ℝ :=
  {anti_terms}

/-- The polynomial itself. -/
def corePoly ({ctype} : ℝ) : ℝ → ℝ :=
  fun x : ℝ => {poly_terms}

/-- deriv (coreAnti) = corePoly, termwise. -/
lemma q01_deriv_coreAnti ({ctype} : ℝ) : deriv (coreAnti {cargs}) = corePoly {cargs} := by
  funext x
  unfold coreAnti corePoly
{deriv_chain_str}
  change deriv (fun y : ℝ => c0 * id y) x + {' + '.join(f'deriv (fun y : ℝ => (c{k} / {k+1}) * y ^ {k+1}) x' for k in range(1, NCOEF))}
      = {poly_terms}
  simp_rw [deriv_const_mul_field, deriv_pow_field, deriv_id]
  simp
  ring_nf

/-- Differentiability of the antiderivative everywhere. -/
lemma q01_diff_coreAnti ({ctype} x : ℝ) : DifferentiableAt ℝ (coreAnti {cargs}) x := by
  unfold coreAnti
  fun_prop

/-- Continuity of the polynomial on [0,1]. -/
lemma q01_cont_corePoly ({ctype} : ℝ) :
    ContinuousOn (corePoly {cargs}) (Set.uIcc 0 1) := by
  unfold corePoly
  apply ContinuousOn.mono (by continuity :
    ContinuousOn (fun x : ℝ => {poly_terms}) Set.univ)
  intro x hx
  simp

/-- Exact polynomial integral on [0,1]. -/
lemma q01_int_core_01 ({ctype} : ℝ) :
    (∫ x in (0 : ℝ)..1, corePoly {cargs} x) = {value_terms} := by
  rw [intervalIntegral.integral_deriv_eq_sub' (coreAnti {cargs})]
  · dsimp [coreAnti]
    norm_num <;> ring_nf
  · exact q01_deriv_coreAnti {cargs}
  · intro x hx
    exact q01_diff_coreAnti {cargs} x
  · exact q01_cont_corePoly {cargs}
"""

def core_theorem(m, coeffs):
    nm = names[m]
    cs = [sp.Rational(0)] * (MAXDEG + 1)
    for k, c in enumerate(coeffs):
        cs[k] = sp.Rational(c)
    arglist = " ".join(f"({lean_rat(c)})" for c in cs)  # FIX-FORWARD 2026-09-24: parenthesize each rational arg so corePoly ((3:R)/8) ... parses as application
    copterm = " + ".join(f"{lean_rat(cs[k])} * R ^ {k}" for k in range(MAXDEG + 1))
    return f"""
/-- I_{m} = ∫₀¹ P~_{{m}} dR = {sp.Rational(targets[m])} (sympy-exact core; see Q01_r6_lean.py). -/
theorem q01Core{nm} : (∫ R in (0 : ℝ)..1, {copterm}) = ({targets[m].p} : ℝ) / {targets[m].q} := by
  have hp : (∫ R in (0 : ℝ)..1, {copterm})
      = (∫ R in (0 : ℝ)..1, corePoly {arglist} R) := by
    apply intervalIntegral.integral_congr
    intro w _
    simp only [corePoly]
    ring
  rw [hp]
  rw [q01_int_core_01 {arglist}]
  norm_num
"""

for m in [1, 2, 4, 6]:
    lean += core_theorem(m, all_cores[m])

lean += """
-- FIX-FORWARD 2026-09-24 (4th): no closing end — the anonymous noncomputable section
-- must be closed before `end Q01`; N03_small_spine.lean precedent is to let EOF auto-close.
"""
for m in [1, 2, 4, 6]:
    lean += f"#print axioms q01Core{names[m]}\n"

lean_path = os.path.join(LEAN_DIR, 'Q01_r6_core.lean')
with open(lean_path, 'w') as f:
    f.write(lean)

# ---- compile
proc = subprocess.run(['lake', 'env', 'lean', 'Q01_r6_core.lean'], cwd=LEAN_DIR,
                      capture_output=True, text=True, timeout=1200)
out = proc.stdout + proc.stderr
with open(os.path.join(LEAN_DIR, 'Q01_r6_core.out'), 'w') as f:
    f.write(out)
has_error = ('error' in out.lower())
has_sorry = ('sorry' in out.lower())
k2 = (proc.returncode == 0) and (not has_error) and (not has_sorry)
check("K2 Lean exit 0, no error, zero sorry", k2, f"returncode={proc.returncode}; out={out[:600]}")

result = {
    "lane": "Q01_r6_lean", "lean_file": lean_path,
    "cores": {names[m]: {"coeffs": [str(sp.Rational(c)) for c in all_cores[m]],
                          "target": str(targets[m])} for m in [1, 2, 4, 6]},
    "checks": checks, "exit0": bool(k1 and k2),
}
with open(os.path.join(BASE, 'Q01_results.json'), 'w') as f:
    json.dump(result, f, indent=1)
print("Q01 COMPLETE; lean returncode =", proc.returncode)
print(out[:800])
print("EXIT", 0 if result["exit0"] else 1)
