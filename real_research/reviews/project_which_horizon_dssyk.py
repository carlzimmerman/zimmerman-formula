#!/usr/bin/env python3
"""
WHICH HORIZON SETS a0? The framework's own DSSYK engine selects the EVENT horizon -- so a0 ~ sqrt(rho_DE),
constant-to-declining, NOT a0 = cH rising. This resolves the high-z rate tension -- and REVISES the headline.
============================================================================================================
The framework rests on two foundations that quietly use DIFFERENT cosmological horizons:

  A. Verlinde/Padmanabhan emergent gravity -> a0 ~ c H  : the APPARENT (Hubble) horizon, R_A = c/H(z).
     In a matter+Lambda universe this RISES with z: a0 prop H(z) = H0 E(z) (x4.6 at z=3). The original headline.
  B. Narovlansky-Verlinde DSSYK = de Sitter -> the dual is the de Sitter STATIC PATCH, bounded by the de Sitter
     EVENT horizon R_dS = c/H_L, H_L = H0 sqrt(OmegaLambda) ~ c sqrt(Lambda/3). Its scale is c H_L ~ c sqrt(Lambda)
     ~ c sqrt(rho_DE) -- CONSTANT for constant Lambda; DESI-evolving if Lambda evolves. NOT rising.

These are physically different horizons (they coincide only in pure de Sitter). The framework's MICROSCOPIC
ENGINE is B (the DSSYK dual is intrinsically the de Sitter event horizon, Narovlansky-Verlinde 2023). So the
ENGINE implies a0 ~ c sqrt(Lambda) ~ sqrt(rho_DE) -- and the a0 = cH (apparent, rising) reading the framework
originally adopted is INCONSISTENT with its own dual. The high-z rotation curves independently disfavor the
rising reading. So internal consistency AND the data point the same way: a0 tracks the EVENT horizon.

CONSEQUENCES, stated straight:
 * a0 ~ sqrt(rho_DE) is DERIVED from the DSSYK = de Sitter dual (the event-horizon scale), NOT a Milgrom
   postulate. This grounds the DESI cross-prediction (project_desi_a0z_crossprediction.py).
 * The framework, done CONSISTENTLY, predicts a0 ~ CONSTANT-to-mildly-DECLINING, the OPPOSITE of its original
   rising headline -- and the consistent prediction is the one the high-z disks favor.
 * This is a REVISION forced by internal consistency + data, NOT a vindication of the rising bet. The rising
   bet was a wrong-horizon error.
HONEST WRINKLE: the pure event horizon gives a0(0)=cH_L/Z ~ 0.93e-10, ~17% below the apparent cH0/Z=1.12e-10
(both inside the observed 1.2+-0.26); the geometric-mean two-horizon form a0 ~ c sqrt(H H_L) splits the
normalization and gives a mild rise. So the ENGINE selects the event/sqrt(rho_DE) FAMILY (constant-to-mild),
decisively away from the steep apparent rise; which member (pure event vs geometric mean) is the normalization
question, set by the dictionary coefficient. Needs numpy.
"""
import numpy as np

c = 2.998e8; G = 6.674e-11; H0 = 67*1e3/3.086e22
Om, OL = 0.315, 0.685
Z = 2*np.sqrt(8*np.pi/3)
E = lambda z: np.sqrt(Om*(1+z)**3 + OL)
HL = H0*np.sqrt(OL)


def rho_de(z, w0, wa):       # DESI evolving DE
    a = 1/(1+z); return (1+z)**(3*(1+w0+wa))*np.exp(-3*wa*(1-a))


def main():
    print("#"*92)
    print("# WHICH HORIZON SETS a0? -- the DSSYK engine selects the EVENT horizon (a0 ~ sqrt(rho_DE))")
    print("#"*92 + "\n")

    print("="*92); print("THE TWO FOUNDATIONS USE DIFFERENT HORIZONS"); print("="*92)
    print(f"  A. emergent gravity   a0 ~ cH      = APPARENT/Hubble horizon  -> a0(z) prop E(z) (RISES)")
    print(f"  B. DSSYK = de Sitter  a0 ~ c H_L   = EVENT/static-patch horizon -> a0 prop sqrt(Lambda)~sqrt(rho_DE)")
    print(f"     H_L = H0 sqrt(OL) = {HL:.3e} /s;  R_dS = c/H_L = {c/HL/3.086e25:.1f} Gly")
    print(f"  a0(0): apparent cH0/Z = {c*H0/Z/1e-10:.2f}e-10 ; event cH_L/Z = {c*HL/Z/1e-10:.2f}e-10  (differ by sqrt(OL)={np.sqrt(OL):.2f},")
    print(f"         degenerate at z=0; both within observed 1.2+-0.26e-10).\n")

    print("="*92); print("THE DISCRIMINATOR -- z-evolution (and what the data say)"); print("="*92)
    print(f"  {'z':>4}{'A: apparent ~E(z)':>20}{'B: event const-L':>20}{'B: event w/ DESI w0wa':>24}")
    for z in (0.5, 1, 2, 3):
        b_desi = np.sqrt(rho_de(z, -0.8, -0.7))
        print(f"  {z:>4.1f}{E(z):>18.2f}x{1.00:>18.2f}x{b_desi:>22.2f}x")
    print("""  high-z rotation curves (Big Wheel, Milgrom/Genzel, RC100): a0 NOT risen x5 -> they DISFAVOR A and FAVOR B.
  So internal consistency (the DSSYK engine IS the event horizon) AND the data BOTH select the event horizon.\n""")

    print("="*92); print("VERDICT -- a resolution AND an honest revision"); print("="*92)
    print(f"""  The framework's headline -- a0 RISES as cH(z)/Z = E(z) -- was a WRONG-HORIZON error: it used the
  apparent/Hubble horizon (Verlinde reading), but the framework's own microscopic engine (DSSYK = de Sitter
  STATIC PATCH) is the EVENT horizon, whose scale is c H_L ~ c sqrt(Lambda) ~ sqrt(rho_DE). The engine therefore
  predicts a0 ~ CONSTANT (constant Lambda) to mildly DECLINING (DESI's weakening Lambda), NOT rising. Two
  independent things select this: (1) internal consistency -- using the same de Sitter horizon the dual is
  built on; (2) the high-z disks, which disfavor the steep rise and favor constant/declining.
  WHAT THIS BUYS: a0 ~ sqrt(rho_DE) is now DERIVED from the DSSYK dual (not Milgrom's postulate), which grounds
  the DESI cross-prediction; and the framework done CONSISTENTLY fits the high-z data that embarrassed the
  rising bet.
  WHAT IT COSTS (reported straight): this is a REVISION, not a vindication -- the framework's original
  distinctive claim (rising a0) is abandoned as a wrong-horizon mistake; the new claim (a0 ~ sqrt(rho_DE),
  constant-to-declining) is LESS distinctive from constant-a0 MOND at z=0 (degenerate, differ only by sqrt(OL)),
  and is testable only by the z-evolution. And the pure event horizon's a0(0)=0.93e-10 is ~17% below the
  apparent normalization, so the geometric-mean two-horizon form may be the true compromise -- a coefficient
  question. NET: the framework's engine resolves its own worst observational tension, by predicting the
  opposite of its original headline. Honest: a stronger, more coherent -- but humbler -- theory.""")
    print("="*92)


if __name__ == "__main__":
    main()
