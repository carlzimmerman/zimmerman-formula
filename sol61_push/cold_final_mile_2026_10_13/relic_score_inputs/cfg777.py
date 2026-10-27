#!/usr/bin/env python3
"""CFG777 (FROZEN_CRITERIA.md, d934591f4): the frozen relic (H-FR) in groups and clusters. The tethered cold-energy profile is the law's
profile of the PEAK condensed mass p*M_cond (present-day baryons set the potential); catchment/supply from the peak condensed mass;
the rest of the supply is free, placed by CFG637 Method A. Only change from CFG721's condensed source: p.
Machinery: CFG721's (cfg637_lib.derive, cfg652_model profiles/delta_sigma, CFG686/687 projection, CFG721 scoring) copied verbatim
where unchanged. Stages (CFG777_MODE): erass | accept | efeds | score (work files in ../_external_data/cfg777_work, not committed).
Run ONLY after the CFG650 T1x job has finished:
  CFG777_MODE=<stage> OMP_NUM_THREADS=1 nice -n 10 python3 -u campaign_fresh_gravity/CFG777_relic_clusters/cfg777.py
CFG777_MUTATE=1 (score stage reads the same work files; M1 = the p = 1 runs vs CFG721 stored, M2 = per-cluster shuffled p).
kappa = 1/2 FITTED; cold energy mass required; no particle species; not theory closed."""

import os, sys, io, json, math, time, contextlib
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_v] = "1"
import warnings
warnings.filterwarnings("ignore", category=RuntimeWarning)
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__)); LANES = os.path.dirname(HERE); REPO = os.path.dirname(LANES)
EXT = os.path.abspath(os.path.join(REPO, "..", "_external_data"))
WORK = os.path.join(EXT, "cfg777_work")
W721 = os.path.join(EXT, "cfg721_work"); os.makedirs(WORK, exist_ok=True)
for d in (LANES, os.path.join(LANES, "CFG637_derived_reservoir"), os.path.join(LANES, "CFG652_hot_group_discriminator"),
          os.path.join(LANES, "CFG540_vizier2026_bfjr_mhongoose")):
    sys.path.insert(0, d)
try:
    os.nice(10)
except OSError:
    pass
import cfg637_lib as L                                              # noqa: E402
import CFG4_common as C4                                            # noqa: E402
with contextlib.redirect_stdout(io.StringIO()):
    import cfg652_model as M652                                     # noqa: E402
MODE = os.environ.get("CFG777_MODE", "score")
MUT = os.environ.get("CFG777_MUTATE", "0") == "1"
T0 = time.time(); LOG = []
N_SH = 600


def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); LOG.append(s)


def nu_s(y):                                                         # CFG695 / CFG720: g_N = g^2/(g + a0)
    y = np.maximum(np.asarray(y, float), 1e-300)
    return 0.5 + np.sqrt(0.25 + 1.0 / y)


KERN = {"mono": C4.nu_mono, "s": nu_s}
# ADDENDUM c5c6894a6 (H-OF2): tethered phantom capped at mean Sigma <= a0/(pi G)  <=>  (nu - 1) <= 1/y
KCAP = {k + "_cap": (lambda y, f=f: np.minimum(f(y), 1.0 + 1.0 / np.maximum(np.asarray(y, float), 1e-300))) for k, f in KERN.items()}
KALL = dict(KERN, **KCAP)
A0SI = {"canonical": C4.A0["canonical"], "alt": C4.A0["alt"]}
FEET = ("canonical", "alt")
# runs per system: primary (Tacconi p) x 2 kernels x 2 footings; brackets + M1 (p = 1) at nu_s / canonical; M1 also nu_mono canonical


def tacconi_p(z=1.5, lmstar=10.8):                                   # CFG776 D3 (coefficients PROVISIONAL, from memory)
    lmu = 0.12 - 3.62 * (math.log10(1 + z) - 0.66) ** 2 - 0.35 * (lmstar - 10.7)
    return (1 + 10 ** lmu) / 0.9


