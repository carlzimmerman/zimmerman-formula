#!/usr/bin/env python3
"""
CFG359 analysis: framework-native nonlinear PM growth of candidate B with the CFG354 T1 switch.
Criteria: FROZEN_CRITERIA.md (ab965b387 + Amendment 1 a3064af84).  Reads the run JSONs/snapshots written by
cfg359_pm.py (via cfg359_run_all.py) in ../_external_data/cfg359_work/ and scores the frozen decision per a0 branch
(FLAT = lane verdict, CRIT = separate branch, DE = reported), per footing, never pooled.
S0 = the Newtonian control (the only non-MOND run).  The ONLY LCDM input = the linear EH spectrum at z_i = 49 (CFG324).
MUTATE: CFG359_MUTATE=1 -> scores C4 (T1 with Delta_ta := 1) and writes *_MUTATE outputs.
Run from the repository root (after cfg359_run_all.py, both modes):
    python3 campaign_fresh_gravity/CFG359_native_pm_growth/cfg359_native_pm_growth.py
    CFG359_MUTATE=1 python3 campaign_fresh_gravity/CFG359_native_pm_growth/cfg359_native_pm_growth.py
"""
import os, sys, json, math
import numpy as np
from scipy.spatial import cKDTree
from scipy.sparse import coo_matrix
from scipy.sparse.csgraph import connected_components
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
_argv = sys.argv; sys.argv = [sys.argv[0]]
import cfg359_pm as C
sys.argv = _argv
MUTATE = C.MUTATE; SUF = "_MUTATE" if MUTATE else ""
OUT = {"lane": "CFG359", "mutate": MUTATE, "frozen": "ab965b387", "amendment1": "a3064af84", "checks": {}, "numbers": {}}
LOG = []
def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); LOG.append(s)
def check(name, ok, measured=""):
    OUT["checks"][name] = {"pass": bool(ok), "measured": str(measured)}
    P(f"  [{'PASS' if ok else 'FAIL'}] {name}: {measured}"); return bool(ok)
def banner(t): P("\n" + "=" * 100 + "\n" + t + "\n" + "=" * 100)
FOOTS, BRANCHES, ZN = ("canonical", "alt"), ("FLAT", "CRIT", "DE"), ("z1", "z0.5", "z0")
RHOBAR = 2.775e11 * C.Om                                 # (Msun/h) / (Mpc/h)^3

def load(sw, br, ft, n=256, amp=1.0, mut=False):
    t = f"{sw}_{br}_{ft}_N{n}" + (f"_amp{amp:g}" if amp != 1 else "") + ("_MUTATE" if mut else "")
    p = os.path.join(C.WORK, f"cfg359_{t}.json")
    return (json.load(open(p)), t) if os.path.exists(p) else (None, t)

def ratios(r, r0, zn):
    s, s0 = r["snap"][zn], r0["snap"][zn]
    k = np.array(s["k"]); pr = np.array(s["P"]) / np.array(s0["P"]); m = k <= 1.0
    return dict(sig8=s["sigma8"] / s0["sigma8"], pk_maxdev=float(np.max(np.abs(pr[m] - 1))),
                pk_at=dict((f"{kk}", float(np.interp(kk, k, pr))) for kk in (0.1, 0.3, 1.0)))

def verdict(rows):
    ds = max(abs(x["sig8"] - 1) for x in rows); dp = max(x["pk_maxdev"] for x in rows)
    if ds > 0.20: return "FAIL", ds, dp
    if ds <= 0.05 and dp <= 0.10: return "GROWTH OK", ds, dp
    return "TENSION", ds, dp

