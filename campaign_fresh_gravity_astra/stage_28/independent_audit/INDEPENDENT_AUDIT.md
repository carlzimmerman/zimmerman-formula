# Independent FGF041 proof audit

**Verdict: proved as written**, for the explicitly stated counterexample to identification of nonlinear currents from bounded energy, weak derivative convergence and the declared vanishing weak residuals. This is not an exact-solution or strongly prepared initial-data counterexample.

## Claim and independence

For a fixed reviewed Q static crossing, select one compact regular-side path X(t)=x0+t/sqrt(tau), a fixed finite time slab on which it stays away from crossing and walls, positive potential/length units Psi,L, and one nonzero f in C_c^infinity((-1,1)). The packet Psi sqrt(epsilon) f((x-X)/(L epsilon)), with actual density, zero matter momentum and scale held at the background, has all sufficiently small positive dimensionless epsilon as its proof domain. It is a family of approximate states only. Its current fields converge to the background, while nonlinear energy, momentum and stress measures retain a transported defect already present initially.

My independent derivation was frozen at 2026-09-30T22:37:30.478936+00:00 with SHA256 a436daa8e9950c7385e1d312b91d0dd14f897ff8241b7b8ff73583bdc6d3d605, before any new author/root proof or formula preview. The author readiness message arrived subsequently and contained no equations. I then read the raw author proof and package. No new stage28 root proof was read. Mathematical overlap in the main packet is expected from the task's prescribed ansatz; the calculations were separately derived. My amplitude control is Psi epsilon^(3/4), while the author's is Psi epsilon; both are valid fixed controls. No mathematical computation or numerical scan was executed. Administrative reads, writes, SHA256 and schema checks are not a numerical experiment or runner manifest.

## Dependencies and obligations

The retained parent Q action and reviewed actual static crossing supply the background; FGF040 supplies full signed momentum and energy conventions. All packet estimates and measure limits are proved directly from those definitions. No external mathematical or literature mechanism is a load-bearing leaf. Source hashes identify dependencies but do not themselves prove them; the raw FGF040 equations and the earlier independent audit were checked for the inherited signs and scope.

| Obligation | Status | Decisive check |
|---|---|---|
| Actual speed, support, wall/mass/scale preservation | Passed | tau psi_tt=psi_xx exactly at c_tau=1/sqrt(tau); fixed finite slab and positive support margin allow every sufficiently small epsilon. |
| Signed Q, high-gradient bounds | Passed | b=(sqrt(a²+4s²)-a)/2 gives s-a/2<=b<=s; signed B, not a positive-gradient formula, is applied even when the packet reverses g. |
| Source, scale, mass and matter residuals | Passed | Exact expressions and each declared norm are checked below. |
| Combined momentum and energy residual | Passed | Direct full-current cancellation, without multiplying weak residuals by a concentrating gradient. |
| Nonlinear measure defects | Passed | Fixed-profile change of variables; errors are uniformly L1-small. |
| Initial data, boundaries and conservation scope | Passed | Initial energy/momentum defects persist; no creation from zero energy, global momentum conservation or exact trajectory claimed. |
| Vanishing-energy control and sufficient compactness | Passed | Independent amplitude control corroborates author control; strong L2 sufficient only for the fixed-matter/scale class. |
| Existence or defect-free approximation supplied by PDE | Not addressed | Explicitly excluded by the result. |
| Physical metric, RAR/M, evolving-H reservoir or observations | Out of scope | No transfer licensed. |

## Exact bounds and residual audit

Write p=psi_x, g0=phi0', S_*=Psi² integral(f'²)/L, and c_tau=1/sqrt(tau). Then integral p²=S_*, integral|p|=O(sqrt(epsilon)), and p_t=-c_tau p_x. The source error D=B(g0+p,a)-B(g0,a)-p is supported on a strip of width O(epsilon) and bounded by a_max. Hence its spatial L1 norm is O(epsilon) and L2 norm O(sqrt(epsilon)), uniformly on the time slab.

The elementary bounds |B-G|<=a/2 and |W-G²/2|<=a|G|/2 are global. For H=BG-W, H_s=s A with 0<=A<=1 gives H<=s²/2. Combining b>=s-a/2 with W<=s²/2 gives H>=s²/2-a s/2, so my sharper |H-s²/2|<=a s/2 also validates the author's looser a s bound. Since T_s=q<=a/2, T(|G|,a) is globally Lipschitz in signed G at each fixed a. None of these uses a deep-field approximation on the concentrating packet.

Mass residual is exactly zero. The actual dynamic source residual is -D_x, O(sqrt(epsilon)) in H^-1 and O(epsilon) against spatial tests with bounded value and derivative. The scale residual is T0-T(g0+p,a), and separate matter residual is rho p; both are O(sqrt(epsilon)) in L1 uniformly in time. They need not be small in L2. Signed background MOND flux obeys B0'=C rho; no static source constraint is falsely imposed on the time-dependent packet.

With Delta R_H=H(g0+p,a)-H(g0,a)-[(g0+p)²-g0²]/2, the FULL currents satisfy

    P-P0=(tau c_tau/C)(p²+g0 p),
    Pi-Pi0=(p²+g0 p+Delta R_H)/C,
    C(P_t+Pi_x)=g0' p+partial_x Delta R_H.

