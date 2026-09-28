#!/usr/bin/env python3
"""
AS652 -- four-form flux equation with a MOND-dependent scale (Tier-0 seed)
===========================================================================
Branch: k04 four-form promotion (pinned 15c0a7e1...) x saturated RAR kernel.
Construction: a0(q) = beta*sqrt(G_N)*|q|, L = P(q) + L_MOND(a0(q)),
  P(q) = (Z/2) q^2 + b beta^2 q^2,  L_MOND = -(2-K_B) J/(16 pi G_mon),
  J = a0^2 j(s), s = g_N/a0, branch identities Y J_Y = a0^2 s Delta(s),
  dJ/da0|_Y = (2/a0)(J - Y J_Y) = -2 a0 W(s), W = s Delta - j.
Flux equation (task step 2):  d_mu(dL/dq) = 0  =>  dL/dq = Z q0  (integration
  constant = four-form flux datum; NOT P_q = 0).
  dL/dq = Z q + 2 b beta^2 q + (2-K_B) beta^2 q W(s) (G_N/G_mon)/(8 pi) = Z q0.
  Gauge-fixed branch (k04): the 2b beta^2 q term is the q-variation of the
  promoted vacuum primitive (AS067 zero-mode gauge); k04's flux equation omits
  it.  Both variants are computed; all k04 comparisons use the gauge-fixed
  equation  q[Z + (2-K_B) beta^2 W/8 pi] = Z q0  with Z = 8 beta^2 (kappa=1/2).
Fixed point:  r = a0_loc/a0 = q/q0 solves  r (1 + (2-K_B) W(g_N/(a0 r))/64 pi) = 1.
Controls: units/signs/normalization; negative control (q unconstrained
  algebraic scalar -> dL/dq = 0 -> q = 0 only); stability per XR31
  (C_L,eff = dg_N/dg_phi < 0 on the band 2.385..155.2 a0).
Bounds: wall <= 120 s (signal.alarm, hard), memory <= 512 MB (RLIMIT_AS, hard),
  1 thread (no threading/multiprocessing/subprocess).
"""
import hashlib, json, math, os, signal, sys, time, resource

# ---------------- hard bounds ----------------
signal.alarm(120)  # hard wall clock
MEM_CAPPED = False
try:
    resource.setrlimit(resource.RLIMIT_AS, (512 * 1024 * 1024, 512 * 1024 * 1024))
    MEM_CAPPED = True
except Exception as e:
    print("RLIMIT_AS not settable (macOS):", e, file=sys.stderr)
    print("memory will be MEASURED, not hard-capped; declared cap 512 MB", file=sys.stderr)

import mpmath as mp
mp.mp.dps = 50
import sympy as sp

T0 = time.time()
RUN = os.path.dirname(os.path.abspath(__file__))
REPO = "/Users/carlzimmerman/new_physics/zimmerman-formula"
TASK = os.path.join(REPO, "deepseek_push/astra_spawn_ideas/AS652_four_form_flux_equation_with_a_mond_dependent_scale.md")
K04 = os.path.join(REPO, "kappa_closure/k04_four_form_promotion_consistency.py")
MANIFEST = os.path.join(REPO, "deepseek_push/astra_spawn_ideas/SOURCE_MANIFEST.json")

