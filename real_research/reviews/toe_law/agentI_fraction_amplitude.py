#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
agentI_fraction_amplitude.py
============================
The GO/NO-GO fraction-amplitude test named decisive by agentH4 (section 7) for the
NONHUYGENS_DOOR_SYNTHESIS spec: can an ultralight field limited to a fraction f <~ 1-3%
of the dark sector produce the FULL MOND-amplitude effect -- in the deep-MOND galactic
regime an effective dynamics equivalent to g_obs = sqrt(g_bar*a0), a0 = 9.36e-11 m/s^2,
i.e. an ORDER-UNITY modification of baryon dynamics at the RAR knee?

  PART 1  sourcing route : the carrier gravitationally supplies the phantom mass
                           (the superfluid-template route; lensing included)
  PART 2  mediator route : the carrier mediates an inertia/dynamics modification
                           (the N2/N3 memory channel); energy density only supports
                           the COUPLING amplitude, not the mass budget
  PART 3  crossfire      : lensing wall / Cherenkov gate / Gaia-DR4 knee discriminator

Discipline (working rule + Door-III discipline): RAW NUMBERS FIRST, comparisons after;
both a0 conventions and both footings run where they could matter; every external number
arXiv-pinned in the printed PIN table; charity choices resolved IN FAVOR of the framework
and labelled as such; no coefficient claims. No git.

