"""LGS3: X54's Pantheon+ and Union3 profiles (and, optionally, CFG689's flat + acoustic-angle modes TF / TU3F) with the
low-redshift supernovae cut. The committed sources are executed with exact text substitutions only, each asserted to occur
exactly once: the supernova / node selection, every output path (into this folder), and the build / run directories
(outside the repository). X54's DES-SN5YR profiles are not refitted: they are loaded from the committed results file through
X54's own REANALYSE path (LGS2 showed the live refit reproduces them exactly), so the Pantheon+ and Union3 profiles start from
the same DES-SN5YR xi = 0 refit as the committed run did.

usage: python3 -I -B lgs3_run.py x54 <PP|U3> <sample>
       python3 -I -B lgs3_run.py cfg689 <TF|TU3F> <sample>
  Pantheon+ samples: full (the loader's own: non-calibrators, zHD > 0.01), zcut (also zHD > 0.0870), legacy_surveys (rows with
                     IDSURVEY 5, 63, 64, 65, 66, 150 dropped at any redshift), rand (size control: as many supernovae as zcut
                     removes, dropped at random from zHD > 0.0870, numpy default_rng(20261114))
  Union3 samples:    full, zcut (the node at z <= 0.0870 marginalised out), node055 (control: the node at z = 0.55 marginalised
                     out, the node above the cut whose M-marginalised conditional precision is closest to the z = 0.05 node's)
kappa = 1/2 FITTED; not theory closed.
"""
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.normpath(os.path.join(HERE, "..", ".."))
EXT = os.path.normpath(os.path.join(REPO, "..", "_external_data"))
X54D = os.path.join(REPO, "rebuild_2026_10_22", "X54_cold_de_exchange")
C689 = os.path.join(REPO, "campaign_fresh_gravity", "CFG689_native_ruler_bao")
X54_BUILD = os.path.join(EXT, "x54_class_build_lgs2")          # LGS2's rebuild of X54's patched CLASS (patch sha d66bbc98)
ZCUT = 0.0870                                                 # top of the Dovekie legacy range
LEGACY = (5, 63, 64, 65, 66, 150)                             # Dovekie's legacy survey codes; Pantheon+ uses the same codes
SEED = 20261114
TARGET, COMP, SAMPLE = sys.argv[1], sys.argv[2], sys.argv[3]
PP_SAMPLES, U3_SAMPLES = ("full", "zcut", "legacy_surveys", "rand"), ("full", "zcut", "node055")
for k in ("X54_MUTATE", "X54_REANALYSE", "X54_SUPP", "X54_BUILD", "CFG689_MODE", "CFG689_PARALLEL"):
    os.environ.pop(k, None)
ACTIVE = [TARGET == "cfg689"]                                 # X54: off during Step 0 (its S0-2 check reads the full Pantheon+)


def LGS_ACTIVATE():
    ACTIVE[0] = True


def LGS_SEL_PP(raw):
    """extra row selection on PantheonPlusSH0ES.dat, combined with the loader's own (IS_CALIBRATOR == 0, zHD > 0.01)"""
    n = len(raw["zHD"])
    if not ACTIVE[0] or SAMPLE == "full":
        return np.ones(n, bool)
    z, ids = raw["zHD"], raw["IDSURVEY"]
    base = (raw["IS_CALIBRATOR"] == 0) & (z > 0.01)
    if SAMPLE == "zcut":
        sel = z > ZCUT
    elif SAMPLE == "legacy_surveys":
        sel = ~np.isin(ids, LEGACY)
    elif SAMPLE == "rand":
        nlow = int((base & (z <= ZCUT)).sum())
        drop = np.random.default_rng(SEED).choice(np.where(base & (z > ZCUT))[0], nlow, replace=False)
        sel = np.ones(n, bool)
        sel[drop] = False
    else:
        raise SystemExit(f"unknown Pantheon+ sample {SAMPLE}")
    print(f"LGS3 Pantheon+ '{SAMPLE}': {int((base & sel).sum())} of {int(base.sum())} kept "
          f"({int((base & sel & (z <= ZCUT)).sum())} at zHD <= {ZCUT}, {int((base & sel & (z > ZCUT)).sum())} above)", flush=True)
    return sel


def LGS_SEL_U3(z, mb, W):
    """Union3 spline nodes: marginalise the dropped nodes (invert the weight matrix, take the covariance sub-block, invert)"""
    if not ACTIVE[0] or SAMPLE == "full":
        return z, mb, W
    if SAMPLE == "zcut":
        keep = z > ZCUT
    elif SAMPLE == "node055":
        keep = np.abs(z - 0.55) > 1e-6
    else:
        raise SystemExit(f"unknown Union3 sample {SAMPLE}")
    assert keep.sum() == len(z) - 1
    Wk = np.linalg.inv(np.linalg.inv(W)[np.ix_(keep, keep)])
    print(f"LGS3 Union3 '{SAMPLE}': {int(keep.sum())} of {len(z)} nodes kept; dropped z = {z[~keep].round(4).tolist()}", flush=True)
    return z[keep], mb[keep], 0.5 * (Wk + Wk.T)


def sub(text, old, new):
    assert text.count(old) == 1, f"expected exactly one occurrence of: {old!r} (found {text.count(old)})"
    return text.replace(old, new)


