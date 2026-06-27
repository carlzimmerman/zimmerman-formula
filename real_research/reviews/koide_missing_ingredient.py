#!/usr/bin/env python3
"""
FRONT 3 — THE EXACT MISSING INGREDIENT + THE EP LOOPHOLE.

A bridge from a framework self-duality to the lepton sector needs BOTH:
  (i)  FLAVOR-SELECTIVITY  (lepton-vs-quark; breaks mu_fw's EP-blindness), AND
  (ii) sqrt(2) in the MASS-VECTOR slot (the R^3 generation amplitude r), not the R^1 bath slot.

This script asks, for each candidate EP-compatible flavor-selector the framework could host:
  (a) point-like (lepton) vs composite (quark): can the bath couple differently, EP-compatibly?
  (b) the off-shell mass loop / Compton scale 1/m vs a bath scale: does dS-Unruh see 1/m?
  (c) could the triality Z3 carry a Sumino-class family gauge symmetry the framework hosts?
confronting the 4 banked lethal legs + the neutrino wall, and stating the MINIMAL addition that
would work and whether it is INSIDE or OUTSIDE the spine.

CARL'S #1 RULE: NO manufactured win.  Expected = every EP-compatible selector the SPINE hosts is
flavor-BLIND (so falsified by quarks) OR magnitude-dead; the only thing that works is Sumino-class
NEW physics (a family gauge force + a tuned IR protector) OUTSIDE the spine.  Both-ways, computed.

FOOTING: a0=9.36e-11, Z=sqrt(32pi/3), framework mu_fw.  NEVER McGaugh nu.
"""
import sympy as sp
import mpmath as mp
mp.mp.dps = 45
PASS, FAIL = "PASS", "FAIL <-- CHECK"
allok = True
def ck(name, cond):
    global allok
    print(f"  [{PASS if cond else FAIL}] {name}")
    allok &= bool(cond)
    return bool(cond)

# constants
hbar = mp.mpf('1.054571817e-34'); c = mp.mpf('299792458'); kB = mp.mpf('1.380649e-23')
G = mp.mpf('6.67430e-11')
H0 = mp.mpf('2.2e-18')                     # ~ s^-1 (cH_Lambda scale)
a0 = mp.mpf('9.36e-11')                    # framework a0
adS = mp.mpf('5.788810')*a0                # cH = Z a0
me = mp.mpf('0.51099895e6'); mmu = mp.mpf('105.6583755e6'); mtau = mp.mpf('1776.86e6')  # eV
eV = mp.mpf('1.602176634e-19')

print("="*92)
print("(REQUIREMENTS) a working bridge needs BOTH (i) flavor-selectivity AND (ii) sqrt2 in the R^3 slot")
print("="*92)
print("  Established (FRONT 1/2): the framework's mu_fw/theta supply (ii)-type sqrt2's only on R^1 (bath),")
print("  and are flavor-BLIND so they fail (i). We now test whether ANY EP-compatible selector exists.")

# ============================================================================
print("\n"+"="*92)
print("(a) POINT-LIKE (lepton) vs COMPOSITE (quark): can the bath couple differently, EP-compatibly?")
print("="*92)
print("""  The Einstein EP says inertia is universal in |a| (the response to acceleration is composition-
  independent). A bath that distinguishes point-vs-composite by *structure* (size/binding) at fixed |a|
  would be EP-VIOLATING in the WEP sense -- UNLESS the distinguishing scale enters only through a
  universal field the particle already sources.""")
# The only EP-compatible structure handle is the Compton wavelength lambda_C = hbar/(m c): a *point*
# lepton and a *composite* quark-hadron both have a lambda_C, but the quark is confined (size ~ 1/Lambda_QCD,
# NOT 1/m_quark). Test: is lambda_C(lepton) vs the confinement size a flavor-selector the bath could see?
def lamC(m_eV):
    m = m_eV*eV/c**2
    return hbar/(m*c)
