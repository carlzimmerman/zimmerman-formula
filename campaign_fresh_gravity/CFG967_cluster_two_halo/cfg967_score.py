#!/usr/bin/env python3
"""CFG967 stage B (criteria FROZEN_CRITERIA.md 908091f9b; AMENDMENT_A1.md 7a7faac97): add the framework's catalogue two-halo term
(stage A, cfg967_tables.npz) to the law's cluster prediction and recompute A_MID, A_OUTER, the outer DeltaSigma-Mgas slope and
the gas terciles with CFG687's own stack, jackknife and T2 code, on both footings (never pooled).
Law kernels: nu_s = AQUAL mu = x/(1+x) in spherical symmetry (primary; record's current statement); nu_mono (CFG687's, continuity).
Run: OMP_NUM_THREADS=1 nice -n 10 python3 -u cfg967_score.py                 (main: amplitude x1)
     CFG967_MUTATE=1 ... cfg967_score.py                                       (MUTATE: amplitude x0 and x2, separate outputs)
kappa = 1/2 FITTED; not theory closed.
"""
import os, sys
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_v] = "1"
import contextlib, io, json, math, time
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__)); LANES = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(LANES, "CFG903_framework_two_halo_kids"))
import cfg903_lib as L                                                        # noqa: E402  (watchdog only)
L.LIM_RSS, L.LIM_T = 0.95e9, 30 * 60
L.start_watchdog("CFG967 score")
MUT = os.environ.get("CFG967_MUTATE") == "1"; SFX = "_MUTATE" if MUT else ""
OUT, CHK = [], {}
def P(s=""):
    print(s, flush=True); OUT.append(str(s))
def check(name, ok, msg):
    CHK[name] = bool(ok); P(f"  [{'PASS' if ok else 'FAIL'}] {name}: {msg}")
FOOTS = ("canonical", "alt")

# ============================================================== CFG686 / CFG687 machinery (CFG949's exec recipe, read-only)
sys.path.insert(0, LANES)
_mut_env = os.environ.pop("MUTATE", None)
import CFG4_common as C4                                                      # noqa: E402
A0 = {"canonical": float(C4.A0["canonical"]), "alt": float(C4.A0["alt"])}
assert abs(A0["canonical"] - 9.3603e-11) < 1e-15 and abs(A0["alt"] - 1.1312e-10) < 1e-15
SRC686 = os.path.join(LANES, "CFG686_cluster_shear_vs_law", "cfg686_shear.py"); TXT686 = open(SRC686).read()
NS6 = {"__file__": SRC686, "__name__": "cfg686"}
_argv = sys.argv; sys.argv = [SRC686, "UNUSED"]
with contextlib.redirect_stdout(io.StringIO()) as _buf:
    exec(TXT686.split("# ---- sources ----")[0], NS6)
    NS6["EDGES"] = np.logspace(np.log10(0.15), np.log10(3.0), 9); NS6["RC"] = np.sqrt(NS6["EDGES"][1:] * NS6["EDGES"][:-1]); NS6["M_BIAS"] = -0.01
    exec(TXT686.split("# ---- the law's prediction from ACCEPT gas ----")[1].split("# ---- measure ----")[0], NS6)
sys.argv = _argv
def nu_s(y):                                                                  # AQUAL mu = x/(1+x), spherical: g = nu_s(g_N/a0) g_N
    y = np.maximum(np.asarray(y, float), 1e-300)
    return 0.5 + np.sqrt(0.25 + 1.0 / y)
TXT687 = open(os.path.join(LANES, "CFG687_erass1_shear_stack", "cfg687_stack.py")).read()
LAWSRC = "def law(" + TXT687.split("def law(")[1].split("BR = [")[0]
LAW = {}
for kern, nu in (("mono", C4.nu_mono), ("s", nu_s)):
    ns = dict(RGRID=NS6["RGRID"], MPC=NS6["MPC"], MSUN=NS6["MSUN"], G=NS6["G"], nu_mono=nu, sigma_proj=NS6["sigma_proj"],
              RC=NS6["RC"], KG=NS6["KG_PER_MSUN_PC2"], np=np)
    exec(LAWSRC, ns); LAW[kern] = ns["law"]                                   # CFG687 law(), verbatim; kernel bound by name

