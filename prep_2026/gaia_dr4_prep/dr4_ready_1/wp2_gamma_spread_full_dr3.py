#!/usr/bin/env python3
"""DR4-READY-1, WP2-gamma: the build-to-build scatter of gamma-hat for the PRIMARY base at the builder's REAL setting (N_SHIFT = 30).
Frozen question: WP2_GAMMA_SPREAD_FROZEN.md (01bc48e32), committed before this script existed.  DR3 numbers are code-path tests, never results (Amendment 7(e)); NON-SCORING; no verdict words.
Ten seed sets k = 0..9 (k = 0 the builder's own frozen seeds) re-seed the three Monte Carlo streams of the frozen builder (the stage-E shifted realisations and mask, the r_chance folds, the stage-G
velocity-error MC); the data, the cuts, the offline correlations and A_V are untouched.  gamma-hat and sigma_fit come from the pipeline's OWN estimator exactly as catalog_builder/validate_dr3.py::v4_gamma
(ingest_csv, the DR3-noise forward model, run_fit, both footings).  NO NETWORK (socket guard).  NEW file: wp2_variant_full_dr3.py's machinery is exec'd READ-ONLY up to its main block with three text
substitutions (the work dir, the stage-E shift seed offset, and writing the final table as final.csv); build_catalog.py and wide_binary_pipeline.py are imported read-only (seeds patched IN MEMORY only).
Run:  python3 prep_2026/gaia_dr4_prep/dr4_ready_1/wp2_gamma_spread_full_dr3.py        (MUTATE=1: a global v_perp x 1.05 on the k = 0 catalog; MUTATE=2: the same scale only for deep-MOND pairs; both need the main run first)
"""
import sys
sys.dont_write_bytecode = True
import io, json, os, time, contextlib
from pathlib import Path
import numpy as np

MUTV = os.environ.pop("MUTATE", "").strip()
MUT = MUTV in ("1", "2")
HERE = Path(__file__).resolve().parent
T0 = time.time()
LOG = []


def P(s=""):
    print(s, flush=True); LOG.append(s)


text = (HERE / "wp2_variant_full_dr3.py").read_text()
cut = text.index('P("WP2 full size: primary vs all-source variant base')
head = text[:cut]
for a, b in (('work = src / "wp2_full"', 'work = WORKDIR'), ('seed=r + 1)', 'seed=r + 1 + SHIFT_OFF)'),
             ('rep["final_csv_sha256"] = __import__("hashlib").sha256(buf.getvalue().encode()).hexdigest()',
              'rep["final_csv_sha256"] = __import__("hashlib").sha256(buf.getvalue().encode()).hexdigest(); (work / "final.csv").write_text(buf.getvalue())')):
    assert head.count(a) == 1, a
    head = head.replace(a, b)
ns = {"__file__": str(HERE / "wp2_variant_full_dr3.py"), "__name__": "wp2_lib", "WORKDIR": None, "SHIFT_OFF": 0}
exec(compile(head, "wp2_variant_full_dr3.py", "exec"), ns)                      # installs the socket guard and defines build()
B, BASES = ns["B"], ns["BASES"]
sys.path.insert(0, str(HERE.parent))
import wide_binary_pipeline as wbp                                                # read-only
SEED0, ORIG_VT = B.SEED, B.vt_error_mc
SRC = BASES["primary"]
WP2 = json.load(open(HERE / "wp2_variant_full_dr3.json"))["bases"]["primary"]
KS = tuple(range(10))
SIG_SYS = 0.02

rng0 = np.random.default_rng(20261216)
with contextlib.redirect_stdout(io.StringIO()):
    pop = wbp.make_population(3_000_000, rng0, dr4=False)
    MODS = {"canonical": (wbp.A0_CAN, wbp.model_medians(pop, wbp.A0_CAN, wbp.GRID, rng0)),
            "alt": (wbp.A0_ALT, wbp.model_medians(pop, wbp.A0_ALT, wbp.GRID, rng0))}


def fit_csv(path, seed, vscale=1.0, lowg_only=False):
    gN, vt, _ = wbp.ingest_csv(str(path))
    out = {}
    for foot, (a0v, mod) in MODS.items():
        with contextlib.redirect_stdout(io.StringIO()):
            ly = np.log10(gN / a0v)
            g, sg, *_ = wbp.run_fit(ly, (np.where(ly < 0, vt * vscale, vt) if lowg_only else vt * vscale), mod, np.random.default_rng(seed), foot)
        out[foot] = (float(g), float(sg))
    return out, int(len(vt))


