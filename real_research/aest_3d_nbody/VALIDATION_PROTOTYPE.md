# Validation gates -- 3D AeST shear-injection NUMERICAL prototype

`collapse3d_prototype.py` is a genuine reduced 3D AeST field evolution (scalar phi +
Maxwell-antisymmetric vector A_i on a periodic grid, symplectic leapfrog, NO numerical
friction). It injects non-radial 3D shear sigma_ij (sigma_xx=-sigma_yy + off-diagonal)
and an O(1) tensor (h_plus,h_cross) drive, evolves the stiff free mode omega=mu c, and
measures the scalar-phase circular-std over the cluster volume + the mode energy vs time.

This is the NUMERICAL confirmation of the SETTLED analytic gate (phase_gate.py,
VERDICT.md, w5ze80cey). All three required gates pass; the headline run reproduces the
NO-pin.

## Headline adversarial trial (N=28^3, omega=708 H0, full 3D shear+tensor)
- circular-std of scalar phase over cluster volume: **1.865 -> 1.977 rad**
  (min over run 1.865) -- stays **O(1)**, does NOT shrink to 0.
- IC-lock |<exp(i(psi-psi_ic))>| = **0.961** -- the phase **tracks ICs ~1:1**.
- mode-energy change = **+1.382e-02** -- pumped/oscillatory, **not bled out**
  (consistent with NO friction; conservative parametric coupling).
- **Verdict: 3D asymmetric collapse does NOT phase-pin omega=mu c. NO-pin = the gate confirmed.**

## (i) Spherical / 1D limit -> reproduces the no-go (IC-tracking)  [PASS]
Random-IC-phase field, no 3D shear: circ_std 1.981->2.049 rad,
IC-lock = 0.977 (phase tracks ICs ~1:1, no organization to 0 -- the published
1D no-go, commit a0bc7620). Spherical uniform-IC breather stays coherent as ICs dictate
(circ_std 0.000->0.022).

## (ii) Deep-MOND limit -> a0 = 9.36e-11  [PASS]
a0 = 9.360e-11 m/s^2 (canonical pure-Lambda, QUARANTINED input). The stiff mode
omega=mu c is inherited from a0: naive a0/c gives 0.138 H0 (lower band),
the banked full AeST mass structure gives 708 H0 (upper band). At BOTH
bands the mode is well-separated from the few-H0 cluster drive -- the stiffness is a
consequence of the framework's own a0, not a tuned knob.

## (iii) Conservative limit -> energy drift ~ 0 (no numerical friction)  [PASS]
Gyroscopic antisymmetric (Maxwell) coupling + g2 cross vertex, NO injected drive:
symplectic leapfrog total-energy fractional drift = **-2.166e-04** over the
run (bounded, no secular loss). The integrator adds NO friction -- so any phase-pinning,
had it occurred, would be physical, not numerical dissipation.

## Adversarial control: the diagnostic is ALIVE, not rigged
The scalar mode sees the GW as a PARAMETRIC (Mathieu) drive: omega^2 -> omega^2(1 + h cos(Omega_h t)),
whose principal resonance is at Omega_h = 2*omega = 1416 H0. Driving ON that resonance vs the
off-resonant cluster drive (Omega = 3 H0), small h to stay finite:
- on-resonance (1416=2w) mode-energy change = +3.091e+13  (EXPONENTIAL Mathieu growth)
- off-resonance (3, cluster) mode-energy change = +2.542e-03
- resonant/cluster |E-pump| ratio = **1.22e+16**

The prototype pumps the mode by ~16 orders of magnitude when the drive is ON
the parametric resonance, and stays dark for the off-resonant cluster drive -- the diagnostic is
NOT dead-rigged to output NO. The cluster drive is off-resonant by ~470x (1416/3) BECAUSE the
framework's a0 makes omega stiff -- so the cluster phase is not pinned. And even when the drive DID
pump (on resonance) it grew the AMPLITUDE, consistent with the no-friction theorem: the shift-
symmetric coupling is conservative (parametric), so the phase precesses/librates, it does not
relax-and-lock to 0 (phase-pinning would need irreversible friction, which AeST has at no order).

## Quarantine
a0=9.36e-11, Z, kappa, I0 are INPUT, never derived. This prototype confirms a structural/
dynamical NO-pin; it derives none of the framework's numbers.
