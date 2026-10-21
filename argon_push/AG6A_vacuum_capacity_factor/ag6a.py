#!/usr/bin/env python3
"""AG6A: can a capacity of the vacuum set the MOND switch-on scale, i.e. derive kappa = 1/2?

Frozen criteria: FROZEN_CRITERIA.md (199ba297e, committed alone before this script existed).
Scale only; the law shape (which n) belongs to AG6B (dbcaeba9e).

Run:     OMP_NUM_THREADS=1 nice -n 10 python3 ag6a.py > ag6a.out
MUTATE:  AG6A_MUTATE=1 OMP_NUM_THREADS=1 nice -n 10 python3 ag6a.py > ag6a_MUTATE.out   (must exit 1)

Units: c = 1 unless stated; H = H_Lambda; a0 = kappa sqrt(G rho_Lambda); H^2 = (8 pi/3) G rho_Lambda.
kappa = 1/2 FITTED; Z = 2 sqrt(8 pi/3) = 5.7888 (Z == kappa, never ~21); both footings 9.3603e-11 / 1.1312e-10 never pooled;
not theory closed.
"""
import json
import math
import os
import sys

import numpy as np
import sympy as sp
import mpmath as mp

MUTATE = os.environ.get("AG6A_MUTATE") == "1"
HERE = os.path.dirname(os.path.abspath(__file__))
RESULTS = {"mode": "MUTATE" if MUTATE else "MAIN", "checks": [], "numbers": {}}
NFAIL = 0


def check(name, measured, ok, reading):
    global NFAIL
    ok = bool(ok)
    if not ok:
        NFAIL += 1
    RESULTS["checks"].append({"name": name, "measured": str(measured), "ok": ok, "reading": reading})
    print(f"{'PASS' if ok else 'FAIL'}  {name}: {measured}  -- {reading}")


def num(key, val):
    RESULTS["numbers"][key] = float(val) if isinstance(val, (int, float, np.floating)) or hasattr(val, "evalf") else val
    return val


print(f"AG6A ({RESULTS['mode']})  kappa = 1/2 FITTED; not theory closed")
print("=" * 110)

# ----------------------------------------------------------------------------------------------------------------
# 0. Targets and identity guard
# ----------------------------------------------------------------------------------------------------------------
pi = sp.pi
Zs = 2 * sp.sqrt(8 * pi / 3)            # Z = 2 sqrt(8 pi/3)
F8 = sp.sqrt(8 * pi / 3)               # H / sqrt(G rho): the Friedmann conversion
Zf = float(Zs)
num("Z", Zf)
num("two_Z", 2 * Zf)
print("\n## 0. targets and identity guard")
rho, G, c = sp.symbols("rho G c", positive=True)
Hsym = sp.sqrt(8 * pi * G * rho / 3)
a0_half = sp.Rational(1, 2) * c * sp.sqrt(G * rho)
ident = sp.simplify(c * Hsym / a0_half - sp.sqrt(32 * pi / 3))
check("G-identity: c H / a0 = sqrt(32 pi/3) for ANY rho (so a 'Z match via Friedmann' is a tautology, never a result)",
      ident, ident == 0, "identity of the definitions; used only as a target")
kap_milgrom = 2 * F8                    # a0 = 2H  =>  kappa = 2 sqrt(8 pi/3)
check("target: Milgrom 1999 dS-Unruh a0 = 2cH  =>  kappa = 2 sqrt(8pi/3), numerically = Z; ratio to kappa = 1/2 is 2Z",
      f"kappa_M = {float(kap_milgrom):.6f}, ratio = {float(kap_milgrom / sp.Rational(1, 2)):.5f}",
      abs(float(kap_milgrom) - Zf) < 1e-12 and abs(float(kap_milgrom * 2) - 2 * Zf) < 1e-12,
      "2Z = sqrt(8pi/3) x (2/kappa) x n_M/2 ... = Friedmann conversion 2.894 x rational 4 (n=2) ; Z = 2.894 x 2 (n=1 cap)")
