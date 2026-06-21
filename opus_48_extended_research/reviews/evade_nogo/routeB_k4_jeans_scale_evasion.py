#!/usr/bin/env python3
r"""
ROUTE B -- the k^4 JEANS / scale-dependent clustering mechanism: THE candidate loophole
=======================================================================================
Carl's challenge (the RIGHT move against a no-go): BEFORE publishing the density-ordering
no-go for the cluster residual, test whether the ghost-condensate's k^4 dispersion sets a
FINITE, SCALE-dependent Jeans scale that lets the AeST Q-mode cluster at CLUSTER scales
(~Mpc) while staying SMOOTH at GALAXY scales (~kpc) -- ordering by SCALE not DENSITY, and
thereby SIDESTEPPING the no-go's "galaxies are denser" argument.

THE NO-GO (banked CLUSTER_RESIDUAL_DENSITY_NOGO.md, draft paper):
  abundance OK (1.46x, zero tuning), but the c_s^2 -> 0 cold mode clumps wherever rho is
  highest; galaxy disks are ~3.7x DENSER than cluster cores, so it clumps MORE in galaxies,
  injecting +0.12-0.23 dex into the RAR (floor 0.11-0.14) = breaks the galaxy law.

THE CANDIDATE EVASION (the loophole the no-go MAY have missed):
  a ghost condensate is NOT just c_s^2 -> 0 -- it has a k^4 dispersion
       omega^2 ~ c_s^2 k^2 + B k^4/M^2          (Arkani-Hamed-Cheng-Luty-Mukohyama 2004)
  The k^4 term sets a FINITE Jeans scale. If that scale sits BETWEEN galaxy (~kpc) and
  cluster (~Mpc) scales, the field clusters at cluster scales (k below Jeans) but is
  smoothed at galaxy scales (k above Jeans) -- evasion by SCALE.

WHAT THIS SCRIPT COMPUTES (both ways, quarantine: a0/Z/kappa/I0 never derived):
  STEP 1.  Derive the ghost-condensate dispersion omega^2 = c_s^2 k^2 + B k^4/M^2 (+ the mu
           mass term) symbolically, and the AeST host's ACTUAL dispersion, from the primary
           papers (verbatim equations).
  STEP 2.  RE-CHECK B=0 RIGOROUSLY. Is the propagating-scalar k^4 coefficient B genuinely
           zero in the named host (AeST khronon), at all scales/backgrounds, or only in a
           special limit? Distinguish the isolated-GC k^4 from the AeST-host dispersion.
  STEP 3.  IF a k^4 (or mu) Jeans scale exists, COMPUTE it as a function of density/scale and
           ask: does lambda_J sit BETWEEN ~kpc (galaxy) and ~Mpc (cluster)?  -- the in-window
           test that decides the evasion.
  STEP 4.  Does the SCALE-ordering actually run the RIGHT way (smooth at small scales/galaxies,
           clumpy at large scales/clusters)? -- the SIGN/DIRECTION test. (A Jeans cutoff
           SMOOTHS BELOW lambda_J, i.e. at SMALL scales -- check which of galaxy/cluster is
           "small" and whether that helps or hurts.)
  STEP 5.  The mu mass term as a scale-dependent SCREENING (SZ21: mu^2 Phi "akin to ghost
           condensation"): does it give a helpful galaxy-safe/cluster-clumpy split?
  STEP 6.  CMB preservation: is c_s^2 -> 0 at large scales/small k preserved (3rd peak)?
           RAR preservation: smooth at galaxy scales?
  VERDICT. Does the k^4/mu mechanism EVADE the no-go, or does the no-go STAND? Both ways.

PRIMARY SOURCES (equations fetched/verified verbatim this session + banked Door-A pin):
  SZ21   = Skordis & Zlosnik 2021, PRL 127 161302, arXiv:2007.00082
           ABSTRACT-verbatim (fetched): "scalar degree of freedom with dispersion relation
           omega=0" is the Minkowski result of the COMPANION Blanchet-Skordis paper; SZ21's
           own cosmological scalar modes (fetched verbatim this session):
             omega^2 = 0                                    (constraint / Jeans mode)
             omega^2 = [(2-K_B)/(K_2 K_B)(1+1/2 K_B lambda_s)] k^2 + M^2   (massive acoustic)
           mass of the potential: mu = sqrt(2 K_2/(2-K_B)) Q_0 ; "mu^-1 >~ 1 Mpc" forced;
           "mu^2 Phi which is akin to ghost condensation" (verbatim).
  BS24   = Blanchet & Skordis 2024, JCAP 11 040, arXiv:2404.06584
           ABSTRACT-verbatim (fetched this session): "a scalar degree of freedom with
           dispersion relation omega=0 ... deconstrained Hamiltonian is bounded from below
           for wavenumbers larger than ~10^-31 eV and unbounded for smaller wavenumbers."
           Door-A pin (banked, verbatim Sec 6.2): "there are no higher derivative interaction
           terms in the action, which are also quadratic in the fields."
  ACLM   = Arkani-Hamed, Cheng, Luty, Mukohyama 2004, hep-th/0312099 (the isolated ghost
           condensate): broken-phase dispersion (their Eq.~7.8/2.9 region)
             omega^2 = (alpha^2/M^2) k^4 - (alpha^2 M^2/(2 M_Pl^2)) k^2
           -> with gravity, k^2 coeff is NEGATIVE (Jeans), k^4 STABILIZES; Jeans scale
             k_J = M^2/(sqrt2 M_Pl) == the "graviton mass" m == AeST's mu.
  Banked: GHOST_CONDENSATE_CONSEQUENCES (k_J = M^2/(sqrt2 M_Pl) = mu), DOORA_PIN (B=0 in host),
          cluster_aest_massterm_derivation.py (mu^2 Phi integration: deficit, not boost),
          Mistele+2023 A&A 676 A100 (galaxy<->cluster scale tension on mu).
"""
import numpy as np
import sympy as sp

