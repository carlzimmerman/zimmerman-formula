# SS1 AMENDMENT A4: variant H (outside round 11), frozen once, committed alone before any H number

Criteria b5adc7a90b, A1 9aeeb48503, A2 2b866ef57a, A3 694668618a. Variants A-G stand as recorded. TEST lane, quarantined;
adopts nothing; no particle adopted. kappa = 1/2 FITTED; not theory closed. Footings as before, never pooled. The outside text
is not in the lane; the construction is frozen here in the lane's words, as the orchestrator relayed it.

## 1. H-core (graded)

**Onset and rate.** As G on the record's footings: z_dec 0.631, alpha 4.367 / 4.366, v_stiff 265.8 / 288.1 km/s.

**No gate.** No Hill switch, no mediator, no x0.

**Retention per radius**, in the pre-conversion halo:

f_ret(r, tau) = exp( -(tau / pi) (v_stiff / v_vir)^2 / g(r) ), with g(r) = sigma(r)^2 / v_vir^2 and v_vir = sqrt(G M500_pre / R500_pre).
At tau = alpha this is today's retention. The halos are SS1's primary: KD1 P3 SIS truncated at R200.
- For the SIS, sigma^2 = V^2 / 2 (isotropic, the untruncated profile), so g = 0.5 at every radius and f_ret is uniform:
  exp(-(2 alpha / pi)(v_stiff / v_vir)^2).
- Bracket H-NFW (Duffy c-M): sigma(r)^2 from the isotropic Jeans equation of the untruncated NFW halo.
- Bracket H-src: the source's fitted g_pot(u) = u / (0.08 + u) / (1 + 2.5 u^1.5), with u = r / R500.

**The daughter.** Onset and rate are G's, so the H-core kick is G's: 4 v_stiff.

**The real question is whether daughters stay bound.** A daughter made at r has mean specific energy
E = (1/2)(3 sigma(r)^2 + v_kick^2) + Phi(r). Phi is the pre-conversion halo's own potential:
- SIS truncated at R200: Phi = -V^2 (1 + ln(R200 / r));
- NFW: -(G M200 / mu(c)) ln(1 + r / r_s) / r.

Daughters with E < 0 stay in the system and are counted at their creation radius (no re-expansion: generous, disclosed).
Daughters with E >= 0 leave. Reported beside H-core: the bound fraction at kick v_stiff and at 2 v_stiff, for galaxy, group
and cluster halos.

**Members** (Coma UDGs, UMa members): their own halo only. H defines no bath.

**Form choices beside the label.**
- H-core: the 1/pi factor, the exponential escape law, and G's choices (the cube root, the kick factor 4, 4 pi).
- H-full additionally: the resonant window, the 180 kpc puff core, and the kick factor 2.

Fitted constants: 0 in H-core. H-full's 180 kpc and the window edge are the source's choices, recorded.

## 2. H-full (bracket, named added form choices, graded and labelled beside H-core but never replacing it)

As H-core, but:
- **Resonant window:** conversion happens only in halos with v_vir > v_stiff / 2.
- **Halos below the window** keep their component, puffed to a fixed core: M_chi(<r) = M_chi0 r^3 / (r^2 + (180 kpc)^2)^(3/2)
  (the WD1 form).
- **Kick** 2 v_stiff (532 / 576 km/s), with the bound-daughter rule as in H-core.

## 3. Gates, lines, label

SS1 A2's gates and lines unchanged:
- 1 KiDS
- 2 groups
- 3 X-COP
- 4 UDGs (reported)
- 5 SPARC
- 5b UMa
- 6 background (mass kept)
- 7(b) lensing (NO VERDICT: no validated method, A and SS2)
- 8 forest + fsigma8
- 9 Bullet (DB1)
- 10 Cassini

In the cosmology, the escaping (unbound) converted mass is the non-clustering fraction above k = 1/lambda, with lambda the
streaming length at the kick. Bound daughters keep clustering.

**Reported:**
- group retention inside R500 against the source's 42-48 % at M500 2.1e13 and 79-82 % at 1.4e14, and the repair band
  30-85 %;
- X-COP retained / M_dyn against TR1;
- TR1's SHAPE statistic;
- the converted cosmic fraction against the source's 16 %;
- sigma8 / S8 against the source's 0.766-0.771 / 0.78;
- the KiDS shift at 0.3, 1, 1.5 Mpc against the source's < +0.035;
- SPARC outer points (H-full puff).

**Label.** Per footing, A's rule (first failing gate in the order 1, 2, 3, 5, 5b, 6, 7b, 8, 9, 10), for H-core and for H-full
separately.

## 4. Known answers

- **KA-H1:** the escape law for an SIS: f = exp(-(2 alpha / pi)(v_stiff / v_vir)^2) evaluated by the code against the formula,
  to 1e-12.
- **KA-H2:** law-only replay (component -> 0).
- **KA-H3:** at M500 2.1e13 and 1.4e14 (z 0.05, 500 rho_c, on the footing's v_stiff) the H-core SIS retention is printed
  beside the source's claims.

  Hand estimate, before any number: v_vir 393 and 742 km/s at the canonical footing give f = exp(-2.78 (265.8 / v)^2) =
  0.28 and 0.70. The low end sits below the source's 42-48 %, because the source's g_pot exceeds 0.5 in the middle.

## 5. MUTATE

- **MH1:** v_stiff -> 0 (no conversion). KiDS or SPARC must FAIL.
- **MH2:** kick -> 0 (every daughter bound). gate 8 must move toward PASS, or its numbers must improve; otherwise NO BITE.

## 6. Hand estimates (before any number)

- **H-core, small halos:** galaxy halos (v_vir 100-250) give f ~ e^-3 to e^-20, so they convert almost entirely.
- **H-core, bound daughters:** with kick 4 v_stiff about 1100 km/s and v_esc < 700 everywhere below clusters, nothing below
  groups stays bound. Growth FAILS as in G.
- **H-core, groups and X-COP:** groups (v 400-880) keep 0.28-0.9: the amount may now fall inside the need. X-COP keeps
  0.75-0.9 uniformly; its shape follows TR1 (as SS2 found) and its amount may pass.
- **H-full:** kick 2 v_stiff about 550 km/s binds daughters only in halos with v_vir above about 250-300. Dwarfs below 133 km/s
  puff to 180 kpc, so the KiDS low bins and SPARC outer points feel a WD1-type core: expect a KiDS shift > 0.05 in the low
  bins.
- **Bullet:** keeps about 0.9 (main) and 0.7 (sub) uniformly; DB1's offset rule may still FAIL.

## 7. Operational

- Disk at about 4 GiB: outputs small. H runs only the primary set plus the NFW bracket in the local gates; no Moster
  rerun (it is reported from G's KiDS result).
- ss1v.py gains the H branch. All outputs carry the "_VH*" tag. Results go in RESULT_H.md.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
