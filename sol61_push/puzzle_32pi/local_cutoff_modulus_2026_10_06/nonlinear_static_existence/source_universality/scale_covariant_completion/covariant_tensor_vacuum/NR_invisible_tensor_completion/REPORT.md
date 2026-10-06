# NR-invisible quadratic completion: curvature repair but no critical kinetic repair

Within the displayed five quadratic connection-contraction types, a linear interaction whose leading pressureless weak-static NR value and spatial first variation both vanish can change the de Sitter relative-tensor curvature mass, but cannot change its kinetic or spatial-gradient coefficient. There is a stable tensor cone for an already nondegenerate subcritical vacuum slope. The actual auxiliary source endpoint m=1/2 remains nonpropagating at quadratic order; this particular completion does not repair its missing kinetic block. Neither conclusion selects lambda or 32pi.

## Actual covariant candidate and primary-source scope

Use the parent's exchange-symmetric two-EH action, healthy EH coefficient K>0, preferred averaged Upsilon_sym, and the same auxiliary interaction M(z,T). Define the five contractions with one metric h (either g or hat g):

- S1(h)=h^{mu nu} C^gamma_{mu lambda} C^lambda_{nu gamma}.
- S2(h)=bar C^gamma C_gamma, with bar C^gamma=h^{mu nu}C^gamma_{mu nu} and C_gamma=C^alpha_{gamma alpha}.
- S3(h)=h_{mu nu}bar C^mu bar C^nu.
- S4(h)=h^{mu nu}C_mu C_nu.
- S5(h)=h_{alpha lambda}h^{beta mu}h^{gamma nu}C^alpha_{beta gamma}C^lambda_{mu nu}.

Take each S_A^sym=[S_A(g)+S_A(hat g)]/2 and set

`J=3S1^sym−2S2^sym−S4^sym+S5^sym`, `Delta S=K integral v(g,hat g) xi(z,T) J/2`.

The symmetric volume v has v=a^n on coincidence. C changes sign under exchange, so every squared contraction and J are invariant after the displayed averaging. This is an actual covariant additional interaction, not a prescribed correction to a tensor ODE. The dimensionless xi is smooth near the vacuum and has value xi0. A constant is sufficient for this local discriminator; a smooth factor exp(−z^2) can suppress it in the large-|z| regime without changing the weak-source invisibility or vacuum quadratic block. This suppression statement is restricted to that invariant becoming large, not every strong-field geometry.

