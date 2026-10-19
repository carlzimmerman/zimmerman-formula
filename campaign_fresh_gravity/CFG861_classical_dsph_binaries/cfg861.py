"""CFG861 -- do unresolved binaries make the CLASSICAL dSphs' excess?  Criteria: FROZEN_CRITERIA.md (4bcf7ce28), block 860-869.
Walker+2023 per-epoch catalogue (real_research/data/walker2023) through CFG51's reducer (reduce_walker.py, imported UNCHANGED as a
module, so its main() and its file output never run): quality cut, membership v2, epochs pooled by Gaia id, Gaussian likelihood.
Classical = LVD-matched and M_V <= -7.7 (CFG51's rule).  Per system, the multi-epoch member set M (>= 2 quality epochs):
  sigma_single(M) = first quality epoch of each star in M;  sigma_clean(M) = stars in M with chi2 p >= 0.01, all-epoch means;
  delta = 2 log10(sigma_clean(M) / sigma_single(M))  (dex in g_obs; same stars, same footprint).  Informative if |M| >= 30.
Delta_LVD = CFG852's delta_ups2 (taken from cfg852.py with ast, as CFG860 did; Ups_V 2, Wolf at 4/3 r_h, nu_e), canonical a0
9.3603e-11 graded, alt 1.1312e-10 reported (the same function with its module-level a0 swapped).  Delta_clean = Delta_LVD + delta.
Graded: informative classicals at log10 g_bar < -11.9.  m = mean Delta_clean, s = std/sqrt(N); classes as frozen.
Run: python3 cfg861.py  ->  cfg861.out, cfg861_results.json;  CFG861_MUTATE=1  ->  cfg861_MUTATE.out, cfg861_results_MUTATE.json.
Choices fixed before any graded number was seen (disclosed in README.md):
  * std in s and in se(delta) uses ddof = 1 (sample standard deviation); the ddof = 0 class is printed alongside.
  * K1 tolerance: the committed walker_reduced_dispersions.tsv is written with '%.4g', so 1e-6 km/s cannot be checked against it;
    K1 requires the '%.4g' strings (and the integer counts) to be identical.  Row/star counts are also checked against CFG51's run.log.
  * Paper-flag variant: CFG51's own keep rule (fvar == 0) applied inside M.
  * Ups_SFH variant: CFG828's rows (delta, lgbar) where present; the g_bar cut uses CFG828's lgbar.
  * MUTATE: M is held fixed (membership not re-run); 50% of M = |M| // 2 stars chosen with numpy default_rng(861), systems in
    Walker-target order; every row of a chosen star gets its own N(0, 10 km/s) offset; the reducer's build_stars re-reduces the rows.
Added AFTER the graded run (printed as POST HOC, not graded): the graded statistic without Crater II.
kappa = 1/2 FITTED; cold energy mass required; not theory closed."""
import os, csv, json, math, ast, importlib.util, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); LANES = os.path.dirname(HERE); REPO = os.path.dirname(LANES)
MUT = os.environ.get("CFG861_MUTATE") == "1"; OUT = []
def P(s=""):
    print(s, flush=True); OUT.append(str(s))
A0 = {"canonical": 9.3603e-11, "alt": 1.1312e-10}; LGCUT, NMIN, NMIN_VAR, PCUT, SEED, SIG_INJ = -11.9, 30, 15, 0.01, 861, 10.0
BIN_BOUND = 4.5   # km/s, single-epoch binary bound (McConnachie & Cote 2010, as used in CFG29)

# ---- CFG51's reducer, imported unchanged (module-level code = imports, paths, column map, function definitions)
spec = importlib.util.spec_from_file_location("cfg51_reduce_walker", os.path.join(LANES, "CFG51_walker_multiepoch", "reduce_walker.py"))
RW = importlib.util.module_from_spec(spec); spec.loader.exec_module(RW)

# ---- CFG852's delta_ups2 and its constants, extracted with ast (CFG860's method); alt = same function, module a0 swapped
src = ast.parse(open(os.path.join(LANES, "CFG852_gas_loss_metallicity", "cfg852.py")).read()); keep = []
for n in src.body:
    if isinstance(n, ast.FunctionDef) and n.name in ("fnum", "delta_ups2"): keep.append(n)
    elif isinstance(n, ast.Assign):
        ids = {t.id for t in n.targets if isinstance(t, ast.Name)} | {e.id for t in n.targets if isinstance(t, ast.Tuple) for e in t.elts if isinstance(e, ast.Name)}
        if ids & {"G", "Msun", "PC", "a0", "nu", "law"}: keep.append(n)
