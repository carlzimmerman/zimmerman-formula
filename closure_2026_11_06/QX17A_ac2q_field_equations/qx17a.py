"""QX17A: full covariant field equations of the AC2q candidate, checked against a direct Euler-Lagrange variation.
Criteria: FROZEN_CRITERIA.md (1b39bcb871, renamed 100b4d4924).  c = 1, K = 4 pi G.  Built from qx17.py.

  L/sqrt(-g) = R/(4K) + Q^2/2 - V(tau) + P^m A_m - W(K|P|) - gam [F(Pi + Q^2) - Q^4/2] + lam n^m P_m   (tau = phi)

The GR part (R, Lam) is standard and not re-checked here; K1-K3 check every non-GR term.
Method: sympy builds the Lagrangian density on jet symbols (g_ab, d_c g_ab, d tau, dd tau, P_a, d_b P_a, lam);
partial derivatives in the jet symbols are lambdified to mpmath and total derivatives are taken numerically
(mpmath.diff, 40 digits) on random polynomial fields in 2+1 dimensions with n.P = 0 imposed by P = h.V, Pi > 0 branch.
QX17_MUTATE=1 flips two pieces of the closed forms (they must then fail).
"""
import os, sys, json, random, time
import sympy as sp
import mpmath as mp

MUT = os.environ.get("QX17A_MUTATE") == "1"
mp.mp.dps = 40
t0 = time.time()
out = {"mutate": MUT, "checks": {}}
D = 3
X = sp.symbols("t x y")

# ---------------- K0: Legendre ----------------
a0, K, p, Am = sp.symbols("a0 K p A", positive=True)
W = (a0**2 / K) * (-p / a0 - sp.log(1 - p / a0))          # W(p), p = K|P|
Wp = sp.diff(W, p)
pstar = a0 * (Am / a0) / (1 + Am / a0)                      # claimed stationary K|P|
stat = sp.simplify((Am - K * Wp.subs(p, pstar)))             # d/d|P| [ |P| A - W(K|P|) ] = A - K W'
u = Am / a0
val = sp.simplify((pstar / K) * Am - W.subs(p, pstar) - (a0**2 / K) * (u - sp.log(1 + u)))
k0 = (stat == 0) and (sp.simplify(sp.expand_log(val, force=True)) == 0)
out["checks"]["K0_legendre"] = {"stationarity_residual": str(stat), "value_residual": str(val), "pass": bool(k0)}

# ---------------- jet symbols ----------------
G = sp.Matrix(D, D, lambda a, b: sp.Symbol(f"g{min(a,b)}{max(a,b)}"))
dG = [[[sp.Symbol(f"g{min(a,b)}{max(a,b)}_{c}") for c in range(D)] for b in range(D)] for a in range(D)]
dT = [sp.Symbol(f"T_{a}") for a in range(D)]
ddT = [[sp.Symbol(f"T_{min(a,b)}{max(a,b)}") for b in range(D)] for a in range(D)]
Pl = [sp.Symbol(f"P{a}") for a in range(D)]
dP = [[sp.Symbol(f"P{a}_{b}") for b in range(D)] for a in range(D)]          # d_b P_a
lam = sp.Symbol("lam")
tau0 = sp.Symbol("tau0")
v1, v2 = sp.Rational(2, 5), sp.Rational(-3, 7)
Vf = lambda q: v1 * q + v2 * q**2
Vfp = lambda q: v1 + 2 * v2 * q
mu, gam, w2, w3 = sp.Rational(7, 10), sp.Rational(3, 5), sp.Rational(1, 3), sp.Rational(1, 7)
Kv = sp.Rational(1, 2)

detg = G.det()
Gi = G.adjugate() / detg
sqrtg = sp.sqrt(-detg)
dGc = [sp.Matrix(D, D, lambda a, b: dG[a][b][c]) for c in range(D)]
dGi = [-Gi * dGc[c] * Gi for c in range(D)]
Q2 = -sum(Gi[a, b] * dT[a] * dT[b] for a in range(D) for b in range(D))
Q = sp.sqrt(Q2)
dQ2 = [-sum(dGi[c][a, b] * dT[a] * dT[b] for a in range(D) for b in range(D))
       - 2 * sum(Gi[a, b] * ddT[a][c] * dT[b] for a in range(D) for b in range(D)) for c in range(D)]
