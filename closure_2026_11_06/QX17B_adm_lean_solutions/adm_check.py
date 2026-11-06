"""QX17B B1-N: ADM projections (rho, J_i, S_ij) of QX17's covariant stress tensor on random 3+1 configurations.
Criteria 9684f63ba8. Built from qx17.py (definitions, config generator, closed forms), D = 4, no jet variation."""
import os, sys, json, random, time
import sympy as sp
import mpmath as mp

MUT = False
mp.mp.dps = 40
t0 = time.time()
out = {"mutate": MUT, "checks": {}}
D = 4
X = sp.symbols("t x y z")

# ---------------- jet symbols ----------------
G = sp.Matrix(D, D, lambda a, b: sp.Symbol(f"g{min(a,b)}{max(a,b)}"))
dG = [[[sp.Symbol(f"g{min(a,b)}{max(a,b)}_{c}") for c in range(D)] for b in range(D)] for a in range(D)]
dT = [sp.Symbol(f"T_{a}") for a in range(D)]
ddT = [[sp.Symbol(f"T_{min(a,b)}{max(a,b)}") for b in range(D)] for a in range(D)]
Pl = [sp.Symbol(f"P{a}") for a in range(D)]
dP = [[sp.Symbol(f"P{a}_{b}") for b in range(D)] for a in range(D)]          # d_b P_a
lam = sp.Symbol("lam")
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
Ldens = sqrtg * (LK - Wf(Kv * Pmod) - Pdl - gam * Pi**2 / 2 + lam * nP)

# ---------------- random configurations ----------------
def rpoly(rng, scale):
    t, x, y, z = X
    mons = [1, t, x, y, z, t*x, x*y, y*z, t*z, x**2, z**2]
    return sum(sp.Rational(rng.randint(-9, 9), 10) * scale * m for m in mons)

def make_config(seed):
    rng = random.Random(seed)
    eta = sp.diag(-1, 1, 1, 1)
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
    return f

def jet_at(f, pt):
    return [f[s.name](*pt) for s in jet_syms]

jet_syms = sorted(set().union(*[e.free_symbols for e in [Pi, divP] + dl]), key=lambda s: s.name)
lamb = lambda e: sp.lambdify(jet_syms, e, "mpmath")
# ---------------- closed forms (RESULT.md) ----------------
sgn_D = -1 if MUT else 1      # MUTATE flips the Pi d lnQ piece of the metric equation
sgn_lt = -1 if MUT else 1     # MUTATE flips the lambda flux in the tau equation

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
pi_fn = lamb(Pi); dl_fn = [lamb(dl[c]) for c in range(D)]; divP_fn = lamb(divP)

def closed_P(f, pt):
    g, gi, sg, Qv, nl, Pl_ = geom(f, pt)
    jt = jet_at(f, pt)
    dlv = [dl_fn[c](*jt) for c in range(D)]
    Piv = pi_fn(*jt)
    dPi = [mp.diff(lambda *q: Pi_at(f, q), pt, tuple(1 if k == c else 0 for k in range(D))) for c in range(D)]
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
            return sg * (1 + gam * Pi_at(f, q)) * Pu_
        return h
    def JP(q):
        g, gi, sg, Qv, nl, Pl_ = geom(f, q)
        return sum(mp.diff(dens_JP(c), q, tuple(1 if k == c else 0 for k in range(D))) for c in range(D)) / sg
    def flux(c):
        def h(*q):
            g, gi, sg, Qv, nl, Pl_ = geom(f, q)
            nu = sum(gi[c, b] * nl[b] for b in range(D))
            Pu_ = sum(gi[c, b] * Pl_[b] for b in range(D))
            fK = JP(q) / Qv + mu**2 * (Qv - 1) / Kv
            return -sg * nu * fK + sgn_lt * sg * f["lam"](*q) * Pu_ / Qv
        return h
    return sum(mp.diff(flux(c), pt, tuple(1 if k == c else 0 for k in range(D))) for c in range(D))

def closed_T(f, pt):
    """T_ab (lower) of the non-GR sector; returns T^{ab} (upper)."""
    g, gi, sg, Qv, nl, Pl_ = geom(f, pt)
    jt = jet_at(f, pt)
    dlv = [dl_fn[c](*jt) for c in range(D)]
    Piv = pi_fn(*jt); divPv = divP_fn(*jt)
    dPi = [mp.diff(lambda *q: Pi_at(f, q), pt, tuple(1 if k == c else 0 for k in range(D))) for c in range(D)]
    Pu_ = [sum(gi[a, b] * Pl_[b] for b in range(D)) for a in range(D)]
    Pm = mp.sqrt(sum(Pu_[a] * Pl_[a] for a in range(D)))
    lv = f["lam"](*pt)
    Fv = Piv**2 / 2
    Dv = [dPi[c] - sgn_D * Piv * dlv[c] for c in range(D)]
    PD = sum(Pu_[c] * Dv[c] for c in range(D))
    Pdlv = sum(Pu_[c] * dlv[c] for c in range(D))
    LKv = mu**2 * (Qv - 1)**2 / (2 * Kv)
    T = mp.matrix(D, D)
    for a in range(D):
        for b in range(D):
            h_ab = g[a, b] + nl[a] * nl[b]
            TK = g[a, b] * LKv + (mu**2 / Kv) * Qv * (Qv - 1) * nl[a] * nl[b]
            TW = -g[a, b] * Wf(Kv * Pm) + Kv * Wfp(Kv * Pm) * Pl_[a] * Pl_[b] / Pm
            TA = (-g[a, b] * Pdlv + Pl_[a] * dlv[b] + Pl_[b] * dlv[a] + divPv * nl[a] * nl[b]
                  + gam * (-g[a, b] * Fv + 2 * Fv * h_ab + h_ab * PD - Pl_[a] * Dv[b] - Pl_[b] * Dv[a])
                  - lv * (nl[a] * Pl_[b] + nl[b] * Pl_[a]))
            T[a, b] = TK + TW + TA
    return gi * T * gi, sg, nl, Piv, Fv, T



