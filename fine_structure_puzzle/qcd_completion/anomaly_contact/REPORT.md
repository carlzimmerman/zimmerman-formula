# Explicit anomalous contact-sector calculation

The compact Gaussian three-form model on a closed S4 has a nonzero topological susceptibility and **zero linear-H vacuum-stress coefficient**. Coupling its constant mode to a compact singlet with a periodic mass potential gives finite axial screening and no new linear-H term. This is an explicit calculation of a previously omitted sector, not a full-QCD result or an alpha prediction.

With V=8pi²/(3H^4), fixed chi_g>0 and canonical gauge measure,

    Z=(2pi chi_g V)^(-1/2) sum_Q exp[-Q²/(2chi_g V)+iQtheta]
      =sum_k exp[-V chi_g(theta+2pi k)²/2].

The complete nonzero three-form/ghost hierarchy cancels in a common regulator. Its harmonic gauge volume supplies V^-1/2; dropping it creates a spurious -1/(2V) stress. A fixed coupling-dependent overall factor is displayed in DERIVATION.md and removed only for this fixed-coupling metric question. At theta=0,

    rho=-d_V log Z ~4pi² chi_g exp[-2pi² chi_g V],
    chi_top(infinity)=chi_g.

Thus a contact susceptibility alone does not imply the required H term, even when the topological flux sum and nonpropagating sector are retained explicitly.

For a compact angle phi with canonical coordinate f_s sqrt(V)phi and periodic mass potential B(1-cos phi), unfolding the anomaly branches once gives

    Z0=mu f_s sqrt(V/(2pi)) integral_R dx
        exp{-V[B(1-cos x)+chi_g(theta+x)²/2]}.

Its exact Fourier representation is in DERIVATION.md. At B=0 this is mu f_s/sqrt(chi_g), independent of V and theta: there is no massless screening divergence. At theta=0 and fixed positive B, with a=chi_g+B,

    chi_screened(infinity)=chi_g B/a,
    rho0=B/(8a²V²)+O(V^-3).

The canonical measure cancels the Gaussian width. At fixed nonzero theta, normalized partition limits B→0 and V→infinity need not commute; no such interchange is used in the theta=0 stress result. Nonconstant singlet fluctuations at quadratic order give one ordinary massive scalar, M_s²=a/f_s². A resummed constant-mode correction must multiply that determinant by Z0/(mu/M_s), since the determinant already includes its constant eigenfunction. Interactions of nonconstant modes and domain walls are not included.

The imported FSP-003 massive scalar calculation gives the covariantly subtracted Gaussian stress a3 H^6/(64pi²M_s²)+..., a3=74/63, at fixed M_s>0 and H/M_s→0. That dependency was independently audited in the preceding phase; it is not retested by this contact script. The extra constant-mode factor starts at H^8.

The model does not supply the full function K(F) of QCD, curved hard matching, proton/quark matching, a cosmological state prescription, or a theta-independent metric factor exp[-V E_match(H,alpha)]. The latter cannot be inferred from normalized theta correlators. No numerical value for chi_g, B, alpha, or the cosmic scale is fitted. In this specified model varying fixed positive matched parameters with alpha cannot produce a nonzero derivative of its zero linear-H coefficient. A nonzero full-QCD coefficient would require physics beyond the metric functional calculated here.

## Evidence

`run-001/manifest.json` is completed and validates against current inputs. The 11.995-second bounded run passed 94 checks: exact spectral-exponent cancellation, Gaussian-moment and screening identities; flux/branch sums; compact Fourier/direct-integral identities; susceptibility moments; and finite-range stress asymptotics at 55 and 80 digits. Maximum relative error between the compact integral and Fourier representations was 2.410e-56. Finite numerical checks are not interval certificates or a proof of full QCD. The analytic identities and saddle expansion define the broader model statements.

The exact-version primary source records are in SOURCES.json. Donnelly–Michel–Wall supplies the compact gauge measure; Dvali supplies the QCD three-form motivation while leaving its effective function undetermined. No novelty claim is made.

The fresh `../reviews/contact/REVIEW.md` derived the measure and compact integrals before reading the target, found no blocking error in the defined model, and passed 47 additional independent checks. It correctly distinguishes the hand/source proof of the harmonic gauge-volume normalization from the 94-check script: that script inserts the normalized partition and checks its identities; it does not derive the gauge-group measure. Its broad result-label wording is qualified here without rewriting executed code or output. The imported H6 coefficient remains a separately pinned earlier dependency. Both current contact manifests validate.
