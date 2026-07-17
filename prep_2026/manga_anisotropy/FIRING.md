# FIRING — Stage-1 proxy firing of the MG-impossible anisotropy discriminator (MaNGA DR17)

**Date fired:** 2026-07-17 (UTC). **Script:** `fire_anisotropy.py` (exit 0, seed fixed,
no hard-coded verdicts; full log in `fire_anisotropy.out`; figures `fig_delta_vs_P2.png`,
`fig_delta_vs_P1.png`). Everything below was run EXACTLY per the pre-registered spec
frozen at **2026-07-17T00:21:52Z, before any data was downloaded** (`FROZEN.md`); every
non-frozen cell is labelled VARIANT/DIAGNOSTIC and never replaces a frozen primary.

> **EXPLORATORY FIREWALL (frozen, FROZEN.md §5 — carried verbatim at the top of every
> output): NO kill conditions exist for this observable. NOTHING in this run can support
> or kill the framework.** This is the first time anyone has confronted
> d(offset)/d(radial-anisotropy) with data (the prediction was derived 2026-07-16,
> `mi_closure_pin/CONSEQUENCES.md` §1 item A-2). This run CREATES the baseline and
> pre-registers the full-Jeans Stage 2. **THE PROXY IS NOT β** — P2/P1 are LOS
> signatures contaminated by inclination, intrinsic shape, rotation residuals, and M/L
> gradients; the slow-rotator cut mitigates rotation only.

**Framework on its own terms:** de Sitter–Unruh **MODIFIED INERTIA**, own
ν(y)=√(1+1/y); both footings everywhere — canonical a₀=9.36e-11 (cH_Λ/Z, ρ_DE), alt
a₀=1.13e-10 (cH₀, ρ_tot). **The forced prediction:** d(offset)/d(radial anisotropy) > 0
(MI) vs **exactly 0** (MG-with-same-ν, isolated spherical systems). Frozen sign map
(Binney & Mamon 1982; Cappellari 2008 JAM): radial anisotropy ↔ more negative
P2 = dlnσ/dlnR, so **MI ⇒ dδ/dP2 < 0; MG ⇒ 0**.

**Sample:** N=48 MaNGA DR17 slow rotators ((V/σ)_glob<0.4 PRIMARY cut), the frozen
SNR-top-16-per-σ_e-tercile resolved subsample of the 382 primary / 2,407 quality-parent
catalog; δ = log₁₀(K_v σ_e² R_e/G) − log₁₀(ν(y)·M_bar), K_v=5.0.
**Controls held: log₁₀M\*, log₁₀R_e, z** (frozen; + log₁₀σ_e in bracket B).
**Environment control OMITTED and stated** — no public group catalog was crossmatched at
firing time (permitted by FROZEN.md §4 with statement; Stage 2 should add e.g. Tempel+
2017 SDSS groups).

---

## 1. THE FIRST NUMBER (exploratory, firewalled)

Full frozen grid — Huber robust slope of δ vs P2 with controls, 10,000-pair bootstrap,
partial Spearman; **dex of offset per unit dlnσ/dlnR**; MG-zero comparison per cell:

| cell (footing × IMF) | slope | 95% CI | p vs MG-zero | partial Spearman ρ |
|---|---|---|---|---|
| **P2 canon fixed-IMF (Chabrier)** | **−0.635** | [−1.141, −0.200] | **0.019** (zero outside) | −0.30 [−0.59, +0.03] |
| P2 canon IMF-A (×1.55 common-mode) | −0.635 | [−1.142, −0.178] | 0.027 | −0.31 |
| **P2 canon IMF-B (σ-dep + σ-control)** | **+0.002** | [−0.011, +0.006] | 0.437 (**zero inside**) | +0.03 |
| P2 alt fixed-IMF | −0.636 | [−1.138, −0.199] | 0.022 | −0.30 |
| P2 alt IMF-A | −0.635 | [−1.139, −0.189] | 0.021 | −0.31 |
| P2 alt IMF-B | +0.002 | [−0.014, +0.007] | 0.430 | +0.03 |
| P1 canon fixed-IMF (secondary, N=33) | −1.086 | [−2.685, +0.585] | 0.198 (zero inside) | −0.24 |
| P1 alt fixed-IMF | −1.088 | [−2.699, +0.620] | 0.192 | −0.24 |
| P1 canon/alt IMF-B | ≈0.00 | zero inside | 0.87/0.84 | −0.20/−0.22 |