# ============================== constants ==============================
c    = 2.99792458e8            # m/s
G    = 6.67430e-11             # SI
hbar = 1.054571817e-34        # J s
eV   = 1.602176634e-19        # J
kpc  = 3.0856775814913673e19  # m
Mpc  = 3.0856775814913673e22  # m
Msun = 1.98892e30             # kg
GeV  = 1e9*eV
M_Pl_red_eV = 2.435e18*GeV/eV         # reduced Planck mass in eV = 2.435e27 eV

H0   = 67.4e3/Mpc             # s^-1
h    = 0.674
Om_L = 0.685; Om_dm = 0.265; Om_b = 0.0493; Om_m = 0.315
H_L  = H0*np.sqrt(Om_L)
Lambda = 3*Om_L*(H0/c)**2     # m^-2
a0   = c**2*np.sqrt(Lambda/(32*np.pi))   # framework a0
rho_crit = 3*H0**2/(8*np.pi*G)           # kg/m^3

W = "="*90
print(W); print("ROUTE B -- the k^4 / mu JEANS SCALE: does scale-ordering evade the density no-go?")
print(W)
print(f"  a0 = c^2 sqrt(Lambda/32pi) = {a0:.4e} m/s^2 (target 9.36e-11)  [QUARANTINED input]")
print(f"  rho_crit = {rho_crit:.4e} kg/m^3 ;  c/H0 = {c/H0/Mpc:.0f} Mpc")

# =====================================================================================
# STEP 1 -- the dispersion relations, symbolic (isolated GC vs the AeST host)
# =====================================================================================
print("\n"+W); print("STEP 1 -- the dispersion: isolated ghost condensate vs the AeST host")
print(W)
k, M, MPl, alpha, cs2, Bcoef, mu, K2, KB, lam_s, Q0 = sp.symbols(
    'k M M_Pl alpha c_s^2 B mu K_2 K_B lambda_s Q_0', positive=True)

# (1a) ISOLATED ghost condensate (ACLM), broken phase, mixed with gravity:
A_aclm = alpha**2 * M**2/(2*MPl**2)      # |k^2| coeff (enters NEGATIVE)
B_aclm = alpha**2                        # k^4 coeff (x k^4/M^2)
omega2_GC = B_aclm*k**4/M**2 - A_aclm*k**2
print("\n(1a) ISOLATED ghost condensate (ACLM hep-th/0312099, w/ gravity):")
print("     omega^2 =", omega2_GC, "   [k^2 coeff NEGATIVE -> Jeans below k_J, k^4 stabilizes above]")
kJ_GC = sp.simplify(M*sp.sqrt(A_aclm/B_aclm))
print("     Jeans wavenumber  k_J = M sqrt(A/B) =", kJ_GC, " = M^2/(sqrt2 M_Pl)  (ACLM graviton mass m)")

