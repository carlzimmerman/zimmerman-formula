#!/usr/bin/env python3
"""H4_v3_saddle_stability: is v3's khronon/dust pair healthy where the phantom density D.P < 0?

v3 (covariant_push_2026_10_22/THEORY_V3_DRAFT.md section 1; C5's Lagrangian at beta = eta = gamma_F = 0, xi = 1):
  L/sqrt(-g) = R/(4K) + P^mu A_mu - W(K|P|) - (gamma_L/2)(D.P)^2 + mu_K^2 (Q-1)^2/(2K),  K = 4 pi G,
  W'(u) = u a0/(K (a0 - u)), gamma_L = K L*^2/2, P orthogonal to n, n_mu = -d_mu tau/Q.
Weak-field PN form used (BS24's PN system with the J term replaced by C4's P sector; tau = t + sigma, c = 1):
  L = -|grad phi|^2/(2K) - rho_m phi + P.grad Xi - W(K|P|) - (gamma_L/2)(div P)^2 + mu_K^2 Xi^2/(2K),
  Xi = phi - sigma_t + |grad sigma|^2/2.
Frozen criteria: FROZEN_CRITERIA.md (b8860b6666, committed alone before any number) + ASSUMPTION_LEDGER.md;
AMENDMENT A1 (002b19eedc, POST-RESULT): execution history, C2 kept FAIL, C2b added.

Run: OMP_NUM_THREADS=1 nice -n 15 python3 h4_v3_saddle_stability.py     (H4_MUTATE=1: sign of the first-order term flipped)
kappa = 1/2 FITTED. Footings 9.36e-11 / 1.13e-10 m/s^2, never pooled. No dark-matter particle. Not "theory closed".
"""
import json
import math
import os
import resource
import sys
import time

if os.environ.get("PYTHONHASHSEED") != "0":      # determinism of sympy's simplification paths
    os.execve(sys.executable, [sys.executable] + sys.argv, dict(os.environ, PYTHONHASHSEED="0"))

import numpy as np
import scipy.sparse as sps
import scipy.sparse.linalg as spla

MUTATE = os.environ.get("H4_MUTATE", "0") == "1"
SGN = -1 if MUTATE else 1                      # sign of the first-order (background-gradient) term
TAG = "_MUTATE" if MUTATE else ""
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, f"h4_v3_saddle_stability{TAG}.out")
JSON = os.path.join(HERE, f"h4_v3_saddle_stability_results{TAG}.json")
P3JSON = os.path.join(HERE, "..", "P3_v3_strong_field", "p3_v3_strong_field_results.json")

# ------------------------------------------------------------------ constants (SI)
c_SI = 2.99792458e8
G_SI = 6.67430e-11
MSUN = 1.98847e30
GMSUN = 1.32712440018e20
PC = 3.0856775814913673e16
KPC = 1e3 * PC
MPC = 1e6 * PC
AU = 1.495978707e11
YR = 3.15576e7
GYR = 1e9 * YR
A0 = {"canonical": 9.36e-11, "alt": 1.13e-10}
LSTAR = {"canonical": [21.7, 24.0, 90.0], "alt": [22.9, 24.0, 90.0]}     # pc: D10 floor per footing, 24, 90
H0_SI = 68.6e3 / MPC
RHO_CRIT = 3 * H0_SI ** 2 / (8 * math.pi * G_SI)
RHO_K = 0.26 * RHO_CRIT                          # BS25's Omega_K via C4 (illustrative), native H0 upper end
F_DUST = (0, 3)
T_H = 13.8 * GYR
MSUN_PC3 = MSUN / PC ** 3

lines, checks = [], []
res = {"mutate": MUTATE, "sign_first_order_term": SGN}


def log(s=""):
    print(s, flush=True)
    lines.append(s)


def check(cid, ok, value, thr):
    ok = bool(ok)
    checks.append({"id": cid, "pass": ok, "value": str(value), "threshold": thr})
    log(f"{cid} {'PASS' if ok else 'FAIL'} {value} {thr}")
    return ok


# ====================================================================================================== AQUAL solver
def graded(lo, hi, keys, alpha):
    """nodes on [lo, hi], spacing h(s) = min_i(h_i + alpha |s - s_i|); key points are snapped onto nodes."""
    s = np.linspace(lo, hi, 400001)
    h = np.min([hk + alpha * np.abs(s - sk) for sk, hk in keys], axis=0)
    cum = np.concatenate([[0], np.cumsum(0.5 * (1 / h[1:] + 1 / h[:-1]) * np.diff(s))])
    n = max(int(np.ceil(cum[-1])), 8)
    nodes = np.interp(np.linspace(0, cum[-1], n + 1), cum, s)
    for sk, _ in keys:
        if lo <= sk <= hi:
            nodes[np.argmin(np.abs(nodes - sk))] = sk
    return np.unique(nodes)


class Grid:
    def __init__(self, R, z):
        self.R, self.z = R, z
        self.nr, self.nz = len(R), len(z)
        self.Rf = np.concatenate([[0.0], 0.5 * (R[1:] + R[:-1]), [R[-1]]])
        self.zf = np.concatenate([[z[0]], 0.5 * (z[1:] + z[:-1]), [z[-1]]])
        self.area_z = np.pi * (self.Rf[1:] ** 2 - self.Rf[:-1] ** 2)
        self.dz = self.zf[1:] - self.zf[:-1]
        self.V = self.area_z[:, None] * self.dz[None, :]
        self.RR, self.ZZ = np.meshgrid(R, z, indexing="ij")
        self.dR, self.dZ = np.diff(R), np.diff(z)


def node_grad(g, Phi):
    gR, gz = np.zeros_like(Phi), np.zeros_like(Phi)
    gR[1:-1] = (Phi[2:] - Phi[:-2]) / (g.R[2:] - g.R[:-2])[:, None]
    gR[-1] = (Phi[-1] - Phi[-2]) / g.dR[-1]
    gz[:, 1:-1] = (Phi[:, 2:] - Phi[:, :-2]) / (g.z[2:] - g.z[:-2])[None, :]
    gz[:, 0] = (Phi[:, 1] - Phi[:, 0]) / g.dZ[0]
    gz[:, -1] = (Phi[:, -1] - Phi[:, -2]) / g.dZ[-1]
    return gR, gz


def face_abs(g, Phi):
    gRn, gzn = node_grad(g, Phi)
    a = np.hypot((Phi[1:] - Phi[:-1]) / g.dR[:, None], 0.5 * (gzn[1:] + gzn[:-1]))
    b = np.hypot(0.5 * (gRn[:, 1:] + gRn[:, :-1]), (Phi[:, 1:] - Phi[:, :-1]) / g.dZ[None, :])
    return a, b


def operator(g, muR, muz):
    """(A Phi)_ij = outward flux of mu grad Phi through the control volume of node ij."""
    idx = np.arange(g.nr * g.nz).reshape(g.nr, g.nz)
    cR = 2 * np.pi * g.Rf[1:-1][:, None] * g.dz[None, :] * muR / g.dR[:, None]
    cz = g.area_z[:, None] * muz / g.dZ[None, :]
    rows, cols, vals = [], [], []
    for (a, b), c in (((idx[:-1].ravel(), idx[1:].ravel()), cR.ravel()),
                      ((idx[:, :-1].ravel(), idx[:, 1:].ravel()), cz.ravel())):
        rows += [a, a, b, b]
        cols += [b, a, a, b]
        vals += [c, -c, c, -c]
    return sps.coo_matrix((np.concatenate(vals), (np.concatenate(rows), np.concatenate(cols))),
                          shape=(g.nr * g.nz,) * 2).tocsr()


def bmask(g):
    m = np.zeros((g.nr, g.nz), bool)
    m[-1, :] = m[:, 0] = m[:, -1] = True
    return m


def mu_deep(x):
    return x


def mu_std(x):
    return x / (1 + x)


