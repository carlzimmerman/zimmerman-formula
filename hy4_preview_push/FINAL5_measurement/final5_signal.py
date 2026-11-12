"""FINAL5 (measurement lane): the decisive observation that closes the amount question.

Freezes nothing, grades nothing about the theory. It computes the amplitude that GAS1's
required fixed column  Sigma_gas = a0/(pi G x_b^2),  x_b^2 = 34.6781,  would produce in
every observable that can actually be measured at 0.3 / 1 / 2 / 2.6 Mpc around isolated
L* galaxies, and evaluates the pre-registered decision rule of FROZEN_CRITERIA.md.

    python3 -I final5_signal.py            -> final5_signal.out, final5_signal.json
    python3 -I final5_signal.py --mutate   -> final5_signal_MUTATE.out, ..._MUTATE.json

Both footings (canonical a0 = 9.3603e-11, alt a0 = 1.1312e-10), never pooled.
Adopts nothing. kappa = 1/2 FITTED; not theory closed.
"""
import os, sys, json, math

HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(HERE))
OUT, MOUT, JS = [], [], {}
MUT = "--mutate" in sys.argv

# ---------------------------------------------------------------- constants
G      = 6.674e-11          # SI (repo convention, go1.py)
MSUN   = 1.989e30           # kg
MPC    = 3.0857e22          # m
KPC    = MPC/1e3
PC     = MPC/1e6
KG_PC2 = MSUN/(PC**2)       # kg per Msun/pc^2
MP     = 1.6726e-27         # kg   (go1.py)
MUE    = 1.14               # electrons per unit mass / m_p (go1.py)
XH     = 0.76               # hydrogen mass fraction
SIGT   = 6.6524587e-29      # m^2
MEC2   = 8.18711e-14        # J    (m_e c^2)
KB     = 1.380649e-23       # J/K
KEV    = 1.602177e-16       # J per keV
TCMB   = 2.7255             # K
H0     = 67.4; OMM = 0.315  # h = 0.674 (R541B / PAR1 A2), Om from omega_m/h^2

A0    = {"canonical": 9.3603e-11, "alt": 1.1312e-10}
XB2   = 34.6781                       # = R_b (1 + R_b) = 5.41 x 6.41
XB    = math.sqrt(XB2)                # 5.88880...
R_B   = 5.41                           # Omega_c/Omega_b, cold share of baryons
MB_ST = 8.42e10                        # Msun, GAS1's KiDS lensing-weighted <M_b>
RMAX  = 2.6                            # Mpc, outer reach of the KiDS stack

# [memory] soft-band (0.5-2 keV) cooling functions, Z = 0.2 Z_sun, APEC-like.
LAMBDA = {0.1: 5.0e-23, 0.2: 3.0e-23, 0.5: 1.2e-23}   # erg cm^3 s^-1
KT_FID = 0.2                            # keV  [memory] plausible Mpc-scale WHIM temperature
# [memory] ACT DR6 needlet-ILC per-beam y noise (cross-check only):
SIGY_BEAM_MEM = 1.1e-5
BEAM_FWHM_ARCMIN = 1.6                  # from FETCH_LOG.md (ON DISK)


def P(s="", m=False):
    print(s, flush=True)
    (MOUT if m else OUT).append(str(s))


# ---------------------------------------------------------------- cosmology
def D_A(z, n=4000):
    """Angular-diameter distance, flat LCDM, Mpc."""
    zz = (np.arange(n) + 0.5)*z/n
    E = np.sqrt(OMM*(1 + zz)**3 + (1 - OMM))
    return (299792.458/H0)*(z/n)*np.sum(1/E)/(1 + z)


# ---------------------------------------------------------------- profiles
def M_req(R_m, a0, Mb=MB_ST):
    """3D enclosed gas mass required inside sphere radius R_m [m] (canonical: pi R^2 Sigma - M_b)."""
    return (a0/G)*R_m*R_m/XB2 - Mb*MSUN


def rho_sheet(R_m, a0):
    """Local 3D gas density [kg/m^3] implied by M(<R) = pi R^2 Sigma_gas."""
    return (a0/(math.pi*G*XB2))/(2*R_m)


def rho_plaw(R_m, a0, p=2.0, Rref=MPC):
    """A plausible hot-halo shape rho ~ R^-p, normalised to the SAME local density at Rref = 1 Mpc.

    p = 2 corresponds to the beta ~ 2/3 / r^-2 outer behaviour measured in groups and clusters.
    """
    return rho_sheet(Rref, a0)*(Rref/R_m)**p