def rel(a, b):
    return float(abs(a - b) / max(abs(a), abs(b), mp.mpf("1e-30")))

out = {"rows": []}
for seed in (11, 22, 33):
    g, tau, Pf, lamf = make_config(seed)
    f = num_funcs(g, tau, Pf, lamf)
    rng = random.Random(seed + 1000)
    pt = tuple(mp.mpf(rng.randint(-20, 20)) / 100 for _ in range(D))
    if Pi_at(f, pt) <= 0:
        Pf = [-e for e in Pf]; f = num_funcs(g, tau, Pf, lamf)
    Tup, sg, nl, Piv, Fv, T = closed_T(f, pt)
    g_, gi, sg_, Qv, nl_, Pl_ = geom(f, pt)
    jt = jet_at(f, pt)
    dlv = [dl_fn[c](*jt) for c in range(D)]
    dPi = [mp.diff(lambda *q: Pi_at(f, q), pt, tuple(1 if k == c else 0 for k in range(D))) for c in range(D)]
    nu = [sum(gi[a, b] * nl_[b] for b in range(D)) for a in range(D)]
    h = mp.matrix(D, D)
    for a in range(D):
        for b in range(D):
            h[a, b] = (1 if a == b else 0) + nu[a] * nl_[b]          # h^a_b
    hl = [[g_[a, b] + nl_[a] * nl_[b] for b in range(D)] for a in range(D)]
    Pu_ = [sum(gi[a, b] * Pl_[b] for b in range(D)) for a in range(D)]
    Pm = mp.sqrt(sum(Pu_[a] * Pl_[a] for a in range(D)))
    A = [-sum(h[c, a] * dlv[c] for c in range(D)) for a in range(D)]      # A_a = -h_a^c d_c l
    PA = sum(Pu_[a] * A[a] for a in range(D))
    DPi = [sum(h[c, a] * dPi[c] for c in range(D)) for a in range(D)]
    E = [DPi[a] + Piv * A[a] for a in range(D)]
    PE = sum(Pu_[a] * E[a] for a in range(D))
    LK = mu**2 * (Qv - 1)**2 / (2 * Kv)
    Wv = Wf(Kv * Pm); Wpv = Wfp(Kv * Pm)
    lv = f["lam"](*pt)
    ndl = sum(nu[c] * dlv[c] for c in range(D)); ndPi = sum(nu[c] * dPi[c] for c in range(D))
    # rho
    rho_cov = sum(nu[a] * nu[b] * T[a, b] for a in range(D) for b in range(D))
    rho_adm = mu**2 * (Qv**2 - 1) / (2 * Kv) + Wv + Piv + gam * Fv
    # momentum density J_a = -n^m h_a^n T_mn
    J_cov = [-sum(nu[m] * h[n_, a] * T[m, n_] for m in range(D) for n_ in range(D)) for a in range(D)]
    J_adm = [Pl_[a] * (ndl + lv - gam * (ndPi - Piv * ndl)) for a in range(D)]
    lam_star = -(1 + gam * Piv) * ndl + gam * ndPi
    J_on = [Pl_[a] * (ndl + lam_star - gam * (ndPi - Piv * ndl)) for a in range(D)]
    # spatial stress S_ab = h_a^m h_b^n T_mn
    S_cov = [[sum(h[m, a] * h[n_, b] * T[m, n_] for m in range(D) for n_ in range(D)) for b in range(D)] for a in range(D)]
    S_adm = [[hl[a][b] * (PA + LK + gam * (Fv + PE) - Wv) - (Pl_[a] * A[b] + Pl_[b] * A[a])
              - gam * (Pl_[a] * E[b] + Pl_[b] * E[a]) + Kv * Wpv * Pl_[a] * Pl_[b] / Pm for b in range(D)] for a in range(D)]
    scale = max(abs(S_cov[a][b]) for a in range(D) for b in range(D))
    row = {"seed": seed, "rho": rel(rho_cov, rho_adm),
           "J": max(float(abs(J_cov[a] - J_adm[a]) / max(abs(x) for x in J_cov)) for a in range(D)),
           "J_on_shell_abs": max(float(abs(x)) for x in J_on),
           "S": max(float(abs(S_cov[a][b] - S_adm[a][b]) / scale) for a in range(D) for b in range(D))}
    out["rows"].append(row); print(row, flush=True)
mx = max(max(r["rho"], r["J"], r["S"], r["J_on_shell_abs"]) for r in out["rows"])
out["max"] = mx; out["pass"] = mx <= 1e-10
json.dump(out, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "adm_check.json"), "w"), indent=1)
print("B1-N", "PASS" if out["pass"] else "FAIL", mx)
