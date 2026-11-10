#!/usr/bin/env python3
"""KL1 PART C (FROZEN_CRITERIA_PARTC.md 190161a7f7) C3: Legacy's own mass-dependent alignment model, its prior recovered from the
release's chain. The release is untrusted data: run with python3 -I, the release folder passed as an argument; only text is read.
  Model: A_i = a x f_r,i x 10^(beta (log M_i - 13.5)), f_r,i from KiDS_Legacy_values.ini; (a, beta, log M_1..6) = Lmat u + c0, u
  the decorrelated parameters with unit Gaussian priors about the KiDS_Legacy_priors.ini means.
  KC5 (map): Lmat, c0 solved from the chain's samples (both the decorrelated and the physical columns) reproduce every sample to 1e-6.
  Reported: the prior mean and covariance of (a, beta, log M_i), the per-bin A_i at the prior mean, and the chain's posterior mean
  (context only: a survey posterior).

  OMP_NUM_THREADS=1 python3 -I kl1c_ia.py <release folder>     -> kl1c_ia.json, kl1c_ia.out
kappa = 1/2 FITTED; not theory closed; adopts nothing."""
import os, sys, json, re
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); REL = os.path.abspath(sys.argv[1])
CH = os.path.join(REL, "chains_and_config_files", "xipm", "output_nautilus_xipm_Fiducial.txt")
hdr = open(CH).readline().lstrip("#").split()
names_u = ["intrinsic_alignment_parameters--uncorr_a", "intrinsic_alignment_parameters--uncorr_beta"] + [f"intrinsic_alignment_parameters--uncorr_log10_m_mean_{i}" for i in range(1, 7)]
names_c = ["INTRINSIC_ALIGNMENT_PARAMETERS--A", "INTRINSIC_ALIGNMENT_PARAMETERS--BETA"] + [f"INTRINSIC_ALIGNMENT_PARAMETERS--LOG10_M_MEAN_{i}" for i in range(1, 7)]
cols = [hdr.index(n) for n in names_u + names_c + ["log_weight"]]
X0 = np.loadtxt(CH, usecols=cols, comments="#"); ok = np.all(np.isfinite(X0), 1); X = X0[ok]; U, C, lw = X[:, :8], X[:, 8:16], X[:, 16]   # rows with a non-finite entry dropped (reported)
D = np.c_[U, np.ones(len(U))]; sol, *_ = np.linalg.lstsq(D, C, rcond=None); Lmat = sol[:8].T; c0 = sol[8]
resid = float(np.max(np.abs(D @ sol - C)))
pri = open(os.path.join(REL, "chains_and_config_files", "xipm", "KiDS_Legacy_priors.ini")).read()
keys = ["uncorr_a", "uncorr_beta"] + [f"uncorr_log10_m_mean_{i}" for i in range(1, 7)]
mu_u = np.array([float(re.search(rf"{k}\s*=\s*gaussian\s+(\S+)\s+1\.0", pri).group(1)) for k in keys])
val = open(os.path.join(REL, "chains_and_config_files", "xipm", "KiDS_Legacy_values.ini")).read()
f_r = np.array([float(re.search(rf"f_r_{i}\s*=\s*(\S+)", val).group(1)) for i in range(1, 7)]); lmpiv = float(re.search(r"log10_m_piv\s*=\s*(\S+)", val).group(1))
def amps(p): return (p[0] * f_r * 10 ** (p[1] * (p[2:8] - lmpiv))).tolist()
pm = Lmat @ mu_u + c0; pc = Lmat @ Lmat.T
w = np.exp(lw - lw.max()); w /= w.sum(); post = (w[:, None] * C).sum(0); post_sd = np.sqrt((w[:, None] * (C - post) ** 2).sum(0))
Aw = np.array([amps(c) for c in C]); A_post = (w[:, None] * Aw).sum(0)
RES = dict(lane="KL1", part="C3 alignment prior", criteria="190161a7f7", note="kappa = 1/2 FITTED; not theory closed; the posterior is a survey posterior (context only)",
           f_r=f_r.tolist(), log10_m_piv=lmpiv, mu_u=mu_u.tolist(), Lmat=Lmat.tolist(), c0=c0.tolist(), KC5_map_resid=resid, KC5_map_pass=bool(resid <= 1e-6),
           prior_mean=pm.tolist(), prior_sd=np.sqrt(np.diag(pc)).tolist(), A_i_prior_mean=amps(pm), posterior_mean=post.tolist(), posterior_sd=post_sd.tolist(),
           A_i_posterior_mean=A_post.tolist(), n_samples=int(len(U)), n_dropped_nonfinite=int((~ok).sum()))
OUT = [f"C3 map from {len(U)} chain samples ({int((~ok).sum())} rows with a non-finite entry dropped): max |Lmat u + c0 - physical| {resid:.1e} -> {'PASS' if resid <= 1e-6 else 'FAIL'}; |c0| max {np.max(np.abs(c0)):.1e}",
       "prior mean (a, beta, log M_1..6): " + " ".join(f"{v:.3f}" for v in pm) + "; prior sd: " + " ".join(f"{v:.3f}" for v in np.sqrt(np.diag(pc))),
       "per-bin A_i at the prior mean: " + " ".join(f"{v:.3f}" for v in amps(pm)),
       "posterior mean (context): " + " ".join(f"{v:.3f}" for v in post) + "; per-bin A_i posterior mean: " + " ".join(f"{v:.3f}" for v in A_post)]
print("\n".join(OUT))
json.dump(RES, open(os.path.join(HERE, "kl1c_ia.json"), "w"), indent=1)
open(os.path.join(HERE, "kl1c_ia.out"), "w").write("\n".join(OUT) + "\n")
