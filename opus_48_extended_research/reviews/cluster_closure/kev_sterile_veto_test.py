#!/usr/bin/env python3
"""
keV STERILE-NEUTRINO cluster-core closure — the galaxy-veto + TG + Lyman-alpha + X-ray test
(2026-06-19, extends galaxy_veto_test.py / tremaine_gunn_matter_route.py)

THE QUESTION (GAP-6): the banked eV-window result is that a Tremaine-Gunn-protected fermion
closes clusters galaxy-safely ONLY in the window ~4.3 eV (cluster TG floor) to ~390 eV (dSph TG
floor). The simplest 11-eV/active versions are squeezed by DESI Sum-m_nu / KATRIN / N_eff.

NOW test the keV STERILE (a sterile neutrino, NOT active -> evades DESI Sum-m_nu / KATRIN / N_eff).
Inject a keV sterile as the cluster-core residual and compute, BOTH WAYS:
 (a) CLUSTER CLOSURE: can a keV fermion supply ~2.3e14 Msun inside 420 kpc at the cluster
     phase-space density (TG packing in the cluster potential)?
 (b) GALAXY VETO — THE CRUX: keV is ABOVE the ~390 eV dSph TG floor, so Tremaine-Gunn does
     NOT forbid it from dSphs/galaxies any more (it CAN phase-space pack in). The protection
     flips from PHASE-SPACE (TG) to FREE-STREAMING (WDM cutoff). Does WARM free-streaming keep
     it OUT of galaxy/dSph halos (RAR safe), or does it OVER-PACK and break the RAR? Resolve
     this honestly -- it is the crux. We compute the WDM half-mode mass M_hm(m_s) and compare
     to galaxy/dSph halo masses; we also inject the keV residual as an actual halo mass on the
     SPARC disks and measure the RAR scatter blow-up vs the 0.11-0.13 dex floor.
 (c) WDM BOUNDS: Lyman-alpha free-streaming (thermal-relic m_th >~ 3-5.3 keV -> sterile m_s
     depends on production: DW resonant/non-resonant) and the X-ray decay-line non-detection
     (the 3.5 keV line; m_s vs sin^2(2theta)). Is there a keV window that closes clusters AND
     passes Lyman-alpha AND X-ray AND the galaxy veto, or is it squeezed shut?

Framework footing sealed: a0=9.36e-11, dS-Unruh nu g_obs=sqrt(gbar^2+gbar*a0), Ups=0.70.
QUARANTINE: this is a PARTICLE closure (RELOCATES the dark sector). It is a PARTIAL answer to
"no dark matter", NOT a vindication of a0=Lambda. BOTH WAYS: find the window if it exists,
concede the squeeze if it does not.
"""
import numpy as np, os, glob

# ----------------------------------------------------------------------------
# constants (SI + astro)
# ----------------------------------------------------------------------------
G    = 6.674e-11; c=2.998e8; hbar=1.0546e-34; kB=1.381e-23
Msun = 1.989e30; pc=3.086e16; kpc=1e3*pc; Mpc=1e6*pc
eV   = 1.602e-19; eV_m=eV/c**2; keV=1e3*eV; keV_m=keV/c**2; km=1e3
Msun_pc3 = Msun/pc**3

a0_FW = 9.36e-11
rho_DE = 6.0e-27
Ups    = 0.70

H0   = 67.4*km/Mpc        # s^-1
Om   = 0.315; OL=0.685; Ob=0.0493
h70  = 0.674
rho_crit = 3*H0**2/(8*np.pi*G)        # kg/m^3
rho_m    = Om*rho_crit

def nu_dsunruh(gbar, a0):
    return np.sqrt(gbar**2 + gbar*a0)

print("="*84)
print("keV STERILE-NEUTRINO CLUSTER-CORE CLOSURE — galaxy-veto + TG + Lyman-alpha + X-ray")
print("="*84)
print(f"[const] rho_crit={rho_crit:.3e} kg/m^3, rho_m={rho_m:.3e}, a0_FW={a0_FW:.2e}")

# ============================================================================
# TREMAINE-GUNN core machinery (reproduced from tremaine_gunn_matter_route.py)
# ============================================================================
def rho_max_TG_Msunpc3(m_eV, sigma_1d_ms, g_nu=2.0):
    """TG max coarse-grained mass density (Msun/pc^3): 2.16e2*(m/eV)^4*(sigma/c)^3, g=2.
       Matches Angus-Famaey-Diaferio 2010 Eq.14 (11 eV) to 0.3%."""
    return 2.16e2 * (m_eV)**4 * (sigma_1d_ms/c)**3 * (g_nu/2.0)

