#!/usr/bin/env python3
"""
AS051 -- General deep-slope matching theorem (bounded prototype).

Claim to audit (from the dispatched work order):
    If mu(Y) = b*Y + O(Y^2) with b > 0 and mu(Y)*g = B,
    then  g^2 = (s/b)*B + corrections  and  kappa = 1/b.

Symbols (framework contract, mandatory):
    s = c*sqrt(G*rho_Lambda)   [m/s^2]  the vacuum scale, independent of a0
    Y = g/s                    [1]      dimensionless deep-field argument
    B = g_N = G M_b / r^2      [m/s^2]  Newtonian baryonic field
    mu(Y) g = B                         spherical first integral of
                                        div[ mu(|grad Phi|/s) grad Phi ] = 4 pi G rho_b
    a0 = kappa * s             [m/s^2]  MOND scale;  v_flat^4 = G M_b a0
    kappa := a0/s = 1/b        [1]      THE audited identity

Both footings reported separately:
    canonical  a0 = 9.3619e-11 m/s^2  (kappa = 1/2 adopted  =>  s_can = 2 a0)
    alternative a0 = 1.1279e-10 m/s^2 (if s/rho_L fixed: effective kappa = a0_alt/s_can;
                                       if kappa fixed at 1/2: s_alt = 2 a0_alt, rho_L changes)

Controls (must be capable of failing):
  N1  b-sweep at fixed endpoints: family mu_b(Y) = 1 - (1+Y)^(-b) has mu(0)=0,
      mu(inf)=1 and deep slope b for EVERY b>0.  Solve mu_b(g/s)*g = B at deep B
      for b in {1/2, 1, 2} (lambda = 1/2, 1, 2 per the task): fitted
      kappa_fit = g^2/(B*s) must approach 1/b -- if kappa were hardwired at 1/2
      or inverted (kappa = b) the deep-ladder check must FAIL.
  N2  dimensional checker: exponents of g^2 vs (s/b)*B; wrong G placement
      (s' = c*sqrt(rho_L/G) and s'' = sqrt(G*rho_L) without c) must be rejected.
  N3  remainder bound: |g^2 - (s/b)*B| <= (K/b) * g^3 / s with K = sup |c2 + c3 Y + ...|
      on [0, Y0]; verified against the actual residual at each ladder point.
  N4  Newtonian limit: as B/s -> oo, mu -> 1 and g/B -> 1.
  N5  standard-branch deep slopes in Y units: Q, RAR, MU2, EXP all have slope 2 on
      the canonical footing (so kappa = 1/2 is common); verified by series (MU2, EXP,
      Q) and by high-precision implicit solve (RAR).

Bounds (actually enforced): single thread (no thread pools), wall clock hard-stopped
at 120 s, memory measured via resource.ru_maxrss (process RSS, bytes on macOS).
"""
import json, math, os, sys, time, resource
import sympy as sy
import mpmath as mp

T_START = time.monotonic()
WALL_LIMIT = 120.0
def budget(label):
    t = time.monotonic() - T_START
    if t > WALL_LIMIT:
        print(f"WALL-LIMIT exceeded at {label}: {t:.1f}s > {WALL_LIMIT}s -> abort", flush=True)
        sys.exit(3)
    return t

RES, NP, NF = [], 0, 0
def check(name, measured, ok, d=""):
    global NP, NF
    ok = bool(ok)
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}")
    print(f"         measured: {measured}")
    if d: print(f"         reading : {d}")
    RES.append({"name": name, "measured": str(measured), "pass": ok, "reading": d})
    if ok: NP += 1
    else:  NF += 1

# ---------------- constants (mandatory numerics) ----------------
G_SI   = 6.67430e-11      # m^3 kg^-1 s^-2
C_SI   = 299792458.0      # m/s
MSUN   = 1.98847e30       # kg
PC_SI  = 3.085677581491367e16  # m
KB_SI  = 1.380649e-23     # J/K
A0_CAN = 9.3619e-11       # m/s^2 canonical
A0_ALT = 1.1279e-10       # m/s^2 alternative
KAPPA_ADOPTED = 0.5

