#!/usr/bin/env python3
"""CFG781 (FROZEN_CRITERIA.md, 3028fcc80): phase-mixed free cold energy (Argon's rule) as a two-population model.
Tethered: law phantom of the CONDENSED baryons, cumulative min(phantom, S_t), S_t = 5.364 M_cond/0.10, to r_ta.
Free: M_free = 5.364 M_hot,tot, untethered, placed by CFG637 Method B (maxent_reservoir) at turnaround energy
E = -G (M_b + S_t + M_free)/r_ta * M_free, self-consistent in baryons + tethered + free.
Stages (CFG781_MODE): erass | accept | efeds | tk | score  (work files in ../_external_data/cfg781_work).  Run ONLY after T1x.
CFG781_MUTATE is a scoring flag only; the M1 (free = 0) and M2 (uniform placement) runs are computed in every stage.
kappa = 1/2 FITTED; cold energy mass required; no particle species; not theory closed."""
import os, sys, io, json, math, time, contextlib
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_v] = "1"
import warnings
warnings.filterwarnings("ignore", category=RuntimeWarning)
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__)); LANES = os.path.dirname(HERE); REPO = os.path.dirname(LANES)
EXT = os.path.abspath(os.path.join(REPO, "..", "_external_data"))
WORK = os.path.join(EXT, "cfg781_work")
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
MODE = os.environ.get("CFG781_MODE", "score")
MUT = os.environ.get("CFG781_MUTATE", "0") == "1"
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

FEET = ("canonical", "alt")
CASES = [("s", f, "P") for f in FEET] + [("mono", f, "P") for f in FEET] + [("s", "canonical", "M1"), ("s", "canonical", "M2")]
CPB = 5.364


def system781(r_obs, Mc, Mh, z, foot, kern, mode):
    """returns rg (= r_obs, kpc), Mb, Mteth, Mfree cumulative (Msun), meta."""
    a0 = A0SI[foot] * L.SI_TO_KPCGYR2
    Mc_tot, Mh_tot = float(Mc[-1]), float(Mh[-1])
    bc = max(Mc_tot / M652.F_COND_FLOOR, (Mc_tot + Mh_tot) / M652.F_RET_XCOP)
    M_ta = bc / L.FB
    rta = float(L.r_ta_single(M_ta, 1.0 / (1.0 + z))[0])
    S_t = CPB * Mc_tot / M652.F_COND_FLOOR
    gN = L.G * np.maximum(Mc, 1e-30) / r_obs ** 2
    ph = Mc * (KALL[kern](gN / a0) - 1.0)
    ph = np.maximum.accumulate(np.maximum(ph, 0.0))
    Mt = np.minimum(ph, S_t)
    Mt = np.where(r_obs <= rta, Mt, np.interp(rta, r_obs, Mt))
    Mf_tot = 0.0 if mode == "M1" else CPB * Mh_tot
    Mb = Mc + Mh
    ok = True
    if Mf_tot <= 0:
        Mf = np.zeros_like(r_obs)
    elif mode == "M2":
        Mf = Mf_tot * np.clip(r_obs / rta, 0, 1) ** 3
    else:
        E = -L.G * (Mb[-1] + S_t + Mf_tot) / rta * Mf_tot
        Mf, s2, Er, ok = L.maxent_reservoir(r_obs, Mb + Mt, Mf_tot, E, rta)
        if not np.all(np.isfinite(Mf)):
            Mf = Mf_tot * np.clip(r_obs / rta, 0, 1) ** 3; ok = False
    meta = dict(rta=rta, S_t=S_t, M_free=Mf_tot, free_over_teth=Mf_tot / max(float(Mt[-1]), 1e-30), mb_ok=bool(ok),
                edge_kpc=float(r_obs[np.argmax(ph >= S_t)]) if np.any(ph >= S_t) else float("inf"))
    return r_obs, Mb, Mt, Mf, meta


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



