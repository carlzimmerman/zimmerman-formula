#!/usr/bin/env python3
"""alpha_bar_checker.py -- look-elsewhere check for a candidate closed form for 1/alpha = 137.035999177 (Thomson limit).

Usage
  python3 alpha_bar_checker.py --expr "4*Z**2+3"                      # family size from the expression's shape (MDL count)
  python3 alpha_bar_checker.py --expr "..." --size 3.2e5              # you declare the number of distinct alternatives you could have used
  python3 alpha_bar_checker.py --expr "..." --extra-choices 6 --n-targets 3 --predicted-precision 1e-4 --fitted-reals 0
  python3 alpha_bar_checker.py --delta 3e-11 --log2size 20            # no expression, just the achieved miss and family size
  python3 alpha_bar_checker.py --selftest [--mutate]

Expression names: pi, e, Z (=2*sqrt(8*pi/3)), kappa (=0.5), sqrt, ln, log, exp, factorial. A value below 1 is inverted (it is taken to be alpha).
What is declared / assumed (all printed): family size N (every integer, constant, operation and shape you could have used, counted BEFORE looking
at 137.036), extra multiplicative choices, number of target values (e.g. which scale of alpha), predicted precision (a-priori, before looking),
number of real parameters fitted to alpha, whether the scale of alpha is stated.
lambda = N_distinct * rho * 2 * delta_eff * extra * n_targets,  P = 1 - exp(-lambda),  delta_eff = max(achieved miss, predicted precision).
rho = fraction of distinct family values per unit relative deviation near 137 (0.0250, measured on E2(12) in d1_grammar_sizes.py);
for MDL sizes N_distinct = N_syntactic * 0.084 (E2(12) distinct/syntactic; for >2 operations the true ratio is smaller, so this is conservative against the claim).
The BAR: P < 1e-3 AND miss <= 5e-10 (or the route's own a-priori predicted precision, which then sets delta_eff) AND 0 fitted reals AND scale stated.
Exit code 0 if the candidate clears the bar, 1 otherwise (selftest: 0 if the checker behaves as specified).
"""
import argparse, ast, json, math, os, sys
import mpmath as mp
import bar_lib as B

mp.mp.dps = 40
DUP_E2 = 0.0838     # distinct/syntactic for E2(12): 44,208,847 / 527,484,450 (d1)
RHO_DEFAULT = 0.0250  # E2(12) rho_frac (d1)
try:
    _cal = B.load_cal()
    RHO_DEFAULT = _cal["E2_12"]["rho_frac"]
    DUP_E2 = _cal["E2_12"]["N_distinct"] / _cal["E2_12"]["N_syntactic"]
except Exception:
    pass

_ALLOWED = {"pi": mp.pi, "e": mp.e, "Z": 2 * mp.sqrt(8 * mp.pi / 3), "kappa": mp.mpf("0.5")}
_FUN = {"sqrt": mp.sqrt, "ln": mp.log, "log": mp.log, "exp": mp.exp, "factorial": mp.factorial}


def _ev(n):
    if isinstance(n, ast.Constant):
        return mp.mpf(n.value)
    if isinstance(n, ast.Name):
        return _ALLOWED[n.id]
    if isinstance(n, ast.UnaryOp):
        v = _ev(n.operand)
        return -v if isinstance(n.op, ast.USub) else v
    if isinstance(n, ast.BinOp):
        a, b = _ev(n.left), _ev(n.right)
        return {ast.Add: lambda: a + b, ast.Sub: lambda: a - b, ast.Mult: lambda: a * b, ast.Div: lambda: a / b, ast.Pow: lambda: a ** b}[type(n.op)]()
    if isinstance(n, ast.Call):
        return _FUN[n.func.id](*[_ev(a) for a in n.args])
    raise ValueError(ast.dump(n))


def evaluate_expr(expr):
    v = _ev(ast.parse(expr, mode="eval").body)
    inverted = False
    if v < 1:
        v = 1 / v; inverted = True
    return v, inverted


