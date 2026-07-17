# THE CONFRONTATION — Single-Metric Pure-MI Lensing vs Brouwer 2021

**Script:** `python3 confront.py` (exit 0, 9/9 checks; this directory, alongside
`total_stress.py` and `lensing_solve.py` / `SOLVE.md` which derived the prediction).
Data: the **real** Brouwer et al. 2021 (A&A 650, A113, KiDS-1000 isolated-lens RAR)
official CDS release in the frozen repo
(`real_research/data/lensing_rar/brouwer2021_rar/`, READ-ONLY), full covariance,
SIS conversion per the release README — the P2 concordance loader. **Both a₀ footings**
(canonical 9.36e-11, alt 1.13e-10) throughout. No "proves" language.

---

## What was confronted

The derivation (SOLVE.md): the total assembled stress tensor of the MI action,
$\hat T_{\mu\nu} = \rho K\,u_\mu u_\nu - 2(\rho K'/a_0^2)a_\mu a_\nu$, sourcing one
metric (photons on $g$ — the only route surviving the GW170817 erratum), gives

$$F(y) \equiv \frac{g_{\rm lens}}{\nu(y)\,g_{\rm bar}} \simeq \frac{M_{\rm eff}}{M_{\rm bar}}\cdot\frac{1}{\nu(y)} < \frac{1}{\nu(y)} < 1 \quad\text{everywhere}$$

— every term is an $O(K)\le1$ dressing (the on-shell identity $K=1/\nu$ exactly), the
$K'aa$ stress is a bounded *negative* (tension) correction, no $O(\nu)$ structure exists.
**F < 1 is the derived outcome** (the banked trilemma made exact, with the frame legs in).

Brouwer 2021 **measured**: the lensing RAR *equals* the dynamical RAR
$g_{\rm obs}=\sqrt{g_{\rm bar}^2+g_{\rm bar}a_0}$ to ~2.5 dex below $a_0$
(Mistele–McGaugh+ 2024, JCAP 04(2024)020, the same and deeper). Equality = F=1.

## The exclusion (confront.py, real points, full covariance)

| footing | rail $g_{\rm bar}\ge10^{-13}$ (N=7) $\Delta\chi^2$(MI−F=1) | formal σ | full range (N=15) | σ |
|---|---|---|---|---|
| canonical 9.36e-11 | **+722** | ~26.9 | +1496 | ~38.7 |
| alt 1.13e-10 | **+754** | ~27.5 | +1565 | ~39.6 |

- Rail-edge single point ($g_{\rm bar}=1.3\times10^{-13}$): MI predicts
  $8.0\times10^{-14}$, measured $6.0\times10^{-12}$ — **1.9 dex short, 13.4σ alone**.
- MI/measured ratio runs 0.013–0.14 across the rail: the prediction under-shoots
  **every** point.

**Honest-error battery (none rescues it):**

| nuisance | rail Δχ² after |
|---|---|
| profiled free ±0.3 dex coherent amplitude (M*/SIS-conversion systematics) | 715 (can) / 721 (alt), ~27σ |
| M* ±0.2 dex on $g_{\rm bar}$ (lens stellar-mass scale) | ≥ 660 / ≥ 700 |
| B21's **own** hot-CGM baryon-budget variant file (diag) | 794 (~28σ) |
| doc-γ fork ($aa$ coefficient halved; SOLVE.md) | max |ΔF/F| = 4.1%, verdict unchanged |

Why nothing rescues: the MI single-metric prediction has the **wrong slope** — deep in,
$g_{\rm lens}\to(M_{\rm eff}^\infty/M_{\rm bar})\,g_{\rm bar}$ (linear) while the measured
relation follows $\sqrt{a_0 g_{\rm bar}}$. Amplitude systematics (mass scale, conversion,
baryon budget) cannot fix a slope. Mistele–McGaugh 2024 extends the measured equality
deeper; the exclusion only grows.

*(Absolute-χ² note, honest both ways: F=1 itself has imperfect absolute χ² on this
conversion/mass convention — the banked lensing-RAR standing (convention-compatible,
footing-non-diagnostic) is not re-litigated. The MI-vs-F=1 **gap** is what this decides.)*

## Cassini — safe

γ-type (light-bending/Shapiro) corrections: solar source dressing
$1-K \sim a_0/2g_{\rm surf}\sim1.7\times10^{-13}$ (mass-weighted smaller) + vacuum slip
**exactly zero** ($\Pi\propto\rho=0$ outside the source, so $\Phi=\Psi$ exactly,
$\gamma_{\rm PPN}=1$): **~8 orders under** the Cassini $2.3\times10^{-5}$ bound.
The local dressings at Saturn ($y\sim7\times10^5$): $1-K = 2K'X/K = 1/(2y+1)
\approx 7\times10^{-7}$ — these enter *dynamics* ($\nu-1$, the banked deep-Newton pass)
and even they sit ~30× under the bound. Both footings pass. (The AeST/MG $Q_2$
quadrupole caveat concerns the MG realization, stays banked, not re-litigated.)

## GW170817 — automatic

One metric for photons, gravitons, matter ⇒ $c_\gamma = c_{\rm GW}$ **exactly** — an
identity of the construction, not a constraint it passes. (The disformal photon metric,
excluded ~6–7 orders by the erratum, was the route that had to be abandoned; this is
what forced the single-metric confrontation.)

---

## STRAIGHT VERDICT

**Brouwer 2021's measured lensing-RAR = dynamical-RAR equality directly falsifies
single-metric pure MI — this action, this assembled $T_{\mu\nu}$, photons on $g$ — as
the complete theory: ~27σ formal on the conservative reliability rail, ~39σ full range,
both footings, robust to the γ-fork, coherent amplitude, stellar-mass scale, and B21's
own baryon-budget variant.** The theory under-lenses by *more* than the trilemma factor
($F<1/\nu$): the source itself is dressed down by the mass-weighted $1/\nu$.

**The completion statement now reads:** the theory is complete up to its constants in
the **dynamics + cosmology sectors**; **lensing requires physics beyond the current
action.** The named doors (not a "no open doors" claim):

1. the off-circular/nonlocal closure (gap A) — would have to conjure $O(\nu)$ from
   structures whose every bound is $O(K)$;
2. a lensing carrier beyond $S_{\rm EH}+S_u+S_{\rm matter}$ (a dark component or new sector);
3. the free-frame $S_u$ bookkeeping wound (Assemblies I/II un-gravitate matter and fail
   the theory's own Newtonian sector — a formulation-level inconsistency worth closing).

Both outcomes were named in advance; the derived one is $F<1/\nu$. No manufactured save;
no manufactured kill — the F=1 outcome was excluded *by derivation* (the $K'$ stress is
$O(K)$-bounded and tension-signed), then confirmed against the real data.
