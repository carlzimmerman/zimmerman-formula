# Exterior basis and remainder estimates

This is the detailed ordinary-ODE justification of the outer-basis/Schur step in
ASYMPTOTIC_REVIEW_v1.md. It uses the actual frozen matrix and the exact local
Coulomb/neutral decomposition; it introduces no extra spectral count.

Let r be sufficiently large. A fixed G-orthonormal charge/neutral change gives
u_c in R6 and u_n in R4, with equations

u_c''=Qc(r)u_c+Ecc(r)u_c+Ecn(r)u_n,
u_n''=Qn(r)u_n+Enc(r)u_c+Enn(r)u_n,

where Qc=I-2I/r+diag(0,0,2,2,6,6)/r² and
Qn=diag(0,2,2,6)/r².
For some fixed finite d, the exact BPS formula implies
|Eab(r)|+|Eab'(r)| <= C r^d e^-r.
This generous bound suffices; some diagonal errors actually decay faster.
Increasing d absorbs fixed polynomial factors and differentiated profiles.

For every charged scalar channel choose the exact growing functions listed in
the independent check and exact decaying functions

c0: r e^-r,
c2: e^-r(r+1+1/(2r)),
c6: e^-r(r+3+9/(2r)+3/r²).

Their Wronskians with the normalized growing functions tend to -2 and are
constant, hence equal -2. For each finite N the growing asymptotic series has
a differentiable O(r^-N) remainder after factoring e^r/r. This follows directly
from the elementary/exponential-integral expressions; no convergent infinite
power series is asserted.

Neutral pairs are r^(l+1),r^-l for l=0,1,2, with Wronskian -(2l+1).
The neutral variation-of-parameters kernel is a constant times

r^(l+1)s^-l-r^-l s^(l+1).

All its factors are powers. A polynomial source r^q integrated from a fixed
large R therefore produces at most a polynomial, with a logarithm only at an
Euler resonance. Choose a finite M larger than d+4 and the homogeneous
degrees; logarithms are bounded by one additional power. All resulting
constants depend at most polynomially on R.

For the charged Green operator imposing no new growing amplitude, use one
integral from r to infinity and the stable integral from R to r. Its two
terms are constant multiples of

gplus(r) integral_r^infinity gminus(s) f(s) ds,
gminus(r) integral_R^r gplus(s) f(s) ds.

A polynomial source gives a polynomial response plus a stable exponential.
A source poly(r)e^-r gives a response poly(r)e^-r, possibly with a logarithm
from the second integral. Differentiating the formulas gives the same types
of bounds. These estimates follow from gplus=O(e^r/r),
gminus=O(r e^-r) and their exact scalar expressions.

For charged-growing columns, first solve the neutral Euler equation with zero
free neutral data at R for the source Enc gplus. That source is polynomial,
so the neutral tail is allowed to be polynomial/logarithmic. Substituting it
back into the charged equation produces a source poly(r)e^-r, whose charge
response is exponentially small relative to e^r/r. The direct Ecc gplus
source is polynomial, with charge response polynomial and therefore also
exponentially small relative to e^r/r.

More explicitly, take the charged normalized norm
sup_(r>=R)|r e^-r u_c(r)| and the neutral norm
sup_(r>=R)|r^-M u_n(r)|, including their corresponding derivative norms.
The charged-to-neutral operator is bounded by a polynomial C_R.
The neutral-to-charged operator, in the charged normalized norm, is bounded
by poly(R)e^-2R. Direct charged self-error is bounded by poly(R)e^-R.
The neutral self-error is bounded by poly(R)e^-R after integration with the
Euler kernel. Solve the neutral equation first and substitute it into the
charged equation. The resulting charged correction has norm
poly(R)e^-R+poly(R)e^-2R C_R, which is less than one for sufficiently large R.
This gives six exact charged-growing solutions with the prescribed charged
leading amplitudes and allowed polynomial neutral tails.

For the no-charged-growing sector, prescribe arbitrary neutral Euler
coefficients and optional charged stable amplitudes. Solve the charged
equation with the same no-growing Green operator. Its forcing from neutral
powers is poly(r)e^-r, hence its charged trace is poly(r)e^-r.
Solve the neutral correction using both Euler integrals with endpoint infinity;
this fixes its free-power coefficients. Their sources are exponential,
so the integrals converge and the corrections and derivatives are exponential.
Direct Enn errors remain exponential; feedback through charged components has
two exponential off-diagonal factors. The correction maps are contractive on
the corresponding exponential weighted spaces for large R. This constructs
the eight exact neutral-power modes and the six charged stable modes.
Together with the six charged-growing modes they have independent leading
data and form the full twenty-dimensional solution space.

The ten-dimensional no-growing subspace S consequently consists of the six
charged stable modes plus neutral powers1,r^-1,r^-1,r^-2. Wronskians between
these modes vanish at infinity, including the constant neutral mode, so S is
Lagrangian. The free neutral constant is correctly kept outside ordinary L².

After the global regular-connection ranks are supplied, use six independent
charged-growing regular columns and four regular columns with zero charged
growth. The actual wall is equivalent by a constant invertible row change to

PD u+PN(u'+u/r).

Since [Pcharge,PN]=0, the row space splits charge/neutral. Its charged6x6
block is (e^r/r)[A0+O(1/r)] with invertible constant A0; its inverse is
O(poly(r)e^-r). The charged wall traces of the four neutral regular columns
are O(poly(r)e^-r); the neutral wall traces of the charged-growing columns
are at most polynomial. Their Schur correction is O(poly(r)e^-2r).

The neutral4x4 leading wall determinant is a nonzero Laurent polynomial,
explicitly calculated with the allowed scattering coefficients in second-002.
Its inverse is bounded by a polynomial via the adjugate formula; adding an
exponentially small matrix does not change that property for large r.
Thus the Schur correction remains exponentially small relative to the neutral
wall block. It cannot change any algebraic first inverse-radius coefficient,
even though charged-growing columns themselves have polynomial neutral tails.

These construction estimates establish the exact asymptotic decomposition
and remainder order required by the kernel/rank and determinant arguments.
They do not supply the global regular-connection ranks independently; those
come from the separately audited ordinary L² kernel and Wronskian argument.