num("kappa_milgrom", float(kap_milgrom))
# SI footing values (Planck 2018: H0 = 67.4, Omega_Lambda = 0.6847) and Milgrom's a0 against AG4f's n = 2 SPARC fit (1.159e-10)
c_SI, H0_SI = 2.99792458e8, 67.4e3 / 3.0856775814913673e22
cHL = c_SI * math.sqrt(0.6847) * H0_SI
a0_can = cHL / Zf
a0_M = 2 * cHL
num("cH_Lambda_SI", cHL)
num("a0_canonical_SI", a0_can)
num("a0_milgrom_SI", a0_M)
num("dex_milgrom_vs_AG4f_n2_best_1.159e-10", math.log10(a0_M / 1.159e-10))
num("dex_milgrom_vs_canonical", math.log10(a0_M / a0_can))
check("G-record: canonical footing a0 = cH_Lambda/Z = 9.3603e-11 reproduced; Milgrom's 2cH_Lambda sits +0.97 dex above AG4f's "
      "n=2 SPARC a0 (reported, not a gate)",
      f"a0_can = {a0_can:.5e}, a0_M = {a0_M:.4e}, offset vs 1.159e-10 = {math.log10(a0_M / 1.159e-10):+.3f} dex",
      abs(a0_can / 9.3603e-11 - 1) < 2e-4, "constants consistent with the record")
# CFG47 control: T_Unruh = T_dS matching gives a = H; mode count n gives a0 = H/n, kappa = sqrt(8pi/3)/n
cfg47 = [float(F8 / n) for n in (1, 2)]
check("G-record CFG47: kappa_match = sqrt(8pi/3)/n  (n=1: 2.894, n=2: 1.447)", [round(x, 4) for x in cfg47],
      abs(cfg47[0] - 2.8944) < 1e-3 and abs(cfg47[1] - 1.4472) < 1e-3, "reproduced")

# ----------------------------------------------------------------------------------------------------------------
# M1. Horizon-information capacity of a uniformly accelerated observer in dS4
# ----------------------------------------------------------------------------------------------------------------
print("\n## M1. horizon-information capacity (dS4 embedded in R^{1,4})")
tau, R, L = sp.symbols("tau R L", positive=True)
eta = sp.diag(-1, 1, 1, 1, 1)
X = sp.Matrix([R * sp.sinh(tau / R), R * sp.cosh(tau / R), sp.sqrt(L**2 - R**2), 0, 0])


def dot(u, v):
    return sp.simplify((u.T * eta * v)[0, 0])


on_dS = sp.simplify(dot(X, X) - L**2)
check("M1.1 orbit lies on dS4 (X.X = L^2)", on_dS, on_dS == 0, "embedding orbit valid for 0 < R < L")
U = sp.diff(X, tau)
norm_u = sp.simplify(dot(U, U))
check("M1.1 proper time: U.U = -1", norm_u, sp.simplify(norm_u + 1) == 0, "tau is proper time")
Acc5 = sp.diff(X, tau, 2)
A5sq = sp.simplify(dot(Acc5, Acc5))
nrm = sp.simplify(dot(Acc5, X) / L)          # component along the unit normal X/L
a4sq = sp.simplify(A5sq - nrm**2)
check("M1.1 5D acceleration A = 1/R and 4D proper acceleration a^2 = 1/R^2 - 1/L^2", f"A^2 = {A5sq}, a^2 = {a4sq}",
      sp.simplify(A5sq - 1 / R**2) == 0 and sp.simplify(a4sq - (1 / R**2 - 1 / L**2)) == 0,
      "A^2 = a^2 + H^2 with H = 1/L (Deser-Levin invariant)")

