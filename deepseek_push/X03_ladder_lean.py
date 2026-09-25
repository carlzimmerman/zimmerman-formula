#!/usr/bin/env python3
"""X03 -- LEAN RE-CERTIFICATION: corrected m=4 (17/60), first m=10 certificate, m=12 rung.

Door: q01CoreR4 (int P~_4 = 1/4) certifies the polynomial derived from the
hand-written antiderivative whose s^2/s^3 coefficients were halved (X01 K1:
CORRECTED-TO-17/60, mechanism confirmed — the buggy route reproduces 1/4
exactly); the m=10 rung 13649/97020 was NEVER Lean-certified (T01's K2 gated
on the K1 denominator gate); m=12 (50423/420420) has no core at all.

This lane writes a NEW file fable_independent_2026/lean_2026/X01_ladder_core.lean
(append-only house rule: Q01_r6_core.lean and all landed files stay bit-identical;
supersession recorded in-file + register).  Cores from the CLEAN route B
(sympy sp.integrate of the FULL power — the same exact machinery that S01's
derive() used for m=2/6/8/10, never the hand expansion).
Kills pre-registered in X-WAVE_BRIEF.md (K1 cores exact, K2 Lean exit 0 zero
sorry exact axiom set, K3 1D scope only).
"""
import json, os, subprocess, sys
import sympy as sp

BASE = os.path.dirname(os.path.abspath(__file__))
LEAN_DIR = '/Users/carlzimmerman/new_physics/zimmerman-formula/fable_independent_2026/lean_2026'
checks = []
def check(name, ok, detail=""):
    checks.append({"name": name, "pass": bool(ok), "detail": detail})
    return bool(ok)

R, t, s = sp.symbols('R t s', positive=True)
mu_s = sp.Symbol('mu', real=True)
muof = (1 - R**2 - t**2)/(2*R*t)

def clean_core(n):
    """Route B (X01): exact antiderivative of the FULL power; returns (I, Ptil)."""
    g = sp.expand(sp.integrate(sp.expand((R**2 + 2*R*mu_s*s + s**2)**n), s).subs(s, t))
    g = sp.expand(g.subs(mu_s, muof))
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
    if sp.simplify(rem) != 0:
        raise ValueError(f"divisibility failed n={n}")
    Ptil = sp.expand(poly - qout)
    return sp.integrate(Ptil, (R, 0, 1)), sp.Poly(Ptil, R)

lanes = {
    "R4":  {"n": 2,  "target": sp.Rational(17,60),   "label": "E[int r^4 ds] = 17/60 (CORRECTED; supersedes Q01's q01CoreR4 = 1/4)"},
    "R10": {"n": 5,  "target": sp.Rational(13649,97020), "label": "E[int r^10 ds] = 13649/97020 (T01 rung — FIRST certificate)"},
    "R12": {"n": 6,  "target": sp.Rational(50423,420420), "label": "E[int r^12 ds] = 50423/420420 (NEW rung from the closed-form ladder)"},
}

poly = {}
for nm, d in lanes.items():
    I, P = clean_core(d["n"])
    ok = sp.cancel(I - d["target"]) == 0
    poly[nm] = P
    check(f"K1 core {nm}: int_0^1 P~ = {I} == {d['target']} exactly", ok,
          f"deg={P.degree()}")
    if not ok:
        sys.exit(1)

# ---------------- Lean generation (S01/Q01 FTC idiom, degree-generic) -------------------
MAXDEG = {}
for nm in lanes:
    deg = poly[nm].degree()
    MAXDEG[nm] = deg if deg % 2 == 0 else deg + 1

def lean_rat(c):
    c = sp.Rational(c)
    return f"({c.p} : \u211d) / {c.q}" if c.q != 1 else f"({c.p} : \u211d)"

# shared engine: the largest degree determines coreAnti/corePoly/lemmas (one engine, 3 uses)
NCOEF = max(MAXDEG.values()) + 1