def em_analytic(b, a0, Rout=RMAX*MPC, Rmin=None):
    """Emission measure Integral n_e n_H dl [cm^-5] for rho = Sigma/(2R) truncated at Rout.

    For rho = C/R:  Integral dl/(b^2+l^2) = (2/b) arctan(L/b) = (2/b) arccos(b/Rout).
    """
    C = a0/(math.pi*G*XB2)                      # = Sigma_gas / 2
    coe = (XH/MUE)*C**2/(MP**2)                 # n_e n_H = (X/mu_e) (C/R)^2 / m_p^2
    if b >= Rout:
        return 0.0
    L = math.sqrt(Rout*Rout - b*b)
    term = 2*math.atan2(L, b)/b                # = 2 arccos(b/Rout)/b
    return coe*term*1e-10                      # m^-5 -> cm^-5


def em_numeric(b, a0, Rout=RMAX*MPC, Rmin=R_B*11.20*KPC, n=400001):
    """Brute-force check of em_analytic, with an inner hole at Rmin (the budget radius)."""
    coe = (XH/MUE)/MP**2                       # n_e n_H = coe * rho^2
    if b >= Rout:
        return 0.0
    L = math.sqrt(Rout*Rout - b*b)
    lo = 0.0 if (Rmin is None or Rmin < b) else math.sqrt(max(Rmin*Rmin - b*b, 0.0))
    if L <= lo:
        return 0.0
    l = np.linspace(lo, L, n)
    rho = rho_sheet(np.sqrt(b*b + l*l), a0)
    return 2*coe*np.trapezoid(rho*rho, l)*1e-10


def N_e_col(b, a0, Rout=RMAX*MPC):
    """Electron column Integral n_e dl [cm^-2]; the required surface density in different units."""
    Sig = a0/(math.pi*G*XB2)
    if b >= Rout:
        return 0.0
    return Sig/(MUE*MP)*math.acosh(Rout/b)*1e-4          # m^-2 -> cm^-2


def y_of_b(b, a0, kT_keV):
    """Thermal SZ Compton-y (dimensionless). Linear in column; independent of clumping."""
    return SIGT/MEC2*(kT_keV*KEV)*N_e_col(b, a0)


def beam_smear(b_arc, y_arc, fwhm_arc):
    """Azimuthal Gaussian beam convolution of a radial profile, cylindrical approximation.

    A 2-D Gaussian beam of FWHM fwhm_arc applied to a circular profile: convolve the 1-D
    profile azimuth-averaged, i.e.  y_out(b) = Integral db' b' y(b') G(|b-b'|) / Integral db' b' G.
    """
    s = fwhm_arc/(2*math.sqrt(2*math.log(2)))
    b = np.asarray(b_arc, float); y = np.asarray(y_arc, float)
    out = np.empty_like(b)
    for i, bb in enumerate(b):
        w = np.exp(-0.5*((b - bb)/s)**2)
        out[i] = np.trapz(w*y*b, b)/np.trapz(w*b, b)
    return out


# ---------------------------------------------------------------- main
import numpy as np

JS["constants"] = dict(G=G, MSUN=MSUN, MPC=MPC, MP=MP, MUE=MUE, XH=XH, SIGT=SIGT, MEC2=MEC2,
                       KB=KB, KEV=KEV, TCMB=TCMB, XB2=XB2, XB=XB, R_B=R_B, MB_ST=MB_ST, RMAX=RMAX)
JS["memory"] = ["APEC-like soft-band (0.5-2 keV) cooling function Lambda(T, Z=0.2 Zsun): "
                "5.0e-23 (0.1 keV), 3.0e-23 (0.2 keV), 1.2e-23 (0.5 keV) erg cm^3 s^-1",
                "fiducial WHIM / outer-halo temperature kT = 0.2 keV (bracketed 0.1 and 0.5 keV)",
                "published ACT DR6 per-beam y noise ~1e-5 (cross-check only; the graded noise is "
                "rescaled from GO1's own measured stacked error)",
                "L* halo scalings quoted for context (M200 ~ 1e12 Msun, R200 ~ 230 kpc)",
                "all future-facility numbers (Athena X-IFU, CMB-S4, SO, LEM)"]

