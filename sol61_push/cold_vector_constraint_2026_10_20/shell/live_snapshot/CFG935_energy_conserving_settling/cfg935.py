#!/usr/bin/env python3
"""CFG935: the minimal energy-conserving form of cold-energy settling.
FROZEN_CRITERIA.md (38f4b6f18, committed alone first); AMENDMENT_A0_pre_result.md (e9a824153, committed alone before any script).

Repairs of the record's settling (CFG638 = CFG541 E3 drift + CFG544 FIX-2 bath; CFG932 Q1: d(K+W)/dt = P_drift + P_bath):
  R-a(i)  'Ra1'  N-type gravity + Hamiltonian FIX-1 settling energy lambda*F (lambda 10; variant 100), Vlasov, no drift / bath
  R-a(ii) 'Ra2'  canonical S2 tether (cold self-gravity cancelled; W_rem push; baryons pull), Vlasov, no drift / bath;
                 thin-shell midpoint-in-mass discretisation (AMENDMENT A1; the frozen step rule had a finite barrier)
  R-b     'Rb'   N-type + one-sided drift (CFG541 E5) with the drift's exact energy change booked as cold-energy heat
  R-c     'Rc'   R-b + one-way cooling above the FIX-2 Jeans target into a declared radiation reservoir E_rad
  R-d     'Rd'   N-type + two-sided drift (FIX-1) + FIX-2 bath, both booked to a dark-energy partner E_DE (CFG542 Pb)
One 1-D spherical shell toy (G = a0 = 1, static Plummer M_b = 1, a = 1, simple nu, r_* = 10, R_C = 30, alpha = 1, N = 10000).

Parts:  python3 cfg935.py <part>  -> parts/<part>.json ;  python3 cfg935.py summary -> cfg935.out, cfg935_results.json
        CFG935_MUTATE=1 python3 cfg935.py  -> M1 (R-d, partner booking off), M2 (R-b, heat booking off), M3 (S2, tether energy
        left out of the books) -> cfg935_MUTATE.out, cfg935_results_MUTATE.json ; exit 1 when all three bite (record convention).
Run with OMP_NUM_THREADS=1 nice -n 10, one process at a time, < 1 GB.
kappa = 1/2 FITTED; footings 9.3603e-11 / 1.1312e-10 never pooled (they enter only the physical tables); cold energy mass
required; no particle species; not theory closed."""
import os, sys, json, math, time
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_v] = "1"
import numpy as np
from scipy.optimize import brentq

HERE = os.path.dirname(os.path.abspath(__file__))
PARTS = os.path.join(HERE, "parts")
CRITERIA, AMEND_A0 = "38f4b6f18", "e9a824153"
AMEND_A1 = "679994050"                               # S2 midpoint-in-mass discretisation
AMEND_A2 = "pending"                                 # N-type thin-shell softening (set after its commit)
MUT = os.environ.get("CFG935_MUTATE", "0") == "1"

# ------------------------------------------------------------------ toy constants (FROZEN_CRITERIA §2, A0)
G, A0, MB, AB = 1.0, 1.0, 1.0, 1.0
RSTAR, RC, ALPHA, NP = 10.0, 30.0, 1.0, 10000
SEED = 935
# implementation knobs (set on the K2 integrator check only; disclosed in the README)
RMIN = 1e-3          # reflecting inner boundary (0.05 failed K2: reflections pump energy; disclosed)
DTMAX = 0.02
CA = 0.03            # dt <= CA * min sqrt(r/|a|)
CS = 0.05            # dt <= CS * min r/|v_s|   (drift)
EPS = 0.02           # AMENDMENT A2: softening of the N-type thin-shell 1/r^2 kernels (self-gravity, lambda F, drift)
T_EDGE = {"N": 2 * math.pi * math.sqrt(RSTAR ** 3 / G), "S2": 2 * math.pi * math.sqrt(RSTAR ** 3 / (G * MB))}

# ------------------------------------------------------------------ baryons (static Plummer) and the law (simple nu)
def Mb_enc(r):
    r = np.asarray(r, float); return MB * r ** 3 / (r * r + AB * AB) ** 1.5
def g_b(r):
    r = np.asarray(r, float); return G * MB * r / (r * r + AB * AB) ** 1.5
def Phi_b(r):
    r = np.asarray(r, float); return -G * MB / np.sqrt(r * r + AB * AB)
def num1(y):
    """nu(y) - 1 for nu = (1 + sqrt(1 + 4/y))/2, written without cancellation."""
    y = np.asarray(y, float); return (2.0 / y) / (1.0 + np.sqrt(1.0 + 4.0 / y))
def Mph(r):
    r = np.asarray(r, float); Mb = Mb_enc(r); y = G * Mb / (r * r * A0); return Mb * num1(y)
def dMph_dMb(r):
    r = np.asarray(r, float); y = G * Mb_enc(r) / (r * r * A0); return num1(y) - 1.0 / np.sqrt(y * y + 4.0 * y)
def g_law(r):
    r = np.asarray(r, float); return G * (Mb_enc(r) + Mph(r)) / r ** 2

MC = float(Mph(RSTAR))                    # cold mass: settled edge at r_* = 10
MU = MC / NP
T_EDGE["N"] = 2 * math.pi * math.sqrt(RSTAR ** 3 / (G * (MB + MC)))
T_END = {"N": {"L": 350.0, "I": 650.0, "S": 650.0}, "S2": {"L": 1000.0, "I": 2000.0, "S": 2000.0}}   # A0.1

RT = np.geomspace(1e-5, 1e4, 400001)
MT = Mph(RT)
assert np.all(np.diff(MT) > 0), "phantom not monotone"
LRT, LMT = np.log(RT), np.log(MT)
def Minv(m):
    return np.exp(np.interp(np.log(np.asarray(m, float)), LMT, LRT))
# cumulative tables for lambda*F: I1 = int_0^r Mph/(r'^2+eps^2), I2 = int_0^r Mph^2/(r'^2+eps^2) (trapezoid on the fine grid)
_f1, _f2 = MT / (RT ** 2 + EPS ** 2), MT ** 2 / (RT ** 2 + EPS ** 2)        # A2: softened kernel 1/(r^2 + eps^2)
_dr = np.diff(RT)
I1T = np.concatenate([[0.0], np.cumsum(0.5 * (_f1[1:] + _f1[:-1]) * _dr)])
I2T = np.concatenate([[0.0], np.cumsum(0.5 * (_f2[1:] + _f2[:-1]) * _dr)])
def I1(r): return np.interp(r, RT, I1T)
def I2(r): return np.interp(r, RT, I2T)

# ------------------------------------------------------------------ S2 tether: W_rem and the exact energy between sorted shells
def wfun(u):
    """w(u) = K W_rem(u)/(4 pi G) * G... = -u^2/2 - a0 u - a0^2 ln(1 - u/a0) (= a0^2 sum_{n>=3} x^n/n, x = u/a0)."""
    x = np.atleast_1d(np.asarray(u, float)) / A0
    out = np.empty_like(x)
    sm = x < 0.1
    if sm.any():
        xs = x[sm]; s = np.zeros_like(xs); p = xs ** 3
        for n in range(3, 40):
            s += p / n; p = p * xs
        out[sm] = A0 * A0 * s
    lg = ~sm
    if lg.any():
        xl = x[lg]
        with np.errstate(divide="ignore", invalid="ignore"):
            out[lg] = np.where(xl < 1.0, A0 * A0 * (-xl * xl / 2 - xl - np.log1p(-xl)), np.inf)
    return out

