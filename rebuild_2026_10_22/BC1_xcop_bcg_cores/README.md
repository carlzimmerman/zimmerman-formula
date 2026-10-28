# BC1_xcop_bcg_cores: the BCG is already in X-COP's stars; the core miss is the halo, not the baryons

Criteria: `FROZEN_CRITERIA.md` (1180f5e8a4, committed alone, before any script or number); no amendment.
Machinery: HO1's committed script, executed read-only.

κ = ½ FITTED. Not "theory closed". Nothing here says the data favour the framework.

## Verdict (frozen): **BCG DOES NOT HELP** (canonical and alt, every variant)

| stars in the graded baryons | Δ at x = 0.1 / 0.2 / 0.3 / 0.5 / 0.7 R500 | mean / rms | class |
|---|---|---|---|
| HO1 (Ghizzardi+20 profile), Step 0 | +0.193 / +0.029 / −0.034 / −0.082 / −0.117 | −0.002 / 0.126 | FAIL (rms) |
| **PRIMARY: BCG floor, R_e 20 kpc** | +0.192 / +0.029 / −0.034 / −0.082 / −0.117 | −0.002 / 0.126 | **DOES NOT HELP** |
| BCG floor, R_e 10 / 40 kpc | unchanged | unchanged | DOES NOT HELP |
| V-ADD (BCG on top of the profile) | +0.180 / +0.026 / … | −0.006 / 0.122 | DOES NOT HELP |
| V-ICL (BCG × 2 on top) | +0.168 / +0.023 / … | −0.009 / 0.118 | DOES NOT HELP |

The alt footing gives identical numbers: above the switch, route E carries no a₀ beyond the floor.

## The audit

**2MRS BCG matches** (within 0.1 R500 of the X-COP centre and 1500 km/s): 6 of 7 clusters (A2142 has none).

**MSTAR(0.1 R500) / M★,BCG:**
- A1795 1.43; A2029 1.10; A2319 1.47; A644 2.03; ZW1215 0.96; A85 0.55;
- A2142: no 2MRS match.

**Reading.** Ghizzardi's profiles already contain at least the BCG (A85 is the exception). Even the ×2 bound for the
envelope and intracluster light moves the 0.1 R500 miss only from +0.19 to +0.17.

**The X-COP shape failure is therefore not a baryon book-keeping problem.** The CL2 picture's cluster halo is too light
in the core and too heavy in the outskirts: Burkert, Σ = η Σ_coll, with the fair-share budget out to r_ta.

The record has one rule that fixes the cores: GT1's gas-temperature core. Inside R500, its X-COP agreement holds by
construction, and its lensing grade passed 14 of 15 keys. Its R_g = 0.7 R500 variant passed all 15. That variant was
reported only, so it **cannot be promoted after the fact**. A clean test needs held-out cluster lensing.

## Checks: 4/4

- **K0:** Step 0 reproduces HO1(a) exactly.
- **K1:** the Hernquist total is correct to 2 %.
- **K2:** peak RSS 0.72 GB.
- **K3:** the stars never decrease.
- **Rerun:** byte-identical.
- **MUTATE twin** (the BCG subtracted in V-ADD): K3 fails, exit 1.
