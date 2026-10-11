#!/usr/bin/env python3
"""CFG598 main (FROZEN_CRITERIA.md): the settling front of CFG541 class A with infall sources (transport-clock geometry automatic),
hosts log M_ta 11-15 + MW, alpha in {0, 0.25, 0.5, 1, 2, inf}, both footings, placements P0 / P2; supply bound; CFG593 context;
MW 30 kpc; CFG543 P2 groups; CFG555 512^3 excess with scalar lambda; verdict.
  OMP_NUM_THREADS=1 nice -n 10 python3 cfg598_front.py               -> cfg598_front.out, cfg598_results.json
  CFG598_MUTATE=1 OMP_NUM_THREADS=1 nice -n 10 python3 cfg598_front.py -> cfg598_front_MUTATE.out, cfg598_results_MUTATE.json (exit 1 iff all teeth bite)
kappa = 1/2 FITTED; footings never pooled; cold energy mass required; not theory closed."""
import os
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_v] = "1"
import sys, json, math, io, contextlib, time
import numpy as np
from multiprocessing import Pool

HERE = os.path.dirname(os.path.abspath(__file__)); LANES = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import cfg598_lib as C                                          # noqa: E402

MUT = os.environ.get("CFG598_MUTATE", "0") == "1"
TAG = "_MUTATE" if MUT else ""
EXT = os.path.abspath(os.path.join(LANES, "..", "..", "_external_data"))
LINES = []
def P(s=""):
    print(s, flush=True); LINES.append(s)

LMS = [11.0, 11.5, 12.0, 12.5, 13.0, 13.5, 14.0, 14.5, 15.0]
ALPHAS = [0.0, 0.25, 0.5, 1.0, 2.0, math.inf]
FOOTS = ["can", "alt"]; PLS = ["P0", "P2"]
XS = (0.03, 0.05, 0.1, 0.2, 0.3, 0.5, 0.7, 1.0)
XFINE = np.geomspace(0.003, 1.0, 60)
ak = lambda a: "inf" if not np.isfinite(a) else f"{a:g}"


def summarize(R, o, Scen, Mcat):
    d = R.diag(o["m"], XS)
    lr = np.log(R.rf); rta = R.H.rta0
    Mcf = np.concatenate([[0.0], np.cumsum(o["m"])])
    Mc_f = np.interp(np.log(XFINE * rta), lr, Mcf); Scen_f = np.interp(np.log(XFINE * rta), lr, Scen)
    Scx = {str(x): float(np.interp(math.log(x * rta), lr, Scen)) for x in XS}
    return dict(F_set=d["F_set"], S=d["S"], Mc=d["Mc"], r_f=d["r_f"], r_f50=d["r_f50"], r_f99=d["r_f99"],
                S_over_Scen={k: d["S"][k] / Scx[k] for k in Scx}, Mc_over_Mccen={k: d["Mc"][k] / Scx[k] for k in Scx},
                R_fine=(Mc_f / np.maximum(Scen_f, 1e-300)).tolist(), transit_frac=o["transit"] / Mcat, mass_err=o["mass_err"],
                vmax_over_Vf=o["vmax_over_Vf"], n=o["n"], hit_cap=bool(o["hit_cap"]), q=d["q"])


def job(args):
    lM, foot, pl, alphas, N = args
    H = C.Host(None, mw=True) if lM == "MW" else C.Host(lM)
    out = {}
    for a in alphas:
        R = C.Run(H, foot, pl, N=N)
        t = time.time(); o = R.run(a)
        Scen_f, Mcat = R.census()
        R.set_baryons(H.X_ta(o["t"]))
        s = summarize(R, o, Scen_f, Mcat)
        s["runtime_s"] = time.time() - t
        if lM == "MW":
            sel = R.rf[1:] <= 30.0
            q = s["q"][sel]; mphv = R.mph[sel]
            s["MW_min_q_30"] = float(np.min(q[mphv > 0])); s["MW_max_q_30"] = float(np.max(q[mphv > 0]))
            s["MW_Mc_over_Mph_30"] = float(o["m"][sel].sum() / R.mph[sel].sum())
            s["MW_rta_kpc"] = H.rta0
        s.pop("q")
        out[ak(a)] = s
    meta = dict(rta0_kpc=H.rta0, Mta=H.Mta, Mb0=H.Mb0, fret=H.fret, t0_gyr=H.t0 * C.TU_GYR, ts_gyr=H.t_s * C.TU_GYR, mono_t=H.mono_t, mono_r=H.mono_r,
                rM0_kpc=math.sqrt(C.GK * H.Mb0 / C.A0K[foot]), sup=C.alpha_sup(H, foot))
    return (lM, foot, pl), out, meta