NS = {}
for ft in ("canonical", "alt"):
    ns = {"math": math}; exec(compile(ast.Module(body=keep, type_ignores=[]), "cfg852_subset", "exec"), ns)
    if ft == "alt": ns["a0"] = A0["alt"]
    assert abs(ns["a0"] - A0[ft]) == 0.0
    NS[ft] = ns

R28J = json.load(open(os.path.join(LANES, "CFG828_dwarf_excess_rotation_vs_dispersion", "cfg828_results.json")))
R28 = {ft: {r["name"]: r for r in R28J[f"{ft}|nu_e"]["rows"]} for ft in ("canonical", "alt")}

def sig(M, vk, ek):
    return RW.mle_sigma([s[vk] for s in M], [s[ek] for s in M]) if len(M) >= 3 else None

def full_estimators(mem):
    """CFG51's full-sample estimators, the same expressions as reduce_walker.main() (N >= 8)."""
    N = len(mem); r = {}
    if N < 8: return r
    a, b = sig(mem, "v1", "e1"), sig(mem, "vm", "em")
    clean = [s for s in mem if not (s["n"] >= 2 and s["p"] < 0.01)]
    pf = [s for s in mem if s["fvar"] == 0]
    c, d = sig(clean, "vm", "em"), sig(pf, "vm", "em")
    r.update(single=a, allmean=b, clean=c, paperflag=d, n_removed=N - len(clean), n_untestable=sum(1 for s in clean if s["n"] < 2),
             n_removed_paperflag=N - len(pf), median_err=float(np.median([s["e1"] for s in mem])))
    return r

def shift(M):
    """like-for-like binary shift on the multi-epoch set M"""
    a = sig(M, "v1", "e1")
    keepc = [s for s in M if not (s["p"] < PCUT)]; keepf = [s for s in M if s["fvar"] == 0]
    c, f = sig(keepc, "vm", "em"), sig(keepf, "vm", "em")
    dl = lambda x: 2 * math.log10(x["sig"] / a["sig"]) if (a and x and a["sig"] > 0 and x["sig"] > 0) else None
    return dict(single=a, clean=c, pflag=f, n_rm=len(M) - len(keepc), n_rm_pf=len(M) - len(keepf), delta=dl(c), delta_pf=dl(f))

def cls_of(m, s, md, N):
    if N < 4: return "NOT DIAGNOSTIC"
    if m < 0.10 and m < 2 * s: return "BINARIES EXPLAIN"
    if abs(md) < 0.05 and m > 3 * s: return "BINARIES MINOR"
    return "PARTIAL"

def grade(rows, dkey="D_can", lgkey="lg", shkey="delta", nmin=NMIN):
    G = [r for r in rows if r["nM"] >= nmin and r.get(dkey) is not None and r.get(lgkey) is not None and r[lgkey] < LGCUT and r.get(shkey) is not None]
    N = len(G); Dc = np.array([r[dkey] + r[shkey] for r in G]); dd = np.array([r[shkey] for r in G])
    se = lambda x, k: float(x.std(ddof=k) / math.sqrt(len(x))) if len(x) >= 2 else float("nan")
    m = float(Dc.mean()) if N else float("nan"); md = float(dd.mean()) if N else float("nan")
    out = dict(N=N, systems=[r["name"] for r in G], m=m, s=se(Dc, 1), mean_delta=md, se_delta=se(dd, 1), s_ddof0=se(Dc, 0),
               mean_D_lvd=float(np.mean([r[dkey] for r in G])) if N else float("nan"))
    out["cls"] = cls_of(m, out["s"], md, N); out["cls_ddof0"] = cls_of(m, out["s_ddof0"], md, N)
    return out

def gline(lab, g):
    if g["N"] == 0: return f"  [{lab}] N 0 -> {g['cls']}"
    return (f"  [{lab}] N {g['N']} ({', '.join(g['systems'])})  mean Delta_LVD {g['mean_D_lvd']:+.3f}  m {g['m']:+.3f} +- {g['s']:.3f}  "
            f"mean delta {g['mean_delta']:+.3f} +- {g['se_delta']:.3f}  -> {g['cls']}" + ("" if g["cls_ddof0"] == g["cls"] else f"  (ddof 0: {g['cls_ddof0']})"))