# causal horizon: boundary of J^-(orbit) = {X0 = X1} intersected with dS4.  Cross-section at X0 = X1 = v:
v, th, ph = sp.symbols("v theta phi", real=True)
r_h = L if not MUTATE else R                 # Mu1: the commonly assumed 'accelerated horizon' of radius 1/A
Y = sp.Matrix([v, v, r_h * sp.sin(th) * sp.cos(ph), r_h * sp.sin(th) * sp.sin(ph), r_h * sp.cos(th)])
on_dS_h = sp.simplify(dot(Y, Y) - L**2)
# null generator: d/dv direction (1,1,0,0,0) is null and tangent
gen = sp.Matrix([1, 1, 0, 0, 0])
gen_null = dot(gen, gen)
# induced metric on the (theta, phi) section
e_th, e_ph = sp.diff(Y, th), sp.diff(Y, ph)
g_tt, g_pp, g_tp = dot(e_th, e_th), dot(e_ph, e_ph), dot(e_th, e_ph)
det_sec = sp.simplify(g_tt * g_pp - g_tp**2)
det_ok = sp.simplify(det_sec - r_h**4 * sp.sin(th)**2) == 0      # so sqrt(det) = r_h^2 sin(theta) on [0, pi]
area = sp.simplify(sp.integrate(sp.integrate(r_h**2 * sp.sin(th), (th, 0, pi)), (ph, 0, 2 * pi)))
dA_dR = sp.simplify(sp.diff(area, R))
check("M1.2 horizon section lies on dS4, its generator is null, induced det = r^4 sin^2",
      f"X.X - L^2 = {on_dS_h}, gen.gen = {gen_null}, det ok = {det_ok}",
      on_dS_h == 0 and gen_null == 0 and det_ok,
      "valid causal-horizon section" if on_dS_h == 0 else "Mu1 surface is NOT on dS4: not a horizon of this spacetime")
check("M1.2 horizon area is independent of the acceleration (dA_h/dR = 0, i.e. dA_h/da = 0)", f"A_h = {area}, dA/dR = {dA_dR}",
      dA_dR == 0,
      "the eternally accelerated observer's causal horizon is the same bifurcation sphere of radius L for every a: "
      "acceleration consumes NO horizon capacity, so M1 sets no scale")
num("M1_area_over_4piL2", float(sp.simplify(area / (4 * pi * L**2)).subs({L: 1, R: sp.Rational(1, 2)})))
# Tolman / KMS temperature from the boost Killing vector xi = X1 d0 + X0 d1 (unit surface gravity in ambient normalization)
xi = sp.Matrix([X[1], X[0], 0, 0, 0])
xi_norm = sp.sqrt(sp.simplify(-dot(xi, xi)))
T_loc = sp.simplify(1 / (2 * pi * xi_norm))
a_sym, Hh = sp.symbols("a H", positive=True)
T_DL = sp.sqrt(a_sym**2 + Hh**2) / (2 * pi)
check("M1.3 local KMS temperature = 1/(2 pi |xi|) = A/(2 pi) = sqrt(a^2 + H^2)/(2 pi) (Deser-Levin)",
      f"T = {T_loc}", sp.simplify(T_loc.subs(R, 1 / sp.sqrt(a_sym**2 + Hh**2)) - T_DL) == 0,
      "the only acceleration-dependent local datum is the Tolman temperature (record WW/agentYY: modular temperature)")
# flat limit: L -> oo, a -> 1/R; horizon X0 = X1 at distance R = 1/a from the orbit at tau = 0 (Rindler)
a_flat = sp.limit(sp.sqrt(1 / R**2 - 1 / L**2), L, sp.oo)
check("M1.4 flat limit: a -> 1/R, horizon = Rindler null plane at proper distance 1/a", a_flat,
      sp.simplify(a_flat - 1 / R) == 0, "control reproduces Rindler")

