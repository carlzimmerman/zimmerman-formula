# Three closure doors: executable work orders

Scope: base `c8d5893d6a543495c464dbb3905574e3432a7475`. These are proposed calculations, not results. The latest target is **cold energy**, with spherical settled halos, finite shared supply and a fitted RAR target. The previous **modified-gravity filtered MONO** branch is a separate target; success for either does not complete the other.

## 1. An explicit energy bath for settling

**Smallest calculation.** Start with CFG489's canonical spherical 10^10-solar-mass infall and its unchanged target. Write a finite bath with its own energy, temperature, heat capacity and coupling equation. Enforce

`d(E_cold + E_gravity + E_bath + E_escaped)/dt = 0`.

Include settling-stress work explicitly. Derive exchange from the proposed coupling; an imposed isothermal condition or cooling function is not the mechanism. Before hydrodynamics, integrate a two-reservoir energy budget and check whether the bath can accept `E_initial - E_target` without heating enough to stop or reverse transfer. Check nonnegative total entropy production. Then linearize the coupled equations both at target and at CFG489's diluted states (`rho_target/rho = 10, 100`).

**Success/failure.** Advance only if finite bath capacity, the derived transfer time and off-target stability permit settling with positive temperatures and conserved total energy. Reject if a thermostat, hidden work source or unspecified escaping energy is needed. Freeze any new parameters before the first attractor run; passing this screen is not an attractor proof.

**Why new.** CFG489's target was too bound and its internal-heat repair failed. This door adds and accounts for a physical receiver of the released energy instead of renaming relaxation as cooling.

## 2. Conserved transport and competition for shared supply

**Smallest calculation.** Put two unequal spherical hosts in one finite reservoir. Evolve reservoir continuity with a declared transport law, initially

`partial_t rho + div J = -S1-S2`,
`tau partial_t J + J = -D grad rho - mu rho grad Phi`.

Deposit each sink into a separately accounted settled component. Specify capture from local states, not a preassigned baryonic quota; disclose this provisional closure and all coefficients. Use reflecting outer boundaries and compare isolated, overlapping and coincident hosts, then exchange their labels. Track total mass and each transfer.

**Success/failure.** Require nonnegative densities, exact mass accounting, label invariance and convergence of allocation under refinement. Reject double-counting, order-dependent ownership or coefficients adjusted per host. Determine whether irreversible retention survives the same equations; do not implement it by forbidding reverse flux without explanation.

**Why new.** This calculates competition through transport rather than rescaling overlapping catchments. **5.364 remains the initial abundance input; allocation does not derive it.**

## 3. Can a round halo survive a disk quadrupole?

**Smallest calculation.** Perturb a spherical halo by `Phi_b = Phi_b0 + epsilon Phi_b2 P2(cos theta)`. Linearize its stress or kinetic equations together with Poisson's equation; solve the forced density quadrupole and free `l=2` modes. Begin with the barotropic baseline `delta p2 = -rho0 delta Phi_total,2`. Report deformation versus disk forcing, without angular averaging.

**Success/failure.** Require a regular stable response and quantify roundness before comparison with R6. An unavoidable substantial deformation demands an explicitly derived supporting stress; instability rejects the closure.

**Why new.** Spherical placement and vertical-force fits prescribe geometry; this tests its dynamical support.

For the separate finite-halo/detuned-threshold-bath door, see [REPORT.md](REPORT.md).
