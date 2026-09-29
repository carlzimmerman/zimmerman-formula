"""CFG152 (independent referee of CFG124, door 10): shared machinery.

Own code, written from CFG152_FROZEN_CRITERIA.md only; it imports nothing from other lanes.

The action (CFG124's, signature (-,+,+,+), c = 1, M_P^2 = 1/(8 pi G)):
    S = INT d^4x sqrt(-g) [ (M_P^2/2) R + lambda (g^{mu nu} d_mu phi d_nu phi + 1) - V(phi) + c_box (box phi)^2 ]
with c_box = gt M_P^2 / 2 in the main run (gt = 8 pi G gamma).  MUTATE a: -gt M_P^2/2; b: gt M_P^2; 1: -gt M_P^2.

Everything is expanded to second order by brute force from the 4-metric (inverse metric, Christoffel
symbols, Ricci scalar, box phi from its covariant definition), using truncated series in a bookkeeping
parameter eps.  No ADM split and no linearised Einstein-Hilbert formula are used.
"""
import hashlib
import json
import os
import time
from pathlib import Path

import sympy as sp

LANE = Path(__file__).resolve().parent
SPEC_REL = Path("campaign_fresh_gravity") / "CFG152_FROZEN_CRITERIA.md"
SPEC_SHA_COMMITTED = "ed516168d11de161d4beea8fc8169c60204e08988035513861bed9d0db0233e9"  # commit 7be9ce713


def repo_root():
    env = os.environ.get("ZF_REPO")
    if env:
        return Path(env).resolve()
    p = LANE
    for _ in range(12):
        if (p / ".git").exists():
            return p
        p = p.parent
    return LANE.parent.parent


def spec_sha():
    return hashlib.sha256((repo_root() / SPEC_REL).read_bytes()).hexdigest()


def get_mode(allowed):
    m = os.environ.get("MUTATE", "").strip() or "main"
    if m not in allowed:
        raise SystemExit(f"MUTATE={m} is not applicable to this script (allowed: {allowed})")
    return m


class Report:
    """Collects printed lines and checks; writes <stem>.out and <stem>_results.json next to the script."""

    def __init__(self, name, mode):
        self.name, self.mode = name, mode
        stem = name if mode == "main" else f"{name}_MUTATE_{mode}"
        self.out_path = LANE / f"{stem}.out"
        self.json_path = LANE / f"{stem}_results.json"
        self.lines, self.checks = [], []
        self.results = {"script": name, "mode": mode}
        self.t0 = time.time()

    def p(self, *a):
        s = " ".join(str(x) for x in a)
        print(s, flush=True)
        self.lines.append(s)

    def check(self, name, passed, detail="", kind="pass line"):
        self.checks.append({"name": name, "passed": bool(passed), "kind": kind, "detail": str(detail)})
        self.p(f"[{'PASS' if passed else 'FAIL'}] {name} ({kind}) {detail}")
        return bool(passed)

    def finish(self):
        failed = [c["name"] for c in self.checks if not c["passed"]]
        rc = 0 if not failed else 1
        self.results.update(checks=self.checks, failed=failed, n_failed=len(failed), exit_code=rc,
                            runtime_s=round(time.time() - self.t0, 1))
        self.p(f"== {self.name} mode={self.mode}: {len(self.checks)} checks, {len(failed)} failed -> exit {rc}")
        if failed:
            self.p("   failed: " + "; ".join(failed))
        self.out_path.write_text("\n".join(self.lines) + "\n")
        self.json_path.write_text(json.dumps(self.results, indent=1, default=str))
        return rc


def header(rep):
    sha = spec_sha()
    rep.p(f"spec sha256 = {sha}")
    rep.p(f"committed spec sha256 (7be9ce713) = {SPEC_SHA_COMMITTED}; match = {sha == SPEC_SHA_COMMITTED}")
    rep.results["spec_sha256"] = sha
    rep.results["spec_sha256_match"] = sha == SPEC_SHA_COMMITTED
    rep.p(f"mode = {rep.mode}; sympy {sp.__version__}")