def assess(expr=None, delta=None, size=None, log2size=None, intmax=12, extra_choices=1.0, n_targets=1, predicted_precision=0.0,
           fitted_reals=0, scale_stated=True, rho=None, verbose=True):
    notes = []
    if expr is not None:
        v, inv = evaluate_expr(expr)
        d = float(abs(v / mp.mpf("137.035999177") - 1))
        if delta is None:
            delta = d
        notes.append(f"expression value 1/alpha = {mp.nstr(v, 14)}{' (inverted from alpha)' if inv else ''}; miss = {d:.3e} = {d/B.DELTA_CODATA:.3g} sigma_CODATA")
    if delta is None:
        raise SystemExit("need --expr or --delta")
    if size is not None:
        Nd = float(size); src = "declared distinct family size"
    elif log2size is not None:
        Nd = 2.0 ** log2size; src = "declared log2 size (taken as distinct)"
    elif expr is not None:
        lg, st = B.mdl_size(expr, intmax=intmax)
        Nd = 2.0 ** lg * DUP_E2
        src = f"MDL typed-tree count 2^{lg:.1f} ({st['nb']} binary ops, integer bound {st['maxint']}) x distinct/syntactic {DUP_E2:.3f}"
    else:
        raise SystemExit("need a size: --size, --log2size or --expr")
    Nd *= extra_choices
    r = B.evaluate(delta, Nd, rho if rho is not None else RHO_DEFAULT, n_targets=n_targets, predicted_precision=predicted_precision,
                   fitted_reals=fitted_reals, scale_stated=scale_stated)
    r.update(N_eff=Nd, size_source=src, notes=notes)
    if verbose:
        for n in notes:
            print(n)
        print(f"family size N_eff = {Nd:.3g} ({math.log2(Nd):.1f} bits) [{src}] x extra choices {extra_choices:g}; targets {n_targets}; rho = {rho if rho is not None else RHO_DEFAULT:.4f}")
        print(f"delta_eff = {r['delta_eff']:.3e};  expected chance hits lambda = {r['lam']:.4g};  look-elsewhere P = {r['p']:.4g}")
        print(f"  c1 P < {B.BAR_P:g}: {r['c1_lookelsewhere']}    c2 precision (miss <= {B.BAR_DELTA:g} or within 2x own predicted precision): {r['c2_precision']}")
        print(f"  c3 zero fitted reals: {r['c3_no_fitted_real']}    c4 scale of alpha stated: {r['c4_scale_stated']}")
        print("VERDICT:", "CLEARS THE BAR" if r["clears"] else "DOES NOT CLEAR THE BAR")
        if r["clears"]:
            print("  (clearing the bar means only: not explained by chance in the declared family. It is a numerical match, not yet a derivation: the principle must FORCE each choice.)")
    return r


def selftest(mutate=False):
    import bar_lib
    if mutate:
        bar_lib.BAR_P = 2.0      # MUTATE: accept any probability; the negative controls must now fail
        bar_lib.BAR_DELTA = 1.0
    fails = []

    def chk(name, cond):
        print(f"  [{'PASS' if cond else 'FAIL'}] {name}")
        if not cond:
            fails.append(name)
    r = assess(expr="4*Z**2+3", verbose=False)
    chk("4Z^2+3 rejected (chance-level, misses CODATA by 2e5 sigma)", not r["clears"] and r["p"] > 0.5)
    r = assess(expr="9/(8*pi**4)*(pi**5/(2**4*factorial(5)))**(1/4)", verbose=False)
    chk("Wyler as free numerology rejected", not r["clears"])
    r = assess(expr="9/(8*pi**4)*(pi**5/(2**4*factorial(5)))**(1/4)", size=1, verbose=False)
    chk("Wyler with N=1 (forced) passes P but fails precision -> rejected", not r["clears"] and r["c1_lookelsewhere"] and not r["c2_precision"])
    r = assess(delta=1e-12, log2size=15, verbose=False)
    chk("positive control: 1e-12 match in a 2^15 family clears", r["clears"])
    r = assess(delta=1e-12, log2size=60, verbose=False)
    chk("same match in a 2^60 family is rejected", not r["clears"])
    r = assess(delta=1e-12, log2size=15, fitted_reals=1, verbose=False)
    chk("a fitted real parameter is rejected", not r["clears"])
    r = assess(delta=1e-12, log2size=15, n_targets=1e6, verbose=False)
    chk("target-scale multiplicity of 1e6 is rejected", not r["clears"])
    r = assess(delta=1e-5, log2size=5, predicted_precision=1e-2, verbose=False)
    chk("route that predicted only 1e-2 and hit 1e-5 is scored at 1e-2 (rejected at N=32)", not r["clears"] or mutate)
    r = assess(delta=1e-3, log2size=3, verbose=False)
    chk("a 1e-3 match never clears (precision)", not r["clears"])
    r = assess(delta=3e-10, log2size=12, verbose=False)
    chk("a CODATA-precision match in a 2^12 family clears", r["clears"])
    r = assess(delta=3e-10, log2size=32, verbose=False)
    chk("a CODATA-precision match in a 2^32 family does not clear", not r["clears"])
    print("FAILED:", fails if fails else "none")
    return 1 if fails else 0


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--expr"); ap.add_argument("--delta", type=float); ap.add_argument("--size", type=float); ap.add_argument("--log2size", type=float)
    ap.add_argument("--intmax", type=int, default=12); ap.add_argument("--extra-choices", type=float, default=1.0)
    ap.add_argument("--n-targets", type=float, default=1.0); ap.add_argument("--predicted-precision", type=float, default=0.0)
    ap.add_argument("--fitted-reals", type=int, default=0); ap.add_argument("--scale-not-stated", action="store_true")
    ap.add_argument("--rho", type=float); ap.add_argument("--selftest", action="store_true"); ap.add_argument("--mutate", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        sys.exit(selftest(a.mutate))
    r = assess(expr=a.expr, delta=a.delta, size=a.size, log2size=a.log2size, intmax=a.intmax, extra_choices=a.extra_choices,
               n_targets=a.n_targets, predicted_precision=a.predicted_precision, fitted_reals=a.fitted_reals,
               scale_stated=not a.scale_not_stated, rho=a.rho)
    sys.exit(0 if r["clears"] else 1)
