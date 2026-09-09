#!/usr/bin/env python3
"""
L45 -- the last door on the cluster problem: can UNDETECTED BARYONS at pair separation supply what the
       binary-galaxy kinematics require?
=======================================================================================================
L41 assembled the specification the cluster source must meet and proved it NOT self-consistent: at the
galaxy pairs' own 132 kpc twelve clusters measure M_dark/M_bar = 9.20 +/- 1.30 while the pairs require
30.9 +/- 1.5 (a factor 3.4 at 11 sigma), and a 35-member scan over the most general host-blind profile
rule closed with three pairwise-disjoint gate windows and an EMPTY intersection.

L41 left exactly ONE door open and explicitly declined to settle it (its check B5): the pairs' baryons
could be UNDERCOUNTED.  The framework's own galaxy-scale gate does not close it -- even 5x the K-band
mass spread uniformly inside 132 kpc puts only 0.0017 M_b inside 10 kpc against a tolerance of 0.408 --
so L41 wrote that the door "is closed, if at all, by circumgalactic-medium mass budgets, which is a
literature question this lane does not settle and does not claim to."

THIS LANE SETTLES IT, against the measured circumgalactic medium.

WHAT A POSITIVE RESULT WOULD MEAN, stated before the computation.  If undetected baryons CAN supply the
pair requirement, that is NOT a win for this framework.  It is a free function of host mass and
environment of exactly the kind LambdaCDM's galaxy-formation sector already contains, and L41 said so:
a completion adopting it inherits that sector wholesale.  The result is reported as a cost either way.
Nothing here claims data favour this framework over LambdaCDM; they do not, and L41's own E1 showed
LambdaCDM's abundance-matching relation predicts the pair ratio to 0.6 sigma with nothing fitted.

STRUCTURE
  PART A  CONTROLS.  Reproduce, from their own data and with this lane's code:
          A1 L21's pair ratio 30.9 +/- 1.6;  A2 L41's fixed-radius cluster ratio 9.20 +/- 1.30;
          A3 a published cosmic baryon fraction;  A4 a published galaxy-scale baryon deficit;
          A5 the pair forward model (L21's own framework amplitudes and implied mass factors).
  PART B  THE REQUIREMENT, recomputed three ways -- Newtonian, the framework's own carried kernel, and
          L41's cosmic-share reading -- as a multiple of the K-band stellar mass and as an absolute mass,
          with the profile freedom priced.
  PART C  THE THREE-WAY CONFRONTATION with what is actually observed:
          (a) total baryon budget            C1
          (b) observed radial distribution   C2, C6, C8
          (c) non-detection constraints      C3 (dispersion measure), C4 (X-ray), C5 (absorption), C7 (global)
  PART D  THE CONSEQUENCES the requirement drags with it -- clusters D1, rotation curves D2, lensing
          shape D3 -- and the joint test D4: can ONE distribution serve all four?
  PART E  THE VERDICT, E1.

Every check is written so that PASS is the outcome FAVOURABLE to the escape.  A FAIL marks a requirement
the escape does not meet.  Both a0 footings throughout (9.3619e-11 canonical, 1.1279e-10 alt).

LITERATURE USED (searched and read for this lane, not recalled):
  Planck 2018 VI (Aghanim+ 2020)                Omega_b h^2 = 0.02237, Omega_m h^2 = 0.1430, h = 0.6736
  Werk+ 2014, ApJ 792, 8 (COS-Halos)            M_cool > 6.5e10 Msun within R_vir; mean log N_H = 19.6;
                                                n_H = 10^(-4.2 +/- 0.25) (R/R_vir)^(-0.8 +/- 0.3) cm^-3
  Tumlinson, Peeples & Werk 2017, ARA&A 55, 389 the CGM review these measurements sit in (context only)
  Bregman+ 2018, ApJ 862, 3                     M_hot(<50 kpc) ~ 5e9 Msun for massive spirals, rho ~ r^-1.5;
                                                ~half of the baryons still missing when extrapolated to R200
  Tisserand+ 2007, A&A 469, 387 (EROS-2)        MACHOs of 0.6e-7 to 15 Msun are < 8% of a standard halo
  Bregman+ 2022, ApJ 928, 14 (SZ)               M_gas = 9.8 +/- 2.8 e10 Msun within 250 kpc of L* galaxies,
                                                ~30% of the cosmic share; ~1.4e11 Msun still missing
  Salem+ 2015, ApJ 815, 77 (LMC ram pressure)   n = 1.1 (+0.44/-0.45) e-4 cm^-3 at r = 48.2 +/- 5 kpc (MW)
  Prochaska+ 2019, Science 366, 231 (FRB181112) DM_FG ~ 50-120 pc cm^-3 at b = 29 kpc from a
                                                log M* = 10.69 galaxy; n_e < 2e-3 cm^-3 for hot halo gas;
                                                f_V < 1e-4 for cool clumps embedded in it
  Prochaska & Zheng 2019, MNRAS 485, 648        DM(MW halo, to 200 kpc) ~ 50-80 pc cm^-3
  Khrykin+ 2024, ApJ 973, 151 (FLIMFLAM DR1)    f_igm = 0.59 (+0.11/-0.10); f_gas(10^10-10^13) = 0.55 (+0.26/-0.29)
  Connor+ 2025, Nat. Astron. (DSA-110)          f_IGM = 0.76 (+0.10/-0.11); Omega_b h70 = 0.051 +/- 0.006
  Deason+ 2021, MNRAS 501, 5964                 M_MW(<100 kpc) = 6.07 +/- 0.29(stat) +/- 1.21(sys) e11 Msun
  Fukugita & Peebles 2004 / Madau & Dickinson 2014   Omega_*/Omega_b = 0.05 +/- 0.01 today
"""
import numpy as np, math, json, os, sys, glob
from scipy.spatial import cKDTree
from astropy.io import fits

FAILS = []
def check(name, ok, detail=""):
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"   ({detail})" if detail else ""), flush=True)
    if not ok: FAILS.append(name)
def P(s=""): print(s, flush=True)
def info(s): print("  " + s, flush=True)

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
DATA = os.path.join(REPO, "real_research", "data")
XDIR = os.path.join(DATA, "xcop")

G = 6.674e-11; MSUN = 1.989e30; kpc = 3.0857e19; Mpc = 3.0857e22
M_H = 1.673e-27                                    # kg, hydrogen mass
CM = 1e-2                                          # m per cm
A0 = {"canonical": 9.3619e-11, "alt": 1.1279e-10}
E_N = {"canonical": 0.01240, "alt": 0.01027}       # 2M++ computed external field, h81_h82
S_SAT, D_SAT = 2.540, 0.6476                       # the carried kernel's saturation, THE_ACTION 2026-09-05 sec.3
F_COSMIC = 5.43                                    # Omega_dm/Omega_b
UPS_K = 0.6; MK_SUN = 3.28; H0_KMS = 67.4; h_little = 0.674
RHO_C_MSUN_MPC3 = 3*(H0_KMS*1e3/Mpc)**2/(8*math.pi*G)/MSUN*Mpc**3

# ---- Planck 2018 VI, TT,TE,EE+lowE+lensing ----
OMBH2, OMMH2, HLIT = 0.02237, 0.1430, 0.6736
OM_B = OMBH2/HLIT**2; OM_M = OMMH2/HLIT**2
F_BAR_COSMIC = OM_B/OM_M

# ---- literature values, as data, each with its source in the docstring ----
LIT = dict(
    werk_Mcool=6.5e10, werk_logNH=19.6, werk_nH0=10**-4.2, werk_nH_slope=-0.8, werk_Rvir=300.0,
    bregman18_M50=5.0e9, bregman18_rho_slope=-1.5,
    bregman22_M250=9.8e10, bregman22_eM250=2.8e10, bregman22_R=250.0, bregman22_frac=0.30,
    bregman22_missing=1.4e11,
    salem_n=1.1e-4, salem_en=0.44e-4, salem_r=48.2,
    frb181112_DMlo=50.0, frb181112_DMhi=120.0, frb181112_b=29.0, frb181112_logMstar=10.69,
    frb181112_ne_max=2.0e-3,
    mwhalo_DMlo=50.0, mwhalo_DMhi=80.0, mwhalo_R=200.0,
    flimflam_figm=0.59, flimflam_efigm=0.105,
    connor_figm=0.76, connor_efigm=0.105, connor_ombh70=0.051, connor_eombh70=0.006,
    deason_M100=6.07e11, deason_eM100=math.hypot(0.29, 1.21)*1e11,
    omstar_over_omb=0.05, e_omstar_over_omb=0.01,
    L24_fw_shear_slope=-0.309,           # L24 C11 / L41 P1: the framework's own projected shear log-slope
)

P("=" * 122)
P("L45 -- undetected baryons at pair separation: L41's last open door, settled against the measured CGM")
P("=" * 122)
P("  data used by this lane (paths relative to the repository root):")
P("    pairs    : real_research/data/2mrs_catalog.csv                       (rebuilt, not reused)")
P("    clusters : qwen_claude_field_theory/closure_2026/cluster_measurement_audit_2026/results.json")
P("    clusters : real_research/data/xcop/<name>/*.fits                     (independent read)")
P("    galaxies : real_research/data/sparc_data/*_rotmod.dat                (the RAR gate)")
P("    literature: the eleven references listed in this file's docstring, searched and read for this lane")

# ==========================================================================================================
# the carried kernel and the two-body machinery (reused from L21, re-stated here so this file stands alone)
# ==========================================================================================================
def Delta(s):
    s = np.asarray(s, float); sc = np.clip(s, 1e-300, S_SAT)
    d = np.where(s > 0, sc/np.expm1(np.sqrt(sc)), 0.0)
    return np.where(s > S_SAT, D_SAT, d)
def dDelta(s):
    s = np.asarray(s, float); u = np.sqrt(np.clip(s, 1e-300, S_SAT)); em = np.expm1(u)
    d = (2.0*em - u*np.exp(u))/(2.0*em*em)
    return np.where(s > S_SAT, 0.0, d)
def g_kernel(gb, a0): return gb + a0*Delta(np.asarray(gb, float)/a0)

def Gamma(M1, M2):
    M1 = np.asarray(M1, float); M2 = np.asarray(M2, float)
    return (2.0/3.0)*((M1 + M2)**1.5 - M1**1.5 - M2**1.5)
def M_eff(M1, M2):
    M1 = np.asarray(M1, float); M2 = np.asarray(M2, float)
    mu = M1*M2/(M1 + M2)
    return (Gamma(M1, M2)/mu)**2
def a_rel_fw_iso(M1, M2, r_m, a0):
    Mt = (np.asarray(M1, float) + np.asarray(M2, float))*MSUN
    Me = M_eff(M1, M2)*MSUN
    return G*Mt/r_m**2 + a0*Delta(G*Me/(a0*r_m**2))
