#!/usr/bin/env python3
"""n1_1 -- independent re-derivation of lane F's S^2 flux relations and their exact scope (pre-registered in N1_PREREGISTRATION.md, Part I).

Route (different from f2, which fibred a Cartan U(1) and integrated cos^2): for each of the THREE SU(2) generators use
    1/g_a^2 = (1/(2 kappa^2)) Int |K_a|^2 dA + (1/g^2) Int mu_a^2 dA ,     i_{K_a} F = - d mu_a ,
with K_a the Killing vectors of S^2(R), F = (N/2) sin(theta) d theta ^ d phi the flux (Int F = 2 pi N for a unit-charge field), and mu_a the moment map.
U(1) (6D Maxwell zero mode, unit charge): 1/g_U1^2 = Area/g^2.   alpha = g^2/(4 pi);  l_P^2 = G_4 = kappa_4^2/(8 pi), kappa_4^2 = kappa^2/Area.
Minkowski point: U = 0 and dU/dR = 0 for U(R) = Area * W(R), W = Lambda/kappa^2 - 1/(kappa^2 R^2) + N^2/(8 g^2 R^4)   (flux F^2/(4 g^2) with F^2 = N^2/(2 R^4)).

Run:     python3 n1_1_s2_rederive.py            (real run, exit 0)
MUTATE:  python3 n1_1_s2_rederive.py --mutate   (control: the flux term of 1/g_a^2 is dropped; the identity alpha_SU2 = 3 l_P^2/R^2 must then FAIL, exit 1)
"""
import sys
sys.dont_write_bytecode = True
import subprocess, os, itertools
from fractions import Fraction
import sympy as sp

MUTATE = "--mutate" in sys.argv
CHECKS = []


def check(tag, ok, detail=""):
    CHECKS.append((tag, bool(ok)))
    print(f"  [{'PASS' if ok else 'FAIL'}] {tag} {detail}")


print("=" * 100)
print("N1-1 S^2 flux relations re-derived -- mode: " + ("MUTATE CONTROL (flux term dropped)" if MUTATE else "REAL RUN"))
print("=" * 100)
FLUX_ON = 0 if MUTATE else 1

R, N, kap, g, Lam = sp.symbols("R N kappa g Lambda", positive=True)
th, ph = sp.symbols("theta phi", real=True)
coords = (th, ph)
metric = sp.diag(R ** 2, R ** 2 * sp.sin(th) ** 2)
sqrtg = R ** 2 * sp.sin(th)

# ---- Killing vectors of SO(3) on the sphere, components (K^theta, K^phi)
Kz = sp.Matrix([0, 1])
Kx = sp.Matrix([-sp.sin(ph), -sp.cot(th) * sp.cos(ph)])
Ky = sp.Matrix([sp.cos(ph), -sp.cot(th) * sp.sin(ph)])
Ks = {"x": Kx, "y": Ky, "z": Kz}

def lie(A, B):
    return sp.simplify(sp.Matrix([sum(A[j] * sp.diff(B[i], coords[j]) - B[j] * sp.diff(A[i], coords[j]) for j in range(2)) for i in range(2)]))

def is_killing(K):
    # L_K g = 0
    res = sp.zeros(2, 2)
    for a in range(2):
        for b in range(2):
            res[a, b] = sum(K[c] * sp.diff(metric[a, b], coords[c]) + metric[c, b] * sp.diff(K[c], coords[a]) + metric[a, c] * sp.diff(K[c], coords[b]) for c in range(2))
    return sp.simplify(res) == sp.zeros(2, 2)

print("\nI1  Killing vectors, algebra normalisation, moment maps, averages")
check("I1a K_x, K_y, K_z are Killing vectors of S^2(R)", all(is_killing(K) for K in Ks.values()))
c1 = sp.simplify(lie(Kx, Ky) - Kz); c2 = sp.simplify(lie(Ky, Kz) - Kx); c3 = sp.simplify(lie(Kz, Kx) - Ky)
c1m = sp.simplify(lie(Kx, Ky) + Kz)
alg_sign = +1 if c1 == sp.zeros(2, 1) else (-1 if c1m == sp.zeros(2, 1) else 0)
check("I1b [K_a, K_b] = eps_abc K_c up to one overall sign: unit-normalised su(2) (doublets have T3 = +-1/2)",
      alg_sign != 0 and (sp.simplify(lie(Ky, Kz) - alg_sign * Kx) == sp.zeros(2, 1)) and (sp.simplify(lie(Kz, Kx) - alg_sign * Ky) == sp.zeros(2, 1)), f"(overall sign {alg_sign})")

