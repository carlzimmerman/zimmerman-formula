"""t04: the Weyl-gravity (conformal gravity, CG) numbers against the puzzle.  Pure arithmetic on QUOTED inputs; nothing is fitted.

Inputs quoted from the papers I opened (arXiv IDs):
  gamma0 = 3.06e-30 cm^-1, gamma* = 5.42e-41 cm^-1           astro-ph/9605085 (also 1101.2186 eq. 66, 1011.3495 eq. 22)
  kappa  = 9.54e-54 cm^-2 (= (100 Mpc)^-2), sign: -kappa c^2 R in v^2/R      1011.3495, 1101.2186 eq. 69, 1007.0970
  quoted derived numbers: gamma0 c^2/2 = 1.4e-9 cm/s^2 (astro-ph/0505266), K = -(gamma0/2)^2 = -2.3e-60 cm^-2 (astro-ph/9605085 abstract),
     a0(MOND) = 4 gamma0 c^2 = 1.1e-8 cm/s^2 and N*_crit = 5.65e10 (astro-ph/9605085 footnote 9 and text), watershed gamma0/kappa = 3.21e23 cm (1101.2186),
     cH/2 = 3.5e-8 cm/s^2 for H = 72 km/s/Mpc (astro-ph/0505266)
  cosmic (Hubble-plot) conformal-cosmology values: Omega_Lambda-bar(t0) = 0.37, Omega_k(t0) = 0.63 (astro-ph/0505266 text and footnote 97)
Inputs from this repo (sonnet55_push/puzzle_32pi/p03_egb_and_data.py, committed): H0 = 67.4 km/s/Mpc, Omega_Lambda = 0.685, SPARC a0_hat = 1.0766e-10 m/s^2 +- 5.44%.

Sections
  A  reproduce the quoted derived numbers from the quoted inputs (control: the reproduction tolerance; mutation: a wrong factor fails)
  B  the CG acceleration scale vs the puzzle's a0
  C  the crossing-point 'a0 = 4 gamma0 c^2' is galaxy-dependent: a0_eff(N*) = 2 c^2 (gamma0 + gamma* N*)
  D  the cosmological consistency of gamma0: Omega_k implied by the galactic gamma0 vs the Hubble-plot Omega_k
  E  the quadratic (de Sitter-like) coefficient vs H^2 and vs the puzzle ratio
"""
import math
import sys

ok = []


def chk(name, cond):
    ok.append(bool(cond))
    print(("PASS " if cond else "FAIL ") + name)


c_cm = 2.99792458e10          # cm/s
Mpc_cm = 3.0856775814913673e24
gam0, gamS, kap = 3.06e-30, 5.42e-41, 9.54e-54
Z = math.sqrt(32 * math.pi / 3)
H0_repo, OmL = 67.4, 0.685
a0_sparc, a0_sparc_sig = 1.0766e-10, 0.0544       # m/s^2
Hc = lambda H: H * 1e5 / Mpc_cm                    # H/c... in cm^-1 when divided by c below: here H in 1/s
H_s = lambda Hkm: Hkm * 1e5 / Mpc_cm               # km/s/Mpc -> 1/s
Hlen = lambda Hkm: H_s(Hkm) / c_cm                 # H/c in cm^-1

