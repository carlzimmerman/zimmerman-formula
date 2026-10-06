# Independent action-level physical-growth closure review

Primary verdict: **proved as written for the retained four-dimensional nonminimal complex-carrier action with separately conserved dust and ideal radiation, finite k>0, and admitted F>0 background**. The exact scalar perturbation system and independent phase-velocity Weyl witness pass. Numerical transfer evidence is bounded to the declared eight paths; it is not a certified full trajectory or an observed growth/CMB likelihood. No blocking correction found.

## Frozen inputs and normalized claim
Reviewed REPORT.md SHA25611d8f8feeb130813ef20c7c1fd76b9f5c18eaa495e93406cd62b9a9a1edc3022, growth.py SHA2563d5934f3e00344f47e6dc6dd042c84f9fb92ddec084c53cf3e0fbcbe83b62367, checks.py SHA2565fc84c57407c190be463bdfa5a6c88051c421644a03619788a22c2c9534793ee. Author input hashes were unchanged. The parent equations.py supplies the already audited actual background; no EdS or tracefree-radiation curvature approximation is substituted.

The action is MR/2−∂χ*∂χ−ξR|χ|² plus ordinary dust and ideal radiation. Its metric equation is
F G_mu nu=T_ord+T_can+nabla_mu nabla_nu F−g_mu nu box F,
F=M−2ξf, f=|χ|²,
T_can=∂χ*∂χ+∂χ∂χ*−gX, X=∂χ*∂χ.
In these complex-field conventions canonical background density and pressure are E=|q|², not E/2. Canonical real fields are sqrt2 times the two components of χ. The background quantities obey3FH²+3FdotH=ρd+ρr+E, B R=ρd+2(6ξ−1)E, B=F+12ξ²f, and R=6(Hdot+2H²).

The dependency chain is raw metric/KG/fluid variation → slip and momentum → algebraic trace and first-order evolution → Hamiltonian constraint propagation → actual geometric Ricci/remaining metric equations → phase-velocity constraint-compatible datum → bounded normalized transfer columns. The report correctly limits its continuation of CFG355 to the carrier action, rather than claiming to have varied the complete rank/gate/Vlasov action. Its gate-OFF discussion is not used as evidence for the transfer theorem.

## Mixed metric constraints reconstructed

Use ds²=−(1+2Ψ)dt²+a²(1−2Φ)dx² and p²=k²/a². Direct canonical mixed stress gives
δρ=ρdδd+ρrδr+2Re(q*δχdot)−2ΨE,
δq=ρdvd+4ρrvr/3−2Re(q*δχ),
δT^0_i=∂iδq.
The slip is F(Φ−Ψ)=δF, as ordinary ideal fluids and the homogeneous canonical carrier have no linear scalar anisotropic stress. The momentum row gives
2FZ=−δq+δFdot−HδF−FdotΨ, Z=Φdot+HΨ.
Both derivative-stress signs agree with the declared metric equation.

For an independent00 derivation, the background derivative contribution (nabla^0 nabla_0−box)F is +3HFdot. Varying the spatial Hessian gives
δ[(nabla^0 nabla_0−box)F]
 =p²δF+3HδFdot−3FdotΦdot−6HFdotΨ.
Combining it with δG^0_0=2p²Φ+6HZ and G^0_0_background=−3H² yields exactly growth.py's C00. Substituting momentum and slip gives
C00=CW=2Fp²W+δρ−3Hδq−6H²δF+3FdotZ,
W=(Φ+Ψ)/2.
In particular the solved Weyl equation has +6H²δF on its right side. Dropping that term would change the source constraint.

For physical interpretation, define Δd=δd−3Hvd and Δr=δr−4Hvr. Then the actual source bracket is
ρdΔd+ρrΔr+[δE+6HRe(q*δχ)]−6H²δF+3FdotZ.
Thus a bare-M Weyl effective density would be M/F times this bracket. It is not ordinary dust density alone, nor simply a total-growth ratio. The phase witness below keeps initial ordinary dust and radiation data identical while changing W, establishing a sharper independent-source statement.

## Local trace, KG and fluid rows

The exact action trace follows by boxχ=ξRχ and box f=2ξRf+2X:
B R=ρd−2(6ξ−1)X.
Perturbing about the homogeneous field has δX=−δE. Also δB=(12ξ²−2ξ)δf=−(6ξ−1)δF. Therefore
δR=[ρdδd+2(6ξ−1)δE+(6ξ−1)RδF]/B.
Ordinary ideal radiation is tracefree, but the carrier and dust are not. Prescribing δR=0 is an inconsistent changed closure in these general data.

Direct KG variation gives
δχddot+3Hδχdot+(p²+ξR)δχ
 =q(Ψdot+3Φdot)−2ξRχΨ−ξχδR.
Differentiating the slip supplies Ψdot=Φdot−δFdot/F+δF Fdot/F². The code uses coordinate δχdot and δFdot, while the normal-frame canonical energy includes the necessary −2ΨE; these conventions are consistent.

Separate perfect-fluid conservation gives d(δd)/dt=3Φdot+p²vd, d(vd)/dt=−Ψ, d(δr)/dt=4Φdot+4p²vr/3, d(vr)/dt=Hvr−Ψ−δr/4. The +Hvr term follows because (ρr+pr)∝a^−4 and T^0_i=(ρr+pr)∂ivr: its momentum conservation contains3Hδq_r, leaving vrdot−Hvr. Dust has cancellation instead. This checks velocity convention and signs independently, not only continuity equations.

## Sufficiency, constraint count and independent geometric check