# ---------------------------------------------------------------- symbols
t, x, y, z = sp.symbols("t x y z", real=True)
COORDS = (t, x, y, z)
gt = sp.Symbol("gt", real=True)
Mp2 = sp.Symbol("Mp2", positive=True)
k = sp.Symbol("k", positive=True)
w = sp.Symbol("omega", real=True)

FIELD_NAMES = ["Phi", "B", "Psi", "E", "dphi", "dlam", "h"]
A_ = sp.Function("a", positive=True)      # FRW scale factor a(t)
LAMB = sp.Function("lamb", real=True)      # background multiplier lambda_bar(t)
VF = sp.Function("V", real=True)           # potential along the background, V(phi_bar = t)


def c_box_for(mode):
    """Coefficient of (box phi)^2 in the action, per mode (frozen in the spec)."""
    return {"main": gt * Mp2 / 2, "a": -gt * Mp2 / 2, "b": gt * Mp2, "1": -gt * Mp2}[mode]


def tx_fields():
    return {n: sp.Function(n, real=True)(t, x) for n in FIELD_NAMES}


# ---------------------------------------------------------------- truncated series (orders 0, 1, 2)
class S3:
    __slots__ = ("c",)

    def __init__(self, c0=0, c1=0, c2=0):
        self.c = (sp.sympify(c0), sp.sympify(c1), sp.sympify(c2))

    def __add__(self, o):
        o = as_s3(o)
        return S3(*(a + b for a, b in zip(self.c, o.c)))

    __radd__ = __add__

    def __sub__(self, o):
        o = as_s3(o)
        return S3(*(a - b for a, b in zip(self.c, o.c)))

    def __rsub__(self, o):
        return as_s3(o) - self

    def __neg__(self):
        return S3(*(-a for a in self.c))

    def __mul__(self, o):
        o = as_s3(o)
        a, b = self.c, o.c
        return S3(a[0] * b[0], a[0] * b[1] + a[1] * b[0], a[0] * b[2] + a[1] * b[1] + a[2] * b[0])

    __rmul__ = __mul__

    def diff(self, *v):
        return S3(*(sp.diff(a, *v) for a in self.c))

    def expand(self):
        return S3(*(sp.expand(a) for a in self.c))


def as_s3(o):
    return o if isinstance(o, S3) else S3(o, 0, 0)


def s3sum(items):
    tot = S3(0, 0, 0)
    for it in items:
        tot = tot + it
    return tot