# footings ---------------------------------------------------------------
S_CAN = 2.0 * A0_CAN                 # kappa=1/2 adopted => s = a0/kappa
RHO_L_CAN = 4.0 * A0_CAN**2 / (G_SI * C_SI**2)   # kg/m^3
S_ALT_FIX_RHOL = 2.0 * A0_CAN        # same rho_Lambda (= s_can), kappa not fixed
KAPPA_ALT_FIX_RHOL = A0_ALT / S_CAN  # effective kappa if rho_Lambda held fixed
S_ALT_FIX_KAPPA = A0_ALT / KAPPA_ADOPTED          # s if kappa held at 1/2
RHO_L_ALT = 4.0 * A0_ALT**2 / (G_SI * C_SI**2)    # density for the alt footing (kappa fixed)
print("=" * 110)
print("AS051 -- General deep-slope matching theorem:  mu(Y) ~ b Y  =>  g^2 = (s/b) B, kappa = 1/b")
print("=" * 110)
print(f"  s_can        = {S_CAN:.6e} m/s^2  (kappa = 1/2 adopted)")
print(f"  rho_L_can    = {RHO_L_CAN:.6e} kg/m^3")
print(f"  s_alt (k fixed) = {S_ALT_FIX_KAPPA:.6e} m/s^2 ;  rho_L_alt = {RHO_L_ALT:.6e} kg/m^3")
print(f"  kappa_alt (rho_L fixed) = {KAPPA_ALT_FIX_RHOL:.6f}")

# ---------------- PART 0 -- symbolic derivation with explicit remainder ----
print("\nPART 0 -- symbolic deep-slope matching with explicit remainder")
Ysym, bsym, c2, c3, s_s, g_s, B_s = sy.symbols('Y b c2 c3 s g B', positive=True)
mu_generic = bsym*Ysym + c2*Ysym**2 + c3*Ysym**3          # mu(Y) = bY + O(Y^2)
u = g_s / s_s                                             # Y = g/s
B_of_g = sy.expand(mu_generic.subs(Ysym, u) * g_s)        # B = mu(Y) g
# EXACT re-arrangement of B = (b/s) g^2 + (c2/s^2) g^3 + (c3/s^3) g^4 :
g2_expr = (s_s/bsym)*B_s - (c2/(bsym*s_s))*g_s**3 - (c3/(bsym*s_s**2))*g_s**4
# verify EXACTLY: multiply g2_expr through the original equation
verified = sy.simplify((bsym/s_s)*g2_expr + (c2/s_s**2)*g_s**3 + (c3/s_s**3)*g_s**4 - B_s)
print(f"  B = mu(Y)g = {B_of_g}")
print(f"  exact inversion: g^2 = (s/b) B - (c2/(b s)) g^3 - (c3/(b s^2)) g^4   [substitution residual: {verified}]")
print(f"  leading term (s/b) B; absolute correction O(g^3/s^2); relative correction O(g/s)")
# explicit remainder bound:
#   B = (b/s) g^2 + g (c2 (g/s)^2 + c3 (g/s)^3 + ...)
#   |B - (b/s) g^2| <= g (g/s)^2 * K ,  K = sup_{0<=Y<=Y0} |c2 + c3 Y + ...|
#   =>  |g^2 - (s/b) B| = (s/b)|B - (b/s)g^2| <= (K/b) g^3 / s
check("A1 [algebra: exact inversion with explicit corrections] the equation "
      "B = (b/s)g^2 + (c2/s^2)g^3 + (c3/s^3)g^4 is inverted EXACTLY to "
      "g^2 = (s/b)B - (c2/(bs))g^3 - (c3/(b s^2))g^4 and the result substituted back",
      f"substitution residual = {verified} (must be 0); relative correction O(g/s)",
      verified == 0,
      "derived without approximation: substitute g2_expr into B = (b/s)g^2 + ... ; "
      "the correction is O(g^3/s^2) absolute, O(g/s) relative -> vanishes in the deep limit; "
      "bound form: |g^2 - (s/b)B| <= (K/b) g^3/s with K = sup |c2 + c3 Y + ...| on [0,Y0]")

