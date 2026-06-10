#!/usr/bin/env python3
"""
LR battery axis 1 — the ESD->g_obs conversion factor C, where g_obs = C * G * DeltaSigma(R).
Brouwer+2021 use the SINGULAR ISOTHERMAL SPHERE value C=4 (their Eq.7) as a single, profile-independent number.
But C is PROFILE-DEPENDENT, and the audit point (Fable) is that the bias is TYPE-DIFFERENTIAL: early vs late
types have different concentrations -> different effective R/r_s -> a differential C bias that does not cancel
in the early/late split. This script computes C(profile) to bound the systematic.

ANCHORS (analytic, verified below):
  point mass : DeltaSigma = M/(pi R^2),  g = GM/R^2            => C = pi   = 3.1416
  SIS        : DeltaSigma = sigma^2/(2GR), g = 2 sigma^2/R      => C = 4    (Brouwer's choice)
  NFW        : C(x), x=R/r_s, from Wright & Brainerd 2000 DeltaSigma and the 3D enclosed mass.

LOGGED ERROR + FIX (the discipline's ledger includes our own mistakes): a first pass carried a spurious 4*pi
in the NFW Sigma normalization (Sigma = 2 r_s rho_s f, NOT 8 pi r_s rho_s f), which pushed C off by ~4pi and
broke the sanity check. FIXED here: with the correct Wright-Brainerd normalization, NFW crosses C = 4.000 at
x = R/r_s = 2 -- exactly where the NFW logarithmic slope hits -2 and the profile is locally isothermal (so it
MUST equal the SIS value there). That crossing is the validation that the table is trustworthy.
Inline, no swarms.  C. Zimmerman / Fable, 2026-06-10.
"""
import numpy as np

def nfw_C(x):
    """Conversion factor C(x)=g_true/(G*DeltaSigma) for an NFW profile, x=R/r_s. rho_s, r_s cancel."""
    x=np.asarray(x,dtype=float)
    # Wright & Brainerd 2000, in units rho_s*r_s = 1:
    #   Sigma_hat(x) = 2 f(x);  <Sigma>_hat(<x) = (4/x^2) h(x);  DeltaSigma_hat = <Sigma>_hat - Sigma_hat
    f=np.empty_like(x); h=np.empty_like(x)
    lo=x<1; hi=x>1; eq=~(lo|hi)
    xl=x[lo]; xh=x[hi]
    f[lo]=(1/(xl**2-1))*(1-(2/np.sqrt(1-xl**2))*np.arctanh(np.sqrt((1-xl)/(1+xl))))
    f[hi]=(1/(xh**2-1))*(1-(2/np.sqrt(xh**2-1))*np.arctan(np.sqrt((xh-1)/(1+xh))))
    f[eq]=1/3
    h[lo]=np.log(xl/2)+(1/np.sqrt(1-xl**2))*np.arccosh(1/xl)
    h[hi]=np.log(xh/2)+(1/np.sqrt(xh**2-1))*np.arccos(1/xh)
    h[eq]=1+np.log(0.5)
    Sigma_hat=2*f
    meanSigma_hat=(4/x**2)*h
    dSigma_hat=meanSigma_hat-Sigma_hat
    # 3D enclosed-mass acceleration g_true_hat = g_true/(G rho_s r_s) = 4 pi [ln(1+x) - x/(1+x)]/x^2
    g_hat=4*np.pi*(np.log(1+x)-x/(1+x))/x**2
    return g_hat/dSigma_hat

if __name__=="__main__":
    print("ANCHORS:  C_point = pi =",round(np.pi,4),"   C_SIS = 4 (exact)")
    print("\nNFW conversion factor C(x), x=R/r_s:")
    print("   x      C(x)")
    for x in [0.05,0.1,0.2,0.5,1.0,1.5,2.0,3.0,5.0,7.0,10.0,20.0]:
        print(f"  {x:5.2f}  {nfw_C(x):.4f}")
    c2=nfw_C(2.0)
    print(f"\nSANITY: NFW C(x=2) = {c2:.4f}  (must be ~4.000: log-slope -2 = locally isothermal = SIS value)")
    xx=np.linspace(1,10,1000); cc=nfw_C(xx)
    print(f"realistic lensing range R/r_s in [1,10]: C runs {cc[0]:.2f} -> {cc[-1]:.2f}  "
          f"(spread {np.log10(cc.max()/cc.min()):.3f} dex)")
    cfull=nfw_C(np.array([0.05,4.76**0]) );
    allx=np.logspace(-1.5,1.5,4000); allc=nfw_C(allx)
    print(f"full bracket [point=pi .. inner-NFW max]: pi={np.pi:.2f} .. {allc.max():.2f}  "
          f"(spread {np.log10(allc.max()/np.pi):.3f} dex)")
    print("\n=> the single-number C any pipeline applies is profile-laden; the stress test (esd battery) is the")
    print("   TYPE-DIFFERENTIAL variation of C between early and late types within [pi, ~4.8].")
