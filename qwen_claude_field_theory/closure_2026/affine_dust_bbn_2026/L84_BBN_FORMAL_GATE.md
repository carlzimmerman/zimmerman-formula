# L84: a kernel-checked closure of the affine dust loophole

The latest affine `F(Q)Theta` FLRW elimination has one conserved charge (C)
and the exact density split

\[
  \rho=\cdots-\frac{2M^2AC}{3f^2}a^{-3}
          -\frac{M^2C^2}{3f^2}a^{-6}.
\]

Taking absolute values when comparing positive density budgets gives

\[
  \frac{\Omega_{\rm stiff,0}}{\Omega_{\rm dust,0}}
    =\frac{r}{2},\qquad r=|C|/|A|.
\]

The executable gate uses exact rational inputs

\[
  \Omega_{\rm dust,0}=33/125,
  \qquad \Omega_{\rm stiff,0}\le 42/10^{26},
\]

corresponding to the fiducial L84 (ΔN_{eff}=0.5), (T_{BBN}=1\,\mathrm{MeV})
bound. It derives

\[
  r\le \frac{7}{2.2\times10^{24}}
     =3.1818\times10^{-24}.
\]

Writing (r=q/10^{24}), the pure Lean companion proves, with no `sorry` and
no Mathlib dependency:

* BBN safety implies (q\le3);
* (q=3) is still safe for this fiducial bound;
* (q=4) is not safe;
* the natural (r=1) branch ((q=10^{24})) is impossible.

This is a route-specific result. It does **not** prove a universal MOND
no-go, and it does not close the nonlocal clock construction. It does remove
the tempting claim that the affine conserved charge can naturally be all of
dark matter without an extreme (10^{-24})-level hierarchy.

The Lean file follows the useful Navier--Stokes formalization discipline:
small explicit definitions, a declared theorem boundary, zero `sorry`, and a
recorded compiler result. The theorem is intentionally kept in Lean core so
its successful check is not obscured by a large Mathlib cache.

