"""LGS1: re-read CFG684 and CFG689 (DES5 modes) with the legacy low-redshift supernovae dropped from the DES-SN5YR
Dovekie Hubble diagram. The lane sources are executed unchanged except for three exact text substitutions each:
the supernova selection mask, the output file paths, and (CFG684 only) the list of combinations.

usage: python3 lgs1_run.py <target> <sample> [outdir]
  target: cfg684 | cfg689_D5 | cfg689_TD5F
  sample: full      every supernova (the committed lanes' own selection; harness check)
          des_only  IDSURVEY == 10 only (1,623 supernovae; the 197 legacy ones dropped)
          rand197   legacy kept, 197 randomly chosen DES supernovae dropped (seed 20261113; size control)
"""
import os, sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.normpath(os.path.join(HERE, "..", ".."))
TARGET, SAMPLE = sys.argv[1], sys.argv[2]
OUTDIR = sys.argv[3] if len(sys.argv) > 3 else HERE
assert SAMPLE in ("full", "des_only", "rand197"), SAMPLE
SEED = 20261113


def LGS_SEL(rows):
    ids = np.array([int(r[2]) for r in rows])
    sel = np.ones(len(ids), bool)
    if SAMPLE == "des_only":
        sel = ids == 10
    elif SAMPLE == "rand197":
        des = np.where(ids == 10)[0]
        drop = np.random.default_rng(SEED).choice(des, int((ids != 10).sum()), replace=False)
        sel[drop] = False
    print(f"LGS1 selection '{SAMPLE}': {int(sel.sum())} of {len(ids)} supernovae kept "
          f"({int((sel & (ids == 10)).sum())} DES, {int((sel & (ids != 10)).sum())} legacy)", flush=True)
    return sel


def sub(text, old, new):
    assert text.count(old) == 1, f"expected exactly one occurrence of: {old!r} (found {text.count(old)})"
    return text.replace(old, new)


if TARGET == "cfg684":
    SRC = os.path.join(REPO, "campaign_fresh_gravity", "CFG684_bao_cc_sn_robust", "cfg684_robust.py")
    LGS_OUT = os.path.join(OUTDIR, f"lgs1_cfg684_{SAMPLE}.json")
    t = open(SRC).read()
    t = sub(t, "ww = dz > 0; Cd = np.linalg.inv(Wd)[np.ix_(ww, ww)]; Wd = np.linalg.inv(Cd)",
            "ww = (dz > 0) & LGS_SEL(rows); Cd = np.linalg.inv(Wd)[np.ix_(ww, ww)]; Wd = np.linalg.inv(Cd)")
    t = sub(t, 'COMBOS = ["BAO+PP", "BAO+CC", "BAO+PP+CC", "BAO+DES5+CC", "BAO+U3+CC", "BAO+DES5", "BAO+U3"]',
            'COMBOS = ["BAO+DES5+CC", "BAO+DES5"]')
    t = sub(t, 'open(os.path.join(HERE, "cfg684_results" + ("_MUTATE" if MUT else "") + ".json"), "w")', 'open(LGS_OUT, "w")')
    os.environ.pop("MUTATE", None)
elif TARGET in ("cfg689_D5", "cfg689_TD5F"):
    SRC = os.path.join(REPO, "campaign_fresh_gravity", "CFG689_native_ruler_bao", "cfg689_native_ruler.py")
    LGS_OUT = os.path.join(OUTDIR, f"lgs1_{TARGET}_{SAMPLE}")
    os.environ["CFG689_MODE"] = TARGET.split("_")[1]
    t = open(SRC).read()
    t = sub(t, "ww = dz > 0; Cd = np.linalg.inv(Wd)[np.ix_(ww, ww)]",
            "ww = (dz > 0) & LGS_SEL(rows); Cd = np.linalg.inv(Wd)[np.ix_(ww, ww)]")
    t = sub(t, 'OUTF = open(os.path.join(HERE, f"cfg689{TAG}.out"), "w")', 'OUTF = open(LGS_OUT + ".out", "w")')
    t = sub(t, 'open(os.path.join(HERE, f"cfg689{TAG}.json"), "w")', 'open(LGS_OUT + ".json", "w")')
else:
    sys.exit(f"unknown target {TARGET}")

g = {"__file__": SRC, "__name__": "__main__", "LGS_SEL": LGS_SEL, "LGS_OUT": LGS_OUT}
exec(compile(t, SRC, "exec"), g)
