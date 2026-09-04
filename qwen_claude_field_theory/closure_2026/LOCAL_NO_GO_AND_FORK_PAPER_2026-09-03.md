# No healthy local relativistic completion of the exponential MOND kernel with $a_0=\tfrac12 c\sqrt{G\rho_\Lambda}$: a structural no-go theorem, and the inertia–gravity fork on galaxies

*Version 2026-09-03 (v1, draft for internal review). A theorem paper. Every quantitative statement below is a committed, runnable script with numbered checks that can fail, at least one mutation control, and both numerical footings of $a_0$. Script paths are given inline; the table in §9 lists them all.*

---

## Abstract

We consider the phenomenological framework in which the Milgromian acceleration scale is the free-fall acceleration of the dark-energy density, $a_0=\tfrac12 c\sqrt{G\rho_\Lambda}=c^2\sqrt{\Lambda/32\pi}$, with the galactic kernel $\nu(y)=[1-e^{-\sqrt y}]^{-1}$, $y=g_{\rm bar}/a_0$. Conditional on the single premise that $a_0$ is a universal local acceleration scale, the $\sqrt{\rho}$ form and the exponent $\tfrac12$ are forced by dimensional analysis; the coefficient $\tfrac12$ is fitted to SPARC and is never claimed derived. We then prove, by exhaustion of cases with each case closed by a committed calculation, that **no local relativistic completion of this kernel passes the standard health gates simultaneously**: the constraint-based (two-degree-of-freedom) branch is instantaneous and carries $\alpha_3=O(1)$; the frame-free scalar branch violates no-slip, and its one named escape—a disformal matter coupling—converts the cancelled slip into an equal gravitational-wave/light speed difference, excluded by GW170817 by $\sim10^6$; and the preferred-frame branch carries an irreducible preferred-frame PPN parameter $\alpha_1$ whose MOND-generating piece is independent of every free kinetic parameter and can be cancelled only by a ghost. The same MOND-generating coupling kills the two scalar-gradient embeddings through $c_T\neq c$ and a radial gradient instability. Every *written* route through the nonlocal spin-2 door is also closed: the smoothly-vanishing spatial projector survives Dirac's algorithm with zero degrees of freedom on both sides of its rank bifurcation and is killed only by being an $\omega$-independent elliptic channel. Independently, we show the cluster mass residual cannot be supplied by any dark component—hot, cold, or mixed—within the framework's own galactic bounds. Finally we exhibit the one structural fork the framework leaves open: every system it fits is rotation-supported and every system it misses is pressure-supported, which is the signature that separates modified inertia from modified gravity. We construct the first test that distinguishes the two arms on rotating galaxies—the curl field of the modified-gravity disc solution—and find that its sign is contradicted by SPARC's deep discs at high significance while its amplitude is degenerate with the stellar mass-to-light ratio; the pressure-supported dwarfs and globular clusters lean the same way but pull in opposite directions from each other. The framework's one distinctive, undecided prediction remains that $a_0$ is constant in redshift where the emergent $\Lambda$CDM scale rises by $+0.33$ dex at $z\simeq2.5$. This paper claims no completion and no discovery; it claims a map.

---

## 1. The framework, and exactly what is and is not asserted

**The equation.** $a_0=\tfrac12 c\sqrt{G\rho_\Lambda}$. Equivalent forms: $a_0=c^2\sqrt{\Lambda/32\pi}$; $a_0=cH_0\sqrt{3\Omega_\Lambda/32\pi}\simeq0.144\,cH_0$. Numerically $9.36\times10^{-11}$ m s$^{-2}$ (Planck $H_0=67.4$, $\Omega_\Lambda=0.69$); the SPARC-fitted value is $1.2\times10^{-10}$. Both footings, $9.36\times10^{-11}$ (canonical) and $1.13\times10^{-10}$ (alternative), are carried through every calculation.

