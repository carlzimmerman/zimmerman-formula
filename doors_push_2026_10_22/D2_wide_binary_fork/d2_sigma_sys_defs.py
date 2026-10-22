"""D2 sigma_sys definitions (owner: "we need to try all of them"), pre-data, DR3 dry run NON-SCORING.

Every candidate sigma_sys definition is evaluated on the DR3 frozen-cut catalogue on disk. For each
one we give the separation of the screened reading (gamma_v - 1 = 8.1e-6, D7d) from AQUAL law-first
(E2: 1.167/1.199 primary g_ext, 1.145/1.173 alt g_ext; canonical/alt), and the pairs needed for 3 sigma.
Canonical and alt footings are never pooled.

The frozen pipeline is IMPORTED READ-ONLY (its functions only; its main() is not run, nothing is
written into prep_2026). A socket guard forbids any network access.

Run: OMP_NUM_THREADS=1 nice -n 10 python3 d2_sigma_sys_defs.py [--mutate]
MUTATE: the baseline catalogue's deep-pair (y < 1) v_perp is scaled by 1.20 -> check S1 (record gamma-hat) must FAIL.
"""
import csv
import json
import math
import os
import socket
import sys

import numpy as np

sys.dont_write_bytecode = True


def _no_net(*a, **k):
    raise RuntimeError("network access forbidden in this lane")


socket.socket.connect = _no_net
socket.create_connection = _no_net

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "prep_2026/gaia_dr4_prep"))
import wide_binary_pipeline as wbp  # noqa: E402  (read-only import)

MUT = "--mutate" in sys.argv
TAG = "_MUTATE" if MUT else ""
OUT = os.path.join(HERE, "d2_sigma_sys_defs%s.out" % TAG)
JS = os.path.join(HERE, "d2_sigma_sys_defs_results%s.json" % TAG)
LINES, CHECKS = [], []


def P(s=""):
    print(s, flush=True)
    LINES.append(s)


def ck(cid, ok, value, thr, note=""):
    CHECKS.append(dict(id=cid, passed=bool(ok), value=value, threshold=thr, note=note))
    P("%s %s %s %s   %s" % (cid, "PASS" if ok else "FAIL", value, thr, note))


DR3 = "real_research/data/widebinaries/dr3_extract/"
CATS = {
    "V0 baseline (frozen-cut build)": DR3 + "wide_binaries_dr3.csv",
    "V4 build: El-Badry R": DR3 + "wide_binaries_dr3_elbadryR.csv",
    "V5 build: scaled_clean": DR3 + "wide_binaries_dr3_scaled_clean.csv",
    "NSSOFF source (CFG816 variant)": "campaign_fresh_gravity/CFG816_dr4_r_statistic_scoring/wide_binaries_dr3_variant.csv",
}


def load(path, vscale=1.0):
    return list(csv.DictReader(open(os.path.join(ROOT, path)))), vscale


def arrays(rows, vscale=1.0):
    s = np.array([float(r["sep_kAU"]) for r in rows]) * wbp.KAU
    vp = np.array([float(r["v_perp_kms"]) for r in rows]) * 1e3 * vscale
    Mt = np.array([float(r["M1_msun"]) + float(r["M2_msun"]) for r in rows])
    gN = wbp.G * Mt * wbp.MSUN / s ** 2
    vt = vp / np.sqrt(wbp.G * Mt * wbp.MSUN / s)
    if vscale != 1.0:                       # MUTATE: boost only the deep pairs (kappa absorbs a uniform scale)
        vt = np.where(gN / wbp.A0_CAN < 1.0, vt * vscale, vt)
    return gN, vt


P("=" * 100)
P("D2 sigma_sys definitions on the DR3 dry run (NON-SCORING)   mutation: %s" % ("deep-pair v_perp x1.20" if MUT else "none"))
P("=" * 100)
rng = np.random.default_rng(20261216)
NM = 1_000_000
pop_m = wbp.make_population(NM, rng, dr4=True)        # as the frozen --catalog path (DR4-noise model)
MOD = {"canonical": wbp.model_medians(pop_m, wbp.A0_CAN, wbp.GRID, rng),
       "alt": wbp.model_medians(pop_m, wbp.A0_ALT, wbp.GRID, rng)}
A0 = {"canonical": wbp.A0_CAN, "alt": wbp.A0_ALT}
P("master MC after selection: %d (frozen code: 3,000,000 oversampled; smaller here, declared)" % len(pop_m["s_obs"]))

base_rows, _ = load(CATS["V0 baseline (frozen-cut build)"])
var_rows = {
    "V0 baseline (frozen-cut build)": base_rows,
    "V1 ladder: R_chance < 0.001": [r for r in base_rows if float(r["R_chance"]) < 0.001],
    "V2 ladder: sep 3-20 kAU": [r for r in base_rows if 3.0 <= float(r["sep_kAU"]) < 20.0],
    "V3 NSS-off probe (s < 30 kAU)": [r for r in load(CATS["NSSOFF source (CFG816 variant)"])[0]
                                      if float(r["sep_kAU"]) < 30.0],
    "V4 build: El-Badry R": load(CATS["V4 build: El-Badry R"])[0],
    "V5 build: scaled_clean": load(CATS["V5 build: scaled_clean"])[0],
}
P("unimplementable on DR3 (declared, not substituted): ladder RUWE 1.4->1.2 (no RUWE column), RV-screened subsample")

