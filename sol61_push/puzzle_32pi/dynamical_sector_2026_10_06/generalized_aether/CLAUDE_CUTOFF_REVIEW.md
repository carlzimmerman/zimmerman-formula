# Independent proof audit: exchange normalization and cutoff self-reflection

Verdict: the analytic statements are correct with the declared conditional normalization and positive-field static dictionary. No blocking correction. This review reconstructs the proof; it does not rerun Claude's scripts or provide fresh astronomical validation.

## Conditional exchange statement

With beta=1, coincident nonzero interaction vacuum and nonsingular alpha, equal vacuum curvatures require (1+fprime)/2=(1-fprime)/(2alpha). Thus fprime=(1-alpha)/(1+alpha). Exact sector exchange at the coincident point implies fprime=0, hence alpha=1. The zero-vacuum exception and alpha=-1 singular case are not covered. Positive Einstein signs do not establish full bimetric health. At alpha=1, J=int (nu-1)d(y²), C=J/2=int y(nu-1)dy provided the source-map boundary term vanishes and M(infinity)=0. For the cutoff family k>1, the boundary term y²(nu-1)²=q(y)²/[1+(y/T)^k]² vanishes at both ends. Restoring g_N=a0 y yields Lambda c^4=int(g-g_N)dg_N with no missing factor of two.

## Integral proof reconstructed

For y>0, q=1/[sqrt(1+1/y)+1] has qprime=1/[2 y² sqrt(1+1/y)(sqrt(1+1/y)+1)²]>0, 0<q<1/2, q(0+)=0 and q(infinity)=1/2. Rescaling y=Tt gives R(T,k)=C_k(T)/T=int q(Tt)/(1+t^k)dt.

Differentiating I=int 1/(1+t^k), splitting at one, and substituting t=1/u in the lower piece produces Iprime=-int_1^infinity u^(k-2)log(u)(u²-1)/(1+u^k)²du<0. Local dominated differentiation for k>1 is valid: the tail is bounded by a logarithmic power u^(-k). Therefore k>=2 implies C_k(T)<T I(k)/2<=pi T/4<T at every finite positive T. No self-reflection root exists in that whole exponent range.

The identical split with q retained produces partial_k R=-int_1^infinity u^(k-2)log(u)[u²q(Tu)-q(T/u)]/(1+u^k)²du<0. Positivity follows from q(Tu)>q(T/u)>0 and u²>1. For fixed T>0, R diverges as k decreases to1: beyond a fixed sufficiently large t, q(Tt)>1/4, and the integral tail diverges. R(T,2)<1. Continuity and strict decrease therefore give exactly one k(T) in(1,2) for each T>0.

At fixed k>1, pointwise strict increase of q implies strict increase of R with T. Dominated convergence by 1/[2(1+t^k)] gives limits0 and I(k)/2. Hence exactly one finite positive T root exists iff I(k)>2; equality gives no finite root. This also confirms the strict boundary correction to the sampled slope criterion.

## Static ellipticity bound and endpoint scope

Writing x=y/T, fprime=qprime/(1+x^k)−(k/T)q x^(k-1)/(1+x^k)² gives fprime>−k/(2T), since qprime>0, q<1/2 and x^(k-1)/(1+x^k)²<=1. The last bound follows separately from x<=1 (numerator<=1) and x>=1 (numerator<=x^(2k)). Thus D=1+2fprime>1−k/T. Every chosen self-reflection T=C>2 has k(T)<2<T, yielding D>0 for every finite y>0.

In the earlier full symmetric six-gradient dictionary, common eigenvalues are2, difference transverse eigenvalues2/(1+2e)>0, and difference radial eigenvalue2/D>0, with e=f/y>=0. Thus the bound establishes pointwise strict NR spatial ellipticity on all nonzero field magnitudes, not merely the radial inversion. At the exact zero-field MOND endpoint, e diverges and these difference eigenvalues approach zero. It is not uniform ellipticity through y=0 or a bounded regular vacuum inverse; no such stronger endpoint statement is needed for the lemma's coefficient nonselection claim. Nor is this a relativistic health theorem.

Observed repository HEAD during review: `220bff33c6f109f244e9ad06b5ea9453b51cd388`. Parent phase entry base: `81af81ba8a7207bca2bc4f13375c757feee7afcd`. Actual inspected bytes, SHA256:

- `sol61_push/puzzle_32pi/dynamical_sector_2026_10_06/CLAUDE_DELTA_AND_CUTOFF_LEMMA.md`: `67483e0b73e7fd3587541cfa6f336d93e4fb642b2616d6e4147cc00b11ea8562`
- `sonnet55_push/puzzle_32pi/p53_bimond_general_alpha.py`: `3bb48a7b88ffbfd2c9b700dc27f73453e502c928342bf3cb3fb6ff38f74b8e38`
- `sonnet55_push/puzzle_32pi/p54_what_fixes_alpha_yt.py`: `a8c54a2bc5a2aa5d3ba21e22702d44babf05f0d9ab5e7cbfe7ad3a2eb8079321`
- `sonnet55_push/puzzle_32pi/p55_turnoff_principles.py`: `dd0139649b6a059fd7d87306e996a896422bc95c041cd97494b6450cd95863dc`
- `sol61_push/puzzle_32pi/breakthrough_2026_10_05/REPORT.md`: `c98adf3a605c42f20a8d42aacc2fd78203e8e96e1fa0c1f9c83434407191df1b`
