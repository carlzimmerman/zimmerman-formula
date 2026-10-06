# Evolving radiation transfer of the repaired projected operator

The geometric shared-leaf projector repair changes actual time-dependent scalar solutions on an admitted unequal-scale radiation branch. For the declared compact interval and relative-coordinate seed recipe, the arithmetic operator amplifies the relative mode increasingly at k=400 and800; lambda=1 gives a bounded oscillating response with smaller physical Weyl potentials. A separate repaired k=6 solution crosses the old velocity-chart rank point with finite phase variables and physical potentials. These are bounded linear-transfer demonstrations, not a cold-abundance mechanism, full stability theorem or observational fit.

## Actual branch, operators and canonical equations

Use the pinned covariant shared-leaf action, and the exact parent quadratic radiation reduction with M=2K=1, eta=1/4, Q=1. Visible radiation is the actual minimally coupled C_r Y² control: rho=3a^-4, W=4a^-4. Its homogeneous background is

a=sqrt(sinh(2t)), H=sqrt(1+a^-4), Hdot=−2a^-4,
bdot=L b, L=a³/b³, H2=L, ell=3(H−H2), e=2a^-4/H.

At t0=asinh(1)/2 set a=1,b=2; stop at a=1.5, t1=asinh(2.25)/2. Both scales, lapses and expansions stay positive, and b>a. This is a positive cosmological-constant radiation background, not an EdS surrogate. hhat=1 is a time-unit choice; it fixes Lambda0=3=a0² A/2 on Q=1. It does not determine a0 or A separately. The field kinetic and density normalization C_r q0^4=4 is specified, not selected.

Write P_g=k²/a²,P_h=k²/b²,b0=9 and
A_r=6/a, B=9a³H², D=9a³,
g=a³P_g H, j=a³P_h H2.
The two actual acceleration operators give
Gamma_arith=a³(P_g+P_h)/4,
Gamma_lambda=a³P_g P_h/[(P_g+P_h)(1+lambda delta²)],
delta=(P_g−P_h)/(P_g+P_h), lambda=1.

The repair changes only this quadratic coefficient about the displayed branch. Its homogeneous source and the CY² scalar fluid remain identical. No arithmetic-source fit or QUMOND likelihood is imported into the changed action.

Keep the canonical Hamiltonian from the independently audited raw Legendre transform. Let a_c=p_w−p_chi−2g chi, S=g²/B+j²/D and Z=g a_c/B+j p_chi/D−ell p_chi. Then
u=Z/(2S), n_g=(a_c−2g u)/(2B), n_h=(p_chi−2j u)/(2D),
w_dot=p_w/(2A_r)+n_g+e w,
chi_dot=p_chi/(2Gamma)+ell u−n_g+n_h−e w,
p_w_dot=−e(p_w−p_chi)−2g e w,
p_chi_dot=2g n_g.

The background a,b evolves along with these four phase variables. S>0 and Gamma>0 throughout, so the RHS does not divide by the velocity-chart determinant C_aux. The inherited two physical scalar pairs persist. This exact time-dependent system does not assume instantaneous eigenvalues describe the history. In particular p_chi is generically not conserved: the earlier acceleration-only signed integration mode cannot be silently substituted for these fluid/shear modes.

## Physical metric and radiation reconstruction

Use the same common unitary clock and only one common spatial gauge. The raw fields are
zeta_h=H2 u, zeta_g=H(chi+u), v=w+chi+u,
nu_g=chi_dot+u_dot+e w+n_g,
nu_h=u_dot+ell u+n_h,
t_g=3H n_g/eta, t_h=3H2 n_h/eta.

Our Newton notation is ds²=−(1+2Psi)dt²+a²(1−2Phi)dx²: Phi is spatial curvature potential, Psi is lapse potential. With covariant metric shifts g0i=partial_i beta and e_shear=Delta E,
B_g=(beta_g−a² E_gdot)=t_g/P_g,
B_h=(beta_h−b² E_hdot)/L²=t_h/(L²P_h).

The actual Bardeen combinations are
Phi_g=−zeta_g−H B_g, Psi_g=nu_g+B_gdot,
Phi_h=−zeta_h−H2 B_h, Psi_h=nu_h+B_hdot+ell B_h.
W_g=(Phi_g+Psi_g)/2 and W_h analogously are the physical Weyl potentials. These are separately invariant combinations; they do not simultaneously place both metrics in Newton gauge, which would require two coordinate freedoms. The L² denominator and the hatted ell term are essential, not conventions that can be dropped.

For the actual radiation, v_N=v+B_g and
(delta rho_r)_N=3W(v_dot−H v−nu_g)−3HW B_g,
(delta q_r)_N=−W v_N, delta p_r=delta rho_r/3.

