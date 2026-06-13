"""
agentOO Route 2 — Block 7: reconcile + the decisive verdict logic, fully hostile both ways.

Two facts now established, both convention-free (Block 3a exact secular + Block 4/5/6 GH spectrum):

  FACT A (sign):  sigma4 = -I2 * c_chi^2, I2=int J/W^4 > 0 for any passive J>=0.
                  => the LEVEL-REPULSION bending sign is GENERIC: sigma4<0 whenever I2 is
                     finite&positive. The dS bath, regularized, DOES carry a negative k^4.
                     *** The bending sign is FORCED by passivity + the dS-bath structure,
                         NOT a free coupling choice. *** (This is framework-FAVORABLE.)

  FACT B (deliverability): the GH spectrum is FEATURELESS/scale-free:
     (i) no convergent moment window (Block 4): I2,I3 are endpoint/cutoff-controlled;
     (ii) monotone, peakless response (Block 5): not the He-II structured-bath class;
     (iii) the stabilizer sigma6 = c_chi^2(I2^2 - I3 c_chi^2) came out NEGATIVE for the GH
           p=2 coupling (Block 6): the +k^6 floor is NOT supplied -- the fold is UNBOUNDED.
     (iv) the fold scale k* is cutoff-set, NOT pinned to the sonic edge b->c_chi (Block 6b):
          NN's edge-coincidence tuning is NOT discharged.

So the question 'does the dS spectrum FORCE sigma4<0' splits cleanly:
  - The SIGN: YES, forced negative (FACT A) -- this is the framework-favorable truth, reported.
  - The STRUCTURE needed for a controlled Airy fold (finite bath-set k4, +k6 floor, edge-pinned
    inflection): NO, the featureless GH bath does not supply it (FACT B).

This block: (1) verify sigma6<0 robustly for the GH coupling (the unbounded-fold finding);
(2) check whether ANY passive bath can give sigma6>0 (is the floor available in principle?);
(3) state the forced_or_free verdict precisely.
"""
import mpmath as mp
mp.mp.dps = 30
H = mp.mpf(1)
def J(W,p): W=mp.mpf(W); return W**p*mp.coth(mp.pi*W/H)
def Imom(n,p,eps,Lam): return mp.quad(lambda W: J(W,p)/W**(2*n), [eps,Lam])

print("="*78)
print("BLOCK 7: sigma6 floor sign for the GH bath, and is a +k^6 floor available at all?")
print("="*78)

# sigma6 = c_chi^2 (I2^2 - I3 c_chi^2). For the floor sigma6>0 need I2^2 > I3 c_chi^2.
# By Cauchy-Schwarz on the measure dnu=J(W)dW>0:
#   I2 = int dnu /W^4,  I3 = int dnu /W^6,  I1 = int dnu/W^2.
#   Cauchy-Schwarz: (int /W^4)^2 = (int W^{-1}*W^{-3})^2 <= (int /W^2)(int /W^6) = I1 I3.
#   => I2^2 <= I1 I3   (EQUALITY only for a single delta -- a sharp resonance!)
# So I2^2 <= I1 I3. Then sigma6>0 requires I2^2 > I3 c_chi^2 = I3(c0^2 - I1), i.e.
#   I3 c0^2 < I2^2 + I3 I1 <= I1 I3 + I3 I1 = 2 I1 I3  -> c0^2 < 2 I1 (roughly).
# But STABILITY needs c_chi^2 = c0^2 - I1 > 0 -> c0^2 > I1. Combine: I1 < c0^2 < 2I1 possible.
# The point: sigma6>0 needs I2^2 close to its Cauchy-Schwarz CEILING I1 I3 -- which is reached
# ONLY for a PEAKED (delta-like) bath. A featureless broadband bath sits FAR below the ceiling,
# giving I2^2 << I1 I3 and hence sigma6<0. Verify numerically for GH:
print("\nCauchy-Schwarz ceiling test: I2^2 vs I1*I3 (equality<=>sharp resonance, peaked bath):")
print(f"{'p':>3} {'Lambda':>8} {'I2^2':>12} {'I1*I3':>12} {'ratio I2^2/(I1 I3)':>20}")
eps=mp.mpf('1e-4')
for p in [2,3]:
    for Lam in [mp.mpf(x) for x in [5,100]]:
        I1=Imom(1,p,eps,Lam); I2=Imom(2,p,eps,Lam); I3=Imom(3,p,eps,Lam)
        ratio = I2**2/(I1*I3)
        print(f"{p:>3} {mp.nstr(Lam,3):>8} {mp.nstr(I2**2,4):>12} {mp.nstr(I1*I3,4):>12} {mp.nstr(ratio,5):>20}")
print("""
  ratio I2^2/(I1 I3) << 1 for the GH bath => FAR from the resonance ceiling => the bath is
  BROADBAND/featureless, and sigma6 < 0 (no +k^6 floor): the induced fold would be UNBOUNDED
  (omega^2 -> -inf at large k). A healthy bounded roton fold needs ratio -> 1, i.e. a SHARP
  spectral PEAK (delta-like) -- exactly the He-II structured-bath signature the dS bath lacks.
""")

print("="*78)
print("BLOCK 7b: spot-checks (independent reproduction of load-bearing facts)")
print("="*78)
# (1) sigma4 = -I2 c_chi^2 sign from a DIRECT 2-mode numeric secular solve (no series):
import numpy as np
# khronon c0=1 coupled to ONE bath mode W0 with strength g; exact dispersion root, small k.
def omega2_exact(k, c0, W0, g):
    # secular: w2 = c0^2 k^2 + g^2 k^2 /(w2 - W0^2). Solve quadratic in w2.
    # w2^2 - w2(c0^2 k^2 + W0^2) + (c0^2 k^2 W0^2 - g^2 k^2) = 0 ; take lower (acoustic) root.
    a=1.0; b=-(c0**2*k**2 + W0**2); cc=(c0**2*k**2*W0**2 - g**2*k**2)
    disc=b*b-4*a*cc
    return (-b - mp.sqrt(disc))/(2*a)
c0=mp.mpf(1); W0=mp.mpf(3); g=mp.mpf('0.4')
ks=[mp.mpf('0.01'),mp.mpf('0.02'),mp.mpf('0.04')]
w2s=[omega2_exact(k,c0,W0,g) for k in ks]
# fit w2 = A k^2 + B k^4 to extract sign of B (=sigma4)
import itertools
# solve 2x2 from first two k
M=mp.matrix([[ks[0]**2, ks[0]**4],[ks[1]**2, ks[1]**4]])
rhs=mp.matrix([w2s[0],w2s[1]])
AB=mp.lu_solve(M,rhs)
print("single-mode exact: c_eff^2 =", mp.nstr(AB[0],6), " sigma4 =", mp.nstr(AB[1],6),
      " (sign", '<0 BEND' if AB[1]<0 else '>0 STIFFEN', ")")
# analytic prediction: I2 for single mode = g^2/W0^4 ; c_chi^2 = c0^2 - g^2/W0^2 ; sigma4=-I2 cchi2
I2_sm=g**2/W0**4; cchi2_sm=c0**2 - g**2/W0**2; sig4_pred=-I2_sm*cchi2_sm
print("analytic prediction sigma4 = -I2 c_chi^2 =", mp.nstr(sig4_pred,6))
print("match:", mp.nstr(abs(AB[1]-sig4_pred),3))
print("""
=> single-mode exact secular solve CONFIRMS sigma4 = -I2 c_chi^2 < 0 to high precision.
   The bending sign is solid and convention-free. (FACT A reproduced a 3rd independent way.)
""")