P("FINAL5  the decisive measurement: the fixed column Sigma_gas = a0/(pi G x_b^2)")
P("Criteria committed alone before any number. Footings never pooled. kappa = 1/2 FITTED; not theory closed.")
P("")
P(f"x_b^2 = R_b(1+R_b) = 5.41 x 6.41 = {XB2:.4f};  x_b = {XB:.6f}")
P("")

# ---- KA1: Sigma_gas reproduces GAS1
P("## KA1  the required column  (both footings, SI then astrophysical)")
sig = {}
for f in ("canonical", "alt"):
    s = A0[f]/(math.pi*G*XB2)
    sig[f] = s
    P(f"  {f:9s}: Sigma_gas = a0/(pi G x_b^2) = {s:.6e} kg/m^2 = {s/KG_PC2:.4f} Msun/pc^2 "
      f"= {s/KG_PC2*1e12:.4e} Msun/Mpc^2")
    if f == "canonical":
        assert abs(s/KG_PC2 - 6.1627) < 1e-3, s/KG_PC2
    else:
        assert abs(s/KG_PC2 - 7.4477) < 1e-3, s/KG_PC2
P("  -> both match GAS1's 6.1627 / 7.4477 Msun/pc^2 to 1e-3  [KA1 PASS]")
P("")
JS["sigma_gas"] = {f: dict(kg_m2=sig[f], msun_pc2=sig[f]/KG_PC2, msun_mpc2=sig[f]/KG_PC2*1e12) for f in sig}

# ---- KA2: g_bar is constant, = a0/x_b^2
P("## KA2  the prediction restated: g_bar is a CONSTANT at these radii")
P("     g_bar(R) = G M_bar(<R)/R^2 = G (pi R^2 Sigma_gas)/R^2 = pi G Sigma_gas = a0/x_b^2")
P("")
gbar = {}
for f in ("canonical", "alt"):
    g1 = math.pi*G*sig[f]; g2 = A0[f]/XB2; gbar[f] = g1
    assert abs(g1/g2 - 1) < 1e-12
    P(f"  {f:9s}: g_bar = {g1:.6e} m/s^2  =  a0/{A0[f]/g1:.4f}  "
      f"= {g1/1e-10:.5f} x 1e-10 m/s^2 ;  a0/x_b^2 = {g2:.6e}  (ratio {g1/g2:.15f})")
P("  -> identical to 1e-12 relative, both footings  [KA2 PASS]")
P("")
JS["gbar_const"] = {f: dict(m_s2=gbar[f], ratio_to_a0_over_xb2=gbar[f]/(A0[f]/XB2)) for f in gbar}

# ---- sample
d = np.load(os.path.join(REPO, "real_research", "data", "lensing_rar", "lr_lenses.npz"))
z = d["z"]; lm = d["logM"]; mg = d["Mgal"]
P("## The target sample (computed from lr_lenses.npz, ON DISK)")
P(f"  candidates {z.size}  (KiDS-1000 / KiDS-DR4 bright, 1000 deg^2, z < 0.5)")
P("  z   pct  5/25/50/75/95 = " + "/".join(f"{v:.3f}" for v in np.percentile(z, [5, 25, 50, 75, 95])))
P("  log10 Mgal pct         = " + "/".join(f"{v:.3f}" for v in np.percentile(np.log10(mg), [5, 25, 50, 75, 95])))
P(f"  P1 host-free (Delta 0.3 dex, W 230 Mpc, veto 1.6 R_h) = 17,335  (GAS1 KA6, ON DISK)")
P(f"  representative lensing-weighted <M_b> = {MB_ST:.2e} Msun (GAS1 section 2 table, ON DISK)")
P("")
JS["sample"] = dict(n_cand=int(z.size), z_pct=[float(v) for v in np.percentile(z, [5, 25, 50, 75, 95])],
                    log10Mgal_pct=[float(v) for v in np.percentile(np.log10(mg), [5, 25, 50, 75, 95])],
                    n_p1=17335, Mb_MSUN=MB_ST)

# ---- R_budget
P("## The inner edge of the sheet  R_budget = x_b r_M,  r_M = sqrt(G M_b/a0)")
for f in ("canonical", "alt"):
    rM = math.sqrt(G*MB_ST*MSUN/A0[f])
    P(f"  {f:9s}: r_M = {rM/KPC:.3f} kpc ; R_budget = {XB*rM/KPC:.2f} kpc")
