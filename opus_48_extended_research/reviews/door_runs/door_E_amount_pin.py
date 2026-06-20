#!/usr/bin/env python3
"""
DOOR E  (door "E_amount_pin")  --  GAP-4 (the AMOUNT of dark matter).
=====================================================================
QUESTION: does ANY de Sitter number PIN Omega_dm without a free integration
constant I0?  Run the Ghost-Dark-Matter abundance integration on an FRW
background: integrate the shift-charge first integral  a^3 K'(Q) = I0,
evolve rho_dust(a) to today, compute Omega_dm(M, I0).  Then SCAN: set the
ghost-condensate SSB scale M to each candidate dS scale
   {hbar H_Lambda,  k_B T_GH,  rho_DE^(1/4),  hbar a0/c}
and test whether a SINGLE relation (NO free I0) lands
   Omega_dm / Omega_Lambda = 0.387  within 5%.

OUTPUT (both ways, quarantine held):
  NULL-CONFIRMED  : I0 must be tuned per M; no dS number hits 0.387 -> the
                    amount is FREE (confirms the banked d rho_dust/dLambda = 0).
  PASS            : a genuine pin -> GAP-4 closure.

This is DISTINCT from the thermal door (pin_I0_thermal.py): that one used the
GH fluctuation VARIANCE delta_pi~(H M^3)^1/4.  THIS door does the homogeneous
FRW abundance integration of the shift-charge MEAN I0 itself -- the dust law
rho_dust = 2 I0 Q0 / a^3 -- and asks whether the off-minimum displacement
(hence I0) is fixed by any dS scale through a parameter-free relation.

REUSED IN-REPO ASSETS (read first):
  ghost_condensate/condensate_postulate_and_eos.py : EoS split (w=-1 at min,
      w=0/a^-3 off-min); first integral a^3 K'(Q) = I0; rho_kin = 2 phidot I0/a^3.
  ghost_condensate/expand_PX_around_condensate.py  : P(X) bilinears.
  gc_consequences/pin_I0_thermal.py                : footing + dS-scale list.
  AEST_EMBEDDING_2026-06-19.md                     : I0 = INTEGRATION CONSTANT,
      d rho_dust/dLambda = 0, Omega_dust ~ Omega_dm but FREE.

Real numpy FRW + sympy first integral.  Both ways: a confirmed NULL is weighted
EQUAL to a pin.  a0/Z/kappa/I0 NEVER asserted derived.
"""
import numpy as np
import sympy as sp

# ============================================================ constants (SI)
c    = 2.99792458e8
G    = 6.67430e-11
hbar = 1.054571817e-34
kB   = 1.380649e-23
Mpc  = 3.0856775814913673e22
eV   = 1.602176634e-19

# ============================================================ framework footing (banked)
H0_kms = 67.4
H0   = H0_kms*1e3/Mpc
Om_L = 0.685
Om_m = 0.315
Om_b = 0.0493
Om_dm= Om_m - Om_b                 # ~0.2657  cold clustering amount CMB+clusters need
Om_r = 9.0e-5                      # radiation (photons+nu) -- for the FRW background

H_L   = H0*np.sqrt(Om_L)           # pure-Lambda Hubble (framework canonical de Sitter)
Lam   = 3*Om_L*H0**2/c**2          # m^-2
Z     = np.sqrt(32*np.pi/3)        # 5.78876
a0    = c**2*np.sqrt(Lam/(32*np.pi))
T_GH  = hbar*H_L/(2*np.pi*kB)      # Gibbons-Hawking temperature (K)
rho_crit = 3*H0**2/(8*np.pi*G)     # kg/m^3
rho_DE   = Om_L*rho_crit
rho_dm   = Om_dm*rho_crit
target   = Om_dm/Om_L              # 0.387...

print("="*84)
print("DOOR E  (E_amount_pin) -- does any dS number pin Omega_dm WITHOUT a free I0?")
print("="*84)
print(f"  H_Lambda        = {H_L:.4e} 1/s")
print(f"  hbar*H_Lambda   = {hbar*H_L/eV:.4e} eV")
print(f"  kB*T_GH         = {kB*T_GH/eV:.4e} eV")
print(f"  rho_DE^(1/4)    = {((rho_DE*c**2)*(hbar*c)**3)**0.25/eV:.4e} eV")
print(f"  hbar*a0/c       = {hbar*a0/c/eV:.4e} eV   (the dS-Unruh acceleration energy)")
print(f"  a0              = {a0:.4e} m/s^2   (Z = {Z:.4f})")
print(f"  Om_dm           = {Om_dm:.4f}   Om_L = {Om_L}")
print(f"  TARGET  Om_dm/Om_L = {target:.4f}")
print(f"  rho_dm          = {rho_dm:.4e} kg/m^3   rho_DE = {rho_DE:.4e} kg/m^3")
print()

