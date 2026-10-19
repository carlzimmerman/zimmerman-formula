# FSP-009 common-response result

The full A_rho(u), individual-proton M_u, R and physical alpha remain open.
This route supplies a new exact comparison map and a controlled non-Born
threshold discriminator. Candidate science is frozen in
[RAW_DERIVATION.md](RAW_DERIVATION.md), SHA256
`368ef3171872e5f00f02aa64703582829e2d92ed88f6776eb17e5bdb31205fab`.
The author's self-review is separate; fresh review is arranged by the parent.

At m_u=m_d>0, exchange the up/down charges of the current while keeping the
same QCD theory. Vector-isospin relabeling proves that the unconditioned
vacuum functional, its electromagnetic insertion and its complete metric
response are unchanged at every radius. In particular

    Delta_S rho_u(g)=0, and Delta_S A_u=0 if that limit exists.

This includes disconnected vacuum contractions, I_t, trace covariances and
all exchange-covariant metric/source/matching contacts. The corresponding
proton response maps to the neutron response. Its charge-odd non-Born
tensor is the p-n tensor, which is allowed by isospin and is not determined
by the singlet vacuum expectation.

The actual non-Born chiral coefficient is authenticated in
[BKSM, hep-ph/9309211v1](https://arxiv.org/abs/hep-ph/9309211v1), (6)--(10),
with the explicit nucleon-pole exclusion checked in
[the companion, hep-ph/9311354v1](https://arxiv.org/abs/hep-ph/9311354v1),
following (8). Writing a=a_E/u, b=b_M/u, it gives the sequential chiral
logarithmic derivatives

    partial_logMpi (a_p-a_n) -> g_A^2/(16 pi^3 F^2 m),
    partial_logMpi (b_p-b_n) -> (1+kappa_s)g_A^2/(16 pi^3 F^2 m).

Here kappa_s=kappa_p+kappa_n; no empirical value is assigned. Analytic
polarizability contacts disappear from these leading mass derivatives.
The source logarithm itself is known; its use in the exact vacuum-null
comparison is the new project step. This is distinct from the M_u
proportional to M_pi relation already calculated in FSP-003.

The complete SO(4) soft-photon angular contraction, derived from both the
Euclidean polarizability action and the parent's full T1/T2 formula, is

    C_soft^NB := lim_(K->0) M_u^NB(0<Q<K)/K^4
               = 3(a-b)/(32 pi).

Thus the new charge-odd scalar-current coefficient is

    lim_(Mpi->0) partial_logMpi (C_soft^p-C_soft^n)
       = -3 kappa_s g_A^2/(512 pi^4 F^2 m).

K->0 is taken first at fixed positive M_pi. The kappa_s-independent
electric and magnetic logarithms cancel in the full angular integral.
On the exceptional kappa_s=0 branch the displayed soft mass logarithm
vanishes; the electric tensor coefficient remains. Taking only the
magnetic subtraction or only the electric logarithm would miss this check.

The finite exact coefficient differences and independent angular/radial
contractions passed in `run_001`. The numerical angular diagnostic used
four rational (a,b) pairs and 1024/4096 Simpson intervals; its largest
absolute residual was 9.44e-18 against the 2e-13 tolerance. The v2 manifest
has `run.status=completed`, validates against current inputs, and records
all before/after hashes. This finite run supports the algebra; it is not
a QCD simulation or proof of the chiral remainder hypotheses.

The result excludes a flavor-covariant Ward identity reconstructing the
entire proton non-Born tensor from only the unconditioned vacuum mixed
metric/current functional. It does not prove that the complete p-n M_u
cannot accidentally cancel after all momenta, subtraction and finite
counterterms are included. Nor does it refute a dynamical relation at one
physical charge assignment or determine a nonzero A_rho. No local R or
fitted nonlocal contact is used as an obstruction.

The remaining physical leaf is the isospin-even individual-proton
non-Born tensor over all momenta, finite QCD/QED matching and its independent
unconditioned S4 response. Physical m_u != m_d adds an isovector scalar
insertion. The exact fixed-theory null statement must also be projected
with the inherited calibration Jacobian before comparing separately
proton-retuned paths; RAW_DERIVATION (12) makes that distinction explicit.

Deliverables and provenance: [contract](CONTRACT.md),
[sources](SOURCES.json), [transcribed coefficients](source_coefficients.json),
[code](check_common.py), [run manifest](run_001/manifest.json),
[result](run_001/result.json), [reproduction](REPRODUCE.md),
[self-audit](SELF_AUDIT.md), and [ancestry pins](INPUT_PINS.json).

Route C1 is a completed structural checkpoint, not completion of the full
research target. Further physics work is deferred until the parent's fresh
review or new common-regulator data changes the surviving leaf.