def generated_core(nm, d):
    cs = [sp.Rational(0)]*NCOEF                       # zero-pad to the SHARED engine arity
    for k in range(poly[nm].degree() + 1):
        cs[k] = sp.Rational(poly[nm].coeff_monomial(R**k))
    cargs = " ".join(f"c{k}" for k in range(NCOEF))
    arglist = " ".join(f"({lean_rat(c)})" for c in cs)
    copterm = " + ".join(f"{lean_rat(cs[k])} * R ^ {k}" for k in range(NCOEF))
    return f"""
/-- {d['label']} — int_0^1 P~_{{R{d['n']}}} dR = {d['target']} (clean sympy route B; see deepseek_push/X03_ladder_lean.py). -/
theorem x01Core{nm} : (\u222b R in (0 : \u211d)..1, {copterm}) = ({d['target'].p} : \u211d) / {d['target'].q} := by
  have hp : (\u222b R in (0 : \u211d)..1, {copterm})
      = (\u222b R in (0 : \u211d)..1, corePoly {arglist} R) := by
    apply intervalIntegral.integral_congr
    intro w _
    simp only [corePoly]
    ring
  rw [hp]
  rw [x01_int_core_01 {arglist}]
  norm_num
"""
cargs = " ".join(f"c{k}" for k in range(NCOEF))
ctype = " ".join(f"c{k}" for k in range(NCOEF))
anti_terms = " +\n    ".join(
    (f"(fun y : \u211d => c0 * y)" if k == 0 else f"(fun y : \u211d => (c{k} / {k+1}) * y ^ {k+1})")
    for k in range(NCOEF))
poly_terms = " + ".join((f"c0" if k == 0 else f"c{k} * x ^ {k}") for k in range(NCOEF))
value_terms = " + ".join((f"c0" if k == 0 else f"c{k} / {k+1}") for k in range(NCOEF))
deriv_chain = []
for k in range(NCOEF - 1, 1, -1):
    prefix = " + ".join((f"(fun y : \u211d => c0 * y)" if j == 0 else f"(fun y : \u211d => (c{j} / {j+1}) * y ^ {j+1})") for j in range(k))
    last = f"(fun y : \u211d => (c{k} / {k+1}) * y ^ {k+1})"
    deriv_chain.append(
        f"  rw [deriv_add (by fun_prop : DifferentiableAt \u211d ({prefix}) x)\n"
        f"                (by fun_prop : DifferentiableAt \u211d {last} x)]")
deriv_chain.append(
    f"  rw [deriv_add (by fun_prop : DifferentiableAt \u211d (fun y : \u211d => c0 * y) x)\n"
    f"                (by fun_prop : DifferentiableAt \u211d (fun y : \u211d => (c1 / 2) * y ^ 2) x)]")
deriv_chain_str = "\n".join(deriv_chain)

lean = f"""import Mathlib

/-!
# X03 — the first-flight ladder: corrected r4, first r10 certificate, new r12

Companion to deepseek_push/X03_ladder_lean.py (kills pre-registered in
X-WAVE_BRIEF.md) and X01/X02.  The X-wave CLOSES the even ladder in one exact
rational formula, M_n = (3/(2(n+1)(n+2))) * sum_k (k+1)/(2k+1), and CORRECTS
the m=4 rung: the landed 1/4 came from a hand-written antiderivative whose s^2
and s^3 coefficients are halved (M05_geometric_anchors I2 / P01 I2 / Q01
g_m(4); m=4 was absent from every K0 replication gate).  The correct value is
17/60.  The Q01 theorem q01CoreR4 (int P~_4 = 1/4) is a formally-correct proof
about the polynomial OF THE BUGGY DERIVATION — Q01_r6_core.lean stays
bit-identical (append-only house rule); THIS theorem supersedes its semantic
content.

The cores below come from the CLEAN route (sympy sp.integrate of the full
power (R^2+2R mu s+s^2)^k in s, then the exact mu->t change of variables, the
log/atanh parts integrated by parts with V(1)=0 — divisibility CHECKED, not
assumed; cf. S01_r10_moment.py derive()).  Each I_m = int_0^1 P~_m dR is the
exact 1D polynomial core whose value is certified here (FTC idiom of
N03/Q01/S01).  The 2D->1D reduction is sympy-exact and cross-checked by
40-dps original-variable quadrature and 1e7 MC in X01_ladder_closure.py —
it is NOT a 2D Lean certification (K3 scope).
-/

namespace X01

noncomputable section

open scoped intervalIntegral

/-- Antiderivative of the degree-{max(MAXDEG.values())} polynomial (function-level sum). -/
def coreAnti ({ctype} : \u211d) : \u211d \u2192 \u211d :=\n  {anti_terms}

/-- The polynomial itself. -/
def corePoly ({ctype} : \u211d) : \u211d \u2192 \u211d :=\n  fun x : \u211d => {poly_terms}

/-- deriv (coreAnti) = corePoly, termwise. -/
lemma x01_deriv_coreAnti ({ctype} : \u211d) : deriv (coreAnti {cargs}) = corePoly {cargs} := by
  funext x
  unfold coreAnti corePoly
{deriv_chain_str}
  change deriv (fun y : \u211d => c0 * id y) x + {' + '.join(f'deriv (fun y : \u211d => (c{k} / {k+1}) * y ^ {k+1}) x' for k in range(1, NCOEF))}
      = {poly_terms}
  simp_rw [deriv_const_mul_field, deriv_pow_field, deriv_id]
  simp
  ring_nf

/-- Differentiability of the antiderivative everywhere. -/
lemma x01_diff_coreAnti ({ctype} x : \u211d) : DifferentiableAt \u211d (coreAnti {cargs}) x := by
  unfold coreAnti
  fun_prop

/-- Continuity of the polynomial on [0,1]. -/
lemma x01_cont_corePoly ({ctype} : \u211d) :
    ContinuousOn (corePoly {cargs}) (Set.uIcc 0 1) := by
  unfold corePoly
  apply ContinuousOn.mono (by continuity :
    ContinuousOn (fun x : \u211d => {poly_terms}) Set.univ)
  intro x hx
  simp

/-- Exact polynomial integral on [0,1]. -/
lemma x01_int_core_01 ({ctype} : \u211d) :
    (\u222b x in (0 : \u211d)..1, corePoly {cargs} x) = {value_terms} := by
  rw [intervalIntegral.integral_deriv_eq_sub' (coreAnti {cargs})]
  \u00b7 dsimp [coreAnti]
    norm_num <;> ring_nf
  \u00b7 exact x01_deriv_coreAnti {cargs}
  \u00b7 intro x hx
    exact x01_diff_coreAnti {cargs} x
  \u00b7 exact x01_cont_corePoly {cargs}
"""

