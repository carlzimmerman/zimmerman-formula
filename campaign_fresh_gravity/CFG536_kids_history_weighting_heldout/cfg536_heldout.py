#!/usr/bin/env python3
"""CFG536 (FROZEN_CRITERIA.md, criteria commit 416acbb62): CFG534's post-hoc overlap-weighted early - late estimator, frozen
unchanged, applied to the DISJOINT held-out sample HO = stack P minus f30, in the validated stack-P environment (CFG529 G1m: W10,
measured leakage 0.2234, constructions A and B).
Machinery: CFG534's cfg534_kids.py exec'd read-only up to its 'SPL = {' line (its wsum / match / esd_w / mstack / cp_w / gls / compare,
and through CFG531 / CFG529 the data, groups, patches, bands, fit_eps).  For HO only the per-group tables GT are replaced by the
stack-P environment tables.  Controls C1/C2 reproduce CFG534 on f30 (NOT CONFIRMATORY).  Leakage: per-class CFG519 S_IC satellite
fractions (L1) and the bias they put into Delta eps (L2).
MUTATE (CFG536_MUTATE=1 -> *_MUTATE.*): MU1 50 within-group label shuffles of HO (overlap), MU2 injected Delta eps = 0.3.
Run: nice -n 10 python3 cfg536_heldout.py ; CFG536_MUTATE=1 nice -n 10 python3 cfg536_heldout.py
"""
import os, sys, io, json, time, contextlib
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_v] = "1"
import numpy as np

T0 = time.time()
HERE = os.path.dirname(os.path.abspath(__file__))
LANES = os.path.dirname(HERE)
REPO = os.path.dirname(LANES)
EXT = os.path.abspath(os.path.join(REPO, "..", "_external_data"))
MUT = os.environ.get("CFG536_MUTATE", "0") == "1"
SUF = "_MUTATE" if MUT else ""
LOG, CHK = [], {}
RES = {"lane": "CFG536", "script": "cfg536_heldout", "mutate": MUT, "criteria_commit": "416acbb62",
       "settings": "kappa = 1/2 FITTED; footings never pooled; nu_mono; cold energy mass still required; not theory closed"}


def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); LOG.append(s)


def check(name, ok, msg):
    CHK[name] = dict(ok=bool(ok), msg=msg); P(f"  [{'PASS' if ok else 'FAIL'}] {name}: {msg}")


try:
    os.nice(10)
except OSError:
    pass

# ------------------------------------------------------------------ CFG534 machinery (read-only exec up to its split dictionary)
P534 = os.path.join(LANES, "CFG534_history_dependent_settling", "cfg534_kids.py")
_src = open(P534).read()
_cut = _src.index("SPL = {")
M = {"__file__": P534, "__name__": "cfg534_ro"}
os.environ["CFG534_MUTATE"] = "0"
_buf = io.StringIO()
with contextlib.redirect_stdout(_buf):
    exec(compile(_src[:_cut], "cfg534_kids", "exec"), M)
NS = M["NS"]                                                                     # CFG531 namespace (holds CFG529's functions)
P(f"CFG534 machinery exec'd read-only ({len(_buf.getvalue().splitlines())} lines suppressed); CFG531 checks: "
  f"{ {k: v['ok'] for k, v in NS['CHK'].items()} }")
F30, EARLY, gi, GP, BANDS, CONS, FOOTS, SHMRS = M["F30"], M["EARLY"], M["gi"], M["GP"], M["BANDS"], M["CONS"], M["FOOTS"], M["SHMRS"]
compare, match, esd_w, mstack, gls, NPATCH = M["compare"], M["match"], M["esd_w"], M["mstack"], M["gls"], M["NPATCH"]
evec, own_rec, model_score, env_cfg, MEAS = NS["evec"], NS["own_rec"], NS["model_score"], NS["env_cfg"], NS["MEAS"]
J534 = json.load(open(os.path.join(LANES, "CFG534_history_dependent_settling", "cfg534_kids_results.json")))
J529 = json.load(open(os.path.join(LANES, "CFG529_f30_matched_environment", "cfg529_score_results.json")))
NL = len(F30)
HO = ~F30
GT30 = dict(M["GT"])
K9 = BANDS["K9"]

# C4 disjointness
check("C4 HO and f30 disjoint, union = stack P", (HO & F30).sum() == 0 and (HO | F30).all() and HO.sum() == 124212,
      f"HO {int(HO.sum())}, f30 {int(F30.sum())}, stack P {NL}")

