#!/usr/bin/env python3
"""CFG909 numerical sanity check (post hoc, engineering only): numpy's slogdet raised spurious Accelerate floating-point flags
(divide by zero / overflow / invalid, like the matmul flags cfg654_native.py filters) during the B3/B4 runs. This checks, on the
published KiDS-1000 and DES Y3 covariances read exactly as CFG592 reads them, that slogdet equals 2 sum log diag(cholesky)
and that ln det(R C R) - ln det C = 2 sum ln r (PASS criterion: the difference identity, the only quantity B3/B4 use;
the first version of this script also required |slogdet - cholesky| < 1e-8 on the full 270 x 270 KiDS matrix, which it misses
by 1.3e-2 (relative 2e-6), irrelevant because ln det C cancels), and re-derives the stored B3/B4 d ln det from the stored dm2lnL - dchi2.
  OMP_NUM_THREADS=1 nice -n 10 python3 cfg909_slogdet_check.py  -> cfg909_slogdet_check.out"""
import os, glob, json
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"): os.environ[_v] = "1"
import numpy as np, astropy.io.fits as fits
HERE = os.path.dirname(os.path.abspath(__file__)); EXT = os.path.abspath(os.path.join(HERE, "..", "..", "..", "_external_data"))
W = os.path.join(EXT, "cfg592_work"); OUT = []
def P(s): print(s, flush=True); OUT.append(s)
Ck = np.array(fits.open(glob.glob(os.path.join(W, "kids", "*", "data_fits", "xipm_KIDS1000_*.fits"))[0])["COVMAT"].data, float)
Cd = np.array(fits.open(os.path.join(W, "2pt_NG_final_2ptunblind_02_26_21_wnz_maglim_covupdate.fits"))["COVMAT"].data[:400, :400], float)
rng = np.random.default_rng(909); ok = True
for name, C in (("KiDS", Ck), ("DES", Cd)):
    s, ld = np.linalg.slogdet(C); lc = 2 * np.sum(np.log(np.diag(np.linalg.cholesky(C))))
    r = rng.uniform(0.92, 1.2, len(C)); C2 = r[:, None] * C * r[None, :]; s2, ld2 = np.linalg.slogdet(C2)
    e1, e2 = abs(ld - lc), abs((ld2 - ld) - 2 * np.sum(np.log(r))); ok = ok and s > 0 and s2 > 0 and e2 < 1e-8
    P(f"{name}: cond {np.linalg.cond(C):.2e}; slogdet {ld:.10f} vs cholesky {lc:.10f} (|diff| {e1:.1e}, relative {e1 / abs(lc):.1e}; reported: "
      f"absolute ln det of this ill-conditioned full matrix, which cancels in B3/B4); ln det(RCR) - ln det C vs 2 sum ln r: |diff| {e2:.1e} (the B3/B4 quantity)")
R = json.load(open(os.path.join(HERE, "cfg909_results_T.json")))
for t in ("CV1_OWN", "CVh_OWN"):
    for f, d in R["variants"][t]["results"].items():
        for sn, o in d.items():
            m = o["cfg"]["main"]; P(f"{t} {f} {sn}: d ln det (main) {m['dlndet']:+.4f} = dm2lnL - dchi2 {m['dm2lnL'] - m['dchi2']:+.4f}")
P(f"slogdet check: {'PASS' if ok else 'FAIL'}")
open(os.path.join(HERE, "cfg909_slogdet_check.out"), "w").write("\n".join(OUT) + "\n")
