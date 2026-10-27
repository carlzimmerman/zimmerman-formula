# Independent adversarial audit of the FGF052 transfer bootstrap

## Normalized claim and primary verdict

**Verdict: proved as written.** Fix the full autonomous diagnostic Q/scale/isothermal-fluid equations, all positive coefficients and either fixed positive reference acceleration, and a smooth compatible hydrostatic background with positive density and initial field gradient. Keep the exact C1,1 packet stated in FGF052. For each fixed B_dagger>15/8, sufficiently large N admits no positive classical whole-packet continuation through T=B_dagger(L/v0)N^-4 on the stated background neighborhood and comparison cones. This is a non-survival conclusion; it constructs neither a shock nor a continuation beyond breakdown. The proof's field-chart exit argument is part of the conclusion, not an added uniform-field hypothesis.

Reviewer: `/root/fgf052_transfer_audit`, dispatched as a fresh adversarial reviewer without an author verdict. Only this audit directory is modified. The candidate and raw FGF051 equations were read first; the key fluid, mass-coordinate, and field-source implications were reconstructed before reading the optional FGF052 moment derivation. No other new stage39 review or coordinator verdict metadata was read. The optional raw moment derivation contains its own older conditional verdict; that is not evidence for the new transfer estimate. Its hash was independently checked after reading, before its algebra was adopted in the final audit. All ten task ancestry pins and the candidate hash were checked before their source use. No literature or numerical experiment was used.

## Source pins and dependency graph

The authoritative candidate is `campaign_fresh_gravity_astra/stage_39/coordinator/ROOT_TRANSFER_BOOTSTRAP.md`, SHA256 `54ca3f4c3b9de4a4db917f23baa5c6bb4c8e94f6068d076035e83611a447905a`.

The raw equation/local-edge dependency is `deepseek_push/astra_spawn_ideas/fresh_gravity_followups/results/FGF-051/fgf051_run_001/DERIVATION.md`, SHA256 `37a88c86cd0ba56c1d30e10d79a68fda0dc2160313ae976712ab39f470418ac3`.

The independently inspected raw moment dependency is `campaign_fresh_gravity_astra/stage_39/independent_audit/INDEPENDENT_DERIVATION.md`, SHA256 `377262c0995702b52c0ad38b41552c0dd614061637a96fcd78a544ea991e3a97`.

Task FGF052 SHA256 is `d368f8c60bf9d3bf112c50c3eafc77b3e083c76d0b7fc7c64bf8b178545b2fa1`; framework SHA256 is `ff0d2873065578b0bd8aa50907e0a39495ff8da775bf2b4890768d83775fd750`; result contract SHA256 is `ba388d0ca8e447a38649a478483e3ff4c2d3293e842eedc8f035499c77a20c29`. The JSON records all ten verified ancestry hashes. The current Git HEAD was `c1449c08768f6ea7553ea0ecbc7c6653f4651bb8`; exact source bytes, not HEAD, identify the evidence.

The dependency graph is acyclic:

1. Pinned FGF051 local edge construction and comparison + unchanged exterior initial data -> exact stationary exterior subcones -> hydrostatic endpoint traces.
2. Actual equations + a provisional compact field chart + endpoint traces -> lower bounds for both acoustic invariants -> a density cap on the actual low-velocity set.
3. Continuity + zero endpoint matter flux + positivity -> conserved mass and a bounded mass primitive -> one integrated Q-source estimate on each entire characteristic tail.
4. That source estimate + bounded regular field sources -> strict improvement of the provisional field chart -> actual uniform force bound throughout the interval.
5. Actual momentum identities + that force bound -> small weighted field-momentum transfer -> first-moment contradiction at every fixed B_dagger>15/8.

There is no energy coercivity leaf, external theorem leaf, numerical leaf, assumed density-gradient estimate, or assumed control of future resonance locations. FGF051 is an inherited internal theorem, inspected in raw form here but not independently reconstructed in every local-existence detail.

## Independent reconstruction of the critical objects

Use the dimensionless variables of FGF051: X=(x-x*)/L, theta=v0 t/L, n=n_physical/nref, q=log n, ell=N^-3. The equations are

    n_theta+(nv)_X=0,
    v_theta+v v_X+c^2 q_X=-g,
    tau p_theta=B_X-Cn,  g_theta=p_X,
    sigma w_theta=J k_X+Tscale-U',  k_theta=w_X, chi_theta=w.

