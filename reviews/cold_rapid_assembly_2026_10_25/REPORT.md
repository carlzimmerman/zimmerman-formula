# Rapid collapse and mergers: fast enough, but not an absolute selector

The existing source-free selective cold-wave equations do not determine a nonzero cluster cold mass from the baryons and vacuum alone. Rapid assembly can rearrange or capture an independently supplied population. The tests here show explicitly where its supply, energy and orbital distribution enter. They do not exclude a statistical attractor once a cosmological ensemble is independently specified, and they do not constitute a self-consistent cluster merger simulation.

**New quantitative result:** the inherited cluster states have R/vc = 0.148–1.085 Gyr. Unlike secular wave relaxation, assembly is not rejected by its characteristic timescale. But an exact impulsive tracer control spans 100% to zero capture at fixed final potential and initial spatial density as the incoming speed changes. Equal total mass, energy and zero vector spin do not fix a radial profile. A merger energy budget likewise retains orbital-energy dependence.

No a0, eta, source amplitude, velocity distribution or halo profile was fitted. The original microscopic vacuum/force matching problem remains open.

## 1. Equations and the exact supply obstruction

This is the CCT selective-coupling candidate, not the literal v3s field system:

    i eta d_t psi = [-eta² laplacian/2 + Phi_b,N + Phi_c] psi,
    laplacian Phi_c = 4 pi G |psi|².

Cold feels Newtonian baryon gravity and its own gravity. Baryons also feel their separate baryon-only modified force. Eta=1500 pc km/s remains imposed.

For real potentials, even when Phi_b,N changes rapidly,

    d_t rho + div j = 0,  j = eta Im(psi* grad psi),
    d_t M_V = - integral_boundary j dot n dA.

Thus global cold mass is conserved for isolated matching boundaries. An initially zero cold field stays zero through arbitrary prescribed baryonic collapse or mergers. An arbitrarily small finite global inventory cannot provide a larger cluster requirement. This is a direct obstruction to an absolute nonzero mass prediction across *all* allowed initial states; it is not an assertion that retained mass must vary for every pair of sufficiently large supplies. Saturation within a restricted ensemble remains possible.

The present inverse cluster requirements at R500 span 6.88e13–3.96e14 solar masses across seven systems, five released mass models and two inherited a0 footings. These 70 alternatives are not independent observations. Each is a required source under that reconstruction, not a measured standalone cold component. Some profiles have negative shells; those are not made physical by this mass-budget test, and the previous missing-covariance caveat remains.

Any successful assembly must supply at least its required enclosed mass, and more if mass remains elsewhere or escapes. A vacuum energy term that supplies no source in this continuity equation does not specify this inventory.

## 2. The fast-timescale gate passes, conditionally

Reuse the 303 positive shell/model/footing records from the previous audit, taking its sigma=vc entry once per shell. There vc²=G(M_b+M_c)/R, appropriate to the selective cold force; it is not the baryonic MOND acceleration. The range R/vc=0.147665–1.084672 Gyr is a crossing-scale estimate, not a measured formation duration. A crossing time does not ensure relaxation, nor reveal the number/timing of mergers. The result only removes the many-orders-of-magnitude timing objection that applied to secular wave scattering.

## 3. Explicit capture dependence in a rapid-collapse control

In the classical tracer limit, switch the external potential instantaneously from zero to

    Phi_f(r) = -GM/sqrt(r²+b²).

Take uniform initial tracer density inside R=4b, with common speed v=q sqrt(GM/b). At the switch positions and velocities are continuous, and the external source does work Delta epsilon=Phi_f. Subsequently the potential is static. Bound energy is equivalent to

    r²/b² < 4/q⁴ - 1,
    F_bound(q) = min[1, max(0,4/q⁴-1)^(3/2)/64].

Independent equal-volume quadrature classifies the energy of 200000 initial cells per case:

| q | Captured fraction |
|---:|---:|
| 0.25 | 1 |
| 0.50 | 1 |
| 0.75 | 0.620669 |
| 1.00 | 0.081190 |
| 1.25 | 0.007970 |
| 1.50 | 0 |
| 2.00 | 0 |

All seven comparisons agree within 1/N. The final potential, supplied mass and spatial profile are identical across cases. Speed is varied as a sensitivity, not introduced as a new fitted parameter. The retained mass is F_bound M_supply. This is a controlled illustration of the dependence on incoming phase space and work history. It is not an exact solution for the finite-eta, self-gravitating cluster wave. The abrupt prescribed potential has an external energy budget; we do not call its work free or claim baryonic assembly is actually instantaneous.

## 4. Even mass, energy and net spin do not specify a profile

For a Kepler tracer ensemble with common semimajor axis a, all particles have epsilon=-GM/(2a). Isotropic orientations and paired opposite angular momenta give zero net vector spin at any eccentricity e. Uniform orbital time defines stationary spherical ensembles with differing distributions of angular-momentum magnitude.

With eccentric anomaly u,

    r/a=1-e cos u,  dt proportional to (1-e cos u) du.

For x=r_cut/a between 1-e and 1+e, the enclosed fraction is

    F(<x a) = [u0 - e sin u0]/pi,  u0=acos[(1-x)/e].

It is zero below pericentre and one above apocentre. At r_cut=a/2, the fractions for e=.2,.6,.9 are respectively 0, .0808581, .0743043. Time-weighted quadrature agrees within 2/N; vis-viva verifies the same energy at every phase. The nonmonotonic last two values reflect residence time, not a sign error.

These are tracer equilibria, not self-gravitating cluster endpoints and not a proof that no restricted ensemble can converge to a common coarse profile. They demonstrate that mass, energy and vector spin alone are insufficient closure. A merger calculation must predict the distribution of orbital actions/anisotropy, rather than silently pick it.