def sd(x):
    return float(np.std(np.asarray(x, float), ddof=1))


if MUT:
    R = json.load(open(HERE / "wp2_gamma_spread_full_dr3.json"))
    low = MUTV == "2"
    base, _ = fit_csv(SRC / "wp2_gamma_0" / "final.csv", 20261217)
    mut, _ = fit_csv(SRC / "wp2_gamma_0" / "final.csv", 20261217, vscale=1.05, lowg_only=low)
    P("WP2-gamma MUTATE" + ("=2 (added after the first MUTATE run; POST HOC): v_perp/v_circ x 1.05 ONLY for pairs with log10(g_N/a0) < 0 (an acceleration-dependent change) on the k = 0 catalog, same fit seed"
                            if low else "=1: v_perp x 1.05 on ALL pairs of the k = 0 catalog, same fit seed (the fit has a free kappa that absorbs a global scale)"))
    ok = True
    for foot in MODS:
        shift = mut[foot][0] - base[foot][0]; thr = 3 * R["fit_only"][foot]["sd"]
        P(f"  {foot:10s} gamma-hat {base[foot][0]:.4f} -> {mut[foot][0]:.4f}  (shift {shift:+.4f}; three times the fit-only SD {thr:.4f})")
        ok &= abs(shift) > thr
    P(f"  [{'PASS' if ok else 'FAIL'}] C3 MUTATE the fit responds to the catalog: the shift exceeds three times the fit-only SD in both footings")
    (HERE / ("wp2_gamma_spread_full_dr3_MUTATE2.out" if low else "wp2_gamma_spread_full_dr3_MUTATE.out")).write_text("\n".join(LOG) + "\n")
    sys.exit(0 if ok else 1)

P("WP2-gamma: build-to-build scatter of gamma-hat, PRIMARY base, N_SHIFT = 30, ten seed sets (DR3 numbers are code-path tests; no verdict words)")
assert B.N_SHIFT == 30
ns["N_SHIFT"] = 30
FIN, REP, CSV = {}, {}, {}
for k in KS:
    work = SRC / f"wp2_gamma_{k}"
    work.mkdir(exist_ok=True)
    for f in ("stage_A.npz", "stage_B.npz", "stage_C.npz", "stage_D.npz", "AV_sfd98.npz"):
        if not (work / f).exists():
            (work / f).symlink_to(SRC / "wp2_full" / f)
    ns["WORKDIR"], ns["SHIFT_OFF"] = work, 100 * k
    B.SEED = SEED0 + k
    B.vt_error_mc = lambda S, a, b, th, corr, n_trials=212, seed=None, k=k: ORIG_VT(S, a, b, th, corr, n_trials=n_trials, seed=SEED0 + k)
    t = time.time()
    with contextlib.redirect_stdout(io.StringIO()):
        rep, sets, gnull, S = ns["build"]("primary", SRC)
    B.SEED, B.vt_error_mc = SEED0, ORIG_VT
    REP[k], FIN[k], CSV[k] = rep, sets["G"], work / "final.csv"
    P(f"  build k = {k}: initial pairs {rep['n_initial_pairs']:,d}; clean {rep['n_clean_pairs']:,d}; with R {rep['n_R_pairs']:,d}; FINAL {rep['n_final']:,d}  ({time.time() - t:.0f} s)")

C1 = B.N_SHIFT == 30 and ns["N_SHIFT"] == 30
C2 = all(REP[k]["n_initial_pairs"] == WP2["n_initial_pairs"] and REP[k]["n_clean_pairs"] == WP2["n_clean_pairs"] for k in KS)
a_, b_ = len(FIN[0]), 0
test = set(list(FIN[0])[100:])
C4 = (len(FIN[0] - test) == 100 and len(test - FIN[0]) == 0)
P(f"\n  [{'PASS' if C1 else 'FAIL'}] C1 the builder's own N_SHIFT default is 30 (used here: {ns['N_SHIFT']})")
P(f"  [{'PASS' if C2 else 'FAIL'}] C2 every build has WP2's stage-C and stage-D counts ({WP2['n_initial_pairs']:,d} initial, {WP2['n_clean_pairs']:,d} clean)")
P(f"  [{'PASS' if C4 else 'FAIL'}] C4 the flip counter returns exactly 100 when 100 pairs are removed from the k = 0 set")

