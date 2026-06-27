#!/usr/bin/env python3
"""
THE EXTRA-CRISPY FALSIFICATION SCORECARD (honest, both-ways).
Carl asked for 'honest fried chicken, extra crispy' -- i.e. the SHARPEST possible statement of where the
de Sitter-Unruh modified-inertia framework lives or dies, and how soon. NOT a TOE (the SM is walled; Carl
retracted the TOE overclaim). This ranks the framework's REAL falsifiable predictions by 'crunch' =
distinctiveness x decidability x near-term, brutally honest about the gradient. Every number is from a
committed script or a published bound. Footing a0=9.36e-11, Z=sqrt(32pi/3), preferred frame = CMB apex.
"""
import math

# ---- the real numbers (each traceable to a committed script / published bound) ----
v_apex   = 369.82e3                       # CMB-apex speed, m/s (Planck)
beta     = v_apex/2.99792458e8            # 1.2336e-3
sTX      = 8.68e-10                        # reviews/stx_target.py
sTX_bnd  = 1.3e-9                          # Hees+ 2015 ephemeris bound
a0z_lo, a0z_hi = 0.61, 0.75               # a0(z=3)/a0(0), DESI w0wa propagation (a0z_desi_chains_propagation.py)
Sig_eff_lo, Sig_eff_hi = 0.032, 0.042     # eV, growing-nu CMB-vs-today (nu_mass_cmb_vs_today_offset.py)
dwarf_MI_lo, dwarf_MI_hi = 0.06, 0.13     # relational sigma-spread, MI (MG = exactly 0)
cassini_margin_orders = 5.5                # framework PASSES |gamma-1|<2.3e-5 by ~5.5 orders (MI-vs-MG discriminator)

ROWS = [
 # rank, name, the sharp number, distinctive?, data status, decision window, crunch, honest caveat
 ("1 (crunchiest)","s^TX boost-dipole @ CMB apex",
   f"{sTX:.1e}, CPT-even, FIXED dir (l,b)=(264,48); {sTX_bnd/sTX:.2f}x under bound",
   "YES -- MI preferred-frame; sign+direction MG-different","INPOP+Cassini+BepiColombo IN HAND",
   "dedicated fit sigma~4e-10, ~2026-2028","EXTRA CRISPY",
   "magnitude framework-specific +-O(1); gravity-sector only"),
 ("2","ZERO GW birefringence + c_T=1 exactly",
   "EXACTLY 0 (CPT-even theorem); d=4 dispersion = 0",
   "YES -- exact structural prediction","LIGO/Virgo/KAGRA, LISA",
   "a CONFIRMED birefringence = instant kill","CRISPY KILL-SWITCH",
   "current anisotropy floor ~1e-14 is above the dipole; the ZERO is the clean falsifier"),
 ("3","a0(z) declines as sqrt(rho_DE)",
   f"a0(z=3)/a0(0) = {a0z_lo:.2f}-{a0z_hi:.2f}  (vs 1.0 constant, vs ~4.6 rising)",
   "YES -- distinct from constant AND rising","DESI w(z) + high-z RAR (ELT/JWST/ALMA)",
   "DESI DR3 + high-z RAR, ~2027-2030","CRISPY but HOSTAGE",
   "DIES if DESI converges to w=-1 (degenerates to plain MOND)"),
 ("4","growing nu mass -> DESI Sigma_m_nu anomaly",
   f"CMB-imprinted Sigma_eff = {Sig_eff_lo:.3f}-{Sig_eff_hi:.3f} eV (right-signed, below floor)",
   "PARTIAL -- overlaps 'dynamical DE mimics neg mass'","CMB-S4 + DESI-DR3/Euclid growth",
   "~2027-2030","MEDIUM (degenerate)",
   "distinctive content = the LOCK to rho_DE^(1/2); conditional on nu=tower + alpha~lambda"),
 ("5","dwarf-sigma relational (non-adiabatic) spread",
   f"MI {dwarf_MI_lo*100:.0f}-{dwarf_MI_hi*100:.0f}%  vs  MG = EXACTLY 0%",
   "MOST distinctive -- MG-IMPOSSIBLE","MW dwarf sigma + orbital history (Gaia DR4)",
   "underpowered now; maybe not this decade","DISTINCTIVE but SOGGY",
   "the sharpest MI-vs-MG signal that exists, but no statistical power in hand"),
 ("-- (already decided)","Cassini |gamma-1| < 2.3e-5",
   f"framework PASSES by ~{cassini_margin_orders:.1f} orders (MI vs MG)",
   "YES -- the in-hand MI-vs-MG discriminator","Cassini (DONE)",
   "ALREADY decided -> PASS","A CRISPY SURVIVAL",
   "not a future prediction; the framework is ALIVE on the one clean in-hand test"),
]

print("="*108)
print("  EXTRA-CRISPY FALSIFICATION SCORECARD  --  de Sitter-Unruh modified inertia (a0 = cH_Lambda/Z = 9.36e-11)")
print("  honest, both-ways, NOT a TOE.  beta(apex) = {:.4e}.   crunch = distinctive x decidable x near-term".format(beta))
print("="*108)
for r in ROWS:
    print(f"\n[{r[0]}]  {r[1]}   <<{r[6]}>>")
    print(f"      prediction : {r[2]}")
    print(f"      distinctive: {r[3]}")
    print(f"      data       : {r[4]}        decision: {r[5]}")
    print(f"      honest     : {r[7]}")
print("\n"+"="*108)
print("""  THE HONEST READ (the crunch gradient):
   * The s^TX is the CRUNCHIEST LIVE test -- the ONE place the framework makes a sharp, distinctive,
     in-hand, near-term, EXCLUSIONARY prediction. It is the crispy sweet spot.
   * Everything MORE distinctive (the dwarf relational spread, MG-impossible) is UNDERPOWERED.
   * Everything MORE decidable (a0(z), the nu-mass) is HOSTAGE (dies if w->-1) or DEGENERATE.
   * That trade -- distinctiveness vs power -- is the SIGNATURE of a one-parameter modified-inertia theory,
     not a flaw to fix by computation. The crunch will come from the EXPERIMENTS, not more theory.
   * The framework is ALIVE and crispy: it PASSES the one clean in-hand discriminator (Cassini, ~5.5 orders),
     and its sharpest live test (s^TX) sits 1.5x under the bound with the data already taken.
  BOTTOM LINE: honest fried chicken, extra crispy = 's^TX = 8.7e-10 at the CMB apex; one dedicated INPOP fit
  detects it or kills this realization, with data in hand, by ~2028.' That is as crunchy as honest gets.""")
print("="*108)