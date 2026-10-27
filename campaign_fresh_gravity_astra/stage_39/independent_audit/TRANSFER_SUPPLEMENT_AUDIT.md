# Supplementary independent audit: actual-source transfer bootstrap

Normalized claim: for the unchanged full diagnostic Q/scale/isothermal-fluid equations with fixed positive coefficients, a compatible smooth hydrostatic background with rho,g0>0, zero initial field velocities and the exact C1,1 polynomial packet of amplitude N and width ell=N^-3, every fixed B_dagger>15/8 excludes a positive classical whole-packet continuation through dimensionless Theta=B_dagger N^-4 for sufficiently large N, on the stated original neighborhood and common edge cones. The proof derives the transfer budget on any hypothetical surviving branch; it does not classify the earlier endpoint or construct a shock.

Primary verdict: **proved as written**, in that precise diagnostic scope. The new actual-source estimate supplies the transfer input that the earlier frozen FGF052 author proof left unresolved. This is a separate root result, not an author correction or a retroactive change in the accepted author audit.

## Target, source ancestry and exposure

Audited root source: `campaign_fresh_gravity_astra/stage_39/coordinator/ROOT_TRANSFER_BOOTSTRAP.md`, SHA256 `54ca3f4c3b9de4a4db917f23baa5c6bb4c8e94f6068d076035e83611a447905a`. Hash checked before read. The root source was read directly, without reading any other transfer reviewer files or verdicts. This is an independent adversarial audit and reconstruction after exposure to the candidate, not a blind independent discovery of its mechanism.

Dependencies were rehashed against the previously accepted exact bytes: FGF051 DERIVATION `37a88c86cd0ba56c1d30e10d79a68fda0dc2160313ae976712ab39f470418ac3`; FGF052 DERIVATION `3f9b23a5ceba551241db18b93a46e32d4a70974033de9746f96d88fc2b75d628`; reviewer independent derivation `377262c0995702b52c0ad38b41552c0dd614061637a96fcd78a544ea991e3a97`; prior audit result `51c865744fd6d6a7bdc684523a7e70e70f1781551b5f9a199486f73c770279c9`. FGF048 DERIVATION `010afcd5c5de6a1618272511e30371feae09f45195405373e15e68f8beb31de2` is retained only for the separately established short lower time. The original ten ancestry pins were already verified before use in the earlier derivation. No prior file, freeze, verifier or metadata record was changed in this supplement.

## Independent reconstruction of the decisive implication

Use the root's dimensionless variables and fixed dimensionless coefficients. Denote the right endpoint by D, the interval by I=[A,D], and density by n=exp q. All characteristic and conservation statements below concern an already existing classical candidate through the proposed horizon; no continuation theorem is imported.

### 1. Protected endpoints and the initially-positive field chart

The accepted FGF051 branch exists on the edge cones with a uniform positive g margin and bounded local speeds. Choose endpoint offsets d N^-7/2 and exterior subcone radii smaller than the offset and the protected-strip margin. The original data on those exterior bases are exactly hydrostatic. Their cone shrinkage over Theta is O(N^-4), strictly smaller than their O(N^-7/2) radii for sufficiently large N. The homogeneous characteristic difference identity therefore identifies the local edge branch with hydrostatics there. Potentials agree as well because their time derivatives vanish and their initial values agree.

There is a minor logical point worth making explicit, not an extra hypothesis: the root assumes a hypothetical whole branch has g>0 initially and proposes to exclude later chart exit. To obtain its endpoint traces one can first propagate comparison with the known edge branch separately on the common edge cones. On the initial short slab positivity holds by continuity. On every compact slab before a first possible g=0 contact, FGF051's comparison applies. Equality to the known edge branch retains its strictly positive margin up to that putative contact, contradicting it by continuity. Thus no g=0 contact can obstruct this edge comparison while the candidate is classical. This uses the existing edge theorem and local uniqueness, not the later interval field estimate. The interval bootstrap can then use exact endpoint traces without circularly assuming its own conclusion. Positivity outside the interval and these common comparison cones is not needed for the estimates.

### 2. Fluid lower bounds and the low-velocity density cap

Within a fixed compact field-state bootstrap, let |g|<=Gbar and |lambda_Q|<=Lambda. The exact fluid invariants r=v+cq and s=v-cq solve transport equations with source -g. A backward characteristic from any point of the compact classical slab either reaches the initial slice or its first lateral boundary contact. Until that stop it remains inside I. For each fixed N classical regularity bounds its speed on the slab, so the path exists to that stop; no uniform-in-N velocity or derivative bound is needed. If a path only approaches the boundary at a limiting stopping time, continuity supplies the same trace. Initial invariants are at least -c Q0 because v_initial>=0, and lateral invariant values are plus/minus c log rho. Integration for t<=1 gives both r,s>=-L0 with L0=c Q0+Gbar.

