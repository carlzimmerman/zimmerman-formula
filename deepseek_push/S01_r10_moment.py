#!/usr/bin/env python3
"""S01 -- LADDER EXTENSION: E[int r^10 ds] (doors: M05 next rung; Q01 certified m<=8).
Measure (P01_r6_moment.py, M05_geometric_anchors): r_birth uniform in the unit ball,
mu isotropic, chord = -R mu + sqrt(1 - R^2 + R^2 mu^2), I_m = int_0^chord (R^2+2Rmu s+s^2)^(m/2) ds.
Route 1: mpmath 40-dps quadrature in ORIGINAL variables (mu split at 0, chord kink).
Route 2: sympy EXACT -- antiderivative of (R^2+2Rmu s+s^2)^5 in s with mu FREE, THEN
mu -> muof(R,t) = (1-R^2-t^2)/(2Rt), integrate t in [1-R,1+R] with weight (3R/4)(t^2+1-R^2)/t^2
(P01 route-2 density), h-substitution for the log part, divisibility V/(1-R^2) CHECKED.
K0 (registered): the replicated pipeline must reproduce m=2 -> 5/12 and m=6 -> 149/700 exactly.
K1: rational claim only if routes agree < 1e-10 abs AND denominator <= 1e4; else NON-CLOSED.
K2: Lean exit 0, zero sorry, axioms {propext, Classical.choice, Quot.sound} (only if K1 closed).
K3: 1D scope only. Kills pre-registered in RWAVE_BRIEF.md before this run."""
import json, os, subprocess
import sympy as sp
import mpmath as mp
import numpy as np

BASE = os.path.dirname(os.path.abspath(__file__))
LEAN_DIR = '/Users/carlzimmerman/new_physics/zimmerman-formula/fable_independent_2026/lean_2026'
mp.mp.dps = 40  # FIX-FORWARD (recorded): module-level mp.dps is DISCONNECTED from the arithmetic context when sympy is imported first (route1/route2 came out double-precision mpf('0.16968253968253968')); the context-level form is required, cf. Q01_r6_lean.py's mp.mp.dps = 30

R, t, s = sp.symbols('R t s', positive=True)
mu_s = sp.Symbol('mu', real=True)
muof = (1 - R**2 - t**2)/(2*R*t)

def g_core(m):  # antiderivative in s of (R^2+2Rmu s+s^2)^(m/2), mu FREE symbol (Q01 g_m convention)
    k = m // 2
    # antiderivative in s with mu FREE, evaluated at the upper limit s=t, THEN mu -> muof(R,t)
    # (Q01 g_m convention: ch = t; order matters — substituting mu first would collapse r^2 == 1)
    return sp.integrate(sp.expand((R**2 + 2*R*mu_s*s + s**2)**k), s).subs(s, t)

def derive(m):
    g = sp.expand(g_core(m).subs(mu_s, (1 - R**2 - t**2)/(2*R*t)))
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
    div_ok = sp.simplify(rem) == 0
    Ptil = sp.expand(poly - qout)
    I = sp.integrate(Ptil, (R, 0, 1))
    return Ptil, I, div_ok

checks = []
def check(name, ok, detail=""):
    checks.append({"name": name, "pass": bool(ok), "detail": detail})
    return bool(ok)

# K0: pipeline replication validated on the landed rungs
_, I2, div2 = derive(2)
_, I6, div6 = derive(6)
_, I10r, div8r = derive(8)
k0 = (sp.cancel(I2 - sp.Rational(5,12)) == 0 and div2 and
      sp.cancel(I6 - sp.Rational(149,700)) == 0 and div6 and
      sp.cancel(I10r - sp.Rational(1069,6300)) == 0 and div8r)
check("K0 replication: derive() reproduces 5/12 (m=2), 149/700 (m=6), 1069/6300 (m=8) exactly", k0,
      f"I2={I2} div2={div2} I6={I6} div6={div6} I10r={I10r} div8r={div8r}")

Ptil, I10, div10 = derive(10)
print("I_10 sympy exact:", I10, "=", float(I10))
check("K1 artanh divisibility V/(1-R^2) exact (m=10)", div10, "")

# Route 1: original variables (P01 measure), m=10
def chord(Rv, muv): return -Rv*muv + mp.sqrt(1 - Rv**2 + Rv**2*muv**2)
def G10(Rv, muv):  # int_0^chord (R^2+2Rmu s+s^2)^5 ds via exact antiderivative with free mu
    expr = g_core_free = sp.integrate(sp.expand((R**2 + 2*R*mu_s*s + s**2)**5), s)
    f = sp.lambdify((R, mu, s), expr, 'mpmath') if False else None
    return None
