"""AGB1 Part B: re-read CFG684 and CFG689 (DES5 modes) with the Son et al. (2025) age correction applied to the
DES-SN5YR Dovekie moduli, mu -> mu - A x T_S(zHD). The lane sources are executed unchanged except for exact text
substitutions (LGS1's harness plus the shift): the supernova selection mask and shift, the output file paths, and
(CFG684 only) the list of combinations.

usage: python3 agb1_reread.py <target> <sample> <A> [outdir]
  target: cfg684 | cfg689_D5 | cfg689_TD5F
  sample: full      every supernova (the committed lanes' own selection)
          des_only  IDSURVEY == 10 only (1,623 supernovae)
  A     : 0 (harness check: the shift is exactly zero) or 1 (the published correction)
"""
import os, sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import agb1_template as TPL

REPO = os.path.normpath(os.path.join(HERE, "..", ".."))
TARGET, SAMPLE, AMP = sys.argv[1], sys.argv[2], float(sys.argv[3])
OUTDIR = sys.argv[4] if len(sys.argv) > 4 else HERE
assert SAMPLE in ("full", "des_only"), SAMPLE
assert AMP in (0.0, 1.0), AMP
TAG = f"{SAMPLE}_A{int(AMP)}"


def AGB_SEL(rows):
    ids = np.array([int(r[2]) for r in rows])
    sel = np.ones(len(ids), bool) if SAMPLE == "full" else ids == 10
    print(f"AGB1 selection '{SAMPLE}': {int(sel.sum())} of {len(ids)} supernovae kept "
          f"({int((sel & (ids == 10)).sum())} DES, {int((sel & (ids != 10)).sum())} legacy)", flush=True)
    return sel


def AGB_SHIFT(z):
    s = AMP*TPL.T(np.asarray(z, float), "S")
    print(f"AGB1 shift: mu -> mu - {AMP:g} x T_S(zHD); shift min {s.min():.4f} max {s.max():.4f} mag", flush=True)
    return s


def sub(text, old, new):
    assert text.count(old) == 1, f"expected exactly one occurrence of: {old!r} (found {text.count(old)})"
    return text.replace(old, new)


if TARGET == "cfg684":
    SRC = os.path.join(REPO, "campaign_fresh_gravity", "CFG684_bao_cc_sn_robust", "cfg684_robust.py")
    AGB_OUT = os.path.join(OUTDIR, f"agb1_cfg684_{TAG}.json")
    t = open(SRC).read()
    t = sub(t, "ww = dz > 0; Cd = np.linalg.inv(Wd)[np.ix_(ww, ww)]; Wd = np.linalg.inv(Cd)",
            "ww = (dz > 0) & AGB_SEL(rows); dmu = dmu - AGB_SHIFT(dz); Cd = np.linalg.inv(Wd)[np.ix_(ww, ww)]; Wd = np.linalg.inv(Cd)")
    t = sub(t, 'COMBOS = ["BAO+PP", "BAO+CC", "BAO+PP+CC", "BAO+DES5+CC", "BAO+U3+CC", "BAO+DES5", "BAO+U3"]',
            'COMBOS = ["BAO+DES5+CC", "BAO+DES5"]')
    t = sub(t, 'open(os.path.join(HERE, "cfg684_results" + ("_MUTATE" if MUT else "") + ".json"), "w")', 'open(AGB_OUT, "w")')
    os.environ.pop("MUTATE", None)
elif TARGET in ("cfg689_D5", "cfg689_TD5F"):
    SRC = os.path.join(REPO, "campaign_fresh_gravity", "CFG689_native_ruler_bao", "cfg689_native_ruler.py")
    AGB_OUT = os.path.join(OUTDIR, f"agb1_{TARGET}_{TAG}")
    os.environ["CFG689_MODE"] = TARGET.split("_")[1]
    t = open(SRC).read()
    t = sub(t, "ww = dz > 0; Cd = np.linalg.inv(Wd)[np.ix_(ww, ww)]",
            "ww = (dz > 0) & AGB_SEL(rows); dmu = dmu - AGB_SHIFT(dz); Cd = np.linalg.inv(Wd)[np.ix_(ww, ww)]")
    t = sub(t, 'OUTF = open(os.path.join(HERE, f"cfg689{TAG}.out"), "w")', 'OUTF = open(AGB_OUT + ".out", "w")')
    t = sub(t, 'open(os.path.join(HERE, f"cfg689{TAG}.json"), "w")', 'open(AGB_OUT + ".json", "w")')
else:
    sys.exit(f"unknown target {TARGET}")

g = {"__file__": SRC, "__name__": "__main__", "AGB_SEL": AGB_SEL, "AGB_SHIFT": AGB_SHIFT, "AGB_OUT": AGB_OUT}
exec(compile(t, SRC, "exec"), g)
