#!/usr/bin/env python3
"""X56_law_floor_structure: gravity is never weaker than the law, g = max(nu(g_b/a0) g_b, g_N[baryons + route-E halo]).

Frozen criteria: FROZEN_CRITERIA.md (f17c99a508). The committed scorers of X43 (SPARC, groups, X30's 15 cluster keys; with
X48's ng 48 c_f table as X48's regrade does), X53 (KiDS-1000 isolated-lens lensing) and X51 (LG dwarfs) are executed
read-only as text copies; the only edit in each is that the route-E total (baryons + halo) passes through LF_G / LF_M.
Modes: on (LF), off (route E alone: K0), law (halo branch off: K2). One thread, minutes.

    PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 x56_law_floor.py            -> .out, _results.json
    PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 x56_law_floor.py --mutate   -> law branch dropped where it wins (K1 must fail)
"""
import os, sys, json, math, time, resource, io, contextlib
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"): os.environ[_v] = "1"
os.environ.pop("X53_MUTATE", None); os.environ.pop("X30_MUTATE", None)
import numpy as np

T0 = time.time(); MUTATE = "--mutate" in sys.argv; TAG = "_MUTATE" if MUTATE else ""
HERE = os.path.dirname(os.path.abspath(__file__)); REB = os.path.dirname(HERE)
OUT = []
def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); OUT.append(s)
def rss(): return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / (1e9 if sys.platform == "darwin" else 1e6)
P(f"X56_law_floor_structure  {'MUTATE (law branch dropped where it wins)' if MUTATE else 'normal run'}   criteria f17c99a508")
P("kappa = 1/2 FITTED; footings never pooled; LF: g = max(law on baryons, Newton on baryons + route-E cold dark energy halo); not theory closed")

# ------------------------------------------------------------------ the law floor (shared by every scorer)
MODE = {"m": "on"}
STAT = {}
def _new(): return dict(n=0, viol=0, eqfail=0, law=0)
def nu(y): return 0.5 + np.sqrt(0.25 + 1.0 / y)
def _combine(law, rE, key):
    if MODE["m"] == "off": return rE
    if MODE["m"] == "law": return law
    out = np.maximum(law, rE)
    if MUTATE: out = rE.copy()                                                      # MUTATE: the floor broken
    s = STAT.setdefault(key, _new()); tol = 1e-12 * np.maximum(np.abs(law), np.abs(rE))
    s["n"] += int(out.size); s["viol"] += int(np.sum((out < law - tol) | (out < rE - tol)))
    s["eqfail"] += int(np.sum((np.abs(out - law) > tol) & (np.abs(out - rE) > tol))); s["law"] += int(np.sum(law > rE))
    return out
LAST = {"law": False}
def LF_G(gb, gh, a0, key="g"):
    """pull: gb = baryonic Newtonian pull (any units, a0 in the same units), gh = halo pull."""
    gb = np.asarray(gb, float); gh = np.broadcast_to(np.asarray(gh, float), np.broadcast(gb, np.asarray(gh)).shape)
    gbb = np.broadcast_to(gb, gh.shape); pos = gbb > 0
    law = np.where(pos, nu(np.where(pos, gbb, 1.0) / a0) * gbb, gbb)
    return _combine(law, gbb + gh, key)
def LF_M(Mb, Mh, r, G, a0, key="M"):
    """enclosed mass: Mb, Mh on radius grid r (consistent units with G, a0)."""
    Mb = np.asarray(Mb, float); Mh = np.asarray(Mh, float); r = np.asarray(r, float)
    with np.errstate(divide="ignore", invalid="ignore"):
        law = np.where((r > 0) & (Mb > 0), Mb * nu(np.maximum(G * Mb / np.where(r > 0, r, 1.0) ** 2, 1e-300) / a0), Mb)
    out = _combine(law, Mb + Mh, key)
    LAST["law"] = bool(MODE["m"] == "law" or (MODE["m"] == "on" and not MUTATE and law[-1] > (Mb + Mh)[-1]))
    return out

