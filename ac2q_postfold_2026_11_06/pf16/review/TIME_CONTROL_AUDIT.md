# Independent audit: conditional L1 time control

**Verdict: proved as written for an existing solution in the stipulated
on-branch bounded BV class.** It is a one-solution time-modulus estimate,
not a construction or a comparison/uniqueness estimate.

Reviewed `pf16/CONDITIONAL_TIME_CONTROL.md`, SHA256
`fe53f73a5fa0041649d15adc25652b7e4fddd4b3ccdbf54f73e58079ffc06807`.
Independent delegated audit, 2026-11-06.

The native scalar and compatibility equations give

    D_t U+D_x f=(S,0) dt dx,

with bounded S and a locally C1 flux in U and the Lipschitz auxiliary/
metric coefficients. Uniform compact positive-R inversion is essential
to the stated flux bound and holds in the declared neighborhood. The
BV slice chain estimate therefore gives, at almost every t,

    TV_x f(t)<=C TV_x U(t)+C.

Spatial BV slicing also identifies D_x f as the disintegration of its
slice derivative measures against dt. The spacetime measure equation
then gives the sharper structural statement

    (projection_t)_# |D_t U|
       <=[TV_x f(t)+||S(t)||L1] dt
       <=C[1+TV_x U(t)]dt.

Spacetime BV makes this right-hand side integrable on compact time
intervals. In particular no temporal null set can carry mass of the
projected variation measure, though the full spacetime measure may be
singular.

For a smooth spatial test vector psi with ||psi||infinity<=1, the balance
equation says its time pairing with U has an absolutely continuous
representative and derivative bounded by the same integrable function.
Integrating between Lebesgue times and taking the supremum over such
tests gives

    ||U(t)-U(s)||L1<=C integral_s^t(1+TV_x U(tau))d tau.

A countable dense test class may be used first to choose common full-
measure endpoint times. The common integrable majorant and completeness
of L1 then give a unique continuous representative and extend the
estimate to all interior endpoint times. Integrability up to an endpoint
gives the corresponding one-sided trace. Uniform slice TV strengthens
the estimate to Lipschitz continuity in the L1 norm.

This is metric/norm absolute continuity of the L1-valued curve; it
does not assert a Bochner L1-valued derivative or D_t U in L1 spacetime.
A translating continuous BV Cantor profile has an L1-Lipschitz time
curve while its spacetime temporal derivative remains a singular spatial
measure. The actual file explicitly preserves this distinction.

The on-branch restriction is also explicit and necessary for the stated
bounded-source equation with m=E h n^t. The full switch introduces the
multiplier current; its divergence is not automatically a bounded source
for that same choice of m. No full-switch time estimate is inferred here.

Finally, applying this estimate separately to two solutions does not
control their distance. The difference equation would require estimates
for spatial variation of the difference flux and for the difference of
the Jacobian sources, which the one-solution bound does not supply.
Nor does it derive the auxiliary Lipschitz bounds assumed at the start.
The result rules out temporal-marginal Cantor mass and strengthens
necessary time regularity within the actual weak class; acoustic
spacetime Cantor variation, continuous unbounded gradients, existence
and uniqueness remain unresolved by this lemma.