FIT = {}
for fo in ("canonical", "alt"):
    for name, rows in var_rows.items():
        vs = 1.20 if (MUT and name.startswith("V0")) else 1.0
        gN, vt = arrays(rows, vs)
        med, sig, cnt = wbp.bin_medians(np.log10(gN / A0[fo]), vt, boot=200, rng=rng)
        g, sg, chi2, nb, kap = wbp.fit_gamma(med, sig, MOD[fo], wbp.GRID)
        FIT["%s|%s" % (fo, name)] = dict(N=len(rows), gamma=float(g), sigma_fit=float(sg), kappa=float(kap))
        P("  %-9s %-34s N=%5d  gamma-hat %.4f +- %.4f  kappa %.4f" % (fo, name, len(rows), g, sg, kap))

g0c = FIT["canonical|V0 baseline (frozen-cut build)"]["gamma"]
ck("S1", abs(g0c - 1.0750) <= 0.03, "%.4f" % g0c, "|g-1.0750|<=0.03",
   "baseline reproduces the record's DR3 dry run (DRY_RUN_2026-10-09.md; estimator jitter ~0.02)")
ck("S2", len(base_rows) == 6210, "%d" % len(base_rows), "6210", "frozen-cut DR3 catalogue")
ck("S3", all(FIT["canonical|%s" % k]["N"] >= 1000 for k in var_rows), "min N %d" % min(v["N"] for v in FIT.values()),
   ">=1000", "every variant has enough pairs for the 8-bin estimator")

# ------------------------------------------------------------------ definitions
LADDER = ["V1 ladder: R_chance < 0.001", "V2 ladder: sep 3-20 kAU", "V3 NSS-off probe (s < 30 kAU)"]
PRED = {"canonical": {"primary": 1.1666821011084045, "alt_gext": 1.1447841306286448},
        "alt": {"primary": 1.1985790300437524, "alt_gext": 1.173011927619301}}   # E2 R2 gamma_AQUAL_anch
SCREENED = 1.0 + 8.1e-6                                                          # D7d, L* = 24 pc
SFIT30 = {"mock": 0.019, "DR3-cal": None}


def defs_for(fo):
    base = FIT["%s|V0 baseline (frozen-cut build)" % fo]["gamma"]
    sf_base = FIT["%s|V0 baseline (frozen-cut build)" % fo]["sigma_fit"]
    shifts = [FIT["%s|%s" % (fo, k)]["gamma"] - base for k in LADDER]
    gl = [base] + [FIT["%s|%s" % (fo, k)]["gamma"] for k in LADDER]
    spread = max(gl) - min(gl)
    n = len(gl)
    loo = [np.mean([x for j, x in enumerate(gl) if j != i]) for i in range(n)]
    jk = math.sqrt((n - 1) / n * sum((x - np.mean(loo)) ** 2 for x in loo))
    nss = abs(FIT["%s|V3 NSS-off probe (s < 30 kAU)" % fo]["gamma"] - base)
    sbuild = 0.44 * 0.019                                   # Amdt 18: sigma_build <= 0.44 sigma_fit (DR3)
    D = {}
    D["a  frozen allowance"] = dict(sigma=0.020, up=0.0, src="PREREG 1.5")
    D["b  max(0.02, half ladder+NSS-off spread)"] = dict(sigma=max(0.020, 0.5 * spread), up=0.0, src="note sec 3")
    D["c  max(0.02, full ladder+NSS-off spread)"] = dict(sigma=max(0.020, spread), up=0.0, src="owner list (c)")
    D["d  record inter-group spread"] = dict(sigma=0.174, up=0.0, src="mi_wb_gate_fork_2026.py:221")
    D["e  jackknife over implementable cut variants"] = dict(sigma=max(jk, 0.0), up=0.0,
                                                           src="delete-one over {V0,V1,V2,V3}")
    for du in (0.0, 0.05, 0.10):
        q = math.sqrt(0.015 ** 2 + 0.005 ** 2 + 0.0373 ** 2 + nss ** 2 + du ** 2)
        D["f  quadrature budget, triples %.2f" % du] = dict(
            sigma=q, up=0.0, src="PREREG 1.5 ecc 0.015 + footing 0.005; Amdt shape +0.0373; NSS-off |shift|; "
                                 "projection 0 (forward-modelled); triples = Amdt 3 delta_up")
    for du in (0.0, 0.05, 0.10):
        D["g1 Amdt 3 one-sided, delta_up %.2f" % du] = dict(sigma=0.020, up=du,
                                                             src="amendment3_systematics S3/S4: law side uses gamma - delta_up")
    D["g2 Amdt 18 sigma_build in quadrature"] = dict(sigma=math.sqrt(0.02 ** 2 + sbuild ** 2), up=0.0,
                                                    src="Amdt 18 (reported-only there; used here as a variant)")
    D["g3 PREREG 1.5 stability gate"] = dict(sigma=0.020, up=0.0, gate_max_shift=max(abs(x) for x in shifts),
                                            gate_sigma_fit=sf_base, src="every ladder shift < 1 sigma_fit")
    return D, dict(shifts=shifts, spread=spread, jackknife=jk, nss_shift=nss, base=base, sigma_fit_base=sf_base)


