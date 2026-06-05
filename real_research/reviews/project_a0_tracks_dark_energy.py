#!/usr/bin/env python3
"""
The framework's faithful reading: a0 tracks sqrt(rho_DARK-ENERGY), not sqrt(rho_total). Resolves the a0(z) tension.
=================================================================================================================
A follow-up that matters. The framework has TWO stated forms, treated as 'the same' because they agree at z=0:
   (geometric)  a0 = c^2 sqrt(Lambda/32pi) = (c/2) sqrt(G rho_Lambda)   ->  a0 ~ sqrt(rho_DARK-ENERGY)
   (Hubble)     a0 = c H(z)/Z,  with H^2 = (8piG/3) rho_total           ->  a0 ~ sqrt(rho_TOTAL)
They AGREE at z=0 (differ by the ~1.21 sqrt(Omega_Lambda)-ish factor) but DIVERGE at high z: rho_total is
matter-dominated in the past (rises as (1+z)^3) while rho_DE is not. So the DISFAVORED 'rising a0 ~ E(z)' claim is
the sqrt(rho_total) reading -- it conflates 'dark energy' with 'total density'. The reading FAITHFUL to the
framework's own formula (a0 set by Lambda / the dark energy) is sqrt(rho_DE).

CONSEQUENCE: under constant Lambda, sqrt(rho_DE) is CONSTANT (the geometric core, safe). Under DESI's dynamical dark
energy (w0=-0.83, wa=-0.75, phantom-crossing), sqrt(rho_DE) gives a MILD DECLINE into the past: a0(z) = 1.02, 0.96,
0.81, 0.70 at z=0.5,1,2,3. This is (i) the ONLY reading that goes BELOW 1; (ii) CONSISTENT with the published tests
that kill the Hubble version (Milgrom 2017 excludes a0 ~4x BIGGER at z~2 -- this is smaller; Limbach 2008 favors
near-constant -- this is ~0.9 at z=1.2); and (iii) a distinct, DESI-tied, z~3-testable signature.
HONEST: contingent on DESI (contested, ~2-4 sigma); assumes a0 tracks the instantaneous rho_DE; the sqrt(rho_DE) vs
sqrt(rho_total) split is a real fork (both are framework derivations), but the rho_DE form is the one tied to the
cosmological CONSTANT and the CKN/de-Sitter structure. Needs numpy, scipy.
"""
import numpy as np
from scipy.integrate import quad

Om,OL=0.315,0.685
Ea=lambda a: np.sqrt(Om*a**-3+OL); E=lambda z: Ea(1/(1+z))
w0,wa=-0.83,-0.75                                   # DESI 2024 BAO+CMB+DESY5
rhoDE=lambda a: a**(-3*(1+w0+wa))*np.exp(-3*wa*(1-a))
a0_DE=lambda z: np.sqrt(rhoDE(1/(1+z)))             # framework formula a0 ~ sqrt(rho_DE), DESI w(z)
chi_event=lambda a: quad(lambda ap: 1/(ap**2*Ea(ap)), a, np.inf)[0]
Re=lambda z:(1/(1+z))*chi_event(1/(1+z)); Re0=Re(0)


def main():
    print("#"*98); print("# a0 tracks sqrt(rho_DARK-ENERGY), not sqrt(rho_total): the faithful reading + DESI"); print("#"*98+"\n")

    print("="*98); print("(1) the two framework forms DIVERGE at high z -- the disfavored one uses rho_total"); print("="*98)
    print("   a0=c^2 sqrt(Lambda/32pi) ~ sqrt(rho_DE)   [geometric, tied to the cosmological CONSTANT]")
    print("   a0=cH(z)/Z              ~ sqrt(rho_total)  [Hubble; rho_total ~ rho_matter at high z -> RISES]")
    print("   they agree at z=0, diverge in the past. The 'rising a0' that the data disfavor is the rho_total form.\n")

    print("="*98); print("(2) the FAITHFUL reading a0 ~ sqrt(rho_DE): constant (Lambda) or MILD DECLINE (DESI)"); print("="*98)
    print(f"   {'z':>4}{'Hubble ~sqrt(rho_tot)':>22}{'event horizon':>15}{'DESI a0~sqrt(rho_DE)':>22}{'const(Lam)':>12}")
    for z in (0.5,1,2,3):
        print(f"   {z:>4}{E(z):>22.2f}{Re0/Re(z):>15.2f}{a0_DE(z):>22.2f}{1.00:>12.2f}")
    print(f"   constant-Lambda limit (w=-1): rho_DE const -> a0 const (the geometric core).")
    print(f"   DESI dynamical DE: a0 nearly flat at low z, MILD DECLINE to {a0_DE(3):.2f} at z=3. The ONLY reading below 1.\n")

    print("="*98); print("(3) consistency with the published tests that KILL the Hubble version"); print("="*98)
    print(f"   Milgrom 2017 ('all but excludes ~4 a0 at z~2'):  DE-track a0(z=2)={a0_DE(2):.2f}  -> SMALLER, SAFE.")
    print(f"   Limbach 2008 (favors near-constant, to z=1.2):    DE-track a0(z=1.2)={a0_DE(1.2):.2f}  -> near-constant, consistent.")
    print(f"   distinct z~3 prediction: a0~{a0_DE(3):.2f} (DE-track) vs 1.0 (const) vs {Re0/Re(3):.2f} (event) vs {E(3):.2f} (Hubble).\n")

    print("="*98); print("VERDICT"); print("="*98)
    print(f"""  Pushing on DESI surfaced the key point: the framework's own formula a0=(c/2)sqrt(G rho_Lambda) ties a0 to the
  DARK-ENERGY density, sqrt(rho_DE) -- NOT the total density. The disfavored 'rising a0~E(z)' claim used sqrt(rho_
  total) (the cH(z)/Z form), which is matter-dominated in the past; that was a conflation. Read faithfully, a0 is
  CONSTANT if Lambda is constant (the safe geometric core), and a MILD DECLINE (a0~0.7 at z=3) if DESI's dynamical
  dark energy is real -- the ONLY reading that goes below 1, consistent with Limbach and Milgrom (which disfavor the
  RISING versions), and a clean DESI-tied z~3 signature. HONEST: contingent on DESI (contested); assumes a0 tracks
  the instantaneous rho_DE; the rho_DE-vs-rho_total split is a genuine fork. But it materially improves the picture:
  the framework's faithful empirical content was never the data-disfavored rising claim -- it is constant-or-mild-
  decline, which the data already accommodate, and which DESI would turn into a distinctive, testable prediction.""")
    print("#"*98)


if __name__=="__main__":
    main()
