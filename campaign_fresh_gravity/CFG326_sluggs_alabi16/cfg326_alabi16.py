#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
CFG326 -- CFG323 (SLUGGS law-only offset with measured tracers) extended with Alabi+16 GC density slopes.
Criteria frozen and committed before any Alabi+16 table value was read: FROZEN_CRITERIA.md (c4aff2ac5).

Base: CFG323 (frozen b2e7ec16d, results 9ee283199). Its script is exec'd READ-ONLY up to its MUTATE block, with __file__ pointed at this lane's
directory so its one side file (the transcribed-values TSV) lands here and is renamed; CFG323's files are never touched.
Law: g = nu_mono(g_N/a0) g_N, kappa = 1/2 FIXED; footings 9.36e-11 | 1.13e-10. Same statistic and decision rule (e) as CFG323.

Alabi+16 (arXiv 1605.06101, owner-approved download, ../_external_data/sluggs_tracers/arxiv_src/1605.06101/mass_est.tex):
  Table tab:summary columns (1) NGC, (9) log M* (M/L_K = 1), (12) gamma (deprojected GC density slope); eq. eq:fit_gamma + its rms scatter.
  Test T0 (frozen 1(b)): a gamma reproduced by the gamma-logM* relation within rounding is a RELATION value, not a measured profile.
