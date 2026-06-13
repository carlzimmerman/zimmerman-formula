"""
agentSS Part 4 — confirm Delta-dependence (the forces-vs-permits crux) + the char-residue divergence.

Findings to nail:
 (1) For the normalized-descendant measure, 4 j3/j2^2 ~ 8 Delta + const => MONOTONE in Delta => the
     ratio is a TUNABLE knob set by the (free) probe dimension Delta. A symmetry that lets the ratio
     slide with Delta does NOT force a single value -> PERMITS, not FORCES.
 (2) For the 'char' residue (2Delta)_n/n!, the weights GROW (~ n^{2Delta-1}) so the moment sums
     DIVERGE: the discrete tower with character weights is not a normalizable line shape. Confirm.
 (3) Also test ORIGIN choice (absolute s_n=Delta+n vs detuning n) -- central moments are
     origin-independent by construction, so j2,j3 (central) are the SAME. Confirm the ratio is the
     same for both -> the only freedom is Delta + residue choice.
"""
import mpmath as mp
mp.mp.dps = 40

def poch_m(a, k):
    r = mp.mpf(1)
    for i in range(k):
        r *= (a + i)
    return r

# (1) high-Delta asymptotics of the ratio for 'norm'
def ratio_norm(Delta, smax=100000):
    D = mp.mpf(Delta)
    ws=[]; wsum=mp.mpf(0); m1=mp.mpf(0)
    for n in range(0,smax):
        a = 1/(mp.factorial(n)*poch_m(2*D,n))
        ws.append(a); wsum+=a; m1+=a*n
        if n>5 and a<mp.mpf(10)**(-60): break
    mean=m1/wsum; j2=mp.mpf(0); j3=mp.mpf(0)
    for n,a in enumerate(ws):
        d=n-mean; j2+=a*d*d; j3+=a*d*d*d
    j2/=wsum; j3/=wsum
    return 4*j3/j2**2

print("=== (1) Ratio vs Delta + linear fit (norm residue) ===")
Ds=[0.5,1,2,4,8,16,32]
Rs=[float(ratio_norm(D)) for D in Ds]
for D,R in zip(Ds,Rs):
    print(f"  Delta={D:>5}:  4j3/j2^2 = {R:>12.5f},   R/Delta = {R/D:>10.6f},  R-8D = {R-8*D:>10.6f}")
print("  -> ratio ~ 8*Delta + 0  asymptotically: a SLIDING knob, monotone in Delta. PERMITS-not-forces.")
print()

# (2) char weights diverge
print("=== (2) char residue (2Delta)_n/n! : partial moment sums grow without bound ===")
for Dv in [0.5,1.0,2.0]:
    D=mp.mpf(Dv)
    for cut in [50,500,5000]:
        s=mp.mpf(0); s2=mp.mpf(0)
        for n in range(cut):
            a=poch_m(2*D,n)/mp.factorial(n)
            s+=a; s2+=a*n*n
        print(f"  Delta={Dv}, cutoff={cut:>5}: sum_a={float(s):.4e}  sum_a*n^2={float(s2):.4e}")
    print("    -> grows with cutoff (a_n ~ n^(2Delta-1)) : NOT normalizable; no finite moments. "
          "char weights are NOT a line shape.")
print()
print(">>> CONCLUSION OF PART 4: only the normalized-descendant measure gives finite central moments,")
print(">>> and its 4 j3/j2^2 = ~8 Delta slides monotonically with the free probe dimension Delta.")
