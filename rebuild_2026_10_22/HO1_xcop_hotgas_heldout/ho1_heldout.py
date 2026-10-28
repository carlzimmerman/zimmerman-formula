#!/usr/bin/env python3
"""HO1_xcop_hotgas_heldout: the frozen CL2 picture (switch 10^12.3, S9 L 4 c_f slope, X43 collapse cores, GS1 native fair-share
cluster budget) graded on held-out data: (a) CS2's 35 X-COP profile points, CS2's rule; (b) the picture's prediction of
HG2's hot/faint group statistic D against HG2's measured 95% interval.

Frozen criteria: FROZEN_CRITERIA.md + ASSUMPTION_LEDGER.md (95341eda1a, committed alone before this script).
CL2's source (up to its K0 block), CS2's X-COP grader and HG2 / HG1's functions are executed read-only.
kappa = 1/2 FITTED; footings never pooled; cold dark energy = gravitating w ~ 0 field component, never a particle;
not theory closed; nothing here says the data favour the framework.

    PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 ho1_heldout.py                 -> ho1_heldout.out, _results.json
    HO1_MUTATE=1 PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 ho1_heldout.py    -> _MUTATE outputs (exit 1 = teeth bite)
"""
import os, sys, io, csv, json, math, time, hashlib, resource, contextlib, warnings
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"): os.environ[_v] = "1"
for _v in ("CL2_MUTATE", "X53_MUTATE", "X30_MUTATE", "MUTATE", "CS2_MUTATE"): os.environ.pop(_v, None)
import numpy as np
from scipy.optimize import minimize_scalar, brentq
from astropy.io import fits
warnings.filterwarnings("ignore", category=RuntimeWarning)

T0 = time.time()
MUTATE = os.environ.get("HO1_MUTATE") == "1"
TAG = "_MUTATE" if MUTATE else ""
HERE = os.path.dirname(os.path.abspath(__file__)); REB = os.path.dirname(HERE); REPO = os.path.dirname(REB)
OUT = []
def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); OUT.append(s)
def rss(): return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / (1e9 if sys.platform == "darwin" else 1e6)
def sha(p): return hashlib.sha256(open(p, "rb").read()).hexdigest()
checks = []
def check(k, ok, msg):
    checks.append((k, bool(ok))); P(f"{k} {'PASS' if ok else 'FAIL'}  {msg}")
FEET = ("canonical", "alt"); SEED = 20261025
P(f"HO1_xcop_hotgas_heldout  {'MUTATE (m1 CL2 flag + shape inverted; m2 S0-HG2 target x1.01)' if MUTATE else 'normal run'}  (frozen 95341eda1a; AMENDMENT A1 af70a0b593)")
P("kappa = 1/2 FITTED; footings never pooled; route E above the switch, the law on baryons below; cold dark energy, not matter; not theory closed")
RES = dict(frozen="95341eda1a", mutate=MUTATE, sources={}, step0={}, footings={f: {} for f in FEET}, checks={})
SRC = {"CL2_script": "CL2_native_cf_slope/cl2_native_slope.py", "CL2_target": "CL2_native_cf_slope/x62_x43copy_on_shpS9_L4_T12.3_B_results.json",
       "X43_script": "X43_collapse_core_floor/x43_collapse_core.py", "GS1_results": "GS1_measured_gas_outskirts/gs1_gas_slope_results.json",
       "CS2_script": "CS2_core_law_out_of_sample/cs2_out_of_sample.py", "CS2_results": "CS2_core_law_out_of_sample/cs2_out_of_sample_results.json",
       "GR1_results": "GR1_core_law_groups_ellipticals/gr1_groups_ellipticals_results.json",
       "HG2_script": "HG2_kids_lowg_hot_gas/hg2_kids_lowg_hot_gas.py", "HG2_results": "HG2_kids_lowg_hot_gas/hg2_kids_lowg_hot_gas.json",
       "HG1_script": "HG1_hot_gas_selector/hg1_hot_gas_selector.py", "X48_A2": "X48_native_cf_zoom/x48_analyze_results_ng48_A2.json",
       "EM1_results": "EM1_emergent_dust_law/em1_emergent_results.json"}
