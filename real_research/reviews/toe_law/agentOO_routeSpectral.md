# agentOO — ROUTE 2 (SPECTRAL / KRAMERS-KRONIG): does the dS / Gibbons-Hawking bath FORCE sigma4 < 0?

**The single question.** The free khronon dispersion is strictly convex (NN/MM: omega'' = ab/(a+bk^2)^{3/2} > 0,
no fold). The generator needs a NEGATIVE induced k^4 (bending) with a +k^6 stabilizer in
omega^2_eff(k) = c_chi^2 k^2 + sigma4 k^4 + sigma6 k^6. The only admissible source is the ACTIVE pump = the
khronon's coupling to the de Sitter HORIZON BATH (Gibbons-Hawking T_dS = H/2pi, occupation
n(w) = 1/(e^{2pi w/H} - 1); X2's pumped reservoir). **Route 2 asks: from the SPECTRAL representation alone, does
the SHAPE of the dS bath spectral density (its IR/UV weighting, its peakedness) FORCE the sign of the induced
k^4 — bending (roton, -> Airy) or stiffening (convex, -> MM kill stands)?** Condensed-matter precedent: a
PEAKED/STRUCTURED bath response gives the roton bend (He-II); a FEATURELESS thermal bath stiffens.

**Coefficient quarantine.** This round is about the SIGN and STRUCTURE of sigma4 only. zeta-tilde, (16pi/3)^{1/4},
q=1/4 stay quarantined and DOWNSTREAM. q=1/4 is NOT asserted anywhere.

**Both-ways honesty, maximum hostility** (framework-favorable = maximum stakes). sigma4_sign is COMPUTED, not chosen.

---

## Setup: the spectral / Kramers-Kronig structure of the induced self-energy

The khronon chi couples to the dS horizon bath. The one-loop in-medium self-energy is the
convolution of chi's propagator with the bath spectral density. The standard microscopic
realization (canonical passive linear bath = khronon linearly coupled to a continuum of horizon
oscillators of frequency W, derivative/momentum coupling) gives an EXACT renormalized dispersion
as the root of a secular equation. Define the bath moments

   I_n = int_0^inf dW J(W) / W^(2n),   J(W) = (coupling form factor) x (GH spectral density) >= 0

