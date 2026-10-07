#!/usr/bin/env python3
"""CFG396: the "two-regime" rule (phantom acts only where rho_cold < rho_ph, capped at rho_ph - rho_cold) vs CFG361's T5.
Criteria: FROZEN_CRITERIA.md (e66c7ca1d).  Step 0 identity gate (G0 algebra, G1 field level), then, because the rule is
identical to T5, the verdict is INHERITED from CFG361's committed numbers (no PM rerun), with controls C1 (reproduction from
the run JSONs) and C2 (gate forced open -> larger over-build).
Run: python3 cfg396_two_regime.py            -> cfg396_two_regime.out / cfg396_two_regime_results.json
     CFG396_MUTATE=1 python3 cfg396_two_regime.py -> regime gate disabled in the independent implementation; G1 must FAIL (rc 1),
                                                     outputs *_MUTATE.out / *_MUTATE_results.json
Reads (read-only): CFG372's engine (imported, TGAS = 0 = no gas filter), CFG361's T5 FLAT canonical z = 0 snapshot and run
JSONs, CFG359's S0 256^3 JSON, CFG361's committed _results.json.
"""
import os, sys, json, time
os.environ.setdefault("CFG372_THREADS", "4")
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
CFG = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(CFG, "CFG372_pressure_filtered_phantom"))
import cfg372_pm as E  # noqa: E402  (engine copy of CFG366/CFG361; read-only import)

MUTATE = os.environ.get("CFG396_MUTATE", "0") == "1"
SUF = "_MUTATE" if MUTATE else ""
EXT = os.path.abspath(os.path.join(CFG, "..", "..", "_external_data"))
W361, W359 = os.path.join(EXT, "cfg361_work"), os.path.join(EXT, "cfg359_work")
WORK = os.path.join(EXT, "cfg396_work"); os.makedirs(WORK, exist_ok=True)
E.DTA_FILE = os.path.join(W361, "cfg361_delta_ta_table.json")   # read the cached table; never write into another lane
E.TGAS = 0.0
OUTL = []
def P(s=""):
    print(s, flush=True); OUTL.append(s)
CHK = {}
def check(name, ok, measured):
    CHK[name] = {"pass": bool(ok), "measured": measured}; P(("PASS  " if ok else "FAIL  ") + name + ": " + measured)

t0 = time.time()
P(__doc__.strip()); P()
P("G0 (algebra). Engine T5 (cfg361_pm.py / cfg366_pm.py / cfg372_pm.py):  extra = fsw * max(s_ph - s_c, 0).")
P("   Two-regime rule: extra = 0 where s_c >= s_ph (cold regime: ordinary cold matter, phantom adds nothing);")
P("                    extra = s_ph - s_c where s_c < s_ph (phantom regime, capped at rho_ph - rho_cold); times the bound switch f.")
P("   => piecewise definition of max(0, s_ph - s_c) times f: term-for-term the same expression, same s_c (engine's CIC cell")
P("      density x (1 - f_b)), same s_ph (baryon-only, unfiltered), same f. G0: IDENTICAL.")
P("   CFG366's 'literal local min rule' (dark <= cold present, added on top of the Newtonian cold) adds 0 = S0: NOT this rule.")
P("   CFG366/372 RES = this rule's e minus its catchment average: this rule is RES's R_c -> infinity limit (CFG366 C2a).")
P()

# ---------------------------------------------------------------- G1: field level on CFG361's evolved z = 0 field
N = 128
mesh = E.Mesh(N); dta = E.dta_table()
pos = np.load(os.path.join(W361, "cfg361_T5_FLAT_canonical_N256_z0.npz"))["pos"].astype(np.float64)
delta = mesh.deposit(pos).astype(np.float32); a = 1.0

