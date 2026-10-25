# The candidate filter supports a stable interface and reflects cold waves

**A positive result within a controlled approximation:** the illustrative Palatini candidate admits a monotone interface between a dense restored region and a broken vacuum. Its scalar fluctuation operator is nonnegative with the source held fixed. Solving the linear wave equation through this profile gives 98.96% reflection for a cold wave at a density where the interior is energetically accessible, and complete reflection at the two higher tested densities.

This is not a galaxy or cluster solution. The example keeps r=1,s=1/4, imposes a sharp planar source step, neglects Einstein-metric backreaction and holds matter fixed. It does not select reservoir abundance, incoming velocities, coefficients, or a0. In particular, a filter that also excludes clusters would fail the intended purpose. The result is an explicit wave filter, not a demonstrated astronomical separation.

## 1. Use a consistent source variable

The preceding local density test compared constant backgrounds. To perturb a field interface one must state what matter quantity is held fixed. For minimally Jordan-coupled nonrelativistic matter, use conserved Einstein-frame rest density rho_star and matter energy rho_star A(phi). Its Jordan density is rho_J=rho_star/A³. Holding rho_J fixed during field variation would describe a different externally maintained source and give a different fluctuation potential.

For the Palatini model define

    q=chi/v, z=x sqrt(D)/v, D=DeltaV,
    y=phi²/v²=sin²(sqrt(s)q)/s,
    f=F/M²=cos²(sqrt(s)q), A=f^-1/2,
    Wbar(q)=[r+(y-1)²]/f².

At r=1,s=1/4, the vacuum has y_out=2/3, q_out=0.84106867, Wbar_out=1.6 and Wbar(0)=2. The dimensionless external density is d=rho_star/D. Take d(z)=d_in for z<0 and zero for z>0. The source is immobile and mechanically supported, not freely responding cosmological dust. The scalar effective potential is

    V(q,z)=Wbar(q)+d(z) A(q),
    q0''=partial_q V(q0,z).

The Einstein metric and lapse are held constant. An infinite planar source cannot have globally flat gravity; this is a local interface approximation. Its use requires a patch small compared with gravitational curvature scales. It is not a solution of the full Einstein/source boundary problem.

## 2. Solve the boundary rather than insert a mass step

Inside, q0 approaches zero; outside, q0 approaches q_out. Translation invariance on each side gives first integrals

    q0'^2/2 = V_in(q0)-V_in(0),        z<0,
    q0'^2/2 = Wbar(q0)-Wbar(q_out),    z>0.

Continuity of q0 and q0' fixes the surface value:

    d_in [A(q_surface)-1] = Wbar(0)-Wbar(q_out)=0.4,
    A(q_surface)=1+0.4/d_in.

This is derived matching, not a fitted wall location or independent width. The interface shape follows by integration on each side. All tested d_in=20,32,100 exceed the restoration threshold 8. The solved field is monotone and approaches both endpoints within 1e-8 over each tested domain.

The interior tail is integrated in log(q), which preserves positivity and resolves its exponential decay. The first direct-q attempt crossed zero at roundoff level in the high-density tail and then evolved on the wrong numerical branch. Its failed record and original code snapshot are preserved under `run/`. The corrected run uses the same equations and acceptance tolerances, recorded under `run_fixed/`.

## 3. Scalar stability has an analytic check

For fixed matter and metric, let

    L=-d²/dz²+V_qq(q0,z),  w=q0'>0.

Away from the source step, differentiating the background equation gives Lw=0. At the step, q0'' jumps by -d_in A_q(q_surface). In distributions,

    Lw=d_in A_q(q_surface) delta(z).