# (1b) AeST HOST cosmological scalar modes (SZ21, verbatim this session):
cs2_aest = (2-KB)/(K2*KB)*(1 + sp.Rational(1,2)*KB*lam_s)   # SZ21 acoustic coeff
omega2_aest_acoustic = cs2_aest*k**2 + M**2                 # massive acoustic mode
omega2_aest_jeans    = sp.Integer(0)                        # constraint / Jeans mode: omega=0
print("\n(1b) AeST HOST (SZ21 arXiv:2007.00082, verbatim cosmological scalar modes):")
print("     omega^2 (constraint/Jeans mode) =", omega2_aest_jeans, "   <-- the propagating dof: omega = 0")
print("     omega^2 (massive acoustic mode) =", omega2_aest_acoustic)
print("        ==> the AeST host dispersion is  c_s^2 k^2 + M^2  (acoustic + mass), NOT k^4.")
print("     mass of metric potential:  mu = sqrt(2 K_2/(2-K_B)) Q_0   ;  mu^2 Phi 'akin to ghost cond.'")

# (1c) the general k^4 ansatz the loophole posits:
omega2_loop = cs2*k**2 + Bcoef*k**4/M**2
print("\n(1c) the LOOPHOLE ansatz to test:  omega^2 =", omega2_loop)
print("     -> a FINITE Jeans scale requires B != 0 (k^4 present in the PROPAGATING quadratic action).")

# =====================================================================================
# STEP 2 -- RE-CHECK B=0 RIGOROUSLY in the named host
# =====================================================================================
print("\n"+W); print("STEP 2 -- is B (the propagating-scalar k^4 coefficient) ZERO in the host? RIGOROUS")
print(W)
print("""
  THREE distinct objects must not be conflated:
   (i)  ISOLATED ghost condensate (ACLM): omega^2 = +B k^4/M^2 - A k^2, B=alpha^2 != 0.
        The k^4 is REAL here because the leading (grad pi)^2 coefficient P'(X0)=0 vanishes
        at the condensate point, so the NEXT term (k^4) is the leading gradient energy.
   (ii) AeST HOST, COSMOLOGICAL scalar sector (SZ21): the propagating mode that fits the
        CMB is the MASSIVE ACOUSTIC mode omega^2 = c_s^2 k^2 + M^2.  Its leading gradient
        term is k^2 (NONZERO c_s^2 from K_2,K_B,lambda_s), so there is NO k^4 needed and the
        action carries NO propagating quadratic k^4. B=0 by the structure of the action.
   (iii) AeST HOST, MINKOWSKI second-order action (BS24): the propagating scalar dof has
        omega = 0 EXACTLY (BS24 abstract, verbatim). Sec 6.2 (Door-A pin, verbatim):
        'there are no higher derivative interaction terms in the action, which are also
        quadratic in the fields.'  The lone k^4 in the action is the CONSTRAINT momentum
        P_nu = (1/3) k^4 (nu_dot + 2 zeta) of the NON-dynamical trace mode, gauge-fixed to 0.

  VERDICT on B: in the NAMED HOST (AeST khronon), the PROPAGATING quadratic k^4 coefficient
  B = 0 EXACTLY -- verbatim from BS24 Sec 6.2 + the omega=0 abstract; and the cosmological
  propagating mode is k^2+M^2, not k^4. B != 0 ONLY for the ISOLATED GC (ACLM), which is
  the EFT-modeling analogy, NOT the host's literal quadratic structure.
""")
# Demonstrate the structural reason symbolically: if the leading gradient coeff is nonzero
# (c_s^2 = (grad)^2 coefficient), the k^4 is subleading and absent in a 2-derivative action.
print("  Structural demonstration (sympy): in a 2-derivative scalar action S ~ integral")
print("  [ A_t (dphi/dt)^2 - A_x (grad phi)^2 - m^2 phi^2 ], the EOM gives")
phi_t, phi_x, A_t, A_x, m2 = sp.symbols('phidot gradphi A_t A_x m^2', positive=True)
omega_sym, ksym = sp.symbols('omega k', positive=True)
disp = sp.Eq(A_t*omega_sym**2, A_x*ksym**2 + m2)
print("     ", disp, "  ->  omega^2 =", sp.solve(disp, omega_sym**2)[0], "  (pure k^2 + mass; NO k^4)")
print("  A k^4 term requires a 4-DERIVATIVE operator (grad^2 phi)^2 in the action. BS24 Sec 6.2")
print("  states such quadratic higher-derivative operators are ABSENT. => B=0 in the host. CONFIRMED.")

