# Fresh soft/current and crossed-collision review

**Normalized claim:** The displayed leading rigid canonical EFT in `cold_states/SOFT_COMPLETION.md`, at its explicit1MeV,e=.003 benchmark, bounds the named phase-radiation and light-Goldstino-exchange corrections to the Ward decay and the named NR collision classes. The previously matched pole/Ward coupling and anomaly coefficient are inputs. There is no all-orders, thermal-history or abundance claim.

**Primary verdict: proved as written** for those displayed leading formulas and their stated threshold/current domain. I reconstructed their load-bearing spinor, spectral, propagator and flux steps rather than relying on small numerical ratios. `CROSSED_HARD_COLLISIONS.md` also passes for its hard class. The coordinator's still looser crossed coefficient is safe, with the factor relation below.

## Direct current radiation

The phase law is fixed by the actual microscopic R charges: theta shifts by2alpha while chi and G have charge1, so the mass and Ward dipole carry exp(-i theta). This preserves the earlier distinction between a mode-derived coupling and an invented exponential kinetic portal. In a linear canonical fermion basis the mass supplies y=m/a and the dipole its phase contact; a field redefinition merely moves this coupling into current vertices.

For incoming p=(m,0), the exact Dirac identity

    (pslash-qslash+m)gamma5 u(p)=-qslash gamma5 u(p)

removes the apparent soft pole. Since ||qslash||<=2q0 and the denominator is2mq0, the initial-leg insertion is bounded by y/m=1/a. The contact has the same1/a factor. The final Goldstino and photon energies are at most m/2. With the author's authenticated kappa=m/(2sqrt2F), each contribution has per-label norm<=4kappa m²/a, and the combined final-spin/polarization squared bound is256kappa²m4/a². Multiplying Phi3=m²/(256pi³) and1/(2m), then dividing by Gamma2=kappa²m³/(2pi), gives exactly m²/(pi²a²). No soft regulator or unprovided phase population is needed.

## Anomaly spectral step and light exchange

For L=ga pi FtildeF/4, a virtual transverse photon of mass sqrt(s) has width ga²s^(3/2)/(96pi): the three-polarization average gives squared amplitude ga²s²/6. Thus ImSigma_T=ga²s²/(96pi); the two photon propagators cancel the s², leaving the stated finite spectral measure.

I independently reconstructed the dipole trace. Put k for the final massless Goldstino and q=p-k. Between on-shell spinors,

    ubar(k)[qslash,gamma_mu]u(p)
       =2[(p+k)_mu ubar(k)u(p)-m ubar(k)gamma_mu u(p)].

The spin-averaged contraction with the transverse polarization sum is4(m²-s)(2m²+s). Including the two-body momentum factor gives f(r)=(1-r)²(1+r/2), and its integral is3/8. Consequently Gamma_anom/Gamma2=ga²m²/(256pi²). The Cauchy--Schwarz interference bound with direct radiation is valid even without fixing relative phases. The anomaly coefficient's sign cannot invalidate an upper bound.

For chi->gamma+G*->gamma+lambda_a+g_a, q²>=ma²: the nonzero final gaugino mass genuinely excludes the massless Goldstino pole. Two dipole commutators, the propagator norm and spinor norms give the stated32kappa1kappa_a m4/ma² amplitude envelope. Eight final spin/polarization choices and da colors then give4da/(pi²ra²)(m²/F)². Both SU3 and SU2 are included; r2=.6008 is below1. The U1 final state has no available energy. This named light exchange is distinct from the heavy local dimension-seven transition and has not been hidden in its Wilson coefficient.

## Collision normalization and domain

At threshold, a phase t/u fermion propagator has denominator-2m² and numerator norm<=2m. Each exchange is<=2m²/a², and the actual mass-phase contact is<=2m²/a². The radial exchange uses y_sigma_chichi=kappa_s m/a, the derivative sigma-phase-phase vertex and the nonresonant denominator mrad²-4m². This reproduces the stated8|kappa_s|m4/[a²(mrad²-4m²)] addition. Identical final phases give sigma v<=|M|²/(64pi m²), agreeing with the author's formula. The declared small NR velocity is far from any pole; a modest uniform cushion suffices for finite-v use, but the evidence is correctly labeled threshold rather than a thermal average.

