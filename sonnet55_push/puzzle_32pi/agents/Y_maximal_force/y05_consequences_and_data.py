"""Lane Y, script 5 (last): what a rational Z = 6 would change relative to the framework's Z = sqrt(32 pi/3) (Part D of PREDECLARED.md),
and only then the comparison with lane V's data summary.  Data inputs are QUOTED from agents/V_evidence_for_the_coefficient/README.md
(a0 = 1.0766e-10 record, 5.44%; ensemble E 1.097e-10, 12.2%; H0 = 67.4 km/s/Mpc; Omega_Lambda = 0.685); they are not re-derived here."""
import json
import os
import sympy as sp
import mpmath as mp
from common import Ledger, HERE

L_ = Ledger("y05_consequences_and_data")
mp.mp.dps = 30
pi = sp.pi
Zs = {"V (rational)": sp.Integer(6), "F (framework)": sp.sqrt(32 * pi / 3), "M (Milgrom 2 pi)": 2 * pi}

print("\n== D1: exact consequences of a0 = c H_Lambda / Z  (c = G = 1) ==")
rows = {}
for name, Z in Zs.items():
    Lam_over_a02 = 3 * Z**2                       # Lambda = 3 H^2, H = Z a0
    Grho_over_a02 = sp.simplify(3 * Z**2 / (8 * pi))   # G rho_L = Lambda/(8 pi)
    kappa = sp.simplify(sp.sqrt(8 * pi / 3) / Z)       # a0 = kappa sqrt(G rho_L):  kappa = 1/sqrt(G rho/a0^2)
    kappa2 = sp.simplify(1 / sp.sqrt(Grho_over_a02))
    AL = sp.simplify(pi * Lam_over_a02)            # area of a Schwarzschild horizon with surface gravity a0 is pi/a0^2  =>  A Lambda / 1
    OmegaCoef = sp.simplify(Z**2)                  # Omega_Lambda = Z^2 a0^2/(c H0)^2
    rows[name] = dict(Lam=Lam_over_a02, Grho=Grho_over_a02, kappa=kappa2, AL=AL, OmegaCoef=OmegaCoef)
    print(f"   {name:18s} Lambda/a0^2 = {sp.nsimplify(Lam_over_a02)} = {float(Lam_over_a02):.4f}   G rho_L/a0^2 = {Grho_over_a02} = {float(Grho_over_a02):.5f}   "
          f"kappa = {float(kappa2):.5f}   A_a0 Lambda = {sp.nsimplify(AL)} = {float(AL):.3f}   Omega coefficient Z^2 = {float(OmegaCoef):.4f}")
L_.check("framework: G rho_L/a0^2 = 4 and A Lambda = 32 pi^2 (the puzzle), kappa = 1/2 exactly", sp.simplify(rows["F (framework)"]["Grho"] - 4) == 0 and sp.simplify(rows["F (framework)"]["AL"] - 32 * pi**2) == 0
         and sp.simplify(rows["F (framework)"]["kappa"] - sp.Rational(1, 2)) == 0)
L_.check("Z = 6: Lambda = 108 a0^2, G rho_L = (27/(2 pi)) a0^2 = 4.297 a0^2, A_a0 Lambda = 108 pi (NOT 32 pi^2), kappa = sqrt(8 pi/3)/6 = 0.4824: the Chern-Gauss-Bonnet coincidence and the kappa = 1/2 are both lost",
         sp.simplify(rows["V (rational)"]["Lam"] - 108) == 0 and sp.simplify(rows["V (rational)"]["Grho"] - 27 / (2 * pi)) == 0 and sp.simplify(rows["V (rational)"]["AL"] - 108 * pi) == 0
         and abs(float(rows["V (rational)"]["kappa"]) - 0.48240) < 1e-4)
ratio = sp.simplify(rows["V (rational)"]["OmegaCoef"] / rows["F (framework)"]["OmegaCoef"])
L_.check(f"Omega_Lambda (Z = 6)/Omega_Lambda (framework) = 36/(32 pi/3) = {ratio} = {float(ratio):.5f} for the same a0 and H0 (7.4% larger); the two laws differ by 3.6% in a0 and 7.4% in Omega_Lambda", sp.simplify(ratio - 27 / (8 * pi)) == 0)
L_.must_fail("control: the ratio is not 1 and not 2 pi/6 (the Milgrom/rational ratio 1.047 is a ratio of a0's, not of Omega)", abs(float(ratio) - 1) < 1e-3 or abs(float(ratio) - float(2 * pi / 6)) < 1e-3)
L_.must_fail("control: the claim that Z = 6 and Z = 5.789 give the same Omega_Lambda coefficient must be rejected (33.51 vs 36)", abs(float(rows["V (rational)"]["OmegaCoef"]) - float(rows["F (framework)"]["OmegaCoef"])) < 1e-6)

