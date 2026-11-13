"""LGS2: re-read X54 and RF5 with the legacy low-redshift supernovae dropped from the DES-SN5YR Dovekie Hubble diagram.
The committed lane sources are executed with exact text substitutions only, each asserted to occur exactly once:
the supernova selection mask, every output path (into this folder), and the build / run / work directories (outside
the repository, under ../_external_data, never another lane's). Nothing else changes: same likelihoods, grids, seeds,
start points, steering and stop rules.

usage: python3 -I -B lgs2_run.py x54_build
       python3 -I -B lgs2_run.py x54 <sample>
       python3 -I -B lgs2_run.py rf5 <sample> <rf5 mode> [rf5 args]     rf5 mode: checks | chain | khronon | channel CELL [noforest] | grade
  sample: full      every supernova (the committed lanes' own selection; harness check)
          des_only  IDSURVEY == 10 only (1,623 supernovae; the 197 legacy ones dropped)  -- the primary sample
          rand197   legacy kept, 197 randomly chosen DES supernovae dropped (seed 20261113; size control, X54 M-C only)
kappa = 1/2 FITTED; not theory closed.
"""
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.normpath(os.path.join(HERE, "..", ".."))
EXT = os.path.normpath(os.path.join(REPO, "..", "_external_data"))
X54D = os.path.join(REPO, "rebuild_2026_10_22", "X54_cold_de_exchange")
RF5D = os.path.join(REPO, "rebuild_2026_10_22", "RF5_growth_native_yardstick")
X54_BUILD = os.path.join(EXT, "x54_class_build_lgs2")          # LGS2's own rebuild of X54's patched CLASS
SEED = 20261113
TARGET = sys.argv[1]
SAMPLE = sys.argv[2] if len(sys.argv) > 2 else None
if TARGET != "x54_build":
    assert SAMPLE in ("full", "des_only", "rand197"), SAMPLE
if TARGET == "rf5":
    assert SAMPLE in ("full", "des_only"), "RF5 has no size control in LGS2"
for k in ("X54_MUTATE", "X54_REANALYSE", "X54_SUPP", "X54_BUILD", "RF5_MUTATE", "RF5_K9_CELL"):
    os.environ.pop(k, None)                                     # normal runs only; no mutation, reanalysis or supplement


def LGS_SEL(rows):
    """rows: the split 'SN:' lines of DES-Dovekie_HD.csv; field 2 is IDSURVEY (10 = DES)."""
    ids = np.array([int(r[2]) for r in rows])
    sel = np.ones(len(ids), bool)
    if SAMPLE == "des_only":
        sel = ids == 10
    elif SAMPLE == "rand197":
        des = np.where(ids == 10)[0]
        drop = np.random.default_rng(SEED).choice(des, int((ids != 10).sum()), replace=False)
        sel[drop] = False
    print(f"LGS2 selection '{SAMPLE}': {int(sel.sum())} of {len(ids)} supernovae kept "
          f"({int((sel & (ids == 10)).sum())} DES, {int((sel & (ids != 10)).sum())} legacy)", flush=True)
    return sel


def sub(text, old, new):
    assert text.count(old) == 1, f"expected exactly one occurrence of: {old!r} (found {text.count(old)})"
    return text.replace(old, new)


MASK_OLD = "        ww = dz > 0\n"
MASK_NEW = "        ww = (dz > 0) & LGS_SEL(rows)\n"
g = {"__name__": "__main__", "LGS_SEL": LGS_SEL, "LGS_SUB": sub}

if TARGET == "x54_build":
    # X54's own builder; only the patch file's destination changes (into the build dir, not the committed X54 folder)
    SRC = os.path.join(X54D, "x54_make_patch.py")
    t = open(SRC).read()
    t = sub(t, 'BUILD = os.environ.get("X54_BUILD", os.path.join(tempfile.gettempdir(), "x54_class_build"))', "BUILD = LGS_BUILD")
    t = sub(t, 'open(os.path.join(HERE, "x54_exchange.patch"), "w")', 'open(os.path.join(BUILD, "x54_exchange_rebuilt.patch"), "w")')
    g["LGS_BUILD"] = X54_BUILD
