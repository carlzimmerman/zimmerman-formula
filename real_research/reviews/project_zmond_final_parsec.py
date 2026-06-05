#!/usr/bin/env python3
"""
Can Z-MOND (evolving a0=cH(z)/Z) solve the final-parsec problem where constant-a0 MOND can't? Worked honestly.
=============================================================================================================
Honest direct answer: NO -- but there is ONE real, distinctive (modest, uncertain) channel, so here is the full
picture rather than a hand-wave. The question is sharp because Z-MOND's a0 was LARGER in the past, so maybe the
final parsec was in the MOND regime at high z. Check it.

THE KEY NUMBER: the SMBH's MOND radius r_M = sqrt(G M_bh / a0) -- the radius where the binary's own gravity g=a0.
Inside r_M: Newtonian (g>a0, MOND does nothing). Outside r_M: MOND. For a 1e9 Msun BH, r_M ~ 1 kpc -- so the final
parsec (1 pc) is ~1000x INSIDE r_M, deeply Newtonian. Evolving a0 shrinks r_M by only sqrt(E(z)) (~/1.7 at z=2), so
the final parsec stays ~600x inside r_M at z=2. To bring a0 up to the final-parsec acceleration (~1e-4 m/s^2) you'd
need E(z)~1e6 (z~1e4) -- long before SMBHs exist. So at NO epoch when black holes exist does the final parsec enter
the MOND regime, even for Z-MOND. The stall is Newtonian for constant-a0 AND evolving-a0 MOND. [robust, decisive]

THE ONE DISTINCTIVE CHANNEL (honest, modest, uncertain): the loss cone is REFILLED by stars whose orbits reach
out to >~ r_M ~ kpc -- the MOND region. Bigger a0 at high z -> SMALLER r_M -> MORE of the nucleus is in the MOND
(enhanced-gravity) regime at the z~1-2 merger peak -> distinctively stronger outer dynamics / refilling than
constant-a0 MOND or LCDM. This does NOT cross the final parsec (still Newtonian), but it is a real, high-z-weighted
boost to the binary SUPPLY/hardening rate -- a distinctive prediction, not a solution. Needs numpy.
"""
import numpy as np

c=2.998e8; G=6.674e-11; Msun=1.989e30; pc=3.086e16; kpc=1e3*pc; Mpc=3.086e22; H0=67.4e3/Mpc
a0=1.2e-10; Z=2*np.sqrt(8*np.pi/3)
E=lambda z: np.sqrt(0.315*(1+z)**3+0.685)


def r_MOND(M_bh_solar, a0_val):
    return np.sqrt(G*M_bh_solar*Msun/a0_val)/pc          # in pc


def main():
    print("#"*100); print("# Can Z-MOND (evolving a0) solve the final parsec? -- worked honestly"); print("#"*100+"\n")

    print("="*100); print("(1) the SMBH MOND radius r_M vs the final parsec (1 pc) -- today"); print("="*100)
    print(f"   {'M_bh [Msun]':>12}{'r_M (a0 today) [pc]':>22}{'final pc is X inside':>22}{'regime @1pc':>14}")
    for M in (1e8,1e9,1e10):
        rM=r_MOND(M,a0)
        print(f"   {M:>12.0e}{rM:>22.0f}{rM/1.0:>22.0f}x{'Newtonian':>13}")
    print("   => the final parsec is 300-3400x INSIDE the MOND radius -> deeply Newtonian. MOND is irrelevant there.\n")

    print("="*100); print("(2) does evolving a0 (larger at high z) bring the final parsec into MOND?"); print("="*100)
    M=1e9
    print(f"   for M_bh=1e9 Msun:   r_M(z) = r_M(0)/sqrt(E(z))   (bigger a0 -> smaller MOND radius)")
    for z in (0,1,2,5):
        rM=r_MOND(M,a0*E(z))
        print(f"     z={z}: E={E(z):.2f}, a0(z)={a0*E(z):.2e}, r_M={rM:.0f} pc  -> final pc still {rM/1.0:.0f}x inside")
    # what E(z) would be needed to reach the final-parsec acceleration?
    g_fp=G*M*Msun/(1*pc)**2
    E_need=g_fp/a0/Z          # a0(z)=cH/Z=a0*E ; need a0(z) ~ g_fp -> E ~ g_fp/(a0)... (Z folded via a0=cH0/Z def)
    print(f"   the final-parsec acceleration is g~{g_fp:.1e} m/s^2; to make a0(z)~g you need E(z)~{g_fp/a0:.0e},")
    print(f"   i.e. z~{((g_fp/a0)**2/0.315)**(1/3):.0e} (E=sqrt(0.315(1+z)^3)) -- long before SMBHs exist (z<~10). NEVER for Z-MOND.\n")

    print("="*100); print("(3) the one distinctive Z-MOND channel: high-z-weighted loss-cone refilling"); print("="*100)
    print(f"   loss-cone refilling comes from stars reaching out to >~ r_M ~ kpc (the MOND region). Bigger a0 at")
    print(f"   high z -> smaller r_M -> MORE of the nucleus is MOND-enhanced at the z~1-2 merger peak:")
    for z in (0,1,2):
        print(f"     z={z}: r_M={r_MOND(M,a0*E(z)):.0f} pc (MOND region starts here; smaller=more nucleus in MOND)")
    print(f"   => distinctively stronger OUTER dynamics/refilling at high z than constant-a0 MOND or LCDM. Modest,")
    print(f"      uncertain, and it does NOT cross the final parsec -- it boosts the SUPPLY rate, weighted to high z.\n")

    print("="*100); print("VERDICT"); print("="*100)
    print("""  Direct answer: NO -- Z-MOND does NOT solve the final-parsec problem. The final parsec (1 pc) is 300-3400x
  INSIDE the SMBH's MOND radius (~kpc), so the stall is deeply Newtonian; evolving a0 shrinks the MOND radius by
  only sqrt(E(z)) (~1.7x at z=2), nowhere near reaching 1 pc, and to make a0 reach the final-parsec acceleration
  you'd need z~1e4 (before black holes exist). The stall is Newtonian for constant-a0 AND evolving-a0 MOND alike.
  What Z-MOND CAN distinctively do: because a0 was larger at high z, MORE of the galactic nucleus was in the MOND
  regime at the z~1-2 merger peak, distinctively enhancing the OUTER dynamics that REFILL the loss cone -- a real,
  high-z-weighted boost to the binary supply/hardening rate (beyond constant-a0 MOND and LCDM). That is a
  distinctive prediction for the nHz background's redshift content, NOT a solution to the final parsec. Honest: a
  modest, uncertain channel -- the framework's real test stays the z~3 a0(z) measurement.""")
    print("#"*100)


if __name__=="__main__":
    main()
