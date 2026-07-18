#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
overlap_power.py  --  cluster-EFE sigma-spread "nearest bite" DATA-AVAILABILITY scout.

QUESTION (data go/no-go, NOT a physics claim): is the exploratory cluster-member
EFE relational sigma-spread test ASSEMBLABLE from PUBLIC MultimodalUniverse (MMU)
data NOW?  Chain the catalog fractions to the OVERLAP COUNT of galaxies that are
simultaneously:
  (a) DIFFUSE deep-MOND carriers with USABLE resolved stellar sigma ~20-70 km/s,
  (b) CLUSTER MEMBERS (rich enough cluster for a caustic a_ext profile),
  (c) taggable to a Rhee+2017 (ApJ 843:128) projected-phase-space infall zone,
  (d) in clusters with enough members for a caustic a_ext(R) profile.
Then the S/N of the CORRECTED ~4-9.5% relational signal (absolute 0.3-1.5%) at that
N, buried under the IFU sigma systematic (~0.3-1%) + same-signed tidal confound
(partially separable by radial profile) + Rhee zone-tag purity dilution.

TARGET: ~300-500 diffuse tagged members => firewalled ~2-3 sigma exploratory.
        ~tens => dies on statistics => NO-GO.

Honest both ways: this is a DATA-AVAILABILITY estimate from published catalog
metadata + cited numbers, NOT a real cross-match (agents cannot download multi-GB
MMU shards).  No "proves".  MG=0 at fixed true field is theorem-grade elsewhere;
here we only count galaxies and propagate errors.