def nu_efe(eN):
    par = 1.0 + float(dDelta(np.array([eN]))[0])
    perp = 1.0 + float(Delta(np.array([eN]))[0])/eN
    return (par + 2*perp)/3.0
def a_rel_fw(M1, M2, r_m, a0, eN):
    Mt = (np.asarray(M1, float) + np.asarray(M2, float))*MSUN
    return np.minimum(a_rel_fw_iso(M1, M2, r_m, a0), nu_efe(eN)*G*Mt/r_m**2)
def a_rel_newton(M1, M2, r_m):
    return G*(np.asarray(M1, float) + np.asarray(M2, float))*MSUN/r_m**2

def a_rel_law(law, M1, M2, r_m, a0, eN):
    if law == "fw_iso": return a_rel_fw_iso(M1, M2, r_m, a0)
    if law == "fw":     return a_rel_fw(M1, M2, r_m, a0, eN)
    if law == "newton": return a_rel_newton(M1, M2, r_m)
    raise ValueError(law)

def sigma_pred(law, M1, M2, rp_kpc, a0, eN, nmc=400, seed=11):
    """Projected-separation forward model.  Only r_p is observed, so the 3-D separation is drawn from a
       log-uniform prior weighted by the random-orientation kernel p(r_p|r) = r_p/(r sqrt(r^2 - r_p^2)),
       and <dv_los^2> = v_rel^2/3 for a circular relative orbit.  Identical in construction to L21's."""
    g = np.random.default_rng(seed)
    M1 = np.atleast_1d(np.asarray(M1, float)); M2 = np.atleast_1d(np.asarray(M2, float))
    rp = np.atleast_1d(np.asarray(rp_kpc, float))
    u = g.random((len(rp), nmc))
    r = rp[:, None]*np.exp(u*math.log(20.0))*1.0001
    w = 1.0/np.sqrt(np.maximum((r/rp[:, None])**2 - 1.0, 1e-6)); w /= w.sum(axis=1, keepdims=True)
    v2 = a_rel_law(law, M1[:, None], M2[:, None], r*kpc, a0, eN)*(r*kpc)
    return np.sqrt(np.sum(w*v2, axis=1)/3.0)/1e3

# ==========================================================================================================
P("\n" + "=" * 122)
P("PART A -- CONTROLS.  Every number this lane leans on, recomputed from its own data before it is used.")
P("=" * 122)

# ---- rebuild the 2MRS pair sample (L41's K2 / L21's C4 machinery) ---------------------------------------
def unitvec(ra, de):
    ra = np.radians(ra); de = np.radians(de)
    return np.c_[np.cos(de)*np.cos(ra), np.cos(de)*np.sin(ra), np.sin(de)]
def ang_sep_deg(u, v): return np.degrees(2*np.arcsin(np.clip(np.linalg.norm(u - v, axis=-1)/2, 0, 1)))
def cmb_frame(ra, de, vhel):
    ra_r, de_r = np.radians(ra), np.radians(de)
    ra_gp, de_gp, l_ncp = math.radians(192.85948), math.radians(27.12825), math.radians(122.93192)
    sb = np.sin(de_r)*math.sin(de_gp) + np.cos(de_r)*math.cos(de_gp)*np.cos(ra_r - ra_gp)
    b = np.arcsin(np.clip(sb, -1, 1))
    y = np.cos(de_r)*np.sin(ra_r - ra_gp)
    x = np.sin(de_r)*math.cos(de_gp) - np.cos(de_r)*math.sin(de_gp)*np.cos(ra_r - ra_gp)
    l = l_ncp - np.arctan2(y, x)
    la, ba, amp = math.radians(264.021), math.radians(48.253), 369.82
    return vhel + amp*(np.sin(b)*math.sin(ba) + np.cos(b)*math.cos(ba)*np.cos(l - la))

CZ_LO, CZ_HI, RP_MAX, DV_MAX, DV_ISO, V_ERR, F_REL = 3000., 12000., 1000., 2000., 1000., 40., 5.0
mr = np.genfromtxt(os.path.join(DATA, "2mrs_catalog.csv"), delimiter=",", names=True)
mok = np.isfinite(mr["cz"]) & (mr["cz"] > 0)
m_ra, m_de, m_K = mr["RAJ2000"][mok], mr["DEJ2000"][mok], mr["Ktmag"][mok]
MX = unitvec(m_ra, m_de); MT = cKDTree(MX); cz = cmb_frame(m_ra, m_de, mr["cz"][mok])
ang_max = math.degrees(RP_MAX/1000.0/(CZ_LO/H0_KMS))
cand = MT.query_pairs(2*math.sin(math.radians(ang_max)/2), output_type="ndarray")
ii, jj = cand[:, 0], cand[:, 1]
czm = (cz[ii] + cz[jj])/2; Dm = czm/H0_KMS
rp = np.radians(ang_sep_deg(MX[ii], MX[jj]))*Dm*1000.0
dv = cz[ii] - cz[jj]
sel = (np.abs(dv) < DV_MAX) & (czm > CZ_LO) & (czm < CZ_HI) & (rp < RP_MAX) & (rp > 10.0)
ii, jj, rp, dv, czm, Dm = ii[sel], jj[sel], rp[sel], dv[sel], czm[sel], Dm[sel]
LK = lambda K, D: 10**(0.4*(MK_SUN - (K - 5*np.log10(D*1e6) + 5)))
L1_, L2_ = LK(m_K[ii], Dm), LK(m_K[jj], Dm)
rok = (np.maximum(L1_, L2_)/np.minimum(L1_, L2_)) < 6.0
ii, jj, rp, dv, czm, Dm, L1_, L2_ = (a[rok] for a in (ii, jj, rp, dv, czm, Dm, L1_, L2_))
mid = MX[ii] + MX[jj]; mid /= np.linalg.norm(mid, axis=1)[:, None]
dch, idx = MT.query(mid, k=80)
dist = np.degrees(2*np.arcsin(np.clip(dch/2, 0, 1)))*np.radians(1.0)*Dm[:, None]*1000.0
bad = (idx == ii[:, None]) | (idx == jj[:, None]) | (np.abs(cz[idx] - czm[:, None]) >= DV_ISO)
d3 = np.where(bad, np.inf, dist).min(axis=1)
keep = d3 > F_REL*rp
S = dict(rp=rp[keep], dv=dv[keep], M1=UPS_K*L1_[keep], M2=UPS_K*L2_[keep])
NPAIR = len(S["rp"])

def ml_amp(dv, shape, dvmax=DV_MAX, verr=V_ERR):
    dv = np.asarray(dv, float); s = np.asarray(shape, float)
    def nll(lA, lf):
        A = math.exp(lA); f = 1/(1 + math.exp(-lf)); sg = np.sqrt((A*s)**2 + verr**2)
        p = f*np.exp(-0.5*(dv/sg)**2)/(math.sqrt(2*math.pi)*sg) + (1 - f)/(2*dvmax)
        return -np.sum(np.log(np.maximum(p, 1e-300)))
    best = (1e30, 0., 0.)
    for lA in np.linspace(math.log(0.10), math.log(12.0), 110):
        for lf in np.linspace(-4, 4, 41):
            v = nll(lA, lf)
            if v < best[0]: best = (v, lA, lf)
    lA0, lf0 = best[1], best[2]
    for _ in range(3):
        lf0 = min(np.linspace(lf0 - 1.0, lf0 + 1.0, 81), key=lambda x: nll(lA0, x))
        lA0 = min(np.linspace(lA0 - 0.15, lA0 + 0.15, 81), key=lambda x: nll(x, lf0))
    fine = np.linspace(lA0 - 0.35, lA0 + 0.35, 161)
    prof = np.array([min(nll(lA, lf) for lf in np.linspace(lf0 - 0.8, lf0 + 0.8, 21)) for lA in fine])
    prof -= prof.min(); lA0 = fine[int(np.argmin(prof))]; hi = fine[prof < 0.5]
    err = (hi.max() - hi.min())/2 if len(hi) > 1 else float(np.diff(fine).mean())
    return math.exp(lA0), math.exp(lA0)*err

sh_N = sigma_pred("newton", S["M1"], S["M2"], S["rp"], A0["canonical"], E_N["canonical"])
A_N, eA_N = ml_amp(S["dv"], sh_N)
RATIO_PAIR = A_N**2 - 1.0; E_RATIO_PAIR = 2*A_N*eA_N
MBAR_PAIR = float(np.median(S["M1"] + S["M2"])); R_PAIR = float(np.median(S["rp"]))
MSTAR_GAL = MBAR_PAIR/2.0
info(f"A1: pairs rebuilt: N = {NPAIR}, median r_p = {R_PAIR:.0f} kpc, median M_b(pair) = {MBAR_PAIR:.2e} Msun "
     f"(= {MSTAR_GAL:.2e} per galaxy, Upsilon_K = {UPS_K}, no gas)")
info(f"    Newtonian-on-baryons amplitude A = {A_N:.3f} +/- {eA_N:.3f}  =>  M_dark/M_bar within r_p = "
     f"A^2 - 1 = {RATIO_PAIR:.1f} +/- {E_RATIO_PAIR:.1f}")
check("A1 [CONTROL] an independent rebuild of the 2MRS pair sample reproduces L21's Newtonian amplitude "
      "5.645 and its dark-to-baryon ratio 30.9 +/- 1.6 inside the pair separation",
      abs(A_N/5.645 - 1) < 0.06 and abs(RATIO_PAIR/30.9 - 1) < 0.15 and abs(NPAIR/1900. - 1) < 0.15,
      f"N = {NPAIR} vs 1900; A = {A_N:.3f} vs 5.645; ratio {RATIO_PAIR:.1f} +/- {E_RATIO_PAIR:.1f} vs 30.9 +/- 1.6")

# ---- A2: L41's fixed-radius cluster ratio at the pair's own 132 kpc --------------------------------------
CLJ = json.load(open(os.path.join(REPO, "qwen_claude_field_theory/closure_2026/"
                                        "cluster_measurement_audit_2026/results.json")))
RR = np.array(CLJ["radii_kpc"], float)
ROWS = CLJ["rows"]
R500 = {d["name"]: d["own_R500_kpc"] for d in CLJ["radius_audit"]}
PROF = {}
for rw in ROWS:
    if rw["footing"] != "canonical": continue
    a0 = A0["canonical"]; r = float(rw["r_kpc"])*kpc
    Mb = rw["g_baryon_over_a0"]*a0*r**2/G/MSUN
    Mh = rw["g_hse_over_a0"]*a0*r**2/G/MSUN
    PROF.setdefault(float(rw["r_kpc"]), []).append((Mb, Mh, rw["cluster"]))
