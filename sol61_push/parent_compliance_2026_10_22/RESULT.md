# Parent action and excess mechanism: a conservative compliance investigation

**The full objective is not reached.** This investigation rules out a constant-compliance construction under declared reduced-model benchmarks, identifies a critical density scaling and a passive-phase obstruction, and constructs a conservative rotationally driven toy that can strengthen matching. The surviving toy has not produced a dwarf/cluster profile or a covariant theory. Its reciprocal effect on baryon inertia is substantial and must be included in any continuation.

Base e9e534936852643bb3f3ca9df07a31ed2734a30c. The input contracts, four reproducible calculation families, controls, and self-audit are in this directory. No existing prediction, canonical statement, or other session's files was changed. No novel-result priority is claimed. This is a local research calculation using prior project reports, not an independently authenticated review of every prior no-go.

## 1. What was already tried and why this route was chosen

| Prior route | Relevant obstruction as recorded | Implication for this work |
|---|---|---|
| CFG941 exact tether / phantom=cold density | Linear self-gravity cancellation; satellite hover; fixed two-population mixture fails | Change the identity itself, not its name |
| CFG944 instantaneous expansion gate | Negative kinetic coefficient in the switching region; local-gate obstruction | Do not prescribe an instantaneous velocity-gradient switch |
| CFG946 separate dust and local law field | Reciprocity, EFE, extra source and no selector | Source every interaction reciprocally; do not hide additional gravitating mass |
| CFG955 kinetic thermostat | Law neither uniquely selected nor retained; ordinary clock ordering fails | Do not impose a Jeans-temperature target as its own derivation |
| D9 / D9b constrained A33 | Exact multiplier restores cancellation/positivity problems; literal version double counts | Couple cold mass to gravity once; replace multiplier by finite energy |
| mechanism_reassessment, 22 October | New lapse constraints, polarized response and radiation; self-consistent background still open | Preserve this separate unfinished route; do not duplicate it or assume its old first-class claim |
| Formation roadmap | Finite inventory, energy/angular-momentum receiver and rates still required | A minimum is not formation, capture, retention, or an attractor |

Paths: `campaign_fresh_gravity/CFG941_self_gravity_repair/DERIVATION.md`, `CFG944_gated_tether_ghost_cure/README.md`, `CFG946_option2_phantom_not_cold/README.md`, `CFG955_kinetic_parent/README.md`; `doors_push_2026_10_22/D9b_A33_multiplier/README.md`; `sol61_push/mechanism_reassessment_2026_10_22/{RESULT,NONLINEAR_WEAK_RESULT,RADIATION_RESULT}.md`; `sol61_push/ROADMAP_COLD_ENERGY_MECHANISMS_2026-10-19.md`.

These are distinct mathematical models. Neither an older shear pass nor a parent stability claim transfers to the new energy below.

## 2. A finite, conservative replacement for the exact identity

Let K=4piG, P be a spatial polarization, d=div P, C=rho-rhobar, and e=C-d. Transport rho by a conserved material current. With constant A>0, use the reduced Newtonian energy

    E = E_Newton[rho_b+rho] + integral [W(K|P|)+A e^2/2] d^3x,
    W(u) = (a0^2/K)[-u/a0-ln(1-u/a0)],  0<=u<a0,
    ell^2=A/K.

The full reduced Lagrangian before eliminating Phi has the usual -|grad Phi|^2/(2K)-(rho_b+rho)Phi, minus the displayed internal energy, plus positive material and polarization kinetic energies. No P.grad Phi term is added: doing so would count the source twice. The internal energy has no explicit time dependence. With suitable closed boundaries the reduced action conserves total energy and mass. Translation/rotation invariant boundary conditions give the corresponding Noether momenta. This is not yet a generally covariant construction; a preferred-frame dot P and a reference rhobar require a physical completion.

### Quadratic self-gravity

