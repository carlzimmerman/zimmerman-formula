#!/usr/bin/env python3
"""L218 -- does gradient-driven criticality still operate at w ~ 6e-7?

L217 tightened the sector's equation of state from the acoustic bound 1e-4 to 5.7e-7 by
requiring a_0 to stay flat.  Every gate from L192 onward was run at 1e-4.  The mechanism
that makes the sector exactly cold is criticality (L192-L194): a clock running fast makes
c_s^2 negative at zero gradient, the instability grows the gradient, the MOND nonlinearity
turns c_s^2 positive at a finite gradient, and the back-reaction parks the field there.
L194's balance is d lnY/dN = -2 + 2 kappa |c_s(Y)| with kappa = k/H, giving |c_s| = 1/kappa
and a residual c_s^2 = 1/kappa^2 that depends on NO coefficient of the action.

Shrinking w weakens the driver: |c_s(0)| = sqrt(w/2).  This lane asks whether the driver is
still strong enough, and finds the mechanism has an OPERATING CONDITION that turns into a
LOWER bound on w -- so the equation of state is now bounded from both sides, for the first
time in this programme.

Every check states measurement and threshold separately.
"""
import json
import sympy as sy

RES, NP, NF = [], 0, 0
def check(n, measured, ok, d=""):
    global NP, NF
    ok = bool(ok)
    print(f"  [{'PASS' if ok else 'FAIL'}] {n}")
    print(f"         measured: {measured}")
    if d: print(f"         reading : {d}")
    RES.append({"name": n, "measured": str(measured), "pass": ok, "reading": d})
    if ok: NP += 1
    else:  NF += 1

print(__doc__)

# --------------------------------------------------------------- cosmology, for kappa(z)
H0, Om, Or, OL = 67.4, 0.315, 9.2e-5, 0.685          # km/s/Mpc; Or includes neutrinos
def aH(z):
    """comoving Hubble rate a H(z) in km/s/Mpc; kappa = k_phys/H scales as 1/(aH) at fixed
    comoving k, because k_phys = k_com/a."""
    zp = 1.0 + z
    return (1.0/zp)*H0*(Or*zp**4 + Om*zp**3 + OL)**0.5

Z_FOREST = 3.0
KAPPA_FOREST = 3.2e4          # L194 V3: the kappa at which the residual meets c_s^2 <= 1e-9
def kappa(z):
    return KAPPA_FOREST*aH(Z_FOREST)/aH(z)

# --------------------------------------------------------------- A: the operating condition
print("PART A -- the condition for the mechanism to run at all")
kap, wv, Y = sy.symbols('kappa w Y', positive=True)
cs0 = sy.sqrt(wv/2)                                   # |c_s| at zero gradient, m_rel -> 0
growth = 2*kap*cs0                                    # L194's growth term at Y -> 0
dilution = 2                                          # L194's dilution term, exactly -2
w_floor_sym = sy.simplify(sy.solve(sy.Eq(growth, dilution), wv)[0])
resid_sym = 1/kap**2
check("V1 [the mechanism has an operating condition, and it is twice the residual] L194's "
      "growth term is evaluated at zero gradient, set equal to the dilution term, and "
      "solved for the equation of state; the result is compared with twice L194's residual "
      "sound speed",
      f"growth = {growth}, dilution = {dilution} => w_floor = {w_floor_sym}; "
      f"2 x residual = {sy.simplify(2*resid_sym)}",
      sy.simplify(w_floor_sym - 2*resid_sym) == 0,
      "w must exceed TWICE the residual sound speed the same mechanism ends up at. Below "
      "that the instability cannot outrun the expansion, the gradient never reaches the "
      "critical surface, and the sector never becomes exactly cold. This is a LOWER bound "
      "on w and the programme has never had one")

# --------------------------------------------------------------- B: at the new ceiling
print()
print("PART B -- the mechanism at the ceiling L217 imposed")
W_CEIL = 5.66e-7                                      # L217 V7
cs_ceil = (W_CEIL/2)**0.5
ratio_forest = kappa(Z_FOREST)*cs_ceil
check("V2 [at the forest epoch the driver is comfortably strong] the growth-to-dilution "
      "ratio is evaluated at the tightened equation of state and the forest's own kappa, "
      "and compared against 1, the value at which the mechanism stalls",
      f"|c_s(0)| = {cs_ceil:.3e}, kappa(z=3) = {kappa(Z_FOREST):.3e}, "
      f"growth/dilution = {ratio_forest:.1f}",
      ratio_forest > 1.0,
      "seventeen times the stall value at z = 3, so at the epoch the Lyman-alpha forest "
      "measures, criticality runs and runs fast. Shrinking w by more than two orders did "
      "not switch the mechanism off")