def fof(tagname, n=256, sub=2):
    cache = os.path.join(C.WORK, f"cfg359_fof_{tagname}.npz")
    if os.path.exists(cache):
        d = np.load(cache); return d["M"], d["X"]
    pos = np.load(os.path.join(C.WORK, f"cfg359_{tagname}_z0.npz"))["pos"].astype(np.float64)
    idx = np.indices((n,) * 3).reshape(3, -1).T
    sel = np.all(idx % sub == 0, axis=1); x = np.mod(pos[sel], C.L); x[x >= C.L] = 0.0
    ns = n // sub; mp = RHOBAR * C.L ** 3 / ns ** 3; b = 0.2 * C.L / ns
    tr = cKDTree(x, boxsize=C.L); pr = tr.query_pairs(b, output_type="ndarray")
    g = coo_matrix((np.ones(len(pr), np.int8), (pr[:, 0], pr[:, 1])), shape=(len(x),) * 2)
    _, lab = connected_components(g, directed=False)
    cnt = np.bincount(lab); good = np.where(cnt >= 20)[0]
    th = 2 * np.pi * x / C.L
    X = np.stack([np.mod(np.arctan2(np.bincount(lab, np.sin(th[:, i]))[good], np.bincount(lab, np.cos(th[:, i]))[good]), 2 * np.pi) * C.L / (2 * np.pi) for i in range(3)], 1)
    M = cnt[good] * mp
    np.savez(cache, M=M, X=X, npairs=len(pr)); return M, X

MB = 10 ** np.arange(12.75, 15.01, 0.25)
def cumN(M): return np.array([(M >= m).sum() for m in MB])

def proximity_split(tagname, M, X):
    d = np.load(os.path.join(C.WORK, f"cfg359_{tagname}_z0.npz")); f = d["f"].astype(np.float32); l3 = d["l3"].astype(np.float32)
    n = f.shape[0]; dx = C.L / n; near = np.zeros(f.shape, bool)
    rta = (3 * M / (4 * np.pi * C.dta_table()["D"][0] * RHOBAR)) ** (1 / 3)
    for (cx, cy, cz), r in zip(X, rta):
        ii = [np.arange(int(math.floor((c - r) / dx)), int(math.ceil((c + r) / dx)) + 1) for c in (cx, cy, cz)]
        dd = [((i + 0.5) * dx - c + C.L / 2) % C.L - C.L / 2 for i, c in zip(ii, (cx, cy, cz))]
        m = (dd[0][:, None, None] ** 2 + dd[1][None, :, None] ** 2 + dd[2][None, None, :] ** 2) <= r * r
        near[np.ix_(ii[0] % n, ii[1] % n, ii[2] % n)] |= m
    on = f > 0.5
    return dict(vol_on=float(on.mean()), on_in_rta=float((on & near).mean()), on_out_rta=float((on & ~near).mean()),
                on_out_rta_filsig=float((on & ~near & (l3 < 0)).mean()), vol_in_rta=float(near.mean()))

# ===================================================================================================== start
P(__doc__.strip())
banner("MODEL (FROZEN ab965b387 + Amendment 1): flags")
P("  Background GR + Lambda (FP2), Om = %.4f, f_b = %.4f; nu_mono (L340 104-118); phantom from baryons only, x switch f;" % (C.Om, C.FB))
P("  kappa = 1/2 FITTED, fixed: a0 canonical 9.3603e-11 / alt 1.1312e-10 m/s^2 (code units %.1f / %.1f H0^2 Mpc/h)." % (C.A0['canonical'] / C.ACC_UNIT, C.A0['alt'] / C.ACC_UNIT))
P("  ** The ONLY LCDM input: the linear EH no-wiggle spectrum (sigma8_lin 0.811) for the Zel'dovich ICs at z_i = 49 (CFG324). **")
P("  S0 = Newtonian control (f = 0), not 'LCDM'. Heat filter identity at Mpc scales (omitted). Box 200 Mpc/h, 256^3 on 256^3, 150 KDK steps.")

