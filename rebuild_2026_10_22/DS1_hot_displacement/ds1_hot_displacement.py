#!/usr/bin/env python3
"""DS1_hot_displacement: a hot atmosphere displaces the cold dark energy halo (X-ray-bright groups on the law, hot gas counted).
Frozen criteria 456bf76c7c (committed alone). Machinery: HO1's committed script (91cc5c3bd4) executed read-only up to its grade
block, with __file__ in this folder so every machinery output lands here. Base lines: BS1 (979363d820) is untouched by the
PRIMARY scope; its rerun identity is checked separately (README). UNIVERSAL clusters: CL2's committed law-only run.

kappa = 1/2 FITTED; footings never pooled; cold dark energy = gravitating w ~ 0 field component, not a particle; not theory closed;
nothing here says the data favour the framework.
Run:  PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 -I ds1_hot_displacement.py      (DS1_MUTATE=1 twin)
"""
import os, sys, json, hashlib, resource
import numpy as np

MUT = os.environ.get("DS1_MUTATE", "0") == "1"
TAG = "_MUTATE" if MUT else ""
HERE = os.path.dirname(os.path.abspath(__file__)); REB = os.path.dirname(HERE); REPO = os.path.dirname(REB)
HO1 = os.path.join(REB, "HO1_xcop_hotgas_heldout", "ho1_heldout.py")
src = open(HO1).read()
cut = src.index("# ------------------------------------------------------------------ 6. grade per footing")
src = src[:cut]
# the HO1 Step-0 stop branch would write HO1-named files; redirect it to DS1 names (no rule changes)
src = src.replace('"ho1_heldout.out"', '"ds1_ho1_step0_STOPPED.out"').replace('"ho1_heldout_results.json"', '"ds1_ho1_step0_STOPPED.json"')
os.environ.pop("HO1_MUTATE", None)
NS = {"__file__": os.path.join(HERE, "ho1_ro.py"), "__name__": "ho1_ro"}
exec(compile(src, HO1, "exec"), NS)
P, rows, ref, hg1, lo0, hi0 = NS["P"], NS["rows"], NS["ref"], NS["hg1"], NS["lo0"], NS["hi0"]
A0, nu, group_pred, FEET = NS["A0"], NS["nu"], NS["group_pred"], NS["FEET"]
P("\n================ DS1_hot_displacement (criteria 456bf76c7c)" + ("  [MUTATE: BRIGHT/FAINT swapped in the branch]" if MUT else ""))
checks = {}
gbar = np.array([r["gbar"] for r in rows]); lref = ref.logref(gbar)
sup = np.isfinite(NS["base"])
RES = dict(criteria="456bf76c7c", machinery="HO1 91cc5c3bd4 (read-only)", mutate=MUT, footings={})
for f in FEET:
    gbase, above, _, _ = group_pred(f)                                   # base picture (HO1(b)): EM1 R1 switch, X43 group halos
    Dbase = hg1.D_stat(rows, np.log10(gbase) - lref)[0]
    glaw = gbar * nu(gbar / A0[f])
    hot = np.array([(r["flag"] == "BRIGHT") != MUT for r in rows])        # MUTATE: labels swapped in the branch assignment
    gds = np.where(hot, glaw, gbase)
    exp_b = gbar * nu(gbar / A0[f])
    k1 = all(abs(gds[i] / exp_b[i] - 1) < 1e-12 for i in range(len(rows)) if rows[i]["flag"] == "BRIGHT") and \
         all(abs(gds[i] / gbase[i] - 1) < 1e-12 for i in range(len(rows)) if rows[i]["flag"] == "FAINT")
    dpred = np.log10(gds) - lref
    D, nb, nf = hg1.D_stat(rows, dpred)
    Dall = hg1.D_stat(rows, np.log10(glaw) - lref)[0]                    # reported: every group on the law
    # bin-by-bin BRIGHT - FAINT (0.1 dex sigma bins, HG1's convention via D_stat on single bins is internal; report arm medians)
    arms = {fl: dict(n=int(sum(1 for i in range(len(rows)) if rows[i]["flag"] == fl and sup[i])),
                     median_pred_vs_ref=float(np.median([dpred[i] for i in range(len(rows)) if rows[i]["flag"] == fl and sup[i]])),
                     on_halo=int(sum(1 for i in range(len(rows)) if rows[i]["flag"] == fl and sup[i] and above[i] and not hot[i])))
            for fl in ("BRIGHT", "FAINT")}
    ok = lo0 <= D <= hi0
    verdict = "HOT DISPLACEMENT FIXES THE GROUP SIGN" if ok else f"HOT DISPLACEMENT FAILS: HG2 D_pred {D:+.3f} ({'ABOVE' if D > hi0 else 'BELOW'} [{lo0:+.3f}, {hi0:+.3f}])"
    k0 = abs(Dbase - {"canonical": 0.2293, "alt": 0.2011}[f]) < 5e-5
    checks[f"K0_{f}"] = bool(k0); checks[f"K1_{f}"] = bool(k1)
    P(f"\n=== [{f}] a0 {A0[f]:.6e}")
    P(f"  K0 base D_pred {Dbase:+.4f} (HO1(b) {'+0.2293' if f == 'canonical' else '+0.2011'}): {'PASS' if k0 else 'FAIL'}")
    P(f"  K1 BRIGHT = law on baryons (hot gas counted), FAINT = base, to 1e-12: {'PASS' if k1 else 'FAIL'}")
    P(f"  (B) HG2 D_pred under DS = {D:+.4f} (BRIGHT {nb} / FAINT {nf}) vs measured [{lo0:+.3f}, {hi0:+.3f}] -> {'PASS' if ok else 'FAIL'}")
    P(f"      reported: all groups on the law D {Dall:+.4f}; arm medians pred-vs-ref BRIGHT {arms['BRIGHT']['median_pred_vs_ref']:+.3f}, "
      f"FAINT {arms['FAINT']['median_pred_vs_ref']:+.3f}; FAINT on halos {arms['FAINT']['on_halo']} of {arms['FAINT']['n']}")
    P(f"  PRIMARY VERDICT [{f}]: {verdict}  (C: base lines untouched by PRIMARY - BS1 committed grade stands; see README)")
    RES["footings"][f] = dict(D_pred=D, D_base=Dbase, D_all_law=Dall, interval=[lo0, hi0], n_bright=nb, n_faint=nf, arms=arms, primary_verdict=verdict)