def sha256(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()

# ---------------- constants (framework numerics) ----------------
G_N = mp.mpf("6.67430e-11")     # m^3 kg^-1 s^-2  (Newton coupling, galactic)
C_L = mp.mpf("299792458")       # m/s
M_SUN = mp.mpf("1.98847e30")    # kg
PC = mp.mpf("3.085677581491367e16")  # m
AU = mp.mpf("1.495978707e11")   # m (IAU 2012)
A0 = {"canonical": mp.mpf("9.3619e-11"), "alt": mp.mpf("1.1279e-10")}  # m/s^2
PI = mp.pi

# ---------------- kernel (k04 saturated RAR) ----------------
def Delta(s):
    if s <= 0:
        return mp.mpf(0)
    return s / mp.expm1(mp.sqrt(s))

s_sat = mp.findroot(lambda s: mp.diff(Delta, s), mp.mpf("2.54"))
D_sat = Delta(s_sat)
I_rar = 2 * (s_sat * D_sat - mp.quad(Delta, [0, s_sat]))
def j_of(s):
    if s <= s_sat:
        return 2 * (s * Delta(s) - mp.quad(Delta, [0, s]))
    return I_rar
def Dl(s):  # frozen (saturated) kernel
    return Delta(s) if s <= s_sat else D_sat
def W(s):   # s Delta - j  (>= 0, strictly increasing, W(0)=0)
    return s * Dl(s) - j_of(s)

# ---------------- symbolic part ----------------
q, Z, b, beta, q0, KB, Wsym, pi_s = sp.symbols(
    "q Z b beta q0 K_B W pi", positive=True)
q = sp.Symbol("q")  # q must be unconstrained: the negative control's root IS q = 0
P = Z * q**2 / 2 + b * beta**2 * q**2
eps = sp.simplify(q * sp.diff(P, q) - P)
kappa2 = sp.simplify(beta**2 * q**2 / eps)  # a0^2/(G eps_vac): G cancels exactly
ratio_needed = sp.solve(sp.Eq(kappa2, sp.Rational(1, 4)), Z)[0] / beta**2
# flux equation (gauge-fixed, k04):  q[Z + (2-K_B) beta^2 W/8pi] = Z q0
alpha_s = 2 - KB
flux_lhs = q * (Z + alpha_s * beta**2 * Wsym / (8 * pi_s))
flux_sol = sp.solve(sp.Eq(flux_lhs, Z * q0), q)[0]
flux_res = sp.simplify(flux_lhs.subs(q, flux_sol) - Z * q0)
nc_sol = sp.solve(sp.Eq(flux_lhs, 0), q)  # negative control: dL/dq = 0
# full-variation variant (with 2b beta^2 q)
flux_lhs_full = q * (Z + 2 * b * beta**2 + alpha_s * beta**2 * Wsym / (8 * pi_s))
flux_sol_full = sp.solve(sp.Eq(flux_lhs_full, Z * q0), q)[0]

# ---------------- numeric machinery ----------------
def r_fixed(gN, a0, KBv, tol=mp.mpf("1e-40")):
    """Unique root r in (0,1] of r*(1 + alpha*W(gN/(a0 r))/64pi) = 1.
    Exists iff gN < g_star; returns (r, exists)."""
    alpha = 2 - KBv
    g_star = 64 * PI * a0 / (alpha * D_sat)
    if gN >= g_star:
        return mp.mpf(0), False
    lo, hi = mp.mpf(0), mp.mpf(1)
    for _ in range(300):
        mid = (lo + hi) / 2
        s = gN / (a0 * mid)
        F = mid * (1 + alpha * W(s) / (64 * PI)) - 1
        if F > 0:
            hi = mid
        else:
            lo = mid
        if hi - lo < tol:
            break
    r = (lo + hi) / 2
    return r, True

def flux_residual(gN, a0, KBv, r):
    """Relative residual of the gauge-fixed flux equation at the fixed point."""
    alpha = 2 - KBv
    s = gN / (a0 * r)
    # q/q0 = r;  equation: r*(Z + alpha beta^2 W/8pi) = Z  (Z = 8 beta^2)
    lhs = r * (8 + alpha * W(s) / (8 * PI))   # in units of beta^2
    return abs(lhs - 8) / 8

def g_phi(gN, a0, KBv):
    r, ok = r_fixed(gN, a0, KBv)
    if not ok:
        return mp.mpf(0)
    s = gN / (a0 * r)
    return a0 * r * Dl(s)

# ---------------- checks ----------------
CHECKS = []
def check(name, ok, detail=""):
    CHECKS.append({"name": name, "pass": bool(ok), "detail": str(detail)})
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"   ({detail})" if detail else ""), flush=True)

print("=" * 110)
print("AS652 -- four-form flux equation with a MOND-dependent scale")
print("=" * 110)

# ---- S1/S2 hashes ----
h_task = sha256(TASK)
h_k04 = sha256(K04)
man = json.load(open(MANIFEST))
h_k04_man = man["sources"]["kappa_closure/k04_four_form_promotion_consistency.py"]
check("S1 task sha256 == pinned 9f3281d9...", h_task == "9f3281d9697c338ef70adb08f74f33f009a4a07ea2a86682a51b477613b50b2e", h_task)
check("S2 k04 source == SOURCE_MANIFEST 15c0a7e1...", h_k04 == h_k04_man, h_k04)

