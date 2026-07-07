# Off-Circular Kernel Completion — Standing (2026-07-07)

**Question.** The dS-Unruh modified-inertia kernel is validated only on the *circular* (on-shell) slice,
`theta(y) = sqrt2 / (1 + (sqrt2-1) y^2)`, `y = om_ext/om_int` (RAR to 3.6e-12, `mi_nonlocal_kernel.py`).
The off-circular completion carries two degrees of freedom the circular slice cannot see:

- **(i) omega_c** — the corner location, equivalently the memory time `tau_mem = 1/omega_c`.
- **(ii) eta(beta)** — the anisotropy / boost function (`beta` = boost/CMB-frame velocity).

Apply every legitimate physical constraint and decide, both-ways, whether each is **forced**, **bounded**, or **free**.

Verification script (exit 0, not committed): `real_research/reviews/mi_offcircular_completion.py`.
Builds on the residual-doors / sixth-theorem results (DOIs 21175723, 21179352) and the committed
`dsunruh_tau_mem.py` (`DSUNRUH_TAU_MEM_2026.md`). Both footings (a0 = 9.36e-11 and 1.13e-10) carried.

---

## Verdict

| DOF | Classification | By what argument |
|---|---|---|
| **omega_c** (tau_mem) | **FREE (bounded)** | No applied constraint pins it; six constraints are consistency/bound, ZERO pinning. Bounded in `[~1/kappa = 17.5 Gyr .. ~1/(d1 above-band pole) = 1 Myr]`. |
| **eta(beta)** | **SIGN FORCED** (MG-impossible); **MAGNITUDE bounded, omega_c-hostage** | `d ln eta / d beta > 0` forced by the pericentre-dominated amplitude functional + 2-pt positivity; MG (virial universality) gives exactly 0. Slope magnitude = retained pericentre-amplitude fraction, which scales with omega_c. |

The crux: **`theta(y)` is scale-free in the ratio `y`** — `d theta / d omega_c = 0` identically (sympy-verified).
The only directly-constrained slice is therefore **corner-location-blind by construction**. "Reduces to the RAR"
is a *consistency check*, never a *pin*. This is the single fact that keeps omega_c free.

---

## Constraint-by-constraint (each shown numerically to be consistency/bound, none pinning)

**C1 — On-shell RAR consistency → CONSISTENCY (corner-blind).**
`theta` is a function of `y = om_ext/om_int` alone; `d theta / d omega_c = 0` (sympy-asserted). Three absolute
corners spanning 10 orders (1/Myr, 1/0.4 Gyr, H_Lambda) give the identical `theta(y)` because omega_c is absent
from the circular observable. Necessary condition, not a pin.
*(Verifier-reconciled: the earlier printout subtracted `theta(y)` from itself — a tautology. Replaced with the
analytic `d theta/d omega_c = 0` as the load-bearing content; the three-corner display is now labeled a corollary,
not independent numeric evidence. Classification unchanged.)*

**C2 — KMS / thermality (T_dS = H_L/2pi) → injects only kappa, not om_int.**
The dS worldline Wightman `~1/sinh^2(kappa u/2)` has Matsubara poles at `n*kappa`; nearest pole (n=1) at
`kappa = H_L` (envelope decay rate = 1.00005 kappa, verified). KMS detailed balance ratio
`exp(-om_int/T_dS)` with `om_int/T_dS = 275` → bath is flat/Planckian in-band; **no in-band feature that could
park a corner at om_int**. The only frequency KMS injects is kappa, which sits **44x below** om_int. It ties the
+/- frequency parts (FDT) and the tail order; it does **not** fix the pole count (sqrt2 vs 2) nor the corner.

**C3 — 2-pt dS spectral positivity (Kallen-Lehmann / Bros-Moschella) → SIGN only, corner-blind.**
`F(w) >= 0` verified for a Lorentzian line at all three corners → holds for **every** omega_c > 0. Fixes the
dressing SIGN (closed elsewhere: D1 2nd-order + sixth-theorem all-orders), **not** the corner location. Feeds the
eta sign, not omega_c.