Run:  python3 agentI_fraction_amplitude.py > agentI_fraction_amplitude.out
"""
import math

# =========================================================================================
# 0. CONSTANTS AND PINNED INPUTS  (every external number pinned; printed below)
# =========================================================================================
G         = 6.674e-11            # m^3 kg^-1 s^-2
c_SI      = 2.99792458e8         # m/s
Msun      = 1.989e30             # kg
pc        = 3.0857e16            # m
kpc       = 1e3*pc
Mpc       = 1e6*pc
hbar_eVs  = 6.582119569e-16      # eV s
hbarc_eVm = 1.97326980e-7        # eV m
MPl_red   = 2.435e27             # eV (reduced Planck mass, standard)
kg_to_eV  = 5.6096e35            # eV per kg
inv_m3_to_eV3 = hbarc_eVm**3     # 1 m^-3 = (hbar c)^3 eV^3 = 7.684e-21 eV^3
rho_SI_to_eV4 = kg_to_eV*inv_m3_to_eV3       # kg/m^3 -> eV^4
GeVcm3_to_SI  = 1.78266e-21                  # GeV/cm^3 -> kg/m^3
GeVcm3_to_eV4 = GeVcm3_to_SI*rho_SI_to_eV4   # GeV/cm^3 -> eV^4 (~7.68e-6)

# cosmology (Planck 2018, arXiv:1807.06209)
H0_kms    = 67.36
h_planck  = 0.6736
Och2      = 0.1200
OLam      = 0.6847
H0_SI     = H0_kms*1e3/Mpc                       # s^-1
HLam_SI   = math.sqrt(OLam)*H0_SI                # Lambda footing (framework canonical)
H0_eV     = hbar_eVs*H0_SI
HLam_eV   = hbar_eVs*HLam_SI
rho_crit  = 3*H0_SI**2/(8*math.pi*G)             # kg/m^3
Omega_c   = Och2/h_planck**2
rho_dm_cosmic_SI  = Omega_c*rho_crit             # kg/m^3 (cosmic mean DM)
rho_dm_cosmic_eV4 = rho_dm_cosmic_SI*rho_SI_to_eV4
rho_dm_cosmic_GeVcm3 = rho_dm_cosmic_SI/GeVcm3_to_SI

# accelerations (both conventions per working rule)
a0_fw  = 9.36e-11   # framework canonical (pure-Lambda footing; repo convention)
a0_def = 1.2e-10    # regular-MOND default (baseline check)

# MW halo pins (per tasking: M200 = 1e12, standard NFW)
M200   = 1e12*Msun
c200   = 10.0       # Dutton & Maccio 2014, arXiv:1402.7073 (c(M) at 1e12 Msun); MW mass
                    # cross-pin Wang+ 2020 review arXiv:1912.02599 (M_MW ~ 1.2e12)
rho200 = 200*rho_crit
R200   = (3*M200/(4*math.pi*rho200))**(1.0/3.0)
Rs     = R200/c200

# MW baryons: Bland-Hawthorn & Gerhard 2016, arXiv:1602.07702
Mstar  = 5.0e10*Msun
Mgas   = 1.1e10*Msun
Mbar   = Mstar + Mgas
Rd     = 2.6*kpc    # exponential disc scale length (same pin)

# local densities
rho_dm_local_GeVcm3      = 0.3   # EPTA convention, arXiv:2306.16228 (H4 ledger anchor)
rho_dm_local_hi_GeVcm3   = 0.4   # charity edge: Read 2014 arXiv:1404.1938 (0.2-0.6);
                                 # de Salas & Widmark 2021 arXiv:2012.11477
rho_b_mid_Msunpc3        = 0.084 # midplane baryons, McKee+ 2015 arXiv:1509.05334
rho_b_mid_SI  = rho_b_mid_Msunpc3*Msun/pc**3
rho_b_mid_eV4 = rho_b_mid_SI*rho_SI_to_eV4

# couplings / bounds
beta_C   = 3.39e-3   # Cassini: |gamma-1| <= 2.3e-5 => 2*beta^2 <= 2.3e-5 (Bertotti+ 2003
                     # via Will arXiv:1403.7377) -- agentN3's convention, kept for continuity
# MICROSCOPE final (composition-dependent): eta = (-1.5 +/- 2.3 +/- 1.5)e-15, arXiv:2209.15487
# (binds non-universal couplings harder; the universal Cassini number is the operative one here)

# velocities
v200  = 200e3        # m/s; lambda_dB convention of agentH4 (lambda_dB = hbar/(m v))
v_orb = 220e3        # m/s; stellar orbital speed for the Cherenkov kinematics

# the knee band (NONHUYGENS_DOOR_SYNTHESIS item 3; agentN2 section 4)
m_floor   = 1.3e-29  # eV
m_top     = 1.6e-24  # eV (framework); hostile ceiling 2.6e-25 (agentN2)
m_top_hos = 2.6e-25
m_DR4     = 5e-28    # eV (Gaia DR4 wide-binary knee discriminator split)

def lam_dB_m(m_eV, v=v200):
    """de Broglie length, H4 convention lambda_dB = hbar/(m v), in meters."""
    return hbarc_eVm/(m_eV*(v/c_SI))

def ledger_f(m_eV):
    """Allowed DM fraction (hard, charitable) from agentH4 section B2 ledger.
    [1.3e-29,1e-27]: f <~ 0.01-0.05 (hardest 0.013 at 1e-27, eROSITA 2502.03353);
    [1e-27,1e-25]:   f <~ 0.03, contested up to ~0.1 (2301.08361 vs 2502.03353);
    [1e-25,1.6e-24]: f <~ 0.2-0.3 (Lya-fractional 1708.00015; EPTA 2306.16228)."""
    if m_eV < 1e-27:  return (0.01, 0.05)
    if m_eV < 1e-25:  return (0.03, 0.10)
    return (0.2, 0.3)

def g_nfw(y):
    return math.log(1.0+y) - y/(1.0+y)

def M_nfw(R):
    return M200*g_nfw(R/Rs)/g_nfw(c200)

def Mbar_enc(R):
    """enclosed baryons: exponential disc factor (bulge+gas folded in; >=20 kpc it is ~1)"""
    x = R/Rd
    return Mbar*(1.0 - (1.0+x)*math.exp(-x))

def nu_rar(y):
    """McGaugh RAR interpolation nu(y) = 1/(1-exp(-sqrt(y))), y=g_bar/a0 (arXiv:1609.05917)"""
    return 1.0/(1.0 - math.exp(-math.sqrt(y)))

def g_obs_rar(gbar, a0):
    return gbar*nu_rar(gbar/a0)

def fmt(x, w=10, p=2):
    return f"{x:{w}.{p}e}"

print("="*100)
print("agentI_fraction_amplitude -- the H4-section-7 GO/NO-GO: fraction-limited carrier vs full MOND amplitude")
print("="*100)
print("""
PINNED INPUTS (raw, before any comparison)
------------------------------------------""")
print(f"  H0 = {H0_kms} km/s/Mpc = {H0_SI:.4e} s^-1 ; H_Lambda = {HLam_SI:.4e} s^-1 (Planck 2018, 1807.06209)")
print(f"  hbar*H0 = {H0_eV:.4e} eV ; hbar*H_Lambda = {HLam_eV:.4e} eV")
print(f"  rho_crit = {rho_crit:.4e} kg/m^3 ; Omega_c = {Omega_c:.4f}")
print(f"  rho_DM_cosmic = {rho_dm_cosmic_SI:.4e} kg/m^3 = {rho_dm_cosmic_GeVcm3:.4e} GeV/cm^3 = {rho_dm_cosmic_eV4:.4e} eV^4")
print(f"  rho_DM_local  = {rho_dm_local_GeVcm3} GeV/cm^3 (2306.16228) = {rho_dm_local_GeVcm3*GeVcm3_to_eV4:.4e} eV^4"
      f"   [charity edge {rho_dm_local_hi_GeVcm3} GeV/cm^3, 1404.1938/2012.11477]")
print(f"  rho_baryon_midplane = {rho_b_mid_Msunpc3} Msun/pc^3 (1509.05334) = {rho_b_mid_SI/GeVcm3_to_SI:.2f} GeV/cm^3")
print(f"  a0 = {a0_fw} (framework canonical) ; baseline check at {a0_def} (regular-MOND default)")
print(f"  MW halo: M200 = 1e12 Msun, c200 = {c200:.0f} (1402.7073; mass cross-pin 1912.02599)")
print(f"           -> R200 = {R200/kpc:.1f} kpc , Rs = {Rs/kpc:.1f} kpc")
print(f"  MW baryons: M* = 5.0e10 + gas 1.1e10 = {Mbar/Msun:.2e} Msun, Rd = 2.6 kpc (1602.07702)")
print(f"  Cassini universal-coupling bound: beta <= {beta_C} (|gamma-1|<=2.3e-5; 1403.7377 -- agentN3 convention)")
print(f"  knee band: mc^2 in [{m_floor:.1e}, {m_top:.1e}] eV (hostile top {m_top_hos:.1e}); DR4 mass {m_DR4:.1e} eV")
print(f"  consistency check: 1 GeV/cm^3 = {GeVcm3_to_eV4:.4e} eV^4 (textbook 7.684e-6 -- OK)")
print(f"  m >> H check at band floor: m_floor/(hbar*H_Lambda) = {m_floor/HLam_eV:.2e}"
      f"   (entire band is principal-series m >> H; agentN2 sec.4)")

# =========================================================================================
# PART 1 -- THE SOURCING ROUTE (superfluid template): energy budget
# =========================================================================================
print("\n" + "="*100)
print("PART 1 -- SOURCING ROUTE: phantom mass needed vs mass available in an f-fraction carrier")
print("="*100)
print("""
M_eff(R) = g_obs R^2/G with g_obs from the RAR at a0 (deep-MOND limit sqrt(g_bar a0) shown too);
M_phantom = M_eff - M_bar(R).  Carrier supply: CLUSTERED f*M_NFW(R) where lambda_dB <= R200
(the field can be halo-bound), HOMOGENEOUS f*(4pi/3) R^3 rho_DM_cosmic where lambda_dB > R200
(quasi-homogeneous cosmic background -- H4 sec. B4: it cannot cluster on a galaxy).
Charity: clustered case uses the FULL NFW profile shape for the carrier (the most favorable
concentration assumption); baryons treated as enclosed (exact exponential-disc factor).
""")

radii = [10, 20, 30, 50, 100, 200, 300, 500, 1000]   # kpc
print("RAW TABLE (a0 = 9.36e-11, framework):")
hdr = (f"{'R[kpc]':>7} {'g_bar':>10} {'g_bar/a0':>9} {'g_obs(RAR)':>11} {'g_dM=sqrt':>10}"
       f" {'M_eff[Msun]':>12} {'M_phant':>10} {'M_NFW':>10} {'M_hom(f=1)':>11}"
       f" {'f_req,clu':>10} {'f_req,hom':>10}")
print(hdr)
rows = {}
for Rk in radii:
    R = Rk*kpc
    Mb = Mbar_enc(R)
    gbar = G*Mb/R**2
    gobs = g_obs_rar(gbar, a0_fw)
    gdm  = math.sqrt(gbar*a0_fw)
    Meff = gobs*R**2/G
    Mph  = Meff - Mb
    Mnf  = M_nfw(R)
    Mhom = (4*math.pi/3.0)*R**3*rho_dm_cosmic_SI
    rows[Rk] = (Mph, Mnf, Mhom)
    print(f"{Rk:>7d} {fmt(gbar)} {gbar/a0_fw:>9.3f} {fmt(gobs,11)} {fmt(gdm)}"
          f" {fmt(Meff/Msun,12)} {fmt(Mph/Msun)} {fmt(Mnf/Msun)} {fmt(Mhom/Msun,11)}"
          f" {fmt(Mph/Mnf)} {fmt(Mph/Mhom)}")

# a0-convention robustness (working rule)
R = 100*kpc
Mb = Mbar_enc(R)
gbar = G*Mb/R**2
Mph_fw  = (g_obs_rar(gbar, a0_fw)*R**2/G - Mb)
Mph_def = (g_obs_rar(gbar, a0_def)*R**2/G - Mb)
print(f"\n  a0-convention check at R = 100 kpc: M_phantom(a0=9.36e-11)/M_phantom(a0=1.2e-10) ="
      f" {Mph_fw/Mph_def:.3f}  (a ~13% effect; nothing below turns on it)")

print("""
COMPARISON 1A -- carrier-to-job ratios at f = 0.01 and f = 0.03 (M_phantom/M_carrier):""")
print(f"{'R[kpc]':>7} {'clu f=0.01':>12} {'clu f=0.03':>12} {'hom f=0.01':>12} {'hom f=0.03':>12}")
for Rk in radii:
    Mph, Mnf, Mhom = rows[Rk]
    print(f"{Rk:>7d} {fmt(Mph/(0.01*Mnf),12)} {fmt(Mph/(0.03*Mnf),12)}"
          f" {fmt(Mph/(0.01*Mhom),12)} {fmt(Mph/(0.03*Mhom),12)}")

print("""
COMPARISON 1B -- per-decade required fraction f_req (carrier must source the effect), vs the H4 ledger.
Regime set by lambda_dB(m) vs R200; f_req quoted at R = 50 kpc (kinematic deep-MOND),
R = 300 kpc and R = 1 Mpc (the Brouwer lensing band reaches ~Mpc; sourcing must continue there).""")
m_grid = [1.3e-29, 1e-28, m_DR4, 1e-27, 1e-26, 5e-26, 1e-25, 1e-24, 1.6e-24]
print(f"{'m[eV]':>9} {'lam_dB':>10} {'regime':>12} {'f_req(50kpc)':>13} {'f_req(300kpc)':>14}"
      f" {'f_req(1Mpc)':>12} {'ledger f':>12} {'gap(min)':>10}")
for m in m_grid:
    lam = lam_dB_m(m)
    regime = "bound" if lam <= R200 else "homogeneous"
    if 0.5*R200 < lam <= R200: regime = "marginal"
    freqs = []
    for Rk in (50, 300, 1000):
        Mph, Mnf, Mhom = rows[Rk]
        freqs.append(Mph/Mnf if lam <= R200 else Mph/Mhom)
    fh, fc = ledger_f(m)
    gap = min(freqs)/fc
    lam_str = f"{lam/Mpc:.2f}Mpc" if lam > 0.5*Mpc else f"{lam/kpc:.0f}kpc"
    print(f"{m:>9.1e} {lam_str:>10} {regime:>12} {fmt(freqs[0],13)} {fmt(freqs[1],14)}"
          f" {fmt(freqs[2],12)} {fh:>5}-{fc:<6} {fmt(gap)}")
print("""  [gap(min) = MOST charitable radius x MOST charitable ledger edge -- a strict lower bound.
   At the kinematic radii (<=100 kpc) the homogeneous gaps are 3e5-3e7. And the homogeneous rows are
   doubly generous: a quasi-homogeneous component cannot concentrate within R at all (its actual
   differential pull is (4pi/3) G rho_f r); f_req is the 'even if it could all be piled up' reading.]""")

Mph1, Mnf1, _ = rows[1000]
print(f"""
  STRUCTURAL NOTE (clustered decades): even at f = 1 the sourcing route fails the Mpc lensing
  continuation: M_phantom(1 Mpc)/M_NFW(1 Mpc) = {Mph1/Mnf1:.2f} -- the MOND-amplitude lensing RAR
  measured to ~Mpc (Brouwer+2021, 2106.11677; flat lensing V_c to 1 Mpc, 2406.09685) needs
  ~{Mph1/Mnf1:.1f}x MORE mass than the entire pinned NFW halo carries there. (Caveat, both ways: a ~3x
  heavier-than-pinned outer halo is the LCDM accommodation question, outside scope; for f <= 0.03
  the gap is x{Mph1/(0.03*Mnf1):.0f} regardless.)  Second structural note: at f < 1 the OTHER (1-f) of the
  dark sector also gravitates -- crediting the carrier with the full phantom job while a (1-f) CDM-like
  partner halo sits in the same potential double-counts; the table is therefore GENEROUS to the route.""")

# =========================================================================================
# PART 2 -- THE MEDIATOR ROUTE (the spec's actual structure): amplitude per energy density
# =========================================================================================
print("\n" + "="*100)
print("PART 2 -- MEDIATOR ROUTE: coherent amplitude phi_max = sqrt(2 rho_f)/m vs order-unity coupling need")
print("="*100)
print(f"""
The carrier does NOT supply the phantom mass; it MEDIATES the inertia/dynamics modification
(N2 memory channel). Its energy budget then only caps the coherent field amplitude:
    rho_f = (1/2) m^2 phi^2  =>  phi_max = sqrt(2 rho_f)/m            [oscillating ULDM condensate]
