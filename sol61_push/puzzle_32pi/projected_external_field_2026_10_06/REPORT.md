# Projected action versus Claude p57: external-field operator discrimination

The actual projected-acceleration NR equations do not inherit p57's QUMOND external-field solution even when their spherical force law is matched exactly. A constant-external-field linear response gives a precise operator distinction and an additional angular prediction. This is a far/external-dominated response, **not** the inner Solar-System quadrupole or a Cassini exclusion of the projected model.

## 1. Bounded audit of current Claude sources

SOURCE_AUDIT.json records the actual inspected HEAD, file hashes versus committed bytes, last file revisions and scoped status. The latest relevant tracked source remains p57 commit `6988a2ecbab63393c26a160f81ee15a4391d6a0a`; campaign work remains CFG355 `be5eee875ba98ad4246ee3e854094fd5050cfd5b`. The bounded tracked log after the verified p57 checkpoint contains no changes under sonnet55_push or campaign_fresh_gravity. The only tracked dirty entries in these scopes are three old CFG4 output files. Numerous untracked legacy simulation artifacts are counted, not executed or treated as new scientific claims. No new tracked p58/CFG356 source was found in this inspected snapshot; this is not a claim about all Claude activity.

The inspected p57 script calls qumond_efe_multipole.py, which actually solves a Poisson equation for the divergence of ν(|g_N|)g_N, projects Legendre multipoles and subtracts the uniform acceleration at the Sun. Its withdrawn algebraic version is clearly separated. The reported Q2 and secular occupancy are outputs of that operator. We did not rerun its astronomical fetch or integrations or infer correctness from its 4/4 label.

The scoped CFG355 source uses a tidal-eigenvalue switch with a cold-rank veto; its declared width and host-shell failure are not a projected-action completion or a selected interpolation scale. No such switch is inserted here. p54's normalization claims likewise are not used as full covariant exchange-symmetry proof. All audited source bytes match their committed HEAD bytes, separately from the dirty legacy outputs.

## 2. Actual varied NR operator and admitted boundary

For the projected action's stationary pressureless branch, let φ*=φ−hatφ, φ+=φ+hatφ, x=|∇φ*|/a0, m=M_eff,I(x²), μ=1−2m. With hatρ=0, its actual equations are

div[μ(x)∇φ*]=Ω_(n−1)G_Nρ,
Δφ+=Ω_(n−1)G_Nρ,
φ=(φ++φ*)/2.

This uses the same minimally coupled physical metric potential φ as the parent NR derivation. It is a nonlinear Poisson **star** field plus a Newtonian sum field, not QUMOND. The spherical/aligned map is y=μx and g/a0=(1+μ)x/2, giving ν(y)=(1+μ)/(2μ). A local source kernel can be inherited parametrically from an admitted spherical ν only where dx/dy>0; no global inversion is inferred merely from a measured interval.

Specify a constant nonzero star-gradient boundary a0 x_e e_z, and a perturbation small relative to it in the linearized region. Define μ_e>0 and L_e=x_e μ'_e/μ_e, with 1+L_e>0. Differentiating μ(|v|)v gives the exact linear operator

μ_e[Δ_perp+(1+L_e)∂z²]ψ*=ΩG_Nρ,
Δψ_N=ΩG_Nρ,
ψ=(ψ_N+ψ*)/2.

Its principal eigenvalues are μ_e transversely and μ_e(1+L_e) longitudinally. These conditions are the local ellipticity hypotheses, not a full scalar/covariant health theorem. The star boundary and Newtonian sum boundary are separate in a generic galaxy. The comparison below explicitly chooses their axes aligned and the Newtonian boundary magnitude y_e=μ_e x_e, so their physical external acceleration equals the spherical prescription. That is a declared matching condition, not an exact Milky-Way disk inference.

## 3. General-d Green response and exact Fourier discriminator