The final identity follows by differentiating p_t=-c_tau p_x and tau c_tau²=1. It keeps matter pressure and scale-gradient/potential stresses in the equilibrium Pi0. Regular-side g0' is bounded; Delta R_H has L1 norm O(sqrt(epsilon)). Thus combined residual tends to zero in the declared spatial Lip* norm uniformly in time and in interior spacetime distributions. A claim of strong combined residual convergence would not follow. The norms can be interpreted after the fixed reference units already declared; no dimensionless numerical physical threshold is inferred.

## Energy, measure and initial-data audit

Changing variables x=X(t)+L epsilon y proves p² dx -> S_* delta_X, including spacetime convergence. Cross terms g0 p vanish in L1. Consequently energy and stress each have extra mass E_*=S_*/C, momentum E_*/c_tau, and energy flux c_tau E_*. These coefficients satisfy their own transport conservation identities, so vanishing distributional residuals do not force the defect to vanish.

The exact energy difference is rho psi+[p²+g0 p+Delta R_W]/C. Here ||Delta R_W||1=O(sqrt(epsilon)) and ||rho psi||1=O(epsilon^(3/2)). Fluid internal energy, fluid kinetic energy and all scale terms are retained and unchanged. The full energy flux is -phi_t B/C, equal to c_tau p²/C plus an L1 error O(sqrt(epsilon)); this follows also for the product pD because D is uniformly bounded and ||p||1 is small. The leading transported pair cancels exactly and derivatives of the remaining L1 errors vanish against fixed compact C1 spacetime tests. This proves weak approximate energy balance, not exact energy conservation at finite epsilon.

Integration by parts using compact support and B0'=C rho gives the additional exact identity

    E_e-E0=(1/C) integral[p²/2+W(g0+p,a)-W(g0,a)-B0 p].

The signed-gradient potential is convex with Hessian 0<=A<=1, including its continuous zero value at g=0. Its Bregman term lies between 0 and p²/2. Thus S_*/(2C)<=E_e-E0<=S_*/C, and the high-gradient remainder bounds show uniform convergence to S_*/C. This verifies uniform finite full energy and the nonzero initial defect, with no cancellation hidden in signed interaction energy.

The same defects occur at t=0. Derivative and velocity data are weakly, not strongly, L2 prepared. Initial energy/momentum tests must carry those initial measures. Because the support stays away from walls, perturbation traces and boundary fluxes coincide with the background. This does not replace actual endpoint traction conditions with a claim of global momentum conservation. The limiting background is itself a solution; the obstruction is identification of nonlinear currents, not a nonzero limit of the residuals.

## Control, exact scope and next implication

For the author's control psi=Psi epsilon f, integral p²=epsilon S_* and the exact Bregman formula bounds relative energy by epsilon E_*. All nonlinear defect masses vanish. The original residual bounds suffice and products converge strongly in L1; derivative and velocity data now converge strongly in L2. My frozen control uses epsilon^(3/4), retaining an unbounded peak gradient while integral p²=S_* sqrt(epsilon) tends to zero. This independently distinguishes peak size from concentration mass, without any scan.

Strong L2 convergence of phi_x and phi_t identifies B by its 1-Lipschitz dependence and identifies all relevant quadratic products by Cauchy-Schwarz; W convergence follows its linear derivative-growth bound. For this fixed-density/scale class the interaction follows from fixed walls and derivative convergence (or the available uniform convergence). Convergence in measure plus uniform integrability of derivative squares yields strong L2 by an elementary exceptional-set split. The main family fails precisely uniform integrability. For varying matter/scale, j²/n, internal energy, fluid energy advection and scale currents need their own hypotheses; the author's qualification that kinetic energy alone does not bound cubic-velocity advection is correct.

The strongest accepted statement is therefore the analytic counterexample for the expressly weak approximation class, for all sufficiently small epsilon. It does not establish a sequence of exact solutions, nonuniqueness, nonlinear instability, or failure with strongly prepared initial energy. The cheapest changed-premise next check is whether vanishing FULL relative energy retaining exact Q Bregman control excludes such defects, conditional on a separately assumed energy inequality; no solution existence or compactness theorem is inferred here. This next target appeared only after my proof freeze in the author's final metadata and has not been executed.

Both a0=9.3619e-11 and 1.1279e-10 m/s² remain separate positive reference hypotheses. Constant vacuum and frozen-H reference comparisons are distinct from an evolving-H history and its exchange obligation. This calculation uses actual signed Q source scaling, with responsive scale and positive tau as diagnostic assumptions. No RAR/M, physical photon speed, metric/DOF completion, physical reservoir, calibrated empirical evidence or theory closure is accepted.

## Provenance and actual checks

Worker result SHA256: 07785d7a09b507a224722edaaf389aeec09d65cb5ce0882d26683d78ad3287d2.
Worker derivation SHA256: 54e8390a0fb61573041e28aade6a68d3bb67e17adfe82b049eb5a63b5f0fd7a5.

An administrative Python check verified all 10 declared input hashes, all 3 artifact hashes, the exact task hash, matching input-map JSON, every required result-contract field, and the 4 independently frozen source pins plus frozen derivation bytes. Full source hash mapping is in audit_result.json. The old stage27 root files in the worker's ancestry were hash-checked only during this audit; no new root proof was read or used. No correction was required and no frozen bytes were replaced. There is no computational manifest because no mathematical executable was run.
