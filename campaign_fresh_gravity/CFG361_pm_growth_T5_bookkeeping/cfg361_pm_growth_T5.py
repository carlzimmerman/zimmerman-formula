#!/usr/bin/env python3
"""
CFG361 analysis: CFG359's nonlinear PM growth test redone with B's bookkeeping.  Criteria: FROZEN_CRITERIA.md (6373544c3).
Reads the run JSONs written by cfg361_pm.py (via cfg361_run_all.py) in ../_external_data/cfg361_work/; S0 at 256^3 and
CFG359's additive T1 A0-FLAT JSONs are read READ-ONLY from ../_external_data/cfg359_work/ (fallback: this lane's own S0).
Scores T5 (primary; A0-FLAT = lane verdict, A0-CRIT separate, A0-DE reported), S (own verdicts), T5F / S1T5 reported;
controls K1-K6.  Never pooled across footings or branches.  Writes cfg361_pm_growth_T5.out / _results.json here.
Run from the repository root:  python3 campaign_fresh_gravity/CFG361_pm_growth_T5_bookkeeping/cfg361_pm_growth_T5.py
"""
import os, sys, json
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
_argv = sys.argv; sys.argv = [sys.argv[0]]
import cfg361_pm as C
sys.argv = _argv
W359 = os.path.join(os.path.dirname(C.WORK), "cfg359_work")
OUT = {"lane": "CFG361", "frozen": "6373544c3", "checks": {}, "numbers": {}}
LOG = []
def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); LOG.append(s)
def check(name, ok, measured=""):
    OUT["checks"][name] = {"pass": bool(ok), "measured": str(measured)}
    P(f"  [{'PASS' if ok else 'FAIL'}] {name}: {measured}"); return bool(ok)
def banner(t): P("\n" + "=" * 100 + "\n" + t + "\n" + "=" * 100)
FOOTS, ZN = ("canonical", "alt"), ("z1", "z0.5", "z0")

def tg(sw, br, ft, n=256, amp=1.0, mut=False):
    return f"{sw}_{br}_{ft}_N{n}" + (f"_amp{amp:g}" if amp != 1 else "") + ("_MUTATE" if mut else "")
def load(sw, br, ft, n=256, amp=1.0, mut=False, where="361"):
    t = tg(sw, br, ft, n, amp, mut)
    p = os.path.join(C.WORK, f"cfg361_{t}.json") if where == "361" else os.path.join(W359, f"cfg359_{t}.json")
    return json.load(open(p)) if os.path.exists(p) else None
def ratios(r, r0, zn="z0"):
    s, s0 = r["snap"][zn], r0["snap"][zn]
    k = np.array(s["k"]); pr = np.array(s["P"]) / np.array(s0["P"]); m = k <= 1.0
    return dict(sig8=s["sigma8"] / s0["sigma8"], pk_maxdev=float(np.max(np.abs(pr[m] - 1))),
                pk_at={f"{kk}": float(np.interp(kk, k, pr)) for kk in (0.1, 0.3, 1.0)})
def verdict(rows):
    ds = max(abs(x["sig8"] - 1) for x in rows); dp = max(x["pk_maxdev"] for x in rows)
    if ds > 0.20: return "FAIL", ds, dp
    if ds <= 0.05 and dp <= 0.10: return "GROWTH OK", ds, dp
    return "TENSION", ds, dp

P(__doc__.strip())
banner("MODEL: CFG359 engine copy; only the ON-cell source changes (T5 / S / T5F / ADD); kappa = 1/2 fixed; nu_mono")
P("  ** The ONLY LCDM input: the linear EH no-wiggle spectrum for the Zel'dovich ICs at z_i = 49 (CFG324). **")
P("  S0 = Newtonian control (not 'LCDM'). Box 200 Mpc/h, 256^3 on 256^3, seed 359, 150 KDK steps. No dark-matter particle.")

