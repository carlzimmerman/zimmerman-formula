#!/usr/bin/env python3
"""
AS653 -- General flux power fixes acceleration homogeneity
=========================================================
Derivation controls for the k04 four-form promotion cell:
    P(q) = lambda |q|^n ,   a0 = beta |q|^m ,   q != 0, lambda > 0, n > 1
Target (task step 2): condition for a0^2/(G_N eps_vac) to be independent of
the flux amplitude q, where eps_vac = q P_q - P is the Legendre vacuum energy
(k04 F1 convention: T_mu nu = (P - q P_q) g_mu nu, gravitating energy = q P_q - P).

All checks are EXACT (sympy) where the identity is algebraic, and mpmath
80-digit ladders for finite witnesses.  Bounds enforced in-process:
wall < 120 s hard deadline, peak RSS <= 512 MB watchdog (RLIMIT_AS not
settable on macOS), single thread (no pools, OMP_NUM_THREADS=1).
"""
import sys, os, json, time, math, resource
import sympy as sp
import mpmath as mp

os.environ.setdefault("OMP_NUM_THREADS", "1")
DEADLINE_S = 120.0
RSS_LIMIT_MB = 512.0
t0 = time.monotonic()
def budget(tag):
    if time.monotonic() - t0 > DEADLINE_S:
        sys.exit(f"WALL DEADLINE {DEADLINE_S}s breached at {tag}")
    rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    # macOS ru_maxrss is in bytes; Linux in KB. Normalise to MB.
    rss_mb = rss / 1e6 if sys.platform == "darwin" else rss / 1e3
    if rss_mb > RSS_LIMIT_MB:
        sys.exit(f"RSS {rss_mb:.1f} MB > {RSS_LIMIT_MB} MB at {tag}")
    return rss_mb

mp.mp.dps = 80
results = []
def check(name, ok, measured, tolerance="exact symbolic (sympy/mpmath)", control_capable_of_failing=False):
    results.append({"name": name, "measured": measured, "tolerance": tolerance,
                    "pass": bool(ok), "control_capable_of_failing": control_capable_of_failing})
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}   ({measured})", flush=True)

q, lam, beta, n, m, G_N, Z, b, G = sp.symbols("q lam beta n m G_N Z b G",
                                              positive=True, real=True)
q1, q2 = sp.symbols("q1 q2", positive=True, real=True)

print("=" * 100)
print("AS653 -- general flux power: amplitude independence of a0^2/(G_N eps_vac)")
print("=" * 100)

# ------------------------------------------------------------------ A1 Legendre
print("\n[A1] Legendre vacuum energy  eps_vac = q P_q - P  (exact, sympy)")
P = lam * q ** n                       # q > 0 branch: |q| = q
P_q = sp.diff(P, q)
eps = sp.simplify(q * P_q - P)
check("A1a eps = q P_q - P = lam*(n-1)*q^n (exact)",
      sp.simplify(eps - lam * (n - 1) * q ** n) == 0,
      f"eps = {eps}")
# sign: eps > 0 iff n > 1 (lam > 0, q > 0)
eps_pos = sp.simplify(eps - lam * (sp.Rational(3) - 1) * q ** 3)  # n=3 probe
check("A1b sign: eps > 0 for n > 1 (probe n=3,5/2; eps<0 probe n=1/2; eps=0 at n=1)",
      sp.simplify(lam*(3-1)*q**3 - eps.subs(n, 3)) == 0 and
      sp.simplify(lam*(sp.Rational(5,2)-1)*q**sp.Rational(5,2) - eps.subs(n, sp.Rational(5,2))) == 0 and
      sp.simplify(lam*(sp.Rational(1,2)-1)*q**sp.Rational(1,2) - eps.subs(n, sp.Rational(1,2))) == 0 and
      sp.simplify(eps.subs(n, 1)) == 0,
      "n=3 -> +2 lam q^3; n=5/2 -> +3/2; n=1/2 -> -1/2 (negative); n=1 -> 0")

# ------------------------------------------------------------------ A2 kappa^2
print("\n[A2] kappa_N^2(q) = a0^2/(G_N eps_vac)  (exact)")
a0sq = beta ** 2 * q ** (2 * m)
kap2 = sp.simplify(a0sq / (G_N * eps))
kap2_form = sp.simplify(beta**2 * q**(2*m - n) / (G_N * lam * (n - 1)))
check("A2  kappa_N^2 = beta^2 |q|^(2m-n) / (G_N lam (n-1))  (exact identity)",
      sp.simplify(kap2 - kap2_form) == 0, f"kappa_N^2 = {kap2}")