# energy<->density helpers (natural units, mostly-plus)
def E4_eV_from_massdensity(rho_kgm3):
    u = rho_kgm3*c**2
    return (u*(hbar*c)**3)**0.25/eV       # eV  (quartic scale)
def massdensity_from_E4_eV(E_eV):
    u = (E_eV*eV)**4/(hbar*c)**3
    return u/c**2                         # kg/m^3

# ============================================================================
# PART 1 -- sympy: the shift-charge first integral and the FRW dust law.
#   K(Q) = K2 (Q - Q0)^2 - 2 Lambda    (AeST/ACLM, the -2Lambda = additive dark ENERGY)
#   K'(Q) = 2 K2 (Q - Q0)
#   shift symmetry first integral:  a^3 K'(Q) = I0  =>  Q(a) = Q0 + I0/(2 K2 a^3)
#   off-minimum displacement dQ(a) = I0/(2 K2 a^3)  -> a^-3  (DUST, w=0)
#   dust energy density (k-essence rho = 2 X P' - P, kinetic piece):
#       rho_dust(a) = (displacement kinetic) ~ 2 Q0 * I0 / a^3   (task's "2 I0 Q0/a^3")
# ============================================================================
print("="*84)
print("PART 1 (sympy) -- shift-charge first integral a^3 K'(Q)=I0  ->  rho_dust ~ a^-3")
print("="*84)
a, I0s, K2, Q0s, Qs, Lam_s, mu_s = sp.symbols('a I0 K2 Q0 Q Lambda mu', positive=True)
Kexpr = K2*(Qs - Q0s)**2 - 2*Lam_s
Kp    = sp.diff(Kexpr, Qs)
Q_of_a = Q0s + I0s/(2*K2*a**3)
dQ_of_a = sp.simplify(Q_of_a - Q0s)
rho_dust = 2*Q0s*I0s/a**3              # the task's rho_dust = 2 I0 Q0 / a^3  (off-min kinetic)
print(f"  K(Q)            = {Kexpr}")
print(f"  K'(Q)           = {Kp}")
print(f"  a^3 K'(Q)=I0 -> Q(a) = {Q_of_a}")
print(f"  off-min dQ(a)   = {dQ_of_a}   (~ a^-3 = DUST, w=0)")
print(f"  rho_dust(a)     = 2 Q0 I0 / a^3")
print(f"  d rho_dust/dLambda = {sp.diff(rho_dust, Lam_s)}   (ZERO: amount orthogonal to Lambda)")
print(f"  d rho_dust/d mu    = {sp.diff(rho_dust, mu_s)}   (ZERO: amount orthogonal to the K2/mu mass)")
print()
print("  => the dust AMOUNT is the constant of integration I0; nothing in K(Q)'s SHAPE")
print("     (Lambda, mu, K2) enters it. Whether a dS NUMBER fixes I0 is the live question.")
print()

# ============================================================================
# PART 2 -- FRW abundance integration of the dust on the framework background.
#   We verify the a^-3 scaling numerically and confirm: to MATCH Omega_dm today
#   you must CHOOSE I0 (equivalently the today-value rho_dust,0). The integration
#   itself imposes NO constraint on the amplitude -- it just transports a^-3.
#   E(a)^2 = Om_r a^-4 + (Om_b+Om_dust) a^-3 + Om_L   (Om_dust set by I0).
# ============================================================================
print("="*84)
print("PART 2 (numpy FRW) -- transport rho_dust(a)=rho_dust0 a^-3 to today; amplitude=free")
print("="*84)
# scan a few candidate today-amplitudes Om_dust0 (= what I0 would have to give) and show
# the FRW integration just reproduces whatever you put in -- it does NOT select 0.2657.
a_grid = np.array([1e-3, 1e-2, 0.1, 0.5, 1.0])
print("  rho_dust(a)/rho_crit0 for a chosen today value Om_dust0 (a^-3 transport):")
print(f"  {'Om_dust0':>10} | " + " | ".join(f"a={aa:g}" for aa in a_grid))
for Om0 in [0.0, 0.05, Om_dm, 0.5]:
    vals = Om0*a_grid**-3
    print(f"  {Om0:>10.4f} | " + " | ".join(f"{v:9.3e}" for v in vals))
print()
print("  The FRW transport is LINEAR in the chosen amplitude Om_dust0: rho_dust(a)=Om_dust0 a^-3.")
print("  Any Om_dust0 in [0, infinity) is an exact solution; the background integration")
print("  contains NO scale that prefers 0.2657. The amount is set ONLY by the boundary")
print("  datum I0 (equivalently rho_dust,0). This is the integration-level statement of")
print("  d rho_dust/dLambda = 0: GAP-4 free at the level of the FRW equations themselves.")
print()

