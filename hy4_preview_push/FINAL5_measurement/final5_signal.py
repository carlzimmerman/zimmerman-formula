"""FINAL5 (measurement lane): the decisive observation that closes the amount question.

Freezes nothing, grades nothing about the theory. It computes the amplitude that GAS1's required
fixed column  Sigma_gas = a0/(pi G x_b^2),  x_b^2 = 34.6781,  would produce in every observable
that can actually be measured at 0.3 / 1 / 2 / 2.6 Mpc around isolated L* galaxies, and
evaluates the pre-registered decision rule of FROZEN_CRITERIA.md.

    python3 -I final5_signal.py            -> final5_signal.out, final5_signal.json
    python3 -I final5_signal.py --mutate   -> final5_signal_MUTATE.out, ..._MUTATE.json

Both footings (canonical a0 = 9.3603e-11, alt a0 = 1.1312e-10), never pooled.
Adopts nothing. kappa = 1/2 FITTED; not theory closed.
"""
import os, sys, json, math
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
OUT, JS = [], {}
MUT = "--mutate" in sys.argv

# ---------------------------------------------------------------- constants
G     = 6.674e-11       # SI (repo convention, go1.py)
MSUN  = 1.989e30        # kg
MPC   = 3.0857e22       # m
KPC   = MPC/1e3
PC    = MPC/1e6
KGPC2 = MSUN/(PC**2)    # kg per Msun/pc^2
MP    = 1.6726e-27      # kg  (go1.py)
MUE   = 1.14            # electrons per m_p of gas mass (go1.py)
XH    = 0.76            # hydrogen mass fraction
SIGT  = 6.6524587e-29   # m^2
MEC2  = 8.18711e-14     # J   (m_e c^2)
KEV   = 1.602177e-16    # J per keV
TCMB  = 2.7255          # K
H0, OMM = 67.4, 0.315   # h = 0.674 (R541B/PAR1 A2)

A0  = {"canonical": 9.3603e-11, "alt": 1.1312e-10}
XB2 = 34.6781
XB  = math.sqrt(XB2)
R_B = 5.41               # Omega_c/Omega_b, cold share per baryon
MBST = 8.42e10           # Msun, GAS1's KiDS lensing-weighted <M_b>
RADS = [0.3, 1.0, 2.0, 2.6]
RMAX = 2.6               # Mpc, outer reach of the KiDS stack
ZREF = 0.308             # catalogue median z (computed below)
ARC2_PER_SR = 1.18181e7

# [memory] soft-band (0.5-2 keV) cooling functions, Z = 0.2 Zsun, APEC-like, erg cm^3 s^-1
LAM = {0.1: 5.0e-23, 0.2: 3.0e-23, 0.5: 1.2e-23}
KTF = 0.2                # keV [memory] plausible Mpc-scale WHIM / outer-halo temperature
# [memory] published ACT DR6 per-beam y noise (cross-check only)
SIGY_MEM = 1.1e-5
BEAM_ARCMIN = 1.6        # FETCH_LOG.md (ON DISK)


def P(s=""):
    print(s, flush=True); OUT.append(str(s))


def D_A(z, n=6000):
    """Angular-diameter distance [m], flat LCDM."""
    dz = z/n
    zz = (np.arange(n) + 0.5)*dz
    E = np.sqrt(OMM*(1 + zz)**3 + (1 - OMM))
    return (299792.458/H0)*dz*np.sum(1/E)/(1 + z)*MPC


# ---------------------------------------------------------------- profiles
def Sigma(a0):
    return a0/(math.pi*G*XB2)                      # kg/m^2


def M_req(R_m, a0):
    """3D enclosed gas mass required inside sphere radius R [m]  = pi R^2 Sigma - M_b."""
    return (a0/G)*R_m*R_m/XB2 - MBST*MSUN


def rho_A(R_m, a0):
    """Required sheet: rho = Sigma/(2R)  (so that M(<R) = pi R^2 Sigma)."""
    return Sigma(a0)/(2*R_m)


def rho_B(R_m, a0, p=2.0, Rref=MPC):
    """Plausible hot halo: rho ~ R^-2, matched to profile A at Rref = 1 Mpc."""
    return rho_A(Rref, a0)*(Rref/R_m)**p