med_ratio = np.array([np.median([(h - b)/b for b, h, _ in PROF[r]]) for r in RR])
sem_ratio = np.array([np.std([(h - b)/b for b, h, _ in PROF[r]], ddof=1)/math.sqrt(len(PROF[r])) for r in RR])
R_CLU_AT_PAIR = float(np.exp(np.interp(math.log(R_PAIR), np.log(RR), np.log(med_ratio))))
E_CLU_AT_PAIR = float(np.exp(np.interp(math.log(R_PAIR), np.log(RR), np.log(sem_ratio))))
CL_OUT = [x for x in PROF[RR[-1]]]
RATIO_CLU = float(np.median([(h - b)/b for b, h, _ in CL_OUT]))
E_RATIO_CLU = float(np.std([(h - b)/b for b, h, _ in CL_OUT], ddof=1))
MBAR_CLU = float(np.median([b for b, h, _ in CL_OUT]))
info(f"A2: at the pair's own {R_PAIR:.0f} kpc the twelve X-COP clusters measure M_dark/M_bar = "
     f"{R_CLU_AT_PAIR:.2f} +/- {E_CLU_AT_PAIR:.2f}; at 1000 kpc they measure {RATIO_CLU:.2f} +/- {E_RATIO_CLU:.2f}")
zA2 = (RATIO_PAIR - R_CLU_AT_PAIR)/math.hypot(E_RATIO_PAIR, E_CLU_AT_PAIR)
info(f"    the pairs need {RATIO_PAIR:.1f} +/- {E_RATIO_PAIR:.1f} at the SAME radius: a factor "
     f"{RATIO_PAIR/R_CLU_AT_PAIR:.1f} at {zA2:.0f} sigma -- L41's A1, reproduced")
check("A2 [CONTROL] this lane reproduces L41's fixed-radius cluster value 9.20 +/- 1.30 at 132 kpc and its "
      "3.4x/11 sigma gap against the pairs, from the same cluster data",
      abs(R_CLU_AT_PAIR/9.20 - 1) < 0.10 and abs(E_CLU_AT_PAIR/1.30 - 1) < 0.30 and abs(zA2) > 8,
      f"{R_CLU_AT_PAIR:.2f} +/- {E_CLU_AT_PAIR:.2f} vs L41's 9.20 +/- 1.30; gap "
      f"{RATIO_PAIR/R_CLU_AT_PAIR:.1f}x at {zA2:.0f} sigma vs L41's 3.4x at 11 sigma")

# ---- A3: the cosmic baryon fraction ----------------------------------------------------------------------
om_b_h70 = OM_B*(HLIT/0.70)**2
info(f"A3: Planck 2018 VI: Omega_b h^2 = {OMBH2}, Omega_m h^2 = {OMMH2}, h = {HLIT}")
info(f"    => Omega_b = {OM_B:.4f}, Omega_m = {OM_M:.4f}, f_bar,cosmic = Omega_b/Omega_m = {F_BAR_COSMIC:.4f}, "
     f"Omega_dm/Omega_b = {(OM_M-OM_B)/OM_B:.2f}")
info(f"    independent check against the FRB measurement: Omega_b h70 = {om_b_h70:.4f} here against Connor+ "
     f"2025's {LIT['connor_ombh70']:.3f} +/- {LIT['connor_eombh70']:.3f} "
     f"({abs(om_b_h70-LIT['connor_ombh70'])/LIT['connor_eombh70']:.1f} sigma)")
check("A3 [CONTROL] this lane's baryon-budget machinery reproduces a published cosmic baryon fraction: "
      "Planck's Omega_b/Omega_m = 0.156 and Omega_dm/Omega_b = 5.4, and agrees with the FRB-measured Omega_b",
      abs(F_BAR_COSMIC - 0.156) < 0.003 and abs((OM_M - OM_B)/OM_B - 5.43) < 0.15
      and abs(om_b_h70 - LIT["connor_ombh70"])/LIT["connor_eombh70"] < 3,
      f"f_bar,cosmic = {F_BAR_COSMIC:.4f} vs 0.156; Omega_dm/Omega_b = {(OM_M-OM_B)/OM_B:.2f} vs 5.43; "
      f"Omega_b h70 = {om_b_h70:.4f} vs {LIT['connor_ombh70']:.3f} +/- {LIT['connor_eombh70']:.3f}")

# ---- A4: a published galaxy-scale baryon deficit ---------------------------------------------------------
def moster_mstar(logMh):
    N, logM1, be, ga = 0.0351, 11.590, 1.376, 0.608
    x = 10**(logMh - logM1)
    return 10**logMh*2*N/(x**(-be) + x**ga)
_LMH = np.linspace(9.0, 15.5, 1301); _LMS = np.log10(moster_mstar(_LMH))
def halo_mass(Mstar): return 10**np.interp(np.log10(np.asarray(Mstar, float)), _LMS, _LMH)
def R200_kpc(Mh): return (3*np.asarray(Mh, float)/(4*math.pi*200*RHO_C_MSUN_MPC3))**(1/3.)*1000.0

# (i) Bregman+2022's own arithmetic: hot gas + stars + disc gas + the mass they say is still missing must
#     equal the halo's cosmic share, and the hot gas must then be the ~30% they quote.
Mstar_L = 5.0e10; Mdisc_gas = 1.0e10                      # an L* galaxy, their own sample description
tot_bregman = LIT["bregman22_M250"] + Mstar_L + Mdisc_gas + LIT["bregman22_missing"]
frac_hot = LIT["bregman22_M250"]/tot_bregman
Mh_impl = tot_bregman/F_BAR_COSMIC
# (ii) abundance matching's own statement of the deficit: stars are what fraction of the cosmic share?
Mh_pairgal = float(halo_mass(MSTAR_GAL)); R200_pairgal = float(R200_kpc(Mh_pairgal))
star_frac = MSTAR_GAL/(F_BAR_COSMIC*Mh_pairgal)
Mh_mw = float(halo_mass(Mstar_L)); star_frac_mw = Mstar_L/(F_BAR_COSMIC*Mh_mw)
info(f"A4: Bregman+ 2022's own accounting, reassembled: hot {LIT['bregman22_M250']:.2e} + stars "
     f"{Mstar_L:.1e} + disc gas {Mdisc_gas:.1e} + their stated missing {LIT['bregman22_missing']:.1e} "
     f"= {tot_bregman:.2e} Msun")
info(f"    => the hot phase is {100*frac_hot:.0f}% of that total against their quoted ~{100*LIT['bregman22_frac']:.0f}%, "
     f"and the implied halo is {Mh_impl:.2e} Msun")
info(f"    abundance matching (Moster+ 2013) at the pair's own per-galaxy M_* = {MSTAR_GAL:.2e}: "
     f"M200 = {Mh_pairgal:.2e} Msun, R200 = {R200_pairgal:.0f} kpc, and the STARS are only "
     f"{100*star_frac:.0f}% of that halo's cosmic baryon share")
info(f"    the same at an L* / Milky-Way M_* = {Mstar_L:.1e}: M200 = {Mh_mw:.2e}, stars = "
     f"{100*star_frac_mw:.0f}% of the cosmic share -- the published 'galaxies retain ~20% of their baryons "
     f"in stars' deficit, reproduced")
check("A4 [CONTROL] this lane's baryon-budget machinery reproduces a published galaxy-scale baryon deficit: "
      "Bregman+ 2022's ~30% hot-halo share of the cosmic budget and abundance matching's ~20% stellar share",
      abs(frac_hot - LIT["bregman22_frac"]) < 0.05 and 0.12 < star_frac_mw < 0.30,
      f"hot phase = {100*frac_hot:.0f}% vs their ~30%; stellar share at L* = {100*star_frac_mw:.0f}% "
      f"(published range 15-25%); implied halo {Mh_impl:.2e} vs abundance matching's {Mh_mw:.2e}")

# ---- A5: the pair forward model reproduces L21's framework amplitudes -------------------------------------
def mass_factor(law, A, a0, eN):
    """The factor by which each member's mass must be multiplied for the law to give the observed
       dispersion.  Solved numerically because deep-MOND (M^1/4) and quasi-Newtonian (M^1/2) differ."""
    base = float(np.median(sigma_pred(law, S["M1"], S["M2"], S["rp"], a0, eN)))
    lo, hi = -3.0, 4.0
    for _ in range(60):
        mid = 0.5*(lo + hi); f = 10**mid
        v = float(np.median(sigma_pred(law, f*S["M1"], f*S["M2"], S["rp"], a0, eN)))
        if v < A*base: lo = mid
        else: hi = mid
    return 10**(0.5*(lo + hi))

AMP = {}
info("A5: the framework's own amplitudes on this rebuild (A = observed / parameter-free prediction):")
for foot in ("canonical", "alt"):
    a0, eN = A0[foot], E_N[foot]
    for law in ("fw_iso", "fw"):
        sh = sigma_pred(law, S["M1"], S["M2"], S["rp"], a0, eN)
        A, eA = ml_amp(S["dv"], sh)
        mf = mass_factor(law, A, a0, eN)
        AMP[(foot, law)] = (A, eA, mf)
        nm = "isolated (BEST CASE)" if law == "fw_iso" else "carried, with the EFE"
        info(f"    {foot:>9}  framework {nm:<22} A = {A:.3f} +/- {eA:.3f}   implied M/M_K = {mf:.2f}")
A_iso_c = AMP[("canonical", "fw_iso")][0]; MF_ISO_C = AMP[("canonical", "fw_iso")][2]
A_iso_a = AMP[("alt", "fw_iso")][0];       MF_ISO_A = AMP[("alt", "fw_iso")][2]
MF_EFE_C = AMP[("canonical", "fw")][2]
check("A5 [CONTROL] the forward model reproduces L21's published framework amplitudes 1.802 (canonical) / "
      "1.731 (alt) and its implied mass factors 8.3 (isolated) and 10.0 (carried)",
      abs(A_iso_c/1.802 - 1) < 0.05 and abs(A_iso_a/1.731 - 1) < 0.05
      and abs(MF_ISO_C/8.3 - 1) < 0.12 and abs(MF_EFE_C/10.0 - 1) < 0.15,
      f"A = {A_iso_c:.3f} / {A_iso_a:.3f} vs 1.802 / 1.731; M/M_K = {MF_ISO_C:.2f} (isolated) and "
      f"{MF_EFE_C:.2f} (carried) vs 8.3 and 10.0")

# ==========================================================================================================
P("\n" + "=" * 122)
P("PART B -- THE REQUIREMENT, stated precisely and recomputed from L21's own numbers.")
P("=" * 122)
P("  How much extra baryonic mass, inside what radius, would the pair kinematics need?  Three readings,")
P("  because they differ and the difference matters:")
P("")

