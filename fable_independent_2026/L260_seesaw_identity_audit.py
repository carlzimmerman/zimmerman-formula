#!/usr/bin/env python3
"""L260 -- H019 "THE FORMULA IS THE SEESAW", AUDITED ON ITS OWN TERMS.  H019 (hy4, 09-15) claims: Z1 the identity
a0 = (1/2)c sqrt(G rho_L) = Lambda^2/(2 M_Pl) (ratio 1.0000000000000002); Z2 the 1/2 is 1/n with n = 2 the graviton's
transverse polarisation count (H017/H018); Z3 Lambda = sqrt(2 M_Pl a0) "predicted with no reference to rho_L"; Z4 dark
energy IS f(0) = -1; Z5 one input scale.  Each is tested below; measurement and threshold stated separately; a FAIL is
the finding.  Both footings where a dimensional number appears."""
import os, re, math, sympy as sp
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(HERE)
G, c, hbar, eV = 6.67430e-11, 2.99792458e8, 1.054571817e-34, 1.602176634e-19
H0 = 67.4e3/3.0856775814913673e22; rho_L = 0.685*3*H0**2/(8*math.pi*G)
CH = []
def check(n, ok, d): CH.append(bool(ok)); print(f"  [{'PASS' if ok else 'FAIL'}] {n}\n           ({d})")
print("L260 -- H019 audited\n")
# Z1: the identity holds for EVERY coefficient, so it selects nothing
k, Gs, rl = sp.symbols('kappa G rho_L', positive=True)
Lam, MPl = rl**sp.Rational(1, 4), 1/sp.sqrt(Gs)                       # the two DEFINITIONS H019 uses (hbar = c = 1)
resid = sp.simplify(k*sp.sqrt(Gs*rl) - k*Lam**2/MPl)
E_Pl = math.sqrt(hbar*c/G)*c**2; Lam_J = (rho_L*c**2*(hbar*c)**3)**0.25
ratios = {kk: (kk*c*math.sqrt(G*rho_L)*hbar/c)/(kk*Lam_J**2/E_Pl) for kk in (0.5, 1/3, 1/(2*math.pi), 0.461)}
print(f"    sympy: kappa sqrt(G rho_L) - kappa Lambda^2/M_Pl with rho_L := Lambda^4, M_Pl := 1/sqrt(G)  ->  {resid}")
print("    H019's 'ratio' recomputed for kappa = 1/2, 1/3, 1/2pi, 0.461: " + ", ".join(f"{v:.15f}" for v in ratios.values()))
check("Z1 [THE IDENTITY SINGLES OUT THE COEFFICIENT 1/2] the identity is checked symbolically with a free coefficient; it "
      "carries information about the 1/2 only if it fails for other coefficients",
      not (resid == 0 and all(abs(v - 1) < 1e-12 for v in ratios.values())),
      "residual is identically zero for every kappa: rho_L = Lambda^4 and G = 1/M_Pl^2 are the definitions of Lambda and "
      "M_Pl, so the 'seesaw' is the same formula in different units. The 1.0000000000000002 is a definition equalling "
      "itself. a0 ~ Lambda^2/M_Pl ~ c H0 ~ sqrt(G rho_L) is the single Milgrom (1983) coincidence written three ways")
# Z3: Lambda "predicted" from a0 -- with H019's a0 (built from rho_L) and with a galactic a0
src = open(os.path.join(REPO, "hy4_push", "H019_zimmerman_is_the_seesaw.py")).read()
builds = bool(re.search(r"a0_Z\s*=\s*0\.5\*c\*math\.sqrt\(G\*rho_L\)", src))
Lam_obs = Lam_J/eV*1e3
preds = {"H019 (a0 from rho_L)": 0.5*c*math.sqrt(G*rho_L), "L232 free-scale fit": 1.2457e-10, "McGaugh+2016": 1.20e-10}
print(f"    H019 computes its a0 from rho_L in-script: {builds};  observed Lambda = {Lam_obs:.4f} meV")
worst = 0
for nm, a0 in preds.items():
    L = math.sqrt(2*E_Pl*a0*hbar/c)/eV*1e3; miss = L/Lam_obs - 1; worst = max(worst, abs(miss)) if "H019" not in nm else worst
    print(f"    Lambda = sqrt(2 M_Pl a0) from {nm:22s} a0 = {a0:.4e}: {L:.4f} meV ({100*miss:+.1f}%; rho_L off by {100*((1+miss)**4-1):+.0f}%)")