def run_copy(src_path, edits, fname, extra=None):
    src = open(src_path).read()
    for old, new in edits:
        assert src.count(old) == 1, (src_path, old[:60]); src = src.replace(old, new)
    ns = {"__file__": os.path.join(HERE, fname), "__name__": fname[:-3], "LF_G": LF_G, "LF_M": LF_M, "LAST": LAST}
    if extra: ns.update(extra)
    argv0 = sys.argv; sys.argv = [ns["__file__"]]
    try:
        with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            try: exec(compile(src, ns["__file__"], "exec"), ns)
            except SystemExit: pass
    finally:
        sys.argv = argv0
    return ns

# ------------------------------------------------------------------ A. X43 scorer (SPARC, groups, clusters), X48 ng48 eta
X48T = json.load(open(os.path.join(REB, "X48_native_cf_zoom", "x48_regrade_ng48.json")))["table"]
LM48, CF48 = np.array(X48T["lgM"]), np.array(X48T["cf"]); B1 = 3 * math.log(2) - math.pi / 2
def eta48(M): return 4.0 / (3.0 * B1) * float(np.interp(math.log10(M), LM48, CF48)) ** 1.25
def run_x43(mode, cfmode):
    MODE["m"] = mode; tag = f"{mode}_{cfmode}{TAG}"
    ed = [('sc = ETA_USE["v"] * sigma_coll(tag, M)[0] * MSUNE / PC2',
           'sc = (ETA_FUN(M) if (ETA_FUN is not None and ETA_USE["v"] == ETA) else ETA_USE["v"]) * sigma_coll(tag, M)[0] * MSUNE / PC2'),
          ('rows.append(fit_one(q, np.log10(np.maximum(q["GB"] + (GE * Mh / q["Rm"] ** 2)[:, None], 1e-300))))',
           'rows.append(fit_one(q, np.log10(np.maximum(LF_G(q["GB"], (GE * Mh / q["Rm"] ** 2)[:, None], A0[f], "sparc"), 1e-300))))'),
          ('V[i] = dvecN(int(i), foot, hk, pp["Mb"] + Mh)', 'V[i] = dvecN(int(i), foot, hk, LF_M(pp["Mb"], Mh, RM, GX, A0[foot], "clusters"))'),
          ('Mh = math.pi * sc * r0 ** 2 * B(np.minimum(rr, R200) / r0); gN = gN + Mh / Mb / XG ** 2',
           'Mh = math.pi * sc * r0 ** 2 * B(np.minimum(rr, R200) / r0); gN = LF_G(gN, Mh / Mb / XG ** 2, A0[foot] / (G540 * Mb / a ** 2), "groups" if dlM == 0.0 else "groups_d")'),
          ("for cf in (3.0, 5.0):", "for cf in ():"),
          ('f"x43_collapse_core{TAG}.out"', f'"x56_x43copy_{tag}.out"'), ('f"x43_collapse_core_results{TAG}.json"', f'"x56_x43copy_{tag}_results.json"'),
          ('"x43_x30_machinery"', '"x56_x30_machinery"')]
    ns = run_copy(os.path.join(REB, "X43_collapse_core_floor", "x43_collapse_core.py"), ed, "x56_x43copy.py", {"ETA_FUN": eta48 if cfmode == "x48" else None})
    return ns["RES"], ns["LAW"]

