#!/usr/bin/env python3
"""
FIRST CRUDE APPLICATION of the eta(beta) MI cluster discriminator
(DOI 10.5281/zenodo.21104820) to real published per-cluster numbers.
Framework footing: a0 = c^2 sqrt(Lambda/32pi) = 9.36e-11 m/s^2 (enters only
through the eta normalization; the SLOPE test is a0-independent).

MI PREDICTION (the note, deep-MOND normalization): G M a0 = eta(beta) sigma^4,
eta: 2.15 (iso) -> 2.8-3.0 (beta 0.3-0.5)  =>  dln(eta)/dbeta ~ +0.75
(band +0.5..+1.0). MG (Milgrom 2014 virial thm: AQUAL/QUMOND/AeST) and
LambdaCDM: eta anisotropy-INDEPENDENT (slope 0).

SIGN MAPPING to observables (derived here, load-bearing):
Under MI-truth with a beta-independent residual dark fraction f_miss,
  sigma^4 = G M_bar f_miss a0 / eta(beta).
(A) empirical etahat = G M_bar a0/sigma^4 = eta(beta)/f_miss -> slope +0.75(deep)
(B) Newtonian MAMPOSSt mass: M_dyn ~ sigma^3 closure (M~sigma^2 r200,
    r200~M^{1/3}) -> ln(M_dyn/M_bar) slope = -(3/4) dln(eta)/dbeta = -0.56(deep)
i.e. MI: more radial => LESS Newtonian-inferred dynamical mass (less boost),
MORE MOND-residual. MG/LCDM: both flat.
DILUTION (unquantified in the note): clusters at r200 sit at g~0.3-1 a0, not
deep MOND; the slope is diluted by a factor ~0.5 (flagged, not computed).

DATA (published, cited):
- beta_sym(r200) + M200(dyn, MAMPOSSt+JEI), 9 CLASH-VLT clusters
  0.19<=z<=0.45: Biviano et al. 2026 A&A (arXiv:2508.05195) Tables 2,3.
  beta_sym = beta/(1-beta/2); 68% intervals.
- Gas: Donahue et al. 2014 ApJ 794,136 (CLASH-X) Chandra Table 4:
  M2500, fg2500=Mgas/M(r2500), r2500.
- Stars: crude M_star = 0.011 M200 (Chiu+18-level), 40% err (~10% of Mbar).

CRUDE steps (flagged): Mgas(r200)=fg2500*M2500*(r200/r2500)^alpha,
alpha=1.1+/-0.2; M200 errors assumed 25% (not tabulated in fetched Table 3);
sigma^4 proxied by (M_dyn E(z))^{4/3}.

BOTH-WAYS controls:
- Biviano+26 report beta correlates with M200/c200 (physical): mass-dependent
  f_gas trends can mimic/mask; partial correlation reported.
- MAMPOSSt fits (M200,beta) jointly: mass-anisotropy degeneracy can induce
  covariance in the ESTIMATES; not removable here.
KILL stated with detection: measured etahat slope <=0 at 3sigma with adequate
power KILLS the MI eta(beta) slide; slope +0.5..+1.0 at 3sigma is
MG/LCDM-impossible.
"""
import numpy as np
from scipy import stats

rng = np.random.default_rng(21104820)

# name,z,Nm,M200dyn(1e14),r200(Mpc),bsym_lo,bsym_hi(68%,r200),M2500,fg2500,r2500
D = [
 ("A209",   0.209, 954, 17.3, 2.31,  0.8, 1.4, 2.49, 0.1100, 0.470),
 ("A383",   0.187, 485,  8.4, 1.83,  0.3, 1.3, 1.42, 0.1070, 0.436),
 ("M0329",  0.450, 262, 11.5, 1.84, -0.5, 1.0, 2.24, 0.1170, 0.460),
 ("M1115",  0.352, 472, 10.7, 1.69, -0.5, 0.4, 3.30, 0.1130, 0.546),
 ("M1206",  0.440, 409, 15.9, 2.06,  0.2, 1.0, 4.59, 0.1220, 0.587),
 ("M1931",  0.352, 250, 11.5, 1.91, -0.1, 1.4, 2.74, 0.1330, 0.511),
 ("MS2137", 0.313, 159,  7.9, 1.70, -0.8, 1.1, 1.78, 0.1205, 0.449),
 ("R2129",  0.234, 248,  7.7, 1.75, -0.9, 0.3, 2.67, 0.1050, 0.529),
 ("R2248",  0.348, 905, 22.7, 2.40,  0.6, 1.4, 7.19, 0.1226, 0.706),
]
names = [d[0] for d in D]
z     = np.array([d[1] for d in D])
M200  = np.array([d[3] for d in D])
r200  = np.array([d[4] for d in D])
bs_lo = np.array([d[5] for d in D]); bs_hi = np.array([d[6] for d in D])
M2500 = np.array([d[7] for d in D])
fg    = np.array([d[8] for d in D])
r2500 = np.array([d[9] for d in D])

bs_mid = 0.5*(bs_lo+bs_hi); bs_sig = 0.5*(bs_hi-bs_lo)
beta_mid = 2*bs_mid/(2+bs_mid)
Ez = np.sqrt(0.3*(1+z)**3 + 0.7)

ALPHA, ALPHA_SIG   = 1.1, 0.2
F_STAR, F_STAR_SIG = 0.011, 0.0045
M200_FRACERR, MGAS_FRACERR = 0.25, 0.10

