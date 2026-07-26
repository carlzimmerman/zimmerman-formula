# A Cubic Gate-Opening Law for Wide Binaries: a Zero-Parameter Prediction in the Separation Window Current Analyses Exclude

**C. P. Zimmerman**
*Briar Creek Tech · Charlotte, NC · carl@briarcreektech.com*

*Version 2026-07-25 · Reproduced in full by `real_research/reviews/mi_wb_cubic_rise_2026.py` (10/10 checks, exit 0) and `real_research/reviews/mi_wb_gate_fork_2026.py` (11/11 checks, exit 0).*

---

## Abstract

Wide binaries at separations of a few kAU are the one regime where the weak-field force law is probed
below the MOND acceleration scale *a*₀ in a system containing negligible dark matter under any model,
so a collisionless-halo picture has essentially no free parameter with which to respond. Published
analyses of the Gaia catalogues nonetheless disagree: Chae (2023–2025) reports a boost, while Banik,
Pittordis & Sutherland (2024) report a Newtonian null, and the two differ by Δγ_v ≈ 0.174 — about
2.1× the entire boost predicted by a de Sitter–Unruh modified-inertia (MI) framework with
*a*₀ = *cH*_Λ/*Z*, *Z* = √(32π/3). An amplitude test cannot survive that spread. We point out that the
same framework, when its committed low-pass response gate *G*(ω) = (1 + *i*ω/ω_c)⁻¹ with
ω_c ∈ [1.782, 2.211] × 10⁻¹⁴ s⁻¹ is applied to the *orbital* frequency of the pair, makes a much
sharper prediction along a *shape* axis that has never been examined. A binary's orbital frequency
Ω = (GM/s³)^{1/2} exceeds ω_c throughout the analysed separation range, so the gate is shut and the
framework predicts a Newtonian result at 2–30 kAU. Because Ω falls as *s*^{−3/2}, the gate does not
open at a threshold but as **Re G → (ω_c²/GM)·s³**, giving
**γ_v(s) − 1 ≃ ½[ν(y_ext) − 1](ω_c²/GM)s³** with the exponent equal to 3 by derivation rather than by
fit and the amplitude fixed entirely by ω_c, the measured pair mass, and the measured Galactic external
field. There are no free parameters and the exponent is not adjustable. Three distinct mass powers
follow from the same closed form and are recovered numerically: the knee radius
*r*_gate = (GM/ω_c²)^{1/3} ∝ *M*^{0.3333}, the external-field plateau radius
*r*_efe = (GM/g_ext)^{1/2} ∝ *M*^{0.5000}, and the fixed-separation excess ∝ *M*^{−0.9935}. Every
published contaminant channel — chance alignment, unresolved tertiaries, close-binary contamination —
carries a fixed velocity scale and therefore rises as *s*^{1/2}; exponent 0.5 against 3.0. The
observational consequence is the point of this note: γ_v rises from 1.0125 at 30 kAU, the cut adopted
by every published analysis, to 1.0932 at 200 kAU, within the reach of the public El-Badry, Rix &
Heintz (2021) catalogue — a factor of 7 in excess, across a window excluded by a cut chosen to control
contamination, for reasons unrelated to this prediction. At the 30 kAU cut the predicted excess
(1.2 × 10⁻²) lies an order of magnitude below the inter-group systematic, so the conventional window
*cannot* test the framework; that is itself the result. **We state the costs plainly.** The prediction
is conditional on an unresolved question about the framework's own kernel: whether *K*(□_u) responds to
the acceleration *magnitude* |a|, which is constant on a circular orbit and would leave the gate open
(recovering the ungated γ_v ≈ 1.09), or acts as the linear operator its covariant form suggests, which
selects the gated branch computed here. The two branches lie 4.9–5.8σ apart in the framework's own
DR4 error model and the choice must be frozen before Gaia DR4. Feasibility is also unresolved:
contamination grows with separation too, and whether signal-to-contamination *improves* beyond 50 kAU
cannot be settled without the catalogue in hand. Finally, a confirmed *s*³ rise would establish a
*frequency* scale ω_c, not the coefficient *Z* — *Z* = 5.7888 and the conventional 2π = 6.2832 differ
by 7.87% and no arena examined here separates them — and it would constrain the weak-field force law,
not the matter content. *a*₀'s value, *Z*, the response sign, and ω_c remain postulated.

---

## 1. The framework, and the credit it owes

The kernel used throughout is the framework's own de Sitter–Unruh interpolation

$$\nu(y)=\sqrt{1+1/y},\qquad y=g_{\rm bar}/a_0,\qquad g_{\rm obs}^2-g_{\rm bar}^2=a_0\,g_{\rm bar},$$

with the acceleration scale tied to the cosmological constant,

$$a_0=\frac{cH_\Lambda}{Z}=c^2\sqrt{\frac{\Lambda}{32\pi}},\qquad Z=\sqrt{32\pi/3}=5.78881 .$$

**This kernel is not new and the identity is not new.** Both are Milgrom (1999, *Phys. Lett. A* **253**,
273), Eqs. (8)–(9), derived from the de Sitter–Unruh temperature difference, with coefficient
2*cH*_Λ — a ratio of exactly 2*Z* to the value used here. Milgrom (1999, 2015) and Smolin (2017, *Phys.
Rev. D* **96**, 083523) had already tied *a*₀ to Λ with a 2π coefficient. The distinctive content of
the present framework is the *coefficient* *cH*_Λ/*Z* together with a covariant modified-inertia
completion; priority for tying *a*₀ to Λ is not claimed, and cannot be, since *Z* and 2π differ by only
7.87%.

Numerically, *a*₀ = 9.36 × 10⁻¹¹ m s⁻² on the canonical (pure-Λ) footing and 1.13 × 10⁻¹⁰ m s⁻² on the
alternative *cH*₀/*Z* footing. **Both are carried through every number below**; they differ by ≈ 21%
and no result here depends on the choice.

The framework's modified-inertia realisation carries a low-pass response gate

$$G(\omega)=\frac{1}{1+i\omega/\omega_c},\qquad \operatorname{Re}G=|G|^2=\frac{1}{1+(\omega/\omega_c)^2},$$

with ω_c ∈ [1.782, 2.211] × 10⁻¹⁴ s⁻¹ on the canonical footing. The lower edge is forced by the
galactic rotation-curve fits; the upper edge by lunar laser ranging. **ω_c is anchored by no
independent theoretical argument** — a dimensional census of the framework's intrinsic scales places
every one of them 3.2–5.6 decades away — and it is the framework's most exposed quantity.

## 2. Why the gate is shut in the analysed window

A binary of total mass *M* at separation *s* presents an orbital frequency Ω = (GM/s³)^{1/2}. For
*M* = 1.5 M⊙ at *s* = 10 kAU,

$$\Omega = 2.44\times10^{-13}\ {\rm s^{-1}} = 11.0\times\omega_c^{\rm(upper)},$$

i.e. above the *entire* committed window. The gate is therefore shut, Re G = 0.005–0.008, and the
predicted velocity boost collapses to γ_v = 1.0004–1.0006 — within 0.04σ of Newton in the framework's
own DR4 error model (σ_γ = 0.0191 at *N* = 30 000).

Two radii govern the pair, and they run in opposite directions with separation:

$$r_{\rm efe}=\sqrt{GM/g_{\rm ext}}\quad(\text{external field takes over}),\qquad
r_{\rm gate}=(GM/\omega_c^2)^{1/3}\quad(\Omega=\omega_c).$$

Since Ω ∝ *s*^{−3/2} while *g* ∝ *s*^{−2}, one has *r*_gate > *r*_efe generically. For 1.5 M⊙ with
*g*_ext = *V*²/*R* = 1.726 × 10⁻¹⁰ m s⁻² (*V* = 233 km s⁻¹, *R* = 8.2 kpc): *r*_efe = 7.18 kAU and
*r*_gate = 49.5–57.3 kAU. **Between them the pair is already below *a*₀ but still gate-shut, and must
look Newtonian.**

**This does not damage the galactic case, which is the check that makes the gated branch admissible at
all.** Galactic orbital frequencies are Ω = *v*/*r*, some nine orders smaller. Across the Milky Way
solar circle and outer disk, dwarfs, low-surface-brightness disks, massive spirals, and the inner disk,
the largest value found is Ω/ω_c = 0.364, giving Re G ≥ 0.883. The gate is open in galaxies and shut in
wide binaries: the radial acceleration relation and the baryonic Tully–Fisher relation are untouched.
The gate makes wide binaries a *different regime*, not the same physics at smaller scale.