def cluster_runs(Mg_rgrid, fs, z, Rx_kpc):
    """harness gas M(<r) on RGRID (Mpc grid, Msun); condensed = fs * M_gas,tot placed as CFG652 (half BCG R_e 15 kpc,
    half members R_e 0.5 R_X); hot = the harness gas profile."""
    rk = RGRID * 1000.0
    mg = np.interp(R_OBS, rk, Mg_rgrid, left=0.0, right=Mg_rgrid[-1])
    Mc = M652.hern(R_OBS, 0.5 * fs * Mg_rgrid[-1], 15.0) + M652.hern(R_OBS, 0.5 * fs * Mg_rgrid[-1], 0.5 * Rx_kpc)
    out = {"M0": {}}
    MbR = np.interp(rk, R_OBS, Mc + mg)
    for kern in KERN:
        for foot in FEET:
            out["M0"][f"{kern}|{foot}"] = dsig_from_M(law_M(Mg_rgrid * (1 + fs), foot, kern))   # CFG687/686 reproduction control
    for kern, foot, mode in CASES:
        rg, Mb, Mt, Mf, meta = system781(R_OBS, Mc, mg, z, foot, kern, mode)
        tR = np.interp(rk, rg, Mt, left=0.0, right=Mt[-1]); fR = np.interp(rk, rg, Mf, left=0.0, right=Mf[-1])
        out[f"{kern}|{foot}|{mode}"] = dict(base=dsig_from_M(MbR + tR), res=dsig_from_M(fR) if Mf[-1] > 0 else np.zeros(8), meta=meta)
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
        o = cluster_runs(Mg, 0.20, float(d["z"][i]), R5 * 1000.0)
        res.append(o)
        if (i + 1) % 10 == 0:
            P(f"  eRASS1 {i + 1}/{len(d['mg'])} ({time.time() - T0:.0f} s); last (s, can): M_free/M_teth {o['s|canonical|P']['meta']['free_over_teth']:.2f}, MethodB ok {o['s|canonical|P']['meta']['mb_ok']}")
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
        Rx = 1000.0                                                     # declared: fixed point R_X = rx_of(M_gas(<R_X)) (ACCEPT has no R500 on record)
        for _ in range(30):
            Rx = float(rx_of(max(float(np.interp(Rx / 1000.0, RGRID, Mg)), 1e10))[0])
        o = cluster_runs(Mg, 0.20, zl, Rx); o["name"] = cl["name"]
        res.append(o)
        P(f"  ACCEPT {cl['name']}: R_X {Rx:.0f} kpc; M_free/M_teth (s, can) {o['s|canonical|P']['meta']['free_over_teth']:.2f}")
    np.save(os.path.join(WORK, "accept.npy"), np.array(res, dtype=object), allow_pickle=True)

# ============================================================================================ eFEDS (CFG652 inputs; same placement)
if MODE == "efeds":
    W652 = os.path.join(EXT, "cfg652_work")
    I0 = np.load(os.path.join(W652, "cfg652_inputs.npz"))
    RB = np.geomspace(30, 3000, 13); RCg = np.sqrt(RB[1:] * RB[:-1]); n = len(I0["z"])
    out = {}
    for kern, foot, mode in CASES:
        arr = np.full((n, len(RCg)), np.nan); okv = np.zeros(n, bool)
        for i in range(n):
            if I0["Mcond"][i] <= 0: continue
            Mc, Mh = M652.profiles(I0["Mcond"][i], I0["Mhot"][i], I0["Rx_kpc"][i], R_OBS, gas_trunc=2.0)
            rg, Mb, Mt, Mf, meta = system781(R_OBS, Mc, Mh, I0["z"][i], foot, kern, mode)
            arr[i] = M652.delta_sigma(rg, Mb + Mt + Mf, RCg, rmax=meta["rta"]); okv[i] = meta["mb_ok"]
        out[f"{kern}|{foot}|{mode}"] = arr; out[f"ok|{kern}|{foot}|{mode}"] = okv
        P(f"  eFEDS {kern} {foot} {mode} done; Method B converged {okv.sum()}/{(I0['Mcond'] > 0).sum()} ({time.time() - T0:.0f} s)")
    np.savez(os.path.join(WORK, "efeds_models.npz"), **{k.replace("|", "__"): v for k, v in out.items()})

