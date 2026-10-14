#!/usr/bin/env python3
"""CFG721 (FROZEN_CRITERIA.md, 93d53f734): SUPPLY OVERFLOW (H-OF). The settled phantom (the law's round phantom of the source, cut at
the supply edge, confined to r_ta) has a finite capacity; the system's cold-energy supply is 5.364 x its catchment baryons; whatever
the phantom cannot hold stays as collisionless cold energy placed by infall (= CFG637 Method A's reservoir). POST-HOC: every target
was already seen.
Machinery: cfg637_lib.derive (unchanged) wrapped as cfg652_model.system (catchment rule, supply, f_ret, M_ta, gate rescale).
Sources: 'all' (all retained baryons) / 'cond' (condensed only). Kernels: nu_mono (CFG4_common) / nu_s (CFG695). Footings never pooled.
Stages (CFG721_MODE): ladder | tk | erass | accept | efeds | score   (work files in ../_external_data/cfg721_work, not committed)
Run from the repository root, one stage at a time:
  CFG721_MODE=<stage> OMP_NUM_THREADS=1 nice -n 10 python3 -u campaign_fresh_gravity/CFG721_supply_overflow/cfg721.py
kappa = 1/2 FITTED; cold energy mass required; no particle species; not theory closed."""
import os, sys, io, json, math, time, contextlib
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_v] = "1"
import warnings
warnings.filterwarnings("ignore", category=RuntimeWarning)
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__)); LANES = os.path.dirname(HERE); REPO = os.path.dirname(LANES)
EXT = os.path.abspath(os.path.join(REPO, "..", "_external_data"))
WORK = os.path.join(EXT, "cfg721_work"); os.makedirs(WORK, exist_ok=True)
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
MODE = os.environ.get("CFG721_MODE", "score")
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
FEET = ("canonical", "alt"); SRCS = ("all", "cond")


def run_system(r_obs, Mcond, Mhot, z, foot, kern, src, N=N_SH, rule="max"):
    """cfg652_model.system with arbitrary cumulative profiles (kpc, Msun). Returns rg (kpc), Mcore, Mset, Mres (gate units), meta."""
    Mhot_tot = float(Mhot[-1]); Mc_tot = float(Mcond[-1])
    bc, supply, fret = M652.catchment(Mc_tot, Mhot_tot, rule)
    M_ta = bc / L.FB
    core = Mcond + Mhot
    srcp = core if src == "all" else Mcond
    I = L.derive(M_ta, fret, r_obs, core, srcp, A0SI[foot] * L.SI_TO_KPCGYR2, KALL[kern], a_obs=1.0 / (1.0 + z), N=N)
    s = supply / I.supply_turned
    cons = abs(I.drawn + I.M_res_tot - I.supply_turned) / I.supply_turned
    meta = dict(rta=I.rta, x_edge=I.x_edge, supply=supply, fret=fret, M_ta=M_ta, res_frac=I.M_res_tot / I.supply_turned,
                settled_frac=I.drawn / I.supply_turned, cons=cons, turned=I.M_turned / M_ta)
    return I.rg, I.M_core_g, I.M_set_g * s, I.M_res_g * s, meta


def rx_of(Mhot):                                                     # eRASS1 catalogue Mgas500-R500 power law (aperture only), kpc
    d = np.load(os.path.join(LANES, "CFG687_erass1_shear_stack", "cfg687_percluster.npz"))
    p = np.polyfit(np.log10(d["mg"]), np.log10(d["R500"]), 1)
    return 1000.0 * 10 ** (p[0] * np.log10(Mhot) + p[1]), p


R_OBS = np.geomspace(0.5, 6e4, 900)


# ============================================================================================ D1 ladder
if MODE == "ladder":
    LM = np.arange(9.0, 15.01, 0.5); FC = {"cond": (1.0, 0.5, 0.25, 0.1, 0.05), "all": (1.0, 0.1)}
    out = []
    for z in (0.0, 0.3):
        for kern in KERN:
            for foot in FEET:
                for src in SRCS:
                    for fc in FC[src]:
                        for lm in LM:
                            Mb = 10 ** lm; Mc = fc * Mb; Mh = (1 - fc) * Mb
                            Rx, _ = rx_of(Mh if Mh > 0 else Mb)
                            mc, mh = M652.profiles(Mc, Mh, Rx, R_OBS)
                            rg, Mcore, Mset, Mres, meta = run_system(R_OBS, mc, mh, z, foot, kern, src)
                            a0 = A0SI[foot] * L.SI_TO_KPCGYR2
                            msrc = Mb if src == "all" else Mc
                            cap = math.sqrt(msrc * a0 / L.G) * meta["rta"]          # deep-regime capacity at r_ta (Msun)
                            redge = (meta["x_edge"] * meta["rta"]) if meta["x_edge"] is not None else meta["rta"]
                            out.append(dict(z=z, kern=kern, foot=foot, src=src, fcond=fc, lMb=float(lm), Rx=float(Rx),
                                            cap_over_supply=cap / meta["supply"], r_edge_kpc=float(redge), **meta))
                            P(f"  ladder z{z} {kern} {foot[:3]} {src} fc {fc:.2f} lMb {lm:.1f}: res/supply {meta['res_frac']:.4f} "
                              f"edge {redge:.0f} kpc r_ta {meta['rta']:.0f} cap/supply {cap / meta['supply']:.3f} ({time.time() - T0:.0f} s)")
    json.dump(C4.jclean(out), open(os.path.join(WORK, "ladder.json"), "w"))