The report's Noether argument is correct. With R_alg provisionally different from geometric R_geo, KG evaluated with R_alg gives boxF=−4ξ(X+ξR_alg f). The raw metric residual has exact trace
E^mu_mu=F(R_alg−R_geo)
and divergence
nabla_mu E^mu_nu=(∂nuF/2)(R_alg−R_geo).
The spatial right side vanishes at linear order on the homogeneous on-shell background. Imposed momentum and traceless spatial rows then force the remaining isotropic pressure residual P=0 for k>0. The temporal divergence and trace give
Cdot=(Fdot/(2F)−3H)C,
δR_geo−δR_alg=−C/F.
Initial C=0 is preserved and implies the proper KG curvature and remaining scalar metric rows. This is an exact closure proof, not just a sampled Hamiltonian defect. F=0 and homogeneous k=0 are deliberately excluded.

Independently corroborated these identities without importing author functions: introduced A=Re(q*δχ), δD_coord=Re(q*δχ+χ*δχdot) and derived
Adot=−3HA−ξRδf/2+δE/2+ΨE,
δEdot=−6HδE−2ξRδD_coord−2p²A+6EΦdot−2ξDδR,
δD_coord_dot=−3HδD_coord−(p²+2ξR)δf/2+δE+2ΨE
 +D(Ψdot+3Φdot)−2ξRfΨ−ξfδR.
Substitution with actual background evolution and Friedmann constraint gives the two identities above. The independent geometric expression used is
δR_geo=−6Φddot−6H(Ψdot+4Φdot)−2RΨ+2p²(Ψ−2Φ).
Exact SymPy cancellation of both residuals returned zero; the action/Noether derivation is the load-bearing proof, so this corroboration is not treated as an independent numerical certificate.

Nine first-order variables with one genuine initial C constraint leave eight scalar phase-space dimensions: four from two real carrier fields, two dust and two ideal-radiation. Slip/momentum determine metric potentials and do not add another gravitational scalar mode. This matches the declared action; no constraint redundancy or missing initial metric row was found.

## Charge transport and phase-velocity Weyl witness

With L=Im(χ*q)=Q/a³, the report's chosen Q normalization is half the conventional complex-field Noether charge if its generator is normalized in the usual way; a constant factor has no effect on the conservation statements. Direct KG variation yields
δLdot+3HδL=−p²Im(χ*δχ)+L(Ψdot+3Φdot).
Consequently the coordinate-volume flux perturbation is
δQ=a³[δL−L(Ψ+3Φ)],
δQdot+a k²Im(χ*δχ)=0.
The lapse/volume correction is essential; conservation is not an algebraic dust closure.

At δχ=0, δχdot=iωχ and vanishing ordinary density/velocity seeds, δF=δFdot=δq=0. Canonical energy gives δρ=2Lω−2ΨE. Slip Φ=Ψ and momentum Z=−FdotΨ/(2F) then force
Φ=Ψ=−2Lω/[2Fp²−2E−3Fdot²/(2F)].
This is a nonzero Bardeen/Weyl potential at exactly equal zero initial ordinary dust/radiation perturbations when Qω≠0 and the denominator is nonzero. It is a phase-velocity/local charge-density datum, not a constant global U(1) rotation or an unconserved arbitrary stress source. The actual initial local charge perturbation is a³[fω−4ΨL]; a finite-k perturbation need not change total background charge.

The selected positive denominator is an initial Φ-solve chart guard, not a kinetic-health condition. If it vanishes, ρd>0 permits solving the Hamiltonian constraint for δd instead; the report correctly avoids inferring physical singularity. The linear seed can be scaled arbitrarily small. This proves dependence on independent carrier initial data, not an impossibility of computing transfer once an initial mode vector is supplied, and not pressureless carrier growth or cold abundance.

## Frozen computation audit and numerical scope

Independently validated all three current standard manifests against frozen input/output bytes: main_a55/55, control_dust_only_a47/55, control_drop_trace_a43/55. These are the current55 assertions including geometric-Ricci checks; old53-assertion development preflight is not authoritative. Dust-only failures are exactly the two initial Hamiltonian/source failures and phase trajectory constraint failures; drop-trace failures are the Ricci/propagation and all trajectory constraint failures. Neither is an alternative physical model excluded merely by check counts.

Inspected the numerical implementation only after scientific inputs froze. It evolves two xi values100/1000, two unit seeds and DOP853/Radau, eight paths on a=1→2 with k=10H_initial, rtol1e−9/atol1e−12 and41 sample points. It checks an evaluation-count postcondition<20000; this is not a per-step hard solver cap. Standard runner resource caps are separate. Maximum nfev14275, maximum common-vector solver difference2.6854e−8 and maximum sampled normalized Hamiltonian defect7.1525e−7 match the records. F remains at least.999 for xi100 and.9999 for xi1000 in these future intervals.

Phase endpoints are W=1.96065060e−6, Δd=−2.2297364e−4 at xi100 and W=1.11661183e−7, Δd=−1.6786366e−5 at xi1000. Dust endpoints are W=−.0100447161, Δd=1.35794769 and W=−.00995878674, Δd=1.34252469. These are normalized linear transfer columns. Zero initial velocities do not prepare a pure growing or primordial adiabatic mode; comparison with a pure EdS growth factor would require changed initial-mode preparation. Solver agreement and41-point defect checks are bounded numerical evidence, not interval error bounds over unsampled times.

The rho_r/rho_d=.01 initial fixture and a1→2 interval are not an early radiation-era calculation. Ideal radiation excludes anisotropic stress, photon transport/polarization, baryon drag and atomic kinetics. Adding radiation anisotropic stress changes slip and adds transport variables. Viable past history avoiding/completing the F boundary, primordial preparation, nonlinear source transfer, cold pressure/phase identity, and observational likelihood remain unresolved. No target coefficient or complete CFG355 theory is inferred.

All requested action/closure/witness obligations pass within these scopes; author scientific inputs remain frozen and unmodified.
