#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CFG159_sp_riccati -- independent referee re-derivation of the CFG119 (door 7) G1 headline: the Schroedinger-Poisson ground state of an
ultralight boson with baryons in its potential against the CFG44 target C(r) = (a0/4pi) M_b(<r).  Criteria: CFG159_FROZEN_CRITERIA.md.

Usage:  python3 CFG159_sp_riccati.py                 main run  (exit 0 iff every solver control and every frozen line P1-P7 passes)
        MUTATE=A|B|C|D|E python3 CFG159_sp_riccati.py   control (exit 1 when it bites: the headline / a solver control fails)
Solver: CFG159_core.py (log-derivative propagation in C, own).  Outputs are keyed by mode:  CFG159_sp_riccati[_MUTATE_x].out / _results.json
"""
import os, sys, math, json, time, hashlib
import numpy as np
from multiprocessing import Pool
from scipy.special import gammainc
from scipy.integrate import solve_ivp

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import CFG159_core as core

MODE = os.environ.get("MUTATE", "").strip().upper()
assert MODE in ("", "A", "B", "C", "D", "E"), MODE
BASE = "CFG159_sp_riccati" + (("_MUTATE_" + MODE) if MODE else "")
NPROC = int(os.environ.get("CFG159_NPROC", "12"))

# ---------------------------------------------------------------- shared constants (CFG44 docstring)
G = 4.30091727e-6                       # kpc (km/s)^2 / Msun
KPC_M = 3.0856775814913673e19
C_KMS = 299792.458
HBARC_EVM = 1.973269804e-7              # eV m
FOOT = {"canonical": 9.3603e-11, "alt": 1.1312e-10}
A0K = {k: v*KPC_M/1e6 for k, v in FOOT.items()}     # (km/s)^2/kpc
MASSES = [1e9, 1e10, 1e11, 1e12]
HKPC = {1e9: 2.0, 1e10: 3.0, 1e11: 4.0, 1e12: 5.0}   # h pairing (read from the CFG119 README)
MBOS = [1e-23, 1e-22, 1e-21, 1e-20]
PASS_BAND = 0.04                        # dex, frozen H1 line (CFG119); the asymmetric band's larger half-width is 0.0458
XG = np.logspace(-1.0, math.log10(30.0), 3001)
LOGS_SCAN = np.arange(-16.0, 4.0 + 1e-9, 0.5)
DT_PROD = 1e-3

# README (CFG119) canonical rule-(ii) J table, READ as a target (rounded as printed there): rows = (geom, M), columns = m
README_J = {("point", 1e9): [4.89, 370, 3.7e4, 3.7e6], ("point", 1e10): [116, 1.2e4, 1.2e6, 1.2e8],
            ("point", 1e11): [3.7e3, 3.7e5, 3.7e7, 3.7e9], ("point", 1e12): [1.18e5, 1.2e7, 1.2e9, 1.2e11],
            ("exp", 1e9): [4.26, 56.1, 605, 6.1e3], ("exp", 1e10): [43.8, 539, 5.5e3, 5.5e4],
            ("exp", 1e11): [474, 5.1e3, 5.1e4, 5.1e5], ("exp", 1e12): [4.6e3, 4.7e4, 4.7e5, 4.7e6]}

class Rep:
    def __init__(self): self.lines = []; self.checks = []; self.num = {}
    def P(self, s=""):
        print(s, flush=True); self.lines.append(s)
    def check(self, name, detail, ok, load=True):
        self.checks.append((name, bool(ok), bool(load)))
        self.P(f"  [{'PASS' if ok else 'FAIL'}] {name}: {detail}")
R = Rep()

# ---------------------------------------------------------------- cell set-up
def cell_geometry(geom, M, m):
    Lg = G*M/C_KMS**2                                   # G M / c^2  [kpc]
    lam = HBARC_EVM/m/KPC_M                             # hbar/(m c) [kpc]
    aB = lam**2/Lg                                      # hbar^2/(G M m^2) [kpc]
    b = {k: math.sqrt(G*M/a0)/aB for k, a0 in A0K.items()}      # r_M / a_B
    hh = (HKPC[M]/aB) if geom == "exp" else None
    rM_kpc = {k: math.sqrt(G*M/a0) for k, a0 in A0K.items()}
    return dict(aB_kpc=aB, b=b, hh=hh, rM_kpc=rM_kpc, rs_over_aB=(2*Lg)/aB)

def build_grid(cg, dt=DT_PROD):
    hh = cg["hh"]
    rfar = max(31.0*max(cg["b"].values()), 60.0*max(1.0, hh if hh else 1.0))
    r0 = 1e-9*min(1e-4, hh if hh else 1.0)
    return core.Grid(r0, rfar, dt)

def hermite_L(grid, st, r):
    t = np.log(r); dt = grid.dt
    i = np.clip(((t - grid.t[0])/dt).astype(int), 0, grid.N - 1)
    tau = (t - grid.t[i])/dt
    L = st["L"]; y = st["W"]*grid.r
    h00 = 2*tau**3 - 3*tau**2 + 1; h10 = tau**3 - 2*tau**2 + tau; h01 = -2*tau**3 + 3*tau**2; h11 = tau**3 - tau**2
    Lr = h00*L[i] + h10*dt*y[i] + h01*L[i+1] + h11*dt*y[i+1]
    yr = (1 - tau)*y[i] + tau*y[i+1]
    Mh = (1 - tau)*st["mom"]["Mnode"][i] + tau*st["mom"]["Mnode"][i+1]
    return Lr, yr, Mh

def evaluate(cell, st, s, footing, srcfac=1.0):
    """log10 of C_SP/C_target over XG for this footing (frozen definition 4/5), plus slopes and core diagnostics."""
    grid = cell["grid"]; b = cell["cg"]["b"][footing]; hh = cell["cg"]["hh"]
    r = XG*b
    Lr, yr, Mh = hermite_L(grid, st, r)
    Lmax = st["mom"]["Lmax"]; lnN = st["mom"]["lnNhat"]
    Mb = np.ones_like(r) if hh is None else gammainc(3.0, r/hh)
    lnratio = (math.log(s) + 2*(Lr - Lmax) - lnN - np.log(r) + 2*math.log(b) + np.log((Mb + s*srcfac*Mh)/Mb))
    lr10 = lnratio/math.log(10.0)
    if MODE == "B":
        lr10 = np.zeros_like(lr10)              # C_target := C_SP  (evaluator bookkeeping control)
    ia = int(np.argmax(np.abs(lr10)))
    def at(x): return float(np.interp(math.log(x), np.log(XG), lr10))
    # core diagnostic: rho(0.1 r_M)/rho(0),  rho ~ u^2/r^2, u(r0)=exp(0)
    Lr01, _, _ = hermite_L(grid, st, np.array([0.1*b]))
    core_ratio = math.exp(2*Lr01[0] - 2*math.log(0.1*b/grid.r[0]))
    slope01 = 2*(float(np.interp(math.log(0.1), np.log(XG), yr)) - 1)
    slope30 = 2*(float(yr[-1]) - 1)
    return dict(J=float(np.max(np.abs(lr10))), xargmax=float(XG[ia]), lr01=at(0.1), lr1=at(1.0), lr30=at(30.0),
                core_ratio=core_ratio, slope01=slope01, slope30=slope30)

# ---------------------------------------------------------------- one cell: rule-(ii) scan + golden section, both footings
def run_cell(args):
    geom, M, m = args
    t0 = time.time()
    cg = cell_geometry(geom, M, m)
    grid = build_grid(cg)
    cell = dict(cg=cg, grid=grid)
    vb, z0, zlo = core.make_vb(grid, cg["hh"], MODE if MODE in ("C", "D") else "")
    srcfac = 1.05 if MODE == "E" else 1.0
    out = dict(geom=geom, M=M, m=m, cg=dict(aB_kpc=cg["aB_kpc"], b=cg["b"], hh=cg["hh"], rs_over_aB=cg["rs_over_aB"], rM_kpc=cg["rM_kpc"]), N=grid.N)
    cache = {}                       # index -> (phi, E)
    scan = {f: [] for f in FOOT}
    state0 = None
    phi = np.zeros(grid.rm.shape[0]); Eg = None
    nosolve = []
    def solve_at(s, phi_g, E_g):
        if MODE in ("C", "D") and not np.any(phi_g):     # no baryon well to seed from: start from a Plummer-like soliton of size ~ 2.68/s
            phi_g = -1.0/np.sqrt(grid.rm**2 + (2.68/s)**2)
        return core.solve_state(grid, vb, z0, zlo, s, phi_g, E_g, srcfac=srcfac)
    for j, ls in enumerate(LOGS_SCAN):
        s = 10.0**ls
        if s < 1e-13 and state0 is not None and MODE not in ("C", "D"):
            st = state0
        else:
            st = solve_at(s, phi, Eg)
            if st is not None and MODE in ("C", "D") and st["E"] > -1e-25: st = None    # unphysical (unbound) numerical artefact
            if st is None:
                if MODE in ("C", "D"): phi = np.zeros(grid.rm.shape[0]); Eg = None
                for f in FOOT: scan[f].append(None)
                nosolve.append(float(ls)); continue
            phi = st["phi"]; Eg = st["E"]
            if state0 is None: state0 = st
            cache[j] = (phi.copy(), Eg)
        for f in FOOT:
            ev = evaluate(cell, st, s, f, srcfac)
            scan[f].append(ev["J"])
    out["scan"] = {f: scan[f] for f in FOOT}; out["nosolve_logs"] = nosolve
    out["opt"] = {}
    for f in FOOT:
        Js = np.array([np.inf if v is None else v for v in scan[f]])
        i0 = int(np.argmin(Js))
        if not np.isfinite(Js[i0]):
            out["opt"][f] = None; continue
        lo = LOGS_SCAN[max(i0 - 1, 0)]; hi = LOGS_SCAN[min(i0 + 1, len(LOGS_SCAN) - 1)]
        cur = {"phi": cache.get(i0, (phi, Eg))[0], "E": cache.get(i0, (phi, Eg))[1]}
        def Jof(ls):
            s = 10.0**ls
            if s < 1e-13 and MODE not in ("C", "D") and state0 is not None:
                return evaluate(cell, state0, s, f, srcfac)["J"], state0
            st = solve_at(s, cur["phi"], cur["E"])
            if st is None: return np.inf, None
            cur["phi"] = st["phi"]; cur["E"] = st["E"]
            return evaluate(cell, st, s, f, srcfac)["J"], st
        gr = (math.sqrt(5) - 1)/2
        a, bb = lo, hi
        c = bb - gr*(bb - a); d = a + gr*(bb - a)
        fc, _ = Jof(c); fd, _ = Jof(d)
        while (bb - a) > 1e-3:
            if fc < fd:
                bb, d, fd = d, c, fc; c = bb - gr*(bb - a); fc, _ = Jof(c)
            else:
                a, c, fc = c, d, fd; d = a + gr*(bb - a); fd, _ = Jof(d)
        lsb = 0.5*(a + bb)
        # compare with the scan minimum; keep the better
        Jb, stb = Jof(lsb)
        if Jb > Js[i0] or stb is None:
            lsb = LOGS_SCAN[i0]; Jb, stb = Jof(lsb)
        ev = evaluate(cell, stb, 10.0**lsb, f, srcfac)
        ev.update(log10s=float(lsb), s=10.0**lsb, E=float(stb["E"]), kappa=math.sqrt(-2*stb["E"]), iters=int(stb["it"]), conv=bool(stb["ok"]))
        out["opt"][f] = ev
    out["seconds"] = time.time() - t0
    return out

# ---------------------------------------------------------------- CFG44 target re-derived (MUTATE A; target slopes)
def target_mc(eta):
    """M_c(x) for the exponential sphere (x = r/r_M, eta = h/r_M), units G = a0 = M_b = 1:  M_c' (M_b + M_c) = M_b x."""
    Mb = lambda x: gammainc(3.0, x/eta)
    K = 1.0/(6*eta**3)
    x0 = 1e-7; y0 = math.sqrt(2*K/5)*x0**2.5
    f = lambda x, y: [Mb(x)*x/(Mb(x) + y[0])]
    sol = solve_ivp(f, [x0, 40.0], [y0], method="DOP853", rtol=1e-13, atol=1e-40, dense_output=True)
    return sol, Mb