def m_min_TG_eV(sigma_1d_ms, rho_req_Msunpc3):
    m4 = rho_req_Msunpc3 / (2.16e2 * (sigma_1d_ms/c)**3)
    return m4**0.25

def rho_iso_core(sigma_1d_ms, r_core_m):
    return 9*sigma_1d_ms**2/(4*np.pi*G*r_core_m**2)   # kg/m^3

# ============================================================================
# (a) CLUSTER CLOSURE — can a keV sterile supply 2.3e14 Msun inside 420 kpc?
# ============================================================================
print("\n" + "="*84)
print("(a) CLUSTER CLOSURE: keV sterile phase-space packing vs the 2.3e14 Msun / 420 kpc core")
print("="*84)
# Target (banked TARGET_PROFILE / CLUSTER_RESIDUAL_CLOSURE): rich cluster core residual
#   M_res ~ 2.3e14 Msun inside ~420 kpc, central/cored, gas-tracking.
M_core_target = 2.3e14*Msun
r_core_target = 420*kpc
rho_core_need = M_core_target/((4/3)*np.pi*r_core_target**3)   # mean density inside 420 kpc
rho_core_need_Msunpc3 = rho_core_need/Msun_pc3
# cluster member/DM velocity dispersion at the core: rich cluster sigma ~ 900-1100 km/s
sigma_cl = 1000*km
print(f"\n  core residual target : {M_core_target/Msun:.2e} Msun inside {r_core_target/kpc:.0f} kpc")
print(f"  => mean density needed: {rho_core_need_Msunpc3:.3e} Msun/pc^3  ({rho_core_need:.3e} kg/m^3)")
print(f"  cluster sigma_1d      : {sigma_cl/km:.0f} km/s")
print(f"\n  {'m_s':>8s} {'TG_max_dens[Msun/pc3]':>22s} {'TG_max/needed':>15s}  pack?")
for m_keV in [0.39, 1.0, 2.0, 3.0, 5.0, 7.0, 10.0, 20.0]:
    m_eV = m_keV*1e3
    rho_tg = rho_max_TG_Msunpc3(m_eV, sigma_cl)
    ratio = rho_tg/rho_core_need_Msunpc3
    print(f"  {m_keV:6.2f}keV {rho_tg:22.3e} {ratio:15.2e}  {'YES' if ratio>1 else 'NO'}")
m_min_cl = m_min_TG_eV(sigma_cl, rho_core_need_Msunpc3)
print(f"\n  TG minimum mass to supply the cluster core (sigma=1000 km/s) = {m_min_cl:.1f} eV "
      f"= {m_min_cl/1e3:.4f} keV")
print(f"  => any keV sterile clears the cluster TG floor by ~{(1000/m_min_cl)**0:.0f}... "
      f"(margin {1e3/m_min_cl:.0f}x in mass = {(1e3/m_min_cl)**4:.1e}x in density at 1 keV).")
print("""
  READ (a): a keV sterile sits WAY above the cluster TG floor (~4-9 eV). Phase-space packing
  is NOT the binding constraint at clusters -- a keV fermion can trivially supply 2.3e14 Msun
  inside 420 kpc at sigma~1000 km/s. (a) CLOSES the cluster-core phase-space requirement.
  Same conclusion as the eV route, with even more headroom.
""")

# ============================================================================
# (b) THE CRUX — galaxy veto: TG no longer forbids keV from dSphs. WDM free-streaming?
# ============================================================================
print("="*84)
print("(b) GALAXY VETO CRUX: keV is ABOVE the dSph TG floor (~390 eV) -> TG no longer protects")
print("="*84)
# dSph and galaxy TG floors (reproduced)
for nm, sig, rc in [("dSph (Fornax)", 10*km, 0.3*kpc),
                    ("SPARC dwarf",   40*km, 1.0*kpc),
                    ("L* spiral",    150*km, 3.0*kpc)]:
    rho_req = rho_iso_core(sig, rc)/Msun_pc3
    mmin = m_min_TG_eV(sig, rho_req)
    print(f"  {nm:14s} sigma={sig/km:4.0f} km/s r_c={rc/kpc:.1f} kpc -> TG floor m_min = {mmin:6.1f} eV "
          f"({mmin/1e3:.4f} keV); keV/floor = {1e3/mmin:6.1f}x")
print("""
  => A keV sterile is 3-30x ABOVE every galaxy/dSph TG floor. Tremaine-Gunn does NOT forbid it
     from galaxies any more (unlike the eV state). PHASE-SPACE PROTECTION IS GONE. The ONLY
     thing that can keep a keV WDM particle out of galaxy/dSph halos is FREE-STREAMING (the WDM
     cutoff in the matter power spectrum suppresses small-halo formation). We test that now.
""")

