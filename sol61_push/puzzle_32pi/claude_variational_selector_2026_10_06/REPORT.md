# Sourced QUMOND energy does not stationarize Claude's cutoff

A concrete variational-naturalness test fails: promoting the cutoff T to a global variable and demanding stationary renormalized source potential energy gives no finite interior T for Claude's positive turnoff family. The source energy samples a different kernel moment from the conditional vacuum moment. This follows from the actual NR action, not an invented smoothness penalty. The proposed variation of a coupling is itself only a diagnostic unless a new dynamical sector justifies it.

## Scientific inputs and action

Read current sonnet55 p35, p54 and p57, without rerunning galaxy/orbit/network fetches. p54 explicitly leaves the cutoff number free; its 32π root is a target fit. p57 uses QUMOND multipole forces and a reduced orbital comparison, not a constitutive Euler–Lagrange equation. Its withdrawn algebraic predecessor is not used. We do not import any claimed data exclusion or rederive the conditional BIMOND vacuum map.

The authenticated primary NR action is Milgrom, *Quasi-linear formulation of MOND*, arXiv:0911.5464v2, equations (3)–(6):

L=−[2∇Φ·∇ΦN−a0² Q(z)]/(8πG)−ρΦ,   z=|∇ΦN|²/a0²,
ΔΦN=4πGρ,   ΔΦ=∇·[ν(y)∇ΦN],   ν(y)=Q′(y²).

Matter accelerates as −∇Φ. QUMOND's two-field form is variational but saddle-like; this argument does not assume a positive full Hessian. Ordinary action variation is over fields and matter, with Q fixed. It does not vary Q or T. The new premise tested is that a putative UV modulus T could be fixed by stationarity of this source energy with no additional T potential, gradient action or boundary functional.

## Envelope variation and source histogram

Use Q(0)=0 throughout and χ(y)=ν(y)−1. Then q(y)=Q(y²)−y²=2∫0^y tχ(t)dt, and, if finite, q(∞)=2C with C=∫0∞yχ(y)dy. A constant Q offset is not changed independently. At fixed source and fixed boundary potential gauge, variation of the stationary static energy U=−L gives

δU=−a0²/(8πG) ∫δq(y(x))d³x.

This is the envelope identity: implicit field variations vanish by the field equations with appropriate fixed-boundary conditions. Work first in a regulated finite domain or smooth source; take finite kernel-energy differences with common IR gauge and kernel-independent subtractions. The absolute isolated MOND energy is IR logarithmically divergent, and a point mass has the usual UV Newtonian self-energy divergence. Neither is declared finite. Changes with fixed deep amplitude and sufficient decay can have a finite envelope variation; their far-field potential difference is normalized to zero at infinity. No boundary contribution is silently varied.

Layer-cake/Fubini gives the raw kernel functional

δU=−a0²/(4πG)∫0∞ y V_>(y) δχ(y)dy,
V_>(y)=volume{x: |∇ΦN(x)|/a0>y}.

Absolute convergence of the displayed variation justifies exchange; compact kernel perturbations already suffice. Thus the variational weight is an actual source acceleration histogram, not a universal function of acceleration fixed by covariance. For a point mass, rM=√(GM/a0), y=(rM/r)² and V_>=4πrM³/(3y^(3/2)), giving the exact result

δU=−a0²rM³/(3G)∫0∞ y^−1/2 δχ(y)dy.

Independently, 4πr²dr=−2πrM³ y^−5/2dy, and radial integration by parts/Fubini gives ∫y^−5/2δq dy=(4/3)∫y^−1/2δχdy, reproducing both sign and normalization. Dimensions are energy: a0²rM³/G. The moment weight y^−1/2 differs from the vacuum weight y. For a uniform sphere radius R, V_>(y)=4π[rM³y^−3/2−(yR³/rM²)³]/3 for 0<y<rM²/R² and zero above: even the histogram depends on body radius. Inside gN=GMr/R³; outside gN=GM/r². The general no-stationarity sign below does not require point-source idealization.

## Claude cutoff: no interior Euler–Lagrange root

Use precisely χ_T(y)=[√(1+1/y)−1]/[1+(y/T)²], T>0, rather than optimizing a target. Its derivative is

∂Tχ_T=2T y²[√(1+1/y)−1]/(T²+y²)²>0.

Near y=0 this is O(y^(3/2)); at infinity O(y^−3). Hence both C′=∫y∂Tχ dy and J′=∫y^−1/2∂Tχdy converge and are strictly positive. Dominated differentiation is valid uniformly on compact positive T intervals using these endpoint bounds. Point-source U′=−a0²rM³J′/(3G)<0, and the histogram formula gives U′<0 for any nontrivial finite source for which the variation converges. Therefore δU/δT=0 has no finite interior solution. Minimizing energy pushes toward larger T; minimizing C alone pushes toward T→0. Neither gives 32π or another positive selected number. The open T>0 family does not attain either boundary; the unregulated isolated energy cannot be used as an absolute minimum.

If a bare term V(T) is added, stationarity becomes V′(T)=a0²rM³J′(T)/(3G) for the point-source convention. The right side scales as M^(3/2), so the same fixed V cannot give a source-independent stationary T for two different point-source masses at the same T. This is a statement about this isolated-source modulus diagnostic, not a cosmological population or local-modulus model. New dynamics, ensemble, boundaries or source dependence would have to be specified.

A fully unrestricted kernel variation makes the missing premise even clearer: δU/δχ=−a0² yV_>/(4πG) is nonzero where the source histogram is nonzero. There is no constitutive Euler–Lagrange equation selecting Q in the original action. Admissibility inequalities and fixed endpoints restrict allowed variations but do not supply the absent modulus dynamics; all finite T sign conclusions above concern a declared admissible interior cutoff branch. This does not prove a no-go for all constrained kernel optimization problems.

## First missing covariant implication

One must write and vary a covariant action for a field/modulus controlling Q, including its vacuum stress, derivative terms, boundary conditions and matter source. Only then can its stationary equation be compared with Λ and a0. QUMOND is NR and the p54 BIMOND moment identification remains conditional; sourced NR energy does not by itself justify a vacuum coefficient or an exchange-symmetric relativistic completion. The result is a sharper obstruction for one natural diagnostic, not an impossibility theorem for all physical selectors.

checks.py verifies exact histogram/Jacobian/derivative and mass-normalization identities, an independent radial moment benchmark, and positive numerical derivatives at T=10,100,1000 with 50-digit quadrature. These are independent examples, not 32π fits. Three false assertions are controls. SOURCE_REVIEW.md records exact primary version and scope. Standard bounded manifests pin actual input hashes, including the Claude files read. No global ledger/peer edits or git changes are made.
