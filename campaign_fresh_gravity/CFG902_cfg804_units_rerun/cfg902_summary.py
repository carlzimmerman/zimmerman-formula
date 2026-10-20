"""CFG902 summary: K1-K3, MUTATE, before/after classes.  Criteria: FROZEN_CRITERIA.md (b35efa722).
Reads CFG804's committed results (read-only) and this lane's run outputs (cfg902_run.py).  Run after:
  cfg902_run.py orig canonical | orig alt | declared canonical | declared alt | mutate canonical
kappa = 1/2 FITTED; not theory closed.
"""
import json, os, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
REC_DIR = os.path.join(HERE, "..", "CFG804_catchment_supply_derived")
FOOTS = ("canonical", "alt"); LABS = ("primary", "all"); SFX = {"canonical": "", "alt": "_alt"}
L = []; CH = {}
def P(s=""):
    print(s, flush=True); L.append(str(s))
def check(key, name, ok, v=""):
    CH[key] = bool(ok); P(f"  [{'PASS' if ok else 'FAIL'}] {key} {name} {v}")
ld = lambda p: json.load(open(p))
REC = {f: ld(os.path.join(REC_DIR, f"cfg804_results{SFX[f]}.json")) for f in FOOTS}
RUN = {(m, f): ld(os.path.join(HERE, f"cfg902_results_{m}{SFX[f]}.json")) for m in ("orig", "declared") for f in FOOTS}
RUN[("mutate", "canonical")] = ld(os.path.join(HERE, "cfg902_results_mutate.json"))
EX = {(m, f): ld(os.path.join(HERE, f"cfg902_extras_{m}{SFX[f]}.json")) for (m, f) in RUN}
cls = lambda d: "DERIVED SUPPLY SUFFICES" if d <= 4 else "FALLS SHORT"

P("CFG902  CFG804 rerun with CFG416's declared Msun/h f_ret ramp (h 0.674, shift -0.17134 dex)")
P(f"  runs: " + "; ".join(f"{m}/{f} {EX[(m, f)]['runtime_s']:.0f} s, {EX[(m, f)]['maxrss_MB']:.0f} MB" for (m, f) in EX))

P("\n K1  orig convention vs CFG804's committed results")
for f in FOOTS:
    o, r = RUN[("orig", f)], REC[f]; dmax, pmax, mmax = 0.0, 0.0, 0.0
    for lab in LABS:
        for k in ("chi2_B", "chi2_D", "dchi2"):
            dmax = max(dmax, abs(o[lab][k] - r[lab][k]))
        pmax = max(pmax, abs(o[lab]["p_D"] / r[lab]["p_D"] - 1))
        mmax = max(mmax, max(abs(a - b) for a, b in zip(o[lab]["logMb"], r[lab]["logMb"])))
    same = all(o[k] == r[k] for k in ("K1", "K2", "cls"))
    check(f"K1_{f}", f"chi2/dchi2 max|d| <= 1e-6, p_D rel <= 1e-6, logMb <= 1e-9, K1/K2/cls equal",
          dmax <= 1e-6 and pmax <= 1e-6 and mmax <= 1e-9 and same, f"(max|d chi2| {dmax:.1e}, p_D rel {pmax:.1e}, logMb {mmax:.1e}, flags equal {same})")
    a = open(os.path.join(HERE, f"cfg902_orig{SFX[f]}.out"), "rb").read(); b = open(os.path.join(REC_DIR, f"cfg804{SFX[f]}.out"), "rb").read()
    P(f"       .out byte-identical to cfg804{SFX[f]}.out (reported): {a == b}")

