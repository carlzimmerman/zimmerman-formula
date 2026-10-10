#!/usr/bin/env python3
"""CFG544: kinetic consistency of class-A settling (CFG541 open item 5). FROZEN_CRITERIA.md (committed alone first, b6eb542c5).

Sympy (moments of the class-A kinetic equation, two-sided deficit variation, velocity relaxation, full-system Lyapunov candidates)
plus a spherical N-body shell toy (no PM) and a 1-D drift-only finite-volume model (CFG541's setup, re-implemented).
kappa = 1/2 FITTED; footings 9.3603e-11 / 1.1312e-10 never pooled; cold energy mass required; not "theory closed".
Inputs read only from ../CFG541_cold_energy_equations_precise/cfg541_results.json.
CFG544_MUTATE=1 -> MV (sigma^2 x 2 at settling), MO (overfill with the one-sided rule as the 'fix'), MT (OU target x 2).
Run: OMP_NUM_THREADS=2 nice -n 10 python3 cfg544.py
"""
import os, sys, json, math, time
os.environ.setdefault("OMP_NUM_THREADS", "1")
import numpy as np
import sympy as sp
from multiprocessing import Pool

HERE = os.path.dirname(os.path.abspath(__file__))
MUT = os.environ.get("CFG544_MUTATE", "0") == "1"
TAG = "_MUTATE" if MUT else ""
G_SI, MSUN, KPC, GYR = 6.674e-11, 1.989e30, 3.0857e19, 3.15576e16
FOOT = {"can": 9.3603e-11, "alt": 1.1312e-10}
J541 = json.load(open(os.path.join(HERE, "..", "CFG541_cold_energy_equations_precise", "cfg541_results.json")))
SYS = {"MW": dict(Mb=6.0e10, a_kpc=2.5), "cluster": dict(Mb=1.5e14, a_kpc=None)}
NPART, EPS, RMIN, NB, ALPHA, SEED = 30000, 0.01, 1e-3, 100, 1.0, 544
DT = {"MW": 1e-3, "cluster": 5e-4}
OUT, RES = [], {"lane": "CFG544", "mutate": MUT, "settings": dict(kappa=0.5, footings=FOOT, N=NPART, eps_over_rstar=EPS,
                                                                     rmin_over_rstar=RMIN, nbins=NB, alpha=ALPHA, seed=SEED,
                                                                     dt_code=DT, inputs="CFG541 cfg541_results.json (read only)")}


def log(s=""):
    print(s, flush=True); OUT.append(s)


def nu_m1(y):
    with np.errstate(over="ignore", divide="ignore", invalid="ignore"):
        return 1.0 / np.expm1(np.sqrt(y))


# ----------------------------------------------------------------------------------------------------------------- cells
def make_cell(sysname, foot):
    s = SYS[sysname]; j = J541["one_d"][foot][sysname]; a0 = FOOT[foot]
    Mb = s["Mb"] * MSUN
    Vf = (G_SI * Mb * a0) ** 0.25
    rstar_kpc = j["r_analytic_kpc"]; rstar = rstar_kpc * KPC
    rM = math.sqrt(G_SI * Mb / a0)
    c = dict(sys=sysname, foot=foot, Vf_kms=Vf / 1e3, rstar_kpc=rstar_kpc, fret=j["fret"],
             Mb=rM / rstar, a=(None if s["a_kpc"] is None else s["a_kpc"] / rstar_kpc),
             rta=j["rta_kpc"] / rstar_kpc, Mcat=j["Mcat_over_Mb"] * rM / rstar, tu_Gyr=rstar / Vf / GYR, dt=DT[sysname],
             Vf2_SI=Vf ** 2, rstar_SI=rstar)
    return c


def Mb_enc(c, r):
    r = np.asarray(r, float)
    if c["a"] is None:
        return np.full_like(r, c["Mb"])
    return c["Mb"] * r ** 2 / (r + c["a"]) ** 2


def Mph_enc(c, r):
    mb = Mb_enc(c, r)
    y = mb * c["Mb"] / np.asarray(r, float) ** 2          # code units: a0 = V_f^2/r_M = 1/M_b
    return mb * nu_m1(y)


def phi_b_grid(c):
    rg = np.geomspace(1e-5, 1e4, 20001)
    g = Mb_enc(c, rg) * rg / (rg ** 2 + EPS ** 2) ** 1.5
    tail = -c["Mb"] / math.sqrt(rg[-1] ** 2 + EPS ** 2)
    seg = 0.5 * (g[1:] + g[:-1]) * np.diff(rg)
    phi = np.concatenate([tail - np.cumsum(seg[::-1])[::-1], [tail]])
    return rg, phi


def jeans_trunc(c, rgrid=None, soft=True, rmax=1.0):
    """isotropic Jeans dispersion of rho_ph in the law's field, truncated at rmax (P(rmax) = 0)."""
    r = np.geomspace(RMIN * 0.5, rmax, 4001) if rgrid is None else rgrid
    Mph = Mph_enc(c, r); rho = np.gradient(Mph, r) / (4 * math.pi * r ** 2)
    Mt = Mb_enc(c, r) + Mph
    g = Mt * r / (r ** 2 + EPS ** 2) ** 1.5 if soft else Mt / r ** 2
    f = rho * g
    P = np.concatenate([np.cumsum((0.5 * (f[1:] + f[:-1]) * np.diff(r))[::-1])[::-1], [0.0]])
    return r, rho, P / np.maximum(rho, 1e-300)


