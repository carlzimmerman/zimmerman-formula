# A measured coefficient for the MOND acceleration scale

### κ = ½ in a₀ = κc√(Gρ_Λ): derived kernel, measured coefficient, and two theorems on why the coefficient cannot be derived

**C. P. Zimmerman**, Briar Creek Tech
Draft, 2 August 2026

---

## Abstract

The MOND acceleration scale can be written in closed form in the dark-energy density,

$$a_0 \;=\; \kappa\,c\sqrt{G\rho_\Lambda}, \qquad \kappa = \tfrac12,$$

equivalently $a_0 = c^2\sqrt{\Lambda/32\pi} = cH_\Lambda/Z$ with $Z = 2\sqrt{8\pi/3} = \sqrt{32\pi/3} = 5.78881$.
With Planck 2018 this evaluates to $9.43\times10^{-11}\,\mathrm{m\,s^{-2}}$, within 0.7% of the
$9.36\times10^{-11}$ obtained by fitting 175 SPARC rotation curves with the interpolation used here (0.108 dex
at $\Upsilon_{3.6} = 0.70$).

We report three results and fence them with two theorems.

**First, the interpolation function is derived, not chosen.** The de Sitter–Unruh temperature
$T(a)\propto\sqrt{a^2+A^2}$, with inertia tracking the excess over the ambient value, yields
$\mu(a) = [\sqrt{a^2+A^2}-A]/a$, which in units of $a_0 = 2A$ is *identically*
$(\sqrt{1+4x^2}-1)/2x$ — the interpolation of $g_{\rm obs}^2 = g_{\rm bar}^2 + g_{\rm bar}a_0$ — for **every**
ambient scale $A$, which cancels from the expression. Among power-law responses $f(T)=T^n$, deep-MOND
linearity forces $n=1$ uniquely. This is Milgrom's (1999) construction; what is new here is the
$A$-independence and the $n=1$ uniqueness, which together mean the *shape* is free and only the *scale* is at
issue.

**Second, the coefficient is measurable, and it is measured.** Profiling $a_0$ on 175 SPARC galaxies with
$\Upsilon$ free **per galaxy** — so that any global population-synthesis offset is absorbed — gives
$\sigma(a_0)/a_0 = 1.24\%$ treating points as independent and 5.44% with within-galaxy clustering, against the
8.20% logarithmic gap to Milgrom's (2020) empirical $cH_\Lambda/2\pi$. The fit gives $\Delta\chi^2 = 63.9$ for
$\kappa=\tfrac12$ against $154.3$ for $\kappa = 1/2\pi$: **the data favour $\kappa = \tfrac12$ at
$\approx 2.2\sigma$** on the conservative counting. The lever is the HI gas, which carries no mass-to-light
ratio and therefore anchors $a_0$ against any $\Upsilon$ rescaling; a mutation that lets $\Upsilon$ scale the
gas destroys the constraint by an order of magnitude.

**Third, $\kappa = \tfrac12$ is not derivable from the geometric or thermodynamic ingredients available**, and
we prove it twice. (i) $Z^2/\pi = 32/3$ is rational while $Z/\pi^k$ is irrational for every integer $k$; since
every ingredient the problem supplies is a rational multiple of an integer power of $\pi$, such ingredients can
force $Z^2$ but never $Z$. (ii) The whole content reduces to one forced dimensionless $\tfrac14$ in
$a_0^2 = \tfrac14 c^2G\rho_\Lambda$; the only forced $\tfrac14$ in gravitational physics is the
Bekenstein–Hawking quarter, which rides $S\sim\hbar^{-1}$ and survives only un-ratioed, while $a_0$ is
$\hbar$-free and the sole available canceller is a temperature — i.e. a frequency scale, returning one to the
class barred by (i). **Quadratic in $Z$, $\hbar$-free, and carrying the $\tfrac14$ are jointly unsatisfiable.**

**We are explicit that this is a measurement, not a derivation, and that the theory side points the other
way.** Seventeen attempts to force $\kappa$ have failed, at 4.1 bits of accumulated look-elsewhere. Three
independent theory arguments land on rival coefficients rather than on $\tfrac12$ — and they are one physical
input wearing three hats, not three votes. Two independent estimators pull $a_0$ 15–26% *above* the canonical
footing. And the exact form carries a solar-system liability we state in full.

---

## 1. What is claimed, and what is not

