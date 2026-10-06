# Second-order zero-mode discriminator for the projected scalar

The positive reduced canonical energy does **not** give a positive dust background in the controlled calculation below. For a single real Fourier mode on a torus, variation of the unreduced common lapse and common scale gives an effective mean Einstein source proportional to a^(−2), with p=−ρ/3 and negative coefficient. The summed interaction stress alone has anisotropic pressure and is not separately conserved at this order. Neither quantity is the reduced Hamiltonian divided by a³.

This is an exact relative-order-two discriminant in a declared averaging chart, not a completed nonlinear periodic solution or an invariant no-go against every cold background. In particular a single plane wave requires homogeneous shear response; the lapse and trace rows do not replace the remaining second-order equations.

## Inherited action and controlled averaging

Use the actual projected-acceleration two-metric action, K>0, M=2K in each Einstein sector, signature −+++, n=3, coincident empty de Sitter with H>0, Λ=3H². Its geometric-mean volume is v and its interaction near coincidence is −4KΛv+K v H^{ij}∂i r∂j r+O(|∂r|³), r=ln(N_g/N_hat), H^{ij}=(γ^{ij}+hatγ^{ij})/2. The cubic term cannot enter the common metric variation at relative order two. The inherited finite-k result is zddot+Hzdot=0 and signed linear density δρ_g=−MPν, ν=zdot/H, P=k²/a². All source files and exact hashes are in provenance.json.

Fix the common clock θ=t, average over a fixed periodic coordinate cell, and use a symmetric exponential plane chart:

N_g=N exp(ε ν cos(kx)/2), N_hat=N exp(−ε ν cos(kx)/2),
u_g=ln a+ε(Z+E)cos(kx)/2, v_g=ln a+εZ cos(kx)/2,
u_hat=ln a−ε(Z+E)cos(kx)/2, v_hat=ln a−εZ cos(kx)/2,
γ=diag(exp(2u),exp(2v),exp(2v)),
N_g^x=−ε kβ sin(kx)/(2a²), N_hat^x=+ε kβ sin(kx)/(2a²).

Here u is a spatial scale variable, distinct from the lapse perturbation ν. The common shift is zero for this homogeneous-row probe. The ε² coefficient, not ε²/2 times that coefficient, is our normalization. The real-mode average is ⟨cos²⟩=⟨sin²⟩=1/2. These conventions matter when comparing to a complex Fourier normalization.

The background a,N are varied **before** eliminating the relative lapse, shear or shift. No common-background equation has been substituted in that variation. Only afterwards set N=1, h=d ln(a)/dt=H, and impose the inherited on-shell linear mode.

## Raw ADM expansion and mean Einstein rows

For one plane metric the exact intrinsic curvature and directional extrinsic curvatures are

R_3=exp(−2u)[−4v_xx+4u_x v_x−6v_x²],
κ_x=(udot−s u_x−s_x)/N_g, κ_y=(vdot−s v_x)/N_g,
Kij Kij−Ktrace²=−4κ_xκ_y−2κ_y².

The standard Einstein ADM action K N_g exp(u+2v)(R_3−4κ_xκ_y−2κ_y²), summed over metrics, and the actual interaction give the following exact averaged ε² coefficient:

L_2=−Ka³ C/N+KNa k² Q,
C=A_x Zdot+Zdot²/2+hX(A_x+2Zdot)+(3/4)h²X²−hPβ T,
A_x=Zdot+Edot+Pβ, T=3Z+E, X=T−ν,
Q=(Z+ν)²/2.

The constant geometric-mean interaction has no relative term in this symmetric exponential chart. It has not been discarded: it supplies the common vacuum background, whereas the two Einstein pieces retain its on-shell volume/curvature effects. As a check ∂C/∂β=P(Zdot−hν), precisely the parent shift constraint.

Moving the relative-order-two contributions to the common background Einstein RHS defines the coordinate-average source

ρ_eff=−(∂L_2/∂N)/a³=−K(C+PQ),
p_eff=[∂L_2/∂ln a−d(∂L_2/∂h)/dt]/(3a³).

This is the total effective zero-mode source of the two Einstein perturbation terms **and** the interaction. It is not the interaction tensor alone. The background tensor coefficient in this common equation is 2M=4K. A common homogeneous lapse perturbation changes the L_0 equation with this same normalization.

