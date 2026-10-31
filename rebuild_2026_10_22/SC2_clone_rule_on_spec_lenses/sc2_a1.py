#!/usr/bin/env python3
"""SC2 AMENDMENT A1 (post-result, reported only): more catalogues under both rules. sc2_run.py's own text with asserted replacements; per-run JSON goes to the scratch root, the summary comes from sc2_a1_table.py.
    OMP_NUM_THREADS=1 nice -n 15 python3 sc2_a1.py measure <kids_cache> <frozen_p2_work> <scratch_root> oldS1..5|newS1..5|old20a|old20b|new20b
    PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 sc2_a1.py grade <kids_cache> <frozen_p2_work> <scratch_root> <same>
kappa = 1/2 FITTED; footings never pooled."""
import os, sys
A1_RUN = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sc2_run.py"); A1_M = sys.argv[5]
A1_TAB = {f"oldS{i}": ("old", (4, 2), 20261031 + 10 + i) for i in range(1, 6)}; A1_TAB.update({f"newS{i}": ("new", (4, 2), 20261031 + 20 + i) for i in range(1, 6)}); A1_TAB.update(old20a=("old", (20, 20), 20261031 + 31), old20b=("old", (20, 20), 20261031 + 32), new20b=("new", (20, 20), 20261031 + 33))
A1_RULE, A1_KEEP, A1_SEED = A1_TAB[A1_M]; a1_s = open(A1_RUN).read()
def a1_rep(a, b):
    global a1_s
    assert a1_s.count(a) == 1, a[:80]; a1_s = a1_s.replace(a, b)
a1_rep('SC2_KEEP = {"new": (4, 2), "k20": (20, 20), "mutate": (4, 2)}.get(SC2_MODE)', f'SC2_KEEP = {A1_KEEP!r}')
a1_rep('    if SC2_MODE == "old": return T\n', f'''    if {A1_RULE == "old"!r}:
        a = "(Rra, Rde, Rz, Rlm, Rf, Rsrc), trR = make_iso(idxS1, 1.0, 3 * len(idxS1), veto=False, emin=1.0)\\n"; assert T.count(a) == 1
        return T.replace(a, a + """_rng_frozen = rng; rng = np.random.default_rng({A1_SEED})
(I3ra, I3de, I3z, I3lm, I3f, I3src), tr3 = make_iso(idxS3, 3.0, {A1_KEEP[0]} * len(idxS3))
(I1ra, I1de, I1z, I1lm, I1f, I1src), tr1 = make_iso(idxS1, 1.0, {A1_KEEP[1]} * len(idxS1))
rng = _rng_frozen; SC2_INFO3 = SC2_INFO1 = dict(rule="old")
""")
''')
a1_rep('rng = np.random.default_rng(20261031 + 4)', f'rng = np.random.default_rng({A1_SEED})')
a1_rep('SC2_R["reading"] = "NO READING" if not all(SC2_OK.values()) else RES2["combined"]', 'SC2_R["reading"] = RES2["combined"]')
a1_rep('SC2_TAG = {"old": "old", "new": "new", "k20": "k20", "mutate": "MUTATE"}[SC2_MODE]', 'SC2_TAG = SC2_MODE')
a1_rep('open(os.path.join(SC2_LANE, f"sc2_results_{SC2_TAG}.json"), "w")', 'open(os.path.join(SC2_ROOT, f"sc2_results_{SC2_TAG}.json"), "w")')
a1_rep('open(os.path.join(SC2_LANE, f"sc2_{SC2_TAG}.out"), "w")', 'open(os.path.join(SC2_ROOT, f"sc2_{SC2_TAG}.out"), "w")')
__file__ = A1_RUN; exec(compile(a1_s, "sc2_run_a1", "exec"))
