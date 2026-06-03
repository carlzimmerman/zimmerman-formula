# The deep-MOND sign as a DSSYK calculation — a precise, hand-off-ready problem

**Carl Zimmerman · June 2026.** *We took the deep-MOND-sign prize as far as honest in-session computation
allows. This document states what is **done** (with verified code) and the **two bounded calculations** that
remain, precisely enough for someone fluent in the chord formalism to finish. Nothing here is fabricated;
the open pieces are stated as problems, not pretended results. Companion code:
`reviews/project04b_dssyk_scoping.py`, `project04c_dssyk_calculation.py`, `project04d_matter_coupling.py`.*

---

## The claim and the setup

If gravity is emergent and the MOND scale is the cosmic horizon's surface gravity, the deep-MOND *sign*
(gravity **enhanced** at low acceleration) requires the horizon degrees of freedom to **freeze linearly**,
$N_{\rm eff}(T)\propto T$ below the de Sitter temperature $T_{\rm dS}$, which gives $a=\sqrt{a_0 g_N}$ with
$a_0\sim cH$. Linear freezing requires a **flat density of states**. The double-scaled SYK theory (DSSYK)
is the proposed dual of the 2D de Sitter static patch (Narovlansky–Verlinde 2023; Rahman 2022; Susskind),
so its spectrum *is* the horizon spectrum. DSSYK Hamiltonian = the q-Hermite chord transfer matrix on
chord-number states $|n\rangle$: diagonal $0$, off-diagonal $b_n=\sqrt{[n]_q}$, $[n]_q=(1-q^n)/(1-q)$,
$q=e^{-\lambda}$. Energies $E=\tfrac{2}{\sqrt{1-q}}\cos\theta$, $\theta\in[0,\pi]$; the de Sitter
(maximal-entropy) point is the spectral **center** $E=0$.

## What is DONE (verified in code)

1. **The DSSYK DOS is the chord-vacuum spectral measure** $\rho(E)=\sum_i|\langle0|E_i\rangle|^2\delta(E-E_i)$
   (the q-Gaussian), *not* the raw eigenvalue density (which is the wrong, arcsine, answer — a bug we caught;
   verified the vacuum-weighted variance against the analytic $\mathrm{Var}(E/E_0)=(1-q)/4$). It is **flat**
   near $E=0$.
2. **The freezing is linear in the dual.** $f(T)=\sum_{|E_i|<T}|\langle0|E_i\rangle|^2\simeq 2[\rho](0)\,T$
   near the de Sitter point, for every $q$. So **DSSYK realizes the linear MOND freezing** — the deep-MOND
   *mechanism* is a property of the solvable dual, not just the brick-wall heuristic. Slope
   $c_1=2\rho(0)\approx1.6/\sqrt{1-q}$.
3. **Linearity is conditional on the coupling.** $f(T)$ is linear iff the probe-weighted DOS $[w\rho](0)\neq0$.
   Chord-vacuum and shallow probes give linear ($\to$MOND); deep-chord probes ($n\gtrsim5$) give sub-linear
   ($\not\to$MOND), because their central overlap oscillates/vanishes. **MOND requires the probe to couple to
   the near-vacuum (low-chord) sector.**

## Remaining Calculation 1 — the matter-chord support (one yes/no)

**Question.** Does the matter operator $O_\Delta$ acting on the de Sitter vacuum produce a state
$O_\Delta|0\rangle$ with **nonzero support at low chord number** (so $[w\rho](0)\neq0$ and the freezing is
linear)?

**What to compute.** The chord-number wavefunction $\psi_n=\langle n|O_\Delta|0\rangle$, and in particular
whether $\psi_0\neq0$ and the weight $w(E)=|\langle E|O_\Delta|0\rangle|^2$ is smooth and nonzero at $E=0$.

