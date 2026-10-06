# Independent evolving-radiation transfer audit

Primary verdict: **computationally verified in the stated bounded range, conditional on the pinned quadratic action and its admitted radiation branch**. The evolving canonical equations, physical metric/fluid dictionary and regular chart-crossing mechanism agree with independent reconstruction. Exact canonical regularity is analytical under the declared positive coefficients; the table and operator comparisons are bounded numerical evidence, not a general stability, abundance or observational theorem.

Pins: REPORT.md SHA256 `ca3eaa375991e60383e00738145d8b7dff12b662ef17c49efc710feb8e1fccc6`; transfer.py `5198f96167044f534eb75f6623ad97be9b5688005338b91912246b8e62f45f4b`; checks.py `c96433d62ea6285cfc6e8d041e681c70d5ac4501e720409fb9ff43d70b78f897`. The actual shared-leaf action, radiation reduction and canonical-rank parent reports listed in provenance were read. No author inputs were changed or imported as proof; no new source simulations were run for this peer.

## Exact background and coefficient reconstruction

The common foliation is timelike in both homogeneous metrics, but the metrics are unequal. The Q=1 branch has N_visible=1, L=a³/b³, visible rho=3a^-4, W=4a^-4, empty hatted ordinary matter and proper hatted expansion one. Independent Friedmann/fluid relations give H²=1+a^-4, Hdot=−2a^-4 and a=sqrt(sinh(2t)). The hatted equation gives bdot=Lb=a³/b², hence partial_t(b³)=3a³ and ell=Ldot/L=3(H−H2), H2=L. Positive a,b,L and b>a hold on the specified compact interval from a=1,b=2 to a=1.5. This is a radiation-plus-positive-volume-vacuum branch, not a coincident mirrored-fluid branch or matter-dominated preparation.

With M=1, eta=1/4 and b0=9, the parent's actual coefficients reduce to A_r=(3/2)a³W=6/a, B=9a³H² and D=9b³H2²/L=9a³. Likewise g=a³P_g H and j=L b³P_hH2=a³P_hH2. The arithmetic Gamma is a³(P_g+P_h)/4. Direct shared-leaf inversion for the isotropic unequal scales gives Gamma_lambda=a³P_gP_h/[(P_g+P_h)(1+lambda delta²)], delta=(P_g−P_h)/(P_g+P_h). The code uses exactly lambda=1. It changes the quadratic relative lapse-gradient coefficient, not the homogeneous action, ordinary CY² fluid or already-derived reference boundary conventions. Units hhat=1 fix Lambda0=3, not A or a0 individually.

## Canonical equations before chart inversion

The pinned raw reference action is

L=A_r(Tw−ng)²+Bng²+Dnh²+2g(u+chi)ng+2j u nh
 +Gamma(Y−ell u+ng−nh)²−g e w²,
Tw=wdot−ew, Y=chidot+ew.

Retaining the auxiliaries, its Legendre momenta are pw=2A_r(Tw−ng), pc=2Gamma(Y−ell u+ng−nh). Therefore the Hamiltonian is

Hbase+ac ng+pc nh+ell pc u−Bng²−Dnh²−2g u ng−2j u nh,
Hbase=pw²/(4A_r)+pc²/(4Gamma)+ew(pw−pc)+ge w²,
ac=pw−pc−2g chi.

Independent stationary auxiliary variation yields ac−2Bng−2g u=0, pc−2Dnh−2j u=0 and ell pc−2gng−2jnh=0. Solving these gives precisely S=g²/B+j²/D>0, Z=g ac/B+j pc/D−ell pc, u=Z/(2S), ng=(ac−2gu)/(2B), nh=(pc−2ju)/(2D).

Envelope differentiation of that raw Hamiltonian gives the code's four phase rows: wdot=pw/(2A_r)+ng+ew; chidot=pc/(2Gamma)+ell u−ng+nh−ew; pwdot=−e(pw−pc)−2ge w; pcdot=2gng. In particular pc is not generally conserved. No time-dependent coefficient derivative has been erased: a,b and all rates are evaluated along the evolving trajectory, and any requested observable derivative is along the same phase RHS.

A,B,D,Gamma,S stay positive on this finite interval and k>0, so these phase rows never divide by det Caux. The inherited six second-class auxiliary constraints have nonzero canonical determinant. The velocity Hessian can fail as a coordinate chart without losing a canonical pair. Linear ODE coefficients remain smooth on this compact domain; the phase solution and its reconstructed observable derivatives are finite. This argument is independent of the numerical root sampling and does not prove energy positivity or nonlinear full-theory constraint admission.

## Bardeen metric and actual radiation source dictionary

The auxiliary definitions imply zeta_g=H(chi+u), zeta_h=H2u and v=w+chi+u. Using Hdot/H=−e and H2dot/H2=ell recovers nu_g=chidot+udot+ew+ng, nu_h=udot+ell u+nh. The actually varied shift rows give tg=3Hng/eta, th=3H2nh/eta.

