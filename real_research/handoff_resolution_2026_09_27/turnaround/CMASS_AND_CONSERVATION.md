# HR01-T CMASS, retained source mass and late-web continuation

This is a new conditional computation, `cmass_source_gate.py`, built from the cached FP23 central-HOD input tables, its Sheth–Tormen/CLASS HOD definitions, FP20's exact spherical projector, FP16's retained-carrier table, and XR36's Newtonian first-turnaround engine. It uses both a0 footings. No new observations were obtained. The CMASS observational likelihood is absent from the local source; FP23's quoted 0.71–0.83 lensing ratio is used only as its inherited informal comparison band, not an independently verified measurement or likelihood.

## Controls and exact scope

The stored FP23 sum of baryons, phantom, retained carrier, escaped carrier and two-halo contributions reproduces its saved total. Rebuilt HOD biases pass 1e-4 relative; rebuilt LCDM one-halo plus stored LCDM two-halo profiles reproduce saved LCDM ratios to machine precision. These are real baseline controls. The new model removes H_K1, uses isolated P2 with uniform-frame subtraction, removes the yield, and keeps the LCDM two-halo contribution. It assumes the central HOD, stellar mass 10^11.4 solar masses, Hernquist scale 5 kpc, gas fraction .157, kick table 575 km/s, and the source's 31 halo masses 10^12.3–10^15.3 solar masses. These inputs are inherited empirical/phenomenological structure, not a zero-parameter derivation.

The bound-region input is constructed instead of silently assumed: the Newtonian convention-B engine determines the first-turnaround radius of a 10^11 solar-mass compact seed at z=.5 and .65; point-mass scaling R0 proportional to Mseed^(1/3) assigns each host a region from its stars+gas+retained-carrier seed. This is an explicit constant compact-seed surrogate, not self-consistent extended-halo or accretion evolution. The HOD-weighted edges are 1.45607 and 1.31544 Mpc.

For an ungated enclosed phantom mass Mphi(r), a response/flux gate produces Mphi(r) times 1[r<re], including its compensating negative shell. A source-density gate integrates 1[r<re] dMphi/dr and gives Mphi(min(r,re)); it retains exterior mass. The latter changes Gauss's equation rather than being a harmless relabeling of XR36. The scalar source term can be written Delta psi=4 pi G 1_Omega rho_phi, but this Poisson equation alone is not a complete variational prescription.

## New CMASS profiles

Ratios of predicted Delta Sigma to FP23's matched LCDM reference are:

| z | footing | prescription | 0.3 Mpc | 1 Mpc | 3 Mpc | 10 Mpc |
|---|---|---|---:|---:|---:|---:|
| .5 | canonical | source gate, additive | 1.0093 | 1.8153 | 2.3624 | 1.3491 |
| .5 | alternate | source gate, additive | 1.0700 | 1.9451 | 2.5262 | 1.3855 |
| .65 | canonical | source gate, additive | .9960 | 1.8348 | 2.1982 | 1.2762 |
| .65 | alternate | source gate, additive | 1.0571 | 1.9677 | 2.3440 | 1.3051 |
| .5 | canonical | conserved replacement | .6576 | .9097 | .9988 | 1.0000 |
| .5 | alternate | conserved replacement | .7194 | .9319 | .9993 | 1.0000 |
| .65 | canonical | conserved replacement | .6601 | .9213 | .9995 | 1.0000 |
| .65 | alternate | conserved replacement | .7210 | .9410 | .9997 | 1.0000 |

The source gate with additive phantom therefore retains the wrong-sign enhancement in this actual CMASS-like construction. The source gate cannot be treated as a free repair of the negative-shell problem.

The conserved replacement row is a second, constructive prescription: replace the original retained+escaped carrier by min[Mphi(min(r,re)), Mh-Mb(infinity)]. It preserves the halo's final total mass rather than adding phantom to a halo that already contains its dark budget. This profile lowers the inner lensing and tends to the correct total-halo exterior, but does not reach the inherited .71–.83 comparison band at 1 Mpc. No covariance-weighted data pass is claimed. The prescription's edge is where the available reservoir is exhausted, not a derived shell-crossing event.

The script also computes exact conditional bounds when independent amplitudes alpha,beta in [0,1] multiply the saved FP23 one-halo phantom and two-halo excess profiles. These are pointwise component-amplitude bounds, not universal bounds on arbitrary radial masks: the ESD projector has sign-changing weights, so nonnegative radial source suppression does not imply pointwise ESD suppression. The explicitly projected radial masks above avoid that invalid inference.

## Mass accounting supplies an edge condition

For point baryons in the P2 law,

Mphi(r)=Mb [sqrt(1+r^2/rM^2)-1], rM=sqrt(G Mb/a0).

A conserved reservoir Mc requires Mphi(re)<=Mc. At equality,

re = sqrt[G Mc(Mc+2 Mb)/(a0 Mb)].

This is an actual algebraic edge condition with no added fitted length. It depends on the separately supplied dark reservoir and is not a collapse or shell-crossing derivation. For extended baryons the corresponding equation Mphi(re)=Mc is solved with their enclosed profile. A smooth time-dependent implementation still needs a dark-field stress tensor and conserved flux.

