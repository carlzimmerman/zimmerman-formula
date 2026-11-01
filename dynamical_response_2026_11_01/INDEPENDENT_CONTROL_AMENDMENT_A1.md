# Independent reference-integrator accuracy amendment

The original independent_checks_001 is retained with its failed global gate.
Its matrix, scalar pulse, angular, harmonic shell Gram and force-sum controls
passed. Direct finite-system state responses agreed with the analytic response
to about 2e-10 or better, and final quadratic energies/angular momenta agreed
to about 6e-10. The failing entries were the independently integrated work and
torque for the two highest-frequency synthetic pulses, whose retained energies
were only about 1e-11 to 2e-13. A uniform absolute ODE tolerance of 2e-14 did
not control the cancellation needed in those accumulated ledgers: their own
work-energy identities failed by the same amounts as their comparisons to the
analytic result. This identifies insufficient accuracy of the reference work
integrator rather than a demonstrated error in the analytic response.

The original code and contract remain unchanged. check_response_v2.py changes
only the finite-system DOP853 reference accuracy and conditioning. It
integrates response divided by amplitude and ledgers divided by amplitude
squared, converting back before comparison. It uses rtol=2e-13, componentwise
atol=2e-18 for the normalized complex response and 2e-20 for normalized ledgers,
and max_step=T/4096. It keeps the pulse-specific control unchanged. No physical
matrix, frequency, source, amplitude, quadrature, comparison scale or 2e-6
pass gate changes. The v2 frozen contract records these choices before its run.

Command under the root's bounded runner:

    python3 dynamical_response_2026_11_01/check_response_v2.py NEW_RUN/result.json

The new result must pass independently; this amendment does not declare the
failed original run successful.
