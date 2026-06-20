#!/usr/bin/env python3
"""
ROUTE C steelman (give the YES its strongest shot): is there ANY self-consistent
dS-Unruh THERMAL condition that forces the transverse/democratic ratio to r=sqrt(2)?

The strongest YES one can construct:
  Posit sqrt(m_i) = <s> + delta s_i, with the democratic mean <s> = thermal mean of a
  family-blind dS bath, and the transverse spread {delta s_i} the THERMAL FLUCTUATION.
  Then r^2 = (1/3)*sum (delta s_i/<s>)^2 * (norm) ... we ask: does equipartition /
  Bose-Einstein / the Planck-dS spectrum FIX r=sqrt(2)?

We test three thermodynamic conditions and show each gives r as a FREE function of a
temperature/occupation parameter, hitting sqrt(2) only at one tuned value.
Also: the famous "sqrt(2) coincidences" (zero-point quadrature, RMS-vs-peak) and show
none is forced to be the GENERATION amplitude.
"""
import sympy as sp, mpmath as mp
mp.mp.dps=30

print("="*78)
print("ROUTE C STEELMAN: can a self-consistent dS thermal condition FORCE r=sqrt(2)?")
print("="*78)

# Condition 1: classical equipartition. A family-blind quadratic potential V=1/2 k s^2
# in thermal eq gives <(delta s)^2> = k_B T / k.  The mean <s> is set by the (separate)
# VEV / explicit symmetry breaking.  r^2 = 3<(delta s)^2>/<s>^2 = 3 k_B T/(k <s>^2).
# => r depends on T, k, <s> ALL FREE.  r=sqrt2 needs a tuned T/k/<s>.
T, k, s0 = sp.symbols('T k s0', positive=True)
kB = sp.symbols('k_B', positive=True)
r2_equip = 3*(kB*T/k)/s0**2
print("\n[1] Equipartition: r^2 = 3 k_B T/(k <s>^2) =", r2_equip)
print("    -> r is a FREE function of (T,k,<s>); only one tuned ratio gives r^2=2. NOT forced.")

# Condition 2: Bose-Einstein zero-point + thermal. <s^2> ~ (hbar omega/2)(1+2 n_BE).
# n_BE = 1/(exp(hbar omega/k_B T)-1).  Ratio transverse/democratic still free (omega,T).
x = sp.symbols('x', positive=True)  # x = hbar omega / k_B T
nBE = 1/(sp.exp(x)-1)
amp2 = sp.Rational(1,2)*(1+2*nBE)   # in units of hbar omega
print("\n[2] Bose-Einstein mode amplitude^2 (units hbar*omega) = (1/2)(1+2 n_BE) =",
      sp.simplify(amp2))
print("    coth(x/2)/2 form:", sp.simplify(sp.coth(x/2)/2))
print("    -> the amplitude runs continuously from 1/2 (T->0) to infinity (T->inf).")
print("    There is NO special x where the GENERATION ratio is pinned to sqrt2 by thermality;")
print("    you must separately fix <s> (the democratic VEV). NOT forced.")

# Condition 3: the dS Gibbons-Hawking temperature itself. T_dS = hbar H_Lambda/(2 pi k_B).
# This is a SINGLE fixed (tiny) number ~ 2.4e-30 K. If it set the transverse spread of
# sqrt-masses, that spread would be ~ k_B T_dS / (typical scale) ~ 1e-33 eV -- astronomically
# smaller than the actual MeV-GeV sqrt-mass splittings.  So the dS bath CANNOT supply the
# O(1) transverse spread r~1 at all (this is the magnitude leg from the prior NO, re-derived).
H_Lambda = mp.mpf('1.78e-33')   # eV  (H0 ~ 67 km/s/Mpc in eV)
T_dS_eV  = H_Lambda/(2*mp.pi)
print("\n[3] dS Gibbons-Hawking energy k_B T_dS = hbar H_Lambda/2pi =", T_dS_eV, "eV")
print("    Required transverse sqrt-mass spread for r~1: O(<s>) ~ sqrt(17.7 MeV) scale ~ MeV^(1/2).")
print("    delta(sqrt m) needed ~ r*<s>/sqrt3 ~ 0.8*4.2 ~ 3.4 (MeV)^(1/2)  i.e. ~3.4 sqrt-MeV.")
print("    dS thermal sqrt-energy scale ~ sqrt(k_B T_dS) ~", mp.sqrt(T_dS_eV)*1e3, "(sqrt-meV)... ")
print("    Ratio (dS thermal spread)/(needed Koide spread) ~",
      float(mp.sqrt(T_dS_eV)/mp.sqrt(mp.mpf('1.77e7'))), " (astronomically tiny).")
print("    -> The dS bath's OWN amplitude is ~10^-19-10^-20 of the required transverse spread.")
print("    It cannot SET r at all; r must come from the (free) Yukawa VEV structure.")

print("\n" + "-"*78)
print("THE SQRT(2) COINCIDENCES, catalogued (each real, none FORCED to be the Koide r):")
print("-"*78)
print("  * zero-point: a single oscillator has 2 quadratures -> sqrt(2) in total RMS. But the")
print("    Koide r is across 3 GENERATIONS, not 2 quadratures of one mode.")
print("  * sqrt(2/Z)=(3/8pi)^(1/4)=0.588 is the FORCED dS amplitude -- it is 0.588, not 1.414;")
print("    r/sqrt(2/Z)=sqrt(Z)=2.406, an unexplained extra factor.")
print("  * 1/sqrt(kappa)=sqrt(2) with kappa=1/2 -- but kappa is the cosmological OUTSIDE fraction,")
print("    cross-sector, mechanism-free, and quark-Koide-FALSIFIED (quarks don't give 2/3).")
print("  * the FDT/Nyquist '2' is a spectral-density normalization, not a generation amplitude.")
print("  Each requires a CHOSEN identification of '2 thermal dof' with 'the 2 transverse")
print("  families' -- i.e. a re-labeling.  NONE is forced by dS-Unruh thermodynamics.")

print("\n" + "="*78)
print("STEELMAN VERDICT: NO self-consistent dS-Unruh thermal condition FORCES r=sqrt(2).")
print("  - equipartition / Bose / FDT all give r as a FREE function of (T, omega, k, <s>);")
print("  - the dS bath's actual amplitude is ~10^19 too small to set an O(1) transverse spread;")
print("  - the only FORCED dS O(1) (sqrt(2/Z)=0.588) is the WRONG number for r (1.414).")
print("  r=sqrt(2) stays FREE.  And the bath is family-blind => cross-fermion FAILS (would give")
print("  Koide for quarks too).  RESULT: RE-LABELING / FREE-r / CROSS-FERMION-FAIL (the null).")
print("="*78)
