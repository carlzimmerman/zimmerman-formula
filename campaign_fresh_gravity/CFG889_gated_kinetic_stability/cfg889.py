#!/usr/bin/env python3
"""CFG889 -- is CFG639's deficit gate dynamically sound once orbits mix?  Criteria: FROZEN_CRITERIA.md (0337ade83, committed alone first).

Spherical shell particle code: Vlasov in the total Newtonian potential (static Plummer baryons + the cold particles' own mass), plus the
record's drift (CFG544 FIX-1 two-sided psi; positions move at fixed (v_r, v_t)) and FIX-2 OU relaxation (rate alpha/tau, target the
Jeans dispersion of the current density), gated chi = 1[d > 0] per radial bin (CFG639 HG), ungated chi = 1, or inverted (MUTATE).
Start: isotropic Eddington equilibrium of the law-settled halo (rho_c = rho_tgt = round-rule phantom x catchment taper) plus CFG877's
clump with a smooth cap.  kappa = 1/2 FITTED; footings never pooled; cold energy is real mass; not theory closed.

Run one part per process (each < 10 min, one core, < 2 GB):
  OMP_NUM_THREADS=1 nice -n 10 python3 cfg889.py <part>      parts: K G1a G1b G2a G2b U1 U2 N1 N2 H1 H3 S
  CFG889_MUTATE=1 OMP_NUM_THREADS=1 nice -n 10 python3 cfg889.py M   then   ... cfg889.py S   (MUTATE summary exits 1 by design)
  POST-HOC (added 2026-10-20 after the frozen parts had run; no class weight): parts P1 (no-OU, no-drift, alpha 0.05, mass-conserving
  comb, OU-target diagnosis) and P2 (no-OU at N x 4); the summary prints them in a separate post-hoc section.
Part results go to parts/part_<P>[_MUTATE].json; the summary writes cfg889[_MUTATE].out and cfg889_results[_MUTATE].json.
"""
import os, sys, json, math, time
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__)); LANES = os.path.dirname(HERE)
MUT = os.environ.get("CFG889_MUTATE", "") == "1"; SUF = "_MUTATE" if MUT else ""
PARTS = os.path.join(HERE, "parts"); os.makedirs(PARTS, exist_ok=True)
OUT = []
def P(s=""):
    print(s, flush=True); OUT.append(str(s))

# ------------------------------------------------------------------ units: pc, Msun, Myr
PC, MSUN, MYR, G_SI = 3.0857e16, 1.989e30, 3.15576e13, 6.674e-11
G = G_SI * MSUN * MYR ** 2 / PC ** 3
KMS = 1e3 * MYR / PC
A0 = {"canonical": 9.3603e-11 * MYR ** 2 / PC, "alt": 1.1312e-10 * MYR ** 2 / PC}
FOOTS = ("canonical", "alt")
R877 = json.load(open(os.path.join(LANES, "CFG877_finite_cold_clump", "cfg877_results.json")))
CL = {f: dict(Vx=R877[f]["Vx"] * KMS, Mcl=R877[f]["Mcl_Msun"], rt=R877[f]["rt_pc"]) for f in FOOTS}
RC, NCAP = 104.0, 4
R1, R2 = 3000.0, 5000.0
HOSTS = {"H1": (1e4, 30.0), "H2": (3e5, 200.0), "H3": (2e7, 700.0)}
NTARGET = {"H1": 1e5, "H2": 1e5, "H3": 2e5}
T_RUN, DT, ETA, NMAX, RMIN = 1500.0, 0.5, 0.05, 4096, 1e-2
SNAP, FINE_T = 10.0, 200.0
S50_882 = {"canonical": 10.37, "alt": 8.58}           # CFG882 V1 H2 s_50 (Myr at alpha = 1)
nu = lambda y: 1.0 / (-np.expm1(-np.sqrt(np.maximum(y, 1e-300))))

# gate bins: faces {0} U geomspace(2 pc, R2, 160) -> 160 bins
GF = np.concatenate([[0.0], np.geomspace(2.0, R2, 160)]); NBG = GF.size - 1
LGB0, DLGB = math.log(2.0), math.log(R2 / 2.0) / 159
GV = 4 * math.pi / 3 * np.diff(GF ** 3); GDR = np.diff(GF)
GRC = np.concatenate([[1.0], np.sqrt(GF[1:-1] * GF[2:])])
XI = np.clip(np.random.default_rng(889).standard_normal(NBG), -3, 3)
def gbin(r):
    """gate-bin index; NBG for r >= R2 (outside the catchment)"""
    k = np.where(r < 2.0, 0, 1 + np.floor((np.log(np.maximum(r, 1e-300)) - LGB0) / DLGB).astype(np.int64))
    k = np.where(r < 2.0, 0, np.clip(k, 1, NBG - 1))
    return np.where(r >= R2, NBG, k)

# enclosed-mass / potential table
LG0, LG1, NG = math.log(1e-2), math.log(2.0e5), 24000
DLG = (LG1 - LG0) / NG
RG = np.exp(LG0 + DLG * np.arange(NG + 1))


def taper(r):
    x = np.clip((r - R1) / (R2 - R1), 0, 1)
    return np.cos(0.5 * math.pi * x) ** 2


