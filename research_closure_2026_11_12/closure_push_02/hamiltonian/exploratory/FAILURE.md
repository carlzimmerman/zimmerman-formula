# Exploratory attempt, not accepted evidence

The literal S=exp(-Pi^3) with symmetric stiffness failed its polarization Newton line search during the first exploratory32-point run. Root inspection also found that negative Pi portions already have Ssecond>0 and potential negative charge compressibility; the driver looked only at positive Pi when labeling entry. This initial state cannot certify entry from an everywhere healthy state. No result was accepted or saved from this failed attempt.

The next explicitly different candidate clamps the gate on the negative branch and uses the action's one-sided stiffness: S=exp[-max(Pi,0)^3], Gamma=gamma max(Pi,0)^2/2. This corrects the candidate's negative-lobe behavior; it is not represented as the identical original gate.

Original source SHA256: 97ec9c9234ad32cc542a4edb427877c7887e9a288254b460103e5b872c065236
