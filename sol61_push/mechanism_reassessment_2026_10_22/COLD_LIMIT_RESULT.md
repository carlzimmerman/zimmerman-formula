# A fixed-mass finite kinetic sequence approaches the cold stiff profile

At fixed cold mass, reducing velocity dispersion moves the constructed finite bound equilibria toward an independently computed cold finite-stiffness reference. The strongest tested occupation gives total gravity within4.56% of that reference at four declared interior radii, including0.392% at r=1. This is numerical evidence for a useful equilibrium branch, not a proof of asymptotic convergence, observational agreement or dynamical formation.

## Controlled comparison

Keep the same identified-medium model and Plummer baryons as FINITE_KINETIC_RESULT.md. Units are GMb=a0=rM=1. Fix gamma=0.01, anisotropy radius ra=1 and total cold mass m_edge=1. The distribution is

    f(Q)=F Q_+, rho_hat=A Psi^(5/2)/(1+r²),

with A proportional to F under a fixed normalization. Vary A and shoot the central Psi to maintain the same finite-edge mass. This avoids making the profile look closer to the law simply by adding mass.

All four accepted trajectories reach their zero-density energy edge, remain below the polarization cap and have positive binding depth. Upper trajectories that approach the cap are used only to bracket a shooting search, never counted as solutions.

The initial coarse shooting probe missed the1e-5 mass gate at A10000 after independent tighter evaluation: mass shifted by5.62e-5. Shooting tolerance was tightened to2e-11, with final evaluation at2e-13 and unchanged gate. The remaining largest mass error is8.11e-7. The failed probe is retained.

## Independent cold free-boundary reference

At fixed positive stiffness, the correct cold interior balance is

    R(q)-gamma rho_hat'=gNb,
    m'=r²rho_hat,
    q=m/r², R=q²/(1-q).

The first contract paragraph transcribed the stiffness sign incorrectly; the force and numerical shooting equations always used the minus sign. The diagnostic residual was corrected and the amendment records it.

Solve these equations as a free-boundary problem: regular centre, m(edge)=1 and rho_hat(edge)=0, with the edge radius unknown. A collocation BVP, separate from the kinetic shooting integrator, gives

    edge=1.70504833560,
    central rho_hat=4.93857170,
    max q approximately0.448026.

The computed density is positive inside; its endpoint residual is below1e-18 in magnitude. Refining the BVP changes the edge by less than4e-13 relative. The exterior edge force is inward,0.0404131 in these units; the decreasing exterior force-ratio argument from FINITE_KINETIC_RESULT.md then applies. This is a finite-mass reference, not the infinite algebraic-law profile.

The old zero-stiffness algebraic relation is not an exact comparison target here, especially in the central stiffness-dominated region. The reference explicitly retains the same stiffness and cold mass.

## Results

Total gravity is gNb+q. The table compares it with the independent cold reference at the same radius.

| A | central Psi | kinetic edge | maximum fractional gravity difference at r=0.1,0.3,0.5,1 | difference at r=1 |
|---|---:|---:|---:|---:|
| 10 | 0.580171 | 6.65311 | 28.34% | 13.51% |
| 100 | 0.260468 | 3.00019 | 17.13% | 4.16% |
| 1000 | 0.110982 | 2.25950 | 9.47% | 1.22% |
| 10000 | 0.0459674 | 1.97210 | 4.56% | 0.392% |

Every difference in this table is a deficit. These four-point maxima are not uniform error bounds over the whole halo. The warm outer edge remains15.66% outside the cold edge in the last case, and the edge layer has not been resolved as an asymptotic limit.

The trend has a simple conditional scaling explanation. If density approaches a nonzero limit at a fixed interior radius, rho_hat=A Psi^(5/2)/(1+r²) implies Psi scales as A^(-2/5). The random velocities scale as sqrt(Psi), or A^(-1/5), and p_r/rho_hat=2Psi/7 tends to zero. This explains how the warm stress can disappear at fixed mass. It is not a proof that the full profiles converge, nor a reason nature chooses large A.

The positive-energy stability argument from ENERGY_CASIMIR_RESULT.md applies conditionally to each exact member of this family in spherical evolution. Its L2 bound is not uniform in the cold limit: the factor F grows and the velocity distribution becomes singular. Stability of a limiting cold fluid must not be claimed by simply taking F to infinity in that bound.

## The formation obstruction remains

Changing A changes the phase-space occupation, not merely a passive numerical resolution parameter. At the centre and zero velocity, f0 is proportional to A Psi_c. This quantity rises from5.8017 to459.674 across the four models, under the same normalization. Collisionless Hamiltonian transport preserves fine-grained values of f along characteristics. It cannot generally turn a lower-occupation initial distribution into an arbitrarily higher-occupation member of this sequence.

Thus the calculation shows compatibility of finite binding, stiffness and near-cold force response for chosen distributions. It does not show a spontaneous cooling trajectory from the first row to the last. A primordial distribution, an allowed collision/conversion process, or a fully accounted mass/energy transport mechanism would have to determine what occupation is reachable. No such process is derived here.

The total cold mass1 was fixed as a controlled test, not predicted. The cutoff, anisotropy radius, stiffness and distribution normalization remain inputs. The required galaxy/cluster population split, kappa and a covariant completion remain unresolved, and no raw observational comparison is claimed.

## Evidence

cold_limit_run/manifest.json validates and6 checks pass: valid finite edges, fixed mass, binding, cap avoidance, cold-reference admissibility and cold-reference refinement. Scripts are cold_limit_checks.py, cold_limit_response.py and cold_reference.py. No new mutation or dynamical evolution was run. The profile trend is reported data, not a separate proof-producing check. All preceding finite-family evidence was left unchanged. Mathematical interpretation remains self-reviewed.
