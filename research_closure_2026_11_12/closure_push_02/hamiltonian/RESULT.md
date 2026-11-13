# Fixed-charge dynamics and entry into the unstable region

The corrected Newtonian equations can actually be evolved. In a finite periodic experiment, a proposed repair of the flat gate starts with positive charge and nonnegative local short-wavelength response, then crosses into negative short-wavelength response during compression. The polarization constraint still has positive curvature at fixed charge. Thus checking that auxiliary curvature, or merely starting on the healthy side, does not protect this model.

This is a converged **finite leading-Newtonian experiment**, not a full Einstein evolution, cosmological initial condition, galaxy simulation or continuum existence theorem. The separate Einstein-constrained calculation and independent audit establish what the corresponding local principal instability means. No evolution beyond the first detected crossing is used as evidence.

## Action and exact reduction

Use the action and ordering derived in `../current_transport/DERIVATION.md`, with K=4piG and x=Q-1. Its conserved charge is n=H_Q+Pi. The material energy, before solving the polarization constraint, is

    e(n,Pi,P)=(n-Pi)x-H(1+x,Pi)+Gamma(Pi)+W(P).

Define A=H_QQ>0, b=H_QPi, c=1+b, D=H_PiPi-Gamma'', and let w>0 be the longitudinal Hessian of W. The local material Hessian in (n,Pi) is

    e_nn=1/A,   e_nPi=-c/A,   e_PiPi=c²/A-D,
    det Hess(e)=-D/A.

At spatial wavenumber k, polarization contributes w/k² to the Pi-Pi entry. Eliminating it gives

    h_eff=(w-D k²)/[A w+(c²-A D)k²],
    omega²=n0 k² h_eff-K n0.

The last term is the ordinary background-subtracted Jeans contribution. Ungated, w=K, b=D=0, this becomes

    omega²=-n0 A K²/(A K+k²),

which approaches zero at high k. In contrast, when D>0 and c²/A-D>0, h_eff tends to a negative constant. The growth then increases proportionally to k. Positive fixed-charge polarization curvature does not establish stability of the coupled charge and velocity.

One can exchange phase and density as canonical coordinates. The density coordinate has positive kinetic coefficient 1/(n0 k²), even when the conjugate phase action has negative kinetic coefficient. We therefore report the physical gradient instability, not an unqualified fundamental-ghost claim. `exact_run` verifies 29 exact identities, including direct differentiation of the three gate energies and the ungated comparison.

## Explicit candidate and initial data

The experiment uses the distinct repaired gate

    S(Pi)=exp[-max(Pi,0)³],    Gamma=gamma max(Pi,0)²/2,
    H=C x² S,                W=-|P|-log(1-|P|),
    C=10^6, gamma=10^-8, K=a0=Pi_c=1.

Clamping avoids the literal gate's exponential enhancement on negative Pi. It is C² at Pi=0; the one-sided stiffness retains its specified regularity. This change is explicit and is not silently attributed to the original action.

The periodic coordinate has derivative D_x=10^4 D_theta. Two disjoint smooth compact bumps give a narrow positive divergence peak of approximately .86 and broad negative compensation, with mean Pi zero. Recover P by Fourier integration. Set e_Pi to an antiderivative of W_P with mean -.15/C and solve the low quadratic root for h=n-Pi. This enforces

    -D_x e_Pi+W_P=0

and gives positive initial n. The initial velocity is -.001 sin(theta). The Poisson mean is explicitly subtracted for periodic compatibility. Initial |x| is below 2.19e-7 and |Phi| below 3.55e-9; the polarization cap fraction is below 2.86e-5. The polarization Newton solve uses the original derivatives, not a clipped or altered gate on accepted states.

Evolve

    n_t=-D_x(nv),
    v_t=-D_x[v²/2+Phi+x],
    D_x² Phi=n-mean(n),

solving the nonlinear polarization constraint at every RK stage. Stop at the first sampled D>0 with positive e_PiPi and negative h_eff at high k. The initial data have D<=0 everywhere and e_PiPi>0. This is a local material-principal condition; ordinary long-wave self-gravity is not asserted to be stable.

## Executed result and controls

All times below are in the declared normalized units; they are not astrophysical time predictions.

| grid points | timestep | first-crossing bracket | final maximum Pi |
|---:|---:|---:|---:|
| 256 | 1e-5 | [.001730,.001740] | .89613535 |
| 512 | 1e-5 | [.001730,.001740] | .89611114 |
| 512 | 5e-6 | [.001735,.001740] | .89611114 |

At the fine crossing, n remains above .0875, the minimum fixed-charge e_PiPi exceeds 2.38e-7, and D becomes 3.89e-11. The maximum speed remains about .001. Thus this is not caused by charge becoming negative or by crossing the polarization cap. The short-wavelength charge sound coefficient has just turned negative; its tiny first-crossing magnitude is expected because the run stops at entry.

Mean charge drift is below 5.6e-17. Recomputed material-plus-kinetic-plus-gravitational energy changes by less than 3e-14 relative in all three runs. The 256-to-512 maximum density change is 2.04e-4, while timestep halving at 512 changes density by at most 5.59e-11. The high Fourier-band fraction decreases from about 2.19e-4 to 1.07e-5. The spatial error dominates; no many-digit continuum crossing time is claimed.

Two controls run the same equations for the same interval. Zero initial velocity and reversed initial velocity both remain on D<=0. Their maximum Pi is approximately .85995 and .82754 respectively. The crossing is associated with compression rather than being a preexisting negative-principal initial state. These controls and the independent energy evaluation are in `controls_run`.

An [independent review](../health_audit/COMPRESSION_REVIEW.md) reconstructed endpoint constraints with FFT derivatives, without using the dense derivative matrix, and checked the energy and principal signs. Its ten accepted checks pass. Differentiating the polarization constraint along the actual Newtonian evolution gives positive peak D-dot, approximately 9.77448e-6, with tangent-constraint residual below 5.73e-13. This supports the direction of entry. It does not establish that the first tiny unstable spatial patch already resolves a high-frequency wave packet, and no such claim is made.

The raw fields, results, contracts, execution metadata and input hashes are preserved in `compression256`, `compression512`, `compression512half`, `controls_run`, and `exact_run`. Early exploratory profiles are archived under `exploratory`; an underresolved profile and a run that lost positive density are not promoted to accepted evidence. The literal-gate exploratory run also failed the proposed healthy-start interpretation and is explicitly excluded.

## What this changes

Clamping the negative-Pi side and declaring an initially healthy state is not sufficient to make the repaired gate safe under the derived Newtonian transport equations. An invariant-domain claim would need additional dynamics or a proven restriction that excludes this compression experiment. This result does not establish that a specific observed galaxy, cosmological history or fully relativistic solution follows this trajectory. It does remove a simple, previously untested escape from the local instability finding.
