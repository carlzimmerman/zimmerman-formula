# Independent audit: exact finite-stiffness halo and its full constrained energy inequality

15 October 2026. Primary verdict: **proved as written within the specified
counted nonrelativistic electrostatic/current model**. The candidate is an
actual finite-gamma constrained equilibrium with positive finite-density cold
matter and a positive fixed baryon source. Its outside inequality proves a
global mechanical energy minimum against arbitrary angular and support
variations in the declared physical domain. This does not make it a solution
of the unconstrained S2 empty-space field variation or a healthy relativistic
material/vacuum interface. Independent here means a separate agent's fresh
reconstruction, with the same model family; it is not external peer review.

Audited SHA-256 values:

- PROOF.md: `db363953a1199748c668e71c65911db17992c7e7868f6591bfc36fe43f7e01ca`
- check_stiff_halo.py: `8e1ad0c4d22564dc1dfec95d9a668ae0d18ac570b6766cb4052b0602ccec767b`
- run_v1/results.json: `306b90af861818289edded99eb0ed17c1290c58fc9a1730745f6a3e590f7ece0`
- run_v1/manifest.json: `da7af2ac56ae0fa2fa591f4aca3e8183cf5c090d127500bd2cc332bea99a4750`
- Referenced lift PROOF.md: `5e34946670364a2563c7c7d9a300e6c281975a1fa3ab0f69f90af10881d51280`

## Sources, force equation and exact positivity certificate

I reconstructed m(r) by integrating the stated cold density with 4 pi r^2,
then computed u=m/r^2 and derived the source required by the actual equilibrium:
`gb=u^2/(1-u)-gamma rho'`. This reproduces the stated source, rather than
assuming that its construction proves stationarity. Its integral cold mass is
1/10 and the source integral is 25/1341; their ratio is exactly 5.364.

The bound `u <= (35/194) r <=35/194<1/5` follows by subtracting the two negative
polynomial terms in u. It avoids the constitutive pole everywhere in the halo;
outside, u=(1/10)/r^2 decreases further. The density factors as
rho0(1-r^2)(1+9r^2/10), so it is positive in the occupied ball, finite at the
center and zero at the edge.

For the baryon source I recomputed
`q=(1-u)^2 Mb'(r)/r^2` from that independent m and force equation. The fifteen
reported positive rational coefficients reconstruct this same q exactly as
`sum c_i binomial(14,i) r^i(1-r)^(14-i)`. This independently verifies both the
certificate's object and its coefficient interpretation; it does not merely
rerun the author's power-to-Bernstein conversion. Thus q>=min c_i=101/84930
on the whole interval. The finite limit rho_b(0)=k/(20 pi) is positive. The
baryon density can have a radial linear correction at the center, so this is a
finite-density source rather than an asserted infinitely smooth baryon core.

The source profile, the chosen gamma and the imposed inventory ratio are
construction inputs. The numerical equality to the supplied 5.364 does not
derive that ratio, select a physical galaxy, fit data or determine Lstar.

## The interface and the missing boundary term check

Write P0=m rhat/(4 pi r^2). Gauss is div P0=rho, so at r=1 the zero limiting
rho implies P0 and its normal first derivative match the Coulomb exterior.
Consequently Delta P0=grad rho holds weakly with a bounded jump and **no delta
surface term**. The exterior field carries the inventory flux; setting it to
zero would violate Gauss. At the center P0=O(r), and at infinity P0=O(r^-2),
so the radial Hodge boundary factor r|P0|^2 vanishes at both ends. The same
boundary conditions are required of admitted competitors or their corresponding
integration terms must be retained.

Let F=u^2/(1-u)-gb. The full first derivative is
`V'[P0]=(F-gamma rho') rhat`. Setting
`psi(r)=integral_r^infinity F(s)ds` and lambda=psi+gamma rho gives exactly
`V'[P0]=-grad lambda`, including across the edge. The cold current equation
requires grad lambda=0 in occupied matter, which is the verified bulk identity.
No equilibrium force equation is imposed on nonexistent exterior particles.

Outside, `r^2 F=M^2/(r^2-M)-Mb` has negative derivative for r>=1 and starts at
F(1)=-101/13410<0. Hence lambda'= -F>0 there, lambda increases to zero and
lambda>=mu=lambda(1)<0. Since rho vanishes continuously at the boundary,
lambda is continuous and there is no omitted interface contribution from its
integration by parts.

## Full angular and support variations

The potential's Hessian is the positive W Hessian plus the nonnegative
transverse Maxwell and gamma gradient forms; the baryon term is linear. The
physical field cap, div P>=0 and fixed mass make a convex admissible class.
For any such competitor, integration by parts and the fixed mass give

    <V'[P0],P-P0>=integral lambda(rho-rho0)
                   =integral (lambda-mu)rho >=0.

This is the missing outside inequality that a mere radial bulk solution would
not establish. It covers moving support and nonradial perturbations without
using a prescribed inner wall or holding the cold boundary fixed. Convexity
therefore proves V[P]>=V[P0]. The gamma quadratic remainder is zero only for a
constant field difference; finite-energy decay excludes a nonzero constant,
so the field minimum is unique within the stated class.

The actual physical current remains independent of P_t except in the radial
reduction. Its kinetic perspective |j|^2/(2rho) is nonnegative with the stated
vacuum convention. The first-order fluid/Vlasov lift in the pinned companion
proof supplies its conservation and Hamiltonian, so the result does not rely
on silently identifying a static auxiliary polarization with a velocity.
Energy conservation presumes an existing sufficiently regular closed evolution.
The theorem supplies a mechanical energetic minimum; it does not prove smooth
global evolution, a formation basin, damping, a spectral gap or a metric cone.

## Material/vacuum scope that remains open

At the edge x=u/a0=0.1 while rho tends to zero. If one tried to attach the
previous reciprocal-current causal-response family unchanged, its required
h_eff>hcrit could not hold through this occupied taper: h_eff tends to zero
while hcrit remains positive. The present Hamiltonian construction is thus a
nonrelativistic result with an exterior static law; it must not be promoted to
that earlier relativistic health theorem. The fixed baryons also have no
proved dynamical response. The proof states these exclusions explicitly.

The orthogonal reconstruction and certificate check are recorded in
`../dynamical_lift/check_stiff_halo_audit.py` and its bounded-run manifest.
No new external theorem is needed for the local algebra, Bernstein positivity
or convex supporting-plane inequality used here.