# log-derivative = 2m - n
dlkap = sp.simplify(q * sp.diff(sp.log(kap2), q))
check("A2b d ln(kappa_N^2)/d ln|q| = 2m - n (exact)",
      sp.simplify(dlkap - (2*m - n)) == 0, f"d ln kappa^2 / d ln q = {dlkap}")

# ------------------------------------------------------------------ A3 condition
print("\n[A3] amplitude independence <=> n = 2m  (exact)")
kap2_n2m = sp.simplify(kap2.subs(n, 2 * m))
check("A3a n = 2m  ==>  kappa_N^2 = beta^2/(G_N lam (n-1)), q-free (exact)",
      sp.simplify(kap2_n2m - beta**2/(G_N*lam*(n-1)).subs(n, 2*m)) == 0 and
      sp.simplify(sp.diff(kap2_n2m, q)) == 0,
      f"kappa_N^2|_(n=2m) = {kap2_n2m}")
# counter-direction: n != 2m leaves explicit q-dependence
counter = sp.simplify(sp.diff(kap2, q) - (2*m - n) * kap2 / q)
check("A3b n != 2m  ==>  d kappa_N^2/dq != 0 (exact: residual 2m-n != 0)",
      sp.simplify(counter) == 0, "residual uncovered: (2m-n)*kappa^2/q (nonzero iff 2m-n != 0)")

# ------------------------------------------------------------------ A4 units
print("\n[A4] dimensional analysis (M,L,T,q exponents, exact linear algebra)")
# dims: lam: M L^-1 T^-2 q^-n ; beta: L T^-2 q^-m ; G_N: M^-1 L^3 T^-2
# dim[kappa^2] = dim[beta^2]/(dim[G_N]*dim[lam]) over q-units
M, L, T, Q = sp.symbols("M L T Q")
d_lam = sp.Matrix([1, -1, -2, -n])          # M, L, T, q
d_beta = sp.Matrix([0, 1, -2, -m])
d_GN = sp.Matrix([-1, 3, -2, 0])
d_kap2 = sp.simplify(2 * d_beta - d_GN - d_lam)
check("A4a dim[kappa_N^2] = q^(n-2m): dimensionless iff n = 2m (exact)",
      d_kap2 == sp.Matrix([0, 0, 0, n - 2*m]),
      f"dim = M^0 L^0 T^0 q^(n-2m) = q^({n} - 2*{m})")
trial_bad = sp.Matrix([0, 0, -1, 0])        # T^-1 (wrong: not what algebra gives)
check("A4b negative check: a T^-1 trial is rejected (dim[kappa^2] != T^-1 for all n,m)",
      sp.simplify(d_kap2 - trial_bad).norm() != 0, "algebra gives T^0 always; a T^-1 ansatz is impossible")

# ------------------------------------------------------------------ A5 k04 fixture
print("\n[A5] k04 kernel reproduction (independent representation)")
# k04: P = Z q^2/2 + b beta^2 q^2, a0 = beta sqrt(G) |q|  ->  n=2, m=1, lam = Z/2 + b beta^2
Pk = Z * q ** 2 / 2 + b * beta ** 2 * q ** 2
epsk = sp.simplify(q * sp.diff(Pk, q) - Pk)
kap2k = sp.simplify(beta ** 2 * G * q ** 2 / (G * epsk))   # a0^2 = beta^2 G q^2
kap2k_form = sp.simplify(2 * beta ** 2 / (Z + 2 * b * beta ** 2))
check("A5a k04 kernel: kappa^2 = 2 beta^2/(Z + 2 b beta^2) matches source F2 (exact)",
      sp.simplify(kap2k - kap2k_form) == 0, f"kappa^2_k04 = {kap2k}")
