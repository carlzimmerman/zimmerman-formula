# Independent proof review: homogeneous aether cone lemma

Pinned read-only inputs:

- HOMOGENEOUS_AETHER_CONE_LEMMA.md SHA256 6f092ea7f97fc502e30552970f7e11293852ef43f064cf36475c78d09d5f5f15.
- aether_cone_checks.py SHA256 7475d6e729f36616c131f60fbd746acfb3d14750030deaaf1d821bdd8ad3ecc3.
- generalized_aether/REPORT.md SHA256 7dc1adb7bbe91b3abcc918221bf702f9a375c14e179ae32fb76341b25252a06a.

**Verdict:** the integral implication and coupled scalar ghost interval are correct for the declared hypersurface-orthogonal, c13=0, c2<0, F′>0, F(0)=0, no-vacuum-source family, in the nondegenerate geodesic homogeneous principal limit. I reconstructed the action coefficients and constraint elimination independently. No peer execution inputs were modified or scripts run. This review does not certify accelerated galaxy transitions or all cosmological histories.

With ∇μuν decomposed into extrinsic curvature and acceleration, c1∇u·∇u+c3 crossed contraction gives c13 KijKij−c1 a². Thus c13=0 leaves c2θ²−c1a². Expanding M²F at a geodesic isotropic background yields c2(F′+2KF″)(δθ)²−c1F′(∂ν)². The F″ term follows directly from (M²/2)F″(2c2θ δθ/M²)²; it cannot be dropped on a nonlinear branch. Adding the Einstein ADM combination KijKij−θ² gives λ=1−c2(F′+2KF″), η=−c1F′.

To reconstruct the scalar time polynomial, let q=ζdot and t=ΔB. The linear extrinsic tensor is qδij−∂i∂jB, so for a nonzero Fourier mode Kij²=nq²−2qt+t² and θ²=(nq−t)². Their difference with coefficient λ is n(1−nλ)q²+2(nλ−1)qt+(1−λ)t². Its shift equation gives t=(nλ−1)q/(λ−1). Completing the square or substitution yields Aζ=(n−1)(nλ−1)/(λ−1), with the positive common K_E/2 normalization. Consequently 1/n<λ<1 is a negative scalar kinetic coefficient; this conclusion does not require a favorable gradient coefficient.

The spatial-curvature expansion can also be reconstructed directly: √h R for h=e^{2ζ}δ integrates to +(n−1)(n−2)|∇ζ|², and the lapse multiplier of its linear curvature gives +2(n−1)∇ν·∇ζ. Together with η|∇ν|² its lapse equation on nonzero modes gives ν=−(n−1)ζ/η. Substitution yields −Bζ|∇ζ|² with Bζ=(n−1)[(n−1)/η−(n−2)]. Hence Bζ/Aζ is the stated c_s². For n=3 the ordinary positive gradient coefficient needs η<2; for n=2 Bζ=1/η is positive for every η>0. These conditions are distinct from the unavoidable kinetic interval.

Homogeneous lapse variation of a^n N M²F(K), with K∝H²/N², gives M²(F−2KF′). Combining with the Einstein lapse variation produces 1−αF′+αF/(2K)=0. At z=−K, F(−z)=−I(z), F′(−z)=h(z), α=nc2<0, so the positive root requires I−2zh=−2z/α>0. Independently, Q=(h+2zh′)/h obeys (√z h)′=hQ/(2√z). If Q≥0 everywhere, √s h(s)≤√z h(z) and integration gives I≤2zh, contradicting the root. With the finite positive C² endpoint Q→1, there must therefore be some negative-Q point. Continuity of λ=1−c2hQ connects λ>1 near zero to a λ<1 point and forces an open interval with 1/n<λ<1. A first zero may be a tangency; the proof needs only a later genuine negative-Q point, and does not require the first zero itself to cross.

The high-frequency reduction is valid at a fixed nondegenerate state for k/a large compared with H and coefficient-variation scales. Terms containing Hν and Hζdot are lower principal order there, but the limit is nonuniform at λ=1 or λ=1/n. The proof avoids using an eliminated formula exactly at those points: continuity supplies interior states with strictly negative finite kinetic coefficient. Accelerated or anisotropic backgrounds have additional F″ mixing and cannot use this two-coefficient symbol without rederivation.

Finally, the existence of an unhealthy homogeneous state somewhere between zero and the root is not a proof that a particular solution traverses it. The report explicitly preserves this distinction. Its result obstructs a demand for healthy geodesic isotropic states throughout that entire interval; a cosmology living wholly on a separate endpoint, or a nonhomogeneous matching path, remains a different obligation. No mathematical correction to the pinned lemma is required.

## Correction identified after the initial audit

The initial acceptance above missed a real general-n normalization error in the homogeneous root equation. It is retained as historical audit provenance, not current approval of that equation. The ADM kinetic/gradient reduction and the integral sign argument are unaffected.

Independently retaining the homogeneous lapse, with coordinate-time H=adot/a, gives the minisuperspace Lagrangian (apart from a^n and the common K_E/2)

L_N=−n(n−1)H²/N + N M² F[n²c2 H²/(M²N²)].

Its lapse derivative at N=1 is n(n−1)H²+M²(F−2KF′). Thus the exact general-n vacuum equation is

F−2KF′=−(n−1)K/α,
1−[2α/(n−1)]F′+[α/(n−1)]F/K=0,
α=nc2.

The previous −2K/α expression is correct only for n=3. After z=−K and F(−z)=−I, the corrected root condition is I−2zh=−(n−1)z/α>0. Since n≥2 and α<0, the same contradiction with Q≥0 follows; hence the same continuity path into 1/n<λ<1 remains. A genuine negative-Q point, rather than the first zero, supplies the argument even when earlier zeros are tangencies. Final repair acceptance will be pinned below after the root publishes its completed revision.

## Final repaired revision accepted

I reread the repaired lemma at SHA256 7b294e2e91e39a1e9349f8b8627e8010eccd497a3d6a24a502f2ff5f751a7e9d and repaired aether_cone_checks.py at SHA256 2ab60aea4bf1129596a0f7da15f739def6dbd624f69f3f93cbfc72545f2a54b6. The lemma now states the correct (n−1) factor and uses a continuous path to any negative-Q point, avoiding the first-zero tangency issue. The new exact minisuperspace lapse-variation check computes the derivative before comparing with the root identity, rather than assuming the erroneous normalization. I accept the repaired restricted theorem. The initial normalization acceptance above is explicitly superseded; the corrected full-interval homogeneous ghost obstruction survives.