# ------------------------------------------------------------------ B. X53 scorer (lensing)
def run_x53(mode, cfmode):
    MODE["m"] = mode; tag = f"{mode}_{cfmode}{TAG}"
    ed = [('return Mb + Mh, (M200, R200, Sig, above)', 'return LF_M(Mb, Mh, RGRID_PC, Gpc, a0u(foot), "lensing"), (M200, R200, Sig, above)'),
          ('tab[gi] = AQ.delta_sigma(Rn[b] * 1e6, RGRID_PC, M, "const")', 'tab[gi] = AQ.delta_sigma(Rn[b] * 1e6, RGRID_PC, M, "linear" if (halo and LAST["law"]) else "const")'),
          ('os.path.join(HERE, "x53_step0_results.json")', repr(os.path.join(REB, "X53_outer_lensing_law_vs_halos", "x53_step0_results.json"))),
          ('H_PRIMARY = dict(bg="A_c2b_refit", cf="cf4", zR200=None)', f'H_PRIMARY = dict(bg="A_c2b_refit", cf="{cfmode}", zR200=None)'),
          ("absorbed=1 - res / e0", "absorbed=1 - res / max(e0, 1e-300)"), ("100 * (1 - res / e0)", "100 * (1 - res / max(e0, 1e-300))"),
          ("{25.0 / e:.2f}", "{25.0 / max(e, 1e-300):.2f}"),   # reported-only lines; e0 = 0 when the two models coincide (law mode)
          ('f"x53_outer_lensing_results{SFX}.json"', f'"x56_x53copy_{tag}_results.json"'), ('f"x53_outer_lensing{SFX}.out"', f'"x56_x53copy_{tag}.out"')]
    ns = run_copy(os.path.join(REB, "X53_outer_lensing_law_vs_halos", "x53_outer_lensing.py"), ed, "x56_x53copy.py")
    return ns["FT"]

# ------------------------------------------------------------------ C. X51 scorer (dwarfs)
def run_x51(mode):
    MODE["m"] = mode; tag = f"{mode}{TAG}"
    ed = [("gp = gN + G * Mh / r12 ** 2", 'gp = float(LF_G(gN, G * Mh / r12 ** 2, A0[f], "dwarfs"))'),
          ('f"x51_dwarfs{TAG}.out"', f'"x56_x51copy_{tag}.out"'), ('f"x51_dwarfs_results{TAG}.json"', f'"x56_x51copy_{tag}_results.json"')]
    ns = run_copy(os.path.join(REB, "X51_dwarf_cooling_floor", "x51_dwarfs.py"), ed, "x56_x51copy.py")
    return ns["RES"]

FEET = ("canonical", "alt"); checks = []; RES = dict(criteria="f17c99a508", mutate=MUTATE, footings={f: {} for f in FEET})
def rel(a, b): return abs(a / b - 1)
# ---------- K0: route E alone reproduces the source lanes
R43off, LAW = run_x43("off", "x48")
X48J = json.load(open(os.path.join(REB, "X48_native_cf_zoom", "x48_regrade_ng48.json")))["footings"]
k0a = all(rel(R43off["footings"][f]["sparc"]["A_c2b_refit"]["rms"], X48J[f]["sparc"]["rms"]) < 1e-3 and abs(R43off["footings"][f]["groups"]["Z"] - X48J[f]["groups"]["Z"]) < 1e-3 for f in FEET)
P(f"K0a law branch off reproduces X48 ng48 regrade (SPARC " + ", ".join(f"{R43off['footings'][f]['sparc']['A_c2b_refit']['rms']:.4f}" for f in FEET) + ", groups Z " + ", ".join(f"{R43off['footings'][f]['groups']['Z']:+.3f}" for f in FEET) + f"): {'PASS' if k0a else 'FAIL'}  [{time.time() - T0:.0f} s]")
F53off4 = run_x53("off", "cf4"); X53J = json.load(open(os.path.join(REB, "X53_outer_lensing_law_vs_halos", "x53_outer_lensing_results.json")))["footings"]
k0b = all(rel(F53off4[f]["all"]["H2H"]["chi2"], X53J[f]["all"]["H2H"]["chi2"]) < 1e-3 for f in FEET)
P(f"K0b law branch off reproduces X53 H2H at c_f 4 (" + ", ".join(f"{F53off4[f]['all']['H2H']['chi2']:.1f}" for f in FEET) + f"; X53 583.9 / 580.6): {'PASS' if k0b else 'FAIL'}  [{time.time() - T0:.0f} s]")
R51off = run_x51("off"); X51J = json.load(open(os.path.join(REB, "X51_dwarf_cooling_floor", "x51_dwarfs_results.json")))["footings"]
k0c = all(abs(R51off["footings"][f]["classes"][c]["median"] - X51J[f]["classes"][c]["median"]) < 1e-3 for f in FEET for c in X51J[f]["classes"])
P(f"K0c law branch off reproduces X51 class medians: {'PASS' if k0c else 'FAIL'}")
checks += [("K0a_x48", k0a), ("K0b_x53", k0b), ("K0c_x51", k0c)]
# ---------- K2: halo branch off reproduces the law
R43law, _ = run_x43("law", "x48"); F53law = run_x53("law", "x48")
k2a = all(rel(R43law["footings"][f]["sparc"]["A_c2b_refit"]["rms"], LAW[f]["rms"]) < 1e-3 for f in FEET)
k2b = all(rel(F53law[f]["all"]["H"]["chi2"], X53J[f]["all"]["L"]["chi2"]) < 1e-3 for f in FEET)
P(f"K2 halo branch off: SPARC " + ", ".join(f"{R43law['footings'][f]['sparc']['A_c2b_refit']['rms']:.4f}" for f in FEET) + f" (EM1 LAW {LAW['canonical']['rms']:.4f} / {LAW['alt']['rms']:.4f}): {'PASS' if k2a else 'FAIL'}; "
  f"lensing chi2 " + ", ".join(f"{F53law[f]['all']['H']['chi2']:.1f}" for f in FEET) + f" (X53 L 160.7 / 127.6): {'PASS' if k2b else 'FAIL'}  [{time.time() - T0:.0f} s]")