MUTATE (CFG326_MUTATE=1): Alabi gamma cyclically shifted by one across the 16 (CFG55 order, galaxies absent from Alabi skipped); separate outputs.
Run: python3 campaign_fresh_gravity/CFG326_sluggs_alabi16/cfg326_alabi16.py   (CFG326_MUTATE=1 for the control)
"""
import os, sys, re, math, json, io, contextlib
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
LANES = os.path.dirname(HERE)
REPO = os.path.dirname(LANES)
EXT = os.path.normpath(os.path.join(REPO, "..", "_external_data", "sluggs_tracers"))
MUTATE = os.environ.get("CFG326_MUTATE", "0") == "1"
TAG = "_MUTATE" if MUTATE else ""
OUT = []


def P(s=""):
    print(s); OUT.append(str(s))


P("=" * 120)
P("CFG326 -- CFG323 extended with Alabi+16 GC density slopes" + ("   *** MUTATE: Alabi slopes cyclically shifted ***" if MUTATE else ""))
P("frozen criteria: FROZEN_CRITERIA.md (commit c4aff2ac5); base CFG323 (b2e7ec16d / 9ee283199); kernel nu_mono, kappa = 1/2 fixed")
P("=" * 120)

# ------------------------------------------------------------------ 0. CFG323 namespace (read-only exec; Alabi OFF)
CFG323_DIR = os.path.join(LANES, "CFG323_sluggs_measured_tracers")
src = open(os.path.join(CFG323_DIR, "cfg323_measured_tracers.py")).read()
cut = src.index("\n# ------------------------------------------------------------------ 9. MUTATE check")
_saved = os.environ.pop("CFG323_MUTATE", None)
NS = {"__file__": os.path.join(HERE, "_cfg323_readonly_exec.py"), "__name__": "cfg323_ns"}
buf = io.StringIO()
with contextlib.redirect_stdout(buf):
    exec(compile(src[:cut], "cfg323_measured_tracers", "exec"), NS)
if _saved is not None:
    os.environ["CFG323_MUTATE"] = _saved
side = os.path.join(HERE, "cfg323_transcribed_values.tsv")
if os.path.exists(side):
    os.replace(side, os.path.join(HERE, f"cfg326_cfg323_rerun_transcribed{TAG}.tsv"))
assert not NS["MUTATE"], "CFG323 namespace must be the unmutated run"

A0, B, S16, CENTRALS, stat = NS["A0"], NS["B"], NS["S16"], NS["CENTRALS"], NS["stat"]
RG, LR, offset, powerlaw_rho, classify = NS["RG"], NS["LR"], NS["offset"], NS["powerlaw_rho"], NS["classify"]
TRACER, TRACER_ERR, MEAS323 = NS["TRACER"], NS["TRACER_ERR"], NS["MEASURED"]
ORDER = NS["ORDER"]

checks = []


def check(lbl, cond, det):
    checks.append((lbl, bool(cond))); P(f"  [{'PASS' if cond else 'FAIL'}] {lbl}\n         {det}")


# ------------------------------------------------------------------ 1. Alabi+16 transcription (by script, from the LaTeX)
P("\n" + "-" * 120); P("1. ALABI+16 TRANSCRIPTION (parsed by script from arXiv 1605.06101 LaTeX)"); P("-" * 120)
tA = open(os.path.join(EXT, "arxiv_src", "1605.06101", "mass_est.tex"), encoding="latin-1").read()
k = tA.index("\\label{tab:summary}")
body = tA[tA.index("\\begin{tabular", k):tA.index("\\end{tabular}", k)]
AL = {}
for line in body.split("\n"):
    c = [x.strip() for x in line.split("&")]
    if len(c) >= 14 and c[0].isdigit():
        AL[int(c[0])] = dict(lMs=float(c[8]), lMs_str=c[8], gamma=float(c[11]), gamma_str=c[11])
me = re.search(r"\\gamma = \( (-?[\d.]+) \\pm ([\d.]+)\) \\times \{\\rm log\}\(M_\*/\\Msun\) \+ \(([\d.]+) \\pm ([\d.]+)\)", tA)
EQ = dict(a=float(me.group(1)), a_str=me.group(1), a_err=float(me.group(2)), b=float(me.group(3)), b_str=me.group(3), b_err=float(me.group(4)))
mr = re.search(r"with a rms scatter of ([\d.]+)\$\\pm\$([\d.]+) in the data around the best--fit line", tA)
EQ["rms"] = float(mr.group(1)); EQ["rms_err"] = float(mr.group(2))
cap = re.search(r"\\caption\{\\label\{fig:RV_rad\}(.*?)\}\s*\n", tA, re.S).group(1)
CAPSET = {int(x) for x in re.findall(r"NGC~(\d+)", cap)}
P(f"  eq:fit_gamma: gamma = ({EQ['a']} +- {EQ['a_err']}) log M* + ({EQ['b']} +- {EQ['b_err']}); rms scatter {EQ['rms']} +- {EQ['rms_err']}")
P(f"  tab:summary rows: {len(AL)}; Fig. 1 caption galaxies: {len(CAPSET)}; in the CFG55 16 but absent from Alabi: {[n for n in S16 if n not in AL]}")
with open(os.path.join(HERE, f"cfg326_alabi16_transcribed{TAG}.tsv"), "w") as fh:
    fh.write("# CFG326: Alabi+16 (arXiv 1605.06101) Table tab:summary columns (1) NGC, (9) log M* [M/L_K=1], (12) gamma -- parsed BY SCRIPT from the LaTeX\n")
    fh.write(f"# eq:fit_gamma a={EQ['a']}+-{EQ['a_err']} b={EQ['b']}+-{EQ['b_err']} rms={EQ['rms']}+-{EQ['rms_err']}\n")
    fh.write("NGC\tlogMstar\tgamma\n")
    for n in sorted(AL):
        fh.write(f"{n}\t{AL[n]['lMs_str']}\t{AL[n]['gamma_str']}\n")
spot = 4486
check("K3 transcription: tab:summary has 23 galaxy rows equal (as a set) to the Fig. 1 caption's 23; eq:fit_gamma gives 2 coefficients + rms",
      len(AL) == 23 and set(AL) == CAPSET and all(math.isfinite(EQ[x]) for x in ("a", "b", "rms")),
      f"rows {len(AL)}, caption {len(CAPSET)}, set equal {set(AL) == CAPSET}; spot NGC {spot}: log M* {AL[spot]['lMs_str']}, gamma {AL[spot]['gamma_str']}")


# ------------------------------------------------------------------ 2. T0: relation or measured
def unit(s):
    s = s.strip().lstrip("-")
    return 10 ** -(len(s.split(".")[1]) if "." in s else 0)


P("\n" + "-" * 120); P("2. T0 -- is each Alabi gamma the gamma-logM* relation's output? (frozen 1(b); a classification, not a pass/fail)"); P("-" * 120)
sec = tA[tA.index("\\label{gamma}"):]
sec = sec[:sec.index("\\subsection")]
T0 = {}
for n in sorted(AL):
    a = AL[n]
    rel = EQ["a"] * a["lMs"] + EQ["b"]
    r = a["gamma"] - rel
    dl = 0.5 * unit(EQ["a_str"]) * abs(a["lMs"]) + 0.5 * unit(EQ["b_str"]) + 0.5 * unit(a["gamma_str"]) + abs(EQ["a"]) * 0.5 * unit(a["lMs_str"])
    if abs(r) <= dl:
        cls = "RELATION"
    else:
        cls = "MEASURED" if (f"NGC~{n}" in sec or f"NGC {n}" in sec) else "UNATTRIBUTED"
    T0[n] = dict(gamma=a["gamma"], relation=rel, resid=r, budget=dl, cls=cls)
    P(f"   NGC{n:<5} {'(in 16)' if n in S16 else '       '} log M* {a['lMs']:5.2f}  gamma {a['gamma']:4.2f}  relation {rel:6.4f}  r {r:+.4f}  |r|<=delta {dl:.4f}?  -> {cls}")
cnt = {c: sum(1 for v in T0.values() if v["cls"] == c) for c in ("RELATION", "MEASURED", "UNATTRIBUTED")}
P(f"  T0 summary over all 23: {cnt}; max |r| {max(abs(v['resid']) for v in T0.values()):.4f}")
ALABI_MEAS = [n for n in S16 if n in T0 and T0[n]["cls"] == "MEASURED" and n not in MEAS323]
UNATTR = [n for n in S16 if n in T0 and T0[n]["cls"] == "UNATTRIBUTED" and n not in MEAS323]

# gamma used (MUTATE: cyclic shift by one across the 16 in CFG55 order, galaxies absent from Alabi skipped)
L = [n for n in S16 if n in AL]
GAM_TRUE = {n: AL[n]["gamma"] for n in L}
GAM = dict(GAM_TRUE)
if MUTATE:
    GAM = {L[i]: GAM_TRUE[L[(i + 1) % len(L)]] for i in range(len(L))}
    for n in L:
        P(f"  MUTATE: NGC{n} gamma {GAM_TRUE[n]:.2f} -> {GAM[n]:.2f} (from NGC{L[L.index(n) + 1 - len(L)]})")

# ------------------------------------------------------------------ 3. scoring machinery (CFG323's offsets; memoised)
MEMO = {}


def off(n, foot, key, comps):
    kk = (n, foot, key)
    if kk not in MEMO:
        MEMO[kk] = offset(n, foot, comps=comps)
    return MEMO[kk]


def pl(g, beta=0.0):
    return [(powerlaw_rho(g), beta)]


def config(meas_alabi=(), gam=None, g_center=None, replace_overlap=False):
    """returns per-galaxy tracer spec: n -> ('cfg323',) | ('pl', gamma, measured?, sigma)"""
    spec = {}
    for n in S16:
        if n in MEAS323 and not replace_overlap:
            spec[n] = ("cfg323",)
        elif n in meas_alabi:
            spec[n] = ("pl", gam[n], True)
        elif g_center is not None and n in g_center:
            spec[n] = ("pl", g_center[n], False)
        else:
            spec[n] = ("pl", 3.0, False)
    return spec


def per_offsets(n, foot, s, half, sig_meas=None):
    """primary, gamma+half, gamma-half, beta+0.5, beta-0.5, fit-error delta (max abs) for one galaxy under spec s"""
    if s[0] == "cfg323":
        comps = lambda beta: [(rho, beta) for rho in TRACER[n]]
        prim = off(n, foot, ("cfg323", 0.0), comps(0.0))
        gp = gm = prim
        bp = off(n, foot, ("cfg323", 0.5), comps(0.5)); bm = off(n, foot, ("cfg323", -0.5), comps(-0.5))
        dm = max(abs(off(n, foot, ("cfg323err", lab), [(rho, 0.0)]) - prim) for lab, rho in TRACER_ERR[n])
        return prim, gp, gm, bp, bm, dm, True
    g, measured = s[1], s[2]
    prim = off(n, foot, ("pl", g, 0.0), pl(g))
    bp = off(n, foot, ("pl", g, 0.5), pl(g, 0.5)); bm = off(n, foot, ("pl", g, -0.5), pl(g, -0.5))
    if measured:
        gp = gm = prim
        sg = (sig_meas or {}).get(n, 0.0)
        dm = 0.0 if sg == 0 else max(abs(off(n, foot, ("pl", g + d, 0.0), pl(g + d)) - prim) for d in (sg, -sg))
    else:
        gp = off(n, foot, ("pl", g + half, 0.0), pl(g + half)); gm = off(n, foot, ("pl", g - half, 0.0), pl(g - half)); dm = None
    return prim, gp, gm, bp, bm, dm, measured


def score(spec, half=0.5, sig_meas=None):
    R = {}
    for foot in A0:
        per = {n: per_offsets(n, foot, spec[n], half, sig_meas) for n in S16}
        R[foot] = {"per": {n: per[n][0] for n in S16}}
        subs = {"ALL": S16, "NO-CENTRALS": [n for n in S16 if n not in CENTRALS], "CENTRALS": [n for n in S16 if n in CENTRALS],
                "MEASURED": [n for n in S16 if per[n][6]], "UNMEASURED": [n for n in S16 if not per[n][6]],
                "ALABI-COVERED": [n for n in S16 if n in AL and n not in MEAS323]}
        for s, names in subs.items():
            if len(names) < 2:
                continue
            m, e, z = stat([per[n][0] for n in names])
            sg = abs(np.mean([per[n][1] for n in names]) - np.mean([per[n][2] for n in names])) / 2
            sb = abs(np.mean([per[n][3] for n in names]) - np.mean([per[n][4] for n in names])) / 2
            dms = [per[n][5] for n in names if per[n][6]]
            smeas = math.sqrt(sum(d * d for d in dms)) / len(names)
            tot = math.sqrt(e * e + sg * sg + sb * sb + smeas * smeas)
            R[foot][s] = dict(mean=m, err_stat=e, z_stat=z, s_gamma=sg, s_beta=sb, s_meas=smeas, err_tot=tot, z_sys=m / tot,
                              cls_stat=classify(m, z), cls_sys=classify(m, m / tot), N=len(names))
    return R


def weaker(R, sub="ALL"):
    cl = {f: R[f][sub]["cls_sys"] for f in A0}
    if "REVERSED" in cl.values():
        return "REVERSED" if all(v == "REVERSED" for v in cl.values()) else "NOT SIGNIFICANT"
    return max(cl.values(), key=lambda c: ORDER.index(c))


def show(lbl, R, subs=("ALL", "NO-CENTRALS", "CENTRALS", "MEASURED", "UNMEASURED", "ALABI-COVERED")):
    for foot in A0:
        for s in subs:
            if s not in R[foot]:
                continue
            z = R[foot][s]
            P(f"  {lbl:10} {foot:9} {s:13} N={z['N']:2d}: {z['mean']:+.4f}  stat +-{z['err_stat']:.4f} (Z_stat {z['z_stat']:+.2f})  | s_gamma {z['s_gamma']:.4f} "
              f"s_beta {z['s_beta']:.4f} s_meas {z['s_meas']:.4f} -> Z_sys {z['z_sys']:+.2f} ({z['cls_sys']})")


# ------------------------------------------------------------------ 4. controls K1 / K4
P("\n" + "-" * 120); P("3. CONTROLS (Alabi OFF)"); P("-" * 120)
J = json.load(open(os.path.join(CFG323_DIR, "cfg323_measured_tracers_results.json")))
R_off = score(config())
d_ns = d_own = 0.0
for foot in A0:
    for s, zj in J["stats"][foot].items():
        for q in ("mean", "z_stat", "z_sys"):
            d_ns = max(d_ns, abs(NS["STATS"][foot][s][q] - zj[q]))
            if s in R_off[foot]:
                d_own = max(d_own, abs(R_off[foot][s][q] - zj[q]))
cls_off = weaker(R_off)
check("K1 Alabi OFF reproduces CFG323's committed stats (mean, Z_stat, Z_sys; every subset, both footings) within 1e-9 and its verdict class",
      d_ns <= 1e-9 and d_own <= 1e-9 and cls_off == J["verdict_class"] and NS["verdict"] == J["verdict_class"],
      f"max |diff| re-run namespace {d_ns:.1e}, this lane's scorer {d_own:.1e}; class {cls_off} vs CFG323 {J['verdict_class']}; "
      f"ALL canonical {R_off['canonical']['ALL']['mean']:+.4f} Z_sys {R_off['canonical']['ALL']['z_sys']:.2f}, alt {R_off['alt']['ALL']['mean']:+.4f} Z_sys {R_off['alt']['ALL']['z_sys']:.2f}")
inh = NS["checks"]
check("K4 inherited CFG323 check rows (C1-C6, P1) pass again in the re-run namespace",
      all(c for _, c in inh) and len(inh) == J["n_checks"], f"{sum(1 for _, c in inh if c)}/{len(inh)}: " + "; ".join(l.split(' ')[0] for l, _ in inh))

# ------------------------------------------------------------------ 5. K2 overlap
P("\n" + "-" * 120); P("4. K2 OVERLAP (Alabi gamma vs CFG323's deprojected slope at the outer-bin radii)"); P("-" * 120)


def mean_outer_slope(n, rho):
    gam = -np.gradient(np.log(np.maximum(rho, 1e-300)), LR)
    return float(np.mean([np.interp(math.log(R), LR, gam) for R in B[n]["Rb"][B[n]["outer"]]]))


K2 = {}
for n in MEAS323:
    if n not in AL:
        continue
    g323 = mean_outer_slope(n, TRACER[n][0])
    s323 = max(abs(mean_outer_slope(n, rho) - g323) for _, rho in TRACER_ERR[n])
    sA = EQ["rms"]      # T0 RELATION (or no tabulated error) -> the relation rms (frozen K2)
    lim = 2 * math.sqrt(sA ** 2 + s323 ** 2)
    K2[n] = dict(gamma_alabi=GAM_TRUE[n], gamma_323=g323, sigma_323=s323, sigma_A=sA, diff=GAM_TRUE[n] - g323, limit=lim, ok=abs(GAM_TRUE[n] - g323) <= lim,
                 t0=T0[n]["cls"])
    P(f"   NGC{n:<5} Alabi {GAM_TRUE[n]:.2f} ({T0[n]['cls']})  CFG323 <gamma>_outer {g323:.3f} (sigma_323 {s323:.3f})  diff {GAM_TRUE[n] - g323:+.3f}  limit +-{lim:.3f}  "
      f"{'agree' if K2[n]['ok'] else 'DISAGREE'}")
check("K2 Alabi vs CFG323 slopes agree on the overlap within 2 sqrt(sigma_A^2 + sigma_323^2)", all(v["ok"] for v in K2.values()),
      "; ".join(f"NGC{n} {v['diff']:+.2f} vs +-{v['limit']:.2f}" for n, v in K2.items()))

# ------------------------------------------------------------------ 6. primary
P("\n" + "-" * 120); P("5. PRIMARY (frozen: CFG323 profiles where they exist; Alabi gamma only where T0 says MEASURED; gamma 3 elsewhere)"); P("-" * 120)
P(f"  Alabi values classed MEASURED for galaxies without a CFG323 profile: {ALABI_MEAS or 'none'}; UNATTRIBUTED: {UNATTR or 'none'}")
SIGM = {}       # no per-galaxy gamma errors are tabulated in Alabi+16 -> contributes 0 (listed)
R_pri = score(config(meas_alabi=ALABI_MEAS, gam=GAM), sig_meas=SIGM)
show("PRIMARY", R_pri)
cov = sum(1 for n in S16 if n in MEAS323 or n in ALABI_MEAS)
vcls = weaker(R_pri)
vtxt = f"{vcls}  [measured-tracer coverage {cov}/16]"
if not ALABI_MEAS:
    vtxt += "  NO NEW MEASURED COVERAGE (Alabi+16 slopes are relation values)"
if ALABI_MEAS:
    P(f"  measured Alabi slopes without a tabulated error contribute 0 to s_meas: {ALABI_MEAS}")

# ------------------------------------------------------------------ 7. reported rows
P("\n" + "-" * 120); P("6. REPORTED ROWS (never decision rows)"); P("-" * 120)
cover = {n: GAM[n] for n in S16 if n in GAM and n not in MEAS323}
R_a16 = score(config(g_center=cover))
show("R-A16", R_a16)
R_a16rms = score(config(g_center=cover), half=EQ["rms"])
show("R-A16rms", R_a16rms, subs=("ALL", "NO-CENTRALS", "CENTRALS"))
R_a16all = score(config(g_center={n: GAM[n] for n in S16 if n in GAM}, replace_overlap=True))
show("R-A16all", R_a16all, subs=("ALL", "NO-CENTRALS", "CENTRALS"))
if UNATTR:
    R_sa = score(config(meas_alabi=ALABI_MEAS + UNATTR, gam=GAM), sig_meas={n: EQ["rms"] for n in UNATTR})
    show("S-A", R_sa, subs=("ALL", "NO-CENTRALS", "CENTRALS"))
else:
    R_sa = None
    P("  S-A: no UNATTRIBUTED candidates -> row empty")
P("\n  per galaxy (canonical): primary | R-A16 (Alabi gamma where no CFG323 profile)")
for n in S16:
    g = "CFG323 profile" if n in MEAS323 else (f"Alabi gamma {GAM[n]:.2f}" if n in GAM else "absent from Alabi -> gamma 3")
    P(f"   NGC{n:<5} {'CENT' if n in CENTRALS else '    '} primary {R_pri['canonical']['per'][n]:+.3f}   R-A16 {R_a16['canonical']['per'][n]:+.3f}   ({g})")

# ------------------------------------------------------------------ 8. verdict
P("\n" + "-" * 120); P("7. VERDICT (rule (e) on Z_sys of ALL; the weaker class over the two footings)"); P("-" * 120)
for foot in A0:
    z = R_pri[foot]["ALL"]
    P(f"  {foot:9}: mean {z['mean']:+.4f}  Z_stat {z['z_stat']:+.2f}  Z_sys {z['z_sys']:+.2f}  ({z['cls_sys']})")
P(f"  VERDICT: {vtxt}")
P(f"  splits (not the headline): NO-CENTRALS canonical {R_pri['canonical']['NO-CENTRALS']['mean']:+.4f} Z_sys {R_pri['canonical']['NO-CENTRALS']['z_sys']:+.2f}, "
  f"alt {R_pri['alt']['NO-CENTRALS']['mean']:+.4f} Z_sys {R_pri['alt']['NO-CENTRALS']['z_sys']:+.2f}; CENTRALS canonical {R_pri['canonical']['CENTRALS']['mean']:+.4f} "
  f"Z_sys {R_pri['canonical']['CENTRALS']['z_sys']:+.2f}, alt {R_pri['alt']['CENTRALS']['mean']:+.4f} Z_sys {R_pri['alt']['CENTRALS']['z_sys']:+.2f}")
P(f"  reported R-A16 (relation slopes): ALL canonical {R_a16['canonical']['ALL']['mean']:+.4f} Z_sys {R_a16['canonical']['ALL']['z_sys']:+.2f}, "
  f"alt {R_a16['alt']['ALL']['mean']:+.4f} Z_sys {R_a16['alt']['ALL']['z_sys']:+.2f} ({weaker(R_a16)}, weaker footing)")

# ------------------------------------------------------------------ 9. MUTATE
mut = None
if MUTATE:
    P("\n" + "-" * 120); P("8. MUTATE CHECK"); P("-" * 120)
    test = "PRIMARY" if ALABI_MEAS else "R-A16"
    Rm = R_pri if ALABI_MEAS else R_a16
    if ALABI_MEAS:
        Ru = score(config(meas_alabi=ALABI_MEAS, gam=GAM_TRUE), sig_meas=SIGM)
    else:
        Ru = score(config(g_center={n: GAM_TRUE[n] for n in S16 if n in GAM_TRUE and n not in MEAS323}))
    dlt = {f: Rm[f]["ALABI-COVERED"]["mean"] - Ru[f]["ALABI-COVERED"]["mean"] for f in A0}
    cm, cu = weaker(Rm), weaker(Ru)
    ok = abs(dlt["canonical"]) >= 0.01 or cm != cu
    P(f"  test row {test}: ALABI-COVERED mean shifted {Rm['canonical']['ALABI-COVERED']['mean']:+.4f} vs true {Ru['canonical']['ALABI-COVERED']['mean']:+.4f} "
      f"(canonical delta {dlt['canonical']:+.4f}; alt delta {dlt['alt']:+.4f}); class shifted {cm} vs true {cu}")
    if not ok:
        P("  MUTATE INSENSITIVE")
    check(f"M1 MUTATE: cyclic shift of the Alabi slopes moves the {test} ALABI-COVERED mean by >= 0.01 dex or changes its class",
          ok, f"delta canonical {dlt['canonical']:+.4f}, class change {cm != cu}")
    mut = dict(test_row=test, delta=dlt, class_shifted=cm, class_true=cu, passed=ok)

npass = sum(1 for _, c in checks if c)
P(f"\n  {npass}/{len(checks)} checks pass")


def strip(R):
    return {f: {k: ({str(n): x for n, x in v.items()} if k == "per" else v) for k, v in R[f].items()} for f in R}


res = dict(lane="CFG326", mutate=MUTATE, frozen_commit="c4aff2ac5", base="CFG323 b2e7ec16d / 9ee283199", kernel="nu_mono", kappa=0.5, a0=A0,
           alabi_source="arXiv 1605.06101 Table tab:summary cols (1),(9),(12); eq:fit_gamma", eq_fit_gamma=EQ,
           alabi_gamma_used={str(n): g for n, g in GAM.items()}, t0={str(n): v for n, v in T0.items()},
           alabi_measured=ALABI_MEAS, unattributed=UNATTR, coverage=cov, centrals=CENTRALS,
           primary=strip(R_pri), alabi_off=strip(R_off), reported={"R-A16": strip(R_a16), "R-A16rms": strip(R_a16rms), "R-A16all": strip(R_a16all),
                                                                 "S-A": strip(R_sa) if R_sa else None},
           k2_overlap={str(n): v for n, v in K2.items()}, verdict=vtxt, verdict_class=vcls,
           verdict_by_footing={f: R_pri[f]["ALL"]["cls_sys"] for f in A0}, mutate_check=mut,
           checks=[dict(label=l, passed=c) for l, c in checks], n_pass=npass, n_checks=len(checks))
json.dump(res, open(os.path.join(HERE, f"cfg326_alabi16{TAG}_results.json"), "w"), indent=1, default=float)
open(os.path.join(HERE, f"cfg326_alabi16{TAG}.out"), "w").write("\n".join(OUT) + "\n")
sys.exit(0 if npass == len(checks) else 1)
