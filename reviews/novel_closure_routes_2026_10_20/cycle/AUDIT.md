# Independent audit of NCR-CYCLE-01

20 October 2026. **Primary verdict: proved as written**, for the declared
effective nearest-neighbor protocol and its explicitly conditional control
and cooling operations. This verdict does not establish a microscopic
writer, a retention time, a universal heat bound, or an entropy balance.

## Claim card and exact revision

The audited claim concerns three extended collective occupancy states
`n=0,1,2`, with real diagonal inputs `H0=0,H1,H2`,

    E_n(B)=Hn-Bn-Jn(n-1)/4,
    B0=H2/2-J/4,
    Delta=H1-H2/2+J/4>0.

The receiver has admissible energy `0<=Q<=Qmax`. Only adjacent occupancy
jumps are allowed, each changing Q by the negative of the state-energy
change. Field changes at held occupancy have work `dW=-n dB`, positive
when supplied to the latch/receiver. Initially
`0<=Q0<Delta` and `Q0<=Qmax`.

The precise assertion is that the pulse `B0 -> B0+Delta -> B0`, with
`0->1->2` at its upper bias and n=2 held on its return, either exceeds
receiver capacity or leaves the middle state accessible. Exported heat can
restore isolation. A specified symmetric erase pulse and receiver resets
close an energy-counted cycle. The article explicitly excludes a universal
claim over all controls.

Exact audited author file:

    reviews/novel_closure_routes_2026_10_20/cycle/COUNTED_WRITE_CYCLE.md
    bytes: 10380
    SHA-256: f219c7bcf2301013ec395f3f91816b1edd84056b7dfefde214b69ab3648a41cd

Additional read input, used only for the declared canonical functional and
its effective-shell convention:

    reviews/novel_closure_routes_2026_10_20/memory/RESULT.md
    bytes: 20704
    SHA-256: cf6f2ea2924c6662b7a7148b23acd4befadb1587633cab4438b948216113453d

No global novelty or earlier-packet verification is part of this audit.

## Dependency graph

1. **Convention/input:** the displayed energy, adjacent-only transition
   graph, receiver bounds and field-work rule define the effective model.
2. **Internal algebra:** writing `x=B-B0` gives
   `E=(0,Delta-x,-2x)`.
3. **Internal proof:** the write jump ledger and field restoration give
   `W=2Delta` and `Q_final=Q0+2Delta`.
4. **Internal proof:** receiver admissibility requires
   `Qmax>=Q0+2Delta`; the restored middle-state gap is only Delta.
5. **Internal proof:** nonnegative receiver energy and strict re-isolation
   require `Q0+Delta<Qout<=Q0+2Delta`.
6. **Conditional construction:** an external sink and occupation holding
   permit receiver reset and the explicit erase pulse. Their microscopic
   realization is not supplied by the model.
7. **Declared field input plus internal calculus:** the full-R conversion
   affinity gives the optional shell H; its derivative and endpoint limit
   are independently checked below. This input is unnecessary for steps
   2-6, which hold for every H1,H2 with Delta>0.

There is no circular dependence and no external theorem or numerical
computation is load bearing.

## Independent state and work ledger

The critical pulse and the alternate control path were derived from the
task's model before the author file was read. Let `x=B-B0`. The following
table uses cumulative work W and exported heat h. Every row obeys
`E_n+Q=Q0+W-h`.

