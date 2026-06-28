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
cassini_margin_orders = 5.5                # framework PASSES |gamma-1|<2.3e-5 by ~5.5 orders -- but MOND-SHARED (trivial a>>a0 at the Sun), NOT distinctive; and the Q2 quadrupole is an INHERITED 3-15sigma tension (corrected 2026-06-28)

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
 ("-- (CORRECTED 2026-06-28)","Cassini |gamma-1| (gamma-pass) vs the Q2 QUADRUPOLE",
   f"gamma-pass ~{cassini_margin_orders:.1f} orders -- but MOND-SHARED (trivial: a>>a0 at the Sun), NOT distinctive",
   "NO -- the gamma-pass is shared survival; the Q2 quadrupole is a 3-15sigma TENSION the framework INHERITS",
   "Cassini (DONE) + Park et al. 2026 (2602.17884)",
   "two-sided: gamma SHARED-pass; Q2 quadrupole = INHERITED tension (AeST=MG, Desmond-Hees-Famaey)",
   "NOT a clean win",
   "the framework's WRITTEN covariant realization (AeST) is modified GRAVITY -> inherits the 3-15sigma RAR-vs-Q2 "
   "tension; MI-evasion needs the UNWRITTEN MI completion. The genuine MI-vs-MG test is s^TX (future). "
   "See reviews/cassini_quadrupole_framework.py."),
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
   * The framework is ALIVE: it PASSES the Cassini gamma bound (~5.5 orders) -- but that pass is MOND-SHARED (trivial
     at the Sun), NOT a distinctive discriminator; and the Cassini Q2 QUADRUPOLE is a 3-15sigma RAR-vs-Q2 TENSION its
     AeST (modified-gravity) realization INHERITS (corrected 2026-06-28). Its sharpest live test (s^TX) sits 1.5x under
     the bound with the data already taken -- and THAT, not Cassini, is the genuine in-hand-data MI-vs-MG channel.
  BOTTOM LINE: honest fried chicken, extra crispy = 's^TX = 8.7e-10 at the CMB apex; one dedicated INPOP fit
  detects it or kills this realization, with data in hand, by ~2028.' That is as crunchy as honest gets.""")
print("="*108)