**Claimed.** (i) The interpolation function is derived, and derived independently of the acceleration scale.
(ii) The coefficient $\kappa = \tfrac12$ is observationally discriminable from its nearest published rival and
is favoured by SPARC at $\approx 2.2\sigma$. (iii) It is not derivable from the available ingredients, by two
theorems with stated scope.

**Not claimed.** We do not derive $a_0$. We claim no novelty for the interpolation function, for the de
Sitter–Unruh construction, or for $a_0 = 2cH_\Lambda$ — all three are Milgrom's, and §7 records two further
independent owners of the kernel. We do not claim an improved fit to anything. And we make no claim about
particle physics or unification; the 2026-06-23 retraction of our earlier statements in that direction stands.

---

## 2. The identity, and where the content sits

With $\rho_\Lambda = 3H_\Lambda^2/8\pi G$,

$$\kappa c\sqrt{G\rho_\Lambda} \;=\; \kappa\,cH_\Lambda\sqrt{\tfrac{3}{8\pi}} \;=\; \frac{cH_\Lambda}{Z},
\qquad Z = \frac{\sqrt{8\pi/3}}{\kappa}.$$

Every factor of $\pi$ cancels: the $8\pi$ is the Einstein coupling and the 3 is Friedmann's. **$32\pi/3$ is
not an independent geometric structure** and should not be presented as one. Written to make the content
visible,

$$Z_{\rm fw} = 2\sqrt{8\pi/3} = 5.78881,$$

so the framework sits exactly **one factor of 2** from the $\kappa=1$ reference $\sqrt{8\pi/3} = 2.894405$.
Equivalently $a_0^2 = \tfrac14 c^2G\rho_\Lambda$: the entire distinctive content is one factor of 4, and §6 is
about why that 4 cannot be derived.

**Two footings, both $\kappa = \tfrac12$.** Taking $\rho_\Lambda$ and $H_\Lambda = H_0\sqrt{\Omega_\Lambda}$
gives the canonical $9.36\times10^{-11}$; taking $\rho_{\rm tot}$ and $H_0$ gives $1.13\times10^{-10}$. The
two differ by exactly $1/\sqrt{\Omega_\Lambda} = 1.2082$ and nothing else. We report both throughout, and §8
records that the data currently lean to the second.

---

## 3. The interpolation function is derived

A detector on a worldline of constant proper acceleration in de Sitter space registers a thermal bath at
$T(a) = (\hbar/2\pi ck_B)\sqrt{a^2+A^2}$ with $A = cH_\Lambda$ (Narnhofer, Peter & Thirring 1996; Deser &
Levin 1997, who identify $\sqrt{\Lambda/3+a^2}$ as the 5-acceleration in the flat embedding). Taking inertia
proportional to the excess over the ambient value, normalised by the flat-space Unruh temperature at the same
acceleration:

$$\mu(a) = \frac{\sqrt{a^2+A^2}-A}{a}. \tag{1}$$

The $2\pi$ and the $\hbar$ sit in a common prefactor and cancel from (1) — which is why the construction
carries no $2\pi$.

**(1) is the framework's interpolation function, for every $A$.** In units of $a_0 = 2A$, i.e. $a = 2Ax$,

$$\mu = \frac{\sqrt{4A^2x^2+A^2}-A}{2Ax} = \frac{\sqrt{1+4x^2}-1}{2x},$$

and $A$ has cancelled entirely. This is the interpolation of $g_{\rm obs}^2 = g_{\rm bar}^2+g_{\rm bar}a_0$
identically (symbolic residual zero). So the *shape* is what the mechanism gives regardless of scale.

**And the response law is forced.** Generalising to "inertia tracks the excess in $f(T) = T^n$,"
$\mu_n(v) = [(1+v^2)^{n/2}-1]/v^n \to (n/2)v^{2-n}$ as $v\to0$. Deep-MOND linearity requires $2-n=1$, so
$n=1$ **uniquely**: at $n=2$ the ratio tends to a constant (no MOND regime at all) and at $n\geq3$ it diverges.
Three further variants fail the same way. Hence $a_0 = 2A$ is locked, and only $A$ is free.

