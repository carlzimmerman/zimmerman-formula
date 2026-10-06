# Finite-Fourier pure-decay scalar admission obstruction

Every nonzero zero-mean **finite real Fourier polynomial** pure-decaying relative scalar seed on a flat three-torus violates the second-order local clock equation of the unchanged projected action. Different Laplace eigenvalue shells cannot cancel the extremal doubled Fourier coefficient. The result closes the multiple-shell loophole in the parent eigenshell theorem for this finite-support scalar class.

This is not a no-go for the full space of vacuum perturbations. Additional independent relative vector or flat-sector data, smooth infinite-support Fourier fields, noncompact boundaries, different backgrounds/operators, and nonregular nonlinear branches are unclassified. Arbitrary common first-order data cannot change the leading coefficient, but additional relative data need not share the scalar shift used here. No ghost, cold abundance, spectrum or 32π selector is inferred.

## 1. Actual clock current and permitted first-order seed

Use n=3, K>0, a=exp(Ht)>0, H>0 and the parent coincident empty de-Sitter projected-acceleration action,

S_int=2K a0²∫v M_eff(I),
I=(P_g+P_hat)^{μν}(a_g−a_hat)_μ(a_g−a_hat)_ν/(2a0²),
M_eff,I(0)=1/2.

Normals are defined by the common timelike clock, with signature −+++. In its unitary chart, I=h^{ij}∂i r∂j r/a0², h=(γ inverse+hatγ inverse)/2 and r=ln(N/L). This calculation retains the eliminated norm-cube envelope; no alternative clock operator or auxiliary fit is inserted.

The normalized-clock acceleration variation at fixed ADM metric is δa_i=−π_it+∂i(S^jπ_j)−[(∂t−S·∂)ln N]π_i. Expanding a pure-relative first metric perturbation about coincidence gives δA_i=∂i(ΔS·∂π)−νdot π_i. The zeroth common −π_it cancels. The full temporal/projector contraction has no additional quadratic term because A_0 has no linear term and the unitary projectors' time row is zero. Periodic spatial integration yields the actual Euler density

Eθ,2=2Ka div[(Δν)ΔS+νdot gradν].

An independent temporal-covariance reconstruction also obtains this current. A metric Lie deformation ξ0=T gives δr=Tνdot−ΔS·gradT and δ(vh)=a(Tdot+HT)identity at background order. Varying Ka(gradν)², time integrations cancel its Tdot/HT terms and leave 2Ka[νdot gradν+(Δν)ΔS]·gradT. The clock Euler density is its negative integrated metric coefficient, exactly as above. This route checks the time normalization and density/projector effects without assuming an arbitrary spatial force action.

The allowed seed is the actual linear pure-decay relative scalar, with no additional independent relative vector/frozen-flat data. Write ν=a^(−1) f(x), f a finite real zero-mean Fourier polynomial. Mode by mode the parent constraints are z=−ν, e=2ν, νdot=−Hν and β_k=2Hν_k/P_k, P_k=|k|²/a². Since the contravariant relative shift is a^(−2)grad β, its exact multi-mode form is

ΔS=2H grad(−Δ)^(−1)ν,
ΔS_k=2H i k ν_k/|k|².

The inverse Laplacian is defined on the zero-mean torus subspace. This is the required shift selected by the scalar constraints; it is not an independently tunable compensating vector field.

## 2. Derive the Fourier kernel

Let S be the finite set of nonzero reciprocal-lattice wave vectors with ν_k≠0, and write ν=∑_(k∈S)ν_k exp(i k·x). A real field has ν_(−k)=conjugate(ν_k); the coefficients need not be real. Fourier multiplication in the actual current gives

−ν gradν→−i∑_(k+l=p) l ν_kν_l,
2(Δν)grad(−Δ)^(−1)ν→−2i∑_(k+l=p) |k|² l ν_kν_l/|l|².

Taking the divergence therefore gives exactly

Eθ,2,p=2KaH∑_(k+l=p)(p·l)[1+2|k|²/|l|²]ν_kν_l.

This is an ordered-pair convolution. In particular E_p=0 at p=0 for every seed: the integrated clock-relabel row cannot distinguish it. On a single eigenvalue shell the symmetrized kernel is 3|p|²/2, reproducing E=−3KaH Δ(ν²). Multiple shells require the following different argument.

## 3. Uniform finite-support theorem