P_TAC = tacconi_p()
CASES = [("s", f, P_TAC) for f in FEET] + [("mono", f, P_TAC) for f in FEET] + [("s", "canonical", pb) for pb in (1.5, 2.0, 3.0, 1.0)] + [("mono", "canonical", 1.0)]


def run_system(r_obs, Mcond, Mhot, z, foot, kern, p, N=N_SH):
    """H-FR: phantom source = p * condensed profile; catchment from the peak condensed mass (CFG652 rule); potential = present baryons."""
    Mhot_tot = float(Mhot[-1]); Mc_tot = float(Mcond[-1])
    bc = max(p * Mc_tot / M652.F_COND_FLOOR, (Mc_tot + Mhot_tot) / M652.F_RET_XCOP)
    supply = M652.COLD_PER_B * bc; fret = (Mc_tot + Mhot_tot) / bc
    M_ta = bc / L.FB
    core = Mcond + Mhot
    I = L.derive(M_ta, fret, r_obs, core, p * Mcond, A0SI[foot] * L.SI_TO_KPCGYR2, KALL[kern], a_obs=1.0 / (1.0 + z), N=N)
    s = supply / I.supply_turned
    cons = abs(I.drawn + I.M_res_tot - I.supply_turned) / I.supply_turned
    meta = dict(rta=I.rta, x_edge=I.x_edge, supply=supply, fret=fret, M_ta=M_ta, res_frac=I.M_res_tot / I.supply_turned,
                settled_frac=I.drawn / I.supply_turned, cons=cons, turned=I.M_turned / M_ta, p=p)
    return I.rg, I.M_core_g, I.M_set_g * s, I.M_res_g * s, meta


def rx_of(Mhot):                                                     # eRASS1 catalogue Mgas500-R500 power law (aperture only), kpc
    d = np.load(os.path.join(LANES, "CFG687_erass1_shear_stack", "cfg687_percluster.npz"))
    p = np.polyfit(np.log10(d["mg"]), np.log10(d["R500"]), 1)
    return 1000.0 * 10 ** (p[0] * np.log10(Mhot) + p[1]), p


R_OBS = np.geomspace(0.5, 6e4, 900)



# ============================================================================================ cluster projection (CFG686/687 code)
G = 6.674e-11; MSUN = 1.989e30; MPC = 3.0857e22; KG = MSUN / (3.0857e16) ** 2
RGRID = np.logspace(-3, np.log10(30), 3000); U_GRID = np.linspace(0, 1, 4001)
EDGES = np.logspace(np.log10(0.15), np.log10(3.0), 9); RC = np.sqrt(EDGES[1:] * EDGES[:-1])


def sigma_proj(rhoL, r, R):                       # CFG686 RUN3, with a floor so a truncated density projects as zero beyond r_ta
    umax = np.arccosh(r[-1] / R); u = U_GRID * umax; rr = R * np.cosh(u)
    rho_u = np.exp(np.interp(np.log(rr), np.log(r), np.log(np.maximum(rhoL, 1e-300))))
    return 2 * np.trapz(rho_u * rr * MPC, u)


def dsig_from_M(ML_msun):
    """CFG687 law() projection for a cumulative mass on RGRID (Mpc grid, Msun) -> DeltaSigma at RC (Msun/pc^2)."""
    ML = ML_msun * MSUN; r = RGRID
    rhoL = np.gradient(ML, r * MPC) / (4 * np.pi * (r * MPC) ** 2)
    Sig = np.array([sigma_proj(rhoL, r, R) for R in RC])
    M2 = np.array([np.interp(R, r, ML) + np.trapz(4 * np.pi * (r[r > R] * MPC) ** 2 * rhoL[r > R] * (1 - np.sqrt(1 - (R / r[r > R]) ** 2)), r[r > R] * MPC) for R in RC])
    return (M2 / (np.pi * (RC * MPC) ** 2) - Sig) / KG


def law_M(Mb_msun, foot, kern):
    gb = G * Mb_msun * MSUN / (RGRID * MPC) ** 2
    return Mb_msun * KALL[kern](gb / A0SI[foot])