# ----------------------------------------------------------------------------------------------------------------
# M1b. Thermal (KMS/Tolman) capacity: F(a) = f(A) - f(H)
# ----------------------------------------------------------------------------------------------------------------
print("\n## M1b. thermal capacity: inertia from the bath energy along the orbit, F(a) = f(A) - f(H), f'(oo) = 1")
f1, f2, f3 = sp.symbols("f1 f2 f3", real=True)          # first three derivatives of a generic smooth f at A = H
Aexpr = sp.sqrt(a_sym**2 + Hh**2)
epsA = Aexpr - Hh
Fgen = f1 * epsA + f2 * epsA**2 / 2 + f3 * epsA**3 / 6
Fser = sp.series(Fgen, a_sym, 0, 5).removeO()
lead = sp.simplify(Fser.coeff(a_sym, 2))
check("B.1 slope theorem: F = f'(H) a^2/(2H) + O(a^4)  =>  deep a0 = 2H/f'(H), kappa = 2 sqrt(8pi/3)/f'(T_GH)",
      f"a^2 coefficient = {lead}", sp.simplify(lead - f1 / (2 * Hh)) == 0 and Fser.coeff(a_sym, 1) == 0,
      "g_N = F(g) gives g = sqrt(2H g_N/f'(H)) in the deep regime; the second derivative enters only at O(a^4)")
slope_req = float(4 * F8)
num("B2_required_slope_fprime_TGH", slope_req)
d1 = math.sqrt(1 + 3 / (32 * math.pi)) - 1
d2 = math.sqrt(1 + 3 / (128 * math.pi)) - 1
num("B2_delta1_T_window_at_a0", d1)
num("B2_delta2_T_window_at_a0_over_2", d2)
check("B.2 kappa = 1/2 needs f'(T_GH) = 2Z = 4 sqrt(8pi/3); the switch sits at a temperature excess dT/T_GH = delta",
      f"f'(T_GH) = {slope_req:.5f}; delta1 (a = a0) = {d1:.6f}, delta2 (a = a0/2) = {d2:.6f}",
      abs(slope_req - 2 * Zf) < 1e-12 and 0.0148 < d1 < 0.0149 and 0.0037 < d2 < 0.0038,
      "a thermal mechanism must change character within 1.5% (0.37%) of the Gibbons-Hawking temperature, "
      "at a pi-carrying (transcendental) location")

# B.3 equipartition bound: Einstein function E(x) = x^2 e^x/(e^x-1)^2 = (y/sinh y)^2, y = x/2
y = sp.symbols("y", positive=True)
xx = sp.symbols("x", positive=True)
Ein = xx**2 * sp.exp(xx) / (sp.exp(xx) - 1)**2
ident_E = sp.simplify(sp.expand((Ein - ((xx / 2) / sp.sinh(xx / 2))**2).rewrite(sp.exp)))
lim0 = sp.limit(Ein, xx, 0)
grid = np.logspace(-6, 2.5, 4000)
# stable form (y/sinh y)^2, y = x/2.  First run used x^2 e^-x/(1-e^-x)^2, which loses ~1e-10 to cancellation at x = 1e-6
# and printed a grid max of 1 + 9e-11 (check-implementation artefact; gate unchanged; disclosed in README).
Egrid = ((grid / 2) / np.sinh(grid / 2))**2
check("B.3a Einstein function = (y/sinh y)^2 <= 1 (sinh y >= y), -> 1 as x -> 0 (classical)",
      f"identity residual {ident_E}, limit {lim0}, grid max {Egrid.max():.12f}",
      ident_E == 0 and lim0 == 1 and Egrid.max() <= 1 + 1e-12,
      "each harmonic mode's heat capacity is at most its classical value")
mp.mp.dps = 30


def debye_ratio(xD, d):
    integ = mp.quad(lambda t: t**(d + 1) * mp.e**t / (mp.e**t - 1)**2, [0, xD])
    return d * integ / xD**d


dvals = {d: [float(debye_ratio(mp.mpf(x), d)) for x in (0.01, 0.3, 1, 2 * math.pi, 10, 50)] for d in (1, 3)}
check("B.3b Debye 1D/3D heat-capacity ratios <= 1 at Theta/T = 0.01 .. 50 (positive-weight averages of E(x))",
      {d: [round(v, 5) for v in vals] for d, vals in dvals.items()},
      all(v <= 1 + 1e-12 for vals in dvals.values() for v in vals), "bound holds for any harmonic density of states")