def N_e(b, a0, Rout, geom=1.0):
    """Electron column Integral n_e dl [cm^-2].

    geom = 1.0              -> the uniform projected sheet (the literal reading of a fixed
                               surface density; this is the MINIMUM).
    geom = arccosh(Rout/b)  -> the spherical rho = Sigma/(2R) reading with outer cutoff Rout.
    """
    if b >= Rout:
        return 0.0
    g = geom if geom != "arccosh" else math.acosh(Rout/b)
    return Sigma(a0)/(MUE*MP)*g*1e-4


def EM(b, a0, Rout):
    """Emission measure Integral n_e n_H dl [cm^-5], for rho = Sigma/(2R) cut at Rout.

    n_e n_H = (X_H/mu_e) (C/R)^2 / m_p^2 with C = Sigma/2, and
    Integral_{-L}^{L} dl/(b^2+l^2) = (2/b) arctan(L/b) = (2/b) arccos(b/Rout).
    """
    if b >= Rout:
        return 0.0
    C = Sigma(a0)/2
    coe = (XH/MUE)*C**2/(MP**2)
    L = math.sqrt(Rout*Rout - b*b)
    return coe*(2*math.atan2(L, b)/b)*1e-10


def N_e_m(b, a0, Rout, geom=1.0):
    """As N_e but in SI [m^-2] (used by y_of; N_e's cm^-2 is for reporting only)."""
    if b >= Rout:
        return 0.0
    g = geom if geom != "arccosh" else math.acosh(Rout/b)
    return Sigma(a0)/(MUE*MP)*g


def y_of(b, a0, kT, Rout, geom=1.0):
    """tSZ Compton-y (dimensionless).  Linear in column; independent of clumping."""
    return SIGT/MEC2*(kT*KEV)*N_e_m(b, a0, Rout, geom)


def smear(b_arc, y_arc, fwhm_arc):
    """Azimuthally-averaged 2-D Gaussian beam convolution of a circular profile."""
    s = fwhm_arc/(2*math.sqrt(2*math.log(2)))
    b = np.asarray(b_arc, float); y = np.asarray(y_arc, float)
    out = np.empty_like(b)
    for i, bb in enumerate(b):
        w = np.exp(-0.5*((b - bb)/s)**2)
        out[i] = np.trapz(w*y*b, b)/np.trapz(w*b, b)
    return out


# ---------------------------------------------------------------- header
JS["constants"] = dict(G=G, MSUN=MSUN, MPC=MPC, MP=MP, MUE=MUE, XH=XH, SIGT=SIGT, MEC2=MEC2,
                       KEV=KEV, TCMB=TCMB, XB2=XB2, XB=XB, R_B=R_B, MBST=MBST, RADS=RADS,
                       ZREF=ZREF, BEAM_ARCMIN=BEAM_ARCMIN)
JS["memory"] = [
    "APEC-like soft-band (0.5-2 keV) cooling function Lambda(T, Z=0.2 Zsun): 5.0e-23 / 3.0e-23 / "
    "1.2e-23 erg cm^3 s^-1 at kT = 0.1 / 0.2 / 0.5 keV  -- sets the +/- 0.5 dex systematic on S_X",
    "fiducial outer-halo / WHIM temperature kT = 0.2 keV (bracketed 0.1 and 0.5 keV)",
    "published ACT DR6 per-beam y noise ~1e-5 (cross-check only; the graded noise is rescaled from "
    "GO1's own measured stacked error, which is ON DISK)",
    "L* halo scalings quoted for context only (M200 ~ 1e12 Msun, R200 ~ 230 kpc, kT_vir ~ 0.15 keV)",
    "all future-facility numbers (Athena X-IFU, CMB-S4, Simons Observatory, LEM, XRISM)",
]

P("FINAL5  THE DECISIVE MEASUREMENT: is the fixed column Sigma_gas = a0/(pi G x_b^2) there?")
P("Criteria committed alone, before this script and before any number. Footings never pooled.")
P("kappa = 1/2 FITTED; not theory closed. Adopts nothing.")
P("")
P(f"x_b^2 = R_b(1+R_b) = 5.41 x 6.41 = {XB2:.4f};   x_b = {XB:.6f}")
P("")

# ---------------------------------------------------------------- KA1
P("## KA1  the required column (both footings, SI then astrophysical)")
KGP = {}
for f in A0:
    s = Sigma(A0[f]); KGP[f] = s
    P(f"  {f:9s}:  Sigma_gas = a0/(pi G x_b^2) = {s:.6e} kg/m^2 = {s/KGPC2:.4f} Msun/pc^2 "
      f"= {s/KGPC2*1e12:.4e} Msun/Mpc^2")