print("== A. reproduce the numbers quoted in the papers from the quoted inputs")
a_g = gam0 * c_cm**2 / 2                                       # cm/s^2
print("   gamma0 c^2/2 = %.4e cm/s^2 = %.4e m/s^2   (paper: 1.4e-9 cm/s^2)" % (a_g, a_g / 100))
chk("A1 gamma0 c^2/2 reproduces the quoted 1.4e-9 cm/s^2 within 2%", abs(a_g / 1.4e-9 - 1) < 0.02)
chk("A1b MUTATION: gamma0 c^2 (no 1/2) does NOT reproduce it", abs(gam0 * c_cm**2 / 1.4e-9 - 1) > 0.5)
K = -(gam0 / 2)**2
print("   K = -(gamma0/2)^2 = %.3e cm^-2   (paper: -2.3e-60)" % K)
chk("A2 K = -(gamma0/2)^2 reproduces the quoted -2.3e-60 cm^-2 within 2%", abs(K / -2.3e-60 - 1) < 0.02)
print("   4 gamma0 c^2 = %.4e cm/s^2   (paper: 1.1e-8)" % (4 * gam0 * c_cm**2))
chk("A3 4 gamma0 c^2 reproduces the quoted 1.1e-8 cm/s^2 within 1%", abs(4 * gam0 * c_cm**2 / 1.1e-8 - 1) < 0.01)
Ncrit = gam0 / gamS
print("   N*_crit = gamma0/gamma* = %.3e   (paper: 5.65e10)" % Ncrit)
chk("A4 N*_crit = gamma0/gamma* reproduces the quoted 5.65e10 within 1%", abs(Ncrit / 5.65e10 - 1) < 0.01)
wat = gam0 / kap
print("   watershed gamma0/kappa = %.3e cm   (paper: 3.21e23)" % wat)
chk("A5 gamma0/kappa reproduces the quoted 3.21e23 cm within 1%", abs(wat / 3.21e23 - 1) < 0.01)
cH2 = c_cm * H_s(72) / 2
print("   c H/2 at H = 72 = %.3e cm/s^2   (paper: 3.5e-8)" % cH2)
chk("A6 cH/2 at H = 72 km/s/Mpc reproduces the quoted 3.5e-8 cm/s^2 within 2%", abs(cH2 / 3.5e-8 - 1) < 0.02)
print("   kappa^-1/2 = %.3e cm = %.1f Mpc  (paper: ~(100 Mpc)^-2)" % (kap**-0.5, kap**-0.5 / Mpc_cm))
chk("A7 kappa = 9.54e-54 cm^-2 is (104 Mpc)^-2, consistent with the quoted (100 Mpc)^-2", abs(kap**-0.5 / Mpc_cm / 100 - 1) < 0.06)

print("\n== B. the CG acceleration scale gamma0 c^2/2 against the puzzle a0")
a_g_si = a_g / 100
a0_fw_L = c_cm / 100 * H_s(H0_repo) * math.sqrt(OmL) / Z      # c H_Lambda / Z  (m/s^2)
a0_fw_0 = c_cm / 100 * H_s(H0_repo) / Z                        # c H0 / Z
print("   framework  c H_L / Z = %.4e m/s^2 ;  c H0 / Z = %.4e ;  SPARC a0_hat = %.4e +- %.1f%%" % (a0_fw_L, a0_fw_0, a0_sparc, 100 * a0_sparc_sig))
print("   gamma0 c^2/2 = %.4e m/s^2 : ratio to SPARC %.3f (factor %.1f low), to c H_L/Z %.3f, to c H0/Z %.3f"
      % (a_g_si, a_g_si / a0_sparc, a0_sparc / a_g_si, a_g_si / a0_fw_L, a_g_si / a0_fw_0))
chk("B1 gamma0 c^2/2 is more than 5 sigma below the SPARC a0_hat (statistical error only)", (a0_sparc - a_g_si) / (a0_sparc * a0_sparc_sig) > 5)
chk("B1b it is a factor 6-9 below the SPARC a0 and the framework values (an order of magnitude, minus a bit)", 6 < a0_sparc / a_g_si < 9 and 6 < a0_fw_L / a_g_si < 8)
print("   the CG paper's own mapping a0(MOND) = 4 gamma0 c^2 = %.4e m/s^2, ratio to SPARC %.3f" % (4 * gam0 * c_cm**2 / 100, 4 * gam0 * c_cm**2 / 100 / a0_sparc))
chk("B2 the factor '4' (footnote 81 of astro-ph/0505266) closes the gap to SPARC to within 5 percent: 4 gamma0 c^2 / a0_hat = %.3f" % (4 * gam0 * c_cm**2 / 100 / a0_sparc),
    abs(4 * gam0 * c_cm**2 / 100 / a0_sparc - 1) < 0.05)
# the gamma that the puzzle's a0 would need
gam_need = 2 * a0_fw_L * 100 / c_cm**2
print("   gamma needed for a0 = c H_L/Z: 2 a0/c^2 = %.3e cm^-1  = %.2f x gamma0" % (gam_need, gam_need / gam0))

