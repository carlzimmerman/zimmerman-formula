#!/usr/bin/env python3
"""C5_health: is the covariant screened theory (C4's Khronon + P parent) healthy? And C1/C3's AeST + gamma_L version?

Theory family T(beta, eta, gamma_L, gamma_F, mu_K, W) in unitary gauge (tau = t), K = 4 pi G, c = 1:
  L/(N sqrt h) = [R3 + K_ij K^ij - (1+beta) theta^2 + 2 mu_K^2 (1/N - 1)^2]/(4K) + xi P^i D_i ln N - W(u)
                 + (eta/2) E_i E^i - (gamma_L/2)(D.P)^2 - (gamma_F/4) F_ij F^ij,   u = K|P|, xi = 1.
C4-literal = (beta 0, eta 0, gamma_F 0): BS's covariant R has no (div n)^2 term; C4 named no P kinetic term.
C4 = A33  = (beta > 0, eta > 0, gamma_F = gamma_L, mu_K = 0).
All P-sector terms carry an overall 1/K after P = p/K, so K = 1 below; lengths in units of L*.

External input (on disk, outside the repo): SZ21 = arXiv:2007.00082 newRMONDLett.tex, eq. Minkowski_action and the dispersion
relations stated after it (path ../_external_data/aest_papers_2026_10_22/src_2007.00082/, sha256 in C2 PROVENANCE).
kappa = 1/2 FITTED. Footings 9.36e-11 / 1.13e-10 m/s^2, never pooled.

Run: OMP_NUM_THREADS=1 nice -n 10 python3 c5_health.py        (C5_MUTATE=1 for the mutation run)
"""
import json
import math
import os
import resource
import sys
import time

import mpmath as mp
import sympy as sp

T0 = time.time()
MUTATE = os.environ.get("C5_MUTATE", "0") == "1"
TAG = "_MUTATE" if MUTATE else ""
XI = 2 if MUTATE else 1          # mutation 1: clock coefficient
SZSGN = -1 if MUTATE else 1      # mutation 2: sign of SZ's K_B|A' - grad h00/2|^2 term
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
OUT = os.path.join(HERE, f"c5_health{TAG}.out")
JSON = os.path.join(HERE, f"c5_health_results{TAG}.json")
mp.mp.dps = 120

c_SI = 2.99792458e8
PC = 3.0856775814913673e16
AU = 1.495978707e11
GMSUN = 1.32712440018e20
A0 = {"canonical": 9.36e-11, "alt": 1.13e-10}
LSTARS = [20, 24, 90]
HBAR_EV_S = 6.582119569e-16
HBARC_EV_M = 1.973269804e-7
G_SI = 6.67430e-11
KPC = 1e3 * PC

lines, checks, res = [], [], {"mutate": MUTATE}


def log(s):
    print(s, flush=True)
    lines.append(s)


def check(kid, ok, value, thr):
    checks.append({"id": kid, "pass": bool(ok), "value": str(value), "threshold": thr})
    log(f"{kid} {'PASS' if ok else 'FAIL'} {value} {thr}")


def f2(v, n=4):
    return mp.nstr(v, n) if isinstance(v, (mp.mpf, mp.mpc)) else (f"{v:.{n}g}" if isinstance(v, float) else str(v))


# ==================================================================================== Part 1: local quadratic matrix
t, x, y, z = sp.symbols("t x y z", real=True)
eps = sp.Symbol("epsilon")
w, k = sp.symbols("omega k", positive=True)
beta, eta, gL, gF, muK, g, P0, th, W1, W2, xi = sp.symbols(
    "beta eta gamma_L gamma_F mu_K g P0 theta W1 W2 xi", real=True)
NAMES = ["n", "Nx", "Ny", "Nz", "zeta", "hp", "hx", "px", "py", "pz"]


def trunc(e):
    e = sp.expand(e)
    return sum(e.coeff(eps, i) * eps ** i for i in range(3))


def build_local():
    F = {nm: sp.Function(nm)(t, z) for nm in NAMES}
    st, ct = sp.sin(th), sp.cos(th)
    Pbar = [P0 * st, 0, P0 * ct]
    Nb = 1 + g * (st * x + ct * z)          # frozen background: lapse gradient g along P-bar
    N = Nb + eps * F["n"]
    Nlo = [eps * F["Nx"], eps * F["Ny"], eps * F["Nz"]]
    s = sp.Matrix([[2 * F["zeta"] + F["hp"], F["hx"], 0], [F["hx"], 2 * F["zeta"] - F["hp"], 0],
                   [0, 0, 2 * F["zeta"]]]) * eps        # spatial gauge: no dd E, no d_(i F_j)
    h = sp.eye(3) + s
    hinv = sp.eye(3) - s + s * s
    sq = 1 + s.trace() / 2 + (s.trace() ** 2 / 8 - (s * s).trace() / 4)
    Xs = (x, y, z)
    Gam = [[[trunc(sum(hinv[a, d] * (sp.diff(h[d, b], Xs[cc]) + sp.diff(h[d, cc], Xs[b]) - sp.diff(h[b, cc], Xs[d]))
                       for d in range(3)) / 2) for cc in range(3)] for b in range(3)] for a in range(3)]
    Ric = sp.zeros(3)
    for b in range(3):
        for d in range(3):
            e = 0
            for a in range(3):
                e += sp.diff(Gam[a][b][d], Xs[a]) - sp.diff(Gam[a][b][a], Xs[d])
                for cc in range(3):
                    e += Gam[a][a][cc] * Gam[cc][b][d] - Gam[a][d][cc] * Gam[cc][b][a]
            Ric[b, d] = trunc(e)
    R3 = trunc(sum(hinv[b, d] * Ric[b, d] for b in range(3) for d in range(3)))
    DN = [[sp.diff(Nlo[j], Xs[i]) for j in range(3)] for i in range(3)]
    Kij = sp.Matrix(3, 3, lambda i, j: (sp.diff(h[i, j], t) - DN[i][j] - DN[j][i]) / 2)
    K2 = trunc(sum(Kij[i, j] ** 2 for i in range(3) for j in range(3)))
    th1 = trunc(Kij.trace())
    Lgrav = trunc(N * sq * (R3 + K2 - (1 + beta) * th1 ** 2 + 2 * muK ** 2 * (1 / N - 1) ** 2) / 4)
    P = [Pbar[i] + eps * F[["px", "py", "pz"][i]] for i in range(3)]
    Pup = [trunc(sum(hinv[i, j] * P[j] for j in range(3))) for i in range(3)]
    clock = trunc(xi * sq * sum(Pup[i] * sp.diff(N, Xs[i]) for i in range(3)))   # N sqrt h P^i d_i ln N
    s2 = trunc(sum(Pup[i] * P[i] for i in range(3)))
    LW = -trunc(N * sq * (W1 * (s2 - P0 ** 2) + W2 / 2 * (s2 - P0 ** 2) ** 2))  # W as a function of u^2
    divP = trunc(sum(sp.diff(trunc(sq * Pup[i]), Xs[i]) for i in range(3)))
    LL = -gL / 2 * trunc(divP ** 2)
    Fij = [[sp.diff(P[j], Xs[i]) - sp.diff(P[i], Xs[j]) for j in range(3)] for i in range(3)]
    LF = -gF / 4 * trunc(sum(Fij[i][j] ** 2 for i in range(3) for j in range(3)))
    Ei = [sp.diff(P[i], t) - sum(Nlo[j] * sp.diff(P[i], Xs[j]) + P[j] * sp.diff(Nlo[j], Xs[i]) for j in range(3))
          for i in range(3)]
    LE = eta / 2 * trunc(sum(Ei[i] ** 2 for i in range(3)))
    L2 = sp.expand(Lgrav + clock + LW + LL + LF + LE).coeff(eps, 2)
    return quad_matrix(L2, [F[nm] for nm in NAMES], (t, z), {x: 0, y: 0, z: 0})


