#!/usr/bin/env python3
"""CFG200 -- the DR4 separation forecast with the corrected P2 merge band (relayed from CFG191, re-run pending).
Frozen criteria: FROZEN_CRITERIA.md here (7a5f6a314), committed before any number.  kappa = 1/2 FITTED, NOT DERIVED.
A forecast from frozen budgets: no data are scored, nothing in the preregistration is changed, and no verdict language is
added (row labels are quoted from the frozen text).  CFG63's algebra is reused (its script is read only, not imported).
Run:  python3 campaign_fresh_gravity/CFG200_dr4_merge_band_forecast/cfg200_merge_forecast.py      (MUTATE=1: merge = 1.000)
"""
import os, sys, math, hashlib
sys.dont_write_bytecode = True
from scipy.stats import norm

LANE = os.path.dirname(os.path.abspath(__file__))
CFG = os.path.dirname(LANE)
REPO = os.path.dirname(CFG)
sys.path.insert(0, CFG)
_mut = os.environ.pop("MUTATE", None)
try:
    import CFG7_common as C
finally:
    if _mut is not None:
        os.environ["MUTATE"] = _mut
MODE = (_mut or "").strip()
assert MODE in ("", "0", "1")
MUT = MODE == "1"
R = C.Report("cfg200_merge_forecast", MUT)
P, check = R.P, R.check
P(__doc__.split("Run:")[0].strip())
INF = float("inf")

# ------------------------------------------------------------------------------------------------ C0 citations
PRE = "prep_2026/gaia_dr4_prep/PREREGISTRATION_DR4.md"
F63 = "campaign_fresh_gravity/CFG63_discrimination_forecast/README.md"
CITES = {
    "SYS": (PRE, 617, "sigma_sys = 0.02"), "TOT": (PRE, 622, "sigma_tot = sqrt(sigma_fit^2 + 0.02^2)"),
    "N": (PRE, 629, "N = 30,000 assumed"), "SCALE": (PRE, 630, "sigma_fit scales as sqrt(30000/N)"),
    "SIGFIT": (PRE, 631, "sigma_fit ≈ 0.019, sigma_tot ≈ 0.028"), "DR3": (PRE, 674, "10,624 pairs): gamma = 1.205 ± 0.035"),
    "T1": (PRE, 636, "| ≤ 1.007 |"), "T2": (PRE, 637, "| 1.007 – 1.083 |"), "T3": (PRE, 638, "| 1.083 – 1.145 |"),
    "ARMA_C": (PRE, 947, "1.1614 ± 0.0175"), "ARMA_A": (PRE, 948, "1.1917 ± 0.0175"),
    "C1": (PRE, 1331, "| ≤ 0.916 |"), "C2": (PRE, 1332, "| 0.916 – 0.944 |"), "C3": (PRE, 1333, "| 0.944 – 1.056 |"),
    "C4": (PRE, 1334, "| 1.056 – 1.084 |"), "C5": (PRE, 1335, "| 1.084 – 1.23 |"), "C6": (PRE, 1336, "| > 1.23 |"),
    "CH": (PRE, 1426, "**1.0725** | **1.0900**"), "CH1": (PRE, 1471, "| ≤ 1.0725 (≤ 1.0900) |"),
    "CH2": (PRE, 1472, "| 1.0725 – 1.157 (1.0900 – 1.174) |"), "CH3": (PRE, 1473, "| ≥ 1.157 (≥ 1.174) |"),
    "R63_A": (F63, 15, "4,342 pairs"), "R63_CH": (F63, 17, "58,850 (alt 21,660)"),
}
# (fixed after the first run, kept as *_firstrun*: the two CFG63 README line numbers were 13 / 15 instead of 15 / 17, so C0
#  failed on them; the prereg citations and every number were unaffected)
sha = hashlib.sha256(open(os.path.join(REPO, PRE), "rb").read()).hexdigest()
bad = []
for k, (f, ln, txt) in CITES.items():
    lines = open(os.path.join(REPO, f)).read().split("\n")
    if ln > len(lines) or txt not in lines[ln - 1]:
        bad.append(k)
check("C0 every cited (file, line) contains its cited text; prereg sha256 prefix as frozen (97aa97c40fc1be25)",
      f"{len(CITES)} citations; failures {bad or 'none'}; sha256 {sha[:16]}", not bad and sha.startswith("97aa97c40fc1be25"))

# ------------------------------------------------------------------------------------------------ inputs
SIGSYS, SIGFIT30, NF = 0.02, 0.019, 30000
V1 = SIGFIT30 ** 2 * NF
V1_DR3, N_DR3 = 0.035 ** 2 * 10624, 10624
OWN = 1.000
CEIL = {"canonical": 1.0725, "alt": 1.0900}
ARMA = {"canonical": 1.1614, "alt": 1.1917}
MERGE = {("canonical", "g_ext 1.778e-10 (primary)"): (1.089, 1.102), ("canonical", "g_ext 2.146e-10"): (1.063, 1.077),
         ("alt", "g_ext 1.778e-10 (primary)"): (1.111, 1.127), ("alt", "g_ext 2.146e-10"): (1.079, 1.099)}
