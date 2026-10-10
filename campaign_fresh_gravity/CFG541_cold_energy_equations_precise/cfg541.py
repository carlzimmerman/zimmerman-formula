#!/usr/bin/env python3
"""CFG541: the cold-energy equations of motion made precise (CFG539 class A). FROZEN_CRITERIA.md (committed alone first).

Sympy (audit, first variation, gradient-flow symmetry test, Lyapunov identity, dispersion relations, Routh-Hurwitz) plus a 1-D
spherical drift-only model of class A (static baryons; cold energy at rest, uniform inside the turnaround radius at the cosmic
ratio; finite-volume donor-cell fluxes, exact mass conservation). No PM runs.
kappa = 1/2 FITTED; footings 9.3603e-11 / 1.1312e-10 never pooled; cold energy mass required; not "theory closed".
CFG541_MUTATE=1 -> M1 sign-reversed drift, M2 unlimited reservoir, M3 hidden-constant audit; outputs *_MUTATE.*
Run: OMP_NUM_THREADS=2 nice -n 10 python3 cfg541.py
"""
import os, sys, json, math
os.environ.setdefault("OMP_NUM_THREADS", "2")
import numpy as np
import sympy as sp
from scipy.integrate import solve_ivp

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "CFG515_census_edge_resolution"))
sys.path.insert(0, os.path.join(HERE, "..", "CFG540_vizier2026_bfjr_mhongoose"))
from cfg515_lib import fret_census, FB, COLD_PER_B  # noqa: E402  (read-only import)
import cfg540_bfjr as B  # noqa: E402  (read-only import: estimator + data reader)

MUT = os.environ.get("CFG541_MUTATE", "0") == "1"
TAG = "_MUTATE" if MUT else ""
G, c, MSUN, KPC, GYR = 6.674e-11, 2.99792458e8, 1.989e30, 3.0857e19, 3.15576e16
FOOT = {"can": 9.3603e-11, "alt": 1.1312e-10}
KAPPA = 0.5
h = 0.674; OM = 0.14237 / h ** 2; OL = 1.0 - OM
H0 = 100 * h * 1e3 / 3.0857e22; RHOCRIT = 3 * H0 ** 2 / (8 * math.pi * G)
OUT, RES = [], {"lane": "CFG541", "mutate": MUT, "settings": dict(kappa=KAPPA, footings=FOOT, f_b=FB, cold_per_b=COLD_PER_B,
                                                                     Omega_m=OM, h=h)}


def log(s=""):
    print(s, flush=True); OUT.append(str(s))


# ====================================================================================== D1: dimensional + constants audit
def audit(hidden=False):
    Mm, Ll, Tt = sp.symbols("M L T", positive=True)
    dims = {"G": Ll ** 3 / Mm / Tt ** 2, "c": Ll / Tt, "rho": Mm / Ll ** 3, "rho_c": Mm / Ll ** 3, "rho_b": Mm / Ll ** 3,
            "rho_m": Mm / Ll ** 3, "rho_ph": Mm / Ll ** 3, "rho_DE": Mm / Ll ** 3, "d": Mm / Ll ** 3, "Phi": Ll ** 2 / Tt ** 2,
            "psi": Ll ** 2 / Tt ** 2, "nabla": 1 / Ll, "dt": 1 / Tt, "v": Ll / Tt, "f": Mm / Ll ** 6 * Tt ** 3, "dV": Ll ** 3,
            "nabla_v": Tt / Ll, "kappa": 1, "f_b": 1, "H": 1 / Tt, "M_b": Mm, "r": Ll, "w": 1, "tau_psi": Tt, "T0": Tt}
    allowed = {"G", "c", "rho_DE", "kappa", "f_b", "H"}           # constants; everything else must be a field/state symbol
    fields = {"rho", "rho_c", "rho_b", "rho_m", "rho_ph", "d", "Phi", "psi", "nabla", "dt", "v", "f", "dV", "nabla_v", "M_b",
              "r", "w", "tau_psi"}
    S = {k: sp.Symbol(k, positive=True) for k in dims}
    tau = (4 * sp.pi * S["G"] * S["rho_m"]) ** sp.Rational(-1, 2)
    if hidden:
        tau = S["T0"]                                              # M3: a hidden constant time (1 Gyr) inserted
    a0 = S["kappa"] * S["c"] * sp.sqrt(S["G"] * S["rho_DE"])
    vs = tau * S["nabla"] * S["psi"]
    Gam = 4 * sp.pi * S["G"] * S["rho_c"] * tau
    eqs = {
        "Poisson Phi": [S["nabla"] ** 2 * S["Phi"], 4 * sp.pi * S["G"] * S["rho_m"]],
        "Vlasov (baryons/cold) + drift": [S["dt"] * S["f"], S["v"] * S["nabla"] * S["f"], S["nabla"] * S["Phi"] * S["nabla_v"] * S["f"],
                                          S["nabla"] * (vs * S["f"])],
        "continuity": [S["dt"] * S["rho_c"], S["nabla"] * (S["rho_c"] * (S["v"] + vs))],
        "deficit Poisson": [S["nabla"] ** 2 * S["psi"], 4 * sp.pi * S["G"] * S["d"]],
        "phantom (QUMOND/round)": [S["rho_ph"], S["nabla"] * (S["nabla"] * S["Phi"]) / (4 * sp.pi * S["G"])],
        "kernel argument y = g/a0": [S["nabla"] * S["Phi"] / a0, sp.Integer(1)],
        "drift velocity": [vs, S["v"]],
        "relaxation rate Gamma": [Gam, S["dt"]],
        "F = (1/8piG) int |grad psi|^2": [(S["nabla"] * S["psi"]) ** 2 * S["dV"] / S["G"], S["M_b"] * S["v"] ** 2],
        "dF/dt = -int rho_c tau |grad psi|^2": [S["dt"] * (S["nabla"] * S["psi"]) ** 2 * S["dV"] / S["G"],
                                               S["rho_c"] * tau * (S["nabla"] * S["psi"]) ** 2 * S["dV"]],
        "census edge r_M/ln(...)": [sp.sqrt(S["G"] * S["M_b"] / a0), S["r"]],
        "Cattaneo drift": [tau * S["dt"] * S["v"], S["v"], tau * S["nabla"] * S["psi"]],
        "damped psi wave": [S["dt"] ** 2 * S["psi"] / S["c"] ** 2, S["dt"] * S["psi"] / (S["c"] ** 2 * S["tau_psi"]),
                            S["nabla"] ** 2 * S["psi"], S["G"] * S["d"]],
        "DE exchange rho_DE' + 3H(1+w)rho_DE = Q/c^2": [S["dt"] * S["rho_DE"], S["H"] * (1 + S["w"]) * S["rho_DE"],
                                                     S["rho_c"] * vs * S["nabla"] * S["Phi"] / S["c"] ** 2],
    }
    sub = {S[k]: v for k, v in dims.items()}
    out, ok_all = {}, True
    for name, terms in eqs.items():
        dl = [sp.simplify(sp.nsimplify(t).subs(sub) / sp.Integer(1)) for t in terms]
        dl = [sp.simplify(x.subs(sp.pi, 1)) for x in dl]
        base = dl[0]
        same = all(sp.simplify(x / base).free_symbols == set() for x in dl)
        consts = set()
        for t in terms:
            consts |= {str(s_) for s_ in sp.sympify(t).free_symbols}
        bad = sorted(consts - allowed - fields)
        ok = same and not bad
        ok_all &= ok
        out[name] = dict(dims_consistent=bool(same), unlisted_constants=bad, ok=bool(ok))
    tau_syms = sorted(str(s_) for s_ in sp.sympify(tau).free_symbols)
    return ok_all, out, tau_syms


