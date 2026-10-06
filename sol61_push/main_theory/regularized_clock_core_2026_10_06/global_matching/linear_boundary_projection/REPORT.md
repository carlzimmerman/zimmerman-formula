# Exact linear boundary projection: C=0 does not cancel the growing clock mode

The source-generated endpoint map has a further necessary linear boundary condition. Interpolating central lapse to cancel C=b+(1−eta)ell leaves a nonzero coefficient of the formally growing modified-Bessel mode: AI=−8.12504e−9 in the declared real basis. Thus the finite lapse-zero shoot, the C-zero shoot and the zero-growing-mode requirement are distinct. These are linear mode projections/interpolations, not completed nonlinear shooting roots or a universal matching no-go.

## Exact real basis and derivative dictionary

For H*=1, eta=.5,kappa=.99, the directly varied linear equation is

 r²ell″+2r ell′+(mu−nu r²)ell=eta C/kappa,
 mu=eta(1−eta)/kappa=.252525252525...,
 nu=3eta²/kappa=.757575757575...,
 k=r ell′, C=b+(1−eta)ell.

The homogeneous basis depends on eta,kappa,H*, but not A. A still affects the nonlinear source-to-endpoint map; its absence from this linear propagation is not proof that a complete boundary problem cannot constrain A/H*.

With alpha=sqrt(nu)=.870388279778..., omega=sqrt(mu−1/4)=.05025189076296 and sigma=i omega, choose
 fI=r^(−1/2)Re I_sigma(alpha r),
 fK=r^(−1/2)K_sigma(alpha r).