# ------------------------------------------------------------------ stack-P environment tables (CFG529 G1m)
GTP = {}
for c in CONS:
    for foot in FOOTS:
        for s in SHMRS:
            GTP[(c, foot, s)] = (evec(GP, c, s, "W10", MEAS["P"][s], "meas|W10"), own_rec(c, "P", foot, "LAW_RTA", s, "W10", MEAS["P"][s]))
c5 = max(abs(model_score(env_cfg(c, "P", MEAS["P"], MEAS["P"], "meas"), "LCDM", "canonical")["chi2"] - J529["gates"][c]["G1m"]["chi2"]) for c in CONS)
check("C5 stack-P environment reproduces CFG529 G1m LCDM chi2 (A, B) within 0.01", c5 <= 0.01, f"max |d| {c5:.2e}")
P(f"stack-P tables built ({time.time() - T0:.0f} s)")


def use(tabs):
    M["GT"].clear(); M["GT"].update(tabs)


def k9(r, cell):
    x = r[cell]["K9"]
    return dict(eps=x["d_eps_moster"]["eps"], sig=x["d_eps_moster"]["sig"], Z=x["d_eps_moster"]["Z"], Z_behroozi=x["d_eps_behroozi"]["Z"],
                Zmin=x["Zmin"], eps_early=x["eps_A"], eps_late=x["eps_B"])


def dd_cov(mA, mB, mode):
    """Delta d and its jackknife covariance exactly as CFG534's compare builds them (for the leakage projection)."""
    MA, MB = match(mA, mB, mode)
    dA, _, LA = esd_w(mA, MA); dB, _, LB = esd_w(mB, MB)
    dv = LA - LB; dv = dv - dv.mean(0)
    return dA - dB, (NPATCH - 1) / NPATCH * dv.T @ dv, MA


CELLS = [f"{c}|{f}" for c in CONS for f in FOOTS]

