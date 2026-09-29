#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CFG158 -- independent referee re-derivation of CFG118's (door 6) headline: cumulative cold mass of spherical secondary infall
onto a static baryon core, relative to the CFG44 target, and the radial scale of the infall.
Frozen criteria: CFG158_FROZEN_CRITERIA.md.  Kernel: cfg158_shells.jl (Julia).  Main: `python3 cfg158_referee.py`;
control: `MUTATE=1 python3 cfg158_referee.py` (reuses cached main products; runs M1-M4).  CFG158_NPROC = number of Julia workers.
Units: kpc, km/s, Msun; time unit kpc/(km/s).  kappa = 1/2 and Omega_c h^2 are FITTED; nothing here says the data favour a model.
"""
import os, sys, json, math, time, hashlib, subprocess
import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq
from scipy.special import gammainc

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
os.chdir(HERE)
MUTATE = os.environ.get("MUTATE", "0") == "1"
NPROC = int(os.environ.get("CFG158_NPROC", "8"))
TAG = "_MUTATE" if MUTATE else ""
SIMS = "cfg158_sims"
os.makedirs(SIMS, exist_ok=True)


class Tee:
    def __init__(self, path):
        self.f = open(path, "w"); self.o = sys.stdout
    def write(self, s):
        self.o.write(s); self.f.write(s); self.f.flush()
    def flush(self):
        self.o.flush(); self.f.flush()


sys.stdout = Tee("cfg158_referee%s.out" % TAG)

G = 4.30091727e-6
KPC_M = 3.0856775814913673e19
A0C = 9.3603e-11 * KPC_M / 1e6           # canonical, (km/s)^2/kpc
A0A = 1.13e-10 * KPC_M / 1e6             # alt footing
H0 = 0.0674                              # km/s/kpc
MYR = 977.79222                          # Myr per (kpc/(km/s))
RHOC0 = 3 * H0 ** 2 / (8 * np.pi * G)
ZI = 100.0
AI = 1 / (1 + ZI)
MASSES = [1e9, 1e10, 1e11, 1e12]
HEXP = {1e9: 2.0, 1e10: 3.0, 1e11: 4.0, 1e12: 5.0}
QS = [0.05, 0.1, 0.2]
COSMO = dict(Om=0.315, OL=0.685, Oc=0.2655, Ob=0.315 - 0.2655)
EDS = dict(Om=1.0, OL=0.0, Oc=1.0, Ob=0.0)
NOSMOOTH = dict(Om=0.315, OL=0.685, Oc=0.315, Ob=0.0)


def age(cs, a):
    if cs["OL"] > 0:
        return 2 / (3 * math.sqrt(cs["OL"]) * H0) * math.asinh(math.sqrt(cs["OL"] / cs["Om"]) * a ** 1.5)
    return 2 / (3 * H0) * a ** 1.5


def a_of_t(cs, t):
    if cs["OL"] > 0:
        return (cs["Om"] / cs["OL"]) ** (1 / 3) * math.sinh(1.5 * math.sqrt(cs["OL"]) * H0 * t) ** (2 / 3)
    return (1.5 * H0 * t) ** (2 / 3)


def rM(Mb, a0):
    return math.sqrt(G * Mb / a0)


def core_of(geom, Mb):
    if geom == "point":
        return dict(geom="point", Mb=Mb, eps=1e-3 * rM(Mb, A0C), h=1.0)
    return dict(geom="exp", Mb=Mb, eps=0.0, h=HEXP[Mb])


def core_acc(core, r):
    if core["Mb"] == 0:
        return 0.0
    if core["geom"] == "point":
        return G * core["Mb"] * r / (r * r + core["eps"] ** 2) ** 1.5
    return G * core["Mb"] * gammainc(3, r / core["h"]) / (r * r)


def core_mass(core, r):
    r = np.asarray(r, float)
    if core["Mb"] == 0:
        return 0.0 * r
    if core["geom"] == "point":
        return core["Mb"] * r ** 3 / (r * r + core["eps"] ** 2) ** 1.5
    return core["Mb"] * gammainc(3, r / core["h"])


# ------------------------------------------------------------------ single-shell (uncrossed) dynamics: set-up quantities
def shell_solve(M, core, cs, t_end, stop_turn=True):
    r0 = AI * (3 * M / (4 * np.pi * cs["Oc"] * RHOC0)) ** (1 / 3)
    ti = age(cs, AI)
    v0 = H0 * math.sqrt(cs["Om"] / AI ** 3 + cs["OL"]) * r0

    def rhs(t, y):
        r, v = y
        a3 = (1.0 / (1.5 * H0 * t) ** 2) if cs["OL"] == 0 else (cs["OL"] / cs["Om"]) / math.sinh(1.5 * math.sqrt(cs["OL"]) * H0 * t) ** 2
        acc = -core_acc(core, r) - G * M / (r * r) - 0.5 * H0 ** 2 * cs["Ob"] * a3 * r + cs["OL"] * H0 ** 2 * r
        return [v, acc]

    ev = lambda t, y: y[1]
    ev.terminal = stop_turn
    ev.direction = -1
    sol = solve_ivp(rhs, (ti, t_end), [r0, v0], method="DOP853", rtol=1e-11, atol=1e-13, events=ev)
    return sol


def turned(M, core, cs, t0):
    sol = shell_solve(M, core, cs, t0, True)
    return len(sol.t_events[0]) > 0


def setup(core, cs, kext=3.0):
    """M_ta (z=0 turnaround mass), r_ta, and M_out (outermost shell: single-shell z=0 radius = kext r_ta)."""
    t0 = age(cs, 1.0)
    Mb = core["Mb"]
    if Mb == 0:
        return None
    lo, hi = 3 * Mb, 500 * Mb
    if not turned(lo, core, cs, t0) or turned(hi, core, cs, t0):
        return None
    for _ in range(46):
        mid = math.sqrt(lo * hi)
        if turned(mid, core, cs, t0):
            lo = mid
        else:
            hi = mid
    Mta = math.sqrt(lo * hi)
    sol = shell_solve(Mta, core, cs, t0, False)
    rta = sol.y[0, -1]

    def rz(M):
        return shell_solve(M, core, cs, t0, False).y[0, -1] - kext * rta
    Mout = brentq(rz, Mta * 1.0001, 6000 * Mb, xtol=1e-9 * Mb, rtol=1e-10)
    return dict(Mta=Mta, rta=rta, Mout=Mout, t0=t0, vta=sol.y[1, -1])


# ------------------------------------------------------------------ CFG44 target
_target_cache = {}


def target_Mc_func(core, a0):
    """Return a callable r -> M_c,target(<r) (target: rho_c r^3 g_tot = (a0/4pi) M_b(<r), closure w' = a0 r u_N/u)."""
    key = (core["geom"], core["Mb"], core["h"], a0)
    if key in _target_cache:
        return _target_cache[key]
    Mb = core["Mb"]
    if core["geom"] == "point":
        rm = rM(Mb, a0)
        f = lambda r: Mb * (np.sqrt(1 + (np.asarray(r, float) / rm) ** 2) - 1)
    else:
        h = core["h"]
        r0 = 1e-6 * h

        def rhs(lnr, y):
            r = math.exp(lnr)
            uN = G * Mb * gammainc(3, r / h)
            u = uN + y[0]
            return [a0 * r * r * uN / u if u > 0 else 0.0]
        uN0 = G * Mb * gammainc(3, r0 / h)
        w0 = math.sqrt(0.4 * a0 * G * Mb / (6 * h ** 3) * r0 ** 5)
        sol = solve_ivp(rhs, (math.log(r0), math.log(2e4)), [w0], method="DOP853", rtol=1e-12, atol=1e-30, dense_output=True)
        f = lambda r: sol.sol(np.log(np.asarray(r, float)))[0] / G
    _target_cache[key] = f
    return f


# ------------------------------------------------------------------ run management
def spec_line(d):
    return " ".join("%s=%s" % (k, d[k]) for k in sorted(d) if k != "name")


def cached(d):
    p = os.path.join(SIMS, d["name"])
    sp = p + ".spec"
    if d.get("mode", "sim") == "orbit":
        ok = os.path.exists(p + ".orbit.txt")
    else:
        ok = os.path.exists(p + ".meta.txt")
    return ok and os.path.exists(sp) and open(sp).read().strip() == spec_line(d)


def run_specs(specs):
    todo = [d for d in specs if not cached(d)]
    print("  runs requested: %d, cached: %d, to run: %d" % (len(specs), len(specs) - len(todo), len(todo)))
    if not todo:
        return
    cost = lambda d: (0.15 if d.get("mode") == "orbit" else float(d["N"]) * (1.0 if d.get("geom") == "point" else 0.8))
    todo.sort(key=cost, reverse=True)
    queues = [[] for _ in range(NPROC)]
    load = [0.0] * NPROC
    for d in todo:
        k = int(np.argmin(load)); queues[k].append(d); load[k] += cost(d)
    procs = []
    t0 = time.time()
    for k, qd in enumerate(queues):
        if not qd:
            continue
        tf = os.path.join(SIMS, "tasks_%d.txt" % k)
        with open(tf, "w") as f:
            for d in qd:
                dd = dict(d); dd["out"] = os.path.join(SIMS, d["name"])
                f.write(spec_line(dd).replace("name=%s" % d["name"], "") + "\n")
        lf = open(os.path.join(SIMS, "log_%d.txt" % k), "w")
        env = dict(os.environ); env["JULIA_NUM_THREADS"] = "1"
        procs.append((subprocess.Popen(["julia", "-O3", "--startup-file=no", "cfg158_shells.jl", tf], stdout=lf, stderr=lf, env=env), qd, lf))
    for pr, qd, lf in procs:
        pr.wait(); lf.close()
    for pr, qd, lf in procs:
        for d in qd:
            ok = os.path.exists(os.path.join(SIMS, d["name"] + (".orbit.txt" if d.get("mode") == "orbit" else ".meta.txt")))
            if ok:
                open(os.path.join(SIMS, d["name"] + ".spec"), "w").write(spec_line(d))
            else:
                print("  !! run failed: %s (see %s/log_*.txt)" % (d["name"], SIMS))
    print("  julia workers finished in %.1f min wall" % ((time.time() - t0) / 60))


def load_run(name):
    p = os.path.join(SIMS, name)
    meta = {}
    for ln in open(p + ".meta.txt"):
        k, v = ln.split(); meta[k] = float(v)
    N = int(meta["N"]); ng = int(meta["ng"]); ns = int(meta["nsamp"])
    fin = np.fromfile(p + ".final.bin").reshape(6, N)
    return dict(meta=meta, N=N, R=fin[0], V=fin[1], J2=fin[2], TU=fin[3], RTA=fin[4], RP=fin[5],
                t=np.fromfile(p + ".times.bin"), S=np.fromfile(p + ".samples.bin").reshape(ns, ng), rg=np.fromfile(p + ".rgrid.bin"))


def make_spec(name, cr, cs, Mout, N, q, **kw):
    d = dict(name=name, mode="sim", geom=cr["geom"], Mb=repr(float(cr["Mb"])), h=cr["h"], eps=repr(cr["eps"] if cr["eps"] > 0 else 1e-3),
             q=q, N=N, Mout=repr(float(Mout)), Om=cs["Om"], OL=cs["OL"], Oc=cs["Oc"], Ob=cs["Ob"], dt_myr=1.0, rtol=1e-10,
             rlo=repr(0.05 * rM(cr["Mb"], A0C) if cr["Mb"] > 0 else 0.05 * rM(1e10, A0C)),
             rhi=repr(80 * rM(cr["Mb"], A0C) if cr["Mb"] > 0 else 80 * rM(1e10, A0C)), ng=155)
    d.update(kw)
    return d


# ------------------------------------------------------------------ analysis of a run
def avg_curve(run, core, t0):
    """Window-averaged cumulative cold mass on the radial grid; window = local dynamical time (B&T), capped at 0.9 t0."""
    rg, t, S = run["rg"], run["t"], run["S"]
    snap = S[-1]
    Menc = core_mass(core, rg) + snap
    rho = Menc / (4 * np.pi / 3 * rg ** 3)
    tdyn = np.sqrt(3 * np.pi / (16 * G * rho))
    w = np.minimum(tdyn, 0.9 * t0)
    out = np.empty_like(snap)
    for j in range(len(rg)):
        sel = t >= t[-1] - w[j] - 1e-12
        out[j] = S[sel, j].mean()
    return out, snap


def interp_lnr(rg, y, r):
    return np.interp(np.log(r), np.log(rg), y)


def R_at(run, core, t0, x, a0):
    av, snap = avg_curve(run, core, t0)
    r = x * rM(core["Mb"], a0)
    tf = target_Mc_func(core, a0)
    return interp_lnr(run["rg"], av, r) / float(tf(r)), interp_lnr(run["rg"], snap, r) / float(tf(r))


def local_C(Mfunc, core, r_edges):
    Me = Mfunc(r_edges)
    dM = np.diff(Me)
    vol = 4 * np.pi / 3 * (r_edges[1:] ** 3 - r_edges[:-1] ** 3)
    rho = dM / vol
    rc = np.sqrt(r_edges[1:] * r_edges[:-1])
    Mc_c = np.interp(np.log(rc), np.log(r_edges), Me)
    g = G * (core_mass(core, rc) + Mc_c) / rc ** 2
    return rho * rc ** 3 * g, rc


def ratio_curve(run, core, t0, a0):
    av, snap = avg_curve(run, core, t0)
    rm = rM(core["Mb"], a0)
    xe = 10 ** (-1 + 0.1 * np.arange(26))
    re = xe * rm
    fsim = lambda r: interp_lnr(run["rg"], av, np.asarray(r))
    ftar = target_Mc_func(core, a0)
    Cs, rc = local_C(fsim, core, re)
    Ct, _ = local_C(lambda r: np.asarray(ftar(r)), core, re)
    return Cs / Ct, rc / rm


def r1_of(run, core, t0):
    av, _ = avg_curve(run, core, t0)
    rg = run["rg"]
    above = np.where(av >= core["Mb"])[0]
    if len(above) == 0 or above[0] == 0:
        return float("nan")
    j = above[0]
    lr = np.interp(core["Mb"], av[j - 1:j + 1], np.log(rg[j - 1:j + 1]))
    return math.exp(lr)


def measured_ta(run):
    tu = run["TU"]
    idx = np.where(tu == 0)[0]
    if len(idx) == 0:
        return None
    i = idx[0]
    if i == 0:
        return None
    v0, v1 = run["V"][i - 1], run["V"][i]
    if not (v0 <= 0 < v1):
        return dict(flag="no-sign-change", v0=v0, v1=v1)
    f = v0 / (v0 - v1)
    return dict(flag="ok", r=run["R"][i - 1] * (1 - f) + run["R"][i] * f, i=i)


def fmt(x, n=3):
    return ("%%.%dg" % n) % x


# ------------------------------------------------------------------ main
def main():
    T0 = time.time()
    results = {"mode": "MUTATE" if MUTATE else "main"}
    checks = {}
    print("CFG158 referee (%s): independent re-derivation of CFG118's infall headline" % ("MUTATE" if MUTATE else "main"))
    print("Frozen criteria: CFG158_FROZEN_CRITERIA.md (commit 240bcd976). Shells: Julia kernel, DP5(4) test bodies in a rebuilt enclosed-mass profile.")
    print("=" * 110)

    # ---- set-up (single-shell, scipy)
    print("\n[set-up] z=0 turnaround mass, radius, and shell extent (single-shell ODE, scipy DOP853)")
    setups = {}
    for geom in ("point", "exp"):
        for M in MASSES:
            core = core_of(geom, M)
            s = setup(core, COSMO)
            setups[(geom, M)] = s
            print("  %-5s M_b=%.0e  M_ta/M_b=%.3f  r_ta=%.1f kpc  r_M=%.3f kpc  x_ta=%.1f  M_out/M_b=%.2f" % (
                geom, M, s["Mta"] / M, s["rta"], rM(M, A0C), s["rta"] / rM(M, A0C), s["Mout"] / M))
    results["setup"] = {"%s_%.0e" % k: v for k, v in setups.items()}

    # ---- run specs
    main_specs = []
    for geom in ("point", "exp"):
        for M in MASSES:
            core = core_of(geom, M)
            for q in QS:
                for N in (20000, 5000):
                    main_specs.append(make_spec("%s_%.0e_q%.2f_N%d" % (geom, M, q, N), core, COSMO, setups[(geom, M)]["Mout"], N, q))
    core10 = core_of("point", 1e10)
    s10 = setups[("point", 1e10)]
    nocore = dict(core10); nocore["Mb"] = 0.0
    extra = []
    extra.append(make_spec("c1_nocore_N20000", core10, COSMO, s10["Mout"], 20000, 0.1, core=0.0))
    seed = core_of("point", 1e10)
    sE = setup(seed, EDS)
    results["setup_eds"] = sE
    print("  EdS control (point seed 1e10, Om=1, no smooth background): M_ta/M_seed=%.3f, r_ta(a=1)=%.1f kpc, M_out/M_seed=%.2f" % (sE["Mta"] / 1e10, sE["rta"], sE["Mout"] / 1e10))
    extra.append(make_spec("c2_eds_N20000", seed, EDS, sE["Mout"], 20000, 0.05))
    extra.append(make_spec("c4_dt05_rtol11_N5000", core10, COSMO, s10["Mout"], 5000, 0.1, dt_myr=0.5, rtol=1e-11))
    sx = setup(core10, COSMO, kext=6.0)
    extra.append(make_spec("r3_ext6_N5000", core10, COSMO, sx["Mout"], 5000, 0.1))
    extra.append(make_spec("r3_jpoint_N5000", core10, COSMO, s10["Mout"], 5000, 0.1, jform=1))
    for q in QS:
        extra.append(dict(name="c6_orbit_q%.2f" % q, mode="orbit", Mb="1e10", eps=repr(1e-3 * rM(1e10, A0C)), rta=0.7, q=q, norb=2000, rtol=1e-10))
    mut_specs = []
    if MUTATE:
        mut_specs.append(make_spec("m1_nocore_N5000", core10, COSMO, s10["Mout"], 5000, 0.1, core=0.0))
        mut_specs.append(make_spec("m2_q0.002_N5000", core10, COSMO, s10["Mout"], 5000, 0.002))
        sM3 = setup(core10, NOSMOOTH)
        results["setup_m3"] = sM3
        print("  M3 set-up (no smooth baryon background, shells carry Om=0.315): M_ta/M_b=%.3f, r_ta=%.1f kpc, M_out/M_b=%.2f" % (sM3["Mta"] / 1e10, sM3["rta"], sM3["Mout"] / 1e10))
        mut_specs.append(make_spec("m3_nosmooth_N5000", core10, NOSMOOTH, sM3["Mout"], 5000, 0.1))
        mut_specs.append(make_spec("m4_subhubble_nocore_N2000", core10, COSMO, s10["Mout"], 2000, 0.1, core=0.0, icf=0.9))
    print("\n[runs]")
    run_specs(mut_specs if MUTATE else main_specs + extra)
    if MUTATE:
        for d in main_specs + extra:
            if not cached(d):
                print("  !! MUTATE needs cached main product %s; run the main script first" % d["name"]); return 2

    t0 = setups[("point", 1e10)]["t0"]
    P = {}  # pass/fail table
    def rec(name, ok, text):
        P[name] = bool(ok)
        print("  %-6s %s  %s" % (name, "PASS" if ok else "FAIL", text))

    # =========================================================== MUTATE branch
    if MUTATE:
        print("\n[MUTATE controls]")
        base = load_run("point_1e+10_q0.05_N20000")
        b1 = load_run("point_1e+10_q0.10_N5000")
        R1_base = R_at(base, core10, t0, 1.12, A0C)
        Rm = {}
        # M1
        r = load_run("m1_nocore_N5000")
        cM1 = dict(core10); cM1["Mb"] = 1e10   # target evaluated for the real 1e10 core
        av, snap = avg_curve(r, dict(core10, Mb=0.0), t0)
        rr = interp_lnr(r["rg"], av, 1.12 * rM(1e10, A0C)) / float(target_Mc_func(core10, A0C)(1.12 * rM(1e10, A0C)))
        nturn = int((r["TU"] > 0).sum())
        bite1 = (rr < 0.85) and nturn == 0
        print("  M1 drop the core: R(1.12)=%.3e, shells that turned around=%d  -> %s" % (rr, nturn, "BITES (H-A and H-E fail)" if bite1 else "DOES NOT BITE"))
        # M2
        r = load_run("m2_q0.002_N5000")
        R2 = R_at(r, core10, t0, 1.12, A0C)[0]
        R2b = R_at(r, core10, t0, 28.2, A0C)[0]
        ratio = R2 / R1_base[0]
        bite2 = ratio >= 1.3
        print("  M2 near-radial q=0.002: R(1.12)=%.3f, R(28.2)=%.3f vs q=0.05 (N=20000) R(1.12)=%.3f: ratio %.3f  -> %s (informative)" % (
            R2, R2b, R1_base[0], ratio, "bites (>=1.3)" if bite2 else "does not bite (<1.3)"))
        # M3
        sM3 = results["setup_m3"]
        r = load_run("m3_nosmooth_N5000")
        mt = measured_ta(r)
        bite3 = sM3["Mta"] / 1e10 > 27.1
        Rm3 = R_at(r, core10, t0, 28.2, A0C)[0]
        print("  M3 no smooth baryon background: M_ta/M_b=%.2f (single shell; line > 27.1); sim zero-velocity r=%s kpc vs r_ta=%.1f; R(28.2)=%.3f  -> %s" % (
            sM3["Mta"] / 1e10, ("%.1f" % mt["r"]) if mt and mt.get("flag") == "ok" else "n/a", sM3["rta"], Rm3, "BITES (H-E fails)" if bite3 else "DOES NOT BITE"))
        # M4
        r = load_run("m4_subhubble_nocore_N2000")
        Mi = (np.arange(r["N"]) + 0.5) * r["meta"]["m"]
        xi = (3 * Mi / (4 * np.pi * COSMO["Oc"] * RHOC0)) ** (1 / 3)
        dev = np.max(np.abs(r["R"] / xi - 1))
        bite4 = dev > 1e-2
        print("  M4 sub-Hubble initial velocity (v=0.9 H r), no core: max |r/r_Hubble - 1| at z=0 = %.3e (line > 1e-2)  -> %s" % (dev, "BITES (C1 fails)" if bite4 else "DOES NOT BITE"))
        # M5
        ok5 = True
        print("  M5 evaluator on the target's own M_c: see C8 in the main run (R = 1 identically; H-A and H-C fail by construction).")
        results["mutate"] = dict(M1=dict(R112=float(rr), nturn=nturn, bite=bool(bite1)), M2=dict(R112=float(R2), R282=float(R2b), base=float(R1_base[0]), ratio=float(ratio), bite=bool(bite2)),
                                 M3=dict(Mta_over_Mb=float(sM3["Mta"] / 1e10), bite=bool(bite3), R282=float(Rm3)), M4=dict(maxdev=float(dev), bite=bool(bite4)))
        allbite = bite1 and bite3 and bite4
        print("\n  MUTATE verdict: M1 %s, M3 %s, M4 %s; M2 (informative) %s -> exit %d" % (bite1, bite3, bite4, bite2, 1 if allbite else 0))
        results["seconds"] = time.time() - T0
        json.dump(results, open("cfg158_referee_MUTATE_results.json", "w"), indent=1, default=float)
        return 1 if allbite else 0

    # =========================================================== main branch
    runs = {}
    for geom in ("point", "exp"):
        for M in MASSES:
            for q in QS:
                for N in (20000, 5000):
                    nm = "%s_%.0e_q%.2f_N%d" % (geom, M, q, N)
                    runs[(geom, M, q, N)] = load_run(nm)
    cores = {(g, M): core_of(g, M) for g in ("point", "exp") for M in MASSES}

    # ---- C7 target identities
    print("\n[C7] target identities")
    dev = 0.0
    for M in MASSES:
        c = core_of("point", M)
        x = np.logspace(-4, 4, 25)
        f = target_Mc_func(c, A0C)
        Mc = f(x * rM(M, A0C))
        rr_ = x * rM(M, A0C)
        gN = G * M / rr_ ** 2
        gtot = np.sqrt(gN ** 2 + A0C * gN)
        rho_c = A0C / (4 * np.pi * G * rr_ * np.sqrt(1 + x ** 2))
        Cpt = rho_c * rr_ ** 3 * gtot
        dev = max(dev, float(np.max(np.abs(Cpt / (A0C / (4 * np.pi) * M) - 1))), float(np.max(np.abs(Mc / (M * (np.sqrt(1 + x ** 2) - 1)) - 1))))
    # closure ODE reproduces the point-mass formula
    Mb = 1e10; rm = rM(Mb, A0C)
    def rhs(lnr, y):
        r = math.exp(lnr); uN = G * Mb; return [A0C * r * r * uN / (uN + y[0])]
    sol = solve_ivp(rhs, (math.log(1e-8 * rm), math.log(1e4 * rm)), [0.0], method="DOP853", rtol=1e-13, atol=1e-30, dense_output=True)
    xs = np.logspace(-4, 4, 33)
    dclos = float(np.max(np.abs(sol.sol(np.log(xs * rm))[0] / G / (Mb * (np.sqrt(1 + xs ** 2) - 1)) - 1)))
    # exponential sphere: Poisson and C identity
    dpois = 0.0; dC = 0.0
    for M in MASSES:
        c = core_of("exp", M); f = target_Mc_func(c, A0C)
        for r in np.logspace(np.log10(0.05 * rM(M, A0C)), np.log10(30 * rM(M, A0C)), 25):
            eps = 1e-4 * r
            dw = G * (float(f(r + eps)) - float(f(r - eps))) / (2 * eps)
            uN = G * core_mass(c, r); u = uN + G * float(f(r))
            gtot = u / r ** 2
            rho_c = (A0C / (4 * np.pi)) * float(core_mass(c, r)) / (r ** 3 * gtot)
            dpois = max(dpois, abs(dw / (4 * np.pi * G * r * r * rho_c) - 1))
            dC = max(dC, abs(rho_c * r ** 3 * gtot / ((A0C / (4 * np.pi)) * float(core_mass(c, r))) - 1))
    rec("C7", dev < 1e-10 and dclos < 1e-8 and dpois < 1e-6 and dC < 1e-8,
        "point identities max dev %.1e (line 1e-10); closure ODE vs formula %.1e (1e-8); exp Poisson %.1e (1e-6); exp C identity %.1e (1e-8)" % (dev, dclos, dpois, dC))

    # ---- C1 Hubble flow
    print("\n[C1] no-core Hubble flow at z=0 (1e10 point shell set, N=20000)")
    r = load_run("c1_nocore_N20000")
    Mi = (np.arange(r["N"]) + 0.5) * r["meta"]["m"]
    xi = (3 * Mi / (4 * np.pi * COSMO["Oc"] * RHOC0)) ** (1 / 3)
    dr = np.max(np.abs(r["R"] / xi - 1)); dv = np.max(np.abs(r["V"] / (H0 * xi) - 1))
    rec("C1", dr <= 1e-6 and dv <= 1e-6, "max |dr/r| = %.2e, max |dv/v| = %.2e (line 1e-6 each; README quotes 4.3e-7 / 2.0e-7)" % (dr, dv))
    results["C1"] = dict(dr=float(dr), dv=float(dv))

    # ---- C2 EdS
    print("\n[C2] Einstein-de Sitter control (point seed, q=0.05, N=20000, snapshot a=1)")
    r = load_run("c2_eds_N20000")
    m = r["meta"]["m"]
    rta = sE["rta"]
    edges = 0.03 * 5.0 ** (np.arange(8) / 7) * rta
    cnt = np.histogram(r["R"], bins=edges)[0]
    rho = cnt * m / (4 * np.pi / 3 * (edges[1:] ** 3 - edges[:-1] ** 3))
    rc = np.sqrt(edges[1:] * edges[:-1])
    ok = cnt > 0
    slope = np.polyfit(np.log(rc[ok]), np.log(rho[ok]), 1)[0]
    loc = np.diff(np.log(rho)) / np.diff(np.log(rc))
    rec("C2", abs(slope + 2.25) <= 0.15 and abs(slope + 2.238) <= 0.05,
        "least-squares slope over r/r_ta in [0.03,0.15] (7 bins) = %.3f; |slope+9/4| line 0.15, |slope+2.238| line 0.05; local slopes %.2f..%.2f; counts %s; M_ta/M_seed=%.2f (hand 57)" % (
            slope, loc.min(), loc.max(), cnt.tolist(), sE["Mta"] / 1e10))
    results["C2"] = dict(slope=float(slope), local=loc.tolist(), counts=cnt.tolist(), Mta_over_seed=float(sE["Mta"] / 1e10))

    # ---- R(x)
    print("\n[cumulative mass ratios R(x) = M_c,sim(<r)/M_c,target(<r), canonical footing, window-averaged; N_s=20000]")
    R = {}
    for k, run in runs.items():
        geom, M, q, N = k
        R[k] = {x: R_at(run, cores[(geom, M)], t0, x, A0C) for x in (0.3, 1.12, 3.0, 10.0, 28.2)}
    print("  %-5s %-7s %-5s %8s %8s %8s %8s %8s   | N=5000: R(1.12) R(28.2)" % ("geom", "M_b", "q", "R(0.3)", "R(1.12)", "R(3)", "R(10)", "R(28.2)"))
    for geom in ("point", "exp"):
        for M in MASSES:
            for q in QS:
                a = R[(geom, M, q, 20000)]; b = R[(geom, M, q, 5000)]
                print("  %-5s %-7.0e %-5.2f %8.3f %8.3f %8.3f %8.3f %8.3f   | %8.3f %8.3f" % (geom, M, q, a[0.3][0], a[1.12][0], a[3.0][0], a[10.0][0], a[28.2][0], b[1.12][0], b[28.2][0]))
    allk = [(g, M, q, 20000) for g in ("point", "exp") for M in MASSES for q in QS]
    ptk = [k for k in allk if k[0] == "point"]
    r1 = np.array([R[k][1.12][0] for k in allk]); r28 = np.array([R[k][28.2][0] for k in allk])
    p1 = np.array([R[k][1.12][0] for k in ptk]); p28 = np.array([R[k][28.2][0] for k in ptk])
    print("\n  envelope R(1.12): all 24 runs [%.3f, %.3f]; point-only [%.3f, %.3f]" % (r1.min(), r1.max(), p1.min(), p1.max()))
    print("  envelope R(28.2): all 24 runs [%.3f, %.3f]; point-only [%.3f, %.3f]" % (r28.min(), r28.max(), p28.min(), p28.max()))
    print("  snapshot (z=0 only) R(1.12) all [%.3f, %.3f]; R(28.2) all [%.3f, %.3f]" % (min(R[k][1.12][1] for k in allk), max(R[k][1.12][1] for k in allk), min(R[k][28.2][1] for k in allk), max(R[k][28.2][1] for k in allk)))
    altR = {k: R_at(runs[k], cores[(k[0], k[1])], t0, 1.12, A0A)[0] for k in allk}
    altR28 = {k: R_at(runs[k], cores[(k[0], k[1])], t0, 28.2, A0A)[0] for k in allk}
    print("  alt footing envelope R(1.12) [%.3f, %.3f]; R(28.2) [%.3f, %.3f]" % (min(altR.values()), max(altR.values()), min(altR28.values()), max(altR28.values())))
    print("\n[headline lines]")
    rec("H-A", 0.85 <= r1.min() <= 1.15 and 3.57 <= r1.max() <= 4.83,
        "R(1.12) envelope (24 runs) [%.3f, %.3f] vs README 1.0-4.2 (min in [0.85,1.15], max in [3.57,4.83]); point-only [%.3f, %.3f]" % (r1.min(), r1.max(), p1.min(), p1.max()))
    rec("H-B", 0.238 <= r28.min() <= 0.322 and 0.561 <= r28.max() <= 0.759,
        "R(28.2) envelope (24 runs) [%.3f, %.3f] vs README 0.28-0.66 (min in [0.238,0.322], max in [0.561,0.759]); point-only [%.3f, %.3f]" % (r28.min(), r28.max(), p28.min(), p28.max()))
    falls = all(R[k][28.2][0] < R[k][1.12][0] for k in allk)
    seq = []
    for k in allk:
        rr = [R[k][x][0] for x in (1.12, 3.0, 10.0, 28.2)]
        seq.append(all(rr[i + 1] <= rr[i] * 1.0000001 for i in range(3)))
    med_ok = np.median(np.array(seq, float)) >= 0.5
    rec("H-C", falls and med_ok, "R(28.2)<R(1.12) in %d of 24 runs; ratio non-increasing over x=1.12,3,10,28.2 in %d of 24 runs (median run: %s)" % (
        sum(R[k][28.2][0] < R[k][1.12][0] for k in allk), sum(seq), "yes" if med_ok else "no"))

    # H-D
    print("\n[H-D radial scale: r1 (M_c = M_b), turnaround radius]")
    hd_ok = True
    exps = {}
    for geom in ("point", "exp"):
        for q in QS:
            xs = []; rs = []
            for M in MASSES:
                r1v = r1_of(runs[(geom, M, q, 20000)], cores[(geom, M)], t0)
                xs.append(M); rs.append(r1v)
            n = np.polyfit(np.log(xs), np.log(rs), 1)[0]
            exps[(geom, q)] = n
            print("  %-5s q=%.2f  r1 (kpc) = %s  x1 = %s  exponent n = %.3f" % (geom, q, ", ".join("%.2f" % v for v in rs),
                  ", ".join("%.2f" % (v / rM(M, A0C)) for v, M in zip(rs, MASSES)), n))
    nta = {g: np.polyfit(np.log(MASSES), np.log([setups[(g, M)]["rta"] for M in MASSES]), 1)[0] for g in ("point", "exp")}
    print("  turnaround-radius exponent: point %.4f, exp %.4f  (README 0.333 / 0.342)" % (nta["point"], nta["exp"]))
    pt_ok = all(0.29 <= exps[("point", q)] <= 0.38 for q in QS) and all(exps[("point", q)] < 0.45 for q in QS) and 0.323 <= nta["point"] <= 0.343
    ex_rep = all(0.17 <= exps[("exp", q)] <= 0.29 for q in QS)
    rec("H-D", pt_ok and ex_rep, "point exponents %s in [0.29,0.38], all < 0.45; turnaround %.4f in [0.323,0.343]; exp exponents %s (line [0.17,0.29]: %s)" % (
        ", ".join("%.3f" % exps[("point", q)] for q in QS), nta["point"], ", ".join("%.3f" % exps[("exp", q)] for q in QS), "met" if ex_rep else "NOT met, reported"))
    # H-E
    Mtas = {(g, M): setups[(g, M)]["Mta"] / M for g in ("point", "exp") for M in MASSES}
    pt = [Mtas[("point", M)] for M in MASSES]; ex = [Mtas[("exp", M)] for M in MASSES]
    rta_ref = {1e9: 236, 1e10: 508, 1e11: 1095, 1e12: 2358}
    xta_ref = {1e9: 193, 1e10: 132, 1e11: 90, 1e12: 61}
    rt_ok = all(abs(setups[("point", M)]["rta"] / rta_ref[M] - 1) <= 0.05 for M in MASSES)
    xt_ok = all(abs(setups[("point", M)]["rta"] / rM(M, A0C) / xta_ref[M] - 1) <= 0.06 for M in MASSES)
    rec("H-E", min(pt) >= 20.1 and max(pt) <= 27.1 and min(ex) >= 16.7 and max(ex) <= 27.1 and rt_ok and xt_ok,
        "M_ta/M_b point %s (line 20.1-27.1); exp %s (line 16.7-27.1); r_ta %s kpc (README 236,508,1095,2358, line 5%%: %s); x_ta %s (README 193,132,90,61, line 6%%: %s)" % (
            ", ".join("%.2f" % v for v in pt), ", ".join("%.2f" % v for v in ex), ", ".join("%.0f" % setups[("point", M)]["rta"] for M in MASSES), rt_ok,
            ", ".join("%.0f" % (setups[("point", M)]["rta"] / rM(M, A0C)) for M in MASSES), xt_ok))
    # H-F and R1 rows
    print("\n[H-F / R1 local C_infall/C_target on 0.1-dex bins x = 0.1..31.6 (window-averaged, N=20000; both footings)]")
    hf_all = True
    for foot, a0 in (("canonical", A0C), ("alt", A0A)):
        for geom in ("point", "exp"):
            for M in MASSES:
                row = []
                for q in QS:
                    rc, xc = ratio_curve(runs[(geom, M, q, 20000)], cores[(geom, M)], t0, a0)
                    sel = (xc >= 0.1) & (xc <= 30)
                    dev = np.max(np.abs(rc[sel] - 1))
                    inside = np.abs(rc[sel] - 1) <= 0.1
                    # longest run of consecutive in-band bins, in dex
                    best = 0; cur = 0
                    for b in inside:
                        cur = cur + 1 if b else 0; best = max(best, cur)
                    row.append((dev, best * 0.1, rc[sel][0], rc[sel][np.argmin(np.abs(xc[sel] - 1.12))], rc[sel][-1]))
                    if foot == "canonical" and not (dev > 0.1):
                        hf_all = False
                print("  %-9s %-5s %.0e  " % (foot, geom, M) + " | ".join("q=%.2f: max|r-1|=%.3g, in-band %.1f dex, r(0.11)=%.3g r(1.1)=%.3g r(28)=%.3g" % ((QS[i],) + row[i][:2] + row[i][2:]) for i in range(3)))
    rec("H-F", hf_all, "|C_infall/C_target - 1| > 0.10 somewhere in x in [0.1,30] in every canonical run (G1 fails everywhere)")

    # ---- C3
    print("\n[C3] resolution: N_s = 5,000 vs 20,000")
    d1 = max(abs(R[(g, M, q, 5000)][1.12][0] / R[(g, M, q, 20000)][1.12][0] - 1) for g in ("point", "exp") for M in MASSES for q in QS)
    d28 = max(abs(R[(g, M, q, 5000)][28.2][0] / R[(g, M, q, 20000)][28.2][0] - 1) for g in ("point", "exp") for M in MASSES for q in QS)
    med1 = np.median([abs(R[(g, M, q, 5000)][1.12][0] / R[(g, M, q, 20000)][1.12][0] - 1) for g in ("point", "exp") for M in MASSES for q in QS])
    med28 = np.median([abs(R[(g, M, q, 5000)][28.2][0] / R[(g, M, q, 20000)][28.2][0] - 1) for g in ("point", "exp") for M in MASSES for q in QS])
    allk5 = [(g, M, q, 5000) for g in ("point", "exp") for M in MASSES for q in QS]
    r15 = np.array([R[k][1.12][0] for k in allk5]); r285 = np.array([R[k][28.2][0] for k in allk5])
    print("  5,000-shell envelopes: R(1.12) [%.3f, %.3f], R(28.2) [%.3f, %.3f]; falls with radius in %d of 24" % (r15.min(), r15.max(), r285.min(), r285.max(), sum(R[k][28.2][0] < R[k][1.12][0] for k in allk5)))
    rec("C3", d1 <= 0.25 and d28 <= 0.10, "largest |R5k/R20k-1|: R(1.12) %.3f (line 0.25, median %.3f), R(28.2) %.3f (line 0.10, median %.3f)" % (d1, med1, d28, med28))
    # ---- C4
    print("\n[C4] time-step convergence (1e10 point q=0.1 N=5000: dt_s 1 -> 0.5 Myr, rtol 1e-10 -> 1e-11)")
    ra = load_run("point_1e+10_q0.10_N5000"); rb = load_run("c4_dt05_rtol11_N5000")
    ca = R_at(ra, core10, t0, 1.12, A0C)[0], R_at(ra, core10, t0, 28.2, A0C)[0]
    cb = R_at(rb, core10, t0, 1.12, A0C)[0], R_at(rb, core10, t0, 28.2, A0C)[0]
    rec("C4", abs(cb[0] / ca[0] - 1) <= 0.03 and abs(cb[1] / ca[1] - 1) <= 0.03, "R(1.12) %.3f -> %.3f (%.1f%%), R(28.2) %.3f -> %.3f (%.1f%%); line 3%%" % (ca[0], cb[0], 100 * (cb[0] / ca[0] - 1), ca[1], cb[1], 100 * (cb[1] / ca[1] - 1)))
    # ---- C5
    print("\n[C5] simulated zero-velocity radius at z=0 vs single-shell r_ta (N=20000 runs)")
    worst = 0.0; flags = 0
    for geom in ("point", "exp"):
        for M in MASSES:
            for q in QS:
                mt = measured_ta(runs[(geom, M, q, 20000)])
                if mt is None or mt["flag"] != "ok":
                    flags += 1; continue
                worst = max(worst, abs(mt["r"] / setups[(geom, M)]["rta"] - 1))
    rec("C5", flags == 0 and worst <= 0.01, "largest |r_zero-velocity(sim)/r_ta(single shell) - 1| = %.2e over 24 runs (line 1e-2); sign-change failures %d" % (worst, flags))
    # ---- C6
    print("\n[C6] static-orbit test of the integrator (1e10 softened point core, turnaround at 0.7 kpc, 2000 orbits)")
    ok6 = True; parts = []
    for q in QS:
        d = {}
        for ln in open(os.path.join(SIMS, "c6_orbit_q%.2f.orbit.txt" % q)):
            k, v = ln.split(); d[k] = float(v)
        good = abs(d["rp_over_rta"] / q - 1) <= 0.02 and d["drift_max"] <= 1e-3
        ok6 &= good
        parts.append("q=%.2f: rp/rta=%.5f, max |dE/E|=%.1e" % (q, d["rp_over_rta"], d["drift_max"]))
    rec("C6", ok6, "; ".join(parts) + " (lines: pericentre within 2%, drift <= 1e-3)")
    # ---- C8
    print("\n[C8] evaluator on the target's own M_c (R = 1 at every x)")
    rr1 = np.ones(24); rr28 = np.ones(24)
    a_ok = 0.85 <= rr1.min() <= 1.15 and 3.57 <= rr1.max() <= 4.83
    c_ok = all(rr28[i] < rr1[i] for i in range(24))
    rec("C8", (not a_ok) and (not c_ok), "on R=1 the evaluator gives H-A %s and H-C %s (both must FAIL)" % ("passes" if a_ok else "fails", "passes" if c_ok else "fails"))
    # ---- reported rows
    print("\n[reported rows]")
    rs = load_run("r3_ext6_N5000"); rj = load_run("r3_jpoint_N5000")
    for nm, rn in (("R3 extent 6 r_ta (M_out/M_b=%.1f)" % (sx["Mout"] / 1e10), rs), ("R3 point-mass-form j", rj)):
        print("  %-42s R(1.12)=%.3f  R(28.2)=%.3f   (base N=5000: %.3f, %.3f)" % (nm, R_at(rn, core10, t0, 1.12, A0C)[0], R_at(rn, core10, t0, 28.2, A0C)[0], ca[0], ca[1]))
    fr = []
    for k in allk:
        run = runs[k]; sel = run["TU"] == 2
        med = np.median(run["RP"][sel] / run["RTA"][sel]) if sel.any() else float("nan")
        fr.append((k, med / k[2]))
    print("  R4 realised median first pericentre / bracket q: min %.3f max %.3f; runs with median < 0.9 q: %d of 24 (README: 0.90-0.96)" % (min(v for _, v in fr), max(v for _, v in fr), sum(v < 0.9 for _, v in fr)))
    print("  integrator counters (N=20000 point 1e10 q=0.1): steps %d, rejects %d, resort fallbacks %d, wall %.0f s" % tuple(
        [int(runs[("point", 1e10, 0.1, 20000)]["meta"][k]) for k in ("steps", "rejects", "resort_fallbacks")] + [runs[("point", 1e10, 0.1, 20000)]["meta"]["seconds"]]))
    results.update(dict(R={"%s_%.0e_q%.2f_N%d" % k: {str(x): [float(v[0]), float(v[1])] for x, v in d.items()} for k, d in R.items()},
                        exps={"%s_q%.2f" % k: float(v) for k, v in exps.items()}, turnaround_exp={k: float(v) for k, v in nta.items()}, passes=P))
    print("\n[summary]")
    for k, v in P.items():
        print("  %-8s %s" % (k, "PASS" if v else "FAIL"))
    allpass = all(P.values())
    results["seconds"] = time.time() - T0
    print("\n  every headline line and control passes: %s  (exit %d)   total %.1f min" % (allpass, 0 if allpass else 1, (time.time() - T0) / 60))
    json.dump(results, open("cfg158_referee_results.json", "w"), indent=1, default=float)
    return 0 if allpass else 1


if __name__ == "__main__":
    sys.exit(main())