for k, p in SRC.items(): RES["sources"][k] = sha(os.path.join(REB, p))
P("sources sha256: " + ", ".join(f"{k} {v[:12]}" for k, v in RES["sources"].items()))

# ------------------------------------------------------------------ 1. CL2 namespace (read-only, up to its K0 block)
TC = open(os.path.join(REB, SRC["CL2_script"])).read()
codeC = TC[:TC.index("# ---------- K0: route E alone reproduces the source lanes")]
old = '    return ns["RES"], ns["LAW"]'; assert codeC.count(old) == 1
codeC = codeC.replace(old, '    LASTNS["ns"] = ns\n' + old)
C = {"__file__": os.path.join(HERE, "cl2_ro.py"), "__name__": "cl2_ro", "LASTNS": {}}
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(codeC, os.path.join(REB, SRC["CL2_script"]), "exec"), C)
if MUTATE: C["MUTATE"] = True; C["TAG"] = "_MUTATE"                                     # m1: CL2's own twin inside the namespace
CFTAB = C["cf_table"]("S9", 4.0)
k4 = all(abs(a - b) <= 0.01 for a, b in zip(CFTAB, [6.37, 4.5, 4.0]))
check("K4", k4, f"c_f(1e12/13/14) = {[round(v, 3) for v in CFTAB]} vs CL2 [6.37, 4.5, 4.0]")
C["STAT"].clear()
R43, _ = C["run_x43"]("on", "shpS9_L4_T12.3_B")
NS = C["LASTNS"]["ns"]; NX = NS["NX"]
stat43 = {k: dict(v) for k, v in C["STAT"].items()}
P(f"CL2 X43 copy at shpS9_L4_T12.3_B run in this lane [{time.time() - T0:.0f} s, RSS {rss():.2f} GB]")
# S0-CL2
TJ = json.load(open(os.path.join(REB, SRC["CL2_target"])))
dmax = 0.0
for f in FEET:
    a, b = R43["footings"][f], TJ["footings"][f]
    for t in b["sparc"]: dmax = max(dmax, abs(a["sparc"][t]["rms"] - b["sparc"][t]["rms"]))
    dmax = max(dmax, abs(a["groups"]["mean"] - b["groups"]["mean"]), abs(a["groups"]["Z"] - b["groups"]["Z"]))
    for hk in b["clusters"]["cells"]:
        for k in b["clusters"]["cells"][hk]: dmax = max(dmax, abs(a["clusters"]["cells"][hk][k]["pred"] - b["clusters"]["cells"][hk][k]["pred"]))
s0cl2 = dmax <= 1e-9
check("S0-CL2", s0cl2, f"CL2 S9 L4 T12.3 X43 grade reproduced (SPARC rms, groups mean/Z, 2 x 15 cluster preds per footing): max |d| {dmax:.1e}"
      + "; canonical groups Z " + f"{R43['footings']['canonical']['groups']['Z']:+.2f}, G-OUT-all Z {R43['footings']['canonical']['clusters']['cells']['h0672']['G-OUT-all']['Z']:+.2f}")
RES["step0"]["CL2_maxdiff"] = dmax

GE, MSUNE, MPCE, A0 = NS["GE"], NS["MSUNE"], NS["MPCE"], NS["A0"]
sig_core, solve_r0, Bk, SAT, BGS = NS["sig_core"], NS["solve_r0"], NS["B"], NS["SAT"], NS["BGS"]
LF_G, nu = C["LF_G"], C["nu"]; NAT_RRAT = C["NAT_RRAT"]
r_ta_com, gc2_ext, RG, RM, MPCX, MSUNX = NX["r_ta_com"], NX["_gc2_ext"], NX["RG"], NX["RM"], NX["MPC"], NX["MSUN"]
assert ("Mfair=%r*Mbt" % NAT_RRAT) in NS["codeX"] and "_gc2_ext" in NS["codeX"]
TBG = "A_c2b_refit"; T_SW = 12.3

# ------------------------------------------------------------------ 2. CS2's X-COP grader (read-only) and S0-CS2
TS = open(os.path.join(REB, SRC["CS2_script"])).read()
codeS = TS[TS.index("# ------------------------------------------------------------------ X-COP (matched-clumping profiles)"):
           TS.index("# ------------------------------------------------------------------ graders per law")]