Here a=a_ref exp chi, B=(sqrt(a^2+4g^2)-a)/2, W_g=B, Tscale=-W_chi. All coefficients in these displayed equations are the fixed dimensionless coefficients; C is not silently replaced by its physical value. Hydrostatics gives B0_X=C rho, c^2 rho_X=-rho g0, and J k0_X+Tscale0-U'=0.

For g>0, B_g=2g/sqrt(a^2+4g^2)>0, b=sqrt(B_g/tau), h_g=b. Let R_+=p+h, R_-=p-h and Z_+=w+d_s k, Z_-=w-d_s k, where d_s=sqrt(J/sigma). The map to z=(R_+,R_-,Z_+,Z_-,chi) is locally invertible because h_g>0 and d_s>0. Direct chain rule, including chi_X=k, gives

    (partial_theta-b partial_X)R_+
       =B_chi k/tau+h_chi(w-bk)-Cn/tau,
    (partial_theta+b partial_X)R_-
       =B_chi k/tau-h_chi(w+bk)-Cn/tau,
    (partial_theta-d_s partial_X)Z_+
       =(partial_theta+d_s partial_X)Z_-=(Tscale-U')/sigma.

Thus the only potentially unbounded matter forcing in either Q equation is the actual density term -Cn/tau. In a fixed compact chart, g,b,k,w,chi and the remaining sources are bounded. k and w are components recovered from z, so bounding these terms does not assume control of z_X. Neither a static-source substitution nor a division by relative characteristic speed occurs.

Pressure is retained by r=v+cq and s=v-cq:

    (partial_theta+(v+c)partial_X)r=-g,
    (partial_theta+(v-c)partial_X)s=-g.

## Boundary and characteristic-domain checks

Choose A=-ell-d N^-7/2 and D=ell+d N^-7/2 with 0<d<R_i. Choose 0<r<min(d,R_i-d)/2. Exterior bases of radius r N^-7/2 around A and D lie outside the packet and inside the protected edge strips. With S_h larger than the constructed edge and stationary characteristic speed bounds, their radii at theta are r N^-7/2-S_h theta. For theta<=B_dagger N^-4, both the edge-time gate and buffer gate hold for sufficiently large N:

    B_dagger N^-1/2 < k_edge,
    S_h B_dagger N^-1/2 < r.

Local comparison on these contained cones gives exact equality with the stationary solution, not an O(theta) approximation. To see why a fast hypothetical core does not invalidate this, use characteristics of the bounded constructed comparison solution. The difference equation contains coefficient differences multiplied by the other solution's finite first derivative. On each fixed-N compact comparison interval this gives D(theta)<=K_N int_0^theta D(u)du, forcing D=0. K_N need not be uniform. Initial positivity permits this comparison in the chart; a hypothetical first chart exit on the comparison cone is excluded by equality before that exit. Hence the traces really are n=rho,v=p=w=0,g=g0,chi=chi0,k=k0,phi=phi0.

Inside I=[A,D], each backward fluid or Q characteristic is used only on its maximal connected tail contained in I. That tail begins at theta=0 or its first backward lateral contact. Classical regularity supplies a finite velocity bound for each fixed N on any compact time slab, so the ODE cannot terminate inside I without reaching one of those sets. Tangential contacts cause no difficulty: stop at that contact and use its known trace. Re-entry outside I is never followed. No inflow sign needs to be imposed because actual solution traces, rather than freely specified boundary data, are being used.

## Acoustic lower bounds and all repeated crossings

Provisionally assume z stays within a fixed delta ball around z*=z0(0), with a larger chart neighborhood and g bounded away from zero. Let |g|<=Gbar and |lambda_Q|<=Lambda there. Let Q0 bound |log rho| on the fixed initial neighborhood. Initial v>=0, while lateral v=0. Integration of each acoustic equation from its initial/lateral contact gives, for theta<=1,

    r>=-L0, s>=-L0,  L0=c Q0+Gbar.

Consequently v>=-L0. If v<=Vcut=Lambda+1, write r+L0,s+L0>=0; then

    2c|q|=|r-s| <= r+s+2L0=2(v+L0),
    n<=Ncut=exp((Vcut+L0)/c).

This bounds density on the actual low-velocity set without bounding its geometry, its number of components, or a fluid gradient. The constants may be large when c is small, but c>0 is fixed independently of N, which suffices. A pressureless limit is not claimed.

Zero matter flux at the endpoints gives constant M=int_A^D n=int_A^D rho. Define m(theta,X)=int_A^X n. Then

    0<=m<=M, m_X=n, m_theta=-nv.

Along either actual Q characteristic gamma with speed lambda=+/-b,

    d m(theta,gamma(theta))/dtheta=-(v-lambda)n.

On its whole contained tail [s0,t], let H={v>Vcut} and L={v<=Vcut}. On H, v-lambda>1. On L, n<=Ncut and |v-lambda|<=Ccut=Lambda+max(L0,Vcut). Absolute continuity of the mass primitive along the path gives the single identity

    int_H (v-lambda)n
       =m(s0,gamma(s0))-m(t,gamma(t))-int_L(v-lambda)n
       <=M+Ccut Ncut(t-s0).

It follows that

    int_s0^t n(theta,gamma(theta))dtheta
       <=M+(Ccut+1)Ncut(t-s0).

This is valid even if H and L have infinitely many connected components. The positive part is bounded through one telescoping endpoint difference; M is not charged anew for every crossing. Resonance v=lambda, when present, belongs to L and has bounded density. No crossing-count, path Jacobian, or resonance-confinement premise is hidden here.

## Closing the compact chart without derivative control

Smooth fixed initial and endpoint data differ from z* by at most C0 ell. Also M<=C_M ell for all sufficiently large N. Integrating the Q equations from the first contact gives

    |R_+/- -R_+/-*|
       <=C0 ell+Hbar t+(C/tau)[C_M ell+(Ccut+1)Ncut t].

The scale equations give |Z_+/- -Z_+/-*|<=C0 ell+Zbar t. The vertical equation gives |chi-chi*|<=C0 ell+sup_K|w|t. In the maximum norm this yields

    sup_I |z-z*|<=C1 ell+C2 t

with fixed constants. Choose N sufficiently large that the initial data lie strictly in the delta ball, the edge and buffer gates above hold, theta<=1, and

    C1 N^-3+C2 B_dagger N^-4 < delta/2.

Every provisional interval then improves the bootstrap to delta/2. Continuity rules out a first exit while the hypothetical classical branch exists through the stated horizon. Since the delta ball has a positive g margin, g=0 cannot furnish an escape from the argument. This is a conditional a priori estimate on a hypothesized existing classical solution, not a claim that bounded amplitudes extend its derivatives or guarantee its existence. No restart or uniform derivative bound is needed.

## Momentum, moment and units

Direct differentiation gives Q and scale momentum densities and stresses

    mQ=-tau pg/C, SQ=(tau p^2/2+gB-W)/C,
    mS=-sigma wk/C, SS=(sigma w^2/2+J k^2/2-U)/C,
    (mQ)_theta+(SQ)_X=ng+Tscale k/C,
    (mS)_theta+(SS)_X=-Tscale k/C.

Indeed (gB-W)_X=g B_X+Tscale k, which fixes the interaction sign. Combining with (nv)_theta+(nv^2+c^2n)_X=-ng gives exact total momentum conservation. Hydrostatics implies (SQ0+SS0)_X=rho g0 and (c^2rho)_X=-rho g0, so the endpoint total stresses agree. Defining P=int nv and F=int(mQ+mS), one obtains

    P+F=P0, F(0)=0,
    P'=-int(ng-rho g0), F'=int(ng-rho g0).

The pressure term is -c^2[rho]=int rho g0. It is generally nonzero, and omitting it would fail the stationary control. Individual Q and scale boundary stresses need not vanish.

With the actual |g|<=Gbar and fixed |g0|<=G0, positivity and conserved M give

    |F(t)|<=M(Gbar+G0)t,
    |int_0^Theta F(t)dt|<=M(Gbar+G0)Theta^2/2.

For I1=int Xn, stationary endpoint flux gives I1'=P. Positivity gives I1(Theta)<DM. Put R0=DM-I1(0)>0. Then the exact weakest scalar sufficient moment gate is int_0^Theta F<=P0 Theta-R0, including equality. The candidate proves a stronger absolute bound.

For H=ell+d N^-7/2, elementary integration gives int_-1^1 f=16/15 and int_-1^1 y f=0. Taylor expansion of the fixed smooth rho gives

    M=2rho*H+O(H^3),
    I1(0)=(2/3)rho'_*(H^3)+O(H^4),
    P0=(16/15)rho* N ell+O(N ell^3).

Thus P0/(MN)->8/15 and R0/(M ell)->1. At Theta=B_dagger N^-4,

    [P0 Theta-R0-M(Gbar+G0)Theta^2/2]/(M ell)
       ->(8/15)B_dagger-1>0,

because Theta^2/ell=B_dagger^2 N^-5. The proved weighted transfer is O(N^-11), while the strict-margin moment capacity is O(N^-6). The endpoint-width error is O(N^-1/2) relative to the leading capacity and vanishes at every fixed positive margin. Nothing here establishes the equality case B_dagger=15/8.

Physical restoration multiplies mass by nref L, momentum by nref L v0, first moment by nref L^2, force by v0^2/L, and time by L/v0. Accordingly

    |int_0^T F_physical dt|
       <=M_physical(Gbar_physical+G0_physical)T^2/2

has units density times length squared, matching P0_physical T and the moment capacity. The factors C,tau,sigma remain in the definition of F and its exact balance; they are not discarded.

## Controls, obligation matrix, and limits

The complete energy density is nv^2/2+c^2 n(log n-1)+n phi+(tau p^2/2+W+sigma w^2/2+J k^2/2+U)/C. Its flux is nv(v^2/2+c^2 log n+phi)-(pB+Jwk)/C. Matter plus interaction exchanges +np, Q exchanges -np-Tscale w/C, and scale exchanges +Tscale w/C. Hence energy is conserved on this fixed interval with its exact zero endpoint flux. The transfer estimate does not infer any gradient norm from this energy.

The zero-velocity hydrostatic control has P0=P=F=0 and constant mass/moment, including all pressure and field stress cancellations. Its positive initial capacity prevents the moment contradiction. Both fixed references 9.3619e-11 and 1.1279e-10 m/s^2 are admitted separately with their own compatible backgrounds and constants. Each separately frozen a0 E(z) is another autonomous parameter choice, distinct from constant vacuum. An evolving reference is excluded because it changes the exterior stationarity and adds protocol work. Q, RAR, registered M and filtered MONO are not identified.

| Obligation | Status | Decisive evidence |
|---|---|---|
| Task ancestry and exact candidate bytes | passed | All ten task pins and candidate pin match |
| Actual dynamic Q/scale/fluid definitions | passed | Direct characteristic reconstruction above |
| Exact C1,1 joins and fixed coefficients | passed | Unchanged source data; no smoothing or retuning |
| Protected exterior endpoint traces | passed | Strict subcone buffers and local uniqueness |
| Initial/lateral characteristic origins | passed | Stop at first contact on contained tail |
| Pressure in density cap | passed | Both acoustic invariants, c>0 fixed |
| Low-velocity density bound | passed | Nonnegative r+L0 and s+L0 |
| Both Q source integrals | passed | One bounded mass primitive identity per path |
| Repeated crossings and resonance points | passed | Measurable whole-path split, no segment count |
| Compact chart and g positivity | passed | Strict delta/2 first-exit improvement |
| Derivative or existence circularity | passed | Assumed classical continuation only; no restart |
| Matter, Q and scale momentum signs | passed | Direct stress/exchange algebra |
| Boundary pressure and stress cancellation | passed | Total hydrostatic stress constant |
| Initial integrals, width and density errors | passed | Polynomial integration and Taylor bounds |
| Actual weighted transfer and moment gate | passed | O(N^-11) bound versus strict O(N^-6) margin |
| Units and fixed B_dagger quantifier | passed | Physical restoration; N may depend on B_dagger |
| Energy and hydrostatic negative control | passed | Exact balances, no false control contradiction |
| Both reference branches and model distinctions | passed | Separate fixed parameter/background choices |
| Equality threshold, endpoint classification, physics closure | out of scope | Not asserted or proved |

**Smallest remaining gap in the audited claim: none identified.** The strongest safe statement is the normalized non-survival theorem above, for each fixed strict B_dagger>15/8 and sufficiently large N. There is no uniform quantitative N threshold over all coefficient/background choices, no pressureless limit, no endpoint classification, and no physical/empirical completion. A different outcome would require a counterexample to one of the explicit exact identities or a failure of the pinned local-edge dependency; no such defect was found. The cheapest next check for downstream reuse is to preserve the two acoustic lower bounds and the whole-path signed mass identity verbatim, since replacing either with continuity alone or summing per-crossing budgets would invalidate the mechanism.

Zero mathematical executable computations were performed. Executed shell/Python operations read files, discovered instructions, checked SHA256 pins, retrieved Git metadata, and wrote/validated these artifacts. They do not constitute finite-range evidence. No external source was consulted and no additional agents were spawned.
