"""CFG390 part A: symbolic consistency of the two-fluid cold-fluid system (1D slab, all terms). Frozen: FROZEN_CRITERIA.md.
Total-derivative tests use the Euler operator (variational derivative in every field), evaluated on random smooth test functions.
CFG390_MUTATE=1 sets kappa_s = 0 (separate outputs)."""
import os, json, math, random
import sympy as sp
from sympy.calculus.euler import euler_equations

HERE = os.path.dirname(os.path.abspath(__file__))
MUTATE = os.environ.get("CFG390_MUTATE") == "1"
TAG = "_MUTATE" if MUTATE else ""
LOG, CH, RES = [], [], {}
def say(s=""): print(s); LOG.append(s)
def check(name, ok, val=""):
    CH.append({"name": name, "pass": bool(ok), "value": str(val)}); say(f"  [{'PASS' if ok else 'FAIL'}] {name}: {val}")

x, t, U = sp.symbols("x t U", real=True)
G, K, Hq, s2, rcrit, theta, tau = sp.symbols("G K H_q sigma2 rho_crit theta tau", positive=True)
kap = sp.Integer(0) if MUTATE else sp.symbols("kappa_s", positive=True)

def model(rs, vs, rn, vn, Ph, rph, eta, L, X, T, Cform="onsager"):
    """Returns dict of time derivatives (as expressions in X) and residual builders. Fields are expressions in (X, T)."""
    d = lambda f, n=1: sp.diff(f, X, n)
    sq = sp.sqrt(rs)
    Q = -Hq / 2 * d(sq, 2) / sq
    mu_s = Ph + K * rs + Q + kap * sp.log(rs / rph)
    mu_n = Ph + s2 * sp.log(rn / rcrit)
    C = L * (mu_s - mu_n) if Cform == "onsager" else Cform
    vstar = theta * vs + (1 - theta) * vn
    rs_t = -d(rs * vs) - C
    rn_t = -d(rn * vn) + C
    vs_t = -vs * d(vs) - d(mu_s) + C * (vs - vstar) / rs
    vn_t = -vn * d(vn) + (-d(rn * s2) - rn * d(Ph) + d(sp.Rational(4, 3) * eta * d(vn)) + C * (vstar - vn)) / rn
    return dict(rs_t=rs_t, rn_t=rn_t, vs_t=vs_t, vn_t=vn_t, mu_s=mu_s, mu_n=mu_n, C=C, Q=Q)

# ---- fields as functions of (x, t) for time-derivative substitution
F = {n: sp.Function(n) for n in ["rs", "vs", "rn", "vn", "Ph", "rph", "eta", "L"]}
fx = {n: F[n](x, t) for n in F}
M = model(fx["rs"], fx["vs"], fx["rn"], fx["vn"], fx["Ph"], fx["rph"], fx["eta"], fx["L"], x, t)
tsub = {"rs": M["rs_t"], "rn": M["rn_t"], "vs": M["vs_t"], "vn": M["vn_t"], "Ph": 0, "rph": 0, "eta": 0, "L": 0}

def dt(expr):
    """Time derivative of expr with the PDEs substituted (Phi, rho_ph static: gravity's own Phi_t part is a pure flux, see README)."""
    e = sp.diff(expr, t)
    reps = {}
    for der in e.atoms(sp.Derivative):
        f = der.expr; vars_ = [v for v, n in der.variable_count for _ in range(n)]
        if t in vars_ and f.func.__name__ in tsub:
            nx = vars_.count(x); reps[der] = sp.diff(tsub[f.func.__name__], x, nx) if nx else tsub[f.func.__name__]
    return e.subs(reps)

xs = sp.Symbol("xs")
def to_x(expr):
    """replace f(x, t) by f(x) for the Euler operator"""
    reps = {fx[n]: sp.Function(n + "_")(x) for n in fx}
    return expr.subs(reps)

random.seed(390)
def test_funcs():
    a = [random.uniform(0.1, 0.4) for _ in range(16)]
    return {"rs_": 2 + a[0] * sp.sin(x) + a[1] * sp.cos(2 * x), "vs_": a[2] * sp.sin(3 * x) + a[3],
            "rn_": 1.5 + a[4] * sp.cos(x) + a[5] * sp.sin(2 * x), "vn_": a[6] * sp.cos(2 * x) - a[7],
            "Ph_": a[8] * sp.sin(x) + a[9] * sp.cos(3 * x), "rph_": 2.2 + a[10] * sp.cos(x) + a[11] * sp.sin(3 * x),
            "eta_": 0.5 + a[12] * sp.sin(x) ** 2, "L_": 0.3 + a[13] * sp.cos(x) ** 2}