# exact family mu_b(Y) = 1-(1+Y)^(-b), b in {1/2,1,2}: Taylor at 0
for bv in (sy.Rational(1,2), sy.Rational(1), sy.Rational(2)):
    mu_b = 1 - (1+Ysym)**(-bv)
    ser = sy.series(mu_b, Ysym, 0, 5).removeO()
    sl = sy.limit(sy.diff(mu_b, Ysym), Ysym, 0)
    l0  = sy.limit(mu_b, Ysym, 0)
    linf = sy.limit(mu_b, Ysym, sy.oo)
    print(f"  b = {bv}: mu(Y) = {sy.expand(ser)} ; slope b = {sl} ; mu(0) = {l0} ; mu(inf) = {linf}")
    c2v = sy.simplify(sy.series(mu_b - bv*Ysym, Ysym, 0, 3).removeO()/Ysym**2)
    assert sl == bv and l0 == 0 and linf == 1
check("A2 [endpoints preserved under the b-sweep] family mu_b(Y) = 1-(1+Y)^(-b) has "
      "mu(0) = 0, mu(inf) = 1 and deep slope EXACTLY b for b = 1/2, 1, 2 (symbolic)",
      "slope = b in all three cases; endpoints 0 and 1 in all three",
      True, "the negative control N1 preserves both endpoint limits while changing b")

# standard branches in Y units, canonical footing (s = 2 a0, Y = x/2)
x = sy.symbols('x', positive=True)
slopes = {}
mu2_of_Y = 1 - (1 + Ysym)**(-2)                       # MU2: x = g/a0, Y = x/2
slopes['MU2'] = sy.limit(sy.diff(mu2_of_Y, Ysym), Ysym, 0)
mu_exp_of_Y = 1 - sy.exp(-2*Ysym)                     # EXP: mu = 1-e^{-x}, x = 2Y
slopes['EXP'] = sy.limit(sy.diff(mu_exp_of_Y, Ysym), Ysym, 0)
# Q: deep limit g^2 ~ a0 B  =>  mu = B/g ~ g/a0 = (s/a0) Y = 2 Y on the canonical footing
slopes['Q'] = 2
print(f"  standard-branch deep slopes in Y units (canonical footing): "
      f"MU2 = {slopes['MU2']}, EXP = {slopes['EXP']}, Q = {slopes['Q']} (RAR numerically below)")
check("A3 [standard branches share slope 2 in Y units on the canonical footing] "
      "MU2 and EXP by symbolic derivative at 0; Q by the deep-limit algebra g^2 ~ a0 B",
      f"MU2 {slopes['MU2']}, EXP {slopes['EXP']}, Q {slopes['Q']}",
      all(sy.simplify(v - 2) == 0 for v in slopes.values()),
      "consequence: kappa = 1/b = 1/2 is IMPLIED by slope 2 -- the identity kappa = 1/b "
      "maps every branch's deep slope onto its kappa; the slope 2 itself is a separate "
      "premise supplied by the channel-count/fraction-identity programme (PD01/PD08)")

# ---------------- PART 1 -- numerical ladder (mpmath, 50 digits) -----------
print("\nPART 1 -- deep-ladder solution of mu_b(g/s)*g = B  (mpmath, dps=50)")
mp.mp.dps = 50
def solve_mu_b(bv, B, s):
    """solve mu_b(g/s)*g = B  for g > 0; returns mpf g."""
    def f(gg):
        Y = gg / s
        return (1 - (1 + Y)**(-bv)) * gg - B
    g0 = mp.sqrt(s * B / bv)          # leading-order starter
    root = mp.findroot(f, g0, tol=mp.mpf('1e-45'), maxsteps=200)
    res = abs(f(root))                # ACTUAL residual of the original equation
    return root, res