def two_regime_force(foot, gate=True):
    """independent implementation: explicit regime masks, not np.maximum."""
    _, info = E.forces(mesh, delta, a, "T1", "FLAT", foot, dta, diag=True)
    fsw = info.pop("_grids")[0].astype(np.float64)
    dk = mesh.fwd(delta); phik = (-1.5 * E.Om / a) * dk * mesh.ik2
    gb = [E.FB * (-mesh.inv(1j * kv * phik)) for kv in mesh.kvec]
    y = np.sqrt(gb[0] ** 2 + gb[1] ** 2 + gb[2] ** 2) / (a * E.a0_code(a, "FLAT", foot))
    w = (E.nu_mono(y) - 1.0).astype(np.float32)
    s_ph = -mesh.inv(sum(1j * kv * mesh.fwd(w * g) for kv, g in zip(mesh.kvec, gb))).astype(np.float64)
    s_c = (1.5 * E.Om * (1.0 - E.FB) / a) * (1.0 + delta.astype(np.float64))
    cold_reg = s_c >= s_ph; ph_reg = ~cold_reg
    src = np.zeros_like(s_ph)
    if gate:
        src[ph_reg] = s_ph[ph_reg] - s_c[ph_reg]        # capped at rho_ph - rho_cold; cold regime stays 0
    else:
        src = s_ph.copy()                                # MUTATE: regime gate disabled (= CFG359 ADD source)
    src *= fsw
    phik2 = phik - mesh.fwd(src.astype(np.float32)) * mesh.ik2
    acc = [-a * mesh.inv(1j * kv * phik2) for kv in mesh.kvec]
    rho = 1.0 + delta.astype(np.float64); on = fsw > 0.5
    st = dict(mass_on=float((rho * on).mean()), mass_on_phantom_regime=float((rho * (on & ph_reg)).mean()),
              mass_on_cold_regime=float((rho * (on & cold_reg)).mean()), vol_on=float(on.mean()))
    return acc, st

G1 = {}
for foot in ("canonical", "alt"):
    acc_t5, _ = E.forces(mesh, delta, a, "T5", "FLAT", foot, dta)
    acc_s0, _ = E.forces(mesh, delta, a, "S0", "FLAT", foot, dta)
    acc_tr, st = two_regime_force(foot, gate=not MUTATE)
    d = max(float(np.abs(x - y).max()) for x, y in zip(acc_tr, acc_t5))
    sc = max(float(np.abs(x - y).max()) for x, y in zip(acc_t5, acc_s0))
    fr = st["mass_on_phantom_regime"] / max(st["mass_on"], 1e-30)
    G1[foot] = dict(max_force_diff=d, t5_extra_force_scale=sc, rel=d / max(sc, 1e-30), phantom_regime_share_of_on_mass=fr, **st)
    P(f"G1 {foot:9s}: max|F_two-regime - F_T5| = {d:.3e}, T5 extra-force scale {sc:.3e}, rel {d / max(sc, 1e-30):.2e}; "
      f"ON mass {st['mass_on']:.4f}: phantom regime {st['mass_on_phantom_regime']:.4f} ({fr:.1%}), cold regime {st['mass_on_cold_regime']:.4f}")
    check(f"G1 two-regime force == engine T5 force ({foot}; rel <= 1e-5; non-vacuous)",
          d <= 1e-5 * sc and st["mass_on_phantom_regime"] > 0 and sc > 0, f"rel {d / max(sc, 1e-30):.2e}, phantom-regime ON mass {st['mass_on_phantom_regime']:.4f}")
identical = all(v["pass"] for k, v in CHK.items() if k.startswith("G1"))
P(f"\nStep 0 decision: {'IDENTICAL to CFG361 T5 -> STOP, no PM rerun; verdict inherited' if identical else 'NOT identical (as computed)'}\n")

# ---------------------------------------------------------------- C1 reproduction + inherited verdict
def ratios(r, r0):
    s, s0 = r["snap"]["z0"], r0["snap"]["z0"]
    k = np.array(s["k"]); pr = np.array(s["P"]) / np.array(s0["P"]); m = k <= 1.0
    return dict(sig8=s["sigma8"] / s0["sigma8"], pk_maxdev=float(np.max(np.abs(pr[m] - 1))),
                pk_at={f"{kk}": float(np.interp(kk, k, pr)) for kk in (0.1, 0.3, 1.0)})
def verdict(rows):
    ds = max(abs(x["sig8"] - 1) for x in rows); dp = max(x["pk_maxdev"] for x in rows)
    if ds > 0.20: return "FAIL"
    if ds <= 0.05 and dp <= 0.10: return "GROWTH OK"
    return "TENSION"