# ------------------------------------------------------------------ equilibrium (Eddington)
class Eq:
    def __init__(self, foot, host, clump=True, ng=8000):
        self.foot, self.host, self.clump = foot, host, clump
        Mb, a = HOSTS[host]; self.Mb, self.a = Mb, a
        a0 = A0[foot]
        r = np.geomspace(1e-3, R2, ng); self.r = r
        Mbr = Mb * r ** 3 / (r ** 2 + a ** 2) ** 1.5
        Mph = (nu(G * Mbr / (r ** 2 * a0)) - 1.0) * Mbr
        self.rho_t = np.maximum(np.gradient(Mph, r), 0) / (4 * math.pi * r ** 2) * taper(r)
        dM = 4 * math.pi * r ** 2 * self.rho_t
        self.Mt = np.concatenate([[0.0], np.cumsum(0.5 * (dM[1:] + dM[:-1]) * np.diff(r))]) + Mph[0]
        if clump:
            c = CL[foot]
            u = c["Vx"] ** 2 * r ** 3 / (G * (r ** 2 + RC ** 2)) / c["Mcl"]
            self.Mx = c["Mcl"] * u / (1 + u ** NCAP) ** (1.0 / NCAP)
            self.rho_x = np.gradient(self.Mx, r) / (4 * math.pi * r ** 2)
        else:
            self.Mx = np.zeros_like(r); self.rho_x = np.zeros_like(r)
        self.Mbr = Mbr; self.rho_c = self.rho_t + self.rho_x
        Mtot = Mbr + self.Mt + self.Mx
        Mc_inf = self.Mt[-1] + self.Mx[-1]
        gr = G * Mtot / r ** 2
        seg = 0.5 * (gr[1:] + gr[:-1]) * np.diff(r)
        Phi_R2 = -G * Mc_inf / R2 - G * Mb / math.sqrt(R2 ** 2 + a ** 2)
        self.Psi = -np.concatenate([Phi_R2 - np.cumsum(seg[::-1])[::-1], [Phi_R2]])
        self.Psi2 = self.Psi[-1]
        self.Mtgt_tot = float(self.Mt[-1])
        self._edd()

    def _edd(self, nE=6000, nt=600):
        Psi, rho = self.Psi[::-1], self.rho_c[::-1]
        drho = np.maximum(np.gradient(rho, Psi), 0.0)
        Emin, Emax = self.Psi2, Psi[-1]
        s = np.linspace(0, 1, nE)
        E = Emin + (Emax - Emin) * 0.5 * (1 - np.cos(math.pi * s))
        F = np.zeros(nE)
        for i in range(1, nE):
            t = np.linspace(0, math.sqrt(E[i] - Emin), nt)
            F[i] = np.trapz(2 * np.interp(E[i] - t ** 2, Psi, drho), t)
        self.E = E; self.f = np.gradient(F, E) / (math.sqrt(8) * math.pi ** 2)

    def rho_from_f(self, rr):
        out = []
        for x in rr:
            ps = np.interp(x, self.r, self.Psi); vmax = math.sqrt(max(2 * (ps - self.Psi2), 0))
            v = np.linspace(0, vmax, 4000)
            out.append(4 * math.pi * np.trapz(np.interp(ps - 0.5 * v ** 2, self.E, self.f, left=0) * v ** 2, v))
        return np.array(out)

    def velocities(self, rad, u, mu, nq=500, nrn=1000):
        rn = np.geomspace(max(rad.min(), 1e-3), max(rad.max(), 1.0001 * max(rad.min(), 1e-3)), nrn)
        q = np.linspace(0, 1, nq)
        cdf = np.zeros((nrn, nq)); vmx = np.zeros(nrn)
        for k, x in enumerate(rn):
            ps = np.interp(x, self.r, self.Psi); vmax = math.sqrt(max(2 * (ps - self.Psi2), 1e-30)); vmx[k] = vmax
            p = np.maximum(np.interp(ps - 0.5 * (q * vmax) ** 2, self.E, self.f, left=0), 0) * q ** 2
            c = np.concatenate([[0], np.cumsum(0.5 * (p[1:] + p[:-1]))]); cdf[k] = c / c[-1]
        k = np.clip(np.searchsorted(rn, rad), 1, nrn - 1)
        w = (np.log(rad) - np.log(rn[k - 1])) / (np.log(rn[k]) - np.log(rn[k - 1]))
        k = np.where(w < 0.5, k - 1, k)
        qq = np.empty(rad.size)
        for kk in np.unique(k):
            s = k == kk; qq[s] = np.interp(u[s], cdf[kk], q)
        ps = np.interp(rad, self.r, self.Psi)
        v = qq * np.sqrt(np.maximum(2 * (ps - self.Psi2), 0))
        return v * mu, v * np.sqrt(1 - mu ** 2)

    def Mtgt(self, x):
        return np.interp(x, self.r, self.Mt, left=0.0, right=self.Mtgt_tot)

    def Mx_at(self, x):
        return np.interp(x, self.r, self.Mx, left=0.0, right=float(self.Mx[-1]))


EQ_CACHE = {}
def get_eq(foot, host, clump):
    key = (foot, host, clump)
    if key not in EQ_CACHE: EQ_CACHE[key] = Eq(foot, host, clump)
    return EQ_CACHE[key]


def m_particle(host, nscale=1.0):
    e = get_eq("canonical", host, True)
    return (e.Mtgt_tot + float(e.Mx[-1])) / (NTARGET[host] * nscale)


def initial_state(foot, host, clump, eps, nscale=1.0, special=None):
    """halo radii from rho_tgt (1 + eps xi_k), clump radii from rho_x, velocities from the total f (same uniforms in paired runs)"""
    e = get_eq(foot, host, clump); e0 = get_eq(foot, host, False)
    mp = m_particle(host, nscale)
    r = e.r
    dM = np.diff(e.Mt)
    rmid = 0.5 * (r[1:] + r[:-1]); kb = gbin(rmid)
    w = np.where(kb < NBG, 1.0 + eps * XI[np.minimum(kb, NBG - 1)], 1.0)
    cum = np.concatenate([[0.0], np.cumsum(dM * w)])
    nh = int(round(e.Mtgt_tot / mp))
    rh = np.interp(np.random.default_rng(88901).random(nh) * cum[-1], cum, r)
    ruh = np.random.default_rng(88903).random((2, nh))
    if clump:
        nc = int(round(CL[foot]["Mcl"] / mp))
        Mx = e.Mx - e.Mx[0]
        rc = np.interp(np.random.default_rng(88902).random(nc) * Mx[-1], Mx, r)
        ruc = np.random.default_rng(88904).random((2, nc))
        rad = np.concatenate([rh, rc]); uu = np.concatenate([ruh, ruc], axis=1)
        tag = np.concatenate([np.zeros(nh, np.int8), np.ones(nc, np.int8)])
    else:
        rad, uu, tag = rh, ruh, np.zeros(nh, np.int8)
    rad = np.maximum(rad, 2 * RMIN)
    vr, vt = e.velocities(rad, uu[0], 2 * uu[1] - 1)
    if special == "half":
        keep = np.arange(rad.size) % 2 == 0
        rad, vr, vt, tag = rad[keep], vr[keep], vt[keep], tag[keep]
    elif special == "comb":
        zb = zone_bins(CL[foot]["rt"]); kill = zb[::2]
        keep = ~np.isin(gbin(rad), kill)
        rad, vr, vt, tag = rad[keep], vr[keep], vt[keep], tag[keep]
    elif special == "comb2":                              # POST-HOC: mass-conserving comb (move, do not remove; v_r, v_t kept)
        zb = zone_bins(CL[foot]["rt"]); kill = zb[::2]
        mv = np.isin(gbin(rad), kill)
        rad = np.where(mv, rad * math.exp(DLGB), rad)
    return rad, vr, rad * vt, mp, tag, e


def zone_bins(rt):
    return np.where((GF[:-1] >= rt) & (GF[1:] <= 2000.0))[0]


# ------------------------------------------------------------------ dynamics
class Field:
    def __init__(self, host, mp):
        self.Mb, self.a = HOSTS[host]; self.mp = mp
        self.Mbt = self.Mb * RG ** 3 / (RG ** 2 + self.a ** 2) ** 1.5
        self.Mbf = self.Mb * GF ** 3 / (GF ** 2 + self.a ** 2) ** 1.5
        self.rhob = np.diff(self.Mbf) / GV

    def build(self, r):
        k = np.clip(((np.log(r) - LG0) / DLG).astype(np.int64), 0, NG - 1)
        c = np.bincount(k, minlength=NG).astype(float)
        self.Mt = self.Mbt + np.concatenate([[0.0], np.cumsum(c)]) * self.mp

    def phi_table(self):
        g = G * self.Mt / RG ** 2
        seg = 0.5 * (g[1:] + g[:-1]) * np.diff(RG)
        top = -G * self.Mt[-1] / RG[-1]
        self.Phi = np.concatenate([top - np.cumsum(seg[::-1])[::-1], [top]])

    def _interp(self, tab, r):
        x = (np.log(r) - LG0) / DLG
        k = np.clip(x.astype(np.int64), 0, NG - 1); w = np.clip(x - k, 0.0, 1.0)
        return tab[k] * (1 - w) + tab[k + 1] * w

    def Menc(self, r): return self._interp(self.Mt, r)
    def phi(self, r): return self._interp(self.Phi, r)