# ----------------------------------------------------------------------------------------------------------------- toy
class Toy:
    def __init__(self, c, rule, ou=False, ou_scale=1.0, drift=True):
        self.c, self.rule, self.ou, self.ou_scale, self.drift = c, rule, ou, ou_scale, drift
        self.rf = np.geomspace(RMIN, c["rta"], NB + 1)
        self.V = 4 * math.pi / 3 * np.diff(self.rf ** 3); self.rc = np.sqrt(self.rf[1:] * self.rf[:-1])
        self.dr = np.diff(self.rf)
        self.rhob = np.diff(Mb_enc(c, self.rf)) / self.V if c["a"] is not None else np.zeros(NB)
        self.rhoph = np.maximum(np.diff(Mph_enc(c, self.rf)), 0.0) / self.V
        self.rhoph_neg = int((np.diff(Mph_enc(c, self.rf)) < 0).sum())
        self.rg, self.phib = phi_b_grid(c)
        rj, _, s2 = jeans_trunc(c)
        self.rj, self.s2eq = rj, s2
        self.n_lim = 0; self.n_mv = 0

    def gravity(self, r):
        idx = np.argsort(r, kind="stable"); rank = np.empty(r.size); rank[idx] = np.arange(r.size)
        Menc = Mb_enc(self.c, r) + self.m * rank
        return Menc * r / (r ** 2 + EPS ** 2) ** 1.5, rank

    def energy(self, r, vr, L):
        g, rank = self.gravity(r)
        K = 0.5 * self.m * np.sum(vr ** 2 + (L / r) ** 2)
        Wcc = -np.sum(self.m * self.m * rank / np.sqrt(r ** 2 + EPS ** 2))
        Wcb = self.m * np.sum(np.interp(r, self.rg, self.phib))
        return K, Wcc + Wcb

    def drift_step(self, r, dt, g):
        c = self.c
        inside = r < c["rta"]
        mc = self.m * np.histogram(r, self.rf)[0]
        rho = mc / self.V
        d = (self.rhoph - rho) if self.rule == "two" else np.maximum(self.rhoph - rho, 0.0)
        Md = np.concatenate([[0.0], np.cumsum(d * self.V)])
        k = np.clip(np.searchsorted(self.rf, r) - 1, 0, NB - 1)
        dpsi = np.interp(r, self.rf, Md) / r ** 2
        tau = 1.0 / np.sqrt(4 * math.pi * (self.rhob + rho))[k]
        vs = np.where(inside, -ALPHA * tau * dpsi, 0.0)
        dx = vs * dt; lim = 0.5 * self.dr[k]
        over = np.abs(dx) > lim
        self.n_lim += int((over & inside).sum()); self.n_mv += int(inside.sum())
        dx = np.clip(dx, -lim, lim)
        rn = r + dx
        rn = np.where(rn < RMIN, 2 * RMIN - rn, rn)
        work = self.m * np.sum(g * (rn - r))                 # first-order potential-energy change of the drift
        return rn, work

    def ou_step(self, r, vr, vt, dt, g, rng):
        c = self.c
        mc = self.m * np.histogram(r, self.rf)[0]; rho = mc / self.V
        Menc_c = Mb_enc(c, self.rc) + np.concatenate([[0.0], np.cumsum(mc)[:-1]]) + 0.5 * mc
        gb = Menc_c * self.rc / (self.rc ** 2 + EPS ** 2) ** 1.5
        fP = rho * gb * self.dr
        Pf = np.concatenate([np.cumsum(fP[::-1])[::-1], [0.0]])
        Pc = 0.5 * (Pf[1:] + Pf[:-1])
        s2J = np.where(rho > 0, Pc / np.maximum(rho, 1e-300), 0.0) * self.ou_scale
        k = np.clip(np.searchsorted(self.rf, r) - 1, 0, NB - 1)
        inside = r < c["rta"]
        gam = ALPHA * np.sqrt(4 * math.pi * (self.rhob + rho))[k]
        a = np.exp(-gam * dt); b = np.sqrt(s2J[k] * (1 - a ** 2))
        K0 = 0.5 * self.m * np.sum(vr ** 2 + vt ** 2)
        x1, x2, x3 = rng.standard_normal((3, r.size))
        vr_n = np.where(inside, a * vr + b * x1, vr)
        vtx = a * vt + b * x2; vty = b * x3
        vt_n = np.where(inside, np.hypot(vtx, vty), vt)
        K1 = 0.5 * self.m * np.sum(vr_n ** 2 + vt_n ** 2)
        return vr_n, vt_n, K1 - K0

    def diag(self, r, vr, L):
        c = self.c
        vt = L / r
        sh = (r > 0.1) & (r < 0.9)
        s2e = np.interp(r[sh], self.rj, self.s2eq)
        X = float(np.sum(vr[sh] ** 2 + vt[sh] ** 2) / 3 / np.sum(s2e)) if sh.sum() > 10 else float("nan")
        be = np.geomspace(0.1, 0.9, 17)
        mc = self.m * np.histogram(r, be)[0]; Vb = 4 * math.pi / 3 * np.diff(be ** 3)
        rph = np.diff(Mph_enc(c, be)) / Vb
        D_bins = np.log10(np.maximum(mc / Vb, 1e-300) / rph)
        D = float(np.median(D_bins))
        s_bins = []
        for i in range(16):
            mk = (r >= be[i]) & (r < be[i + 1])
            if mk.sum() < 20: s_bins.append(float("nan")); continue
            s2m = (np.var(vr[mk]) + np.mean(vt[mk] ** 2)) / 3
            s_bins.append(float(s2m / np.interp(math.sqrt(be[i] * be[i + 1]), self.rj, self.s2eq)))
        beta = 1 - np.mean(vt[sh] ** 2) / (2 * np.var(vr[sh])) if sh.sum() > 10 else float("nan")
        mcin = self.m * np.sum(r < 1.0)
        r99 = float(np.quantile(r, 0.99))
        return dict(X=X, logX=float(np.log10(X)) if X > 0 else -99.0, D=D, D_bins=D_bins.tolist(), s_bins=s_bins,
                    beta=float(beta), Mc_in_rstar_over_Mph=float(mcin / Mph_enc(c, np.array([1.0]))[0]),
                    excess_in_rstar=float(mcin - Mph_enc(c, np.array([1.0]))[0]), r99=r99,
                    frac_beyond_rta=float(np.mean(r > c["rta"])))


