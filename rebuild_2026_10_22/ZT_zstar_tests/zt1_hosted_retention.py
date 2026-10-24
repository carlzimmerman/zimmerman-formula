#!/usr/bin/env python3
"""ZT_zstar_tests / Z-T1: hosted retention of design Z* (v3s-OC), plus the frozen Coma UDG side line.

Frozen line: Z1_successor_design/TEST_PLAN.md section 2 (0d1959a4f5); implementation choices: FROZEN_CRITERIA.md section 2
(this lane, committed alone first).  Per owner i: Delta_pred in [Delta_lo,i, Delta_hi,i],
  Delta_lo,i = 1/2 log10(1 + median gas-to-star ratio of X1's isolated LG field dwarfs within +-0.5 dex in log M*) (RAW HI),
  Delta_hi,i = 1/2 log10(L_MDF_I0_m05,i) from P1.
Observed: X1's class bootstrap median of Delta[iso AQUAL L*0] +- its bootstrap sd.

Run:  OMP_NUM_THREADS=1 nice -n 15 python3 zt1_hosted_retention.py [--mutate]
      --mutate: Newtonian retention (exponent 1, not 1/2) and HI mass without the D^2 factor; K1 and K4 must FAIL.
Read-only inputs only; nothing downloaded; one thread.  kappa = 1/2 FITTED; footings never pooled; no dark-matter particle;
not theory closed."""
import csv, json, math, os, resource, sys, time
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_v] = "1"
import numpy as np
from scipy.special import exp1, digamma, polygamma
from scipy.optimize import brentq, minimize_scalar
from scipy.integrate import quad

T0 = time.time()
HERE = os.path.dirname(os.path.abspath(__file__))
REB = os.path.dirname(HERE)
REPO = os.path.dirname(REB)
MUT = "--mutate" in sys.argv
TAG = "_MUTATE" if MUT else ""
OUT = []
RES = {"lane": "ZT_zstar_tests", "test": "Z-T1", "plan": "Z1_successor_design/TEST_PLAN.md @ 0d1959a4f5", "mutate": MUT}
CHECKS = []


def say(s=""):
    print(s, flush=True); OUT.append(str(s))


def check(k, ok, val, thr, what):
    CHECKS.append((k, bool(ok))); RES.setdefault("checks", {})[k] = dict(pass_=bool(ok), value=str(val), threshold=str(thr), what=what)
    say(f"{k} {'PASS' if ok else 'FAIL'} {val} {thr}  -- {what}")


def fl(x):
    try:
        v = float(x); return v if math.isfinite(v) else None
    except Exception:
        return None


def rss_gb():
    return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / (1e9 if sys.platform == "darwin" else 1e6)


FEET = ("canonical", "alt")
A0 = {"canonical": 9.3603e-11, "alt": 1.1312e-10}
CLASSES = ["MW classical", "bright M31", "MW ultra-faint", "M31 others"]
CONTROL = "LG field"
GAS_FAC = 1.33
EXPO = 1.0 if MUT else 0.5                     # retention exponent: deep law 1/2 (Z1 K9); MUTATE: Newtonian 1

say(f"Z-T1 hosted retention (Z* v3s-OC) {'MUTATE (exponent 1, no D^2 in M_HI)' if MUT else 'normal run'}")
say("kappa = 1/2 FITTED. Footings canonical 9.3603e-11 / alt 1.1312e-10 m/s^2, never pooled. Cold energy, no particle. Not 'theory closed'.")
say("Nothing here says the data favour the framework.")
say()

# ============================================================ inputs
X1DIR = os.path.join(REB, "X1_hosted_recount")
X1 = list(csv.DictReader(open(os.path.join(X1DIR, "x1_per_system.csv"))))
X1J = json.load(open(os.path.join(X1DIR, "x1_hosted_recount_results.json")))
CST = X1J["class_stats"]
P1ROWS = list(csv.DictReader(open(os.path.join(REB, "P1_dwarf_chemistry", "p1_per_system.csv"))))
P1 = {(r["footing"], r["name"]): r for r in P1ROWS}
DSPH = os.path.join(REPO, "real_research", "data", "dsph")
LVD = {}
for fn in ("lvd_dwarf_mw.csv", "lvd_dwarf_m31.csv", "lvd_dwarf_local_field.csv"):
    for r in csv.DictReader(open(os.path.join(DSPH, fn))):
        LVD[r["name"]] = r