# ---------------------------------------------------------------------------------------------------------------- K3 / M2 benchmark
def benchmark(alpha=1.0, N=3000):
    """transport_clock benchmark on the PDE flux: SIS target, filled core r < r_i, uniform f beyond; instantaneous d_t f per cell."""
    R = C.Run.__new__(C.Run)
    R.N = N; R.rf = rf = np.geomspace(1.0, 1000.0, N + 1); R.V = 4 * math.pi / 3 * np.diff(rf ** 3); R.A = 4 * math.pi * rf ** 2
    Vf = 200.0; Cm = Vf ** 2 / C.GK; ri = 10.0
    R.mph = Cm * np.diff(rf); R.rhob = np.zeros(N); R.thr = np.full(N, 1e-30)
    rc = np.sqrt(rf[1:] * rf[:-1]); out = {}
    for f in (0.2, 0.5, 0.8):
        m = np.where(rf[:-1] >= ri - 1e-9, f * R.mph, R.mph)
        dt = 1e-9
        m2, dtu, _ = R.flux_step(m, alpha, 1e30, dt)
        dfdt = (m2 - m) / dtu / R.mph
        rows = {}
        for x in (2, 5, 10):
            i = int(np.argmin(np.abs(rc - x * ri)))
            pred = alpha * Vf * math.sqrt(f) * (1 - f) * ri / rc[i] ** 2
            single = alpha * Vf * math.sqrt(f) * (1 - f) / rc[i]
            rows[str(x)] = dict(pde=float(dfdt[i]), transport_clock=pred, single_clock=single, rel=float(dfdt[i] / pred - 1),
                                single_over_pde=float(single / dfdt[i]), r_over_ri=float(rc[i] / ri))
        out[str(f)] = rows
    return out


def single_clock_check(alpha=1.0, r=50.0, Vf=200.0, f0=0.01, T=20.0):
    u0 = math.sqrt(f0); f = f0; n = 20000; dt = T / n
    rhs = lambda f: alpha * math.sqrt(max(f, 0)) * (1 - f) * Vf / r
    for _ in range(n):
        k1 = rhs(f); k2 = rhs(f + 0.5 * dt * k1); k3 = rhs(f + 0.5 * dt * k2); k4 = rhs(f + dt * k3)
        f += dt * (k1 + 2 * k2 + 2 * k3 + k4) / 6
    ua = math.tanh(alpha * Vf * T / (2 * r) + math.atanh(u0))
    return dict(numeric=f, analytic=ua ** 2, absdiff=abs(f - ua ** 2))


def single_clock_fset(lM, foot, alpha):
    """reported only: per-cell single clock from entry (r_ta(t) passes r), f0 = 0, V_f final."""
    H = C.Host(lM); R = C.Run(H, foot, "P0"); R.set_baryons(1.0)
    rc = R.rc; tent = np.interp(rc, H.r_sh, H.t_ta, left=H.t_s); T = np.maximum(H.t0 - tent, 0.0)
    f = np.tanh(alpha * R.Vf0 * T / (2 * rc)) ** 2
    Sf = np.concatenate([[0.0], np.cumsum(f * R.mph)]); Mph = R.Mphf - R.Mphf[0]
    lr = np.log(R.rf)
    return {str(x): float(np.interp(math.log(x * H.rta0), lr, Sf) / np.interp(math.log(x * H.rta0), lr, Mph)) for x in XS}


# ---------------------------------------------------------------------------------------------------------------- groups (CFG543 P2)
def groups_setup():
    sys.path.insert(0, os.path.join(LANES, "CFG543_group_supply"))
    with contextlib.redirect_stdout(io.StringIO()):
        import cfg543_group_supply as M43                         # noqa: E402  (read-only; main guarded)
    M43.GEO = M43.gas_geometry(M43.lovisari())
    return M43, M43.read_groups()