# ---- the FROZEN step rule (criteria §2): kept for the record, unused after AMENDMENT A1 (its thin-shell barrier is finite)
def Gfun(r, A):
    """Antiderivative of r^2 w(A/r^2) that vanishes at r -> infinity (closed form for x >= 0.3, series below)."""
    r = np.atleast_1d(np.asarray(r, float)); A = np.broadcast_to(np.asarray(A, float), r.shape).astype(float)
    x = A / (A0 * r * r)
    out = np.zeros_like(r)
    sm = (x < 0.3) & np.isfinite(r)
    if sm.any():
        xs, rs = x[sm], r[sm]; s = np.zeros_like(xs); p = xs ** 3
        for n in range(3, 70):
            s += p / (n * (3.0 - 2.0 * n)); p = p * xs
        out[sm] = A0 * A0 * rs ** 3 * s
    lg = (~sm) & np.isfinite(r)
    if lg.any():
        rl, Al = r[lg], A[lg]; b = np.sqrt(Al / A0)
        with np.errstate(divide="ignore", invalid="ignore"):
            br = A0 * A0 * ((rl ** 3 / 3) * np.log1p(-b * b / (rl * rl)) - (2.0 / 3.0) * b * b * rl
                            - (b ** 3 / 3) * np.log((rl - b) / (rl + b)))
            out[lg] = np.where(rl > b, Al * Al / (2 * rl) - A0 * Al * rl - br, np.inf)
    return out

def V_tether_sorted(rs):
    """(1/G) int_0^inf r^2 w(G m(<r)/r^2) dr with m piecewise constant between sorted radii rs (masses MU)."""
    n = rs.size
    A = G * MU * np.arange(1, n + 1)
    lower = Gfun(rs, A)
    upper = np.zeros(n); upper[:-1] = Gfun(rs[1:], A[:-1])
    return float(np.sum(upper - lower)) / G

def phi_mid(r, A):
    """int_r^inf h(A/r'^2) dr', h(u) = u^2/(a0 - u): (A/r)[atanh(sqrt x)/sqrt x - 1], x = A/(a0 r^2) (series below x = 0.3)."""
    r = np.atleast_1d(np.asarray(r, float)); A = np.broadcast_to(np.asarray(A, float), r.shape).astype(float)
    x = A / (A0 * r * r)
    out = np.empty_like(r)
    sm = x < 0.3
    if sm.any():
        xs = x[sm]; s = np.zeros_like(xs); p = xs.copy()
        for n in range(1, 61):
            s += p / (2 * n + 1); p = p * xs
        out[sm] = A[sm] / r[sm] * s
    lg = ~sm
    if lg.any():
        xl = x[lg]
        with np.errstate(divide="ignore", invalid="ignore"):
            q = np.sqrt(np.minimum(xl, 1.0))
            out[lg] = np.where(xl < 1.0, A[lg] / r[lg] * (np.arctanh(q) / q - 1.0), np.inf)
    return out

def V_tether_mid_sorted(rs):
    """AMENDMENT A1: midpoint-in-mass discretisation of (1/G) int r^2 w(G m/r^2) dr = sum_k mu phi_k(r_(k)), A_k = G(k+1/2)mu.
    Its exact gradient is the thin-shell push mu h(G(k+1/2)mu/r^2), which keeps the continuum's infinite barrier at u = a0."""
    A = G * MU * (np.arange(rs.size) + 0.5)
    return MU * float(np.sum(phi_mid(rs, A)))

def F_settle_sorted(rs):
    """F = (G/2) int_0^{R_C} [Mph(<r) - m(<r)]^2 / (r^2 + eps^2) dr (A2), m piecewise constant between sorted radii rs."""
    n = rs.size
    a = np.minimum(np.concatenate([[0.0], rs]), RC); b = np.minimum(np.concatenate([rs, [RC]]), RC)
    m = MU * np.arange(n + 1)
    tot = I2(b) - I2(a) - 2 * m * (I1(b) - I1(a))
    ok = (a > 0) & (b > a)
    tot = tot + m * m * (np.arctan(b / EPS) - np.arctan(a / EPS)) / EPS     # A2: int dr/(r^2 + eps^2)
    return 0.5 * G * float(np.sum(tot))

# ------------------------------------------------------------------ law-state helpers (Jeans support of the N-type law)
def law_jeans_sigma2(r):
    """Isotropic Jeans sigma^2 of rho_ph in the N-type field g = G(Mb + Mph)/r^2, truncated at r_* (zero surface pressure)."""
    sel = RT <= RSTAR
    rr = RT[sel]; MM = MT[sel]
    rho = np.gradient(MM, rr) / (4 * np.pi * rr ** 2)
    g = G * (Mb_enc(rr) + MM) / rr ** 2
    integ = rho * g
    p = np.concatenate([np.cumsum((0.5 * (integ[1:] + integ[:-1]) * np.diff(rr))[::-1])[::-1], [0.0]])
    return np.interp(r, rr, p / rho)

def K_jeans_law(M):
    """K_J = 1/2 int_0^{r_*(M)} G[Mb(<r) + Mph(<r)]/r dMph (virial identity)."""
    rs = float(Minv(M))
    sel = RT <= rs
    rr = np.concatenate([RT[sel], [rs]]); MM = Mph(rr)
    f = G * (Mb_enc(rr) + MM) / rr
    return 0.5 * float(np.sum(0.5 * (f[1:] + f[:-1]) * np.diff(MM)))

# ------------------------------------------------------------------ initial states
def ic_state(ic, grav, rng):
    m = MU * (np.arange(NP) + 0.5)
    if ic == "L":
        if grav == "S2":
            r = s2_static_positions()
            return r, np.zeros(NP), np.zeros(NP)
        r = Minv(m)
        s = np.sqrt(np.maximum(law_jeans_sigma2(r), 0.0))
        v = s * rng.standard_normal(NP)
        vt = s * np.sqrt(rng.standard_normal(NP) ** 2 + rng.standard_normal(NP) ** 2)
        return r, v, r * vt
    if ic == "I":
        r = 15.0 * (m / MC) ** (1.0 / 3.0); mic = m
    elif ic == "S":
        r = Minv(m / 1.5); mic = m
    else:
        raise ValueError(ic)
    vc = np.sqrt(G * (Mb_enc(r) + mic) / r)
    return r, np.zeros(NP), 0.05 * r * vc

_S2POS = None
def s2_static_positions():
    """Exact discrete static equilibrium of the S2 cold law (A1 midpoint rule): mu h(G(k+1/2)mu/r_k^2) = mu g_b(r_k)."""
    global _S2POS
    if _S2POS is not None:
        return _S2POS.copy()
    # A1: with the midpoint push mu h(G(k+1/2)mu/r^2) = mu g_b(r), the static state is exactly Mph(r_k) = (k+1/2) mu
    m = MU * (np.arange(NP) + 0.5)
    out = Minv(m)
    for _ in range(4):                                             # Newton refinement of the table inversion
        hstep = 1e-6 * out
        dM = (Mph(out + hstep) - Mph(out - hstep)) / (2 * hstep)
        out = out - (Mph(out) - m) / dM
    assert np.all(np.diff(out) > 0), "S2 static positions not ordered"
    _S2POS = out
    return out.copy()