CJ = json.load(open(os.path.join(REB, SRC["CS2_results"])))
S = {"os": os, "np": np, "math": math, "csv": csv, "fits": fits, "minimize_scalar": minimize_scalar, "brentq": brentq, "REPO": REPO,
     "check": (lambda k, ok, msg: check("K5", ok, msg)), "R0C": CJ["calibration"]["r0_law"]["c"], "R0P": CJ["calibration"]["r0_law"]["p"], "SREF": 70.50}
exec(compile(codeS, os.path.join(REB, SRC["CS2_script"]), "exec"), S)
XC = S["XC"]
SREFM = float(json.load(open(os.path.join(REB, SRC["GR1_results"])))["sigma_ref"])
QF = {"canonical": 0.892, "alt": 0.748}
SPC = MSUNE / 3.0857e16 ** 2
d0 = []
cs2x = S["xcop"](CJ["calibration"]["A"], CJ["calibration"]["q"], 70.50)
os1x = {f: S["xcop"](math.log10(NS["SIG"][f] / SPC), QF[f], SREFM) for f in FEET}
for f in FEET:
    for lab, got, ref in (("CS2", cs2x, CJ["footings"][f]["CS2"]["xcop"]), ("OS1", os1x[f], CJ["footings"][f]["OS1"]["xcop"])):
        d0 += [abs(got["mean"] - ref["mean"]), abs(got["rms"] - ref["rms"]), abs(got["n"] - ref["n"]), abs(got["saturated"] - ref["saturated"])]
s0cs2 = max(d0) <= 1e-9
check("S0-CS2", s0cs2, f"CS2 X-COP grader reproduces CS2 (law {cs2x['mean']:+.3f}/{cs2x['rms']:.3f}) and OS1 comparator ("
      + ", ".join(f"{f} {os1x[f]['mean']:+.3f}/{os1x[f]['rms']:.3f}" for f in FEET) + f"): max |d| {max(d0):.1e}")
RES["step0"]["CS2_maxdiff"] = max(d0); RES["step0"]["CS2_xcop"] = dict(CS2=cs2x, OS1=os1x)

# ------------------------------------------------------------------ 3. HG2 / HG1 (read-only) and S0-HG2
sys.path.insert(0, os.path.join(REB, "HG2_kids_lowg_hot_gas"))
with contextlib.redirect_stdout(io.StringIO()):
    import hg2_kids_lowg_hot_gas as hg2
hg1 = hg2.hg1
HJ = json.load(open(os.path.join(REB, SRC["HG2_results"])))
rng = np.random.default_rng(SEED)
gb, go, Cv = hg2.load(*hg2.BLUE); A1, sA1 = hg2.k1_amp(gb, go, Cv)
groups, mem = hg1.load_groups(); erass = hg1.load_erass()
rows, drops = hg1.build(groups, mem, erass)
ref = hg2.Ref(gb, go, Cv); base = hg2.deltas(rows, ref)
pw = hg1.power(rows, base, rng)
D0, nb0, nf0 = hg1.D_stat(rows, base)
lo0, hi0, nbad0 = hg2.bootstrap(rows, ref, rng)
arms0 = {fl: float(np.median([d for r, d in zip(rows, base) if r["flag"] == fl and np.isfinite(d)])) for fl in ("BRIGHT", "FAINT")}
nsup = int(np.isfinite(base).sum()); nB = sum(r["flag"] == "BRIGHT" for r in rows)
tD = HJ["D"] * (1.01 if MUTATE else 1.0)                                                   # m2
dh = max(abs(A1 - HJ["k1"][0]), abs(sA1 - HJ["k1"][1]), abs(D0 - tD), abs(lo0 - HJ["ci95"][0]), abs(hi0 - HJ["ci95"][1]), abs(pw - HJ["power"]),
         abs(arms0["BRIGHT"] - HJ["arms"]["BRIGHT"]["median"]), abs(arms0["FAINT"] - HJ["arms"]["FAINT"]["median"]))
