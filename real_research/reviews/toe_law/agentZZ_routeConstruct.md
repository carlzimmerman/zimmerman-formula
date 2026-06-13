# agentZZ — Route 1: the SPATIAL-nonlocal slip carrier. Does it evade the keying theorem?

STATUS: IN PROGRESS (compute-first; written incrementally).

## Charge

Build a SPATIAL-nonlocal slip operator: the slip Psi at point x depends on the field through a
finite-range spatial kernel K(|x-x'|) (Yukawa/Gaussian of range L, or the resolvent
1/(1 - L^2 nabla^2) acting on the metric potential), NOT on the local acceleration Y_a and NOT on
time-history. THE KEY TEST: the keying theorem's pollution (agentDD) came from delta-Y_a/delta-Phi
(the LOCAL key's lapse response) feeding the Hamiltonian constraint at (a0 r/c^2)^-1 x phantom. A
SPATIAL kernel's key is the smoothed field; its lapse response is the SMOOTHED delta-Phi. Does the
spatial smoothing SUPPRESS the constraint pollution, or merely relocate it?

## What the two prior walls actually proved (read in full)

- **agentDD KEYING THEOREM.** Pollution enters eqN through delta-Y_a/delta-Phi. The mechanism, made
  fully explicit (agentDD wall-3, KK reading log): Y_a = a.a c^4/a0^2 with a_i = d_i ln N, so the
  variation of the key wrt the lapse test function puts a SPATIAL DERIVATIVE on that test function;
  IBP lands an UNSUPPRESSED geometric piece ~ slip/r^2 = (a0 r/c^2)^-1 x phantom. The wall-4 r^0
  (geometric) class of the exact lens-only condition is S-FREE and equals alpha^6 x (slip/Phi') ->
  slip == 0 is the only lens-only branch. The carrier "must read y NONLOCALLY."
- **agentKK STATIC-EQUIVALENCE (KK-1).** Any TTI causal TIME-history key K[y2-history] with a
  differentiable static read K_static(Y) gives, ON STATIC BACKGROUNDS, field equations IDENTICAL to
  the local theory with C_eff(Y)=F(K_static(Y)). Time-nonlocality is INVISIBLE in the static sector.
  The DC weight of any tracking window is 1; value and constraint-sensitivity are the same number.
  KK explicitly scoped SPATIAL nonlocality as NOT closed: "would need its own charge and faces the
  same track-vs-pollute variational structure."

## The pre-registered hostile question (before computing)

The kill in BOTH prior memos is a STATIC-SECTOR statement. KK-1 worked because a TIME filter, on a
static background, collapses to its DC value (a number) -> a local theory. THE DECISIVE DIFFERENCE
for a SPATIAL kernel: on a static background the spatial kernel does NOT collapse to a number -- it
genuinely convolves over space, exactly where the lens and the kill both live. So KK-1's collapse
does NOT automatically transfer. BUT: the hostile mirror -- a spatial kernel acting on the lapse
still has a delta(smoothed-key)/delta-Phi response; the question is whether the convolution
SUPPRESSES the IBP-enhanced geometric piece by the kernel's smoothing, or just smears it (a smeared
(a0 r/c^2)^-1 is still (a0 r/c^2)^-1 in amplitude at the halo scale r >> L). PLUS the OWN-pathology
tax: a finite-range spatial kernel 1/(1-L^2 nabla^2) is an Ostrogradski/ghost risk and a momentum-
space constraint-structure risk -- a carrier that slips only by introducing a ghost is NOT a
survivor.

## Plan (compute-first)

K0. Reproduce the banked local pollution from agentY_eqs.pkl (the gate).
ZZ1. Build the spatial-nonlocal slip operator on the quasi-static two-function metric. Derive the
     smoothed key and its lapse response delta(K*y)/delta-Phi. The kernel as a LOCAL DIFFERENTIAL
     resolvent 1/(1 - L^2 nabla^2) (so the variation is tractable in closed form; Yukawa Green fn).
ZZ2. Compute the matter-channel (eqN) pollution for the spatial-nonlocal carrier vs DD's local
     result. Does the smoothing suppress the (a0 r/c^2)^-1 factor below the double-counting bar?
ZZ3. Pathology audit: ghost (Ostrogradski sign of the L^2 nabla^2 kinetic operator), causality,
     momentum-space constraint structure.
ZZ4. Second-discriminant check: does the finite range L distinguish linear modes (k~0.01) from
     halos (k~1) = agentII's needed second discriminant?


---

## RESULTS (compute-first; all machine-derived)

### K0 gate — PASS
`agentY_eqs.pkl` loads clean (slipgrad 25 atoms, DeltaPsi 55 atoms; free symbols
{G,J1,J2,alpha,c10,c11,c20,c21,c30,c31,chi1,r}). The harness used for the kernel-invariance
corollary. Files: `agentZZ_routeConstruct.py`, `agentZZ_resolvent.py`, `agentZZ_locked.py`,
`agentZZ_action.py`, `agentZZ_gate.py`, `agentZZ_decouple.py`, `agentZZ_pathology.py`,
`agentZZ_disc2.py`.

### ZZ1/ZZ2 — THE KERNEL IS LOCKED (the keying theorem TRANSFERS, spatial version). EVADES-NOTHING.

The finite-range spatial kernel = the resolvent 1/(1 - L^2 nabla^2), Fourier multiplier
**Khat(k) = 1/(1 + L^2 k^2)** (the massive/Yukawa propagator; the unique ghost-free finite-range
form). Khat(0)=1, Khat(inf)=0; monotone-decreasing low-pass.

**Honest action variation (the load-bearing check, `agentZZ_action.py`).** From ONE Lagrangian
density `L_slip = B(K)*(Psi-Phi)*k^2`, key `K = k^2 Khat^2 Phi^2` (the smoothed acceleration
magnitude — the ONLY key that yields nu(g_bar/a0)):
- `eqL` (slip channel) = `k^2 B(K)` — carries the kernel through K ~ Khat^2.
- `eqN` (matter channel) keying-pollution term = `B'(K)*(dK/dPhi)*(Psi-Phi)*k^2`, with
  `dK/dPhi = 2 Phi k^2 Khat^2`. The pollution carries the SAME geometric k^2 enhancement
  (= agentDD's slip/r^2 = (a0 r/c^2)^-1) AND the SAME Khat^2 dressing as the slip.
- **pollution/slip kernel ratio = Khat^0 = 1, exactly, at every mode k.** The smoothing that
  suppresses the pollution suppresses the slip by the identical factor.

**Kernel-invariance corollary on the real pickle (`agentZZ_gate.py`).** Matching the slip target
re-amplifies B by 1/Khat(k), which cancels the kernel in the pollution: slip-matched pollution /
local = **1.000000** at every (L,k) tested. This is agentDD/agentKK's locked ratio, now proved
for the SPATIAL class — the spatial analog of KK-K2's filter-invariance.

**The two-branch fork (`agentZZ_resolvent.py`, `agentZZ_locked.py`).**
- Branch A (acceleration-keyed, smoothed gradient): the ONLY branch that produces nu(g_bar/a0).
  The kernel only ADDS an L^2-derivative dressing (`-L^2 Phi' eta'''`) on top of the LOCAL
  enhanced term (`Phi' eta'`) — it does NOT cancel the leading (a0 r/c^2)^-1 enhancement.
  Suppressed only at k >> 1/L, where the slip dies too. INHERITS THE WALL.
- Branch B (potential-value-keyed): the lapse response loses the (a0 r/c^2)^-1 enhancement, BUT
  the slip is then potential-keyed not acceleration-keyed -> does NOT give nu(g_bar/a0); constant/
  potential-keyed slip is a dead wall-4 branch in agentY/agentW. WRONG OBSERVABLE.

**Hostile decoupling attempt (`agentZZ_decouple.py`).** Enumerated independent kernel powers on
the key (p), the geometric generator (q), and the slip-difference (s). In EVERY placement the
keying pollution rides the SAME `B(key)` response as the slip — decoupling the geometric
*generator* kernel does NOT decouple the pollution from the slip. A bare (un-smoothed) generator
(q=0) just re-imports the FULL un-suppressed (a0 r/c^2)^-1 pollution. No placement gives an
acceleration-keyed slip with a suppressed pollution.

### ZZ3 — PATHOLOGY AUDIT: the carrier is CLEAN, but the clean kernel is EXACTLY the one that LOCKS.

- **No ghost / no acausality.** Finite RANGE (exponential localization exp(-r/L)/r) REQUIRES the
  +sign resolvent 1/(1+L^2k^2): poles at k=+-i/L (imaginary -> decaying, causal). The -sign
  1/(1-L^2k^2) has a REAL pole at k=1/L (tachyon/ghost/oscillatory-acausal) and is NOT
  finite-range. The healthy kernel = one auxiliary massive scalar (mass 1/L, standard +kinetic
  sign): finite d.o.f., no Ostrogradski, causal static Yukawa Green function. **The spatial-
  nonlocal carrier is ghost-free and causal — slip does NOT require a pathology.**
- **But the clean = low-pass with Khat(0)=1 (DC gain 1) = the KK-1 locked-DC condition in space.**
  Long-wavelength modes pass unsuppressed; to suppress the pollution at the slip's mode you
  suppress the slip equally. The only kernel that decouples scales is a BAND-PASS with Khat(0)=0
  = NO static long-range force = NO lens (the spatial twin of KK's failed zero-DC derivative key),
  and a high-pass/band-pass form carries a 1/k^2 IR pathology (acausal long-range) or a ghost
  pole. **Ghost-free <=> locked; decoupled <=> no-lens-or-ghost. No third branch.**

### ZZ4 — SECOND DISCRIMINANT: the finite range IS a scale knob, but WRONG-WAY (does NOT supply agentII's).

agentII needs: suppress (Sigma-1) by >=50-800x at k<=0.3 h/Mpc (linear) WHILE preserving halo nu
to r~1-3 Mpc. The finite-range LOW-PASS kernel is monotone-decreasing in k, so it does the
OPPOSITE: transparent at small k (linear: Khat->1), suppressing at large k (halos). Numerically
(`agentZZ_disc2.py`): >=50x linear suppression needs L>=33 Mpc, but halo preservation at r=3 Mpc
needs L<<0.5 Mpc — a ~70x contradiction, and even then it suppresses the HALO not the linear mode
(Khat(k_lin) > Khat(k_halo) ALWAYS, since k_lin<k_halo). **The finite range distinguishes scales
in the INVERTED direction; it supplies the mirror image of agentII's discriminant, not the
discriminant.** (A carrier that suppressed slip at LINEAR scales would need a HIGH-pass kernel —
Khat(0)=0 — which is the no-static-lens/ghost branch from ZZ3.)

## VERDICT: **NEW-WALL — INHERITS-WALLS.** The spatial-nonlocal carrier is GHOST-FREE and CAUSAL
(no pathology required for slip), but it does NOT evade the keying theorem: the ghost-free
finite-range kernel is a low-pass with DC gain 1, and the pollution and the slip carry the
IDENTICAL kernel factor at every mode (locked ratio = 1, exact; slip-matched pollution
kernel-invariant = 1.000000 on the real pickle). This is the SPATIAL completion of agentKK's
static-equivalence theorem: just as time-nonlocality is invisible in the static sector (KK-1),
SPATIAL-nonlocality is locked because the lens and the pollution are the SAME spatial structure
(agentDD wall-4: r^0-class = alpha^6 (slip/Phi')) — smoothing one smooths the other identically.
The keying theorem now spans LOCAL (agentDD), TIME-nonlocal (agentKK), and SPATIAL-nonlocal
(agentZZ): **any kernel — local, temporal, or spatial — that the slip operator uses to read the
acceleration key is shared by the slip and the matter-channel pollution; the (a0 r/c^2)^-1
double-counting cannot be smoothed away in EITHER coordinate.**

Second discriminant: NOT supplied (wrong-way monotonicity; the low-pass suppresses halos, the
mirror image of agentII's need). The finite range is a real scale knob but pointed backwards.

**The new theorem (ZZ-1, the kernel-locking theorem).** For any slip operator whose acceleration
key is read through a convolution kernel Khat(k) (local: Khat=1; temporal: KK-1; spatial: this
memo), the matter-channel keying pollution and the Psi-channel slip carry the SAME Khat at every
mode -> the slip-matched pollution is kernel-invariant. Suppression (|Khat|<1) and slip-delivery
are the same number at the same mode. Escape requires Khat that is small where the slip lives and
large elsewhere = a band-pass, which on the STATIC lensing job means Khat(0)=0 = no long-range
slip (or a ghost/IR-acausal pole). The unification is now three-coordinate-robust: LOCAL + TIME +
SPACE all locked, by the same DC/zero-mode argument.

## For DERIVATION_CHAIN Link 7 / [SLOT-Y]
The keying-theorem pincer closes the SPATIAL-nonlocal route (the last of agentDD/KK's named
survivors except the singular-surface route and non-b(x)b spin-2). The slip operator cannot escape
by reading the acceleration key through ANY kernel in space, time, or locally. Remaining
genuinely-open: the singular-surface exact route (low prior, and ZZ-1 says no kernel dressing
helps it either, mirroring KK corollary iv) and non-b(x)b spin-2 condensates (keying-argument
disfavored, not machine-closed). Convention-robustness: ZZ-1 and the kernel ratio are symbolic —
no a0/footing/weighting/nu-shape enters; the ZZ4 numbers are at the agentII bar and survive both
footings at the orders involved. No git.