For a real Fourier amplitude convention in which the common spatial normalization is suppressed,

    E_k = -K(B+C)^2/(2k^2) + K d^2/(2k^2) + A(C-d)^2/2.

Eliminate d by its stationary equation:

    d = z C/(1+z),  z=k^2 ell^2,
    partial_C^2 E_eff = -K/[k^2(1+z)],
    partial_B partial_C E_eff = -K/k^2.

Thus cold self-gravity survives with fraction S=1/(1+z); the baryon/cold interaction is unchanged and reciprocal. At z large this approaches the old cancellation. At z small it approaches dust. This limited result directly follows from one energy rather than an independently chosen force prescription.

For pure cold density rho with displacement xi and polarization inertia eta>0, the frozen-background growing root t=s^2/(K rho) satisfies

    epsilon t^2+[1+z+epsilon(z-1)]t-1=0,  epsilon=eta rho>0.

There is exactly one positive root, because the leading coefficient is positive and the constant is negative. Evaluating at t=1/(1+z) gives epsilon z^2/(1+z)^2>=0. Therefore 0<t<=1/(1+z): polarization inertia does not rescue the frozen-background growth suppression. This proof is not a reduction of a general relativistic expanding background. In particular, any expansion-induced kinetic mixing would need to be derived separately.

### Static radial error from the same energy

Use rhobar=0 for an isolated, finite-radius diagnostic. For positive cold density, static chemical equilibrium and P variation give

    Phi+A e=mu,       grad Phi=partial_P W,
    g=F(u)=a0 u/(a0-u),  u=K|P|,
    h(g)=g-u=g^2/(g+a0).

Spherical Poisson then becomes

    (r^2 h(g))'/r^2 = K rho_b+(mu-Phi)/ell^2.

The finite-compliance correction is physical extra density. The law is recovered only when the last term is negligible. Set mu=Phi(R), R>=r, and assume an attractive solution with regular cold flux at the origin around a central point baryonic mass M. Then mu-Phi(s)=integral_s^R g(t)dt>=0, so h(g)>=GM/r^2 and g>=sqrt(GMa0)/r. Consequently

    h(g(r))-GM/r^2
       >= sqrt(GMa0)/(ell^2 r^2) integral_0^r s^2 ln(r/s) ds
       = sqrt(GMa0) r/(9 ell^2).

This is a necessary inequality, not an existence proof for a cold point-source atmosphere. It is independent of the outer radius beyond requiring R>=r. Different pressure, nonzero boundary mismatch, or an extended source requires a different bound.

### Declared benchmark: no overlap

For the illustrative point source M=1e10 solar masses at r=50 kpc, require g<=1.1 g_law. Separately require the local, quasistatic EdS growing exponent to be at least .999 at k_com=.1/Mpc, z_redshift=1100. Use the record's input rho_c/rho_b=5.364. The instantaneous growth matrix is

    [[f_b, f_c], [f_b, f_c/(1+z)]],
    n=(-1+sqrt(1+24 lambda_max))/4.

It yields z<=.0023513263. These are declared consistency diagnostics, not a CMB likelihood or an observational exclusion of all parents.

| a0 footing, m/s^2 | galaxy lower ell | early-growth upper ell | separation |
|---|---:|---:|---:|
| 9.3603e-11 | 133.787 kpc | .440422 kpc | 303.77 times |
| 1.1312e-10 | 140.005 kpc | .440422 kpc | 317.89 times |

At the galaxy lower lengths the diagnostic n is about .611, near the hard-identity value .609545. The constant-A construction cannot satisfy these requirements together. A complete FRW calculation could change the diagnostic and is not silently assumed done.

## 3. Density-dependent compliance: an admissible energy with another limitation