dl = [dQ2[c] / (2 * Q2) for c in range(D)]                       # d_c ln Q
n = [-dT[a] / Q for a in range(D)]
Pu = [sum(Gi[a, b] * Pl[b] for b in range(D)) for a in range(D)]
dlnsg = [sum(Gi[a, b] * dGc[c][a, b] for a in range(D) for b in range(D)) / 2 for c in range(D)]
divP = sum(dGi[a][a, b] * Pl[b] + Gi[a, b] * dP[b][a] + Gi[a, b] * Pl[b] * dlnsg[a] for a in range(D) for b in range(D))
Pdl = sum(Pu[a] * dl[a] for a in range(D))
Pi = divP + Pdl
Pmod = sp.sqrt(sum(Pu[a] * Pl[a] for a in range(D)))
Wf = lambda q: w2 * q**2 + w3 * q**3
Wfp = lambda q: 2 * w2 * q + 3 * w3 * q**2
LK = mu**2 * (Q - 1)**2 / (2 * Kv)
nP = sum(Gi[a, b] * n[a] * Pl[b] for a in range(D) for b in range(D))
Sig = Pi + Q2
Ldens = sqrtg * (Q2 / 2 - Vf(tau0) - Wf(Kv * Pmod) - Pdl - gam * (Sig**2 / 2 - Q2**2 / 2) + lam * nP)

# field list: (name, symbol, first-derivative symbols, second-derivative symbols {(c,d): sym} c<=d)
fields = []
for a in range(D):
    for b in range(a, D):
        fields.append((f"g{a}{b}", G[a, b], [dG[a][b][c] for c in range(D)], {}))
fields.append(("tau", tau0, dT, {(c, d): ddT[c][d] for c in range(D) for d in range(c, D)}))
for a in range(D):
    fields.append((f"P{a}", Pl[a], [dP[a][c] for c in range(D)], {}))
fields.append(("lam", lam, [], {}))

jet_syms = sorted(Ldens.free_symbols, key=lambda s: s.name)
lamb = lambda e: sp.lambdify(jet_syms, e, "mpmath")
partials = {}
for name, s0, s1, s2 in fields:
    partials[name] = (lamb(sp.diff(Ldens, s0)) if s0 is not None else None,
                      [lamb(sp.diff(Ldens, s)) for s in s1],
                      {cd: lamb(sp.diff(Ldens, s)) for cd, s in s2.items()})
print(f"jet partials built in {time.time()-t0:.1f}s", flush=True)

# ---------------- random configurations ----------------
def rpoly(rng, scale):
    t, x, y = X
    mons = [1, t, x, y, t*x, x*y, t*y, x**2, y**2, t**2]
    return sum(sp.Rational(rng.randint(-9, 9), 10) * scale * m for m in mons)

def make_config(seed):

    rng = random.Random(seed)
    eta = sp.diag(-1, 1, 1)
    g = sp.Matrix(D, D, lambda a, b: 0)
    for a in range(D):
        for b in range(a, D):
            e = eta[a, b] + rpoly(rng, sp.Rational(1, 10))
            g[a, b] = g[b, a] = e
    tau = X[0] + rpoly(rng, sp.Rational(1, 10))
    V = [rpoly(rng, 1) + (sp.Integer(2) if a == 1 else 0) for a in range(D)]
    lamf = rpoly(rng, 1)
    gi = g.inv()
    dt = [sp.diff(tau, X[c]) for c in range(D)]
    Qf = sp.sqrt(-sum(gi[a, b] * dt[a] * dt[b] for a in range(D) for b in range(D)))
    nf = [-dt[a] / Qf for a in range(D)]
    nu = [sum(gi[a, b] * nf[b] for b in range(D)) for a in range(D)]
    nV = sum(nu[a] * V[a] for a in range(D))
    Pf = [V[a] + nf[a] * nV for a in range(D)]                       # h_a^b V_b
    return g, tau, Pf, lamf

