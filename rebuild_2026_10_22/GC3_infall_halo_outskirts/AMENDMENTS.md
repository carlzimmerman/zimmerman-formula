# GC3_infall_halo_outskirts: AMENDMENTS

## A1 (code-only fix after the first run; its R4 result is WITHDRAWN as an artefact)

**The bug.** The first run's saturation branch set r₀ = 10⁴ R500 whenever the target mass could not be reached. At fixed
core surface density Σ, the cored infall profile's mass inside R500, M(r₀) = 4πΣ r₀² I(R500/r₀), rises and then falls
with r₀, peaking at r₀ ~ R500. Every cluster-cell saturated (1956/1956), and the r₀ = 10⁴ R500 choice left almost no
halo.

**The withdrawn result.** The first run's "G-OUT-M3 Z +11.35, 11 keys UNDER" is an artefact of that branch.

**The fix.** X43's own A1 convention: the compact root on the rising branch, saturating at the peak (maximum mass inside
R500) when the target is unreachable. That is what the frozen S0c wording ("saturated cases are counted") presupposes.

**The structural fact the bug exposed (reported, not graded).** At X43's Σ, a cored profile may be unable to hold
(Ω_c/Ω_b) M_b inside R500 at all. The rerun reports the saturated fraction.

**Unchanged:** model, gates, normalisation target and variants.