check("Z3 [LAMBDA IS PREDICTED FROM a0 WITHOUT REFERENCE TO rho_L] the script's a0 is traced to its source, and the "
      "prediction is repeated with the two galactic a0 values on the record; it counts as a prediction only if a galactic "
      "a0 lands within 1% of the observed Lambda",
      (not builds) and worst < 0.01,
      f"the a0 H019 feeds in is computed from rho_L three lines earlier, so Z3 returns its input (the rung-9 circularity of "
      f"L258); an independent a0 misses Lambda by {100*worst:.0f}% (rho_L by ~70%): the coincidence holds at the 20-30% level, as always")
# Z4: f(0) is a zero mode of the static law
K, cc = sp.symbols('K c0', real=True); f = sp.Function('f')
static_eq_coeff = sp.diff(f(K) + cc, K)                                # the static equation div[f'(K) grad phi] = 4 pi G rho carries f' only
rho_vac = lambda F: (2*K*sp.diff(F, K) - F).subs(K, 0)                 # rho = Lambda^4 (2K f' - f) at K = 0
print(f"    static law depends on f through f'(K) only: d/dc0 of the coefficient = {sp.diff(static_eq_coeff, cc)};  "
      f"rho_vac(f + c0) - rho_vac(f) = {sp.simplify(rho_vac(f(K) + cc) - rho_vac(f(K)))} Lambda^4")
check("Z4 [f(0) = -1 IS FIXED BY THE THEORY] adding a constant to f must change either the static law or be forbidden; "
      "if the static law is unchanged and only the vacuum energy shifts, f(0) is a free integration constant",
      sp.diff(static_eq_coeff, cc) != 0,
      "f -> f + c0 leaves every galactic prediction untouched and shifts the dark energy by -c0 Lambda^4: this is the "
      "k01/L226 zero mode. 'Dark energy IS f(0) = -1' is the choice of that constant to match Planck, not a derivation")
# Z2: the deep slope of mu_n is n for every n, and the joint relation holds for every n
Y = sp.symbols('Y', positive=True); slopes = {n: sp.limit((1 - (1 + Y)**(-n))/Y, Y, 0) for n in (1, 2, 3, 4)}
print(f"    deep slope of mu_n(Y) = 1-(1+Y)^-n: {slopes};  H017's 'a0 M_Pl n = Lambda^2' with a0 := s/n holds for every n by definition")
check("Z2 [n = 2 IS DERIVED FROM THE GRAVITON'S POLARISATION COUNT] the slope of the family at n and the TT rank D(D-3)/2 "
      "are two integers; a derivation must produce the slope from the tensor sector, i.e. the static scalar equation must "
      "contain the polarisation count",
      any(v != n for n, v in slopes.items()),
      "the slope is n by construction of the family; the static equation div[f' grad phi] = 4 pi G rho contains no tensor "
      "polarisation at all (the TT modes decouple from a static scalar source), so H018's 'one monopole, two helicities' "
      "identifies two unrelated 2s. The programme's own theorems stand: kappa is a zero mode (k01/L226), no monotone kernel "
      "fixes it (L227), a factor of 2 in a parameter-free shape is a free parameter (L230); n = 2 remains SELECTED BY DATA (L232/L259)")
# Z5: literal-True
lit = len(re.findall(r"\n\s*True,\s*\n", src))
check("Z5 [NO LITERAL-TRUE CHECKS] the H019 source is scanned for pass conditions that are the literal True",
      lit == 0, f"{lit} literal-True check (Z5 itself); the 'one input scale' count also omits n, kappa, Omega_dm, the cluster and "
      f"Milky-Way dust normalisations, and the choice of the mu_n family")
print(f"\nL260 COMPLETE: {sum(CH)}/{len(CH)} checks PASS.  READING: H019 is the rung-9 circularity in natural units; nothing in it "
      "changes PAPER29 v2 or the G03 spec.")
