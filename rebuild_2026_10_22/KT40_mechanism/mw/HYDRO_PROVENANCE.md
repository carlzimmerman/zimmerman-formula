# Failed restoring-force assumption retained

hydro_001 stopped at an assertion requiring g_z>0 before writing numerical
results. This was an assumed physical property, not a convergence condition.
The fixed law must determine this sign. The original code, contract and failed
manifest remain unchanged. The continuation in diagnose_hydro_v2.py keeps
all numerical identities and accuracy gates. It records signed g_z and the
hydrostatically required dP/dρ; negative values are classified as absence of
a positive-compressibility barotropic hydrostatic closure at that point.
The rank-one finite-pressure instability criterion is applied only where
both required sound-speed squares are positive. No negative number is clipped
into an acceptable physical gas model, and no observational cut is changed.