N = [len(FIN[k]) for k in KS]
flips = [(len(FIN[0] - FIN[k]), len(FIN[k] - FIN[0])) for k in KS[1:]]
pair_flips = [len(FIN[i] - FIN[j]) for i in KS for j in KS if i != j]
P("\nQ1  final pair count and flips")
P(f"    final counts: {N}; mean {np.mean(N):.1f}, SD {sd(N):.1f}, range {min(N)} to {max(N)}")
P(f"    one-way flips against k = 0: {flips}; mean {np.mean([x for f in flips for x in f]):.1f}")
P(f"    all ordered pairs of builds, one-way flips: mean {np.mean(pair_flips):.1f}, SD {sd(pair_flips):.1f}, range {min(pair_flips)} to {max(pair_flips)}  (fraction of the mean final count: {np.mean(pair_flips) / np.mean(N):.4f})")

G, SF = {f: [] for f in MODS}, {f: [] for f in MODS}
for k in KS:
    fits, n = fit_csv(CSV[k], 20261217 + k)
    for f in MODS:
        G[f].append(fits[f][0]); SF[f].append(fits[f][1])
FO = {f: [] for f in MODS}
for j in range(1, 11):
    fits, _ = fit_csv(CSV[0], 20261217 + 100 + j)
    for f in MODS:
        FO[f].append(fits[f][0])
P("\nQ2 / Q3  gamma-hat across the ten builds (pipeline estimator, DR3-noise forward model, NON-SCORING)")
res = {"final_counts": N, "flips_vs_k0": flips, "pair_flips_mean": float(np.mean(pair_flips)), "fit_only": {}, "footings": {}}
for f in MODS:
    g, s = np.array(G[f]), np.array(SF[f]); st = np.sqrt(s ** 2 + SIG_SYS ** 2)
    sdb, sdf = sd(g), sd(FO[f])
    bo = float(np.sqrt(max(0.0, sdb ** 2 - sdf ** 2)))
    P(f"  {f}:")
    P("    gamma-hat per build: " + " ".join(f"{x:.4f}" for x in g))
    P("    sigma_fit per build: " + " ".join(f"{x:.4f}" for x in s))
    P(f"    mean gamma-hat {g.mean():.4f}; SD across builds {sdb:.4f}; mean sigma_fit {s.mean():.4f}; mean sigma_tot {st.mean():.4f}")
    P(f"    SD/mean sigma_fit = {sdb / s.mean():.3f};  SD/mean sigma_tot = {sdb / st.mean():.3f}")
    P(f"    fit-only control (k = 0 catalog, ten other fit seeds): SD {sdf:.4f} (SD/mean sigma_fit {sdf / s.mean():.3f}); SD_build / SD_fitonly = {sdb / sdf:.2f}; implied build-only SD {bo:.4f} ({bo / s.mean():.3f} of mean sigma_fit)")
    res["footings"][f] = dict(gamma=g.tolist(), sigma_fit=s.tolist(), sd_build=sdb, mean_sigma_fit=float(s.mean()), mean_sigma_tot=float(st.mean()), ratio_fit=sdb / float(s.mean()), ratio_tot=sdb / float(st.mean()),
                              build_only_sd=bo, build_only_over_sigma_fit=bo / float(s.mean()))
    res["fit_only"][f] = dict(gamma=FO[f], sd=sdf)
res["controls"] = dict(C1=C1, C2=C2, C4=C4)
res["seconds"] = round(time.time() - T0, 1)
P("\nReading: these are build-to-build and fit-only spreads of the pipeline's gamma-hat on DR3 at the real N_SHIFT; they are code-path numbers, they say nothing about any law, and the ratio to sigma_fit at DR4's N is not measured here.")
P(f"\n{sum([C1, C2, C4])}/3 controls pass (C3 is the MUTATE run); {time.time() - T0:.0f} s")
(HERE / "wp2_gamma_spread_full_dr3.json").write_text(json.dumps(res, indent=1, default=float) + "\n")
(HERE / "wp2_gamma_spread_full_dr3.out").write_text("\n".join(LOG) + "\n")
sys.exit(0 if (C1 and C2 and C4) else 1)