def num_funcs(g, tau, Pf, lamf):
    """lambdified field values and their needed derivatives as functions of a point."""
    f = {}
    for a in range(D):
        for b in range(a, D):
            f[f"g{a}{b}"] = sp.lambdify(X, g[a, b], "mpmath")
            for c in range(D):
                f[f"g{a}{b}_{c}"] = sp.lambdify(X, sp.diff(g[a, b], X[c]), "mpmath")
    for a in range(D):
        f[f"T_{a}"] = sp.lambdify(X, sp.diff(tau, X[a]), "mpmath")
        for b in range(a, D):
            f[f"T_{a}{b}"] = sp.lambdify(X, sp.diff(tau, X[a], X[b]), "mpmath")
        f[f"P{a}"] = sp.lambdify(X, Pf[a], "mpmath")
        for b in range(D):
            f[f"P{a}_{b}"] = sp.lambdify(X, sp.diff(Pf[a], X[b]), "mpmath")
    f["lam"] = sp.lambdify(X, lamf, "mpmath")
    f["tau0"] = sp.lambdify(X, tau, "mpmath")
    return f

def jet_at(f, pt):
    return [f[s.name](*pt) for s in jet_syms]

def EL(name, f, pt):
    s0, s1, s2 = partials[name]
    e = s0(*jet_at(f, pt)) if s0 is not None else mp.mpf(0)
    for c, fn in enumerate(s1):
        h = lambda *q: fn(*jet_at(f, q))
        e -= mp.diff(h, pt, tuple(1 if k == c else 0 for k in range(D)))
    for (c, d), fn in s2.items():
        h = lambda *q: fn(*jet_at(f, q))
        order = [0] * D; order[c] += 1; order[d] += 1
        e += mp.diff(h, pt, tuple(order))
    return e

# ---------------- closed forms (RESULT.md) ----------------
sgn_D = 0 if MUT else 1       # MUTATE drops the -2 gam Q^2 Sigma nn term of the metric equation
sgn_lt = 0 if MUT else 1      # MUTATE drops the -2 gam (Sigma - Q^2) piece of the phi current

def geom(f, pt):
    """pointwise geometric quantities from the field functions."""
    g = mp.matrix(D, D)
    for a in range(D):
        for b in range(D):
            g[a, b] = f[f"g{min(a,b)}{max(a,b)}"](*pt)
    gi = g ** -1
    sg = mp.sqrt(-mp.det(g))
    dt = [f[f"T_{a}"](*pt) for a in range(D)]
    Qv = mp.sqrt(-sum(gi[a, b] * dt[a] * dt[b] for a in range(D) for b in range(D)))
    nl = [-dt[a] / Qv for a in range(D)]
    Pl_ = [f[f"P{a}"](*pt) for a in range(D)]
    return g, gi, sg, Qv, nl, Pl_

def Pi_at(f, pt):
    return pi_fn(*jet_at(f, pt))
def Sig_at(f, pt):
    return sig_fn(*jet_at(f, pt))
pi_fn = lamb(Pi); sig_fn = lamb(Sig); q2_fn = lamb(Q2); dl_fn = [lamb(dl[c]) for c in range(D)]; divP_fn = lamb(divP)

def closed_P(f, pt):
    g, gi, sg, Qv, nl, Pl_ = geom(f, pt)
    jt = jet_at(f, pt)
    dlv = [dl_fn[c](*jt) for c in range(D)]
    Piv = sig_fn(*jt)
    dPi = [mp.diff(lambda *q: Sig_at(f, q), pt, tuple(1 if k == c else 0 for k in range(D))) for c in range(D)]
    Pu_ = [sum(gi[a, b] * Pl_[b] for b in range(D)) for a in range(D)]
    nu = [sum(gi[a, b] * nl[b] for b in range(D)) for a in range(D)]
    Pm = mp.sqrt(sum(Pu_[a] * Pl_[a] for a in range(D)))
    lv = f["lam"](*pt)
    res = []
    for a in range(D):
        e = (-sum(gi[a, c] * dlv[c] for c in range(D))
             - Kv * Wfp(Kv * Pm) * Pu_[a] / Pm
             + gam * sum(gi[a, c] * (dPi[c] - Piv * dlv[c]) for c in range(D))
             + lv * nu[a])
        res.append(sg * e)
    return res