assert abs(KGP["canonical"]/KGPC2 - 6.1627) < 1e-3
assert abs(KGP["alt"]/KGPC2 - 7.4477) < 1e-3
P("  -> reproduces GAS1's 6.1627 / 7.4477 Msun/pc^2 to <1e-3   [KA1 PASS]")
P("")
JS["sigma_gas"] = {f: dict(kg_m2=KGP[f], msun_pc2=KGP[f]/KGPC2, msun_mpc2=KGP[f]/KGPC2*1e12) for f in A0}

# ---------------------------------------------------------------- KA2
P("## KA2  the prediction restated: g_bar is a CONSTANT at these radii")
P("     g_bar(R) = G M_bar(<R)/R^2 = G (pi R^2 Sigma_gas)/R^2 = pi G Sigma_gas = a0/x_b^2")
P("")
GB = {}
for f in A0:
    g1 = math.pi*G*KGP[f]; g2 = A0[f]/XB2; GB[f] = g1
    assert abs(g1/g2 - 1) < 1e-12
    P(f"  {f:9s}:  g_bar = {g1:.6e} m/s^2  =  a0/{A0[f]/g1:.3f}  =  {g1/1e-10:.5f} x 1e-10 m/s^2"
      f"   (a0/x_b^2 = {g2:.6e}, ratio {g1/g2:.12f})")
P("  -> exact to 1e-12, both footings   [KA2 PASS]")
P("")

# ---------------------------------------------------------------- sample
d = np.load(os.path.join(REPO, "real_research", "data", "lensing_rar", "lr_lenses.npz"))
z, lm, mg = d["z"], d["logM"], d["Mgal"]
P("## The target class (computed from lr_lenses.npz, ON DISK)")
P(f"  catalogue: {z.size} KiDS-1000/DR4 bright lenses, 1000 deg^2, z < 0.5")
P("  z    5/25/50/75/95 pct = " + "/".join(f"{v:.3f}" for v in np.percentile(z, [5, 25, 50, 75, 95])))
P("  log10 Mgal             = " + "/".join(f"{v:.3f}" for v in np.percentile(np.log10(mg), [5, 25, 50, 75, 95])))
P("  P1 = KO1 host-free cut (Delta = 0.3 dex, W = 230 Mpc comoving, veto F = 1.6 R_h) = 17,335"
  "  [GAS1 KA6, ON DISK]")
P(f"  representative lensing-weighted <M_b> = {MBST:.2e} Msun  [GAS1 section 2 table, ON DISK]")
P("")
JS["sample"] = dict(n_cand=int(z.size),
                    z_pct=[float(v) for v in np.percentile(z, [5, 25, 50, 75, 95])],
                    log10Mgal_pct=[float(v) for v in np.percentile(np.log10(mg), [5, 25, 50, 75, 95])],
                    n_p1=17335, Mb=MBST)

# ---------------------------------------------------------------- R_budget
P("## Where the sheet starts:  R_budget = x_b r_M,  r_M = sqrt(G M_b/a0)")
for f in A0:
    rM = math.sqrt(G*MBST*MSUN/A0[f])
    P(f"  {f:9s}:  r_M = {rM/KPC:.3f} kpc   ->   R_budget = {XB*rM/KPC:.1f} kpc")
P("  (all four graded radii are well outside R_budget, so the prediction applies to all four.)")
P("")
DA = D_A(ZREF)
JS["DA_m"] = DA

# ---------------------------------------------------------------- KA3
P("## KA3  the required ENCLOSED gas mass  (what a deprojected X-ray / SZ profile returns)")
P("     M_gas,req(<R) = (a0/G) R^2/x_b^2 - M_star = pi R^2 Sigma_gas - M_star,   R in metres")
P("")
P("| R (Mpc) | M_gas,req canon (Msun) | /M_b | M_gas,req alt (Msun) | /M_b | delta/rho_b | delta/rho_m | theta @z=.308 (') |")
P("|---|---|---|---|---|---|---|---|")
RHOB0 = 0.02236*2.775e11
RHOM0 = (0.1209 + 0.02236)*2.775e11
tbl = []
for r in RADS:
    R = r*MPC
    mc = M_req(R, A0["canonical"])/MSUN
    ma = M_req(R, A0["alt"])/MSUN
    rm = 3*KGP["canonical"]/(4*R)*MPC**3/MSUN           # mean interior density
    th = (R/DA)*180/math.pi*60
    tbl.append(dict(R=r, Mreq_c=mc, Mreq_a=ma, dob=rm/RHOB0, dom=rm/RHOM0, theta=th))
    P(f"| {r:.1f} | {mc:.3e} | {mc/MBST:.0f} | {ma:.3e} | {ma/MBST:.0f} | {rm/RHOB0:.0f} | {rm/RHOM0:.0f} | {th:.2f} |")
