# QX2 iter 2: any universal interpolation (any J(Y) in the AQUAL class)
Frozen before code. Class: every static law g = nu(g_N/a0) g_N with a single-valued nu, i.e. any J(Y) in v3s's slot.
Class representative chosen by the data, not by fitting X-COP: nu_SPARC(y) = the binned median of g_obs/g_bar
from SPARC (real_research/data/sparc_data rotmod + SPARC_Lelli2016c.mrt; Q <= 2, inc >= 30 deg, errV/Vobs <= 0.1,
Upsilon_disk 0.5, Upsilon_bul 0.7, 0.1 dex bins in log y, bins with >= 20 points, log-linear interpolation),
with y = g_bar/a0 per footing.
- Graded 1: X-COP gate G-X with nu = nu_SPARC. X-COP points outside SPARC's y range are reported, not graded.
- Graded 2 (class statement): the per-bin excess E(y) = median log(M_HSE/M_b) for X-COP - log nu_SPARC(y). The
  class is DEAD if E > 0.15 dex (3 x HO1's mean line) in every bin shared by >= 3 X-COP points. Any single-valued
  nu matching SPARC to within its 0.054 rms in that bin then misses X-COP there by > 0.09 dex.
- Lean certifies the logic: with nu a function, equal y forces equal nu (no single nu serves two required values
  at one y).
MUTATE: plant nu_SPARC x 3 in the X-COP read. The gate mean must fall by > 0.4 dex (bites); the excess must vanish.