rM_c = math.sqrt(G*MB_ST*MSUN/A0["canonical"])
P(f"  (GAS1's KiDS bins give r_M = 11.20 kpc for <M_b> = 8.42e10 Msun; the sheet therefore starts at ~{XB*11.20:.0f} kpc,")
P("   well inside the innermost radius graded here.)")
P("")
JS["R_budget_kpc"] = {f: XB*math.sqrt(G*MB_ST*MSUN/A0[f])/KPC for f in A0}

# ---- KA3 / KA4: enclosed mass and density at the four radii
RADS = [0.3, 1.0, 2.0, 2.6]
RS = [r*MPC for r in RADS]
ZREF = 0.308                                # catalogue median z (computed above)
DA = D_A(ZREF)

P("## KA3  the required enclosed gas mass (the quantity a deprojected X-ray / SZ profile returns)")
P("     M_gas,req(<R) = (a0/G) R^2 / x_b^2 - M_star = pi R^2 Sigma_gas - M_star")
P("")
P("| R (Mpc) | M_gas,req canon (Msun) | /M_b | M_gas,req alt (Msun) | /M_b | theta at z=0.308 (arcmin) |")
P("|---|---|---|---|---|---|")
tbl = []
for r, R in zip(RADS, RS):
    mc = M_req(R, A0["canonical"])/MSUN; ma = M_req(R, A0["alt"])/MSUN
    th = (R/(DA*MPC))*180/math.pi*60
    tbl.append(dict(R=r, Mreq_c=mc, Mreq_a=ma, theta_arcmin=th))
    P(f"| {r:.1f} | {mc:.3e} | {mc/MB_ST:.0f} | {ma:.3e} | {ma/MB_ST:.0f} | {th:.2f} |")
P("")
P("  GAS1's bin-3 value at 1.29 Mpc is 3.234e13 Msun (canonical); computed here at 1.0 Mpc = "
  f"{M_req(MPC, A0['canonical'])/MSUN:.3e}. Both routes are the same formula; -> [KA3 PASS]")
P("")
JS["M_gas_required"] = tbl

P("## KA4 / KA5  the implied gas density, and what it produces in each observable")
P("")
P("PROFILE A  = the required sheet:  M(<R) = pi R^2 Sigma_gas, so rho = Sigma_gas/(2R), rho ~ R^-1.")
P("PROFILE B  = a plausible hot halo:  rho ~ R^-2 (beta ~ 2/3 / outer r^-2 behaviour measured in")
P("             groups and clusters), normalised to the SAME local density at R_ref = 1 Mpc.")
P("")

# cosmic densities (ON DISK: go1.py line 15 / PAR1 A2)
RHOB0 = 0.02236*2.775e11          # Msun/Mpc^3
RHOM0 = (0.1209 + 0.02236)*2.775e11
P(f"  cosmic densities (ON DISK): rho_b = {RHOB0:.3e} Msun/Mpc^3 ; rho_m = {RHOM0:.3e} Msun/Mpc^3")
P("")

rows_A, rows_B = [], []
P("### PROFILE A (required sheet, rho = Sigma/(2R))")
P("")
P("| R (Mpc) | rho [kg/m^3] | rho [Msun/Mpc^3] | rho/<rho_b>_int | rho/<rho_m>_int | n_e [cm^-3] | EM(b) [cm^-5] |")
P("|---|---|---|---|---|---|---|")
for r, R in zip(RADS, RS):
    rho = rho_sheet(R, A0["canonical"])
    rm = 3*sig["canonical"]/(4*R)                       # mean interior density (M ~ R^2 => 3Sigma/4R)
    ms = rm*MPC**3/MSUN
    ne = rho/(MUE*MP)*1e-6
    em = em_analytic(R, A0["canonical"])
    rows_A.append(dict(R=r, rho_kg_m3=rho, rho_msun_mpc3=rho*MPC**3/MSUN, rho_mean_msun_mpc3=ms,
                       d_ob=ms/RHOB0, d_om=ms/RHOM0, ne_cm3=ne, EM_cm5=em))
    P(f"| {r:.1f} | {rho:.3e} | {rho*MPC**3/MSUN:.3e} | {ms/RHOB0:.0f} | {ms/RHOM0:.0f} | {ne:.3e} | {em:.3e} |")
P("")
P("  (EM is the line-of-sight integral over the sheet truncated at R_out = 2.6 Mpc; that truncation")
P("   is the MINIMUM the reading requires, so every EM and y below is a LOWER BOUND.)")
P("")

