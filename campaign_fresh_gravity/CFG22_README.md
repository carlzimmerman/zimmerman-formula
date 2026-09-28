# CFG22 — a soft edge: can one phantom shape satisfy KiDS and the Local Group?

Script: `CFG22_soft_edge.py`, about 3 min.
- Outputs: `.out` and `_results.json`.
- MUTATE control: `_MUTATE.out` and `_MUTATE_results.json`. With the tail off, the sharp edge comes back and H0 fails (rc = 1).
- The main run exits 1, because H0 and H1 failed.

## The change

The law's phantom (ρ ∝ r⁻²) runs inside r_s = x_s r_ta. Beyond r_s it continues as ρ = ρ_s (r_s/r)³, continuous at r_s with no new amplitude, out to r_ta. Beyond r_ta the enclosed mass is constant.

It is scored exactly as CFG21:
- **KiDS:** CFG16's machinery, with the self-consistent 2-halo caps taken from the soft profile's own turnaround mass;
- **LG:** CFG20's integrator, with r_s(t) and the tail following r_ta(t);
- **Tension:** T = [χ²_KiDS − min] + χ²_LG.

## Results

**C1 (control):** with the tail off, the lane reproduces CFG21's sharp-edge KiDS best (0.62, −35.114) and CFG20's R₀ at 0.2 / 0.34 exactly.

| row | KiDS best x_s | LG best x_s | joint x_s | T_min (soft) | T_min (sharp, CFG21) |
|---|---|---|---|---|---|
| canonical P2, LG 1.145e11 | 0.40 | 0.04 | 0.26 | 29.8 (5.5σ) | 26.2 |
| canonical ν_mono, LG 1.145e11 | 0.42 | 0.03 | 0.26 | 30.8 (5.6σ) | 27.8 |
| canonical, LG 1.72e11 | 0.40–0.42 | 0.02–0.03 | 0.24 | 44.7 / 45.9 | 41.0 / 42.7 |
| alt, both LG masses | 0.38–0.40 | 0.02–0.03 | 0.24–0.26 | 35.2–54.0 | 31.9–50.6 |

- **H0** (the tail lowers T_min by more than 3): **FAILED**. It raises T_min by 3–4.
- **H1** (T_min ≤ 9): **FAILED**.

## Standing

**The soft edge makes the conflict worse.**
- The tail supplies KiDS's large-radius signal, so KiDS settles for a shorter core.
- The tail also piles mass inside the LG's zero-velocity radius, and the LG's r_ta in the law's convention is 2.1–2.4 Mpc, far outside its observed R₀.

**The lesson: the LG caps the TOTAL mass within about 1 Mpc of the MW+M31 pair near 3 × 10¹² M☉.** Any profile that puts the law's phantom mass out to KiDS's radii overloads it, unless the large-radius KiDS signal comes from the lens's surroundings, not its own phantom.

That points at the 2-halo term. It is modelled here, as in CFG4, CFG15 and CFG16, with the **linear** matter correlation.

Nothing here says the theory is closed.