# ============================================================================================ T-K KiDS early/late pairs
if MODE in ("tk", "hof2"):
    out = []
    RK = np.array([50.0, 70.71, 100.0])
    for kern in (KERN if MODE == "tk" else KCAP):
        for foot in FEET:
            a0 = A0SI[foot] * L.SI_TO_KPCGYR2
            for src in SRCS:
                for lm in (10.0, 10.5, 11.0, 11.5):
                    Mb = 10 ** lm; row = dict(kern=kern, foot=foot, src=src, lMb=lm)
                    for typ, Mh in (("late", 0.0), ("early", Mb)):
                        Rx, _ = rx_of(Mh if Mh > 0 else Mb)
                        mc, mh = M652.profiles(Mb, Mh, Rx, R_OBS)
                        rg, Mcore, Mset, Mres, meta = run_system(R_OBS, mc, mh, 0.0, foot, kern, src)
                        hof = M652.delta_sigma(rg, Mcore + Mset + Mres, RK, rmax=meta["rta"])
                        gN = L.G * np.maximum(Mcore, 0) / rg ** 2                       # plain law: uncut all-baryon phantom to r_ta
                        law = Mcore * KALL[kern.replace("_cap", "")](gN / a0)
                        lawds = M652.delta_sigma(rg, law, RK, rmax=meta["rta"])
                        row[typ] = dict(hof=hof.tolist(), law=lawds.tolist(), res_frac=meta["res_frac"], x_edge=meta["x_edge"], rta=meta["rta"])
                    e, l_ = row["early"], row["late"]
                    row["dOF"] = float(np.mean(np.log10(np.array(e["hof"]) / np.array(l_["hof"])) - np.log10(np.array(e["law"]) / np.array(l_["law"]))))
                    out.append(row)
                    P(f"  T-K {kern} {foot[:3]} {src} lMb {lm}: res early {e['res_frac']:.4f} late {l_['res_frac']:.4f} dOF {row['dOF']:+.4f}")
    json.dump(C4.jclean(out), open(os.path.join(WORK, "tk.json" if MODE == "tk" else "tk_hof2.json"), "w"))

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


def cluster_runs(Mg_rgrid, fs, z, tag, cond_alt=None, kerns=None, feet=FEET):
    """Mg_rgrid: harness gas M(<r) on RGRID (Msun). Returns dict of components per (kern, foot, src)."""
    rk = RGRID * 1000.0
    mg = np.interp(R_OBS, rk, Mg_rgrid, left=0.0, right=Mg_rgrid[-1])
    out = {"base_law": {}, "M0": {}}
    Mb = Mg_rgrid * (1 + fs)
    for kern in (kerns or KERN):
        for foot in feet:
            out["M0"][f"{kern}|{foot}"] = dsig_from_M(law_M(Mb, foot, kern))           # overflow x0, phantom uncut: plain law
            for src in SRCS:
                mc = fs * mg if cond_alt is None else cond_alt
                rg, Mcore, Mset, Mres, meta = run_system(R_OBS, mc, mg, z, foot, kern, src)
                setR = np.interp(rk, rg, Mset, left=0.0, right=Mset[-1])
                resR = np.interp(rk, rg, Mres, left=0.0, right=Mres[-1])
                out[f"{kern}|{foot}|{src}"] = dict(base=dsig_from_M(Mb + setR), res=dsig_from_M(resR) if meta["res_frac"] > 0 else np.zeros(8),
                                                   meta=meta)
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
        o = cluster_runs(Mg, 0.20, float(d["z"][i]), "erass")
        if os.environ.get("CFG721_BRACKET", "1") == "1":                                          # reported bracket: condensed as CFG652
            rx = R5 * 1000.0; mcb = M652.hern(R_OBS, 0.5 * 0.2 * Mg[-1], 15.0) + M652.hern(R_OBS, 0.5 * 0.2 * Mg[-1], 0.5 * rx)
            rk = RGRID * 1000.0; mgk = np.interp(R_OBS, rk, Mg, left=0.0, right=Mg[-1])
            rg, Mcore, Mset, Mres, meta = run_system(R_OBS, mcb, mgk, float(d["z"][i]), "canonical", "mono", "cond")
            MbR = np.interp(rk, R_OBS, mcb + mgk)
            o["bracket_cond_bcg"] = dict(base=dsig_from_M(MbR + np.interp(rk, rg, Mset, left=0, right=Mset[-1])),
                                         res=dsig_from_M(np.interp(rk, rg, Mres, left=0, right=Mres[-1])), meta=meta)
        res.append(o)
        if (i + 1) % 10 == 0:
            P(f"  eRASS1 {i + 1}/{len(d['mg'])} ({time.time() - T0:.0f} s); last: cond res/supply "
              f"{o['mono|canonical|cond']['meta']['res_frac']:.3f}, all {o['mono|canonical|all']['meta']['res_frac']:.3f}")
            np.save(os.path.join(WORK, "erass_partial.npy"), np.array(res, dtype=object), allow_pickle=True)
    np.save(os.path.join(WORK, "erass.npy"), np.array(res, dtype=object), allow_pickle=True)

