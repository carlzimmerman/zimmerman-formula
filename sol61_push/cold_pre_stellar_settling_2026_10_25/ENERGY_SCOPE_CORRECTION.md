# Correction to the frozen energy-screen interpretation

The saved ENERGY_CONTRACT.md used 'stationary/time-averaged' too broadly. It is retained byte-for-byte as a producer input. The computed target energy applies to the exact stationary smooth density, or a density with negligible/explicitly accounted fluctuations. It does not in general apply to every field whose mean density is Plummer.

For a fixed baryonic source, write rho=mean(rho)+delta(rho). Then

< W[rho] > = W[mean(rho)] + < W[delta(rho)] >,

where <W[delta(rho)]> = -integral <|grad delta(Phi)|^2>/(8pi G) <= 0 under isolated boundary conditions. Ub and Wb are linear in rho. Thus the averaged virial target has the additional term .5<W[delta(rho)]>. Strong fluctuations can supply extra negative binding and remove a positive smooth-profile gap. They may also change forces felt by the stars; neither effect may be omitted selectively.

The stationary profile screen and its numerical values remain correct. Its interpretation is narrowed, not a claim that fluctuating envelopes are excluded. The independent reviewer identified this distinction before the final result. Analysis reports the finite sampled fluctuation-binding identity separately; that sample identity alone does not establish temporal stationarity, isolated escape or stellar safety.
