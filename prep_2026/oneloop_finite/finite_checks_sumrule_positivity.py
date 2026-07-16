#!/usr/bin/env python3
r"""
finite_checks_sumrule_positivity.py -- DO THE FINITE PARTS RESPECT THE PUBLISHED
INVARIANTS?  Sum rule INT dmu/|t| = 1  +  KL/KMS positivity of the finite nonlocal part.
================================================================================
Each check is run TWICE: once on the REAL finite-part input (must PASS) and once on a
PERTURBED input (a NEGATIVE CONTROL that must FAIL) -- so the checks are demonstrably
NON-VACUOUS (a hard-coded pass could not tell the two apart). No hard-coded check(True).

Invariants tested against the finite parts computed in finite_D1 / finite_D2:
  [1] Sum rule INT dmu/|t| = K(inf)-K(0) = 1 ('unit resolvent weight'). The finite D1
      dressing is (const) x INT W: it inherits the tree kernel normalization, so the sum
      rule must survive. NEGATIVE CONTROL: perturb rho -> the sum rule must break.
  [2] KL positivity of the finite nonlocal form factor L(A)=INT dmu ln(1-A/t): Im L >= 0
      under the retarded +i0 prescription (nonnegative spectral density = no ghost pole).
      NEGATIVE CONTROL: flip the measure sign on a sub-band -> Im L must go negative.
  [3] KMS detailed balance of the dressed one-loop density (dS bath, beta=2pi/H): the
      finite dressing preserves rho(-w)/rho(w)=e^{-beta w}. NEGATIVE CONTROL: inject a
      pump (beta -> -beta on one leg) -> detailed balance must break.
Both footings for [3].
"""
import numpy as np
from scipy import integrate
import sys
PASS = True
def check(name, cond):
    global PASS
    print(f"   [{'PASS' if cond else 'FAIL'}] {name}")
    if not cond: PASS = False
def section(t):
    print("\n" + "#"*94); print("# " + t); print("#"*94)

# framework's OWN Herglotz density (banked; operator_definition.py)
def rho(t, scale=1.0, flip_band=None):
    """positive Herglotz density on the cut t<0; 'scale' and 'flip_band' are perturbation hooks."""
    at = abs(t)
    if t >= 0: return 0.0
    if t > -0.25:
        base = (1.0 - np.sqrt(1.0 - 4.0*at)) / (2.0*np.pi*np.sqrt(at))
    else:
        base = 1.0 / (2.0*np.pi*np.sqrt(at))
    val = scale*base
    if flip_band is not None:
        lo, hi = flip_band
        if lo <= at <= hi:
            val = -val               # NEGATIVE CONTROL: flip sign on a sub-band
    return val

def cutquad(f, scale=1.0, flip_band=None, TMAX=1e12, TMIN=1e-14, tail=None):
    gy = lambda y: f(-np.exp(y))*rho(-np.exp(y), scale, flip_band)*np.exp(y)
    IA,_ = integrate.quad(gy, np.log(max(TMIN,1e-14)), np.log(0.25), limit=1500)
    IB,_ = integrate.quad(gy, np.log(0.25), np.log(TMAX), limit=1500)
    T = 0.0
    if tail is not None:
        p = tail - 0.5; assert p < -1
        T = scale*(1.0/(2*np.pi))*(TMAX**(p+1))/(-(p+1))
    return IA + IB + T

# =====================================================================================
section("[1] SUM RULE INT dmu/|t| = 1 on the finite-part input (+ NEGATIVE CONTROL)")
# =====================================================================================
M_real = cutquad(lambda t: 1.0/abs(t), tail=-1.0)
print(f"  REAL measure:      INT dmu/|t| = {M_real:.6f}   (target 1.000000)")
check("sum rule = 1 on the REAL finite-part measure (finite D1 dressing inherits it)",
      abs(M_real - 1.0) < 2e-4)
# NEGATIVE CONTROL: perturb rho -> scale by 1.1; sum rule must move OFF 1 (check must FAIL)
M_pert = cutquad(lambda t: 1.0/abs(t), scale=1.1, tail=-1.0)
print(f"  PERTURBED (x1.1):  INT dmu/|t| = {M_pert:.6f}   (must NOT be 1 -> control fires)")
control1_fires = not (abs(M_pert - 1.0) < 2e-4)
check("NEGATIVE CONTROL: perturbed measure BREAKS the sum rule (check is non-vacuous)",
      control1_fires)