# =====================================================================================
# STEP 3 -- IF a k^4 (or mu) Jeans scale existed, WHERE does it land? (in-window test)
# =====================================================================================
print("\n"+W); print("STEP 3 -- the candidate Jeans scale lambda_J: is it BETWEEN ~kpc and ~Mpc?")
print(W)

def kJ_from_M_eV(M_eV):
    """isolated-GC Jeans wavenumber k_J = M^2/(sqrt2 M_Pl) as an inverse length -> h/Mpc."""
    m_eV   = M_eV**2/(np.sqrt(2)*M_Pl_red_eV)     # eV (graviton-mass scale)
    k_invm = m_eV*eV/(hbar*c)                     # 1/m
    k_hMpc = k_invm*Mpc/h
    lam_Mpc = (1.0/k_invm)/Mpc if k_invm>0 else np.inf
    return m_eV, k_hMpc, lam_Mpc

print("\n  (3a) ISOLATED-GC route: k_J = M^2/(sqrt2 M_Pl), scan the clustering-M window:")
print(f"  {'M (eV)':>9} | {'k_J (h/Mpc)':>13} | {'lambda_J (Mpc)':>15} | {'between kpc & Mpc?':>18}")
for M_eV in [0.04, 0.1, 0.148, 0.4, 1.0, 10.0]:
    _, k_hMpc, lam_Mpc = kJ_from_M_eV(M_eV)
    inwin = "YES" if (1e-3 < lam_Mpc < 1.0) else ("no (too big)" if lam_Mpc>=1.0 else "no (too small)")
    print(f"  {M_eV:>9.3g} | {k_hMpc:>13.3e} | {lam_Mpc:>15.3e} | {inwin:>18}")
print("""    => for the framework's self-consistent M (mu^-1=1 Mpc <-> M=0.148 eV), lambda_J = mu^-1
       = 1 Mpc -- i.e. the GC Jeans scale IS the mu scale, sitting AT the cluster scale, NOT
       between kpc and Mpc. To put lambda_J at ~100 kpc (between galaxy & cluster) needs M~0.5 eV,
       which forces mu^-1 ~ 0.1 Mpc -- and that BREAKS galaxies (see Step 5).""")

print("\n  (3b) the AeST mu mass scale directly (the cosmologically/galactically forced object):")
print(f"  {'mu^-1 (Mpc)':>12} | {'lambda_J=mu^-1':>14} | {'galaxy-safe?':>13} | {'cluster-clumpy?':>16}")
for mu_inv in [10.0, 3.0, 1.0, 0.3, 0.1]:
    gal = "YES" if mu_inv >= 1.0 else "NO (mu reaches into disks)"
    clu = "marginal" if mu_inv <= 1.0 else "no (mu only at >Mpc)"
    print(f"  {mu_inv:>12.2g} | {mu_inv:>11.2g} Mpc | {gal:>13} | {clu:>16}")
print("""    => mu^-1 must be >~ 1 Mpc to keep galaxies MOND-pure (SZ21/VSB24/Mistele). But the
       cluster CORE is at ~0.4 Mpc -- INSIDE mu^-1. So at the radius where we need extra cluster
       clumping, the mu screening is ON (suppressing), and where we need galaxies smooth (kpc)
       the screening is far inside mu^-1 and basically OFF. The scale-ordering helps the WRONG way
       (see Step 4).""")

