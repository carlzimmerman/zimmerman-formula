# Preserved corrections and finite-evidence limits

* source_waveform.py correctly predicts the packet but its charge-history
  diagnostic divided by t_dyn instead of multiplying. The mismatch exposed the
  unit error. source_waveform_checked.py fixes only that factor and adds explicit
  assertions; the charge-history residual becomes 3.95e-5. Use the checked run.
* transport_visibility.py tried loading a static archive as a full dynamical
  state. Static data have no carrier_p key. The failed run is retained;
  transport_visibility_checked.py reads the amplitudes directly and passes.
* frequency_visibility.py initially named its conditional scalar peak-power
  coefficient "photon" power and left peak versus cycle average implicit.
  frequency_visibility_checked.py corrects terminology only. The field is
  scalar; cycle-averaged harmonic power is half the peak coefficient. No
  prescribed oscillation is used in autonomous formation evolution.
* One-step large-step qualification at 12.135 Myr passes but does not establish
  a production solver gain. Subsequent guarded trajectories shrink their steps.
  Record actual accepted durations and adaptive histories; no unchanged claim
  that .02-Myr steps solve the long-time problem is justified.
* Response probes alter only material composition/carrier coordinates near the
  live boundary, exactly preserving total cell mass and global charge and
  leaving phases/chi/pi unchanged. They are deliberate response perturbations,
  never parent populations counted as unseeded formation. Their energy defects
  and time-ceiling refinement are reported separately from the baseline.
* Positive instantaneous restoring response and a half-Myr return/overshoot do
  not prove asymptotic stability. The late 12.135-Myr audit is instantaneous;
  the finite response experiment starts at 5.7 Myr.
* A positive populated transition is not a proof that no density trough forms.
  The rebound diagnostic grows during continuation; report its actual value.
* Bright/dark transport projection is a frozen-profile linear source audit.
  Its 0.057321% kinetic fraction is distinct from measured outgoing/field-work
  efficiency. Dark directions need not stay dark under Hamiltonian mixing.
* The scalar exterior's 2-kpc mesh cannot propagate arbitrary carrier-frequency
  radiation above 306.60 rad/Myr. Present windowed high-frequency content is
  small; fast-outlet claims remain conditional on exterior refinement.