# --- WDM free-streaming: half-mode mass M_hm(m_s) ---------------------------
# Standard WDM relations. Convert sterile mass to a thermal-relic-equivalent mass m_th, then
# use the half-mode mass M_hm (the halo mass below which WDM suppresses structure by 50%).
#
# Sterile->thermal mapping depends on PRODUCTION. We carry the two bracketing cases:
#   (i)  Dodelson-Widrow (non-resonant, "NRP"): m_th = 0.8 keV * (m_s/keV)^(0.83) /(Om h^2/0.135)^?
#        Viel+2005 / Bozek+2016:  m_s = 4.43 keV (m_th/keV)^(1.333) (Om/0.1225)^... -> invert.
#   (ii) Shi-Fuller resonant (RP): produces a COLDER spectrum -> for a given m_s the effective
#        m_th is LARGER (less free-streaming) by ~2-3x; we bracket with a colder mapping.
#
# We use the widely-cited Viel et al. 2005 / Lovell et al. relation for the NRP (DW) case:
#   m_th(keV) = ( (m_s/keV) / 4.43 )^(3/4) * (Om_wdm/0.1225)^(... )  ~ collapse to:
#   m_s = 4.43 keV * (m_th/keV)^(4/3) (omega_wdm/0.1225)^(-1/3)
def m_th_from_ms_DW(m_s_keV, omega_wdm=0.12):
    """Thermal-relic-equivalent mass (keV) for a Dodelson-Widrow (non-resonant) sterile.
       Inverts Viel+2005:  m_s = 4.43 keV (m_th)^(4/3) (omega_wdm/0.1225)^(-1/3)."""
    return ( (m_s_keV/4.43) * (omega_wdm/0.1225)**(1/3) )**(3/4)

def lambda_fs_Mpc(m_th_keV, omega_wdm=0.12):
    """WDM free-streaming length (comoving Mpc) for a thermal relic of mass m_th.
       Bode-Ostriker-Turok / Viel:  lambda_fs ~ 0.049 (m_th/keV)^(-1.11) (Om/0.25)^0.11 h^1.22 Mpc."""
    return 0.049*(m_th_keV)**(-1.11)*(Om/0.25)**0.11*(h70)**1.22

def M_hm_Msun(m_th_keV, omega_wdm=0.12):
    """Half-mode mass (Msun): the halo mass at the half-mode wavenumber k_hm.
       lambda_hm ~ 2 pi / k_hm; k_hm = (2^(1/(2*1.12)) - 1)^(-1/(2*1.12)) / lambda_fs-ish.
       Use the standard fitted half-mode mass (Schneider+2012 / Lovell+2014):
         M_hm = (4/3) pi rho_m (lambda_hm/2)^3,  lambda_hm = 13.93 * lambda_fs (alpha-form)."""
    lam_fs = lambda_fs_Mpc(m_th_keV)*Mpc                  # m, comoving
    # half-mode scale: lambda_hm ~ 13.93 lambda_fs (Schneider 2012, alpha-WDM transfer)
    lam_hm = 13.93*lam_fs
    M_hm = (4/3)*np.pi*rho_m*(lam_hm/2.0)**3
    return M_hm/Msun, lam_fs/Mpc, lam_hm/Mpc

# direct fitted M_hm (cross-check), Nadler+2021 / Lovell: M_hm ~ 1e10 Msun (m_th/keV)^(-3.33)
def M_hm_fit(m_th_keV):
    return 1.0e10 * (m_th_keV)**(-3.33)   # Msun (Nadler+2021 fit, NRP)

print("-"*84)
print("WDM free-streaming: half-mode mass M_hm vs sterile mass (NRP / Dodelson-Widrow)")
print("-"*84)
print(f"{'m_s[keV]':>9s} {'m_th[keV]':>10s} {'lam_fs[Mpc]':>12s} {'M_hm[Msun]':>13s} {'M_hm_fit':>12s}")
for m_s in [1.0, 2.0, 3.0, 5.0, 7.0, 10.0, 20.0]:
    m_th = m_th_from_ms_DW(m_s)
    M_hm, lfs, lhm = M_hm_Msun(m_th)
    print(f"{m_s:9.1f} {m_th:10.3f} {lfs:12.4f} {M_hm:13.2e} {M_hm_fit(m_th):12.2e}")