banner("K6  Delta_ta(z) vs CFG354 K4 (11.806 at z = 0, 6.412 at z = 1)")
dt = C.dta_table()
check("K6 Delta_ta reproduces CFG354 K4 (1%)", abs(dt["D"][0] / 11.806 - 1) < 0.01 and abs(dt["D"][4] / 6.412 - 1) < 0.01, f"{dt['D'][0]:.3f} / {dt['D'][4]:.3f}")

r0 = load("S0", "FLAT", "canonical", where="359"); src = "CFG359 (read-only)"
if r0 is None:
    r0 = load("S0", "FLAT", "canonical"); src = "CFG361 own"
P(f"  S0 256^3 source: {src}; sigma8 z0 {r0['snap']['z0']['sigma8']:.4f}")
OUT["numbers"]["S0_source"] = src

banner("RATIOS TO S0 at z = 0 (sigma8 ratio; max |P ratio - 1| for k <= 1 h/Mpc; P ratio at k = 0.1/0.3/1), plus ON diagnostics")
TAB = {}
for sw, brs in (("T5", ("FLAT", "CRIT", "DE")), ("S", ("FLAT", "CRIT")), ("T5F", ("FLAT",)), ("ADD", ("FLAT",)), ("S1T5", ("FLAT",))):
    for br in brs:
        for ft in FOOTS:
            r = load(sw, br, ft)
            if r is None:
                P(f"  {tg(sw, br, ft):26s} MISSING"); continue
            t = tg(sw, br, ft); z0s = r["snap"]["z0"]
            TAB[t] = {zn: ratios(r, r0, zn) for zn in ZN}
            TAB[t]["diag_z0"] = {k: z0s[k] for k in z0s if k in ("vol_f", "mass_f", "vol_on", "vol_on_knot", "vol_on_fil", "mass_on",
                                 "mass_on_phantom_dom", "y_median", "nu_median", "tau", "S_nreg", "S_fex_mass", "S_fex0_mass")}
            d = TAB[t]["diag_z0"]; z0 = TAB[t]["z0"]
            pdom = d.get("mass_on_phantom_dom", float("nan")) / max(d.get("mass_on", 1e-30), 1e-30)
            P(f"  {t:26s} s8 {z0['sig8']:.4f}  Pdev {z0['pk_maxdev']:.4f}  P@0.1/0.3/1 " + " / ".join(f"{v:.3f}" for v in z0["pk_at"].values())
              + f" | z0.5 {TAB[t]['z0.5']['sig8']:.4f} z1 {TAB[t]['z1']['sig8']:.4f} | ON vol {d['vol_on']:.4f} <f>_mass {d['mass_f']:.4f}"
              + f" | phantom-dominated share of ON mass {pdom:.3f}" + (f" | S: {d['S_nreg']} regions, <f_ex>_mass {d['S_fex_mass']:.3f}" if "S_nreg" in d else ""))
OUT["numbers"]["ratios"] = TAB

banner("DECISION (frozen; per branch; both footings; never pooled)")
VER = {}
for sw, br, lab in (("T5", "FLAT", "[LANE VERDICT]"), ("T5", "CRIT", "[separate branch]"), ("T5", "DE", "[reported only]"),
                    ("S", "FLAT", "[S reading, own verdict]"), ("S", "CRIT", "[S reading, own verdict]"),
                    ("T5F", "FLAT", "[reported only]"), ("S1T5", "FLAT", "[reported only]"), ("ADD", "FLAT", "[control = CFG359 T1]")):
    rows = [TAB[tg(sw, br, ft)]["z0"] for ft in FOOTS if tg(sw, br, ft) in TAB]
    if len(rows) == 2:
        v, ds, dp = verdict(rows); VER[f"{sw}_{br}"] = dict(verdict=v, max_sig8_shift=ds, max_pk_dev=dp)
        P(f"  {sw:4s} A0-{br:4s}: {v:9s} (max |sigma8 ratio - 1| {ds:.4f}; max |P ratio - 1| k<=1 {dp:.4f})  {lab}")
