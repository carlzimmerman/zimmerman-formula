# Independent audit: measurable positive interface clock speed

**Verdict: proved under the explicitly retained limiting balances and
trace identities.** PF11 nonactivation does not require an originally
continuous clock speed. Measurable positive speed bounded above and away
from zero is sufficient. This is a regularity improvement of the balance
lemma, not propagation of its geometric or current-trace assumptions.

Use proper interface time s, positive C1 transverse area a, and a
bi-Lipschitz increasing interface clock tau=phi_Sigma(s). Its a.e.
derivative v satisfies 0<v_min<=v<=v_max locally. Retain the identified
outer-flux identities and limiting scalar and Israel energy balances,
with locally integrable f=[T(N,T)]. In particular assume the charge and
energy measure relation has passed to the limit. They give

    q'=a f/v,
    y'=a f-(a'/(2a))y,
    q=2y/v>=0 a.e.,    y=a sigma.

Here q is the charge composed with phi_Sigma and primes are a.e. s
derivatives. The flux assumption and the bi-Lipschitz change of time make
q absolutely continuous; the energy equation makes y absolutely
continuous. The relation and nonnegativity extend q>=0 to its continuous
representative. No derivative of the original measurable v is used.

On any open connected component I of {q>0}, define

    v_rep=2y/q.

It is locally absolutely continuous on I and equals v almost everywhere.
Continuity of v_rep and the a.e. positive upper/lower bounds on v imply
those same bounds at every point of I. Substitute v_rep in the equations
and differentiate their product relation almost everywhere to obtain

    (q/(v_rep sqrt(a)))'=0 on I.

Thus q=2C v_rep sqrt(a), with C>0 for a positive component. If I has a
left endpoint where q=0, continuity of q and the lower bounds on v_rep
and a contradict this formula. If q(s0)=0, every hypothetical positive
component in the forward connected interval has such a left endpoint.
Hence no component can activate and q=y=sigma=0 throughout that interval.

This also follows using the formula only at a.e. points approaching the
endpoint; continuity of the original v at that endpoint is unnecessary.
The bi-Lipschitz clock change preserves the measure-density conversion
used by PF11, with d tau=v ds almost everywhere.

The conclusion requires that the limiting outer stress/current identity,
common tangential traces and Israel energy balance hold a.e. It does not
derive them from measurable v or from incoming BV clock traces. A
vanishing/unbounded speed, nonintegrable outer flux, missing initial
charge control, or undefined geometric/product traces remains outside
the proof. Thus loss of clock-speed continuity alone does not evade this
balance lemma, but incoming BV data alone do not establish the complete
PF11 layer class.

Independent delegated audit of the parent's PF12 measurable-speed
extension, 2026-11-06. No postbreak existence theorem is assumed or proved.

Actual-file follow-up: read `pf12/ROUGH_CLOCK_NONACTIVATION.md`, SHA256
`4bb11e6f01e40ace57a4d4bf7c0e50f9d0e52ab0b502da401ced10e56c46d8ea`.
Its equations, component argument and scope agree with this independent
derivation. Verdict for that exact file: proved as written.