# ============================================================================================ ACCEPT (CFG686)
if MODE in ("accept", "hof2"):
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
        o = cluster_runs(Mg, 0.20, zl, "accept", kerns=(None if MODE == "accept" else KCAP)); o["name"] = cl["name"]
        res.append(o)
        kk = "mono" if MODE == "accept" else "mono_cap"
        P(f"  ACCEPT {cl['name']}: cond res/supply {o[kk + '|canonical|cond']['meta']['res_frac']:.3f}, all {o[kk + '|canonical|all']['meta']['res_frac']:.3f}")
    np.save(os.path.join(WORK, "accept.npy" if MODE == "accept" else "accept_hof2.npy"), np.array(res, dtype=object), allow_pickle=True)

# ============================================================================================ H-OF2 on 20 eRASS1 clusters (addendum)
if MODE == "hof2":
    d = np.load(os.path.join(LANES, "CFG687_erass1_shear_stack", "cfg687_percluster.npz"))
    res = []
    for i in range(20):
        R5, mgas = float(d["R500"][i]), float(d["mg"][i])
        r = RGRID; rc = 0.15 * R5; shape = (1 + (r / rc) ** 2) ** (-1.0); shape[r > 3.0] = 0
        dm = 4 * np.pi * (r * MPC) ** 2 * shape; Mm = np.r_[0, np.cumsum(0.5 * (dm[1:] + dm[:-1]) * np.diff(r * MPC))]
        Mg = Mm * (mgas / np.interp(R5, r, Mm))
        res.append(cluster_runs(Mg, 0.20, float(d["z"][i]), "erass", kerns=KCAP, feet=("canonical",)))
    np.save(os.path.join(WORK, "erass20_hof2.npy"), np.array(res, dtype=object), allow_pickle=True)
    P(f"  H-OF2 eRASS1 20 done ({time.time() - T0:.0f} s)")

# ============================================================================================ eFEDS (CFG652 models, kernel swapped)
if MODE == "efeds":
    W652 = os.path.join(EXT, "cfg652_work")
    I = np.load(os.path.join(W652, "cfg652_inputs.npz"))
    RB = np.geomspace(30, 3000, 13); RCg = np.sqrt(RB[1:] * RB[:-1]); n = len(I["z"])
    out = {}
    nu652 = M652.NU
    # M0 reproduction of cfg652_models.npz (canonical x1, both models, CFG652's own kernel)
    for model in "ab":
        arr = np.full((n, len(RCg)), np.nan)
        for i in range(n):
            if I["Mcond"][i] <= 0: continue
            M652.NU = nu652
            o = M652.system(I["Mcond"][i], I["Mhot"][i], I["Rx_kpc"][i], I["z"][i], "canonical", model, N=600, gas_trunc=2.0)
            arr[i] = M652.delta_sigma(o["rg"], o["Mbound"], RCg, rmax=o["rta"])
        out[f"M0repro|{model}"] = arr
        P(f"  eFEDS M0 reproduction model {model} done ({time.time() - T0:.0f} s)")
    for kern in KERN:
        for foot in FEET:
            for src, model in (("all", "b"), ("cond", "a")):
                arr = np.full((n, len(RCg)), np.nan); rf = np.full(n, np.nan)
                for i in range(n):
                    if I["Mcond"][i] <= 0: continue
                    M652.NU = KERN[kern]
                    o = M652.system(I["Mcond"][i], I["Mhot"][i], I["Rx_kpc"][i], I["z"][i], foot, model, N=600, gas_trunc=2.0)
                    arr[i] = M652.delta_sigma(o["rg"], o["Mbound"], RCg, rmax=o["rta"]); rf[i] = o["res_frac"]
                out[f"{kern}|{foot}|{src}"] = arr; out[f"rf|{kern}|{foot}|{src}"] = rf
                P(f"  eFEDS {kern} {foot} {src} done; median res/supply {np.nanmedian(rf):.3f} ({time.time() - T0:.0f} s)")
    M652.NU = nu652
    np.savez(os.path.join(WORK, "efeds_models.npz"), **{k.replace("|", "__"): v for k, v in out.items()})