# natural members: classical (Milgrom), quantum single mode at the horizon frequency, Debye cutoffs at the horizon frequency
E_2pi = float((math.pi / math.sinh(math.pi))**2)  # mode omega = H at T = H/2pi: x = 2 pi
members = {
    "classical f = A (Milgrom 1999)": 1.0,
    "one quantum mode, omega = H (x = 2 pi at T_GH)": E_2pi,
    "Debye 1D, cutoff omega_D = H": float(debye_ratio(mp.mpf(2 * math.pi), 1)),
    "Debye 3D, cutoff omega_D = H": float(debye_ratio(mp.mpf(2 * math.pi), 3)),
    "one quantum mode, omega = H/(2 pi) (x = 1)": float(1 / (4 * math.sinh(0.5)**2)),
}
if MUTATE:
    # Mu2: f(A) = A + (1 - 2Z) H^2/A : f'(H) = 2Z by an inserted transcendental constant
    members["Mu2 inserted: f = A + (1-2Z)H^2/A"] = 2 * Zf
member_kappa = {k: float(2 * F8) / s for k, s in members.items()}
RESULTS["numbers"]["B3_members_fprime"] = members
RESULTS["numbers"]["B3_members_kappa"] = member_kappa
for k in members:
    print(f"      member {k:52s} f'(T_GH) = {members[k]:10.6f}   a0/H = {2 / members[k]:10.4f}   kappa = {member_kappa[k]:10.4f}")
check("B.3c equipartition bound holds for every declared member: f'(T_GH) <= 1  =>  a0 >= 2cH_Lambda, kappa >= 2 sqrt(8pi/3)",
      f"max f' = {max(members.values()):.5f}, min kappa = {min(member_kappa.values()):.4f}",
      max(members.values()) <= 1 + 1e-12,
      "Milgrom's value is the FLOOR of the harmonic-bath class; quantum modes push a0 UP; kappa = 1/2 lies 2Z below the floor")
check("B.3d no natural member reaches the required slope 2Z (kappa = 1/2)",
      f"closest kappa = {min(member_kappa.values(), key=lambda q: abs(q - 0.5)):.4f}",
      all(abs(q - 0.5) > 1e-6 for q in member_kappa.values()), "no hit")
# B.4 power family F_k = (A^k - H^k)^(1/k): deep exponent 2/k
pw = {}
for k in (sp.Rational(1, 2), 1, 2, 3, 4):
    Fk = (Aexpr**k - Hh**k)**(1 / sp.S(k))
    Fk1 = Fk.subs(Hh, 1)
    expo = sp.limit(sp.simplify(a_sym * sp.diff(Fk1, a_sym) / Fk1), a_sym, 0)
    big = sp.limit(Fk1 / a_sym, a_sym, sp.oo)
    pw[str(k)] = (expo, big)
    print(f"      k = {str(k):4s}: deep exponent F ~ a^{expo}, large-a F/a -> {big}")
mond_k = [k for k, (e, b) in pw.items() if e == 2 and b == 1]
check("B.4 thermal-moment family: deep MOND (F ~ a^2) with a Newtonian limit iff k = 1 (Milgrom ΔT)", mond_k,
      mond_k == ["1"], "k = 2 is exactly Newtonian, k = 3, 4 anti-MOND, k = 1/2 too deep: the linear-T form is forced")
# B.5 escapes: Schottky peak and the count needed
xs = np.linspace(0.05, 20, 200000)
Csch = xs**2 * np.exp(xs) / (1 + np.exp(xs))**2
cmax, xmax = Csch.max(), xs[Csch.argmax()]
nS = (2 * Zf - 1) / cmax
num("B5_schottky_max", cmax)
num("B5_schottky_count_needed", nS)
check("B.5 escapes need tuned structure: Schottky max C/k = 0.4392 at Delta/T = 2.40; reaching f' = 2Z needs >= 24 tuned levels "
      "per classical DOF with gaps tied to T_GH (>= 2 free choices); a phase transition needs T_c and an amplitude",
      f"C_max = {cmax:.4f} at {xmax:.3f}; levels needed {nS:.1f}", abs(cmax - 0.4392) < 2e-4 and nS > 20,
      "every escape inserts a scale at T_GH: not a derivation")