# ============================================================== data (CFG687 per-cluster file) and CFG687's stack code (verbatim)
PC = np.load(os.path.join(LANES, "CFG687_erass1_shear_stack", "cfg687_percluster.npz"))
D, E, PL, PN, mg, zc, ra, dec, R500 = (np.asarray(PC[k], float) for k in ("D", "E", "PL", "PN", "mg", "z", "ra", "dec", "R500"))
N = len(mg)
W = np.where(E > 0, 1 / E ** 2, 0)
order = np.argsort(ra); patch = np.empty(N, int); patch[order] = np.arange(N) * 30 // N
BANDS = {"INNER": [0, 1, 2], "MID": [3, 4, 5], "OUTER": [6, 7]}
q = np.quantile(mg, [0, 1 / 3, 2 / 3, 1]); tid = np.clip(np.digitize(mg, q[1:-1]), 0, 2)
def A_of(sel, Pm):
    return {b: (W[sel][:, j] * D[sel][:, j]).sum() / (W[sel][:, j] * Pm[sel][:, j]).sum() for b, j in BANDS.items()}
def jk(fun, base=None):
    base = np.ones(N, bool) if base is None else base
    full = fun(base); reps = [fun(base & (patch != p)) for p in range(30)]
    return {k: (float(full[k]), float(np.sqrt(29 / 30 * np.sum((np.array([r[k] for r in reps]) - np.mean([r[k] for r in reps])) ** 2)))) for k in full}
def outer_stack(sel, arr):
    j = BANDS["OUTER"]; return (W[sel][:, j] * arr[sel][:, j]).sum() / W[sel][:, j].sum()
def slope(sel, arr, t=None):
    t = tid if t is None else t; xs, ys = [], []
    for k in range(3):
        s = sel & (t == k); v = outer_stack(s, arr)
        if v <= 0: return np.nan
        xs.append(np.log10(np.median(mg[s]))); ys.append(np.log10(v))
    return np.polyfit(xs, ys, 1)[0]
ALL = np.ones(N, bool)
R687 = json.load(open(os.path.join(LANES, "CFG687_erass1_shear_stack", "cfg687_results.json")))
M2 = json.load(open(os.path.join(LANES, "CFG687_erass1_shear_stack", "cfg687_results_MUTATE_M2.json")))["A"]
OFF = {f: tuple(M2[f"{f}|b0.67|rc0.15|f0.20"]["OUTER"]) for f in FOOTS}       # random-minus-random OUTER offset (A units)
S_OBS = jk(lambda s: {"s": slope(s, D)})["s"]

P("=" * 110)
P(f"CFG967  framework catalogue two-halo term around 318 eRASS1 clusters (NA-5)" + ("   [MUTATE: amplitude x0 and x2]" if MUT else ""))
P("  criteria 908091f9b; amendment A1 7a7faac97 (d grid); kappa = 1/2 FITTED; footings never pooled; framework-native")

# ============================================================== law predictions, K1, K5
t0 = time.time()
PRED = {(k, f): np.array([LAW[k](dict(Mgas500=mg[i], R500=R500[i]), A0[f]) for i in range(N)]) for k in ("mono", "s") for f in FOOTS}
P(f"  law predictions: 2 kernels x 2 footings x {N} clusters in {time.time() - t0:.0f} s")
relPL = float(np.max(np.abs(PRED[("mono", "canonical")] / PL - 1)))
dA = 0.0
for key, Pm in (("canonical|b0.67|rc0.15|f0.20", PRED[("mono", "canonical")]), ("alt|b0.67|rc0.15|f0.20", PRED[("mono", "alt")]), ("newton", PN)):
    a = jk(lambda s, Pm=Pm: A_of(s, Pm))
    for b in ("MID", "OUTER"): dA = max(dA, abs(a[b][0] - R687["A"][key][b][0]), abs(a[b][1] - R687["A"][key][b][1]))
