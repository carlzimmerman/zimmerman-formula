"""LGS4 checks made BEFORE the criteria are frozen. None of them fits a supernova sample.
 K1  early-universe numbers against CAMB at one constant-dark-energy point (100 theta*, r_drag, z*, z_drag).
 K2  the compressed CMB summary alone, flat constant dark energy: H0 against the 67.19 +- 0.38 km/s/Mpc that
     arXiv:2610.23657 quotes for SPT-3G + ACT DR6 + Planck.
 K3  DESI DR2 BAO + the BBN prior, flat constant dark energy: Omega_m against DESI's own 0.2975 +- 0.0086.
 K4  supernova bookkeeping only: row counts per sample, and the chi2 of the full sample at one fixed, arbitrary point
     computed two ways (the class, and the official likelihood's formula written out). No minimisation."""
import json, os, sys
import numpy as np
import lgs4_like as L
import lgs4_fit as F

out = {}
def P(*a):
    print(*a, flush=True)

# ---- K1 ----
import camb
h, wb, wc = 0.6720, 0.02240, 0.14265 - 0.02240
pars = camb.set_params(H0=100 * h, ombh2=wb, omch2=wc, mnu=0.06, num_massive_neutrinos=2, neutrino_hierarchy="normal",
                       nnu=3.044, TCMB=L.T_CMB, tau=0.055, As=2.1e-9, ns=0.965)
der = camb.get_results(pars).get_derived_params()
obc = (wb + wc) / h ** 2
rs, rd, zs, zd = L.early(h, obc, wb, -1.0, 0.0)
D, H = L.dc_grid(h, obc, wb, -1.0, 0.0)
th = 100 * rs / np.interp(np.log1p(zs), L._XG, D)
k1 = dict(theta100=(float(th), float(der["thetastar"])), rdrag=(float(rd), float(der["rdrag"])), rstar=(float(rs), float(der["rstar"])),
          zstar=(float(zs), float(der["zstar"])), zdrag=(float(zd), float(der["zdrag"])))
for k, (a, b) in list(k1.items()):
    P(f"K1 {k:9s} here {a:.5f}  CAMB {b:.5f}  rel diff {a / b - 1:+.2e}")
P(f"K1 theta* difference in units of the CMB summary's sigma (0.000232): {(k1['theta100'][0] - k1['theta100'][1]) / np.sqrt(L.C_CMB[0, 0]):+.2f} (different z* definitions; see K1b and K2)")
# like for like: the same integrals evaluated at CAMB's own z* and z_drag (CAMB's z* is optical depth 1; the paper's
# fit follows CLASS's recombination redshift, about 1.1 lower, and the CMB summary is defined with that one)
a_s, a_d = 1 / (1 + der["zstar"]), 1 / (1 + der["zdrag"])
rs_c = L.sound_horizon(a_s, h, obc, wb, -1.0, 0.0); rd_c = L.sound_horizon(a_d, h, obc, wb, -1.0, 0.0)
th_c = 100 * rs_c / np.interp(np.log1p(der["zstar"]), L._XG, D)
k1["at_camb_redshifts"] = dict(rstar=(float(rs_c), float(der["rstar"])), rdrag=(float(rd_c), float(der["rdrag"])), theta100=(float(th_c), float(der["thetastar"])))
for k, (a, b) in k1["at_camb_redshifts"].items():
    P(f"K1b {k:9s} at CAMB's redshift: here {a:.5f}  CAMB {b:.5f}  rel diff {a / b - 1:+.2e}")
P(f"K1b theta* difference at CAMB's z*, in units of the CMB summary's sigma: {(th_c - der['thetastar']) / np.sqrt(L.C_CMB[0, 0]):+.2f}")
out["K1"] = k1

# ---- K2 ----
use = ("cmb",)
f = lambda q: L.chi2_total(np.r_[q, -1.0, 0.0], None, use) if L.in_prior(np.r_[q, -1.0, 0.0], lcdm=True) else 1e30
b = F.best_fit(f, [[0.67, 0.315, 0.0224], [0.68, 0.30, 0.0223]])
cov = F.laplace_cov(f, b.x, [2e-3, 2e-3, 5e-5])
ch, info = F.metropolis(f, lambda q: L.in_prior(np.r_[q, -1.0, 0.0], lcdm=True), b.x, cov, 30000, seed=11)
H0 = 100 * ch[:, 0]
out["K2"] = dict(best=b.x.tolist(), chi2=float(b.fun), H0_mean=float(H0.mean()), H0_sd=float(H0.std()), laplace_sd=float(100 * np.sqrt(cov[0, 0])), mcmc=info,
                 ref=[67.19, 0.38])
