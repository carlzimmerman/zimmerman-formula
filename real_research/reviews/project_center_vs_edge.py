#!/usr/bin/env python3
"""
The microscopic crux: flat rotation curves REQUIRE de Sitter = the DSSYK spectral CENTER (not the edge).
======================================================================================================
The framework's deep-MOND derivation rests on the Narovlansky-Verlinde identification de Sitter = the DSSYK
spectral CENTER (E=0), where the density of states is FLAT. Rahman (2025, arXiv:2505.08116) instead derives
de Sitter-JT gravity at the spectral EDGE (E=E0), where the DSSYK density of states VANISHES as a square root
(the Schwarzian edge). This is the central contested input (project_the_wall.py). The question that settles
whether the framework's assumption is forced: does the observed MOND phenomenology require the center, or does
the edge work too?

THE CALCULATION. The DSSYK q-Gaussian density of states rho(E) on E in [-E0, E0] (E = E0 cos theta) has:
  * CENTER (E->0):  rho ~ |E|^0      -- FLAT, finite nonzero DOS (numerically confirmed: exponent ~ 0)
  * EDGE   (E->E0): rho ~ (E0-E)^1/2 -- SQUARE-ROOT edge, DOS vanishes (numerically confirmed: exponent ~ 0.53)
The framework maps the MOND interpolation mu(x) to the cumulative 'freezing' measure = integral of rho over the
energy window (~ the acceleration ratio x) AROUND the de Sitter spectral state. By calculus the cumulative
exponent m = (local DOS exponent) + 1:
  * CENTER: m = 1   (flat DOS integrates linearly)
  * EDGE:   m = 3/2 (sqrt DOS integrates as 3/2)
Then mu(x) = x^m with x = g_obs/a0 and mu(x) g_obs = g_bar gives g_obs ~ g_bar^p, p = 1/(m+1), and a point-mass
rotation curve V(r) ~ r^{(1-2p)/2}:
  * CENTER: p = 1/2 -> g_obs ~ g_bar^0.50, V(r) ~ r^0 = FLAT, BTFR V^4 ~ M           <-- the observed MOND
  * EDGE:   p = 2/5 -> g_obs ~ g_bar^0.40, V(r) ~ r^{+0.10} = RISING, no flat BTFR    <-- NOT observed

THE RESULT. Flat rotation curves and the BTFR slope 4 (g_obs ~ g_bar^0.50) REQUIRE the flat-center DOS. The
edge (Schwarzian) reading gives g_obs ~ g_bar^0.40 and RISING rotation curves -- excluded by the most basic
galactic fact. So, GIVEN the framework's emergent-gravity/DSSYK bridge, the very existence of flat rotation
curves is evidence that de Sitter = the DSSYK spectral CENTER (Narovlansky-Verlinde), not the edge (Rahman).

WHAT THIS BUYS. The framework's single most contested assumption (project_the_wall.py: de Sitter = center) is
turned from 'assumed' into 'data-favored': of the two live de Sitter-holography proposals, only the center is
consistent with galaxy dynamics. This (i) strengthens the deep-MOND SIGN derivation (flat DOS -> sqrt-law) and
(ii) shores up the FOUNDATION of the conditional coefficient result Z = 4 rho0(q)/sqrt(1-q) (which needs the
central DOS). It does NOT by itself fix Z, because the DSSYK coupling q remains free (q ~ 0.926 is then a
prediction, given the observed a0). HONEST CAVEAT: the discrimination is conditional on the framework's mapping
(MOND interpolation = cumulative chord-vacuum DOS, deep-MOND = near the de Sitter spectral state); it is a clean
implication of that structure, not an unconditional theorem. Needs numpy.
"""
import numpy as np

q = 0.90; K = 600; kk = np.arange(K); qk = q**kk; q2k = q**(2*kk)


def rhoE(th):
    c2 = np.cos(2*th)
    rt = np.prod(1-2*qk[None, :]*c2[:, None]+q2k[None, :], axis=1)
    return rt/np.sin(th)


def main():
    print("#"*94)
    print("# Microscopic crux: flat rotation curves REQUIRE de Sitter = the DSSYK CENTER, not the edge")
    print("#"*94 + "\n")

    print("="*94); print("DSSYK q-Gaussian density of states: local behaviour at center vs edge (q=0.90)"); print("="*94)
    thc = np.linspace(1e-4, np.pi-1e-4, 200001); Ec = np.cos(thc); rc = rhoE(thc)
    mC = (np.abs(Ec) > 1e-3) & (np.abs(Ec) < 3e-2) & (rc > 0)
    cexp = np.polyfit(np.log(np.abs(Ec[mC])), np.log(rc[mC]), 1)[0]
    th = np.logspace(-5, -1.2, 6000); rE = rhoE(th); ome = 1-np.cos(th); g = rE > 0
    eexp = np.polyfit(np.log(ome[g]), np.log(rE[g]), 1)[0]
    print(f"  CENTER E->0 : rho ~ |E|^{cexp:+.2f}      (analytic 0  -> FLAT, finite nonzero DOS)")
    print(f"  EDGE  E->E0 : rho ~ (E0-E)^{eexp:+.2f}   (analytic 0.5 -> SQUARE-ROOT edge, DOS vanishes)\n")

    print("="*94); print("Trace each de Sitter identification to a rotation curve"); print("="*94)
    print(f"  cumulative exponent m = (DOS exponent)+1; mu(x)=x^m; g_obs~g_bar^p, p=1/(m+1); V(r)~r^((1-2p)/2)")
    print(f"  {'reading':30}{'DOS exp':>9}{'m':>5}{'p':>6}{'V(r)':>10}{'curve':>9}")
    for nm, dos, m in [("CENTER flat (Narovlansky-Verl.)", 0.0, 1.0),
                       ("EDGE sqrt (Rahman/Schwarzian)", 0.5, 1.5)]:
        p = 1/(m+1); v = (1-2*p)/2
        print(f"  {nm:30}{dos:>9.1f}{m:>5.1f}{p:>6.2f}{('r^%+.2f'%v):>10}{('FLAT' if abs(v)<0.03 else 'RISING'):>9}")
    print()

    print("="*94); print("VERDICT"); print("="*94)
    print("""  OBSERVED: flat rotation curves, BTFR V^4 ~ M (g_obs ~ g_bar^0.50). This REQUIRES the flat-CENTER DOS
  (p=0.50, flat). The EDGE reading gives g_obs ~ g_bar^0.40 and RISING curves (V ~ r^+0.10) -- excluded by the
  most basic galactic fact. So, given the framework's emergent-gravity/DSSYK bridge, FLAT ROTATION CURVES ARE
  EVIDENCE that de Sitter = the DSSYK spectral CENTER (N-V), not the edge (Rahman).

  Consequence: the framework's most contested assumption (the wall) is now DATA-FAVORED -- of the two live de
  Sitter-holography proposals, only the center reproduces galaxy dynamics. This strengthens the deep-MOND sign
  derivation and the FOUNDATION of the conditional coefficient Z = 4 rho0(q)/sqrt(1-q), without by itself fixing
  Z (the coupling q stays free; q ~ 0.926 is then the prediction, given the observed a0). Conditional on the
  framework's mapping -- a clean implication of its structure, not an unconditional theorem.""")
    print("="*94)


if __name__ == "__main__":
    main()