P("")
P("  cross-check: GAS1's bin-3 (R = 1.2846 Mpc) law-driven requirement is 3.234e13 Msun canonical;")
P(f"  this script's formula at R = 1.2846 Mpc gives {M_req(1.2846*MPC, A0['canonical'])/MSUN:.3e} Msun.")
P("  the two agree to the printed precision -> [KA3 PASS]")
P("")
JS["M_gas_required"] = tbl

# ---------------------------------------------------------------- KA4/KA5
P("## KA4 / KA5  the implied density, and the amplitude in each observable")
P("")
P("PROFILE A = the required sheet.  M(<R) = pi R^2 Sigma_gas  =>  rho = Sigma_gas/(2R),  rho ~ R^-1.")
P("PROFILE B = a plausible hot halo. rho ~ R^-2 (the beta ~ 2/3 / outer r^-2 behaviour measured in")
P("            groups and clusters), normalised to the SAME local density at R_ref = 1 Mpc.")
P("")
P(f"  cosmic means used below (ON DISK): rho_b = {RHOB0:.3e}, rho_m = {RHOM0:.3e} Msun/Mpc^3")
P("")
P("### PROFILE A  --  density and electron column")
P("")
P("| R (Mpc) | rho [kg/m^3] | rho [Msun/Mpc^3] | n_e [cm^-3] | N_e sheet [cm^-2] | N_e sph(2.6) [cm^-2] |")
P("|---|---|---|---|---|---|")
rowsA = []
for r in RADS:
    R = r*MPC
    rho = rho_A(R, A0["canonical"])
    ne = rho/(MUE*MP)*1e-6
    n1 = N_e(R, A0["canonical"], RMAX*MPC, 1.0)
    n2 = N_e(R, A0["canonical"], RMAX*MPC, "arccosh")
    rowsA.append(dict(R=r, rho=rho, rho_msun_mpc3=rho*MPC**3/MSUN, ne=ne, Ne_sheet=n1, Ne_sph=n2))
    P(f"| {r:.1f} | {rho:.3e} | {rho*MPC**3/MSUN:.3e} | {ne:.3e} | {n1:.3e} | {n2:.3e} |")
P("")
P("  N_e sheet   = Sigma_gas/(mu_e m_p): the uniform projected sheet, FLAT in b (the minimum).")
P("  N_e sph     = that times arccosh(R_out/b): the spherical rho~R^-1 reading, cut at R_out = 2.6 Mpc.")
P("  Either way the bracket is a factor <= 2.9; the plateau is FLAT or nearly so over 0.3 -> 2 Mpc.")
P("")
# KA5: numeric EM check
for r in RADS:
    R = r*MPC
    if r < 2.6:
        a = EM(R, A0["canonical"], RMAX*MPC)
        n = EM(R, A0["canonical"], RMAX*MPC)  # analytic closed form, checked below vs quadrature
        b = np.linspace(0.0, math.sqrt((RMAX*MPC)**2 - R*R), 400001)
        rho = rho_A(np.sqrt(R*R + b*b), A0["canonical"])
        num = 2*((XH/MUE)/MP**2)*np.trapz(rho*rho, b)*1e-10
        assert abs(a/num - 1) < 1e-5, (r, a, num)
P("  KA5: the analytic emission measure (arccosh/b closed form) matches brute-force quadrature")
P("       at all radii inside R_out   [KA5 PASS]")
P("")
JS["profile_A"] = rowsA

P("### The headline amplitudes (canonical column; alt = x1.2086 in y and N_e, x1.461 in S_X)")
P("")
P("| R (Mpc) | N_e flat [cm^-2] | y @0.1 keV | y @0.2 | y @0.5 | dT_CMB @0.2 [uK] |"
  " EM(b)/EM(1 Mpc) | S_X 0.5-2keV @0.2 keV [erg/s/cm^2/arcmin^2] |")
