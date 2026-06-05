#!/usr/bin/env python3
"""
The decisive test made concrete: a JWST+ALMA observing proposal for the coefficient-free bridge a0(z)=sqrt(rho_DE(z)).
=====================================================================================================================
The dark-universe theory's one now-testable claim is the COEFFICIENT-FREE bridge a0(z)/a0(0) = sqrt(rho_DE(z)/rho_DE0)
(THE_A0_LAMBDA_BRIDGE.md). This script turns it into a concrete measurement design: what to observe, with what, how
many, to what precision, to distinguish the three live hypotheses at z~3.

THE THREE HYPOTHESES at z~3 (a0(z=3)/a0(0)):
   * sqrt(rho_DE), DESI DR2 dynamical DE -> 0.74   (the distinctive, faithful prediction: a0 DECLINES)
   * constant Lambda                      -> 1.00   (the safe null)
   * a0 ~ cH(z) (Hubble)                   -> 4.57   (already excluded by Milgrom 2017 -- the dead version)
THE OBSERVABLE: the Baryonic Tully-Fisher zero-point. M_b = V_flat^4/(G a0), so at fixed M_b, V_flat ~ a0^(1/4).
The coefficient-free RATIO a0(z)/a0(0) is read from the SHIFT of the BTFR zero-point between a z~3 sample and a z~0
anchor (SPARC), analyzed through the SAME pipeline so the absolute a0 calibration, the IMF/M_star, and the
interpolation-function systematics CANCEL.

Needs numpy.
"""
import numpy as np

Om,OL=0.315,0.685; c=2.998e8; Mpc=3.086e22; H0=67.4e3/Mpc; Z=2*np.sqrt(8*np.pi/3)
E=lambda z: np.sqrt(Om*(1+z)**3+OL)
w0,wa=-0.752,-0.86
rhoDE=lambda a: a**(-3*(1+w0+wa))*np.exp(-3*wa*(1-a))
a0_sqrtDE=lambda z: np.sqrt(rhoDE(1/(1+z)))


def main():
    print("#"*100); print("# z~3 observing proposal: the coefficient-free bridge a0(z)=sqrt(rho_DE(z)) made concrete"); print("#"*100+"\n")

    print("="*100); print("(1) THE SIGNAL: BTFR zero-point shift (V_flat ~ a0^1/4 at fixed M_b), z=3 vs z=0"); print("="*100)
    for name,r in (("sqrt(rho_DE) [faithful, DESI]",a0_sqrtDE(3)),("constant Lambda [null]",1.0),("cH(z) [dead]",E(3))):
        dlogV=0.25*np.log10(r)
        print(f"   {name:<32} a0(3)/a0(0)={r:>5.2f}  -> Dlog V_flat = {dlogV:+.3f} dex ({100*(10**dlogV-1):+.0f}%)")
    sig=abs(0.25*np.log10(a0_sqrtDE(3)))     # |signal| to distinguish faithful from null
    print(f"   => the test that matters (faithful vs null) is a {sig:.3f} dex shift in V_flat at z=3. The dead Hubble")
    print(f"      version (+0.16 dex) is ~5x larger and already excluded -- so the real measurement targets ~0.033 dex.\n")

    print("="*100); print("(2) SAMPLE SIZE: how many z~2.5-3.5 deep-MOND discs to distinguish faithful from null"); print("="*100)
    sig_gal=0.06     # per-galaxy V_flat precision (dex): rotation curve + inclination + beam, RELATIVE (ratio cancels absolute)
    print(f"   per-galaxy V_flat precision ~{sig_gal} dex (incl. inclination/beam; the z0-anchored RATIO cancels absolute systematics)")
    print(f"   {'detection':>12}{'N galaxies = (n*sig_gal/signal)^2':>40}")
    for nsig in (3,5):
        N=int(np.ceil((nsig*sig_gal/sig)**2))
        print(f"   {str(nsig)+'-sigma':>12}{N:>40}")
    print(f"   => ~30 clean deep-MOND discs at z~2.5-3.5 give a 3-sigma separation of the DESI-decline from constant;")
    print(f"      ~80 give 5-sigma. Feasible with a dedicated JWST+ALMA program. (Statistics, not heroics.)\n")

    print("="*100); print("(3) THE MEASUREMENT DESIGN"); print("="*100)
    print("""   TARGET: 30-80 rotation-supported, LOW-surface-density discs at z=2.5-3.5 (M*=10^9.5-10^10.5) selected to
           reach g_bar < a0 in their outskirts (the deep-MOND regime -- NOT the compact massive monsters, which
           stay Newtonian and only give upper limits).
   OBSERVE:
     * JWST/NIRSpec IFU -- spatially-resolved Halpha/[OIII] -> the OUTER rotation curve -> V_flat.
     * ALMA [CII]/CO    -> cold-gas mass + an independent dynamical tracer -> the baryonic mass M_b (gas+stars).
     * JWST/NIRCam SED  -> stellar mass M_star.
   ANCHOR: re-reduce a z~0 SPARC-like sample through the IDENTICAL V_flat + M_b pipeline, so the BTFR zero-point
     RATIO a0(z)/a0(0) is coefficient-free and cancels IMF/M*/interpolation/absolute-a0 systematics.
   ANALYZE: fit the BTFR zero-point in z-bins; the shift gives a0(z)/a0(0); compare to sqrt(rho_DE(z)) from DESI
     BAO and to the flat null. Report the coefficient-free ratio -- NO need to know 32pi or the absolute a0.
   KILL CONDITIONS: a0 rising (excludes the framework's faithful decline); a0 flat at <1-sigma from sqrt(rho_DE)
     decline with N>80 (disfavors the distinctive branch, leaves the safe constant core).
   FEASIBILITY: ~tens of hours JWST + matched ALMA; the deep-MOND-disc sample is the same one the field is already
     assembling for high-z dynamics. The novel content is the z0-anchored RATIO analysis tied to DESI's rho_DE(z).\n""")

    print("="*100); print("VERDICT"); print("="*100)
    print(f"""  The decisive test is concrete and modest: ~30 (3-sigma) to ~80 (5-sigma) low-surface-density deep-MOND discs at
  z~2.5-3.5, JWST/NIRSpec rotation curves + ALMA gas masses, analyzed as the z0-anchored, coefficient-free BTFR
  zero-point ratio a0(z)/a0(0), compared to DESI's sqrt(rho_DE(z)). It distinguishes the faithful DESI-decline
  (0.74) from the constant null (1.00) at z=3 -- a {sig:.3f} dex V_flat shift -- and trivially excludes the dead
  Hubble rise. This is the real experiment the dark-universe theory lives or dies on, and it needs no new theory,
  no coefficient, and no facility that does not exist -- only a dedicated program and the z0-anchored ratio analysis.""")
    print("#"*100)


if __name__=="__main__":
    main()