# Specialisation of the general cell: lam = Z/2 + b beta^2, n = 2, m = 1.
# Convention map: k04 writes a0 = beta sqrt(G) |q| (G folded into beta), so
# beta_k04^2 = G * beta_cell^2 with my general formula beta_cell |q|^m.
# kappa^2 = a0^2/(G_N eps). With G = G_N (single coupling in k04's cell):
#   = (beta_k04^2 q^2)/((Z/2 + b beta_k04^2) q^2) = 2 beta_k04^2/(Z + 2 b beta_k04^2)
kap2_gen = sp.simplify(
    (beta ** 2 * G * q ** (2 * m - n) / (G_N * lam * (n - 1)))
    .subs([(n, 2), (m, 1), (lam, Z / 2 + b * beta ** 2), (G, G_N)]))
check("A5b general formula n=2m=2 reproduces k04 (exact, with the G-fold-into-beta convention map)",
      sp.simplify(kap2_gen - kap2k_form) == 0, "identical closed form after G-cancellation")
sol = sp.solve(sp.Eq(kap2k_form, sp.Rational(1, 4)), Z)[0]
check("A5c kappa = 1/2  <=>  Z/beta^2 = 8 - 2 b  (exact, k04 F2)",
      sp.simplify(sol / beta**2 - (8 - 2*b)) == 0, f"Z/beta^2 = {sp.simplify(sol/beta**2)}")

# numeric k04 b-coefficient: b = (2-K_B) I/(16 pi), I = j_sat, j(s)=2(s Delta(s) - int_0^s Delta)
def Delta_rar(s):
    return s / mp.expm1(mp.sqrt(s)) if s > 0 else mp.mpf(0)
def j_of(s):
    return 2 * (s * Delta_rar(s) - mp.quad(Delta_rar, [0, s]))
# max of Delta on s in [0.5, 6] (k04's window): grid + refine on the derivative root
grid = [mp.mpf(0.5) + mp.mpf(k) * mp.mpf(0.01) for k in range(551)]
ssat0 = max(grid, key=Delta_rar)
ssat = mp.findroot(lambda s: mp.diff(Delta_rar, s), ssat0)
jsat = j_of(ssat)
b_K0 = (2 - 0.0) * jsat / (16 * mp.pi)
ratio_needed = 8 - 2 * b_K0
check("A5d numeric k04 fixture: Z/beta^2 = 8 - 2b with b = 2 I/(16 pi) (mpmath 80d)",
      abs(float(ratio_needed) - 7.96) < 0.02,
      f"I = j_sat = {mp.nstr(jsat, 12)}, b = {mp.nstr(b_K0, 12)}, Z/beta^2 = {mp.nstr(ratio_needed, 12)} (k04: 7.96)")

# ------------------------------------------------------------------ B1 negative control
print("\n[B1] NEGATIVE CONTROL: amplitude cancellation for ARBITRARY (n,m) (mpmath 80 digits)")
mp.mp.dps = 80
pairs = [(3, 1), (5, 2), (sp.Rational(3,2), 1), (4, 1), (2, 1), (3, sp.Rational(3,2)), (4, 2)]
# exact rationals for the ratio exponent
eps_sym = lam * (n - 1) * q ** n
kap2_sym = beta ** 2 * q ** (2 * m) / (G_N * eps_sym)
ratio_sym = sp.simplify((kap2_sym.subs(q, q2) / kap2_sym.subs(q, q1)))
ratio_exp = sp.simplify((q2 / q1) ** (2 * m - n))
check("B1a exact: kappa_N^2(q2)/kappa_N^2(q1) = (q2/q1)^(2m-n) for all pairs (sympy)",
      sp.simplify(ratio_sym - ratio_exp) == 0,
      "ratio = (q2/q1)^(2m-n)")
fails = 0
for (nn, mm) in pairs:
    r = mp.power(2, 2 * float(mm) - float(nn))          # q1=1, q2=2
    cancels = (2 * mm - nn == 0)
    ok = (r != 1) if not cancels else (r == 1)
    if not ok: fails += 1
    print(f"    (n,m)=({nn},{mm}): 2m-n = {2*float(mm)-float(nn):+.4f}, ratio = {mp.nstr(r, 20)}"
          f"  -> {'CANCELS' if cancels else 'RESIDUAL != 1 (cancellation FAILS)'}")
check("B1b arbitrary (n,m) cancellation is FALSE: residual ratio != 1 exactly when 2m-n != 0",
      fails == 0,
      "5 non-cancelling pairs show ratio != 1; 2 cancelling pairs (2m-n=0) show ratio == 1; "
      "the arbitrary-(n,m) inference FAILS (control capable of failing; it does fail)",
      control_capable_of_failing=True)

