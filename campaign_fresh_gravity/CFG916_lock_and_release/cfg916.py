#!/usr/bin/env python3
"""CFG916: lock-and-release (H-LR).  Criteria: FROZEN_CRITERIA.md (a3b2ffd2d, committed alone before this script).  HYPOTHESIS TEST.

H-LR = CFG915's LC latching + release: member-owned latched cold energy (t) beyond the member's King/Jacobi radius r_J in a host's
field becomes mobile (f) again.  r_J from the law's effective (baryons + cold energy) masses, no new constant; epoch pericentre
(primary), present position (alternative).  Two latching readings: LR-x (CFG915 LC exactly) and LR-c (capped capture).
Tests: G (CFG598 MW drift model), M (CFG726 eRASS1 / ACCEPT OUTER; eFEDS report), B (Bullet, record inputs), D (satellites at
CFG839 pericentres / CFG838 present positions; field dwarfs CFG873-875).

Run from this directory, one process at a time, in this order:
  CFG916_MODE=K OMP_NUM_THREADS=1 nice -n 10 python3 cfg916.py    -> computes + caches every run; K tests -> cfg916_K.out
  CFG916_MUTATE=1 OMP_NUM_THREADS=1 nice -n 10 python3 cfg916.py  -> cfg916_MUTATE.out, cfg916_results_MUTATE.json (exit 1 iff
                                                                     every required arm bites)
  OMP_NUM_THREADS=1 nice -n 10 python3 cfg916.py                  -> cfg916.out, cfg916_results.json
Read-only inputs: cfg598_lib, cfg637_lib, CFG4_common, cfg652_model, cfg599_lib (imported); CFG915 Run2 and CFG726 / CFG839 code
(copied); result JSONs of CFG915, 598, 726, 828, 827, 838, 839, 873, 874, 875, 623 runs; CFG687 per-cluster arrays; CFG686 JSON;
LVD csv files; CFG726 / CFG652 / CFG686 work files in ../../_external_data (not committed).  Nothing downloaded; no other lane edited.
kappa = 1/2 FITTED; footings never pooled; cold energy is real gravitating mass; no particle species; not theory closed."""
import os, sys, io, json, math, time, contextlib, subprocess, csv
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_v] = "1"
sys.dont_write_bytecode = True
import warnings
warnings.filterwarnings("ignore")
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__)); LANES = os.path.dirname(HERE); REPO = os.path.dirname(LANES)
EXT = os.path.abspath(os.path.join(REPO, "..", "_external_data"))
W726 = os.path.join(EXT, "cfg726_work"); W652 = os.path.join(EXT, "cfg652_work")
MUT = os.environ.get("CFG916_MUTATE", "") == "1"
MODE = "mutate" if MUT else os.environ.get("CFG916_MODE", "main")
for d in ("CFG637_derived_reservoir", "CFG652_hot_group_discriminator", "CFG598_settling_front_partial", "CFG599_merger_stopwatch_v2"):
    sys.path.insert(0, os.path.join(LANES, d))
sys.path.insert(0, LANES)
with contextlib.redirect_stdout(io.StringIO()):
    import cfg637_lib as L                                          # noqa: E402  (read-only)
    import CFG4_common as C4                                        # noqa: E402
    import cfg652_model as M652                                     # noqa: E402
    import cfg598_lib as C                                          # noqa: E402
    import cfg599_lib as P599                                       # noqa: E402

T0 = time.time(); OUT = []


def P(s=""):
    print(s, flush=True); OUT.append(str(s))


def memcheck(stage):
    """abort if free + inactive memory < 10 GB (machine shared with a 1024^3 job)."""
    try:
        out = subprocess.run(["vm_stat"], capture_output=True, text=True).stdout
        pg = 16384
        for l in out.splitlines():
            if "page size of" in l:
                pg = int(l.split("page size of")[1].split()[0])
        val = {l.split(":")[0].strip(): int(l.split(":")[1].strip().rstrip(".")) for l in out.splitlines()[1:] if ":" in l}
        gb = (val.get("Pages free", 0) + val.get("Pages inactive", 0)) * pg / 1e9
    except Exception:
        return
    P(f"  [vm_stat before {stage}: free+inactive {gb:.1f} GB]")
    if gb < 10.0:
        P(f"  ABORT {stage}: free+inactive {gb:.1f} GB < 10 GB"); sys.exit(3)


rd = lambda p: json.load(open(os.path.join(LANES, p)))
CACHE_F = os.path.join(HERE, "cfg916_cache.json")
CACHE = json.load(open(CACHE_F)) if os.path.exists(CACHE_F) else {}
for _s in ("pde", "M", "sat", "misc", "K"):
    CACHE.setdefault(_s, {})


def jclean(o):
    if isinstance(o, dict):
        return {str(k): jclean(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)):
        return [jclean(v) for v in o]
    if isinstance(o, np.ndarray):
        return jclean(o.tolist())
    if isinstance(o, (np.bool_,)):
        return bool(o)
    if isinstance(o, (np.floating,)):
        o = float(o)
    if isinstance(o, (np.integer,)):
        return int(o)
    if isinstance(o, float) and not np.isfinite(o):
        return str(o)
    return o


def save_cache():
    json.dump(jclean(CACHE), open(CACHE_F, "w"), indent=0, sort_keys=True)


def fl(x):
    return float(x) if not isinstance(x, str) else float(x)


FOOTS = ("can", "alt"); FL = {"can": "canonical", "alt": "alt"}
ALPHAS_F = (0.5, 1.0)
R_CORE = 200.0
SUP_PER_COND = M652.COLD_PER_B / M652.F_COND_FLOOR                   # 53.64 x m (condensed progenitor)
A0K = {f: C4.A0[FL[f]] * L.SI_TO_KPCGYR2 for f in FOOTS}             # kpc / Gyr^2 (cfg637 units)
A0SI = {f: C4.A0[FL[f]] for f in FOOTS}


def nu_s(y):                                                         # CFG695: g_N = g^2/(g + a0)
    y = np.maximum(np.asarray(y, float), 1e-300)
    return 0.5 + np.sqrt(0.25 + 1.0 / y)


def nu_e(y):
    y = np.maximum(np.asarray(y, float), 1e-300)
    return 1.0 / (-np.expm1(-np.sqrt(y)))


_RTA = {}


def rta_of(M_ta, z):                                                 # CFG726
    k = (round(math.log10(M_ta), 4), round(z, 4))
    if k not in _RTA:
        _RTA[k] = L.r_ta_single(M_ta, 1.0 / (1.0 + z))[0]
    return _RTA[k]


def prog_halo(rg, Mshape, m, z, a0, nu):                             # CFG726 (copied)
    rta = rta_of(m / M652.F_COND_FLOOR / L.FB, z)
    mph, xe = L.phantom_trunc(rg / rta, m * Mshape, rta, a0, nu, SUP_PER_COND * m)
    return mph, rta, xe


def rJ_from_X(X, s, mcum):
    """invert r^3/m(<r) = X on the member grid s (monotone; running max).  X >= q(end) -> inf."""
    q = np.maximum.accumulate(s ** 3 / np.maximum(mcum, 1e-300))
    X = np.asarray(X, float)
    out = np.exp(np.interp(np.log(np.maximum(X, 1e-300)), np.log(q), np.log(s)))
    out = np.where(X >= q[-1], np.inf, out)
    return np.where(X <= q[0], s[0], out)


def host_table(r, M, tracerM=None):
    """host tables in kpc / Msun / (km/s): g, Phi (relative), gamma = dlnM/dlnr, isotropic-Jeans sigma^2 of a tracer M_tr(<r)."""
    GK = 4.30091e-6
    g = GK * M / r ** 2
    Phi = np.r_[0.0, np.cumsum(0.5 * (g[1:] + g[:-1]) * np.diff(r))]
    gam = np.gradient(np.log(np.maximum(M, 1e-300)), np.log(r))
    tab = dict(r=r, lr=np.log(r), M=M, lM=np.log(np.maximum(M, 1e-300)), g=g, Phi=Phi, gam=gam)
    if tracerM is not None:
        n = np.maximum(np.gradient(tracerM, r), 0.0) / (4 * math.pi * r ** 2)
        f = n * g
        I = np.zeros_like(r); I[:-1] = np.cumsum((0.5 * (f[1:] + f[:-1]) * np.diff(r))[::-1])[::-1]
        tab["sig2"] = np.where(n > 0, I / np.maximum(n, 1e-300), 0.0)
    return tab


def rJ_at(tab, rr, s, mcum):
    """King/Jacobi radius at host-centric radius rr (kpc): r_J^3/m(<r_J) = rr^3/((3 - gamma) M(<rr)); 3 - gamma <= 0 -> inf."""
    lrr = np.log(np.asarray(rr, float))
    M = np.exp(np.interp(lrr, tab["lr"], tab["lM"]))
    den = 3.0 - np.interp(lrr, tab["lr"], tab["gam"])
    X = np.where(den > 0, np.asarray(rr, float) ** 3 / (np.maximum(den, 1e-300) * M), 1e300)
    return np.where(den > 0, rJ_from_X(X, s, mcum), np.inf)


HX, HW = np.polynomial.hermite.hermgauss(8)
_sel = HX > 0
LX, LW = np.polynomial.laguerre.laggauss(8)
NODE_XR = np.repeat(HX[_sel], 8); NODE_U = np.tile(LX, int(_sel.sum()))
NODE_W = np.outer(2 * HW[_sel] / math.sqrt(math.pi), LW).ravel()          # sums to 1


def pericentres(tab, d):
    """isotropic Gaussian velocities at the Jeans sigma (4 |v_r| x 8 v_t nodes); r_p = root of 2(E - Phi) - L^2/r^2 below d,
    floored at the table's first radius."""
    ld = np.log(d)
    Phid = np.interp(ld, tab["lr"], tab["Phi"]); s2 = np.maximum(np.interp(ld, tab["lr"], tab["sig2"]), 0.0)
    vr = np.sqrt(2 * s2)[:, None] * NODE_XR[None, :]; vt = np.sqrt(2 * s2[:, None] * NODE_U[None, :])
    E = Phid[:, None] + 0.5 * (vr ** 2 + vt ** 2); Lsq = (d[:, None] * vt) ** 2
    F = lambda rr: 2 * (E - np.interp(np.log(rr), tab["lr"], tab["Phi"])) - Lsq / rr ** 2
    lo = np.full(vr.shape, tab["r"][0]); hi = np.broadcast_to(d[:, None], vr.shape).astype(float).copy()
    floor = F(lo) >= 0
    for _ in range(60):
        mid = np.sqrt(lo * hi); pos = F(mid) > 0
        hi = np.where(pos, mid, hi); lo = np.where(pos, lo, mid)
    rp = np.where(floor, tab["r"][0], hi)
    return np.minimum(rp, d[:, None]), vr, vt


# ===================================================================================================== G model (CFG915 Run2 copy)
GK, TU = C.GK, C.TU_GYR
WALL = 290.0