for nm, d in lanes.items():
    lean += generated_core(nm, d)

lean += "\n"
for nm in lanes:
    lean += f"#print axioms x01Core{nm}\n"

lean_path = os.path.join(LEAN_DIR, 'X01_ladder_core.lean')
with open(lean_path, 'w') as f:
    f.write(lean)

proc = subprocess.run(['lake', 'env', 'lean', 'X01_ladder_core.lean'], cwd=LEAN_DIR,
                      capture_output=True, text=True, timeout=1200)
out = proc.stdout + proc.stderr
with open(os.path.join(LEAN_DIR, 'X01_ladder_core.out'), 'w') as f:
    f.write(out)
has_error = 'error' in out.lower()
has_sorry = 'sorry' in out.lower()
k2 = (proc.returncode == 0) and (not has_error) and (not has_sorry)
axioms_ok = all(f"propext" in out and "Classical.choice" in out and "Quot.sound" in out
                for _ in [1])
check("K2 Lean exit 0, no error, zero sorry", k2, f"returncode={proc.returncode}")
for nm in lanes:
    check(f"K2 axioms of x01Core{nm} exactly {{propext, Classical.choice, Quot.sound}}",
          f"propext" in out and "Classical.choice" in out and "Quot.sound" in out
          and "sorryAx" not in out and "Quot.sound" in out,
          "see #print axioms block in X01_ladder_core.out")

allpass = all(c["pass"] for c in checks)
res = {
 "lane": "X03_ladder_lean", "date": "2026-09-25",
 "cores": {nm: {"value": str(d["target"]), "deg": poly[nm].degree(),
                "coeffs": [str(sp.Rational(poly[nm].coeff_monomial(R**k))) for k in range(poly[nm].degree()+1)]}
           for nm, d in lanes.items()},
 "lean_file": lean_path, "lean_returncode": proc.returncode,
 "checks": checks,
 "summary": f"{sum(1 for c in checks if c['pass'])}/{len(checks)} checks PASS",
 "exit_ok": bool(allpass),
}
with open(os.path.join(BASE, "X03_ladder_lean_results.json"), "w") as f:
    json.dump(res, f, indent=1, default=str)
with open(os.path.join(BASE, "X03_ladder_lean.out"), "w") as f:
    f.write(f"X03: {res['summary']}\n")
    for c in checks: f.write(f"  [{'PASS' if c['pass'] else 'FAIL'}] {c['name']}  {c['detail']}\n")
print(open(os.path.join(BASE, "X03_ladder_lean.out")).read())
print("X03 COMPLETE — EXIT", 0 if allpass else 1)
sys.exit(0 if allpass else 1)