if not MUT:
    # ------------------------------------------------------------------ C1 / C2: f30 reproduction (NOT CONFIRMATORY)
    P("\n== C1/C2: CFG534 on f30 (NOT CONFIRMATORY) ==")
    use(GT30)
    r30o = compare(F30 & EARLY, F30 & ~EARLY, "f30 overlap [control]", mode="overlap")
    r30f = compare(F30 & EARLY, F30 & ~EARLY, "f30 frozen [control]", mode="A")
    c1 = c2 = 0.0
    for cell in CELLS:
        ref = J534["postfreeze_overlap"]["1a_type"][cell]["K9"]; a = r30o[cell]["K9"]
        c1 = max(c1, *(abs(a["d_eps_moster"][q] - ref["d_eps_moster"][q]) for q in ("eps", "sig", "Z")), abs(a["Zmin"] - ref["Zmin"]))
        ref = J534["compare"]["1a_type"][cell]["K9"]; a = r30f[cell]["K9"]
        c2 = max(c2, *(abs(a["d_eps_moster"][q] - ref["d_eps_moster"][q]) for q in ("eps", "sig", "Z")), abs(a["Zmin"] - ref["Zmin"]))
    check("C1 overlap estimator on f30 reproduces CFG534 postfreeze_overlap 1a K9 (eps, sigma, Z, Zmin; 4 cells; 1e-6) [NOT CONFIRMATORY]",
          c1 < 1e-6, f"max |d| {c1:.1e}; A|canonical {r30o['A|canonical']['K9']['d_eps_moster']['eps']:+.4f} +- "
          f"{r30o['A|canonical']['K9']['d_eps_moster']['sig']:.4f}")
    check("C2 frozen estimator on f30 reproduces CFG534 compare 1a K9 (1e-6)", c2 < 1e-6, f"max |d| {c2:.1e}")
    RES["control_f30_NOT_CONFIRMATORY"] = {"overlap": {cl: k9(r30o, cl) for cl in CELLS}, "frozen": {cl: k9(r30f, cl) for cl in CELLS}}

    # ------------------------------------------------------------------ held-out
    P("\n== HELD-OUT HO = stack P minus f30, stack-P environment (W10, 0.2234) ==")
    use(GTP)
    rho = compare(HO & EARLY, HO & ~EARLY, "HO overlap [VERDICT]", mode="overlap")
    rhf = compare(HO & EARLY, HO & ~EARLY, "HO frozen [reported]", mode="A")
    check("C3 HO matched classes share identical stacked model vectors (1e-10 rel; both modes)",
          max(rho["K2_model_maxrel"], rhf["K2_model_maxrel"]) < 1e-10, f"overlap {rho['K2_model_maxrel']:.1e}, frozen {rhf['K2_model_maxrel']:.1e}")
    P(f"  HO overlap: n_early {rho['nA']} (kept {rho['nA_kept']}), n_late {rho['nB']} (kept {rho['nB_kept']})")
    HOR = {"n": {k: rho[k] for k in ("nA", "nB", "nA_kept", "nB_kept")},
           "overlap": {cl: dict(K9=k9(rho, cl), bands={b: {q: rho[cl][b]["d_eps_moster"][q] for q in ("eps", "sig", "Z")} for b in BANDS}) for cl in CELLS},
           "frozen": {cl: dict(K9=k9(rhf, cl), bands={b: {q: rhf[cl][b]["d_eps_moster"][q] for q in ("eps", "sig", "Z")} for b in BANDS}) for cl in CELLS}}
    RES["heldout"] = HOR

    # ------------------------------------------------------------------ leakage L1 (CFG519 state, per class)
    P("\n== L1: per-class leaked-satellite fraction (CFG519 S_IC, 48-cell reweighting, 12-region jackknife) ==")
    S = np.load(os.path.join(EXT, "cfg502_work", "cfg502_stage.npz"))
    X = np.load(os.path.join(EXT, "cfg519_work", "cfg519_state.npz"))
    iso10, iso30, iso_idx, ltyp = S["iso10"].astype(bool), S["iso30"].astype(bool), S["iso_idx"], S["typ"].astype(int)
    wl = S["WW"].sum(1)
    inside, L_m, REG, S_IC, cell = X["inside"].astype(bool), X["L_m"].astype(bool), X["REG"], X["S_IC"].astype(float), X["cell"]
    assert np.array_equal(iso30[iso_idx], F30) and np.array_equal(ltyp[iso_idx], EARLY.astype(int))
    NC, NCM, NCZ = 48, 6, 4
    ho_all = iso10 & ~iso30

    def cell_frac(val, src, fallback):
        num = np.bincount(cell[src], weights=(wl * val)[src], minlength=NC); den = np.bincount(cell[src], weights=wl[src], minlength=NC)
        n = np.bincount(cell[src], minlength=NC)
        f = np.full(NC, np.nan); direct = n >= 20
        f[direct] = num[direct] / den[direct]
        if fallback:                                                             # CFG519's frozen fallback (copied)
            n3, num3, den3, f3 = n.reshape(NCM, NCZ, 2), num.reshape(NCM, NCZ, 2), den.reshape(NCM, NCZ, 2), f.reshape(NCM, NCZ, 2)
            for a in range(NCM):
                for t in range(2):
                    for zc in range(NCZ):
                        if np.isnan(f3[a, zc, t]):
                            if n3[a, :, t].sum() >= 20:
                                f3[a, zc, t] = num3[a, :, t].sum() / den3[a, :, t].sum()
                            elif n3[a].sum() >= 20:
                                f3[a, zc, t] = num3[a].sum() / den3[a].sum()
            f = f3.reshape(NC)
        return f

    def rew(src, tgt, fallback=False):
        f = cell_frac(S_IC, src, fallback)
        W = np.bincount(cell[tgt], weights=wl[tgt], minlength=NC); g = np.isfinite(f)
        return float((W[g] * f[g]).sum() / W[g].sum()), float(W[g].sum() / W.sum())

    base = inside & L_m
    c6, _ = rew(iso30 & base, iso30, fallback=True)
    check("C6 f30 overall leaked fraction (CFG519 cell scheme with fallback) reproduces CFG519 main.f30 (1e-6)",
          abs(c6 - 0.16863265651220682) < 1e-6, f"{c6:.8f}")
    SETS = {"f30": iso30, "HO": ho_all}
    L1 = {}
    for nm, ms in SETS.items():
        for cl, tm in (("all", np.ones_like(ms)), ("early", ltyp == 1), ("late", ltyp == 0)):
            f, share = rew(ms & tm & base, ms & tm)
            jk = np.array([rew(ms & tm & base & (REG != k), ms & tm)[0] for k in range(12)])
            L1[f"{nm}|{cl}"] = dict(f=f, sig=float(np.sqrt(11 / 12 * ((jk - jk.mean()) ** 2).sum())), W_share_defined=share)
        jk = np.array([rew(ms & (ltyp == 1) & base & (REG != k), ms & (ltyp == 1))[0] - rew(ms & (ltyp == 0) & base & (REG != k), ms & (ltyp == 0))[0]
                       for k in range(12)])
        df = L1[f"{nm}|early"]["f"] - L1[f"{nm}|late"]["f"]
        L1[f"{nm}|delta_f"] = dict(f=df, sig=float(np.sqrt(11 / 12 * ((jk - jk.mean()) ** 2).sum())))
        P(f"  {nm:4s}: all {L1[nm + '|all']['f']:.4f}+-{L1[nm + '|all']['sig']:.4f}  early {L1[nm + '|early']['f']:.4f}+-{L1[nm + '|early']['sig']:.4f}  "
          f"late {L1[nm + '|late']['f']:.4f}+-{L1[nm + '|late']['sig']:.4f}  Delta f (E-L) {df:+.4f}+-{L1[nm + '|delta_f']['sig']:.4f}  "
          f"(weight share defined early {L1[nm + '|early']['W_share_defined']:.3f} / late {L1[nm + '|late']['W_share_defined']:.3f})")
    L1["CFG509_cross_check_stackP"] = dict(f_late=0.113, f_early=0.168, delta_f=0.055, sig=0.004, note="counts-based, halo-model converted (CFG509 README)")
    RES["L1_leakage"] = L1

    # ------------------------------------------------------------------ leakage L2 (bias put into Delta eps)
    P("\n== L2: leakage bias Delta eps_leak = Delta f x GLS(D) (D = d model / d leaked fraction, matched overlap stack, Moster) ==")
    L2 = {}
    for nm, mask, K, smp, tabs in (("HO", HO, "W10", "P", GTP), ("f30", F30, "W30", "f30", GT30)):
        mA, mB = mask & EARLY, mask & ~EARLY
        dd, Cd, MA = dd_cov(mA, mB, "overlap")
        dfv = L1[f"{nm}|delta_f"]["f"]
        for c in CONS:
            for foot in FOOTS:
                s = "moster"
                one, zero = np.ones_like(MEAS[smp][s]), np.zeros_like(MEAS[smp][s])
                Dg = (evec(GP, c, s, K, one, f"cfg536_f1|{K}") - evec(GP, c, s, K, zero, f"cfg536_f0|{K}")
                      + own_rec(c, smp, foot, "LAW_RTA", s, K, one) - own_rec(c, smp, foot, "LAW_RTA", s, K, zero))
                Dst = mstack(Dg, mA, MA)
                o = mstack(tabs[(c, foot, s)][1], mA, MA)
                g = gls(Dst, Cd, o, K9)
                de = (rho if nm == "HO" else r30o)[f"{c}|{foot}"]["K9"]["d_eps_moster"]
                L2[f"{nm}|{c}|{foot}"] = dict(deps_per_unit_f=g["eps"], delta_f=dfv, deps_leak=dfv * g["eps"],
                                              deps_leak_sig=L1[f"{nm}|delta_f"]["sig"] * abs(g["eps"]),
                                              ratio_to_deps=dfv * g["eps"] / de["eps"], Z_adjusted=(de["eps"] - dfv * g["eps"]) / de["sig"])
                v = L2[f"{nm}|{c}|{foot}"]
                P(f"  {nm:4s} [{c} {foot:9s}] dDelta eps/df {g['eps']:+.3f}; Delta eps_leak {v['deps_leak']:+.3f}+-{v['deps_leak_sig']:.3f}; "
                  f"leak / Delta eps {v['ratio_to_deps']:+.2f}; leakage-adjusted Z {v['Z_adjusted']:+.2f}")
    RES["L2_leakage_bias"] = L2

    # ------------------------------------------------------------------ verdict (needs MU1 from the MUTATE JSON)
    mu_path = os.path.join(HERE, "cfg536_heldout_results_MUTATE.json")
    MU1 = json.load(open(mu_path))["MU1"] if os.path.exists(mu_path) else None
    VER = {}
    for foot in FOOTS:
        sig = [HOR["overlap"][f"{c}|{foot}"]["K9"]["sig"] for c in CONS]
        z = [HOR["overlap"][f"{c}|{foot}"]["K9"]["Zmin"] for c in CONS]
        e = [HOR["overlap"][f"{c}|{foot}"]["K9"]["eps"] for c in CONS]
        mu_ok = None if MU1 is None else all(abs(MU1["mean_Z"][f"{c}|{foot}"]) < 1 for c in CONS)
        if max(sig) > 0.30 or mu_ok is False:
            lab = "NOT DIAGNOSTIC"
        elif mu_ok is None:
            lab = "PENDING (run MUTATE first)"
        elif all(x > 0 for x in e) and all(x >= 3 for x in z):
            lab = "CONFIRMED"
        elif all(x > 0 for x in e) and all(x >= 2 for x in z):
            lab = "CONSISTENT"
        else:
            lab = "NOT CONFIRMED"
        leak = any(L2[f"HO|{c}|{foot}"]["deps_leak"] >= 0.5 * HOR["overlap"][f"{c}|{foot}"]["K9"]["eps"] for c in CONS)
        VER[foot] = dict(label=lab + (" + LEAKAGE-LIMITED" if leak else ""), sig=sig, Zmin=z, eps=e, MU1_pass=mu_ok, leakage_limited=leak)
        P(f"\n  VERDICT [{foot}]: {VER[foot]['label']}  (Delta eps K9 A/B {e[0]:+.3f}/{e[1]:+.3f}, sigma {sig[0]:.3f}/{sig[1]:.3f}, Zmin {z[0]:+.2f}/{z[1]:+.2f}; MU1 {mu_ok})")
    labs = {v["label"] for v in VER.values()}
    VER["headline"] = labs.pop() if len(labs) == 1 else "FOOTING-DEPENDENT: " + "; ".join(f"{f} {VER[f]['label']}" for f in FOOTS)
    P(f"  HEADLINE: {VER['headline']}")
    RES["verdict"] = VER