def vlasov_step(toy, r, vr, L, dt, eta=0.03, nmax=4096):
    """Vlasov sub-step: kick-drift-kick in the frozen enclosed-mass profile of this step, with per-particle power-of-two
    substeps (individual time steps; correction 1, dated 2026-10-09)."""
    rs = np.sort(r); m = toy.m; c = toy.c
    def acc(rr, LL):
        Me = Mb_enc(c, rr) + m * np.searchsorted(rs, rr)
        return LL ** 2 / rr ** 3 - Me * rr / (rr ** 2 + EPS ** 2) ** 1.5, Me
    _, Me = acc(r, L)
    v = np.sqrt(vr ** 2 + (L / r) ** 2) + 1e-12
    tdyn = np.minimum(np.sqrt((r ** 2 + EPS ** 2) ** 1.5 / np.maximum(Me, 1e-30)), np.maximum(r, EPS) / v)
    lev = np.clip(np.ceil(np.log2(np.maximum(dt / (eta * tdyn), 1.0))), 0, int(math.log2(nmax))).astype(int)
    r = r.copy(); vr = vr.copy()
    for l in np.unique(lev):
        k = np.where(lev == l)[0]; n = 2 ** l; h = dt / n
        rr, vv, LL = r[k], vr[k], L[k]
        a, _ = acc(rr, LL)
        for _ in range(n):
            vv = vv + 0.5 * h * a
            rr = rr + h * vv
            neg = rr < RMIN
            rr = np.where(neg, 2 * RMIN - rr, rr); vv = np.where(neg, -vv, vv)
            a, _ = acc(rr, LL)
            vv = vv + 0.5 * h * a
        r[k], vr[k] = rr, vv
    return r, vr, int(2 ** lev.max())


def sample_ph(c, n, rmax, rng):
    rg = np.geomspace(RMIN, rmax, 20001); M = Mph_enc(c, rg); M = M - M[0]
    return np.interp(rng.random(n) * M[-1], M, rg)


def make_ic(c, ic, rng, sig2_scale=1.0, inject=False):
    m = c["Mcat"] / NPART
    if ic == "B":
        u = rng.random(NPART); r = np.maximum(c["rta"] * u ** (1 / 3), RMIN * 1.01)
        vr, vtx, vty = 0.05 * rng.standard_normal((3, NPART))
    else:
        r = sample_ph(c, NPART, 1.0, rng)
        if ic == "C":
            vr, vtx, vty = 0.05 * rng.standard_normal((3, NPART))
        else:
            rj, _, s2 = jeans_trunc(c)
            s = np.sqrt(np.interp(r, rj, s2) * sig2_scale)
            vr, vtx, vty = s * rng.standard_normal((3, NPART))
        if inject:
            Mi = 0.3 * float(Mph_enc(c, np.array([0.3]))[0] - Mph_enc(c, np.array([RMIN]))[0])
            ni = int(round(Mi / m))
            ri = sample_ph(c, ni, 0.3, rng)
            rj, _, s2 = jeans_trunc(c)
            si = np.sqrt(np.interp(ri, rj, s2))
            r = np.concatenate([r, ri])
            vr = np.concatenate([vr, si * rng.standard_normal(ni)])
            vtx = np.concatenate([vtx, si * rng.standard_normal(ni)]); vty = np.concatenate([vty, si * rng.standard_normal(ni)])
    vt = np.hypot(vtx, vty)
    return r, vr, r * vt, m


def run(job):
    c, name, ic, rule, ou, T_Gyr = job["c"], job["name"], job["ic"], job["rule"], job["ou"], job["T"]
    rng = np.random.default_rng(SEED)
    r, vr, L, m = make_ic(c, ic, rng, sig2_scale=job.get("sig2", 1.0), inject=job.get("inject", False))
    toy = Toy(c, rule, ou=ou, ou_scale=job.get("ou_scale", 1.0), drift=(rule != "none")); toy.m = m
    n0 = r.size
    dt = c["dt"]; nsteps = int(round(T_Gyr / (dt * c["tu_Gyr"])))
    every = max(1, int(round(0.25 / (dt * c["tu_Gyr"]))))
    K0, W0 = toy.energy(r, vr, L)
    W_drift = 0.0; W_ou = 0.0; Wd_in = 0.0; Wd_out = 0.0
    snaps = []
    t0 = time.time()
    nsub_max = 0
    for it in range(nsteps + 1):
        if it % every == 0 or it == nsteps:
            dg = toy.diag(r, vr, L); K, W = toy.energy(r, vr, L)
            dg.update(t_Gyr=it * dt * c["tu_Gyr"], E=K + W, K=K, W=W, sink_cum_over_Vf2Mcat=-(W_drift + W_ou) / c["Mcat"],
                      drift_work=W_drift, ou_work=W_ou, integ_err=(K + W - K0 - W0 - W_drift - W_ou) / abs(K0 + W0))
            snaps.append(dg)
        if it == nsteps: break
        r, vr, ns = vlasov_step(toy, r, vr, L, dt)
        nsub_max = max(nsub_max, ns)
        if toy.drift:
            vt = L / r
            g, _ = toy.gravity(r)
            _, Wb = toy.energy(r, vr, L)
            rn, _w = toy.drift_step(r, dt, g)
            Ln = rn * vt
            _, Wa = toy.energy(rn, vr, Ln)
            W_drift += Wa - Wb                                  # exact: the drift keeps (v_r, v_t), so only W changes
            L = Ln; r = rn
            if toy.ou:
                vr, vt, dk = toy.ou_step(r, vr, vt, dt, g, rng)
                W_ou += dk; L = r * vt
    E0 = K0 + W0
    fin = snaps[-1]
    # steadiness over the last 2 Gyr
    tl = fin["t_Gyr"] - 2.0
    ref = min(snaps, key=lambda s: abs(s["t_Gyr"] - tl))
    res = dict(name=name, sys=c["sys"], foot=c["foot"], ic=ic, rule=rule, ou=ou, T_Gyr=T_Gyr, steps=nsteps,
               n_particles=n0, n_final=int(r.size), mass_exact=bool(r.size == n0),
               dE_over_E=float((fin["E"] - E0) / abs(E0)), final=fin, d_logX_last2=float(fin["logX"] - ref["logX"]),
               d_D_last2=float(fin["D"] - ref["D"]), limited_frac=toy.n_lim / max(toy.n_mv, 1),
               series=[dict(t=s["t_Gyr"], logX=s["logX"], D=s["D"], Min=s["Mc_in_rstar_over_Mph"], r99=s["r99"],
                            sink=s["sink_cum_over_Vf2Mcat"], E=s["E"]) for s in snaps],
               wall_s=time.time() - t0, rhoph_neg_bins=toy.rhoph_neg, nsub_max=nsub_max,
               integ_err_final=fin["integ_err"], integ_err_maxabs=float(max(abs(s["integ_err"]) for s in snaps)))
    # first time |D| > 0.1
    tD = [s["t_Gyr"] for s in snaps if abs(s["D"]) > 0.1]
    res["t_first_absD_gt_0p1"] = tD[0] if tD else None
    res["gate_end"] = bool(abs(fin["logX"]) <= 0.1 and abs(fin["D"]) <= 0.1)
    res["gate_steady"] = bool(abs(res["d_logX_last2"]) <= 0.05 and abs(res["d_D_last2"]) <= 0.05)
    res["gate"] = res["gate_end"] and res["gate_steady"]
    # sink rate over the last 2 Gyr (per M_cat V_f^2 per Gyr)
    res["sink_rate_last2"] = float((fin["sink_cum_over_Vf2Mcat"] - ref["sink_cum_over_Vf2Mcat"]) / max(fin["t_Gyr"] - ref["t_Gyr"], 1e-9))
    return res