K_sigma is real for positive argument; the imaginary part of I_sigma is −sinh(pi omega)K_sigma/pi. Hence taking ReI gives a real independent basis rather than discarding a physical mode. This follows from the conjugate-order connection formula; the numerical check confirms it. [DLMF10.27](https://dlmf.nist.gov/10.27).

For z=alpha r, the exact log-radius derivatives are
 kI=r^(−1/2)Re[−I_sigma/2+z(I_(sigma−1)+I_(sigma+1))/2],
 kK=r^(−1/2)[−K_sigma/2−z(K_(sigma−1)+K_(sigma+1))/2].

The minus sign in the K derivative is required. The underlying modified-cylinder derivative identities are documented by [DLMF10.29](https://dlmf.nist.gov/10.29). With orientation (fI,fK), the radial Wronskian is −r^−2 and the (ell,k) determinant is
 W_t=fI kK−fK kI=−1/r.
The sign follows from W(K,I)=+1/z. [DLMF10.28](https://dlmf.nist.gov/10.28).

For a declared regular even-power particular p with C=1,
 p0=1/(1−eta), p_j=nu p_(j−1)/[(2j)²+2j+mu],
 p(r)=sum p_j r^(2j), kp=sum 2j p_j r^(2j).

This series solves the forced equation. For data at r0 define e=ell−C p and q=k−C kp; then
 AI=(e kK−fK q)/W_t,
 AK=(fI q−e kI)/W_t.
The code verifies the exact basis, particular, determinant and endpoint reconstruction at50 digits.

## Formal asymptotic conditions and the particular convention

For positive r tending formally to infinity at fixed order, fI behaves as e^(alpha r)/[sqrt(2pi alpha)r] while fK behaves as sqrt(pi/(2alpha))e^(−alpha r)/r. The positive argument lies in the stated asymptotic sectors for complex fixed order. [DLMF10.40](https://dlmf.nist.gov/10.40).

For the declared flat benchmark, ell→0 and b→0 require C=0 in the exact linear system. On that branch there is no particular term, and the additional formal clock condition is AI=0, leaving only fK. Equivalently at any finite r0,
 k=(kK/fK)ell,
 provided fK(r0)≠0. The mass-type flow mode u_h∝r^−3 can remain independently at linear order; it is not identified with cold matter and does not prove nonlinear geodesic mass admissibility.

At C≠0, AI after subtracting a particular solution is **not** by itself the total growing amplitude: the regular particular can also contribute growing behavior. Replacing p by p+d fI changes the extracted AI by−Cd. Consequently this report applies the zero-growing-mode criterion only on the C=0 branch. It does not silently choose an asymptotic convention for nonzero C.

The r→infinity language here classifies solutions of the mathematical linear radial equation. The physical static patch has a Killing horizon, nonlinear errors can accumulate, and the full solution may leave its perturbative domain. No large-radius cosmological boundary theorem follows from Bessel asymptotics.

## Actual source-generated endpoint and residual targets

The inputs are the finer3e−8-tolerance results of minus6_a,zero_b,plus_b. Every source/body is recomputed by its parent solve; the endpoint is r=.003 (actual stored radius .002999999999999999). Absolute ell is the stored relative lapse plus central lnN0. LogB is used as b to first order, consistently with the parent linear diagnostic; its difference from B−1 is second order.

After subtracting the declared regular particular, the three AI coefficients are respectively−8.12503493e−9,−8.12507278e−9,−8.12509801e−9, and AK≈−1.88685e−10. Their weak variation with central lapse reflects that the dominant source clock component is not removed by shifting the approximately constant particular offset. For these C≠0 cases those AI numbers remain convention-dependent coefficients, not standalone total asymptotic growth diagnostics.

Secant interpolation between negative and zero central lapses gives C=0 at
 lnN0=−5.1559165134139446e−6,
 ell=−1.6232861913154266e−7,
 b=8.11643095657713e−8,
 k=8.220153500364312e−8.

On this C=0 interpolated branch, the particular ambiguity disappears:
 AI=−8.125040253158893e−9,
 AK=−1.886855185042421e−10.

At r=.003, a pureK clock requires k/ell=−.659742133873525, whereas these data have k/ell=−.506389664640905. The independent growing-mode boundary residual k−(kK/fK)ell is−2.48934945709436e−8. Holding k fixed would require ell=−1.245964609248398e−7 rather than−1.623286191315427e−7. C-zero therefore does not cancel the formally growing clock mode in this interpolated linear projection.

The finite lapse-zero target lnN0≈−4.99358813e−6 is already distinct from C-zero by≈1.6233e−7. A single finite lapse-zero condition is not sufficient for the selected flat clock boundary. None of these interpolated central lapses was rerun as a nonlinear shooting root in this child study. Nonlinear correction bounds and a actual outer boundary prescription are unresolved. A one-body, fixed-parameter endpoint map cannot prove a no-go for every A, density profile, cosmological slicing or MOND action.

## Independent finite linear ODE validation

For each actual endpoint, a fresh independent DOP853 integration solves only the two-dimensional linear (ell,k) equation from .003 to .3. At31 finite radii its solution agrees with exact basis plus declared particular to maximum absolute error3.90e−20 across two tolerance settings; endpoint comparisons and determinant checks pass. This tests the mode decomposition **before** invoking formal asymptotics. It is not a nonlinear continuation of the source solution to .3 and its small error does not describe source-data precision.

The test uses binary64 ODE arithmetic versus50-digit special-function projection, fixed max log-radius step .1, rtol1e−10/1e−12 and atol1e−18/1e−20. The numerical floor is already dominated by rounding at this small amplitude. The script retains errors and evaluation counts. Wrong Wronskian orientation, dropping the r² coefficient, and incorrectly asserting C0⇒AI0 are separate negative controls.

## Sources, provenance, and missing implication

`sources.json` records exact DLMF section URLs, version1.2.8/release2026-09-15, hypotheses and the hash of the locally retained web-readable snapshot. That snapshot is not original HTML and is ignored as a reference cache. Shell network retrieval and raw-TeX web retrieval were unavailable; readable primary pages supplied the verified identities. Rerunning the mathematics needs no download. Restoring the source cache for a literature re-audit requires reopening the listed primary pages; a regenerated snapshot may have a new hash and should receive new provenance.

Fresh contracts and manifests pin both actual raw source-generated outputs and this child's report/script. The new exact diagnostic identifies the missing linear growing-mode condition at C=0. Its physical completion requires a nonlinear boundary-value solution with a declared clock/cosmological boundary and health on that background. No A/H or32pi selection has been derived.
