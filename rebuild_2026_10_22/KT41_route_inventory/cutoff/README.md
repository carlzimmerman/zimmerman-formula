# Cutoff, granularity and curvature-regularization route inventory

Read-only scientific audit, 2026-11-04. No physics experiment, model change,
parameter scan or rerun was performed. Only this audit directory was written.
This is a bounded repository-prior search, **not a proof of global novelty**.
The source evidence below is recorded work, not newly independently verified
physics. `SOURCE_HASHES.json` pins the inspected load-bearing files.

## Result

“Add a cutoff,” “resolve stars,” “use a density screen,” “add a healthy k^4
term,” and “smooth the curvature” are all present in earlier repository work.
They are not new route descriptions. In particular H4 already quantified a
microscopic/macroscopic cutoff conflict for the older v3 action; V1 tested
finite stellar size and density screening; L59 explicitly calculated stellar
granularity in a quadratic-curvature invariant; XR15 varied a smoothed gate
and retained its adjoint/background terms. Their different actions prevent
transferring their empirical verdicts automatically to KT39.

The specific changed functional

\[
 E_a[\psi]=\int |g|^2R\!\left(x+
       [\ell^2(T_aH):(T_aH)/a_0^2]^p\right)d^3x,
 \quad g=\nabla\psi,\quad H=\nabla\nabla\psi,
\]

with **unfiltered g**, a fixed translation-invariant filter acting **only on
the tensor H before its norm**, and the **full outer adjoint T_a*** in the
physical equation, was **not found in the searched scope**. This does not
make generalized nonlocal QUMOND, curvature smoothing, or adjoint variation
new architectures. The potentially new work is a specific implementation
and a simultaneous scale-compatibility calculation for KT39/KT40's fixed
baryons and cuts. It deserves a cheap analytic gate before any MW grid scan.

## Search coverage and its limits

`all_text_files.txt` enumerates 92,740 current-worktree files totalling
1,033,335,832 bytes with extensions `.md .tex .py .txt .rst`. Enumeration and
content searches used `rg --hidden --no-ignore`; explicit exclusions are
`.git`, node_modules, virtual environments, __pycache__, site-packages, and
the entire new KT41 directory. No scientific directory or file-size ceiling
was excluded. Existing archive/mirror/snapshot text files were therefore
searched when they have those extensions, including ignored and hidden files.
Git history, deleted files, PDFs without a searched text counterpart,
notebooks, binary/compressed archives, extensionless files, and JSON-only
formula/results content were **not exhaustively searched**. Selected JSON
outputs were inspected to corroborate relevant prior records.

The initial cutoff vocabulary returned 3,468 files; 2,219 also contain one of
QUMOND, AQUAL, Cassini, Milky Way, baryon, modified gravity, MOND or Poisson.
This latter selection is a relevance heuristic, not a completeness theorem.
To remove that prefilter's blind spot, three additional direct searches ran
over the entire original text scope: curvature/filter proximity (747 lines),
curvature-only/unfiltered-gradient wording (216 lines), and granularity versus
curvature proximity (3 lines). Their exact argv, outputs and return codes are
in `ALL_TEXT_TARGETED_SEARCHES.json` and the correspondingly named text files.
The resulting nearest-family passages and selected actual derivations were
read; not all 92,740 files were manually audited.

The preliminary piped `rg` call accidentally omitted an explicit search path
and read empty stdin. Its zero hits are invalid evidence and are preserved as
`INITIAL_QUERY_DEFECT.json`. All reported content counts come from the
corrected explicit `.` searches. A secondary `uv_stabilizer` heuristic also
matches ordinary labels such as K4; its count must not be interpreted as a
count of physical stabilizers. It was used only to locate files.

## Closest prior routes and exact distinctions