P(f"K2 CMB summary alone, constant dark energy: H0 = {H0.mean():.3f} +- {H0.std():.3f} (Laplace sd {100 * np.sqrt(cov[0, 0]):.3f}); "
  f"quoted 67.19 +- 0.38; chi2_min {b.fun:.2e}; R-1 max {max(info['rhat_minus_1']):.4f}")

# ---- K3 ----
use = ("bao", "bbn")
f = lambda q: L.chi2_total(np.r_[q, -1.0, 0.0], None, use) if L.in_prior(np.r_[q, -1.0, 0.0], lcdm=True) else 1e30
b = F.best_fit(f, [[0.68, 0.297, 0.0219], [0.70, 0.31, 0.0220]])
cov = F.laplace_cov(f, b.x, [2e-3, 2e-3, 5e-5])
o = L.parts(np.r_[b.x, -1.0, 0.0], None, use)
out["K3"] = dict(best=b.x.tolist(), chi2=float(b.fun), om=float(o["om"]), om_sd=float(np.sqrt(cov[1, 1])), H0=float(100 * b.x[0]), H0_sd=float(100 * np.sqrt(cov[0, 0])),
                 rd=float(o["rd"]), ref_om=[0.2975, 0.0086])
P(f"K3 BAO + BBN, constant dark energy: Omega_m = {o['om']:.4f} +- {np.sqrt(cov[1, 1]):.4f} (DESI DR2: 0.2975 +- 0.0086); "
  f"H0 = {100 * b.x[0]:.2f} +- {100 * np.sqrt(cov[0, 0]):.2f}; r_d = {o['rd']:.2f} Mpc; chi2_min {b.fun:.2f} (13 points, 2 shape parameters)")

# ---- K4 ----
k4 = {}
for s in ("full", "des_only", "rand197"):
    sn = L.SN(s); k4[s] = dict(n=sn.n, n_des=sn.n_des, n_legacy=sn.n_leg, zmin=float(sn.z.min()), zmax=float(sn.z.max()))
    P(f"K4 sample {s:9s}: {sn.n} supernovae ({sn.n_des} DES, {sn.n_leg} legacy), z {sn.z.min():.4f}-{sn.z.max():.4f}")
sn = L.SN("full")
p = np.array([0.70, 0.30, 0.0224, -1.0, 0.0]); D, H = L.dc_grid(*p)
c1 = sn.chi2(D)
rows = [l.split() for l in open(os.path.join(L.IN, "des5", "DES-Dovekie_HD.csv")) if l.startswith("SN:")]
z = np.array([float(r[3]) for r in rows]); zh = np.array([float(r[4]) for r in rows]); mu = np.array([float(r[5]) for r in rows])
npz = np.load(os.path.join(L.IN, "des5", "STAT+SYS.npz")); n = int(npz[npz.files[0]][0]); W = np.zeros((n, n)); W[np.triu_indices(n)] = npz[npz.files[1]]
il = np.tril_indices(n, -1); W[il] = W.T[il]
DA = np.interp(np.log1p(z), L._XG, D) / (1 + z)
delta = 5 * np.log10((1 + z) * (1 + zh) * DA) + 25 - mu
c2 = float(delta @ W @ delta - (delta @ W).sum() ** 2 / W.sum())
k4["chi2_fixed_point"] = dict(class_method=float(c1), official_formula=c2, diff=float(c1 - c2))
P(f"K4 chi2 of the full sample at the fixed point (h 0.70, Omega_bc 0.30, w = -1): class {c1:.4f}, official formula {c2:.4f}, diff {c1 - c2:+.2e}")
out["K4"] = k4
json.dump(out, open(os.path.join(L.HERE, "lgs4_prefreeze_checks.json"), "w"), indent=1)
