#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
reachability_gonogo.py -- SURVEY REACHABILITY + HONEST GO/NO-GO for the cluster-member
EFE relational sigma-spread discriminator (MI-class vs MG=0), the paper's ONE
genuinely-MG-impossible handle.  ARMS (does NOT relitigate) MI_SIGMA_SPREAD_2026.md
(Zenodo 21421896).  numpy-only, exit 0.  2026-07-23.
================================================================================================
WHAT THIS ADDS over the banked overlap_power.py / inventory_*.py (which are correct but
partial):  overlap_power.py propagated a 4-9.5% signal -- that is effectively the PURE-DELAY
kernel corner.  The published paper's HONEST magnitude is a KERNEL-HOSTAGE BAND with a
LOW-PASS floor at ~1.3-1.5% that sits AT OR BELOW the confound floors.  Per the calibration
rule "a manufactured win and a manufactured deficit are penalised EQUALLY", this script
carries the FULL band and reports detectability SEPARATELY for the two kernel readings, and
broadens the dataset census to every EXISTING resolved-sigma + phase-space-taggable diffuse
cluster-dwarf survey (not just MaNGA/SAMI).

GIVENS FROM THE PAPER (do NOT re-derive; Sec. 4.2, 4.4, 5.4, 6.2):
  * observable  D(zone) = <ln(sigma_int/sigma_bary)>_zone - <>_ancient, at fixed deprojected
    caustic a_ext bin, sign statistic pinned to the FIRST-INFALL pre-pericentre zone only.
  * MG field sector: D=0 EXACTLY (theorem, any a0, any interpolation, both footings, off-adiab).
  * MI signal magnitude at the framework-committed E10 memory (tau_mem=2Z/H_Lambda=203/168 Gyr):
      LOW-PASS reading   : D_firstinfall ~ +1.3% (canonical) / +1.5% (alt)   <-- the honest floor
      PURE-DELAY |K|=1   : D_firstinfall ~ +8 to +13%                         <-- the high corner
    genuinely UNCOMPUTED between these WITHIN the committed kernel.  Both share the SIGN.
  * confound floors (irreducible systematics, NOT beaten by N):
      projection alias (observable's own) : ~1-2% (up to ~7% filamentary/triaxial)
      same-signed tidal/environmental     : ~2-8% raw; F3 outward-rising radial separator
                                            leaves a residual ~1-3% (clean low-tidal sample)
  * a0 CANCELS at fixed dimensionless depth y (both footings within <20% on N_3sigma); the
    signal does NOT test a0's value or the sign postulate s=-1.
  * MI-CLASS-GENERIC: separates history-dependent inertia from MG(=0); does NOT separate THIS
    framework from Milgrom's linear no-EFE MI (2503.07106), which also spreads.

CREDIT: Milgrom 1983 (MOND) / 1999 PLA 253:273 (nu-kernel wellhead) / 2022 PRD 106 064060
(two-frequency EFE) / 2503.07106 (linear MI, also spreads).  Cluster/IFU census cited inline.
"""
import numpy as np

LINE = "=" * 100
def h(t): print(); print(LINE); print(t); print(LINE)

# ================================================================ 0.  MAGNITUDE + FLOOR CONSTANTS (from paper)
A0_CAN, A0_ALT = 9.36e-11, 1.13e-10
# D(first-infall) ABSOLUTE ln-contrast, per kernel reading (paper Sec 4.2 / 5.4):
D_LOWPASS = {"canonical": 0.013, "alternate": 0.015}     # the honest low-pass floor
D_PUREDELAY = (0.08, 0.13)                                # the |K|=1 high corner band
# confound floors on the D(zone) contrast (paper Sec 4.4):
FLOOR_PROJ = (0.010, 0.020)      # observable's own projection alias (isotropic); up to 0.07 filamentary
FLOOR_PROJ_FILAMENT = 0.07
FLOOR_TIDAL_RAW = (0.02, 0.08)   # same-signed tidal/environmental, raw
FLOOR_TIDAL_RESID = (0.010, 0.030)  # residual AFTER the F3 outward-rising radial-profile separator

h(" 0.  THE KERNEL-HOSTAGE SIGNAL vs THE CONFOUND FLOORS  (both readings, carried at full weight)")
print(f"  D(first-infall) signal, LOW-PASS   : {D_LOWPASS['canonical']*100:.1f}% (canon) / {D_LOWPASS['alternate']*100:.1f}% (alt)")
print(f"  D(first-infall) signal, PURE-DELAY : {D_PUREDELAY[0]*100:.0f}-{D_PUREDELAY[1]*100:.0f}%")
print(f"  projection floor (own)             : {FLOOR_PROJ[0]*100:.0f}-{FLOOR_PROJ[1]*100:.0f}%  (up to {FLOOR_PROJ_FILAMENT*100:.0f}% filamentary/triaxial)")
print(f"  tidal floor, raw                   : {FLOOR_TIDAL_RAW[0]*100:.0f}-{FLOOR_TIDAL_RAW[1]*100:.0f}%")
print(f"  tidal floor, residual after F3     : {FLOOR_TIDAL_RESID[0]*100:.0f}-{FLOOR_TIDAL_RESID[1]*100:.0f}%  (clean low-tidal sample)")
print()
print("  IMMEDIATE READING (independent of ANY dataset -- this is a FLOOR fact, not an N fact):")
lp_vs_floor = D_LOWPASS["canonical"] / np.mean(FLOOR_TIDAL_RESID)
pd_vs_floor = np.mean(D_PUREDELAY) / np.mean(FLOOR_TIDAL_RESID)
print(f"   * LOW-PASS  signal 1.3-1.5%  <=  projection 1-2% AND <= residual-tidal 1-3%  ->"
      f" signal/floor ~ {lp_vs_floor:.1f}  => BURIED. No N clears it; it is a FLOOR NO-GO.")
print(f"   * PURE-DELAY signal 8-13%     >  residual-tidal 1-3% (and >> projection)      ->"
      f" signal/floor ~ {pd_vs_floor:.1f}  => CLEARS the floor; becomes an N (statistics) problem.")
assert D_LOWPASS["canonical"] <= FLOOR_PROJ[1] and D_LOWPASS["canonical"] <= FLOOR_TIDAL_RESID[1], \
    "low-pass must sit at/below the floors (the honest deficit-side of the ledger)"
assert D_PUREDELAY[0] > FLOOR_TIDAL_RESID[1], \
    "pure-delay must clear the residual-tidal floor (the honest win-side of the ledger)"

# ================================================================ 1.  EXISTING-DATASET CENSUS (cited)
h(" 1.  EXISTING-DATASET REACHABILITY CENSUS -- resolved internal sigma + phase-space tag for DIFFUSE carriers")
print("""  CARRIER definition: DIFFUSE deep-MOND members, a_in<~1.5 a0 => stellar sigma ~20-70 km/s.
  Bright E/L* (sigma>100) are adiabatically DEAD (y>>1, f tiny) -- NOT carriers.  Each dataset is
  scored on: N_diffuse_tagged (diffuse carrier AND in a caustic-able cluster AND Rhee-taggable AND
  reliable resolved sigma), per-galaxy sigma precision, and whether phase-space tagging exists.
""")
# (name, N_diffuse_tagged_lo, hi, sigma_precision, environment/phase-tag note, cite)
DATASETS = [
    ("MaNGA DR17 (MMU-served)", 40, 77, "5-15% (LSF 1sig~70; DAP floor ~20 @ high S/N)",
     "FIELD-dominated; few rich-cluster dwarfs; phase-tag via GalWCat19/DESI",
     "Abdurrouf+2022; Law+2021; Sanchez-Garcia+2026"),
    ("SAMI cluster (Owers+2017)", 95, 160, "5-12% (R~4500)",
     "8 low-z clusters, membership+R200+caustic BUILT-IN (Rhee-ready); M* floor logM~9.5",
     "Owers+2017 MNRAS 468:1824"),
    ("SAMI-Fornax Dwarfs (Scott+2020/Eftekhari+2022)", 20, 31, "~3-8 km/s (deep IFU on dEs)",
     "ONE cluster (Fornax); 31 dEs 1e7.5-1e9.5; all members, PS known; sigma 20-50",
     "Scott+2020 MNRAS 497:1571; Eftekhari+2022"),
    ("SMAKCED Virgo dEs (Toloba+2014)", 25, 39, "~2-10 km/s (long-slit sigma profiles)",
     "ONE cluster (Virgo); 39 dEs Mr -19..-16; members, PS known; sigma 20-60",
     "Toloba+2014 ApJ 783:120 / ApJS 215:17"),
    ("Fornax3D dwarf overlap (Sarzi+2018)", 3, 5, "~5-15 km/s (mag-limited, bright-dominated)",
     "Fornax; only ~5 dwarf-E overlap SAMI-Fornax; 21/33 have resolved sigma but mostly bright",
     "Sarzi+2018 A&A 616:A121; Iodice+2019"),
    ("MATLAS dwarfs w/ MUSE (Heesters+2023)", 0, 5, "v_rad only; sigma mostly UPPER LIMITS",
     "GROUP/FIELD (nearby-ETG satellites), NOT rich clusters -> environment-DISQUALIFIED",
     "Heesters+2023 A&A 676:A33 (56 dwarfs, v_rad + pops)"),
    ("Coma MUSE/Subaru dwarf spectroscopy", 10, 30, "correction-dominated (d~100 Mpc; sigma~20-40 hard)",
     "ONE cluster (Coma); rich, well-mapped PS; but resolved sigma on faint dwarfs marginal",
     "e.g. deep Coma dwarf programs; upper-limit-prone"),
]
print(f"  {'dataset':46s} {'N_diffuse_tagged':>16s}  {'sigma precision':>34s}")
for nm, lo, hi, prec, env, cite in DATASETS:
    print(f"  {nm:46s} {f'~{lo}-{hi}':>16s}  {prec:>34s}")
    print(f"    env/tag: {env}")
    print(f"    cite   : {cite}")

# public-stack total of GENUINE diffuse tagged carriers (exclude MATLAS: wrong environment)
stack_lo = sum(lo for nm, lo, hi, *_ in DATASETS if "MATLAS" not in nm)
stack_hi = sum(hi for nm, lo, hi, *_ in DATASETS if "MATLAS" not in nm)
print(f"\n  ==> TOTAL EXISTING PUBLIC diffuse tagged carriers, ALL surveys stacked: ~{stack_lo}-{stack_hi}")
print("      (spread across Virgo, Fornax, Coma + 8 SAMI clusters + scattered MaNGA fields;")
print("       heterogeneous sigma pipelines + zero-points are themselves a stacking systematic.)")
print("  ==> membership/phase-space SCAFFOLDING is ABUNDANT and NOT the wall (GalWCat19 1800 cl,")
print("      HeCS-omnibus, Rhee+2017 zones, DESI-DR1-BGS ~9.5x deepening). The wall is CARRIER COUNT.")

# ================================================================ 2.  POWER MODEL (two-zone contrast)
h(" 2.  POWER MODEL -- two-zone D(zone) contrast, systematic floor added in quadrature")
# first-infall vs ancient zone split of N; purity dilutes the signal; residual-tidal is the floor.
F_FIRST, F_ANC = 0.33, 0.50           # Rhee zone fractions (paper Sec 4)
def z_of(N, D_signal, s_ln, purity, sys_floor):
    N1, N2 = max(N * F_FIRST, 1.0), max(N * F_ANC, 1.0)
    se_stat = s_ln * np.sqrt(1.0 / N1 + 1.0 / N2)
    se_tot = np.hypot(se_stat, sys_floor)        # systematic floor is irreducible in N
    return (D_signal * purity) / se_tot, se_stat
def N_for_z3(D_signal, s_ln, purity, sys_floor, cap=1e7):
    # smallest N reaching z=3, or 'inf' if the systematic floor alone caps z<3
    eff = D_signal * purity
    if eff / sys_floor < 3.0:                     # floor-limited: no N works
        return np.inf
    need_se_stat = np.sqrt((eff / 3.0) ** 2 - sys_floor ** 2)
    # se_stat = s_ln*sqrt(1/(N*F_FIRST)+1/(N*F_ANC)) -> solve for N
    return s_ln ** 2 * (1 / F_FIRST + 1 / F_ANC) / need_se_stat ** 2

# fiducial per-member scatter + purity + residual-tidal floor (central; carried opt/pes below)
S_LN = 0.20         # per-member ln(sigma_int/sigma_bary) scatter (FJ residual + diffuse-dwarf sigma err)
PURITY = 0.52       # Rhee two-zone purity after DS-cut + caustic membership
SYS = 0.020         # residual-tidal + zone-dependent sigma-bias floor after F3 (central)
print(f"  fiducial: per-member scatter s_ln={S_LN}, zone purity={PURITY}, residual systematic floor={SYS*100:.1f}%")
print(f"  (opt: s_ln=0.18, purity=0.65, sys=0.012 ;  pes: s_ln=0.28, purity=0.40, sys=0.030)")

# ================================================================ 3.  DETECTABILITY, SPLIT BY KERNEL READING
h(" 3.  DETECTABILITY AT THE BEST REAL DATASET -- SPLIT BY KERNEL READING (the calibration-rule #1 crux)")
STACKS = [
    ("MaNGA alone (MMU now)", 77),
    ("MaNGA+SAMI-cluster", 237),
    ("+SAMI-Fornax+SMAKCED (Virgo+Fornax dEs)", 307),
    ("ALL public IFU stacked (max)", stack_hi),
    ("dedicated dwarf-IFU survey (future)", 3000),
]
for reading, Dsig, tag in [("LOW-PASS  (D=1.3%)", D_LOWPASS["canonical"], "honest floor"),
                            ("PURE-DELAY (D=10%)", 0.10, "high corner")]:
    print(f"\n  --- {reading}  [{tag}] ---")
    print(f"   {'sample':44s} {'N':>6s} {'z_opt':>7s} {'z_mid':>7s} {'z_pes':>7s} {'N_for_3sig(mid)':>16s}")
    for nm, N in STACKS:
        z_opt, _ = z_of(N, Dsig, 0.18, 0.65, 0.012)
        z_mid, _ = z_of(N, Dsig, S_LN, PURITY, SYS)
        z_pes, _ = z_of(N, Dsig, 0.28, 0.40, 0.030)
        n3 = N_for_z3(Dsig, S_LN, PURITY, SYS)
        n3s = "FLOOR-CAPPED" if not np.isfinite(n3) else f"{n3:,.0f}"
        print(f"   {nm:44s} {N:6d} {z_opt:7.2f} {z_mid:7.2f} {z_pes:7.2f} {n3s:>16s}")

# the two decisive facts
h(" 4.  THE TWO DECISIVE FACTS")
n3_lp = N_for_z3(D_LOWPASS["canonical"], S_LN, PURITY, SYS)
n3_pd = N_for_z3(0.10, S_LN, PURITY, SYS)
n3_pd_opt = N_for_z3(0.10, 0.18, 0.65, 0.012)
print(f"""  (A) LOW-PASS reading is a FLOOR NO-GO, independent of dataset size.
      The 1.3-1.5% signal, diluted by zone purity to ~0.7%, sits UNDER even the optimistic
      1.2% residual-tidal floor: eff_sig/floor = {D_LOWPASS['canonical']*0.52/0.012:.1f} < 3.  N_for_3sigma = {'INFINITE (floor-capped)' if not np.isfinite(n3_lp) else f'{n3_lp:,.0f}'}.
      No existing OR future dataset detects the low-pass corner unless the tidal systematic is
      pushed BELOW ~0.3% -- which no cluster-dwarf programme can currently promise. This is the
      honest deficit side: if the framework's committed kernel reads low-pass, the discriminator
      is UNDETECTABLE in principle on this observable, not merely underpowered.

  (B) PURE-DELAY reading clears the floor ONLY under optimistic systematics -- and EXISTING data
      still miss even then.  The RAW 8-13% signal clears the 1-3% residual-tidal floor, BUT zone
      purity dilutes it to ~5% and the CENTRAL 2% residual-tidal floor then caps z at ~2.6 for ANY
      N: N_for_3sigma (central) = {('FLOOR-CAPPED (inf)' if not np.isfinite(n3_pd) else f'{n3_pd:,.0f}')}.  It becomes genuinely N-limited only in the
      OPTIMISTIC corner (sub-1.2% tidal control + 0.65 purity), where N_for_3sigma = {n3_pd_opt:,.0f}.
      EXISTING public stack tops out at ~{stack_hi} carriers across all surveys -> z ~ 1.6 (mid) to
      2.6 (opt), an underpowered, systematics-fragile HINT, not a 3-sigma detection.  And that ~{stack_hi}
      assumes a clean heterogeneous-pipeline stack of Virgo+Fornax+Coma+SAMI+MaNGA dwarfs with
      matched sigma zero-points -- itself optimistic.  So even the pure-delay GO demands BOTH a
      future N~500-1000+ carrier sample AND sub-percent tidal systematics simultaneously.""")

# ================================================================ 5.  GO/NO-GO VERDICT
h(" 5.  HONEST GO/NO-GO VERDICT  (both footings; MI-class-generic; a0-value-blind)")
print(f"""  VERDICT:  NO-GO on ALL currently-existing datasets, for BOTH kernel readings, for different reasons:

    * LOW-PASS corner  : NO-GO by FLOOR (signal <= confound floor).  Un-reachable by ANY N, present
                         or future, on this observable -- a future facility does NOT fix a floor NO-GO.
    * PURE-DELAY corner: NO-GO on existing data.  At CENTRAL 2% tidal systematics it is ALSO
                         floor-capped (purity dilutes 10%->5%, z caps ~2.6); it turns N-limited only
                         with sub-1.2% tidal control, needing ~{n3_pd_opt:,.0f} carriers vs the ~{stack_lo}-{stack_hi} public.
                         Existing stack = z~1.6-2.6 firewalled hint only.

  SINGLE MOST-REALISTIC KILL-OR-CONFIRM TARGET (named, candid):
    A DEDICATED WIDE NEARBY-CLUSTER DWARF-IFU SURVEY -- push the M* floor to logM~8, reliable
    resolved stellar sigma well below 45 km/s, sub-percent sigma systematics, ~1e3-1e4 diffuse
    members across Virgo+Fornax+Coma+Hydra+Centaurus with clean first-infall/ancient Rhee tags
    and a LOW-TIDAL selection.  Nearest-term instrument that could deliver it: the HECTOR cluster
    survey (Bryant+; large multiplex IFU) stacked with a MUSE/WEAVE dwarf-cluster large programme;
    a clean >=3-sigma bite otherwise waits on ELT-HARMONI resolved cluster-dwarf sigma (~2032).

    CANDID BOTTOM LINE: NOT YET REACHABLE with present instruments/datasets.  The scaffolding
    (membership, caustics, Rhee zones) is ready and would slot straight in, but the diffuse
    IFU sigma-carrier count (~hundreds public, needs ~1e3-1e4) AND the sub-percent tidal control
    are both missing -- and even the future GO exists ONLY IF the committed kernel reads
    pure-delay; if it reads low-pass, this observable is a floor NO-GO regardless of facility.

  CAVEAT CARRIED (unchanged from the paper): a DETECTION would be MI-CLASS-GENERIC -- it separates
    history-dependent inertia from the MG(=0) field-sector class (theorem-grade), but does NOT
    isolate THIS de Sitter-Unruh framework from Milgrom's linear no-EFE MI (2503.07106), which also
    spreads.  It does NOT test a0's value (cancels at fixed depth, both footings) or the sign s=-1.""")

# guardrails: the verdict must be internally consistent with the paper
assert not np.isfinite(n3_lp), "low-pass MUST be floor-capped (paper Sec 4.4)"
assert n3_pd > stack_hi, "pure-delay N_3sigma must exceed the existing public stack (underpowered)"
assert stack_hi < 500, "existing public diffuse tagged carrier stack must be sub-500 (the wall)"
print("\n EXIT 0 = full kernel band carried; low-pass=floor NO-GO, pure-delay=statistics NO-GO on existing")
print("          data; single realistic target = dedicated dwarf-IFU cluster survey / ELT-HARMONI ~2032.")