# B.6 (post-freeze diagnostic, disclosed in README; not a gate): the bath energy function the framework law would require
eps = np.logspace(-7, 3, 20001)            # eps = (A - H)/H, H = 1
aa = np.sqrt(eps * (2 + eps))
a0n = 1 / Zf
need = {}
for n_law in (1, 2):
    if n_law == 1:
        Fn = aa**2 / (aa + a0n)                     # simple law g_N = g^2/(g + a0)
    else:
        Fn = np.sqrt(aa**2 + (a0n / 2)**2) - a0n / 2  # quadratic law: rest scale a0/2
    fprime = np.gradient(Fn, eps)
    loc = np.gradient(np.log(fprime), np.log(eps))
    win = (eps > 3 * (a0n**2 / 2)) & (eps < 0.3)
    need[n_law] = {"fprime_at_TGH": float(fprime[0]), "fprime_at_large_T": float(fprime[-1]),
                   "min_local_slope_in_window": float(loc[win].min()) if win.any() else None}
RESULTS["numbers"]["B6_required_bath"] = need
print(f"      B.6 diagnostic (required bath heat capacity C/C_cl = f'(T)):  n=1 {need[1]}  n=2 {need[2]}")
print("          reading: f' must equal ~2Z at T_GH (both laws), fall roughly like (T - T_GH)^(-1/2) above "
      "delta ~ 0.015, and reach 1 (classical) for T >> T_GH: a near-critical bath AT T_GH, rounded at a0 (a free scale)")

# ----------------------------------------------------------------------------------------------------------------
# M2. Holographic / Bekenstein polarization-capacity menu
# ----------------------------------------------------------------------------------------------------------------
print("\n## M2. holographic / Bekenstein polarization capacity (u_sat = 4 pi G P_sat), hbar must cancel")
hb, kB, Hc = sp.symbols("hbar k_B H", positive=True)
cc, GG = sp.symbols("c G", positive=True)
lP2 = hb * GG / cc**3
kT = hb * Hc / (2 * pi)                        # k_B T_GH
entries = {
    "(i) BH cells 1/(4 lP^2) x one thermal quantum kT_GH/c^2": 4 * pi * GG * (1 / (4 * lP2)) * kT / cc**2,
    "(ii) Padmanabhan 1/lP^2 x (1/2)kT_GH/c^2": 4 * pi * GG * (1 / lP2) * (kT / 2) / cc**2,
    "(iii) CKN/Schwarzschild-saturated vacuum ball: c^2/(2R), R = c/H": cc**2 / (2 * (cc / Hc)),
    "(iv) Bekenstein-saturated static patch: G E/(c^2 R^2), E = c^4 R/(2G), R = c/H": GG * (cc**4 * (cc / Hc) / (2 * GG)) / (cc**2 * (cc / Hc)**2),
    "(v) thermal Compton dipole crossover kT_GH/(m hbar/(m c)) [scale only]": kT * cc / hb,
}
if MUTATE:
    entries["Mu3 inserted: u_sat = cH/(2Z)"] = cc * Hc / (2 * Zs)
m2 = {}
inband = 0
total = 0
exact_half = []
for name, expr in entries.items():
    r = sp.simplify(expr / (cc * Hc))
    has_hbar = r.has(hb) or r.has(GG)
    for n_law in (1, 2):
        kap = sp.simplify(n_law * r * F8)
        k2 = sp.simplify(kap**2)
        pik = next(j for j in range(-3, 4) if sp.simplify(k2 / pi**j).is_rational)
        kv = float(kap)
        total += 1
        if 0.417 - 0.095 <= kv <= 0.417 + 0.095:
            inband += 1
        if sp.simplify(kap - sp.Rational(1, 2)) == 0:
            exact_half.append((name, n_law))
        m2[f"{name} | n={n_law}"] = {"u_over_cH": str(r), "kappa": kv, "kappa^2": str(k2), "pi_power_of_kappa^2": int(pik),
                                     "hbar_or_G_left": bool(has_hbar)}
        print(f"      {name:78s} n={n_law}: u_sat/cH = {str(r):10s} kappa = {kv:8.4f}  kappa^2 = {str(k2):14s} pi^{pik}")