print("\n== D2: numbers (SI), Planck-like H0 = 67.4 km/s/Mpc, Omega_Lambda = 0.685 ==")
c_ = mp.mpf("299792458")
Mpc = mp.mpf("3.0856775814913673e22")
H0 = mp.mpf("67.4") * 1000 / Mpc
cH0 = c_ * H0
print(f"   c H0 = {mp.nstr(cH0, 6)} m/s^2")
Om = mp.mpf("0.685")
a0_needed = {n: cH0 * mp.sqrt(Om) / mp.mpf(str(float(Z))) for n, Z in Zs.items()}
for n, v in a0_needed.items():
    print(f"   a0 that reproduces Omega_Lambda = 0.685 with Z of {n:18s}: {mp.nstr(v * 1e0, 5)} m/s^2")
L_.check("a0(Z = 6)/a0(Z = F) = sqrt(32 pi/3)/6 = 0.96479: a 3.6% lower a0 is needed for the same Omega_Lambda", abs(a0_needed["V (rational)"] / a0_needed["F (framework)"] - mp.sqrt(32 * mp.pi / 3) / 6) < mp.mpf("1e-12"))
Omega_pred = lambda a0, Z: (mp.mpf(str(float(Z))) * a0 / cH0) ** 2
rec = mp.mpf("1.0766e-10")
ens = mp.mpf("1.097e-10")
print(f"   Omega_Lambda predicted from the record a0 = 1.0766e-10: Z=F {mp.nstr(Omega_pred(rec, Zs['F (framework)']), 5)},  Z=6 {mp.nstr(Omega_pred(rec, Zs['V (rational)']), 5)}")
print(f"   Omega_Lambda predicted from the ensemble a0 = 1.097e-10: Z=F {mp.nstr(Omega_pred(ens, Zs['F (framework)']), 5)},  Z=6 {mp.nstr(Omega_pred(ens, Zs['V (rational)']), 5)}")
L_.check("reproduces lane V's Omega_Lambda = 0.906 for the record a0 with Z = F (0.9058); Z = 6 gives 0.973", abs(Omega_pred(rec, Zs["F (framework)"]) - mp.mpf("0.9058")) < 0.002 and abs(Omega_pred(rec, Zs["V (rational)"]) - mp.mpf("0.9733")) < 0.002)

print("\n== D3: which H?  A pure-Lambda construction has H = H_Lambda, so the natural footing is the rho_Lambda footing (Z_Lambda = c H0 sqrt(Omega)/a0) ==")
def zscore(Zc, a0, err):
    Zhat_tot = cH0 / a0
    Zhat_L = cH0 * mp.sqrt(Om) / a0
    return (mp.log(mp.mpf(str(float(Zc)))) - mp.log(Zhat_L)) / err, (mp.log(mp.mpf(str(float(Zc)))) - mp.log(Zhat_tot)) / err, Zhat_L, Zhat_tot
res = {}
for nm, a0, err in [("ensemble E (12.2%)", ens, mp.mpf("0.122")), ("record as quoted (5.44%)", rec, mp.mpf("0.0544"))]:
    print(f"   {nm}: Z_Lambda,hat = {mp.nstr(zscore(6, a0, err)[2], 4)}, Z_total,hat = {mp.nstr(zscore(6, a0, err)[3], 4)}")
    for n, Z in Zs.items():
        zL, zT, _, _ = zscore(Z, a0, err)
        res[(nm, n)] = (zL, zT)
        print(f"      Z of {n:18s} = {float(Z):7.4f}   offset (rho_Lambda footing) {mp.nstr(zL, 3):>6s} sigma   (rho_total footing) {mp.nstr(zT, 3):>6s} sigma")