if MUT:
    MERGE = {k: (1.000, 1.000) for k in MERGE}
    P("  MUTATE=1: every P2-merge value set to 1.000")


def st(v1, n):
    return math.sqrt(v1 / n + SIGSYS ** 2)


def S(d, v1, n):
    return abs(d) / st(v1, n)


def nk(d, v1, k):
    t = (abs(d) / k) ** 2 - SIGSYS ** 2
    return INF if t <= 0 else v1 / t


def cap(d):
    return abs(d) / SIGSYS


def f(x):
    return "inf" if x == INF else (f"{x:,.0f}" if x >= 1000 else f"{x:.2f}")


R.banner("C1  CFG63'S COMMITTED ROWS, REPRODUCED WITH THE SAME ALGEBRA")
s_a = S(1.1614 - 1.0, V1, NF); n_a = nk(1.1614 - 1.0, V1, 3); n_ch = nk(0.0725, V1, 3); n_cha = nk(0.0900, V1, 3)
check("C1 B vs Arm A floor: S(30,000) = 5.85, N(3s) = 4,342; chain vs Newton: N(3s) = 58,850 canonical / 21,660 alt",
      f"S = {s_a:.3f}, N3 = {n_a:,.0f}; chain N3 = {n_ch:,.0f} / {n_cha:,.0f}",
      abs(s_a - 5.85) < 0.005 and round(n_a) == 4342 and round(n_ch) == 58850 and round(n_cha) == 21660)
P(f"  sigma_tot(30,000) frozen = {st(V1, NF):.5f};  DR3-like: at 10,624 = {st(V1_DR3, N_DR3):.5f}, at 30,000 = {st(V1_DR3, NF):.5f}")

# ------------------------------------------------------------------------------------------------ separations
R.banner("SEPARATIONS  (S at N; N for 2 and 3 sigma; cap = Delta / sigma_sys at infinite N)")
rows = []


def rowp(label, d):
    r = dict(pair=label, delta=abs(d), S30=S(d, V1, NF), S_dr3_10624=S(d, V1_DR3, N_DR3), S_dr3_30000=S(d, V1_DR3, NF),
             N2=nk(d, V1, 2), N3=nk(d, V1, 3), N3_dr3=nk(d, V1_DR3, 3), cap=cap(d))
    rows.append(r)
    P(f"  {label:66s} Delta {r['delta']:.4f}  S(30k) {r['S30']:5.2f}  S(DR3-like: 10,624 / 30k) {r['S_dr3_10624']:5.2f} / "
      f"{r['S_dr3_30000']:5.2f}  N2 {f(r['N2']):>9s}  N3 {f(r['N3']):>9s}  (DR3-like {f(r['N3_dr3']):>9s})  cap {f(r['cap'])}")
    return r


SEP = {}
for foot in ("canonical", "alt"):
    P(f"\n  -- {foot} footing (chain ceiling {CEIL[foot]}, Arm A floor {ARMA[foot]}) --")
    SEP[(foot, "c")] = rowp(f"(c) chain ceiling vs ownership 1.000 [{foot}]", CEIL[foot] - OWN)
    for (ft, case), (lo, hi) in MERGE.items():
        if ft != foot:
            continue
        for anc, v in (("floor", lo), ("top", hi)):
            SEP[(foot, case, anc, "a")] = rowp(f"(a) P2-merge {anc} {v:.3f} vs ownership [{case}]", v - OWN)
            SEP[(foot, case, anc, "b")] = rowp(f"(b) P2-merge {anc} {v:.3f} vs chain ceiling {CEIL[foot]} [{case}]", v - CEIL[foot])
            SEP[(foot, case, anc, "d")] = rowp(f"(d) P2-merge {anc} {v:.3f} vs Arm A floor {ARMA[foot]} [{case}]", ARMA[foot] - v)

# ------------------------------------------------------------------------------------------------ landing
R.banner("LANDING  (gamma-hat ~ N(T, sigma_tot(30,000)); contamination NOT modelled; row labels quoted from the frozen text)")
s30 = st(V1, NF)
LAB15 = [("<= 1.007", "supports Newtonian over framework-MI"), ("1.007-1.083", "no hypothesis separation ... undecided"),
         ("1.083-1.23", "framework-band, arm NOT decided (Amendment 11(d))"), ("> 1.23", "contamination-guard zone, no verdict")]
LABC = [("<= 0.916", "disfavored (z_C <= -3)"), ("0.916-0.944", "2-3 sigma below, not a kill"), ("0.944-1.056", "consistent"),
        ("1.056-1.084", "disfavored at 2-3 sigma, not a kill"), ("1.084-1.23", "falsified if the stability requirements pass"),
        ("> 1.23", "no verdict")]
