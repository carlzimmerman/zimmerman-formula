# Proper-volume normal expansion after the mean Bianchi-I response

For the admitted **linear** decaying signed integration mode, the formally sourced homogeneous second-order Einstein rows can be solved with explicit initial data. Their homogeneous shear matters. After including those mean responses, the proper-volume-weighted expansion of the preferred-clock normal remains exactly the de Sitter value at this order. Its homogeneous normal shear can also remain zero with the corresponding initial data. This provides no positive cold abundance from this mean observable.

This completes the common homogeneous response calculation, not the full local second-order field solution. The zero Fourier clock row is an identity; its local nonzero Fourier rows are not. The possible nonlinear admission obstruction from the quadratically degenerate clock remains explicit below. We do not assume those unresolved rows admit the linear mode.

## Scope, mode and exact mean chart

The inherited projected action has two Einstein coefficients K>0, individual M=2K, geometric-mean volume, common preferred clock θ, and near-coincidence interaction −4KΛv+K v H^{ij}∂i r∂j r+O(|∂r|³). Work in n=3 coincident empty de Sitter, H>0, Λ=3H², and a fixed three-torus containing a real mode cos(kx), k>0. All inputs are pinned in provenance.json; base inspected is 67e981cf7888172c584868ae80a178492af40fa1.

Use the symmetric exponential unitary-clock chart of the previous raw source calculation, with relative lapse amplitude ν, parallel spatial amplitude U=Z+E and two transverse amplitudes Z. Retain common homogeneous Bianchi-I lengths a_x,a_y=a_z, with h_x=dln a_x/dt and h_y=dln a_y/dt, and vary the common lapse N before choosing its mean proper-time value one. Opposite shifts are ∓εkβ sin(kx)/(2a_x²). The common mean lapse can be set to one by a common homogeneous time reparametrization together with the exact clock relabeling symmetry; this preserves the foliation rather than asserting an additional relative gauge.

The actual first-order scalar constraints give ν=Zdot/H, E=−3Z−ν, β=−Edot/P−(Z+ν)/H, P=k²/a². Select the genuinely gravitating decay mode Z0=0:

Z=B/a, ν=−B/a, E=2ν, β=2Hν/P, a=exp(Ht), a(0)=1.

B is a free small-mode amplitude. Its actual visible first-order Weyl potential is ν/2 and its signed density is −MPν. No positive background density is present. Every second-order expression below is the coefficient of ε² with ⟨sin²⟩=⟨cos²⟩=1/2; no complex-mode normalization is substituted.

## Unreduced directional Einstein variation

With γ=diag(exp(2u),exp(2v),exp(2v)), the exact plane ADM curvature is exp(−2u)[−4v_xx+4u_x v_x−6v_x²] and the extrinsic invariant is −4κ_xκ_y−2κ_y². The raw expansion, keeping h_x,h_y independent, yields

L_2=−K a_x a_y² C/N+K N(a_y²/a_x)k²Q,
C=A_x Zdot+Zdot²/2+X[h_y A_x+(h_x+h_y)Zdot]
  +X²(h_xh_y/2+h_y²/4)−Pβ[h_y U+(h_x+h_y)Z],
A_x=Zdot+Edot+Pβ, X=3Z+E−ν, Q=(Z+ν)²/2.

Here the symbol A_x is a relative velocity combination, not the second-order mean scale correction introduced next. checks.py reconstructs this expression by differentiating the two exact plane contributions, not importing the previous formula. The interaction vacuum supplies the background and is exactly independent of the symmetric relative exponential variables. Its effects are retained in the Einstein constraints through the admitted background H.

Varying N, ln a_x and ln a_y before imposing relative constraints, then evaluating on the actual linear mode, gives the total effective common Einstein source

ρ_eff=−K H²ν²/2,
p_parallel=3K H²ν²/2,
p_transverse=−K H²ν²/2.

These include the Einstein perturbation nonlinearities as well as the interaction; they are not a newly declared material stress. Their trace pressure is −ρ_eff/3 and their time conservation row is zero. The anisotropic source is p_parallel−p_transverse=2KH²ν². Dropping it would be an inconsistent isotropic mean truncation.

## Exact homogeneous second-order solution

Write ln a_x=Ht+ε²[A(t)+2S(t)/3], ln a_y=Ht+ε²[A(t)−S(t)/3]. The common Einstein coefficient is 2M=4K. Its mean lapse, anisotropic and trace equations are respectively

24KH Adot=ρ_eff,
4K(Sddot+3HSdot)=p_parallel−p_transverse,
−8K Addot−24KH Adot=(p_parallel+2p_transverse)/3.

They are solved by

A=A_i+B²(a^(−2)−1)/96,
S=S_i+B²[1/12−a^(−2)/4+a^(−3)/6]+J(1−a^(−3))/(3H),

where A(0)=A_i, S(0)=S_i, Sdot(0)=J. Thus Adot=−Hν²/48. The lapse fixes the initial mean expansion; it is not an arbitrary datum that can be chosen independently of the signed mode. The trace equation follows consistently from the lapse conservation identity and is also checked directly.

