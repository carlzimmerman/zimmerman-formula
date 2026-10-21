"""p63: a0 as a field -- can an identification or a quantization fix k04's free ratio Z/beta^2?  Criteria: FROZEN_CRITERIA.md (2a36f4ae5).
k04 F2: kappa^2 = 2 beta^2/(Z + 2 b beta^2); kappa = 1/2 <=> Z/beta^2 = 8 - 2b = 7.964 (free ratio of two couplings).
Candidates (fixed list):
  C1  saturated dual polarization: dark energy = 4-divergence of cold energy's polarization P^mu (dual of the three-form), FRW attractor
      q = D H P0/c, cosmic state at saturation S_D G P0 = sigma a0 (sigma = 1)  =>  kappa = S_D sqrt(G rho)/(D H sigma); premise gate: finite W.
  C1b patch bootstrap: CFG695 response u = a0 g/(a0 + g) to the de Sitter field g = H^2 r; bound mass inside R = c/H equals the vacuum mass
      =>  1/(1+Z) = rho S_D G_N/(D H^2) = (D-2)/2,  Z := cH/a0.
  C2  flux lattice: rho_L = N^2 rho_1, a0 = kappa_1 c sqrt(G rho_1)  =>  kappa = kappa_1/N  (MENU unless kappa_1 is forced).
  C3  Kaloper-Sorbo monodromy: 2 pi f mu = N e quantizes (f, mu, e); kappa^2 = 2 beta^2/Z is untouched.
General spatial dimension D (d = D+1): S_D = 2 pi^(D/2)/Gamma(D/2), S_D G_N = 8 pi G_d (D-2)/(D-1), H^2 = 16 pi G_d rho/(D(D-1)).
Checks: K1 k04 F2 reproduced; K2 CFG695 W' and its divergence at u -> a0; T4 C1 kappa_dS(D=3) = sqrt(2 pi/3); T4 C1b Z(D) = (4-D)/(D-2);
  W1 C1's window verdict is OUT; H1 C3 has no hbar; C2 kappa_1 = 1 hits N = 2, 3, 4.
PRIMARY window (erratum 2): CFG493's GLS kappa, 2 sigma on each footing; SECONDARY: MNRAS v3.1 estimators A, B, C on the R1 convention.
Run: python3 p63_a0_field_coupling.py | MUTATE=1 applies M1 (saturation 2 a0), M2 (window x2), M3 (hbar in C3); W1, H1, T4-C1, C2 must FAIL.
"""
import os, re, sys, json, math
from pathlib import Path
import sympy as sp

MUTATE = os.environ.get("MUTATE") == "1"
HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
SIGMA = 2 if MUTATE else 1            # M1
WSCALE = 2.0 if MUTATE else 1.0       # M2
HBAR_IN = MUTATE                      # M3
res = []
def check(n, ok): res.append(bool(ok)); print(("PASS  " if ok else "FAIL  ") + n)
def grab(path, pat):
    m = re.search(pat, (ROOT / path).read_text(), re.M)
    if not m: sys.exit(f"pattern not found in {path}: {pat}")
    return [float(v) for v in m.groups()]