# ============================================================================================ score
if MODE == "score":
    from scipy.stats import chi2 as CHI2
    RES = {"lane": "CFG721", "criteria": "93d53f734", "post_hoc": True}
    CHK = {}

    def check(name, ok, msg):
        CHK[name] = dict(ok=bool(ok), msg=msg); P(f"  [{'PASS' if ok else 'FAIL'}] {name}: {msg}")

    P(__doc__.split("Stages")[0].strip())
    # ---------------- D1 ladder
    LAD = json.load(open(os.path.join(WORK, "ladder.json")))
    P("\n== D1 threshold ladder: reservoir/supply (overflow fraction) vs M_b (z = 0 primary; z = 0.3 reported)")
    THR = {}
    for z in (0.0, 0.3):
        for kern in KERN:
            for foot in FEET:
                for src in SRCS:
                    for fc in sorted({r["fcond"] for r in LAD if r["src"] == src}, reverse=True):
                        rows = sorted([r for r in LAD if r["z"] == z and r["kern"] == kern and r["foot"] == foot and r["src"] == src and r["fcond"] == fc],
                                      key=lambda r: r["lMb"])
                        lm = np.array([r["lMb"] for r in rows]); rfv = np.array([r["res_frac"] for r in rows])
                        k = np.where(rfv >= 0.01)[0]
                        if not len(k):
                            thr = None
                        elif k[0] == 0:
                            thr = float(lm[0])
                        else:
                            j = k[0]; a, b = rfv[j - 1], rfv[j]
                            thr = float(lm[j - 1] + (lm[j] - lm[j - 1]) * (0.01 - a) / (b - a))
                        key = f"z{z}|{kern}|{foot}|{src}|fc{fc}"
                        THR[key] = dict(lMb_OF=thr, res_frac=rfv.tolist(), lMb=lm.tolist(), cap_over_supply=[r["cap_over_supply"] for r in rows],
                                        r_edge_kpc=[r["r_edge_kpc"] for r in rows])
                        P(f"  {key}: log M_b,OF = {('> 15 (never overflows)' if thr is None else f'{thr:.2f}')}; res/supply "
                          + " ".join(f"{x:.2f}" for x in rfv) + " | cap/supply " + " ".join(f"{r['cap_over_supply']:.2f}" for r in rows))
    RES["D1"] = THR
    c1 = max(r["cons"] for r in LAD)
    check("C1 supply = settled + reservoir (ladder)", c1 < 1e-9, f"max rel {c1:.1e}")
    # ladder M-SHUF: permuting res/supply across masses destroys the monotone onset
    rng = np.random.default_rng(721)
    mono = {k: bool(np.all(np.diff(np.array(v["res_frac"])) >= -0.02)) for k, v in THR.items() if v["lMb_OF"] is not None}
    shuf = {k: bool(np.all(np.diff(rng.permutation(np.array(THR[k]["res_frac"]))) >= -0.02)) for k in mono}
    RES["D1_MSHUF"] = dict(monotone_onset=mono, monotone_after_shuffle=shuf)
    P(f"  ladder M-SHUF (reported): cells with an onset {len(mono)}, monotone {sum(mono.values())}, still monotone after shuffle {sum(shuf.values())}")

    # ---------------- T-S SPARC guard
    bad = [r for r in LAD if r["fcond"] == 1.0 and r["lMb"] <= 12.0 and r["z"] == 0.0 and (r["res_frac"] > 0 or r["r_edge_kpc"] <= 108.31)]
    minedge = min(r["r_edge_kpc"] for r in LAD if r["fcond"] == 1.0 and r["lMb"] <= 12.0 and r["z"] == 0.0)
    TS = dict(n_bad=len(bad), min_edge_kpc=minedge, max_res=max(r["res_frac"] for r in LAD if r["fcond"] == 1.0 and r["lMb"] <= 12.0 and r["z"] == 0.0),
              verdict="PASS" if not bad else "FAIL (not verified)")
    RES["T_S"] = TS
    P(f"\n== T-S SPARC guard: max reservoir/supply {TS['max_res']:.4f}, min edge {minedge:.0f} kpc (> 108.3 needed), violations {len(bad)} -> {TS['verdict']}"
      + (" (H-OF changes no SPARC point; RAR scatter change exactly 0 vs 0.100 dex)" if not bad else ""))

    # ---------------- T-K KiDS early/late
    TK = json.load(open(os.path.join(WORK, "tk.json")))
    P("\n== T-K KiDS f30 early/late at matched M_b (obs +0.280 +- 0.083; CFG658 law -0.027)")
    TKR = {}
    for kern in KERN:
        for foot in FEET:
            for src in SRCS:
                rows = [r for r in TK if r["kern"] == kern and r["foot"] == foot and r["src"] == src]
                dOF = float(np.mean([r["dOF"] for r in rows])); pred = -0.027 + dOF
                ok = abs(pred - 0.280) < 2 * 0.083
                TKR[f"{kern}|{foot}|{src}"] = dict(dOF=dOF, pred=pred, Z=(0.280 - pred) / 0.083, pass_=ok,
                                                   res_early=[r["early"]["res_frac"] for r in rows], res_late=[r["late"]["res_frac"] for r in rows])
                P(f"  {kern} {foot[:3]} {src}: overflow early {['%.3f' % r['early']['res_frac'] for r in rows]} late {['%.3f' % r['late']['res_frac'] for r in rows]}; "
                  f"dOF {dOF:+.4f} -> pred {pred:+.3f} (Z {(0.280 - pred) / 0.083:+.2f}) {'PASS' if ok else 'FAIL'}")
    RES["T_K"] = TKR

    # ---------------- T-R eRASS1
    d = np.load(os.path.join(LANES, "CFG687_erass1_shear_stack", "cfg687_percluster.npz"))
    ER = list(np.load(os.path.join(WORK, "erass.npy"), allow_pickle=True))
    D, E = d["D"], d["E"]; W = np.where(E > 0, 1 / E ** 2, 0); n = len(D)
    order = np.argsort(d["ra"]); patch = np.empty(n, int); patch[order] = np.arange(n) * 30 // n
    BANDS = {"INNER": [0, 1, 2], "MID": [3, 4, 5], "OUTER": [6, 7]}
    mg = d["mg"]; q = np.quantile(mg, [0, 1 / 3, 2 / 3, 1]); tid = np.clip(np.digitize(mg, q[1:-1]), 0, 2)

    def A_of(sel, Pm):
        return {b: (W[sel][:, j] * D[sel][:, j]).sum() / (W[sel][:, j] * Pm[sel][:, j]).sum() for b, j in BANDS.items()}

    def jk(fun):
        full = fun(np.ones(n, bool)); reps = [fun(patch != p) for p in range(30)]
        return {k: (float(full[k]), float(np.sqrt(29 / 30 * np.sum((np.array([r[k] for r in reps]) - np.mean([r[k] for r in reps])) ** 2)))) for k in full}

    def slope(sel, arr):
        xs, ys = [], []
        for t in range(3):
            s = sel & (tid == t); j = BANDS["OUTER"]; v = (W[s][:, j] * arr[s][:, j]).sum() / W[s][:, j].sum()
            if v <= 0: return np.nan
            xs.append(np.log10(np.median(mg[s]))); ys.append(np.log10(v))
        return np.polyfit(xs, ys, 1)[0]

    P("\n== MUTATE M0 (overflow x0, phantom uncut = plain law) vs CFG687's stored law prediction (canonical, nu_mono, primary)")
    PM0 = np.array([o["M0"]["mono|canonical"] for o in ER])
    rel = np.median(np.abs(PM0 / d["PL"] - 1), axis=0)
    A0m = jk(lambda s: A_of(s, PM0)); APL = jk(lambda s: A_of(s, d["PL"]))
    dA = max(abs(A0m[b][0] - APL[b][0]) for b in BANDS)
    check("M0 eRASS1: plain law reproduced (median per-bin <= 1%, band A <= 0.01)", rel.max() <= 0.01 and dA <= 0.01,
          f"median |rel| per bin max {rel.max():.2e}; max |dA| {dA:.4f}")
    s_obs = jk(lambda s: {"s": slope(s, D)})["s"]
    TR = {}
    P("\n== T-R eRASS1 318 clusters: A = obs / H-OF (jackknife 30 patches); pass |A_MID-1| < 2 sig AND |A_OUTER-1| < 2 sig")
    for kern in KERN:
        for foot in FEET:
            PLk = np.array([o["M0"][f"{kern}|{foot}"] for o in ER])
            Alaw = jk(lambda s: A_of(s, PLk)); s_law = slope(np.ones(n, bool), PLk)
            for src in SRCS:
                base = np.array([o[f"{kern}|{foot}|{src}"]["base"] for o in ER]); resd = np.array([o[f"{kern}|{foot}|{src}"]["res"] for o in ER])
                Ph = base + resd
                A = jk(lambda s: A_of(s, Ph))
                rf = np.array([o[f"{kern}|{foot}|{src}"]["meta"]["res_frac"] for o in ER])
                zmid = (A["MID"][0] - 1) / A["MID"][1]; zout = (A["OUTER"][0] - 1) / A["OUTER"][1]
                ok = abs(zmid) < 2 and abs(zout) < 2
                s_h = slope(np.ones(n, bool), Ph)
                expl = abs(s_obs[0] - s_h) < 2 * s_obs[1] and (s_h - s_law) >= 0.21
                # M-SHUF: cluster i takes cluster j's overflow fraction and shape, rescaled to its own supply
                perm = np.random.default_rng(721).permutation(n)
                sup = np.array([o[f"{kern}|{foot}|{src}"]["meta"]["supply"] for o in ER])
                Psh = base + resd[perm] * (sup / sup[perm])[:, None]
                s_sh = slope(np.ones(n, bool), Psh)
                dtrend = abs(s_h - s_law)
                msh = "NOT APPLICABLE (no threshold inside the sample)" if dtrend < 0.05 else ("BITES" if abs(s_sh - s_h) >= 0.5 * dtrend else "DOES NOT BITE")
                spear = float(np.corrcoef(np.argsort(np.argsort(mg)), np.argsort(np.argsort(rf)))[0, 1])
                rf_t = [float(np.median(rf[tid == t])) for t in range(3)]
                TR[f"{kern}|{foot}|{src}"] = dict(A=A, A_law=Alaw, Z_mid=zmid, Z_outer=zout, pass_=ok, s_HOF=float(s_h), s_law=float(s_law),
                                                  s_obs=s_obs, explains_090=bool(expl), s_shuffled=float(s_sh), MSHUF=msh,
                                                  res_frac_median=float(np.median(rf)), res_frac_range=[float(rf.min()), float(rf.max())],
                                                  res_frac_tercile_median=rf_t, spearman_resfrac_mg=spear,
                                                  A_tercile_MID=[float((W[tid == t][:, 3:6] * D[tid == t][:, 3:6]).sum() / (W[tid == t][:, 3:6] * Ph[tid == t][:, 3:6]).sum()) for t in range(3)])
                P(f"  {kern} {foot[:3]} {src}: overflow/supply median {np.median(rf):.3f} (range {rf.min():.3f}-{rf.max():.3f}; terciles "
                  + " ".join(f"{x:.3f}" for x in rf_t) + f"); A INNER {A['INNER'][0]:.2f}+-{A['INNER'][1]:.2f} MID {A['MID'][0]:.2f}+-{A['MID'][1]:.2f} "
                  f"(Z {zmid:+.1f}) OUTER {A['OUTER'][0]:.2f}+-{A['OUTER'][1]:.2f} (Z {zout:+.1f}) -> {'PASS' if ok else 'FAIL'} | law A MID {Alaw['MID'][0]:.2f} "
                  f"OUTER {Alaw['OUTER'][0]:.2f} | slope s_HOF {s_h:.2f} vs law {s_law:.2f}, obs {s_obs[0]:.2f}+-{s_obs[1]:.2f} -> explains 0.90: {expl}; "
                  f"M-SHUF s {s_sh:.2f}: {msh}")
    if "bracket_cond_bcg" in ER[0]:
        Pb = np.array([o["bracket_cond_bcg"]["base"] + o["bracket_cond_bcg"]["res"] for o in ER])
        Ab = jk(lambda s: A_of(s, Pb)); rfb = np.array([o["bracket_cond_bcg"]["meta"]["res_frac"] for o in ER])
        TR["bracket_cond_bcg|mono|canonical"] = dict(A=Ab, s_HOF=float(slope(np.ones(n, bool), Pb)), res_frac_median=float(np.median(rfb)))
        P(f"  bracket (reported) cond placed as BCG + members, mono can: A INNER {Ab['INNER'][0]:.2f}+-{Ab['INNER'][1]:.2f} MID {Ab['MID'][0]:.2f}+-{Ab['MID'][1]:.2f} "
          f"OUTER {Ab['OUTER'][0]:.2f}+-{Ab['OUTER'][1]:.2f}; slope {TR['bracket_cond_bcg|mono|canonical']['s_HOF']:.2f}; overflow/supply median {np.median(rfb):.3f}")
    c1e = max(o[k]["meta"]["cons"] for o in ER for k in o if isinstance(o[k], dict) and "meta" in o[k])
    check("C1 supply = settled + reservoir (eRASS1)", c1e < 1e-9, f"max rel {c1e:.1e}")
    RES["T_R"] = TR

    # ---------------- T-A ACCEPT
    C686 = json.load(open(os.path.join(LANES, "CFG686_cluster_shear_vs_law", "cfg686_results.json")))
    cls = C686["clusters"]; AC = list(np.load(os.path.join(WORK, "accept.npy"), allow_pickle=True))
    D_ = np.nan_to_num(np.array([x["dsig"] for x in cls])); E_ = np.array([x["err"] for x in cls]); W_ = np.where(np.isfinite(E_) & (E_ > 0), 1 / E_ ** 2, 0)
    P("\n== MUTATE M0 ACCEPT: plain law vs CFG686's stored primary predictions")
    worst = 0.0
    for foot in FEET:
        PM = np.array([o["M0"][f"mono|{foot}"] for o in AC]); PS = np.array([x["pred"][f"{foot}|b+0.0|f0.20"] for x in cls])
        worst = max(worst, float(np.max(np.abs(PM / PS - 1))))
    check("M0 ACCEPT: plain law reproduced (<= 1% every bin)", worst <= 0.01, f"max |rel| {worst:.2e}")

    def bandA(Pm, sel):
        out = {}
        for b, j in BANDS.items():
            num = (W_[sel][:, j] * D_[sel][:, j]).sum(); den = (W_[sel][:, j] * Pm[sel][:, j]).sum(); out[b] = num / den if den != 0 else np.nan
        return out
    TA = {}
    P("== T-A ACCEPT 8 clusters (bootstrap 1000, seed 1)")
    for kern in KERN:
        for foot in FEET:
            for src in SRCS:
                Pm = np.array([o[f"{kern}|{foot}|{src}"]["base"] + o[f"{kern}|{foot}|{src}"]["res"] for o in AC])
                A = bandA(Pm, np.arange(len(cls))); rb = np.random.default_rng(1)
                boots = [bandA(Pm, rb.integers(0, len(cls), len(cls))) for _ in range(1000)]
                sig = {b: float(np.nanstd([bb[b] for bb in boots])) for b in BANDS}
                zm, zo = (A["MID"] - 1) / sig["MID"], (A["OUTER"] - 1) / sig["OUTER"]
                ok = abs(zm) < 2 and abs(zo) < 2
                rf = [o[f"{kern}|{foot}|{src}"]["meta"]["res_frac"] for o in AC]
                TA[f"{kern}|{foot}|{src}"] = dict(A={b: [float(A[b]), sig[b]] for b in BANDS}, Z_mid=float(zm), Z_outer=float(zo), pass_=bool(ok), res_frac=rf)
                P(f"  {kern} {foot[:3]} {src}: overflow/supply {np.median(rf):.3f}; A INNER {A['INNER']:.2f}+-{sig['INNER']:.2f} MID {A['MID']:.2f}+-{sig['MID']:.2f} "
                  f"(Z {zm:+.1f}) OUTER {A['OUTER']:.2f}+-{sig['OUTER']:.2f} (Z {zo:+.1f}) -> {'PASS' if ok else 'FAIL'}")
    RES["T_A"] = TA

    # ---------------- T-E eFEDS (CFG652 score code)
    W652 = os.path.join(EXT, "cfg652_work")
    I0 = np.load(os.path.join(W652, "cfg652_inputs.npz")); D0 = np.load(os.path.join(W652, "cfg652_esd.npz"))
    MD = np.load(os.path.join(W652, "cfg652_models.npz")); EM = np.load(os.path.join(WORK, "efeds_models.npz"))
    keep = I0["Mcond"] > 0
    P("\n== MUTATE M0 eFEDS: cfg652_model re-run with CFG652's kernel vs cfg652_models.npz (canonical x1)")
    w = 0.0
    for model in "ab":
        a1 = EM[f"M0repro__{model}"][keep]; a2 = MD[f"canonical__x1__{model}"][keep]
        w = max(w, float(np.nanmax(np.abs(a1 / a2 - 1))))
    check("M0 eFEDS: CFG652 models reproduced (<= 1% every group and bin)", w <= 0.01, f"max |rel| {w:.2e}")
    RB = np.geomspace(30, 3000, 13); RCg = np.sqrt(RB[1:] * RB[:-1])
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
    C = (NPATCH - 1) / NPATCH * (vals - mv).T @ (vals - mv)
    nb = int(USE.sum()); hart = (NPATCH - nb - 2) / (NPATCH - 1); Ci = np.linalg.inv(C) * hart
    obs = esd(allg, allr)
    aout = lambda o, m: float(np.log10(np.sum(o[BAND]) / np.sum(m[BAND])))
    TE = {}
    # control: CFG652's own (a) canonical x1 chi2 from the stored models
    ms = model_stack(MD["canonical__x1__a"][keep], allg); dd = obs[USE] - ms[USE]
    check("eFEDS score code reproduces CFG652's chi2 (a, canonical, x1) to 0.01", abs(float(dd @ Ci @ dd) - 22.895815392627757) < 0.01, f"{float(dd @ Ci @ dd):.4f} vs 22.8958")
    P("== T-E eFEDS 131 groups; pass chi2 p >= 0.01 AND |A_out| < 2 sigma")
    for kern in KERN:
        for foot in FEET:
            for src in SRCS:
                arr = EM[f"{kern}__{foot}__{src}"][keep]; ms = model_stack(arr, allg); dd = obs[USE] - ms[USE]
                ch = float(dd @ Ci @ dd); p = float(CHI2.sf(ch, nb)); A = aout(obs, ms)
                Aj = np.array([aout(esd(Dd["pg"] != qq, Dd["pr"] != qq), model_stack(arr, Dd["pg"] != qq)) for qq in range(NPATCH)])
                sA = float(math.sqrt((NPATCH - 1) / NPATCH * np.sum((Aj - Aj.mean()) ** 2)))
                ok = p >= 0.01 and abs(A) < 2 * sA
                rf = EM[f"rf__{kern}__{foot}__{src}"][keep]
                TE[f"{kern}|{foot}|{src}"] = dict(chi2=ch, p=p, A_out=A, sA=sA, pass_=bool(ok), model=ms[USE].tolist(), res_frac_median=float(np.nanmedian(rf)))
                P(f"  {kern} {foot[:3]} {src}: overflow/supply median {np.nanmedian(rf):.3f}; chi2 {ch:.1f}/{nb} p {p:.3g}; A_out {A:+.3f} +- {sA:.3f} -> {'PASS' if ok else 'FAIL'}")
                P("     model " + " ".join(f"{x:6.1f}" for x in ms[USE]) + " | obs " + " ".join(f"{x:6.1f}" for x in obs[USE]))
    RES["T_E"] = TE

    # ---------------- T-X X-COP (committed CFG637 numbers; nu_s not run)
    X637 = {"cond": dict(eta=[1.494, 1.661], sig=[0.061, 0.080], inner=[0.859, 0.889], label="FAIL"),
            "all": dict(eta=[1.820, 1.679], sig=[0.067, 0.062], inner=[3.163, 2.927], label="FAIL")}
    RES["T_X"] = {f"mono|{src}": dict(X637[src], source="CFG637 README / cfg637_gates_results.json (T3 headline 1000 kpc, old supply); CFG656 native supply: cond 0.452/0.460 TENSION, all identical FAIL")
                  for src in SRCS}
    RES["T_X"].update({f"s|{src}": dict(label="NOT RUN") for src in SRCS})
    P("\n== T-X X-COP (committed CFG637; nu_s not run): cond eta 1.494/1.661 FAIL (inner 0.859/0.889 PASS); all 1.820/1.679 FAIL")

    # ---------------- verdict
    P("\n== VERDICT per (source, kernel); both footings required")
    V = {}
    for kern in KERN:
        for src in SRCS:
            fails = []
            for foot in FEET:
                k = f"{kern}|{foot}|{src}"
                for nm, tab in (("T-K", TKR), ("T-E", TE), ("T-R", TR), ("T-A", TA)):
                    if not tab[k]["pass_"]: fails.append(f"{nm}[{foot[:3]}]")
            if RES["T_X"][f"{kern}|{src}"]["label"] != "PASS": fails.append(f"T-X({RES['T_X'][f'{kern}|{src}']['label']})")
            if TS["verdict"] != "PASS": fails.append("T-S")
            V[f"{src}|{kern}"] = "H-OF PASSES" if not fails else "H-OF FAILS: " + ", ".join(fails)
            P(f"  source {src}, kernel {kern}: {V[f'{src}|{kern}']}")
    # ---------------- ADDENDUM c5c6894a6: Bullet cores (CFG637 B1, nu_mono) and H-OF2
    G637 = json.load(open(os.path.join(LANES, "CFG637_derived_reservoir", "cfg637_gates_results.json")))["T4"]
    SIGCAP = {f: A0SI[f] / (math.pi * G) / KG for f in FEET}                       # Msun/pc^2
    BU = {}
    P("\n== ADDENDUM target: Bullet cores, M_model(<250 kpc)/P16 (CFG637 B1, nu_mono; P16 PROVISIONAL); pass 0.75-1.25 main AND sub")
    for src, s637 in (("cond", "HCB"), ("all", "B")):
        rows = {}
        for foot, ft in (("canonical", "can"), ("alt", "alt")):
            c = G637[f"B1|{ft}|{s637}|RD|P|phase"]["core"]
            rows[foot] = {r: c[r]["ratio_P16"] for r in ("main", "sub")}
        ok = all(0.75 <= rows[f][r] <= 1.25 for f in FEET for r in ("main", "sub"))
        BU[f"mono|{src}"] = dict(ratios=rows, pass_=ok)
        BU[f"s|{src}"] = dict(label="NOT RUN", pass_=False)
        P(f"  {src}: main {rows['canonical']['main']:.3f} / {rows['alt']['main']:.3f}, sub {rows['canonical']['sub']:.3f} / {rows['alt']['sub']:.3f} -> {'PASS' if ok else 'FAIL'}"
          f" (capacity a0/piG = {SIGCAP['canonical']:.1f} / {SIGCAP['alt']:.1f} Msun/pc^2)")
    RES["T_B"] = BU
    P("\n== ADDENDUM H-OF2 verification: capped-kernel runs vs H-OF (rule: max |rel| <= 1e-3 in DeltaSigma and overflow fraction)")
    worst = dict(ds=0.0, rf=0.0)
    AC2 = list(np.load(os.path.join(WORK, "accept_hof2.npy"), allow_pickle=True)); E20 = list(np.load(os.path.join(WORK, "erass20_hof2.npy"), allow_pickle=True))
    for A1, A2, feet in ((AC, AC2, FEET), (ER[:20], E20, ("canonical",))):
        for o1, o2 in zip(A1, A2):
            for kern in KERN:
                for foot in feet:
                    for src in SRCS:
                        a, b = o1[f"{kern}|{foot}|{src}"], o2[f"{kern}_cap|{foot}|{src}"]
                        t1, t2 = a["base"] + a["res"], b["base"] + b["res"]
                        worst["ds"] = max(worst["ds"], float(np.max(np.abs(t2 / t1 - 1))))
                        worst["rf"] = max(worst["rf"], abs(a["meta"]["res_frac"] - b["meta"]["res_frac"]))
    TK2 = json.load(open(os.path.join(WORK, "tk_hof2.json")))
    for r2 in TK2:
        r1 = [r for r in TK if r["kern"] + "_cap" == r2["kern"] and r["foot"] == r2["foot"] and r["src"] == r2["src"] and r["lMb"] == r2["lMb"]][0]
        for typ in ("early", "late"):
            worst["ds"] = max(worst["ds"], float(np.max(np.abs(np.array(r2[typ]["hof"]) / np.array(r1[typ]["hof"]) - 1))))
            worst["rf"] = max(worst["rf"], abs(r2[typ]["res_frac"] - r1[typ]["res_frac"]))
    same = worst["ds"] <= 1e-3 and worst["rf"] <= 1e-3
    RES["HOF2_verification"] = dict(worst, identical=same)
    P(f"  max |DeltaSigma_HOF2/DeltaSigma_HOF - 1| = {worst['ds']:.2e}; max |d overflow fraction| = {worst['rf']:.2e} -> "
      + ("H-OF2 = H-OF numerically: H-OF2 takes H-OF's scores" if same else "H-OF2 DIFFERS: full H-OF2 stage runs required (not done here)"))
    P("\n== VERDICT side by side (Bullet core added to both)")
    V2 = {}
    for kern in KERN:
        for src in SRCS:
            k = f"{src}|{kern}"; extra = [] if BU[f"{kern}|{src}"]["pass_"] else [f"T-B({BU[f'{kern}|{src}'].get('label', 'FAIL')})"]
            base = V[k]
            v1 = ("H-OF FAILS: " + ", ".join(([] if base == "H-OF PASSES" else [base.split(": ", 1)[1]]) + extra)) if (base != "H-OF PASSES" or extra) else "H-OF PASSES"
            V[k] = v1
            V2[k] = (v1.replace("H-OF", "H-OF2") if same else "H-OF2 NOT SCORED (differs from H-OF)")
            P(f"  source {src}, kernel {kern}:  {V[k]}   ||   {V2[k]}")
    RES["verdict_HOF2"] = V2
    RES["verdict"] = V; RES["checks"] = CHK; RES["elapsed_s"] = round(time.time() - T0, 1)
    nf = sum(1 for c in CHK.values() if not c["ok"])
    P(f"\n{len(CHK) - nf}/{len(CHK)} checks pass. kappa fitted; cold energy mass required; not theory closed.")
    json.dump(C4.jclean(RES), open(os.path.join(HERE, "cfg721_results.json"), "w"), indent=1)
    open(os.path.join(HERE, "cfg721.out"), "w").write("\n".join(LOG) + "\n")
    sys.exit(1 if nf else 0)

if MODE != "score":
    open(os.path.join(HERE, f"cfg721_{MODE}.log"), "w").write("\n".join(LOG) + f"\nelapsed {time.time() - T0:.0f} s\n")