# =====================================================================================
# STEP 4 -- the SIGN/DIRECTION: a Jeans cutoff SMOOTHS BELOW lambda_J (= small scales)
# =====================================================================================
print("\n"+W); print("STEP 4 -- DIRECTION of the scale-ordering: does it smooth galaxies & clump clusters?")
print(W)
print("""
  A Jeans/sound cutoff at lambda_J SUPPRESSES growth on scales SMALLER than lambda_J
  (k > k_J) and ALLOWS growth on scales LARGER than lambda_J (k < k_J).
  Scale hierarchy:  galaxy disk ~ kpc  <  cluster core ~ Mpc  <  c/H0 ~ 4000 Mpc.

  The loophole NEEDS: smooth at GALAXY (kpc) scales, clumpy at CLUSTER (Mpc) scales.
  A Jeans cutoff at lambda_J ~ 100 kpc (between kpc and Mpc) WOULD do exactly this:
    - kpc < lambda_J  -> galaxy scale is BELOW the cutoff -> SMOOTHED (good, galaxy-safe)
    - Mpc > lambda_J  -> cluster scale is ABOVE the cutoff -> CLUMPS (good, cluster mass)
  So the DIRECTION is RIGHT *if* lambda_J can be parked between kpc and Mpc.

  THE CATCH (both ways): the loophole's direction is correct, but Steps 2-3 show lambda_J is
  NOT a free knob you can park at 100 kpc:
    (i)  in the NAMED HOST B=0 -> there is NO k^4 Jeans scale at all (the propagating mode is
         omega=0 / k^2+M^2). The only finite scale is mu^-1, which the data force to >~1 Mpc.
    (ii) the isolated-GC k_J and the mu mass scale are the SAME scale (k_J=mu=M^2/sqrt2 M_Pl),
         so you cannot separately tune a 'galaxy-smoothing' lambda_J from the 'cluster' mu.
    (iii) to park lambda_J at ~100 kpc you must set mu^-1 ~ 100 kpc, which puts the screening
         INSIDE galaxy disks and BREAKS the RAR (Step 5) -- the very thing the no-go says.
""")

# Quantify: the per-galaxy RAR injection if the field clumps at the disk (the no-go's kill)
print("  Quantify (the no-go's kill, reproduced): inject Om_dm-worth cold density into a disk.")
# fiducial disk: M_b = 6e10 Msun within R_d = 3 kpc scale; cold add at Om_dm/Om_b ratio
Mb_disk = 6e10*Msun; R_disk = 3*kpc
ratio_dm_b = Om_dm/Om_b
g_bar_disk = G*Mb_disk/R_disk**2
g_mond_disk = np.sqrt(g_bar_disk*a0 + g_bar_disk**2)
# if a fraction f of the cosmic dm/b ratio clumps locally onto the disk baryons:
print(f"  Om_dm/Om_b = {ratio_dm_b:.2f}; disk g_bar={g_bar_disk:.3e}, g_mond={g_mond_disk:.3e}")
print(f"  {'clump fraction f':>16} | {'extra g_dm':>12} | {'g_tot/g_mond':>13} | {'RAR shift (dex)':>16}")
for f in [0.05, 0.10, 0.30, 0.60, 1.00]:
    g_dm = f*ratio_dm_b*g_bar_disk          # cold mass tracks baryons at fraction f of cosmic ratio
    g_tot = np.sqrt((g_bar_disk + g_dm)*a0 + (g_bar_disk+g_dm)**2)  # add to baryonic source
    shift = np.log10(g_tot/g_mond_disk)
    print(f"  {f:>16.2f} | {g_dm:>12.3e} | {g_tot/g_mond_disk:>13.3f} | {shift:>16.3f}")
print("  RAR scatter floor = 0.11-0.14 dex (McGaugh+2016). Any f>~0.10 clumping in disks breaks it.")