[Milgrom2208.10882v4](https://arxiv.org/pdf/2208.10882v4), equations9,51–55, provides these five contraction types and a sufficient NR mixed-free class. In n=3, J=2S_q+S3 in his notation. His equation99 allows additional scalars with mixed NR terms when their interaction derivatives vanish on the NR branch. The paper leaves health open. The following general-n first-variation and tensor calculation is a scoped extension/test of those ingredients, not a novelty claim or a theorem about all invariants.

## General-n pressureless weak-static first variation

Set q=1/(n−2), n>=3. At the leading weak static scalar branch the difference connections are

`C^i_00=a_i`, `C^0_0i=C^0_i0=a_i`,
`C^j_ik=−q(delta^j_i a_k+delta^j_k a_i−delta_ik a_j)`, with a_i=partial_i phi_star.

This is the conformal spatial branch independently proved in the parent dictionary. No radial alignment is used here: a_i(x) is an arbitrary static gradient, and all spatial tensor perturbation directions are retained. Metric factors in the contractions are the common flat metric at this weak order. Corrections to contracting metrics and the volume are higher weak-field order; the result does not assert invisibility in the exact strong-field equations.

The traces are bar C^i=0 and C_i=−2q a_i. Consequently

`S1=−(n−1)/(n−2) a^2`, `S2=S3=0`, `S4=4q^2 a^2`, `S5=−3S1+S4`.

For an arbitrary static spatial metric derivative variation delta C^k_ij symmetric in i,j, define

`P=a_k sum_i delta C^k_ii`, `R=a_k sum_i delta C^i_ki`.

Direct index contraction gives

`delta S1=−2q P`, `delta S2=−2q P`, `delta S3=0`, `delta S4=−4q R`, `delta S5=2q P−4q R`.

Thus J=0 and delta J=0 for **all** these spatial perturbations, not just a radial scalar ansatz. S3 also has zero value and first variation because bar C=0. Varying the lapse scalar is a tangent to the same exact leading NR identity J(a)=0, so its first variation also vanishes. Static shift variation has no time-even cross term. If an arbitrary time-dependent shift test variation is used to form the full action Euler equation on the static background, the only linear temporal remainder is

`delta J=4(n−1)/(n−2) a_i (delta C^0_0i−delta C^i_00)`.

At linear weak order this difference is minus the time derivative of the shift perturbation. Its action variation is a time boundary term since a_i and xi(z,T) are static. Compactly supported variations therefore give no shift source. The result is an action-level stationary NR first-variation statement, not the false claim that delta J vanishes for every unconstrained delta C pointwise.

Multiplying J by a smooth xi(z,T) preserves the result: its first variation is xi delta J+J delta xi. Auxiliary T variation and the radial kernel remain unchanged on this leading branch. The parent's generic symmetric NR equations therefore survive; its constitutive relation to physical Newton acceleration remains spherical/aligned only. This completion does not turn that branch into arbitrary nonspherical QUMOND or inherit QUMOND external-field observables automatically.

## Completeness within this displayed quadratic contraction space

Consider I=sum_A c_A S_A with constant coefficients at the background. Requiring its NR spatial first variation to vanish gives

`c5=c1+c2`, `c4=−c5`.

Requiring its NR value to vanish then gives c1=3c5 and c2=−2c5; c3 is unconstrained. Hence this linear space is exactly span{J,S3}. P and R are independent spatial derivative variations: they can be independently varied by trace versus off-diagonal derivative choices for n>=3. The exact index identities supply the general-n proof; raw symbolic checks independently test all spatial h_ij,k directions for n=3,4,5,6.

This classification is restricted to the five displayed single-common-metric quadratic contraction types at leading weak order, their exchange-symmetric lifts, and regular linear coefficients. Metric-ratio weighted contractions coincide with these at this order but arbitrary additional tensor structures, derivatives of C, nonlocal operators, singular functions, or a changed auxiliary continuation are not classified. Merely vanishing NR value is insufficient: generic equation99-type scalars can have nonzero spatial first variations. If their smooth interaction derivative vanishes on the entire NR branch, including the origin, they contribute only beyond quadratic TT order at coincidence and cannot repair this quadratic kinetic block. A nonsmooth derivative limit evades that statement but requires a separately defined symbol.

## Exact common-FRW tensor contribution

For relative TT d_ij on a common FRW background, C^0_ij=a^2(Hd_ij+dot d_ij/2), C^i_0j=dot d_ij/2, and the usual spatial half-gradient connection. Both traces vanish. After spatial integrations by parts using TT transversality,

`S1=tr(dot d^2−a^−2(partial d)^2)/4+H tr(d dot d)`,
`S2=S3=S4=0`,
`S5=−3 tr(dot d^2−a^−2(partial d)^2)/4−H tr(d dot d)−H^2 tr d^2`.

Thus

`J=2H tr(d dot d)−H^2 tr d^2`.

The kinetic and spatial-gradient terms cancel identically. In particular S3 is tensor-inactive. This result holds for every TT polarization and n>=3; one may rotate the wavevector to a coordinate axis, and the TT contraction is proportional to its polarization norm. The executable additionally contracts a raw plus polarization without using a parent formula.

For constant xi0 and de Sitter H, integration with a^n gives

`integral a^n J=−(n+1)H^2 integral a^n tr d^2` up to a time boundary.

For general FRW it is −[(n+1)H^2+dot H] rather than the de Sitter coefficient. The latter distinction is not used to assert stability on an evolving matter background.

## Stable regular tensor cone and actual critical limitation

Assume the parent's regular **two-sided** vacuum slope m exists. The corrected relative-TT action on de Sitter is

`K integral a^n {(1−2m)/8 [tr dot d^2−a^−2 tr(partial d)^2]+[mn−xi0(n+1)]H^2 tr d^2/2}`.

For m<1/2 its exact evolving comoving mode equation has positive kinetic and

`ddot d+nH dot d+[(k/a)^2+mu^2]d=0`,
`mu^2=4[xi0(n+1)−mn]H^2/(1−2m)`.

The stable tensor cone is xi0>=mn/(n+1), with strict inequality supplying a positive mass. Its evolving-mode energy obeys dot E=−nH dot d^2−H(k/a)^2 d^2, so all future modes are bounded; equality gives the bounded massless branches. For example n=3,m=1/4,xi0=1/4 gives kinetic K/16, mu^2=2H^2, and retains the conditional flat radial boost B=3/2. This is a constructive repair of the **regular-slope tensor screen**, not an all-helicity healthy model or a realization of deep MOND.

For the actual auxiliary minimizing source endpoint m=1/2, neither J nor S3 adds tensor kinetic. The corrected unsourced de Sitter equation is algebraic, with coefficient proportional to n/2−xi0(n+1). If that coefficient is nonzero it imposes d=0; if xi0=n/[2(n+1)], the entire relative quadratic block vanishes. Neither case is a positive propagating tensor completion. The missing two-sided invariant definition and auxiliary order-of-limits issues remain independently open. No ghost is inferred merely from the zero coefficient.

At H=0, J has no quadratic TT effect. The regular-slope de Sitter mass repair disappears, exactly as required by the explicit curvature origin. Scalar/vector constraint and Hamiltonian analysis, nonlinear admission, matter coupling, observed tensor propagation and EFT cutoff remain required before any full physical health conclusion.

## Vacuum/source normalization remains independent

On coincident metrics C=0, J=0 and its first metric variation is zero. Thus adding this term does not change the coincident vacuum auxiliary equation, interaction value M(0,T), or the conditional cosmological-constant dictionary. Its leading NR stationarity and radial interpolation kernel likewise survive. Xi0 is an additional dimensionless coupling and the tensor cone is an inequality, not a mechanism fixing lambda or the additive offset. The parent's conditional source moment C_resp(lambda) and UV-offset convention still vary continuously. No equality to32pi is imposed or derived, and no physical Lambda dictionary is imported from the NR moment without the parent's stated covariant assumptions.

## Evidence

checks.py validates the raw five contraction tensor coefficients, exact general-n NR value/first-variation identities, complete finite-n spatial derivative nullspaces, de Sitter boundary identity and corrected evolving Euler equation. Negative controls falsely add critical tensor kinetic, discard the H-dependent raw contraction, or call S5 invisible solely by assertion. These are bounded/exact algebraic evidence; finite dimensions corroborate rather than prove the general-n index statements. provenance.json pins actual input bytes and HEAD. SOURCES.md records exact primary version and inherited source restoration limitations. REPORT is a frozen run input; authoritative run summaries are separate in RUNS.json.