**Read-off (three facts, equal prominence):**

1. **Fixed-IMF: the MI-predicted sign fires.** dδ/dP2 = −0.64 ± 0.24, excluding the MG
   zero at p≈0.02 (~2.3σ bootstrap-equivalent; rank-based partial Spearman is weaker,
   ρ=−0.30 with CI grazing zero → treat as ~1.5–2σ). Footing-independent to 3 decimal
   places (the footings differ only through log ν, ~0.005 dex here) and untouched by the
   common-mode IMF-A bracket, exactly as pre-registered.
2. **The frozen bracket-B rerun kills it: NOT ROBUST by the frozen standard.**
   FROZEN.md §2 pre-committed: "a slope that dies under bracket B is reported as NOT
   robust." It dies (+0.002, zero inside). Verbatim verdict: **the MI-like fixed-IMF
   slope is NOT ROBUST.**
3. **Why it dies (diagnostic decomposition, labelled non-frozen cells):** bracket B
   changes two things at once. Separated: the literature-scale (0.30 dex/dex) IMF *mass
   correction alone* (frozen C3 controls) only moves −0.636 → −0.545 (**14% removed**,
   still zero-excluding); the added **log σ_e control alone** (no IMF correction) drives
   the slope to +0.0005 with residual scatter 0.001 dex. The collapse is **algebraically
   structural**: δ contains +2 log σ_e by construction (M_dyn = K_v σ_e² R_e/G), so at
   fixed M*, R_e the dynamical "hotter" signal and any σ-correlated IMF live in the SAME
   direction — the σ-control removes signal and confounder TOGETHER. A σ-dependent IMF
   would need ~2.0 dex/dex (≈6–7× the literature trend) to cancel the whole fixed-IMF
   slope through the mass term alone. **Stage 1 cannot separate a σ-correlated IMF from
   the dynamical signal; only Stage-2 Jeans β (not a monotone function of σ_e) breaks
   the degeneracy.** Both the frozen NOT-ROBUST verdict and this structural reason are
   carried together.

**The amplitude over-budget check (computed, decisive for interpretation):** the 48
galaxies sit at **y = g_bar/a₀ ≈ 5–11** (median 7.9 canon / 6.6 alt), where the
framework's own boost is only ν−1 ≈ 2–10% (median log ν ≈ 0.026/0.031 dex). The
fixed-IMF trend amplitude |slope|×s_P2 = **0.173 dex ≈ 7× the entire per-galaxy MI
boost** (and ~11× its 16–84% cross-sample spread) — far more than any genuine MI
anisotropy modulation could produce in this high-acceleration sample. **So even at face
value the MI-signed slope CANNOT be read as MI support**; its amplitude is dominated by
structural/K_v/σ-channel systematics, exactly what the firewall anticipated.

**Bottom line of the first number:** an MI-signed, MG-zero-excluding fixed-IMF proxy
slope that (a) is declared NOT ROBUST by the pre-registered bracket-B standard, (b) is
an order of magnitude too large to be the MI effect in this y-regime, and (c) is
therefore a **baseline systematics measurement, not evidence** — for either side. MG is
NOT favored either: the bracket-B zero is equally consistent with "signal removed by an
over-conservative control." Honest state: **UNINFORMATIVE ON MI-vs-MG, by construction;
baseline created.**

## 2. Robustness grid (labelled variants; frozen primaries never replaced)

