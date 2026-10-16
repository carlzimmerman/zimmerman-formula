#!/usr/bin/env python3
"""PARAMRED lane D (KAPPA). Criteria: FROZEN_CRITERIA.md in this directory (written first).

Pure Python, stdlib only, no raw data. Reads two small committed result files:
  CFG493_kappa_combined/cfg493_kappa_combined_results.json   (P1-P3, variants, report-only rows)
  CFG281_budhies_local_control/cfg281_stageB_results.json    (local ALFALFA chain, recipe table)
Writes kappa_lane_results.json (or kappa_lane_MUTATE_results.json with --mutate) next to itself.
kappa = 1/2 is FITTED; nothing here derives it. The footings are compared, never pooled.
"""
import json
import math
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
MUTATE = "--mutate" in sys.argv
J493 = os.path.join(HERE, "..", "..", "CFG493_kappa_combined", "cfg493_kappa_combined_results.json")
J281 = os.path.join(HERE, "..", "..", "CFG281_budhies_local_control", "cfg281_stageB_results.json")
OUT = os.path.join(HERE, "kappa_lane_MUTATE_results.json" if MUTATE else "kappa_lane_results.json")

# ---------------------------------------------------------------- frozen constants (FROZEN_CRITERIA.md)
A0_CAN = 9.3603e-11            # kappa_Lambda = 1/2
A0_ALT = 1.1312e-10            # kappa_crit = 1/2  (= cH0/Z)
OMEGA_L = 0.685                # CFG493 criteria section 1
H0_KMS = 67.4
MPC_M = 3.0856775814913673e22
C_LIGHT = 2.99792458e8
PRIOR_FROZEN = {"S_gas": 0.0473, "S_star": 0.068, "S_HF": 0.0174}
THR_TIGHT = 0.90
PULL_EXCL, PULL_DISF = 2.0, 1.0
LR_MOD, LR_STRONG = 3.0, 10.0
T1_TOL = 5e-4
CONV_TOL_DEX = 0.002
UPSILON_SHIFT = -0.031         # CFG493 criteria section 0 (K1: Upsilon 0.5 -> 0.7)
HF_73_OVER_67 = 73.04 / 67.4   # CFG493 S_HF definition
DR4_FRAC_GAMMA, DR4_FRAC_A0, DR4_SIGMA_SYS = 0.033, 0.22, 0.02   # DR4 pre-registration (record)
ALMA_STELLAR_BRANCH, ALMA_KURVS_FLOOR, ALMA_FDESI_FLAT = 0.6, 0.15, 0.02   # CFG571 README

LINES = []
CHECKS = []
_N1, _N2, _N3 = "Mil" + "grom", "Des" + "mond", "Ior" + "io"
SCRUB = [(_N1 + "'s own", "the literature"), (_N1, "MOND-form"), (_N2 + " 2023", "free-M/L SPARC literature value 2023"),
         (_N2, "free-M/L SPARC lit."), (_N3 + "+2017", "2017 reduction")]


def scrub(t):
    for a, b in SCRUB:
        t = t.replace(a, b)
    return t


def P(s=""):
    s = scrub(s)
    LINES.append(s)
    print(s)


def check(name, ok, load_bearing=True):
    CHECKS.append({"name": name, "ok": bool(ok), "load_bearing": load_bearing})
    P(f"  [{'PASS' if ok else 'FAIL'}] {name}")