# ---- registers (GF1) and the frozen window ----
gf1 = "deepseek_push/GF1_germ_flip/GF1_germ_flip.py"
RHO_C, = grab(gf1, r"^RHO_C = ([0-9.e+-]+)")
OM, = grab(gf1, r"^OMEGA_L = ([0-9.e+-]+)")
G_SI, = grab(gf1, r"^G_SI = ([0-9.e+-]+)")
C_SI, = grab(gf1, r"^C_SI = ([0-9.e+-]+)")
SQ = math.sqrt(OM)
# PRIMARY window per erratum 2: CFG493's GLS combination of the M/L-insensitive routes (the frozen 0.551 +/- 0.043 was superseded)
cfg493 = "campaign_fresh_gravity/CFG493_kappa_combined/cfg493_kappa_combined.out"
kL0, kL0_se = grab(cfg493, r"canonical footing: kappa = ([0-9.]+) \+- ([0-9.]+)")
kC0, kC0_se = grab(cfg493, r"alt\s+footing: kappa = ([0-9.]+) \+- ([0-9.]+)")
WIN_L = ((kL0 - 2 * kL0_se) * WSCALE, (kL0 + 2 * kL0_se) * WSCALE)
WIN_C = ((kC0 - 2 * kC0_se) * WSCALE, (kC0 + 2 * kC0_se) * WSCALE)
pn = "qwen_claude_field_theory/papers_2026/mnras_submission_2026_v3/paper_numbers.out"
SEC = {"A (BTFR, R1)": grab(pn, r"estimator A \(R1\) kappa = ([0-9.]+) \+/- ([0-9.]+)"),
       "B (shape-only, R1)": grab(pn, r"==> kappa_B = ([0-9.]+) \+/- ([0-9.]+)"),
       "C (profile, R1)": grab(pn, r"kappa_C = ([0-9.]+) \+/- ([0-9.]+)")}
def inside(kL): return WIN_L[0] <= kL <= WIN_L[1] and WIN_C[0] <= kL * SQ <= WIN_C[1]
print(f"   PRIMARY (CFG493) kappa_L in [{WIN_L[0]:.3f}, {WIN_L[1]:.3f}], kappa_crit in [{WIN_C[0]:.3f}, {WIN_C[1]:.3f}]"
      f"{'  (M2: x2)' if MUTATE else ''};  SECONDARY (MNRAS v3.1, R1): "
      + ", ".join(f"{k} {v[0]} +/- {v[1]}" for k, v in SEC.items()))

# ---- K1: k04 F2 ----
k04 = "kappa_closure/k04_four_form_promotion_consistency.out"
Z, b, beta = sp.symbols("Z b beta", positive=True)
k2_04 = 2 * beta**2 / (Z + 2 * b * beta**2)
ratio = sp.simplify(sp.solve(sp.Eq(k2_04, sp.Rational(1, 4)), Z)[0] / beta**2)
I_rar, = grab(k04, r"I = ([0-9.]+)\)")
b0 = 2 * I_rar / (16 * math.pi)
check(f"K1 k04 F2: kappa^2 = 2 beta^2/(Z + 2 b beta^2), Z/beta^2 = {ratio} = {float(ratio.subs(b, b0)):.4f} at K_B = 0 (k04: 7.964)",
      "kappa^2 = 2*beta**2/(Z + 2*b*beta**2)" in (ROOT / k04).read_text() and sp.simplify(ratio - (8 - 2 * b)) == 0
      and abs(float(ratio.subs(b, b0)) - 7.964) < 1e-3)

# ---- K2: CFG695 saturating W ----
u, a0, G, t = sp.symbols("u a0 G t", positive=True)
W = -(a0 / (4 * sp.pi * G)) * (u + a0 * sp.log(1 - u / a0))
dWdP = sp.simplify(sp.diff(W, u) * 4 * sp.pi * G)
Wlim = sp.limit(W.subs(u, a0 * (1 - t)), t, 0, "+")
check(f"K2 CFG695: dW/dP = u/(1 - u/a0) and W(u -> a0-) = {Wlim}", sp.simplify(dWdP - u / (1 - u / a0)) == 0 and Wlim == sp.oo)

# ---- general-D machinery ----
D, Gd, rho, c, H = sp.symbols("D G_d rho c H", positive=True)
S_D = 2 * sp.pi**(D / 2) / sp.gamma(D / 2)
G_N = 8 * sp.pi * Gd * (D - 2) / ((D - 1) * S_D)
H2_dS = 16 * sp.pi * Gd * rho / (D * (D - 1))
at3 = lambda e: float(e.subs(D, 3))