Write a=1+L_e>0 and R²=|x_perp|²+z²/a. For n≥3, coordinate stretching z'=z/√a maps the operator to μ_eΔ', with δ^(n)(x)=δ^(n)(x')/√a. Consequently the linear point-source Green potential is

ψ*=−G_N M/[(n−2)μ_e√a] R^(2−n),
ψ_N=−G_N M/[(n−2)r^(n−2)].

The factor 1/(n−2) follows from Δr^(2−n)=−(n−2)Ωδ. This is an exact linear Green function. For an admitted nonlinear compact source it supplies the leading far monopole under the additional decaying-perturbation/asymptotic-expansion hypotheses: the integrated full star flux fixes M, while higher nonlinear flux terms vanish on large spheres. It is not an existence theorem for that globally sourced solution. A literal point source violates external dominance near its center.

For arbitrary finite Fourier wave number let u=(k·e_z)²/k². The physical Fourier susceptibility relative to the Newton potential is

P_proj(u)=1/2[1+1/(μ_e(1+L_e u))].

A QUMOND theory matched to the same spherical ν instead has

P_Q(u)=ν_e(1+K_e u),
K_e=dlnν/dlny=−L_e/[(1+μ_e)(1+L_e)].

Therefore exactly

P_proj−P_Q=L_e² u(u−1)/[2μ_e(1+L_e)(1+L_e u)].

For 0<u<1, this is strictly negative whenever L_e≠0 under the ellipticity hypotheses, and vanishes on the two Fourier axes. Equality of spherical laws is thus insufficient to transfer any generic external-field solution. This is a specific instance of the known nonlinear-Poisson/QUMOND distinction, now applied to the actual half-Newtonian-plus-star projected operator; no literature novelty is asserted.

A fully Newtonian linear external response at all angles requires μ_e=1 and L_e=0, equivalently m_e=0 and x_e m'_e=0. Merely matching one direction or steepening a distant high-force tail is insufficient for this local criterion. This criterion is not a lower bound on the inner solar Q2 and does not show that every unscreened model is excluded.

## 4. A distinct observable angular shape in n=3

With cθ=z/r the projected potential coefficient is

P_proj(θ)=1/2[1+1/(μ_e√(1+L_e)) (1−L_e cθ²/(1+L_e))^(−1/2)].

The corresponding QUMOND coefficient is ν_e[1+K_e(1−cθ²)/2]. The polar projected coefficient equals ν_e, but the equatorial difference is exactly

P_proj(eq)−P_Q(eq)=−(√(1+L_e)−1)²/[4μ_e(1+L_e)].

The projected coefficient has a Legendre l=4 term starting at 3L_e²/(70μ_e)+O(L_e³), whereas the linear-QUMOND coefficient has no l=4 term. This is an **angular 1/r far potential** coefficient, not the inner regular r^4 multipole from a Solar-System matching problem. A far-field angular or suitably modeled wide-binary response is the next discriminating forecast, conditional on the actual background and source model.

For a bounded comparison we use the p57 inputs verbatim: a0=9.3603e−11 m/s², aligned observed external acceleration 2.146e−10 m/s², ν=1+[sqrt(1+1/y)−1]/[1+(y/T)²], and T=128.915, with no target fitting or vacuum integral insertion. At this declared boundary:

| coefficient | projected | matched QUMOND |
|---|---:|---:|
| polar | 1.24153178 | 1.24153178 |
| equatorial | 1.12299036 | 1.13246538 |
| far angular l4 | 0.00674715 | 0 |

Here y_e=1.84663944, μ_e=0.67427993 and L_e=0.41676197; the local inverse and ellipticity conditions hold. Removing the cutoff gives a similar but separately calculated comparison (full precision in results.json). The numerical proximity is not a proof that the two operators have similar inner Q2 or orbit histories.

## 5. What remains of the solar veto

The isolated spherical monopole law can be retained by construction, so p56's radial-force mechanism remains a conditional model concern on that branch. But its simplified orbit inference is not transferred as a full projected solar-system calculation. p57's QUMOND near-Sun quadrupole, multipoles and secular population results require a new nonlinear-Poisson-star field solve before they can be evaluated for this action. Most inner solar/ETNO radii are internally dominated; the external-dominated Green formula above cannot provide their local tidal coefficient. For example at r=rM/10, the isolated spherical y=100 gives a star perturbation far larger than the declared x_e, violating the linearization condition.

The measured physical quadrupole remains an observational benchmark if the model predicts the same fitted potential term Φ_Q=−Q2 r²(cθ²−1/3)/2. The historical p57 citation used (3±3)e−27 s−2. A bounded primary check of Park et al. arXiv:2602.17884v2 instead finds the updated fitted Q2=(1.6±1.8)e−27 s−2 (1σ), estimated with ephemeris parameters. Their QUMOND/AQUAL kernel-to-Q2 relations are theory-dependent and cannot be borrowed for this two-potential operator. The data constraint and the model prediction must be kept separate. [Exact current primary](https://arxiv.org/pdf/2602.17884v2), eq/result in Sec III.

Milgrom arXiv:0911.5464v2, Sec5 eq60,66,67–69, explicitly gives distinct QUMOND and nonlinear-Poisson external responses under constant-boundary assumptions. The source paper authenticates the comparison hypotheses, not projected-action covariant health or a solar exclusion. [Exact primary](https://arxiv.org/pdf/0911.5464v2). Hees et al. 1402.6950v2 eq6 authenticates the historical quadrupole convention. [Historical primary](https://arxiv.org/pdf/1402.6950v2).

## 6. Reproducibility and limits

SOURCE_AUDIT.json is the bounded source-revision snapshot. sources.json records exact primary URLs/versions and locators; no full PDF bytes were downloaded, so original PDF hashes are null rather than invented. Re-auditing literature requires reopening those versions. checks.py differentiates the constitutive vector, checks the dimension-free radial harmonic identity, exact Fourier/equatorial differences, angular l4 coefficient and bounded 40-digit calculations. No peer script is imported or rerun.

Three controls falsely transfer spherical equivalence into EFE equivalence, apply the far formula at an internally dominated radius, or omit the Newtonian sum potential. The preserved initial 18/19 preflight used structural equality of a substituted derivative and an evaluated derivative. Calling doit proves the same Jacobian identity; the formula was unchanged. It is not passed evidence. Current bounded manifests and counts are in RUNS.json. Full solar matching, clock/source admission, EFT health and any covariant vacuum selector remain open.