with J >= 0 forced by passivity (X2's vacuum-passivity sign, Im response >= 0). The GH spectral
density carries the thermal KMS factor coth(pi W / H) forced by T_dS = H/2pi.

---

## COMPUTED RESULTS (3 independent derivations, all convention-free)

### Block 3a — EXACT secular dispersion (no expansion-convention freedom). File: `agentOO_block3_concrete.py`
Integrating out the passive bath exactly, omega^2(k) = c_chi^2 k^2 + sigma4 k^4 + sigma6 k^6 with

   c_chi^2 = c0^2 - I1
   **sigma4 = - I2 * c_chi^2**                          (I2 > 0, c_chi^2 > 0  =>  sigma4 < 0)
   sigma6  = c_chi^2 * (I2^2 - I3 * c_chi^2)

**The bending sign is GENERIC and convention-free:** sigma4 < 0 whenever I2 = int J/W^4 is finite
and positive. This is the level-repulsion sign of integrating out ANY passive bath. (Block 1's
D=1/(W^2-x^2) guessed this sign; Block 2's naive even-KK kernel guessed the OPPOSITE; the EXACT
eigenvalue problem settles it as BEND. Both guesses recorded and the exact result overrules.)

**Spot-check (Block 7b):** a single-mode exact secular solve (direct quadratic root, no series)
gives sigma4 = -0.0019403, matching -I2 c_chi^2 = -0.0019402 to 1e-7. Bending sign reproduced a
3rd independent way.

### Block 4 — the ACTUAL Gibbons-Hawking spectrum. File: `agentOO_block4_GHspectrum.py`
GH spectral density J(W) = W^p coth(pi W/H). The curvature moments have NO convergent window:
- I2 (n=2) needs 4 < p < 3 for IR+UV convergence: **IMPOSSIBLE**.
- I3 (n=3) needs 6 < p < 5: **IMPOSSIBLE**.
The featureless GH bath is SCALE-FREE: a single power-law coupling cannot make both the IR and UV
curvature moments converge. The moments are always ENDPOINT/CUTOFF-controlled, never bath-controlled.

### Block 5 — peakedness classification (He-II roton vs featureless thermal). File: `agentOO_block5_peakedness.py`
- coth(pi W/H) is **strictly monotone decreasing** (d/dW = -pi/(H sinh^2) < 0): no resonance.
- W^p coth is **monotone** for every p: no interior peak, no maxon-roton double hump.
- The curvature integrand W^(p-4) coth is monotone: the bend contribution NEVER concentrates at a
  finite W0; it is always endpoint-dominated.
**The dS/GH bath is in the FEATURELESS class.** Its only scale H sets the TEMPERATURE (overall
weight), NOT a spectral PEAK position. He-II bends because its structure factor PEAKS at the roton
wavevector; the dS horizon bath has a monotone, peakless, scale-free thermal response.

### Block 6 — cutoff regularization (the both-ways rescue test). File: `agentOO_block6_cutoff.py`
With a physical UV cutoff Lambda making the moments finite:
- **sigma4 = -I2 c_chi^2 < 0 for EVERY cutoff** — the bending sign survives regularization. The
  featurelessness does NOT flip sigma4; it makes its MAGNITUDE cutoff-controlled.
- The fold scale k* (where omega''(k*)=0) is set by the ratio |sigma4|/sigma6 = bath moments =
  CUTOFF-controlled. k* MOVES with the coupling/cutoff and is NOT pinned to the sonic edge b->c_chi.
  NN's edge-coincidence tuning (condition 2) is **NOT discharged** by the dS spectrum.

### Block 7 — the stabilizer floor sigma6. File: `agentOO_block7_reconcile.py`
sigma6 = c_chi^2 (I2^2 - I3 c_chi^2) > 0 requires I2^2 > I3 c_chi^2, i.e. I2^2 near its
Cauchy-Schwarz ceiling I1 I3 (equality only for a delta-like SHARP resonance). For the GH bath:

   ratio I2^2/(I1 I3) = 0.043 (p=2,Lam=5) ... 0.003 (p=2,Lam=100) ... 1e-8 (p=3,Lam=100)

**ratio << 1: the GH bath sits FAR below the resonance ceiling => sigma6 < 0 (NO +k^6 floor).**
The induced fold would be UNBOUNDED (omega^2 -> -inf at large k). A bounded healthy roton fold
needs ratio -> 1, i.e. a SHARP spectral PEAK — exactly the He-II structured-bath signature the dS
bath lacks.

---

## VERDICT — FOLD-POSSIBLE-COUPLING-DEPENDENT (the sign is forced; the STRUCTURE is not supplied)

Split cleanly, both-ways honest:

**The SIGN is framework-FAVORABLE and reported as such.** sigma4 < 0 (negative-bending) is FORCED
by passivity + the dS-bath structure, NOT a free coupling choice. The Gibbons-Hawking spectrum is a
PASSIVE bath (J >= 0), and integrating out ANY passive bath via the exact secular equation gives
the level-repulsion sign sigma4 = -I2 c_chi^2 < 0. This is robust to cutoff and reproduced 3
independent ways (exact series, single-mode exact, moment rule). The bending DIRECTION the roton
needs IS the generic direction the dS bath pushes.

**The STRUCTURE needed for a controlled Airy fold is NOT supplied by the dS spectrum** (this is the
hostile truth, equal weight):
1. **Featureless / scale-free** (Blocks 4,5): no convergent curvature-moment window; monotone,
   peakless response. The dS bath is the STIFFENING/featureless CM class, NOT the He-II
   structured/peaked class. The bend magnitude is cutoff-controlled, not bath-controlled.
2. **No +k^6 stabilizer** (Block 7): sigma6 = c_chi^2(I2^2 - I3 c_chi^2) < 0 for the GH bath
   (ratio I2^2/(I1 I3) << 1, far from the resonance ceiling). The fold is UNBOUNDED — a runaway,
   not a controlled roton minimum. A healthy floor needs a SHARP peak the dS bath does not have.
3. **Fold not pinned to the edge** (Block 6): k* is cutoff-set, free, NOT tied to b->c_chi. NN's
   edge-coincidence tuning remains undischarged.

**forced_or_free:** the SIGN (negative-bending) is FORCED by the dS-bath/passivity structure — not
a coupling choice. But the three STRUCTURAL ingredients of a controlled, edge-pinned Airy fold
(finite bath-set curvature, a +k^6 floor, edge coincidence) are NOT forced by the GH spectrum; they
require additional structure (a sharp spectral peak / an internal scale) that the featureless dS
bath lacks. So: bending sign forced YES; controlled bounded edge-pinned fold forced NO.

**Relation to MM/NN:** This does NOT revive MM's kill on the sign axis — the dS bath genuinely
pushes in the bending direction, which is real progress and the framework-favorable truth. But it
does NOT deliver NN's named operator either: the featureless GH spectrum supplies neither the +k^6
stabilizer nor the edge-coincidence, and gives an unbounded (runaway) rather than a controlled
roton fold. The bend is structurally available in SIGN but not in CONTROLLED FORM from the dS
spectrum alone. NN's roton operator still needs an internal-scale / peaked-response input the bare
Gibbons-Hawking bath does not carry.

**Next calc:** test whether a STRUCTURED dS coupling (a horizon form factor with an internal scale
— e.g. a quasinormal-mode resonance in the horizon response, which IS peaked, vs the smooth
thermal continuum) can simultaneously (a) keep sigma4 < 0, (b) lift sigma6 > 0 (push I2^2 toward
the Cauchy-Schwarz ceiling), and (c) pin k* to b->c_chi. If the dS horizon's QNM spectrum supplies
the peak, the controlled fold becomes available; if only the smooth GH continuum is present, the
fold stays unbounded and the Airy normal form is not delivered.

