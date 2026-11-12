# The completion attempt: action, mechanism, growth (2026-11-11)

Adopts nothing. kappa = 1/2 FITTED; not theory closed. Not a lane: no criteria, no label, nothing graded.
**A candidate, not a result. No piece below has passed a gate.** Each piece names the lane that grades it.
Status tags: **[C]** certified in a lane of the record; **[H]** hand algebra; **[X]** the equations do not give it.
Footings never pooled.

---

## 0. What a completion has to do, given `CRUX.md`

1. **Pay the amount**, or show the amount is smaller than the record's 59.5 M_b. The budget is 5.41 M_b and the
   charge that falls in is 0.9-1.4 M_b. T4 and LFS1 (both exact) cap the halo at the charge carried in.
2. **Make the clock static behind the fold, and the dust inert there** (CLOSURE.md's two requirements), *and*
   make the law's reach exceed the fold's reach — FLD1 says the fold stops 1.3-5.4x short of KiDS's windows.
3. **Grow structure**: the forest at z 2.2-4.4, CMB lensing, f sigma8. FRZ1, FZS1, SRH1 and FRZ2 each fail a
   simple version of this.

These three are not independent. (1) is the gate: everything else has a candidate; (1) does not.

---

## 1. The action

    S = Int sqrt(-g) {  R / (4K)  -  Lambda / (2K)                                [FROM (A)]
                        + L_K(Q, Pi)                                              [NEW - see 1.1]
                        + P^m A_m - W(K|P|) - gamma_L F(Pi) + lambda n^m P_m      [FROM (A): the law]
                     } + S_matter[g, baryons, photons, neutrinos]

    W(p)   = (a0^2 / K) [ -p/a0 - ln(1 - p/a0) ]          [FROM (A)]
    F(Pi)  = [max(Pi,0)]^2 / 2,   gamma_L = K Lstar^2 / 2 [FROM (A)]
    Q = sqrt(-g^{mn} d_m tau d_n tau),  n_m = -d_m tau / Q,  A_m = n^n nabla_n n_m,  Pi = D_m P^m

Everything except L_K is the record's certified action (A) (QX17). Nothing else is changed: no switch, no wall,
no second force on baryons, baryons stay on geodesics. That is deliberate — every departure from (A) that the
record has tried has a failing verdict (see the closed list in `ANALYSIS_2026-11-11.md` section 2).

### 1.1 The dust term: the one change MK1 asks for

MK1's own conclusion: **the dust term cannot depend on the clock offset alone.** DT1's trade-off, which kills
every one-variable n(x), assumes one variable. So:

    L_K(Q, Pi) = (mu_K^2 / 2K) (Q - 1)^2 * S(Pi / Pi_c),     S(0) = 1,  S decreasing.

Why Pi: it is already in the action, it is zero on the FRW background (P = 0 by symmetry), it is **first order
in perturbations** about FRW, and it is large exactly where a halo exists.

| Row | What the key does | Status |
|---|---|---|
| FRW | Pi = 0, so S = 1: the CMB rows are MK1's, unchanged, mu_K free for the CMB | [H], to grade |
| Linear order | Pi is O(delta), so the correction multiplies (Qbar-1)^2 ~ 1e-12: **invisible at linear order**; growth is untouched | [H], to grade |
| Static galaxy | Pi large, S small: the -mu_K^2 Phi/K pooling that breaks the galaxy bound is suppressed | [H], to grade |
| Cluster | **collision.** Pi is LARGER in a cluster than in a galaxy at the same radius (rho_c ~ sqrt(M_b)/r^2), so a monotone S suppresses clusters more — but X-COP needs the dust ON there (+0.5 dex) | [X] as written |

**The cluster collision is stated here, not hidden.** A monotone S cannot give "no dust in galaxies, dust in
clusters" because Pi is ordered the same way in both. PIK1 (HY4-3) grades both signs and a non-monotone S, and
is instructed to report which rows each fixes and which it breaks. If no S works, the dust term needs a
different second variable, and I do not have one: the variable must be small at recombination, small in
galaxies, and large in clusters, and every field in the action is monotone across galaxies and clusters.

### 1.2 The share

X_s is an input rule in the record (PD1's 59.5 M_b), not an output. **[X]**. Two routes:
- **Formation-set (FRM1, HY4-5):** the amount is fixed when the system forms and conserved afterwards. HIS1
  scores this reading 4 of 5 on DD1's frozen 626-system table, against 1 of 5 for "the law is a force every
  system obeys now". It predicts, in advance, that stripped systems (tidal dwarfs, DF2/DF4) sit LOW and hosted
  systems sit HIGH — which is what DD1 measures (0.6-0.9 low; +0.5 to +0.6 high).
- **Budget-limited (this file):** the share cannot exceed 5.41 M_b unless the baryon census is wrong.

---

## 2. The mechanism

**The medium is an elastic solid, not a gas.** Computed (`hy4_crux_check.out` section A), from the record's own
certified stress Pi_ij = J(g) delta_ij - g_i g_j/(K(1+u)):

    in the deep field   Pi_rr = -Pi_tt   exactly,   so   sigma_r^2 = -v_inf^2/2  < 0,
                                                          sigma_t^2 = +v_inf^2/2,   v_inf^4 = G M_b a0.

A negative radial "dispersion" is impossible for any kinetic gas and is the signature of a shear modulus: the
halo is a medium under **radial tension** and **tangential pressure**. Computed values of
(Pi_rr + Pi_tt)/Pi_tt: 0.96 at 0.1 r_M, 0.20 at 3 r_M, 0.066 at 30 r_M, 0.0066 at 100 r_M — the deep-field
identity, with the correction dying as 1/x.

**How it gets there (the settling):** VSH1 finds the clock settles behind a shock at 0.51 of the turnaround
radius (FLD1's fold: 0.52), at every mass and both footings, since z 4.96 / 3.45 / 1.46. Behind the shock the
clock is at rest and in pressure balance — that is the static state, and SCS1/SCS2 say it is stable once
reached. So the mechanism for reaching it exists **[C: VSH1, under its post hoc A1]**.

**Why it stops there (the reach):** FLD1 says the fold covers every rotation curve and stops 1.3-5.4x short of
KiDS's windows. So the mechanism makes the clock static *inside* the fold and nowhere else, and lensing sees
the law outside it. **[X] — this is the joint, still open.**

**What it costs:** a solid has to pass through itself (the Bullet's offset) and stay decoupled at
recombination. Both are named in advance as the gates most likely to kill it. ELA1 (HY4-7) grades them.

---

## 3. Structure growth

The growth rows are computed, not derived, in the record: form B carries the CMB and large-scale growth from
the cold reference, and its own redistribution at z 2-4 is what fails the forest (FRZ1 Delta chi^2 9916 / 9009
against a gate of 4). There is no derivation of the growth history. **[X]**

What I would run, and what GRW2 (HY4-6) is running: **the inverse problem.** Take the halo's share as a free
function X_s(z, M_b) and ask what history satisfies SRH1's four gates at once:

| Gate | Requirement (SRH1) |
|---|---|
| G1 forest (FZS1 pipeline) | f <= 0.70 (edge 0.722 / 0.725) |
| G2 RC100 coverage at 2.2 R_e | f >= 0.391 |
| G3 SPARC coverage | holds at every grid f |
| G4 ONE1 KiDS host-free | f >= 1.25 (edge 1.004 / 1.050) |

G1 and G4 exclude each other by a factor 1.39 / 1.45 for any single f. SRH1 found a post hoc redshift tilt
f = f0 (1+z)^beta with beta = -1 (f0 1.5, 2.0) or -0.5 (f0 1.25) that passes all four, and counted that as an
outcome against. GRW2 is asked to say whether that tilt is *excluded* or merely *post hoc*, and if post hoc, to
freeze the test that would decide it.

**Honest status of the growth piece: there is no derived growth history. There is a required one being
computed, and it is currently empty (SRH1 WINDOW EMPTY).**

---

## 4. The exits, ranked by what I think they are worth

| # | Exit | Escapes | Graded by | My read |
|---|---|---|---|---|
| 1 | **The gas census.** g_bar at 0.1-2 Mpc is missing hot gas; the 11.0x is a measurement, not a contradiction. | nothing — it removes the contradiction | HY4-1 GAS1 | **most likely.** The record's own B21 note moves KiDS from 1.50 to 0.47 of the law. Bet registered in `CRUX.md`. |
| 2 | **Formation-set share.** The amount is set when the system forms, then conserved; the 5.41 budget applies to the halo's *virial* baryons, not its stars. | the budget, not T4 | HY4-5 FRM1, HY4-9 DWF1 | Scores 4 of 5 on the data already. Needs the epoch fixed. |
| 3 | **Two-variable dust term.** Escapes DT1's trade-off. | DT1, MK1 | HY4-3 PIK1 | Right shape; dies on the cluster collision unless S is non-monotone. |
| 4 | **Sourced charge.** Break the conservation law; the vacuum pays. | T4, LFS1 | HY4-4 VCC1 | Radical, TOE-scale, and the only route past a conservation cap. Must keep Bianchi and the background. |
| 5 | **An elastic solid.** Says what the medium is. | M5 (if the constitutive relation is non-local or self-gravity non-normal) | HY4-7 ELA1 | Right physics for the stress; must pass the Bullet and recombination. |
| 6 | **a0 as a field.** a0 = kappa sqrt(G V(chi)). | the constant a0; gives a0(z) | HY4-8 A0Z1 | Ungraded since DT1. The bracket goes negative at u > 100. |
| 7 | **Clusters are per-galaxy halos.** Apply "counted once" per member, not per cluster. | CLS1's NO STATE | HY4-10 CLS2 | Cheap to test on all seven X-COP clusters. |

---

## 5. Kill conditions, stated before the lanes report

1. If GAS1 shows the gas on disk supplies **less than half** of the 11.0x, the amount is a real contradiction
   and exits 2-4 are the only ones left.
2. If PIK1 finds no S (either sign, monotone or not) that keeps X-COP's +0.5 dex while lifting MK1's galaxy
   bound, the two-variable dust term is closed and MK1's conclusion stands unrepaired.
3. If ELA1 finds the solid's transverse sound speed imaginary anywhere, or that it cannot pass through the
   Bullet's offset, the elastic reading is closed and the negative sigma_r^2 becomes an artefact of a kinetic
   description that does not apply.
4. If VCC1 cannot keep the Bianchi identity and the 5.41 background while sourcing 59.5 M_b in a galaxy, the
   conservation cap stands.
5. If GRW2's required history is empty even with a free X_s(z, M_b), the growth row is not recoverable inside
   form B and the form, not the joint, is what fails.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