# ----------------------------------------------------------------------------------------------------------------- sympy
def sympy_items():
    R = {}
    x, t, v = sp.symbols("x t v", real=True)
    rho, u, s2, q, vs, Phi = [sp.Function(n)(x, t) for n in ("rho", "u", "s2", "q", "vs", "Phi")]
    M0, M1 = rho, rho * u
    M2 = rho * (u ** 2 + s2); M3 = rho * (u ** 3 + 3 * u * s2) + q
    # moment equations of d_t f + d_x[(v + vs) f] - Phi_x d_v f = 0: d_t M_n + d_x(M_{n+1} + vs M_n) + n Phi_x M_{n-1} = 0
    e0 = sp.diff(M0, t) + sp.diff(M1 + vs * M0, x)
    e1 = sp.diff(M1, t) + sp.diff(M2 + vs * M1, x) + sp.diff(Phi, x) * M0
    e2 = sp.diff(M2, t) + sp.diff(M3 + vs * M2, x) + 2 * sp.diff(Phi, x) * M1
    sol = sp.solve([e0, e1, e2], [sp.diff(rho, t), sp.diff(u, t), sp.diff(s2, t)], dict=True)[0]
    Ds2 = sp.simplify(sol[sp.diff(s2, t)] + (u + vs) * sp.diff(s2, x))
    target = -2 * s2 * sp.diff(u, x) - sp.diff(q, x) / rho
    R["K1_Dsigma2_along_u_plus_vs"] = str(Ds2)
    R["K1_no_drift_compression_term"] = bool(sp.simplify(Ds2 - target) == 0)
    R["K1_contains_dvs_dx"] = bool(Ds2.has(sp.Derivative(vs, x)))
    # ordinary flow (vs folded into u) for contrast: compression heating -2 s2 d_x(u + vs)
    R["K1_note"] = ("drift-advected sigma^2 obeys D sigma^2/Dt = -2 sigma^2 u_x - q_x/rho with D along u + v_s: the drift "
                    "compresses density without compression heating, so settled cold energy keeps its source dispersion")
    # K3a: two-sided deficit, discrete 3-cell model, F = 1/2 d^T K d, d = P - rho
    n = 3
    Ks = sp.Matrix(n, n, lambda i, j: sp.Symbol(f"K{min(i, j)}{max(i, j)}"))
    P = sp.symbols("P0:3"); rh = sp.symbols("rho0:3")
    d = sp.Matrix([P[i] - rh[i] for i in range(n)])
    F = (d.T * Ks * d)[0] / 2
    psi = -(Ks * d)
    grad = [sp.diff(F, rh[i]) for i in range(n)]
    R["K3a_first_variation_equals_psi"] = all(sp.simplify(grad[i] - psi[i]) == 0 for i in range(n))
    H = sp.hessian(F, rh)
    R["K3a_hessian_equals_K_symmetric"] = bool(sp.simplify(H - Ks) == sp.zeros(n, n))
    R["K3a_note"] = "two-sided: dF/drho_c = psi everywhere (no interval), Hessian = Coulomb kernel (positive) -> smooth convex gradient flow"
    # K3b: by-parts Lyapunov identity, radial (same as CFG541 V3, signed d)
    r = sp.symbols("r", positive=True); w = sp.Function("w")(r); ps = sp.Function("psi")(r)
    lhs = sp.diff(ps * w * sp.diff(ps, r) * r ** 2, r) - ps * sp.diff(w * sp.diff(ps, r) * r ** 2, r)
    R["K3b_by_parts_identity"] = bool(sp.simplify(lhs - w * sp.diff(ps, r) ** 2 * r ** 2) == 0)
    # K3c: psi = Phi_law - Phi for the two-sided deficit where B∩C covers the support
    R["K3c_identity"] = "lap psi = 4 pi G (rho_ph - rho_c) = lap(Phi_ph - Phi_c) => psi = Phi_law - Phi (inside B∩C, isolated BCs); v_s = alpha tau (g_law - g)"
    # K3d: OU velocity relaxation, local free energy G_x = int f (v^2/2 + T ln f) dv
    T = sp.symbols("T", positive=True); f = sp.Function("f")(v)
    J = v * f + T * sp.diff(f, v)
    integrand = (v ** 2 / 2 + T * sp.log(f) + T) * sp.diff(J, v)
    byparts = sp.diff((v ** 2 / 2 + T * sp.log(f) + T) * J, v) - integrand    # = J d_v(v^2/2 + T ln f)
    R["K3d_OU_dissipation_is_J2_over_f"] = bool(sp.simplify(byparts - J ** 2 / f) == 0)
    R["K3d_note"] = ("at fixed x the OU term is the gradient flow of int f (v^2/2 + T ln f) dv, dG_x/dt = -gamma int J^2/f <= 0; "
                     "with T = sigma_J^2(x) varying in x there is no global E - T S conserved by Vlasov")
    # K3e: full-system cross terms (1-D, symbolic)
    rr, uu, pp, ff, tt = sp.symbols("rho u psi_x Phi_x tau", real=True)
    al = sp.symbols("alpha", positive=True)
    R["K3e_dF_dt_Vlasov_integrand"] = str(rr * uu * pp)
    R["K3e_dE_dt_drift_integrand"] = str(sp.expand(rr * (-al * tt * pp) * ff))
    lnr = sp.symbols("dlnq_x", real=True)   # d_x ln(rho/rho_ph)
    R["K3e_d(E-TS)_dt_drift_integrand_isothermal"] = str(sp.expand(rr * (-al * tt * pp) * (-pp + T * lnr)))
    # discrete check that E_law - F = E + const (quadratic forms)
    Kc = sp.Matrix(2, 2, lambda i, j: sp.Symbol(f"C{min(i, j)}{max(i, j)}"))
    rc_ = sp.Matrix(sp.symbols("c0:2")); rp = sp.Matrix(sp.symbols("p0:2")); phb = sp.Matrix(sp.symbols("b0:2"))
    Phi_c = -Kc * rc_; Phi_ph = -Kc * rp
    E = (rc_.T * phb)[0] + (rc_.T * Phi_c)[0] / 2
    Elaw = (rc_.T * (phb + Phi_ph))[0]
    dd = rp - rc_; Fq = (dd.T * Kc * dd)[0] / 2
    R["K3e_Elaw_minus_F_equals_E_plus_const"] = bool(sp.simplify(sp.expand(Elaw - Fq - E + (rp.T * Kc * rp)[0] / 2)) == 0)
    R["K3e_signs"] = {"F under Vlasov": "int rho u psi_x: sign of u relative to psi_x -> INDEFINITE",
                      "E under drift": "-alpha int rho tau psi_x Phi_x: negative for underfill (psi_x > 0), positive for overfill removal -> INDEFINITE",
                      "E - T S under drift": "+alpha int rho tau psi_x^2 - alpha T int rho tau psi_x (ln rho/rho_ph)_x: first term >= 0 -> INDEFINITE",
                      "E_law - F": "equals E + const (sympy), so same as E -> INDEFINITE"}
    R["K3_full_system_Lyapunov"] = "NOT ESTABLISHED"
    return R