| Prior record | Load-bearing formula or result | Consequence for this task |
|---|---|---|
| `rebuild_2026_10_22/H4_v3_saddle_stability/README.md` and results JSON | For the older khronon/dust system, at mu_K=0, omega^2=4 pi G rho_tau(M_theta-1+Lstar^2 k^2/2). Negative rho_tau gives Gamma~Lstar k sqrt(2 pi G abs(rho_tau)). One-e-fold cutoff wavelengths are 4–330 pc across the sampled systems, while the same stiffness supplies AU-scale Solar screening. | A physical-cutoff conflict was already calculated. It is not the KT39 baryonic-response theorem. H4 retains its failed original C2 convergence check; the separately declared extra-fine check passes. |
| `rebuild_2026_10_22/H5_v3s_lobe_growth/README.md` | Moving-source susceptibility is delta rho_tau=delta rho_m/[M(khat)-1+Theta Lstar^2 k^2/2-(k.V)^2/(4 pi G rhobar)]. Positive conserved charge stays positive along the pre-caustic flow. | H4's static branch cannot be transplanted into all moving systems. This also does not repair the instantaneous KT39 static force. |
| `rebuild_2026_10_22/V1_density_screen/README.md` and results JSON | Symmetron multiplier s=psi^2 gives mu_s=1-s/(1+x). Exterior maximum-principle bound: 1-s(r)/s_a <= 2R/r. Star thin shells cap scalar charge by 4 pi M^2 R. At least two independent screening parameters fail to decouple; the reported baryon budget condition misses by factors2.6/3.4. | A finite stellar radius, density gate, and stars-seen versus stars-thin-shell alternatives are prior work. V1's scoped NO-GO is not a theorem excluding every density coupling. |
| `fable_independent_2026/L59_SECOND_ORDER.md`, sections3–4 | H:H = (1/2) Delta(g^2)-g.grad(Delta Phi). Hence Delta^-1(H:H)=(1/2)g^2-4 pi G Delta^-1(g.grad rho). Compact interiors add 4 pi G^2 integral(rho^2)/d. Gaussian smoothing gives ell_crit^3=G m abs(Phi_pop)/(sqrt(pi) g^2). Reported ell_crit:1.20pc solar neighborhood,0.53pc Draco,38.5kpc cluster granules. | Granular tidal invariants and a required coarse-graining length were explicitly studied. The operator is an inverse Laplacian of a quadratic invariant, not E(g,T_a H). Its relativistic/lensing conclusions are not independently authenticated here. |
| `FRESH_AND_CRISPY_ASTRA_IDEAS.md`, F07–F08 | Existing proposals ask for the particle-to-Vlasov limit and physical stellar force/tidal covariance through inner nonlinear response plus outer heat filter. | Even an unexecuted proposal counts as already in the repo. Do not advertise generic stellar-noise/homogenization work as a newly invented option. |
| `qwen_claude_field_theory/closure_2026/filtered_tidal_relation_2026/REPORT.md` | In external-dominated linear response, Phi_ph_hat=-4 pi GM abs(sigma)^2[A+B(khat.e)^2]/k^2. Central H_ij=(4 pi GM I/15)[(5A+B)delta_ij+2B e_i e_j]. Gaussian/Helmholtz and finite spherical source controls share the same angular ratio. | Adjoint source/gradient filtering, finite source size, and central tidal checks are already present. This filter acts on the gradient entering the nonlinear flux, not only H in KT39. |
| `real_research/cross_thread_review_2026_09_26/XR15_README.md` | A Helmholtz-smoothed gate chi=G_ell U has second-variation terms with two filters, one filter, and an unsuppressed background term. Omitting background/cross terms misses direct energy differences. No single ell passes the tested global layer gates. | Smoothing an action variable and returning its adjoint is old. Multiplying a local instability coefficient by a filter while dropping other variation terms is not a valid repair. |
| `campaign_fresh_gravity/CFG49_gate_scalar/README.md` | Independent chi: L=-(mu/2)(partial chi)^2-(m2/2)(chi-t[baryons])^2+B W(chi). It has healthy principal kinetics on plateaus but a low-k instability and tracking/force costs. Appended corrections retain no joint gate pass. | A dynamical density/curvature gate with its own stiffness is prior work. Changing its name is not a new response law. |
| `rebuild_2026_10_22/UX1_action_class/README.md` | Positive-spectral Lorentz-invariant D has d(k^2D)/d(k^2)=sum w mu^2/(k^2+mu^2)^2>=0. The simple 1/(k^2+epsilon k^4) propagator has a negative-residue pole. | A covariant higher-derivative denominator cannot be assumed healthy just because its static smoothing looks favorable. The theorem has stated linear/spectral assumptions; preferred-foliation or nonlinear completions are not all excluded. |
| `real_research/closure_doors_2026_09_26/environment_gate/REPORT.md` | A regulated smooth gate f(R,K) and concave C(R) repair the frozen isotropic scalar k^4 sign in a specified coefficient window. The resulting all-frequency cone condition fails; finite-band causal completion remains an obligation. | Curvature EFT repair plus finite validity band is already developed, with an explicit restriction. It is neither a KT39 completion nor a generic no-go. |
| `opus_48_extended_research/reviews/gc_consequences/EFT_VALIDITY_WINDOW_VERDICT_2026-06-19.md` | Existing ghost-condensate discussion uses omega^2=alpha^2 k^4/M^2-alpha^2 M^2 k^2/(2 M_Pl^2). | A k^4 stabilizer/strong-coupling-window proposal is old. The report's external claims were not reverified here. |
| `deepseek_push/DS_FINAL_2026_10_21/A57_uv_completion/report.md` | Finite-state medium has xi=sqrt(gamma/K)=Lstar/sqrt2. Shifting microscopic H by a constant leaves Gibbs weights unchanged, so the absolute vacuum normalization remains free. A microscopic cutoff changes the closure integral negligibly in the inspected construction. | A microscopic completion that derives kappa and stiffness has already been attempted; it cannot simply be relabelled. This is not a theorem against every microscopic theory. |
| `rebuild_2026_10_22/UV1_uv_power_truncation/README.md` | Same-seed cosmological simulations truncate the initial P(k); reported resolved profiles change little. | Initial-data power truncation is mathematically different from changing the response operator. Same keyword, not a test of KT39 ultraviolet completion. |
| `rebuild_2026_10_22/KT26_local_filter_rule/README.md`, KT28, KT35 structural reconnaissance | Local field/tidal estimates set a width, but earlier empirical equations omit parts of a density-dependent filter variation. KT35 lists local geometric generalized QUMOND and variational filter-state routes already. | Do not reopen the old tidal width prescription or claim any arbitrary local Hessian action is a new architecture. |