P("\n K2  the change touches only D")
d = max(abs(RUN[("orig", f)][lab]["chi2_B"] - RUN[("declared", f)][lab]["chi2_B"]) for f in FOOTS for lab in LABS)
flags = all(RUN[(m, f)]["K1"] and RUN[(m, f)]["K2"] for m in ("orig", "declared") for f in FOOTS)
check("K2", "chi2_B orig = declared (<= 1e-9, both footings, both radius sets); internal K1/K2 PASS in all non-mutate runs",
      d <= 1e-9 and flags, f"(max|d chi2_B| {d:.1e}; flags {flags})")

P("\n K3  fixed point in the declared convention")
T = EX[("declared", "canonical")]["tables"]["declared"]
k3a = abs(T["K3_logMb_10.5"]["N"] - 10) < 5e-4 and abs(T["K3_logMb_10.5"]["logMta"] - 12.133) <= 0.01
Ns = [x["N"] for x in T["cfg804_primary"]]
k3b = max(abs(a - b) for a, b in zip(Ns, (10.0, 10.0, 9.4, 7.0))) <= 0.05
check("K3", "log M_b 10.5 -> N 10.000, log M_ta[Msun/h] 12.133 +- 0.01; CFG804 canonical primary masses -> CFG886's 10.0/10.0/9.4/7.0 (<= 0.05)",
      k3a and k3b, f"(N {T['K3_logMb_10.5']['N']:.3f}, log M_ta {T['K3_logMb_10.5']['logMta']:.3f}; N " + "/".join(f"{x:.2f}" for x in Ns) + ")")

P("\n MUTATE  doubled shift (h^2, -0.34268 dex), canonical")
TT = EX[("declared", "canonical")]["tables"]; ge, gt = True, False
for lab in ("own_primary", "own_all"):
    for x, y in zip(TT["declared"][lab], TT["mutate"][lab]):
        ge &= y["N"] >= x["N"] - 1e-12; gt |= y["N"] > x["N"] + 1e-9
    P(f"    at declared {lab[4:]} best-fit masses: N declared " + "/".join(f"{x['N']:.2f}" for x in TT["declared"][lab])
      + " -> mutate " + "/".join(f"{x['N']:.2f}" for x in TT["mutate"][lab]))
dd, dm = RUN[("declared", "canonical")]["all"]["dchi2"], RUN[("mutate", "canonical")]["all"]["dchi2"]
dpm = RUN[("mutate", "canonical")]["primary"]["dchi2"]
P(f"    all-radii dchi2: declared {dd:+.2f} -> mutate {dm:+.2f} (change {dm - dd:+.2f}); primary mutate {dpm:+.2f}")
check("MUTATE", "(a) N_mutate >= N_declared every bin, > in >= 1; (b) dchi2_all(mutate) <= dchi2_all(declared) - 1.0",
      ge and gt and dm <= dd - 1.0, f"(a {ge and gt}; b {dm <= dd - 1.0})")

P("\n RESULT  before (CFG804 committed, Msun) / after (declared Msun/h ramp)")
P(f"    {'footing':9s} {'radii':8s} {'B chi2':>7s} {'D before':>9s} {'D after':>8s} {'dchi2 before':>13s} {'dchi2 after':>12s} {'change':>7s}  class before -> after")
TAB = {}
for f in FOOTS:
    for lab in LABS:
        r, n = REC[f][lab], RUN[("declared", f)][lab]; cb, ca = cls(r["dchi2"]), cls(n["dchi2"])
        TAB[f"{f}_{lab}"] = dict(chi2_B=n["chi2_B"], chi2_D_before=r["chi2_D"], chi2_D_after=n["chi2_D"], dchi2_before=r["dchi2"], dchi2_after=n["dchi2"],
                                 change=n["dchi2"] - r["dchi2"], class_before=cb, class_after=ca, class_changed=cb != ca,
                                 logMb_before=r["logMb"], logMb_after=n["logMb"], p_D_after=n["p_D"])
        P(f"    {f:9s} {lab:8s} {n['chi2_B']:7.1f} {r['chi2_D']:9.1f} {n['chi2_D']:8.1f} {r['dchi2']:+13.2f} {n['dchi2']:+12.2f} {n['dchi2'] - r['dchi2']:+7.2f}  "
          f"{cb} -> {ca}  CLASS CHANGED: {'yes' if cb != ca else 'no'}")