Fth = (N / 2) * sp.sin(th)                      # F_{theta phi}
Fmat = sp.Matrix([[0, Fth], [-Fth, 0]])
check("I1c flux quantisation: Int F = 2 pi N", sp.simplify(sp.integrate(sp.integrate(Fth, (th, 0, sp.pi)), (ph, 0, 2 * sp.pi)) - 2 * sp.pi * N) == 0)
n_hat = {"x": sp.sin(th) * sp.cos(ph), "y": sp.sin(th) * sp.sin(ph), "z": sp.cos(th)}
mus = {}
for a, K in Ks.items():
    iKF = sp.Matrix([sum(K[nu] * Fmat[nu, mu] for nu in range(2)) for mu in range(2)])     # (i_K F)_mu = K^nu F_{nu mu}
    cand = None
    for s in (+1, -1):
        m = s * (N / 2) * n_hat[a]
        dm = sp.Matrix([sp.diff(m, c) for c in coords])
        if sp.simplify(iKF + dm) == sp.zeros(2, 1):
            cand = m
    mus[a] = cand
check("I1d moment maps found: i_{K_a} F = -d mu_a with mu_a = +-(N/2) n_a (adjoint, traceless)", all(m is not None for m in mus.values()), str({a: sp.simplify(m) for a, m in mus.items()}))

def avg(expr):
    return sp.simplify(sp.integrate(sp.integrate(expr * sqrtg, (th, 0, sp.pi)), (ph, 0, 2 * sp.pi)) / (4 * sp.pi * R ** 2))
Kn2 = {a: sp.simplify((K.T * metric * K)[0]) for a, K in Ks.items()}
avK = {a: avg(Kn2[a]) for a in Ks}
avmu = {a: avg(mus[a] ** 2) for a in Ks}
print(f"    <|K_a|^2> = {avK};   <mu_a^2> = {avmu}")
check("I1e <|K_a|^2> = 2 R^2/3 for a = x, y, z", all(sp.simplify(v - 2 * R ** 2 / 3) == 0 for v in avK.values()))
check("I1f <mu_a^2> = N^2/12 for a = x, y, z", all(sp.simplify(v - N ** 2 / 12) == 0 for v in avmu.values()))
offK = sp.simplify(avg((Kx.T * metric * Ky)[0])) == 0 and sp.simplify(avg((Kx.T * metric * Kz)[0])) == 0
offmu = sp.simplify(avg(mus["x"] * mus["y"])) == 0 and sp.simplify(avg(mus["x"] * mus["z"])) == 0
check("I1g no off-diagonal kinetic mixing between different generators (K.K and mu mu)", offK and offmu)
check("I1h SU(2)-U(1) mixing vanishes: <mu_a> = 0 (a 6D Maxwell zero mode does not mix with any su(2) generator)", all(avg(m) == 0 for m in mus.values()))
# Why the symmetric moment map (no additive constant): it is the one transforming in the adjoint (traceless); a shifted mu_z would give the Cartan an asymmetric charge spectrum.
print("    NOTE (statement, not a check): the flux term uses the traceless moment map; <mu_a> = 0 (I1h) fixes the additive constant. A shifted constant c would add c^2 to <mu^2> and give the Cartan an asymmetric charge spectrum, i.e. it would not be the SU(2)-covariant gauge field.")

print("\nI2  Minkowski point and the couplings")
W = Lam / kap ** 2 - 1 / (kap ** 2 * R ** 2) + N ** 2 / (8 * g ** 2 * R ** 4)
sol = sp.solve([sp.Eq(W, 0), sp.Eq(sp.diff(W, R), 0)], [Lam, R], dict=True)
sol = [s for s in sol if s[R].is_positive][0]
R2M = sp.simplify(sol[R] ** 2); LamM = sp.simplify(sol[Lam])
print(f"    Minkowski: R^2 = {R2M},   Lambda_6 = {LamM}")
check("I2a Minkowski point R^2 = N^2 kappa^2/(4 g^2) and Lambda_6 = 1/(2 R^2) (agrees with f2 B2a/B2b)",
      sp.simplify(R2M - N ** 2 * kap ** 2 / (4 * g ** 2)) == 0 and sp.simplify(LamM - 1 / (2 * R2M)) == 0)