**What is forced.** Given one premise—$a_0$ is a universal *local* acceleration scale, so its inputs are $\{c,G,\rho\}$—Buckingham-$\Pi$ leaves exactly one dimensionless group: $a_0=\kappa c\sqrt{G\rho}$. The form and the exponent are not choices (`real_research/uniqueness_dimensional_proof.py`). Two things are not forced and are stated as such: the premise itself (Milgrom calls $\Lambda$-versus-$H_0$ "moot"; the premise is the content), and the coefficient $\kappa$, which is fitted: $\kappa=0.465\pm0.076$ (BTFR) and $0.551\pm0.043$ (distance-free), bracketing $\tfrac12$, with $\tfrac12$ versus $1/2\pi$ separated at $\sim4\sigma$ (`real_research/reviews/mi_kappa_error_budget_unlock_2026.py`). **$\kappa=\tfrac12$ is provably underivable from any homogeneous or quadratic sector of the theory**: $\ell_0=c^2/a_0$ cancels identically at quadratic order in the acceleration expansion, and $a_\mu=0$ on FLRW, so the first place a theory could fix $\kappa$ is cubic order (§8).

**The kernel.** $\nu(y)=[1-e^{-\sqrt y}]^{-1}$, the radial-acceleration-relation fit of McGaugh, Lelli & Schombert. Fitted, and stated as fitted.

**Where it works.** 147–175 SPARC rotating discs at 0.06 dex; the Milky Way rotation curve; the vertical force (`prep_2026`); Renzo's rule. A theorem of this repository (`hunt_2026/k_unexplained-regularities_closure.py`) shows that ten of twelve "unexplained galactic regularities" in the literature, including the baryonic Tully–Fisher relation, are reparametrisations of the radial acceleration relation to machine precision under a seeded derangement shuffle; only a two-radius statistic and a non-multiplicative statistic escape. The framework's galactic content is therefore one relation.

**Where it fails.** Every pressure-supported system (`hunt_2026/THE_LIABILITY_TABLE.md`): clusters need $\times2$–$3$ at $R_{500}$ and their cores are Newtonian at $g\approx20a_0$; groups, ellipticals, dwarf spheroidals, ultra-diffuse galaxies, globular clusters. The external-field slope is measured at $+0.080\pm0.047$ where modified gravity predicts $-0.093$, a sign disagreement at $3.7\sigma$ (`hunt_2026/f03_efe_slope_prediction.py`).

**The gates.** A relativistic completion must produce $\mu(y)=1-e^{-y}$ exactly in the quasi-static limit from one action, with $N_{\rm grav}=2$ tensor degrees of freedom plus at most one healthy scalar (all degrees of freedom explicit, counted, healthy); $\Phi=\Psi$ derived; full PPN with $\gamma=\beta=1$, $\alpha_{1,2,3}=0$ (Cassini $|\gamma-1|<2.3\times10^{-5}$; pulsar $|\alpha_3|<4\times10^{-20}$); $\nabla_\mu T^{\mu\nu}=0$ as a Noether identity; $c_T=c$ to $10^{-15}$; stability with no instantaneous channel; a dynamically accelerating FLRW background; a controlled $y\to0$ limit; $G_N$ derived; one metric (`FRIED_CHICKEN_SPEC.md`).

---

## 2. Assumptions of the no-go

- **A1** The matter coupling is metric, or metric plus a Bekenstein-form disformal term $B\,\partial_\mu\phi\,\partial_\nu\phi$.
- **A2** Locality: the action is a local functional of the fields (the nonlocal case is treated separately in §5).
- **A3** At most one propagating scalar beyond the two tensor polarisations, or a unit timelike vector.
- **A4** Lensing and dynamics agree in the MOND regime ($\gamma_{\rm PPN}=1$ from KiDS-1000: $21.2\sigma\to0.6\sigma$).
- **A5** GW170817: $|c_{\rm GW}/c_{\rm light}-1|<10^{-15}$ along the observed path.
- **A6** Pulsar bound $|\alpha_3|<4\times10^{-20}$; Cassini $|\gamma-1|<2.3\times10^{-5}$.
- **A7** An expanding background with $H\neq0$.

A2 is load-bearing. Everything in §3–§4 is unconditional within the local class and conditional on A2 overall.

---

## 3. The local no-go, by branch

A local theory can carry the MOND force in exactly three ways: through a constraint on the metric with no new propagating field; through a frame-free scalar; or through a field that defines a preferred frame. Each is closed.

### 3.1 The constraint branch: two degrees of freedom is instantaneous