P("\n  derived per bin at the declared run's best-fit masses (log M_ta in Msun/h):")
BINS = {}
for f in FOOTS:
    TD = EX[("declared", f)]["tables"]; BINS[f] = {}
    for lab in LABS:
        BINS[f][lab] = TD["declared"][f"own_{lab}"]
        for b, x in enumerate(TD["declared"][f"own_{lab}"]):
            P(f"    [{f} {lab}] bin {b + 1}: log M_b {x['logMb']:.2f} -> log M_ta {x['logMta']:.2f}, f_ret {x['f_ret']:.3f}, N {x['N']:.2f} (grid {x['N_snap']:.2f}), "
              f"edge {x['edge_rM']:.1f} r_M = {x['edge_kpc']:.0f} kpc")
P("\n  fixed-mass convention effect (CFG804's committed best-fit masses; N Msun -> Msun/h):")
for f in FOOTS:
    TD = EX[("declared", f)]["tables"]
    for lab in LABS:
        P(f"    [{f} {lab}] N " + "/".join(f"{x['N']:.2f}" for x in TD["orig"][f"cfg804_{lab}"]) + " -> " + "/".join(f"{x['N']:.2f}" for x in TD["declared"][f"cfg804_{lab}"])
          + "; edge kpc " + "/".join(f"{x['edge_kpc']:.0f}" for x in TD["orig"][f"cfg804_{lab}"]) + " -> " + "/".join(f"{x['edge_kpc']:.0f}" for x in TD["declared"][f"cfg804_{lab}"]))

P("\n R-h (reported only): h 0.6736 instead of 0.674 at the declared best-fit masses")
RH = {}
for f in FOOTS:
    TD = EX[("declared", f)]["tables"]; ch = []
    for lab in LABS:
        for x, y in zip(TD["declared"][f"own_{lab}"], TD["declared_h6736"][f"own_{lab}"]):
            ch.append(dict(radii=lab, N_674=x["N"], N_6736=y["N"], snap_changed=x["N_snap"] != y["N_snap"]))
    RH[f] = ch
    P(f"    [{f}] max |dN| {max(abs(c['N_674'] - c['N_6736']) for c in ch):.4f}; NGRID snap changed in any bin: {any(c['snap_changed'] for c in ch)}")

st = subprocess.run(["git", "status", "--porcelain", "--", os.path.relpath(REC_DIR, HERE), os.path.join("..", "CFG416_supply_edge_confinement_512")],
                    cwd=HERE, capture_output=True, text=True).stdout.strip()
check("UNTOUCHED", "CFG804 and CFG416 directories unchanged (git status empty)", st == "", f"({st or 'clean'})")
ok = all(CH.values())
P(f"\n  K1 canonical/alt, K2, K3, MUTATE, UNTOUCHED: {'ALL PASS' if ok else 'NOT ALL PASS'}")
P("  kappa = 1/2 FITTED; footings never pooled; raw KiDS data; not theory closed.")
json.dump(dict(lane="CFG902", criteria="b35efa722", h=0.674, shift_dex=EX[("declared", "canonical")]["shift_dex"], checks=CH, all_pass=ok,
               result=TAB, bins_declared=BINS, R_h=RH, runs={f"{m}_{f}": dict(runtime_s=EX[(m, f)]["runtime_s"], maxrss_MB=EX[(m, f)]["maxrss_MB"]) for (m, f) in EX}),
          open(os.path.join(HERE, "cfg902_results.json"), "w"), indent=1, default=float)
open(os.path.join(HERE, "cfg902_summary.out"), "w").write("\n".join(L) + "\n")
sys.exit(0 if ok else 1)