fmt = lambda x, f="%.3f": (f % x) if (x is not None and np.isfinite(x)) else "NA"

# ---- data
P("CFG861  classical dSphs: like-for-like multi-epoch binary shift (Walker+2023 through CFG51's reducer)" + ("  [MUTATE]" if MUT else ""))
rows = []
for f in ("hectocat.dat.gz", "m2fshi.dat.gz", "m2fsmed.dat.gz"):
    rows += RW.parse(RW.IN + f)
stars_all = RW.build_stars(rows); lvd = RW.load_lvd()
nrow = {}
for r in rows: nrow[r["Target"]] = nrow.get(r["Target"], 0) + 1
names = sorted(nrow); P(f"  rows parsed {len(rows)}, targets {len(names)}, stars (quality, Gaia) {len(stars_all)}")
# row/star counts against CFG51's run.log
logtab = {}
for ln in open(os.path.join(LANES, "CFG51_walker_multiepoch", "run.log")):
    t = ln.split()
    if len(t) == 5 and t[1] in ("UFD", "classical", "noLVD"): logtab[t[0]] = (t[1], int(t[3]), int(t[4]))
cnt_ok = 0; CLASSICAL = []
for n in names:
    x = lvd.get(n.lower()); mv = RW.fnum(x["M_V"]) if x else float("nan")
    c = "noLVD" if x is None else ("UFD" if mv > -7.7 else "classical")
    ns_ = sum(1 for s in stars_all.values() if s["target"] == n)
    cnt_ok += logtab.get(n) == (c, nrow[n], ns_)
    if c == "classical": CLASSICAL.append(n)
P(f"  class/rows/stars match CFG51 run.log for {cnt_ok}/{len(names)} targets (log lists {len(logtab)})")
P(f"  classical systems ({len(CLASSICAL)}): {', '.join(CLASSICAL)}")

def reduce_sys(n, stars_src):
    stars = {k: s for k, s in stars_src.items() if s["target"] == n}
    mem, nvrej, vc, sw = RW.membership(stars, lvd[n.lower()])
    mem = sorted(mem, key=lambda s: s["gaia"])
    return mem, nvrej, vc, sw

# ---- per classical system
SYS, MEMB = [], {}
for n in CLASSICAL:
    lv = lvd[n.lower()]; mem, nvrej, vc, sw = reduce_sys(n, stars_all); M = [s for s in mem if s["n"] >= 2]; MEMB[n] = (mem, M)
    fe = full_estimators(mem); sh = shift(M)
    dc, lg = NS["canonical"]["delta_ups2"](lv); da, lga = NS["alt"]["delta_ups2"](lv)
    sl = RW.fnum(lv["vlos_sigma"]); nm = lv["name"]
    sbin = sl * math.sqrt(1 - 10 ** (-dc)) if dc > 0 else 0.0
    base = [float(s["hjd"].max() - s["hjd"].min()) for s in M]
    r = dict(name=nm, target=n, M_V=RW.fnum(lv["M_V"]), N=len(mem), n_vreject=nvrej, vsys_fit=vc, sig_seed=sw, nM=len(M),
             frac_multi=len(M) / len(mem) if mem else float("nan"), med_epochs_M=float(np.median([s["n"] for s in M])) if M else float("nan"),
             base_med_M=float(np.median(base)) if base else float("nan"), n_rm=sh["n_rm"], n_rm_pf=sh["n_rm_pf"],
             sig_single_M=sh["single"], sig_clean_M=sh["clean"], sig_pflag_M=sh["pflag"], delta=sh["delta"], delta_pf=sh["delta_pf"],
             D_can=dc, D_alt=da, lg=lg, sig_lvd=sl, sig_bin_needed=sbin, exceeds_bound=bool(sbin > BIN_BOUND),
             D_sfh_can=R28["canonical"].get(nm, {}).get("delta"), lg_sfh=R28["canonical"].get(nm, {}).get("lgbar"),
             D_sfh_alt=R28["alt"].get(nm, {}).get("delta"), full=fe)
    r["D_clean"] = dc + sh["delta"] if sh["delta"] is not None else None
    r["informative"] = int(r["nM"] >= NMIN); r["graded"] = int(r["informative"] and lg < LGCUT and sh["delta"] is not None)
    SYS.append(r)

G0 = grade(SYS)