F_NEWTON = A_N**2
F_SHARE = (1.0 + RATIO_PAIR)/(1.0 + F_COSMIC)
REQ = {
  "newton":  ("Newton on baryons alone (no kernel, no dark component)", F_NEWTON),
  "fw_iso":  ("the framework's carried kernel, ISOLATED branch (its best case)", MF_ISO_C),
  "fw":      ("the framework's carried kernel with the computed external field", MF_EFE_C),
  "share":   ("baryons PLUS a cosmic-share dark component (L41's B5 reading)", F_SHARE),
}
info(f"{'reading':<62} {'M_b,true/M_K':>13} {'M_b,true [Msun]':>17} {'undetected [Msun]':>19}")
info("-"*118)
for k in ("newton", "fw_iso", "fw", "share"):
    lbl, f = REQ[k]
    info(f"{lbl:<62} {f:13.2f} {f*MSTAR_GAL:17.3e} {(f-1)*MSTAR_GAL:19.3e}")
info("-"*118)
info(f"all per GALAXY, inside the pairs' own median separation r_p = {R_PAIR:.0f} kpc, against a K-band "
     f"stellar mass of {MSTAR_GAL:.2e} Msun.")
info(f"both footings: the framework's isolated requirement is {MF_ISO_C:.2f}x (canonical) / {MF_ISO_A:.2f}x (alt); "
     f"the Newtonian and cosmic-share readings are footing-free (a0 cancels).")

# the operative number: the framework's OWN best case
F_REQ = MF_ISO_C
M_REQ = F_REQ*MSTAR_GAL                 # total baryons required inside r_p, per galaxy
M_HID = (F_REQ - 1.0)*MSTAR_GAL         # of which undetected
F_REQ_ALT = MF_ISO_A; M_HID_ALT = (F_REQ_ALT - 1.0)*MSTAR_GAL
P("")
info(f"THE OPERATIVE NUMBER, and it is the framework's own BEST case: {M_HID:.3e} Msun of undetected baryons "
     f"inside {R_PAIR:.0f} kpc")
info(f"of an L* galaxy whose detected stellar mass is {MSTAR_GAL:.2e} -- i.e. {F_REQ-1:.1f} stellar masses of "
     f"invisible gas ({F_REQ_ALT-1:.1f} on the alt footing).")
info(f"L41's own B5 quoted {F_SHARE:.2f}x for the cosmic-share reading; this lane reproduces {F_SHARE:.2f}x and "
     f"adds the framework's own {F_REQ:.1f}x, which is the larger and the one that matters here.")

# ---- the profile freedom, priced -------------------------------------------------------------------------
P("")
P("  THE PROFILE FREEDOM.  M(<r_p) is fixed by the kinematics; the SHAPE is free.  Take rho ~ r^-alpha")
P("  truncated at r_p, the one-parameter family that contains every proposal, and price the extremes.")
def enc_frac(alpha, r, rt=None):
    rt = rt if rt is not None else R_PAIR
    return np.clip(np.asarray(r, float)/rt, 0, 1)**(3.0 - alpha)
def sigma_of_b(alpha, b_kpc, Mtot, rt=None):
    """Projected surface density [kg m^-2] at impact parameter b for rho ~ r^-alpha truncated at rt."""
    rt = rt if rt is not None else R_PAIR
    if b_kpc >= rt: return 0.0
    A = (3.0 - alpha)*Mtot*MSUN/(4*math.pi*(rt*kpc)**(3.0 - alpha))     # rho = A r^-alpha
    zmax = math.sqrt(rt**2 - b_kpc**2)*kpc
    z = np.linspace(0.0, zmax, 4000)
    r = np.sqrt((b_kpc*kpc)**2 + z**2)
    return float(2.0*np.trapz(A*np.maximum(r, 1e-6*kpc)**(-alpha), z))
B_FRB = LIT["frb181112_b"]
info(f"    {'alpha':>7} {'M(<10kpc)/M_K':>15} {'N_H(b=29kpc)':>16} {'DM(b=29kpc)':>15} {'<n>(<10kpc)':>14} "
     f"{'<n>(<r_p)':>12}   [cm^-2 / pc cm^-3 / cm^-3]")
PROF_TAB = []
for al in (0.0, 0.5, 1.0, 1.5, 2.0):
    m10 = M_HID*float(enc_frac(al, 10.0))/MSTAR_GAL
    sg = sigma_of_b(al, B_FRB, M_HID)
    NH = sg/(1.4*M_H)*1e-4                                  # cm^-2, mean mass per hydrogen of 1.4 m_H
    DMv = sg/(1.18*M_H)*1e-4/3.0857e18                      # pc cm^-3 if fully ionised
    n10 = M_HID*float(enc_frac(al, 10.0))*MSUN/(1.18*M_H*(4*math.pi/3)*(10.0*kpc)**3)*1e-6
    nmean = M_HID*MSUN/(1.18*M_H*(4*math.pi/3)*(R_PAIR*kpc)**3)*1e-6
    PROF_TAB.append((al, m10, NH, DMv, n10, nmean))
    info(f"    {al:7.1f} {m10:15.3f} {NH:16.3e} {DMv:15.1f} {n10:14.3e} {nmean:12.3e}")
# the profile-FREE numbers: everything inside r_p projects inside r_p, so the MEAN column over the disc of
# radius r_p is fixed by the mass alone.  These carry the argument, so no profile choice can evade them.
SIG_MEAN = M_HID*MSUN/(math.pi*(R_PAIR*kpc)**2)                        # kg m^-2
NH_MEAN = SIG_MEAN/(1.4*M_H)*1e-4                                      # cm^-2
DM_MEAN = SIG_MEAN/(1.18*M_H)*1e-4/3.0857e18                           # pc cm^-3
N_MEAN = M_HID*MSUN/(1.18*M_H*(4*math.pi/3)*(R_PAIR*kpc)**3)*1e-6      # cm^-3
sh_sig = M_HID*MSUN/(2*math.pi*(R_PAIR*kpc)**2)                        # thin shell at r_p, central column
P("")
info(f"    PROFILE-FREE, and this is what carries the argument: every gram inside r_p projects inside r_p, so")
info(f"    the MEAN column over the disc of radius r_p is fixed by the MASS alone, at any alpha:")
info(f"        <N_H> = {NH_MEAN:.3e} cm^-2,   <DM> = {DM_MEAN:.0f} pc cm^-3,   "
     f"<n_e>(<r_p) = {N_MEAN:.3e} cm^-3")
info(f"    at b -> 0 the whole family spans only a factor 3: the uniform sphere gives 1.5x the mean and the")
info(f"    least-detectable configuration there -- a thin shell at r_p -- gives exactly 0.5x the mean, "
     f"{sh_sig/(1.4*M_H)*1e-4:.2e} cm^-2.")
info(f"    No choice of profile hides the column, because the column is fixed by the mass.")
NH_UNI = NH_MEAN; DM_UNI = DM_MEAN

# ==========================================================================================================
P("\n" + "=" * 122)
P("PART C -- THE CONFRONTATION, three ways, because they can differ.")
P("=" * 122)

# ---- C1: the total baryon budget -------------------------------------------------------------------------
P("")
P("  (a) IS THE REQUIRED MASS INSIDE THE TOTAL BARYON BUDGET?  Does the galaxy have that many baryons at all?")
share_moster = F_BAR_COSMIC*Mh_pairgal
# a second, deliberately generous halo mass: the stellar-to-halo relation is uncertain, so bracket it
Mh_lo, Mh_hi = 2.5e12, Mh_pairgal
share_lo, share_hi = F_BAR_COSMIC*Mh_lo, F_BAR_COSMIC*Mh_hi
# a framework-agnostic version: the comoving Lagrangian sphere that must be swept clean of baryons
rho_b_com = OM_B*RHO_C_MSUN_MPC3
R_lag = (3*M_REQ/(4*math.pi*rho_b_com))**(1/3.)
info(f"C1: abundance matching at M_* = {MSTAR_GAL:.2e} gives M200 = {Mh_pairgal:.2e} Msun (R200 = "
     f"{R200_pairgal:.0f} kpc); its ENTIRE cosmic baryon allotment is {share_moster:.3e} Msun.")
info(f"    required inside {R_PAIR:.0f} kpc = 0.{int(100*R_PAIR/R200_pairgal):02d} R200: {M_REQ:.3e} Msun "
     f"= {100*M_REQ/share_moster:.0f}% of the WHOLE allotment,")
info(f"    the stellar-to-halo relation is uncertain, so bracket it: M200 = {Mh_hi:.1e} Msun (Moster+ 2013, "
     f"the GENEROUS end) gives {100*M_REQ/share_hi:.0f}%,")
info(f"    M200 = {Mh_lo:.1e} Msun (the value abundance matching gives this M_* at the conservative end) "
     f"gives {100*M_REQ/share_lo:.0f}% -- i.e. MORE than the halo owns.")
info(f"    framework-agnostic version: gathering {M_REQ:.2e} Msun of baryons needs a comoving Lagrangian "
     f"sphere of radius {R_lag:.2f} Mpc swept to 100% efficiency,")
info(f"    against the {(3*Mh_pairgal/(4*math.pi*OM_M*RHO_C_MSUN_MPC3))**(1/3.):.2f} Mpc the halo's own "
     f"total mass corresponds to.")
check("C1 (a) the required mass is inside the system's total baryon budget -- the galaxy has that many "
      "baryons to hide",
      M_REQ < share_moster,
      f"{M_REQ:.2e} against the halo's whole cosmic share {share_moster:.2e}: "
      f"{100*M_REQ/share_moster:.0f}% of it, all of it inside 0.{int(100*R_PAIR/R200_pairgal):02d} R200 and "
      f"none of it anywhere else in the halo.  It PASSES on the generous halo mass and reaches "
      f"{100*M_REQ/share_lo:.0f}% on the conservative one, so this arm is at the ceiling, not comfortably "
      f"inside it")

# ---- C2: the observed radial distribution ----------------------------------------------------------------
P("")
P("  (b) IS IT CONSISTENT WITH THE OBSERVED RADIAL DISTRIBUTION?  Can that much sit at ~130 kpc?")
# Werk+2014's OWN measured cool-phase density profile, integrated to 132 kpc
def werk_mass(R_kpc):
    """M = int 4 pi r^2 mu m_H n_H dr with n_H = n0 (r/Rvir)^-0.8, Werk+ 2014's fitted profile."""
    n0 = LIT["werk_nH0"]*1e6                       # m^-3
    Rv = LIT["werk_Rvir"]*kpc; R = R_kpc*kpc; p = LIT["werk_nH_slope"]
    return 4*math.pi*1.4*M_H*n0*Rv**(-p)*R**(3.0 + p)/(3.0 + p)/MSUN