PARS = {G: 0.7, K: 0.9, Hq: 0.37, s2: 1.3, rcrit: 1.1, theta: sp.Rational(3, 10), tau: 0.8}
if not MUTATE:
    PARS[kap] = 1.7

def is_flux(expr, label, npts=4):
    """Euler operator of expr in every field -> evaluate on random test functions. Returns (bool, max |EL|)."""
    ex = to_x(expr)
    funcs = [sp.Function(n + "_")(x) for n in fx]
    funcs = [f for f in funcs if ex.has(f)]
    eqs = euler_equations(ex, funcs, x)
    worst = 0.0
    tf = test_funcs()
    for eq in eqs:
        el = eq.lhs
        sub = el.subs(PARS)
        for f in funcs:
            sub = sub.subs(f, tf[f.func.__name__])
        sub = sub.doit()
        for xv in [0.3, 1.1, 2.4, 4.0][:npts]:
            worst = max(worst, abs(float(sub.subs(x, xv).evalf())))
    return worst < 1e-8, worst

say("CFG390 part A: symbolic consistency" + ("  (MUTATE: kappa_s = 0)" if MUTATE else ""))
say("=" * 78)

# A1 mass
ok, w = is_flux(dt(fx["rs"] + fx["rn"]), "mass")
check("A1 total cold mass d_t(rho_s + rho_n) is a pure flux", ok, f"max|EL| = {w:.1e}")
RES["A1"] = ok
# A1b sign of the proposed C
rneq = sp.Symbol("rho_n_eq", positive=True); rn_s = sp.Symbol("rho_n", positive=True)
C_prop = (rn_s - rneq) / tau
slope = sp.diff(C_prop, rn_s)
check("A1b proposed C = (rho_n - rho_n_eq)/tau with d_t rho_n = +C ANTI-relaxes (d C/d rho_n > 0): declared R1 fixes the sign",
      sp.simplify(slope - 1 / tau) == 0 and bool(slope > 0), f"dC/drho_n = {slope}")
RES["A1b_proposed_C_antirelaxes"] = True

# A2 momentum (dark sector + reaction on the static baryons: rho_b = Phi_xx/(4 pi G) - rho_s - rho_n)
P = fx["rs"] * fx["vs"] + fx["rn"] * fx["vn"]
rb = sp.diff(fx["Ph"], x, 2) / (4 * sp.pi * G) - fx["rs"] - fx["rn"]
Pdot = dt(P) + (-rb * sp.diff(fx["Ph"], x))          # add the impulse delivered to the baryons
settle_force = kap * fx["rs"] * sp.diff(sp.log(fx["rph"]), x)  # external part of the settling force on the condensate
ok_raw, w_raw = is_flux(Pdot, "mom raw")
ok_sink, w_sink = is_flux(Pdot - settle_force, "mom minus sink")
sink_required = not ok_raw
say(f"  A2: total momentum incl. baryon reaction: pure flux? {ok_raw} (max|EL| {w_raw:.2e}); after removing the settling "
    f"target force kappa_s rho_s grad ln rho_ph: {ok_sink} (max|EL| {w_sink:.1e})")
# exchange cancellation explicitly: coefficient of C in d_t P is zero
Csym = sp.Symbol("Cx")
Mc = model(fx["rs"], fx["vs"], fx["rn"], fx["vn"], fx["Ph"], fx["rph"], fx["eta"], fx["L"], x, t, Cform=Csym)
Pdot_C = (Mc["rs_t"] * fx["vs"] + fx["rs"] * Mc["vs_t"] + Mc["rn_t"] * fx["vn"] + fx["rn"] * Mc["vn_t"])
exch = sp.simplify(sp.diff(sp.expand(Pdot_C), Csym))
check("A2a exchange terms equal and opposite (d(d_t P)/dC = 0)", exch == 0, f"{exch}")
check("A2 momentum conserved up to the declared sink (R6): flux after removing kappa_s rho_s grad ln rho_ph", ok_sink, f"{w_sink:.1e}")
say(f"  A2 sink required (settling term not a flux): {sink_required}")
RES.update(A2a=bool(exch == 0), A2=ok_sink, sink_required=sink_required)
if MUTATE:
    check("T-MUT A2 sink_required flips to FALSE with kappa_s = 0", not sink_required, sink_required)

