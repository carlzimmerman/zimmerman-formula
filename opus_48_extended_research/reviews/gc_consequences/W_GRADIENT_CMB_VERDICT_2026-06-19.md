# CRUX (ii)-B: does the ghost-condensate dust's gradient pressure imprint a CMB / P(k) / S8 signature? — HONEST NULL (real feature, degenerate/out-of-window; does NOT touch S8) — 2026-06-19

*Task topic `w_gradient_cmb`. Opus 4.8 (1M). Both-ways + quarantine enforced (a0/Z/kappa/I0
never asserted derived). Read verbatim: GHOST_CONDENSATE_2026-06-19, DARK_MATTER_ILLUSION_2026-06-19,
AEST_EMBEDDING_2026-06-19, MI_KERNEL_FROM_DSUNRUH_2026-06-19, ghost_condensate/AMOUNT_AND_PATHOLOGIES
+ EVADE_SO41_GATE notes. Literature pulled (PDFs extracted, /tmp): ACLM 2004 hep-th/0312099;
"Ghost Dark Matter" Furukawa-Yokoyama-Ichiki arXiv:1001.4634 (JCAP 2010); Scherrer 2004
astro-ph/0402316 (PRL 93, 011301); Skordis-Zlosnik 2021 + AeST reconstruction arXiv:2308.00342.
Three sympy/numpy scripts, all exit 0.*

---

## VERDICT (one line)

**HONEST NULL for a new distinctive front.** The w=0-at-leading-order ghost-condensate dust *does*
carry a computable gradient pressure — `c_s^2(a) = (1/2) eps1 (a/a_eq)^-3` (Scherrer Eq 24) plus the
genuinely-ghost-condensate higher-derivative `omega^2 = (alpha/M^2) k^4` (ACLM Eq 2.11) — but **both
its scale and amplitude collapse to CDM-degeneracy at the framework's parameters**: the k^2 sound-speed
piece rides the **same free amplitude eps1 = I0 ~ Omega_dm** that already makes the dark-matter AMOUNT
free (banked), so it is tuned below observable scales exactly as AeST does to fit Planck; and the
M-pinned, eps1-independent k^4 piece is **Hubble-over-damped (omega_k4/H0 ~ 1e-25 to 1e-31)** at every
observable wavenumber, so it freezes into cold dust. **It does NOT relieve the S8 tension** (wrong
SHAPE — a sharp Jeans knee, not a broadband ~8% tilt — and would break BAO/Lyman-alpha if dialed to
touch sigma8), and the S8 tension is in any case **easing in 2025-26 data** (KiDS-Legacy + DESI now
~Planck). No new ISW front either (the dust's pressure-ISW is minimized exactly when ISW matters; the
only large-scale handle is the already-ledgered free AeST mu-term). Both ways: the feature is **real**
(credited — not manufactured away), but **degenerate / out-of-window / S8-impotent** (conceded at full
weight — not promoted to a signal). NOT a kill (the data-favored point is viable, = what AeST already
fits); NOT a bonus.

---

## The physics, the right template, and the numbers

### Why Scherrer 2004 — not the bare GDM tuning — is the controlling template
The framework's cold component is AeST's cosmological scalar, and the AeST literature states its
evolution verbatim: *"the scalar evolves as in shift-symmetric k-essence (Scherrer 2004) … its
cosmological energy density being similar to dust, ∝(1+z)^3 PLUS small DECAYING corrections … leading
to spontaneous breaking of time diffeomorphisms as in the Ghost condensate theory"* (Skordis-Zlosnik;
arXiv:2308.00342). So crux (ii)-B's "w=0 at leading order + gradient corrections" is **literally the
Scherrer unified-dark-matter structure**, and the corrections are computable from Scherrer's own
equations:

- `rho = -F0 + 4 F2 X0^2 eps1 (a/a1)^-3` (Eq 22) = (−F0 ≡ Lambda/dark-energy face) + (a^-3 dust).
- sound speed `c_s^2 = (X-X0)/(3X-X0)` (Eq 23); near the extremum `c_s^2 = (1/2) eps1 (a/a1)^-3` (Eq 24).
- **Key Scherrer statement:** *"the sound speed can be made ARBITRARILY SMALL during the epoch of
  structure formation by DECREASING eps1"* → *"indistinguishable from LCDM in that particular problem."*