checks += [("K2a_sparc_law", k2a), ("K2b_lensing_law", k2b)]
# ---------- primary: LF on, native c_f
STAT.clear()
R43, _ = run_x43("on", "x48"); F53 = run_x53("on", "x48"); F53re = run_x53("off", "x48"); R51 = run_x51("on")
P(f"primary runs done [{time.time() - T0:.0f} s, RSS {rss():.2f} GB]")
S1 = {k: dict(v) for k, v in STAT.items()}
k1 = all(v["viol"] == 0 and v["eqfail"] == 0 for v in S1.values()) and len(S1) >= 5
P("K1 floor property (M_eff >= both branches, equal to one): " + "; ".join(f"{k} n {v['n']} viol {v['viol']} neither {v['eqfail']} law-active {v['law'] / max(v['n'], 1):.3f}" for k, v in S1.items()) + f": {'PASS' if k1 else 'FAIL'}")
checks.append(("K1_floor", k1)); RES["branch_stats"] = S1

def grade(R43_, F53_, F53re_, R51_, lab):
    out = {}
    for f in FEET:
        F = R43_["footings"][f]; sp = {t: F["sparc"][t] for t in F["sparc"]}; gr = F["groups"]; cl = F["clusters"]
        c0 = cl["cells"]["h0672"]; dw = R51_["footings"][f]["classes"]
        Lf, Lre = F53_[f]["all"], F53re_[f]["all"]
        dL = Lf["H2H"]["chi2"] - Lf["L2H"]["chi2"]; dE = Lf["H2H"]["chi2"] - Lre["H2H"]["chi2"]
        dLp = F53_[f]["primary"]["H2H"]["chi2"] - F53_[f]["primary"]["L2H"]["chi2"]
        fails = []
        if not all(s["line"] for s in sp.values()): fails.append("SPARC line")
        if not gr["PASS"]: fails.append(f"groups ({gr['verdict']}, Z {gr['Z']:+.2f})")
        fails += cl["fails"]
        fails += [f"dwarfs {c} ({'UNDER' if v['median'] > 0 else 'OVER'}, Z {v['Z']:+.2f})" for c, v in dw.items() if not abs(v["Z"]) < 2]
        if not (dL <= 9.0 and dE < 0): fails.append(f"lensing (LF2H-L2H {dL:+.1f}, LF2H-H2H {dE:+.1f})")
        v = "LAW FLOOR UNIFIES" if not fails else "LF FAILS: " + ", ".join(fails)
        P(f"\n=== [{f}] {lab}")
        for t, s in sp.items(): P(f"  SPARC [{t}]: rms {s['rms']:.4f}, median U {s['U_median']:.2f}, line {'PASS' if s['line'] else 'FAIL'}")
        P(f"  groups: mean {gr['mean']:+.4f} Z {gr['Z']:+.2f} -> {gr['verdict']}")
        P("  clusters: " + "; ".join(f"{k} {c0[k]['pred']:.2f}/{c0[k]['meas']:.2f} Z {c0[k]['Z']:+.2f}{'' if cl['ok'][k] else ' FAIL'}" for k in c0))
        P("  dwarfs: " + "; ".join(f"{c} {d['median']:+.3f} (Z {d['Z']:+.2f})" for c, d in dw.items()))
        P(f"  lensing all radii: L2H {Lf['L2H']['chi2']:.1f}, LF2H {Lf['H2H']['chi2']:.1f}, route-E H2H {Lre['H2H']['chi2']:.1f}; dchi2(LF2H-L2H) {dL:+.1f}, dchi2(LF2H-H2H) {dE:+.1f}; primary R<=0.31 Mpc dchi2(LF2H-L2H) {dLp:+.1f}")
        P(f"  VERDICT [{f}] ({lab}): {v}")
        out[f] = dict(verdict=v, fails=fails, sparc={t: dict(rms=s["rms"], U=s["U_median"], line=s["line"]) for t, s in sp.items()},
                      groups=dict(mean=gr["mean"], Z=gr["Z"], verdict=gr["verdict"]), clusters={k: dict(pred=c0[k]["pred"], meas=c0[k]["meas"], Z=c0[k]["Z"], ok=cl["ok"][k]) for k in c0},
                      dwarfs={c: dict(median=d["median"], Z=d["Z"]) for c, d in dw.items()},
                      lensing=dict(L2H=Lf["L2H"]["chi2"], LF2H=Lf["H2H"]["chi2"], H2H=Lre["H2H"]["chi2"], d_LF_L=dL, d_LF_H=dE, d_LF_L_primary=dLp))
    return out