LABCH = [("<= ceiling", "consistent, at or below the ceiling"), ("ceiling-(+3s)", "above the ceiling, within 3 sigma: not a kill"),
         ("(+3s)-1.23", "falsified at every allowed xi, if the stability requirements pass"), ("> 1.23", "no verdict")]


def probs(T, edges):
    cdf = [norm.cdf((e - T) / s30) for e in edges]
    ps = [cdf[0]] + [cdf[i] - cdf[i - 1] for i in range(1, len(cdf))] + [1 - cdf[-1]]
    return ps


def edges(foot, mode):
    if mode == "illustrative":
        e15 = [1.007, 1.083, 1.23]
        ec = [0.916, 0.944, 1.056, 1.084, 1.23]
        ech = [CEIL[foot], 1.157 if foot == "canonical" else 1.174, 1.23]
    else:
        e15 = [1.09 - 3 * s30, 1.0 + 3 * s30, 1.23]
        ec = [1 - 3 * s30, 1 - 2 * s30, 1 + 2 * s30, 1 + 3 * s30, 1.23]
        ech = [CEIL[foot], CEIL[foot] + 3 * s30, 1.23]
    return e15, ec, ech


LAND = {}
norm_ok = True
for foot in ("canonical", "alt"):
    targets = [("ownership 1.000", OWN), (f"chain ceiling {CEIL[foot]}", CEIL[foot])]
    for (ft, case), (lo, hi) in MERGE.items():
        if ft == foot:
            targets += [(f"P2-merge floor {lo:.3f} [{case}]", lo), (f"P2-merge top {hi:.3f} [{case}]", hi)]
    P(f"\n  -- {foot} footing {'(DECIDES)' if foot == 'canonical' else '(reported)'} --")
    for name, T in targets:
        zt = {"z to 1.000": (T - 1.0) / s30, "z to chain": (T - CEIL[foot]) / s30, "z to Arm A floor": (T - ARMA[foot]) / s30,
              "z to 1.09": (T - 1.09) / s30, "z to 1.137": (T - 1.137) / s30}
        P(f"    T = {T:.4f}  {name}")
        P("      z at T: " + ", ".join(f"{k} {v:+.2f}" for k, v in zt.items()))
        for mode in ("illustrative", "z-rule"):
            e15, ec, ech = edges(foot, mode)
            p15, pc, pch = probs(T, e15), probs(T, ec), probs(T, ech)
            norm_ok &= all(abs(sum(p) - 1) < 1e-12 for p in (p15, pc, pch))
            LAND[(foot, name, mode)] = dict(T=T, z=zt, sec15=dict(zip([a for a, _ in LAB15], p15)),
                                            armC=dict(zip([a for a, _ in LABC], pc)), chain=dict(zip([a for a, _ in LABCH], pch)))
            P(f"      [{mode:12s}] sec 1.5: " + "  ".join(f"{a} {p:5.1%}" for (a, _), p in zip(LAB15, p15)))
            P(f"      [{mode:12s}] Arm C  : " + "  ".join(f"{a} {p:5.1%}" for (a, _), p in zip(LABC, pc)))
            P(f"      [{mode:12s}] chain  : " + "  ".join(f"{a} {p:5.1%}" for (a, _), p in zip(LABCH, pch)))
P("\n  row labels (frozen text, quoted): sec 1.5 " + "; ".join(f"{a}: {b}" for a, b in LAB15))
P("                                    Arm C   " + "; ".join(f"{a}: {b}" for a, b in LABC))
P("                                    chain   " + "; ".join(f"{a}: {b}" for a, b in LABCH))
check("C2 every landing distribution sums to 1 within 1e-12", f"{len(LAND) * 3} distributions", norm_ok)

# ------------------------------------------------------------------------------------------------ headline check
R.banner("HEADLINE CHECK (load-bearing; must FAIL under MUTATE)")
h = SEP[("canonical", "g_ext 1.778e-10 (primary)", "floor", "a")]
check("H P2-merge floor vs ownership (canonical, primary g_ext): S(30,000) > 0 and N(3 sigma) finite",
      f"S = {h['S30']:.3f}, N3 = {f(h['N3'])}", h["S30"] > 0 and h["N3"] != INF)
if MUT:
    same = all(abs(SEP[(ft, cs, an, "b")]["delta"] - SEP[(ft, "c")]["delta"]) < 1e-12 for (ft, cs, an, k) in
               [k for k in SEP if len(k) == 4 and k[3] == "b"])
    check("MUTATE: with merge = 1.000, every (b) row equals (c) (reported)", f"{same}", same, load_bearing=False)
R.num("separations", rows)
R.num("landing", {f"{k[0]} | {k[1]} | {k[2]}": v for k, v in LAND.items()})
R.num("sigma_tot_30k", s30)
nf = R.write(here=LANE)
sys.exit(1 if nf else 0)
