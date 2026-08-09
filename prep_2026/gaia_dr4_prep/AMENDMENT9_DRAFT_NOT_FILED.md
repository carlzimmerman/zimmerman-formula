# ✅ AMENDMENT 9 — **FILED 2026-08-09**

**This draft is superseded. Amendment 9 was FILED on 2026-08-09 on Carl's explicit instruction.**
The registration body now carries the amendment block; `AMENDMENT9_HASH.txt` records
sha256 = e4cbef5b849d817205f35dcb415010abd28b5493837718fd521d56ffd7189ec8.
All eight prior hash files were left unmodified.

**Both blocking issues were resolved rather than waived:**
1. The >1.20 no-verdict edge was **re-derived from its own stated definition** ("above every
   EFE-saturated target"), which had become factually false once the MG target reached 1.2592.
   New edge 1.26, by the same construction that set the original. The cost — 1.20–1.26 becomes
   scoreable, and the DR3 dry run's 1.205 sits there — is filed as a NEW DECLARED RISK.
2. The target is registered **PROVISIONAL**, not at parity, because it is the point-field
   isotropic asymptote and the full nonlinear AQUAL-EFE solve is still owed.

Kept below for the audit trail: the draft as it stood before filing.

---

# AMENDMENT 9 — DRAFT, **NOT FILED**

**Status: prepared but NOT applied. PREREGISTRATION_DR4.md is untouched and its hash still matches
Amendment 8's record (`0a448f88…b54dc`, verified 2026-08-08). No `AMENDMENT9_HASH.txt` exists.**

This draft exists because filing it as written would put the framework's own prediction into a bin the
frozen decision table pre-declares **unscoreable**. That has to be resolved by the author before
anything is stamped. Two blocking issues are stated first, before the amendment text.

---

## BLOCKING ISSUE 1 — the new target lands in the frozen no-verdict bin

Amendment 8 registered declared risk (d): on the magnitude convention a result above **1.20** is
**pre-declared unscoreable**, flagged there because the modified-inertia alt-footing corner reached
1.20069, i.e. 0.00069 over the line.

The modified-gravity target is not near that line. It is entirely past it:

| | value | vs the 1.20 edge |
|---|---|---|
| MG target, canonical | 1.21385 | **above — unscoreable** |
| MG target, alt footing | 1.25916 | **above — unscoreable** |
| *(superseded MI target)* | *1.1582* | *below — scoreable* |

**So filing this amendment as drafted would register a prediction that the framework's own frozen
table cannot score.** That is the same class of scoring defect Amendment 1 fixed, Amendment 7 re-found
and Amendment 8 called "the single most important thing the Route A amendment has to repair" — and it
would be the fourth occurrence.

It cannot be repaired by quietly moving the edge. The edge exists because above it the estimator's
behaviour was judged untrustworthy; raising it requires a stated reason of that kind, not the
convenience of the new prediction. **Either the edge is re-justified on its own merits, or the
amendment must register the target while explicitly accepting that DR4 cannot score it.** Both are
defensible. Neither is mine to choose.

## BLOCKING ISSUE 2 — the new number does not have the old number's provenance

The superseded value came from a **full nonlinear per-star external-field-effect solve**, validated
against an independent linear-response tensor calculation agreeing to $2.9\times10^{-5}$, with an
orientation average over both footings and both external-field conventions.

The replacement, $\gamma_{v}^{\rm MG}=\sqrt{\nu(y_{\rm ext})}$, is the **point-field isotropic
asymptotic** value. It is correct as far as it goes — for an AQUAL-type external-field effect the
boost is isotropic, so no orientation average is needed, and the number reproduces the corpus's
independently recorded perpendicular eigenvalue to $10^{-4}$. But it is not the same grade of
calculation.

**A full AQUAL-EFE solve for the modified-gravity arm is owed.** Until it exists, this target should
be registered as **provisional**, or the amendment should be held until the solve is done. Filing it
at the same status as the number it replaces would overstate it.

---

## The amendment text, as it would read

> **AMENDMENT 9 — the framework's operative arm changes from modified INERTIA to modified GRAVITY,
> and the wide-binary target moves accordingly.**
> date: *(unset — not filed)*
> sha256(PREREGISTRATION_DR4.md) after Amendment 9: *(unset — not filed)*
>
> **superseded:** Amendment 8's in-force $\gamma_{v}=1.1582$ (range 1.1311–1.1964 radial /
> 1.1339–1.2007 magnitude). That value is the **modified-inertia** external-field-effect prediction.
>
> **reason:** the modified-inertia reading is excluded. With the metric unmodified and baryon-sourced
> — a requirement of modified inertia, not an incidental feature — and photons having no rest mass to
> modify, it predicts $M_{\rm dyn}/M_{\rm lens}=1/f_{\rm bar}\approx6.4$ in clusters against an
> observed 1.0–1.3: **$\sim21\sigma$**, and $4.2\sigma$ even on a fivefold-inflated systematic. All
> three rescue routes are closed: the enhancement cannot sit in both the metric and the inertia
> (doing both gives $a=\nu^{2}g_{\rm bar}$); the Randers–Finsler null cone degenerates at
> $\mu=\tfrac12$ with Euclidean signature below, unavoidably for any interpolation reaching deep
> MOND; and Bekenstein–Milgrom's point-particle limit is memoryless.
> Sources: `mi_lensing_axis_2026.py` (24/24), `mi_finsler_null_cone_2026.py` (23/23),
> `mi_point_particle_limit_2026.py` (19/19).
>
> **amended to:** $\gamma_{v}^{\rm MG}=\sqrt{\nu(y_{\rm ext})}=1.2139$ (canonical) / 1.2592 (alt
> footing), **registered as PROVISIONAL** pending the full AQUAL-EFE solve named in Blocking Issue 2.
> Source: `mi_mg_arm_standing_2026.py` (18/18).
>
> **FOR the framework:** (i) the new range is **disjoint** from the superseded one, and the
> separation is $2.68\sigma$ at the frozen $N$, so **DR4 can now distinguish the two arms** — which
> the modified-inertia reading could not do. (ii) The directional external-field test flips from
> kill-switch to **expected signal**: pure modified inertia predicted *exactly zero* aligned
> asymmetry, AQUAL-class theories predict 1–4% with a definite sign, and the first firing gave
> $\hat A=+2.95$ at $p=0.029$ **with the AQUAL-class sign**. An observation that was evidence against
> the superseded arm is evidence for the new one, and it required no new data.
>
> **AGAINST the framework:** (a) **the new target lies entirely above the 1.20 no-verdict edge** —
> Blocking Issue 1, unresolved. (b) The provenance mismatch of Blocking Issue 2. (c) The Cassini
> quadrupole tension (3–15$\sigma$ RAR-versus-$Q_{2}$) is **inherited** by the modified-gravity arm
> and was **not** carried by modified inertia. (d) $a_{0}=\tfrac23c\,m^{2}/g$ and the $\zeta$-pole
> no-go do **not** transfer — a Bekenstein–Milgrom theory has no memory kernel and no first moment.
> (e) The $g^{-2}$ Lorentz-violation prediction is **gone** in pure Bekenstein–Milgrom, which has no
> preferred frame; it survives only under an AeST-type completion. (f) **Clusters are unchanged**: the
> +0.368 dex shortfall is a kernel property, and the cosmic-baryon-budget wall stands.
>
> **unchanged:** the estimator; the 16-row frozen cut table; the error model; the strictness ladder;
> the NSS screen; the frozen $N=30{,}000$; both $a_{0}$ footings; §2 void per Amendment 5;
> Amendment 7(e)'s reporting rule (raw $\hat\gamma$ with $\sigma_{\rm fit}$ and both distances, never
> a single verdict word); the $\kappa$-window declared risk; and **$\kappa=\tfrac12$ FITTED, NOT
> DERIVED**. No measurement moves.

---

## What must happen before this is filed

1. **Resolve Blocking Issue 1.** Either re-justify the 1.20 edge on its own merits, or register the
   target while explicitly accepting that DR4 cannot score it. The second is honest and costly; the
   first must not be done for the new prediction's convenience.
2. **Decide on Blocking Issue 2.** File as provisional, or hold until the full AQUAL-EFE solve exists.
3. **Retarget the pipeline** — `wide_binary_pipeline.py` currently carries the superseded 1.1582,
   retargeted there earlier on 2026-08-08 from the even older 1.09.
4. **Then, and only then**, apply the body edit, compute the new digest, and write
   `AMENDMENT9_HASH.txt`.

**Nothing in this file has been applied. The registration and every existing hash file are
untouched.**
