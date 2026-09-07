# The Zimmerman Programme

**One claim: the galactic acceleration scale is set by the dark-energy density.**

$$a_0 \;=\; \kappa\,c\sqrt{G\rho_\Lambda}\;=\;c^2\sqrt{\frac{\Lambda}{32\pi}}\;=\;9.3619\times10^{-11}\ \mathrm{m\,s^{-2}}$$

Plain text, for the record: `a0 = kappa * c * sqrt(G * rho_Lambda) = c^2 * sqrt(Lambda / (32 pi)) = 9.36e-11 m/s^2`, with κ = ½ **adopted** — measured **0.551 ± 0.043** by a distance-free method (fitted, **not derived**; four candidate coefficients sit inside 2σ). Alternative footing (ρ_total, cH₀): a₀ = 1.1279×10⁻¹⁰ — every dimensional result in this repository is quoted on both footings.

<details open><summary><b>Key equations, plain text (for search; every symbol defined)</b></summary>

```
a0 = kappa c sqrt(G rho_Lambda), kappa = 1/2 (FITTED, not derived):  a0 = (1/2) c sqrt(G rho_Lambda) = c^2 sqrt(Lambda/(32 pi)) = 9.36e-11 m/s^2
   natural units (c = hbar = 1):  a0 = M_Lambda^2 / (2 M_Planck),  M_Lambda^4 = rho_Lambda,  M_Planck = G^(-1/2)   (a gravitational seesaw with an exact 2)
   equivalently  4 a0^2 = G c^2 rho_Lambda,   Lambda = 32 pi a0^2 / c^4,   Lambda l0^2 = 32 pi  with  l0 = c^2/a0
deep-MOND baryonic Tully-Fisher:  v_flat^4 = G M_bar a0 = (1/2) c G^(3/2) M_bar sqrt(rho_Lambda)
the a0-line:  g_obs^2 - g_bar^2 = a0 g_bar;   RAR kernel  nu(y) = 1/(1 - exp(-sqrt(y))),  y = g_bar/a0   (Milgrom & Sanders 2008; McGaugh, Lelli & Schombert 2016)
a0(z)/a0(0) = sqrt(rho_DE(z)/rho_DE(0)):  flat to < 1% for z <= 5 if Lambda is constant
candidate covariant action (2026-09):  L = sqrt(-g)/(16 pi G) [ R - 2 Lambda - c1 T1 - c2 T2 - c3 T3 + c4 T4 + 2 (2 - K_B) J^mu d_mu phi - K(Q) - (2 - K_B) J(Y + xi^2 |grad_perp V|^2) ] + L_m
   n_mu = -d_mu tau / N (khronometric clock),  J^mu = n^nu grad_nu n^mu,  Q = n . d phi,  Y = q^{mu nu} d_mu phi d_nu phi,  K = K2 (Q - Q0)^2,  c1 = -c3 = K_B
static law:  div( J_Y grad phi ) = laplacian Psi,   J_Y(s) = s / Delta(s),   g_phi = a0 Delta(s),   s = g_N / a0
   nu_RAR carried:  Delta(s) = s / (exp(sqrt(s)) - 1), saturated at its maximum s = 2.540, Delta = 0.6476 (bounded-boost theorem)
coherence length (Cassini floor):  xi >= 0.10 pc (canonical) / 0.15 pc (alt)
zero-mode theorem (k01):  the field equations contain J only through J';  the background sees Lambda_eff = Lambda + (2 - K_B) J(0)/2 + K(Q0)/2  =>  a0 and Lambda independent
Lambda-free vacuum (k01):  rho_vac = -(2 - K_B) I a0^2 / (16 pi G),  I = 2 int_0^{s_sat} s dDelta = 0.4525  =>  rho_vac / rho_Lambda = -0.0045 (wrong sign, 220x too small)
global constraint (k02):  <L_phi> / rho_Lambda ~ 1e-5 today -> 0 in the de Sitter future
four-form promotion (k04):  a0 = beta sqrt(G) |q|,  P(q) = Z q^2 / 2,  eps = q P_q - P > 0;   kappa^2 = 2 beta^2 / (Z + 2 b beta^2);   kappa = 1/2  <=>  Z / beta^2 = 7.96
   environmental scale:  a0_loc = a0 (1 - g_N / (155 a0)),  scalar off above 155 a0
horizon coefficient (k03):  a0 = c^2 / (2 pi L_dS)  =>  kappa = sqrt(8 pi / 3) / (2 pi) = 0.461;   H0 lock:  kappa = 1/2 at H0 = 67.4  ==  kappa = 0.461 at H0 = 73.0 (fixed Omega_Lambda, to 0.2%)
Gaia DR4 wide binaries (Amendment 11, both arms registered):  Arm A  gamma_v = 1.1614-1.1814 (canonical) / 1.1917-1.2267 (alt);   Arm B  gamma_v <= 1.0450 / 1.0300;   Newton 1.000
```
</details>

The exact algebraic law (the **a₀-line**) and the operative interpolation kernel:

$$g_{\rm obs}^2-g_{\rm bar}^2=a_0\,g_{\rm bar}
\qquad\Longleftrightarrow\qquad
g_{\rm obs}=\sqrt{g_{\rm bar}^2+a_0\,g_{\rm bar}}\,,
\qquad
\nu(y)=\frac{1}{1-e^{-\sqrt{y}}}$$