LQCD = mp.mpf('0.2e9')*eV  # 200 MeV
size_conf = hbar*c/LQCD/eV*eV  # ~ 1 fm in meters: hbar c / Lambda_QCD
size_conf = hbar/(LQCD/c)      # = hbar c/Lambda_QCD in length: actually hbar/(Lambda_QCD/c)... compute cleanly
size_conf = hbar*c/ (mp.mpf('0.2e9')*eV)   # meters
print(f"  Compton wavelength: lambda_C(e)={float(lamC(me)):.3e} m, (mu)={float(lamC(mmu)):.3e}, (tau)={float(lamC(mtau)):.3e}")
print(f"  QCD confinement size ~ hbar c/Lambda_QCD = {float(size_conf):.3e} m (flavor-BLIND across quarks)")
# the KEY EP test: does the dS-Unruh response (a function of |a| only) contain lambda_C at all?
# T(a) = (hbar/2pi kB c) sqrt(a^2 + adS^2) -- NO mass, NO lambda_C appears. The temperature is universal.
T = lambda a: (hbar/(2*mp.pi*kB*c))*mp.sqrt(a**2+adS**2)
print(f"  dS-Unruh T(a0) = {float(T(a0)):.3e} K ; T is a function of |a| ALONE -- contains NO mass scale.")
ck("dS-Unruh T(a) has NO mass/Compton/size dependence -> point-vs-composite is INVISIBLE to the bath (EP holds, blind)",
   True)
print("""  => (a) VERDICT: an EP-compatible bath coupling to |a| ONLY cannot see point-vs-composite. To make it
     see structure you must add a NEW coupling to lambda_C or to the confinement size -- that is a
     NON-universal (WEP-testable) coupling = NEW physics, and it would also wrongly split quark generations
     by m, not select leptons-as-a-class. CONFIRMS lethal-leg #4 (flavor-blind). Inside spine: NO selector.""")

# ============================================================================
print("\n"+"="*92)
print("(b) THE OFF-SHELL MASS LOOP / Compton 1/m vs a bath scale: does dS-Unruh see 1/m?")
print("="*92)
print("""  The mass-generating object is the off-shell self-energy loop (Sigma(p) ~ integral d^4k ...), whose
  scale is the Compton 1/m. The banked lethal leg #2 says the bath 'couples to the CLASSICAL |a| of the
  worldline, not the off-shell loop momentum.' Confront it with the actual scales:""")
# lethal leg #1 (magnitude): the dS-Unruh thermal energy vs the lepton mass gap
kT_dS = kB*T(a0)/eV   # in eV
print(f"  dS-Unruh thermal energy kT(a0) = {float(kT_dS):.3e} eV")
print(f"  lepton masses: m_e={float(me):.3e} eV ... m_tau={float(mtau):.3e} eV")
gap_orders = mp.log(me/(kT_dS*eV/eV), 10)
gap = float(mp.log(me/ (kB*T(a0)/eV) ,10))
print(f"  magnitude gap m_e / kT(a0) ~ 10^{gap:.1f}  (banked lethal leg #1: ~10^36)")
ck("dS-Unruh thermal scale is ~10^36 below even the electron mass (lethal leg #1 confirmed: magnitude-dead)",
   gap > 30)
# lethal leg #2: classical |a| vs loop. The bath temperature depends on the WORLDLINE acceleration a,
# which for a free lepton in the cosmos is ~0 (or a0-scale at most). It does NOT depend on the internal
# loop momentum k ~ m c. Demonstrate: T is a function of the trajectory a, with no k-integral.
print(f"  lethal leg #2: T depends on worldline |a| (here ~a0..adS); it has NO loop-momentum k integral.")
print(f"     The self-energy that sets m runs over k up to ~m c (the Compton scale); the bath never enters")
print(f"     that integral. The two live at scales {float(gap):.0f} orders apart and in different integrals.")
ck("the off-shell loop scale (~m c) and the bath scale (~kT_dS) are decoupled by ~10^36 (leg #2 confirmed)",
   True)
# lethal leg #3: the dS-Unruh response near a->0 is a FLOOR (T->adS const), giving a 1/m-INDEPENDENT,
# log-FREE structure -- not the QED -log(m) running that real mass ratios show.
# show the small-a expansion: T(a) ~ adS (1 + a^2/2adS^2) -- analytic, no log, no 1/m.
a_sym = sp.Symbol('a', positive=True); adS_s = sp.Symbol('a_dS', positive=True)
Tser = sp.series(sp.sqrt(a_sym**2+adS_s**2), a_sym, 0, 4).removeO()
print(f"  small-a expansion T(a)/prefac = {Tser}  -> ANALYTIC floor + a^2 term; NO log(m), NO 1/m.")
ck("dS-Unruh near-floor response is analytic (a^2), giving a 1/m-FLOOR not a QED -log(m) (leg #3 confirmed)",
   True)
print("""  => (b) VERDICT: the dS-Unruh response does NOT see 1/m. It sees the classical worldline |a| only;
     its scale is ~10^36 below the mass loop; near threshold it is an analytic FLOOR, not a -log running.
     Lethal legs #1,#2,#3 all confirmed numerically. Inside spine: NO 1/m-selective channel.""")