# ------------------------------------------------------------------ the shell simulation
EDGES = np.concatenate([[0.0], np.geomspace(0.05, RC, 41)])
NB = EDGES.size - 1
VOLB = 4 * np.pi / 3 * np.diff(EDGES ** 3)
DMB = np.diff(Mb_enc(np.maximum(EDGES, 1e-8)))
DMPH = np.diff(Mph(np.maximum(EDGES, 1e-8)))
RMID = np.concatenate([[0.5 * EDGES[1]], np.sqrt(EDGES[1:-1] * EDGES[2:])])
SEDGES = np.geomspace(0.1 * RSTAR, 0.9 * RSTAR, 17)            # measurement bins in S = [1, 9]
SVOL = 4 * np.pi / 3 * np.diff(SEDGES ** 3)
SRHOPH = np.diff(Mph(SEDGES)) / SVOL
RM3 = np.array([2.0, 5.0, 8.0])

class Sim:
    def __init__(self, rep, ic, lam=0.0, mut=None):
        self.rep, self.ic, self.lam, self.mut = rep, ic, lam, mut
        self.grav = "S2" if rep == "Ra2" else "N"
        self.drift = {"Rb": "one", "Rc": "one", "Rd": "two"}.get(rep)
        self.bath = {"Rc": "cool", "Rd": "ou"}.get(rep)
        self.heat = rep in ("Rb", "Rc")
        self.rng = np.random.default_rng(SEED)
        self.r, self.v, self.L = ic_state(ic, self.grav, self.rng)
        self.t = 0.0
        self.E_part = 0.0            # E_rad (R-c) or E_DE (R-d)
        self.heat_in = 0.0           # heat booked by the drift (R-b, R-c)
        self.flows = dict(drift_to_partner_pos=0.0, drift_to_partner_neg=0.0, bath_to_partner_pos=0.0,
                          bath_to_partner_neg=0.0, heat_pos=0.0, heat_neg=0.0, unbooked=0.0)
        self.vs = np.zeros(NP)
        self.nsteps = 0
        self.flags = []
        self.a = self.accel()
        if self.drift:
            self.vs = self.drift_velocity(self.binned())

    # ---- ordering
    def sort(self):
        self.order = np.argsort(self.r, kind="stable")
        self.rank = np.empty(NP, np.int64); self.rank[self.order] = np.arange(NP)

    # ---- accelerations (per unit mass, radial, incl. centrifugal)
    def accel(self):
        self.sort()
        r, k = self.r, self.rank
        if self.grav == "N":
            a = -G * Mb_enc(r) / r ** 2 - G * MU * (k + 0.5) * r / (r * r + EPS * EPS) ** 1.5     # A2 softened shells
            if self.lam > 0:
                inC = r < RC
                a = a - np.where(inC, self.lam * G * (Mph(r) - MU * (k + 0.5)) / (r * r + EPS * EPS), 0.0)
        else:
            um = G * (k + 0.5) * MU / r ** 2                     # A1: midpoint-in-mass push
            if np.any(um >= A0):
                self.flags.append(f"t={self.t:.3f}: u >= a0 for {int(np.sum(um >= A0))} shells")
            with np.errstate(divide="ignore"):
                push = np.where(um < A0, um * um / (A0 - um), np.inf)
            a = -g_b(r) + push
        return a + self.L ** 2 / r ** 3

    # ---- energies
    def KE(self):
        return 0.5 * MU * float(np.sum(self.v ** 2 + self.L ** 2 / self.r ** 2))
    def V_grav(self):
        if self.grav == "N":
            return MU * float(np.sum(Phi_b(self.r))) - G * MU * MU * float(np.sum((self.rank + 0.5) / np.sqrt(self.r ** 2 + EPS ** 2)))
        return MU * float(np.sum(Phi_b(self.r)))
    def V_set(self):
        rs = self.r[self.order]
        if self.grav == "S2":
            return V_tether_mid_sorted(rs)
        if self.lam > 0:
            return self.lam * F_settle_sorted(rs)
        return 0.0
    def energies(self):
        K, Vg, Vs = self.KE(), self.V_grav(), self.V_set()
        booked = K + Vg + (0.0 if self.mut == "notether" else Vs) + self.E_part
        return dict(K=K, Vg=Vg, Vs=Vs, E_part=self.E_part, E_tot=booked, E_matter=K + Vg + Vs)

    # ---- binned fields (catchment bins)
    def binned(self):
        r = self.r
        idx = np.searchsorted(EDGES, r, side="right") - 1
        inC = (r < RC) & (idx >= 0) & (idx < NB)
        cnt = np.bincount(idx[inC], minlength=NB).astype(float)
        Mcb = MU * cnt
        rhoc = Mcb / VOLB
        rhom = (DMB + Mcb) / VOLB
        tau = 1.0 / np.sqrt(4 * np.pi * G * rhom)
        d = np.maximum(DMPH - Mcb, 0.0)
        Md_edges = np.concatenate([[0.0], np.cumsum(d)])
        m_lo = np.concatenate([[0.0], np.cumsum(Mcb)[:-1]])
        gmid = G * (Mb_enc(RMID) + m_lo + 0.5 * Mcb) / RMID ** 2
        dr = np.diff(EDGES)
        col = rhoc * gmid * dr
        pJ = np.cumsum(col[::-1])[::-1] - 0.5 * col
        sigJ2 = np.where(rhoc > 0, pJ / np.where(rhoc > 0, rhoc, 1.0), 0.0)
        return dict(idx=idx, inC=inC, cnt=cnt, tau=tau, Md_edges=Md_edges, sigJ2=sigJ2)

    def drift_velocity(self, B):
        r = self.r; inC = B["inC"]
        tau_i = np.where(inC, B["tau"][np.clip(B["idx"], 0, NB - 1)], 0.0)
        if self.drift == "two":
            D = Mph(r) - MU * (self.rank + 0.5)
        else:
            D = np.interp(r, EDGES, B["Md_edges"])
        return np.where(inC, -ALPHA * tau_i * G * D / (r * r + EPS * EPS), 0.0)        # A2 softened kernel

    # ---- one step
    def choose_dt(self):
        dt = min(DTMAX, CA * float(np.min(np.sqrt(self.r / (np.abs(self.a) + 1e-300)))))
        if self.grav == "S2":
            # W_rem diverges at u = a0: an inward-moving shell may cover at most 10% of the gap to its own barrier
            # r_b = sqrt(G (k+1/2) mu / a0) per step (implementation fix with A1; disclosed)
            inw = self.v < 0
            if inw.any():
                gap = self.r[inw] - np.sqrt(G * (self.rank[inw] + 0.5) * MU / A0)
                dt = min(dt, 0.1 * float(np.min(np.maximum(gap, 0.0) / (-self.v[inw]))))
                if dt < 1e-10:
                    self.flags.append(f"t={self.t:.3f}: S2 barrier step floor hit"); dt = 1e-10
        if self.drift:
            mv = np.abs(self.vs) > 0
            if mv.any():
                dt = min(dt, CS * float(np.min(self.r[mv] / np.abs(self.vs[mv]))))
        return dt

    def reflect(self):
        m = self.r < RMIN
        if m.any():
            self.r[m] = 2 * RMIN - self.r[m]; self.v[m] = -self.v[m]

    def step(self, dt):
        self.v += 0.5 * dt * self.a
        self.r += dt * self.v
        self.reflect()
        self.a = self.accel()
        self.v += 0.5 * dt * self.a
        self.t += dt
        if self.drift:
            self.do_drift(dt)
        if self.bath:
            self.do_bath(dt)
        self.nsteps += 1

    def matter_E_nset(self):
        return self.KE() + self.V_grav()

    def do_drift(self, dt):
        B = self.binned()
        vs = self.drift_velocity(B)
        E0 = self.matter_E_nset()
        self.r = self.r + vs * dt
        self.reflect()
        self.a = self.accel()
        E1 = self.matter_E_nset()
        dE = E1 - E0
        self.vs = vs
        if self.mut == "nobook":
            self.flows["unbooked"] += dE
            return
        if self.heat:
            self.inject_heat(-dE, vs)
        else:                                          # R-d: partner takes the drift's energy change
            self.E_part -= dE
            if dE < 0: self.flows["drift_to_partner_pos"] += -dE
            else: self.flows["drift_to_partner_neg"] += -dE

    def inject_heat(self, Q, vs):
        mv = vs != 0
        if not mv.any() or Q == 0.0:
            if Q != 0.0: self.flags.append(f"t={self.t:.3f}: heat {Q:.3e} with no drifted shell")
            self.flows["unbooked"] += -Q
            return
        if Q > 0:
            w = np.abs(vs[mv]) * np.abs(self.a[mv])
            w = w / w.sum() if w.sum() > 0 else np.full(w.size, 1.0 / w.size)
            q = Q * w
            vv = self.v[mv]
            sg = np.sign(vv); z = sg == 0
            if z.any(): sg[z] = self.rng.choice([-1.0, 1.0], size=int(z.sum()))
            self.v[mv] = sg * np.sqrt(vv * vv + 2 * q / MU)
            self.heat_in += Q; self.flows["heat_pos"] += Q
            return
        else:
            need = -Q
            KEr = 0.5 * MU * float(np.sum(self.v[mv] ** 2))
            if KEr >= need:
                self.v[mv] *= math.sqrt(1.0 - need / KEr)
            else:
                self.v[mv] = 0.0; rest = need - KEr
                KEt = 0.5 * MU * float(np.sum(self.L[mv] ** 2 / self.r[mv] ** 2))
                if KEt >= rest:
                    self.L[mv] *= math.sqrt(1.0 - rest / KEt)
                else:
                    self.L[mv] = 0.0; self.flows["unbooked"] += rest - KEt
                    self.flags.append(f"t={self.t:.3f}: heat removal short by {rest - KEt:.3e}")
            self.heat_in += Q; self.flows["heat_neg"] += Q
            self.a = self.accel()                      # L may have changed (rare branch)

    def do_bath(self, dt):
        B = self.binned()
        inC, idx = B["inC"], np.clip(B["idx"], 0, NB - 1)
        ii = idx[inC]
        cnt = np.bincount(ii, minlength=NB).astype(float)
        v, L, r = self.v[inC], self.L[inC], self.r[inC]
        sv = np.bincount(ii, weights=v, minlength=NB)
        vbar = np.where(cnt > 0, sv / np.maximum(cnt, 1), 0.0)
        dv = v - vbar[ii]
        s3 = (np.bincount(ii, weights=dv * dv, minlength=NB) + np.bincount(ii, weights=L * L / (r * r), minlength=NB)) / np.maximum(cnt, 1)
        tgt = 3.0 * B["sigJ2"]
        gam = ALPHA / B["tau"]
        new = tgt + (s3 - tgt) * np.exp(-2.0 * gam * dt)
        act = (cnt >= 2) & (s3 > 0)
        if self.bath == "cool":
            act &= s3 > tgt
        f = np.where(act, np.sqrt(np.maximum(new, 0.0) / np.where(s3 > 0, s3, 1.0)), 1.0)
        K0 = self.KE()
        fi = f[ii]
        self.v[inC] = vbar[ii] + fi * dv
        self.L[inC] = fi * L
        self.a[inC] += (self.L[inC] ** 2 - L ** 2) / r ** 3     # only the centrifugal part changes (positions fixed)
        K1 = self.KE()
        dK = K1 - K0
        if self.mut == "nobook":
            self.flows["unbooked"] += dK
        else:
            self.E_part -= dK
            if dK < 0: self.flows["bath_to_partner_pos"] += -dK
            else: self.flows["bath_to_partner_neg"] += -dK

    # ---- measurement
    def measure(self):
        r = self.r
        cnt, _ = np.histogram(r, bins=SEDGES)
        m3 = MU * np.array([np.count_nonzero(r < R) for R in RM3])
        fesc = np.count_nonzero(r > RC) / NP
        X = None
        if self.grav == "N":
            B = self.binned()
            inS = (r >= SEDGES[0]) & (r <= SEDGES[-1])
            sj = B["sigJ2"][np.clip(B["idx"][inS], 0, NB - 1)]
            den = float(np.sum(sj))
            X = float(np.sum(self.v[inS] ** 2 + self.L[inS] ** 2 / r[inS] ** 2) / 3.0) / den if den > 0 else None
        e = self.energies()
        return dict(t=self.t, cnt=cnt.tolist(), m3=m3.tolist(), fesc=fesc, X=X, **e)

    def run(self, t_end, log_every=50.0):
        samples = [self.measure()]
        e0 = samples[0]
        Eref = abs(e0["K"]) + abs(e0["Vg"]) + abs(e0["Vs"]) + abs(e0["E_part"])
        next_s = 1.0; next_log = log_every; t0 = time.time()
        while self.t < t_end - 1e-12:
            dt = min(self.choose_dt(), t_end - self.t, next_s - self.t + 1e-12)
            self.step(dt)
            if self.t >= next_s - 1e-9:
                samples.append(self.measure()); next_s += 1.0
                if self.t >= next_log - 1e-9:
                    s = samples[-1]
                    print(f"  t {self.t:8.2f} steps {self.nsteps:8d} dE/Eref {(s['E_tot'] - e0['E_tot']) / Eref:+.3e} "
                          f"fesc {s['fesc']:.3f} m3 {np.round(s['m3'], 3).tolist()} wall {time.time() - t0:6.0f}s", flush=True)
                    next_log += log_every
        return samples, Eref