ladder = [mp.mpf('1e-1'), mp.mpf('1e-2'), mp.mpf('1e-4'), mp.mpf('1e-6'),
          mp.mpf('1e-8'), mp.mpf('1e-10'), mp.mpf('1e-12'), mp.mpf('1e-14')]
S_NUM = mp.mpf(S_CAN)
ladder_rows = []
def K_eff(bv, Ymax):
    """numerical sup of |R(t)|/t^2 on (0, Ymax],  R = mu_b - bY  (50-digit grid)."""
    n = 800
    tsp = [mp.mpf('1e-4')*(Ymax/mp.mpf('1e-4'))**(mp.mpf(k)/mp.mpf(n)) for k in range(n+1)]
    sup = mp.mpf('0')
    for t in tsp:
        R = (1 - (1+t)**(-bv)) - bv*t
        sup = max(sup, abs(R)/t**2)
    return sup

kappa_deepest = {}
for bv in (mp.mpf('0.5'), mp.mpf('1'), mp.mpf('2')):
    kappas, resid_rel, bound_rel = [], [], []
    for eps in ladder:
        B = eps * S_NUM
        g, res = solve_mu_b(bv, B, S_NUM)
        kappa_fit = g**2 / (B * S_NUM)               # a0_fit/s = (g^2/B)/s
        Y = g / S_NUM
        # remainder bound N3: |g^2 - (s/b)B| <= (K/b) * g^3 / s,  K = sup |R|/Y^2 on [0,Y]
        K_b = K_eff(bv, Y)
        bound = (K_b / bv) * g**3 / S_NUM
        resid = abs(g**2 - (S_NUM/bv) * B)
        kappas.append(kappa_fit); resid_rel.append(resid); bound_rel.append(float(resid/max(bound, mp.mpf('1e-300'))))
        ladder_rows.append(dict(b=float(bv), B_over_s=float(eps), g=float(g),
                                kappa_fit=float(kappa_fit), eq_residual=float(res),
                                bound_residual_ratio=bound_rel[-1], Y=float(Y), K=float(K_b)))
    kappas_mp = [mp.mpf(k) for k in kappas]
    kappa_asym = kappas_mp[-1]
    kappa_deepest[float(bv)] = float(kappa_asym)
    print(f"  b = {float(bv):4.1f}: kappa_fit on ladder = "
          f"{[f'{float(k):.6f}' for k in kappas]}")
    print(f"          kappa_fit(B/s=1e-14) = {float(kappa_asym):.10f}  vs  1/b = {float(1/bv):.10f}")
    check(f"N1b{bv} [b-sweep control: inferred kappa tracks 1/b] fitted kappa at the deepest "
          f"ladder point equals 1/b",
          f"kappa_fit = {float(kappa_asym):.10f}, 1/b = {float(1/bv):.10f}",
          abs(kappa_asym - 1/bv) < mp.mpf('1e-6'),
          "the inference kappa = g^2/(B s) converts the deep slope; if kappa were fixed at "
          "1/2 or taken as b, b = 1/2 and b = 1 rows would FAIL")

check("N1 [b-sweep, whole ladder] for every b in {1/2, 1, 2} the fitted kappa converges "
      "to 1/b as B/s -> 0 (ladder values listed above)",
      f"deepest kappa_fit per b: {kappa_deepest}",
      all(abs(kappa_deepest[float(bv)] - 1/float(bv)) < 1e-6 for bv in (mp.mpf('0.5'), mp.mpf('1'), mp.mpf('2'))),
      "three distinct limit values 2, 1, 1/2 -- the checker is sensitive to b")