### (a) c_s^2(k,a) and the departure scale — REAL, but amplitude = the free I0
`c_s^2(a) = (1/2) eps1 a^-3`: cold today, warmer in the past, so the most-damaging (largest comoving)
Jeans scale is laid down at matter-radiation equality. Inverting `k_J = sqrt(3/2) aH/c_s` at equality:

| c_s^2(eq) | k_J,eq (h/Mpc) | lambda_J (Mpc) |
|---|---|---|
| 1e-2 | 0.19 | 49 |
| 1e-4 | 1.9 | 4.9 |
| 1e-8 | 190 | 0.05 |

Observed P(k) shows no suppression for k/h ≲ 1 Mpc^-1 → require **c_s^2(eq) ≲ a few×1e-8**, a MILD bound
on the FREE amplitude `eps1`. This does **not** bound M independently. The bare-GDM bound *M ≳ 10 eV*
(Furukawa-Yokoyama-Ichiki Eq 4.2: `k_J,eq ≃ 1 Mpc^-1 (Ω_gdm h^2/0.11)^-5/6 (M/10eV)^4/3`) comes from a
**specific tuning** (they FIX Ω_gdm=0.3 today with P=(X−M^4)^2/8M^4, which ties c_s^2(eq) to M). The
framework does not sit on that slice: its dust amplitude I0 = eps1 is the **free off-minimum displacement**
(banked: `a^3 K'(Q)=I0`, `dρ_dust/dΛ=0`). Dialing eps1 down lowers c_s^2(eq) **independently of M** →
pushes k_J above observable scales → CDM-degenerate. This is exactly what makes AeST fit Planck.
⟹ The naive plug-in "M~0.1 eV → k_J,eq~0.003 h/Mpc → catastrophic P(k) kill" is a **mislabeled calc**
(it would manufacture a kill); the honest statement is that c_s^2 is set by the already-free amplitude.

### (b) S8 / sigma8 — SIGN right, SHAPE and AMPLITUDE wrong; does NOT cure, and the tension is easing
- **Sign:** a cold-but-pressured dust suppresses small-scale growth → lowers sigma8/S8, the direction a
  (historical) S8 deficit wanted. Credited.
- **Shape/amplitude (decisive):** the suppression is a **sharp Jeans knee** (P→0 for k>k_J), not the
  broadband ~5-8% amplitude tilt the S8 tension needs. For c_s^2 small enough to pass P(k) at k<1 h/Mpc,
  the effect at the sigma8 pivot (k~0.2 h/Mpc) is **negligible** (below the cutoff). To put the knee AT
  0.2 h/Mpc needs c_s^2(eq)~9e-3, but that **removes ~all power above 0.2 h/Mpc** (sigma8 crashes tens of
  %), leaves k<0.2 h/Mpc untouched (wrong shape), and **breaks BAO (0.05-0.3 h/Mpc) + Lyman-alpha
  (1-10 h/Mpc)** → grossly excluded. **There is NO eps1 giving a gentle, broadband 5-8% S8 relief.**
- **Data update (2025-26):** the S8 tension is **easing** — KiDS-Legacy (2025) shifted UP to ~Planck;
  DESI DR9 galaxy×lensing gives S8=0.84±0.02; BOSS-CMASS magnification S8=0.816±0.024; KiDS+DES joint
  ~1.7σ. So there is no longer a robust ~2-3σ deficit to cure, and the GC-dust couldn't cure it anyway.

