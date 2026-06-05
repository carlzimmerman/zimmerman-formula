#!/usr/bin/env python3
"""
The VALUE of Lambda: does the framework's seesaw say anything NEW, or restate the CC problem? (honest)
=====================================================================================================
Target: the deepest debt in the framework -- the VALUE of the cosmological constant Lambda. The framework
reformulates a0 as a seesaw, a0 = c E_Lambda^2/(2 hbar E_P), and notes the "cosmic seesaw"
E_Lambda = sqrt((2/Z) E_P E_H): the meV vacuum scale is (close to) the GEOMETRIC MEAN of the Planck (UV) and
Hubble (IR) energy scales. The question is whether this structure CONSTRAINS Lambda's value or merely RELOCATES
the puzzle. This script settles three things with real computation (numpy):

  ITEM 1 -- DERIVATION OR RESTATEMENT?  Carry the algebra explicitly. The geomean E_L=sqrt((2/Z)E_P E_H) is shown
            to be an ALGEBRAIC IDENTITY, true iff Z^2 = 32pi/3 (the DEFINITION of Z), given only the standard
            rho_Lambda = 3 H^2 c^2/(8 pi G). It carries ZERO information beyond rho_Lambda and the def of Z.
            => RESTATEMENT of the same coincidence, not new information.

  ITEM 2 -- THE CKN / HOLOGRAPHIC BOUND (the one place something non-trivial might be true).
            Cohen-Kaplan-Nelson (1999, hep-th/9803132): an EFT in a box of size L with UV cutoff Lambda_UV that
            forms no black hole obeys Lambda_UV^2 L <~ M_P, hence rho_vac <~ M_P^2/L^2; with L~1/H this is
            rho_vac <~ M_P^2 H^2 -- the OBSERVED magnitude (the ~10^-122 suppression, for free). We verify the
            magnitude, then show the framework's seesaw IS rho_vac = (3/8pi) M_P^2 H^2 -- i.e. the SAME equation
            as the CKN bound, with the framework's (2/Z) sitting exactly where CKN's free O(1) sits. So the
            a0<->Lambda welding = the CKN UV-IR relation in disguise, SATURATED, with the O(1) fixed to the
            Friedmann value. What that buys and does NOT buy is reported precisely.

  ITEM 3 -- COMPARISON to the other serious approaches (sequestering/Kaloper-Padilla; unimodular; Sorkin
            causal-set fluctuating-Lambda = repo Door 2) and the HONEST VERDICT: does the framework add a new
            handle on WHY Lambda has its value?

BRUTAL-HONESTY HEADLINE (computed below, not asserted): the geomean is algebraically CIRCULAR; the framework's
seesaw is the CKN bound restated and SATURATED; CKN genuinely supplies the magnitude but NOT via this framework
(it is inherited), and the dimensionless ratio E_L/E_P ~ 1.8e-31 -- the actual CC problem -- is UNTOUCHED. No new
win on Lambda's value. The single genuinely-new framework content is the O(1) (Z), which is a coefficient debt,
not a value debt.
Needs numpy.
"""
import numpy as np

# ---- constants (SI) ----
c    = 2.998e8        # m/s
G    = 6.674e-11      # m^3 kg^-1 s^-2
hbar = 1.055e-34      # J s
eV   = 1.602e-19      # J
Mpc  = 3.086e22       # m
H0   = 67.4e3/Mpc     # s^-1  (Planck 2018)
OmL  = 0.685          # dark-energy fraction

Z      = 2*np.sqrt(8*np.pi/3)          # = 5.7888...  the framework coefficient, a0 = cH/Z
H_L    = H0*np.sqrt(OmL)               # the de Sitter (Lambda-only) Hubble rate, so rho_L = 3 H_L^2 c^2/(8 pi G)
E_P    = np.sqrt(hbar*c**5/G)          # Planck ENERGY  = M_P c^2     (M_P = Planck mass)
E_Pred = np.sqrt(hbar*c**5/(8*np.pi*G))# reduced Planck energy        (M_Pl_reduced c^2)
E_H    = hbar*H_L                      # Hubble energy (de Sitter)
lP     = np.sqrt(hbar*G/c**3)          # Planck length
RdS    = c/H_L                         # de Sitter horizon radius