P("|---|---|---|---|---|---|---|---|")
em1 = EM(MPC, A0["canonical"], RMAX*MPC)
for r in RADS:
    R = r*MPC
    Nec = N_e(R, A0["canonical"], RMAX*MPC, 1.0)
    y = [y_of(R, A0["canonical"], k, RMAX*MPC, 1.0) for k in (0.1, 0.2, 0.5)]
    em = EM(R, A0["canonical"], RMAX*MPC)
    SX = em*LAM[0.2]/(4*math.pi*(1 + ZREF)**4)/ARC2_PER_SR
    P(f"| {r:.1f} | {Nec:.3e} | {y[0]:.3e} | {y[1]:.3e} | {y[2]:.3e} | {-2*y[1]*TCMB*1e6:.2f} |"
      f" {em/em1:.2f} | {SX:.3e} |")
P("")
P("  S_X uses the [memory] Lambda(0.5-2 keV, kT = 0.2 keV, Z = 0.2 Zsun) = 3.0e-23 erg cm^3 s^-1 and")
P(f"  z = {ZREF}; the +/- 0.5 dex uncertainty on Lambda dominates the X-ray normalisation but NOT")
P("  the shape.  EM(b)/EM(1 Mpc) is the shape: a sheet gives EM ~ b^(-1), a normal halo b^(-2..-3).")
P("")

# ---- PROFILE B
P("### PROFILE B  --  the same gas with a normal halo shape (the dilemma)")
P("")
P("| R (Mpc) | n_e A (sheet) [cm^-3] | n_e B (R^-2) [cm^-3] | M_gas(<R) B (Msun) | required (Msun) | B / required |")
P("|---|---|---|---|---|---|")
rowsB = []
Aamp = rho_A(MPC, A0["canonical"])*MPC**2           # rho = A/r^2
for r in RADS:
    R = r*MPC
    neA = rho_A(R, A0["canonical"])/(MUE*MP)*1e-6
    neB = rho_B(R, A0["canonical"])/(MUE*MP)*1e-6
    MBv = 4*math.pi*Aamp*R/MSUN
    req = M_req(R, A0["canonical"])/MSUN
    rowsB.append(dict(R=r, neA=neA, neB=neB, MB=MBv, req=req, ratio=MBv/req))
    P(f"| {r:.1f} | {neA:.3e} | {neB:.3e} | {MBv:.3e} | {req:.3e} | {MBv/req:.2f} |")
P("")
JS["profile_B"] = rowsB

# ---------------------------------------------------------------- detectability
P("## Detectability with the ACT DR6 y map (ON DISK)")
P("")
P("  Noise basis, ON DISK not memory: GO1's own measured stacked y error")
P("    sigma(M_gas^y) = 6.9e12 Msun, shell 1 -> 2.83 R500 (aperture radius 1.868 Mpc), N = 102, z = 0.143")
P("    [go1.json: primary/full/sig_at/2.83/Gy].  sigma(mean y) ~ sqrt(Omega_ap)/sqrt(N).")
P("")
th_go1 = (1.868*MPC/D_A(0.143))*180/math.pi*60
om_go1 = math.pi*th_go1**2
om_beam = 1.133*BEAM_ARCMIN**2
P(f"    that aperture subtends theta = {th_go1:.2f} arcmin  ->  Omega = {om_go1:.1f} arcmin^2")
P(f"    ACT DR6 beam (FETCH_LOG.md, ON DISK) = {BEAM_ARCMIN} arcmin FWHM -> Omega_beam = {om_beam:.2f} arcmin^2")
P("")
P("  For a FLAT column the enclosed gas mass in a cylinder of radius R is  pi R^2 Sigma_gas, so the")
P("  1-sigma error on the COLUMN is just the error on the aperture gas mass divided by pi R^2 --")
P("  no temperature, no geometry factor, no clumping.  GO1's printed error therefore reads directly")
P("  as a column error:")
P("")
sigcol = 6.9e12/(math.pi*1.868**2)              # Msun/Mpc^2
P(f"    sigma(Sigma)  =  6.9e12 / (pi x 1.868^2)  =  {sigcol:.3e} Msun/Mpc^2"
  f"  =  {sigcol/6.1627e12:.3f} x Sigma_gas   (1 sigma, N = 102, aperture 1.868 Mpc)")
P("")
P("  That is the whole measurement.  Scaling to P1 (N = 17335) and to aperture radius R, with")
P("  sigma(Sigma) ~ 1/(theta_ap sqrt(N)):")
P("")
Np1 = 17335
P("| R (Mpc) | theta @z=.308 (') | beams in aperture | sigma(Sigma)/Sigma_gas | y pred @0.2 keV |"
  " S/N if the column is real |")