def vlasov_step(fd, r, vr, L, dt):
    fd.build(r)
    Me = fd.Menc(r)
    v = np.sqrt(vr ** 2 + (L / r) ** 2) + 1e-12
    tdyn = np.minimum(np.sqrt(r ** 3 / np.maximum(G * Me, 1e-30)), r / v)
    lev = np.clip(np.ceil(np.log2(np.maximum(dt / (ETA * tdyn), 1.0))), 0, int(math.log2(NMAX))).astype(int)
    r = r.copy(); vr = vr.copy()
    for l in np.unique(lev):
        k = np.where(lev == l)[0]; n = 2 ** l; h = dt / n
        rr, vv, LL = r[k], vr[k], L[k]
        aa = LL ** 2 / rr ** 3 - G * fd.Menc(rr) / rr ** 2
        for _ in range(n):
            vv = vv + 0.5 * h * aa
            rr = rr + h * vv
            neg = rr < RMIN
            rr = np.where(neg, 2 * RMIN - rr, rr); vv = np.where(neg, -vv, vv)
            aa = LL ** 2 / rr ** 3 - G * fd.Menc(rr) / rr ** 2
            vv = vv + 0.5 * h * aa
        r[k], vr[k] = rr, vv
    return r, vr, int(lev.max())


def gate_of(mode, d):
    if mode == "gate": return d > 0
    if mode == "inv": return d < 0
    if mode == "one":
        g = d > 0; g[:] = True; return g          # gated code path with chi forced to 1 (K1)
    if mode == "two": return np.ones(d.size, bool)
    raise ValueError(mode)


class Dyn:
    """drift + OU on the gate bins"""
    def __init__(self, fd, mtgt, alpha, mode):
        self.fd, self.mtgt, self.alpha, self.mode = fd, mtgt, alpha, mode
        self.Wd = 0.0; self.Wou = 0.0; self.nclip = 0; self.nmove = 0; self.ndmax = 0
        self.precond_ok = True; self.duty_hist = []

    def binstate(self, r):
        k = gbin(r)
        inside = k < NBG
        cnt = np.bincount(k[inside], minlength=NBG).astype(float)
        mc = cnt * self.fd.mp
        d = self.mtgt - mc
        chi = gate_of(self.mode, d)
        if self.mode in ("gate", "one", "two") and np.any((cnt > 0) & (d <= 0)): self.precond_ok = False
        rhoc = mc / GV
        tau = 1.0 / np.sqrt(4 * math.pi * G * (self.fd.rhob + rhoc))
        Mexf = np.concatenate([[0.0], np.cumsum(mc - self.mtgt)])
        return k, inside, cnt, mc, d, chi, rhoc, tau, Mexf

    def drift(self, r, dt):
        if self.alpha == 0: return r
        k, inside, cnt, mc, d, chi, rhoc, tau, Mexf = self.binstate(r)
        def vs_of(r, k, inside, chi, tau, Mexf):
            kk = np.minimum(k, NBG - 1)
            w = (r - GF[kk]) / GDR[kk]
            Mex = Mexf[kk] * (1 - w) + Mexf[kk + 1] * w
            on = inside & chi[kk]
            return np.where(on, self.alpha * tau[kk] * G * Mex / r ** 2, 0.0), kk
        vs, kk = vs_of(r, k, inside, chi, tau, Mexf)
        mv = vs != 0
        if not mv.any(): return r
        nd = int(min(16, max(1, math.ceil(float(np.max(np.abs(vs[mv]) * dt / (0.4 * GDR[kk[mv]])))))))
        self.ndmax = max(self.ndmax, nd); h = dt / nd
        for it in range(nd):
            if it > 0:
                k, inside, cnt, mc, d, chi, rhoc, tau, Mexf = self.binstate(r)
                vs, kk = vs_of(r, k, inside, chi, tau, Mexf)
            self.fd.build(r); self.fd.phi_table()
            dx = vs * h; lim = 0.5 * GDR[kk]
            over = np.abs(dx) > lim
            self.nclip += int(over.sum()); self.nmove += int((vs != 0).sum())
            dx = np.clip(dx, -lim, lim)
            rn = r + dx
            rn = np.where(rn < RMIN, 2 * RMIN - rn, rn)
            self.Wd += self.fd.mp * float(np.sum(self.fd.phi(rn) - self.fd.phi(r)))
            r = rn
        return r

    def ou(self, r, vr, vt, dt, rng):
        x1, x2, x3 = rng.standard_normal((3, r.size))      # drawn for every particle whatever the gate
        if self.alpha == 0: return vr, vt
        k, inside, cnt, mc, d, chi, rhoc, tau, Mexf = self.binstate(r)
        Mc_c = np.concatenate([[0.0], np.cumsum(mc)[:-1]]) + 0.5 * mc
        Mb_c = self.fd.Mb * GRC ** 3 / (GRC ** 2 + self.fd.a ** 2) ** 1.5
        gb = G * (Mb_c + Mc_c) / GRC ** 2
        Pf = np.concatenate([np.cumsum((rhoc * gb * GDR)[::-1])[::-1], [0.0]])
        Pc = 0.5 * (Pf[1:] + Pf[:-1])
        s2J = np.where(rhoc > 0, Pc / np.maximum(rhoc, 1e-300), 0.0)
        kk = np.minimum(k, NBG - 1)
        on = inside & chi[kk]
        a = np.exp(-self.alpha / tau[kk] * dt); b = np.sqrt(s2J[kk] * (1 - a ** 2))
        K0 = float(np.sum(vr ** 2 + vt ** 2))
        vr_n = np.where(on, a * vr + b * x1, vr)
        vt_n = np.where(on, np.hypot(a * vt + b * x2, b * x3), vt)
        self.Wou += 0.5 * self.fd.mp * (float(np.sum(vr_n ** 2 + vt_n ** 2)) - K0)
        return vr_n, vt_n


def energy(r, vr, L, mp, Mb, a):
    idx = np.argsort(r, kind="stable"); rank = np.empty(r.size); rank[idx] = np.arange(r.size)
    K = 0.5 * mp * float(np.sum(vr ** 2 + (L / r) ** 2))
    W = -G * mp * mp * float(np.sum(rank / r)) - G * mp * Mb * float(np.sum(1 / np.sqrt(r ** 2 + a ** 2)))
    Menc = Mb * r ** 3 / (r ** 2 + a ** 2) ** 1.5 + mp * rank
    vir = 2 * K / (mp * float(np.sum(G * Menc / r)))
    return K, W, vir


COARSE = np.geomspace(50.0, 3000.0, 11)


