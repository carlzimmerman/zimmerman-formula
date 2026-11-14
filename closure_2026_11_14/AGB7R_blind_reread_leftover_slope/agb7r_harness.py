"""AGB7R (blind re-grade of AGB7): generalised re-read harness for CFG684 and CFG689 (DES5 modes).

The committed lane sources are executed unchanged apart from exact text substitutions, each asserted to occur once:
  - supernova mask  : ww = dz > 0            ->  (dz > 0) & sample mask
  - moduli          : dmu                    ->  dmu - A x T(zHD), on every supernova before the mask
  - output paths    : the lane's own files   ->  this folder (basename agb7r_<target>_<sample>_<tpl>_A<amp>)
  - CFG684 only     : the combination list   ->  ["BAO+DES5+CC", "BAO+DES5"]
Templates: "S" = AGB1's cosmic-average T_S (agb1_template.T(z, "S"), imported unchanged);
           "H" = the sample's own mean-host-age drift from AGB3's agb3_S.json "curves" (full_sfr / des_only_sfr):
                 T_H(z) = 0.030 mag/Gyr x [age(z_1) - age(z)], age linear in zHD between bins, constant beyond them.

usage: python3 -I -B agb7r_harness.py <cfg684|cfg689_D5|cfg689_TD5F> <full|des_only> <A> <S|H> [outdir]
"""
import hashlib, json, os, sys, time
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.normpath(os.path.join(HERE, "..", ".."))
AGB1 = os.path.join(REPO, "closure_2026_11_13", "AGB1_progenitor_age_bias")
AGB3S = os.path.join(REPO, "closure_2026_11_14", "AGB3_des_host_star_formation", "agb3_S.json")
SLOPE = 0.030                                     # mag / Gyr, the slope T_S carries (agb1_template.SLOPE, checked below)

TARGET, SAMPLE, AMP, TPL = sys.argv[1], sys.argv[2], float(sys.argv[3]), sys.argv[4]
OUTDIR = os.path.abspath(sys.argv[5]) if len(sys.argv) > 5 else HERE
assert TARGET in ("cfg684", "cfg689_D5", "cfg689_TD5F"), TARGET
assert SAMPLE in ("full", "des_only"), SAMPLE
assert TPL in ("S", "H"), TPL
assert np.isfinite(AMP), AMP
AMPS = ("%g" % AMP).replace(".", "p").replace("-", "m")
BASE = os.path.join(OUTDIR, f"agb7r_{TARGET}_{SAMPLE}_{TPL}_A{AMPS}")


# ---------------------------------------------------------------- templates
def template_fn():
    if TPL == "S":
        sys.path.insert(0, AGB1)
        import agb1_template as T1
        assert abs(T1.SLOPE - SLOPE) < 1e-15
        return (lambda z: T1.T(np.asarray(z, float), "S")), "AGB1 agb1_template.T(z, 'S')"
    with open(AGB3S) as fh:
        cur = json.load(fh)["curves"][f"{SAMPLE}_sfr"]          # only this key is read
    zb, ab = np.asarray(cur["z"], float), np.asarray(cur["age"], float)
    assert np.all(np.diff(zb) > 0) and len(zb) == len(ab)
    return (lambda z: SLOPE*(ab[0] - np.interp(np.asarray(z, float), zb, ab))), f"AGB3 curves['{SAMPLE}_sfr'] ({len(zb)} bins)"


TFUN, TDESC = template_fn()
LOG = {}


def R7_MASK(rows):
    ids = np.array([int(r[2]) for r in rows])
    keep = np.ones(ids.size, bool) if SAMPLE == "full" else (ids == 10)
    LOG.update(n_rows=int(ids.size), n_sample=int(keep.sum()), n_des=int((keep & (ids == 10)).sum()),
               n_legacy=int((keep & (ids != 10)).sum()))
    print(f"AGB7R sample '{SAMPLE}': {LOG['n_sample']} of {LOG['n_rows']} rows kept "
          f"({LOG['n_des']} DES, {LOG['n_legacy']} legacy) before the zHD > 0 cut", flush=True)
    return keep


def R7_SHIFT(z):
    z = np.asarray(z, float); s = AMP*TFUN(z)
    LOG.update(shift_min=float(s.min()), shift_max=float(s.max()), shift_sha=hashlib.sha256(s.tobytes()).hexdigest()[:16])
    print(f"AGB7R shift: mu -> mu - {AMP:g} x T_{TPL}(zHD) [{TDESC}]; min {s.min():.5f} max {s.max():.5f} mag", flush=True)
    return s