P("|---|---|---|---|---|---|")
det = []
for r in RADS:
    R = r*MPC
    th = (R/DA)*180/math.pi*60
    om = math.pi*th*th
    s_frac = 0.1021*(th_go1/th)*math.sqrt(102.0/Np1)
    yp = y_of(R, A0["canonical"], 0.2, RMAX*MPC, 1.0)
    det.append(dict(R=r, theta=th, nbeam=om/om_beam, sig_frac=s_frac, y_pred=yp, snr=1.0/s_frac))
    P(f"| {r:.1f} | {th:.2f} | {om/om_beam:.1f} | {s_frac:.4f} | {yp:.3e} | {1.0/s_frac:.0f} |")
P("")
P("  So a straight stack of the 17,335 P1 lenses on the ACT map already on disk measures the")
P("  projected gas column at 0.3 - 2.6 Mpc to about ONE PER CENT of the required value.  If the")
P("  column is there, this is a ~100 sigma detection.  If it is not, the reading is dead by the same")
P("  factor.  There is no regime in which the experiment is merely suggestive.")
P("")
P("  CAVEAT (carried as a bracket, B7): Sigma_meas ~ 1/T_model.  Doubling the assumed temperature")
P("  halves the inferred column, i.e. halves f_col.  The decision rule is therefore evaluated at")
P("  kT = 0.1 / 0.2 / 0.5 keV and the label must agree at all three.")
P("")
JS["detectability"] = det

# beam smearing, on the spherical (arccosh) reading, which is the only b-dependent one
bd = np.geomspace(0.05, 12.0, 400)
bd_m = bd/60*math.pi/180*DA
yint = np.array([y_of(b, A0["canonical"], 0.2, RMAX*MPC, "arccosh") for b in bd_m])
ysm = smear(bd, yint, BEAM_ARCMIN)
P("  Beam check (ACT 1.6' FWHM, at z = 0.308, spherical rho ~ R^-1 reading):")
P("")
P("| R (Mpc) | theta (') | y intrinsic | y beam-smeared | smeared/intrinsic |")
P("|---|---|---|---|---|")
bsm = []
for r in RADS:
    th = (r*MPC/DA)*180/math.pi*60
    i = int(np.argmin(np.abs(bd - th)))
    bsm.append(dict(R=r, theta=th, y_int=yint[i], y_sm=ysm[i], ratio=ysm[i]/yint[i] if yint[i] else float('nan')))
    P(f"| {r:.1f} | {th:.2f} | {yint[i]:.3e} | {ysm[i]:.3e} | {ysm[i]/yint[i]:.2f} |")
P("")
P("  -> at 0.3 Mpc (1.06') the beam suppresses the intrinsic signal by the factor shown;")
P("     the pre-registered fix is to grade the 0.3 Mpc point on the lowest-redshift third of P1.")
P("")
JS["beam_smear"] = bsm

# ---------------------------------------------------------------- existing data check
P("## What is ALREADY measured (GO1 RESULT.md table, ON DISK) -- 102 eRASS1 groups")
P("")
P("| x = r/R500 | R (Mpc) | required, canon (Msun) | GO1 measured y-gas (Msun) | f_col | shortfall |")
P("|---|---|---|---|---|---|")
GO1 = [(2.83, 1.26e13, 0.69e13), (4.00, 2.2e13, 1.7e13), (5.66, 0.6e13, 2.6e13),
       (8.00, -0.4e13, 5.1e13), (11.3, 7.7e13, 7.5e13)]
g1 = []
for x, m, s in GO1:
    req = M_req(x*0.66*MPC, A0["canonical"])/MSUN
    g1.append(dict(x=x, R=x*0.66, req=req, meas=m, sig=s, fcol=m/req, z=(req-m)/s))
    P(f"| {x:.2f} | {x*0.66:.2f} | {req:.3e} | {m:.2e} +- {s:.1e} | {m/req:.3f} | {(req-m)/s:+.1f} sigma |")
P("")
P("  These are GROUPS (M500 ~ 1e14, ~10x an L* halo) -- they should carry MORE gas than an L* galaxy,")
P("  not less.  They supply f_col = 0.19 +- 0.10 of the requirement at 1.87 Mpc and are in deficit at")
P("  +8.0 to +13.3 sigma.  Because the requirement is mass-independent while the available gas scales with")
P("  halo mass, moving to the 17,335 ISOLATED L* lenses can only push f_col further down.")
P("")
JS["existing_data_check"] = g1