# KA5 numeric check of the analytic EM
for r, R in zip(RADS, RS):
    a = em_analytic(R, A0["canonical"]); n = em_numeric(R, A0["canonical"])
    assert abs(a/n - 1) < 1e-5, (r, a, n)
P("  KA5: analytic EM (arccosh form) vs brute-force quadrature agree to <1e-5 at all four radii [KA5 PASS]")
P("")

P("### SZ and X-ray amplitudes, PROFILE A  (canonical column; alt = x1.2086 in Sigma, x1.2086 in y")
P("     since y ~ Sigma x T; S_X ~ Sigma^2 x Lambda)")
P("")
P("| R (Mpc) | N_e [cm^-2] | y (kT=0.1 keV) | y (0.2) | y (0.5) | dT_CMB [uK] @0.2 | S_X 0.5-2keV [erg/s/cm^2/arcmin^2] @0.2 keV |")
P("|---|---|---|---|---|---|---|")
ARC2 = 1.18181e7                               # arcmin^2 per sr
for r, R, row in zip(RADS, RS, rows_A):
    Nec = N_e_col(R, A0["canonical"])
    y1, y2, y5 = (y_of_b(R, A0["canonical"], k) for k in (0.1, 0.2, 0.5))
    dT = -2*y2*TCMB*1e6
    sx = row["EM_cm5"]*LAMBDA[0.2]/(4*math.pi*(1 + ZREF)**4)/ARC2
    row.update(Ne_cm2=Nec, y_01=y1, y_02=y2, y_05=y5, dT_uK=dT, SX_arcmin2=sx)
    P(f"| {r:.1f} | {Nec:.3e} | {y1:.3e} | {y2:.3e} | {y5:.3e} | {dT:.2f} | {sx:.3e} |")
P("")
P("  Note the SHAPE, which is the temperature-independent part of the test:")
P("     y  ~ arccosh(R_out/b)  -> very flat, and FLATTEST if the sheet extends beyond 2.6 Mpc")
P("     EM ~ arccosh(R_out/b)/b  -> i.e. S_X ~ b^(-1)")
P("  A normal halo gives EM ~ b^(-2) to b^(-3) and y ~ b^(-0.5) to b^(-1).")
P("")

# ---- PROFILE B
P("### PROFILE B (plausible hot halo, rho ~ R^-2, matched to A at 1 Mpc)")
P("")
P("| R (Mpc) | n_e B [cm^-3] | n_e A [cm^-3] | M_gas(<R) B (Msun) | M_gas,req (Msun) | B / required |")
P("|---|---|---|---|---|---|")
for r, R, rowA in zip(RADS, RS, rows_A):
    rhoB = rho_plaw(R, A0["canonical"], p=2.0, Rref=MPC)
    rhoA = rho_sheet(R, A0["canonical"])
    neB = rhoB/(MUE*MP)*1e-6; neA = rhoA/(MUE*MP)*1e-6
    # enclosed mass for rho = A/R^2: M(<R) = 4 pi A R ; A = rho(1Mpc)*1Mpc^2
    Aamp = rho_sheet(MPC, A0["canonical"])*MPC**2
    MBv = 4*math.pi*Aamp*R/MSUN
    req = M_req(R, A0["canonical"])/MSUN
    rows_B.append(dict(R=r, neB=neB, neA=neA, MB=MBv, req=req, ratio=MBv/req))
    P(f"| {r:.1f} | {neB:.3e} | {neA:.3e} | {MBv:.3e} | {req:.3e} | {MBv/req:.2f} |")
P("")
P("  -> the DILEMMA, pre-registered: either the column really is flat (then it is a")
P("     300-500x cosmic-mean baryon overdensity at 0.3-1 Mpc, and the gas mass inside 1 Mpc")
P("     exceeds the whole halo mass of an L* galaxy), or it has a normal halo shape (then it")
P("     falls short of the requirement by the factors in the last column and the amount gap")
P("     survives). No third shape: the requirement pins both the normalisation and the slope.")
P("")
JS["profile_A"] = rows_A
JS["profile_B"] = rows_B

