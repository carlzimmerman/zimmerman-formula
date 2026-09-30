#!/usr/bin/env python3
"""DR4-READY-1, WP2 NOISE FLOOR at full size: how many final pairs change when NOTHING about the data changes and only the random streams of the builder's Monte Carlo steps do?
The full WP2 dry run (wp2_variant_full_dr3.py) found 180 primary-only and 185 variant-only final pairs (about 3% each way, all first missing at stage G).  The frozen builder draws random numbers
in three places: the shifted chance realisations of stage E (pair_search(shift = True, seed = r + 1), per-block seeds over np.array_split(keep, 400), so the blocks move when the source set moves),
the leave-10%-out fold of r_chance (default_rng(SEED).integers over len(Xc)) and the velocity-error Monte Carlo of stage G (one stream over the pair array).  Adding the 3,218 sources without G moves
all three streams, so part of those differences is reseeding noise, not the all-source cut.  Here: each base (primary, all-source variant) is rebuilt with other seeds for ALL THREE streams
(N_SHIFT = 3, the builder's smoke setting, as in WP2), the data untouched; the flips between two builds of the SAME base are the noise floor, to be set against the primary-versus-variant differences.
NO NETWORK (socket guard).  NEW file: wp2_variant_full_dr3.py's machinery is exec'd READ-ONLY up to its main block, with exactly two text substitutions (the work dir, and the stage-E shift seed offset);
catalog_builder/build_catalog.py is imported read-only and its SEED / vt_error_mc are patched IN MEMORY only (no frozen file is edited).  The default-seed build must reproduce the WP2 counts.
DR3 numbers are code-path tests, never results (Amendment 7(e)).
Run: python3 prep_2026/gaia_dr4_prep/dr4_ready_1/wp2_noise_floor_full_dr3.py
"""
import sys
sys.dont_write_bytecode = True
import io, json, time, contextlib
from pathlib import Path
import numpy as np

HERE = Path(__file__).resolve().parent
T0 = time.time()
text = (HERE / "wp2_variant_full_dr3.py").read_text()
cut = text.index('P("WP2 full size: primary vs all-source variant base')
head = text[:cut]
for a in ('work = src / "wp2_full"', 'seed=r + 1)'):
    assert head.count(a) == 1, a
head = head.replace('work = src / "wp2_full"', 'work = WORKDIR').replace('seed=r + 1)', 'seed=r + 1 + SHIFT_OFF)')
ns = {"__file__": str(HERE / "wp2_variant_full_dr3.py"), "__name__": "wp2_lib", "WORKDIR": None, "SHIFT_OFF": 0}
exec(compile(head, "wp2_variant_full_dr3.py", "exec"), ns)                      # installs the socket guard and defines build()
B, BASES = ns["B"], ns["BASES"]
SEED0 = B.SEED
ORIG_VT = B.vt_error_mc
LOG = []


def P(s=""):
    print(s, flush=True); LOG.append(s)


def run(base, k):
    """build `base` with the seed set k (k = 0: the frozen seeds, reusing the WP2 caches)."""
    src = BASES[base]
    if k == 0:
        work = src / "wp2_full"
    else:
        work = src / f"wp2_noise_{k}"
        work.mkdir(exist_ok=True)
        for f in ("stage_A.npz", "stage_B.npz", "stage_C.npz", "stage_D.npz", "AV_sfd98.npz"):
            if not (work / f).exists():
                (work / f).symlink_to(src / "wp2_full" / f)
    ns["WORKDIR"] = work
    ns["SHIFT_OFF"] = 100 * k
    B.SEED = SEED0 + k
    B.vt_error_mc = lambda S, a, b, th, corr, n_trials=212, seed=None: ORIG_VT(S, a, b, th, corr, n_trials=n_trials, seed=SEED0 + k)
    t = time.time()
    with contextlib.redirect_stdout(io.StringIO()):
        rep, sets, gnull, S = ns["build"](base, src)
    B.SEED = SEED0
    B.vt_error_mc = ORIG_VT
    P(f"  {base:14s} seed set {k}: initial pairs {rep['n_initial_pairs']:,d}; clean {rep['n_clean_pairs']:,d}; with R {rep['n_R_pairs']:,d}; FINAL {rep['n_final']:,d}  ({time.time() - t:.0f} s)")
    return rep, sets["G"], sets["F"]