# ====================================================================================== V1/V2: first variation, gradient test
def variational_sympy():
    r1, r2, r3, P1, P2, P3 = sp.symbols("rho1 rho2 rho3 P1 P2 P3", real=True)
    K = sp.Matrix(3, 3, lambda i, j: sp.Symbol(f"K{min(i, j)}{max(i, j)}", positive=True))   # symmetric Green matrix (>0)
    rho, P = sp.Matrix([r1, r2, r3]), sp.Matrix([P1, P2, P3])
    # cells 1,2 in deficit with s = 1; cell 3 = shell: s = 1 (variational form) or s = 0 (CFG539 committed: outside the edge)
    res = {}
    for form, s3 in (("variational", 1), ("committed", 0)):
        s = sp.Matrix([1, 1, s3])
        d = sp.Matrix([s[i] * (P[i] - rho[i]) for i in range(3)])   # cells taken in deficit (d > 0 branch)
        psi = -K * d
        F = sp.Rational(1, 2) * (d.T * K * d)[0]
        grad = sp.Matrix([sp.diff(F, x) for x in rho])
        v1 = sp.simplify(grad - sp.Matrix([s[i] * psi[i] for i in range(3)])) == sp.zeros(3, 1)
        mobile = [0, 1, 2]                                           # variational: mobility on s; committed: on the catchment
        mu = sp.Matrix([s[i] * psi[i] for i in range(3)]) if form == "variational" else psi   # committed drift uses psi everywhere
        J = sp.Matrix(3, 3, lambda i, j: sp.diff(mu[i], rho[j]))
        sym = sp.simplify(J - J.T) == sp.zeros(3, 3)
        res[form] = dict(first_variation_is_s_psi=bool(v1), response_matrix_symmetric=bool(sym),
                         J=str(J))
    # interval subgradient on {d = 0, s > 0}: one-sided derivatives of F wrt rho_3 at rho_3 = P_3 (s3 = 1)
    e = sp.Symbol("e", positive=True)
    d_lo = sp.Matrix([P1 - r1, P2 - r2, e]); d_hi = sp.Matrix([P1 - r1, P2 - r2, 0])
    F_lo = sp.Rational(1, 2) * (d_lo.T * K * d_lo)[0]
    left = sp.simplify(-sp.diff(F_lo, e).subs(e, 0))                # derivative wrt rho_3 from below (removing mass)
    psi3 = (-K * d_hi)[2]
    res["subgradient_at_filled_cell"] = dict(left_derivative=str(left), equals_psi3=bool(sp.simplify(left - psi3) == 0),
                                             right_derivative="0 (overfilling leaves d = 0)")
    return res


def lyapunov_sympy():
    r = sp.Symbol("r", positive=True)
    psi, w = sp.Function("psi")(r), sp.Function("w")(r)            # w = rho_c tau >= 0
    lhs = sp.diff(psi * w * sp.diff(psi, r) * r ** 2, r) - psi * sp.diff(w * sp.diff(psi, r) * r ** 2, r)
    ident = sp.simplify(lhs - w * sp.diff(psi, r) ** 2 * r ** 2) == 0
    # stationary condition: flux rho_c tau psi' = 0 contains alpha only as an overall positive factor
    al, rc, tau = sp.symbols("alpha rho_c tau", positive=True); dpsi = sp.Symbol("dpsi", real=True)
    flux = al * rc * tau * dpsi
    stat = sp.solve(sp.Eq(flux, 0), dpsi)
    return dict(by_parts_identity=bool(ident),
                note="d/dr(psi w psi' r^2) - psi (w psi' r^2)' = w psi'^2 r^2 => dF/dt = int psi d_t rho_c dV = -int rho_c tau |psi'|^2 dV "
                     "+ [4 pi r^2 psi rho_c tau psi'] at the mobility boundary, which vanishes because the mobility is zero outside it",
                stationary_condition_alpha_free=bool(stat == [0]),
                stationary_solutions_dpsi=str(stat))


# ====================================================================================== C2: dispersion relations
def dispersion():
    s, k, cc, G_, rc, tau, taup = sp.symbols("s k c G rho_c tau tau_psi", positive=True)
    s = sp.Symbol("s")
    drho, v, psi = sp.symbols("drho v psi")
    Gam = 4 * sp.pi * G_ * rc * tau
    I = sp.I
    cont = s * drho + rc * I * k * v
    drift0 = v + tau * I * k * psi
    drift1 = tau * s * v + v + tau * I * k * psi
    psi0 = -k ** 2 * psi + 4 * sp.pi * G_ * drho                     # lap psi = 4 pi G d, delta d = -delta rho
    psi1 = -k ** 2 * psi - s ** 2 * psi / cc ** 2 + 4 * sp.pi * G_ * drho
    psi2 = -k ** 2 * psi - s ** 2 * psi / cc ** 2 - s * psi / (cc ** 2 * taup) + 4 * sp.pi * G_ * drho
    models = {"A0 instantaneous": (drift0, psi0), "A1 undamped wave": (drift0, psi1), "A2 damped wave": (drift0, psi2),
              "A3 Cattaneo + instantaneous": (drift1, psi0), "A4 Cattaneo + undamped wave": (drift1, psi1),
              "A5 Cattaneo + damped wave": (drift1, psi2)}
    gam, q, K, beta = sp.symbols("Gamma q K beta", positive=True)     # Gamma = 4piG rho_c tau, q = Gamma tau = rho_c/rho_m
    out, polys = {}, {}
    for name, (dr, ps) in models.items():
        Mx = sp.Matrix([[sp.diff(e_, x) for x in (drho, v, psi)] for e_ in (cont, dr, ps)])
        det = sp.expand(sp.simplify(Mx.det()))
        # units Gamma = 1: tau = q, tau_psi = beta * tau, c k = K, 4 pi G rho_c tau = 1 -> 4 pi G = 1/(rho_c q)
        det1 = det.subs({taup: beta * tau}).subs({G_: 1 / (4 * sp.pi * rc * tau)}).subs({tau: q, cc: K / k})
        poly = sp.Poly(sp.numer(sp.together(sp.expand(det1))), s)
        co = [sp.simplify(x) for x in poly.all_coeffs()]
        lead = co[0]
        co = [sp.simplify(x / lead) for x in co]
        polys[name] = co
        hur = {}
        n = len(co) - 1
        if n == 1:
            hur = {"root": str(sp.solve(sum(cf * s ** (n - i) for i, cf in enumerate(co)), s))}
        elif n == 3:
            a2, a1, a0_ = co[1], co[2], co[3]
            hur = {"a2": str(a2), "a1": str(a1), "a0": str(a0_), "H2 = a2 a1 - a0": str(sp.factor(sp.simplify(a2 * a1 - a0_)))}
        elif n == 2:
            hur = {"a1": str(co[1]), "a0": str(co[2])}
        elif n == 4:
            a3, a2, a1, a0_ = co[1], co[2], co[3], co[4]
            hur = {"a3": str(a3), "a2": str(a2), "a1": str(a1), "a0": str(a0_),
                   "H2 = a3 a2 - a1": str(sp.factor(sp.simplify(a3 * a2 - a1))),
                   "H3 = a3 a2 a1 - a1^2 - a3^2 a0": str(sp.factor(sp.simplify(a3 * a2 * a1 - a1 ** 2 - a3 ** 2 * a0_)))}
        out[name] = dict(degree=n, coeffs_monic=[str(x) for x in co], hurwitz=hur)
    # numerical root scan
    Ks = np.logspace(-3, 3, 61); qs = np.linspace(0.01, 0.99, 50)
    scan = {}
    for name, co in polys.items():
        f = [sp.lambdify((K, q, beta), x, "numpy") for x in co]
        worst = -np.inf; arg = None
        for Kv in Ks:
            for qv in qs:
                cf = [complex(fi(Kv, qv, 1.0)) for fi in f]
                rts = np.roots(cf)
                mr = float(np.max(rts.real))
                if mr > worst: worst, arg = mr, (float(Kv), float(qv))
        # beta scan for the damped models: stability boundary beta * q < 1
        bscan = None
        if "damped" in name:
            bscan = {}
            for bv in (0.5, 1.0, 2.0, 5.0):
                wb = -np.inf
                for Kv in Ks[::3]:
                    for qv in qs:
                        rts = np.roots([complex(fi(Kv, qv, bv)) for fi in f]); wb = max(wb, float(np.max(rts.real)))
                bscan[str(bv)] = wb
        scan[name] = dict(max_Re_s_over_Gamma=worst, at_Kc_over_Gamma_q=arg, beta_scan_max_Re=bscan)
    # A0: k-independence (no propagation)
    a0root = sp.solve(sum(cf * s ** (len(polys["A0 instantaneous"]) - 1 - i) for i, cf in enumerate(polys["A0 instantaneous"])), s)
    return out, scan, [str(x) for x in a0root]