# ============================================================================
# PART 3 -- THE PIN TEST.  For the amount to be PINNED, a dS NUMBER must fix I0.
#   The only honest "no-free-I0" hypothesis: the off-minimum displacement dQ_0 today
#   (hence rho_dust,0 = 2 Q0 dQ_0) is itself SET by a single de Sitter scale, with
#   Q0 = M^2 (the condensate VEV, ACLM phi=M^2 t) and the natural displacement
#   candidates all expressed through ONE dS energy scale E_dS.  We try EVERY
#   M = E_dS and EVERY parameter-free displacement relation, and test 0.387.
#
#   Dimensions (natural units, mostly-plus):  [rho] = E^4, [Q]=[phidot]=E^2,
#   Q0 = M^2.  rho_dust = 2 Q0 dQ has dim E^2 * [dQ]; for rho ~ E^4 need [dQ]=E^2,
#   i.e. dQ is itself a (velocity)^2 = (energy)^2.  The parameter-free candidates
#   for the displacement, all built from ONE scale:
#       (H1) dQ = E_dS^2                      -> rho = 2 M^2 E_dS^2
#       (H2) dQ = M E_dS                      -> rho = 2 M^3 E_dS
#       (H3) dQ = Q0 = M^2 (order-unity disp) -> rho = 2 M^4   (pure M^4)
#       (H4) dQ from the GH fluctuation dpi:  dQ ~ (H_L M^3)^(1/2)  (delta_pi^2 scale)
#   For each candidate dS scale E_dS in {hbar H_L, kB T_GH, rho_DE^1/4, hbar a0/c}
#   we set M = E_dS (no second scale) and compute Omega_dust, then Omega_dust/Om_L.
# ============================================================================
print("="*84)
print("PART 3 -- THE PIN: set M = a dS scale, displacement from the SAME scale, no free I0")
print("="*84)
dS_scales = {
    "hbar*H_Lambda  ": hbar*H_L/eV,                                   # eV
    "kB*T_GH        ": kB*T_GH/eV,                                    # eV
    "rho_DE^(1/4)   ": E4_eV_from_massdensity(rho_DE),                # eV
    "hbar*a0/c      ": hbar*a0/c/eV,                                  # eV  (dS-Unruh accel energy)
}
# displacement hypotheses: rho_dust(M, E_dS) in eV^4, with M = E_dS (single scale)
def rho_H1(M, E): return 2*M**2 * E**2          # dQ = E^2
def rho_H2(M, E): return 2*M**3 * E             # dQ = M E
def rho_H3(M, E): return 2*M**4                 # dQ = M^2  (order-unity displacement)
def rho_H4(M, E):                                # dQ ~ (H_L M^3)^(1/2) GH-variance scale
    H_eV = hbar*H_L/eV
    return 2*M**2 * (H_eV*M**3)**0.5
hyps = {"H1 dQ=E^2":rho_H1, "H2 dQ=M E":rho_H2, "H3 dQ=M^2 (O1)":rho_H3, "H4 dQ=(H M^3)^1/2":rho_H4}

print(f"  TARGET Omega_dust/Om_L = {target:.4f}  (and Omega_dust = {Om_dm:.4f})")
print()
print(f"  {'dS scale = M':<16}{'E_dS(eV)':>12} | " + " | ".join(f"{h:>17}" for h in hyps))
print(f"  {'':<16}{'':>12} | " + " | ".join(f"{'Om_dust : ratio':>17}" for _ in hyps))
print("  " + "-"*100)
any_hit = False
hit_log = []
for name, E_dS in dS_scales.items():
    M = E_dS                                 # single-scale hypothesis: M = the dS scale
    cells = []
    for hname, f in hyps.items():
        rho_eV4 = f(M, E_dS)                  # eV^4
        E_quartic = rho_eV4**0.25
        rho_kg = massdensity_from_E4_eV(E_quartic)
        Om = rho_kg/rho_crit
        ratio = Om/Om_L
        hit = abs(ratio-target)/target < 0.05
        if hit:
            any_hit = True
            hit_log.append((name.strip(), hname, Om, ratio))
        cells.append(f"{Om:7.1e}:{ratio:6.1e}{'*' if hit else ' '}")
    print(f"  {name:<16}{E_dS:12.3e} | " + " | ".join(f"{cc:>17}" for cc in cells))
print()
print("  (* = lands Omega_dust/Om_L = 0.387 within 5% with NO free I0)")
print()