def sigma_log_R(M43, o, a0, dlM, Rfun):
    """cfg543 sigma_log (kind P2, Mhot = 0, edge) copied, with ONE change: the law's cold mass x R(r)."""
    lM = o["lM"] + dlM
    M, Mhot, Msup, _ = M43.config_masses(lM, dict(kind="P2"))
    Re = o["Re"]; a = Re * M43.KPC / M43.HERN_RE; r = M43.X * a
    Mb = M * M43.M_T
    gN = M43.G * Mb * M43.MSUN / r ** 2
    nu = M43.C.nu(gN / a0)
    mph = (nu - 1.0) * Mb
    k = np.where(mph >= Msup)[0]
    mc = mph.copy()
    if len(k):
        xe = k[0]; mc = np.where(np.arange(len(M43.X)) > xe, mph[xe], mph)
    Rr = Rfun(lM, r / M43.KPC) if Rfun is not None else 1.0
    g = M43.G * (Mb + Rr * mc) * M43.MSUN / r ** 2
    s2 = np.trapezoid(4 * np.pi * M43.X ** 2 * M43.RHO_T * r * g * M43.X, M43.LX) / 3.0
    return 0.5 * math.log10(s2) - 3.0


def groups_run(M43, rows, a0, Rfun):
    lp = np.array([sigma_log_R(M43, o, a0, 0.0, Rfun) for o in rows])
    lp2 = np.array([sigma_log_R(M43, o, a0, 0.01, Rfun) for o in rows])
    D = np.array([o["ls"] for o in rows]) - lp
    return M43.stats(D, (lp2 - lp) / 0.01)


def make_Rfun(table, rta_of_lM):
    """table: {lM: R_fine array on XFINE}.  R(lM_bar, r_kpc) with group M_ta[Msun/h] = M_bar h/(0.10 f_b)."""
    lms = np.array(sorted(table)); Rs = np.array([table[l] for l in lms])
    def Rfun(lMbar, r_kpc):
        lMta = lMbar + math.log10(C.h / (0.10 * C.FB))
        lc = float(np.clip(lMta, lms[0], lms[-1]))
        j = int(np.clip(np.searchsorted(lms, lc) - 1, 0, len(lms) - 2)); w = (lc - lms[j]) / (lms[j + 1] - lms[j])
        Rx = (1 - w) * Rs[j] + w * Rs[j + 1]
        rta = 10 ** np.interp(lc, lms, np.log10([rta_of_lM[l] for l in lms]))
        x = np.clip(r_kpc / rta, XFINE[0], XFINE[-1])
        return np.interp(np.log(x), np.log(XFINE), Rx)
    return Rfun


# ---------------------------------------------------------------------------------------------------------------- CFG555 lambda
def stat555(k, Pr, s8r, k0, P0, s80):
    """cfg555_analysis.stat copied (CFG361 cuts)."""
    cat = lambda s8, pd: "FAIL" if abs(s8 - 1) > 0.20 else ("GROWTH OK" if abs(s8 - 1) <= 0.05 and pd <= 0.10 else "TENSION")
    k = np.array(k); m = k <= 1.0; r = np.array(Pr)[m] / np.interp(k[m], np.array(k0), np.array(P0))
    i = int(np.argmax(np.abs(r - 1)))
    return dict(s8=s8r / s80, pdev=float(np.abs(r[i] - 1)), k_at=float(k[m][i]), verdict=cat(s8r / s80, float(np.abs(r[i] - 1))))


def lam_spectrum(name, lam):
    d = json.load(open(os.path.join(EXT, "cfg555_work", f"cfg555_{name}.json")))
    s0 = json.load(open(os.path.join(EXT, d["s0_base"] + ".json")))["snap"]["z0"]
    Pp, Pg, Ps = (np.array(d[x]) for x in ("P_part", "P_grav", "P_src"))
    Pl = Pp + lam * (Pg - Pp - Ps) + lam ** 2 * Ps
    s2 = d["s8_part"] ** 2 + lam * (d["s8_grav"] ** 2 - d["s8_part"] ** 2 - d["s8_src"] ** 2) + lam ** 2 * d["s8_src"] ** 2
    return stat555(d["k"], Pl, math.sqrt(max(s2, 0)), s0["k"], s0["P"], s0["sigma8"])


RUN555 = {"can": "425_R3_can_512", "alt": "439_A_alt_512"}


