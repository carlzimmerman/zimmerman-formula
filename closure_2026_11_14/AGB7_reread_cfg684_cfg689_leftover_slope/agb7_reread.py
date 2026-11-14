"""AGB7: re-read CFG684 and CFG689 (DES5 modes) with an age drift of chosen size and shape applied to the DES-SN5YR
Dovekie moduli, mu -> mu - A x T(zHD). This is AGB1's harness (agb1_reread.py, itself LGS1's) with two
generalisations: A may be any number, and T may be AGB1's cosmic-average template T_S or the sample's own drift
T_H of AGB3. The lane sources are executed unchanged except for the harness's exact text substitutions.

usage: python3 agb7_reread.py <target> <sample> <A> <template> [outdir]
  target  : cfg684 | cfg689_D5 | cfg689_TD5F
  sample  : full | des_only (IDSURVEY == 10 only, 1,623 supernovae)
  A       : amplitude in units of the published slope (0 = harness check)
  template: S (AGB1's T_S) | H (AGB3's T_H: curve full_sfr or des_only_sfr of agb3_S.json, by sample)
Outputs: agb7_<target>_<sample>_<template><100 A, three digits>.json (and .out for CFG689)."""
import json, os, sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.normpath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, os.path.join(REPO, "closure_2026_11_13", "AGB1_progenitor_age_bias"))
import agb1_template as TPL

TARGET, SAMPLE, AMP, TEMPLATE = sys.argv[1], sys.argv[2], float(sys.argv[3]), sys.argv[4]
OUTDIR = sys.argv[5] if len(sys.argv) > 5 else HERE
assert SAMPLE in ("full", "des_only") and TEMPLATE in ("S", "H"), (SAMPLE, TEMPLATE)
TAG = f"{SAMPLE}_{TEMPLATE}{int(round(100*AMP)):03d}"
if TEMPLATE == "H":
    _c = json.load(open(os.path.join(REPO, "closure_2026_11_14", "AGB3_des_host_star_formation", "agb3_S.json")))["curves"][f"{SAMPLE}_sfr"]
    _zc, _ac = np.array(_c["z"]), np.array(_c["age"])


def AGB_SEL(rows):
    ids = np.array([int(r[2]) for r in rows])
    sel = np.ones(len(ids), bool) if SAMPLE == "full" else ids == 10
    print(f"AGB7 selection '{SAMPLE}': {int(sel.sum())} of {len(ids)} supernovae kept "
          f"({int((sel & (ids == 10)).sum())} DES, {int((sel & (ids != 10)).sum())} legacy)", flush=True)
    return sel


def AGB_SHIFT(z):
    z = np.asarray(z, float)
    t = TPL.T(z, "S") if TEMPLATE == "S" else 0.030*(_ac[0] - np.interp(z, _zc, _ac))
    s = AMP*t
    print(f"AGB7 shift: mu -> mu - {AMP:g} x T_{TEMPLATE}(zHD); shift min {s.min():.4f} max {s.max():.4f} mag", flush=True)
    return s


def sub(text, old, new):
    assert text.count(old) == 1, f"expected exactly one occurrence of: {old!r} (found {text.count(old)})"
    return text.replace(old, new)


if TARGET == "cfg684":
    SRC = os.path.join(REPO, "campaign_fresh_gravity", "CFG684_bao_cc_sn_robust", "cfg684_robust.py")
    AGB_OUT = os.path.join(OUTDIR, f"agb7_cfg684_{TAG}.json")
    t = open(SRC).read()
    t = sub(t, "ww = dz > 0; Cd = np.linalg.inv(Wd)[np.ix_(ww, ww)]; Wd = np.linalg.inv(Cd)",
            "ww = (dz > 0) & AGB_SEL(rows); dmu = dmu - AGB_SHIFT(dz); Cd = np.linalg.inv(Wd)[np.ix_(ww, ww)]; Wd = np.linalg.inv(Cd)")
    t = sub(t, 'COMBOS = ["BAO+PP", "BAO+CC", "BAO+PP+CC", "BAO+DES5+CC", "BAO+U3+CC", "BAO+DES5", "BAO+U3"]',
            'COMBOS = ["BAO+DES5+CC", "BAO+DES5"]')
    t = sub(t, 'open(os.path.join(HERE, "cfg684_results" + ("_MUTATE" if MUT else "") + ".json"), "w")', 'open(AGB_OUT, "w")')
    os.environ.pop("MUTATE", None)
elif TARGET in ("cfg689_D5", "cfg689_TD5F"):
    SRC = os.path.join(REPO, "campaign_fresh_gravity", "CFG689_native_ruler_bao", "cfg689_native_ruler.py")
    AGB_OUT = os.path.join(OUTDIR, f"agb7_{TARGET}_{TAG}")
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