| Operation completed | n | x | E_n | Q | W | h |
|---|---:|---:|---:|---:|---:|---:|
| Initial state | 0 | 0 | 0 | Q0 | 0 | 0 |
| Raise bias while holding n=0 | 0 | Delta | 0 | Q0 | 0 | 0 |
| Neutral capture 0->1 | 1 | Delta | 0 | Q0 | 0 | 0 |
| Capture 1->2 | 2 | Delta | -2Delta | Q0+2Delta | 0 | 0 |
| Restore bias while holding n=2 | 2 | 0 | 0 | Q0+2Delta | 2Delta | 0 |
| Export 2Delta | 2 | 0 | 0 | Q0 | 2Delta | 2Delta |
| Lower bias while holding n=2 | 2 | -Delta | 2Delta | Q0 | 4Delta | 2Delta |
| Neutral release 2->1 | 1 | -Delta | 2Delta | Q0 | 4Delta | 2Delta |
| Release 1->0 | 0 | -Delta | 0 | Q0+2Delta | 4Delta | 2Delta |
| Restore bias while holding n=0 | 0 | 0 | 0 | Q0+2Delta | 4Delta | 2Delta |
| Export 2Delta | 0 | 0 | 0 | Q0 | 4Delta | 4Delta |

The full loop therefore needs `Qmax>=Q0+2Delta`, field control reaching
`B0-Delta`, a work source supplying net 4Delta, and a counted sink accepting
4Delta over the loop. No restriction to nonnegative B was declared. The
loop returns the latch, bias and receiver to their starting values; the
work source and sink undergo the counted changes.

At the uncooled written endpoint, `2->1` costs Delta and changes Q from
`Q0+2Delta` to `Q0+Delta`. The subsequent downhill `1->0` returns Q to
`Q0+2Delta`. Both jumps satisfy the receiver bounds whenever the write did.
Thus an entire reverse passage is accessible. Accessibility alone supplies
no release timescale.

## Capacity and the strict heat threshold

For the exact unvented pulse, its only receiver-energy increase is the
2Delta capture release. Its capacity requirement is both necessary and
sufficient for this energy-admissible jump sequence. Calling the receiver
merely finite-energy would not specify a hard capacity; Qmax is explicitly
declared in the audited revision.

After heat export h at B0, endpoint isolation is equivalent to

    0<=Q0+2Delta-h<Delta.

Hence the allowable range is

    Q0+Delta<h<=Q0+2Delta.

In the continuous-energy model, the heat infimum is `Q0+Delta`; it is not
an attained minimum. At equality the receiver contains exactly Delta and
`2->1` is allowed, leaving Q=0. The note correctly uses a strict inequality.
Exporting 2Delta exactly restores Q0 and lies strictly above the infimum
because Q0<Delta.

This capacity result is pulse-specific. For example, precooling the
receiver before the 2Delta release changes its required capacity; a
receiver with `Qmax<2Delta` cannot accept that release even from Q=0 under
the isolated-jump rule. A simultaneous transfer directly to a sink is an
additional operation and requires its own ledger. None of these variations
alters the unvented-pulse calculation.

## Adversarial scope checks

The author's alternate zero-heat path is algebraically valid under the
additional conditional occupation-holding controls stated there:

    (n,x): (0,0) -> (0,Delta) -> (1,Delta)
           -> (1,-Delta) -> (2,-Delta) -> (2,0).

Its jumps are neutral. The held-n=1 sweep costs +2Delta; the held-n=2
restoration extracts 2Delta. It ends at n=2 with Q=Q0<Delta, zero net work
and zero exported heat. It is a counterexample to an unrestricted positive
write-heat theorem for energy-admissible paths, not to the specified pulse.
It does not count controller measurement, feedback, timing or reset costs
and does not prove a probability-one writer. The author now states these
limitations explicitly.

There is also a direct first-law check without intermediate re-isolation:
undo the original write by raising B to B1 at n=2, extracting 2Delta of
work, then use the retained receiver energy to pay for `2->1` at B1 and
take the neutral `1->0`. Restoring B0 at n=0 costs zero. The combined
write/reversal has zero net work and heat. It has no isolated written
intermediate state, so it does not defeat the re-isolation threshold.

Direct `0<->2` transitions remain excluded by definition. Finite rates,
kinetic barriers, microscopic channel suppression, physical control cost,
temperature and receiver/sink entropy are not inferred from the graph.
In particular 4Delta is this symmetric cycle's energy cost, not a Landauer
bound or a universal optimal-cycle claim.

## Supporting full-R shell calculation