For crossed hard chi chi->VV, all external states are still neutral under the residual U1, all loop edges remain charged, and routed momenta<=2m are negligible compared with M. The same per-label bound4Bloop m³/M³ therefore applies. With the generous final-label count32768 and no identical-final suppression,

    sigma v <= 32768*16Bloop²m6/M6 /(32pi m²)
            =16384Bloop²m4/(pi M6)
            =c7_eff²m4/(16pi M6).

The microphysics author's c7_eff²m4/(pi M6) adds a factor16. The coordinator's16c7_eff²m4/(pi M6) adds a factor256 relative to the direct majorant; it is valid as a generous cushion, not the exact result of multiplying that direct expression by16. Initial-spin averaging does not increase a uniform bound. For identical incoming particles, the per-particle annihilation loss is n sigma v: the event factor1/2 and two lost particles cancel.

The optional two-Ward-dipole exchange diagrams have no threshold pole (t=u=-m²). For chi chi->gamma gamma, two commutators<=4m, a propagator<=2/m and spinor product<=2m give a conservative per-route64kappa²m². For chi chi->GG via a photon, the vector-current norm is<=4m at q0=0, giving the same envelope. Two routings plus an extra Majorana factor2, four final labels and phase space imply128m6/(pi F4) per named diagram class. An inclusive512m6/(pi F4) also cushions the two channels and |p|/m<=.001. This statement is about two Ward vertices, not every amplitude with a GG final state: scalar-mediated GG and direct hard four-fermion matching are separate obligations, addressed by the companion lane rather than silently omitted.

## Finite reconstruction

`run_soft_review` reproduces the formulas independently from the frozen mass/unit inputs. All7 controls pass and the v2 manifest validates. The spectral integral was also checked as the exact rational3/8. At the specified benchmark:

| Quantity | Reconstructed upper ratio/value |
|---|---:|
| Direct phase radiation/Gamma2 | 8.4810910123e-27 |
| Anomaly-only radiation/Gamma2 | 2.2625246822e-43 |
| Combined phase radiation/Gamma2 | 8.4810910999e-27 |
| SU3+SU2 light exchange/Gamma2 | 6.3125654287e-39 |
| Phase annihilation sigma v, GeV^-2 | 1.2545275493e-45 |
| Direct hard-crossing sigma v, GeV^-2 | 9.5576251729e-36 |
| Coordinator-cushioned hard sigma v, GeV^-2 | 2.4467520443e-33 |
| Coordinator-cushioned hard n sigma v/Gamma2 | 9.9692341618e-28 |
| Phase n sigma v/Gamma2 | 5.1115432519e-40 |
| Named two-Ward diagrams n sigma v/Gamma2 | 5.3696909656e-66 |

The local density is the explicitly chosen .3GeV/cm³ benchmark, not a fitted halo. The conversion n=.3(hbar c)³/m is dimensionally correct; rate n sigma v has energy dimension1. These bounds say nothing about an unspecified early hot bath or a production mechanism. Interference between named amplitudes with the same final states can be bounded by Cauchy--Schwarz; the displayed many-order margins leave it negligible, while no signed cancellation is assumed.

## Scope and provenance

This is a fresh constrained review: I requested the omitted light completion, supplied the already authenticated anomaly convention and discussed possible channels, but did not author its norms or spectral proof. I previously authored the radial/current matching; hence the review is not blind to the action or benchmark. The exact Ward and anomaly normalizations are inherited previously reviewed inputs, not newly authenticated literature here. The source bytes and reconstruction evidence are pinned in `SOFT_REVIEW_INPUTS.json` and `run_soft_review/manifest.json`.

The leading loss budget now has explicit bounds for the named hard and light channels. This supports a conditional long-lived cold photino state at the benchmark, while higher-order/nonperturbative/UV/gravity effects, other specified collision states, photon identification and cosmological preparation remain outside the claim. No local decay proof alone selects that population.