R = {"fits": FIT, "mutate": MUT, "predictions_AQUAL": PRED, "screened": SCREENED, "defs": {}}
dry_sig = {fo: FIT["%s|V0 baseline (frozen-cut build)" % fo]["sigma_fit"] for fo in ("canonical", "alt")}
for fo in ("canonical", "alt"):
    D, info = defs_for(fo)
    s1 = {"mock": 0.019 * math.sqrt(30000.0), "DR3-cal": dry_sig[fo] * math.sqrt(6210.0)}
    P("\n[%s] ladder shifts %s ; spread %.4f ; jackknife %.4f ; NSS-off |shift| %.4f ; baseline sigma_fit %.4f"
      % (fo, ", ".join("%+.4f" % x for x in info["shifts"]), info["spread"], info["jackknife"],
         info["nss_shift"], info["sigma_fit_base"]))
    P("  %-46s %7s | %-34s | %-34s" % ("definition", "sig_sys", "z at N=30k (mock/DR3cal) prim | altg",
                                        "N for 3 sigma (mock/DR3cal) prim | altg"))
    out = {}
    for name, d in D.items():
        row = dict(sigma_sys=d["sigma"], delta_up=d["up"], source=d["src"])
        zs, ns = [], []
        for gk in ("primary", "alt_gext"):
            delta = PRED[fo][gk] - SCREENED - d["up"]
            for lab in ("mock", "DR3-cal"):
                sf = s1[lab] / math.sqrt(30000.0)
                z = delta / math.sqrt(sf ** 2 + d["sigma"] ** 2)
                need = (delta / 3.0) ** 2 - d["sigma"] ** 2
                N3 = (s1[lab] ** 2 / need) if need > 0 else None
                row["%s|%s" % (gk, lab)] = dict(delta=delta, z=z, N3=N3)
                zs.append(z)
                ns.append(N3)
        row["ceiling_sigma_sys_3sigma"] = {gk: (PRED[fo][gk] - SCREENED - d["up"]) / 3.0 for gk in PRED[fo]}
        if "gate_max_shift" in d:
            row["gate_pass_on_DR3"] = d["gate_max_shift"] < d["gate_sigma_fit"]
            row["gate_max_shift"] = d["gate_max_shift"]
        out[name] = row

        def fn(v):
            return "never" if v is None else "%.0f" % v
        P("  %-46s %7.4f | %5.2f/%5.2f | %5.2f/%5.2f        | %6s/%6s | %6s/%6s"
          % (name, d["sigma"], zs[0], zs[1], zs[2], zs[3], fn(ns[0]), fn(ns[1]), fn(ns[2]), fn(ns[3])))
        if "gate_max_shift" in d:
            P("      gate on DR3: max ladder shift %.4f vs sigma_fit %.4f -> %s"
              % (d["gate_max_shift"], d["gate_sigma_fit"], "PASS" if row["gate_pass_on_DR3"] else "FAIL (systematic-limited)"))
    R["defs"][fo] = out
    R["info_" + fo] = info
    worst = min(min(r["%s|%s" % (gk, lab)]["z"] for gk in ("primary", "alt_gext") for lab in ("mock", "DR3-cal"))
                for r in out.values())
    n3ok = [k for k, r in out.items() if all(r["%s|%s" % (gk, lab)]["N3"] is not None
                                             for gk in ("primary", "alt_gext") for lab in ("mock", "DR3-cal"))]
    P("  -> %s: worst z over all definitions %.2f ; definitions under which 3 sigma is reachable at some N: %d of %d"
      % (fo, worst, len(n3ok), len(out)))
    R["summary_" + fo] = dict(worst_z=worst, n_defs_reachable=len(n3ok), n_defs=len(out),
                              unreachable=[k for k in out if k not in n3ok])

npass = sum(c["passed"] for c in CHECKS)
P("\nD2_SIGMA_SYS_DEFS COMPLETE: %d/%d checks PASS." % (npass, len(CHECKS)))
R["checks"] = CHECKS
with open(OUT, "w") as f:
    f.write("\n".join(LINES) + "\n")
with open(JS, "w") as f:
    json.dump(R, f, indent=1, default=float)
sys.exit(0 if npass == len(CHECKS) else 1)