> **Scope, and it is a real restriction.** Step (1) is exact for *uniformly accelerated* motion. The step from
> $|a_5|^2 = a_4^2+H^2$ (trajectory-independent) to $T = |a_5|/2\pi$ is the Unruh formula and requires a
> hyperbolic worldline; a circular orbit has Frenet torsion $B$ with $|a|/B = v/c$ exactly, so it is never
> hyperbolic, and rotating detectors are not thermal (Letaw & Pfautsch 1980). Milgrom (1999) states the same
> restriction: *"it is difficult to see how to generalize the argument to arbitrary motions."* The
> $A$-independence and the $n=1$ uniqueness are algebra and survive this; the thermodynamic *derivation* of the
> shape for orbits does not.

---

## 4. The coefficient is discriminable

$Z_{\rm fw} = 5.78881$ against Milgrom's (2020) $2\pi = 6.28319$ is an 8.20% logarithmic gap — 0.0356 dex in
$a_0$, half that in $g_{\rm obs}$ deep in the MOND regime, against 0.108 dex of RAR scatter. Graded by that
scatter the two are indistinguishable, and we previously said so. **That grading is wrong**: the scatter of a
relation is not the error on its parameter, and the two differ by $\sim\sqrt{N}$ with $N = 3380$ here. McGaugh,
Lelli & Schombert (2016) themselves quote $g^\dagger = 1.20\pm0.02\,({\rm random})\pm0.24\,({\rm systematic})$
— a 1.7% random error, five times *smaller* than the gap. The blocker is the 20% stellar mass-to-light
systematic, not statistics.

**That systematic is removable.** Profiling $a_0$ on all 175 SPARC galaxies with $\Upsilon_{\rm disc}$ free
**per galaxy** absorbs any global SPS offset into 175 nuisance parameters. Calibrating the intrinsic scatter to
$\chi^2/{\rm dof}=1$ (0.081 dex) and profiling:

| hypothesis | $a_0$ [$10^{-10}$] | $\Delta\chi^2$ |
|---|---|---|
| **$\kappa=\tfrac12$ (this work)** | 0.936 | **63.9** |
| $\kappa=1/2\pi$ (Milgrom 2020) | 0.862 | 154.3 |
| alternative footing $\rho_{\rm tot}/cH_0$ | 1.131 | 7.0 |
| free best fit | 1.077 | 0 |

$\sigma(a_0)/a_0 = 1.24\%$ with points independent, 5.44% after inflating by the within-galaxy clustering
factor $\sqrt{N_{\rm pts}/N_{\rm gal}} = 4.39$. Against the 8.20% gap that is $Z_{\rm disc} = 6.6$ and 1.5
respectively; the $\Delta\chi^2$ separation of 90.4 is $\approx2.2\sigma$ on the conservative counting.
**$\kappa=\tfrac12$ is favoured over $\kappa=1/2\pi$.**

**Why it works, verified by mutation.** The lever is not the transition shape but the **gas**: with
$g_{\rm bar} = \Upsilon g_\star + g_{\rm gas}$, rescaling $\Upsilon$ does not rescale $g_{\rm bar}$, so the
classical exact $\Upsilon$–$a_0$ degeneracy of the gas-free deep-MOND limit is broken by the HI, whose mass
comes from a flux and carries no mass-to-light ratio. Letting $\Upsilon$ scale the gas as well — restoring the
exact invariance — collapses the constraint by an order of magnitude. The transition region supplies a second,
independent lever: the same rescaling multiplies $g_{\rm obs}$ by the full factor $L$ in the Newtonian limit.

**Forecast-grade, and we label it so.** The estimate omits distance and inclination errors, which are
correlated within a galaxy — the clustering inflation is a stand-in, not a treatment — and it uses the kernel's
shape as part of the lever while assuming that shape. A wrong kernel would bias $a_0$ without widening this
bar. The claim earned is *"the RAR can resolve 8.2% and the M/L systematic is not a wall, and on the
framework's own kernel $\kappa=\tfrac12$ beats $1/2\pi$"* — not *"$a_0$ is now measured to 5.4%."*

---

## 5. The coefficient is not derivable: theorem I

Every ingredient the problem supplies is a rational multiple of an **integer** power of $\pi$: the $4\pi$ of a
sphere's area, the $\tfrac14$ of $S = A/4G$, the $4\pi/3$ of its volume, the $2\pi$ of Unruh and of
Gibbons–Hawking, the $8\pi$ of Einstein, the 3 of Friedmann. De Sitter thermality supplies exactly one number,
$2\pi$.

