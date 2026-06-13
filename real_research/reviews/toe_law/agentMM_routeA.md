# agentMM ROUTE A — the pumped-khronon pullback on the Deser-Levin b-family; the b->c_chi edge

**STATUS: IN PROGRESS (compute-first, written incrementally). Route A = DIRECT CONTINUATION.**

Date: 2026-06-12.

## Charter (Route A)

Take the pumped khronon mode equation (HH [1a] universal scale-invariant pump ODE), build its
Wightman/pullback on the Deser-Levin b-family (EE [2c]: W_b, kappa^2=a^2+H^2, b=a/kappa), and extract
the EDGE behavior as b -> c_chi. Does an essential singularity emerge, of what root order? Do NOT assume
q=1/4. Let the pump dynamics produce whatever class it produces; compare to q=1/4 only at the very end.
If the bulk pump (HH's scale-invariant g) gives only the transcription (no genuine edge essential
singularity), say so — that would CONFIRM the edge is FREE input.

## The two banked inputs (verbatim structure)

**HH [1a] — the pump ODE (a function of w = k_phys/H ONLY; carries NO b-index):**
> g'' - 2 ghat(w) g' + c^2 (1 + f(w)) g = 0,  w = k_phys/H,  ghat>0 physical-time gain.
> Hermitian form (g = e^{Ghat} psi, Ghat'=ghat): psi'' + Omega^2 psi = 0,
> Omega^2 = c^2(1+f) + ghat' - ghat^2.
> The response (worldline soft channel) reads the CAUCHY PROPAGATOR (commutator) of this ODE —
> Bogoliubov/normalization invariant. c == c_chi here (the khronon sound speed).

**EE [2c] / STEP 2 — the two-variable representation + the b-family pullback:**
> W(eta,eta',r) = (1/2pi^2) \int_0^inf (dk/k) j0(kr) Psi(k eta, k eta'),  Psi = phi(w1) conj-phi(w2),
> free phi(w) = w e^{i c w}, w = k|eta|.
> On the Deser-Levin orbit (offset x=b eta, velocity b rel. khronon frame): a = b kappa,
> kappa = H/sqrt(1-b^2), kappa^2 = a^2 + H^2, b = a/kappa.
> FREE pullback:
>   W_b(tau) = -H^2 / [16 pi^2 c_chi (c_chi^2 - b^2) sinh^2(kappa tau/2)],  KMS at kappa/2pi,
>   amplitude A(b) = H^2/(16 pi^2 c_chi (c_chi^2 - b^2)).

**The structural fact to confront head-on (the firewall's central point):** the pump ODE lives on label
w (mode/scale); the b-family lives on label b (worldline). They are DISJOINT in the banked dynamics.
The question is whether the *pullback construction itself* (the dk/k integral with the j0(kr) factor
evaluated on the b-orbit) develops an edge singularity at b->c_chi from the b-DEPENDENCE that enters
through the orbit kinematics, independent of the pump's w-shape.

(results appended below as they land)

---

## [MM-1] The FREE-pullback edge: SIMPLE POLE (machine, sympy)

`/tmp/mm_step1.py`. Amplitude A(b) = H^2/[16 pi^2 c_chi (c_chi^2-b^2)]. Set x = c_chi - b.
- c_chi^2 - b^2 = 2 c_chi x - x^2  =>  A(b) = [H^2/(32 pi^2 c_chi^2)] (1/x) + analytic. **SIMPLE POLE**,
  residue R = H^2/(32 pi^2 c_chi^2). This reproduces the SHARED EDGE MAP's free-amplitude simple pole
  EXACTLY (residue -H^2/(32 pi^2 c_chi^2) in the x=c_chi-b convention; sign per orientation).
- **Origin of c_chi^2-b^2 (machine):** it is the inverse SOUND-cone interval on the orbit:
  c^2 deta^2 - (b deta)^2 = -deta^2 (b-c)(b+c). The factor 1/(c_chi^2-b^2) is the orbit crossing the
  SOUND cone (r=b|deta| meeting r=c_chi|deta|). PURELY KINEMATIC — set by the orbit's velocity b
  relative to the sound speed c_chi, NOT by the pump's mode profile.

## [MM-2] The luminal-edge subtlety: b=c_chi is PAST the physical edge b=1 (c_chi>1)

`/tmp/mm_step1.py`, `/tmp/mm_step3.py`. agentU's corner is c_chi^2 = O(gamma/alpha) >> 1, c_chi>1.
The worldline velocity b = a/kappa lives in [0,1) for ALL physical (metric-subluminal) worldlines, and
the PHYSICAL stationary/thermal edge is b=1 (kappa = H/sqrt(1-b^2) -> infinity). The b->c_chi edge with
c_chi>1 is therefore an **analytic continuation PAST the physical luminal edge** — exactly the
"c_chi-luminal edge is an analytic continuation with no banked physical population there" the edge map
flagged. At b=c_chi: 1-b^2 = 1-c_chi^2 is FINITE and NEGATIVE, so **kappa(c_chi) is finite and
imaginary** (machine: 1-b^2 at x=0 is 1-c_chi^2, d/dx = 2 c_chi — analytic, finite). The pump's tail
shape G(omega/kappa) is a FUNCTION of omega/kappa(b); since kappa(b) is finite-analytic at b=c_chi, G is
finite-analytic there. **The ONLY singular b-channel at b=c_chi is the kinematic amplitude pole.**

## [MM-3] The pumped pullback edge: SIMPLE POLE, pump rides through (no new singularity)

`/tmp/mm_step3.py`. Assemble the pumped worldline commutator density on the b-orbit:
> Delta rho_c(omega; b) = A(b) * G(omega/kappa(b)),
with A(b) the kinematic amplitude (simple pole) and G the pumped tail SHAPE (HH's transcribed
omega^{-1/3} e^{-ctil omega^{1/3}} cos(...), b-independent at leading order by EE[3e]'s beta kappa^2=H^2).
At b->c_chi: G(omega/kappa(c_chi)) is FINITE (kappa(c_chi) finite-imaginary), so
> Delta rho_c ~ [H^2/(32 pi^2 c_chi^2)] G(omega sqrt(1-c_chi^2)/H) * (1/(c_chi-b)) + analytic.
**The pumped edge is a SIMPLE POLE.** The pump does NOT generate an essential singularity at b=c_chi;
it transcribes its own analytic shape times the kinematic pole. The two indices ride disjoint labels —
w (pump/scale) and b (worldline) — confirmed: they never meet in a way that turns the pole into a
fourth-root.

(continued — testing the alternative edge variable + whether the response cancels the pole)

## [MM-4] The response pole does NOT cancel for c_chi>1 (machine) — the cancellation is the c_chi=1 anchor

`/tmp/mm_step4.py`. The edge map's exact response cancellation [(c_chi^2-b^2)^{-1} kappa^{-2} = c_chi/H^2]
holds at the CONFORMAL anchor c_chi=1. Machine: (c_chi^2-b^2)^{-1} kappa^{-2} = (1-b^2)/[H^2(c_chi^2-b^2)].
At b->c_chi for c_chi>1 the numerator -> 1-c_chi^2 != 0, so the response KEEPS a **simple pole**, residue
(1-c_chi^2)/(2 H^2 c_chi). For c_chi>1 (agentU's actual corner) there is NO cancellation and NO conversion
to a vanishing sqrt edge — the response is itself a simple pole. The Watson-power-law nullity the edge map
reported was specifically the c_chi=1 cancellation; off it, the simple pole survives in the response too.

## [MM-5] ADVERSARIAL: the sqrt(c_chi-b) conversion has NO substrate at b=c_chi (smuggle vector exposed)

`/tmp/mm_step4.py`. The fourth-root story relies on u = 2pi/kappa ~ sqrt(c_chi-b) converting an x^{-1/4}
edge into u^{-1/2}. Machine check of u(b)=2pi sqrt(1-b^2)/H:
- at b=c_chi (c_chi>1): u = 2pi sqrt(1-c_chi^2)/H = FINITE (imaginary). **u does NOT vanish like
  sqrt(c_chi-b)** — there is no sqrt-of-the-edge-distance behavior at b=c_chi.
- u ~ sqrt(edge distance) holds ONLY near b=1: 1-b^2 = 2(1-b)-(1-b)^2, so u ~ 2pi sqrt(2(1-b))/H.
- These coincide ONLY at c_chi=1 (where b=1 IS b=c_chi). **For c_chi>1 the sqrt-conversion variable lives at
  the PHYSICAL luminal edge b=1, the WRONG edge — and b=1 is the thermal/conformal edge (kappa->inf), which
  carries NO essential singularity.** So the kinematic substrate for "fourth-root in x converts to
  half-power in u" is ABSENT at the b=c_chi edge. Re-presenting it would be smuggle vector S2/S5
  (importing LL's conversion-theorem target as the edge form). Flagged and refused.

## [MM-6] THE STEELMAN at c_chi=1: a generic bulk pump gives POWER LAW, not a fourth root

`/tmp/mm_step5.py`, `/tmp/mm_step6.py`. The only place the geometry could support a fourth root is the
c_chi=1 anchor (pole cancels, u~sqrt(1-b)). There the surviving edge is the PUMP TAIL SHAPE re-expressed in
u. Run the bulk pump FORWARD with no target input:
- HH's banked theorem (powers -> powers, all-orders anchors p=0,1,2): a generic structureless
  scale-invariant pump gives a POWER-LAW worldline tail => POWER-LAW u->0 edge. Bessel anchor
  nu*Delta rho_c -> -mu c^2/2 = -0.8 EXACTLY (a constant; pure 1/nu power series, NO e^{-omega^{1/3}}).
- An x^{-1/4}/u^{-1/4} ESSENTIAL singularity (the oscillatory fourth-root) appears ONLY IF the input pump
  profile ALREADY carries the locked Gevrey-3 pair e^{2 ctil e^{+-2pi i/3}(c w)^{1/3}} — i.e. it is HANDED
  ctil*c_chi^{1/3} ~ zeta^{2/3}, the 1/sqrt3 lock, and the phase. This is HH Theorem HH-1 reaching the edge.

## [MM-7] FORWARD numeric edge-exponent fit: p -> -1 (simple pole), c_chi=1 residue regular (machine)

`/tmp/mm_step6.py` (mpmath dps 30). Build Delta rho_c(b) = A(b) G(omega/kappa(b)) for a generic analytic
bounded pump shape G and fit the edge exponent on b = c_chi - eps:

| eps | local log-log slope p |
|---|---|
| 1e-3 | -0.99372 |
| 1e-4 | -0.99937 |
| 1e-5 | -0.99994 |
| 1e-6 | -0.999994 |

**Edge exponent p -> -1.000000 (SIMPLE POLE), NOT -1/4.** Any analytic bounded pump gives the same -1
(the pole is the kinematic A(b); the pump shape only sets the residue). At the c_chi=1 anchor the
prefactor (1-b^2)/(c_chi^2-b^2) collapses to the constant 1/H^2 (machine: =1.0 at every eps) and the
surviving response is the regular pump shape in u~sqrt(1-b) — a Watson power law, respDR -> const, **no
u^{-1/2}, no x^{-1/4}.**

## VERDICT (Route A)

**The bulk pump (HH's scale-invariant g) on the Deser-Levin b-family gives the TRANSCRIPTION plus a
kinematic SIMPLE POLE at the b->c_chi edge — NO genuine edge essential singularity, NO fourth root.**

1. The b->c_chi edge of both the raw pullback amplitude and (for c_chi>1) the response is a **SIMPLE POLE**
   [MM-1, MM-3, MM-4, MM-7], residue H^2/(32 pi^2 c_chi^2). Its origin is purely kinematic — the orbit
   crossing the SOUND cone (1/(c_chi^2-b^2) = inverse sound-cone interval) — set by the worldline velocity
   b, NOT by the pump's mode profile [MM-1].
2. b and w (the pump label) ride DISJOINT labels; the pump's tail SHAPE enters as G(omega/kappa(b)) which
   is finite-analytic at b=c_chi because kappa(c_chi) is finite-imaginary for c_chi>1 [MM-2, MM-3].
3. The sqrt(c_chi-b) conversion that the fourth-root story needs has NO substrate at b=c_chi for c_chi>1
   (it lives at the physical luminal edge b=1, which carries no essential singularity) [MM-5]. Using it
   would be smuggle vector S2/S5.
4. At the c_chi=1 anchor (the only place the pole cancels and u~sqrt(1-b)), a GENERIC bulk pump produces a
   POWER LAW, not a fourth root [MM-6, MM-7]. An oscillatory x^{-1/4} essential singularity appears ONLY if
   the input pump ALREADY carries the locked Gevrey-3 pair — i.e. it is HANDED the edge form. **This
   CONFIRMS the edge is FREE input** (the SHARED EDGE MAP's central claim, reached here independently by
   forward construction): rho(b)'s b->c_chi edge / the pump's edge essential singularity is not fixed by
   the bulk pump dynamics — it is the lone free input on which index-1/3 vs power-law nullity turns.

**carries_fourth_root = NO** (computed, not assumed): the bulk pump gives a simple pole / power law; the
fourth-root is FREE input, not generated.

## SMUGGLE AUDIT (mandatory, self-incriminating)

Where this derivation could have cheated to reach q=1/4 / a fourth root:
- **[avoided] Choosing the c_chi=1 edge variable u~sqrt(c_chi-b) and DECLARING the response a fourth root.**
  At c_chi=1 the response pole cancels and u~sqrt(1-b) is real — exactly the geometry that converts a
  hypothetical x^{-1/4} into u^{-1/2}. I could have asserted "the edge is u^{-1/2} = fourth-root class" and
  matched q=1/4. I refused: the conversion converts a fourth-root that the BULK PUMP DOES NOT PRODUCE
  (generic pump -> power law, [MM-6/MM-7]); presenting the conversion as a derivation is smuggle vector
  S2/S5 (importing LL's conversion theorem / re-presenting sigma_req's edge as a derived rho(b)).
- **[avoided] Feeding the locked Gevrey-3 input profile and reading its edge back out.** HH's keystone
  profile F_req ALREADY carries ctil*c_chi^{1/3} ~ zeta^{2/3}; running THAT through the pullback reproduces
  the fourth-root — but that is transcription (D2/D3 violation: q=1/4 in -> q=1/4 out), the headline
  inverse-image laundering (S5). I used only a GENERIC structureless pump for the forward edge fit, so the
  -1/4 had no way to enter except by being handed.
- **[avoided] Quoting EE[3c]'s omega^{1/3} <-> u^{-1/4} dictionary as if the dictionary were the
  derivation.** That dictionary maps sigma_req (TARGET) to the worldline; applying it forward to the bulk
  pump is only legitimate if the bulk pump independently produces the omega^{1/3} tail — which HH proved it
  does NOT (it transcribes). I kept the dictionary on the target side.
- **[residual caveat] kappa(b) is reconstructed from the short-distance normalization** (matches EE[2c]/
  LL S4b), not an independent read; but the simple-pole and power-law edge classes are robust to this (the
  c_chi=1 cancellation is exact and the fixed-kappa variant is still non-fourth-root, per the edge map).
- **[honest both-ways]** Framework-favorable territory got maximum hostility: I built the steelman
  (c_chi=1, the one place a fourth root could live) and STILL found power law. The verdict is not a reflex
  ANTI-framework call either — if the input pump carries the locked pair, the fourth root DOES return at
  unit fidelity (HH-verified). The finding is precise: the edge is FREE, not forced, not forbidden.