def quad_matrix(L2, fields, tz, frozen):
    """theta-averaged quadratic Lagrangian of plane waves exp(i(kz - wt)) -> Hermitian matrix (A^dagger M A)."""
    tt, zz = tz
    idx = {f: i for i, f in enumerate(fields)}

    def sym_of(d):
        if isinstance(d, sp.Derivative):
            f = d.expr
            nt = sum(cc for v, cc in d.variable_count if v == tt)
            nz = sum(cc for v, cc in d.variable_count if v == zz)
        else:
            f, nt, nz = d, 0, 0
        return idx[f], (-sp.I * w) ** nt * (sp.I * k) ** nz

    n = len(fields)
    M = sp.zeros(n, n)
    for term in sp.Add.make_args(sp.expand(L2)):
        coef, fl = sp.Integer(1), []
        for fac, ex in term.as_powers_dict().items():
            if fac.has(*fields):
                fl += [fac] * int(ex)
            else:
                coef *= fac ** ex
        coef = coef.subs(frozen)
        if coef == 0:
            continue
        assert len(fl) == 2, term
        (a, sa), (b, sb) = sym_of(fl[0]), sym_of(fl[1])
        M[b, a] += coef * sa * sp.conjugate(sb)
        M[a, b] += coef * sp.conjugate(sa) * sb
    return M.applyfunc(sp.expand)


log(f"C5_health  mutate={MUTATE}  (xi={XI}, SZ K_B-term sign={SZSGN})")
Mloc = build_local()
herm = (Mloc - Mloc.H).applyfunc(sp.simplify) == sp.zeros(10, 10)
log(f"  local quadratic matrix built (10 fields: {NAMES}); Hermitian: {herm}; {time.time() - T0:.1f} s")

# ------------------------------------------------------------------ H1: Minkowski vs A68
M0s = Mloc.subs({P0: 0, g: 0, muK: 0, xi: XI, W1: sp.Rational(1, 2), W2: 0}).applyfunc(sp.simplify)
det0 = sp.factor(M0s.det(method="berkowitz"))
prod = (w ** 2 - k ** 2) ** 2 * (eta * w ** 2 - gF * k ** 2 - 1) ** 2 * (w ** 2 * (eta * k ** 2 + (2 + 3 * beta) / beta)
                                                                       - gL * k ** 4)
ratio = sp.cancel(det0 / prod)
r_free = sp.simplify(sp.diff(ratio, w))
res["H1"] = {"det_Minkowski": str(det0), "det_over_expected": str(ratio), "d_ratio_d_omega": str(r_free),
             "expected": "tensor w^2=k^2 (x2); transverse P w^2=(K+gamma_F k^2)/eta (x2); "
                         "scalar w^2 = gamma_L k^4/(K(2+3beta)/beta + eta k^2) (A68)"}
check("H1", herm and r_free == 0 and ratio != 0, f"det/expected = {ratio} (omega-free: {r_free == 0}); Hermitian {herm}",
      "residual 0 (A68's tensor, transverse-P and k^4 scalar exactly)")

# ------------------------------------------------------------------ numeric mode machinery
PN = ["P0", "g", "mu_K", "xi", "W1", "W2", "beta", "eta", "gamma_L", "gamma_F", "theta", "k"]
SYM = {s.name: s for s in Mloc.free_symbols}
ARGS = [SYM[nm] for nm in PN]
Mcoef = [Mloc.applyfunc(lambda e: sp.expand(e).coeff(w, j)) for j in range(3)]
assert (Mloc - Mcoef[0] - w * Mcoef[1] - w ** 2 * Mcoef[2]).applyfunc(sp.expand) == sp.zeros(10, 10)
FM = [sp.lambdify(ARGS, m, "mpmath") for m in Mcoef]


def mats(par, kval):
    a = [mp.mpf(par[nm]) if nm != "k" else mp.mpf(kval) for nm in PN]
    return [mp.matrix(f(*a).tolist()) for f in FM]


def detpoly(Ms, R, deg=20):
    Nn = deg + 4
    vals = [mp.det(Ms[0] + zz * Ms[1] + zz * zz * Ms[2])
            for zz in (R * mp.expjpi(mp.mpf(2 * j) / Nn) for j in range(Nn))]
    return [sum(vals[j] * mp.expjpi(-mp.mpf(2 * j * m) / Nn) for j in range(Nn)) / Nn / R ** m for m in range(Nn)]


def modes(par, kval):
    """roots of det M(omega) (one of each +-omega pair), with nullity and Krein sign per root; zero-root count."""
    Ms = mats(par, kval)
    R = mp.mpf(kval)
    cs = detpoly(Ms, R)
    mx = max(abs(cc) * R ** i for i, cc in enumerate(cs))
    cs = [cc if abs(cc) * R ** i > mp.mpf(10) ** -80 * mx else 0 for i, cc in enumerate(cs)]
    nz = 0
    while cs and cs[0] == 0:
        cs, nz = cs[1:], nz + 1
    while cs and cs[-1] == 0:
        cs = cs[:-1]
    roots = mp.polyroots(cs[::-1], maxsteps=800, extraprec=600) if len(cs) > 1 else []
    out = []
    for r in roots:
        if mp.re(r) < -mp.mpf(10) ** -30 * abs(r) or (abs(mp.re(r)) <= mp.mpf(10) ** -30 * abs(r) and mp.im(r) < 0):
            continue
        A = Ms[0] + r * Ms[1] + r * r * Ms[2]
        U, Sv, V = mp.svd_c(A)
        Vh = V.transpose_conj()
        dM = Ms[1] + 2 * r * Ms[2]
        nulls = [i for i in range(10) if Sv[i] < mp.mpf(10) ** -40 * Sv[0]]
        kre = [mp.re(r * (Vh[:, i].transpose_conj() * dM * Vh[:, i])[0]) for i in nulls]
        out.append({"w": r, "w2": r * r, "krein": kre, "nullity": len(nulls)})
    return {"zero_roots": nz, "deg": len(cs) - 1, "roots": out, "Ms": Ms}


def clusters_of(mo):
    """numerically split degenerate roots grouped; multiplicity = max(cluster size, null-space dimension)."""
    cls = []
    for rr in mo["roots"]:
        for cl in cls:
            if abs(rr["w"] - cl[0]["w"]) <= mp.mpf(10) ** -20 * abs(cl[0]["w"]):
                cl.append(rr)
                break
        else:
            cls.append([rr])
    return [(cl[0]["w2"], max(len(cl), max(r_["nullity"] for r_ in cl))) for cl in cls]


def summarize(mo, kval):
    """distinct roots with multiplicity; stable iff all w^2 real >= 0; ghost-free iff all Krein > 0."""
    rs = mo["roots"]
    w2 = [rr["w2"] for rr in rs]
    unstable = [v for v in w2 if mp.re(v) < -mp.mpf(10) ** -30 * abs(v) or abs(mp.im(v)) > mp.mpf(10) ** -20 * abs(v)]
    kmin = min([q for rr in rs for q in rr["krein"]] + [mp.mpf(1)]) if rs else mp.mpf(1)
    stable_roots = [rr for rr in rs if rr["w2"] not in unstable]
    neg_krein = [q for rr in stable_roots for q in rr["krein"] if q <= 0]
    return {"n_modes": mo["deg"] // 2, "zero_roots": mo["zero_roots"], "n_unstable": len(unstable),
            "n_ghost": len(neg_krein), "w2_over_k2": [mp.re(v) / kval ** 2 for v in w2],
            "min_w2": min([mp.re(v) for v in w2]) if w2 else None, "min_krein": kmin}


def bg(a0L, y=0, beta_v=1, etaf=1.0, gFf=1.0, mu=0, theta=0.3, gval=None, u0=None):
    """background parameters in L* units (gamma_L = 1/2). u0 from the unscreened law (u = a0 y/(1+y)) unless given."""
    a0L = mp.mpf(a0L)
    if u0 is None:
        yy = mp.mpf(y)
        u0 = a0L * yy / (1 + yy)
    v = u0 / a0L
    MT = 1 / (1 - v)
    ML = MT ** 2
    W2v = (ML - MT) / (4 * u0 ** 2) if u0 > 0 else mp.mpf(0)
    gam = mp.mpf(1) / 2
    return dict(P0=u0, g=(a0L * mp.mpf(y) if gval is None else mp.mpf(gval)), mu_K=mu, xi=XI, W1=MT / 2, W2=W2v,
                beta=beta_v, eta=etaf * gam, gamma_L=gam, gamma_F=gFf * gam, theta=theta)


def a0L_of(foot, Lpc):
    return A0[foot] * Lpc * PC / c_SI ** 2