If $N_{\rm grav}=2$, the MOND force is carried by a second-class constraint. A constraint has an $\omega$-independent $1/k^2$ propagator, i.e. it is instantaneous in the preferred foliation, and an instantaneous potential in a moving frame carries the preferred-frame parameter $\alpha_3=O(1)$. The furthest any strict two-degree-of-freedom MOND reached is the cuscuton-plus-Laplacian-constraint construction, which clears exact $\mu$, the deep-MOND cubic, the $a_0$ promotion $a_0^2=GV(\chi)/4$, no-slip, and the Dirac count, and dies at $\alpha_3=-1$ in the principal $(k,\omega)$ extraction, excluded by $\sim10^{19}$ (`cde_l4c_2026/cde_l4c_ppn_alpha3.py`). The mechanism is a pincer:
$$N_{\rm grav}=2\;\Longleftrightarrow\;\text{MOND via second-class constraint}\;\Longleftrightarrow\;\omega\text{-independent }1/k^2\;\Longleftrightarrow\;\alpha_3=O(1).$$
$\alpha_3=0$ requires a retarded propagating carrier, which is exactly the scalar that $N_{\rm grav}=2$ removes. Independent confirmations: the elliptic MOND potential becomes a physical instantaneous observable via the external-field effect (`theory_2026/york/YORK_CAUSAL_GATE_VERDICT.md`); DC-019.

### 3.2 The frame-free branch: slip, and the disformal escape