RESULTS["numbers"]["M2_entries"] = m2
check("M2.a hbar and G cancel in every entry (classical capacities, as a0 requires)",
      [v["hbar_or_G_left"] for v in m2.values()], not any(v["hbar_or_G_left"] for v in m2.values()), "all classical")
check("M2.b no entry gives kappa = 1/2 exactly (kappa^2 carries pi^(+-1) in every horizon-capacity entry; 1/4 is pi^0)",
      exact_half if exact_half else "none", len(exact_half) == 0,
      "horizon capacities read H, so kappa = rational x sqrt(8pi/3) x pi^(0 or -1): never 1/2 (pi irrational)")
check("M2.c G-record k03: the Compton-dipole scale gives kappa = sqrt(8pi/3)/(2pi) = sqrt(2/(3pi)) = 0.4607 (n=1)",
      f"{m2[list(m2)[8]]['kappa']:.4f}" if len(m2) > 8 else "n/a",
      len(m2) > 8 and abs(m2[list(m2)[8]]["kappa"] - math.sqrt(2 / (3 * math.pi))) < 1e-12,
      "data-compatible alternative (inside CFG493 1 sigma), NOT 1/2; its shape is a paraelectric (AG6B class A)")
num("M2_base_rate_in_CFG493_1sigma", inband / total)
print(f"      base rate: {inband}/{total} entries inside the CFG493 1-sigma band [0.322, 0.512] (reported, not evidence)")

# ----------------------------------------------------------------------------------------------------------------
# M3. Enthalpy (inertial-density) capacity of the dark-energy medium
# ----------------------------------------------------------------------------------------------------------------
print("\n## M3. enthalpy capacity u_sat = q c sqrt(G (rho + p/c^2))")
w = sp.symbols("w", real=True)
enth = sp.simplify(rho * (1 + w))
check("C.1 Lambda (w = -1): rho + p/c^2 = 0, so the vacuum's own capacity vanishes for every q and every length",
      enth.subs(w, -1), enth.subs(w, -1) == 0, "X2 (linear response) extended to the nonlinear capacity: a Lambda vacuum cannot be polarised")
# DESI DR2 flat w0waCDM rows as recorded in sonnet55_push/puzzle_32pi/p13b_desi_dr2_a0z.py (37b55b149)
ROWS = {
    "DESI+CMB": (0.353, -0.42, 0.21, -1.75),
    "DESI+CMB+Pantheon+": (0.3114, -0.838, 0.055, -0.62),
    "DESI+CMB+Union3": (0.3275, -0.667, 0.088, -1.09),
    "DESI+CMB+DESY5": (0.3191, -0.752, 0.057, -0.86),
}
if MUTATE:
    ROWS = {k: (om, -0.75, 0.05, 0.0) for k, (om, *_r) in ROWS.items()}   # Mu4


def rde(z, w0, wa):
    return (1 + z) ** (3 * (1 + w0 + wa)) * math.exp(-3 * wa * z / (1 + z))


def onepw(z, w0, wa):
    return 1 + w0 + wa * z / (1 + z)


qs = {"1 (bare G)": 1.0, "sqrt(4pi/3) (ball)": math.sqrt(4 * math.pi / 3), "sqrt(8pi/3) (Friedmann)": math.sqrt(8 * math.pi / 3),
      "sqrt(4pi) (Jeans)": math.sqrt(4 * math.pi)}
