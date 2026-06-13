"""
agentOO VERIFY — CHERRY-PICK TEST: try the OTHER admissible couplings/regularizations.

Referee question (2)+(3): was sigma4<0 cherry-picked? Did the route pick a coupling/cutoff
PRE-SHAPED to bend? I steelman BOTH the fold and the kill by scanning the admissible coupling
space and reading sigma4's sign in each. If the sign FLIPS with admissible choices, the honest
verdict is FOLD-POSSIBLE-COUPLING-DEPENDENT, not FOLD-GENERATED.

ADMISSIBLE = (a) passive bath J(W)>=0 [X2 vacuum passivity, non-negotiable], (b) a local Lorentz/
shift-covariant coupling of the khronon to the horizon DOF. Within that, the FREE choices are:
  (C1) coupling derivative structure: how many gradients/time-derivatives hit chi at the vertex.
       This sets the k- and omega-power prefactor of Pi.
  (C2) whether the khronon mode sits BELOW or ABOVE (part of) the bath band.
  (C3) the spectral shape J(W) (tested separately in blocks 4/5; here I test the COUPLING).

I solve the EXACT secular root for each and read sigma4. No series.
"""
import numpy as np
from scipy.optimize import brentq

def secular_root_general(Spi, c0, k, w2max):
    # G^{-1}=0:  w2 - c0^2 k^2 - Pi(w2,k) = 0, Pi given as callable of (w2,k).
    f = lambda w2: w2 - c0**2*k**2 - Spi(w2, k)
    lo, hi = 1e-14, w2max*(1-1e-9)
    flo, fhi = f(lo), f(hi)
    if flo*fhi > 0:
        return None
    return brentq(f, lo, hi, xtol=1e-16, rtol=1e-15)

def sigma4_of(Spi, c0, w2max, kmax=1e-3, npts=9):
    ks = np.linspace(kmax/npts, kmax, npts)
    w2 = []
    for k in ks:
        r = secular_root_general(Spi, c0, k, w2max)
        if r is None: return None, None
        w2.append(r)
    w2 = np.array(w2); u = ks**2
    A = np.vstack([u, u**2, u**3]).T
    a2,a4,a6 = np.linalg.lstsq(A, w2, rcond=None)[0]
    return a2, a4

# Fixed passive bath (discrete, positive weights), modes all in [1,4].
Ws  = np.linspace(1.0, 4.0, 30)
g2s = 0.01/Ws**1.2     # arbitrary positive weights, J>=0
def Sbase(w2): return np.sum(g2s/(w2 - Ws**2))
w2max = Ws.min()**2
c0 = 1.6

print("="*78)
print("COUPLING SCAN — sigma4 sign across admissible vertex derivative structures")
print("="*78)
print(f"(bath modes in [{Ws.min()},{Ws.max()}], c0={c0}; on-shell mode is IR, w2->0 < W^2 band)\n")

# (C1) Vertex derivative structures. Pi(w2,k) generically = P(w2,k) * Sbath(w2), where the
# prefactor P is set by how the vertex derivatives act. Lorentz/shift covariant admissible forms:
couplings = {
    "deriv/momentum coupling  Pi=k^2 S(w2)         [route's choice]": lambda w2,k: k**2*Sbase(w2),
    "time-derivative coupling Pi=w2 S(w2)/c0^2 *k^2": lambda w2,k: (w2/c0**2)*k**2*Sbase(w2),
    "mixed     Pi=(k^2 + w2/c0^2) S(w2)            ": lambda w2,k: (k**2 + w2/c0**2)*Sbase(w2),
    "scalar (no-deriv) coupling Pi = mu^2 S(w2)    ": lambda w2,k: 0.5*Sbase(w2),
    "higher-grad coupling Pi=k^4 S(w2)             ": lambda w2,k: k**4*Sbase(w2),
}
for name, Spi in couplings.items():
    a2,a4 = sigma4_of(Spi, c0, w2max)
    if a4 is None:
        print(f"  {name}: no stable lower-branch root (skip)"); continue
    tag = "BEND(<0)" if a4 < 0 else ("STIFFEN(>0)" if a4>0 else "ZERO")
    print(f"  {name}: c_chi^2={a2:+.5f}  sigma4={a4:+.4e}  {tag}")

print("""
NOTE on the scalar / no-derivative coupling: Pi = const * S(w2) renormalizes omega^2 by a
k-INDEPENDENT piece + a w2-dependent piece; it does NOT produce a c^2 k^2 sound mode shift the
same way (it shifts the GAP). For a gapless khronon (shift symmetry) the vertex MUST carry
gradients => the k^2-prefactor (derivative) couplings are the shift-symmetric-admissible ones.
The scalar coupling breaks the khronon shift symmetry and is therefore NOT admissible for a
Goldstone khronon — but I include it to show the sign behaviour.
""")

print("="*78)
print("(C2) THE REAL STEELMAN: can an admissible coupling put bath weight BELOW the mode?")
print("="*78)
print("""
The bend sign sigma4=-I2 c_chi^2<0 follows whenever the WHOLE bath sits ABOVE the IR mode
(w2->0 < W^2). To FLIP to stiffen you need bath weight at W^2 < w2 = c_chi^2 k^2, i.e. modes
SOFTER than the khronon sound at the probed k. As k->0 that needs W->0 bath modes: a bath with
spectral weight extending to W=0.  The GH bath: J(W)=W^p coth(piW/H).  As W->0, coth~H/(piW) so
J ~ W^(p-1)*(H/pi): there IS IR weight down to W=0 for p<=1. Test whether IR bath weight flips
the sign of sigma4 in the exact root.
""")
# Bath WITH soft (W->0) modes: include modes from 0.05 up.
for Wlo in [1.0, 0.3, 0.05, 0.01]:
    Ws2 = np.linspace(Wlo, 4.0, 60)
    g2s2 = 0.01/Ws2**1.2
    def Sb(w2, Ws2=Ws2, g2s2=g2s2): return np.sum(g2s2/(w2 - Ws2**2))
    w2max2 = Ws2.min()**2
    Spi = lambda w2,k,Sb=Sb: k**2*Sb(w2)
    a2,a4 = sigma4_of(Spi, c0, w2max2)
    if a4 is None:
        print(f"  bath W in [{Wlo},4]: no stable lower-branch root"); continue
    tag = "BEND(<0)" if a4<0 else "STIFFEN(>0)"
    print(f"  bath W in [{Wlo},4]: c_chi^2={a2:+.5f}  sigma4={a4:+.4e}  {tag}")

print("""
The on-shell IR mode w2=c_chi^2 k^2 -> 0 as k->0 always sits BELOW any bath band with W_min>0,
so for k->0 the bend sign is forced for ANY positive bath with a gap. Even pushing W_min toward 0
keeps every finite bath mode ABOVE the k->0 mode (the secular root stays on the lower branch).
The ONLY way to stiffen is genuine bath weight AT EXACTLY W=0 (a zero-frequency mode) overlapping
the khronon — i.e. a second gapless sound mode degenerate with the khronon, not a horizon bath.
""")
