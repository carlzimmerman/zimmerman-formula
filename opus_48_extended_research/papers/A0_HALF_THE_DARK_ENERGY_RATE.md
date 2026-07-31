# The MOND acceleration scale as half the dark-energy gravitational rate

**Carl P. Zimmerman**
Briar Creek Tech

---

## Abstract

The acceleration scale $a_0 \simeq 1.2\times10^{-10}\,\mathrm{m\,s^{-2}}$ that organises galactic
dynamics is numerically close to $cH_0$, a coincidence noted since Milgrom (1983). We record an exact
closed form for that scale in terms of the dark-energy density alone,
$$a_0 = \tfrac{1}{2}\,c\sqrt{G\rho_\Lambda},$$
i.e. one half of $c$ times the gravitational rate $\sqrt{G\rho_\Lambda}$ of the dark-energy density.
With the Planck 2018 $\rho_\Lambda$ this evaluates to $9.43\times10^{-11}\,\mathrm{m\,s^{-2}}$, within
0.7% of the value $9.36\times10^{-11}\,\mathrm{m\,s^{-2}}$ obtained by fitting 175 SPARC rotation curves
with the interpolation used here. The expression contains no free parameter beyond the coefficient
$\kappa = 1/2$ itself, and it is algebraically identical to $cH_\Lambda/\sqrt{32\pi/3}$ — every factor of
$\pi$ cancels in the reduction, so the apparent geometric structure $32\pi/3$ carries no content and is
merely the conversion between $H_\Lambda$ and $\sqrt{G\rho_\Lambda}$ bookkeeping.

**We are explicit about the limits of the claim.** The coefficient $\kappa = 1/2$ is *fitted*, not
derived, and we summarise our own no-go argument for why it is not forced. The interpolating function used
is identical to Milgrom (1999), Eq. (9); that paper also *derives* $a_0 = 2cH_\Lambda$ from a de
Sitter–Unruh argument, which is $2\sqrt{32\pi/3} = 11.58$ times larger than the value in use here. And the
present coefficient is **not numerically distinguishable** from Milgrom's (2020) empirical $cH_\Lambda/2\pi$:
$\sqrt{32\pi/3} = 5.789$ against $2\pi = 6.283$ differ by 7.9%, or 0.036 dex, far inside the 0.112 dex
scatter of the fit. The claim advanced here is therefore one of **form** — an exact, parameter-free
expression in $\rho_\Lambda$ with coefficient $1/2$ — and explicitly *not* one of improved fit.

---

## 1. What is claimed, and what is not

Let $\rho_\Lambda \equiv \Lambda c^2/8\pi G$ be the dark-energy mass density and
$\sqrt{G\rho_\Lambda}$ the associated gravitational rate (dimensions of inverse time; the quantity whose
reciprocal sets the dynamical time of a region of density $\rho_\Lambda$). The observation is:

$$\boxed{\;a_0 = \tfrac{1}{2}\,c\sqrt{G\rho_\Lambda}\;}\tag{1}$$

**Claimed.** (i) Eq. (1) is an exact closed form containing no free parameter other than the numerical
coefficient $1/2$. (ii) It is algebraically identical to $a_0 = cH_\Lambda/Z$ with $Z=\sqrt{32\pi/3}$, and
the reduction cancels every $\pi$ — so $32\pi/3$ is *not* an independent geometric structure and should not
be presented as one. (iii) It evaluates to $9.43\times10^{-11}\,\mathrm{m\,s^{-2}}$ on Planck 2018 inputs,
0.7% from the fitted value.

**Not claimed.** (a) That $\kappa = 1/2$ is derived — §5 gives our own argument that it is not forced.
(b) That Eq. (1) fits data better than existing proposals — §3 shows it cannot be distinguished from
Milgrom (2020) at present precision. (c) That the interpolating function is new — it is not (§3).
(d) Any claim about particle physics, the Standard Model, or a unified theory. The author has publicly
withdrawn earlier statements of that kind and does not restate them here.

---

## 2. The identity

With $\rho_\Lambda = \Lambda c^2/8\pi G$, the de Sitter rate is
$H_\Lambda = c\sqrt{\Lambda/3} = \sqrt{8\pi G\rho_\Lambda/3}$. Hence

$$\frac{cH_\Lambda}{\sqrt{32\pi/3}}
= c\sqrt{\frac{8\pi G\rho_\Lambda}{3}}\cdot\sqrt{\frac{3}{32\pi}}
= c\sqrt{\frac{8\pi G\rho_\Lambda}{32\pi}}
= c\sqrt{\frac{G\rho_\Lambda}{4}}
= \tfrac{1}{2}c\sqrt{G\rho_\Lambda}.\tag{2}$$

The cancellation is complete: the $8\pi$ against the $32\pi$, the $3$ against the $3$. Two consequences
follow and both matter for how the result should be read.

