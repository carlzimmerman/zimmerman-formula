# Generator audit

The strongest new nominal success, Qwen 7376a647fa2c4a9dba52909aeb4d4068,
is refuted. Its code omits streaming, sets L(r^2)=0 and L(I)=kI incorrectly,
uses incorrect angular moments, accepts a constant residual instead of zero,
ignores the outgoing boundary, and inverts its negative predicate. Its own
local referee caught the boundary and control failures but did not supply the
correct operator. Adding a constant cannot repair a residual because L1=0.

With s=r^2,z=x dot u, streaming is 2z partial_s+partial_z. The audited Thomson
angular leaf gives Kz=0 and Kz^2=3s/10+z^2/10. Therefore the nominal solution
P=s-2z/k has residual L(P)+2m=-ks+k+2z-2/k, not merely 2I(1).
At physical state k=1,s=1/4,z=0 this is -5/4. Its outgoing boundary residual
at k=z=s=1 is -2. The exact audit also checks constants, s,z,z^2, the mean
equation/boundary, and the vacuum second moment w=z^2. Ten checks pass and
the current computation manifest validates. This is a refutation and operator
calibration, not a transport simulation, new law, or novelty assertion.

Later code 31f9f3fb643f4bada02f4db68791edfb integrates only mu in [0,1]
with an extra factor mu, identifies x dot u' with r mu for general orientation,
and omits the streaming derivative of z^2. Its residual is also unreliable.
Boundary elimination D=-C assumes I(1)=1 without justification; the correct
condition in that old basis is D=-C I(1). Failed equations from these codes
do not prove even their stated restricted ansatz obstruction.

Next Qwen calculation: coefficient-match a polynomial particular solution in
s^2,sz,z^2, explicitly retain its boundary mismatch h(z), then derive bounds
using extrema of h on the physical outgoing interval. The version 3 task is
self-contained and pins the correct operator. Same obligation ID; no new
discovery label. A useful bound must still survive independent transport and
primary-source novelty review before promotion.