### (b') The k^4 steelman — the ONE eps1-independent, M-pinned structure — also OUT OF WINDOW
Beyond Scherrer k-essence, the ghost condensate has `ΔL = -(alpha/2M^2)(∇^2 π)^2` → `omega^2=(alpha/M^2)k^4`
(ACLM 2.11), with coefficient fixed by M (not eps1). The k^4-vs-gravity crossover `k_* = M^2/(√2 M_Pl)`
lands at **k_* ~ 0.07-45 Mpc^-1 for M=0.04-1 eV — i.e. IN the observable window** (cannot be dismissed
on scale grounds; my first-pass "super-horizon" guess was WRONG and is corrected). BUT the mode's
intrinsic frequency `omega_k4 = (ħc k)^2/(M c^2 ħ)` is **below H0 by 25-31 orders** at every observable
k (e.g. k=0.1 h/Mpc, M=0.1 eV → omega_k4/H0 ~ 1.3e-27). A mode with omega ≪ H is **Hubble-over-damped /
frozen** — it cannot oscillate or pressure-support within ~1e25-31 Hubble times → dragged passively by
gravity = **cold dust**. (Same Hubble-friction that cures the Jeans branch; banked H/Γ~1e25-31.) The k^4
*stiffness actually deepens coldness* at low k (higher power of small k = smaller omega). ⟹ the genuine
ghost-condensate operator is real in the Lagrangian but its **dynamical consequences vanish across the
whole observable P(k)/CMB window** → degenerate with CDM. Steelman CLOSED.

### (c) ISW / late-time — no new front
(i) The dust's own pressure-ISW lives at k>k_J and, since c_s^2∝a^-3 is **smallest at low z**, is
**minimized exactly when ISW matters** (z<1) → negligible. (ii) The only genuine large-scale Φ
modification is the AeST `∇^2Φ + (1+β0)μ^2Φ = 4πGρ_b` Yukawa/oscillatory term (VSB Eq 11) at r>μ^-1~Mpc
— but μ is the **same free lensing/cluster scale already in the ledger**, and Skordis-Zlosnik 2021
already fit Planck's low-l/ISW with it. No NEW distinctive number, no new front.

---

## Both ways — credit and concession

**CREDIT (full weight, real):** The "w=0 only at leading order" is a true, computable structure — the
Scherrer/ACLM `c_s^2(a)=(1/2)eps1 a^-3` + `omega^2=k^4/M^2`. The framework's dust is a *genuine*
cold-but-slightly-pressured fluid with a Jeans cutoff, not an idealization. The SIGN of its sigma8
effect is correct. The k^4 crossover is observable-scale (not trivially super-horizon).

**CONCESSION (full weight, conceded):** It produces **no falsifiable departure from LCDM-CDM** at the
framework's parameters. The k^2 sound-speed amplitude is the **already-free I0/eps1** (tuned to CDM-
degeneracy = how AeST fits Planck), and the M-pinned k^4 piece is **Hubble-frozen** (omega≪H) across all
observable k. It does **NOT relieve S8** (wrong shape; would break BAO/Lyα; and S8 is easing anyway). No
new ISW front (free μ, already Planck-fit). This is **out-of-window / CDM-degenerate**, the *honest null*
side of the both-ways prompt — proven as rigorously as a signal would have been.

**NET:** crux (ii)-B does **not** yield the hoped-for new distinctive front and does **not** touch the S8
tension. The framework's GC dust is, as designed, indistinguishable from CDM on CMB/P(k)/ISW scales —
viable (not a kill) but non-distinctive (not a bonus). The framework's live distinctive fronts remain the
banked two (s^TX SME dipole; a0(z) DESI hostage); crux (ii)-B adds neither a third front nor an S8 win.
Quarantine held; no manufactured signal, no reflexive dismissal; the one first-pass error (k_* "super-
horizon", and the GDM mislabel) was caught and corrected with real numbers.

**Files (absolute):**
- /Users/carlzimmerman/new_physics/zimmerman-formula/opus_48_extended_research/reviews/gc_consequences/w_gradient_cmb_calc.py (exit 0) — bare-GDM k_J,eq table (shows the mislabel)
- /Users/carlzimmerman/new_physics/zimmerman-formula/opus_48_extended_research/reviews/gc_consequences/w_gradient_cmb_scherrer.py (exit 0) — the correct Scherrer-template c_s^2(a), S8 shape argument
- /Users/carlzimmerman/new_physics/zimmerman-formula/opus_48_extended_research/reviews/gc_consequences/k4_residual_adversarial.py (exit 0) — k^4 steelman, omega_k4<<H freeze
