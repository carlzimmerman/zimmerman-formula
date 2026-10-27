# Independent finite-mode outlet audit

Read-only audit of ../eos_route/wave_outlet.py and
../eos_route/run_wave_extended/result.json, 2026-10-27. No new outlet model run.
Primary verdict: **the finite semidiscrete energy outlet is consistent with the
displayed reciprocal action; numerical evidence covers the declared two meshes**.
This is not a field-theory completion, gate derivation or formation calculation.

## Action and reciprocal sign

For

    L = mu/2 (qdot^2 - omega^2 q^2)
        + 1/2 int (chidot^2-c^2|grad chi|^2) dx
        + qdot int J chi dx,

variation gives

    mu(qddot+omega^2 q) = -int J chidot dx,
    chiddot-c^2 Laplacian chi = J qdot.

The script's skew matrix G has exactly these opposite signs. The Hamiltonian is

    H = (p_q-int J chi)^2/(2mu) + mu omega^2 q^2/2 + H_chi.

It is nonnegative for positive mu, omega^2, c^2 and the stated positive wave
energy. In velocity variables the interaction cancels from the energy sum.

The proposed source also has the right bulk factor. With conserved current
j^mu=n u^mu, integration by parts gives

    n j^mu partial_mu chi = -chi j^mu partial_mu n + divergence
                         = chi n^2 partial_mu u^mu + divergence.

For a static background and velocity qdot xi, this yields
J=g n0^2 div xi. The discarded divergence needs the stated regular/material
boundary treatment; this is not a derivation of a microscopic gate.

## Radial energy and boundary convention

With w=r chi and regular center,

    int_0^R r^2 chi_r^2 dr = int_0^R w_r^2 dr - w(R)^2/R.

Therefore the reported reduced canonical energy and physical finite-ball wave
energy differ by

    E_phys = E_can - S_R,    S_R = 2 pi c^2 w(R)^2/R.

For an initially quiet boundary, physical export equals canonical export plus
S_R. The canonical outgoing condition w_t+c w_r=0 gives canonical power
4 pi c w_t^2 >=0, matching the endpoint damping D in units c=1. The discretized
last row implements an approximate outgoing impedance, rather than an exact
reflection-free boundary for every lattice frequency.

The saved outer-band amplitude bounds S_R/E_initial below 1.40e-4 (using R>=85
conservatively). This omitted physical/canonical correction cannot change the
qualitative energy-transfer conclusion. The exact endpoint field was not saved,
so the exact correction cannot be recovered from this result file.

## Midpoint ledger and finite numerical evidence

The update is implicit midpoint for

    M vdot = G v - K z - D v,    zdot=v,

with G antisymmetric. Its quadratic discrete energy satisfies exactly

    E_(n+1)-E_n = -dt v_mid^T D v_mid.

Thus summing that same export is the right energy ledger, and tiny ledger error
is expected from the integrator. It does not independently validate continuum
accuracy, causality or the physical core model.

At t=350, the fine mesh reports:

* core energy fraction 0.0154759365985;
* wave energy fraction 0.0310121797593;
* exported canonical wave energy fraction 0.953511883643;
* relative energy-ledger error 6.66e-13.

Fine minus coarse is +0.00111011 for final core fraction and -0.00148006 for
export. This supports the bounded qualitative outlet result. One joint dx/dt
refinement does not determine convergence order or isolate space/time errors.
The open-boundary checks in the script auto-pass when OPEN_OUTLET is true; they
are declarations of the chosen model, not numerical reflection tests. No strong
claim of a verified transparent boundary should be attached to them.

Minor issue: line 16's comment says the boundary stays outside the light cone
during the run. It is correct for t=70 and stale for the t=350 outlet extension;
the actual output correctly records boundary_reachable=true.

## Audited hashes

SHA-256:

* wave_outlet.py: de2101f88a2a825841410b5f907f016ee9a44cbfa89ca71544def82d69ef97b0
* run_wave_extended/result.json: 12b046f53e599ff64132cf9d41c258592d4ea9d1bb44ee32927785c9d076fe00
* run_wave_extended/manifest.json: 3fc468ec9213683eb973a1268fc4c0faa5964bb7dbe85d757494ba455d18a729

The manifest reports completed, exit 0, runtime 4.20796 seconds. Implementation
and algebra were audited independently by the kinetic-route subagent; the model
was not rerun during this review.
