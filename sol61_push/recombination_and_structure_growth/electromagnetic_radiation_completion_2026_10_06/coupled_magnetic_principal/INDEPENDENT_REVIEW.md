# Independent coupled magnetic-principal audit

**Primary verdict: proved conditional on the declared covariant action, finite on-trajectory pure-magnetic triad and admitted short-wavelength regime.** The actual conserved-dust, Maxwell-Gauss, lapse and scalar-momentum equations preserve a nonzero transverse electromagnetic branch

`omega²/p² -> c_mag²=1−2Z(Bcal_rho)²B0²`.

When c_mag²<0 it is a physical classical high-frequency gradient instability in this coupled model. This verdict was reconstructed from the raw source/constraint action, not inherited from this reviewer's fixed-clock screen. It includes the nominal and exact auxiliary-subblock degeneracies. No all-radiation, electric-sector, thermal-photon, cutoff or 32pi conclusion follows.

Observed HEAD: `85251b027ede0ec3a57bec52da9548b290fe4829`. Final author-report and script hashes below match the explicitly supplied frozen versions. This reviewer did not execute or edit author inputs; all four runner manifests were independently validated against current hashes. The bounded numerical records corroborate the algebra rather than prove the universal mode.

## Source/normalization reconstruction

With signature −+++ and the parent's orthonormal electric convention, the ADM normal field is `F0i−NjFji`. For the pure magnetic triad `B_i^a=B0 delta_i^a` and scalar sine photon `Axy=C/sqrt(2)`, `Ayx=−C/sqrt(2)`, a scalar sine shift Nz=S changes the two nonzero normal electric components oppositely. Their summed energy is exactly

`(Cdot−sqrt(2)B0 S)²/2`.

The term B0²S² therefore belongs to Maxwell's same-action source reaction. It cannot be replaced by a fluid shift term. With `gamma_ij=a²exp(2zeta)delta_ij`, the magnetic density variation is independently

`delta rho_EM=sqrt(2)B0 pC−4rho_EM zeta`

`=sqrt(2)B0 pC−6B0²zeta`, `rho_EM=3B0²/2`.

It contains neither lapse nor shift at first order: the background normal electric field is zero, while its shift-induced perturbation enters energy only at second order. Hence the square's actual quadratic is `Z[q²nu+b delta rho_EM]²/2`, b=Bcal_rho. Directly expanding the bare magnetic action `−Nexp(−zeta)sum B_coord²/2` gives the stated `−p²C²/2+sqrt(2)B0pC(zeta−nu)` and finite metric tadpoles. No scalar-fluid density conversion is used.

The finite alpha,beta background tadpoles may be retained as arbitrary bounded coefficients for the principal proof: the analysis below shows explicitly that they scale below the leading action. Their precise values are unnecessary for this asymptotic claim, though they would be required for finite-p transfer or global background matching.

## Maxwell Gauss and scalar-sector closure

At nonzero k choose A_z^a=0 but retain each scalar potential. The scalar shift cross background B has no z component. Since the positive square has no electric first variation about E0=0, Gauss still forces each longitudinal normal electric amplitude to zero. Thus all three Maxwell auxiliaries are properly constrained and the transverse C mode is not a promoted gauge field.

The C perturbation has `delta B_x^x=delta B_y^y=pC/sqrt(2)`, `delta B_z^z=0`. Its bare linear stress has equal xx/yy components, no xy tensor source, no zx/zy vector source, and its Poynting/metric momentum is only along z. This proves closure against vector and tensor helicities in the isotropic background.