S1J = json.load(open(os.path.join(REB, "S1_v3_hosted_small", "s1_v3_hosted_small_results.json")))
C948 = json.load(open(os.path.join(REPO, "campaign_fresh_gravity", "CFG948_nocapture_vs_udgs", "cfg948_results.json")))
E6 = {(r["footing"], r["name"]): r for r in csv.DictReader(open(os.path.join(REPO, "doors_push_2026_10_22", "E6_native_fret",
                                                                               "e6_per_system.csv")))}

# ============================================================ K2: X1 class_stats = X1 README iso-AQUAL row (rounded 0.01)
README_ISO = {"canonical": {"MW classical": 0.28, "MW ultra-faint": 0.63, "bright M31": 0.25, "M31 others": 0.64, "LG field": 0.05},
              "alt": {"MW classical": 0.24, "MW ultra-faint": 0.59, "bright M31": 0.21, "M31 others": 0.59, "LG field": 0.02}}
OBS = {}
k2 = 0.0
for f in FEET:
    for c in CLASSES + [CONTROL]:
        s = CST[f"{f}|{c}|primary|iso AQUAL L*0"]
        OBS[(f, c)] = (float(s["median"]), float(s["sd"]), int(s["N"]))
        k2 = max(k2, abs(round(s["median"], 2) - README_ISO[f][c]))
check("K2", k2 <= 0.005 + 1e-12, f"max |round(class median) - README| {k2:.3f}", "<= 0.005",
      "X1 class_stats (iso AQUAL L*0) reproduce X1's README class table")

# ============================================================ control: RAW HI -> gas-to-star ratios (K1)
members = {f: {c: [r for r in X1 if r["footing"] == f and r["cls"] == c] for c in CLASSES + [CONTROL]} for f in FEET}
ctrl = members["canonical"][CONTROL]
GAS = {}       # name -> dict(logMs, ratio_primary, ratio_ul_at_limit, detected, M_HI)
k1 = 0.0; nk1 = 0
for r in ctrl:
    L = LVD[r["name"]]
    D = fl(L["distance"]) / 1e3                      # Mpc (LVD distance in kpc)
    S = fl(L["flux_HI"]); Sul = fl(L["flux_HI_ul"])
    fac = (D ** 2) if not MUT else D                 # MUTATE: the D^2 factor broken
    lms = float(r["logMstar"]); Ms = 10 ** lms
    if S is not None:
        mhi = 2.356e5 * fac * S
        lv = fl(L["mass_HI"])
        if lv is not None:
            k1 = max(k1, abs(math.log10(mhi) - lv)); nk1 += 1
        GAS[r["name"]] = dict(logMs=lms, ratio=GAS_FAC * mhi / Ms, ratio_ul=GAS_FAC * mhi / Ms, detected=True, logMHI=math.log10(mhi))
    else:
        mul = 2.356e5 * fac * Sul
        GAS[r["name"]] = dict(logMs=lms, ratio=0.0, ratio_ul=GAS_FAC * mul / Ms, detected=False, logMHI_ul=math.log10(mul))
check("K1", k1 <= 0.02 and nk1 >= 11, f"max |log M_HI(flux, D) - LVD mass_HI| {k1:.4f} dex over {nk1} detections", "<= 0.02, all 11",
      "RAW HI masses from LVD flux_HI and distance (M_HI = 2.356e5 D^2 S)")
RES["control_gas"] = GAS
say("   control gas-to-star ratios (1.33 M_HI / M*; upper limits -> 0 primary): " +
    "; ".join(f"{n} {g['logMs']:.2f} {g['ratio']:.3f}{'' if g['detected'] else ' (UL ' + format(g['ratio_ul'], '.3f') + ')'}"
              for n, g in sorted(GAS.items(), key=lambda kv: kv[1]["logMs"])))