It follows that v=(r+s)/2>=-L0. If v<=Vcut=Lambda+1, then for fixed sum r+s=2v and lower bounds r,s>=-L0,

    |r-s|<=2(v+L0), hence |q|<= (v+L0)/c <=(Vcut+L0)/c.

Therefore n<=Ncut=exp((Vcut+L0)/c) throughout the actual low-velocity set. The bound is finite and independent of N, although it may be very large for a particular fixed coefficient cell. No initial-profile formula is imposed on the later low-velocity set. The argument includes acoustic/Q coincidences and all later crossings without dividing by relative speed.

### 3. Source control along an arbitrary actual Q path

Exact stationary traces give nv(A)=nv(D)=0 and conserved M=int_I n=int_I rho<=C_M ell. Define the actual cumulative mass m(t,X)=int_A^X n. Continuity gives m_t=-nv and m_X=n; consequently along either Q path X'=lambda, |lambda|<=Lambda,

    d_t m=-(v-lambda)n, with 0<=m<=M.

The characteristic is stopped at its initial or first backward lateral contact s0 and integrated to its terminal t. On H={v>Lambda+1}, v-lambda>1. On L={v<=Lambda+1}, the preceding density bound holds, and -L0<=v<=Vcut implies |v-lambda|<=Ccut=Lambda+max(L0,Vcut). Integration over the complete path, including all components of H and L, gives

    int_H(v-lambda)n
       =m(s0)-m(t)-int_L(v-lambda)n
       <=M+Ccut Ncut(t-s0).

Since int_H n<=int_H(v-lambda)n and int_L n<=Ncut(t-s0),

    int_s0^t n <=M+(Ccut+1)Ncut(t-s0).

This is the critical estimate. Measurable splitting of an ordinary time integral suffices; there is no finite-crossing premise. A path can enter and leave H infinitely often, or spend a positive time interval at the cutoff. Assigning the cutoff itself to L preserves every bound. The derivation charges the mass range once for the complete path, not once per high-speed component. Negative contributions of v-lambda on L are bounded by the already established low-speed density cap, so oscillatory mass recycling is explicitly accounted for. Initial stops can have any m between 0 and M; lateral stops have m=0 or M. The same bound covers both.

### 4. Compact field closure without density or derivative suprema

The actual Q diagonal equations have sources H_regular(z)-C n/tau. The two scale sources depend only on z, and chi_t=w. Coordinates k and w are included in z, so their appearances in H_regular are controlled state factors, not hidden derivatives of z. No q_x,n_x or v_x occurs.

On a chosen compact neighborhood of z*=z0(0), all regular sources, characteristic speeds and inverse chart functions are bounded. Initial data and exact lateral traces differ from z* by O(ell). Every field characteristic can be stopped at its initial/lateral contact just as above. The Q source integral then gives

    |R_±-R_±*| <= C0 ell+Hbar t+(C/tau)[M+(Ccut+1)Ncut t].

Scale characteristics give |Z_±-Z_±*|<=C0 ell+Zbar t, and the vertical chi equation gives |chi-chi*|<=C0 ell+Wbar t. Therefore sup_I|z-z*|<=C1 ell+C2 t. All constants depend only on the fixed background/coefficient neighborhood. Taking the bootstrap ball small enough inside the chart and then N large makes this bound <delta/2 for every t<=Theta. A first exit of the compact ball is impossible. The inverse chart keeps g uniformly positive, a bounded away from zero and above, and g uniformly bounded throughout the interval.

This is an amplitude bound only. It neither needs nor supplies a bound on first derivatives uniformly up to an actual singular endpoint. If the candidate is classical on the closed hypothetical slab, those derivatives are finite for that fixed N, sufficient for all path constructions. Classical failure earlier already precludes the assumed survival, so no high-norm restart is required by this contradiction argument.

### 5. Actual transfer and strict moment capacity

The complete momentum identities already derived from the actual equations give physical-sign field momentum F=-C^-1 int(tau p g+sigma w k), P+F=P0 and

    F'=int_I(ng-rho g0), F(0)=0.

The boundary pressure difference contributes int rho g0; it is not silently discarded. Since n>0, int n=M and |g|<=Gbar on the now-closed bootstrap,

    |F'|<=M(Gbar+G0),
    |F(t)|<=M(Gbar+G0)t,
    |int_0^Theta F|<=M(Gbar+G0)Theta^2/2.

With M=O(N^-3) and Theta=O(N^-4), the last bound is O(N^-11). This estimate is derived from actual dynamics and is stronger than needed; it is not inferred from the small total energy. The frozen earlier O(N^-5) energy estimate remains correct but is not the relevant bound here.