A small qualification to a symmetry-only explanation is important: another electromagnetic m=0 combination `C_E=(Axx+Ayy)/sqrt(2)` exists, so rotation symmetry alone cannot exclude all scalar mixing. I checked it directly. Its induced delta B is antisymmetric in the internal/spatial xy indices, has zero trace, and has zero symmetric bare stress contraction with `B_i^a=B0delta_i^a`. Its electric variation is parallel to each corresponding background B, giving zero Poynting vector. It therefore sources neither delta rho nor the scalar shift or metric at linear order; free Maxwell quadratic terms are orthogonal to C. The new square couples only through delta rho. Thus this additional m=0 photon decouples and does not create an omitted auxiliary equation or cancel the C branch. The remaining helicity sectors are also unsourced. This explicit check completes the stated closure without relying merely on a mode count.

## Ordinary dust and the actual constraints

The unmodified Schutz coordinate-density pair contributes

`pi(v_d_dot−nu)−rho_d p²v_d²/2+rho_d p v_d S+3rho_d zeta nu`.

Its density equation gives v_d_dot=nu. The complete momentum constraint from the retained raw action is

`2p(M zetadot−Theta nu)−sqrt(2)B0 Cdot+2B0²S+rho_d p v_d=0`.

The lapse equation includes the canonical dust density source and the new square; it is varied, not imposed by a radiation-fluid dictionary. Scalar clock and spatial gauges plus Maxwell gauges have already been specified. No remaining Gauss or dust conservation equation can be added as an independent restriction after the full Euler system used below.

## Independent fast-time action and leading matrix

Let `tau=p t` and rescale the fields

`zeta_bar=p zeta`, `S_bar=S/p`, `v_bar=p v_d`, `pi_bar=pi/p²`.

Divide the action by p². Every omitted term in the written raw quadratic is explicitly lower order: clock/gravity metric tadpoles, Sigma and −3M zetadot² are O(p^(−2)); the lapse–metric spatial term, density-square cross terms, Maxwell C(zeta−nu), and dust shift source are at most O(p^(−1)); the finite dust v_d² term is O(p^(−2)). The retained leading action is

`L0=kappa Mnu²+2S_bar(M zeta_bar'−Theta nu)`

`   +(C'−sqrt(2)B0 S_bar)²/2−c_mag² C²/2`

`   +pi_bar(v_bar'−nu)`.

Primes are fast-time derivatives, not physical-time derivatives. Ordinary dust remains genuinely varied in this leading action, unlike an externally frozen matter approximation.

For x=omega/p≠0 the zeta_bar equation gives S_bar'=0, hence S_bar=0 in the nonzero-frequency sector. The v_bar equation gives pi_bar'=0, hence pi_bar=0. The lapse equation then gives nu=0 since kappa M>0. The pi_bar equation gives v_bar'=nu, hence v_bar=0. The shift equation fixes

`zeta_bar=B0 C/(sqrt(2)M)`.

The remaining photon equation is `C''+c_mag²C=0`. No lapse/shift Schur denominator has been divided by at any point.

For clarity, in the ordering `(zeta_bar,C,nu,S_bar,v_bar,pi_bar)`, the leading Fourier Euler matrix is

```
[ 0             0              0        -2iMx        0       0 ]
[ 0         c_mag²-x²           0         i√2B0x     0       0 ]
[ 0             0           -2κM          2Θ         0       1 ]
[ 2iMx      -i√2B0x             2Θ       -2B0²       0       0 ]
[ 0             0              0           0         0      -ix ]
[ 0             0              1           0        ix       0 ]
```

Laplace expansion along the first and fifth rows independently gives

`det E0=8kappa M³ x⁴(x²−c_mag²)`.

For the raw matrix the field-scaling determinant is p and the matrix is divided by p². Consequently `det E0=lim det E_raw/p^10`. All scaled entries have finite limits, proving that no untested p^12 term lies above the author's extracted p^10 coefficient. This is an independent check on the exact permutation calculation. The original real standing-wave action is invariant under `p→−p` combined with `C,S→−C,−S`; the determinant is even in p, giving the stated O(p^8) frozen remainder.

Without dust the same Laplace calculation gives `−8kappa M³x²(x²−c_mag²)`; adding its canonical pair contributes the additional −omega² and flips the leading sign. This reconstructs the report's corrected sign and multiplicity, rather than assuming a frozen-dust factorization.