m3 = {}
chi2 = 0.0
within = 0
zx_all = []
for name, (om, w0, sw0, wa) in ROWS.items():
    k1 = math.sqrt(1 + w0)
    sk = sw0 / (2 * k1)
    pull = (k1 - 0.5) / sk
    chi2 += pull**2
    within += abs(pull) <= 1
    s = -(1 + w0) / wa if wa != 0 else float("inf")
    zx = s / (1 - s) if (wa != 0 and 0 < s < 1) else float("inf")
    zx_all.append(zx)
    r02 = math.sqrt(max(onepw(0.2, w0, wa), 0) * rde(0.2, w0, wa) / (1 + w0))
    r03 = math.sqrt(max(onepw(0.3, w0, wa), 0) * rde(0.3, w0, wa) / (1 + w0))
    fw02 = math.sqrt(rde(0.2, w0, wa))
    m3[name] = {"kappa_eff_q1": k1, "sigma": sk, "pull_vs_half": pull, "z_cross": zx,
                "a0ratio_z0.2_enthalpy": r02, "a0ratio_z0.3_enthalpy": r03, "a0ratio_z0.2_framework_sqrt_rhoDE": fw02,
                "kappa_eff_other_q": {qn: qv * k1 for qn, qv in qs.items()}}
    print(f"      {name:20s} 1+w0 = {1 + w0:6.3f}  kappa_eff(q=1) = {k1:.4f} +- {sk:.4f} (pull vs 1/2 {pull:+.2f})  z_x = {zx:7.3f}  "
          f"a0(0.2)/a0(0): enthalpy {r02:.3f} vs framework {fw02:.3f}; a0(0.3)/a0(0) {r03:.3f}")
RESULTS["numbers"]["M3_rows"] = m3
spread = max(v["kappa_eff_q1"] for v in m3.values()) - min(v["kappa_eff_q1"] for v in m3.values())
num("M3_chi2_about_half_q1_4rows_not_independent", chi2)
num("M3_spread_q1", spread)
check("C.3 kappa_eff(0) with q = 1 is DATASET-DEPENDENT (spread > 0.1; not all four within 1 sigma of 1/2)",
      f"spread {spread:.3f}; {within}/4 within 1 sigma; chi2 about 1/2 = {chi2:.2f} (rows share DESI+CMB, not independent)",
      spread > 0.1 and within < 4, "the DESY5 hit 0.498 is one row of four: post hoc, not forced")
check("C.4 the enthalpy capacity vanishes at the w = -1 crossing below z = 2.5 in every DESI row (a0^2 < 0 beyond)",
      [round(z, 3) for z in zx_all], all(z < 2.5 for z in zx_all),
      "the mechanism is undefined at z > z_x: it cannot be the framework's a0, which must exist at every redshift the record uses")
other_q = {qn: [round(v["kappa_eff_other_q"][qn], 3) for v in m3.values()] for qn in qs}
RESULTS["numbers"]["M3_other_q"] = other_q
check("C.2 the other declared normalisations (ball, Friedmann, Jeans) put kappa_eff(0) at 0.8-2.7, outside the data band",
      other_q, all(min(vals) > 0.6 for qn, vals in other_q.items() if qn != "1 (bare G)"),
      "only the bare-G choice lands near 1/2: the same un-forced coefficient choice as the record's open target")

# ----------------------------------------------------------------------------------------------------------------
print("\n" + "=" * 110)
nchk = len(RESULTS["checks"])
print(f"{nchk - NFAIL}/{nchk} checks hold  ({RESULTS['mode']})")
RESULTS["n_checks"] = nchk
RESULTS["n_fail"] = NFAIL
RESULTS["verdict_inputs"] = {
    "M1": "SCOPED NO-GO (horizon area a-independent)" if not MUTATE else "mutated",
    "M1b": "SCOPED NO-GO (equipartition floor a0 >= 2cH_Lambda; kappa = 1/2 needs f'(T_GH) = 2Z)" if not MUTATE else "mutated",
    "M2": "SCOPED NO-GO (pi-grade; best entry k03 0.461, not 1/2)" if not MUTATE else "mutated",
    "M3": "SCOPED NO-GO (zero for Lambda; dataset-dependent; undefined beyond z_x ~ 0.35-0.50)" if not MUTATE else "mutated",
}
out = os.path.join(HERE, "ag6a_results_MUTATE.json" if MUTATE else "ag6a_results.json")
with open(out, "w") as fh:
    json.dump(RESULTS, fh, indent=1, default=str)
print(f"wrote {os.path.basename(out)}")
sys.exit(1 if NFAIL else 0)