# ------------------------------------------------------------------ H4: mode counts, two routes
a0c24 = a0L_of("canonical", 24)
MU_BS = (24 * PC) / (100 * KPC)   # mu_K L* for mu^-1 = 100 kpc (BS24 Eq. 39 lower bound, via C4)
rows = {
    "A33 (beta=1, eta=gamma, gF=gL, mu=0)": dict(beta_v=1, etaf=1, gFf=1, mu=0),
    "C4-literal (beta=0, eta=0, gF=0, mu=0)": dict(beta_v=0, etaf=0, gFf=0, mu=0),
    "C4-literal + BS dust (mu^-1=100 kpc)": dict(beta_v=0, etaf=0, gFf=0, mu=MU_BS),
    "beta=0, eta=gamma, gF=gL": dict(beta_v=0, etaf=1, gFf=1, mu=0),
    "beta=1, eta=0, gF=gL": dict(beta_v=1, etaf=0, gFf=1, mu=0),
    "A33 + BS dust": dict(beta_v=1, etaf=1, gFf=1, mu=MU_BS),
}
h4, ok4 = {}, True
for lab, kw in rows.items():
    for bgl, yv in (("Minkowski", 0), ("y=1", 1)):
        mo = modes(bg(a0c24, y=yv, **kw), mp.mpf(1))
        route1 = mo["deg"] // 2
        route2 = sum(mult for _, mult in clusters_of(mo))
        sm = summarize(mo, mp.mpf(1))
        h4[f"{lab} | {bgl}"] = {"route1_modes": route1, "route2_nullity_sum": route2, "zero_roots": mo["zero_roots"],
                                "n_unstable": sm["n_unstable"], "n_ghost": sm["n_ghost"],
                                "w2_over_k2": [f2(v, 6) for v in sm["w2_over_k2"]]}
        ok4 &= route1 == route2
        log(f"  H4 {lab:42s} {bgl:9s}: modes {route1} (route2 {route2}), omega=0 roots {mo['zero_roots']}, "
            f"unstable {sm['n_unstable']}, ghost {sm['n_ghost']}, w2/k2 {[f2(v, 4) for v in sm['w2_over_k2']]}")
a33_count = h4["A33 (beta=1, eta=gamma, gF=gL, mu=0) | Minkowski"]["route1_modes"]
res["H4"] = h4
check("H4", ok4 and a33_count == 5, f"routes agree on all {len(h4)} rows: {ok4}; A33 count {a33_count}; "
                                    f"C4-literal {h4['C4-literal (beta=0, eta=0, gF=0, mu=0) | y=1']['route1_modes']} modes "
                                    f"+ {h4['C4-literal (beta=0, eta=0, gF=0, mu=0) | y=1']['zero_roots']} omega=0 roots",
      "routes agree AND A33 = 5 (A68)")


# ------------------------------------------------------------------ H5: closed form (decoupling limit) vs full
def closed_w2(par, kval):
    """decoupling limit: tensors w^2 = k^2 (x2) + P system Kin = diag(B/k^2 + eta, eta, eta),
    Pot = [[gL k^2 + Mzz - 1, Mzx, 0], [Mzx, gF k^2 + Mxx, 0], [0, 0, gF k^2 + MT]] with M = MT I + (ML-MT) Phat Phat."""
    kk = mp.mpf(kval)
    MT = 2 * par["W1"]
    ML = MT + 4 * par["W2"] * par["P0"] ** 2
    st, ct = mp.sin(par["theta"]), mp.cos(par["theta"])
    Mzz, Mxx, Mzx = MT + (ML - MT) * ct ** 2, MT + (ML - MT) * st ** 2, (ML - MT) * st * ct
    B = (2 + 3 * mp.mpf(par["beta"])) / mp.mpf(par["beta"])
    Kin = mp.matrix([[B / kk ** 2 + par["eta"], 0, 0], [0, par["eta"], 0], [0, 0, par["eta"]]])
    Pot = mp.matrix([[par["gamma_L"] * kk ** 2 + Mzz - 1, Mzx, 0], [Mzx, par["gamma_F"] * kk ** 2 + Mxx, 0],
                     [0, 0, par["gamma_F"] * kk ** 2 + MT]])
    ev = mp.eig(mp.inverse(Kin) * Pot, left=False, right=False)
    return sorted([kk ** 2, kk ** 2] + [mp.re(e) for e in ev])


def bg_named(foot, Lpc, name, xe=None, beta_v=1, etaf=1):
    a0L = a0L_of(foot, Lpc)
    Lm = Lpc * PC
    if name == "Minkowski":
        return bg(a0L, 0, beta_v, etaf), [mp.mpf("1e-3"), mp.mpf(1), mp.mpf(1000)]
    if name == "galaxy y=1":
        return bg(a0L, 1, beta_v, etaf), [mp.mpf("1e-3"), mp.mpf(1), mp.mpf(1000)]
    if name.startswith("unscreened"):
        yv = mp.mpf(name.split("=")[1])
        return bg(a0L, yv, beta_v, etaf), [mp.mpf("1e-3"), mp.mpf(1), mp.mpf(1000)]
    if name == "Solar System":   # screened: P at the Galactic external value; local g at 1 AU
        u0 = mp.mpf(a0L) * xe / (1 + xe)
        gl = GMSUN / AU ** 2 * Lm / c_SI ** 2
        return bg(a0L, 0, beta_v, etaf, u0=u0, gval=gl), [mp.mpf(Lm / AU), mp.mpf(Lm / (100 * AU))]
    if name == "NS":             # screened; local g = 1e12 m/s^2 at r = 10 km
        u0 = mp.mpf(a0L) * xe / (1 + xe)
        gl = 1e12 * Lm / c_SI ** 2
        return bg(a0L, 0, beta_v, etaf, u0=u0, gval=gl), [mp.mpf(Lm / 1e4)]
    raise ValueError(name)


XE = {}
d7d = json.load(open(os.path.join(ROOT, "doors_push_2026_10_22/D7d_screened_q2/d7d_screened_q2_results.json")))
for key, v in d7d["R2_scan"].items():
    if isinstance(v, dict) and "x_e" in v:
        XE.setdefault(key.split("|")[0], []).append(float(v["x_e"]))