# ====================================================================================== 1-D spherical drift model
def delta_ta(z=0.0):
    """spherical-collapse turnaround overdensity in flat LCDM (algorithm of the CFG361/539 engines' delta_ta, re-implemented)."""
    ai = 1e-3
    def run(di):
        Ri = ai * (1 - di / 3.0); GM = 0.5 * OM * (1 + di) * Ri ** 3 / ai ** 3; Hi = math.sqrt(OM / ai ** 3 + OL)
        def rhs(t, y):
            a, R, V = y; return [a * math.sqrt(OM / a ** 3 + OL), V, -GM / R ** 2 + OL * R]
        ev = lambda t, y: y[2]; ev.terminal = True; ev.direction = -1
        so = solve_ivp(rhs, [0, 50], [ai, Ri, Hi * Ri * (1 - di / 3.0)], events=ev, rtol=1e-10, atol=1e-13)
        if not so.t_events[0].size: return None
        a, R, _ = so.y_events[0][0]; return a, (1 + di) * (Ri / ai) ** 3 * a ** 3 / R ** 3
    at = 1 / (1 + z); lo, hi = 1e-4, 0.05
    for _ in range(60):
        mid = math.sqrt(lo * hi); r = run(mid)
        if r is None or r[0] > at: lo = mid
        else: hi = mid
    return run(hi)[1]


DTA = delta_ta()


def nu_m1(y):
    with np.errstate(over="ignore", divide="ignore"):
        return 1.0 / np.expm1(np.sqrt(y))


