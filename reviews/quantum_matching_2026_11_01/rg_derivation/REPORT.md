# TP02 independent running and matching result

The raw 49-field SU(5) action now has independently reconstructed and
checked one- and two-loop gamma/beta polynomials, including dimensional f
running and the two-loop gauge Yukawa trace. The full explicit tensor check
agrees with the separate analytic group reduction; all seven deterministic
cases and eight exact CS/field identities pass. This is running information,
not a complete finite two-loop threshold calculation. Here L=16π².

The substantive matching results are:

1. The complete one-loop threshold satisfies
   β1·∂U0=STr M⁴/(32π²), cancelling its explicit Q derivative. The old
   critical gauge relation is not preserved under RG and must not be reset.
2. Original X runs with −γ_X, whereas re-minimized canonical T runs with
   −γ_eff. A heavy A drift distinguishes a re-minimized tree valley from
   a fully transported background. The initial f_eff T product is invariant
   under the stated dictionary.
3. The reduced quantum potential at fixed original X has a well-defined
   CS log completion at two-loop order. It includes scale-log information
   about heavy relaxation implicitly, while leaving the finite reduced
   two-loop function uncomputed. RG-improving a tree-plus-one-loop formula
   does not calculate that missing function or the finite kinetic metric.
4. At fixed dimensionless field and jointly weak couplings, ordinary
   perturbative counting gives U1∼f²ε²/L and U2∼f²ε⁴/L², with possible logs.
   A conditional C² continuity inequality states exactly what omitted
   derivative bound would preserve a comparator pressure failure. Uniformity
   over the massless/light sectors is an open hypothesis, not a theorem.

A separate 12-case arithmetic check translates this last condition into
required derivative budgets without estimating the unknown correction. At
ε=.03, X/X_min=1.3, a common bound on |δU_s| and |δU_ss| must be strictly
below 1.9575×10⁻¹⁰ to preserve positive source, radial stability and the
negative comparator compressibility numerator there. Equivalently a proved
bound Cε⁴/L² would need C<6.02643. This is not a measured C, an exclusion
at ε=.03, or a native-phase-pressure condition.

`IMPLEMENTATION_REVIEW.md` passes the RG interface under its stated partial
matching scope: running f, X/T transport, full threshold log normalization,
CS-required log signs and non-reset critical drift agree with the independent
derivation. Completed numerical coverage and current hash validation are
recorded in VERIFICATION.json. The reviewer did not rerun those pressure
scans. Primary Martin–Vaughn v4 formulas were checked directly; source and
input provenance are retained separately. No scientific input or TP01
artifact was edited.

The remaining physical dependencies are the finite two-loop reduced
potential, finite kinetic matching, local heavy quantum/transverse control,
light/IR matching and an actual occupied state/material coupling. Small
matching-scale variation does not bound those missing functions. The
separate microscopic matter route determines which pressure criterion is
appropriate; the old exp(2s) waterbag portal remains a comparator here.

The main route subsequently calculated the finite normal-relaxation subset
from the full one-loop matrix tadpoles; its constrained Hessian, source
square and geometric angular pullback pass independent reconstruction.
All 28 declared RG/scale comparator cases and all four added-vacuum-relaxation
cases retain their pressure failure. The finite subset is gauge/scheme
dependent and does not bound the remaining diagrams.

The fresh occupied-state cross-review, `OCCUPIED_REVIEW.md`, checks the
actual rotating-field source square, Legendre Schur complement and full
P/energy/charge ledger. Its separate ε=.03 phase boundary is approximately
X/X_min=1.21263208 with w_ex≈.61567. This phase state is still stable at
the old waterbag's 1.2 witness and becomes negative in its own IR response
by 1.3; the different states and their pressure criteria are preserved.
Genuine finite vacuum/derivative matching and light/gauge/state control
still prevent a full physical pressure no-go.