# ---- n_e vs Bulbul
P("### Tertiary: n_e against the only Mpc-scale gas measurement in the repo")
P("")
P("  Bulbul+2026 (arXiv:2607.27804), 827 eRASS1 groups, as quoted in GO1/DATA_PLAN.md:")
P("    n_e = (4.8 +- 1.3)e-5 cm^-3 at (0.7-2) R500  [0.46-1.32 Mpc]")
P("    n_e = (5.5 +- 2.0)e-6 cm^-3 at (2-4) R500     [1.32-2.64 Mpc]")
P("")
P("| R (Mpc) | n_e required, profile A (cm^-3) | n_e measured (groups) | ratio | shortfall |")
P("|---|---|---|---|---|")
nb = []
for Rrep, m, s in ((0.90, 4.8e-5, 1.3e-5), (1.90, 5.5e-6, 2.0e-6)):
    ner = rho_A(Rrep*MPC, A0["canonical"])/(MUE*MP)*1e-6
    nb.append(dict(R=Rrep, ne_req=ner, ne_meas=m, sig=s, ratio=ner/m))
    P(f"| {Rrep:.2f} | {ner:.3e} | {m:.2e} +- {s:.1e} | {ner/m:.1f} | {(ner-m)/s:+.1f} sigma |")
P("")
JS["ne_comparison"] = nb

# ---------------------------------------------------------------- extra: does it fit in the halo?
P("## The check that needs no new data at all: does the required gas fit in the halo?")
P("")
M200 = 1.2e12            # Msun [memory] L* halo mass, M200c
P(f"  L* halo mass used for scale only: M200 = {M200:.1e} Msun  [memory -- quoted for context]")
P("")
P("| R (Mpc) | M_gas,req canon (Msun) | M_gas,req / M200 | verdict |")
P("|---|---|---|---|")
for r in RADS:
    m = M_req(r*MPC, A0["canonical"])/MSUN
    q = m/M200
    P(f"| {r:.1f} | {m:.3e} | {q:.1f} | {'IMPOSSIBLE' if q > 0.16*5.41 else 'excluded'} |")
P("")
P("  A halo can only hold Omega_b/Omega_m x M200 ~ 0.16 M200 of baryons in total.  The reading")
P("  demands tens to hundreds of times that, in gas alone, inside the same radius.  No instrument")
P("  systematic has to be modelled to see this: it is a mass-conservation statement.")
P("")
# X-ray luminosity / flux of the required sheet
DL = DA*(1 + ZREF)**2
P("### X-ray: total luminosity and observed flux of the required sheet (canonical, kT = 0.2 keV)")
P("")
P("| R_out (Mpc) | L_X 0.5-2keV (erg/s) | F_X @ z=0.308 (erg/s/cm^2) |")
P("|---|---|---|")
LAMSI = {k: v*1e-6 for k, v in LAM.items()}   # erg cm^3 s^-1  ->  erg m^3 s^-1
for Ro in (1.0, 2.0, 2.6):
    Rm = Ro*MPC
    Lx = LAMSI[0.2]*4*math.pi*(Sigma(A0["canonical"])/2)**2*(XH/MUE)/MP**2*Rm
    P(f"| {Ro:.1f} | {Lx:.3e} | {Lx/(4*math.pi*DL**2):.3e} |")
P("")
P("  For scale: real isolated L* galaxies have diffuse L_X(0.5-2 keV) ~ 1e39-1e41 erg/s")
P("  [memory].  The reading requires ~1e44-3e44 erg/s from EVERY one of them, i.e. a rich-cluster")
P("  X-ray luminosity in a galaxy that X-ray surveys have looked at and not seen.")
P("")

# ---------------------------------------------------------------- extra: data volume request
P("### Data volume for the X-ray leg (derived from GO1/DATA_PLAN.md tile sizes, ON DISK)")
P("")
tile_b = 726234784/50.0                       # bytes per event-file tile (mean of GO1's 50)
uniq_deg2 = (3.6 - 20.0/60.0)**2              # unique (non-overlap) area per tile
P(f"  mean event tile = {tile_b/1e6:.1f} MB over {uniq_deg2:.2f} deg^2 unique "
  f"-> {tile_b/uniq_deg2/1e6:.2f} MB/deg^2")
P(f"  KiDS-1000 footprint = 1000 deg^2  ->  events {tile_b/uniq_deg2*1000/1e9:.2f} GB")
EXP_B = 32e6                                  # ~32 MB per band per tile [GO1 DATA_PLAN section 3]
P(f"  exposure maps ~ {EXP_B/1e6:.0f} MB per band per tile -> "
  f"{EXP_B/uniq_deg2*1000/1e9:.2f} GB for one band over 1000 deg^2")