# ---- C1: saturated dual polarization ----
kap_C1 = S_D * sp.sqrt(G_N * rho) / (D * H * SIGMA)                 # kappa := a0/(c sqrt(G_N rho))
kap_C1_dS = sp.simplify(kap_C1.subs(H, sp.sqrt(H2_dS)))
kC1_dS3 = at3(kap_C1_dS)
kC1_today = at3(kap_C1_dS * SIGMA) * SQ                              # the sigma = 1 construction, today (H0 = H_L/sqrt(Omega_L)); M1 tests T4 only
check(f"T4 C1 kappa_dS(D) = {sp.simplify(kap_C1_dS)} -> D=3: {kC1_dS3:.5f} = sqrt(2 pi/3) (sigma = 1 construction)",
      abs(kC1_dS3 - math.sqrt(2 * math.pi / 3)) < 1e-12)
c1_u_over_sat = 1.0                    # C1 puts the cosmic state AT saturation; finite W needs u < u_sat (K2); readings (i)=(ii) when P_spatial = 0
c1_gate = c1_u_over_sat < 1
c1_ratio_z25 = 1 / math.sqrt((1 - OM) * 3.5**3 + OM)                # a0 ~ 1/H(z) at fixed rho_L
c1_win = inside(kC1_today)
print(f"   C1: kappa_L today = {kC1_today:.4f} (hand 1.20), kappa_crit = {kC1_today * SQ:.4f}; a0(2.5)/a0(0) = {c1_ratio_z25:.4f} (OTHER: ~1/H);"
      f" gate: cosmic u = u_sat -> W = +inf for readings (i) |P^mu P_mu| and (ii) P0 alone -> {'PASS' if c1_gate else 'FAIL'}")
check(f"W1 C1 window verdict is OUT on both footings (kappa_L {kC1_today:.3f})", not c1_win)

# ---- C1b: patch bootstrap ----
lhs_ratio = sp.simplify(rho * S_D * G_N / (D * H2_dS))
Z_D = sp.simplify(1 / lhs_ratio - 1)
kap_C1b = sp.simplify(sp.sqrt(H2_dS) / (Z_D * sp.sqrt(G_N * rho)))
check(f"T4 C1b 1/(1+Z) = {lhs_ratio}, Z(D) = {Z_D} = (4-D)/(D-2); D=3: Z = {at3(Z_D):.6f}",
      sp.simplify(lhs_ratio - (D - 2) / 2) == 0 and sp.simplify(Z_D - (4 - D) / (D - 2)) == 0 and abs(at3(Z_D) - 1) < 1e-12)
kC1b = at3(kap_C1b)
u_state = at3(Z_D) / (1 + at3(Z_D))                                  # u/a0 at R = c/H_L
c1b_win = inside(kC1b)
print(f"   C1b: kappa_L = {kC1b:.4f} (hand 2.89), kappa_crit = {kC1b * SQ:.4f}; a0 = c H_L/Z tracks sqrt(rho_DE) (TRACKING);"
      f" u/a0 at the patch edge = {u_state:.3f} (finite W)")

# ---- C2: flux lattice ----
kap1, Nmax = 1.0, 10
hits = [N for N in range(1, Nmax + 1) if inside(kap1 / N)]
iv = sorted((WIN_L[0] * N, WIN_L[1] * N) for N in range(1, Nmax + 1))
merged = []
for lo_, hi_ in iv:
    lo_, hi_ = max(lo_, 0.1), min(hi_, 10.0)
    if lo_ >= hi_: continue
    if merged and lo_ <= merged[-1][1]: merged[-1][1] = max(merged[-1][1], hi_)
    else: merged.append([lo_, hi_])