def delta_lo(lms, key="ratio", exclude=None, nearest=False):
    win = [g[key] for n, g in GAS.items() if abs(g["logMs"] - lms) <= 0.5 + 1e-12 and n != exclude]
    if not win:
        if not nearest:
            return None, 0
        n_, g_ = min(GAS.items(), key=lambda kv: abs(kv[1]["logMs"] - lms))
        return EXPO * math.log10(1 + g_[key]), 0
    return EXPO * math.log10(1 + float(np.median(win))), len(win)


# ============================================================ K4: deep-AQUAL retention identity (the 1/2 in every edge)
def g_aqual(gN, a0):
    return gN / 2 + math.sqrt(gN ** 2 / 4 + a0 * gN)


k4 = 0.0
for f in FEET:
    a0 = A0[f]
    for ratio in (2.0, 5.0, 20.0):
        x_orig = 1e-6; gN_o = x_orig * a0; gN_n = gN_o / ratio
        d = math.log10(g_aqual(gN_o, a0)) - math.log10(g_aqual(gN_n, a0))
        k4 = max(k4, abs(d - EXPO * math.log10(ratio)))
check("K4", k4 <= 1e-3, f"max |dlog g - e log(M_orig/M_now)| {k4:.2e} dex (e = {EXPO}; x_orig 1e-6, ratios 2/5/20)", "<= 1e-3",
      "deep-law retention identity Delta = 1/2 log(M_orig/M_now) (Z1 K9) on the spherical simple-mu law")

# ============================================================ K3 + E3: P1's lmdf exec'd from its source text (extension gate)
P1SRC = open(os.path.join(REB, "P1_dwarf_chemistry", "p1_dwarf_chemistry.py")).read()


def cut(t, a, b):
    i = t.index(a); j = t.index(b, i); return t[i:j]


NS = dict(np=np, math=math, exp1=exp1, digamma=digamma, polygamma=polygamma, brentq=brentq, minimize_scalar=minimize_scalar,
          quad=quad, MUT=False, P=lambda *a, **k: None, ck=lambda *a, **k: None, fl=fl, sys=sys)
t1 = time.time()
exec(cut(P1SRC, "LN10 = math.log(10.0)", "# ============================================================ inputs"), NS)
exec(cut(P1SRC, "def lvd_sigma(r):", "def width_class(w):"), NS)
exec(cut(P1SRC, "def intervals(w):", "def wget("), NS)
lmdf, lvd_sigma, intervals = NS["lmdf"], NS["lvd_sigma"], NS["intervals"]
say(f"   P1 lmdf/lvd_sigma/intervals exec'd from P1's source ({time.time() - t1:.1f} s grid)")


def mass_g(name):
    mhi = fl(LVD[name].get("mass_HI")) if name in LVD else None
    return GAS_FAC * 10 ** mhi if mhi is not None else 0.0


def L_ext(name, logms):
    lv = LVD.get(name)
    if lv is None:
        return None, "no LVD row"
    feh = fl(lv.get("metallicity")); w = lvd_sigma(lv)
    I0 = intervals(w)[0] if w is not None else None
    if feh is None or I0 is None:
        return None, ("no [Fe/H]" if feh is None else "no MDF width")
    r = lmdf(feh, -0.5, 10 ** logms, mass_g(name), I0)
    return r["L"], r["flag"]


k3 = 0.0; nk3 = 0
for (f, n), r in P1.items():
    if r["tested"] != "True" or fl(r["L_MDF_I0_m05"]) is None:
        continue
    e6 = E6.get(("canonical", n)) or E6.get(("alt", n))
    Lx, _ = L_ext(n, float(e6["logMstar"]))
    k3 = max(k3, abs(Lx / float(r["L_MDF_I0_m05"]) - 1)); nk3 += 1
check("K3", k3 <= 1e-9 and nk3 > 0, f"max rel |L(copy) / L(P1) - 1| {k3:.1e} over {nk3} system-footings", "<= 1e-9",
      "P1's lmdf exec'd from source reproduces P1's committed L_MDF_I0_m05 (gates extension E3)")
E3_OK = CHECKS[-1][1]