def jeans_controls(c):
    """C1: untruncated deep-regime sigma_eq^2/V_f^2 at r = 100 r_M (integral to 1e5 r_M, unsoftened)."""
    rM = c["Mb"]
    r = np.geomspace(rM, 1e5 * rM, 40001)
    Mph = Mph_enc(c, r); rho = np.gradient(Mph, r) / (4 * math.pi * r ** 2)
    f = rho * (Mb_enc(c, r) + Mph) / r ** 2
    P = np.concatenate([np.cumsum((0.5 * (f[1:] + f[:-1]) * np.diff(r))[::-1])[::-1], [0.0]])
    # add the analytic tail beyond 1e5 r_M (SIS: P = 1/(8 pi r^2))
    P = P + 1.0 / (8 * math.pi * r[-1] ** 2)
    s2 = P / rho
    return float(np.interp(100 * rM, r, s2))


# ----------------------------------------------------------------------------------------------------------------- 1-D drift-only
def drift1d(c, rule, N=400):
    rin = (1e-2 * c["a"]) if c["a"] is not None else 1e-3 * c["Mb"]
    rf = np.geomspace(rin, c["rta"], N + 1); V = 4 * math.pi / 3 * np.diff(rf ** 3); A = 4 * math.pi * rf ** 2
    rhob = np.diff(Mb_enc(c, rf)) / V if c["a"] is not None else np.zeros(N)
    rhoph = np.maximum(np.diff(Mph_enc(c, rf)), 0.0) / V
    m = np.full(N, c["Mcat"] / (4 * math.pi / 3 * (c["rta"] ** 3 - rin ** 3))) * V
    t = 0.0; it = 0; tend = 60.0 / c["tu_Gyr"]
    while t < tend and it < 400000:
        rho = m / V
        d = (rhoph - rho) if rule == "two" else np.maximum(rhoph - rho, 0.0)
        Md = np.concatenate([[0.0], np.cumsum(d * V)])
        dpsi = Md / rf ** 2
        vface = np.zeros(N + 1)
        # upwind density and tau at interior faces
        vi = -ALPHA * dpsi[1:-1]
        up = np.where(vi < 0, np.arange(1, N), np.arange(0, N - 1))
        tau = 1.0 / np.sqrt(4 * math.pi * np.maximum(rhob + rho, 1e-300))
        vface[1:-1] = vi * tau[up]
        live = np.zeros(N + 1, bool); live[1:-1] = m[up] > 1e-14 * c["Mcat"]
        vl = np.where(live, np.abs(vface), 0.0)
        cfl = np.min(np.diff(rf) / np.maximum(vl[1:] + vl[:-1], 1e-300))
        gam = np.max(4 * math.pi * rho * tau * ALPHA)
        dt = min(0.4 * cfl, 0.2 / gam, tend - t)
        flux = np.zeros(N + 1)
        flux[1:-1] = np.where(live[1:-1], rho[up] * vface[1:-1] * A[1:-1] * dt, 0.0)
        # donor-cell, never more than the donor's mass
        flux[1:-1] = np.where(vface[1:-1] < 0, -np.minimum(-flux[1:-1], m[up]), np.minimum(flux[1:-1], m[up]))
        m = m - (flux[1:] - flux[:-1])
        m = np.maximum(m, 0.0)
        t += dt; it += 1
    rho = m / V; q = rho / np.maximum(rhoph, 1e-300)
    i0 = int(np.where(q < 0.999)[0][0]) if (q < 0.999).any() else N
    # sub-cell filled radius (equivalent filled volume beyond i0)
    r3 = rf[i0] ** 3 + np.sum(np.minimum(q[i0:], 1) * np.diff(rf[i0:] ** 3) * (rf[i0 + 1:] <= 1.5))
    return dict(rf=rf, m=m, rstar_subcell=float(r3 ** (1 / 3)), r_filled_face=float(rf[i0]), t_end_Gyr=t * c["tu_Gyr"],
                steps=it, mass_err=float(abs(m.sum() - c["Mcat"] / (4 * math.pi / 3 * (c["rta"] ** 3 - rin ** 3)) * V.sum()) / c["Mcat"]))