$Z_{\rm fw}^2/\pi = 32/3$ is **rational**, but $Z_{\rm fw}/\pi^k$ is irrational for every integer $k$ (it
always retains $\pi^{1/2}$, and $\pi$ is transcendental). **Therefore ingredients of that class can force
$Z^2$ but never $Z$** — and every construction attempted fixes $Z$, or a temperature, or a count, *linearly*.
That is why seventeen attempts failed structurally rather than by bad luck, and it identifies the only
admissible shape: a construction intrinsically quadratic in the horizon radius.

**Caveat, stated because it limits the theorem's force.** "Unreachable" here is exact arithmetic. Rational
multiples of powers of $\pi$ come within 0.50% of $\sqrt{32\pi/3}$ (e.g. $\tfrac{11}{6}\pi$), comfortably
inside the empirical box, so approximate agreement in this class is cheap and any future construction must
land *exactly* to count.

---

## 6. The coefficient is not derivable: theorem II

Reduce the target. $a_0^2 = c^4\Lambda/32\pi$, and with $\Lambda = 8\pi G\rho_\Lambda/c^2$,

$$a_0^2 = \tfrac14\,c^2G\rho_\Lambda,$$

so the whole remaining content is one forced dimensionless $\tfrac14$ multiplying $c^2G\rho_\Lambda$. Two facts
then close the admissible shape identified in §5:

1. **$32\pi$ is not a geometric number.** Every forced de Sitter curvature invariant is an $O(1)$ multiple of
   $\Lambda$ ($R/4$, $\sqrt{R_{ab}R^{ab}}/2$, $\sqrt{3K/8}$ all equal $\Lambda$; $1/R_H^2 = \Lambda/3$),
   against a target coefficient $1/32\pi = 0.00995$ — 34× smaller at best. A quadratic construction therefore
   cannot be built from curvature alone; it must couple explicitly to matter, forcing the $\tfrac14\,c^2G\rho$
   form above.
2. **The only forced $\tfrac14$ carries $\hbar$.** $a_0 = \kappa c\sqrt{G\rho_\Lambda}$ is $\hbar$-free. The
   Bekenstein–Hawking $\tfrac14$ lives in $S$ and only in $S$, and in any ratio of entropies it cancels
   together with the $\hbar$ — so it survives only un-ratioed, and then $\hbar^{-1}$ survives with it. The sole
   $\hbar^{+1}$ the horizon supplies is a **temperature**, which is a frequency scale, returning the
   construction to the linear class barred by §5.

**Hence quadratic in $Z$, $\hbar$-free, and carrying the forced $\tfrac14$ are jointly unsatisfiable.**
Exactly one thing would reopen this: a forced dimensionless $\tfrac14$ that is $\hbar$-free and is not the
Bekenstein–Hawking quarter. Nothing in general relativity or horizon thermodynamics supplies one — the
available constants ($4\pi/3$, $8\pi$, 3, the Schwarzschild $\tfrac12$, the Tolman 2, the equipartition
$\tfrac12$) combine into halves, never quarters. Recorded as a coincidence and not cashed: the Newtonian
self-gravity of $\rho_\Lambda$ at $R_H$ is exactly $\tfrac12 cH_\Lambda$, because $(4\pi/3)\times(3/8\pi) =
\tfrac12$ identically — which shows where the halves come from, and that it is not $\kappa$.

---

## 7. Prior art, and what is and is not ours

**The kernel has three independent owners. The coefficient has none.**

1. **Milgrom (1999)**, Phys. Lett. A **253**, 273, eqs (6)–(9): the de Sitter–Unruh construction, this
   interpolation function, and $\hat a_0 = 2(\Lambda/3)^{1/2} = 2cH_\Lambda$ — which is $2Z = 11.5776$ times
   the value used here. His Eq. (9) is algebraically our kernel. He writes no action, and concludes that "an
   actual inertia-from-vacuum mechanism is still a far cry off."
2. **Deser & Levin (1997)**, Class. Quantum Grav. **14**, L163: $2\pi T = (\Lambda/3+a^2)^{1/2} = a_5$, the
   5-acceleration in the flat embedding. Any reading of $A$ as a "rest mass in acceleration space" is this.
   With **Narnhofer, Peter & Thirring (1996)**, Int. J. Mod. Phys. B **10**, 1507. Neither mentions MOND.