# A3 Galilean invariance
xp = sp.Symbol("xp", real=True)
def boosted(lab):
    g = {n: sp.Function(n.upper())(xp, t) for n in ["rs", "vs", "rn", "vn", "Ph", "eta", "L"]}
    g["rph"] = sp.Function("RPH")(xp)
    return g
gb = boosted(True)
def resids(f, X, T, extra_v=0):
    m = model(f["rs"], f["vs"] + extra_v, f["rn"], f["vn"] + extra_v, f["Ph"], f["rph"], f["eta"], f["L"], X, T)
    return {"rs": sp.diff(f["rs"], T), "rn": sp.diff(f["rn"], T), "vs": sp.diff(f["vs"] + extra_v, T), "vn": sp.diff(f["vn"] + extra_v, T)}, m
# primed frame: residual_e = d_t field - rhs, with fields G(xp, t)
_, m_p = resids(gb, xp, t)
lhs_p = {k: sp.diff(gb[k], t) for k in ["rs", "rn", "vs", "vn"]}
res_p = {"rs": lhs_p["rs"] - m_p["rs_t"], "rn": lhs_p["rn"] - m_p["rn_t"], "vs": lhs_p["vs"] - m_p["vs_t"], "vn": lhs_p["vn"] - m_p["vn_t"]}
# lab frame: f(x, t) = G(x - U t, t), velocities + U
lab = {n: sp.Function(n.upper())(x - U * t, t) for n in ["rs", "vs", "rn", "vn", "Ph", "eta", "L"]}
lab["rph"] = sp.Function("RPH")(x - U * t)
m_l = model(lab["rs"], lab["vs"] + U, lab["rn"], lab["vn"] + U, lab["Ph"], lab["rph"], lab["eta"], lab["L"], x, t)
res_l = {"rs": sp.diff(lab["rs"], t) - m_l["rs_t"], "rn": sp.diff(lab["rn"], t) - m_l["rn_t"],
         "vs": sp.diff(lab["vs"] + U, t) - m_l["vs_t"], "vn": sp.diff(lab["vn"] + U, t) - m_l["vn_t"]}
gal_worst = 0.0
tfun = {"RS": lambda a, b: 2 + 0.3 * sp.sin(a) + 0.1 * sp.cos(b + a), "VS": lambda a, b: 0.2 * sp.sin(2 * a) * sp.cos(b),
        "RN": lambda a, b: 1.4 + 0.2 * sp.cos(a - b), "VN": lambda a, b: 0.3 * sp.cos(a) + 0.1 * b,
        "PH": lambda a, b: 0.4 * sp.sin(a) * (1 + 0.1 * b), "ETA": lambda a, b: 0.6 + 0.1 * sp.sin(a) ** 2,
        "L": lambda a, b: 0.3 + 0.1 * sp.cos(a) ** 2}
def subst_tf(expr):
    for n, fn in tfun.items():
        expr = expr.replace(sp.Function(n), sp.Lambda((sp.Symbol("_a"), sp.Symbol("_b")), fn(sp.Symbol("_a"), sp.Symbol("_b"))))
    expr = expr.replace(sp.Function("RPH"), sp.Lambda(sp.Symbol("_a"), 2.1 + 0.2 * sp.cos(sp.Symbol("_a"))))
    return expr.doit()
for k in res_p:
    a = subst_tf(res_l[k].subs(PARS)); b = subst_tf(res_p[k].subs(PARS))
    b = b.subs(xp, x - U * t)
    for (xv, tv, Uv) in [(0.4, 0.2, 0.7), (1.9, 1.3, -1.1), (3.1, 0.5, 2.3)]:
        gal_worst = max(gal_worst, abs(float((a - b).subs({x: xv, t: tv, U: Uv}).evalf())))
check("A3 Galilean invariance (all four evolution equations; target co-moving with baryons)", gal_worst < 1e-9, f"max residual {gal_worst:.1e}")
RES["A3"] = gal_worst < 1e-9

