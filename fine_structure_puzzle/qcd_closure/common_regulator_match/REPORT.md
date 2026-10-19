# FSP-005 local charged bulk plus relative-wall collar match

At center holonomy v=pi/L, for h=v-a/r and B=n_mag rhat/r^2 compared with
constant v and zero field on the same relative wall, the matched local
one-loop inverse-radius coefficient is

    Gamma_local(R)|inverse = C_Gamma/R,
    C_Gamma = (L/pi)[11 log(2)(a^2+n_mag^2)/3+7a^2/6-a^4/3],
    C_logweight = -C_Gamma.

This fixes the magnetic harmonic finite scheme at mu=2pi/L and adds no
finite background-dependent wall matching functional. It is a local charged
bulk-plus-outer-collar comparison, not a complete monopole action or stress.

## Decisive convention correction

The frozen boundary Duhamel collar has zero flat mass first jet because
it describes the full smeared response. It accompanies the bulk density
after integration by parts. The unintegrated local diagonal bulk instead
differs by

    Gamma_bulk,diag-Gamma_bulk,IBP = integral Delta F0(h)/(12pi),
    F0(h)=sum_n,j c_j sqrt((2pi n/L+h)^2+M_j^2).

Its compatible collar must therefore include

    Gamma_collar,diag-Gamma_collar,IBP
       =-integral_outer partial_out F0(h)/(12pi).

At center this contributes -La^2/(3pi R). This correction follows both
from a direct two-derivative local diagonal calculation and from the
authenticated mixed a4 normal-potential coefficient. The earlier boundary
lane remains unchanged; its lower-wall +4La^2/(3pi R) term is retained in
the IBP/Duhamel collar, and becomes +La^2/(pi R) in the compatible diagonal
collar. Combining the diagonal bulk with the unconverted Duhamel collar
would overcount by La^2/(3pi R).

The separate terms, in units L/pi for C_Gamma, are:

| Contribution | IBP bulk plus Duhamel collar | Local diagonal bulk plus compatible collar |
|---|---:|---:|
| Bulk electric | [11log(2)/3-1/6] a^2 | [11log(2)/3+1/6] a^2 |
| Bulk magnetic | 11log(2) n_mag^2/3 | 11log(2) n_mag^2/3 |
| Quartic GPY potential | -a^4/3 | -a^4/3 |
| Profile wall term | 4a^2/3 | a^2 |
| Total nonlogarithmic electric coefficient | 7a^2/6 | 7a^2/6 |

The center reflection n -> -n-1 cancels the odd log/mass-jet sums at
finite PV mass. The same-domain pure cubic geometric surface counterterm
cancels against the constant-v reference at inverse-radius order. The
heavy-PV lower-wall term survives because the tower sum precedes regulator
removal. No modewise substitution M_j=0 is used for that limit.

## Matching data and scope

A finite common bulk coefficient shift delta_kappa changes C_Gamma by
-4pi delta_kappa(a^2+n_mag^2). Additional permitted finite boundary source
actions give a separate delta_C_wall. For example, reduced boundary terms
integral[K w(h)+z(h)partial_out h] change C_Gamma at center by
4pi a^2 w''(v)-4pi a^2 z'(v). These data are not fixed merely by cancelling
the pure geometric cubic wall counterterm. The displayed benchmark sets
them to zero. The allowed boundary matching class must be stated before
assigning a physical meaning to its finite coefficient.

The comparison fixes asymptotic v. Holding the wall value fixed while R
changes transports the entire profile by a/R and mixes lower bulk powers
into inverse-radius terms; a quadratic potential already introduces an
inner-cutoff-dependent inverse term, and the quartic potential introduces
log(R)/R. That is a different subtraction path.

Unknown pieces include the core, global angular determinant, neutral
sector, lifted modes and measure, deformation, screening and actual stable
saddle, and regulator-uniform remainder control. Magnetic flux also changes
the global charged bundle data relative to zero field; the present local
invariant comparison supplies no equality of global spectra. Metric stress
and electromagnetic normalization remain further missing maps. No alpha
selector is obtained.

## Evidence and checks

* `INDEPENDENT_RAW.md` was saved before any new root synthesis was read.
* `CONVENTION_AUDIT.md` gives the exact mixed-a4 flat-jet contraction,
  finite wall-matching examples, and fixed-wall transport integrals.
* `INPUTS_SOURCES.json` pins all consulted frozen scientific inputs and
  exact primary PDFs/hypotheses by SHA-256; full source texts remain temporary.
* `EXACT_CONTRACT.json` and `check_match.py` precontract a bounded exact
  rational/formal-polynomial check. `runs/match-001/manifest.json` has
  `run.status=completed` and validates with current input hashes.

The finite run checks the PV moment example, formal mass derivatives,
canonical normal-potential heat contraction, bridge integrals and equality
of the two matched coefficient polynomials. It performs no frequency fit,
root fit or physical-parameter fit. The Riemann limits and local remainder
scope remain separately stated hand arguments. Parent coordination reports
fresh independent agreement on the coefficient and representative conversion;
the review text itself was not needed or read to derive this result.

Self-proofreading covered all new derivations and coefficient/sign tables;
no mathematical-token edits were made after match-001 pinned its inputs.
Earlier boundary and far-field scientific files remain immutable.
