# Microscopic condensate matching: MOND construction versus joint selection

The requested joint selector remains open. This continuation obtains an actual MOND-force operator from a specified higher-energy effective parent, checks its finite-regulator branch, and identifies the dimensionless matching ratio a successful microscopic theory must compute. Ordinary analytic Rabi mixing does not supply a vacuum source in the stated nonrelativistic regime; the normalized phase interaction used for dark energy has an independently supplied amplitude. No eta, vacuum scale or numerical a0 has been predicted.

Base adb56b9dc14fbb4559de50809cfcaf07108ee52c; freezes fba75ecd27 and 54785632d6. Dark-energy footing. Kappa=1/2 is FITTED; CFG493 kappa_Lambda=0.417 +/- 0.095 and kappa_crit=0.345 +/- 0.078 are separate, not inputs. Natural c=hbar=1 throughout; epsilon denotes energy density (rho_DE in these units).

## 1. A microscopic Rabi interaction does not automatically act as vacuum energy

Consider canonical complex fields with the quadratic potential

U = a |Psi1|^2 + c |Psi2|^2 - k(Psi1* Psi2 + Psi2* Psi1),

where a,c>0 and ac>k^2. A constant unitary rotation diagonalizes the mass matrix. Its eigenvalues are

m_plus/minus^2 = [a+c +/- sqrt((a-c)^2+4k^2)]/2.

Thus this mixing changes particle masses; it does not generate an independent classical positive vacuum constant at the zero-field minimum. The vacuum energy from quantum corrections still requires a renormalization prescription and gravitational matching, not provided by this diagonalization.

In the slowly varying nonrelativistic condensate description, the corresponding mixing contribution has the form

U_R=-2 Omega sqrt(n1 n2) cos(delta),

with number densities n_i>0 and relative phase delta. For a local energy contribution U(n1,n2,delta), its adiabatic isotropic pressure at fixed particle numbers and phase is

p_U = n1 U_n1+n2 U_n2-U.

U_R is homogeneous of degree one in the densities, so p_R=0. For fixed fractions and phase, n_i proportional to scale_factor^(-3) implies U_R proportional to scale_factor^(-3). Relative conversion can change those fractions, but the Euler homogeneity pressure identity holds at each state. Repulsive density-quadratic and density-cubic interactions instead give p_2=U_2 and p_3=2U_3. These statements assume the nonrelativistic, weak-gradient, positive-mass branch; they do not rule out relativistic, metastable or other interacting condensates.

Compare a density-independent phase potential U_phase=J[1-cos(delta)]. It gives p_phase=-U_phase. The difference is physical: removing the density factors is what changes the homogeneous stress. It cannot be done without changing the microscopic interaction.

The checked unified-superfluid source uses such an amplitude-divided interaction, supplies its potential scale, and allows a vacuum offset. It therefore does not furnish the missing joint selector. This source result and the separate two-field force construction are distinct models: joining their actions is not proof of a healthy combined state. See SOURCES.md for precise locators.

## 2. A constructive MOND parent, with its assumptions retained

Use the higher-energy effective parent in arXiv:2009.03003v3 Appendix B, in its +--- convention. Let Y=K_plus+K_minus-m^2<0, u=rho_plus^2>0, a=Lambda_c^2>0. Neglect amplitude gradients only for the following stationary matching:

L(u,Y)=uY/2 + Lambda^4 u^3 Y^3/[6(a+u)^6].              (1)

This is a prescribed nonlinear derivative action; it is not an established microscopic UV completion. Nevertheless, it provides a concrete amplitude-elimination calculation rather than only assuming the final cubic.

For u>>a, the amplitude equation gives u=Lambda sqrt(|Y|), and substitution yields

L_eff=(2Lambda/3) Y sqrt(|Y|).                          (2)

In the gradient-dominated force regime, Y approximately equals -|grad theta_plus|^2, so this becomes -(2Lambda/3)|grad theta_plus|^3. The second field supports the density and can cure the particular one-field ghost under the source's stability conditions; we do not import a universal single-field instability. Neither that conditional stability nor (2) proves UV consistency, lensing viability or a combined cosmological solution.

Keeping a finite, the exact stationary equation from (1) is

Lambda^4 Y^2 = (a+u)^7/[u^2(u-a)],  u>a.               (3)

With x=u/a, define F(x)=(1+x)^7/[x^2(x-1)], x>1. Its logarithmic derivative is

F'/F=(4x^2-8x+2)/[x(x-1)(x+1)].

F diverges at both ends of this domain and has a unique minimum at x_star=1+1/sqrt(2). There is therefore an amplitude-branch threshold

|Y| >= (a^2/Lambda^2) sqrt(F(x_star)).                 (4)

The equality is not a controlled EFT matching point: the amplitude curvature vanishes there. On a stationary solution,