RES["footings"] = grade(R43, F53, F53re, R51, "PRIMARY (X48 ng48 c_f)")
V = {f: RES["footings"][f]["verdict"].split(":")[0] for f in FEET}
RES["verdict"] = RES["footings"]["canonical"]["verdict"] if V["canonical"] == V["alt"] else f"UNDECIDED {V}"
# ---------- reported: c_f = 4
if not MUTATE:
    STAT.clear(); R43c4, _ = run_x43("on", "cf4"); F53c4 = run_x53("on", "cf4")
    RES["reported_cf4"] = grade(R43c4, F53c4, F53off4, R51, "REPORTED c_f = 4 (dwarfs as primary)")
P(f"\n=== VERDICT (both footings, frozen rule): {RES['verdict']}")
checks.append(("K3", rss() < 1.0))
P("\n=== CHECKS"); [P(f"  [{'PASS' if ok else 'FAIL'}] {k}") for k, ok in checks]
RES["checks"] = {k: bool(ok) for k, ok in checks}; n = sum(bool(ok) for _, ok in checks)
P(f"\nchecks {n}/{len(checks)}; runtime {time.time() - T0:.0f} s; peak RSS {rss():.2f} GB")
open(os.path.join(HERE, f"x56_law_floor{TAG}.out"), "w").write("\n".join(OUT) + "\n")
json.dump(RES, open(os.path.join(HERE, f"x56_law_floor_results{TAG}.json"), "w"), indent=1, default=float)
for fn in ("x56_x43copy.py", "x56_x53copy.py", "x56_x51copy.py"):
    try: os.remove(os.path.join(HERE, fn))
    except OSError: pass
sys.exit(0 if n == len(checks) else 1)
