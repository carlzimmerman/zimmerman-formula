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

**Standing 2026-09-13 (rev. 20) — ★ the interpolating function is a photocount formula, the clock provably cannot derive κ, and the exponent is an empirical quantity.** Yesterday the galaxies selected the integer with nothing fitted. Today's question was *why that integer*, and the honest answer is that no mathematical reason was found and four of the routes to one are now closed. **★ THE NO-GO** ([L236](fable_independent_2026/L236_can_the_two_tracks_merge.py), 7/7): a cuscuton clock's own field equation fixes **V′(τ) = −3HU**, so a vanishing potential forces a vanishing expansion rate — **any cuscuton clock in an expanding universe REQUIRES a potential.** And a potential is exactly the free additive constant the zero-mode no-go needs in order to bite, so the twelve-gate relativistic construction sits *inside* the class that no-go covers and **provably cannot derive κ**. The two tracks also cannot be merged: they assign U = 3.68e-25 eV⁴ and U = 2.52e-11 eV⁴ to the same coefficient, a ratio of **6.9e13**, and forcing agreement needs a margin of 2.58 where the margin is 1 − μ and cannot exceed one. **The architecture is a genuine fork and one horn's failure is now a theorem.** **★ THE IDENTIFICATION** ([L237](fable_independent_2026/L237_the_mandel_reading.py)): the family is *exactly* **Mandel's n-mode photocount formula** — for n independent thermal modes of mean occupancy Y, μ_n is the probability that at least one quantum is present (Monte Carlo 0.88914 against the closed form 0.88889). Equivalently it is one minus a **Tsallis q-exponential with q = 1 + 1/n**, the exponential kernel being the infinite-mode limit. That explains why the exponent is an **integer** — it is a *mode count* — without fixing its value, and sharpens the question to: why does the vacuum present exactly **two** modes to an acceleration? ⚠️ **AND THE ROUTES TO AN ANSWER CLOSED, ONE BY ONE.** The modes are **not Unruh modes**: a fixed-frequency thermal occupancy gives 3.72e-44 where the reading needs 0.01 — **41 orders**, in the only regime MOND is about ([L238](fable_independent_2026/L238_the_two_modes.py)); what survives is that the occupancy is exactly *linear*, an equipartition statement rather than a Boltzmann one, and that is specifically a **three-dimensional** fact. Twelve **pre-registered** mathematical criteria scatter over three different members with **n = 1 the modal choice** (5 of 9), and the only two picking n = 2 are the same fact twice and pick it as a **boundary**, not an optimum ([L235](fable_independent_2026/L235_which_integer_does_the_maths_pick.py)). EFT **positivity is inapplicable** — the kinetic matrix degenerates where μ(0) = 0, so there is no propagator and no S-matrix — and granting it anyway the one scale-free invariant **9(n+1)/(16n)** is continuous and monotone, so no bound can ever select an integer; **causality is saturated identically**, c_∥² → 2 deep for every kernel ([eft01](hunt_2026/eft01_positivity_causality_mu_family_2026.py)). The **d-dimensional generalisation** μ_n^(d)(Y) = 1 − (1 + Y^(d−2))^(−n) exists and is forced, carrying Milgrom's conformally invariant deep power — **but it closes the route rather than opening it**: the count enters the deep limit as a *multiplicative prefactor* and cannot change a power, so it is **dimensionally inert** and all four candidate counts stay degenerate ([L239](fable_independent_2026/L239_d_dimensional.py), 7/7). **The conclusion, stated plainly: the exponent is an empirical quantity.** The curves prefer n = 2 over n = 1 by 0.016 dex; sharpening that means beating the relation's ~0.045 dex intrinsic scatter, which needs better mass-to-light ratios and distances rather than better theory. After these closures this is reported as *the result*, not as a placeholder for a derivation. Lean **160 theorems, zero `sorry`**; published as [DOI 10.5281/zenodo.22735193](https://doi.org/10.5281/zenodo.22735193). **Limits:** the clock no-go is written at constant U and the τ-dependent case is not computed; the photocount identification is an *identification* and nothing here shows the vacuum response **is** such a count; twelve criteria is not exhaustive; and this concerns one coefficient and is not a verdict on any construction.

**Standing 2026-09-12 (rev. 19) — ★ κ = ½ is no longer a fit: with the acceleration scale removed as a free parameter, 155 real rotation curves select it.** The κ no-go was re-examined and found **far more general than it had been quoted**: for any FREE interpolating function, shifting it by a constant leaves its derivative untouched and moves only the vacuum energy, so the normalisation is a zero mode — **regardless of field content or whether Λ appears explicitly** ([L226](fable_independent_2026/L226_kappa_and_the_free_function.py)). Searching a wider action class is therefore wasted effort. But the same argument names the escape: **the obstruction is the freedom of the FUNCTION.** **The principle: there is no independent a₀.** Put the interpolating function's argument in units of the dark-energy acceleration s = c√(Gρ_Λ) and a₀ becomes an **output**, with **κ = 1/c** where c is the function's deep-MOND slope ([L230](fable_independent_2026/L230_one_number.py)). Every standard parameter-free shape has slope 1, predicting κ = 1 — **excluded at 7–10σ by this programme's own measurements.** **The curve:** μ_n(Y) = 1 − (1+Y)^{−n} has slope exactly n, so the slope is an **integer count, not a dial**, with 1 − μ_n = (1 − μ₁)^n ([L231](fable_independent_2026/L231_the_curve.py)). An independent literature search finds it is **not a named interpolating function** and is genuinely distinct from the standard n-family. **★ THE TEST** ([L232](fable_independent_2026/L232_sparc_parameter_free.py), 6/6): each integer is a complete prediction of the radial acceleration relation with **nothing fitted at all**. On **155 of 175 SPARC curves, 2788 points**, the data select **n = 2, i.e. κ = ½**, on both density conventions — 0.1502/0.1438 dex against 0.1660/0.1846 for n = 1. ν_RAR *fitted* at a *fitted* scale gives 0.1453 on the same data. **And the two registered a₀ footings are exactly n = 2 on the two density conventions, to 0.02% and 0.33%.** **Predictions** ([L233](fable_independent_2026/L233_predictions.py)): a **power-law** approach to Newton leaving 5.8e-16 m/s² at Saturn, 17× under Cassini, where the fitted kernel predicts *zero*; a wide-binary boost differing by up to 0.28 in γ_v (the frozen preregistration is untouched); a Tully-Fisher zero point with no freedom; and **a₀ inheriting the dark energy's equation of state** — flat for w = −1, 1.31× at z = 5 for w = −0.9, so measuring a₀ at high z measures w. ⚠️ **WE DO NOT DERIVE THE INTEGER** ([L234](fable_independent_2026/L234_structural_search.py)). Four structural angles searched, none fixes it, and **two point elsewhere**: the algebraically clean member is n = 3, degree-of-freedom counting wants 3/2, and the AQUAL–QUMOND duality favours n = 1. **The data select the exponent; the mathematics does not.** No published work derives any interpolating exponent. Lean **158 theorems, zero `sorry`**; published as [DOI 10.5281/zenodo.22731370](https://doi.org/10.5281/zenodo.22731370). Single-field AQUAL, fixed mass-to-light, **an rms comparison and not a likelihood**.

**Standing 2026-09-12 (rev. 18) — the clock rate is a conserved charge, the equation of state is forced two orders tighter, and the whole board is run end to end for the first time.** The clock rate rev. 17 left unexplained does not need explaining. The closure's two kinetic coefficients descend from a **single logarithmic function** whose pole is a **speed limit**, with 1/m_rel its Lorentz factor; and since every term of the action carries χ only through derivatives, the shift symmetry is exact and that Lorentz factor is its **conserved Noether charge** ([L217](fable_independent_2026/L217_where_the_clock_rate_comes_from.py)). Set once and protected, which makes 1e7 technically natural rather than tuned. **The cost:** MOND's own matter coupling breaks that symmetry, drives the charge linearly in cosmic time and so drives a₀ **down** by 12.4% since z = 5 against the 1% the derived flat law allows. The breaking rate is independent of the clock rate, so it cannot be tuned away, and holding the flat law forces **w ≲ 5.7e-7** — 177× tighter than the acoustic bound, and the published prediction band shrinks by that factor (its sign survives). Criticality survives there, beating dilution 17× at the forest epoch and running from z ≈ 940 down, and supplies an exact **operating condition w > 2/κ²** ([L218](fable_independent_2026/L218_criticality_at_the_tightened_w.py)). **And the board now runs end to end** ([L223](fable_independent_2026/L223_end_to_end.py), 11/11): two gates fix two numbers, **all twelve gates pass simultaneously**, the four at unit margin are exactly the four parameters put on their boundaries on purpose, and two combinations derived in different lanes from different physics agree to **one part in 1e7** with the residual exactly s₀/(s₀−1). The run also exposed a coupling never stated: the flat-a₀ gate constrains the **product** Cw, so MOND interpolation depth and the equation of state **trade off**; honouring it, the allowed set has a genuine **interior** with every gate clearing by at least 1.9. **Seven quantities fixed, five free, two of those bounded.** **Two of our own results were overturned on the way and are reported in the paper as loudly as the standing ones:** a claimed naturalness pincer ([L220](fable_independent_2026/L220_radiative_stability.py)) whose radiative estimate omitted the sound-speed factor in the mode sum, and the cutoff it rested on ([L219](fable_independent_2026/L219_the_uv_cutoff.py)) whose sound speed dropped the cuscuton's gradient contribution — **that cutoff number must not be quoted until recomputed** ([L221](fable_independent_2026/L221_the_cutoff_step.py), [L222](fable_independent_2026/L222_auditing_l221.py)). What survives needs no loop estimate: the conserved charge makes a small margin a *large charge* rather than a cancellation, with square-root sensitivity. Lean **147 theorems, zero `sorry`**; published as [DOI 10.5281/zenodo.22731066](https://doi.org/10.5281/zenodo.22731066). **This is a construction closed on its own gates, not a complete theory.** Every gate is an analytic estimate rather than a likelihood: **there is no Boltzmann run with this sector present, no N-body, no loop computed anywhere, and no likelihood.** The board says the construction is not obviously inconsistent, not that it fits the data. And κ = ½ remains fitted and provably underivable by this class of actions — a theorem of this programme, and the reason a complete theory is not available on this action however long one pushes.

**Standing 2026-09-12 (rev. 17) — the last gate computed: the solar system is an inequality on the rate of cosmic time, and it wants ten million.** Rev. 16 left the solar-system gate as one number, an alignment of 4.6 m/s between the clock's frame and the local matter frame, uncomputed. [L216](fable_independent_2026/L216_clock_alignment.py) computes it, 8/8, and the answer is a requirement rather than a verdict. Four things fall out before the number. **There is no escape by tuning:** writing the matter metric with independent conformal and disformal strengths and demanding γ_PPN = 1 forces **b = 2a exactly**, so the operator that fixes light bending *is* the operator that generates the preferred-frame effect. **The dragging is a constraint, not a response:** the cuscuton's coefficient for the squared time derivative is **exactly zero**, so the clock propagates nothing and its tilt solves an elliptic boundary-value problem against the cosmic frame at infinity. **It cannot be bought:** the stiffness is the gradient function at the *local* invariant, W = f_s²GM²/(8πs₀r⁴), and ∂W/∂λ = ∂W/∂β = 0 — neither free coefficient can improve the drag, leaving the clock rate as the only handle. **And the gain is a property of the theory, not the object:** D(R) = 24s₀/f_s, independent of the star's mass and radius entirely, with the falling stiffness making the exterior tilt decay as r^{−(√17−1)/2} = r^{−1.562} instead of the r^{−3} of a constant-stiffness dipole. Both help and neither suffices: at Earth's orbit the drag is **0.011** at the minimum clock rate and the residual misses the bound by **7.9e4**. Inverting, **s₀ ≳ 1.5e7**. **The solar system does not exclude this construction. It demands a clock running about ten million times proper time.** That is the **third independent constraint on s₀ and the third pointing the same way** — the clock identity, positivity of the sector's energy (s₀ ≥ 2), and now the solar system — which is a real convergence. But the first two want order unity and nothing here explains a number seven orders larger, so it is recorded as a requirement, not a derivation. The price is computed too: the margin falls to m_rel = 6.8e-12 and the scalar's kinetic coefficient rises to P_X/d = 1.5e11. Nothing computed contradicts that, because every gate of rev. 16 depends on w and not on s₀ — but a kinetic coefficient eleven orders above its neighbour is a **strong-coupling question this lane states and does not answer**. Lean file **128 theorems, zero `sorry`**; published as [DOI 10.5281/zenodo.22729935](https://doi.org/10.5281/zenodo.22729935). **This is not a complete theory of gravity.** Open, and stated as open: the origin of that clock rate, the strong-coupling question above, and κ = ½, still fitted and provably underivable by this class of actions.

**Standing 2026-09-12 (rev. 16) — the obstruction removed, the MOND scale derived, and the solar system reduced to one number.** Rev. 15 recorded that the action produces a dark sector and no force law. The reason is simpler than the exponents it gave: matter enters only through minimally coupled radiation and baryon terms, so the variation of the matter action with respect to the scalar vanishes identically ([L211](fable_independent_2026/L211_three_corrections.py)). An external audit also reversed the health condition, which is **U > 4dℓ**, and corrected the interpolating exponent from 0.470 to 0.997 — the first number had been measured against the Newtonian rather than the true acceleration. Adding a matter coupling is what gives MOND, and the obstruction was that the clock and scalar mix. **That mixing vanishes exactly on the locus W₀ = U − 2γq̄²q̄′ = 0** ([L212](fable_independent_2026/L212_decoupling_branch.py)), a condition on coefficients the action already has. A first pass priced that locus at a cubic coupling eight orders too large, and **that pricing was wrong**: it held the clock coefficient fixed, and with ρ = U/m_rel imposed the factor of w cancels identically ([L213](fable_independent_2026/L213_branch_solved_and_the_board.py), 12/12). What the locus fixes is a **ratio**, γq̄³H/ρ = −1/[6(s₀−1)], of magnitude at most 1/6, and the operator's weight against gravity is Ω/[6(s₀−1)] ≤ **0.044** — so every result derived at vanishing coupling survives there to about four percent. The locus also **forces two previously free quantities**: positivity requires **s₀ ≥ 2**, hence **m_rel ≤ w ≲ 1e-4**, the margin sitting below the equation of state rather than above it. Extending the action by the Y^{3/2} operator rev. 15 named as missing, plus a leading-order coupling, the quasi-static gradient sector **yields deep MOND outright** (d log g/d log r = −1, d log g/d log M = +1/2) and **fixes the scale**, a₀ = λ³/(12πGβs₀), mass-independent and *falling with the clock rate* ([L214](fable_independent_2026/L214_force_law_on_the_branch.py), 8/8). The one conflict is a single coefficient pulled both ways and it resolves into one inequality, C = 2kq̄²/U ≳ 1e3, whose derived exponents cancel exactly — **C is a constant of the motion**, imposed once and holding for all time. Finally, coupling matter **disformally along the clock's own timelike direction** shifts both weak-field potentials equally, so **γ_PPN = 1 exactly, with no added vector field** — the mechanism TeVeS and AeST need a whole extra dynamical field for, obtained here because the cuscuton already supplies the direction and propagates nothing ([L215](fable_independent_2026/L215_solar_system_on_the_branch.py), 6/6). Boosted, the same term gives α₁ = 8f_s, five orders over the bound **unless local matter drags the clock to within 4.6 m/s**. Lean file **124 theorems, zero `sorry`**, axioms ⊆ {propext, Classical.choice, Quot.sound}; published as [DOI 10.5281/zenodo.22729429](https://doi.org/10.5281/zenodo.22729429). **This is not a complete theory of gravity.** Two things are open and are stated as open: that 4.6 m/s clock alignment, which no lane has computed and which an earlier lane measuring a dragged cuscuton recorded as a kill; and κ = ½, still fitted and provably underivable by this class of actions.

**Standing 2026-09-12 (rev. 15) — the scope of yesterday's gate board, corrected.** Rev. 14 reported a mechanism passing nine gates. That stands, and its scope is narrower than it reads. Every derivation behind it set the cubic coupling to zero, and that cubic is the only Galileon-type operator in the action. Restoring it ([L206](fable_independent_2026/L206_cubic_restored.py), [DOI 10.5281/zenodo.22728946](https://doi.org/10.5281/zenodo.22728946)) gives two results. **The action cannot produce flat rotation curves.** Its two gradient operators give curves rising as r^{1/6} and r^{1/4}, flat requires r⁰, both exponents are strictly positive and no mixture of them reaches zero; what flat curves need is a Y^{3/2} operator the action does not contain. **So the nine gates are dark-matter gates**, and the chain from [L192](fable_independent_2026/L192_gradient_criticality.py) to [L204](fable_independent_2026/L204_boosted_metric_expansion.py) derives a cold, clustering dark sector and the rate of cosmic time from a clock, with the force law still put in by hand. Two things survive that correction intact. The clock identity, now certified in Lean (114 theorems): **the clock's rate relative to proper time is not an input but the dark sector's own pressure divided by the margin, and time runs fast exactly when that pressure is positive.** And the prediction that follows: **a positive dark matter equation of state, 0 < w_dm ≲ 1e-4, where ΛCDM says exactly zero**, testable in existing data. **And the no-go is a specification.** Any action meant to do both jobs must carry a Y^{3/2} operator alongside the clock, with U ∝ a^{−3(1+w)}, d ∝ a^{−3(1−w)}, q ∝ a^{−3w}, s₀ − 1 = w/m_rel, 4dℓ > U and 0 < w ≲ 1e-4. That is a far narrower target than this programme began with, and it is where the work goes next.

**Standing 2026-09-12 (rev. 14) — one mechanism has now been walked through nine gates, and what that does and does not mean.** The mechanism: a sector with a little positive pressure makes the clock run faster than proper time; that makes it gradient-unstable; its own MOND nonlinearity cures the instability at a finite gradient whose marginal state has zero sound speed **and** isotropic stress; the back-reaction parks it there; and the coefficient history doing all of it is explicit, because the field equations **force** s₀ − 1 = w/m_rel and Friedmann closes it in closed form. Depletion from galaxies is supplied separately by clock-frame kicks. **The board:** stability ✓ · Lyman-α forest ✓ · CMB third peak ✓ (0.991 vs ΛCDM 0.992) · galaxy lensing and rotation curves ✓ *only in combination with the depletion* · S₈ ✓ and non-discriminating · NGC 1052-DF2 in tension at the far distance only, with named escapes · depletion trigger resolved to a condition · matter budget ✓ · post-Newtonian, static ✓ and **preferred-frame ✓** ([DOI 10.5281/zenodo.22728789](https://doi.org/10.5281/zenodo.22728789)). **One prediction came out of it that data can test now:** a positive dark matter equation of state, 0 < w_dm ≲ 1e-4, where ΛCDM says exactly zero. **What this is not.** It is a mechanism with a certified algebraic core and a gate board, not a complete theory, and five things are assumed rather than derived: the amount of the sector (Friedmann is one equation for two dark unknowns), the depletion trigger as a structure separate from the coefficient family, the coefficient closure itself, the preferred-frame leakage estimate (no post-Newtonian parameter is extracted from a full metric expansion), and κ = ½, still fitted and provably underivable by this class of actions. Each of those is a place a referee would push, and each should be pushed.

**Standing 2026-09-12 (rev. 13) — one mechanism, seven gates walked, and a prediction that existing data can test.** The chain runs: a sector with a little positive pressure makes the clock run faster than proper time; that makes it gradient-unstable; its own MOND nonlinearity cures the instability at a finite gradient whose marginal state has zero sound speed **and** isotropic stress; the back-reaction parks it there with a residual (H/k_max)²; and the coefficient history doing all this is now explicit, because the clock equation with current and energy conservation **forces** s₀ − 1 = w/m_rel and Friedmann closes it in closed form ([DOI 10.5281/zenodo.22728545](https://doi.org/10.5281/zenodo.22728545)). **The gate board for this mechanism:** stability ✓, Lyman-α forest ✓, CMB third peak ✓ ([L195](fable_independent_2026/L195_cmb_gate_self_critical.py), 0.991 against ΛCDM's 0.992), galaxy lensing and rotation curves ✓ but only in combination with the depletion mechanism ([L196](fable_independent_2026/L196_lensing_gate.py)), S₈ ✓ and non-discriminating ([L197](fable_independent_2026/L197_s8_gate.py), the kernel's lift and the kicks' suppression cancel), NGC 1052-DF2 in tension at the far distance only ([L198](fable_independent_2026/L198_df2_external_field.py)), and the depletion trigger resolved to a condition rather than a free function ([L199](fable_independent_2026/L199_trigger_sharpness.py)). **The new prediction: a positive dark matter equation of state, 0 < w_dm ≲ 1e-4, where ΛCDM says exactly zero.** It follows from criticality requiring w > 0 and the acoustic scale bounding it from above, and it is within reach of existing data. Lean file 111 theorems, zero `sorry`. **Still not derived, and stated plainly:** the amount of the sector (Friedmann is one equation for two dark unknowns), the depletion trigger as a structure independent of the coefficient family, the matter budget and the post-Newtonian limit for this sector, and κ = ½, which remains fitted and provably underivable by this class of actions.

**Standing 2026-09-12 (rev. 12) — one mechanism now runs end to end, and the gates it has not faced are named.** The chain is closed on its own terms and each link is a committed script: a clock running faster than proper time makes the sector gradient-unstable ([DOI 10.5281/zenodo.22717950](https://doi.org/10.5281/zenodo.22717950)); its own MOND nonlinearity cures that instability at a finite gradient ([DOI 10.5281/zenodo.22727111](https://doi.org/10.5281/zenodo.22727111)); the marginal state there has zero sound speed **and** isotropic stress, by an exact off-shell stress degeneracy, which is what a clustering cold component is; and the back-reaction drives the sector to that state and holds it, with a residual sound speed of (H/k_max)² ([L194](fable_independent_2026/L194_tracking_dynamics.py), [DOI 10.5281/zenodo.22727860](https://doi.org/10.5281/zenodo.22727860)). The Lyman-α gate is met once the instability reaches sub-Mpc scales, and **nothing is tuned** — what used to require the logarithm margin at one part in 1e8 is now a consequence of dynamics. Lean file 111 theorems, zero `sorry`. **This is a mechanism with a certified algebraic core, not a complete theory.** It has faced the forest and stability only. Still open, in the order that decides it: the CMB acoustic peaks with this sector present; galaxy-galaxy lensing and S₈; the amount of the sector and the late-time matter budget; the post-Newtonian limit; and the fact that the candidate's own coefficient history still fails the forest on its early branch, where the clock runs slow and the criticality never operates — so a history with a fast clock throughout must be exhibited. A search harness for exactly that is in [hermes_push/search](hermes_push/search/). Two costs stand on the record: the residual coldness is ultraviolet-sensitive, and κ = ½ remains fitted and provably underivable by this class of actions.

**Standing 2026-09-12 (rev. 11) — the instability we recorded as fatal is the mechanism.** The clock stability theorem ([DOI 10.5281/zenodo.22717950](https://doi.org/10.5281/zenodo.22717950)) showed the candidate's clock sector is gradient-unstable whenever the clock runs faster than proper time, and that derivation evaluated the sound speed at **zero field gradient**. Carried through with the background gradient ([L192](fable_independent_2026/L192_gradient_criticality.py)), the MOND sector cures its own instability: c_s² rises monotonically with the gradient invariant and crosses zero at a unique Y*, which is a **two-sided attractor** whose state has c_s² = 0 exactly. The same surface is an exact off-shell stress degeneracy, det(T^mixed_tx − L·I) = −s₀b²W·N ([L193](fable_independent_2026/L193_stress_degeneracy.py), verified independently of a concurrent audit), so there the stress becomes a perfect fluid: **isotropic stress and non-propagating perturbations arrive together on one surface fixed by the action** — which is what a clustering cold component is, obtained by criticality rather than by tuning the logarithm margin to 1e-8. Lean file now **111 theorems, zero `sorry`**; published as [DOI 10.5281/zenodo.22727111](https://doi.org/10.5281/zenodo.22727111). Independently, the depletion question advanced: the ledger's mass dependence is pure geometry ([DOI 10.5281/zenodo.22718357](https://doi.org/10.5281/zenodo.22718357)), density-gated depletion is excluded by galaxy-galaxy lensing for any density-monotone rate ([L188](fable_independent_2026/L188_density_gated_depletion.py), Lean), and a clock-frame-kick mechanism reproduces the ledger to 22% under an orbit integration while predicting a **universal galaxy-scale dark fraction** ([L191](fable_independent_2026/L191_c003_orbit_integration.py)). **Still owed, and now the highest-value calculation in the programme:** the tracking dynamics — the Lyman-α bound requires the gradient to follow Y* to about one part in a million, and whether the back-reaction achieves that is not established. A parameter-space search harness for coefficient histories is in [hermes_push/search](hermes_push/search/).

**Standing 2026-09-11 (rev. 10) — the recombination wall confirmed in a full Boltzmann code; the lead candidate's clock sector solved to a theorem.** A mean-field MOND kernel patched into CLASS 3.3.4.0 ([L183](fable_independent_2026/L183_class_kernel_recombination.py), reusable patch in [L183_class_mond_kernel/](fable_independent_2026/L183_class_mond_kernel/)) does not restore the third peak without cold matter (restoration −0.03 → −0.00 with the consistent metric derivative, [L184](fable_independent_2026/L184_class_kernel_consistent_derivative.py)) and adds an ISW-borne low-ℓ excess of ×578/×785 at ℓ = 30 over ΛCDM (the kernel's intrinsic ISW rate (ℋ/2)·u/(e^u−1) is Lean-certified): the kernel on linear scales is excluded at the CMB on both footings, and the clustering cold component at recombination is required either way. For the lead field-theory candidate ([DOI 10.5281/zenodo.22699828](https://doi.org/10.5281/zenodo.22699828)), whose same-action cosmological bridge now reaches a radiation-majority branch, the clock sector's sub-horizon sound speed was derived and Lean-certified — **the clock stability theorem**, c_s² = (1−s₀)·m_rel/(2−m_rel), stable iff the clock runs no faster than proper time ([L185](fable_independent_2026/L185_astra_clock_sound_speed.py), [L186](fable_independent_2026/L186_clock_stability_theorem.py), [DOI 10.5281/zenodo.22717950](https://doi.org/10.5281/zenodo.22717950)): the candidate is gradient-unstable on its own branch for z ≲ 2.4, its early branch would pass the third peak but misses the forest by 1e5 in c_s², and no sound speed can supply the galaxy depletion — the required host-mass-dependent dark fraction must be dynamical, and the dynamical routes computed so far are pincered. Lean file now **105 theorems, zero `sorry`**. The depletion question itself was then attacked ([L187](fable_independent_2026/L187_late_puffy_component_topdown.py), [DOI 10.5281/zenodo.22718357](https://doi.org/10.5281/zenodo.22718357)): the ledger's mass dependence is pure geometry (one universal concentration c* = 0.4 at the ledger's three radii), which needs a component with no structure below ~Mpc, and nonlinear top-down fragmentation does not put the forest power back (0.45 of ΛCDM at k = 5 h/Mpc, z = 2.2 for k_cut = 2) — so pressure, kinetic removal and late collapse are each computed to failure. Open, as before: a depletion mechanism that is neither acoustic nor decay/kick; nonlinear top-down fragmentation; emergent MOND from dark matter; the action-level origin of the kernel's ambient acceleration.

**Standing 2026-09-10 (rev. 9) — the map is complete; the mechanism is not.** An independent gate programme ([`fable_independent_2026/`](fable_independent_2026/), lanes L129–L178, [FINDINGS.md](fable_independent_2026/FINDINGS.md)) took every way of making MOND relativistic on the de Sitter-locked a₀ through thirteen gates with committed scripts and a Lean 4 file of **100 theorems, zero `sorry`** ([Mondlean.lean](fable_independent_2026/lean_2026/Mondlean.lean)). **Certified necessity** ([L166](fable_independent_2026/FINDINGS.md)): any theory on these equations passing galaxies, CMB, Lyman-α and PPN together must carry a dark fraction that *rises with host mass* — the CMB third peak needs ≥ 0.988 of a clustering cold budget at recombination ([L129](fable_independent_2026/L129_smooth_dust_third_peak_boltzmann.py), [L165](fable_independent_2026/L165_camb_cross_check.py)), spirals tolerate ≤ 0.105, clusters need 0.58, the Milky Way sits at 0.14 (Gaia DR3), the trend is f ∝ M^0.16 ([L172](fable_independent_2026/L172_mw_outer_curve_and_fgal_ledger.py)) — plus a non-barotropic effective fluid and a locally screened preferred-frame source. **The single-metric kinetic-mixing action** ([SINGLE_METRIC_ACTION.md](fable_independent_2026/SINGLE_METRIC_ACTION.md), [L169](fable_independent_2026/L169_single_metric_action.py)) is written and reduced: its static limit *derives* the double-filter screening the wide-binary work had assumed (transmission 1 − e^{−x}(1 + x + x²/2), γ safe at Cassini, 0-DOF smoothing sector, all Lean-certified), and it is **certified to fail** cosmology (host-independent dark fraction) and, with a cuscuton clock, the preferred-frame test (the clock is dragged by moving sources, [L170](fable_independent_2026/L170_boosted_ppn_single_metric.py)); a stiff khronometric clock repairs PPN at the cost of a G_cosmo shift and leaves cosmology dead ([L171](fable_independent_2026/L171_stiff_clock_version.py)). **Every mechanism for the mass-dependent fraction is computed and excluded**: two-body decay by a lifetime pincer (forest τ ≥ 41 Gyr vs galaxies τ ≤ 20; [L167](fable_independent_2026/L167_nbody_kick_test.py) N-body, [L168](fable_independent_2026/L168_flux_power_two_body_decay.py) exact linear response), a clock-switched velocity by small-scale cosmic shear ([L173](fable_independent_2026/L173_internal_clock_fluid.py)–[L174](fable_independent_2026/L174_small_scale_shear.py)), a potential-depth threshold by the forest ([L175](fable_independent_2026/L175_potential_depth_mechanism.py)), a time-dependent coupling by S₈ ([L177](fable_independent_2026/L177_time_dependent_coupling.py)). The framework's own nonlinear P(k,z) with the kernel active was then computed ([L176](fable_independent_2026/L176_framework_pk_baseline.py), QUMOND particle-mesh validated against halofit) and closes the last loophole both ways ([L178](fable_independent_2026/L178_pm_coupled_component_kernel_baryons.py)): a kernel on the peculiar field overshoots ΛCDM structure at z = 3 and z ≤ 0.5 by 2–3×, a kernel that sees the Hubble-flow acceleration is off cosmologically (cH/a₀ = 7 today) and every component-alone kill stands. The Milky Way's Gaia DR3 decline is an undecided prediction (kernel + LMC external field: slope −0.35 to −0.20 vs −0.47 ± 0.15). **Open, not closed:** nonlinear top-down fragmentation of a hot component, the emergent-MOND-from-dark-matter branch, a hydro forest likelihood, a galaxy-resolution kernel N-body, and the action-level derivation of how the background acceleration enters the kernel. The lead field-theory candidate (primordial clock + dynamical scalar + cubic coupling) is published as a status report with its failures — coefficient functions reconstructed rather than derived, instantaneous MOND excluded on expanding initial data, a failed convergence test — as [DOI 10.5281/zenodo.22699828](https://doi.org/10.5281/zenodo.22699828). Nothing here is a theory; it is the complete statement of what one would have to be.

**Standing 2026-09-06 (rev. 8) — the coefficient is a boundary condition; both wide-binary arms registered; the dark-sector hunt frozen.** The candidate covariant action (khronometric clock + dynamical MOND scalar + coherence operator, ν_RAR carried) **cannot relate a₀ to Λ**: the MOND primitive enters the field equations only through its derivative and the FLRW background only through Λ + (2−K_B)J(0)/2, a normalisation zero mode ([`kappa_closure/k01`](kappa_closure/k01_zero_mode_theorem_and_lambda_free_vacuum.py)). The Λ-free repair yields a *negative* vacuum energy 220× too small; a sequestering-type global constraint misses by five orders ([`k02`](kappa_closure/k02_global_constraint_average.py)); promoting a₀ to a conserved four-form flux fixes the sign and makes a₀ ∝ √(Gρ_Λ) structural but leaves κ as the free coupling ratio Z/β² = 8, with an environmental a₀ that switches the scalar off above 155 a₀ and is invisible in galaxies ([`k04`](kappa_closure/k04_four_form_promotion_consistency.py)). The one coefficient-free alternative, the horizon form a₀ = c²/(2πL_dS) (κ = 0.461), is 8.5% from ½, below the 9.5% BTFR mass-budget floor, and **exactly degenerate with the H₀ tension**: κ = ½ on Planck's H₀ and κ = 0.461 on SH0ES's predict the same a₀ to 0.2% ([`k03`](kappa_closure/k03_half_vs_two_pi_precision.py)). κ = ½ is therefore an empirical boundary condition this class of actions cannot derive, to be settled by a stellar M/L zero point, an absolute gas scale and H₀ — published as [DOI 10.5281/zenodo.22559892](https://doi.org/10.5281/zenodo.22559892). **Gaia DR4:** [Amendment 11](prep_2026/gaia_dr4_prep/PREREGISTRATION_DR4.md) registers **both** mutually exclusive arms before the data — Arm A (the frozen kernel as modified gravity) γ_v = 1.1614–1.1814 / 1.1917–1.2267, Arm B (the covariant candidate at its Cassini-minimal coherence length) **ceilings 1.0450 / 1.0300** — with the decision rule fixed in advance; DR4 separates the arms at 4.2σ but cannot confirm Arm B over Newton beyond 1.6σ (stated against interest). **Dark sector:** the thermal-relic completion is a pincer with no interior (N_eff needs m ≥ 27.6 eV, the RAR needs ≤ 11 eV, the cluster profile worked only at 11.4 eV; [`g04f`–`g04i`](qwen_claude_field_theory/closure_2026/)), four condensate doors are closed on the action's own terms, and the last scale-selective mechanism, wave exclusion near 10⁻²⁴ eV, is closed too ([`g04j`](qwen_claude_field_theory/closure_2026/g04j_wave_dark_matter_door.py): the wave sea responds to a galaxy well like a classical one; the uncertainty-limited core pinches the BTFR and KiDS against cluster formation; the forest is not regenerated). **No particle or condensate mechanism keeps the action's dark fluid out of galaxies** — and the number that verdict rests on, the cold-infall mass, survived a 3D collisionless particle test with angular momentum and a flattened disc ([`g04k`](qwen_claude_field_theory/closure_2026/g04k_infall_3d_particles.py), corrected 09-08 by [`L1`](fable_independent_2026/L1_caustics_and_cap.py) which resolves caustics and repairs the acceleration cap: **0.92–1.45 M_b inside 10 kpc**, down a factor of two from 2.6 but still 4–6× the 0.25 M_b the relation tolerates; 7.8–9.4 inside 30 kpc; 14× a Newtonian control inside 100 kpc). The existing-archive high-z Tully–Fisher confrontation is exhausted; the decisive object is a deep-MOND lensed rotator at z ≈ 2.5 ([target ranking](prep_2026/a0z_crossscale/highz_target_score_2026.py)); the measurement itself — target gate, NIRSpec-then-ALMA CO(3–2) funnel, frozen statistic 0.00 vs +0.33 dex at ±0.13 dex — is pre-registered for observers as [DOI 10.5281/zenodo.22563139](https://doi.org/10.5281/zenodo.22563139). **DR4 readiness:** the pipeline has been re-run end to end with both arms reported and every checklist item closed; December is mechanical.

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

## The gems — what would survive a hostile expert

Sorted by robustness, not by ambition. Everything below is either a published theorem, a preregistered test, or a computed cost, each with its script or DOI. None of it is the RAR fit, which reproduces the McGaugh–Lelli–Schombert relation at its own scatter by construction.

**Theorems (published; machine-checked where noted)**
- **Matching theorem** — a galaxy well today is the cosmic background at (1+z)³ ≤ 5000 with the same sound speed, so any dust cold enough for the Lyman-α forest falls into galaxies, for any equation of state. The cleanest general result here and the reason every pressure-supported dark sector dies. [DOI 10.5281/zenodo.22261001](https://doi.org/10.5281/zenodo.22261001)
- **κ no-go / zero-mode theorem** — this class of actions cannot derive the a₀–Λ coefficient; the MOND primitive enters the field equations only through its derivative. [DOI 10.5281/zenodo.22559892](https://doi.org/10.5281/zenodo.22559892)
- **Foliation theorem** — two-mode MOND forces a preferred frame. [DOI 10.5281/zenodo.22679408](https://doi.org/10.5281/zenodo.22679408)
- **Cuscuton classification** — a canonical MOND scalar cannot close the hypersurface-deformation constraint algebra; consistency and ghost-freedom coincide only on the cuscuton branch. [DOI 10.5281/zenodo.22682544](https://doi.org/10.5281/zenodo.22682544)
- **Stiff-partner / BBN theorem** — shift-symmetric k-essence dust carries an a⁻⁶ partner whenever dK/dQ is asymptotically linear. [DOI 10.5281/zenodo.22682539](https://doi.org/10.5281/zenodo.22682539)
- **Bounded-boost theorem** — a ceiling that dark matter cannot impose. [DOI 10.5281/zenodo.22548669](https://doi.org/10.5281/zenodo.22548669)
- **GDM degeneracy theorem** — the CMB constrains a fluid, not a particle ([`particle-vs-mode`](nbody_2026/)).
- **Necessity certificate** (Lean 4) — what any completion on these equations must contain: a host-mass-dependent dark fraction, a non-barotropic effective fluid, a locally screened preferred-frame source ([Mondlean.lean](fable_independent_2026/lean_2026/Mondlean.lean), `necessary_conditions_for_all_gates`).
- **Lifetime pincer** (Lean 4) — two-body decaying dark matter needs τ ≥ 41 Gyr for the forest and τ ≤ 20 Gyr for galaxies ([L168](fable_independent_2026/L168_flux_power_two_body_decay.py), `two_body_tau_pincer`).
- **Clock stability theorem** (Lean 4, 2026-09-11, new) — for the lead candidate's cuscuton-clock MOND sector the sub-horizon sound speed is c_s² = [2P_X(1−D) − 2s₀W_Y]/[B(1−D)], D = 2q²W_Y/W (the clock constraint and the lapse enhance the MOND gradient term by 1/(1−D); the naive k-essence form is wrong by −28 to +4×), collapsing under the candidate's closure to c_s² = (1−s₀)·m_rel/(2−m_rel): the sector is gradient-stable **iff the clock runs no faster than proper time** (s₀ ≤ 1; on the candidate's branch it crosses 1 at a = 0.29). Verified against the candidate's exact transfer operator to 1e-3. Corollaries: the forest bound c_s² ≤ 1e-9 forces the closure margin below ~1e-8 (branch: 7e-4–9e-3), and no sound speed can deplete galaxies while clustering on forest scales (Jeans length < 7 kpc at 9.5 km/s) — the host-mass-dependent dark fraction must be dynamical. `clock_sound_speed_closure`, `clock_gradient_stability_iff`, `clock_softness_forces_margin` (105 theorems). [DOI 10.5281/zenodo.22717950](https://doi.org/10.5281/zenodo.22717950), [L185](fable_independent_2026/L185_astra_clock_sound_speed.py), [L186](fable_independent_2026/L186_clock_stability_theorem.py)
- **Gradient-driven criticality** (Lean 4, 2026-09-12, new) — the clock stability theorem was computed at ZERO field gradient. Carried through with the gradient, the MOND sector cures its own instability: the destabilising stiffness falls as (1+Y/ℓ)^{−1/2} while the logarithm margin grows as m₀ + 2dY, so c_s² rises monotonically and crosses zero at a unique Y*. Below Y* the sector is unstable so gradients grow, above it expansion dilutes them — **Y\* is a two-sided attractor and its state has c_s² = 0 exactly**. On the candidate's own history Y* sits at 0.2–2% of the transition scale, and at Y = ℓ the sound speed stays positive with the clock rate tripled. The surface is also algebraic: varying the action gives det(T^mixed_tx − L·I) = −s₀b²W·N with N the same numerator, so a third eigenvalue joins the transverse pair and the stress becomes a perfect fluid. Isotropic stress plus non-propagating perturbations **is** a clustering cold component, arriving on one surface fixed by the action instead of by tuning the margin to 1e-8. Still owed: the gradient must track Y* to ~1e-6 for the forest. `mond_stiffness_strict_anti`, `mond_margin_strict_mono`, `critical_gradient_unique`, `stress_degeneracy_identity`, `critical_stiffness_kills_N` (111 theorems). [DOI 10.5281/zenodo.22727111](https://doi.org/10.5281/zenodo.22727111), [L192](fable_independent_2026/L192_gradient_criticality.py), [L193](fable_independent_2026/L193_stress_degeneracy.py)
- **The coldness is dynamical** (2026-09-12, new) — the tracking calculation the criticality result owed. Exactly two rates act on the field gradient: expansion dilutes it, and where the sound speed is negative each mode pumps it at twice its own growth rate. Growth stops the instant the gradient passes critical, so they balance at |c_s| = H/k and **the residual sound speed is exactly (H/k_max)²**. Integrated from gradients eight orders of magnitude off critical, every trajectory lands on the same point to six digits from both sides; the scaling holds to six digits over four decades and at every unstable epoch; and with a spectrum evolving together the shortest wavelength carries essentially all the gradient variance. **The Lyman-α bound is met once the instability reaches 0.78 Mpc comoving at z = 3.** The apparent demand that the gradient track critical to one part in a million is the same condition in other units, so nothing is tuned, and in particular the logarithm margin need not be tuned to 1e-8. Cost: the residual is set by the instability's ultraviolet reach, so the forest gate is now a lower bound on that reach. [DOI 10.5281/zenodo.22727860](https://doi.org/10.5281/zenodo.22727860), [L194](fable_independent_2026/L194_tracking_dynamics.py)
- **The clock rate is the dark matter pressure** (2026-09-12, new) — the coefficient history the criticality construction owed, in closed form. Imposing the clock's own field equation together with current and energy conservation collapses the freedom to ONE parameter and forces **s₀ − 1 = w/m_rel**: the clock's excess rate over proper time is the sector's equation of state divided by the logarithm margin, not an input. The family is U ∝ a^−3(1+w), d ∝ a^−3(1−w), q ∝ a^−3w, with constant margin and conserved clock charge. Imposing Friedmann at the same time closes it: the expansion history is **ΛCDM with the cold sector's exponent −3(1+w) instead of −3**, so that parameter is the dark matter equation of state, a measured quantity. The acoustic scale (reproduced to 0.16% at w = 0) bounds it near 1e-4, and there the sound speed is still negative so the criticality still operates. **Since criticality requires w strictly positive, the framework predicts 0 < w_dm ≲ 1e-4 where ΛCDM predicts exactly zero** — testable in existing data. [DOI 10.5281/zenodo.22728545](https://doi.org/10.5281/zenodo.22728545), [L200](fable_independent_2026/L200_coefficient_history.py), [L201](fable_independent_2026/L201_friedmann_simultaneous.py)
- **A clock that cannot be dragged** (2026-09-12, new) — the preferred-frame test is what kills theories with a preferred foliation, and it killed an earlier action in this repository. It does not bite this one, for a structural reason: the background scalar depends only on the clock, so its gradient is **parallel** to the clock's normal, and the MOND invariant is by construction the part **orthogonal** to that normal. A boost tilts both together, so **the invariant vanishes in the moving frame exactly as at rest, to all orders in the velocity** — there is no first-order preferred-frame coupling to screen. The clock rate, being a scalar, is exactly invariant too. What remains is the sector's boosted stress (6e-16 of the Sun inside Saturn's orbit) and the scalar's leakage, 6.1e-10 at the screening floor. Solving for the length each test demands: the preferred-frame bound needs ξ > 5.4e-4 pc, the static Cassini bound needs 8.8e-4 pc — **the static test binds, so the preferred-frame bound is automatic**. No post-Newtonian parameter is extracted from a full metric expansion and none is claimed. [DOI 10.5281/zenodo.22728789](https://doi.org/10.5281/zenodo.22728789), [L203](fable_independent_2026/L203_preferred_frame_gate.py), [L204](fable_independent_2026/L204_boosted_metric_expansion.py)
- **★ The interpolating function is a photocount formula, and the clock cannot derive κ** (2026-09-13, new) — **the close of the κ question.** A cuscuton clock's field equation forces V′(τ) = −3HU, so it **cannot expand without a potential** — and that potential is precisely the zero mode that makes the acceleration-scale normalisation underivable, so the twelve-gate construction **provably** cannot produce κ, and the two tracks disagree by 6.9e13 on the same coefficient. Meanwhile the family selected by the data turns out to be **Mandel's n-mode photocount formula**, equivalently one minus a Tsallis q-exponential with q = 1 + 1/n — which explains the **integer** as a mode count without fixing it. Then the routes close: not Unruh modes (**41 orders** off), twelve pre-registered criteria scattering with n = 1 modal, EFT positivity inapplicable and its invariant monotone, causality saturated for every kernel, and a d-dimensional generalisation that is **dimensionally inert**. **The exponent is an empirical quantity — reported as the result, not a placeholder.** 160 theorems. [DOI 10.5281/zenodo.22735193](https://doi.org/10.5281/zenodo.22735193), [L236](fable_independent_2026/L236_can_the_two_tracks_merge.py), [L237](fable_independent_2026/L237_the_mandel_reading.py), [L239](fable_independent_2026/L239_d_dimensional.py)
- **★ A parameter-free radial acceleration relation** (2026-09-12, new) — **the best result of the day.** Remove a₀ as an independent parameter by measuring acceleration in units of the dark-energy scale, and κ becomes the reciprocal of the interpolating function's deep-MOND slope. Standard shapes all have slope 1, predicting κ = 1, excluded at 7–10σ. A family whose slope is its **integer** exponent then makes every integer a complete prediction of the relation with **nothing fitted** — and on **155 SPARC curves, 2788 points, the data pick n = 2, i.e. κ = ½**, matching a *fitted* kernel to 0.005 dex. The two registered a₀ footings turn out to be exactly that integer on the two density conventions. Predicts a power-law solar-system tail where the fitted kernel predicts zero, and ties a₀ to the dark energy's equation of state. **The integer is selected by data, not derived: four structural searches failed and two favour other integers.** [DOI 10.5281/zenodo.22731370](https://doi.org/10.5281/zenodo.22731370), [L232](fable_independent_2026/L232_sparc_parameter_free.py), [L234](fable_independent_2026/L234_structural_search.py)
- **A conserved clock rate, and the board end to end** (Lean 4, 2026-09-12, new) — **the consolidation.** The clock rate is a conserved Noether charge of an exact shift symmetry, and the margin is the distance to a speed limit the closure's single logarithmic kinetic function creates, so a value of 1e7 is technically natural rather than tuned. MOND's coupling breaks that symmetry and drives a₀ down, forcing **w ≲ 5.7e-7**, 177× tighter than the acoustic bound. Criticality survives, with an exact operating condition. Then **every gate at one parameter point, all twelve passing simultaneously**, with two independently derived combinations agreeing to one part in 1e7 and a newly exposed trade-off between MOND interpolation depth and the equation of state. **Seven quantities fixed, five free, two bounded.** Reports in full two of our own results that later lanes overturned, and their audit. 147 theorems. [DOI 10.5281/zenodo.22731066](https://doi.org/10.5281/zenodo.22731066), [L217](fable_independent_2026/L217_where_the_clock_rate_comes_from.py), [L223](fable_independent_2026/L223_end_to_end.py)
- **A clock that must run fast** (Lean 4, 2026-09-12, new) — **the last gate computed, and it is an inequality.** γ_PPN = 1 locks the disformal coefficient to twice the conformal one, so the light-bending fix and the preferred-frame source are one operator and cannot be separated. The cuscuton's squared-time-derivative coefficient is exactly zero, so the clock propagates nothing and its tilt is an elliptic boundary-value problem against the cosmic frame. The stiffness that resists dragging is free of both the matter coupling and the MOND coefficient, so the clock rate is the only handle; the gain at a stellar surface, 24s₀/f_s, is independent of the star entirely, and the tilt decays as r^{−1.562} rather than r^{−3}. At Earth's orbit the drag is 1% at the minimum clock rate, and the bound inverts to **s₀ ≳ 1.5e7** — the third constraint on that quantity, the third pointing up, and seven orders beyond what the other two need. Unexplained, and recorded as a requirement. 128 theorems. [DOI 10.5281/zenodo.22729935](https://doi.org/10.5281/zenodo.22729935), [L216](fable_independent_2026/L216_clock_alignment.py)
- **The decoupling locus** (Lean 4, 2026-09-12, new) — **the obstruction removed and the MOND scale derived.** The clock-scalar mixing that made a matter coupling dangerous vanishes exactly on W₀ = 0, a locus the action already contains. A first pass priced it at a coupling eight orders too large; that held the clock coefficient fixed and the factor cancels once it is tied to the sector's pressure — the locus fixes a ratio of magnitude at most 1/6, and the operator's weight against gravity is at worst 0.044. It also forces the clock to run at least twice proper time and the margin to sit below the equation of state. With the Y^{3/2} operator and a coupling added, deep MOND falls out of the gradient sector and **a₀ = λ³/(12πGβs₀)** is mass-independent and falls with the clock rate; the whole cost is one time-invariant inequality. And coupling matter disformally along the clock's own timelike direction gives **γ_PPN = 1 exactly with no added vector**, leaving the solar system as a single number: local matter must align the clock to within **4.6 m/s**. Carries three corrections to the entry below it. 124 theorems. [DOI 10.5281/zenodo.22729429](https://doi.org/10.5281/zenodo.22729429), [L213](fable_independent_2026/L213_branch_solved_and_the_board.py), [L214](fable_independent_2026/L214_force_law_on_the_branch.py), [L215](fable_independent_2026/L215_solar_system_on_the_branch.py)
- **What a clock can and cannot do** (Lean 4, 2026-09-12, ⚠️ **three claims corrected** by [DOI 10.5281/zenodo.22729429](https://doi.org/10.5281/zenodo.22729429): the health condition is **U > 4dℓ** not 4dℓ > U, the exponent is 0.997 not 0.470, and the absence of a force law is due to **minimal coupling**, not the exponents) — **the scope correction, and the most useful result of the day.** Every derivation above set the cubic coupling to zero, and that cubic is the only Galileon-type operator in the action. Restoring it settles the question against the action: its two gradient operators give rotation curves rising as r^{1/6} and r^{1/4}, flat curves require r⁰, both exponents are strictly positive and no mixture reaches zero. **This action cannot produce flat rotation curves for any coupling.** What flat curves need is a Y^{3/2} operator it does not contain. A consolation: its two terms cancel *exactly* at zero gradient, so the deep-MOND boundary condition holds unimposed — only the exponent is wrong. A new health condition falls out too, 4dℓ > U. **The positive half:** the cubic cancels out of the density and the current, survives only in the pressure, and the clock identity becomes s₀ − 1 = w/m_rel − 2γq²q̇/U, a three-parts-in-a-million correction. Certified in Lean: `clock_rate_from_conservation`, `clock_rate_is_pressure_over_margin`, `clock_runs_fast_iff_pressure_positive` — **the clock's rate is not an input, it is the dark sector's pressure over the margin, and time runs fast exactly when that pressure is positive** (114 theorems). [DOI 10.5281/zenodo.22728946](https://doi.org/10.5281/zenodo.22728946), [L205](fable_independent_2026/L205_does_the_family_give_mond.py), [L206](fable_independent_2026/L206_cubic_restored.py)
- **The ledger is geometry + the late-and-puffy closure** (computed, 2026-09-11, new) — the dark-fraction ledger's host-mass dependence (≤ 0.105 / 0.14 / 0.576 at spirals / MW / clusters, f ∝ M^0.16) is what ONE universal halo concentration looks like through the ledger's three windows (0.5 / 1.2 / 2.7 scale radii): c* = 0.40 gives 0.086 / 0.165 / 0.704, all within a factor 1.6 — no mass-dependent physics needed. The cost: c* = 0.4 is far below any collapsed halo (c ≈ 3–4), so the component would need no structure below ~Mpc (k_cut ≲ 1 h/Mpc). The open "top-down fragmentation" door was then computed: phase-matched PM runs regenerate only 0.04 / 0.45 / 0.81 of ΛCDM's power at k = 5 h/Mpc, z = 2.2 for k_cut = 1 / 2 / 4, against a forest tolerance of 0.9 — closed. With the acoustic route (clock theorem) and the decay/kick route (lifetime pincer) already closed, all three physical routes to depletion are computed to failure; the geometric shape is the exact target. [DOI 10.5281/zenodo.22718357](https://doi.org/10.5281/zenodo.22718357), [L187](fable_independent_2026/L187_late_puffy_component_topdown.py)

**Predictions and tests, fixed before the data**
- **The Hubble-kernel growth equation** (2026-09-11, new): with a₀ = κc√(Gρ_Λ) and the Hubble-flow acceleration as the kernel's cosmological ambient field (the only prescription that survives the lensing test), the linear-scale coupling is fixed with no new parameter, G_eff(z)/G = ν(cH(z)/a₀), (cH₀/a₀)² = 8π/(3κ²Ω_Λ) = 49. It predicts σ₈ +1.1–1.5% over Planck-ΛCDM (S₈ = 0.843–0.847) and fσ₈ +2–4% at z < 1 — opposite in sign to the S₈ tension, at DESI reach, killable. Checked against DESI DR1 (L181): consistent, χ²/bin 0.65–0.73, not yet discriminated (errors 10–19% vs a 1–4% effect). Lean `hubble_kernel_identity` (100 theorems). [DOI 10.5281/zenodo.22706925](https://doi.org/10.5281/zenodo.22706925), [L180](fable_independent_2026/L180_hubble_kernel_growth_prediction.py)
- **Observing case for the z ≈ 2.5 decisive galaxy** — gate, funnel, budget, candidates, decision rule, written for observers. [DOI 10.5281/zenodo.22700993](https://doi.org/10.5281/zenodo.22700993), [OBSERVING_CASE_A0Z_2026.md](prep_2026/a0z_crossscale/OBSERVING_CASE_A0Z_2026.md)
- **Flat a₀(z)** — deep-MOND Tully–Fisher zero-point at z ≈ 2.5: 0.00 dex (this framework) vs +0.33 dex (a ΛCDM-native rising scale), decidable at ±0.13 dex. [DOI 10.5281/zenodo.22563139](https://doi.org/10.5281/zenodo.22563139)
- **Gaia DR4** — both mutually exclusive wide-binary arms registered with a fixed decision rule. [DOI 10.5281/zenodo.21702746](https://doi.org/10.5281/zenodo.21702746), [Amendment 11](prep_2026/gaia_dr4_prep/PREREGISTRATION_DR4.md)
- **Milky Way outer slope** — −0.35 to −0.20 over 19.5–26.5 kpc with the LMC's external field, against Gaia DR3's −0.47 ± 0.15 ([L172](fable_independent_2026/L172_mw_outer_curve_and_fgal_ledger.py)).
- **Dwarf-spheroidal external-field effect** — ~1.9× across Galactocentric radius, where dark matter predicts none ([`hunt_2026/g06*`](hunt_2026/)).
- **SN-Ia host-mass step at a₀** — the 6.9σ step reproduced; decisive tests still underpowered ([`nbody_2026/`](nbody_2026/)).

**Tools and honest costs**
- A QUMOND cosmological particle-mesh code validated against halofit ([L176](fable_independent_2026/L176_framework_pk_baseline.py)) and an exact linear-response solver for kicked or decaying dark matter ([L168](fable_independent_2026/L168_flux_power_two_body_decay.py)).
- The kernel-prescription dichotomy on lensing ([L178](fable_independent_2026/L178_pm_coupled_component_kernel_baryons.py), [L179](fable_independent_2026/L179_lensing_from_kernel_potential.py)): a kernel on the peculiar field overpowers cosmological lensing tenfold; a kernel that sees the Hubble-flow acceleration is off cosmologically. The sharpest statement here of what the cosmological-a₀ ambiguity costs.
- The dark-fraction ledger, f ∝ M^0.16 from spirals to clusters, as the target any mechanism must hit ([L172](fable_independent_2026/L172_mw_outer_curve_and_fgal_ledger.py)).
- Liabilities found and kept on the record: the Coma UDG factor-14 discrepancy (4.9σ), the cold-infall mass 4–6× over what the relation tolerates, and κ = ½ versus 1/2π degenerate with the H₀ tension.

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

[![DESI DR1 Growth Check](https://img.shields.io/badge/Hubble--Kernel%20Equation%20vs%20DESI%20DR1%20(Sep%2011%202026)-10.5281%2Fzenodo.22708060-blue)](https://doi.org/10.5281/zenodo.22708060)
[![Clock Stability Theorem](https://img.shields.io/badge/The%20Clock%20Stability%20Theorem%20(Sep%2011%202026)-10.5281%2Fzenodo.22717950-blue)](https://doi.org/10.5281/zenodo.22717950)
[![Ledger Geometry](https://img.shields.io/badge/The%20Ledger%20Is%20Geometry%20(Sep%2011%202026)-10.5281%2Fzenodo.22718357-blue)](https://doi.org/10.5281/zenodo.22718357)
[![Gradient-Driven Criticality](https://img.shields.io/badge/Gradient--Driven%20Criticality%20(Sep%2012%202026)-10.5281%2Fzenodo.22727111-blue)](https://doi.org/10.5281/zenodo.22727111)
[![The Coldness Is Dynamical](https://img.shields.io/badge/The%20Coldness%20Is%20Dynamical%20(Sep%2012%202026)-10.5281%2Fzenodo.22727860-blue)](https://doi.org/10.5281/zenodo.22727860)
[![Positive Dark Matter Pressure](https://img.shields.io/badge/The%20Clock%20Rate%20Is%20the%20Dark%20Matter%20Pressure%20(Sep%2012%202026)-10.5281%2Fzenodo.22728545-blue)](https://doi.org/10.5281/zenodo.22728545)
[![A Clock That Cannot Be Dragged](https://img.shields.io/badge/A%20Clock%20That%20Cannot%20Be%20Dragged%20(Sep%2012%202026)-10.5281%2Fzenodo.22728789-blue)](https://doi.org/10.5281/zenodo.22728789)
[![Photocount Reading + Clock No-Go](https://img.shields.io/badge/A%20Photocount%20Reading%20%2B%20a%20Clock%20No--Go%20(Sep%2013%202026)-10.5281%2Fzenodo.22735193-brightgreen)](https://doi.org/10.5281/zenodo.22735193)
[![Parameter-Free RAR](https://img.shields.io/badge/A%20Parameter--Free%20Radial%20Acceleration%20Relation%20(Sep%2012%202026)-10.5281%2Fzenodo.22731370-brightgreen)](https://doi.org/10.5281/zenodo.22731370)
[![A Conserved Clock Rate](https://img.shields.io/badge/A%20Conserved%20Clock%20Rate%20%E2%80%94%20the%20Board%20End%20to%20End%20(Sep%2012%202026)-10.5281%2Fzenodo.22731066-blue)](https://doi.org/10.5281/zenodo.22731066)
[![A Clock That Must Run Fast](https://img.shields.io/badge/A%20Clock%20That%20Must%20Run%20Fast%20%E2%80%94%20the%20Solar%20System%20as%20an%20Inequality%20(Sep%2012%202026)-10.5281%2Fzenodo.22729935-blue)](https://doi.org/10.5281/zenodo.22729935)
[![The Decoupling Locus](https://img.shields.io/badge/The%20Decoupling%20Locus%20%E2%80%94%20a%20MOND%20Scale%20Derived%20from%20a%20Clock%20(Sep%2012%202026)-10.5281%2Fzenodo.22729429-blue)](https://doi.org/10.5281/zenodo.22729429)
[![What a Clock Can and Cannot Do](https://img.shields.io/badge/What%20a%20Clock%20Can%20and%20Cannot%20Do%20(Sep%2012%202026)-10.5281%2Fzenodo.22728946-blue)](https://doi.org/10.5281/zenodo.22728946)
[![Hubble-Kernel Growth Equation](https://img.shields.io/badge/The%20Hubble--Kernel%20Growth%20Equation%20(Sep%2011%202026)-10.5281%2Fzenodo.22706925-blue)](https://doi.org/10.5281/zenodo.22706925)
[![Observing Case z~2.5](https://img.shields.io/badge/Observing%20Case%20%E2%80%94%20One%20Deep--MOND%20Rotator%20at%20z%E2%89%832.5%20(Sep%2011%202026)-10.5281%2Fzenodo.22700993-black)](https://doi.org/10.5281/zenodo.22700993)
[![Primordial-Clock Candidate Status](https://img.shields.io/badge/Primordial--Clock%20Candidate%20%E2%80%94%20Status%20Report%20with%20Failures%20(Sep%2010%202026)-10.5281%2Fzenodo.22699828-orange)](https://doi.org/10.5281/zenodo.22699828)
[![Relativistic MOND Is a Cuscuton Theory](https://img.shields.io/badge/Relativistic%20MOND%20Is%20a%20Cuscuton%20Theory%20(Sep%209%202026)-10.5281%2Fzenodo.22682544-blue)](https://doi.org/10.5281/zenodo.22682544)
[![Falsifiable Predictions](https://img.shields.io/badge/Falsifiable%20Predictions%20of%20the%20Cuscuton%20Completion%20(Sep%209%202026)-10.5281%2Fzenodo.22682541-blue)](https://doi.org/10.5281/zenodo.22682541)
[![BBN Fine-Tuning Theorem](https://img.shields.io/badge/BBN%20Fine--Tuning%20Theorem%20(Sep%209%202026)-10.5281%2Fzenodo.22682539-red)](https://doi.org/10.5281/zenodo.22682539)
[![Foliation Theorem](https://img.shields.io/badge/A%20Preferred%20Frame%20Is%20Forced%20%E2%80%94%20Foliation%20Theorem%20for%20Two--Mode%20MOND%20(Sep%209%202026)-10.5281%2Fzenodo.22679408-blue)](https://doi.org/10.5281/zenodo.22679408)
[![Complete Theory](https://img.shields.io/badge/A%20Non--Empty%20Parameter%20Region%20for%20a%20Foliation--Based%20Relativistic%20MOND%20Theory%20(Sep%208%202026)-10.5281%2Fzenodo.22667688-blue)](https://doi.org/10.5281/zenodo.22667688)
[![a0(z) Decisive Measurement](https://img.shields.io/badge/Does%20the%20MOND%20Scale%20Evolve%3F%20Pre--Registered%20z%E2%89%832.5%20Measurement%20(Sep%206%202026)-10.5281%2Fzenodo.22563139-black)](https://doi.org/10.5281/zenodo.22563139)
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
| 2026-09-15 | [10.5281/zenodo.22776494](https://doi.org/10.5281/zenodo.22776494) (concept 22753164) | The Equilibrium Reading of the Radial Acceleration Relation: What Is Derived, What Is Measured, What Is Dead | v3 (adds the natural-units form a₀ = Λ_DE²/(2M_Pl) stated as notation, and the L260 audit of H019/H020) |
| 2026-09-15 | [10.5281/zenodo.22772710](https://doi.org/10.5281/zenodo.22772710) (concept 22753164) | The Equilibrium Reading of the Radial Acceleration Relation: What Is Derived, What Is Measured, What Is Dead | v2 (adds Section 8, the L258 audit of the post-v1 closure claims: none landed, v1 labels stand; and L257 on what the lensing relation's shape tests) |
| 2026-09-14 | [10.5281/zenodo.22753165](https://doi.org/10.5281/zenodo.22753165) (concept 22753164) | The Equilibrium Reading of the Radial Acceleration Relation: What Is Derived, What Is Measured, What Is Dead | v1 |
| 2026-09-13 | [10.5281/zenodo.22735193](https://doi.org/10.5281/zenodo.22735193) (concept 22735192) | A Photocount Reading of the Interpolating Function, and a No-Go for Deriving Its Normalisation from a Clock | v1 |
| 2026-09-12 | [10.5281/zenodo.22731370](https://doi.org/10.5281/zenodo.22731370) (concept 22731369) | A Parameter-Free Radial Acceleration Relation from the Dark-Energy Scale | v1 |
| 2026-09-12 | [10.5281/zenodo.22731066](https://doi.org/10.5281/zenodo.22731066) (concept 22731065) | A Conserved Clock Rate, and the Board Run End to End | v1 |
| 2026-09-12 | [10.5281/zenodo.22729935](https://doi.org/10.5281/zenodo.22729935) (concept 22729934) | A Clock That Must Run Fast: the Solar System as an Inequality on the Rate of Cosmic Time | v1 |
| 2026-09-12 | [10.5281/zenodo.22729429](https://doi.org/10.5281/zenodo.22729429) (concept 22729428) | The Decoupling Locus: a MOND Scale Derived from a Clock, and the Solar System Reduced to One Number | v1 |
| 2026-09-12 | [10.5281/zenodo.22728946](https://doi.org/10.5281/zenodo.22728946) (concept 22728945) | What a Clock Can and Cannot Do: a Cold Dark Sector Derived, a Force Law Excluded, and the Rate of Cosmic Time Certified | v1 |
| 2026-09-12 | [10.5281/zenodo.22728789](https://doi.org/10.5281/zenodo.22728789) (concept 22728788) | A Clock That Cannot Be Dragged: Why the Preferred-Frame Test Does Not Bite a Cuscuton-Clock MOND Sector | v1 |
| 2026-09-12 | [10.5281/zenodo.22728545](https://doi.org/10.5281/zenodo.22728545) (concept 22728544) | The Clock Rate Is the Dark Matter Pressure: a Closed-Form Coefficient History for a Self-Critical MOND Sector, and a Prediction of Positive w_dm | v1 |
| 2026-09-12 | [10.5281/zenodo.22727860](https://doi.org/10.5281/zenodo.22727860) (concept 22727859) | The Coldness Is Dynamical: How Cold a Self-Critical MOND Sector Ends Up, and Why Nothing Has To Be Tuned | v1 |
| 2026-09-12 | [10.5281/zenodo.22727111](https://doi.org/10.5281/zenodo.22727111) (concept 22727110) | Gradient-Driven Criticality: a MOND Sector That Cures Its Own Gradient Instability, and a Marginal State That Is Exactly Cold | v1 |
| 2026-09-11 | [10.5281/zenodo.22718357](https://doi.org/10.5281/zenodo.22718357) (concept 22718356) | The Dark-Fraction Ledger Is Geometry: One Universal Concentration Reproduces the Host-Mass Dependence, and the Lyman-alpha Forest Closes the Late-and-Puffy Component | v1 |
| 2026-09-11 | [10.5281/zenodo.22717950](https://doi.org/10.5281/zenodo.22717950) (concept 22717949) | The Clock Stability Theorem: the Sub-Horizon Sound Speed of a Cuscuton-Clock MOND Sector Is Set by the Clock Rate | v1 |
| 2026-09-09 | [10.5281/zenodo.22679408](https://doi.org/10.5281/zenodo.22679408) (concept 22679407) | A Preferred Frame Is Forced: Static Weak-Field MOND with One Metric and Two Propagating Modes, and the Lensing Lock That Discharges the Locality Hypothesis | v1 |
| 2026-09-08 | [10.5281/zenodo.22667688](https://doi.org/10.5281/zenodo.22667688) (concept 22667687) | A Non-Empty Parameter Region for a Foliation-Based Relativistic MOND Theory: Eleven Gates Passed Below the Galaxy Scale, and a Factor 1.49–1.99 Mass Deficit Above It | v1 |
| 2026-09-06 | [10.5281/zenodo.22563139](https://doi.org/10.5281/zenodo.22563139) (concept 22563138) | Does the MOND Acceleration Scale Evolve? A Pre-Registered Decisive Measurement: the Deep-MOND Tully–Fisher Zero Point of One Lensed Rotator at z ≃ 2.5, with a Two-Stage JWST/ALMA Funnel | v1 |
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

---

# Individuals Cited

Every individual whose work is used anywhere in this repository — in papers, as
mechanisms inside Python scripts, or as references — is indexed below.
**Click any name** for its dedicated citation page in [`citations/`](citations/),
which links to every repo file where that person is cited (GitHub) plus their papers.
The master growing list lives in [`CITATIONS.md`](CITATIONS.md) (append-only; add
new names as work lands). Page indexes: **2,012 confirmed individuals indexed to date —
full-repo corpus sweep (Surname et al. / (Year) / &\ / \cite{} / filename-author patterns),
every file and occurrence listed (no caps); non-person tokens (tools, words, instruments)
flagged and listed separately.**

## Paper citations

Direct citations in the paper(s) — [`paper/dark_universe_bridge.tex`](paper/dark_universe_bridge.tex):

- [Mordehai Milgrom](citations/milgrom/index.md) — MOND (1983, 1999, 2009, 2017)
- [Jacob Bekenstein](citations/bekenstein/index.md) — AQUAL / MOND covariant realisations (1984, with Milgrom)
- [Luc Blanchet](citations/blanchet/index.md) — relativistic MOND
- [C. Skordis](citations/skordis/index.md) & [T. Zlosnik](citations/zlosnik/index.md) — AeST (2021)
- [Stacy McGaugh](citations/mcgaug/index.md) — the radial acceleration relation (2016)
- [Kyu-Hyun Chae](citations/chae/index.md) — wide binaries (2020)
- [M. Brouwer](citations/brouwer/index.md) — lensing RAR (2021)
- [S. Limbach](citations/limbach/index.md) — planetary systems / EFE
- [T. P. Singh](citations/singh/index.md) — (2026)
- [S. Marongwe](citations/marongwe/index.md) & [S. Kauffman](citations/kauffman/index.md) — (2025)
- [M. Li](citations/li/index.md) — (2004)
- DESI Collaboration (2024/2025) — cosmology data

## Mechanisms used in Python scripts

Authors whose data or methods are used inside the repository's Python lanes
(mapping to the numbered experiment lanes G001…Z10 in [`glm53_push/`](glm53_push/),
[`deepseek_push/`](deepseek_push/), and the sibling tracks):

- [Indranil Banik](citations/banik/index.md) — wide-binary / DR3 Newtonian analyses (G006, G014)
- [Federico Lelli](citations/lelli/index.md) — SPARC rotation curves (G036, G044, G071, G114)
- [M. Brouwer](citations/brouwer/index.md) — KiDS lensing RAR (G073)
- [Vittorio Ghirardini](citations/ghirardini/index.md) — X-COP cluster profiles (G008, G050, G057b)
- [Kenneth Rines](citations/rines/index.md) — HeCS cluster members (G203, G206, G209)
- [Anna-Christina Eilers](citations/eilers/index.md) — MW rotation curve (G197)
- [Joshua Simon](citations/simon/index.md) — dSph compendium (G070, G213)
- [A. Dainelli](citations/dainelli/index.md) — BTFR at z≈2.5 (G011, G080)
- [Michele Cappellari](citations/cappellari/index.md) — ATLAS3D ellipticals (G162)
- [Dominique Eckert](citations/eckert/index.md) — cluster gas fraction (G126)
- [Bode](citations/bode/index.md) & [Anosova](citations/anosova/index.md) — slab equilibrium methods (G003)
- Navarro–Frenk–White ([Navarro](citations/navarro/index.md), [Frenk](citations/frenk/index.md), [White](citations/white/index.md)) — NFW halo profile (G096, G184, G207)
- [H. C. Plummer](citations/plummer/index.md) — potential models
- [James Jeans](citations/jeans/index.md) — Jean's equations / collapse
- [V. A. Antonov](citations/antonov/index.md) — stability analysis
- [Tremaine](citations/tremaine/index.md) & [Gunn](citations/gunn/index.md) — phase-space bound
- [Bondi](citations/bondi/index.md) & [Hoyle](citations/hoyle/index.md) — accretion (G200, G210)
- [Pais](citations/pais/index.md) & [Uhlenbeck](citations/uhlenbeck/index.md) — fourth-order operators (G030)
- [Boulware](citations/boulware/index.md) & [Deser](citations/deser/index.md) — ghost analysis (G007)
- [Bertschinger](citations/bertschinger/index.md) — infall / envelope models

## Referenced

All other persons referenced across the repo (research notes, referee documents,
theories, tooling) — full per-person file lists on their pages:

- [Robert H. Sanders](citations/sanders/index.md) · [Benoît Famaey](citations/famaey/index.md) — MOND reviews
- [Pavel Kroupa](citations/kroupa/index.md) · [Marcel Pawlowski](citations/pawlowski/index.md) — satellite planes
- [Pieter van Dokkum](citations/vandokkum/index.md) · [Avi Loeb](citations/loeb/index.md) — dwarf galaxies
- [R. Brent Tully](citations/tully/index.md) · [J. Richard Fisher](citations/fisher/index.md) — the Tully–Fisher relation
- [Sandra Faber](citations/faber/index.md) · [Ray Jackson](citations/jackson/index.md) — the Faber–Jackson relation
- [Jaan Einasto](citations/einasto/index.md) — halo families · [Lars Hernquist](citations/hernquist/index.md) — bulge profiles
- [James Binney](citations/binney/index.md) — stellar dynamics
- [Edwin Salpeter](citations/salpeter/index.md) — IMF
- [José Luis Sérsic](citations/sersic/index.md) — surface-brightness profiles
- [Ivan King](citations/king/index.md) — star-cluster profiles
- [Pierre Teyssandier](citations/teyssandier/index.md) · [L. Lombardelli](citations/lombardelli/index.md) · [Boufourou](citations/boufourou/index.md) — wide-binary / light-deflection analyses
- [William Unruh](citations/unruh/index.md) · [Stephen Hawking](citations/hawking/index.md) — the de Sitter-Unruh / Hawking-temperature framework
- [Erik Verlinde](citations/verlinde/index.md) · [Thanu Padmanabhan](citations/padmanabhan/index.md) · [Ted Jacobson](citations/jacobson/index.md) — entropic / thermodynamic gravity
- [Paul Davies](citations/davies/index.md) · [Stephen Fulling](citations/fulling/index.md) — the Unruh effect / vacuum structure
- [Willem de Sitter](citations/desitter/index.md) — the de Sitter horizon / cosmic constant
- [James Schombert](citations/schombert/index.md) — SPARC / RAR co-author
- [Deidre Hunter](citations/hunter/index.md) — LITTLE THINGS / dwarf-disc HI
- [Renzo Sancisi](citations/sancisi/index.md) · [Filippo Fraternali](citations/fraternali/index.md) — HI rotation / extra-planar gas
- [Ayesha Begum](citations/begum/index.md) — dwarf rotation curves
- [HongSheng Zhao](citations/zhao/index.md) — MOND / wide-binary theory
- [Jeremiah Ostriker](citations/ostriker/index.md) — disc stability / halos
- [Donald Lynden-Bell](citations/lyndenbell/index.md) — dynamics / the "two-body" relaxation
- [Daniel Eisenstein](citations/eisenstein/index.md) — BAO / dark-energy surveys
- ClearPotential collaboration — neural ρ_DM,⊙ measurement

> **Full living index:** [`CITATIONS.md`](CITATIONS.md) — 2,012 confirmed individuals,
> each with a clickable citation page under [`citations/`](citations/), every file and
> occurrence listed (full-repo sweep, no caps). Append-only: every new contribution gets
> added there as it lands; nothing is ever deleted.

---

## Complete alphabetical index — all confirmed individuals

**2012 individuals**, each linking to its citation page (every repo file where the
person is cited + occurrence counts). Generated from the corpus sweep; append-only.

<details><summary><b>A</b> · 6 names</summary>

| Name | Files | Occurrences | Citation page |
|---|---|---|---|
| Abel | 2 | 35 | [citations/abel/](citations/abel/index.md) |
| Allen | 2 | 14 | [citations/allen/](citations/allen/index.md) |
| Anderson | 1 | 1 | [citations/anderson/](citations/anderson/index.md) |
| Arkani Hamed | 159 | 588 | [citations/arkani-hamed/](citations/arkani-hamed/index.md) |
| Atiyah Singer | 3 | 3 | [citations/atiyah-singer/](citations/atiyah-singer/index.md) |
| Auger | 6 | 7 | [citations/auger/](citations/auger/index.md) |

</details>

<details><summary><b>B</b> · 71 names</summary>

| Name | Files | Occurrences | Citation page |
|---|---|---|---|
| Bailey | 1 | 3 | [citations/bailey/](citations/bailey/index.md) |
| Baker | 5 | 7 | [citations/baker/](citations/baker/index.md) |
| Banik | 129 | 261 | [citations/banik/](citations/banik/index.md) |
| Battaglia | 1 | 1 | [citations/battaglia/](citations/battaglia/index.md) |
| Begum | 25 | 49 | [citations/begum/](citations/begum/index.md) |
| Bekenstein | 298 | 585 | [citations/bekenstein/](citations/bekenstein/index.md) |
| Bell | 61 | 134 | [citations/bell/](citations/bell/index.md) |
| Beurling | 1 | 1 | [citations/beurling/](citations/beurling/index.md) |
| Binney | 44 | 87 | [citations/binney/](citations/binney/index.md) |
| Blanchet | 102 | 200 | [citations/blanchet/](citations/blanchet/index.md) |
| Blas | 1 | 12 | [citations/blas/](citations/blas/index.md) |
| Blok | 1 | 4 | [citations/blok/](citations/blok/index.md) |
| Bosch | 29 | 57 | [citations/bosch/](citations/bosch/index.md) |
| Boselli | 12 | 17 | [citations/boselli/](citations/boselli/index.md) |
| Bosma | 1 | 2 | [citations/bosma/](citations/bosma/index.md) |
| Boss | 149 | 1051 | [citations/boss/](citations/boss/index.md) |
| Both | 14185 | 46444 | [citations/both/](citations/both/index.md) |
| Boue | 1 | 2 | [citations/boue/](citations/boue/index.md) |
| Bound | 9599 | 57135 | [citations/bound/](citations/bound/index.md) |
| Bourgain Sarnak Ziegler | 1 | 1 | [citations/bourgain-sarnak-ziegler/](citations/bourgain-sarnak-ziegler/index.md) |
| Bourgoin | 1 | 2 | [citations/bourgoin/](citations/bourgoin/index.md) |
| Bournaud | 1 | 2 | [citations/bournaud/](citations/bournaud/index.md) |
| Bousso | 26 | 58 | [citations/bousso/](citations/bousso/index.md) |
| Boutivas | 3 | 6 | [citations/boutivas/](citations/boutivas/index.md) |
| Bovy | 1 | 2 | [citations/bovy/](citations/bovy/index.md) |
| Boylan Kolchin | 1 | 2 | [citations/boylan-kolchin/](citations/boylan-kolchin/index.md) |
| Brada | 1 | 2 | [citations/brada/](citations/brada/index.md) |
| Brainerd | 1 | 2 | [citations/brainerd/](citations/brainerd/index.md) |
| Brand | 813 | 3299 | [citations/brand/](citations/brand/index.md) |
| Brannen | 3 | 5 | [citations/brannen/](citations/brannen/index.md) |
| Brans | 44 | 81 | [citations/brans/](citations/brans/index.md) |
| Brax | 19 | 240 | [citations/brax/](citations/brax/index.md) |
| Breakthrough | 207 | 386 | [citations/breakthrough/](citations/breakthrough/index.md) |
| Bregman | 1 | 2 | [citations/bregman/](citations/bregman/index.md) |
| Brewer | 15 | 31 | [citations/brewer/](citations/brewer/index.md) |
| Briareusflow | 44 | 172 | [citations/briareusflow/](citations/briareusflow/index.md) |
| Briggs | 17 | 40 | [citations/briggs/](citations/briggs/index.md) |
| Brighenti | 2 | 2 | [citations/brighenti/](citations/brighenti/index.md) |
| Broadhurst | 1 | 2 | [citations/broadhurst/](citations/broadhurst/index.md) |
| Brocato | 1 | 2 | [citations/brocato/](citations/brocato/index.md) |
| Broeils | 1 | 2 | [citations/broeils/](citations/broeils/index.md) |
| Broglie | 56 | 103 | [citations/broglie/](citations/broglie/index.md) |
| Bromley | 2 | 6 | [citations/bromley/](citations/bromley/index.md) |
| Broughan | 1 | 2 | [citations/broughan/](citations/broughan/index.md) |
| Brout | 1 | 2 | [citations/brout/](citations/brout/index.md) |
| Brouwer | 114 | 224 | [citations/brouwer/](citations/brouwer/index.md) |
| Brown | 103 | 384 | [citations/brown/](citations/brown/index.md) |
| Bruneton | 21 | 46 | [citations/bruneton/](citations/bruneton/index.md) |
| Bruningseeley | 1 | 1 | [citations/bruningseeley/](citations/bruningseeley/index.md) |
| Brunthaler | 4 | 6 | [citations/brunthaler/](citations/brunthaler/index.md) |
| Bruzual | 7 | 70 | [citations/bruzual/](citations/bruzual/index.md) |
| Bryan | 5 | 6 | [citations/bryan/](citations/bryan/index.md) |
| Bucher | 10 | 12 | [citations/bucher/](citations/bucher/index.md) |
| Buckley Geer | 1 | 2 | [citations/buckley-geer/](citations/buckley-geer/index.md) |
| Buell | 1 | 2 | [citations/buell/](citations/buell/index.md) |
| Bueno | 9 | 21 | [citations/bueno/](citations/bueno/index.md) |
| Buhimschi | 2 | 2 | [citations/buhimschi/](citations/buhimschi/index.md) |
| Bulbul | 1 | 2 | [citations/bulbul/](citations/bulbul/index.md) |
| Bulk | 4605 | 14303 | [citations/bulk/](citations/bulk/index.md) |
| Bullock | 2 | 4 | [citations/bullock/](citations/bullock/index.md) |
| Bunker | 2 | 4 | [citations/bunker/](citations/bunker/index.md) |
| Buoninfante | 5 | 8 | [citations/buoninfante/](citations/buoninfante/index.md) |
| Buote | 1 | 2 | [citations/buote/](citations/buote/index.md) |
| Bureau | 31 | 72 | [citations/bureau/](citations/bureau/index.md) |
| Burg | 578 | 1433 | [citations/burg/](citations/burg/index.md) |
| Burkert | 43 | 405 | [citations/burkert/](citations/burkert/index.md) |
| Burnol | 1 | 1 | [citations/burnol/](citations/burnol/index.md) |
| Burstein | 1 | 2 | [citations/burstein/](citations/burstein/index.md) |
| Buta | 155 | 332 | [citations/buta/](citations/buta/index.md) |
| Buttazzo | 2 | 7 | [citations/buttazzo/](citations/buttazzo/index.md) |
| Butterfield | 1 | 1 | [citations/butterfield/](citations/butterfield/index.md) |

</details>

<details><summary><b>C</b> · 143 names</summary>

| Name | Files | Occurrences | Citation page |
|---|---|---|---|
| Ca Only | 7 | 15 | [citations/ca-only/](citations/ca-only/index.md) |
| Cahn | 1 | 2 | [citations/cahn/](citations/cahn/index.md) |
| Cai | 216 | 2782 | [citations/cai/](citations/cai/index.md) |
| Calabi Yau | 126 | 245 | [citations/calabi-yau/](citations/calabi-yau/index.md) |
| Calafut | 1 | 2 | [citations/calafut/](citations/calafut/index.md) |
| Caldeira | 1 | 2 | [citations/caldeira/](citations/caldeira/index.md) |
| Calderaro | 1 | 1 | [citations/calderaro/](citations/calderaro/index.md) |
| Caldwell | 21 | 29 | [citations/caldwell/](citations/caldwell/index.md) |
| Calet | 24 | 44 | [citations/calet/](citations/calet/index.md) |
| Camb | 372 | 1752 | [citations/camb/](citations/camb/index.md) |
| Camille | 7 | 115 | [citations/camille/](citations/camille/index.md) |
| Campbell | 1 | 2 | [citations/campbell/](citations/campbell/index.md) |
| Campeti | 1 | 1 | [citations/campeti/](citations/campeti/index.md) |
| Candelas | 1 | 2 | [citations/candelas/](citations/candelas/index.md) |
| Cannaliato | 1 | 2 | [citations/cannaliato/](citations/cannaliato/index.md) |
| Cappellari | 39 | 77 | [citations/cappellari/](citations/cappellari/index.md) |
| Car | 13597 | 134980 | [citations/car/](citations/car/index.md) |
| Carr | 3 | 26 | [citations/carr/](citations/carr/index.md) |
| Carroll | 160 | 612 | [citations/carroll/](citations/carroll/index.md) |
| Cartan | 4 | 11 | [citations/cartan/](citations/cartan/index.md) |
| Casagrande | 6 | 6 | [citations/casagrande/](citations/casagrande/index.md) |
| Casals | 3 | 5 | [citations/casals/](citations/casals/index.md) |
| Casey | 1 | 2 | [citations/casey/](citations/casey/index.md) |
| Casimir | 234 | 1251 | [citations/casimir/](citations/casimir/index.md) |
| Casper | 16 | 24 | [citations/casper/](citations/casper/index.md) |
| Cassisi | 1 | 3 | [citations/cassisi/](citations/cassisi/index.md) |
| Castell | 27 | 441 | [citations/castell/](citations/castell/index.md) |
| Category | 1511 | 16768 | [citations/category/](citations/category/index.md) |
| Cava | 72 | 628 | [citations/cava/](citations/cava/index.md) |
| Cbmai | 4 | 14 | [citations/cbmai/](citations/cbmai/index.md) |
| Cect | 6 | 55 | [citations/cect/](citations/cect/index.md) |
| Cepheids | 51 | 79 | [citations/cepheids/](citations/cepheids/index.md) |
| Cha | 98037 | 547677 | [citations/cha/](citations/cha/index.md) |
| Chae | 193 | 399 | [citations/chae/](citations/chae/index.md) |
| Chan | 32 | 119 | [citations/chan/](citations/chan/index.md) |
| Chandra | 3 | 5 | [citations/chandra/](citations/chandra/index.md) |
| Chang | 3 | 21 | [citations/chang/](citations/chang/index.md) |
| Checked | 75118 | 76718 | [citations/checked/](citations/checked/index.md) |
| Checklist | 356 | 1183 | [citations/checklist/](citations/checklist/index.md) |
| Cheeger | 1 | 2 | [citations/cheeger/](citations/cheeger/index.md) |
| Chem | 7344 | 48203 | [citations/chem/](citations/chem/index.md) |
| Chen | 4 | 74 | [citations/chen/](citations/chen/index.md) |
| Cherenkov | 140 | 645 | [citations/cherenkov/](citations/cherenkov/index.md) |
| Chern | 224 | 664 | [citations/chern/](citations/chern/index.md) |
| Chetyrkin | 1 | 1 | [citations/chetyrkin/](citations/chetyrkin/index.md) |
| Chiba | 1 | 2 | [citations/chiba/](citations/chiba/index.md) |
| Chicago | 30 | 56 | [citations/chicago/](citations/chicago/index.md) |
| Chicone | 1 | 7 | [citations/chicone/](citations/chicone/index.md) |
| Chilingarian | 1 | 2 | [citations/chilingarian/](citations/chilingarian/index.md) |
| Chiti | 38 | 820 | [citations/chiti/](citations/chiti/index.md) |
| Chiu | 1 | 2 | [citations/chiu/](citations/chiu/index.md) |
| Chluba | 1 | 2 | [citations/chluba/](citations/chluba/index.md) |
| Cho | 12282 | 78587 | [citations/cho/](citations/cho/index.md) |
| Christoffels | 124 | 184 | [citations/christoffels/](citations/christoffels/index.md) |
| Christoph | 36 | 51 | [citations/christoph/](citations/christoph/index.md) |
| Ciardullo | 1 | 2 | [citations/ciardullo/](citations/ciardullo/index.md) |
| Cintio | 1 | 2 | [citations/cintio/](citations/cintio/index.md) |
| Ciocan | 2 | 4 | [citations/ciocan/](citations/ciocan/index.md) |
| Ciotti | 7 | 13 | [citations/ciotti/](citations/ciotti/index.md) |
| Ciufolini | 1 | 2 | [citations/ciufolini/](citations/ciufolini/index.md) |
| Clark | 48 | 118 | [citations/clark/](citations/clark/index.md) |
| Clean | 6146 | 27045 | [citations/clean/](citations/clean/index.md) |
| Clearpotential | 19 | 50 | [citations/clearpotential/](citations/clearpotential/index.md) |
| Clementini | 3 | 22 | [citations/clementini/](citations/clementini/index.md) |
| Cli | 9445 | 131212 | [citations/cli/](citations/cli/index.md) |
| Clipper | 1 | 1 | [citations/clipper/](citations/clipper/index.md) |
| Closer | 502 | 897 | [citations/closer/](citations/closer/index.md) |
| Closure | 6775 | 92971 | [citations/closure/](citations/closure/index.md) |
| Cloud | 1471 | 8677 | [citations/cloud/](citations/cloud/index.md) |
| Clowe | 1 | 2 | [citations/clowe/](citations/clowe/index.md) |
| Clube | 2 | 4 | [citations/clube/](citations/clube/index.md) |
| Coccato | 2 | 5 | [citations/coccato/](citations/coccato/index.md) |
| Codecov | 2 | 5 | [citations/codecov/](citations/codecov/index.md) |
| Coe | 11079 | 63986 | [citations/coe/](citations/coe/index.md) |
| Cohen | 3 | 6 | [citations/cohen/](citations/cohen/index.md) |
| Coingecko'S | 8 | 8 | [citations/coingecko's/](citations/coingecko's/index.md) |
| Colao | 5 | 26 | [citations/colao/](citations/colao/index.md) |
| Cole | 3 | 29 | [citations/cole/](citations/cole/index.md) |
| Colin | 67 | 353 | [citations/colin/](citations/colin/index.md) |
| Colladay | 3 | 3 | [citations/colladay/](citations/colladay/index.md) |
| Colless | 3 | 15 | [citations/colless/](citations/colless/index.md) |
| Collins | 1 | 2 | [citations/collins/](citations/collins/index.md) |
| Colm | 71 | 430 | [citations/colm/](citations/colm/index.md) |
| Colors | 1240 | 6214 | [citations/colors/](citations/colors/index.md) |
| Combes | 1 | 2 | [citations/combes/](citations/combes/index.md) |
| Command | 4427 | 50236 | [citations/command/](citations/command/index.md) |
| Community | 468 | 1475 | [citations/community/](citations/community/index.md) |
| Companions | 84 | 123 | [citations/companions/](citations/companions/index.md) |
| Comparison | 3205 | 8001 | [citations/comparison/](citations/comparison/index.md) |
| Complete | 11892 | 52831 | [citations/complete/](citations/complete/index.md) |
| Concannon | 1 | 1 | [citations/concannon/](citations/concannon/index.md) |
| Concentrations | 95 | 167 | [citations/concentrations/](citations/concentrations/index.md) |
| Conect | 3551 | 258113 | [citations/conect/](citations/conect/index.md) |
| Congedo | 1 | 1 | [citations/congedo/](citations/congedo/index.md) |
| Connes | 154 | 612 | [citations/connes/](citations/connes/index.md) |
| Conrad | 14 | 17 | [citations/conrad/](citations/conrad/index.md) |
| Conrey | 10 | 11 | [citations/conrey/](citations/conrey/index.md) |
| Conroy | 1 | 2 | [citations/conroy/](citations/conroy/index.md) |
| Constantinos | 16 | 21 | [citations/constantinos/](citations/constantinos/index.md) |
| Construction | 4354 | 64090 | [citations/construction/](citations/construction/index.md) |
| Contaldi | 1 | 2 | [citations/contaldi/](citations/contaldi/index.md) |
| Contextvar | 80 | 636 | [citations/contextvar/](citations/contextvar/index.md) |
| Cooke | 1 | 2 | [citations/cooke/](citations/cooke/index.md) |
| Cookson Banik | 3 | 5 | [citations/cookson-banik/](citations/cookson-banik/index.md) |
| Cooperstock | 1 | 2 | [citations/cooperstock/](citations/cooperstock/index.md) |
| Copi | 1809 | 8315 | [citations/copi/](citations/copi/index.md) |
| Cordiner | 1 | 1 | [citations/cordiner/](citations/cordiner/index.md) |
| Corey | 1 | 2 | [citations/corey/](citations/corey/index.md) |
| Corless | 1 | 2 | [citations/corless/](citations/corless/index.md) |
| Cornish | 1 | 2 | [citations/cornish/](citations/cornish/index.md) |
| Corrected | 1952 | 5392 | [citations/corrected/](citations/corrected/index.md) |
| Corrections | 4170 | 6423 | [citations/corrections/](citations/corrections/index.md) |
| Corsini | 1 | 1 | [citations/corsini/](citations/corsini/index.md) |
| Cosmological | 3481 | 12023 | [citations/cosmological/](citations/cosmological/index.md) |
| Cosmology | 2556 | 7262 | [citations/cosmology/](citations/cosmology/index.md) |
| Cote | 3 | 7 | [citations/cote/](citations/cote/index.md) |
| Coulton | 1 | 2 | [citations/coulton/](citations/coulton/index.md) |
| Courteau | 1 | 2 | [citations/courteau/](citations/courteau/index.md) |
| Cover | 9789 | 33253 | [citations/cover/](citations/cover/index.md) |
| Cowan | 5 | 7 | [citations/cowan/](citations/cowan/index.md) |
| Cowie | 1 | 2 | [citations/cowie/](citations/cowie/index.md) |
| Cremades | 6 | 8 | [citations/cremades/](citations/cremades/index.md) |
| Creminelli | 1 | 2 | [citations/creminelli/](citations/creminelli/index.md) |
| Critical | 2732 | 9678 | [citations/critical/](citations/critical/index.md) |
| Crnojevic | 5 | 16 | [citations/crnojevic/](citations/crnojevic/index.md) |
| Cromm | 1 | 2 | [citations/cromm/](citations/cromm/index.md) |
| Cronin | 5 | 7 | [citations/cronin/](citations/cronin/index.md) |
| Crotts | 1 | 4 | [citations/crotts/](citations/crotts/index.md) |
| Crystals | 3848 | 4224 | [citations/crystals/](citations/crystals/index.md) |
| Csaba | 10 | 10 | [citations/csaba/](citations/csaba/index.md) |
| Csaki | 4 | 5 | [citations/csaki/](citations/csaki/index.md) |
| Ctan | 1013 | 3077 | [citations/ctan/](citations/ctan/index.md) |
| Cube | 1742 | 21589 | [citations/cube/](citations/cube/index.md) |
| Cubic | 2875 | 7668 | [citations/cubic/](citations/cubic/index.md) |
| Cunningham | 1 | 2 | [citations/cunningham/](citations/cunningham/index.md) |
| Cuomo | 1 | 2 | [citations/cuomo/](citations/cuomo/index.md) |
| Cup | 1885 | 4306 | [citations/cup/](citations/cup/index.md) |
| Curves | 1614 | 4801 | [citations/curves/](citations/curves/index.md) |
| Cyburt | 1 | 2 | [citations/cyburt/](citations/cyburt/index.md) |
| Cylleneflow | 55 | 125 | [citations/cylleneflow/](citations/cylleneflow/index.md) |
| Cypriano | 1 | 2 | [citations/cypriano/](citations/cypriano/index.md) |
| Czarnecki | 1 | 2 | [citations/czarnecki/](citations/czarnecki/index.md) |
| Czeisler | 1 | 1 | [citations/czeisler/](citations/czeisler/index.md) |

</details>

<details><summary><b>D</b> · 120 names</summary>

| Name | Files | Occurrences | Citation page |
|---|---|---|---|
| D'Eugenio | 1 | 2 | [citations/d'eugenio/](citations/d'eugenio/index.md) |
| Dai | 402 | 19654 | [citations/dai/](citations/dai/index.md) |
| Dalal | 1 | 2 | [citations/dalal/](citations/dalal/index.md) |
| Dalang | 1 | 1 | [citations/dalang/](citations/dalang/index.md) |
| Dalcanton | 12 | 20 | [citations/dalcanton/](citations/dalcanton/index.md) |
| Dalgarno | 2 | 2 | [citations/dalgarno/](citations/dalgarno/index.md) |
| Dall'Ora | 2 | 20 | [citations/dall'ora/](citations/dall'ora/index.md) |
| Dam | 6510 | 22484 | [citations/dam/](citations/dam/index.md) |
| Dan | 6758 | 39401 | [citations/dan/](citations/dan/index.md) |
| Danhaive | 1 | 2 | [citations/danhaive/](citations/danhaive/index.md) |
| Daniel | 100 | 1006 | [citations/daniel/](citations/daniel/index.md) |
| Dapo | 19 | 76 | [citations/dapo/](citations/dapo/index.md) |
| Das | 1949 | 119442 | [citations/das/](citations/das/index.md) |
| David | 1550 | 2085 | [citations/david/](citations/david/index.md) |
| Davies | 80 | 159 | [citations/davies/](citations/davies/index.md) |
| Davis | 5 | 6 | [citations/davis/](citations/davis/index.md) |
| Davoudiasl | 3 | 3 | [citations/davoudiasl/](citations/davoudiasl/index.md) |
| Deason | 1 | 2 | [citations/deason/](citations/deason/index.md) |
| Death | 337 | 3313 | [citations/death/](citations/death/index.md) |
| Debattista | 1 | 1 | [citations/debattista/](citations/debattista/index.md) |
| Deblok | 1 | 2 | [citations/deblok/](citations/deblok/index.md) |
| Dec | 14724 | 276913 | [citations/dec/](citations/dec/index.md) |
| Default | 7615 | 57991 | [citations/default/](citations/default/index.md) |
| Deffayet | 1 | 2 | [citations/deffayet/](citations/deffayet/index.md) |
| Deg | 43191 | 134677 | [citations/deg/](citations/deg/index.md) |
| Dehnen | 1 | 1 | [citations/dehnen/](citations/dehnen/index.md) |
| Deitmar | 1 | 1 | [citations/deitmar/](citations/deitmar/index.md) |
| Dekel | 10 | 132 | [citations/dekel/](citations/dekel/index.md) |
| Delaunay | 30 | 118 | [citations/delaunay/](citations/delaunay/index.md) |
| Delay | 761 | 3740 | [citations/delay/](citations/delay/index.md) |
| Delfini | 1 | 1 | [citations/delfini/](citations/delfini/index.md) |
| Deligne | 1 | 2 | [citations/deligne/](citations/deligne/index.md) |
| Dell'Antonio | 3 | 9 | [citations/dell'antonio/](citations/dell'antonio/index.md) |
| Delpopolo | 6 | 18 | [citations/delpopolo/](citations/delpopolo/index.md) |
| Delta | 34232 | 95870 | [citations/delta/](citations/delta/index.md) |
| Demeule | 1 | 2 | [citations/demeule/](citations/demeule/index.md) |
| Democles | 1 | 2 | [citations/democles/](citations/democles/index.md) |
| Demoura | 1 | 1 | [citations/demoura/](citations/demoura/index.md) |
| Deng | 2 | 5 | [citations/deng/](citations/deng/index.md) |
| Denton | 4 | 4 | [citations/denton/](citations/denton/index.md) |
| Derham | 5 | 6 | [citations/derham/](citations/derham/index.md) |
| Derossi | 3 | 3 | [citations/derossi/](citations/derossi/index.md) |
| Derue | 1 | 2 | [citations/derue/](citations/derue/index.md) |
| Des | 52460 | 228174 | [citations/des/](citations/des/index.md) |
| Deser | 214 | 436 | [citations/deser/](citations/deser/index.md) |
| Desmond | 3 | 4 | [citations/desmond/](citations/desmond/index.md) |
| Detal | 9 | 34 | [citations/detal/](citations/detal/index.md) |
| Devaucouleurs | 2 | 4 | [citations/devaucouleurs/](citations/devaucouleurs/index.md) |
| Devday | 8 | 24 | [citations/devday/](citations/devday/index.md) |
| Developments | 34 | 38 | [citations/developments/](citations/developments/index.md) |
| Devlin | 2 | 4 | [citations/devlin/](citations/devlin/index.md) |
| Dew | 322 | 2251 | [citations/dew/](citations/dew/index.md) |
| Diacoumis | 1 | 2 | [citations/diacoumis/](citations/diacoumis/index.md) |
| Diaferio | 1 | 2 | [citations/diaferio/](citations/diaferio/index.md) |
| Dicintio | 1 | 2 | [citations/dicintio/](citations/dicintio/index.md) |
| Dickinson | 1 | 2 | [citations/dickinson/](citations/dickinson/index.md) |
| Diego Palazuelos | 8 | 9 | [citations/diego-palazuelos/](citations/diego-palazuelos/index.md) |
| Diemer | 2 | 3 | [citations/diemer/](citations/diemer/index.md) |
| Diez Tejedor | 8 | 11 | [citations/diez-tejedor/](citations/diez-tejedor/index.md) |
| Different | 8260 | 19029 | [citations/different/](citations/different/index.md) |
| Dimanalysis | 1 | 1 | [citations/dimanalysis/](citations/dimanalysis/index.md) |
| Dinamo | 4 | 8 | [citations/dinamo/](citations/dinamo/index.md) |
| Dipole | 544 | 2427 | [citations/dipole/](citations/dipole/index.md) |
| Dirac | 2008 | 12059 | [citations/dirac/](citations/dirac/index.md) |
| Direct | 11086 | 51618 | [citations/direct/](citations/direct/index.md) |
| Discovered | 992 | 3231 | [citations/discovered/](citations/discovered/index.md) |
| Discrete | 1969 | 5436 | [citations/discrete/](citations/discrete/index.md) |
| Distler Garibaldi | 12 | 36 | [citations/distler-garibaldi/](citations/distler-garibaldi/index.md) |
| Diteodoro | 2 | 4 | [citations/diteodoro/](citations/diteodoro/index.md) |
| Dive | 2254 | 6599 | [citations/dive/](citations/dive/index.md) |
| Dixon | 34 | 43 | [citations/dixon/](citations/dixon/index.md) |
| Dmsxi | 5 | 8 | [citations/dmsxi/](citations/dmsxi/index.md) |
| Dobrescu | 11 | 13 | [citations/dobrescu/](citations/dobrescu/index.md) |
| Document | 3215 | 12178 | [citations/document/](citations/document/index.md) |
| Dodd | 26 | 45 | [citations/dodd/](citations/dodd/index.md) |
| Dodelson | 17 | 49 | [citations/dodelson/](citations/dodelson/index.md) |
| Doenhoff | 2 | 3 | [citations/doenhoff/](citations/doenhoff/index.md) |
| Dof | 5587 | 27734 | [citations/dof/](citations/dof/index.md) |
| Dogariu | 3 | 5 | [citations/dogariu/](citations/dogariu/index.md) |
| Dokkum | 1 | 2 | [citations/dokkum/](citations/dokkum/index.md) |
| Dolag | 1 | 2 | [citations/dolag/](citations/dolag/index.md) |
| Donagi | 1 | 2 | [citations/donagi/](citations/donagi/index.md) |
| Donahue | 1 | 2 | [citations/donahue/](citations/donahue/index.md) |
| Donato | 23 | 103 | [citations/donato/](citations/donato/index.md) |
| Donelan | 1 | 1 | [citations/donelan/](citations/donelan/index.md) |
| Donnan | 7 | 20 | [citations/donnan/](citations/donnan/index.md) |
| Donnarumma | 1 | 2 | [citations/donnarumma/](citations/donnarumma/index.md) |
| Donnelly | 6 | 12 | [citations/donnelly/](citations/donnelly/index.md) |
| Door | 4534 | 13226 | [citations/door/](citations/door/index.md) |
| Dorian | 37 | 405 | [citations/dorian/](citations/dorian/index.md) |
| Douglas | 1 | 2 | [citations/douglas/](citations/douglas/index.md) |
| Douwe | 8 | 8 | [citations/douwe/](citations/douwe/index.md) |
| Drafting | 67 | 112 | [citations/drafting/](citations/drafting/index.md) |
| Dragonfly | 12 | 27 | [citations/dragonfly/](citations/dragonfly/index.md) |
| Drahus | 1 | 1 | [citations/drahus/](citations/drahus/index.md) |
| Draper | 6 | 11 | [citations/draper/](citations/draper/index.md) |
| Dream | 187 | 657 | [citations/dream/](citations/dream/index.md) |
| Dressler | 13 | 15 | [citations/dressler/](citations/dressler/index.md) |
| Drlica Wagner | 1 | 2 | [citations/drlica-wagner/](citations/drlica-wagner/index.md) |
| Drozdov | 3 | 7 | [citations/drozdov/](citations/drozdov/index.md) |
| Dssyk | 256 | 1321 | [citations/dssyk/](citations/dssyk/index.md) |
| Dtensor | 12 | 1080 | [citations/dtensor/](citations/dtensor/index.md) |
| Duarte | 1 | 2 | [citations/duarte/](citations/duarte/index.md) |
| Dudahart | 2 | 4 | [citations/dudahart/](citations/dudahart/index.md) |
| Duffy | 1 | 2 | [citations/duffy/](citations/duffy/index.md) |
| Dunbar | 60 | 135 | [citations/dunbar/](citations/dunbar/index.md) |
| Dune | 2 | 4 | [citations/dune/](citations/dune/index.md) |
| Dunkerton | 2 | 2 | [citations/dunkerton/](citations/dunkerton/index.md) |
| Durakovic | 1 | 2 | [citations/durakovic/](citations/durakovic/index.md) |
| Durante | 2 | 3 | [citations/durante/](citations/durante/index.md) |
| Durbala | 9 | 19 | [citations/durbala/](citations/durbala/index.md) |
| Durret | 1 | 2 | [citations/durret/](citations/durret/index.md) |
| Dutch | 20 | 36 | [citations/dutch/](citations/dutch/index.md) |
| Dutton | 1 | 2 | [citations/dutton/](citations/dutton/index.md) |
| Dvali | 25 | 306 | [citations/dvali/](citations/dvali/index.md) |
| Dvorak | 6 | 10 | [citations/dvorak/](citations/dvorak/index.md) |
| Dvorkin | 1 | 2 | [citations/dvorkin/](citations/dvorkin/index.md) |
| Dwarf | 1139 | 6501 | [citations/dwarf/](citations/dwarf/index.md) |
| Dwyer | 7 | 12 | [citations/dwyer/](citations/dwyer/index.md) |
| Dyson | 16 | 27 | [citations/dyson/](citations/dyson/index.md) |

</details>

<details><summary><b>E</b> · 60 names</summary>

| Name | Files | Occurrences | Citation page |
|---|---|---|---|
| Eadie | 6 | 9 | [citations/eadie/](citations/eadie/index.md) |
| Earth | 972 | 9969 | [citations/earth/](citations/earth/index.md) |
| Eastman | 4 | 4 | [citations/eastman/](citations/eastman/index.md) |
| Ebeling | 1 | 4 | [citations/ebeling/](citations/ebeling/index.md) |
| Eberhardt | 2 | 2 | [citations/eberhardt/](citations/eberhardt/index.md) |
| Eckert | 69 | 137 | [citations/eckert/](citations/eckert/index.md) |
| Eckmiller | 14 | 25 | [citations/eckmiller/](citations/eckmiller/index.md) |
| Eddington | 71 | 169 | [citations/eddington/](citations/eddington/index.md) |
| Edelsbrunner | 6 | 16 | [citations/edelsbrunner/](citations/edelsbrunner/index.md) |
| Edm | 1659 | 321026 | [citations/edm/](citations/edm/index.md) |
| Edr | 3276 | 28878 | [citations/edr/](citations/edr/index.md) |
| Edt | 1017 | 16086 | [citations/edt/](citations/edt/index.md) |
| Efe | 88737 | 357959 | [citations/efe/](citations/efe/index.md) |
| Effect | 6989 | 34761 | [citations/effect/](citations/effect/index.md) |
| Efraimidis | 1 | 1 | [citations/efraimidis/](citations/efraimidis/index.md) |
| Efstathiou | 7 | 11 | [citations/efstathiou/](citations/efstathiou/index.md) |
| Eichner | 2 | 2 | [citations/eichner/](citations/eichner/index.md) |
| Eilers | 58 | 139 | [citations/eilers/](citations/eilers/index.md) |
| Einasto | 43 | 85 | [citations/einasto/](citations/einasto/index.md) |
| Einstein | 38 | 115 | [citations/einstein/](citations/einstein/index.md) |
| Eisenstein | 56 | 111 | [citations/eisenstein/](citations/eisenstein/index.md) |
| El Badry | 1 | 2 | [citations/el-badry/](citations/el-badry/index.md) |
| Elbadry | 9 | 13 | [citations/elbadry/](citations/elbadry/index.md) |
| Element | 2733 | 27298 | [citations/element/](citations/element/index.md) |
| Elizalde | 6 | 6 | [citations/elizalde/](citations/elizalde/index.md) |
| Elliott | 42 | 79 | [citations/elliott/](citations/elliott/index.md) |
| Ellipticals | 120 | 238 | [citations/ellipticals/](citations/ellipticals/index.md) |
| Ellis | 132 | 516 | [citations/ellis/](citations/ellis/index.md) |
| Elt | 74605 | 89830 | [citations/elt/](citations/elt/index.md) |
| Emanuel | 2 | 4 | [citations/emanuel/](citations/emanuel/index.md) |
| Emsellem | 1 | 2 | [citations/emsellem/](citations/emsellem/index.md) |
| England | 11 | 28 | [citations/england/](citations/england/index.md) |
| English | 237 | 1182 | [citations/english/](citations/english/index.md) |
| Entanglement | 169 | 748 | [citations/entanglement/](citations/entanglement/index.md) |
| Entropy | 1516 | 8437 | [citations/entropy/](citations/entropy/index.md) |
| Env | 13302 | 172934 | [citations/env/](citations/env/index.md) |
| Epjc | 26 | 41 | [citations/epjc/](citations/epjc/index.md) |
| Equipartition | 473 | 1644 | [citations/equipartition/](citations/equipartition/index.md) |
| Era | 71950 | 475212 | [citations/era/](citations/era/index.md) |
| Eriksen | 8 | 10 | [citations/eriksen/](citations/eriksen/index.md) |
| Escape | 2440 | 153526 | [citations/escape/](citations/escape/index.md) |
| Esposito Farese | 1 | 2 | [citations/esposito-farese/](citations/esposito-farese/index.md) |
| Essn | 1390 | 2072 | [citations/essn/](citations/essn/index.md) |
| Estabrook | 1 | 2 | [citations/estabrook/](citations/estabrook/index.md) |
| Esteban | 2 | 2 | [citations/esteban/](citations/esteban/index.md) |
| Ettori | 1 | 2 | [citations/ettori/](citations/ettori/index.md) |
| Eugene | 12 | 14 | [citations/eugene/](citations/eugene/index.md) |
| Euler | 190 | 444 | [citations/euler/](citations/euler/index.md) |
| Evans | 48 | 185 | [citations/evans/](citations/evans/index.md) |
| Everitt | 1 | 2 | [citations/everitt/](citations/everitt/index.md) |
| Evil | 226 | 1488 | [citations/evil/](citations/evil/index.md) |
| Evrard | 8 | 16 | [citations/evrard/](citations/evrard/index.md) |
| Exact | 85073 | 183782 | [citations/exact/](citations/exact/index.md) |
| Experience | 517 | 1191 | [citations/experience/](citations/experience/index.md) |
| Experiment | 8952 | 83213 | [citations/experiment/](citations/experiment/index.md) |
| Expired | 746 | 3050 | [citations/expired/](citations/expired/index.md) |
| Explicit | 5725 | 16257 | [citations/explicit/](citations/explicit/index.md) |
| Express | 5056 | 24464 | [citations/express/](citations/express/index.md) |
| Extracted | 796 | 2155 | [citations/extracted/](citations/extracted/index.md) |
| Ezquiaga | 18 | 34 | [citations/ezquiaga/](citations/ezquiaga/index.md) |

</details>

<details><summary><b>F</b> · 78 names</summary>

| Name | Files | Occurrences | Citation page |
|---|---|---|---|
| Faa | 372 | 22279 | [citations/faa/](citations/faa/index.md) |
| Faber | 116 | 297 | [citations/faber/](citations/faber/index.md) |
| Fabian | 1 | 2 | [citations/fabian/](citations/fabian/index.md) |
| Fabrizio | 5 | 16 | [citations/fabrizio/](citations/fabrizio/index.md) |
| Fairall | 2 | 6 | [citations/fairall/](citations/fairall/index.md) |
| Fall | 6799 | 33899 | [citations/fall/](citations/fall/index.md) |
| Faltings | 3 | 4 | [citations/faltings/](citations/faltings/index.md) |
| Famaey | 154 | 306 | [citations/famaey/](citations/famaey/index.md) |
| Fan | 734 | 9615 | [citations/fan/](citations/fan/index.md) |
| Faraggi | 1 | 2 | [citations/faraggi/](citations/faraggi/index.md) |
| Farguesfontaine | 2 | 2 | [citations/farguesfontaine/](citations/farguesfontaine/index.md) |
| Farnaby | 1 | 2 | [citations/farnaby/](citations/farnaby/index.md) |
| Farrar | 1 | 2 | [citations/farrar/](citations/farrar/index.md) |
| Fasta | 250 | 2133 | [citations/fasta/](citations/fasta/index.md) |
| Faulkner | 2 | 2 | [citations/faulkner/](citations/faulkner/index.md) |
| Faxai | 1 | 3 | [citations/faxai/](citations/faxai/index.md) |
| Fda | 452 | 15896 | [citations/fda/](citations/fda/index.md) |
| Fearnley | 1 | 2 | [citations/fearnley/](citations/fearnley/index.md) |
| Feb | 2324 | 5846 | [citations/feb/](citations/feb/index.md) |
| Fei | 592 | 14273 | [citations/fei/](citations/fei/index.md) |
| Felts | 1 | 2 | [citations/felts/](citations/felts/index.md) |
| Felzer | 1 | 1 | [citations/felzer/](citations/felzer/index.md) |
| Feng | 49 | 317 | [citations/feng/](citations/feng/index.md) |
| Fensch | 3 | 3 | [citations/fensch/](citations/fensch/index.md) |
| Fermilab | 43 | 66 | [citations/fermilab/](citations/fermilab/index.md) |
| Ferreira | 1 | 2 | [citations/ferreira/](citations/ferreira/index.md) |
| Fessolov | 1 | 1 | [citations/fessolov/](citations/fessolov/index.md) |
| Fetchcommontype | 4 | 48 | [citations/fetchcommontype/](citations/fetchcommontype/index.md) |
| Fetchsharedcythonmodule | 4 | 16 | [citations/fetchsharedcythonmodule/](citations/fetchsharedcythonmodule/index.md) |
| Feynman | 3 | 6 | [citations/feynman/](citations/feynman/index.md) |
| Fienga | 1 | 2 | [citations/fienga/](citations/fienga/index.md) |
| Filed | 467 | 951 | [citations/filed/](citations/filed/index.md) |
| Filestore | 8 | 72 | [citations/filestore/](citations/filestore/index.md) |
| Fillmore | 11 | 25 | [citations/fillmore/](citations/fillmore/index.md) |
| Finkelstein | 1 | 2 | [citations/finkelstein/](citations/finkelstein/index.md) |
| Finner | 4 | 6 | [citations/finner/](citations/finner/index.md) |
| Fiona | 8 | 286 | [citations/fiona/](citations/fiona/index.md) |
| Firas | 46 | 103 | [citations/firas/](citations/firas/index.md) |
| Fischler | 10 | 25 | [citations/fischler/](citations/fischler/index.md) |
| Fisher | 204 | 431 | [citations/fisher/](citations/fisher/index.md) |
| Fit | 10921 | 57871 | [citations/fit/](citations/fit/index.md) |
| Fixed | 6996 | 25644 | [citations/fixed/](citations/fixed/index.md) |
| Fixsen | 1 | 2 | [citations/fixsen/](citations/fixsen/index.md) |
| Fixupextensiontype | 4 | 20 | [citations/fixupextensiontype/](citations/fixupextensiontype/index.md) |
| Flail | 11 | 25 | [citations/flail/](citations/flail/index.md) |
| Flamholz | 2 | 2 | [citations/flamholz/](citations/flamholz/index.md) |
| Flanagan | 1 | 2 | [citations/flanagan/](citations/flanagan/index.md) |
| Flat | 6834 | 62136 | [citations/flat/](citations/flat/index.md) |
| Flex | 959 | 7669 | [citations/flex/](citations/flex/index.md) |
| Float | 5685 | 61176 | [citations/float/](citations/float/index.md) |
| Florence | 29 | 1014 | [citations/florence/](citations/florence/index.md) |
| Flores | 8 | 9 | [citations/flores/](citations/flores/index.md) |
| Flynn | 1 | 2 | [citations/flynn/](citations/flynn/index.md) |
| Foffa | 1 | 2 | [citations/foffa/](citations/foffa/index.md) |
| Folkner | 2 | 4 | [citations/folkner/](citations/folkner/index.md) |
| Fontaine | 14 | 72 | [citations/fontaine/](citations/fontaine/index.md) |
| Forbes | 1 | 2 | [citations/forbes/](citations/forbes/index.md) |
| Ford | 5 | 55 | [citations/ford/](citations/ford/index.md) |
| Forecasts | 115 | 364 | [citations/forecasts/](citations/forecasts/index.md) |
| Foreman Mackey | 2 | 4 | [citations/foreman-mackey/](citations/foreman-mackey/index.md) |
| Foster | 6 | 13 | [citations/foster/](citations/foster/index.md) |
| Four | 4548 | 16745 | [citations/four/](citations/four/index.md) |
| Franck | 1 | 2 | [citations/franck/](citations/franck/index.md) |
| Frank | 11 | 19 | [citations/frank/](citations/frank/index.md) |
| Fraser | 341 | 740 | [citations/fraser/](citations/fraser/index.md) |
| Frebel | 1 | 2 | [citations/frebel/](citations/frebel/index.md) |
| Freedman | 2 | 3 | [citations/freedman/](citations/freedman/index.md) |
| Freeman | 2 | 4 | [citations/freeman/](citations/freeman/index.md) |
| Frenk | 53 | 105 | [citations/frenk/](citations/frenk/index.md) |
| Fresh | 2219 | 15228 | [citations/fresh/](citations/fresh/index.md) |
| Freundlich | 1 | 2 | [citations/freundlich/](citations/freundlich/index.md) |
| Friden | 1 | 1 | [citations/friden/](citations/friden/index.md) |
| Friedmann | 1150 | 8159 | [citations/friedmann/](citations/friedmann/index.md) |
| Froggatt Nielsen | 8 | 14 | [citations/froggatt-nielsen/](citations/froggatt-nielsen/index.md) |
| Frozen | 5360 | 13481 | [citations/frozen/](citations/frozen/index.md) |
| Fuente Nunez | 4 | 5 | [citations/fuente-nunez/](citations/fuente-nunez/index.md) |
| Fukugita | 1 | 2 | [citations/fukugita/](citations/fukugita/index.md) |
| Fund | 4147 | 14927 | [citations/fund/](citations/fund/index.md) |

</details>

<details><summary><b>G</b> · 111 names</summary>

| Name | Files | Occurrences | Citation page |
|---|---|---|---|
| Gabrielse | 1 | 1 | [citations/gabrielse/](citations/gabrielse/index.md) |
| Gadd | 1 | 2 | [citations/gadd/](citations/gadd/index.md) |
| Gaia | 1202 | 10578 | [citations/gaia/](citations/gaia/index.md) |
| Galactic | 1695 | 5308 | [citations/galactic/](citations/galactic/index.md) |
| Galante | 2 | 3 | [citations/galante/](citations/galante/index.md) |
| Galaxies | 2793 | 14352 | [citations/galaxies/](citations/galaxies/index.md) |
| Galaxy | 3906 | 24680 | [citations/galaxy/](citations/galaxy/index.md) |
| Galileo | 109 | 255368 | [citations/galileo/](citations/galileo/index.md) |
| Galley Etal | 6 | 8 | [citations/galley-etal/](citations/galley-etal/index.md) |
| Galli | 1 | 2 | [citations/galli/](citations/galli/index.md) |
| Galvagnion | 1 | 2 | [citations/galvagnion/](citations/galvagnion/index.md) |
| Gambini | 4 | 7 | [citations/gambini/](citations/gambini/index.md) |
| Gamma | 6507 | 47979 | [citations/gamma/](citations/gamma/index.md) |
| Gao | 75 | 230 | [citations/gao/](citations/gao/index.md) |
| Gardner | 8 | 43 | [citations/gardner/](citations/gardner/index.md) |
| Garg | 89 | 3360 | [citations/garg/](citations/garg/index.md) |
| Garibaldi | 18 | 49 | [citations/garibaldi/](citations/garibaldi/index.md) |
| Garnier | 2 | 2 | [citations/garnier/](citations/garnier/index.md) |
| Garofalo | 4 | 8 | [citations/garofalo/](citations/garofalo/index.md) |
| Garriga | 8 | 12 | [citations/garriga/](citations/garriga/index.md) |
| Garzilli | 1 | 2 | [citations/garzilli/](citations/garzilli/index.md) |
| Garzon | 1 | 1 | [citations/garzon/](citations/garzon/index.md) |
| Gastaldello | 1 | 2 | [citations/gastaldello/](citations/gastaldello/index.md) |
| Gatewayrunner | 380 | 2196 | [citations/gatewayrunner/](citations/gatewayrunner/index.md) |
| Gauge | 2868 | 23947 | [citations/gauge/](citations/gauge/index.md) |
| Gauss | 1394 | 5448 | [citations/gauss/](citations/gauss/index.md) |
| Gavazzi | 2 | 5 | [citations/gavazzi/](citations/gavazzi/index.md) |
| Gayler | 1 | 2 | [citations/gayler/](citations/gayler/index.md) |
| Gcvel | 4 | 22 | [citations/gcvel/](citations/gcvel/index.md) |
| Gebert | 1 | 2 | [citations/gebert/](citations/gebert/index.md) |
| Gebhardt | 3 | 4 | [citations/gebhardt/](citations/gebhardt/index.md) |
| Gebru | 3 | 8 | [citations/gebru/](citations/gebru/index.md) |
| Geha | 1 | 2 | [citations/geha/](citations/geha/index.md) |
| Geller | 1 | 2 | [citations/geller/](citations/geller/index.md) |
| Gen | 83560 | 487933 | [citations/gen/](citations/gen/index.md) |
| Gentile | 1 | 1 | [citations/gentile/](citations/gentile/index.md) |
| Genzel | 2 | 2 | [citations/genzel/](citations/genzel/index.md) |
| Geometric | 5369 | 23377 | [citations/geometric/](citations/geometric/index.md) |
| Geometry | 7869 | 28926 | [citations/geometry/](citations/geometry/index.md) |
| George | 66 | 629 | [citations/george/](citations/george/index.md) |
| Georgi | 122 | 196 | [citations/georgi/](citations/georgi/index.md) |
| Gerda | 16 | 309 | [citations/gerda/](citations/gerda/index.md) |
| Gerhard | 1 | 2 | [citations/gerhard/](citations/gerhard/index.md) |
| Geron | 1 | 2 | [citations/geron/](citations/geron/index.md) |
| Geshnizjani | 25 | 32 | [citations/geshnizjani/](citations/geshnizjani/index.md) |
| Get | 22334 | 303349 | [citations/get/](citations/get/index.md) |
| Gev | 1107 | 100495 | [citations/gev/](citations/gev/index.md) |
| Gguf | 150 | 6834 | [citations/gguf/](citations/gguf/index.md) |
| Ghari | 4 | 7 | [citations/ghari/](citations/ghari/index.md) |
| Ghirardini | 41 | 81 | [citations/ghirardini/](citations/ghirardini/index.md) |
| Gibbons | 2 | 4 | [citations/gibbons/](citations/gibbons/index.md) |
| Giesen | 1 | 2 | [citations/giesen/](citations/giesen/index.md) |
| Gilbert | 21 | 168 | [citations/gilbert/](citations/gilbert/index.md) |
| Giles | 1 | 2 | [citations/giles/](citations/giles/index.md) |
| Gilkey | 1 | 2 | [citations/gilkey/](citations/gilkey/index.md) |
| Gilman | 1 | 2 | [citations/gilman/](citations/gilman/index.md) |
| Gilmore | 1 | 2 | [citations/gilmore/](citations/gilmore/index.md) |
| Giorello | 2 | 5 | [citations/giorello/](citations/giorello/index.md) |
| Girardi | 14 | 178 | [citations/girardi/](citations/girardi/index.md) |
| Giudice | 3 | 3 | [citations/giudice/](citations/giudice/index.md) |
| Giustina | 1 | 2 | [citations/giustina/](citations/giustina/index.md) |
| Glamos | 17 | 43 | [citations/glamos/](citations/glamos/index.md) |
| Glashow | 1 | 2 | [citations/glashow/](citations/glashow/index.md) |
| Glazebrook | 1 | 2 | [citations/glazebrook/](citations/glazebrook/index.md) |
| Gleason | 13 | 22 | [citations/gleason/](citations/gleason/index.md) |
| Gleyzes | 1 | 2 | [citations/gleyzes/](citations/gleyzes/index.md) |
| Glycosci | 1 | 2 | [citations/glycosci/](citations/glycosci/index.md) |
| Gnedin | 1 | 2 | [citations/gnedin/](citations/gnedin/index.md) |
| Gogoi | 2 | 2 | [citations/gogoi/](citations/gogoi/index.md) |
| Goldberger Wise | 36 | 100 | [citations/goldberger-wise/](citations/goldberger-wise/index.md) |
| Goldfinger | 3 | 7 | [citations/goldfinger/](citations/goldfinger/index.md) |
| Goldman | 5 | 5 | [citations/goldman/](citations/goldman/index.md) |
| Goldreich | 11 | 25 | [citations/goldreich/](citations/goldreich/index.md) |
| Golini | 1 | 1 | [citations/golini/](citations/golini/index.md) |
| Gong | 32 | 128 | [citations/gong/](citations/gong/index.md) |
| Gonzalez | 2 | 4 | [citations/gonzalez/](citations/gonzalez/index.md) |
| Goodfellow | 2 | 4 | [citations/goodfellow/](citations/goodfellow/index.md) |
| Goodwin | 1 | 2 | [citations/goodwin/](citations/goodwin/index.md) |
| Gordon | 2 | 4 | [citations/gordon/](citations/gordon/index.md) |
| Gould | 1 | 2 | [citations/gould/](citations/gould/index.md) |
| Governato | 1 | 2 | [citations/governato/](citations/governato/index.md) |
| Gqumond | 3 | 8 | [citations/gqumond/](citations/gqumond/index.md) |
| Graaff | 1 | 2 | [citations/graaff/](citations/graaff/index.md) |
| Graham | 42 | 1931 | [citations/graham/](citations/graham/index.md) |
| Grall Melville | 12 | 21 | [citations/grall-melville/](citations/grall-melville/index.md) |
| Granata | 17 | 45 | [citations/granata/](citations/granata/index.md) |
| Gravity | 5004 | 16449 | [citations/gravity/](citations/gravity/index.md) |
| Greaves | 1 | 2 | [citations/greaves/](citations/greaves/index.md) |
| Grebel | 1 | 2 | [citations/grebel/](citations/grebel/index.md) |
| Greco | 34 | 134 | [citations/greco/](citations/greco/index.md) |
| Gremer | 2 | 3 | [citations/gremer/](citations/gremer/index.md) |
| Grenacher | 1 | 2 | [citations/grenacher/](citations/grenacher/index.md) |
| Grillmair | 6 | 16 | [citations/grillmair/](citations/grillmair/index.md) |
| Groener | 6 | 17 | [citations/groener/](citations/groener/index.md) |
| Gross | 1586 | 1876 | [citations/gross/](citations/gross/index.md) |
| Gruen | 163 | 472 | [citations/gruen/](citations/gruen/index.md) |
| Grumiller | 2 | 4 | [citations/grumiller/](citations/grumiller/index.md) |
| Gruzinov | 5 | 7 | [citations/gruzinov/](citations/gruzinov/index.md) |
| Gso | 380 | 1101 | [citations/gso/](citations/gso/index.md) |
| Gue | 2518 | 8445 | [citations/gue/](citations/gue/index.md) |
| Guide | 1455 | 5398 | [citations/guide/](citations/guide/index.md) |
| Gundlach | 1 | 2 | [citations/gundlach/](citations/gundlach/index.md) |
| Gunn | 80 | 159 | [citations/gunn/](citations/gunn/index.md) |
| Gupta | 28 | 42 | [citations/gupta/](citations/gupta/index.md) |
| Gurevich | 1 | 2 | [citations/gurevich/](citations/gurevich/index.md) |
| Gusfield | 2 | 4 | [citations/gusfield/](citations/gusfield/index.md) |
| Gut | 861 | 5674 | [citations/gut/](citations/gut/index.md) |
| Guzik | 6 | 6 | [citations/guzik/](citations/guzik/index.md) |
| Gwosc | 9 | 53 | [citations/gwosc/](citations/gwosc/index.md) |
| Gyr | 904 | 49464 | [citations/gyr/](citations/gyr/index.md) |
| Gyuck | 1 | 4 | [citations/gyuck/](citations/gyuck/index.md) |

</details>

<details><summary><b>H</b> · 128 names</summary>

| Name | Files | Occurrences | Citation page |
|---|---|---|---|
| H Bond | 1355 | 5276 | [citations/h-bond/](citations/h-bond/index.md) |
| Haarsma | 1 | 4 | [citations/haarsma/](citations/haarsma/index.md) |
| Haba | 44 | 79 | [citations/haba/](citations/haba/index.md) |
| Haehnelt | 7 | 9 | [citations/haehnelt/](citations/haehnelt/index.md) |
| Haghi | 1 | 2 | [citations/haghi/](citations/haghi/index.md) |
| Hagibis | 3 | 7 | [citations/hagibis/](citations/hagibis/index.md) |
| Hainaut | 1 | 1 | [citations/hainaut/](citations/hainaut/index.md) |
| Haiyan | 9 | 15 | [citations/haiyan/](citations/haiyan/index.md) |
| Hales | 1 | 2 | [citations/hales/](citations/hales/index.md) |
| Halkola | 1 | 2 | [citations/halkola/](citations/halkola/index.md) |
| Hallenbeck | 1 | 2 | [citations/hallenbeck/](citations/hallenbeck/index.md) |
| Halofit | 105 | 876 | [citations/halofit/](citations/halofit/index.md) |
| Halos | 547 | 3609 | [citations/halos/](citations/halos/index.md) |
| Hamanowicz | 3 | 6 | [citations/hamanowicz/](citations/hamanowicz/index.md) |
| Hamaus | 1 | 2 | [citations/hamaus/](citations/hamaus/index.md) |
| Hamed Cheng Luty Mukohyama | 13 | 15 | [citations/hamed-cheng-luty-mukohyama/](citations/hamed-cheng-luty-mukohyama/index.md) |
| Hamed Dubovsky Nicolis Rattazzi | 4 | 4 | [citations/hamed-dubovsky-nicolis-rattazzi/](citations/hamed-dubovsky-nicolis-rattazzi/index.md) |
| Hamiltonian | 1471 | 8666 | [citations/hamiltonian/](citations/hamiltonian/index.md) |
| Hammer | 119 | 193 | [citations/hammer/](citations/hammer/index.md) |
| Han | 98335 | 421778 | [citations/han/](citations/han/index.md) |
| Hardy | 70 | 183 | [citations/hardy/](citations/hardy/index.md) |
| Hargis | 1 | 2 | [citations/hargis/](citations/hargis/index.md) |
| Harikane | 2 | 2 | [citations/harikane/](citations/harikane/index.md) |
| Harko | 1 | 2 | [citations/harko/](citations/harko/index.md) |
| Harmony | 92 | 395 | [citations/harmony/](citations/harmony/index.md) |
| Haro | 166 | 1616 | [citations/haro/](citations/haro/index.md) |
| Harper | 7 | 15 | [citations/harper/](citations/harper/index.md) |
| Harris | 2 | 3 | [citations/harris/](citations/harris/index.md) |
| Hart | 840 | 3701 | [citations/hart/](citations/hart/index.md) |
| Harvey | 2 | 4 | [citations/harvey/](citations/harvey/index.md) |
| Hasegawa | 11 | 15 | [citations/hasegawa/](citations/hasegawa/index.md) |
| Hasenbusch | 3 | 4 | [citations/hasenbusch/](citations/hasenbusch/index.md) |
| Haslbauer | 1 | 2 | [citations/haslbauer/](citations/haslbauer/index.md) |
| Hasse | 73 | 223 | [citations/hasse/](citations/hasse/index.md) |
| Haubner | 6 | 9 | [citations/haubner/](citations/haubner/index.md) |
| Haugg | 1 | 1 | [citations/haugg/](citations/haugg/index.md) |
| Hawking | 193 | 385 | [citations/hawking/](citations/hawking/index.md) |
| Hayashi | 1 | 2 | [citations/hayashi/](citations/hayashi/index.md) |
| Haydys | 15 | 41 | [citations/haydys/](citations/haydys/index.md) |
| Haynes | 1 | 2 | [citations/haynes/](citations/haynes/index.md) |
| Haystac | 24 | 60 | [citations/haystac/](citations/haystac/index.md) |
| Hazel | 9 | 312 | [citations/hazel/](citations/hazel/index.md) |
| Heart | 637 | 13507 | [citations/heart/](citations/heart/index.md) |
| Heavens | 19 | 33 | [citations/heavens/](citations/heavens/index.md) |
| Hees | 6 | 12 | [citations/hees/](citations/hees/index.md) |
| Heintz | 1 | 2 | [citations/heintz/](citations/heintz/index.md) |
| Heisenberg | 65 | 164 | [citations/heisenberg/](citations/heisenberg/index.md) |
| Heisler | 3 | 3 | [citations/heisler/](citations/heisler/index.md) |
| Helene | 4 | 9 | [citations/helene/](citations/helene/index.md) |
| Henriksson | 1 | 4 | [citations/henriksson/](citations/henriksson/index.md) |
| Henriques | 1 | 2 | [citations/henriques/](citations/henriques/index.md) |
| Hensley | 1 | 1 | [citations/hensley/](citations/hensley/index.md) |
| Herbonnet | 1 | 2 | [citations/herbonnet/](citations/herbonnet/index.md) |
| Here | 92940 | 260012 | [citations/here/](citations/here/index.md) |
| Herglotz | 191 | 693 | [citations/herglotz/](citations/herglotz/index.md) |
| Hermes | 5591 | 126141 | [citations/hermes/](citations/hermes/index.md) |
| Hernandez | 2 | 3 | [citations/hernandez/](citations/hernandez/index.md) |
| Hernquist | 85 | 168 | [citations/hernquist/](citations/hernquist/index.md) |
| Hertog | 4 | 5 | [citations/hertog/](citations/hertog/index.md) |
| Hessian | 1185 | 17336 | [citations/hessian/](citations/hessian/index.md) |
| Hetatm | 3880 | 2005674 | [citations/hetatm/](citations/hetatm/index.md) |
| Heymans | 9 | 10 | [citations/heymans/](citations/heymans/index.md) |
| Higgs | 767 | 3782 | [citations/higgs/](citations/higgs/index.md) |
| Higuchi | 57 | 123 | [citations/higuchi/](citations/higuchi/index.md) |
| Hilary | 4 | 10 | [citations/hilary/](citations/hilary/index.md) |
| Hilbert | 653 | 1568 | [citations/hilbert/](citations/hilbert/index.md) |
| Hilker | 1 | 2 | [citations/hilker/](citations/hilker/index.md) |
| Hill | 17 | 43 | [citations/hill/](citations/hill/index.md) |
| Hinsen | 1 | 2 | [citations/hinsen/](citations/hinsen/index.md) |
| Hint | 2272 | 12560 | [citations/hint/](citations/hint/index.md) |
| Hirata | 1 | 2 | [citations/hirata/](citations/hirata/index.md) |
| Hitomi | 3 | 7 | [citations/hitomi/](citations/hitomi/index.md) |
| Hjorth | 1 | 1 | [citations/hjorth/](citations/hjorth/index.md) |
| Hmcode | 82 | 2337 | [citations/hmcode/](citations/hmcode/index.md) |
| Hodge | 111 | 273 | [citations/hodge/](citations/hodge/index.md) |
| Hodgkin | 17 | 50 | [citations/hodgkin/](citations/hodgkin/index.md) |
| Hodson | 4 | 11 | [citations/hodson/](citations/hodson/index.md) |
| Hoekstra | 1 | 2 | [citations/hoekstra/](citations/hoekstra/index.md) |
| Hoffman | 27 | 118 | [citations/hoffman/](citations/hoffman/index.md) |
| Hofmann | 1 | 2 | [citations/hofmann/](citations/hofmann/index.md) |
| Hogan | 11 | 18 | [citations/hogan/](citations/hogan/index.md) |
| Hogg | 27 | 52 | [citations/hogg/](citations/hogg/index.md) |
| Hojman Kuchar Teitelboim | 5 | 6 | [citations/hojman-kuchar-teitelboim/](citations/hojman-kuchar-teitelboim/index.md) |
| Holden | 1 | 2 | [citations/holden/](citations/holden/index.md) |
| Holland | 37 | 216 | [citations/holland/](citations/holland/index.md) |
| Hollenbach | 1 | 2 | [citations/hollenbach/](citations/hollenbach/index.md) |
| Holmberg | 1 | 2 | [citations/holmberg/](citations/holmberg/index.md) |
| Holographic | 960 | 4463 | [citations/holographic/](citations/holographic/index.md) |
| Holonomy | 178 | 533 | [citations/holonomy/](citations/holonomy/index.md) |
| Holtzman | 2 | 5 | [citations/holtzman/](citations/holtzman/index.md) |
| Homebrew | 272 | 1660 | [citations/homebrew/](citations/homebrew/index.md) |
| Homma | 5 | 27 | [citations/homma/](citations/homma/index.md) |
| Honcho | 306 | 7016 | [citations/honcho/](citations/honcho/index.md) |
| Hooft | 52 | 138 | [citations/hooft/](citations/hooft/index.md) |
| Hooper | 1 | 2 | [citations/hooper/](citations/hooper/index.md) |
| Horava | 3043 | 3251 | [citations/horava/](citations/horava/index.md) |
| Horizon | 2947 | 14220 | [citations/horizon/](citations/horizon/index.md) |
| Horndeski | 75 | 5734 | [citations/horndeski/](citations/horndeski/index.md) |
| Horne | 21 | 97 | [citations/horne/](citations/horne/index.md) |
| Hosotani | 3 | 5 | [citations/hosotani/](citations/hosotani/index.md) |
| Hossenfelder | 169 | 658 | [citations/hossenfelder/](citations/hossenfelder/index.md) |
| Hou | 16193 | 72028 | [citations/hou/](citations/hou/index.md) |
| Hoyt | 1 | 2 | [citations/hoyt/](citations/hoyt/index.md) |
| Huang | 2 | 5 | [citations/huang/](citations/huang/index.md) |
| Hubble | 1770 | 7107 | [citations/hubble/](citations/hubble/index.md) |
| Huber | 2 | 4 | [citations/huber/](citations/huber/index.md) |
| Huchra | 1 | 2 | [citations/huchra/](citations/huchra/index.md) |
| Huchtmeier | 6 | 13 | [citations/huchtmeier/](citations/huchtmeier/index.md) |
| Hudson | 2 | 3 | [citations/hudson/](citations/hudson/index.md) |
| Huffenberger | 1 | 1 | [citations/huffenberger/](citations/huffenberger/index.md) |
| Hugenholtz | 3 | 4 | [citations/hugenholtz/](citations/hugenholtz/index.md) |
| Hugging | 478 | 9119 | [citations/hugging/](citations/hugging/index.md) |
| Hugo | 27 | 215 | [citations/hugo/](citations/hugo/index.md) |
| Hui | 137 | 2399 | [citations/hui/](citations/hui/index.md) |
| Hulst | 10 | 20 | [citations/hulst/](citations/hulst/index.md) |
| Human | 2379 | 65721 | [citations/human/](citations/human/index.md) |
| Humphrey | 14 | 25 | [citations/humphrey/](citations/humphrey/index.md) |
| Hunter | 62 | 125 | [citations/hunter/](citations/hunter/index.md) |
| Hurwitz | 44 | 104 | [citations/hurwitz/](citations/hurwitz/index.md) |
| Huston | 1 | 1 | [citations/huston/](citations/huston/index.md) |
| Huterer | 5 | 6 | [citations/huterer/](citations/huterer/index.md) |
| Huxley | 1 | 2 | [citations/huxley/](citations/huxley/index.md) |
| Hwang | 25 | 34 | [citations/hwang/](citations/hwang/index.md) |
| Hwee | 18 | 64 | [citations/hwee/](citations/hwee/index.md) |
| Hydrogen | 3547 | 10023 | [citations/hydrogen/](citations/hydrogen/index.md) |
| Hyeonghan | 4 | 4 | [citations/hyeonghan/](citations/hyeonghan/index.md) |
| Hyper Kamiokande | 22 | 27 | [citations/hyper-kamiokande/](citations/hyper-kamiokande/index.md) |
| Hyrec | 149 | 2077 | [citations/hyrec/](citations/hyrec/index.md) |

</details>

<details><summary><b>I</b> · 42 names</summary>

| Name | Files | Occurrences | Citation page |
|---|---|---|---|
| Iain | 37 | 259 | [citations/iain/](citations/iain/index.md) |
| Ian | 64918 | 178246 | [citations/ian/](citations/ian/index.md) |
| Iapws | 3 | 19 | [citations/iapws/](citations/iapws/index.md) |
| Iau | 114 | 373 | [citations/iau/](citations/iau/index.md) |
| Ibanez | 1 | 2 | [citations/ibanez/](citations/ibanez/index.md) |
| Ibata | 1 | 2 | [citations/ibata/](citations/ibata/index.md) |
| Iclr | 85 | 798 | [citations/iclr/](citations/iclr/index.md) |
| Icml | 80 | 1063 | [citations/icml/](citations/icml/index.md) |
| Ida | 89394 | 270209 | [citations/ida/](citations/ida/index.md) |
| Identified | 1258 | 7538 | [citations/identified/](citations/identified/index.md) |
| Ids | 4379 | 32835 | [citations/ids/](citations/ids/index.md) |
| Iess | 2 | 4 | [citations/iess/](citations/iess/index.md) |
| Ifs | 351 | 16825 | [citations/ifs/](citations/ifs/index.md) |
| Igimf | 70 | 487 | [citations/igimf/](citations/igimf/index.md) |
| Iii | 2754 | 32590 | [citations/iii/](citations/iii/index.md) |
| Ilgenfritz | 2 | 2 | [citations/ilgenfritz/](citations/ilgenfritz/index.md) |
| Ilic | 4 | 10 | [citations/ilic/](citations/ilic/index.md) |
| Importimpl | 4 | 16 | [citations/importimpl/](citations/importimpl/index.md) |
| Independent | 80970 | 109041 | [citations/independent/](citations/independent/index.md) |
| Ingredient | 410 | 764 | [citations/ingredient/](citations/ingredient/index.md) |
| Inhibitors | 334 | 527 | [citations/inhibitors/](citations/inhibitors/index.md) |
| Ink | 9392 | 88590 | [citations/ink/](citations/ink/index.md) |
| Inputs | 2688 | 6770 | [citations/inputs/](citations/inputs/index.md) |
| Instability | 718 | 1872 | [citations/instability/](citations/instability/index.md) |
| Intellect | 99 | 166 | [citations/intellect/](citations/intellect/index.md) |
| International | 228 | 341 | [citations/international/](citations/international/index.md) |
| Investigations | 47 | 62 | [citations/investigations/](citations/investigations/index.md) |
| Iodice | 1 | 2 | [citations/iodice/](citations/iodice/index.md) |
| Iorio | 1 | 2 | [citations/iorio/](citations/iorio/index.md) |
| Iris | 102 | 948 | [citations/iris/](citations/iris/index.md) |
| Irma | 1064 | 2276 | [citations/irma/](citations/irma/index.md) |
| Irsic | 1 | 2 | [citations/irsic/](citations/irsic/index.md) |
| Irwin | 303 | 478 | [citations/irwin/](citations/irwin/index.md) |
| Ishak | 7 | 22 | [citations/ishak/](citations/ishak/index.md) |
| Ishiyama | 1 | 2 | [citations/ishiyama/](citations/ishiyama/index.md) |
| Isobe | 1 | 2 | [citations/isobe/](citations/isobe/index.md) |
| Israel | 3 | 5 | [citations/israel/](citations/israel/index.md) |
| Issn | 2381 | 4397 | [citations/issn/](citations/issn/index.md) |
| Iteration | 4585 | 22331 | [citations/iteration/](citations/iteration/index.md) |
| Ivezic | 1 | 2 | [citations/ivezic/](citations/ivezic/index.md) |
| Iyer | 25 | 432 | [citations/iyer/](citations/iyer/index.md) |
| Iyonaga | 13 | 15 | [citations/iyonaga/](citations/iyonaga/index.md) |

</details>

<details><summary><b>J</b> · 45 names</summary>

| Name | Files | Occurrences | Citation page |
|---|---|---|---|
| Jacobson | 143 | 284 | [citations/jacobson/](citations/jacobson/index.md) |
| Jacoby | 4 | 4 | [citations/jacoby/](citations/jacoby/index.md) |
| Jades | 110 | 388 | [citations/jades/](citations/jades/index.md) |
| Jafari | 2 | 3 | [citations/jafari/](citations/jafari/index.md) |
| Jafferis | 1 | 2 | [citations/jafferis/](citations/jafferis/index.md) |
| Jain | 34 | 85 | [citations/jain/](citations/jain/index.md) |
| Jan | 2723 | 6752 | [citations/jan/](citations/jan/index.md) |
| Jarlskog | 135 | 384 | [citations/jarlskog/](citations/jarlskog/index.md) |
| Jarrett | 3 | 10 | [citations/jarrett/](citations/jarrett/index.md) |
| Jason | 19 | 37 | [citations/jason/](citations/jason/index.md) |
| Jcap | 6 | 9 | [citations/jcap/](citations/jcap/index.md) |
| Jeanneau | 1 | 2 | [citations/jeanneau/](citations/jeanneau/index.md) |
| Jeffrey | 43 | 55 | [citations/jeffrey/](citations/jeffrey/index.md) |
| Jensen | 92 | 289 | [citations/jensen/](citations/jensen/index.md) |
| Jentschura | 1 | 1 | [citations/jentschura/](citations/jentschura/index.md) |
| Jeon | 34 | 135 | [citations/jeon/](citations/jeon/index.md) |
| Jerabkova | 1 | 2 | [citations/jerabkova/](citations/jerabkova/index.md) |
| Jerjen | 2 | 19 | [citations/jerjen/](citations/jerjen/index.md) |
| Jesus | 33 | 69 | [citations/jesus/](citations/jesus/index.md) |
| Jetzer | 1 | 2 | [citations/jetzer/](citations/jetzer/index.md) |
| Jewitt | 1 | 2 | [citations/jewitt/](citations/jewitt/index.md) |
| Jezza | 16 | 104 | [citations/jezza/](citations/jezza/index.md) |
| Jhep | 1 | 2 | [citations/jhep/](citations/jhep/index.md) |
| Ji'S | 24 | 57 | [citations/ji's/](citations/ji's/index.md) |
| Jiao | 1 | 2 | [citations/jiao/](citations/jiao/index.md) |
| Jing Shin | 8 | 8 | [citations/jing-shin/](citations/jing-shin/index.md) |
| Jlab | 16 | 30 | [citations/jlab/](citations/jlab/index.md) |
| Johan | 54 | 91 | [citations/johan/](citations/johan/index.md) |
| Johnson | 250 | 361 | [citations/johnson/](citations/johnson/index.md) |
| Joinable | 12 | 152 | [citations/joinable/](citations/joinable/index.md) |
| Joinhook | 8 | 64 | [citations/joinhook/](citations/joinhook/index.md) |
| Jonathan | 17 | 25 | [citations/jonathan/](citations/jonathan/index.md) |
| Jones | 6 | 16 | [citations/jones/](citations/jones/index.md) |
| Jong | 72 | 147 | [citations/jong/](citations/jong/index.md) |
| Jonsson | 5 | 5 | [citations/jonsson/](citations/jonsson/index.md) |
| Jordan | 65 | 174 | [citations/jordan/](citations/jordan/index.md) |
| Jordi | 1 | 2 | [citations/jordi/](citations/jordi/index.md) |
| Jow | 27 | 152 | [citations/jow/](citations/jow/index.md) |
| Jsonl | 405 | 1862 | [citations/jsonl/](citations/jsonl/index.md) |
| Juan | 38 | 252 | [citations/juan/](citations/juan/index.md) |
| Jul | 4235 | 9520 | [citations/jul/](citations/jul/index.md) |
| Jumper | 7 | 10 | [citations/jumper/](citations/jumper/index.md) |
| Jun | 2416 | 5564 | [citations/jun/](citations/jun/index.md) |
| Juric | 5 | 6 | [citations/juric/](citations/juric/index.md) |
| Jwstbullet | 1 | 2 | [citations/jwstbullet/](citations/jwstbullet/index.md) |

</details>

<details><summary><b>K</b> · 109 names</summary>

| Name | Files | Occurrences | Citation page |
|---|---|---|---|
| Kaasik | 2 | 3 | [citations/kaasik/](citations/kaasik/index.md) |
| Kachru | 16 | 17 | [citations/kachru/](citations/kachru/index.md) |
| Kadowaki | 4 | 5 | [citations/kadowaki/](citations/kadowaki/index.md) |
| Kafle | 1 | 2 | [citations/kafle/](citations/kafle/index.md) |
| Kagra | 1 | 2 | [citations/kagra/](citations/kagra/index.md) |
| Kahane | 1 | 2 | [citations/kahane/](citations/kahane/index.md) |
| Kahneman | 3 | 3 | [citations/kahneman/](citations/kahneman/index.md) |
| Kahya | 1 | 2 | [citations/kahya/](citations/kahya/index.md) |
| Kaiser | 39 | 82 | [citations/kaiser/](citations/kaiser/index.md) |
| Kaisin | 17 | 26 | [citations/kaisin/](citations/kaisin/index.md) |
| Kallivayalil | 1 | 2 | [citations/kallivayalil/](citations/kallivayalil/index.md) |
| Kallosh | 21 | 27 | [citations/kallosh/](citations/kallosh/index.md) |
| Kaloper | 5 | 8 | [citations/kaloper/](citations/kaloper/index.md) |
| Kaluza | 3 | 6 | [citations/kaluza/](citations/kaluza/index.md) |
| Kamionkowski | 1 | 2 | [citations/kamionkowski/](citations/kamionkowski/index.md) |
| Kamland Zen | 19 | 28 | [citations/kamland-zen/](citations/kamland-zen/index.md) |
| Kamphuis | 2 | 2 | [citations/kamphuis/](citations/kamphuis/index.md) |
| Kaplan | 4 | 8 | [citations/kaplan/](citations/kaplan/index.md) |
| Kaplinghat | 1 | 2 | [citations/kaplinghat/](citations/kaplinghat/index.md) |
| Kapner | 3 | 3 | [citations/kapner/](citations/kapner/index.md) |
| Karachentsev | 1 | 2 | [citations/karachentsev/](citations/karachentsev/index.md) |
| Karczmarek | 4 | 7 | [citations/karczmarek/](citations/karczmarek/index.md) |
| Karen | 10 | 452 | [citations/karen/](citations/karen/index.md) |
| Karim | 16 | 25 | [citations/karim/](citations/karim/index.md) |
| Kartaltepe | 2 | 3 | [citations/kartaltepe/](citations/kartaltepe/index.md) |
| Kashlinsky | 3 | 5 | [citations/kashlinsky/](citations/kashlinsky/index.md) |
| Kasting | 2 | 2 | [citations/kasting/](citations/kasting/index.md) |
| Kastritis | 1 | 1 | [citations/kastritis/](citations/kastritis/index.md) |
| Katrin | 2 | 4 | [citations/katrin/](citations/katrin/index.md) |
| Kauffman | 36 | 71 | [citations/kauffman/](citations/kauffman/index.md) |
| Kaufmann | 12 | 14 | [citations/kaufmann/](citations/kaufmann/index.md) |
| Kawasaki | 6 | 13 | [citations/kawasaki/](citations/kawasaki/index.md) |
| Kay | 214 | 8948 | [citations/kay/](citations/kay/index.md) |
| Kearns | 2 | 4 | [citations/kearns/](citations/kearns/index.md) |
| Keating | 1 | 2 | [citations/keating/](citations/keating/index.md) |
| Keck | 157 | 636 | [citations/keck/](citations/keck/index.md) |
| Keenan | 1 | 2 | [citations/keenan/](citations/keenan/index.md) |
| Keiper | 1 | 2 | [citations/keiper/](citations/keiper/index.md) |
| Kelleher | 1 | 2 | [citations/kelleher/](citations/kelleher/index.md) |
| Keller | 1 | 2 | [citations/keller/](citations/keller/index.md) |
| Kelly | 6 | 9 | [citations/kelly/](citations/kelly/index.md) |
| Kelson | 2 | 2 | [citations/kelson/](citations/kelson/index.md) |
| Kennicutt | 1 | 2 | [citations/kennicutt/](citations/kennicutt/index.md) |
| Kerins | 1 | 4 | [citations/kerins/](citations/kerins/index.md) |
| Kessler | 18 | 39 | [citations/kessler/](citations/kessler/index.md) |
| Kettula | 3 | 21 | [citations/kettula/](citations/kettula/index.md) |
| Khatri | 1 | 2 | [citations/khatri/](citations/khatri/index.md) |
| Khelashvili | 2 | 4 | [citations/khelashvili/](citations/khelashvili/index.md) |
| Khosroshahi | 2 | 2 | [citations/khosroshahi/](citations/khosroshahi/index.md) |
| Khoury | 1 | 2 | [citations/khoury/](citations/khoury/index.md) |
| Khronon | 25626 | 81490 | [citations/khronon/](citations/khronon/index.md) |
| Kill | 9150 | 379167 | [citations/kill/](citations/kill/index.md) |
| Kilo | 254 | 1103 | [citations/kilo/](citations/kilo/index.md) |
| Kim | 792 | 12486 | [citations/kim/](citations/kim/index.md) |
| Kinemuchi | 3 | 14 | [citations/kinemuchi/](citations/kinemuchi/index.md) |
| King | 508 | 1183 | [citations/king/](citations/king/index.md) |
| Kinoshita | 9 | 15 | [citations/kinoshita/](citations/kinoshita/index.md) |
| Kirby | 1 | 2 | [citations/kirby/](citations/kirby/index.md) |
| Kiri | 33 | 197 | [citations/kiri/](citations/kiri/index.md) |
| Kirsten | 6 | 8 | [citations/kirsten/](citations/kirsten/index.md) |
| Kitty | 79 | 392 | [citations/kitty/](citations/kitty/index.md) |
| Kitzbichler | 1 | 1 | [citations/kitzbichler/](citations/kitzbichler/index.md) |
| Klacka | 1 | 2 | [citations/klacka/](citations/klacka/index.md) |
| Klein | 26 | 92 | [citations/klein/](citations/klein/index.md) |
| Kleyna | 4 | 32 | [citations/kleyna/](citations/kleyna/index.md) |
| Kling | 109 | 381 | [citations/kling/](citations/kling/index.md) |
| Klinkhamer | 1 | 2 | [citations/klinkhamer/](citations/klinkhamer/index.md) |
| Klioner | 4 | 5 | [citations/klioner/](citations/klioner/index.md) |
| Kluge | 20 | 23 | [citations/kluge/](citations/kluge/index.md) |
| Kluyver | 7 | 42 | [citations/kluyver/](citations/kluyver/index.md) |
| Klypin | 8 | 20 | [citations/klypin/](citations/klypin/index.md) |
| Knaff Zehr Courtney | 2 | 2 | [citations/knaff-zehr-courtney/](citations/knaff-zehr-courtney/index.md) |
| Knebe | 3 | 4 | [citations/knebe/](citations/knebe/index.md) |
| Kneib | 4 | 4 | [citations/kneib/](citations/kneib/index.md) |
| Known | 9840 | 24846 | [citations/known/](citations/known/index.md) |
| Koch | 71 | 239 | [citations/koch/](citations/koch/index.md) |
| Kofman | 1 | 2 | [citations/kofman/](citations/kofman/index.md) |
| Kogut | 1 | 2 | [citations/kogut/](citations/kogut/index.md) |
| Koide | 22 | 67 | [citations/koide/](citations/koide/index.md) |
| Komatsu | 1 | 2 | [citations/komatsu/](citations/komatsu/index.md) |
| Koop | 12 | 18 | [citations/koop/](citations/koop/index.md) |
| Koposov | 1 | 2 | [citations/koposov/](citations/koposov/index.md) |
| Kopp | 2 | 5 | [citations/kopp/](citations/kopp/index.md) |
| Kordower | 1 | 2 | [citations/kordower/](citations/kordower/index.md) |
| Koribalski | 1 | 2 | [citations/koribalski/](citations/koribalski/index.md) |
| Kormendy | 12 | 14 | [citations/kormendy/](citations/kormendy/index.md) |
| Kos | 167 | 626 | [citations/kos/](citations/kos/index.md) |
| Kourkchi | 1 | 2 | [citations/kourkchi/](citations/kourkchi/index.md) |
| Kraljic | 8 | 8 | [citations/kraljic/](citations/kraljic/index.md) |
| Kramer | 1 | 2 | [citations/kramer/](citations/kramer/index.md) |
| Kravtsov | 1 | 2 | [citations/kravtsov/](citations/kravtsov/index.md) |
| Krolewski | 1 | 2 | [citations/krolewski/](citations/krolewski/index.md) |
| Krot | 10 | 19 | [citations/krot/](citations/krot/index.md) |
| Kroupa | 87 | 172 | [citations/kroupa/](citations/kroupa/index.md) |
| Kubo | 3 | 5 | [citations/kubo/](citations/kubo/index.md) |
| Kucerka | 2 | 2 | [citations/kucerka/](citations/kucerka/index.md) |
| Kuehn | 6 | 13 | [citations/kuehn/](citations/kuehn/index.md) |
| Kugel | 6 | 7 | [citations/kugel/](citations/kugel/index.md) |
| Kuhn | 47 | 231 | [citations/kuhn/](citations/kuhn/index.md) |
| Kuijken | 1 | 2 | [citations/kuijken/](citations/kuijken/index.md) |
| Kulkarni | 2 | 2 | [citations/kulkarni/](citations/kulkarni/index.md) |
| Kumar | 2 | 6 | [citations/kumar/](citations/kumar/index.md) |
| Kundu | 3 | 3 | [citations/kundu/](citations/kundu/index.md) |
| Kunkel | 1 | 3 | [citations/kunkel/](citations/kunkel/index.md) |
| Kunz | 22 | 37 | [citations/kunz/](citations/kunz/index.md) |
| Kuo | 35 | 200 | [citations/kuo/](citations/kuo/index.md) |
| Kurtz | 1 | 2 | [citations/kurtz/](citations/kurtz/index.md) |
| Kuzmich | 4 | 6 | [citations/kuzmich/](citations/kuzmich/index.md) |
| Kvernmo | 4 | 27 | [citations/kvernmo/](citations/kvernmo/index.md) |

</details>

<details><summary><b>L</b> · 91 names</summary>

| Name | Files | Occurrences | Citation page |
|---|---|---|---|
| Laakkonen | 2 | 2 | [citations/laakkonen/](citations/laakkonen/index.md) |
| Laboratory | 212 | 431 | [citations/laboratory/](citations/laboratory/index.md) |
| Labzowsky | 1 | 2 | [citations/labzowsky/](citations/labzowsky/index.md) |
| Lacroix | 1 | 1 | [citations/lacroix/](citations/lacroix/index.md) |
| Lagarias | 1 | 2 | [citations/lagarias/](citations/lagarias/index.md) |
| Lagrangian | 1190 | 3881 | [citations/lagrangian/](citations/lagrangian/index.md) |
| Lahav | 7 | 22 | [citations/lahav/](citations/lahav/index.md) |
| Lam | 13700 | 151796 | [citations/lam/](citations/lam/index.md) |
| Lancaster | 1 | 2 | [citations/lancaster/](citations/lancaster/index.md) |
| Land | 4009 | 14000 | [citations/land/](citations/land/index.md) |
| Lane | 5630 | 19534 | [citations/lane/](citations/lane/index.md) |
| Lang | 2573 | 12260 | [citations/lang/](citations/lang/index.md) |
| Laporte | 3 | 3 | [citations/laporte/](citations/laporte/index.md) |
| Lasserre | 4 | 11 | [citations/lasserre/](citations/lasserre/index.md) |
| Latest | 4018 | 6143 | [citations/latest/](citations/latest/index.md) |
| Latex | 455 | 3159 | [citations/latex/](citations/latex/index.md) |
| Latour | 1 | 2 | [citations/latour/](citations/latour/index.md) |
| Lattice | 819 | 5051 | [citations/lattice/](citations/lattice/index.md) |
| Lau | 11571 | 110971 | [citations/lau/](citations/lau/index.md) |
| Lavaux | 1 | 2 | [citations/lavaux/](citations/lavaux/index.md) |
| Learning | 621 | 3740 | [citations/learning/](citations/learning/index.md) |
| Lecar | 2 | 2 | [citations/lecar/](citations/lecar/index.md) |
| Ledu | 3 | 9 | [citations/ledu/](citations/ledu/index.md) |
| Lee | 2144 | 98970 | [citations/lee/](citations/lee/index.md) |
| Lees | 1 | 5 | [citations/lees/](citations/lees/index.md) |
| Legacy | 1179 | 5068 | [citations/legacy/](citations/legacy/index.md) |
| Leggett | 2 | 3 | [citations/leggett/](citations/leggett/index.md) |
| Legomena | 1883 | 17986 | [citations/legomena/](citations/legomena/index.md) |
| Leinaas | 3 | 4 | [citations/leinaas/](citations/leinaas/index.md) |
| Leisman | 34 | 121 | [citations/leisman/](citations/leisman/index.md) |
| Lejeune | 1 | 3 | [citations/lejeune/](citations/lejeune/index.md) |
| Lelli | 197 | 392 | [citations/lelli/](citations/lelli/index.md) |
| Lenses | 319 | 798 | [citations/lenses/](citations/lenses/index.md) |
| Leong | 1 | 2 | [citations/leong/](citations/leong/index.md) |
| Lerchster | 2 | 2 | [citations/lerchster/](citations/lerchster/index.md) |
| Leroy | 1 | 2 | [citations/leroy/](citations/leroy/index.md) |
| Lesgourgues | 132 | 142 | [citations/lesgourgues/](citations/lesgourgues/index.md) |
| Lesuer | 1 | 2 | [citations/lesuer/](citations/lesuer/index.md) |
| Letal | 26 | 160 | [citations/letal/](citations/letal/index.md) |
| Letaw | 12 | 26 | [citations/letaw/](citations/letaw/index.md) |
| Levin | 3 | 6 | [citations/levin/](citations/levin/index.md) |
| Lewis | 3 | 5 | [citations/lewis/](citations/lewis/index.md) |
| Liang | 55 | 185 | [citations/liang/](citations/liang/index.md) |
| Libra | 3611 | 10626 | [citations/libra/](citations/libra/index.md) |
| Licquia | 1 | 2 | [citations/licquia/](citations/licquia/index.md) |
| Lie | 48744 | 163718 | [citations/lie/](citations/lie/index.md) |
| Life | 1568 | 7717 | [citations/life/](citations/life/index.md) |
| Lilly | 14 | 24 | [citations/lilly/](citations/lilly/index.md) |
| Lim | 10924 | 66798 | [citations/lim/](citations/lim/index.md) |
| Limaye | 2 | 2 | [citations/limaye/](citations/limaye/index.md) |
| Limbach | 54 | 105 | [citations/limbach/](citations/limbach/index.md) |
| Limousin | 1 | 2 | [citations/limousin/](citations/limousin/index.md) |
| Lin | 99322 | 628923 | [citations/lin/](citations/lin/index.md) |
| Lipa | 56 | 580 | [citations/lipa/](citations/lipa/index.md) |
| Lipinski | 2 | 4 | [citations/lipinski/](citations/lipinski/index.md) |
| Lisa | 1341 | 5300 | [citations/lisa/](citations/lisa/index.md) |
| Liske | 9 | 109 | [citations/liske/](citations/liske/index.md) |
| Lisowski | 1 | 1 | [citations/lisowski/](citations/lisowski/index.md) |
| List | 12346 | 86436 | [citations/list/](citations/list/index.md) |
| Lit Verified | 3 | 3 | [citations/lit-verified/](citations/lit-verified/index.md) |
| Litebird | 4 | 7 | [citations/litebird/](citations/litebird/index.md) |
| Liu | 644 | 4257 | [citations/liu/](citations/liu/index.md) |
| Llama | 763 | 18349 | [citations/llama/](citations/llama/index.md) |
| Llinares | 14 | 17 | [citations/llinares/](citations/llinares/index.md) |
| Lo Et Al | 9 | 31 | [citations/lo et al/](citations/lo et al/index.md) |
| Logan | 94 | 156 | [citations/logan/](citations/logan/index.md) |
| Lokas | 1 | 2 | [citations/lokas/](citations/lokas/index.md) |
| Loll | 156 | 638 | [citations/loll/](citations/loll/index.md) |
| Lombardi | 16 | 31 | [citations/lombardi/](citations/lombardi/index.md) |
| Longeard | 4 | 9 | [citations/longeard/](citations/longeard/index.md) |
| Loparco | 5 | 6 | [citations/loparco/](citations/loparco/index.md) |
| Lopes | 2 | 4 | [citations/lopes/](citations/lopes/index.md) |
| Lopez Sanjuan | 1 | 2 | [citations/lopez-sanjuan/](citations/lopez-sanjuan/index.md) |
| Lorce | 1 | 1 | [citations/lorce/](citations/lorce/index.md) |
| Lorenz | 80 | 187 | [citations/lorenz/](citations/lorenz/index.md) |
| Love | 387 | 2724 | [citations/love/](citations/love/index.md) |
| Lovisari | 3 | 6 | [citations/lovisari/](citations/lovisari/index.md) |
| Lpo | 212 | 774 | [citations/lpo/](citations/lpo/index.md) |
| Lucca | 1 | 2 | [citations/lucca/](citations/lucca/index.md) |
| Lucky | 83 | 489 | [citations/lucky/](citations/lucky/index.md) |
| Ludlow | 1 | 2 | [citations/ludlow/](citations/ludlow/index.md) |
| Luhausen | 2 | 2 | [citations/luhausen/](citations/luhausen/index.md) |
| Luk | 118 | 424 | [citations/luk/](citations/luk/index.md) |
| Luminet | 4 | 4 | [citations/luminet/](citations/luminet/index.md) |
| Lund | 2 | 4 | [citations/lund/](citations/lund/index.md) |
| Luo | 942 | 2814 | [citations/luo/](citations/luo/index.md) |
| Luque | 5 | 12 | [citations/luque/](citations/luque/index.md) |
| Luty | 1 | 4 | [citations/luty/](citations/luty/index.md) |
| Lux | 1666 | 92853 | [citations/lux/](citations/lux/index.md) |
| Lyman Alpha | 215 | 534 | [citations/lyman-alpha/](citations/lyman-alpha/index.md) |
| Lynden Bell | 11 | 20 | [citations/lynden-bell/](citations/lynden-bell/index.md) |

</details>

<details><summary><b>M</b> · 163 names</summary>

| Name | Files | Occurrences | Citation page |
|---|---|---|---|
| M Theory | 251 | 1082 | [citations/m-theory/](citations/m-theory/index.md) |
| Maccio | 1 | 2 | [citations/maccio/](citations/maccio/index.md) |
| Macdonald | 9 | 13 | [citations/macdonald/](citations/macdonald/index.md) |
| Macdowell | 2 | 4 | [citations/macdowell/](citations/macdowell/index.md) |
| Machinelearningi | 2 | 4 | [citations/machinelearningi/](citations/machinelearningi/index.md) |
| Mack | 116 | 350 | [citations/mack/](citations/mack/index.md) |
| Macquart | 1 | 2 | [citations/macquart/](citations/macquart/index.md) |
| Madau | 1 | 2 | [citations/madau/](citations/madau/index.md) |
| Maddox | 3 | 6 | [citations/maddox/](citations/maddox/index.md) |
| Madejski | 2 | 2 | [citations/madejski/](citations/madejski/index.md) |
| Maeder | 1 | 2 | [citations/maeder/](citations/maeder/index.md) |
| Maggie | 9 | 11 | [citations/maggie/](citations/maggie/index.md) |
| Maggiore | 20 | 46 | [citations/maggiore/](citations/maggiore/index.md) |
| Magnetized | 41 | 95 | [citations/magnetized/](citations/magnetized/index.md) |
| Magoulas | 1 | 2 | [citations/magoulas/](citations/magoulas/index.md) |
| Magueijo | 13 | 17 | [citations/magueijo/](citations/magueijo/index.md) |
| Mahler | 7 | 41 | [citations/mahler/](citations/mahler/index.md) |
| Maiani | 1 | 1 | [citations/maiani/](citations/maiani/index.md) |
| Maier | 12 | 17 | [citations/maier/](citations/maier/index.md) |
| Maiolino | 4 | 5 | [citations/maiolino/](citations/maiolino/index.md) |
| Majewski | 4 | 25 | [citations/majewski/](citations/majewski/index.md) |
| Makarov | 1 | 2 | [citations/makarov/](citations/makarov/index.md) |
| Maldacena | 187 | 688 | [citations/maldacena/](citations/maldacena/index.md) |
| Malhotra | 1 | 2 | [citations/malhotra/](citations/malhotra/index.md) |
| Maloney | 4 | 5 | [citations/maloney/](citations/maloney/index.md) |
| Mamajek | 9 | 899 | [citations/mamajek/](citations/mamajek/index.md) |
| Mamon | 1 | 2 | [citations/mamon/](citations/mamon/index.md) |
| Managedserver | 36 | 216 | [citations/managedserver/](citations/managedserver/index.md) |
| Mandel | 101 | 288 | [citations/mandel/](citations/mandel/index.md) |
| Mannheim | 15 | 27 | [citations/mannheim/](citations/mannheim/index.md) |
| Mansouri | 2 | 4 | [citations/mansouri/](citations/mansouri/index.md) |
| Mantz | 1 | 2 | [citations/mantz/](citations/mantz/index.md) |
| Mao | 70 | 242 | [citations/mao/](citations/mao/index.md) |
| Maquet | 1 | 2 | [citations/maquet/](citations/maquet/index.md) |
| Mar | 90193 | 1603262 | [citations/mar/](citations/mar/index.md) |
| Marshall | 1 | 5 | [citations/marshall/](citations/marshall/index.md) |
| Mashhoon | 1 | 2 | [citations/mashhoon/](citations/mashhoon/index.md) |
| Maskawa | 1 | 2 | [citations/maskawa/](citations/maskawa/index.md) |
| Massari | 14 | 86 | [citations/massari/](citations/massari/index.md) |
| Match | 13128 | 78175 | [citations/match/](citations/match/index.md) |
| Mateo | 6 | 29 | [citations/mateo/](citations/mateo/index.md) |
| Mathematics | 1188 | 1887 | [citations/mathematics/](citations/mathematics/index.md) |
| Mathews | 22 | 49 | [citations/mathews/](citations/mathews/index.md) |
| Mathur | 16 | 37 | [citations/mathur/](citations/mathur/index.md) |
| Matouschek | 1 | 1 | [citations/matouschek/](citations/matouschek/index.md) |
| Matrix | 3653 | 46749 | [citations/matrix/](citations/matrix/index.md) |
| Matter | 28701 | 67379 | [citations/matter/](citations/matter/index.md) |
| Mattingly | 1 | 2 | [citations/mattingly/](citations/mattingly/index.md) |
| Mau | 213 | 1715 | [citations/mau/](citations/mau/index.md) |
| Mazumdar | 14 | 27 | [citations/mazumdar/](citations/mazumdar/index.md) |
| Mazzeo | 1 | 2 | [citations/mazzeo/](citations/mazzeo/index.md) |
| Mccarthy | 13 | 24 | [citations/mccarthy/](citations/mccarthy/index.md) |
| Mcclintock | 3 | 5 | [citations/mcclintock/](citations/mcclintock/index.md) |
| Mcconnachie | 1 | 2 | [citations/mcconnachie/](citations/mcconnachie/index.md) |
| Mcgaugh | 15 | 33 | [citations/mcgaugh/](citations/mcgaugh/index.md) |
| Mckee | 1 | 2 | [citations/mckee/](citations/mckee/index.md) |
| Mckinven | 1 | 1 | [citations/mckinven/](citations/mckinven/index.md) |
| Mclaughlin | 4 | 4 | [citations/mclaughlin/](citations/mclaughlin/index.md) |
| Mcmillan | 1 | 2 | [citations/mcmillan/](citations/mcmillan/index.md) |
| Mcphedran | 1 | 2 | [citations/mcphedran/](citations/mcphedran/index.md) |
| Mead | 3 | 4 | [citations/mead/](citations/mead/index.md) |
| Measured | 4769 | 29995 | [citations/measured/](citations/measured/index.md) |
| Measurements | 1240 | 3175 | [citations/measurements/](citations/measurements/index.md) |
| Mechanism | 79531 | 242490 | [citations/mechanism/](citations/mechanism/index.md) |
| Medezinski | 2 | 2 | [citations/medezinski/](citations/medezinski/index.md) |
| Medicine | 108 | 9772 | [citations/medicine/](citations/medicine/index.md) |
| Medina | 7 | 11 | [citations/medina/](citations/medina/index.md) |
| Meech | 1 | 2 | [citations/meech/](citations/meech/index.md) |
| Megaparsec | 63 | 210 | [citations/megaparsec/](citations/megaparsec/index.md) |
| Mei | 520 | 6385 | [citations/mei/](citations/mei/index.md) |
| Melmed | 2 | 22 | [citations/melmed/](citations/melmed/index.md) |
| Melor | 2 | 4 | [citations/melor/](citations/melor/index.md) |
| Memory | 3350 | 35917 | [citations/memory/](citations/memory/index.md) |
| Memviewslicevalidateandinit | 4 | 16 | [citations/memviewslicevalidateandinit/](citations/memviewslicevalidateandinit/index.md) |
| Menanteau | 1 | 2 | [citations/menanteau/](citations/menanteau/index.md) |
| Menezes | 1 | 1 | [citations/menezes/](citations/menezes/index.md) |
| Menting | 229 | 303 | [citations/menting/](citations/menting/index.md) |
| Mercado | 4 | 9 | [citations/mercado/](citations/mercado/index.md) |
| Mercier | 9 | 12 | [citations/mercier/](citations/mercier/index.md) |
| Mercury | 361 | 1209 | [citations/mercury/](citations/mercury/index.md) |
| Merged | 614 | 2507 | [citations/merged/](citations/merged/index.md) |
| Mergevtables | 4 | 36 | [citations/mergevtables/](citations/mergevtables/index.md) |
| Merloni | 1 | 2 | [citations/merloni/](citations/merloni/index.md) |
| Merritt | 9 | 19 | [citations/merritt/](citations/merritt/index.md) |
| Merten | 1 | 2 | [citations/merten/](citations/merten/index.md) |
| Mertsch | 1 | 2 | [citations/mertsch/](citations/mertsch/index.md) |
| Meshcheryakov | 1 | 2 | [citations/meshcheryakov/](citations/meshcheryakov/index.md) |
| Messagesender | 12 | 80 | [citations/messagesender/](citations/messagesender/index.md) |
| Messenger | 121 | 217 | [citations/messenger/](citations/messenger/index.md) |
| Meta | 8738 | 55181 | [citations/meta/](citations/meta/index.md) |
| Metzger | 2 | 3 | [citations/metzger/](citations/metzger/index.md) |
| Michael | 8 | 14 | [citations/michael/](citations/michael/index.md) |
| Micheli | 1 | 2 | [citations/micheli/](citations/micheli/index.md) |
| Microbiology | 7 | 10 | [citations/microbiology/](citations/microbiology/index.md) |
| Microsoft | 244 | 1504 | [citations/microsoft/](citations/microsoft/index.md) |
| Mifflin | 1 | 2 | [citations/mifflin/](citations/mifflin/index.md) |
| Milgrom | 311 | 1158 | [citations/milgrom/](citations/milgrom/index.md) |
| Millan | 8 | 39 | [citations/millan/](citations/millan/index.md) |
| Miller | 60 | 138 | [citations/miller/](citations/miller/index.md) |
| Mills | 109 | 225 | [citations/mills/](citations/mills/index.md) |
| Milone | 2 | 7 | [citations/milone/](citations/milone/index.md) |
| Milton | 1501 | 8828 | [citations/milton/](citations/milton/index.md) |
| Mime | 499 | 3255 | [citations/mime/](citations/mime/index.md) |
| Minami | 1 | 2 | [citations/minami/](citations/minami/index.md) |
| Minazzoli | 1 | 2 | [citations/minazzoli/](citations/minazzoli/index.md) |
| Minimax | 447 | 5278 | [citations/minimax/](citations/minimax/index.md) |
| Minkowski | 380 | 820 | [citations/minkowski/](citations/minkowski/index.md) |
| Mistele | 2 | 3 | [citations/mistele/](citations/mistele/index.md) |
| Mistral | 318 | 3230 | [citations/mistral/](citations/mistral/index.md) |
| Mitch | 71 | 362 | [citations/mitch/](citations/mitch/index.md) |
| Mivilledeschenes | 2 | 3 | [citations/mivilledeschenes/](citations/mivilledeschenes/index.md) |
| Mmu | 2222 | 63865 | [citations/mmu/](citations/mmu/index.md) |
| Mnemosynelake | 126 | 1747 | [citations/mnemosynelake/](citations/mnemosynelake/index.md) |
| Mocz | 2 | 2 | [citations/mocz/](citations/mocz/index.md) |
| Modal | 875 | 6781 | [citations/modal/](citations/modal/index.md) |
| Mode | 52131 | 288861 | [citations/mode/](citations/mode/index.md) |
| Modified | 3216 | 11646 | [citations/modified/](citations/modified/index.md) |
| Moffat | 1 | 2 | [citations/moffat/](citations/moffat/index.md) |
| Moffett | 1 | 2 | [citations/moffett/](citations/moffett/index.md) |
| Mogul | 3 | 3 | [citations/mogul/](citations/mogul/index.md) |
| Moiseev | 3 | 3 | [citations/moiseev/](citations/moiseev/index.md) |
| Mojzsis | 1 | 1 | [citations/mojzsis/](citations/mojzsis/index.md) |
| Mok | 284 | 834 | [citations/mok/](citations/mok/index.md) |
| Molikawa | 1 | 2 | [citations/molikawa/](citations/molikawa/index.md) |
| Monjo | 5 | 13 | [citations/monjo/](citations/monjo/index.md) |
| Monte | 376 | 966 | [citations/monte/](citations/monte/index.md) |
| Montgomery | 1 | 2 | [citations/montgomery/](citations/montgomery/index.md) |
| Moonshot | 258 | 1526 | [citations/moonshot/](citations/moonshot/index.md) |
| Moore | 2 | 4 | [citations/moore/](citations/moore/index.md) |
| Morelli | 5 | 8 | [citations/morelli/](citations/morelli/index.md) |
| Moretti | 3 | 6 | [citations/moretti/](citations/moretti/index.md) |
| Morgan | 25 | 37 | [citations/morgan/](citations/morgan/index.md) |
| Morris | 1 | 2 | [citations/morris/](citations/morris/index.md) |
| Mortlock | 1 | 2 | [citations/mortlock/](citations/mortlock/index.md) |
| Morton | 1 | 2 | [citations/morton/](citations/morton/index.md) |
| Moschella | 29 | 55 | [citations/moschella/](citations/moschella/index.md) |
| Moss | 79 | 137 | [citations/moss/](citations/moss/index.md) |
| Moster | 1 | 2 | [citations/moster/](citations/moster/index.md) |
| Mottola | 12 | 46 | [citations/mottola/](citations/mottola/index.md) |
| Mousa | 14 | 50 | [citations/mousa/](citations/mousa/index.md) |
| Mroz | 8 | 17 | [citations/mroz/](citations/mroz/index.md) |
| Msun | 2458 | 17459 | [citations/msun/](citations/msun/index.md) |
| Mucciarelli | 4 | 7 | [citations/mucciarelli/](citations/mucciarelli/index.md) |
| Mueller | 1 | 2 | [citations/mueller/](citations/mueller/index.md) |
| Mukhanov | 1 | 2 | [citations/mukhanov/](citations/mukhanov/index.md) |
| Mukohyama | 1 | 4 | [citations/mukohyama/](citations/mukohyama/index.md) |
| Mulchaey | 3 | 5 | [citations/mulchaey/](citations/mulchaey/index.md) |
| Mulki | 2 | 3 | [citations/mulki/](citations/mulki/index.md) |
| Muller | 1 | 2 | [citations/muller/](citations/muller/index.md) |
| Multica | 25 | 49 | [citations/multica/](citations/multica/index.md) |
| Multiple | 3615 | 8483 | [citations/multiple/](citations/multiple/index.md) |
| Multiprocessing | 98 | 209 | [citations/multiprocessing/](citations/multiprocessing/index.md) |
| Munday | 1 | 1 | [citations/munday/](citations/munday/index.md) |
| Munoz | 9 | 131 | [citations/munoz/](citations/munoz/index.md) |
| Murgia | 1 | 2 | [citations/murgia/](citations/murgia/index.md) |
| Murray | 46 | 75 | [citations/murray/](citations/murray/index.md) |
| Murugeshan | 1 | 2 | [citations/murugeshan/](citations/murugeshan/index.md) |
| Musacchio | 2 | 3 | [citations/musacchio/](citations/musacchio/index.md) |
| Muse | 463 | 1916 | [citations/muse/](citations/muse/index.md) |
| Musedark | 1 | 1 | [citations/musedark/](citations/musedark/index.md) |
| Mutlu Pakdil | 2 | 4 | [citations/mutlu-pakdil/](citations/mutlu-pakdil/index.md) |
| Myers | 7 | 25 | [citations/myers/](citations/myers/index.md) |
| Myr | 362 | 5889 | [citations/myr/](citations/myr/index.md) |

</details>

<details><summary><b>N</b> · 72 names</summary>

| Name | Files | Occurrences | Citation page |
|---|---|---|---|
| N Body | 295 | 803 | [citations/n-body/](citations/n-body/index.md) |
| Naab | 1 | 2 | [citations/naab/](citations/naab/index.md) |
| Naacl | 20 | 44 | [citations/naacl/](citations/naacl/index.md) |
| Naaman | 4 | 4 | [citations/naaman/](citations/naaman/index.md) |
| Nadathur | 7 | 10 | [citations/nadathur/](citations/nadathur/index.md) |
| Nadler | 1 | 2 | [citations/nadler/](citations/nadler/index.md) |
| Naess | 5 | 7 | [citations/naess/](citations/naess/index.md) |
| Nagai | 51 | 105 | [citations/nagai/](citations/nagai/index.md) |
| Nagamine | 4 | 4 | [citations/nagamine/](citations/nagamine/index.md) |
| Nagesh | 1 | 2 | [citations/nagesh/](citations/nagesh/index.md) |
| Nagib | 2 | 3 | [citations/nagib/](citations/nagib/index.md) |
| Nagle | 8 | 40 | [citations/nagle/](citations/nagle/index.md) |
| Naidu | 1 | 2 | [citations/naidu/](citations/naidu/index.md) |
| Nakai | 8 | 36 | [citations/nakai/](citations/nakai/index.md) |
| Nakamura | 40 | 81 | [citations/nakamura/](citations/nakamura/index.md) |
| Namouni | 3 | 8 | [citations/namouni/](citations/namouni/index.md) |
| Nanoom | 54 | 54 | [citations/nanoom/](citations/nanoom/index.md) |
| Napolitano | 2 | 4 | [citations/napolitano/](citations/napolitano/index.md) |
| Naray | 16 | 43 | [citations/naray/](citations/naray/index.md) |
| Narnhofer | 72 | 88 | [citations/narnhofer/](citations/narnhofer/index.md) |
| Narovlansky | 2 | 4 | [citations/narovlansky/](citations/narovlansky/index.md) |
| Nasa | 163 | 1077 | [citations/nasa/](citations/nasa/index.md) |
| Nassar | 2 | 3 | [citations/nassar/](citations/nassar/index.md) |
| Natarajan | 1 | 2 | [citations/natarajan/](citations/natarajan/index.md) |
| Navarro | 58 | 115 | [citations/navarro/](citations/navarro/index.md) |
| Navas | 5 | 224 | [citations/navas/](citations/navas/index.md) |
| Ncimb | 27 | 312 | [citations/ncimb/](citations/ncimb/index.md) |
| Nebraska | 2 | 7 | [citations/nebraska/](citations/nebraska/index.md) |
| Necib | 1 | 2 | [citations/necib/](citations/necib/index.md) |
| Nedm | 49 | 179 | [citations/nedm/](citations/nedm/index.md) |
| Neeleman | 1 | 1 | [citations/neeleman/](citations/neeleman/index.md) |
| Neither | 2414 | 3940 | [citations/neither/](citations/neither/index.md) |
| Nejm | 8 | 34 | [citations/nejm/](citations/nejm/index.md) |
| Neklesa | 2 | 2 | [citations/neklesa/](citations/neklesa/index.md) |
| Nelson | 3 | 6 | [citations/nelson/](citations/nelson/index.md) |
| Ness | 1 | 1 | [citations/ness/](citations/ness/index.md) |
| Nestor Shachar | 10 | 18 | [citations/nestor-shachar/](citations/nestor-shachar/index.md) |
| Nestorshachar | 19 | 22 | [citations/nestorshachar/](citations/nestorshachar/index.md) |
| Neumann | 120 | 281 | [citations/neumann/](citations/neumann/index.md) |
| Neurips | 82 | 492 | [citations/neurips/](citations/neurips/index.md) |
| Neville | 5 | 5 | [citations/neville/](citations/neville/index.md) |
| Newell | 2 | 4 | [citations/newell/](citations/newell/index.md) |
| Newman | 1 | 2 | [citations/newman/](citations/newman/index.md) |
| Newton | 4003 | 18239 | [citations/newton/](citations/newton/index.md) |
| Nicastro | 1 | 2 | [citations/nicastro/](citations/nicastro/index.md) |
| Nicolis | 15 | 28 | [citations/nicolis/](citations/nicolis/index.md) |
| Nielsenninomiya | 1 | 1 | [citations/nielsenninomiya/](citations/nielsenninomiya/index.md) |
| Nightingale | 1 | 2 | [citations/nightingale/](citations/nightingale/index.md) |
| Nikolaev | 1 | 4 | [citations/nikolaev/](citations/nikolaev/index.md) |
| Nils | 144 | 4044 | [citations/nils/](citations/nils/index.md) |
| Nipoti | 1 | 2 | [citations/nipoti/](citations/nipoti/index.md) |
| Nissimov | 3 | 4 | [citations/nissimov/](citations/nissimov/index.md) |
| Nix | 1947 | 4398 | [citations/nix/](citations/nix/index.md) |
| Noaa | 119 | 694 | [citations/noaa/](citations/noaa/index.md) |
| Nobel | 62 | 115 | [citations/nobel/](citations/nobel/index.md) |
| Nolan | 3 | 3 | [citations/nolan/](citations/nolan/index.md) |
| Noordermeer | 1 | 2 | [citations/noordermeer/](citations/noordermeer/index.md) |
| Norberg | 2 | 10 | [citations/norberg/](citations/norberg/index.md) |
| Norman | 2 | 4 | [citations/norman/](citations/norman/index.md) |
| Norris | 6 | 42 | [citations/norris/](citations/norris/index.md) |
| Nous | 1511 | 22562 | [citations/nous/](citations/nous/index.md) |
| Nov | 79995 | 94139 | [citations/nov/](citations/nov/index.md) |
| Nozawa | 1 | 2 | [citations/nozawa/](citations/nozawa/index.md) |
| Nrao | 6 | 68 | [citations/nrao/](citations/nrao/index.md) |
| Nufit | 96 | 308 | [citations/nufit/](citations/nufit/index.md) |
| Nunes | 3 | 4 | [citations/nunes/](citations/nunes/index.md) |
| Nuri | 17 | 63 | [citations/nuri/](citations/nuri/index.md) |
| Nusser | 51 | 81 | [citations/nusser/](citations/nusser/index.md) |
| Nutrition | 34 | 166 | [citations/nutrition/](citations/nutrition/index.md) |
| Nvidia | 307 | 2118 | [citations/nvidia/](citations/nvidia/index.md) |
| Nygaard | 4 | 11 | [citations/nygaard/](citations/nygaard/index.md) |
| Nyman | 2 | 3 | [citations/nyman/](citations/nyman/index.md) |

</details>

<details><summary><b>O</b> · 51 names</summary>

| Name | Files | Occurrences | Citation page |
|---|---|---|---|
| O Zone | 35 | 188 | [citations/o-zone/](citations/o-zone/index.md) |
| Oauth | 650 | 10397 | [citations/oauth/](citations/oauth/index.md) |
| Obes | 4 | 17 | [citations/obes/](citations/obes/index.md) |
| Obied | 1 | 2 | [citations/obied/](citations/obied/index.md) |
| Obreschkow | 2 | 5 | [citations/obreschkow/](citations/obreschkow/index.md) |
| Observation | 2628 | 10962 | [citations/observation/](citations/observation/index.md) |
| Observatory | 76 | 134 | [citations/observatory/](citations/observatory/index.md) |
| Oct | 3587 | 10208 | [citations/oct/](citations/oct/index.md) |
| Oda | 3450 | 17892 | [citations/oda/](citations/oda/index.md) |
| Odlyzko | 2 | 3 | [citations/odlyzko/](citations/odlyzko/index.md) |
| Odom | 423 | 1743 | [citations/odom/](citations/odom/index.md) |
| Oei | 41 | 170 | [citations/oei/](citations/oei/index.md) |
| Oesch | 8 | 58 | [citations/oesch/](citations/oesch/index.md) |
| Oguri | 1 | 2 | [citations/oguri/](citations/oguri/index.md) |
| Okabe | 2 | 4 | [citations/okabe/](citations/okabe/index.md) |
| Okamoto | 7 | 24 | [citations/okamoto/](citations/okamoto/index.md) |
| Oke | 6459 | 94945 | [citations/oke/](citations/oke/index.md) |
| Okuyama | 55 | 172 | [citations/okuyama/](citations/okuyama/index.md) |
| Olive | 63 | 274 | [citations/olive/](citations/olive/index.md) |
| Olson | 21 | 40 | [citations/olson/](citations/olson/index.md) |
| Olympusdaemon | 16 | 27756 | [citations/olympusdaemon/](citations/olympusdaemon/index.md) |
| Olympusflow | 324 | 2110 | [citations/olympusflow/](citations/olympusflow/index.md) |
| Oman | 6 | 29 | [citations/oman/](citations/oman/index.md) |
| Omega | 6911 | 56237 | [citations/omega/](citations/omega/index.md) |
| Oncol | 64 | 436 | [citations/oncol/](citations/oncol/index.md) |
| Only | 15535 | 72515 | [citations/only/](citations/only/index.md) |
| Ontario | 5 | 19 | [citations/ontario/](citations/ontario/index.md) |
| Oosv | 1 | 2 | [citations/oosv/](citations/oosv/index.md) |
| Openclaw | 283 | 3464 | [citations/openclaw/](citations/openclaw/index.md) |
| Opencode | 234 | 2580 | [citations/opencode/](citations/opencode/index.md) |
| Openstreetmap | 9 | 33 | [citations/openstreetmap/](citations/openstreetmap/index.md) |
| Operator | 6628 | 114235 | [citations/operator/](citations/operator/index.md) |
| Opml | 7 | 19 | [citations/opml/](citations/opml/index.md) |
| Opportunity | 103 | 161 | [citations/opportunity/](citations/opportunity/index.md) |
| Opt | 12515 | 79944 | [citations/opt/](citations/opt/index.md) |
| Orbifold | 570 | 3942 | [citations/orbifold/](citations/orbifold/index.md) |
| Organization | 247 | 1024 | [citations/organization/](citations/organization/index.md) |
| Orientation | 529 | 1287 | [citations/orientation/](citations/orientation/index.md) |
| Original | 4052 | 16156 | [citations/original/](citations/original/index.md) |
| Orionis | 3 | 185 | [citations/orionis/](citations/orionis/index.md) |
| Orpheus | 18 | 349 | [citations/orpheus/](citations/orpheus/index.md) |
| Osmond | 1 | 2 | [citations/osmond/](citations/osmond/index.md) |
| Ostriker | 43 | 85 | [citations/ostriker/](citations/ostriker/index.md) |
| Ott | 3061 | 15581 | [citations/ott/](citations/ott/index.md) |
| Ouriaghli | 2 | 2 | [citations/ouriaghli/](citations/ouriaghli/index.md) |
| Outmezguine | 1 | 2 | [citations/outmezguine/](citations/outmezguine/index.md) |
| Outside | 5925 | 9022 | [citations/outside/](citations/outside/index.md) |
| Owers | 968 | 1806 | [citations/owers/](citations/owers/index.md) |
| Owneddictnext | 4 | 24 | [citations/owneddictnext/](citations/owneddictnext/index.md) |
| Oxnard | 1 | 2 | [citations/oxnard/](citations/oxnard/index.md) |
| Ozel | 2 | 4 | [citations/ozel/](citations/ozel/index.md) |

</details>

<details><summary><b>P</b> · 133 names</summary>

| Name | Files | Occurrences | Citation page |
|---|---|---|---|
| Pac | 19141 | 167939 | [citations/pac/](citations/pac/index.md) |
| Padilla | 11 | 20 | [citations/padilla/](citations/padilla/index.md) |
| Padmanabhan | 106 | 211 | [citations/padmanabhan/](citations/padmanabhan/index.md) |
| Page | 2712 | 19546 | [citations/page/](citations/page/index.md) |
| Palik | 7 | 15 | [citations/palik/](citations/palik/index.md) |
| Pan Starrs | 7 | 12 | [citations/pan-starrs/](citations/pan-starrs/index.md) |
| Pandhi | 1 | 1 | [citations/pandhi/](citations/pandhi/index.md) |
| Panja | 2 | 4 | [citations/panja/](citations/panja/index.md) |
| Pannella | 2 | 2 | [citations/pannella/](citations/pannella/index.md) |
| Pantheon | 212 | 707 | [citations/pantheon/](citations/pantheon/index.md) |
| Papalini | 4 | 8 | [citations/papalini/](citations/papalini/index.md) |
| Papastergis | 1 | 2 | [citations/papastergis/](citations/papastergis/index.md) |
| Paraficz | 5 | 7 | [citations/paraficz/](citations/paraficz/index.md) |
| Paranjape | 3 | 5 | [citations/paranjape/](citations/paranjape/index.md) |
| Park | 51 | 99 | [citations/park/](citations/park/index.md) |
| Parma | 18 | 47 | [citations/parma/](citations/parma/index.md) |
| Parodi | 3 | 6 | [citations/parodi/](citations/parodi/index.md) |
| Parravano | 1 | 2 | [citations/parravano/](citations/parravano/index.md) |
| Parsekeywordsimpl | 4 | 28 | [citations/parsekeywordsimpl/](citations/parsekeywordsimpl/index.md) |
| Pat | 69085 | 422629 | [citations/pat/](citations/pat/index.md) |
| Pauco | 1 | 2 | [citations/pauco/](citations/pauco/index.md) |
| Paulin Henriksson | 2 | 2 | [citations/paulin-henriksson/](citations/paulin-henriksson/index.md) |
| Pauling | 33 | 139 | [citations/pauling/](citations/pauling/index.md) |
| Pavlov | 3 | 5 | [citations/pavlov/](citations/pavlov/index.md) |
| Pawliuk | 1 | 1 | [citations/pawliuk/](citations/pawliuk/index.md) |
| Pawlowski | 50 | 98 | [citations/pawlowski/](citations/pawlowski/index.md) |
| Pecaut | 5 | 8 | [citations/pecaut/](citations/pecaut/index.md) |
| Peccei Quinn | 30 | 44 | [citations/peccei-quinn/](citations/peccei-quinn/index.md) |
| Peebles | 1 | 2 | [citations/peebles/](citations/peebles/index.md) |
| Peeples | 2 | 2 | [citations/peeples/](citations/peeples/index.md) |
| Peg | 2646 | 40796 | [citations/peg/](citations/peg/index.md) |
| Peiris | 1 | 2 | [citations/peiris/](citations/peiris/index.md) |
| Pellegrino | 2 | 2 | [citations/pellegrino/](citations/pellegrino/index.md) |
| Pelliccia | 3 | 5 | [citations/pelliccia/](citations/pelliccia/index.md) |
| Peloso | 1 | 2 | [citations/peloso/](citations/peloso/index.md) |
| Penarrubia | 1 | 2 | [citations/penarrubia/](citations/penarrubia/index.md) |
| Pendleton Ross | 3 | 14 | [citations/pendleton-ross/](citations/pendleton-ross/index.md) |
| Penedones | 5 | 8 | [citations/penedones/](citations/penedones/index.md) |
| Peng | 7 | 34 | [citations/peng/](citations/peng/index.md) |
| Pep | 3183 | 152186 | [citations/pep/](citations/pep/index.md) |
| Pequignot | 1 | 2 | [citations/pequignot/](citations/pequignot/index.md) |
| Perlick | 2 | 3 | [citations/perlick/](citations/perlick/index.md) |
| Perlmutter | 1 | 2 | [citations/perlmutter/](citations/perlmutter/index.md) |
| Perry | 18 | 66 | [citations/perry/](citations/perry/index.md) |
| Perside | 31 | 79 | [citations/perside/](citations/perside/index.md) |
| Pesce | 2 | 3 | [citations/pesce/](citations/pesce/index.md) |
| Peter | 3 | 7 | [citations/peter/](citations/peter/index.md) |
| Petigura | 1 | 1 | [citations/petigura/](citations/petigura/index.md) |
| Petsko | 35 | 84 | [citations/petsko/](citations/petsko/index.md) |
| Pettini | 1 | 2 | [citations/pettini/](citations/pettini/index.md) |
| Pfas | 68 | 513 | [citations/pfas/](citations/pfas/index.md) |
| Pfautsch | 2 | 3 | [citations/pfautsch/](citations/pfautsch/index.md) |
| Pfeifer | 8 | 12 | [citations/pfeifer/](citations/pfeifer/index.md) |
| Pfenniger | 1 | 14 | [citations/pfenniger/](citations/pfenniger/index.md) |
| Phan | 2510 | 14815 | [citations/phan/](citations/phan/index.md) |
| Phenomenon | 191 | 255 | [citations/phenomenon/](citations/phenomenon/index.md) |
| Phi | 86347 | 303635 | [citations/phi/](citations/phi/index.md) |
| Philcox | 1 | 2 | [citations/philcox/](citations/philcox/index.md) |
| Phys | 14446 | 91819 | [citations/phys/](citations/phys/index.md) |
| Picciotto | 1 | 1 | [citations/picciotto/](citations/picciotto/index.md) |
| Pier | 150 | 1193 | [citations/pier/](citations/pier/index.md) |
| Pietrzynski | 5 | 5 | [citations/pietrzynski/](citations/pietrzynski/index.md) |
| Piffaretti | 1 | 2 | [citations/piffaretti/](citations/piffaretti/index.md) |
| Pik | 507 | 42049 | [citations/pik/](citations/pik/index.md) |
| Pil | 7239 | 30428 | [citations/pil/](citations/pil/index.md) |
| Pimbblet | 2 | 13 | [citations/pimbblet/](citations/pimbblet/index.md) |
| Pina | 82 | 452 | [citations/pina/](citations/pina/index.md) |
| Piotrowska | 1 | 1 | [citations/piotrowska/](citations/piotrowska/index.md) |
| Piotto | 1 | 4 | [citations/piotto/](citations/piotto/index.md) |
| Piran | 6 | 11 | [citations/piran/](citations/piran/index.md) |
| Pisanti | 1 | 1 | [citations/pisanti/](citations/pisanti/index.md) |
| Piskunov | 2 | 2 | [citations/piskunov/](citations/piskunov/index.md) |
| Pitjev | 1 | 2 | [citations/pitjev/](citations/pitjev/index.md) |
| Pitrou | 13 | 55 | [citations/pitrou/](citations/pitrou/index.md) |
| Pittordis | 1 | 2 | [citations/pittordis/](citations/pittordis/index.md) |
| Pizzuti | 1 | 2 | [citations/pizzuti/](citations/pizzuti/index.md) |
| Planelles | 1 | 2 | [citations/planelles/](citations/planelles/index.md) |
| Plastino | 1 | 2 | [citations/plastino/](citations/plastino/index.md) |
| Pnas | 362 | 1591 | [citations/pnas/](citations/pnas/index.md) |
| Pointecouteau | 1 | 2 | [citations/pointecouteau/](citations/pointecouteau/index.md) |
| Pois | 1389 | 6490 | [citations/pois/](citations/pois/index.md) |
| Polchinski | 18 | 25 | [citations/polchinski/](citations/polchinski/index.md) |
| Pole | 2894 | 16707 | [citations/pole/](citations/pole/index.md) |
| Polnarev | 1 | 2 | [citations/polnarev/](citations/polnarev/index.md) |
| Polyakov | 1 | 2 | [citations/polyakov/](citations/polyakov/index.md) |
| Pond | 2354 | 14002 | [citations/pond/](citations/pond/index.md) |
| Ponman | 1 | 2 | [citations/ponman/](citations/ponman/index.md) |
| Ponomareva | 9 | 31 | [citations/ponomareva/](citations/ponomareva/index.md) |
| Pontzen | 1 | 2 | [citations/pontzen/](citations/pontzen/index.md) |
| Popesso | 13 | 43 | [citations/popesso/](citations/popesso/index.md) |
| Popolo | 2 | 3 | [citations/popolo/](citations/popolo/index.md) |
| Popovic | 1 | 2 | [citations/popovic/](citations/popovic/index.md) |
| Porquet | 1 | 1 | [citations/porquet/](citations/porquet/index.md) |
| Portal | 360 | 2559 | [citations/portal/](citations/portal/index.md) |
| Pos | 32569 | 145115 | [citations/pos/](citations/pos/index.md) |
| Poulin | 1 | 2 | [citations/poulin/](citations/poulin/index.md) |
| Powell | 2 | 6 | [citations/powell/](citations/powell/index.md) |
| Powershell | 66 | 443 | [citations/powershell/](citations/powershell/index.md) |
| Ppo Lite | 8 | 8 | [citations/ppo-lite/](citations/ppo-lite/index.md) |
| Prad | 48 | 337 | [citations/prad/](citations/prad/index.md) |
| Prasad | 24 | 31 | [citations/prasad/](citations/prasad/index.md) |
| Prep | 1764 | 9749 | [citations/prep/](citations/prep/index.md) |
| Preregistration | 176 | 337 | [citations/preregistration/](citations/preregistration/index.md) |
| Prex Ii | 5 | 18 | [citations/prex-ii/](citations/prex-ii/index.md) |
| Price | 3934 | 12275 | [citations/price/](citations/price/index.md) |
| Primack | 7 | 19 | [citations/primack/](citations/primack/index.md) |
| Principle | 4566 | 18462 | [citations/principle/](citations/principle/index.md) |
| Prize | 163 | 295 | [citations/prize/](citations/prize/index.md) |
| Probiotics | 2 | 2 | [citations/probiotics/](citations/probiotics/index.md) |
| Prochaska | 1 | 2 | [citations/prochaska/](citations/prochaska/index.md) |
| Profumo | 3 | 5 | [citations/profumo/](citations/profumo/index.md) |
| Properties | 1990 | 6445 | [citations/properties/](citations/properties/index.md) |
| Proposal | 548 | 1362 | [citations/proposal/](citations/proposal/index.md) |
| Propris | 2 | 4 | [citations/propris/](citations/propris/index.md) |
| Protocol | 5263 | 8042 | [citations/protocol/](citations/protocol/index.md) |
| Protsiv | 2 | 3 | [citations/protsiv/](citations/protsiv/index.md) |
| Proven | 3463 | 6241 | [citations/proven/](citations/proven/index.md) |
| Provider | 2356 | 73676 | [citations/provider/](citations/provider/index.md) |
| Prugniel | 5 | 9 | [citations/prugniel/](citations/prugniel/index.md) |
| Psaltis | 5 | 8 | [citations/psaltis/](citations/psaltis/index.md) |
| Psi | 10394 | 69844 | [citations/psi/](citations/psi/index.md) |
| Ptep | 35 | 200 | [citations/ptep/](citations/ptep/index.md) |
| Public | 2812 | 7200 | [citations/public/](citations/public/index.md) |
| Published | 3299 | 10780 | [citations/published/](citations/published/index.md) |
| Puchwein | 1 | 2 | [citations/puchwein/](citations/puchwein/index.md) |
| Pujolas | 1 | 2 | [citations/pujolas/](citations/pujolas/index.md) |
| Pulicherla | 1 | 1 | [citations/pulicherla/](citations/pulicherla/index.md) |
| Pure | 7456 | 14332 | [citations/pure/](citations/pure/index.md) |
| Pusz | 20 | 44 | [citations/pusz/](citations/pusz/index.md) |
| Pydantic | 183 | 996 | [citations/pydantic/](citations/pydantic/index.md) |
| Pyobject | 10 | 38400 | [citations/pyobject/](citations/pyobject/index.md) |
| Pypi | 146 | 1576 | [citations/pypi/](citations/pypi/index.md) |
| Pytype | 4 | 1548 | [citations/pytype/](citations/pytype/index.md) |

</details>

<details><summary><b>Q</b> · 12 names</summary>

| Name | Files | Occurrences | Citation page |
|---|---|---|---|
| Qed | 554 | 7600 | [citations/qed/](citations/qed/index.md) |
| Qin | 132 | 5192 | [citations/qin/](citations/qin/index.md) |
| Qoura | 1 | 1 | [citations/qoura/](citations/qoura/index.md) |
| Quack | 6 | 6 | [citations/quack/](citations/quack/index.md) |
| Quadri | 2 | 4 | [citations/quadri/](citations/quadri/index.md) |
| Quantum | 3454 | 8537 | [citations/quantum/](citations/quantum/index.md) |
| Quataert | 1 | 2 | [citations/quataert/](citations/quataert/index.md) |
| Quilis | 2 | 2 | [citations/quilis/](citations/quilis/index.md) |
| Quinn | 64 | 140 | [citations/quinn/](citations/quinn/index.md) |
| Quintana | 2 | 3 | [citations/quintana/](citations/quintana/index.md) |
| Quintin | 7 | 9 | [citations/quintin/](citations/quintin/index.md) |
| Quiros | 1 | 1 | [citations/quiros/](citations/quiros/index.md) |

</details>

<details><summary><b>R</b> · 96 names</summary>

| Name | Files | Occurrences | Citation page |
|---|---|---|---|
| Raamsdonk | 1 | 2 | [citations/raamsdonk/](citations/raamsdonk/index.md) |
| Rabinowitz | 1 | 2 | [citations/rabinowitz/](citations/rabinowitz/index.md) |
| Radziwill | 1 | 2 | [citations/radziwill/](citations/radziwill/index.md) |
| Raghavan | 6 | 7 | [citations/raghavan/](citations/raghavan/index.md) |
| Rahman | 2 | 5 | [citations/rahman/](citations/rahman/index.md) |
| Rahvar | 8 | 9 | [citations/rahvar/](citations/rahvar/index.md) |
| Raj | 1063 | 5443 | [citations/raj/](citations/raj/index.md) |
| Ralph | 38 | 46 | [citations/ralph/](citations/ralph/index.md) |
| Ramachandran | 3196 | 6524 | [citations/ramachandran/](citations/ramachandran/index.md) |
| Ramalingam | 1 | 1 | [citations/ramalingam/](citations/ramalingam/index.md) |
| Ramazanov | 1 | 1 | [citations/ramazanov/](citations/ramazanov/index.md) |
| Randall | 104 | 243 | [citations/randall/](citations/randall/index.md) |
| Raptor'S | 4 | 8 | [citations/raptor's/](citations/raptor's/index.md) |
| Rasmussen | 1 | 2 | [citations/rasmussen/](citations/rasmussen/index.md) |
| Rasp | 65 | 445 | [citations/rasp/](citations/rasp/index.md) |
| Rassoul | 1 | 2 | [citations/rassoul/](citations/rassoul/index.md) |
| Rattazzi | 10 | 16 | [citations/rattazzi/](citations/rattazzi/index.md) |
| Ray | 38540 | 102870 | [citations/ray/](citations/ray/index.md) |
| Real | 87127 | 157488 | [citations/real/](citations/real/index.md) |
| Reasor | 1 | 1 | [citations/reasor/](citations/reasor/index.md) |
| Reassessment | 46 | 74 | [citations/reassessment/](citations/reassessment/index.md) |
| Reed | 2526 | 8751 | [citations/reed/](citations/reed/index.md) |
| Rees | 8 | 34 | [citations/rees/](citations/rees/index.md) |
| Reffert | 1 | 2 | [citations/reffert/](citations/reffert/index.md) |
| Refinement | 5947 | 28118 | [citations/refinement/](citations/refinement/index.md) |
| Reformulation | 74 | 160 | [citations/reformulation/](citations/reformulation/index.md) |
| Refs | 538 | 2915 | [citations/refs/](citations/refs/index.md) |
| Reid | 1 | 2 | [citations/reid/](citations/reid/index.md) |
| Reiprich | 1 | 2 | [citations/reiprich/](citations/reiprich/index.md) |
| Relativity | 502 | 1303 | [citations/relativity/](citations/relativity/index.md) |
| Release | 1772 | 8058 | [citations/release/](citations/release/index.md) |
| Remus | 7 | 11 | [citations/remus/](citations/remus/index.md) |
| Ren | 23790 | 189880 | [citations/ren/](citations/ren/index.md) |
| Renou | 1 | 3 | [citations/renou/](citations/renou/index.md) |
| Research | 5933 | 66329 | [citations/research/](citations/research/index.md) |
| Resolution | 6374 | 50432 | [citations/resolution/](citations/resolution/index.md) |
| Resolved | 2775 | 18496 | [citations/resolved/](citations/resolved/index.md) |
| Resonated | 7 | 9 | [citations/resonated/](citations/resonated/index.md) |
| Retherford | 2 | 2 | [citations/retherford/](citations/retherford/index.md) |
| Retracted | 360 | 953 | [citations/retracted/](citations/retracted/index.md) |
| Retractions | 97 | 247 | [citations/retractions/](citations/retractions/index.md) |
| Retrieval | 223 | 462 | [citations/retrieval/](citations/retrieval/index.md) |
| Revaz | 1 | 2 | [citations/revaz/](citations/revaz/index.md) |
| Revision | 590 | 1351 | [citations/revision/](citations/revision/index.md) |
| Revival | 24 | 43 | [citations/revival/](citations/revival/index.md) |
| Reyes | 24 | 86 | [citations/reyes/](citations/reyes/index.md) |
| Rezchikov | 1 | 2 | [citations/rezchikov/](citations/rezchikov/index.md) |
| Rhee | 1 | 2 | [citations/rhee/](citations/rhee/index.md) |
| Richards | 1 | 2 | [citations/richards/](citations/richards/index.md) |
| Ricotti | 7 | 28 | [citations/ricotti/](citations/ricotti/index.md) |
| Riele | 12 | 18 | [citations/riele/](citations/riele/index.md) |
| Riess | 2 | 4 | [citations/riess/](citations/riess/index.md) |
| Riet | 467 | 874 | [citations/riet/](citations/riet/index.md) |
| Rigidity | 166 | 431 | [citations/rigidity/](citations/rigidity/index.md) |
| Rihtarsic | 6 | 8 | [citations/rihtarsic/](citations/rihtarsic/index.md) |
| Rindler Daller | 1 | 1 | [citations/rindler-daller/](citations/rindler-daller/index.md) |
| Rines | 73 | 148 | [citations/rines/](citations/rines/index.md) |
| Rising | 1633 | 5829 | [citations/rising/](citations/rising/index.md) |
| Rita | 877 | 2883 | [citations/rita/](citations/rita/index.md) |
| Ritchie | 1 | 2 | [citations/ritchie/](citations/ritchie/index.md) |
| Rives | 2796 | 4194 | [citations/rives/](citations/rives/index.md) |
| Rix | 3940 | 52648 | [citations/rix/](citations/rix/index.md) |
| Rizzi | 6 | 15 | [citations/rizzi/](citations/rizzi/index.md) |
| Rizzo | 13 | 16 | [citations/rizzo/](citations/rizzo/index.md) |
| Robbia | 2 | 4 | [citations/robbia/](citations/robbia/index.md) |
| Robertson | 27 | 38 | [citations/robertson/](citations/robertson/index.md) |
| Robin | 318 | 145719 | [citations/robin/](citations/robin/index.md) |
| Robotham | 1 | 2 | [citations/robotham/](citations/robotham/index.md) |
| Rocha Pinto | 1 | 2 | [citations/rocha-pinto/](citations/rocha-pinto/index.md) |
| Rockmore | 2 | 4 | [citations/rockmore/](citations/rockmore/index.md) |
| Rodgers Tao | 5 | 7 | [citations/rodgers-tao/](citations/rodgers-tao/index.md) |
| Rodrigues | 1 | 2 | [citations/rodrigues/](citations/rodrigues/index.md) |
| Roeser | 1 | 2 | [citations/roeser/](citations/roeser/index.md) |
| Rogers | 1 | 2 | [citations/rogers/](citations/rogers/index.md) |
| Roman | 40 | 101 | [citations/roman/](citations/roman/index.md) |
| Rood | 7 | 23 | [citations/rood/](citations/rood/index.md) |
| Roper | 5946 | 17511 | [citations/roper/](citations/roper/index.md) |
| Rorai | 1 | 1 | [citations/rorai/](citations/rorai/index.md) |
| Rosetta | 70 | 331 | [citations/rosetta/](citations/rosetta/index.md) |
| Roshan | 419 | 419 | [citations/roshan/](citations/roshan/index.md) |
| Roshko | 2 | 3 | [citations/roshko/](citations/roshko/index.md) |
| Rotation | 3035 | 12759 | [citations/rotation/](citations/rotation/index.md) |
| Rotmod | 341 | 1322 | [citations/rotmod/](citations/rotmod/index.md) |
| Rousselle | 1 | 2 | [citations/rousselle/](citations/rousselle/index.md) |
| Route | 4935 | 31771 | [citations/route/](citations/route/index.md) |
| Rowland | 1 | 2 | [citations/rowland/](citations/rowland/index.md) |
| Roy | 816 | 1862 | [citations/roy/](citations/roy/index.md) |
| Rubin | 2 | 4 | [citations/rubin/](citations/rubin/index.md) |
| Rudakovskyi | 1 | 1 | [citations/rudakovskyi/](citations/rudakovskyi/index.md) |
| Rudie | 1 | 2 | [citations/rudie/](citations/rudie/index.md) |
| Rudnick | 2 | 5 | [citations/rudnick/](citations/rudnick/index.md) |
| Rule | 3866 | 14475 | [citations/rule/](citations/rule/index.md) |
| Ruscio | 5 | 7 | [citations/ruscio/](citations/ruscio/index.md) |
| Russell | 40 | 80 | [citations/russell/](citations/russell/index.md) |
| Russi | 246 | 336 | [citations/russi/](citations/russi/index.md) |
| Ruth | 1641 | 15008 | [citations/ruth/](citations/ruth/index.md) |

</details>

<details><summary><b>S</b> · 212 names</summary>

| Name | Files | Occurrences | Citation page |
|---|---|---|---|
| Saad | 2 | 4 | [citations/saad/](citations/saad/index.md) |
| Saar | 39 | 955 | [citations/saar/](citations/saar/index.md) |
| Saba | 36 | 200 | [citations/saba/](citations/saba/index.md) |
| Sackett | 1 | 1 | [citations/sackett/](citations/sackett/index.md) |
| Sage | 6069 | 127041 | [citations/sage/](citations/sage/index.md) |
| Sagi | 620 | 3870 | [citations/sagi/](citations/sagi/index.md) |
| Sah | 331 | 7390 | [citations/sah/](citations/sah/index.md) |
| Sakagami | 1 | 1 | [citations/sakagami/](citations/sakagami/index.md) |
| Sakai | 1 | 2 | [citations/sakai/](citations/sakai/index.md) |
| Sakharov | 34 | 72 | [citations/sakharov/](citations/sakharov/index.md) |
| Salami | 4 | 8 | [citations/salami/](citations/salami/index.md) |
| Salamon | 1 | 3 | [citations/salamon/](citations/salamon/index.md) |
| Salas | 12 | 113 | [citations/salas/](citations/salas/index.md) |
| Salati | 1 | 5 | [citations/salati/](citations/salati/index.md) |
| Salcedo | 11 | 16 | [citations/salcedo/](citations/salcedo/index.md) |
| Salo | 18 | 51 | [citations/salo/](citations/salo/index.md) |
| Saltas | 1 | 2 | [citations/saltas/](citations/saltas/index.md) |
| Salvio | 1 | 2 | [citations/salvio/](citations/salvio/index.md) |
| Saminadayar | 1 | 1 | [citations/saminadayar/](citations/saminadayar/index.md) |
| Samoylova | 2 | 2 | [citations/samoylova/](citations/samoylova/index.md) |
| Samuel | 2 | 4 | [citations/samuel/](citations/samuel/index.md) |
| Sanchez | 22 | 28 | [citations/sanchez/](citations/sanchez/index.md) |
| Sancisi | 30 | 59 | [citations/sancisi/](citations/sancisi/index.md) |
| Sand | 1318 | 7476 | [citations/sand/](citations/sand/index.md) |
| Sanders | 113 | 225 | [citations/sanders/](citations/sanders/index.md) |
| Sano | 2 | 3 | [citations/sano/](citations/sano/index.md) |
| Sans | 438 | 3467 | [citations/sans/](citations/sans/index.md) |
| Santos Santos | 1 | 2 | [citations/santos-santos/](citations/santos-santos/index.md) |
| Sarkar | 63 | 169 | [citations/sarkar/](citations/sarkar/index.md) |
| Sartoris | 1 | 1 | [citations/sartoris/](citations/sartoris/index.md) |
| Satellites | 255 | 891 | [citations/satellites/](citations/satellites/index.md) |
| Saunders | 9 | 27 | [citations/saunders/](citations/saunders/index.md) |
| Saveresetexception | 4 | 16 | [citations/saveresetexception/](citations/saveresetexception/index.md) |
| Savir | 9 | 36 | [citations/savir/](citations/savir/index.md) |
| Saxena | 5 | 6 | [citations/saxena/](citations/saxena/index.md) |
| Sazhin | 1 | 4 | [citations/sazhin/](citations/sazhin/index.md) |
| Scaramella | 1 | 1 | [citations/scaramella/](citations/scaramella/index.md) |
| Scarlett | 9 | 13 | [citations/scarlett/](citations/scarlett/index.md) |
| Schaan | 1 | 2 | [citations/schaan/](citations/schaan/index.md) |
| Schael | 1 | 1 | [citations/schael/](citations/schael/index.md) |
| Schaye | 1 | 2 | [citations/schaye/](citations/schaye/index.md) |
| Schecter | 1 | 1 | [citations/schecter/](citations/schecter/index.md) |
| Schellenberger | 1 | 2 | [citations/schellenberger/](citations/schellenberger/index.md) |
| Scherrer | 21 | 44 | [citations/scherrer/](citations/scherrer/index.md) |
| Scherzinger | 1 | 1 | [citations/scherzinger/](citations/scherzinger/index.md) |
| Schilbach | 4 | 5 | [citations/schilbach/](citations/schilbach/index.md) |
| Schirmer | 9 | 18 | [citations/schirmer/](citations/schirmer/index.md) |
| Schlafli | 1 | 2 | [citations/schlafli/](citations/schlafli/index.md) |
| Schlamminger | 5 | 5 | [citations/schlamminger/](citations/schlamminger/index.md) |
| Schmidt | 97 | 234 | [citations/schmidt/](citations/schmidt/index.md) |
| Schneider | 2 | 4 | [citations/schneider/](citations/schneider/index.md) |
| Schober | 3 | 4 | [citations/schober/](citations/schober/index.md) |
| Schoenmakers | 2 | 14 | [citations/schoenmakers/](citations/schoenmakers/index.md) |
| Scholarpedia | 16 | 22 | [citations/scholarpedia/](citations/scholarpedia/index.md) |
| Scholtz | 2 | 2 | [citations/scholtz/](citations/scholtz/index.md) |
| Scholze | 22 | 103 | [citations/scholze/](citations/scholze/index.md) |
| Schombert | 145 | 289 | [citations/schombert/](citations/schombert/index.md) |
| Schon | 7 | 12 | [citations/schon/](citations/schon/index.md) |
| Schouws | 1 | 2 | [citations/schouws/](citations/schouws/index.md) |
| Schrabback | 3 | 10 | [citations/schrabback/](citations/schrabback/index.md) |
| Schreiber | 12 | 18 | [citations/schreiber/](citations/schreiber/index.md) |
| Schubert | 1 | 2 | [citations/schubert/](citations/schubert/index.md) |
| Schulz | 1 | 2 | [citations/schulz/](citations/schulz/index.md) |
| Schwarze | 5 | 8 | [citations/schwarze/](citations/schwarze/index.md) |
| Schwarzschild | 358 | 1011 | [citations/schwarzschild/](citations/schwarzschild/index.md) |
| Schwinger | 122 | 288 | [citations/schwinger/](citations/schwinger/index.md) |
| Sciama | 25 | 44 | [citations/sciama/](citations/sciama/index.md) |
| Scoccimarro | 1 | 2 | [citations/scoccimarro/](citations/scoccimarro/index.md) |
| Scorecard | 141 | 290 | [citations/scorecard/](citations/scorecard/index.md) |
| Scott | 8 | 16 | [citations/scott/](citations/scott/index.md) |
| Scovil | 1 | 1 | [citations/scovil/](citations/scovil/index.md) |
| Screenshot | 381 | 2297 | [citations/screenshot/](citations/screenshot/index.md) |
| Scrollbox | 96 | 340 | [citations/scrollbox/](citations/scrollbox/index.md) |
| Scutaru | 1 | 2 | [citations/scutaru/](citations/scutaru/index.md) |
| Seager | 1 | 2 | [citations/seager/](citations/seager/index.md) |
| Seb | 221 | 1477 | [citations/seb/](citations/seb/index.md) |
| Sec | 91784 | 373448 | [citations/sec/](citations/sec/index.md) |
| Seeley | 1 | 2 | [citations/seeley/](citations/seeley/index.md) |
| Segmental | 3 | 6 | [citations/segmental/](citations/segmental/index.md) |
| Seikel | 11 | 20 | [citations/seikel/](citations/seikel/index.md) |
| Sekanina | 1 | 1 | [citations/sekanina/](citations/sekanina/index.md) |
| Selberg | 55 | 310 | [citations/selberg/](citations/selberg/index.md) |
| Seligman | 1 | 2 | [citations/seligman/](citations/seligman/index.md) |
| Sellwood | 4 | 6 | [citations/sellwood/](citations/sellwood/index.md) |
| Seng | 209 | 1809 | [citations/seng/](citations/seng/index.md) |
| Sennrich | 1 | 2 | [citations/sennrich/](citations/sennrich/index.md) |
| Sep | 8604 | 45822 | [citations/sep/](citations/sep/index.md) |
| Sequist | 1 | 1 | [citations/sequist/](citations/sequist/index.md) |
| Seraille | 25 | 146 | [citations/seraille/](citations/seraille/index.md) |
| Sereno | 1 | 2 | [citations/sereno/](citations/sereno/index.md) |
| Serra | 72 | 326 | [citations/serra/](citations/serra/index.md) |
| Setal | 43 | 136 | [citations/setal/](citations/setal/index.md) |
| Sevenster | 1 | 2 | [citations/sevenster/](citations/sevenster/index.md) |
| Sha | 11772 | 143324 | [citations/sha/](citations/sha/index.md) |
| Shachar | 1 | 2 | [citations/shachar/](citations/shachar/index.md) |
| Shannon | 7 | 12 | [citations/shannon/](citations/shannon/index.md) |
| Shen | 125 | 695 | [citations/shen/](citations/shen/index.md) |
| Sheppard | 3 | 10 | [citations/sheppard/](citations/sheppard/index.md) |
| Sheth | 29 | 55 | [citations/sheth/](citations/sheth/index.md) |
| Shi | 9077 | 48603 | [citations/shi/](citations/shi/index.md) |
| Shull | 1 | 2 | [citations/shull/](citations/shull/index.md) |
| Sibiryakov | 1 | 2 | [citations/sibiryakov/](citations/sibiryakov/index.md) |
| Siegel | 1 | 2 | [citations/siegel/](citations/siegel/index.md) |
| Sierra Townsend | 6 | 10 | [citations/sierra-townsend/](citations/sierra-townsend/index.md) |
| Sigatm | 9 | 20102 | [citations/sigatm/](citations/sigatm/index.md) |
| Sigma | 9064 | 96670 | [citations/sigma/](citations/sigma/index.md) |
| Siguij | 9 | 19385 | [citations/siguij/](citations/siguij/index.md) |
| Silk | 21 | 140 | [citations/silk/](citations/silk/index.md) |
| Silva | 35 | 131 | [citations/silva/](citations/silva/index.md) |
| Simien | 5 | 9 | [citations/simien/](citations/simien/index.md) |
| Simon | 144 | 295 | [citations/simon/](citations/simon/index.md) |
| Sims | 88 | 962 | [citations/sims/](citations/sims/index.md) |
| Singer | 46 | 104 | [citations/singer/](citations/singer/index.md) |
| Singh | 104 | 206 | [citations/singh/](citations/singh/index.md) |
| Sirianni | 1 | 3 | [citations/sirianni/](citations/sirianni/index.md) |
| Sirko | 1 | 2 | [citations/sirko/](citations/sirko/index.md) |
| Site | 19986 | 105634 | [citations/site/](citations/site/index.md) |
| Sivan | 13 | 25 | [citations/sivan/](citations/sivan/index.md) |
| Skater | 3 | 8 | [citations/skater/](citations/skater/index.md) |
| Skill | 2442 | 64954 | [citations/skill/](citations/skill/index.md) |
| Skordis | 174 | 347 | [citations/skordis/](citations/skordis/index.md) |
| Skowron | 1 | 1 | [citations/skowron/](citations/skowron/index.md) |
| Skrutskie | 2 | 6 | [citations/skrutskie/](citations/skrutskie/index.md) |
| Slac | 701 | 7846 | [citations/slac/](citations/slac/index.md) |
| Slatyer | 7 | 14 | [citations/slatyer/](citations/slatyer/index.md) |
| Slepian | 1 | 2 | [citations/slepian/](citations/slepian/index.md) |
| Slone | 1 | 2 | [citations/slone/](citations/slone/index.md) |
| Sluis | 3 | 6 | [citations/sluis/](citations/sluis/index.md) |
| Smarra | 3 | 3 | [citations/smarra/](citations/smarra/index.md) |
| Sme | 4062 | 24469 | [citations/sme/](citations/sme/index.md) |
| Smirnov | 26 | 49 | [citations/smirnov/](citations/smirnov/index.md) |
| Smith | 8 | 17 | [citations/smith/](citations/smith/index.md) |
| Smolin | 146 | 580 | [citations/smolin/](citations/smolin/index.md) |
| Snaith | 5 | 6 | [citations/snaith/](citations/snaith/index.md) |
| Soda | 39 | 68 | [citations/soda/](citations/soda/index.md) |
| Soergel | 1 | 2 | [citations/soergel/](citations/soergel/index.md) |
| Sohn | 52 | 231 | [citations/sohn/](citations/sohn/index.md) |
| Sommerfeld | 16 | 34 | [citations/sommerfeld/](citations/sommerfeld/index.md) |
| Son | 1 | 1 | [citations/son/](citations/son/index.md) |
| Sorbo | 47 | 90 | [citations/sorbo/](citations/sorbo/index.md) |
| Soria | 2 | 4 | [citations/soria/](citations/soria/index.md) |
| Soucek | 4 | 8 | [citations/soucek/](citations/soucek/index.md) |
| Soul | 290 | 1812 | [citations/soul/](citations/soul/index.md) |
| Soundararajan | 6 | 13 | [citations/soundararajan/](citations/soundararajan/index.md) |
| Soussa | 1 | 2 | [citations/soussa/](citations/soussa/index.md) |
| Sparke | 5 | 5 | [citations/sparke/](citations/sparke/index.md) |
| Spatial | 50443 | 80974 | [citations/spatial/](citations/spatial/index.md) |
| Spencer | 23 | 45 | [citations/spencer/](citations/spencer/index.md) |
| Spergel | 14 | 36 | [citations/spergel/](citations/spergel/index.md) |
| Sphere | 3669 | 17175 | [citations/sphere/](citations/sphere/index.md) |
| Spin | 2003 | 13338 | [citations/spin/](citations/spin/index.md) |
| Spite | 478 | 831 | [citations/spite/](citations/spite/index.md) |
| Springel | 1 | 2 | [citations/springel/](citations/springel/index.md) |
| Springer | 14 | 26 | [citations/springer/](citations/springer/index.md) |
| Sse | 95302 | 503657 | [citations/sse/](citations/sse/index.md) |
| Stacy | 23 | 34 | [citations/stacy/](citations/stacy/index.md) |
| Stadinski | 1 | 1 | [citations/stadinski/](citations/stadinski/index.md) |
| Standard | 84298 | 225206 | [citations/standard/](citations/standard/index.md) |
| Standing | 1778 | 3762 | [citations/standing/](citations/standing/index.md) |
| Stanley | 15 | 20 | [citations/stanley/](citations/stanley/index.md) |
| Starkman | 18 | 20 | [citations/starkman/](citations/starkman/index.md) |
| Steidel | 1 | 2 | [citations/steidel/](citations/steidel/index.md) |
| Steinhardt | 20 | 86 | [citations/steinhardt/](citations/steinhardt/index.md) |
| Steinmetz | 1 | 2 | [citations/steinmetz/](citations/steinmetz/index.md) |
| Stern | 153 | 613 | [citations/stern/](citations/stern/index.md) |
| Steven | 101 | 262 | [citations/steven/](citations/steven/index.md) |
| Stewart | 28 | 76 | [citations/stewart/](citations/stewart/index.md) |
| Stieltjes | 45 | 126 | [citations/stieltjes/](citations/stieltjes/index.md) |
| Stierwalt | 2 | 3 | [citations/stierwalt/](citations/stierwalt/index.md) |
| Stil | 6967 | 24311 | [citations/stil/](citations/stil/index.md) |
| Stiskalek | 1 | 2 | [citations/stiskalek/](citations/stiskalek/index.md) |
| Stocke | 1 | 2 | [citations/stocke/](citations/stocke/index.md) |
| Stoecker | 1 | 2 | [citations/stoecker/](citations/stoecker/index.md) |
| Stoica | 1 | 2 | [citations/stoica/](citations/stoica/index.md) |
| Stojkovic | 16 | 26 | [citations/stojkovic/](citations/stojkovic/index.md) |
| Stolzenburg | 1 | 1 | [citations/stolzenburg/](citations/stolzenburg/index.md) |
| Stone | 612 | 1513 | [citations/stone/](citations/stone/index.md) |
| Story | 3258 | 17675 | [citations/story/](citations/story/index.md) |
| Stoughton | 2 | 3 | [citations/stoughton/](citations/stoughton/index.md) |
| Straatman | 5 | 6 | [citations/straatman/](citations/straatman/index.md) |
| Strategies | 352 | 1657 | [citations/strategies/](citations/strategies/index.md) |
| Strateva | 1 | 2 | [citations/strateva/](citations/strateva/index.md) |
| Strauss | 2 | 4 | [citations/strauss/](citations/strauss/index.md) |
| Strick | 9 | 15 | [citations/strick/](citations/strick/index.md) |
| Stringjoin | 4 | 16 | [citations/stringjoin/](citations/stringjoin/index.md) |
| Strominger | 1 | 2 | [citations/strominger/](citations/strominger/index.md) |
| Struble | 2 | 15 | [citations/struble/](citations/struble/index.md) |
| Strynadka | 3 | 4 | [citations/strynadka/](citations/strynadka/index.md) |
| Studies | 382 | 584 | [citations/studies/](citations/studies/index.md) |
| Study | 605 | 1243 | [citations/study/](citations/study/index.md) |
| Stull | 1 | 1 | [citations/stull/](citations/stull/index.md) |
| Sudarshan | 3 | 4 | [citations/sudarshan/](citations/sudarshan/index.md) |
| Sugahara | 8 | 14 | [citations/sugahara/](citations/sugahara/index.md) |
| Sugiyama | 1 | 2 | [citations/sugiyama/](citations/sugiyama/index.md) |
| Suite | 680 | 2009 | [citations/suite/](citations/suite/index.md) |
| Sully | 1 | 1 | [citations/sully/](citations/sully/index.md) |
| Summerfield | 1 | 2 | [citations/summerfield/](citations/summerfield/index.md) |
| Sun | 4067 | 27965 | [citations/sun/](citations/sun/index.md) |
| Superman | 7 | 44 | [citations/superman/](citations/superman/index.md) |
| Suslick | 3 | 4 | [citations/suslick/](citations/suslick/index.md) |
| Susskind | 160 | 572 | [citations/susskind/](citations/susskind/index.md) |
| Sutherland | 1 | 2 | [citations/sutherland/](citations/sutherland/index.md) |
| Suto | 1 | 2 | [citations/suto/](citations/suto/index.md) |
| Sutter | 2 | 2 | [citations/sutter/](citations/sutter/index.md) |
| Svartholm | 1 | 1 | [citations/svartholm/](citations/svartholm/index.md) |
| Swarup | 1 | 1 | [citations/swarup/](citations/swarup/index.md) |
| Swaters | 1 | 2 | [citations/swaters/](citations/swaters/index.md) |
| Sweet | 130 | 301 | [citations/sweet/](citations/sweet/index.md) |
| Syaifudin | 1 | 2 | [citations/syaifudin/](citations/syaifudin/index.md) |
| Symmetry | 7006 | 35970 | [citations/symmetry/](citations/symmetry/index.md) |
| Sys | 14888 | 106142 | [citations/sys/](citations/sys/index.md) |
| Szalay | 1 | 2 | [citations/szalay/](citations/szalay/index.md) |

</details>

<details><summary><b>T</b> · 74 names</summary>

| Name | Files | Occurrences | Citation page |
|---|---|---|---|
| Tacchella | 1 | 2 | [citations/tacchella/](citations/tacchella/index.md) |
| Tacconi | 1 | 2 | [citations/tacconi/](citations/tacconi/index.md) |
| Tagirov | 2 | 2 | [citations/tagirov/](citations/tagirov/index.md) |
| Taibi | 9 | 13 | [citations/taibi/](citations/taibi/index.md) |
| Takahashi | 2 | 3 | [citations/takahashi/](citations/takahashi/index.md) |
| Tamosiunas | 1 | 2 | [citations/tamosiunas/](citations/tamosiunas/index.md) |
| Tan | 44824 | 628866 | [citations/tan/](citations/tan/index.md) |
| Tang | 23 | 350 | [citations/tang/](citations/tang/index.md) |
| Target | 13884 | 96665 | [citations/target/](citations/target/index.md) |
| Taruya | 1 | 2 | [citations/taruya/](citations/taruya/index.md) |
| Tashiro | 1 | 2 | [citations/tashiro/](citations/tashiro/index.md) |
| Tassis | 5 | 6 | [citations/tassis/](citations/tassis/index.md) |
| Taubes | 7 | 18 | [citations/taubes/](citations/taubes/index.md) |
| Taylor | 11 | 27 | [citations/taylor/](citations/taylor/index.md) |
| Tegmark | 128 | 510 | [citations/tegmark/](citations/tegmark/index.md) |
| Teitelboim | 1 | 4 | [citations/teitelboim/](citations/teitelboim/index.md) |
| Tempel | 12 | 28 | [citations/tempel/](citations/tempel/index.md) |
| Ten | 67986 | 394781 | [citations/ten/](citations/ten/index.md) |
| Teodoro | 1 | 2 | [citations/teodoro/](citations/teodoro/index.md) |
| Ter | 111089 | 1376284 | [citations/ter/](citations/ter/index.md) |
| Testa | 1779 | 4261 | [citations/testa/](citations/testa/index.md) |
| Teukolsky | 1 | 2 | [citations/teukolsky/](citations/teukolsky/index.md) |
| Text | 10855 | 181611 | [citations/text/](citations/text/index.md) |
| Things | 1089 | 2659 | [citations/things/](citations/things/index.md) |
| Thirring | 1 | 2 | [citations/thirring/](citations/thirring/index.md) |
| Thomas | 3 | 7 | [citations/thomas/](citations/thomas/index.md) |
| Thompson | 271 | 514 | [citations/thompson/](citations/thompson/index.md) |
| Thonnard | 1 | 1 | [citations/thonnard/](citations/thonnard/index.md) |
| Thooft | 170 | 644 | [citations/thooft/](citations/thooft/index.md) |
| Thorn | 66 | 586 | [citations/thorn/](citations/thorn/index.md) |
| Thress | 2 | 3 | [citations/thress/](citations/thress/index.md) |
| Tian | 4 | 8 | [citations/tian/](citations/tian/index.md) |
| Tiec | 2 | 4 | [citations/tiec/](citations/tiec/index.md) |
| Tiesinga | 1 | 2 | [citations/tiesinga/](citations/tiesinga/index.md) |
| Tiley | 1 | 2 | [citations/tiley/](citations/tiley/index.md) |
| Timotheeee | 8 | 8 | [citations/timotheeee/](citations/timotheeee/index.md) |
| Ting | 21 | 453 | [citations/ting/](citations/ting/index.md) |
| Tipler | 10 | 13 | [citations/tipler/](citations/tipler/index.md) |
| Tiret | 12 | 15 | [citations/tiret/](citations/tiret/index.md) |
| Title | 8643 | 40588 | [citations/title/](citations/title/index.md) |
| Tno | 1024 | 11713 | [citations/tno/](citations/tno/index.md) |
| Toloba | 1 | 2 | [citations/toloba/](citations/toloba/index.md) |
| Tonin | 58 | 140 | [citations/tonin/](citations/tonin/index.md) |
| Tonks | 1 | 1 | [citations/tonks/](citations/tonks/index.md) |
| Tools | 4427 | 61363 | [citations/tools/](citations/tools/index.md) |
| Toomre | 8 | 9 | [citations/toomre/](citations/toomre/index.md) |
| Topological | 1041 | 4590 | [citations/topological/](citations/topological/index.md) |
| Topology | 1324 | 5161 | [citations/topology/](citations/topology/index.md) |
| Tornroth Horsefield | 1 | 1 | [citations/tornroth-horsefield/](citations/tornroth-horsefield/index.md) |
| Torre | 2 | 5 | [citations/torre/](citations/torre/index.md) |
| Tortora | 2 | 4 | [citations/tortora/](citations/tortora/index.md) |
| Touboul | 1 | 2 | [citations/touboul/](citations/touboul/index.md) |
| Touchdesigner | 74 | 476 | [citations/touchdesigner/](citations/touchdesigner/index.md) |
| Towner | 10 | 11 | [citations/towner/](citations/towner/index.md) |
| Tram | 357 | 1200 | [citations/tram/](citations/tram/index.md) |
| Transport | 1641 | 13407 | [citations/transport/](citations/transport/index.md) |
| Tremaine | 73 | 145 | [citations/tremaine/](citations/tremaine/index.md) |
| Treu | 24 | 100 | [citations/treu/](citations/treu/index.md) |
| Trial | 665 | 2260 | [citations/trial/](citations/trial/index.md) |
| Trincherini | 2 | 3 | [citations/trincherini/](citations/trincherini/index.md) |
| Tristram | 3 | 3 | [citations/tristram/](citations/tristram/index.md) |
| Trombetta | 31 | 124 | [citations/trombetta/](citations/trombetta/index.md) |
| Trujillo | 1 | 2 | [citations/trujillo/](citations/trujillo/index.md) |
| Tui | 1043 | 6904 | [citations/tui/](citations/tui/index.md) |
| Tully | 196 | 478 | [citations/tully/](citations/tully/index.md) |
| Tuma | 6 | 8 | [citations/tuma/](citations/tuma/index.md) |
| Tuning | 1470 | 7338 | [citations/tuning/](citations/tuning/index.md) |
| Turner | 2 | 3 | [citations/turner/](citations/turner/index.md) |
| Turok | 23 | 32 | [citations/turok/](citations/turok/index.md) |
| Turygin | 1 | 2 | [citations/turygin/](citations/turygin/index.md) |
| Turyshev | 11 | 16 | [citations/turyshev/](citations/turyshev/index.md) |
| Tversky | 2 | 2 | [citations/tversky/](citations/tversky/index.md) |
| Twomrs | 1 | 2 | [citations/twomrs/](citations/twomrs/index.md) |
| Tyr | 4600 | 1368077 | [citations/tyr/](citations/tyr/index.md) |

</details>

<details><summary><b>U</b> · 18 names</summary>

| Name | Files | Occurrences | Citation page |
|---|---|---|---|
| Ubler | 2 | 4 | [citations/ubler/](citations/ubler/index.md) |
| Udalski | 2 | 4 | [citations/udalski/](citations/udalski/index.md) |
| Udgs | 119 | 438 | [citations/udgs/](citations/udgs/index.md) |
| Uebler | 7 | 22 | [citations/uebler/](citations/uebler/index.md) |
| Uetal | 1 | 2 | [citations/uetal/](citations/uetal/index.md) |
| Ugc | 300 | 19495 | [citations/ugc/](citations/ugc/index.md) |
| Uglum | 1 | 1 | [citations/uglum/](citations/uglum/index.md) |
| Umetsu | 1 | 2 | [citations/umetsu/](citations/umetsu/index.md) |
| Uml | 87 | 391 | [citations/uml/](citations/uml/index.md) |
| Union | 570 | 1922 | [citations/union/](citations/union/index.md) |
| Units | 3985 | 10022 | [citations/units/](citations/units/index.md) |
| Universe | 1941 | 7523 | [citations/universe/](citations/universe/index.md) |
| Unno | 72 | 160 | [citations/unno/](citations/unno/index.md) |
| Upsilon | 729 | 6803 | [citations/upsilon/](citations/upsilon/index.md) |
| Uri | 10467 | 37761 | [citations/uri/](citations/uri/index.md) |
| Url | 5352 | 100914 | [citations/url/](citations/url/index.md) |
| Ursula | 19 | 46 | [citations/ursula/](citations/ursula/index.md) |
| Uvlf | 8 | 17 | [citations/uvlf/](citations/uvlf/index.md) |

</details>

<details><summary><b>V</b> · 45 names</summary>

| Name | Files | Occurrences | Citation page |
|---|---|---|---|
| Vafa | 2 | 4 | [citations/vafa/](citations/vafa/index.md) |
| Vainshtein | 88 | 222 | [citations/vainshtein/](citations/vainshtein/index.md) |
| Valageas | 1 | 1 | [citations/valageas/](citations/valageas/index.md) |
| Valenzuela | 18 | 34 | [citations/valenzuela/](citations/valenzuela/index.md) |
| Valluri | 2 | 2 | [citations/valluri/](citations/valluri/index.md) |
| Vanderburg | 2 | 4 | [citations/vanderburg/](citations/vanderburg/index.md) |
| Vandokkum | 32 | 63 | [citations/vandokkum/](citations/vandokkum/index.md) |
| Vaneymeren | 6 | 42 | [citations/vaneymeren/](citations/vaneymeren/index.md) |
| Varasteanu | 1 | 2 | [citations/varasteanu/](citations/varasteanu/index.md) |
| Vasiliev | 1 | 2 | [citations/vasiliev/](citations/vasiliev/index.md) |
| Vaswani | 6 | 8 | [citations/vaswani/](citations/vaswani/index.md) |
| Vasyunin | 1 | 10 | [citations/vasyunin/](citations/vasyunin/index.md) |
| Vavilova | 2 | 2 | [citations/vavilova/](citations/vavilova/index.md) |
| Vecitis | 1 | 2 | [citations/vecitis/](citations/vecitis/index.md) |
| Vectors | 766 | 2867 | [citations/vectors/](citations/vectors/index.md) |
| Velten | 1 | 2 | [citations/velten/](citations/velten/index.md) |
| Vendruscolo | 1 | 1 | [citations/vendruscolo/](citations/vendruscolo/index.md) |
| Veneziano | 6 | 8 | [citations/veneziano/](citations/veneziano/index.md) |
| Venn | 39 | 186 | [citations/venn/](citations/venn/index.md) |
| Verdaguer | 20 | 26 | [citations/verdaguer/](citations/verdaguer/index.md) |
| Verde | 312 | 921 | [citations/verde/](citations/verde/index.md) |
| Verheijen | 1 | 2 | [citations/verheijen/](citations/verheijen/index.md) |
| Verified | 77905 | 84375 | [citations/verified/](citations/verified/index.md) |
| Verlinde | 235 | 885 | [citations/verlinde/](citations/verlinde/index.md) |
| Vernizzi | 11 | 26 | [citations/vernizzi/](citations/vernizzi/index.md) |
| Vernon | 1 | 2 | [citations/vernon/](citations/vernon/index.md) |
| Verwayen | 1 | 2 | [citations/verwayen/](citations/verwayen/index.md) |
| Viel | 3 | 13 | [citations/viel/](citations/viel/index.md) |
| Vikhlinin | 1 | 2 | [citations/vikhlinin/](citations/vikhlinin/index.md) |
| Vikman | 26 | 77 | [citations/vikman/](citations/vikman/index.md) |
| Villain | 3 | 7 | [citations/villain/](citations/villain/index.md) |
| Villasenor | 1 | 2 | [citations/villasenor/](citations/villasenor/index.md) |
| Viola | 1916 | 5788 | [citations/viola/](citations/viola/index.md) |
| Viridian | 4 | 16 | [citations/viridian/](citations/viridian/index.md) |
| Vitells | 5 | 8 | [citations/vitells/](citations/vitells/index.md) |
| Vitral | 1 | 2 | [citations/vitral/](citations/vitral/index.md) |
| Vivas | 10 | 515 | [citations/vivas/](citations/vivas/index.md) |
| Vives | 5900 | 8793 | [citations/vives/](citations/vives/index.md) |
| Vivian | 21 | 27 | [citations/vivian/](citations/vivian/index.md) |
| Vogel | 17 | 29 | [citations/vogel/](citations/vogel/index.md) |
| Voges | 1 | 2 | [citations/voges/](citations/voges/index.md) |
| Voids | 903 | 1930 | [citations/voids/](citations/voids/index.md) |
| Volovich | 11 | 12 | [citations/volovich/](citations/volovich/index.md) |
| Voros | 2 | 4 | [citations/voros/](citations/voros/index.md) |
| Vrot | 84 | 17890 | [citations/vrot/](citations/vrot/index.md) |

</details>

<details><summary><b>W</b> · 74 names</summary>

| Name | Files | Occurrences | Citation page |
|---|---|---|---|
| Wadekar | 1 | 1 | [citations/wadekar/](citations/wadekar/index.md) |
| Wadsley | 1 | 2 | [citations/wadsley/](citations/wadsley/index.md) |
| Wagenveld | 1 | 2 | [citations/wagenveld/](citations/wagenveld/index.md) |
| Wagner | 60 | 126 | [citations/wagner/](citations/wagner/index.md) |
| Wake | 241 | 1223 | [citations/wake/](citations/wake/index.md) |
| Wald | 92 | 926 | [citations/wald/](citations/wald/index.md) |
| Wales | 6 | 9 | [citations/wales/](citations/wales/index.md) |
| Walker | 42 | 96 | [citations/walker/](citations/walker/index.md) |
| Walmsley | 1 | 6 | [citations/walmsley/](citations/walmsley/index.md) |
| Walsh | 28 | 108 | [citations/walsh/](citations/walsh/index.md) |
| Walter | 2 | 3 | [citations/walter/](citations/walter/index.md) |
| Wandelt | 2 | 2 | [citations/wandelt/](citations/wandelt/index.md) |
| Wands | 5 | 15 | [citations/wands/](citations/wands/index.md) |
| Wang | 3 | 10 | [citations/wang/](citations/wang/index.md) |
| Warmels | 2 | 5 | [citations/warmels/](citations/warmels/index.md) |
| Warps | 55 | 92 | [citations/warps/](citations/warps/index.md) |
| Watch | 2406 | 9193 | [citations/watch/](citations/watch/index.md) |
| Watkins | 1 | 2 | [citations/watkins/](citations/watkins/index.md) |
| Waves | 551 | 1375 | [citations/waves/](citations/waves/index.md) |
| Waxman | 1 | 2 | [citations/waxman/](citations/waxman/index.md) |
| Way | 11731 | 85125 | [citations/way/](citations/way/index.md) |
| Webb | 1 | 1 | [citations/webb/](citations/webb/index.md) |
| Wechsler | 2 | 4 | [citations/wechsler/](citations/wechsler/index.md) |
| Wegorzewska | 1 | 2 | [citations/wegorzewska/](citations/wegorzewska/index.md) |
| Weibel | 4 | 5 | [citations/weibel/](citations/weibel/index.md) |
| Weil | 2 | 8 | [citations/weil/](citations/weil/index.md) |
| Weinberg | 35 | 64 | [citations/weinberg/](citations/weinberg/index.md) |
| Weiner | 1 | 2 | [citations/weiner/](citations/weiner/index.md) |
| Weisberg | 1 | 2 | [citations/weisberg/](citations/weisberg/index.md) |
| Wel | 4383 | 30374 | [citations/wel/](citations/wel/index.md) |
| Werk | 3 | 16 | [citations/werk/](citations/werk/index.md) |
| Westmeier | 1 | 2 | [citations/westmeier/](citations/westmeier/index.md) |
| Wex | 57 | 306 | [citations/wex/](citations/wex/index.md) |
| Weyl | 10 | 23 | [citations/weyl/](citations/weyl/index.md) |
| Wheeler | 48 | 107 | [citations/wheeler/](citations/wheeler/index.md) |
| Whelan | 9 | 18 | [citations/whelan/](citations/whelan/index.md) |
| Whitbourn | 1 | 2 | [citations/whitbourn/](citations/whitbourn/index.md) |
| White | 1103 | 4085 | [citations/white/](citations/white/index.md) |
| Whitmore | 1 | 2 | [citations/whitmore/](citations/whitmore/index.md) |
| Wick | 394 | 783 | [citations/wick/](citations/wick/index.md) |
| Widiyantoro | 2 | 3 | [citations/widiyantoro/](citations/widiyantoro/index.md) |
| Widmark | 1 | 1 | [citations/widmark/](citations/widmark/index.md) |
| Widnall | 1 | 1 | [citations/widnall/](citations/widnall/index.md) |
| Widrow | 6 | 15 | [citations/widrow/](citations/widrow/index.md) |
| Wigner | 7 | 9 | [citations/wigner/](citations/wigner/index.md) |
| Wikiproject | 4 | 8 | [citations/wikiproject/](citations/wikiproject/index.md) |
| Wilde | 9 | 36 | [citations/wilde/](citations/wilde/index.md) |
| Wilkinson | 27 | 63 | [citations/wilkinson/](citations/wilkinson/index.md) |
| Wilma | 1 | 2 | [citations/wilma/](citations/wilma/index.md) |
| Wilson | 10 | 21 | [citations/wilson/](citations/wilson/index.md) |
| Winnink | 1 | 1 | [citations/winnink/](citations/winnink/index.md) |
| Wintner | 1 | 2 | [citations/wintner/](citations/wintner/index.md) |
| Wintrode | 1 | 1 | [citations/wintrode/](citations/wintrode/index.md) |
| Wisnioski | 8 | 11 | [citations/wisnioski/](citations/wisnioski/index.md) |
| Withdrawn | 552 | 1353 | [citations/withdrawn/](citations/withdrawn/index.md) |
| Witten | 198 | 751 | [citations/witten/](citations/witten/index.md) |
| Wohlfarth | 6 | 8 | [citations/wohlfarth/](citations/wohlfarth/index.md) |
| Woit | 6 | 9 | [citations/woit/](citations/woit/index.md) |
| Wojtak | 1 | 2 | [citations/wojtak/](citations/wojtak/index.md) |
| Wolf | 16 | 35 | [citations/wolf/](citations/wolf/index.md) |
| Wonder | 74 | 144 | [citations/wonder/](citations/wonder/index.md) |
| Wong | 2 | 3 | [citations/wong/](citations/wong/index.md) |
| Wood | 412 | 1972 | [citations/wood/](citations/wood/index.md) |
| Woolgar | 1 | 2 | [citations/woolgar/](citations/woolgar/index.md) |
| Work | 20256 | 123158 | [citations/work/](citations/work/index.md) |
| Workman | 1 | 2 | [citations/workman/](citations/workman/index.md) |
| Woronowicz | 16 | 37 | [citations/woronowicz/](citations/woronowicz/index.md) |
| Wrasidlo | 1 | 1 | [citations/wrasidlo/](citations/wrasidlo/index.md) |
| Wright | 3 | 8 | [citations/wright/](citations/wright/index.md) |
| Writing | 1314 | 3679 | [citations/writing/](citations/writing/index.md) |
| Wulandari | 2 | 3 | [citations/wulandari/](citations/wulandari/index.md) |
| Wuyts | 1 | 2 | [citations/wuyts/](citations/wuyts/index.md) |
| Wyler | 1 | 2 | [citations/wyler/](citations/wyler/index.md) |
| Wynne | 2 | 3 | [citations/wynne/](citations/wynne/index.md) |

</details>

<details><summary><b>X</b> · 2 names</summary>

| Name | Files | Occurrences | Citation page |
|---|---|---|---|
| X Ray | 4321 | 14099 | [citations/x-ray/](citations/x-ray/index.md) |
| Xie | 3124 | 16741 | [citations/xie/](citations/xie/index.md) |

</details>

<details><summary><b>Y</b> · 19 names</summary>

| Name | Files | Occurrences | Citation page |
|---|---|---|---|
| Yacine | 54 | 54 | [citations/yacine/](citations/yacine/index.md) |
| Yagi | 64 | 1585 | [citations/yagi/](citations/yagi/index.md) |
| Yahil | 12 | 26 | [citations/yahil/](citations/yahil/index.md) |
| Yakaboylu | 1 | 2 | [citations/yakaboylu/](citations/yakaboylu/index.md) |
| Yamaguchi | 28 | 54 | [citations/yamaguchi/](citations/yamaguchi/index.md) |
| Yan | 1438 | 13431 | [citations/yan/](citations/yan/index.md) |
| Yang | 7 | 21 | [citations/yang/](citations/yang/index.md) |
| Yao | 96 | 322 | [citations/yao/](citations/yao/index.md) |
| Yasin | 12 | 59 | [citations/yasin/](citations/yasin/index.md) |
| Year | 2038 | 10110 | [citations/year/](citations/year/index.md) |
| Yeomans | 1 | 1 | [citations/yeomans/](citations/yeomans/index.md) |
| Yin | 10112 | 39650 | [citations/yin/](citations/yin/index.md) |
| Yokoyama | 28 | 43 | [citations/yokoyama/](citations/yokoyama/index.md) |
| Yoo | 32 | 193 | [citations/yoo/](citations/yoo/index.md) |
| York | 345 | 6737 | [citations/york/](citations/york/index.md) |
| Yoshii | 1 | 2 | [citations/yoshii/](citations/yoshii/index.md) |
| Yozin | 2 | 4 | [citations/yozin/](citations/yozin/index.md) |
| Yuanbao | 114 | 1660 | [citations/yuanbao/](citations/yuanbao/index.md) |
| Yukawa | 552 | 2042 | [citations/yukawa/](citations/yukawa/index.md) |

</details>

<details><summary><b>Z</b> · 36 names</summary>

| Name | Files | Occurrences | Citation page |
|---|---|---|---|
| Z Squared | 246 | 1059 | [citations/z-squared/](citations/z-squared/index.md) |
| Zabludoff | 3 | 7 | [citations/zabludoff/](citations/zabludoff/index.md) |
| Zacharegkas | 3 | 5 | [citations/zacharegkas/](citations/zacharegkas/index.md) |
| Zahid | 6 | 6 | [citations/zahid/](citations/zahid/index.md) |
| Zakamska | 1 | 2 | [citations/zakamska/](citations/zakamska/index.md) |
| Zanelli | 3 | 5 | [citations/zanelli/](citations/zanelli/index.md) |
| Zaninetti | 2 | 4 | [citations/zaninetti/](citations/zaninetti/index.md) |
| Zaritsky | 9 | 19 | [citations/zaritsky/](citations/zaritsky/index.md) |
| Zdesi | 1 | 2 | [citations/zdesi/](citations/zdesi/index.md) |
| Zehavi | 1 | 2 | [citations/zehavi/](citations/zehavi/index.md) |
| Zeilinger | 7 | 49 | [citations/zeilinger/](citations/zeilinger/index.md) |
| Zekser | 2 | 2 | [citations/zekser/](citations/zekser/index.md) |
| Zel'Dovich | 34 | 63 | [citations/zel'dovich/](citations/zel'dovich/index.md) |
| Zeller | 2 | 2 | [citations/zeller/](citations/zeller/index.md) |
| Zen | 6544 | 20918 | [citations/zen/](citations/zen/index.md) |
| Zfte | 1 | 2 | [citations/zfte/](citations/zfte/index.md) |
| Zhang | 3 | 5 | [citations/zhang/](citations/zhang/index.md) |
| Zhao | 85 | 170 | [citations/zhao/](citations/zhao/index.md) |
| Zheng | 6 | 8 | [citations/zheng/](citations/zheng/index.md) |
| Zhonest | 2 | 7 | [citations/zhonest/](citations/zhonest/index.md) |
| Zhong | 2 | 5 | [citations/zhong/](citations/zhong/index.md) |
| Zhou | 2 | 8 | [citations/zhou/](citations/zhou/index.md) |
| Zibetti | 2 | 5 | [citations/zibetti/](citations/zibetti/index.md) |
| Zimmerman | 3547 | 4928336 | [citations/zimmerman/](citations/zimmerman/index.md) |
| Ziour | 2 | 2 | [citations/ziour/](citations/ziour/index.md) |
| Zitrin | 1 | 2 | [citations/zitrin/](citations/zitrin/index.md) |
| Zlosnik | 129 | 257 | [citations/zlosnik/](citations/zlosnik/index.md) |
| Zmnras | 1 | 2 | [citations/zmnras/](citations/zmnras/index.md) |
| Zonoozi | 1 | 2 | [citations/zonoozi/](citations/zonoozi/index.md) |
| Zou | 49 | 178 | [citations/zou/](citations/zou/index.md) |
| Zsigma | 2 | 5 | [citations/zsigma/](citations/zsigma/index.md) |
| Zuhone | 1 | 1 | [citations/zuhone/](citations/zuhone/index.md) |
| Zumalacarregui | 17 | 31 | [citations/zumalacarregui/](citations/zumalacarregui/index.md) |
| Zwaan | 1 | 2 | [citations/zwaan/](citations/zwaan/index.md) |
| Zwicky | 45 | 237 | [citations/zwicky/](citations/zwicky/index.md) |
| Zyla | 14 | 29 | [citations/zyla/](citations/zyla/index.md) |

</details>

<details><summary><b>\</b> · 1 names</summary>

| Name | Files | Occurrences | Citation page |
|---|---|---|---|

</details>

---
*Complete index regenerates from [`CITATIONS.md`](CITATIONS.md) · never delete.*