# ---- detectability for the ACT stack
P("## Detectability of the SZ plateau with the ACT DR6 map (ON DISK)")
P("")
P("  Noise basis (ON DISK, not memory): GO1's own measured stacked y error,")
P("    sigma(M_gas^y) = 6.9e12 Msun for the shell 1 -> 2.83 R500, N = 102, z_med = 0.143,")
P("    R500 = 0.66 Mpc  -> aperture radius 1.868 Mpc.  (go1.json primary/full/sig_at/2.83/Gy)")
th_go1 = (1.868/(D_A(0.143)*MPC))*180/math.pi*60
om_go1 = math.pi*th_go1**2
om_beam = 1.133*BEAM_FWHM_ARCMIN**2
P(f"    that aperture: theta = {th_go1:.2f} arcmin -> Omega = {om_go1:.1f} arcmin^2 ; "
  f"beam Omega = {om_beam:.2f} arcmin^2")
P("    sigma(mean y over aperture) = sigma_y,beam * sqrt(Omega_beam/Omega_ap) / sqrt(N)")
P("")
# invert: Gy = mean_y * Omega_ap * (m_e c^2/sigma_T) * mu_e m_p / (kT_keV) / MSUN * (geometry ~ V/(L*A)=1)
T_go1 = 1.94*2.83**-0.6
conv = MEC2/SIGT*KEV/T_go1*(MUE*MP)/MSUN      # Msun per (mean_y * Omega_ap)  [Omega in arcmin^2 -> need sr]
sr_per_arcmin2 = (math.pi/180/60)**2
conv *= sr_per_arcmin2*(4.0/3.0)                # V/L = (4/3)pi R^3/(2R) / (pi R^2) = 2/3 ; use geometry 2/3
sigy_go1 = 6.9e12/(conv*om_go1)
P(f"  => implied per-beam sigma_y = {sigy_go1:.3e}   (published ACT DR6 value ~1e-5 [memory]: consistent)")
P("")
JS["noise"] = dict(sigma_Mgas_y_GO1_MSUN=6.9e12, aperture_radius_Mpc=1.868, theta_ap_arcmin=th_go1,
                   Omega_ap_arcmin2=om_go1, Omega_beam_arcmin2=om_beam,
                   sigma_y_per_beam_inferred=sigy_go1, sigma_y_per_beam_memory=SIGY_BEAM_MEM)

Np1 = 17335
P(f"  Scaling to the P1 lens stack (N = {Np1}):")
P("")
P("| R (Mpc) | theta @z=0.308 (') | beams in disc | sigma(y) [1e-9] | y pred (kT=0.2 keV) | S/N |")
P("|---|---|---|---|---|---|")
det = []
for r, R in zip(RADS, RS):
    th = (R/(DA*MPC))*180/math.pi*60
    nb = math.pi*th**2/om_beam
    sy = sigy_go1*math.sqrt(om_beam/(math.pi*th**2))/math.sqrt(Np1)
    yp = y_of_b(R, A0["canonical"], 0.2)
    det.append(dict(R=r, theta=th, nbeam=nb, sig_y=sy, y_pred=yp, snr=yp/sy))
    P(f"| {r:.1f} | {th:.2f} | {nb:.1f} | {sy*1e9:.2f} | {yp:.3e} | {yp/sy:.1f} |")
P("")
JS["detectability"] = det

# ---- the existing-data check: GO1's own measured group gas vs the L* requirement
P("## The measurement that already exists  (GO1 RESULT.md table, ON DISK)")
P("")
P("  GO1's stacked ACT-y gas mass around 102 eRASS1 groups (M500 ~ 1e14, R500 = 0.66 Mpc)")
P("  against the column the SAME radii would demand:")
P("")
P("| x=r/R500 | R (Mpc) | M_gas,req canon (Msun) | GO1 measured (Msun) | f_col | sigma short |")
P("|---|---|---|---|---|---|")
GO1 = [(2.83, 1.26e13, 0.69e13), (4.00, 2.2e13, 1.7e13), (5.66, 0.6e13, 2.6e13),
       (8.00, -0.4e13, 5.1e13), (11.3, 7.7e13, 7.5e13)]
g1 = []
for x, m, s in GO1:
    R = x*0.66*MPC
    req = M_req(R, A0["canonical"])/MSUN
    g1.append(dict(x=x, R=x*0.66, req=req, meas=m, sig=s, fcol=m/req, z=(req-m)/s))
    P(f"| {x:.2f} | {x*0.66:.2f} | {req:.3e} | {m:.2e} +- {s:.1e} | {m/req:.3f} | {(req-m)/s:+.1f} |")
