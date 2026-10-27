# Nonlinear saturation: what changes and what does not

Use the predecessor's dimensionless units and the passive reciprocal action. This calculation keeps the exact polarization potential W(p)=-p-ln(1-p), 0≤p<1. It is not a new saturation term added to the theory: this is the same W already used in the earlier fitted static cores.

## Exact nonlinear dual

For fixed χ=1, the matter/field energy is

 E=Ugrav+(1/4π)∫[|ρ-div P|²/2+W(|P|)] d³x.

The Legendre conjugate of W is W*(s)=s-ln(1+s), because s=W'(p)=p/(1-p) and p=s/(1+s). Introducing h=ρ-div P and minimizing P gives

 P=-grad h/(1+|grad h|),
 ρ=h-div[grad h/(1+|grad h|)].

The positive field energy is minus the minimum of the convex functional

 F[h]=(1/4π)∫[h²/2+|grad h|-ln(1+|grad h|)-ρh].

The quadratic control replaces W* by |grad h|²/2 and recovers h(K)=ρ(K)/(1+K²). Strict convexity from h² makes the finite-grid minimizer unique. Forward differences and their negative adjoints are used consistently; a small solver residual does not establish continuum accuracy.

Mass rescaling no longer works: P(Mh) is not M P(h). For a smooth small-amplitude source ρ=M f, h=M h1+O(M²), and

 E(M)=M² E2 + M³/(12π)∫|grad h1|³ + O(M⁴).

The positive cubic correction increases the energetic cost of concentrating a fixed profile. The stationary h correction first contributes at fourth order because h1 extremizes the quadratic dual. This explains a scaling defect, not a preferred mass across profiles.

## Phase relaxation without inventing damping

Let χ=1+z and A=a-d∇², with positive a,d and periodic or decaying boundary conditions. The phase energy is (1/2)<z,Az> and its passive source gives

 Az=h²/2,  χ=1+(1/2)A^-1(h²).

Eliminating the quasistatic phase adds to F the nonlocal positive term

 (1/8)<h²,A^-1(h²)>.

Its functional derivative is h A^-1(h²)/2, so the nonlinear equation becomes

 ρ=χ h-div[grad h/(1+|grad h|)].

The phase probe uses a=1/(2λ), d=a/(0.2)², λ=1,100, matching the previous passive parameter convention. It is an adiabatically relaxed phase, not finite-inertia evolution, radiation or cooling. Its boundary extent must be resolved independently of the compact source. Because the source for z is quadratic, the homogeneous unpumped linear response remains unchanged.

## A nonlinear sheet capacity is not a selected mass

For an isolated razor-thin planar source Σδ(z), symmetry and h+P'=ρ give P(0+)=Σ/2. In vacuum z>0, P'=-h and h'=-P/(1-P). Therefore

 h²/2=W(P),
 h(0+)=[2W(Σ/2)]^(1/2).

The regular finite-central-field sheet branch requires Σ<2 in the declared units. The limiting value corresponds to about 106.9 solar masses/pc², about95 times the input surface density previously chosen to match the canonical footprint mass. This is a limit of the razor-thin static-field source problem, not a universal threshold for finite-thickness clouds. At the canonical footprint input P(0+)=0.01053: this sheet is weakly nonlinear. Changing the transverse area changes total mass without changing this local surface-density relation. Thus capacity alone supplies no absolute mass.

## The passive energy obstruction is not spherical

The earlier core_formation_transport derivation assumes an isolated, static, finite-mass, passive X=0 solution with decaying fields, χ→χ0 and well-defined surface terms. Its variations ρ(x)→t³ρ(tx), P(x)→t²P(tx), χ(x)→χ(tx) are valid for arbitrary shapes. No spherical step is needed.

With U gravitational energy, V mismatch energy, Z phase potential energy, J phase-gradient energy, T optional polarization-gradient energy, B=∫W, D=∫p W'(p), and H=χ0∫h², its identities are

 U+3V-3Z-J+3T+2D-3B=0,
 μM=2U+2V+D+2T,
 V=2J+2Z+H/2.

Subtracting E=U+V+Z+J+T+B yields

 μM-E=-4J-2Z-H-2T+2B-D<0,
 d(E/M)/dM=(μM-E)/M²<0.

The sign follows from d[2W-pW']/dp=-p²/(1-p)² and nonnegative remaining energies. This applies along a differentiable stationary branch at fixed couplings; it does not prove all masses admit solutions. It excludes a preferred interior mass from minimizing energy per mass on that branch, including nonradial stationary configurations. A branch endpoint, external confinement, driven fields, rotation and dynamical fragmentation/ejection require their own analysis. The result neither excludes dynamical mass selection nor proves actual mergers occur.

## What the affine collapse can test

A Gaussian cloud with three evolving widths ai and velocities adot_i has the imposed reduced kinetic energy M sum(adot_i²)/2. A rotational coordinate about the third axis has I=M(a1²+a2²); fixed L gives C=L²/(2I). The reduced evolution uses

 M addot_i=-∂[Efield+Ugrav+C]/∂ai.

Each step solves the exact nonlinear quasistatic polarization problem. Analytic isolated Gaussian gravity removes the large periodic Newtonian image offset. The Gaussian field source is normalized in the finite periodic box; this truncation and finite-difference orientation errors still require refinement. The kinetic closure represents an infinite Gaussian affine ansatz approximately when its tails fit inside the box. Rotational energy is treated with the continuum orientation symmetry; the grid introduces errors.

This ansatz permits unequal-axis contraction and rebound. It has no independent fragments, no internal angular-momentum exchange between pieces, no ejection and no radiative degrees of freedom. Conservation of M and fixed L is imposed, not evidence of universal remnant selection. Its outcome is only a discriminator for saturation opposing contraction, never a mass-function prediction.