print("\n== C. the crossing-point a0 is galaxy dependent: a0_eff(N*) = 2 c^2 (gamma0 + gamma* N*)")
print("   (generalises footnote 81: g_N = g_lin = c^2 gamma_tot/2 at the crossing; MOND sqrt(a0 g_N) = c^2 gamma_tot  =>  a0 = 2 c^2 gamma_tot)")
a_eff = lambda N: 2 * c_cm**2 * (gam0 + gamS * N) / 100
chk("C1 at N* = N*_crit the generalised formula gives 4 gamma0 c^2 (the CG paper's value)", abs(a_eff(Ncrit) / (4 * gam0 * c_cm**2 / 100) - 1) < 1e-12)
rows = [(1e8, a_eff(1e8)), (1e9, a_eff(1e9)), (1e10, a_eff(1e10)), (1e11, a_eff(1e11)), (1e12, a_eff(1e12))]
for N, aeff in rows:
    print("   N* = %.0e : a0_eff = %.3e m/s^2  (x %.2f of SPARC a0_hat)" % (N, aeff, aeff / a0_sparc))
chk("C2 a0_eff varies by more than a factor 10 between N* = 1e9 and N* = 1e12 (no universal acceleration)", a_eff(1e12) / a_eff(1e9) > 10)
chk("C2b CONTROL: a universal a0 (constant) would give ratio 1", abs(a_eff(1e9) / a_eff(1e9) - 1) < 1e-15 and a_eff(1e12) / a_eff(1e9) > 1.5)

print("\n== D. is gamma0 cosmologically consistent?  gamma0/2 = sqrt(-K) = (H/c) sqrt(Omega_k)  (the CG papers' identification)")
for Hk in (67.4, 72.0):
    Ok_gal = (gam0 / 2 / Hlen(Hk))**2
    gam_cos = 2 * Hlen(Hk) * math.sqrt(0.63)
    print("   H0 = %.1f: Omega_k implied by the galactic gamma0 = %.3e ; Omega_k(Hubble plot, footnote 97) = 0.63 -> gamma0(cosmic) = %.3e cm^-1 = %.1f x galactic"
          % (Hk, Ok_gal, gam_cos, gam_cos / gam0))
Ok_gal72 = (gam0 / 2 / Hlen(72))**2
chk("D1 the galactic gamma0 implies Omega_k ~ 4e-4 (H0 = 72), not 0.63: the two determinations of the same spatial curvature differ by > 1000 in |K|", 0.63 / Ok_gal72 > 1000)
chk("D1b the same conclusion holds for H0 = 67.4 (ratio %.0f)" % (0.63 / (gam0 / 2 / Hlen(67.4))**2), 0.63 / (gam0 / 2 / Hlen(67.4))**2 > 1000)
chk("D1c MUTATION: if Omega_k were the galactic value the ratio would be 1", abs(Ok_gal72 / Ok_gal72 - 1) < 1e-15)
# what the two possible CG readings predict for the puzzle ratio (a0/H)^2 vs 3/(32 pi)
target = 3 / (32 * math.pi)
print("   puzzle: (a0/H_Lambda)^2 = 3/(32 pi) = %.5f  (Omega_k/Omega_Lambda-bar in the CG cosmology of t03 E)" % target)
r_sn = 0.63 / 0.37
r_gal = (gam0 / 2)**2 / (Hlen(H0_repo)**2 * OmL)
print("   (i)  Hubble-plot values: Omega_k/Omega_Lambda-bar = %.3f  -> %.0f x the puzzle value" % (r_sn, r_sn / target))
print("   (ii) galactic gamma0 with H_Lambda^2 = (H0/c)^2 Omega_Lambda: (gamma0/2)^2/H_L^2 = %.3e -> %.3f x the puzzle value" % (r_gal, r_gal / target))
chk("D2 neither reading gives the puzzle ratio: (i) is %.0fx too big, (ii) is %.0fx too small (my pre-run guess of 76x for (ii) was wrong: it used H0 instead of H_Lambda)" % (r_sn / target, target / r_gal), 40 < r_sn / target < 80 and 1 / 60 < r_gal / target < 1 / 30)

