# Preserved failed checks and corrections

The first combined-current CS check (`run_current_pullback`) failed its
relative-residual assertion. Inspection showed that at the critical trial
ratio the required scale derivative is exactly zero, while graph and heavy
terms cancel to about 10^-13 in absolute units. The original script divided
that roundoff-sized residual by the roundoff-sized sum, giving a meaningless
relative error near one. The heavy derivative separately agreed to 10^-11.

The original script, contract and failed record remain unchanged.
`check_current_pullback_v2.py` normalizes the residual by the sizes of the
individual graph and heavy terms. It does not change any physical formula
or data. Its fresh contract and output are separate artifacts.

Subroute launch histories also preserve the builder's initial NumPy-bool
serialization failure and a vector-function runner contract preflight
rejection. Neither is a positive scientific result.
