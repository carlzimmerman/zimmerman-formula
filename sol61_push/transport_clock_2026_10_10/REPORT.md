# A transport clock for cold-energy assembly

2026-10-10. Research checkpoint, not theory closure. Started at `23fd031bc0b8b4889b41a30d897f55ef2b2efa5a`; incorporated the subsequent committed CFG588 result at `e7bd0a4433286b1a96df17bf8b4fbca776c0287c`. Work scope is this folder only.

**New project-level result:** the existing settling equation gives an explicitly radius-dependent delivery rate. It does not justify replacing the entire halo by one age-dependent amplitude. Mass conservation then connects that amplitude to the edge and delivered supply. These are analytic consistency conditions and a concrete route to a physical assembly model, not a discovered substance or a derived coefficient.

Target: turn the [ACE hypothesis](../../campaign_fresh_gravity/MODEL_accumulating_cold_energy_2026-10-10.md) and the [partial-profile clue in CFG593](../../campaign_fresh_gravity/CFG593_required_halo_profile/README.md) into a conserved dynamical prediction. The first checkpoint is a necessary transport relation; success at the full target would additionally require stable kinetics and a raw-data test.

## What changed in the latest work

- [CFG595](../../campaign_fresh_gravity/CFG595_measured_cold_supply/README.md) finds more available cold mass, not less. Its roughly 21% assigned source fraction is an engine diagnostic; supply normalization is unconverged and the bound network percolates. It does not measure an observed settling fraction.
- [CFG588](../../campaign_fresh_gravity/CFG588_within_class_clock/README.md) reports a common within-class colour slope near Z=3, but its frozen verdict is SPLIT and late-type mass matching fails. Colour is not a calibrated formation age. Clock universality is unestablished.
- [CFG596](../../campaign_fresh_gravity/CFG596_lean_pm_1024/README.md) has validated engineering changes; this checkpoint does not import a completed new shear verdict. [CFG597](../../campaign_fresh_gravity/CFG597_merger_settling_stopwatch/FROZEN_CRITERIA.md) is separately testing merger response. Neither is rerun here.

## 1. Derive the delivery rate before choosing an age formula

Use [CFG541 E3–E6](../../campaign_fresh_gravity/CFG541_cold_energy_equations_precise/EQUATIONS.md):

\[
\partial_t\rho_c+\nabla\cdot[\rho_c(u_c+v_s)]=0,
\quad v_s=-\alpha\tau\nabla\psi,
\quad\nabla^2\psi=4\pi G(\rho_{\rm ph}-\rho_c)_+.
\]

Specify the benchmark completely: spherical deep-law target \(M_0(<r)=Cr\), \(C=V_f^2/G\); a filled core with zero enclosed deficit at \(r_i\); a uniform partial fraction \(0<f<1\) immediately outside it; local density dominated by this cold component; no mean radial orbital flow; switches fully on and caps inactive. Only the **instantaneous derivative** at this profile is claimed. The ideal core is not a globally realistic central solution.

Then \(\rho_c=fC/(4\pi r^2)\), \(\tau=r/(\sqrt f V_f)\), and the enclosed deficit is \(D=(1-f)C(r-r_i)\). Gauss's law and the drift give

\[
v_s=-\alpha V_f\frac{1-f}{\sqrt f}(1-r_i/r),
\qquad
J\equiv-4\pi r^2\rho_cv_s
=\frac{\alpha V_f^3}{G}\sqrt f(1-f)(1-r_i/r).
\]

Conservation, \(C\partial_t f=\partial_rJ\), therefore implies

\[
\boxed{\partial_t f=\alpha V_f\sqrt f(1-f)\frac{r_i}{r^2}
=\Gamma(r)(1-f)\frac{r_i}{r}},
\quad\Gamma=\alpha\sqrt f V_f/r.
\]

At 10 core radii the homogeneous relaxation estimate \(\Gamma(1-f)\) is ten times too large; at 100 it is 100 times too large, under these assumptions. This is a geometric effect, not a fitted suppression. Far from the core the inward current becomes almost constant, so most entering mass passes through rather than accumulating locally. In the ideal scale-free case with the corresponding enclosed deficit and no core offset, J is exactly constant and the interior density has zero instantaneous derivative. That limit requires boundary flux; it is not an isolated steady finite halo.

**The useful door is an evolving radial delivery profile with a finite reservoir.** Inner regions fill faster than outer ones in this benchmark. A moving transition is plausible; no stable travelling front or full kinetic solution has been proved. Uniform f is immediately lost, so this formula must not be integrated as a closed one-variable ODE.

For an outer feeding boundary R with no replenishment or return current,
\(\int_0^T J(R,t)dt\le S_{\rm available}\). For approximately constant parameters and \(R\gg r_i\), this gives
\[
\alpha\lesssim\frac{G S_{\rm available}}{T V_f^3\sqrt f(1-f)}.
\]
This constrains the same alpha that enters merger dynamics, without assuming that formation and recentering have the same response time. Unsettled material in the local density changes tau; orbital return flux changes the net current. Neither may be omitted in an actual application to CFG593's profiles.

## 2. The exact amplitude–edge–supply relation