def sub(text, old, new):
    n = text.count(old)
    assert n == 1, f"expected one occurrence, found {n}: {old!r}"
    return text.replace(old, new)


if TARGET == "cfg684":
    SRC = os.path.join(REPO, "campaign_fresh_gravity", "CFG684_bao_cc_sn_robust", "cfg684_robust.py")
    t0 = open(SRC).read(); t = t0
    t = sub(t, "Wd = Wd + np.triu(Wd, 1).T; ww = dz > 0; Cd = np.linalg.inv(Wd)[np.ix_(ww, ww)]",
            "Wd = Wd + np.triu(Wd, 1).T; ww = (dz > 0) & R7_MASK(rows); dmu = dmu - R7_SHIFT(dz); Cd = np.linalg.inv(Wd)[np.ix_(ww, ww)]")
    t = sub(t, 'COMBOS = ["BAO+PP", "BAO+CC", "BAO+PP+CC", "BAO+DES5+CC", "BAO+U3+CC", "BAO+DES5", "BAO+U3"]',
            'COMBOS = ["BAO+DES5+CC", "BAO+DES5"]')
    t = sub(t, 'open(os.path.join(HERE, "cfg684_results" + ("_MUTATE" if MUT else "") + ".json"), "w")',
            'open(R7_BASE + ".json", "w")')
    assert t.count('"w")') == 1
    os.environ.pop("MUTATE", None)
else:
    MODE = TARGET.split("_")[1]
    SRC = os.path.join(REPO, "campaign_fresh_gravity", "CFG689_native_ruler_bao", "cfg689_native_ruler.py")
    assert os.environ.get("CFG689_PARALLEL") == "1", "the criteria run CFG689 with CFG689_PARALLEL=1"
    assert "CFG689_NSTEP" not in os.environ, "the frozen 60,000 steps: CFG689_NSTEP must not be set"
    os.environ["CFG689_MODE"] = MODE
    t0 = open(SRC).read(); t = t0
    t = sub(t, "Wd = Wd + np.triu(Wd, 1).T; ww = dz > 0; Cd = np.linalg.inv(Wd)[np.ix_(ww, ww)]",
            "Wd = Wd + np.triu(Wd, 1).T; ww = (dz > 0) & R7_MASK(rows); dmu = dmu - R7_SHIFT(dz); Cd = np.linalg.inv(Wd)[np.ix_(ww, ww)]")
    t = sub(t, 'OUTF = open(os.path.join(HERE, f"cfg689{TAG}.out"), "w")', 'OUTF = open(R7_BASE + ".out", "w")')
    t = sub(t, 'json.dump(res, open(os.path.join(HERE, f"cfg689{TAG}.json"), "w")', 'json.dump(res, open(R7_BASE + ".json", "w")')
    # the only other write in the source is the P5 branch (MODE == "P5"), never reached in D5 / TD5F
    assert t.count('"w")') == 3 and t.count('"cfg689_P5.json"), "w")') == 1

meta = dict(target=TARGET, sample=SAMPLE, A=AMP, template=TPL, template_desc=TDESC,
            src=os.path.relpath(SRC, REPO), src_sha256=hashlib.sha256(t0.encode()).hexdigest(),
            exec_sha256=hashlib.sha256(t.encode()).hexdigest(),
            T_at={str(z): float(TFUN(z)) for z in (0.01, 0.05, 0.1, 0.2, 0.3, 0.5, 0.7, 1.0, 1.2)},
            numpy=np.__version__, python=sys.version.split()[0],
            threads={k: os.environ.get(k) for k in ("VECLIB_MAXIMUM_THREADS", "OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS")},
            env={k: os.environ.get(k) for k in ("CFG689_PARALLEL", "CFG689_MODE", "CFG689_NSTEP", "MUTATE")},
            started=time.strftime("%Y-%m-%dT%H:%M:%S"))
T0 = time.time()
g = {"__file__": SRC, "__name__": "__main__", "R7_MASK": R7_MASK, "R7_SHIFT": R7_SHIFT, "R7_BASE": BASE}
try:
    exec(compile(t, SRC, "exec"), g)
    meta["exit"] = 0
finally:
    meta.update(LOG, seconds=round(time.time() - T0, 1))
    if "exit" not in meta:
        meta["exit"] = "nonzero (see the runner status)"
    with open(BASE + ".meta.json", "w") as fh:
        json.dump(meta, fh, indent=1)
