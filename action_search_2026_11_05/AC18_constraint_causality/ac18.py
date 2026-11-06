"""AC18: constraint causality of v3s / AC2q on charged backgrounds. Criteria: FROZEN_CRITERIA.md (5ba6bdfd7c).

Kappa = 1/2 FITTED; not theory closed. Single thread. Run from the repo root:
    python3 action_search_2026_11_05/AC18_constraint_causality/ac18.py            -> ac18.json / ac18.out
    AC18_MUTATE=1 python3 ...                                                     -> ac18_MUTATE.json / .out
"""
import json, os, sys, time
from pathlib import Path
import sympy as sp
import mpmath as mp

MUTATE = os.environ.get("AC18_MUTATE") == "1"
D = Path(__file__).resolve().parent
mp.mp.dps = 50
T0 = time.time()
out = {"mode": "MUTATE_hyperbolic_leaf" if MUTATE else "main",
       "note": "kappa = 1/2 FITTED; not theory closed"}

# ---------------------------------------------------------------- S1: structure of the weak-field system
t, X, Y, Z = sp.symbols("t x y z", real=True)
gam = sp.symbols("gamma", positive=True)
w = sp.Function("W")
P = [sp.Function(f"P{i}")(t, X, Y, Z) for i in (1, 2, 3)]
sig = sp.Function("sigma")(t, X, Y, Z)
phi = sp.Function("phi")(t, X, Y, Z)
co = (X, Y, Z)
grad = lambda f: [sp.diff(f, c) for c in co]
Xi = phi - sp.diff(sig, t) + sum(g ** 2 for g in grad(sig)) / 2
q = sum(sp.diff(P[i], co[i]) for i in range(3))
L = sum(P[i] * sp.diff(Xi, co[i]) for i in range(3)) - gam / 2 * q ** 2 - w(sum(p ** 2 for p in P))


def EL(Lag, f):
    """Euler-Lagrange expression for field f (all derivative orders up to 2)."""
    vars4 = (t, X, Y, Z)
    e = sp.diff(Lag, f)
    for v in vars4:
        e -= sp.diff(sp.diff(Lag, sp.diff(f, v)), v)
    for i, v in enumerate(vars4):
        for v2 in vars4[i:]:
            d2 = sp.diff(f, v, v2)
            if Lag.has(d2):
                e += sp.diff(sp.diff(Lag, d2), v, v2)
    return sp.expand(e)


E_sig = EL(L, sig)
vel = [-g for g in grad(sig)]
cont = sp.diff(q, t) + sum(sp.diff(q * vel[i], co[i]) for i in range(3))
s1a = sp.simplify(E_sig - cont) == 0 or sp.simplify(E_sig + cont) == 0
E_P = [EL(L, p) for p in P]
s1b_noPdot = all(not e.has(sp.Derivative(p, t)) for e in E_P + [E_sig] for p in P)
# the P equation is grad(Xi + gamma q) = W'-force: check E_P_i = d_i(Xi + gamma q) - 2 W' P_i
Wp = sp.Subs(sp.diff(w(sp.Symbol("u")), sp.Symbol("u")), sp.Symbol("u"), sum(p ** 2 for p in P)).doit()
s1b_form = all(sp.simplify(E_P[i] - (sp.diff(Xi + gam * q, co[i]) - 2 * Wp * P[i])) == 0 for i in range(3))
# (c) Euler identity: d_t v + grad|v|^2/2 = -grad phi + grad Xi  (v irrotational)
s1c = all(sp.simplify(sp.diff(vel[i], t) + sp.diff(sum(u ** 2 for u in vel) / 2, co[i])
                      - (-sp.diff(phi, co[i]) + sp.diff(Xi, co[i]))) == 0 for i in range(3))
out["S1"] = {"a_sigma_eq_is_charge_continuity": bool(s1a), "b_no_time_derivative_of_P": bool(s1b_noPdot),
             "b_P_equation_form_grad(Xi+gamma q)=2W'P": bool(s1b_form), "c_Euler_identity": bool(s1c)}
critB = bool(s1a and s1b_noPdot and s1b_form and s1c)
out["criterion_B_label"] = "PASS" if critB else "FAIL"