First, **$Z = \sqrt{32\pi/3} = 5.78881$ carries no geometric content.** It is the numerical factor
relating $H_\Lambda$ to $\sqrt{G\rho_\Lambda}$, nothing more. Any interpretation that treats $32\pi/3$ as
a structure to be explained — a solid angle, a horizon count, a degree-of-freedom tally — is reading
significance into a unit conversion. We state this plainly because it is an easy error and one the author
has previously made.

Second, **the entire content of Eq. (1) is the single number $\kappa = 1/2$.** Everything else is
definitional. This is a one-parameter statement, and §5 concerns whether that parameter can be fixed.

---

## 3. Prior art, stated first rather than last

This section is placed before the numbers deliberately. The following results are *not* ours.

**Milgrom (1983)** introduced $a_0$ and noted its proximity to $cH_0$.

**Milgrom (1999)**, Phys. Lett. A **253**, 273, is the closest prior work and must be credited on two
counts. (i) The interpolating function used throughout the present programme,
$\nu(y) = \sqrt{1+1/y}$ — equivalently the closure $g_{\rm obs}^2 = g_{\rm bar}^2 + a_0 g_{\rm bar}$ — is
**identical to his Eq. (9)**. It is not a variant and it is not new. (ii) That paper *derives* a value of
the scale from a de Sitter–Unruh vacuum argument, obtaining $a_0 = 2cH_\Lambda$. Relative to Eq. (1) that
is a factor $2Z = 11.58$ larger. So the de Sitter–Unruh route does not leave the coefficient open: it
predicts one, and the prediction misses the measured scale by an order of magnitude. **Our contribution is
a renormalisation of his coefficient to match data, not a new derivation.**

**Pikhitsa (2010)** and **Klinkhamer & Kopp (2011)** independently obtain $2cH$-type coefficients.

**Milgrom (2020)** gives the empirical $a_0 = cH_\Lambda/2\pi$. This is the sharpest comparison and it
limits our claim severely: $2\pi = 6.28319$ against $Z = 5.78881$ is a **7.9% difference, i.e. 0.036 dex**.
In the deep-field regime $g_{\rm obs} = \sqrt{g_{\rm bar}a_0}$ a shift in $a_0$ enters $g_{\rm obs}$ at
half that, 0.018 dex, against a fitted radial-acceleration-relation scatter of 0.112 dex (§4). **The two
coefficients are observationally indistinguishable.** We therefore do not claim a better fit. What
distinguishes Eq. (1) is that it is a closed form in $\rho_\Lambda$ with a rational coefficient, where
$cH_\Lambda/2\pi$ is an empirical divisor.

**Milgrom (1994)**, Ann. Phys. **229**, 384, is the foundational modified-inertia paper: it establishes
that modified inertia requires a definition of absolute acceleration, that such theories are generically
nonlocal, and that their effective interpolating function depends on orbit shape. **Milgrom (2022)**,
Phys. Rev. D **106**, 064060, writes modified inertia in Fourier space and states that the algebraic
relation $g\,\mu(g/a_0) = g_N$ holds only for single-frequency (circular) trajectories. Both results were
independently re-derived in the course of the present programme and are **not** claimed here.

---

## 4. Numerical evaluation

Planck 2018 (TT,TE,EE+lowE+lensing+BAO): $H_0 = 67.66\,\mathrm{km\,s^{-1}Mpc^{-1}}$,
$\Omega_\Lambda = 0.6889$, giving $\rho_\Lambda = 5.927\times10^{-27}\,\mathrm{kg\,m^{-3}}$ and

$$a_0 = \tfrac12 c\sqrt{G\rho_\Lambda} = 9.43\times10^{-11}\ \mathrm{m\,s^{-2}}.$$

Fitting the closure $g_{\rm obs}^2 = g_{\rm bar}^2 + a_0g_{\rm bar}$ to 175 SPARC galaxies with a single
global stellar mass-to-light ratio $\Upsilon_{[3.6]} = 0.70$ returns
$a_0 = 9.36\times10^{-11}\,\mathrm{m\,s^{-2}}$ with 0.112 dex residual scatter. The agreement between the
Planck-derived and fitted values is 0.7%.

**A second density choice must be reported.** Using the *total* density with $cH_0$ in place of the
pure-$\Lambda$ combination gives $a_0 = 1.13\times10^{-10}\,\mathrm{m\,s^{-2}}$. This is a genuine fork —
the two footings differ by 21% — and it is not resolved by the fit. Every dimensional quantity in the
programme is carried both ways. Eq. (1) is the pure-$\Lambda$ branch, and §6 gives the observable that
distinguishes them.

---

## 5. Why $\kappa = 1/2$ is not derived

We regard this as the central open problem and state it as such rather than obscuring it.

An attempt to force $\kappa$ from first principles was made and failed. Requiring the coefficient to
follow from ghost-freedom, unitarity, and a holographic degree-of-freedom count does not select $1/2$: the
constructions that reproduce the correct interpolating form leave the overall normalisation free, and the
one geometric candidate that appeared to fix it, $(3/8\pi)^{1/4} = 0.5878$, turns out to be the
$g_* = 1$ limit of a count with no independent microscopic justification. We therefore report Eq. (1) as a
**one-parameter empirical relation**, not a derivation, and we do not claim the value of $a_0$ has been
explained. Anyone reading Eq. (1) as a prediction of $a_0$ from $\Lambda$ is reading it wrongly: it is a
prediction of the *scaling* $a_0 \propto \sqrt{\rho_\Lambda}$ with an unexplained coefficient.