def target_J_and_slope(geom, M, footing):
    """J of C_target evaluated on the target's OWN rho_c (MUTATE A); slope of rho_c at x = 0.1."""
    if geom == "point":
        Mc = lambda x: math.sqrt(1 + x*x) - 1.0
        Mb = lambda x: 1.0
        dMc = lambda x: x/math.sqrt(1 + x*x)
    else:
        rM = math.sqrt(G*M/A0K[footing]); eta = HKPC[M]/rM
        sol, Mbf = target_mc(eta)
        Mc = lambda x: float(sol.sol(x)[0]); Mb = lambda x: float(Mbf(x))
        dMc = lambda x: (float(sol.sol(x*(1 + 1e-5))[0]) - float(sol.sol(x*(1 - 1e-5))[0]))/(2e-5*x)
    worst = 0.0
    for x in XG[::10]:
        rho = dMc(x)/(4*math.pi*x*x); g = (Mb(x) + Mc(x))/(x*x)
        C = rho*x**3*g; Ct = Mb(x)/(4*math.pi)
        worst = max(worst, abs(math.log10(C/Ct)))
    lr = lambda x: math.log(dMc(x)/(x*x))
    e = 1e-4
    slope = (lr(0.1*(1 + e)) - lr(0.1*(1 - e)))/(math.log(1 + e) - math.log(1 - e))
    return worst, slope

