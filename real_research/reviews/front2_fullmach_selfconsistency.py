#!/usr/bin/env python3
"""
FRONT 2 -- FULL-MACH SELF-CONSISTENCY FOR REST MASS.
====================================================
Question: does the loop  m_rest -> coupling-to-bath -> bath sourced by rho_DE ->
(does rho_DE depend on the masses?) -> back to m_rest  CLOSE into a constraint on
the mass spectrum, or RESTATE the input?

Framework footing (Carl's, NEVER McGaugh nu):
  a0 = cH_Lambda/Z = 9.36e-11 m/s^2,  Z = 2 sqrt(8pi/3) = sqrt(32pi/3) = 5.7888
  T0 = hbar cH_Lambda/(2pi kB c) = hbar H_Lambda/(2pi kB) = dS-Unruh floor temp
  rest mass = LOCAL floor coupling ~ m c^2/(kB T0)  (CIRCULAR by construction)
  Lambda sourced by rho_DE (dark energy), NOT by matter content.

Three legs, all sympy/numpy, both-ways, no manufactured crack.
"""
import sympy as sp
import numpy as np

print("#"*92)
print("# FRONT 2 -- does FULL Mach close a mass constraint, or restate the input?")
print("#"*92)

# ----- constants (SI) -----
c=2.99792458e8; G=6.67430e-11; hbar=1.054571817e-34; kB=1.380649e-23; eV=1.602176634e-19
Mpc=3.0856775814913673e22; H0=67.4e3/Mpc; OmL=0.685; OmM=0.315
H_L=H0*np.sqrt(OmL); Lam=3*H0**2*OmL/c**2
rho_DE=Lam*c**2/(8*np.pi*G); Z=np.sqrt(32*np.pi/3)
a0=c*H_L/Z
T0=hbar*H_L/(2*np.pi*kB)   # dS-Unruh floor temperature
E_T0=kB*T0/eV              # floor energy in eV
print(f"\n  a0={a0:.4e}  Z={Z:.5f}  H_L={H_L:.4e}/s  rho_DE={rho_DE:.4e} kg/m^3")
print(f"  T0 = {T0:.4e} K   kB*T0 = {E_T0:.4e} eV   (the floor coupling energy)")

# ==================================================================
# (a) SET UP THE LOOP and ask: does rho_DE depend on the masses?
# ==================================================================
print("\n"+"="*92); print("(a) THE LOOP: m_rest -> coupling -> T0(rho_DE) -> does rho_DE see the masses?"); print("="*92)

# Step 1: coupling. The floor coupling that sets rest mass:
#   m_rest c^2 = g_floor * kB * T0,  with g_floor = m_rest c^2/(kB T0).
# This DEFINES g_floor as the number of floor-quanta in the rest energy. CIRCULAR.
m_rest, gfloor, T0s, rhoDE, Lams = sp.symbols('m_rest g_floor T0 rho_DE Lambda', positive=True)
csym,hbars,kBs,Gs,pis = sp.symbols('c hbar k_B G pi', positive=True)
# coupling identity (definitional):
coupling = sp.Eq(gfloor, m_rest*csym**2/(kBs*T0s))
print("\n  Step1 (coupling, DEFINITIONAL):  g_floor = m_rest c^2 / (kB T0)")
print("     -> g_floor is just the rest energy measured in floor-quanta. Solving for m_rest:")
m_from_coupling = sp.solve(coupling, m_rest)[0]
print(f"     m_rest = {m_from_coupling}  ==> CIRCULAR: m_rest in terms of (g_floor, T0), g_floor itself = m_rest c^2/kB T0.")

# Step 2: T0 from rho_DE.  T0 = hbar H_L/(2pi kB), H_L = c sqrt(Lambda/3), Lambda = 8 pi G rho_DE/c^2.
T0_of_rho = hbars*csym*sp.sqrt(8*pis*Gs*rhoDE/csym**2/3)/(2*pis*kBs)
T0_of_rho = sp.simplify(T0_of_rho)
print(f"\n  Step2 (bath temp from vacuum):  T0(rho_DE) = {T0_of_rho}")
print("     -> T0 depends ONLY on rho_DE (the dark-energy density), NOT on any matter mass.")