Let A(rho)=A0(rho/rho0)^(-m). The mismatch energy V=A(rho)e^2/2 has Hessian determinant, in (rho,d),

    det Hess V = e^2 [A A''/2-(A')^2]
               = A^2 e^2 m(1-m)/(2 rho^2).

Since V_dd=A>0, this local potential is convex for 0<=m<=1. It is degenerate at e=0, even inside that interval. This does not prove gravitational stability or PDE well-posedness.

Coefficient derivatives alter the static force:

    mu=Phi+A e+A' e^2/2,
    partial_P W=-grad(A e)=grad Phi+grad(A' e^2/2).

It would be incorrect to replace ell by ell(rho) in the constant-A galaxy calculation while dropping this force. No galaxy prediction from section 2 transfers unchanged.

On a homogeneous matter scaling rho=rho0 a^-3,

    k_phys^2 ell(rho)^2=(k_com ell0)^2 a^(3m-2).

Keeping this quantity from diverging as a tends to zero requires m>=2/3 within that scaling. This is an idealized matter-limit criterion, not a radiation-era result.

For a compact fixed-mass uniform sphere and the admissible trial P=0, high density makes rhobar negligible. The energies are

    U_mismatch = (A0 rho0^m/2) M^(2-m) (3/4pi)^(1-m) R^[-3(1-m)],
    E_grav = -3GM^2/(5R).

For m>2/3 this trial's Newtonian energy tends to minus infinity as R tends to zero. At m=2/3 the two terms have the same power. In that marginal case the trial becomes negative and unbounded for

    M > M_trial = (5 sqrt(10) pi/3) rho0 ell0^3.

This gives a concentration direction, not a proof that every equilibrium is unstable or that actual galaxies collapse. Smooth compact profiles can approximate the uniform-sphere trial. Relativistic breakdown, pressure and new short-distance operators are outside this energy; the existing grad P stiffness is zero on the trial and cannot remove it.

At the diagnostic growth upper length ell0=.484905 Mpc and declared rho0=2.26e-27 kg/m^3, the trial scale is recorded in `scaling_run/result.json` (approximately 6.3e10 solar masses). It is neither a measured threshold nor a predicted core mass: ell0 is merely an upper bound, rho0 is an illustrative input, and the uniform sphere is only one trial.

Therefore m=2/3 is the marginal candidate in this restricted family, but it supplies no stable universal core population and no distinction between baryons with the same density and different orbital support. Finite-redshift growth constraints do not justify extending the concentration conclusion beyond their density range; high-density changes to the model remain possible and must be declared.

## 4. A passive phase cannot provide the desired stiffening

Promote susceptibility chi=1/A to a positive dynamical scalar. With positive kinetic/gradient terms and

    V_total(e,chi)=e^2/(2chi)+mu_chi^2(chi-chi0)^2/2,

the joint Hessian determinant is mu_chi^2/chi>0. The equilibrium equation is

    mu_chi^2(chi-chi0)=e^2/(2chi^2),

so chi>=chi0 and matching softens rather than stiffens.

There is a more general minimizer statement. Suppose q0 globally minimizes V(q) and q_e globally minimizes V(q)+A(q)e^2/2 at fixed e!=0. Comparing these two values gives

    [A(q_e)-A(q0)] e^2/2 <= V(q0)-V(q_e) <= 0.

Hence A(q_e)<=A(q0). This excludes spontaneous equilibrium stiffening from the mismatch penalty alone. It does not exclude an independent source, metastability, driven phases, or a phase coupled to baryon state.

## 5. A constructive remaining candidate: rotationally driven susceptibility

An independent energy reservoir can change that ordering. Consider the explicit toy

    L=I(chi) theta_dot^2/2 + Mchi chi_dot^2/2
      -mu_chi^2(chi-chi0)^2/2-e^2/(2chi),
    I(chi)=I0+b/chi,  I0,b,Mchi,mu_chi,chi0>0.

Both kinetic eigenvalues are positive. theta is cyclic, so angular momentum J=I theta_dot is conserved. Routh reduction at fixed J gives

    E_J(chi)=J^2/[2I(chi)]+mu_chi^2(chi-chi0)^2/2+e^2/(2chi).

The drive toward smaller chi at chi0 is present when

    J^2 b/(I0 chi0+b)^2 > e^2/chi0^2.

It is essential to hold J, not angular velocity, fixed. An isolated system cannot get the required work from an undeclared motor.

For dimensionless I0=b=Mchi=mu_chi=chi0=1, e=.1, exact polynomial root isolation finds one positive equilibrium in each example; all have positive local curvature:

| J | chi | matching stiffness 1/chi | change in inertia from chi0 |
|---|---:|---:|---:|
| 0 | 1.004951 | .995074 | -.246% |
| 1 | .862597 | 1.159290 | +7.964% |
| 3 | .039504 | 25.313944 | +1215.7% |

**The reciprocal cost is not optional.** Large stiffening in this example also greatly changes rotation. It cannot be inserted into the present rotation-curve fits with baryons held fixed. More generally, if f=(b/chi0)/(I0+b/chi0) and S=A/A0, then Delta I/I(chi0)=f(S-1). Small observational backreaction would constrain f and the phase energy, not disappear by calling the field dark.

The enhanced inertia admits a positive-energy auxiliary-oscillator realization, rather than requiring it as an unexplained algebraic substitution:

    L_aux=I0 theta_dot^2/2 + MX X_dot^2/2 + g X theta_dot
          -chi X^2/2 + Mchi chi_dot^2/2 - V_total(e,chi).

For chi>0 its Hamiltonian is

    H=(J-gX)^2/(2I0)+pX^2/(2MX)+pchi^2/(2Mchi)
      +chi X^2/2+V_total(e,chi).

Minimizing X at fixed J gives X=gJ/(I0 chi+g^2) and rotational energy J^2/[2(I0+g^2/chi)], reproducing b=g^2. This is a static or adiabatic elimination; a finite MX introduces a real dynamical mode and cannot be discarded at arbitrary frequency. The displayed squares prove positive kinetic energy in this finite-dimensional toy. They do not prove a covariant field theory healthy.

A local vorticity-mediated field version is a possible continuation, but it needs a specified baryonic current, material constitutive law, resolution-independent source, covariant constraint analysis and causal mediator dynamics. Pressure-supported systems can contain local vorticity or internal angular momentum; net J is not a universal classifier. No dwarf/cluster selection claim follows from this example.

## 6. What has and has not been gained

Gained: a common action-level diagnostic connecting matching to self-gravity; an explicit constant-coupling conflict; the derivative terms and critical scaling of a material-dependent alternative; a general passive-minimum obstruction; and a conservative driven toy with its energy and angular-momentum cost visible.

Not gained: a generally covariant parent; an allowed cosmic history; a selected a0 coefficient or microscopic length; a halo attractor; a finite cold inventory; a four-dwarf fit; cluster-core mass; retention or settling rate; permission to transfer old shear results. All new couplings remain model inputs.

**Strongest remaining route after these tests:** a dynamical, independently driven material state with a reciprocal mediator, tested jointly with baryon motion. The rotational toy is a precise candidate for that next reduction, not evidence that this is nature's mechanism. The separate A33 background/radiation route stays open as recorded elsewhere.

## 7. Evidence, limits and continuation

Final calculation families: `run2` (12/12), `scaling_run` (6/6), `phase_run` (4/4), `rotation_run` (10/10). Each has a sign/ordering mutation that fails, plus a v2 provenance manifest. Passing means the declared algebra/finite examples agree; it does not mean the theory passes. `run` preserves the initial inaccurate-decimal check failure. No claim is based on that failed anchor. All review in this directory is self-review.

Reproduction and pending obligations are in `HANDOFF.md`; the claim audit is in `AUDIT.md`. Subsequent work should begin with a full reciprocal field action for the mediator and baryonic current, then derive its FRW and rotating/nonrotating weak-field limits before any data fitting. The numerical toy has no dissipative channel, so it oscillates rather than necessarily settling. A physical radiation/receiver channel and its E/J budget remain mandatory.