if not MUT:
    P("\n  PER SYSTEM (M = members with >= 2 quality epochs; sigma in km/s; delta, Delta in dex of g)")
    P("  system            |M|/N      fM   rm  base_d ep  sig_single(M)         sig_clean(M)          delta   Delta_LVD Delta_clean lg_gbar  "
      "sig_LVD sig_bin_need  graded")
    for r in sorted(SYS, key=lambda r: r["lg"]):
        a, c = r["sig_single_M"], r["sig_clean_M"]
        sa = f"{a['sig']:5.2f} +{a['ep']:.2f} -{a['em']:.2f}" if a else "NA"; sc = f"{c['sig']:5.2f} +{c['ep']:.2f} -{c['em']:.2f}" if c else "NA"
        P(f"  {r['name']:17s} {r['nM']:4d}/{r['N']:<4d} {r['frac_multi']:5.2f} {r['n_rm']:4d} {fmt(r['base_med_M'], '%6.0f')} {fmt(r['med_epochs_M'], '%2.0f')}"
          f"  {sa:20s}  {sc:20s} {fmt(r['delta'], '%+.3f'):7s} {r['D_can']:+.3f}    {fmt(r['D_clean'], '%+.3f'):7s}   {r['lg']:7.3f}  {r['sig_lvd']:5.2f}  "
          f"{r['sig_bin_needed']:5.2f} {'> 4.5' if r['exceeds_bound'] else '<=4.5'}  {'YES' if r['graded'] else ('no (|M|<30)' if not r['informative'] else 'no (g_bar)')}")
    P("\n  CFG51 full-sample estimators (all members; sigma km/s)  + variants per system")
    P("  system            N  vrej  single        allmean  clean (rm, untest)   paperflag (rm)  med_err | delta_pf  Delta_alt  Delta_SFH can/alt (lg)")
    for r in sorted(SYS, key=lambda r: r["lg"]):
        fe = r["full"]; g = lambda k: fmt(fe[k]["sig"], "%5.2f") if fe.get(k) else "NA"
        P(f"  {r['name']:17s} {r['N']:4d} {r['n_vreject']:4d}  {g('single'):5s} +{fmt(fe['single']['ep'] if fe.get('single') else None, '%.2f')}  "
          f"{g('allmean'):5s}    {g('clean'):5s} ({fe.get('n_removed', 'NA')}, {fe.get('n_untestable', 'NA')})      {g('paperflag'):5s} ({fe.get('n_removed_paperflag', 'NA')})     "
          f"{fmt(fe.get('median_err'), '%.2f')}  | {fmt(r['delta_pf'], '%+.3f')}    {r['D_alt']:+.3f}     {fmt(r['D_sfh_can'], '%+.3f')}/{fmt(r['D_sfh_alt'], '%+.3f')} ({fmt(r['lg_sfh'], '%.2f')})")
    P("\n  GRADED (canonical a0 9.3603e-11; informative |M| >= 30; log g_bar < -11.9; s = std(ddof 1)/sqrt(N))")
    P(gline("canonical", G0))
    for r in SYS:
        if r["graded"]: P(f"      {r['name']:17s} |M| {r['nM']:4d}  delta {r['delta']:+.3f}  Delta_LVD {r['D_can']:+.3f}  Delta_clean {r['D_clean']:+.3f}  "
                          f"sig_bin needed {r['sig_bin_needed']:.2f} km/s ({'above' if r['exceeds_bound'] else 'within'} the 4.5 km/s bound)")
    P(f"\n  CLASS: {G0['cls']}")
    P("\n  REPORTED VARIANTS (not graded)")
    VAR = {"alt footing": grade(SYS, dkey="D_alt"), "|M| >= 15": grade(SYS, nmin=NMIN_VAR), "paper-flag cleaning": grade(SYS, shkey="delta_pf"),
           "Ups_SFH canonical (CFG828 rows, CFG828 lgbar)": grade(SYS, dkey="D_sfh_can", lgkey="lg_sfh"),
           "Ups_SFH alt (CFG828 rows, CFG828 lgbar)": grade(SYS, dkey="D_sfh_alt", lgkey="lg_sfh"),
           "alt footing, |M| >= 15": grade(SYS, dkey="D_alt", nmin=NMIN_VAR)}
    for k, v in VAR.items(): P(gline(k, v))
    POST = {"graded set without Crater II (tidally disturbed, below the law)": grade([r for r in SYS if r["name"] != "Crater II"])}
    for k, v in POST.items(): P(gline("POST HOC, added after the graded run, not in the frozen criteria: " + k, v))
    P("  UFD context (quoted, not re-run; LEDGER CFG51/CFG93): offsets there are log10(sigma_obs/sigma_law), dex in SIGMA (x2 for g), kernel nu_mono;"
      " Bootes I cleaned +0.219 +- 0.089 (single +0.310), Tucana II +0.465 +- 0.128 (single +0.730); CFG93: Tucana II testable stars only +0.22 +- 0.14.")
    # ---- K1: UFD reproduction against CFG51's committed tsv
    tsv = {}
    with open(os.path.join(LANES, "CFG51_walker_multiepoch", "walker_reduced_dispersions.tsv")) as fh:
        for row in csv.DictReader(fh, delimiter="\t"): tsv[row["name"]] = row
    K1 = {}; k1ok = True
    for n in ("Bootes_1", "Tucana_2"):
        mem, nvrej, vc, sw = reduce_sys(n, stars_all); fe = full_estimators(mem); M = [s for s in mem if s["n"] >= 2]
        mine = {"sigma_single": "%.4g" % fe["single"]["sig"], "sigma_clean": "%.4g" % fe["clean"]["sig"], "sigma_allmean": "%.4g" % fe["allmean"]["sig"],
                "sigma_paperflag": "%.4g" % fe["paperflag"]["sig"], "n_members": str(len(mem)), "n_multi": str(len(M)), "n_removed": str(fe["n_removed"])}
        ok = {k: mine[k] == tsv[n][k] for k in mine}; graded_ok = ok["sigma_single"] and ok["sigma_clean"]; k1ok &= all(ok.values())
        K1[n] = dict(mine=mine, tsv={k: tsv[n][k] for k in mine}, match=ok, single_unrounded=fe["single"]["sig"], clean_unrounded=fe["clean"]["sig"])
        P(f"  K1 {n}: single {fe['single']['sig']:.6f} ('{mine['sigma_single']}' vs tsv '{tsv[n]['sigma_single']}'), clean {fe['clean']['sig']:.6f} "
          f"('{mine['sigma_clean']}' vs '{tsv[n]['sigma_clean']}'), allmean '{mine['sigma_allmean']}'/'{tsv[n]['sigma_allmean']}', paperflag "
          f"'{mine['sigma_paperflag']}'/'{tsv[n]['sigma_paperflag']}', N {mine['n_members']}/{tsv[n]['n_members']}, multi {mine['n_multi']}/{tsv[n]['n_multi']}, "
          f"rm {mine['n_removed']}/{tsv[n]['n_removed']} -> {'PASS' if all(ok.values()) else 'FAIL'}")
    K1.update(passed=bool(k1ok), counts_runlog=f"{cnt_ok}/{len(names)}", tolerance="identical '%.4g' strings (the tsv's precision) and integer counts")
    P(f"  K1 {'PASS' if k1ok else 'FAIL'} (tolerance: the tsv's '%.4g' precision; 1e-6 km/s is below the committed file's precision); run.log counts {cnt_ok}/{len(names)}")
    # ---- K2: Draco Delta vs CFG860
    c860 = json.load(open(os.path.join(LANES, "CFG860_stripping_vs_isolated_dwarfs", "cfg860_results.json")))
    dr860 = [m for m in c860["members"]["S"] if m["name"] == "Draco"][0]; dr = [r for r in SYS if r["name"] == "Draco"][0]
    k2 = abs(dr["D_can"] - dr860["d"]) <= 1e-9; k2alt = abs(dr["D_alt"] - dr860["d_alt"]) <= 1e-9
    P(f"  K2 Draco Delta_LVD {dr['D_can']:+.12f} vs CFG860 {dr860['d']:+.12f} (diff {abs(dr['D_can'] - dr860['d']):.1e}) -> {'PASS' if k2 else 'FAIL'};"
      f"  alt {dr['D_alt']:+.12f} vs {dr860['d_alt']:+.12f} -> {'match' if k2alt else 'differs'} (reported)")
    RES = dict(lane="CFG861", criteria_commit="4bcf7ce28", mutate=False, systems=SYS, graded=G0, cls=G0["cls"], variants=VAR, post_hoc=POST, K1=K1,
               K2=dict(draco=dr["D_can"], cfg860=dr860["d"], passed=bool(k2), alt=dr["D_alt"], cfg860_alt=dr860["d_alt"], alt_match=bool(k2alt)))