# ============================================================ per-owner edges
PER = []
for f in FEET:
    for c in CLASSES + [CONTROL]:
        for r in members[f][c]:
            n = r["name"]; lms = float(r["logMstar"])
            dlo, nwin = delta_lo(lms)
            dlo_e1 = dlo if dlo is not None else 0.0
            dlo_e2, _ = delta_lo(lms, nearest=True)
            dlo_e4, _ = delta_lo(lms, key="ratio_ul")
            dlo_e5, _ = delta_lo(lms, exclude=n) if c == CONTROL else (None, 0)
            p = P1.get((f, n))
            Lp = fl(p["L_MDF_I0_m05"]) if (p is not None and p["tested"] == "True") else None
            dhi = EXPO * math.log10(Lp) if Lp is not None else None
            if Lp is None and E3_OK:
                Le, fe = L_ext(n, lms)
            else:
                Le, fe = Lp, (p["flag_I0"] if Lp is not None else "")
            dhi_e3 = EXPO * math.log10(Le) if Le is not None else None
            PER.append(dict(footing=f, cls=c, name=n, logMstar=lms, Delta_obs_i=float(r["Delta[iso AQUAL L*0]"]),
                            sdMC_i=float(r["sdMC[iso AQUAL L*0]"]), n_window=nwin, Delta_lo=dlo, Delta_lo_E1=dlo_e1, Delta_lo_E2=dlo_e2,
                            Delta_lo_E4=dlo_e4, Delta_lo_E5=dlo_e5, L_MDF_P1=Lp, Delta_hi=dhi, L_MDF_E3=Le, L_E3_flag=fe,
                            Delta_hi_E3=dhi_e3))
RES["per_owner"] = PER


def edge(rows, key):
    vals = [r[key] for r in rows if r[key] is not None]
    cov = len(vals) / len(rows) if rows else 0.0
    return (float(np.median(vals)) if (vals and cov >= 0.5) else None), len(vals), len(rows)


def status(obs, sd, lo, hi):
    if lo is not None and obs < lo - 2 * sd:
        return "OUT (below)"
    if hi is not None and obs > hi + 2 * sd:
        return "OUT (above)"
    if lo is not None and hi is not None:
        return "IN"
    return "UNDETERMINED"


def classify(lo_key, hi_key, label, ctrl_key=None):
    ctrl_key = ctrl_key or lo_key
    T = {}
    for f in FEET:
        for c in CLASSES:
            rows = [r for r in PER if r["footing"] == f and r["cls"] == c]
            lo, nlo, N = edge(rows, lo_key); hi, nhi, _ = edge(rows, hi_key)
            m, sd, _ = OBS[(f, c)]
            T[f"{f}|{c}"] = dict(obs=m, sd=sd, lo=lo, hi=hi, n_lo=nlo, n_hi=nhi, N=N, status=status(m, sd, lo, hi),
                                 lo_all=(float(np.median([r[lo_key] for r in rows if r[lo_key] is not None])) if nlo else None),
                                 hi_all=(float(np.median([r[hi_key] for r in rows if r[hi_key] is not None])) if nhi else None))
        rows = [r for r in PER if r["footing"] == f and r["cls"] == CONTROL]
        lo, nlo, N = edge(rows, ctrl_key)
        m, sd, _ = OBS[(f, CONTROL)]
        T[f"{f}|{CONTROL}"] = dict(obs=m, sd=sd, lo=lo, n_lo=nlo, N=N, z=(m - lo) / sd if lo is not None else None,
                                   status=("PASS" if (lo is not None and abs(m - lo) <= 2 * sd) else ("FAIL" if lo is not None else "UNDEFINED")))
    ins = {f: sum(T[f"{f}|{c}"]["status"] == "IN" for c in CLASSES) for f in FEET}
    outs = {f: sum(T[f"{f}|{c}"]["status"].startswith("OUT") for c in CLASSES) for f in FEET}
    ctl = {f: T[f"{f}|{CONTROL}"]["status"] for f in FEET}
    if any(outs[f] >= 2 for f in FEET) or any(ctl[f] == "FAIL" for f in FEET):
        v = "FAIL"
    elif all(ins[f] >= 3 for f in FEET) and all(ctl[f] == "PASS" for f in FEET):
        v = "PASS"
    else:
        v = "UNDECIDED"
    why = []
    for f in FEET:
        und = [c for c in CLASSES if T[f"{f}|{c}"]["status"] == "UNDETERMINED"]
        if und:
            why.append(f"{f}: UNDETERMINED (edge coverage) in " + ", ".join(und))
    T["_verdict"] = dict(verdict=v, IN=ins, OUT=outs, control=ctl, why=why, label=label)
    say(f"\n--- {label} ---")
    for f in FEET:
        say(f"   [{f}]")
        for c in CLASSES:
            t = T[f"{f}|{c}"]
            fm = lambda x: "  --  " if x is None else f"{x:+.3f}"
            say(f"   {c:15s} N {t['N']:2d}  obs {t['obs']:+.3f} +- {t['sd']:.3f}  band [{fm(t['lo'])} - 2s, {fm(t['hi'])} + 2s]"
                f"  (coverage lo {t['n_lo']}/{t['N']}, hi {t['n_hi']}/{t['N']}; medians over available lo {fm(t['lo_all'])} hi {fm(t['hi_all'])})"
                f"  -> {t['status']}")
        t = T[f"{f}|{CONTROL}"]
        say(f"   {'control LG field':15s} N {t['N']:2d}  obs {t['obs']:+.3f} +- {t['sd']:.3f}  own Delta_lo "
            f"{'--' if t['lo'] is None else format(t['lo'], '+.3f')}  z {'--' if t['z'] is None else format(t['z'], '+.2f')}  -> {t['status']}")
    say(f"   VERDICT ({label}): {v}   IN {ins}  OUT {outs}  control {ctl}")
    for w in why:
        say(f"      {w}")
    return T