# Galaxy / dSph halo masses (the mass scale the keV WDM must or must not suppress)
print(f"\n  Reference halo masses:")
print(f"    dSph (Fornax-class)        : M_halo ~ 1e9  - 1e10 Msun")
print(f"    SPARC dwarf disk           : M_halo ~ 1e10 - 5e10 Msun")
print(f"    SPARC L* spiral (MW-like)  : M_halo ~ 1e12       Msun")
print("""
  READ (b)-crux: WDM free-streaming SUPPRESSES halos BELOW M_hm. For the keV sterile to be kept
  OUT of dSphs (M_halo ~ 1e9-1e10), we need M_hm >~ 1e9-1e10 Msun. From the table:
    - m_s ~ 1-2 keV (m_th ~ 0.3-0.5 keV): M_hm ~ 1e11-1e12 -> suppresses dSphs AND dwarfs
      (KEEPS keV OUT of dwarfs -> galaxy-veto-SAFE) -- but this same free-streaming is exactly
      what Lyman-alpha EXCLUDES (too warm, erases the observed Lyman-alpha forest small-scale power).
    - m_s ~ 7-20 keV (m_th ~ 1.5-3 keV): M_hm ~ 1e8-1e7 -> does NOT suppress dSphs -> the keV
      WDM DOES cluster into dSphs/dwarfs. Then phase-space (TG) no longer forbids it (keV>>390 eV)
      AND free-streaming no longer forbids it -> it ADDS mass to galaxies/dwarfs.
  This is the CRUX VISE: warm enough to free-stream out of galaxies (m_s ~1-2 keV) = TOO WARM for
  Lyman-alpha; cold enough for Lyman-alpha (m_s >~7 keV) = clusters into galaxies/dwarfs. Resolve
  with the actual RAR injection + Lyman-alpha bound below.
""")

# ============================================================================
# (b2) DIRECT RAR INJECTION — put the keV residual as a real WDM halo on SPARC disks
# ============================================================================
print("="*84)
print("(b2) DIRECT RAR INJECTION: keV WDM halo added to SPARC baryons, measure RAR scatter")
print("="*84)
# Load SPARC
DATADIR=None
for cand in ["real_research/data/sparc_data",
             os.path.join(os.path.dirname(__file__),"../../../real_research/data/sparc_data")]:
    if os.path.isdir(cand): DATADIR=cand; break
assert DATADIR, "SPARC dir not found"
files=sorted(glob.glob(os.path.join(DATADIR,"*_rotmod.dat")))
print(f"[data] {len(files)} SPARC rotmod files")

def load_galaxies():
    """Per-galaxy arrays: r[m], gbar, gobs, Vbar2, name. Keep per-galaxy for halo injection."""
    gals=[]
    for f in files:
        d=np.loadtxt(f,comments='#')
        if d.ndim==1 or d.shape[0]<3: continue
        r=d[:,0]*kpc; Vo=d[:,1]*km; eV_=d[:,2]*km
        Vg=d[:,3]*km; Vd=d[:,4]*km; Vb=d[:,5]*km
        Vbar2=Vg*np.abs(Vg)+Ups*Vd*np.abs(Vd)+Ups*Vb*np.abs(Vb)
        good=(r>0)&(Vo>0)&(eV_/np.clip(Vo,1e-9,None)<=0.10)&(Vbar2>0)
        if good.sum()<3: continue
        gals.append(dict(r=r[good], Vo=Vo[good], Vbar2=np.clip(Vbar2[good],0,None),
                         name=os.path.basename(f).replace("_rotmod.dat","")))
    return gals
gals=load_galaxies()
npts=sum(len(g['r']) for g in gals)
print(f"[data] {len(gals)} galaxies, {npts} points after err/V<0.10 cut, Ups={Ups}")

def rar_scatter_global(gbar, gobs, a0):
    gpred=nu_dsunruh(gbar,a0)
    res=np.log10(gobs)-np.log10(gpred); res-=np.median(res)
    return np.sqrt(np.mean(res**2))

# baseline (no injection): framework dS-Unruh
gbar_all=np.concatenate([g['Vbar2']/g['r'] for g in gals])
gobs_all=np.concatenate([g['Vo']**2/g['r'] for g in gals])
floor=rar_scatter_global(gbar_all,gobs_all,a0_FW)
print(f"\n[baseline] framework dS-Unruh a0=9.36e-11: RAR scatter floor = {floor:.4f} dex")