For I1=int X n, strict density positivity yields I1<D M. The identity I1(Theta)=I1(0)+P0Theta-int F, the exact integral int f=16/15, and smooth-background endpoint errors give P0/(MN)->8/15 and R0/(M ell)->1, R0=D M-I1(0). Hence

    (P0Theta-R0-M(Gbar+G0)Theta^2/2)/(M ell)
      ->(8/15)B_dagger-1>0,

because Theta^2/ell=B_dagger^2 N^-5. The lower bound forces I1(Theta)>D M for sufficiently large N, a contradiction. There is no equality ambiguity: the proof uses a strict positive margin at fixed B_dagger>15/8. It asserts nothing at B_dagger=15/8. All large-N requirements are simultaneous finite inequalities in fixed constants, including the exterior-cone margin, t<=1 and the compact-bootstrap margin; a potentially large fixed Ncut only enlarges the threshold.

## Dependency and obligation matrix

| Obligation | Evidence | Status |
|---|---|---|
| Original exact Q/scale/fluid equations and packet | pinned FGF051/052 sources | passed |
| Protected exact endpoint traces | edge theorem plus exterior uniqueness | passed |
| Initial-only g>0 versus edge comparison | first-contact continuation of local equality | passed |
| Fluid characteristic initial/lateral stops | compact classical slab and continuous traces | passed |
| Lower r,s bounds with pressure retained | direct invariant integration | passed |
| Actual low-velocity density bound | fixed-sum algebra | passed |
| Actual cumulative-mass derivative on both Q families | continuity and no-flux boundary | passed |
| Arbitrarily many high/low crossings and resonances | single integrated identity, measurable split | passed |
| Field initial/lateral source integration | exact diagonal equations | passed |
| Closed compact bootstrap and g margin | strict C1 ell+C2 t improvement | passed |
| Actual signed transfer bound | mass plus bounded actual force | passed |
| First-moment contradiction at B_dagger>15/8 | explicit profile integral and strict capacity | passed |
| Full energy and both field fluxes | unchanged accepted exact balances | passed |
| Zero-velocity control | exact substitution | passed |
| Both a0 normalizations and history/model separation | fixed coefficient/background branches | passed |
| Endpoint classification or continuation after breakdown | no such implication claimed | out of scope |

Graph: pinned edge theorem -> exact traces -> mass conservation and path stopping data. Compact field bootstrap -> bounded g -> fluid lower invariants -> low-speed density cap; mass conservation + cap -> complete Q path source bound -> strict compact field improvement. The bootstrap is logically closed by continuity, not circularly assumed at the conclusion. Closed field amplitudes -> actual force-transfer bound -> accepted moment identity -> non-survival horizon. No external theorem or numerical-computation leaf enters this graph.

## Controls, physical scope and remaining implications

The zero-velocity hydrostatic tuple remains an exact solution. It has P0=P=F=0, constant moment and conserved mass. It satisfies the lower-invariant and characteristic-source inequalities, but lacks the positive P0/(MN)->8/15 limit; therefore the contradiction does not apply to it. The proof never treats the source bound alone as a blow-up criterion.

Dimensionless constants 1 and Lambda in Vcut refer to the fixed velocity unit v0, not an added physical coefficient. Restore g by v0^2/L, mass by nref L, momentum by nref L v0 and first moment by nref L^2. The restored bound M_physical(Gbar_physical+G0_physical)T^2/2 has first-moment units. Both a0=9.3619e-11 and 1.1279e-10 m/s^2 require their own compatible backgrounds and constants. Constant vacuum and separately frozen a0 E(z), E^2=.315(1+z)^3+.685, remain distinct fixed-reference branches. Evolving reference generally removes stationary exterior data and adds protocol work, and is excluded. Q, RAR, registered M and filtered MONO remain distinct.

No missing implication remains for this particular diagnostic upper-horizon theorem. Still unproved and not implied are the nature of the earlier breakdown, sharpness of 15/8, survival to that coefficient, weak/post-breakdown solutions, full-cone gradient control, or physical metric/photon/vacuum/two-DOF completion, criterion B, calibration, cosmology, novelty and theory closure. Combining the theorem with the separately accepted small FGF048 lower interval is permissible only with each theorem's original constants and domains.

The preserved failed routes remain failures: unsigned energy alone, continuity without momentum for the low-speed trace, mass charged separately to every high-speed excursion, and unproved future-resonance confinement. The candidate avoids each with an explicit new argument. No actual PDE counterexample is asserted.

Verification was proof-only. Six needed file hashes were checked by a read-only Python SHA256 loop and all matched; no mathematical executable computation, literature lookup or new metadata-verifier execution was performed. Conservative self-review covered this whole supplement for signs, units, quantifiers, path stopping and scope; no frozen source edits or mathematical-token corrections were made. The exact input map and output hash are in the separate new TRANSFER_SUPPLEMENT_RESULT.json.