## 3. The cubic law

Deep in the gate-shut regime Ω ≫ ω_c, so Re G → (ω_c/Ω)², and substituting Ω = (GM/s³)^{1/2},

$$\boxed{\ \operatorname{Re}G \longrightarrow \frac{\omega_c^{2}}{GM}\,s^{3},\qquad
\gamma_v(s)-1 \simeq \tfrac{1}{2}\big[\nu(y_{\rm ext})-1\big]\frac{\omega_c^{2}}{GM}\,s^{3}\ }$$

saturating at ½[ν(*y*_ext) − 1] once Ω < ω_c. The local logarithmic slope
d ln(γ_v − 1)/d ln *s*, evaluated numerically, is **3.00** at 5 kAU and falls monotonically through the
knee to 0.06 once saturated.

The exponent is **derived, not fitted**, and is not adjustable. The amplitude contains ω_c (committed),
*M* (measured per pair), and *y*_ext = *g*_ext/*a*₀ (measured Galactic field, postulated *a*₀). **There
are no free parameters.**

Three mass powers follow from the same closed form, and are recovered numerically over 0.5–5.0 M⊙:

| quantity | measured | analytic |
|---|---|---|
| *r*_gate | *M*^{0.3333} | *M*^{1/3} |
| *r*_efe | *M*^{0.5000} | *M*^{1/2} |
| excess at fixed *s* = 10 kAU | *M*^{−0.9935} | *M*^{−1} |

The third is **asymptotic**, valid only where Re G ≪ 1. Measured at 30 kAU it is *M*^{−0.857}, not
*M*^{−1}, because low-mass pairs are by then near their own knee (*r*_gate shrinks as *M*^{1/3}). Any
fit must use the local slope rather than assume a global 1/*M*. We report both values rather than the
favourable one.

## 4. The discriminant

Every published contaminant channel carries a *fixed velocity scale* σ_v and therefore produces a
scaled relative velocity rising as *s*^{1/2}: chance alignment (El-Badry, Rix & Heintz 2021, via
*R*_chance_align), unresolved tertiaries and hierarchical systems (Peñarrubia 2021; Tyler, Green &
Goodwin 2023), and close-binary contamination. **Exponent 0.5 against 3.0** — a factor of six in
logarithmic slope. Contamination and signal therefore have *different* separation dependences, which
makes a joint fit for both well posed in principle. This is strictly stronger than the amplitude test,
which uses no shape information at all and is hostage to a 0.174 inter-group systematic amounting to
2.1× the entire ungated signal.

## 5. The window nobody has examined

Because the excess grows as *s*³, essentially the whole signal lies at large separation
(*M* = 1.5 M⊙, canonical footing, lower ω_c edge):

| *s* [kAU] | γ_v | note |
|---|---|---|
| 30 | 1.0125 | the cut used by every published analysis |
| 50 | 1.0392 | — |
| 100 | 1.0808 | — |
| 200 | 1.0932 | the public catalogue's actual reach |

The predicted excess grows by a **factor of 7** from the conventional cut to the catalogue limit. The
El-Badry, Rix & Heintz (2021, *MNRAS* **506**, 2269) Gaia DR3 catalogue extends to ≈ 1 pc = 206 kAU and
is public; the data are already taken. Analyses cut near 30 kAU because chance-alignment contamination
rises with separation — a motivation entirely unrelated to this prediction.

At the 30 kAU cut the predicted excess is 1.2 × 10⁻², an order of magnitude below the demonstrated
inter-group systematic of 0.174. **The conventional window cannot test this framework.** That is the
central observational claim of this note.

## 6. What is not claimed

- **The branch is unresolved, and this whole result is conditional on it.** *K*(□_u) is a *linear*
  operator, while |a| = (a^μ a_μ)^{1/2} is not a linear functional of the trajectory — a linear kernel
  cannot by itself sense the acceleration magnitude that ν(*y*) depends on. That obstruction points to
  the gated (AC) branch, but settling it requires reading the published action's contraction structure,
  which we have not done. On the ungated (DC) branch — where the kernel responds to |a|, constant on a
  circular orbit — this entire note is void and γ_v ≈ 1.09 stands instead. The branches lie 4.9–5.8σ
  apart in the framework's own DR4 error model. **The choice must be frozen before DR4 or the test is
  post hoc.** The same fork governs the framework's apparent Ġ/G floor, since the lunar mean motion
  exceeds ω_c by ≈ 1.5 × 10⁸.
- **Feasibility beyond 50 kAU is unresolved and may be fatal to a DR3 test.** Contamination also grows
  with separation. Whether signal-to-contamination *improves* beyond 50 kAU is an empirical question
  that cannot be answered without the catalogue in hand. If it does not, this prediction waits for
  DR4's astrometry and higher *N* rather than being testable now. We state this rather than assume the
  favourable case.
- **A confirmed *s*³ rise would not test *Z*.** It would establish a frequency scale ω_c. The
  coefficient *Z* = 5.7888 and the conventional 2π = 6.2832 differ by 7.87%, both lie inside the ±16%
  empirical *a*₀ box, and no arena examined here separates them. Separately and against interest:
  matching Chae (2024b)'s central γ on this framework's own kernel would require *a*₀ ≈ 1.9× the
  canonical value, which at face value disfavours the Λ-tied coefficient specifically.
- **Nothing here bears on whether dark matter exists.** A wide-binary result constrains the weak-field
  *force law*, not the matter content. γ_v = 1 is Newton's prediction, shared by ΛCDM, by this
  framework's own gated branch, and by hybrid modified-force-plus-particle models.
- ***a*₀'s value, *Z*, the response sign, and ω_c are postulated, not derived.**

## 7. Falsification

The prediction fails if, in a contamination-controlled sample beyond ≈ 50 kAU, the scaled relative
velocity excess is (i) absent, (ii) present with a logarithmic slope inconsistent with 3 in the
gate-shut regime, (iii) present but without the knee moving as *M*^{1/3}, or (iv) present with an
amplitude inconsistent with ω_c² /*GM* on both footings and both window edges. Any of these kills the
gated branch. A Newtonian result *inside* 30 kAU falsifies nothing, on either branch — which is
precisely the defect in the current pre-registration that this note exists to correct.

## 8. Reproducibility

Every number is printed by two committed scripts, both `exit 0`, with no hard-coded verdicts and both
footings and both ω_c edges carried throughout:

- `real_research/reviews/mi_wb_gate_fork_2026.py` — the DC/AC fork, the gate-shut computation, the
  galactic-safety check, and the dead zone (11/11 checks).
- `real_research/reviews/mi_wb_cubic_rise_2026.py` — the *s*³ law, the slope measurement, the three
  mass exponents, the profile table, and the feasibility caveat (10/10 checks).

Two assertions failed their own checks on first run and were corrected in place rather than patched:
an overstated 200-vs-30 kAU excess ratio (claimed >10×, actually 7×) and an overstated global 1/*M*
scaling (actually *M*^{−0.857} at 30 kAU, asymptotic only). Both corrections are recorded in the
scripts and in the commit history.

---

## References

Banik, I., Pittordis, C., Sutherland, W., et al. 2024, *MNRAS* — wide-binary Newtonian null.
Bekenstein, J. D., & Milgrom, M. 1984, *ApJ* **286**, 7.
Chae, K.-H. 2023–2025, *ApJ* — wide-binary boost claims.
El-Badry, K., Rix, H.-W., & Heintz, T. M. 2021, *MNRAS* **506**, 2269 — the public Gaia DR3 catalogue.
Milgrom, M. 1983, *ApJ* **270**, 365.
Milgrom, M. 1999, *Phys. Lett. A* **253**, 273 — Eqs. (8)–(9): the kernel and identity used here.
Milgrom, M. 2015, *Can. J. Phys.* **93**, 107.
Peñarrubia, J. 2021 — wide-binary contamination.
Smolin, L. 2017, *Phys. Rev. D* **96**, 083523.
Tyler, J., Green, A., & Goodwin, S. 2023 — hierarchical contamination.
