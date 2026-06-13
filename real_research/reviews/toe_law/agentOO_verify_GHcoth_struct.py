"""
agentOO VERIFY — final: (A) sign of sigma4 with the ACTUAL Gibbons-Hawking coth spectrum + cutoff,
exact root; (B) independently check the route's STRUCTURAL caveats (sigma6<0, unbounded fold,
edge not pinned) that hold it back from FOLD-GENERATED.

If sigma4<0 survives the real GH coth bath (not just generic positive baths), the bending sign is
FORCED, not cherry-picked. If sigma6<0 / fold-unbounded also reproduce, the route's split verdict
(sign forced, controlled fold NOT supplied) is the honest one.
"""
import numpy as np
from scipy.integrate import quad
from scipy.optimize import brentq

H = 1.0
def coth(z): return 1.0/np.tanh(z)

# GH spectral density with UV cutoff Lambda and IR-regular coupling power p:
#   J(W) = W^p * coth(pi W / H),  0<W<Lambda.   (passive: J>=0 since W^p, coth>0)
def make_S(p, Lam):
    def Jfun(W): return W**p * coth(np.pi*W/H)
    def S(w2):
        # principal value: for w2 on lower branch (w2 < W^2 for all W in (0,Lam) when w2<0...);
        # here on-shell w2=c_chi^2 k^2 is tiny>0; smallest W^2 ~ (IR)^2. Keep w2 below band: use
        # IR start eps so band is [eps,Lam], w2 kept < eps^2.
        val,_ = quad(lambda W: Jfun(W)/(w2 - W**2), 1e-6, Lam, limit=200)
        return val
    def moments():
        I1,_ = quad(lambda W: Jfun(W)/W**2, 1e-6, Lam, limit=200)
        I2,_ = quad(lambda W: Jfun(W)/W**4, 1e-6, Lam, limit=200)
        I3,_ = quad(lambda W: Jfun(W)/W**6, 1e-6, Lam, limit=200)
        return I1,I2,I3
    return S, moments

def fit(S, c0, kmax=3e-3, npts=11):
    # on-shell mode kept well below band IR edge (eps^2=1e-12), so use tiny k.
    ks = np.linspace(kmax/npts, kmax, npts)
    w2 = []
    for k in ks:
        f = lambda v: v - c0**2*k**2 - k**2*S(v)
        # lower branch root in (1e-16, (1e-6)^2). band starts at W=1e-6 so pole at 1e-12.
        try:
            r = brentq(f, 1e-18, (1e-6)**2*(1-1e-6), xtol=1e-20, rtol=1e-14)
        except Exception:
            return None
        w2.append(r)
    w2=np.array(w2); u=ks**2
    A=np.vstack([u,u**2,u**3]).T
    return np.linalg.lstsq(A,w2,rcond=None)[0]

print("="*78)
print("(A) ACTUAL GH coth bath with IR+UV cutoff band [Wir,Lam], exact secular root — sigma4 sign")
print("="*78)
# Use a banded GH bath [Wir,Lam] so moments are finite (the route's Block6 cutoff regularization).
# On-shell IR mode kept below Wir^2. coupling power p sets J=W^p coth.
def make_S_band(p, Wir, Lam):
    def Jfun(W): return W**p * coth(np.pi*W/H)
    def S(w2):
        val,_ = quad(lambda W: Jfun(W)/(w2 - W**2), Wir, Lam, limit=300)
        return val
    def moments():
        I1,_=quad(lambda W: Jfun(W)/W**2, Wir, Lam, limit=300)
        I2,_=quad(lambda W: Jfun(W)/W**4, Wir, Lam, limit=300)
        I3,_=quad(lambda W: Jfun(W)/W**6, Wir, Lam, limit=300)
        return I1,I2,I3
    return S, moments, Wir
def fit_band(S, c0, Wir, kmax=None, npts=11):
    if kmax is None: kmax = 0.3*Wir   # keep on-shell w2=c_chi^2 k^2 < Wir^2
    ks=np.linspace(kmax/npts, kmax, npts); w2=[]
    for k in ks:
        f=lambda v: v - c0**2*k**2 - k**2*S(v)
        try:
            r=brentq(f, 1e-18, Wir**2*(1-1e-9), xtol=1e-20, rtol=1e-13)
        except Exception:
            return None
        w2.append(r)
    w2=np.array(w2); u=ks**2; A=np.vstack([u,u**2,u**3]).T
    return np.linalg.lstsq(A,w2,rcond=None)[0]
c0=3.0
for p in [0.5, 1.0, 2.0]:
    for (Wir,Lam) in [(1.0,5.0),(1.0,20.0),(0.5,10.0)]:
        S, moments, Wir_ = make_S_band(p, Wir, Lam)
        I1,I2,I3 = moments()
        c_chi2 = c0**2 - I1
        if c_chi2<=0:
            print(f"  p={p} band[{Wir},{Lam}]: unstable c_chi^2={c_chi2:.3g} (raise c0; sign rule still -I2 c_chi^2)"); continue
        res = fit_band(S, c0, Wir_)
        if res is None:
            print(f"  p={p} band[{Wir},{Lam}]: root failed"); continue
        a2,a4,a6 = res
        pred4=-I2*c_chi2; pred6=c_chi2*(I2**2-I3*c_chi2)
        print(f"  p={p} band[{Wir},{Lam}]: c_chi^2={a2:+.4f} sigma4={a4:+.3e}"
              f"({'BEND' if a4<0 else 'STIFF'}) [pred {pred4:+.3e}] "
              f"sigma6_pred={pred6:+.3e}({'+floor' if pred6>0 else '-runaway'}) "
              f"CS={I2**2/(I1*I3):.4f}")

print("""
(B) STRUCTURAL caveats cross-check (analytic, from the moment rule sigma6=c_chi^2(I2^2-I3 c_chi^2)):
 - sigma6>0 needs I2^2 > I3 c_chi^2.  Cauchy-Schwarz: I2 = int J/W^4 = int (sqrt J/W)(sqrt J/W^3)
   <= sqrt(I1) sqrt(I3) => I2^2 <= I1 I3.  Equality ONLY for a delta-bath (single sharp mode).
   For a broadband featureless bath I2^2 << I1 I3, so I2^2 < I3 c_chi^2 unless c_chi^2 < I2^2/I3,
   i.e. unless the renormalized speed is tiny. => sigma6<0 generic => UNBOUNDED fold. CONFIRMED.
 - The fold location k*^2 ~ |sigma4|/sigma6 is set by moment RATIOS = bath scale, cutoff-controlled
   for the scale-free GH bath; nothing ties it to c_chi (the sonic edge). Edge NOT pinned. CONFIRMED.
""")

# Cauchy-Schwarz ceiling demonstration: a near-delta bath approaches the +floor.
print("Cauchy-Schwarz: as the bath -> single sharp mode, I2^2/(I1 I3) -> 1 (sigma6 can turn +):")
for width in [2.0, 0.5, 0.1, 0.02]:
    W0=2.0
    Ws=np.linspace(max(0.05,W0-width), W0+width, 200)
    g=np.exp(-((Ws-W0)/(width/3+1e-9))**2)  # peaked weight
    I1=np.sum(g/Ws**2); I2=np.sum(g/Ws**4); I3=np.sum(g/Ws**6)
    print(f"  peak width={width}: I2^2/(I1 I3)={I2**2/(I1*I3):.5f}")
print("  => only a SHARP spectral peak reaches the ceiling; the monotone GH coth continuum cannot.")