# ---------------------------------------------------------------- A2: the leaf kernel H
xs, bs = sp.symbols("x_bg b", positive=True)
a_ = 1 / (1 + xs)
b_ = xs / (1 + xs)
kx, ky, kz = sp.symbols("k_x k_y k_z", real=True)
k2 = kx ** 2 + ky ** 2 + kz ** 2
sym = k2 / (a_ * (k2 - b_ * kz ** 2))                         # k^2/(k.Mt^-1.k), e = z
split = sp.simplify(sym - (1 / a_) * (1 + b_ * kz ** 2 / (k2 - b_ * kz ** 2)))
S = sp.sqrt(X ** 2 + Y ** 2 + Z ** 2 / (1 - b_))
Gb = 1 / (4 * sp.pi * sp.sqrt(1 - b_) * S)
H = -xs * sp.diff(Gb, Z, 2)                                   # off-origin kernel (b/a = x)
Lmt = lambda f: a_ * (sp.diff(f, X, 2) + sp.diff(f, Y, 2) + (1 - b_) * sp.diff(f, Z, 2))
LH = sp.simplify(Lmt(H))
lapH = sp.diff(H, X, 2) + sp.diff(H, Y, 2) + sp.diff(H, Z, 2)
lapH_pt = sp.N(lapH.subs({xs: sp.Rational(23, 20), X: sp.Rational(3, 10), Y: sp.Rational(2, 10), Z: sp.Rational(7, 10)}), 30)
out["A2_sympy"] = {"symbol_split_residual": str(split), "L_Mt_H_offorigin": str(LH),
                   "lap_H_at_test_point_x1.15": str(lapH_pt)}

Hf = sp.lambdify((X, Y, Z, xs), H, "mpmath")


def H_radon(xv, xbg):
    """Independent inverse transform of the degree-0 symbol f(k_hat) = 1/(a(1 - b kz^2)) off the origin:
    H(x) = -F''(0)/(8 pi^2 r^3), F(s) = int_0^2pi f(s xhat + sqrt(1-s^2)(cos psi u1 + sin psi u2)) dpsi."""
    xv = [mp.mpf(c) for c in xv]
    r = mp.sqrt(sum(c * c for c in xv))
    xh = [c / r for c in xv]
    tmp = [1, 0, 0] if abs(xh[0]) < 0.9 else [0, 1, 0]
    u1 = [tmp[1] * xh[2] - tmp[2] * xh[1], tmp[2] * xh[0] - tmp[0] * xh[2], tmp[0] * xh[1] - tmp[1] * xh[0]]
    n1 = mp.sqrt(sum(c * c for c in u1)); u1 = [c / n1 for c in u1]
    u2 = [xh[1] * u1[2] - xh[2] * u1[1], xh[2] * u1[0] - xh[0] * u1[2], xh[0] * u1[1] - xh[1] * u1[0]]
    av, bv = 1 / (1 + mp.mpf(xbg)), mp.mpf(xbg) / (1 + mp.mpf(xbg))

    def F(s):
        c = mp.sqrt(1 - s * s)
        return mp.quad(lambda p: 1 / (av * (1 - bv * (s * xh[2] + c * (mp.cos(p) * u1[2] + mp.sin(p) * u2[2])) ** 2)),
                       [0, mp.pi / 2, mp.pi, 3 * mp.pi / 2, 2 * mp.pi])
    return -mp.diff(F, 0, 2) / (8 * mp.pi ** 2 * r ** 3)


mp.mp.dps = 30
a2pts = [((0.3, 0.2, 0.7), 1.15), ((1.0, -0.4, 0.2), 2.6), ((-0.5, 0.8, -0.9), 1.15)]
a2 = []
for xv, xb in a2pts:
    hc, hr = Hf(*[mp.mpf(c) for c in xv], mp.mpf(xb)), H_radon(xv, xb)
    a2.append({"x": xv, "x_bg": xb, "H_closed": mp.nstr(hc, 15), "H_radon": mp.nstr(hr, 15),
               "rel_diff": float(abs(hc - hr) / abs(hc))})
