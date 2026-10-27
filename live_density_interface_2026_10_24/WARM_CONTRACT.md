# LD-3: distinguish unfinished optimization from loss of the near-law branch

LD-1 beta1000,k120,tau1,K3 has qinner .9936, outer F mass about1.59Mb and
law error .0318dex, but fails material stationarity. It is a candidate only.
Use its computed mobile density as the warm start, direct masses, exact
saturation constraint and energy scaling /100. n96 then192; extend domain
2 to4 at n192 (same spacing as initial n96) to test boundary confinement.
No target-law density is inserted during interpolation. An inadmissible
continuation is not used as the next start. This is an optimizer/refinement
test, not a new model. Candidate must pass all original criteria.