T2 = R687["T2"]
dS = max(abs(S_OBS[0] - T2["s_obs"]), abs(S_OBS[1] - T2["s_err"]), abs(slope(ALL, PRED[("mono", "canonical")]) - T2["s_law"]), abs(slope(ALL, PN) - T2["s_newton"]))
check("K1 CFG687 reproduced (nu_mono law = stored PL; A MID/OUTER canonical, alt, Newton; s_obs, s_err, s_law, s_N)",
      relPL <= 1e-9 and dA <= 1e-6 and dS <= 1e-6, f"PL max rel {relPL:.1e}; A max |d| {dA:.1e}; slopes max |d| {dS:.1e}")
yy = np.logspace(-4, 4, 2001); xx = yy * nu_s(yy); k5 = float(np.max(np.abs(xx * xx / (1 + xx) / yy - 1)))
check("K5 nu_s solves mu(x) x = y with mu = x/(1+x)", k5 <= 1e-12, f"max rel {k5:.1e} on y in [1e-4, 1e4]")
P(f"  s_obs = {S_OBS[0]:.4f} +/- {S_OBS[1]:.4f} (CFG687); random-minus-random OUTER offset (A units): canonical {OFF['canonical'][0]:+.3f} +/- {OFF['canonical'][1]:.3f}, alt {OFF['alt'][0]:+.3f} +/- {OFF['alt'][1]:.3f}")

# ============================================================== two-halo tables (stage A)
TB = np.load(os.path.join(HERE, "cfg967_tables.npz"))
RC2 = TB["RC2"]
def T_of(foot, key):
    if key == "C2p":
        return (TB[f"L_{foot}|V1P1X1"] - TB[f"R_{foot}|V1P1X1"]) * RC2[:, None]
    return TB[f"L_{foot}|{key}"] - TB[f"R_{foot}|{key}"]
SPEC = {"primary": ("s", "V0P1X1"), "X2": ("s", "V0P1X2"), "X3": ("s", "V0P1X3"), "E0": ("s", "V0P1E0"), "C0": ("s", "V1P1X1"),
        "C2p": ("s", "C2p"), "W300": ("s", "V2P1X1"), "W1000": ("s", "V3P1X1"), "P0": ("s", "V0P0X1"), "P2": ("s", "V0P2X1"),
        "M1": ("s", "V4P1X1"), "nu_mono": ("mono", "V0P1X1")}
DOUBLE = ("X2", "E0")                                                          # double-counting brackets (criteria section 6)
RANK = {"MOVES AWAY": 0, "NO EFFECT": 0, "PARTIAL": 1, "EXPLAINS": 2}

def evaluate(foot, kern, T, amp):
    Pb = PRED[(kern, foot)]; Pa = Pb + amp * T
    Ab = jk(lambda s: A_of(s, Pb)); Aa = jk(lambda s: A_of(s, Pa))
    sb = float(slope(ALL, Pb)); sa = float(slope(ALL, Pa))
    reps = np.array([slope(patch != p, Pa) for p in range(30)]); sa_err = float(np.sqrt(29 / 30 * np.sum((reps - reps.mean()) ** 2)))
    ds = sa - sb
    stot = math.hypot(Aa["OUTER"][1], OFF[foot][0])
    ok_s = abs(sa - S_OBS[0]) <= S_OBS[1]; ok_a = abs(Aa["OUTER"][0] - 1) <= 2 * stot
    if ok_s and ok_a: cls = "EXPLAINS"
    elif ds >= 0.10: cls = "PARTIAL" + (" (slope reached, A_OUTER inconsistent)" if ok_s else "")
    elif ds <= -0.10: cls = "MOVES AWAY"
    else: cls = "NO EFFECT"
    touch = abs(Aa["MID"][0] - Ab["MID"][0]) >= Ab["MID"][1]
    return dict(A_before=Ab, A_after=Aa, s_before=sb, s_after=sa, s_after_jk=sa_err, ds=ds, sigma_tot_outer=stot,
                A_outer_minus_offset=Aa["OUTER"][0] - OFF[foot][0], z_outer=(Aa["OUTER"][0] - 1) / stot, cls=cls, touches_A_MID=bool(touch))