M_cool_132 = werk_mass(R_PAIR)
M_hot_132 = LIT["bregman18_M50"]*(R_PAIR/50.0)**(3.0 + LIT["bregman18_rho_slope"])
M_sz_132 = LIT["bregman22_M250"]*(R_PAIR/LIT["bregman22_R"])**(3.0 + LIT["bregman18_rho_slope"])
e_sz_132 = LIT["bregman22_eM250"]*(R_PAIR/LIT["bregman22_R"])**(3.0 + LIT["bregman18_rho_slope"])
M_det_132 = M_cool_132 + M_hot_132
M_gen = LIT["bregman22_M250"] + LIT["werk_Mcool"]     # the most generous possible reading, at 250 kpc / R_vir
info(f"    {'measurement':<58} {'as published':>26} {'scaled to 132 kpc':>19}")
info(f"    {'-'*58} {'-'*26} {'-'*19}")
info(f"    {'Werk+ 2014 COS-Halos cool phase (its own n_H profile)':<58} "
     f"{'>6.5e10 within R_vir':>26} {M_cool_132:19.2e}")
info(f"    {'Bregman+ 2018 X-ray hot halo (its own rho ~ r^-1.5)':<58} "
     f"{'5.0e09 within 50 kpc':>26} {M_hot_132:19.2e}")
info(f"    {'Bregman+ 2022 SZ (thermal pressure, density-linear)':<58} "
     f"{'9.8+/-2.8e10 within 250kpc':>26} {M_sz_132:19.2e}")
info(f"    {'sum of the detected phases':<58} {'':>26} {M_det_132:19.2e}")
info(f"    {'REQUIRED (framework carried kernel, best case)':<58} {'':>26} {M_HID:19.2e}")
info(f"    the requirement exceeds the summed measured CGM at the same radius by {M_HID/M_det_132:.0f}x; "
     f"even against the")
info(f"    MOST generous possible reading -- the full SZ mass at 250 kpc PLUS the full COS-Halos cool mass "
     f"within R_vir, {M_gen:.2e} Msun")
info(f"    at twice the radius -- it is over by {M_HID/M_gen:.1f}x "
     f"({(M_HID-LIT['bregman22_M250'])/LIT['bregman22_eM250']:.0f} sigma on the SZ statistical error alone).")
check("C2 (b) the required mass is consistent with the observed radial distribution: that much CGM is "
      "measured at ~130 kpc",
      M_HID < M_det_132 + 3*e_sz_132,
      f"required {M_HID:.2e} Msun against a summed measured {M_det_132:.2e} at the same radius "
      f"({M_HID/M_det_132:.0f}x over) and against the most generous reading {M_gen:.2e} at twice the radius "
      f"({M_HID/M_gen:.1f}x over).  Three independent probes -- UV absorption, X-ray emission and the "
      f"thermal SZ -- agree on the amount and none of them leaves room")

# ---- C3: non-detection, dispersion measure ---------------------------------------------------------------
P("")
P("  (c) IS IT EXCLUDED BY NON-DETECTION?  If that much gas were there, would we have seen it?")
P("      c-i  DISPERSION MEASURE (free electrons; the most model-independent channel).")
DM_at_b = {al: sigma_of_b(al, B_FRB, M_HID)/(1.18*M_H)*1e-4/3.0857e18 for al in (0.0, 1.0, 1.5)}
DM_shell = (M_HID*MSUN/(2*math.pi*(R_PAIR*kpc)**2)/math.sqrt(1 - (B_FRB/R_PAIR)**2)
            )/(1.18*M_H)*1e-4/3.0857e18
DM_MIN = min(DM_shell, min(DM_at_b.values()))
info(f"      required DM at the FRB's own impact parameter b = {B_FRB:.0f} kpc:")
info(f"        uniform sphere {DM_at_b[0.0]:.0f} pc cm^-3;  rho ~ r^-1 {DM_at_b[1.0]:.0f};  "
     f"rho ~ r^-1.5 {DM_at_b[1.5]:.0f};  thin shell at r_p (the family MINIMUM) {DM_shell:.0f}")
info(f"      and the profile-FREE mean over the whole disc of radius r_p: <DM> = {DM_MEAN:.0f} pc cm^-3")
info(f"      measured, Prochaska+ 2019 (FRB 181112 through a log M* = {LIT['frb181112_logMstar']} foreground "
     f"galaxy, MORE massive than this pair's members and at a SMALLER impact parameter, where a halo's DM is "
     f"LARGER):")
info(f"        DM_FG = {LIT['frb181112_DMlo']:.0f}-{LIT['frb181112_DMhi']:.0f} pc cm^-3, and n_e < "
     f"{LIT['frb181112_ne_max']:.0e} cm^-3 for hot virialised halo gas")
info(f"      the Milky Way's own halo, Prochaska & Zheng 2019: DM = {LIT['mwhalo_DMlo']:.0f}-"
     f"{LIT['mwhalo_DMhi']:.0f} pc cm^-3 out to {LIT['mwhalo_R']:.0f} kpc, against a required "
     f"{DM_MEAN:.0f} inside only {R_PAIR:.0f} kpc.")
DM_ratio = DM_at_b[0.0]/LIT["frb181112_DMhi"]
check("C3 (c-i) the implied dispersion measure is consistent with the FRB constraints on foreground galaxy "
      "halos and on the Milky Way's own halo",
      DM_MIN < LIT["frb181112_DMhi"],
      f"required {DM_at_b[0.0]:.0f} pc cm^-3 at b = {B_FRB:.0f} kpc against a measured "
      f"{LIT['frb181112_DMlo']:.0f}-{LIT['frb181112_DMhi']:.0f} ({DM_ratio:.1f}x over), and the family "
      f"MINIMUM -- a thin shell at r_p, the least detectable configuration there is -- still gives "
      f"{DM_MIN:.0f}, {DM_MIN/LIT['frb181112_DMhi']:.1f}x over.  The mean density {N_MEAN:.2e} cm^-3 also "
      f"sits at Prochaska+ 2019's own ceiling n_e < {LIT['frb181112_ne_max']:.0e} for hot halo gas, which "
      f"any centrally concentrated profile then exceeds")

# ---- C4: non-detection, X-ray emission -------------------------------------------------------------------
P("      c-ii X-RAY EMISSION (emissivity ~ n^2, so this is the sharpest channel if the gas is hot).")
def emission_measure(alpha, Mtot, R_kpc, r_in=0.5):
    """int n^2 dV for rho = A r^-alpha truncated at R, normalised to total mass Mtot inside R."""
    A = (3.0 - alpha)*Mtot*MSUN/(4*math.pi*(R_kpc*kpc)**(3.0 - alpha))
    r = np.exp(np.linspace(math.log(r_in*kpc), math.log(R_kpc*kpc), 3000))
    n = A*r**(-alpha)/(1.18*M_H)
    return float(np.trapz(4*math.pi*r**2*n**2, r))
EM_ratio = (M_HID/M_hot_132)**2                      # matched shape: the shape cancels exactly
EM_floor = emission_measure(0.0, M_HID, R_PAIR)/emission_measure(1.5, M_hot_132, R_PAIR)
Tvir = 0.5*0.6*M_H*G*Mh_pairgal*MSUN/(1.381e-23*R200_pairgal*kpc)
info(f"      at the SAME shape and temperature the surface brightness scales as the SQUARE of the gas mass, so")
info(f"      the required halo would be ({M_HID:.2e}/{M_hot_132:.2e})^2 = {EM_ratio:.0f}x brighter than the "
     f"hot halos")
info(f"      Bregman+ 2018 detect and eROSITA now resolves by stacking out to R_vir.  A FLOOR that grants the")
info(f"      escape the minimum-emission configuration there is -- uniform density, which minimises "
     f"int n^2 dV at fixed")
info(f"      mass and volume -- against the observed rho ~ r^-1.5 still leaves {EM_floor:.0f}x.  The virial")
info(f"      temperature of this halo is {Tvir:.2e} K, so the gas would be in exactly the band those surveys "
     f"observe,")
info(f"      and a COOLER phase radiates MORE per unit emission measure in the soft band, so that direction "
     f"does not help.")
check("C4 (c-ii) the implied X-ray emission is consistent with the measured hot halos of L* galaxies",
      EM_floor < 4.0,
      f"the required gas would be {EM_ratio:.0f}x brighter in X-rays at matched shape and temperature than "
      f"the halos Bregman+ 2018 and eROSITA measure, and {EM_floor:.0f}x even granting it the "
      f"minimum-emission uniform configuration.  This is a ratio of emission measures and needs no cooling "
      f"function; it fails by two to three orders of magnitude, not marginally")

# ---- C5: non-detection, absorption ------------------------------------------------------------------------
P("      c-iii ABSORPTION COLUMN (works for any phase that is not fully neutral AND not fully molecular).")
NH_obs = 10**LIT["werk_logNH"]
info(f"      required MEAN total-hydrogen column inside r_p, which is profile-free: {NH_MEAN:.2e} cm^-2")
info(f"      per-profile at the FRB's b = {B_FRB:.0f} kpc: {PROF_TAB[0][2]:.2e} (uniform), "
     f"{PROF_TAB[3][2]:.2e} (rho ~ r^-1.5); thin-shell central column {sh_sig/(1.4*M_H)*1e-4:.2e}")
info(f"      measured, Werk+ 2014 COS-Halos: mean log N_H = {LIT['werk_logNH']} i.e. {NH_obs:.1e} cm^-2 for "
     f"L* galaxies inside 160 kpc,")
info(f"      AFTER the ionisation correction that already multiplies N_HI by ~100.  The requirement is "
     f"{NH_MEAN/NH_obs:.0f}x that, over the SAME aperture.")
check("C5 (c-iii) the implied absorption column is consistent with the measured circumgalactic hydrogen "
      "column at these radii",
      NH_MEAN < 3*NH_obs,
      f"required mean {NH_MEAN:.2e} cm^-2 against COS-Halos' measured mean {NH_obs:.1e} cm^-2 over the same "
      f"aperture ({NH_MEAN/NH_obs:.0f}x over), and {sh_sig/(1.4*M_H)*1e-4/NH_obs:.0f}x over even for the "
      f"thin shell.  The mean column is fixed by the mass alone, so no profile choice reaches the measured "
      f"value")

# ---- C6: in-situ density ---------------------------------------------------------------------------------
P("      c-iv IN-SITU DENSITY, where it has been measured directly rather than inferred from a column.")
n_req_48 = M_HID*float(enc_frac(0.0, LIT["salem_r"]))*MSUN/(1.18*M_H*(4*math.pi/3)
                                                            *(LIT["salem_r"]*kpc)**3)*1e-6
info(f"      Salem+ 2015 measure the Milky Way's halo density from the ram-pressure stripping of the LMC's "
     f"disc:")