# ------------------------------------------------------------------ analysis of a run
def analyse(samples, Eref, t_end, lam=0.0):
    ts = np.array([s["t"] for s in samples])
    Et = np.array([s["E_tot"] for s in samples])
    eps = float(np.max(np.abs(Et - Et[0])) / Eref)
    def win(lo, hi):
        sel = (ts >= lo * t_end - 1e-9) & (ts <= hi * t_end + 1e-9)
        cnt = np.mean(np.array([samples[i]["cnt"] for i in np.where(sel)[0]]), axis=0)
        m3 = np.mean(np.array([samples[i]["m3"] for i in np.where(sel)[0]]), axis=0)
        rho = MU * cnt / SVOL
        with np.errstate(divide="ignore"):
            lr = np.log10(rho / SRHOPH)
        Xs = [samples[i]["X"] for i in np.where(sel)[0] if samples[i]["X"] is not None]
        return dict(D=float(np.median(lr)), logratio_bins=lr.tolist(), m3=m3.tolist(),
                    X=(float(np.mean(Xs)) if Xs else None), n=int(sel.sum()))
    W1, W2 = win(0.50, 0.75), win(0.75, 1.0)
    D, dD = W2["D"], W2["D"] - W1["D"]
    on_law = bool(np.isfinite(D) and abs(D) <= 0.1 and np.isfinite(dD) and abs(dD) <= 0.05)
    Mph3 = Mph(RM3)
    Xm = float(np.max(np.abs(np.log10(np.maximum(np.array(W2["m3"]), 1e-300) / Mph3))))
    out = dict(eps_E=eps, conserves_1e3=bool(eps <= 1e-3), D_W2=D, D_W1=W1["D"], dD=dD, on_law=on_law,
               X_m=Xm, m3_W2=W2["m3"], Mph3=Mph3.tolist(), fesc_end=samples[-1]["fesc"], X_W2=W2["X"],
               logratio_bins_W2=W2["logratio_bins"], E0=samples[0], E_end={k: samples[-1][k] for k in ("K", "Vg", "Vs", "E_part", "E_tot", "E_matter")})
    if lam > 0:
        m3 = np.array(W2["m3"])
        psi = G * (Mph3 - m3) / RM3 ** 2
        ab = lam * psi * dMph_dMb(RM3)
        out["baryon_reaction_over_glaw"] = (np.abs(ab) / g_law(RM3)).tolist()
        out["baryon_reaction_max"] = float(np.max(np.abs(ab) / g_law(RM3)))
    return out