def cluster_runs(Mg_rgrid, fs, z, mc_override=None):
    """Mg_rgrid: harness gas M(<r) on RGRID (Msun). Condensed = fs * gas (CFG721 primary placement) unless overridden."""
    rk = RGRID * 1000.0
    mg = np.interp(R_OBS, rk, Mg_rgrid, left=0.0, right=Mg_rgrid[-1])
    out = {"M0": {}}
    Mb = Mg_rgrid * (1 + fs)
    for kern in KERN:
        for foot in FEET:
            out["M0"][f"{kern}|{foot}"] = dsig_from_M(law_M(Mb, foot, kern))           # plain law (CFG687/686 reproduction)
    mc = fs * mg if mc_override is None else mc_override
    for kern, foot, p in CASES:
        rg, Mcore, Mset, Mres, meta = run_system(R_OBS, mc, mg, z, foot, kern, p)
        setR = np.interp(rk, rg, Mset, left=0.0, right=Mset[-1])
        resR = np.interp(rk, rg, Mres, left=0.0, right=Mres[-1])
        out[f"{kern}|{foot}|p{p:.4f}"] = dict(base=dsig_from_M(Mb + setR), res=dsig_from_M(resR) if meta["res_frac"] > 0 else np.zeros(8), meta=meta)
    return out


# ============================================================================================ eRASS1 (CFG687)
if MODE == "erass":
    d = np.load(os.path.join(LANES, "CFG687_erass1_shear_stack", "cfg687_percluster.npz"))
    res = []
    for i in range(len(d["mg"])):
        R5, mgas = float(d["R500"][i]), float(d["mg"][i])
        r = RGRID; rc = 0.15 * R5; shape = (1 + (r / rc) ** 2) ** (-1.0); shape[r > 3.0] = 0      # beta = 2/3
        dm = 4 * np.pi * (r * MPC) ** 2 * shape; Mm = np.r_[0, np.cumsum(0.5 * (dm[1:] + dm[:-1]) * np.diff(r * MPC))]
        Mg = Mm * (mgas / np.interp(R5, r, Mm))                                                  # Msun (CFG687 normalisation)
        o = cluster_runs(Mg, 0.20, float(d["z"][i]))
        res.append(o)
        if (i + 1) % 10 == 0:
            P(f"  eRASS1 {i + 1}/{len(d['mg'])} ({time.time() - T0:.0f} s); last: free/supply at Tacconi p (s, can) {o[f's|canonical|p{P_TAC:.4f}']['meta']['res_frac']:.3f}")
            np.save(os.path.join(WORK, "erass_partial.npy"), np.array(res, dtype=object), allow_pickle=True)
    np.save(os.path.join(WORK, "erass.npy"), np.array(res, dtype=object), allow_pickle=True)