info(f"        n = {LIT['salem_n']:.2e} +/- {LIT['salem_en']:.2e} cm^-3 at r = {LIT['salem_r']:.1f} kpc")
info(f"      the requirement, uniform (the shallowest and therefore most favourable profile), gives "
     f"{n_req_48:.2e} cm^-3 there: {n_req_48/LIT['salem_n']:.0f}x higher.")
check("C6 (b/c) the implied in-situ gas density agrees with the one place it is measured directly, the Milky "
      "Way's halo at ~50 kpc",
      n_req_48 < LIT["salem_n"] + 3*LIT["salem_en"],
      f"required {n_req_48:.2e} cm^-3 at {LIT['salem_r']:.0f} kpc against Salem+ 2015's measured "
      f"{LIT['salem_n']:.2e} +/- {LIT['salem_en']:.2e} ({n_req_48/LIT['salem_n']:.0f}x over).  A ram-pressure "
      f"measurement is a direct dynamical weighing of the gas and does not depend on ionisation state, "
      f"temperature or metallicity.  STATED AGAINST INTEREST: this one arm alone IS evadable, by a hollow "
      f"configuration that puts nothing at 48 kpc -- but the hollow limit is the thin shell, which C3 and C5 "
      f"then catch at {DM_MIN/LIT['frb181112_DMhi']:.1f}x and {sh_sig/(1.4*M_H)*1e-4/NH_obs:.0f}x, and which "
      f"C4 catches worst of all because a shell maximises int n^2 dV")

# ---- C7: the global closure ------------------------------------------------------------------------------
P("      c-v  GLOBAL CLOSURE.  If EVERY galaxy carried this, how much of the cosmic baryon budget would sit")
P("           inside 132 kpc of a galaxy, and does the measured baryon partition allow it?")
frac_halo_req = (F_REQ - 1.0)*LIT["omstar_over_omb"] + LIT["omstar_over_omb"]
e_frac = F_REQ*LIT["e_omstar_over_omb"]
allow_connor = 1.0 - LIT["connor_figm"]; allow_flim = 1.0 - LIT["flimflam_figm"]
info(f"      Omega_*/Omega_b today = {LIT['omstar_over_omb']:.2f} +/- {LIT['e_omstar_over_omb']:.2f}, so a "
     f"host-blind rule of {F_REQ:.1f}x the stellar mass puts")
info(f"        Omega(<132 kpc of a galaxy)/Omega_b = {frac_halo_req:.2f} +/- {e_frac:.2f} of ALL cosmic baryons")
info(f"      measured non-IGM fraction: Connor+ 2025 f_IGM = {LIT['connor_figm']:.2f} +/- "
     f"{LIT['connor_efigm']:.2f} leaves {allow_connor:.2f} +/- {LIT['connor_efigm']:.2f} for ALL halos "
     f"(clusters and groups included);")
info(f"                                 FLIMFLAM DR1 f_igm = {LIT['flimflam_figm']:.2f} +/- "
     f"{LIT['flimflam_efigm']:.2f} leaves {allow_flim:.2f} +/- {LIT['flimflam_efigm']:.2f}")
z_connor = (frac_halo_req - allow_connor)/math.hypot(e_frac, LIT["connor_efigm"])
z_flim = (frac_halo_req - allow_flim)/math.hypot(e_frac, LIT["flimflam_efigm"])
info(f"      tension: {z_connor:+.1f} sigma against Connor+ 2025, {z_flim:+.1f} sigma against FLIMFLAM DR1 "
     f"-- and the FRB measurements disagree with each other by more than that, so this arm is real but NOT "
     f"decisive.")
check("C7 (c-v) the global baryon partition measured by fast radio bursts allows this much mass inside "
      "132 kpc of galaxies",
      z_flim < 3.0,
      f"required {frac_halo_req:.2f} +/- {e_frac:.2f} of all baryons against a measured non-IGM budget of "
      f"{allow_flim:.2f} +/- {LIT['flimflam_efigm']:.2f} (FLIMFLAM, {z_flim:+.1f} sigma) and "
      f"{allow_connor:.2f} +/- {LIT['connor_efigm']:.2f} (Connor+ 2025, {z_connor:+.1f} sigma).  This arm "
      f"PASSES on the more permissive of the two FRB analyses and is stated as a tension, not a kill -- the "
      f"kill is C2-C6, which are local and much sharper")

# ---- C8: the Milky Way, framework-internal ----------------------------------------------------------------
P("")
P("      c-vi THE MILKY WAY, tested inside the framework's OWN kernel.  This is the one galaxy where the")
P("           enclosed mass at ~100 kpc is measured directly, so the escape can be run against it.")
def M_dyn_from_bar(Mb, r_kpc, a0):
    gb = G*Mb*MSUN/(r_kpc*kpc)**2
    return float(g_kernel(gb, a0))*(r_kpc*kpc)**2/G/MSUN
R_MW = 100.0
MW_frac = float(enc_frac(0.0, R_MW))
MW_hid = (F_REQ - 1.0)*Mstar_L*MW_frac                     # the same host-blind rule at the MW's OWN M_*
MW_det = Mstar_L + Mdisc_gas
row = []
for foot in ("canonical", "alt"):
    a0 = A0[foot]
    m_det = M_dyn_from_bar(MW_det, R_MW, a0)
    m_esc = M_dyn_from_bar(MW_det + MW_hid, R_MW, a0)
    row.append((foot, m_det, m_esc))
    info(f"      {foot:>9}: framework kernel on the DETECTED baryons ({MW_det:.2e} Msun) predicts "
         f"M(<100 kpc) = {m_det:.2e} Msun")
    info(f"      {'':>9}  the same kernel with the escape's {MW_hid:.2e} Msun added predicts {m_esc:.2e} Msun")
info(f"      measured, Deason+ 2021 from halo stars: M(<100 kpc) = {LIT['deason_M100']:.2e} +/- "
     f"{LIT['deason_eM100']:.2e} Msun (stat + sys)")
# AGAINST INTEREST: L21's M0 found the framework's deficit GROWS with host mass (A: 1.59 -> 2.10 across
# 0.56 dex).  The Milky Way sits at the LOW-mass end of the pair sample, so the fair requirement there is
# the low-mass-bin amplitude, not the sample median.  Priced rather than ignored.
F_LOW = mass_factor("fw_iso", 1.59, A0["canonical"], E_N["canonical"])
MW_hid_low = (F_LOW - 1.0)*Mstar_L*MW_frac
m_esc_low = M_dyn_from_bar(MW_det + MW_hid_low, R_MW, A0["canonical"])
z_esc_low = (m_esc_low - LIT["deason_M100"])/LIT["deason_eM100"]
info(f"      AGAINST INTEREST: L21's M0 found the framework's deficit GROWS with host mass (A = 1.59 in the "
     f"lowest mass bin against 1.80 for the sample).")
info(f"      The Milky Way sits at the LOW-mass end, so the fair requirement there is {F_LOW:.2f}x rather "
     f"than {F_REQ:.2f}x, giving {MW_hid_low:.2e} Msun and a predicted")
info(f"      M(<100 kpc) = {m_esc_low:.2e}: {m_esc_low/LIT['deason_M100']:.1f}x measured at "
     f"{z_esc_low:.1f} sigma.  Weaker, and still a fail; the check below carries the SAMPLE value and this "
     f"line is the honest floor.")
z_det = (row[0][1] - LIT["deason_M100"])/LIT["deason_eM100"]
z_esc = min(abs((r[2] - LIT["deason_M100"])/LIT["deason_eM100"]) for r in row)
esc_ratio = min(r[2] for r in row)/LIT["deason_M100"]
info(f"      => with the detected baryons the framework's kernel lands at {abs(z_det):.1f} sigma (this is a "
     f"genuine success of the KERNEL and is recorded as one,")
info(f"         though it is not a discriminant: LambdaCDM's own halo fits the same number by construction).  "
     f"With the escape's baryons it over-predicts by")
info(f"         {esc_ratio:.1f}x, at {z_esc:.1f} sigma, on BOTH footings.")
check("C8 (b) the required baryons are compatible with the Milky Way's directly measured enclosed mass at "
      "100 kpc, run through the framework's own kernel",
      z_esc < 3.0,
      f"the kernel plus the escape's baryons predicts M(<100 kpc) = {min(r[2] for r in row):.2e} Msun "
      f"against Deason+ 2021's measured {LIT['deason_M100']:.2e} +/- {LIT['deason_eM100']:.2e}: "
      f"{esc_ratio:.1f}x over at {z_esc:.1f} sigma, and {m_esc_low/LIT['deason_M100']:.1f}x at "
      f"{z_esc_low:.1f} sigma on the low-mass-bin amplitude that is fairer to the Milky Way.  The same "
      f"kernel on the DETECTED baryons lands at {abs(z_det):.1f} sigma, so this is a statement about the "
      f"escape and not about the kernel")

# ---- the phase-by-phase table -----------------------------------------------------------------------------
P("")
P("  WHICH PHASE COULD IT BE?  Every phase has a detection channel; the table names the channel and the")
P("  factor by which the requirement exceeds what that channel measures.")
info(f"    {'phase':<34} {'channel':<34} {'requirement exceeds by':>23}")
info(f"    {'-'*34} {'-'*34} {'-'*23}")
info(f"    {'hot, T ~ 10^6.3 K (virial)':<34} {'X-ray emission (n^2)':<34} {EM_floor:22.0f}x")
info(f"    {'warm-hot, 10^5-10^6 K':<34} {'dispersion measure + O VI/O VII':<34} {DM_ratio:22.1f}x")
info(f"    {'cool photoionised, 10^4 K':<34} {'Lyman-alpha + metal columns':<34} {NH_MEAN/NH_obs:22.0f}x")
info(f"    {'cold neutral atomic':<34} {'N_HI: every sightline a DLA':<34} {NH_MEAN/2.0e20:22.1f}x")
info(f"    {'cold molecular clumps':<34} {'NONE of the above directly':<34} {'not excluded here':>23}")
info(f"    {'compact objects (MACHOs)':<34} {'microlensing (EROS-2, Tisserand+07)':<34} {'< 8% of a halo':>23}")
info(f"    (the 'cold neutral atomic' row is the ratio of the required column to the damped-Lyman-alpha "
     f"threshold 2e20 cm^-2:")
info(f"     a fully neutral phase would make EVERY sightline within 132 kpc of an L* galaxy a DLA, and none "
     f"is seen.)")
info("    the ONE surviving phase is cold, dense, neutral molecular gas with a tiny volume filling factor.")
info(f"    Prochaska+ 2019's same sightline bounds exactly that: f_V < 1e-4 for cool clumps embedded in hot")
info("    halo gas.  And it is closed independently at cluster scale by D1 below, which does not care about")
info("    the phase at all -- only about the amount.")