s0hg2 = dh <= 1e-9 and (len(rows), nB, nsup, nb0, nf0) == (190, 14, 188, HJ["n_bright"], HJ["n_faint"])
check("S0-HG2", s0hg2, f"HG2 reproduced: K1 A {A1:.4f}+-{sA1:.4f}; {len(rows)} groups, BRIGHT {nB}, supported {nsup}; D {D0:+.4f} [{lo0:+.4f}, {hi0:+.4f}], power {pw:.3f}; "
      f"arm medians B {arms0['BRIGHT']:+.3f} F {arms0['FAINT']:+.3f}: max |d| {dh:.1e}{' (target x1.01, m2)' if MUTATE else ''}")
RES["step0"]["HG2_maxdiff"] = dh; RES["step0"]["HG2"] = dict(D=D0, ci95=[lo0, hi0], power=pw, n_bright=nb0, n_faint=nf0)
if not (s0cl2 and s0cs2 and s0hg2) and not MUTATE:
    P("STOPPED AT STEP 0"); RES["verdict"] = "STOPPED AT STEP 0"; RES["checks"] = {k: v for k, v in checks}
    open(os.path.join(HERE, "ho1_heldout.out"), "w").write("\n".join(OUT).replace(REPO, "<repo>") + "\n")
    json.dump(RES, open(os.path.join(HERE, "ho1_heldout_results.json"), "w"), indent=1, default=float); sys.exit(1)

# ------------------------------------------------------------------ 4. (a) X-COP under the CL2 picture
PCm = 3.0857e16
XMETA = {}
for c in XC:
    p_ = os.path.join(REPO, "real_research", "data", "xcop", c["name"])
    with fits.open(os.path.join(p_, f"{c['name']}_hydro_mass.fits")) as h: z = float(h[1].header["REDSHIFT"]); r500 = float(h[1].header["R500"])
    with fits.open(os.path.join(p_, f"{c['name']}_fgas_profile.fits")) as h: gas = h[1].data.copy(); rg500 = h[1].header["R500"]
    XMETA[c["name"]] = dict(z=z, r500=r500, Mg500=S["li"](gas["RADIUS"] * rg500, gas["MGAS"], r500))
def budget(name, start_fac=1.0):
    m = XMETA[name]; R5 = m["r500"] / 1e3
    Mbx, Mbt = gc2_ext(m["Mg500"], R5, m["z"], start_fac * 3.0 * 1.2 * m["Mg500"] * MSUNX)
    rta = r_ta_com(Mbt) / (1 + m["z"])
    fp = abs(float(np.interp(rta, RM, Mbx)) / Mbt - 1)
    return Mbt, rta, fp
def xcop_cl2(foot):
    d, per, info = [], {}, {}; sat0 = SAT["n"]; sw_ok = True; k2 = []; k3 = []
    for c in XC:
        Mbt, rta, fp = budget(c["name"])
        alt_ = [budget(c["name"], s_)[0] for s_ in (0.3, 3.0)]
        k2.append(max(abs(v / Mbt - 1) for v in alt_))                                  # AMENDMENT A1: start independence only
        Mfair = NAT_RRAT * Mbt; Mtot = (Mfair + Mbt) / MSUNE
        s, above = sig_core(foot, TBG, Mtot); sw_ok &= bool(above) and math.log10(Mtot) > T_SW
        n0 = SAT["n"]; r0 = solve_r0(Mfair, rta, s); sat = SAT["n"] > n0
        k3.append(True if sat else abs(math.pi * s * r0 ** 2 * float(Bk(rta / r0)) / Mfair - 1) < 1e-8)
        dd = []
        for x, r, mh, mb in c["rows"]:
            if x > 0.75: continue
            rm = r * 1e3 * PCm
            Mh = math.pi * s * r0 ** 2 * float(Bk(min(rm, rta) / r0))
            gbv, ghv = GE * mb * MSUNE / rm ** 2, GE * Mh / rm ** 2
            g = float(LF_G(gbv, ghv, A0[foot], "xcop", bool(above)))
            dd.append((x, math.log10(GE * mh * MSUNE / rm ** 2 / g)))
        d += [v for _, v in dd]; per[c["name"]] = float(np.mean([v for _, v in dd]))
        info[c["name"]] = dict(logM=math.log10(Mtot), Sigma_pc2=s * PCm ** 2 / MSUNE, r0_kpc=r0 / PCm / 1e3, rta_Mpc=rta / MPCX,
                               Mbt_over_Mg500=Mbt / (XMETA[c["name"]]["Mg500"] * MSUNX), saturated=bool(sat),
                               Mh_R500_over_Mdata=float(math.pi * s * r0 ** 2 * Bk(XMETA[c["name"]]["r500"] * 1e3 * PCm / r0) / MSUNE /
                                                        [r for r in c["rows"] if abs(r[0] - 1.0) < 1e-9][0][2]))
    d = np.array(d); xs = [x for c in XC for x, *_ in c["rows"] if x <= 0.75]
    byx = {f"{x:g}": float(np.mean([v for v, xx in zip(d, xs) if abs(xx - x) < 1e-9])) for x in (0.1, 0.2, 0.3, 0.5, 0.7)}
    mean, rms = float(d.mean()), float(np.sqrt(np.mean(d ** 2)))
    ok = abs(mean) <= 0.05 and rms <= 0.10
    return dict(mean=mean, rms=rms, n=len(d), saturated=SAT["n"] - sat0, per_cluster=per, by_x=byx, info=info,
                verdict="PASS" if ok else ("FAIL (" + "+".join(([] if abs(mean) <= 0.05 else ["mean"]) + ([] if rms <= 0.10 else ["rms"])) + (", OVER)" if mean < 0 else ", UNDER)")),
                switch_ok=sw_ok, k2=max(k2), k3=all(k3))                                  # A1 label