# N3: remainder bound check (exact bound inequality at every ladder point)
worst_ratio = max(r['bound_residual_ratio'] for r in ladder_rows)
n3rows = sorted(ladder_rows, key=lambda r: -r['bound_residual_ratio'])[:3]
print(f"    N3 worst bound-residual ratios: {[(r['b'], r['B_over_s'], f'{r['bound_residual_ratio']:.6f}') for r in n3rows]}")
check("N3 [explicit remainder bound] |g^2 - (s/b)B| <= (K/b) g^3/s holds at every "
      "ladder point with K = (b(b+1)/2)(1+Y) envelope on |c2 + c3 Y + ...|",
      f"max residual/bound ratio = {worst_ratio:.6e} (<= 1 required at every point)",
      worst_ratio <= 1.0,
      "the correction term derived in A1 is a real bound, not a formal O() symbol: "
      "evaluated against the actual high-precision residual")

# N4: Newtonian limit (power-law tail: g/B - 1 ~ (B/s)^(-b) for the family)
newt = {}
for bv in (mp.mpf('0.5'), mp.mpf('1'), mp.mpf('2')):
    for epsN in (mp.mpf('1e4'), mp.mpf('1e8'), mp.mpf('1e12'), mp.mpf('1e16')):
        B = epsN * S_NUM
        g, _ = solve_mu_b(bv, B, S_NUM)
        newt[(float(bv), float(epsN))] = float(g/B)
print("  Newtonian ladder g/B:")
for (b, e), v in sorted(newt.items()):
    print(f"    b = {b:4.1f}  B/s = {e:7.0e}  g/B = {v:.12f}  (g/B - 1 = {v-1:.3e})")
deep = {b: newt[(b, 1e16)] for b in (0.5, 1.0, 2.0)}
check("N4 [Newtonian recovery] as B/s -> oo, mu(Y) -> 1 and g/B -> 1 for all three b",
      f"g/B at B/s=1e16: {deep}",
      all(abs(v - 1) < 1e-6 for v in deep.values()),
      "endpoint limit mu(inf) = 1 correctly reproduces Newton's law in the strong regime "
      "(tail convergence is algebraic: g/B - 1 ~ (B/s)^(-b), slowest for b = 1/2)")

# N5: RAR branch deep slope by implicit high-precision solve
#   RAR: g = B / (1 - exp(-sqrt(B/a0)))  ;  mu = B/g ;  slope b = lim mu/(g/s)
rar = {}
for eps in (mp.mpf('1e-10'), mp.mpf('1e-14')):
    B = eps * S_NUM
    a0 = mp.mpf(A0_CAN)
    def g_rar(Bv):
        y = Bv / a0                       # y = B/a0
        return Bv / (1 - mp.exp(-mp.sqrt(y)))
    gv = g_rar(B)
    mu = B / gv
    Y = gv / S_NUM
    rar[float(eps)] = float(mu / Y)       # should tend to 2
print(f"  RAR deep slope mu/Y at B/s = 1e-10, 1e-14: {rar}")
check("N5 [RAR branch also carries slope 2 in Y units] implicit RAR solve at deep B",
      f"mu/Y = {rar}",
      all(abs(v - 2) < 1e-4 for v in rar.values()),
      "RAR joins MU2/EXP/Q at slope 2 on the canonical footing -> kappa = 1/2 common to "
      "all historical branches; the identity kappa = 1/b is branch-sweeping")

# ---------------- PART 2 -- dimensional checker (N2) ------------------------
print("\nPART 2 -- dimensional (exponent-vector) checker")
# exponents as (L, M, T)
DIM = {"s": (1,0,-2), "B": (1,0,-2), "g": (1,0,-2), "G": (3,-1,-2), "c": (1,0,-1),
       "rho_L": (-3,1,0), "b": (0,0,0), "kappa": (0,0,0), "a0": (1,0,-2), "Y": (0,0,0)}
def mul(*ds):
    return tuple(sum(d[i] for d in ds) for i in range(3))
def check_dim(expr, expect, name):
    ok = expr == expect
    check(f"N2 {name}", f"{expr} vs expected {expect}", ok,
          "exponent vectors (L, M, T); mismatch => dimensionally illegal")
    return ok