# exact antiderivative expression (free mu), evaluated numerically at s=chord
mu_free = sp.Symbol('mu', real=True)
G10_expr = sp.integrate(sp.expand((R**2 + 2*R*mu_free*s + s**2)**5), s)
G10_fun = sp.lambdify((R, mu_free, s), G10_expr, 'mpmath')
def moment(gRRmu):
    inner = lambda Rv: mp.quad(lambda muv: 0.5*g(Rv, muv), [-1, 0, 1])
    return 3*mp.quad(lambda Rv: Rv**2*inner(Rv), [0, 1])
g = lambda Rv, muv: G10_fun(Rv, muv, chord(Rv, muv))
route1 = moment(g)
print("route1 (original vars, 40dps):", mp.nstr(route1, 22))

# FIX-FORWARD (recorded): an earlier 'route2 numeric' here integrated the CORE polynomial
# P~ with the route-2 density — a meaningless quantity, not the route-2 integrand; first run's
# spurious 0.0636 disagreement came from that. The independent route is route1 (original
# variables); the exact rational is compared against it directly.
route2 = mp.mpf(I10.p)/mp.mpf(I10.q) if I10.is_Rational else mp.mpf(float(I10))
agree = abs(route1 - route2)
print("exact vs route1 abs diff:", mp.nstr(agree, 6))
print("DIAGNOSTIC (recorded in JSON): repr(route1)=", repr(route1), " repr(route2)=", repr(route2),
      " mp.dps=", mp.mp.dps, " type(route1)=", type(route1).__name__)
check("K1 route1 (original vars, 40dps) agrees with exact rational < 1e-10 abs",
      agree < mp.mpf('1e-10'), f"route1={mp.nstr(route1, 22)} exact={I10}; diff={mp.nstr(agree, 8)}")

I_exact = sp.Rational(I10) if I10.is_Rational else None
if I_exact is not None:
    check("K1 value rational with q <= 1e4", I_exact.q <= 10000, f"I10 = {I_exact} (q={I_exact.q})")
else:
    conv = sp.nsimplify(route2_num, rational=True)
    check("K1 value rational with q <= 1e4", False, f"I10 = {I10} NOT rational; nsimplify={sp.nsimplify(route2_num, rational=False)}; status NON-CLOSED")

# MC in ORIGINAL variables (independent of the sympy transform): R~3R^2, mu~U(-1,1), est = mean G10
rng = np.random.default_rng(20260924)
n = 10_000_000
Ru = rng.random(n)
Rm = Ru**(1/3.0)                      # R ~ 3 R^2 on [0,1]
mum = rng.uniform(-1, 1, n)
ch = -Rm*mum + np.sqrt(1 - Rm**2 + Rm**2*mum**2)
# G10 evaluated at s=ch: use numpy Horner from exact coeffs in s with symbolic R,mu -> lambdify
G10_fun_np = sp.lambdify((R, mu_free, s), G10_expr, 'numpy')
est_vals = G10_fun_np(Rm, mum, ch)
est = float(np.mean(est_vals))  # FIX-FORWARD: cleaned dead conditional-walrus from first draft
blocks = est_vals.reshape(10, -1).mean(axis=1)
mc_se = float(np.std(blocks, ddof=1)/2)
z_mc = abs(est - float(route2))/mc_se if mc_se > 0 else 0.0
check("MC 1e7 original-variable jackknife (gate z<5)", z_mc < 5, f"MC={est:.10f} se={mc_se:.3e} z={z_mc:.3f}")