# ---------------------------------------------------------------- solver controls
def virial_ratio(cell, st, s):
    """point-mass virial residual |2T + <Vb> + <Vpsi>/2| / T for the SP state (psi normalised to 1)."""
    grid = cell["grid"]; mom = st["mom"]; l = mom["l"]; r = grid.r; dt = grid.dt
    Pn = np.exp(2*l)/math.exp(mom["lnNhat"])                 # P(r) per unit r (normalised)
    y = st["W"]*r
    w = st["W"]
    with np.errstate(over="ignore", invalid="ignore"):
        Tt = 0.5*Pn*w*w*r
        Tt = np.where(np.isfinite(Tt), Tt, 0.0)
    trap = lambda a: float(np.sum(0.5*(a[1:] + a[:-1]))*dt)
    T = trap(Tt)
    vbn = -1.0/r
    phin = -(mom["Mnode"]/r + mom["Tnode"])
    Vb = trap(Pn*r*vbn); Vp = trap(Pn*r*s*phin)
    Etot = T + Vb + Vp
    return abs(2*T + Vb + 0.5*Vp)/T, abs(Etot - st["E"])/abs(st["E"])

def solver_controls():
    R.P("SOLVER CONTROLS S1-S5 (dt = 2.5e-4 unless stated)")
    dt = 2.5e-4
    # S1 hydrogen
    g = core.Grid(1e-9, 60.0, dt); vb, z0, zlo = core.make_vb(g, None, "")
    E = core.find_E(g, vb, z0, 1.0)
    fl, f, m = core.shoot(g, vb, E, z0)
    L = g.Lbuf.copy(); r = g.r; lp = L - np.log(r)
    sel = (r > 0.01) & (r < 40)
    ex = -(r[sel] - r[0])
    err = np.abs((lp[sel] - lp[0]) - ex)/np.maximum(1.0, np.abs(ex))
    R.num["S1_E"] = E; R.num["S1_lnpsi_err"] = float(err.max())
    R.check("S1 hydrogen (self-gravity off, point mass)", f"E = {E:.9f} (exact -0.5, rel err {abs(E+0.5)/0.5:.2e}); max rel. err of ln psi over 0.01<r<40 a_B: {err.max():.2e}",
            abs(E + 0.5)/0.5 < 1e-8 and err.max() < 1e-6)
    # S2 pure soliton, s = 1, no baryons; srcfac from the mode (E: 1.05)
    g2 = core.Grid(1e-8, 60.0, dt); vb2, z02, zlo2 = core.make_vb(g2, None, "C")
    srcfac = 1.05 if MODE == "E" else 1.0
    st = core.solve_state(g2, vb2, z02, zlo2, 1.0, -1.0/np.sqrt(g2.rm**2 + 1.0), None, srcfac=srcfac)
    r2 = g2.r; rho = np.exp(2*(st["L"] - np.log(r2))); rho /= rho[0]
    rc = float(np.interp(0.5, rho[::-1], r2[::-1]))
    Es = st["E"]
    R.num["S2_E"] = Es; R.num["S2_rc"] = rc
    R.check("S2 pure soliton, no baryons", f"E = {Es:.8f} (target -0.16277, rel diff {abs(Es+0.16277)/0.16277:.1e}); r_c = {rc:.6f} a_B(M_sol) (target 2.6794, rel diff {abs(rc/2.6794-1):.1e}); iterations {st['it']}",
            abs(Es + 0.16277)/0.16277 < 1e-5 and abs(rc/2.6794 - 1) < 1e-4)
    return st, g2