def snapshot(t, r, vr, L, mp, e, foot, dyn, E0, fesc_base=None):
    Mb, a = e.Mb, e.a
    rt = CL[foot]["rt"]
    r90 = float(np.interp(0.9 * CL[foot]["Mcl"], get_eq(foot, e.host, True).Mx, e.r))
    k = gbin(r); cnt = np.bincount(k[k < NBG], minlength=NBG).astype(float)
    mtgt = np.diff(e.Mtgt(GF))
    zb = zone_bins(rt)
    mc = cnt * mp
    Mex = lambda x: mp * float(np.sum(r < x)) - float(e.Mtgt(x))
    K, W, vir = energy(r, vr, L, mp, Mb, a)
    s = dict(t=t, Mex_rt=Mex(rt), Mex_r90=Mex(r90),
             C={str(int(x)): Mex(x) / CL[foot]["Mcl"] for x in (500.0, 1000.0, 2000.0, 3000.0)},
             He=float(np.mean(cnt[zb] == 0)), Hd=float(np.mean(mc[zb] < 0.5 * mtgt[zb])),
             zone_ratio=float(mc[zb].sum() / mtgt[zb].sum()), Mzone=float(mc[zb].sum()),
             duty=float(np.mean((mtgt[zb] - mc[zb]) > 0)),
             E=K + W, K=K, W=W, vir=vir, Wd=(dyn.Wd if dyn else 0.0), Wou=(dyn.Wou if dyn else 0.0),
             fesc=float(np.mean(r > R2)), coarse=np.histogram(r, COARSE)[0].tolist())
    s["Einj"] = s["Wd"] + s["Wou"]
    s["epsE"] = (s["E"] - E0 - s["Einj"]) / abs(E0) if E0 is not None else 0.0
    return s


