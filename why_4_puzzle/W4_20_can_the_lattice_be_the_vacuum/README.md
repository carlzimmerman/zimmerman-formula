# W4-20: can the touching-horizon lattice be the vacuum?

**Verdict: THE LATTICE ½ CANNOT BE THE VACUUM.** The record's only π-free ½ (W4-18 B7) is closed as a route to ρ_DE.
**κ = ½ stays FITTED.** Not theory closed.

W4-18 found that a simple-cubic lattice of masses whose horizons touch has a single-neighbour pull of exactly (c/2)√(Gρ). The
caveat was that it is a dust lattice. This lane tests whether any lattice can carry the vacuum's w = −1 instead (criteria
5d7db2b16).

| item | classical result | finding |
|---|---|---|
| V1 | von Laue: a static self-bound body has ∫T^{ij}dV = 0 | A ball of vacuum held static by a shell needs a **compressive** shell (γ = −ρc²R/2). Its trace vanishes, so it gravitates with **positive** active mass 4πR²(Rρc² + 3σ_s)/(3c²). A lattice of such elements has w_eff = 0: dust, whatever is inside. |
| V2 | give each element an isotropic w instead | κ²(w) = (1+3w)/4. A horizon needs w > −1/3. At w = −1 the active mass is −2m, there is no horizon, and "touching" is undefined. |
| V3 | frozen brane networks ("solid dark energy", w = −p/3) | A point (w = 0) pulls Gm/r², π-free. A Nambu–Goto string (w = −⅓) has **zero** active density and no Newtonian pull, only a deficit angle 8πGμ/c². A wall (w = −⅔) has active density −σ and pushes with 2πGσ, which carries π. **No w < 0 element has a π-free pull.** |

## What this says

- **A π-free pull needs bare G from a point-like source.** Point-like sources gravitate as dust:
  - wrapping vacuum in a wall makes it dust (von Laue);
  - extended relativistic sources (strings, walls, and the space-filling vacuum itself) either cancel their Newtonian pull
    or bring Gauss's π back.
- The ½ of W4-18 is therefore a property of dust lattices. It cannot be the dark-energy density's own coefficient.
- With this, every π-free route in the record is either a free portal (CFG911's ξ) or this closed lattice.

## Checks and controls

- **K1–K4 and I1 pass** (5/5):
  - K1: the von Laue trace is zero at the force-balanced γ.
  - K2: a bare vacuum ball has Komar mass −2ρV.
  - K3: the Gauss fields of a point, a line and a sheet.
  - K4: V2 at w = 0 reproduces W4-18's ½.
- **MUTATE (`W4_20_MUTATE=1`) bites on all three** (exit 1 by design):
  - MU1: with no shell the element is not dust and its active mass is negative.
  - MU2: a non-relativistic string regains the π-free 2Gλ/r, but at w = 0.
  - MU3: at w = 0 the touching condition and ½ return.

`FROZEN_CRITERIA.md`, `w4_20.py`, `w4_20.out`, `w4_20_MUTATE.out`, `w4_20_results*.json`. Run from the repo root:
`python3 why_4_puzzle/W4_20_can_the_lattice_be_the_vacuum/w4_20.py`.