# ---- kernel landmarks ----
print(f"  kernel: s_sat = {mp.nstr(s_sat, 12)}, Delta_sat = {mp.nstr(D_sat, 12)}, I_rar = j_sat = {mp.nstr(I_rar, 12)}")
check("K1 Delta'(s_sat) = 0 (residual)", abs(mp.diff(Delta, s_sat)) < mp.mpf("1e-30"), mp.nstr(mp.diff(Delta, s_sat), 6))
Wgrid = [W(s) for s in [mp.mpf("1e-6"), mp.mpf("0.01"), mp.mpf("0.1"), mp.mpf("1"), mp.mpf("2.54"), mp.mpf("10"), mp.mpf("100"), mp.mpf("1e4")]]
check("K2 W = s Delta - j >= 0 on grid (secant stiffness; NOT a stability statement per XR31)", min(Wgrid) >= 0, f"min W = {mp.nstr(min(Wgrid), 6)}")
# W monotone increasing: numeric derivative > 0
Wmono = all(mp.diff(W, s) > 0 for s in [mp.mpf("0.01"), mp.mpf("0.5"), mp.mpf("1"), mp.mpf("2.54"), mp.mpf("10")])
check("K3 W strictly increasing (analytic: d(Delta/s)/ds < 0; numeric)", Wmono)
# deep asymptote W ~ s^{3/2}/3
wdeep = W(mp.mpf("1e-6")) / (mp.mpf("1e-6") ** mp.mpf("1.5"))
check("K4 deep asymptote W ~ s^{3/2}/3", abs(wdeep - mp.mpf(1) / 3) < mp.mpf("1e-3"), f"W/s^{{3/2}} = {mp.nstr(wdeep, 8)}")

# ---- F1 sign (symbolic) ----
check("F1 [sign] eps = q P_q - P = +Z q^2/2 + b beta^2 q^2 (promoted primitive gravitates positive)",
      sp.simplify(eps - (Z * q**2 / 2 + b * beta**2 * q**2)) == 0, str(eps))
# ---- F2 coefficient ----
b_num = {0.0: float((2 - 0.0) * I_rar / (16 * PI)), 0.25: float((2 - 0.25) * I_rar / (16 * PI))}
ratio_num = {k: float(ratio_needed.subs(b, sp.Float(v))) for k, v in b_num.items()}
print(f"  F2: kappa^2 = {kappa2};  kappa = 1/2 <=> Z/beta^2 = 8 - 2b = {ratio_num}")
check("F2 [coefficient] the action fixes Z/beta^2 (kappa=1/2 needs 8-2b ~ 7.96); it is a free ratio of two couplings",
      False, "one number, undetermined: the flux amplitude cancels from kappa (k04 F2 FAIL stands; this is the seed's core finding)")
# ---- F3 feedback ----
S0 = [mp.mpf("1e-6"), mp.mpf("0.01"), mp.mpf("0.1"), mp.mpf("1"), mp.mpf("2.54"), mp.mpf("10"), mp.mpf("100"), mp.mpf("1000")]
rows = []
for KBv in (0.0, 0.25):
    for foot, a0 in A0.items():
        for s0 in S0:
            gN = s0 * a0
            r, ok = r_fixed(gN, a0, KBv)
            if ok:
                s = gN / (a0 * r)
                gobs_p = gN + a0 * r * Dl(s)
                gobs_0 = gN + a0 * Dl(s0)
                dlog = mp.log10(gobs_p / gobs_0)
                res = flux_residual(gN, a0, KBv, r)
            else:
                s, dlog, res = None, None, None
            rows.append(dict(KB=KBv, foot=foot, s0=float(s0), r=float(r), ok=ok,
                             dlog=float(dlog) if dlog is not None else None,
                             res=float(res) if res is not None else None))
for KBv in (0.0, 0.25):
    line = ", ".join(f"s={r['s0']:g}: {r['r']:.4f}" for r in rows if r["KB"] == KBv and r["foot"] == "canonical")
    print(f"  F3: K_B = {KBv:.2f} canonical: a0_loc/a0: {line}")
ok_rows = [r for r in rows if r["ok"] and r["s0"] <= 100]
check("F3 [feedback] unique root in (0,1) for g_N <= 100 a0, |Delta log g_obs| < 0.01 dex (both footings, K_B 0-0.25)",
      all(abs(r["dlog"]) < 0.01 for r in ok_rows),
      f"max |dlog| = {max(abs(r['dlog']) for r in ok_rows):.4f} dex")