RES["frozen"] = classify("Delta_lo", "Delta_hi", "FROZEN (plan inputs only; no substitute)")
VERD = RES["frozen"]["_verdict"]["verdict"]
# missing-input list (what would be needed to complete each UNDETERMINED leg)
MISSING = {}
for f in FEET:
    for c in CLASSES:
        rows = [r for r in PER if r["footing"] == f and r["cls"] == c]
        MISSING[f"{f}|{c}"] = dict(no_isolated_match=[r["name"] for r in rows if r["Delta_lo"] is None],
                                   no_P1_L_MDF=[r["name"] for r in rows if r["Delta_hi"] is None])
RES["missing"] = MISSING
say("\n   missing per class (canonical; alt identical except bright M31 And XXVIII in P1):")
for c in CLASSES:
    m = MISSING[f"canonical|{c}"]
    say(f"   {c}: no isolated LG dwarf within 0.5 dex: {len(m['no_isolated_match'])} ({', '.join(m['no_isolated_match']) or '-'});"
        f" no P1 L_MDF: {len(m['no_P1_L_MDF'])} ({', '.join(m['no_P1_L_MDF']) or '-'})")

# ---------------- reported only (no verdict weight)
say("\n=== REPORTED ONLY (declared extensions E1-E5; never the verdict) ===")
if E3_OK:
    ext3 = [r for r in PER if r["L_MDF_P1"] is None and r["cls"] in CLASSES]
    say("   E3 L_MDF from P1's lmdf on LVD (members without a P1 value): " + "; ".join(
        f"{r['name']} ({r['footing'][:3]}) " + (f"L {r['L_MDF_E3']:.2f} [{r['L_E3_flag']}]" if r["L_MDF_E3"] is not None else f"-- [{r['L_E3_flag']}]")
        for r in ext3 if r["footing"] == "canonical"))
RES["E1_E3"] = classify("Delta_lo_E1", "Delta_hi_E3", "EXTENSION E1+E3 (empty window -> 0; P1 lmdf on LVD where P1 has none)")
RES["E2_E3"] = classify("Delta_lo_E2", "Delta_hi_E3", "EXTENSION E2+E3 (empty window -> nearest isolated dwarf; P1 lmdf on LVD)")
RES["E4"] = classify("Delta_lo_E4", "Delta_hi", "E4 (HI upper limits at the limit; plan inputs otherwise)")
RES["E5"] = classify("Delta_lo", "Delta_hi", "E5 (control leave-one-out; plan inputs otherwise)", ctrl_key="Delta_lo_E5")