# ------------------------------------------------------------------ parts
REPS = {"P0": dict(rep="K2"),                       # POST HOC (A2): pure N-type Vlasov, no settling (IC-L steadiness control)
        "Ra1": dict(rep="Ra1", lam=10.0), "Ra1x100": dict(rep="Ra1", lam=100.0), "Ra2": dict(rep="Ra2"),
        "Rb": dict(rep="Rb"), "Rc": dict(rep="Rc"), "Rd": dict(rep="Rd")}

def run_part(name, mut=None, t_override=None):
    key, ic = name.rsplit("_", 1)
    spec = REPS[key]
    sim = Sim(spec["rep"], ic, lam=spec.get("lam", 0.0), mut=mut)
    t_end = t_override if t_override else T_END[sim.grav][ic]
    print(f"[{name}] rep {spec['rep']} lam {spec.get('lam', 0.0)} ic {ic} grav {sim.grav} t_end {t_end} mut {mut}", flush=True)
    t0 = time.time()
    samples, Eref = sim.run(t_end)
    res = analyse(samples, Eref, t_end, lam=spec.get("lam", 0.0))
    res.update(part=name, rep=spec["rep"], lam=spec.get("lam", 0.0), ic=ic, grav=sim.grav, t_end=t_end, Eref=Eref,
               steps=sim.nsteps, wall_s=time.time() - t0, flows=sim.flows, heat_in=sim.heat_in, flags=sim.flags[:20],
               nflags=len(sim.flags), mut=mut, E_init_matter=samples[0]["E_matter"],
               series=dict(t=[s["t"] for s in samples[::5]], E_tot=[s["E_tot"] for s in samples[::5]],
                           m3=[s["m3"] for s in samples[::5]], fesc=[s["fesc"] for s in samples[::5]]))
    return res

# ---- K0: CFG932's drift test, verbatim copy (G = 1 units; NFW cold; Plummer; a0 0.05; two-sided)
def mfun(x):
    """ln(1+x) - x/(1+x), with its series below x = 1e-3 (no cancellation)."""
    x = np.asarray(x, float)
    xs = np.minimum(x, 1e-3)
    ser = xs ** 2 / 2 - 2 * xs ** 3 / 3 + 3 * xs ** 4 / 4 - 4 * xs ** 5 / 5
    with np.errstate(divide='ignore', invalid='ignore'):
        full = np.log1p(x) - x / (1 + x)
    return np.where(x < 1e-3, ser, full)

def drift_test(two_sided, t_end=200.0, maxsteps=3_000_000, exact_book=False):
    G = 1.0; N = 400; alpha = 1.0
    rf = np.geomspace(1e-3, 30.0, N + 1); V = 4 * math.pi / 3 * np.diff(rf ** 3); A = 4 * math.pi * rf ** 2
    rc = np.sqrt(rf[1:] * rf[:-1])
    Mbf = rf ** 3 / (rf ** 2 + 1.0) ** 1.5; Mb_in = Mbf[0]; mb = np.diff(Mbf); rhob = mb / V
    a0 = 0.05
    Mphf = Mbf / np.expm1(np.sqrt(Mbf / (rf ** 2 * a0))); rhoph = np.diff(Mphf) / V
    Mcf = 30.0 * mfun(rf / 3.0) / float(mfun(10.0)); mc = np.diff(Mcf).copy(); mc[0] += Mcf[0]
    def W_Phi(mc):
        mt = mb + mc; Sinc = Mb_in + np.cumsum(mt)
        W = -G * float(np.sum((Sinc - 0.5 * mt) * mt / rc))
        tail = np.cumsum((mt / rc)[::-1])[::-1] - mt / rc
        return W, -G * (Sinc / rc + tail)
    # central surplus zone at t = 0: first face where cumulative cold < phantom
    cum0 = np.cumsum(mc)
    below = cum0[:-1] < Mphf[1:N]
    k1 = int(np.argmax(below)) + 1 if below.any() else N
    Mcen0 = float(mc[:k1].sum())
    W0, Phi = W_Phi(mc); t = 0.0; n = 0; Pacc = Pout = Pin = 0.0
    Pmid = 0.0; clipped = 0
    while t < t_end and n < maxsteps:
        rho = mc / V; rhom = rho + rhob
        cin = np.cumsum(mc)[:-1]                                   # cold mass inside internal faces 1..N-1
        if two_sided:
            dpsi = G * (Mphf[1:N] - cin) / rf[1:N] ** 2
        else:
            d = np.maximum(rhoph - rho, 0.0); Md = np.cumsum(d * V)[:-1]
            dpsi = G * Md / rf[1:N] ** 2
        out_dir = dpsi < 0                                         # v = -alpha tau dpsi > 0 -> outward, donor = inner cell
        donor = np.where(out_dir, np.arange(0, N - 1), np.arange(1, N))
        tau = 1.0 / np.sqrt(4 * math.pi * G * np.maximum(rhom[donor], 1e-300))
        v = -alpha * tau * dpsi
        flux = v * rho[donor] * A[1:N]
        act = np.abs(flux) > 0
        if not act.any(): break
        lim = V[donor][act] / (np.abs(v[act]) * A[1:N][act])
        dt = min(0.2 * float(lim.min()), t_end - t)
        dm = flux * dt
        P = dm * (Phi[1:] - Phi[:-1])
        Pacc += float(P.sum()); Pout += float(P[dm > 0].sum()); Pin += float(P[dm < 0].sum())
        mc[:-1] -= dm; mc[1:] += dm
        if exact_book and np.any(mc < 0): clipped += 1
        mc = np.maximum(mc, 0.0)
        Phi_old = Phi
        _, Phi = W_Phi(mc); t += dt; n += 1
        if exact_book:
            Pb = 0.5 * (Phi_old + Phi)
            Pmid += float(np.sum(dm * (Pb[1:] - Pb[:-1])))
    W1, _ = W_Phi(mc)
    dW = W1 - W0
    inner = slice(0, k1)
    out = dict(two_sided=two_sided, t_end=t, steps=n, W0=W0, dW=dW, dW_over_absW0=dW / abs(W0), int_P_dt=Pacc,
               identity_rel=abs(dW - Pacc) / max(abs(dW), 1e-300), int_P_outward=Pout, int_P_inward=Pin,
               central_zone_r=float(rf[k1]), central_mass_t0=Mcen0, central_mass_end=float(mc[inner].sum()),
               mass_err=abs(mc.sum() - (Mcf[-1])) / Mcf[-1])
    if exact_book:
        out.update(int_Pmid_dt=Pmid, exact_closure_over_absW0=abs(dW - Pmid) / abs(W0), clipped_steps=clipped,
                   E_X_end=-Pmid, W_plus_EX_change_over_absW0=abs((W1 - Pmid) - W0) / abs(W0))
    return out