**The object to use.** The DSSYK matter two-point function / matrix element of $O_\Delta$ between energy
eigenstates is known in closed q-form: a matter chord of weight $\Delta$ crosses Hamiltonian chords with
weight $q^\Delta$, and (Berkooz–Isachenko–Narovlansky–Torrents 2018; Lin 2022)
$$
 |\langle\theta_1|O_\Delta|\theta_2\rangle|^2 \;\propto\;
 \frac{\big(q^{2\Delta};q\big)_\infty}{\prod_{\pm,\pm}\big(q^{\Delta}e^{i(\pm\theta_1\pm\theta_2)};q\big)_\infty}
 \quad(\text{q-Gamma form; verify the exact prefactor against the source}).
$$
Project this onto the chord-number basis via the q-Hermite overlaps $\langle n|\theta\rangle\propto H_n(\cos\theta\,;q)$
to get $\psi_n$, and read off $\psi_0$ and $w(0)$.

**Success / failure.** $w(0)\neq0$ $\Rightarrow$ deep-MOND sign holds in the dual. $w(0)=0$ $\Rightarrow$ the
freezing picture fails and the sign must come from elsewhere (the modified-entropy route, Project 1 Part 5).
**Bulk expectation:** chord number $\sim$ geodesic length $\sim$ depth in the static patch; the MOND regime is
**near the horizon** = low chord number, so $w(0)\neq0$ is expected. (This is the DSSYK form of the
spherical-probe$\to$monopole selection rule, Project 1c.)

## Remaining Calculation 2 — the coefficient $Z$ (the dictionary)

**Question.** Does the DSSYK freezing reproduce $a_0\simeq0.18\,cH$ (equivalently $Z\simeq5.5$)?

**What to compute.** Two dictionary numbers fix it:
- **$\lambda_{\rm dS}$** — the value of $\lambda$ (hence $q$) describing the physical de Sitter horizon. Fix it
  from the de Sitter entropy: $S_{\rm dS}=A/4G\sim10^{122}$ must equal the DSSYK entropy at the center
  ($\ln$ of the effective central degeneracy), which is a known function of $\lambda$ and the system size.
- **$T_{\rm dS}/E_0$** — the Gibbons–Hawking temperature in units of the spectral width, i.e. where the
  freezing completes ($f\!=\!1$). The flat window shrinks as $q\to1$, so verify $T_{\rm dS}/E_0$ lies **inside**
  it (the "race" of project 4b).

Then $N_{\rm eff}/N_{\rm full}=c_1(T/E_0)$ with $T/E_0$ mapped to $a/(cH)$ via $T_{\rm dS}$, giving
$a_0/cH=1/[c_1\,(T_{\rm dS}/E_0)^{-1}\cdots]$ — evaluate and compare to $0.18$. A match for a physically
sensible $\lambda_{\rm dS}$ would **derive $Z$**; a mismatch quantifies what extra physics the coefficient needs.

## Status

> **Mechanism: derived in the dual (linear freezing realized in DSSYK).** **Coupling: MOND requires
> near-vacuum probe coupling (computed); whether the physical probe satisfies it is Calculation 1.**
> **Coefficient: open, Calculation 2.** Two bounded calculations in existing formalism finish the prize.

This is the sharpest, most honest state of the deep-MOND-sign problem reached here: not solved, but reduced
from "why this sign?" to two named, literature-defined calculations, with the mechanism verified by direct
computation and nothing fabricated.

**References.** Berkooz, Isachenko, Narovlansky, Torrents, *JHEP* (2018), arXiv:1811.02584 (DSSYK spectrum &
correlators); H. Lin, *JHEP* (2022), arXiv:2208.07032 (the bulk/chord Hilbert space & matter); Narovlansky &
Verlinde, arXiv:2310.16994 (DSSYK–de Sitter); Rahman, arXiv:2209.09997 (dS JT & DSSYK); Susskind,
arXiv:2209.09999 (de Sitter static patch & complexity).
