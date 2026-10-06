# Log-braiding plus a varied acceleration response: vacuum map survives, MOND is not automatic

The proposed repair preserves the exact classical vacuum-rescaling map and has positive fully constrained quadratic scalar coefficients on its four-dimensional rolling de Sitter branch. It does **not** turn that branch into a static critical MOND response: the original nonzero curvature gradient stiffness remains. More concretely, a conserved first-order smooth comoving dust source has an inverse-square physical metric force while the clock acceleration vanishes. This is a restricted sourced countercontrol, not a bound-galaxy solution or a no-go for nonlinear matching.

## Declared action and invariant vacuum map

Use signature (−+++), c_light=ℏ=1, X=−∂φ²/2>0, and the same physical metric for matter sources and test bodies:

S=∫√−g [K_E R/2−c ln(X/Xref)−G(X)□φ−ρv+Lresp]+Sm[g,ψ],
G(X)=−√2 c/(nH*) X^{−1/2},
uμ=−∂μφ/√(2X), aμ=uν∇νuμ, g_a=√(aμaμ), θ=∇μuμ.

The action/vacuum symmetry statement holds for general n; all quadratic constraints and source calculations below are explicitly n=3. Take c>0, K_E>0, H*>0 and q=φdot>0 constant on the rolling de Sitter state. With [φ]=mass, [X]=mass^4, [c]=mass^4, [K_E]=mass², [G]=mass and [H*]=mass, every displayed four-dimensional Lagrangian term has mass^4. This is a formal classical X>0 action; singular zero-X limits, cutoff control and quantum corrections are not resolved.

Add the exact same-foliation term

Lresp=−2K_E[W(g_a;A)−g_a²/2],
W(g;A)=½[g√(g²+A²/4)+(A²/4)asinh(2g/A)]−Ag/2.

Choose either A=A*>0, or A=βθ on an expanding θ>0 branch with β>0 dimensionless. No value of β is set from the target coefficient. For a finite constant vacuum change Δρ, define s=exp[−Δρ/(2c)]>0 and φnew=sφ, ρv,new=ρv+Δρ. Then Xnew=s²X, K(Xnew)=K(X)+Δρ, G(Xnew)□φnew=G(X)□φ. Moreover u, a, θ and the metric are exactly unchanged. Both choices of A are therefore invariant, and the entire added response is invariant pointwise. This establishes a map between the constant-vacuum theories, not adjustment through a physical time-dependent phase transition.

For A=βθ its full variation includes δA=βδθ in addition to δu and δa. It cannot be treated as an external fixed function in an inhomogeneous calculation. However W=O(g³/A) near g=0, so Lresp=K_E a²+O(|a|³/A). Its quadratic coefficient is independent of A: the extra θ variation first enters at higher perturbative order about the geodesic rolling background. Lresp and its first variation vanish on that background, preserving its exact H* and vacuum map.

The original functional KGB branch satisfies J=0, with z=−c/(3K_E H*²) independent of vacuum. Use −1<z<0; z=0 is degenerate and z=−1 singular in the constraint inversion. The field normalization q changes with vacuum while H* remains fixed. With A=βθ the background scale is A0=3βH*, and Λgeom/A0²=1/(3β²). This is a free dimensionless action parameter, not a selected coefficient. With fixed A*, the ratio is 3H*²/A*².

## Full quadratic constraints, including the added lapse gradient

Work in unitary gauge δφ=0, h_ij=a(t)²e^{2ζ}δij, lapse N=1+ν, shift N_i=∂iB. Because u is the unit normal, a_i=∂i ln N exactly. Thus the added quadratic term is +K_E a(t)^{−2}|∇ν|², not a fixed-metric scalar approximation. On the constant-q rolling branch,

Θ=K_E H*(1+z), Σ=−3K_E H*²(1+2z).

Writing Δ/a² for the spatial Laplacian, the complete scalar quadratic integrand divided by a³ is

−3K_E ζdot²+K_E|∇ζ|²/a²+Σν²
−2Θν ΔB/a²+2K_E ζdot ΔB/a²+6Θνζdot
−2K_Eν Δζ/a²+K_E|∇ν|²/a².

This is the Einstein/KGB constrained scalar action plus the directly varied response contribution. Variation of B is unchanged: Θν=K_E ζdot on nonzero Fourier modes. Variation of ν is changed by the new spatial operator. In the presence of a weak density source its constraint is

Σν−ΘΔB/a²+3Θζdot−K_EΔζ/a²−K_EΔν/a²=δρ/2.

There is no extra propagating lapse mode because the added term has no νdot. Eliminating B first enforces ν=ζdot/[H*(1+z)]; substituting this constraint into the action and integrating the ζζdot gradient term by parts gives

S²=∫dt d³x a³ [G_S ζdot²−F_S |∇ζ|²/a²
+K_E |∇ζdot|²/(a²H*²(1+z)²)],
G_S=3K_E z²/(1+z)²,
F_S=−K_E z/(1+z).

Thus the original F_S stays nonzero and positive. For a Fourier mode with p=k/a,
A_k=G_S+K_E p²/[H*²(1+z)²]>0.