def part_K0():
    rec = dict(dW_over_absW0=0.5926642444000018, identity_rel=0.0018633353183663936)
    d = drift_test(True)
    e = drift_test(True, exact_book=True)
    k0 = (abs(d["dW_over_absW0"] / rec["dW_over_absW0"] - 1) <= 1e-9 and abs(d["identity_rel"] / rec["identity_rel"] - 1) <= 1e-9)
    k0b = e["exact_closure_over_absW0"] <= 1e-12 and e["clipped_steps"] == 0
    print(f"K0  CFG932 drift test (verbatim copy): dW/|W0| {d['dW_over_absW0']:.16f} (record {rec['dW_over_absW0']:.16f}), "
          f"identity {d['identity_rel']:.10e} (record {rec['identity_rel']:.10e}): {'PASS' if k0 else 'FAIL'}")
    print(f"K0b exact discrete-gradient bookkeeping: |dW - int P_mid dt|/|W0| = {e['exact_closure_over_absW0']:.2e} "
          f"(explicit accounting {abs(e['dW'] - e['int_P_dt']) / abs(e['W0']):.2e}), clipped steps {e['clipped_steps']}: {'PASS' if k0b else 'FAIL'}")
    return dict(part="K0", record=rec, K0=d, K0b=e, K0_pass=bool(k0), K0b_pass=bool(k0b))

def part_K2():
    sim = Sim("K2", "I")
    print(f"[K2] pure N-type Vlasov on IC-I, t_end 200", flush=True)
    t0 = time.time()
    samples, Eref = sim.run(200.0)
    ts = np.array([s["t"] for s in samples]); Et = np.array([s["E_tot"] for s in samples])
    eps = float(np.max(np.abs(Et - Et[0])) / Eref)
    print(f"K2 eps_E = {eps:.3e} (<= 1e-3: {'PASS' if eps <= 1e-3 else 'FAIL'}), steps {sim.nsteps}, wall {time.time() - t0:.0f}s")
    return dict(part="K2", eps_E=eps, pass_=bool(eps <= 1e-3), steps=sim.nsteps, Eref=Eref, wall_s=time.time() - t0,
                knobs=dict(RMIN=RMIN, DTMAX=DTMAX, CA=CA, CS=CS, EPS=EPS))

def part_ETH():
    """Energy theorem: E_init per IC and type; E_law(M) curves; excess Delta E_x and f_esc,max (A0.2)."""
    rng = np.random.default_rng(SEED)
    Ms = np.linspace(0.05, 1.0, 39) * MC
    def law_particles(M):
        n = int(round(NP * M / MC))
        return Minv(MU * (np.arange(n) + 0.5))
    def V_N_sorted(rs):
        k = np.arange(rs.size)
        return MU * float(np.sum(Phi_b(rs))) - G * MU * MU * float(np.sum((k + 0.5) / np.sqrt(rs ** 2 + EPS ** 2)))
    def V_S2_sorted(rs):
        return MU * float(np.sum(Phi_b(rs))) + V_tether_mid_sorted(rs)
    curves = {"N": [], "Ra1x10": [], "Ra1x100": [], "S2": []}
    for M in Ms:
        rs = law_particles(M)
        VN = V_N_sorted(rs); KJ = K_jeans_law(rs.size * MU)
        F = F_settle_sorted(rs)
        curves["N"].append(VN + KJ); curves["Ra1x10"].append(VN + KJ + 10.0 * F); curves["Ra1x100"].append(VN + KJ + 100.0 * F)
        curves["S2"].append(V_S2_sorted(rs))
    curves = {k: np.array(v) for k, v in curves.items()}
    mono = {k: bool(np.all(np.diff(v) < 0)) for k, v in curves.items()}
    # E_init per IC per type (from the actual particle ICs, matter energy)
    einit = {}
    for typ, rep, lam in (("N", "Rb", 0.0), ("Ra1x10", "Ra1", 10.0), ("Ra1x100", "Ra1", 100.0), ("S2", "Ra2", 0.0)):
        for ic in ("L", "I", "S"):
            sim = Sim(rep, ic, lam=lam)
            einit[f"{typ}|{ic}"] = sim.energies()["E_matter"]
    res = {}
    for key, E0 in einit.items():
        typ, ic = key.split("|")
        cur = curves[typ]; Elaw_full = float(cur[-1])
        dEx = E0 - Elaw_full
        if dEx < 0:
            res[key] = dict(E_init=E0, E_law_Mc=Elaw_full, excess=dEx, excess_frac=dEx / abs(Elaw_full), f_esc_max=None,
                            note="energy deficit: the law is unreachable without an energy input")
            continue
        if E0 >= cur[0]:
            fmax = 1.0 - Ms[0] / MC; note = "E_init above E_law(0.05 M_c): f_esc,max >= 0.95"
        else:
            # cur decreasing in M: find M_x with cur(M_x) = E0
            Mx = float(np.interp(E0, cur[::-1], Ms[::-1])); fmax = 1.0 - Mx / MC; note = ""
        res[key] = dict(E_init=E0, E_law_Mc=Elaw_full, excess=dEx, excess_frac=dEx / abs(Elaw_full), f_esc_max=fmax, note=note)
    for k, v in res.items():
        print(f"ETH {k:12s} E_init {v['E_init']:+.5e}  E_law(M_c) {v['E_law_Mc']:+.5e}  excess {v['excess']:+.4e} "
              f"({v['excess_frac']:+.3f} of |E_law|)  f_esc,max {v['f_esc_max']}  {v['note']}")
    # S2 static-state residual (K1 part)
    rs = s2_static_positions()
    sim = Sim("Ra2", "L")
    resid = float(np.max(np.abs(sim.a) / g_b(sim.r)))
    print(f"K1 S2 discrete static law: max |a|/g_b = {resid:.2e} (<= 1e-10: {'PASS' if resid <= 1e-10 else 'FAIL'}); "
          f"r_last {rs[-1]:.6f} (continuum r_* {RSTAR})")
    return dict(part="ETH", Ms=Ms.tolist(), curves={k: v.tolist() for k, v in curves.items()}, monotone=mono, results=res,
                K1_S2_residual=resid, K1_S2_pass=bool(resid <= 1e-10), r_last_S2=float(rs[-1]), M_c=MC)