check("F3b [feedback] flux-equation residual at fixed point < 1e-30 (substitution verification)",
      all(r["res"] is not None and r["res"] < mp.mpf("1e-30") for r in rows if r["ok"]),
      f"worst residual = {max(r['res'] for r in rows if r['ok']):.2e}")
# k04 comparison (gauge-fixed, K_B=0, canonical): k04 printed r values
k04_r = {0.01: 1.0000, 0.1: 0.9999, 1: 0.9968, 2.54: 0.9881, 10: 0.9398, 100: 0.3574}
cmp_ok = all(abs(r["r"] - k04_r[r["s0"]]) < 5e-4 for r in rows if r["KB"] == 0.0 and r["foot"] == "canonical" and r["s0"] in k04_r)
check("F3c [feedback] r(s0) matches k04 printed values within 5e-4 (gauge-fixed branch, framework numerics)", cmp_ok,
      "; ".join(f"s={r['s0']:g}: {r['r']:.4f}" for r in rows if r["KB"] == 0.0 and r["foot"] == "canonical" and r["s0"] in k04_r))
# s0 = 1000: no smooth root (g_N > g_*); k04's 0.0000 row is the map's spurious fixed point
r1000 = [r for r in rows if r["s0"] == 1000 and r["KB"] == 0.0 and r["foot"] == "canonical"][0]
check("F3d [feedback] s0=1000: g_N > g_* -> NO smooth root (k04's 0.0000 row is the iteration's spurious fixed point, not a flux-equation solution)",
      r1000["ok"] is False, f"g_N = 1000 a0 > g_* = {155.2:.1f} a0")

# ---- F4 solar system ----
A_SUN = {foot: a0 / (2 * 1278.0) for foot, a0 in A0.items()}
PLANETS = {"Mercury": 0.387, "Venus": 0.723, "Earth": 1.0, "Mars": 1.524,
           "Jupiter": 5.203, "Saturn": 9.58, "Uranus": 19.2, "Neptune": 30.05}
g_star = {foot: 64 * PI * a0 / (2 * D_sat) for foot, a0 in A0.items()}  # K_B = 0
print(f"  F4: g_* = 64 pi a0/((2-K_B) Delta_sat) = {mp.nstr(g_star['canonical'], 8)} (canonical), {mp.nstr(g_star['alt'], 8)} (alt) m/s^2")
ss = {}
for foot, a0 in A0.items():
    for name, au in PLANETS.items():
        gN = G_N * M_SUN / (au * AU) ** 2
        r, ok = r_fixed(gN, a0, 0.0)
        gphi = a0 * r * D_sat if ok else mp.mpf(0)
        ss[(foot, name)] = dict(gN=float(gN), gphi=float(gphi), over=float(gphi / A_SUN[foot]), ok=ok)
    print(f"    {foot:9s} residual g_phi vs sunward bound {mp.nstr(A_SUN[foot], 4)} m/s^2: " +
          ", ".join(f"{n} {ss[(foot, n)]['gphi']:.1e} ({ss[(foot, n)]['over']:.1f}x)" for n in ("Mercury", "Earth", "Saturn", "Neptune")))
check("F4 [Solar System] all planets in the switch-off core (g_N > g_*): residual phantom force 0 < sunward bound",
      all(not v["ok"] and v["gphi"] == 0.0 for v in ss.values()),
      f"largest residual/bound = {max(v['over'] for v in ss.values()):.1e}; switch-off radius (1 M_sun) = {mp.nstr(mp.sqrt(G_N*M_SUN/g_star['canonical'])/AU, 6)} AU")
r_off = mp.sqrt(G_N * M_SUN / g_star["canonical"]) / AU
check("F4b [Solar System] shut-off radius ~ 639 AU (XR31)", abs(r_off - 639) / 639 < 0.01, f"r_off = {mp.nstr(r_off, 7)} AU")

# ---- F5 wide binaries ----
wb = {}
for foot, a0 in A0.items():
    for kau in (2, 3, 5, 10, 20):
        gN = G_N * 1.5 * M_SUN / (kau * 1e3 * AU) ** 2
        r, ok = r_fixed(gN, a0, 0.0)
        wb[(foot, kau)] = dict(s0=float(gN / a0), r=float(r), ok=ok, dgam=0.1155 * math.log(float(r)) if ok else None)
    print(f"    F5: {foot:9s} a0_loc/a0 at 2,3,5,10,20 kAU (1.5 M_sun): " +
          ", ".join(f"{wb[(foot, k)]['r']:.3f} (dgamma_v {wb[(foot, k)]['dgam']:+.4f})" for k in (2, 3, 5, 10, 20)))