- **V/σ cut:** the resolved subsample is all-PRIMARY by the frozen rule, so the 0.6
  VARIANT is the identical sample at the resolved level, and no catalog-level variant
  exists because NO DAPall-level proxy was frozen (FROZEN.md §3) — stated, not run.
  Labelled substitute (resolved-V/σ median split at 0.10): colder half +0.31 (zero
  inside, N=24); hotter half −0.66 [−1.28, −0.22] (zero outside, N=24). The signal
  carrier is the half with more residual rotation — consistent with a
  rotation/structural contaminant, flagged.
- **IMF-risk guard (drop σ_e ≥ 212 km/s top quartile, N=36):** slope −0.70 but 95% CI
  [−1.11, +0.44] — sign stable, significance lost (power).
- **Resolved-vs-catalog-proxy comparison:** EMPTY BY FREEZE (no catalog proxy frozen).

## 3. Power statement for full-Jeans Stage 2 (from the observed scatter)

Observed post-control robust δ scatter **s_e = 0.181 dex**; P2 spread 0.272; P1 spread
0.051. For δ regressed on Jeans/JAM β with population spread s_β and per-galaxy error
e_β (attenuated lever s_β_eff), a 3σ detection at 80% power needs
N ≈ ((3.84·s_e)/(b·s_β_eff))², with the MI slope scale b bracketed 0.02–0.05 dex/unit-β
from the rider-a bracket (illustrative; `mi_closure_pin/CONSEQUENCES.md` §1):

| b [dex/β] | s_β=0.20, e_β=0.05 | s_β=0.20, e_β=0.10 | s_β=0.15, e_β=0.10 |
|---|---|---|---|
| 0.02 | N ~ 32,000 | N ~ 38,000 | N ~ 78,000 |
| 0.05 | N ~ 5,200 | N ~ 6,100 | N ~ 12,500 |
| 0.10 | N ~ 1,300 | N ~ 1,500 | N ~ 3,100 |

Against available samples (MaNGA: 382 primary slow rotators / 2,407 quality parent;
published ATLAS³D-class JAM β for ~260 ETGs): **Stage 2 at the current 0.18-dex scatter
is underpowered at every plausible b.** Feasibility requires BOTH (i) driving s_e down
to ~0.10 dex (SBF/FP distances + resolved M/L in place of NSA masses) and (ii) moving to
**low-y pressure-supported systems** (dSphs, dwarf ETGs, cluster outskirts) where the MI
budget O(0.02–0.05 dex) is actually available — in this MaNGA regime (y≈5–11) the
effect ceiling is ~7× below the systematics floor regardless of N. That regime
statement is itself a Stage-1 product: **the discriminator's natural home is deep-MOND
dispersion systems, not massive ETGs.**

## 4. Honesty rails (status at firing)

1. Freeze preceded data (2026-07-17T00:21:52Z; HEAD checks only before it); the firing
   ran the frozen spec unmodified; all extra cells labelled DIAGNOSTIC/VARIANT.
2. Proxy ≠ β stated at every output; the P1 β-mapping remains
   inclination/shape-degenerate and P1 stayed secondary (its fixed-IMF sign agrees but
   is zero-inside).
3. IMF confounder: pre-registered direction honored; corr(P2, log σ_e) = −0.62 makes the
   confounder LIVE; the frozen bracket-B verdict (NOT ROBUST) is reported verbatim, with
   the computed decomposition (14% IMF-correction vs σ-control collapse) beside it.
4. Exploratory firewall enforced: nothing here supports or kills the framework; the
   MG-consistent bracket-B cells and the MI-signed fixed-IMF cells are reported with
   equal prominence; the amplitude over-budget check actively blocks over-reading the
   MI-like sign.
5. Both footings in every cell (differences negligible, as expected at y≫1); exit-0;
   seed fixed; frozen zimmerman-formula repo untouched (this lane lives outside it).

**Next actions pre-registered by this firing:** Stage 2 = per-galaxy Jeans/JAM β on
low-y dispersion systems with ≤0.1-dex mass/distance errors; add an environment control
(named group catalog); keep P2 only as a cross-check, never as the β carrier.