def part_PHYS():
    """Physical tables (both footings): CFG932 excess energies; CFG630 cosmic exchange; CFG689 cited."""
    G_cgs, Msun, kpc, c_cgs = 6.674e-8, 1.989e33, 3.0857e21, 2.99792458e10
    p932 = os.path.join(HERE, "..", "CFG932_settling_energy_bookkeeping", "cfg932_results.json")
    p630 = os.path.join(HERE, "..", "CFG630_settling_feeds_dark_energy", "cfg630_results.json")
    d932 = json.load(open(p932)); d630 = json.load(open(p630))
    fb = d932["settings"]["f_b"]
    tab = {}
    for fk in ("can", "alt"):
        g = d932["grid"][f"{fk}|EPS0.05|L1"]
        rows = {}
        for sysn, x in g.items():
            Mb = x["M_ta"] * x["f_ret"] * fb / x["L"]
            Ex = -x["dE_a_tot_erg"]; Exb = -x["dE_b_tot_erg"]
            Phi = G_cgs * (Mb + x["M_cat"]) * Msun / (x["r_star_kpc"] * kpc)
            rows[sysn] = dict(M_b=Mb, M_cat=x["M_cat"], r_star_kpc=x["r_star_kpc"], E_x_a_erg=Ex, E_x_b_erg=Exb,
                              E_x_over_Mcat_c2=Ex / (x["M_cat"] * Msun * c_cgs ** 2),
                              E_x_over_Mcat_Phi=Ex / (x["M_cat"] * Msun * Phi),
                              f_esc_max_est=Ex / (x["M_cat"] * Msun * Phi))
        tab[fk] = rows
    h = d630["inputs"]["h"]; rhoDE0 = d630["inputs"]["rho_DE0"]
    H0 = 100 * h * 1e5 / 3.0857e24
    rho_crit = 3 * H0 ** 2 / (8 * math.pi * G_cgs)          # g/cm^3 (CFG630 rho in kg/m^3 -> convert)
    Om_DE = rhoDE0 * 1e-3 / rho_crit
    Om_gamma = 2.473e-5 / h ** 2                              # T_CMB = 2.7255 K (declared)
    cos = {}
    for fk in ("can", "alt"):
        lo, hi = d630["brackets"][fk]["drho_z1"]
        cos[fk] = dict(drho_DE_over_rhoDE_z1=[lo, hi], Omega_rad_new_max=[lo * Om_DE, hi * Om_DE],
                       Omega_rad_new_over_Omega_gamma=[lo * Om_DE / Om_gamma, hi * Om_DE / Om_gamma],
                       dlog10_a0_from_tracking=[0.5 * math.log10(1 + lo), 0.5 * math.log10(1 + hi)])
    cited689 = dict(source="LEDGER row CFG689 (record text)", a0z_over_a00_z1_primary=[0.91, 0.76, 1.03],
                    constant_DE_rejection_sigma_primary=1.97, verdict="constant DE NOT rejected")
    for fk in ("can", "alt"):
        print(f"PHYS {fk}: " + "; ".join(f"{s} E_x {r['E_x_a_erg']:.2e} erg, E_x/(M_cat|Phi*|) {r['E_x_over_Mcat_Phi']:.3f}, "
                                          f"E_x/(M_cat c^2) {r['E_x_over_Mcat_c2']:.1e}" for s, r in tab[fk].items()))
        print(f"PHYS {fk}: CFG630 drho_DE/rho_DE since z=1 {cos[fk]['drho_DE_over_rhoDE_z1']}, R-c Omega_rad,new <= "
              f"{cos[fk]['Omega_rad_new_max']} ({cos[fk]['Omega_rad_new_over_Omega_gamma']} of Omega_gamma)")
    return dict(part="PHYS", systems=tab, cosmic=cos, Omega_DE=Om_DE, Omega_gamma=Om_gamma, cited_CFG689=cited689)

MAIN_RUNS = ["Ra1_L", "Ra1_I", "Ra1_S", "Ra1x100_I", "Ra2_L", "Ra2_I", "Ra2_S", "Rb_L", "Rb_I", "Rb_S",
             "Rc_L", "Rc_I", "Rc_S", "Rd_L", "Rd_I", "Rd_S"]

def jsonable(x):
    if isinstance(x, dict): return {k: jsonable(v) for k, v in x.items()}
    if isinstance(x, (list, tuple)): return [jsonable(v) for v in x]
    if isinstance(x, np.floating): return float(x)
    if isinstance(x, np.integer): return int(x)
    if isinstance(x, np.bool_): return bool(x)
    if isinstance(x, np.ndarray): return jsonable(x.tolist())
    if isinstance(x, float) and not math.isfinite(x): return str(x)
    return x

def save_part(name, res):
    os.makedirs(PARTS, exist_ok=True)
    json.dump(jsonable(res), open(os.path.join(PARTS, f"{name}.json"), "w"), indent=1)

# ------------------------------------------------------------------ classification and summary
def classify(P):
    """FROZEN_CRITERIA §4. P: dict part -> result."""
    reps = {"R-a(i)": ["Ra1_L", "Ra1_I", "Ra1_S", "Ra1x100_I"], "R-a(ii)": ["Ra2_L", "Ra2_I", "Ra2_S"],
            "R-b": ["Rb_L", "Rb_I", "Rb_S"], "R-c": ["Rc_L", "Rc_I", "Rc_S"], "R-d": ["Rd_L", "Rd_I", "Rd_S"]}
    new_physics = {"R-a(i)": "new constant lambda (stiffness of the settling energy) and a mediator for +F (CFG542 Pc2: a healthy scalar gives -F)",
                   "R-a(ii)": None, "R-b": None,
                   "R-c": "a new gapless radiation field coupled to cold energy (the record's P field is gapped: CFG760-762) plus the cooling law",
                   "R-d": "a dynamical dark-energy partner (exact Lambda cannot exchange; a canonical partner is singular at w = -1, CFG542 K10)"}
    pre = {"R-a(i)": "Ra1", "R-a(ii)": "Ra2", "R-b": "Rb", "R-c": "Rc", "R-d": "Rd"}
    out = {}
    for R, parts in reps.items():
        p = pre[R]
        cons = all(P[q]["eps_E"] <= 1e-3 for q in parts)
        b = P[f"{p}_L"]["on_law"]
        c = P[f"{p}_I"]["on_law"]
        if R == "R-a(i)":
            c = c and P["Ra1_I"].get("baryon_reaction_max", 1e9) <= 0.1
        ok = cons and b and c
        if not ok: cls = "NOT VIABLE"
        elif new_physics[R]: cls = "VIABLE-WITH-COST"
        else: cls = "VIABLE"
        fails = [n for n, f in (("(a) conservation", cons), ("(b) IC-L equilibrium", b), ("(c) IC-I infall / record passes", c)) if not f]
        out[R] = dict(cls=cls, a=bool(cons), b=bool(b), c=bool(c), fails=fails, cost=new_physics[R],
                      eps_E_max=max(P[q]["eps_E"] for q in parts))
    clss = [v["cls"] for v in out.values()]
    overall = "REPAIR FOUND" if "VIABLE" in clss else ("REPAIR NEEDS NEW PHYSICS" if "VIABLE-WITH-COST" in clss else "NO REPAIR")
    return out, overall