For any smooth compactly supported fluctuation h, integration by parts gives

    integral [h'^2+V_qq h²] dz
      = integral w² [(h/w)']² dz
        + [d_in A_q(q_surface)/w(0)] h(0)² >= 0.

Here A_q>0 on this branch. This establishes no negative scalar modes in the fixed-source, flat-metric problem. The potential can have a locally negative region without an unstable eigenmode. Transverse planar momenta add a nonnegative k_parallel² term. This proof does not include matter motion, metric perturbations, nonlinear fragmentation, or quantum corrections.

Finite-domain Dirichlet spectra independently support the sign:

| d_in | Lowest eigenvalue at domain [-20,20], spacing 0.01 |
|---:|---:|
| 20 | 2.922593 |
| 32 | 3.356829 |
| 100 | 3.502225 |

Eigenvalues use dimensionless z units. Comparing spacings .02 and .01 changes the lowest value by at most 9.17e-4. Comparing domains [-15,15] and [-20,20] passes the predeclared .01 tolerance. These finite calculations corroborate the analytic conditional stability argument; they are not a live-gravity stability certificate.

## 4. Scatter waves through the calculated profile

Write a small fluctuation as exp(-i omega t) u(z), in the same rescaled units:

    u''+[omega²-V_qq(q0,z)]u=0.

The asymptotic squared masses are

    m_out,E²=5.76,  m_in,E²=d_in/4-2.

For an incoming vacuum wave with p/m_out=epsilon,

    omega²=5.76(1+epsilon²).

Integrate from the interior with a purely outgoing wave when omega²>m_in², or the decaying solution when omega²<m_in². Resolve incoming and reflected amplitudes in the vacuum. For propagating interiors the transmitted flux includes the wave-number ratio k_in/k_out; amplitude squared alone is not transmission. For a forbidden semi-infinite interior, there is evanescent penetration but no transmitted flux to minus infinity.

| d_in | p/m_out | Reflected flux | Transmitted flux |
|---:|---:|---:|---:|
| 20 | .001 | .989573 | .010427 |
| 20 | .1 | .362791 | .637209 |
| 20 | 1 | .017161 | .982839 |
| 20 | 3 | .000591 | .999409 |
| 32 | .001 | 1 | 0 |
| 32 | .1 | 1 | 0 |
| 32 | 1 | .054647 | .945353 |
| 32 | 3 | .001475 | .998525 |
| 100 | .001 | 1 | 0 |
| 100 | .1 | 1 | 0 |
| 100 | 1 | 1 | 0 |
| 100 | 3 | .018886 | .981114 |

Only .001 is a representative nonrelativistic cold speed (approximately 300 km/s under the conventional relativistic scalar interpretation). The larger values are high-energy controls, not realistic cluster velocities or a proposed reservoir spectrum.

The important additional result is reflection at d=20 even though m_in²=3 < m_out²=5.76. An allowed interior is not sufficient for efficient transmission: a slow wave with wavelength longer than the boundary's variation scale can reflect strongly. Thus the earlier threshold-only argument was insufficient. The reflection depends on the solved interface and incoming momentum.

At d=32 and 100, the slow-wave energies are below the interior propagation threshold. This confirms the energy barrier in the stated semi-infinite geometry. Finite objects allow tunneling; a smooth density gradient can substantially change above-threshold reflection. We have not computed either. Actual galactic/cluster gas gradients cannot be assumed to be this sharp.

## 5. Frame consistency and conservation

All frequencies, asymptotic masses and wave fluxes are evaluated in the Einstein frame with its stipulated constant lapse. The conformal Jordan lapse is retained implicitly by that consistent choice; local Jordan masses must not be compared while dropping the lapse transformation. The vacuum-to-interior shift in ln A is about .091 for this example, so doing that would be a material error.

Maximum |R+T-1| is 4.12e-10. Changing the integration domain changes the reflected fraction by at most 1.32e-10. These are linear flux checks for a fixed source, not a total matter/gravity energy ledger. The wall can exert a force on its externally supported source; a live calculation must track recoil and work.

The density d is external conserved rest density. It is not the cold-field density being produced. Assigning the same cold energy both to d and to the scalar stress would double count it.

## 6. What this establishes for the framework

There is now a resolved, conditionally stable mechanism that can reject slow excitations, rather than an assumed environmental retention factor. It survives the elementary scalar-interface and flux checks. That is the positive advance.

The original objective remains open. The candidate has not fixed r,s or the vacuum energy; it has not produced a normalized reservoir; it has not passed a galaxy law or cluster-profile likelihood; and the strong matter coupling from the preceding calculation has not been rendered harmless by these fixed-source results. This interface calculation supplies no MOND force amplitude or microscopic protection of vanished response terms.

The next discriminating tests are smooth finite-density profiles with live matter/metric response and actual cluster/galaxy source densities, followed by production from a specified cosmological state. A successful filter must transmit or retain enough material in clusters while rejecting the problematic galaxy contribution with the same derived coefficients. The present high reflection at a nominally accessible density warns that the filter could reject too much material everywhere. Do not treat the illustrative densities as an observed environmental split.

## 7. Reproduction and provenance

Current evidence: `run_fixed/result.json` and `run_fixed/manifest.json`; deliberate missing-source mutation: `mutation/manifest.json`. Both validate against current input hashes. Historical `run/manifest.json` records the numerical failure before log integration; its script input is superseded, so it is not advertised as validating against the current script. `run/check_at_failure.py` preserves the original implementation for inspection.

`FROZEN_CRITERIA.md`, `contract.json` and `check.py` define the bounded single-thread computation. The deliberate mutation omits matter from the interior first integral and fails surface derivative matching. The continuum scalar-stability argument was derived after the finite calculation and is self-reviewed; it does not change the frozen numerical criteria. No independent referee or novelty claim is made.
