# Focused independent review of the tilted-torus Green function

**Normalized claim.** Equation (119) of Sachs--Wipf,
`hep-th/9508142v1`, equals the zero-mode-excluded positive spectral kernel

    m^2 K = (1/V) sum_{n != 0} [1/p_n^2 - 1/(p_n^2+m^2)]

for all L,m,tau0>0 and real tau1, using its equation (13) metric and
coordinates 0<=x0,x1<L. **Verdict: refuted, with the smallest valid
counterexample below.** This review concerns that kernel formula, not the
entire paper, every possible Schwinger observable, or physical QCD.

## Source and review provenance

- I. Sachs and A. Wipf, *Generalized Thirring Models*,
  [hep-th/9508142v1](https://arxiv.org/abs/hep-th/9508142), submitted
  1995-08-25 18:47:06 UTC; Annals of Physics 249 (1996), 380--429,
  DOI 10.1006/aphy.1996.0077.
- Primary arXiv metadata confirms that exact version. PDF bytes read from
  `/private/tmp/fsp3-hep-th-9508142v1.pdf`, SHA-256
  `559a000ac43c50089d8b3a5e7d40486c1723e44380146333f6421b310b45636b`.
  Its first-page margin identifies the version. The regenerated PDF metadata
  is dated 2024; the submission version and byte identity are recorded
  separately. No assertion about a corrected journal version or erratum is
  made.
- Checked equation (13), printed page 6; equations (115)--(121), printed
  pages 42--43. Equation (119) was independently inspected in rendered PDF
  pixels (PDF page 44), not inferred only from extracted text.
- Parent claim reviewed:
  `coordinator/SCHWINGER_CLAIM.md`, SHA-256
  `6559cab0c9396ec96961cf30045f90cf2f6c1e77c77db4e27efe41f7e4b90b7b`.
- This is a separate agent's fresh derivation from the raw metric and
  spectrum after seeing the coordinator's suspected normalization issue.
  It is not a blinded review or independent discovery of the issue. No
  coordinator implementation was reused. The decisive small-m pole test
  below is an additional analytic check.

## Dependency graph and obligations

    raw metric -> inverse metric -> periodic scalar spectrum
       -> n0=0 massive slice -> its exact coth normalization
       -> comparison with source (119)

    positive spectrum -> dominated small-m limit -> source pole test

| Obligation | Result |
|---|---|
| Metric and coordinate domain agree with source (13) | Passed |
| Inverse metric, volume and Fourier normalization | Passed by direct derivation |
| Exact n0=0 sum | Passed by elementary coth partial fractions |
| Printed coefficient agrees off rectangular tori | Failed |
| Source expression has correct small-m limit | Failed |
| All physical condensate/global-mode identifications | Not addressed by this focused verdict |
| Transport to 4D QCD or de Sitter | Out of scope |

## Direct slice derivation

Set tau=tau1+i tau0. The source metric and volume are

    g = [[tau1^2+tau0^2, tau1], [tau1, 1]],
    det(g)=tau0^2, V=L^2 tau0,
    g^-1 = tau0^-2 [[1,-tau1],[-tau1,|tau|^2]].

Normalized periodic eigenfunctions are V^-1/2 exp(2pi i n.x/L), so

    p_n^2 = (2pi/L)^2[(n0-tau1 n1)^2+tau0^2 n1^2]/tau0^2.

On n0=0 this is c n1^2 with c=(2pi |tau|/(L tau0))^2. Therefore

    G_slice = (1/V) sum_{j in Z} 1/(c j^2+m^2)
            = 1/(2m L |tau|) coth[m L tau0/(2|tau|)].                 (R1)

This follows from sum_j 1/(j^2+b^2)=pi coth(pi b)/b with
b=mL tau0/(2pi|tau|). The factors V and the eigenfunction normalization
are essential. Swapping the coordinate labels changes which slice is
being summed, but cannot replace |tau| by tau0 with the same coth
argument.

The printed coefficient in equation (119) is instead 1/(2mL tau0)
with precisely that argument. It agrees with (R1) only when tau1=0.

## A decisive counterexample without a truncated lattice sum

The exact spectral definition is nonnegative and, at fixed nondegenerate
torus, obeys

    0 <= m^2 K
       = (m^2/V) sum_{n!=0} 1/[p_n^2(p_n^2+m^2)]
      <= (m^2/V) sum_{n!=0} p_n^-4 -> 0 as m->0+.

The last sum converges because the positive metric makes p_n^2
comparable to |n|^2 and the dimension is two.

For the first term of the source's equation (119), coth z=1/z+O(z)
instead gives

    -[1/(2mL tau0)] coth[mL tau0/(2|tau|)]
      = -|tau|/(m^2 L^2 tau0^2) + O(1).

Its explicit constant-mode term is +1/(m^2 V). Together they leave

    (1-|tau|/tau0)/(m^2 L^2 tau0) + O(1).                            (R2)

Every other term in (119)--(121) remains finite as m->0 at fixed
tau0>0. The eta function is nonzero, F(a)->0 with
0<=F(a)<=a^2 zeta(3)/2, and the H series is dominated by a convergent
exponential sequence since its real suppression is bounded below by
2pi tau0 n/|tau|^2. Thus no other term can cancel (R2).

Take the concrete admissible shape tau=1+i and L=1. The coefficient
in (R2) is 1-sqrt(2)<0: the printed expression diverges negatively
as m->0, while its defining spectral kernel is nonnegative and tends
to zero. This refutes the printed equation on its claimed tilted-torus
domain without any floating-point experiment or ultraviolet subtraction
ambiguity. Replacing the prefactor by the directly derived (R1) cancels
the 1/m^2 pole exactly.

## Consequence and limits

The coordinator's proposed corrected zero-slice coefficient passes this
independent audit. Its stated difference between the printed and
corrected condensate exponents,

    -pi/(mL) [1/tau0-1/|tau|] coth[mL tau0/(2|tau|)],

is the algebraic consequence of this coefficient difference in the
Schwinger-limit Gaussian exponent 2pi m^2 K. Since it has a nonzero
1/L limit at fixed tilted shape, a claimed inverse-size term inherited
from that printed coefficient cannot be accepted as exact supporting
evidence until the normalization is resolved.

This focused review does not independently certify all global factors
of the finite-torus condensate. The cheapest remaining check is the
coordinator's independently implemented convergent double spectrum
versus the resummed kernel and image/Bessel representations, followed
by a source/version comparison of the actual condensate convention.
No conclusion about physical 4D c_H follows just from this source error.

Commands performed for this review: `pdftotext -layout`, `pdftoppm`
for PDF page 44, `view_image` on that rendering, `shasum -a 256`, and
primary arXiv metadata read. No load-bearing numerical experiment is
used in the analytic counterexample.