3. **Luo (2026)**, arXiv:2602.14515v2: $a_{\rm eff}^2 = (a_N+a_{\rm bg})^2-a_{\rm bg}^2$ with
   $a_{\rm bg} = \sqrt{\Lambda/12}$ is our exact relation, from de Sitter second-moment broadening. An
   independent third occupation, and his $a_0$ sits at the horizon scale.
4. **Ho, Minic & Ng** (Phys. Lett. B **693**, 567; arXiv:1201.2365) write a Born–Infeld action with a force law
   of our form. **It forces no coefficient**: their Born–Infeld scale is never computed, their $1/4\pi$ is
   inserted "for a normalization purpose," and $a_0$ is *set* by the equivalence principle with the value
   imported from their earlier de Sitter-temperature argument. They state $a_c = 2a_0$ as a law and use
   $a_c = a_0/2\pi$ as admitted numerology — two statements differing by $4\pi$ within one lineage. Their field
   solution moreover has no MOND branch at all: with Gauss's law, $E_g/a_N\to1$ exactly in the weak field.

So: **the shape, the mechanism, and $2cH_\Lambda$ are prior art; the rational coefficient $\kappa=\tfrac12$,
its measurement in §4, and the two theorems in §5–6 are the contribution.** Also cited for the record:
**Milgrom (1994)** Ann. Phys. **229**, 384 (the nonlocality theorem, and the exactness of the algebraic
relation for circular orbits); **Milgrom (2022)** PRD **106**, 064060 (modified inertia in Fourier space);
**Bekenstein (2004)** PRD **70**, 083509 and **Bekenstein & Milgrom (1984)** ApJ **286**, 7; **Shariati &
Jafari (2021)** PRD **104**, 084070 (the curl obstruction); **Costa, Franzmann & Pereira** arXiv:1904.07321
(the local modified-inertia Lagrangian and its instability); **Namouni (2015)** MNRAS **452**, 210 (a
variational modified-inertia construction treating light deflection).

---

## 8. Liabilities, stated in full

**The theory side points away from $\kappa=\tfrac12$.** Spectral naturalness picks $2\pi$; the horizon-entropy
route picks $2cH_\Lambda$; de Sitter thermality picks $A = cH_\Lambda$, i.e. $a_0 = 2cH_\Lambda$ — 11.58× the
value here. These are **one physical input wearing three hats**, not three independent votes, and $2\pi$ is not
even the nearest reachable value (§5). But the direction is consistent and it is against us. In the de
Sitter–Unruh reading $A$ is a theorem, not a parameter.

**Two independent estimators pull $a_0$ high.** The §4 profile likelihood gives $1.077\times10^{-10}$ and the
gas-dominated $a_0$-line slope gives $1.181\times10^{-10}$ with a 13% averaging floor (11–14%, and the floor
cannot be beaten by sample size). Both sit above canonical; they bracket the alternative footing, agreeing with
each other to 9.2% — tighter than the 20.8% footing fork. They are not independent (the gas-dominated sample is
a subset of the 175), so the bracketing is the robust part, not a combined error bar.

**The exact form carries a solar-system liability.** $g_{\rm obs}^2 = g_{\rm bar}^2+g_{\rm bar}a_0$ forces a
constant $a_0/2$ sunward anomaly, 1279× the Earth 2σ ephemeris bound, with **no external-field relief**: the
orbit-averaged sunward anomaly is $1.000\times a_0/2$ on all four footing × field corners, because a
fixed-direction field enters through $\langle \mathbf{g}_{\rm ext}\cdot\hat r\rangle = 0$. Softening the kernel
to $\mu = x/\sqrt{1+x^2}$ reduces this by $a_\odot/a_0 = 2233$ but does **not** discharge it: the residual is a
$1/g$ tail and therefore binds at the *lowest*-acceleration body, which is the Sun, giving 8.5× (canonical) /
12.4× (alternative) the Mars ranging budget after a full ephemeris fit. Escapes exist outside the power-law
family — an exponential tail clears by $>10^{13}$ — at the cost of the derivation in §3.

