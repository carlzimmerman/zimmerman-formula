# Can elastic thermalization preserve the current target?

2026-10-11. The preceding elastic-exchange turn made progress by deriving a
signed, conserving moment and auditing its finite implementation. This turn
checks whether its simplest equilibrium can support the frozen CFG626 target.

## Exact ansatz calculation

Take a dilute classical elastic Boltzmann description in a static gravitational
potential, with acceleration -grad Phi and no bulk flow. For the local Maxwellian

    f(x,v)=n(x)[2 pi s(x)]^(-3/2) exp[-v²/(2s(x))],

elastic energy and momentum conservation imply f(v)f(v*)=f(v')f(v*') at each
position. Thus the local collision term vanishes, including for an
energy-dependent reversible differential cross section. The streaming term is

    [v.grad_x f - grad Phi.grad_v f]/f
      = v.[grad ln n - (3/2)grad ln s + v² grad s/(2s²) + grad Phi/s].

For this polynomial to vanish for every velocity requires grad s=0 and
s grad ln n=-grad Phi. A spatially varying Jeans dispersion does not make a
local Maxwellian an exact stationary kinetic solution. Jeans balance cancels
one moment, not every velocity coefficient.

This is a direct result for this ansatz. It does not invoke or establish a
classification of all stationary solutions. Nonthermal, open, metastable,
rotating, quantum and additional-force configurations are outside its scope.
A non-Maxwellian stationary state can have streaming balanced by collisions;
that possibility is not tested here.

## Frozen target screen, excluding the outer edge

Use the repaired nu_mono and six cell parameters from CFG626, extracting only
its kernel and CFG544 mass functions rather than running either campaign.
Keep the same softened force convention as the receiver energy audit:

    rho=M_ph'(r)/(4 pi r²),
    g=[M_b(r)+M_ph(r)-M_ph(0.001)]r/(r²+0.01²)^(3/2).

At each radius, hydrostatic balance would require

    s_required(r)=-r g(r)/(d ln rho/d ln r).

Evaluate 201 logarithmically spaced radii 0.03 <= r/r_star <= 0.8, away from
the natural truncation edge. Positive density and negative logarithmic slope
hold on this grid. For positive s_required, the best CONSTANT s minimizing
max |s/s_required-1| is 2*s_min*s_max/(s_min+s_max); its residual is
(s_max-s_min)/(s_max+s_min). This residual measures relative force imbalance
at fixed target density, not density error or observational disagreement.

| Cell | s_required max/min | Best constant s / Vf² | Maximum fractional force residual |
| --- | ---: | ---: | ---: |
| MW canonical | 1.0433 | 0.51330 | 0.02119 |
| MW alternative | 1.0361 | 0.51125 | 0.01774 |
| Cluster canonical | 7.6039 | 0.97502 | 0.76755 |
| Cluster alternative | 7.6043 | 0.97502 | 0.76756 |
| Compact canonical | 1.1865 | 0.54892 | 0.08531 |
| Compact alternative | 1.1804 | 0.54749 | 0.08273 |

The MW interior is approximately isothermal by this metric. The cluster target
is far from a constant-temperature hydrostatic profile under these assumptions.
This result is about the frozen CFG626 cells, not every possible halo or the
new CFG634 condensed-baryon source hypothesis. The latter was read at commit
1fea20013; its phase split is a new conditional proposal and is not substituted
silently into this calculation.

## A constructive implication, with the missing normalization exposed

In a spherical, self-gravity-dominated region, an isothermal solution with
rho=A/r² has M=4 pi A r. Hydrostatic balance gives

    A=s/(2 pi G),  v_c²=2s.

The approximately isothermal galaxy result is therefore physically consistent
with a flat outer rotation curve. Elastic redistribution could help maintain
this shape where the kinetic approximation and relaxation times permit it.
But the temperature s is a free scale in this family. Matching the repo's
amplitude requires s=sqrt(G M_b a0)/2. Elastic conservation alone does not select
that value from M_b and a0, and the singular isothermal family has neither a
finite total mass nor a natural outer edge. A realistic interior/edge and an
energy history remain necessary. This calculation supplies neither a target
attractor nor a timescale for reaching one.

## Evidence and consequence for the next transport calculation

`elastic_stationarity_v2.py` uses fourth-order logarithmic finite differences,
with density derivative steps one quarter of slope steps. Slope steps 0.02
and 0.01 give residual agreement within the declared 0.005 absolute tolerance
for every cell. A harmonic-potential isothermal control and a direct finite-
difference check of the streaming polynomial are independent controls. All
14 finite checks pass; the manifest validates recorded inputs and outputs.
The original `elastic_stationarity.py` run failed at parsing due to a missing
parenthesis, before producing scientific results. It and its failed manifest
are preserved; v2 repairs the syntax and uses a distinct output directory.

This is a bounded numerical profile screen, not an interval-certified continuum
bound. No old exponential-kernel hollow obstruction is used.

A transport calculation should therefore test TWO outcomes separately:
(1) whether collision-driven redistribution reaches an approximately isothermal
MW interior at the correct temperature without imposing it; and (2) whether a
nonthermal distribution or sustained energy flux can support the cluster
profile. A uniform Maxwellian bath imposed as the final state would preselect
one answer and cannot serve as a derivation of all six targets. The protected
quantum cold carrier remains intact as a candidate; its preparation, halo
normalization, finite edge and cosmological history remain unresolved.
