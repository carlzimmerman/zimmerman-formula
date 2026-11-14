"""LGS4 run: one supernova sample, one model. Best fit, chi2 by probe, Laplace covariance, four Metropolis chains.

usage: python3 lgs4_run.py <sample> <model>
  sample: full | des_only | rand197        (as LGS1; rand197 uses LGS1's seed)
  model:  cpl      (h, Omega_bc, omega_b, w0, wa)
          lcdm     (h, Omega_bc, omega_b; w0 = -1, wa = 0: constant dark energy)
          cpl_dm   cpl  + a free magnitude offset on the legacy rows
          lcdm_dm  lcdm + the same offset
Writes lgs4_<sample>_<model>.json and .out in this folder; thinned chains go outside the repo."""
import json, os, sys
import numpy as np
import lgs4_like as L
import lgs4_fit as F

SAMPLE, MODEL = sys.argv[1], sys.argv[2]
assert SAMPLE in ("full", "des_only", "rand197") and MODEL in ("cpl", "lcdm", "cpl_dm", "lcdm_dm")
NSTEP = int(os.environ.get("LGS4_NSTEP", "60000")); FROZEN_NSTEP = 60000
TAG = f"lgs4_{SAMPLE}_{MODEL}"
OUTF = open(os.path.join(L.HERE, TAG + ".out"), "w")
def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); OUTF.write(s + "\n"); OUTF.flush()

sn = L.SN(SAMPLE)
if MODEL.endswith("_dm"): assert sn.n_leg > 0, "the offset needs legacy rows"
LCDM, DM = MODEL.startswith("lcdm"), MODEL.endswith("_dm")
NAMES = ["h", "obc", "wb"] + ([] if LCDM else ["w0", "wa"]) + (["dm"] if DM else [])
def full_p(q):
    q = np.asarray(q, float)
    base = np.r_[q[:3], -1.0, 0.0] if LCDM else q[:5]
    return np.r_[base, q[-1]] if DM else base
def chi2(q):
    p = full_p(q)
    return L.chi2_total(p, sn) if L.in_prior(p, lcdm=LCDM) else 1e30
inpr = lambda q: L.in_prior(full_p(q), lcdm=LCDM)

P(f"LGS4 {TAG}: {sn.n} supernovae ({sn.n_des} DES, {sn.n_leg} legacy); parameters {NAMES}; NSTEP {NSTEP}"
  + ("" if NSTEP == FROZEN_NSTEP else f"  (NOT the frozen {FROZEN_NSTEP}: no verdict weight)"))
base = [[0.674, 0.310, 0.0223], [0.680, 0.300, 0.0224], [0.670, 0.316, 0.0222]]
shape = [[]] if LCDM else [[-0.80, -0.75], [-1.00, 0.00], [-0.60, -1.30]]
off = [[0.0], [0.05]] if DM else [[]]
starts = [b + s + o for b in base for s in shape for o in off]
bf = F.best_fit(chi2, starts)
pb = full_p(bf.x); o = L.parts(pb, sn)
steps = [F.STEP[n] for n in NAMES]
cov_l = F.laplace_cov(chi2, bf.x, steps)
ok_l = bool(np.all(np.linalg.eigvalsh(cov_l) > 0))
P(f"best fit: " + "  ".join(f"{n} {v:.5f}" for n, v in zip(NAMES, bf.x)) + f"   chi2 {bf.fun:.4f}")
P("chi2 by probe: " + "  ".join(f"{k} {o[k]:.3f}" for k in L.PROBES) + f"   Omega_m {o['om']:.4f}  H0 {100 * pb[0]:.3f}  r_d {o['rd']:.3f}  100theta* {o['theta100']:.5f}")
P(f"Laplace sd: " + "  ".join(f"{n} {np.sqrt(cov_l[i, i]):.5f}" for i, n in enumerate(NAMES)) + f"   positive definite: {ok_l}")
if not ok_l:
    cov_l = np.diag(np.array(steps) ** 2) * 4
seed = 20261114 + 10 * ("full", "des_only", "rand197").index(SAMPLE) + ("cpl", "lcdm", "cpl_dm", "lcdm_dm").index(MODEL)
ch, info = F.metropolis(chi2, inpr, bf.x, cov_l, NSTEP, seed=seed)
om = ch[:, 1] + L.OMEGA_NU / ch[:, 0] ** 2; H0 = 100 * ch[:, 0]
ext = np.c_[ch, om, H0]; XN = NAMES + ["om", "H0"]
mean, cov = ext.mean(axis=0), np.cov(ext.T)
q = np.percentile(ext, [16, 50, 84], axis=0)
P(f"chains: acceptance {np.round(info['acceptance'], 3).tolist()}  max R-1 {max(info['rhat_minus_1']):.4f}  kept {len(ch)}")
for i, n in enumerate(XN):
    P(f"   {n:4s} mean {mean[i]:+.5f}  sd {np.sqrt(cov[i, i]):.5f}  median {q[1, i]:+.5f}  68% [{q[0, i]:+.5f}, {q[2, i]:+.5f}]")
res = dict(sample=SAMPLE, model=MODEL, nstep=NSTEP, frozen_nstep=FROZEN_NSTEP, n_sn=sn.n, n_des=sn.n_des, n_legacy=sn.n_leg, names=NAMES,
           best=dict(x=bf.x.tolist(), chi2=float(bf.fun), parts={k: float(o[k]) for k in L.PROBES}, om=float(o["om"]), H0=float(100 * pb[0]),
                     rd=float(o["rd"]), theta100=float(o["theta100"])),
           laplace=dict(cov=cov_l.tolist(), positive_definite=ok_l),
           chain=dict(names=XN, mean=mean.tolist(), cov=cov.tolist(), q16=q[0].tolist(), q50=q[1].tolist(), q84=q[2].tolist(), n=int(len(ch)), **info))
json.dump(res, open(os.path.join(L.HERE, TAG + ".json"), "w"), indent=1)
work = os.path.normpath(os.path.join(L.REPO, "..", "_external_data", "lgs4_work")); os.makedirs(work, exist_ok=True)
np.savez_compressed(os.path.join(work, TAG + "_chain_thin20.npz"), chain=ext[::20], names=np.array(XN))