OUT["numbers"]["verdicts"] = VER

banner("CONTROLS K1-K5")
k1 = {}
for ft in FOOTS:
    a = load("ADD", "FLAT", ft); b = load("T1", "FLAT", ft, where="359")
    if a and b:
        k1[ft] = (ratios(a, r0)["sig8"], ratios(b, r0)["sig8"])
check("K1 ADD reproduces CFG359 T1 A0-FLAT sigma8 ratio (|d| <= 0.01, both footings)", len(k1) == 2 and all(abs(x - y) <= 0.01 for x, y in k1.values()),
      " | ".join(f"{f}: {x:.4f} vs {y:.4f}" for f, (x, y) in k1.items()))
OUT["numbers"]["K1"] = k1
rl = load("T5", "FLAT", "canonical", amp=0.01)
if rl:
    s = rl["snap"]; k = np.array(s["zi"]["k"]); m = k <= 0.1; dev = {}
    for zn in ZN:
        g = np.sqrt(np.array(s[zn]["P"])[m] / np.array(s["zi"]["P"])[m]) / (s[zn]["D"] / s["zi"]["D"]); dev[zn] = float(np.max(np.abs(g - 1)))
    check("K2 T5 linear (amp 0.01) matches D(a) to 1% (k <= 0.1)", max(dev.values()) <= 0.01, json.dumps({a: round(b, 5) for a, b in dev.items()}) + f"; ON vol z0 {s['z0']['vol_on']:.2e}")
    OUT["numbers"]["K2"] = dev
k3 = {}
for ft in FOOTS:
    a = load("T5", "FLAT", ft, mut=True); b = load("T5", "FLAT", ft)
    if a and b:
        k3[ft] = (ratios(a, r0)["sig8"], ratios(b, r0)["sig8"])
check("K3 MUTATE (s_c := 0 in the max) sigma8 ratio exceeds T5's by > 0.01 (both footings)", len(k3) == 2 and all(x - y > 0.01 for x, y in k3.values()),
      " | ".join(f"{f}: MUTATE {x:.4f} vs T5 {y:.4f}" for f, (x, y) in k3.items()))
OUT["numbers"]["K3"] = k3
a = load("T5", "FLAT", "canonical", n=128); b = load("S0", "FLAT", "canonical", n=128)
if a and b and "T5_FLAT_canonical_N256" in TAB:
    lo = ratios(a, b); hi = TAB["T5_FLAT_canonical_N256"]["z0"]
    check("K4 resolution: T5 A0-FLAT canonical verdict unchanged 128^3 -> 256^3", verdict([lo])[0] == verdict([hi])[0],
          f"{lo['sig8']:.4f} (128^3, {verdict([lo])[0]}) vs {hi['sig8']:.4f} (256^3, {verdict([hi])[0]})")
    OUT["numbers"]["K4"] = dict(N128=lo, N256=hi)
k5 = {}
for ft in FOOTS:
    t5, ad, s1 = (TAB.get(tg(sw, "FLAT", ft), {}).get("z0", {}).get("sig8") for sw in ("T5", "ADD", "S1T5"))
    if None not in (t5, ad, s1):
        k5[ft] = dict(T5=t5, ADD=ad, S1T5=s1, ok=bool(t5 <= ad and t5 <= s1))
check("K5 monotonicity (reported): sigma8(T5) <= sigma8(ADD) and <= sigma8(S1T5), both footings", len(k5) == 2 and all(v["ok"] for v in k5.values()),
      " | ".join(f"{f}: T5 {v['T5']:.4f}, ADD {v['ADD']:.4f}, S1T5 {v['S1T5']:.4f}" for f, v in k5.items()))
OUT["numbers"]["K5"] = k5

json.dump(OUT, open(os.path.join(HERE, "cfg361_pm_growth_T5_results.json"), "w"), indent=1)
open(os.path.join(HERE, "cfg361_pm_growth_T5.out"), "w").write("\n".join(LOG) + "\n")