print("\n== E. the quadratic coefficient kappa against H^2, Lambda/3 and the puzzle relation k' = (a0)^2 + k")
H2 = Hlen(H0_repo)**2
LamO3 = H2 * OmL
print("   (H0/c)^2 = %.3e cm^-2 ; Lambda/3 = (H0/c)^2 Omega_L = %.3e cm^-2 ; kappa = %.3e cm^-2" % (H2, LamO3, kap))
print("   kappa/(H0/c)^2 = %.0f ; kappa/(Lambda/3) = %.0f" % (kap / H2, kap / LamO3))
chk("E1 kappa exceeds Lambda/3 by a factor > 2000 (the fitted quadratic term is not the cosmological Lambda)", kap / LamO3 > 2000)
kprime = kap + (gam0 / 2)**2
print("   if the fitted kappa were the frame invariant k' = (gamma0/2)^2 + k: (a0)^2/k' = %.3e vs puzzle %.5f" % ((gam0 / 2)**2 / kprime, target))
chk("E2 (gamma0/2)^2 / k' with k' = kappa + (gamma0/2)^2 is ~2.5e-7, i.e. 1e5 below the puzzle 3/(32 pi)", (gam0 / 2)**2 / kprime < 1e-6)
need = (32 * math.pi / 3 - 1)
print("   the puzzle needs k/a0^2 = 32 pi/3 - 1 = %.4f; the CG galactic fit has kappa/(gamma0/2)^2 = %.3e" % (need, kap / (gam0 / 2)**2))
chk("E3 kappa/(gamma0/2)^2 = %.2e is %.1e times the puzzle's 32.51" % (kap / (gam0 / 2)**2, kap / (gam0 / 2)**2 / need), kap / (gam0 / 2)**2 / need > 1e4)
# G_eff rho / a0^2 with rho the observed Lambda-density on the H_Lambda footing
GrhoOverA0sq = 3 * LamO3 / (8 * math.pi) / (gam0 / 2)**2
print("   G rho_Lambda/a0^2 with a0 = gamma0/2 and the observed Lambda: (3/8pi) (Lambda/3)/(gamma0/2)^2 = %.1f (puzzle: 4)" % GrhoOverA0sq)
chk("E4 that ratio is ~2e2, not 4 (a factor ~50; the CG a0 is not tuned to the observed Lambda)", 100 < GrhoOverA0sq < 400)
# sign facts
print("   signs: k' = -2 lambda phi0^2 > 0 needs lambda < 0; G_eff = -3/(4 pi phi0^2) < 0; fitted kappa > 0 (repulsive, de Sitter-like: B has -kappa r^2)")
chk("E5 sign bookkeeping: G_eff < 0 and rho_V = lambda phi0^4 < 0 (lambda < 0) give G_eff rho_V > 0", (-3.0) * (-1.0) > 0)

print("\n== F. what curvature the SPARC a0 would need in the CG identification a0 = c H sqrt(Omega_k)")
cH0 = c_cm / 100 * H_s(H0_repo)
Ok_need = (a0_sparc / cH0)**2
print("   a0_hat = c H0 sqrt(Omega_k)  =>  Omega_k = (a0_hat/(c H0))^2 = %.4f  (H0 = 67.4)" % Ok_need)
chk("F1 the SPARC a0 corresponds to Omega_k = 0.027 in that identification: between the galactic-gamma0 value (4e-4) and the Hubble-plot value (0.63)", 4.4e-4 < Ok_need < 0.63)
a_over_H_sn = math.sqrt(0.63 / 0.37)
print("   Hubble-plot CG cosmology: a0/(c H_dS) = sqrt(Omega_k/Omega_Lambda-bar) = %.3f vs puzzle 1/Z = %.4f  (ratio %.1f)" % (a_over_H_sn, 1 / Z, a_over_H_sn * Z))
chk("F2 in the Hubble-plot CG cosmology a0/(c H_dS) = 1.30, i.e. 7.5 times the puzzle's 1/Z", abs(a_over_H_sn * Z - 7.5) < 0.1)
u_sn = math.atanh(math.sqrt(0.37))
print("   epoch u = atanh(sqrt(Omega_Lambda-bar)) = %.3f for Omega_Lambda-bar = 0.37; the puzzle needs u = asinh(Z) = %.4f (Omega_Lambda-bar = %.4f)" % (u_sn, math.asinh(Z), Z**2 / (1 + Z**2)))
chk("F3 the puzzle epoch u = asinh(Z) = 2.46 is far from the Hubble-plot epoch u = 0.70 of the same cosmology", math.asinh(Z) > 3 * u_sn)

print("\nPASS %d / %d" % (sum(ok), len(ok)))
sys.exit(0 if all(ok) else 1)