mp.mp.dps = 50
A2_ok = (sp.simplify(split) == 0 and sp.simplify(LH) == 0 and abs(lapH_pt) > 1e-10
         and all(r["rel_diff"] <= 1e-6 for r in a2))
out["A2_numeric"] = a2
out["A2_pass"] = bool(A2_ok)

# ---------------------------------------------------------------- A1 / KA3: retarded source moments
c_, G_, m_, vs, Pi_, tp, tt = sp.symbols("c G m v_s Pi tp tt", positive=True)
es = sp.Matrix(sp.symbols("e1 e2 e3", real=True))
kv = sp.Matrix([kx, ky, kz])
kk = sp.sqrt(k2)
kappa = (kv.T * es)[0]
# phi_hat_b(k,tt) = -4 pi G c^2 int_0^tt sin(c k (tt-tp))/(c k) m (exp(-i kappa v_s tp) - 1) dtp, to O(k^3)
ORDER = 4
sinc_ser = sum((-1) ** n * (c_ ** 2 * k2) ** n * (tt - tp) ** (2 * n + 1) / sp.factorial(2 * n + 1) for n in range(2))
exp_ser = sum((-sp.I * kappa * vs * tp) ** n / sp.factorial(n) for n in range(1, ORDER))
integrand = sp.expand(-4 * sp.pi * G_ * c_ ** 2 * m_ * sinc_ser * exp_ser)
phihat = sp.expand(sp.integrate(integrand, (tp, 0, tt)))
lam = sp.symbols("lam")
phihat_tr = sp.expand(phihat.subs({kx: lam * kx, ky: lam * ky, kz: lam * kz}))
phihat_tr = sum(phihat_tr.coeff(lam, n) for n in range(0, ORDER))  # keep total degree <= 3
moment0 = phihat_tr.subs({kx: 0, ky: 0, kz: 0})
order1 = sp.expand(sum(sp.diff(phihat_tr, kc).subs({kx: 0, ky: 0, kz: 0}) * kc for kc in (kx, ky, kz)))
Dt = sp.integrate((tt - tp) * vs * tp, (tp, 0, tt))
order1_expected = sp.expand(4 * sp.pi * G_ * c_ ** 2 * sp.I * m_ * kappa * Dt)
A1_moments_ok = (sp.simplify(moment0) == 0 and sp.simplify(order1 - order1_expected) == 0)
out["A1"] = {"phihat_k0": str(moment0), "phihat_order1": str(sp.factor(order1)),
             "first_moment_matches_-4piG m c^2 D(t)": bool(A1_moments_ok),
             "support": "delta phi_b = retarded - static, both equal for |x-y| > c t (Huygens, 3D); g = Pi int (t-t') delta phi_b, same ball",
             "pass": bool(A1_moments_ok)}

# KA3: independent quadrature of the exact retarded k-space solution at small k (scaled units)
mp.mp.dps = 40
cS, GS, mS, vS, tS = mp.mpf(1), 1 / (4 * mp.pi), mp.mpf(1), mp.mpf("0.3"), mp.mpf(1)
kvec = [mp.mpf("1e-6") * c for c in (mp.mpf("0.6"), mp.mpf("0.0"), mp.mpf("0.8"))]
esv = [1 / mp.sqrt(3)] * 3
kn = mp.sqrt(sum(c * c for c in kvec)); kap = sum(kvec[i] * esv[i] for i in range(3))
exact = mp.quad(lambda s: -4 * mp.pi * GS * cS ** 2 * mS * mp.sin(cS * kn * (tS - s)) / (cS * kn)
                * (mp.exp(-1j * kap * vS * s) - 1), [0, tS])
subsd = {c_: 1, G_: sp.Rational(1, 1) / (4 * sp.pi), m_: 1, vs: sp.Rational(3, 10), tt: 1,
         kx: sp.Float("6e-7", 40), ky: 0, kz: sp.Float("8e-7", 40),
         es[0]: 1 / sp.sqrt(3), es[1]: 1 / sp.sqrt(3), es[2]: 1 / sp.sqrt(3)}