check("F5 [wide binaries] |dgamma_v| < DR4 +/-0.015 at 2 kAU (k04 F5 FAIL stands; per XR31 the 2 kAU point sits on the unstable band and is not a prediction)",
      False, f"largest |dgamma_v| = {max(abs(wb[(f, k)]['dgam']) for f in A0 for k in (2,3)):.4f} at 2 kAU (computed on the C_L,eff < 0 band)")

# ---- S4 stability (XR31) ----
def dgphi_dgN(gN, a0, KBv):
    h = gN * mp.mpf("1e-6")
    return (g_phi(gN + h, a0, KBv) - g_phi(gN - h, a0, KBv)) / (2 * h)
# bracket the peak: sign change + -> - of dg_phi/dg_N between grid points
g0 = A0["canonical"]
prev, prev_d = None, None
peak_bracket = None
for g_a0 in (mp.mpf("1.0"), mp.mpf("1.5"), mp.mpf("2.0"), mp.mpf("2.2"), mp.mpf("2.3"),
             mp.mpf("2.4"), mp.mpf("2.5"), mp.mpf("3.0"), mp.mpf("5.0")):
    d = dgphi_dgN(g_a0 * g0, g0, 0.0)
    if prev_d is not None and prev_d > 0 and d <= 0:
        peak_bracket = (prev, g_a0)
        break
    prev, prev_d = g_a0, d
assert peak_bracket is not None, "peak bracket not found"
g_peak = mp.findroot(lambda g: dgphi_dgN(g, g0, 0.0),
                     (peak_bracket[0] * g0, peak_bracket[1] * g0))
g_peak_a0 = g_peak / g0
CL20 = 1 / dgphi_dgN(mp.mpf("20") * g0, g0, 0.0)
print(f"  S4: g_phi(g_N) peaks at g_N = {mp.nstr(g_peak_a0, 7)} a0; C_L,eff(20 a0) = {mp.nstr(CL20, 7)}")
check("S4 [stability] g_phi peak at 2.385 a0 (XR31)", abs(g_peak_a0 - 2.385) / 2.385 < 0.01, mp.nstr(g_peak_a0, 7))
check("S4b [stability] C_L,eff = dg_N/dg_phi < 0 on the band (2.385, 155.2) a0; at 20 a0 ~ -238.6 (XR31)",
      CL20 < 0 and abs(CL20 + 238.6) / 238.6 < 0.01, mp.nstr(CL20, 7))
band = [g_phi(g * A0["canonical"], A0["canonical"], 0.0) for g in (3, 10, 50, 100, 150)]
band_ok = all(g_phi(g * A0["canonical"], A0["canonical"], 0.0) < g_phi(mp.mpf("2.385") * A0["canonical"], A0["canonical"], 0.0) for g in (3, 10, 50, 100, 150))
check("S4c [stability] g_phi falls monotonically on the band (fold to switch-off)", band_ok)

# ---- S5 uniqueness / contraction ----
def Fmap(r, gN, a0, KBv):
    alpha = 2 - KBv
    s = gN / (a0 * r)
    return 1 / (1 + alpha * W(s) / (64 * PI))
uniq = True
maxdT = mp.mpf(0)
for s0 in (0.1, 1, 2.54, 10, 100):
    gN = s0 * A0["canonical"]
    r, ok = r_fixed(gN, A0["canonical"], 0.0)
    dT = mp.diff(lambda x: Fmap(x, gN, A0["canonical"], 0.0), r)
    maxdT = max(maxdT, abs(dT))
    if not (ok and abs(dT) < 1):
        uniq = False
check("S5 [uniqueness] fixed-point map is a contraction at the root (|T'| < 1) on the tested grid", uniq,
      f"max |T'| = {mp.nstr(maxdT, 3)}")