This is a full quadratic lapse/shift reduction, not a frozen-clock Hessian. Tensor coefficients remain those of Einstein gravity at this order because δN=0 for a tensor and the response vanishes on the background. Finite-gradient and nonlinear constraint health do not follow from these vacuum coefficients.

## De Sitter time dependence: short wavelength does not mean rapid relaxation

A frozen instantaneous ratio F_S p²/A_k is algebraically positive, but is not a controlled oscillation frequency: at large p it is only of order H*². On exact de Sitter p_dot=−H*p, hence A_dot=−2H*(A−G_S). The exact free mode equation is

ζddot+H* [3G_S+D p²]/[G_S+D p²] ζdot
+F_S p²/[G_S+D p²] ζ=0,
D=K_E/[H*²(1+z)²].

In the p/H*→∞ regime its leading equation is ζddot+H*ζdot−z(1+z)H*²ζ=0. Characteristic roots are H*z and −H*(1+z), both negative on the stated interval; at z=−1/2 the repeated root is −H*/2. The instantaneous restoring coefficient −z(1+z)H*² is at most H*²/4. This describes Hubble-scale decay in the UV regime, not high-frequency scalar oscillations. It can frustrate an assumed rapid stationary galaxy response, but says neither that the physical source force has a particular form nor that signal causality is established.

## A sourced physical-metric control: regular force and a geodesic clock

A nonzero F_S alone is not enough to infer the measured Newton force because ζ is a clock-gauge curvature variable. The following control supplies the source and observable dictionary explicitly.

Let a smooth first-order comoving dust density be δρ(t,x)=a(t)^{−3}ρ0(x), with δmomentum=δpressure=0 and no incoming/free scalar waves. These stresses are conserved on the de Sitter background at first order: δρdot+3H*δρ=0. Force-induced velocities and worldline displacements may be order M, but their corrections to the order-M stress enter at second order. The fixed comoving shape is the background source prescription, not a claim that exact fixed-coordinate dust worldlines are geodesics in the perturbed metric. This control is not a virialized stationary object at fixed physical radius. Use isolated/invertible Laplacian boundary conditions; no homogeneous clock charge is inserted.

Its matter coupling is −∫a³δρ ν. After the momentum constraint this becomes −∫a³δρ ζdot/[H*(1+z)], a time boundary term because a³δρ is constant. Hence ζ=ν=0 solves the reduced sourced equation with the stated no-free-wave prescription. The lapse constraint then gives

ΔB/a²=−δρ/(2Θ),
B_k=δρ_k/(2Θp²), Bdot_k=−H*B_k.

To convert to the physical Newton gauge, use the time shift T=−B, keeping zero spatial shear. The physical potentials are

Ψ=ν+Bdot, Φ=−ζ−H*B.

They therefore coincide, Ψ_k=Φ_k=−δρ_k/[2K_E(1+z)p²]. Equivalently ∇²_physical Ψ=δρ/[2K_E(1+z)]. Outside a compact smooth source, the linear spherical metric force is G_N,measured M/r² with G_N,measured=1/[8πK_E(1+z)]. It is proportional to M, and A does not enter at this order. Simultaneously a_i=∂iν=0: the rolling clock is geodesic even though the physical test metric has a force. The new response senses the clock's proper acceleration, not automatically |∇Ψ| in Newton gauge. Replacing the former by the latter without varying the clock would discard this branch.

This control demonstrates that adding the P2 operator does not by itself remove all regular weak-source metric response or force every source onto MOND. It does not prove a nonlinear bound galaxy has the same geodesic clock, or establish a universal static no-go. Nonlinear response branches, imposed stationary physical boundary conditions and formation histories need their own coupled analysis.

## Evidence and exact next obligation

Fresh main_b passes the exact vacuum identities, momentum/lapse reduction, gradient coefficient, exact de Sitter friction, sourced metric dictionary and 16 bounded coefficient controls at z∈{−.1,−.25,−.5,−.9}, p/H*∈{.1,1,10,100}. Fresh control_mixing_b, control_kinetic_b and control_scale_b reject the omitted clock mixing, omitted acceleration kinetic term and incorrect rescaling of fixed A respectively. All four manifests validate. Earlier a-runs predate the added exact-friction checks and are retained as historical bounded evidence, not the current full check set. Counts do not replace the derivation.

The authorized local primary copies are Kobayashi–Yamaguchi–Yokoyama [arXiv:1105.5723v2](https://arxiv.org/pdf/1105.5723v2), especially the raw action (55), constraints (60)–(61), and reduced coefficients (62)–(64); Bernardo [arXiv:2101.00965v2](https://arxiv.org/pdf/2101.00965v2), the KGB action and functional rolling self-tuning branch. Their cached exact-version text hashes, inspected peer report and actual checkout HEAD are pinned in provenance.json and standard-run manifests. No peer execution inputs were changed. The extension and source control are derived here; no global-literature novelty or health inheritance is claimed.

The missing implication is now sharper: obtain a timelike, conserved, fully sourced bound-galaxy solution of this same extended action in which the clock's proper acceleration actually supplies the required physical metric MOND flux after all clock/lapse/shift variations, with specified cosmological boundary and history data. It must coexist with the surviving regular source branch and Hubble-scale scalar relaxation, and its finite-gradient constraints must be healthy. Even if that succeeds, a separate selector for β (or A*/H*) is still required for 32π.