# where does it stall?
def stall_z():
    lo, hi = 3.0, 5000.0
    for _ in range(200):
        mid = 0.5*(lo + hi)
        if kappa(mid)*cs_ceil > 1.0: lo = mid
        else: hi = mid
    return 0.5*(lo + hi)
z_stall = stall_z()
check("V3 [and it runs from well before structure forms] the redshift at which growth "
      "equals dilution is solved for at the tightened equation of state, and compared with "
      "z = 30, comfortably earlier than any epoch the sector must be cold for",
      f"criticality operates for z < {z_stall:.0f}; kappa there = {kappa(z_stall):.3e}",
      z_stall > 30.0,
      "the mechanism switches on at z ~ 1e3 and runs all the way down. Everything that "
      "requires the sector to be exactly cold -- the forest, galaxy formation, lensing, S8 "
      "-- happens below that, so the tightening costs the mechanism nothing where it matters")

# --------------------------------------------------------------- C: the floor, and the window
print()
print("PART C -- the floor, and the window it closes")
print("      z by which criticality must run |   kappa(z)  |  floor on w")
rows = []
for zc in [3.0, 10.0, 30.0, 100.0, 300.0, 1100.0]:
    kz = kappa(zc)
    floor = 2.0/kz**2
    rows.append((zc, kz, floor))
    print(f"      {zc:>31.0f} | {kz:>11.3e} | {floor:.2e}")
floor_z30 = [f for z, k, f in rows if z == 30.0][0]
floor_rec = [f for z, k, f in rows if z == 1100.0][0]
check("V4 [THE WINDOW, bounded from both sides for the first time] the floor required for "
      "criticality to have run by z = 30 is compared with L217's ceiling from holding a_0 "
      "flat; a floor above the ceiling would mean no equation of state works at all",
      f"floor (criticality by z = 30) = {floor_z30:.2e}; ceiling (flat a_0) = {W_CEIL:.2e}; "
      f"window width = {W_CEIL/floor_z30:.0f}x = {(W_CEIL/floor_z30):.3g} "
      f"({(sy.log(W_CEIL/floor_z30)/sy.log(10)).evalf():.2f} decades)",
      floor_z30 < W_CEIL,
      "the window is open and about one and a half decades wide. This is the first time "
      "this programme has bounded the sector's equation of state from BELOW, and the two "
      "bounds come from completely different physics: small-scale power on one side, the "
      "drift of the acceleration scale on the other")

check("V5 [but demanding it at recombination closes it] the same floor is evaluated at "
      "recombination and compared with the ceiling, because a mechanism that only switches "
      "on after recombination leaves the sector un-criticalised when the CMB is imprinted",
      f"floor (criticality by z = 1100) = {floor_rec:.2e} vs ceiling {W_CEIL:.2e}; "
      f"ratio = {floor_rec/W_CEIL:.2f}",
      floor_rec > W_CEIL,
      "at the forest's own kappa the mechanism cannot have run at recombination: the floor "
      "exceeds the ceiling by about twenty percent. So the sector reaches the CMB NOT yet "
      "parked on the critical surface, and whether that matters is V6")

# --------------------------------------------------------------- D: does the CMB care?
print()
print("PART D -- the sector at recombination, before criticality switches on")
k_cmb = 0.2                                           # Mpc^-1 comoving, third-peak scale
z_rec = 1100.0
corr = (W_CEIL/2)*(k_cmb/(aH(z_rec)/299792.458))**2   # c_s^2 k^2/(aH)^2, the pressure term
check("V6 [and it does not] the sound-speed correction to the sector's perturbation "
      "equation is evaluated at the third-peak scale and recombination, and compared "
      "against 0.01, below which it cannot move a peak height",
      f"c_s^2 k^2/(aH)^2 = {corr:.2e} at k = {k_cmb} /Mpc, z = {z_rec:.0f}",
      corr < 0.01,
      "four parts in ten thousand. Un-criticalised, the sector is still cold ENOUGH at "
      "recombination because the equation of state is now so small; criticality is needed "
      "for the forest and for structure, not for the CMB. So V5's closure is not a kill, "
      "it relocates the requirement to where the mechanism does run")