The selected CMASS-central population has number densities 1.50925e-4 and 1.38543e-4 Mpc^-3 in the discrete HOD quadrature. The additive source phantom alone contributes 0.33464/0.36951 of the cosmological matter mean at z=.5, and 0.26217/0.28956 at z=.65 (canonical/alternate). These are selected-population halo-model integrals, not measured cosmic densities. They diagnose substantial double counting if one simply appends retained phantom to the existing matter background. A viable continuation must replace or redistribute dark matter, or else re-solve the cosmology with that extra mean.

Continuity makes the same point dynamically. If rho_s=W rho_phi is postulated, partial_t rho_s+div(W j_phi)=(partial_t W) rho_phi+j_phi.grad W whenever the ungated pair obeys continuity. The switch therefore requires exchange terms or a surface flux. Conserving total matter requires an opposite carrier transfer, not just deletion of the gate's negative shell. Neither the original XR36 mask nor the new static capped profile supplies this current.

## A discriminating late-web check

A compact mass-conserving rearrangement of one halo has Delta u(0)=0 and, with finite second moment,

Delta u(k)= -k^2 Delta<r^2>/6+O(k^4).

Thus retained source mass and conserved replacement have distinct infrared limits. This statement concerns the density form factor, not a theorem of unchanged growth or unchanged sigma8.

The script implements a separate compact-support control: truncate the baryon tail at max(re,R200), cap the phantom by the remaining total mass, and keep any leftover reservoir at the boundary. The compact construction is declared separately because the untruncated Hernquist tail in FP23 does not have finite second moment; one cannot apply an O(k^2) proof to that tail without this restriction. Total halo-mass differences are zero to 1e-12 relative, and the numerical low-k coefficient matches the moment formula to 1e-4 relative.

For the compact HOD-weighted replacement, Delta u at k=.1 h/Mpc is -3.516e-4/-2.556e-4 at z=.5 and -3.604e-4/-2.637e-4 at z=.65. At k=1 h/Mpc it is -0.03007/-0.02222 and -0.03110/-0.02311. This route avoids the additive monopole boost and produces modest finite-scale suppression in this controlled static calculation. It does not yet determine the CMB lensing power: halo bias, unequal-time correlations, evolving profiles, velocities and a dynamical action are missing.

MUTATE removes the exterior retained source mass. It fails the named source-mass conservation checks rather than crashing; baseline HOD/projector checks remain valid. The density form-factor check is not a replacement for a particle-mesh evolution.

## Paired density-tide followup

`density_tide_pair.py` computes an independent spherical test at Mb=10^11 solar masses and z=.25. A uniform peculiar overdensity delta=1 extends to a declared 5 Mpc test radius. In potential-gradient convention, the matched environmental phantom subtraction is

p(gb+gt)-p(gt), p(g)=g[nu(g/a0)-1], gt=(4 pi G delta rho/3)r.

In deep MOND the excess/isolated phantom-flux ratio is sqrt(1+e)-sqrt(e), e=gt/gb. At 1 Mpc, e=3.23184 and the deep result is .25941; exact P2 gives .25046/.25126. After the exact spherical ESD projection, the paired/isolated ratios at .1/.3/.6/1/2/3 Mpc are approximately .976/.854/.599/.352/.135/.074 for both footings. This is a large density-tide suppression despite exact cancellation of a uniform vector field.

This matched spherical environment subtraction is not automatically the operation performed by an observational random catalogue or isolation cut. It is a controlled counterexample to assuming uniform-field subtraction restores the isolated signal under a density tide. The finite 5 Mpc environment and spherical alignment are test inputs. The zero-lens and projector-linearity controls pass; MUTATE omits the environment subtraction and fails both controls on both footings.

The next mathematical implication is a conserved dark-field evolution generating the capped/compact profile and its exchange current from one action, together with the region/frame and perturbation equations. The source-gate mass-budget and late-web checks narrow that task substantially but do not establish it.

## The source-gate action cannot be inferred from the Poisson rule

There is a concrete variational check. For a prescribed nonconstant W and a linearized ungated symmetric operator L, the source-gated map E(u)=W L u has derivative W L, whose adjoint is L W. Unless [W,L]=0, this is not a Hessian of a real twice-differentiable single-field functional. The two-cell example

L=[[-1,1],[1,-1]], W=diag(1,0), W L=[[-1,1],[0,0]]

already has unequal off-diagonal entries. For continuum L=Delta, the missing adjoint terms are 2 grad W.grad u+(Delta W)u. In contrast, the flux-gated operator div(W A grad u) is symmetric under the usual fixed-boundary hypotheses. This is why one cannot simply replace the response gate by a source mask in the original scalar action while keeping all its other equations.

This audit does not exclude a theory with independent conserved dark degrees of freedom. It identifies the actual next construction: the capped source density must be supplied by an independent matter field/current with its own equations, or the scalar variational completion must include the missing interface/adjoint response. The static min rule alone supplies neither. Eliminating regular variational auxiliaries gives a symmetric Schur complement, so auxiliary labels without their physical equations do not by themselves cure the reciprocity condition.
