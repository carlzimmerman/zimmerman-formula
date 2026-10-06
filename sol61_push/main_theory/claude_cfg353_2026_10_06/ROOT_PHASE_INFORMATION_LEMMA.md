# Density and tidal information do not fix turnaround without phase information

Read-only starting input: Claude-associated CFG353 frozen criteria commit `c9d9a1d7b7a7accbf773424a5180f35ac85896f4` and its working-tree README/script. The new results were inspected, not authenticated by rerunning their computation or Lean output. This is a separate analytic implication of the proposed reader, not a correction to Claude's files.

## Conditional no-go

Consider Newtonian pressureless spherical initial data with a positive de Sitter acceleration H²r, in n>=3 spatial dimensions. A homologous uniform ball has outer-radius equation

`Rddot=-mu/R^(n-1)+H²R`,

where mu>0 is its force-normalized mass parameter, constant before shell crossing. Its conserved energy is

`E=Rdot²/2+U(R)`,

`U(R)=-mu/[(n-2)R^(n-2)]-H²R²/2`.

The potential has a unique maximum at `R_s=(mu/H²)^(1/n)`, with

`Umax=-n H² R_s²/[2(n-2)]`.

Fix exactly the same mass, density profile, radius `0<R_0<R_s`, and Newtonian gravitational potential, with the same boundary convention. Initial radial velocity is independent initial data. At rest, E=U(R_0)<Umax and the surface accelerates inward: this is a bound turnaround configuration. Choose instead positive outward speed with

`Rdot_0²>2[Umax-U(R_0)]`.

Then E>Umax, Rdot can never vanish on its outward trajectory, and it crosses R_s and expands without turnaround. Homologous velocity profiles preserve the same initial density and gravitational field. Therefore both initial states have identical *every-order spatial jets* of density and potential, hence identical instantaneous tidal eigenvalues, yet different turnaround behavior.

Consequently no instantaneous rule depending only on density and spatial derivatives of the Newtonian potential can classify bound/turning-around matter versus escaping matter for **all** these admissible initial data. Replacing CFG353's potential-zero estimator by a shift-invariant tidal tensor resolves the zero-point problem but does not supply the missing phase information. Spatial nonlocality of the same instantaneous density field alone also cannot distinguish this pair.

The claim does not exclude a conditional spherical-collapse threshold after imposing a growing-mode cosmological initial condition: that restriction supplies phase/history information, tying velocities to density. It also does not exclude readers of actual velocity, expansion, time derivatives, phase-space history, boundary dynamics or relativistic initial geometry/momentum. The Newtonian Poisson constraint has no velocity source; a GR claim would require separately solving its momentum constraint and comparing the appropriate full geometric data.

## Concrete four-dimensional control

Set n=3, mu=H=1 and R_0=1/2 in mathematical units. Then `U(R_0)=-17/8`, `R_s=1`, and `Umax=-3/2`. Rest is below the escape barrier. Outward speed 2 gives `E=-1/8>Umax`. This is a dimensionless mechanical example, not an astronomical parameter fit; physical units can be rescaled to a weak-gravity nonrelativistic regime.

## Implication for the research program

Claude's CFG351 phase-space direction and CFG353 tidal suggestion address different information deficits. Stream rank distinguishes multistream axes but turns on too late in the reported lensing test; tidal eigenvalues avoid a potential offset but cannot alone identify the dynamical branch. A serious next construction must retain phase information for still-single-stream infall, exclude unbound sheets/filaments and carry its action reaction and ownership rule. Existing theta-only obstructions remain relevant: adding phase information does not by itself establish a healthy switch.