if MUTATE:
    banner("C4 MUTATE: T1 with Delta_ta := 1 (tau = 0) must move toward S1 (sigma8 ratio above T1's) on both footings")
    r0, _ = load("S0", "FLAT", "canonical"); rows = {}; ok = True
    for ft in FOOTS:
        rm, _ = load("T1", "FLAT", ft, mut=True); rt, _ = load("T1", "FLAT", ft); rs, _ = load("S1", "FLAT", ft)
        a, b, c = (ratios(x, r0, "z0")["sig8"] for x in (rm, rt, rs))
        rows[ft] = dict(mutate=a, T1=b, S1=c, on_vol_mutate=rm["snap"]["z0"]["vol_on"], on_vol_T1=rt["snap"]["z0"]["vol_on"])
        ok &= a > b
        P(f"  {ft}: sigma8/S0  T1 {b:.4f} -> MUTATE {a:.4f}  (S1 {c:.4f}); ON volume {rows[ft]['on_vol_T1']:.4f} -> {rows[ft]['on_vol_mutate']:.4f}")
    OUT["numbers"]["C4"] = rows
    check("C4 MUTATE moves toward S1 on both footings", ok, json.dumps({k: round(v['mutate'], 4) for k, v in rows.items()}))
else:
    banner("C5  Delta_ta(z) table vs CFG354 K4 (11.806 at z = 0, 6.412 at z = 1)")
    dt = C.dta_table(); check("C5 Delta_ta reproduces CFG354 K4 (1%)", abs(dt["D"][0] / 11.806 - 1) < 0.01 and abs(dt["D"][4] / 6.412 - 1) < 0.01,
                              f"{dt['D'][0]:.3f} / {dt['D'][4]:.3f}; tau(0) = {(dt['D'][0] - 1) / 3:.4f}, tau(49) = {(dt['D'][-1] - 1) / 3:.4f}")
    OUT["numbers"]["Delta_ta"] = dt

    banner("C1  LINEAR GROWTH: S0 x 0.01 amplitude, k <= 0.1 h/Mpc, sqrt(P(a)/P(a_i)) / (D(a)/D(a_i)) within 1%")
    rl, _ = load("S0", "FLAT", "canonical", amp=0.01); s = rl["snap"]; k = np.array(s["zi"]["k"]); m = k <= 0.1; dev = {}
    for zn in ZN:
        g = np.sqrt(np.array(s[zn]["P"])[m] / np.array(s["zi"]["P"])[m]) / (s[zn]["D"] / s["zi"]["D"]); dev[zn] = float(np.max(np.abs(g - 1)))
    check("C1 S0 linear growth matches D(a) to 1%", max(dev.values()) <= 0.01, json.dumps({k_: round(v, 5) for k_, v in dev.items()}))
    OUT["numbers"]["C1"] = dev

    r0, _ = load("S0", "FLAT", "canonical")
    P(f"\n  S0 Newtonian control sigma8 (box modes, nonlinear): z1 {r0['snap']['z1']['sigma8']:.4f}, z0.5 {r0['snap']['z0.5']['sigma8']:.4f}, z0 {r0['snap']['z0']['sigma8']:.4f}; runtime {r0['runtime_s']/60:.1f} min")
    banner("RATIOS TO S0 (sigma8 ratio; max |P ratio - 1| for k <= 1 h/Mpc; P ratio at k = 0.1/0.3/1)")
    TAB = {}
    for sw in ("S1", "T1", "T1V"):
        for br in BRANCHES:
            for ft in FOOTS:
                r, t = load(sw, br, ft)
                if r is None: continue
                TAB[t] = {zn: ratios(r, r0, zn) for zn in ZN}
                TAB[t]["runtime_min"] = r["runtime_s"] / 60
                z0 = TAB[t]["z0"]
                P(f"  {t:28s} z0: s8 {z0['sig8']:.4f}  Pdev {z0['pk_maxdev']:.4f}  P@0.1/0.3/1 " + " / ".join(f"{v:.3f}" for v in z0["pk_at"].values())
                  + f"  | z0.5 s8 {TAB[t]['z0.5']['sig8']:.4f} | z1 s8 {TAB[t]['z1']['sig8']:.4f}  ({TAB[t]['runtime_min']:.0f} min)")
    OUT["numbers"]["ratios"] = TAB

    banner("T1 ON FRACTIONS (switch f on the mesh; ON = f > 0.5; T-web: knot l3 >= 0, filament signature l3 < 0)")
    ONF = {}
    for br in BRANCHES:
        for ft in FOOTS:
            r, t = load("T1", br, ft)
            if r is None: continue
            ONF[t] = {zn: {k_: r["snap"][zn][k_] for k_ in ("vol_f", "mass_f", "vol_on", "vol_on_knot", "vol_on_fil", "mass_on_knot", "mass_on_fil", "tau", "y_median", "nu_median")} for zn in ZN}
            z0 = ONF[t]["z0"]
            P(f"  {t:28s} z0: <f>_vol {z0['vol_f']:.4f} <f>_mass {z0['mass_f']:.4f}; ON vol {z0['vol_on']:.4f} = knot {z0['vol_on_knot']:.4f} + fil-sig {z0['vol_on_fil']:.4f};"
                  f" ON mass knot {z0['mass_on_knot']:.4f} fil-sig {z0['mass_on_fil']:.4f}; median y {z0['y_median']:.2e}, nu {z0['nu_median']:.1f}")
    OUT["numbers"]["on_fractions"] = ONF

    banner("HALO MASS FUNCTION PROXY (FoF b = 0.2, >= 20 members, Lagrangian 128^3 sub-lattice, z = 0): N(>M)/N_S0(>M)")
    HMF = {}; FOFR = {}
    tags = ["S0_FLAT_canonical_N256"] + [f"{sw}_{br}_{ft}_N256" for sw in ("T1", "T1V") for br in BRANCHES for ft in FOOTS] + [f"S1_FLAT_{ft}_N256" for ft in FOOTS]
    for t in tags:
        if not os.path.exists(os.path.join(C.WORK, f"cfg359_{t}_z0.npz")): continue
        try:
            FOFR[t] = fof(t)
        except MemoryError:
            P(f"  {t}: FoF skipped (memory)"); continue
        HMF[t] = cumN(FOFR[t][0]).tolist()
    n0 = np.array(HMF["S0_FLAT_canonical_N256"])
    P("  log10 M (Msun/h):        " + " ".join(f"{x:6.2f}" for x in np.log10(MB)))
    P("  S0 N(>M):                " + " ".join(f"{x:6d}" for x in n0))
    for t, v in HMF.items():
        if t.startswith("S0"): continue
        rr = np.array(v) / np.maximum(n0, 1)
        P(f"  {t:25s} " + " ".join(f"{x:6.3f}" for x in rr))
    OUT["numbers"]["hmf"] = dict(logM=np.log10(MB).tolist(), N=HMF)

    banner("WHERE T1 IS ON at z = 0: inside vs outside FoF halo r_ta spheres (r_ta from Delta_ta(0) = 11.806)")
    PROX = {}
    for t in [f"T1_{br}_{ft}_N256" for br in BRANCHES for ft in FOOTS]:
        if t in FOFR:
            PROX[t] = proximity_split(t, *FOFR[t])
            p_ = PROX[t]
            P(f"  {t:25s} ON vol {p_['vol_on']:.4f}: inside r_ta {p_['on_in_rta']:.4f}, outside {p_['on_out_rta']:.4f} (of which fil-sig {p_['on_out_rta_filsig']:.4f}); r_ta spheres fill {p_['vol_in_rta']:.4f}")
    OUT["numbers"]["proximity"] = PROX

    banner("FILAMENT-VETO DIAGNOSTIC: T1 vs T1-VETO (f = 0 where l3 < 0; removes filament cores AND host outskirts, Lean S8)")
    VET = {}
    for ft in FOOTS:
        a = TAB.get(f"T1_FLAT_{ft}_N256"); b = TAB.get(f"T1V_FLAT_{ft}_N256")
        if a and b:
            VET[ft] = dict(T1=a["z0"]["sig8"], T1V=b["z0"]["sig8"], share=(a["z0"]["sig8"] - b["z0"]["sig8"]) / max(a["z0"]["sig8"] - 1, 1e-12))
            P(f"  {ft}: sigma8/S0 T1 {VET[ft]['T1']:.4f}, T1-VETO {VET[ft]['T1V']:.4f}; share of T1's shift removed by the veto (upper bound on filament cores) {VET[ft]['share']:.3f}")
    OUT["numbers"]["veto"] = VET

    banner("DECISION (frozen; per branch, both footings, never pooled)")
    VER = {}
    for br in BRANCHES:
        rows = [TAB[f"T1_{br}_{ft}_N256"]["z0"] for ft in FOOTS if f"T1_{br}_{ft}_N256" in TAB]
        if len(rows) == 2:
            v, ds, dp = verdict(rows); VER[br] = dict(verdict=v, max_sig8_shift=ds, max_pk_dev=dp)
            P(f"  T1 A0-{br:4s}: {v:9s} (max |sigma8 ratio - 1| {ds:.4f}, max |P ratio - 1| (k<=1) {dp:.4f})" + ("   [LANE VERDICT]" if br == "FLAT" else "   [reported only]" if br == "DE" else "   [separate branch]"))
    for br in BRANCHES:
        rows = [TAB[f"S1_{br}_{ft}_N256"]["z0"] for ft in FOOTS if f"S1_{br}_{ft}_N256" in TAB]
        if len(rows) == 2:
            v, ds, dp = verdict(rows); VER["S1_" + br] = dict(verdict=v, max_sig8_shift=ds, max_pk_dev=dp)
            P(f"  S1 A0-{br:4s}: {v:9s} (max |sigma8 ratio - 1| {ds:.4f}) [reported]")
    OUT["numbers"]["verdicts"] = VER

    banner("CONTROLS C2, C3")
    s1 = [TAB[f"S1_FLAT_{ft}_N256"]["z0"]["sig8"] for ft in FOOTS]
    check("C2 S1 (bare chassis, A0-FLAT) sigma8/S0 >= 1.5 on both footings", min(s1) >= 1.5, " / ".join(f"{x:.3f}" for x in s1))
    r0l, _ = load("S0", "FLAT", "canonical", n=128); r1l, _ = load("T1", "FLAT", "canonical", n=128)
    lo = ratios(r1l, r0l, "z0"); hi = TAB["T1_FLAT_canonical_N256"]["z0"]
    vlo = verdict([lo])[0]; vhi = verdict([hi])[0]
    OUT["numbers"]["C3"] = dict(N128=lo, N256=hi, verdict_N128=vlo, verdict_N256=vhi, on_vol_N128=r1l["snap"]["z0"]["vol_on"])
    check("C3 resolution: T1 A0-FLAT canonical verdict category unchanged 128^3 -> 256^3", vlo == vhi,
          f"sigma8 ratio {lo['sig8']:.4f} (128^3) vs {hi['sig8']:.4f} (256^3); ON vol {r1l['snap']['z0']['vol_on']:.4f} vs {r0 and load('T1','FLAT','canonical')[0]['snap']['z0']['vol_on']:.4f}; {vlo} vs {vhi}")

json.dump(OUT, open(os.path.join(HERE, f"cfg359_native_pm_growth_results{SUF}.json"), "w"), indent=1)
open(os.path.join(HERE, f"cfg359_native_pm_growth{SUF}.out"), "w").write("\n".join(LOG) + "\n")
sys.exit(0 if all(c["pass"] for c in OUT["checks"].values()) or not MUTATE else 1)
