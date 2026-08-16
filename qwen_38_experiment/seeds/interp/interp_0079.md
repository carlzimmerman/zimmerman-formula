# interp_0079 -- the single shared dimensionless number

Seed 0079 is a random collision of three facts. Read charitably as ONE conjecture:
there is a single dimensionless number, sigma, that BOTH bullets independently
encode, and sigma sets the transition index z_t.

## Conjecture (the wildcard)
sigma = 0.108  (dimensionless; the pi-free residual, in dex, of the RAR at Ups=0.70).
The two bullets are two independent readings of this ONE number.

## Bullet 1 -- RAR side
- The RAR at Ups = 0.70 carries a 0.108-dex offset.
- Claim: that offset has a pi-free part; strip the pi-dependent term and the
  residual left is exactly sigma = 0.108 dex.
- "measured by m_mu/m_e = 206.77": sigma must be reproducible from the mass
  ratio alone, sigma = f(206.768) for some NAMED simple function f.
  Constraint to satisfy: f(206.768) = 0.108 (e.g. a candidate is
  f(x) = (log10 x - 2)/pi = 0.100; or f(x) = 10^(-0.108)/1.08 = 0.722 --
  to be fixed). If f cannot be a simple named function, the reading is a
  CONVENTION fit, NOT a hit (do not count it).

## Bullet 2 -- CKM side
- "Averaging over structure of the CKM CP phase (~1.14 rad)" yields sigma.
  Candidate: sigma = (1 - cos delta)/pi or sigma = delta/10.56 with delta ~ 1.14 rad;
  the structure-average must equal 0.108.
- That sigma sets the transition z_t = nu0^(-1/3) - 1, predicted to land in
  [17, 35]. (nu0 is the dimensionless reference frequency; z_t is dimensionless.)

## Exact test
1. RAR: from the framework's RAR formula at Ups=0.70, subtract the pi term;
   assert the residual offset = 0.108 dex to within +/- 0.003 dex.
2. Mass ratio: identify a simple f with f(206.768) = 0.108 within 3%.
   If no simple f exists -> Bullet 1 DEAD (convention, not hit).
3. CKM: average the CP phase over the CKM structure; assert it = 0.108 within 3%.
4. Transition: from sigma, compute z_t = nu0^(-1/3) - 1; assert 17 <= z_t <= 35.

## What kills it
- Any of (1)-(4) fails its tolerance -> DEAD.
- In particular: if the 0.108-dex offset is NOT pi-free (removing pi does not
  leave a 0.108 residual) the whole conjecture collapses.
- If f(m_mu/m_e) or the CKM structure-average is a tuned fit to 0.108 rather
  than a named function, it is a CONVENTION-grade match -> NOT a hit.
- If z_t falls outside [17,35], the bullet-2 reading is refuted.

## Footings
All quantities here are dimensionless (dex, mass ratio, phase, z_t, Ups), so
the dimensional footings 9.3619e-11 / 1.1279e-10 do not apply. Flagged N/A.

## Status
Ungraded. Single-number unification is the conjecture; the sub-tests are the
falsification. Referee should check (1)-(4) independently and refuse to count
any f that is not a named function.