# Step 3: THE PIVOT. Does rho_DE depend on the matter content (the masses)?
print("\n  Step3 (THE PIVOT): does rho_DE depend on the masses?")
print("     In the framework, Lambda is sourced by rho_DE = dark-energy vacuum density (w=-1, flat).")
print("     The Friedmann constraint:  3H^2 = 8 pi G (rho_matter + rho_DE).")
print("     rho_DE is the COSMOLOGICAL-CONSTANT piece: independent of rho_matter (that is what w=-1 MEANS).")
print("     -> d rho_DE / d m_rest = 0  by the framework's own w=-1 (constant Lambda) postulate.")
print("     The matter masses set rho_matter (which DILUTES as a^-3); rho_DE does NOT track them.")
# show that if instead we (wrongly) fed total density rho_tot = rho_m + rho_DE into the floor,
# the matter piece dilutes to zero and only the constant rho_DE survives at late times -- the
# floor that sets TODAY's rest mass would then be EPOCH-DEPENDENT (it is not). So the framework's
# choice rho_DE (not rho_tot) is what makes rest mass a stable LOCAL constant.
print("\n     Counterfactual: if the floor used rho_tot = rho_m+rho_DE, then T0 (hence the rest-mass")
print("     coupling) would DECAY as a^-3 with matter dilution -> electron mass would change with")
print("     cosmic time. It does not (atomic-clock/quasar mu=m_p/m_e bounds < 1e-7). So the framework")
print("     MUST use the constant rho_DE -> the loop's rho_DE leg is matter-INDEPENDENT by consistency.")

print("\n  VERDICT (a): the loop has a BROKEN link. rho_DE does NOT depend on the masses (w=-1).")
print("     m_rest -> g_floor -> T0 -> rho_DE, and rho_DE -|/-> m_rest. The arrow back is CUT.")
print("     => the loop does NOT close. It is an OPEN chain that terminates at the free input rho_DE.")

# ==================================================================
# (b) Is there ANY framework-internal equation fixing m c^2 beyond 'it is the rest energy'?
# ==================================================================
print("\n"+"="*92); print("(b) ANY closure that FIXES m c^2 (quantization / self-energy balance / relational)?"); print("="*92)

# Try (b1): self-energy balance -- 'the body sources a bath that re-acts on it'.
# The gravitational self-coupling to the dS bath gives a shift dm ~ +(2/pi)int rho/omega^2,
# which the banked passivity theorem shows is POSITIVE and ~ a tiny anti-MOND correction.
# Does setting dm = m_rest (a self-consistency 'all mass is bath self-energy') fix m?
print("\n  (b1) SELF-ENERGY BALANCE: set m_rest = dm_bath (all rest mass = dS bath self-energy).")
# dS bath energy in a body's Compton volume: U_bath ~ rho_DE c^2 * (hbar/m c)^3 (Compton vol).
# Set m c^2 = U_bath:  m c^2 = rho_DE c^2 (hbar/(m c))^3  -> m^4 = rho_DE hbar^3/c^3.
msym=sp.symbols('m', positive=True)
eq_self=sp.Eq(msym*csym**2, rhoDE*csym**2*(hbars/(msym*csym))**3)
m_self=sp.solve(eq_self, msym)
m_self=[s for s in m_self if s.is_real or True]
print(f"     m c^2 = rho_DE c^2 (hbar/mc)^3  =>  m^4 = rho_DE hbar^3/c^3  =>  m = (rho_DE hbar^3/c^3)^(1/4)")
m_self_num=(rho_DE*hbar**3/c**3)**0.25
print(f"     m_self = {m_self_num:.4e} kg = {m_self_num*c**2/eV*1e3:.4f} meV/c^2")
print(f"        -> this is EXACTLY rho_DE^(1/4) = the vacuum-energy scale E_Lambda = {(rho_DE*c**2*(hbar*c)**3)**0.25/eV*1e3:.4f} meV.")
print("        It RESTATES rho_Lambda (the dark-energy scale), gives ONE number ~2.2 meV, NOT the")
print("        SM spectrum (electron 0.511 MeV = 2.3e8x larger). A single vacuum scale, not masses.")
print("     => self-energy balance RESTATES the input rho_DE (banked vacuum-self-inertia loop). NO spectrum.")

# Try (b2): quantization condition -- does the dS-Unruh kernel admit a discrete mass tower?
print("\n  (b2) QUANTIZATION: does the kernel admit a discrete mass tower? (cf attack6)")
print("     dS propagator poles at Delta_- = -n give m^2/H^2 = 9/4-(3/2+n)^2 < 0 for n>=1 (tachyonic).")
H=sp.symbols('H', positive=True); n=sp.symbols('n', integer=True, nonnegative=True)
m2_pole=sp.simplify(sp.Rational(9,4)-(sp.Rational(3,2)+n)**2)
print(f"        m^2/H^2 = {m2_pole}  -> only n=0 (massless) physical. NO real-mass tower. Re-confirmed.")