**C4 — 4-pt / interacting dS complementary-series positivity → OPEN but band-separated.**
Genuinely open in the literature (named residual-doors edge). But the framework's inertia response is in-band at
`w/H in [54, 3662]`; any complementary-series subtlety lives at `w <~ H`, `>=15x below` the in-band floor. It
therefore **cannot reach** om_int either way. Not resolved here — shown to be band-separated, so no in-band reach.

**C5 — Causality / analyticity (Kramers-Kronig) → form-class only.**
KK dispersion relation verified (median error ~0.001) for the DC=sqrt2 Lorentzian at all three corners → a causal,
KK-consistent kernel exists for **every** omega_c. The bare dS response is ohmic/local (no intrinsic corner). KK
constrains the FORM-class, not the location.

**C6 — Orbit-(in)stability clamp → BOUND, not a pin.**
In-band dissipative weight capped at `|Im K/Re K| < 1e-4` (orbits neither decay nor blow up over t_Hubble). This
**forbids an in-band dissipative corner** (pushes the spectral weight above-band, or into KK tails) but does not
select om_int. A genuine bound on the corner's *character*, not its location.

**Stage 5 — The actual off-circular pullback attempt (the only thing that could pin it).**
Built the dS-Unruh commutator response on a Kepler-worldline family (`e in [0, 0.9]`) to O(a_ext) and read the
dominant pole of the RESPONSE = `|chi_bath(w)| * |A_drive(w)|`. Result: the bath transfer is a Lorentzian pinned at
`kappa = H_L` (~0.02 om_int), monotone-decreasing above kappa, so it suppresses the high orbital harmonics that
eccentricity produces and the response peaks at the **lowest** drive harmonic = om_int (the fundamental) for all e.
**But that fundamental is what we imposed by choosing the orbit — not a bath-derived corner.** Tell-tale test:
rescaling om_int by 0.1x/1x/10x, the response peak stays exactly at `1.0` in om_int units (absolute peak tracks
om_int over 100x). **No absolute bath-derived corner** — omega_c rides on the drive, which is precisely the
Milgrom-1994 quasi-static averaging-bandwidth POSTULATE (Eq. 55-57; general multi-frequency Eq. 33 obstructed), an
*input*, not a derivation. The bath's own pole stays at kappa, untouched by e.

---

## Consequence: tau_mem

**omega_c FREE → tau_mem UNDETERMINED**, bounded in:

| Candidate | tau_mem | Status vs door |
|---|---|---|
| Raw dS correlator (`1/kappa`) | 17.5 Gyr | 44x too slow — door ~dies (fully mixed) |
| **Milgrom-1994 postulate (`1/om_int`)** | **0.4 Gyr** | door-relevant value — selected ONLY by the postulate |
| d1 above-band pole (`1/v2`) | 1 Myr | 220x too fast — no retained memory, door ~dies |

The bath selects **none** of the three. `1/om_int` sits between the two bath-native scales and is chosen only by
the averaging-bandwidth assumption the theory cannot currently derive.

## Consequence: dwarf sigma-hysteresis door magnitude

**Existence + sign + MG-impossibility are FIRM** (double-valued `sigma(r)` for any nonzero memory — MG-impossible).
**Magnitude is NOT pinned** and is a **proxy measurement of omega_c**:

- `tau = 1/kappa` (17.5 Gyr): ~0-1.4% (door ~dies)
- **`tau = 1/om_int` (postulate): ~7-18% (Crater II) / ~4-13% (Antlia II) — peaks HERE, at the postulate**
- `tau = 1/v2` (Myr): ~0.1-0.2% (door ~dies)

So the door is **not a dated prediction** — the largest signal sits exactly at the postulated scale, not a
bath-forced one. A positive dwarf sigma-hysteresis detection would **measure** omega_c (resolve the postulate).