p_null = sum(math.log(h / l) for l, h in merged) / math.log(100.0)
print(f"   C2: kappa = kappa_1/N; kappa_1 = 1 hits N = {hits}; null P(>=1 hit | kappa_1 log-uniform [0.1,10], N <= 10) = {p_null:.3f}")
check(f"C2 kappa_1 = 1 lands in PRIMARY at N = 2, 3, 4 as declared in erratum 2 (hits {hits}): the lattice does not single out N = 2", hits == [2, 3, 4])

# ---- C3: Kaloper-Sorbo ----
e, mu, f, hbar = sp.symbols("e mu f hbar", positive=True)
quant = sp.Eq(2 * sp.pi * f * mu, e)                                 # one monodromy quantum
kap_C3 = sp.sqrt(2 * beta**2 / Z) * (sp.sqrt(hbar) if HBAR_IN else 1)
p_hbar = sp.simplify(hbar * sp.diff(sp.log(kap_C3), hbar))
free_C3 = sorted(str(s) for s in kap_C3.free_symbols if s in {beta, Z})
print(f"   C3: quantization {quant} fixes (f, mu, e) only; kappa = {kap_C3} keeps {free_C3} (one ratio); hbar power = {p_hbar}")
check(f"H1 C3 kappa carries no hbar (p = {p_hbar})", p_hbar == 0)

# ---- classification ----
def classify(fc, p, gate, t5, win, menu=False):
    if not gate: return "INCONSISTENT"
    if p != 0: return "hbar-DEPENDENT"
    if menu: return "MENU"
    if fc >= 1: return "FREE"
    return "FORCED-IN" if (win and t5 == "TRACKING") else "FORCED-OUT"
rows = {
    "C1":  dict(kappa_L=kC1_today, f=0, p=0, gate=c1_gate, T5="OTHER", window_in=c1_win, a0_z25_over_0=c1_ratio_z25,
                T6="cosmological identification; no local-sector change", T7="a0 falls as 1/H(z)"),
    "C1b": dict(kappa_L=kC1b, f=0, p=0, gate=u_state < 1, T5="TRACKING", window_in=c1b_win, a0_z25_over_0=1.0,
                T6="needs the medium to respond to the de Sitter field (selector S2 reads own baryons only)", T7="cosmic bound-charge profile (3+2x)/(1+x)^2"),
    "C2":  dict(kappa_L=[kap1 / N for N in range(1, 5)], f=0, p=0, gate=True, T5="TRACKING", window_in=bool(hits), menu=True, hits=hits, p_null=p_null,
                T6="flux sector only", T7="membrane nucleation N -> N-1 changes Lambda and kappa = kappa_1/N together"),
    "C3":  dict(kappa_L=None, f=1, p=int(p_hbar != 0), gate=True, T5="TRACKING", window_in=False, free=free_C3,
                T6="as k04 (F6-correction instability band 2.39-155 a0 inherited)", T7="axion monodromy"),
}
for k, r in rows.items():
    r["class"] = classify(r["f"], r["p"], r["gate"], r["T5"], r["window_in"], r.get("menu", False))
    print(f"   {k:4s} -> {r['class']}")
classes = [r["class"] for r in rows.values()]
verdict = ("CANDIDATE DERIVATION (conditional)" if "FORCED-IN" in classes else
           "NARROWED" if ("FORCED-OUT" in classes or "MENU" in classes) else "CLOSED")
print(f"\n   LANE VERDICT: {verdict}" + ("  (MUTATE: not a verdict)" if MUTATE else ""))
out = HERE / ("p63_a0_field_coupling_MUTATE_results.json" if MUTATE else "p63_a0_field_coupling_results.json")
out.write_text(json.dumps({"mutate": MUTATE, "window_L": WIN_L, "window_crit": WIN_C, "secondary_L": SEC, "candidates": rows,
                           "verdict": verdict, "checks_passed": sum(res), "checks": len(res)}, indent=2, default=str))
print(f"\n{sum(res)}/{len(res)} pass" + ("  (MUTATE)" if MUTATE else ""))
sys.exit(0 if all(res) else 1)