# Try (b3): relational closure -- inertia = sum over cosmic matter (Sciama). Does requiring
# Sum(G m_i/(c^2 r_i)) = 1 (Sciama's full-Mach closure) constrain the individual masses?
print("\n  (b3) SCIAMA RELATIONAL CLOSURE:  Sum_i G m_i/(c^2 r_i) ~ 1  (inertia from all matter).")
# Sciama: 1/(inertial coupling) = G rho_matter/(c^2 H^2) ~ Omega_matter ~ O(1). This is a
# constraint on the TOTAL matter density vs H, i.e. Omega_m ~ 1, NOT on individual masses.
Om_sciama = OmM   # the framework/LCDM Omega_matter
print(f"     Sciama sum ~ G rho_m/(c^2 H^2) = Omega_m ~ {Om_sciama:.3f}  (an O(1) cosmic AVERAGE).")
print("     This constrains the BULK (rho_matter vs H^2), giving Omega_m ~ O(1) -- a statement about")
print("     the SUM/AVERAGE of all masses, NOT the RATIO of any two. It cannot split m_e from m_mu:")
print("     any redistribution of mass among species at fixed total rho_m leaves the closure intact.")
print("     => relational closure constrains the SCALAR total (Omega_m), is BLIND to the spectrum.")

print("\n  VERDICT (b): NO framework-internal equation fixes an individual m c^2 beyond 'rest energy'.")
print("     self-energy -> restates rho_Lambda (one vacuum scale); quantization -> tachyonic/empty;")
print("     relational closure -> constrains the SUM (Omega_m~1), blind to ratios. The rest energy is INPUT.")

# ==================================================================
# (c) HONEST both-ways: real mass equation, or unbreakable circularity?
# ==================================================================
print("\n"+"="*92); print("(c) HONEST VERDICT -- crack or wall?"); print("="*92)

# Quantify the structural blindness with a permutation/degeneracy argument (a 'both-ways' stress):
# Construct two mass spectra with IDENTICAL (rho_DE, Omega_m, total rho_m) but different ratios.
# Show the full-Mach loop returns the SAME closure for both -> the loop cannot tell them apart.
print("\n  DEGENERACY STRESS (both-ways): two spectra, same totals, different ratios.")
specA=np.array([0.511e6, 105.66e6, 1776.86e6])   # e, mu, tau (eV) -- real
total=specA.sum()
specB=np.array([1.0, 1.0, total-2.0])            # same SUM, wildly different ratios (eV)
def loop_outputs(spec):
    # everything the full-Mach loop can 'see': it only feeds the SUM into rho_m, and rho_DE/T0
    # are matter-independent. So the only loop-observable is the total (-> Omega_m) and rho_DE.
    return dict(total=spec.sum(), rhoDE=rho_DE, T0=T0)
oA=loop_outputs(specA); oB=loop_outputs(specB)
same = np.isclose(oA['total'],oB['total']) and oA['rhoDE']==oB['rhoDE'] and oA['T0']==oB['T0']
print(f"     spec A (real e,mu,tau) total={oA['total']:.4e} eV ;  spec B (1,1,rest) total={oB['total']:.4e} eV")
print(f"     loop sees IDENTICAL (total, rho_DE, T0) for both: {same}")
print("     => the full-Mach loop is DEGENERATE over the mass ratios at fixed total. It CANNOT")
print("        produce a constraint that distinguishes the real spectrum from a flat one.")
print("        This is the half-Machian wall made quantitative for the mass SECTOR.")

print("\n  WHERE A CRACK WOULD HAVE TO LIVE (the honest 'door', not a TOE):")
print("     A real mass equation needs a matter->rho_DE BACKREACTION (so the bath the body couples")
print("     to depends on the body), which w=-1 forbids; OR a forced KERNEL in the Yukawa sector")
print("     (none exists, FDR wall); OR a quantization the dS propagator denies (tachyonic poles).")
print("     The ONE pattern-level residue (NOT a mass derivation, NOT a TOE, Z free): the SCALAR")
print("     closure Omega_m ~ O(1) (Sciama) is genuinely framework-consistent -- a constraint on the")
print("     TOTAL matter budget, blind to the spectrum. That is a relation, not a mass formula.")

print("\n  FINAL (both-ways):")
print("     CRACK?  The self-energy loop DOES close -- but onto rho_Lambda (one ~2.2 meV vacuum scale),")
print("             RESTATING the input, exactly the banked vacuum-self-inertia result. The relational")
print("             (Sciama) closure DOES give a real constraint -- but on the SUM (Omega_m~1), not the")
print("             spectrum. Neither yields a mass equation.")
print("     WALL?   The circularity m_rest = g_floor*kB*T0 with g_floor:=m_rest c^2/kB T0 is structurally")
print("             unbreakable WITHOUT a new ingredient (backreaction / forced Yukawa kernel /")
print("             quantization) -- all three independently blocked. rho_DE is matter-blind (w=-1),")
print("             so the loop never returns to the masses. The HALF-MACHIAN WALL HOLDS for rest mass.")
print("\n  => FULL MACH does NOT give a mass equation. It restates rho_Lambda (self-energy leg) and")
print("     constrains only the scalar total (relational leg). The rest energy is the INPUT; the bath")
print("     only modulates the LOW-a inertia DEFICIT (1-mu_fw), never the floor coupling. Z stays free.")
print("#"*92)
