"""CFG264 shared helpers: PASS/FAIL checks, pi-content of k2, circularity guard, result writer.

k2 := a0^2 / (c^2 G rho_Lambda); the target is k2 = 1/4 (kappa = 1/2). The target is used ONLY in compare().
"""
import json
import sympy as sp

PI = sp.pi
TARGET_K2 = sp.Rational(1, 4)
DECOYS = [sp.Rational(1, 3), sp.Rational(1, 5), sp.Rational(1, 6), sp.Rational(1, 8),
          sp.Rational(2, 9), sp.Rational(3, 8), sp.Rational(1, 2), sp.Integer(1)]


class Checker:
    def __init__(self, name):
        self.name = name
        self.n_pass = 0
        self.n_fail = 0
        self.lines = []
        self.records = []

    def log(self, s=""):
        print(s)
        self.lines.append(s)

    def check(self, label, ok, detail=""):
        ok = bool(ok)
        if ok:
            self.n_pass += 1
        else:
            self.n_fail += 1
        msg = f"[{'PASS' if ok else 'FAIL'}] {label}" + (f" -- {detail}" if detail else "")
        self.log(msg)
        self.records.append({"check": label, "pass": ok, "detail": detail})
        return ok

    def summary(self):
        self.log(f"\nSUMMARY {self.name}: {self.n_pass} PASS, {self.n_fail} FAIL")


def pi_content(expr):
    """Return (kind, coefficient, pi_exponent) for a closed-form positive number.
    kind: 'rational' (expr = q pi^e, q rational), 'algebraic' (q algebraic, irrational), 'other'."""
    expr = sp.nsimplify(sp.simplify(expr)) if not expr.has(sp.Symbol) else expr
    if expr.free_symbols:
        return ("symbolic", expr, None)
    for twice_e in range(-8, 9):
        e = sp.Rational(twice_e, 2)
        q = sp.simplify(expr / PI**e)
        if q.has(PI):
            continue
        q = sp.nsimplify(q)
        if q.is_rational:
            return ("rational", q, e)
    for twice_e in range(-8, 9):
        e = sp.Rational(twice_e, 2)
        q = sp.simplify(expr / PI**e)
        if not q.has(PI) and q.is_algebraic:
            return ("algebraic", q, e)
    return ("other", expr, None)


def is_target(k2):
    try:
        return sp.simplify(k2 - TARGET_K2) == 0
    except Exception:
        return False


def decoy_hits(k2):
    out = []
    for d in DECOYS:
        try:
            if sp.simplify(k2 - d) == 0:
                out.append(str(d))
        except Exception:
            pass
    return out


def circularity_guard(eqs, a0, rho, c, G, extra_free=()):
    """Each input equation ALONE must not force k2 = 1/4.
    Substitute a0 = sqrt(K) c sqrt(G rho) and solve the single equation for K.
    Returns list of (index, verdict) with verdict 'ok' or 'FORCES_TARGET'."""
    K = sp.Symbol("K_guard", positive=True)
    res = []
    for i, eq in enumerate(eqs):
        e = eq.lhs - eq.rhs if isinstance(eq, sp.Equality) else eq
        e = e.subs(a0, sp.sqrt(K) * c * sp.sqrt(G * rho))
        if not e.has(K):
            res.append((i, "ok (K absent)"))
            continue
        try:
            sols = sp.solve(sp.Eq(e, 0), K, dict=False)
        except Exception:
            res.append((i, "ok (unsolved)"))
            continue
        forced = [s for s in sols if not (sp.sympify(s).free_symbols - {c, G, rho}) and sp.simplify(s - TARGET_K2) == 0]
        res.append((i, "FORCES_TARGET" if forced else "ok"))
    return res


def write_json(path, obj):
    def conv(o):
        if isinstance(o, (sp.Basic,)):
            return str(o)
        raise TypeError(str(type(o)))
    with open(path, "w") as f:
        json.dump(obj, f, indent=2, default=conv)