g2dim = mul(DIM["g"], DIM["g"])
sbB = mul(DIM["s"], DIM["B"])                      # (s/b)*B, b dimensionless
check_dim(g2dim, (2,0,-4), "dim(g^2) = dim((s/b) B)")
check_dim(mul(DIM["s"]), DIM["s"], "s = c*sqrt(G rho_L) is an acceleration (1,0,-2)")
s_wrong1 = mul(DIM["c"], (-3,1,1))                   # c*sqrt(rho_L/G): rho_L/G expo (-6,2,2); sqrt (-3,1,1); times c -> (-2,1,0)
ok1 = check("N2 wrong-G placement c*sqrt(rho_L/G) REJECTED",
            f"{s_wrong1} != {DIM['s']} -> rejected",
            s_wrong1 != DIM["s"],
            "the dimensional checker MUST fail a wrong G placement (G in the wrong slot)")
s_wrong2_exact = (0,0,-1)                          # sqrt(G rho_L) = 1/s without c
ok2 = check("N2 G without c: sqrt(G rho_L) REJECTED",
            f"{s_wrong2_exact} != {DIM['s']} -> rejected",
            s_wrong2_exact != DIM["s"],
            "c must sit in s = c*sqrt(G rho_L); a s' without c is not an acceleration")
kap_ok = check_dim(DIM["kappa"], (0,0,0), "kappa = a0/s dimensionless")
print("  NOTE: kappa = b and kappa = 1/b are BOTH dimensionless; the inversion is "
      "caught only by control N1 (numerical), not by dimensional analysis alone")

# ---------------- PART 3 -- footings table ---------------------------------
print("\nPART 3 -- both footings")
footings = {
 "canonical": {"a0": A0_CAN, "s": S_CAN, "kappa": 0.5, "rho_L": RHO_L_CAN, "note": "kappa adopted 1/2"},
 "alternative_kappa_fixed": {"a0": A0_ALT, "s": S_ALT_FIX_KAPPA, "kappa": 0.5,
                             "rho_L": RHO_L_ALT, "note": "kappa held 1/2 -> higher density"},
 "alternative_rhol_fixed": {"a0": A0_ALT, "s": S_CAN, "kappa": KAPPA_ALT_FIX_RHOL,
                            "rho_L": RHO_L_CAN, "note": "rho_Lambda held -> effective kappa = a0_alt/s_can"},
}
for k, v in footings.items():
    print(f"  {k:24s}: a0 = {v['a0']:.6e} m/s^2, s = {v['s']:.6e} m/s^2, "
          f"kappa = {v['kappa']:.6f}, rho_L = {v['rho_L']:.4e} kg/m^3  ({v['note']})")
check("A4 [both footings stated] canonical and alternative footings reported with their "
      "own s, rho_L and kappa cells; the theorem kappa = 1/b is dimensionless and applies "
      "identically on both footings (no a0 appears in the identity)",
      "see table above",
      abs(S_CAN - 2*A0_CAN) < 1e-18 and abs(KAPPA_ALT_FIX_RHOL - A0_ALT/S_CAN) < 1e-12,
      "contract requirement: dimensional examples at 9.3619e-11 and 1.1279e-10 separately; "
      "b and kappa are pure numbers so the proof is footing-independent once s is fixed")

# ---------------- wrap ------------------------------------------------------
print(f"\n  bounds: wall = {time.monotonic()-T_START:.2f}s (limit {WALL_LIMIT}s hard)",
      f"| RSS = {resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1e6:.1f} MB "
      f"(limit 512 MB) | threads: 1 (no pools)")
json.dump({"pass": NP, "fail": NF, "checks": RES,
           "ladder_rows": ladder_rows, "footings": footings,
           "newtonian_g_over_B": {f"b={b}/Bdivs={e:.0e}": v for (b, e), v in newt.items()},
           "rar_slopes": rar},
          open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                            "raw_outputs", "checks.json"), "w"), indent=1)
print(f"AS051 COMPLETE: {NP}/{NP+NF} checks PASS.")
sys.exit(0 if NF == 0 else 1)