else:
    P("\n== MUTATE (HO, stack-P environment) ==")
    use(GTP)
    idxH = np.nonzero(HO)[0]
    groups = np.unique(gi[idxH])
    Zs = {cl: [] for cl in CELLS}
    for i, seed in enumerate(range(5360, 5410)):
        rng = np.random.default_rng(seed)
        ES = EARLY.copy()
        for g in groups:
            m = idxH[gi[idxH] == g]
            ES[m] = rng.permutation(EARLY[m])
        with contextlib.redirect_stdout(io.StringIO()):
            r = compare(HO & ES, HO & ~ES, f"MU1 seed {seed}", mode="overlap")
        for cl in CELLS:
            Zs[cl].append(r[cl]["K9"]["d_eps_moster"]["Z"])
        if i == 0:
            P("  seed 5360: " + "; ".join(f"{cl} Z {Zs[cl][0]:+.2f}" for cl in CELLS))
    mu1 = dict(mean_Z={cl: float(np.mean(v)) for cl, v in Zs.items()}, sd_Z={cl: float(np.std(v, ddof=1)) for cl, v in Zs.items()},
               seed5360_Z={cl: v[0] for cl, v in Zs.items()}, frac_absZ_ge2={cl: float(np.mean(np.abs(v) >= 2)) for cl, v in Zs.items()}, Z_all=Zs)
    check("MU1 50 within-group label shuffles of HO (overlap): |mean Z(K9)| < 1 in all four cells",
          all(abs(v) < 1 for v in mu1["mean_Z"].values()),
          "; ".join(f"{cl} mean {mu1['mean_Z'][cl]:+.2f} sd {mu1['sd_Z'][cl]:.2f}" for cl in CELLS))
    RES["MU1"] = mu1
    r = compare(HO & EARLY, HO & ~EARLY, "MU2", inject=0.3, mode="overlap")
    mu2 = max(abs(r[cl][b]["d_eps_moster"]["eps"] - 0.3) for cl in CELLS for b in BANDS)
    check("MU2 mock d_early = d_late,matched + 0.3 own on HO (overlap): Delta eps = 0.300 every band (1e-6)", mu2 < 1e-6, f"max |d| {mu2:.1e}")

RES["checks"] = CHK
RES["elapsed_s"] = round(time.time() - T0, 1)
nf = sum(1 for v in CHK.values() if not v["ok"])
P(f"\n{len(CHK) - nf}/{len(CHK)} checks pass; elapsed {RES['elapsed_s']} s")
json.dump(RES, open(os.path.join(HERE, f"cfg536_heldout_results{SUF}.json"), "w"), indent=1, default=float)
open(os.path.join(HERE, f"cfg536_heldout{SUF}.out"), "w").write("\n".join(LOG) + "\n")
sys.exit(1 if nf else 0)