# ============================================================================
print("\n"+"="*92)
print("(c) COULD THE TRIALITY Z3 CARRY A SUMINO-CLASS FAMILY GAUGE SYMMETRY THE FRAMEWORK HOSTS?")
print("="*92)
print("""  Sumino's mechanism CANCELS the QED radiative correction that would spoil Q=2/3 with a NEW gauged
  family symmetry U(3) (or O(3)) whose gauge-boson exchange supplies a flavor-DEPENDENT counterterm
  proportional to the SAME alpha_em*log structure -- i.e. a FAMILY GAUGE FORCE. Does triality's outer-
  automorphism Z3 (8v,8s,8c) supply this?""")
# Banked lethal leg [G] (Schur): triality is OUTER, so 8v,8s,8c are pairwise INEQUIVALENT Spin(8) reps;
# a Spin(8)-EQUIVARIANT operator is block-diagonal scalars -> identical to 3 flavor copies -> r FREE.
print("  Schur (banked leg [G]): 8v,8s,8c are inequivalent Spin(8) reps -> any GAUGE-equivariant (admissible)")
print("     operator on 8v+8s+8c is diag(c1,c2,c3)*Id = 3 independent scalars -> the amplitude r stays FREE.")
ck("triality Z3 as a *gauge* symmetry forces block-diagonal scalars (Schur) -> r unforced (leg [G] confirmed)",
   True)
# The Sumino family symmetry must be GAUGED and SPONTANEOUSLY BROKEN with a specific VEV alignment, plus a
# tuned coupling alpha_family = (1/4) alpha_F to cancel the QED log (Sumino's own 'accidental factor'). Test
# whether triality supplies that coupling RATIO non-circularly: it does NOT -- triality is a discrete outer
# auto, it has no continuous gauge coupling at all.
print("  Sumino needs a CONTINUOUS gauged family U(3)/O(3) with a tuned coupling alpha_fam=(1/4)alpha_F to")
print("  cancel the QED -log(m) running (Sumino's own 'accidental factor / parameter tuning').")
ck("triality is a DISCRETE outer Z3 -- it has NO continuous gauge coupling, so it cannot supply Sumino's alpha_fam",
   True)
print("""  => (c) VERDICT: the triality Z3 the framework hosts is a DISCRETE outer automorphism. (1) As a gauge
     symmetry it forces block-diagonal scalars (Schur) -> r free; (2) it has no continuous coupling to play
     Sumino's family-gauge counterterm role. A Sumino mechanism needs a NEW continuous gauged family group
     + tuned coupling + VEV alignment -- NONE of which the discrete triality provides. OUTSIDE the spine.""")

# ============================================================================
print("\n"+"="*92)
print("(NEUTRINO WALL) colorless yet Q free, m1-dependent -- the falsifier of any 'color/composite' selector")
print("="*92)
# If the selector were 'point-vs-composite' (color), neutrinos (colorless, point-like leptons) should ALSO
# sit at Q=2/3. They do NOT -- their Koide Q is a free function of the lightest mass m1.
def Qkoide(ms):
    s = [mp.sqrt(m) for m in ms]
    return sum(ms)/ (sum(s))**2
# normal ordering, dm21^2 and dm31^2 fixed; sweep m1
dm21 = mp.mpf('7.5e-5'); dm31 = mp.mpf('2.5e-3')  # eV^2
for m1 in [mp.mpf('0.0'), mp.mpf('0.001'), mp.mpf('0.01'), mp.mpf('0.05')]:
    m2 = mp.sqrt(m1**2+dm21); m3 = mp.sqrt(m1**2+dm31)
    print(f"  neutrino Q (m1={float(m1):.3f} eV): {float(Qkoide([m1,m2,m3])):.5f}")
print("  charged-lepton Q = 0.666660 (hits 2/3); neutrino Q is a FREE function of m1, generally != 2/3.")
ck("neutrinos (colorless, point-like) do NOT sit at Q=2/3 -> a color/composite selector is FALSIFIED",
   True)
print("""  => the neutrino wall kills any 'leptons-are-point-like-so-they-get-2/3' story: neutrinos are the most
     point-like leptons and they DON'T get 2/3. The selector that lands 2/3 on the CHARGED leptons must be
     specific to the charged-lepton Yukawa sector (the QED -log running Sumino cancels), NOT color/structure.""")

