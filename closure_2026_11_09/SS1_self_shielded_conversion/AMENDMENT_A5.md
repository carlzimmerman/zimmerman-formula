# SS1 AMENDMENT A5: variant I (outside round 12), frozen once, committed alone before any I number

Criteria b5adc7a90b; A1-A4 as recorded. TEST lane, quarantined; adopts nothing; no particle adopted. kappa = 1/2 FITTED; not
theory closed. Footings never pooled. Construction as relayed by the orchestrator, in the lane's words.

## 1. I-core (graded)

**Onset and rate.** G's on the record's footings: z_dec 0.631, alpha 4.367 / 4.366.

**Kick.** v_kick = 1 x v_stiff (265.8 / 288.1 km/s).

**Retention per radius**, in SS1's primary pre-conversion halos (KD1 P3 SIS):

f(r) = e^-alpha + (C - e^-alpha) exp(-3 (v_stiff / v_vir)^2 / g(r)), with C = 1/sqrt(3).

- **g:** I-core uses the halo's own sigma(r)^2 / v_vir^2, which is 0.5 for the SIS.
- **Time dependence** (not given by the source, frozen here): the converted share grows linearly in tau,
  f(r, tau) = 1 - (1 - f(r)) tau / alpha.
- **Daughters:** A4's bound-daughter rule. A daughter with E = (1/2)(3 sigma^2 + v_kick^2) + Phi < 0 stays where it was made.
  Unbound daughters are placed in a Gaussian shell around their system: mean R_FS, sigma 0.3 R_FS. R_FS is the comoving
  streaming length today, the integral of v_kick (a_dec/a) / a dt from z_dec, from the lane's own background (the source
  claims 1.68 / 1.82 Mpc).
- **Members** take the host's f at their radius (reported only: gate 4).
- **Cosmology:** unbound daughters are the non-clustering fraction above k = 1 / lambda (lambda = R_FS(a)); bound daughters
  keep clustering.

## 2. Brackets (labelled beside I-core, never replacing it)

- **I-src:** the source's fitted g_vir(u) = (u / (0.07 + u))(1 - 0.45 u), with u = r / R500 (clipped at 0 beyond u = 2.22).
- **I-nob, the source's accounting:** every daughter leaves its system, even where it is bound (E < 0). This is the only
  way the source's X-COP "G x 0.5" can arise, and it is named as such. The unbound share goes in the shell; the bound share
  is removed from the system.

## 3. Constants recorded beside the labels (orchestrator flags)

- The ceiling 1/sqrt(3): **fitted**, chosen after SS2's over-fill (log 1/0.577 = 0.24 against SS2's measured 0.21).
- g_vir's 0.07 and 0.45: **fitted** shape numbers (I-src only).
- Form choices: the factor 3, the exponential law, kick factor 1, and G's cube root / 4 pi.

Count: I-core has 1 fitted constant plus its form choices; I-src has 3 fitted.

## 4. Gates, lines, label

A4's gates and lines, unchanged:
- 1 KiDS
- 2 groups
- 3 X-COP
- 4 UDGs (reported)
- 5 SPARC
- 5b UMa
- 6 background
- 7(b) lensing (NO VERDICT; no validated method)
- 8 forest + fsigma8 (fine-grid derivative, A4 disclosure)
- 9 Bullet
- 10 Cassini

**Label:** first failing gate in A's order, per footing, for I-core. The brackets are labelled beside it.

**Reported beside the claims** (compute, do not take):
- KiDS 1-halo retention at M* 10^11 / 10^11.3 / 10^11.5 (claimed 1.3 / 2.1 / 4.0 %), on primary and Moster halos;
- the Delta Sigma-equivalent shift at 1.5 Mpc (claimed +0.038);
- groups at M500 2e13 / 4.5e13 / 1.4e14 (claimed 22 / 32 / 45 %);
- X-COP retained / M_dyn (claimed 0.71 / 0.65 / 0.46);
- sigma8 ratio (claimed 0.95), S8 (0.769), fsigma8 (0.459 / 0.471).

## 5. Known answers

- **KA-I1:** the code's f equals the formula at u where g is known (SIS g 0.5), to 1e-12.
- **KA-I2:** law-only replay.
- **KA-I3:** R_FS from the lane's background is printed beside the source's 1.68 / 1.82 Mpc.

## 6. MUTATE

- **MI1:** ceiling C -> 1 (the fitted constant removed). Groups or X-COP numbers must move by more than 0.05 dex in the
  median; otherwise NO BITE.
- **MI2:** kick -> 0 (all daughters bound). KiDS or SPARC must FAIL.

## 7. Hand estimates (before any number)

- **Retention, SIS g = 0.5:** groups (v_vir 460-880) f about 0.09-0.33; X-COP about 0.4; galaxies about e^-alpha = 0.013.
- **Kick v_stiff:** groups and clusters keep every daughter bound, so I-core over-fills them as H did (FAIL at groups or
  X-COP). Galaxy halos keep about 0-15 %.
- **KiDS:** the unbound 85 % of a top-bin lens's 4.1 M_b goes to a shell near 1.7 Mpc. Expect +0.1-0.2 dex at 1-1.5 Mpc:
  KiDS FAIL, as the source's own round-11 +0.13.
- **I-nob:** groups under-fill at f* 0, and X-COP is about G x 0.4.
- **S8:** the escaped share is about 50 % of the component at lambda about 1.7 Mpc. Milder than G (6.7 Mpc); the fsigma8
  verdict is unknown.

## 8. Operational

- Disk at about 4 GiB: primary and the NFW local bracket only; outputs small.
- ss1v.py gains the I branch. Outputs are tagged _VI*. Results go in RESULT_I.md.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