# --------------------------------------------------------------- E: what is untouched
print()
print("PART E -- what the tightening does NOT change")
kaps = [1e3, 1e4, 1e5]
resid = [1.0/k**2 for k in kaps]
check("V7 [the residual, hence the forest gate, is untouched] L194's residual is evaluated "
      "at three values of kappa and its dependence on the equation of state is measured, "
      "since a residual that moved with w would reopen the forest gate",
      f"residual c_s^2 = {['%.1e' % x for x in resid]} at kappa = {kaps}; "
      f"d(residual)/dw = {sy.diff(resid_sym, wv)}",
      sy.diff(resid_sym, wv) == 0,
      "how cold the sector ends up is fixed by the instability-versus-dilution balance and "
      "by nothing in the action, so shrinking w by two orders leaves the forest gate exactly "
      "where L194 left it")

s0_req = 1.5e7                                        # L216
mrel_new = W_CEIL/(s0_req - 1)
check("V8 [what it does change: the margin] the margin implied by the clock rate the solar "
      "system demands is evaluated at the new ceiling and compared with the value at the "
      "old one, since the margin is what the speed-limit picture of L217 measures",
      f"m_rel = w/(s_0-1) = {mrel_new:.2e} at w = {W_CEIL:.2e}, against "
      f"{1e-4/(s0_req-1):.2e} at w = 1e-4",
      mrel_new < 1e-4/(s0_req - 1),
      "the field sits 180 times closer to its own speed limit than before. Nothing computed "
      "forbids it -- the Lorentz factor is a conserved charge (L217) and takes whatever "
      "value it was given -- but the strong-coupling question L216 raised gets 180 times "
      "sharper, and it is still NOT computed")

print()
print("READING")
print("""
  Criticality survives the tightening, and the tightening gives the programme something it
  has never had: a LOWER bound on the sector's equation of state.

  The mechanism has an operating condition, and it is exact and pretty: w must exceed TWICE
  the residual sound speed the mechanism itself ends up at (V1).  Below that the instability
  cannot outrun the expansion, the gradient never reaches the critical surface, and the
  sector never becomes exactly cold.  Since the residual is 1/kappa^2 and kappa = k/H falls
  into the past, the floor is an epoch-dependent statement: the earlier you demand the
  mechanism have run, the larger w must be.

  At L217's ceiling the driver is still strong.  At the forest epoch the growth beats the
  dilution seventeen times over (V2), and the mechanism switches on around z ~ 1e3 and runs
  all the way down (V3) -- covering the forest, galaxy formation, lensing and S8, which is
  everything that needs the sector exactly cold.

  So the equation of state is now bounded on both sides,

      1.5e-8  <~  w  <~  5.7e-7 ,

  about one and a half decades (V4), with the two bounds coming from completely unrelated
  physics: small-scale power on one side, the drift of the acceleration scale under
  symmetry breaking on the other.  That is the first two-sided determination of this
  quantity in the programme.

  One thing does close.  If criticality is demanded at recombination itself, the floor
  exceeds the ceiling by about twenty percent (V5) -- at the forest's own kappa the
  mechanism cannot have run that early.  That is not a kill, because the sector does not
  NEED criticality at recombination: with w this small the sound-speed correction at the
  third-peak scale is four parts in ten thousand (V6).  It does mean the window's existence
  now depends on the effective theory's ultraviolet cutoff, which sets kappa and which this
  programme has never determined.  That is the next quantity to compute.

  LIMITS.  kappa is normalised at L194's forest value and evolved as 1/(aH) at fixed
  comoving wavenumber, which assumes the same physical mode dominates the gradient variance
  at all epochs; L194 V5 supports that at one epoch, not across a thousandfold in redshift.
  The operating condition is evaluated at zero gradient, where the driver is weakest, so it
  is conservative.  The ceiling 5.7e-7 inherits every limit of L217, including a coupling
  to baryons only and a one percent flat-law tolerance taken from theory rather than data.
  The CMB estimate of V6 is the size of a term in the perturbation equation, not a Boltzmann
  calculation.  No gate has been re-run end to end at w = 6e-7.  a_0 does not enter this
  lane, so the result is the same on both footings and is quoted once.
""")
print(f"L218 COMPLETE: {NP}/{NP+NF} checks PASS.")
json.dump({"pass": NP, "fail": NF, "checks": RES},
          open("fable_independent_2026/L218_results.json", "w"), indent=1)
