"""AGB2R Part J fits: AGB1's Part A model at fixed amplitude A with q0 = 0 imposed (t) and with q(z) >= 0 imposed on
0 <= z <= 2.33 (n), using AGB1's fitter and starts (agb1_run.py, imported unchanged). Also the KJ re-fits of f at A = 0, 1.
Reads no Pantheon+ magnitude; the host term is combined in agb2r_collect.py.

Usage: python3 agb2r_joint.py SAMPLE      (SAMPLE = full or des_only) -> agb2r_J_<SAMPLE>.json
"""
import json, os, sys, time
for _v in ("VECLIB_MAXIMUM_THREADS", "OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ.setdefault(_v, "2")
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.normpath(os.path.join(HERE, "..", ".."))
AGB1 = os.path.join(REPO, "closure_2026_11_13", "AGB1_progenitor_age_bias")
sys.path.insert(0, AGB1)
_argv = sys.argv; sys.argv = [_argv[0], "import"]
import agb1_run as A1                                    # unchanged; its module-level MODE reads argv[1]
sys.argv = _argv

GRID_T = [round(x, 2) + 0.0 for x in np.arange(-1.0, 2.0001, 0.1)]
GRID_N = [round(x, 2) + 0.0 for x in np.arange(-1.0, 2.0001, 0.25)]
KEEP = ("chi2", "chi2_bao", "chi2_sn", "Om", "w0", "wa", "q0", "qmin", "z_qmin", "hrd", "edge", "x3", "con")


def slim(d):
    return {k: d[k] for k in KEEP if k in d}


def main():
    sample = sys.argv[1]; t0 = time.time(); log = lambda m: print(m, flush=True)
    com = json.load(open(os.path.join(AGB1, f"agb1_A_{sample}.json")))
    prof = {float(k): v for k, v in com["profile"].items()}; free = com["free"]
    sn = A1.SN(sample); bao = A1.BAO("all"); sn.add_template("age", A1.TPL.T(sn.z, "S"))
    F = A1.Fitter("A", sn, bao)
    log(f"AGB2R Part J fits on AGB1 sample {sample}: {sn.n} supernovae; BAO {bao.names}; template T_S")
    res = dict(sample=sample, n_sn=sn.n)
    # KJ: f re-fitted at A = 0 and 1 the way AGB1's profile was (fixed starts + previous grid point + the A-free fit)
    kj = {}
    for a in (0.0, 1.0):
        prev = prof[round(a - 0.1, 2) + 0.0]
        r = F.fit({"age": a}, [], extra=(prev, free))
        kj[f"{a:+.2f}"] = dict(refit=r["chi2"], committed=prof[a]["chi2"], diff=r["chi2"] - prof[a]["chi2"])
        log(f"KJ re-fit f(A={a:+.1f}) {r['chi2']:.6f}  committed {prof[a]['chi2']:.6f}  diff {r['chi2'] - prof[a]['chi2']:+.2e}")
    res["KJ_refit"] = kj
    # t(A): q0 = 0, started as AGB1's forks (fixed starts + the free fit at that A)
    T = {}
    for a in GRID_T:
        r = F.fit({"age": a}, [], "today", extra=(prof[a],)); T[a] = r
        log(f"t  A {a:+.2f}  chi2 {r['chi2']:10.4f}  (f {prof[a]['chi2']:10.4f}; t - f {r['chi2'] - prof[a]['chi2']:8.3f})"
            f"  Om {r['Om']:.4f} w0 {r['w0']:+.4f} wa {r['wa']:+.4f}  edge {r['edge']}")
    # n(A): never accelerated, started as AGB1's forks (fixed NEVER starts + the q0 = 0 fit + the free fit at that A)
    N = {}; bases = {}
    for a in GRID_N:
        if a in prof:
            base = prof[a]
        else:                                           # off the committed 0.1 grid: free fit started from both neighbours
            lo, hi = np.floor(a*10)/10, np.ceil(a*10)/10
            base = F.fit({"age": a}, [], extra=(prof[round(lo, 2) + 0.0], prof[round(hi, 2) + 0.0])); bases[a] = slim(base)
        today = T[a] if a in T else F.fit({"age": a}, [], "today", extra=(base,))
        r = F.fit({"age": a}, [], "never", extra=(today, base)); N[a] = r
        log(f"n  A {a:+.2f}  chi2 {r['chi2']:10.4f}  (free at A {base['chi2']:10.4f}; n - f {r['chi2'] - base['chi2']:8.3f})"
            f"  Om {r['Om']:.4f} w0 {r['w0']:+.4f} wa {r['wa']:+.4f} min q {r['qmin']:+.6f}  edge {r['edge']}")
    res["t"] = {f"{a:+.2f}": slim(v) for a, v in T.items()}
    res["n"] = {f"{a:+.2f}": slim(v) for a, v in N.items()}
    res["offgrid_free"] = {f"{a:+.2f}": v for a, v in bases.items()}
    res["nfit"] = F.nfit; res["seconds"] = round(time.time() - t0, 1)
    with open(os.path.join(HERE, f"agb2r_J_{sample}.json"), "w") as fh: json.dump(res, fh, indent=1, default=float)
    log(f"wrote agb2r_J_{sample}.json ({res['seconds']} s, {F.nfit} fits)")


if __name__ == "__main__":
    main()