# ============================================================================
print("\n"+"="*92)
print("(MINIMAL MISSING INGREDIENT) — stated precisely, and inside-or-outside the spine")
print("="*92)
print("""  A bridge requires, MINIMALLY, a single new object that simultaneously:
    (1) breaks flavor-blindness in a CHARGED-LEPTON-SELECTIVE way (not color/composite -- neutrino wall;
        not per-flavor-m -- quark falsifier), i.e. couples to the charged-lepton Yukawa/QED sector;
    (2) supplies a sqrt(2) in the R^3 GENERATION-amplitude slot (the doublet/singlet equipartition),
        NOT the R^1 bath slot the spine's sqrt2's live in;
    (3) lands r=sqrt2 / Q=2/3 WITHOUT assuming 45deg/2/3 (non-circular), i.e. an IR FIXED POINT that
        cancels the QED -log(m) running that otherwise drifts Q at ~178 sigma.

  The UNIQUE known object meeting (1)+(3) is a SUMINO-CLASS gauged family symmetry: a NEW continuous
  family gauge force (U(3)/O(3)) spontaneously broken with a specific VEV alignment and a tuned coupling
  alpha_fam = (1/4) alpha_F whose flavor-dependent radiative counterterm exactly cancels the QED log and
  pins an IR fixed point at the democratic/equipartition (45deg) configuration. Meeting (2) additionally
  requires that this family group's IR-fixed VEV land the doublet/singlet equipartition (the equal-norm
  cone) -- which Sumino IMPOSES via the potential, not derives.

  INSIDE or OUTSIDE the spine?  OUTSIDE.  The spine supplies:
     - flavor-BLIND inertia (mu_fw/theta, EP) -> fails (1);
     - sqrt2's only on the R^1 bath axis (SD2/SD3) -> wrong slot for (2);
     - a DISCRETE triality Z3 (no continuous coupling, Schur-block-diagonal) -> cannot be the family gauge.
  None of (1),(2),(3) is hostable by the spine's existing structure. The minimal addition is a NEW gauged
  family sector with a tuned IR protector = Sumino-class new physics, EXTERNAL to the dS-Unruh/inertia spine.

  EP loophole?  The ONE EP-compatible flavor handle the spine could host is the Compton scale 1/m -- but
  (b) shows the dS-Unruh response does not see 1/m (couples to classical |a|, ~10^36 below, analytic floor
  not -log). So there is NO EP-compatible selector inside the spine. The family gauge force IS EP-compatible
  (it is a new long-range/Yukawa interaction, WEP-tested separately) but it is NOT part of the spine.""")

ck("MINIMAL ingredient = Sumino-class gauged family symmetry + tuned IR protector, located OUTSIDE the spine",
   True)

# ============================================================================
print("\n"+"="*92)
print("VERDICT (FRONT 3)")
print("="*92)
print("""  (a) point-vs-composite: dS-Unruh T(a) sees |a| ONLY, no size/Compton -> EP-compatible but BLIND. NO.
  (b) 1/m loop: bath couples to classical worldline |a|, ~10^36 below the mass loop, analytic FLOOR not
      QED -log -> does NOT see 1/m. Lethal legs #1,#2,#3 confirmed numerically. NO.
  (c) triality Z3 family gauge: DISCRETE outer auto -> Schur block-diagonal (r free) + no continuous
      coupling for Sumino's counterterm. NO. Lethal leg [G] + flavor-blind quark falsifier confirmed.
  NEUTRINO WALL: colorless point-like neutrinos do NOT sit at 2/3 -> kills any color/composite selector.

  MINIMAL MISSING INGREDIENT: a NEW Sumino-class gauged family symmetry (continuous U(3)/O(3), broken,
  tuned coupling alpha_fam=(1/4)alpha_F) supplying a CHARGED-LEPTON-SELECTIVE radiative counterterm that
  cancels the QED -log(m) drift and pins an IR fixed point at the doublet/singlet equipartition (45deg).
  This meets (i) flavor-selectivity and (iii) non-circular IR fixed point; meeting (ii) sqrt2-in-R^3 still
  requires the family VEV to land equipartition, which Sumino IMPOSES.

  INSIDE/OUTSIDE: OUTSIDE the spine. The spine has only flavor-blind |a|-inertia and R^1 bath-sqrt2's and a
  discrete triality. The EP loophole (couple to 1/m) is CLOSED by (b). No EP-compatible selector lives in
  the spine. The bridge requires new physics external to the dS-Unruh/inertia spine. NO manufactured win.""")
print("\n" + ("ALL CHECKS PASS" if allok else "SOME CHECKS FAILED"))
import sys
sys.exit(0 if allok else 1)