# ============================================================ Coma UDG side line (frozen)
say("\n=== Coma UDG side line (frozen: Delta_pred = 1/2 log10(1/(1 - 0.81)) vs S1's isolated-law excess, PASS within 2 sigma) ===")
fg = float(C948["R6_HUD"]["Ups1.0|all"]["median"])
check("K5", round(fg, 2) == 0.81 and all(abs(round(S1J["coma"][f"{f}|S0 old: isolated nu_e law (CFG933)"]["meanE"] / math.log(10), 3) - v) < 1e-9
                                         for f, v in (("canonical", 0.330), ("alt", 0.291))),
      f"CFG948 HUD f_gas median {fg:.4f}; S1 S0 {S1J['coma']['canonical|S0 old: isolated nu_e law (CFG933)']['meanE'] / math.log(10):.4f} / "
      f"{S1J['coma']['alt|S0 old: isolated nu_e law (CFG933)']['meanE'] / math.log(10):.4f} dex", "0.81; 0.330 / 0.291",
      "Coma inputs (CFG948 R6, S1)")
dpred = EXPO * math.log10(1 / (1 - 0.81))
COMA = {"Delta_pred": dpred, "Delta_pred_unrounded_fgas": EXPO * math.log10(1 / (1 - fg)),
        "Delta_pred_Ups0.5": EXPO * math.log10(1 / (1 - C948["R6_HUD"]["Ups0.5|all"]["median"])),
        "Delta_pred_Ups2.0": EXPO * math.log10(1 / (1 - C948["R6_HUD"]["Ups2.0|all"]["median"]))}
for f in FEET:
    s2 = S1J["coma"][f"{f}|S2 AQUAL isolated L*0 E-W"]; s0 = S1J["coma"][f"{f}|S0 old: isolated nu_e law (CFG933)"]
    obs = s2["meanE"] / math.log(10); sig = s2["se"] / math.log(10); sigt = math.hypot(s2["se"], s2["sigma_sys"]) / math.log(10)
    z = (obs - dpred) / sig
    COMA[f] = dict(obs_S2=obs, sigma_stat=sig, sigma_tot=sigt, obs_S0=s0["meanE"] / math.log(10), z_stat=z, z_tot=(obs - dpred) / sigt,
                   status="PASS" if abs(z) <= 2 else "FAIL")
    say(f"   [{f}] Delta_pred {dpred:+.3f}  obs (S2 AQUAL isolated) {obs:+.3f} +- {sig:.3f} (stat; tot {sigt:.3f})  z {z:+.2f} (tot {COMA[f]['z_tot']:+.2f})"
        f"  -> {COMA[f]['status']}   [S0 law {COMA[f]['obs_S0']:+.3f}]")
say(f"   reported: Delta_pred at CFG948 unrounded {fg:.4f}: {COMA['Delta_pred_unrounded_fgas']:+.3f}; Upsilon_g 0.5 / 2 brackets "
    f"{COMA['Delta_pred_Ups0.5']:+.3f} / {COMA['Delta_pred_Ups2.0']:+.3f}")
RES["coma"] = COMA

# ============================================================ close
pk = rss_gb()
check("K6", pk < 1.0, f"peak RSS {pk:.3f} GB", "< 1 GB", "memory")
npass = sum(ok for _, ok in CHECKS)
RES.update(verdict=VERD, coma_status={f: COMA[f]["status"] for f in FEET}, runtime_s=time.time() - T0, peak_rss_GB=pk)
say(f"\nZ-T1 FROZEN VERDICT: {VERD}   Coma side line: " + ", ".join(f"{f} {COMA[f]['status']}" for f in FEET))
say(f"ZT1 COMPLETE: {npass}/{len(CHECKS)} checks PASS. [{time.time() - T0:.0f} s]")
open(os.path.join(HERE, f"zt1_hosted_retention{TAG}.out"), "w").write("\n".join(OUT) + "\n")
json.dump(RES, open(os.path.join(HERE, f"zt1_hosted_retention_results{TAG}.json"), "w"), indent=1,
          default=lambda o: o.tolist() if hasattr(o, "tolist") else (float(o) if isinstance(o, (np.floating, np.integer)) else str(o)))
if not MUT:
    keys = list(PER[0].keys())
    with open(os.path.join(HERE, "zt1_per_owner.csv"), "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=keys); w.writeheader(); [w.writerow(p) for p in PER]
sys.exit(0 if npass == len(CHECKS) else 1)