For fixed point baryons, fixed a0, and the **exponential** kernel written in THEORY_v1, set \(r_M=\sqrt{GM_b/a_0}\). The base cold mass is
\(P(r)=M_b/[\exp(r_M/r)-1]\).
The kernel is the empirical form in [McGaugh, Lelli & Schombert (2016), Eq. 4](https://arxiv.org/pdf/1609.05917); this calculation adds no novelty claim for that relation. The legacy repaired `nu_mono` table is a different function; the exact formulas here concern the exponential kernel, and the deep limit is shared.

An ACE amplitude B truncated at edge R contains settled mass S:
\[
\boxed{S=B P(R),\qquad R=\frac{r_M}{\ln(1+B M_b/S)}}.
\]

- **Fixed settled S:** increasing B contracts the edge. For the illustrative \(S/M_b=5.364\), doubling B from 1 to 2 changes \(R/r_M\) from approximately 5.850 to 3.156. The edge becomes 54% as large. This is not a measured galaxy result.
- **Fixed edge:** doubling B requires doubling settled S. An unexhausted reservoir can supply it, but must lose that mass. Fixed total catchment mass alone does **not** force contraction while delivery continues.

In the deep limit \(BR\sqrt{M_ba_0/G}\simeq S\). Thus amplitude, size, and delivery cannot be independently prescribed. For a filled core and partial outer profile the corresponding relation is \(S=P(r_i)+f[P(R)-P(r_i)]\).

Source-free continuity with no central flux also fixes the total mean radial transport needed by \(\rho=B(t)\rho_0(r)\):
\[
u_{\rm tot}=-\frac{\dot B}{B}\frac{P}{P'}
=-\frac{\dot B}{B}\frac{r^2}{r_M}(1-e^{-r_M/r})
\simeq-r\dot B/B.
\]
An exactly source-free compact component needs a material edge and constant total mass. If a0 varies while Mb stays fixed, add \(r\dot r_M/r_M\) to this velocity; the fixed-scale comparison must not be applied unchanged. If “settled” is a label converting from another component, its equation has a transfer source, and this velocity need not describe it; the sum of both components must still conserve mass.

In an isolated spherical filled interior with B>1, CFG541's one-sided deficit is zero there and exterior deficit shells exert zero interior force. Its deficit drift therefore cannot generate the required extra inward current in that region. Ordinary orbital inflow or a changed physical coupling is needed. A delivery clock toward the original target alone does not explain above-target old-galaxy mass.

## 3. Execute the next discriminating check

Use the existing early-type old/young radial lensing vectors, with their joint covariance. Fix inner amplitudes on a declared inner band, then predict a disjoint outer band under (a) equal settled S with moving edges, and (b) equal edges with increasing S and explicit reservoir depletion. Freeze the radius split, mass treatment, reservoir profile, and environment treatment before fitting. Forward-project each full density; do not identify lensing amplitude epsilon directly with B.

For compact spherical settled components with equal S, the settled contribution beyond both edges is exactly \(\Delta\Sigma=S/(\pi R^2)\), so their difference vanishes there. The total lensing difference need not vanish if reservoirs, baryons, or environments differ. This is why those contributions belong in the test, not in an unmodelled correction.

Before a full data comparison, check the actual radial flux in the existing dynamics against section 1, then add the recorded orbital and unsettled terms. Formation mainly probes a radial mass change; merger recentering probes a displacement. One alpha does not make these one scalar clock. Linearize the two-sided drift alone about a fixed matched target \(\rho_0=\rho_{\rm ph}\), with zero background deficit force, and write \(\eta=\rho_c-\rho_0\). Then \(\partial_t\eta=-4\pi G\mathcal M\eta+\nabla\mathcal M\cdot\nabla\psi\), \(\mathcal M=\alpha\rho_0\tau_0\), \(\nabla^2\psi=-4\pi G\eta\); the second term and boundaries distinguish these spatial modes. A nonzero background deficit force adds a mobility-variation term. One-sided drift at zero deficit is not differentiable and is not covered by this linearization.

## Evidence and limits

`check.py` evaluates the identities using independent finite differences of flux assembled from density, Poisson force, and drift. It checks integral mass balance and includes a negative control that replaces the radial result by homogeneous relaxation. The v2 run manifest records the actual revision, dirty workspace, execution limits, inputs and output hashes. See `run/manifest.json` and `run/results.json`.

Independent read-only derivations by `latest_supply_door`, `latest_clock_door`, and `edge_clock_audit` agreed on the equations. The audit required the zero-central-flux condition, separated settled S from total catchment mass, and restricted the finite-core result to its instantaneous derivative. Those qualifications are incorporated above. Agent agreement is not a formal proof certificate.

Local overlap check covered ACE, CFG541, CFG557, CFG593, CFG595 and the previous Sol61 kinetic and counter-transport reports. The conservation law and finite-time filling are not new principles. The displayed finite-core suppression and explicit ACE amplitude–edge trajectory were not found in those reviewed records. Limited web discovery checked the RAR attribution and constant-flux terminology; it is not a global novelty search. No new observational detection, repaired kinetic closure, kappa=1/2 derivation, 32pi-squared resolution, or TOE closure is claimed.

Remaining dependency: a conserved, kinetically supported transport model that produces the above-law old-galaxy signal, preserves young-disc predictions, and passes the framework-native data tests. This checkpoint supplies benchmark equations and a discriminating work order, not that missing model.
