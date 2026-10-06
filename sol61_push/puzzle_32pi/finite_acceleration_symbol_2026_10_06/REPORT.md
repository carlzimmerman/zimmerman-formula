# Finite-acceleration ADM symbol: a constrained planar negative-kinetic direction

The decisive result is restricted but stronger than the previous lapse-Hessian test. In a spatially flat planar initial slice, with an isotropic expansion jet and a nonzero acceleration along the wavevector, the longitudinal shift remains an exact multiplier. After both lapse and shift constraints, the physical scalar has leading kinetic coefficient

\[
 {K_E Q_{aa}\over2N_0 [h-b/(2K_E)]^2}\,k^2.
\]

Thus `Qaa<0` produces a physical high-frequency negative-kinetic direction in this sector, provided `D=h-b/(2KE) != 0`. Constraint-compatible initial-data jets with these properties exist locally. Full on-shell time evolution from these jets has **not** been established here; this is a constrained principal-symbol result, conditional on a solution having the stated jets. It neither forces every galaxy clock onto this branch nor establishes a Hadamard instability. Low-acceleration flowing clocks remain a distinct escape.

## Action and conventions

In four spacetime dimensions, signature `-+++`, natural units, use the unitary clock `phi=qt`, `q>0`, and the exact ADM action, up to the same boundary term as the prior log-braiding derivation,

\[
S=\int dt\,d^3x\,N\sqrt\gamma\left\{ {K_E\over2}
[{}^{(3)}R+K_{ij}K^{ij}-\theta^2]+2c\ln N-V_{\rm eff}
-b\theta\ln N+K_E Q(a)\right\},
\]

`Kij=(dot gammaij−Di Nj−Dj Ni)/(2N)`, `theta=Kii`, `ai=Di lnN`, `a²=gammaij ai aj`, `b=2c/(3H*)`, `KE>0`. The response is fixed-A, `Q=(1−epsilon)a²−2W(a;A)`. Set epsilon zero for the exact critical response. `KE` has mass², `c,Veff` mass⁴, `b` mass³, and `h,a,k` mass; `Q` has mass². Compactly supported perturbations discard spatial boundaries. Matter is absent in the symbol and background-constraint construction; a matter shift Hessian cannot be silently omitted if matter is added.

The covariant ancestor is `K(X)=−c ln(X/Xref)`, `G(X)=−sqrt(2)c/(3H*) X^(-1/2)`, with `X>0`. Prior authenticated local primary sources are Bernardo arXiv:2101.00965v2 and Kobayashi et al. arXiv:1105.5723v2; the latter's Eqs.55–64 give the ordinary homogeneous lapse/shift reduction. Here the nonzero-acceleration calculation is reconstructed from the action above, rather than importing that homogeneous reduction. Exact unitary boundary/source derivation is pinned in `cuscuton/log_braiding_extension/REPORT.md` by the run manifest.

## Background jets and the constraint obstruction to naive freezing

At one initial slice take `gammaij=deltaij`, `Ni=0`, `Kij=h(x)deltaij`, and `N=N0(x)>0`. At the point of interest `a=N0'/N0 !=0`. Flat spatial geometry and planar lapse imply `Ricij=0`, `Da` has only its xx component. The expansion need not be spatially constant. The vacuum momentum constraint is

\[
 K_E D_j(K^j{}_i-\delta^j_i\theta)-b a_i=0,
 \qquad 2K_E h'+b a=0.
\]

A constant-h finite-a jet would violate this equation. The calculation below keeps its required gradient. The initial expansion jet is isotropic; isotropic acceleration/evolution jets at later times are not assumed. A conformally flat spatial gauge can be imposed at this slice in the planar scalar sector. This does not assert that the entire background evolution is globally conformally flat with vanishing shift.

## Exact planar shift variation and both auxiliary constraints

Use spatial gauge `gammaij=e^(2 zeta)deltaij`, and planar shift `Nx=v`. At the chosen slice write `L=N0 h+dot zeta`, `t=(L−v zeta')/N`, and `d=v'/N`. The three eigenvalues of K are `(t−d,t,t)`, so the exact kinetic and braid densities are

