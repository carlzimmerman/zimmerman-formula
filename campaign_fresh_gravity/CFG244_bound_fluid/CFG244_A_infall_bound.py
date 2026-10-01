#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
CFG244 Gate A -- AMOUNT: the BOUND part of a collapsed cold fluid (spherical secondary infall onto a static baryon core, the CFG118
design) against the target C(r) = rho_c r^3 g_tot = (a0/4 pi) M_b(<r).
Frozen criteria: ../CFG244_FROZEN_CRITERIA.md (committed 84e100c47, sha256 944adc80...), written before this script.

CODE.  CFG118's own code is IMPORTED READ-ONLY (module CFG118_secondary_infall: set-up, `shellcore.c` compiled at run time into a temporary
directory, snapshot/target helpers); nothing in CFG118 is edited and nothing is written into the repository.  The new layer (this file)
adds: (i) the bound/unbound classification at z = 0, (ii) the binned products and the shell-bootstrap restricted to the bound shells,
(iii) the three frozen sub-tests A1 (local amount), A2 (cumulative amount), A3 (radial scale against M_b), (iv) the controls and MUTATE modes.

CLASSIFICATION (frozen, one rule).  Instantaneous at z = 0: shell i is BOUND iff E_i = v_i^2/2 + j_i^2/(2 r_i^2) + Phi_eff(r_i) < Phi_eff(r_s),
Phi_eff = Phi_N(shells + core, half-own-mass convention neglected) + (f_sm H0^2/4) r^2 - (Omega_L H0^2/2) r^2 (the smooth background and Lambda of
the integrator), r_s the OUTERMOST radius where G M(<r)/r^2 = (Omega_L - f_sm/2) H0^2 r.  Alternatives, reported: B-ta ("ever turned around",
the integrator's turnaround record) and B-noL (E < 0 in Phi_N alone).

SUB-TESTS (point cores primary; both footings; q = 0.05, 0.1, 0.2).
  A1 local: C_bound/C_target on CFG118's 25 bins of 0.1 dex: |ratio - 1| <= 0.10 on every bin with centre in [0.1, 30], for at least one q at every mass.
  A2 cumulative: M_c,bound(<r)/M_c,target(<r) in [0.90, 1.10] on bins with centre in [0.3, 30], same bracket logic.
  A3 scale: R_s = radius where M_c,bound(<r) = M_b; exponent p of log R_s on log M_b over 1e9..1e12; PASS |p - 1/2| <= 0.0291; the turnaround reading
     |p - 1/3| <= 0.05 and |p - 1/2| > 0.10.
  Noise guard: a bin fails only if its deviation beyond the band exceeds max(shell-bootstrap sd, |R_5k - R_20k|).
Run: python3 CFG244_A_infall_bound.py ; MUTATE=MA1..MA5 python3 CFG244_A_infall_bound.py   (CFG244_NPROC sets the process count; ZF_REPO if outside the repo)
Exit: main 0; MUTATE exits 1 when the control bites, 0 when it does not.  kappa = 1/2 FITTED; no dark-matter particle; the mass is required; not closure.
"""
import os, sys, math, json, time, shutil, hashlib
sys.dont_write_bytecode = True
import numpy as np
import CFG244_common as K

K.use_lane_code()
sys.path.insert(0, os.path.join(K.LANES, "CFG118_secondary_infall"))
import CFG118_secondary_infall as M118            # READ-ONLY import of the record's code (its main() is not run)

HERE = K.HERE
CACHE = os.path.join(HERE, "CFG244_A_infall_bound_sims.json")
G, H0, OL, OB, FB = M118.G, M118.H0, M118.OL, M118.OB, M118.FB
FOOTS = M118.FOOTS
MASSES, QS, GEOMS = M118.MASSES, M118.QS, M118.GEOMS
XB = M118.XB_EDGES
XC = np.sqrt(XB[1:] * XB[:-1])
A1_MASK = (XC >= 0.1) & (XC <= 30.0)
A2_MASK = (XC >= 0.3) & (XC <= 30.0)
N20, N5 = M118.NS, M118.NS_C3
FSM = OB
KNET = (OL - 0.5 * FSM) * H0 ** 2


# ------------------------------------------------------------------------------------------------ classification of a z = 0 state
def core_phi(r, M, geom, soft):
    r = np.asarray(r, float)
    if geom == "point":
        return -G * M / np.sqrt(r * r + soft * soft)
    h = M118.HEXP[M]
    return -G * M * (M118.Mb_enc(M, "exp", r) / M / r + (r + h) * np.exp(-r / h) / (2 * h))


def core_mass(r, M, geom, soft):
    if geom is None or M == 0:
        return np.zeros_like(np.asarray(r, float))
    return M118.Mb_enc(M, geom, r, soft)


def classify_state(rf, vf, j2f, m, M, geom, soft):
    """instantaneous bound classification at z = 0 (see the module docstring).  M = 0 / geom None: no core."""
    o = np.argsort(rf); rs = rf[o]
    inv = 1.0 / rs
    suf = np.concatenate([np.cumsum(inv[::-1])[::-1], [0.0]])            # sum_{j >= k} 1/r_j

    def phi_N(r):
        r = np.atleast_1d(np.asarray(r, float))
        k = np.searchsorted(rs, r, side="left")                           # shells strictly inside r
        ph = -G * (m * k / r + m * suf[k])
        if geom is not None and M > 0:
            ph = ph + core_phi(r, M, geom, soft)
        return ph

    def phi_eff(r):
        r = np.atleast_1d(np.asarray(r, float))
        return phi_N(r) + 0.25 * FSM * H0 ** 2 * r * r - 0.5 * OL * H0 ** 2 * r * r

    def force_net(r):
        r = np.atleast_1d(np.asarray(r, float))
        Me = m * np.searchsorted(rs, r, side="left") + core_mass(r, M, geom, soft)
        return G * Me / (r * r) - KNET * r

    grid = np.geomspace(0.3 * rs[0], 30.0 * rs[-1], 40000)
    F = force_net(grid)
    idx = np.where((F[:-1] > 0) & (F[1:] <= 0))[0]
    if len(idx):
        i = idx[-1]
        r_s = float(grid[i] + (grid[i + 1] - grid[i]) * F[i] / (F[i] - F[i + 1]))
        e_crit = float(phi_eff(r_s)[0])
    else:
        r_s, e_crit = float("nan"), -np.inf
    E = 0.5 * vf * vf + j2f / (2 * rf * rf) + phi_eff(rf)
    E_N = 0.5 * vf * vf + j2f / (2 * rf * rf) + phi_N(rf)
    return dict(bound=E < e_crit, bound_noL=E_N < 0.0, r_s=r_s, e_crit=e_crit, E=E)


# ------------------------------------------------------------------------------------------------ the binned products with masks
def binned_multi(snap_s, masks, m, edges, Mb_c, taus, boot_key=None, Wts=None):
    rc = np.sqrt(edges[1:] * edges[:-1])
    s0 = np.sort(snap_s[0]); Mc0 = m * np.searchsorted(s0, rc)
    rhobar = (Mb_c + Mc0) / (4.0 * math.pi / 3.0 * rc ** 3)
    W = np.sqrt(3.0 * math.pi / (16.0 * G * rhobar))
    W = np.minimum(W, taus[-1])
    c = M118.tavg_weights(taus, W)
    live = np.where(c.any(axis=0))[0]
    res = {k: dict(dM=np.zeros(len(rc)), Mc=np.zeros(len(rc))) for k in masks}
    N = snap_s.shape[1]
    if boot_key is not None:
        O = np.zeros((len(rc), N)); E = np.zeros((len(rc), N)); idx = np.arange(N); mk_b = masks[boot_key]
    for s in live:
        rs = snap_s[s]
        for k, mk in masks.items():
            so = np.sort(rs if mk is None else rs[mk])
            cnt = np.searchsorted(so, edges)
            res[k]["dM"] += c[:, s] * m * np.diff(cnt)
            res[k]["Mc"] += c[:, s] * m * np.searchsorted(so, rc)
        if boot_key is not None:
            bi = np.searchsorted(edges, rs, side="right") - 1
            ok = (bi >= 0) & (bi < len(rc)) & mk_b
            O[bi[ok], idx[ok]] += c[bi[ok], s]
            E += (c[:, s][:, None] * (rs[None, :] < rc[:, None])) * mk_b[None, :]
    if boot_key is not None:
        bdM = m * np.einsum("bn,kn->bk", O, Wts); bMc = m * np.einsum("bn,kn->bk", E, Wts)
        res["_boot"] = dict(dM=bdM, Mc=bMc)
    return rc, res


# ------------------------------------------------------------------------------------------------ one simulation + analysis (a worker)
def run_bound(job):
    so, spec = job
    t_start = time.time()
    kind, M, geom, q, N = spec["kind"], spec["M"], spec["geom"], spec["q"], spec["N"]
    nocore = (kind == "NOCORE")
    if nocore:
        su = M118.setup(1e10, "point", "LCDM"); su["soft"] = None; Mref = 1e10; geom_eff = "point"
    else:
        su = M118.setup(M, geom, "LCDM"); Mref = M; geom_eff = geom
    eds, Om_, OL_, fsm, ocold = M118.cosmo("LCDM")
    m = su["M_out"] / N
    Mk = m * (np.arange(N) + 0.5)
    r0 = (3.0 * Mk / (4.0 * math.pi * su["rhoci"])) ** (1.0 / 3.0)
    v0 = su["Hi"] * r0
    core = 0 if nocore else (1 if geom == "point" else 2)
    P = M118.Params(eds, H0, Om_, OL_, fsm, G, core, 0.0 if nocore else M, su["soft"] or 0.0, M118.HEXP.get(M, 1.0), N, m, q,
                    su["t0"], su["t1"], M118.KMAX, M118.KF, M118.ETA, M118.ETAH, 0)
    T = su["t1"] - su["t0"]
    taus = M118.snapshot_taus(T)
    tsnap = (su["t1"] - taus)[::-1].copy(); tsnap[-1] = su["t1"]
    P.nsnap = len(tsnap)
    out, stats = M118.integrate(so, P, r0, v0, tsnap)
    snap_s = out["snap"][::-1]
    rf, vf, j2f = out["r"], out["v"], out["j2"]
    Mcore = 0.0 if nocore else M
    cl = classify_state(rf, vf, j2f, m, Mcore, None if nocore else geom, su["soft"])
    turned = np.isfinite(out["r_ta"])
    masks = {"all": None, "inst": cl["bound"], "ta": turned, "noL": cl["bound_noL"]}
    rMc = M118.r_M(Mref)
    x = rf / rMc
    res = dict(spec=spec, setup={k: v for k, v in su.items()}, m=m, stats=stats, N=N, r_s_phi=cl["r_s"], e_crit=cl["e_crit"])
    # diagnostics at z = 0
    inner = x <= 30.0
    outer = (rf >= su["r_ta0"]) & (rf <= 3.0 * su["r_ta0"])
    res["diag"] = dict(
        n_inner=int(inner.sum()),
        frac_bound_inner=float(cl["bound"][inner].mean()) if inner.any() else float("nan"),
        frac_ta_inner=float(turned[inner].mean()) if inner.any() else float("nan"),
        frac_noL_inner=float(cl["bound_noL"][inner].mean()) if inner.any() else float("nan"),
        mass_bound_inner=float(m * (cl["bound"] & inner).sum()), mass_all_inner=float(m * inner.sum()),
        flip_turned_unbound=float((turned & ~cl["bound"])[inner].mean()) if inner.any() else float("nan"),
        flip_unturned_bound=float((~turned & cl["bound"])[inner].mean()) if inner.any() else float("nan"),
        n_outer=int(outer.sum()),
        frac_unbound_outer_inst=float((~cl["bound"])[outer].mean()) if outer.any() else float("nan"),
        frac_unbound_outer_noL=float((~cl["bound_noL"])[outer].mean()) if outer.any() else float("nan"),
        frac_bound_all=float(cl["bound"].mean()), frac_ta_all=float(turned.mean()),
        r_ta_meas=M118.zero_velocity_radius(rf, vf) if not nocore else float("nan"),
        n_turned=int(turned.sum()))
    # radial scale: radius where the cumulative z = 0 mass of each class equals M_b (rank estimator)
    Rs = {}
    for k in ("all", "inst", "ta", "noL"):
        sel = np.ones(N, bool) if masks[k] is None else masks[k]
        rr = np.sort(rf[sel]); kk = int(math.ceil(Mref / m))
        Rs[k] = float(rr[kk - 1]) if len(rr) >= kk else float("nan")
    res["Rs_z0"] = Rs
    res["x_Rs_z0"] = {k: (v / rMc if np.isfinite(v) else float("nan")) for k, v in Rs.items()}
    if nocore or kind == "NOCORE":
        res["seconds"] = time.time() - t_start
        return res
    Mb_core = lambda r: M118.Mb_enc(M, geom, r)
    rng = np.random.default_rng(118)
    Wts = rng.multinomial(N, np.full(N, 1.0 / N), size=M118.NBOOT).astype(float)
    res["foot"] = {}
    for f in FOOTS:
        e = XB * M118.r_M(M, f)
        rc = np.sqrt(e[1:] * e[:-1])
        Mbc = Mb_core(rc)
        rcb, b = binned_multi(snap_s, masks, m, e, Mbc, taus, boot_key="inst", Wts=Wts)
        T_ = M118.target_binned(M, geom, f)
        dMT, McT = np.array(T_["dM"]), np.array(T_["Mc"])
        ff = {}
        for k in ("all", "inst", "ta", "noL"):
            rat = M118.ratio_of(b[k]["dM"], b[k]["Mc"], dMT, McT, Mbc)
            ff[k] = dict(dM=b[k]["dM"].tolist(), Mc=b[k]["Mc"].tolist(), ratio=rat.tolist(),
                         cum_ratio=(b[k]["Mc"] / McT).tolist())
        brat = M118.ratio_of(b["_boot"]["dM"], b["_boot"]["Mc"], dMT[:, None], McT[:, None], Mbc[:, None])
        ff["inst"]["boot_sd"] = np.std(brat, axis=1).tolist()
        ff["inst"]["boot_sd_cum"] = np.std(b["_boot"]["Mc"] / McT[:, None], axis=1).tolist()
        ff["target"] = dict(dM=dMT.tolist(), Mc=McT.tolist(), Mbc=Mbc.tolist())
        # time-averaged cumulative scale: radius (in x) where the cumulative bound mass crosses M_b (log-linear interpolation)
        Mcb = np.array(b["inst"]["Mc"])
        if Mcb.max() >= M and Mcb.min() <= M:
            kx = int(np.argmax(Mcb >= M))
            if kx > 0:
                lx = np.log(rc[kx - 1]) + (np.log(rc[kx]) - np.log(rc[kx - 1])) * (M - Mcb[kx - 1]) / (Mcb[kx] - Mcb[kx - 1])
                ff["Rs_tavg_x"] = float(math.exp(lx) / M118.r_M(M, f))
            else:
                ff["Rs_tavg_x"] = float("nan")
        else:
            ff["Rs_tavg_x"] = float("nan")
        res["foot"][f] = ff
    res["seconds"] = time.time() - t_start
    return res


def c1_job(job):
    return M118.run_one(job)


def kepler_job(job):
    return M118.kepler_test(job)


def config_hash():
    import inspect
    src = open(os.path.join(K.LANES, "CFG118_secondary_infall", "shellcore.c")).read()
    src += "".join(inspect.getsource(f) for f in (run_bound, classify_state, binned_multi, core_phi, core_mass))
    return hashlib.sha256(src.encode()).hexdigest()[:16]


def simulate_all(nproc):
    import multiprocessing as mp
    tmp, so = M118.build_lib()
    try:
        specs = []
        for N in (N20, N5):
            for q in QS:
                for M in MASSES:
                    for g in GEOMS:
                        specs.append(dict(kind="main" if N == N20 else "C3", M=M, geom=g, q=q, N=N))
        specs.append(dict(kind="NOCORE", M=1e10, geom="point", q=0.05, N=N20))
        specs.sort(key=lambda s: (s["N"] != N20, s["geom"] != "point", s["q"]))
        t0 = time.time()
        with mp.get_context("spawn").Pool(nproc) as pool:
            c1 = pool.apply_async(c1_job, ((so, dict(kind="C1", M=1e10, geom=None, q=0.05, N=N20)),))
            kep = pool.map(kepler_job, [(so, q) for q in QS])
            runs = []
            for i, r in enumerate(pool.imap_unordered(run_bound, [(so, s) for s in specs])):
                s = r["spec"]
                print(f"    [{i + 1:2d}/{len(specs)}] {s['kind']:6s} M={s['M']:.0e} {str(s['geom']):5s} q={s['q']:.2f} N={s['N']:5d}: {r['seconds']:6.0f} s (elapsed {time.time() - t0:.0f} s)", flush=True)
                runs.append(r)
            c1r = c1.get()
        return dict(hash=config_hash(), runs=runs, kepler=kep, c1=dict(dr=c1r["c1_dr"], dv=c1r["c1_dv"], n_turned=c1r["n_turned"]), wall=time.time() - t0, nproc=nproc)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


# ================================================================================================ main
def main():
    MUT = os.environ.get("MUTATE", "")
    SLUG = "CFG244_A_infall_bound" + (f"_MUTATE_{MUT}" if MUT else "")
    R = K.Report(SLUG); P = R.P
    P(__doc__.split("Run: python3")[0].strip())
    P(f"\n  repo: <repo>   mode: {'MUTATE=' + MUT if MUT else 'main'}   CFG118 code: imported read-only (module CFG118_secondary_infall; shellcore.c compiled in a temporary directory)")
    nproc = int(os.environ.get("CFG244_NPROC", str(min(14, os.cpu_count() or 4))))
    sims = None
    h = config_hash()
    if os.path.exists(CACHE):
        d = json.load(open(CACHE))
        if d.get("hash") == h and (MUT or os.environ.get("CFG244_REUSE") == "1"):
            sims = d; P(f"\n  simulation products reused from the cache (hash {h})")
    if sims is None:
        R.banner("SIMULATIONS  (CFG118 design: 24 main runs at N = 20,000, 24 at N = 5,000, one no-core run, the CFG118 Hubble-flow control, 3 test orbits)")
        sims = K.jclean(simulate_all(nproc))
        if not MUT:
            json.dump(sims, open(CACHE, "w"))
    runs = sims["runs"]
    get = lambda kind, M=None, g=None, q=None: [r for r in runs if r["spec"]["kind"] == kind and (M is None or r["spec"]["M"] == M)
                                                and (g is None or r["spec"]["geom"] == g) and (q is None or r["spec"]["q"] == q)]
    P(f"\n  simulation wall time {sims['wall'] / 60:.1f} min on {sims['nproc']} processes")

    # ------------------------------------------------------------------ set-up and controls
    R.banner("SET-UP and CONTROLS")
    su_ok = True; lines = []
    r_ta_ref = {1e9: 236.0, 1e10: 508.0, 1e11: 1095.0, 1e12: 2358.0}
    for M in MASSES:
        for g in GEOMS:
            su = get("main", M, g, 0.1)[0]["setup"]
            lines.append(f"    {M:.0e} {g:5s}: M_ta/M_b = {su['M_ta'] / M:6.2f}  r_ta(z=0) = {su['r_ta0']:7.1f} kpc  x_ta = {su['r_ta0'] / M118.r_M(M):6.1f}  M_out/M_b = {su['M_out'] / M:6.1f}")
            if g == "point":
                su_ok &= (20.1 <= su["M_ta"] / M <= 27.1) and abs(su["r_ta0"] / r_ta_ref[M] - 1) <= 0.01
    P("\n".join(lines))
    R.check("C-A1 CFG118's set-up reproduced: M_ta/M_b within 20.1-27.1 (CFG158's line) and r_ta(z = 0) = 236 / 508 / 1095 / 2358 kpc within 1% (point cores)", "see lines above", su_ok)
    # exact reproduction of CFG118's committed all-shell ratio
    cj = os.path.join(K.LANES, "CFG118_secondary_infall", "CFG118_secondary_infall_sims.json")
    dev = float("nan"); nrep = 0
    if os.path.exists(cj) and not MUT:
        cd = json.load(open(cj))
        dev = 0.0
        for r in get("main") + get("C3"):
            s = r["spec"]
            for cr in cd["runs"]:
                cs = cr["spec"]
                if cs["kind"] == s["kind"] and cs["M"] == s["M"] and cs["geom"] == s["geom"] and cs["q"] == s["q"] and cs["N"] == s["N"]:
                    for f in FOOTS:
                        a = np.array(r["foot"][f]["all"]["ratio"], float); b = np.array(cr["foot"][f]["ratio"], float)
                        ok = np.isfinite(a) & np.isfinite(b)
                        dev = max(dev, float(np.max(np.abs(a[ok] - b[ok]) / np.maximum(np.abs(b[ok]), 1e-300))))
                    nrep += 1
        R.check("C-A1b the all-shell C/C_target of this layer reproduces CFG118's committed ratios (deterministic code; imported kernel)", f"{nrep} runs compared; max relative difference {dev:.2e}", dev < 1e-6)
        R.num("c_a1b", dict(nrep=nrep, maxdev=dev))
    c1 = sims["c1"]
    R.check("C-A2 CFG118's C1 (no core): every shell on the Hubble flow to 1e-6 at z = 0", f"max |dr/r| = {c1['dr']:.2e}, max |dv/v| = {c1['dv']:.2e}", c1["dr"] <= 1e-6 and c1["dv"] <= 1e-6)
    worst = max(abs(k_["dE"]) for k_ in sims["kepler"])
    R.check("C-A4 test shell in the static softened 1e10 point mass: energy drift over the run < 1e-3 (frozen line)", "; ".join(f"q={k_['q']}: {k_['dE']:+.2e}, r_p/r_ta {k_['peri_ratio']:.4f}" for k_ in sims["kepler"]), worst < 1e-3)
    # classifier synthetic test (C-A4b)
    Mt, rt = 1e10, np.array([100.0, 100.0, 100.0])
    soft = 1e-3 * M118.r_M(Mt)
    vt = np.array([0.0, 800.0, 100.0]); j2t = np.zeros(3)
    ct = classify_state(rt, vt, j2t, 0.0, Mt, "point", soft)
    rs_an = (G * Mt / KNET) ** (1.0 / 3.0)
    ecr_an = -G * Mt / math.sqrt(rs_an ** 2 + soft ** 2) + 0.25 * FSM * H0 ** 2 * rs_an ** 2 - 0.5 * OL * H0 ** 2 * rs_an ** 2
    ok_cls = bool(ct["bound"][0]) and (not bool(ct["bound"][1])) and abs(ct["r_s"] / rs_an - 1) < 1e-3 and abs(ct["e_crit"] / ecr_an - 1) < 1e-3
    R.check("C-A4b the classifier on a synthetic core + test shells: v = 0 bound, v = 800 km/s unbound; saddle radius and E_crit match the closed form",
            f"r_s = {ct['r_s']:.2f} (closed form {rs_an:.2f}); E_crit rel. diff {ct['e_crit'] / ecr_an - 1:.1e}; bound flags {ct['bound'].tolist()}", ok_cls)
    # resolution control
    cum_dev = []
    for r5 in get("C3", g="point"):
        s5 = r5["spec"]
        r20 = get("main", s5["M"], s5["geom"], s5["q"])[0]
        for f in FOOTS:
            a = np.array(r5["foot"][f]["inst"]["cum_ratio"]); b = np.array(r20["foot"][f]["inst"]["cum_ratio"])
            i28 = int(np.argmin(np.abs(np.log(XC / 28.2))))
            cum_dev.append(abs(a[i28] / b[i28] - 1))
    R.check("C-A3 resolution: cumulative bound-mass ratio at x about 28 between 5,000 and 20,000 shells within 10% (point cores, all q, both footings)",
            f"largest {max(cum_dev):.3f}, median {np.median(cum_dev):.3f} over {len(cum_dev)} cases (CFG118: median 2%, largest 10%)", max(cum_dev) <= 0.10)

    # ------------------------------------------------------------------ the classification diagnostics
    R.banner("THE BOUND PART: classification diagnostics at z = 0 (shells inside x = r/r_M <= 30; canonical r_M; point cores | exponential spheres)")
    P(f"  {'M_b':>6s} {'geom':5s} {'q':>5s} {'N in':>6s} {'bound(E)':>9s} {'turned':>7s} {'bound(noL)':>10s} {'turned&unbound':>14s} {'unturned&bound':>14s} {'unbound(outer)':>14s} {'(noL)':>6s}  r_s/r_ta0   x_Rs(z0, bound)")
    for q in QS:
        for M in MASSES:
            for g in GEOMS:
                r_ = get("main", M, g, q)[0]; d = r_["diag"]
                P(f"  {M:6.0e} {g:5s} {q:5.2f} {d['n_inner']:6d} {d['frac_bound_inner']:9.4f} {d['frac_ta_inner']:7.4f} {d['frac_noL_inner']:10.4f} {d['flip_turned_unbound']:14.4f} "
                  f"{d['flip_unturned_bound']:14.4f} {d['frac_unbound_outer_inst']:14.3f} {d['frac_unbound_outer_noL']:6.3f}  {r_['r_s_phi'] / r_['setup']['r_ta0']:8.2f}  {r_['x_Rs_z0']['inst']:8.3f}")
    nc = get("NOCORE")[0]["diag"]
    P(f"\n  no-core run (M = 0; the MA2 control): bound fraction inside x <= 30: {nc['frac_bound_inner']:.4f}; of all shells {nc['frac_bound_all']:.4f}; shells that turned around {nc['n_turned']}")
    mainp = [get("main", M, "point", q)[0] for q in QS for M in MASSES]
    minbf = min(r_["diag"]["frac_bound_inner"] for r_ in mainp)
    mf_ta = max(abs(r_["diag"]["frac_ta_inner"] - r_["diag"]["frac_bound_inner"]) for r_ in mainp)
    mflip = max(r_["diag"]["flip_turned_unbound"] + r_["diag"]["flip_unturned_bound"] for r_ in mainp)
    P(f"\n  point cores, all q and masses: smallest bound fraction inside x <= 30 = {minbf:.4f}; largest |turned - bound| = {mf_ta:.4f}; largest boundness-flip proxy = {mflip:.4f}")
    R.num("diag", dict(min_bound_frac_inner=minbf, max_ta_minus_bound=mf_ta, max_flip_proxy=mflip, nocore_bound_inner=nc["frac_bound_inner"]))

    # ------------------------------------------------------------------ the sub-tests
    cls_key = "inst"
    if MUT == "MA4":
        cls_key = "ta"         # classification by "ever turned around"
    if MUT == "MA5":
        cls_key = "noL"        # Lambda removed from the classifier
    TT = {}                    # (foot, q, M, geom) -> dict

    def rat_of(r_, f, key, kind="loc"):
        F_ = r_["foot"][f][key]
        if MUT == "MA1":       # evaluator fed the target's own profile
            return np.ones(len(XC))
        return np.array(F_["ratio" if kind == "loc" else "cum_ratio"], float)

    for f in FOOTS:
        R.banner(f"A1 / A2 ({f} footing, a0 = {M118.A0_SI[f]:.4e}): bound-part C/C_target (local, 0.1-dex bins) and M_c,bound(<r)/M_c,target(<r) at x = r/r_M  [classifier: {cls_key}]")
        P("  x centres:   " + " ".join(f"{x:6.2f}" for x in XC))
        for q in QS:
            P(f"\n  q = {q}:")
            for g in GEOMS:
                for M in MASSES:
                    r20 = get("main", M, g, q)[0]; r5 = get("C3", M, g, q)[0]
                    loc = rat_of(r20, f, cls_key); cum = rat_of(r20, f, cls_key, "cum")
                    loc5 = rat_of(r5, f, cls_key); cum5 = rat_of(r5, f, cls_key, "cum")
                    sd = np.array(r20["foot"][f]["inst"]["boot_sd"], float); sdc = np.array(r20["foot"][f]["inst"]["boot_sd_cum"], float)
                    if MUT == "MA1":
                        sd = np.zeros(len(XC)); sdc = np.zeros(len(XC))
                    guard_l = np.maximum(sd, np.abs(loc5 - loc)); guard_c = np.maximum(sdc, np.abs(cum5 - cum))
                    dl = np.abs(loc - 1.0); dc = np.abs(cum - 1.0)
                    fail_l = A1_MASK & (dl - 0.10 > guard_l); fail_c = A2_MASK & (dc - 0.10 > guard_c)
                    out_l = A1_MASK & (dl > 0.10); out_c = A2_MASK & (dc > 0.10)
                    TT[(f, q, M, g)] = dict(loc=loc.tolist(), cum=cum.tolist(), pass_A1=bool(not out_l.any()), pass_A2=bool(not out_c.any()),
                                            fail_A1=bool(fail_l.any()), fail_A2=bool(fail_c.any()), max_dev_loc=float(np.nanmax(np.where(A1_MASK, dl, 0))),
                                            max_dev_cum=float(np.nanmax(np.where(A2_MASK, dc, 0))), noise_only_A1=bool(out_l.any() and not fail_l.any()),
                                            noise_only_A2=bool(out_c.any() and not fail_c.any()))
                    if q == 0.1 or g == "point":
                        P(f"  {g:5s} {M:6.0e} loc " + " ".join(f"{x:6.2f}" if np.isfinite(x) else "   nan" for x in loc))
                        P(f"  {'':5s} {'':6s} cum " + " ".join(f"{x:6.2f}" if np.isfinite(x) else "   nan" for x in cum))
    # per (foot, q, geom): which sub-tests hold at every mass
    P("\n  SUMMARY of A1 / A2 (every mass must hold for a bracket; PASS = within the band everywhere; FAIL = guarded fail = beyond the band by more than the noise guard):")
    sumr = {}
    for geom in GEOMS:
        for f in FOOTS:
            for q in QS:
                a1p = all(TT[(f, q, M, geom)]["pass_A1"] for M in MASSES); a2p = all(TT[(f, q, M, geom)]["pass_A2"] for M in MASSES)
                a1f = any(TT[(f, q, M, geom)]["fail_A1"] for M in MASSES); a2f = any(TT[(f, q, M, geom)]["fail_A2"] for M in MASSES)
                mx1 = max(TT[(f, q, M, geom)]["max_dev_loc"] for M in MASSES); mx2 = max(TT[(f, q, M, geom)]["max_dev_cum"] for M in MASSES)
                sumr[(geom, f, q)] = dict(A1_pass=a1p, A2_pass=a2p, A1_guarded_fail=a1f, A2_guarded_fail=a2f, max_dev_loc=mx1, max_dev_cum=mx2)
                P(f"    {geom:5s} {f:9s} q={q:.2f}: A1 {'PASS' if a1p else ('FAIL' if a1f else 'noise-limited')} (largest |ratio-1| {mx1:.2f}); "
                  f"A2 {'PASS' if a2p else ('FAIL' if a2f else 'noise-limited')} (largest |ratio-1| {mx2:.2f})")
    # headline numbers at x about 0.11, 1.12, 28.2 (canonical)
    i0, i1, i2 = [int(np.argmin(np.abs(np.log(XC / x)))) for x in (0.11, 1.12, 28.2)]
    P("\n  canonical footing, point cores, q = 0.05 / 0.1 / 0.2: local ratio and cumulative ratio at x = 0.11 / 1.12 / 28.2 (min-max over the four masses):")
    hl = {}
    for q in QS:
        for kind in ("loc", "cum"):
            vals = [np.array(TT[("canonical", q, M, "point")][kind]) for M in MASSES]
            rng_ = [(min(v[i] for v in vals), max(v[i] for v in vals)) for i in (i0, i1, i2)]
            hl[(q, kind)] = rng_
            P(f"    q={q:.2f} {kind}: " + "   ".join(f"x={XC[i]:.2f}: {a:.2f}-{b:.2f}" for i, (a, b) in zip((i0, i1, i2), rng_)))
    # ------------------------------------------------------------------ A3: the exponent
    R.banner("A3: the radial scale R_s (where M_c,bound(<r) = M_b) against M_b; target R_s = sqrt(3) r_M proportional to M^(1/2)")
    expo = {}
    cen = 1.0 / 3.0 if MUT == "MA3" else 0.5
    for geom in GEOMS:
        for q in QS:
            xs = []; xt = []
            for M in MASSES:
                r_ = get("main", M, geom, q)[0]
                Rs = r_["Rs_z0"][cls_key]; xs.append(Rs); xt.append(r_["foot"]["canonical"].get("Rs_tavg_x", float("nan")) * M118.r_M(M) if cls_key == "inst" else float("nan"))
            lm = np.log10(MASSES); p = float(np.polyfit(lm, np.log10(xs), 1)[0])
            pt = float(np.polyfit(lm, np.log10(xt), 1)[0]) if np.all(np.isfinite(xt)) else float("nan")
            r5 = [get("C3", M, geom, q)[0]["Rs_z0"][cls_key] for M in MASSES]
            p5 = float(np.polyfit(lm, np.log10(r5), 1)[0])
            xr = [xs[i] / M118.r_M(MASSES[i]) for i in range(4)]
            expo[(geom, q)] = dict(p=p, p_tavg=pt, p_5k=p5, x_Rs=xr, spread=max(xr) / min(xr))
            P(f"    {geom:5s} q={q:.2f}: R_s = {', '.join(f'{x:.1f}' for x in xs)} kpc  (x = R_s/r_M: {', '.join(f'{v:.3f}' for v in xr)}; target {math.sqrt(3):.3f})  "
              f"exponent p = {p:.3f}  (time-averaged estimator {pt:.3f}; 5,000 shells {p5:.3f})  spread max/min x = {max(xr) / min(xr):.2f}")
    p_pt = np.array([expo[("point", q)]["p"] for q in QS])
    a3_half = all(abs(p - cen) <= 0.0291 for p in p_pt)
    a3_third = all((abs(p - 1 / 3) <= 0.05 and abs(p - 0.5) > 0.10) for p in p_pt)
    P(f"\n  point cores: exponents {', '.join(f'{p:.3f}' for p in p_pt)}; |p - {cen:.3f}| <= 0.0291 for all q: {a3_half}; the turnaround reading (|p - 1/3| <= 0.05 and |p - 1/2| > 0.10) for all q: {a3_third}")

    # ------------------------------------------------------------------ the gate
    A1_pass = any(all(sumr[("point", f, q)]["A1_pass"] for f in FOOTS) for q in QS)
    A2_pass = any(all(sumr[("point", f, q)]["A2_pass"] for f in FOOTS) for q in QS)
    A1_fail = all(any(sumr[("point", f, q)]["A1_guarded_fail"] for f in FOOTS) for q in QS)
    A2_fail = all(any(sumr[("point", f, q)]["A2_guarded_fail"] for f in FOOTS) for q in QS)
    A3_pass = bool(a3_half)
    A3_fail = not any(abs(p - cen) <= 0.0291 for p in p_pt)
    gate = "PASS" if (A1_pass and A2_pass and A3_pass) else ("FAIL" if (A1_fail or A2_fail or A3_fail) else "UNDEFINED")
    P(f"\n  A1 (local, within 10% for at least one q at every mass, both footings): {'PASS' if A1_pass else ('FAIL' if A1_fail else 'noise-limited')}")
    P(f"  A2 (cumulative, within 10% for x in [0.3, 30]): {'PASS' if A2_pass else ('FAIL' if A2_fail else 'noise-limited')}")
    P(f"  A3 (|p - {cen:.3f}| <= 0.0291 for every q): {'PASS' if A3_pass else 'FAIL'}")
    P(f"  GATE A (all three; point cores primary): {gate}")
    R.num("A", dict(gate=gate, A1_pass=A1_pass, A1_fail=A1_fail, A2_pass=A2_pass, A2_fail=A2_fail, A3_pass=A3_pass, A3_fail=A3_fail,
                    exponents={f"{k[0]}|{k[1]}": v for k, v in expo.items()}, summary={f"{k[0]}|{k[1]}|{k[2]}": v for k, v in sumr.items()},
                    headline={f"{k[0]}|{k[1]}": v for k, v in hl.items()}, classifier=cls_key))
    if not MUT:
        R.num("tables", {f"{k[0]}|{k[1]}|{k[2]:.0e}|{k[3]}": v for k, v in TT.items()})
        # R_cum / local numbers for the binding-failure statement
        R.num("binding", dict(p_point=p_pt.tolist(), spread=[expo[("point", q)]["spread"] for q in QS], hl={f"{k[0]}|{k[1]}": v for k, v in hl.items()}))
        R.write(); P(f"\n  GATE A RESULT: {gate}")
        sys.exit(0)
    # ------------------------------------------------------------------ MUTATE: baseline (instantaneous classifier, real evaluator) for comparison
    base_gate = "FAIL"; base = None
    if os.path.exists(os.path.join(HERE, "CFG244_A_infall_bound_results.json")):
        base = json.load(open(os.path.join(HERE, "CFG244_A_infall_bound_results.json")))["numbers"]
        base_gate = base["A"]["gate"]
    if MUT == "MA1":
        bite = (gate == "PASS" or (A1_pass and A2_pass)) and base_gate != "PASS"
        tgt = f"A1/A2 evaluator on the target's own profile: A1 {A1_pass}, A2 {A2_pass} (main gate {base_gate})"
    elif MUT == "MA2":
        bf_main = min(r_["diag"]["frac_bound_inner"] for r_ in mainp)
        bite = bf_main >= 0.99 and (nc["frac_bound_inner"] < 0.5 or not np.isfinite(nc["frac_bound_inner"]))
        tgt = f"bound fraction inside x <= 30: with the core (smallest over point runs) {bf_main:.4f}; no core {nc['frac_bound_inner']:.4f} (cell: >= 0.99)"
    elif MUT == "MA3":
        bite = A3_pass and not (base and base["A"]["A3_pass"])
        tgt = f"A3 against a target scale proportional to M^(1/3): p = {', '.join(f'{p:.3f}' for p in p_pt)} -> PASS {A3_pass} (main {base['A']['A3_pass'] if base else 'n/a'})"
    elif MUT == "MA4":
        bf_inst = np.array([r_["diag"]["frac_bound_inner"] for r_ in mainp]); bf_ta = np.array([r_["diag"]["frac_ta_inner"] for r_ in mainp])
        bite = (bf_inst.min() >= 0.99) != (bf_ta.min() >= 0.99)
        tgt = f"bound fraction cell (>= 0.99 inside x <= 30): instantaneous min {bf_inst.min():.4f}, turned-around min {bf_ta.min():.4f}; gate {gate} (main {base_gate})"
    elif MUT == "MA5":
        out_i = np.array([r_["diag"]["frac_unbound_outer_inst"] for r_ in mainp]); out_n = np.array([r_["diag"]["frac_unbound_outer_noL"] for r_ in mainp])
        in_i = np.array([r_["diag"]["frac_bound_inner"] for r_ in mainp]); in_n = np.array([r_["diag"]["frac_noL_inner"] for r_ in mainp])
        bite = float(np.max(np.abs(out_i - out_n))) >= 0.05
        tgt = f"outer-region (r_ta0..3 r_ta0) unbound fraction instantaneous vs no-Lambda: largest difference {np.max(np.abs(out_i - out_n)):.3f} (cell: >= 0.05); inner bound fractions differ by at most {np.max(np.abs(in_i - in_n)):.4f}"
    else:
        raise SystemExit("unknown MUTATE id")
    P(f"\n  MUTATE {MUT}: {tgt}\n  BITES: {bite}")
    R.num("mutate", dict(id=MUT, bites=bool(bite), target=tgt, gate=gate))
    R.write()
    sys.exit(1 if bite else 0)


if __name__ == "__main__":
    main()
