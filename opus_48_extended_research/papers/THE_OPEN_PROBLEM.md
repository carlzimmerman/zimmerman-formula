# The open problem

## One number stands between a fitted coefficient and a derived one

**Carl P. Zimmerman** — Briar Creek Tech
*2026-08-09. Every number below is produced by a named committed script that exits non-zero on failure.*

---

## The question, posed exactly

The framework's central claim is $a_0 = \kappa\,c\sqrt{G\rho_\Lambda}$ with $\kappa$ a pure number,
fitted at $\tfrac12$. The graviton-bath calculation (`mi_graviton_bath_ctp_2026.py`, 15/15)
established the exact relation

$$\boxed{\;\kappa^2 \;=\; 8\pi\,\epsilon_{\rm tot}\;}$$

where $\epsilon_{\rm tot}$ is the fractional inertia correction from summing horizon-mode variances.
**"Why is $\kappa = \tfrac12$?" is therefore precisely the question "why is
$\epsilon_{\rm tot} = 1/(32\pi) = 0.00995$?"** — a specific dimensionless number in a specific
mode-counting calculation. That question was not well-posed before; it is now.

## What is already established

1. **The form is derived.** The de Sitter horizon entropy cancels the Planck suppression *exactly*:
   $S_{\rm dS}\,GH^2 = \pi$ identically, so $G$, $H$ and $M_{\rm Pl}$ all drop out of
   $\epsilon_{\rm tot}$ and $a_0 = cH \times (\text{pure number})$ is forced. Control: with a generic
   mode count the scales survive — only the horizon entropy cancels them.
2. **The nonlinearity is free.** $\sqrt{1+X} = 1 + X/2 - X^2/8 + \dots$: the worldline's own
   proper-time element supplies the rectifying term, at second order in $h$, using the graviton
   two-point function. No third cumulant needed.
3. **A single graviton loop is dead**: $\epsilon_1 \sim 3\times10^{-125}$, short by ~120 orders.
   The horizon sum is not optional.
4. **The bath must be gravitational.** Universality of $a_0$ excludes any scalar bath (mass-dependent
   drift), and a graviton bath produces the density form $c\sqrt{G\rho_\Lambda}$ — the form whose
   coefficient can be *rational*. Rate mechanisms ($cH$) cannot avoid $\sqrt{\pi}$
   (`mi_cubic_noise_ctp_2026.py`, 18/18).

## Why nobody has the number

Five defensible readings of "sum the variance over horizon modes" span
$\kappa = 0.013$–$2.047$ — a factor 162 (`mi_eps_tot_mode_counting_verdict_2026.py`, 13/13).
**The one that lands on $\tfrac12$ exactly is structurally invalid**: it used
$\langle X^2\rangle = \langle h^2\rangle$ with $X = h_{\mu\nu}u^\mu u^\nu$, but radiative gravitons in
TT gauge have $h_{0\mu}=0$, so for a static worldline the coupling *vanishes*, and for a moving one it
is $(v/c)^2$-suppressed and velocity-dependent — which would break universality outright. That
near-miss is recorded, because it was one unchecked step from being reported as a derivation.

## The calculation that would settle it

A pure number, from a fixed procedure with no free choices:

1. the **gauge-invariant coupling** — the tidal (Riemann) projection along the worldline, not the
   $u$-contraction of $h_{\mu\nu}$;
2. the **accelerated worldline**, not a static one — with the Deser–Levin temperature
   $T \propto \sqrt{a^2 + (cH)^2}$, which is simultaneously where the $a$-dependence (the
   interpolation function itself) must come from;
3. the graviton **tensor structure and both polarisations**;
4. the horizon **mode count** $S_{\rm dS} = A/4G = \pi/GH^2$, or its justified replacement;
5. a **regulator** for the $\zeta(1)$ divergence at the rapidity-gap-forced $p=1$ — the surviving
   half of the old no-go.

**If it returns $1/(32\pi)$, $\kappa = \tfrac12$ is derived. If it returns anything else, the
framework's coefficient is an empirical constant — like $G$ — and none the worse for it.**
This is a real calculation someone should do properly, not an evening's computer algebra.

One warning attaches: $\epsilon_{\rm tot} = (\text{horizon entropy})\times(\text{per-mode
fluctuation})$ is the structure of Verlinde-class entropic gravity, which carries a large critical
literature. Landing there is not automatically good news.

## The sober fact about the data

$\kappa$ is currently **measured**, not known:

| route | result | script |
|---|---|---|
| BTFR intercept (SPARC) | $\kappa = 0.465 \pm 0.076$ | `mi_btfr_intercept_kappa_door_2026.py` (20/20) |
| distance-free $g_{\rm bar}$ estimator (175 SPARC galaxies) | $\kappa = 0.551 \pm 0.043$ | `mi_distance_free_gbar_estimator_sparc_2026.py` (14/14) |

**$\tfrac12$, $1/\sqrt3 = 0.577$, $\sqrt{3/8} = 0.612$ and $0.40$ all sit inside $2\sigma$.**
So a "derivation" of $\tfrac12$ published today would be unfalsifiable decoration — worth nothing
with referees, and this framework does not traffic in it.

What would make the question falsifiable: $\sigma(\kappa) \approx 0.014$, reachable by combining
SPARC's 3.9% floor with the wide-binary + pulsar-timing route (chain sensitivity
$-L/2(1+L) = 0.184$, amplification $5.44\times$, $N \gtrsim 136{,}000$ clean pairs — DR5-and-beyond;
`mi_session_audit_2026.py`, 11/11) — **conditional on the $H_0$ tension resolving, because
$\kappa \propto a_0/H_0$ at full strength** (`mi_wb_gext_kappa_route_2026.py`, 19/19).

## What must not be cited on this question

- **Not the de Sitter–Unruh heuristic.** It derives the interpolation function exactly — which is
  Milgrom 1999, PLA 253:273, eq. 9 — and simultaneously forces $a_0 = 2cH_\Lambda$, excluded by SPARC
  at $15.6\sigma$. The construction is rigid at all three of its steps
  (`mi_deser_levin_interpolation_2026.py`, 24/24).
- **Not the "exactly $2Z$" ratio.** $(2cH)/(cH/Z) = 2Z$ identically for any $Z$; Milgrom's rival
  $2\pi$ gives $4\pi$ by the same algebra. A tautology.
- **Not any identity built from $(\Lambda, G, c)$ alone.** Each is a relabelling with a
  convention-dependent residue ($a_0 = m_{\rm cond}/4\sqrt{\pi}$ included;
  `mi_condensate_vacuum_energy_a0_2026.py`, 17/17).

---

*Credit: Milgrom 1999 (the interpolation function); Deser & Levin 1997 (the accelerated-observer
temperature); Gibbons & Hawking 1977; Arkani-Hamed, Cheng, Luty & Mukohyama 2004 (the ghost
condensate). The relation $\kappa^2 = 8\pi\epsilon_{\rm tot}$, the mode-counting no-go, the
universality screen and the problem statement above are this framework's.*
