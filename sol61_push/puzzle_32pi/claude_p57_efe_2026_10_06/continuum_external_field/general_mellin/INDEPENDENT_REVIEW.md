# Independent proof audit: continuum Mellin injectivity

**Primary verdict: proved as written**, for the exact parent functional and the class `integral_0^infinity y|f(y)|dy<infinity`. This accepts mathematical injectivity of the ideal entire continuum, not finite observational inversion, a cosmological dictionary, or coefficient selection. The review reconstructs the critical reductions independently; agreement with finite numerical checks is not its proof.

Observed HEAD: `30b858d2d7d4b1eff9916a06fcf2e3e8d70842c2`. Inspected source hashes:

- `sol61_push/puzzle_32pi/claude_p57_efe_2026_10_06/continuum_external_field/general_mellin/REPORT.md`: `3626298455d974f8efb7591adff699cfeddac1a02e7d99ab303b5788b911e0b2`.
- `sol61_push/puzzle_32pi/claude_p57_efe_2026_10_06/REPORT.md`: `cbc5a75fe84b619ff84f5031c583f9c8d328430b509393ea019be01b8b77b541`.
- `sol61_push/puzzle_32pi/claude_p57_efe_2026_10_06/checks.py`: `3d3e4422d5f066426133a5a2db52bdbb21020c4ebcdeeee68dc10e2e38f25470`.
- `sol61_push/puzzle_32pi/claude_p57_efe_2026_10_06/continuum_external_field/INDEPENDENT_MELLIN.md`: `aa82c1759d75cb70aa89928707742cfc226badfb90229670a309bd97c2a02b58`.

## Dependencies and obligations

The raw parent weight is the declared functional input. The two-branch geometric calculation in `../INDEPENDENT_MELLIN.md` independently proves the nonzero value at the only exceptional point on the Fourier line. Gamma recurrence, reflection, absence of zeros and Euler beta integrals are external standard identities, checked directly against primary NIST DLMF on 2026-10-06: [5.2](https://dlmf.nist.gov/5.2), [5.5](https://dlmf.nist.gov/5.5), [5.12](https://dlmf.nist.gov/5.12). Endpoint subtraction, the convolution dictionary and the zero-location argument are internal derivations. Fourier uniqueness is justified below without leaving it as an uninspected theorem.

The full branch weight, endpoint strip, beta recurrence, common-cutoff cancellation, Fourier-line nonvanishing, convolution powers and L1 uniqueness all pass. Numerical reconstruction stability and finite-domain inference are out of scope. No missing mathematical implication was found under the stated hypotheses.

## Endpoint finite parts: no invented common strip

For each coefficient `a_n=(12,6,1,2)`, let `r=s−3+n`. The plus integral has integrand `q^(r−1)/sqrt(1+q)`. Its ordinary convergence strip is `0<Re r<1/2`. The signed minus integral consists of `(0,1)` minus `(1,infinity)` with denominator `sqrt(|1−q|)`; its continued expression is

`B(r,1/2)−B(1/2−r,1/2)`.

Neither branch's four individual coefficient terms has a common ordinary strip. That fact does not invalidate the finite sum if finite parts are defined using one common small cutoff and one common large cutoff. A concrete justification is to subtract finitely many small-q powers on `(0,1/2)` and inverse-q powers on `(2,infinity)`, integrate the remainders, and analytically integrate each subtracted monomial. The resulting expression is meromorphic in s. For a generic s, it equals the constant term of the common-cutoff integral, and agrees with the beta expression wherever that individual beta integral ordinarily converges; analytic continuation then identifies it elsewhere.

Linearity at common cutoffs is essential. In the complete coefficient/branch sum, the expansions are exactly `F=O(q²)` and `F=O(q^(−7/2))`. All divergent endpoint monomials cancel for `−2<Re s<7/2`; the remaining cutoff integral tends to its ordinary value. At isolated logarithmic or pole locations, use analyticity of the *combined* convergent integral, rather than assigning separate infinite terms values. The q=1 square-root singularity is integrable term by term and introduces no finite-part ambiguity. Thus the report's finite-part route supplies the needed equality, without an arbitrary subtraction constant or a fictitious common convergence strip.

## Independent beta algebra

Reflection gives

`B(r,1/2)/Iplus(r)=cos(pi r)` and
`B(1/2−r,1/2)/Iplus(r)=sin(pi r)`,

where `Iplus=Gamma(r)Gamma(1/2−r)/sqrt(pi)`. Because `r=s−3+n`, the signed coefficient difference is `Iplus(r)[1+cos(pi s)−sin(pi s)]`, with the same factor for every n. Recurrence gives

`Iplus(r+n)/Iplus(r)=(-1)^n (r)_n/(r+1/2)_n`.

Direct rational combination of `(12,6,1,2)` yields

`sum a_n (-1)^n (s−3)_n/(s−5/2)_n =20s(s−2)/[(2s−5)(2s−1)]`.

I recomputed this exact rational identity independently with SymPy; it reduces to zero after subtracting the report's expression. This finite check corroborates the displayed recurrence calculation. The Mellin expression and its normalization consequently match the raw full weight.

## Nonzero Fourier line, including the removable point

On `s=1/2−i omega`, `omega!=0`, both gamma factors are finite and nonzero; all rational numerator and denominator factors are also nonzero. The remaining factor is

`2cos(pi s/2)[cos(pi s/2)−sin(pi s/2)]`.

The first factor's complex zeros are real odd integers. The second has only real zeros `s=1/2+2j`: from `tan(pi s/2)=1`, or directly the exponential equation, its imaginary part must vanish. Therefore no zero occurs on the line away from omega=0. At omega=0 the trigonometric zero cancels the rational pole: the independent geometric proof gives the finite nonzero value `−4pi/35`. Reading the isolated trigonometric zero as a blind mode would be an error.

## Weighted convolution and uniqueness

For `x=ln e`, `z=ln y`, define `g(z)=e^(2z)f(e^z)` and `k(u)=e^(u/2)F(e^u)`. The finite-moment hypothesis gives `norm(g)_1=integral y|f|dy`. The endpoint bounds and shell singularity give `norm(k)_1=integral q^(−1/2)|F(q)|dq<infinity`. Direct change of variables yields

`e^(x/2) R(e^x)=integral g(z)k(x−z)dz`,

so the exponents in the report are correct. This identity is an L1/Fubini identity, hence initially almost everywhere; smooth physical representatives may upgrade the interpretation where appropriate. The Fourier multiplier is exactly `K(1/2−i omega)` for the convention `hat k=integral e^(−i omega u)k(u)du`.

If the response difference vanishes, nonvanishing of this multiplier gives `hat g=0`. For every positive Gaussian width, `g` convolved with that Gaussian has integrable Fourier transform (bounded `hat g` times a Gaussian), so Fourier inversion makes the convolution zero. Gaussian approximate identities converge to g in L1; consequently `g=0` almost everywhere and `f=0` almost everywhere. This proves the stated injectivity. It supplies no lower bound for the inverse multiplier and no stable inversion from noise.

## Strongest safe statement

An ideal exact positive-external-field quadrupole continuum determines the entire finite-absolute-moment response kernel almost everywhere, including its moment C. This extends the independent geometric moment identity. It does not contradict any finite-observable null family, nor infer a preferred numerical value of C. The physical source identification and QUMOND-to-relativistic-vacuum mapping remain separate inputs.