# ============================================================================================ ACCEPT (CFG686)
if MODE == "accept":
    from scipy.interpolate import PchipInterpolator
    c = 2.998e8; MP = 1.6726e-27
    zb = [0.510, 0.706, 0.934, 1.321, 1.484, 2.330]; DMr = [13.588, 17.351, 21.576, 27.601, 30.512, 38.988]   # CFG686 verbatim
    DHb = 21.863 + (21.863 - 19.455) / (0.706 - 0.510) * (0.510 - 0.295); DMb = np.sqrt(7.942 ** 3 / (0.295 * DHb))
    pch = PchipInterpolator(np.r_[0, 0.295, zb], np.r_[0, DMb, DMr]); RD = 101.54 / 0.70
    DM = lambda z: pch(np.minimum(np.asarray(z, float), 2.33)) * RD
    prof = {}
    for l in open(os.path.join(EXT, "cfg686_inputs", "accept", "all_profiles.dat")):
        if l.startswith("#"): continue
        p = l.split()
        try: prof.setdefault(p[0], []).append([float(x) for x in p[1:14]])
        except ValueError: pass
    C686 = json.load(open(os.path.join(LANES, "CFG686_cluster_shear_vs_law", "cfg686_results.json")))["clusters"]
    res = []
    for cl in C686:                                                 # CFG686 law_dsigma gas construction, verbatim (beta_shift 0)
        Pp = np.array(prof[cl["key"]]); Pp = Pp[np.argsort(Pp[:, 0])]; rin, rout, ne = Pp[:, 0], Pp[:, 1], Pp[:, 2]
        ok_ = ne > 0; rin, rout, ne = rin[ok_], rout[ok_], ne[ok_]
        zl = cl["z"]; zz = np.linspace(0, zl, 400); E = np.sqrt(0.3 * (1 + zz) ** 3 + 0.7); DA_acc = np.trapz(1 / E, zz) * c / (70e3 / MPC) / MPC / (1 + zl)
        q = (float(DM(zl)) / (1 + zl)) / DA_acc; rin, rout, ne = rin * q, rout * q, ne * q ** -0.5
        rm = 0.5 * (rin + rout); rho = 1.17 * MP * ne * 1e6
        half = rm >= np.exp(0.5 * (np.log(rm[0]) + np.log(rm[-1]))); b0 = -np.polyfit(np.log(rm[half]), np.log(rho[half]), 1)[0]
        flag = not (b0 >= 1.5); b = 2.0 if flag else b0
        r = RGRID; rho_g = np.interp(r, rm, rho, left=rho[0], right=np.nan)
        out_ = r > rm[-1]; rho_g[out_] = rho[-1] * (r[out_] / rm[-1]) ** (-b); rho_g[r > 3.0] = 0.0
        Mg = np.r_[0, np.cumsum(0.5 * (4 * np.pi * (r[1:] * MPC) ** 2 * rho_g[1:] + 4 * np.pi * (r[:-1] * MPC) ** 2 * rho_g[:-1]) * np.diff(r) * MPC)] / MSUN
        o = cluster_runs(Mg, 0.20, zl); o["name"] = cl["name"]
        res.append(o)
        P(f"  ACCEPT {cl['name']}: free/supply (s, can, Tacconi p) {o[f's|canonical|p{P_TAC:.4f}']['meta']['res_frac']:.3f}")
    np.save(os.path.join(WORK, "accept.npy"), np.array(res, dtype=object), allow_pickle=True)
# ============================================================================================ eFEDS (CFG652 model (a) with peak factor p)
def efeds_system(Mcond, Mhot, Rx, z, foot, kern, p, N=600):
    """cfg652_model.system, model (a), copied with the H-FR change only: source p*M_cond, catchment from p*M_cond (M652 convention:
    settled not rescaled, reservoir rescaled)."""
    r_obs = np.geomspace(0.5, 6e4, 900)
    Mc, Mh = M652.profiles(Mcond, Mhot, Rx, r_obs, gas_trunc=2.0)
    Mhot_tot = float(Mh[-1])
    bc = max(p * Mcond / M652.F_COND_FLOOR, (Mcond + Mhot_tot) / M652.F_RET_XCOP)
    supply = M652.COLD_PER_B * bc; fret = (Mcond + Mhot_tot) / bc
    M_ta = bc / L.FB
    I = L.derive(M_ta, fret, r_obs, Mc + Mh, p * Mc, M652.A0[foot], KALL[kern], a_obs=1.0 / (1.0 + z), N=N)
    s = supply / I.supply_turned
    Mbound = I.M_core_g + I.M_set_g + I.M_res_g * s
    return dict(rg=I.rg, Mbound=Mbound, rta=I.rta, res_frac=I.M_res_tot / I.supply_turned)


if MODE == "efeds":
    W652 = os.path.join(EXT, "cfg652_work")
    I0 = np.load(os.path.join(W652, "cfg652_inputs.npz"))
    RB = np.geomspace(30, 3000, 13); RCg = np.sqrt(RB[1:] * RB[:-1]); n = len(I0["z"])
    out = {}
    for kern, foot, p in CASES:
        arr = np.full((n, len(RCg)), np.nan); rf = np.full(n, np.nan)
        for i in range(n):
            if I0["Mcond"][i] <= 0: continue
            o = efeds_system(I0["Mcond"][i], I0["Mhot"][i], I0["Rx_kpc"][i], I0["z"][i], foot, kern, p)
            arr[i] = M652.delta_sigma(o["rg"], o["Mbound"], RCg, rmax=o["rta"]); rf[i] = o["res_frac"]
        out[f"{kern}|{foot}|p{p:.4f}"] = arr; out[f"rf|{kern}|{foot}|p{p:.4f}"] = rf
        P(f"  eFEDS {kern} {foot} p {p:.3f} done; median free/supply {np.nanmedian(rf):.3f} ({time.time() - T0:.0f} s)")
    np.savez(os.path.join(WORK, "efeds_models.npz"), **{k.replace("|", "__"): v for k, v in out.items()})