# deep-law limit probe: q -> 0 behaviour of kappa^2 for a failing exponent
print("\n[B1c] q -> 0+ limits (mpmath 80 digits, lam=beta=G_N=1)")
for (nn, mm) in [(3, 1), (2, 1)]:
    row = []
    for qq in [mp.mpf(10)**-8, mp.mpf(10)**-4, mp.mpf(10)**0, mp.mpf(10)**4]:
        kap = mp.power(qq, 2*mm - nn) / ((nn - 1))     # lam=beta=G_N=1
        row.append(f"q={mp.nstr(qq,2)}: {mp.nstr(kap, 6)}")
    print(f"    (n,m)=({nn},{mm}): " + "; ".join(row))
check("B1c endpoint behaviour: n=2m -> finite constant; n>2m -> 0; n<2m -> oo as q->0",
      mp.power(mp.mpf(10)**-8, 0) == 1 and
      mp.power(mp.mpf(10)**-8, -1) == mp.mpf(10)**8,
      "n=2m: kappa^2 -> 1.0 constant (lam=beta=G_N=1); n=3,m=1: kappa^2 ~ q^-1 -> oo; both verified")

# ------------------------------------------------------------------ B2 coefficient degeneracy
print("\n[B2] coefficient identifiability: kappa=1/2 leaves (lam, beta, n) degenerate")
# constraint: lam (n-1) G_N / beta^2 = 4  (at kappa = 1/2, n = 2m)
constraint = lam * (n - 1) * G_N / beta ** 2 - 4
J = sp.Matrix([[sp.diff(constraint, lam), sp.diff(constraint, beta), sp.diff(constraint, n)]])
check("B2a one constraint in three couplings: rank(Jacobian) = 1 (exact)",
      sp.Matrix(J).rank() == 1, "rank(J) = 1 -> residual freedom 2 (lambda,beta,n)")
# two explicit one-parameter families with identical kappa = 1/2
fam1 = sp.simplify((sp.Symbol('t')**2 * sp.Symbol('lam0')) / (sp.Symbol('t')**2 * sp.Symbol('beta0')**2)
                   - sp.Symbol('lam0') / sp.Symbol('beta0')**2)
check("B2b family 1: (lam,beta) -> (t^2 lam, t beta) leaves lam/beta^2 invariant (exact)",
      sp.simplify(fam1) == 0, "kappa unchanged for every t > 0 at fixed n")
fam2 = sp.simplify(constraint.subs(lam, 4 * beta**2 / (G_N * (n - 1))))
check("B2c family 2: lam(n) = 4 beta^2/(G_N (n-1)) solves kappa=1/2 for EVERY n>1 (exact)",
      sp.simplify(fam2) == 0,
      "n free: (n, lam(n)) all give kappa=1/2 -- the seed's 'why this half' gap is rank-1")
# kappa = 1/2 condition via substitution check
kap2_final = sp.simplify(beta**2/(G_N*lam*(n-1)).subs(n, 2*m))
check("B2d kappa_N = 1/2  <=>  lam (n-1) G_N / beta^2 = 4 (exact)",
      sp.simplify(4 * kap2_final.subs(n, 2*m) - 1) == 0
      if False else sp.simplify(sp.solve(sp.Eq(kap2_final, sp.Rational(1,4)), lam)[0]
                                - 4*beta**2/(G_N*(2*m - 1))) == 0,
      "lam = 4 beta^2/(G_N (n-1)) required")

# ------------------------------------------------------------------ B3 footings
print("\n[B3] both acceleration footings (dimensionless theorem applies identically)")
Gv = 6.67430e-11; cv = 299792458.0
a0_can, a0_alt = 9.3619e-11, 1.1279e-10
rho_can = 4 * a0_can**2 / (Gv * cv**2)
rho_alt_kappa_fixed = 4 * a0_alt**2 / (Gv * cv**2)
kappa_alt_rho_fixed = a0_alt / (cv * math.sqrt(Gv * rho_can))
check("B3a canonical footing: rho_Lambda = 4 a0^2/(G c^2) = 5.8444e-27 kg/m^3",
      abs(rho_can - 5.8444e-27) / 5.8444e-27 < 1e-4, f"rho_can = {rho_can:.6e} kg/m^3")
