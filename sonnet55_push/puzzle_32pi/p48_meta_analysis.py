"""p48: random-effects (DerSimonian-Laird) combination of the independent Upsilon-robust a0 estimates from p43/p46/p47, in ln a0.
Independent sets (no shared galaxies): SPARC gas points TRGB/Cepheid (p46: 1.158e-10, 20.2%), SPARC gas points Hubble flow (p46: 6.97e-11, 18.3%), WALLABY gas points
(p43: 7.28e-11, 23.3%), LITTLE THINGS (p47: 7.80e-11, 40.8%; 3 galaxies overlap SPARC's set, kept, noted). Between-set scatter tau^2 estimated by DL; pooled ln a0 with
error sqrt(1/sum w*), w* = 1/(s_i^2 + tau^2). Then the pooled value against the footings and rivals. A second combination uses only the redshift-independent set.
Run: python3 p48_meta_analysis.py  |  MUTATE=1: TRGB estimate set to 2.0e-10 (heterogeneity must rise: check H fails)
"""
import os, sys, math
MUTATE = os.environ.get("MUTATE") == "1"
res = []
def check(n, ok): res.append(bool(ok)); print(("PASS  " if ok else "FAIL  ") + n)
E = [("SPARC gas, TRGB/Cepheid", 2.0e-10 if MUTATE else 1.158e-10, 0.202), ("SPARC gas, Hubble flow", 6.97e-11, 0.183),
     ("WALLABY gas (Hubble flow)", 7.28e-11, 0.233), ("LITTLE THINGS (authors' M/L)", 7.80e-11, 0.408)]
y = [math.log(a) for _, a, s in E]; s2 = [s * s for _, a, s in E]; w = [1 / v for v in s2]
ybar = sum(wi * yi for wi, yi in zip(w, y)) / sum(w)
Q = sum(wi * (yi - ybar)**2 for wi, yi in zip(w, y)); k = len(E)
tau2 = max(0.0, (Q - (k - 1)) / (sum(w) - sum(wi * wi for wi in w) / sum(w)))
ws = [1 / (v + tau2) for v in s2]; mu = sum(wi * yi for wi, yi in zip(ws, y)) / sum(ws); se = math.sqrt(1 / sum(ws))
I2 = max(0.0, (Q - (k - 1)) / Q) if Q > 0 else 0.0
print(f"   fixed-effect: {math.exp(ybar):.3e};  Q = {Q:.2f} (k-1 = {k-1}), I^2 = {100*I2:.0f}%, tau = {math.sqrt(tau2):.3f} (between-set scatter in ln a0)")
print(f"   RANDOM-EFFECTS POOLED a0 = {math.exp(mu):.3e}  (68%: {math.exp(mu-se):.3e} - {math.exp(mu+se):.3e}; +-{100*se:.1f}%)")
for lab, v in (("kappa=1/2 rho_Lambda", 9.3603e-11), ("alt rho_total (original)", 1.1312e-10), ("Verlinde 6 rho_L", 9.033e-11), ("Milgrom 2pi rho_L", 8.626e-11),
               ("Milgrom 2pi rho_tot", 1.042e-10), ("32pi turn-off", 1.061e-10), ("SPARC conventional 1.2e-10", 1.2e-10)):
    print(f"      {lab:28s} {v:.3e}: pull {(math.log(v) - mu)/se:+.2f}")
check(f"P every candidate in 0.86-1.13e-10 lies within 2 sigma of the pooled value (the data cannot pick among them)",
      all(abs((math.log(v) - mu) / se) < 2 for v in (9.3603e-11, 1.1312e-10, 9.033e-11, 8.626e-11, 1.042e-10, 1.061e-10)))
check(f"H the estimates are mutually consistent at the 2-sigma level of the Q test (Q = {Q:.2f} < {k-1 + 2*math.sqrt(2*(k-1)):.2f})", Q < (k - 1) + 2 * math.sqrt(2 * (k - 1)))
print(f"\n{sum(res)}/{len(res)} pass" + ("  (MUTATE)" if MUTATE else ""))
sys.exit(0 if all(res) else 1)