# ------------------------------------------------------------------ 5. (b) HG2 groups under the CL2 picture
EMG = {}
for e in erass: EMG.setdefault(e[0], []).append(e)
assert all(len(EMG[r["erass"]]) == 1 for r in rows if r["flag"] == "BRIGHT")
def group_pred(foot, mstar_only=False):
    bg = BGS[TBG]; rc = 3 * (100 * bg["h"] * 1e3 / MPCE) ** 2 / (8 * math.pi * GE)
    gp, above_l, k1, k3 = [], [], True, True
    for r in rows:
        mg500 = 0.0 if (r["flag"] != "BRIGHT" or mstar_only) else float(EMG[r["erass"]][0][4])
        lMb = math.log10(r["mstar"] + mg500); M200 = 10 ** (bg["a"] + bg["b"] * (lMb - 10))
        R200 = (3 * M200 * MSUNE / (4 * math.pi * 200 * rc)) ** (1 / 3)
        s, above = sig_core(foot, TBG, M200); n0 = SAT["n"]; r0 = solve_r0(M200 * MSUNE, R200, s); sat = SAT["n"] > n0
        if not sat: k3 &= abs(math.pi * s * r0 ** 2 * float(Bk(R200 / r0)) / (M200 * MSUNE) - 1) < 1e-8
        rr = r["r_mpc"] * hg1.MPC; Mh = math.pi * s * r0 ** 2 * float(Bk(min(rr, R200) / r0)); gh = GE * Mh / rr ** 2
        g = float(LF_G(r["gbar"], gh, A0[foot], "hg2", bool(above)))
        exp = r["gbar"] + gh if above else r["gbar"] * float(nu(r["gbar"] / A0[foot]))
        k1 &= bool(above) == (M200 > 10 ** T_SW) and abs(g / exp - 1) < 1e-12
        gp.append(g); above_l.append(bool(above))
    return np.array(gp), np.array(above_l), k1, k3