A linear matter coupling m_p(phi) = m_p (1 + beta phi/MPl_red) -- the N3/quintessence normalization --
gives a dimensionless dynamics modification
    eps = beta * phi_max / MPl_red = beta * sqrt(2 f rho_DM) / (m * MPl_red)
SCALING (the task's derivation): eps ~ beta * sqrt(f) / m at fixed rho_DM -- improves as 1/m at fixed
density, as anticipated. Order-unity MOND at the RAR knee requires eps >= O(1); this is a NECESSARY
condition (generous: the DC inertia shift from an oscillating linear term is SECOND order in eps_lin,
so demanding eps_lin ~ 1 is the charitable floor of the requirement).
rho_f assignment: f * rho_DM_local where lambda_dB <= R200 (halo-bound), f * rho_DM_cosmic otherwise
(quasi-homogeneous background; H4 sec. B4). Both shown at the marginal mass.
""")

print("RAW TABLE (phi_max and eps across the band; f at the H4 ledger hard/charitable edges):")
print(f"{'m[eV]':>9} {'regime':>12} {'rho_f@f=.01':>12} {'phi_max[eV]':>12} {'phi/MPl':>10}"
      f" {'eps(bC,fh)':>11} {'eps(bC,fc)':>11} {'eps(b=1,fc)':>11} {'beta_req':>10} {'f_req(b=1)':>11}")
best = (0, None)
for m in m_grid:
    lam = lam_dB_m(m)
    bound = lam <= R200
    regime = "bound" if bound else "homogeneous"
    if 0.5*R200 < lam <= R200: regime = "marginal"
    rho_tot_eV4 = (rho_dm_local_GeVcm3*GeVcm3_to_eV4) if bound else rho_dm_cosmic_eV4
    fh, fc = ledger_f(m)
    phi_01 = math.sqrt(2*0.01*rho_tot_eV4)/m
    phi_fh = math.sqrt(2*fh*rho_tot_eV4)/m
    phi_fc = math.sqrt(2*fc*rho_tot_eV4)/m
    eps_bC_fh = beta_C*phi_fh/MPl_red
    eps_bC_fc = beta_C*phi_fc/MPl_red
    eps_b1_fc = 1.0*phi_fc/MPl_red
    beta_req  = MPl_red/phi_fc                     # for eps = 1 at charitable f
    f_req_b1  = (m*MPl_red)**2/(2*1.0**2*rho_tot_eV4)
    if eps_b1_fc > best[0]: best = (eps_b1_fc, m)
    print(f"{m:>9.1e} {regime:>12} {fmt(0.01*rho_tot_eV4,12)} {fmt(phi_01,12)} {fmt(phi_01/MPl_red)}"
          f" {fmt(eps_bC_fh,11)} {fmt(eps_bC_fc,11)} {fmt(eps_b1_fc,11)} {fmt(beta_req)} {fmt(f_req_b1,11)}")

# marginal mass both ways
m = 5e-26
rho_loc = rho_dm_local_GeVcm3*GeVcm3_to_eV4
phi_loc = math.sqrt(2*0.1*rho_loc)/m
phi_cos = math.sqrt(2*0.1*rho_dm_cosmic_eV4)/m
print(f"\n  marginal mass 5e-26 eV both ways (f=0.1): eps(b=1) local = {phi_loc/MPl_red:.2e},"
      f" cosmic = {phi_cos/MPl_red:.2e}")

print(f"""
COMPARISON 2A -- the make-or-break numbers:
  * BEST decade in the whole band (eps maximal): m = {best[1]:.1e} eV, eps(beta=1, ledger-charitable f)
    = {best[0]:.2e} -> short of order-unity by x{1.0/best[0]:.1e} ({math.log10(1.0/best[0]):.1f} dex) EVEN AT
    GRAVITATIONAL-STRENGTH COUPLING WITH ALL FIFTH-FORCE BOUNDS IGNORED.
  * With the Cassini bound enforced (beta = {beta_C}): best eps = {beta_C*best[0]:.2e} -> short by
    x{1.0/(beta_C*best[0]):.1e} ({math.log10(1.0/(beta_C*best[0])):.1f} dex).
  * The required coupling at the best decade: beta_req = {MPl_red/(math.sqrt(2*0.05*rho_dm_cosmic_eV4)/best[1]):.1e}
    -> a fifth force beta_req^2 = {(MPl_red/(math.sqrt(2*0.05*rho_dm_cosmic_eV4)/best[1]))**2:.1e} x gravity between unscreened
    test masses, vs the Cassini-allowed 2*beta_C^2 ~ {2*beta_C**2:.1e}: excluded by ~{(MPl_red/(math.sqrt(2*0.05*rho_dm_cosmic_eV4)/best[1]))**2/(2*beta_C**2):.0e} in force.""")

# maximum-charity stack
m_ch = 5e-26
rho_ch = 0.1 * (rho_dm_local_hi_GeVcm3*GeVcm3_to_eV4) * 100.0   # f=0.1(S8, contested) x 0.4 GeV/cc x 100 (soliton)
phi_ch = math.sqrt(2*rho_ch)/m_ch
eps_ch = phi_ch/MPl_red
m_fl = m_floor
phi_fl = math.sqrt(2*0.05*rho_dm_cosmic_eV4)/m_fl
eps_fl = phi_fl/MPl_red
eps_max_charity = max(eps_ch, eps_fl)
print(f"""
COMPARISON 2B -- MAXIMUM-CHARITY STACK (every dial at its most favorable published-contested edge):
  bound side  : m = 5e-26 eV (lowest halo-bound), f = 0.1 (contested S8 window 2301.08361),
                rho_local = 0.4 GeV/cm^3 (1404.1938 high edge), x100 central soliton overdensity
                (Schive+ 1407.7762-class relation extrapolated far beyond its f=1 validity -- pure charity):
                eps(beta=1) = {eps_ch:.2e}
  floor side  : m = 1.3e-29 eV (band floor, homogeneous so no soliton possible), f = 0.05:
                eps(beta=1) = {eps_fl:.2e}
  => the charity-stack maximum over the ENTIRE band is eps = {eps_max_charity:.2e}: the mediator route
     misses order-unity by >= x{1.0/eps_max_charity:.1e} ({math.log10(1.0/eps_max_charity):.1f} dex) with fifth-force bounds IGNORED,
     and by >= x{1.0/(beta_C*eps_max_charity):.1e} ({math.log10(1.0/(beta_C*eps_max_charity)):.1f} dex) with Cassini enforced.  NO DECADE PASSES.""")

# improvement over N3 and the vacuum-correlator sub-route
beta_N3 = 2.2e40
beta_best = MPl_red/phi_ch
m_top_ratio = m_top/HLam_eV
beta_vac_top = beta_N3/math.sqrt(1.85*m_top_ratio)   # dressing ~ q^2 m/8pi vs q^2*0.27H/4pi -> x1.85 m/H
print(f"""
COMPARISON 2C -- the 1/m improvement is REAL and it is still not enough:
  * agentN3's dS-bath coupling wall: beta_req = {beta_N3:.1e} (banked). The condensate carrier at the
    charity stack brings this down to beta_req = {beta_best:.1e} -- an improvement of ~{math.log10(beta_N3/beta_best):.0f} ORDERS,
    exactly the 1/m amplitude-per-density gain the route was built for. The remaining gap to Cassini
    is {math.log10(beta_best/beta_C):.1f} dex (and {math.log10(beta_best):.1f} dex to beta=1): the door closed from ~85 orders to ~5-7 orders
    and is still closed.
  * VACUUM-CORRELATOR sub-route (amplitude from the field's state-independent retarded tail instead of
    the condensate): dressing ~ q^2 m/8pi vs N3's q^2(0.27 H/4pi) -> beta_req improves only as
    sqrt(1.85 m/H) <= {math.sqrt(1.85*m_top_ratio):.1e} (band top) -> beta_req >= {beta_vac_top:.1e}: >= {math.log10(beta_vac_top/beta_C):.0f} orders above Cassini.
    AND the sign is wrong: N3 sec.2 (machine-verified) -- the tail dressing is MOND-signed ONLY for
    m^2 < 2H^2; the knee band is m >> H EVERYWHERE (m/H from {m_floor/HLam_eV:.1e} to {m_top/HLam_eV:.1e}),
    so the in-band vacuum dressing is ANTI-MOND-signed at every decade. The sign (needs m^2 < 2H^2)
    and the knee (needs m >> H, agentN2 sec.4) CANNOT come from the same field's vacuum tail:
    structural kill independent of amplitude.""")

# quadratic-coupling sub-route
print("""
COMPARISON 2D -- QUADRATIC-coupling escape hatch (m_p(phi) = m_p(1 + phi^2/M^2)) checked and closed:
  eps = 2 rho_f/(m^2 M^2) = 1 requires M = phi_max -- but a universal matter coupling at scale M
  gives the field a matter-induced mass m_ind = sqrt(2 rho_b)/M in the disc; with midplane baryons:""")
for m in (m_floor, m_DR4, 1e-26, m_top):
    lam = lam_dB_m(m); bound = lam <= R200
    rho_tot_eV4 = (rho_dm_local_GeVcm3*GeVcm3_to_eV4) if bound else rho_dm_cosmic_eV4
    fh, fc = ledger_f(m)
    M_req = math.sqrt(2*fc*rho_tot_eV4)/m
    m_ind = math.sqrt(2*rho_b_mid_eV4)/M_req
    print(f"    m = {m:>8.1e} eV: M_req = {M_req:.2e} eV ({M_req/MPl_red:.1e} MPl) -> m_ind = {m_ind:.2e} eV"
          f" = {m_ind/m:.1e} x m_bare")
print("""  At the eps=1 coupling the matter-induced mass exceeds the bare mass in EVERY decade (x6 at the
  band top to x7100 at the floor): the knee position is then set by the LOCAL BARYON density, not by the carrier mass --
  the universal acceleration-keyed knee (spec items 2+3) is destroyed, and the environment-dependent
  knee is an RAR-scatter liability of exactly the kind N5 killed at 5.2 sigma. Closed structurally.
  (Derivative/P(X) couplings: eps ~ 2 xi rho_f/M^4 = 1 at f=0.01-local needs M ~ 0.015 eV -- a
  universal matter coupling at meV scale is the BK-superfluid structure (Lambda ~ 0.2 meV, 1507.01019):
  the escape hatch exits INTO the fully mapped Wall-A of agentH4, not out of it.)""")

# =========================================================================================
# PART 3 -- CROSSFIRE on the (empty) passing set + the named partner
# =========================================================================================
print("\n" + "="*100)
print("PART 3 -- CROSSFIRE: lensing wall / Cherenkov gate / DR4 discriminator")
print("="*100)
print("""
Item 2 returned an EMPTY passing set; the crossfire is run anyway on (i) the hypothetical best
decade (the band floor) and (ii) the DR4 discriminator mass, both ways at full weight.
""")

# (a) lensing wall -- required partner
print("(a) THE LENSING WALL (banked: f4_lensing_wall.out -- baryon-only excluded at 40.5 sigma,")
print("    deep-bin amplitude ratio 229.7x in ESD; Brouwer+2021 2106.11677; flat V_c to 1 Mpc 2406.09685):")
print("    A mediator does not lens. With dynamics carried by the inertia channel (metric potential")
print("    stays baryonic, Phi = Phi_bar), the partner must source the LENSING potential alone:")
print("    grad(Psi) = 2 g_MOND - g_bar  =>  required gravitational slip Psi'/Phi' = 2 nu(g_bar/a0) - 1:")
for gb in (1e-13, 1e-12, 1e-11):
    nu = nu_rar(gb/a0_fw)
    print(f"      g_bar = {gb:.0e}: nu = {nu:6.2f} -> slip required = {2*nu-1:6.1f}")
mph300, mnf300, _ = rows[300]
print(f"""    The carrier's own convergence cannot help: at 300 kpc its clustered mass fraction of the job
    is f*M_NFW/M_phantom = {0.03*mnf300/mph300:.3f} at f = 0.03 (and zero in the homogeneous decades).
    NAMED PARTNER REQUIREMENT (explicit, per the task): a metric component sourcing Psi at 10-60x the
    baryonic Phi-gradient at 0.1-1 Mpc while staying inside the Cassini Q2 window [-2.0,+5.2]e-27 s^-2
    (2602.17884) at kAU and inside the MW vertical-Jeans budget (1812.08169/1911.12365) in the disc.
    The pincer, stated plainly:
      (i)  a partner with real stress-energy arranged MOND-like pulls STARS too -- it double-counts the
           mediator's dynamics and collapses the architecture to dark matter with extra steps;
      (ii) a lens-only (slip) partner has NO published field-level realization; the one Phi=Psi template
           in the literature (1602.05961 sec.6, medium 4-velocity) presupposes a metric MOND force --
           porting it re-imports the AQUAL static limit and with it the Cassini Q2 kill that took AeST
           (repo-banked) and DEW (agentD, 8.8-14.6 sigma);
      (iii) photon-disformal implementations (photons see the dark medium, matter does not) are squeezed
           by the GW170817 photon/graviton speed coincidence |Delta c|/c <~ 1e-15 (1710.05834) accumulated
           through the very halo medium that must do the lensing.""")

# (b) Cherenkov gate
print("\n(b) THE CHERENKOV GATE (2103.16954-class):")
print("    Free massive carrier, relativistic branch: omega^2 = m^2 + k^2 -> v_phase = sqrt(1+(m/k)^2) > c")
print("    for ALL k: true Cherenkov emission is kinematically FORBIDDEN (no subluminal phase velocity).")
print("    Gapless collective branch (Madelung/quasiparticle): omega = k^2/2m -> v_phase = k/2m; modes")
print("    slower than v_orb = 220 km/s exist at wavelengths lambda > pi*lambda_dB(v_orb) at EVERY in-band mass:")
for m in (m_floor, m_DR4, 1e-25, m_top):
    lam_slow = math.pi*lam_dB_m(m, v_orb)
    unit = f"{lam_slow/Mpc:.2f} Mpc" if lam_slow > 0.5*Mpc else f"{lam_slow/kpc:.1f} kpc"
    print(f"      m = {m:>8.1e} eV: slow modes at lambda > {unit}")
beta_req_best = MPl_red/phi_ch
print(f"""    [Both ways: in the homogeneous decades (m <~ 1e-26 eV) the slow modes EXCEED the system size --
    the gate has no purchase there even in principle; in the bound decades they fit (17-274 kpc).]
    Exposure scales as (matter coupling)^2 x rho_f. At beta <= beta_C = {beta_C} and f <= 0.03 the
    drag/emission exposure sits >= x{(1/beta_C)**2/0.03:.0e} below the killed BK point (order-unity effective
    coupling, all-DM medium; star lifetimes <~10 Gyr there, 2103.16954 via the H1 ledger): the gate
    PASSES trivially -- but only because the coupling is too small to matter dynamically. THE GATE AND
    THE AMPLITUDE ARE ONE DIAL: at the amplitude-required beta_req ~ {beta_req_best:.0e} the emission exposure
    rises ~beta_req^2/O(1) x f ~ 1e7 over the killed point: its <~10 Gyr lifetimes scale toward the
    kyr class. Any coupling big enough to do MOND re-arms the gate in the bound decades; any coupling
    small enough to pass the gate cannot do MOND.""")

# (c) DR4 discriminator
fh_dr4 = 0.013
phi_dr4 = math.sqrt(2*fh_dr4*rho_dm_cosmic_eV4)/m_DR4
eps_dr4_C  = beta_C*phi_dr4/MPl_red
eps_dr4_b1 = phi_dr4/MPl_red
print(f"""
(c) THE DR4 KNEE DISCRIMINATOR (m = 5e-28 eV, the hardest ledger pinch f <= {fh_dr4} -- eROSITA
    2502.03353 neighboring grid point; lambda_dB = {lam_dB_m(m_DR4)/Mpc:.1f} Mpc -> homogeneous, cosmic-mean density):
      eps(Cassini) = {eps_dr4_C:.1e}  ({-math.log10(eps_dr4_C):.1f} dex short)
      eps(beta=1)  = {eps_dr4_b1:.1e}  ({-math.log10(eps_dr4_b1):.1f} dex short)
    H4 sec.7 framed a two-branch fork: (i) mechanism works at f <= 3% -> band stays open with DR4 as
    discriminator; (ii) mechanism needs f > 3% -> knee forced into the top decades. THE FORK HAS NO
    LIVE BRANCH on this route: the top decades are the WORST in the band (eps ~ 1e-10 at Cassini),
    the floor is best and still {-math.log10(beta_C*eps_fl):.1f} dex short. The band does not narrow -- it closes.""")

# =========================================================================================
# VERDICT
# =========================================================================================
print("\n" + "="*100)
print("VERDICT (both ways, full weight)")
print("="*100)
print(f"""
NO-GO. The f-limited ultralight carrier cannot produce the full MOND-amplitude effect by ANY of the
three channels available to it, in ANY decade of the knee band, under EVERY convention checked:

  ROUTE A (sourcing, superfluid template): needs f = 0.85-1.3 at 50-200 kpc in the clustered decades
    (vs ledger 0.1-0.3: gap x2.8-8.5 at the most charitable radius), f > 1 at the Mpc lensing
    continuation EVEN BEFORE the ledger, and f ~ 2e4-3e5 at the kinematic radii in the homogeneous
    decades (vs 0.01-0.05: gap 3e5-3e7; >= 9e2 even at the most charitable radius). Dead everywhere.
  ROUTE B (mediator, condensate amplitude): eps_max = {eps_max_charity:.1e} at the maximum-charity stack with
    beta = 1 (fifth-force bounds ignored) -- {math.log10(1/eps_max_charity):.1f} dex short of order-unity; {math.log10(1/(beta_C*eps_max_charity)):.1f} dex short with
    Cassini enforced. beta_req >= {beta_req_best:.1e} everywhere = a fifth force >= {beta_req_best**2:.0e} x gravity. Dead in
    every decade; the DR4 discriminator mass sits {-math.log10(eps_dr4_C):.1f} dex short -- among the worst points.
  ROUTE C (vacuum correlator): amplitude inherits N3's wall improved only x{math.sqrt(1.85*m_top_ratio):.0e} -> >= 38 orders
    short, AND anti-MOND-signed across the whole band (sign needs m^2 < 2H^2, knee needs m >> H).

  Convention immunity: a0 footing changes M_phantom by 13%; f-ledger edges, rho_local 0.3->0.4,
  x100 soliton charity, hostile vs framework band ceiling -- all checked above; none moves any gap
  by more than ~1 dex against shortfalls of 4-38 orders. The kill is convention-immune BOTH WAYS.

  What the calculation does NOT kill (named, honest): the carrier as KNEE-SETTER with the amplitude
  paid by something else -- but the only published 'something else' candidates are (i) the dS bath
  (N3: 1e85 wall, banked), (ii) a metric MOND sector (AeST-class: Cassini Q2, banked), (iii) meV-scale
  derivative couplings (BK-class: H4 Wall-A, mapped). Every exit from this calculation lands on an
  already-banked kill. The hybrid build as specced -- fraction-limited carrier supplying the MOND
  amplitude -- dies PRE-ASSEMBLY; what survives of Door II must find an order-unity amplitude source
  OUTSIDE the carrier's energy budget, and no published structure supplies one.
""")