For covariant metric shift beta and e_shear=Delta_coordinate E, tg=P_g(beta_g−a²Edot_g). Thus B_g=tg/P_g. The hatted combination must be B_h=(beta_h−b²Edot_h)/L²=th/(L²P_h). A common time displacement T sends B_g,B_h to B_g+T,B_h+T, while zeta_h -> zeta_h−H2T and nu_h -> nu_h−Tdot−ell T. It follows directly that

Phi_g=−zeta_g−HB_g, Psi_g=nu_g+Bdot_g,
Phi_h=−zeta_h−H2B_h, Psi_h=nu_h+Bdot_h+ell B_h

are invariant combinations. Omitting L² would give B_h a spurious L²T shift, which the control correctly detects. These two invariant pairs do not assert two simultaneous independent Newton-coordinate gauges. Their half-sums are the declared linear physical Weyl potentials of each metric.

The actual radiation action rho=3C_r q⁴/4, W=C_r q⁴ and qdot/q=−H implies delta rho=3W(vdot−Hv−nu_g), delta q=−Wv, delta p=delta rho/3. Newton-gauge reconstruction uses v_N=v+B_g and rho_N=delta rho+rho_dot B_g=3W(vdot−Hv−nu_g)−3HWB_g. This agrees with the implementation. It also gives the radiation Euler identity

vdot_N−H v_N=Psi_g+delta_r/4,

where delta_r=rho_N/rho; its two sides agree algebraically because 3W=4rho. Continuity delta_r_dot+(4/3)P_gv_N−4Phi_gdot=0 is the additional independent dynamical row checked from the evolved trajectory. Its sign follows from delta T^0_i=−W partial_i v_N, not an imported cold-fluid stress prescription.

The code's complex-step directional derivatives use smooth rational/square-root functions on positive coefficients. They are floating arithmetic derivative evaluations, not exact interval certificates. The independent five-point dense-trajectory continuity test is a useful orthogonal bounded check; it is not an exhaustive full covariance/EFE/source proof.

## Initial preparation and numerical coverage

The initial recipe chi=1,w=−j/(g+j), chidot=wdot=0 is solved with the actual velocity auxiliary rows once at a nonsingular initial chart. The recovered momenta then satisfy the canonical Legendre equations. Gamma differs between operators, so their initial reconstructed lapse/radiation/Weyl data need not agree. The report correctly calls this a common coordinate/velocity recipe, not matched observed initial data or a measured enhancement ratio.

Actual high-k columns at k=400,800 evolve from a=1 to1.5 at two DOP853 tolerances, each with a40000-RHS guard. Reported chi endpoints 4.8071281 and48.209068 for arithmetic versus−0.21331365 and0.012509416 for lambda1 match the retained results. The displayed Weyl endpoints likewise match−0.68101656,−6.8483819 versus0.029907781,−0.0016022233. This is the actual evolving system with perturbing radiation, not a frozen principal matrix. Normalized phase/observable tolerance comparisons and canonical residual checks cover these seeds/intervals. Maxima are maxima over401 sampled dense-trajectory times; no uniform continuum peak bound or physical EFT availability is certified.

For k=6 the repaired canonical solution samples both signs of the old velocity-chart determinant, about−2929.73 to20508.47. DOP853 and Radau use104 and1572 RHS calls; their finite phases and physical vectors agree at the reported tight normalized tolerance. This verifies the chosen crossing trajectory, consistent with the exact S>0 canonical argument. It does not convert a crossing into all-wavelength health. The unit Weyl column can exceed one; it is not a physical small nonlinear perturbation unless scaled. The stated epsilon example controls sampled reconstructed lapse/invariant values, while sufficient small scaling on a compact regular linear domain follows from bounded linear coefficients. Neither assertion supplies a full nonlinear continuation or cures the inherited relative norm-cube regularity problem.

## Standard records, verdict and missing implication

Independently validated main_a, control_operator_a and control_hat_a against current frozen input hashes using validate_manifest.py --root /Users/carlzimmerman/new_physics/zimmerman-formula. Each returned exit0 and `valid evidence record; mathematical interpretation requires review`. Main is41/41. The operator mutation is39/41 with precisely the two declared repaired-relative bounded tests failing. The hatted-normalization mutation is39/41 with precisely the two Bardeen gauge identities failing. The controls distinguish their asserted claims; success flags are not a universal physical-health theorem. Preserved development preflights are not pooled as current evidence.

Passed: evolving background/coefficient consistency; canonical raw auxiliary and phase equations; physical gauge/source factors including hatted L² and ell; declared seed interpretation; implementation and tolerance/solver evidence in the tested range. Conditional: the pinned on-shell quadratic reduction and timelike/operator domain, linear amplitude and physical cutoff availability. Not addressed: finite-k full stability or conserved canonical energy, nonlinear clock/source admission, observed primordial preparation, real thermal-photon/radiation transport, baryon/cold abundance, matter-era growth or32pi selection.

The strongest safe result is an actual, bounded, physically reconstructed radiation/Weyl transfer discrimination of the arithmetic and repaired operators, plus a regular canonical trajectory through the velocity-chart root. The first missing physical arrows remain nonlinear/clock admission, canonical mode/cutoff interpretation and a specified abundance/early-state mechanism. Same canonical recipe is not matched observable data, and a small positive sound speed does not create cold matter.