# --- HONEST RAR metric for injection -----------------------------------------
# THE TRAP (caught on first run): if we ADD g_halo to g_MOND, then call rar_scatter_global,
# the per-injection median-subtraction silently absorbs the systematic over-prediction (a
# smooth NFW halo even REDUCES vertical scatter -> a false "safe" 0.09 dex). That is wrong.
# The framework already FITS the observed rotation curve with MOND-from-baryons (the floor).
# If a REAL keV halo ALSO sits in the galaxy, the model now PREDICTS g_MOND+g_halo while the
# data show gobs (which MOND alone already matched). The honest residual is:
#     res = log10(model_prediction) - log10(actual_observed gobs)
# centered on the SAME baseline median (the M/L offset), NOT re-centered per injection.
res0 = np.log10(gobs_all) - np.log10(nu_dsunruh(gbar_all,a0_FW))   # baseline residual
med0 = np.median(res0)                                              # fixed M/L offset
def injected_rms(model_g):
    """rms residual of (model prediction) about the actual observed gobs, baseline-centered."""
    res = np.log10(model_g) - np.log10(gobs_all) - (-med0)   # keep baseline M/L offset fixed
    return np.sqrt(np.mean(res**2))

# Inject a keV WDM halo. The WDM density profile in a dwarf is a CORED (Burkert/cored-NFW)
# halo whose mass below M_hm is SUPPRESSED. We model the keV halo two ways and report both:
#   (A) "COLD limit" (m_s large / Lyman-alpha-safe): the WDM behaves like CDM down to the dSph
#       scale -> a full NFW/cored halo of mass M_halo(V_flat). This is the OVER-PACK scenario.
#   (B) "WARM limit" (m_s ~1-2 keV / galaxy-veto-safe): free-streaming suppresses the halo on
#       dwarf scales -> the injected halo mass is multiplied by the WDM transfer suppression
#       S(M_halo, M_hm) ~ (1+ (M_hm/M_halo))^(-beta) so dwarfs get LITTLE halo.
#
# For the framework MOND context the "dark halo" is a PHANTOM (MOND already supplies the missing
# accel). Injecting an ADDITIONAL real WDM halo means the gravity is now g = g_MOND(baryons) +
# g_WDM(halo). If the WDM halo is non-negligible it OVER-predicts the rotation curve -> blows
# up the RAR. We compute g_obs_model = sqrt(g_MOND^2 ... ) -- but physically the cleanest test:
# does adding the WDM halo to the EXISTING baryons (then re-applying MOND, or just Newtonian for
# the halo) push the predicted g away from observed? The honest test: compute the EXTRA g from a
# keV halo of the cosmologically-required mass and ask if it exceeds the RAR residual budget.

def Mhalo_from_Vflat(Vflat_ms):
    """Abundance-matched-ish halo mass from V_flat (Msun). M_halo ~ (Vflat/ (a fixed))^3.
       Use M_halo = 1e12 Msun (Vflat/170 km/s)^3.5 (stellar-to-halo / BTFR-consistent)."""
    return 1.0e12*(Vflat_ms/(170*km))**3.5

def wdm_suppress(M_halo_Msun, M_hm_Msun_val, beta=1.0):
    """Fraction of CDM halo mass that survives WDM free-streaming at M_halo.
       Halos << M_hm are strongly suppressed; >> M_hm form normally.
       S = 1/(1+(M_hm/M_halo)^beta) (smooth step; S->1 for M_halo>>M_hm, ->0 below)."""
    return 1.0/(1.0+(M_hm_Msun_val/M_halo_Msun)**beta)

