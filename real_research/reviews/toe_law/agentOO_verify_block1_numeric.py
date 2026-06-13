"""
agentOO VERIFY — independent numeric re-derivation of the sigma4 SIGN, no series, no convention.

The route's whole verdict hinges on resolving a Block2(stiffen)-vs-Block3(bend) sign clash.
Block 3 claims the EXACT secular root of
    omega^2 = c0^2 k^2 + k^2 * S(omega^2),   S(w2) = int dW J(W)/(w2 - W^2)
expands to omega^2 = c_chi^2 k^2 - I2 c_chi^2 k^4 + ...,  i.e. sigma4 < 0 (BEND).

I do NOT trust the analytic series alone (sign flips are exactly where conventions hide). Here I
take a CONCRETE positive bath J>=0, solve the secular equation NUMERICALLY for omega(k)^2 as an
exact root, and read sigma4 by finite differences in k^2. No Taylor convention, no kernel choice.

CRUCIAL physics point I will stress-test: the self-energy pole. S(w2)=int J/(w2-W^2) has poles at
w2=W^2. For the IR khronon mode the on-shell w2=c_chi^2 k^2 -> 0 as k->0, which is BELOW the bath
band [W_min^2, ...]. So at small k we are on the LOWER branch, w2 < W^2 for all bath modes =>
S(w2)<0 and the geometric expansion S = -(I1 + w2 I2 + ...) is the correct analytic continuation.
That is the regime Block 3 expanded in. I verify the ROOT actually tracks that branch.
"""
import numpy as np
from scipy.optimize import brentq

np.set_printoptions(precision=10)

# ---- Concrete bath: a set of discrete oscillators with positive weights g_i^2 (J>=0) ----
# Discrete bath:  S(w2) = sum_i g2_i / (w2 - W_i^2)
def make_bath(Ws, g2s):
    Ws = np.asarray(Ws, float); g2s = np.asarray(g2s, float)
    assert np.all(g2s > 0), "passive bath: weights must be > 0"
    def S(w2):
        return np.sum(g2s/(w2 - Ws**2))
    # moments I_n = sum g2_i / W_i^{2n}
    I1 = np.sum(g2s/Ws**2)
    I2 = np.sum(g2s/Ws**4)
    I3 = np.sum(g2s/Ws**6)
    return S, I1, I2, I3, Ws, g2s

def secular_root(S, c0, k, Wmin):
    # Solve f(w2) = w2 - c0^2 k^2 - k^2 S(w2) = 0 on the LOWER branch w2 in (0, Wmin^2).
    f = lambda w2: w2 - c0**2 * k**2 - k**2 * S(w2)
    lo, hi = 1e-14, (Wmin**2)*(1-1e-9)
    # f(lo) ~ -c0^2 k^2 - k^2 S(0) ; need sign change to Wmin^2 where S->-inf => f->+inf?
    # As w2->Wmin^2^-, the nearest pole g2/(w2-Wmin^2) -> -inf, so -k^2 S -> +inf => f->+inf.
    # As w2->0+, f-> -c0^2 k^2 - k^2 S(0); S(0)=sum g2/(-W^2) = -I1 <0 so -k^2 S(0)=+k^2 I1>0.
    #   f(0+) = -c0^2 k^2 + k^2 I1 = -(c0^2-I1) k^2 = -c_chi^2 k^2 < 0 (stable). Good: sign change.
    flo, fhi = f(lo), f(hi)
    if flo*fhi > 0:
        raise RuntimeError(f"no bracket: f(lo)={flo}, f(hi)={fhi}")
    return brentq(f, lo, hi, xtol=1e-16, rtol=1e-15)

def fit_dispersion(S, c0, Wmin, kmax=1e-3, npts=9):
    ks = np.linspace(kmax/npts, kmax, npts)
    w2 = np.array([secular_root(S, c0, k, Wmin) for k in ks])
    # omega^2 = a2 k^2 + a4 k^4 + a6 k^6 ; fit in variable u=k^2
    u = ks**2
    A = np.vstack([u, u**2, u**3]).T
    coef, *_ = np.linalg.lstsq(A, w2, rcond=None)
    return coef  # a2, a4, a6

print("="*78)
print("INDEPENDENT NUMERIC SIGN TEST (exact secular root, finite-difference sigma4)")
print("="*78)

cases = [
    ("single mode W=1, g2=0.1, c0=1.2", [1.0], [0.1], 1.2),
    ("single mode W=2, g2=0.5, c0=1.5", [2.0], [0.5], 1.5),
    ("three modes 1,2,3 equal weight",  [1.0,2.0,3.0], [0.1,0.1,0.1], 1.3),
    ("broadband 1..10, decaying g2",    list(np.linspace(1,10,40)),
                                        list(0.02/np.linspace(1,10,40)**1.5), 2.0),
]

for name, Ws, g2s, c0 in cases:
    S, I1, I2, I3, Wsa, g2sa = make_bath(Ws, g2s)
    Wmin = Wsa.min()
    c_chi2 = c0**2 - I1
    if c_chi2 <= 0:
        print(f"\n[{name}] SKIP: unstable (c_chi^2={c_chi2:.4g}<=0)"); continue
    a2, a4, a6 = fit_dispersion(S, c0, Wmin)
    pred_a2 = c_chi2
    pred_a4 = -I2*c_chi2
    pred_a6 = c_chi2*(I2**2 - I3*c_chi2)
    print(f"\n[{name}]")
    print(f"  c_chi^2:   fit={a2:+.8f}  Block3-pred(c0^2-I1)={pred_a2:+.8f}")
    print(f"  sigma4 :   fit={a4:+.8e}  Block3-pred(-I2 c_chi^2)={pred_a4:+.8e}   "
          f"SIGN={'BEND(<0)' if a4<0 else 'STIFFEN(>0)'}")
    print(f"  sigma6 :   fit={a6:+.8e}  Block3-pred={pred_a6:+.8e}   "
          f"SIGN={'+floor' if a6>0 else '-runaway'}")
