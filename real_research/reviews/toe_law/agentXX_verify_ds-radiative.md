# agentXX VERIFY — hostile referee of the dS-RADIATIVE c_chi(H) lock route

*Verifier pass, 2026-06-13. Independently re-derived every load-bearing number and the
physics logic. Question: is the claimed c_chi<->H lock genuinely FORCED, or is c_chi a free
Lagrangian coupling tuned to land the edge coincidence and relabelled "locked"? The route
itself returned FREE-PARAMETER; my job is to check it didn't bury a hidden lock OR overstate
the kill. Coefficient quarantine held: q=1/4, Z, the coefficient never asserted.*

---

## VERDICT: route CONFIRMED. FREE-PARAMETER stands.

The route's own verdict is FREE-PARAMETER / FREE-MUST-TUNE, and it is correct. There is no
claimed lock to overturn here — the route did NOT claim SCALE-LOCK-FORCED, it honestly
reported no lock. My independent recomputation reproduces all load-bearing numbers exactly,
the symbolic spin-0 sound speed is genuinely scale-free, and the dS correction at the
relevant scale is negligible by 60+ decades. c_chi must be TUNED to land the edge coincidence.

This is the rare case where the central referee question ("forced or tuned?") is answered the
honest way by the route itself: **tuned**. My pass confirms it and finds no smuggle in either
direction (no buried lock, no manufactured kill).

---

## [1] Recomputation — all 5 load-bearing numbers MATCH (independent, mp.dps=50)

| quantity | route | my recompute | status |
|---|---|---|---|
| H0 in energy = hbar*H0 | 1.448e-42 GeV | 1.448e-42 GeV | MATCH |
| (H/M)^2 at M=meV (SC floor) | 2.097e-60 | 2.097e-60 | MATCH |
| (H/M)^2 at M=M_Pl | 3.536e-121 | 3.536e-121 | MATCH |
| M needed for O(1) lock | 3.464*H0 (~3.5H) | 5.016e-42 GeV = 3.464*H0 | MATCH |
| log10(M_SC/H) | 29.84 | 29.84 | MATCH |
| IR (H/k)^2 at fold band | 8.264e-11 | 8.26446e-11 = 1/(1.1e5)^2 | MATCH |
| GH thermal (T_dS/M)^2 at meV | 5.311e-62 | 5.311e-62 = (1/2pi)^2*(H/M)^2 | MATCH |

Recompute: `/tmp/verify_xx.py`. Every number reproduces to the quoted precision.

## [2] Symbolic check — the spin-0 speed is genuinely a scale-free coupling ratio

I re-entered the standard Einstein-aether spin-0 (khronon) squared speed
> c_chi^2 = c123 (2 - c14) / [ c14 (1 - c13)(2 + c13 + 3 c2) ]
and confirmed via sympy that its free symbols are **{c1,c2,c3,c4} only** — no H, no M, no
k, no curvature scale appears. This is the structural heart of the verdict: the bare sound
speed is dimensionless and set entirely by the (free, marginal) Lagrangian couplings. There
is nothing for H to determine at tree level. CONFIRMED. (`/tmp/verify_xx2.py`)

## [3] Spin-0 / spin-2 independence — the GW170817 bound does NOT secretly fix c_chi

A natural worry: maybe c_T^2=1 (GW170817) plus some relation pins c_chi too, giving a hidden
lock the route missed. Checked directly: c_T^2 = 1/(1-c13) is fixed by c13->0, but c_chi^2 at
c13=0 is `-c2(c1+c4-2)/[(c1+c4)(3c2+2)]` — still free in (c1,c2,c4). The tensor-speed bound
does NOT pin the scalar speed. The route's claim that c_chi is a SEPARATE combination is
correct. So no hidden symmetry lock smuggled in through GW170817. CONFIRMED.

## [4] The T-odd argument (the only place a real enhancement could have lived) is correct

The route's strongest-shot for the framework was the linear-in-K operator (K/M)(del chi)^2,
which would give delta c_chi^2 ~ 3H/M (ONE power of H/M, ~1e-30 at meV — still dead, but far
larger than (H/M)^2). The route forbids it because K = nabla.u is T-ODD (one u-derivative,
flips under u->-u) while (del chi)^2 is T-EVEN, so the product is T-odd and not generated in
the T-invariant khronon action. I confirm the parity bookkeeping: K carries a single factor
of u (odd), the gradient term is built from chi-derivatives (even). The argument is sound.
Even if one (wrongly) allowed it, 3H/M ~ 1e-30 at the meV floor — still negligible. So the
route gave the lock its best shot and it failed honestly, not by omission.