def base_cls(c): return c.split(" (")[0]
def band_sel(Pm, sel):                                                        # CFG949's subset jackknife (A per band on a subset)
    def A(s): return {b: float((W[s][:, j] * D[s][:, j]).sum() / (W[s][:, j] * Pm[s][:, j]).sum()) for b, j in BANDS.items()}
    full = A(sel); reps = [A(sel & (patch != p)) for p in range(30)]
    return {k: (full[k], float(np.sqrt(29 / 30 * np.sum((np.array([r[k] for r in reps]) - np.mean([r[k] for r in reps])) ** 2)))) for k in full}
def wmean(sel, arr, band):
    j = BANDS[band]; return float((W[sel][:, j] * arr[sel][:, j]).sum() / W[sel][:, j].sum())

RES = dict(lane="CFG967", mutate=MUT, criteria="908091f9b", amendments=["7a7faac97"], s_obs=S_OBS, offset=OFF, checks=CHK, footings={})
AMPS = (0.0, 1.0, 2.0) if MUT else (1.0,)
for foot in FOOTS:
    P(f"\n{'-' * 110}\n  FOOTING {foot} (a0 {A0[foot]:.4e})")
    FR = {}
    for kern in ("s", "mono"):
        Pb = PRED[(kern, foot)]; Ab = jk(lambda s: A_of(s, Pb)); sb = slope(ALL, Pb)
        P(f"  law alone [{'AQUAL nu_s (primary)' if kern == 's' else 'nu_mono (CFG687)'}]: A_MID {Ab['MID'][0]:.3f} +/- {Ab['MID'][1]:.3f}, "
          f"A_OUTER {Ab['OUTER'][0]:.3f} +/- {Ab['OUTER'][1]:.3f}, s_law {sb:.4f}")
    for amp in AMPS:
        tag = f"x{amp:g}"; FR[tag] = {}
        for name, (kern, key) in SPEC.items():
            FR[tag][name] = evaluate(foot, kern, T_of(foot, key), amp)
        r = FR[tag]["primary"]
        P(f"\n  [{tag}] PRIMARY (AQUAL nu_s, X1 own catchment edge, C1', W500, P1, unmasked):")
        P(f"    A_MID   {r['A_before']['MID'][0]:.3f} +/- {r['A_before']['MID'][1]:.3f}  ->  {r['A_after']['MID'][0]:.3f} +/- {r['A_after']['MID'][1]:.3f}   (touches core excess: {r['touches_A_MID']})")
        P(f"    A_OUTER {r['A_before']['OUTER'][0]:.3f} +/- {r['A_before']['OUTER'][1]:.3f}  ->  {r['A_after']['OUTER'][0]:.3f} +/- {r['A_after']['OUTER'][1]:.3f}"
          f"   (sigma_tot {r['sigma_tot_outer']:.3f}, Z {r['z_outer']:+.2f}; minus offset {r['A_outer_minus_offset']:.3f})")
        P(f"    slope   {r['s_before']:.4f}  ->  {r['s_after']:.4f} (jk {r['s_after_jk']:.3f})   ds {r['ds']:+.4f}   vs s_obs {S_OBS[0]:.3f} +/- {S_OBS[1]:.3f}   ==> {r['cls']}")
        if amp == 1.0:
            P(f"    brackets (one at a time):")
            for name in SPEC:
                if name == "primary": continue
                b = FR[tag][name]
                P(f"      {name:8s}: A_MID {b['A_after']['MID'][0]:.3f}  A_OUTER {b['A_after']['OUTER'][0]:.3f} +/- {b['A_after']['OUTER'][1]:.3f}  "
                  f"s {b['s_before']:.4f} -> {b['s_after']:.4f} (ds {b['ds']:+.4f})  {b['cls']}")
    if 1.0 in AMPS:
        prim = FR["x1"]["primary"]
        FR["class_flips"] = [n for n in SPEC if n != "primary" and base_cls(FR["x1"][n]["cls"]) != base_cls(prim["cls"])]
        FR["double_count_only"] = (RANK[base_cls(prim["cls"])] == 0) and any(RANK[base_cls(FR["x1"][n]["cls"])] > 0 for n in DOUBLE)
        P(f"    class flips vs primary: {FR['class_flips'] or 'none'}; advance only in a double-counting bracket: {FR['double_count_only']}")
        # ---------------- terciles (CFG815's middle-tercile issue), before / after, primary kernel and T
        Tp = T_of(foot, "V0P1X1"); Pb = PRED[("s", foot)]; Pa = Pb + Tp
        terc = {}
        P(f"    gas terciles (A per band, subset jackknife), primary:")
        for k in range(3):
            s = tid == k; bb, aa = band_sel(Pb, s), band_sel(Pa, s)
            terc[k] = dict(n=int(s.sum()), Mgas_med=float(np.median(mg[s])), z_med=float(np.median(zc[s])), before=bb, after=aa,
                           T_outer=wmean(s, Tp, "OUTER"), T_mid=wmean(s, Tp, "MID"), law_outer=wmean(s, Pb, "OUTER"), law_mid=wmean(s, Pb, "MID"))
            P(f"      tercile {k} (N {terc[k]['n']}, Mgas {terc[k]['Mgas_med']:.2e}, z {terc[k]['z_med']:.3f}): "
              f"A_MID {bb['MID'][0]:.3f} -> {aa['MID'][0]:.3f} (+/- {aa['MID'][1]:.3f}); A_OUTER {bb['OUTER'][0]:.3f} -> {aa['OUTER'][0]:.3f} (+/- {aa['OUTER'][1]:.3f}); "
              f"two-halo OUTER {terc[k]['T_outer']:.2f} vs law {terc[k]['law_outer']:.2f} Msun/pc^2, MID {terc[k]['T_mid']:.2f} vs {terc[k]['law_mid']:.2f}")
        FR["terciles"] = terc
        # ---------------- reported only: two-halo stack, random-only term, host share, needed amplitude, Z17
        st = {b: jk(lambda s, b=b: {"v": wmean(s, Tp, b)})["v"] for b in ("INNER", "MID", "OUTER")}
        ro = {b: wmean(ALL, TB[f"R_{foot}|V0P1X1"], b) for b in ("MID", "OUTER")}
        hs = wmean(ALL, TB[f"L_{foot}|V0P1host"] - TB[f"R_{foot}|V0P1host"], "OUTER")
        FR["twohalo_stack"] = st; FR["random_only"] = ro; FR["host_outer"] = hs
        P(f"    two-halo stack (Msun/pc^2, jk): INNER {st['INNER'][0]:.2f} +/- {st['INNER'][1]:.2f}, MID {st['MID'][0]:.2f} +/- {st['MID'][1]:.2f}, "
          f"OUTER {st['OUTER'][0]:.2f} +/- {st['OUTER'][1]:.2f}; law OUTER {wmean(ALL, Pb, 'OUTER'):.2f}; random-only term MID {ro['MID']:.2f}, OUTER {ro['OUTER']:.2f}; "
          f"hosts (more massive than the cluster) OUTER {hs:.3f}")
        def s_of_amp(lam): return float(slope(ALL, Pb + lam * Tp))
        need = {}
        for lab, target in (("s_obs", S_OBS[0]), ("s_obs-1sig", S_OBS[0] - S_OBS[1])):
            lo, hi = 0.0, 200.0
            if not (s_of_amp(lo) < target <= s_of_amp(hi)):
                need[lab] = None; continue
            for _ in range(60):
                mid = 0.5 * (lo + hi)
                if s_of_amp(mid) < target: lo = mid
                else: hi = mid
            need[lab] = 0.5 * (lo + hi)
        FR["amplitude_needed"] = need
        P(f"    amplitude on the two-halo term needed for s_model = s_obs: {need['s_obs']}; for s_obs - 1 sigma: {need['s_obs-1sig']} (None = not reached for 0-200)")
        z17 = zc >= 0.17; q17 = np.quantile(mg[z17], [0, 1 / 3, 2 / 3, 1]); t17 = np.where(z17, np.clip(np.digitize(mg, q17[1:-1]), 0, 2), -1)
        so17 = slope(z17, D, t17); reps = np.array([slope(z17 & (patch != p), D, t17) for p in range(30)])
        Z17 = dict(n=int(z17.sum()), s_obs=float(so17), s_obs_err=float(np.sqrt(29 / 30 * np.nansum((reps - np.nanmean(reps)) ** 2))),
                   s_before=float(slope(z17, Pb, t17)), s_after=float(slope(z17, Pa, t17)), A=band_sel(Pa, z17), A_before=band_sel(Pb, z17))
        FR["Z17"] = Z17
        P(f"    Z17 (z >= 0.17, N {Z17['n']}, terciles re-cut): s_obs {Z17['s_obs']:.3f} +/- {Z17['s_obs_err']:.3f}; s_model {Z17['s_before']:.4f} -> {Z17['s_after']:.4f}; "
          f"A_OUTER {Z17['A_before']['OUTER'][0]:.3f} -> {Z17['A']['OUTER'][0]:.3f}")
        # ---------------- K4 random halves
        dh = TB[f"RA_{foot}"] - TB[f"RB_{foot}"]; k4 = jk(lambda s: {"v": wmean(s, dh, "OUTER")})["v"]
        ok4 = abs(k4[0]) <= 3 * k4[1]
        check(f"K4 random halves A - B, OUTER stack ({foot})", ok4, f"{k4[0]:+.3f} +/- {k4[1]:.3f} Msun/pc^2 ({k4[0] / k4[1]:+.2f} sigma; <= 3)")
        FR["K4"] = k4
    if MUT:
        r0, r1, r2 = FR["x0"]["primary"], FR["x1"]["primary"], FR["x2"]["primary"]
        Pb = PRED[("s", foot)]; Pm = PRED[("mono", foot)]
        ex0 = np.array_equal(Pb + 0.0 * T_of(foot, "V0P1X1"), Pb) and r0["s_after"] == r0["s_before"] and r0["A_after"] == r0["A_before"]
        key = f"{foot}|b0.67|rc0.15|f0.20"; rm = FR["x0"]["nu_mono"]
        d687 = max(abs(rm["A_after"][b][0] - R687["A"][key][b][0]) for b in ("MID", "OUTER"))
        if foot == "canonical": d687 = max(d687, abs(rm["s_after"] - T2["s_law"]))
        check(f"MUTATE x0 reproduces 'before' exactly and CFG687 ({foot})", ex0 and d687 <= 1e-6, f"arrays equal {ex0}; nu_mono vs CFG687 JSON max |d| {d687:.1e}")
        b2 = abs(r2["s_after"] - r0["s_after"]); b1 = abs(r1["s_after"] - r0["s_after"])
        bite = b2 >= 0.01 and b2 > b1
        check(f"MUTATE x2 moves the slope ({foot})", bite, f"|s(x2) - s(x0)| = {b2:.4f} (>= 0.01 and > |s(x1) - s(x0)| = {b1:.4f})")
        FR["mutate"] = dict(s_x0=r0["s_after"], s_x1=r1["s_after"], s_x2=r2["s_after"], bite=bool(bite))
    RES["footings"][foot] = FR