\[
 {K_Ee^{3\zeta}\over N}[-3(L-v\zeta')^2+2(L-v\zeta')v'],
 \quad -b e^{3\zeta}[3(L-v\zeta')-v']\ln N.
\]

In particular there is no `(v')²` term. At `v=0` their shift Euler derivative is exactly

\[
 E_v=-e^{3\zeta}\partial_x[2K_E L/N+b\ln N].
\]

For `N=N0 exp(nu)`, linearizing about `zeta=0` gives

\[
\partial_x\left[{\dot\zeta\over N_0}-D\nu\right]=0,
\qquad D=h-{b\over2K_E}.
\]

For nonzero local wavevector, remove the spatially homogeneous integration mode. The momentum constraint therefore gives `nu=dot zeta/(N0 D)`. It does not constrain zeta to zero. The lapse equation has a nonzero longitudinal-shift coefficient `2KE D k² beta`, with `v=beta'`, and solves for beta when `D !=0` and `k !=0`. It supplies no second independent condition eliminating zeta. The clock equation is the diffeomorphism Noether consequence of the metric equations for a nonzero timelike clock gradient; it cannot be counted again as a constraint.

The response contributes `KE N0 Qaa (nu')²/2`. Substitution yields the kinetic coefficient stated above. Terms from the spatial curvature and response metric variation supply spatial/first-time-derivative terms, but no additional `k² dot zeta²` in this planar sector. The ordinary EH/KGB scalar kinetic is order `k^0`. It cannot change a strictly negative leading coefficient at sufficiently large k.

Rotations in the transverse yz plane separate the scalar, vector and tensor sectors: tensor perturbations are `(delta gammayy−delta gammazz,delta gammayz)` and do not mix with this scalar; vector metric perturbations are removable by spatial gauge and their shifts are ordinary elliptic auxiliaries. Hence the negative coefficient is a physical scalar kinetic direction after constraints, not an unphysical lapse or shift eigenvalue. The tensors retain the positive EH principal kinetic. This comparison fixes the energy sign convention.

For a local WKB interpretation require wavelength shorter than the background derivative scales and `k² |Qaa|/D² >> 1` (with the finite lower coefficients also included). A proposed EFT cutoff or higher-derivative repair must specify the actual new terms and whether the physical momenta reach this regime. The present two-derivative action supplies none. A negative kinetic coefficient is a ghost criterion for this constrained symbol; dispersion, Hadamard ill-posedness, and growth rates are separate claims not derived here.

## Constraint-compatible initial jets, not a proved solution theorem

The planar vacuum lapse equation is

\[
3K_Eh^2+2c\ln N_0-V_{\rm eff}+2c-3bh
+K_E[Q-aQ_a-Q_{aa}a']=0.
\]

Together with momentum it is a local first-order system

\[
N_0'=N_0a,\qquad h'=-{b\over2K_E}a,\qquad
 a'={3h^2+(2c/K_E)\ln N_0-V_{\rm eff}/K_E+2c/K_E
 -3bh/K_E+Q-aQ_a\over Q_{aa}}.
\]

For a smooth constitutive Q with `Qaa !=0`, positive N0 and arbitrary finite initial `(N0,h,a)` with `D !=0`, standard local ODE existence supplies a constraint-compatible planar initial slice. This is a genuine construction of the two ADM constraint equations, including spatial derivatives, rather than a frozen off-shell coefficient choice. The spatial evolution equations, preservation/solution of the full lapse constraint in time, boundary conditions, and local on-shell time evolution have not been proved. The strongest unconditional result here is the constraint-compatible initial-data construction plus its constrained kinetic symbol. At `Qaa=0` this ODE construction and the leading kinetic test both require a separate compatibility/rank analysis.

## Why the general non-aligned symbol cannot use the same multiplier blindly

For a general isotropic-K jet the exact pure-shift quadratic action is

\[
{K_E\over8}\int\sqrt\gamma\,f[(D_i n_j+D_j n_i)^2-4(D_i n^i)^2],\quad f=1/N_0.
\]

For `ni=Di beta`, integration by parts gives

\[
\int f[(D_iD_j\beta)^2-(\Delta\beta)^2]
=\int[(\Delta f)\gamma^{ij}-D^iD^jf-fR^{ij}]D_i\beta D_j\beta.
\]

Its coefficient at direction `l=k/|k|` is `Sdirect=a_perp²−tr(Da)+Da_ll−Ric_ll`. Leading mixing with the transverse shift gives `nT=−2 aT beta`; eliminating it subtracts `2 a_perp²`. Thus the longitudinal shift block has `S=−a_perp²−tr(Da)+Da_ll−Ric_ll`. In a flat constant-a coefficient jet, `Sparallel=0` but `Sperp=−a²`. The latter example is a coefficient check; constant h at finite a is not a vacuum solution.

The resulting enhanced scalar auxiliary block, when the remaining principal metric reduction is nonsingular, is

\[
{\mathcal L\over K_E k^2}=C\nu^2-2\beta(\dot\zeta/N_0-D\nu)+{S\over2}\beta^2,
\quad C={1\over2}[Q_{aa}(l\cdot\hat a)^2+(Q_a/a)(1-(l\cdot\hat a)^2)].
\]

Its algebraic Schur coefficient is `C/[D²−SC/2]` for `(dot zeta/N0)²`. This generic block is a useful conditional leading template, **not** a proved every-jet full physical symbol in this report. Tensor/subleading mixing and all rank-degenerate cases must still be audited for a specified nonplanar solution. In particular, for `C<0`, sufficiently negative S can change the sign through the auxiliary denominator. At `D²−SC/2=0` the elimination is singular. A negative longitudinal lapse Hessian by itself therefore does not prove a ghost on every finite-acceleration background. The exact planar result avoids these generic ambiguities by having S identically zero and sector symmetry.

## Cutoff and epsilon consequences

For the monotone inverse source dictionary `a=A[y+h(y)]`, `Wa=Ay`,

\[
C_L={Q_{aa}\over2}=(1-\epsilon)-{1\over1+h'},\qquad
C_T={Q_a\over2a}=(1-\epsilon)-{y\over y+h}.
\]

At epsilon0 a positive excess h which ultimately decreases has `CL<0` wherever `h'<0`. For the pinned cutoff `h=[sqrt(1+1/y)+1]^-1/[1+(y/T)²]`, T128.9153707043, the finite point y100 gives `a/A=100.311388927`, `CL=−0.002337307245`, while `CT=0.003104223065>0`. The previously demonstrated inverse-chart regularity and stationary radial rank loss are distinct from the present planar constrained kinetic result.

For **uncut** P2, `Waa=2a/sqrt(A²+4a²)`. Epsilon detuning needed by the separate regular-core repair changes the longitudinal coefficient to

\[
 C_L=1-\epsilon-{2a\over\sqrt{A^2+4a^2}}.
\]

Every `0<epsilon<1` has a negative high-clock region beginning at

\[
{a\over A}>{1-\epsilon\over2\sqrt{\epsilon(2-\epsilon)}}.
\]

For epsilon.01 the threshold is3.508961965. Thus epsilon repairs a low-acceleration center at the cost of a high-acceleration negative planar kinetic region in this unchanged two-derivative action. This is not a claim that physical solar/galactic acceleration equals the clock acceleration: the freefall-clock route can have a tiny clock acceleration and a large Killing-metric force. No target A/H or32pi coefficient is selected.

## Evidence, controls and remaining implication

`checks.py` reconstructs the three extrinsic-curvature eigenvalues, exact shift Euler derivative, vanishing pure shift-square term, linear momentum constraint, Hamiltonian jet ODE and the auxiliary Schur factor. It also checks the weighted transverse completion in the flat exponential-lapse example and declared finite cutoff/epsilon signs. `runs/main_a` passes23 assertions. `control_shift_a` drops the braiding contribution in the momentum solution and fails; `control_kinetic_a` reverses the reduced kinetic sign and fails. Their failed manifests are valid negative-control provenance. The runner pins the script and two actual prior input reports; this report is not a computational input, so prose clarification does not stale those manifests. Actual Git/head/input hashes are in each manifest; `provenance.json` pins this report and script after finalization.

The exact next implication is to construct a full on-shell background with these planar jets, or derive the finite-jet constrained kinetic matrix on an actual sourced flowing clock. This report refutes the shortcut that all omitted constraints necessarily rescue negative response curvature; it does not prove that every acceptable sourced branch encounters it. Separately, a proposed healthy cutoff/epsilon completion must explain how it avoids the explicitly constrained negative-clock sector or changes the action before its relevant momenta, while retaining the source bridge.

## Domain-restricted turnoff obstruction

Suppose the action above is required to have a nonnegative physical high-k kinetic coefficient on **every** smooth constraint-compatible planar initial-data jet in a declared allowed interval of clock acceleration, with `D !=0`, and suppose such jets are admitted as backgrounds for the local dynamical theory. The exact planar reduction requires `Qaa>=0` throughout that interval. The last proviso matters: the full on-shell time-evolution existence step was not proved here, and a theory could restrict the permitted background domain or introduce new operators.

For the source inverse `a=s+delta(s)`, assume `delta` is C1, positive at some finite s, tends to zero as s tends to infinity, and `1+delta'(s)>0`. There must be a point with `delta'<0`: otherwise the excess would be nondecreasing and could not return to zero. Since `Wa=s`, the exact critical response gives

\[
Q_{aa}=2\left(1-{1\over1+\delta'}\right)
={2\delta'\over1+\delta'}<0
\]

at such a point. That point lies in the constraint-compatible planar negative-kinetic sector derived above. Consequently, this unchanged single-clock two-derivative action cannot meet the stated **all-admitted-planar-jets** health requirement over the complete turnoff range. This is a necessary-condition obstruction in this action class, not a no-go for every MOND theory, not a proof that a particular galaxy crosses the range, and not a transplantation of the BIMOND vacuum integral into KGB. Restricting clock gradients to a low-acceleration branch or adding a specified dynamical completion changes the premise and remains open.

The epsilon detuning gives `Qepsilon,aa=2[delta'/(1+delta')−epsilon]`; the uncut P2 excess approaches a constant rather than zero, but its derivative tends to zero, so every positive epsilon still violates the same all-gradient requirement at sufficiently large clock acceleration. This provides the exact high-clock cost of that particular regular-core repair.