# ---------------------------------------------------------------- the brute-force expansion
def expand_action(background, c_box, mimetic=True, keep_potential=True, log=None):
    """Second-order expansion of sqrt(-g) * Lagrangian.

    background: 'mink' (a = 1, lambda_bar = 0, V = 0) or 'frw' (a(t), lambda_bar(t), V(t) general).
    mimetic=False gives GR alone (only the Einstein-Hilbert term; dphi and dlam absent).
    Returns dict with L0, L1, L2 (expanded), the fields, and internal checks.
    """
    F = tx_fields()
    Phi, B, Psi, E, dphi, dlam, h = (F[n] for n in FIELD_NAMES)
    if background == "mink":
        a, lamb, V0, V1, V2 = sp.Integer(1), sp.Integer(0), sp.Integer(0), sp.Integer(0), sp.Integer(0)
    else:
        a, lamb = A_(t), LAMB(t)
        V0 = VF(t) if keep_potential else sp.Integer(0)
        V1, V2 = sp.diff(V0, t), sp.diff(V0, t, 2)   # V'(phi), V''(phi) at phi = t
    tick = time.time()
    # metric: exactly linear in eps
    g0 = sp.diag(-1, a**2, a**2, a**2)
    g1 = sp.zeros(4, 4)
    g1[0, 0] = -2 * Phi
    g1[0, 1] = g1[1, 0] = a * sp.diff(B, x)
    g1[1, 1] = a**2 * (-2 * Psi + 2 * sp.diff(E, x, 2))
    g1[2, 2] = a**2 * (-2 * Psi + h)
    g1[3, 3] = a**2 * (-2 * Psi - h)
    g = [[S3(g0[m, n], g1[m, n], 0) for n in range(4)] for m in range(4)]
    g0i = g0.inv()
    gi1 = -g0i * g1 * g0i
    gi2 = g0i * g1 * g0i * g1 * g0i
    gi = [[S3(g0i[m, n], sp.expand(gi1[m, n]), sp.expand(gi2[m, n])) for n in range(4)] for m in range(4)]
    # Christoffel symbols Gamma^r_{mn}
    dg = {(m, n, l): g[m][n].diff(COORDS[l]) for m in range(4) for n in range(4) for l in range(4)}
    Gam = {}
    for r in range(4):
        for m in range(4):
            for n in range(m, 4):
                val = s3sum(gi[r][s] * (dg[(s, n, m)] + dg[(s, m, n)] - dg[(m, n, s)]) for s in range(4))
                val = (val * sp.Rational(1, 2)).expand()
                Gam[(r, m, n)] = Gam[(r, n, m)] = val
    # Ricci tensor R_{mn} = d_r G^r_mn - d_n G^r_rm + G^r_rl G^l_mn - G^r_nl G^l_rm   (MTW sign convention)
    Ric = {}
    for m in range(4):
        for n in range(m, 4):
            val = S3()
            for r in range(4):
                val = val + Gam[(r, m, n)].diff(COORDS[r]) - Gam[(r, r, m)].diff(COORDS[n])
                for l in range(4):
                    val = val + Gam[(r, r, l)] * Gam[(l, m, n)] - Gam[(r, n, l)] * Gam[(l, r, m)]
            Ric[(m, n)] = Ric[(n, m)] = val.expand()
    Rs = s3sum(gi[m][n] * Ric[(m, n)] for m in range(4) for n in range(4)).expand()
    # sqrt(-g) and 1/sqrt(-g)
    eps = sp.Symbol("eps")
    gmat = sp.Matrix(4, 4, lambda m, n: g0[m, n] + eps * g1[m, n])
    Dd = sp.expand(-gmat.det(method="berkowitz"))
    D0, D1, D2 = Dd.coeff(eps, 0), Dd.coeff(eps, 1), Dd.coeff(eps, 2)
    checks = {"D0_is_a6": sp.simplify(D0 - a**6) == 0}
    sD0 = a**3
    sqrtg = S3(sD0, sp.expand(sD0 * D1 / (2 * D0)), sp.expand(sD0 * (D2 / (2 * D0) - D1**2 / (8 * D0**2))))
    isqrtg = S3(1 / sD0, sp.expand(-D1 / (2 * D0) / sD0),
                sp.expand((3 * D1**2 / (8 * D0**2) - D2 / (2 * D0)) / sD0))
    if background == "frw":
        Rbar = sp.simplify(Rs.c[0] - 6 * (sp.diff(a, t, 2) / a + (sp.diff(a, t) / a)**2))
        checks["Rbar_is_6(add/a+H^2)"] = Rbar == 0
    else:
        checks["Rbar_is_0"] = sp.simplify(Rs.c[0]) == 0
    EH = Rs * (Mp2 / 2)
    out = {"fields": F, "a": a, "checks": checks}
    if not mimetic:
        L = (sqrtg * EH).expand()
    else:
        phi = S3(t, dphi, 0)
        dphi_ = [phi.diff(c) for c in COORDS]
        X = s3sum(gi[m][n] * dphi_[m] * dphi_[n] for m in range(4) for n in range(4)).expand()
        W = [s3sum(sqrtg * gi[m][n] * dphi_[n] for n in range(4)).expand() for m in range(4)]
        box = (isqrtg * s3sum(W[m].diff(COORDS[m]) for m in range(4))).expand()
        box2 = s3sum(gi[m][n] * (dphi_[m].diff(COORDS[n])
                                 - s3sum(Gam[(r, m, n)] * dphi_[r] for r in range(4)))
                     for m in range(4) for n in range(4)).expand()
        checks["box_divergence_equals_christoffel_form"] = all(
            sp.simplify(sp.expand(u - v)) == 0 for u, v in zip(box.c, box2.c))
        lam = S3(lamb, dlam, 0)
        Vphi = S3(V0, dphi * V1, dphi**2 * V2 / 2)
        bracket = EH + lam * (X + 1) - Vphi + (box * box) * c_box
        L = (sqrtg * bracket).expand()
        out.update(X=X, box=box)
    out.update(L0=L.c[0], L1=L.c[1], L2=L.c[2], runtime=time.time() - tick)
    if log:
        log(f"   expansion ({background}, mimetic={mimetic}) done in {out['runtime']:.1f} s; "
            f"L2 has {len(sp.Add.make_args(out['L2']))} terms; internal checks {checks}")
    return out