## 5. Merger energetics retain an assembly input

For isolated Newtonian virial endpoints define gravitational radius rg=-GM²/W, so E=-GM²/(2rg). For two equal progenitors of mass M and rg, in the deliberately restrictive case of no escaping mass/energy and no external work, let

    epsilon_orb = E_orb / [GM²/(2rg)].

Energy conservation requires

    rg_final/rg = 4/(2-epsilon_orb).

Orbital energies -1,0,+1 therefore require radius ratios 4/3,2,4 respectively *if a virial remnant forms*. The calculation does not assert that a positive orbital-energy encounter actually merges. Wave ejection, baryonic work, residual fragments and angular momentum add bookkeeping obligations, not automatically known numbers. The general budget is

    E_remnant = E_1 + E_2 + E_orbit + W_external - E_ejecta,
    M_remnant = M_1 + M_2 + M_inflow - M_outflow.

This virial example applies to the cold-dominated Newtonian limit, not to arbitrary externally bound or time-dependent configurations. It shows why specifying an equilibrium or assuming a parabolic encounter is not an independent selection of cluster size.

## 6. A concrete galaxy-preservation and supply condition

In the spherical selective branch, put B=M_b(<r), A=a0 r²/G and

    L(B,A) = [B+sqrt(B²+4AB)]/2,
    g_law = G L/r²,  g_total = g_law + G M_c(<r)/r².

If observations permit a fractional additional acceleration delta relative to the existing law, the exact aperture condition is

    M_c(<r) <= delta L(B,A).

Delta must come from the actual galaxy likelihood; no numerical tolerance is assigned here. Exact preservation (delta=0) requires zero additional spherical enclosed cold mass. This is not a disk or external-tide theorem: non-spherical fields require their full force calculation.

Now partition the merger supply into disjoint, galaxy-tested progenitor interiors plus everything outside those interiors. If there is no cold production, a necessary condition for a descendant cluster requiring M_req is

    M_outside >= max[0, M_req - sum_i delta_i L_i].

Here M_outside includes progenitor outer halos, diffuse material and later inflow. Outflow or cold mass left outside the descendant aperture can only increase the necessary supply. The inequality follows by adding nonnegative masses and the progenitor aperture bounds, not by assuming a retention efficiency. It cannot yet be evaluated for real assembly trees: their progenitor census and joint galaxy allowances are absent. It nevertheless excludes treating unrestricted inner galaxy cold mass as an invisible merger reservoir while demanding the original galaxy law.

A promising *conditional* mechanism is therefore selective capture from a diffuse or outer-halo reservoir. In the same impulsive control, a mono-speed supply is completely unbound in a galaxy when

    v² >= 2GM_g/b_g,

and completely bound throughout a cluster's initial radius R_c when

    v² < 2GM_c/sqrt(R_c²+b_c²).

A nonempty speed window exists if the latter threshold exceeds the former. This establishes a possible environmental filter, not a selected cosmic speed distribution. The symbols M_g,M_c here denote prescribed well-source masses in the tracer control, not the previously reconstructed cold requirements. Actual self-gravity, phase correlations, merger work and feedback must be solved together. Assigning a reservoir density, a speed within this window or separate galaxy/cluster histories merely to obtain the desired result would reintroduce the missing inputs.

## 7. What survives and what is required next

Rapid assembly survives as a physical transport route. It fails as an *unconditional* parameter-free mass selector for the existing source-free equations. The zero/small-inventory argument is exact; the finite controls expose capture, profile and merger-energy dependencies without fitting them away. No universal exclusion of statistical universality, self-gravitating violent relaxation or gravitational cooling is claimed.

The next genuine new mechanism must independently specify the cosmological cold inventory and phase-space supply (or derive a production term from the action). A formation calculation can then predict retention and profiles, with common rules across galaxies and clusters. It must track external work and outgoing mass/energy/angular momentum, converge numerically and pass the galaxy likelihood. Running a large merger with arbitrarily chosen supply before that step would be a conditional sensitivity experiment, not the requested parameter-free prediction.

The previously established density-matrix isospectral invariants are not a new result here. Fine-grained conservation does not by itself prohibit coarse-grained relaxation. Nor does a family of cooling attractors fix its member's mass. The literature gives useful context: Guzman & Urena-Lopez's [gravitational-cooling study](https://arxiv.org/abs/astro-ph/0603613) reports relaxation via field emission in spherical SP simulations, including self-interaction; this is not a prediction of our cluster inventory. Arad & Lynden-Bell's [violent-relaxation analysis](https://arxiv.org/abs/astro-ph/0409728) reports history dependence in particular equilibrium-statistical closures. Only their abstracts were checked here; neither is used as a theorem or a numerical calibration for this report.

## Reproduction and evidence status

Finite assertion verified in the declared range; continuum interpretations are limited as above. `check.py`, `contract.json` and `FROZEN_CRITERIA.md` define the calculation. `run/result.json` retains every crossing row and mass requirement. `run/manifest.json` records bounded execution and input/output hashes. `mutation/manifest.json` records the expected failure when the analytic capture threshold loses its factor of two, caught by independent energy classification.

Reproduce in a fresh output directory with the installed mathbox bounded runner, the four inputs listed in contract.json, a 60-second timeout and one numerical thread; invoke `python reviews/cold_rapid_assembly_2026_10_25/check.py --output <fresh-directory>`. Add `--mutate` only for the expected-failure control. Both original manifests are validated with the installed `validate_manifest.py --root .`. Results are self-reviewed, not independently refereed. No full formation run, new observational covariance, fitted halo, or microscopic vacuum matching has been supplied.