def control_S3S4(cells_done):
    dt = 2.5e-4
    # S3 virial on five point-mass SP states (M = 1e9, m = 1e-23, s in a spread)
    cg = cell_geometry("point", 1e9, 1e-23)
    g = core.Grid(1e-9*1e-4, max(31*max(cg["b"].values()), 60.0), dt)
    vb, z0, zlo = core.make_vb(g, None, "")
    cell = dict(cg=cg, grid=g)
    res = []
    phi = np.zeros(g.rm.shape[0]); Eg = None
    for s in [1e-2, 1e-1, 1.0, 10.0, 100.0]:
        st = core.solve_state(g, vb, z0, zlo, s, phi if Eg is None else phi, Eg)
        phi = st["phi"]; Eg = st["E"]
        vr, er = virial_ratio(cell, st, s); res.append((s, vr, er))
    R.num["S3"] = res
    R.check("S3 virial theorem 2T + <Vb> + <Vpsi>/2 = 0 (five point-mass SP states)", "; ".join(f"s={s:g}: {vr:.1e} (E vs T+V: {er:.1e})" for s, vr, er in res), max(v for _, v, _ in res) < 1e-6)

def control_S4(cells_out):
    """halving the step on five cells at their rule-(ii) optimum s (canonical): E and J change by < 1e-6 relative."""
    picks = [("exp", 1e9, 1e-23), ("point", 1e12, 1e-23), ("point", 1e9, 1e-22), ("exp", 1e10, 1e-22), ("exp", 1e12, 1e-20)]
    rows = []
    for geom, M, m in picks:
        oo = [c for c in cells_out if (c["geom"], c["M"], c["m"]) == (geom, M, m)]
        if not oo: continue
        o = oo[0]
        opt = o["opt"]["canonical"]
        if opt is None: continue
        s = opt["s"]
        cg = cell_geometry(geom, M, m)
        vals = []
        for dt in (DT_PROD, DT_PROD/2):
            grid = build_grid(cg, dt); cell = dict(cg=cg, grid=grid)
            vb, z0, zlo = core.make_vb(grid, cg["hh"], MODE if MODE in ("C", "D") else "")
            # cold start then relax: walk s up from 1e-13 to the target for a robust start
            phi = np.zeros(grid.rm.shape[0]); Eg = None; st = None
            for ls in list(np.arange(-13.0, math.log10(s), 1.0)) + [math.log10(s)]:
                st = core.solve_state(grid, vb, z0, zlo, 10.0**ls, phi, Eg, srcfac=1.05 if MODE == "E" else 1.0)
                phi = st["phi"]; Eg = st["E"]
            ev = evaluate(cell, st, s, "canonical", 1.05 if MODE == "E" else 1.0)
            vals.append((st["E"], ev["J"]))
        dE = abs(vals[0][0] - vals[1][0])/abs(vals[1][0]); dJ = abs(vals[0][1] - vals[1][1])/abs(vals[1][1])
        rows.append((geom, M, m, dE, dJ))
    R.num["S4"] = rows
    R.check("S4 halving the step (dt 1e-3 -> 5e-4) at the rule-(ii) optimum", "; ".join(f"{g} {M:.0e} m={m:.0e}: dE/E {a:.1e}, dJ/J {c:.1e}" for g, M, m, a, c in rows),
            all(a < 1e-6 and c < 1e-6 for _, _, _, a, c in rows), True)