# ---------------------------------------------------------------- Fourier Hermitian form (constant backgrounds)
def fourier_matrix(L2, fields):
    """M[a,b] = d^2 <L2> / ds_a dr_b with F_a = s_a e^{-i th} + r_a e^{+i th}, th = k x - omega t.
    Total derivatives drop out identically; M is Hermitian for a real Lagrangian."""
    Em = sp.Symbol("Em")
    n = len(fields)
    s = sp.symbols(f"s0:{n}")
    r = sp.symbols(f"r0:{n}")
    idx = {f.func: i for i, f in enumerate(fields)}
    rep = {}
    for d in L2.atoms(sp.Derivative):
        fn = d.expr.func
        if fn not in idx:
            continue
        vc = dict(d.variable_count)
        m_, n_ = vc.get(t, 0), vc.get(x, 0)
        if set(vc) - {t, x}:
            raise ValueError(f"unexpected derivative {d}")
        i = idx[fn]
        rep[d] = (s[i] * (sp.I * w)**m_ * (-sp.I * k)**n_ / Em
                  + r[i] * (-sp.I * w)**m_ * (sp.I * k)**n_ * Em)
    for f in fields:
        rep[f] = s[idx[f.func]] / Em + r[idx[f.func]] * Em
    Ls = sp.expand(L2.xreplace(rep) * Em**2)
    L0 = Ls.coeff(Em, 2)
    return sp.Matrix(n, n, lambda i_, j_: sp.expand(sp.diff(L0, s[i_], r[j_])))


def lie_gauge_vectors(fields_order, a=1, lam_bar_dot=0):
    """Scalar gauge vectors from delta g = -Lie_xi g_bar, delta phi = -xi^r d_r t, delta lambda = -xi^r d_r lambda_bar,
    with xi^mu = (xi0, d_x zeta, 0, 0), both proportional to exp(i(kx - omega t)).  Minkowski only (a = 1)."""
    ph = sp.exp(sp.I * (k * x - w * t))
    Xi0, Z = sp.symbols("Xi0 Z")
    xi = [Xi0 * ph, sp.diff(Z * ph, x), 0, 0]
    gbar = sp.diag(-1, a**2, a**2, a**2)
    Lg = sp.Matrix(4, 4, lambda m, n: sum(
        xi[r] * sp.diff(gbar[m, n], COORDS[r]) + gbar[r, n] * sp.diff(xi[r], COORDS[m])
        + gbar[m, r] * sp.diff(xi[r], COORDS[n]) for r in range(4)))
    dg = -Lg
    comps = {
        "Phi": -dg[0, 0] / 2,
        "B": dg[0, 1] / (a * sp.I * k),
        "Psi": -(dg[2, 2] + dg[3, 3]) / (4 * a**2),
        "h": (dg[2, 2] - dg[3, 3]) / (2 * a**2),
        "dphi": -xi[0] * 1,          # phi_bar = t
        "dlam": -xi[0] * lam_bar_dot,
    }
    comps["E"] = (dg[1, 1] / a**2 + 2 * comps["Psi"]) / (2 * (sp.I * k)**2)
    vecs = []
    for par in (Xi0, Z):
        vecs.append(sp.Matrix([sp.simplify(sp.diff(comps[nm], par) / ph) for nm in fields_order]))
    return vecs


def poly_in_w(expr):
    """Return (m, Poly) with expr = w^m * P(w), P(0) != 0."""
    P = sp.Poly(sp.expand(expr), w)
    coeffs = P.all_coeffs()[::-1]          # ascending
    m = 0
    while m < len(coeffs) and sp.simplify(coeffs[m]) == 0:
        m += 1
    if m == len(coeffs):
        return None, None
    Q = sp.Poly(sum(sp.simplify(c) * w**(i - m) for i, c in enumerate(coeffs) if i >= m), w)
    return m, Q