def closed_tau(f, pt):
    # E_tau = -d_nu( sqrt(-g) n^nu fK ) + sgn * d_nu( sqrt(-g) lam P^nu / Q ),  fK = J_P/Q + mu^2 (Q-1)/K,
    # J_P = (1/sqrt(-g)) d_nu( sqrt(-g) (1 + gam Pi) P^nu )
    def dens_JP(c):
        def h(*q):
            g, gi, sg, Qv, nl, Pl_ = geom(f, q)
            Pu_ = sum(gi[c, b] * Pl_[b] for b in range(D))
            return sg * (1 + gam * Sig_at(f, q)) * Pu_
        return h
    def JP(q):
        g, gi, sg, Qv, nl, Pl_ = geom(f, q)
        return sum(mp.diff(dens_JP(c), q, tuple(1 if k == c else 0 for k in range(D))) for c in range(D)) / sg
    def flux(c):
        def h(*q):
            g, gi, sg, Qv, nl, Pl_ = geom(f, q)
            nu = sum(gi[c, b] * nl[b] for b in range(D))
            Pu_ = sum(gi[c, b] * Pl_[b] for b in range(D))
            fK = JP(q) / Qv + Qv * (1 - sgn_lt * 2 * gam * (Sig_at(f, q) - Qv**2))
            return -sg * nu * fK + sg * f["lam"](*q) * Pu_ / Qv
        return h
    g, gi, sg, Qv, nl, Pl_ = geom(f, pt)
    return sum(mp.diff(flux(c), pt, tuple(1 if k == c else 0 for k in range(D))) for c in range(D)) - sg * Vfp(f["tau0"](*pt))

def closed_T(f, pt):
    """T_ab (lower) of the non-GR sector; returns T^{ab} (upper)."""
    g, gi, sg, Qv, nl, Pl_ = geom(f, pt)
    jt = jet_at(f, pt)
    dlv = [dl_fn[c](*jt) for c in range(D)]
    Piv = pi_fn(*jt); divPv = divP_fn(*jt); Sv = sig_fn(*jt)
    dPi = [mp.diff(lambda *q: Sig_at(f, q), pt, tuple(1 if k == c else 0 for k in range(D))) for c in range(D)]
    Pu_ = [sum(gi[a, b] * Pl_[b] for b in range(D)) for a in range(D)]
    Pm = mp.sqrt(sum(Pu_[a] * Pl_[a] for a in range(D)))
    lv = f["lam"](*pt)
    Fv = Sv**2 / 2
    Dv = [dPi[c] - Sv * dlv[c] for c in range(D)]
    PD = sum(Pu_[c] * Dv[c] for c in range(D))
    Pdlv = sum(Pu_[c] * dlv[c] for c in range(D))
    T = mp.matrix(D, D)
    for a in range(D):
        for b in range(D):
            h_ab = g[a, b] + nl[a] * nl[b]
            TK = Qv**2 * nl[a] * nl[b] + g[a, b] * (Qv**2 / 2 - Vf(f["tau0"](*pt)))
            TW = -g[a, b] * Wf(Kv * Pm) + Kv * Wfp(Kv * Pm) * Pl_[a] * Pl_[b] / Pm
            TA = (-g[a, b] * Pdlv + Pl_[a] * dlv[b] + Pl_[b] * dlv[a] + divPv * nl[a] * nl[b]
                  + gam * (-g[a, b] * Fv + Piv * Sv * h_ab + h_ab * PD - Pl_[a] * Dv[b] - Pl_[b] * Dv[a]
                           - sgn_D * 2 * Qv**2 * Sv * nl[a] * nl[b] + g[a, b] * Qv**4 / 2 + 2 * Qv**4 * nl[a] * nl[b])
                  - lv * (nl[a] * Pl_[b] + nl[b] * Pl_[a]))
            T[a, b] = TK + TW + TA
    return gi * T * gi, sg, nl, Piv, Sv, T

def rel(a, b):
    return float(abs(a - b) / max(abs(a), abs(b), mp.mpf("1e-30")))