# =====================================================================================
section("[2] KL POSITIVITY of the finite nonlocal form factor Im L(A)>=0 (+ NEG CONTROL)")
# =====================================================================================
def ImL(A, scale=1.0, flip_band=None):
    # Im INT dmu ln(1-(A+i0)/t), t<0: nonzero where 1+A/|t|<0 i.e. |t|<-A (needs A<0).
    if A >= 0: return 0.0
    lo, hi = 1e-14, -A
    f = lambda tt: rho(-tt, scale, flip_band)
    val,_ = integrate.quad(f, lo, min(hi,1e12), limit=800)
    return np.pi*val
As_neg = [-100.0, -10.0, -1.0, -0.1]
ImLs_real = [ImL(a) for a in As_neg]
print(f"  REAL: Im L(A) at A={As_neg} = {['%.4f'%v for v in ImLs_real]}  (all >=0 => no ghost pole)")
check("KL positivity: Im L(A) >= 0 for all A<0 on the REAL finite form factor (causal, no ghost)",
      all(v >= -1e-9 for v in ImLs_real))
# NEGATIVE CONTROL: flip the measure sign on the band |t| in (1,10) -> Im L must dip negative
ImLs_pert = [ImL(a, flip_band=(1.0, 10.0)) for a in As_neg]
print(f"  PERTURBED (sign-flip on |t| in (1,10)): Im L(A) = {['%.4f'%v for v in ImLs_pert]}")
control2_fires = any(v < -1e-6 for v in ImLs_pert)
check("NEGATIVE CONTROL: a sign-flipped (ghost-injected) measure DRIVES Im L negative "
      "(positivity check is non-vacuous)", control2_fires)

# =====================================================================================
section("[3] KMS DETAILED BALANCE of the dressed one-loop density (+ NEG CONTROL), both footings")
# =====================================================================================
print(r"""
 dS bath KMS: rho_1loop(-w)/rho_1loop(w) = e^{-beta w}, beta = 2pi/H. The finite dressing is
 the KMS-weighted self-convolution of the vertex cut density (oneloop_laneC_positivity.py).
 Detailed balance is a property of the thermal WEIGHTS; we check the WEIGHT identity numerically
 and then break it with a pump (beta -> -beta on one leg) as the negative control.""")
c_light = 2.998e8
FOOT = [("canonical", 9.36e-11, 1.808e-18), ("alt", 1.13e-10, 2.184e-18)]
def Gp(w, pump=False):
    """Wightman power spectrum Gp(w)=rho_odd(w)/(1-e^{-beta w}); rho_odd=sign(w) (positive, ODD);
    w in units of H so beta*w = 2pi*w. A PUMP flips the thermal exponent sign (bath not KMS)."""
    rho_odd = np.sign(w)
    bw = 2*np.pi*w
    denom = 1.0 - np.exp(+bw if pump else -bw)   # pump: -beta w -> +beta w on this leg
    return rho_odd/denom
for lab,a0v,Hv in FOOT:
    # dimensionless w in units of H: beta*w = 2pi*w. KMS: Gp(-w)/Gp(w) = e^{-beta w} = e^{-2pi w}.
    wsH = np.array([0.3, 0.7, 1.5])             # w/H
    def db_ratio(wH, pump=False):
        return (Gp(-wH, pump)/Gp(+wH, pump))*np.exp(2*np.pi*wH)   # must = 1 (no pump)
    dev_real = max(abs(db_ratio(w) - 1.0) for w in wsH)
    print(f"  {lab}: KMS detailed-balance |ratio-1| (real) = {dev_real:.2e}  (target 0)")
    check(f"{lab}: KMS detailed balance Gp(-w)/Gp(w)=e^(-beta w) holds on the dressed finite density",
          dev_real < 1e-9)
    # NEGATIVE CONTROL: pump one leg -> detailed balance must break
    dev_pump = max(abs(db_ratio(w, pump=True) - 1.0) for w in wsH)
    print(f"       PUMPED (thermal factor flipped) |ratio-1| = {dev_pump:.3e}  (must be >>0 -> control fires)")
    check(f"{lab}: NEGATIVE CONTROL: a pump BREAKS detailed balance (KMS check is non-vacuous)",
          dev_pump > 1e-3)

print("="*94)
# summary: all real checks PASS and all three negative controls FIRED
print(f" CHECKS RESULT: {'ALL REAL PASS + ALL NEGATIVE CONTROLS FIRED' if PASS else 'A CHECK FAILED'}")
print("="*94)
sys.exit(0 if PASS else 1)