# UNIVERSAL: clusters on the law on measured baryons = CL2's committed law-only run (x62_x43copy_law_a2)
LJ = json.load(open(os.path.join(REB, "CL2_native_cf_slope", "x62_x43copy_law_a2_results.json")))
for f in FEET:
    cl = LJ["footings"][f]["clusters"]
    fails = cl["fails"]
    uv = "DISPLACEMENT IS UNIVERSAL" if (not fails and RES["footings"][f]["primary_verdict"].startswith("HOT DISPLACEMENT FIXES")) else \
         f"DISPLACEMENT NEEDS A SCOPE: {len(fails)} failing cluster cells" + ("" if RES["footings"][f]["primary_verdict"].startswith("HOT DISPLACEMENT FIXES") else "; group sign also fails")
    RES["footings"][f]["universal"] = dict(cluster_fails=fails, ratio_median=cl["ratio_median"], verdict=uv)
    P(f"  UNIVERSAL [{f}]: clusters on the law (CL2 law run): pred/meas median {cl['ratio_median']:.2f}; {len(fails)} failing cells -> {uv}")
peak = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1e9
checks["K2_rss"] = peak < 1.0
P(f"\n  K2 peak RSS {peak:.2f} GB: {'PASS' if checks['K2_rss'] else 'FAIL'}")
RES["checks"] = checks
fn = os.path.join(HERE, f"ds1_hot_displacement_results{TAG}.json")
json.dump(RES, open(fn, "w"), indent=1, default=float)
P(f"checks {sum(checks.values())}/{len(checks)}; results sha256 {hashlib.sha256(open(fn, 'rb').read()).hexdigest()}")
open(os.path.join(HERE, f"ds1_hot_displacement{TAG}.out"), "w").write("\n".join(NS["OUT"]).replace(REPO, "<repo>") + "\n")
sys.exit(0 if all(checks.values()) else 1)
