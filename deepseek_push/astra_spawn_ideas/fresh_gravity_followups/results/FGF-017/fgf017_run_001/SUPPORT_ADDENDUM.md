# Registered M whole-support addendum

This supplementary control closes the domain condition left by knot-only root
checks. It evaluates no further roots. Each original positive mass profile is
piecewise a power law. For a central-minus-error curve c-e on its original
common grid, e/c is a power law on every cell. Thus c-e >= min(c)*(1-max(e/c))
throughout its support. Central masses are bounded by their endpoint extrema;
stellar endpoint choices are likewise bounded. The global minimum/maximum of
C follows from the shared radius endpoints.

Use amin=9.3619e-11 and amax=1.05*1.1279e-10; both pinned z<.08 give E(z)<1.05.
The resulting lower stellar y=C*S/a exceeds 1e-12 and its upper bound is below
1e12. Hence at eta=0 the force already lies in M's registered interval and
eta F/(C H)=0. At its upper boundary B=a*1e12,

    eta_top=(a*1e12/C-S)/X,
    h(eta_top) >= [(amin*1e12/Cmax-Smax)/Xmax]
                  *amin*1e12/(Cmax*Hmax).

Both brackets are positive and the h lower bound exceeds 1 by >1e18 for both
objects. Strict monotonicity therefore supplies a unique M root within its
registered interval at every admissible radius, for all 24 choices per object.
The numerical bounds in support_control.json are binary64 with large margins,
not a directed-rounding certificate. No extra observational assumption is used.