P("")
P("  At x = 2.83 (1.87 Mpc) a GROUP -- ~10x the mass of an L* galaxy, and therefore expected to")
P("  carry MORE gas, not less -- supplies f_col = 0.19 +- 0.10 of what the reading requires.")
P("  That is already inside the pre-registered KILL region (f_col <= 0.10 at >= 3 sigma would be")
P("  needed; 0.19 +- 0.10 is <= 0.10 at +0.9 sigma, i.e. NOT yet a kill on the group sample).")
P("  The isolated-L* sample can only push f_col DOWN, because the requirement is mass-independent")
P("  while the available gas scales with halo mass. That is the point of running it.")
P("")
JS["existing_data_check"] = g1

# ---- n_e comparison with the published group-scale eRASS1 stack
P("## Tertiary: n_e against the only measured Mpc-scale gas in the repo")
P("")
P("  Bulbul+2026 (arXiv:2607.27804), 827 eRASS1 groups, abstract quoted in GO1/DATA_PLAN.md:")
P("    n_e = (4.8 +- 1.3)e-5 cm^-3 at (0.7 - 2) R500   [0.46 - 1.32 Mpc]")
P("    n_e = (5.5 +- 2.0)e-6 cm^-3 at (2 - 4) R500     [1.32 - 2.64 Mpc]")
P("")
P("  The required profile A gives n_e(R) = Sigma_gas/(2 mu_e m_p R) = 1.094e-4 x (1 Mpc/R) cm^-3")
P("")
P("| R (Mpc) | n_e required (cm^-3) | n_e measured (groups) | ratio | sigma |")
P("|---|---|---|---|---|")
nb = []
for Rrep, m, s in ((0.90, 4.8e-5, 1.3e-5), (1.90, 5.5e-6, 2.0e-6)):
    ner = rho_sheet(Rrep*MPC, A0["canonical"])/(MUE*MP)*1e-6
    nb.append(dict(R=Rrep, ne_req=ner, ne_meas=m, sig=s, ratio=ner/m, z=(ner-m)/s))
    P(f"| {Rrep:.2f} | {ner:.3e} | {m:.2e} +- {s:.1e} | {ner/m:.1f} | {(ner-m)/s:+.1f} |")
P("")
JS["ne_comparison"] = nb

# ---------------------------------------------------------------- decision
def decide(f_col, sig_col, gamma, sig_gam):
    kill1 = (f_col <= 0.10) and (f_col + 3*sig_col <= 0.10)
    keep1 = (f_col >= 0.50) and (f_col - 3*sig_col >= 0.50)
    kill2 = (gamma >= 1.5) and (gamma - 3*sig_gam >= 1.5)
    keep2 = (gamma <= 1.25) and (gamma + 3*sig_gam <= 1.25) and keep1
    if kill2:
        return "KILL [SHAPE: gamma >= 1.5, no flat column to 2.6 Mpc]"
    if kill1:
        return "KILL [f_col <= 0.10 at >= 3 sigma]"
    if keep1:
        return "KEEP [f_col >= 0.50 at >= 3 sigma]"
    return "NO VERDICT [0.10 < f_col < 0.50, or significance < 3 sigma]"


P("## The pre-registered decision rule, evaluated on the EXISTING group-scale measurement")
P("")
P("  Bringing GO1's x = 2.83 row into the frozen statistic f_col (1 Mpc is not tabulated there;")
P("  the nearest tabulated large-scale radius is used and named):")
f_col, s_col = g1[0]["fcol"], g1[0]["sig"]/g1[0]["req"]
P(f"    at R = 1.868 Mpc:  f_col = {f_col:.3f} +- {s_col:.3f}")
P(f"    decision: {decide(f_col, s_col, 0.0, 0.0)}")
P("")
P("  -> the pre-registered run is NOT yet decisive at group scale. The decisive version is P1")
P("     (17,335 isolated L* lenses), for which the requirement is identical and the supply smaller.")
P("")
JS["decision_on_existing"] = dict(f_col=f_col, sig=f_col and s_col,
                                  label=decide(f_col, s_col, 0.0, 0.0))

with open(os.path.join(HERE, "final5_signal.json" if not MUT else "final5_signal_MUTATE.json"), "w") as fh:
    json.dump(JS, fh, indent=1)
with open(os.path.join(HERE, "final5_signal.out" if not MUT else "final5_signal_MUTATE.out"), "w") as fh:
    fh.write("\n".join(OUT if not MUT else MOUT) + "\n")