def hg2_cl2(foot):
    gp, ab, k1, k3 = group_pred(foot)
    dpred = np.log10(gp) - ref.logref(np.array([r["gbar"] for r in rows]))
    Dp, nbp, nfp = hg1.D_stat(rows, dpred)
    ok = lo0 <= Dp <= hi0
    sup = np.isfinite(base)
    dres = np.where(sup, np.log10(np.array([r["gobs"] for r in rows])) - np.log10(gp), np.nan)
    rr_ = np.random.default_rng(SEED); pwr = hg1.power(rows, dres, rr_)
    Dr, nbr, nfr = hg1.D_stat(rows, dres)
    ib = [i for i, r in enumerate(rows) if r["flag"] == "BRIGHT" and sup[i]]; i_f = [i for i, r in enumerate(rows) if r["flag"] == "FAINT" and sup[i]]
    bs = []
    for _ in range(2000):
        pick = list(rr_.choice(ib, len(ib))) + list(rr_.choice(i_f, len(i_f)))
        bs.append(hg1.D_stat([rows[i] for i in pick], dres[pick])[0])
    bs = np.array(bs); bs = bs[np.isfinite(bs)]; lr, hr = float(np.percentile(bs, 2.5)), float(np.percentile(bs, 97.5))
    arms = {fl: dict(n=int(sum(1 for i in range(len(rows)) if rows[i]["flag"] == fl and sup[i])),
                     median_res=float(np.median([dres[i] for i in range(len(rows)) if rows[i]["flag"] == fl and sup[i]])),
                     median_pred_vs_ref=float(np.median([dpred[i] for i in range(len(rows)) if rows[i]["flag"] == fl and sup[i]])),
                     frac_above=float(np.mean([ab[i] for i in range(len(rows)) if rows[i]["flag"] == fl and sup[i]]))) for fl in ("BRIGHT", "FAINT")}
    gp2, ab2, _, _ = group_pred(foot, mstar_only=True)
    Dv = hg1.D_stat(rows, np.log10(gp2) - ref.logref(np.array([r["gbar"] for r in rows])))[0]
    return dict(D_pred=float(Dp), n_bright=nbp, n_faint=nfp, interval=[lo0, hi0],
                verdict="PASS" if ok else ("FAIL (ABOVE)" if Dp > hi0 else "FAIL (BELOW)"),
                reported=dict(D_res=float(Dr), ci95_res=[lr, hr], power=float(pwr), cls_res=hg1.classify(Dr, lr, hr, nbr, nfr, pwr), arms=arms,
                              D_pred_mstar_only=float(Dv), frac_above_mstar_only=dict(BRIGHT=float(np.mean(ab2[[i for i in ib]])), FAINT=float(np.mean(ab2[[i for i in i_f]])))),
                k1=k1, k3=k3)

# ------------------------------------------------------------------ 6. grade per footing
C["STAT"].clear()
k1all, k2all, k3all = [], [], []
for f in FEET:
    xa = xcop_cl2(f); hb = hg2_cl2(f)
    k1all += [xa["switch_ok"], hb["k1"]]; k2all.append(xa["k2"]); k3all += [xa["k3"], hb["k3"]]
    fails = [n for n, v in (("X-COP", xa["verdict"]), ("HG2", hb["verdict"])) if v != "PASS"]
    lane = "CL2 PICTURE PASSES BOTH HELD-OUT TESTS" if not fails else "CL2 PICTURE FAILS: " + ", ".join(f"{n} {v}" for n, v in (("X-COP", xa["verdict"]), ("HG2", hb["verdict"])) if v != "PASS")
    P(f"\n=== [{f}] a0 {A0[f]:.6e}{'  (MUTATED picture)' if MUTATE else ''}")
    P(f"  (a) X-COP 35 points: mean Delta {xa['mean']:+.3f} dex, rms {xa['rms']:.3f} (saturated {xa['saturated']}) -> {xa['verdict']}   "
      f"[CS2 law {cs2x['mean']:+.3f}/{cs2x['rms']:.3f}; OS1 {os1x[f]['mean']:+.3f}/{os1x[f]['rms']:.3f}; both HSE-normalised]")
    P("      per cluster: " + ", ".join(f"{k} {v:+.3f}" for k, v in xa["per_cluster"].items()))
    P("      per radius:  " + ", ".join(f"{k} R500 {v:+.3f}" for k, v in xa["by_x"].items()))
    P("      halos: " + "; ".join(f"{k} logM {v['logM']:.2f} Sigma {v['Sigma_pc2']:.0f} r0 {v['r0_kpc']:.0f} kpc r_ta {v['rta_Mpc']:.2f} Mpc Mb_t/Mg500 {v['Mbt_over_Mg500']:.2f} Mh(R500)/M_HSE {v['Mh_R500_over_Mdata']:.2f}" for k, v in xa["info"].items()))
    P(f"  (b) HG2: D_pred {hb['D_pred']:+.3f} (BRIGHT {hb['n_bright']} / FAINT {hb['n_faint']}) vs measured 95% [{lo0:+.3f}, {hi0:+.3f}] -> {hb['verdict']}")
    rp = hb["reported"]
    P(f"      reported: D_res {rp['D_res']:+.3f} [{rp['ci95_res'][0]:+.3f}, {rp['ci95_res'][1]:+.3f}], power {rp['power']:.3f} -> {rp['cls_res']}; "
      + "; ".join(f"{k} n {v['n']} median res {v['median_res']:+.3f}, pred-vs-ref {v['median_pred_vs_ref']:+.3f}, above switch {v['frac_above']:.2f}" for k, v in rp["arms"].items())
      + f"; M*-only variant D_pred {rp['D_pred_mstar_only']:+.3f} (above: B {rp['frac_above_mstar_only']['BRIGHT']:.2f}, F {rp['frac_above_mstar_only']['FAINT']:.2f})")
    P(f"  LANE [{f}]: {lane}   [{time.time() - T0:.0f} s, RSS {rss():.2f} GB]")
    RES["footings"][f] = dict(xcop={k: v for k, v in xa.items() if k not in ("switch_ok", "k2", "k3")}, hg2={k: v for k, v in hb.items() if k not in ("k1", "k3")}, lane=lane)