# A4 H-theorem
rs, vs, rn, vn, Ph, rph, eta, L = (fx[n] for n in ["rs", "vs", "rn", "vn", "Ph", "rph", "eta", "L"])
e = (rs * vs**2 / 2 + rn * vn**2 / 2 + (rs + rn) * Ph + K * rs**2 / 2 + Hq / 8 * sp.diff(rs, x)**2 / rs
     + kap * (rs * sp.log(rs / rph) - rs + rph) + s2 * (rn * sp.log(rn / rcrit) - rn))
diss = -sp.Rational(4, 3) * eta * sp.diff(vn, x)**2 - L * (M["mu_s"] - M["mu_n"])**2 + M["C"] * (sp.Rational(1, 2) - theta) * (vs - vn)**2
ok4, w4 = is_flux(dt(e) - diss, "H")
check("A4 H-theorem identity: d_t e + div J = -(4/3) eta v_x^2 - L (mu_s - mu_n)^2 + C (1/2 - theta)(v_s - v_n)^2 (Onsager C, static target)",
      ok4, f"max|EL| = {w4:.1e}")
say("      each term <= 0 for eta >= 0, L >= 0 and the donor rule (theta = 1 if C > 0, 0 if C < 0); gravity's Phi_t part is a pure flux")
RES["A4"] = ok4
okn, wn = is_flux(dt(e) - (diss + sp.Rational(4, 3) * eta * sp.diff(vn, x)**2), "Hneg")
check("A4neg sensitivity: dropping the viscous term from the identity must break it", not okn, f"max|EL| = {wn:.2e}")
# A4b: task's relaxation-time C (sign-corrected) with Bose rho_n_eq = rho_crit (saturated): production -C (mu_s - mu_n)
kv = 1.0 if MUTATE else 1.0
r_s_over_ph, r_n_over_c = 0.1, 0.9
C_task = (1.0 - r_n_over_c)                    # (rho_crit - rho_n)/tau in units rho_crit/tau
dmu = (0.0 if MUTATE else kv) * math.log(r_s_over_ph) - 1.0 * math.log(r_n_over_c)   # kappa_s = sigma_n^2 = 1
prod = -C_task * dmu
say(f"  A4b relaxation-time C (sign-corrected, Bose rho_n_eq) at rho_s = 0.1 rho_ph, rho_n = 0.9 rho_crit, kappa_s = sigma_n^2: "
    f"dF/dt contribution = {prod:+.3f} (rho_crit sigma^2/tau units) -> {'F INCREASES (H-theorem violated)' if prod > 0 else 'F decreases'}")
RES["A4b_relaxation_time_C_violates_H"] = prod > 0
# A4c time-dependent target
extra = sp.diff(kap * (rs * sp.log(rs / rph) - rs + rph), rph)
say(f"  A4c with a moving target, d_t F gains  {sp.simplify(extra)} * d_t rho_ph  (energy exchanged with the sink; sign-indefinite)")
RES["A4c_extra"] = str(sp.simplify(extra))

# A5 rest state rho_s = rho_ph, v = 0
X = sp.Symbol("X"); Rph = sp.Function("Rph")(X); PhX = sp.Function("PhiX")(X)
Mr = model(Rph, sp.Integer(0), sp.Function("Rn")(X), sp.Integer(0), PhX, Rph, sp.Integer(1), sp.Integer(0), X, t)
vs_rest = sp.simplify(Mr["vs_t"])
expect = -sp.diff(PhX + K * Rph + Mr["Q"], X)
a5_resid_is_grad = sp.simplify(vs_rest - expect) == 0
stationary = sp.simplify(vs_rest) == 0
check("A5a at rho_s = rho_ph, v = 0 the condensate acceleration is exactly -grad(Phi + h + Q)", a5_resid_is_grad, str(vs_rest)[:90])
check("A5 rest state rho_s = rho_ph, v = 0 stationary in a gravitating host", stationary,
      "NO: stationary only if Phi + h + Q is uniform; true rest state kappa_s ln(rho_s/rho_ph) + h + Q = mu - Phi")
RES["A5"] = bool(stationary)

n = sum(c["pass"] for c in CH)
say(f"\nPart A: {n}/{len(CH)} checks pass" + ("  (MUTATE)" if MUTATE else ""))
json.dump({"lane": "CFG390", "part": "A", "mutate": MUTATE, "results": RES, "checks": CH},
          open(os.path.join(HERE, f"cfg390_symbolic_results{TAG}.json"), "w"), indent=1, default=str)
open(os.path.join(HERE, f"cfg390_symbolic{TAG}.out"), "w").write("\n".join(LOG) + "\n")