# E-frame V_E = U (Area0/Area)^2 ; second derivative at the Minkowski point (radion stability, l = 0 only)
R0 = sp.symbols("R0", positive=True)
UU = 4 * sp.pi * R ** 2 * W
VE = (R0 / R) ** 4 * UU
d2 = sp.simplify(sp.diff(VE, R, 2).subs(Lam, LamM).subs(R, R0).subs(R0, sol[R]))
check("I2b radion (l = 0) is stable there: V_E'' > 0 (other modes NOT tested)", sp.simplify(d2 - 64 * sp.pi * g ** 2 / (N ** 2 * kap ** 4)) == 0, f"V'' = {d2}")

area = 4 * sp.pi * R ** 2
invg2 = {a: sp.simplify(area * avK[a] / (2 * kap ** 2) + FLUX_ON * area * avmu[a] / g ** 2) for a in Ks}
kap4sq = kap ** 2 / area
lP2 = kap4sq / (8 * sp.pi)
subsM = {g: sp.sqrt(N ** 2 * kap ** 2 / (4 * R ** 2))}
a_su2 = {a: sp.simplify((1 / invg2[a]).subs(subsM) / (4 * sp.pi) / (lP2 / R ** 2)) for a in Ks}
invg2_u1 = area / g ** 2
a_u1 = sp.simplify((1 / invg2_u1).subs(subsM) / (4 * sp.pi) / (lP2 / R ** 2))
print(f"    alpha_a / (l_P^2/R^2) = {a_su2};   alpha_U1(unit) / (l_P^2/R^2) = {a_u1}")
check("I2c alpha_SU2 = 3 l_P^2/R^2 for a = x, y, z (all three generators; f2 B3d got it from the Cartan only)", all(sp.simplify(v - 3) == 0 for v in a_su2.values()))
check("I2d alpha_U1(unit charge) = N^2 l_P^2/(2 R^2)  (f2 B3e)", sp.simplify(a_u1 - N ** 2 / 2) == 0)
ratio = sp.simplify(a_u1 / a_su2["z"])
check("I2e ratio alpha_U1/alpha_SU2 = N^2/6, independent of chat = g^2/kappa and of R", sp.simplify(ratio - N ** 2 / 6) == 0, f"ratio = {ratio}")
chat = sp.symbols("chat", positive=True)
# with kappa = 1, g^2 = chat*kappa: R^2 = N^2/(4 chat)... l_P^2 = kappa^2/(32 pi^2 R^2)
lP2_c = sp.Rational(1, 32) / sp.pi ** 2 / (N ** 2 / (4 * chat))
a2_c = sp.simplify(3 * lP2_c / (N ** 2 / (4 * chat)))
check("I2f alpha_SU2 = 3 chat^2/(2 pi^2 N^4): the ONE free real of the map is chat (matches f2's alpha_U1 = (chat/(2 pi N))^2 via the ratio)", sp.simplify(a2_c - 3 * chat ** 2 / (2 * sp.pi ** 2 * N ** 4)) == 0, f"alpha_SU2 = {a2_c}")

print("\nI3  general geometric formula alpha_geo = 4 l_P^2/<|K|^2>  (pure metric part)")
# 1/g^2 = Vol <|K|^2>/(2 kappa_D^2) = <|K|^2>/(2 kappa_4^2)  ->  g^2 = 2 kappa_4^2/<|K|^2>, alpha = g^2/4pi = 2 kappa_4^2/(4 pi <K^2>) = 4 l_P^2/<K^2>
KK2 = sp.symbols("KK2", positive=True)
alpha_geo = sp.simplify((2 * (8 * sp.pi * sp.Symbol("lP2", positive=True)) / KK2) / (4 * sp.pi))
check("I3a alpha_geo = 4 l_P^2/<|K|^2>", sp.simplify(alpha_geo - 4 * sp.Symbol("lP2", positive=True) / KK2) == 0)
print("    NOTE: S^1 (K = d/dy, |K|^2 = R^2) gives 4 l_P^2/R^2, the AH6/F relation (recalled from those lanes, not re-run here).")
check("I3b S^2 pure-metric half: <|K|^2> = 2R^2/3 gives 6 l_P^2/R^2; the flux piece equals it at Minkowski, so 1/g^2 doubles and alpha_SU2 = 3 l_P^2/R^2",
      sp.simplify(4 / (avK["z"] / R ** 2) - 6) == 0 and sp.simplify((area * avmu["z"] / g ** 2 - area * avK["z"] / (2 * kap ** 2)).subs(subsM)) == 0)

