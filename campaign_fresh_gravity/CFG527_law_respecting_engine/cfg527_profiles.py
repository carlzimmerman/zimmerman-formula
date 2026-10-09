#!/usr/bin/env python3
"""CFG527 Gate 1 (FROZEN_CRITERIA.md): law consistency with CFG526's statistic, reused UNCHANGED.
cfg526_profiles.py is imported as a module; only its run table (RUNS), its work directory and the per-run mix (MIXA / NOFILT, set after
CFG526's load_engine exactly as the run was launched) are replaced.  compute / analyse / kcheck / conv_stat are CFG526's functions.
Stage 1 (`compute`, heavy, cached in _external_data/cfg527_work/profiles): engine `forces` (cfg527_pm.py) on each saved z = 0 state.
Stage 2 (default): K1-K3, R = M_grav/M_law per run, the Gate-1 verdict per footing (frozen rules), MUTATE A / K1 / SHF / MUTATE B reported.
Usage: python3 cfg527_profiles.py compute [run ...] ;  python3 cfg527_profiles.py"""
import os, sys, json, math, importlib.util
HERE = os.path.dirname(os.path.abspath(__file__))
CFG = os.path.abspath(os.path.join(HERE, ".."))
EXT = os.path.abspath(os.path.join(HERE, "..", "..", "..", "_external_data"))
spec = importlib.util.spec_from_file_location("cfg526p", os.path.join(CFG, "CFG526_small_scale_deficit_judged", "cfg526_profiles.py"))
C = importlib.util.module_from_spec(spec); spec.loader.exec_module(C)
import numpy as np

W527, W521, W359 = (os.path.join(EXT, d) for d in ("cfg527_work", "cfg521_work", "cfg359_work"))
C.WORK = os.path.join(W527, "profiles"); os.makedirs(C.WORK, exist_ok=True)
E521 = C.E521
E527 = os.path.join(HERE, "cfg527_pm.py")

def t527(mix, draw, L, foot="canonical", mode="census", nocomp=False):
    return os.path.join(W527, f"cfg527_RES_TA{'_NOCOMP' if nocomp else ''}_{mix}_MASSCONS_fret{mode}_FLAT_{foot}_N256"
                        + (f"_L{L}" if L != 200 else "") + f"_draw{draw}")
RUNS = {}; MIXOF = {}
for L in (50, 25, 100):
    RUNS[f"S0_L{L}"] = (L, E521, "CFG521", {}, "S0", "canonical", C.t521("S0", L))
RUNS["S0_L200"] = (200, E521, "CFG521", {}, "S0", "canonical", os.path.join(W359, "cfg359_S0_FLAT_canonical_N256"))
for L in (200, 100, 50, 25):
    RUNS[f"LRcan_L{L}"] = (L, E527, "CFG527", {"DRAW": "SHELL"}, "RES", "canonical", t527("NOFILT", "SHELL", L))
    RUNS[f"LRalt_L{L}"] = (L, E527, "CFG527", {"DRAW": "SHELL"}, "RES", "alt", t527("NOFILT", "SHELL", L, "alt"))
    MIXOF[f"LRcan_L{L}"] = MIXOF[f"LRalt_L{L}"] = "NOFILT"
for L in (50, 25):
    RUNS[f"K1_L{L}"] = (L, E527, "CFG527", {"DRAW": "SHELL", "FRET_MODE": "one"}, "RES", "canonical", t527("NOFILT", "SHELL", L, mode="one"))
    RUNS[f"MUTA_L{L}"] = (L, E527, "CFG527", {"DRAW": "SC"}, "RES", "canonical", t527("MIXA", "SC", L))
    RUNS[f"SHF_L{L}"] = (L, E527, "CFG527", {"DRAW": "SHELL"}, "RES", "canonical", t527("MIXA", "SHELL", L))
    MIXOF[f"K1_L{L}"] = "NOFILT"; MIXOF[f"MUTA_L{L}"] = MIXOF[f"SHF_L{L}"] = "MIXA"