class Model:
    def __init__(self, Mb, a_kpc, a0, fret, N=400):
        self.Mb, self.a0, self.fret = Mb * MSUN, a0, fret
        M = self.Mb
        self.rM = math.sqrt(G * M / a0)
        self.Mta = M / (fret * FB); self.Mcat = (1 - FB) * self.Mta
        self.rta = (3 * self.Mta / (4 * math.pi * DTA * OM * RHOCRIT)) ** (1 / 3)
        rin = 1e-3 * self.rM if a_kpc is None else 1e-2 * a_kpc * KPC
        self.rf = rf = np.geomspace(rin, self.rta, N + 1)
        self.V = 4 * math.pi / 3 * np.diff(rf ** 3); self.rc = np.sqrt(rf[1:] * rf[:-1]); self.A = 4 * math.pi * rf ** 2
        self.N = N
        if a_kpc is None:
            self.Mbf = np.full(N + 1, M); self.rhob = np.zeros(N); self.mb = np.zeros(N); self.Mb_in = M
        else:
            ah = a_kpc * KPC; self.Mbf = M * rf ** 2 / (rf + ah) ** 2; self.mb = np.diff(self.Mbf); self.rhob = self.mb / self.V
            self.Mb_in = self.Mbf[0]
        y = G * self.Mbf / (rf ** 2 * a0)
        self.Mphf = self.Mbf * nu_m1(y)
        self.rhoph = np.maximum(np.diff(self.Mphf), 0.0) / self.V
        self.rhoph_neg_cells = int((np.diff(self.Mphf) < 0).sum())
        self.rhoc0 = self.Mcat / (4 * math.pi / 3 * (self.rta ** 3 - rin ** 3))
        self.Vf2 = math.sqrt(G * M * a0)
        gN = G * self.Mbf / rf ** 2
        self.gl = gN * (1 + nu_m1(gN / a0))                       # law field of the baryons (target)

    # --- field quantities
    def fields(self, m):
        rho = m / self.V
        d = np.maximum(self.rhoph - rho, 0.0)
        Md = np.concatenate([[0.0], np.cumsum(d * self.V)])
        dpsi = G * Md / self.rf ** 2
        return rho, d, Md, dpsi

    def psi_cells(self, Md, dpsi):
        psi_f = np.empty(self.N + 1); psi_f[-1] = -G * Md[-1] / self.rf[-1]
        dr = np.diff(self.rf)
        psi_f[:-1] = psi_f[-1] - np.cumsum((0.5 * (dpsi[1:] + dpsi[:-1]) * dr)[::-1])[::-1]
        return 0.5 * (psi_f[1:] + psi_f[:-1])

    def F(self, m):
        rho, d, Md, dpsi = self.fields(m)
        return -0.5 * float(np.dot(self.psi_cells(Md, dpsi), d * self.V))

    def energy(self, m):
        mt = self.mb + m
        Menc = self.Mb_in + np.concatenate([[0.0], np.cumsum(mt)[:-1]]) + 0.5 * mt
        W = -float(np.sum(G * Menc * mt / self.rc))
        g = G * Menc / self.rc ** 2
        rho = m / self.V; dr = np.diff(self.rf)
        P = np.cumsum((rho * g * dr)[::-1])[::-1]
        K = 1.5 * float(np.sum(P * self.V))
        return W, K

    def front(self, m, frac=0.5):
        rho = m / self.V
        q = np.where(self.rhoph > 1e-300, rho / np.maximum(self.rhoph, 1e-300), np.inf)
        bad = np.where(q < frac)[0]
        if bad.size == 0: return self.rf[-1], self.rf[-1], self.N
        i = int(bad[0])                                           # first cell (from inside) below frac: front = its inner face
        # sub-cell estimate: equivalent filled radius, r^3 = r_i0^3 + sum_j min(q_j, 1) (r_j+1^3 - r_j^3) from the first cell i0 with
        # q < 0.999 outward (volume-weighted fill of the partially filled front cells)
        i0 = int(np.where(q < 0.999)[0][0])
        qq = np.minimum(np.where(np.isfinite(q), q, 1.0), 1.0)[i0:]
        rsub = (self.rf[i0] ** 3 + float(np.sum(qq * (self.rf[i0 + 1:] ** 3 - self.rf[i0:-1] ** 3)))) ** (1 / 3)
        return self.rf[i], rsub, i

    def analytic_rstar(self):
        dens = np.maximum(self.rhoph, self.rhoc0)
        cum = np.concatenate([[0.0], np.cumsum(dens * self.V)])
        if cum[-1] < self.Mcat: return self.rf[-1]
        i = int(np.searchsorted(cum, self.Mcat)) - 1
        fr = (self.Mcat - cum[i]) / (cum[i + 1] - cum[i])
        return (self.rf[i] ** 3 + fr * (self.rf[i + 1] ** 3 - self.rf[i] ** 3)) ** (1 / 3)

    def settled_front(self, m):
        """cold mass inside the current front (contiguous filled region from the centre)."""
        _, _, i = self.front(m)
        return float(m[:i].sum())

    def run(self, alpha=1.0, sign=1, unlimited=False, tmax=300 * GYR, trackF=False, stop=True, maxsteps=3_000_000):
        N, V, A = self.N, self.V, self.A
        m = self.rhoc0 * V.copy(); m0 = m.copy()
        thr = 1e-12 * m0                                           # per-cell trace threshold (correction 1, numerics)
        rstar = self.analytic_rstar(); kin = int(np.searchsorted(self.rf, rstar)) - 1   # cells fully inside r_*: [0, kin)
        Sin = lambda mm: float(mm[:kin].sum())
        t, n = 0.0, 0
        Fprev = self.F(m) if trackF else None
        F0 = Fprev; maxinc = -np.inf
        ts, Ss, fronts, vmax_run, pimax_run = [0.0], [Sin(m)], [self.front(m)[0]], 0.0, 0.0
        ffill = [self.front(m, 0.999)[0]]                          # post-freeze diag: filled front (q >= 0.999)
        rho, d, Md, dpsi = self.fields(m)
        tau = 1 / np.sqrt(4 * math.pi * G * (rho + self.rhob))
        v0 = alpha * tau[1:] * dpsi[1:N]                            # inward drift speed at internal faces, t = 0 (donor = outer cell)
        vc = np.sqrt(self.gl[1:N] * self.rf[1:N])
        pi0 = v0 * tau[1:] / self.rf[1:N]                           # overdamped-consistency number Pi = |v_s| tau / r (post-freeze diag)
        c1 = dict(max_vs_over_c=float(v0.max() / c), max_vs_over_Vc=float(np.max(v0 / vc)), max_vs_kms=float(v0.max() / 1e3),
                  r_at_max_kpc=float(self.rf[1:N][np.argmax(v0)] / KPC), max_Pi=float(pi0.max()),
                  r_at_maxPi_kpc=float(self.rf[1:N][np.argmax(pi0)] / KPC))
        while t < tmax and n < maxsteps:
            rho, d, Md, dpsi = self.fields(m)
            live = m > thr
            with np.errstate(divide="ignore"):
                tau = np.where(live, 1 / np.sqrt(4 * math.pi * G * np.maximum(rho + self.rhob, 1e-300)), 0.0)
            don = slice(1, N) if sign > 0 else slice(0, N - 1)
            v = alpha * tau[don] * dpsi[1:N]
            ok = live[don]
            flux = rho[don] * v * A[1:N]
            with np.errstate(divide="ignore", over="ignore"):
                dtc = np.where(ok & (v > 0), 0.4 * V[don] / np.maximum(A[1:N] * v, 1e-300), np.inf).min()
            gam = float((4 * math.pi * G * rho * tau * alpha)[live].max()) if live.any() else 0.0
            dt = min(dtc, 0.2 / gam if gam > 0 else np.inf, tmax - t)
            if not np.isfinite(dt): dt = tmax - t
            tr = np.where(ok, np.minimum(flux * dt, m[don]), 0.0)
            tr = np.where(ok & (m[don] - tr < thr[don]) & (tr > 0), m[don], tr)   # a draining cell's last trace moves whole: mass exact
            if sign > 0:
                m[1:] -= tr; m[:-1] += tr
            else:
                m[:-1] -= tr; m[1:] += tr
            if unlimited: m[-1] = m0[-1]
            t += dt; n += 1
            sel = (rho >= 1e-3 * self.rhoc0)[don] & ok
            if sel.any():
                vmax_run = max(vmax_run, float(np.max(np.where(sel, v, 0.0))))
                pimax_run = max(pimax_run, float(np.max(np.where(sel, v * tau[don] / self.rf[1:N], 0.0))))
            if trackF:
                Fn = self.F(m); maxinc = max(maxinc, (Fn - Fprev) / F0); Fprev = Fn
            if n % 100 == 0:
                ts.append(t); Ss.append(Sin(m)); fronts.append(self.front(m)[0]); ffill.append(self.front(m, 0.999)[0])
                if stop and not unlimited and flux.sum() * GYR < 1e-7 * self.Mcat: break
                if unlimited and self.settled_front(m) > 1.2 * self.Mcat: break
        ts.append(t); Ss.append(Sin(m)); fronts.append(self.front(m)[0]); ffill.append(self.front(m, 0.999)[0])
        ts, Ss = np.array(ts), np.array(Ss)
        dlf = np.diff(np.log(np.array(ffill)))
        fr_half = np.array(fronts); jmax = int(np.argmax(fr_half))
        tgt = Ss[0] + 0.9 * (Ss[-1] - Ss[0])
        if Ss[-1] > Ss[0]:
            j = int(np.argmax(Ss >= tgt))
            t90 = float(ts[j] if j == 0 else ts[j - 1] + (tgt - Ss[j - 1]) / (Ss[j] - Ss[j - 1]) * (ts[j] - ts[j - 1]))
        else:
            t90 = float("nan")
        fr = np.array(fronts)
        dl = np.diff(np.log(fr)) if fr.size > 1 else np.array([0.0])
        return dict(m=m, t=t, n=n, t90=t90, S_final=self.settled_front(m), Sin_final=float(Ss[-1]), Sin0=float(Ss[0]),
                    maxinc=float(maxinc) if trackF else None, F0=F0, F_final=Fprev, front_min_dlog=float(dl.min()),
                    front_n_recede=int((dl < -1e-12).sum()), filled_front_min_dlog=float(dlf.min()),
                    filled_front_n_recede=int((dlf < -1e-12).sum()), front_overshoot=float(fr_half[jmax] / fr_half[-1]), c1=c1, vmax_run_kms=vmax_run / 1e3, Pi_max_run=pimax_run,
                    mass_err=float(abs(m.sum() - m0.sum()) / m0.sum()) if not unlimited else None)


def kkt(model, m):
    rho, d, Md, dpsi = model.fields(m)
    psi = model.psi_cells(Md, dpsi)
    q = np.where(model.rhoph > 1e-300, rho / np.maximum(model.rhoph, 1e-300), np.inf)
    filled = q >= 1 - 1e-3
    empty = rho <= 1e-6 * np.maximum(model.rhoph, 1e-300)
    _, _, i = model.front(m)
    lam = psi[min(i, model.N - 1)]
    vio = 0.0
    if filled.any(): vio = max(vio, float(np.max(psi[filled] - lam)))
    if empty.any(): vio = max(vio, float(np.max(lam - psi[empty])))
    return max(vio, 0.0) / float(np.max(np.abs(psi))), int(filled.sum()), int(empty.sum())


# ====================================================================================== groups (T2b)
def group_rows():
    rows = B.read_tian()
    return [o for o in rows if B.CLASS[o["sample"]] == "GROUPS"]


def group_pred(o, a0, mode, supply_factor=1.0):
    M = 10 ** o["lM"] * MSUN; a = o["Re"] * KPC / B.HERN_RE; GM = G * M; a0d = a0 * a * a / GM
    f = fret_census(10 ** o["lM"])[0]
    if mode == "noedge":
        xe = None
    elif mode == "census_pm":
        xe = (1.0 / math.sqrt(a0d)) / math.log1p(f * FB / (1 - FB))
    else:                                                          # class A exhaustion radius of the Hernquist round phantom
        rho, mm = B.prof("hern", B.X); gN = mm / B.X ** 2; g = B.nu(gN / a0d) * gN; mph = (g - gN) * B.X ** 2
        cap = COLD_PER_B / f * supply_factor
        k = np.where(mph >= cap)[0]
        if k.size == 0:
            xe = None
        else:
            k = int(k[0]); x1, x2 = B.LX[k - 1], B.LX[k]; y1, y2 = mph[k - 1], mph[k]
            xe = math.exp(x1 + (cap - y1) / (y2 - y1) * (x2 - x1))
    s2 = B.sigma2("hern", a0d, 0.0, None, xe) * GM / a
    return 0.5 * math.log10(s2) - 3.0, (xe / B.HERN_RE if xe else float("inf")), f


