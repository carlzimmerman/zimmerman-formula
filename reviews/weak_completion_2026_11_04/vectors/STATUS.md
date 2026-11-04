# CC11 vector leaf — finite transport complete, global candidate open

Preferred vector1↔2 implementation is frozen `transport_v3.py`, `rates_v2.py`
and `run_table003/result.json`. It evolves thirty physical groups with separate
massive-vector L/T occupations, their actual momenta, inverse reactions,
quantum factors, charged returns, and common-background energy/force. All24
canonical gauge generators and all physical VSS/VFF/SVV tensors are used.
Tree VVV cuts are explicitly zero/closed. This is an actual transport operator,
not a vector eligibility fraction or terminal-radiation prescription.

Preferred **portable cold self-elastic** implementation is
`coulomb/elastic_builder_v3.py`, `scalar_factory_v3.py`, `template_v2.py`, using
root's frozen `integration/binary_events_v2.py`. The previous starred-subscript
syntax in builder v1/v2 was valid in the actual Python3.13 experiment environment
but not root's Python3.9. `run_portable313001` proves the portable rewrite is
bitwise identical, and `run_portable39001` reproduces all five coefficient,
weight, index, measure and energy fingerprints in actual Xcode Python3.9.6;
RHS/Jacobian differences are below6.2e-16. Use the v3 factory for root integration.

## Tested outcomes

| Record | Tested result | Precision/scope |
| --- | --- | --- |
| `run_transport003` | Goldstone/Ward, boost, quantum detailed balance, H theorem, physical-number Jacobian and bosonic vectors pass | Local x3.8632,5,25.4000; angular order2→8 warm RHS~2e-6, order4→8~4e-10 |
| `run_normalization005` | Independent Dirac traces, absolute Weyl/Dirac/scalar widths, signed charge, twelve-colour width degeneracy, VVV closure | Trace errors~3e-16; no P decoherence assertion |
| `run_population002`, `run_refine001` | Six finite steps over three vector lifetimes on actual conditional warm packet; physical vector force and both forward/inverse charged currents retained | Full vs SF-only photino number+0.789%, gas force+1.001%; halving dt changes vector population2.21%, charged5.3e-7rel, photino4.2e-5rel; vector seed1e-25/45 changes<6.3e-11rel |
| `run_cold002` | Hard-tail-resolved dilute F8_2 impulse at actual pole produces V, then charged returns; P direct vector cuts close | qmax~7.75e5 at Tc1e-6; charged carriers1.99166 per injected parent after three V lifetimes; energy drift1.65e-13; conditional Green response |
| `run_coulomb003` | Actual cold scalar relative-speed convolution and positive static screening; colour factor7/12 | Self dp²/(p²H)=.0299 initial, .1908 memory endpoint, .8216 hybrid endpoint; Born-low-speed fraction of diffusion<2.4e-6, but up to22% of a Born collision count is in that uncertain region |
| `run_elastic_relax001` | Positive conservative quantum2↔2 evolves actual cold holes | Over0.1/H, shape L1 changes2.14%; N/K conserved to~1e-13/1e-14; physical pressure/force leading invariants remain constant; dt endpoint L1 difference2.87e-4 |
| `run_elastic_operator001`, `run_elastic_template001` | Angular and dynamic-log template controls | Actual RHS L1 angular difference1.04%; template vs fresh kernels at three actual T/shapes .204%, .126%, roundoff. These are finite tested controls, not continuum error bounds |
| `run_coulomb_bath001` | Actual late neutral-cascade λ3/λ8 cohorts reconstructed with redshift | Charged momentum diffusion/heating .0003444/H; continuous-stream fmax<3.6e-10; these late baths are subpercent. Earlier legacy λ bath has no recorded shape and is not invented as FD |
| `run_late_kernels001` | Actual4P channel/work pretable, massive terminal transfer and delay | Seventeen orbit points; five named weighted interpolation checks≤.091%; maxHdelay6.51e-7; terminal energy error<1e-9 |
| `run_cold_split001`, **`run_cold_split002`** | Full *conditional old late window* Tc1e-5→1e-6 with accurate positive annihilation halfsteps, quantum C-C elastic, actual massive neutral cohorts, redshift, force and signed scalar work | Fine noelasticY1.7235110633e-13; elasticY1.7259997896e-13 (+.144399%). Coarse effect+.143726%; differential dt change6.73e-6 relative charged number. Neutral pressure−.057181%; recorded-orbit force shift<2.2e-7 amplitude and action correction<6.9e-8 |
| `run_chemical001` | Actual cold C C*→unbroken gauge-pair rate and colour-weighted Coulomb Sommerfeld reference | Canonical annihilation factor13/4. Γchem/H≤3.34e-13 tested; Sommerfeld means1.00030..1.00300; no arbitrarily-late Born/formation theorem |
| `run_warm_ann002`, `run_warm_vector_ann002` | Conservative S/F/vector gauge-annihilation diagram-norm estimates on actual warm packet | Combined all-charged fractional loss/H bound~.0006024; vector part1.52e-8. Positive quadrature and spin sums reported; no exact-interference cross-section claim |
| `run_opacity001` | Tree χ+C↔F narrow-line absorption of late hot χ | Exact spin ratio1; Γin3.88947e-13μ; resonanceE.000603774μ; maxcoldτ.00066261, off-resonant current estimate≤1.72e-9. Early warm χ survival not assumed |

