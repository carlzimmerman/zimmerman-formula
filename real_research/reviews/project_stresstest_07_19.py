#!/usr/bin/env python3
"""
STRESS-TEST of the forecast/derivation claims #7 (JWST collapse) and #19 (lensing). Both OVERCLAIMED.
====================================================================================================
Continuing the adversarial sweep onto the two forecast claims most likely to overreach. Both survive in
weakened form, and both corrections are the same kind: the underlying calculation is right, but the
COMPARISON TO LambdaCDM / the systematics were stated too favorably. Honest corrections, with the original
files flagged. Needs numpy.
"""
import numpy as np

G, a0, Msun, kpc = 6.674e-11, 1.2e-10, 1.989e30, 3.0857e19
Om, Ob = 0.315, 0.049
E = lambda z: np.sqrt(Om*(1+z)**3 + 0.685)
fDM = Om/Ob


def attack_7():
    print("="*92); print("ATTACK on #7 -- does rising-a0 MOND really beat LambdaCDM-WITH-DM for JWST galaxies?"); print("="*92)
    print("""  #7 showed MOND collapses faster than BARYONS-ALONE-Newtonian. But the JWST comparison is vs LambdaCDM,
  which has DARK MATTER. LambdaCDM gravity is (Om/Ob)~6.4x the baryonic g_N; MOND (deep) is sqrt(g_N a0 E(z)).
  MOND out-pulls LambdaCDM only where g_N < g_N* = a0 E(z)/(Om/Ob)^2. By surface density at z=3:""")
    print(f"     {'case':22}{'g_N':>10}{'MOND g':>11}{'LCDM g':>11}{'winner':>8}")
    for name, M, r in [("diffuse (30 kpc)", 1e10, 30), ("typical (5 kpc)", 1e10, 5), ("compact JWST (1 kpc)", 1e10, 1)]:
        gN = G*M*Msun/(r*kpc)**2; gM = np.sqrt(gN*a0*E(3)); gL = fDM*gN
        print(f"     {name:22}{gN:>10.1e}{gM:>11.1e}{gL:>11.1e}{('MOND' if gM > gL else 'LCDM'):>8}")
    print(f"""  g_N*(z=3) = {a0*E(3)/fDM**2:.1e}. CORRECTION: MOND/rising-a0 wins only at LOW surface density (the cosmic
  web, diffuse first structures). The COMPACT massive galaxies JWST flags have high g_N -> LambdaCDM-with-DM
  gives MORE gravity there. So #7's 'forms galaxies EARLIEST of the three' was too strong: it holds for
  diffuse/large-scale collapse, not for compact proto-galaxies. The closed-form collapse t~r/(GMa0)^1/4
  (verified 3 ways) stands; the blanket JWST framing does not. MOND's early-structure case lives on LARGE,
  LOW-density scales (linear growth), not single dense-object collapse.\n""")


def attack_19():
    print("="*92); print("ATTACK on #19 -- is lensing really 'immune to the gas/pressure confound'?"); print("="*92)
    print("""  #19 claimed lensing (M_lens ~ sqrt(M_bar a0) ~ sqrt(E(z))) is immune to the gas/pressure confound that
  limits the dynamical a0(z). But M_lens depends on the BARYONIC mass, and at fixed STELLAR mass M_bar =
  M_star(1+f_gas) with f_gas RISING at high z. So the gas evolution inflates M_lens too:""")
    print(f"     {'z':>4}{'wanted sqrt(E(z))':>18}{'gas factor sqrt((1+fg)/1.2)':>30}")
    for z, fg in [(0, 0.2), (1, 0.5), (2, 1.0), (3, 1.6)]:
        print(f"     {z:>4}{np.sqrt(E(z)):>18.2f}{np.sqrt((1+fg)/1.2):>30.2f}  (f_gas~{fg})")
    print("""  CORRECTION: the gas-fraction factor is COMPARABLE to the wanted sqrt(E(z)) signal. So lensing is NOT
  immune to the gas confound -- it still needs a per-galaxy GAS CENSUS for M_bar, exactly like the dynamical
  method. What lensing IS immune to is the PRESSURE-SUPPORT / KINEMATIC confound (it uses no velocities) --
  a real and distinct advantage, because lensing and dynamics then fail DIFFERENTLY. So #19's value stands
  (an orthogonal-systematics cross-check) but 'immune to gas/pressure' should read 'immune to kinematics,
  still needs the gas census'.\n""")


def verdict():
    print("="*92); print("VERDICT -- both #7 and #19 survive WEAKENED (overclaims corrected)"); print("="*92)
    print("""  Same pattern as the rest of the adversarial sweep: the core CALCULATION is right (the closed-form
  collapse; the sqrt(E(z)) lensing scaling), but the framing vs LambdaCDM / systematics overreached.
    * #7: MOND-earliest holds at LOW surface density, NOT for compact JWST galaxies (LambdaCDM-with-DM wins there).
    * #19: lensing is immune to KINEMATICS (real, distinct), not to the gas census (still required).
  Neither is fatal; both are now stated honestly. The recurring lesson of the whole sweep: the framework's
  CALCULATIONS hold up; its COMPARISONS-TO-LambdaCDM and significance claims need deflating -- which is exactly
  the discipline that keeps it credible.""")
    print("="*92)


def main():
    print("#"*92); print("# STRESS-TEST -- forecast claims #7 (collapse/JWST) and #19 (lensing)"); print("#"*92 + "\n")
    attack_7(); attack_19(); verdict()


if __name__ == "__main__":
    main()