# ============================================================================================ score
if MODE == "score":
    from scipy.stats import chi2 as CHI2
    RES = {"lane": "CFG777", "criteria": "d934591f4", "p_tacconi": P_TAC, "mutate": MUT}
    CHK = {}

    def check(name, ok, msg):
        CHK[name] = dict(ok=bool(ok), msg=msg); P(f"  [{'PASS' if ok else 'FAIL'}] {name}: {msg}")

    P(__doc__.split("Stages")[0].strip())
    P(f"\nTacconi peak factor p = {P_TAC:.4f} (provisional coefficients)")
    key = lambda kern, foot, p: f"{kern}|{foot}|p{p:.4f}"
    # ---------------- eRASS1
    d = np.load(os.path.join(LANES, "CFG687_erass1_shear_stack", "cfg687_percluster.npz"))
    ER = list(np.load(os.path.join(WORK, "erass.npy"), allow_pickle=True))
    D, E = d["D"], d["E"]; W = np.where(E > 0, 1 / E ** 2, 0); n = len(D)
    order = np.argsort(d["ra"]); patch = np.empty(n, int); patch[order] = np.arange(n) * 30 // n
    BANDS = {"INNER": [0, 1, 2], "MID": [3, 4, 5], "OUTER": [6, 7]}

    def A_of(sel, Pm):
        return {b: (W[sel][:, j] * D[sel][:, j]).sum() / (W[sel][:, j] * Pm[sel][:, j]).sum() for b, j in BANDS.items()}

    def jk(fun):
        full = fun(np.ones(n, bool)); reps = [fun(patch != p_) for p_ in range(30)]
        return {k: (float(full[k]), float(np.sqrt(29 / 30 * np.sum((np.array([r[k] for r in reps]) - np.mean([r[k] for r in reps])) ** 2)))) for k in full}

    PM0 = np.array([o["M0"]["mono|canonical"] for o in ER])
    rel = np.median(np.abs(PM0 / d["PL"] - 1), axis=0)
    check("M0 eRASS1: plain law reproduces CFG687 PL (median per-bin <= 1%)", rel.max() <= 0.01, f"max {rel.max():.2e}")
    ER721 = list(np.load(os.path.join(W721, "erass.npy"), allow_pickle=True))
    TR = {}
    P("\n== eRASS1 318: A = obs / model (jackknife 30); pass |A_MID-1| < 2 sig AND |A_OUTER-1| < 2 sig")
    for kern, foot, p in CASES:
        k = key(kern, foot, p)
        Ph = np.array([o[k]["base"] + o[k]["res"] for o in ER])
        A = jk(lambda s: A_of(s, Ph))
        zm, zo = (A["MID"][0] - 1) / A["MID"][1], (A["OUTER"][0] - 1) / A["OUTER"][1]
        rf = np.array([o[k]["meta"]["res_frac"] for o in ER])
        TR[k] = dict(A=A, Z_mid=zm, Z_outer=zo, pass_=bool(abs(zm) < 2 and abs(zo) < 2), free_median=float(np.median(rf)))
        P(f"  {kern:4s} {foot[:3]} p {p:.3f}: free/supply {np.median(rf):.3f}; A INNER {A['INNER'][0]:.2f}+-{A['INNER'][1]:.2f} MID {A['MID'][0]:.2f}+-{A['MID'][1]:.2f} "
          f"(Z {zm:+.1f}) OUTER {A['OUTER'][0]:.2f}+-{A['OUTER'][1]:.2f} (Z {zo:+.1f}) -> {'PASS' if TR[k]['pass_'] else 'FAIL'}")
    # M1: p = 1 vs CFG721 cond
    m1 = []
    for kern in ("s", "mono"):
        P1 = np.array([o[key(kern, "canonical", 1.0)]["base"] + o[key(kern, "canonical", 1.0)]["res"] for o in ER])
        P7 = np.array([o[f"{kern}|canonical|cond"]["base"] + o[f"{kern}|canonical|cond"]["res"] for o in ER721])
        A1, A7 = A_of(np.ones(n, bool), P1), A_of(np.ones(n, bool), P7)
        m1.append(max(abs(A1[b] - A7[b]) for b in BANDS))
    check("M1 eRASS1: p = 1 reproduces CFG721's condensed source (band A within 0.01)", max(m1) <= 0.01, f"max |dA| {max(m1):.4f}")
    # M2: per-cluster shuffled p in {1.5, 3}
    rng = np.random.default_rng(777); pick = rng.integers(0, 2, n)
    Psh = np.array([(ER[i][key("s", "canonical", 1.5)] if pick[i] == 0 else ER[i][key("s", "canonical", 3.0)]) for i in range(n)])
    Psh = np.array([x["base"] + x["res"] for x in Psh])
    Ash = A_of(np.ones(n, bool), Psh); Ap = A_of(np.ones(n, bool), np.array([o[key("s", "canonical", P_TAC)]["base"] + o[key("s", "canonical", P_TAC)]["res"] for o in ER]))
    P(f"  M2 shuffled p: A MID {Ash['MID']:.3f} vs Tacconi {Ap['MID']:.3f}; OUTER {Ash['OUTER']:.3f} vs {Ap['OUTER']:.3f} -> "
      f"{'changes (bites)' if abs(Ash['MID'] - Ap['MID']) > 1e-3 else 'NO CHANGE'}")
    RES["T_R"] = TR
    # ---------------- ACCEPT
    C686 = json.load(open(os.path.join(LANES, "CFG686_cluster_shear_vs_law", "cfg686_results.json")))
    cls = C686["clusters"]; AC = list(np.load(os.path.join(WORK, "accept.npy"), allow_pickle=True))
    D_ = np.nan_to_num(np.array([x["dsig"] for x in cls])); E_ = np.array([x["err"] for x in cls]); W_ = np.where(np.isfinite(E_) & (E_ > 0), 1 / E_ ** 2, 0)

    def bandA(Pm, sel):
        o_ = {}
        for b, j in BANDS.items():
            num = (W_[sel][:, j] * D_[sel][:, j]).sum(); den = (W_[sel][:, j] * Pm[sel][:, j]).sum(); o_[b] = num / den if den != 0 else np.nan
        return o_
    worst = 0.0
    for foot in FEET:
        PM = np.array([o["M0"][f"mono|{foot}"] for o in AC]); PS = np.array([x["pred"][f"{foot}|b+0.0|f0.20"] for x in cls])
        worst = max(worst, float(np.max(np.abs(PM / PS - 1))))
    check("M0 ACCEPT: plain law reproduces CFG686 (<= 1% every bin)", worst <= 0.01, f"max |rel| {worst:.2e}")
    TA = {}
    P("\n== ACCEPT 8 (bootstrap 1000, seed 1); pass |A_OUTER-1| < 2 sig (criteria: outer)")
    for kern, foot, p in CASES:
        k = key(kern, foot, p)
        Pm = np.array([o[k]["base"] + o[k]["res"] for o in AC])
        A = bandA(Pm, np.arange(len(cls))); rb = np.random.default_rng(1)
        boots = [bandA(Pm, rb.integers(0, len(cls), len(cls))) for _ in range(1000)]
        sig = {b: float(np.nanstd([bb[b] for bb in boots])) for b in BANDS}
        zo = (A["OUTER"] - 1) / sig["OUTER"]
        TA[k] = dict(A={b: [float(A[b]), sig[b]] for b in BANDS}, Z_outer=float(zo), pass_=bool(abs(zo) < 2))
        P(f"  {kern:4s} {foot[:3]} p {p:.3f}: A INNER {A['INNER']:.2f}+-{sig['INNER']:.2f} MID {A['MID']:.2f}+-{sig['MID']:.2f} OUTER {A['OUTER']:.2f}+-{sig['OUTER']:.2f} "
          f"(Z {zo:+.1f}) -> {'PASS' if TA[k]['pass_'] else 'FAIL'}")
    RES["T_A"] = TA
    # ---------------- eFEDS (CFG652 score code, as in CFG721)
    W652 = os.path.join(EXT, "cfg652_work")
    I0 = np.load(os.path.join(W652, "cfg652_inputs.npz")); D0 = np.load(os.path.join(W652, "cfg652_esd.npz"))
    EM = np.load(os.path.join(WORK, "efeds_models.npz")); EM7 = np.load(os.path.join(W721, "efeds_models.npz"))
    keep = I0["Mcond"] > 0
    RB = np.geomspace(30, 3000, 13); RCg = np.sqrt(RB[1:] * RB[:-1])
    USE = (RCg >= 50) & (RCg <= 1000); NPATCH = 30
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
    vals = np.array([esd(Dd["pg"] != p_, Dd["pr"] != p_)[USE] for p_ in range(NPATCH)]); mv = vals.mean(0)
    C = (NPATCH - 1) / NPATCH * (vals - mv).T @ (vals - mv)
    nb = int(USE.sum()); hart = (NPATCH - nb - 2) / (NPATCH - 1); Ci = np.linalg.inv(C) * hart
    obs = esd(allg, allr)
    m1e = max(float(np.nanmax(np.abs(EM[f"{kern}__canonical__p1.0000"][keep] / EM7[f"{kern}__canonical__cond"][keep] - 1))) for kern in ("s", "mono"))
    check("M1 eFEDS: p = 1 reproduces CFG721's condensed models (<= 1% every group and bin)", m1e <= 0.01, f"max |rel| {m1e:.2e}")
    TE = {}
    P("\n== eFEDS 131 groups; pass chi2 p >= 0.01")
    for kern, foot, p in CASES:
        k = key(kern, foot, p)
        arr = EM[k.replace("|", "__")][keep]; ms = model_stack(arr, allg); dd = obs[USE] - ms[USE]
        ch = float(dd @ Ci @ dd); pv = float(CHI2.sf(ch, nb))
        TE[k] = dict(chi2=ch, p=pv, pass_=bool(pv >= 0.01))
        P(f"  {kern:4s} {foot[:3]} p {p:.3f}: chi2 {ch:.1f}/{nb} p {pv:.3g} -> {'PASS' if pv >= 0.01 else 'FAIL'}")
    RES["T_E"] = TE
    # ---------------- verdict
    P("\n== VERDICT at the Tacconi p (PASS = eRASS1 + ACCEPT + eFEDS on >= 1 footing; PARTIAL = two of three)")
    V = {}
    for kern in KERN:
        best = 0
        for foot in FEET:
            k = key(kern, foot, P_TAC)
            best = max(best, sum([TR[k]["pass_"], TA[k]["pass_"], TE[k]["pass_"]]))
        V[kern] = "PASS" if best == 3 else ("PARTIAL" if best == 2 else "FAIL")
        P(f"  kernel {kern}: {V[kern]} (best footing passes {best}/3)")
    RES["verdict"] = V; RES["checks"] = CHK; RES["elapsed_s"] = round(time.time() - T0, 1)
    nf = sum(1 for c in CHK.values() if not c["ok"])
    P(f"\n{len(CHK) - nf}/{len(CHK)} checks pass. kappa fitted; cold energy mass required; not theory closed.")
    json.dump(C4.jclean(RES), open(os.path.join(HERE, "cfg777_results.json"), "w"), indent=1)
    open(os.path.join(HERE, "cfg777.out"), "w").write("\n".join(LOG) + "\n")
    sys.exit(1 if nf else 0)

if MODE != "score":
    open(os.path.join(HERE, f"cfg777_{MODE}.log"), "w").write("\n".join(LOG) + f"\nelapsed {time.time() - T0:.0f} s\n")