# ---- S6 deep limit ----
r_deep, ok_deep = r_fixed(mp.mpf("1e-6") * A0["canonical"], A0["canonical"], 0.0)
check("S6 [deep limit] r -> 1 as g_N -> 0 (global a0 restored; W ~ s^{3/2}/3 -> 0)", ok_deep and abs(r_deep - 1) < mp.mpf("1e-9"), f"r(1e-6 a0) = {mp.nstr(r_deep, 12)}")

# ---- S7 saturated linear regime ----
g_star_c = g_star["canonical"]
lin_ok = True
for frac in (0.1, 0.5, 0.9):
    gN = frac * g_star_c
    r, ok = r_fixed(gN, A0["canonical"], 0.0)
    r_lin = (1 - frac) / (1 - 2 * I_rar / (64 * PI))
    if not (ok and abs(r / r_lin - 1) < mp.mpf("1e-4")):
        lin_ok = False
check("S7 [saturated linear] r_lin = (1 - g/g_*)/(1 - 2 j_sat/64 pi) matches the numeric root within 1e-4", lin_ok)
r_at_star, ok_at_star = r_fixed(g_star_c, A0["canonical"], 0.0)
check("S7b [saturated linear] r(g_*) = 0 exactly (switch-off endpoint)", (not ok_at_star) or r_at_star < mp.mpf("1e-12"), f"r(g_*) = {mp.nstr(r_at_star, 6)}")
r_above, ok_above = r_fixed(mp.mpf("1.01") * g_star_c, A0["canonical"], 0.0)
check("S7c [saturated linear] no smooth root for g_N > g_* (kink switch-off; q=0 only in the subdifferential sense)", not ok_above)

# ---- S8 negative control ----
nc_eq = sp.factor(flux_lhs)
nc = sp.solve(sp.Eq(nc_eq, 0), q)
check("S8 [negative control] q unconstrained algebraic scalar: dL/dq = 0 admits ONLY q = 0 (Z>0, W>=0; no fine-tuned pole)",
      len(nc) == 1 and sp.simplify(nc[0]) == 0, f"solutions: {nc} of {nc_eq}")
s0nc = mp.mpf("0.1")
dlog_nc = mp.log10(1 + Delta(s0nc) / s0nc)
check("S8b [negative control] the altered premise loses the MOND scale: at s0 = 0.1 the RAR predicts g_obs/g_N = 1 + Delta/s = 3.69 (+0.567 dex); the control gives 0",
      dlog_nc > mp.mpf("0.5"), f"lost RAR signal = {mp.nstr(dlog_nc, 6)} dex (control misses it entirely)")

# ---- S9 footings ----
foot = {}
for name, a0 in A0.items():
    rhoL = 4 * a0**2 / (G_N * C_L**2)
    epsL = rhoL * C_L**2
    tau = a0 / mp.sqrt(G_N)          # beta*q0 = a0/sqrt(G_N)
    rM = mp.sqrt(G_N * 1.5 * M_SUN / a0)
    vflat4 = G_N * 1.5 * M_SUN * a0
    foot[name] = dict(a0=float(a0), rhoL=float(rhoL), epsL=float(epsL), tau=float(tau),
                      rM_pc=float(rM / PC), vflat4=float(vflat4), g_star=float(g_star[name]))
    print(f"  S9 {name:9s}: rho_Lambda = {mp.nstr(rhoL, 10)} kg/m^3, eps_Lambda = {mp.nstr(epsL, 10)} J/m^3, "
          f"beta*q0 = {mp.nstr(tau, 8)} kg^1/2 m^-1/2 s^-1, r_M(1.5 M_sun) = {mp.nstr(rM/PC, 8)} pc, "
          f"v_flat^4 = {mp.nstr(vflat4, 8)} m^4/s^4, g_* = {mp.nstr(g_star[name], 8)} m/s^2")
check("S9 [footings] canonical rho_Lambda ~ 5.8444e-27 kg/m^3 (matches AS059 bookkeeping)",
      abs(foot["canonical"]["rhoL"] / 5.8444124540218754e-27 - 1) < 1e-6, f"{foot['canonical']['rhoL']:.6e}")
check("S9b [footings] alternative footing: kappa fixed -> rho_Lambda ratio = (a0_alt/a0_can)^2 = 1.45149",
      abs(foot["alt"]["rhoL"] / foot["canonical"]["rhoL"] - (1.1279e-10 / 9.3619e-11) ** 2) < 1e-9,
      f"ratio = {foot['alt']['rhoL']/foot['canonical']['rhoL']:.6f}")