# =====================================================================================
# STEP 5 -- the mu mass term as scale-dependent SCREENING: galaxy-safe AND cluster-clumpy?
# =====================================================================================
print("\n"+W); print("STEP 5 -- the mu mass term as scale-dependent screening (the only finite host scale)")
print(W)
print("""
  SZ21: 'mu^2 Phi which is akin to ghost condensation'; mu = sqrt(2 K_2/(2-K_B)) Q_0.
  The mass term gives the metric potential a Yukawa screening on scales > mu^-1:
       (Laplacian - mu^2) Phi = 4 pi G rho   ->   Phi ~ -(GM/r) e^{-mu r}
  SCREENING DIRECTION: it SUPPRESSES the potential on LARGE scales r > mu^-1 (the OPPOSITE
  of what we need -- it would suppress the CLUSTER-scale mass, not the galaxy-scale).
""")
# banked cluster_aest_massterm_derivation.py: integrating the modified Helmholtz with mu^-1=1 Mpc
# gives a DEFICIT at R500 (ratio ~0.2), helpful peak at 3-4.5 Mpc (wrong radius). Reproduce the sign.
print("  Banked integration (cluster_aest_massterm_derivation.py): with mu^-1 = 1 Mpc (CMB-pinned),")
print("  the mu^2 Phi term DRAINS g at R500 (ratio ~0.2 = a DEFICIT) and the helpful peak sits at")
print("  3-4.5 Mpc (BEYOND R500) -- the WRONG radius. The amplitude at R500 rides a FREE boundary")
print("  shift chi_inf (fitted per cluster, not predicted). => the mu term does NOT naturally boost.")
print()
# Yukawa screening factor at galaxy vs cluster scales for mu^-1 = 1 Mpc:
mu_inv_Mpc = 1.0
print(f"  Yukawa screening e^(-mu r) for mu^-1 = {mu_inv_Mpc} Mpc:")
print(f"  {'scale r':>16} | {'mu r':>8} | {'e^(-mu r)':>10} | {'screening':>12}")
for lab, r_Mpc in [("galaxy disk 10 kpc",0.010),("galaxy halo 100 kpc",0.10),
                   ("cluster core 0.4 Mpc",0.4),("R500 1.3 Mpc",1.3),("outskirt 3 Mpc",3.0)]:
    mur = r_Mpc/mu_inv_Mpc
    scr = np.exp(-mur)
    tag = "OFF (unscreened)" if mur<0.3 else ("partial" if mur<1.5 else "ON (suppressed)")
    print(f"  {lab:>16} | {mur:>8.3f} | {scr:>10.4f} | {tag:>12}")
print("""    => the mass term is OFF at galaxy scales (good for galaxy-safety) but it is ON (suppressing)
       exactly at cluster scales where we NEED extra mass -- it SUPPRESSES the cluster potential,
       the wrong sign for a cluster surplus. The scale-dependent screening orders the WRONG way:
       it would help only if it ENHANCED at cluster scales, but Yukawa screening always suppresses
       at large r. (The Durakovic-Skordis oscillatory peak CAN exceed MOND, but at 3-4.5 Mpc and
       only via a fitted boundary shift -- not a galaxy-safe, predicted, in-the-core boost.)""")

# =====================================================================================
# STEP 6 -- CMB + RAR preservation (the two constraints the evasion must also satisfy)
# =====================================================================================
print("\n"+W); print("STEP 6 -- does any helpful scale preserve BOTH the CMB 3rd peak AND the RAR?")
print(W)
print("""
  CMB 3rd peak: requires the Q-mode to be COLD (c_s^2 -> 0, clusters like CDM) at the large
  scales / small k probed by Planck (k ~ 0.001-0.2 h/Mpc). AeST achieves this with the
  massive-acoustic mode tuned so c_s^2 -> 0 sub-horizon (SZ21 fit the full Planck spectrum).
  -> The CMB fit FORCES c_s^2 -> 0 at small k. Good news: that is consistent with a Jeans
     scale at SMALL scales (large k) -- it does NOT by itself force c_s^2->0 at ALL k.

  RAR: requires the field SMOOTH at galaxy (kpc) scales. A Jeans cutoff at lambda_J between
  kpc and Mpc would smooth galaxies. -> consistent IN PRINCIPLE.

  SO the constraints CMB + RAR are individually satisfiable by a lambda_J in (kpc, Mpc). The
  evasion fails NOT on CMB/RAR compatibility but on STEP 2: in the NAMED HOST there is NO such
  k^4 Jeans scale (B=0; propagating mode omega=0 / k^2+M^2), and the only finite scale mu^-1 is
  (i) forced >~1 Mpc by galaxies and (ii) a SUPPRESSING screening (wrong sign) at cluster scales.
""")

# Self-consistency: M <-> mu^-1 relation, and where lambda_J would have to be vs galaxy break
print("  Self-consistency knot (the killer): one scale M sets BOTH k_J and the galaxy-break radius.")
print(f"  {'mu^-1 (Mpc)':>12} | {'M (eV)':>9} | {'lambda_J':>10} | {'galaxies?':>22} | {'clusters?':>10}")
for mu_inv in [10.0, 3.0, 1.0, 0.3, 0.1]:
    # mu (1/m) -> M^2/(sqrt2 MPl) = mu => M_eV = sqrt(mu_eV * sqrt2 * MPl)
    mu_invm = 1.0/(mu_inv*Mpc)                # 1/m
    mu_eV   = mu_invm*hbar*c/eV               # eV
    M_eV    = np.sqrt(mu_eV*np.sqrt(2)*M_Pl_red_eV)
    lam_J   = mu_inv                          # lambda_J = mu^-1 (k_J=mu)
    gal = "MOND-pure" if mu_inv>=1.0 else "BROKEN (mu in disk)"
    clu = "screened" if mu_inv<=1.0 else "mu>Mpc, no help"
    print(f"  {mu_inv:>12.2g} | {M_eV:>9.3f} | {lam_J:>8.2g} Mpc | {gal:>22} | {clu:>10}")
