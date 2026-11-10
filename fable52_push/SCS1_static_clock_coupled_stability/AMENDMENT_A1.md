# SCS1 AMENDMENT A1 (post hoc; committed alone, before any graded run)

TEST lane. Adopts nothing. kappa = 1/2 FITTED; not theory closed.

**What changes.** Route 1's growth rate is computed from the **Hermitian part** of the WKB symbol for real omega,
M_H(omega) = [M(omega) + M(omega)^dagger]/2, instead of from the full complex symbol. This generalises TPA1 item 6, which
used Re P for its 1x1 symbol (the criteria say route 1 is "as TPA1 item 6"). The antihermitian part comes from the
coefficient gradients. At leading WKB order it is amplitude transport (energy-flux conservation), not growth. It is
reported for every row as a diagnostic, with the growth that the full symbol would give beside it, and no label rests on
it. Nothing else changes: no line, grid, known answer, MUTATE arm or label rule.

**Why, and what was seen first (post hoc).** Before freezing this I ran one probe background: the primary configuration,
log M_b 10.45 at 30 kpc, canonical, kr 10 / 1e3 / 1e5, radial and tangential. The Hermitian dispersion there is positive
(omega^2 = 1.115e-7 radial and 4.98e-8 tangential, in units of 1/r^2), and it matches the hand closed form to 1e-7 at
kr 1e5. The full symbol adds Im(omega^2) = 2.05e-8, 2.05e-10 and 2.05e-12 at kr 10, 1e3 and 1e5, falling as 1/(kr)^2, on
radial modes only. Read literally, the frozen rule ("no growing root: Gamma below 1e-6 of the local free-fall rate") would
count that transport term as growth at kr 10 and 1e3, and the ratio rule would then misfile a stable point as JEANS-ONLY.

**Not affected.** KA2 (flat background, no gradients). Route 2's global radial eigensolve, which has no WKB transport term
and decides independently whether any lambda < 0.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