def foot_verdict(x):
    return verdict([x])
r0 = json.load(open(os.path.join(W359, "cfg359_S0_FLAT_canonical_N256.json")))
COM = json.load(open(os.path.join(CFG, "CFG361_pm_growth_T5_bookkeeping", "cfg361_pm_growth_T5_results.json")))["numbers"]["ratios"]
R = {}
for sw in ("T5", "ADD", "S1T5"):
    for foot in ("canonical", "alt"):
        t = f"{sw}_FLAT_{foot}_N256"
        R[t] = ratios(json.load(open(os.path.join(W361, f"cfg361_{t}.json"))), r0)
dmax = max(max(abs(R[t]["sig8"] - COM[t]["z0"]["sig8"]), abs(R[t]["pk_maxdev"] - COM[t]["z0"]["pk_maxdev"])) for t in R)
check("C1 re-derived ratios (T5/ADD/S1T5 FLAT, both footings) match CFG361's committed _results.json to 1e-6", dmax <= 1e-6, f"max |diff| {dmax:.1e}")
P("\nINHERITED VERDICT (two-regime == T5; CFG361 256^3, ratios to CFG359 S0 at z = 0; CFG361's cuts):")
P(f"  {'run':26s} {'sigma8 ratio':>12s} {'max|P-1| k<=1':>14s}   P@0.1/0.3/1        per-footing verdict")
for t, x in R.items():
    P(f"  {t:26s} {x['sig8']:12.4f} {x['pk_maxdev']:14.3f}   " + " / ".join(f"{v:.3f}" for v in x["pk_at"].values()) + f"   {foot_verdict(x)}")
lane = verdict([R["T5_FLAT_canonical_N256"], R["T5_FLAT_alt_N256"]])
P(f"\nLANE VERDICT (two-regime = T5 A0-FLAT, both footings): {lane}")
okc2 = all(R[f"ADD_FLAT_{f}_N256"]["sig8"] > R[f"T5_FLAT_{f}_N256"]["sig8"] for f in ("canonical", "alt"))
check("C2 regime gate forced open (ADD) over-builds more than the gated rule (sigma8 ratio, both footings)", okc2,
      " | ".join(f"{f}: ADD {R[f'ADD_FLAT_{f}_N256']['sig8']:.4f} vs gated {R[f'T5_FLAT_{f}_N256']['sig8']:.4f}" for f in ("canonical", "alt")))
P("  (spatial gate forced open, f = 1 everywhere = CFG361 S1T5: " +
  " | ".join(f"{f} {R[f'S1T5_FLAT_{f}_N256']['sig8']:.4f}" for f in ("canonical", "alt")) + ")")
P(f"\nCFG372 comparator (its README): T = 1e6 K sigma8 1.0089 / 1.0105 (GROWTH OK, WITHDRAWN by the 10-06 k_J audit); the two-regime "
  f"rule is CFG372's T = 0 / R_c -> infinity limit and gives {R['T5_FLAT_canonical_N256']['sig8']:.3f} / {R['T5_FLAT_alt_N256']['sig8']:.3f}.")
P(f"runtime {time.time() - t0:.0f} s" + ("  (MUTATE)" if MUTATE else ""))
allok = all(v["pass"] for v in CHK.values())
P(f"{sum(v['pass'] for v in CHK.values())}/{len(CHK)} checks pass")
json.dump({"lane": "CFG396", "frozen": "e66c7ca1d", "mutate": MUTATE, "G0": "identical (term-for-term max(0, s_ph - s_c) * f)",
           "G1": G1, "identical_to_T5": identical, "checks": CHK, "inherited_ratios": R, "lane_verdict": lane,
           "per_footing": {t: foot_verdict(x) for t, x in R.items()}, "runtime_s": time.time() - t0},
          open(os.path.join(HERE, f"cfg396_two_regime{SUF}_results.json"), "w"), indent=1)
open(os.path.join(HERE, f"cfg396_two_regime{SUF}.out"), "w").write("\n".join(OUTL) + "\n")
sys.exit(0 if allok else 1)