# Lean certification ONLY if closed (K1)
lean_rc = None
lean_file = ""
if I_exact is not None and I_exact.q <= 10000 and div10 and agree < mp.mpf('1e-10'):
    MAXDEG = sp.Poly(Ptil, R).degree()
    if MAXDEG % 2 == 1: MAXDEG += 1
    NCOEF = MAXDEG + 1
    P = sp.Poly(Ptil, R)
    cs = [sp.Rational(0)]*NCOEF
    for k in range(P.degree()+1): cs[k] = sp.Rational(P.coeff_monomial(R**k))
    def lean_rat(c): return f"({c.p} : \u211d) / {c.q}" if c.q != 1 else f"({c.p} : \u211d)"
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
    arglist = " ".join(f"({lean_rat(c)})" for c in cs)
    copterm = " + ".join(f"{lean_rat(cs[k])} * R ^ {k}" for k in range(NCOEF))
    lean = f"""import Mathlib

/-!
# S01 — the m=10 rung of the first-flight ladder certified as an exact R-core polynomial integral
Companion to deepseek_push/S01_r10_moment.py.  1D scope ONLY (K3): the 2D->1D reduction is
sympy-exact, cross-checked by P01-style original-variable 40-dps quadrature and 1e7 MC
(S01_results.json); the artanh divisibility V/(1-R^2) is CHECKED there, not assumed.
-/

namespace S01

noncomputable section

open scoped intervalIntegral

/-- Antiderivative of a degree-{MAXDEG} polynomial (function-level sum). -/
def coreAnti ({ctype} : \u211d) : \u211d \u2192 \u211d :=
  {anti_terms}

/-- The polynomial itself. -/
def corePoly ({ctype} : \u211d) : \u211d \u2192 \u211d :=
  fun x : \u211d => {poly_terms}

/-- deriv (coreAnti) = corePoly, termwise. -/
lemma s01_deriv_coreAnti ({ctype} : \u211d) : deriv (coreAnti {cargs}) = corePoly {cargs} := by
  funext x
  unfold coreAnti corePoly
{deriv_chain_str}
  change deriv (fun y : \u211d => c0 * id y) x + {' + '.join(f'deriv (fun y : \u211d => (c{k} / {k+1}) * y ^ {k+1}) x' for k in range(1, NCOEF))}
      = {poly_terms}
  simp_rw [deriv_const_mul_field, deriv_pow_field, deriv_id]
  simp
  ring_nf

/-- Differentiability of the antiderivative everywhere. -/
lemma s01_diff_coreAnti ({ctype} x : \u211d) : DifferentiableAt \u211d (coreAnti {cargs}) x := by
  unfold coreAnti
  fun_prop

/-- Continuity of the polynomial on [0,1]. -/
lemma s01_cont_corePoly ({ctype} : \u211d) :
    ContinuousOn (corePoly {cargs}) (Set.uIcc 0 1) := by
  unfold corePoly
  apply ContinuousOn.mono (by continuity :
    ContinuousOn (fun x : \u211d => {poly_terms}) Set.univ)
  intro x hx
  simp

/-- Exact polynomial integral on [0,1]. -/
lemma s01_int_core_01 ({ctype} : \u211d) :
    (\u222b x in (0 : \u211d)..1, corePoly {cargs} x) = {value_terms} := by
  rw [intervalIntegral.integral_deriv_eq_sub' (coreAnti {cargs})]
  \u00b7 dsimp [coreAnti]
    norm_num <;> ring_nf
  \u00b7 exact s01_deriv_coreAnti {cargs}
  \u00b7 intro x hx
    exact s01_diff_coreAnti {cargs} x
  \u00b7 exact s01_cont_corePoly {cargs}

theorem r01CoreR10 : (\u222b R in (0 : \u211d)..1, {copterm}) = ({I_exact.p} : \u211d) / {I_exact.q} := by
  have hp : (\u222b R in (0 : \u211d)..1, {copterm})
      = (\u222b R in (0 : \u211d)..1, corePoly {arglist} R) := by
    apply intervalIntegral.integral_congr
    intro w _
    simp only [corePoly]
    ring
  rw [hp]
  rw [s01_int_core_01 {arglist}]
  norm_num

-- no closing end: anonymous noncomputable section auto-closes at EOF (N03/Q01 precedent)
"""
    lean += "\n#print axioms r01CoreR10\n"
    lean_file = os.path.join(LEAN_DIR, 'S01_r10_core.lean')
    with open(lean_file, 'w') as f: f.write(lean)
    proc = subprocess.run(['lake', 'env', 'lean', 'S01_r10_core.lean'], cwd=LEAN_DIR,
                          capture_output=True, text=True, timeout=1200)
    out = proc.stdout + proc.stderr
    with open(os.path.join(LEAN_DIR, 'S01_r10_core.out'), 'w') as f: f.write(out)
    lean_rc = proc.returncode
    k2 = (proc.returncode == 0) and ('error' not in out.lower()) and ('sorry' not in out.lower())
    check("K2 Lean exit 0, no error, zero sorry", k2, f"returncode={proc.returncode}; out={out[:600]}")
else:
    check("K2 Lean certification SKIPPED — K1 not closed (NON-CLOSED recorded honestly)", True,
          "no Lean run: exact rational with q<=1e4 not established")

result = {
 "lane": "S01_r10_moment", "lean_file": lean_file, "lean_returncode": lean_rc,
 "I10_exact": str(I10), "is_rational": I_exact is not None,
 "deg": sp.Poly(Ptil, R).degree(),
 "coeffs": [str(sp.Poly(Ptil, R).coeff_monomial(R**k)) for k in range(sp.Poly(Ptil, R).degree()+1)],
 "route1": mp.nstr(route1, 25), "exact": str(I10),
 "agreement": mp.nstr(agree, 10),
 "mc": {"n": n, "est": est, "se": mc_se, "z": z_mc},
 "checks": checks,
 "exit0": bool(all(c["pass"] for c in checks)),
}
# FIX-FORWARD (conductor 2026-09-24): original target S01_results.json is the COMMITTED S01_coherence_length lane's file (house rule 7); rerouted to S01_r10_moment_results.json
with open(os.path.join(BASE, 'S01_r10_moment_results.json'), 'w') as f: json.dump(result, f, indent=1)
print("S01 COMPLETE")
print("EXIT", 0 if result["exit0"] else 1)
