#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
h34_h35_h38_milky_way.py -- HUNT ITEMS 34, 35, 38.  The Milky Way, three lever arms, one mass model.
=====================================================================================================
Three items from predictions_2026/SECOND_LAW_HUNT_2026.md that all interrogate the same object at three
radii, so they share one validated baryonic model, one kernel and one set of checks:

  ITEM 34  K_z(R), the RADIAL run of the vertical force at |z| = 1.1 kpc.  The framework has no halo, so
           K_z is fixed by the baryonic column times the kernel's local boost nu(|g_N|/a_0).  g_N falls
           outward, so nu RISES outward, and the predicted K_z(R) must fall with a LONGER scale length
           than the baryons themselves.  Nothing is free.  LambdaCDM does the same job with a round halo
           whose column at 1.1 kpc is nearly flat in R, at the cost of one fitted normalisation.
  ITEM 35  the claimed Keplerian decline of the outer rotation curve.  MOND with no external field cannot
           decline much; the question the list asks is whether an external field of the size the Milky Way
           actually has (e_N <~ 0.05 from M31 and large-scale structure) produces the observed decline, or
           whether a liability has to be recorded.
  ITEM 38  halo-star dynamics beyond 50 kpc.  There the Galaxy is effectively a point mass, so the
           framework predicts M_dyn(<r) = nu(g_N/a_0) M_b with nothing free, and -- distinctively -- says
           the enclosed mass SATURATES at nu(e_N) M_b once the external field takes over, instead of
           climbing to a virial mass.

WHAT IS NEW IN RUNNING THEM TOGETHER, and it is the only genuinely new thing here: items 35 and 38 both
reduce to a measurement of ONE number, the external-field strength e_N, from two lever arms a factor of
three apart in radius.  Section CROSS asks whether one e_N serves both, and whether the baryonic amplitude
the three items demand is one number.  That comparison is new; the underlying liability is not.

INHERITED, NOT REDISCOVERED.  The repository already carries a Milky Way v_c NORMALISATION liability: with
a published baryon census the framework under-predicts v_c(R_0)  (real_research/reviews/
mi_aqual_mcmillan2017_2026.py, mi_route_a_vertical_radial_ratio_2026.py, and hunt item 36 in
hunt_2026/h76_h13_h36_h63.py).  Every test below is therefore run BOTH as an absolute prediction and with a
single amplitude nuisance A on the baryonic mass, so that the SHAPE questions the three items actually ask
are separated from that standing liability.

