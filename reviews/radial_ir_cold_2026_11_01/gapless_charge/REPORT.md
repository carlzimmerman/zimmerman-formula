# TP04 gapless-sector result

The twelve unbroken gauginos acquire nonzero finite one-loop masses. At the
leading finite-CW vacuum, the residual neutral photino has

    m_photino=1.1164161506e−4 mu e^(5/2), F_eff=mu²/sqrt(31).

It is a serious separate fermion candidate; cold occupation and its actual
Goldstino decay must be assessed by the cold-state lane. None of this relies
on exact global charge conservation. The full thirteen-dimensional neutral
nullspace check confirms negligible Goldstino/photino mixing at this order.

The residual photon remains massless. Charged heavy fields leave the exact
U(1) anomaly term −5g1²theta F1 Ftilde1/(32pi²). A constant rotating phase in
an infinite empty vacuum consequently has a gauge-helicity instability:

    gamma_max/|omega|=5g1²/(16pi²)
       =4.5911078e−7 (.01),4.1319371e−6 (.03),4.5911161e−11 (.0001).

This is a zero-temperature channel. Tiny nonabelian instantons do not protect
that rolling state. A finite patch needs an admitted wave number below
5g1²|omega|/(8pi²); conductivity, expansion, coherence time and seed energy
then determine whether growth depletes the charge. The result is an actual
conditional instability scale, not a selected cosmological lifetime. The
uncharged radial candidate has omega=0 and avoids this particular source.

Full mass-basis one-loop gauge threshold logs and the radiative gaugino
threshold give extremely small formal pure-YM scales. At e=.03,
log10(Lambda/mu) is about−23890 for SU3 and−35834 for SU2; at weaker coupling
the suppression grows as exp(−const/e²). These are running-scale estimates,
not a nonperturbative gap or susceptibility calculation. The nonabelian far
IR is not massless-gaugino SYM, because m_lambda≫Lambda.

Evidence: run_003 passes 22 controls, run_ir_001 passes 33, run_null_001 passes 2.
All three completed v2 manifests validate. Largest observed RSS 98.9MB; all
runs used one numerical thread and minute-scale caps. run_001 serialization
failure and run_002 benchmark auxiliary-sign failure remain preserved. The
first prelaunch was rejected for a missing contract `inputs` field; no
scientific child executed in that attempt. No previous-science file changed.

Remaining dependencies are explicit: finite two-loop fermion self-energies;
occupied-state nonlocal light response; a thermal/state/patch specification
for a fractional charge lifetime; nonperturbative strong dynamics; and the
photino decay/cold distribution in the companion lane. These do not erase
the measured leading masses or the local U(1) helicity equation.

See DERIVATION.md for raw equations, sources, tested domains and distinctions
between vacuum poles, background thresholds and conditional thermal drift.