def alt_s(c):
    """ALT-S: isothermal (T = V_f^2/2) self-consistent cold energy + static baryons, mass M_cat inside r_ta (reflecting r_min)."""
    T = 0.5
    r = np.geomspace(RMIN, c["rta"], 20001)
    mbr = Mb_enc(c, r)
    def solve(lrho0):
        rho = np.empty_like(r); M = 0.0; phi = 0.0
        rho[0] = math.exp(lrho0)
        Ms = np.zeros_like(r)
        for i in range(1, r.size):
            dr = r[i] - r[i - 1]
            gi = (mbr[i - 1] + M) / r[i - 1] ** 2
            phi += gi * dr
            lr = lrho0 - phi / T
            if lr > 700: return None, None
            rho[i] = math.exp(lr)
            M += 4 * math.pi * r[i] ** 2 * rho[i] * dr
            Ms[i] = M
        return rho, Ms
    # first crossing of M(r_ta) = M_cat scanning the central density upward (the isothermal M(rho0) is not monotone: spiral)
    lo = None; hi = None; prev = -30.0
    for l0 in np.arange(-30.0, 40.0, 0.25):
        rho, Ms = solve(l0)
        if rho is None or Ms[-1] > c["Mcat"]:
            lo, hi = prev, l0; break
        prev = l0
    ok = None
    if lo is not None:
        for _ in range(60):
            mid = 0.5 * (lo + hi); rho, Ms = solve(mid)
            if rho is None or Ms[-1] > c["Mcat"]: hi = mid
            else: lo = mid; ok = (rho, Ms)
    if ok is None:
        return dict(exists=False)
    rho, Ms = ok
    be = np.geomspace(0.1, 0.9, 17); rc = np.sqrt(be[1:] * be[:-1])
    rph = np.gradient(Mph_enc(c, r), r) / (4 * math.pi * r ** 2)
    with np.errstate(divide="ignore"):
        Dm = float(np.median(np.log10(np.interp(rc, r, rho) / np.interp(rc, r, rph))))
    r99 = float(np.interp(0.99 * Ms[-1], Ms, r))
    with np.errstate(divide="ignore"):
        inner = float(np.log10(np.interp(c["Mb"], r, rho) / np.interp(c["Mb"], r, rph)))
    fin = lambda z: (float(z) if np.isfinite(z) else None)
    return dict(exists=True, M_over_Mcat=float(Ms[-1] / c["Mcat"]), D_shell=fin(Dm), log_rho_over_rhoph_at_rM=fin(inner),
                r99_over_rstar=r99, central_fraction_inside_0p01=float(np.interp(0.01, r, Ms) / Ms[-1]))


# ----------------------------------------------------------------------------------------------------------------- main
def r99_analytic(c):
    rg = np.geomspace(RMIN, 1.0, 20001); M = Mph_enc(c, rg); M = M - M[0]
    return float(np.interp(0.99 * M[-1], M, rg))