def run(spec):
    """spec: name, foot, host, clump, alpha, eps, mode, vlasov, ou, drift, T, nscale, special"""
    t0 = time.time()
    foot, host = spec["foot"], spec["host"]
    r, vr, L, mp, tag, e = initial_state(foot, host, spec["clump"], spec["eps"], spec.get("nscale", 1.0), spec.get("special"))
    N0 = r.size
    fd = Field(host, mp)
    mtgt = np.diff(e.Mtgt(GF))
    dyn = Dyn(fd, mtgt, spec["alpha"], spec["mode"])
    rng = np.random.default_rng(88905)
    rt = CL[foot]["rt"]; Mtgt_rt = float(e.Mtgt(rt))
    snaps = [snapshot(0.0, r, vr, L, mp, e, foot, dyn, None)]
    E0 = snaps[0]["E"]; snaps[0]["epsE"] = 0.0
    Mex0 = snaps[0]["Mex_rt"]
    fine = [(0.0, 1.0)]
    nst = int(round(spec["T"] / DT)); every = int(round(SNAP / DT)); lmax = 0
    for it in range(1, nst + 1):
        if spec.get("vlasov", True):
            r, vr, lv = vlasov_step(fd, r, vr, L, DT); lmax = max(lmax, lv)
        vt = L / r
        if spec.get("drift", True):
            r = dyn.drift(r, DT)
        if spec.get("ou", True):
            vr, vt = dyn.ou(r, vr, vt, DT, rng)
        L = r * vt
        t = it * DT
        if t <= FINE_T + 1e-9 or it % 10 == 0:
            if spec["clump"] and abs(Mex0) > 0:
                fine.append((t, (mp * float(np.sum(r < rt)) - Mtgt_rt) / Mex0))
        if it % every == 0:
            snaps.append(snapshot(t, r, vr, L, mp, e, foot, dyn, E0))
    ok_mass = bool(r.size == N0 and np.all(np.isfinite(r)) and np.all(r > 0) and np.all(np.isfinite(vr)) and np.all(np.isfinite(L)))
    for s in snaps:
        s["R"] = s["Mex_rt"] / Mex0 if spec["clump"] else None
        s["R90"] = s["Mex_r90"] / snaps[0]["Mex_r90"] if spec["clump"] else None
    t50 = None
    if spec["clump"]:
        for (t, R) in fine:
            if R <= 0.5: t50 = t; break
    out = dict(spec={k: v for k, v in spec.items()}, N=N0, mp=mp, n_clump=int(tag.sum()), ok_mass=ok_mass, lmax=lmax,
               ndmax=dyn.ndmax, clip_frac=dyn.nclip / max(dyn.nmove, 1), precond_ok=dyn.precond_ok, t50=t50,
               fine=fine[:: max(1, len(fine) // 400)], snaps=snaps, wall_s=time.time() - t0)
    if spec.get("keep_state"): out["state"] = dict(r=r.tolist(), vr=vr.tolist())
    return out


def wavg(snaps, key, t1, t2, sub=None):
    v = [(s[key][sub] if sub else s[key]) for s in snaps if t1 - 1e-9 <= s["t"] <= t2 + 1e-9]
    v = [x for x in v if x is not None]
    return float(np.mean(v)) if v else float("nan")


def summarize_run(o):
    s = o["snaps"]; T = o["spec"]["T"]
    f = dict(R=wavg(s, "R", T - 100, T) if o["spec"]["clump"] else None,
             R90=wavg(s, "R90", T - 100, T) if o["spec"]["clump"] else None,
             He=wavg(s, "He", T - 100, T), Hd=wavg(s, "Hd", T - 100, T),
             He_mid=wavg(s, "He", T / 2 - 50, T / 2 + 50), Hd_mid=wavg(s, "Hd", T / 2 - 50, T / 2 + 50),
             Mzone_T=s[-1]["Mzone"], Mzone_0=s[0]["Mzone"], Mzone_mid=wavg(s, "Mzone", T / 2 - 50, T / 2 + 50),
             zone_ratio=s[-1]["zone_ratio"], duty=wavg(s, "duty", T - 100, T), duty0=s[0]["duty"],
             C={k: s[-1]["C"][k] for k in s[-1]["C"]}, E0=s[0]["E"], ET=s[-1]["E"], Einj=s[-1]["Einj"],
             Wd=s[-1]["Wd"], Wou=s[-1]["Wou"], epsE=max(abs(x["epsE"]) for x in s), fesc=s[-1]["fesc"],
             vir0=s[0]["vir"], virT=s[-1]["vir"])
    n = len(s); i1 = n // 3; i2 = 2 * n // 3
    r1 = (s[i1]["Einj"] - s[0]["Einj"]) / max(s[i1]["t"] - s[0]["t"], 1e-9)
    r3 = (s[-1]["Einj"] - s[i2]["Einj"]) / max(s[-1]["t"] - s[i2]["t"], 1e-9)
    f["Einj_rate_first"], f["Einj_rate_last"] = r1, r3
    f["energy_bounded"] = bool(abs(f["Einj"]) <= 0.01 * abs(f["E0"]) or abs(r3) <= 0.5 * abs(r1))
    return f


# ------------------------------------------------------------------ parts
def spec(name, foot, host="H2", clump=True, alpha=1.0, eps=0.01, mode="gate", T=T_RUN, **kw):
    d = dict(name=name, foot=foot, host=host, clump=clump, alpha=alpha, eps=eps, mode=mode, T=T)
    d.update(kw); return d


def pair(prefix, foot, alpha, eps, mode, host="H2", **kw):
    return [spec(f"{prefix}|{foot}|{host}|a{alpha}|e{eps}|clump", foot, host, True, alpha, eps, mode, **kw),
            spec(f"{prefix}|{foot}|{host}|a{alpha}|e{eps}|noclump", foot, host, False, alpha, eps, mode, **kw)]


def part_specs(p):
    if p == "K":
        return ([spec(f"KV|{f}", f, clump=True, alpha=0.0, eps=0.0, mode="two", drift=False, ou=False) for f in FOOTS]
                + [spec("K1|two", "canonical", alpha=1.0, eps=0.01, mode="two", T=100.0),
                   spec("K1|one", "canonical", alpha=1.0, eps=0.01, mode="one", T=100.0),
                   spec("K1b|two", "canonical", clump=False, alpha=1.0, eps=0.0, mode="two", T=20.0, special="half"),
                   spec("K1b|gate", "canonical", clump=False, alpha=1.0, eps=0.0, mode="gate", T=20.0, special="half"),
                   spec("KOU", "canonical", clump=False, alpha=1.0, eps=0.0, mode="two", drift=False, T=500.0),
                   spec("Dmix", "canonical", clump=False, alpha=0.0, eps=0.0, mode="two", drift=False, ou=False, special="comb")]
                + pair("Dnoorbit", "canonical", 1.0, 0.01, "gate", vlasov=False, ou=False)
                + pair("Dnoorbit", "canonical", 1.0, 0.1, "gate", vlasov=False, ou=False))
    if p in ("G1a", "G1b", "G2a", "G2b"):
        foot = "canonical" if p[1] == "1" else "alt"; al = 0.5 if p[2] == "a" else 1.0
        return pair("G", foot, al, 0.01, "gate") + pair("G", foot, al, 0.1, "gate")
    if p in ("U1", "U2"):
        foot = "canonical" if p == "U1" else "alt"
        return pair("U", foot, 0.5, 0.01, "two") + pair("U", foot, 1.0, 0.01, "two")
    if p == "N1": return [pair("N", "canonical", 1.0, 0.01, "gate", nscale=4.0)[0]]
    if p == "N2": return [pair("N", "canonical", 1.0, 0.01, "gate", nscale=4.0)[1]]
    if p in ("H1", "H3"): return pair("H", "canonical", 1.0, 0.01, "gate", host=p)
    if p == "P1":                                          # POST-HOC diagnostics (no class weight)
        return (pair("PnoOU", "canonical", 1.0, 0.01, "gate", ou=False) + pair("PnoDrift", "canonical", 1.0, 0.01, "gate", drift=False)
                + pair("Pa0.05", "canonical", 0.05, 0.01, "gate")
                + [spec("Dmix2", "canonical", clump=False, alpha=0.0, eps=0.0, mode="two", drift=False, ou=False, special="comb2")])
    if p == "P2":                                          # POST-HOC: drift + orbits without OU at N x 4
        return pair("PnoOU", "canonical", 1.0, 0.01, "gate", ou=False, nscale=4.0)
    if p == "M":
        assert MUT, "part M is the MUTATE part (CFG889_MUTATE=1)"
        return pair("M", "canonical", 1.0, 0.01, "inv") + pair("M", "alt", 1.0, 0.01, "inv")
    raise SystemExit(f"unknown part {p}")


def run_part(p):
    t0 = time.time()
    P(f"CFG889 part {p}{'  [MUTATE: inverted gate]' if MUT else ''}  (kappa = 1/2 FITTED; footings never pooled; not theory closed)")
    res = {}
    if p == "K":
        for f in FOOTS:                                   # equilibrium diagnostics (DF positivity, rho from f)
            for cl in (True, False):
                e = get_eq(f, "H2", cl)
                rr = np.array([1.0, 10.0, 50.0, 100.0, 200.0, 500.0, 1000.0, 2000.0, 3000.0, 4500.0])
                ratio = e.rho_from_f(rr) / np.interp(rr, e.r, e.rho_c)
                res[f"EQ|{f}|{'clump' if cl else 'noclump'}"] = dict(fmin_over_fmax=float(e.f.min() / e.f.max()),
                                                                    neg_frac=float(np.mean(e.f < 0)),
                                                                    rho_f_ratio={str(x): float(y) for x, y in zip(rr, ratio)})
                P(f"  EQ {f:9s} {'clump  ' if cl else 'noclump'} f_min/f_max {e.f.min() / e.f.max():+.2e}  rho(f)/rho at "
                  + " ".join(f"{x:g}:{y:.3f}" for x, y in zip(rr, ratio)))
    if p == "P1":                                          # POST-HOC K-OU diagnosis: OU target vs the particles' own dispersion
        r, vr, L, mp, tag, e = initial_state("canonical", "H2", False, 0.0)
        fd = Field("H2", mp); dy = Dyn(fd, np.diff(e.Mtgt(GF)), 1.0, "two")
        k, inside, cnt, mc, dd, chi, rhoc, tau, Mexf = dy.binstate(r)
        Mc_c = np.concatenate([[0.0], np.cumsum(mc)[:-1]]) + 0.5 * mc
        gb = G * (fd.Mb * GRC ** 3 / (GRC ** 2 + fd.a ** 2) ** 1.5 + Mc_c) / GRC ** 2
        Pf = np.concatenate([np.cumsum((rhoc * gb * GDR)[::-1])[::-1], [0.0]]); Pc = 0.5 * (Pf[1:] + Pf[:-1])
        s2J = np.where(rhoc > 0, Pc / np.maximum(rhoc, 1e-300), 0.0)
        diag = {}
        for lo, hi in ((20, 60), (60, 120), (120, 300), (300, 1000), (1000, 2000), (2000, 3000), (3000, 4000), (4000, 5000)):
            m = (r >= lo) & (r < hi)
            w = s2J[np.minimum(k[m], NBG - 1)]
            diag[f"{lo}-{hi}"] = dict(n=int(m.sum()), s2J_over_s2r=float(np.mean(w) / np.mean(vr[m] ** 2)),
                                      kurt_vr=float(np.mean(vr[m] ** 4) / np.mean(vr[m] ** 2) ** 2),
                                      median_bin_count=float(np.median(cnt[np.unique(k[m])])))
            P(f"  OU-diag r {lo:5d}-{hi:5d} pc: n {m.sum():6d}, median particles/bin {diag[f'{lo}-{hi}']['median_bin_count']:6.0f}, "
              f"<s2_J>/<v_r^2> {diag[f'{lo}-{hi}']['s2J_over_s2r']:.3f}, kurtosis(v_r) {diag[f'{lo}-{hi}']['kurt_vr']:.2f} (Gaussian 3)")
        res["OUdiag"] = diag
    for sp_ in part_specs(p):
        o = run(sp_)
        o["final"] = summarize_run(o)
        res[sp_["name"]] = o
        fz = o["final"]
        P(f"  {sp_['name']:38s} N {o['N']:6d} (clump {o['n_clump']:5d})  R {fz['R'] if fz['R'] is None else round(fz['R'], 4)}"
          f"  R90 {fz['R90'] if fz['R90'] is None else round(fz['R90'], 4)}  t50 {o['t50']}  He {fz['He']:.3f} Hd {fz['Hd']:.3f}"
          f"  zone {fz['zone_ratio']:.3f}  duty {fz['duty0']:.2f}->{fz['duty']:.2f}  C1k {fz['C']['1000']:+.3f} C2k {fz['C']['2000']:+.3f}"
          f"  Einj/|E0| {fz['Einj'] / abs(fz['E0']):+.2e}  epsE {fz['epsE']:.1e}  fesc {fz['fesc']:.4f}  clip {o['clip_frac']:.1e}"
          f"  nd {o['ndmax']}  lmax {o['lmax']}  ({o['wall_s']:.0f}s)")
    res["_wall_s"] = time.time() - t0
    json.dump(res, open(os.path.join(PARTS, f"part_{p}{SUF}.json"), "w"), default=float)
    open(os.path.join(PARTS, f"part_{p}{SUF}.out"), "w").write("\n".join(OUT) + "\n")
    P(f"  part {p} wall {time.time() - t0:.0f} s")


# ------------------------------------------------------------------ summary
def load(p, suf=""):
    fn = os.path.join(PARTS, f"part_{p}{suf}.json")
    return json.load(open(fn)) if os.path.exists(fn) else None


def cell_verdict(c, b):
    fc, fb = c["final"], b["final"]
    Mcl = CL[c["spec"]["foot"]]["Mcl"]
    dHe, dHd = fc["He"] - fb["He"], fc["Hd"] - fb["Hd"]
    dHd_mid = fc["Hd_mid"] - fb["Hd_mid"]
    dMz = ((fc["Mzone_T"] - fc["Mzone_0"]) - (fb["Mzone_T"] - fb["Mzone_0"])) / Mcl
    dMz_mid = ((fc["Mzone_mid"] - fc["Mzone_0"]) - (fb["Mzone_mid"] - fb["Mzone_0"])) / Mcl
    kept = fc["R"] >= 0.9
    healed = dHe <= 0.05 and dHd <= 0.05 and dMz >= -0.10
    growing = (dHd - dHd_mid > 0.05) or ((-dMz) - (-dMz_mid) > 0.05)
    wb = bool(c["ok_mass"] and b["ok_mass"] and fc["fesc"] <= 0.01 and fc["energy_bounded"])
    return dict(R=fc["R"], R90=fc["R90"], dHe=dHe, dHd=dHd, dHd_mid=dHd_mid, dMzone=dMz, dMzone_mid=dMz_mid, KEPT=bool(kept),
                HEALED=bool(healed), GROWING=bool(growing), WELL_BEHAVED=wb, energy_bounded=fc["energy_bounded"], fesc=fc["fesc"],
                C=fc["C"], C_base=fb["C"], duty0=fc["duty0"], duty=fc["duty"], zone_ratio=fc["zone_ratio"],
                zone_ratio_base=fb["zone_ratio"], He=fc["He"], Hd=fc["Hd"], He_base=fb["He"], Hd_base=fb["Hd"],
                Einj_over_E0=fc["Einj"] / abs(fc["E0"]), Wd_over_E0=fc["Wd"] / abs(fc["E0"]), Wou_over_E0=fc["Wou"] / abs(fc["E0"]),
                Einj_rates=(fc["Einj_rate_first"], fc["Einj_rate_last"]), epsE=max(fc["epsE"], fb["epsE"]))


def summary():
    R = {"lane": "CFG889", "criteria": "0337ade83", "mutate": MUT}
    if MUT:
        M = load("M", "_MUTATE")
        if M is None: raise SystemExit("run part M first")
        P("CFG889 MUTATE summary: inverted gate chi = 1[d < 0] (alpha = 1, eps = 0.01, H2)")
        cells = {}
        for f in FOOTS:
            c = M[f"M|{f}|H2|a1.0|e0.01|clump"]; b = M[f"M|{f}|H2|a1.0|e0.01|noclump"]
            v = cell_verdict(c, b); v["t50"] = c["t50"]; cells[f] = v
            P(f"  [{f:9s}] R(T) {v['R']:.4f}  t50 {c['t50']} Myr  dHe {v['dHe']:+.3f} dHd {v['dHd']:+.3f} dMzone {v['dMzone']:+.3f}"
              f"  C(1 kpc) {v['C']['1000']:+.3f}  Einj/|E0| {v['Einj_over_E0']:+.2e}")
        bites = all(cells[f]["R"] < 0.5 for f in FOOTS)
        R["M1"] = dict(cells=cells, bites=bool(bites))
        P(f"  M1 (inverted gate: R(T) < 0.5 on both footings) -> {'BITES' if bites else 'DOES NOT BITE'}")
        json.dump(R, open(os.path.join(HERE, "cfg889_results_MUTATE.json"), "w"), indent=1, default=float)
        open(os.path.join(HERE, "cfg889_MUTATE.out"), "w").write("\n".join(OUT) + "\n")
        P("  MUTATE: exit 1 by design when M1 bites" if bites else "  MUTATE: M1 did not bite")
        raise SystemExit(1 if bites else 0)

    parts = {p: load(p) for p in ("K", "G1a", "G1b", "G2a", "G2b", "U1", "U2", "N1", "N2", "H1", "H3")}
    missing = [p for p, v in parts.items() if v is None]
    if missing: raise SystemExit(f"missing parts: {missing}")
    A = {}
    for v in parts.values(): A.update(v)
    P("CFG889  gated kinetic stability of the deficit gate (orbits + drift + OU), H2 primary")
    P("  kappa = 1/2 FITTED; footings never pooled; cold energy is real mass; not theory closed.\n")
    K = parts["K"]
    for k in [x for x in K if x.startswith("EQ|")]:
        R.setdefault("EQ", {})[k] = K[k]
    # ---- K-tests
    kres = {}
    for f in FOOTS:
        o = A[f"KV|{f}"]; s = o["snaps"]
        c0, cT = np.array(s[0]["coarse"], float), np.array(s[-1]["coarse"], float)
        dlog = float(np.max(np.abs(np.log10(cT / c0))))
        dR = abs(s[-1]["Mex_rt"] / s[0]["Mex_rt"] - 1.0)
        dE = abs(s[-1]["E"] / s[0]["E"] - 1.0); dvir = abs(s[-1]["vir"] - s[0]["vir"])
        ok = dlog <= 0.05 and dR <= 0.05 and dE <= 0.01 and dvir <= 0.02
        kres[f"KV_{f}"] = dict(pass_=bool(ok), max_dlog=dlog, dR=dR, dE=dE, dvir=dvir,
                               noise_dlog=(0.4343 * np.sqrt(2 / c0)).tolist(), dlog_bins=np.log10(cT / c0).tolist())
        P(f"  K-V [{f:9s}] max|dlog rho| {dlog:.3f} dex (<=0.05), |dR| {dR:.3f} (<=0.05), |dE/E| {dE:.1e} (<=0.01), |dvir| {dvir:.3f}"
          f" (<=0.02) -> {'PASS' if ok else 'FAIL'}")
    # K1 bitwise: compare final snapshots exactly (energies, counts) and fine R series
    a, b = A["K1|two"], A["K1|one"]
    same = (a["snaps"] == b["snaps"]) and (a["fine"] == b["fine"])
    kres["K1"] = dict(pass_=bool(same))
    P(f"  K1 gated path with chi forced to 1 vs ungated (100 Myr, alpha 1): every snapshot and the R series identical -> {'PASS' if same else 'FAIL'}")
    a, b = A["K1b|two"], A["K1b|gate"]
    pre = bool(a["precond_ok"] and b["precond_ok"])
    sameb = (a["snaps"] == b["snaps"])
    kres["K1b"] = dict(applicable=pre, pass_=(bool(sameb) if pre else None))
    P(f"  K1b d > 0 in every occupied bin (rho_c ~ rho_tgt/2): precondition {'MET' if pre else 'NOT MET'}; gated = ungated "
      f"{'identical' if sameb else 'DIFFER'} -> {('PASS' if sameb else 'FAIL') if pre else 'NOT APPLICABLE'}")
    o = A["KOU"]; s = o["snaps"]
    c0, cT = np.array(s[0]["coarse"], float), np.array(s[-1]["coarse"], float)
    dlog = float(np.max(np.abs(np.log10(cT / c0)))); dE = abs(s[-1]["E"] / s[0]["E"] - 1.0)
    okou = dlog <= 0.05 and dE <= 0.01
    kres["KOU"] = dict(pass_=bool(okou), max_dlog=dlog, dE=dE, Wou_over_E0=s[-1]["Wou"] / abs(s[0]["E"]))
    P(f"  K-OU OU alone on the no-clump equilibrium (500 Myr): max|dlog rho| {dlog:.3f}, |dE/E| {dE:.1e}, W_OU/|E0| "
      f"{s[-1]['Wou'] / abs(s[0]['E']):+.1e} -> {'PASS' if okou else 'FAIL'}")
    runs = {k: v for k, v in A.items() if isinstance(v, dict) and "snaps" in v}
    km = all(v["ok_mass"] for v in runs.values())
    kres["KM"] = dict(pass_=bool(km), n_runs=len(runs))
    P(f"  K-M particle number conserved, positions finite and > 0 in all {len(runs)} runs -> {'PASS' if km else 'FAIL'}")
    verdict_runs = [k for k in runs if k.split("|")[0] in ("G", "U", "N")]
    worstE = max(runs[k]["final"]["epsE"] for k in verdict_runs)
    ke = worstE <= 0.01
    kres["KE"] = dict(pass_=bool(ke), worst=worstE, worst_run=max(verdict_runs, key=lambda k: runs[k]["final"]["epsE"]))
    P(f"  K-E |eps_E| <= 0.01 in every verdict run: worst {worstE:.2e} ({kres['KE']['worst_run']}) -> {'PASS' if ke else 'FAIL'}")
    kall = all(v["pass_"] for k, v in kres.items() if k != "K1b") and (kres["K1b"]["pass_"] is not False)
    R["K"] = kres; R["K_all_pass"] = bool(kall)
    # ---- tooth T-H (orbits off)
    P("\n  D-noorbit (drift only, gated, no Vlasov/OU; CFG882-like): tooth T-H")
    th = {}
    for eps in (0.01, 0.1):
        c, b = A[f"Dnoorbit|canonical|H2|a1.0|e{eps}|clump"], A[f"Dnoorbit|canonical|H2|a1.0|e{eps}|noclump"]
        v = cell_verdict(c, b); th[str(eps)] = v
        P(f"    eps {eps:4.2f}: He clump {v['He']:.3f} vs no clump {v['He_base']:.3f} (dHe {v['dHe']:+.3f}); Hd {v['Hd']:.3f} vs "
          f"{v['Hd_base']:.3f}; R {v['R']:.4f}; C(1 kpc) {v['C']['1000']:+.3f} (no clump {v['C_base']['1000']:+.3f}); dMzone {v['dMzone']:+.3f}")
    thb = all(th[e]["dHe"] >= 0.10 for e in th)
    R["T_H"] = dict(cells=th, bites=bool(thb))
    P(f"    T-H (dHe >= 0.10 at both eps) -> {'BITES' if thb else 'DOES NOT BITE (hole metric NOT DIAGNOSTIC)'}"
      f"   [CFG882 D1, 12 Gyr density flow: 39-45% emptied vs 0-5%; M_ex(<1 kpc)/M_cl 0.91-0.94]")
    # ---- D-mix
    o = A["Dmix"]; s = o["snaps"]
    ser = [(x["t"], x["He"], x["Hd"]) for x in s]
    heal_t = next((t for t, he, hd in ser if he == 0 and hd <= 0.05), None)
    R["Dmix"] = dict(series=ser[:31], He0=s[0]["He"], Hd0=s[0]["Hd"], He_T=s[-1]["He"], Hd_T=s[-1]["Hd"], heal_time=heal_t,
                     zone_ratio_0=s[0]["zone_ratio"], zone_ratio_T=s[-1]["zone_ratio"])
    P(f"\n  D-mix (comb of emptied zone bins, pure Vlasov): He {s[0]['He']:.3f} -> {s[-1]['He']:.3f}, Hd {s[0]['Hd']:.3f} -> "
      f"{s[-1]['Hd']:.3f}; first time He = 0 and Hd <= 0.05: {heal_t} Myr; zone ratio {s[0]['zone_ratio']:.3f} -> {s[-1]['zone_ratio']:.3f}")
    # ---- primary gated cells
    P("\n  PRIMARY gated cells (H2; clump minus paired no-clump)")
    cells = {}
    for f in FOOTS:
        for al in (0.5, 1.0):
            for eps in (0.01, 0.1):
                c, b = A[f"G|{f}|H2|a{al}|e{eps}|clump"], A[f"G|{f}|H2|a{al}|e{eps}|noclump"]
                v = cell_verdict(c, b); key = f"{f}|a{al}|e{eps}"; cells[key] = v
                P(f"    [{key:20s}] R {v['R']:.4f} R90 {v['R90']:.4f} | dHe {v['dHe']:+.3f} dHd {v['dHd']:+.3f} (mid {v['dHd_mid']:+.3f})"
                  f" dMzone {v['dMzone']:+.3f} (mid {v['dMzone_mid']:+.3f}) | C 0.5/1/2/3 kpc " + "/".join(f"{v['C'][k]:+.2f}" for k in ("500", "1000", "2000", "3000"))
                  + f" | duty {v['duty0']:.2f}->{v['duty']:.2f} | Einj/|E0| {v['Einj_over_E0']:+.2e} (drift {v['Wd_over_E0']:+.2e}, OU {v['Wou_over_E0']:+.2e})"
                  f" fesc {v['fesc']:.4f} -> KEPT {v['KEPT']} HEALED {v['HEALED']} GROWING {v['GROWING']} WB {v['WELL_BEHAVED']}")
    R["cells"] = cells
    # ---- resolution
    c, b = A["N|canonical|H2|a1.0|e0.01|clump"], A["N|canonical|H2|a1.0|e0.01|noclump"]
    vN = cell_verdict(c, b); v1 = cells["canonical|a1.0|e0.01"]
    res_agree = (vN["KEPT"] == v1["KEPT"]) and (vN["HEALED"] == v1["HEALED"])
    R["resolution"] = dict(N4=vN, N1=v1, agree=bool(res_agree), N=c["N"])
    P(f"\n  RESOLUTION N = {c['N']} (x4): R {vN['R']:.4f}, dHe {vN['dHe']:+.3f}, dHd {vN['dHd']:+.3f}, dMzone {vN['dMzone']:+.3f}, "
      f"C(1 kpc) {vN['C']['1000']:+.3f}; KEPT {vN['KEPT']} HEALED {vN['HEALED']} (N1e5: KEPT {v1['KEPT']} HEALED {v1['HEALED']}) "
      f"-> {'AGREES' if res_agree else 'CHANGES STATUS'}; dMzone ratio N4/N1 = {vN['dMzone'] / v1['dMzone'] if v1['dMzone'] != 0 else float('nan'):.2f}")
    # ---- hosts (report-only)
    P("\n  HOSTS (report-only; canonical, gated, alpha 1, eps 0.01)")
    hv = {}
    for h in ("H1", "H3"):
        c, b = A[f"H|canonical|{h}|a1.0|e0.01|clump"], A[f"H|canonical|{h}|a1.0|e0.01|noclump"]
        v = cell_verdict(c, b); hv[h] = v
        P(f"    [{h}] N {c['N']} (clump {c['n_clump']}): R {v['R']:.4f} R90 {v['R90']:.4f} dHe {v['dHe']:+.3f} dHd {v['dHd']:+.3f} "
          f"dMzone {v['dMzone']:+.3f} C(1 kpc) {v['C']['1000']:+.3f} C(2 kpc) {v['C']['2000']:+.3f} -> KEPT {v['KEPT']} HEALED {v['HEALED']} "
          f"GROWING {v['GROWING']} WB {v['WELL_BEHAVED']}")
    R["hosts"] = hv
    # ---- ungated comparison
    P("\n  V-U ungated two-sided drift + OU (eps 0.01)")
    vu = {}
    for f in FOOTS:
        for al in (0.5, 1.0):
            c, b = A[f"U|{f}|H2|a{al}|e0.01|clump"], A[f"U|{f}|H2|a{al}|e0.01|noclump"]
            v = cell_verdict(c, b); t882 = S50_882[f] / al
            v["t50"] = c["t50"]; v["t50_882"] = t882; v["ratio"] = (c["t50"] / t882) if c["t50"] else None
            vu[f"{f}|a{al}"] = v
            P(f"    [{f:9s} a {al}] R(T) {v['R']:.4f}  t50 {c['t50']} Myr vs CFG882 {t882:.2f} Myr (ratio {v['ratio'] if v['ratio'] is None else round(v['ratio'], 2)})"
              f"  dHe {v['dHe']:+.3f} dHd {v['dHd']:+.3f} dMzone {v['dMzone']:+.3f} C(1/2/3 kpc) {v['C']['1000']:+.2f}/{v['C']['2000']:+.2f}/{v['C']['3000']:+.2f}"
              f"  Einj/|E0| {v['Einj_over_E0']:+.2e} fesc {v['fesc']:.4f}")
    drains = all(v["R"] < 0.5 for v in vu.values())
    o1 = all(v["ratio"] is not None and 1 / 3 <= v["ratio"] <= 3 for v in vu.values())
    R["VU"] = dict(cells=vu, drains=bool(drains), cfg882_O1=("CONFIRMED" if o1 else "NOT CONFIRMED"))
    P(f"    V-U: {'DRAINS' if drains else 'DOES NOT DRAIN in every cell'}; CFG882 O(1) drain rate {R['VU']['cfg882_O1']}")
    # ---- MUTATE tooth
    Mres = None
    fn = os.path.join(HERE, "cfg889_results_MUTATE.json")
    if os.path.exists(fn): Mres = json.load(open(fn))
    m1 = bool(Mres and Mres["M1"]["bites"])
    R["M1_bites"] = m1
    P(f"\n  M1 (from the MUTATE run): {'BITES' if m1 else ('DOES NOT BITE' if Mres else 'MISSING')}")
    # ---- class
    allkept = all(v["KEPT"] for v in cells.values()); allheal = all(v["HEALED"] for v in cells.values())
    allwb = all(v["WELL_BEHAVED"] for v in cells.values()); anygrow = any(v["GROWING"] for v in cells.values())
    allbound = all(v["energy_bounded"] for v in cells.values())
    eroded = [k for k, v in cells.items() if not v["KEPT"]]
    if not (kall and thb and m1 and res_agree):
        why = [w for w, ok in (("K-test", kall), ("T-H", thb), ("M1", m1), ("resolution", res_agree)) if not ok]
        cls = "INCONCLUSIVE (" + ", ".join(why) + ")"
    elif allkept and allheal and allwb:
        cls = "GATE SOUND"
    else:
        sub = []
        if not allheal: sub.append("holes " + ("GROW" if anygrow else "PERSIST"))
        sub.append("energy " + ("BOUNDED" if allbound else "RUNAWAY"))
        if not allwb and allbound: sub.append("not well behaved (escape)")
        sub.append("clump KEPT" if allkept else "clump ERODED")
        cls = "GATE UNSTABLE (" + "; ".join(sub) + ")"
    if eroded: cls += " + CLUMP ERODED (" + ", ".join(eroded) + ")"
    R["class"] = cls
    P(f"\n  K all: {'PASS' if kall else 'FAIL'}; T-H {'bites' if thb else 'no'}; M1 {'bites' if m1 else 'no'}; resolution {'agrees' if res_agree else 'CHANGES'}")
    P(f"  CLASS: {cls}")
    post = {}
    P1, P2 = load("P1"), load("P2")
    if P1 or P2:
        P("\n  ---- POST-HOC diagnostics (added after the frozen runs; NO class weight) ----")
    if P1:
        for lab in ("PnoOU", "PnoDrift", "Pa0.05"):
            al = 0.05 if lab == "Pa0.05" else 1.0
            c, b = P1[f"{lab}|canonical|H2|a{al}|e0.01|clump"], P1[f"{lab}|canonical|H2|a{al}|e0.01|noclump"]
            v = cell_verdict(c, b); v["t50"] = c["t50"]; post[lab] = v
            P(f"    {lab:8s} (canonical, alpha {al}): R(T) {v['R']:.4f}  t50 {c['t50']} Myr  dHe {v['dHe']:+.3f} dHd {v['dHd']:+.3f} dMzone {v['dMzone']:+.3f}"
              f"  C(1 kpc) {v['C']['1000']:+.3f} (base {v['C_base']['1000']:+.3f})  Einj/|E0| {v['Einj_over_E0']:+.2e}  fesc {v['fesc']:.4f} (base {P1[f'{lab}|canonical|H2|a{al}|e0.01|noclump']['final']['fesc']:.4f})")
        o = P1["Dmix2"]; s = o["snaps"]
        ser = [(x["t"], x["He"], x["Hd"], x["zone_ratio"]) for x in s]
        post["Dmix2"] = dict(series=ser[:31], He_T=s[-1]["He"], Hd_T=s[-1]["Hd"], zone_ratio_T=s[-1]["zone_ratio"])
        P("    Dmix2 (mass-conserving comb, pure Vlasov): (t, He, Hd, zone ratio) " + " ".join(f"({t:.0f},{he:.2f},{hd:.2f},{zr:.3f})" for t, he, hd, zr in ser[:6]) + f" ... T: He {s[-1]['He']:.2f} Hd {s[-1]['Hd']:.2f}")
        post["OUdiag"] = P1.get("OUdiag")
    if P2:
        c, b = P2["PnoOU|canonical|H2|a1.0|e0.01|clump"], P2["PnoOU|canonical|H2|a1.0|e0.01|noclump"]
        v = cell_verdict(c, b); v["t50"] = c["t50"]; post["PnoOU_N4"] = v
        P(f"    PnoOU N x 4 (N {c['N']}): R(T) {v['R']:.4f}  t50 {c['t50']} Myr  dHe {v['dHe']:+.3f} dHd {v['dHd']:+.3f} dMzone {v['dMzone']:+.3f}  C(1 kpc) {v['C']['1000']:+.3f}")
    if post: R["post_hoc"] = post
    json.dump(R, open(os.path.join(HERE, "cfg889_results.json"), "w"), indent=1, default=float)
    open(os.path.join(HERE, "cfg889.out"), "w").write("\n".join(OUT) + "\n")


if __name__ == "__main__":
    p = sys.argv[1] if len(sys.argv) > 1 else "S"
    if p == "S": summary()
    else: run_part(p)