if not MUT:
    cl = {f: RES["footings"][f]["x1"]["primary"]["cls"] for f in FOOTS}
    head = min((base_cls(c) for c in cl.values()), key=lambda c: RANK[c]) if len({base_cls(c) for c in cl.values()}) > 1 else base_cls(cl["canonical"])
    RES["class"] = dict(per_footing=cl, headline=head)
    P(f"\n{'=' * 110}\n  READING (primary, per footing): canonical {cl['canonical']}; alt {cl['alt']}  ==> headline {head}")
    for f in FOOTS:
        fr = RES["footings"][f]
        P(f"    {f}: flips {fr['class_flips'] or 'none'}; double-count-only advance {fr['double_count_only']}; A_MID touched {fr['x1']['primary']['touches_A_MID']}")
RES["runtime_s"] = round(time.time() - L.T0, 1); RES["peak_current_rss_MB"] = round(L.PEAK_CUR[0] / 1e6, 1)
P(f"\n  checks {sum(CHK.values())}/{len(CHK)} PASS; runtime {RES['runtime_s']} s; peak current RSS {RES['peak_current_rss_MB']} MB")
P("  kappa = 1/2 FITTED; footings never pooled; raw KiDS data, framework-native neighbours; not theory closed.")
json.dump(RES, open(os.path.join(HERE, f"cfg967_results{SFX}.json"), "w"), indent=1, default=float)
open(os.path.join(HERE, f"cfg967_score{SFX}.out"), "w").write("\n".join(OUT) + "\n")
sys.exit(0 if all(CHK.values()) else 1)