The inherited finite-k constraints are ν=Zdot/H, E=−3Z−ν, β=−Edot/P−(Z+ν)/H. Let Z=Z0+Z1/a, ν=−Z1/a. Substitution after variation gives

ρ_eff=−K[H²ν²+P Z0²]/2
       =−K(H²Z1²+k²Z0²)/(2a²),
p_eff=+K(H²Z1²+k²Z0²)/(6a²)=−ρ_eff/3.

The trace/lapse source obeys ρ_eff_dot+3H(ρ_eff+p_eff)=0. The raw relative kinetic term on the parent constraints becomes −(KH/2)d(a³ν²)/dt, so the first-order reduced action is recovered with its required boundary. Varying that reduced boundary-subtracted action instead of the raw common lapse would give a different gravitational source.

For the actual gravitating decaying mode, Z0=0 and Z1≠0, this defined source is still negative and a^(−2), with nonzero pressure. It supplies neither the sign nor dilution law of positive conserved cold matter. For Z1=0 it also contains a frozen-mode contribution although the first-order Bardeen Weyl potential vanishes. That observation diagnoses the background/coordinate split: it is not a new invariant energy assigned to every frozen foliation configuration.

## Actual summed interaction stress

There is a separate, directly varied tensor result. On the first-order volume constraint D=ν+3Z+E=0, the two proper vacuum ratios are reciprocal. Their summed extra vacuum density has no ε² term: any second-order relative volume perturbation enters each vacuum with opposite signs and cancels in the sum. The derivative part of the two gradient-lapse Euler equations also cancels in that sum at this order.

Varying the gradient term with common independent spatial lengths a_x,a_y,a_z, before setting all equal, gives

L_I,2=K N (a_y a_z/a_x) k²ν²/2.

Consequently, in the common-clock normal frame,

ρ_I,sum=−K Pν²/2,
p_I,parallel=ρ_I,sum, p_I,transverse=−ρ_I,sum,
p_I,trace=−ρ_I,sum/3.

This is nonzero homogeneous anisotropic stress from a single plane wave. The summed density scales as a^(−4), but its mean energy residual is ρdot+3H(ρ+p)=−2Hρ, not zero. A fluid name or physical equation of state cannot be inferred by that scaling alone. At this order the full covariant system includes perturbed connections acting on the first-order, opposite stresses, the Einstein nonlinearities, and the sourced metric/clock equations. One cannot apply an isolated homogeneous-fluid continuity equation to just this interaction contribution.

The common metric must allow homogeneous Bianchi-I shear if these directional sources are retained. Ordinary common-coordinate scalar gauge fixing cannot remove the physical relative shear. We have computed the source of the lapse and isotropic trace rows, not solved all directional rows or the second-order clock/relative constraints.

## What the discriminator establishes and leaves open

A periodic zero-mean first-order density can have nonzero second-order averages. Positivity of its reduced temporal Hamiltonian nevertheless does not imply positive gravitational dust abundance: the raw lapse source demonstrably differs. Its real-mode canonical H/a³=K Pν²/2 is positive and a^(−4); the varied total source above is negative and a^(−2). No physical radiation backreaction is asserted from the former either.

Averaging prescription and observable mean matter: in this chart each proper spatial volume has fractional correction ν²/16 after averaging. Defining a background by proper-volume expansion instead changes the second-order split. Neither the frozen-coordinate source nor ρ_eff alone is a gauge-independent backreaction observable. A completed second-order solution must specify a geometric mean expansion/curvature observable, solve the mean lapse, anisotropic Einstein and clock rows and the relative corrections, and fix homogeneous integration data. It must then demonstrate a positive, conserved, pressureless component in that observable rather than importing the canonical energy. That is the exact missing arrow.

The present necessary-source calculation therefore does not close Claude's cold-assembly or actual growth deficit. It rules out the shortest proposed inference within this explicit chart, while preserving the action as a conditional route requiring a fuller calculation. No abundance, primordial spectrum, recombination transport, nonlinear health or 32π selection has been derived.

## Reproducible evidence

checks.py differentiates the two raw plane ADM contributions in ε and reconstructs the real-mode average independently of the displayed reduced formula. It checks the mean lapse/scale variations, boundary identity, source dilution and varied directional interaction pressures. Twenty exact identities pass. Controls replace the raw lapse source with canonical H/a³, omit the Einstein contribution, or declare dust pressure. These are candidate changes, not overwritten success flags. Standard run provenance and current manifest validation are recorded in RUNS.md; no numerical cosmology is run.