# ====================================================================================== main
def main():
    log(f"CFG541 {'MUTATE' if MUT else 'PRIMARY'}: cold-energy equations of motion made precise (CFG539 class A)")
    log("kappa = 1/2 FITTED; footings never pooled; cold energy mass required; not theory closed. Delta_ta(z=0) = %.4f" % DTA)
    rc_ok = True

    # ---------------- D1 / M3
    ok, aud, tau_syms = audit(hidden=MUT)
    RES["D1_audit"] = dict(pass_=ok, equations=aud, tau_symbols=tau_syms)
    log(f"\nD1 dimensional + constants audit{' (M3: hidden tau = T0 inserted)' if MUT else ''}: {'PASS' if ok else 'FAIL'}; "
        f"tau built from {tau_syms}")
    for k, v in aud.items():
        if not v["ok"]: log(f"   flagged: {k}: dims {v['dims_consistent']}, unlisted constants {v['unlisted_constants']}")

    if MUT:
        # M1, M2 on the MW-like Hernquist canonical model
        mod = Model(6.0e10, 2.5, FOOT["can"], fret_census(6.0e10)[0])
        r1 = mod.run(alpha=1.0, sign=-1, trackF=True, tmax=20 * GYR, stop=False, maxsteps=200000)
        m1 = r1["maxinc"] > 1e-3
        log(f"\nM1 sign-reversed drift: max step dF/F0 = {r1['maxinc']:+.3e} (F0 {r1['F0']:.3e} -> {r1['F_final']:.3e} J) -> "
            f"{'BITES (F increases)' if m1 else 'DOES NOT BITE'}")
        rstar = mod.analytic_rstar()
        r2 = mod.run(alpha=1.0, unlimited=True, tmax=600 * GYR)
        fr2 = mod.front(r2["m"])[1]
        m2 = (r2["S_final"] > 1.05 * mod.Mcat) and (fr2 > 1.05 * rstar)
        log(f"M2 unlimited reservoir: settled {r2['S_final'] / mod.Mcat:.3f} M_cat, front {fr2 / KPC:.1f} kpc vs r_* {rstar / KPC:.1f} kpc "
            f"(t = {r2['t'] / GYR:.1f} Gyr) -> {'BITES (cap broken)' if m2 else 'DOES NOT BITE'}")
        m3 = not ok
        log(f"M3 hidden constant: audit {'FLAGS it (BITES)' if m3 else 'misses it (DOES NOT BITE)'}")
        RES["MUTATE"] = dict(M1=dict(maxinc=r1["maxinc"], F0=r1["F0"], F_final=r1["F_final"], bites=bool(m1)),
                             M2=dict(settled_over_Mcat=r2["S_final"] / mod.Mcat, front_kpc=fr2 / KPC, rstar_kpc=rstar / KPC,
                                     t_Gyr=r2["t"] / GYR, bites=bool(m2)), M3=dict(bites=bool(m3)))
        allb = m1 and m2 and m3
        log(f"\nMUTATE: {'all three bite -> exit 1 (as designed)' if allb else 'NOT all bite -> exit 0 (teeth missing)'}")
        return 1 if allb else 0

    # ---------------- V1/V2
    vr = variational_sympy()
    RES["V1_V2"] = vr
    log("\nV1 first variation (3-cell sympy model): dF/drho_c = s psi on {d > 0}: "
        f"{'PASS' if vr['variational']['first_variation_is_s_psi'] and vr['committed']['first_variation_is_s_psi'] else 'FAIL'}; "
        f"at a filled cell the left derivative = psi ({vr['subgradient_at_filled_cell']['equals_psi3']}), right = 0 -> interval [psi, 0]")
    log(f"V2 gradient-flow test (response matrix dmu_i/drho_j symmetric?): VARIATIONAL form (s = f_sw catch, no edge) "
        f"{vr['variational']['response_matrix_symmetric']} -> {'IS' if vr['variational']['response_matrix_symmetric'] else 'IS NOT'} a gradient flow; "
        f"CFG539 COMMITTED form (edge in s, mobility on catch) {vr['committed']['response_matrix_symmetric']} -> "
        f"{'IS' if vr['committed']['response_matrix_symmetric'] else 'IS NOT'} a gradient flow")
    log(f"   committed-form response matrix: {vr['committed']['J']}")
    ly = lyapunov_sympy(); RES["V3_sympy"] = ly
    log(f"V3 sympy by-parts identity: {'PASS' if ly['by_parts_identity'] else 'FAIL'}; stationary condition alpha-free: "
        f"{ly['stationary_condition_alpha_free']} (solutions dpsi = {ly['stationary_solutions_dpsi']})")

    # ---------------- C2
    disp, scan, a0root = dispersion()
    RES["C2"] = dict(polynomials=disp, root_scan=scan, A0_root=a0root)
    log("\nC2 linear dispersion about a uniform state (units Gamma = 4 pi G rho_c tau = 1; q = Gamma tau = rho_c/rho_m; K = c k/Gamma; "
        "tau_psi = beta tau):")
    log(f"   A0 root: s = {a0root} (k-independent: no propagation, no k^2 diffusion)")
    for k_, v_ in disp.items():
        sc = scan[k_]
        st = "STABLE" if sc["max_Re_s_over_Gamma"] < 1e-9 else "UNSTABLE"
        log(f"   {k_}: monic coeffs {v_['coeffs_monic']}; Hurwitz {v_['hurwitz']}")
        log(f"      root scan max Re s/Gamma = {sc['max_Re_s_over_Gamma']:+.4e} at (K, q) = {sc['at_Kc_over_Gamma_q']} -> {st}"
            + (f"; beta scan {sc['beta_scan_max_Re']}" if sc['beta_scan_max_Re'] else ""))
        sc["label"] = st

    # ---------------- 1-D systems
    groups = group_rows()
    lMg = float(np.median([o["lM"] for o in groups])); Reg = float(np.median([o["Re"] for o in groups]))
    systems = {"MW": (6.0e10, 2.5), "group": (10 ** lMg, Reg / B.HERN_RE)}
    RES["systems"] = dict(MW=dict(Mb=6.0e10, a_kpc=2.5), group=dict(Mb=10 ** lMg, a_kpc=Reg / B.HERN_RE, median_lM=lMg, median_Re_kpc=Reg),
                          cluster=dict(Mb=1.5e14, a_kpc=None))
    log(f"\nSystems: MW-like M_b 6.0e10, a 2.5 kpc; group-like = CFG540 median (log M_b {lMg:.3f}, Re {Reg:.1f} kpc, a {Reg / B.HERN_RE:.1f} kpc); "
        "cluster-like 1.5e14 point mass (energy bound only)")
    one = {}
    for fk, a0 in FOOT.items():
        one[fk] = {}
        log(f"\n=== footing {fk} (a0 = {a0:.4e})")
        # T2a: point masses
        for nm, (Mb, _) in systems.items():
            f = fret_census(Mb)[0]
            mod = Model(Mb, None, a0, f)
            r = mod.run(alpha=1.0)
            rcen = mod.rM / math.log1p(f * FB / (1 - FB))
            fl, fs, _ = mod.front(r["m"]); ran = mod.analytic_rstar()
            kv, nf, ne = kkt(mod, r["m"])
            rec = dict(fret=f, rM_kpc=mod.rM / KPC, rta_kpc=mod.rta / KPC, Mcat_over_Mb=mod.Mcat / mod.Mb, r_census_kpc=rcen / KPC,
                       r_flow_literal_kpc=fl / KPC, r_flow_subcell_kpc=fs / KPC, r_analytic_kpc=ran / KPC,
                       literal_over_census=fl / rcen, subcell_over_census=fs / rcen, subcell_over_analytic=fs / ran,
                       front_min_dlog=r["front_min_dlog"], cell_dlog=float(np.log(mod.rf[1] / mod.rf[0])), kkt_violation=kv,
                       mass_err=r["mass_err"], t_end_Gyr=r["t"] / GYR, steps=r["n"], settled_over_Mcat=r["S_final"] / mod.Mcat,
                       front_n_recede=r["front_n_recede"], filled_front_min_dlog=r["filled_front_min_dlog"],
                       filled_front_n_recede=r["filled_front_n_recede"], front_overshoot=r["front_overshoot"])
            q0 = mod.rhoc0 / np.maximum(mod.rhoph, 1e-300); jj = np.where((mod.rc > ran) & (q0 >= 0.5))[0]
            rec["reservoir_q0_ge_half_from_over_rstar"] = float(mod.rf[jj[0]] / ran) if jj.size else None
            # disclosed resolution check (not in the frozen text): the same cell at N = 1600 (cell width 0.7% in r)
            mod4 = Model(Mb, None, a0, f, N=1600); r4 = mod4.run(alpha=1.0); fl4, fs4, _ = mod4.front(r4["m"])
            rec.update(N1600_literal_over_census=fl4 / rcen, N1600_subcell_over_census=fs4 / rcen, N1600_front_n_recede=r4["front_n_recede"],
                       N1600_front_min_dlog=r4["front_min_dlog"], N1600_cell_dlog=float(np.log(mod4.rf[1] / mod4.rf[0])))
            one[fk][nm + "_point"] = rec
            log(f"T2a {nm} point (f_ret {f:.3f}, M_cat {rec['Mcat_over_Mb']:.2f} M_b, r_M {rec['rM_kpc']:.2f}, r_ta {rec['rta_kpc']:.0f} kpc): "
                f"r_census {rec['r_census_kpc']:.2f}; flow literal {rec['r_flow_literal_kpc']:.2f} ({rec['literal_over_census']:.4f}), "
                f"sub-cell {rec['r_flow_subcell_kpc']:.2f} ({rec['subcell_over_census']:.4f}); analytic exhaustion {rec['r_analytic_kpc']:.2f}; "
                f"front min dlog {rec['front_min_dlog']:+.2e} (cell {rec['cell_dlog']:.3f}); KKT {kv:.1e}; |dM|/M {r['mass_err']:.1e}; "
                f"settled {rec['settled_over_Mcat']:.6f} M_cat; 0.5-front receded in {rec['front_n_recede']} samples (max front / final "
                f"{rec['front_overshoot']:.3f}); post-freeze filled front (q >= 0.999): min dlog {rec['filled_front_min_dlog']:+.2e}, receded in "
                f"{rec['filled_front_n_recede']} samples; the undrained reservoir already has rho_c0 >= rho_ph/2 beyond "
                f"{rec['reservoir_q0_ge_half_from_over_rstar']:.3f} r_*")
            log(f"    N = 1600 check: literal/census {rec['N1600_literal_over_census']:.4f}, sub-cell/census {rec['N1600_subcell_over_census']:.4f}, "
                f"front receded in {rec['N1600_front_n_recede']} samples (min dlog {rec['N1600_front_min_dlog']:+.2e}, cell {rec['N1600_cell_dlog']:.4f})")
        # Hernquist systems: V3 numerics, V4, V5, S0, C1
        for nm, (Mb, ah) in list(systems.items()) + [("cluster", (1.5e14, None))]:
            f = fret_census(Mb)[0]
            mod = Model(Mb, ah, a0, f)
            alphas = (0.5, 1.0, 2.0) if nm != "cluster" else (1.0,)
            runs = {}
            for al in alphas:
                runs[al] = mod.run(alpha=al, trackF=(al == 1.0))
            r = runs[1.0]
            ran = mod.analytic_rstar(); fl, fs, _ = mod.front(r["m"]); kv, nf, ne = kkt(mod, r["m"])
            prof = {al: np.cumsum(rr["m"]) / mod.Mcat for al, rr in runs.items()}
            dprof = max(float(np.max(np.abs(prof[al] - prof[1.0]))) for al in prof)
            m0 = mod.rhoc0 * mod.V
            Wi, Ki = mod.energy(m0); Wf, Kf = mod.energy(r["m"])
            dW = Wi - Wf; Esink = dW - Kf
            Fi, Ff = mod.F(m0), mod.F(r["m"])
            Ms = r["S_final"]
            rec = dict(fret=f, rM_kpc=mod.rM / KPC, rta_kpc=mod.rta / KPC, Mcat_over_Mb=mod.Mcat / mod.Mb, Vf_kms=math.sqrt(mod.Vf2) / 1e3,
                       r_analytic_kpc=ran / KPC, r_flow_literal_kpc=fl / KPC, r_flow_subcell_kpc=fs / KPC, subcell_over_analytic=fs / ran,
                       r_census_pm_kpc=mod.rM / math.log1p(f * FB / (1 - FB)) / KPC, kkt_violation=kv, n_filled=nf, n_empty=ne,
                       V3_max_step_dF_over_F0=r["maxinc"], F0=r["F0"], mass_err=r["mass_err"], rhoph_neg_cells=mod.rhoph_neg_cells,
                       t90_Gyr={str(al): rr["t90"] / GYR for al, rr in runs.items()},
                       t_end_Gyr={str(al): rr["t"] / GYR for al, rr in runs.items()}, alpha_profile_maxdiff=dprof,
                       front_min_dlog=r["front_min_dlog"], cell_dlog=float(np.log(mod.rf[1] / mod.rf[0])),
                       dW_per_mass=dW / mod.Mcat, Kf_per_mass=Kf / mod.Mcat, Esink_per_mass=Esink / mod.Mcat,
                       dW_over_Vf2=dW / mod.Mcat / mod.Vf2, Esink_over_Vf2=Esink / mod.Mcat / mod.Vf2, Kf_over_Vf2=Kf / mod.Mcat / mod.Vf2,
                       dF_J=Fi - Ff, dF_over_dW=(Fi - Ff) / dW, Esink_over_Kf=Esink / Kf, settled_over_Mcat=Ms / mod.Mcat,
                       Esink_J=Esink, Kb_J=0.75 * mod.Vf2 * mod.Mb, C1=r["c1"], vmax_run_kms=r["vmax_run_kms"],
                       Pi_max_run=r["Pi_max_run"], front_n_recede=r["front_n_recede"], front_overshoot=r["front_overshoot"],
                       filled_front_min_dlog=r["filled_front_min_dlog"], filled_front_n_recede=r["filled_front_n_recede"])
            # local injected energy density at r_M (final cold density there)
            rhoc_rM = float(np.interp(math.log(mod.rM), np.log(mod.rc), r["m"] / mod.V))
            rec["rhoc_at_rM"] = rhoc_rM
            rec["e_over_c2"] = rec["Esink_per_mass"] / c ** 2
            one[fk][nm] = rec
            log(f"{nm} Hernquist{'' if ah else '(point)'} (f_ret {f:.3f}, M_cat {rec['Mcat_over_Mb']:.2f} M_b, V_f {rec['Vf_kms']:.1f} km/s, "
                f"r_ta {rec['rta_kpc']:.0f} kpc):")
            log(f"   V4 r_* analytic {ran / KPC:.2f} kpc, flow sub-cell {fs / KPC:.2f} ({rec['subcell_over_analytic']:.4f}), literal {fl / KPC:.2f}; "
                f"point-mass census {rec['r_census_pm_kpc']:.2f}; KKT violation {kv:.1e} (filled {nf}, empty {ne}); front min dlog {r['front_min_dlog']:+.2e} (receded in {r['front_n_recede']} samples, max/final {r['front_overshoot']:.3f}); filled front receded in {r['filled_front_n_recede']} samples")
            log(f"   V3 max step dF/F0 {r['maxinc']:+.2e}; |dM|/M {r['mass_err']:.1e}; negative-rho_ph cells {mod.rhoph_neg_cells}")
            log(f"   V5 t_90 [Gyr] " + ", ".join(f"alpha {k}: {v:.2f}" for k, v in rec["t90_Gyr"].items()) +
                f"; steady profiles max|dM_c(<r)|/M_cat across alpha {dprof:.1e}")
            log(f"   S0 per settled mass: dW {dW / mod.Mcat / 1e6:.0f} km^2/s^2 ({rec['dW_over_Vf2']:.3f} V_f^2), K_f {rec['Kf_over_Vf2']:.3f} V_f^2, "
                f"E_sink {rec['Esink_over_Vf2']:.3f} V_f^2; E_sink/K_f {rec['Esink_over_Kf']:.3f}; dF/dW {rec['dF_over_dW']:.3f}")
            log(f"   C1 t=0 max|v_s| {r['c1']['max_vs_kms']:.1f} km/s at {r['c1']['r_at_max_kpc']:.0f} kpc: /c {r['c1']['max_vs_over_c']:.2e}, "
                f"/V_c {r['c1']['max_vs_over_Vc']:.3f}; run max over cells with rho_c >= 1e-3 rho_c0: {r['vmax_run_kms']:.1f} km/s")
            log(f"   post-freeze diag: overdamped-consistency Pi = |v_s| tau/r: t=0 max {r['c1']['max_Pi']:.2f} at {r['c1']['r_at_maxPi_kpc']:.0f} kpc; "
                f"run max {r['Pi_max_run']:.2f} (overdamped reading needs Pi << 1)")
    RES["one_d"] = one

    # ---------------- labels: V3, V4, V5, T2a
    hs = [one[f][n] for f in FOOT for n in ("MW", "group", "cluster")]
    ps = [one[f][n + "_point"] for f in FOOT for n in ("MW", "group")]
    v3 = all(x["V3_max_step_dF_over_F0"] <= 1e-9 for x in hs)
    v4 = all(abs(x["subcell_over_analytic"] - 1) <= 0.01 and x["kkt_violation"] <= 1e-6 for x in hs + ps)
    v4_lit = all(abs(x["r_flow_literal_kpc"] / x["r_analytic_kpc"] - 1) <= 0.01 for x in hs + ps)
    v5_stat = all(x["alpha_profile_maxdiff"] <= 1e-3 for x in hs if "0.5" in x["t90_Gyr"])
    v5_rob = all(x["t90_Gyr"]["0.5"] < 10.0 for x in hs if "0.5" in x["t90_Gyr"])
    t2a_lit = all(abs(x["literal_over_census"] - 1) <= 0.01 for x in ps)
    t2a_sub = all(abs(x["subcell_over_census"] - 1) <= 0.01 for x in ps)
    inside_out = all(x["front_min_dlog"] >= -1e-12 for x in ps)
    inside_out_1600 = all(x["N1600_front_min_dlog"] >= -1e-12 for x in ps)
    filled_mono = all(x["filled_front_n_recede"] == 0 for x in ps + hs)
    t2a_lit1600 = all(abs(x["N1600_literal_over_census"] - 1) <= 0.01 for x in ps)
    RES["labels"] = dict(V3_numeric=v3, V4=v4, V4_literal_face=v4_lit, V5_stationary_alpha_free=v5_stat,
                         V5_coefficient="O(1) FREE", V5_robustness="ROBUST (idealised)" if v5_rob else "RATE-SENSITIVE",
                         T2a_literal_face=t2a_lit, T2a_subcell=t2a_sub, T2a_inside_out=inside_out,
                         T2a_literal_face_N1600=t2a_lit1600, T2a_inside_out_N1600=inside_out_1600,
                         T2a_postfreeze_filled_front_monotone=filled_mono,
                         T2a="EMERGENT" if (t2a_lit and inside_out) else "NOT EMERGENT BY THE FROZEN RULE")
    log(f"\nV3 numeric Lyapunov (max step dF/F0 <= 1e-9, all Hernquist/cluster runs at alpha = 1): {'PASS' if v3 else 'FAIL'}")
    log(f"V4 minimiser (sub-cell r_* within 1% of the analytic inside-out fill, KKT <= 1e-6): {'PASS' if v4 else 'FAIL'}; "
        f"literal-face reading within 1%: {v4_lit}")
    log(f"V5 stationary states alpha-free (profiles <= 1e-3): {'PASS' if v5_stat else 'FAIL'}; coefficient: O(1) FREE; robustness "
        f"(t_90(alpha 0.5) < 10 Gyr everywhere): {RES['labels']['V5_robustness']}")
    log(f"T2a: literal face within 1% of census in every point cell: {t2a_lit}; sub-cell within 1%: {t2a_sub}; inside-out (front never "
        f"recedes, point cells): {inside_out}; N = 1600 check: literal within 1% {t2a_lit1600}, inside-out {inside_out_1600}")
    log(f"T2a frozen label: {RES['labels']['T2a']}; post-freeze filled-front (q >= 0.999) monotone in every run: {filled_mono}")

    # ---------------- T2b groups
    out_g = {}
    for fk, a0 in FOOT.items():
        D = {m: [] for m in ("census_pm", "classA", "noedge")}; xr = []
        ls = np.array([o["ls"] for o in groups])
        for o in groups:
            for mde in D:
                lp, xe, f = group_pred(o, a0, mde)
                D[mde].append(lp)
                if mde == "classA": xr.append(xe)
        res_ = {}
        for mde, lp in D.items():
            dd = ls - np.array(lp)
            res_[mde] = dict(mean=float(dd.mean()), se=float(dd.std(ddof=1) / math.sqrt(len(dd))))
        xr = np.array(xr)
        scanf = {}
        for sf in (1.5, 2.0, 3.0, 5.0, 10.0, 20.0, 50.0):
            dd = ls - np.array([group_pred(o, a0, "classA", sf)[0] for o in groups])
            scanf[str(sf)] = float(dd.mean())
        need = next((float(k) for k, v in scanf.items() if abs(v) < 0.042), None)
        out_g[fk] = dict(N=len(groups), modes=res_, rstar_over_Re_median=float(np.median(xr[np.isfinite(xr)])),
                         rstar_over_Re_range=[float(np.min(xr)), float(np.max(xr[np.isfinite(xr)]))], supply_scan_mean=scanf,
                         supply_factor_needed=need)
        log(f"\nT2b groups ({fk}, N {len(groups)}): census point-mass edge (CFG540 identity) {res_['census_pm']['mean']:+.4f} +- {res_['census_pm']['se']:.3f}; "
            f"class-A exhaustion edge {res_['classA']['mean']:+.4f} +- {res_['classA']['se']:.3f}; no edge {res_['noedge']['mean']:+.4f}")
        log(f"   class-A r_*/Re median {out_g[fk]['rstar_over_Re_median']:.2f} (range {out_g[fk]['rstar_over_Re_range'][0]:.2f}-"
            f"{out_g[fk]['rstar_over_Re_range'][1]:.2f}); supply scan mean Delta {scanf}; factor for |Delta| < 0.042: {need}")
    cfg540 = json.load(open(os.path.join(HERE, "..", "CFG540_vizier2026_bfjr_mhongoose", "cfg540_bfjr_results.json")))
    RES["T2b"] = out_g
    mcan = out_g["can"]["modes"]["classA"]["mean"]
    t2b = "PROBLEM PERSISTS" if mcan >= 0.063 else ("RESOLVED" if abs(mcan) < 0.042 else "REDUCED")
    RES["labels"]["T2b"] = t2b
    log(f"T2b label (can mean {mcan:+.3f}): {t2b}")
    idg = {}
    for fk in FOOT:                                               # identity: CFG540's estimator at CFG540's own footing values
        ls_ = np.array([o["ls"] for o in groups])
        lp_ = np.array([group_pred(o, B.FOOT[fk], "census_pm")[0] for o in groups])
        idg[fk] = abs(float((ls_ - lp_).mean()) - cfg540["footings"][fk]["runs"]["beta+0.0"]["classes"]["GROUPS"]["mean"])
    RES["T2b_identity_vs_CFG540_json"] = idg
    log(f"T2b identity control (census point-mass edge vs CFG540 JSON group mean): |diff| {idg} -> "
        f"{'PASS' if max(idg.values()) < 1e-6 else 'FAIL'}")
    rc_ok &= max(idg.values()) < 1e-6

    # ---------------- S labels
    worst = max(math.log10(1 + one[f][n]["Esink_over_Kf"]) for f in FOOT for n in ("MW", "group") if one[f][n]["Esink_over_Kf"] > -1)
    neg = any(one[f][n]["Esink_per_mass"] < 0 for f in FOOT for n in ("MW", "group"))
    s1 = "SOURCE NEEDED" if neg else ("EXCLUDED" if worst > 0.1 else "ALLOWED")
    OmC = OM * (1 - FB)
    emax = max(one[f][n]["e_over_c2"] for f in FOOT for n in ("MW", "group", "cluster"))
    drr = OmC / OL * emax; dla0 = 0.5 * math.log10(1 + drr)
    loc = {}
    for f, a0 in FOOT.items():
        rDE = (a0 / (KAPPA * c)) ** 2 / G
        for n in ("MW", "group"):
            x = one[f][n]
            xa = x["rhoc_at_rM"] * x["Esink_per_mass"] / (rDE * c ** 2)
            xb = xa * (x["rM_kpc"] * KPC / c) / (x["t90_Gyr"]["1.0"] * GYR)
            loc[f"{f}_{n}"] = dict(rho_DE=rDE, x_stay=xa, da0_stay=math.sqrt(1 + xa) - 1, x_leave_c=xb, da0_leave=math.sqrt(1 + xb) - 1)
    s2b = all(v["da0_leave"] < 1e-3 for v in loc.values()); s2a = all(v["da0_stay"] < 1e-3 for v in loc.values())
    s2 = "ALLOWED" if (dla0 < 0.004 and s2b) else ("EXCLUDED" if dla0 > 0.04 else "UNDECIDED")
    gw = {}
    for f in FOOT:
        for n in ("MW", "group", "cluster"):
            x = one[f][n]; t90 = x["t90_Gyr"]["1.0"] * GYR; Mc = x["Mcat_over_Mb"] * RES["systems"][n]["Mb"] * MSUN
            rs = x["r_analytic_kpc"] * KPC
            Pgw = G / (5 * c ** 5) * (Mc * rs ** 2 / t90 ** 3) ** 2; Preq = x["Esink_J"] / t90
            gw[f"{f}_{n}"] = Pgw / Preq
    s3 = "EXCLUDED" if max(gw.values()) < 1e-3 else ("NOT EXCLUDED BY THE 1e-3 RULE (but < 1: cannot carry the sink)"
                                                     if max(gw.values()) < 1 else "ALLOWED")
    s4 = {f"{f}_{n}": one[f][n]["Esink_J"] / one[f][n]["Kb_J"] for f in FOOT for n in ("MW", "group")}
    RES["S"] = dict(i=dict(label=s1, worst_log10_sigma2_ratio=worst),
                    ii=dict(label=s2, cosmic_drho_over_rho=drr, cosmic_dlog10_a0=dla0, e_over_c2_max=emax, local=loc,
                            local_stay_label="ALLOWED" if s2a else "EXCLUDED", local_leave_label="ALLOWED" if s2b else "EXCLUDED",
                            conditions=["exact Lambda (w = -1) cannot exchange energy: requires dynamical dark energy",
                                        "exchange coupling Q not derived (open item)"]),
                    iii=dict(label=s3, EM="EXCLUDED (no EM coupling)", Pgw_over_Preq=gw),
                    iv=dict(label="EXCLUDED (G9: the drift force is not gravitational)", Esink_over_Kb=s4))
    log(f"\nS(i) heat in the cold energy: worst log10(1 + E_sink/K_f) = {worst:.3f} -> {s1}")
    log(f"S(ii) dark-energy exchange: max e/c^2 {emax:.2e}; cosmic Delta rho_DE/rho_DE {drr:.2e}, Delta log10 a0 {dla0:.2e} dex; local "
        + "; ".join(f"{k}: stay {v['da0_stay']:.2e}, leave-at-c {v['da0_leave']:.2e}" for k, v in loc.items())
        + f" -> {s2} (clustering-DE case: {RES['S']['ii']['local_stay_label']}); conditions: exact Lambda cannot exchange; Q not derived")
    log(f"S(iii) radiation: EM EXCLUDED (dark); GW P/P_req max {max(gw.values()):.1e} -> {s3}")
    log("S(iv) baryons: EXCLUDED by G9; E_sink/K_b " + ", ".join(f"{k} {v:.1f}" for k, v in s4.items()))

    # ---------------- C labels
    c1 = all(one[f][n]["C1"]["max_vs_over_c"] < 1e-2 for f in FOOT for n in ("MW", "group", "cluster"))
    stab = {k: scan[k]["label"] for k in scan}
    caus = "CAUSAL-WITH-tau" if stab["A2 damped wave"] == "STABLE" else ("ACAUSAL" if stab["A1 undamped wave"] != "STABLE" else "CAUSAL-WITH-tau")
    RES["labels"].update(C1_subluminal=c1, C2_stability=stab, causality=caus,
                         undamped_retarded=stab["A1 undamped wave"])
    log(f"\nC1 subluminal (max|v_s|/c < 1e-2): {c1}.  C2 stability: {stab}")
    log(f"Causality label: {caus} (undamped retarded psi: {stab['A1 undamped wave']})")
    RES["labels"]["overall"] = "SPECIFIED WITH OPEN ITEMS" if RES["D1_audit"]["pass_"] else "INCONSISTENT"
    log(f"\nOverall (E1, with the open items listed in EQUATIONS.md): {RES['labels']['overall']}")
    return 0 if rc_ok else 1


if __name__ == "__main__":
    rc = main()
    with open(os.path.join(HERE, f"cfg541{TAG}.out"), "w") as fh:
        fh.write("\n".join(OUT) + "\n")
    with open(os.path.join(HERE, f"cfg541_results{TAG}.json"), "w") as fh:
        json.dump(RES, fh, indent=1, default=lambda o: o.tolist() if hasattr(o, "tolist") else str(o))
    sys.exit(rc)