L_uu=Y(2u^2-4au+a^2)/[u(u-a)(u+a)].

For Y<0, the large-u branch u>a x_star has L_uu<0, the sign appropriate to positive restoring curvature of the amplitude energy. The coefficient of K_rho in the parent at that stationary point is u/(u-a)>0. These are amplitude diagnostics, not the full coupled characteristic matrix. The near-a branch has the opposite amplitude curvature. At the threshold the gap closes, and derivatives of the amplitude cannot simply be discarded.

The resulting minimum force in the gradient-dominated approximation is

g_min = q (Lambda_c^2/Lambda) F(x_star)^(1/4).

This is a cutoff/branch-existence condition, not the normalization of the MOND law. It retains Lambda_c, and (2) needs a stronger large-u separation than merely satisfying (4). No pure number from this minimum is identified with kappa.

## 3. Derive a0 from the actual source equation

For any conditional static action

L_static=-C |grad theta|^3/3 - q rho_b theta, C,q>0,

the field equation is div(C |grad theta| grad theta)=q rho_b. For a regular source in n spatial dimensions, the exterior flux is

S_(n-1) r^(n-1) C theta'^2 = q m_b.

In three dimensions, baryons feel g_phi=q theta', hence

g_phi^2 = [q^3/(4pi G C)] g_N,
a0 = q^3/(4pi G C).                                   (5)

This is an actual MOND radial force law wherever the cubic EFT and its source coupling are valid. Total gravity may also include the Newtonian force from baryons and the condensate. The result is not a claim about all radii or the full relativistic theory.

For (2), C=2Lambda. With the source convention q=alpha Lambda/Mpl and G=1/(8pi Mpl^2), equation (5) becomes a0=alpha^3 Lambda^2/Mpl. That relation does not determine alpha or Lambda.

The field normalization cannot eliminate the physical freedom: theta_new=z theta gives C_new=C/z^3 and q_new=q/z. The combination q^3/C is invariant. Doubling a physical q at fixed C changes a0 by a factor of eight, while changing field units does nothing. This separates a genuine parameter from notation.

## 4. What a successful common-scale mechanism would have to compute

Grant, as a new conditional microscopic hypothesis, a single dynamically generated scale Lambda with

C=c3 Lambda,  q=cb Lambda/Mpl,  epsilon_DE=c0 Lambda^4,

where c0,c3,cb are dimensionless and positive. This hypothesis is not derived by the cited models. Equation (5) gives the exact matching target

kappa = a0/sqrt(G epsilon_DE)
      = 2 sqrt(8pi) cb^3/[c3 sqrt(c0)].                 (6)

Both Lambda and Mpl cancel. Thus a common microscopic origin is not excluded by dimensional analysis. It could in principle predict the ratio if its dimensionless amplitudes were determined independently. In SI the denominator corresponding to this natural-unit ratio is c sqrt(G rho_DE), with rho_DE a mass density.

But sharing a scale alone is insufficient. The exact sensitivities are

d ln kappa / d ln cb=3,
d ln kappa / d ln c3=-1,
d ln kappa / d ln c0=-1/2.

Shift symmetry permits derivative operators with arbitrary C; it does not set a baryon coupling that breaks that shift. The residual diagonal symmetry of two condensates permits an arbitrary additive vacuum constant. Permutation symmetry can relate coefficients between species but does not equate an identity operator, a derivative interaction and a matter portal. These observations concern those specified symmetries; they are not a no-go against a stronger microscopic theory.

Dimensional transmutation can produce a scale from microscopic coupling and boundary data, but it does not by itself determine that input coupling. Neither the absolute vacuum scale nor the three amplitudes in (6) have been computed here. Setting c0,c3,cb to convenient order-one values would be another ansatz, not the requested eta selection.

## 5. Evidence and exact disposition

The main check passes 20/20 symbolic identities; its separate mutation deliberately fails pressure/source-normalization assertions. The parent check passes 10/10 identities; reversing its cubic sign fails the asserted stationary matching. Bounded run manifests and validation results accompany the scripts. No empirical acceleration, target kappa, numerical scan or fitted coefficient enters either script. Symbolic checks verify these algebraic reductions, not a microscopic theory.

Route A closes only the proposed replacement of normalized phase energy with ordinary stable-mass, nonrelativistic Rabi mixing. Route B establishes the conditional force and invariant matching target (6), leaving its microscopic amplitudes and scale unselected. Route C verifies a constructive higher-energy EFT parent and its cutoff limitation; a genuine UV calculation remains open.

The previous KGB route failed to produce MOND at all. This route gets the force functional but not joint selection. The remaining task is therefore precise: construct a theory that computes c0,c3,cb and its scale, supplies the allowed parent branch and baryon portal, and retains a healthy cosmological and galactic solution. No such theory has been obtained in this continuation.