The last pressure relation belongs to the actual ideal radiation. It does not assert that the extra interaction stress is a pressureless component. The radiation conservation check is delta_r_dot+(4/3)P_g v_N−4Phi_gdot=0. transfer.py computes derivatives of analytic rational/square-root functions along the full evolving phase vector by complex-step differentiation; an independent five-point time derivative of the dense trajectory checks this conservation row. Canonical auxiliary/momentum residuals are also retained. This is a physical radiation/Weyl transfer dictionary, not just a plot of an unobservable lapse.

## Seed recipe, bounded comparison and normalization

At a=1,b=2 define r=j/(g+j). In both operators prescribe chi=1,w=−r, chi_dot=w_dot=0. The exact initial auxiliary rows are solved to obtain the compatible canonical momenta, once at the nonsingular initial chart. All subsequent evolution is canonical. This is the same physical-coordinate/velocity recipe w,chi in the same boundary convention; it is NOT identical initial observed radiation density or Weyl data in the two theories. Different operators give different initial lapse/metric/source reconstruction. No inferred observed transfer ratio is claimed.

DOP853 evolves k=400 and800 at rtol=2e−9 and2e−10, atol=rtol*10^-3, with an individual 40000-RHS cap. The interval is the same in all cases. The following unit-column results are from the looser run; tighter runs agree in phase vectors to3.3e−8 and physical vectors to3.3e−8 in the declared normalized max norms.

|k|operator|chi(t1)|max abs(W_g)|W_g(t1)|delta_r(t1)|
|--:|:--|--:|--:|--:|--:|
|400|arithmetic|4.80713|0.681017|−0.681017|3.37468|
|400|lambda1|−0.213314|0.0486543|0.0299078|0.559879|
|800|arithmetic|48.2091|6.84838|−6.84838|27.8891|
|800|lambda1|0.0125094|0.0594562|−0.00160222|0.672995|

For repaired UV cases max abs(chi)=1 over the sampled trajectory, whereas the arithmetic ends at growing values. This is consistent with, but does not replace, the analytic parent sign of the principal frequencies: omega_arith²<0 and omega_lambda²=−lambda omega_arith²>0 when a!=b. Ordinary radiation retains its sound speed squared1/3. Finite duration and these two momenta cannot prove universal boundedness of repaired solutions.

The unit columns are freely scalable. They are not amplitudes at which a nonlinear perturbation remains small. For the illustrative choice a0=1,A=6, multiplying by epsilon=10^-8 makes reconstructed lapse amplitudes small and the computed leading invariant I small (checked against10^-6 on every sampled UV case). For any other fixed a0>0 on this compact finite-k interval, sufficiently small epsilon does the same. This establishes the consistency of using linear columns near the background, not existence of their full nonlinear continuation or higher-order regularity.

## Actual evolving chart crossing

A distinct lambda=1 k=6 trajectory starts with negative det C_aux and ends with positive det C_aux (sampled range about−2929.73 to20508.47). Its canonical phase vector and reconstructed metric potentials remain finite. At rtol=2e−10 DOP853 uses104 RHS calls; Radau independently uses1572 and agrees with the sampled phase and physical vectors to1.7e−10 and4.3e−11 in the declared normalized norms. Weyl remains finite, max abs(W_g) about7.30 for the unit column. This is not a small physical amplitude until scaled.

This evolving discriminant is stronger than freezing an instantaneous matrix at its root. It does not turn the rank crossing into a health theorem: negative instantaneous momentum Hessians, actual canonical mode energies, a cutoff and time-dependent amplification remain distinct questions. The exact canonical regularity theorem comes from S>0 and the nonzero Dirac determinant, not from the finite floating-point samples. Numerical signs/transfer errors here are tested with tolerance and solver comparison, not rigorously certified continuum error bounds.

## Cold implication and missing arrows

The repair removes the arithmetic UV amplification for these actual evolving radiation solutions and supplies a well-defined Weyl/radiation transfer in the tested range. It has not supplied a positive conserved homogeneous cold density. This background still contains only the specified radiation and volume vacuum source. A small positive relative sound speed is dependent on mismatch, eta and lambda, and becomes a wave at sufficiently high k; it is not a material dust abundance or pressureless-growth signature. The coupled radiation perturbations in the table are evolved rather than frozen. There is no matter-era transfer, baryon fraction, thermal-photon transport, atomic recombination calculation or primordial preparation in this package.

The first unresolved implications are full nonlinear/clock admission, finite-k physical stability and an actual early-state/abundance model. A physical EFT cutoff must decide whether the illustrated high-k range is available; the same-action continuum comparison alone supplies no cutoff. Static source corrections of the new projector remain a separate obligation. A, a0/H and32pi remain unselected.

## Bounded evidence

Preflight34,37 and41 check records are retained as development history. Fresh standard runs freeze transfer.py, checks.py, REPORT, provenance and inherited report bytes. The controls replace the repaired coefficient by the arithmetic coefficient or drop L² from the hatted Bardeen shift. The latter breaks gauge invariance; the former fails the declared bounded repaired-relative criterion. Neither is silently pooled as successful evidence. No source theorem or astronomical data is imported; all exact equations come from the pinned parent action and the raw canonical/metric derivations above.
