# Independent audit of the evolving scalar reduction

**Primary verdict: computationally verified only in the stated range.** The archived constant small-alpha model has a genuine rapid metric/density-growth witness after extending its initial-value problem to Δlog(a)=0.1. The archived power-four response witness instead develops an oscillatory transient over that same duration; its initial clock-slicing amplification is not sufficient evidence of a sustained gravitational instability. Neither finding closes the theory or proves stability for a parameter family.

This audit is confined to the quadratic scalar ADM action and the archived `frw_repair/run_verified` matrices. It does not independently reconstruct every term of the covariant action, add baryons/radiation, or test nonlinear validity. The computations read earlier files and write only this new directory. Baseline repository revision supplied to this audit: `23d3890790291c0ec44b4ca7da784a806d7094d2`; the repository has pre-existing untracked research material.

## Claim and dependency graph

The precise input claim is that, for the stated exponential-well background, positive c14=alpha, c2=b, epsilon and nonzero k, the algebraic lapse/shift constraints leave two scalar fields with positive kinetic matrix, and that two specified initial-value problems exhibit strong short-interval amplification. The separate physical question is whether those witnesses represent growth of measured metric/stress variables, a transient transfer between fields and velocities, or a slicing-sensitive coordinate effect.

Dependency chain:

1. Specified ADM action and projected-gradient healing operator → archived four scalar Euler–Lagrange equations. **Input assumption here**, reviewed structurally but not a fresh covariant tensor derivation.
2. Exact exponential background → lapse, charge, and spatial-trace equations. **Independently checked exactly.**
3. Algebraic lapse/shift solutions and their full time derivatives → archived two-field equations. **All four original equation residuals checked exactly.**
4. Reduced equations → variational/Helmholtz identities. **Independently checked exactly**, including symbolic alpha-dot.
5. Reduced solutions → Bardeen potentials, Newtonian density, and physical clock observables. **Derived and checked below.**
6. Selected finite evolution → numerical amplification witnesses. **Adaptive float64 and independent 50-digit RK4 evidence**, not interval certification or a universal theorem.

## Exact background and variational checks

Let Gc=1+3b/2, F=epsilon j, F_Q=j, Hdot=Qj/(4Gc), Qdot=−3epsilon H, jdot=−3Hj, and Lambda=3Gc H²−(epsilon−Q)j/2.

The homogeneous spatial-trace equation divided by a² is

    18 Gc H² + 12 Gc Hdot − 3(F+2Lambda) = 0.

It vanishes identically after these substitutions. This is the missing trace check beyond the already checked lapse/charge equations.

For the unrestricted homogeneous action

    L = −6Gc a adot²/N − N a³ [F(phidot/N)+2Lambda],

with Euler–Lagrange convention E_x=L_x−dt L_xdot, the exact identity is

    adot E_a + phidot E_phi − N dt(E_N) = 0.

`constraints_check.py` verifies this symbolically before specializing F. It also substitutes the archived lapse/shift solutions, their exact derivatives, and the reduced accelerations back into **all four** archived perturbation equations; every residual is identically zero. Thus no missing lapse/shift derivative was found in this reduction. This is constraint reconstruction/propagation by algebraic elimination, not a separate numerical evolution of constraint-violating data.

Write the reduced equations in cosmic time as

    K qddot + D qdot + U q = 0,     q=(Phi,P),
    K=−mass, D=−rest[:,(1,3)], U=−rest[:,(0,2)].

The following exact identities both pass:

    D+Dᵀ = 2 Kdot,
    U−Uᵀ = dt(D−Dᵀ)/2.

They are the Helmholtz conditions for this second-order system to come from a real quadratic action. They give an orthogonal check on the time derivatives retained by the reduction. Constant and response archived matrices also agree exactly with the appropriate specialization of the general matrix.

The checks find no missing scalar-background chain-rule term. A full clock-field Ward identity for an independently restored covariant clock remains outside this audit; minisuperspace covariance and all four gauge-fixed ADM equations are what was checked.

## Physical observables and signs

The metric convention is

    ds²=−(1+2psi)dt² + 2a ∂iB dt dxi + a²(1−2Phi) δij dxi dxj.