print("""    => there is NO row where galaxies are MOND-pure AND clusters get a clumping boost: the
       SAME mu^-1 that keeps galaxies safe (>~1 Mpc) puts the screening at/inside the cluster core
       where it SUPPRESSES, not enhances. The would-be 'park lambda_J at 100 kpc' row (mu^-1=0.1
       Mpc) BREAKS galaxies. The scale window the loophole needs is EMPTY in the host.""")

# =====================================================================================
# VERDICT
# =====================================================================================
print("\n"+W); print("VERDICT (both ways) -- does the k^4 / mu Jeans scale EVADE the no-go?")
print(W)
print("""
  THE LOOPHOLE'S LOGIC IS SOUND IN PRINCIPLE (credit at full weight): a finite Jeans scale
  lambda_J parked BETWEEN galaxy (kpc) and cluster (Mpc) scales WOULD order clustering by SCALE
  (smooth galaxies, clumpy clusters), sidestepping the density-ordering argument, AND would be
  compatible with both the CMB 3rd peak (c_s^2->0 at small k) and the RAR (smooth at kpc). The
  no-go's density-ordering argument does NOT, by itself, exclude a scale-ordering escape. This
  is a genuine, well-posed physics loophole -- Carl was right to demand it be tested.

  BUT THE EVASION FAILS IN THE NAMED HOST (report straight, both ways):
   (1) B = 0 EXACTLY in the AeST khronon (BS24 Sec 6.2 verbatim: 'no higher derivative
       interaction terms... quadratic in the fields'; abstract: scalar dof 'dispersion relation
       omega=0'). The propagating cosmological mode is the MASSIVE ACOUSTIC k^2+M^2 (SZ21), NOT
       k^4. There is NO propagating-quadratic k^4 Jeans scale to park. The k^4 belongs to the
       ISOLATED ghost condensate (ACLM) -- an EFT-modeling analogy, not the host's literal action.
   (2) Even taking the isolated-GC k^4 at face value, its Jeans scale k_J = M^2/(sqrt2 M_Pl) is
       NOT independent of the mass scale: k_J = mu EXACTLY. So there is no separate galaxy-
       smoothing knob; the one scale mu^-1 is forced >~1 Mpc by galaxies (SZ21/VSB24/Mistele) --
       ABOVE the cluster core, not between kpc and Mpc.
   (3) The mu mass term is a SCREENING (Yukawa e^{-mu r}) that SUPPRESSES the potential at LARGE
       r > mu^-1 -- the WRONG sign at cluster scales (it drains, not boosts; banked integration
       gives a DEFICIT ~0.2 at R500, peak at the wrong radius 3-4.5 Mpc, amplitude on a fitted
       boundary shift). To park lambda_J at ~100 kpc you must set mu^-1 ~ 100 kpc, which BREAKS
       galaxies (the no-go's own kill: +0.12-0.23 dex into the RAR).
   (4) The scale window the loophole needs -- a tunable lambda_J in (kpc, Mpc) decoupled from the
       galaxy-break scale -- is EMPTY: one parameter (mu/M) sets BOTH the Jeans scale AND the
       galaxy-break scale, and they coincide. You cannot smooth galaxies and clump clusters with
       one knob whose value is pinned >~1 Mpc by galaxies.

  NET: the no-go STANDS. The k^4 / mu scale-ordering mechanism is a real, correct-in-principle
  idea, but it does NOT evade the no-go in the framework's actual host (AeST/Skordis-Zlosnik):
  B=0 removes the k^4 Jeans scale, and the lone finite scale mu is (a) a single knob that pins
  the galaxy-break and 'Jeans' scales together and (b) a wrong-signed screening at cluster scales.
  No manufactured loophole; no reflexive dismissal -- the loophole was hunted hard and is closed
  by the host's actual quadratic structure, verbatim from the primary papers.

  QUARANTINE: a0/Z/kappa/I0 never asserted derived; mu/M/I0 remain free inputs.
""")
print(W)