series_val = complex(sp.N(phihat_tr.subs(subsd), 40))
ka3_rel = float(abs(mp.mpc(series_val) - exact) / abs(exact))
out["KA3"] = {"exact_quad": mp.nstr(exact, 20), "series": str(series_val), "rel_diff": ka3_rel, "pass": ka3_rel <= 1e-10}
mp.mp.dps = 50

# ---------------------------------------------------------------- A3: the outside-cone response
# g_hat(k,t) = Pi int_0^t (t-t') phihat(k,t') dt'  (leading order in G)
ghat = sp.expand(Pi_ * sp.integrate((sp.Symbol("T") - tt) * phihat_tr, (tt, 0, sp.Symbol("T"))))
Tsym = sp.Symbol("T")
# Xi(x,T) outside supp g = K sum_alpha c_alpha (-i d)^alpha H(x); K = 4 pi G
poly = sp.Poly(ghat, kx, ky, kz)
K_ = 4 * sp.pi * G_


def deriv(expr, mono):
    for var, n in zip((X, Y, Z), mono):
        if n:
            expr = sp.diff(expr, var, n)
    return expr


# Monomial coefficients of g_hat (polynomials in T); time integrals done on the coefficients only.
Tp = sp.Symbol("Tp")
COEF = []   # (mono, C_dv(T) = int_0^T c dT', C_dq(T) = -Pi int_0^T (T-T') c dT', C_dip_flag)
for mono, coef in poly.terms():
    if sum(mono) == 0:
        continue
    cdv = sp.integrate(coef.subs(Tsym, Tp), (Tp, 0, Tsym))
    cdq = -Pi_ * sp.integrate((Tsym - Tp) * coef.subs(Tsym, Tp), (Tp, 0, Tsym))
    COEF.append((mono, sp.lambdify((Tsym, Pi_, G_, c_, m_, vs, es[0], es[1], es[2]), cdv, "mpmath"),
                 sp.lambdify((Tsym, Pi_, G_, c_, m_, vs, es[0], es[1], es[2]), cdq, "mpmath"), sum(mono)))
Hnum = sp.lambdify((X, Y, Z, xs), H, "mpmath")


def dH(xo, xb, n):
    """Partial derivative d^n H at xo, n = (nx, ny, nz), mpmath numerical differentiation at 50 digits."""
    r = mp.sqrt(sum(c * c for c in xo))
    u = tuple(c / r for c in xo)              # H homogeneous of degree -3: d^n H(r u) = r^(-3-|n|) d^n H(u)
    if sum(n) == 0:
        return Hnum(*u, xb) / r ** 3
    return mp.diff(lambda a, b, c: Hnum(a, b, c, xb), u, tuple(n)) / r ** (3 + sum(n))


def response(xo, xb, T, Pi_v, Gv, cv, m, vsv, esv):
    """dv(x,T) = K sum c_alpha (-i)^|a| grad d^a H integrated; dq = -Pi K sum (-i)^|a| lap d^a H (double time integral)."""
    K = 4 * mp.pi * Gv
    dv = [mp.mpc(0)] * 3; dvd = [mp.mpc(0)] * 3; dq = mp.mpc(0)
    args = (T, Pi_v, Gv, cv, m, vsv, *esv)
    for mono, fdv, fdq, deg in COEF:
        cv_ = fdv(*args); cq_ = fdq(*args)
        ph = (-1j) ** deg
        for j in range(3):
            nn = list(mono); nn[j] += 1
            val = K * cv_ * ph * dH(xo, xb, nn)
            dv[j] += val
            if deg == 1:
                dvd[j] += val
        for j in range(3):
            nn = list(mono); nn[j] += 2
            dq += K * cq_ * ph * dH(xo, xb, nn)
    return dv, dvd, dq


Msun, pc = mp.mpf("1.98847e30"), mp.mpf("3.0856775814913673e16")
cv, Gv = mp.mpf(299792458), mp.mpf("6.67430e-11")
FOOT = {"canonical": {"a0": "9.3603e-11", "rho0": "0.0447", "x": "1.15", "Lstar_pc": "21.68", "gamma_s2": "2.4e-17"},
        "alt": {"a0": "1.1312e-10", "rho0": "0.0514", "x": "2.6", "Lstar_pc": "22.85", "gamma_s2": "4.0e-17"}}
