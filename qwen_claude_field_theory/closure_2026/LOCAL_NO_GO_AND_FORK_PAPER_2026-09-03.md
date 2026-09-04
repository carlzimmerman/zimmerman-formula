# Obstruction map for tested relativistic completions of exponential-MOND phenomenology, and the inertia–gravity fork on galaxies

*Version 2026-09-03 (v2.1, corrected draft for internal review; v2.1 adds the PPN-invisibility theorem to §3.1). Each computational claim below carries its cited artifact and scope. Checks, mutation controls, and numerical footings vary by artifact. Script paths are given inline; the table in §10 lists them.*

---

## Abstract

We consider the phenomenological framework in which the Milgromian acceleration scale is the free-fall acceleration of the dark-energy density, $a_0=\tfrac12 c\sqrt{G\rho_\Lambda}=c^2\sqrt{\Lambda/32\pi}$. We distinguish the fitted algebraic RAR function $\nu_{\rm RAR}$ from the exact exponential AQUAL constitutive law $\mu_{\exp}$. Conditional on the premise that $a_0$ is a universal local acceleration scale, dimensional analysis fixes the $\sqrt\rho$ scaling but not the fitted coefficient $\tfrac12$. Across three tested, non-exhaustive local architecture families, named candidates fail specific gates. In the tested constraint reductions the scalar response is $\omega$-independent; where that response is the physical MOND mediator it fails the stipulated no-unacceptable-instantaneous-channel gate, but $\alpha_1$, $\alpha_2$, and $\alpha_3$ remain uncomputed absent a boosted 1PN metric/matter solution and standard-PPN gauge matching. A new regular-center theorem supplies an independent obstruction: exact $\mu_{\exp}$ and no slip turn any smooth positive-density spherical core into a finite-action but non-$C^2$ metric with divergent Ricci and tidal curvature. The other candidate-specific local, nonlocal, cluster, and inertia–gravity results are mapped with their individual scopes. This paper claims no completed relativistic theory, no exhaustive classification of all local actions, and no global novelty theorem; it claims a reproducible map and a new repository-level central-core prediction.

---

## 1. The framework, and exactly what is and is not asserted

**The equation.** $a_0=\tfrac12 c\sqrt{G\rho_\Lambda}$. Equivalent forms: $a_0=c^2\sqrt{\Lambda/32\pi}$; $a_0=cH_0\sqrt{3\Omega_\Lambda/32\pi}\simeq0.144\,cH_0$. Numerically $9.36\times10^{-11}$ m s$^{-2}$ (Planck $H_0=67.4$, $\Omega_\Lambda=0.69$); the SPARC-fitted value is $1.2\times10^{-10}$. Both footings, $9.36\times10^{-11}$ (canonical) and $1.13\times10^{-10}$ (alternative), are carried through every calculation.

**What is forced.** Given one premise—$a_0$ is a universal *local* acceleration scale, so its inputs are $\{c,G,\rho\}$—Buckingham-$\Pi$ leaves exactly one dimensionless group: $a_0=\kappa c\sqrt{G\rho}$. The form and the exponent are not choices (`real_research/uniqueness_dimensional_proof.py`). Two things are not forced and are stated as such: the premise itself (Milgrom calls $\Lambda$-versus-$H_0$ "moot"; the premise is the content), and the coefficient $\kappa$, which is fitted: $\kappa=0.465\pm0.076$ (BTFR) and $0.551\pm0.043$ (distance-free), bracketing $\tfrac12$, with $\tfrac12$ versus $1/2\pi$ separated at $\sim4\sigma$ (`real_research/reviews/mi_kappa_error_budget_unlock_2026.py`). For the displayed acceleration-kernel actions studied here, $\ell_0=c^2/a_0$ cancels at quadratic order and $a_\mu=0$ on FLRW; those sectors therefore do not fix $\kappa$. This is not a theorem about every possible homogeneous or quadratic completion.