class Run3(C.Run):
    """CFG915 Run2 (copied verbatim for flux2 and the LC capture) + capped capture (LR-c) + release beyond r_J."""

    def flux2(self, mt, mf, at, af, rta, dtmax):
        N, V, A, rf = self.N, self.V, self.A, self.rf
        cellB = rf[:-1] < rta
        m = mt + mf
        rho = m / V
        d = np.where(cellB, np.maximum(self.mph / V - rho, 0.0), 0.0)
        Md = np.concatenate([[0.0], np.cumsum(d * V)])
        dpsi = GK * Md / rf ** 2
        don = slice(1, N)
        pops = []; dtc = np.inf; gam = 0.0
        for X, mX, aX in (("f", mf, af), ("t", mt, at)):
            if not (aX > 0 and np.isfinite(aX)):
                continue
            live = mX > self.thr
            tau = np.where(live, 1.0 / np.sqrt(4 * math.pi * GK * np.maximum(rho + self.rhob, 1e-300)), 0.0)
            ok = live[don] & cellB[don]
            v = aX * tau[don] * dpsi[1:N]
            rhoX = mX / V
            flux = rhoX[don] * v * A[1:N]
            with np.errstate(divide="ignore", over="ignore", invalid="ignore"):
                dtcX = np.where(ok & (v > 0), 0.4 * V[don] / np.maximum(A[1:N] * v, 1e-300), np.inf).min()
            sel = live & cellB
            gX = float((4 * math.pi * GK * rho * tau * aX)[sel].max()) if sel.any() else 0.0
            dtc = min(dtc, dtcX); gam = max(gam, gX)
            pops.append((X, mX, ok, flux, v))
        dt = min(dtc, 0.2 / gam if gam > 0 else np.inf, dtmax)
        new = {"t": mt, "f": mf}; vm = 0.0
        for X, mX, ok, flux, v in pops:
            tr = np.where(ok, np.minimum(flux * dt, mX[don]), 0.0)
            tr = np.where(ok & (mX[don] - tr < self.thr[don]) & (tr > 0), mX[don], tr)
            m2 = mX.copy(); m2[1:] -= tr; m2[:-1] += tr
            new[X] = m2
        mtot = new["t"] + new["f"]
        for X, mX, ok, flux, v in pops:
            sig = ok & (mtot[don] >= 1e-3 * self.mph[don])
            vm = max(vm, float(np.max(np.where(sig, v, 0.0))) if sig.any() else 0.0)
        return new["t"], new["f"], dt, vm

    def capture(self, mt, mf, rta, tol, cap):
        """LC (CFG915, tol 1e-12 branch): cells inside B, settled, no deficit inside.  cap 'x': all f -> t (CFG915 exactly);
        cap 'c' (LR-c): t raised only up to the phantom, dm_t = min(m_f, max(m_ph - m_t, 0))."""
        cellB = self.rf[:-1] < rta
        m = mt + mf
        short = np.maximum(self.mph - m, 0.0)
        cellset = m >= self.mph * (1 - tol)
        inner = np.concatenate([[0.0], np.cumsum(np.where(cellset, 0.0, short))])[:-1]
        noinner = inner == 0.0
        c = cellB & cellset & noinner & (mf > 0)
        if c.any():
            mt = mt.copy(); mf = mf.copy()
            if cap == "x":
                mt[c] += mf[c]; mf[c] = 0.0
            else:
                dd = np.minimum(mf[c], np.maximum(self.mph[c] - mt[c], 0.0)); mt[c] += dd; mf[c] -= dd
        return mt, mf

    def release(self, mt, mf, rJ):
        """member-owned t in cells whose centre lies beyond r_J becomes f (rJ = inf: none; rJ = 0: all)."""
        if not (rJ < self.rc[-1]):
            return mt, mf, 0.0
        sel = self.rc > rJ
        if not mt[sel].any():
            return mt, mf, 0.0
        rm = float(mt[sel].sum())
        mt = mt.copy(); mf = mf.copy(); mf[sel] = mf[sel] + mt[sel]; mt[sel] = 0.0
        return mt, mf, rm

    def run3(self, af, cap="x", rJ=np.inf, at=0.0, cap_tol=1e-12, maxsteps=4_000_000, dtcap_gyr=0.01):
        H = self.H; tend = H.t0
        mf = self.initial(); mt = np.zeros(self.N)
        self.thr = 1e-14 * H.Mcat / self.N * np.ones(self.N)
        t = H.t_s; k = 0; ndep = len(self.dep_t); n = 0; vmax = 0.0
        dtcap = dtcap_gyr / TU; wall0 = time.time(); walled = False
        moving = (af > 0 and np.isfinite(af)) or (at > 0 and np.isfinite(at))
        lc = cap in ("x", "c")
        rel_tot = 0.0; rel_max = 0.0
        while t < tend - 1e-12:
            xb = H.X_ta(t)
            if abs(xb / self.xb - 1) > 2e-3:
                self.set_baryons(xb)
            rta = H.r_ta(t)
            nxt = self.dep_t[k] if k < ndep else np.inf
            dtmax = min(dtcap, tend - t, max(nxt - t, 1e-9))
            if not moving:
                dt = dtmax
            else:
                mt, mf, dt, vm = self.flux2(mt, mf, at, af, rta, dtmax); vmax = max(vmax, vm)
            if lc:
                mt, mf = self.capture(mt, mf, rta, cap_tol, cap)
                mt, mf, rm = self.release(mt, mf, rJ); rel_tot += rm; rel_max = max(rel_max, rm)
            t += dt; n += 1
            while k < ndep and self.dep_t[k] <= t + 1e-12:
                mf = mf + self.deposit_profile(self.dep_R[k], self.dep_m[k]); k += 1
            if lc:
                mt, mf = self.capture(mt, mf, H.r_ta(t), cap_tol, cap)
                mt, mf, rm = self.release(mt, mf, rJ); rel_tot += rm; rel_max = max(rel_max, rm)
            if n >= maxsteps:
                break
            if (n & 1023) == 0 and time.time() - wall0 > WALL:
                walled = True; break
        transit = float(self.dep_m[k:].sum())
        self.set_baryons(H.X_ta(t))
        m = mt + mf
        return dict(mt=mt, mf=mf, m=m, t=t, n=n, hit_cap=bool(n >= maxsteps and t < tend - 1e-9), walled=walled,
                    mass_err=abs(m.sum() + transit - H.Mcat) / H.Mcat, vmax_over_Vf=vmax / self.Vf0, wall_s=time.time() - wall0,
                    rel_tot=rel_tot, rel_max=rel_max)


HOSTS = {}


def host(key):
    if key not in HOSTS:
        with contextlib.redirect_stdout(io.StringIO()):
            HOSTS[key] = C.Host(None, mw=True) if key == "MW" else C.Host(float(key))
    return HOSTS[key]


def akey(a):
    return "inf" if not np.isfinite(a) else f"{a:g}"


def rkey(r):
    return "inf" if not np.isfinite(r) else f"{r:.6g}"


def gt(hkey, foot, cap, af, rJ=np.inf):
    """one drift-PDE run (cached by its full setting): small diagnostics (+ label arrays for grid hosts)."""
    key = f"{hkey}|{foot}|{cap}|af{akey(af)}|rJ{rkey(rJ)}"
    if key in CACHE["pde"]:
        return CACHE["pde"][key]
    H = host(hkey)
    R = Run3(H, foot, "P0", N=300)
    o = R.run3(af, cap, rJ)
    m, mt, mf = o["m"], o["mt"], o["mf"]
    rf = R.rf
    with np.errstate(divide="ignore", invalid="ignore"):
        q = np.where(R.mph > 0, m / R.mph, np.inf)
    out = dict(n=o["n"], hit_cap=o["hit_cap"], walled=o["walled"], mass_err=o["mass_err"], wall_s=round(o["wall_s"], 2),
               t_frac=float(mt.sum() / m.sum()), rel_tot=o["rel_tot"], rel_max=o["rel_max"], rta0_kpc=H.rta0, rc_last=float(R.rc[-1]))
    settled = (m >= R.mph * (1 - 1e-12)) | (R.mph <= 0)
    j = int(np.argmin(settled)) if not settled.all() else R.N
    out["r_cap_kpc"] = float(rf[j])
    if hkey == "MW":
        sel = rf[1:] <= 30.0
        mph = R.mph[sel]
        out.update(min_q=float(np.min(q[sel][mph > 0])), max_q=float(np.max(q[sel][mph > 0])),
                   Mc_over_Mph=float(m[sel].sum() / R.mph[sel].sum()), f_share_30=float(mf[sel].sum() / m[sel].sum()))
        out["i_holds"] = bool(out["min_q"] >= 0.99 and not (out["Mc_over_Mph"] - 1 > 0.01))
    else:
        s = rf[1:] <= R_CORE
        out["phi_f_200"] = float(mf[s].sum() / max(m[s].sum(), 1e-300))
        out["rf"] = rf.tolist(); out["mt"] = mt.tolist(); out["mf"] = mf.tolist()
    CACHE["pde"][key] = jclean(out); save_cache()
    P(f"    run {key}: {o['wall_s']:.1f} s, n {o['n']}" + (" [WALL]" if o["walled"] else "") + (" [CAP]" if o["hit_cap"] else ""))
    return CACHE["pde"][key]


# ===================================================================================================== record numbers
R915 = rd("CFG915_population_label_mobility/cfg915_results.json")
C915 = rd("CFG915_population_label_mobility/cfg915_runs_cache.json")
R598 = rd("CFG598_settling_front_partial/cfg598_results.json")
R726 = rd("CFG726_merger_memory/cfg726_results.json")
PHI = R915["phi_lin"]


# ===================================================================================================== G: r_J of the MW in M31's field
def m31_position():
    import astropy.units as u
    import astropy.coordinates as coord
    from scipy.optimize import least_squares
    ra, dec, dist, dm = [], [], [], []
    for f in ("lvd_dwarf_mw.csv", "lvd_dwarf_m31.csv", "lvd_dwarf_local_field.csv"):
        for r in csv.DictReader(open(os.path.join(REPO, "real_research", "data", "dsph", f))):
            try:
                v = [float(r["ra"]), float(r["dec"]), float(r["distance"]), float(r["distance_m31"])]
            except (ValueError, KeyError, TypeError):
                continue
            if all(np.isfinite(v)):
                ra.append(v[0]); dec.append(v[1]); dist.append(v[2]); dm.append(v[3])
    c = coord.SkyCoord(ra=np.array(ra) * u.deg, dec=np.array(dec) * u.deg, distance=np.array(dist) * u.kpc).transform_to(coord.Galactocentric())
    X = np.c_[c.x.to(u.kpc).value, c.y.to(u.kpc).value, c.z.to(u.kpc).value]; D = np.array(dm)
    res = least_squares(lambda x: np.linalg.norm(X - x, axis=1) - D, x0=np.array([-380.0, 610.0, -280.0]))
    resid = np.linalg.norm(X - res.x, axis=1) - D
    return res.x, float(np.sqrt(np.mean(resid ** 2))), len(D)


def law_point_table(Mb, foot, r):
    """host = point-mass baryons Mb under the law (nu_s), cfg637 units for y; masses in Msun."""
    y = L.G * Mb / (r ** 2 * A0K[foot])
    return host_table(r, Mb * nu_s(y))


def mw_rJ():
    if "G_rJ" in CACHE["misc"]:
        return CACHE["misc"]["G_rJ"]
    x, rms, n = m31_position()
    d = float(np.linalg.norm(x))
    s = np.geomspace(1e-2, 3e3, 3000)
    shape = s ** 2 / (s + 2.5) ** 2                                  # Hernquist a = 2.5 kpc (CFG598 MW)
    out = dict(x_m31=x.tolist(), d_kpc=d, fit_rms_kpc=rms, n_rows=n)
    rt = np.geomspace(1.0, 5e3, 4000)
    for f in FOOTS:
        T, _, _ = prog_halo(s, shape, 6.0e10, 0.0, A0K[f], nu_s)
        tab = law_point_table(1.0e11, f, rt)
        out[f] = float(rJ_at(tab, np.array([d]), s, 6.0e10 * shape + T)[0])
    CACHE["misc"]["G_rJ"] = out; save_cache()
    return out


# ===================================================================================================== M: clusters (CFG726 harness, copied)
G_SI = 6.674e-11; MSUN = 1.989e30; MPC = 3.0857e22; KG = MSUN / (3.0857e16) ** 2
RGRID = np.logspace(-3, np.log10(30), 3000); U_GRID = np.linspace(0, 1, 4001)
EDGES = np.logspace(np.log10(0.15), np.log10(3.0), 9); RC = np.sqrt(EDGES[1:] * EDGES[:-1])
RK_GRID = RGRID * 1000.0
R_OBS = np.geomspace(0.5, 6e4, 900)
RCOARSE = np.geomspace(0.3, 3.0e4, 170)
DK = np.geomspace(1.0, 3000.0, 140)
DM_ = np.sqrt(DK[1:] * DK[:-1])
SM_ = np.r_[R_OBS[0] * 0.5, np.sqrt(R_OBS[1:] * R_OBS[:-1])]
RE_GAL = M652.RE_BCG
A0SI726 = {FL[f]: C4.A0[FL[f]] for f in FOOTS}