statg = {k: dict(v) for k, v in C["STAT"].items()}
nviol = sum(v["viol"] for v in list(stat43.values()) + list(statg.values()))
check("K1", all(k1all) and nviol == 0, f"switch: X-COP all above T, HG2 branch = [M200 > 10^12.3] with exact branch values; LF_G violations {nviol} (X43 copy {sum(v['viol'] for v in stat43.values())})")
check("K2", max(k2all) < 1e-5, f"GS1 turnaround budget start independence (x0.3, x3; AMENDMENT A1): max rel {max(k2all):.1e}")
check("K3", all(k3all), "Burkert mass at r_ta = M_fair (X-COP) and at R200 = M200 (groups), or counted saturated")
RES["stat"] = dict(x43=stat43, graders=statg)
V = {f: RES["footings"][f]["lane"] for f in FEET}
RES["verdict"] = dict(canonical_primary=V["canonical"], alt=V["alt"], footings_agree=V["canonical"] == V["alt"])
P(f"\n=== VERDICT (canonical, primary): {V['canonical']}\n=== alt (reported beside it): {V['alt']}" + ("" if V["canonical"] == V["alt"] else "\n=== the footings disagree; no pooled verdict"))
check("K6", rss() < 1.0, f"peak RSS {rss():.2f} GB, one thread")
n = sum(v for _, v in checks); RES["checks"] = {k: v for k, v in checks}
P(f"\nchecks {n}/{len(checks)}; runtime {time.time() - T0:.0f} s; peak RSS {rss():.2f} GB")
open(os.path.join(HERE, f"ho1_heldout{TAG}.out"), "w").write("\n".join(OUT).replace(REPO, "<repo>") + "\n")
def clean(o):
    if isinstance(o, dict): return {str(k): clean(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)): return [clean(v) for v in o]
    if isinstance(o, (np.floating, float)): return float(o)
    if isinstance(o, (np.integer,)): return int(o)
    if isinstance(o, np.bool_): return bool(o)
    return o
json.dump(clean(RES), open(os.path.join(HERE, f"ho1_heldout_results{TAG}.json"), "w"), indent=1, default=str)
try: os.remove(os.path.join(HERE, "x62_x43copy.py"))
except OSError: pass
if MUTATE:
    bites = not dict(checks)["S0-CL2"] and not dict(checks)["K1"] and not dict(checks)["S0-HG2"]
    P(f"MUTATE: S0-CL2 {dict(checks)['S0-CL2']}, K1 {dict(checks)['K1']}, S0-HG2 {dict(checks)['S0-HG2']} -> {'teeth BITE (exit 1)' if bites else 'ALARM: a tooth does not bite (exit 0)'}")
    open(os.path.join(HERE, f"ho1_heldout{TAG}.out"), "w").write("\n".join(OUT).replace(REPO, "<repo>") + "\n")
    sys.exit(1 if bites else 0)
sys.exit(0 if n == len(checks) else 1)