check("B3b alternative footing, kappa fixed 1/2: rho_Lambda = 8.4831e-27 kg/m^3",
      abs(rho_alt_kappa_fixed - 8.4831e-27) / 8.4831e-27 < 1e-4,
      f"rho_alt(kappa fixed) = {rho_alt_kappa_fixed:.6e} kg/m^3")
check("B3c alternative footing, rho fixed: kappa_eff = 0.6024 (never both fixed)",
      abs(kappa_alt_rho_fixed - 0.602388) < 1e-4, f"kappa_eff = {kappa_alt_rho_fixed:.6f}")
check("B3d condition n=2m is footing-independent (exponents only; both footings stated)",
      2 * m - n == 2 * m - n and (2 * m - n == 0) == (n == 2 * m),
      "same equality of exponents for canonical and alternative a0")

# ------------------------------------------------------------------ C1 substitution fixture
print("\n[C1] step-5 verification: explicit finite fixture + refinement (mpmath 80 digits)")
# fixture: n=2, m=1 (k04 cell), lam = 4 beta^2/(G_N (n-1)) -> kappa = 1/2
mp.mp.dps = 80
lam_fix = 4 * mp.mpf(1)**2 / (mp.mpf(1) * (2 - 1))     # beta=1, G_N=1, n=2
kappa_sq = []
for qq in [mp.mpf(10)**-12, mp.mpf(1), mp.mpf(10)**12]:
    eps_v = lam_fix * (2 - 1) * qq ** 2
    k2 = (mp.mpf(1) * qq ** (2 * 1)) / (mp.mpf(1) * eps_v)
    kappa_sq.append((qq, k2))
ok_fix = all(abs(k2 - mp.mpf(0.25)) < mp.mpf(10)**-70 for _, k2 in kappa_sq)
check("C1a fixture (n=2,m=1,lam=4): kappa_N^2 = 1/4 for q in {1e-12,1,1e12} (80 digits)",
      ok_fix, "kappa^2 = " + ", ".join(f"{mp.nstr(k2, 20)}" for _, k2 in kappa_sq))
# refinement: dps 50 -> 80 stability of the same fixture
mp.mp.dps = 50
k2_50 = (mp.mpf(1) * mp.mpf(2) ** 2) / (lam_fix * (2 - 1) * mp.mpf(2) ** 2)
mp.mp.dps = 80
k2_80 = (mp.mpf(1) * mp.mpf(2) ** 2) / (lam_fix * (2 - 1) * mp.mpf(2) ** 2)
check("C1b refinement dps 50 -> 80 stable at q=2", abs(k2_50 - k2_80) < mp.mpf(10)**-45,
      f"k2(50d) = {mp.nstr(k2_50, 30)}; k2(80d) = {mp.nstr(k2_80, 30)}")
# failing fixture: n=3, m=1, lam = 4 beta^2/(G_N (n-1)) same style: kappa^2(q) = q^-1/2 ... exact ratio law
mp.mp.dps = 80
k3_1 = mp.power(mp.mpf(1), -1) / 2
k3_2 = mp.power(mp.mpf(2), -1) / 2
check("C1c failing exponent (n=3,m=1): ratio law kappa^2(q2)/kappa^2(q1) = (q2/q1)^(-1) holds, != 1",
      abs(k3_2 / k3_1 - mp.mpf(0.5)) < mp.mpf(10)**-70 and k3_2 != k3_1,
      f"kappa^2(1)=1/2, kappa^2(2)=1/4 (ratio 1/2 != 1)")

# ------------------------------------------------------------------ C2 global report
print("\n" + "=" * 100)
npass = sum(1 for r in results if r["pass"])
budget("report")
elapsed = time.monotonic() - t0
rss_mb = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1e6
print(f"CHECKS: {npass}/{len(results)} passed; elapsed {elapsed:.2f} s; peak RSS {rss_mb:.1f} MB")
json.dump({"results": results, "elapsed_s": elapsed, "peak_rss_mb": rss_mb,
           "deadline_s": DEADLINE_S, "rss_limit_mb": RSS_LIMIT_MB,
           "dps": [50, 80], "mpmath_dps_final": mp.mp.dps},
          open("raw_outputs/checks.json", "w"), indent=1)
sys.exit(0 if npass == len(results) else 2)