def aqual_solve(g, mass, a0h, mufun, bcfun, itmax=300, tol_res=1e-8, damp=0.5):
    bm = bmask(g)
    inner = ~bm.ravel()
    Phi = bcfun(g.RR, g.ZZ).copy()
    rhs_full = 4 * np.pi * mass.ravel()
    muR = muz = None
    rnorm = np.max(np.abs(rhs_full))
    for it in range(itmax):
        aR, az = face_abs(g, Phi)
        nR, nZ = mufun(aR / a0h), mufun(az / a0h)
        rr_ = (operator(g, nR, nZ) @ Phi.ravel() - rhs_full)[inner]      # nonlinear residual with the undamped mu
        if it >= 3 and np.max(np.abs(rr_)) / rnorm < tol_res:
            break
        muR = nR if muR is None else muR ** (1 - damp) * nR ** damp
        muz = nZ if muz is None else muz ** (1 - damp) * nZ ** damp
        muR, muz = np.maximum(muR, 1e-14), np.maximum(muz, 1e-14)
        A = operator(g, muR, muz)
        Ai = A[inner]
        rhs = rhs_full[inner] - Ai[:, ~inner] @ Phi.ravel()[~inner]
        sol = spla.spsolve(Ai[:, inner].tocsc(), rhs, permc_spec="MMD_AT_PLUS_A")
        new = Phi.ravel().copy()
        new[inner] = sol
        new = new.reshape(Phi.shape)
        dmax = np.max(np.abs(new - Phi)) / (np.max(np.abs(new)) + 1e-300)
        Phi = new
    aR, az = face_abs(g, Phi)
    A = operator(g, mufun(aR / a0h), mufun(az / a0h))
    r = (A @ Phi.ravel() - rhs_full).reshape(Phi.shape)
    return Phi, {"iters": it + 1, "last_change": float(dmax),
                 "residual_rel": float(np.max(np.abs(r[~bm])) / np.max(np.abs(rhs_full)))}


def phantom(g, Phi, mass):
    A = operator(g, np.ones((g.nr - 1, g.nz)), np.ones((g.nr, g.nz - 1)))
    rho = (A @ Phi.ravel()).reshape(Phi.shape) / g.V / (4 * np.pi) - mass / g.V
    rho[bmask(g)] = np.nan
    return rho


def plummer(g, M, zc, b):
    r2 = g.RR ** 2 + (g.ZZ - zc) ** 2
    m = 3 * M / (4 * np.pi * b ** 3) * (1 + r2 / b ** 2) ** -2.5 * g.V
    return m * (M / m.sum())


def disc(g, M, hz):
    ez = np.exp(-2 * np.abs(g.ZZ) / hz)
    m = M / (4 * np.pi * hz) * np.exp(-g.RR) * 4 * ez / (1 + ez) ** 2 * g.V      # R_d = 1 units, sech^2 vertical
    return m * (M / m.sum())


def phi_sph(r, M, a0h):
    """spherical potential of a point mass with mu = x/(1+x) (exact law), up to a constant; G = 1."""
    lg = np.logspace(np.log10(max(np.min(r), 1e-8)), np.log10(np.max(r)), 6000)
    gN = M / lg ** 2
    gg = 0.5 * gN * (1 + np.sqrt(1 + 4 * a0h / gN))
    cum = np.concatenate([[0], np.cumsum(0.5 * (gg[1:] + gg[:-1]) * np.diff(lg))])
    return np.interp(r, lg, cum) - np.interp(np.max(r), lg, cum)      # zero at the box: keeps Phi O(1)


def bc_factory(Mtot, zc, a0h, eh, deep):
    """outer Dirichlet data: isolated -> spherical law of the total mass about zc; external field eh (units a0h) along z ->
    linearised AQUAL far field Phi = g_e z - M/(mu_e sqrt(1+L_e) sqrt(R^2 + (z-zc)^2/(1+L_e)))."""
    if eh == 0:
        if deep:
            return lambda RR, ZZ: math.sqrt(Mtot * a0h) * 0.5 * np.log(RR ** 2 + (ZZ - zc) ** 2 + 1e-8)
        return lambda RR, ZZ: phi_sph(np.sqrt(RR ** 2 + (ZZ - zc) ** 2 + 1e-4), Mtot, a0h)   # softened start guess
    ge = eh * a0h
    mue, Le = (eh, 1.0) if deep else (eh / (1 + eh), 1 / (1 + eh))
    return lambda RR, ZZ: ge * ZZ - Mtot / (mue * math.sqrt(1 + Le) * np.sqrt(RR ** 2 + (ZZ - zc) ** 2 / (1 + Le) + 1e-12))


LEVELS = {"base": (1.0, 0.08), "fine": (0.7, 0.055), "xfine": (0.5, 0.042)}      # (spacing scale, growth rate)


def build_case(spec, level, null_z=None):
    s, alpha = LEVELS[level]
    box = spec["box"]
    if spec["kind"] == "disc":
        R = graded(0, box, [(0, 0.03 * s), (1, 0.05 * s)], alpha)
        z = graded(-box, box, [(0, spec["hz"] / 6 * s)], alpha)
    else:
        zk = [(zc, min(b / 4, 0.004) * s) for (_, zc, b) in spec["masses"]]
        if len(spec["masses"]) == 2:
            zk.append((0.0, 0.0025 * s))
        for nz_ in (null_z or []):           # a null's structure scales with its distance from the masses
            if all(abs(nz_ - zk_[0]) > 1e-9 for zk_ in zk):
                zk.append((nz_, 0.0025 * s * max(1.0, abs(nz_ - spec["zc"]))))
        R = graded(0, box, [(0, 0.0025 * s), (0.2, 0.0025 * s)], alpha)
        z = graded(-box, box, zk, alpha)
    g = Grid(R, z)
    if spec["kind"] == "disc":
        mass = disc(g, 1.0, spec["hz"])
        if spec.get("bulge"):
            mass = mass + plummer(g, spec["bulge"][0], 0.0, spec["bulge"][1])
    else:
        mass = sum(plummer(g, M, zc, b) for (M, zc, b) in spec["masses"])
    return g, mass


def run_case(spec):
    """worker (own process): solve base and fine levels; returns arrays of the fine level and convergence numbers."""
    os.environ["OMP_NUM_THREADS"] = "1"
    t0 = time.time()
    out = {"name": spec["name"], "levels": {}}
    mufun = mu_deep if spec["deep"] else mu_std
    null_z = None
    for level in ("base", "fine"):
        g, mass = build_case(spec, level, null_z)
        bc = bc_factory(spec["Mtot"], spec["zc"], spec["a0h"], spec["eh"], spec["deep"])
        Phi, info = aqual_solve(g, mass, spec["a0h"], mufun, bc)
        rho = phantom(g, Phi, mass)
        gR, gz = node_grad(g, Phi)
        gabs = np.hypot(gR, gz)
        if level == "base" and spec["kind"] == "pair" and (len(spec["masses"]) == 2 or spec["eh"] > 0):
            # on-axis nulls: local minima of |g| along the axis, away from the mass cores and the outer boundary
            ok_ = np.abs(g.z - spec["zc"]) < 30.0
            ok_[:3] = ok_[-3:] = False
            for (_, zc, b) in spec["masses"]:
                ok_ &= np.abs(g.z - zc) > 3 * b
            ga = gabs[0]
            lm = np.zeros(g.nz, bool)
            lm[1:-1] = (ga[1:-1] <= ga[:-2]) & (ga[1:-1] <= ga[2:])
            cand = np.where(lm & ok_)[0]
            null_z = sorted(float(g.z[j]) for j in cand[np.argsort(ga[cand])][:4])
        out["levels"][level] = {"g": g, "rho": rho, "gabs": gabs, "mass": mass, "info": info,
                                "nr": g.nr, "nz": g.nz}
    out["null_z"] = null_z
    out["rss_GB"] = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / (1024 ** 3 if sys.platform == "darwin" else 1024 ** 2)
    out["time_s"] = time.time() - t0
    for lv in out["levels"].values():         # make picklable: replace Grid by arrays
        g = lv.pop("g")
        lv.update({"R": g.R, "z": g.z, "V": g.V, "RR": g.RR, "ZZ": g.ZZ})
    return out


def run_level(spec, level, null_z):
    """worker (own process): one level with given null keys (A1's C2b extra-fine check)."""
    t0 = time.time()
    g, mass = build_case(spec, level, null_z)
    Phi, info = aqual_solve(g, mass, spec["a0h"], mu_deep if spec["deep"] else mu_std,
                            bc_factory(spec["Mtot"], spec["zc"], spec["a0h"], spec["eh"], spec["deep"]))
    gR, gz = node_grad(g, Phi)
    return {"rho": phantom(g, Phi, mass), "gabs": np.hypot(gR, gz), "info": info, "nr": g.nr, "nz": g.nz,
            "R": g.R, "z": g.z, "V": g.V, "RR": g.RR, "ZZ": g.ZZ, "time_s": time.time() - t0,
            "rss_GB": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / (1024 ** 3 if sys.platform == "darwin" else 1024 ** 2)}