# ---------------------------------------------------------------- main
def main():
    t00 = time.time()
    core.lib()                                  # compile once before forking
    R.P(f"CFG159 independent re-derivation of CFG119's G1 headline   mode = {MODE or 'main'}")
    R.P("criteria: CFG159_FROZEN_CRITERIA.md;  README numbers are READ targets, not blind predictions;  a0 canonical 9.3603e-11, alt 1.1312e-10")
    R.P("kappa = 1/2 is FITTED; nothing here says the data favour the framework or that the theory is closed.")
    R.P()
    st_ctrl, g2 = solver_controls()
    if MODE == "E":
        R.P("MUTATE E: Poisson source x 1.05 in the solver controls and in the reference cells")
    # ---- cell set
    cells = [(geom, M, m) for geom in ("point", "exp") for M in MASSES for m in MBOS]
    if MODE in ("C", "D"):
        cells = [c for c in cells if c[2] in (1e-23, 1e-22)]
    if MODE == "E":
        cells = [c for c in cells if c[2] == 1e-23]
    if MODE == "A":
        outs = None
    else:
        R.P(f"cells: {len(cells)}  (x2 footings, rule (ii))  workers {NPROC}")
        with Pool(NPROC) as pool:
            outs = pool.map(run_cell, cells, chunksize=1)
    # table (built from either the SP scan or the target's own rho_c)
    J = {f: {} for f in FOOT}
    slopes = {}
    if MODE == "A":
        R.P("MUTATE A: rho_psi replaced by the target's own rho_c (re-derived from the CFG44 definition, own ODE)")
        for geom in ("point", "exp"):
            for M in MASSES:
                for f in FOOT:
                    worst, sl = target_J_and_slope(geom, M, f)
                    for m in MBOS: J[f][(geom, M, m)] = worst
    else:
        for o in outs:
            for f in FOOT:
                J[f][(o["geom"], o["M"], o["m"])] = None if o["opt"][f] is None else o["opt"][f]["J"]
    if MODE not in ("A",):
        control_S3S4(outs)
        if MODE in ("", "E"):
            control_S4(outs)
    # ---- report
    R.P()
    R.P("RULE-(ii) J TABLE (dex; largest |log10 C_SP/C_target| over x in [0.1, 30]); canonical footing, README value in brackets")
    R.P("  {:<16}".format("cell") + "".join(f"{m:>26.0e}" for m in MBOS))
    for geom in ("point", "exp"):
        for M in MASSES:
            row = []
            for j, m in enumerate(MBOS):
                v = J["canonical"].get((geom, M, m))
                rd = README_J[(geom, M)][j]
                row.append("n/a" if v is None else f"{v:.4g} [{rd:g}]")
            R.P("  {:<16}".format(f"{geom} {M:.0e}") + "".join(f"{x:>26}" for x in row))
    R.P("ALT footing:")
    for geom in ("point", "exp"):
        for M in MASSES:
            R.P("  {:<16}".format(f"{geom} {M:.0e}") + "".join(f"{('n/a' if J['alt'].get((geom, M, m)) is None else format(J['alt'][(geom, M, m)], '.4g')):>26}" for m in MBOS))
    R.P()
    verdicts = {}
    finite = lambda f: {k: v for k, v in J[f].items() if v is not None}
    # P1
    R.P("FROZEN LINES")
    p1 = {}
    for f in FOOT:
        jf = finite(f)
        if not jf: p1[f] = None; continue
        kmin = min(jf, key=jf.get); p1[f] = (kmin, jf[kmin])
    tgt = {"canonical": 4.26, "alt": 4.0}
    ok1 = all(p1[f] is not None and p1[f][0] == ("exp", 1e9, 1e-23) and abs(p1[f][1] - tgt[f]) <= 0.3 for f in FOOT)
    R.check("P1 closest cell = (exp 1e9, h=2, m=1e-23), J within 0.3 dex of 4.26 / 4.0",
            "; ".join(f"{f}: {p1[f][0]} J = {p1[f][1]:.4f}" if p1[f] else f"{f}: none" for f in FOOT), ok1)
    # P2
    ok2 = True; parts = []
    for f in FOOT:
        jf = finite(f)
        mn = min(jf.values()) if jf else float("nan"); nband = sum(1 for v in jf.values() if v <= 0.0458)
        parts.append(f"{f}: min J = {mn:.4g}, cells within band = {nband}, undefined cells = {len(J[f]) - len(jf)}")
        ok2 = ok2 and jf and mn >= 3.0 and nband == 0
    R.check("P2 verdict: J >= 3.0 dex in every cell (H1 = FAIL)", "; ".join(parts), ok2)
    # P3
    ok3 = True; parts = []
    wj = {}
    for f in FOOT:
        wm = {}
        for m in MBOS:
            vals = [(J[f].get((geom, M, m)), (geom, M)) for geom in ("point", "exp") for M in MASSES]
            if any(v is None for v, _ in vals): wm[m] = (float("inf"), None); continue
            wm[m] = max(vals, key=lambda t: t[0])
        best = min(wm, key=lambda m: wm[m][0]); wj[f] = (best, wm[best])
        parts.append(f"{f}: best m = {best:.0e} eV, worst galaxy {wm[best][1]} J = {wm[best][0]:.5g}")
    ratio = wj["alt"][1][0]/wj["canonical"][1][0] if wj["canonical"][1][0] > 0 else float("nan")
    ok3 = (wj["canonical"][0] == 1e-23 and wj["alt"][0] == 1e-23 and abs(wj["canonical"][1][0]/1.18e5 - 1) <= 0.01
           and 0.89 <= ratio <= 0.94 and wj["canonical"][1][1] == ("point", 1e12))
    R.check("P3 best single m = 1e-23, worst galaxy point 1e12 with J within 1% of 1.18e5, alt/canonical in [0.89, 0.94]", "; ".join(parts) + f"; alt/canonical = {ratio:.4f}", ok3)
    # P4 table
    n_ok = 0; devs = []
    for geom in ("point", "exp"):
        for M in MASSES:
            for j, m in enumerate(MBOS):
                v = J["canonical"].get((geom, M, m)); rd = README_J[(geom, M)][j]
                if v is None: continue
                tol = max(0.3, 0.02*rd)
                good = abs(v - rd) <= tol
                n_ok += good; devs.append((geom, M, m, v, rd, v/rd - 1, good))
    verdict4 = "agreement" if n_ok >= 29 else ("partial" if n_ok >= 24 else "disagreement")
    R.check("P4 table: 32 canonical cells within max(0.3 dex, 2%) of the README table", f"{n_ok}/32 within tolerance -> {verdict4} (2-s.f. README entries carry up to 1.4% rounding)", n_ok >= 29)
    big = [(k, v) for k, v in J["canonical"].items() if v is not None and v > 100 and J["alt"].get(k) is not None]
    rat = [J["alt"][k]/v for k, v in big]
    R.check("P4b tail-dominated cells: alt/canonical = 0.910 +- 0.02", (f"{len(big)} cells, ratio range [{min(rat):.4f}, {max(rat):.4f}]" if rat else "no cell with J > 100"), bool(rat) and all(abs(x - 0.910) <= 0.02 for x in rat))
    # P5, P6 on closest cell
    o1 = [o for o in outs if (o["geom"], o["M"], o["m"]) == ("exp", 1e9, 1e-23)] if outs else []
    if o1 and o1[0]["opt"]["canonical"] and o1[0]["opt"]["alt"]:
        oc = o1[0]["opt"]["canonical"]; oa = o1[0]["opt"]["alt"]
        R.check("P5 R1 profile at the closest cell (canonical): log10 ratio at x = 0.1, 1, 30 within 0.3 dex of -3.57, -2.58, -4.26; argmax x = 30",
                f"{oc['lr01']:.3f}, {oc['lr1']:.3f}, {oc['lr30']:.3f}; argmax x = {oc['xargmax']:.3g}",
                abs(oc["lr01"] + 3.57) <= 0.3 and abs(oc["lr1"] + 2.58) <= 0.3 and abs(oc["lr30"] + 4.26) <= 0.3 and abs(oc["xargmax"] - 30) < 1e-6)
        R.check("P6 M_sol/M_b at the closest cell: 0.64 (canonical) and 0.76 (alt) each within 0.1 dex",
                f"canonical {oc['s']:.4f}, alt {oa['s']:.4f}", abs(math.log10(oc["s"]/0.64)) <= 0.1 and abs(math.log10(oa["s"]/0.76)) <= 0.1)
    # P7
    core_cells = []; env = []; both = 0; ncell = 0; argmax30 = 0
    for o in outs or []:
        for f in FOOT:
            ev = o["opt"][f]
            if ev is None: continue
            ncell += 1
            env.append(ev["slope30"]); argmax30 += (abs(ev["xargmax"] - 30) < 1e-6)
            both += (abs(ev["lr01"]) > 0.3 and abs(ev["lr30"]) > 0.3)
            if ev["core_ratio"] >= 0.5: core_cells.append((o["geom"], o["M"], o["m"], f, ev["slope01"]))
    if outs:
        okc = len(core_cells) > 0 and all(c[2] <= 1e-22 and c[1] <= 1e10 and -0.15 <= c[4] <= 0.0 for c in core_cells)
        R.check("P7a core: flat-core cells exist, all with m <= 1e-22 and M_b <= 1e10, slope in [-0.15, 0]",
                f"{len(core_cells)} core cells (of {ncell}); slope range " + (f"[{min(c[4] for c in core_cells):.4f}, {max(c[4] for c in core_cells):.4f}]" if core_cells else "n/a"), okc)
        R.check("P7b envelope: slope at x = 30 <= -6 in every cell, shallowest in [-18, -4.5], steepest <= -1e9",
                f"shallowest {max(env):.3g}, steepest {min(env):.3g}", max(env) <= -6 and -18 <= max(env) <= -4.5 and min(env) <= -1e9)
        R.check("P7c both ends fail (|log ratio| > 0.3 at x=0.1 and 30) in all cells; argmax at x = 30 in >= 90%", f"both: {both}/{ncell}; argmax x=30: {argmax30}/{ncell}", both == ncell and argmax30 >= 0.9*ncell)
        # target slopes at x=0.1 (own ODE)
        tsl = {}
        for M in MASSES:
            _, sl = target_J_and_slope("exp", M, "canonical"); tsl[M] = sl
        _, slp = target_J_and_slope("point", 1e9, "canonical")
        R.check("P7d target slope at x = 0.1 (own ODE): point -1.0099, exp spheres in [-1.05, -0.45]", f"point {slp:.4f}; " + ", ".join(f"{M:.0e}: {v:.3f}" for M, v in tsl.items()),
                abs(slp + 1.0099) < 1e-3 and all(-1.05 <= v <= -0.45 for v in tsl.values()))
    if outs:
        flat = [(o["geom"], o["M"], o["m"], f, o["opt"][f]["slope01"]) for o in outs for f in FOOT if o["opt"][f] is not None and o["opt"][f]["slope01"] > -0.075]
        R.P(f"POST-HOC (undeclared, does not re-score P7a): cells whose boson log-slope at x = 0.1 is above -0.075: {len(flat)} of {ncell}; "
            + (f"slope range [{min(c[4] for c in flat):.4f}, {max(c[4] for c in flat):.4f}], max m = {max(c[2] for c in flat):.0e}, max M_b = {max(c[1] for c in flat):.0e}" if flat else "none"))
        R.P("  core cells under the declared rho(0.1 r_M)/rho(0) >= 0.5: " + "; ".join(f"{g} {M:.0e} m={m:.0e} {f[:3]} {sl:.3f}" for g, M, m, f, sl in core_cells))
    # R1-type rows on all closest per mass
    R.P()
    R.P("rule-(ii) optimum rows (canonical): cell -> s = M_sol/M_b, kappa, J, argmax x, log10 ratio at x = 0.1 / 1 / 30, core ratio, slopes at 0.1 / 30, seconds")
    for o in outs or []:
        ev = o["opt"]["canonical"]
        if ev is None: R.P(f"  {o['geom']} {o['M']:.0e} m={o['m']:.0e}: NO BOUND STATE / no defined J"); continue
        R.P(f"  {o['geom']:5s} {o['M']:.0e} m={o['m']:.0e}: s={ev['s']:.3e} kappa={ev['kappa']:.4g} J={ev['J']:.5g} xmax={ev['xargmax']:.3g} lr={ev['lr01']:.3f}/{ev['lr1']:.3f}/{ev['lr30']:.4g} core={ev['core_ratio']:.3g} slope={ev['slope01']:.4f}/{ev['slope30']:.4g} it={ev['iters']} conv={ev['conv']}  a_B/r_s={1/o['cg']['rs_over_aB']:.3g} ({o['seconds']:.0f}s)")
    # verdict/exit
    load = [c for c in R.checks if c[2]]
    allpass = all(c[1] for c in load)
    R.P()
    R.P(f"seconds {time.time() - t00:.0f}")
    fails = [c[0] for c in load if not c[1]]
    if MODE:
        bites = len(fails) > 0
        R.P(f"MUTATE {MODE}: control {'BITES' if bites else 'DOES NOT BITE'}; failed load-bearing lines: {len(fails)}")
        for x in fails: R.P("   fail: " + x)
        rc = 1 if bites else 0
    else:
        R.P(f"main: {len(load) - len(fails)}/{len(load)} load-bearing checks pass")
        for x in fails: R.P("   FAIL: " + x)
        rc = 0 if allpass else 1
    R.P("kappa = 1/2 and Omega_c h^2 stay fitted. Nothing here says the data favour either model, or that the theory is closed.")
    with open(os.path.join(HERE, BASE + ".out"), "w") as f: f.write("\n".join(R.lines) + "\n")
    js = dict(mode=MODE or "main", cells=outs, J={f: {f"{k[0]}|{k[1]:.0e}|{k[2]:.0e}": v for k, v in J[f].items()} for f in FOOT}, nums=R.num,
              checks=[dict(name=n, ok=o, load=l) for n, o, l in R.checks], exit_code=rc)
    with open(os.path.join(HERE, BASE + "_results.json"), "w") as f: json.dump(js, f, indent=1, default=lambda x: float(x) if isinstance(x, (np.floating, np.integer)) else str(x))
    sys.exit(rc)

if __name__ == "__main__":
    main()