# ---- S10 full-variation refinement ----
b0 = float(b_num[0.0])
r0_full = 1 / (1 + 2 * b0 / 8)   # deep-limit r with the 2b beta^2 q term (Z = 8 beta^2)
g_star_full = 64 * PI * A0["canonical"] * (1 + 2 * b0 / 8) / (2 * D_sat)
print(f"  S10: full-variation flux equation: deep r0 = {r0_full:.6f} (0.45% suppression), g_* shift +0.45% -> {mp.nstr(g_star_full/A0['canonical'], 6)} a0")
check("S10 [refinement] the 2b beta^2 q term (q-variation of the promoted primitive) is a uniform 0.45% renormalization absorbed by q0; k04's gauge-fixed equation is the comparison branch",
      abs(r0_full - 0.9955) < 1e-3 and abs(g_star_full / A0["canonical"] / 155.2 - 1) < 0.01, f"r0 = {r0_full:.5f}")

# ---- sign control: wrong-sign coupling ----
# L_MOND with the opposite sign -> flux equation q[Z - alpha beta^2 W/8pi] = Z q0
# -> r = 1/(1 - alpha W/64 pi): pole at W = 64 pi/alpha and r > 1 (runaway a0_loc)
Wpole = 64 * PI / 2  # wrong-sign pole at W = Wpole (K_B = 0 -> alpha = 2)
r_wp_half = 1 / (1 - 2 * (Wpole * 0.5) / (64 * PI))   # r = 2: a0_loc = 2 a0 (runaway)
r_wp_near = 1 / (1 - 2 * (Wpole * 0.99) / (64 * PI))  # r = 100: pole approach
check("S11 [sign control] opposite-sign coupling gives r > 1 (a0_loc runaway) and a pole at W = 32 pi (no switch-off): excluded",
      r_wp_half == 2 and r_wp_near > 10,
      f"r(0.5 Wpole) = {mp.nstr(r_wp_half, 4)}, r(0.99 Wpole) = {mp.nstr(r_wp_near, 4)}")

# ---- G_N/G_mon ratio ----
print(f"  S12: general flux equation carries (G_N/G_mon); branch matching condition G_mon = G_N (k04 single-G). "
      f"g_* scales as (G_mon/G_N): g_* = 64 pi a0 (G_mon/G_N)/((2-K_B) Delta_sat).")

# ---------------- outputs ----------------
elapsed = time.time() - T0
rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss  # bytes on macOS
npass = sum(1 for c in CHECKS if c["pass"])
print(f"\n  RESULT: {npass}/{len(CHECKS)} checks PASS; elapsed {elapsed:.2f} s; max RSS {rss/1e6:.1f} MB")
out = dict(
    task_sha256=h_task, k04_sha256=h_k04, k04_manifest_sha256=h_k04_man,
    kernel=dict(s_sat=float(s_sat), Delta_sat=float(D_sat), I_rar=float(I_rar),
                b_K0=float(b_num[0.0]), b_K025=float(b_num[0.25]),
                Z_over_beta2_K0=ratio_num[0.0], Z_over_beta2_K025=ratio_num[0.25]),
    symbolic=dict(P=str(P), eps=str(eps), kappa2=str(kappa2),
                  flux_equation=str(sp.Eq(flux_lhs, Z * q0)),
                  flux_solution=str(flux_sol), flux_residual_symbolic=str(flux_res),
                  negative_control_solutions=[str(s) for s in nc],
                  full_variation_solution=str(flux_sol_full)),
    fixed_points=rows,
    solar_system={f"{f}_{n}": v for (f, n), v in ss.items()},
    wide_binaries={f"{f}_{k}": v for (f, k), v in wb.items()},
    g_star={f: float(v) for f, v in g_star.items()},
    stability=dict(g_peak_a0=float(g_peak_a0), CL_eff_20a0=float(CL20)),
    footings=foot,
    refinement=dict(r0_full=r0_full, g_star_full_a0=float(g_star_full / A0["canonical"])),
    checks=CHECKS,
    bounds=dict(elapsed_s=elapsed, max_rss_bytes=rss, npass=npass, nchecks=len(CHECKS)),
)
with open(os.path.join(RUN, "raw_output.json"), "w") as f:
    json.dump(out, f, indent=1)
print("  wrote raw_output.json")
sys.exit(0)
