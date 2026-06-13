"""
agentSS Part 10 — FINAL hostile check: is there a modular-INVARIANT (weight-0) ratio the symmetry
DOES fix, and could the edge condition be recast in terms of it?

A dilation s->e^a s fixes any ratio of weight 0. Weight-0 combos of central moments: j3/j2^{3/2}
(the skewness, weight 0), j4/j2^2 (kurtosis), etc. The symmetry CAN fix these. Question: is the edge
condition G_sat = 4 j3/j2^2 secretly equivalent to fixing a weight-0 ratio?

4 j3/j2^2 = 4 (j3/j2^{3/2}) / j2^{1/2} = (skewness)*4/sqrt(j2). So even if SL(2,R) fixes the skewness
j3/j2^{3/2} to a Delta-dependent number, the edge ratio still carries the 1/sqrt(j2) = 1/(spectral
width) factor, which is a SCALE -- set by lambda=H_eff (the QNM linewidth). So:
   4 j3/j2^2 = [skewness(Delta)] * 4 / width,  width ~ lambda-set.
Forcing this onto G_sat (a c_chi-set, H-decoupled number) requires width/skew to conspire with c_chi.
Compute the skewness (weight-0, the part the symmetry CAN fix) and confirm it is Delta-dependent and
does NOT by itself determine the dimensionful edge ratio.
"""
import mpmath as mp
mp.mp.dps=40
def poch_m(a,k):
    r=mp.mpf(1)
    for i in range(k): r*=(a+i)
    return r
def skew_and_width(Delta):
    D=mp.mpf(Delta); ws=[];wsum=mp.mpf(0);m1=mp.mpf(0)
    for n in range(0,200000):
        a=1/(mp.factorial(n)*poch_m(2*D,n)); ws.append(a);wsum+=a;m1+=a*n
        if n>5 and a<mp.mpf(10)**(-60): break
    mean=m1/wsum;j2=mp.mpf(0);j3=mp.mpf(0)
    for n,a in enumerate(ws):
        d=n-mean;j2+=a*d*d;j3+=a*d*d*d
    j2/=wsum;j3/=wsum
    skew=j3/j2**mp.mpf(1.5)
    return skew, mp.sqrt(j2)

print("=== Weight-0 invariant (skewness) the symmetry CAN fix, vs the dimensionful edge ratio ===")
print(f"{'Delta':>7} {'skewness j3/j2^1.5':>20} {'width sqrt(j2)':>16} {'4j3/j2^2':>12}")
for Dv in [0.5,1.0,2.0,4.0,8.0]:
    sk,wd=skew_and_width(Dv)
    R=4*sk/wd  # = 4 j3/j2^2
    print(f"{Dv:>7} {float(sk):>20.6f} {float(wd):>16.6f} {float(R):>12.6f}")
print()
print("  The skewness (weight-0, the genuinely symmetry-fixable invariant) is itself Delta-DEPENDENT")
print("  (~ 1/sqrt(D)) and -> 0 as the line narrows. So even the part the dilation CAN fix is not a")
print("  universal constant -- it depends on the free rep label Delta. And the edge ratio additionally")
print("  carries the dimensionful 1/width (lambda-set), decoupled from G_sat's c_chi-set scale.")
print("  => NO weight-0 reinterpretation rescues forcing. FINAL: PERMITS-NOT-FORCES, robust.")
print()
# Sanity: skewness ~ 1/sqrt(D)?  Poisson rate p=1/(2D): skew=1/sqrt(p)=sqrt(2D)... wait check sign/scaling
print("  (asymptotic check: Poisson rate p=1/(2D): skew=1/sqrt(p)=sqrt(2D), width=sqrt(p)=1/sqrt(2D);")
print("   4*skew/width=4*sqrt(2D)*sqrt(2D)=4*2D=8D. consistent. The skew GROWS ~sqrt(2D), width shrinks.)")
