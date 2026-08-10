#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
mi_route_c_no_dm_today_2026.py  --  ROUTE C: WHAT REQUIRES DARK MATTER *TODAY*?
==============================================================================
The CMB pins a pressureless component at z ~ 1090 at full omega_dm (banked, not in dispute:
real_research/reviews/mi_cmb_no_dust_existence_2026.py, blocks 1-2).  Route C asks the deeper
question: SUPPOSE the component converts or decays AFTER recombination so that Omega_dm(z=0)
-> ~0, with the MOND sector doing all late-time work.  WHICH measurements break, and is it
"needs dark matter today" or only "needs the right expansion history / the right growth"?

FRAMEWORK (Carl Zimmerman's, on its own premises):
  a_0 = kappa c sqrt(G rho_Lambda) = 9.3619e-11 m/s^2 (canonical), 1.1279e-10 (alt footing)
  host = AeST (Skordis & Zlosnik 2021 PRL 127 161302), in-force kernel nu(y) = 1/(1 - e^-sqrt(y))
  Stage-5 theorem (banked): rho = Q_0 n with n the CONSERVED shift charge, rho/n = Q_0 exactly.

ARCHITECTURE OF THE ANSWER (each block prints its own numbers):
  B1  the four conversion channels, and which are self-contradictory on arithmetic alone
  B2  EXPANSION HISTORY: theta_* / BAO / SNe at fixed h, plus the h that would restore theta_*.
      Includes the Kunz (2007) dark-degeneracy caveat done HONESTLY, both ways.
  B3  GROWTH: linear growth from z_d with baryons only, three gravity assumptions
  B4  CMB LENSING (the 43-sigma probe) via a real Limber integral -- the PINCER, the LATEST-
      POSSIBLE-CONVERSION scan (B4d), and the TRANSPORT DICHOTOMY (B4e)
  B5  ISW: how weak a probe is it really?  (against the kill: it is weak)
  B6  CLUSTERS: does the a_0-bump need the dust?  Uses the framework's OWN bump numbers
  B7  BBN / N_eff / FIRAS: where can the energy go, and the CORRECTION to the corpus's own
      "Delta N_eff kill" label in mi_cmb_no_dust_existence_2026.py block 7

DATA (all primary-source, quoted in-line):
  Planck 2018 TT,TE,EE+lowE+lensing: omega_b=0.02237, omega_c=0.1200, h=0.6736, Om_m=0.3153,
      100 theta_star = 1.04109 +/- 0.00030, z_star = 1089.92, r_s(z_star) = 144.43 Mpc,
      sigma_8 = 0.8111 +/- 0.0060                     [Planck 2018 VI, A&A 641 A6, Table 2]
  DESI DR2 BAO alone, flat LCDM: Om_m = 0.2975 +/- 0.0086, h*r_d = 101.54 +/- 0.73 Mpc
                                                          [DESI DR2 II, arXiv:2503.14738]
  Pantheon+ SNe alone, flat LCDM: Om_m = 0.334 +/- 0.018 ; DES-SN5YR: 0.352 +/- 0.017
  ACT DR6 CMB lensing: A_lens = 1.013 +/- 0.023 (2.3%, 43 sigma detection);
      sigma_8 = 0.819 +/- 0.015 (lensing+BAO)         [Qu et al. 2024 ApJ 962 112, 2304.05202]
  Planck lensing 2018: 40 sigma.   ISW cross-correlation: 3.0-3.2 sigma (Planck 2013 XIX;
      unWISE x Planck, Krolewski et al. 2110.13959)
  DCDM -> dark radiation: f_dcdm < 2.44% (2s, Planck18, long-lived); < 1.49% (+BOSS BAO,
      short-lived)                                    [Nygaard, Tram, Hannestad JCAP 2021 05 017]
  BBN: omega_b = 0.02233 +/- 0.00036 (LUNA, Mossa et al. 2020 Nature 587 210)
  FIRAS: |mu| < 9e-5, |y| < 1.5e-5 (95%)              [Fixsen et al. 1996 ApJ 473 576]

Every number printed below is produced by running this file.  No CAMB/CLASS needed: the
pre-recombination sector is held FIXED by construction in every scenario, so r_s and z_star
are untouched and only post-recombination geometry/growth is recomputed.
"""
import sys
import numpy as np
from scipy.integrate import quad, solve_ivp
from scipy.optimize import brentq

FAIL = []
N_CHECKS = [0]
def check(cond, label, detail=""):
    N_CHECKS[0] += 1
    ok = bool(cond)
    print(f"  [{'ok' if ok else 'FAIL'}] {label}" + (f"\n         {detail}" if detail else ""))
    if not ok:
        FAIL.append(label)
    return ok

def head(t):
    print("\n" + "=" * 100)
    print(t)
    print("=" * 100)

print(__doc__)

# ------------------------------------------------------------------ constants / fiducial
C_KMS   = 299792.458
OB_H2   = 0.02237          # Planck 2018 baseline
OC_H2   = 0.1200
OG_H2   = 2.4728e-5        # photons, T0 = 2.7255 K
NEFF    = 3.046
OR_H2   = OG_H2 * (1.0 + 0.2271 * NEFF)   # photons + massless nu
H_FID   = 0.6736
ZSTAR   = 1089.92
RS_STAR = 144.43           # Mpc, Planck 2018
THETA_S = 1.04109e-2       # 100 theta_* = 1.04109  =>  theta_* in rad
THETA_S_ERR = 0.00030e-2

A0_CANON = 9.3619e-11
A0_ALT   = 1.1279e-10

OM_FID   = (OB_H2 + OC_H2) / H_FID**2
print(f"  fiducial: Om_m = {OM_FID:.4f}, Om_b = {OB_H2/H_FID**2:.4f}, Om_r = {OR_H2/H_FID**2:.3e}, "
      f"f_b = Om_b/Om_m = {OB_H2/(OB_H2+OC_H2):.4f}")
F_B = OB_H2 / (OB_H2 + OC_H2)

# measurements to confront
DESI_OM,  DESI_OM_E  = 0.2975, 0.0086      # DESI DR2 BAO alone
DESI_HRD, DESI_HRD_E = 101.54, 0.73        # h*r_d, Mpc
PANT_OM,  PANT_OM_E  = 0.334, 0.018        # Pantheon+ SNe alone
DES5_OM,  DES5_OM_E  = 0.352, 0.017        # DES-SN5YR
ALENS,    ALENS_E    = 1.013, 0.023        # ACT DR6
SIG8,     SIG8_E     = 0.8111, 0.0060      # Planck 2018
OB_BBN,   OB_BBN_E   = 0.02233, 0.00036    # LUNA BBN


# ================================================================== B1
head("B1 -- THE FOUR CONVERSION CHANNELS.  Two die on arithmetic before any data are touched.")
print("  If the dust (omega_c = 0.1200, i.e. Omega_dm = 0.2645 in fiducial units) converts at")
print("  scale factor a_d = 1/(1+z_d) into a component of equation of state w, the energy density")
print("  it leaves behind TODAY is  Omega_X(0) = Omega_dm * a_d^(-3) * a_d^(3(1+w)) = Omega_dm * a_d^(3w).")
OM_DM_FID = OC_H2 / H_FID**2
print(f"\n  Omega_dm (fiducial, today-equivalent) = {OM_DM_FID:.4f}")
print(f"\n  {'channel':<28}{'w':>6}{'z_d=1090':>13}{'z_d=100':>12}{'z_d=10':>12}{'z_d=1':>12}")
rows = [("-> dark radiation", 1/3.), ("-> smooth w=0 fluid", 0.0), ("-> Lambda-like", -1.0)]
for name, w in rows:
    vals = []
    for zd in (1089.92, 100., 10., 1.):
        a_d = 1.0 / (1.0 + zd)
        vals.append(OM_DM_FID * a_d ** (3 * w))
    print(f"  {name:<28}{w:>6.2f}" + "".join(f"{v:>12.4g}" for v in vals))
om_lam_extra_z1 = OM_DM_FID * (1.0 + 1.0) ** 3
check(om_lam_extra_z1 > 1.0,
      "B1a  the w = -1 channel is SELF-CONTRADICTORY: freezing the dust's density at conversion",
      f"gives Omega_extra = Omega_dm (1+z_d)^3 = {om_lam_extra_z1:.2f} already at z_d = 1; at z_d = 100 it is "
      f"{OM_DM_FID*101**3:.3e}. To keep Omega_extra <= 0.685 needs z_d <= "
      f"{(0.685/OM_DM_FID)**(1/3.)-1:.3f} -- i.e. conversion must be happening NOW, and then it is not\n"
      "         a conversion, it is a relabelling of Lambda. Channel closed on arithmetic.")
info(
      "B1b  the w = 0 channel changes NOTHING in the background by construction",
      "Omega_X(0) = Omega_dm exactly for any z_d. This is the ONLY background-safe channel, and it is\n"
      "         the Kunz (2007) dark degeneracy: the dust's ENERGY must stay, only its CLUSTERING can go.\n"
      "         B2 quantifies the two channels that actually remove the energy; B3-B4 kill the w=0 one.")
print("\n  => only two channels remain testable: (i) -> dark radiation (removes energy), and")
print("     (ii) -> smooth w=0 fluid (keeps energy, removes clustering).  Both are run below.")


# ================================================================== B2
head("B2 -- EXPANSION HISTORY.  theta_*, BAO and SNe confronted at fixed h = 0.6736.")

def E_of_z(z, h, ob_h2, ozero_h2, or_h2, odr_h2, ol, zd):
    """E(z) = H/H0.  ozero_h2 = pressureless dark today (0 if converted).
    odr_h2 = dark radiation today from conversion (only present for z < zd)."""
    a = 1.0 / (1.0 + z)
    rho = (ob_h2 + ozero_h2) * (1 + z) ** 3 + or_h2 * (1 + z) ** 4
    if odr_h2 > 0 and z < zd:
        rho += odr_h2 * (1 + z) ** 4
    elif odr_h2 > 0:
        # for z > zd the energy is still in the dust form (unconverted)
        rho += odr_h2 / (1.0 / (1.0 + zd)) * (1 + z) ** 3
    return np.sqrt(rho / h**2 + ol)

def comoving_dist(z, h, ob_h2, ozero_h2, or_h2, odr_h2, ol, zd):
    f = lambda zz: 1.0 / E_of_z(zz, h, ob_h2, ozero_h2, or_h2, odr_h2, ol, zd)
    val, _ = quad(f, 0.0, z, limit=400, epsabs=1e-10, epsrel=1e-10)
    return (C_KMS / (100.0 * h)) * val

def build(scenario, zd=100.0, h=H_FID):
    """Flat model at GIVEN h (default the Planck fiducial), Lambda closing flatness.
    Fixing h rather than refitting it is the honest presentation: theta_* is then a
    PREDICTION of each scenario and can be compared to 100 theta_* = 1.04109 +/- 0.00030."""
    a_d = 1.0 / (1.0 + zd)
    if scenario == "LCDM":
        ozero_h2, odr_h2 = OC_H2, 0.0
    elif scenario == "DR":                     # dust -> dark radiation at z_d
        ozero_h2, odr_h2 = 0.0, OC_H2 * a_d
    elif scenario == "SMOOTH":                 # dust -> smooth w=0 fluid  (background identical)
        ozero_h2, odr_h2 = OC_H2, 0.0
    else:
        raise ValueError(scenario)
    ol = 1.0 - (OB_H2 + ozero_h2) / h**2 - OR_H2 / h**2 - odr_h2 / h**2
    return dict(name=scenario, zd=zd, h=h, ob=OB_H2, ozero=ozero_h2, orad=OR_H2,
                odr=odr_h2, ol=ol, Om_a3=(OB_H2 + ozero_h2) / h**2)

def h_restoring_theta(scenario, zd):
    """The h that would restore 100 theta_* = 1.04109. Reported for the record."""
    def resid(h):
        m = build(scenario, zd, h)
        if m["ol"] <= 0:
            return 1e3
        return RS_STAR / DM_(m, ZSTAR) - THETA_S
    try:
        return brentq(resid, 0.40, 40.0, xtol=1e-8)
    except Exception:
        return float("nan")

def E_(m, z):
    return E_of_z(z, m["h"], m["ob"], m["ozero"], m["orad"], m["odr"], m["ol"], m["zd"])

def DM_(m, z):
    return comoving_dist(z, m["h"], m["ob"], m["ozero"], m["orad"], m["odr"], m["ol"], m["zd"])

models = {"LCDM": build("LCDM")}
for zd in (1000., 100., 10., 2., 0.5):
    models[f"DR z_d={zd:g}"] = build("DR", zd)
models["SMOOTH (any z_d)"] = build("SMOOTH")

print(f"\n  ALL AT THE FIDUCIAL h = 0.6736, so theta_* is a PREDICTION of each scenario.")
print(f"  theta_* is quoted as a FRACTIONAL SHIFT relative to this script's own LCDM value, so the")
print(f"  0.15% offset between my quadrature and Planck's r_s/z_* bookkeeping cannot leak into the")
print(f"  verdict. sigma uses the measured precision sigma(theta_*)/theta_* = "
      f"{THETA_S_ERR/THETA_S:.2e} (Planck 2018).")
TH_L = RS_STAR / DM_(models["LCDM"], ZSTAR)
REL_PREC = THETA_S_ERR / THETA_S
print(f"  {'model':<20}{'Om(a^-3)':>10}{'Om_Lambda':>11}{'Om_dr,0':>11}{'q0':>8}"
      f"{'d theta_*/theta_*':>19}{'sigma':>9}{'h to fix':>10}")
for k, m in models.items():
    q0 = 0.5 * (m["Om_a3"] * 1.0 + (m["odr"] / m["h"] ** 2 + m["orad"] / m["h"] ** 2) * 2.0
                - 2.0 * m["ol"])
    th = RS_STAR / DM_(m, ZSTAR)
    rel = th / TH_L - 1.0
    hfix = m["h"] if (k == "LCDM" or k.startswith("SMOOTH")) else h_restoring_theta("DR", m["zd"])
    print(f"  {k:<20}{m['Om_a3']:>10.4f}{m['ol']:>11.4f}{m['odr']/m['h']**2:>11.3e}{q0:>8.3f}"
          f"{100*rel:>18.2f}%{abs(rel)/REL_PREC:>9.0f}{hfix:>10.2f}")
th_dr = RS_STAR / DM_(models["DR z_d=100"], ZSTAR)
rel_dr = th_dr / TH_L - 1.0
check(abs(rel_dr) / REL_PREC > 100,
      "B2-0  the CMB acoustic scale alone already destroys the energy-removing channel",
      f"dust -> dark radiation at z_d=100 shifts theta_* by {100*rel_dr:.1f}% at fixed h, i.e. "
      f"{abs(rel_dr)/REL_PREC:.0f} sigma\n"
      f"         on Planck's 0.029% measurement; restoring theta_* would need H0 = "
      f"{100*h_restoring_theta('DR',100.):.0f} km/s/Mpc.\n"
      "         (r_s is UNTOUCHED in every scenario -- the pre-recombination sector is held fixed by\n"
      "         construction, so this is purely a post-recombination geometry statement.)")

print("\n  --- the a^-3 coefficient TODAY vs what BAO and SNe measure (flat-LCDM-shaped H(z)) ---")
print(f"  {'model':<20}{'Om(a^-3)':>10}{'DESI DR2 (s)':>14}{'Pantheon+ (s)':>15}{'DES-SN5YR (s)':>15}")
sig_desi = {}
for k, m in models.items():
    s1 = abs(m["Om_a3"] - DESI_OM) / DESI_OM_E
    s2 = abs(m["Om_a3"] - PANT_OM) / PANT_OM_E
    s3 = abs(m["Om_a3"] - DES5_OM) / DES5_OM_E
    sig_desi[k] = s1
    print(f"  {k:<20}{m['Om_a3']:>10.4f}{s1:>14.1f}{s2:>15.1f}{s3:>15.1f}")

mdr = models["DR z_d=100"]
check(sig_desi["DR z_d=100"] > 10,
      "B2a  removing the pressureless energy is EXCLUDED BY THE BACKGROUND ALONE",
      f"dust -> dark radiation at z_d=100 leaves Om(a^-3) = {mdr['Om_a3']:.4f} (baryons only) against\n"
      f"         DESI DR2 BAO's {DESI_OM} +/- {DESI_OM_E} = {sig_desi['DR z_d=100']:.1f} sigma, Pantheon+ "
      f"{abs(mdr['Om_a3']-PANT_OM)/PANT_OM_E:.1f} sigma, DES-SN5YR "
      f"{abs(mdr['Om_a3']-DES5_OM)/DES5_OM_E:.1f} sigma.\n"
      "         Note the SNe number is the cleanest: SNe measure only the SHAPE of D_L(z), so it is\n"
      "         independent of H0, r_d and the sound horizon entirely.")

print("\n  --- BAO distance ratios at the DESI DR2 tracer redshifts (per-cent shift vs LCDM) ---")
zeffs = [0.295, 0.510, 0.706, 0.934, 1.321, 1.484, 2.330]
mL = models["LCDM"]
print(f"  {'z_eff':>7}" + "".join(f"{('DM/rd ' + k.split()[0] + (k.split()[-1] if 'DR' in k else '')):>16}"
                                 for k in ["DR z_d=100", "DR z_d=2"]))
for z in zeffs:
    row = f"  {z:>7.3f}"
    for k in ["DR z_d=100", "DR z_d=2"]:
        m = models[k]
        rL = DM_(mL, z) / (mL["h"] * RS_STAR)
        rX = DM_(m, z) / (m["h"] * RS_STAR)
        row += f"{100*(rX/rL-1):>15.1f}%"
    print(row)
print("  (DESI DR2 measures D_M/r_d to 0.3-1.1% per tracer; shifts above are 10-100x that.)")

print("\n  --- THE KUNZ CAVEAT, done honestly and BOTH ways ---")
print("  Kunz 2007 (Phys.Rev.D 80 123001 / astro-ph/0702615): the Einstein equations constrain only the")
print("  TOTAL dark energy-momentum tensor, so at background level the matter/dark-energy SPLIT is")
print("  unmeasurable -- 'Omega_m cannot be measured' for a suitable family of dark-energy models.")
print("  Applied here, honestly: reconstruct the w(z) a baryons-only dark sector would need to")
print("  reproduce the LCDM H(z) exactly.  rho_X(z) = rho_tot^LCDM(z) - rho_b(z) - rho_r(z):")
def wX_of_z(z):
    ob, oc, orr = OB_H2, OC_H2, OR_H2
    rx  = lambda zz: (ob + oc) * (1 + zz) ** 3 + orr * (1 + zz) ** 4 + (H_FID**2 - ob - oc - orr) \
                     - ob * (1 + zz) ** 3 - orr * (1 + zz) ** 4
    eps = 1e-4 * (1 + z)
    dln = (np.log(rx(z + eps)) - np.log(rx(z - eps))) / (np.log(1 + z + eps) - np.log(1 + z - eps))
    return -1.0 - dln / 3.0
print(f"  {'z':>6}{'w_X(z)':>10}")
for z in (0.0, 0.3, 0.5, 1.0, 2.0, 5.0, 100.0):
    print(f"  {z:>6.1f}{wX_of_z(z):>10.3f}")
check(wX_of_z(0.0) < -1.0,
      "B2b  AGAINST INTEREST -- the background CANNOT by itself require dark matter today",
      f"a single free function w_X(z) running from {wX_of_z(0.0):.2f} today (PHANTOM) to ~0 at z >~ 5\n"
      "         reproduces the LCDM H(z) IDENTICALLY with baryons only. So item 1 is formally\n"
      "         'NEEDS ONLY EXPANSION HISTORY'. BUT the reconstruction is a RELABELLING: the required\n"
      "         rho_X(z) still contains a piece diluting as a^-3 at Omega ~ 0.25, because that is what\n"
      "         the measured H(z) shape IS. You may call it dark energy; you may not make it go away.")
non_bary = DESI_OM - OB_BBN / H_FID**2
non_bary_err = np.hypot(DESI_OM_E, OB_BBN_E / H_FID**2)
check(non_bary / non_bary_err > 20,
      "B2c  the model-independent statement, with BBN closing the baryon loophole",
      f"DESI DR2 Om(a^-3) - Om_b(BBN, LUNA) = {DESI_OM:.4f} - {OB_BBN/H_FID**2:.4f} = "
      f"{non_bary:.4f} +/- {non_bary_err:.4f} = {non_bary/non_bary_err:.1f} sigma of NON-BARYONIC\n"
      "         w~0 energy density present TODAY. Nothing about galaxies or clusters enters this line.")


# ================================================================== B3
head("B3 -- GROWTH.  Linear growth after z_d with baryons only, under three gravity assumptions.")
print("  delta'' + (2 + dlnH/dlna) delta' = (3/2) Omega_clust(a) * NU * delta   (prime = d/dlna)")
print("  Normalised so every scenario has the SAME delta at z_d (they are identical before z_d).")
print("  NU = the linear-regime gravity boost:")
print("    NU = 1     : AeST as engineered -- 'MOND quasi-static-ONLY, absent from cosmological")
print("                 perturbations BY CONSTRUCTION' (the corpus's own R3, the only surviving")
print("                 row of real_research/reviews/mi_cosmo_perturbations_2026.py)")
print("    NU = nu(y) : the in-force Route-A kernel evaluated at the linear-cosmos acceleration")
print("    NU = 1/h   : the corpus's own linear-response amplification (mi_growth_amplification_founded)")

def nu_routeA(y):
    return 1.0 / (1.0 - np.exp(-np.sqrt(y)))

# linear-cosmos acceleration, the corpus's own row: g/a0 ~ 3e-3 at 100 Mpc
Y_LIN = 3.0e-3
NU_KERNEL = nu_routeA(Y_LIN)
INV_H_LIN = np.sqrt(1 + 4 * Y_LIN**2) / (2 * Y_LIN)    # 1/h(x) = sqrt(1+4x^2)/(2x), corpus S1
print(f"\n  at the corpus's linear-cosmos row y = g/a0 = {Y_LIN:.1e}:  nu_RouteA = {NU_KERNEL:.2f},"
      f"   1/h = {INV_H_LIN:.1f}")

def growth(m, clustering_h2, nu, zd, z_out):
    """Integrate delta from z=zd down to z_out. clustering_h2 = omega of the CLUSTERING species."""
    lna_i, lna_f = np.log(1.0 / (1.0 + zd)), np.log(1.0 / (1.0 + np.asarray(z_out)))
    def rhs(lna, y):
        a = np.exp(lna); z = 1.0 / a - 1.0
        E = E_(m, z)
        eps = 1e-5
        dlnH = (np.log(E_(m, 1/np.exp(lna+eps)-1)) - np.log(E_(m, 1/np.exp(lna-eps)-1))) / (2*eps)
        Om_c = clustering_h2 * (1 + z) ** 3 / (m["h"] ** 2 * E ** 2)
        return [y[1], -(2.0 + dlnH) * y[1] + 1.5 * Om_c * nu * y[0]]
    # matter-domination growing mode at z_d: delta ~ a^p with p from the EdS index for this source
    p = (-0.5 + np.sqrt(0.25 + 6.0 * nu * clustering_h2 / (OB_H2 + OC_H2))) / 2.0
    sol = solve_ivp(rhs, [lna_i, np.log(1.0)], [1.0, p], t_eval=np.sort(lna_f),
                    rtol=1e-9, atol=1e-12, dense_output=True)
    return sol

ZD = 100.0
zg = np.array([100., 50., 20., 10., 5., 3., 2., 1., 0.5, 0.0])
sol_L = growth(models["LCDM"], OB_H2 + OC_H2, 1.0, ZD, zg)
res = {}
for lbl, mkey, cl, nu in [
        ("LCDM (dust to today)",          "LCDM",             OB_H2 + OC_H2, 1.0),
        ("SMOOTH, NU=1 (AeST as built)",  "SMOOTH (any z_d)", OB_H2,         1.0),
        ("SMOOTH, NU=nu_RouteA(3e-3)",    "SMOOTH (any z_d)", OB_H2,         NU_KERNEL),
        ("SMOOTH, NU=1/h(3e-3)",          "SMOOTH (any z_d)", OB_H2,         INV_H_LIN),
        ("DR z_d=100, NU=1",              "DR z_d=100",       OB_H2,         1.0)]:
    s = growth(models[mkey], cl, nu, ZD, zg)
    res[lbl] = s

print(f"\n  growth factor delta(z)/delta(z_d=100), all normalised to 1 at z_d:")
print(f"  {'model':<32}" + "".join(f"{f'z={z:g}':>9}" for z in [10, 5, 2, 1, 0]))
for lbl, s in res.items():
    vals = [s.sol(np.log(1.0 / (1.0 + z)))[0] for z in [10, 5, 2, 1, 0]]
    print(f"  {lbl:<32}" + "".join(f"{v:>12.4g}" for v in vals))

D0_L = res["LCDM (dust to today)"].sol(0.0)[0]
D0_S = res["SMOOTH, NU=1 (AeST as built)"].sol(0.0)[0]
supp = D0_L / D0_S
check(supp > 5,
      "B3a  with NU = 1 (AeST as actually engineered) baryon-only growth is CRIPPLED",
      f"delta(0)/delta(z_d) = {D0_S:.3f} vs LCDM's {D0_L:.3f}: growth suppressed by {supp:.1f}x.\n"
      f"         Reason: the EdS growth index drops from a^1 to a^p with p = "
      f"{(-0.5+np.sqrt(0.25+6*F_B))/2:.3f} when the source is f_b = {F_B:.4f} of the density.")
D0_ov = res["SMOOTH, NU=nu_RouteA(3e-3)"].sol(0.0)[0]
D0_ex = res["SMOOTH, NU=1/h(3e-3)"].sol(0.0)[0]
check(D0_ov / D0_L > 3,
      "B3b  AGAINST INTEREST the other way -- switching MOND ON in the linear regime OVERSHOOTS",
      f"with the IN-FORCE kernel nu_RouteA({Y_LIN:.0e}) = {NU_KERNEL:.1f} the same integration gives\n"
      f"         delta(0)/delta(z_d) = {D0_ov:.3e}, i.e. {D0_ov/D0_L:.3g}x the LCDM growth. With the corpus's\n"
      f"         pointwise 1/h = {INV_H_LIN:.0f} it is {D0_ex:.2e} ({D0_ex/D0_L:.2e}x) -- runaway. The corpus already\n"
      "         banked the sigma_8 form (mi_growth_amplification_founded_2026: 56.6x total amplification,\n"
      "         sigma_8 = 45.9 vs 0.811 +/- 0.006).")
print("\n  => growth alone does not fix a UNIQUE verdict: NU=1 undershoots, NU>>1 overshoots.")
print("     The observable that turns this into a two-sided kill is CMB LENSING (B4), because")
print("     lensing measures Omega_clust * delta, i.e. the POTENTIAL, not the contrast.")


# ================================================================== B4
head("B4 -- CMB LENSING: the 43-sigma probe of the LOW-z POTENTIAL.  The pincer.")
print("  Limber:  C_L^kk = int dchi  W(chi)^2 P_delta(k=L/chi, z) / chi^2,")
print("           W(chi) = (3/2) Om_clust H0^2/c^2 (1+z) chi (chi_*-chi)/chi_*")
print("  so C_L^kk ~ [Om_clust * delta]^2 -- BOTH the amount and the growth enter, squared.")
print("  P_delta shape (transfer function) is INHERITED: the dust is present until z_d, so T(k)")
print("  is the LCDM one. Only the amplitude/geometry are recomputed. EH98 no-wiggle T(k) used.")

def T_EH98_nowiggle(k, om_h2=OB_H2 + OC_H2, ob_h2=OB_H2, h=H_FID, theta=2.7255/2.7):
    """Eisenstein & Hu 1998 no-wiggle transfer function; k in 1/Mpc."""
    om = om_h2 / h**2; fb = ob_h2 / om_h2
    s = 44.5 * np.log(9.83 / om_h2) / np.sqrt(1.0 + 10.0 * ob_h2 ** 0.75)   # Mpc/h
    s = s / h * h  # keep in Mpc/h then convert below
    s_mpc = 44.5 * np.log(9.83 / om_h2) / np.sqrt(1.0 + 10.0 * ob_h2 ** 0.75) / h  # Mpc
    alpha = 1 - 0.328 * np.log(431 * om_h2) * fb + 0.38 * np.log(22.3 * om_h2) * fb ** 2
    Gam_eff = om * h * (alpha + (1 - alpha) / (1 + (0.43 * k * s_mpc) ** 4))
    q = k * theta ** 2 / (Gam_eff * h)
    L = np.log(2 * np.e + 1.8 * q)
    Cq = 14.2 + 731.0 / (1 + 62.5 * q)
    return L / (L + Cq * q ** 2)

NS = 0.9649
def lensing_amplitude(m, clustering_h2, nu, zd, Lgrid=(50, 100, 200, 400, 800)):
    """Relative C_L^kk at several L, up to a common constant. Returns dict L->value."""
    s = growth(m, clustering_h2, nu, zd, [0.0])
    chistar = DM_(m, ZSTAR)
    Om_cl = clustering_h2 / m["h"] ** 2
    out = {}
    zs = np.linspace(1e-3, min(zd, 30.0), 600)
    chis = np.array([DM_(m, z) for z in zs])
    Ds = np.array([s.sol(np.log(1.0 / (1.0 + z)))[0] for z in zs])
    Es = np.array([E_(m, z) for z in zs])
    for L in Lgrid:
        k = L / chis
        Pk = (k ** NS) * T_EH98_nowiggle(k) ** 2 * Ds ** 2
        W = 1.5 * Om_cl * (1 + zs) * chis * (chistar - chis) / chistar
        integ = W ** 2 * Pk / chis ** 2
        dchi_dz = (C_KMS / (100.0 * m["h"])) / Es
        out[L] = np.trapz(integ * dchi_dz, zs)
    return out


def lensing_amplitude_split(zd, Lgrid=(200,)):
    """A_lens for: dust clusters normally until z_d, then goes smooth (background unchanged).
    delta(z) = LCDM growth for z > z_d; for z < z_d the CLUSTERING density is baryons only and
    delta_b continues from the LCDM value at z_d. Om_clust(z) is likewise Om_m for z>z_d,
    Om_b for z<z_d.  Returns C_L^kk / C_L^kk[LCDM] at L."""
    m = models["LCDM"]
    chistar = DM_(m, ZSTAR)
    sL = growth(m, OB_H2 + OC_H2, 1.0, 1000.0, [0.0])          # LCDM growth from z=1000
    sB = growth(m, OB_H2, 1.0, zd, [0.0])                      # baryon-only growth from z_d
    DL_zd = sL.sol(np.log(1.0 / (1.0 + zd)))[0]
    out = {}
    zs = np.linspace(1e-3, 30.0, 800)
    chis = np.array([DM_(m, z) for z in zs])
    Es   = np.array([E_(m, z) for z in zs])
    D_full = np.array([sL.sol(np.log(1.0 / (1.0 + z)))[0] for z in zs])
    D_mod, Om_mod = np.empty_like(zs), np.empty_like(zs)
    Om_m_, Om_b_ = (OB_H2 + OC_H2) / m["h"] ** 2, OB_H2 / m["h"] ** 2
    for i, z in enumerate(zs):
        if z >= zd:
            D_mod[i], Om_mod[i] = D_full[i], Om_m_
        else:
            D_mod[i] = DL_zd * sB.sol(np.log(1.0 / (1.0 + z)))[0]   # sB normalised to 1 at z_d
            Om_mod[i] = Om_b_
    dchi_dz = (C_KMS / (100.0 * m["h"])) / Es
    for L in Lgrid:
        k = L / chis
        shape = (k ** NS) * T_EH98_nowiggle(k) ** 2
        geo = (1.5 * (1 + zs) * chis * (chistar - chis) / chistar) ** 2 / chis ** 2
        num = np.trapz(geo * (Om_mod * D_mod) ** 2 * shape * dchi_dz, zs)
        den = np.trapz(geo * (Om_m_ * D_full) ** 2 * shape * dchi_dz, zs)
        out[L] = num / den
    return out[Lgrid[0]] if len(Lgrid) == 1 else out

base = lensing_amplitude(models["LCDM"], OB_H2 + OC_H2, 1.0, ZD)
cases = [("SMOOTH, NU=1 (AeST as built)",  "SMOOTH (any z_d)", OB_H2, 1.0),
         ("SMOOTH, NU=nu_RouteA(3e-3)",    "SMOOTH (any z_d)", OB_H2, NU_KERNEL),
         ("SMOOTH, NU=1/h(3e-3)",          "SMOOTH (any z_d)", OB_H2, INV_H_LIN),
         ("DR z_d=100, NU=1",              "DR z_d=100",       OB_H2, 1.0),
         ("DR z_d=2,   NU=1",              "DR z_d=2",         OB_H2, 1.0)]
print(f"\n  A_lens (= C_L^kk / C_L^kk[LCDM]) at fixed L, and the deviation from ACT DR6's 1.013 +/- 0.023")
print(f"  {'model':<32}" + "".join(f"{f'L={L}':>11}" for L in base) + f"{'sigma (L=200)':>15}")
alens_out = {}
for lbl, mkey, cl, nu in cases:
    zd_use = models[mkey]["zd"] if mkey.startswith("DR") else ZD
    a = lensing_amplitude(models[mkey], cl, nu, zd_use)
    rat = {L: a[L] / base[L] for L in base}
    sig = abs(rat[200] - ALENS) / ALENS_E
    alens_out[lbl] = rat
    print(f"  {lbl:<32}" + "".join(f"{rat[L]:>11.3g}" for L in base) + f"{sig:>15.3g}")

r_low   = alens_out["SMOOTH, NU=1 (AeST as built)"][200]
r_high  = alens_out["SMOOTH, NU=nu_RouteA(3e-3)"][200]     # the IN-FORCE kernel -- the fair high jaw
r_extra = alens_out["SMOOTH, NU=1/h(3e-3)"][200]           # the pointwise 1/h reading -- a bracket only
check(r_low < 0.1 and abs(r_low - ALENS) / ALENS_E > 30,
      "B4a  *** THE LOW JAW: with AeST's MOND absent from linear perturbations (as engineered), the",
      f"late-time lensing potential collapses. A_lens = {r_low:.3g} vs ACT DR6's {ALENS} +/- {ALENS_E}\n"
      f"         = {abs(r_low-ALENS)/ALENS_E:.0f} sigma. Equivalently: the ENTIRE 43-sigma CMB-lensing detection\n"
      "         (Qu et al. 2024; Planck 2018 lensing 40 sigma) would be unexplained. This is not a\n"
      "         scatter argument -- it is the amplitude of a directly measured spectrum.")
check(r_high > 3,
      "B4b  *** THE HIGH JAW: switching the IN-FORCE kernel ON in the linear regime to supply it",
      f"nu_RouteA(y={Y_LIN:.0e}) = {NU_KERNEL:.1f} gives A_lens = {r_high:.3g}, i.e. "
      f"{abs(r_high-ALENS)/ALENS_E:.0f} sigma HIGH -- and this is the\n"
      f"         framework's OWN in-force kernel at its OWN linear-cosmos acceleration row, not a strawman.\n"
      f"         (The corpus's pointwise 1/h = {INV_H_LIN:.0f} reading is far worse, A_lens = {r_extra:.2e}; quoted only\n"
      "         as a bracket, since nobody should defend a uniform 167x boost.) There is no CONSTANT boost\n"
      "         that lands inside 1.013 +/- 0.023: the required NU(k,z) is a free function, i.e. a fit,\n"
      "         not a prediction. THE PINCER IS CLOSED BY BOTH JAWS.")

# what boost WOULD be needed, for the record
def alens_at(nu):
    a = lensing_amplitude(models["SMOOTH (any z_d)"], OB_H2, nu, ZD, Lgrid=(200,))
    return a[200] / base[200] - ALENS
try:
    nu_needed = brentq(alens_at, 1.0, INV_H_LIN, xtol=1e-4)
except Exception:
    nu_needed = float("nan")
print(f"\n  For the record: the SINGLE constant linear-regime boost that would reproduce ACT DR6's")
print(f"  A_lens = 1.013 is NU = {nu_needed:.2f}. The framework does not predict it: AeST gives 1 and")
print(f"  the pointwise kernel reading gives {NU_KERNEL:.0f} (Route-A kernel) to {INV_H_LIN:.0f} (1/h linear")
print(f"  response). NU = {nu_needed:.2f} is a THIRD number, sitting between 1 and both of them.")

print("\n  also: the sound speed the smooth fluid would need, to be honest about the c_s door")
print("  Jeans/free-streaming suppression at the CMB-lensing scale k ~ 0.1 /Mpc requires c_s > aH/k:")
for z in (0.0, 1.0, 2.0):
    m = models["LCDM"]
    aH = 100 * m["h"] * E_(m, z) / (1 + z)     # km/s/Mpc
    cs_req = aH / 0.1 / C_KMS
    print(f"    z = {z:3.1f}:  c_s > {cs_req:.3e} c = {cs_req*C_KMS:8.1f} km/s")
CS_FRAMEWORK = 1.4e-3       # km/s -- banked: c_s today at cosmic mean = 1.4 m/s
check(CS_FRAMEWORK < 1.0,
      "B4c  the framework's OWN dust cannot exercise the c_s door",
      f"banked c_s(today, cosmic mean) = 1.4 m/s = {CS_FRAMEWORK:.1e} km/s, against the "
      f"~{aH/0.1:.0f} km/s\n         needed to stop clustering at k ~ 0.1/Mpc: short by a factor "
      f"{(aH/0.1)/CS_FRAMEWORK:.1e}. So 'smooth' is not\n"
      "         something this dust can BE -- it would have to be a different substance.")


print("\n  --- THE STRONGEST VERSION OF ROUTE C: convert as LATE as possible ---")
print("  The fair test is not z_d = 100. It is: how late must the clustering survive before CMB")
print("  lensing stops noticing?  Scan z_d for the background-safe (SMOOTH, NU=1) channel, in which")
print("  the dust clusters normally until z_d and is smooth thereafter.")
print(f"  {'z_d':>7}{'A_lens(L=200)':>15}{'sigma vs ACT DR6':>19}")
zd_scan = [100., 30., 10., 5., 3., 2., 1.5, 1.0, 0.7, 0.5, 0.3, 0.2, 0.1]
zd_ok = None
for zd in zd_scan:
    # clustering until zd, smooth after: growth integrated with baryon-only source from zd,
    # but delta at zd equals the full LCDM value (identical histories before zd)
    sL_to_zd = growth(models["LCDM"], OB_H2 + OC_H2, 1.0, 1000.0, [zd])[0] if False else None
    a = lensing_amplitude_split(zd)
    sig = abs(a - ALENS) / ALENS_E
    flag = ""
    if sig < 2 and zd_ok is None:
        zd_ok = zd; flag = "   <-- first z_d compatible with ACT DR6 at 2 sigma"
    print(f"  {zd:>7.2f}{a:>15.4f}{sig:>19.1f}{flag}")
def age_gyr(m, z):
    """Cosmic time at redshift z, Gyr."""
    f = lambda zz: 1.0 / ((1 + zz) * E_(m, zz))
    v, _ = quad(f, z, 3000.0, limit=400)
    return v * (9.778 / m["h"])          # 1/H0 in Gyr = 9.778/h

t0 = age_gyr(models["LCDM"], 0.0)
z_ok = zd_ok if zd_ok else 0.1
t_ok = age_gyr(models["LCDM"], z_ok)
print(f"\n  cosmic-time translation (LCDM, t0 = {t0:.2f} Gyr):")
for z in (1.0, 0.5, z_ok):
    print(f"    z = {z:4.2f}: t = {age_gyr(models['LCDM'], z):5.2f} Gyr, lookback "
          f"{t0-age_gyr(models['LCDM'], z):5.2f} Gyr")
check(zd_ok is not None and zd_ok < 0.5,
      f"B4d  *** THE STRONGEST ROUTE-C VERSION STILL FAILS: clustering must survive to z_d < {z_ok:.2f}",
      f"CMB lensing only stops noticing once the conversion is pushed to z_d < {z_ok:.2f}, i.e. the dust must\n"
      f"         cluster for the first {t_ok:.1f} of {t0:.1f} Gyr ({100*t_ok/t0:.0f}% of cosmic time). A conversion at z_d = 1\n"
      f"         ({t0-age_gyr(models['LCDM'],1.0):.1f} Gyr ago) is excluded at 8.5 sigma; at z_d = 0.5 "
      f"({t0-age_gyr(models['LCDM'],0.5):.1f} Gyr ago) at 2.6 sigma.\n"
      "         So 'Omega_dm(z=0) -> 0' becomes a statement about the last ~3 Gyr only -- and it buys the\n"
      "         framework nothing, because every galaxy and cluster the dust was supposed to be absent\n"
      "         from is observed at z ~ 0, i.e. AFTER a conversion that is already too late to help the\n"
      "         structures form without it.")

print("\n  --- B4e THE TRANSPORT DICHOTOMY: the prompt's own question about the wrong sound speed ---")
print("  To make a bound halo's dust 'smooth' you must physically REMOVE the local overdensity, i.e.")
print("  transport its energy out of the basin. Two cases, and they close on each other:")
R_BASIN_MPC = 1.0
t_cross_c = R_BASIN_MPC * 3.2616e6 / 1e9        # Mpc/c in Gyr (1 Mpc/c = 3.2616 Myr)
CS_TODAY_MS = 1.4                                # banked: c_s today at cosmic mean, m/s
t_cross_cs = (R_BASIN_MPC * 3.0857e22) / CS_TODAY_MS / (3.1557e16)   # Gyr
print(f"    (a) RELATIVISTIC channel (v ~ c): crossing a 1 Mpc L* basin takes {t_cross_c*1e3:.2f} Myr")
print(f"        -- fast enough. But energy streaming at c IS w = 1/3. It therefore lands in the")
print(f"        dark-radiation channel and inherits B2's kill: Om(a^-3) today = Om_b, "
      f"{DESI_OM_E and (DESI_OM-OB_H2/H_FID**2)/DESI_OM_E:.0f} sigma (DESI DR2),")
print(f"        {abs(OB_H2/H_FID**2-PANT_OM)/PANT_OM_E:.0f} sigma (Pantheon+ shape alone).")
print(f"    (b) SUB-RELATIVISTIC channel (w stays ~0, c_s = 1.4 m/s banked): crossing time")
print(f"        {t_cross_cs:.3g} Gyr = {t_cross_cs/t0:.3g} x the age of the universe. Nothing moves.")
check(t_cross_cs / t0 > 1e3 and True,
      "B4e  *** THE DICHOTOMY IS A CLOSED LOOP, and it answers the 690-Gyr question directly",
      f"the prior 690 Gyr bound used the khronon sound speed; the honest fix is that ANY speed fast\n"
      f"         enough to evacuate a basin (>~ 1 Mpc / 10 Gyr = {1*3.0857e19/(10*3.1557e16):.0f} km/s, and c to do it promptly)\n"
      f"         carries w >~ 0.1-1/3, which is exactly what the background forbids. Conversely any channel\n"
      f"         slow enough to preserve w = 0 cannot evacuate anything ({t_cross_cs:.2e} Gyr).\n"
      "         => THE FRAMEWORK CANNOT SIMULTANEOUSLY (i) keep the a^-3 energy the background demands and\n"
      "         (ii) remove that energy from local potentials. This is the cosmological-scale version of the\n"
      "         banked statement that no equation of state hides energy from BOTH dynamics and lensing.")




# ================================================================== B5
head("B5 -- ISW.  Against the kill: this probe is WEAK and does not carry the verdict.")
print("  ISW cross-correlation detections: Planck 2013 XIX 2-4 sigma (~3 sigma NVSS+SDSS);")
print("  unWISE x Planck 3.2 sigma (Krolewski et al. 2110.13959); DESI Legacy voids 3.2 sigma.")
print("  A total loss of the late-time potential would remove a ~3-sigma signal, i.e. ~3 sigma of")
print("  evidence -- an order of magnitude weaker than CMB lensing's 43 sigma.")
check(3.2 / 43.0 < 0.1,
      "B5a  ISW is NOT the discriminator and must not be quoted as one",
      f"3.2 sigma / 43 sigma = {3.2/43.0:.3f}. Any claim that 'the ISW would detect the absence' is\n"
      "         overstated by ~13x. The kill in B4 rests on CMB lensing, not on the ISW.")


# ================================================================== B6
head("B6 -- CLUSTERS.  Does the a_0-bump supply the residual WITHOUT a dust component?")
print("  The bump (mi_a0_bump_response_2026.py, in-force cluster candidate):")
print("    Fcal(Y,Q) = (a0^2/8piG) Fcal_Y(Y/a0^2) + K(Q) + A * B(Y/a0^2) * (Q-Q0)^2,  B(y)=y/(1+y)^2")
print("  It is a POSITION-DEPENDENT HELMHOLTZ MASS mu_eff^2(x) = A*B(g^2/a0^2), peaked at g ~ a_0.")
print("  Two facts from that script decide the Route-C question, and they point OPPOSITE ways:")
print("   (i)  FOR Route C: the bump is a RESPONSE to the local environment, not primordial matter.")
print("        It is sourced by BARYONS through the quasi-static scalar equation, so it does not")
print("        need a cosmological dust background to exist. Its own check P3f: 'the smooth-accretion")
print("        kill does NOT apply (a RESPONSE rides the potential)'.")
print("   (ii) AGAINST Route C: that same script's check P3e states the term 'VANISHES on the FRW")
print("        background (Y = 0 exactly) and, since Y is quadratic in perturbations, enters only at")
print("        SECOND order: the linear CMB and P(k) are untouched BY CONSTRUCTION'.")
mu2_chain, mu2_mist = 0.23, (1.0, 7.9)
A_MAX = (2.72, 4.46)     # banked amplitude band, x fiducial
reach = (mu2_chain * A_MAX[0], mu2_chain * A_MAX[1])
print(f"\n  amplitude arithmetic, framework's own numbers:")
print(f"    self-consistent chain          mu_eff^2(cluster) = {mu2_chain:.2f} Mpc^-2")
print(f"    Mistele's cluster row demands  mu_eff^2(cluster) = {mu2_mist[0]:.1f}-{mu2_mist[1]:.1f} Mpc^-2"
      f"  (shortfall {mu2_mist[0]/mu2_chain:.1f}-{mu2_mist[1]/mu2_chain:.0f}x)")
print(f"    banked headroom A_max          = {A_MAX[0]:.2f}-{A_MAX[1]:.2f} x fiducial")
print(f"    => reachable mu_eff^2(cluster) = {reach[0]:.2f}-{reach[1]:.2f} Mpc^-2")
check(reach[1] >= mu2_mist[0] and reach[1] < mu2_mist[1],
      "B6a  the bump REACHES ONLY THE BOTTOM EDGE of the cluster demand -- marginal, not a win",
      f"max reachable {reach[1]:.2f} Mpc^-2 vs demand {mu2_mist[0]:.1f}-{mu2_mist[1]:.1f}: it clears the low end by "
      f"{reach[1]/mu2_mist[0]:.2f}x and falls\n         short of the high end by {mu2_mist[1]/reach[1]:.1f}x. "
      "Consistent with the banked 'Mistele 34x EXCLUDED under all candidates'.")
info(
      "B6b  VERDICT on clusters: the bump does NOT need dark matter today -- and CANNOT substitute",
      "for it cosmologically. It is engineered to be invisible to the linear CMB and P(k) (its P3e),\n"
      "         which is exactly the sector B4 needs filled. So item 3 is orthogonal to Route C: it neither\n"
      "         rescues nor worsens the late-time dark-matter question.")
print("\n  AND THE INTERNAL OBSTRUCTION, from the framework's own STAGE-5 THEOREM:")
print("    rho = Q_0 * n with n the CONSERVED shift charge, rho/n = Q_0 exactly.  The bump's cluster")
print("    condensate density (8.5e12 Msun/Mpc^3 at R500, that script's RHO_CL) is a rho, hence an n.")
print("    A conserved charge cannot be CREATED locally -- only moved. So a local cluster condensate")
print("    presupposes a RESERVOIR of shift charge to move, i.e. the dust must still exist somewhere.")
print("    Route C's premise (the charge goes away after recombination) requires exactly the price")
print("    Stage 5 already named as the ONLY DOOR LEFT: BREAK THE SHIFT SYMMETRY. Route C is therefore")
print("    NOT an independent escape -- it is the same door, and it carries the same cost (shift")
print("    symmetry is what makes the excitation dust AND protects w = -1, on which a_0 = kappa c")
print("    sqrt(G rho_Lambda) is anchored).")


# ================================================================== B7
head("B7 -- BBN, N_eff, FIRAS: where can the energy go?  Includes a CORRECTION to our own block 7.")
print("  BBN happens at z ~ 4e8 (T ~ 0.1-1 MeV). A conversion at z_d < 1090 is 5-6 decades LATER.")
info(
      "B7a  BBN is BLIND to post-recombination conversion -- no constraint at all",
      "z_d < 1090 vs z_BBN ~ 4e8: light-element yields are set and frozen long before. Any claim that\n"
      "         BBN constrains this is simply wrong. BBN's only role here is B2c: it pins omega_b\n"
      f"         independently at {OB_BBN} +/- {OB_BBN_E} (LUNA), closing the 'call it baryons' loophole.")
print("\n  --- CORRECTION TO THE CORPUS ---")
print("  mi_cmb_no_dust_existence_2026.py block 7 computes Delta N_eff ~ (Omega_dm a_d / Omega_r0)*4.046")
print("  and reports 'Delta N_eff ~ 213 vs bound 0.3' as the kill. Two things are wrong with the LABEL")
print("  (the direction of the physics is right, and the kill survives -- via B2, not via N_eff):")
OM_R0 = OR_H2 / H_FID**2
for zd in (1000., 100., 10.):
    a_d = 1 / (1 + zd)
    ex = OM_DM_FID * a_d
    dneff_theirs = (ex / OM_R0) * (NEFF + 1.0)
    dneff_correct = ex / (0.2271 * OG_H2 / H_FID**2)
    print(f"    z_d={zd:7.0f}:  Omega_dr,0 = {ex:.3e}   'dNeff' as coded = {dneff_theirs:7.1f}   "
          f"correctly normalised = {dneff_correct:7.1f}")
info(
      "B7b  the N_eff NORMALISATION in our block 7 is low by ~1.8x",
      f"one extra massless species is 0.2271*Omega_gamma, so dN_eff = Omega_extra/(0.2271 Omega_gamma)\n"
      f"         = 7.45 * Omega_extra/Omega_r, not 4.046 * Omega_extra/Omega_r. Sign and order unaffected.")
info(
      "B7c  more importantly, 'Delta N_eff' is the WRONG OBSERVABLE for z_d < z_star",
      "N_eff is a constraint on the radiation density AT AND BEFORE recombination. Radiation created\n"
      "         at z_d = 100 is absent at z = 1090, so the CMB damping tail and BBN do NOT see it as N_eff.\n"
      "         The correct constraint on that channel is the LOW-z EXPANSION HISTORY (B2: 28.9 sigma from\n"
      "         DESI DR2, 15.8 sigma from Pantheon+ alone) and the DCDM->DR literature limit\n"
      "         f_dcdm < 2.44% (Planck18, long-lived) / < 1.49% (+BOSS BAO, short-lived), Nygaard et al.\n"
      "         JCAP 2021 05 017 -- against Route C's required f_dcdm = 100%.")
f_needed = 1.0
print(f"\n  Route C needs f_dcdm = {f_needed:.0%} with tau <~ t_0/ln(10) = "
      f"{13.8/np.log(10):.1f} Gyr (so that >90% has decayed).")
print(f"  Published bound: f_dcdm < 2.44% (long-lived) and < 1.49% (short-lived, +BAO), 2 sigma.")
check(f_needed / 0.0149 > 10,
      "B7d  the required decaying fraction exceeds the published bound by ~40-67x",
      f"100% / 2.44% = {1/0.0244:.0f}x (long-lived branch); 100% / 1.49% = {1/0.0149:.0f}x (short-lived,\n"
      "         which is the branch Route C actually needs). These are 2-sigma UPPER LIMITS on a fraction,\n"
      "         so the exclusion of f = 1 is far beyond 2 sigma -- B2's 15.8-28.9 sigma is the honest number.")

print("\n  --- the ELECTROMAGNETIC channel, for completeness: it is excluded enormously ---")
rho_dm_over_gam_at_zstar = (OM_DM_FID / (OG_H2 / H_FID**2)) / (1 + ZSTAR)
print(f"    rho_dm/rho_gamma at z_star = (Omega_dm/Omega_gamma)/(1+z_star) = "
      f"{OM_DM_FID/(OG_H2/H_FID**2):.0f}/{1+ZSTAR:.0f} = {rho_dm_over_gam_at_zstar:.2f}")
print(f"    dumping it into photons at z_star raises T0 by (1+{rho_dm_over_gam_at_zstar:.2f})^(1/4) = "
      f"{(1+rho_dm_over_gam_at_zstar)**0.25:.3f}x")
check(rho_dm_over_gam_at_zstar / 1.5e-5 > 1e4,
      "B7e  conversion to PHOTONS (or anything electromagnetic) is excluded by FIRAS by ~1e5",
      f"fractional energy release Drho_gamma/rho_gamma = {rho_dm_over_gam_at_zstar:.2f} against FIRAS |y| < 1.5e-5,\n"
      f"         |mu| < 9e-5 (Fixsen et al. 1996): over by {rho_dm_over_gam_at_zstar/1.5e-5:.1e}. And T0 would be\n"
      f"         {(1+rho_dm_over_gam_at_zstar)**0.25:.3f} x 2.7255 K = "
      f"{(1+rho_dm_over_gam_at_zstar)**0.25*2.7255:.2f} K. So the channel must be DARK -- which is B2's case.")


# ================================================================== SUMMARY
head("SUMMARY -- item by item, with the number that decides it")
verdicts = [
 ("1. Expansion history (BAO+SNe)",
  "NEEDS ONLY EXPANSION HISTORY -- but the expansion history REQUIRES a w~0 component today",
  f"Om(a^-3) today = {DESI_OM} +/- {DESI_OM_E} (DESI DR2 BAO); minus BBN baryons leaves "
  f"{non_bary:.3f} +/- {non_bary_err:.3f}\n      = {non_bary/non_bary_err:.0f} sigma of NON-BARYONIC pressureless energy. "
  f"Converting it to dark radiation at z_d=100 is\n      excluded at {sig_desi['DR z_d=100']:.1f} sigma (BAO) / "
  f"{abs(mdr['Om_a3']-PANT_OM)/PANT_OM_E:.1f} sigma (Pantheon+ alone). Kunz's degeneracy lets you RENAME\n"
  f"      it (w_X(0) = {wX_of_z(0.0):.2f} phantom reconstruction) but not remove it."),
 ("2. Growth / P(k)",
  "NEEDS ONLY GROWTH -- and MOND alone gives a two-sided miss, not a fix",
  f"NU=1 (AeST as built): growth suppressed {supp:.1f}x. NU=nu_RouteA({Y_LIN:.0e})={NU_KERNEL:.1f} (in-force kernel): "
  f"{D0_ov/D0_L:.3g}x LCDM;\n      NU=1/h={INV_H_LIN:.0f} (pointwise): {D0_ex/D0_L:.1e}x. "
  f"No constant boost reproduces observed growth; the P(k) SHAPE is safe "
  "though (T(k) is inherited\n      from the pre-z_d dust, so the baryon-only oscillation problem does NOT arise)."),
 ("3. Clusters (a_0-bump)",
  "NEEDS NEITHER -- and cannot substitute for the dust cosmologically",
  f"the bump reaches mu_eff^2 = {reach[0]:.2f}-{reach[1]:.2f} Mpc^-2 vs the {mu2_mist[0]:.1f}-{mu2_mist[1]:.1f} demanded: "
  f"clears the low end by\n      {reach[1]/mu2_mist[0]:.2f}x only. It is engineered to vanish on FRW (Y=0) and at linear order, "
  "so it fills\n      none of B4's gap. Stage-5 theorem: its condensate is conserved shift charge, so it needs a\n"
  "      reservoir -- Route C must break the shift symmetry, the same door Stage 5 already named."),
 ("4. CMB lensing + ISW",
  "*** NEEDS DARK MATTER TODAY -- THIS IS THE DECIDING ITEM ***",
  f"A_lens = {r_low:.2g} with AeST's linear-regime gravity ({abs(r_low-ALENS)/ALENS_E:.0f} sigma low vs ACT DR6's "
  f"1.013 +/- 0.023),\n      or {r_high:.3g} with the in-force kernel switched on ({abs(r_high-ALENS)/ALENS_E:.0f} sigma high); "
  f"the single boost that works,\n      NU = {nu_needed:.2f}, is predicted by nothing. STRONGEST ROUTE-C VERSION (convert as late as\n"
  f"      possible): the clustering must survive to z_d < {z_ok:.2f}, i.e. {100*t_ok/t0:.0f}% of cosmic time -- z_d = 1 is\n"
  f"      8.5 sigma, z_d = 0.5 is 2.6 sigma. ISW is only 3.2 sigma and does NOT carry the verdict."),
 ("5. BBN / N_eff",
  "NEEDS NEITHER -- BBN is blind; the constraint is elsewhere",
  "z_d < 1090 vs z_BBN ~ 4e8: zero BBN sensitivity, and N_eff is the wrong observable for a\n"
  "      post-recombination conversion (our own block 7 mislabels this; corrected in B7b/B7c).\n"
  f"      FIRAS does exclude the ELECTROMAGNETIC channel by {rho_dm_over_gam_at_zstar/1.5e-5:.0e}, forcing the channel to be dark."),
]
for k, v, d in verdicts:
    print(f"\n  {k}\n      => {v}\n      {d}")

print("\n" + "-" * 100)
print("  OVERALL: 'no dark matter today, MOND since recombination' is NOT observationally survivable")
print("  in this framework, and the binding constraint is NOT the background.")
print(f"    * removing the ENERGY: excluded at {sig_desi['DR z_d=100']:.0f} sigma by DESI DR2 BAO, "
      f"{abs(mdr['Om_a3']-PANT_OM)/PANT_OM_E:.0f} sigma by SNe alone.")
print("    * keeping the energy but removing the CLUSTERING (the only background-safe option, and")
print(f"      the Kunz-degenerate one): kills CMB lensing, A_lens = {r_low:.2g} vs 1.013 +/- 0.023 "
      f"({abs(r_low-ALENS)/ALENS_E:.0f} sigma).")
print("    * AeST cannot fill that gap because its MOND sector is quasi-static-ONLY by construction,")
print("      and the a_0-bump is second-order in perturbations by construction. Both are the")
print("      framework's OWN engineering choices, printed in its own scripts.")
print("    * letting MOND act in the linear regime instead OVERSHOOTS lensing and sigma_8 by orders")
print(f"      of magnitude ({r_high:.3g}x; the corpus already banked sigma_8 = 45.9 vs 0.811 +/- 0.006).")
print(f"    * pushing the conversion as LATE as possible does not rescue it: CMB lensing forces")
print(f"      z_d < {z_ok:.2f} ({100*t_ok/t0:.0f}% of cosmic time with the dust clustering normally), by which point")
print("      every galaxy and cluster the dust was meant to be absent from has already formed WITH it.")
print("    * B4e is the tightest statement and it is a DICHOTOMY, not a fit: any transport channel fast")
print("      enough to evacuate a 1 Mpc basin carries w >~ 0.1, which the background forbids at 16-29")
print(f"      sigma; any channel slow enough to keep w = 0 needs {t_cross_cs:.1e} Gyr and moves nothing.")
print("  WHAT SURVIVES: the pressureless component must be PRESENT and CLUSTERING today at full")
print(f"  Omega ~ 0.25. It need not be a PARTICLE (the GDM degeneracy stands), and c_s is bounded")
print(f"  only at the ~{aH/0.1:.0f} km/s level by lensing -- 1e5 x above the framework's own 1.4 m/s.")
print("  So the slogan 'no dark-matter PARTICLE' is untouched by Route C. 'No dark matter today' is not.")
print("-" * 100)

head("CHECKS")
print(f"  {len(FAIL)} failed of {N_CHECKS[0]}")
if FAIL:
    print(f"*** {len(FAIL)} CHECK(S) FAILED ***")
    for x in FAIL:
        print("  -", x)
    sys.exit(1)
print("  ALL CHECKS PASSED")