def main():
    cells = {f"{s}_{f}": make_cell(s, f) for s in SYS for f in FOOT}
    RES["cells"] = {k: {kk: vv for kk, vv in v.items() if kk not in ("Vf2_SI", "rstar_SI")} for k, v in cells.items()}
    log("CFG544 kinetic consistency of class-A settling" + (" [MUTATE]" if MUT else ""))
    ok_ctrl = True; c4_ok = True; keys0 = list(cells)
    # C4 + C1
    for k, c in cells.items():
        mph1 = float(Mph_enc(c, np.array([1.0]))[0])
        c4 = abs(mph1 / c["Mcat"] - 1)
        c1 = jeans_controls(c)
        RES["cells"][k].update(C4_Mph_rstar_over_Mcat_minus1=c4, C1_sigma2_deep_over_Vf2=c1, r99_analytic=r99_analytic(c))
        log(f"{k}: V_f {c['Vf_kms']:.1f} km/s, r_* {c['rstar_kpc']:.1f} kpc, r_ta/r_* {c['rta']:.3f}, M_cat/M_b {c['Mcat']/c['Mb']:.3f}, "
            f"t_unit {c['tu_Gyr']:.3f} Gyr; C4 |M_ph(<r_*)/M_cat - 1| = {c4:.2e}; C1 sigma_eq^2/V_f^2 (deep, 100 r_M) = {c1:.4f}")
        ok_ctrl &= abs(c1 / 0.5 - 1) <= 0.02
        c4_ok = (c4 <= 1e-4) if k == keys0[0] else (c4_ok and c4 <= 1e-4)
    RES["controls"] = dict(C1_pass=ok_ctrl, C4_Mph_match_pass=c4_ok)
    if not MUT:
        RES["sympy"] = sympy_items()
        log("\nSympy:")
        for kk, vv in RES["sympy"].items():
            log(f"  {kk}: {vv}")

    jobs = []
    for k, c in cells.items():
        if not MUT:
            jobs += [dict(c=c, name=f"{k}|C2_vlasov_eq", ic="E", rule="none", ou=False, T=2.0),
                     dict(c=c, name=f"{k}|asis_B", ic="B", rule="one", ou=False, T=10.0),
                     dict(c=c, name=f"{k}|asis_C", ic="C", rule="one", ou=False, T=5.0),
                     dict(c=c, name=f"{k}|fix1_B", ic="B", rule="two", ou=False, T=10.0),
                     dict(c=c, name=f"{k}|fix1_C", ic="C", rule="two", ou=False, T=5.0),
                     dict(c=c, name=f"{k}|fix2_B", ic="B", rule="two", ou=True, T=10.0),
                     dict(c=c, name=f"{k}|fix2_C", ic="C", rule="two", ou=True, T=5.0),
                     dict(c=c, name=f"{k}|over_one_base", ic="E", rule="one", ou=False, T=5.0),
                     dict(c=c, name=f"{k}|over_one_inj", ic="E", rule="one", ou=False, T=5.0, inject=True),
                     dict(c=c, name=f"{k}|over_two_base", ic="E", rule="two", ou=False, T=5.0),
                     dict(c=c, name=f"{k}|over_two_inj", ic="E", rule="two", ou=False, T=5.0, inject=True)]
        else:
            jobs += [dict(c=c, name=f"{k}|MV_vlasov_sig2x2", ic="E", rule="none", ou=False, T=2.0, sig2=2.0),
                     dict(c=c, name=f"{k}|MO_base", ic="E", rule="one", ou=False, T=5.0),
                     dict(c=c, name=f"{k}|MO_inj", ic="E", rule="one", ou=False, T=5.0, inject=True),
                     dict(c=c, name=f"{k}|MT_fix2_C_target_x2", ic="C", rule="two", ou=True, T=5.0, ou_scale=2.0)]
    # longest first
    jobs.sort(key=lambda j: -j["T"] / j["c"]["dt"] / j["c"]["tu_Gyr"])
    with Pool(2) as pool:
        out = pool.map(run, jobs, chunksize=1)
    runs = {o["name"]: o for o in out}
    RES["runs"] = runs
    log("\nRuns (end state; shell 0.1-0.9 r_*):")
    for nm in sorted(runs):
        o = runs[nm]; f = o["final"]
        log(f"  {nm:34s} t {o['T_Gyr']:4.1f} Gyr  logX {f['logX']:+.3f}  D {f['D']:+.3f}  dlogX/dD last2 {o['d_logX_last2']:+.3f}/{o['d_D_last2']:+.3f}"
            f"  M(<r*)/Mph {f['Mc_in_rstar_over_Mph']:.3f}  r99 {f['r99']:.3f}  beta {f['beta']:+.2f}  sink {f['sink_cum_over_Vf2Mcat']:+.3f}"
            f"  dE/E {o['dE_over_E']:+.1e} integ {o['integ_err_maxabs']:.1e} nsub {o['nsub_max']}  lim {o['limited_frac']:.1e}  gate {o['gate']}  tD {o['t_first_absD_gt_0p1']}  ({o['wall_s']:.0f}s)")
        log("       s(r) bins: " + " ".join("nan" if (x != x) else f"{x:.2f}" for x in f["s_bins"]))

    keys = list(cells)
    if MUT:
        mv = {k: (not runs[f"{k}|MV_vlasov_sig2x2"]["gate_end"]) for k in keys}
        mo = {}
        for k in keys:
            inj = runs[f"{k}|MO_inj"]; base = runs[f"{k}|MO_base"]
            Mi = (inj["n_particles"] - base["n_particles"]) * cells[k]["Mcat"] / NPART
            mo[k] = (inj["final"]["excess_in_rstar"] - base["final"]["excess_in_rstar"]) / Mi
        mt = {k: (not runs[f"{k}|MT_fix2_C_target_x2"]["gate"]) for k in keys}
        bite = dict(MV=all(mv.values()), MO=all(v > 0.2 for v in mo.values()), MT=all(mt.values()))
        RES["mutate_teeth"] = dict(MV_breaks=mv, MO_P=mo, MT_fails=mt, bite=bite)
        log(f"\nMUTATE: MV breaks {mv}; MO P {mo}; MT fails {mt}; bite {bite}")
        return 1 if all(bite.values()) else 0

    # controls C2/C3
    c2 = {k: runs[f"{k}|C2_vlasov_eq"]["gate_end"] for k in keys}
    c3 = {k: abs(runs[f"{k}|C2_vlasov_eq"]["dE_over_E"]) <= 1e-2 for k in keys}
    RES["controls"]["integrator_err_maxabs_all_runs"] = {nm: o["integ_err_maxabs"] for nm, o in runs.items()}
    mass = all(o["mass_exact"] for o in runs.values())
    RES["controls"].update(C2=c2, C3=c3, C4_mass_exact_all_runs=mass)
    ctrl = ok_ctrl and all(c2.values()) and all(c3.values()) and mass          # every control except the C4 M_ph match
    ctrl_frozen = ctrl and c4_ok
    RES["controls"]["all_pass_as_frozen"] = ctrl_frozen
    RES["controls"]["all_pass_except_C4_match"] = ctrl
    log(f"\nControls: C1 {ok_ctrl}; C4 M_ph(<r_*) = M_cat to 1e-4: {c4_ok}; C2 {c2}; C3 {c3}; mass exact {mass} -> "
        f"{'PASS' if ctrl_frozen else 'FAIL as frozen'}")

    # Q1
    q1 = {k: dict(B=runs[f"{k}|asis_B"]["gate"], C=runs[f"{k}|asis_C"]["gate"]) for k in keys}
    q1_ok = all(v["B"] and v["C"] for v in q1.values())
    # FIX-1/2
    f1 = {k: dict(B=runs[f"{k}|fix1_B"]["gate"], C=runs[f"{k}|fix1_C"]["gate"]) for k in keys}
    f2 = {k: dict(B=runs[f"{k}|fix2_B"]["gate"], C=runs[f"{k}|fix2_C"]["gate"]) for k in keys}
    f1_ok = all(v["B"] and v["C"] for v in f1.values()); f2_ok = all(v["B"] and v["C"] for v in f2.values())
    # overfill
    P = {}
    for rule in ("one", "two"):
        for k in keys:
            inj = runs[f"{k}|over_{rule}_inj"]; base = runs[f"{k}|over_{rule}_base"]
            Mi = (inj["n_particles"] - base["n_particles"]) * cells[k]["Mcat"] / NPART
            P[f"{k}|{rule}"] = (inj["final"]["excess_in_rstar"] - base["final"]["excess_in_rstar"]) / Mi
    handled = all(P[f"{k}|two"] <= 0.2 for k in keys) and all(P[f"{k}|one"] >= 0.5 for k in keys)
    overfill = "HANDLED" if handled else ("NOT HANDLED" if any(P[f"{k}|two"] > 0.2 for k in keys) else
                                          "HANDLED by FIX-1, but the one-sided persistence (P >= 0.5) is not shown in every cell")
    # energy
    en = {}
    for k in keys:
        for fx in ("fix1", "fix2"):
            for ic in ("B", "C"):
                o = runs[f"{k}|{fx}_{ic}"]
                en[f"{k}|{fx}_{ic}"] = dict(net_sink=o["final"]["sink_cum_over_Vf2Mcat"], rate_last2=o["sink_rate_last2"])
    en_ok = all(0 <= en[f"{k}|fix1_{ic}"]["net_sink"] <= 1.0 for k in keys for ic in ("B", "C"))
    # Q3
    q3a = {}
    for k, c in cells.items():
        one = drift1d(c, "one"); two = drift1d(c, "two")
        Mone = np.cumsum(one["m"]); Mtwo = np.cumsum(two["m"]); rr = one["rf"][1:]
        ins = rr <= 1.0
        q3a[k] = dict(rstar_one=one["rstar_subcell"], rstar_two=two["rstar_subcell"],
                      dln_rstar=float(math.log(two["rstar_subcell"] / one["rstar_subcell"])),
                      max_cum_diff_over_Mcat=float(np.max(np.abs(Mtwo[ins] - Mone[ins])) / c["Mcat"]),
                      t_end_Gyr=one["t_end_Gyr"], steps=(one["steps"], two["steps"]), mass_err=(one["mass_err"], two["mass_err"]))
    q3b = {k: float(math.log(runs[f"{k}|fix1_B"]["final"]["r99"] / RES["cells"][k]["r99_analytic"])) for k in keys}
    q3_ok = all(abs(v["dln_rstar"]) <= 0.01 and v["max_cum_diff_over_Mcat"] <= 1e-3 for v in q3a.values()) and \
        all(abs(v) <= 0.1 for v in q3b.values())
    alts = {k: alt_s(c) for k, c in cells.items()}

    lyap = RES["sympy"]["K3_full_system_Lyapunov"]
    if not ctrl:
        lab = "NO LABEL (controls fail)"
    elif q1_ok:
        lab = "KINETICALLY CONSISTENT (as is)"
    elif f1_ok and mass and handled and q3_ok and en_ok:
        lab = f"CONSISTENT WITH FIX (FIX-1 two-sided deficit; full-system Lyapunov {lyap})"
    elif f2_ok:
        lab = "INCONSISTENT (needs a posited velocity closure; FIX-2 is a candidate, not adopted)"
    else:
        lab = "INCONSISTENT (no fix passes)"
    RES["Q1"] = dict(gates=q1, kinetically_consistent_as_is=q1_ok)
    RES["Q2"] = dict(fix1_gates=f1, fix1_pass=f1_ok, fix2_gates=f2, fix2_pass=f2_ok, energy=en, energy_compatible_fix1=en_ok,
                     overfill_P=P, overfill=overfill, full_system_lyapunov=lyap, alt_s=alts)
    RES["Q3"] = dict(one_d=q3a, nbody_dln_r99=q3b, label="UNCHANGED" if q3_ok else "CHANGED")
    lab_frozen = lab if ctrl_frozen else "NO LABEL as frozen (control C4 fails)"
    RES["labels"] = dict(kinetic_as_frozen=lab_frozen, kinetic_if_C4_read_at_toy_resolution=lab, overfill=overfill,
                         Q3=RES["Q3"]["label"], full_system_lyapunov=RES["sympy"]["K3_full_system_Lyapunov"])
    log(f"\nQ1 as is: {q1} -> {'KINETICALLY CONSISTENT' if q1_ok else 'NOT consistent as is'}")
    log(f"FIX-1 gates {f1} -> {f1_ok}; FIX-2 gates {f2} -> {f2_ok}")
    log(f"Energy (net sink per M_cat V_f^2; rate last 2 Gyr): " + "; ".join(f"{a} {b['net_sink']:+.3f} ({b['rate_last2']:+.4f}/Gyr)" for a, b in en.items()))
    log(f"Energy compatible (FIX-1): {en_ok}")
    log(f"Overfill P: " + ", ".join(f"{a} {b:+.3f}" for a, b in P.items()) + f" -> {overfill}")
    log(f"Q3 1-D: " + "; ".join(f"{a}: r*_one {b['rstar_one']:.4f} r*_two {b['rstar_two']:.4f} dln {b['dln_rstar']:+.2e} maxcum {b['max_cum_diff_over_Mcat']:.2e} (t {b['t_end_Gyr']:.0f} Gyr)" for a, b in q3a.items()))
    log(f"Q3 N-body dln r99 (FIX-1, IC-B): {q3b} -> {RES['Q3']['label']}")
    log(f"ALT-S (diagnostic): {alts}")
    log(f"\nLABELS: kinetic as frozen = {lab_frozen}; kinetic if C4 is read at the toy's resolution = {lab}; overfill = {overfill}; Q3 = {RES['Q3']['label']}; full-system Lyapunov = {lyap}")
    return 0 if ctrl else 1


if __name__ == "__main__":
    rc = main()
    with open(os.path.join(HERE, f"cfg544{TAG}.out"), "w") as fh:
        fh.write("\n".join(OUT) + "\n")
    with open(os.path.join(HERE, f"cfg544_results{TAG}.json"), "w") as fh:
        json.dump(RES, fh, indent=1, default=lambda o: o.tolist() if hasattr(o, "tolist") else str(o))
    sys.exit(rc)