def shell_frac(s, d, R):
    f = (R ** 2 - (d - s) ** 2) / (4.0 * np.maximum(d * s, 1e-300))
    f = np.clip(f, 0.0, 1.0)
    f = np.where(R >= s + d, 1.0, f)
    f = np.where(R <= np.abs(s - d), 0.0, f)
    return f


def convolve_members(dk, Ncum, sk, Tcum, Rout_kpc):                 # CFG726 (copied verbatim)
    dN = np.diff(Ncum); dm = np.sqrt(dk[1:] * dk[:-1])
    dT = np.r_[Tcum[0], np.diff(Tcum)]; sm = np.r_[sk[0] * 0.5, np.sqrt(sk[1:] * sk[:-1])]
    Cc = np.zeros(len(RCOARSE))
    for j0 in range(0, len(RCOARSE), 34):
        Rj = RCOARSE[j0:j0 + 34]
        A = shell_frac(sm[None, :, None], dm[:, None, None], Rj[None, None, :])
        Cc[j0:j0 + 34] = np.einsum("d,s,dsr->r", dN, dT, A)
    Cc = np.maximum.accumulate(Cc)
    lo = np.log(np.maximum(Cc, 1e-300))
    out = np.exp(np.interp(np.log(Rout_kpc), np.log(RCOARSE), lo, left=-700.0))
    out[Rout_kpc > RCOARSE[-1]] = Cc[-1]
    return np.where(out < 1e-250, 0.0, out)


_ABLK = None


def ablocks():
    global _ABLK
    if _ABLK is None:
        _ABLK = [shell_frac(SM_[None, :, None], DM_[:, None, None], RCOARSE[j0:j0 + 34][None, None, :]) for j0 in range(0, len(RCOARSE), 34)]
    return _ABLK


def convolve_members_w(Ncum, Tcum, Rout_kpc, Wt):
    """CFG726 convolve_members on (DK, R_OBS) with a per-position retention weight Wt[d, s] (fraction of nodes with r_J > s)."""
    dN = np.diff(Ncum); dT = np.r_[Tcum[0], np.diff(Tcum)]
    dNT = dN[:, None] * dT[None, :] * Wt
    Cc = np.zeros(len(RCOARSE))
    for b, j0 in enumerate(range(0, len(RCOARSE), 34)):
        Cc[j0:j0 + 34] = np.einsum("ds,dsr->r", dNT, ablocks()[b])
    Cc = np.maximum.accumulate(Cc)
    lo = np.log(np.maximum(Cc, 1e-300))
    out = np.exp(np.interp(np.log(Rout_kpc), np.log(RCOARSE), lo, left=-700.0))
    out[Rout_kpc > RCOARSE[-1]] = Cc[-1]
    return np.where(out < 1e-250, 0.0, out)


def sigma_proj(rhoL, r, R):
    umax = np.arccosh(r[-1] / R); u = U_GRID * umax; rr = R * np.cosh(u)
    rho_u = np.exp(np.interp(np.log(rr), np.log(r), np.log(np.maximum(rhoL, 1e-300))))
    return 2 * np.trapz(rho_u * rr * MPC, u)


def dsig_from_M(ML_msun):
    ML = ML_msun * MSUN; r = RGRID
    rhoL = np.gradient(ML, r * MPC) / (4 * np.pi * (r * MPC) ** 2)
    Sig = np.array([sigma_proj(rhoL, r, R) for R in RC])
    M2 = np.array([np.interp(R, r, ML) + np.trapz(4 * np.pi * (r[r > R] * MPC) ** 2 * rhoL[r > R] * (1 - np.sqrt(1 - (R / r[r > R]) ** 2)), r[r > R] * MPC) for R in RC])
    return (M2 / (np.pi * (RC * MPC) ** 2) - Sig) / KG


def law_M(Mb_msun, foot, nu):
    gb = G_SI * Mb_msun * MSUN / (RGRID * MPC) ** 2
    return Mb_msun * nu(gb / A0SI726[foot])


def erass_gas(i, d):
    R5, mgas = float(d["R500"][i]), float(d["mg"][i])
    r = RGRID; rc = 0.15 * R5; shape = (1 + (r / rc) ** 2) ** (-1.0); shape[r > 3.0] = 0
    dm = 4 * np.pi * (r * MPC) ** 2 * shape; Mm = np.r_[0, np.cumsum(0.5 * (dm[1:] + dm[:-1]) * np.diff(r * MPC))]
    return Mm * (mgas / np.interp(R5, r, Mm))


def lr_weights(tab, s, mcum):
    """retention weights per member position: pericentre (primary) and present (alternative); plus r_J summaries."""
    rp, vr, vt = pericentres(tab, DM_)
    rJp = rJ_at(tab, rp, s, mcum)                                    # (nd, nodes)
    Wp = np.einsum("w,dws->ds", NODE_W, (SM_[None, None, :] < rJp[:, :, None]).astype(float))
    rJn = rJ_at(tab, DM_, s, mcum)
    Wn = (SM_[None, :] < rJn[:, None]).astype(float)
    return Wp, Wn, rJp, rJn, rp


def wmedian(x, w):
    x = np.asarray(x, float).ravel(); w = np.asarray(w, float).ravel()
    ok = w > 0
    x, w = x[ok], w[ok]
    o = np.argsort(x); c = np.cumsum(w[o]) / w.sum()
    return float(x[o][np.searchsorted(c, 0.5)])


def cluster_variants(Mg, fs, z, Nmem, foot):
    """CFG726 primary member model (nu_s), variants: law (= release-all), hmm (= release-none, CFG726 path verbatim),
    lrp (LR-c pericentre), lrn (LR-c present)."""
    f = FL[foot]
    Mb = Mg * (1 + fs); Ms = fs * Mg; Mstar = float(Ms[-1])
    Ncum = np.interp(DK / 1000.0, RGRID, Mg) / Mg[-1]
    Mlaw = law_M(Mb, f, nu_s); T = Mlaw - Mb
    nmem = max(1, int(round(Nmem))); mi = Mstar / nmem
    sk = R_OBS; shape = M652.hern(sk, 1.0, RE_GAL)
    h, rt, xe = prog_halo(sk, shape, mi, z, A0K[foot], nu_s)
    C1 = nmem * convolve_members(DK, Ncum, sk, h, RK_GRID)
    tab = host_table(RK_GRID, Mlaw, Mg)
    mcum = mi * shape + h
    Wp, Wn, rJp, rJn, rp = lr_weights(tab, sk, mcum)
    Cp = nmem * convolve_members_w(Ncum, h, RK_GRID, Wp)
    Cn = nmem * convolve_members_w(Ncum, h, RK_GRID, Wn)
    out = dict(law=dsig_from_M(Mlaw), hmm=dsig_from_M(Mb + np.maximum(C1, T)),
               lrp=dsig_from_M(Mb + np.maximum(Cp, T)), lrn=dsig_from_M(Mb + np.maximum(Cn, T)))
    F = float(np.max(np.maximum(C1 - T, 0))); Fp = float(np.max(np.maximum(Cp - T, 0))); Fn = float(np.max(np.maximum(Cn - T, 0)))
    dNw = np.diff(Ncum)
    diag = dict(F=F, Fp_over_F=Fp / F if F > 0 else 0.0, Fn_over_F=Fn / F if F > 0 else 0.0,
                C1Mpc_ratio_p=float(np.interp(1000.0, RK_GRID, Cp) / max(np.interp(1000.0, RK_GRID, C1), 1e-300)),
                rJp_med=wmedian(np.minimum(rJp, 1e9), dNw[:, None] * NODE_W[None, :]), rJn_med=wmedian(np.minimum(rJn, 1e9), dNw),
                rp_over_d_med=wmedian(rp / DM_[:, None], dNw[:, None] * NODE_W[None, :]), edge_kpc=None if xe is None else xe * rt, m_i=mi, N=nmem)
    # transport clock of the released surplus at r = 1.5 Mpc (report only)
    r = RK_GRID; GKk = 4.30091e-6
    rho_c = np.gradient(T, r) / (4 * math.pi * r ** 2); rho_b = np.gradient(Mb, r) / (4 * math.pi * r ** 2)
    rc_, rb_ = float(np.interp(1500.0, r, rho_c)), float(np.interp(1500.0, r, rho_b))
    G4 = 4 * math.pi * GKk
    diag["Gamma_per_alpha_Gyr"] = float(G4 * rc_ / math.sqrt(G4 * (rb_ + rc_)) * L.KMS)
    # K-M-W code-path check: weight 1 against the verbatim convolution
    C1w = nmem * convolve_members_w(Ncum, h, RK_GRID, np.ones_like(Wp))
    diag["KMW_maxrel"] = float(np.max(np.abs(C1w - C1) / np.maximum(C1, 1e-300) * (C1 > 1e-200)))
    return out, diag, dict(tab=tab, mcum=mcum, sk=sk, rp=rp)


def score_TR(arrs_by_var):
    d = np.load(os.path.join(LANES, "CFG687_erass1_shear_stack", "cfg687_percluster.npz"))
    D, E = d["D"], d["E"]; W = np.where(E > 0, 1 / E ** 2, 0); n = len(D)
    order = np.argsort(d["ra"]); patch = np.empty(n, int); patch[order] = np.arange(n) * 30 // n
    BANDS = {"INNER": [0, 1, 2], "MID": [3, 4, 5], "OUTER": [6, 7]}

    def A_of(sel, Pm):
        return {b: (W[sel][:, j] * D[sel][:, j]).sum() / (W[sel][:, j] * Pm[sel][:, j]).sum() for b, j in BANDS.items()}

    def jk(fun):
        full = fun(np.ones(n, bool)); reps = [fun(patch != p) for p in range(30)]
        return {k: (float(full[k]), float(np.sqrt(29 / 30 * np.sum((np.array([r[k] for r in reps]) - np.mean([r[k] for r in reps])) ** 2)))) for k in full}
    out = {}
    for v, Pm in arrs_by_var.items():
        A = jk(lambda s: A_of(s, Pm))
        out[v] = dict(A=A, Z_mid=(A["MID"][0] - 1) / A["MID"][1], Z_outer=(A["OUTER"][0] - 1) / A["OUTER"][1])
    return out


