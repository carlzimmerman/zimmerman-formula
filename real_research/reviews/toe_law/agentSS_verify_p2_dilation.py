"""
agentSS VERIFY part 2 — the MODULAR/DILATION scaling weight of 4 j3/j2^2.
Route claim: modular flow = static-patch boost = dilation s->e^a s of the spectral axis;
under it central moments j_n -> e^{n a} j_n, so 4 j3/j2^2 -> e^{(3-2*2)a}? NO -- route says
e^{(3-4)a}=e^{-a}, weight -1. Let me derive the weight FROM SCRATCH, ruthlessly, because the
exponent bookkeeping is exactly the kind of place an error hides.

A CENTRAL moment j_n = <(s-<s>)^n> has dimension [s]^n. Under s->e^a s every length scales,
so j_n -> e^{n a} j_n (n-th power of a length). Then
   4 j3 / j2^2  has dimension [s]^3 / ([s]^2)^2 = [s]^{3-4} = [s]^{-1}.
=> scales as e^{(3-4)a} = e^{-a}: weight -1.  CONFIRM by explicit numeric dilation.
Also: is the EDGE TARGET G_sat dimensionless or [s]^{-1}? If both sides are [s]^{-1} and
co-dilate, the equation IS scale-covariant and the dilation does NOT obstruct -> the route's
H1 rescue (G_sat is scale-DECOUPLED) is then the load-bearing claim. Test the bookkeeping.
"""
import mpmath as mp
mp.mp.dps = 40

def poch(a,k):
    r=mp.mpf(1)
    for i in range(int(k)): r*=(a+i)
    return r

def moments_scaled(D, scale, N=4000):
    """central moments of the measure with spectral positions s_n = scale*n (dilated)."""
    D=mp.mpf(D); sc=mp.mpf(scale)
    a=[1/(mp.factorial(n)*poch(2*D,n)) for n in range(N)]
    Z=mp.fsum(a)
    s=[sc*n for n in range(N)]
    m1=mp.fsum(a[n]*s[n] for n in range(N))/Z
    j2=mp.fsum(a[n]*(s[n]-m1)**2 for n in range(N))/Z
    j3=mp.fsum(a[n]*(s[n]-m1)**3 for n in range(N))/Z
    return j2,j3

print("=== Explicit dilation test: scale the spectral axis s_n -> scale * n ===")
D=mp.mpf(2)
base=None
print(f"{'scale':>8} {'j2':>16} {'j3':>16} {'4j3/j2^2':>16} {'ratio/base':>14}")
for sc in [mp.mpf('1'), mp.mpf('2'), mp.mpf('5'), mp.mpf('0.5')]:
    j2,j3=moments_scaled(D,sc)
    R=4*j3/j2**2
    if base is None: base=R; basesc=sc
    # predicted weight w: R(sc)/R(1) = (sc/1)^w  -> w = log(R/base)/log(sc/basesc)
    if sc!=basesc:
        w=mp.log(R/base)/mp.log(sc/basesc)
    else:
        w=mp.mpf('nan')
    print(f"{mp.nstr(sc,4):>8} {mp.nstr(j2,8):>16} {mp.nstr(j3,8):>16} {mp.nstr(R,10):>16} {mp.nstr(R/base,8):>14}  weight={mp.nstr(w,6)}")
print("Expected: j2 scales as sc^2, j3 as sc^3, R=4j3/j2^2 as sc^(3-4)=sc^-1 (weight -1).")
print()
print("So R is NOT dimensionless: it carries [s]^-1. A pure dilation rescales it freely")
print("(only scale-fixed points 0 and infinity). CONFIRMS route's weight -1.")
print()
print("=== The load-bearing follow-up: is the edge target G_sat co-dilating? ===")
print("agentRR edge eq: G_sat = 4 j3/j2^2. Dimensionally G_sat must also be [s]^-1 (consistent).")
print("If G_sat ALSO scaled as e^-a under the SAME boost, the equation would be scale-COVARIANT")
print("and the dilation could not break a match. The route's escape (H1): G_sat is set by c_chi")
print("(sonic-edge dispersion geometry), which has NO scale-tie to H/the dS boost (agentRR CHECK5).")
print("=> under the dS modular boost the spectral axis s (= omega^2 detuning, H-set) dilates but")
print("   G_sat (c_chi-set) does NOT -> equation NOT covariant -> dilation genuinely breaks match.")
print("THIS IS THE CRUX OF 'permits not forces' AND IT HINGES ENTIRELY ON c_chi<->H decoupling.")
print("-> verify that decoupling claim against agentRR (part 3).")