# ==========================================================================================================
P("\n" + "=" * 122)
P("PART D -- THE CONSEQUENCES.  Undetected baryons at pair scale are not free.  Can ONE distribution serve")
P("          the pairs, the clusters, the rotation curves and the lensing shape together?")
P("=" * 122)

# ---- D1: clusters -----------------------------------------------------------------------------------------
P("")
P("  D1 CLUSTERS.  The rule is host-blind by construction, so it must also apply to the galaxies IN clusters,")
P("     where the baryon fraction is measured and is near-cosmic.  X-COP publishes both M_gas and M_star.")
def _rkpc(rad, unit, R5):
    u = (unit or "").strip().lower()
    if u in ("r/r500", "r500"): return np.asarray(rad, float)*R5
    if u == "mpc": return np.asarray(rad, float)*1e3
    return np.asarray(rad, float)
def li(xq, x, v):
    m = (x > 0) & (v > 0)
    return np.exp(np.interp(np.log(xq), np.log(x[m]), np.log(v[m])))
def load_cluster(name):
    p = os.path.join(XDIR, name); c = {"name": name}
    with fits.open(os.path.join(p, name + "_hydro_mass.fits")) as f:
        d = f[1].data; R5 = float(f[1].header["R500"]); c["R500"] = R5
        c["rh"] = _rkpc(d["RADIUS"], f[1].columns["RADIUS"].unit, R5); c["Mh"] = np.array(d["M_FORW"], float)
    with fits.open(os.path.join(p, name + "_fgas_profile.fits")) as f:
        d = f[1].data
        c["rg"] = _rkpc(d["RADIUS"], f[1].columns["RADIUS"].unit, c["R500"]); c["Mg"] = np.array(d["MGAS"], float)
    sp = os.path.join(p, name + "_mstar.fits"); c["has_star"] = os.path.exists(sp)
    if c["has_star"]:
        with fits.open(sp) as f:
            d = f[2].data
            c["rs"] = _rkpc(d["RADIUS"], f[2].columns["RADIUS"].unit, c["R500"]); c["Ms"] = np.array(d["MSTAR"], float)
    return c
R_CL = 1000.0
MHSE = {}
for rw in ROWS:
    if rw["footing"] != "canonical" or float(rw["r_kpc"]) != R_CL: continue
    MHSE[rw["cluster"]] = rw["g_hse_over_a0"]*A0["canonical"]*(R_CL*kpc)**2/G/MSUN
info(f"    {'cluster':<9} {'M_gas':>11} {'M_star':>11} {'M_HSE':>11} {'f_bar':>8} {'f_bar with the rule':>20} "
     f"{'/ cosmic':>9}")
CLROWS = []
for n in sorted(R500):
    c = load_cluster(n)
    if not c["has_star"] or n not in MHSE: continue
    Mg = float(li(np.array([R_CL]), c["rg"], c["Mg"])[0])
    Ms = float(li(np.array([R_CL]), c["rs"], c["Ms"])[0])
    Mh = MHSE[n]
    fb = (Mg + Ms)/Mh; fb2 = (Mg + Ms + (F_REQ - 1.0)*Ms)/Mh
    CLROWS.append((n, Mg, Ms, Mh, fb, fb2))
    info(f"    {n:<9} {Mg:11.3e} {Ms:11.3e} {Mh:11.3e} {fb:8.3f} {fb2:20.3f} {fb2/F_BAR_COSMIC:9.2f}")
fb_med = float(np.median([r[4] for r in CLROWS])); fb2_med = float(np.median([r[5] for r in CLROWS]))
fb2_min = min(r[5] for r in CLROWS)
info(f"    median measured f_bar = {fb_med:.3f} (cosmic {F_BAR_COSMIC:.3f}); with the host-blind rule applied "
     f"to the clusters' OWN stellar mass it becomes {fb2_med:.3f},")
info(f"    i.e. {fb2_med/F_BAR_COSMIC:.2f}x the cosmic baryon fraction, in {sum(1 for r in CLROWS if r[5] > F_BAR_COSMIC)} "
     f"of {len(CLROWS)} clusters, and the framework's own reading makes it WORSE:")
info(f"    the framework's kernel says the true gravitating mass is BELOW M_HSE, which raises f_bar further.")
check("D1 the same host-blind rule, applied to the clusters' own measured stellar mass, keeps the cluster "
      "baryon fraction at or below the cosmic value",
      fb2_med <= F_BAR_COSMIC*1.10,
      f"it does not: f_bar runs {fb_med:.3f} -> {fb2_med:.3f} = {fb2_med/F_BAR_COSMIC:.2f}x cosmic (worst "
      f"cluster {max(r[5] for r in CLROWS)/F_BAR_COSMIC:.2f}x, best {fb2_min/F_BAR_COSMIC:.2f}x).  A cluster "
      f"cannot hold more baryons per unit mass than the universe does.  The only repair is to make the rule "
      f"environment-dependent -- gas retained in the field, stripped and already-counted in clusters -- "
      f"which is a SECOND free function on top of the first")

# ---- D2: rotation curves ----------------------------------------------------------------------------------
P("")
P("  D2 ROTATION CURVES.  The framework's kernel already fits SPARC with the DETECTED baryons; the escape")
P("     must not put enough inside 10 kpc to break that.  L21's own tolerance, recomputed here.")
def rar_tol(Mb, r_kpc, a0, tol_dex=0.11):
    gb = G*Mb*MSUN/(r_kpc*kpc)**2; g0 = float(g_kernel(gb, a0))
    lo, hi = 0.0, 60.0
    for _ in range(80):
        f = 0.5*(lo + hi); gbf = (1 + f)*gb
        gf = float(g_kernel(gbf, a0))
        if math.log10(gf/g0) < tol_dex: lo = f
        else: hi = f
    return 0.5*(lo + hi)
TOL_L = rar_tol(8e10, 10.0, A0["canonical"]); TOL_D = rar_tol(2e9, 10.0, A0["canonical"])
info(f"     tolerance on extra mass inside 10 kpc: {TOL_L:.3f} M_b at L* (M_b = 8e10) and {TOL_D:.3f} M_b at a "
     f"dwarf (M_b = 2e9), from the RAR's own 0.11 dex scatter")
info(f"     the escape's truncation radius at a dwarf is scaled as M_*^(1/3) at fixed mean density, which is "
     f"the choice generous to the escape.")
info(f"     {'alpha':>7} {'L*: inside 10 kpc':>19} {'dwarf: inside 10 kpc':>21} {'rho_X log-slope':>17} "
     f"{'verdict':>9}")
OK_ALPHA = []
for al in np.round(np.arange(0.0, 2.51, 0.25), 3):
    rt_d = R_PAIR*(2e9/8e10)**(1/3.)
    mL = (F_REQ - 1.0)*float(enc_frac(al, 10.0, R_PAIR))
    mD = (F_REQ - 1.0)*float(enc_frac(al, 10.0, rt_d))
    ok = (mL < TOL_L) and (mD < TOL_D)
    if ok: OK_ALPHA.append(al)
    info(f"     {al:7.2f} {mL:19.3f} {mD:21.3f} {-al:17.2f} {'pass' if ok else 'FAIL':>9}")
info(f"     admissible: alpha in [{min(OK_ALPHA):.2f}, {max(OK_ALPHA):.2f}]" if OK_ALPHA else
     "     admissible: EMPTY")
check("D2 some member of the profile family puts little enough inside 10 kpc to leave the rotation-curve fit "
      "intact at BOTH L* and dwarf scale",
      len(OK_ALPHA) > 0,
      f"admissible alpha in [{min(OK_ALPHA):.2f}, {max(OK_ALPHA):.2f}] -- the gate is passable, and by "
      f"SHALLOW profiles only.  This arm does NOT close the door; L41 already found this and it is "
      f"reproduced here" if OK_ALPHA else "no member passes")

# ---- D3: the lensing shape ---------------------------------------------------------------------------------
P("")
P("  D3 LENSING SHAPE.  L24 measures d ln DeltaSigma / d ln R = -0.851 +/- 0.040 over 0.5-2 Mpc, against the")
P("     framework's own -0.309: short by 0.54 at 9 sigma.  Does the escape move it?")
info(f"     the escape adds mass in proportion to the STELLAR profile, which X-COP already measures and which")
info(f"     is already inside M_bar.  Its enclosed-mass log-slope over 0.5-2 Mpc, from the same X-COP stellar")
info(f"     profiles used in D1:")
Rg = np.exp(np.linspace(math.log(500.), math.log(2000.), 12))
sl_star, sl_bar, sl_esc = [], [], []
for n, Mg, Ms, Mh, fb, fb2 in CLROWS:
    c = load_cluster(n)
    ms = li(np.clip(Rg, c["rs"].min(), c["rs"].max()), c["rs"], c["Ms"])
    mg = li(np.clip(Rg, c["rg"].min(), c["rg"].max()), c["rg"], c["Mg"])
    sl_star.append(float(np.polyfit(np.log(Rg), np.log(ms), 1)[0]))
    sl_bar.append(float(np.polyfit(np.log(Rg), np.log(mg + ms), 1)[0]))
    sl_esc.append(float(np.polyfit(np.log(Rg), np.log(mg + F_REQ*ms), 1)[0]))
d_ln_star = float(np.mean(sl_star)); d_ln_bar = float(np.mean(sl_bar)); sl_new = float(np.mean(sl_esc))
info(f"       d ln M_star / d ln r = {d_ln_star:+.3f}, d ln M_bar / d ln r = {d_ln_bar:+.3f} over 0.5-2 Mpc")
info(f"     the escape's added component is (F-1) x M_star(r), so it changes M_bar's log-slope from "
     f"{d_ln_bar:+.3f} to")
info(f"     {sl_new:+.3f} -- a move of {sl_new-d_ln_bar:+.3f} in the enclosed-mass slope.  The measured shear")
info(f"     slope needs the SOURCE to be NFW-like ({LIT['L24_fw_shear_slope']:+.3f} is what the framework's "
     f"near-uniform phantom gives, against -0.851 measured).")
info(f"     But the escape's component is BARYONIC and in a cluster the baryons are DIRECTLY MEASURED: adding")
info(f"     undetected baryons to a cluster is exactly what D1 forbids.  So the escape cannot repair R4 -- it")
info(f"     is barred from acting in clusters at all, and R4 is a statement about clusters.")
check("D3 the escape repairs, or even moves, L24's 9 sigma cluster lensing-shape failure",
      abs(sl_new - d_ln_bar) > 0.30 and fb2_med <= F_BAR_COSMIC*1.10,
      f"it does not: the added component moves the cluster baryon enclosed-mass slope by only "
      f"{sl_new-d_ln_bar:+.3f}, and the amount needed to matter is precisely the amount D1 excludes.  The "
      f"escape fixes the pairs and leaves the cluster residual, its 3-D shape (R3) and its projected shear "
      f"shape (R4) exactly where L41 found them")