## Exact remaining sub-obligations worth doing

1. **Curvature-only filter compatibility.** First derive the full variation of
   E(g,T_aH), including T_a*. At frozen constant coefficients and a real even
   isotropic multiplier sigma_a, the quadratic response is expected to be
   K(n)+(1/2)E_HH[nn,nn] k^2 sigma_a(k)^2; mixed odd-derivative terms cancel
   only in that frozen setting. Gaussian filtering bounds k^2 sigma_a^2 by
   1/(e a^2), removing the specific unbounded symbol. This is a prediction to
   derive and check, not a completed stability proof on variable backgrounds.

   The same operator gives, for a point mass and standard Gaussian width a,

   \[
   (T_aH)(0)=\frac{\sqrt2}{3\sqrt\pi}\frac{GM}{a^3}I,
   \qquad s(0)=\frac{2\ell^2(GM)^2}{3\pi a_0^2a^6}.
   \]

   Consequently if r_M=sqrt(GM/a0)<<a, order-unity curvature screening near
   the source requires a no larger than order
   [sqrt(2/(3pi)) ell r_M^2]^(1/3), a parsec-scale quantity for the Sun and
   ell=3kpc. This does **not** alone prove a Cassini exclusion: the uniform
   external field, full variation, extended source and physical quadrupole
   still need evaluation. Cheapest discriminator: this scaling plus one
   exact reciprocal small-source fixture, then the actual Solar quadrupole;
   only a survivor merits a complete MW/dwarf scan.

2. **A quantified static-repair budget, rather than a renamed cutoff.** KT40
   has an outward MW force at resolved 100–500pc heights and negative Draco
   virial. A completion preserving those static observables within errors
   smaller than their sign margins cannot repair them, independently of its
   high-k stability. Derive an explicit operator/source norm bound for a
   proposed filter's correction; comparing a to grid spacing is insufficient.
   No prior quantitative bound on the specific KT40 E(g,T_aH) correction was
   found in the searched scope. H4 is the nearest old scale-conflict argument.
   Cheapest calculation: one fixed source and the already pinned force/virial
   margin, before a parameter survey. A microscopic correction may survive as
   an EFT completion while still failing the observational repair.

3. **Close the local-regulator loophole by checking theorem hypotheses.** If
   a proposed finite-density floor or finite-source regulator still leaves
   a C^2 local E(g,H), a finite high-curvature endpoint, and an above-endpoint
   finite-curvature value, KT40's obstruction already applies on its admitted
   positive-density jets. It is unnecessary to scan every smooth replacement.
   The only new work would be a stated regulator failing one of those exact
   hypotheses and then its physical meaning/empirical check. No universal
   claim is made about discrete particles, kinetic matter, or spatially
   nonlocal constitutive laws.

These are new **sub-obligations relative to identified prior calculations**,
not first-discovery claims. Generic granularity, source-size, density-screen,
Lorentz-invariant k^4, and dynamic-gate routes already have exact antecedents.
The most useful closure may be ruling out a concrete repair cheaply; it need
not consist of another broad scan with retuned baryons.

## Recent and live-work boundary

KT40's `dynamics/run_003/manifest.json` reports successful completion and
unchanged input hashes; `results.json` reports `all_checks_pass: true` for its
symbolic/finite checks. This audit read those files, not an independent rerun.
Other dated work visible in the search includes `finish_2026_11_04/`,
`cw_lanes_2026_11_04/`, `claude_goal_2026_11_03/` and
`astra_goal_2026_11_03/`. Their presence is not evidence that a process is
currently running, nor was this audit allowed to start or interfere with one.
The worktree can change during this search; content hashes, not current HEAD
alone, identify the inspected evidence.