def accept_inputs():
    from scipy.interpolate import PchipInterpolator
    c = 2.998e8; MP = 1.6726e-27
    zb = [0.510, 0.706, 0.934, 1.321, 1.484, 2.330]; DMr = [13.588, 17.351, 21.576, 27.601, 30.512, 38.988]
    DHb = 21.863 + (21.863 - 19.455) / (0.706 - 0.510) * (0.510 - 0.295); DMb = np.sqrt(7.942 ** 3 / (0.295 * DHb))
    pch = PchipInterpolator(np.r_[0, 0.295, zb], np.r_[0, DMb, DMr]); RD = 101.54 / 0.70
    DM = lambda z: pch(np.minimum(np.asarray(z, float), 2.33)) * RD
    prof = {}
    for l in open(os.path.join(EXT, "cfg686_inputs", "accept", "all_profiles.dat")):
        if l.startswith("#"):
            continue
        pp = l.split()
        try:
            prof.setdefault(pp[0], []).append([float(x) for x in pp[1:14]])
        except ValueError:
            pass
    C686 = rd("CFG686_cluster_shear_vs_law/cfg686_results.json")["clusters"]
    p = json.load(open(os.path.join(W726, "lambda.json")))["p"]
    res = []
    for cl in C686:
        Pp = np.array(prof[cl["key"]]); Pp = Pp[np.argsort(Pp[:, 0])]; rin, rout, ne = Pp[:, 0], Pp[:, 1], Pp[:, 2]
        ok_ = ne > 0; rin, rout, ne = rin[ok_], rout[ok_], ne[ok_]
        zl = cl["z"]; zz = np.linspace(0, zl, 400); Ez = np.sqrt(0.3 * (1 + zz) ** 3 + 0.7); DA_acc = np.trapz(1 / Ez, zz) * c / (70e3 / MPC) / MPC / (1 + zl)
        q = (float(DM(zl)) / (1 + zl)) / DA_acc; rin, rout, ne = rin * q, rout * q, ne * q ** -0.5
        rm = 0.5 * (rin + rout); rho = 1.17 * MP * ne * 1e6
        half = rm >= np.exp(0.5 * (np.log(rm[0]) + np.log(rm[-1]))); b0 = -np.polyfit(np.log(rm[half]), np.log(rho[half]), 1)[0]
        flag = not (b0 >= 1.5); b = 2.0 if flag else b0
        r = RGRID; rho_g = np.interp(r, rm, rho, left=rho[0], right=np.nan)
        out_ = r > rm[-1]; rho_g[out_] = rho[-1] * (r[out_] / rm[-1]) ** (-b); rho_g[r > 3.0] = 0.0
        Mg = np.r_[0, np.cumsum(0.5 * (4 * np.pi * (r[1:] * MPC) ** 2 * rho_g[1:] + 4 * np.pi * (r[:-1] * MPC) ** 2 * rho_g[:-1]) * np.diff(r) * MPC)] / MSUN
        mg1 = float(np.interp(1.0, RGRID, Mg)); Nm = 10 ** (p[0] * math.log10(mg1) + p[1])
        res.append(dict(Mg=Mg, z=zl, Nm=Nm, name=cl["name"]))
    return res, C686


def score_TA(arrs_by_var, C686):
    D_ = np.nan_to_num(np.array([x["dsig"] for x in C686])); E_ = np.array([x["err"] for x in C686])
    W_ = np.where(np.isfinite(E_) & (E_ > 0), 1 / E_ ** 2, 0)
    BANDS = {"INNER": [0, 1, 2], "MID": [3, 4, 5], "OUTER": [6, 7]}

    def bandA(Pm, sel):
        o_ = {}
        for b, j in BANDS.items():
            num = (W_[sel][:, j] * D_[sel][:, j]).sum(); den = (W_[sel][:, j] * Pm[sel][:, j]).sum(); o_[b] = num / den if den != 0 else np.nan
        return o_
    out = {}
    for v, Pm in arrs_by_var.items():
        A = bandA(Pm, np.arange(len(C686))); rb = np.random.default_rng(1)
        boots = [bandA(Pm, rb.integers(0, len(C686), len(C686))) for _ in range(1000)]
        sig = {b: float(np.nanstd([bb[b] for bb in boots])) for b in BANDS}
        out[v] = dict(A={b: [float(A[b]), sig[b]] for b in BANDS}, Z_mid=float((A["MID"] - 1) / sig["MID"]), Z_outer=float((A["OUTER"] - 1) / sig["OUTER"]))
    return out


def leapfrog_min_r(tab, d, vr, vt, T_kpc_per_kms, n=200000):
    """direct 2-D leapfrog in the spherical host table (kpc, km/s): minimum radius reached."""
    x = np.array([d, 0.0]); v = np.array([vr, vt]); dt = T_kpc_per_kms / n
    acc = lambda x: -np.interp(math.log(max(np.hypot(*x), 1e-6)), tab["lr"], tab["g"]) * x / max(np.hypot(*x), 1e-12)
    a = acc(x); rmin = d
    for _ in range(n):
        v = v + 0.5 * dt * a; x = x + dt * v; a = acc(x); v = v + 0.5 * dt * a
        rmin = min(rmin, math.hypot(x[0], x[1]))
    return rmin


