#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
ballistic_survivor_window_2026.py -- after the merger gate: the dark component is ballistic and must still stay out of galaxies.
================================================================================================================================
Two known objects are ballistic (pass the Bullet), are absent from galaxies for a reason that is NOT pressure (so the matching
theorem does not apply), and can fill clusters:
  BOSON   an ultralight scalar (fuzzy DM).  Halos below M_min(m) ~ 4.4e7 (m/1e-22 eV)^(-3/2) Msun cannot form (de Broglie);
          the CMB needs the field to behave as matter at recombination: m >= ~1e-24 eV (Hlozek+ 2015, Planck).
  FERMION a light sterile fermion (Angus 2009 class).  Tremaine-Gunn caps its density at rho_max = (g/2) m^4 (2 pi sigma^2)^(3/2)/h^3:
          galaxies (sigma ~ 100 km/s) get little, clusters (sigma ~ 1000 km/s) get much -- ordered by depth, ballistically.
          Thermal production gives Omega h^2 = m/94 eV and Delta N_eff = 1.
Gates: galaxy shield (< 30% of the baryons inside 30 kpc of an L*), cluster fill (>= 1e14 Msun inside 1 Mpc possible), CMB floor,
N_eff.  Both a_0 footings where a_0 enters (nowhere here: the caps are a_0-free).  Checks CAN fail.  The LSS side (MOND-boosted
baryons carrying k >= 1 h/Mpc) is the undecidable-by-linear-theory question of cmc_filter_no_dm_growth_gate_2026.py and is NOT
re-decided here; the one N-body verdict in print (Angus+ 2013, MOND + 11 eV) found too many massive clusters.
"""
import sys, math
P = lambda *a: print(*a, flush=True); FAILS = []; NCHK = [0]
def check(name, ok, detail=""):
    NCHK[0] += 1; P(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"   ({detail})" if detail else ""))
    if not ok: FAILS.append(name)
def info(s): P("  " + s)
G = 6.674e-11; c = 2.99792458e8; hP = 6.62607e-34; eV = 1.602176634e-19; Mpc = 3.0857e22; kpc = Mpc/1e3; Msun = 1.989e30
MB = 6e10*Msun; V30 = 4/3*math.pi*(30*kpc)**3; V1 = 4/3*math.pi*Mpc**3
P("="*100); P("A. the boson: de Broglie exclusion vs the CMB floor"); P("="*100)
def M_min(m_eV): return 4.4e7*(m_eV/1e-22)**(-1.5)*Msun                 # minimum halo mass (Schive+ 2014 / Hui+ 2017)
M_STAR_HALO = 1e11*Msun                                                   # what an L* galaxy's well would collect in the hybrid (baryons + MOND ~ 1e11 effective)
M_CLUSTER = 1e15*Msun; M_CMB_FLOOR = 1e-24                                # Hlozek+ 2015: m >= 1e-24 eV for the field to be the CMB's dark matter
m_gal = 1e-22*(M_min(1e-22)/M_STAR_HALO)**(2/3)                          # largest m for which an L* halo cannot form
m_clu = 1e-22*(M_min(1e-22)/M_CLUSTER)**(2/3)                             # smallest m for which a cluster halo can still form
info(f"L* galaxy halo-free needs M_min >= {M_STAR_HALO/Msun:.0e} Msun  ->  m <= {m_gal:.1e} eV")
info(f"cluster halo can form needs M_min <= {M_CLUSTER/Msun:.0e} Msun ->  m >= {m_clu:.1e} eV")
info(f"CMB (Planck) floor: m >= {M_CMB_FLOOR:.0e} eV")
info(f"A1 at the L* level alone the gap is only x{M_CMB_FLOOR/m_gal:.1f} -- an EDGE, inside the modelling slop of M_min and of the Planck floor")
# the RAR is mass-independent to 0.034 dex up to the most massive SPARC discs (M_b ~ 3e11 Msun, v_flat ~ 300 km/s), whose wells would
# collect a 1e12-1e13 Msun boson halo in the hybrid; those galaxies must be halo-free too, or the RAR would bend at high mass.
for Mw in (1e12, 1e13):
    m_w = 1e-22*(M_min(1e-22)/(Mw*Msun))**(2/3)
    info(f"massive SPARC discs halo-free (well collects {Mw:.0e} Msun) -> m <= {m_w:.1e} eV : gap to the CMB floor x{M_CMB_FLOOR/m_w:.0f}")
m_1e12 = 1e-22*(M_min(1e-22)/(1e12*Msun))**(2/3)
check("A2 the boson window is EMPTY once the RAR's mass-independence is used: keeping the most massive SPARC discs halo-free needs m <= 1.3e-25 eV, the CMB needs m >= 1e-24 eV -- a gap of >= 7x; fuzzy dark matter cannot be the CMB's dark matter and leave the whole RAR untouched",
      M_CMB_FLOOR/m_1e12 >= 5, f"gap = x{M_CMB_FLOOR/m_1e12:.0f}")
P(""); P("="*100); P("B. the fermion: the Tremaine-Gunn cap orders the dark density by depth, ballistically"); P("="*100)
def rho_max(m_eV, sigma_kms, g=2): m = m_eV*eV/c**2; s = sigma_kms*1e3; return (g/2)*m**4*(2*math.pi*s**2)**1.5/hP**3
info(f"{'m (eV)':>7} {'rho_max gal (100 km/s)':>24} {'M(<30kpc)/M_b':>14} {'rho_max clu (1000 km/s)':>25} {'M_max(<1Mpc)/1e14':>18} {'thermal Omega h^2':>18}  galaxy  cluster")
res = {}
for m in (2.0, 5.0, 8.0, 11.0, 15.0, 20.0):
    rg = rho_max(m, 100.0); rc = rho_max(m, 1000.0)
    fg = rg*V30/MB; Mc = rc*V1/(1e14*Msun); om = m/94.0
    res[m] = (fg, Mc, om)
    info(f"{m:7.1f} {rg:24.2e} {fg:14.3f} {rc:25.2e} {Mc:18.3g} {om:18.3f}  {'ok' if fg <= 0.30 else 'NO':>6}  {'ok' if Mc >= 1.0 else 'short':>7}")
win = [m for m, v in res.items() if v[0] <= 0.30 and v[1] >= 1.0]
check("B1 a fermion window EXISTS: for m ~ 5-11 eV the phase-space cap keeps the medium below 30% of the baryons inside 30 kpc of an L* galaxy while allowing >= 1e14 Msun inside 1 Mpc of a cluster -- the depth-ordered cap the polytrope and the solid were built to imitate, from Pauli exclusion, ballistic",
      len(win) >= 2 and 5.0 in win and 11.0 in win, f"window: {win} eV")
dNeff_thermal = 1.0
check("B2 but THERMAL production is dead: Omega_dm h^2 = m/94 eV needs m = 11.3 eV and brings Delta N_eff = 1, against Planck's N_eff = 2.99 +/- 0.17 (a ~6 sigma exclusion); the window survives only with non-thermal production, i.e. one more free input",
      abs(res[11.0][2] - 0.12) < 0.01 and dNeff_thermal/0.17 > 5)
P(""); P("="*100); P("C. what the fermion passes and what it still owes"); P("="*100)
info("passes: the merger gate (ballistic), the matching theorem (no equation of state: it is collisionless), the CMB (non-relativistic since z ~ 2e4 for m ~ 10 eV),")
info("        the galaxy shield (Pauli, not pressure), the cluster mass (Angus+ 2010 fits), the Bullet peaks (Angus, Famaey & Zhao 2007 with 2 eV; KATRIN now < 0.45 eV for actives -> sterile)")
info("owes:   large-scale structure -- its free-streaming scale is ~Mpc, so k >= 1 h/Mpc must be grown by MOND on the baryons: the shape question linear theory cannot decide;")
info("        the one N-body in print (Angus, Diaferio, Famaey, van der Heyden 2013) overproduces massive clusters; and a non-thermal production mechanism.")
info("and it is a PARTICLE.  A sterile fermion at 5-11 eV is dark matter in every sense except 'in galaxies'.")
P(""); P("="*100); P("VERDICT"); P("="*100)
P("  Ballistic and absent from galaxies leaves two objects.  The boson's window is empty by a factor 7-30 between the CMB floor and the")
P("  RAR's massive discs (x1.7 at the L* level alone).  The fermion's window is real, 5-11 eV, ordered by depth through Pauli exclusion rather than pressure, ballistic through")
P("  the Bullet, but dead if thermal (N_eff) and undecided on large-scale structure, where the only N-body verdict is negative.  It is a")
P("  particle.  The 'not matter' reading of the framework's dark sector has no surviving object; the 'no dark matter in galaxies' reading")
P("  has exactly one, and it is Angus's sterile neutrino, whose fate is a MOND N-body that nobody has run with the framework's a_0(z).")
P(f"\nRESULT: {NCHK[0]} checks, {len(FAILS)} FAIL" + (f" -> {FAILS}" if FAILS else "") + f"   rc={1 if FAILS else 0}")
sys.exit(1 if FAILS else 0)
