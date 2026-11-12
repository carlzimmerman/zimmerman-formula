# PD1 AMENDMENT A1: N's cluster rule, as given by the source (committed alone, before any number under this rule)

Criteria 0dc7929421. Adopts nothing. kappa = 1/2 FITTED; not theory closed. Footings never pooled.

**Timing, disclosed.** PD1's RESULT (6bd9621320) has already landed as FAIL / FAIL, first failing gate P2 KiDS. The orchestrator
relayed this rule after that. No number under this rule has been computed.

## The rule, frozen (graded as N's halo rule at every scale; the original leftover rule becomes the bracket)

- **Budgets.** The share is as frozen (Lagrangian turnaround dust; 59.5 M_b at z 0). v_vir = sqrt(G M200 / R200), with
  M200 = M_b,sys + share and R200 at 200 rho_crit(z) (SS1's C.halo). v_stiff = 265.8 / 288.1 km/s.
- **Core.** If v_vir > v_stiff, a fraction f_core = (1/2)[1 - (v_stiff / v_vir)^2] of the share sits in an NFW core: Duffy 2008
  c200 at M200, truncated at R200. Otherwise f_core = 0.
- **Phantom-locked part.**
  - M_ph(<r) = W_vir M_b(<r) [nu(g_N,b / a0) - 1].
  - W_vir = S^2 / (S^2 + c_s,IGM^2), with S^2 = sigma_3D^2 = (3/2) v_vir^2 (SIS) and c_s,IGM = 15 km/s (T 1e4 K, mu 0.6, adiabatic).
  - The phantom is capped by the extended budget E = (1 - f_core) share: truncated at R_trunc where the phantom reaches E (the
    spherical formula on M_b,sys).
- **Remainder.** If the phantom inside R_ms uses less than E, the remainder E - M_ph(<R_ms) sits in an isothermal profile out to
  R_ms, as frozen in the criteria. The source's "rest in the phantom / extended part" does not define its shape.
- **Gravity.** The core and the remainder are Newtonian; no nu acts on them.

**Gates rerun under A1** (the label is recomputed in the frozen order): P2 KiDS, P2 SPARC, P3 groups, P3 X-COP, P5 Bullet. The
Bullet's core and remainder inside R200 are galaxy-traced; the phantom part is DB1's law row. P1 and P4 are unchanged (the total
dust is unchanged).

**Reported.**
- Per system: v_vir, f_core, W_vir, and the core, phantom and remainder masses.
- X-COP: f_miss = dark / M_dyn per bin vs TR1 0.71 / 0.66 / 0.58 / 0.46 / 0.32. The source claims about 0.71 inside 0.25 R500 and
  TR1's falling profile.
- The TR1 SHAPE (per-bin dark/M_dyn minus its mean) against TR1's.

**Statement (no number).** Whether the virial-equipartition argument between the Pi^2 dust term and the gradient term gives
f_core = (1/2)[1 - (v_stiff / v_vir)^2]. The 1/2 and the square are recorded as form choices.