RUNS["MUTB_L200"] = (200, E527, "CFG527", {"DRAW": "SHELL", "NOCOMP": "1"}, "RES", "canonical", t527("NOFILT", "SHELL", 200, nocomp=True))
MIXOF["MUTB_L200"] = "NOFILT"
ORDER = ["S0_L50", "S0_L25", "S0_L100", "S0_L200",
         "LRcan_L50", "LRcan_L25", "LRalt_L50", "LRalt_L25", "MUTA_L50", "MUTA_L25",
         "LRcan_L100", "LRalt_L100", "LRcan_L200", "LRalt_L200", "K1_L50", "K1_L25", "SHF_L50", "SHF_L25", "MUTB_L200"]
C.RUNS = RUNS
_load0 = C.load_engine
def load_engine(name):
    mod = _load0(name)                                   # CFG526's loader (sets env, RC = 0, MIX = MIXA, NTH)
    mod.MIX = MIXOF.get(name, "MIXA")                    # the mix the run was launched with
    return mod
C.load_engine = load_engine

if __name__ == "__main__" and len(sys.argv) > 1 and sys.argv[1] == "compute":
    try: os.nice(10)
    except OSError: pass
    for n in (sys.argv[2:] or ORDER):
        if not os.path.exists(RUNS[n][6] + ".json"):
            print("not yet run", n, flush=True); continue
        C.compute(n)
    sys.exit(0)

# ============================================================== stage 2
LINES = []
def P(s=""):
    print(s); LINES.append(s)
T = 10 ** -0.1
inside = lambda x: x is not None and abs(math.log10(x)) <= 0.1

def pairs_stat(hA, hB, pairs):
    """CFG526 conv_stat's rule (median log10 R, log M_ta in [12.7, 14.3], >= 10 halos in both) on the given index pairs."""
    out = []
    for jA, jB in pairs:
        mA = hA["scored"][:, jA] & (hA["lM"] >= 12.7) & (hA["lM"] <= 14.3)
        mB = hB["scored"][:, jB] & (hB["lM"] >= 12.7) & (hB["lM"] <= 14.3)
        if mA.sum() >= 10 and mB.sum() >= 10:
            a = float(np.median(np.log10(hA["R"][mA, jA]))); b = float(np.median(np.log10(hB["R"][mB, jB])))
            out.append({"r_phys": float(hA["reff"][jA]), "nA": int(mA.sum()), "nB": int(mB.sum()), "logR_coarse": a, "logR_fine": b, "d": b - a})
        else:
            out.append({"r_phys": float(hA["reff"][jA]), "nA": int(mA.sum()), "nB": int(mB.sum()), "skip": True})
    return out