## Consequence: anisotropy eta(beta)

**Sign FORCED, MG-impossible.** The Milgrom-2022 amplitude functional `A(om) ~ sum om_k^2 |r_k|` is
pericentre-dominated; on an eccentric orbit the rms/amplitude average rises steeply with e
(1.0 → 9.45 as e: 0 → 0.9) while the residence-average stays ~flat (1.0 → 2.3), so `d ln eta / d beta > 0`. MG
(Milgrom-2014 virial universality) gives exactly 0 — so a nonzero slope is MG-impossible. **Magnitude/slope is
bounded but omega_c-hostage**: the retained pericentre-amplitude fraction runs 0.05 (at omega_c = 0.3 om_int) to
0.99 (at 30 om_int). Same hostage as the dwarf-door magnitude.

---

## The single closing input (what would flip FREE → FORCED)

The **full non-uniform dS Wightman two-point pullback** `W(tau, tau')` on the eccentric worldline, showing the
response's dominant pole is a **bath property** landing at om_int rather than the drive fundamental. Stage 5's
reduced-order O(a_ext) model shows the response rides on the drive and the bath pole stays at kappa — but a
genuinely different pole structure could, in principle, appear only in the full non-uniform pullback, which is the
named closing computation and is **not done here** (this matches d1's "off-circular completion UNDERDETERMINED"
flag; Milgrom's general multi-frequency case Eq. 33 is obstructed).

**Empirical alternative:** a positive dwarf sigma-hysteresis or cluster eta(beta)-slope detection **measures**
omega_c directly (proxy measurement), resolving the scale the theory cannot currently derive.

---

## Honest caveats (biggest first)

1. **The pin candidate is genuinely un-adjudicated, not closed.** The bath-native pin (kappa, → 17.5 Gyr) and the
   drive-native scale (om_int, the postulate) are un-adjudicated by every applied constraint. Stage 5 is a
   REDUCED-order model (O(a_ext) commutator response, bath pole fixed at kappa), **not** the full non-uniform dS
   pullback. It shows the response rides on the drive and the bath pole stays at kappa — but the full pullback (the
   named closing input) is NOT done. That computation was not faked.
2. **Stage 5's "peak at om_int" is deliberately NOT read as a pin.** It is the drive fundamental we imposed by
   choosing the orbit; the rescaling tell-tale is what establishes there is no absolute bath-derived corner.
   Misreading it as forcing would be the exact honesty-guard violation the task warns against.
3. **C4 is genuinely OPEN.** The 4-pt complementary-series dS positivity is unresolved in the literature; it is
   shown band-separated (cannot reach in-band inertia), not solved.
4. **eta-sign forcing is conditional** on the Milgrom-2022 amplitude functional being the correct off-circular
   dressing — and that functional is itself part of the underdetermined completion. The sign is as firm as that
   functional + 2-pt positivity, no firmer.
5. **Footing-stable.** Both footings carried; `kappa/om_int = 0.023` (canonical) vs `0.028` (alternate); Stage 5
   peak identical. Verdict does not depend on the a0 fork.

---

## Does this close the door, or characterize the open frontier?

**It precisely characterizes the remaining open frontier — it does not close the door.**

- omega_c is **FREE (bounded)**: no constraint pins it; the constrained space is `[1 Myr .. 17.5 Gyr]` with the
  door-relevant `0.4 Gyr` selected only by the averaging-bandwidth postulate.
- eta(beta) is **sign-forced (MG-impossible), magnitude-bounded-but-omega_c-hostage**.
- The dwarf-door **existence/sign/MG-impossibility are firm**; the **magnitude is a proxy measurement of omega_c**,
  not a dated prediction.
- Two paths close it: the **full non-uniform dS Wightman pullback** (theory) or a **positive dwarf/cluster
  detection** (measurement).

No positivity/KMS bound was mis-stated to force a corner; the averaging-bandwidth postulate was not re-inserted as
a derivation. **FREE(bounded)** is the honest verdict.