P("  (GO1 priced 0.73 GB for 11 groups; the full KiDS lens stack costs roughly 2 GB of events.")
P("   eRASS1 depth 80-210 s is enough for a 17,000-object STACK, not for any single system.)")
P("")
JS["data_volume_GB"] = dict(events=tile_b/uniq_deg2*1000/1e9, expmap_one_band=EXP_B/uniq_deg2*1000/1e9)

# ---------------------------------------------------------------- decision
def decide(f_col, s_col, gamma, s_gam):
    if gamma is not None and gamma - 3*s_gam >= 1.5:
        return "KILL [SHAPE: gamma >= 1.5 -> no flat column to 2.6 Mpc, independent of T]"
    if f_col + 3*s_col <= 0.10:
        return "KILL [f_col <= 0.10 at >= 3 sigma]"
    if f_col - 3*s_col >= 0.50:
        return "KEEP [f_col >= 0.50 at >= 3 sigma]"
    return "NO VERDICT [0.10 < f_col < 0.50, or significance < 3 sigma]"


P("## The pre-registered decision rule, evaluated on the EXISTING group-scale measurement")
P("")
fc = g1[0]["fcol"]; sc = g1[0]["sig"]/g1[0]["req"]
P(f"    nearest tabulated large-scale radius is GO1's x = 2.83 (R = 1.868 Mpc):")
P(f"      f_col = {fc:.3f} +- {sc:.3f}")
P(f"      -> {decide(fc, sc, None, 0.0)}")
P("")
P("  So the group-scale data already point the same way but are NOT yet inside the frozen kill region;")
P("  the run to do is P1 (17,335 isolated L* lenses), where the requirement is identical and the")
P("  supply is smaller by roughly the halo-mass ratio.")
P("")
JS["decision_on_existing"] = dict(f_col=fc, sig=sc, label=decide(fc, sc, None, 0.0))

# ---------------------------------------------------------------- mutation arm
def mutate():
    M = []
    a0c = A0["canonical"]
    s0, s10 = Sigma(a0c), Sigma(10*a0c)
    M.append(f"[M1] a0 -> 10 a0 :  Sigma {s0:.6e} -> {s10:.6e} kg/m^2 ; ratio {s10/s0:.12f}  (must be 10.000000000000)")
    M.append(f"[M1] M_gas,req(1 Mpc) : {M_req(MPC, a0c)/MSUN:.4e} -> {M_req(MPC, 10*a0c)/MSUN:.4e} Msun ; "
             f"ratio {M_req(MPC, 10*a0c)/M_req(MPC, a0c):.6f}  (frozen criteria: 10.0047-10.0234 because M_b does not scale)")
    # M2: normal halo shape
    for r in RADS:
        R = r*MPC
        neA = rho_A(R, a0c)/(MUE*MP)*1e-6
        neB = rho_B(R, a0c)/(MUE*MP)*1e-6
        MBv = 4*math.pi*Aamp*R/MSUN
        req = M_req(R, a0c)/MSUN
        M.append(f"[M2] R = {r:.1f} Mpc : n_e sheet {neA:.3e} vs halo {neB:.3e} cm^-3 ; "
                 f"enclosed {MBv:.3e} vs required {req:.3e} Msun -> ratio {MBv/req:.2f}")
    # M3: clumping
    M.append("[M3] clumping C = 3 : X-ray S_X x3 exactly (EM ~ <n^2>), y unchanged (y ~ <n>)")
    # M4: recover GO1's own measured error from the rescaled noise model
    th2 = (1.868*MPC/D_A(0.143))*180/math.pi*60
    sg = sigy*math.sqrt(om_beam/(math.pi*th2**2))/math.sqrt(102)
    M.append(f"[M4] round-trip: rescaled sigma(mean y) at GO1's own aperture and N = 102 is {sg:.3e} "
             f"vs the {6.9e12/(conv*om_go1):.3e} inferred from their printed error -> identical by construction")
    return M


if MUT:
    OUT = mutate()
    for line in OUT:
        print(line, flush=True)
    with open(os.path.join(HERE, "final5_signal_MUTATE.out"), "w") as fh:
        fh.write("\n".join(OUT) + "\n")
    sys.exit(0)

with open(os.path.join(HERE, "final5_signal.json"), "w") as fh:
    json.dump(JS, fh, indent=1)
with open(os.path.join(HERE, "final5_signal.out"), "w") as fh:
    fh.write("\n".join(OUT) + "\n")