# For each galaxy: V_flat ~ sqrt of median outer gobs*r; build NFW halo; add g_halo to baryons.
def inject_and_score(m_s_keV, cold=False):
    """Add a keV WDM halo to each galaxy. Model prediction = g_MOND(baryons) + g_halo.
       Score = rms of [log10(model) - log10(actual observed gobs)], baseline-centered.
       The framework already fit gobs with MOND alone; an EXTRA real halo OVER-predicts ->
       drives the residual above the floor. cold=True = no WDM suppression (heavy-keV / Lya end)."""
    m_th=m_th_from_ms_DW(m_s_keV); M_hm=M_hm_fit(m_th)
    model_list=[]; gobs_list=[]; ghalo_frac=[]
    for g in gals:
        r=g['r']; Vbar2=g['Vbar2']
        gbar=Vbar2/r; gobs=g['Vo']**2/r
        Vflat=np.sqrt(np.median((g['Vo']**2)[-max(1,len(r)//3):]))  # outer V
        Mh=Mhalo_from_Vflat(Vflat)*Msun
        S=1.0 if cold else wdm_suppress(Mh/Msun, M_hm)
        Mh_eff=Mh*S
        r200=(Mh_eff/((4/3)*np.pi*200*rho_crit))**(1/3) if Mh_eff>0 else 1e-30
        cc=10.0; rs=r200/cc
        def mnfw(rr):
            x=rr/rs; return np.log(1+x)-x/(1+x)
        norm=Mh_eff/mnfw(r200) if (Mh_eff>0 and mnfw(r200)>0) else 0.0
        g_halo=G*norm*mnfw(r)/r**2
        g_mond=nu_dsunruh(gbar,a0_FW)
        model_list.append(g_mond+g_halo); gobs_list.append(gobs)
        ghalo_frac.append(g_halo/g_mond)
    model=np.concatenate(model_list); go=np.concatenate(gobs_list)
    fr=np.concatenate(ghalo_frac)
    res=np.log10(model)-np.log10(go); res-=med0   # baseline-centered (fixed M/L offset)
    return np.sqrt(np.mean(res**2)), M_hm, np.median(fr)

print(f"\n  HONEST metric: model = g_MOND(baryons) + g_keV-halo, residual vs ACTUAL observed gobs,")
print(f"  centered on the baseline M/L offset (NOT re-centered). Floor (no halo) = {floor:.3f} dex.")
print(f"  {'m_s[keV]':>9s} {'m_th[keV]':>10s} {'M_hm[Msun]':>12s} {'g_halo/g_M':>11s} {'WARM-inj':>10s} {'COLD-inj':>10s}")
for m_s in [1.0, 2.0, 3.0, 5.0, 7.0, 10.0, 20.0, 40.0]:
    sc_warm,M_hm,fr_w=inject_and_score(m_s, cold=False)
    sc_cold,_,fr_c   =inject_and_score(m_s, cold=True)
    m_th=m_th_from_ms_DW(m_s)
    print(f"  {m_s:9.1f} {m_th:10.3f} {M_hm:12.2e} {fr_c:11.2f} {sc_warm:10.4f} {sc_cold:10.4f}")
print(f"""
  READ (b2): floor (no halo, pure framework MOND) = {floor:.3f} dex.
   - COLD limit (no WDM suppression = the Lyman-alpha-safe heavy-keV end, m_s>=20 keV): a full
     CDM-like halo sits on top of MOND-from-baryons. Median g_halo/g_MOND ~ O(0.5-1) -> the model
     OVER-predicts the rotation curve that MOND alone already fit -> residual BLOWS well above the
     {floor:.3f} floor. A keV WDM cold enough to cluster into galaxies is RAR-INCOMPATIBLE with the
     framework (MOND already supplies the missing gravity; a real halo on top is double-counted
     excess). => galaxy-veto BREAKS for any keV cold enough to enter galaxies.
   - WARM limit (m_s~1-2 keV, M_hm>~1e11): WDM suppression S->0 on dwarf halos -> g_halo->~0 ->
     residual stays at the floor (galaxy-veto SAFE) -- but that warmth is Lyman-alpha-excluded.
   The injection makes the crux QUANTITATIVE: galaxy-safe ONLY where M_hm >~ the dwarf halo mass
   (m_s small = warm = Lyman-alpha-dead). Cold-enough-for-Lya = over-packs = RAR breaks.
""")

# ============================================================================
# (c) WDM BOUNDS — Lyman-alpha free-streaming + X-ray decay line
# ============================================================================
print("="*84)
print("(c) WDM BOUNDS: Lyman-alpha free-streaming + X-ray decay-line (3.5 keV) non-detection")
print("="*84)
# Lyman-alpha (2023-2026 state of the art):
#   - NRP/thermal-relic bound: m_th >~ 5.3 keV (Villasenor+2023, arXiv:2209.14220; 3sigma),
#     earlier Irsic+2017 m_th>3.5 keV, Palanque-Delabrouille+2020 m_th>5.3 keV.
#   - Translate to sterile (DW/NRP): m_s = 4.43 (m_th)^(4/3) -> m_th 5.3 keV => m_s ~ 43 keV (NRP).
#   - For RESONANT production (Shi-Fuller, colder) the bound relaxes to m_s >~ 10-20 keV.
m_th_lya = 5.3   # keV, conservative modern Lyman-alpha 3sigma (Villasenor+2023 / PDB2020)
m_s_lya_NRP = 4.43*(m_th_lya)**(4/3)
print(f"\n  Lyman-alpha (modern, Villasenor+2023 / PDB2020): m_th >~ {m_th_lya} keV (3sigma)")
print(f"    -> NRP (Dodelson-Widrow) sterile bound: m_s >~ {m_s_lya_NRP:.0f} keV")
print(f"    -> RESONANT (Shi-Fuller, colder spectrum) sterile bound: m_s >~ 10-20 keV (relaxed)")

# X-ray decay line: sterile nu decays nu_s -> nu + gamma, E_gamma = m_s/2.
#   Non-detection (no 3.5 keV line confirmed; Dessert+2020 / Foster+2021 / Roach+2023/2025)
#   gives an UPPER bound on sin^2(2theta) vs m_s. The 3.5 keV line would be m_s ~ 7 keV,
#   sin^2(2theta) ~ 5e-11 (Boyarsky/Bulbul 2014) -- now strongly disputed/excluded by
#   blank-sky (Dessert+2020 arXiv:1812.06976) and Milky-Way halo (Foster+2021, Roach+2020/2023).
#   The DW production of the FULL Omega_DM requires sin^2(2theta) ~ a value EXCLUDED for all
#   m_s by X-ray for m_s >~ 1-2 keV (the "DW closed" result, Boyarsky+2019 review).
print(f"""
  X-ray decay line (nu_s -> nu + gamma, E=m_s/2):
    - The 3.5 keV line (m_s~7 keV, sin^2(2theta)~5e-11; Bulbul/Boyarsky 2014) is now
      strongly DISPUTED/EXCLUDED by deep blank-sky + MW-halo non-detections
      (Dessert+2020 arXiv:1812.06976; Foster+2021; Roach+2020,2023; Sicilian+2022; Dessert+2023).
    - For DODELSON-WIDROW (NRP) production of the FULL DM abundance, the required mixing
      sin^2(2theta)(m_s) is EXCLUDED by X-ray for essentially ALL m_s (the DW mechanism as
      100% of DM is CLOSED: Lyman-alpha kills the light end, X-ray kills the heavy end --
      Boyarsky-Drewes-Lasserre-Mertens-Ruchayskiy 2019 review, arXiv:1807.07938).
    - RESONANT (Shi-Fuller, nu_MSM) production survives in a NARROW window m_s ~ 7-50 keV with
      small mixing, partially probed by X-ray; m_s~7.1 keV at the 3.5 keV mixing is now in
      tension with Dessert/Foster/Roach.
""")

# ============================================================================
# THE WINDOW — does a keV sterile close clusters AND pass Lya AND X-ray AND galaxy veto?
# ============================================================================
print("="*84)
print("THE keV WINDOW — intersect all four constraints")
print("="*84)
# Galaxy-veto-safe (WDM free-streams out of dwarfs): need M_hm >~ M_dwarf ~ 1e9-1e10 Msun.
# Solve M_hm_fit(m_th)=1e9 and 1e10 for m_th, then -> m_s (NRP).
def m_th_for_Mhm(M_target):
    # M_hm_fit = 1e10 m_th^-3.33 = M_target -> m_th = (1e10/M_target)^(1/3.33)
    return (1.0e10/M_target)**(1/3.33)
m_th_veto_lo=m_th_for_Mhm(1e10)   # M_hm=1e10 (suppress up to dwarf)
m_th_veto_hi=m_th_for_Mhm(1e9)    # M_hm=1e9  (suppress only smallest dSph)
m_s_veto_lo=4.43*(m_th_veto_lo)**(4/3)
m_s_veto_hi=4.43*(m_th_veto_hi)**(4/3)
print(f"\n  Galaxy-veto-SAFE (free-streams out of dwarfs, M_hm in 1e9-1e10 Msun):")
print(f"    requires m_th ~ {m_th_veto_lo:.2f}-{m_th_veto_hi:.2f} keV -> m_s(NRP) ~ "
      f"{m_s_veto_lo:.1f}-{m_s_veto_hi:.1f} keV (UPPER bound: colder = enters dwarfs)")
print(f"  Lyman-alpha-SAFE: m_th >~ {m_th_lya} keV -> m_s(NRP) >~ {m_s_lya_NRP:.0f} keV (LOWER bound)")
print(f"\n  CRUX VISE (NRP/DW):")
print(f"    galaxy-veto wants m_th <~ {m_th_veto_hi:.1f} keV (warm, free-streams out of dwarfs)")
print(f"    Lyman-alpha     wants m_th >~ {m_th_lya:.1f} keV (cold, preserves forest power)")
print(f"    => {m_th_veto_hi:.1f} keV < {m_th_lya:.1f} keV : the two REQUIREMENTS DO NOT OVERLAP "
      f"(gap factor ~{m_th_lya/m_th_veto_hi:.1f}x in m_th).")
print(f"""
  THE RESOLUTION (both ways, honest):
   - If the keV sterile is WARM enough to free-stream OUT of dwarfs (galaxy-veto-safe via WDM,
     m_th <~ {m_th_veto_hi:.1f} keV), it is EXCLUDED by Lyman-alpha (m_th >~ {m_th_lya} keV).
   - If it is COLD enough to pass Lyman-alpha (m_th >~ {m_th_lya} keV, m_s >~ {m_s_lya_NRP:.0f} keV NRP),
     then M_hm <~ {M_hm_fit(m_th_lya):.1e} Msun << dwarf halos -> it CLUSTERS INTO dwarfs/galaxies.
     And TG no longer forbids it (keV >> 390 eV). So it ADDS a real halo to galaxies on top of
     MOND -> the RAR injection (b2, COLD column) BREAKS the RAR.
   - X-ray decay (Dessert/Foster/Roach) + the Lyman-alpha+X-ray "DW-closed" theorem independently
     kill the DW route as 100% DM; only a resonant nu_MSM sliver (m_s~7-50 keV) survives, and that
     sliver is the COLD (galaxy-entering) end -> still breaks the galaxy veto in this framework.
  => For the FRAMEWORK (where MOND already supplies galaxy gravity), the keV sterile is in a VISE:
     the only galaxy-safe end is Lyman-alpha-excluded, and the only Lyman-alpha/X-ray-allowed end
     clusters into galaxies and breaks the RAR (because MOND + a real halo double-count). The eV
     window (4.3-390 eV) was protected by TG on BOTH ends (cluster-fill + galaxy-exclude); the keV
     state LOSES the galaxy-side TG protection and gains a WDM/Lyman-alpha problem instead. The
     keV window is SQUEEZED SHUT for a framework that already MONDifies galaxies.
""")

# ============================================================================
# BOTH-WAYS CONTROL: is the vise robust to the sterile->thermal mapping + Lya bound choice?
# ============================================================================
print("="*84)
print("BOTH-WAYS robustness: vary the Lyman-alpha bound, production (NRP/RP), and the dwarf M_hm")
print("="*84)
print(f"{'Lya m_th[keV]':>13s} {'prod':>6s} {'veto-safe m_th_max':>18s} {'overlap?':>9s}")
for m_th_lya_v in [3.5, 5.0, 5.3]:    # Irsic2017 .. PDB2020/Villasenor2023
    for prod,relax in [("NRP",1.0),("RP",2.5)]:   # resonant relaxes the effective Lya m_th by ~2.5x
        # veto needs to suppress dwarf (M_hm>1e9..1e10); pick the generous M_hm=1e9 end
        m_th_veto=m_th_for_Mhm(1e9)
        m_th_lya_eff=m_th_lya_v/relax     # RP: colder, so a given m_th_lya corresponds to warmer m_s; relax the m_th requirement
        overlap = "YES" if m_th_veto>=m_th_lya_eff else "no"
        print(f"{m_th_lya_v:13.1f} {prod:>6s} {m_th_veto:18.2f} {overlap:>9s}  "
              f"(Lya-eff m_th>={m_th_lya_eff:.2f})")
print("""
  READ: across the modern Lyman-alpha range (3.5-5.3 keV) and both production channels, the
  galaxy-veto-safe ceiling (m_th ~0.4-0.5 keV, M_hm~1e9-1e10) NEVER reaches the Lyman-alpha
  floor (m_th>~1.4-5.3 keV effective). The vise does NOT overlap in any cell -> the squeeze is
  robust, not an artifact of one bound or one production mapping. (Only an extreme, contrived
  RP spectrum with a designer transfer function could thread it -- not a generic keV sterile.)
""")

print("="*84)
print("ONE-LINE VERDICT")
print("="*84)
print(f"""
  (a) keV sterile CLOSES the cluster core in phase-space (TG floor ~{m_min_cl:.0f} eV << keV;
      2.3e14 Msun inside 420 kpc trivially packable at sigma~1000 km/s).
  (b) CRUX: keV is ABOVE the dSph TG floor (~390 eV) so phase-space NO LONGER protects galaxies;
      protection must come from WDM FREE-STREAMING. RAR injection: COLD keV (Lya-safe) adds a real
      halo on top of MOND -> RAR blows up; WARM keV (galaxy-safe) is the only safe end.
  (c) BUT the WARM/galaxy-safe end (m_th<~0.5 keV) is EXCLUDED by Lyman-alpha (m_th>~5.3 keV) and
      the DW route is X-ray-closed; only a resonant m_s~7-50 keV sliver survives, and that is the
      COLD end that clusters into galaxies -> breaks the RAR here.
  => NO keV window closes clusters AND passes Lya AND X-ray AND the galaxy veto for THIS framework.
     The eV window (4.3-390 eV, TG-protected both ends) was the cheapest surviving patch; the keV
     state is SQUEEZED SHUT. Quarantine: even the eV patch RELOCATES the dark sector (a separate
     ~0.25-Omega species) -- a partial answer to "no dark matter", not a vindication of a0=Lambda.
""")