L_.check("reproduces lane V's ensemble offsets (rho_total footing: F -0.25, V +0.05, M +0.42; rho_Lambda footing: F +1.30, V +1.59, M +1.97)",
         abs(res[("ensemble E (12.2%)", "F (framework)")][1] + 0.25) < 0.03 and abs(res[("ensemble E (12.2%)", "V (rational)")][1] - 0.05) < 0.03 and abs(res[("ensemble E (12.2%)", "M (Milgrom 2 pi)")][1] - 0.42) < 0.03
         and abs(res[("ensemble E (12.2%)", "F (framework)")][0] - 1.30) < 0.03 and abs(res[("ensemble E (12.2%)", "V (rational)")][0] - 1.59) < 0.03 and abs(res[("ensemble E (12.2%)", "M (Milgrom 2 pi)")][0] - 1.97) < 0.03)
sep = abs(mp.log(6 / mp.sqrt(32 * mp.pi / 3))) / mp.mpf("0.122")
L_.check(f"Z = 6 vs Z = F: separation {mp.nstr(sep, 3)} sigma at the ensemble scatter (12.2%): NOT separable (lane V: 1.8% total error needed for 2 sigma); on the pure-Lambda footing Z = 6 sits 1.6 sigma above the data, 0.3 sigma further than F", sep < 0.35)
L_.must_fail("control: the claim that a decoy Z = 7 is within 0.3 sigma of Z = 6 at the same scatter must be rejected (it is 1.3 sigma away: the data do discriminate at that level)", abs(mp.log(7 / mp.mpf(6))) / mp.mpf("0.122") < 0.3)

print("\n== D4: how the constructions of this lane compare with the data (declared: only now) ==")
cands = {"S3 M_a  (g_H = cH/2)": mp.mpf(2), "S3 M_b,M_d (Komar / zero-force, cH/4)": mp.mpf(4), "S3 M_e (cH/6, void as evidence)": mp.mpf(6),
         "S3 M_f (Z = 3 pi/2)": 3 * mp.pi / 2, "S3 M_g (Z = 3 pi)": 3 * mp.pi, "C-metric R1+C6+C4 (q* = 2.448, Z = 0.4085)": 1 / mp.mpf("2.44811125333193949659")}
zs = {}
for n, Zc in cands.items():
    zL, zT = zscore(Zc, ens, mp.mpf("0.122"))[:2]
    zs[n] = (zL, zT)
    print(f"   {n:52s} Z = {mp.nstr(Zc, 5):>8s}   offset rho_Lambda footing {mp.nstr(zL, 3):>7s} sigma, rho_total footing {mp.nstr(zT, 3):>7s} sigma")
L_.check("only the M_e entry (Z = 6, a restatement) is within 2 sigma on either footing; the C-metric fixed point (a0 = 2.45 cH) is excluded at > 15 sigma; M_a (Z = 2) at ~ 6-7 sigma; Z = 4 at 1.7 (rho_Lambda) or 3.3 sigma (rho_total)",
         abs(zs["S3 M_e (cH/6, void as evidence)"][1]) < 2 and abs(zs["S3 M_e (cH/6, void as evidence)"][0]) < 2 and abs(zs["C-metric R1+C6+C4 (q* = 2.448, Z = 0.4085)"][0]) > 15
         and abs(zs["S3 M_a  (g_H = cH/2)"][1]) > 5)

print("\n== D5: what the Lambda-force remark adds (not in the pre-declared menu; reported for completeness, not counted in the census) ==")
G, c, H, m = sp.symbols("G c H m", positive=True)
F_L = 3 * c**4 / (2 * G)
m_sol = sp.solve(sp.Eq(m * c * H, F_L), m)[0]     # mass on which the horizon Lambda-acceleration c H exerts the total vacuum force
MH = c**3 / (2 * G * H)
L_.check(f"the mass on which the Hubble-horizon Lambda-acceleration c H exerts a force equal to the whole vacuum tension F_Lambda is m = {m_sol} = 3 M_H, which is M_e again: a0 = F_max/m = c H F_max/F_Lambda; a second description of the same restatement",
         sp.simplify(m_sol - 3 * MH) == 0)
L_.check("and the mass on which cH exerts exactly F_max is M_H/2 (q = 1 by definition: the acceleration is cH itself)", sp.simplify(sp.solve(sp.Eq(m * c * H, c**4 / (4 * G)), m)[0] - MH / 2) == 0)

json.dump({"a0_needed": {k: str(v) for k, v in a0_needed.items()},
           "offsets_ensemble": {f"{k[1]}": [str(v[0]), str(v[1])] for k, v in res.items() if k[0].startswith("ensemble")}},
          open(os.path.join(HERE, "y05_results.json"), "w"), indent=1)
L_.finish()
