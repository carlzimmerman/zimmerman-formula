"""
agentSS Part 3 — THE DECISIVE MOMENT-RATIO COMPUTATION.

Compute R(Delta) = 4 j3 / j2^2 for the symmetry-canonical spectral measures and check:
  (1) convergence of the discrete moment sums (a tower has INFINITE rungs -> do j2, j3 converge?);
  (2) dependence on the (origin, residue) choice -- if a symmetry FORCED the line shape, the ratio
      would be choice-INDEPENDENT;
  (3) numerical value vs G_sat target.

CRUCIAL REALITY CHECK (agentRR): the edge surface 4 j3/j2^2 = G_sat is built for a SINGLE peaked
resonance line rho(s) (a NARROW gain peak, center s_g, width Gamma), whose 2nd & 3rd CENTRAL moments
(about the line center) give j2 ~ Gamma^2, j3 ~ Gamma^2 * (skew). For a narrow symmetric line j3->0
=> G_sat -> 0; the fold needs an ASYMMETRIC (skewed) line. So the real test of the QNM tower:
  does the QNM spectral density, treated as the gain line shape, have CENTRAL moments j2, j3 whose
  ratio 4 j3/j2^2 is FORCED by SL(2,R)/modular/SO(4,1) onto G_sat?

I'll compute CENTRAL moments (about the spectral mean) of the discrete QNM measure, which is the
physically correct object for a line shape. Test both residue choices.
"""
import sympy as sp
import mpmath as mp
mp.mp.dps = 40

def poch_m(a, k):
    r = mp.mpf(1)
    for i in range(k):
        r *= (a + i)
    return r

def moments_central(Delta, residue='char', smax=200000):
    """Central moments j1(mean), j2, j3 of the discrete measure a_n at positions s_n=n (detuning)."""
    D = mp.mpf(Delta)
    # weights
    wsum = mp.mpf(0); m1=mp.mpf(0)
    ws=[]
    for n in range(0, smax):
        if residue=='char':
            a = poch_m(2*D, n)/mp.factorial(n)         # (2D)_n/n!  -> DIVERGES (grows); test convergence
        elif residue=='norm':
            a = 1/(mp.factorial(n)*poch_m(2*D, n))      # 1/[n!(2D)_n] -> converges fast
        elif residue=='exp':
            a = poch_m(2*D, n)/mp.factorial(n) * mp.mpf(0)  # placeholder
        ws.append(a)
        wsum += a; m1 += a*n
        if residue in ('norm',) and n>5 and a < mp.mpf(10)**(-50):
            break
    mean = m1/wsum
    j2 = mp.mpf(0); j3=mp.mpf(0)
    for n,a in enumerate(ws):
        d = n-mean
        j2 += a*d*d
        j3 += a*d*d*d
    j2/=wsum; j3/=wsum
    return wsum, mean, j2, j3

print("=== Residue choice 'norm' = 1/[n!(2Delta)_n] (normalized descendant, CONVERGES) ===")
print(f"{'Delta':>8} {'sum':>14} {'mean':>12} {'j2':>14} {'j3':>16} {'4j3/j2^2':>14}")
for Dv in [0.5, 1.0, 1.5, 2.0, 3.0, 5.0]:
    wsum, mean, j2, j3 = moments_central(Dv, 'norm')
    R = 4*j3/j2**2 if j2!=0 else mp.nan
    print(f"{Dv:>8} {float(wsum):>14.6f} {float(mean):>12.6f} {float(j2):>14.6e} {float(j3):>16.6e} {float(R):>14.6f}")
print()
print(">>> Check: does 4 j3/j2^2 depend on Delta (=> PERMITS a range, tuned by Delta)?")
print(">>> Or is it a Delta-independent constant (=> a symmetry FORCES one value)?")