**Other fronts, honestly.** $a_0(z)$ is **exactly blind** to $\kappa$ ($\kappa$ cancels in $a_0(z)/a_0(0)$), so
it tests the $\rho_\Lambda$ tie and not the number. The cluster residual is $+0.405$ dex, which is 1.35–4.05σ
across the systematic floor's own 0.1–0.3 dex range — the range, not its tight end, is the honest statement.
The SN-Ia host-step lever yields $|\Delta m_{a_0}| < 0.082$ mag at 2σ with a central $-0.023\pm0.017$: mass
remains the preferred carrier, and the $a_0$ component is disfavoured but not excluded. The Milky Way rotation
curve's normalisation at $R_0$ misses by $\sim34$ km/s, with boundary, convergence, disc-geometry and
external-field escapes all closed by computation — the residual is real, and $\sim33\%$ of it is the cost of
the softened kernel.

---

## 9. What would settle it

**For the coefficient:** the measurement of §4 with a genuine distance and inclination error model. It is the
only front in the corpus that resolves 8.2% at all, and it needs no new data.

**For the derivation:** a forced, $\hbar$-free dimensionless $\tfrac14$ that is not the Bekenstein–Hawking
quarter (§6). Absent that, $\kappa = \tfrac12$ is fitted and, on the ingredients available, provably
unfitted-by-derivation. Seventeen attempts across four independent axes now stand behind that statement, at
$\log_2 17 = 4.09$ bits of accumulated look-elsewhere.

**We state the resulting position plainly.** The de Sitter tie and the interpolation function are derivable, and
one of them we derive here in a form independent of the scale. The coefficient is measured, favoured over its
nearest rival at $\approx2.2\sigma$, and not derived — and we have shown that it cannot be, on this ingredient
set. That is a smaller claim than we have made in the past and a better-supported one.

---

## 10. Reproducibility

Every number is produced by a committed, runnable script that exits non-zero on a failed internal check.
§3: `reviews/mi_dsunruh_kernel_package_2026.py`, `reviews/mi_dsunruh_freedom_audit_2026.py`. §4:
`real_research/reviews/mi_a0_profile_likelihood_sparc_2026.py`. §5:
`reviews/mi_kernel_measure_from_desitter_2026.py`, `reviews/mi_kappa_linear_class_2026.py`. §6:
`reviews/mi_quadratic_z_escape_2026.py`, `reviews/mi_horizon_entropy_route_2026.py`. §7 and the corrections in
§3 and §8: `reviews/mi_action_programme_close_2026.py`. §8:
`real_research/reviews/mi_alpha2_sun_reflex_2026.py`,
`real_research/reviews/mi_efe_escape_and_ch23_withdrawn_2026.py`,
`real_research/reviews/mi_a0_footing_selection_2026.py`,
`real_research/reviews/mi_snia_power_curve_2026.py`,
`real_research/reviews/mi_aqual_alt_footing_rerun_2026.py`, `real_research/reviews/clusters_eta_audit.py`.
SPARC data: Lelli, McGaugh & Schombert (2016).

## References

Bekenstein, J. D. 2004, Phys. Rev. D **70**, 083509 · Bekenstein, J. D. & Milgrom, M. 1984, ApJ **286**, 7 ·
Costa, R., Franzmann, G. & Pereira, J. P. 2019, arXiv:1904.07321 · Deser, S. & Levin, O. 1997, Class. Quantum
Grav. **14**, L163 · Gibbons, G. W. & Hawking, S. W. 1977, Phys. Rev. D **15**, 2738 · Ho, C. M., Minic, D. &
Ng, Y. J. 2010, Phys. Lett. B **693**, 567; arXiv:1201.2365 · Lelli, F., McGaugh, S. S. & Schombert, J. M.
2016, AJ **152**, 157 · Letaw, J. R. & Pfautsch, J. D. 1980, Phys. Rev. D **22**, 1345 · Luo, M. J. 2026,
arXiv:2602.14515 · McGaugh, S. S., Lelli, F. & Schombert, J. M. 2016, Phys. Rev. Lett. **117**, 201101 ·
Milgrom, M. 1994, Ann. Phys. **229**, 384 · Milgrom, M. 1999, Phys. Lett. A **253**, 273 · Milgrom, M. 2020 ·
Milgrom, M. 2022, Phys. Rev. D **106**, 064060 · Namouni, F. 2015, MNRAS **452**, 210 · Narnhofer, H., Peter,
I. & Thirring, W. 1996, Int. J. Mod. Phys. B **10**, 1507 · Shariati, A. & Jafari, N. 2021, Phys. Rev. D
**104**, 084070 · Skordis, C. & Złośnik, T. 2021, Phys. Rev. Lett. **127**, 161302