## Simple physical root and auxiliary degeneracies

For strict c_mag²<0, `x0=±i sqrt(−c_mag²)` is nonzero and simple; `det E0` has derivative `16kappa M³x0^5≠0`. The leading matrix's kernel is exactly the exhibited nonzero C direction, with rank five. The full scaled frozen matrix is analytic in 1/p near these roots. The implicit-function theorem therefore supplies actual finite-p roots approaching x0 and finite-p null vectors approaching that kernel. It does not require invertibility of the isolated auxiliary block.

Indeed the isolated lapse/shift determinant is

`4(B0²M kappa−Theta²)p²+4B0²Sigma+2B0²Zq⁴`.

At `B0²M kappa=Theta²`, or even where its constant term also vanishes, the direct full E0 determinant, kernel and root derivative remain unchanged. These are not exceptions to this particular mode. No general constraint-count or clock-health conclusion should instead be inferred from that isolated auxiliary rank/sign. The proof avoids the singular intermediate elimination rather than cancelling a divergent expression after division.

The perturbation is physical: `delta[X−Bcal]≈−b sqrt(2)B0pC` at leading order and cannot vanish for the strict unstable branch. This scalar is gauge invariant because the corresponding background F vanishes identically. The temporal/spatial gauges and Maxwell Gauss equations have been fixed/varied, and the C kernel satisfies every retained equation. Finite-p lapse, shift, metric and dust responses are subleading in the declared scaling; the proof does not set them to zero exactly at finite p.

## Scope, evidence and remaining arrows

The physical principal conclusion is stronger than the parent's held-clock screen for this **pure magnetic** case, but remains restricted to finite smooth on-trajectory coefficients, positive finite M,kappa,Z, nonzero b, q>0 and Theta≠0. Marginal c_mag²=0, electric/mixed branches, other operator choices and global source solutions are not classified. A coherent three-U(1) triad is not ordinary thermal photons. One still needs an admitted window above all background rates and below the EFT cutoff before asserting a concrete cosmological instability; no cutoff, observed rate, recombination or CMB transfer is provided.

I inspected the frozen 27-check main output, including regular/leading-aux-degenerate/exact-aux-degenerate matrix controls and their convergence, and validated all four main/control manifests with current hashes. Those coefficient samples are explicitly algebra controls, not on-background fits or interval certificates. The universal principal proof is the raw action, leading full matrix and simple-root argument above. No external theorem supplies the EM instability, and no author source was modified or reexecuted here.

- `sol61_push/recombination_and_structure_growth/electromagnetic_radiation_completion_2026_10_06/coupled_magnetic_principal/REPORT.md`: `11207218bd0ef85bbe43d7314fbef0b5fe6b7ef46148867bf08c17ee06db99c0`.
- `sol61_push/recombination_and_structure_growth/electromagnetic_radiation_completion_2026_10_06/coupled_magnetic_principal/checks.py`: `dee8578424c8a92e0eaadb385b8dec19145b228a7743272065f25c3145eccecb`.
- `sol61_push/recombination_and_structure_growth/electromagnetic_radiation_completion_2026_10_06/coupled_magnetic_principal/runs/main_a/results.json`: `c16412411a43669113e4a3558542eee396f3ee7f16184059f873ebc1af7ae829`.
- `sol61_push/recombination_and_structure_growth/electromagnetic_radiation_completion_2026_10_06/coupled_magnetic_principal/runs/main_a/manifest.json`: `49957a7b177aab76772481faba001726ed5bba0db03775cd73a7f8804c39e898`.
- `sol61_push/recombination_and_structure_growth/electromagnetic_radiation_completion_2026_10_06/REPORT.md`: `acf1a10777142ba7e3d03d8340f576b253a0add3c5258bc240ca1462a50430c3`.