Under a time-gauge shift chi, delta psi=−chidot, delta Phi=Hchi, delta B=chi/a, and delta P=−Qchi. Setting B_new=0 therefore uses chi=−aB. Consequently

    Phi_Newtonian = Phi − H a B,
    Psi_Newtonian = psi + dt(aB),
    P_Newtonian = P + Q aB,
    deltaQ_Newtonian = (Pdot−Qpsi) + Qdot aB,
    delta_rho_Newtonian/rho = Q/(Q−epsilon) * [(Pdot−Qpsi)/epsilon − 3HaB].

The last formula uses rho=F−QF_Q=(epsilon−Q)j and rho_Q=−QF_QQ. All quantities are reconstructed on solutions of the original reduced equations. In this scalar theory the symbolic difference `Psi_Newtonian−Phi_Newtonian` is **exactly zero** after the constraints and equations of motion, for arbitrary alpha, alpha-dot and b in the generic domain. Equality is not merely a numerical coincidence.

Additional physical clock observables are

    delta(theta_clock)/H = [−3(Phidot+Hpsi)+k²B/a]/H,
    |a_clock|/H = k psi/(aH)                 (signed Fourier amplitude).

The clock acceleration vanishes on the homogeneous background, so its first-order perturbation is automatically gauge invariant. The expansion instead has background theta_clock=3H: its raw perturbation transforms as delta theta_clock -> delta theta_clock−3Hdot chi. With clock perturbation T transforming as T -> T−chi, the gauge-invariant completion is delta theta_clock−3Hdot T. The displayed expansion formula is this completion evaluated in unitary clock gauge T=0; its computed numbers are unchanged. The scalar perturbation P in clock gauge also measures the scalar's spatial gradient relative to the clock congruence. Therefore growth of P or clock acceleration cannot simply be dismissed as pure gauge, even when the Bardeen potentials remain quiet.

As an independent check on the parent's phase-space construction, pi_phi=−sqrt(h) F_Q has background a³t with t=−j, and

    delta pi_phi/(a³t) = (Pdot−Qpsi)/epsilon − 3Phi.

The lapse cancels between N sqrt(h) and dQ/dphidot=1/N; the other displayed ADM terms add no linear canonical momentum in this gauge.

## Bounded evolution results

Initial data are exactly the largest-real-eigenvalue directions used by the archived witnesses; the numerical initializer has roundoff-sized differences from the saved vectors. The original equations evolve in N=log(a) with the full evolving background. Amplitudes may be uniformly rescaled to remain linear; the unscaled numerical amplitudes below are not nonlinear predictions.

| Case and interval | Clock Phi gain | Bardeen Phi and Psi gain | Newtonian density-contrast gain |
|---|---:|---:|---:|
| Constant alpha=1/40000, a0=.1, k=.1/Mpc, ΔN=.01 | 22.4311 | 1.00054031 | 1.62508 |
| Response alpha=.5v/(.5+v), v=1e−7 a⁻⁴, a0=.5, k=.001/Mpc, ΔN=.004 | 17.8141 | .993429875 | 3.71835 |
| Same constant case, ΔN=.1 | about 7.88e9 | about 1.73325e7 | about 2.97007e8 |
| Same response case, ΔN=.1 | about −73.35 | about 1.05968481 | about −13.6546 |

Signed gains are ratios to the initial signed amplitude; a negative value is a sign reversal. Component ratios can be large when an initial component is small and are not by themselves an energy norm.

At ΔN=.1 the 50-digit calculations give:

- Constant: Bardeen Phi=78371.2661583 and Newtonian density contrast=−5.885986871e10. The initial values were .00452164554 and −198.17702. Intermediate adaptive results at ΔN=.05 already give Bardeen Phi≈1.60695. This is real metric/stress growth, not only a slicing artifact.
- Response: Bardeen Phi=−.00238117604748 and Newtonian density contrast=−.668065026. Initial values were −.00224706066 and .048926119. The clock fields undergo a sizeable transient with oscillatory later behavior; the metric potential remains near its initial scale throughout the sampled interval. Density and clock amplitudes are not uniformly small relative to their initial values, so this is **not** a proof of stability.