From the declared canonical functional in the pinned memory input,
conversion at fixed T+F cancels the ordinary gravitational variation.
Varying its `G/2 integral T(s)^2/s^2 ds` counterterm and its remainder gives

    mu_switch(r)=integral_r^infinity [G T(s)/s^2+R(GT(s)/s^2)] ds.

For nonnegative subcritical T and `R(u)=u^2/(a0-u)`, this is nonnegative,
strict when T is positive on a set of positive measure beyond r. The
initial zero-stock marginal is zero. The initial author revision used an
unqualified strict inequality; the exact pinned revision includes the
required boundary correction.

For the shell, put `A=a0^2 r^3/(3G)` and
`f(x)=2x^3 artanh(x)+x^2+ln(1-x^2)`, with
`x=sqrt(GT/(a0 r^2))` and `0<=x<1`. Direct differentiation gives

    f'(x)=6x^2 artanh(x),
    dx/dT=G/(2a0 r^2 x),
    d[A f(x)]/dT=a0 r x artanh(x).

The last expression extends continuously to zero at T=0. The equivalent
primitive with H(0)=0 is

    H(T)=(2a0^2 r^3/G) integral_0^x z^2 artanh(z) dz.

For the cap, the exact identity

    f(x)=(1+x^3)ln(1+x)+(1-x^3)ln(1-x)+x^2

has limit `1+2ln2=1+ln4` as x tends to 1 from below. Thus the stated
`Hcap=A(1+ln4)` is correct, although the marginal affinity diverges. A
budget at least Hcap cannot alone bound x uniformly away from 1. This
does not admit x=1 as a regular state and supplies no real point-particle
Hamiltonian or nonzero-stiffness shell construction.

With fixed total cold profile N, the displayed baryonic cross energy is a
state function of M_b. Its change around a closed M_b cycle is zero. This
supports the note's fixed-density qualification and does not constrain
cycles that also move cold matter or change other couplings.

## Obligation matrix and remaining gap

| Obligation | Finding |
|---|---|
| Endpoint energies and invariance under a linear H convention shift | Passed |
| Every pulse jump and source-work sign | Passed |
| Capacity obstruction for the stated unvented pulse | Passed |
| Uncooled write admits middle-state and full reverse passage | Passed |
| Strict exported-heat condition and receiver reset | Passed |
| Symmetric write/erase first law and sink load | Passed |
| Alternate zero-heat path and protocol scope | Passed under its stated conditional holding controls |
| Shell primitive derivative and finite cap | Passed for the declared spherical effective input |
| Full-R affinity sign at zero stock | Passed in the corrected pinned revision |
| Microscopic H,J, graph, writer and cooling channel | Conditional inputs; not derived |
| Reliability, retention lifetime and entropy accounting | Not addressed, and not claimed |
| Literature or repository-wide novelty | Out of scope |

There is no remaining algebraic gap in NCR-CYCLE-01 as bounded above. The
strongest safe conclusion is an exact incompatibility between this pulse's
closed-receiver write and its original finite-energy isolation, together
with a conditional counted cooling repair. The cheapest next physical
check is to specify the actual holding/transition and heat-transfer
operators, then verify their finite rate, work and entropy costs. No new
scientific numerical run is needed to establish the present finite-state
accounting.

## Review provenance and validation

This is an independent subagent derivation of the critical pulse and its
control counterexample before reading the author's result, followed by an
exact-file audit. It is not an independent model validation or formal
certificate. The author adopted the independent scope counterexample and
the zero-stock sign correction before the final revision was pinned.

Validation used analytic reconstruction, the complete per-operation first
law above, and Python standard-library SHA-256 reads of the exact inputs.
No scientific simulation, numerical fit, symbolic package, job, frozen
criterion, old packet, publication or Git-state change was performed by
this reviewer. Only this audit file was written. Final mathematical
proofreading covered this new report: no unresolved notation or sign
issue remains; no mathematical token in the author file was edited by
the reviewer.
