# Finite two-loop scalar/fermion graph contract

Frozen before execution, 1 November 2026. Starting shared revision is
7b1880de2caded85da4b8c34d84b5dc6c005650e; actual pinned inputs govern.
TP01 and TP02 remain immutable. This route owns only this directory.

Implement actual Martin hep-ph/0111209v2 finite SSS,SS,FFS,barFFS vacuum
graphs, including all full-SU5 scalar F/D vertices and chiral/gaugino
Yukawa vertices. Real fields satisfy z=z0+(q+ip)/sqrt(2). Scalar and
vector orthogonal eigenvectors and the fermion Takagi columns are shared
with the coordinator's gauge graph route. No quartic98^4 tensor is stored;
only the required lambda_iijj contraction is formed. Degenerate masses
are grouped before master-integral calls, with recorded grouping tolerance
and discarded-roundoff weights. Loop factors are excluded until final
V2/(16pi²)^2; graph symmetry factors follow source4.2–4.5.

Primary source target: Martin section2 defines mass/coupling conventions,
section4 supplies graph prefactors/kernels, section5 confirms these four
classes are unchanged in DR, and section6 supplies the gauged DRprime
completion handled separately. A partial scalar/fermion sum is not the
full gauged answer. The master-integral worker independently implements
sunset/massless branches; no substitute RG logarithm is used.

First controls: complete dense spectrum/Takagi residuals; cubic/quartic
vertices against independent directional derivatives of the original
polynomial potential; Yukawa derivatives against mass-matrix variation;
tensor permutation symmetry and basis-rotation invariance of grouped
weights. Test a one-field Wess-Zumino supersymmetric origin analytically
and full SU5 unbroken SUSY f=0,g=0 at nonzero X. Gauged SUSY cancellation
requires the coordinator's vector graphs and is not demanded of these
four classes alone. Preserve adverse results and failed implementations.

Physical target: weak e=.03, h=lambda=e,g=sqrt(29/200)e,f=1, reference
Xmin=7.367143721278508*sqrt(e/31)/e. Fixed Q²=e/31+(eXmin)^2. Initially
evaluate X/Xmin={1,1.2} and then a fixed compact .9..1.4 grid if controls
pass and complete graph sum is available. Scaling controls at e=.01 must
give V2 proportional to e^4 at equal dimensionless field and Q²/e.
Do not infer pressure from an incomplete graph sum or uncontrolled
interpolation. Heavy normal relaxation is counted separately once.

Resource policy: one numerical thread, below1GB measured RSS, at most180
wall/170CPU seconds per bounded run, no downloads/installs/production
jobs/queue changes/Git mutations. Scripts/contracts precede execution,
fresh v2 manifests preserve actual hashes and outcomes. Direct kinetic
matching is separately owned; no full physical completion is presumed.
