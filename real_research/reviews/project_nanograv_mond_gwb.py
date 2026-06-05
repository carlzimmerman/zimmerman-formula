#!/usr/bin/env python3
"""
The one PRO-framework observable, worked honestly: does MOND (+evolving a0) raise the nHz GW background? -> SOFT, weak.
=====================================================================================================================
The ledger flags the nHz/PTA stochastic GW background as 'the one novel pro-framework observable, unworked,
publishable': NANOGrav 15yr (2023) measures a background at the HIGH end of supermassive-black-hole-binary (SMBHB)
predictions, and MOND-enhanced dynamical friction might help SMBHBs merge (the 'final parsec problem') -> more
mergers -> higher GWB. Worked here. HONEST RESULT: it is a SOFT, weak hint, NOT a win -- and the optimistic note
needs tempering, because the actual bottleneck (the final parsec) is in the NEWTONIAN regime where MOND does nothing.

THE DECISIVE PHYSICS IS THE ACCELERATION REGIME AT EACH STAGE OF THE MERGER:
  stage                         separation     g = GM/r^2        g/a0          MOND modifies?
  galaxy merger / inspiral      ~5-10 kpc      ~1-2 a0           ~1            YES (deep-MOND friction enhanced)
  SMBHB hardening / final pc    ~1 pc          ~1e-4 m/s^2       ~1e6          NO  (deeply Newtonian)
  GW-driven coalescence         << pc          strong field      huge          NO  (GR)
=> MOND speeds the LARGE-SCALE inspiral (galaxies arrive faster, in greater numbers) but does NOT touch the
   final-parsec STALL, which is the actual bottleneck and is Newtonian. So 'MOND solves the final parsec' is wrong;
   the honest claim is only 'MOND may raise the SUPPLY rate of binaries to the stalling radius'.

THE EVOLVING-a0 (framework-distinctive) PART: a0(z) is larger at high z (E(z)), so the galaxy-scale friction
enhancement was STRONGER at z~1-2 where most SMBHB mergers occur -> the framework predicts the GWB enhancement is
weighted to high z (a spectral/redshift signature), beyond constant-a0 MOND. Distinctive but tiny.

HONEST verdict: a soft, order-of-magnitude, RIGHT-DIRECTION hint (GWB up by ~sqrt(friction boost) ~ 1.3-1.8x IF the
rate is large-scale-limited), in the ballpark of NANOGrav's high amplitude -- but (i) the NANOGrav 'excess' is
marginal and model-dependent (standard SMBHB models can already fit it), (ii) the bottleneck is Newtonian so the
boost may not apply at all, (iii) this is an order-of-magnitude estimate, not a population-synthesis result.
=> downgrade the ledger's 'novel publishable observable' to 'qualitative soft hint, honestly weak'. Needs numpy.
"""
import numpy as np

c=2.998e8; G=6.674e-11; Msun=1.989e30; pc=3.086e16; kpc=1e3*pc
a0=1.2e-10; Mpc=3.086e22; H0=67.4e3/Mpc
E=lambda z: np.sqrt(0.315*(1+z)**3+0.685)


def g_of(M_solar, r_m):
    return G*M_solar*Msun/r_m**2


def main():
    print("#"*102); print("# nHz GW background under MOND + evolving a0: the one pro-framework observable, worked honestly"); print("#"*102+"\n")

    print("="*102); print("(1) THE DECISIVE REGIME CHECK: which merger stages are MOND vs Newtonian?"); print("="*102)
    stages=[("galaxy merger / inspiral", 1e11, 8*kpc),
            ("SMBHB hardening / final parsec", 1e9, 1*pc),
            ("loss-cone stars at influence radius", 1e9, 10*pc)]
    print(f"   {'stage':<38}{'M[Msun]':>10}{'r':>10}{'g[m/s^2]':>12}{'g/a0':>10}  regime")
    for name,M,r in stages:
        g=g_of(M,r); reg='DEEP-MOND' if g<a0 else ('transition' if g<5*a0 else 'Newtonian')
        rs=f"{r/kpc:.0f}kpc" if r>=kpc else f"{r/pc:.0f}pc"
        print(f"   {name:<38}{M:>10.0e}{rs:>10}{g:>12.2e}{g/a0:>10.1e}  {reg}")
    print("   => galaxy-scale inspiral is at the MOND scale (MOND helps); the final-parsec STALL is Newtonian (MOND")
    print("      does NOT help). The bottleneck is in the wrong regime for MOND to solve. [decisive, robust]\n")

    print("="*102); print("(2) the size of the effect IF the rate is large-scale (MOND) limited"); print("="*102)
    boost_friction=3.0   # deep-MOND dynamical-friction enhancement, ~2-5 (Nipoti/Sanchez-Salcedo; order-of-mag)
    A_gwb_boost=np.sqrt(boost_friction)   # h_c amplitude ~ sqrt(merger-rate density)
    print(f"   deep-MOND dynamical-friction enhancement ~ {boost_friction:.0f}x (literature order-of-magnitude)")
    print(f"   GWB strain amplitude A ~ sqrt(rate) -> boost ~ sqrt({boost_friction:.0f}) = {A_gwb_boost:.2f}x")
    print(f"   NANOGrav 15yr A ~ 2.4e-15 sits ~1.5-2x above fiducial SMBHB models -> the boost is the RIGHT")
    print(f"   ORDER, IF (big if) the merger rate is set by the large-scale stage, not the Newtonian final parsec.\n")

    print("="*102); print("(3) the framework-distinctive part: evolving a0 weights the boost to high z"); print("="*102)
    print(f"   a0(z)/a0(0)=E(z): z=0.5 -> {E(0.5):.2f}, z=1 -> {E(1):.2f}, z=2 -> {E(2):.2f}. Stronger MOND friction")
    print(f"   at the z~1-2 merger peak -> the GWB enhancement is weighted to high z vs constant-a0 MOND. A real but")
    print(f"   tiny spectral/redshift signature (future PTA + individual sources), NOT a near-term discriminator.\n")

    print("="*102); print("VERDICT"); print("="*102)
    print("""  Worked honestly, the nHz GWB is a SOFT, WEAK, right-direction hint -- not the clean pro-framework win the ledger
  suggested. The decisive problem: the final-parsec STALL (the actual bottleneck) is deeply Newtonian (g ~ 1e6 a0),
  so MOND cannot solve it; MOND only speeds the large-scale (galaxy) inspiral. IF the merger rate is large-scale-
  limited, MOND raises the GWB amplitude by ~sqrt(friction boost) ~ 1.3-1.8x -- the right order for NANOGrav's high
  value -- but the NANOGrav 'excess' is marginal/model-dependent and the bottleneck-regime caveat may kill the boost
  entirely. Evolving a0 adds a tiny high-z weighting. NET: a qualitative soft hint worth one honest paragraph, NOT a
  'novel publishable observable' -- the ledger line is hereby tempered. The framework's real test stays the z~3
  a0(z) measurement, not the PTA.""")
    print("#"*102)


if __name__=="__main__":
    main()
