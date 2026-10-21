"""p62: audit of GF1's 'data pin' n = 2.000 +/- 0.017 (deepseek_push/GF1_germ_flip, R3d) -- and n from MEASURED kappa instead.
GF1 writes the tie as a0 = c sqrt(G rho_L)/n and 'measures' n_germ = c sqrt(G rho_L)/A0 with A0 = 9.3619e-11, the G058/C06 FOOTING value,
which is itself c sqrt(G rho_L)/2. So n_germ = 2 by construction (GF1 even declares the A0 error as 0.05%, 'footed a0 class').
Its second 'lockstep' channel, the BTFR slope b = 1.004 +/- 0.011, measures the deep-MOND exponent, which every MOND kernel shares
whatever kappa is; GF1's own V2 says the flatness route 'gives the exponent, not the normalization'. Neither channel measures n.
This script reads the record's CURRENT measured kappa (n = 1/kappa on each footing), after the 2026-10-19 provenance audit:
  PRIMARY  CFG493 GLS combination of the M/L-insensitive routes (SPARC ladder gas points, MIGHTEE widths, WALLABY gas points),
           shared systematics included: kappa_L 0.417 +/- 0.095, kappa_crit 0.345 +/- 0.078;
  also     its three routes, and MNRAS v3.1's SPARC estimators A, B, C on the H0-consistent R1 convention.
NOT used (superseded or not like-for-like): 0.551 +/- 0.043 (mixed H0, bulge M/L fixed); SPARC 1.0766e-10 (alpha=1 kernel, which
SPARC disfavours by d chi2 168); p48's pool (LITTLE THINGS failed its overlap test, H0 = 73 distances); McGaugh+16 and Desmond 2023
(SPARC's H0 = 73 distances, not converted).
Checks: I GF1's A0 equals c sqrt(G rho_L)/2 (the pin is an identity); R GF1's own text concedes the slope route fixes the exponent only;
  S measured n spans > 10x GF1's quoted sigma; P the tightest measured n has sigma >= 5x GF1's; K n = 2 is inside 2 sigma of CFG493
  on both footings (consistent, NOT pinned).
Run: python3 p62_gf1_data_pin_audit.py | MUTATE=1 substitutes CFG493's central a0 for GF1's A0 -> I fails
"""
import os, re, sys
from pathlib import Path
MUTATE = os.environ.get("MUTATE") == "1"
ROOT = Path(__file__).resolve().parents[2]
res = []
def check(n, ok): res.append(bool(ok)); print(("PASS  " if ok else "FAIL  ") + n)
def grab(path, pat):
    m = re.search(pat, (ROOT / path).read_text(), re.M)
    if not m: sys.exit(f"pattern not found in {path}: {pat}")
    return [float(v) for v in m.groups()]

# GF1 registers, read from the committed lane file
gf1 = "deepseek_push/GF1_germ_flip/GF1_germ_flip.py"
A0, = grab(gf1, r"^A0 = ([0-9.e+-]+)")
RHO_C, = grab(gf1, r"^RHO_C = ([0-9.e+-]+)")
OM, = grab(gf1, r"^OMEGA_L = ([0-9.e+-]+)")
G, = grab(gf1, r"^G_SI = ([0-9.e+-]+)")
C, = grab(gf1, r"^C_SI = ([0-9.e+-]+)")
SIG_GF1 = 0.0172   # GF1 README/out: n_germ = 2.00010 +/- 0.0172
S_L = C * (G * OM * RHO_C) ** 0.5      # c sqrt(G rho_L)

# current measured kappa (committed, tracked outputs)
cfg493 = "campaign_fresh_gravity/CFG493_kappa_combined/cfg493_kappa_combined.out"
pn = "qwen_claude_field_theory/papers_2026/mnras_submission_2026_v3/paper_numbers.out"
kL, kL_se = grab(cfg493, r"canonical footing: kappa = ([0-9.]+) \+- ([0-9.]+)")
kC, kC_se = grab(cfg493, r"alt\s+footing: kappa = ([0-9.]+) \+- ([0-9.]+)")
rows = [("CFG493 GLS (M/L-insensitive routes)", kL, kL_se),
        ("  P1 SPARC gas points, ladder distances", *grab(cfg493, r"P1 SPARC gas points \(ladder\): log a0 .*?kappa_Lambda ([0-9.]+) \+- ([0-9.]+)")),
        ("  P2 MeerKAT MIGHTEE-HI widths", *grab(cfg493, r"P2 MeerKAT MIGHTEE-HI widths: log a0 .*?kappa_Lambda ([0-9.]+) \+- ([0-9.]+)")),
        ("  P3 WALLABY DR2 gas points", *grab(cfg493, r"P3 WALLABY DR2 gas points: log a0 .*?kappa_Lambda ([0-9.]+) \+- ([0-9.]+)")),
        ("MNRAS v3.1 A (BTFR intercept, R1)", *grab(pn, r"estimator A \(R1\) kappa = ([0-9.]+) \+/- ([0-9.]+)")),
        ("MNRAS v3.1 B (shape-only, R1)", *grab(pn, r"==> kappa_B = ([0-9.]+) \+/- ([0-9.]+)")),
        ("MNRAS v3.1 C (profile likelihood, R1)", *grab(pn, r"kappa_C = ([0-9.]+) \+/- ([0-9.]+)"))]
print(f"   c sqrt(G rho_L) = {S_L:.5e} (GF1 registers)")
print(f"   {'source':42s} {'kappa_L':>8s} {'n_L':>7s} {'sigma_n':>8s} {'n=2 pull':>9s}")
nL, sn = [], []
for name, k, se in rows:
    n, s = 1 / k, se / k**2
    nL.append(n); sn.append(s)
    print(f"   {name:42s} {k:8.3f} {n:7.3f} {s:8.3f} {(n - 2) / s:+9.2f}")
n_c, s_c = 1 / kC, kC_se / kC**2
print(f"   CFG493 on rho_crit: kappa_crit {kC} +/- {kC_se} -> n_crit = {n_c:.3f} +/- {s_c:.3f}")

a0_gf1 = kL * S_L if MUTATE else A0
check(f"I GF1's A0 = c sqrt(G rho_L)/2 to 1e-4 (n_germ = {S_L / a0_gf1:.5f} is an identity, not a measurement)", abs(S_L / a0_gf1 - 2) < 1e-4 * 2)
check("R GF1's own V2 concedes the flatness/slope route fixes the exponent, not the normalization",
      "gives the exponent, not the normalization" in (ROOT / gf1).read_text())
check(f"S measured n_L spans {max(nL) - min(nL):.3f} > 10x GF1's sigma {SIG_GF1}", max(nL) - min(nL) > 10 * SIG_GF1)
check(f"P tightest measured n has sigma {min(sn):.3f} >= 5x GF1's {SIG_GF1}", min(sn) >= 5 * SIG_GF1)
check(f"K n = 2 inside 2 sigma of CFG493 on both footings ({abs(nL[0] - 2) / sn[0]:.2f} / {abs(n_c - 2) / s_c:.2f} sigma)",
      abs(nL[0] - 2) < 2 * sn[0] and abs(n_c - 2) < 2 * s_c)
print(f"\n{sum(res)}/{len(res)} pass" + ("  (MUTATE)" if MUTATE else ""))
sys.exit(0 if all(res) else 1)