# ================================================================================================================ main
def main():
    res = dict(lane="CFG598", date="2026-10-10", mutate=MUT, settings="kappa=1/2 FITTED; footings never pooled; nu_mono; candidate B; G9; no EFE; "
               "accretion history INHERITED (CFG557 cfg557_lib, EPS q=2.2 PROVISIONAL); cold energy mass required; not theory closed")
    P(__doc__.strip().splitlines()[0])
    P("kappa = 1/2 FITTED; footings never pooled; cold energy mass required; not theory closed.  Accretion history INHERITED (CFG557).")
    E = C.epoch0()
    k1 = dict(t0_gyr=E.t_obs * C.L.GYR_PER_HINV, Delta_ta=E.Delta_ta)
    k1["pass"] = abs(k1["t0_gyr"] / 13.820 - 1) <= 1e-3 and abs(k1["Delta_ta"] / 11.806 - 1) <= 1e-3
    P(f"\nK1 t0 = {k1['t0_gyr']:.4f} Gyr (CFG557 13.820), Delta_ta = {k1['Delta_ta']:.4f} (11.806) -> {'PASS' if k1['pass'] else 'FAIL'}")
    res["K1"] = k1

    # K3 / M2 benchmark
    bm = benchmark(1.0)
    k3 = max(abs(r["rel"]) for f in bm.values() for r in f.values()) <= 0.02
    m2b = max(abs(r["single_over_pde"] / r["r_over_ri"] - 1) for f in bm.values() for r in f.values()) <= 0.02
    sc = single_clock_check()
    P("\nK3 transport-clock benchmark (SIS target, filled core r_i, uniform f beyond; PDE flux divergence, one instant, alpha = 1):")
    for f, rows in bm.items():
        P("  f = " + f + ": " + "; ".join(f"r/r_i {r['r_over_ri']:.2f}: PDE {r['pde']:.4e} vs TC {r['transport_clock']:.4e} (rel {r['rel']:+.4f}), "
                                        f"single/PDE {r['single_over_pde']:.3f}" for r in rows.values()))
    P(f"  -> K3 {'PASS' if k3 else 'FAIL'} (<= 2%);  M2 tooth (single clock = r/r_i x PDE to 2%): {'BITES' if m2b else 'FAILS'}")
    P(f"  M2 single-clock code path vs analytic tanh^2: |diff| {sc['absdiff']:.2e} -> {'BITES' if sc['absdiff'] <= 1e-3 else 'FAILS'}")
    res["K3_benchmark"] = bm; res["K3_pass"] = bool(k3); res["M2_benchmark_bites"] = bool(m2b); res["M2_ode"] = sc

    if MUT:
        return mutate(res)

    # ------------------------------------------------------------------------------------------------ host runs
    jobs = [(lM, ft, pl, ALPHAS, 300) for lM in LMS + ["MW"] for ft in FOOTS for pl in PLS]
    t = time.time()
    with Pool(4) as pool:
        outs = pool.map(job, jobs, chunksize=1)
    P(f"\nHost runs: {len(jobs)} jobs x {len(ALPHAS)} alpha in {time.time() - t:.0f} s (4 processes, 1 thread each)")
    RUNS, META = {}, {}
    for (lM, ft, pl), out, meta in outs:
        RUNS[f"{lM}|{ft}|{pl}"] = out; META[f"{lM}|{ft}"] = meta
    # convergence
    cj = [(14.0, "can", pl, [0.5], 600) for pl in PLS]
    with Pool(2) as pool:
        couts = pool.map(job, cj)
    conv = {}
    for (lM, ft, pl), out, meta in couts:
        a = RUNS[f"{lM}|{ft}|{pl}"]["0.5"]["F_set"]; b = out["0.5"]["F_set"]
        conv[pl] = max(abs(a[k] - b[k]) for k in a)
    P(f"Convergence N = 600 vs 300 (log M_ta 14, alpha 0.5, can): max |dF_set| P0 {conv['P0']:.4f}, P2 {conv['P2']:.4f} (disclose if > 0.02)")
    res["convergence_max_dFset"] = conv
    K2 = max(v[a]["mass_err"] for v in RUNS.values() for a in v); K4 = [f"{k}|{a}" for k, v in RUNS.items() for a in v if v[a]["hit_cap"]]
    P(f"K2 max mass error {K2:.2e} (<= 1e-10) -> {'PASS' if K2 <= 1e-10 else 'FAIL'};  K4 runs at step cap: {K4 if K4 else 'none'}")
    res["K2_max_mass_err"] = K2; res["K4_capped"] = K4
    res["host_meta"] = META

    # ------------------------------------------------------------------------------------------------ tables
    P("\n=== f_set(<r) at t0 (fraction of the law's phantom settled inside r), front r_f/r_ta (q < 0.9), S/S_inf(<0.5 r_ta) ===")
    for pl in PLS:
        for ft in FOOTS:
            P(f"\n[{pl} | {ft}]   columns: F_set at r/r_ta = " + " ".join(f"{x:g}" for x in XS) + " | r_f | S/S_inf(0.5) | S/S_cen(0.5) | transit | vmax/Vf")
            for lM in LMS + ["MW"]:
                v = RUNS[f"{lM}|{ft}|{pl}"]
                for a in ALPHAS:
                    s = v[ak(a)]; si = v["inf"]
                    P(f"  {str(lM):>4s} a={ak(a):>4s}: " + " ".join(f"{s['F_set'][str(x)]:.3f}" for x in XS) +
                      f" | {s['r_f']:.3f} | {s['S']['0.5'] / si['S']['0.5']:.3f} | {s['S_over_Scen']['0.5']:.3f} | {s['transit_frac']:.3f} | {s['vmax_over_Vf']:.2f}")
    P("\n=== supply-based alpha bound alpha_sup = G S/(T V_f^3 2/(3 sqrt 3)), T = t0 - t_ta(X=0.5)  [T = t0 - t_s] ===")
    for lM in LMS + ["MW"]:
        P(f"  {str(lM):>4s}: " + "; ".join(f"{ft}: {META[f'{lM}|{ft}']['sup']['alpha_sup']:.3f} [{META[f'{lM}|{ft}']['sup']['alpha_sup_Ts']:.3f}] "
                                           f"(T {META[f'{lM}|{ft}']['sup']['T_gyr']:.2f} Gyr, V_f {META[f'{lM}|{ft}']['sup']['Vf_kms']:.0f})" for ft in FOOTS))

    # single clock (reported)
    P("\nReported: single-clock (no transport-clock correction) F_set at t0 vs PDE P0 (alpha 0.5 / 1, can), r/r_ta = 0.1 0.2 0.5")
    scr = {}
    for lM in (12.0, 13.0, 14.0, 15.0):
        for a in (0.5, 1.0):
            f1 = single_clock_fset(lM, "can", a); f2 = RUNS[f"{lM}|can|P0"][ak(a)]["F_set"]
            scr[f"{lM}|{a}"] = dict(single=f1, pde=f2)
            P(f"  {lM:g} a={a:g}: single " + " ".join(f"{f1[str(x)]:.3f}" for x in (0.1, 0.2, 0.5)) + "  | PDE " + " ".join(f"{f2[str(x)]:.3f}" for x in (0.1, 0.2, 0.5)))
    res["single_clock_reported"] = scr

    # ------------------------------------------------------------------------------------------------ (b) MW
    P("\n=== (i) MW inside 30 kpc (CFG553): SETTLED iff q >= 0.99 in every cell r <= 30 kpc; OVERFILLED iff M_c/M_ph(<30) - 1 > 0.01 ===")
    MWr = {}
    for pl in PLS:
        for ft in FOOTS:
            for a in ALPHAS:
                s = RUNS[f"MW|{ft}|{pl}"][ak(a)]
                settled = s["MW_min_q_30"] >= 0.99; over = s["MW_Mc_over_Mph_30"] - 1 > 0.01
                MWr[f"{pl}|{ft}|{ak(a)}"] = dict(min_q=s["MW_min_q_30"], max_q=s["MW_max_q_30"], Mc_over_Mph=s["MW_Mc_over_Mph_30"],
                                                  settled=bool(settled), overfilled=bool(over), i_holds=bool(settled and not over))
                P(f"  {pl} {ft} a={ak(a):>4s}: min q {s['MW_min_q_30']:.4f}, max q {s['MW_max_q_30']:.3f}, M_c/M_ph(<30) {s['MW_Mc_over_Mph_30']:.4f} -> "
                  f"{'SETTLED' if settled else 'NOT SETTLED'}{', OVERFILLED' if over else ''} -> (i) {'holds' if settled and not over else 'fails'}")
    res["MW"] = MWr

    # ------------------------------------------------------------------------------------------------ (a) CFG593 context + (ii)
    HI = [13.0, 13.5, 14.0, 14.5, 15.0]
    P("\n=== (ii) partial settling, log M_ta 13-15: F_set(<0.2) <= 0.8, 0.3 <= F_set(<0.5) <= 0.8, S/S_inf(<0.5) <= 0.9 ===")
    P("    (a) CFG593 context only (LCDM-SHMR masses): 30-80% settled reaching ~0.5 r_ta; its family is a UNIFORM partial fill, this PDE gives an inside-out front")
    IIr = {}
    for pl in PLS:
        for ft in FOOTS:
            for a in ALPHAS[1:5]:
                rows = []
                for lM in HI:
                    v = RUNS[f"{lM}|{ft}|{pl}"]; s = v[ak(a)]
                    f2, f5 = s["F_set"]["0.2"], s["F_set"]["0.5"]; rr = s["S"]["0.5"] / v["inf"]["S"]["0.5"]
                    rows.append(dict(lM=lM, F02=f2, F05=f5, S_over_Sinf=rr, ok=bool(f2 <= 0.8 and 0.3 <= f5 <= 0.8 and rr <= 0.9)))
                ok = all(r["ok"] for r in rows)
                IIr[f"{pl}|{ft}|{ak(a)}"] = dict(rows=rows, holds=bool(ok))
                P(f"  {pl} {ft} a={ak(a):>4s}: " + "  ".join(f"{r['lM']:g}:{r['F02']:.2f}/{r['F05']:.2f}/{r['S_over_Sinf']:.2f}{'' if r['ok'] else '*'}" for r in rows)
                  + f" -> (ii) {'holds' if ok else 'fails'}")
    res["II"] = IIr

    # ------------------------------------------------------------------------------------------------ (iii) CFG555 lambda
    P("\n=== (iii) CFG555 512^3 gravitating excess with the settled source scaled by lambda = mean_{13-15} S_alpha/S_cen(<0.5 r_ta) ===")
    J555 = json.load(open(os.path.join(LANES, "CFG555_growth_on_gravitating_field", "cfg555_results.json")))
    ctrl = {}
    for ft, nm in RUN555.items():
        g1 = lam_spectrum(nm, 1.0); g0 = lam_spectrum(nm, 0.0); ref = J555["runs"][nm]
        ok = abs(g1["pdev"] - ref["gravitating"]["pdev"]) <= 1e-6 and abs(g1["s8"] - ref["gravitating"]["s8"]) <= 1e-6 and \
            abs(g0["pdev"] - ref["particle"]["pdev"]) <= 1e-6 and abs(g0["s8"] - ref["particle"]["s8"]) <= 1e-6
        ctrl[ft] = dict(lam1=g1, lam0=g0, ref_grav=ref["gravitating"]["pdev"], ref_part=ref["particle"]["pdev"], pass_=bool(ok))
        P(f"  control {ft} ({nm}): lambda 1 -> max|P-1| {g1['pdev']:.6f} s8 {g1['s8']:.6f} (CFG555 {ref['gravitating']['pdev']:.6f} / {ref['gravitating']['s8']:.6f}); "
          f"lambda 0 -> {g0['pdev']:.6f} / {g0['s8']:.6f} (particle {ref['particle']['pdev']:.6f}) -> {'PASS' if ok else 'FAIL'}")
    res["III_controls"] = ctrl
    IIIr = {}
    for pl in PLS:
        for ft in FOOTS:
            for a in ALPHAS:
                lams = [RUNS[f"{lM}|{ft}|{pl}"][ak(a)]["S_over_Scen"]["0.5"] for lM in HI]
                lm = float(np.mean(lams)); st = lam_spectrum(RUN555[ft], lm)
                stl, sth = lam_spectrum(RUN555[ft], min(lams)), lam_spectrum(RUN555[ft], max(lams))
                ref = ctrl[ft]["ref_grav"]
                lvl = "PASS" if (st["pdev"] <= 0.10 and abs(st["s8"] - 1) <= 0.05) else ("REDUCED" if st["pdev"] <= 0.75 * ref else "NOT REDUCED")
                IIIr[f"{pl}|{ft}|{ak(a)}"] = dict(lam_mean=lm, lam_min=min(lams), lam_max=max(lams), stat=st, stat_lam_min=stl, stat_lam_max=sth, level=lvl)
                P(f"  {pl} {ft} a={ak(a):>4s}: lambda {lm:.3f} [{min(lams):.3f}, {max(lams):.3f}] -> max|P-1| {st['pdev']:.4f} (k {st['k_at']:.2f}), s8 {st['s8']:.4f}; "
                  f"bracket {stl['pdev']:.4f}..{sth['pdev']:.4f} -> {lvl}")
    # level on both footings
    III = {}
    for pl in PLS:
        for a in ALPHAS:
            lv = [IIIr[f"{pl}|{ft}|{ak(a)}"]["level"] for ft in FOOTS]
            III[f"{pl}|{ak(a)}"] = "PASS" if all(x == "PASS" for x in lv) else ("REDUCED" if all(x in ("PASS", "REDUCED") for x in lv) else "NOT REDUCED")
    res["III"] = IIIr; res["III_both"] = III

    # ------------------------------------------------------------------------------------------------ groups CFG543
    P("\n=== groups CFG543 P2 with the cold mass x R(r) = M_c,alpha/M_c,cen (point-mass host ratio, interpolated) ; PASS iff |Z| < 2 ===")
    M43, rows = groups_setup()
    J543 = json.load(open(os.path.join(LANES, "CFG543_group_supply", "cfg543_results.json")))
    GR = {}
    for ft in FOOTS:
        a0 = M43.FOOT[ft]                                           # CFG543 footing values (9.36e-11 / 1.13e-10), as in CFG543
        st1 = groups_run(M43, rows, a0, None); ref = J543["footings"][ft]["configs"]["P2"]["mean"]
        g0 = abs(st1["mean"] - ref) <= 1e-6
        P(f"  G0 {ft}: R = 1 -> {st1['mean']:+.6f} vs CFG543 P2 {ref:+.6f} -> {'PASS' if g0 else 'FAIL'}")
        GR[f"G0|{ft}"] = dict(mean=st1["mean"], ref=ref, pass_=bool(g0))
        rta_of = {lM: META[f"{lM}|{ft}"]["rta0_kpc"] for lM in LMS}
        for pl in PLS:
            for a in ALPHAS:
                table = {lM: np.array(RUNS[f"{lM}|{ft}|{pl}"][ak(a)]["R_fine"]) for lM in LMS}
                st = groups_run(M43, rows, a0, make_Rfun(table, rta_of))
                GR[f"{pl}|{ft}|{ak(a)}"] = dict(mean=st["mean"], Z=st["Z"], pass_=bool(abs(st["Z"]) < 2))
                P(f"  {pl} {ft} a={ak(a):>4s}: mean {st['mean']:+.4f}, Z {st['Z']:+.2f} -> {'PASS' if abs(st['Z']) < 2 else 'FAIL'}")
    res["groups"] = GR

    # ------------------------------------------------------------------------------------------------ verdict
    P("\n=== VERDICT (frozen section 3) ===")
    rank = {"DOES NOT": 0, "PARTIAL": 1, "WORKS": 2}
    V = {}
    for pl in PLS:
        works, partial = [], []
        for a in ALPHAS[1:5]:
            i_ = all(MWr[f"{pl}|{ft}|{ak(a)}"]["i_holds"] for ft in FOOTS)
            ii = all(IIr[f"{pl}|{ft}|{ak(a)}"]["holds"] for ft in FOOTS)
            iii = III[f"{pl}|{ak(a)}"]
            gp = all(GR[f"{pl}|{ft}|{ak(a)}"]["pass_"] for ft in FOOTS)
            P(f"  {pl} alpha {ak(a)}: (i) {i_}  (ii) {ii}  (iii) {iii}  groups {gp}")
            if i_ and ii and iii == "PASS" and gp: works.append(a)
            elif i_ and (ii or iii in ("PASS", "REDUCED")): partial.append(a)
        lab = "WORKS" if works else ("PARTIAL" if partial else "DOES NOT")
        V[pl] = dict(label=lab, works_alpha=works, partial_alpha=partial)
        P(f"  -> {pl}: {('ONE-alpha PARTIAL SETTLING WORKS (alpha = ' + ', '.join(f'{x:g}' for x in works) + ')') if works else lab}"
          + (f"  [PARTIAL at alpha = {', '.join(f'{x:g}' for x in partial)}]" if partial and not works else ""))
    labs = [V[pl]["label"] for pl in PLS]
    overall = min(labs, key=lambda x: rank[x]); sens = labs[0] != labs[1]
    P(f"  OVERALL: {overall}{' (PLACEMENT-SENSITIVE: P0 ' + labs[0] + ', P2 ' + labs[1] + ')' if sens else ''}")
    res["verdict"] = dict(per_placement=V, overall=overall, placement_sensitive=bool(sens))
    res["runs"] = RUNS
    finish(res)