# ============================================================================================ T-K KiDS early/late (CFG721 construction)
if MODE == "tk":
    out = []
    RK = np.array([50.0, 70.71, 100.0])
    for kern, foot, mode in CASES:
        a0 = A0SI[foot] * L.SI_TO_KPCGYR2
        for hfac in ((1.0, 0.25, 0.5, 2.0) if (kern, foot, mode) == ("s", "canonical", "P") else (1.0,)):
            for lm in (10.0, 10.5, 11.0, 11.5):
                Mbv = 10 ** lm; row = dict(kern=kern, foot=foot, mode=mode, h=hfac, lMb=lm)
                for typ, Mh_ in (("late", 0.0), ("early", hfac * Mbv)):
                    Rx, _ = rx_of(Mh_ if Mh_ > 0 else Mbv)
                    mc, mh = M652.profiles(Mbv, Mh_, Rx, R_OBS)
                    rg, Mb, Mt, Mf, meta = system781(R_OBS, mc, mh, 0.0, foot, kern, mode)
                    mod = M652.delta_sigma(rg, Mb + Mt + Mf, RK, rmax=meta["rta"])
                    gN = L.G * np.maximum(Mb, 0) / rg ** 2
                    law = M652.delta_sigma(rg, Mb * KALL[kern](gN / a0), RK, rmax=meta["rta"])
                    row[typ] = dict(mod=mod.tolist(), law=law.tolist(), free=meta["M_free"], edge=meta["edge_kpc"], ok=meta["mb_ok"])
                e, l_ = row["early"], row["late"]
                row["dOF"] = float(np.mean(np.log10(np.array(e["mod"]) / np.array(l_["mod"])) - np.log10(np.array(e["law"]) / np.array(l_["law"]))))
                out.append(row)
                P(f"  T-K {kern} {foot[:3]} {mode} h {hfac} lMb {lm}: dOF {row['dOF']:+.4f} (pred {-0.027 + row['dOF']:+.3f}); late edge {l_['edge']:.0f} kpc; early free {e['free']:.2e}")
    json.dump(C4.jclean(out), open(os.path.join(WORK, "tk.json"), "w"))


