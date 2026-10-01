# Pressure normalization correction

During this pass the independent auditor's frozen plan labelled the saved
pressure coefficients keV/cm³. Root relayed that label to the author without
first checking the original FGF019 definition. The author challenged it;
root then read the original FGF019 derivation and projection code and confirmed
the author's correction. The erroneous frozen note is preserved, not overwritten.

The actual saved basis uses

 x=r/R_t, C_SZ=sigma_T/(m_e c²), p(x)=C_SZ R_t P_e(R_t x).

Thus p and y are dimensionless; U,c,E,e map dimensionless normalized pressure
to dimensionless Compton-y. L returns dp/dx, also dimensionless. The physical
electron-pressure gradient is (dp/dx)/(C_SZ R_t²), in Pa/m with consistent SI
conversion. Neither a keV/cm³ basis conversion nor a new physical radius is
applied in FGF031. R_t is the inherited selected target radius; its physical
calibration is not established by this calculation.

The root proof declares abstract common pressure/data coordinates and remains
valid. Its constants must be interpreted in the pinned saved normalization.
No load-bearing numeric matrix or code should be silently rescaled to match
the wrong label. Any already executed arithmetic retains its original bytes
and manifest, with a metadata addendum if required. A numerical radius in the
saved convention is conditional; it is not an authenticated instrument bound.