def mutate(res):
    teeth = {}
    P("\n=== MUTATE ===")
    # M1: alpha = 64 vs exact alpha -> inf (log 14, can, both placements)
    H = C.Host(14.0)
    for pl in PLS:
        R = C.Run(H, "can", pl); oi = R.run(math.inf); di = R.diag(oi["m"], XS)
        R2 = C.Run(H, "can", pl); t = time.time(); o6 = R2.run(64.0, maxsteps=20_000_000); d6 = R2.diag(o6["m"], XS)
        dF = max(abs(di["F_set"][k] - d6["F_set"][k]) for k in di["F_set"]); sr = d6["S"]["1.0"] / di["S"]["1.0"]
        ok = dF <= 0.03 and abs(sr - 1) <= 0.03 and not o6["hit_cap"]
        teeth[f"M1_{pl}"] = dict(max_dF=dF, S_ratio=sr, bites=bool(ok), runtime_s=time.time() - t, n=o6["n"])
        P(f"  M1 {pl}: alpha 64 vs exact inf: max |dF_set| {dF:.4f}, S(<r_ta) ratio {sr:.4f}, steps {o6['n']} -> {'BITES' if ok else 'FAILS'}")
    # M1b: census edge
    for lM in (12.0, 14.0):
        Hh = C.Host(lM)
        for ft in FOOTS:
            R = C.Run(Hh, ft, "P0"); R.set_baryons(1.0); R.thr = np.zeros(R.N)
            m = np.zeros(R.N); m[-1] = Hh.Mcat
            m = R.settle_inf(m, Hh.rta0 * 1.01)
            j = int(np.nonzero(m > 0)[0][-1])                          # last (partially) filled cell of the inside-out fill
            re = (R.rf[j] ** 3 + (m[j] / R.mph[j]) * (R.rf[j + 1] ** 3 - R.rf[j] ** 3)) ** (1 / 3)
            rM = math.sqrt(C.GK * Hh.Mb0 / C.A0K[ft]); rs = rM / math.log1p(Hh.Mb0 / Hh.Mcat)
            ok = abs(re / rs - 1) <= 0.01
            teeth[f"M1b_{lM}_{ft}"] = dict(r_edge_grid=re, r_star=rs, rel=re / rs - 1, bites=bool(ok))
            P(f"  M1b log {lM:g} {ft}: minimiser edge {re:.1f} kpc vs CFG541 r_M/ln(1+M_b/M_cat) {rs:.1f} kpc (rel {re / rs - 1:+.4f}) -> {'BITES' if ok else 'FAILS'}")
    teeth["M2_benchmark"] = dict(bites=res["M2_benchmark_bites"]); teeth["M2_ode"] = dict(bites=res["M2_ode"]["absdiff"] <= 1e-3)
    allb = all(v["bites"] for v in teeth.values())
    P(f"  all teeth bite: {allb}")
    res["teeth"] = teeth; res["all_teeth_bite"] = bool(allb)
    finish(res)
    sys.exit(1 if allb else 0)


def finish(res):
    def clean(o):
        if isinstance(o, dict): return {str(k): clean(v) for k, v in o.items()}
        if isinstance(o, (list, tuple)): return [clean(v) for v in o]
        if isinstance(o, (np.floating,)): return float(o)
        if isinstance(o, (np.integer,)): return int(o)
        if isinstance(o, np.bool_): return bool(o)
        if isinstance(o, float) and not math.isfinite(o): return str(o)
        return o
    json.dump(clean(res), open(os.path.join(HERE, f"cfg598_results{TAG}.json"), "w"), indent=1)
    open(os.path.join(HERE, f"cfg598_front{TAG}.out"), "w").write("\n".join(LINES) + "\n")


if __name__ == "__main__":
    main()