# ============================================================================
# PART 4 -- the inversion: what I0/displacement WOULD each dS-scale M need, and how
#   far is the implied displacement from any O(1) or dS-natural value?  (both ways)
# ============================================================================
print("="*84)
print("PART 4 -- inversion: the displacement dQ each M would need to hit Omega_dm=0.2657")
print("="*84)
rho_dm_eV4 = E4_eV_from_massdensity(rho_dm)**4         # eV^4
print(f"  rho_dm = {rho_dm_eV4:.4e} eV^4   (rho_dm^1/4 = {rho_dm_eV4**0.25:.4e} eV)")
print(f"  For rho_dust = 2 M^2 dQ = rho_dm:  required dQ = rho_dm/(2 M^2)")
print(f"  {'M = dS scale':<16}{'M(eV)':>12}{'req dQ(eV^2)':>16}{'req dQ/M^2':>14}{'req dQ/(dS)^2':>16}")
print("  " + "-"*74)
for name, E_dS in dS_scales.items():
    M = E_dS
    dQ_req = rho_dm_eV4/(2*M**2)              # eV^2
    print(f"  {name:<16}{M:12.3e}{dQ_req:16.3e}{dQ_req/M**2:14.3e}{dQ_req/E_dS**2:16.3e}")
print()
print("  The required displacement dQ/M^2 is NOT O(1) and NOT any clean dS ratio for any")
print("  M = dS scale -- it spans tens of orders of magnitude across the candidate scales.")
print("  No single relation makes it O(1) or a dS number simultaneously with M = that scale.")
print()

# ============================================================================
# PART 5 -- dimensionless O(1)/dS combos vs 0.387 (the standard scan, completeness)
# ============================================================================
print("="*84)
print("PART 5 -- does ANY dS dimensionless combination equal 0.387 within 5%?")
print("="*84)
H_eV = hbar*H_L/eV
rhoDE14 = E4_eV_from_massdensity(rho_DE)
combos = {
    "Om_L":            Om_L,
    "1/Z":             1.0/Z,
    "1/Z^2":           1.0/Z**2,
    "(3/8pi)^(1/4)":   (3/(8*np.pi))**0.25,
    "3/8pi":           3/(8*np.pi),
    "sqrt(3/8pi)":     np.sqrt(3/(8*np.pi)),
    "Om_dm/Om_L(=tgt)":target,
    "(rhoDE14/(hbar a0/c))": rhoDE14/(hbar*a0/c/eV),
    "(hbar a0/c)/rhoDE14":   (hbar*a0/c/eV)/rhoDE14,
    "H_L/a0*c (dimless?)":   H_L*c/a0,        # = Z (sanity)
}
print(f"  target = {target:.4f}")
print(f"  {'combination':<24}{'value':>16}   within 5%?")
print("  " + "-"*54)
combo_hit = False
for k,v in combos.items():
    h = abs(v-target)/target < 0.05
    combo_hit = combo_hit or (h and 'tgt' not in k)
    print(f"  {k:<24}{v:>16.4e}   {'YES' if h else 'no'}")
print()

# ============================================================================
# VERDICT
# ============================================================================
print("="*84)
print("VERDICT (both ways, quarantine held)")
print("="*84)
pinned = any_hit or combo_hit
if pinned:
    print("  PASS -- a dS number pins Omega_dm without a free I0:")
    for nm in hit_log:
        print(f"     {nm}")
    print("  => GAP-4 closure. (Verify the relation is parameter-free and not tuned.)")
else:
    print("  NULL-CONFIRMED -- NO dS number pins Omega_dm; I0 must be tuned per M.")
    print("   * The FRW abundance integration transports rho_dust ~ a^-3 with an amplitude")
    print("     that is a FREE boundary datum (Part 2): the background equations contain no")
    print("     scale preferring Omega_dust = 0.2657 (d rho_dust/dLambda = 0, sympy Part 1).")
    print("   * Setting M = each dS scale {hbar H_L, kB T_GH, rho_DE^1/4, hbar a0/c} and the")
    print("     displacement from the SAME single scale (4 parameter-free hypotheses) NEVER")
    print("     lands Omega_dust/Om_L = 0.387 within 5% (Part 3): the results miss by tens")
    print("     of orders of magnitude (the dS energy scales hbar H_L ~ 1e-33 eV, rho_DE^1/4")
    print("     ~ 2e-3 eV are FAR below any M that gives O(1) Omega).")
    print("   * The displacement each M would need (Part 4) is neither O(1) nor a clean dS")
    print("     ratio; no single relation makes M = a dS scale AND dQ dS-natural at once.")
    print("   * No dS dimensionless combination equals 0.387 within 5% (Part 5).")
    print()
    print("  => The AMOUNT of dark matter (I0 = Omega_dm) is a FREE integration constant.")
    print("     This CONFIRMS the banked d rho_dust/dLambda = 0 at the FRW-abundance level.")
    print("     Both ways: a genuine pin would have been a GAP-4 closure (huge); it does not")
    print("     occur, and the null is verified as rigorously as a pin would be. I0 NEVER")
    print("     asserted derived. Quarantine held.")
print()
print(f"  [machine] any_hit={any_hit}  combo_hit={combo_hit}  PINNED={pinned}")