e_s = [1 / mp.sqrt(3)] * 3                       # source displacement direction (generic, not along e)
dirs = {"+e": (0, 0, 1), "-e": (0, 0, -1), "perp_x": (1, 0, 0), "perp_y": (0, 1, 0),
        "45_xz": (1 / mp.sqrt(2), 0, 1 / mp.sqrt(2)), "45_y-z": (0, 1 / mp.sqrt(2), -1 / mp.sqrt(2))}
grid = [(1, 1e9), (1, 1e10), (10, 1e10), (10, 1e9)]   # (t s, r m); (10, 1e9) is inside the cone: excluded
vrel = mp.mpf(220e3)
gam_rel = 1 / mp.sqrt(1 - (vrel / cv) ** 2)
eps = mp.mpf(2) ** -52

A3 = {}
for fname, F in FOOT.items():
    Pi_v = mp.mpf(F["rho0"]) * Msun / pc ** 3
    xb = mp.mpf(F["x"])
    rows = []
    for tsec, rm in grid:
        tsec, rm = mp.mpf(tsec), mp.mpf(rm)
        inside = cv * tsec >= rm
        for dn, dvec in dirs.items():
            xo = [rm * mp.mpf(c) for c in dvec]
            row = {"t_s": float(tsec), "r_m": float(rm), "dir": dn, "ct_over_r": float(cv * tsec / rm)}
            if inside:
                row["excluded"] = "inside the light cone (frozen-grid slip: r < c t)"
                rows.append(row); continue
            if MUTATE:
                # hyperbolic leaf: retarded Green function of a(d_perp^2 + (1-b) d_z^2) - c^-2 d_t^2;
                # speeds c sqrt(a), c sqrt(a(1-b)) <= c. Earliest arrival from the source ball |x'| <= c t':
                cmax = cv / mp.sqrt(1 + xb)
                t_arr = min(tq + (rm - cv * tq) / cmax for tq in [tsec * j / 200 for j in range(201)])
                zero = tsec < t_arr
                row.update({"mutant_earliest_arrival_s": float(t_arr), "dv": [0.0, 0.0, 0.0] if zero else None,
                            "dq": 0.0 if zero else None, "dO": 0.0 if zero else None, "nonzero": not zero})
                rows.append(row); continue
            dv, dvd, dq = response(xo, xb, tsec, Pi_v, Gv, cv, mp.mpf(1000), mp.mpf(1), e_s)
            dv = [mp.re(c) for c in dv]; dvd = [mp.re(c) for c in dvd]; dq = mp.re(dq)
            vdotdv = vrel * sum(e_s[i] * dv[i] for i in range(3))
            dO = 8 * mp.pi * Gv / cv ** 2 * (dq * (gam_rel ** 2 - mp.mpf(1) / 2) + Pi_v * 2 * gam_rel ** 4 * vdotdv / cv ** 2)
            O_bg = 8 * mp.pi * Gv / cv ** 2 * Pi_v * (gam_rel ** 2 - mp.mpf(1) / 2)
            ndv = mp.sqrt(sum(c * c for c in dv)); ndvd = mp.sqrt(sum(c * c for c in dvd))
            corr = mp.sqrt(sum((dv[i] - dvd[i]) ** 2 for i in range(3))) / ndvd if ndvd else mp.inf
            # floor: double-precision floor of the evaluated expression, scale = |dipole term|
            floor = eps * ndvd
            row.update({"dv_m_s": [mp.nstr(c, 6) for c in dv], "abs_dv_m_s": float(ndv),
                        "dipole_only_abs_dv": float(ndvd), "higher_moment_rel_correction": float(corr),
                        "dq_kg_m3": mp.nstr(dq, 6), "dO_per_m2": mp.nstr(dO, 6), "dO_over_O_bg": mp.nstr(dO / O_bg, 6),
                        "abs_dv_over_floor": float(ndv / floor) if floor else None,
                        "nonzero": bool(ndv > 1e6 * floor and abs(dO) > 0)})
            rows.append(row)
    # AC2q regulator bound
    Ls = mp.mpf(F["Lstar_pc"]) * pc
    rmax = mp.mpf(1e10)
    reg = mp.mpf(F["gamma_s2"]) * 2 * rmax ** 2 / Ls ** 2 * (1 + xb)
    A3[fname] = {"Pi_kg_m3": mp.nstr(Pi_v, 6), "x_bg": float(xb), "rows": rows,
                 "AC2q_regulator_rel_bound_at_1e10m": float(reg), "AC2q_carries": bool(reg < 1e-6)}