def observables(m200, m2500, alpha, fstar):
    mgas200 = fg*m2500*(r200/r2500)**alpha
    mbar = mgas200 + fstar*m200
    yA = np.log(mbar) - (4/3)*np.log(m200*Ez)      # ~ ln(etahat) + const
    yB = np.log(m200/mbar)                          # Newtonian Mdyn/Mbar
    return yA, yB, mbar, mgas200

yA0, yB0, Mbar0, Mgas0 = observables(M200, M2500, ALPHA, F_STAR)

print("CRUDE eta(beta) FIRST APPLICATION -- 9 CLASH-VLT clusters (2026 data)")
print(f"{'cluster':8s} {'beta(r200)':>10s} {'M200dyn':>8s} {'Mgas200':>8s} "
      f"{'Mbar200':>8s} {'MdynN/Mbar':>10s}")
for i, n in enumerate(names):
    print(f"{n:8s} {beta_mid[i]:10.2f} {M200[i]:8.1f} {Mgas0[i]:8.2f} "
          f"{Mbar0[i]:8.2f} {M200[i]/Mbar0[i]:10.2f}")
fb = np.median(Mbar0/M200)
print(f"median f_bar(r200) = {fb:.3f} (sane: 0.10-0.16; Newtonian ratio "
      f"{1/fb:.1f} ~ cosmic 1/f_b=6.3, i.e. the usual cluster budget)")

# ---- Monte-Carlo slopes ----------------------------------------------------
NMC = 20000
slA = np.empty(NMC); slB = np.empty(NMC); sp = np.empty(NMC)
for k in range(NMC):
    bs = rng.normal(bs_mid, bs_sig); beta = 2*bs/(2+bs)
    m200 = M200*np.exp(rng.normal(0, M200_FRACERR, 9))
    m25  = M2500*np.exp(rng.normal(0, MGAS_FRACERR, 9))
    al   = rng.normal(ALPHA, ALPHA_SIG)
    fs   = max(rng.normal(F_STAR, F_STAR_SIG), 0.002)
    yA, yB, _, _ = observables(m200, m25, al, fs)
    A = np.vstack([beta, np.ones(9)]).T
    slA[k] = np.linalg.lstsq(A, yA, rcond=None)[0][0]
    slB[k] = np.linalg.lstsq(A, yB, rcond=None)[0][0]
    sp[k]  = stats.spearmanr(beta, yA).statistic

qA = np.percentile(slA, [16, 50, 84]); qB = np.percentile(slB, [16, 50, 84])
eA = 0.5*(qA[2]-qA[0]); eB = 0.5*(qB[2]-qB[0])
print(f"\n(A) dln(etahat)/dbeta      = {qA[1]:+.2f} +/- {eA:.2f}"
      f"   [MI deep +0.75 (band +0.5..+1.0); diluted ~+0.4; MG/LCDM 0]")
print(f"    P(slope>0) = {np.mean(slA>0):.3f}, Spearman med {np.median(sp):+.2f}")
print(f"(B) dln(MdynN/Mbar)/dbeta  = {qB[1]:+.2f} +/- {eB:.2f}"
      f"   [MI deep -0.56; diluted ~-0.3; MG/LCDM 0]")
for tag, s, e, mi_deep, mi_dil in [("A", qA[1], eA, 0.75, 0.4),
                                   ("B", qB[1], eB, -0.56, -0.3)]:
    print(f"    ({tag}) tension: vs MI-deep {abs(s-mi_deep)/e:.1f} sig, "
          f"vs MI-diluted {abs(s-mi_dil)/e:.1f} sig, vs flat "
          f"{abs(s)/e:.1f} sig")

# ---- confound --------------------------------------------------------------
def partial(x, y, c):
    rxy = stats.pearsonr(x, y).statistic; rxc = stats.pearsonr(x, c).statistic
    ryc = stats.pearsonr(y, c).statistic
    return (rxy - rxc*ryc)/np.sqrt((1 - rxc**2)*(1 - ryc**2))
print(f"\nCONFOUND: Spearman(beta, lnM200) = "
      f"{stats.spearmanr(beta_mid, np.log(M200)).statistic:+.2f} "
      "(Biviano+26: massive clusters more radial -- physical)")
print(f"partial corr(yA, beta | lnM200) = "
      f"{partial(yA0, beta_mid, np.log(M200)):+.2f}; "
      f"partial corr(yB, beta | lnM200) = "
      f"{partial(yB0, beta_mid, np.log(M200)):+.2f} (central values)")

# ---- N_clusters forecast for 3 sigma on projection (A) ---------------------
TRUE = 0.75  # deep normalization; halve for diluted
for tag, sy, sberr, sb in [("today, CLASH-VLT-like (150-950 mem)", .45, .30, .25),
                           ("CHANCES-era (>1000 mem/cluster)",     .35, .12, .25)]:
    lam = sb**2/(sb**2 + sberr**2)
    seff2 = sy**2 + (TRUE*sberr)**2
    sbobs2 = sb**2 + sberr**2
    for lbl, tr in [("deep +0.75", TRUE), ("diluted +0.40", 0.40)]:
        N3 = seff2*(3/(lam*tr))**2/sbobs2
        print(f"N for 3sigma [{tag}; {lbl}]: {int(np.ceil(N3))} clusters")

print("\nKILL: etahat slope <= 0 at 3sigma with adequate N kills the MI "
      "eta(beta) slide.\nDETECT: +0.5..+1.0 at 3sigma is MG/LCDM-impossible "
      "(Milgrom 2014 PRD 89,024016 virial universality).")