**The two functions that must not be conflated.** The phenomenological algebraic RAR fit used in the galaxy analyses is $\nu_{\rm RAR}(y_N)=[1-e^{-\sqrt{y_N}}]^{-1}$, $y_N=g_{\rm bar}/a_0$. Separately, the relativistic-action target is exact AQUAL $\mu_{\exp}(x)=1-e^{-x}$, $x=g/a_0$. In spherical symmetry its boost $\nu_{\rm AQUAL}$ is defined implicitly by $y_N=x\mu_{\exp}(x)$ and $x=\nu_{\rm AQUAL}(y_N)y_N$, hence
$$\nu_{\rm AQUAL}(y_N)\left[1-e^{-\nu_{\rm AQUAL}(y_N)y_N}\right]=1.$$
No exact identity between $\nu_{\rm RAR}$ and $\nu_{\rm AQUAL}$ is claimed; they share the deep-MOND and Newtonian limiting behavior but differ at finite acceleration.

**Where it works.** 147–175 SPARC rotating discs at 0.06 dex; the Milky Way rotation curve; the vertical force (`prep_2026`); Renzo's rule. A theorem of this repository (`hunt_2026/k_unexplained-regularities_closure.py`) shows that ten of twelve "unexplained galactic regularities" in the literature, including the baryonic Tully–Fisher relation, are reparametrisations of the radial acceleration relation to machine precision under a seeded derangement shuffle; only a two-radius statistic and a non-multiplicative statistic escape. The framework's galactic content is therefore one relation.

**Where it fails.** Every pressure-supported system (`hunt_2026/THE_LIABILITY_TABLE.md`): clusters need $\times2$–$3$ at $R_{500}$ and their cores are Newtonian at $g\approx20a_0$; groups, ellipticals, dwarf spheroidals, ultra-diffuse galaxies, globular clusters. The external-field slope is measured at $+0.080\pm0.047$ where modified gravity predicts $-0.093$, a sign disagreement at $3.7\sigma$ (`hunt_2026/f03_efe_slope_prediction.py`).

**The gates.** For the exact-AQUAL action target, distinct from the fitted $\nu_{\rm RAR}$ relation above, a relativistic completion must produce $\mu(y)=1-e^{-y}$ exactly in the quasi-static limit from one action, with $N_{\rm grav}=2$ tensor degrees of freedom plus at most one healthy scalar (all degrees of freedom explicit, counted, healthy); $\Phi=\Psi$ derived; full PPN with $\gamma=\beta=1$, $\alpha_{1,2,3}=0$ (Cassini $|\gamma-1|<2.3\times10^{-5}$; pulsar $|\alpha_3|<4\times10^{-20}$); $\nabla_\mu T^{\mu\nu}=0$ as a Noether identity; $c_T=c$ to $10^{-15}$; stability with no unacceptable instantaneous physical channel; a dynamically accelerating FLRW background; a controlled $y\to0$ limit; $G_N$ derived; one metric (`FRIED_CHICKEN_SPEC.md`).

---

## 2. Assumptions and scope of the obstruction map

- **A1** The matter coupling is metric, or metric plus a Bekenstein-form disformal term $B\,\partial_\mu\phi\,\partial_\nu\phi$.
- **A2** Locality: the action is a local functional of the fields (the nonlocal case is treated separately in §5).
- **A3** At most one propagating scalar beyond the two tensor polarisations, or a unit timelike vector.
- **A4** On the relevant quasistatic branch, dynamics and lensing require $\Phi=\Psi$ at leading weak-field order. Calling this $\gamma_{\rm PPN}=1$ additionally requires a complete 1PN solution and standard-PPN gauge/matching; the KiDS statistic is not that derivation.
- **A5** GW170817: $|c_{\rm GW}/c_{\rm light}-1|<10^{-15}$ along the observed path.
- **A6** Pulsar bound $|\alpha_3|<4\times10^{-20}$; Cassini $|\gamma-1|<2.3\times10^{-5}$.
- **A7** An expanding background with $H\neq0$.
- **A8** The exact AQUAL equation applies through smooth positive-density matter, and the physical weak metric is at least $C^2$ with bounded classical curvature at a regular force-free center.

A2 and A8 are load-bearing for different claims. Results in §§3–4 are conditional on each subsection's displayed field content, action, and branch assumptions; they do not exhaust the local class.

---

## 3. Local obstruction map, by tested branch

We audit three broad, non-exhaustive architectures represented by explicit candidate actions in the repository.

### 3.1 The constraint branch: bounded successes, open PPN, and a regular-center obstruction