## [5] Did the route bury any path to a lock? — the three failure modes, checked

A hostile referee must ask: is FREE-PARAMETER the manufactured-kill of a real lock?
I checked the three ways a dS lock could have been real and the route's handling of each:

- **IR correction (H/k)^2.** Real, but rides 1/k^2 and is ~8e-11 at the fold band (sub-horizon).
  Vanishes as k->inf. Correctly sized; not a lock (it's k-dependent, not a fixing of c_chi).
- **UV/radiative (R/M^2) insertion.** ~(H/M)^2, dead by >=60 decades for any M>=meV. The
  controlling scale M is the khronon LV scale, bounded BELOW by the strong-coupling floor
  M_SC>~meV (banked from agentU_khronon_m22.md / 1711.08845 Eq.15 — I verified the floor is
  in the banked reference, line 125-126). Correctly sized.
- **Symmetry lock.** Even if a symmetry pinned c_chi, it would pin it to a CONSTANT, not to
  f(H). The route's point (C) is the decisive one for the *physics*: this residual needs an
  H-DEPENDENT lock (so R(H) tracks G_sat(H)); a constant lock leaves R(H) sliding against
  G_sat(const) and the coincidence still fails. This is correct and is the real reason the
  route is honest: it does not even let a symmetry-to-constant masquerade as a fix.

So the route did not bury a lock. Each candidate is the wrong KIND (k-dependent, M-suppressed,
or constant) to tie the H-intrinsic R to the c_chi-intrinsic G_sat.

## [6] The central referee question — forced or tuned?

**TUNED.** c_chi^2 enters as the Cherenkov-corner value [1.000,1.033] banked FREE by agentU.
Landing the edge coincidence R=G_sat requires choosing c_chi by hand in that window. The dS
background supplies only an (H/M)^2 lever with M>=meV ~ 10^29.8 H — 30 decades too weak to
convert "free coupling" into "H-determined." The structural decoupling (R is set by the dS
scale H / GH modular structure; c_chi/G_sat is set by the khronon LV scale M>=meV) is the
recurring residual, and this route QUANTIFIES it at >=30 decades rather than resolving it.

No fixed point is claimed by this route (it explicitly defers the dynamical/attractor question
to ROUTE 2), so referee point (3) — does a fixed point help or hurt — does not bite here; the
route is honest that a constant-valued lock (the only thing a symmetry would give) would NOT
help. That is the correct hurt-not-help reading: driving c_chi to a fixed CONSTANT (e.g. ->1
luminal) decouples the sonic edge from H rather than tying it. The route states this.

## [7] Smuggle check — both directions clean

- No buried lock: every candidate mechanism is named and sized; none is the H-dependent lock
  the residual needs.
- No manufactured kill: the route gave the framework-favorable outcome (a lock) its strongest
  shot (linear-K enhancement, GH-thermal) and it failed on the merits, not by dismissal. The
  (H/M)^2 suppression is convention-robust across M in [meV, M_Pl] — there is no choice of M
  consistent with the EFT that produces a lock.
- Coefficient quarantine held: nothing here asserts q=1/4, Z, or the coefficient.

---

## REGRADE

- **recompute_agrees:** yes (all 7 load-bearing numbers + symbolic scale-freeness reproduce).
- **forced_or_tuned:** TUNED — c_chi is a free Lagrangian coupling ratio (Cherenkov corner,
  banked free), with the only H-dependence being delta c_chi^2 ~ (H/M)^2, M>=meV, ~10^-60.
- **regrade:** CONFIRMED (the route's FREE-PARAMETER verdict stands; not a relabelled lock).
- **regraded_verdict:** FREE-PARAMETER.
- **one-line:** dS curvature gives c_chi only an (H/M)^2 correction with M (the khronon LV
  scale) >= meV ~ 10^29.8 H, so the lever is 30+ decades too weak; c_chi stays a free
  Cherenkov-corner coupling that must be TUNED to land the edge coincidence — NO H-lock.