def compute_M():
    if "eRASS1" in CACHE["M"] and "ACCEPT" in CACHE["M"]:
        return
    memcheck("M eRASS1")
    d = np.load(os.path.join(LANES, "CFG687_erass1_shear_stack", "cfg687_percluster.npz"))
    Nm = json.load(open(os.path.join(W726, "lambda.json")))["Nmem"]
    ER = list(np.load(os.path.join(W726, "erass.npy"), allow_pickle=True))
    n = len(d["mg"])
    arr = {f: {v: np.zeros((n, 8)) for v in ("law", "hmm", "lrp", "lrn")} for f in FOOTS}
    diags = {f: [] for f in FOOTS}
    kmn = 0.0; kma = 0.0; kmw = 0.0
    korb = None
    imed = int(np.argsort(d["mg"])[n // 2])
    for i in range(n):
        Mg = erass_gas(i, d)
        for f in FOOTS:
            o, dg, aux = cluster_variants(Mg, 0.20, float(d["z"][i]), float(Nm[i]), f)
            for v in o:
                arr[f][v][i] = o[v]
            diags[f].append(dg)
            kmn = max(kmn, float(np.max(np.abs(o["hmm"] / ER[i][f"hmm|s|{FL[f]}|primary"] - 1))))
            kma = max(kma, float(np.max(np.abs(o["law"] / ER[i][f"law|s|{FL[f]}"] - 1))))
            kmw = max(kmw, dg["KMW_maxrel"])
            if i == imed and f == "can":
                tab, rp = aux["tab"], aux["rp"]
                k = int(np.argmin(np.abs(DM_ - 500.0))); w = int(np.argmax(NODE_W * (rp[k] > 0.1 * DM_[k])))
                s2 = float(np.interp(math.log(DM_[k]), tab["lr"], tab["sig2"]))
                vr0 = math.sqrt(2 * s2) * NODE_XR[w]; vt0 = math.sqrt(2 * s2 * NODE_U[w])
                vc = math.sqrt(float(np.interp(math.log(DM_[k]), tab["lr"], tab["g"])) * DM_[k])
                rmin = leapfrog_min_r(tab, float(DM_[k]), vr0, vt0, 6 * 2 * math.pi * DM_[k] / vc)
                korb = dict(cluster=i, d_kpc=float(DM_[k]), node=w, rp_solver=float(rp[k, w]), rmin_leapfrog=rmin,
                            rel=abs(rmin / float(rp[k, w]) - 1), all_rp_le_d=bool(np.all(rp <= DM_[:, None] * (1 + 1e-12))))
        if (i + 1) % 40 == 0:
            P(f"  eRASS1 {i + 1}/{n} ({time.time() - T0:.0f} s)")
        if (i + 1) % 120 == 0:
            memcheck(f"eRASS1 {i + 1}")
    TR = {f: score_TR(arr[f]) for f in FOOTS}
    summ = {}
    for f in FOOTS:
        dd = diags[f]
        summ[f] = dict(Fp_over_F_med=float(np.median([x["Fp_over_F"] for x in dd])), Fn_over_F_med=float(np.median([x["Fn_over_F"] for x in dd])),
                       C1Mpc_ratio_p_med=float(np.median([x["C1Mpc_ratio_p"] for x in dd])),
                       rJp_med_kpc=float(np.median([x["rJp_med"] for x in dd])), rJn_med_kpc=float(np.median([x["rJn_med"] for x in dd])),
                       rp_over_d_med=float(np.median([x["rp_over_d_med"] for x in dd])),
                       Gamma_inv_Gyr={str(a): float(np.median([1.0 / (a * x["Gamma_per_alpha_Gyr"]) for x in dd])) for a in ALPHAS_F},
                       N_med=float(np.median([x["N"] for x in dd])), edge_med_kpc=float(np.median([x["edge_kpc"] or np.nan for x in dd])))
    CACHE["M"]["eRASS1"] = dict(TR=TR, summary=summ, K=dict(KMN_maxrel=kmn, KMA_maxrel=kma, KMW_maxrel=kmw, KORB=korb))
    save_cache()
    # ACCEPT
    memcheck("M ACCEPT")
    acc, C686 = accept_inputs()
    AC = list(np.load(os.path.join(W726, "accept.npy"), allow_pickle=True))
    arrA = {f: {v: np.zeros((len(acc), 8)) for v in ("law", "hmm", "lrp", "lrn")} for f in FOOTS}
    kmnA = 0.0; kmaA = 0.0; dA = {f: [] for f in FOOTS}
    for j, a in enumerate(acc):
        for f in FOOTS:
            o, dg, _ = cluster_variants(a["Mg"], 0.20, a["z"], a["Nm"], f)
            for v in o:
                arrA[f][v][j] = o[v]
            dA[f].append(dg)
            kmnA = max(kmnA, float(np.max(np.abs(o["hmm"] / AC[j][f"hmm|s|{FL[f]}|primary"] - 1))))
            kmaA = max(kmaA, float(np.max(np.abs(o["law"] / AC[j][f"law|s|{FL[f]}"] - 1))))
    TA = {f: score_TA(arrA[f], C686) for f in FOOTS}
    CACHE["M"]["ACCEPT"] = dict(TA=TA, K=dict(KMN_maxrel=kmnA, KMA_maxrel=kmaA),
                                summary={f: dict(Fp_over_F=[x["Fp_over_F"] for x in dA[f]], rJp_med_kpc=[x["rJp_med"] for x in dA[f]],
                                                 rJn_med_kpc=[x["rJn_med"] for x in dA[f]], N=[x["N"] for x in dA[f]]) for f in FOOTS})
    save_cache()


def compute_efeds():
    """eFEDS (report only): CFG726's T-E model (candidate B law, BCG concentric = host central, members on CFG652's satellite profile)
    with members' halos truncated at r_J; CFG652/CFG726 score code."""
    if "eFEDS" in CACHE["M"]:
        return
    if not os.path.exists(os.path.join(W652, "cfg652_inputs.npz")):
        CACHE["M"]["eFEDS"] = "inputs not on disk"; save_cache(); return
    memcheck("M eFEDS")
    from scipy.stats import chi2 as CHI2
    I = np.load(os.path.join(W652, "cfg652_inputs.npz"))
    RB = np.geomspace(30, 3000, 13); RCg = np.sqrt(RB[1:] * RB[:-1]); n = len(I["z"])
    arrs = {f"{v}|{f}": np.full((n, len(RCg)), np.nan) for v in ("base", "hmm", "lrp", "lrn") for f in FOOTS}
    for i in range(n):
        if I["Mcond"][i] <= 0:
            continue
        Mcd, Mh0, Rx, z = float(I["Mcond"][i]), float(I["Mhot"][i]), float(I["Rx_kpc"][i]), float(I["z"][i])
        mc, mh = M652.profiles(Mcd, Mh0, Rx, R_OBS, gas_trunc=2.0); core = mc + mh
        bc, sup, fret = M652.catchment(Mcd, float(mh[-1])); rta = rta_of(bc / L.FB, z)
        mbcg = min(float(I["Mbcg"][i]), Mcd); nmem = max(1, int(round(float(I["Nmem"][i])))); mi = (Mcd - mbcg) / nmem
        shape = M652.hern(R_OBS, 1.0, RE_GAL)
        Ncum = M652.hern(DK, 1.0, 0.5 * Rx)
        for f in FOOTS:
            a0 = A0K[f]
            T, xe = L.phantom_trunc(R_OBS / rta, core, rta, a0, nu_s, sup)
            arrs[f"base|{f}"][i] = M652.delta_sigma(R_OBS, core + T, RCg, rmax=rta)
            Cs = {v: np.zeros(len(R_OBS)) for v in ("hmm", "lrp", "lrn")}
            if mi > 0:
                h, rt, xm = prog_halo(R_OBS, shape, mi, z, a0, nu_s)
                Cs["hmm"] += nmem * convolve_members(DK, Ncum / Ncum[-1], R_OBS, h, R_OBS)
                tab = host_table(R_OBS, core + T, M652.hern(R_OBS, 1.0, 0.5 * Rx))
                Wp, Wn, _, _, _ = lr_weights(tab, R_OBS, mi * shape + h)
                Cs["lrp"] += nmem * convolve_members_w(Ncum / Ncum[-1], h, R_OBS, Wp)
                Cs["lrn"] += nmem * convolve_members_w(Ncum / Ncum[-1], h, R_OBS, Wn)
            if mbcg > 0:
                hb, _, _ = prog_halo(R_OBS, shape, mbcg, z, a0, nu_s)
                for v in Cs:
                    Cs[v] += hb
            for v in Cs:
                arrs[f"{v}|{f}"][i] = M652.delta_sigma(R_OBS, core + np.maximum(Cs[v], T), RCg, rmax=rta)
        if (i + 1) % 40 == 0:
            P(f"  eFEDS {i + 1}/{n} ({time.time() - T0:.0f} s)")
    EM = np.load(os.path.join(W726, "efeds.npz"))
    I0 = I; D0 = np.load(os.path.join(W652, "cfg652_esd.npz"))
    keep = I0["Mcond"] > 0
    krep = max(float(np.nanmax(np.abs(arrs[f"hmm|{f}"][keep] / EM[f"hmm__s__{FL[f]}"][keep] - 1))) for f in FOOTS)
    krepb = max(float(np.nanmax(np.abs(arrs[f"base|{f}"][keep] / EM[f"base__s__{FL[f]}"][keep] - 1))) for f in FOOTS)
    USE = (RCg >= 50) & (RCg <= 1000); BAND = (RCg >= 250) & (RCg <= 1000); NPATCH = 30
    Dd = {k: (D0[k][keep] if k in ("WG", "WX", "WW", "NN", "pg") else D0[k]) for k in D0.files}

    def esd(sel_g, sel_r):
        Wg = Dd["WW"][sel_g].sum(0); Wr = Dd["rWW"][sel_r].sum(0)
        g = Dd["WG"][sel_g].sum(0) / np.where(Wg > 0, Wg, np.nan); r = Dd["rWG"][sel_r].sum(0) / np.where(Wr > 0, Wr, np.nan)
        boost = (Dd["NN"][sel_g].sum(0) / max(sel_g.sum(), 1)) / (Dd["rNN"][sel_r].sum(0) / max(sel_r.sum(), 1))
        return boost * g - r

    def model_stack(arr, sel_g):
        Wm = Dd["WW"][sel_g]
        return (Wm * arr[sel_g]).sum(0) / np.where(Wm.sum(0) > 0, Wm.sum(0), np.nan)
    ng = int(keep.sum()); allg = np.ones(ng, bool); allr = np.ones(len(Dd["rz"]), bool)
    vals = np.array([esd(Dd["pg"] != p, Dd["pr"] != p)[USE] for p in range(NPATCH)]); mv = vals.mean(0)
    Cv = (NPATCH - 1) / NPATCH * (vals - mv).T @ (vals - mv)
    nb = int(USE.sum()); hart = (NPATCH - nb - 2) / (NPATCH - 1); Ci = np.linalg.inv(Cv) * hart
    obs = esd(allg, allr)
    aout = lambda o, m: float(np.log10(np.sum(o[BAND]) / np.sum(m[BAND])))
    TE = {}
    for f in FOOTS:
        for v in ("base", "hmm", "lrp", "lrn"):
            arr = arrs[f"{v}|{f}"][keep]; ms = model_stack(arr, allg); dd = obs[USE] - ms[USE]
            ch = float(dd @ Ci @ dd); p = float(CHI2.sf(ch, nb)); A = aout(obs, ms)
            Aj = np.array([aout(esd(Dd["pg"] != qq, Dd["pr"] != qq), model_stack(arr, Dd["pg"] != qq)) for qq in range(NPATCH)])
            sA = float(math.sqrt((NPATCH - 1) / NPATCH * np.sum((Aj - Aj.mean()) ** 2)))
            TE[f"{v}|{f}"] = dict(chi2=ch, p=p, A_out=A, sA=sA, pass_=bool(p >= 0.01 and abs(A) < 2 * sA))
    CACHE["M"]["eFEDS"] = dict(TE=TE, K_rep_hmm_maxrel=krep, K_rep_base_maxrel=krepb)
    save_cache()


# ===================================================================================================== D: satellites
def law_s_SI(gN, a0):
    return gN * float(nu_s(gN / a0))


def law_e_SI(gN, a0):
    return gN * float(nu_e(gN / a0))


def sat_orbit(r, Mmw, a0, lawf):
    """CFG839 orbit() (copied) with the law as a parameter: turning points in the law's MW field (SI)."""
    import astropy.units as u
    import astropy.coordinates as coord
    from scipy.optimize import brentq
    from scipy.integrate import quad
    Gs, Msun, KPC = 6.674e-11, 1.989e30, 3.0857e19
    c = coord.SkyCoord(ra=float(r["ra"]) * u.deg, dec=float(r["dec"]) * u.deg, distance=float(r["distance"]) * u.kpc,
                       pm_ra_cosdec=float(r["pmra"]) * u.mas / u.yr, pm_dec=float(r["pmdec"]) * u.mas / u.yr,
                       radial_velocity=float(r["vlos_systemic"]) * u.km / u.s).transform_to(coord.Galactocentric())
    x = np.array([c.x.to(u.m).value, c.y.to(u.m).value, c.z.to(u.m).value]); v = np.array([c.v_x.to(u.m / u.s).value, c.v_y.to(u.m / u.s).value, c.v_z.to(u.m / u.s).value])
    gf = lambda rr: lawf(Gs * Mmw * Msun / rr ** 2, a0)
    rn = float(np.linalg.norm(x)); Lz = float(np.linalg.norm(np.cross(x, v))); E0 = 0.5 * float(v @ v)
    Phi = lambda rr: quad(gf, rn, rr, limit=200)[0]
    f = lambda rr: 2 * (E0 - Phi(rr)) - Lz ** 2 / rr ** 2
    rp = brentq(f, 1e-3 * rn, rn * (1 - 1e-9)) if f(rn * (1 - 1e-9)) > 0 else rn
    return dict(rnow=rn / KPC, rp=rp / KPC)


def fnum(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return None


def compute_sats():
    if "rows" in CACHE["sat"]:
        return
    LVD = {}
    for fn in ("lvd_dwarf_mw.csv", "lvd_dwarf_m31.csv", "lvd_dwarf_local_field.csv"):
        for r in csv.DictReader(open(os.path.join(REPO, "real_research", "data", "dsph", fn))):
            LVD[r["name"]] = r
    R828 = rd("CFG828_dwarf_excess_rotation_vs_dispersion/cfg828_results.json")
    rows = {f: {x["name"]: x for x in R828[f"{FL[f]}|nu_e"]["rows"]} for f in FOOTS}
    U27 = rd("CFG827_dwarf_age_sfh_ml/cfg827_results.json")["rows"]
    R839 = rd("CFG839_pericentre_tides/cfg839_results.json")["rows"]
    s = np.geomspace(1e-4, 100.0, 4000)
    rt = np.geomspace(0.1, 5e3, 4000)
    tabs = {(h, f): law_point_table(M, f, rt) for h, M in (("mw", 6.0e10), ("m_031", 1.0e11)) for f in FOOTS}
    out = {}; kq = []
    for nm in rows["can"]:
        g = LVD.get(nm, {})
        hostk = g.get("host", "")
        if hostk not in ("mw", "m_031"):
            continue
        D = fnum(g.get("distance_host"))
        if D is None or D != D:
            continue
        rh_pc = fnum(g.get("rhalf_sph_physical")) or fnum(g.get("rhalf_physical"))
        a_kpc = rh_pc / 1000.0; r12 = (4.0 / 3.0) * a_kpc
        Ms = U27[nm]["ups"] * 10 ** (0.4 * (4.83 - fnum(g["M_V"])))
        Mst = Ms * s ** 3 / (s ** 2 + a_kpc ** 2) ** 1.5
        rec = dict(host=hostk, D_kpc=D, r12_kpc=r12, Ms=Ms)
        peri_ok = (hostk == "mw" and nm in R839)
        if peri_ok:
            o = sat_orbit(g, 6.0e10, 9.3603e-11, law_e_SI)                       # K-SAT: CFG839's own settings
            kq.append(abs(o["rp"] / R839[nm]["rp"] - 1)); rec["rp_K839"] = o["rp"]
        for f in FOOTS:
            rta = rta_of(Ms / M652.F_COND_FLOOR / L.FB, 0.0)
            T, _ = L.phantom_trunc(s / rta, Mst, rta, A0K[f], nu_s, SUP_PER_COND * Ms)
            mc = Mst + T
            rec[f"delta_{f}"] = rows[f][nm]["delta"]
            rec[f"rJ_present_{f}"] = float(rJ_at(tabs[(hostk, f)], np.array([D]), s, mc)[0])
            if peri_ok:
                o = sat_orbit(g, 6.0e10, A0SI[f], law_s_SI)
                rec[f"rp_{f}"] = o["rp"]; rec["rnow"] = o["rnow"]
                rec[f"rJ_peri_{f}"] = float(rJ_at(tabs[("mw", f)], np.array([o["rp"]]), s, mc)[0])
        out[nm] = rec
    CACHE["sat"] = dict(rows=out, K_SAT_maxrel=max(kq) if kq else None, K_SAT_n=len(kq))
    save_cache()


# ===================================================================================================== B: Bullet
def compute_B():
    if "B" in CACHE["misc"]:
        return
    out = {}
    runs = {}
    for f in FOOTS:
        P599f = "can" if f == "can" else "alt"
        main = P599.Progenitor599(1.5e15, P599f, cloud=False)
        sub = P599.Progenitor599(1.5e14, P599f, cloud=True)
        r = np.maximum(main.r, 1e-3)
        ok = main.r > 0
        tab = host_table(main.r[ok], main.Mtot[ok])
        s = sub.r[ok]; msub = sub.Mtot[ok]
        dgrid = np.geomspace(5.0, 720.0, 240)
        rJg = rJ_at(tab, dgrid, s, msub)
        rec = dict(rJ_present=float(rJ_at(tab, np.array([720.0]), s, msub)[0]), dgrid=dgrid.tolist(), rJ_grid=np.minimum(rJg, 1e12).tolist())
        # record head-on model pericentre (report only): minimum sampled galaxy separation in CFG623's alpha = 0 run
        try:
            rr = json.load(open(os.path.join(LANES, "CFG623_merger_stopwatch_v5", "runs", f"a0_{f}_v2666.7_eta1.132.json")))
            sep = [float(np.hypot(*(np.array(x["sub"]["gal"]) - np.array(x["main"]["gal"])))) for x in rr["diag"]]
            rec["dmin_model_kpc"] = min(sep)
            rec["rJ_dmin"] = float(rJ_at(tab, np.array([min(sep)]), s, msub)[0])
        except (OSError, KeyError):
            rec["dmin_model_kpc"] = None
        out[f] = rec
    CACHE["misc"]["B"] = out; save_cache()


def B_phi(run, rJ):
    rf = np.array(run["rf"]); mt = np.array(run["mt"]); mf = np.array(run["mf"]); m = mt + mf
    rc = np.sqrt(rf[1:] * rf[:-1]); s = rf[1:] <= R_CORE
    tot = max(m[s].sum(), 1e-300)
    rel = float(mt[s & (rc > rJ)].sum() / tot) if np.isfinite(rJ) else 0.0
    return float(mf[s].sum() / tot), rel


# ===================================================================================================== compute everything
def compute_all():
    rjmw = mw_rJ()
    P(f"G: M31 Galactocentric position fitted to {rjmw['n_rows']} LVD distance_m31 values: d = {rjmw['d_kpc']:.1f} kpc "
      f"(rms {rjmw['fit_rms_kpc']:.2f} kpc); r_J,MW (present; no MW-M31 pericentre yet) = {rjmw['can']:.0f} / {rjmw['alt']:.0f} kpc")
    memcheck("G runs")
    for f in FOOTS:
        for a in ALPHAS_F:
            for cap in ("x", "c"):
                for rJ in (np.inf, rjmw[f], 0.0):
                    gt("MW", f, cap, a, rJ)
            for cap in ("x", "c"):
                gt("14.0", f, cap, a)
    compute_B()
    compute_sats()
    compute_M()
    compute_efeds()


compute_all()
P()
P("CFG916  lock-and-release H-LR   criteria a3b2ffd2d   HYPOTHESIS TEST   mode " + MODE)
P("  kappa = 1/2 FITTED; footings 9.3603e-11 / 1.1312e-10 never pooled; cold energy real gravitating mass; no species; not theory closed.")
P("  readings: LR-x = CFG915 LC exactly + release; LR-c = capped capture + release.  t = latched (alpha_t 0), f = mobile (alpha_f 0.5/1).")
P()

# ===================================================================================================== K tests
K = {}


def kline(name, ok, msg):
    K[name] = dict(pass_=ok if isinstance(ok, str) else bool(ok), msg=msg)
    P(f"{name}: {msg} -> {ok if isinstance(ok, str) else ('PASS' if ok else 'FAIL')}")


rjmw = dict(CACHE["misc"]["G_rJ"])
for _f in FOOTS:
    rjmw[_f] = fl(rjmw[_f])


def rel(a, b):
    return abs(a / b - 1) if b != 0 else abs(a)


worst = 0.0; worst_all = 0.0; worst598 = 0.0; worst_call = 0.0
for f in FOOTS:
    for a in ALPHAS_F:
        o = gt("MW", f, "x", a, np.inf); ref = C915[f"MW|{f}|LC|af{akey(a)}|at0|X05|tol1e-12"]
        worst = max(worst, *(rel(o[k], ref[k]) for k in ("min_q", "max_q", "Mc_over_Mph", "f_share_30", "t_frac")))
        o = gt("MW", f, "x", a, 0.0); ref = C915[f"MW|{f}|REF|af{akey(a)}|at0|X05|tol1e-12"]
        worst_all = max(worst_all, *(rel(o[k], ref[k]) for k in ("min_q", "max_q", "Mc_over_Mph", "f_share_30")))
        r598 = R598["MW"][f"P0|{f}|{akey(a)}"]
        worst598 = max(worst598, *(rel(o[k], r598[k]) for k in ("min_q", "max_q", "Mc_over_Mph")))
        o = gt("MW", f, "c", a, 0.0)
        worst_call = max(worst_call, *(rel(o[k], ref[k]) for k in ("min_q", "max_q", "Mc_over_Mph", "f_share_30")))
kline("K-G-NONE", worst <= 1e-12, f"LR-x with r_J = inf vs CFG915 cached LC MW runs (min q, max q, M_c/M_ph, f share, t share; alpha_f 0.5, 1; both footings): max rel {worst:.1e}")
kline("K-G-ALL", worst_all <= 1e-12 and worst598 <= 1e-9 and worst_call <= 1e-9,
      f"release-all vs CFG915 REF: exact capture max rel {worst_all:.1e}; vs cfg598_results.json MW P0 {worst598:.1e}; capped capture {worst_call:.1e}")
wh = 0.0
for f in FOOTS:
    for a in ALPHAS_F:
        o = gt("14.0", f, "x", a); ref = C915[f"14.0|{f}|LC|af{akey(a)}|at0|X05|tol1e-12"]
        wh = max(wh, rel(o["phi_f_200"], ref["phi_f_200"]), rel(o["t_frac"], ref["t_frac"]))
kline("K-H14", wh <= 1e-12, f"LR-x log-14 host runs vs CFG915 cache phi_f(<200), t share: max rel {wh:.1e}")
ME, MA = CACHE["M"]["eRASS1"], CACHE["M"]["ACCEPT"]
dz = 0.0; dA = 0.0
for f in FOOTS:
    for samp, key, mine in (("T_R", "s|%s|primary", ME["TR"][f]["hmm"]), ("T_A", "s|%s|primary", MA["TA"][f]["hmm"])):
        ref = R726[samp][key % FL[f]]
        dz = max(dz, abs(mine["Z_outer"] - ref["Z_outer"]), abs(mine["Z_mid"] - ref["Z_mid"]))
        Am = mine["A"]["OUTER"][0]; Ar = ref["A"]["OUTER"][0] if isinstance(ref["A"]["OUTER"], list) else ref["A"]["OUTER"]
        dA = max(dA, rel(Am, Ar))
kline("K-M-NONE", ME["K"]["KMN_maxrel"] <= 1e-10 and MA["K"]["KMN_maxrel"] <= 1e-10 and dz <= 1e-3 and dA <= 1e-6,
      f"release-none per-cluster DeltaSigma vs CFG726 stored arrays: eRASS1 {ME['K']['KMN_maxrel']:.1e}, ACCEPT {MA['K']['KMN_maxrel']:.1e}; "
      f"Z (MID, OUTER) max |diff| {dz:.1e}; A_OUTER max rel {dA:.1e}")
dL = 0.0
for f in FOOTS:
    ref = R726["T_R"][f"s|{FL[f]}|primary"]["A_law"]
    for b in ("MID", "OUTER"):
        dL = max(dL, rel(ME["TR"][f]["law"]["A"][b][0], ref[b][0]))
kline("K-M-ALL", ME["K"]["KMA_maxrel"] <= 1e-10 and MA["K"]["KMA_maxrel"] <= 1e-10 and dL <= 1e-6,
      f"release-all = CFG726 stored law arrays: eRASS1 {ME['K']['KMA_maxrel']:.1e}, ACCEPT {MA['K']['KMA_maxrel']:.1e}; A_law (MID, OUTER) max rel {dL:.1e}")
kline("K-M-W", ME["K"]["KMW_maxrel"] <= 1e-10, f"truncated convolution with weight 1 vs CFG726 convolve_members: max rel {ME['K']['KMW_maxrel']:.1e}")
ko = ME["K"]["KORB"]
kline("K-ORB", ko["rel"] <= 0.01 and ko["all_rp_le_d"],
      f"median eRASS1 cluster (canonical), d {ko['d_kpc']:.0f} kpc, node {ko['node']}: solver r_p {ko['rp_solver']:.2f} kpc vs leapfrog "
      f"{ko['rmin_leapfrog']:.2f} kpc (rel {ko['rel']:.1e}); all nodes r_p <= d: {ko['all_rp_le_d']}")
SAT = CACHE["sat"]
kline("K-SAT", SAT["K_SAT_n"] == 12 and SAT["K_SAT_maxrel"] <= 1e-6, f"CFG839 r_peri reproduced with its own settings for {SAT['K_SAT_n']} satellites: max rel {SAT['K_SAT_maxrel']:.1e}")
R873 = rd("CFG873_field_dwarf_environment/cfg873_results.json"); R874 = rd("CFG874_isolated_dwarfs_pooled/cfg874_results.json")
R875 = rd("CFG875_host_distance_trend/cfg875_results.json")
R838 = rd("CFG838_satellite_tides/cfg838_results.json"); R839 = rd("CFG839_pericentre_tides/cfg839_results.json")
R827 = rd("CFG827_dwarf_age_sfh_ml/cfg827_results.json")
E827 = np.array([v["E_SFH"] for v in R827["rows"].values() if not v["train"]]); LOSS = np.exp(4 * E827)
k = (abs(PHI["can"]["B"] - 0.1346) <= 1e-4 and abs(PHI["alt"]["B"] - 0.1338) <= 1e-4 and abs(PHI["can"]["H"] - 0.0390) <= 1e-4
     and abs(PHI["alt"]["H"] - 0.0411) <= 1e-4
     and abs(R915["hosts"]["LC|14.0|can|0.5"]["phi_f_200"] - 0.864) <= 1e-3 and abs(R915["hosts"]["LC|14.0|alt|0.5"]["phi_f_200"] - 0.882) <= 1e-3)
kz = all(abs(R726[t][f"s|{FL[f]}|primary"]["Z_outer"] - w) <= 0.01 for (t, f), w in
         {("T_R", "can"): -3.63, ("T_R", "alt"): -4.05, ("T_A", "can"): -4.83, ("T_A", "alt"): -5.19}.items())
kl = abs(R726["T_R"]["s|canonical|primary"]["A_law"]["MID"][0] - 1.91) <= 0.01 and abs(R726["T_R"]["s|canonical|primary"]["A_law"]["OUTER"][0] - 1.01) <= 0.01
p873, p874, p875 = R873["canonical"]["primary"], R874["canonical"]["primary"], R875["canonical"]["primary"]
kf = (abs(p873["D"] + 0.150) <= 0.001 and abs(p873["se_D"] - 0.097) <= 0.001 and abs(p874["c"] + 0.100) <= 0.001 and abs(p874["se_c"] - 0.091) <= 0.001
      and abs(p875["k"] + 0.190) <= 0.001 and abs(p875["se_k"] - 0.150) <= 0.001)
kc = R838["cls"] == "NO TIDAL SIGNAL" and R839["cls"] == "NO SIGNAL" and abs(np.median(LOSS) - 4.3) <= 0.05
kline("K-R", bool(k and kz and kl and kf and kc),
      f"CFG915 phi_lin B {PHI['can']['B']:.4f}/{PHI['alt']['B']:.4f} H {PHI['can']['H']:.4f}/{PHI['alt']['H']:.4f}, LC log-14 phi_f "
      f"{R915['hosts']['LC|14.0|can|0.5']['phi_f_200']:.3f}/{R915['hosts']['LC|14.0|alt|0.5']['phi_f_200']:.3f}; CFG726 Z_outer ok {kz}, law A ok {kl}; "
      f"CFG873 D {p873['D']:+.3f}+-{p873['se_D']:.3f}, CFG874 c {p874['c']:+.3f}+-{p874['se_c']:.3f}, CFG875 k {p875['k']:+.3f}+-{p875['se_k']:.3f}; "
      f"CFG838 {R838['cls']}, CFG839 {R839['cls']}; CFG827 loss factor median {np.median(LOSS):.2f}")
KALL = all(v["pass_"] is True for v in K.values())
P(f"K-tests: {sum(1 for v in K.values() if v['pass_'] is True)}/{len(K)} PASS")
CACHE["K"] = K; save_cache()
P()
if MODE == "K":
    P(f"elapsed {time.time() - T0:.0f} s")
    open(os.path.join(HERE, "cfg916_K.out"), "w").write("\n".join(OUT) + "\n")
    sys.exit(0)


# ===================================================================================================== grading (shared by main and MUTATE)
RANK = {"CONSISTENT": 0, "UNDERDETERMINED": 1, "CONTRADICTED": 2}


def worst_cls(cs):
    return max(cs, key=lambda c: RANK[c.split(" ")[0]])


def best_cls(cs):
    return min(cs, key=lambda c: RANK[c.split(" ")[0]])


def grade_G(reading, arm):
    """arm: 'H' (H-LR, r_J,MW), 'all' (r_J 0), 'none' (r_J inf)."""
    cap = "x" if reading == "LR-x" else "c"
    out = {}
    for f in FOOTS:
        rJ = {"H": rjmw[f], "all": 0.0, "none": np.inf}[arm]
        runs = {akey(a): gt("MW", f, cap, a, rJ) for a in ALPHAS_F}
        ok = [a for a in runs if runs[a]["i_holds"] and not runs[a]["walled"]]
        out[f] = dict(cls="CONSISTENT" if ok else "CONTRADICTED", pass_alpha=ok,
                      min_q={a: runs[a]["min_q"] for a in runs}, Mc_over_Mph={a: runs[a]["Mc_over_Mph"] for a in runs},
                      t_frac={a: runs[a]["t_frac"] for a in runs}, rel_max={a: runs[a]["rel_max"] for a in runs},
                      r_cap_kpc={a: runs[a]["r_cap_kpc"] for a in runs}, rJ_kpc=rJ)
    out["joint_pass_alpha"] = [a for a in out["can"]["pass_alpha"] if a in out["alt"]["pass_alpha"]]
    return out


def grade_M(reading, arm):
    """M from the cached CFG726-harness scores.  LR-x: identity with release-none (re-latched in place); LR-c: lrp (peri) / lrn."""
    out = {}
    for f in FOOTS:
        if arm == "all":
            vp = vn = "law"
        elif arm == "none" or reading == "LR-x":
            vp = vn = "hmm"
        else:
            vp, vn = "lrp", "lrn"
        res = {}
        for ep, v in (("peri", vp), ("present", vn)):
            zr = ME["TR"][f][v]; za = MA["TA"][f][v]
            Ar, Aa = zr["A"]["OUTER"][0], za["A"]["OUTER"][0]
            over = [(abs(z["Z_outer"]) >= 2 and A < 1) for z, A in ((zr, Ar), (za, Aa))]
            if any(over):
                cls = "CONTRADICTED"
            elif abs(zr["Z_outer"]) < 2 and abs(za["Z_outer"]) < 2:
                cls = "CONSISTENT (static)"
            else:
                cls = "UNDERDETERMINED"
            res[ep] = dict(cls=cls, variant=v, eRASS1=dict(A_MID=zr["A"]["MID"], A_OUTER=zr["A"]["OUTER"], Z_mid=zr["Z_mid"], Z_outer=zr["Z_outer"]),
                           ACCEPT=dict(A_MID=za["A"]["MID"], A_OUTER=za["A"]["OUTER"], Z_mid=za["Z_mid"], Z_outer=za["Z_outer"]))
        out[f] = dict(cls=res["peri"]["cls"], alt_cls=res["present"]["cls"], **res)
    return out


def grade_B(reading, arm, Gpass):
    cap = "x" if reading == "LR-x" else "c"
    BB = CACHE["misc"]["B"]
    out = {}
    for f in FOOTS:
        use = [a for a in ALPHAS_F if akey(a) in Gpass[f]] or list(ALPHAS_F)
        rows = {}
        for a in ALPHAS_F:
            run = gt("14.0", f, cap, a)
            phi_f, _ = B_phi(run, np.inf)
            rec = dict(phi_f=phi_f)
            for ep, rJ in (("present", fl(BB[f]["rJ_present"])),):
                if arm == "all":
                    phm = phi_f if reading == "LR-x" else 1.0
                elif arm == "none" or reading == "LR-x":
                    phm = phi_f
                else:
                    phm = phi_f + B_phi(run, rJ)[1]
                rec[f"phi_mob_{ep}"] = phm
            # pericentre: no record pericentre distance; class only if a threshold is met at zero release (or by the arm)
            if arm == "all":
                rec["phi_mob_peri_floor"] = phi_f if reading == "LR-x" else 1.0
            else:
                rec["phi_mob_peri_floor"] = phi_f
            # condition d*: largest d (record main/sub model) below which phi_mob >= 0.9 (LR-c, H arm only; report)
            if reading == "LR-c" and arm == "H":
                dg = np.array(BB[f]["dgrid"]); rg = np.array(BB[f]["rJ_grid"])
                ph = np.array([phi_f + B_phi(run, r)[1] for r in rg])
                bad = dg[ph >= 0.9]
                rec["d_star_kpc"] = float(bad.max()) if bad.size else None
                rec["phi_mob_at_dmin_model"] = phi_f + B_phi(run, fl(BB[f]["rJ_dmin"]))[1] if BB[f].get("rJ_dmin") is not None else None
            rows[akey(a)] = rec

        def cls_of(key):
            vals = [rows[akey(a)][key] for a in use]
            if any(v <= PHI[f]["H"] for v in vals):
                return "CONSISTENT (first order)"
            if all(v >= 0.9 for v in vals):
                return "CONTRADICTED"
            return "UNDERDETERMINED"
        c_floor = cls_of("phi_mob_peri_floor")
        cls_peri = "CONTRADICTED" if c_floor == "CONTRADICTED" else "UNDERDETERMINED"
        if arm == "all" and reading == "LR-c":
            cls_peri = "CONTRADICTED"
        out[f] = dict(cls=cls_peri, alt_cls=cls_of("phi_mob_present"), alphas_used=[akey(a) for a in use], rows=rows,
                      rJ_present_kpc=fl(BB[f]["rJ_present"]), dmin_model_kpc=BB[f].get("dmin_model_kpc"),
                      rJ_dmin_kpc=None if BB[f].get("rJ_dmin") is None else fl(BB[f]["rJ_dmin"]))
    return out


def grade_D(reading, arm, Gres):
    rows = SAT["rows"]
    out = {}
    for f in FOOTS:
        res = {}
        for ep in ("peri", "present"):
            names = [n for n, r in rows.items() if (f"rJ_peri_{f}" in r if ep == "peri" else True)]
            exposed = {}
            for n in names:
                r = rows[n]
                rJ = r[f"rJ_peri_{f}"] if ep == "peri" else r[f"rJ_present_{f}"]
                if arm == "all":
                    if reading == "LR-c":
                        exposed[n] = True
                    else:                                                  # LR-x: re-latched only inside the MW's settled radius
                        if r["host"] != "mw":
                            exposed[n] = None                              # no M31 drift model: not evaluable
                        else:
                            rcap = max(gt("MW", f, "x", a, rjmw[f])["r_cap_kpc"] for a in ALPHAS_F)   # the LR-x MW run; most favourable alpha_f
                            exposed[n] = bool(r["D_kpc"] > rcap)
                else:
                    exposed[n] = bool(fl(rJ) < r["r12_kpc"])
            intact = [rows[n][f"delta_{f}"] for n in names if exposed[n] is False]
            ref = float(np.median(intact)) if len(intact) >= 3 else 0.0
            above = [n for n in names if exposed[n] and rows[n][f"delta_{f}"] > ref]
            cls = "CONSISTENT" if not above else ("UNDERDETERMINED" if len(above) == 1 else "CONTRADICTED")
            res[ep] = dict(cls=cls, N=len(names), exposed=[n for n in names if exposed[n]], above_ref=above, ref_delta=ref,
                           not_evaluable=[n for n in names if exposed[n] is None],
                           rJ_over_r12={n: (fl(rows[n][f"rJ_peri_{f}"] if ep == "peri" else rows[n][f"rJ_present_{f}"]) / rows[n]["r12_kpc"]) for n in names})
        # field
        tests = {"CFG873 D": (R873[FL[f]]["primary"]["D"], R873[FL[f]]["primary"]["se_D"]),
                 "CFG874 c": (R874[FL[f]]["primary"]["c"], R874[FL[f]]["primary"]["se_c"]),
                 "CFG875 k": (R875[FL[f]]["primary"]["k"], R875[FL[f]]["primary"]["se_k"])}
        zs = {k_: v[0] / v[1] for k_, v in tests.items()}
        fcls = "CONTRADICTED" if any(z <= -2 for z in zs.values()) else "CONSISTENT"
        dsat = res["peri"]["cls"]
        dcls = "CONTRADICTED" if "CONTRADICTED" in (dsat, fcls) else ("CONSISTENT" if dsat == fcls == "CONSISTENT" else "UNDERDETERMINED")
        dalt = res["present"]["cls"]
        dcls_alt = "CONTRADICTED" if "CONTRADICTED" in (dalt, fcls) else ("CONSISTENT" if dalt == fcls == "CONSISTENT" else "UNDERDETERMINED")
        out[f] = dict(cls=dcls + (" (conditional)" if dcls == "CONSISTENT" else ""), alt_cls=dcls_alt + (" (conditional)" if dcls_alt == "CONSISTENT" else ""),
                      sat=res, field=dict(cls=fcls, values={k_: list(v) for k_, v in tests.items()}, z=zs))
    return out


def grade_reading(reading, arm="H"):
    G = grade_G(reading, arm)
    Gpass = {f: G[f]["pass_alpha"] for f in FOOTS}
    M = grade_M(reading, arm)
    B = grade_B(reading, arm, Gpass)
    D = grade_D(reading, arm, G)
    per = {}
    for f in FOOTS:
        per[f] = {t: X[f]["cls"] for t, X in (("G", G), ("M", M), ("B", B), ("D", D))}
    allc = [c for f in FOOTS for c in per[f].values()]
    lab = worst_cls(allc).split(" ")[0]
    lab = {"CONSISTENT": "CONSISTENT WITH ALL FOUR"}.get(lab, lab)
    why = [f"{t}[{f}] {per[f][t]}" for f in FOOTS for t in per[f] if per[f][t].startswith(("CONTRADICTED", "UNDERDETERMINED"))]
    return dict(G=G, M=M, B=B, D=D, per_footing=per, label=lab, why=why)


def show(reading, R):
    P(f"--- {reading} ---")
    for f in FOOTS:
        g = R["G"][f]
        P(f"  G [{f}] {g['cls']}: min q " + ", ".join(f"af {a} {g['min_q'][a]:.4f}" for a in g["min_q"]) + "; M_c/M_ph(<30) "
          + ", ".join(f"{g['Mc_over_Mph'][a]:.4f}" for a in g["Mc_over_Mph"]) + f"; t share " + ", ".join(f"{g['t_frac'][a]:.4f}" for a in g["t_frac"])
          + f"; r_J,MW {g['rJ_kpc'] if isinstance(g['rJ_kpc'], str) else round(g['rJ_kpc'], 1)} kpc; max t found beyond r_J at a release "
          + ", ".join(f"{g['rel_max'][a]:.3g}" for a in g["rel_max"]) + " Msun")
    P(f"  G joint pass alpha_f (both footings): {R['G']['joint_pass_alpha']}")
    for f in FOOTS:
        m = R["M"][f]
        for ep in ("peri", "present"):
            e, a = m[ep]["eRASS1"], m[ep]["ACCEPT"]
            P(f"  M [{f}] {ep:7s} ({m[ep]['variant']}): eRASS1 OUTER {e['A_OUTER'][0]:.3f}+-{e['A_OUTER'][1]:.3f} (Z {e['Z_outer']:+.2f}), "
              f"MID {e['A_MID'][0]:.3f}+-{e['A_MID'][1]:.3f} (Z {e['Z_mid']:+.2f}); ACCEPT OUTER {a['A_OUTER'][0]:.3f}+-{a['A_OUTER'][1]:.3f} "
              f"(Z {a['Z_outer']:+.2f}), MID {a['A_MID'][0]:.3f} (Z {a['Z_mid']:+.2f}) -> {m[ep]['cls']}")
    for f in FOOTS:
        b = R["B"][f]
        P(f"  B [{f}] peri {b['cls']} | present {b['alt_cls']}: r_J(720 kpc) {b['rJ_present_kpc']:.0f} kpc; record head-on d_min "
          f"{b['dmin_model_kpc']} kpc (r_J {b['rJ_dmin_kpc'] if b['rJ_dmin_kpc'] is None else round(b['rJ_dmin_kpc'], 1)} kpc, report only); "
          + "; ".join(f"af {a}: phi_f {r_['phi_f']:.4f}, phi_mob present {r_['phi_mob_present']:.4f}"
                      + (f", d* {r_['d_star_kpc']} kpc, phi_mob(d_min) {r_['phi_mob_at_dmin_model']:.4f}" if "d_star_kpc" in r_ and r_.get("phi_mob_at_dmin_model") is not None else "")
                      for a, r_ in b["rows"].items()) + f" (alphas used {b['alphas_used']}; phi_lin,H {PHI[f]['H']:.4f})")
    for f in FOOTS:
        d_ = R["D"][f]
        for ep in ("peri", "present"):
            s_ = d_["sat"][ep]
            P(f"  D-sat [{f}] {ep:7s} N {s_['N']}: exposed {s_['exposed']} (ref Delta {s_['ref_delta']:+.3f}; above ref {s_['above_ref']}"
              + (f"; not evaluable {s_['not_evaluable']}" if s_["not_evaluable"] else "") + f") -> {s_['cls']}; min r_J/r_1/2 "
              + f"{min(s_['rJ_over_r12'].values()):.2f} ({min(s_['rJ_over_r12'], key=s_['rJ_over_r12'].get)})")
        P(f"  D-field [{f}]: " + ", ".join(f"{k_} {v[0]:+.3f}+-{v[1]:.3f} (z {d_['field']['z'][k_]:+.2f})" for k_, v in d_["field"]["values"].items())
          + f" -> {d_['field']['cls']};  D [{f}] = {d_['cls']} | present {d_['alt_cls']}")
    P(f"  CLASS {reading}: {R['label']}" + "".join(f"\n     - {w}" for w in R["why"]))


# ===================================================================================================== main / MUTATE
RES = dict(lane="CFG916", criteria="a3b2ffd2d", label="HYPOTHESIS TEST", mutate=MUT, K=K,
           settings=dict(kappa="1/2 FITTED", footings=A0SI, alpha_f=ALPHAS_F, alpha_t=0.0, R_core_kpc=R_CORE, kernel_rJ="nu_s"),
           G_rJ=rjmw)
if not MUT:
    P("Inputs and summaries")
    P(f"  r_J,MW in M31's field: {rjmw['can']:.0f} / {rjmw['alt']:.0f} kpc at d = {rjmw['d_kpc']:.0f} kpc; MW drift grid outer cell centre "
      f"{gt('MW', 'can', 'x', 0.5)['rc_last']:.0f} kpc")
    for f in FOOTS:
        s_ = ME["summary"][f]
        P(f"  eRASS1 [{f}] members: N_mem median {s_['N_med']:.0f}, own halo edge median {s_['edge_med_kpc']:.0f} kpc; r_J median at pericentre "
          f"{s_['rJp_med_kpc']:.1f} kpc (r_p/d median {s_['rp_over_d_med']:.2f}), at present {s_['rJn_med_kpc']:.1f} kpc; retained free memory F_J/F "
          f"peri {s_['Fp_over_F_med']:.3f}, present {s_['Fn_over_F_med']:.3f}; released-surplus clock 1/Gamma at 1.5 Mpc "
          + ", ".join(f"alpha_f {a}: {v:.2f} Gyr" for a, v in s_["Gamma_inv_Gyr"].items()) + " (report only)")
    EF = CACHE["M"].get("eFEDS")
    if isinstance(EF, dict):
        P("  eFEDS (report only; CFG726 T-E fails at the law's level): " + "; ".join(
            f"{v}|{f} chi2 {EF['TE'][f'{v}|{f}']['chi2']:.1f} p {EF['TE'][f'{v}|{f}']['p']:.2g} A_out {EF['TE'][f'{v}|{f}']['A_out']:+.3f}+-{EF['TE'][f'{v}|{f}']['sA']:.3f}"
            for f in FOOTS for v in ("base", "hmm", "lrp", "lrn")) + f"; reproduction of CFG726 stored arrays: hmm {EF['K_rep_hmm_maxrel']:.1e}, law {EF['K_rep_base_maxrel']:.1e}")
    P()
    CL = {}
    for reading in ("LR-x", "LR-c"):
        CL[reading] = grade_reading(reading, "H")
        show(reading, CL[reading])
        P()
    rank2 = {"CONSISTENT WITH ALL FOUR": 0, "UNDERDETERMINED": 1, "CONTRADICTED": 2}
    overall = min((CL[r]["label"] for r in CL), key=lambda x: rank2[x])
    P(f"OVERALL H-LR (best over LR-x, LR-c; two chances, disclosed): {overall}")
    P("Conditions carried (D): alpha_t = 0; D-i formation-epoch baryon loss, loss factor median "
      f"x{np.median(LOSS):.2f} (16-84% {np.percentile(LOSS, 16):.2f}-{np.percentile(LOSS, 84):.2f}, CFG827 28 OOS dwarfs); LR-c adds: t latched "
      "(exact settling, growth halted) before the loss.")
    RES.update(readings=CL, overall=overall, summaries=dict(eRASS1=ME["summary"], ACCEPT=MA["summary"], eFEDS=CACHE["M"].get("eFEDS")),
               D_conditions=dict(loss_median=float(np.median(LOSS)), loss_p16=float(np.percentile(LOSS, 16)), loss_p84=float(np.percentile(LOSS, 84))))
    # ------------------------------------------------------------------------------------------- POST HOC (2026-10-20; no class weight)
    P()
    P("POST HOC diagnostics (added after the first full main run; no class weight; frozen numbers above unchanged):")
    PH = {}
    # PH1: how much of the released surplus may still sit in place at t_obs before the static LR-c M pass breaks.
    # 1/A is linear in the model DeltaSigma, so a residual fraction f of the released memory gives 1/A(f) = 1/A_law + f (1/A_hmm - 1/A_law);
    # sigma(f) = A(f) x (sigma/A of the law). Threshold A(f) = 1 - 2 sigma(f).  Then dt_min = -ln(f_max) / Gamma (median 1/Gamma at 1.5 Mpc).
    ph1 = {}
    for f in FOOTS:
        for samp, src in (("eRASS1", ME["TR"][f]), ("ACCEPT", MA["TA"][f])):
            Al, sl = src["law"]["A"]["OUTER"][0], src["law"]["A"]["OUTER"][1]; Ah = src["hmm"]["A"]["OUTER"][0]
            Athr = 1.0 / (1.0 + 2.0 * sl / Al)
            fmax = (1.0 / Athr - 1.0 / Al) / (1.0 / Ah - 1.0 / Al)
            ph1[f"{samp}|{f}"] = dict(A_thr=Athr, f_max=fmax,
                                      dt_min_Gyr={str(a): float(-math.log(min(max(fmax, 1e-12), 1.0)) * ME["summary"][f]["Gamma_inv_Gyr"][str(a)]) for a in ALPHAS_F})
            P(f"  PH1 {samp} [{f}]: static pass survives while <= {fmax:.2f} of the released surplus remains in place at t_obs (A_OUTER >= {Athr:.3f}); "
              f"with the median transport clock that needs a time since release >= "
              + ", ".join(f"{v:.1f} Gyr (alpha_f {a})" for a, v in ph1[f'{samp}|{f}']['dt_min_Gyr'].items()) + "  [linear estimate; heavy run (a) decides]")
    PH["PH1_residual_tolerance"] = ph1
    # PH2: margin of the closest intact satellite
    ph2 = {}
    for f in FOOTS:
        for ep in ("peri", "present"):
            s_ = CL["LR-c"]["D"][f]["sat"][ep]
            intact = {n: v for n, v in s_["rJ_over_r12"].items() if n not in s_["exposed"]}
            nmin = min(intact, key=intact.get)
            ph2[f"{f}|{ep}"] = dict(name=nmin, rJ_over_r12=intact[nmin])
            P(f"  PH2 D-sat [{f}] {ep}: closest intact satellite {nmin} r_J/r_1/2 = {intact[nmin]:.2f}; exposed: {s_['exposed']}")
    PH["PH2_intact_margin"] = ph2
    # PH3 / PH4: notes
    P("  PH3 frozen-text inconsistency (MUTATE): section 6 grades release-all M as the plain law for BOTH readings; under LR-x's own identity argument")
    P("      (exact capture re-latches released surplus in a settled host) release-all M would be H-MM instead. The LR-x release-all tooth bites")
    P("      on D (class change) and G (min q move) without the M entry, so the MUTATE status does not depend on it.")
    BB = CACHE["misc"]["B"]
    P(f"  PH4 B under the record's head-on geometry (report only by the frozen rule): LR-c phi_mob at the model's minimum sampled separation "
      + "; ".join(f"[{f}] d_min {BB[f]['dmin_model_kpc']:.1f} kpc -> " + ", ".join(f"af {a} {CL['LR-c']['B'][f]['rows'][a]['phi_mob_at_dmin_model']:.3f}" for a in CL['LR-c']['B'][f]['rows'])
                  + f" (d* {CL['LR-c']['B'][f]['rows']['0.5']['d_star_kpc']:.1f} kpc)" for f in FOOTS) + "; threshold 0.9")
    RES["post_hoc"] = PH
else:
    MAIN = json.load(open(os.path.join(HERE, "cfg916_results.json"))) if os.path.exists(os.path.join(HERE, "cfg916_results.json")) else None
    P("MUTATE: release-all (r_J -> 0) and release-none (r_J -> inf = CFG915 LC), both readings")
    TOOTH = {}
    base = {r_: grade_reading(r_, "H") for r_ in ("LR-x", "LR-c")}
    for reading in ("LR-x", "LR-c"):
        for arm in ("all", "none"):
            R = grade_reading(reading, arm)
            show(f"{reading} / release-{arm}", R)
            B0 = base[reading]
            changed = [f"{t}[{f}] {B0['per_footing'][f][t]} -> {R['per_footing'][f][t]}" for f in FOOTS for t in R["per_footing"][f]
                       if R["per_footing"][f][t].split(" ")[0] != B0["per_footing"][f][t].split(" ")[0]]
            moves = []
            for f in FOOTS:
                for samp in ("eRASS1", "ACCEPT"):
                    dzv = abs(R["M"][f]["peri"][samp]["Z_outer"] - B0["M"][f]["peri"][samp]["Z_outer"])
                    if dzv >= 1.0:
                        moves.append(f"M[{f}] {samp} |dZ_OUTER| {dzv:.2f}")
                for a in R["B"][f]["rows"]:
                    dp = abs(R["B"][f]["rows"][a]["phi_mob_present"] - B0["B"][f]["rows"][a]["phi_mob_present"])
                    dpf = abs(R["B"][f]["rows"][a]["phi_mob_peri_floor"] - B0["B"][f]["rows"][a]["phi_mob_peri_floor"])
                    if max(dp, dpf) >= 0.05:
                        moves.append(f"B[{f}] af {a} |dphi_mob| {max(dp, dpf):.3f}")
                for a in R["G"][f]["min_q"]:
                    dq = abs(R["G"][f]["min_q"][a] - B0["G"][f]["min_q"][a])
                    if dq >= 1e-3:
                        moves.append(f"G[{f}] af {a} |dmin q| {dq:.4f}")
            bites = bool(changed or moves)
            required = not (reading == "LR-x" and arm == "none")
            TOOTH[f"{reading}|{arm}"] = dict(changed=changed, moves=moves, bites=bites, required=required, label=R["label"])
            P(f"  TOOTH {reading} / release-{arm}: {'BITES' if bites else 'does not bite'} ({'required' if required else 'not required: expected identity'}); "
              f"class changes {changed}; score moves {moves}")
            P()
            RES[f"{reading}|{arm}"] = R
    allreq = all(v["bites"] for v in TOOTH.values() if v["required"])
    RES["tooth"] = TOOTH; RES["bites"] = allreq
    P(f"MUTATE: {'every required arm BITES' if allreq else 'NOT every required arm bites'}; LR-x release-none "
      f"{'bites' if TOOTH['LR-x|none']['bites'] else 'does not bite (identity: the release rule is inert under exact capture)'}")

P(f"K-tests: {'all PASS' if KALL else 'SOME FAIL'} ({sum(1 for v in K.values() if v['pass_'] is True)}/{len(K)})")
P(f"elapsed {time.time() - T0:.0f} s")
SUF = "_MUTATE" if MUT else ""
json.dump(jclean(RES), open(os.path.join(HERE, f"cfg916_results{SUF}.json"), "w"), indent=1)
open(os.path.join(HERE, f"cfg916{SUF}.out"), "w").write("\n".join(OUT) + "\n")
sys.exit(1 if (MUT and RES.get("bites")) else 0)