The HPI-$\Delta$ candidate is the strongest bounded construction in this branch. Its first-order action retains the Einstein Hamiltonian and adds one trace-momentum Laplacian constraint. On the tested $k\neq0$, $y>0$ scalar block, the generated eight-constraint chain has Poisson rank six, two first-class and six second-class constraints, and zero scalar configuration degrees of freedom. Independent leading static-dust variations give $\nabla^2(\Phi-\Psi)=0$ and exact exponential AQUAL in the bounded branch. This is not yet a derivation of $\gamma_{\rm PPN}$. The configuration action and a clock-covariant notation are derived in `hpi_delta_covariant_lift_2026/`; a full nonlinear covariant Dirac theorem is not.

In the tested CDE-L4C and vanishing-projector reductions, the principal scalar response is proportional to $1/k^2$ and independent of $\omega$. This is a valid instantaneous-channel diagnostic when that response is the physical MOND channel; it is not a PPN coefficient. The corrected CDE-L4C provenance audit leaves $\alpha_1$, $\alpha_2$, and $\alpha_3$ uncomputed. A full boosted 1PN solve—including $g_{00}$, $g_{0i}$, $g_{ij}$, all constraint/multiplier backreaction, moving conserved matter, and standard-PPN gauge matching—is required.

That solve, if done, cannot close the branch. In every constraint construction here the MOND channel couples to matter and metric only through $F_{\exp}(y)=2[(1+y)e^{-y}-1]$, whose coupling $F'=-2ye^{-y}$ and linear response $F''=2(y-1)e^{-y}$ carry $e^{-y}$. At every post-Newtonian test site $y=g/a_0$ is large—$7\times10^5$ at Saturn, $6\times10^7$ at Earth, $\sim2\times10^{12}$ in a binary-pulsar orbit—so the channel's contribution to $\gamma-1$, $\beta-1$, $\alpha_{1,2,3}$ and $\xi$ is suppressed by $e^{-y}$, below $10^{-300000}$ at the weakest site (`cde_l4c_2026/gateA/constraint_channel_ppn_invisibility_2026.py`, 9/9, both footings). The constraint channel of the exponential kernel has GR's PPN status and no solar-system or pulsar datum can change it; the same tail that makes the kernel Cassini-safe makes the channel invisible wherever it is tested, and it switches on at the Oort cloud ($y\simeq2.5$ at 5000 AU) as the wide-binary predictions require. The scope is a channel whose only coupling is $F$; the Einstein-aether vector of §3.3 has an $F$-independent kinetic sector, so its $\alpha_1$ kill is unaffected. What therefore constrains this branch is not data but two principles: the regular-center theorem below (A8), and gate 7 as stated—no instantaneous physical channel—whose justification is the York/CMC causality argument (`theory_2026/york/YORK_CAUSAL_GATE_VERDICT.md`: the external-field effect promotes the elliptic potential to a gauge-invariant observable delivered at equal time across spacelike separation), which rates itself "medium confidence, structurally robust at linear order."

The exact zero-field law supplies a different, action-independent obstruction. Let $A(p)=(1-e^{-|p|/a_0})p$. Then $DA(0)=0$, so any $C^2$ solution with $\nabla\Phi(x_0)=0$ obeys $\nabla\!\cdot A(\nabla\Phi)(x_0)=0$ and the exact field equation forces $\rho(x_0)=0$. For a smooth spherical core with $\rho(r)=\rho_0+O(r^2)$ and $C=4\pi G\rho_0/3$,
$$g(r)=\sqrt{a_0Cr}+\frac C4r+O(r^{3/2}),\qquad R^{(1)}\sim\frac{5\sqrt{a_0C}}{c^2\sqrt r}.$$
The weak solution has finite action but the no-slip physical metric is not $C^2$ and its Ricci and tidal curvature diverge. Thus HPI-$\Delta$ is dead as an exact classical regular-center theory under A8, without invoking any PPN identification (`exact_mond_regular_center_no_go_2026/`).

### 3.2 The frame-free branch: slip, and the disformal escape