The constant 50-digit RK4 2000/4000-step state discrepancy is 5.67e−8. The response 8000/16000-step discrepancy is 7.61e−7; its fast oscillatory phase requires many more steps than its metric potential alone suggests. These figures describe numerical convergence, not rigorous error bounds. The maximum component-scaled float64/high-precision observable discrepancies, |difference|/(1+|high-precision value|), are 3.63e−9 for the constant case and 5.58e−7 for the response case. Both independent checks agree within 1e−6 in this metric.

## Coordinate and energy checks

A configuration transformation

    zeta=Phi+HP/Q,   vartheta=HP/Q,
    q=Sx, S=[[1,−1],[0,Q/H]]

retains the exact additional derivative terms. Its log-a action matrices are

    K_N = H Sᵀ K S,
    D_N = Sᵀ(2K Sdot+D S) + (Hdot/H)Sᵀ K S,
    U_N = Sᵀ(K Sddot+D Sdot+U S)/H.

Independent integration in these variables matches the original short-interval solution at relative errors below 6e−10. The instantaneous rates change substantially under this time-dependent transformation. They are not coordinate-invariant stability diagnostics. A trial energy formed by adding 4K_N to sym(U_N) **failed positivity** in these coordinates; this unsuccessful trial is preserved in `physical_coordinates.py` and is not offered as an energy bound.

`phase_transform.json` supplies an exact phase-space transformation to

    (Phi_Newtonian, delta_rho_Newtonian/rho, H aB, d(HaB)/dN).

For cosmic-time original state y=(Phi,Phidot,P,Pdot), it records z=S_phys y and (dS_phys/dt+S_phys A_cosmic)/H. Therefore its full transformed generator is

    A_phys = [(dS_phys/dt+S_phys A_cosmic)/H] S_phys^−1.

Time-dependent coefficient derivatives, including alpha-double-dot where present, are included. The saved phase matrix is exact symbolic data; the displayed pointwise spectra use a numerical inversion and are only diagnostics. The original constant case's transform condition number is around 7e8 at the start, so its pointwise floating-point eigenvalues warrant less weight than the independently checked evolved observables.

A useful sufficient energy criterion follows directly from the exact Helmholtz identities. For any chosen physical configuration coordinates and N-action matrices, set

    G=(D_N−D_Nᵀ)/2, V=(U_N+U_Nᵀ)/2,
    W=V+mu² K_N,
    E=(x_Nᵀ K_N x_N + xᵀ W x)/2.

If K_N and W are uniformly positive, then

    E_N = −x_Nᵀ K_N' x_N/2
          + x_Nᵀ(mu²K_N−G'/2)x + xᵀW'x/2.

With P=diag(W,K_N), Cmat=mu²K_N−G'/2, and

    L=[[W',Cmatᵀ],[Cmat,−K_N']],

any bound L<=C(N)P implies E(N)<=E(N0)exp(integral C dN). To give this physical content one also needs explicit comparison bounds between P and the chosen metric, stress and clock observables. Positivity of K alone is insufficient. This is an exact sufficient condition, **not a claim that it has been established** for the constant alpha=.5 candidate or any continuum of parameters.

## Remaining gap and cheapest next check

The smallest missing implication for a successful construction is a controlled physical evolution/energy bound over an explicit wavelength and epoch domain for the same action. The response example should not be rejected solely from its short clock-amplitude witness. Conversely, the constant small-alpha example has a longer metric/stress witness that cannot be removed by merely relabeling Phi.

The parent's canonical density phase-space formulation is a useful next check because it avoids the near cancellation defining the kinetic mode. Apply a physical norm and longer bounded evolution there, then seek explicit matrix inequalities over the proposed alpha=.5 cosmological branch. No global stability, galactic consistency, nonlinear cutoff, or closure result follows from the present finite runs.

Reproduction is pinned by `contract.json` and the completed new `run_verified_dynamic/manifest.json`; the computation-audit validator accepted the record and checked its input/result hashes. `verify_dynamic.py OUTPUT_DIRECTORY` regenerates exact identities, transforms, adaptive trajectories and high-precision checks while preserving older evidence directories.

Final mathematical proofreading covered this report only. A subsequent scoped correction distinguishes raw expansion perturbations from their unitary-clock gauge-invariant completion; numerical results are unchanged. No unresolved local notation errors were found. The substantive limitations are stated above.