## Energy qualification

The cold split runs retain the **raw** energy-plus-FRW-work residual. Its
maximum is about4.24e-8 of the initial charged-plus-oscillation energy, and the
explicit full model residual is approximately−4.22e-8 of that reference. The
finite-width, radial-cell projection, parent-boost and source interpolation
contributions remain separate. The much smaller residual after subtracting
those terms is an accounting closure; it is **not** an independent certificate
that the finite-width source exactly conserves physical energy. Positive
annihilation ODE source quadrature and the elastic solver are independent.

## Coverage and remaining physical obligations

The cold self-elastic factory is restricted to Sc_0. It is appropriate to the
recorded late scalar-dominated packets, not to an arbitrary epoch with abundant
charged fermions, heavy branches or other gauge baths. Initially the specified
packet is charged-fermion FD with empty daughters; neutral production and
charged returns create scalars and vectors. F↔C+λ thresholds and inverses must
therefore decide the species mix dynamically. A new common history must verify
when the scalar-dominated, nonrelativistic regime is reached. The old CT09
fermion depletion cannot be imported as a new-history fact.

The late bath probe includes the actually reconstructible neutral-cascade
λ3/λ8 cohorts. Legacy early radiation/event counts do not specify their
occupations or screening. A new common calculation must carry that bath.
Warm fermion/scalar/gaugino elastic redistribution, other populated massive
colour baths, and reactions not bounded by the present finite packets remain
separate coverage obligations if material. Gauge annihilation bounds here do
not implicitly bound every conversion or off-shell reaction. The cold
self-elastic kernel is a screened direct-t Born/leading-log description;
finite-log exchange/contact terms, dynamic screening and a nonperturbative
low-relative-speed completion are not promoted to exact QFT transport.

The four P states remain coherent physical parents. Their vector absorptive
matrices and canonical frame columns are provided in `run_normalization005`;
a diagonal population transport calculation does not prove decoherence.
The conditional cold stage uses the prior vacuum memory model and tree
cascade terminal map. It does not silently include the newly matched loop
neutral exits or an occupied dispersive selfenergy. The small force/work
correction validates only its recorded-orbit first-correction scope.

**No old late endpoint is spliced onto the new common warm history.** The
fixed warm packet also inherits its old energy/coherence limitations. Root's
fresh common evolution is a separate calculation. These results do not prove
candidate viability, cold photino DM, or a complete charged-relic history.

## Failed and superseded evidence

All failures, source bytes and logs remain. They include import-name collisions,
a measure tiling error, a tiny protected-channel cancellation fixed in v3,
incorrect common/raw-index use in an independent audit test, zero-width metadata
counted as a charge violation, a wrong expectation that a *net* return must be
positive, missing explicit hole flags, an insufficient relative-convolution
rule, and a subnormal ghost-cell Jacobian overflow fixed by root's binary v2.
`run_elastic_builder001` also used an unnecessarily large78-node diagnostic
(27.6M rows, measured12.49GB RSS); no such job is repeated. Preferred finite
relaxation used~0.76GB; portability control~0.94GB. Larger angular diagnostics
measured1.4–1.83GB and are not production recommendations.

The fully implicit cold-stage002/003 records are valid but have shared chemical
BE time bias. The positive split pair supersedes them for endpoint comparisons.
The warm-annihilation001 records normalized by all gas particles; corrected002
records use all charged carriers and are preferred. See
`ENVIRONMENT_ERRATUM.md` for the original launcher's incorrect historical
software strings. Later launchers record the actual per-job interpreter and
library versions; root Python3.9 jobs are distinguished explicitly.