---

## 6. A falsifiable consequence

The two footings of §4 make different predictions for redshift evolution, and this is the cleanest way to
test Eq. (1) rather than merely admire it. If $a_0 \propto \sqrt{\rho_\Lambda}$ with $\rho_\Lambda$ the
dark-energy density, then for a general equation of state $w(z) = w_0 + w_a z/(1+z)$,

$$\frac{a_0(z)}{a_0(0)} = (1+z)^{\frac{3}{2}(1+w_0+w_a)}\exp\!\left(-\frac{3w_az}{2(1+z)}\right).\tag{3}$$

For $w_0 = -1$, $w_a = 0$ this is exactly constant. For the DESI-preferred $w_0 > -1$, $w_a < 0$ it rises
to a maximum and then declines — *not* a monotonic rise. The competing footing, $a_0 \propto cH(z)$,
rises monotonically. These are distinguishable in principle by measurements of the acceleration scale at
$z \gtrsim 1$.

We note honestly that current measurements do not settle this. A recent determination reports a *rising*
$a_0$ with redshift, which is in tension with the constant/bump-then-decline behaviour of Eq. (3) on the
pure-$\Lambda$ branch, although that measurement is itself degenerate with $\Lambda$CDM assumptions in the
mass modelling. We record it as a live tension, not as support.

---

## 7. Known liabilities

Presented so a referee does not have to find them.

1. **Galaxy clusters.** The same closure applied to cluster-scale systems underpredicts the required
   acceleration. On raw eRASS1 masses the discrepancy factor at $R_{500}$ is 2.33 (median), and the
   cluster-scale acceleration inferred from lensing is $2.02\times10^{-9}\,\mathrm{m\,s^{-2}}$ — a factor
   21.6 above Eq. (1). A weak-lensing mass recalibration softens this to roughly 1.6–1.8 but does not
   remove it. The lower value of $a_0$ in Eq. (1) makes this discrepancy 13% *worse* than it is for the
   standard coefficient. This is unresolved and is shared with relativistic MOND theories generally.
2. **Solar system.** The closure of §4, applied exactly, forces a constant sunward anomaly $a_0/2$ that
   exceeds the Earth/Mars ranging bound by three orders of magnitude. This is a property of the specific
   $\alpha=1$ interpolation, not of Eq. (1); interpolations with a faster approach to Newtonian behaviour
   (e.g. $\mu(x) = x/\sqrt{1+x^2}$) reduce the anomaly by five orders of magnitude at a cost of
   0.003 dex in the SPARC fit. The word *exact* should not be attached to the $\alpha=1$ closure.
3. **The scale is degenerate with the interpolation.** As §3 shows, the fitted $a_0$ and the choice of
   interpolating function trade off; the radial acceleration relation constrains the combination, not
   $a_0$ alone. No claim here should be read as a measurement of $a_0$ to better than the 7.9% that
   separates Eq. (1) from $cH_\Lambda/2\pi$.

---

## 8. Reproducibility and disclosure

All numerical claims above are produced by committed, runnable scripts that exit non-zero on internal
check failure; see the repository accompanying this note. In particular the identity of Eq. (2), the SPARC
fit of §4, the evolution law of Eq. (3), and the cluster factors of §7 each have a corresponding script.

**AI-assistance disclosure.** Portions of the analysis, numerical verification, and drafting of this note
were carried out with the assistance of a large language model (Anthropic Claude). The author directed the
work, specified and reviewed every load-bearing calculation, and takes full responsibility for the
content, including all errors. No AI system is an author. Several intermediate claims generated during the
work were subsequently found to be wrong and were withdrawn before this draft; the surviving claims are
those that passed independent adversarial re-derivation.

---

## References

1. M. Milgrom, *Astrophys. J.* **270**, 365 (1983).
2. M. Milgrom, *Ann. Phys.* **229**, 384 (1994).
3. M. Milgrom, *Phys. Lett. A* **253**, 273 (1999).
4. P. V. Pikhitsa, arXiv:1010.0318 (2010).
5. F. R. Klinkhamer and M. Kopp, arXiv:1104.2022 (2011).
6. M. Milgrom, *Phys. Rev. D* **102**, 084010 (2020).
7. M. Milgrom, *Phys. Rev. D* **106**, 064060 (2022).
8. Planck Collaboration, *Astron. Astrophys.* **641**, A6 (2020).
9. F. Lelli, S. S. McGaugh, J. M. Schombert, *Astron. J.* **152**, 157 (2016) — SPARC.
10. S. S. McGaugh, F. Lelli, J. M. Schombert, *Phys. Rev. Lett.* **117**, 201101 (2016).

*(Reference details to be verified against the published records before submission; items 4–7 in
particular should be checked for volume and page numbers.)*