TOL = 1e-10
k1 = k2 = k3 = k5 = True
rows = []
for seed in (11, 22, 33):
    g, tau, Pf, lamf = make_config(seed)
    f = num_funcs(g, tau, Pf, lamf)
    rng = random.Random(seed + 1000)
    pt = tuple(mp.mpf(rng.randint(-20, 20)) / 100 for _ in range(D))
    Piv = Pi_at(f, pt)
    if Piv <= 0:          # stay on the Pi > 0 branch: flip V's sign flips Pi
        Pf = [-e for e in Pf]; f = num_funcs(g, tau, Pf, lamf); Piv = Pi_at(f, pt)
    r = {"seed": seed, "point": [float(v) for v in pt], "Pi": float(Piv)}
    # K1 P equation
    cp = closed_P(f, pt)
    r["K1"] = [rel(EL(f"P{a}", f, pt), cp[a]) for a in range(D)]
    # K2 tau equation
    r["K2"] = rel(EL("tau", f, pt), closed_tau(f, pt))
    # K3 metric equation: T^{ab} = (2/sqrt(-g)) dS/dg_ab, off-diagonal symbol counts twice
    Tup, sg, nl, Piv2, Sv, Tlow = closed_T(f, pt)
    k3r = []
    for a in range(D):
        for b in range(a, D):
            E = EL(f"g{a}{b}", f, pt)
            dS = E if a == b else E / 2
            k3r.append(rel(2 * dS / sg, Tup[a, b]))
    r["K3"] = k3r
    # K5: n^a n^b T_ab of the P sector (W term has no nn part since n.P = 0) = Pi + gam F
    g_, gi, sg_, Qv, nl_, Pl_ = geom(f, pt)
    nu = [sum(gi[a, b] * nl_[b] for b in range(D)) for a in range(D)]
    rhoK = Qv**2 / 2 + Vf(f["tau0"](*pt))
    Wv = Wf(Kv * mp.sqrt(sum(sum(gi[a, b] * Pl_[b] for b in range(D)) * Pl_[a] for a in range(D))))
    rho_tot = sum(nu[a] * nu[b] * Tlow[a, b] for a in range(D) for b in range(D))
    r["K5"] = rel(rho_tot - rhoK - Wv, Piv * (1 - gam * Qv**2) + gam * Piv**2 / 2)
    rows.append(r)
    k1 &= max(r["K1"]) <= TOL; k2 &= r["K2"] <= TOL; k3 &= max(r["K3"]) <= TOL; k5 &= r["K5"] <= TOL
    print(json.dumps(r), flush=True)

out["checks"]["K1_P_equation"] = {"pass": bool(k1), "max_rel": max(max(r["K1"]) for r in rows)}
out["checks"]["K2_tau_equation"] = {"pass": bool(k2), "max_rel": max(r["K2"] for r in rows)}
out["checks"]["K3_metric_equation"] = {"pass": bool(k3), "max_rel": max(max(r["K3"]) for r in rows)}
out["checks"]["K5_static_source"] = {"pass": bool(k5), "max_rel": max(r["K5"] for r in rows),
                                     "note": "rho of P + stiffness sector = Pi (1 - gam Q^2) + gam Pi^2/2"}

# ---------------- K4: FRW from the closed forms (P = 0, so Pi = 0, Sigma = Q^2) ----------------
Qs, gs = sp.symbols("Q gamma", positive=True)
Sg = Qs**2
# coefficients of g_ab and n_a n_b in the stiffness part of T^P at P = 0 (h_ab = g_ab + n n; Pi = 0 kills Pi*Sigma*h)
coef_g = -Sg**2 / 2 + Qs**4 / 2
coef_nn = -2 * Qs**2 * Sg + 2 * Qs**4
rhoQ = Qs * (1 - 2 * gs * (Sg - Qs**2))          # phi current density along n at P = 0
k4 = sp.simplify(coef_g) == 0 and sp.simplify(coef_nn) == 0 and sp.simplify(rhoQ - Qs) == 0
# rho_Q = Q  =>  nabla(n Q) = -box phi (n Q = -grad phi)  =>  phi equation: box phi = V'(phi)
out["checks"]["K4_FRW"] = {"pass": bool(k4), "stiffness_T_coeffs": [str(coef_g), str(coef_nn)],
                           "phi_current": str(sp.simplify(rhoQ)), "phi_eq": "box phi = V'(phi)"}

allpass = all(v["pass"] for v in out["checks"].values())
out["label"] = "CERTIFIED" if allpass else "FAIL"
out["rows"] = rows
out["seconds"] = round(time.time() - t0, 1)
suffix = "_MUTATE" if MUT else ""
with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), f"qx17a{suffix}.json"), "w") as fh:
    json.dump(out, fh, indent=1)
for k, v in out["checks"].items():
    print(k, "PASS" if v["pass"] else "FAIL", v.get("max_rel", ""))
print("LABEL", out["label"], f"{out['seconds']}s")
sys.exit(0 if (allpass or MUT) else 1)