else:
    P(gline("real run, canonical", G0))
    rng = np.random.default_rng(SEED); MR = {}; n_inj_tot = n_rm_tot = n_pre_tot = n_rm_new_tot = 0; dmut = []
    rows_by = {}
    for r in rows: rows_by.setdefault(r["Target"], []).append(r)
    for n in CLASSICAL:
        r0 = [r for r in SYS if r["target"] == n][0]
        if not r0["graded"]: continue
        mem, M = MEMB[n]; idx = rng.choice(len(M), len(M) // 2, replace=False); inj = {M[i]["gaia"] for i in idx}
        new = []
        for rw in rows_by[n]:
            if rw["Gaia"] in inj:
                rw = dict(rw); rw["Vlos"] = rw["Vlos"] + rng.normal(0.0, SIG_INJ)
            new.append(rw)
        sm = RW.build_stars(new); Mm = [sm[(n, s["gaia"])] for s in M]; sh = shift(Mm)
        pre = {s["gaia"] for s in M if s["p"] < PCUT}
        n_rm_inj = sum(1 for g in inj if sm[(n, g)]["p"] < PCUT); n_pre = len(inj & pre); n_rm_new = sum(1 for g in inj - pre if sm[(n, g)]["p"] < PCUT)
        n_inj_tot += len(inj); n_rm_tot += n_rm_inj; n_pre_tot += n_pre; n_rm_new_tot += n_rm_new; dmut.append(sh["delta"])
        MR[r0["name"]] = dict(nM=len(M), n_inj=len(inj), n_rm_inj=n_rm_inj, n_inj_already_flagged=n_pre, n_rm_inj_new=n_rm_new,
                              sig_single=sh["single"]["sig"], sig_clean=sh["clean"]["sig"], delta=sh["delta"], delta_real=r0["delta"],
                              D_clean=r0["D_can"] + sh["delta"])
        P(f"    {r0['name']:17s} |M| {len(M):4d} injected {len(inj):4d}  removed {n_rm_inj:4d} ({n_rm_inj / len(inj):.2f}; {n_pre} were flagged before injection)"
          f"  sig_single(M) {sh['single']['sig']:.2f} (real {r0['sig_single_M']['sig']:.2f})  sig_clean(M) {sh['clean']['sig']:.2f} (real {r0['sig_clean_M']['sig']:.2f})"
          f"  delta {sh['delta']:+.3f} (real {r0['delta']:+.3f})")
    fa = n_rm_tot / n_inj_tot if n_inj_tot else float("nan"); md = float(np.mean(dmut)) if dmut else float("nan")
    fnew = n_rm_new_tot / (n_inj_tot - n_pre_tot) if n_inj_tot > n_pre_tot else float("nan")
    oka, okb = fa >= 0.70, md <= -0.10
    P(f"  (a) injected stars removed: {n_rm_tot}/{n_inj_tot} = {fa:.3f} (must be >= 0.70) -> {'PASS' if oka else 'FAIL'}"
      f"   [among injected stars not already flagged: {n_rm_new_tot}/{n_inj_tot - n_pre_tot} = {fnew:.3f}]")
    P(f"  (b) mean delta over graded systems {md:+.3f} (must be <= -0.10) -> {'PASS' if okb else 'FAIL'}")
    P(f"  MUTATE {'BITES (2/2)' if (oka and okb) else 'DOES NOT BITE'}")
    RES = dict(lane="CFG861", criteria_commit="4bcf7ce28", mutate=True, seed=SEED, real=G0, per_system=MR, frac_removed=fa,
               frac_removed_not_preflagged=fnew, mean_delta=md, a_pass=bool(oka), b_pass=bool(okb), bites=bool(oka and okb))

def clean_json(o):
    if isinstance(o, dict): return {k: clean_json(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)): return [clean_json(v) for v in o]
    if isinstance(o, (np.floating, float)): return None if not np.isfinite(o) else float(o)
    if isinstance(o, (np.integer,)): return int(o)
    if isinstance(o, np.bool_): return bool(o)
    return o
sfx = "_MUTATE" if MUT else ""
json.dump(clean_json(RES), open(os.path.join(HERE, f"cfg861_results{sfx}.json"), "w"), indent=1)
open(os.path.join(HERE, f"cfg861{sfx}.out"), "w").write("\n".join(OUT) + "\n")