print("\nI5  chirality / content lattice of the S^2 map (spinor zero-mode counts RECALLED; algebra checked)")
k_, Qm = sp.symbols("k Q", positive=True)
check("I5a Dirac spectrum lambda^2 R^2 = k(k+|Q|) reproduced by (k+|Q|/2)^2 - Q^2/4 (algebra of the recalled j-spectrum); lowest level k = 0 has j = (|Q|-1)/2, multiplicity |Q|",
      sp.expand((k_ + Qm / 2) ** 2 - Qm ** 2 / 4 - k_ * (k_ + Qm)) == 0)
SM = {"Q": (2, Fraction(1, 6)), "L": (2, Fraction(-1, 2)), "u^c": (1, Fraction(-2, 3)), "d^c": (1, Fraction(1, 3)), "e^c": (1, Fraction(1))}
print("    S^2 map: dim_SU2 = |q N|  =>  |Y_f|/dim_f = |s|/N must be the SAME for every field (Y = s q).  SM left-handed Weyl content per generation:")
vals = {f: abs(y) / d for f, (d, y) in SM.items()}
for f, v in vals.items():
    print(f"      {f:4s} dim_SU2 = {SM[f][0]}  Y = {str(SM[f][1]):>5s}  |Y|/dim = {v}")
eq_sets = [S for r in range(2, 6) for S in itertools.combinations(SM, r) if len({vals[f] for f in S}) == 1]
print(f"    subsets (size >= 2) with equal |Y|/dim: {eq_sets if eq_sets else 'none'}")
check("I5b NO subset of two or more SM fields has equal |Y|/dim: the SM hypercharge lattice cannot be the S^2 flux U(1) (the doublets alone: Q 1/12 vs L 1/4)", len(eq_sets) == 0)
check("I5c the map requires |Y_doublet| = 2 |Y_singlet| for every (doublet, singlet) pair; no SM pair satisfies it (|Y_L|/|Y_e^c| = 1/2, |Y_Q|/|Y_u^c| = 1/4, ...)",
      not any(abs(SM[a][1]) == 2 * abs(SM[b][1]) for a in ("Q", "L") for b in ("u^c", "d^c", "e^c")))

print("\nI6  scope of the relations (statement only; not a check)")
for s in ("tree level at mu_c = 1/R; no running, no KK threshold",
          "radion (l = 0) direction only; fluxed dS_p x S^q is generically unstable in other modes (hep-th/0205080, abstract read by lane F)",
          "Minkowski point requires Lambda_6 tuned to 2 (R/l_P)^2 x ~ 3e-119 of its value (f2 B2e): the vacuum-energy problem re-enters",
          "chat = g^2/kappa is a free continuous real: alpha_SU2 = 3 chat^2/(2 pi^2 N^4)",
          "4D gauge group SU(2) x U(1) only; there is no SU(3); the SU(2) is a KK isometry with unit-index generators"):
    print("    *", s)


print("\nCross-check against lane F's own script (run as a subprocess, PASS lines B3d/B3e read)")
here = os.path.dirname(os.path.abspath(__file__))
f2 = os.path.join(here, "..", "F_kk_stabilization", "f2_flux_freund_rubin.py")
env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")
proc = subprocess.run([sys.executable, f2], capture_output=True, text=True, env=env)
out = proc.stdout
ok_f2 = proc.returncode == 0 and "[PASS] B3d Minkowski point: alpha_SU2 = 3 l_P^2/R^2" in out and "[PASS] B3e Minkowski point: alpha_U1(unit charge) = N^2 l_P^2/(2 R^2)" in out
check("X1 lane F f2 run exits 0 and its B3d/B3e (alpha_SU2 = 3, alpha_U1 = N^2/2) PASS lines agree with this independent derivation", ok_f2, f"(f2 exit {proc.returncode})")

n_ok = sum(1 for _, o in CHECKS if o)
print("\n" + "=" * 100)
print(f"CHECKS: {n_ok}/{len(CHECKS)} passed")
print("SCOPE (exact): tree-level relations at mu_c = 1/R for the Minkowski point of 6D Einstein-Maxwell-Lambda on S^2 with integer flux N;")
print("  alpha_SU2 = 3 l_P^2/R^2, alpha_U1(unit) = N^2 l_P^2/(2 R^2), ratio N^2/6 (chat-free); overall coupling = 3 chat^2/(2 pi^2 N^4) with chat FREE.")
print("  The SM hypercharge lattice is NOT reproducible by this U(1) (I5).")
sys.exit(0 if n_ok == len(CHECKS) else 1)