# ============================================================================================ score
if MODE == "score":
    from scipy.stats import chi2 as CHI2
    RES = {"lane": "CFG781", "criteria": "3028fcc80"}
    CHK = {}

    def check(name, ok, msg):
        CHK[name] = dict(ok=bool(ok), msg=msg); P(f"  [{'PASS' if ok else 'FAIL'}] {name}: {msg}")

    P(__doc__.split("Stages")[0].strip())
    key = lambda kern, foot, mode: f"{kern}|{foot}|{mode}"
    d = np.load(os.path.join(LANES, "CFG687_erass1_shear_stack", "cfg687_percluster.npz"))
    ER = list(np.load(os.path.join(WORK, "erass.npy"), allow_pickle=True))
    D, E = d["D"], d["E"]; W = np.where(E > 0, 1 / E ** 2, 0); n = len(D)
    order = np.argsort(d["ra"]); patch = np.empty(n, int); patch[order] = np.arange(n) * 30 // n
    BANDS = {"INNER": [0, 1, 2], "MID": [3, 4, 5], "OUTER": [6, 7]}
    A_of = lambda sel, Pm: {b: (W[sel][:, j] * D[sel][:, j]).sum() / (W[sel][:, j] * Pm[sel][:, j]).sum() for b, j in BANDS.items()}

    def jk(fun):
        full = fun(np.ones(n, bool)); reps = [fun(patch != p_) for p_ in range(30)]
        return {k: (float(full[k]), float(np.sqrt(29 / 30 * np.sum((np.array([r[k] for r in reps]) - np.mean([r[k] for r in reps])) ** 2)))) for k in full}
    rel = np.median(np.abs(np.array([o["M0"]["mono|canonical"] for o in ER]) / d["PL"] - 1), axis=0)
    check("M0 eRASS1 plain law reproduces CFG687 PL", rel.max() <= 0.01, f"max {rel.max():.2e}")
    mbok = np.mean([o[key(k_, f_, "P")]["meta"]["mb_ok"] for o in ER for k_ in KERN for f_ in FEET])
    check("K2 Method B converged >= 95% (eRASS1)", mbok >= 0.95, f"{100 * mbok:.1f}%")
    TR = {}
    P("\n== eRASS1 318 (jackknife 30): pass |A_MID-1| < 2 sig AND |A_OUTER-1| < 2 sig")
    for kern, foot, mode in CASES:
        k = key(kern, foot, mode)
        Ph = np.array([o[k]["base"] + o[k]["res"] for o in ER]); A = jk(lambda s_: A_of(s_, Ph))
        zm, zo = (A["MID"][0] - 1) / A["MID"][1], (A["OUTER"][0] - 1) / A["OUTER"][1]
        TR[k] = dict(A=A, Z_mid=zm, Z_outer=zo, pass_=bool(abs(zm) < 2 and abs(zo) < 2))
        P(f"  {k:20s}: A INNER {A['INNER'][0]:.2f}+-{A['INNER'][1]:.2f} MID {A['MID'][0]:.2f}+-{A['MID'][1]:.2f} (Z {zm:+.1f}) OUTER {A['OUTER'][0]:.2f}+-{A['OUTER'][1]:.2f} (Z {zo:+.1f}) -> {'PASS' if TR[k]['pass_'] else 'FAIL'}")
    m1 = abs(TR[key("s", "canonical", "M1")]["A"]["MID"][0] - TR[key("s", "canonical", "P")]["A"]["MID"][0])
    P(f"  MUTATE M1 (free = 0): MID changes by {m1:.3f} -> {'bites' if m1 >= 0.1 else 'DOES NOT BITE'}")
    RES["T_R"] = TR
    C686 = json.load(open(os.path.join(LANES, "CFG686_cluster_shear_vs_law", "cfg686_results.json")))
    cls = C686["clusters"]; AC = list(np.load(os.path.join(WORK, "accept.npy"), allow_pickle=True))
    D_ = np.nan_to_num(np.array([x["dsig"] for x in cls])); E_ = np.array([x["err"] for x in cls]); W_ = np.where(np.isfinite(E_) & (E_ > 0), 1 / E_ ** 2, 0)

    def bandA(Pm, sel):
        o_ = {}
        for b, j in BANDS.items():
            num = (W_[sel][:, j] * D_[sel][:, j]).sum(); den = (W_[sel][:, j] * Pm[sel][:, j]).sum(); o_[b] = num / den if den != 0 else np.nan
        return o_
    TA = {}
    P("\n== ACCEPT 8 (bootstrap 1000, seed 1); pass |A_OUTER-1| < 2 sig")
    for kern, foot, mode in CASES:
        k = key(kern, foot, mode); Pm = np.array([o[k]["base"] + o[k]["res"] for o in AC])
        A = bandA(Pm, np.arange(len(cls))); rb = np.random.default_rng(1)
        boots = [bandA(Pm, rb.integers(0, len(cls), len(cls))) for _ in range(1000)]
        sig = {b: float(np.nanstd([bb[b] for bb in boots])) for b in BANDS}; zo = (A["OUTER"] - 1) / sig["OUTER"]
        TA[k] = dict(A={b: [float(A[b]), sig[b]] for b in BANDS}, Z_outer=float(zo), pass_=bool(abs(zo) < 2))
        P(f"  {k:20s}: A INNER {A['INNER']:.2f} MID {A['MID']:.2f} OUTER {A['OUTER']:.2f}+-{sig['OUTER']:.2f} (Z {zo:+.1f}) -> {'PASS' if TA[k]['pass_'] else 'FAIL'}")
    RES["T_A"] = TA
    W652 = os.path.join(EXT, "cfg652_work")
    I0 = np.load(os.path.join(W652, "cfg652_inputs.npz")); D0 = np.load(os.path.join(W652, "cfg652_esd.npz")); EM = np.load(os.path.join(WORK, "efeds_models.npz"))
    keep = I0["Mcond"] > 0
    RB = np.geomspace(30, 3000, 13); RCg = np.sqrt(RB[1:] * RB[:-1]); USE = (RCg >= 50) & (RCg <= 1000); NPATCH = 30
    Dd = {k: (D0[k][keep] if k in ("WG", "WX", "WW", "NN", "pg") else D0[k]) for k in D0.files}

    def esd(sel_g, sel_r):
        Wg = Dd["WW"][sel_g].sum(0); Wr = Dd["rWW"][sel_r].sum(0)
        g = Dd["WG"][sel_g].sum(0) / np.where(Wg > 0, Wg, np.nan); r = Dd["rWG"][sel_r].sum(0) / np.where(Wr > 0, Wr, np.nan)
        boost = (Dd["NN"][sel_g].sum(0) / max(sel_g.sum(), 1)) / (Dd["rNN"][sel_r].sum(0) / max(sel_r.sum(), 1))
        return boost * g - r

    def model_stack(arr, sel_g):
        Wm = Dd["WW"][sel_g]
        return (Wm * arr[sel_g]).sum(0) / np.where(Wm.sum(0) > 0, Wm.sum(0), np.nan)
    allg = np.ones(int(keep.sum()), bool); allr = np.ones(len(Dd["rz"]), bool)
    vals = np.array([esd(Dd["pg"] != p_, Dd["pr"] != p_)[USE] for p_ in range(NPATCH)]); mv = vals.mean(0)
    C = (NPATCH - 1) / NPATCH * (vals - mv).T @ (vals - mv); nb = int(USE.sum()); Ci = np.linalg.inv(C) * (NPATCH - nb - 2) / (NPATCH - 1)
    obs = esd(allg, allr); TE = {}
    P("\n== eFEDS 131; pass chi2 p >= 0.01")
    for kern, foot, mode in CASES:
        k = key(kern, foot, mode); ms = model_stack(EM[k.replace("|", "__")][keep], allg); dd = obs[USE] - ms[USE]
        ch = float(dd @ Ci @ dd); pv = float(CHI2.sf(ch, nb)); TE[k] = dict(chi2=ch, p=pv, pass_=bool(pv >= 0.01))
        P(f"  {k:20s}: chi2 {ch:.1f}/{nb} p {pv:.3g} -> {'PASS' if pv >= 0.01 else 'FAIL'}")
    RES["T_E"] = TE
    TK = json.load(open(os.path.join(WORK, "tk.json"))); TKR = {}
    P("\n== KiDS early - late at matched M_b (obs +0.280 +- 0.083; pred = -0.027 + mean dOF)")
    for kern, foot, mode in CASES:
        for hfac in sorted({r["h"] for r in TK if (r["kern"], r["foot"], r["mode"]) == (kern, foot, mode)}):
            rows = [r for r in TK if (r["kern"], r["foot"], r["mode"], r["h"]) == (kern, foot, mode, hfac)]
            pred = -0.027 + float(np.mean([r["dOF"] for r in rows])); Z = (0.280 - pred) / 0.083
            TKR[f"{key(kern, foot, mode)}|h{hfac}"] = dict(pred=pred, Z=Z, pass_=bool(abs(Z) < 2))
            P(f"  {key(kern, foot, mode):20s} h {hfac}: pred {pred:+.3f} (Z {Z:+.2f}) -> {'PASS' if abs(Z) < 2 else 'FAIL'}")
    k1 = all(r["late"]["free"] == 0 for r in TK)
    check("K1 discs (M_hot = 0) carry no free mass", k1, "late types M_free = 0 in every T-K row")
    m2 = abs(TKR["s|canonical|M2|h1.0"]["pred"] - TKR["s|canonical|P|h1.0"]["pred"]) > 1e-3 and abs(TR[key("s", "canonical", "M2")]["A"]["MID"][0] - TR[key("s", "canonical", "P")]["A"]["MID"][0]) > 1e-3
    P(f"  MUTATE M2 (uniform placement): KiDS and eRASS1 MID change -> {'bites' if m2 else 'DOES NOT BITE'}")
    RES["T_K"] = TKR
    P("\n== VERDICT (nu_s; PASS = eRASS1 + ACCEPT + eFEDS + KiDS on >= 1 footing)")
    best = None
    for foot in FEET:
        k = key("s", foot, "P"); r4 = [TR[k]["pass_"], TA[k]["pass_"], TE[k]["pass_"], TKR[f"{k}|h1.0"]["pass_"]]
        P(f"  {foot}: eRASS1 {r4[0]}, ACCEPT {r4[1]}, eFEDS {r4[2]}, KiDS {r4[3]}")
        sc = (all(r4), all(r4[:3]) or r4[3])
        best = sc if best is None else (best[0] or sc[0], best[1] or sc[1])
    V = "PASS" if best[0] else ("PARTIAL" if best[1] else "FAIL")
    P(f"  -> {V}   (UFDs: M_hot = 0, no change predicted; declared expected FAIL of the UFD problem)")
    RES["verdict"] = V; RES["checks"] = CHK; RES["elapsed_s"] = round(time.time() - T0, 1)
    json.dump(C4.jclean(RES), open(os.path.join(HERE, "cfg781_results.json"), "w"), indent=1)
    open(os.path.join(HERE, "cfg781.out"), "w").write("\n".join(LOG) + "\n")

if MODE != "score":
    open(os.path.join(HERE, f"cfg781_{MODE}.log"), "w").write("\n".join(LOG) + f"\nelapsed {time.time() - T0:.0f} s\n")