def main():
    A, H, KOK = {}, {}, {}
    P("CFG527 Gate 1: engine gravitating M(<r) vs candidate B's law profile (CFG526 statistic unchanged), z = 0, 256^3 seed 359")
    P("kappa = 1/2 FITTED; footings never pooled; a0 flat; cold energy MASS still required; not theory closed.")
    P("R = M_grav/M_law (scored radii r_eff <= census edge r_e); D = M/M_S0 (matched S0 peak within +-2 cells); median [16, 84].")
    for name in ORDER:
        if not os.path.exists(os.path.join(C.WORK, f"cfg526_{name}.npz")):
            P(f"\n{name}: MISSING"); continue
        if RUNS[name][4] == "S0":
            d = np.load(os.path.join(C.WORK, f"cfg526_{name}.npz")); res = {"K": json.loads(str(d["K"])), "name": name}
            ok, why = C.kcheck(name, res); KOK[name] = ok; A[name] = {"K_ok": ok, "K": why}
            P(f"\n{name}: integrity {'PASS' if ok else 'FAIL'} ({why})"); continue
        res, h = C.analyse(name)
        ok, why = C.kcheck(name, res); KOK[name] = ok; res["K_ok"] = ok; res["K_why"] = why
        A[name] = res; H[name] = h
        P(f"\n{name}  (L = {res['L']}, cell {res['L'] / C.NP:.3f} Mpc/h, {res['foot']}, mix {MIXOF[name]})  integrity {'PASS' if ok else 'FAIL'}: {why}")
        P(f"  hosts {res['n_hosts']}, scored available {res['n_scored_avail']}, used {res['n_scored']}")
        if h is None: continue
        P(f"  log M_ta {res['lM_range'][0]:.2f}-{res['lM_range'][1]:.2f}; median census edge {res['re_cells_med']:.2f} cells; median r_M {res['rM_med']:.4f} Mpc/h")
        P("   R(cells) r_eff   n   R=Mgrav/Mlaw          R_noexp  R_in     D_eng   D_part  D_law   r/r_M    Mp/Mlaw")
        for p in res["per"]:
            if p["n"] == 0:
                P(f"   {p['R_cells']:4.1f} {p['r_eff']:.3f} {p['n']:4d}   (beyond edge; all-halo R {p['all_R'][0]:.3f}, D_eng {p['all_D_eng'][0]:.3f}, D_law {p['all_D_law'][0]:.3f})")
                continue
            P(f"   {p['R_cells']:4.1f} {p['r_eff']:.3f} {p['n']:4d}   {C.fmt(p['R'])}  {p['R_noexp'][0]:.3f}    {p['R_in'][0]:.3f}    "
              f"{p['D_eng'][0]:.3f}   {p['D_part'][0]:.3f}   {p['D_law'][0]:.3f}   {p['r_over_rM'][0]:6.1f}   {p['Mp_over_Mlaw'][0]:.2f}")
        c = res["core"]
        P(f"  CORE (scored, <= 2 cells, n = {c['n']}): R {C.fmt(c['R'])}; R_noexp {c['R_noexp'][0]:.3f}; R_in {c['R_in'][0]:.3f}; "
          f"D_eng {c['D_eng'][0]:.3f}; D_part {c['D_part'][0]:.3f}; D_law {c['D_law'][0]:.3f}")

    def gate1(tag):
        n50, n25, n100 = f"{tag}_L50", f"{tag}_L25", f"{tag}_L100"
        out = {"items": {}}
        if n50 not in A or n25 not in A:
            out.update(verdict="PENDING"); return out
        k_ok = KOK[n50] and KOK[n25] and KOK["S0_L50"] and KOK["S0_L25"] and all(KOK.get(f"S0_L{L}", True) for L in (100, 200))
        nsc = [A[n50]["n_scored"], A[n25]["n_scored"]]
        c50 = pairs_stat(H[n50], H[n25], ((0, 2), (2, 4), (3, 5), (4, 6)))          # CFG526 conv_stat pairs (L50 1,2,3,4 = L25 2,4,6,8 cells)
        c100 = pairs_stat(H[n100], H[n50], ((0, 2), (2, 4), (4, 6))) if n100 in H and H[n100] is not None else []   # frozen: L100 1,2,4 = L50 2,4,8
        ev50 = [c for c in c50 if not c.get("skip")]; ev100 = [c for c in c100 if not c.get("skip")]
        out.update(conv_L50_L25=c50, conv_L100_L50=c100, n_scored=nsc, K_ok=k_ok)
        if not k_ok or min(nsc) < 20 or not ev50:
            out.update(verdict="NOT DIAGNOSTIC", why=("integrity" if not k_ok else "< 20 scored halos" if min(nsc) < 20 else "no evaluable shared radius L50-L25"))
            return out
        bad = []
        for n in (n50, n25):
            for p in A[n]["per"]:
                if p["n"] >= 1 and not inside(p["R"][0]):
                    bad.append(f"{n} R({p['R_cells']:g} cells) = {p['R'][0]:.3f}")
            if not inside(A[n]["core"]["R"][0]):
                bad.append(f"{n} core R = {A[n]['core']['R'][0]:.3f}")
        for c in ev50:
            if abs(c["d"]) > 0.1: bad.append(f"L50-L25 convergence at r = {c['r_phys']:.3f}: d log R = {c['d']:+.3f}")
        for c in ev100:
            if abs(c["d"]) > 0.1: bad.append(f"L100-L50 convergence at r = {c['r_phys']:.3f}: d log R = {c['d']:+.3f}")
        cell = {}
        for L in (200, 100, 50, 25):
            n = f"{tag}_L{L}"
            if n in A and A[n].get("n_scored", 0) >= 20:
                cell[L] = A[n]["core"]["R"][0]
                if not inside(cell[L]): bad.append(f"cell-unit: {n} core R = {cell[L]:.3f}")
        lc = [math.log10(v) for v in cell.values()]
        out.update(cell_unit_core_R=cell, cell_unit_spread_dex=(max(lc) - min(lc)) if lc else None,
                   core_R=[A[n50]["core"]["R"][0], A[n25]["core"]["R"][0]],
                   core_D_law=[A[n50]["core"]["D_law"][0], A[n25]["core"]["D_law"][0]],
                   core_D_eng=[A[n50]["core"]["D_eng"][0], A[n25]["core"]["D_eng"][0]])
        if not bad:
            out.update(verdict="LAW-CONSISTENT", why="all scored radii and cores within 0.1 dex in L50 and L25; converged (physical and cell units)")
        else:
            cr = out["core_R"]
            lab = "SHORTFALL" if cr[0] < T and cr[1] < T else ("EXCESS" if cr[0] > 1 / T and cr[1] > 1 / T else "DEPARTS")
            out.update(verdict=f"NOT LAW-CONSISTENT ({lab})", why="; ".join(bad))
        return out

    V = {"canonical": gate1("LRcan"), "alt": gate1("LRalt")}
    REP = {}
    for tag in ("MUTA", "K1", "SHF"):
        n50, n25 = f"{tag}_L50", f"{tag}_L25"
        if n50 in A and n25 in A and "core" in A[n50] and "core" in A[n25]:
            REP[tag] = {"core_R": [A[n50]["core"]["R"][0], A[n25]["core"]["R"][0]], "K_ok": [KOK[n50], KOK[n25]],
                        "n_scored": [A[n50]["n_scored"], A[n25]["n_scored"]],
                        "all_scored_within_0.1dex": all(inside(p["R"][0]) for n in (n50, n25) for p in A[n]["per"] if p["n"] >= 1)
                                                    and all(inside(A[n]["core"]["R"][0]) for n in (n50, n25))}
    if "MUTB_L200" in A and "core" in A["MUTB_L200"]:
        REP["MUTB_L200"] = {"core_R": A["MUTB_L200"]["core"]["R"][0], "n_scored": A["MUTB_L200"]["n_scored"]}
    # MUTATE A must NOT be law-consistent (frozen): it fails if any core / scored radius is outside 0.1 dex
    mA = REP.get("MUTA")
    mA_fails = None if mA is None else (not mA["all_scored_within_0.1dex"])
    P("\nGate 1 per footing:")
    for f, v in V.items():
        P(f"  [{f}] {v['verdict']}" + (f" -- {v.get('why', '')}" if v.get("why") else ""))
        for key, lab in (("conv_L50_L25", "L50->L25"), ("conv_L100_L50", "L100->L50")):
            for c in v.get(key, []):
                P(f"      {lab} r = {c['r_phys']:.3f}: " + ("skipped (n %d / %d)" % (c["nA"], c["nB"]) if c.get("skip")
                  else f"coarse {c['logR_coarse']:+.3f} (n {c['nA']})  fine {c['logR_fine']:+.3f} (n {c['nB']})  d {c['d']:+.3f}"))
        if v.get("cell_unit_core_R"):
            P("      cell-unit core R: " + ", ".join(f"L{L} {x:.3f}" for L, x in v["cell_unit_core_R"].items())
              + f"  (spread {v['cell_unit_spread_dex']:.3f} dex)")
    P("\nControls / reported:")
    for k, v in REP.items():
        P(f"  {k}: {json.dumps(v)}")
    P(f"  MUTATE A must NOT be law-consistent: {'OK (fails law consistency)' if mA_fails else ('PENDING' if mA_fails is None else 'NO -> statistic has no teeth -> NOT DIAGNOSTIC')}")
    json.dump({"runs": A, "gate1": V, "reported": REP, "MUTA_fails_law": mA_fails, "mix": MIXOF},
              open(os.path.join(HERE, "cfg527_profiles.json"), "w"), indent=1)
    open(os.path.join(HERE, "cfg527_profiles.out"), "w").write("\n".join(LINES) + "\n")

if __name__ == "__main__":
    main()