def summary_main():
    P = {}
    for n in ["K0", "K2", "ETH", "PHYS"] + MAIN_RUNS:
        f = os.path.join(PARTS, f"{n}.json")
        if not os.path.exists(f):
            print(f"missing part {n}"); sys.exit(2)
        P[n] = json.load(open(f))
    L = []
    def log(s=""):
        print(s, flush=True); L.append(s)
    log(f"CFG935: minimal energy-conserving settling (criteria {CRITERIA}; amendments A0 {AMEND_A0}, A1 {AMEND_A1}, A2 {AMEND_A2})")
    log(f"toy: G = a0 = 1, Plummer M_b 1 a 1, simple nu, r_* {RSTAR}, M_c = Mph(<r_*) = {MC:.6f}, R_C {RC}, alpha {ALPHA}, N {NP}; "
        f"T_edge N {T_EDGE['N']:.2f} / S2 {T_EDGE['S2']:.2f}; knobs RMIN {RMIN} DTMAX {DTMAX} CA {CA} CS {CS} EPS {EPS} (A2)")
    k0 = P["K0"]
    log(f"K0  CFG932 drift test reproduced: dW/|W0| {k0['K0']['dW_over_absW0']:.16f}, identity {k0['K0']['identity_rel']:.10e}: "
        f"{'PASS' if k0['K0_pass'] else 'FAIL'}; K0b exact bookkeeping closure {k0['K0b']['exact_closure_over_absW0']:.2e}: "
        f"{'PASS' if k0['K0b_pass'] else 'FAIL'}")
    log(f"K1  S2 static residual {P['ETH']['K1_S2_residual']:.2e}: {'PASS' if P['ETH']['K1_S2_pass'] else 'FAIL'} (the IC-L gates are criterion (b))")
    log(f"K2  pure N-type Vlasov IC-I eps_E {P['K2']['eps_E']:.3e}: {'PASS' if P['K2']['pass_'] else 'FAIL'}")
    log("")
    log("runs: part | eps_E | D(W2) | dD | ON THE LAW | X_m | f_esc | X(N) | flows")
    for n in MAIN_RUNS:
        r = P[n]
        fl = r["flows"]
        extra = ""
        if r["rep"] in ("Rb", "Rc"): extra += f" heat {r['heat_in']:+.3f}"
        if r["rep"] in ("Rc", "Rd"): extra += f" E_part {r['E_end']['E_part']:+.3f}"
        if r["rep"] == "Rd": extra += f" (drift +{fl['drift_to_partner_pos']:.3f}/{fl['drift_to_partner_neg']:+.3f}, bath +{fl['bath_to_partner_pos']:.3f}/{fl['bath_to_partner_neg']:+.3f})"
        if "baryon_reaction_max" in r: extra += f" baryon reaction max {r['baryon_reaction_max']:.3f} g_law"
        X = f"{r['X_W2']:.2f}" if r.get("X_W2") is not None else "-"
        log(f"  {n:10s} {r['eps_E']:.2e} {r['D_W2']:+.3f} {r['dD']:+.3f} {str(r['on_law']):5s} {r['X_m']:.3f} {r['fesc_end']:.3f} {X:>6s}{extra}"
            + (f"  flags {r['nflags']}" if r['nflags'] else ""))
    log("")
    eth = P["ETH"]["results"]
    log("energy theorem (A0.2): excess = E_init - E_law(M_c) (fraction of |E_law|), f_esc,max (zero-energy escapers)")
    for k, v in eth.items():
        log(f"  {k:12s} excess {v['excess']:+.4e} ({v['excess_frac']:+.3f})  f_esc,max {v['f_esc_max']}  {v['note']}")
    cl, overall = classify(P)
    log("")
    for R, v in cl.items():
        log(f"CLASS {R:8s}: {v['cls']}  (a {v['a']}, b {v['b']}, c {v['c']}; eps_E max {v['eps_E_max']:.2e})"
            + (f"  fails: {', '.join(v['fails'])}" if v['fails'] else "") + (f"  cost: {v['cost']}" if v['cost'] and v['cls'] != 'NOT VIABLE' else ""))
    log(f"OVERALL: {overall}")
    # ---- post hoc, no class weight
    ph = {}
    f0 = os.path.join(PARTS, "P0_L.json")
    if os.path.exists(f0):
        r = json.load(open(f0)); ph["P0_L"] = {k: v for k, v in r.items() if k != "series"}
        log(f"POST HOC P0_L (pure N-type Vlasov on IC-L, no settling): eps_E {r['eps_E']:.2e} D(W2) {r['D_W2']:+.3f} dD {r['dD']:+.3f} "
            f"ON THE LAW {r['on_law']} X_m {r['X_m']:.3f} f_esc {r['fesc_end']:.3f} X {r['X_W2']}")
    for n in ("preA2_Rd_L", "preA2_Rd_I"):
        f1 = os.path.join(PARTS, f"{n}.json")
        if os.path.exists(f1):
            r = json.load(open(f1)); ph[n] = {k: v for k, v in r.items() if k != "series"}
            log(f"PRE-A2 record {n} (frozen thin-shell kernels): eps_E {r['eps_E']:.2e} D(W2) {r['D_W2']:+.3f} ON THE LAW {r['on_law']} "
                f"X_m {r['X_m']:.3f} m3 {[round(x, 3) for x in r['m3_W2']]}")
    log("kappa = 1/2 FITTED; footings never pooled (physical tables per footing in PHYS); cold energy mass required; not theory closed.")
    res = dict(lane="CFG935", criteria=CRITERIA, amendment_A0=AMEND_A0, toy=dict(M_c=MC, T_edge=T_EDGE, T_end=T_END,
               knobs=dict(RMIN=RMIN, DTMAX=DTMAX, CA=CA, CS=CS, EPS=EPS)), parts={k: {kk: vv for kk, vv in v.items() if kk != "series"} for k, v in P.items()},
               classes=cl, overall=overall, post_hoc=ph, amendment_A1=AMEND_A1, amendment_A2=AMEND_A2)
    json.dump(jsonable(res), open(os.path.join(HERE, "cfg935_results.json"), "w"), indent=1)
    open(os.path.join(HERE, "cfg935.out"), "w").write("\n".join(L) + "\n")
    ok_controls = P["K0"]["K0_pass"] and P["K0"]["K0b_pass"] and P["ETH"]["K1_S2_pass"] and P["K2"]["pass_"]
    sys.exit(0 if ok_controls else 1)

def mutate_main():
    L = []
    def log(s=""):
        print(s, flush=True); L.append(s)
    log(f"CFG935 MUTATE (criteria {CRITERIA}): bookkeeping switched off; each must show |dE|/E_ref >= 1e-3")
    R = {}
    for tag, name, mut in (("M1", "Rd_I", "nobook"), ("M2", "Rb_I", "nobook"), ("M3", "Ra2_I", "notether")):
        r = run_part(name, mut=mut, t_override=100.0)
        bites = r["eps_E"] >= 1e-3
        R[tag] = dict(part=name, mut=mut, eps_E=r["eps_E"], bites=bool(bites), flows=r["flows"], E0=r["E0"], E_end=r["E_end"])
        log(f"{tag} {name} ({mut}): |dE|/E_ref max {r['eps_E']:.3e} -> {'BITES' if bites else 'DOES NOT BITE'}; unbooked {r['flows']['unbooked']:+.4e}")
    allb = all(v["bites"] for v in R.values())
    log(f"MUTATE: {'all three bite' if allb else 'NOT all bite'} -> exit {1 if allb else 0}")
    json.dump(jsonable(dict(lane="CFG935", mutate=True, criteria=CRITERIA, results=R, all_bite=allb, exit=1 if allb else 0)),
              open(os.path.join(HERE, "cfg935_results_MUTATE.json"), "w"), indent=1)
    open(os.path.join(HERE, "cfg935_MUTATE.out"), "w").write("\n".join(L) + "\n")
    sys.exit(1 if allb else 0)

if __name__ == "__main__":
    if os.path.exists(os.path.join(PARTS, "STOP")):
        print("parts/STOP present: part skipped"); sys.exit(3)
    if MUT:
        mutate_main()
    part = sys.argv[1] if len(sys.argv) > 1 else "summary"
    if part == "summary":
        summary_main()
    elif part == "K0":
        save_part("K0", part_K0())
    elif part == "K2":
        save_part("K2", part_K2())
    elif part == "ETH":
        save_part("ETH", part_ETH())
    elif part == "PHYS":
        save_part("PHYS", part_PHYS())
    elif part in MAIN_RUNS or part == "P0_L":
        save_part(part, run_part(part))
    else:
        print(f"unknown part {part}"); sys.exit(2)