(kernel form: **Milgrom & Sanders 2008**, ApJ 678, 131, Eq. 13 at α = ½ — adopted by McGaugh–Lelli–Schombert 2016; credited, not claimed). Operative arm since 2026-08-08: **modified gravity** — the modified-inertia arm is closed, excluded 21σ by lensing. Prior art on the arm verdict: Banik & Zhao ([arXiv:2110.06936](https://arxiv.org/abs/2110.06936), §2.5–2.6).

**The relativistic realisation** embeds the scale in Aether-Scalar-Tensor theory (Skordis & Złośnik 2021, PRL **127** 161302 — theirs, credited) with one structural promotion — **the MOND scale is the dark sector's pressure**:

$$\boxed{\;\mathcal{A}(\mathcal{Q})\equiv a_0^2(\mathcal{Q})=\kappa^2\,G\,\bigl(-\mathcal{K}(\mathcal{Q})\bigr)\;}
\qquad
\mathcal{K}(\mathcal{Q})=-M^4+\mu^2\Lambda_D^2\left[1-\sqrt{1-\frac{(\mathcal{Q}-\mathcal{Q}_0)^2}{\Lambda_D^2}}\right]$$

an offset-DBI with β ≡ μ²Λ_D²/M⁴ = 1 (selected, not derived). Since p = 𝒦 identically and −𝒦 = ρ_Λ today, the a₀ normalisation above is reproduced to the digit, **w = −1 stays exact**, and the redshift law is **derived, not imposed**:

$$\frac{a_0^2(z)}{a_0^2(0)}=\frac{\sqrt{1+\nu_0^2}}{\sqrt{1+\nu_0^2\,(1+z)^6}}\,,
\qquad z_t=\nu_0^{-1/3}-1\in[17,35]$$

— constant to <1% everywhere MOND is tested (z ≤ 5), **off at recombination as an output** (a₀ falls to 0.002–0.006 of today's value), so the CMB's dust-like clustering is a prediction, not an accommodation. Newest result (2026-08-14): AeST's free background rate is **pinned by galaxy-scale phenomenology alone**, in observables where a₀ cancels identically:

$$\mathcal{Q}_0=\frac{g_{\rm tot}-g_N}{c\,v}\;\approx\;2.4\times10^{-3}\,\text{–}\,1.5\times10^{-2}\ \mathrm{Mpc}^{-1}$$

interior to Skordis & Złośnik's own CMB fits, containing both their MOND-compatible parameter sets and excluding their MOND-incompatible one ([DOI 10.5281/zenodo.21937958](https://doi.org/10.5281/zenodo.21937958)).

**Standing 2026-09-06 (rev. 8) — the coefficient is a boundary condition; both wide-binary arms registered; the dark-sector hunt frozen.** The candidate covariant action (khronometric clock + dynamical MOND scalar + coherence operator, ν_RAR carried) **cannot relate a₀ to Λ**: the MOND primitive enters the field equations only through its derivative and the FLRW background only through Λ + (2−K_B)J(0)/2, a normalisation zero mode ([`kappa_closure/k01`](kappa_closure/k01_zero_mode_theorem_and_lambda_free_vacuum.py)). The Λ-free repair yields a *negative* vacuum energy 220× too small; a sequestering-type global constraint misses by five orders ([`k02`](kappa_closure/k02_global_constraint_average.py)); promoting a₀ to a conserved four-form flux fixes the sign and makes a₀ ∝ √(Gρ_Λ) structural but leaves κ as the free coupling ratio Z/β² = 8, with an environmental a₀ that switches the scalar off above 155 a₀ and is invisible in galaxies ([`k04`](kappa_closure/k04_four_form_promotion_consistency.py)). The one coefficient-free alternative, the horizon form a₀ = c²/(2πL_dS) (κ = 0.461), is 8.5% from ½, below the 9.5% BTFR mass-budget floor, and **exactly degenerate with the H₀ tension**: κ = ½ on Planck's H₀ and κ = 0.461 on SH0ES's predict the same a₀ to 0.2% ([`k03`](kappa_closure/k03_half_vs_two_pi_precision.py)). κ = ½ is therefore an empirical boundary condition this class of actions cannot derive, to be settled by a stellar M/L zero point, an absolute gas scale and H₀ — published as [DOI 10.5281/zenodo.22559892](https://doi.org/10.5281/zenodo.22559892). **Gaia DR4:** [Amendment 11](prep_2026/gaia_dr4_prep/PREREGISTRATION_DR4.md) registers **both** mutually exclusive arms before the data — Arm A (the frozen kernel as modified gravity) γ_v = 1.1614–1.1814 / 1.1917–1.2267, Arm B (the covariant candidate at its Cassini-minimal coherence length) **ceilings 1.0450 / 1.0300** — with the decision rule fixed in advance; DR4 separates the arms at 4.2σ but cannot confirm Arm B over Newton beyond 1.6σ (stated against interest). **Dark sector:** the thermal-relic completion is a pincer with no interior (N_eff needs m ≥ 27.6 eV, the RAR needs ≤ 11 eV, the cluster profile worked only at 11.4 eV; [`g04f`–`g04i`](qwen_claude_field_theory/closure_2026/)), four condensate doors are closed on the action's own terms, and the hunt is frozen behind the coefficient question. The existing-archive high-z Tully–Fisher confrontation is exhausted; the decisive object is a deep-MOND lensed rotator at z ≈ 2.5 ([target ranking](prep_2026/a0z_crossscale/highz_target_score_2026.py)).

**Standing 2026-09-04 (rev. 7) — the kernel, the pincer, and a length.** The field theory's own kernel is the RAR function exactly; the closure programme had frozen $1-e^{-x}$ and then the sharp $\mu_{10}$, and with $a_0$ and the disc M/L profiled the galaxy data reject every Cassini-safe sharpened kernel while leaving exponential-versus-RAR undecided ([`f23`](hunt_2026/f23_kernel_transcription_audit.py), [`f25`](hunt_2026/f25_profiled_kernel_comparison_mu10.py), [`f28`](hunt_2026/f28_one_argument_pincer.py)). The framework's kernel as modified gravity gives the Solar System an external-field quadrupole 6–9× the Cassini ceiling ([`f23`](hunt_2026/f23_kernel_transcription_audit.py), [`f24`](hunt_2026/f24_aqual_quadrupole_rar_kernel.py)); modified inertia is lensing-dead; no acceleration-only law passes both. The one structure that does is **QUMOND on a Helmholtz-smoothed Newtonian potential with a coherence length ξ**: the Solar System needs only ξ ≥ 0.045 pc (one solar MOND radius; the binding bound is the phantom mass inside Saturn's orbit), for a smooth-cored smoothing the pre-registered wide-binary boost at 20–30 kAU survives with the knee moved to 15–20 kAU, while a local biharmonic host has a cuspy kernel whose constant sunward force needs ξ ≥ 0.8 pc and predicts Newtonian binaries; three of four outer-halo globulars want ξ ≈ 50–140 pc ([`f29`](hunt_2026/f29_coherence_length_law.py), [`f30`](hunt_2026/f30_ppn_screening_door.py); the pre-registration is untouched). The screened scalar has no 1/r potential inside ξ, so the preferred-frame PPN lock that closed the aether-scalar hosts does not apply to it: that host class is reopened as a calculation. Clusters: no threshold in any variable marks where the kernel stops working, and the group-versus-cluster contrast is estimator-limited ([`f22`](hunt_2026/f22_cluster_threshold_hunt.py)). Full block: [STANDING.md](STANDING.md).

**Standing 2026-09-02 (rev. 6) — what the September closure changed.** The condensate above is a **γ = 2 polytrope** in the static limit, $p_d=(2\pi G/\mu^2)\rho_d^2$, $c_s^2=4\pi G\rho_d/\mu^2=|\Psi|c^2$ (published, [DOI 10.5281/zenodo.22242701](https://doi.org/10.5281/zenodo.22242701), v2 [22254075](https://doi.org/10.5281/zenodo.22254075)). Read on the cosmic background the same relation gives $c_s^2(z)=4\pi G\rho_{\rm dm}(z)/\mu^2$, which **pins** the DBI amplitude at β = 1, $\Lambda_D/Q_0=\nu_0\Omega_\Lambda/\Omega_{\rm dm}$, 18–300× above the repository's own $P(k)$ ceiling: **the v9 single-field dark sector is excluded**, and the cluster cosmology built on it is withdrawn ([RETRACTIONS.md](RETRACTIONS.md), 2026-09-02). Underneath is a $K$-independent matching theorem: a galaxy well today is the background at $(1+z)^3=\delta_{\rm well}\le5000$ with identical sound speed, so a dust cold enough for the Lyman-α forest falls into galaxies — **pressure cannot keep Ω_dm out of galaxies**, for any $K$. The superfluid route, a rising $a_0\propto H(z)$, and a Hubble-scaled high-pass filter were each run and closed the same way; a quadratic-order theorem shows any elliptic auxiliary that enters the lapse equation frees one dust-like scalar, which is why TeVeS, AeST and the superfluid all carry a third field. The v9 embedding also fails the preferred-frame PPN bounds (α₁, α₂; 2026-08-31, [`closure_2026/fried_chicken_final/`](qwen_claude_field_theory/closure_2026/fried_chicken_final/)), and the nonlocal Deffayet–Woodard kernel class is unstable at linear order (published, [DOI 10.5281/zenodo.22253953](https://doi.org/10.5281/zenodo.22253953), v2 [22255522](https://doi.org/10.5281/zenodo.22255522)). **What survives:** $a_0=\tfrac c2\sqrt{G\rho_{\rm DE}(z)}$ with κ fitted, the $a_0(z)$ switch-off law (it needs only the trace khronon dust), MOND phenomenology, and a cold Ω_dm that double-counts with the boost in galaxies by 2.7–4.4× — the programme's blocking problem. Scripts: [`closure_2026/condensate_pincer_2026/`](qwen_claude_field_theory/closure_2026/condensate_pincer_2026/); explainer: [DUST_FALLS_INTO_GALAXIES.md](opus_48_extended_research/papers/DUST_FALLS_INTO_GALAXIES.md).

> ### ⚠️ Read this first
>
> **This is not a theory of everything.** All theory-of-everything and Standard-Model claims were
> **publicly retracted 2026-06-23** — see [RETRACTIONS.md](RETRACTIONS.md), which records every
> withdrawn claim, dated, including material from an earlier automated effort that is **not part of
> the audited programme**.
>
> **Credit — and it is larger than this repository used to say.** The law
> $g_{\rm obs}^2=g_{\rm bar}^2+a_0g_{\rm bar}$ is **not merely the same interpolating kernel** as
> Milgrom's. **Milgrom (1999, *Phys. Lett. A* 253, 273, Eqs. 6–9) derives this exact law from the de
> Sitter–Unruh balance and fixes its coefficient at $a_0=2cH_\Lambda$** — verified symbolically here,
> difference exactly zero. Re-derived entropically by Pikhitsa (2010, arXiv:1010.0318) and
> Klinkhamer & Kopp (2011, arXiv:1104.2022), both also landing on $2cH_\Lambda$. The a₀–Λ *tie* has
> prior art three times over: Blanchet & Le Tiec (2009), Blanchet & Seraille (2025), and Singh (2026,
> arXiv:2601.04290 — the same formula, coefficient 8% away).
>
> **So what is this programme's?** A **re-normalisation of the coefficient to fit data**
> ($\kappa=\tfrac12$ against Milgrom's derived 2), the **pressure promotion 𝒜(𝒬) and its derived
> a₀(z) law**, the **𝒬₀ pin**, the **frozen wide-binary pre-registration**, and the structural
> results below. Not a derivation of the law, and not a derivation of its scale.
>
> **→ [STANDING.md](STANDING.md) is the single source of truth.** If anything here conflicts with it,
> STANDING is newer.

---

## Start here

| document | what it is |
|---|---|
| **[STANDING.md](STANDING.md)** | **The entry point** (rev. 7 block, 2026-09-04, at the top; rev. 6 below it). Claim · earned · postulated · live fronts · closed doors · open liabilities · retractions in force. |
| [RETRACTIONS.md](RETRACTIONS.md) | Every withdrawn claim, dated. |
| [INTEGRITY_AUDIT.md](INTEGRITY_AUDIT.md) | Audit trail on the corpus itself. |
| [CITATION.cff](CITATION.cff) · [LICENSE.md](LICENSE.md) | How to cite; code AGPL-3.0, content CC-BY-4.0. |

---

## What is novel, by topic

Ordered by how much survives scrutiny. Each entry links the working directory and the paper.

### 1 · The coefficient reduction and the a₀ line
$a_0=\kappa c\sqrt{G\rho_\Lambda}$ makes every $\pi$, the 32 and the 3 cancel, and
$g_{\rm obs}^2-g_{\rm bar}^2=a_0g_{\rm bar}$ is an exact identity.
**RAR fit: 0.108 dex on SPARC** at Υ = 0.70 — the anchored a₀ costs *nothing* against a fitted one
(anchoring is cost-free, not "better"; both are indistinguishable after Υ-refit). κ is **measured**:
0.551 ± 0.043 distance-free, 0.465 ± 0.076 from the BTFR.
[`prep_2026/a0_line/`](prep_2026/a0_line/) · paper [THE_COSMOLOGICAL_CONSTANT_SETS_A0.md](opus_48_extended_research/papers/THE_COSMOLOGICAL_CONSTANT_SETS_A0.md)

### 2 · The field theory — THE COMPLETION (v9)
The full action, the pressure promotion, the derived a₀(z), and the no-ghost/c_T = 1 health
results — with the non-claims led by "κ = ½ NOT DERIVED".
Verified (all script-backed): CLASS CMB pass (0.01σ vs cosmic variance) · lensing 21.2σ → 0.6σ with
γ_PPN = 1 · c_T = 1 exact · no-ghost theorem · RAR 0.108 dex · BTFR · solar system ·
**pure-framework weak-lensing RAR 40 kpc–2.2 Mpc, χ²/dof = 2.03 canonical / 0.94 alt, no dark
component** (real KiDS data, and the same fit *rejects* adding one).
Honest limits: **dark matter exists at full Ω_dm, and as of 2026-09-02 it is cold** — the condensate's
own equation of state, read on the cosmic background, excludes the single-field dark sector and closes
every kinetic mechanism for keeping it out of galaxies (see the rev. 6 block above). The action, the
promotion, the switch-off law and the health results stand; the "dust job" does not.
**Paper: [THE_COMPLETION.md](opus_48_extended_research/papers/THE_COMPLETION.md) · v9 DOI [10.5281/zenodo.21895046](https://doi.org/10.5281/zenodo.21895046)** (concept [21863521](https://doi.org/10.5281/zenodo.21863521)) · plain-language companion [10.5281/zenodo.21865866](https://doi.org/10.5281/zenodo.21865866) · evidence: [`nbody_2026/`](nbody_2026/), every stage green.

### 3 · Pinning AeST's free parameter — the 𝒬₀ pin
AeST's authors state the dark-sector density is "not (classically) predicted"; its published fits
span four orders of magnitude in 𝒬₀. Three framework commitments collapse that freedom to one
parameter, and galaxy-scale phenomenology fixes it: **𝒬₀ ≈ 2.4×10⁻³–1.5×10⁻² Mpc⁻¹** — with the
corroboration that both MOND-compatible published CMB fits land inside the band and the
MOND-incompatible one lands outside, though no CMB information entered the derivation. The pin is
**a₀-free in observables** (the local-a₀ challenge was raised by the author and adjudicated in the
open), and it survived its strongest internal test: a candidate transport mechanism that would have
drained the halo turns out to be inconsistent with the pin that calibrates it — a fixed-point
result that closed a door and defended the pin in the same move.
**Paper: [PINNING_Q0_IN_AEST.md](opus_48_extended_research/papers/PINNING_Q0_IN_AEST.md) · v4 DOI [10.5281/zenodo.21937958](https://doi.org/10.5281/zenodo.21937958)** (concept [21935942](https://doi.org/10.5281/zenodo.21935942)) · scripts: [`nbody_2026/`](nbody_2026/) stages 56–63.

### 4 · Wide binaries — the sharpest live front
[`prep_2026/gaia_dr4_prep/`](prep_2026/gaia_dr4_prep/) — **frozen, hash-stamped pre-registration**,
ten amendments, all filed *before* data. **In force (Amendment 10): γ_v = 1.1614–1.1814 canonical /
1.1917–1.2267 alt**, no-verdict edge 1.23, built on the full nonlinear AQUAL-EFE solve (the
registered point-response number was killed by its own solve — largest eigenvalue declared
isotropic — and replaced by a computed band, in the open, before data). **Clock: Gaia DR4,
~Dec 2026.** Newest (2026-08-14): the EFE-present *exact two-body* solve shows the band top is
conservative **and** a sub-band reading is more likely — both directions stated; and under the
framework's own local-a₀ structure DR4 doubles as a *conditional* charge meter.
**New note: [DR4_TARGET_UNDER_LOCAL_A0.md](opus_48_extended_research/papers/DR4_TARGET_UNDER_LOCAL_A0.md) · DOI [10.5281/zenodo.21937976](https://doi.org/10.5281/zenodo.21937976).**
⚠️ The literature disagrees violently on this quantity — Banik+24 reports 19σ Newtonian; Chae 2023
reports γ = 1.43 ± 0.06 — which is why the systematic budget is split one-sided.

**Amendment 11 (2026-09-06) — both arms registered.** The programme now carries two mutually exclusive wide-binary predictions and both are on record before Gaia DR4: Arm A, the frozen kernel as modified gravity, γ_v = 1.1614–1.1814 (canonical) / 1.1917–1.2267 (alt); Arm B, the covariant candidate action at its Cassini-minimal coherence length evaluated with the same estimator, ceilings γ_v ≤ 1.0450 / ≤ 1.0300 falling toward 1.000 as the length grows. Arm A's kernel as strict AQUAL fails the Cassini quadrupole 4–5×; with the length that passes Cassini it *is* Arm B, so the two cannot both hold. Decision rule fixed in advance (σ_tot = 0.028): A falsified below 1.056, B falsified at or above 1.129, arm undecided 1.084–1.101; DR4 separates the arms at 4.2σ but cannot confirm B over Newton beyond 1.6σ even at its ceiling — a Newtonian result kills A and leaves B alive but unconfirmed, and must never be called a success. Append-only, hash-stamped ([`AMENDMENT11_HASH.txt`](prep_2026/gaia_dr4_prep/AMENDMENT11_HASH.txt)).

### 5 · The BTFR discriminator and a₀(z) fronts
The derived a₀(z) law predicts **<2×10⁻⁴ dex** of BTFR zero-point evolution at z ≤ 5 (flat below
z_t) — so the observed 1 < z < 5 null is a *prediction*, while the naive a₀ ∝ cH(z) reading is
disfavoured ~2.3σ with two wrong-sign tests. Pre-stated falsification bars: **0.15 dex** (HI,
gas-dominated, z ≤ 1) / **0.33** ([CII], z ~ 2–5) / **0.44** (stellar); SKA-mid/ngVLA reach
decisive power. Any robust a₀ evolution below z ~ 5 falsifies the law — either sign.
[`nbody_2026/stage60_btfr_discriminator_2026.py`](nbody_2026/stage60_btfr_discriminator_2026.py) · cross-scale: [`prep_2026/a0z_crossscale/`](prep_2026/a0z_crossscale/)
**Framework vs ΛCDM (2026-09-01):** ΛCDM's RAR scale is emergent from halo structure and rises ×1.8 by z = 2; added as a fourth zero-parameter law to the joint likelihood over the 10 committed high-z constraints it is **undecided and prior-dominated** (the sign flips with the drift ceiling; Ciocan carries every face-value verdict). The decisive measurement is the **deep-MOND BTFR zero-point at z ≈ 2.5: framework 0.00 dex, ΛCDM-native +0.33 dex, one clean point at ±0.13 dex decides at 20:1** — a JWST/ALMA target, not a survey. To mimic a flat a₀, ΛCDM's haloes would have to be diluted to 0.61 (z = 2) / 0.40 (z = 3) of their N-body concentrations. [`a0z_lcdm_native_hypothesis_2026.py`](prep_2026/a0z_crossscale/a0z_lcdm_native_hypothesis_2026.py) · [`real_research/crispy_2026/`](real_research/crispy_2026/)

### 6 · Structural theorems (MI era, kept for the record)
Seven machine-verified results on the closed modified-inertia arm; five are prohibitions.
**Paper: [MI_STRUCTURAL_THEOREMS.md](opus_48_extended_research/papers/MI_STRUCTURAL_THEOREMS.md) · DOI [10.5281/zenodo.21708842](https://doi.org/10.5281/zenodo.21708842)** — the worldline
test-particle theory survives as mathematics; the arm is closed as physics.

### 7 · Nulls, published as nulls — **the part most worth reading**
- [`project_atomos/`](project_atomos/) — exhaustive Standard-Model parameter search, **null**, DOI [10.5281/zenodo.21654272](https://doi.org/10.5281/zenodo.21654272), published *after* an audit withdrew two of its own claims
- **Z carries no geometry:** at the real ±16% precision **9,912** expressions match a₀; $Z=\sqrt{8\pi/3}/\kappa$ carries exactly one bit beyond κ — [`reviews/z_numerology_density_2026.py`](reviews/z_numerology_density_2026.py)
- κ-forcing closed: [KAPPA_ONE_PARAMETER_GEOMETRY.md](opus_48_extended_research/papers/KAPPA_ONE_PARAMETER_GEOMETRY.md) · [THE_SEARCH_WAS_NEVER_WASTED.md](opus_48_extended_research/papers/THE_SEARCH_WAS_NEVER_WASTED.md)

---

## Working rules

Enforced by the scripts, not by trust.

1. **Test the framework on its own terms** — modified gravity (since 2026-08-08), horizon-derived a₀, its own interpolation. Never through the standard-MOND lens.
2. **Verify a deficit as rigorously as a win.** Manufacture neither.
3. **Both a₀ footings on every dimensional number** — canonical ρ_DE (9.36×10⁻¹¹), alternative ρ_total (1.13×10⁻¹⁰) — and show the spread.
4. **Every load-bearing claim gets a committed, runnable script** that exits non-zero on a failed internal check. No hard-coded verdicts.
5. **Never say "the theory is closed."**
6. **Amend frozen pre-registrations in the open, before data.**
7. **Adversarial refereeing before commit** — findings land only after an independent attempt to refute them, and refuted drafts are withdrawn with banners, not silent edits.
8. **Cite or flag** — any number not traced to a script or a cited paper is marked unverified.
9. **Nothing personal in this repository.**

---

## Publication record

[![Kappa No-Go](https://img.shields.io/badge/The%20Coefficient%20of%20the%20a0%E2%80%93%CE%9B%20Relation%20%E2%80%94%20Zero--Mode%20Theorem%20(Sep%206%202026)-10.5281%2Fzenodo.22559892-red)](https://doi.org/10.5281/zenodo.22559892)
[![Bounded-Boost Theorem v4](https://img.shields.io/badge/A%20Ceiling%20Dark%20Matter%20Cannot%20Impose%20%E2%80%94%20Bounded--Boost%20Theorem%20(v4%2C%20Sep%206%202026)-10.5281%2Fzenodo.22548669-red)](https://doi.org/10.5281/zenodo.22548669)
[![Filtered MOND Action](https://img.shields.io/badge/The%20Filtered%20MOND%20Action%20(Sep%205%202026)-10.5281%2Fzenodo.22347632-red)](https://doi.org/10.5281/zenodo.22347632)
[![Crispy Fried Chicken Matching Theorem](https://img.shields.io/badge/Crispy%20Fried%20Chicken%20Matching%20Theorem%20(Sep%202%202026)-10.5281%2Fzenodo.22261001-red)](https://doi.org/10.5281/zenodo.22261001)
[![Nonlocal MOND Kernel Instability v2](https://img.shields.io/badge/Nonlocal%20MOND%20Kernel%20Instability%20(v2%2C%20Sep%202026)-10.5281%2Fzenodo.22255522-red)](https://doi.org/10.5281/zenodo.22255522)
[![Cluster Phase Pinning v2](https://img.shields.io/badge/Cluster%20Phase%20Pinning%20Polytrope%20(v2%2C%20Sep%202026%20%E2%80%94%20cosmology%20withdrawn)-10.5281%2Fzenodo.22254075-orange)](https://doi.org/10.5281/zenodo.22254075)
[![THE COMPLETION v9](https://img.shields.io/badge/THE%20COMPLETION%20v9%20(dark%20sector%20excluded%20Sep%202026)-10.5281%2Fzenodo.21895046-red)](https://doi.org/10.5281/zenodo.21895046)
[![Q0 Pin v4](https://img.shields.io/badge/Pinning%20AeST's%20Q0%20(v4%2C%20Aug%2014%202026)-10.5281%2Fzenodo.21937958-red)](https://doi.org/10.5281/zenodo.21937958)
[![DR4 under local a0](https://img.shields.io/badge/DR4%20Target%20under%20Local%20a0%20(Aug%2014%202026)-10.5281%2Fzenodo.21937976-red)](https://doi.org/10.5281/zenodo.21937976)
[![DR4 Pre-registration](https://img.shields.io/badge/Gaia%20DR4%20Pre--registration-10.5281%2Fzenodo.21702746-black)](https://doi.org/10.5281/zenodo.21702746)
[![MI Structural Theorems](https://img.shields.io/badge/MI%20Structural%20Theorems%20(v2)-10.5281%2Fzenodo.21708842-blueviolet)](https://doi.org/10.5281/zenodo.21708842)
[![Atomos Null](https://img.shields.io/badge/Atomos%20SM%20Search%20%E2%80%94%20NULL%20(v2)-10.5281%2Fzenodo.21654272-lightgrey)](https://doi.org/10.5281/zenodo.21654272)
[![License](https://img.shields.io/badge/code-AGPL--3.0-lightgrey)](LICENSE)
[![Content License](https://img.shields.io/badge/content-CC--BY--4.0-lightgrey)](LICENSE.md)

<details><summary>Full chronological badge wall (2026 record)</summary>

[![Paper DOI](https://img.shields.io/badge/Paper-10.5281%2Fzenodo.20576485-blue)](https://doi.org/10.5281/zenodo.20576485)
[![Falsification Map DOI](https://img.shields.io/badge/Falsification%20Map%20(June%202026)-10.5281%2Fzenodo.20670670-blueviolet)](https://doi.org/10.5281/zenodo.20670670)
[![de Sitter Gauge DOI](https://img.shields.io/badge/de%20Sitter%20Gauge%20(June%2016%202026)-10.5281%2Fzenodo.20721540-blueviolet)](https://doi.org/10.5281/zenodo.20721540)
[![Skordis-Zlosnik DOI](https://img.shields.io/badge/Why%20Skordis%20%26%20Zlosnik%20Were%20Right%20(June%2020%202026)-10.5281%2Fzenodo.20773004-blueviolet)](https://doi.org/10.5281/zenodo.20773004)
[![Cluster Density No-Go DOI](https://img.shields.io/badge/Galaxy--Cluster%20Density%20No--Go%20(June%2020%202026)-10.5281%2Fzenodo.20779562-blueviolet)](https://doi.org/10.5281/zenodo.20779562)
[![s̄^TX Target DOI](https://img.shields.io/badge/s%CC%84%5ETX%20Ephemeris%20Target%20(June%2027%202026)-10.5281%2Fzenodo.20978308-blueviolet)](https://doi.org/10.5281/zenodo.20978308)
[![Growing-ν DOI](https://img.shields.io/badge/Growing%20Neutrino%20Mass%20(June%2027%202026)-10.5281%2Fzenodo.20977421-blueviolet)](https://doi.org/10.5281/zenodo.20977421)
[![Scale Without Law DOI](https://img.shields.io/badge/Scale%20Without%20Law%20(June%2028%202026)-10.5281%2Fzenodo.21016309-blueviolet)](https://doi.org/10.5281/zenodo.21016309)
[![Cluster Anisotropy DOI](https://img.shields.io/badge/Cluster%20Anisotropy%20MI%20Test%20(July%201%202026)-10.5281%2Fzenodo.21104820-blueviolet)](https://doi.org/10.5281/zenodo.21104820)
[![a0(z) Discriminant DOI](https://img.shields.io/badge/Non--Monotonic%20a0(z)%20(July%201%202026)-10.5281%2Fzenodo.21110936-blueviolet)](https://doi.org/10.5281/zenodo.21110936)
[![s̄^TX Fixed-Direction DOI](https://img.shields.io/badge/s%CC%84%5ETX%20Fixed--Direction%20Fit%20(July%202%202026)-10.5281%2Fzenodo.21137568-blueviolet)](https://doi.org/10.5281/zenodo.21137568)
[![Sign Premise DOI](https://img.shields.io/badge/Sign%20Premise%20%3D%20State%20Clause%20(July%202%202026)-10.5281%2Fzenodo.21139029-blueviolet)](https://doi.org/10.5281/zenodo.21139029)
[![Which-a₀ DOI](https://img.shields.io/badge/Which%20a0%3F%20Population%20Split%20(July%202%202026)-10.5281%2Fzenodo.21140507-blueviolet)](https://doi.org/10.5281/zenodo.21140507)
[![Fourth Horn DOI](https://img.shields.io/badge/Fourth%20Horn%20PT%2FPU%20Exclusion%20(July%202%202026)-10.5281%2Fzenodo.21148494-blueviolet)](https://doi.org/10.5281/zenodo.21148494)
[![Five Theorems DOI](https://img.shields.io/badge/Five%20Theorems%20Kernel%20Closure%20(July%203%202026)-10.5281%2Fzenodo.21152331-blueviolet)](https://doi.org/10.5281/zenodo.21152331)
[![Sixth Theorem DOI](https://img.shields.io/badge/Sixth%20Theorem%20Transient%20Closure%20(July%203%202026)-10.5281%2Fzenodo.21175723-blueviolet)](https://doi.org/10.5281/zenodo.21175723)
[![Residual Doors DOI](https://img.shields.io/badge/No%20Pump--Free%20Corner%20(v3%2C%20July%2017%202026%20%E2%80%94%20D3%20sign%20corrected)-10.5281%2Fzenodo.21179351-blueviolet)](https://doi.org/10.5281/zenodo.21179351)
[![Position Whitepaper DOI](https://img.shields.io/badge/POSITION%3A%20There%20Is%20No%20Dark%20Matter%20in%20Galaxies%20(July%2011%202026)-10.5281%2Fzenodo.21312985-black)](https://doi.org/10.5281/zenodo.21312985)
[![Flagship DOI](https://img.shields.io/badge/FLAGSHIP%20dS--Unruh%20MI%20%2B%20Lensing%20Trilemma%20(July%2011%202026)-10.5281%2Fzenodo.21312654-red)](https://doi.org/10.5281/zenodo.21312654)
[![Elastic-Medium Action DOI](https://img.shields.io/badge/Covariant%20Elastic--Medium%20Action%20(July%2010%202026)-10.5281%2Fzenodo.21301058-blueviolet)](https://doi.org/10.5281/zenodo.21301058)
[![y_c=Z/2 Cutoff DOI](https://img.shields.io/badge/Elastic--Medium%20Cutoff%20y_c%3DZ%2F2%20(July%2010%202026)-10.5281%2Fzenodo.21300855-blueviolet)](https://doi.org/10.5281/zenodo.21300855)
[![MI Completion DOI](https://img.shields.io/badge/Written%20MI%20Action%20%E2%80%94%20Covariant%20Completion%20(v13%2C%20July%209%202026)-10.5281%2Fzenodo.21253644-crimson)](https://doi.org/10.5281/zenodo.21253644)
[![MI Field Theory Results DOI](https://img.shields.io/badge/MI%20Field%20Theory%20Results%20(July%2016%202026)-10.5281%2Fzenodo.21403470-crimson)](https://doi.org/10.5281/zenodo.21403470)
[![a0-line / Lambda-inversion DOI](https://img.shields.io/badge/a0--line%20%2B%20%CE%9B--inversion%20from%20Rotation%20(July%2017%202026)-10.5281%2Fzenodo.21419735-red)](https://doi.org/10.5281/zenodo.21419735)
[![Lensing No-Go DOI](https://img.shields.io/badge/Passivity%20Obstruction%20%E2%80%94%20MI%20Lensing%20No--Go%20(July%2017%202026)-10.5281%2Fzenodo.21418816-red)](https://doi.org/10.5281/zenodo.21418816)
[![Sigma-Spread DOI](https://img.shields.io/badge/Relational%20%CF%83--Spread%20%E2%80%94%20MG--Impossible%20Signature%20(July%2017%202026)-10.5281%2Fzenodo.21421896-red)](https://doi.org/10.5281/zenodo.21421896)
[![Cross-Scale a0(z) DOI](https://img.shields.io/badge/Cross--Scale%20a0(z)%20%E2%80%94%20Galaxy%20vs%20Cosmic%20Dark%20Energy%20(v2%2C%20July%2019%202026)-10.5281%2Fzenodo.21440407-red)](https://doi.org/10.5281/zenodo.21440407)
[![SHLEM Null DOI](https://img.shields.io/badge/SHLEM%20Null%20%E2%80%94%20Which%20Acceleration%20Does%20Inertia%20Listen%20To%3F%20(July%2020%202026)-10.5281%2Fzenodo.21458605-red)](https://doi.org/10.5281/zenodo.21458605)
[![Triangle DOI](https://img.shields.io/badge/Three%20Roads%20to%20the%20%CE%9B%20Acceleration%20Scale%20(July%2020%202026)-10.5281%2Fzenodo.21460161-red)](https://doi.org/10.5281/zenodo.21460161)
[![TDG History DOI](https://img.shields.io/badge/Tidal%20Dwarfs%20%26%20History--Dependent%20Inertia%20(July%2020%202026)-10.5281%2Fzenodo.21461435-red)](https://doi.org/10.5281/zenodo.21461435)
[![Rubin Pre-Reg DOI](https://img.shields.io/badge/Pre--Registered%20a0(z)%20Gate%20vs%20Rubin%2FLSST%20SNe%20(July%2021%202026)-10.5281%2Fzenodo.21478568-black)](https://doi.org/10.5281/zenodo.21478568)
[![Corpus DOI](https://img.shields.io/badge/Code%20%26%20Data-10.5281%2Fzenodo.20576494-blue)](https://doi.org/10.5281/zenodo.20576494)

</details>


### DOI index — every deposit with its title (newest first; version DOI, concept DOI in brackets)

Plain text on purpose, so that titles and DOIs are searchable. Versions of one record share a concept DOI; cite the concept DOI for "latest".

| date | DOI | title | version |
|---|---|---|---|
| 2026-09-06 | [10.5281/zenodo.22559892](https://doi.org/10.5281/zenodo.22559892) (concept 22559891) | The Coefficient of the a0–Λ Relation: a Zero-Mode Theorem for Local MOND Actions, Two Failed Repairs, a Four-Form Reframing, and an H0 Degeneracy | v1 |
| 2026-09-06 | [10.5281/zenodo.22548669](https://doi.org/10.5281/zenodo.22548669) (concept 22544564) | A Ceiling Dark Matter Cannot Impose: the Bounded-Boost Theorem for MOND-Class Kernels, and What It Says About Galaxies and Clusters | v4 (v1 22544565, v2 22544996, v3 22548309) |
| 2026-09-05 | [10.5281/zenodo.22347632](https://doi.org/10.5281/zenodo.22347632) (concept 22347631) | The Filtered MOND Action: a Central Tidal Identity, Comparable-Mass Forces, a First Covariant Clock Action, and the Operator That Screens the Solar System | v1 |
| 2026-09-02 | [10.5281/zenodo.22261001](https://doi.org/10.5281/zenodo.22261001) (concept 22261000) | Crispy Fried Chicken Matching Theorem | v1 |
| 2026-09-02 | [10.5281/zenodo.22255522](https://doi.org/10.5281/zenodo.22255522) (concept 22253952) | The Retarded Nonlocal MOND Kernel Is Unstable on MOND Backgrounds: a Longitudinal Gradient Instability and a Deep-MOND Ghost Close the Nonlocal Door | v2 (v1 22253953) |
| 2026-09-02 | [10.5281/zenodo.22254075](https://doi.org/10.5281/zenodo.22254075) (concept 22242700) | The Aether-Scalar-Tensor Dark Sector Is a γ = 2 Polytrope: the Cluster Helmholtz Phase Is Its Mass, It Pins Dynamically, and It Fills About a Quarter of the Cluster Gap | v2 (v1 22242701; cosmology withdrawn) |
| 2026-08-28 | [10.5281/zenodo.22135510](https://doi.org/10.5281/zenodo.22135510) (concept 22135509) | An Obstruction Map for Relativistic MOND: the Conformal Lensing Barrier and the Cost of Its Repair | v1 |
| 2026-08-27 | [10.5281/zenodo.22133406](https://doi.org/10.5281/zenodo.22133406) (concept 22132651) | A Conditionally Closed Constraint-Defined MOND Theory with Two Tensor Degrees of Freedom: Hamiltonian Certification, Kernel-Agnostic Chassis, and Solar-System Gates | v2 (v1 22132652) |
| 2026-08-27 | [10.5281/zenodo.22132648](https://doi.org/10.5281/zenodo.22132648) (concept 22132647) | Carrier No-Go Theorems for Two-Degree-of-Freedom MOND: the F(A²) Class, the Auxiliary-Legendre Escape, and a Hamiltonian Audit of Causal Nonlocal MOND | v1 |
| 2026-08-21 | [10.5281/zenodo.22044021](https://doi.org/10.5281/zenodo.22044021) (concept 22036262) | The Amplitude Law: the obstruction is the interpolation function, not the carrier — and a monotone kernel escapes it with a0 untouched | v3 |
| 2026-08-14 | [10.5281/zenodo.21937976](https://doi.org/10.5281/zenodo.21937976) (concept 21937975) | The Registered Wide-Binary Target under a Local a0: A Conditional Charge Meter, and the EFE-Present Exact Two-Body Solve | v1 |
| 2026-08-14 | [10.5281/zenodo.21937958](https://doi.org/10.5281/zenodo.21937958) (concept 21935942) | Pinning AeST's Free Background Parameter: Q0 = 2.4e-3 – 1.5e-2 Mpc^-1 from Galaxy-Scale Phenomenology | v4 |
| 2026-08-12 | [10.5281/zenodo.21895046](https://doi.org/10.5281/zenodo.21895046) (concept 21863521) | The completion: a relativistic field theory carrying a0 = κ c √(G ρ_Λ) | v9 (dark sector excluded Sep 2026) |
| 2026-08-10 | [10.5281/zenodo.21865866](https://doi.org/10.5281/zenodo.21865866) (concept 21865865) | The Completion, For Everyone: the whole theory in plain words | v1 |
| 2026-07-30 | [10.5281/zenodo.21708842](https://doi.org/10.5281/zenodo.21708842) (concept 21707844) | Structural Theorems for de Sitter-Unruh Modified Inertia: What the First-Moment Closure Forbids | v2 |
| 2026-07-30 | [10.5281/zenodo.21702746](https://doi.org/10.5281/zenodo.21702746) (concept 21580092) | A Cubic Separation Law for Wide Binaries: an Exponent With No Free Parameters (the Gaia DR4 pre-registration) | v4 |
| 2026-07-29 | [10.5281/zenodo.21654272](https://doi.org/10.5281/zenodo.21654272) (concept 21654271) | When Is a Numerological Search Finished? An Exhaustive Null to Depth 10, and What Went Wrong With Our Own Stopping Rule | v2 (null) |
| 2026-07-21 | [10.5281/zenodo.21478568](https://doi.org/10.5281/zenodo.21478568) (concept 21478567) | A Pre-Registered a0(z) Gate for the Rubin/LSST Supernova Stream: Committing the Test Before the Data | v1 |
| 2026-07-20 | [10.5281/zenodo.21461435](https://doi.org/10.5281/zenodo.21461435) (concept 21461434) | Tidal Dwarf Galaxies as a Test of History-Dependent Inertia: How a Long-Memory Kernel Can Leave Young Dwarfs Near-Newtonian | v1 |
| 2026-07-20 | [10.5281/zenodo.21460161](https://doi.org/10.5281/zenodo.21460161) | Three Roads to the Cosmological-Constant Acceleration Scale: Dynamics, Weak-Lensing Geometry, and Expansion — and Why the Lensing Leg Is a Consistency Check | v1 |
| 2026-07-20 | [10.5281/zenodo.21458605](https://doi.org/10.5281/zenodo.21458605) | Which Acceleration Does Inertia Listen To? The Ignatiev High-Latitude Window as an Intra-Modified-Inertia Discriminator, and a Pre-Registered Exact Null | v1 |
| 2026-07-19 | [10.5281/zenodo.21440407](https://doi.org/10.5281/zenodo.21440407) | Does the Galaxy Acceleration Scale Track Cosmic Dark Energy? A Non-Circular Cross-Scale a0(z) Test of de Sitter-Unruh Modified Inertia | v2 |
| 2026-07-18 | [10.5281/zenodo.21421896](https://doi.org/10.5281/zenodo.21421896) (concept 21421895) | The Relational Velocity-Dispersion Spread: A Modified-Gravity-Impossible Signature of History-Dependent Inertia | v1 |
| 2026-07-18 | [10.5281/zenodo.21179351](https://doi.org/10.5281/zenodo.21179351) | No Pump-Free Corner: The Residual Doors of Covariant Modified Inertia, Computed — and a Pre-Registered Sign-Flip Signature | v3 |
| 2026-07-17 | [10.5281/zenodo.21419735](https://doi.org/10.5281/zenodo.21419735) (concept 21419734) | Reading the Cosmological Constant from Dwarf-Galaxy Rotation Curves: The a0-Line, Its Systematic Floor, and the de Sitter-Modified-Inertia Inversion | v1 |
| 2026-07-17 | [10.5281/zenodo.21418816](https://doi.org/10.5281/zenodo.21418816) (concept 21418815) | A Passivity Obstruction: Why a Derived a0 = cH_Λ/Z and Single-Metric Weak Lensing Cannot Coexist in de Sitter-Unruh Modified Inertia | v1 |
| 2026-07-17 | [10.5281/zenodo.21403470](https://doi.org/10.5281/zenodo.21403470) (concept 21403469) | A de Sitter-Unruh Modified-Inertia Field Theory, Complete Up To Its Constants: the Action, Its Radiative Protection, Its Equation Set, and Its Measurements | v1 |
| 2026-07-11 | [10.5281/zenodo.21312985](https://doi.org/10.5281/zenodo.21312985) (concept 21312984) | There Is No Dark Matter in Galaxies: a staked position (the bold statement inside is retracted; see RETRACTIONS.md) | v1 |
| 2026-07-11 | [10.5281/zenodo.21312654](https://doi.org/10.5281/zenodo.21312654) (concept 21312653) | A Cosmological-Constant Acceleration Scale, and the Dark-Matter-Free Theories It Points To (flagship; the MI arm is since closed) | v1 |
| 2026-07-10 | [10.5281/zenodo.21301058](https://doi.org/10.5281/zenodo.21301058) (concept 21301057) | A Covariant Action for the Elastic Dark-Energy Medium: the Verlinde-class anharmonic solid with the a0 = c²√(Λ/32π) displacement law | v1 |
| 2026-07-10 | [10.5281/zenodo.21300855](https://doi.org/10.5281/zenodo.21300855) (concept 21300854) | A Derived Response Cutoff for Elastic Dark-Energy Lensing: y_c = Z/2 from Verlinde's Own Entropy Budget (located, not detected) | v1 |
| 2026-07-08 | [10.5281/zenodo.21253644](https://doi.org/10.5281/zenodo.21253644) | A Written de Sitter-Unruh Modified-Inertia Action (v13): the passive-frame constraint structure closes | v13 |
| 2026-07-03 | [10.5281/zenodo.21175723](https://doi.org/10.5281/zenodo.21175723) (concept 21175722) | Scale Yes, Shape Yes, Sign No: A Sixth Theorem Closing the Finite-Time/Non-Stationary Corner of Covariant Modified Inertia | v1 |
| 2026-07-03 | [10.5281/zenodo.21152331](https://doi.org/10.5281/zenodo.21152331) (concept 21152330) | The Kernel That Builds Its Own Laser: Five Theorems on Covariant Modified Inertia, from Specification to Closure | v1 |
| 2026-07-03 | [10.5281/zenodo.21148494](https://doi.org/10.5281/zenodo.21148494) (concept 21148493) | The Fourth Horn: Local Pais-Uhlenbeck Modified Inertia Is Excluded by an Exceptional-Point Cap and a Frequency-Selection No-Go | v1 |
| 2026-07-02 | [10.5281/zenodo.21140507](https://doi.org/10.5281/zenodo.21140507) (concept 21140506) | Which a0? The Coefficient of the Radial-Acceleration Relation Under Full Nuisances: A Population-Split Answer | v1 |
| 2026-07-02 | [10.5281/zenodo.21139029](https://doi.org/10.5281/zenodo.21139029) (concept 21139028) | The Sign Premise Is a State Clause: Pumped Baths, the de Sitter Thermostat, and the Limits of Scale Without Law | v1 |
| 2026-07-02 | [10.5281/zenodo.21137568](https://doi.org/10.5281/zenodo.21137568) (concept 21137567) | A Fixed-Direction Ephemeris Test of s^TX at the CMB Apex: Pre-Registered Prediction, Analysis Recipe, and a Provisional Bound from Public Data | v1 |
| 2026-07-01 | [10.5281/zenodo.21110936](https://doi.org/10.5281/zenodo.21110936) (concept 21110935) | A Non-Monotonic a0(z) Signature: An Observational Discriminant Among Evolving-Acceleration-Scale Models in the DESI Era | v1 |
| 2026-07-01 | [10.5281/zenodo.21104820](https://doi.org/10.5281/zenodo.21104820) (concept 21104819) | Testing Modified Inertia in Galaxy Clusters: An Anisotropy-Dependent Mass Normalization | v1 |
| 2026-06-29 | [10.5281/zenodo.21016309](https://doi.org/10.5281/zenodo.21016309) (concept 21016308) | Scale Without Law: Why the de Sitter-Unruh Temperature Forces the MOND Acceleration but Not the Interpolation | v1 |
| 2026-06-28 | [10.5281/zenodo.20978308](https://doi.org/10.5281/zenodo.20978308) (concept 20978306) | A Fixed-Direction Solar-System Lorentz-Violation Target: the s̄^TX Boost-Dipole of de Sitter-Unruh Modified Inertia | v1 |
| 2026-06-27 | [10.5281/zenodo.20977421](https://doi.org/10.5281/zenodo.20977421) (concept 20977420) | A Growing Neutrino Mass from an Evolving MOND Scale: A de Sitter-Unruh Reading of the DESI Σm_ν Anomaly | v1 |
| 2026-06-21 | [10.5281/zenodo.20779562](https://doi.org/10.5281/zenodo.20779562) (concept 20779561) | The Galaxy-Cluster Residual in de Sitter-MOND: the Dark Sector Has the Mass, but a Density-Ordering Veto Forbids It from Being Galaxy-Safe and Cluster-Sufficient | v1 |
| 2026-06-20 | [10.5281/zenodo.20773004](https://doi.org/10.5281/zenodo.20773004) | Why Skordis and Złośnik Were Right: The MOND Acceleration Scale as a de Sitter-Unruh Manifestation of the Cosmological Constant | v1 |
| 2026-06-16 | [10.5281/zenodo.20721540](https://doi.org/10.5281/zenodo.20721540) (concept 20721539) | The MOND Acceleration Scale as a de Sitter Curvature Scale: Gauged SO(4,1) Gravity Reduces a0 = c²√(Λ/32π) to a Single Free Number | v1 |
| 2026-06-12 | [10.5281/zenodo.20670670](https://doi.org/10.5281/zenodo.20670670) (concept 20670669) | The Λ-Anchored Acceleration Scale a0 = c²√(Λ/32π): A Completed Falsification Map, Exact No-Go Results, and the Specification of the Unique Surviving Option | v1 |
| 2026-06-07 | [10.5281/zenodo.20576494](https://doi.org/10.5281/zenodo.20576494) (concept 20576493) | The Zimmerman Theory of Gravity — Research Corpus (code, data, and analysis) | 2026-06-06 |
| 2026-06-07 | [10.5281/zenodo.20576485](https://doi.org/10.5281/zenodo.20576485) (concept 20576484) | The Zimmerman Theory of Gravity (comprehensive edition; the TOE/SM claims in it are RETRACTED, see RETRACTIONS.md) | 2026-06-06 |

---

## Citation and licence

Cite the repository via [CITATION.cff](CITATION.cff) (GitHub's "Cite this repository" button), or
cite individual papers by their Zenodo DOIs above.

**Code: [AGPL-3.0](LICENSE). Prose, papers, figures, and scientific content: CC-BY-4.0.**
Details: [LICENSE.md](LICENSE.md). Author: Carl P. Zimmerman (Briar Creek Tech),
ORCID [0009-0008-3508-7982](https://orcid.org/0009-0008-3508-7982).
