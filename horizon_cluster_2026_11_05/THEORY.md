# HC-002: structural results and scoped self-audit

These results use specified models. They do not exclude every possible new horizon coupling. Review provenance: same-agent derivation and adversarial self-review; no independent referee or Lean certificate in this campaign.

## 1. A real astrophysical horizon is not the constructed puzzle area

For a Schwarzschild hole, rs=2GM/c², A=4πrs², and κ=c²/(2rs). Setting κ=a0 constructs A=πc⁴/a0². Substituting Λ=32πa0²/c⁴ then gives AΛ=32π². This is an implication from the proposed acceleration relation, not an independent derivation of that relation.

For Λ>0 fixed, the target radius is sqrt(8π/Λ). The de Sitter radius is sqrt(3/Λ), so their ratio is sqrt(8π/3). In the static, spherical Schwarzschild–de Sitter solution, the Nariai mass is c²/(3G sqrt(Λ)). The mass assigned to the formal Schwarzschild sphere exceeds it by 3sqrt(8π)/2. Thus the formal Schwarzschild construction cannot simply be identified with an ordinary black hole in that same Schwarzschild–de Sitter universe. This is not a general no-horizon theorem or a statement about all surface-gravity normalizations.

For fixed nonnegative masses M_i and fixed Λ, Schwarzschild area sums obey

    Σ A_i Λ = (16πG²Λ/c⁴) Σ M_i²
             ≤ (16πG²Λ/c⁴) (Σ M_i)².

The inequality follows from the nonnegative pairwise cross terms. Equal masses give 1/N of the one-hole area at fixed total mass. Kerr spin further multiplies each area by (1+sqrt(1-χ²))/2 in [1/2,1]. These are individual-horizon area sums, not a formula for a common horizon or a cosmological entropy bound. A putative common horizon requires its own spacetime solution.

Even assigning an illustrative entire 10^15 solar-mass cluster to one Schwarzschild hole gives AΛ=1.19e-14, versus the target 315.83. Splitting the mass cannot close this gap by summing ordinary horizon areas.

## 2. Distinct radii and local versus cosmological curvature

Keep rs, GM/σ² (an approximate influence radius), sqrt(GM/a0) (MOND acceleration radius), and (3GM/(Λc²))^(1/3) (static spherical turnaround radius) distinct. Their meanings and regimes differ. Defining Racc=c²/a0 gives rM²=rs Racc/2 identically. Such geometric-mean identities do not introduce additional mass or select a0.

In Schwarzschild–de Sitter, the Ricci scalar is 4Λ, the Weyl invariant is 48(GM/c²)²/r^6, and the Kretschmann scalar is their contribution 48(GM/c²)²/r^6+8Λ²/3. Comparing curvature scales selects a mass-dependent radius; it does not select a universal galaxy acceleration coefficient. These standard metric identities are stated here as model background; they were not independently tensor-recomputed in this campaign. H07 remains open for that computation.

## 3. Enclosing-sphere QUMOND bound

Claim HC-Q: consider a finite positive Newtonian mass distribution entirely and strictly inside a sphere of radius R, no external Newtonian field or exterior matter, and the QUMOND source law div grad Φ=div[ν(|grad ΦN|/a0) grad ΦN]. If ν is nonincreasing and h(q)=qν(q/a0) is concave for q>0, then the total enclosed effective mass is at most that of the spherical reference with the same M and R. This applies to the two interpolating laws used here, not arbitrary modified gravity.

Proof. Use b=grad ΦN, an outward-pointing field for a central mass, not the physical inward acceleration. On the enclosing sphere b_n=b·n>0: each positive source inside contributes a strictly positive normal component. Also |b|≥b_n. Therefore

    ν(|b|/a0)b_n ≤ ν(b_n/a0)b_n = h(b_n).

The QUMOND Poisson equation and the divergence theorem give

    M_eff = (4πG)^(-1) ∮ ν(|b|/a0)b_n dA.

Jensen's inequality on the sphere yields mean h(b_n)≤h(mean b_n). Newtonian Gauss flux gives mean b_n=GM/R². Consequently

    M_eff ≤ (R²/G) h(GM/R²) = M ν(GM/(R²a0)).

Since the true enclosed M is the same, the same ordering holds after subtracting M to define phantom mass. The physical QUMOND acceleration need not equal -νb pointwise; only its divergence/flux is used.

For quadrature ν(y)=sqrt(1+1/y), h(q)=sqrt(q²+a0q), with h''=-a0²/[4(q²+a0q)^(3/2)]<0. For simple ν(y)=1/2+sqrt(1/4+1/y), h(q)=[q+sqrt(q²+4a0q)]/2, with h''=-2a0²/(q²+4a0q)^(3/2)<0. Both ν are decreasing. The numerical script checks the exact derivatives with SymPy and evaluates the flux for two equal point clumps.

Correction to older wording: this proves an inequality, not exact invariance at every finite enclosing radius. For clumps at ±0.9R and monopole boundary GM/(R²a0)=0.01, the computed effective mass is about 0.732 of the smooth value. At large R compared with the source extent the anisotropy vanishes and the ratio approaches one. This does not contradict the older nearly-unity results in their more compact configurations.

The theorem does not apply directly when a boundary cuts through sources, exterior cluster material or an external field is present, or the quantity is projected lensing mass. It does not bound a new field with different source equations. It is not a pointwise force comparison or an AQUAL theorem.

## 4. Obligation audit

| Obligation | Outcome |
|---|---|
| Positive normal Newtonian field | Passed for positive sources strictly inside sphere; fails as a general exterior-source statement |
| ν monotonicity and h concavity | Passed analytically for the two named kernels; exact second derivatives checked |
| Gauss and QUMOND flux sign | Passed with b=grad ΦN convention |
| Pointwise vector superposition of MOND gravity | Not used; would be invalid in general |
| Finite-radius exact invariance in old prose | Refuted by two-clump configuration; safe replacement is inequality above |
| All cluster geometries and all theories | Out of scope |
| Numerical implementation | 45 configurations; 64/128/256-point quadrature; 15 independent adaptive vector integrals |
| 32π coefficient selection | Incomplete: no independent physical equation fixing it |

Verdict for HC-Q: proved as written under its explicit mathematical model assumptions, self-reviewed. Verdict for the unrestricted old finite-radius invariance claim: refuted. No source file outside this campaign was rewritten.

## 5. What would change the conclusion

A new horizon mechanism must specify an action or field equation, a source charge, the exterior force and lensing response, and an independently fixed normalization. One cannot introduce a free amplification factor, fit it to the cluster deficit, and call that a derivation. It must also explain galaxy data without inserting black-hole masses inferred from the very relation being tested. The October coefficient-shift counterfamily remains a constraint: matching a local force law does not by itself fix an additive vacuum term.