g = {"__name__": "__main__", "LGS_SEL_PP": LGS_SEL_PP, "LGS_SEL_U3": LGS_SEL_U3, "LGS_ACTIVATE": LGS_ACTIVATE}
if TARGET == "x54":
    assert COMP in ("PP", "U3") and SAMPLE in (PP_SAMPLES if COMP == "PP" else U3_SAMPLES), (COMP, SAMPLE)
    SRC = os.path.join(X54D, "x54_cold_de_exchange.py")
    out = os.path.join(HERE, f"lgs3_x54_{COMP}_{SAMPLE}")
    t = open(SRC).read()
    t = sub(t, '        sel = (raw["IS_CALIBRATOR"] == 0) & (raw["zHD"] > 0.01)\n',
            '        sel = (raw["IS_CALIBRATOR"] == 0) & (raw["zHD"] > 0.01) & LGS_SEL_PP(raw)\n')
    t = sub(t, "        z, mb, W = M_[0, 1:], M_[1:, 0], M_[1:, 1:]\n",
            "        z, mb, W = M_[0, 1:], M_[1:, 0], M_[1:, 1:]\n        z, mb, W = LGS_SEL_U3(z, mb, W)\n")
    t = sub(t, 'BUILD = os.environ.get("X54_BUILD", os.path.join(tempfile.gettempdir(), "x54_class_build"))', "BUILD = LGS_BUILD")
    t = sub(t, 'RUNS = os.path.join(BUILD, f"runs{TAG}")', "RUNS = LGS_RUNS")
    t = sub(t, 'OUTF = open(os.path.join(HERE, f"x54_cold_de_exchange{TAG}.out"), "w")', 'OUTF = open(LGS_OUT + ".out", "w")')
    t = sub(t, 'open(os.path.join(HERE, f"x54_cold_de_exchange_results{TAG}.json"), "w")', 'open(LGS_OUT + ".json", "w")')
    # after Step 0 and the checks (which read the full sets), reload the profile sets with the cut and print their sizes
    t = sub(t, 'P("\\n== profiles (graded chi2 = plik + lowTT + lowEE + Aprior + BAO + SN)")',
            'LGS_ACTIVATE(); SN.update({k_: load_sn(k_) for k_ in LGS_OTHER_SN})\n'
            'P(f"LGS3 profile sets: PP {SN[\'PP\'][\'n\']}, U3 {SN[\'U3\'][\'n\']} (sample {LGS_SAMPLE})")\n'
            'P("\\n== profiles (graded chi2 = plik + lowTT + lowEE + Aprior + BAO + SN)")')
    # DES-SN5YR profiles loaded from the committed results (REANALYSE); the Pantheon+ / Union3 profile is refitted live
    t = sub(t, 'recs2 = load_prev(f"{model}_{sn}") if REAN else profile(', "recs2 = profile(")
    t = sub(t, 'for sn in ("PP", "U3"):', "for sn in LGS_OTHER_SN:")
    os.environ["X54_REANALYSE"] = os.path.join(X54D, "x54_cold_de_exchange_results.json")
    g.update(LGS_BUILD=X54_BUILD, LGS_RUNS=os.path.join(X54_BUILD, f"runs_lgs3_{COMP}_{SAMPLE}"), LGS_OUT=out,
             LGS_OTHER_SN=(COMP,), LGS_SAMPLE=SAMPLE)
elif TARGET == "cfg689":
    assert (COMP, SAMPLE) in [("TF", s) for s in ("full", "zcut")] + [("TU3F", s) for s in ("full", "zcut")], (COMP, SAMPLE)
    SRC = os.path.join(C689, "cfg689_native_ruler.py")
    out = os.path.join(HERE, f"lgs3_cfg689_{COMP}_{SAMPLE}")
    os.environ["CFG689_MODE"] = COMP
    t = open(SRC).read()
    t = sub(t, '    sel = (raw["IS_CALIBRATOR"] == 0) & (raw[cfg["snz"]] > cfg["snzmin"])\n',
            '    sel = (raw["IS_CALIBRATOR"] == 0) & (raw[cfg["snz"]] > cfg["snzmin"]) & LGS_SEL_PP(raw)\n')
    t = sub(t, 'zsn, MB, Wsn = M_[0, 1:], M_[1:, 0], M_[1:, 1:]; zhel = zsn; SNLAB = "Union3 nodes (CFG684 loader)"',
            'zsn, MB, Wsn = M_[0, 1:], M_[1:, 0], M_[1:, 1:]; zsn, MB, Wsn = LGS_SEL_U3(zsn, MB, Wsn); zhel = zsn; SNLAB = "Union3 nodes (CFG684 loader)"')
    t = sub(t, 'OUTF = open(os.path.join(HERE, f"cfg689{TAG}.out"), "w")', 'OUTF = open(LGS_OUT + ".out", "w")')
    t = sub(t, 'open(os.path.join(HERE, f"cfg689{TAG}.json"), "w")', 'open(LGS_OUT + ".json", "w")')
    g["LGS_OUT"] = out
else:
    sys.exit(f"unknown target {TARGET}")

g["__file__"] = SRC
exec(compile(t, SRC, "exec"), g)