One concrete geometric preparation chooses A_i=−B²/48, S_i=0, J=HB²/2. The first choice normalizes the averaged proper volume to its unperturbed value initially; the third sets the initial **normal** mean shear to zero, which differs from setting the chart shear rate to zero. General A_i,S_i,J are retained above so this preparation is transparent rather than a forced unique state.

## Geometric mean observable versus coordinate-volume rate

Define each metric's preferred-clock normal expansion Θ_g=∇_μu_g^μ and its proper-volume average on θ=t:

H_normal,g=∫√γ_g Θ_g d³x/[3∫√γ_g d³x].

This is a specified geometric foliation observable. It is not dln(V_g,spatial)/dt divided by three when the local lapse is inhomogeneous. The hatted observable is equal at this order by the periodic symmetry.

The first-order mode changes each averaged proper spatial volume by ν²/16. Its raw contribution to the averaged normal expansion is Hν²/48. To see the latter, use Θ=κ_x+2κ_y and weight by √γ: the exponential factor is exp[ε(3Z+E−ν)cos(kx)/2]. On the mode, the quadratic numerator is Hν²/4, while denominator normalization subtracts 3Hν²/16. Their difference divided by three is Hν²/48. The actual mean scale response therefore gives

H_normal,g=H+ε²[Adot+Hν²/48]+o(ε²)=H+o(ε²).

The normal mean directional shear has correction −Hν²/2, so

S_normal=Sdot−Hν²/2=(J−HB²/2)a^(−3).

The declared initial normal shear zero remains zero. Its homogeneous integration mode otherwise decays as a^(−3), but its quadratic shear energy would enter at order ε⁴; this does not supply an order-ε² dust density.

By contrast the spatial-volume scale obeys

ln a_volume=Ht+ε²[A+ν²/48],
dln a_volume/dt=H−ε²Hν²/16.

The discrepancy is the inhomogeneous lapse/transport weighting, not an algebra inconsistency. It demonstrates why a coordinate-rate background correction cannot automatically be interpreted as a positive gravitating cold component. No universal statement about every averaging prescription follows from this one preferred-foliation observable.

## Which remaining equations can enter the mean rows?

At the coincident translation-invariant background, the **linear** operator on second-order perturbations preserves Fourier wave number. Consequently the nonzero harmonics of the second-order fields cannot enter the zero-mode rows above. Common mean momentum sources average to zero by reflection (their quadratic integrands contain sin(kx)cos(kx)); directional common spatial rows are retained by the Bianchi-I ansatz.

For the analytic Einstein/vacuum/quadratic-gradient terms, exchange symmetry makes the action even in relative variables and their pure-relative cubic Taylor coefficient vanish. They therefore do not drive a second-order relative zero mode. The lowest nonanalytic |∂ν|³ term generates a relative order-two local Euler source that is a spatial divergence of |∂ν|∂ν. Its torus average is zero. Thus homogeneous relative integration data can be chosen zero at this order without adding a hidden arbitrary charge to these common mean equations. Local relative corrections are still required and have not been solved.

Most critically, θ→f(θ) leaves the normalized normals and acceleration invariant **exactly**. On θ=t, varying θ by any homogeneous δf(t) therefore leaves the action unchanged, so ∫E_θ(t,x)d³x=0 is an off-shell zero-mode identity. The mean clock row does not obstruct the above mean solution. This does not make E_θ(t,x)=0 pointwise. Because the common clock has no quadratic action at coincidence, its first nonzero local Euler condition at order two can be a compatibility condition on the first-order metric data rather than an equation invertible for θ_2.

The precise unsolved local obligation is the order-two coefficient of

δS_int=2K a0²∫v[m δI],
δI=δ(P_g+P_hat)^{μν}A_μA_ν/(2a0²)+2P_avg^{μν}A_μδA_ν/a0²,
δu_gμ=−N_θ,g P_gμ^ν∂νδθ,
δa_gμ=δu_g^ν∇νu_gμ+u_g^ν∇νδu_gμ,

and its hatted counterpart, integrated by parts for arbitrary **inhomogeneous** δθ. Spatial averaging kills only its zero row. No full local second-order completion is asserted until that condition and the nonzero-harmonic metric constraints are solved or shown compatible. If this condition excludes the seed, the formal mean response remains a correct necessary-row calculation, not an admitted solution.

## Cold/growth implication and evidence

The geometric mean expansion shows no order-two positive homogeneous cold component from this prepared single mode. The free signed linear integration amplitude remains a clue, but neither its canonical energy nor its mean chart source closes Claude CFG355's required cold mass, stream/host state or actual growth history. CFG355's rank/tidal source is read and pinned only as context; its scripts/results are not rerun or reclassified.

Twenty-one exact checks reconstruct the raw anisotropic action, all three mean Einstein rows, explicit initial data, normal-weighted expansion/shear and coordinate-volume distinction. The three controls equate the coordinate volume rate with normal expansion, omit the mean response, or insert a positive dust expansion term. Standard bounded evidence and validation are in RUNS.md. No physical second-order backreaction equation of state, full nonlinear health, particle identity, primordial state, likelihood or 32π selection is inferred.