DATA PROVENANCE -- all three tables were re-verified against the papers' own sources this session:
  * real_research/data/mw_kz11_bovyrix2013_table3.tsv    REPLACED by the arXiv ANCILLARY FILE itself
      (https://arxiv.org/src/1309.0809/anc/table3.csv).  The version previously on disk was a hand
      transcription with 3 of its 43 rows wrong (the innermost, lowest-weight [Fe/H] = -1.25, -1.15 and
      -1.05/0.425 points).  40/43 rows were exact.  That is a data bug found and fixed by this script.
  * real_research/data/mw_rc_ou2024_table1.tsv           all 37 rows verified against tab01.tex in
      https://arxiv.org/e-print/2303.12838; their baryonic model (their Table 2) verified too.
  * real_research/data/mw_halo_bird2022_jeans.txt        every number verified against the LaTeX source
      of https://arxiv.org/e-print/2207.08839.
  * real_research/data/mw_rc_eilers2019_table1.tsv       NEW this session, extracted from the LaTeX source
      of https://arxiv.org/e-print/1810.09466.  Item 35 names Eilers+2019 as well as Ou+2024, and running
      both is the only way to see whether the item's verdict is a property of one pipeline.

Both footings on every number.  Mutation controls.  Checks that CAN fail, with no threshold moved to make
one pass.  The LambdaCDM / Newtonian alternative computed beside the framework, with its fitted parameters
counted out loud.
"""
import sys, math, os
import numpy as np
from scipy.special import j0 as J0, j1 as J1
from hunt_lib import *
TRAPZ = getattr(np, "trapezoid", None) or np.trapz

ck = Check(); rng = np.random.default_rng(343538)
PC = kpc/1000.0
MSUN_PC2 = Msun/PC**2
MSUN_PC3 = Msun/PC**3

# =====================================================================================================
#  THE MASS MODELS  (baryons only; there is no halo anywhere in the framework's column)
# =====================================================================================================
# McMillan 2017 (MNRAS 465, 76) Table 3 best-fitting BARYONS -- the repository's validated model, used
# verbatim in real_research/reviews/mi_aqual_mcmillan2017_2026.py.
def mcm(fRd=1.0):
    """McMillan's baryons, with an optional common stretch fRd on the two STELLAR disc scale lengths
    (masses held fixed).  fRd = 1 is his model; the stretch is used to ask what disc scale length item
    34 would require, and is compared with Bovy & Rix's own measured 2.15 +- 0.14 kpc."""
    return dict(
        thin =dict(S0=896.0*MSUN_PC2/fRd**2, Rd=fRd*2.50*kpc, zd=0.300*kpc, Rm=0.0,       vert="exp"),
        thick=dict(S0=183.0*MSUN_PC2/fRd**2, Rd=fRd*3.02*kpc, zd=0.900*kpc, Rm=0.0,       vert="exp"),
        HI   =dict(Sfid=10.0*MSUN_PC2, Rfid=8.33*kpc, Rd=7.00*kpc, zd=0.085*kpc, Rm=4.0*kpc,  vert="sech2"),
        H2   =dict(Sfid= 2.0*MSUN_PC2, Rfid=8.33*kpc, Rd=1.50*kpc, zd=0.045*kpc, Rm=12.0*kpc, vert="sech2"))
MCM = mcm()
MCM_BULGE_M = 9.23e9*Msun          # his quoted bulge mass; a compact monopole outside 3 kpc
MCM_R0 = 8.21*kpc
BR_R0 = 8.00*kpc                   # the R0 Bovy & Rix assume; their radii move with R0 at fixed R0 - R

# Ou+2024's OWN baryonic model (their Table 2, verified against their source): Misiriotis+2006 double
# exponentials + a de Salas+2019 Hernquist bulge.  Used for item 35 so that their rotation curve is
# confronted with the mass model its own authors adopted, not with one chosen here.
OU = dict(disc =dict(M=3.65e10*Msun, Rd=2.35*kpc,  zd=0.14*kpc),
          HI   =dict(M=8.20e9*Msun,  Rd=18.24*kpc, zd=0.52*kpc),
          H2   =dict(M=1.30e9*Msun,  Rd=2.57*kpc,  zd=0.08*kpc),
          dustc=dict(M=7.00e7*Msun,  Rd=5.00*kpc,  zd=0.10*kpc),
          dustw=dict(M=2.20e5*Msun,  Rd=3.30*kpc,  zd=0.09*kpc))
OU_BULGE_M, OU_BULGE_A = 1.55e10*Msun, 0.70*kpc
OU_R0 = 8.178*kpc

def sigma_of_R(c, R):
    """Face-on surface density of one exponential disc component, with the gas discs' inner hole."""
    R = np.maximum(np.asarray(R, float), 1e-4*kpc)
    S0 = c["S0"] if "S0" in c else c["Sfid"]/math.exp(-c["Rm"]/c["Rfid"] - c["Rfid"]/c["Rd"])
    return S0*np.exp(-c.get("Rm", 0.0)/R - R/c["Rd"])

def zeta_grid(c, n=3001):
    zd = c["zd"]; zg = np.linspace(-18*zd, 18*zd, n)
    z = np.exp(-np.abs(zg)/zd)/(2*zd) if c["vert"] == "exp" else 1.0/np.cosh(zg/(2*zd))**2/(4*zd)
    return zg, z/TRAPZ(z, zg)

def disc_mass(c):
    Rg = np.geomspace(1e-4*kpc, 400*kpc, 6000)
    return float(TRAPZ(2*math.pi*Rg*sigma_of_R(c, Rg), Rg))

def column(c, R, Z):
    zg, zz = zeta_grid(c)
    return sigma_of_R(c, R)*float(TRAPZ(np.where(np.abs(zg) <= Z, zz, 0.0), zg))

# ---- Hankel machinery.  Phi(R,z) = -2 pi G INT dk J0(kR) S(k) INT dz' zeta(z') exp(-k|z-z'|), so
#      |g_R| = 2 pi G INT dk k J1(kR) S(k) V(k,z)  and  K_z = 2 pi G INT dk k J0(kR) S(k) W(k,z),
#      V = INT zeta e^{-k|z-z'|} dz', W = INT zeta sign(z-z') e^{-k|z-z'|} dz'.  Exact for an axisymmetric
#      disc of separable (R,z) structure.  Validated below against the analytic exponential transform.
KMAX = 100.0/kpc
KGRID = np.linspace(1e-6*KMAX, KMAX, 60000)     # fine linear grid: the J0/J1 oscillations set the spacing
KCO   = np.geomspace(1e-5/kpc, KMAX, 700)       # coarse grid for the smooth kernels S, V, W

def S_of_k(c):
    Rg = np.geomspace(1e-4*kpc, 400*kpc, 5000); Sg = sigma_of_R(c, Rg)
    S = TRAPZ(Sg[None, :]*J0(KCO[:, None]*Rg[None, :])*Rg[None, :], Rg, axis=1)
    return np.interp(KGRID, KCO, S)

def VW_of_k(c, Z):
    zg, zz = zeta_grid(c); d = Z - zg
    e = np.exp(-KCO[:, None]*np.abs(d)[None, :])
    V = TRAPZ(zz[None, :]*e, zg, axis=1); W = TRAPZ(zz[None, :]*np.sign(d)[None, :]*e, zg, axis=1)
    return np.interp(KGRID, KCO, V), np.interp(KGRID, KCO, W)

class DiscField:
    """Newtonian radial and vertical force of one exponential disc component at a fixed height Z.
    Evaluated ONCE on a log grid in R and then interpolated -- the earlier draft of this script called
    forces() inside a 60 x 61 chi2 grid and never finished."""
    NG = np.geomspace(0.5*kpc, 300*kpc, 420)
    def __init__(self, c, Z):
        self.S = S_of_k(c); self.V, self.W = VW_of_k(c, Z)
        kR = KGRID[None, :]*self.NG[:, None]
        self.gRg = 2*math.pi*G*TRAPZ(KGRID[None, :]*J1(kR)*(self.S*self.V)[None, :], KGRID, axis=1)
        self.Kzg = 2*math.pi*G*TRAPZ(KGRID[None, :]*J0(kR)*(self.S*self.W)[None, :], KGRID, axis=1)
    def forces(self, R):
        R = np.atleast_1d(np.asarray(R, float))
        return np.interp(R, self.NG, self.gRg), np.interp(R, self.NG, self.Kzg)
    def forces_exact(self, R):
        R = np.atleast_1d(np.asarray(R, float)); kR = KGRID[None, :]*R[:, None]
        return (2*math.pi*G*TRAPZ(KGRID[None, :]*J1(kR)*(self.S*self.V)[None, :], KGRID, axis=1),
                2*math.pi*G*TRAPZ(KGRID[None, :]*J0(kR)*(self.S*self.W)[None, :], KGRID, axis=1))

def hernquist_M(M, a, r): return M*r**2/(r + a)**2

def load_tsv(fname):
    lines = [l.rstrip("\n") for l in open(os.path.join(DATA, fname)) if l.strip() and not l.startswith("#")]
    hdr = lines[0].split("\t")
    d = np.array([[float(x) for x in l.split("\t")] for l in lines[1:]])
    return {h: d[:, i] for i, h in enumerate(hdr)}

def expfit(v, dv, R, Rpiv=None):
    """Weighted fit of v = K0 exp(-(R-Rpiv)/h).  Returns K0, h, and their formal errors.
    BUG FIXED IN THE MAKING: the pivot defaults to the MODEL's R0, not 8.0 kpc.  Bovy & Rix's radii are
    shifted below to this model's R0 = 8.21 kpc, and quoting the fitted normalisation at 8.0 kpc in the
    shifted frame silently reports K_z at R0 - 0.21 kpc, which is 8 per cent high."""
    Rpiv = MCM_R0 if Rpiv is None else Rpiv
    w = (v/dv)**2; x = (R - Rpiv)/kpc; ly = np.log(v)
    A = np.vstack([np.ones_like(x), -x]).T; W = np.diag(w)
    M = A.T@W@A; p = np.linalg.solve(M, A.T@W@ly); C = np.linalg.inv(M)
    return math.exp(p[0]), 1.0/p[1], math.exp(p[0])*math.sqrt(C[0, 0]), math.sqrt(C[1, 1])/p[1]**2

def logslope(R, v, lo, hi):
    m = (R >= lo) & (R <= hi)
    return float(np.polyfit(np.log(R[m]), np.log(v[m]), 1)[0])

# =====================================================================================================
P("="*118); P("MASS-MODEL VALIDATION -- nothing is tested until the model reproduces its own published numbers")
P("="*118)
mcm_m = {k: disc_mass(c)/Msun for k, c in MCM.items()}
mstar = mcm_m["thin"] + mcm_m["thick"] + MCM_BULGE_M/Msun
MCM_MB = (mstar + mcm_m["HI"] + mcm_m["H2"])*Msun
info(f"McMillan 2017 baryons: thin {mcm_m['thin']:.3e}, thick {mcm_m['thick']:.3e}, bulge {MCM_BULGE_M/Msun:.3e}, "
     f"HI {mcm_m['HI']:.3e}, H2 {mcm_m['H2']:.3e} Msun")
ck("V1 the McMillan mass model reproduces his own stellar mass to better than 10 per cent",
   abs(mstar/5.43e10 - 1) < 0.10,
   f"M_* = {mstar:.3e} vs his 5.43e10 ({abs(mstar/5.43e10-1):.1%}); HI {mcm_m['HI']:.3e} vs his 1.1e10; "
   f"total baryons M_b = {MCM_MB/Msun:.3e} Msun")
sig_star_R0 = sum(column(MCM[k], MCM_R0, 1.1*kpc) for k in ("thin", "thick"))/MSUN_PC2
sig_bar_R0 = sum(column(MCM[k], MCM_R0, 1.1*kpc) for k in MCM)/MSUN_PC2
ck("V2 the local stellar column matches Bovy & Rix's own measured 38 +- 4 Msun/pc^2 -- the model is anchored "
   "in the same quantity, at the same height, as the data item 34 uses",
   abs(sig_star_R0 - 38.0) < 8.0,
   f"model {sig_star_R0:.1f} vs 38 +- 4 (stars); total baryonic column {sig_bar_R0:.1f} Msun/pc^2")
c = MCM["thin"]; Sn = S_of_k(c); Sa = c["S0"]*c["Rd"]**2*(1 + (KGRID*c["Rd"])**2)**-1.5
m = KGRID < 20/kpc; err_S = float(np.max(np.abs(Sn[m]/Sa[m] - 1)))
ck("V3 the numerical Hankel transform reproduces the ANALYTIC exponential-disc transform",
   err_S < 0.02, f"max |S_num/S_analytic - 1| = {err_S:.2e} over k < 20/kpc")
Rt = np.array([4.0, 6.0, 8.0, 12.0])*kpc
inv = np.array([float(TRAPZ(KGRID*J0(KGRID*r)*Sn, KGRID)) for r in Rt])
err_inv = float(np.max(np.abs(inv/sigma_of_R(c, Rt) - 1)))
ck("V4 the k-grid is fine enough that the inverse transform returns Sigma(R) itself",
   err_inv < 0.03, f"max |inverse/direct - 1| = {err_inv:.2e} at R = 4, 6, 8, 12 kpc")

# =====================================================================================================
P(""); P("="*118); P("ITEM 34 -- the RADIAL run of the vertical force, K_z at |z| = 1.1 kpc"); P("="*118)
# =====================================================================================================
rows = load_tsv("mw_kz11_bovyrix2013_table3.tsv")
Kz_obs = rows["Kz11_o2piG"]; dKz = rows["dKz11_o2piG"]
Rk = (MCM_R0/kpc - rows["R0mR"])*kpc          # B&R: radii move with R0 at fixed R0 - R; this model's R0
Rk_raw = rows["R_kpc"]*kpc
Z11 = 1.1*kpc
info(f"Bovy & Rix 2013 Table 3 (arXiv ancillary file): {len(Rk)} independent K_Z,1.1 measurements, one per "
     f"mono-abundance population, R = {Rk.min()/kpc:.2f} to {Rk.max()/kpc:.2f} kpc.")
info(f"radii are placed at R = R0(model) - (R0 - R)_table = {MCM_R0/kpc:.2f} - (R0-R), as Bovy & Rix instruct; "
     f"using their tabulated R (R0 = 8.00) instead shifts every radius by {(MCM_R0-BR_R0)/kpc:+.2f} kpc.")
info("THE ITEM ASKED FOR Gaia DR3 K_z(R) OVER R = 6-12 kpc AND NO SUCH TABULATED RUN EXISTS that I could find;")
info("this is the SEGUE mono-abundance measurement, which is still the standard.  Range covered is 4 kpc of")
info("radius, and it is INSIDE R0, not outside -- a limitation of the data, not of the prediction.")

FLD = {k: DiscField(MCM[k], Z11) for k in MCM}
ge, Ke = FLD["thin"].forces_exact(np.array([5.0, 8.0, 11.0])*kpc)
gi, Ki = FLD["thin"].forces(np.array([5.0, 8.0, 11.0])*kpc)
ck("V5 the interpolated force grid reproduces the exact Hankel evaluation (this is the speed fix that let the "
   "script run at all -- it must not cost accuracy)",
   float(np.max(np.abs(Ki/Ke - 1))) < 1e-3 and float(np.max(np.abs(gi/ge - 1))) < 1e-3,
   f"max |interp/exact - 1| = {max(float(np.max(np.abs(Ki/Ke-1))), float(np.max(np.abs(gi/ge-1)))):.2e}")

def newtonian_at(R, model=MCM, fld=None):
    fld = FLD if fld is None else fld
    gR = np.zeros_like(R); Kz = np.zeros_like(R)
    for k in model:
        a, b = fld[k].forces(R); gR += a; Kz += b
    r = np.sqrt(R**2 + Z11**2); gb = G*MCM_BULGE_M/r**2       # compact bulge as a monopole (R > 3 kpc)
    return gR + gb*R/r, Kz + gb*Z11/r

gRn, Kzn = newtonian_at(Rk); Kzn_o = Kzn/(2*math.pi*G)/MSUN_PC2

# --- the measured exponential, and an honest error on it -------------------------------------------
K0o, ho, dK0o_f, dho_f = expfit(Kz_obs, dKz, Rk)
chi2_exp = float(np.sum(((K0o*np.exp(-(Rk - MCM_R0)/(ho*kpc)) - Kz_obs)/dKz)**2))
bo = []
for _ in range(2000):
    i = rng.integers(0, len(Rk), len(Rk))
    if len(np.unique(Rk[i])) < 3: continue           # a degenerate resample cannot define a scale length
    K, hh = expfit(Kz_obs[i], dKz[i], Rk[i])[:2]
    if 0 < hh < 50: bo.append((K, hh))
bo = np.array(bo); dK0o, dho = bo[:, 0].std(), bo[:, 1].std()
info(f"the measured exponential:  K_z,1.1(R0)/2piG = {K0o:.1f} Msun/pc^2, scale length {ho:.2f} kpc.")
info(f"  formal (quoted-error) uncertainties {dK0o_f:.1f} and {dho_f:.2f}; BOOTSTRAP over the 43 MAPs gives "
     f"{dK0o:.1f} and {dho:.2f}, and the exponential's own chi2 = {chi2_exp:.0f}/{len(Rk)-2} d.o.f.")
info(f"  chi2/dof = {chi2_exp/(len(Rk)-2):.2f} for a pure exponential means the quoted errors are "
     f"{'ADEQUATE' if chi2_exp/(len(Rk)-2) < 1.6 else 'TOO SMALL for the MAP-to-MAP scatter'}.")
# Bovy & Rix's OWN published fit to these same points, from their eq. (bestfitkz), read out of the paper's
# LaTeX source this session.  This is the validation of the statistic, not a citation for colour.
BR_K0, BR_h, BR_dK0, BR_dh = 67.0, 2.7, 0.025*67.0, 0.04*2.7
ck("V6 the refit REPRODUCES Bovy & Rix's own published exponential, which validates the two statistics that "
   "item 34's whole verdict rests on",
   abs(K0o - BR_K0) < 2.0 and abs(ho - BR_h) < 0.1,
   f"refit {K0o:.1f} Msun/pc^2 and {ho:.2f} kpc against their published "
   f"K_z,1.1(R0)/2piG = {BR_K0:.0f} exp(-(R-R0)/{BR_h:.1f} kpc), formal errors 2.5% and 4%")
# from here on the PUBLISHED errors are used for significances, not the bootstrap: they are larger and they
# are the authors' own, and the bootstrap only captures MAP-to-MAP scatter, not their systematics.
dK0o, dho = BR_dK0, BR_dh
info(f"  significances below use the AUTHORS' formal errors ({dK0o:.1f} Msun/pc^2, {dho:.2f} kpc), which are "
     f"larger than the bootstrap and include what they could quantify.  McMillan 2017's independently fitted "
     f"K_z,1.1 corresponds to 73.9 +- 6, and that 10 per cent disagreement BETWEEN measurements is the honest "
     f"floor on any claim made here.")

info("")
info(f"{'R [kpc]':>8}{'Sig_b(<1.1)':>13}{'K_z^N/2piG':>12}{'|g_N|/a0':>10}{'nu':>7}{'K_z^fw':>9}{'K_z obs':>9}{'+-':>7}")
R34 = {}
for foot, a0 in A0.items():
    y = np.sqrt(gRn**2 + Kzn**2)/a0; nuv = nu(y); pred = nuv*Kzn_o
    if foot == "canonical":
        for i in np.argsort(Rk)[::6]:
            info(f"{Rk[i]/kpc:8.2f}{sum(column(MCM[k], Rk[i], Z11) for k in MCM)/MSUN_PC2:13.1f}"
                 f"{Kzn_o[i]:12.1f}{y[i]:10.2f}{nuv[i]:7.3f}{pred[i]:9.1f}{Kz_obs[i]:9.1f}{dKz[i]:7.1f}")
    chi2 = float(np.sum(((pred - Kz_obs)/dKz)**2))
    K0p, hp, _, _ = expfit(pred, dKz*pred/Kz_obs, Rk)
    R34[foot] = (pred, chi2, K0p, hp, nuv)
K0b, hb, _, _ = expfit(Kzn_o, dKz*Kzn_o/Kz_obs, Rk)
chi2_bar = float(np.sum(((Kzn_o - Kz_obs)/dKz)**2))
info("")
for foot in A0:
    pred, chi2, K0p, hp, nuv = R34[foot]
    info(f"{foot:10} predicted K_z,1.1(R0)/2piG = {K0p:5.1f} ({(K0p-K0o)/dK0o:+5.1f} sigma), scale length "
         f"{hp:.2f} kpc ({(hp-ho)/dho:+5.1f} sigma), chi2 = {chi2:5.0f} / {len(Rk)} points, 0 free parameters")
info(f"{'baryons only':10} (nu = 1)  K_z,1.1(R0)/2piG = {K0b:5.1f} ({(K0b-K0o)/dK0o:+5.1f} sigma), scale length "
     f"{hb:.2f} kpc ({(hb-ho)/dho:+5.1f} sigma), chi2 = {chi2_bar:5.0f} / {len(Rk)} points")
K0p, hp = R34["canonical"][2], R34["canonical"][3]
chi2c = R34["canonical"][1]

info(f"THIS IS A PUBLISHED TEST, NOT A NEW ONE, and that has to be said before any verdict: Bovy & Rix devote a")
info(f"paragraph of their own Section 7 to exactly this.  They estimate that MOND enhances the vertical force at")
info(f"R0 by >~60 per cent, so that for a baryonic column of 51 +- 4 Msun/pc^2 they expect K_z,1.1/2piG >~ 82 +- 6")
info(f"against their measured 68 +- 4 -- a '>~2 sigma tension' in their words -- and that the dynamically inferred")
info(f"disc scale length should come out ~25 per cent long, ~2.9 kpc, which they call '5 sigma removed' from their")
info(f"measured 2.15 +- 0.14 kpc.  What is new here is only that it is redone with THIS kernel and THIS a_0, on")
info(f"the full radial run rather than at R0, with the model's own baryonic column ({sig_bar_R0:.1f} against their 51 +- 4).")
ck("34a AGAINST INTEREST -- THE NORMALISATION DOES NOT LAND, AND IT CONFIRMS THE PUBLISHED TENSION RATHER THAN "
   "RELIEVING IT.  With a_0 fixed, no halo and nothing fitted, the kernel boost on McMillan's baryonic column "
   "gives %.1f (canonical) and %.1f (alt) Msun/pc^2 against a measured %.1f -- %.0f and %.0f per cent over.  "
   "The formal significance is %.0f sigma on the authors' own 2.5 per cent error, but THAT NUMBER MUST NOT BE "
   "QUOTED: McMillan's independent fit of the same quantity gives 73.9 +- 6, a 10 per cent disagreement between "
   "measurements, and against that the honest significance is %.1f sigma.  Either way it sits just above Bovy & "
   "Rix's own MOND estimate of >~82 +- 6, so the exponential kernel does not escape the tension they identified."
   % (K0p, R34['alt'][2], K0o, 100*(K0p/K0o - 1), 100*(R34['alt'][2]/K0o - 1),
      (K0p-K0o)/dK0o, (K0p-73.9)/6.0),
   abs(K0p - K0o) < 2*dK0o,
   f"predicted {K0p:.1f} (canonical) / {R34['alt'][2]:.1f} (alt) vs measured {K0o:.1f} +- {dK0o:.1f} "
   f"Msun/pc^2 (authors' formal error); against McMillan's independent 73.9 +- 6 it is "
   f"{(K0p-73.9)/6:+.1f} sigma; baryons alone give {K0b:.1f}, already within {100*abs(K0b/K0o-1):.0f} per cent")

ck("34b AGAINST INTEREST -- THE SHAPE, WHICH IS WHAT THE ITEM ACTUALLY ASKS, DOES NOT LAND EITHER.  The kernel "
   "lengthens the predicted scale length (nu rises outward, exactly as the framework says it must), but the "
   "baryons were ALREADY too long: predicted %.2f kpc against a measured %.2f +- %.2f.  The kernel makes the "
   "one discrepancy that existed WORSE, by %+.2f kpc.  The item's own criterion was 10 per cent across the "
   "measured range." % (hp, ho, dho, hp - hb),
   abs(hp - ho) < 2*dho,
   f"predicted {hp:.2f} kpc (canonical) / {R34['alt'][3]:.2f} (alt) vs measured {ho:.2f} +- {dho:.2f}; "
   f"baryons alone {hb:.2f} kpc")

frac = np.abs(R34["canonical"][0]/Kz_obs - 1)
info(f"point by point: median |predicted/measured - 1| = {np.median(frac):.1%}, 90th percentile "
     f"{np.percentile(frac, 90):.1%}, worst {frac.max():.1%} at R = {Rk[np.argmax(frac)]/kpc:.2f} kpc")
ck("34c the point-by-point agreement misses the item's 10 per cent criterion",
   np.median(frac) < 0.10, f"median {np.median(frac):.1%}, chi2/N = {chi2c/len(Rk):.2f}")

# --- what disc scale length would the framework NEED?  a sharp, falsifiable number -------------------
def h_pred_for(fRd, a0=A0["canonical"], boost=True):
    mod = mcm(fRd); fl = {k: DiscField(mod[k], Z11) for k in mod}
    gR, Kz = newtonian_at(Rk, mod, fl); Ko = Kz/(2*math.pi*G)/MSUN_PC2
    v = nu(np.sqrt(gR**2 + Kz**2)/a0)*Ko if boost else Ko
    return expfit(v, dKz*v/Kz_obs, Rk)[1]
grid_f = np.linspace(0.20, 1.20, 21)
h_f = np.array([h_pred_for(f) for f in grid_f])
h_fN = np.array([h_pred_for(f, boost=False) for f in grid_f])
def invert_h(target, hs, fs):
    """f such that h(f) = target.  h(f) is monotone increasing in f; returns nan OUTSIDE the grid rather
    than silently clamping, which is what the first version of this block did (it reported R_d = 2.88
    [2.88, 2.88] kpc, three identical clamped values, and I nearly wrote that up as a measurement)."""
    if not np.all(np.diff(hs) > 0): return float("nan")
    if target < hs[0] or target > hs[-1]: return float("nan")
    return float(np.interp(target, hs, fs))
Rd_need  = invert_h(ho, h_f, grid_f)*2.50
Rd_needN = invert_h(ho, h_fN, grid_f)*2.50
Rd_lo    = invert_h(ho - dho, h_f, grid_f)*2.50
Rd_hi    = invert_h(ho + dho, h_f, grid_f)*2.50
info(f"predicted K_z scale length as the STELLAR discs are stretched (masses held fixed):")
info(f"    {'R_d,thin [kpc]':>16}" + "".join(f"{f*2.5:8.2f}" for f in grid_f[::4]))
info(f"    {'h framework':>16}" + "".join(f"{v:8.2f}" for v in h_f[::4]))
info(f"    {'h baryons only':>16}" + "".join(f"{v:8.2f}" for v in h_fN[::4]))
info(f"  the mapping is NOT monotone -- it turns over at R_d = {grid_f[int(np.argmin(h_f))]*2.5:.2f} kpc, because a very "
     f"short stellar disc becomes a point mass whose K_z falls faster while the 7 kpc gas disc holds the outer")
info(f"  column up.  So 'what R_d does the framework need' has no unique answer and the inverse problem is the")
info(f"  wrong question.  (An earlier version of this block asked it anyway and, because np.interp CLAMPS at the")
info(f"  ends of a non-monotone grid, it silently returned R_d = 2.88 [2.88, 2.88] kpc -- three identical clamped")
info(f"  values that I nearly wrote up as a measurement.  The guard that catches it is in invert_h above.)")
# the WELL-POSED version: evaluate at the disc scale length these same data actually measure
f215 = 2.15/2.50
h215 = h_pred_for(f215); h215N = h_pred_for(f215, boost=False)
h215lo, h215hi = h_pred_for((2.15-0.14)/2.50), h_pred_for((2.15+0.14)/2.50)
info(f"the well-posed question instead: FEED THE FRAMEWORK THE DISC BOVY & RIX MEASURE, R_d = 2.15 +- 0.14 kpc.")
info(f"  framework then predicts a K_z scale length of {h215:.2f} [{h215lo:.2f}, {h215hi:.2f}] kpc; "
     f"baryons alone predict {h215N:.2f} kpc; the measurement is {ho:.2f} +- {dho:.2f} kpc")
dtot = math.hypot(dho, abs(h215hi - h215lo)/2)
ck("34d THE WELL-POSED VERSION, and it is the cleanest form of the liability because it uses only quantities "
   "these same 43 stars measure: given Bovy & Rix's own disc, R_d = 2.15 +- 0.14 kpc, the framework predicts a "
   "K_z scale length of %.2f kpc against their measured %.2f +- %.2f -- %.1f sigma long.  Newtonian baryons with "
   "the same disc give %.2f kpc, %.1f sigma.  The kernel's outward-rising boost inflates the inferred disc, "
   "which is exactly the effect Bovy & Rix predicted for MOND at 25 per cent; here it is %.0f per cent."
   % (h215, ho, dho, (h215 - ho)/dtot, h215N, (h215N - ho)/dtot, 100*(h215/h215N - 1)),
   abs(h215 - ho) < 2*dtot,
   f"framework {h215:.2f} [{h215lo:.2f}, {h215hi:.2f}] kpc, baryons alone {h215N:.2f}, measured {ho:.2f} "
   f"+- {dho:.2f}; combined error {dtot:.2f}; at McMillan's own R_d = 2.50 the framework gives {hp:.2f} kpc")

# --- the LambdaCDM alternative, with its fitted parameter counted -----------------------------------
def nfw_Kz(rho_s, rs, R, Z):
    r = np.sqrt(R**2 + Z**2); x = r/rs
    M = 4*math.pi*rho_s*rs**3*(np.log(1+x) - x/(1+x))
    return (G*M/r**2)*(Z/r)/(2*math.pi*G)/MSUN_PC2
rs_h = 19.0*kpc; b = nfw_Kz(1.0, rs_h, Rk, Z11)
rho_s = np.sum((Kz_obs - Kzn_o)*b/dKz**2)/np.sum(b**2/dKz**2)
chi2_nfw = float(np.sum(((Kzn_o + nfw_Kz(rho_s, rs_h, Rk, Z11) - Kz_obs)/dKz)**2))
rho_local = rho_s/((MCM_R0/rs_h)*(1+MCM_R0/rs_h)**2)/MSUN_PC3
info(f"LambdaCDM alternative (the SAME baryons + a round NFW halo, r_s = 19 kpc fixed, ONE fitted "
     f"normalisation): rho_dm(R0) = {rho_local:.4f} Msun/pc^3, chi2 = {chi2_nfw:.0f}")
ck("34e THE COMPARISON, both ways: on these 43 points the framework's zero-parameter prediction is WORSE than "
   "the baryons alone and far worse than baryons plus a one-parameter round halo, which lands on the standard "
   "local dark-matter density.  The vertical force at 1.1 kpc is the one place the Milky Way is close to "
   "maximal-disc, and that is precisely where a boost is not wanted",
   chi2c < min(chi2_bar, chi2_nfw),
   f"chi2: framework {chi2c:.0f} (0 params), baryons alone {chi2_bar:.0f} (0 params), baryons + NFW "
   f"{chi2_nfw:.0f} (1 param, rho_dm(R0) = {rho_local:.4f} against the usual 0.008-0.013)")

# --- mutations ---------------------------------------------------------------------------------------
y10 = np.sqrt(gRn**2 + Kzn**2)/(10*A0["canonical"]); mut2 = float(np.sum(((nu(y10)*Kzn_o - Kz_obs)/dKz)**2))
ck("M34 mutation control, and it FIRES THE WRONG WAY, which is the point: moving a_0 up by a decade (which "
   "switches the kernel off) IMPROVES the fit towards the baryons-only value, and switching the kernel off "
   "entirely improves it further.  The estimator is working; it is the framework that is being rejected here",
   mut2 > chi2c and chi2_bar > chi2c,
   f"chi2: framework {chi2c:.0f}, a_0 x10 {mut2:.0f}, nu = 1 (baryons alone) {chi2_bar:.0f} -- the "
   f"mutations are BETTER, not worse")
sh = rng.permutation(Kz_obs)
ck("M34b mutation control: shuffling the measured K_z values between radii destroys the measured scale length, "
   "so the scale-length statistic that 34b and 34d turn on carries real radial information",
   abs(expfit(sh, dKz, Rk)[1] - ho) > 2*dho,
   f"shuffled scale length {expfit(sh, dKz, Rk)[1]:+.2f} kpc vs real {ho:.2f} +- {dho:.2f}")
Rk_alt = Rk_raw; gA, KA = newtonian_at(Rk_alt); KAo = KA/(2*math.pi*G)/MSUN_PC2
hA = expfit(nu(np.sqrt(gA**2 + KA**2)/A0["canonical"])*KAo, dKz, Rk_alt)[1]
hoA = expfit(Kz_obs, dKz, Rk_alt)[1]
info(f"R0 systematic: using the tabulated radii (R0 = 8.00) instead of shifting to the model's 8.21 moves the "
     f"predicted scale length {hp:.2f} -> {hA:.2f} and the measured {ho:.2f} -> {hoA:.2f} kpc; the GAP, which is "
     f"the result, moves {hp-ho:+.2f} -> {hA-hoA:+.2f} kpc.  The verdict is not an R0 artefact.")
info("CAVEAT that sets the size of the claim, stated because it is the framework's best defence: K_z^fw = "
     "nu(|g_N|) K_z^N is the ALGEBRAIC (QUMOND) estimate with the curl term dropped.  The repository's own")
info("full AQUAL solve (real_research/reviews/mi_route_a_vertical_radial_ratio_2026.py) finds nu_rad = 1.222 and")
info(f"nu_vert = 1.251 at R0 for the alpha=2 kernel, against nu = {R34['canonical'][4][np.argmin(np.abs(Rk-8*kpc))]:.3f} "
     f"used here -- so the true boost may be ~15 per cent smaller than the algebraic one, which would cut but not")
info("close the 34a gap (92 -> ~80 against 67.5).  It does NOT touch 34b/34d, because the vertical-to-radial ratio")
info("that solve reports is 1.024, i.e. essentially constant in R, so it cannot change a SCALE LENGTH.")

# =====================================================================================================
P(""); P("="*118); P("ITEM 35 -- the Milky Way's claimed Keplerian decline beyond 20 kpc"); P("="*118)
# =====================================================================================================
OUFLD = {k: DiscField(dict(S0=v["M"]/(2*math.pi*v["Rd"]**2), Rd=v["Rd"], zd=v["zd"], Rm=0.0, vert="exp"), 0.0)
         for k, v in OU.items()}
OU_MB = sum(v["M"] for v in OU.values()) + OU_BULGE_M
RG = np.geomspace(3*kpc, 60*kpc, 300)
gN_grid = sum(OUFLD[k].forces(RG)[0] for k in OU) + G*hernquist_M(OU_BULGE_M, OU_BULGE_A, RG)/RG**2
def gN_ou(R, A=1.0): return A*np.interp(R, RG, gN_grid)

CURVES = {}
d = load_tsv("mw_rc_ou2024_table1.tsv")
CURVES["Ou+2024   "] = (d["R_kpc"]*kpc, d["vc_kms"]*1e3, 0.5*(d["sig_plus"] + d["sig_minus"])*1e3,
                        np.where(d["R_kpc"] < 22, 0.04, 0.15), 12*kpc, 27.4*kpc)
d = load_tsv("mw_rc_eilers2019_table1.tsv")
CURVES["Eilers+2019"] = (d["R_kpc"]*kpc, d["vc_kms"]*1e3, 0.5*(d["sig_plus"] + d["sig_minus"])*1e3,
                         np.full(len(d["R_kpc"]), 0.035), 12*kpc, 25*kpc)
info("two independent measurements of the same curve are run, because the item names both and because a")
info("verdict that depends on one pipeline is not a verdict.  Systematic fractions are the authors' own:")
info("  Ou+2024      37 points 6.3-27.3 kpc; their stated total systematic 1-5% to R = 22 kpc (4% used), 15% beyond")
info("  Eilers+2019  38 points 5.3-24.8 kpc; their stated total systematic 2-5% throughout (3.5% used)")
info("EVERY NUMBER BELOW IS QUOTED TWICE, with STAT-only errors and with stat+sys added in quadrature, because")
info("neither is right on its own: a systematic is COHERENT between radii, so folding it in per point as if it")
info("were random both flatters the model (chi2 falls) and hides the decline (the slope error inflates).  The")
info("first version of this section used stat+sys only and reported a comfortable fit; that was my error and it")
info("is corrected here.  The stat-only column is the SHAPE question the item actually asks.")

# the external field the Milky Way ACTUALLY sits in, computed rather than assumed
M31_MB, D_M31 = 1.2e11*Msun, 0.78*Mpc
eN_M31 = {f: math.sqrt(G*M31_MB*a0)/D_M31/a0 for f, a0 in A0.items()}
info(f"the external field the Milky Way actually has: M31's deep-MOND field at 780 kpc is e_N = "
     f"{eN_M31['canonical']:.3f} (canonical) / {eN_M31['alt']:.3f} (alt) a_0, and the repository's large-scale-"
     f"structure field for a field galaxy is 0.01-0.03.  The physical prior is e_N <= 0.05, which is exactly")
info("the number the hunt list wrote down.  e_N is NOT fitted below except to measure what would be required.")

GRID_A = np.geomspace(0.5, 6.0, 120); GRID_E = np.concatenate([[0.0], np.geomspace(0.002, 5.0, 120)])
R35 = {}
for cname, (Rr, vo, dvs, sysf, LO, HI) in CURVES.items():
    gN1 = gN_ou(Rr)
    sl_obs = logslope(Rr, vo, LO, HI)
    ERRS = {"stat": dvs, "stat+sys": np.sqrt(dvs**2 + (sysf*vo)**2)}
    bsd = {k: np.array([logslope(Rr, vo*np.exp(rng.normal(0, e/vo)), LO, HI)
                        for _ in range(2000)]).std() for k, e in ERRS.items()}
    info("")
    info(f"{cname}: v_c falls {vo.max()/1e3:.1f} -> {vo[-1]/1e3:.1f} km/s.  Measured outer log-slope over "
         f"{LO/kpc:.0f}-{HI/kpc:.0f} kpc = {sl_obs:+.3f} +- {bsd['stat']:.3f} (stat) "
         f"+- {bsd['stat+sys']:.3f} (stat+sys)   [flat 0.000, Keplerian -0.500]")
    for ename, dv in ERRS.items():
        for foot, a0 in A0.items():
            g = gN1[None, :]*GRID_A[:, None]                          # (A, R) -- g_N scales with A exactly
            chi2 = np.empty((len(GRID_A), len(GRID_E)))
            for j, e in enumerate(GRID_E):
                chi2[:, j] = np.sum(((np.sqrt(nu((g + e*a0)/a0)*g*Rr[None, :]) - vo[None, :])
                                     / dv[None, :])**2, axis=1)
            i, j = np.unravel_index(np.argmin(chi2), chi2.shape)
            Ab, eb, c2b = GRID_A[i], GRID_E[j], chi2[i, j]
            prof = chi2.min(axis=0); ok = prof <= prof.min() + 1.0
            elo, ehi = GRID_E[ok].min(), GRID_E[ok].max()
            i0 = int(np.argmin(chi2[:, 0])); A0f, c20 = GRID_A[i0], chi2[i0, 0]
            v0 = np.sqrt(nu(gN_ou(Rr, A0f)/a0)*gN_ou(Rr, A0f)*Rr); sl0 = logslope(Rr, v0, LO, HI)
            R35[(cname, ename, foot)] = dict(Ab=Ab, eb=eb, elo=elo, ehi=ehi, c2b=c2b, A0f=A0f, c20=c20,
                                             sl0=sl0, sl_obs=sl_obs, bs=bsd[ename], n=len(Rr))
            if foot == "canonical":
                info(f"   {ename:9} {foot:10} best fit A = {Ab:.2f} (M_b = {Ab*OU_MB/Msun:.2e} Msun), "
                     f"e_N = {eb:.3f} [{elo:.3f}, {ehi:.3f}], chi2/N = {c2b/len(Rr):.1f}; with e_N = 0 "
                     f"forced, A = {A0f:.2f}, outer slope {sl0:+.3f}")
    for foot in ("alt",):
        d = R35[(cname, "stat+sys", foot)]
        info(f"   {'stat+sys':9} {foot:10} best fit A = {d['Ab']:.2f}, e_N = {d['eb']:.3f} "
             f"[{d['elo']:.3f}, {d['ehi']:.3f}], chi2/N = {d['c2b']/d['n']:.1f}, e_N=0 slope {d['sl0']:+.3f}")
    info(f"   NOTE the chi2 swings by a factor {R35[(cname,'stat','canonical')]['c2b']/R35[(cname,'stat+sys','canonical')]['c2b']:.0f} "
         f"between the two error models, from {R35[(cname,'stat','canonical')]['c2b']/len(Rr):.0f} to "
         f"{R35[(cname,'stat+sys','canonical')]['c2b']/len(Rr):.1f} per point.  NEITHER is a usable goodness of fit: "
         f"the random errors alone")
    info(f"   (0.3-2 km/s) are far below both the authors' coherent systematics and the real non-axisymmetric")
    info(f"   structure in the disc, and adding a coherent systematic in quadrature per point then over-corrects.")
    info(f"   Only the SLOPE is quoted as a result below, and the e_N interval only from the stat+sys fit, where")
    info(f"   chi2 per point is of order one and a delta-chi2 = 1 interval means something.")

CN = list(CURVES)
S = lambda c, e: R35[(c, e, "canonical")]
info("")
info(f"{'':>14}{'measured slope':>18}{'framework (e_N=0)':>20}{'gap':>10}{'sigma':>8}")
for c in CN:
    d = S(c, "stat")
    info(f"{c:>14}{d['sl_obs']:>+13.3f} +-{d['bs']:.3f}{d['sl0']:>+20.3f}{d['sl0']-d['sl_obs']:>+10.3f}"
         f"{(d['sl0']-d['sl_obs'])/d['bs']:>+8.1f}")
ck("35a THE ITEM'S PREMISE IS WRONG AND THAT IS THE FIRST RESULT: the outer decline is NOT Keplerian.  The "
   "measured log-slopes are %+.3f (Ou) and %+.3f (Eilers) against -0.500 for Kepler, and the two independent "
   "pipelines agree with each other to %.1f sigma.  Any verdict phrased as 'can the framework survive a "
   "Keplerian decline' is answering a question these data do not pose."
   % (S(CN[0], 'stat')['sl_obs'], S(CN[1], 'stat')['sl_obs'],
      abs(S(CN[0], 'stat')['sl_obs'] - S(CN[1], 'stat')['sl_obs'])/math.hypot(S(CN[0], 'stat')['bs'], S(CN[1], 'stat')['bs'])),
   all(-0.45 < S(c, "stat")["sl_obs"] < -0.05 for c in CN),
   f"measured {S(CN[0],'stat')['sl_obs']:+.3f} +- {S(CN[0],'stat')['bs']:.3f} (Ou) and "
   f"{S(CN[1],'stat')['sl_obs']:+.3f} +- {S(CN[1],'stat')['bs']:.3f} (Eilers), stat-only; Keplerian is -0.500")

ck("35b THE FRAMEWORK DOES MOST BUT NOT ALL OF IT, WITH NO EXTERNAL FIELD AT ALL.  With e_N = 0 and one "
   "amplitude, the kernel already produces %+.3f and %+.3f -- %.0f and %.0f per cent of the observed decline -- "
   "because g_bar is still falling at 12-27 kpc and the curve has not reached its asymptote.  What is left over "
   "is %.1f and %.1f sigma on stat-only errors and %.1f and %.1f sigma once the authors' own systematics are "
   "folded in.  This is a MILD tension, not a kill, and it is smaller than the item anticipated."
   % (S(CN[0], 'stat')['sl0'], S(CN[1], 'stat')['sl0'],
      100*S(CN[0], 'stat')['sl0']/S(CN[0], 'stat')['sl_obs'], 100*S(CN[1], 'stat')['sl0']/S(CN[1], 'stat')['sl_obs'],
      (S(CN[0], 'stat')['sl0']-S(CN[0], 'stat')['sl_obs'])/S(CN[0], 'stat')['bs'],
      (S(CN[1], 'stat')['sl0']-S(CN[1], 'stat')['sl_obs'])/S(CN[1], 'stat')['bs'],
      (S(CN[0], 'stat+sys')['sl0']-S(CN[0], 'stat+sys')['sl_obs'])/S(CN[0], 'stat+sys')['bs'],
      (S(CN[1], 'stat+sys')['sl0']-S(CN[1], 'stat+sys')['sl_obs'])/S(CN[1], 'stat+sys')['bs']),
   max(abs((S(c, "stat")['sl0']-S(c, "stat")['sl_obs'])/S(c, "stat")['bs']) for c in CN) < 2.0,
   "residual slope tension, stat-only: " +
   ", ".join(f"{c.strip()} {(S(c,'stat')['sl0']-S(c,'stat')['sl_obs'])/S(c,'stat')['bs']:+.1f} sigma" for c in CN) +
   "; stat+sys: " +
   ", ".join(f"{c.strip()} {(S(c,'stat+sys')['sl0']-S(c,'stat+sys')['sl_obs'])/S(c,'stat+sys')['bs']:+.1f} sigma" for c in CN))

eb_c = [S(c, "stat+sys")["eb"] for c in CN]; ehi_c = [S(c, "stat+sys")["ehi"] for c in CN]
ck("35c THE EXTERNAL FIELD IS NOT NEEDED AND IS NOT DETECTED -- which retires the item's own framing.  Fitting "
   "e_N freely returns %.3f [0, %.3f] (Ou) and %.3f [0, %.3f] (Eilers): consistent with zero, and the UPPER "
   "limits sit at or below the %.3f that M31 alone supplies.  So the correct statement is the opposite of the "
   "one the item expected: these curves put a CEILING on the Milky Way's external field, they do not demand one."
   % (eb_c[0], ehi_c[0], eb_c[1], ehi_c[1], eN_M31["canonical"]),
   max(eb_c) < 0.05,
   f"fitted e_N (stat+sys, canonical) = {eb_c[0]:.3f} [0, {ehi_c[0]:.3f}] and {eb_c[1]:.3f} [0, {ehi_c[1]:.3f}]; "
   f"alt footing {R35[(CN[0],'stat+sys','alt')]['eb']:.3f}/{R35[(CN[1],'stat+sys','alt')]['eb']:.3f}; M31 supplies "
   f"{eN_M31['canonical']:.3f}")

Ab_c = [S(c, "stat+sys")["Ab"] for c in CN]
ck("35d THE PRICE, AND IT IS THE INHERITED LIABILITY IN ITS SHARPEST FORM: the fit is bought with a baryonic "
   "amplitude A = %.2f-%.2f on Ou's own census, i.e. M_b = %.2f-%.2fe10 Msun against their 6.16e10 and "
   "McMillan's 6.68e10.  The framework needs 25-40 per cent more baryons than the published Milky Way has.  In "
   "velocity that is only 6-9 per cent, which is why the curve LOOKS fitted, but it is a real mass discrepancy "
   "and it is the same one hunt item 36 recorded"
   % (min(Ab_c), max(Ab_c), min(Ab_c)*OU_MB/Msun/1e10, max(Ab_c)*OU_MB/Msun/1e10),
   max(Ab_c)*OU_MB <= 1.15*MCM_MB,
   f"A = {Ab_c[0]:.2f} (Ou) and {Ab_c[1]:.2f} (Eilers) on M_b = {OU_MB/Msun:.2e}; required "
   f"M_b = {min(Ab_c)*OU_MB/Msun:.2e}-{max(Ab_c)*OU_MB/Msun:.2e} vs McMillan's {MCM_MB/Msun:.2e}")

Rr, vo, dvs, sysf, LO, HI = CURVES["Ou+2024   "]; dv = dvs
slo_c = [S(c, "stat")["sl_obs"] for c in CN]; bs_c = [S(c, "stat")["bs"] for c in CN]
A0f = S("Ou+2024   ", "stat+sys")["A0f"]
vN = np.sqrt(gN_ou(Rr, A0f)*Rr)
A_dm = float(vo[np.argmin(np.abs(Rr - 20*kpc))]**2/(gN_ou(np.array([20*kpc]))[0]*20*kpc))
info(f"Newtonian baryons alone, with the same one amplitude freedom, give an outer log-slope of "
     f"{logslope(Rr, vN, LO, HI):+.3f} and need A = {A_dm:.1f} at 20 kpc -- which is the statement 'dark matter'.")
info("Ou+2024's own LambdaCDM answer is a fitted CORED EINASTO halo with M_vir = 1.81e11 Msun (their abstract),")
info("i.e. two shape parameters plus a normalisation, and they say themselves it is in tension with globular-")
info("cluster, satellite and stream masses.  Bird+2022's NFW fits to halo stars give 0.55-1.00e12.  So the")
info("decline is uncomfortable for BOTH sides; it is not a clean LambdaCDM win, and it must not be reported as one.")
shf = rng.permutation(vo)
ck("M35 mutation control: shuffling v_c between radii destroys the outer-slope statistic the whole item turns on",
   abs(logslope(Rr, shf, LO, HI) - slo_c[0]) > 3*bs_c[0],
   f"shuffled slope {logslope(Rr, shf, LO, HI):+.3f} vs real {slo_c[0]:+.3f} +- {bs_c[0]:.3f}")
info("BOTH WAYS ON THE RESIDUAL 1-3 SIGMA, which is why item 35 is recorded as a MILD TENSION and not as the")
info("liability the item anticipated: (i) Ou+2024's own systematic")
info("budget reaches 15 per cent beyond 22 kpc, where the last four points carry the steepest part and have only")
info("7-22 stars each -- though the authors state explicitly that systematics 'are insufficient to explain the")
info("decline ... starting at R ~ 15 kpc'; (ii) the two independent pipelines agree on the slope, which removes")
info("the easy escape that one of them is broken; (iii) a 2025 re-analysis (arXiv:2507.23551) argues the")
info("recovered potentials are nearly SPHERICAL beyond 20 kpc, contradicting the axisymmetric Jeans equation used")
info("to derive them, so the steep part may be an artefact.  The liability is recorded anyway: the framework must")
info("not be allowed to wait for the data to be withdrawn.")

# =====================================================================================================
P(""); P("="*118); P("ITEM 38 -- halo-star dynamics: enclosed mass and sigma_r(r) beyond 50 kpc"); P("="*118)
# =====================================================================================================
B = {}
for line in open(os.path.join(DATA, "mw_halo_bird2022_jeans.txt")):
    if line.startswith("#") or not line.strip(): continue
    k, v = line.split()[:2]; B[k] = float(v)
info("THE ITEM ASKED FOR sigma_r(r) TO 100 kpc AND THAT CANNOT BE RUN.  Bird+2019 (AJ 157, 104) does measure")
info("sigma_r out past 100 kpc, but its arXiv source (1805.04503, downloaded and checked this session) contains")
info("FIGURES ONLY -- there is no table of sigma_r(r) anywhere in this literature chain.  The outermost")
info(f"machine-readable quantities are Bird+2022's enclosed masses at median radii of {B['JEANS_KG_r_kpc']:.0f} and "
     f"{B['JEANS_BHB_r_kpc']:.0f} kpc, and a two-parameter")
info("exponential fit to sigma_r(r) that its own authors call 'a fitting function only'.  Everything below is")
info("therefore a 25-73 kpc test.  ITEM 38 IS MARKED UNDERPOWERED FOR ITS OWN STATED RANGE, not null.")

MEAS = [("Jeans (K giants)", B["JEANS_KG_r_kpc"], B["JEANS_KG_M_e11"], math.hypot(B["JEANS_KG_Mrand_e11"], B["JEANS_KG_Msys_e11"])),
        ("Jeans (BHB)",      B["JEANS_BHB_r_kpc"], B["JEANS_BHB_M_e11"], math.hypot(B["JEANS_BHB_Mrand_e11"], B["JEANS_BHB_Msys_e11"])),
        ("TME  (K giants)",  B["TME_KG_r_kpc"],   B["TME_KG_M_e11"],   B["TME_KG_Mrand_e11"]),
        ("TME  (BHB)",       B["TME_BHB_r_kpc"],  B["TME_BHB_M_e11"],  B["TME_BHB_Mrand_e11"])]
def Mdyn(r, a0, MB, eN=0.0):
    gNn = G*MB/r**2
    return nu((gNn + eN*a0)/a0)*MB/Msun/1e11
info("")
info(f"{'measurement':>18}{'r[kpc]':>8}{'M_obs':>8}{'+-':>7}{'canon':>8}{'sig':>7}{'alt':>8}{'sig':>7}{'baryons':>9}")
sig = {"canonical": [], "alt": []}
for name, rkpc, M, dM in MEAS:
    r = rkpc*kpc; row = []
    for foot, a0 in A0.items():
        p = Mdyn(r, a0, MCM_MB); row += [p]; sig[foot].append((p - M)/dM)
    info(f"{name:>18}{rkpc:8.0f}{M:8.2f}{dM:7.2f}{row[0]:8.2f}{(row[0]-M)/dM:+7.2f}{row[1]:8.2f}"
         f"{(row[1]-M)/dM:+7.2f}{MCM_MB/Msun/1e11:9.3f}")
sig_c = np.array(sig["canonical"]); sig_a = np.array(sig["alt"])
sig_bar = np.array([(MCM_MB/Msun/1e11 - M)/dM for _, _, M, dM in MEAS])
ck("38a A REAL PASS, with nothing fitted anywhere: the kernel applied to the SAME baryon mass that fails to "
   "reproduce v_c(R0) reproduces all four of Bird's outer-halo mass measurements, on both footings, where the "
   "baryons alone are 3-4 sigma short and a factor 6-8 low.  This is the framework doing at 50-73 kpc exactly "
   "what it is for",
   np.max(np.abs(sig_c)) < 2.0 and np.max(np.abs(sig_a)) < 2.0,
   f"canonical residuals {np.array2string(sig_c, precision=2)} sigma, alt {np.array2string(sig_a, precision=2)}; "
   f"baryons alone {np.array2string(sig_bar, precision=1)} sigma")

# --- the distinctive half: saturation instead of a virial mass ---------------------------------------
info("")
for foot, a0 in A0.items():
    for eN in (0.02, 0.05):
        r_efe = math.sqrt(G*MCM_MB/(eN*a0))/kpc; Msat = nu_s(eN)*MCM_MB/Msun/1e11
        if foot == "canonical" and eN == 0.02: R38sat = (r_efe, Msat)
        info(f"{foot:10} e_N = {eN:.2f}: the external field takes over at r_EFE = {r_efe:5.0f} kpc and the "
             f"enclosed dynamical mass SATURATES at nu(e_N) M_b = {Msat:5.2f}e11 Msun and stops growing")
info(f"LambdaCDM's answer from the very same measurements (Bird's own NFW fits): M200 = "
     f"{10*B['NFW_JEANS_KG_M200_e12']:.1f}e11 (KG) to {10*B['NFW_JEANS_BHB_M200_e12']:.1f}e11 (BHB) Msun inside "
     f"r200 = {B['NFW_JEANS_KG_r200_kpc']:.0f}-{B['NFW_JEANS_BHB_r200_kpc']:.0f} kpc -- a mass that keeps CLIMBING "
     f"by a further factor {10*B['NFW_JEANS_KG_M200_e12']/4.3:.1f}-{10*B['NFW_JEANS_BHB_M200_e12']/4.3:.1f} beyond "
     f"the data.")
ck("38b the distinctive, falsifiable half of item 38 is a PREDICTION, not a measurement, and this sample cannot "
   "test it: the framework says the enclosed mass stops at about %.1fe11 Msun beyond r_EFE = %.0f kpc while the "
   "LambdaCDM fit to the same points extrapolates to %.1f-%.1fe11.  They differ by a factor 1.3-2.3, and the "
   "outermost measurement here is at 73 kpc, INSIDE r_EFE.  A mass at 150-250 kpc would separate them"
   % (R38sat[1], R38sat[0], 10*B["NFW_JEANS_KG_M200_e12"], 10*B["NFW_JEANS_BHB_M200_e12"]),
   R38sat[0] < 73.0,
   f"framework saturates at {R38sat[1]:.2f}e11 beyond {R38sat[0]:.0f} kpc (e_N = 0.02); the data stop at 73 kpc, "
   f"so the saturation is UNTESTED by this sample")

# --- the forward dispersion profile, and what e_N it demands -----------------------------------------
def sigr_g(r, gfunc, alpha, beta):
    """Spherical Jeans, rho ~ r^alpha, constant beta, in ANY radial field g(r).  Taking g as an argument
    is what lets the SAME estimator be run on the framework and on Bird's own NFW halo, which is the only
    way to know whether a failure here is the framework's or the estimator's."""
    s = np.geomspace(r, 6000*kpc, 4000); p = alpha + 2*beta
    return np.sqrt(float(TRAPZ(s**p*gfunc(s), s))*r**(-p))
def g_fw(a0, MB, eN=0.0):
    return lambda s: nu((G*MB/s**2 + eN*a0)/a0)*G*MB/s**2
def g_nfw(M200_e12, r200_kpc, c200, MB):
    """Baryons + Bird's own fitted NFW halo -- the LambdaCDM alternative, on the same tracer assumptions."""
    rs = r200_kpc*kpc/c200
    rho_s = M200_e12*1e12*Msun/(4*math.pi*rs**3*(math.log(1+c200) - c200/(1+c200)))
    def g(s):
        x = s/rs
        return G*(MB + 4*math.pi*rho_s*rs**3*(np.log(1+x) - x/(1+x)))/s**2
    return g
def sigr(r, a0, MB, alpha, beta, eN=0.0): return sigr_g(r, g_fw(a0, MB, eN), alpha, beta)
rgrid = np.array([25.0, 40.0, 55.0, 73.0])
sm_kg = B["KG_sigma0_kms"]*np.exp(-rgrid/B["KG_hr_kpc"])
sm_bhb = B["BHB_sigma0_kms"]*np.exp(-rgrid/B["BHB_hr_kpc"])
info("")
info(f"{'r [kpc]':>9}{'sig_r KG':>10}{'sig_r BHB':>11}{'  <- Bird+2022 exponential fits, the only tabulated form'}")
for i, rk in enumerate(rgrid):
    info(f"{rk:9.0f}{sm_kg[i]:10.1f}{sm_bhb[i]:11.1f}")
info(f"the two independent tracer populations agree to {100*np.max(np.abs(sm_kg/sm_bhb-1)):.0f} per cent over this "
     f"range, so the DECLINE itself is not a one-sample artefact; both fall by a factor "
     f"{sm_kg[0]/sm_kg[-1]:.1f} (KG) and {sm_bhb[0]/sm_bhb[-1]:.1f} (BHB) from 25 to 73 kpc.")
BETAS = (0.4, 0.7, 0.9)
info("")
info(f"{'':>26}" + "".join(f"{'beta='+str(b):>12}" for b in BETAS))
for eN in (0.0, 0.02, 0.05, 0.20, 0.50):
    ratios = []
    for bta in BETAS:
        pr = np.array([sigr(rk*kpc, A0["canonical"], MCM_MB, B["KG_alpha_out"], bta, eN)/1e3 for rk in rgrid])
        ratios.append(pr[-1]/pr[0])
    info(f"  predicted sigma_r(73)/sigma_r(25), e_N = {eN:4.2f}:" + "".join(f"{r:12.2f}" for r in ratios))
GN_KEP = lambda s: G*MCM_MB/s**2                 # the hardest fall any bounded mass can produce
rat = lambda gf, bta: (sigr_g(rgrid[-1]*kpc, gf, B["KG_alpha_out"], bta) /
                       sigr_g(rgrid[0]*kpc, gf, B["KG_alpha_out"], bta))
info(f"  {'LambdaCDM (Bird NFW, KG fit)':<38}" + "".join(
    f"{rat(g_nfw(B['NFW_JEANS_KG_M200_e12'], B['NFW_JEANS_KG_r200_kpc'], B['NFW_JEANS_KG_c'], MCM_MB), b):12.2f}"
    for b in BETAS))
info(f"  {'LambdaCDM (Bird NFW, BHB fit)':<38}" + "".join(
    f"{rat(g_nfw(B['NFW_JEANS_BHB_M200_e12'], B['NFW_JEANS_BHB_r200_kpc'], B['NFW_JEANS_BHB_c'], MCM_MB), b):12.2f}"
    for b in BETAS))
info(f"  {'pure Keplerian point mass (the floor)':<38}" + "".join(f"{rat(GN_KEP, b):12.2f}" for b in BETAS))
info(f"  {'MEASURED (KG / BHB)':<38}{sm_kg[-1]/sm_kg[0]:12.2f}{sm_bhb[-1]/sm_bhb[0]:12.2f}")
# what e_N does the observed decline require?  It may be UNREACHABLE -- report that rather than a nan.
eN_req = {}; FLOOR = rat(GN_KEP, 0.7)
for bta in BETAS:
    eg = np.geomspace(1e-3, 50.0, 240)
    rr = np.array([rat(g_fw(A0["canonical"], MCM_MB, e), bta) for e in eg])
    tgt = sm_kg[-1]/sm_kg[0]
    eN_req[bta] = float(np.interp(-tgt, -rr, eg)) if rr.min() <= tgt <= rr.max() else float("inf")
info("")
info(f"  the e_N the observed KG decline would require: " +
     ", ".join(f"beta={b}: " + ("UNREACHABLE at any e_N" if math.isinf(eN_req[b]) else f"{eN_req[b]:.2f}")
               for b in BETAS))
ck("38c NOT A TEST OF THE FRAMEWORK AT ALL -- MY OWN ESTIMATOR FAILS FIRST, AND SO DOES LambdaCDM.  The measured "
   "KG ratio sigma_r(73)/sigma_r(25) = %.2f is BELOW the pure-Keplerian floor %.2f, which no bounded mass "
   "distribution can go under with a single power-law tracer and constant anisotropy.  Bird's own NFW halo, fitted "
   "to these very stars, gives %.2f -- it misses the observed decline by as much as the framework does.  The "
   "excess steepness therefore lives in the tracer assumptions (a broken alpha, a rising beta(r), or the "
   "exponential fitting function), not in the gravity, and item 38c cannot discriminate."
   % (sm_kg[-1]/sm_kg[0], FLOOR,
      rat(g_nfw(B['NFW_JEANS_KG_M200_e12'], B['NFW_JEANS_KG_r200_kpc'], B['NFW_JEANS_KG_c'], MCM_MB), 0.7)),
   sm_kg[-1]/sm_kg[0] > FLOOR,
   f"measured {sm_kg[-1]/sm_kg[0]:.2f} (KG) and {sm_bhb[-1]/sm_bhb[0]:.2f} (BHB); Keplerian floor {FLOOR:.2f}; "
   f"framework e_N = 0 gives {rat(g_fw(A0['canonical'], MCM_MB, 0.0), 0.7):.2f}; LambdaCDM NFW gives "
   f"{rat(g_nfw(B['NFW_JEANS_KG_M200_e12'], B['NFW_JEANS_KG_r200_kpc'], B['NFW_JEANS_KG_c'], MCM_MB), 0.7):.2f} "
   f"(KG fit) and {rat(g_nfw(B['NFW_JEANS_BHB_M200_e12'], B['NFW_JEANS_BHB_r200_kpc'], B['NFW_JEANS_BHB_c'], MCM_MB), 0.7):.2f} (BHB fit)")
ck("38d the ONE thing the dispersion shape does say, and it is against the framework though weakly: the BHB "
   "sample's ratio %.2f IS reachable, and reaching it needs e_N = %s -- above the 0.05 the Milky Way has.  With "
   "no external field the framework predicts %.2f, i.e. an almost flat profile, because a logarithmic potential "
   "makes sigma_r exactly constant.  The framework's outer halo is too ISOTHERMAL, on both samples, by less than "
   "LambdaCDM's own miss."
   % (sm_bhb[-1]/sm_bhb[0],
      ("UNREACHABLE" if not np.isfinite(float(np.interp(-(sm_bhb[-1]/sm_bhb[0]),
        -np.array([rat(g_fw(A0['canonical'], MCM_MB, e), 0.7) for e in np.geomspace(1e-3, 50.0, 120)]),
        np.geomspace(1e-3, 50.0, 120)))) else
       f"{float(np.interp(-(sm_bhb[-1]/sm_bhb[0]), -np.array([rat(g_fw(A0['canonical'], MCM_MB, e), 0.7) for e in np.geomspace(1e-3, 50.0, 120)]), np.geomspace(1e-3, 50.0, 120))):.2f}"),
      rat(g_fw(A0["canonical"], MCM_MB, 0.0), 0.7)),
   float(np.interp(-(sm_bhb[-1]/sm_bhb[0]),
        -np.array([rat(g_fw(A0['canonical'], MCM_MB, e), 0.7) for e in np.geomspace(1e-3, 50.0, 120)]),
        np.geomspace(1e-3, 50.0, 120))) <= 0.05,
   f"BHB ratio {sm_bhb[-1]/sm_bhb[0]:.2f}; framework e_N = 0 gives {rat(g_fw(A0['canonical'], MCM_MB, 0.0), 0.7):.2f}; "
   f"the two tracer samples disagree with EACH OTHER about the steepness ({sm_kg[-1]/sm_kg[0]:.2f} vs "
   f"{sm_bhb[-1]/sm_bhb[0]:.2f}), which is itself the size of the systematic here")
info("MY OWN ESTIMATOR'S LIMITS, stated rather than hidden, and they are severe:")
info("  (i) sigma_r and M(<r) are NOT independent -- Bird's masses are derived FROM these dispersions through the")
info("      same Jeans equation, so 38a and 38c are two readings of one dataset, not two tests.  38c is the shape")
info("      of it and 38a the amplitude, and it is entirely consistent that one passes and the other fails.")
info("  (ii) the exponential sigma_r fit, the broken power-law tracer density and Bird's binned dispersions are")
info("      not mutually consistent point by point.  Inverting their own Jeans equation for the anisotropy with")
info("      their own published summary parameters returns:")
for rr in (50.0, 73.0):
    sm = (B["KG_sigma0_kms"]*math.exp(-rr/B["KG_hr_kpc"])*1e3)**2
    bb = (2*rr/B["KG_hr_kpc"] - B["KG_alpha_out"] - G*4.3e11*Msun/(rr*kpc*sm))/2
    info(f"        beta = {bb:+.2f} at r = {rr:.0f} kpc" + ("   (UNPHYSICAL: beta <= 1)" if bb > 1 else ""))
info("      so the size of the 38c failure should be read as indicative.  Bird themselves call the exponential")
info("      'a fitting function only, without direct physical interpretation'.")
ck("M38 mutation control: with the kernel switched off the baryons miss Bird's masses by a factor 6-8, and "
   "moving a_0 up by a decade misses them the other way -- so the pass in 38a is carried by the kernel at the "
   "framework's own a_0 and not by the mass model",
   np.max(np.abs(sig_bar)) > 3 and abs(Mdyn(73*kpc, 10*A0["canonical"], MCM_MB) - 4.3)/1.13 > 2,
   f"nu = 1 gives {MCM_MB/Msun/1e11:.3f}e11 ({sig_bar[0]:+.1f} sigma); a_0 x10 gives "
   f"{Mdyn(73*kpc, 10*A0['canonical'], MCM_MB):.2f}e11 "
   f"({(Mdyn(73*kpc, 10*A0['canonical'], MCM_MB)-4.3)/1.13:+.1f} sigma)")

# =====================================================================================================
P(""); P("="*118); P("CROSS -- the three lever arms against each other: one e_N?  one baryonic mass?"); P("="*118)
# =====================================================================================================
info("this is the only genuinely new thing in the three items: 35 and 38 both constrain ONE number, the external")
info("field e_N, from lever arms a factor of three apart in radius, and 34, 35 and 38a all make a demand on ONE")
info("number, the baryonic amplitude A.  Asking whether either comes out single-valued is the cross-check.")
info("")
e35, e35hi = S(CN[0], "stat+sys")["eb"], S(CN[0], "stat+sys")["ehi"]
e35b, e35bhi = S(CN[1], "stat+sys")["eb"], S(CN[1], "stat+sys")["ehi"]
eg120 = np.geomspace(1e-3, 50.0, 120)
e38 = float(np.interp(-(sm_bhb[-1]/sm_bhb[0]),
                      -np.array([rat(g_fw(A0["canonical"], MCM_MB, e), 0.7) for e in eg120]), eg120))
info(f"  e_N ALLOWED by the rotation curve at 12-27 kpc   (item 35, Ou)      {e35:6.3f}  [0, {e35hi:.3f}]")
info(f"  e_N ALLOWED by the rotation curve at 12-25 kpc   (item 35, Eilers)  {e35b:6.3f}  [0, {e35bhi:.3f}]")
info(f"  e_N NEEDED  by the halo dispersion at 25-73 kpc  (item 38d, BHB)    {e38:6.3f}")
info(f"  e_N NEEDED  by the halo dispersion at 25-73 kpc  (item 38c, KG)      unreachable at any e_N")
info(f"  e_N the Milky Way actually has (M31 + large-scale structure)        {eN_M31['canonical']:6.3f} + 0.01-0.03")
ck("CROSS-1 THE EXTERNAL FIELD IS SQUEEZED FROM BOTH SIDES AND THE WINDOW IS EMPTY.  The rotation curve at "
   "12-27 kpc puts a CEILING on it, e_N < %.3f, while the halo dispersion at 25-73 kpc needs a FLOOR of e_N = "
   "%.2f to bend its profile down -- %.0f times the ceiling.  One external field cannot do both jobs, so the "
   "framework's own escape hatch for the outer Milky Way is closed by the inner Milky Way.  This is new; it is "
   "also weak, because the dispersion side of it fails for LambdaCDM too (38c)"
   % (max(e35hi, e35bhi), e38, e38/max(e35hi, e35bhi)),
   e38 <= max(e35hi, e35bhi),
   f"ceiling from item 35 = {max(e35hi, e35bhi):.3f} (1 sigma, stat+sys, the looser of the two curves); floor "
   f"from item 38d = {e38:.2f}; M31 supplies {eN_M31['canonical']:.3f}")

# the three baryonic amplitudes
A_Kz = K0o/K0p
lo, hi = 0.3, 20.0; Rr, vo = CURVES["Ou+2024   "][0], CURVES["Ou+2024   "][1]
i0 = int(np.argmin(np.abs(Rr - 8.19*kpc)))
for _ in range(80):
    mid = math.sqrt(lo*hi)
    g = gN_ou(Rr[i0:i0+1], mid)
    lo, hi = (mid, hi) if math.sqrt(nu(g/A0["canonical"])[0]*g[0]*Rr[i0]) < vo[i0] else (lo, mid)
A_vc = math.sqrt(lo*hi)
A_M73 = 4.3e11*Msun/(nu_s(G*MCM_MB/(73*kpc)**2/A0["canonical"])*MCM_MB)
info("")
info("amplitude on the published baryonic mass demanded by each lever arm, canonical footing:")
info(f"   K_z,1.1 at R0            (item 34, |z| = 1.1 kpc, R ~ 8 kpc)   A = {A_Kz:.2f}")
info(f"   v_c at 8.2 kpc           (item 35, in the plane)               A = {A_vc:.2f}   <- the inherited liability")
info(f"   M(< 73 kpc) halo stars   (item 38a)                            A = {A_M73:.2f}")
ck("CROSS-2 the three lever arms do NOT agree on one baryonic mass, and the pattern is diagnostic: the vertical "
   "force at 1.1 kpc wants LESS than the published census (A = %.2f), the halo-star mass at 73 kpc wants about "
   "the census (A = %.2f), and the in-plane rotation speed at 8 kpc wants %.1f times more.  The framework's Milky "
   "Way is too flat -- too slow in the plane, too strong above it, and the spread is %.1fx across 8 to 73 kpc.  "
   "No single amplitude rescues items 34 and 35 together, so this is a SHAPE problem and adding baryons cannot "
   "fix it" % (A_Kz, A_M73, A_vc, max(A_Kz, A_vc, A_M73)/min(A_Kz, A_vc, A_M73)),
   max(A_Kz, A_vc, A_M73)/min(A_Kz, A_vc, A_M73) < 1.5,
   f"A(K_z,1.1) = {A_Kz:.2f}, A(M<73 kpc) = {A_M73:.2f}, A(v_c at R0) = {A_vc:.2f}")
info("the v_c normalisation entry is the repository's KNOWN liability (mi_aqual_mcmillan2017_2026.py; hunt item")
info("36), inherited and not re-discovered here.  What this section adds is that it is one face of a three-sided")
info(f"shape problem: the SAME kernel that needs {100*(A_vc-1):.0f} per cent MORE baryons to turn the disc at 8 kpc needs")
info(f"{100*(1-A_Kz):.0f} per cent FEWER to hold the disc down at 1.1 kpc, and those two demands are made of the same stars.")
info("That is a statement about the VERTICAL-TO-RADIAL ratio of the boost, which the repository's own full AQUAL")
info(f"solve puts at 1.024 -- and {A_vc/A_Kz:.2f} is not 1.02.  A curl-term correction of the size that solve reports cannot")
info("close it, so the gap lies either in the Milky Way's baryon distribution or in the kernel, not in the algebra.")
info("")
info("WHAT SURVIVES, stated as plainly as what does not: item 38a is a genuine zero-parameter success.  The same")
info("kernel and the same a_0 that fail on the vertical force and on the outer rotation curve turn a 6.7e10 Msun")
info(f"baryon census into 4-5e11 Msun of dynamical mass at 52-73 kpc, matching all four independent measurements")
info(f"within {max(np.max(np.abs(sig_c)), np.max(np.abs(sig_a))):.1f} sigma with nothing fitted.  The Milky Way is a hard case for the framework inside 25 kpc")
info("and an easy one beyond 50, and that radial split is the result of this group.")
sys.exit(ck.done())