out["A3"] = A3

# KA1 / KA2
ka1 = sp.simplify(H.subs(xs, 0)) == 0
ka2 = sp.simplify(ghat.subs(Pi_, 0)) == 0
out["KA1_isotropic_H_offorigin_zero"] = bool(ka1)
out["KA2_zero_charge_g_zero"] = bool(ka2)

# ---------------------------------------------------------------- labels
graded = [r for F in A3.values() for r in F["rows"] if "excluded" not in r]
any_nonzero_both = all(any(r["nonzero"] for r in F["rows"] if "excluded" not in r) for F in A3.values())
none_nonzero = not any(r["nonzero"] for r in graded)
if any_nonzero_both:
    critA = "FAIL"
elif none_nonzero:
    critA = "PASS-AT-THIS-ORDER"
else:
    critA = "SPLIT (one footing only)"
checks_ok = bool(A2_ok and A1_moments_ok and out["KA3"]["pass"] and ka1 and ka2 and critB)
out["criterion_A_label"] = critA
out["AC2q_label_carries"] = all(F["AC2q_carries"] for F in A3.values())
out["known_answers_and_checks_ok"] = checks_ok
out["runtime_s"] = round(time.time() - T0, 1)

suffix = "_MUTATE" if MUTATE else ""
(D / f"ac18{suffix}.json").write_text(json.dumps(out, indent=1, default=str) + "\n")
lines = [f"AC18 {out['mode']}", f"criterion B (tau-ordering): {out['criterion_B_label']}  S1={out['S1']}",
         f"A2 kernel: {A2_ok}  {[(r['x'], r['rel_diff']) for r in a2]}",
         f"A1 moments: {A1_moments_ok}   KA3 rel {ka3_rel:.2e}   KA1 {ka1}  KA2 {ka2}"]
for fname, F in A3.items():
    lines.append(f"{fname}: Pi {F['Pi_kg_m3']} kg/m3, x {F['x_bg']}, AC2q regulator bound {F['AC2q_regulator_rel_bound_at_1e10m']:.2e}")
    for r in F["rows"]:
        if "excluded" in r:
            lines.append(f"  t {r['t_s']:g} r {r['r_m']:.0e} {r['dir']:7s} EXCLUDED ({r['excluded']})"); continue
        if MUTATE:
            lines.append(f"  t {r['t_s']:g} r {r['r_m']:.0e} {r['dir']:7s} mutant arrival {r['mutant_earliest_arrival_s']:.3g} s nonzero {r['nonzero']}")
        else:
            lines.append(f"  t {r['t_s']:g} r {r['r_m']:.0e} {r['dir']:7s} ct/r {r['ct_over_r']:.2f} |dv| {r['abs_dv_m_s']:.3e} m/s "
                         f"(dipole {r['dipole_only_abs_dv']:.3e}, higher {r['higher_moment_rel_correction']:.1e}) dq {r['dq_kg_m3']} "
                         f"dO/O {r['dO_over_O_bg']} floor-ratio {r['abs_dv_over_floor']:.1e} nonzero {r['nonzero']}")
lines.append(f"criterion A: {critA}; AC2q carries: {out['AC2q_label_carries']}; checks ok: {checks_ok}; runtime {out['runtime_s']} s")
(D / f"ac18{suffix}.out").write_text("\n".join(lines) + "\n")
print("\n".join(lines))
sys.exit(0 if (checks_ok and (critA == "FAIL") != MUTATE) else 1)