# ---- D4: the joint test --------------------------------------------------------------------------------------
P("")
P("  D4 THE JOINT TEST.  One distribution, four constraints.")
JOINT = [
  ("pairs  -- supplies 30.9 M_bar inside 132 kpc", M_HID < M_det_132 + 3*e_sz_132,
   f"needs {M_HID:.1e} Msun; the measured CGM at that radius is {M_det_132:.1e}"),
  ("clusters -- keeps f_bar at or below cosmic", fb2_med <= F_BAR_COSMIC*1.10,
   f"f_bar {fb_med:.3f} -> {fb2_med:.3f} = {fb2_med/F_BAR_COSMIC:.2f}x cosmic"),
  ("rotation curves -- under 0.41 M_b inside 10 kpc", len(OK_ALPHA) > 0,
   f"passable for alpha <= {max(OK_ALPHA):.2f}" if OK_ALPHA else "no member passes"),
  ("lensing shape -- reaches -0.851 +/- 0.040", False,
   f"untouched at {LIT['L24_fw_shear_slope']:+.3f}, 9 sigma short"),
]
for lbl, ok, det in JOINT:
    info(f"     [{'pass' if ok else 'FAIL'}] {lbl:<48} {det}")
n_ok = sum(1 for _, ok, _ in JOINT if ok)
check("D4 [THE JOINT TEST] a single undetected-baryon distribution serves the pairs, the clusters, the "
      "rotation curves and the lensing shape at once",
      n_ok == len(JOINT),
      f"{n_ok} of {len(JOINT)} arms pass.  Only the rotation-curve arm is satisfiable, and it is the one "
      f"L41 had already shown does not close the door.  The two arms that DECIDE -- the measured CGM mass at "
      f"pair separation and the cluster baryon fraction -- fail in OPPOSITE directions: the pairs need more "
      f"gas than is observed, and the clusters cannot absorb any")

# ==========================================================================================================
P("\n" + "=" * 122)
P("PART E -- THE VERDICT.")
P("=" * 122)
P("")
P("  E0 SENSITIVITY.  The verdict is quoted for the framework's own best case.  Does it depend on that")
P("     choice?  Every reading of the requirement, against every local arm:")
SHORT = {"newton": "Newton on baryons alone", "fw": "framework kernel, carried with the EFE",
         "fw_iso": "framework kernel, isolated (its BEST case)",
         "share": "baryons + a cosmic-share halo (L41's B5)"}
info(f"    {'reading':<44} {'M_b/M_K':>8} {'M_hid [Msun]':>13} {'/CGM(132)':>10} {'/CGM(gen)':>10} {'<DM>':>7} "
     f"{'<N_H>/obs':>10} {'EM floor':>9}")
info("    " + "-"*115)
for k in ("newton", "fw", "fw_iso", "share"):
    f = REQ[k][1]
    mh = (f - 1.0)*MSTAR_GAL
    dm = mh*MSUN/(math.pi*(R_PAIR*kpc)**2)/(1.18*M_H)*1e-4/3.0857e18
    nh = mh*MSUN/(math.pi*(R_PAIR*kpc)**2)/(1.4*M_H)*1e-4
    emf = emission_measure(0.0, mh, R_PAIR)/emission_measure(1.5, M_hot_132, R_PAIR)
    info(f"    {SHORT[k]:<44} {f:8.2f} {mh:13.3e} {mh/M_det_132:9.1f}x {mh/M_gen:9.1f}x {dm:7.0f} "
         f"{nh/NH_obs:9.0f}x {emf:8.0f}x")
info("    " + "-"*115)
info(f"    measured for comparison: CGM(132 kpc) = {M_det_132:.2e} Msun, most generous reading "
     f"{M_gen:.2e}, DM_FG = {LIT['frb181112_DMlo']:.0f}-{LIT['frb181112_DMhi']:.0f} pc cm^-3,")
info(f"    <N_H> = {NH_obs:.1e} cm^-2.  EVERY reading fails EVERY local arm, including L41's own "
     f"cosmic-share reading, which is the smallest of the four.")
P("")
arms = {
  "budget (a)": M_REQ < share_moster,
  "radial distribution (b)": M_HID < M_det_132 + 3*e_sz_132,
  "dispersion measure (c)": DM_MIN < LIT["frb181112_DMhi"],
  "X-ray emission (c)": EM_floor < 4.0,
  "absorption column (c)": NH_MEAN < 3*NH_obs,
  "in-situ density (b)": n_req_48 < LIT["salem_n"] + 3*LIT["salem_en"],
  "global partition (c)": z_flim < 3.0,
  "Milky Way (b)": z_esc < 3.0,
}
info(f"    {'arm':<28} {'verdict':>9}   the number")
info(f"    {'-'*28} {'-'*9}   {'-'*70}")
DETAIL = {
  "budget (a)": f"{100*M_REQ/share_moster:.0f}% of the halo's whole cosmic baryon allotment on the generous "
                f"halo mass, {100*M_REQ/share_lo:.0f}% on the conservative one",
  "radial distribution (b)": f"{M_HID/M_det_132:.0f}x the summed measured CGM at 132 kpc; "
                             f"{M_HID/M_gen:.1f}x the most generous reading at 250 kpc",
  "dispersion measure (c)": f"{DM_at_b[0.0]:.0f} pc cm^-3 against a measured 50-120 at b = 29 kpc "
                            f"({DM_ratio:.1f}x); {DM_MIN:.0f} even for the family minimum",
  "X-ray emission (c)": f"{EM_ratio:.0f}x brighter than the detected hot halos at matched shape, "
                        f"{EM_floor:.0f}x even in the minimum-emission configuration",
  "absorption column (c)": f"mean N_H = {NH_MEAN:.1e} against COS-Halos' {NH_obs:.1e} cm^-2 "
                           f"({NH_MEAN/NH_obs:.0f}x), profile-free",
  "in-situ density (b)": f"{n_req_48:.1e} cm^-3 at 48 kpc against Salem+ 2015's {LIT['salem_n']:.1e} "
                         f"({n_req_48/LIT['salem_n']:.0f}x)",
  "global partition (c)": f"{frac_halo_req:.2f} +/- {e_frac:.2f} of all baryons against "
                          f"{allow_flim:.2f} +/- {LIT['flimflam_efigm']:.2f} (FLIMFLAM) and "
                          f"{allow_connor:.2f} +/- {LIT['connor_efigm']:.2f} (Connor+)",
  "Milky Way (b)": f"{esc_ratio:.1f}x Deason+ 2021's measured M(<100 kpc), {z_esc:.0f} sigma, both footings; "
                   f"{m_esc_low/LIT['deason_M100']:.1f}x / {z_esc_low:.0f} sigma on the fairer low-mass amplitude",
}
for k, v in arms.items():
    info(f"    {k:<28} {'PASS' if v else 'EXCLUDED':>9}   {DETAIL[k]}")
n_excl = sum(1 for v in arms.values() if not v)
check("E1 [VERDICT] the undetected-baryon escape survives the observational confrontation, i.e. L41's last "
      "door remains OPEN",
      n_excl == 0,
      f"{n_excl} of {len(arms)} arms EXCLUDE it, and they are independent probes of different physics: "
      f"UV absorption, X-ray emission, the thermal SZ, ram-pressure stripping, FRB dispersion, and the "
      f"Milky Way's own stellar-halo dynamics.  It survives only the TOTAL budget (at the ceiling) and the "
      f"global FRB partition (on the more permissive of two analyses).  The door is CLOSED")

P("")
P("-"*122)
P("  WHAT THIS DOES AND DOES NOT SAY, stated plainly:")
P("  1. This is a COST for the framework and NOT a result in its favour.  Had the escape survived, that would")
P("     also have been a cost -- a free function of host mass and environment, i.e. LambdaCDM's galaxy-")
P("     formation sector imported wholesale, exactly as L41 wrote.  There was no outcome here that was a win.")
P("  2. Nothing here constrains LambdaCDM.  LambdaCDM does not need the escape: its missing baryons are")
P("     EJECTED to large radii and to the IGM by feedback, which is what the FRB partition, the SZ profile")
P("     and the eROSITA extrapolation to ~3 R_vir all measure.  The framework needs them BOUND and INSIDE")
P("     132 kpc, and that is the specific thing the data exclude.")
P("  3. The framework's kernel passes the Milky Way's M(<100 kpc) on the DETECTED baryons at well under")
P("     1 sigma (C8).  That is a real success of the kernel and it is recorded as one -- but it is not a")
P("     discriminant, because a LambdaCDM halo fits the same number by construction.")
f_deep = mass_factor("fw_iso", 1.51, A0["canonical"], E_N["canonical"])
P("  4. Systematics that bound this, and they run the RIGHT way for the escape, so they are priced.  The pair")
P("     amplitudes are UPPER limits (L21's isolation-depth caveat: A falls 1.99 -> 1.51 as the isolation")
P("     deepens), so the required mass is an upper limit too.  Taking L21's own deepest-isolation A = 1.51")
P(f"     lowers the requirement to {f_deep:.1f}x the K-band mass ({(f_deep-1)*MSTAR_GAL:.2e} Msun), which is "
  f"still {(f_deep-1)*MSTAR_GAL/M_det_132:.0f}x the measured CGM at 132 kpc,")
P(f"     {(f_deep-1)*MSTAR_GAL/M_gen:.1f}x the most generous reading, and "
  f"{(f_deep-1)*MSTAR_GAL*MSUN/(math.pi*(R_PAIR*kpc)**2)/(1.18*M_H)*1e-4/3.0857e18:.0f} pc cm^-3 in mean")
P("     dispersion measure against a measured 50-120.  Even L21's most pessimistic amplitude does not reach")
P("     the observations.  Also priced: circular orbits are assumed, which is generous to the framework and")
P("     therefore generous to the escape; and the stellar mass uses Upsilon_K = 0.6 with no gas, so raising")
P("     the detected baryons by the ~15% a gas term adds moves nothing at these ratios.")
P("  5. The one phase not excluded by absorption, emission or dispersion -- cold dense molecular clumps with")
P("     a filling factor below ~1e-4 -- is closed by D1 instead, which is blind to phase and counts only")
P("     mass.  Naming the observation that WOULD find it, if anyone wants to reopen this: a stacked FRB")
P("     dispersion excess behind isolated L* galaxies at 100-150 kpc, at the ~10 pc cm^-3 level, which the")
P("     current samples do not yet reach.  That, not a theoretical argument, is what would move this verdict.")
P("-"*122)
P(f"\nRESULT: {len(FAILS)} FAIL" + (f" -> {FAILS}" if FAILS else ""))
sys.exit(0)