P("WP2 NOISE FLOOR, full size: each base rebuilt with other random seeds for the shifted realisations, the r_chance folds and the velocity-error Monte Carlo (data untouched)")
KS = (0, 1, 2)
FIN, STF, REP = {}, {}, {}
for base in BASES:
    for k in KS:
        REP[(base, k)], FIN[(base, k)], STF[(base, k)] = run(base, k)
WP2 = json.load(open(HERE / "wp2_variant_full_dr3.json"))
ok0 = all(REP[(b, 0)]["n_final"] == WP2["bases"][b]["n_final"] and REP[(b, 0)]["n_initial_pairs"] == WP2["bases"][b]["n_initial_pairs"] for b in BASES)
P(f"\n  [{'PASS' if ok0 else 'FAIL'}] CONTROL: the default seeds reproduce WP2's counts (initial pairs and FINAL, both bases): primary {REP[('primary', 0)]['n_final']:,d} vs {WP2['bases']['primary']['n_final']:,d}; variant {REP[('allsource_15c', 0)]['n_final']:,d} vs {WP2['bases']['allsource_15c']['n_final']:,d}")


def diff(A, Bset):
    return len(A - Bset), len(Bset - A)


P("\n  FLIPS in the FINAL pair sets (one-way counts: only in the first, only in the second)")
same, cross = [], []
for base in BASES:
    for i in range(len(KS)):
        for j in range(i + 1, len(KS)):
            a, b = diff(FIN[(base, KS[i])], FIN[(base, KS[j])])
            same.append((a, b))
            P(f"    SAME base {base:14s} seed set {KS[i]} vs {KS[j]}: {a} / {b}  (final {len(FIN[(base, KS[i])]):,d} / {len(FIN[(base, KS[j])]):,d})")
for k in KS:
    a, b = diff(FIN[("primary", k)], FIN[("allsource_15c", k)])
    cross.append((a, b))
    P(f"    CROSS bases, SAME seed set {k}: primary-only {a}; variant-only {b}")
for i in KS:
    for j in KS:
        if i != j:
            a, b = diff(FIN[("primary", i)], FIN[("allsource_15c", j)])
            P(f"    CROSS bases, DIFFERENT seed sets (primary {i}, variant {j}): primary-only {a}; variant-only {b}")
ms = float(np.mean([x for t in same for x in t])); mc = float(np.mean([x for t in cross for x in t]))
P(f"\n  mean one-way flips: SAME base, other seeds (pure noise) {ms:.0f}; CROSS bases, same seeds (noise + the all-source effect) {mc:.0f}; ratio {mc / ms:.2f}")
P("  Reading: if the pure-noise flips are about as large as the cross-base differences, the WP2 difference counts are at the reseeding noise floor at N_SHIFT = 3 and do not show an effect of the all-source base on the final pair set; a real effect would show as cross-base flips well above the noise.")
res = dict(flips_same_base=same, flips_cross_same_seed=cross, mean_same=ms, mean_cross=mc, control_default_reproduces_wp2=ok0,
           finals={f"{b}|{k}": len(FIN[(b, k)]) for (b, k) in FIN}, seconds=round(time.time() - T0, 1))
P(f"\n{'ALL PASS' if ok0 else 'CONTROL FAILED'}  ({time.time() - T0:.0f} s)")
(HERE / "wp2_noise_floor_full_dr3.json").write_text(json.dumps(res, indent=1, default=str) + "\n")
(HERE / "wp2_noise_floor_full_dr3.out").write_text("\n".join(LOG) + "\n")
sys.exit(0 if ok0 else 1)