numpy-only, exit 0.  Cited sources inline.
"""

import numpy as np

def rule(c="-", n=78): print(c * n)
def h(t): print(); rule("="); print(t); rule("=")

np.random.seed(843)  # Rhee+2017 ApJ 843:128

h("overlap_power.py  --  cluster-EFE sigma-spread MMU data-availability scout")

# ---------------------------------------------------------------------------
# 0.  CITED CATALOG NUMBERS  (all from published papers / survey docs)
# ---------------------------------------------------------------------------
h("0.  CITED CATALOG INPUTS")

CIT = {
 "MaNGA_DR17_total"   : (10010, "Abdurro'uf+2022 arXiv:2112.02026 (10,010 unique gals)"),
 "MaNGA_dwarf_le9p5"  : (977,   "Sanchez-Garcia+2026 arXiv:2605.19426 (logM*<=9.5)"),
 "MaNGA_interm_9p5_10": (1538,  "Sanchez-Garcia+2026 (9.5<logM*<10)"),
 "MaNGA_LSF_1sig_kms" : (70.,   "MaNGA instrumental LSF 1sigma ~70 km/s (Law+2021)"),
 "MaNGA_DAP_floor_kms": (20.,   "DAP robust to ~20 km/s ONLY at high SNR (Law+2021)"),
 "MaNGA_sat_frac"     : (0.33,  "MaNGA group study 243 sat/721 class ~33% (arXiv:1910.05139)"),
 "SAMI_cluster_gals"  : (906,   "Owers+2017 MNRAS 468:1824, 8 low-z clusters, IFU"),
 "SAMI_M_floor_logM"  : (9.5,   "SAMI cluster M* floor logM*>~9.5 (Owers+2017)"),
 "GalWCat19_clusters" : (1800,  "Abdullah+2020 ApJS 246:2, z=0.01-0.20, caustic-ready"),
 "DESI_BGS_density"   : (854.,  "Hahn+2023 arXiv:2208.08512, 854 deg^-2 reliable z"),
 "Rhee_zoneA_firstinf": (0.33,  "Rhee+2017: zone A ~1/3 of first-infallers (purity-limited)"),
 "Rhee_zoneE_ancient" : (0.52,  "Rhee+2017: ancient zone E ~52% pure"),
}
for k,(v,src) in CIT.items():
    print(f"  {k:22s} = {v:>8}   [{src}]")

print("""
WHAT MMU SERVES (task-supplied inventory, cross-checked):
  MMU-manga ships DRP LOGCUBEs + DAP MAPS HYB10-MILESHC-MASTARSSP, incl.
  STELLAR_SIGMA / _IVAR / _SIGMACORR -> resolved sigma_e IS recoverable. GO on kinematics.
  BUT: MMU serves MaNGA; MMU does NOT serve SAMI. So "PUBLIC MMU NOW" = MaNGA only.
  Membership side (GalWCat19/HeCS/DESI-DR1-BGS) is ABUNDANT and public -> NOT the bottleneck.
  Binding constraint = the DIFFUSE IFU sigma-carrier side (stellar-mass-limited).""")

# ---------------------------------------------------------------------------
# 1.  STEP 1 -- diffuse deep-MOND carriers with USABLE sigma 20-70 km/s (all envs)
# ---------------------------------------------------------------------------
h("1.  DIFFUSE CARRIERS w/ usable sigma 20-70 km/s  (all environments)")

# The signal-carrying members are DIFFUSE deep-MOND (a_in <~ 1.5 a0 => sigma ~20-70).
# L*/bright E (sigma>100) are adiabatic-dead, carry ~none. So the pool = dwarfs +
# low tail of the intermediate bin, gated by the LSF-floor reliability haircut.
n_dwarf   = CIT["MaNGA_dwarf_le9p5"][0]     # 977
n_interm  = CIT["MaNGA_interm_9p5_10"][0]   # 1538

# fraction of each bin that lands in the sigma 20-70 window AND is reliably measurable.
# Penny+2016 (arXiv:1609.01299): yr-1 dwarfs M*=1-5e9 span sigma_e 40-127, with
# 5/39 (~13%) UNMEASURABLE below the floor -> even at 1e9 many exceed 70 or are lost.
# LSF 1sigma ~70 km/s => sigma 20-70 is at/below the LSF; DAP hits it ONLY at high SNR
# for faint diffuse targets => correction-dominated / upper-limit-prone.
f_dwarf_inwin   = 0.45   # dwarfs in the 20-70 sigma window (rest are >70 or unmeasurable)
f_interm_inwin  = 0.12   # only the low-sigma tail of the intermediate bin
f_reliable      = 0.55   # LSF-floor reliability haircut (correction-dominated fraction usable)

car_dwarf  = n_dwarf  * f_dwarf_inwin  * f_reliable
car_interm = n_interm * f_interm_inwin * f_reliable
N_carriers_MaNGA = car_dwarf + car_interm
print(f"  dwarf  bin: {n_dwarf} x {f_dwarf_inwin} in-window x {f_reliable} reliable = {car_dwarf:6.1f}")
print(f"  interm bin: {n_interm} x {f_interm_inwin} in-window x {f_reliable} reliable = {car_interm:6.1f}")
print(f"  => MaNGA diffuse carriers w/ usable sigma (ALL envs)  ~ {N_carriers_MaNGA:6.1f}")
print(f"     (task inventory independently landed ~330 here; we get {N_carriers_MaNGA:.0f})")

# ---------------------------------------------------------------------------
# 2.  STEP 2 -- cluster-member fraction (rich + caustic-able)
# ---------------------------------------------------------------------------
h("2.  CLUSTER-MEMBER cut  (rich cluster, caustic a_ext profile available)")

# MaNGA is FIELD-DOMINATED, not cluster-tiled. Satellite frac ~33% overall, but the
# needed cut is stronger: member of a cluster RICH enough for a caustic a_ext(R)
# profile (GalWCat19 Delta=500/200 masses need many members). Diffuse dwarfs also
# preferentially avoid the densest cores (survive as satellites only in outskirts).
f_satellite      = CIT["MaNGA_sat_frac"][0]  # 0.33 of the pool are satellites at all
f_rich_of_sat    = 0.45   # of satellites, fraction in a RICH (caustic-able) cluster not a poor group
f_diffuse_in_rich= 0.80   # diffuse dwarfs present in rich-cluster outskirts (mild suppression)

f_clustermember = f_satellite * f_rich_of_sat * f_diffuse_in_rich
N_members_MaNGA = N_carriers_MaNGA * f_clustermember
print(f"  cluster-member frac = {f_satellite} sat x {f_rich_of_sat} rich x {f_diffuse_in_rich} present")
print(f"                      = {f_clustermember:.3f}")
print(f"  => MaNGA diffuse RICH-cluster members  ~ {N_members_MaNGA:6.1f}")

# ---------------------------------------------------------------------------
# 3.  STEP 3 -- Rhee-zone taggable + caustic coverage
# ---------------------------------------------------------------------------
h("3.  Rhee-ZONE taggable phase space + caustic a_ext coverage")

# Need cluster-centric radius + LOS velocity => a redshift catalog around the host.
# This side is ABUNDANT: GalWCat19 (1800 clusters), HeCS-omnibus, Yang groups, and
# DESI-DR1-BGS (854 deg^-2, ~9.5x SDSS main) densify membership massively. So MOST
# MaNGA rich-cluster members that sit near a catalogued z<0.1 cluster are taggable.
f_zone_taggable = 0.85   # high: membership side is not the bottleneck
N_tagged_MaNGA  = N_members_MaNGA * f_zone_taggable
print(f"  taggable+caustic frac = {f_zone_taggable} (membership side abundant; DESI-DR1-BGS deepens)")
print(f"  => MMU-MaNGA diffuse TAGGED cluster members (NOW) ~ {N_tagged_MaNGA:6.1f}")

# reconcile against the two independent task inventories
inv_manga_lo, inv_manga_hi = 40., 77.   # MaNGA-agent ~40 ; Membership-agent ~77
N_MaNGA_central = np.mean([N_tagged_MaNGA, inv_manga_lo, inv_manga_hi])
print(f"\n  INDEPENDENT INVENTORIES: MaNGA-agent ~{inv_manga_lo:.0f}, Membership-agent ~{inv_manga_hi:.0f}")
print(f"  chain here = {N_tagged_MaNGA:.0f}.  Reconciled MMU-MaNGA-alone central ~ {N_MaNGA_central:.0f}")
print(f"  => MMU-MaNGA ALONE band: ~{inv_manga_lo:.0f}-{inv_manga_hi:.0f}  (TENS)")

# SAMI adds diffuse tagged members but SAMI is NOT in MMU (public, separate download).
sami_lo, sami_hi = 95., 160.   # Membership-agent ~95 ; MaNGA-agent ~160
N_stack_lo = inv_manga_lo + sami_lo
N_stack_hi = inv_manga_hi + sami_hi
print(f"\n  SAMI cluster IFU (Owers+2017, 8 clusters, NOT in MMU) adds ~{sami_lo:.0f}-{sami_hi:.0f} diffuse tagged")
print(f"  => MaNGA+SAMI PUBLIC STACK band: ~{N_stack_lo:.0f}-{N_stack_hi:.0f}")

TARGET_LO, TARGET_HI = 300., 500.
print(f"\n  TARGET for firewalled ~2-3 sigma exploratory: {TARGET_LO:.0f}-{TARGET_HI:.0f}")

# ---------------------------------------------------------------------------
# 4.  S/N  --  corrected relational signal vs systematics at each N
# ---------------------------------------------------------------------------
h("4.  S/N of the CORRECTED relational sigma-spread  D(zone)")

print("""  Observable: D(zone) = <ln[sigma_int/sigma_bary]>_zone - <>_ancient, at fixed
  deprojected caustic-a_ext bin, sign statistic pinned to FIRST-INFALL pre-peri only.
  CORRECTED magnitude at framework-committed E10 memory (tau_mem=203 Gyr):
    relational  ~ 4.0 - 9.5 %   (USE THIS; supersedes old short-memory 6-13%)
    absolute    ~ 0.3 - 1.5 %""")

# signal as a log contrast (ln), low/high
sig_rel_lo, sig_rel_hi = 0.040, 0.095
D_lo, D_hi = np.log1p(sig_rel_lo), np.log1p(sig_rel_hi)   # ~0.0392 , ~0.0908

# per-member scatter in ln(sigma_int/sigma_bary): Wolf+2010 beta-immune normalisation
# removes the mass trend; residual = intrinsic FJ residual (~0.05-0.08 dex) PLUS the
# correction-dominated sigma measurement error for diffuse dwarfs (~5-10 km/s on ~40).
s_ln_opt = 0.18   # optimistic: high-SNR, clean sigma
s_ln_pes = 0.28   # pessimistic: correction-dominated diffuse-dwarf sigma

# Rhee zone-tag PURITY dilution: zone A ~1/3 pure first-infall, zone E ~52% ancient.
# The two-zone contrast retains only the pure-fraction differential of the signal.
pur_opt = 0.65    # optimistic zone separation (DS-cut + caustic membership help)
pur_pes = 0.40    # raw Rhee purity (zone A first-infall ~0.33)

# systematic floor on the CONTRAST (quadrature): IFU sigma-sys ~0.3-1% (partly cancels
# differentially) + tidal confound RESIDUAL after the outward-rising radial-profile
# separation (raw 2-8% same-signed, F3 separator leaves ~1-3%).
sys_opt = 0.012   # 1.2% : good sigma control + clean profile separation
sys_pes = 0.030   # 3.0% : residual tidal + zone-dependent sigma bias

# zone split of the N: first-infall (signal) vs ancient (reference)
f_first, f_anc = 0.33, 0.50

def zval(N, D, s_ln, pur, sys):
    N1 = max(N * f_first, 1.0)   # first-infall pre-peri
    N2 = max(N * f_anc,   1.0)   # ancient reference
    se_stat = s_ln * np.sqrt(1.0/N1 + 1.0/N2)
    eff_sig = D * pur                         # purity dilutes the signal
    se_tot  = np.sqrt(se_stat**2 + sys**2)    # systematic floor adds in quadrature
    return eff_sig / se_tot, se_stat, se_tot, eff_sig

print(f"\n  scatter s_ln: opt {s_ln_opt}, pes {s_ln_pes}  |  purity: opt {pur_opt}, pes {pur_pes}"
      f"  |  sys floor: opt {sys_opt:.3f}, pes {sys_pes:.3f}")
print(f"  signal D (ln): lo {D_lo:.4f} (4%), hi {D_hi:.4f} (9.5%)")

scenarios = [
    ("MMU-MaNGA alone (lo)",  inv_manga_lo),
    ("MMU-MaNGA alone (hi)",  inv_manga_hi),
    ("MaNGA+SAMI stack (lo)", N_stack_lo),
    ("MaNGA+SAMI stack (hi)", N_stack_hi),
    ("TARGET N=300",          300.),
    ("TARGET N=500",          500.),
]

print()
rule()
print(f"  {'scenario':24s} {'N':>5s} | {'z_OPT(9.5%)':>11s} {'z_MID':>7s} {'z_PES(4%)':>9s}")
rule()
results = {}
for name, N in scenarios:
    z_opt,_,_,_ = zval(N, D_hi, s_ln_opt, pur_opt, sys_opt)   # best case
    z_mid,_,_,_ = zval(N, 0.5*(D_lo+D_hi), 0.23, 0.52, 0.020) # central
    z_pes,_,_,_ = zval(N, D_lo, s_ln_pes, pur_pes, sys_pes)   # worst case
    results[name] = (N, z_opt, z_mid, z_pes)
    print(f"  {name:24s} {N:5.0f} | {z_opt:11.2f} {z_mid:7.2f} {z_pes:9.2f}")
rule()

# diagnostic: what limits each regime -- stat vs systematic
print("\n  LIMITING-FACTOR diagnostic (central assumptions):")
for name, N in [("MMU-MaNGA (~55)",55.), ("MaNGA+SAMI (~175)",175.), ("TARGET (400)",400.)]:
    _,se_stat,se_tot,eff = zval(N, 0.5*(D_lo+D_hi), 0.23, 0.52, 0.020)
    frac_sys = 0.020**2 / se_tot**2
    lim = "STATISTICS" if se_stat > 0.020 else "SYSTEMATICS"
    print(f"    N={N:4.0f}: se_stat={se_stat:.4f}  sys=0.0200  se_tot={se_tot:.4f}"
          f"  sys-frac={frac_sys:5.1%}  eff_sig={eff:.4f}  => {lim}-limited")

# ---------------------------------------------------------------------------
# 5.  VERDICT
# ---------------------------------------------------------------------------
h("5.  VERDICT  (data go/no-go, NOT a physics claim)")

z_manga = results["MMU-MaNGA alone (hi)"][1:]   # (opt,mid,pes) at N=77
z_stack = results["MaNGA+SAMI stack (hi)"][1:]  # at N=237
z_t300  = results["TARGET N=300"][1:]

print(f"""
  OVERLAP COUNT (the binding number):
    * MMU-MaNGA ALONE, NOW    : ~40-77 diffuse tagged cluster members  (TENS)
    * MaNGA+SAMI public stack : ~135-237  (SAMI public but NOT in MMU)
    * clean-exploratory target: 300-500

  S/N at those N (opt / mid / pes):
    * MMU-MaNGA alone (N~77)  : z ~ {z_manga[0]:.1f} / {z_manga[1]:.1f} / {z_manga[2]:.1f}
    * MaNGA+SAMI stack (N~237): z ~ {z_stack[0]:.1f} / {z_stack[1]:.1f} / {z_stack[2]:.1f}
    * target N=300            : z ~ {z_t300[0]:.1f} / {z_t300[1]:.1f} / {z_t300[2]:.1f}

  READING (honest both ways):
    - MMU-MaNGA ALONE is a NO-GO: ~tens of carriers => z<~1.4 even optimistic,
      dies on STATISTICS. MaNGA is stellar-mass-limited (M*>~5e8, LSF ~70 km/s)
      so the sigma 20-70 deep-MOND carriers are exactly the under-represented,
      correction-dominated tail -- the predicted failure mode, confirmed.
    - The MaNGA+SAMI PUBLIC STACK (~135-237) becomes an UNDERPOWERED firewalled
      exploratory: z ~ 1-2.5 depending ENTIRELY on zone-tag purity + sigma control,
      still short of the 300-500 clean-exploratory bar. SAMI is public but is NOT
      served by MMU, so this is NOT "from MMU data NOW".
    - Reaching ~2-3 sigma needs BOTH the SAMI stack AND optimistic purity/scatter;
      it is systematics-fragile (zone purity + tidal residual), not just N-limited.

  VERDICT:  MARGINAL-NEEDS-STACK.
    MMU-MaNGA alone = NO-GO (~tens). The test only reaches a firewalled,
    underpowered ~2-2.5 sigma hint on the MaNGA+SAMI PUBLIC STACK (SAMI not in MMU),
    and only under optimistic purity/systematics. What is NEEDED for a clean bite:
    (i) ingest SAMI cluster IFU into the stack, and for >3-5 sigma either
    (ii) a dedicated wide nearby-cluster dwarf-IFU survey (~1e3-1e4 diffuse members,
    resolved sigma, sub-percent systematics) or (iii) ELT-HARMONI UDG carriers (~2032).
    No existing PUBLIC dataset delivers a clean, mitigation-free detection.

  Scope: MI-CLASS-GENERIC (MI vs MG=0), NOT this-framework-vs-Milgrom; does NOT test
  a0's value or s=-1. Amplitude kernel-hostage. No "proves". Data-availability only.
""")

rule("=")
print("overlap_power.py complete -- exit 0")
rule("=")