Choose k*∈S of maximal squared Euclidean norm. It is nonzero. This gives a constructive uniquely exposed support point: for every distinct j∈S,

k*·k*−k*·j=(|k*|²−|j|²+|k*−j|²)/2>0.

Thus the linear functional k→k*·k has a unique maximum at k*, even if other modes have the same norm. A generic exposing functional would also work; this explicit one avoids a genericity choice.

If k,l∈S and k+l=2k*, applying the functional shows that both terms must attain its maximum. By uniqueness k=l=k*. Hence no cross pair contributes to p=2k*. The exact residual coefficient there is

Eθ,2,2k*=12KaH |k*|² ν_k*²
          =12KH |k*|² f_k*²/a ≠0.

The square is a complex square, not a squared modulus; either is nonzero for a nonzero scalar amplitude, but they are not interchangeable as Fourier coefficients. The reality condition supplies the conjugate residual at −2k*, so the physical real Euler field is nonzero. For a real cosine of amplitude B the complex coefficient B/2 reproduces the parent real residual 6KaHk²ν_amp² cos(2kx); a sine has the opposite second-harmonic phase. No positivity of individual complex residual coefficients is claimed.

This proves the theorem for any finite support, arbitrary finite number of different eigenvalue shells, arbitrary phases representing a real field, and any finite nonzero amplitude coefficients. The finite fixtures below are not extrapolated into the proof. The strict exposure identity also applies with the fixed positive flat spatial inner product on a differently normalized torus; the actual normalization here is the parent's a² identity metric.

## 4. Why second-order corrections cannot repair this tangent

At exact coincidence the common clock cancels from the full quadratic action, including metric-clock mixing. Thus Eθ^(1) is zero as an operator on arbitrary first-order metric and clock fields. For a regular order-by-order family whose field/Euler jets possess the stated amplitude expansion, the clock equation at order two is Eθ^(1)[q2]+Eθ^(2)[q1,q1]=0. The first term is identically zero and the extremal residual in the second is not; no ordinary second-order fields can cancel it. This is compatibility of the full metric system under diagonal covariance, not an extra independent propagating equation appended by hand.

The norm-cube contribution has M_I correction O(|ε|), while the common-clock variation of I starts at ε² for relative first data; it therefore enters this clock row only at higher order. The lack of a general third Taylor derivative of that envelope does not invalidate the second-order clock coefficient used here.

Adding common first-order metric or clock data does not alter this leading relative quadratic coefficient. The clock functional is exchange even in relative data and identically zero on the equality slice for every common metric/clock; its lowest nonzero term is relative quadratic at the fixed common background. Common first-order changes act on that coefficient at the next order. This reasoning does not exclude **additional relative** vector or flat-sector first data: they can modify ΔS in the current and are outside the scalar shift premise above. Nor does the proof address a different admitted background.

Finite support is essential to the current proof: general infinite lattice support need not have an exposed maximum. Approximation by Fourier polynomials does not supply a uniform lower residual bound because an extremal coefficient can become arbitrarily small as the support changes. No conclusion about all smooth or analytic infinite-support seeds follows. Singular/nonuniform amplitude expansions, nonperturbative source branches and noncompact flux also remain outside the theorem.

## 5. Bounded checks and scientific implication

checks.py computes the source in two separate ways: differentiating/multiplying Fourier dictionaries for the raw current, and the ordered kernel formula. Five exact real fixtures include cosine, sine, different shells, complex phases and equal-norm extremal modes. A 124-mode integer-grid fixture checks constructive exposure and pair uniqueness. It also checks the time/prefactor dictionary, zero integral and the parent eigenshell limit. Three controls discard the shift term, keep only the integrated row, or replace the complex square by a modulus square. The latter control protects phase information rather than introducing a positivity assumption. Current contracts and manifests carry the exact tested bounds; count alone is not the theorem.

The linear signed dustlike stress dictionary remains valid algebraically, but no nonzero finite pure-decay scalar Fourier seed in this class is a regular tangent to a local second-order solution of the retained action. The previously solved homogeneous mean response is still a correct necessary-row identity and still insufficient for admission. The next changed premise is an explicitly allowed additional relative sector, an infinite-support compatibility construction, a different on-shell background, or an independently motivated changed operator; each requires its actual constraints and sources. This result does not itself establish a physical cold population or select a vacuum coefficient.
