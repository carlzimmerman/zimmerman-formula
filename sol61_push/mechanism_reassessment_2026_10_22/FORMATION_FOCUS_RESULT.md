# Formation focus: source preparation is missing; reciprocal collapse begins without a prescribed ramp

User steering: stop damping refinement and investigate cold-seed origin and natural baryonic assembly. No further damping calculation was run in this checkpoint. The full formation mechanism remains unestablished.

## What the existing production evidence actually supplies

The current ARGON11 STATUS.md reports fragmentation of an initially coherent charged field into bound lumps, with unresolved resolution dependence. Its FROZEN_CRITERIA.md explicitly makes that coherent state and its noise amplitude inputs. This demonstrates conditional fragmentation, not production of the initial coherent population.

The existing nonthermal_state_2026_10_19/production_state/DERIVATION.txt studies the charged X/Phi action with X*Phi²+h.c. Its source population, phases, momentum distribution and epoch are preparation inputs. The decay can yield nonthermal daughters; low daughter speed requires a near-threshold mass splitting. Charge conservation does not select the source abundance or produce a coherent charged state from neutral initial conditions. ARGON's real-mediator model and this charged action are different theories and cannot be combined by importing their favorable pieces.

The identified-medium fluid model used in our assembly experiments contains a conserved mass current, not a particle-production equation. It therefore cannot, by itself, derive a nonzero cold population from an empty sector. A cosmological origin must be supplied through an actual parent and initial state. A literature discovery search found established coherent-scalar production routes, but none was imported as a solution: the necessary mapping to this theory and its couplings has not been derived.

## First autonomous baryonic driver

The prescribed beta ramps added baryonic mass externally. This new prototype instead holds both masses fixed and evolves a baryonic radius B together with the cold shells. Baryons are represented by a uniform homologous gas sphere. This is a deliberately reduced variational gas model, not resolved gas hydrodynamics.

For unit baryon mass and G=1 in the existing dimensionless units, its kinetic energy is3 Bdot²/10, self-gravity is-3/(5B), and its ideal-gas gamma_ad=5/3 internal energy is kappa/B² at fixed entropy. The experiment uses kappa=.3, an input entropy coefficient unrelated to the theory's fitted acceleration coefficient also called kappa elsewhere. To avoid ambiguity, this coefficient is a gas thermal-energy parameter only.

The baryonic potential at a cold node is

    Phi_b(r;B)=-(3B²-r²)/(2B³) for r<B; -1/r for r>=B.

Add sum w_j Phi_b(r_j;B) to the cold Hamiltonian from COLD_SHELL_DISCRETIZATION.md, retaining its central half-weight consistently. Varying this SAME energy gives both the cold gravitational acceleration and the reaction on B:

    (3/5) Bddot = 2 kappa/B³ -3/(5B²)
                  -sum_j w_j partial_B Phi_b(r_j;B)
                  -(dm/2) 3/(2B²),

    partial_B Phi_b = 3(B²-r²)/(2B⁴) inside, zero outside.

The cross term pulls baryons inward. There is no externally assigned mass-growth curve, friction, thermal relaxation or cooling. All source work is internal to the conserved Hamiltonian. The gas approximation assumes homology and fixed entropy; its pressure profile and shocks are not independently resolved.

## Executed collapse and failure

Initial conditions are a uniform cold sphere of radius6, a baryonic sphere of radius3, both at rest, with unit masses. The cold population is already cold and the gas is subvirial. These are explicit trial conditions, not primordial predictions or a cosmological turnaround solution. Both populations are gravitationally bound initially; this is not capture of initially unbound material.

At time6 the baryonic radius contracts to1.032 at32 shells and1.041 at64 shells. The cold half-mass radius contracts from4.762 to3.929 at both resolutions. Fourfold time-step reduction changes those early values negligibly. Saved energy errors through time6 decrease from about5.5e-9/1.2e-9 to3.5e-10/7.4e-11. This supports early reciprocal infall in the chosen reduced model.

The refined runs STOP at times6.548 and6.591 because an explicit integration stage reaches q>=1. They do not produce a settled cold object. The first runs stopped at6.509/6.340 with a less-specific domain guard; all failures are preserved. The v2 checks deliberately retain failed completion status, while the manifest validates the failure record.

Crucially, the discrete field energy diverges positively as q approaches1. A finite-energy trajectory cannot simply cross that barrier while the other coordinates and energy terms remain finite. Thus the explicit guard event is a numerical breakdown near a stiff region, not evidence that physical matter crosses the barrier or that the underlying theory is ruled out. The saved pre-failure energy samples do not bound the energy error at the failing step. An adaptive stiff or energy-controlled solver is required before interpreting the subsequent evolution.

## Route decision

The slow favorable ramp does not follow automatically from a closed gas-cold system: this prototype contracts rapidly instead. That makes radiative gas thermodynamics, pressure support, cosmological initial data and kinetic evolution at compression essential parts of the formation problem. They cannot be replaced by tuning a smooth history after seeing the desired final state.

Two active obligations now govern this work: derive cold population preparation from the existing parent fields, including abundance and initial momentum/charge; and complete a self-consistent gas-cold collapse calculation with justified gas thermodynamics. The immediate numerical continuation is the stiff reciprocal collapse, not damping refinement. The current source-preparation gap remains independent of any success of that collapse.

Evidence: reciprocal_collapse.py and reciprocal_collapse_v2.py, their contracts, outputs and failed manifests are retained. v2 manifest validates with run status failed; early contraction is conditional evidence only. Model variation and interpretation are self-reviewed. No novelty or completed formation claim is made.