A single frame-free scalar $F(X)$, $X=-\tfrac12(\partial\phi)^2$, has anisotropic stress $\propto F_X\partial_i\phi\partial_j\phi$ that sources $\nabla^2(\Phi-\Psi)\neq0$ at $O(\Phi)$ in the MOND regime (the Bekenstein–Sanders result that forced TeVeS's vector; DC-013). One tested escape in the named model is a disformal matter coupling, $\tilde g_{\mu\nu}=g_{\mu\nu}+B\,\partial_\mu\phi\,\partial_\nu\phi$, whose spatial correction shares the tensor structure $\partial_i\phi\partial_j\phi$ of the scalar stress and can therefore cancel the slip *pointwise* (`door_a_2026/doorA_disformal_slip_vs_cT.py`, check A1). It dies on one identity (check A2): the no-slip condition fixes $B\phi'^2=2(\Psi-\Phi)$, and that same quantity is the fractional difference between the null cone of $g$ (gravitational waves) and of $\tilde g$ (light):
$$\frac{c_{\rm GW}-c_{\rm light}}{c}=\frac{B\phi'^2}{2}=(\Psi-\Phi)_{\rm uncancelled}.$$
The slip cancelled is the light-cone tilt created. In a galaxy's MOND outskirts $\Psi-\Phi\sim\epsilon\,\Phi_{\rm MOND}$ with $\Phi_{\rm MOND}=v_{\rm flat}^2/c^2=3.9\times10^{-7}$ (NGC 4993's host), $3.0\times10^{-7}$ (Milky Way). Along GW170817's path the two galaxies' MOND regions give $2\times10^{6}\,\epsilon$ over the bound; the 40 Mpc of intergalactic medium alone, suppressed by $(g_{\rm IGM}/g_{\rm gal})^2$, still exceeds it by 30–300. Cassini is untouched because the scalar carries no force at solar-system accelerations (check A6): the escape trades gate 3 for gate 6 and nothing else. Calibrated against the repository's own curvature-clock kill (a light-cone tilt of $-2\times10^{-7}$, excluded $10^5$–$10^9\times$). 9/9 checks; mutation controls $B=0$ (slip returns, tilt vanishes) and $\phi'=0$ (GR).

### 3.3 The preferred-frame branch: the $\alpha_1$ lock

In the Einstein-aether + shift-scalar class the closed form is
$$\alpha_1=-4c_{14}-\frac{4(2-K_B)}{J_Y+1},\qquad c_{14}=K_B+c_4,$$
verified against a $4\times3$ $(K_B,J_Y)$ grid (`generalized_aest_2026/`). The drag coefficient $(2-K_B)$ *is* the MOND-generating coupling $2(2-K_B)J\!\cdot\!\nabla\phi$. `door_a_2026/doorA_alpha1_generality_theorem.py` (12/12) proves the kill is structural rather than a parametrisation artefact:
- **T2a** the MOND piece $-4(2-K_B)/(J_Y+1)$ is independent of the free kinetic knob: $\partial/\partial c_4=0$;
- **T2b** it is sign-definite (negative) for all $0<K_B<2$, $J_Y\ge1$;
- **T2c** it vanishes exactly when MOND is off ($K_B=2$), at which point $\alpha_1=-4c_{14}$ is zeroable at $c_{14}=0$, ghost-free.

So $\alpha_1=0$ can be reached only at $c_{14}=(K_B-2)/(J_Y+1)<0$, which flips the spin-1 kinetic sign (verified: $-0.429$ healthy vs $+1.930$ at the null locus). Solar screening worsens it ($\alpha_1$: $-4.4\to-5.65$). The term that makes MOND breaks preferred-frame PPN.

Two other tested preferred-frame embeddings are killed by the *same* coupling: a curvature-coupled clock forces $\lambda_r=-a_0\,y\,e^{-y}\neq0$ in the tensor kinetic term, $c_T^2=1/(1-2\lambda)$ departs from 1 by $\sim2\times10^{-7}$ in every MOND zone, excluded $10^7$–$10^9\times$ (`one_shot_final/curvature_qumond_luminality_no_go_2026.py`, 6/6; `…observational_strengthening_2026.py`, 11/11); an acceleration-coupled khronon has $c_\parallel^2\propto f''<0$ on $a_0<a<38a_0$, an uncurable radial gradient instability (`fc_kh_terminal/`, and the $(yq)'$ theorem). Three tested embeddings, one recurring mechanism.

### 3.4 Statement

**Theorem (regular center, conditional on A8).** Any theory whose no-slip weak branch obeys exact exponential AQUAL pointwise inside a smooth spherical positive-density core fails bounded classical curvature at its force-free center. Equivalently, retaining the exact law requires a $C^{1,1/2}$ weak potential rather than a $C^2$ physical metric. This theorem is independent of the candidate carrier and the numerical footing of $a_0$. The remaining subsections establish candidate-specific failures, not an exhaustive theorem over every local metric-plus-scalar/vector action.

---

## 4. Clusters: no dark component can supply the residual

Suppose the cluster residual is a dark component. Structure caps a hot (free-streaming) fraction of the dark sector at $f_h\le0.0375$, through the standard $\Delta P/P\simeq-8f_h$ suppression against a Lyman-$\alpha$ forest measured to 10–20 per cent. The framework's own galaxies require $f_h\ge0.30$–$0.80$, because whatever is not hot is cold, and a cold component clusters into galaxies exactly as cold dark matter does—and the framework's galactic success *is* the statement that there is nothing cold in galaxies. All nine pairings of the most generous bound on each side fail; the tightest gap is a factor of eight (`hunt_2026/f07_two_component_nogo.py`, 6/6; single-species and free-streaming versions in `f04`–`f06`). The result is structural, so a third component does not help. The escape that a MOND cosmology regrows erased power is closed for this framework by its own bulk-flow null ($\beta=0.447$ against $\Lambda$CDM's $0.440$), which measured its linear regime Newtonian.

---

## 5. The nonlocal door: scoped failures and an open class

A2 is load-bearing, so the nonlocal spin-2 class is examined separately (`nonlocal_door/`). Under the explicit regularity, spectral, and form-factor hypotheses recorded in the state-space verdict of 2026-09-02, the named positive-spectral causal completion, pole-free regular metric completion, and Ricci-polynomial elliptic projector fail their stated gates. The corrected rank-change result withdrew "every regular metric-only projector is excluded" and left one loophole: a field-dependent spatial projector $H^{\mu\nu}=X(g^{\mu\nu}+u^\mu u^\nu)$ that is rank three away from zero field and vanishes smoothly at $X=0$, whose constraint structure changes rank.

`nonlocal_door/vanishing_projector_dirac_chain_2026.py` (13 checks) runs Dirac's algorithm through that bifurcation. On the $u$-frame background $H^{00}=X(-1+1)=0$, so no time derivatives survive. For $X\neq0$: two primaries, two secondaries, $\det C=X^4k^8$, four second-class constraints, multipliers fixed, no tertiary, zero degrees of freedom, on-shell $\chi=-J/(Xk^2)$. For $X=0$: one secondary vanishes identically, the other degenerates to the constant $J$, the primaries become first class, zero degrees of freedom, and consistency demands $J\propto X$. **The bifurcation changes the class of the constraints, not the count.** This candidate-specific $u$-frame, $k\neq0$ auxiliary reduction has zero auxiliary degrees of freedom on both branches. Its physical MOND response is instantaneous and its $X\to0$ solution map is path-dependent, so this specified reduction is adverse on gates 7 and 9. It does not establish full ghost freedom, and $\alpha_1$, $\alpha_2$, and $\alpha_3$ are uncomputed.

What remains is an unconstructed possibility: a genuinely retarded, $\omega$-dependent constrained kernel that yields $\mu=1-e^{-y}$; §4 of the state-space verdict shows positive spectral weight costs extra carrier states. The broader nonlocal door remains open.

---

## 6. The fork the map leaves open: inertia or gravity

### 6.1 The pattern

Read the liability table by how each system holds itself up: every system the framework fits is rotation-supported, every system it misses is pressure-supported, across eleven decades of mass and five of size. Milgrom proved that modified inertia and modified gravity agree exactly for circular orbits in the deep-MOND limit and differ for every other orbit. The split is therefore a theory fork, and this repository ran only the modified-gravity arm from 2026-08-08 until 2026-09-03.

### 6.2 Pressure-supported systems

*Satellites.* Matched at internal acceleration, rotating systems sit on the kernel ($+0.013\pm0.175$ dex, $N=105$) and the eight classical Milky Way dwarf spheroidals sit above it ($+0.228\pm0.349$), a $1.73\sigma$ hint whose sample size is the ceiling; the residual's sign tracked a branch of the external-field prescription, recorded as a check that fails (`hunt_2026/f09_orbital_coherence_fork.py`).

*Isolated dwarfs.* On ten isolated Local Group dwarfs with modern dispersions (Cetus 8.3, Tucana 6.2 km s$^{-1}$; the 2012 values would have manufactured a 0.4 dex excess), Milgrom's exact deep-MOND virial law $\sigma^4=\tfrac{4}{81}GM_{\rm bar}a_0$—proved for any spherical profile in `f11`—is off in zero-point by $+0.06$ to $+0.18$ dex across the mass-to-light and external-field box, and, more decisively, **off in exponent**: the slope of $\log\sigma$ on $\log M_{\rm bar}$ is $0.072\pm0.038$ for the isolated dwarfs and $0.088\pm0.024$ for the classical satellites, each more than $4\sigma$ from $\tfrac14$ (`f14`, corrected by `f15`). Dwarf dispersions are nearly mass-independent over three decades—Strigari's common mass scale—and this is not confined to external-field-dominated satellites. The relation is radius-free (Newton would need $-0.5$ in $\log r_h$; measured $+0.08\pm0.07$), so the data prefer an acceleration-scale structure with an exponent the theory does not produce.

*Globular clusters.* The confound-free pressure-supported systems (baryon-dominated, no dark halo claimed). Of 157 in the Baumgardt catalogue only 16 have both a sub-$a_0$ interior and a sub-$a_0$ external field; on them the framework **over**-predicts the dispersion by $+0.30$ dex with the external-field effect on and $+0.56$ without (`f13`). The external-field effect of modified gravity is *required* to keep it that close; a modified-inertia arm with a weaker effect makes the clusters worse. So the two pressure-supported populations pull the fork in opposite directions: dwarfs under-predicted, clusters over-predicted.

### 6.3 Rotating discs: the curl field

`f12` proved the disc virial coefficient is $0.82$, not the spherical $\tfrac23$ (the kernel predicts $0.823$ from the baryons alone; the observed curves deliver $0.826$), and concluded that rotating galaxies can never decide the fork because what they test is a circular-orbit identity. That conclusion was wrong, and finding the error is the origin of the test that follows. It is true of the *algebraic* relation $g=\nu(g_N)g_N$ only. Modified inertia gives that relation exactly for circular orbits. Modified gravity's true disc field is the algebraic one *plus a curl field* that vanishes for spheres and not for discs (Brada & Milgrom 1995). The two arms therefore differ on every disc.

We compute the curl template with a derivative-free QUMOND solver validated against Freeman's closed form (to 5.5 per cent for a $z_0=0.02R_d$ disc, the residual being the known thickness reduction) and the exact spherical identity (`f16`). For a deep-MOND exponential disc the algebraic relation over-boosts by 42 per cent at $0.1R_d$ and 20 per cent at $R_d$, crosses zero near $3R_d$, and under-boosts by 2 per cent at 5–7$R_d$; the correction shrinks monotonically as the disc becomes less deep (`f17`, six-depth family). Against 1214 deep-MOND SPARC points with galaxy fixed effects and a kernel-shape slope, the template amplitude $A$ (modified inertia 0, modified gravity 1) is **degenerate with the stellar mass-to-light ratio**: every model with an unconstrained M/L term fails its own shuffle-null test (floors 0.45–0.65), and in those models $A\to+1.1$ only by shifting $\Upsilon_{3.6}$ by $0.6$ dex ($0.5\to\sim2$), which population synthesis excludes. Within the allowed $|\delta\Upsilon|\le0.1$ dex the amplitude runs $A=-0.30$, $-0.11$, $+0.16$ with galaxy-bootstrap error $\pm0.5$: modified gravity's value is disfavoured by 1.8–2.7$\sigma$, modified inertia's is consistent. With each disc's own template from its own inverted baryon profile (`f18`; 37 of 88 profiles invert to 5 per cent) the bootstrap shrinks to $\pm0.32$ but the fitted $A=-0.98$ is a value neither arm predicts and the shuffle floor is 0.53, so the amplitude is not a fork verdict.

What is robust is the **sign**. In the 0.7–2$R_d$ band the stacked residual is $+0.109\pm0.012$ dex (galaxy-correlation-inflated error) while every modified-gravity curl template there is negative. Modified gravity's curl requires the inner disc *below* the algebraic relation; SPARC's deep discs sit *above* it. This is amplitude-free and needs no identifiable fit. It disfavours the modified-gravity curl field. It does not confirm modified inertia, which predicts zero there; the $+0.1$ dex inner excess is an unexplained feature for both arms, with an inner mass-to-light gradient the mundane suspect.

### 6.4 The fork's status

Modified inertia is the less wrong arm on discs and on dwarfs; modified gravity's external-field effect is required on globular clusters. Modified inertia has no accepted relativistic completion, and this repository's own rapidity-gap modified-inertia action was excluded at $21\sigma$. The cheapest observational decider—an eccentricity split of the Gaia wide-binary ratio—is shut: the projected-angle slope reverses sign between thermal and uniform eccentricity populations (`f10`). The fork is open.

---

## 7. The one distinctive prediction, and what decides it

If $\Lambda$ is a constant, $\rho_\Lambda$ is constant and $a_0$ is **flat** in redshift. The emergent radial-acceleration scale of $\Lambda$CDM halos is not: it rises to $+0.33$ dex (Dutton & Macciò 2014; $+0.45$ for Duffy et al. 2008) by $z\simeq2.5$ from halo structure. On present data the two are prior-dominated and undecided; the RC100 closed-form inversion $a_0=(1-f_{\rm DM})g_{\rm obs}/[\ln(1/f_{\rm DM})]^2$ gives $d\log a_0/dz=-0.112\pm0.063$, disfavouring the rise at $3.9\sigma$ while being a monotone restatement of RC100's own falling dark fractions and therefore a constraint on the rise, never a detection of a decline (`hunt_2026/h16_h27_h97.py`). One clean deep-MOND rotator at $z\simeq2.5$ with a baryonic mass good to $0.13$ dex decides at 20:1. The Gaia DR4 wide-binary band is frozen and hash-stamped at $\gamma_v=1.1614$–$1.1814$ (Amendment 10) and is not touched by anything in this paper.

---

## 8. Two companion theorems on the dark sector (stated, verified, not extended here)

*The well–cosmology sum rule.* For any single-branch shift-symmetric barotrope $p=K(Q)$, $c_s^2=d\ln Q/d\ln n$; with the static Klein relation $NQ=$ const and the conserved charge $n\propto(1+z)^3$, a galaxy well of overdensity $\delta$ matches the cosmic background at $(1+z_{\rm match})^3=\delta$ and obeys $\Psi_B-\Psi_W=3\int_0^{z_{\rm match}}c_s^2\,dz/(1+z)$. By the mean-value theorem some epoch below $z_{\rm match}=3$ must have $c_s\gtrsim74$–$123$ km s$^{-1}$ for a $150$–$250$ km s$^{-1}$ well; an exotic $K$ can relocate the warm epoch, not erase it. The $\gamma=2$ polytrope is the special case $c_{s,W}^2=\Psi_B-\Psi_W$. For that polytrope the stiffness parameter cancels from the matched Jeans scale, $k_{J,{\rm match}}=(H_0/v_\Phi)\sqrt{3\Omega_d/2}\,\sqrt{1+z_{\rm match}}=0.50$–$0.84\,h$ Mpc$^{-1}$. Caveat, load-bearing: the Lyman-$\alpha$ window $z=2$–3 covers 21 per cent of the sum-rule range; a $K$ that parks its warmth at $z<2$ passes the forest and is owed to lower-redshift growth data. The Klein relation is assumed with the MOND drag off.

*The $\kappa$ obstruction.* With $F_{\exp}(y)=2[(1+y)e^{-y}-1]=-y^2+\tfrac23y^3-\tfrac14y^4+\dots$, the term $-(2/\ell_0^2)F_{\exp}$ is $2a^2-\tfrac43\ell_0 a^3+\dots$: $\ell_0$ cancels at quadratic order and $a_\mu=0$ on FLRW, so neither the background nor the quadratic theory can fix $\kappa$. The first opportunity is the cubic vertex, through $\zeta=H_\Lambda\ell_0/c$, with $\kappa=\tfrac12\Leftrightarrow\zeta=\sqrt{32\pi/3}$. Whether a regularity condition on the cubic Dirac chain produces that root, or leaves $\zeta$ free, is an open, well-posed calculation; the standing expectation is the latter.

---

## 9. What this paper does not claim

- It does not present a completed relativistic theory or a theory of everything. Its central result is a scoped obstruction map plus the conditional regular-center theorem, not an exhaustive local no-go.
- It does not claim $\kappa=\tfrac12$ is derived. It is fitted, and §8 shows where a derivation would have to live.
- It does not claim the data favour the framework over $\Lambda$CDM. The one discriminating measurement (§7) has not been made.
- It does not claim the constraint (two-degree-of-freedom) branch is excluded by post-Newtonian data: under the exponential kernel its channel is PPN-invisible (§3.1). What constrains it is the regular-center theorem under A8 and the no-instantaneous-channel principle, the latter at medium confidence.
- It does not claim the broader nonlocal door is closed; the vanishing-projector calculation closes only its specified reduced mechanism on gates 7 and 9.
- It does not claim modified inertia is confirmed. It claims the modified-gravity curl field has the wrong sign on SPARC's deep discs, and that pressure-supported systems break the kernel in both directions.
- Every "fails" was verified as hard as every "works": the 2012 dwarf dispersions, the $+1.1$ curl amplitude, the $-0.98$ amplitude, and the $10\sigma$ virial offset of `f11` were each caught by a control and are recorded as such.

---

## 10. Reproducibility

Run each cited artifact according to its own documented interface. Checks, mutations, and numerical footings vary by artifact.

| claim | script | checks |
|---|---|---|
| form and exponent forced | `real_research/uniqueness_dimensional_proof.py` | — |
| $\kappa$ measured | `real_research/reviews/mi_kappa_error_budget_unlock_2026.py` | — |
| CDE-L4C PPN provenance: $\alpha_3$ uncomputed | `cde_l4c_2026/gateA/cde_l4c_ppn_alpha3.py` | 4/4 |
| constraint channel PPN-invisible under the exponential kernel | `cde_l4c_2026/gateA/constraint_channel_ppn_invisibility_2026.py` | 9/9 |
| HPI-$\Delta$ action/covariant-lift gate | `hpi_delta_covariant_lift_2026/` | 16/16 |
| exact-MOND regular-center theorem and central Kepler law | `exact_mond_regular_center_no_go_2026/` | 17/17 |
| disformal escape: slip $\to$ $c_T$ | `door_a_2026/doorA_disformal_slip_vs_cT.py` | 9/9 |
| $\alpha_1$ structural lock | `door_a_2026/doorA_alpha1_generality_theorem.py` | 12/12 |
| curvature-clock $c_T$ | `one_shot_final/curvature_qumond_luminality_no_go_2026.py` | 6/6 |
| khronon gradient instability | `fc_kh_terminal/` | — |
| vanishing projector Dirac chain | `nonlocal_door/vanishing_projector_dirac_chain_2026.py` | 13 checks |
| cluster dark-component no-go | `hunt_2026/f04`–`f07` | 6/6, 8/8, 7/7, 6/6 |
| external-field slope | `hunt_2026/f03_efe_slope_prediction.py` | 4/4 |
| closure of galactic regularities | `hunt_2026/k_unexplained-regularities_closure.py` | — |
| rotation/pressure matched pair | `hunt_2026/f09_orbital_coherence_fork.py` | 7 (2 fail by design) |
| wide-binary eccentricity shut | `hunt_2026/f10_eccentricity_falsifier.py` | 7 (2 fail by design) |
| disc virial coefficient | `hunt_2026/f11`, `f12` | 12 (3 fail), 6/6 |
| globular clusters | `hunt_2026/f13_globular_clusters_confound_free.py` | 5/5 |
| isolated dwarfs, exponent | `hunt_2026/f14`, `f15` | 10/10, 10 (4 fail by design) |
| curl field on discs | `hunt_2026/f16`, `f17`, `f18` | 9 (1 fail), 14 (4 fail), 11 (4 fail) |
| RC100 inversion | `hunt_2026/h16_h27_h97.py` | 5/5 |

Repository: `github.com/carlzimmerman/zimmerman-formula`.