elif TARGET == "x54":
    SRC = os.path.join(X54D, "x54_cold_de_exchange.py")
    out = os.path.join(HERE, f"lgs2_x54_{SAMPLE}")
    t = open(SRC).read()
    t = sub(t, MASK_OLD, MASK_NEW)
    t = sub(t, 'BUILD = os.environ.get("X54_BUILD", os.path.join(tempfile.gettempdir(), "x54_class_build"))', "BUILD = LGS_BUILD")
    t = sub(t, 'RUNS = os.path.join(BUILD, f"runs{TAG}")', "RUNS = LGS_RUNS")
    t = sub(t, 'OUTF = open(os.path.join(HERE, f"x54_cold_de_exchange{TAG}.out"), "w")', 'OUTF = open(LGS_OUT + ".out", "w")')
    t = sub(t, 'open(os.path.join(HERE, f"x54_cold_de_exchange_results{TAG}.json"), "w")', 'open(LGS_OUT + ".json", "w")')
    # scope: the DES-SN5YR profiles only (Pantheon+ and Union3 contain no Dovekie supernova); the size control runs M-C only
    t = sub(t, 'for model in ("C", "D"):', "for model in LGS_MODELS:")
    t = sub(t, 'for sn in ("PP", "U3"):', "for sn in LGS_OTHER_SN:")
    g.update(LGS_BUILD=X54_BUILD, LGS_RUNS=os.path.join(X54_BUILD, f"runs_{SAMPLE}"), LGS_OUT=out,
             LGS_MODELS=("C",) if SAMPLE == "rand197" else ("C", "D"), LGS_OTHER_SN=())
elif TARGET == "rf5":
    SRC = os.path.join(RF5D, "rf5.py")
    t = open(SRC).read()
    t = sub(t, 'WORK = os.path.join(EXT, f"rf5_work{TAG}")', "WORK = LGS_WORK")
    t = sub(t, 'CELLS = os.path.join(HERE, f"cells{TAG}")', "CELLS = LGS_CELLS")
    # the supernova mask enters through the X54 BAO / SN block that RF5 executes
    t = sub(t, """    blk = blk.replace('("DES5", "PP", "U3")', '("DES5",)')\n""",
            """    blk = blk.replace('("DES5", "PP", "U3")', '("DES5",)')\n    blk = LGS_SUB(blk, LGS_MASK_OLD, LGS_MASK_NEW)\n""")
    t = sub(t, 'ns = {"np": np, "os": os, "EXT": EXT, "C_KMS": C_KMS, "P": lambda *a: None}',
            'ns = {"np": np, "os": os, "EXT": EXT, "C_KMS": C_KMS, "P": lambda *a: None, "LGS_SEL": LGS_SEL}')
    # chain: the eight cells the committed run finished (1e6 .. 7000); 4000 and below stay UNDETERMINED (not finished), as committed
    t = sub(t, "    for z in ZONS:\n", "    for z in LGS_CHAIN_ZONS:\n")
    t = sub(t, 'jw(os.path.join(HERE, f"rf5_results{TAG}.json"), RES)', 'jw(LGS_OUT + ".json", RES)')
    t = sub(t, 'open(os.path.join(HERE, f"rf5{TAG}.out"), "w")', 'open(LGS_OUT + ".out", "w")')
    g.update(LGS_WORK=os.path.join(EXT, f"rf5_work_lgs2_{SAMPLE}"), LGS_CELLS=os.path.join(HERE, f"rf5_cells_{SAMPLE}"),
             LGS_OUT=os.path.join(HERE, f"lgs2_rf5_{SAMPLE}"), LGS_MASK_OLD=MASK_OLD, LGS_MASK_NEW=MASK_NEW,
             LGS_CHAIN_ZONS=[1e6, 3e5, 1e5, 5e4, 3e4, 2e4, 1.2e4, 7000.0])
    sys.argv = [SRC] + sys.argv[3:]
else:
    sys.exit(f"unknown target {TARGET}")

g["__file__"] = SRC
exec(compile(t, SRC, "exec"), g)