A single frame-free scalar $F(X)$, $X=-\tfrac12(\partial\phi)^2$, has anisotropic stress $\propto F_X\partial_i\phi\partial_j\phi$ that sources $\nabla^2(\Phi-\Psi)\neq0$ at $O(\Phi)$ in the MOND regime (the Bekenstein–Sanders result that forced TeVeS's vector; DC-013). The one escape is a disformal matter coupling, $\tilde g_{\mu\nu}=g_{\mu\nu}+B\,\partial_\mu\phi\,\partial_\nu\phi$, whose spatial correction shares the tensor structure $\partial_i\phi\partial_j\phi$ of the scalar stress and can therefore cancel the slip *pointwise* (`door_a_2026/doorA_disformal_slip_vs_cT.py`, check A1). It dies on one identity (check A2): the no-slip condition fixes $B\phi'^2=2(\Psi-\Phi)$, and that same quantity is the fractional difference between the null cone of $g$ (gravitational waves) and of $\tilde g$ (light):
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

The other two local ways to carry a preferred frame are killed by the *same* coupling: a curvature-coupled clock forces $\lambda_r=-a_0\,y\,e^{-y}\neq0$ in the tensor kinetic term, $c_T^2=1/(1-2\lambda)$ departs from 1 by $\sim2\times10^{-7}$ in every MOND zone, excluded $10^7$–$10^9\times$ (`one_shot_final/curvature_qumond_luminality_no_go_2026.py`, 6/6; `…observational_strengthening_2026.py`, 11/11); an acceleration-coupled khronon has $c_\parallel^2\propto f''<0$ on $a_0<a<38a_0$, an uncurable radial gradient instability (`fc_kh_terminal/`, and the $(yq)'$ theorem). Three embeddings, one mechanism.

### 3.4 Statement

**Theorem (local).** Under A1–A7, no action that is a local functional of a metric, at most one scalar, and at most one unit timelike vector reproduces $\mu(y)=1-e^{-y}$ in the quasi-static limit while satisfying no-slip, $c_T=c$, $\alpha_1=\alpha_2=\alpha_3=0$, and absence of ghosts, gradient instabilities and instantaneous channels. Each branch of the case analysis is closed by the committed calculation named above; the result is independent of the numerical footing of $a_0$, which enters only the background magnitude of $y$.

---

## 4. Clusters: no dark component can supply the residual

Suppose the cluster residual is a dark component. Structure caps a hot (free-streaming) fraction of the dark sector at $f_h\le0.0375$, through the standard $\Delta P/P\simeq-8f_h$ suppression against a Lyman-$\alpha$ forest measured to 10–20 per cent. The framework's own galaxies require $f_h\ge0.30$–$0.80$, because whatever is not hot is cold, and a cold component clusters into galaxies exactly as cold dark matter does—and the framework's galactic success *is* the statement that there is nothing cold in galaxies. All nine pairings of the most generous bound on each side fail; the tightest gap is a factor of eight (`hunt_2026/f07_two_component_nogo.py`, 6/6; single-species and free-streaming versions in `f04`–`f06`). The result is structural, so a third component does not help. The escape that a MOND cosmology regrows erased power is closed for this framework by its own bulk-flow null ($\beta=0.447$ against $\Lambda$CDM's $0.440$), which measured its linear regime Newtonian.

---

## 5. The nonlocal door: every written route closed

A2 is load-bearing, so the nonlocal spin-2 class is examined separately (`nonlocal_door/`). The state-space verdict of 2026-09-02 closes the positive-spectral causal completion (memory implies extra carrier states), the pole-free regular metric completion (no-slip forces the form factors equal; exact $\mu(0)=0$ removes the TT quadratic action), and the Ricci-polynomial elliptic projector. The corrected rank-change result withdrew "every regular metric-only projector is excluded" and left one loophole: a field-dependent spatial projector $H^{\mu\nu}=X(g^{\mu\nu}+u^\mu u^\nu)$ that is rank three away from zero field and vanishes smoothly at $X=0$, whose constraint structure changes rank.

`nonlocal_door/vanishing_projector_dirac_chain_2026.py` (11/11) runs Dirac's algorithm through that bifurcation. On the $u$-frame background $H^{00}=X(-1+1)=0$, so no time derivatives survive. For $X\neq0$: two primaries, two secondaries, $\det C=X^4k^8$, four second-class constraints, multipliers fixed, no tertiary, zero degrees of freedom, on-shell $\chi=-J/(Xk^2)$. For $X=0$: one secondary vanishes identically, the other degenerates to the constant $J$, the primaries become first class, zero degrees of freedom, and consistency demands $J\propto X$. **The bifurcation changes the class of the constraints, not the count.** The loophole is consistent and ghost-free—and it is killed by what it is: the surviving channel $\chi=-\tilde J/k^2$ has no $\omega$ anywhere, an instantaneous elliptic potential, which by the pincer of §3.1 carries $\alpha_3=O(1)$. It is a local elliptic constraint that switches itself off at zero field.

What remains for the nonlocal door is not a loophole but an unwritten construction: a genuinely retarded, $\omega$-dependent kernel that yields $\mu=1-e^{-y}$; §4 of the state-space verdict shows positive spectral weight costs extra carrier states. We do not say the door is closed; we say every route through it that has been written is.

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

- It does not present a relativistic completion, a field theory, or a theory of everything. Its central result is a **no-go**.
- It does not claim $\kappa=\tfrac12$ is derived. It is fitted, and §8 shows where a derivation would have to live.
- It does not claim the data favour the framework over $\Lambda$CDM. The one discriminating measurement (§7) has not been made.
- It does not claim the nonlocal door is closed, only that every written route through it is.
- It does not claim modified inertia is confirmed. It claims the modified-gravity curl field has the wrong sign on SPARC's deep discs, and that pressure-supported systems break the kernel in both directions.
- Every "fails" was verified as hard as every "works": the 2012 dwarf dispersions, the $+1.1$ curl amplitude, the $-0.98$ amplitude, and the $10\sigma$ virial offset of `f11` were each caught by a control and are recorded as such.

---

## 10. Reproducibility

All scripts exit 0 unless the listed checks are designed to fail; each has numbered checks, a mutation control, and both $a_0$ footings.

| claim | script | checks |
|---|---|---|
| form and exponent forced | `real_research/uniqueness_dimensional_proof.py` | — |
| $\kappa$ measured | `real_research/reviews/mi_kappa_error_budget_unlock_2026.py` | — |
| constraint branch: $\alpha_3=O(1)$ | `cde_l4c_2026/cde_l4c_ppn_alpha3.py` | — |
| disformal escape: slip $\to$ $c_T$ | `door_a_2026/doorA_disformal_slip_vs_cT.py` | 9/9 |
| $\alpha_1$ structural lock | `door_a_2026/doorA_alpha1_generality_theorem.py` | 12/12 |
| curvature-clock $c_T$ | `one_shot_final/curvature_qumond_luminality_no_go_2026.py` | 6/6 |
| khronon gradient instability | `fc_kh_terminal/` | — |
| vanishing projector Dirac chain | `nonlocal_door/vanishing_projector_dirac_chain_2026.py` | 11/11 |
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