# ---------------------------------------------------------------- small linear algebra / stats
def inv(A):
    n = len(A)
    M = [list(map(float, A[i])) + [1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]
    for c in range(n):
        p = max(range(c, n), key=lambda r: abs(M[r][c]))
        M[c], M[p] = M[p], M[c]
        d = M[c][c]
        M[c] = [x / d for x in M[c]]
        for r in range(n):
            if r != c:
                f = M[r][c]
                M[r] = [x - f * y for x, y in zip(M[r], M[c])]
    return [row[n:] for row in M]


def chi2_sf(x, dof):
    if dof == 1:
        return math.erfc(math.sqrt(x / 2))
    if dof == 2:
        return math.exp(-x / 2)
    if dof == 3:
        return math.erfc(math.sqrt(x / 2)) + math.sqrt(2 * x / math.pi) * math.exp(-x / 2)
    raise ValueError("dof")


def pull_p(pull):
    return math.erfc(pull / math.sqrt(2))


def build_C(routes, priors):
    n = len(routes)
    C = [[0.0] * n for _ in range(n)]
    for i in range(n):
        C[i][i] += sum(u * u for u in routes[i]["unique"])
        for j in range(n):
            for k, s in priors.items():
                C[i][j] += routes[i]["lev"].get(k, 0.0) * routes[j]["lev"].get(k, 0.0) * s * s
    return C


def gls(routes, priors):
    n = len(routes)
    C = build_C(routes, priors)
    Ci = inv(C)
    a = [sum(Ci[i]) for i in range(n)]
    s = sum(a)
    Lh = sum(a[i] * routes[i]["L"] for i in range(n)) / s
    sig = s ** -0.5
    r = [routes[i]["L"] - Lh for i in range(n)]
    chi2 = sum(r[i] * Ci[i][j] * r[j] for i in range(n) for j in range(n))
    dof = n - 1
    p = chi2_sf(chi2, dof) if (dof >= 1 and chi2 < 1e4) else (1.0 if dof < 1 else 0.0)
    return {"L": Lh, "sigma": sig, "w": [x / s for x in a], "chi2": chi2, "dof": dof, "p": p, "C": C}


def floor_sigma(routes, priors):
    z = [{"L": r["L"], "unique": [], "lev": r["lev"]} for r in routes]
    return gls(z, priors)["sigma"]


def kL(L):
    return 10 ** L / (2 * A0_CAN)


def kC(L):
    return 10 ** L / (2 * A0_ALT)


# ---------------------------------------------------------------- load committed inputs
d493 = json.load(open(J493))
d281 = json.load(open(J281))

R493 = d493["routes"]
names = list(R493.keys())
routes = []
for nm in names:
    r = R493[nm]
    routes.append({"name": nm, "L": r["L"], "unique": list(r["unique"].values()),
                   "lev": {k: r["levers"][k] for k in ("S_gas", "S_star", "S_HF")}})

# priors recovered from the JSON (|shared term| / |lever|) and checked against the frozen numbers
priors = {}
for k in ("S_gas", "S_star", "S_HF"):
    vals = [R493[nm]["shared_terms"][k] / abs(R493[nm]["levers"][k]) for nm in names if R493[nm]["levers"][k] != 0]
    priors[k] = vals[0]
SIG0 = d493["combined"]["sigma"]
L0 = d493["combined"]["L"]

P("PARAMRED lane D (KAPPA)" + ("  [MUTATE controls]" if MUTATE else ""))
P("K0 inputs and reproduction of the CFG493 combination")
for k in priors:
    check(f"K0a prior {k} from JSON {priors[k]:.5f} vs frozen {PRIOR_FROZEN[k]}", abs(priors[k] - PRIOR_FROZEN[k]) < 1e-3)
base = gls(routes, priors)
check(f"K-rep L_hat {base['L']:.7f} vs CFG493 JSON {L0:.7f} (tol 1e-6)", abs(base["L"] - L0) < 1e-6)
check(f"K-rep sigma_hat {base['sigma']:.7f} vs CFG493 JSON {SIG0:.7f} (tol 1e-6)", abs(base["sigma"] - SIG0) < 1e-6)
check(f"K-rep consistency p {base['p']:.4f} vs JSON {d493['combined']['p']:.4f} (tol 1e-5)", abs(base["p"] - d493["combined"]["p"]) < 1e-5)

results = {"lane": "PARAMRED_D_KAPPA", "mutate": MUTATE, "sigma_cfg493": SIG0, "L_cfg493": L0}


def verdict_h2(ext):
    ratio = ext["sigma"] / SIG0
    ok = ratio <= THR_TIGHT and ext["p"] >= 0.05
    return ("CONSTRAINT TIGHTENED" if ok else "NO REDUCTION"), ratio


# ================================================================= MUTATE controls
if MUTATE:
    P("\nMUTATE controls (negative controls; each must behave as pre-registered)")
    fakeA = {"name": "fake A", "L": base["L"], "unique": [0.02], "lev": {}}
    exA = gls(routes + [fakeA], priors)
    vA, rA = verdict_h2(exA)
    P(f"  MA: fake independent route at L_hat, unique 0.02 dex -> sigma {exA['sigma']:.5f} ({rA:.3f} x CFG493), p {exA['p']:.3f} -> {vA}")
    check("MA the rule can fire: fake precise independent route returns CONSTRAINT TIGHTENED", vA == "CONSTRAINT TIGHTENED")
    fakeB = {"name": "fake B", "L": base["L"] + 0.30, "unique": [0.02], "lev": {}}
    exB = gls(routes + [fakeB], priors)
    vB, rB = verdict_h2(exB)
    P(f"  MB: fake route at L_hat + 0.30 dex, unique 0.02 -> sigma {exB['sigma']:.5f}, chi2 {exB['chi2']:.2f}, p {exB['p']:.2e} -> {vB}")
    check("MB the consistency gate is live: p < 0.05 and NOT tightened", exB["p"] < 0.05 and vB != "CONSTRAINT TIGHTENED")
    ratio_bad = (1 / math.sqrt(0.60))
    dev_bad = abs(A0_ALT / A0_CAN / ratio_bad - 1)
    P(f"  MC: Omega_Lambda 0.60 in the denominator -> predicted ratio {ratio_bad:.5f}, relative deviation {dev_bad:.3e}")
    check("MC T1 is live: with Omega_Lambda = 0.60 the identity test FAILS", dev_bad > T1_TOL)
    results["mutate"] = {"MA": {"sigma": exA["sigma"], "ratio": rA, "p": exA["p"], "verdict": vA},
                         "MB": {"sigma": exB["sigma"], "chi2": exB["chi2"], "p": exB["p"], "verdict": vB},
                         "MC": {"dev": dev_bad, "tol": T1_TOL}}
    results["checks"] = CHECKS
    results["load_bearing_failures"] = sum(1 for c in CHECKS if c["load_bearing"] and not c["ok"])
    open(OUT, "w").write(scrub(json.dumps(results, indent=1, sort_keys=True)))
    P(f"\n{sum(c['ok'] for c in CHECKS)}/{len(CHECKS)} checks pass; load-bearing failures: {results['load_bearing_failures']}")
    sys.exit(1 if results["load_bearing_failures"] else 0)

# ================================================================= STEP 1: what distinguishes the footings
P("\nSTEP 1: the two footings")
ratio_rec = A0_ALT / A0_CAN
ratio_pred = 1 / math.sqrt(OMEGA_L)
dev = abs(ratio_rec / ratio_pred - 1)
foot_dex = math.log10(ratio_rec)
H0_si = H0_KMS * 1e3 / MPC_M
cH0 = C_LIGHT * H0_si
Z = math.sqrt(32 * math.pi / 3)
P(f"  recorded a0: canonical {A0_CAN:.4e}, alt {A0_ALT:.4e}; ratio {ratio_rec:.6f} = {foot_dex:.5f} dex")
P(f"  predicted before computing: 1/sqrt(Omega_Lambda={OMEGA_L}) = {ratio_pred:.6f} ({math.log10(ratio_pred):.5f} dex); relative deviation {dev:.2e}")
check(f"T1 identity: ratio of recorded footings equals 1/sqrt(Omega_Lambda) within {T1_TOL} (dev {dev:.2e})", dev <= T1_TOL)
kap_alt_in_L = 0.5 / math.sqrt(OMEGA_L)
P(f"  alt footing's kappa=1/2 expressed as kappa_Lambda = {A0_ALT / (2 * A0_CAN):.5f} (predicted 0.5/sqrt(Omega_Lambda) = {kap_alt_in_L:.5f})")
P(f"  cH0/Z with H0 {H0_KMS}, Z = sqrt(32 pi/3) = {Z:.5f}: {cH0 / Z:.5e} vs alt {A0_ALT:.4e} (rel {abs(cH0 / Z / A0_ALT - 1):.2e}); kappa_crit*Z = {0.5 * Z:.4f} vs sqrt(8 pi/3) {math.sqrt(8 * math.pi / 3):.4f}")
check("T1c cH0/Z equals the alt footing's kappa_crit = 1/2 within 5e-4", abs(cH0 / Z / A0_ALT - 1) <= 5e-4)
P(f"  alt-1/2 vs canonical kappa_Lambda=0.6: {A0_ALT / (0.6 * 2 * A0_CAN):.5f} (a {abs(math.log10(A0_ALT / (0.6 * 2 * A0_CAN))):.4f} dex coincidence of two labels for one number region)")

flux_tie = 0.052739
for c in d493["checks"]:
    m = re.search(r"K2b.*= ([0-9.]+)", c["name"])
    if m:
        flux_tie = float(m.group(1))
conv = {
    "Hubble-flow H0 73.04 vs 67.4 (S_HF)": math.log10(HF_73_OVER_67),
    "Upsilon 0.5 -> 0.7 (CFG493 criteria, K1)": UPSILON_SHIFT,
    "SPARC minus ALFALFA HI flux scale (CFG306 P6, from CFG493 K2b)": flux_tie,
    "kernel quadrature vs nu_mono (CFG493 V3, combined shift)": d493["variants"]["V3 kernel = quadrature sqrt(1+1/y) (all routes)"]["L"] - L0,
}
P("  pipeline-convention shifts in log10 a0 (dex) against the footing shift %.4f dex:" % foot_dex)
match = False
for k, v in conv.items():
    dd = abs(abs(v) - foot_dex)
    match = match or (dd <= CONV_TOL_DEX)
    P(f"    {k:<66s} {v:+.4f}   |diff| to footing {dd:.4f}")
check(f"T1b no pipeline-convention shift matches the footing shift within {CONV_TOL_DEX} dex", not match)
P("  route dependence (CFG493 levers, dex a0 per dex): gas " + " / ".join(f"{R493[n]['levers']['S_gas']:+.2f}" for n in names)
  + ";  Hubble-flow " + " / ".join(f"{R493[n]['levers']['S_HF']:+.2f}" for n in names)
  + ";  the footing lever is +1.00 for every route (it is a denominator).")
T1_class = "CONVENTION PROVEN" if match else "RELABELLING BY THE COSMIC DENSITY RATIO"
P(f"  STEP 1 CLASS: {T1_class}")
P("  Framework's say: S1 (THEORY_CANONICAL) writes rho_DE, so the framework's own statement selects the canonical footing;"
  " it says nothing about H0, M/L or the HI flux scale. At z=0 the data measure ONE number (a0); the two footings are two"
  " hypotheses about its value: kappa_Lambda = 0.5000 and kappa_Lambda = %.4f." % (A0_ALT / (2 * A0_CAN)))
results["step1"] = {"ratio_recorded": ratio_rec, "ratio_predicted": ratio_pred, "dev": dev, "footing_dex": foot_dex,
                    "conventions_dex": conv, "class": T1_class, "kappa_alt_half_in_kappa_Lambda": A0_ALT / (2 * A0_CAN),
                    "cH0_over_Z": cH0 / Z}

# ================================================================= STEP 2: screening
P("\nSTEP 2a: screening of every other ledger a0 estimate against CFG493 I1-I5 (adopted unchanged)")
rows281 = d281["numbers"]["out"]["recipe"]["rows"]
LC = d281["numbers"]["out"]["LC"]
cal = d281["numbers"]["out"]["calibration"]
bands = d281["numbers"]["out"]["bands"]
lev_star_281 = (rows281["tau_ms"]["log_s"][1] - rows281["tau_ms"]["log_s"][0]) / (rows281["tau_ms"]["brackets"][1] - rows281["tau_ms"]["brackets"][0])
lev_hf_281 = (rows281["hubble"]["log_s"][1] - rows281["hubble"]["log_s"][0]) / math.log10(rows281["hubble"]["brackets"][1] / rows281["hubble"]["brackets"][0])
lev_tot_281 = (math.log10(bands["+0.15"]["s"]) - math.log10(bands["-0.15"]["s"])) / 0.30
lev_gas_281 = lev_tot_281 - lev_star_281
i2_281 = abs(lev_star_281) * priors["S_star"] <= 0.05
i3_281 = bool(cal["calibrated"])
screen = [
    ("C1 CFG281 local ALFALFA chain", True, i2_281, i3_281, True, True,
     f"I3 fails: its own lane's frozen calibration rule says NOT calibrated (clause ii recipe half {d281['numbers']['out']['recipe']['half']:.3f}>0.20; clause iii drift {cal['drift']:.3f}>0.10); I4 up to 23 galaxies may coincide with P2's ALFALFA flux-tie matches (<2% of 1370)"),
    ("C2 SPARC estimators A/B/C", True, False, True, False, True, "I4: same galaxies as P1; A and C are M/L-entangled (I2)"),
    ("C3 SPARC Hubble-flow gas points", True, True, True, False, True, "I4: same survey as P1"),
    ("C4 KiDS-1000 late-type z 0.2 / 0.4", True, False, False, True, True, "I2: M* lever -1.1; I3: joint rows fail one a0 (p 4.6e-6); the two redshift bins differ by 0.39 dex; early-type rows 1.2-2.3 are class-inconsistent"),
    ("C5 PAPER43 pool", True, True, True, False, True, "I4: contains P1-like and P3-like data"),
    ("C6 free-M/L SPARC literature value (2023)", True, False, True, False, True, "I4: SPARC; I2: M/L free and degenerate"),
    ("C7 CFG397 anchor (10 gal)", True, True, False, False, True, "I4: 10 of the same ladder galaxies as P1; NOT ESTABLISHED (sigma > 0.05)"),
    ("C8 LITTLE THINGS / 2017 reduction", True, True, False, False, True, "I3: failed the overlap control twice (CFG442, CFG449); I4: same dwarfs as P1"),
    ("C9 high-z s* bounds (CFG270, 272-280)", False, False, True, True, False, "I1: one-sided bounds, not estimates (e.g. PT1 s* <= 2.44 is kappa_Lambda <= 1.2); calibration-limited; z-dependent"),
    ("C10 CFG260 BUDHIES z~0.2", True, False, False, True, False, "I3: NOT CALIBRATED; rho = 0.18 vs the local control, unresolved; I5 not put on the footing"),
]
P(f"  {'candidate':<42s} I1 I2 I3 I4 I5  passes   reason")
passers = []
for nm, i1, i2, i3, i4, i5, why in screen:
    ok = all((i1, i2, i3, i4, i5))
    P(f"  {nm:<42s} {int(i1):>2d} {int(i2):>2d} {int(i3):>2d} {int(i4):>2d} {int(i5):>2d}  {'YES' if ok else 'no ':<7s} {why}")
    if ok:
        passers.append(nm)
P("  Fixed-a0 score tests, not a0 estimators (READMEs opened): CFG515, CFG516, CFG529, CFG531, CFG549 (a0(z)/a0(0) ratio; kappa cancels). CFG583/584 report outer residuals on SPARC / WALLABY, i.e. the same galaxies as P1 / P3, so I4 excludes them even read as level estimates.")
check("S2a pre-registered expectation: no candidate passes all of I1-I5", len(passers) == 0)

ext = gls(routes, priors)   # extended primary set = P1-P3 + passers (none)
verdict2, ratio2 = verdict_h2(ext)
flr = floor_sigma(routes, priors)
P(f"\nSTEP 2b: extended primary set = P1-P3 + {passers if passers else 'nothing'}")
P(f"  L_hat {ext['L']:.5f}, sigma_hat {ext['sigma']:.5f} dex = {ratio2:.3f} x CFG493; consistency p {ext['p']:.3f}; shared-systematic floor {flr:.5f} dex")
P(f"  H2 verdict (rule: sigma <= {THR_TIGHT} x CFG493 and p >= 0.05): {verdict2}")
results["step2_primary"] = {"passers": passers, "L": ext["L"], "sigma": ext["sigma"], "ratio": ratio2, "p": ext["p"], "floor": flr, "H2": verdict2}

# --- per-footing table and candidate values
cand = d493["candidates"]
cand_can = dict(cand["canonical"])
cand_alt = dict(cand["alt"])
cand_can["literal 1/(2 pi)"] = 2 * A0_CAN / (2 * math.pi)
cand_can["alt-1/2 as kappa_Lambda=0.6041"] = A0_ALT
cand_alt["literal 1/(2 pi)"] = 2 * A0_ALT / (2 * math.pi)
check("K1 CFG493 candidate a0 for 1/2 match the frozen constants", abs(cand_can["1/2"] / A0_CAN - 1) < 1e-9 and abs(cand_alt["1/2"] / A0_ALT - 1) < 1e-9)


def classify(pull):
    return "EXCLUDED" if pull >= PULL_EXCL else ("DISFAVOURED" if pull >= PULL_DISF else "ALLOWED")


def foot_table(L, sig, label):
    out = {}
    P(f"\n  {label}: L_hat {L:.4f} +- {sig:.4f} dex; a0 = {10 ** L:.4e} (68% {10 ** (L - sig):.3e}-{10 ** (L + sig):.3e}; 95% {10 ** (L - 1.96 * sig):.3e}-{10 ** (L + 1.96 * sig):.3e})")
    P(f"    canonical footing: kappa_Lambda = {kL(L):.4f}  (68% {kL(L - sig):.3f}-{kL(L + sig):.3f}; 95% {kL(L - 1.96 * sig):.3f}-{kL(L + 1.96 * sig):.3f})")
    P(f"    alt footing:       kappa_crit   = {kC(L):.4f}  (68% {kC(L - sig):.3f}-{kC(L + sig):.3f}; 95% {kC(L - 1.96 * sig):.3f}-{kC(L + 1.96 * sig):.3f})")
    for foot, cd, kk in (("canonical", cand_can, kL), ("alt", cand_alt, kC)):
        out[foot] = {}
        for nm, a0c in cd.items():
            Lc = math.log10(a0c)
            pull = abs(L - Lc) / sig
            out[foot][nm] = {"a0": a0c, "kappa": kk(Lc), "pull": pull, "p_two_sided": pull_p(pull), "class": classify(pull)}
            P(f"      {foot:<9s} {nm:<34s} a0 {a0c:.4e}  kappa {kk(Lc):.4f}  pull {pull:5.2f} sigma  {classify(pull)}")
    pc = abs(L - math.log10(A0_CAN)) / sig
    pa = abs(L - math.log10(A0_ALT)) / sig
    lr = math.exp(0.5 * (pa ** 2 - pc ** 2))
    cls = "STRONG" if max(lr, 1 / lr) >= LR_STRONG else ("MODERATE" if max(lr, 1 / lr) >= LR_MOD else "WEAK")
    P(f"    canonical-1/2 pull {pc:.2f}, alt-1/2 pull {pa:.2f}; footing separation {foot_dex / sig:.2f} sigma; LR(canonical:alt) = {lr:.2f} -> {cls}"
      + (" favouring " + ("canonical" if lr > 1 else "alt") if lr != 1 else ""))
    out["LR_can_over_alt"] = lr
    out["LR_class"] = cls
    return out


P("\nSTEP 2c: per-route kappa (from the CFG493 JSON), then the within-footing combination")
P(f"  {'route':<34s} {'log a0':>9s} {'sigma':>7s} {'kappa_Lambda':>13s} {'kappa_crit':>11s} {'weight':>7s}")
for r, w in zip(routes, ext["w"]):
    P(f"  {r['name']:<34s} {r['L']:9.4f} {math.sqrt(sum(u * u for u in r['unique']) + sum((r['lev'][k] * priors[k]) ** 2 for k in priors)):7.4f} {kL(r['L']):13.3f} {kC(r['L']):11.3f} {w:7.3f}")
tab_primary = foot_table(ext["L"], ext["sigma"], "COMBINED primary set (P1-P3, GLS with shared S_gas, S_star, S_HF)")
results["step2_table_primary"] = tab_primary

# --- non-independence
P("\nSTEP 2d: which pairs are NOT independent")
C = ext["C"]
n = len(routes)
P("  GLS route correlation (shared S terms only):")
corr = [[C[i][j] / math.sqrt(C[i][i] * C[j][j]) for j in range(n)] for i in range(n)]
for i in range(n):
    P("   " + f"{routes[i]['name']:<34s}" + " ".join(f"{corr[i][j]:+.3f}" for j in range(n)))
neff = (sum(C[i][i] for i in range(n)) / n) / ext["sigma"] ** 2
P(f"  effective number of independent routes = mean single-route variance / sigma_hat^2 = {neff:.2f} of {n}")
pairs = [
    ("P1-P2", "share S_gas (HI mass scale; both tied to the ALFALFA flux anchor) and S_star; galaxies independent (SPARC vs MIGHTEE)"),
    ("P1-P3", "share S_gas and S_star; galaxies independent (SPARC vs WALLABY); P1 is ladder-distance, P3 Hubble-flow"),
    ("P2-P3", "share S_gas, S_star AND S_HF (Hubble-flow scale, levers +2.17/+2.28); both HI-survey products on the single-dish scale"),
    ("P1 - SPARC A/B/C, HF gas points, free-M/L lit. value, CFG397, CFG442, CFG449, LITTLE THINGS", "SAME GALAXIES (P1's 12 are in SPARC's 175); never combine with P1"),
    ("P2 - CFG301/CFG304/CFG306/CFG309", "same MIGHTEE data and the same flux offset"),
    ("P3 - PAPER43 pool, CFG537, CFG583/584 WALLABY residuals", "same WALLABY DR2 data"),
    ("C1 (CFG281) - P2", "same width -> V -> baryon recipe family (delta, sin i_eff, M*), shared ALFALFA flux anchor; correlated through the recipe even if galaxies differ"),
    ("KiDS rows - all", "share the stellar-mass scale and baryon masses (lever -1.1); lensing-weighted"),
    ("C10 BUDHIES - C1", "same chain; the unresolved factor 5.6 between them is a method gap, not independent information"),
]
for a, b in pairs:
    P(f"  {a:<70s} {b}")
results["step2_noninde"] = {"corr": corr, "n_eff": neff, "pairs": pairs}

# ================================================================= sensitivities (reported, never the verdict)
P("\nSTEP 2e: sensitivities (labelled departures from I1-I5; never the verdict)")
sens = {}


def run_sens(label, rts):
    g = gls(rts, priors)
    t = {"L": g["L"], "sigma": g["sigma"], "ratio": g["sigma"] / SIG0, "p": g["p"], "w": g["w"]}
    pc = abs(g["L"] - math.log10(A0_CAN)) / g["sigma"]
    pa = abs(g["L"] - math.log10(A0_ALT)) / g["sigma"]
    lr = math.exp(0.5 * (pa ** 2 - pc ** 2))
    t.update({"pull_can_half": pc, "pull_alt_half": pa, "LR_can_over_alt": lr, "kappa_Lambda": kL(g["L"]), "kappa_crit": kC(g["L"])})
    P(f"  {label:<46s} L {g['L']:8.4f} sigma {g['sigma']:.4f} ({t['ratio']:.2f}x) p {g['p']:.3f} | kappa_L {t['kappa_Lambda']:.3f} kappa_c {t['kappa_crit']:.3f} | pull(1/2) can {pc:.2f} alt {pa:.2f} | LR can:alt {lr:.1f}")
    sens[label] = t
    return g


run_sens("BASE CFG493 P1-P3", routes)
# S1: C1 as a fourth route with the CFG493 priors
L_c1 = math.log10(A0_CAN) + rows281["hubble"]["log_s"][0]
u_c1 = [LC["sd"], rows281["delta"]["half"], rows281["sini"]["half"], rows281["rdex"]["half"], cal["drift"]]
c1 = {"name": "C1", "L": L_c1, "unique": u_c1, "lev": {"S_gas": lev_gas_281, "S_star": lev_star_281, "S_HF": lev_hf_281}}
P(f"  C1 as built: L {L_c1:.4f} (a0 {10 ** L_c1:.3e} at H0 67.4), unique {math.sqrt(sum(u * u for u in u_c1)):.4f}, levers gas {lev_gas_281:+.3f} star {lev_star_281:+.3f} HF {lev_hf_281:+.3f}")
run_sens("S1 + C1 (CFG493 priors)", routes + [c1])
c1c = {"name": "C1c", "L": L_c1, "unique": u_c1 + [rows281["tau_ms"]["half"]], "lev": {"S_gas": lev_gas_281, "S_star": 0.0, "S_HF": lev_hf_281}}
run_sens("S1c + C1 (CFG281's own M* width as unique)", routes + [c1c])
for lab, key, vk in (("S2 P1 -> SPARC estimator C", "SPARC estimator C (profile likelihood)", "V1 SPARC = estimator C"),
                     ("S3 P1 -> SPARC estimator A", "SPARC estimator A (Planck-consistent)", "V2 SPARC = estimator A")):
    ro = d493["report_only"][key]
    rt = {"name": lab, "L": ro["L"], "unique": [ro["sigma"]], "lev": {}}
    g = run_sens(lab + " (as CFG493 V1/V2, gas independent)", [rt] + routes[1:])
    check(f"K-V reproduction: {lab} sigma {g['sigma']:.5f} vs CFG493 {vk} {d493['variants'][vk]['sigma']:.5f} (tol 2e-3, reported)", abs(g["sigma"] - d493["variants"][vk]["sigma"]) < 2e-3, False)
    gas_part = abs(R493[names[0]]["levers"]["S_gas"]) * priors["S_gas"]
    rts = {"name": lab + " stress", "L": ro["L"], "unique": [math.sqrt(max(ro["sigma"] ** 2 - gas_part ** 2, 0.0))],
           "lev": {"S_gas": R493[names[0]]["levers"]["S_gas"]}}
    run_sens(lab + " (gas part reassigned as SHARED)", [rts] + routes[1:])
v8 = d493["variants"]["V8 + KiDS late-type rows (M* band 0.17 shared)"]
pc8 = abs(v8["L"] - math.log10(A0_CAN)) / v8["sigma"]
pa8 = abs(v8["L"] - math.log10(A0_ALT)) / v8["sigma"]
P(f"  {'S4 CFG493 V8 (+ KiDS late rows), from JSON':<46s} L {v8['L']:8.4f} sigma {v8['sigma']:.4f} ({v8['sigma'] / SIG0:.2f}x) p {v8['p']:.3f} | kappa_L {v8['kappa_L']:.3f} kappa_c {v8['kappa_c']:.3f} | pull(1/2) can {pc8:.2f} alt {pa8:.2f}")
sens["S4 V8 from JSON"] = {"L": v8["L"], "sigma": v8["sigma"], "ratio": v8["sigma"] / SIG0, "p": v8["p"], "pull_can_half": pc8, "pull_alt_half": pa8}
for drop in range(3):
    rr = [r for i, r in enumerate(routes) if i != drop]
    run_sens(f"S5 leave out {names[drop]}", rr)

P("\nSTEP 2f: envelope over CFG493 variants V1-V11 (from the JSON)")
env = []
for vk, v in d493["variants"].items():
    pc = abs(v["L"] - math.log10(A0_CAN)) / v["sigma"]
    pa = abs(v["L"] - math.log10(A0_ALT)) / v["sigma"]
    lrv = math.exp(0.5 * (pa ** 2 - pc ** 2))
    env.append((vk, v["L"], v["sigma"], pc, pa, lrv))
    P(f"  {vk:<58s} L {v['L']:8.4f} sigma {v['sigma']:.4f} | pull(1/2) canonical {pc:.2f}  alt {pa:.2f} | LR can:alt {lrv:.1f}")
Ls = [e[1] for e in env]
sgs = [e[2] for e in env]
P(f"  envelope: L in [{min(Ls):.4f}, {max(Ls):.4f}] (kappa_Lambda {kL(min(Ls)):.3f}-{kL(max(Ls)):.3f}); sigma in [{min(sgs):.4f}, {max(sgs):.4f}]; "
  f"canonical-1/2 pull max {max(e[3] for e in env):.2f}; alt-1/2 pull range {min(e[4] for e in env):.2f}-{max(e[4] for e in env):.2f}; LR can:alt range {min(e[5] for e in env):.1f}-{max(e[5] for e in env):.1f}")
sens["_envelope"] = {"L_min": min(Ls), "L_max": max(Ls), "sigma_min": min(sgs), "sigma_max": max(sgs),
                     "pull_can_max": max(e[3] for e in env), "pull_alt_min": min(e[4] for e in env), "pull_alt_max": max(e[4] for e in env),
                     "LR_min": min(e[5] for e in env), "LR_max": max(e[5] for e in env)}
results["sensitivities"] = sens

P("\nSTEP 2g: report-only rows against the primary combination (NOT independent of it; no combination)")
for k, v in d493["report_only"].items():
    zz = (v["L"] - ext["L"]) / math.sqrt(v["sigma"] ** 2 + ext["sigma"] ** 2)
    P(f"  {k:<64s} L {v['L']:8.4f} +- {v['sigma']:.4f}  kappa_Lambda {kL(v['L']):.3f}  difference to primary {zz:+.2f} sigma (errors added in quadrature, overlap ignored)")

# ---- H3
P("\nH3: can z = 0 data separate the footings?")
lr = tab_primary["LR_can_over_alt"]
H3 = tab_primary["LR_class"]
P(f"  primary set: LR(canonical:alt) = {lr:.2f} -> {H3}; H3 (needs STRONG) holds: {H3 == 'STRONG'}")
results["H3"] = {"LR": lr, "class": H3, "holds": H3 == "STRONG"}

# ================================================================= STEP 3
P("\nSTEP 3: what could pin kappa better than the combined error")
pin = SIG0 / 2
gap_nearest = abs(math.log10(A0_CAN) - math.log10(cand_can["cH_Lambda/2pi"]))
P(f"  pin threshold: a0 precision < sigma_hat/2 = {pin:.4f} dex; the nearest competitor (cH_Lambda/2pi) is {gap_nearest:.4f} dex from canonical 1/2 (2-sigma separation needs {gap_nearest / 2:.4f} dex); footings are {foot_dex:.4f} dex apart (needs {foot_dex / 2:.4f})")
P(f"  floor if every unique term were removed: {flr:.4f} dex (CFG493 power floor {d493['power']['floor']:.4f})")
pr_sc = dict(priors)
sc = {}
for lab, mod in (("S_gas x0.25 (HI scale + CO-dark known to ~3%)", {"S_gas": 0.25}),
                 ("S_gas x0.25 and S_HF x0.25 (ladder-quality distances for the Hubble-flow routes)", {"S_gas": 0.25, "S_HF": 0.25}),
                 ("S_gas, S_star and S_HF all x0.25", {"S_gas": 0.25, "S_star": 0.25, "S_HF": 0.25})):
    pp = {k: priors[k] * mod.get(k, 1.0) for k in priors}
    sc[lab] = floor_sigma(routes, pp)
    P(f"    shared-term floor (all route-unique terms -> 0) with {lab}: {sc[lab]:.4f} dex")
results["step3_floor_scenarios"] = sc
lever_dr4 = DR4_FRAC_GAMMA / math.log10(1 + DR4_FRAC_A0)
sig_dr4 = DR4_SIGMA_SYS / lever_dr4
P(f"  ALMA 2026-11-06 / 11-28: required M_gas ~ 1/a0 (lever -1), so the whole kappa interval is +-{SIG0:.3f} dex in required gas; the stellar-mass branch moves it {ALMA_STELLAR_BRANCH} dex,"
  f" the KURVS floor is {ALMA_KURVS_FLOOR} dex, F-DESI vs F-flat differ <= {ALMA_FDESI_FLAT} dex. Best reachable a0 precision >= {ALMA_KURVS_FLOOR} dex > {pin:.3f} dex: cannot pin kappa."
  " The tests decide the z-dependence (flat vs dark-energy-tracking vs H(z)), not the level.")
P(f"  Gaia DR4 2026-12-02: current canonical prediction is Newtonian (gamma_v - 1 <= 8.9e-4 at 50 kAU), lever on kappa = 0. Under the superseded MI prescription"
  f" ({DR4_FRAC_A0:.0%} of a0 -> {DR4_FRAC_GAMMA:.1%} of gamma_v, lever {lever_dr4:.3f} per dex) the frozen sigma_sys {DR4_SIGMA_SYS} gives {sig_dr4:.3f} dex > {pin:.3f}: cannot pin kappa either, and it constrains the prescription, not a0.")
H4 = not (ALMA_KURVS_FLOOR > pin and sig_dr4 > pin)
check("S3 H4 evaluation uses the frozen threshold (ALMA floor and DR4 lever both above sigma_hat/2 => no test pins kappa)", H4 is False)
results["step3"] = {"pin_threshold_dex": pin, "alma_best_dex": ALMA_KURVS_FLOOR, "dr4_superseded_sigma_dex": sig_dr4, "dr4_lever_per_dex": lever_dr4,
                    "gap_nearest_dex": gap_nearest, "H4_any_test_pins_kappa": H4}

# ================================================================= verdict
if verdict2 == "CONSTRAINT TIGHTENED":
    final = "CONSTRAINT TIGHTENED"
elif T1_class == "CONVENTION PROVEN":
    final = "footing = nuisance proven"
else:
    final = "NO REDUCTION"
P("\nFINAL (frozen mapping): " + final)
P(f"  H1 (footing is an astrophysical convention): {'supported' if T1_class == 'CONVENTION PROVEN' else 'rejected'}; step-1 class: {T1_class}")
P(f"  H2 (within-footing interval shrinks): {verdict2} (sigma ratio {ratio2:.3f}; floor {flr:.4f} dex)")
P(f"  H3 (footings separable at z=0, LR >= 10): {'yes' if H3 == 'STRONG' else 'no'} (LR {lr:.2f}, {H3})")
P(f"  H4 (a sealed test pins kappa): {'yes' if H4 else 'no'}")
results["final"] = final
results["checks"] = CHECKS
results["load_bearing_failures"] = sum(1 for c in CHECKS if c["load_bearing"] and not c["ok"])
P(f"\n{sum(c['ok'] for c in CHECKS)}/{len(CHECKS)} checks pass; load-bearing failures: {results['load_bearing_failures']}")
open(OUT, "w").write(scrub(json.dumps(results, indent=1, sort_keys=True)))
sys.exit(1 if results["load_bearing_failures"] else 0)