# ====================================================================================================== main
def main():
    import sympy as sp
    from sympy.calculus.euler import euler_equations
    import concurrent.futures as cf
    import multiprocessing as mp
    T0 = time.time()
    log("H4_v3_saddle_stability: khronon/dust pair where the phantom density D.P < 0")
    log(f"mutate = {MUTATE} (sign of the first-order term = {SGN}); kappa = 1/2 FITTED; footings never pooled")

    def el_zero(expr, funcs, xs):
        eqs = euler_equations(expr, funcs, xs)            # sympy drops identically satisfied equations
        return [sp.simplify(e.lhs - e.rhs) for e in eqs if sp.simplify(e.lhs - e.rhs) != 0]

    # ================================================================================================ PART A
    log("")
    log("A: derivation (sympy)")
    t, x, y, z = X = sp.symbols("t x y z", real=True)
    K, gL, muK, a0s = sp.symbols("K gamma_L mu_K a_0", positive=True)
    phi = sp.Function("phi")(*X)
    sig = sp.Function("sigma")(*X)
    Pf = [sp.Function(f"P{i}")(*X) for i in range(3)]
    rhom = sp.Function("rho_m")(x, y, z)
    Wf = sp.Function("W")
    xs = (x, y, z)
    grad = lambda f: [sp.diff(f, v) for v in xs]
    div = lambda F: sum(sp.diff(F[i], xs[i]) for i in range(3))
    Xi = phi - sp.diff(sig, t) + sum(d ** 2 for d in grad(sig)) / 2
    modP = sp.sqrt(sum(p ** 2 for p in Pf))
    Lpn = (-sum(d ** 2 for d in grad(phi)) / (2 * K) - rhom * phi + sum(Pf[i] * sp.diff(Xi, xs[i]) for i in range(3))
           - Wf(K * modP) - gL / 2 * div(Pf) ** 2 + muK ** 2 * Xi ** 2 / (2 * K))
    eqs = euler_equations(Lpn, [phi, sig] + Pf, X)
    rho_tau = div(Pf) - muK ** 2 * Xi / K
    vtau = [-d for d in grad(sig)]
    cont = sp.diff(rho_tau, t) + div([rho_tau * vtau[i] for i in range(3)])
    r_sig = sp.simplify(sp.expand(eqs[1].lhs + cont))
    r_phi = sp.simplify(sp.expand(eqs[0].lhs - (sum(sp.diff(phi, v, 2) for v in xs) / K - rhom - rho_tau)))
    # (ii) static, gamma_L = 0: P from dL/dP = 0 -> |grad phi| = K W'(u); with the capped W: u = g a0/(a0 + g)
    gg_, uu = sp.symbols("g u", positive=True)
    KWp = uu * a0s / (a0s - uu)                                   # K W'(u)
    usol = sp.solve(sp.Eq(KWp, gg_), uu)[0]
    xg = gg_ / a0s
    mu_from_P = sp.simplify((gg_ - usol) / gg_)                   # grad phi - K P = mu grad phi
    r_mu = sp.simplify(mu_from_P - xg / (1 + xg))
    log(f"  A1: sigma-EL + [d_t rho_tau + div(rho_tau v_tau)] = {r_sig}; phi-EL - [lap phi/K - rho_m - rho_tau] = {r_phi};"
        f" static P elimination: mu = {mu_from_P}, minus x/(1+x) = {r_mu}")
    check("A1", r_sig == 0 and r_phi == 0 and r_mu == 0,
          f"continuity identity residual {r_sig}; Poisson residual {r_phi}; AQUAL mu residual {r_mu}",
          "all identically 0")
    res["A1"] = {"continuity_residual": str(r_sig), "poisson_residual": str(r_phi), "mu": str(mu_from_P)}

    # A2: covariant leaf divergence on Minkowski with tau = t + eps sigma, P orthogonal to n
    ep = sp.Symbol("epsilon")
    s_ = sp.Function("sigma")(*X)
    P0 = [sp.Function(f"P0{i}")(x, y, z) for i in range(3)]
    pp = [sp.Function(f"p{i}")(*X) for i in range(3)]
    eta = [-1, 1, 1, 1]
    dtau = [sp.diff(t + ep * s_, v) for v in X]
    Q = sp.sqrt(-sum(eta[m] * dtau[m] ** 2 for m in range(4)))
    n_lo = [-d / Q for d in dtau]
    n_up = [eta[m] * n_lo[m] for m in range(4)]
    Ps = [P0[i] + ep * pp[i] for i in range(3)]
    P_0 = sum(n_up[i + 1] * Ps[i] for i in range(3)) / (-n_up[0])
    P_lo = [P_0] + Ps
    P_up = [eta[m] * P_lo[m] for m in range(4)]
    A_lo = [sum(n_up[m] * sp.diff(n_lo[nu], X[m]) for m in range(4)) for nu in range(4)]
    DP = sum((eta[m] * (1 if m == nn else 0) + n_up[m] * n_up[nn]) * sp.diff(P_lo[nn], X[m])
             for m in range(4) for nn in range(4))
    divP4 = sum(eta[m] * sp.diff(P_lo[m], X[m]) for m in range(4))
    PA = sum(P_up[m] * A_lo[m] for m in range(4))
    ident = [sp.simplify(sp.expand(sp.diff(DP - (divP4 - PA), ep, o).subs(ep, 0))) for o in range(3)]
    DP1 = sp.simplify(sp.expand(sp.diff(DP, ep).subs(ep, 0)))
    tilt_res = sp.simplify(DP1 - sum(sp.diff(pp[i], xs[i]) for i in range(3)))
    tilt_term = sp.simplify(sp.expand(sp.diff(divP4, ep).subs(ep, 0) - sum(sp.diff(pp[i], xs[i]) for i in range(3))))
    log(f"  A2: D.P - (div4 P - P.A) at O(eps^0,1,2) = {ident}; tilt term of div4 P at O(eps): {tilt_term}; "
        f"O(eps) of D.P minus div p = {tilt_res}")
    check("A2", all(v == 0 for v in ident) and tilt_res == 0 and tilt_term != 0,
          f"identity residuals {ident}; O(eps) D.P has no sigma term (residual {tilt_res}); the cancelled tilt term "
          f"is {tilt_term}", "identity 0; sigma-free O(eps) leaf divergence")
    res["A2"] = {"identity": [str(v) for v in ident], "tilt_term": str(tilt_term), "DP1": str(DP1)}

    # A3: plane-symmetric decoupling, P0_z(z), sigma(t,z), p(t,z)
    tz = (t, z)
    s1 = sp.Function("sigma")(t, z)
    P0z = sp.Function("P0")(z)
    p1 = sp.Function("p")(t, z)
    dtau2 = [sp.diff(t + ep * s1, v) for v in tz]
    Q2 = sp.sqrt(dtau2[0] ** 2 - dtau2[1] ** 2)
    nl = [-d / Q2 for d in dtau2]
    nu_ = [-nl[0], nl[1]]
    Pz = P0z + ep * p1
    Pt = nu_[1] * Pz / (-nu_[0])
    Pu = [-Pt, Pz]
    Al = [sum(nu_[m] * sp.diff(nl[k_], tz[m]) for m in range(2)) for k_ in range(2)]
    PA2 = sp.expand(sp.diff(sum(Pu[m] * Al[m] for m in range(2)), ep, 2).subs(ep, 0) / 2)
    ss = PA2.subs(p1, 0).doit()
    cross = sp.expand(PA2 - ss)
    r_ss = el_zero(ss + sp.Rational(1, 2) * sp.diff(P0z, z) * sp.diff(s1, z) ** 2, [s1, p1], tz)
    r_cr = el_zero(cross + p1 * sp.diff(s1, t, z), [s1, p1], tz)
    modP2 = sp.simplify(sp.expand(sp.diff(Pz ** 2 - Pt ** 2, ep, 2).subs(ep, 0) / 2))
    # integrate p out (leading WKB): L = -p sigma_tz - (1/2)(K M + gamma_L k^2) p^2 -> (1/2) chi |sigma_t|^2
    kk, ww, MM = sp.symbols("k omega M", positive=True)
    pv = sp.Symbol("pv")
    Lf = -pv * (kk * ww) - (K * MM + gL * kk ** 2) * pv ** 2 / 2       # sigma_tz -> k omega |sigma| (amplitudes)
    psol = sp.solve(sp.diff(Lf, pv), pv)[0]
    chi_kin = sp.simplify(Lf.subs(pv, psol) * 2 / ww ** 2)
    r_chi = sp.simplify(chi_kin - kk ** 2 / (K * MM + gL * kk ** 2))
    log(f"  A3: O(eps^2) of P.A = {PA2}")
    log(f"      Euler operator of [sigma-sigma part + (1/2) P0' sigma_z^2] = {r_ss}; of [cross part + p sigma_tz] = {r_cr}; "
        f"|P|^2 at O(eps^2) = {modP2} (the W tilt term, PN order); chi from integrating p out minus k^2/(K M + gL k^2) = {r_chi}")
    check("A3", r_ss == [] and r_cr == [] and r_chi == 0,
          f"sigma-sigma part = -(1/2)(d_z P0_z) sigma_z^2 + total derivative ({r_ss}); cross = -p sigma_tz ({r_cr}); "
          f"chi residual {r_chi}", "identically 0 (Euler operator)")
    res["A3"] = {"PA_eps2": str(PA2), "modP2_eps2": str(modP2), "chi": str(chi_kin)}

    # A4: PN linear system with the anisotropic W Hessian, background moving at V (A6 uses kV != 0)
    k, om, r0, th, ML, MT = sp.symbols("k omega rho_0 theta M_L M_T", positive=True)
    kV = sp.Symbol("kV", real=True)
    dphi, dsig, dXi, drho = sp.symbols("dphi dsigma dXi drho")
    dP = sp.symbols("dP0:3")
    kh = sp.Matrix([0, 0, 1])
    Ph = sp.Matrix([sp.sin(th), 0, sp.cos(th)])
    Hm = K * (MT * sp.eye(3) + (ML - MT) * Ph * Ph.T)
    dPv = sp.Matrix(dP)
    W2 = sp.Symbol("W2")

    def dispersion(kVv, poisson=True, sgn=SGN, cont_eq=None, bern_eq=None):
        Peq = sp.I * k * kh * dXi - gL * k ** 2 * kh * (kh.dot(dPv)) - Hm * dPv
        ce = cont_eq if cont_eq is not None else -sp.I * (om - kVv) * drho + sgn * r0 * k ** 2 * dsig
        be = bern_eq if bern_eq is not None else dXi - (dphi + sp.I * (om - kVv) * dsig)
        eqs_ = [(-k ** 2 * dphi - K * drho) if poisson else dphi,
                drho - (sp.I * k * kh.dot(dPv) - muK ** 2 * dXi / K), ce, be] + list(Peq)
        Msys = sp.linear_eq_to_matrix(eqs_, [dphi, dsig, dXi, drho] + list(dP))[0]
        det = sp.factor(sp.simplify(Msys.det()))
        return sp.solve(sp.Eq(det.subs(om, kVv + sp.sqrt(W2)), 0), W2)

    Mth = 1 / (sp.cos(th) ** 2 / ML + sp.sin(th) ** 2 / MT)
    chi = k ** 2 / (K * Mth + gL * k ** 2) + muK ** 2 / K
    w2_expected = r0 * (k ** 2 / chi - K)
    sol = dispersion(0)
    r_a4 = sp.simplify(sol[0] - w2_expected) if len(sol) == 1 else "no unique root"
    fth = 1 - 1 / Mth
    bsk1 = K * r0 * (k ** 2 * fth - muK ** 2) / (k ** 2 * (1 - fth) + muK ** 2)
    r_bsk1 = sp.simplify(sol[0].subs(gL, 0) - bsk1) if len(sol) == 1 else "n/a"
    sol_dec = dispersion(0, poisson=False)
    r_p3 = sp.simplify(sol_dec[0] - r0 * k ** 2 / chi) if len(sol_dec) == 1 else "n/a"
    r_mu0 = sp.simplify(w2_expected.subs(muK, 0) - K * r0 * (Mth - 1 + gL * k ** 2 / K))
    log(f"  A4: derived omega^2 = {sp.simplify(sol[0]) if len(sol) == 1 else sol}")
    log(f"      minus rho_tau (k^2/chi - K): {r_a4}; gamma_L = 0 minus BSK1 M4: {r_bsk1}; no-Poisson minus P3's "
        f"rho_tau k^2/chi: {r_p3}; mu_K = 0 form K rho_tau (M_theta - 1 + gamma_L k^2/K): {r_mu0}")
    check("A4", r_a4 == 0 and r_bsk1 == 0 and r_p3 == 0,
          f"dispersion residual {r_a4}; BSK1 limit residual {r_bsk1}; P3 decoupled limit residual {r_p3}",
          "all identically 0")
    res["A4"] = {"omega2": str(sol), "residual": str(r_a4), "bsk1_residual": str(r_bsk1), "p3_residual": str(r_p3),
                 "dispersion": "omega^2 = rho_tau [k^2/chi(k) - K], chi = k^2/(K M_theta + gamma_L k^2) + mu_K^2/K; "
                               "mu_K = 0: omega^2 = K rho_tau (M_theta - 1 + L*^2 k^2/2)"}

    # A5: J_x masses
    xx = sp.Symbol("x", positive=True)
    muX = xx / (1 + xx)
    fL = sp.diff(xx * muX, xx)
    MT_u = sp.simplify((KWp / uu).subs(uu, usol).subs(gg_, xx * a0s))
    ML_u = sp.simplify(sp.diff(KWp, uu).subs(uu, usol).subs(gg_, xx * a0s))
    r_a5 = [sp.simplify(1 - muX - 1 / (1 + xx)), sp.simplify(1 - fL - 1 / (1 + xx) ** 2),
            sp.simplify(MT_u - (1 + xx)), sp.simplify(ML_u - (1 + xx) ** 2)]
    log(f"  A5: 1-mu - 1/(1+x) = {r_a5[0]}; 1-f_L - 1/(1+x)^2 = {r_a5[1]}; M_T from W = {MT_u}; M_L from W = {ML_u}")
    check("A5", all(v == 0 for v in r_a5), f"residuals {r_a5}", "all 0: M_T = 1+x, M_L = (1+x)^2")

    # A6: boost, linearised from the nonlinear Bernoulli and continuity expressions about sigma0 = -V z + V^2 t/2
    Vs = sp.Symbol("V", real=True)
    Ab, Fb, Bb = sp.symbols("A_s F_p B_r")
    sigf = sp.Function("s")(t, z)
    phf = sp.Function("f")(t, z)
    rhf = sp.Function("q")(t, z)
    Xi_nl = phf - sp.diff(sigf, t) + sp.diff(sigf, z) ** 2 / 2
    cont_nl = sp.diff(rhf, t) + sp.diff(rhf * (-sp.diff(sigf, z)), z)
    ph_ = sp.exp(sp.I * (k * z - om * t))
    sub = {sigf: -Vs * z + Vs ** 2 * t / 2 + ep * Ab * ph_, phf: ep * Fb * ph_, rhf: r0 + ep * Bb * ph_}
    lin = lambda e: sp.simplify(sp.diff(e.subs(sub).doit(), ep).subs(ep, 0) / ph_)
    Xi_lin = lin(Xi_nl)
    cont_lin = lin(cont_nl)
    be = dXi - Xi_lin.subs({Ab: dsig, Fb: dphi})
    ce = (cont_lin.subs({Ab: dsig, Bb: drho}))
    ce = sp.expand(ce)
    if SGN < 0:   # flip the first-order (rho_0) term in the mutated run
        ce = ce.subs(r0, -r0)
    sol6 = dispersion(k * Vs, cont_eq=ce, bern_eq=be)
    r_a6 = sp.simplify(sol6[0] - w2_expected) if len(sol6) == 1 else "n/a"
    log(f"  A6: linearised Bernoulli dXi = {Xi_lin}; continuity {cont_lin}; (omega - kV)^2 minus rho_tau(k^2/chi - K) = {r_a6}")
    check("A6", r_a6 == 0, f"boosted dispersion residual {r_a6}", "0: (omega - k.V)^2 = rho_tau (k^2/chi - K)")

    # ================================================================================================ PART B
    log("")
    log("B: well-posedness")
    w2 = sol[0]
    lim_uv = sp.simplify(sp.limit(w2 / k ** 2, k, sp.oo))
    lim_b = sp.simplify(sp.limit(w2.subs(gL, 0), k, sp.oo))
    exp_uv = SGN * gL * K * r0 / (K + gL * muK ** 2)
    log(f"  B1: lim omega^2/k^2 (k -> inf) = {lim_uv}; gamma_L = 0: lim omega^2 = {lim_b}")
    ok_b1 = (sp.simplify(lim_uv - exp_uv) == 0) and lim_b.is_finite is not False and not lim_b.has(sp.oo)
    check("B1", ok_b1 and lim_uv != 0,
          f"UV: omega^2 -> ({lim_uv}) k^2 (Gamma proportional to k where SGN*rho_tau < 0: UV-unbounded); gamma_L = 0: "
          f"omega^2 -> {lim_b} (finite: bounded)", "both limits derived; UV coefficient gamma_L rho_tau/(1 + mu^2 gL/K)")
    res["B1"] = {"uv_coefficient": str(lim_uv), "bounded_limit_gammaL0": str(lim_b)}

    def gmax(N, gLv, Kv=1.0, M=2.0, rbar=-0.5, amp=1.0):
        n = np.arange(-N // 2, N // 2 + 1)
        n = n[n != 0]
        kn = 2 * np.pi * n
        a = (Kv * (M - 1) + gLv * kn ** 2) / kn ** 2
        dn = n[:, None] - n[None, :]
        rh = np.where(dn == 0, rbar, np.where(np.abs(dn) == 1, amp / 2, 0.0))
        w = np.sqrt(a) * kn
        ev = np.linalg.eigvalsh(-SGN * w[:, None] * rh * w[None, :])
        return math.sqrt(max(ev.max(), 0.0))

    ladder = {}
    for gLv in (1e-3, 0.0):
        ladder[str(gLv)] = [gmax(N, gLv) for N in (64, 128, 256, 512)]
    g1, g0 = ladder["0.001"], ladder["0.0"]
    pred = math.sqrt(1.0 * (2.0 - 1) * 1.5)
    r_grow = g1[3] / g1[2]
    r_conv = g0[3] / g0[2]
    log(f"  B2: Gamma_max ladder N = 64..512: gamma_L = 1e-3: {[round(v, 4) for v in g1]}; gamma_L = 0: "
        f"{[round(v, 6) for v in g0]}; bounded prediction sqrt(K(M-1)|min rho|) = {pred:.6f}")
    check("B2", 1.8 <= r_grow <= 2.2 and r_conv <= 1.01 and abs(g0[3] / pred - 1) <= 0.01,
          f"gamma_L > 0: Gamma(512)/Gamma(256) = {r_grow:.4f}; gamma_L = 0: ratio {r_conv:.6f}, "
          f"Gamma(512)/prediction = {g0[3] / pred:.6f}", "[1.8, 2.2]; <= 1.01 and within 1%")
    res["B2"] = {"ladder": ladder, "prediction_bounded": pred}

    # B3: P3's E4 rows
    p3 = json.load(open(P3JSON))
    BHM = {"BH10": 10.0, "BH63": 63.0, "SgrA*": 4.3e6, "M87*": 6.5e9}
    rows_scored, rows_report = [], []
    for key, row in p3["E4"].items():
        if row.get("c_pi") is None:
            continue
        sname, foot, Lp = key.split("|")
        if sname.startswith("Eot"):
            kk_ = 1 / 38.6e-6
        elif sname.startswith("planets"):
            kk_ = 1 / AU
        elif sname.startswith("double"):
            kk_ = 1 / 8.79e8
        elif sname.startswith("galaxy"):
            kk_ = 1 / KPC
        elif sname.startswith("cosmology"):
            kk_ = 10 * 0.675 / MPC
        elif sname.startswith("NS"):
            kk_ = 1 / (p3["NS"][f"1.4|{foot}|{Lp}"]["R_km"] * 1e3)
        else:
            kk_ = 1 / (G_SI * BHM[sname.split(" ")[0]] * MSUN / c_SI ** 2)
        Gh, Zh = row["G_hat"], row["Z_hat"]
        c2 = SGN * (Gh / Zh - Gh / kk_ ** 2)
        cmine = math.sqrt(c2) if c2 > 0 else float("nan")
        rec = {"row": key, "c_pi_P3": row["c_pi"], "c_pi_H4": cmine, "Z_hat_over_k2": Zh / kk_ ** 2}
        (rows_scored if Zh / kk_ ** 2 <= 1e-3 else rows_report).append(rec)
    dev = [abs(r_["c_pi_H4"] / r_["c_pi_P3"] - 1) if np.isfinite(r_["c_pi_H4"]) else float("inf") for r_ in rows_scored]
    for r_ in rows_report:
        r_["correction_factor"] = math.sqrt(1 - r_["Z_hat_over_k2"]) if r_["Z_hat_over_k2"] < 1 else "Jeans branch"
    log(f"  B3: {len(rows_scored)} scored P3 rows, max |c_pi(H4)/c_pi(P3) - 1| = {max(dev):.3e}; reported rows: " +
        "; ".join(f"{r_['row']}: {r_['correction_factor'] if isinstance(r_['correction_factor'], str) else round(r_['correction_factor'], 4)}"
                  for r_ in rows_report if "canonical|24" in r_["row"]))
    check("B3", len(rows_scored) > 0 and max(dev) <= 1e-3,
          f"{len(rows_scored)} rows (lab, planets, double pulsar, BH, NS; both footings, all L*): max dev {max(dev):.3e}",
          "<= 1e-3 (P3's D.P > 0 speeds reproduced)")
    res["B3"] = {"scored": rows_scored, "reported": rows_report}
    log(f"A, B done ({time.time() - T0:.1f} s)")

    # ================================================================================================ PART C
    log("")
    log("C: where rho_tau < 0 (own axisymmetric AQUAL solver, mu = x/(1+x); validation in deep units G = M = d = a0 = 1)")
    specs = []
    # validation cases (deep)
    specs.append({"name": "V_single", "kind": "pair", "deep": True, "masses": [(1.0, 0.0, 0.003)], "Mtot": 1.0,
                  "zc": 0.0, "a0h": 1.0, "eh": 0.0, "box": 20.0})
    specs.append({"name": "V_pair", "kind": "pair", "deep": True, "masses": [(1.0, 0.5, 0.01), (1.0, -0.5, 0.01)],
                  "Mtot": 2.0, "zc": 0.0, "a0h": 1.0, "eh": 0.0, "box": 30.0})
    for e_ in (0.3, 0.68):
        specs.append({"name": f"V_efe{e_}", "kind": "pair", "deep": True, "masses": [(1.0, 0.5, 0.01), (1.0, -0.5, 0.01)],
                      "Mtot": 2.0, "zc": 0.0, "a0h": 1.0, "eh": e_, "box": 60.0})
    # declared systems
    SYS = {
        "S1_MW-M31": {"L": 780 * KPC, "Mu": 6.0e10, "m": [(1.0, 0.5, 3.0), (1.0e11 / 6.0e10, -0.5, 4.0)], "e": (0, 0.01),
                      "v": 110e3},
        "S2_LMC-MW": {"L": 50 * KPC, "Mu": 6.0e10, "m": [(1.0, 0.5, 3.0), (3.0e9 / 6.0e10, -0.5, 1.5)], "e": (0,),
                      "v": 320e3},
        "S3_galaxy_pair": {"L": 300 * KPC, "Mu": 5.0e10, "m": [(1.0, 0.5, 3.0), (1.0, -0.5, 3.0)], "e": (0, 0.01),
                           "v": 150e3},
        "S4_cluster_pair": {"L": 3 * MPC, "Mu": 1.5e14, "m": [(1.0, 0.5, 300.0), (1.0e14 / 1.5e14, -0.5, 250.0)],
                            "e": (0, 0.01), "v": 1000e3},
        "S6_single_in_field": {"L": 100 * KPC, "Mu": 6.0e10, "m": [(1.0, 0.0, 3.0)], "e": (0.01,), "v": None},
    }
    DISCS = {"S5a_MW_disc": {"Rd": 2.6, "Md": 5e10, "hz": 0.3, "bulge": (1e10, 0.6)},
             "S5b_dwarf_disc": {"Rd": 1.5, "Md": 1e9, "hz": 0.2, "bulge": None}}
    meta = {}
    for foot, a0 in A0.items():
        for sname, S in SYS.items():
            a0h = a0 * S["L"] ** 2 / (G_SI * S["Mu"] * MSUN)
            masses = [(M, zc, b * PC * 1e3 / S["L"]) for (M, zc, b) in S["m"]]
            Mtot = sum(M for M, _, _ in masses)
            zc = sum(M * z_ for M, z_, _ in masses) / Mtot
            for e_ in S["e"]:
                re = math.sqrt(Mtot * a0h) / (e_ * a0h) if e_ > 0 else 0.0
                box = 60.0 if e_ == 0 else max(60.0, 15 * re)
                nm = f"{sname}|{foot}|e{e_}"
                specs.append({"name": nm, "kind": "pair", "deep": False, "masses": masses, "Mtot": Mtot, "zc": zc,
                              "a0h": a0h, "eh": e_, "box": box})
                meta[nm] = {"L_m": S["L"], "Mu_kg": S["Mu"] * MSUN, "a0": a0, "a0h": a0h, "foot": foot, "e": e_,
                            "v": S["v"], "r_e": re, "system": sname, "zc": zc,
                            "near_r": (3 * re if e_ > 0 else 2.0) if sname.startswith("S6") or e_ == 0 else max(2.0, 3 * re)}
        for dname, D in DISCS.items():
            L = D["Rd"] * KPC
            a0h = a0 * L ** 2 / (G_SI * D["Md"] * MSUN)
            bulge = (D["bulge"][0] / D["Md"], D["bulge"][1] / D["Rd"]) if D["bulge"] else None
            Mtot = 1.0 + (bulge[0] if bulge else 0.0)
            for e_ in (0, 0.01):
                re = math.sqrt(Mtot * a0h) / (e_ * a0h) if e_ > 0 else 0.0
                box = 200.0 if e_ == 0 else max(200.0, 15 * re)
                nm = f"{dname}|{foot}|e{e_}"
                specs.append({"name": nm, "kind": "disc", "deep": False, "hz": D["hz"] / D["Rd"], "bulge": bulge,
                              "Mtot": Mtot, "zc": 0.0, "a0h": a0h, "eh": e_, "box": box})
                meta[nm] = {"L_m": L, "Mu_kg": D["Md"] * MSUN, "a0": a0, "a0h": a0h, "foot": foot, "e": e_, "v": None,
                            "r_e": re, "system": dname, "zc": 0.0, "near_r": 50.0 if e_ == 0 else 3 * re}
    results = {}
    ctx = mp.get_context("spawn")
    with cf.ProcessPoolExecutor(max_workers=1, mp_context=ctx, max_tasks_per_child=1) as ex:
        for sp_ in specs:
            r_ = ex.submit(run_case, sp_).result()
            results[sp_["name"]] = r_
            lv = r_["levels"]["fine"]
            log(f"  solved {sp_['name']:38s} grid {lv['nr']}x{lv['nz']} iters {lv['info']['iters']} residual "
                f"{lv['info']['residual_rel']:.1e} box {sp_['box']:.0f} nulls {[round(v, 3) for v in (r_['null_z'] or [])]} "
                f"({r_['time_s']:.0f} s, child RSS {r_['rss_GB']:.2f} GB)")

    # ---- C1 validation
    def interp_mid(lv, R0=0.2, z0=0.0):
        j = np.argmin(np.abs(lv["z"] - z0))
        return float(np.interp(R0, lv["R"], lv["rho"][:, j]))

    lv = results["V_single"]["levels"]["fine"]
    rr = np.sqrt(lv["RR"] ** 2 + lv["ZZ"] ** 2)
    sel = (rr > 0.2) & (rr < 2) & np.isfinite(lv["rho"])
    q = 4 * np.pi * rr[sel] ** 2 * lv["rho"][sel]
    c1i = float(np.max(np.abs(q - 1)))
    cpair = {lvn: interp_mid(results["V_pair"]["levels"][lvn]) for lvn in ("base", "fine")}
    cefe = {e_: interp_mid(results[f"V_efe{e_}"]["levels"]["fine"]) for e_ in (0.3, 0.68)}
    log(f"  C1: single lens max|4 pi r^2 rho - 1| = {c1i:.4f}; pair C(0.2d) base/fine = {cpair['base']:.5f} / "
        f"{cpair['fine']:.5f} (A38 -0.2413, A23 -0.2404); EFE C(0.2d) e = 0.3: {cefe[0.3]:.5f} (A23 -0.0315), "
        f"e = 0.68: {cefe[0.68]:.5f} (A23 +0.1453)")
    check("C1", c1i <= 0.02 and abs(cpair["fine"] / -0.2413 - 1) <= 0.015 and abs(cefe[0.3] + 0.0315) <= 0.02
          and cefe[0.68] > 0,
          f"(i) {c1i:.4f}; (ii) {cpair['fine']:.5f} vs -0.2413 ({(cpair['fine'] / -0.2413 - 1) * 100:+.2f} %); "
          f"(iii) e 0.3: {cefe[0.3]:.5f}, e 0.68: {cefe[0.68]:.5f}",
          "(i) <= 0.02; (ii) within 1.5 %; (iii) within 0.02 of -0.0315 and > 0")
    vneg = {}
    for e_ in (0.3, 0.68):
        l2 = results[f"V_efe{e_}"]["levels"]["fine"]
        rr2 = np.sqrt(l2["RR"] ** 2 + l2["ZZ"] ** 2)
        m_ = (l2["rho"] < 0) & np.isfinite(l2["rho"])
        vneg[e_] = {"V_neg_r<0.6": float(l2["V"][m_ & (rr2 < 0.6)].sum()), "V_neg_r<3": float(l2["V"][m_ & (rr2 < 3)].sum())}
    l0 = results["V_pair"]["levels"]["fine"]
    rr0 = np.sqrt(l0["RR"] ** 2 + l0["ZZ"] ** 2)
    m0 = (l0["rho"] < 0) & np.isfinite(l0["rho"])
    vneg[0] = {"V_neg_r<0.6": float(l0["V"][m0 & (rr0 < 0.6)].sum()), "V_neg_r<3": float(l0["V"][m0 & (rr0 < 3)].sum())}
    log(f"      reading: negative volume (d^3) inside r < 0.6 d / r < 3 d: e 0: {vneg[0]}, e 0.3: {vneg[0.3]}, "
        f"e 0.68: {vneg[0.68]} -- the external field empties the saddle but opens equatorial lobes")
    res["C1"] = {"single_maxdev": c1i, "pair_C02": cpair, "efe_C02": {str(k_): v for k_, v in cefe.items()},
                 "neg_volumes": {str(k_): v for k_, v in vneg.items()}}

    # ---- C2 region maps
    def local_minima(gabs):
        G = gabs.copy()
        G[np.isnan(G)] = np.inf
        pad = np.pad(G, 1, constant_values=np.inf)
        nb = np.min([pad[1 + di:pad.shape[0] - 1 + di, 1 + dj:pad.shape[1] - 1 + dj]
                     for di in (-1, 0, 1) for dj in (-1, 0, 1) if (di, dj) != (0, 0)], axis=0)
        return G <= nb

    def region_stats(lv, M, f, near_r, zc):
        conv = M["Mu_kg"] / M["L_m"] ** 3
        rho_si = lv["rho"] * conv + f * RHO_K
        x_ = lv["gabs"] / M["a0h"]
        val = np.isfinite(rho_si)
        neg = val & (SGN * rho_si < 0)
        rr_ = np.sqrt(lv["RR"] ** 2 + (lv["ZZ"] - zc) ** 2)
        mins = local_minima(lv["gabs"])
        near_null = np.zeros_like(neg)
        for (i, j) in zip(*np.where(mins)):
            near_null[max(i - 2, 0):i + 3, max(j - 2, 0):j + 3] = True
        out = {}
        for zone, zm in (("box", np.ones_like(neg)), ("near", rr_ < near_r)):
            nz_ = neg & zm
            Vn = float(lv["V"][nz_].sum()) * M["L_m"] ** 3
            if Vn == 0:
                out[zone] = {"V_m3": 0.0, "empty": True}
                continue
            w = lv["V"][nz_]
            a_ = np.abs(rho_si[nz_])
            o_ = np.argsort(a_)
            cw = np.cumsum(w[o_]) / w.sum()
            med = float(a_[o_][np.searchsorted(cw, 0.5)])
            xo = x_[nz_]
            ox = np.argsort(xo)
            cwx = np.cumsum(w[ox]) / w.sum()
            xmed = float(xo[ox][np.searchsorted(cwx, 0.5)])
            ex = nz_ & ~near_null
            mx = float(np.max(np.abs(rho_si[ex]))) if ex.any() else float("nan")
            imx = np.unravel_index(np.argmax(np.where(ex, np.abs(rho_si), -1)), rho_si.shape)
            out[zone] = {"V_m3": Vn, "empty": False, "ell_m": Vn ** (1 / 3), "median_abs_rho": med, "x_median": xmed,
                         "max_abs_rho_excl_null": mx, "x_at_max": float(x_[imx]),
                         "at_max_Rz_m": [float(lv["RR"][imx] * M["L_m"]), float(lv["ZZ"][imx] * M["L_m"])],
                         "R_range_m": [float(lv["RR"][nz_].min() * M["L_m"]), float(lv["RR"][nz_].max() * M["L_m"])],
                         "z_range_m": [float(lv["ZZ"][nz_].min() * M["L_m"]), float(lv["ZZ"][nz_].max() * M["L_m"])],
                         "touches_box": bool((lv["RR"][nz_].max() >= lv["R"][-2]) or (np.abs(lv["ZZ"][nz_]).max() >= lv["z"][-2]))}
        return out

    regions = {}
    conv_ok = True
    conv_rows = []
    for nm, M in meta.items():
        regions[nm] = {}
        for f in F_DUST:
            regions[nm][f"f{f}"] = {lvn: region_stats(results[nm]["levels"][lvn], M, f, M["near_r"], M["zc"])
                                    for lvn in ("base", "fine")}
        b_, f_ = regions[nm]["f0"]["base"]["box"], regions[nm]["f0"]["fine"]["box"]
        if b_["empty"] and f_["empty"]:
            dv = dm = 0.0
        elif b_["empty"] != f_["empty"]:
            dv = dm = float("inf")
        else:
            dv = abs(f_["V_m3"] / b_["V_m3"] - 1)
            dm = abs(f_["median_abs_rho"] / b_["median_abs_rho"] - 1)
        conv_rows.append((nm, dv, dm))
        conv_ok &= dv <= 0.10 and dm <= 0.10
    worst = max(conv_rows, key=lambda r_: max(r_[1], r_[2]))
    for nm in meta:
        rf = regions[nm]["f0"]["fine"]
        bx, nr_ = rf["box"], rf["near"]
        r3 = regions[nm]["f3"]["fine"]["near"]
        if bx["empty"]:
            log(f"  {nm:40s}: R- EMPTY (f = 0)")
            continue
        log(f"  {nm:40s}: near zone V^(1/3) {nr_.get('ell_m', 0) / KPC if not nr_['empty'] else 0:9.1f} kpc, median |rho| "
            f"{(nr_.get('median_abs_rho', 0) / MSUN_PC3):.2e} Msun/pc^3 (x {nr_.get('x_median', float('nan')):.2e}), max "
            f"{(nr_.get('max_abs_rho_excl_null', 0) / MSUN_PC3):.2e}; whole box V^(1/3) {bx['ell_m'] / KPC:.0f} kpc "
            f"(touches box: {bx['touches_box']}); f = 3: near V^(1/3) "
            f"{(r3.get('ell_m', 0) / KPC) if not r3['empty'] else 0:.1f} kpc")
    check("C2", conv_ok, f"{len(conv_rows)} maps; worst base->fine change {worst[0]}: volume {worst[1]:.3f}, "
          f"median {worst[2]:.3f}", "<= 0.10 each")
    res["C2_convergence"] = conv_rows
    # C2b (AMENDMENT A1, post-result): fine -> extra-fine for the isolated unequal-mass maps
    c2b = []
    spec_by = {sp_["name"]: sp_ for sp_ in specs}
    with cf.ProcessPoolExecutor(max_workers=1, mp_context=ctx, max_tasks_per_child=1) as ex:
        for nm in [n_ for n_ in meta if (n_.startswith("S2_") or n_.startswith("S4_")) and n_.endswith("|e0")]:
            lx = ex.submit(run_level, spec_by[nm], "xfine", results[nm]["null_z"]).result()
            sx = region_stats(lx, meta[nm], 0, meta[nm]["near_r"], meta[nm]["zc"])["box"]
            sf = regions[nm]["f0"]["fine"]["box"]
            dv, dm = abs(sx["V_m3"] / sf["V_m3"] - 1), abs(sx["median_abs_rho"] / sf["median_abs_rho"] - 1)
            c2b.append((nm, dv, dm, lx["nr"], lx["nz"], lx["info"]["residual_rel"], lx["rss_GB"]))
            log(f"  C2b {nm:32s} extra-fine grid {lx['nr']}x{lx['nz']} residual {lx['info']['residual_rel']:.1e} "
                f"(child RSS {lx['rss_GB']:.2f} GB): fine->extra-fine volume {dv:.4f}, median {dm:.4f}")
    check("C2b", all(r_[1] <= 0.10 and r_[2] <= 0.10 for r_ in c2b),
          f"max change volume {max(r_[1] for r_ in c2b):.4f}, median {max(r_[2] for r_ in c2b):.4f} over {len(c2b)} maps",
          "<= 0.10 each (AMENDMENT A1, post-result; C2 kept as frozen)")
    res["C2b_extra_fine"] = c2b

    # ---- C3 screened Solar System (linear response about the Galactic P background)
    ss_rows = []
    ok_c3 = True
    for foot in A0:
        lvd = results[f"S5a_MW_disc|{foot}|e0"]["levels"]["fine"]
        Md = meta[f"S5a_MW_disc|{foot}|e0"]
        jz = np.argmin(np.abs(lvd["z"] - 0.02 / 2.6))
        rho_gal = float(np.interp(8.2 / 2.6, lvd["R"], lvd["rho"][:, jz])) * Md["Mu_kg"] / Md["L_m"] ** 3 / MSUN_PC3
        for Lp in LSTAR[foot]:
            ell = Lp / math.sqrt(2)                     # pc
            for xe in (1.15, 2.6):
                mmax = 2 * xe + xe ** 2
                Glow = lambda r_pc: 1 / (4 * math.pi * ell ** 2 * r_pc) - math.sqrt(mmax) / (4 * math.pi * ell ** 3)
                rnull = math.sqrt(GMSUN / (xe * A0[foot]))
                pts = {"Sun-Earth saddle": [(1.0, AU - 2.59e8), (3.003e-6, 2.59e8)],
                       "Earth-Moon saddle": [(1.0, AU), (3.003e-6, 3.46e8), (3.69e-8, 3.844e8 - 3.46e8)],
                       "1 AU": [(1.0, AU), (3.003e-6, 2 * AU)],
                       "100 AU": [(1.0, 100 * AU)],
                       "Sun-Galaxy null": [(1.0, rnull)],
                       "0.1 pc": [(1.0, 0.1 * PC)]}
                for pn, comps in pts.items():
                    dp = rho_gal + sum(Mc * Glow(rc / PC) for Mc, rc in comps)
                    ss_rows.append({"foot": foot, "Lstar_pc": Lp, "x_e": xe, "point": pn, "DP_Msun_pc3": dp,
                                    "rho_gal_phantom": rho_gal})
                    ok_c3 &= dp > 0
    mindp = min(ss_rows, key=lambda r_: r_["DP_Msun_pc3"])
    log(f"  C3: Galactic phantom at the Sun (S5a, in-plane, 8.2 kpc) = "
        f"{[round(r_['rho_gal_phantom'], 4) for r_ in ss_rows if r_['point'] == '0.1 pc' and r_['x_e'] == 1.15 and r_['Lstar_pc'] == 24.0]}"
        f" Msun/pc^3 (canonical, alt); min screened D.P over samples = {mindp['DP_Msun_pc3']:.3e} Msun/pc^3 at "
        f"{mindp['point']} ({mindp['foot']}, L* {mindp['Lstar_pc']} pc, x_e {mindp['x_e']})")
    check("C3", ok_c3, f"min D.P = {mindp['DP_Msun_pc3']:.3e} Msun/pc^3 over {len(ss_rows)} samples",
          "> 0 everywhere (screening removes the region)")
    res["C3"] = ss_rows
    log(f"C done ({time.time() - T0:.1f} s)")

    # ================================================================================================ PART D
    log("")
    log("D: growth rates, e-folds, verdicts")
    K4 = 4 * math.pi * G_SI

    def rates(rho_abs, x_, Lp, T):
        mL1 = (1 + x_) ** 2 - 1
        Gb = math.sqrt(K4 * rho_abs * mL1)
        out = {"Gamma_bounded_s-1": Gb, "N_bounded": Gb * T}
        for lam_name, lam in (("L*", Lp * PC), ("1pc", PC), ("1AU", AU)):
            kL = 2 * math.pi / lam * Lp * PC
            Gm = math.sqrt(K4 * rho_abs * (mL1 + kL ** 2 / 2))
            out[f"Gamma_{lam_name}_s-1"] = Gm
            out[f"N_{lam_name}"] = Gm * T
        rhs = 1 / (K4 * rho_abs * T ** 2) - mL1
        out["lambda1_pc"] = float("inf") if rhs <= 0 else 2 * math.pi * Lp / math.sqrt(2 * rhs)
        return out

    verdict = {}
    efold = {}
    system_names = sorted({M["system"] for M in meta.values()})
    for sysn in system_names + ["S7_solar_system"]:
        verdict[sysn] = {}
        for foot in A0:
            if sysn == "S7_solar_system":
                neg_any = any((SGN * r_["DP_Msun_pc3"] < 0) for r_ in ss_rows if r_["foot"] == foot)
                v = "ILL-POSED" if neg_any else "HEALTHY"
                if neg_any:   # mutated run: the Solar System pair (D.P > 0) becomes the unstable one
                    rr_ = [r_ for r_ in ss_rows if r_["foot"] == foot and r_["point"] == "1 AU"][0]
                    efold[f"S7|{foot}"] = rates(rr_["DP_Msun_pc3"] * MSUN_PC3, 1.15, 24.0, T_H)
                verdict[sysn][foot] = v
                continue
            names = [nm for nm, M in meta.items() if M["system"] == sysn and M["foot"] == foot]
            vs = []
            for nm in names:
                M = meta[nm]
                r0_ = regions[nm]["f0"]["fine"]
                r3_ = regions[nm]["f3"]["fine"]
                if r0_["box"]["empty"] or r0_["near"]["empty"] and r0_["box"].get("ell_m", 0) < 10 * 90 * PC:
                    vs.append("HEALTHY")
                    continue
                zone = r0_["near"] if not r0_["near"]["empty"] else r0_["box"]
                ell = zone["ell_m"]
                ill = (ell >= 10 * 90 * PC) and (lim_uv != 0) and (1.8 <= r_grow <= 2.2)
                dust_cond = r3_["near"]["empty"] and r3_["box"]["empty"]
                v = ("ILL-POSED" + (" (dust-conditional)" if dust_cond else "")) if ill else "BOUNDED INSTABILITY"
                vs.append(v)
                T = min(T_H, ell / M["v"]) if M["v"] else 10 * GYR
                for Lp in LSTAR[foot]:
                    efold[f"{nm}|L*{Lp}"] = {"T_Gyr": T / GYR, "ell_kpc": ell / KPC,
                                             "median": rates(zone["median_abs_rho"], zone["x_median"], Lp, T),
                                             "max": rates(zone["max_abs_rho_excl_null"], zone["x_at_max"], Lp, T)}
                    if not r3_["near"]["empty"]:
                        z3 = r3_["near"]
                        efold[f"{nm}|L*{Lp}"]["f3_median"] = rates(z3["median_abs_rho"], z3["x_median"], Lp, T)
            order = ["ILL-POSED", "ILL-POSED (dust-conditional)", "BOUNDED INSTABILITY", "HEALTHY"]
            verdict[sysn][foot] = min(vs, key=lambda s: order.index(s)) if vs else "HEALTHY"
    allv = [v for d in verdict.values() for v in d.values()]
    overall = ("ILL-POSED" if any(v.startswith("ILL-POSED") for v in allv)
               else ("HEALTHY" if all(v == "HEALTHY" for v in allv) else "BOUNDED INSTABILITY"))
    for sysn, d in verdict.items():
        log(f"  {sysn:22s}: canonical {d['canonical']:30s} alt {d['alt']}")
    log(f"  OVERALL: {overall}")
    for key in [k_ for k_ in efold if "|L*24.0" in k_ and "canonical" in k_]:
        e_ = efold[key]
        m_ = e_["median"]
        log(f"    {key:52s} T {e_['T_Gyr']:.2f} Gyr: N_bounded {m_['N_bounded']:.2e}; N(L*) {m_['N_L*']:.2e}, "
            f"N(1 pc) {m_['N_1pc']:.2e}, N(1 AU) {m_['N_1AU']:.2e}; lambda_1 {m_['lambda1_pc']:.3g} pc; "
            f"Gamma(1 AU) {m_['Gamma_1AU_s-1']:.2e} /s")
    finite = all(np.isfinite(v_) for e_ in efold.values() for blk in e_.values() if isinstance(blk, dict)
                 for kk2, v_ in blk.items() if kk2 != "lambda1_pc")
    check("D1", finite and len(efold) > 0, f"{len(efold)} e-fold rows, all finite: {finite}", "all finite")
    # hydrostatic mu_K dust estimate (reading)
    hyd = {}
    for nm, M in meta.items():
        z0 = regions[nm]["f0"]["fine"]["near"]
        if z0["empty"] or M["system"].startswith("S5") or M["system"].startswith("S6"):
            continue
        dpsi = math.sqrt(G_SI * M["Mu_kg"] * sum(m_[0] for m_ in SYS[M["system"]]["m"]) * M["a0"]) * math.log(10)
        hyd[nm] = {f"muK={mk}/Mpc": (mk / MPC) ** 2 * dpsi / (4 * math.pi * G_SI) / z0["median_abs_rho"]
                   for mk in (0.1, 10.0)}
    log(f"  reading: hydrostatic mu_K^2 dust / median |rho_tau| (|dpsi| = sqrt(G M a0) ln 10): "
        + "; ".join(f"{k_.split('|')[0]} {k_.split('|')[2]}: {v['muK=0.1/Mpc']:.1e} (0.1/Mpc), {v['muK=10.0/Mpc']:.1e} (cap)"
                    for k_, v in hyd.items() if "canonical" in k_))
    res.update({"regions": regions, "meta": meta, "efolds": efold, "verdicts": verdict, "overall": overall,
                "hydrostatic_dust_ratio": hyd, "rho_K_kg_m3": RHO_K})

    npass = sum(c_["pass"] for c_ in checks)
    rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / (1024 ** 3 if sys.platform == "darwin" else 1024 ** 2)
    rssc = resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss / (1024 ** 3 if sys.platform == "darwin" else 1024 ** 2)
    log(f"run: {time.time() - T0:.1f} s, peak RSS parent {rss:.2f} GB, children {rssc:.2f} GB, single thread")
    log(f"H4_V3_SADDLE_STABILITY COMPLETE: {npass}/{len(checks)} checks PASS.")
    res["checks"] = checks
    res["runtime_s"] = time.time() - T0
    res["peak_rss_GB"] = {"parent": rss, "children": rssc}

    def clean(o):
        if isinstance(o, dict):
            return {str(k_): clean(v) for k_, v in o.items()}
        if isinstance(o, (list, tuple)):
            return [clean(v) for v in o]
        if isinstance(o, (np.floating, float)):
            return float(o) if np.isfinite(o) else str(o)
        if isinstance(o, (np.integer,)):
            return int(o)
        if isinstance(o, (np.bool_,)):
            return bool(o)
        return o

    with open(JSON, "w") as fh:
        json.dump(clean(res), fh, indent=1)
    with open(OUT, "w") as fh:
        fh.write("\n".join(lines) + "\n")
    sys.exit(0 if npass == len(checks) else 1)


if __name__ == "__main__":
    main()