def nat_energy_density_from_E4(E4):
    """E^4 (in J^4) -> energy density in J/m^3, restoring (hbar c)^3."""
    return E4/(hbar*c)**3


def main():
    print("#"*100)
    print("# The VALUE of Lambda: new handle, or the CC problem restated? -- a0 seesaw vs the CKN bound")
    print("#"*100 + "\n")

    # ---------- the scales ----------
    u_L = OmL*3*H0**2/(8*np.pi*G)*c**2          # observed vacuum ENERGY density (J/m^3)
    E_L = (u_L*(hbar*c)**3)**0.25               # vacuum energy scale rho_L^(1/4)
    print("="*100); print("THE SCALES (observed)"); print("="*100)
    print(f"  E_Lambda = rho_Lambda^(1/4)      = {E_L/eV*1e3:.3f} meV      (vacuum-energy scale)")
    print(f"  E_Planck = M_P c^2               = {E_P/eV/1e9:.3e} GeV")
    print(f"  E_Hubble = hbar H_Lambda         = {E_H/eV:.3e} eV")
    print(f"  E_Lambda / E_Planck              = {E_L/E_P:.3e}   <-- THIS ~1.8e-31 ratio IS the CC problem")
    print(f"  rho_Lambda / E_Planck^4          = {(E_L/E_P)**4:.3e}   <-- equivalently the ~10^-122 problem\n")

    # =====================================================================================================
    print("#"*100)
    print("# ITEM 1 -- is 'E_Lambda = geometric mean of E_P,E_H' a DERIVATION or a RESTATEMENT?")
    print("#"*100)
    print("""
  Carry the algebra. Inputs are the framework's two relations, NOTHING else:
      (i)  rho_Lambda (energy density)  u_L = 3 H^2 c^2/(8 pi G)        [standard Friedmann, H = H_Lambda]
      (ii) Z defined by  a0 = cH/Z = c^2 sqrt(Lambda/32pi), i.e.  32pi = 3 Z^2   (Z = 2 sqrt(8pi/3))

  Claim to test:   E_L := (u_L (hbar c)^3)^{1/4}  ==  sqrt((2/Z) E_P E_H),  E_P=sqrt(hbar c^5/G), E_H=hbar H.

  RHS to the 4th power:
      E_L^4 = [ (2/Z) E_P E_H ]^2 = (4/Z^2) E_P^2 E_H^2 = (4/Z^2)(hbar c^5/G)(hbar^2 H^2) = (4/Z^2) hbar^3 c^5 H^2/G
  LHS to the 4th power:
      E_L^4 = u_L (hbar c)^3 = [3 H^2 c^2/(8 pi G)] hbar^3 c^3        = (3/(8 pi))   hbar^3 c^5 H^2/G

  Equate:   3/(8 pi) = 4/Z^2   <=>   Z^2 = 32 pi/3.   <-- EXACTLY the DEFINITION of Z. The geomean is an IDENTITY.
""")
    E_L4_lhs = (3/(8*np.pi))*hbar**3*c**5*H_L**2/G
    E_L4_rhs = (4/Z**2)   *hbar**3*c**5*H_L**2/G
    E_L_geo  = np.sqrt((2/Z)*E_P*E_H)
    print(f"  E_L^4 from rho_Lambda (LHS)       = {E_L4_lhs:.6e}")
    print(f"  E_L^4 from the geomean (RHS)      = {E_L4_rhs:.6e}   identical: {np.isclose(E_L4_lhs,E_L4_rhs)}")
    print(f"  sqrt((2/Z) E_P E_H)               = {E_L_geo/eV*1e3:.4f} meV   vs rho_L^(1/4) = {E_L/eV*1e3:.4f} meV"
          f"   ratio {E_L_geo/E_L:.6f}")
    print("  VERDICT 1: RESTATEMENT. The geomean is true iff Z^2=32pi/3 (the def of Z); it adds NO information")
    print("             beyond rho_Lambda=3H^2c^2/8piG. It is the SAME a0<->Lambda coincidence rewritten in")
    print("             energy-scale language -- algebraically CIRCULAR, not a new fact about Lambda.\n")

    # =====================================================================================================
    print("#"*100)
    print("# ITEM 2 -- THE CKN / HOLOGRAPHIC BOUND: does the seesaw = CKN saturated? what does CKN buy?")
    print("#"*100)
    print("""
  CKN (Cohen-Kaplan-Nelson 1999, hep-th/9803132). An EFT in a box of size L with UV cutoff Lambda_UV holds
  energy ~ L^3 Lambda_UV^4; demanding it not exceed the mass of a black hole of size L (~ L M_P^2 / [restore c,G])
  gives the UV-IR relation
        Lambda_UV^2 L  <~  M_P        =>        rho_vac  <~  M_P^2 / L^2.
  Taking the IR scale to be the Hubble radius, L ~ c/H:
        rho_vac  <~  M_P^2 H^2   (natural units)   -- and THIS is the observed dark-energy magnitude.
""")
    print("-"*100); print("STEP A -- verify the CKN magnitude rho ~ M_P^2 H^2 hits the observed value to O(1):"); print("-"*100)
    rho_CKN_full = nat_energy_density_from_E4(E_P**2    * E_H**2)   # M_P^2 H^2 with the full Planck mass
    rho_CKN_red  = nat_energy_density_from_E4(E_Pred**2 * E_H**2)   # ... with the reduced Planck mass
    print(f"  observed u_Lambda                = {u_L:.3e} J/m^3   (E_L = {E_L/eV*1e3:.2f} meV)")
    print(f"  M_P^2 H^2   (full Planck mass)    = {rho_CKN_full:.3e} J/m^3   obs/CKN = {u_L/rho_CKN_full:.4f}  (= 3/8pi)")
    print(f"  M_P^2 H^2   (reduced Planck mass) = {rho_CKN_red:.3e} J/m^3   obs/CKN = {u_L/rho_CKN_red:.4f}  (= 3)")
    print("  => CKN reproduces the OBSERVED magnitude (the ~10^-122 suppression) up to an O(1). The O(1) needed")
    print("     is exactly the Friedmann 3/(8pi) [full] or 3 [reduced]; CKN itself does NOT fix it (see STEP C).\n")

    print("-"*100); print("STEP B -- is the framework's seesaw the SAME equation as CKN's rho_vac ~ M_P^2 H^2?"); print("-"*100)
    lhs = E_P**2 * E_H**2
    rhs = hbar**3*c**5*H_L**2/G
    print(f"  E_P^2 E_H^2                       = {lhs:.4e}")
    print(f"  hbar^3 c^5 H^2 / G                = {rhs:.4e}   identical: {np.isclose(lhs,rhs)}")
    print("  geomean:        E_L^4 = (4/Z^2) E_P^2 E_H^2        (ITEM 1)")
    print("  CKN-saturated:  rho_vac = (O(1))  M_P^2 H^2   <=>  E_L^4 = (O(1)) E_P^2 E_H^2")
    print("  => IDENTICAL EQUATIONS. The framework's seesaw IS the CKN UV-IR relation, SATURATED, with the")
    print("     framework's (2/Z) sitting EXACTLY where CKN's free O(1) sits:  4/Z^2 = 3/(8pi).")
    print("     a0 = c^2 sqrt(Lambda/32pi) with Lambda~H^2 is STRUCTURALLY the CKN bound saturated.\n")

    print("-"*100); print("STEP C -- what CKN-saturation BUYS, and what it does NOT (the honest ledger):"); print("-"*100)
    print("  BUYS:    rho_vac ~ M_P^2 H^2 is the right MAGNITUDE -- the 10^-122 is no longer a tuning, it is the")
    print("           ratio (H/M_P)^2 forced by a UV-IR/black-hole argument. That is a genuine, non-trivial CKN win.")
    print("  ASSUMES: (1) the bound is SATURATED (CKN gives rho <~ M_P^2 H^2; zero is the generic/likeliest value).")
    print("           (2) the IR cutoff is precisely L = c/H (CKN note there is 'no explicit reason' to pick H).")
    print("           (3) no additive constant is added back (always allowed) -- the old CC problem in new clothes.")
    print("  The framework INHERITS all three. It does not re-derive the magnitude; it ADOPTS CKN's saturated value")
    print("  and then tracks it (a0 follows Lambda whatever Lambda is).")
    print("  CAVEAT (cuts BOTH ways): as a DYNAMICAL model, CKN with L=c/H gives the WRONG equation of state --")
    print("           Hsu/Li: rho_DE ~ H(t)^2 then tracks matter, w=0, NO acceleration -- which is why holographic-")
    print("           dark-energy builders switch the IR cutoff to the future EVENT horizon (reintroducing")
    print("           circularity + the coincidence problem). The framework DODGES this ONLY by treating Lambda as a")
    print("           true CONSTANT (de Sitter, Lambda ~ H_Lambda^2), not rho_DE(t) ~ H(t)^2 -- so it keeps the")
    print("           today-magnitude coincidence but inherits NO working VALUE/dynamics mechanism. Smallness INHERITED:")
    inherited = np.sqrt(E_H/E_P)*np.sqrt(2/Z)
    print(f"     E_L/E_P  (from geomean) = sqrt(E_H/E_P)*sqrt(2/Z) = {inherited:.3e}  vs direct {E_L/E_P:.3e}"
          f"  match {np.isclose(inherited,E_L/E_P)}")
    print(f"     so the 1.8e-31 comes ENTIRELY from sqrt(E_H/E_P) = sqrt({E_H/E_P:.2e}); the framework explains")
    print("     NONE of it -- it relocates 'why is rho_L small' to 'why is H/M_P small (and why saturate)'.\n")

    # the famous sub-mm / dark-energy length coincidence, for completeness (real, but buys nothing for the VALUE)
    ellL = hbar*c/E_L
    print(f"  (aside) dark-energy length ell_L = hbar c/E_L = {ellL*1e6:.1f} um ~ sqrt(lP R_dS) = "
          f"{np.sqrt(lP*RdS)*1e6:.1f} um: a real geomean-of-lengths coincidence, but it constrains no VALUE.\n")

    # =====================================================================================================
    print("#"*100)
    print("# ITEM 3 -- comparison to the serious approaches, and what (if anything) the framework adds")
    print("#"*100)
    print("""
  | approach                         | mechanism for Lambda's VALUE                         | derives the number? |
  |----------------------------------|------------------------------------------------------|---------------------|
  | CKN / holographic dark energy    | UV-IR no-black-hole bound -> rho <~ M_P^2 H^2         | NO (needs saturate) |
  | Sequestering (Kaloper-Padilla)   | global constraint makes vacuum energy NOT gravitate; | NO -- removes the    |
  |                                  | historic average of T^mu_mu; residual ~ 1/V_4-ish    | tuning, residual not |
  |                                  |                                                      | predicted (V_4 set   |
  |                                  |                                                      | by the universe)     |
  | Unimodular gravity               | Lambda = integration constant (a boundary datum),    | NO -- Lambda becomes |
  |                                  | decoupled from the vacuum-energy radiative problem   | initial data, free   |
  | Sorkin causal-set (repo Door 2)  | fluctuating Lambda ~ +/- 1/sqrt(N) ~ +/- H^2;        | scale YES, value NO; |
  |                                  | a DYNAMICAL everpresent-Lambda PREDICTION of the     | sign fluctuates (a0  |
  |                                  | magnitude (pre-1998 success)                         | imaginary half-time) |
  | THIS framework (a0 seesaw)       | a0 = c^2 sqrt(Lambda/32pi); E_L = geomean(E_P,E_H)   | NO -- ITEM 1 shows   |
  |                                  | = CKN saturated with O(1) fixed to 3/8pi (ITEM 2)    | it is CKN restated   |

  What the framework ADDS that CKN/sequestering/unimodular do NOT:
    * It FIXES the O(1) coefficient (Z = 2 sqrt(8pi/3)) geometrically, where CKN leaves it free. That is real,
      distinctive content -- BUT it is a COEFFICIENT result, not a VALUE result. It tells you the relation's slope,
      not why Lambda sits where it does. (And per the repo's own ledgers, Z is reproduced/route-forced, not
      derived from below -- DSSYK forcing of Z is COMPUTED TO FAIL.)
    * It WELDS the dark sector: a0 (MOND) and rho_Lambda (dark energy) become one scale sqrt(Lambda). Genuine
      unification of the dark sector -- but it is unification AT a value, not a prediction OF the value.

  What the framework does NOT add (vs the others): any new dynamics, constraint, or selection principle that
  pins the NUMBER. CKN at least supplies a magnitude argument (which the framework borrows); Sorkin at least
  makes Lambda dynamical/everpresent (a real prediction with a fatal sign problem); sequestering/unimodular at
  least remove the radiative-tuning channel. The a0 seesaw, by itself, supplies NONE of these -- it is a
  bookkeeping identity (ITEM 1) over CKN's saturated magnitude (ITEM 2).
""")

    # =====================================================================================================
    print("#"*100)
    print("# HONEST VERDICT")
    print("#"*100)
    print("""  (a) GEOMEAN -- DERIVATION OR RESTATEMENT?  RESTATEMENT (algebraically circular). E_L = sqrt((2/Z)E_P E_H)
      is an IDENTITY, true iff Z^2 = 32pi/3 (the definition of Z), given only rho_Lambda = 3H^2c^2/(8pi G). It
      re-expresses the SAME a0<->Lambda coincidence in UV/IR energy-scale language; it is NOT independent
      information about Lambda.

  (b) WHAT CKN BUYS, AND IS THE FRAMEWORK = CKN SATURATED?  YES, structurally identical. The framework's seesaw
      IS rho_vac = (3/8pi) M_P^2 H^2 -- the CKN UV-IR bound SATURATED, with the framework's (2/Z) occupying the
      slot of CKN's free O(1) (4/Z^2 = 3/8pi). CKN genuinely delivers the right MAGNITUDE (rho ~ M_P^2 H^2 ~
      observed; the 10^-122 becomes (H/M_P)^2 from a black-hole argument) -- a non-trivial result. BUT it requires
      SATURATION + choosing L=c/H + dropping the additive constant, all ASSUMPTIONS, all INHERITED by the
      framework, which adds no independent reason for any of them. The smallness is inherited from sqrt(H/M_P),
      not explained.

  (c) ANYTHING NEW ABOUT LAMBDA'S VALUE?  NO. The framework's structure offers no new handle on WHY Lambda has its
      value; a0 simply tracks Lambda whatever its value. The one genuinely-new piece -- fixing the O(1) (Z)
      geometrically -- is a COEFFICIENT debt, not the VALUE debt, and is itself reproduced rather than derived.
      The dimensionless E_L/E_P ~ 1.8e-31 (= the cosmological-constant problem) is UNTOUCHED.

  BOTTOM LINE: the cosmic seesaw is a beautiful, exact RESTATEMENT of the CKN coincidence with a pinned O(1). It
  inherits CKN's magnitude win and CKN's saturation debt; it does NOT solve, soften, or newly constrain the VALUE
  of Lambda. Honest, and not a win on the hardest problem in physics.""")
    print("#"*100)


if __name__ == "__main__":
    main()
