"""LGS4 POST HOC repair of the sampler (written after the frozen run failed its own gate G0; not frozen).

What failed: in the four CPL runs the numerical Hessian of lgs4_run.py (fixed steps per parameter) was not positive
definite along the w0-wa degeneracy, so the chains fell back to a diagonal proposal, accepted 1.7 % of steps, and two
of them missed R - 1 < 0.01. The constant-dark-energy runs were fine.

What changes here, and nothing else:
  - the proposal covariance is the covariance of the frozen run's own chain (a second pass);
  - the Hessian is taken in coordinates whitened by that covariance, with steps of 0.25 sd;
  - the best fit is polished again from the frozen best fit and from the frozen chain mean (the lower chi2 is kept).
Same likelihood, data, samples, models, priors, step count and burn-in. Outputs go to lgs4_posthoc_<sample>_<model>.*

usage: python3 lgs4_posthoc_run.py <sample> <model>"""
import json, os, sys
import numpy as np
import lgs4_like as L
import lgs4_fit as F

SAMPLE, MODEL = sys.argv[1], sys.argv[2]
assert SAMPLE in ("full", "des_only", "rand197") and MODEL in ("cpl", "lcdm", "cpl_dm", "lcdm_dm")
NSTEP = 60000
FRO = json.load(open(os.path.join(L.HERE, f"lgs4_{SAMPLE}_{MODEL}.json")))
TAG = f"lgs4_posthoc_{SAMPLE}_{MODEL}"
OUTF = open(os.path.join(L.HERE, TAG + ".out"), "w")
def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); OUTF.write(s + "\n"); OUTF.flush()

sn = L.SN(SAMPLE)
LCDM, DM = MODEL.startswith("lcdm"), MODEL.endswith("_dm")
NAMES = ["h", "obc", "wb"] + ([] if LCDM else ["w0", "wa"]) + (["dm"] if DM else [])
assert NAMES == FRO["names"]
k = len(NAMES)
def full_p(q):
    q = np.asarray(q, float)
    base = np.r_[q[:3], -1.0, 0.0] if LCDM else q[:5]
    return np.r_[base, q[-1]] if DM else base
def chi2(q):
    p = full_p(q)
    return L.chi2_total(p, sn) if L.in_prior(p, lcdm=LCDM) else 1e30
inpr = lambda q: L.in_prior(full_p(q), lcdm=LCDM)

P(f"LGS4 POST HOC {TAG}: {sn.n} supernovae ({sn.n_des} DES, {sn.n_leg} legacy); parameters {NAMES}; NSTEP {NSTEP}")
C0 = np.array(FRO["chain"]["cov"])[:k, :k]
bf = F.best_fit(chi2, [FRO["best"]["x"], FRO["chain"]["mean"][:k]])
x, f = (bf.x, float(bf.fun)) if bf.fun <= FRO["best"]["chi2"] else (np.array(FRO["best"]["x"]), float(FRO["best"]["chi2"]))
P(f"best fit chi2 {f:.4f} (frozen run {FRO['best']['chi2']:.4f}; difference {f - FRO['best']['chi2']:+.2e})")
Lc = np.linalg.cholesky(C0); Li = np.linalg.inv(Lc)
Hu = F.hessian(lambda u: chi2(x + Lc @ u), np.zeros(k), [0.25] * k)
cov_l = 2 * np.linalg.inv(Li.T @ Hu @ Li)
ok_l = bool(np.all(np.linalg.eigvalsh(cov_l) > 0))
pb = full_p(x); o = L.parts(pb, sn)
P("best fit: " + "  ".join(f"{n} {v:.5f}" for n, v in zip(NAMES, x)))
P("chi2 by probe: " + "  ".join(f"{kk} {o[kk]:.3f}" for kk in L.PROBES) + f"   Omega_m {o['om']:.4f}  H0 {100 * pb[0]:.3f}  r_d {o['rd']:.3f}  100theta* {o['theta100']:.5f}")
P("Laplace sd: " + "  ".join(f"{n} {np.sqrt(abs(cov_l[i, i])):.5f}" for i, n in enumerate(NAMES)) + f"   positive definite: {ok_l}")
seed = 20261114 + 100 + 10 * ("full", "des_only", "rand197").index(SAMPLE) + ("cpl", "lcdm", "cpl_dm", "lcdm_dm").index(MODEL)
ch, info = F.metropolis(chi2, inpr, x, C0, NSTEP, seed=seed)
om = ch[:, 1] + L.OMEGA_NU / ch[:, 0] ** 2; H0 = 100 * ch[:, 0]
ext = np.c_[ch, om, H0]; XN = NAMES + ["om", "H0"]
mean, cov = ext.mean(axis=0), np.cov(ext.T)
q = np.percentile(ext, [16, 50, 84], axis=0)
P(f"chains: acceptance {np.round(info['acceptance'], 3).tolist()}  max R-1 {max(info['rhat_minus_1']):.4f}  kept {len(ch)}")
for i, n in enumerate(XN):
    P(f"   {n:4s} mean {mean[i]:+.5f}  sd {np.sqrt(cov[i, i]):.5f}  median {q[1, i]:+.5f}  68% [{q[0, i]:+.5f}, {q[2, i]:+.5f}]")
res = dict(sample=SAMPLE, model=MODEL, posthoc=True, nstep=NSTEP, frozen_nstep=60000, n_sn=sn.n, n_des=sn.n_des, n_legacy=sn.n_leg, names=NAMES,
           best=dict(x=x.tolist(), chi2=f, parts={kk: float(o[kk]) for kk in L.PROBES}, om=float(o["om"]), H0=float(100 * pb[0]),
                     rd=float(o["rd"]), theta100=float(o["theta100"])),
           laplace=dict(cov=cov_l.tolist(), positive_definite=ok_l),
           chain=dict(names=XN, mean=mean.tolist(), cov=cov.tolist(), q16=q[0].tolist(), q50=q[1].tolist(), q84=q[2].tolist(), n=int(len(ch)), **info))
json.dump(res, open(os.path.join(L.HERE, TAG + ".json"), "w"), indent=1)
work = os.path.normpath(os.path.join(L.REPO, "..", "_external_data", "lgs4_work")); os.makedirs(work, exist_ok=True)
np.savez_compressed(os.path.join(work, TAG + "_chain_thin20.npz"), chain=ext[::20], names=np.array(XN))