res["x_e_D7d"] = XE
h5, maxdev, maxdrop, worst = {}, mp.mpf(0), mp.mpf(0), ""
for foot in ("canonical", "alt"):
    for Lpc in LSTARS:
        for name in ("Minkowski", "galaxy y=1", "Solar System", "NS"):
            xes = XE[foot] if name in ("Solar System",) else [sorted(XE[foot])[len(XE[foot]) // 2]]
            for xe in xes:
                par, ks = bg_named(foot, Lpc, name, mp.mpf(xe))
                for kk in ks:
                    mo = modes(par, kk)
                    full = sorted([mp.re(w2_) for w2_, mult in clusters_of(mo) for _ in range(mult)])
                    cl = closed_w2(par, kk)
                    dev = max(abs(a - b) / abs(b) for a, b in zip(full, cl)) if len(full) == len(cl) else mp.mpf(1)
                    drop = max(par["g"] / kk, par["eta"] * par["P0"] ** 2, par["gamma_L"] * par["P0"] ** 2)
                    key = f"{foot}|{Lpc}pc|{name}|x_e={xe:.3f}|kL*={f2(kk, 3)}"
                    h5[key] = {"max_rel_dev": f2(dev, 3), "dropped_max": f2(drop, 3), "g_over_k": f2(par["g"] / kk, 3)}
                    if dev > maxdev:
                        maxdev, worst = dev, key
                    maxdrop = max(maxdrop, drop)
# the NS row separately (weak-field frozen expansion is not valid at NS compactness)
nonNS = [v for kk_, v in h5.items() if "|NS|" not in kk_]
dev_nonNS = max(mp.mpf(v["max_rel_dev"]) for v in nonNS)
drop_nonNS = max(mp.mpf(v["dropped_max"]) for v in nonNS)
res["H5"] = {"rows": h5, "max_dev_all": f2(maxdev, 3), "worst": worst, "max_dropped_all": f2(maxdrop, 3),
             "max_dev_without_NS": f2(dev_nonNS, 3), "max_dropped_without_NS": f2(drop_nonNS, 3),
             "closed_form": "tensor w^2 = k^2; P: det[w^2 diag(B/k^2+eta, eta, eta) - Pot] = 0, "
                            "Pot = [[gL k^2 + Mzz - 1, Mzx, 0],[Mzx, gF k^2 + Mxx, 0],[0,0,gF k^2 + MT]], "
                            "M = MT I + (ML - MT) Phat Phat, MT = W'(u0)/u0 K^-1 = a0/(a0-u0), ML = K W''(u0) = MT^2"}
check("H5", maxdev < mp.mpf("1e-6") and maxdrop < mp.mpf("1e-6"),
      f"max rel dev {f2(maxdev, 3)} at {worst}; max dropped factor {f2(maxdrop, 3)}; "
      f"without the NS row: dev {f2(dev_nonNS, 3)}, dropped {f2(drop_nonNS, 3)}",
      "both < 1e-6 at every record background (NS included)")

# ------------------------------------------------------------------ H6: strong fields (J outside BS's class), A33 values
h6, ok6, n6 = {}, True, 0
speed_max = mp.mpf(0)
for foot in ("canonical", "alt"):
    for Lpc in LSTARS:
        for etaf in (1, 10):
            for beta_v in (1, mp.mpf("1e-3")):
                names = ["unscreened y=1e2", "unscreened y=1e4", "unscreened y=1e8", "Solar System", "NS"]
                for name in names:
                    xe = mp.mpf(max(XE[foot])) if name in ("Solar System", "NS") else None
                    par, ks = bg_named(foot, Lpc, name, xe, beta_v=beta_v, etaf=etaf)
                    kgrid = [mp.mpf("1e-3"), mp.mpf(1), mp.mpf(1000)] + (ks if name in ("Solar System", "NS") else [])
                    for kk in kgrid:
                        sm = summarize(modes(par, kk), kk)
                        n6 += 1
                        good = sm["n_unstable"] == 0 and sm["n_ghost"] == 0
                        ok6 &= good
                        key = f"{foot}|{Lpc}pc|eta={etaf}gamma|beta={f2(beta_v, 2)}|{name}|kL*={f2(kk, 3)}"
                        h6[key] = {"stable": sm["n_unstable"] == 0, "ghost_free": sm["n_ghost"] == 0,
                                   "max_w2_over_k2": f2(max(sm["w2_over_k2"]), 4), "g_over_k": f2(par["g"] / kk, 3)}
                        speed_max = max(speed_max, max(sm["w2_over_k2"]))
valid6 = [v for v in h6.values() if float(v["g_over_k"]) < 1]
bad6 = [kk_ for kk_, v in h6.items() if not (v["stable"] and v["ghost_free"])]
log(f"  H6 (post hoc reading, not a frozen line): {len(valid6)} points with g/k < 1 (frozen-coefficient WKB valid): "
    f"all healthy = {all(v['stable'] and v['ghost_free'] for v in valid6)}; {len(bad6)} failing points, "
    f"min g/k among them = {min([float(h6[q]['g_over_k']) for q in bad6] + [float('inf')]):.3g}")
res["H6"] = {"valid_wkb_points": len(valid6), "valid_all_healthy": all(v["stable"] and v["ghost_free"] for v in valid6),
             "failing_points": bad6, "n_points": n6, "all_healthy": ok6, "max_phase_speed2": f2(speed_max, 4), "rows": h6}
for kk_ in [q for q in h6 if q.startswith("canonical|24pc|eta=1gamma|beta=1|unscreened y=1e8")]:
    log(f"  H6 sample {kk_}: {h6[kk_]}")
check("H6", ok6, f"{n6} (footing, L*, eta, beta, background, k) points: no omega^2 < 0, no negative Krein norm; "
                 f"max phase speed^2 {f2(speed_max, 3)} (mass-dominated, finite k)",
      "all points stable and ghost-free")

# ------------------------------------------------------------------ H7: beta = 0 (BS's R) with eta > 0
def min_w2(par, kk):
    sm = summarize(modes(par, kk), kk)
    return sm["min_w2"], sm


a0L = a0L_of("canonical", 24)
kH7 = mp.mpf(10) ** 6
par0 = bg(a0L, 1, 0, 1, theta=0)
u0 = par0["P0"]
line = 2 * par0["eta"] * u0 ** 2
lo, hi = line / 100, line * 100
for _ in range(60):
    mid = mp.sqrt(lo * hi)
    m, _s = min_w2(bg(a0L, 1, mid, 1, theta=0), kH7)
    if m < 0:
        lo = mid
    else:
        hi = mid
beta_star = mp.sqrt(lo * hi)
rel7 = abs(beta_star / line - 1)
rate = {}
for thv in (0, mp.mpf("0.3")):
    m0, sm0 = min_w2(bg(a0L, 1, 0, 1, theta=thv), kH7)
    pred = -par0["gamma_L"] * par0["eta"] * u0 ** 2 * mp.cos(thv) ** 2 * kH7 ** 4
    rate[f"theta={f2(thv, 2)}"] = {"w2_min": f2(m0, 6), "pred_-gL_eta_u0^2_cos^2_k^4": f2(pred, 6),
                                   "ratio": f2(m0 / pred, 8)}
# Solar System at beta = 0 (Galactic external field, x_e = max), k = 1/AU
ss = {}
for foot in ("canonical", "alt"):
    par, ks = bg_named(foot, 24, "Solar System", mp.mpf(max(XE[foot])), beta_v=0, etaf=1)
    m, sm = min_w2(par, ks[0])
    Lm = 24 * PC
    rate_SI = mp.sqrt(-m) * c_SI / Lm if m < 0 else 0
    ss[foot] = {"w2_min_Lstar_units": f2(m, 6), "growth_rate_per_yr": f2(rate_SI * 3.15576e7, 4)}
res["H7"] = {"beta_star_bisected": f2(beta_star, 8), "round2_line_2eta_u0^2": f2(line, 8), "rel": f2(rel7, 3),
             "beta0_rate": rate, "solar_system_beta0": ss,
             "reading": "beta=0 with eta>0 and u0 != 0: one scalar root w^2 = -gamma_L eta u0^2 cos^2(theta) k^4 (K=1): "
                        "gradient instability with rate ~ k^2 (Hadamard ill-posed)"}
log(f"  H7 beta* = {f2(beta_star, 6)} vs 2 eta u0^2 = {f2(line, 6)}; beta=0 rates {rate}; Solar System {ss}")
check("H7", rel7 < mp.mpf("1e-3"), f"sign change at beta = {f2(beta_star, 6)} vs round-2 line {f2(line, 6)} "
                                   f"(rel {f2(rel7, 2)}, aligned theta = 0, kL* = 1e6)", "rel < 1e-3")

# ------------------------------------------------------------------ H8: the k^4 mode and its strong-coupling scale
k4 = {}
for lab, par in (("A33 Minkowski", bg(a0L, 0, 1, 1)), ("A33 galaxy y=1", bg(a0L, 1, 1, 1)),
                 ("beta=0 Minkowski", bg(a0L, 0, 0, 1))):
    vals = []
    for kk in (mp.mpf("1e-4"), mp.mpf("1e-3")):
        sm = summarize(modes(par, kk), kk)
        vals.append(min(sm["w2_over_k2"]) if sm["w2_over_k2"] else None)
    k4[lab] = {"min_w2_over_k2_at_kL*=1e-4,1e-3": [f2(v, 6) if v is not None else None for v in vals],
               "zero_roots": summarize(modes(par, mp.mpf("1e-3")), mp.mpf("1e-3"))["zero_roots"]}
# natural units (hbar = c = 1, eV)
Mp_eV = math.sqrt(1.054571817e-34 * c_SI ** 5 / G_SI) / 1.602176634e-19
Knat = 4 * math.pi / Mp_eV ** 2                       # eV^-2
psc = {}
ok8 = True
for foot in ("canonical", "alt"):
    a0nat = A0[foot] * HBAR_EV_S / c_SI            # eV
    Hnat = math.sqrt(64 * math.pi * a0nat ** 2 / (3 * 5))   # round-2: H^2 = 64 pi a0^2/(3(2+3beta)), beta = 1
    for Lpc in LSTARS:
        Lnat = Lpc * PC / HBARC_EV_M                # eV^-1
        alpha = Knat * Lnat ** 2 / 2
        B = Knat * 5.0                              # beta = 1
        p_B = Knat ** 4 / (9 * a0nat ** 2 * math.sqrt(B) * alpha ** 2.5)
        p_eta = Knat ** 2 / (3 * a0nat * alpha ** 1.5)          # eta = alpha
        p_A69 = Knat ** 2 / (8.485 * math.pi * a0nat * alpha ** 1.5)
        k_cross = math.sqrt(B / alpha)
        psc[f"{foot}|{Lpc}pc"] = {"p_sc_B_regime_eV": p_B, "p_sc_eta_regime_eV": p_eta, "A69_formula_eV": p_A69,
                                  "H_native_eV": Hnat, "regime_crossover_k_eV": k_cross,
                                  "p_B/H": p_B / Hnat, "p_eta/H": p_eta / Hnat}
        ok8 &= p_B < Hnat and p_eta < Hnat
res["H8"] = {"k4_mode": k4, "strong_coupling": psc, "K_nat_eV^-2": Knat,
             "formulae": "B-regime (eta k^2 << B): p_sc = K^4/(9 a0^2 B^1/2 alpha^5/2); eta-regime (eta = alpha): "
                         "p_sc = K^2/(3 a0 alpha^3/2); A69: K^2/(8.485 pi a0 alpha^3/2). Potential-only cubic K^2|P|^3/(3a0)."}
log(f"  H8 k^4 mode: {k4}")
log(f"  H8 p_sc canonical 24 pc: {psc['canonical|24pc']}")
check("H8", ok8, f"max p_sc/H_native: B-regime {max(v['p_B/H'] for v in psc.values()):.3e}, "
                 f"eta-regime {max(v['p_eta/H'] for v in psc.values()):.3e} (both footings, L* 20/24/90 pc)",
      "< 1 in both regimes (weakly coupled on all sub-Hubble scales)")

# ==================================================================================== Part 2: FRW
eps2 = sp.Symbol("eps2")
kF, KF = sp.symbols("k K", positive=True)
Lam = sp.Symbol("Lambda", real=True)
af = sp.Function("a")(t)
Nbf = sp.Function("Nb")(t)
Kq = sp.Function("Kq")
cs_, sn_ = sp.symbols("cs sn")
zt, nn, ps, sg = [sp.Function(nm)(t) for nm in ("zeta", "nF", "psi", "sigma")]
C, Sn = sp.cos(kF * x), sp.sin(kF * x)
Zf = eps2 * zt * C
Nf = Nbf * (1 + eps2 * nn * C)
Xs = (x, y, z)
hF = af ** 2 * sp.exp(2 * Zf) * sp.eye(3)
hiF = af ** -2 * sp.exp(-2 * Zf) * sp.eye(3)
sqF = af ** 3 * sp.exp(3 * Zf)
NloF = [sp.diff(eps2 * ps * C, v) for v in Xs]
PloF = [sp.diff(eps2 * sg * C, v) for v in Xs]
GamF = [[[sum(hiF[a_, d] * (sp.diff(hF[d, b], Xs[cc]) + sp.diff(hF[d, cc], Xs[b]) - sp.diff(hF[b, cc], Xs[d]))
              for d in range(3)) / 2 for cc in range(3)] for b in range(3)] for a_ in range(3)]
RicF = sp.zeros(3)
for b in range(3):
    for d in range(3):
        e = 0
        for a_ in range(3):
            e += sp.diff(GamF[a_][b][d], Xs[a_]) - sp.diff(GamF[a_][b][a_], Xs[d])
            for cc in range(3):
                e += GamF[a_][a_][cc] * GamF[cc][b][d] - GamF[a_][d][cc] * GamF[cc][b][a_]
        RicF[b, d] = e
R3F = sum(hiF[b, d] * RicF[b, d] for b in range(3) for d in range(3))
DNF = [[sp.diff(NloF[j], Xs[i]) - sum(GamF[m][i][j] * NloF[m] for m in range(3)) for j in range(3)] for i in range(3)]
KijF = sp.Matrix(3, 3, lambda i, j: (sp.diff(hF[i, j], t) - DNF[i][j] - DNF[j][i]) / (2 * Nf))
KKF = sum(hiF[i, i] * hiF[j, j] * KijF[i, j] ** 2 for i in range(3) for j in range(3))
thF = sum(hiF[i, i] * KijF[i, i] for i in range(3))
LgF = Nf * sqF * (R3F + KKF - (1 + beta) * thF ** 2 - 2 * Lam + 2 * Kq(1 / Nf)) / (4 * KF)
NupF = [hiF[j, j] * NloF[j] for j in range(3)]
EF = [(sp.diff(PloF[i], t) - sum(NupF[j] * sp.diff(PloF[i], Xs[j]) + PloF[j] * sp.diff(NupF[j], Xs[i]) for j in range(3)))
      / Nf for i in range(3)]
E2F = sum(hiF[i, i] * EF[i] ** 2 for i in range(3))
u2F = KF ** 2 * sum(hiF[i, i] * PloF[i] ** 2 for i in range(3))
divPF = sum(sp.diff(sqF * hiF[i, i] * PloF[i], Xs[i]) for i in range(3)) / sqF
clockF = XI * sqF * sum(hiF[i, i] * PloF[i] * sp.diff(Nf, Xs[i]) for i in range(3))
LPF = clockF + Nf * sqF * (-u2F / (2 * KF) + eta / 2 * E2F - gL / 2 * divPF ** 2)  # P-bar = 0: W = u^2/2K, F = 0
L2F = sp.series(LgF + LPF, eps2, 0, 3).removeO().coeff(eps2, 2)
L2F = sp.expand(L2F.subs({C: cs_, Sn: sn_}))
L2F = sp.expand(L2F.subs({cs_ ** 2: sp.Rational(1, 2), sn_ ** 2: sp.Rational(1, 2)}).subs({cs_ * sn_: 0})
                .subs({cs_: 0, sn_: 0}))
zd, sd, Zs, Ns, Ps, Ss = sp.symbols("zd sd Z_ N_ P_ S_")
ad, Nd, Hh, Hd = sp.symbols("ad Nd H Hd")
A_, Nb_ = sp.symbols("a_ Nb_", positive=True)
K0, K1, K2, K3 = sp.symbols("Kq0 Kq1 Kq2 Kq3")
LF0 = L2F.subs({sp.diff(zt, t): zd, sp.diff(sg, t): sd}).subs({zt: Zs, nn: Ns, ps: Ps, sg: Ss})
LF0 = LF0.subs({sp.diff(af, t): ad, sp.diff(Nbf, t): Nd}).subs({af: A_, Nbf: Nb_})
LF0 = LF0.replace(lambda e: isinstance(e, sp.Subs), lambda e: e.doit())
LF0 = LF0.replace(lambda e: isinstance(e, sp.Derivative) and e.expr.func == Kq and len(e.variables) == 2, lambda e: K2)
LF0 = LF0.replace(lambda e: isinstance(e, sp.Derivative) and e.expr.func == Kq and len(e.variables) == 1, lambda e: K1)
LF0 = LF0.replace(lambda e: isinstance(e, sp.Function) and e.func == Kq, lambda e: K0)
LF0 = LF0.replace(lambda e: isinstance(e, sp.Subs), lambda e: e.expr)
LF0 = sp.expand(LF0.subs(ad, A_ * Hh * Nb_))


def Dt(e):
    e = sp.sympify(e)
    return sp.expand(sp.diff(e, A_) * A_ * Hh * Nb_ + sp.diff(e, Nb_) * Nd + sp.diff(e, Hh) * Hd
                     + sp.diff(e, K0) * K1 * (-Nd / Nb_ ** 2) + sp.diff(e, K1) * K2 * (-Nd / Nb_ ** 2)
                     + sp.diff(e, K2) * K3 * (-Nd / Nb_ ** 2))


# background: lapse equation and a equation of the minisuperspace action
Lbg = A_ ** 3 * (-3 * (2 + 3 * beta) * Hh ** 2 * Nb_ + 2 * Nb_ * K0 - 2 * Lam * Nb_) / (4 * KF)  # (with a' = a H Nb)
tt_ = sp.Symbol("tt")
aT, NT = sp.Function("aT")(tt_), sp.Function("NT")(tt_)
KT = sp.Function("KT")
LbgT = aT ** 3 * (-3 * (2 + 3 * beta) * sp.diff(aT, tt_) ** 2 / (aT ** 2 * NT) + 2 * NT * KT(1 / NT) - 2 * Lam * NT) / (4 * KF)
EN = sp.diff(LbgT, NT)
Ea = sp.diff(sp.diff(LbgT, sp.diff(aT, tt_)), tt_) - sp.diff(LbgT, aT)


def bgsub(e):
    e = e.replace(lambda q: isinstance(q, sp.Subs), lambda q: q.doit())
    e = e.subs(sp.diff(aT, tt_, 2), sp.Symbol("add_")).subs(sp.diff(NT, tt_), Nd).subs(sp.diff(aT, tt_), sp.Symbol("adt_"))
    e = e.replace(lambda q: isinstance(q, sp.Derivative) and q.expr.func == KT, lambda q: K1)
    e = e.replace(lambda q: isinstance(q, sp.Function) and q.func == KT, lambda q: K0)
    e = e.replace(lambda q: isinstance(q, sp.Subs), lambda q: q.expr)
    return e.subs({aT: A_, NT: Nb_})


ENs = sp.expand(bgsub(EN).subs(sp.Symbol("adt_"), A_ * Hh * Nb_))
Eas = sp.expand(bgsub(Ea).subs(sp.Symbol("add_"), Dt(A_ * Hh * Nb_)).subs(sp.Symbol("adt_"), A_ * Hh * Nb_))
bsol = sp.solve([ENs, Eas], [Lam, Hd], dict=True)[0]
LF1 = sp.expand(LF0.subs(Lam, bsol[Lam]))
log(f"  FRW: background Lambda = {bsol[Lam]}, dH/dt = {bsol[Hd]}; {time.time() - T0:.1f} s")


def frw_reduce(LL, b0):
    if not b0:
        sol = sp.solve([sp.diff(LL, Ns), sp.diff(LL, Ps)], [Ns, Ps], dict=True)[0]
        return LL.subs(sol)
    L0 = sp.expand(LL.subs(beta, 0))
    cP = sp.diff(L0, Ps)
    assert not cP.has(Ps)
    return L0.subs(Ps, 0).subs(Ns, sp.solve(cP, Ns)[0])


def frw_forms(Lr):
    vs = (zd, sd, Zs, Ss)
    z0 = {v: 0 for v in vs}

    def gco(m):
        e = Lr
        for v, p in zip(vs, m):
            if p:
                e = sp.diff(e, v, p)
        return sp.cancel(e.subs(z0) / sp.prod([sp.factorial(p) for p in m]))

    Kin = sp.Matrix([[2 * gco((2, 0, 0, 0)), gco((1, 1, 0, 0))], [gco((1, 1, 0, 0)), 2 * gco((0, 2, 0, 0))]])
    Gy = (gco((1, 0, 0, 1)) - gco((0, 1, 1, 0))) / 2
    sym = (gco((1, 0, 0, 1)) + gco((0, 1, 1, 0))) / 2
    V = sp.Matrix([[-2 * gco((0, 0, 2, 0)) + Dt(gco((1, 0, 1, 0))), -gco((0, 0, 1, 1)) + Dt(sym)],
                   [-gco((0, 0, 1, 1)) + Dt(sym), -2 * gco((0, 0, 0, 2)) + Dt(gco((0, 1, 0, 1)))]])
    return Kin.applyfunc(sp.factor), Gy, V


# H2: de Sitter, K(Q) = 0, beta > 0 -> round-2
LdS = sp.expand(LF1.subs({K0: 0, K1: 0, K2: 0}))
LrdS = frw_reduce(LdS, False)
KinD, GyD, VD = frw_forms(LrdS)
dsub = {Nb_: 1, Nd: 0, Hd: 0, K3: 0}
# zeta has no kinetic term here: eliminate it (L = 1/2 Kin q'q' + Gy(z' s - s' z) - 1/2 qVq, frozen-free exact route)
vs = (zd, sd, Zs, Ss)


def gco_e(Lr, m):
    e = Lr
    for v, p in zip(vs, m):
        if p:
            e = sp.diff(e, v, p)
    return sp.cancel(e.subs({v: 0 for v in vs}) / sp.prod([sp.factorial(p) for p in m]))


gD = {m: gco_e(LrdS, m) for m in [(2, 0, 0, 0), (1, 1, 0, 0), (1, 0, 1, 0), (1, 0, 0, 1), (0, 2, 0, 0), (0, 0, 2, 0),
                                  (0, 0, 1, 1), (0, 0, 0, 2), (0, 1, 1, 0), (0, 1, 0, 1)]}
alpha_ = sp.cancel((gD[(0, 0, 2, 0)] - Dt(gD[(1, 0, 1, 0)]) / 2).subs(dsub))
b1_ = sp.cancel((gD[(0, 0, 1, 1)] - Dt(gD[(1, 0, 0, 1)])).subs(dsub))
b2_ = sp.cancel((gD[(0, 1, 1, 0)] - gD[(1, 0, 0, 1)]).subs(dsub))
Zsol = -(b1_ * Ss + b2_ * sd) / (2 * alpha_)
Lsig = sp.expand(alpha_ * Zsol ** 2 + Zsol * (b1_ * Ss + b2_ * sd) + gD[(0, 2, 0, 0)].subs(dsub) * sd ** 2
                 + gD[(0, 0, 0, 2)].subs(dsub) * Ss ** 2 + gD[(0, 1, 0, 1)].subs(dsub) * sd * Ss)
kin_s = sp.cancel(sp.diff(Lsig, sd, 2) / 2)
mass_s = sp.cancel((sp.diff(Lsig, Ss, 2) / 2 - Dt(sp.diff(Lsig, sd, Ss)) / 2).subs(dsub))
Bc = KF * (2 + 3 * beta) / beta
pphys = kF / A_
r_kin = sp.cancel(kin_s - A_ ** 3 * (Bc + eta * pphys ** 2) / 4)
r_mass = sp.cancel(mass_s + A_ ** 3 * (gL * pphys ** 4 + 2 * Bc * Hh ** 2) / 4)
res["H2"] = {"kin_residual": str(r_kin), "mass_residual": str(r_mass),
             "note": "x-average of cos^2 gives the overall 1/2: mine = round-2/2"}
check("H2", r_kin == 0 and r_mass == 0, f"kinetic residual {r_kin}, mass residual {r_mass}",
      "0 vs round-2's 1/2 a^3[(B + eta p^2) s'^2 - (gamma p^4 + 2 B H^2) s^2] (x 1/2 average)")

# H9: K(Q) dust, beta > 0 and beta = 0
LrA = frw_reduce(LF1, False)
LrB = frw_reduce(LF1, True)
KinA, GyA, VA = frw_forms(LrA)
KinB, GyB, VB = frw_forms(LrB)
log(f"  H9 kinetic matrix (beta != 0): {KinA}")
log(f"  H9 kinetic matrix (beta = 0):  {KinB}")
# dust sound speed (beta = 0, clock off): leading k^2 coefficient of V_zz / Kin_zz, physical units
VBzz = sp.cancel(VB[0, 0])
cs2 = sp.limit(sp.cancel(VBzz / KinB[0, 0]) * A_ ** 2 / (kF ** 2 * Nb_ ** 2), kF, sp.oo)
cs2 = sp.simplify(cs2.subs(Hd, bsol[Hd]).subs(beta, 0))   # the beta = 0 row (LrB); Hd re-inserts beta
r_cs2 = sp.simplify(cs2 - K1 * Nb_ / K2)
log(f"  H9 dust sound speed^2 (beta = 0, k >> aH): {cs2} ; minus K'/(Q K''): {r_cs2}")


def frw_numeric(Kin, Gy, V, beta_v, OmK, mu, Lst_H, etaf, kval):
    Q = mp.sqrt(1 + OmK * mp.mpf(3) * (2 + 3 * beta_v) / 2 / mu ** 2)
    Nbv = 1 / Q
    gam = Lst_H ** 2 / 2
    d = {A_: 1, Nb_: Nbv, Hh: 1, KF: 1, beta: beta_v, eta: etaf * gam, gL: gam, kF: kval,
         K0: mu ** 2 * (Q - 1) ** 2, K1: 2 * mu ** 2 * (Q - 1), K2: 2 * mu ** 2, K3: 0,
         Hd: -2 * mu ** 2 * (Q - 1) / (2 + 3 * beta_v), Nd: 3 * (Q - 1) * Nbv / Q ** 2}
    d = {kk_: sp.Float(str(v), 60) for kk_, v in d.items()}
    ev = lambda e: mp.mpmathify(sp.N(sp.sympify(e).subs(d), 60))
    Kn = mp.matrix([[ev(Kin[i, j]) for j in range(2)] for i in range(2)])
    Vn = mp.matrix([[ev(V[i, j]) for j in range(2)] for i in range(2)])
    Gn = ev(Gy)
    # det(-w^2 Kin - 2 i w Gy J + V) = 0, J = [[0, 1], [-1, 0]]
    c4 = Kn[0, 0] * Kn[1, 1] - Kn[0, 1] ** 2
    c2 = -(Kn[0, 0] * Vn[1, 1] + Kn[1, 1] * Vn[0, 0] - 2 * Kn[0, 1] * Vn[0, 1]) - 4 * Gn ** 2
    c0 = Vn[0, 0] * Vn[1, 1] - Vn[0, 1] ** 2
    if c4 == 0:
        roots = [-c0 / c2]
    else:
        disc = mp.sqrt(c2 ** 2 - 4 * c4 * c0)
        roots = [(-c2 + disc) / (2 * c4), (-c2 - disc) / (2 * c4)]
    return Kn, roots, Q


h9 = {}
Lst_H = mp.mpf(24 * PC) * mp.mpf(2.2e-18) / c_SI    # L* in Hubble units (illustrative H ~ 2.2e-18 s^-1)
for lab, (Kin, Gy, V, bv) in {"beta=1": (KinA, GyA, VA, 1), "beta=1e-3": (KinA, GyA, VA, mp.mpf("1e-3")),
                              "beta=0": (KinB, GyB, VB, 0)}.items():
    for etaf in (1, 0):
        for mu in (mp.mpf(100), mp.mpf("4.4e4")):
            rowv = []
            for kval in ("30", "1e3", "1e5", "1e7", "1e10"):
                Kn, roots, Q = frw_numeric(Kin, Gy, V, bv, mp.mpf("0.26"), mu, Lst_H, etaf, mp.mpf(kval))
                rowv.append({"k/aH": kval, "w2/H2": [f2(mp.re(r), 5) for r in roots],
                             "kin_diag": [f2(Kn[0, 0], 3), f2(Kn[1, 1], 3)]})
            h9[f"{lab}|eta={etaf}gamma|mu/H={f2(mu, 3)}"] = {"Q-1": f2(Q - 1, 4), "rows": rowv}
for kk_, v in h9.items():
    log(f"  H9 {kk_}: Q-1={v['Q-1']} " + "; ".join(f"k={r['k/aH']}: {r['w2/H2']}" for r in v["rows"]))


# classify: squared speeds in the band aH << k << mu (k = 30, 1e3 at mu = 4.4e4) and Jeans offsets
def band_speed(key):
    rws = h9[key]["rows"]
    w30 = min(mp.mpf(q) for q in rws[0]["w2/H2"])
    w1e3 = min(mp.mpf(q) for q in rws[1]["w2/H2"])
    s2 = (w1e3 - w30) / (mp.mpf(1000) ** 2 - 900)
    return s2, w30 - s2 * 900


bs = {kk_: band_speed(kk_) for kk_ in h9 if "mu/H=4.4e+4" in kk_}
for kk_, (s2, A) in bs.items():
    log(f"  H9 band aH<<k<<mu  {kk_}: squared speed {f2(s2, 4)} (beta/(2+3beta) = "
        f"{f2((lambda b: b / (2 + 3 * b))(mp.mpf(kk_.split('|')[0].split('=')[1])), 4)}), Jeans offset {f2(A, 4)} H^2")
kin_ok = True
for KinM, cond in ((KinA, {beta: 1}), (KinA, {beta: sp.Rational(1, 1000)}), (KinB, {})):
    kz = KinM[0, 0].subs(cond).subs({Hh: 1, Nb_: 1, A_: 1, KF: 1, K2: 2})
    ks_ = KinM[1, 1].subs(cond).subs({Hh: 1, Nb_: 1, A_: 1, KF: 1, eta: 1, kF: 1})
    kin_ok &= bool(kz > 0) and bool(ks_ > 0)
speeds_ok = all(s2 >= 0 for s2, _ in bs.values())
res["H9"] = {"kin_beta_nonzero": str(KinA), "kin_beta0": str(KinB), "dust_cs2_beta0": str(cs2),
             "dust_cs2_minus_Kp_over_QKpp": str(r_cs2), "numeric": h9,
             "band_speed2_and_jeans": {kk_: [f2(s2, 5), f2(A, 5)] for kk_, (s2, A) in bs.items()},
             "illustrative_background": "Omega_K = 0.26 (BS25's value, illustrative only), H = 1, a = 1, "
                                        "mu_K/H = 1e2 and 4.4e4 (mu^-1 = 100 kpc); no data verdict"}
check("H9", kin_ok and r_cs2 == 0 and speeds_ok,
      f"kinetic matrices positive (K''>0, beta>=0, eta>0): {kin_ok}; dust c_s^2 = K'/(Q K'') residual {r_cs2}; "
      f"band squared speeds " + ", ".join(f"{kk_.split('|')[0]}|{kk_.split('|')[1]}: {f2(s2, 3)}" for kk_, (s2, _) in bs.items()),
      "kinetic > 0 AND every sub-horizon squared speed >= 0 (beta > 0 and beta = 0 rows)")

# ==================================================================================== Part 3: AeST (SZ21 on disk)
KB, KK2, lam, Q0, Ls = sp.symbols("K_B K_2 lambda_s Q_0 L_s", real=True)
X4 = (t, x, y, z)
ETA4 = sp.diag(-1, 1, 1, 1)


def sz_lagrangian(hup, A, vphi, stiff=False):
    hlo = ETA4 * hup * ETA4
    htr = sum(ETA4[m, m] * hup[m, m] for m in range(4))
    d = lambda f, m: sp.diff(f, X4[m])
    up = lambda m: ETA4[m, m]
    L = -sp.Rational(1, 2) * sum(d(htr, m) * d(hup[m, nn_], nn_) for m in range(4) for nn_ in range(4))
    L += sp.Rational(1, 4) * sum(up(r) * d(htr, r) ** 2 for r in range(4))
    L += sp.Rational(1, 2) * sum(d(hup[m, r], m) * d(hup[nn_, s_], nn_) * ETA4[s_, r]
                                 for m in range(4) for nn_ in range(4) for r in range(4) for s_ in range(4))
    L += -sp.Rational(1, 4) * sum(up(r) * d(hup[m, nn_], r) * d(hlo[m, nn_], r)
                                  for r in range(4) for m in range(4) for nn_ in range(4))
    E = [d(A[i], 0) - sp.Rational(1, 2) * d(hup[0, 0], i + 1) for i in range(3)]
    V = [d(vphi, i + 1) + Q0 * A[i] for i in range(3)]
    L += SZSGN * KB * sum(e ** 2 for e in E)
    L += -2 * KB * sum(((d(A[j], i + 1) - d(A[i], j + 1)) / 2) ** 2 for i in range(3) for j in range(3))
    L += (2 - KB) * (2 * sum(E[i] * V[i] for i in range(3)) - (1 + lam) * sum(v ** 2 for v in V))
    L += 2 * KK2 * (d(vphi, 0) + Q0 * hup[0, 0] / 2) ** 2
    if stiff:   # C3's beta_L term, linearised on Minkowski (aether frame, h^{0i} = 0): -(2-K_B)(L*^2/2)(div V)^2
        L += -(2 - KB) * Ls ** 2 / 2 * sum(d(V[i], i + 1) for i in range(3)) ** 2
    return L


def sz_scalar(stiff=False):
    Psi, Phi, al, vp = [sp.Function(nm)(t, z) for nm in ("Psi", "Phi", "alpha", "varphi")]
    hup = sp.diag(-2 * Psi, -2 * Phi, -2 * Phi, -2 * Phi)
    A = [sp.diff(al, v) for v in (x, y, z)]
    return quad_matrix(sz_lagrangian(hup, A, vp, stiff), [Psi, Phi, al, vp], (t, z), {})


def sz_vector():
    W1f, b1f = [sp.Function(nm)(t, z) for nm in ("W1f", "b1f")]
    hup = sp.zeros(4)
    hup[0, 1] = hup[1, 0] = W1f
    return quad_matrix(sz_lagrangian(hup, [b1f, 0, 0], sp.Integer(0)), [W1f, b1f], (t, z), {})


Msz = sz_scalar()
Mvz = sz_vector()
dsz = sp.factor(Msz.det())
dvz = sp.factor(Mvz.det())
Msq = (2 - KB) * (1 + lam) * Q0 ** 2 / KB
w2_scalar_SZ = (2 - KB) * (1 + KB * lam / 2) * k ** 2 / (KK2 * KB) + Msq
w2_vector_SZ = k ** 2 + Msq
sol_s = [s_ for s_ in sp.solve(dsz, w ** 2 if False else w) if s_ != 0]
r_s = [sp.simplify(s_ ** 2 - w2_scalar_SZ) for s_ in sol_s]
sol_v = sp.solve(dvz, w)
r_v = [sp.simplify(s_ ** 2 - w2_vector_SZ) for s_ in sol_v]
deg_s = sp.Poly(dsz, w).degree()
res["H3"] = {"det_scalar": str(dsz), "det_vector": str(dvz), "scalar_residuals": [str(r) for r in r_s],
             "vector_residuals": [str(r) for r in r_v], "det_degree_in_omega": deg_s,
             "source": "newRMONDLett.tex eq. Minkowski_action; missing operator before K_B|...|^2 read as '+'"}
check("H3", all(r == 0 for r in r_s) and all(r == 0 for r in r_v) and deg_s == 4 and len(r_s) >= 1,
      f"scalar residuals {r_s}, vector residuals {r_v}; det degree in omega {deg_s} (omega^2 = 0 twice + one branch)",
      "all 0; two scalar branches (omega^2 = 0 and the massive one)")

# H10: AeST + gamma_L operator, capped F
Msz2 = sz_scalar(stiff=True)
dsz2 = sp.factor(Msz2.det())
sol2 = [s_ for s_ in sp.solve(dsz2, w) if s_ != 0]
w2_stiff = sp.simplify(sol2[0] ** 2)
w2_stiff_expect = w2_scalar_SZ + (2 - KB) * Ls ** 2 * Q0 ** 2 * k ** 2 / (2 * KB) + (2 - KB) * Ls ** 2 * k ** 4 / (4 * KK2)
r10 = sp.simplify(w2_stiff - w2_stiff_expect)
deg_s2 = sp.Poly(dsz2, w).degree()


def jordan_energy(M, wsym):
    """energy of the omega = 0 Jordan (linear-in-t) mode: E = v0^H M2 v0 + i v1^H M1 v0, M0 v1 = -i M1 v0."""
    Mz = M.subs(wsym, 0)
    M1 = sp.diff(M, wsym).subs(wsym, 0)
    M2 = sp.diff(M, wsym, 2) / 2
    outE = []
    for v0 in Mz.nullspace():
        sol, params = Mz.gauss_jordan_solve(-sp.I * M1 * v0)
        v1 = sol.subs({p_: 0 for p_ in params})
        outE.append(sp.factor(sp.simplify((v0.H * M2 * v0)[0] + sp.I * (v1.H * M1 * v0)[0])))
    return outE


EJ_aest = jordan_energy(Msz, w)
EJ_aest_st = jordan_energy(Msz2, w)
# Krein / sign scan of AeST + stiffness at capped-F background lambda values (aligned: lambda_L along V)
lam_cases = {"Y=0 (vacuum, FRW)": 0}
for foot in ("canonical", "alt"):
    xe = max(XE[foot])
    lam_cases[f"screened SS ({foot}, x_e={xe:.2f}): lambda_L=(1+x_e)^2-1"] = (1 + xe) ** 2 - 1
for yv in (1e2, 1e4, 1e8):
    lam_cases[f"unscreened y={yv:.0e}: lambda_L=(1+y)^2-1"] = (1 + yv) ** 2 - 1
h10, ok10 = {}, True
for KBv in (0.05, 1.0):
    for lab, lv in lam_cases.items():
        for kv in (1e-3, 1.0, 1e3):
            sub = {KB: KBv, KK2: 0.5, Q0: 1.0, Ls: 1.0, lam: lv, k: kv}
            Mn = Msz2.subs(sub)
            w2v = float(w2_stiff.subs(sub))
            wv = math.sqrt(w2v) if w2v > 0 else None
            krein = None
            if wv:
                wvm = sp.sqrt(w2_stiff.subs({kk_: sp.nsimplify(v_) for kk_, v_ in sub.items()}))
                Am = mp.matrix([[mp.mpmathify(sp.N(Msz2[i, j].subs({kk_: sp.nsimplify(v_) for kk_, v_ in sub.items()}).subs(w, wvm), 80))
                                 for j in range(4)] for i in range(4)])
                U, Sv, Vv = mp.svd_c(Am)
                v0 = Vv.transpose_conj()[:, 3]
                dMs = sp.diff(Msz2, w).subs({kk_: sp.nsimplify(v_) for kk_, v_ in sub.items()}).subs(w, wvm)
                dM = mp.matrix([[mp.mpmathify(sp.N(dMs[i, j], 80)) for j in range(4)] for i in range(4)])
                wv = mp.mpmathify(sp.N(wvm, 80))
                krein = float(mp.re(wv * (v0.transpose_conj() * dM * v0)[0]))
            ok10 &= w2v > 0 and (krein is None or krein > 0)
            h10[f"K_B={KBv}|{lab}|k={kv:g}"] = {"w2": w2v, "w2_over_k2": w2v / kv ** 2, "krein": krein}
vec_mass = {lab: f"(2-K_B)(1+lambda_T)Q0^2/K_B with lambda_T = {('x_e' if 'SS' in lab else ('y' if 'unscreened' in lab else '0'))}"
            for lab in lam_cases}
res["H10"] = {"w2_scalar_with_stiffness": str(w2_stiff), "residual_vs_closed_form": str(r10), "det_degree": deg_s2,
              "jordan_energy_AeST": [str(e) for e in EJ_aest], "jordan_energy_AeST_plus_stiffness": [str(e) for e in EJ_aest_st],
              "scan": h10, "vector_mass": vec_mass,
              "lambda_eff": "capped F: lambda_T = J'(Y) = y, lambda_L = J' + 2Y J'' = (1+y)^2 - 1 (y = g/a0); "
                            "Y = 0 (vacuum, FRW): lambda = 0"}
log(f"  H10 scalar w^2 (AeST + stiffness) = {w2_stiff}")
log(f"  H10 omega=0 Jordan-mode energy, AeST: {EJ_aest}")
log(f"  H10 omega=0 Jordan-mode energy, AeST + stiffness: {EJ_aest_st}")
check("H10", r10 == 0 and deg_s2 == 4 and ok10,
      f"w^2 residual {r10}; det degree {deg_s2} (count unchanged); all {len(h10)} scan points w^2 > 0, Krein > 0: {ok10}",
      "count unchanged AND every w^2 >= 0 for 0<K_B<2, K_2>0, lambda_eff >= 0")

# Khronon omega = 0 sector energies (Minkowski, beta = 0) for comparison with AeST's
EJ_kh = {}
for lab, extra in (("beta=0, eta=0, mu_K=0", {beta: 0, muK: 0, eta: 0}), ("beta=0, eta=0, mu_K>0", {beta: 0, eta: 0}),
                   ("beta=0, eta>0, mu_K>0", {beta: 0})):
    Mk = Mloc.subs({P0: 0, g: 0, xi: XI, W1: sp.Rational(1, 2), W2: 0, th: 0}).subs(extra).applyfunc(sp.simplify)
    EJ_kh[lab] = [str(e) for e in jordan_energy(Mk, w)]
res["khronon_omega0_energy"] = EJ_kh
log(f"  Khronon omega=0 Jordan-mode energy (Minkowski): {EJ_kh}")

# ==================================================================================== summary
npass = sum(ch["pass"] for ch in checks)
rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / (1024 ** 3 if sys.platform == "darwin" else 1024 ** 2)
res.update(checks=checks, n_pass=npass, n_checks=len(checks), runtime_s=round(time.time() - T0, 1), max_rss_GB=round(rss, 3))
log(f"  runtime {time.time() - T0:.1f} s, max RSS {rss:.3f} GB")
log(f"C5_HEALTH COMPLETE: {npass}/{len(checks)} checks PASS.")
with open(OUT, "w") as fh:
    fh.write("\n".join(lines) + "\n")
with open(JSON, "w") as fh:
    json.dump(res, fh, indent=1, default=str)
sys.exit(0 if npass == len(checks) else 1)
