# Independent review of the root microscopic-current note

**Claim:** The selected Phi/X conversion action yields the source equations,
positive-sector charge/rest-mass relation, threshold quartic matching, and
the bounded operator checks in ../coherent_current/CURRENT_AND_MATCHING.txt.

**Primary verdict: proved as written**, for the algebraic claims under the
note's stated nonrelativistic, antiparticle-free, threshold and finite-sector
restrictions. The finite numerical observations were implementation-audited
and their manifest validated; this review did not independently rerun the
numerical evolution. No relativistic mass identity, settled/free transfer
rate, irreversible decay or gauge-compatible W follows from these results.

## Source and phase signs

An independent Euler-equation calculation in the relativistic convention
Phi=f exp(-i theta_rel), X=h exp[-i(2theta_rel+delta_rel)] gives
div j_Phi=-4g Im(X*Phi²), div j_X=+2g Im(X*Phi²).
For the root's slow fields,

\[
 \Phi={e^{-imt}\psi\over\sqrt{2m}},\quad
 X={e^{-2imt}b\over\sqrt{2M}},\quad
 \psi=\sqrt n e^{i\theta},\quad
 b=\sqrt{n_b}e^{i(2\theta+\chi)},
\]

theta_rel=mt-theta and delta_rel=-chi. Thus
g X*Phi²=c3 b*psi² and
div j_Phi=-4c3 Im(b*psi²)=+4c3 Im(b psi*²)=2R.
The source equation is div j_b=-R, with the root's positive
R=2c3 n sqrt(nb) sin chi. The symplectic term is exactly
-q theta_dot-nb chi_dot. The different signs of the named relative phases
therefore agree after translation.

For A=b†psi², the operator source R=i c3(A-A†) is Hermitian.
[Npsi,A]=-2A and [Nb,A]=A yield dot Npsi=2R and dot Nb=-R.
These signs agree with the classical limit and the conserved Q=Npsi+2Nb.

## Mass approximation and energy ledger

rho_rest=mq+delta nb follows directly from M=2m+delta. For delta>=0,
delta nb/(m n+M nb)<=delta/M; the lower bound is positivity of nb.
This is pointwise and also holds for expectations of the positive number
operators in the regulated homogeneous theory. It excludes antiparticles
and does not replace the full stress-energy source. The derivative
dot rho_rest+div j_rest=-delta R follows with the source signs above.
In the homogeneous model the remaining interaction-energy derivative is
+delta R, so the root's ledger is total-energy conserving.

## Full threshold versus source-only rotating-wave matching

The identity

\[
 {1\over4m^2-M^2}={1\over2M}
 \left[{1\over2m-M}-{1\over2m+M}\right]
\]

is exact away from M=2m. The original complex cubic gives a Phi Phi
s-channel source amplitude. In the convention -lambda|Phi|^4, the
threshold effective quartic is
lambda_tot-g²/(M²-4m²)=lambda_rep. By contrast the source-only NR square
subtracts g²/[2M(M-2m)], leaving a positive excess
g²/[2M(M+2m)] over lambda_rep. Including the negative-frequency analytic
piece removes this excess. The root's shift, its sign, the ratio
delta/(2M), and the conversion g_NR=lambda_rep/(2m²) all agree.
This does not assert the source-only finite operator Hamiltonian is already
the fully matched continuum theory; the root explicitly distinguishes them.

## Finite operator implementation

The enumerated Q<=16 space has 81 states and contains all states in each
reaction sector. The elementary raising matrices do have a top cutoff, but
every Hamiltonian composite conserves Q and its lower-then-raise
intermediates stay inside the enumerated space. In particular b†a²,
a†²b, a†²a² and B†B with B=b+(c3/delta)a² are represented correctly within
every retained sector. The 81-state composite-operator checks therefore
avoid a truncated reaction block. This does not establish canonical
untruncated commutators for arbitrary raising operations.

The stored run has 34 passing checks, four complete sectors Q=2,4,8,16,
and 101 times per evolution. Eigenspace time evolution, phase-reversed
vectors and the energy ledger match the declared model. Two vectors with
the same populations and energy but opposite source invalidate a universal
instantaneous density-only irreversible rate in this coherent setting.
The root accepted the terminology clarification **phase-coherent
superpositions in Q=2**, which avoids confusing the vectors with canonical
Glauber coherent states. It does not change the mathematical counterexample.

## Audit matrix and provenance

| Obligation | Status |
|---|---|
| Exact species source signs | Passed by independent Euler/commutator derivation |
| Relativistic/slow phase translation | Passed, delta_rel=-chi |
| Positive-sector mass bound | Passed, delta>=0 |
| Threshold and RWA distinction | Passed by independent propagator/amplitude calculation |
| Operator truncation and 81-state count | Passed for declared composites/sectors |
| Recorded finite evolution and manifest | Passed by code/output audit and manifest validation; not rerun |
| Physical coarse-graining, gravity response, capture | Not established here and not claimed by root |

Reviewed byte hashes after the terminology clarification:

| Artifact within coherent_current/ | SHA-256 |
|---|---|
| CURRENT_AND_MATCHING.txt | 93d507b4cf5a300f3bf6c6a66df373ff4bbb00454c0f5a80f70223787561802b |
| check_current.py | 66dd895a8703749d277d7ed39f79cf3a710623dc89bcaed6b8a0d122608d9ae4 |
| contract.json | 2f0fd750feee678afc174f48a5fc4d33c6c8b416d2c6fb6c74030471f1c6338a |
| run_001/results.json | 6e0c6bea06de5e27e0889cdba9d2347e1ad3ee636e20f02dc795d8692aa0fa61 |
| run_001/manifest.json | 79b51e395a48a8267109e2e937bdfca9eefdd2a4d610ac71ce2a2f04392ec325 |

Command executed: installed mathbox computation-audit `validate_manifest.py`
on coherent_current/run_001/manifest.json with the project root. Result:
valid evidence record, run status completed. No parent note/code was edited
by this review. This is a separate agent's reconstruction after seeing the
raw note and code, with access to shared project context; it is not a blind
or externally independent referee report.
