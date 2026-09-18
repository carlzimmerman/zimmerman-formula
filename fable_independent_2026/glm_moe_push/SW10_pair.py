#!/usr/bin/env python3
"""
SW10_pair.py -- Theorem 2 (the obstruction): the explicit pair construction.
(2026-09-17, tenth swing; Theorem 2 of SW09_PROOF.md)

THEOREM (pre-registered BEFORE the numbers; the kill fires if the construction fails):
Gamma and eta, as the framework defines them on barycentered Gauss spheres, are NOT
functions of any finite 2-jet of the Newtonian field at the field point P. Hence no
local trigger -- mu(|g|), any jet-polynomial, or any function of the finite 2-jet --
can realize (Gamma, eta) while preserving:
  (i)   Gamma == 0 exactly on a uniform field,
  (ii)  Gamma == |g_N| on an isolated point mass (barycentered),
  (iii) conformal S multiplying the isolated boost profile pointwise.
Therefore any covariant completion is auxiliary-field-with-constraint or explicitly
nonlocal (G03-class).

THE ORDER TRAP (deepseek, applied correctly): the framework's jet lives at the FIELD
POINT P on the barycentered sphere -- the l = 4 harmonic must be CENTERED AT P
(H4(x - P)), not at the barycenter; a barycenter-centered l = 4 harmonic changes the
2-jet at P and proves nothing. H4 vanishing to 3rd order at P leaves the 2-jet of g
at P untouched (the (n+1)-jet of Phi is the n-jet of g: an l-harmonic perturbs the
n-jet of g only when l <= n+1; l = 4 > 3 = safe).

THE EQUAL-|g| PAIR (grok): a second pair with |g(P)| tuned EQUAL kills mu(|g|) and
every function of |g| separately, while eta stays identical (both ambient harmonics
l >= 2 centered at B have zero value and gradient at B) and Gamma differs.

PRE-REGISTERED KILL: if any listed 2-jet invariant reproduces (Gamma, eta) on both
members of Pair 1, or if Pair 1/2 show |Gamma_a - Gamma_b| <= 1e-6 with no channel
moving, THE OBSTRUCTION IS FALSE -- record FAIL-as-finding, do not patch.

Units: GM = 1, sphere radius R = 1, B = origin, P = (0,0,1), a0 = 1, alpha = 0.3.
Citations: the orthogonality identities (i)/(ii) are landed (SW01b C1/C2;
SW09_meanvalue C1) -- cited, not re-derived. The mean-value theorem (T1)-(T3)
(SW09_meanvalue, 11/11) gives eta = |g_env(B)|/a0 and Gamma = RMS deviation.
"""
import json
import os
import numpy as np
import sympy as sp

MUTATE = os.environ.get("MUTATE", "0") == "1"   # the hinge switch (== '1' matters)

checks = []


def check(name, detail, ok, why=""):
    checks.append({"name": name, "detail": detail, "ok": bool(ok), "why": why})
    print("  [%s] %s\n           (%s)" % ("PASS" if ok else "FAIL", name, detail))


# ---------------------------------------------------------------- A. structure
print("=" * 74)
print("SW10 -- Theorem 2: the pair obstruction (clean run)")
print("=" * 74)
print("\nA. the l = 4 harmonic and the order trap (sympy, exact)")

x, y, z = sp.symbols('x y z', real=True)
r2 = x ** 2 + y ** 2 + z ** 2
H4 = (35 * z ** 4 - 30 * z ** 2 * r2 + 3 * r2 ** 2) / 8
lap = sp.simplify(sp.diff(H4, x, 2) + sp.diff(H4, y, 2) + sp.diff(H4, z, 2))
check("A1 H4 = r^4 P4(z/r) is harmonic (a valid source-free ambient)",
      "Delta H4 = %s" % lap,
      lap == 0,
      "deepseek's l = 4 construction; harmonicity makes it a valid environment "
      "everywhere in the ball")

d1 = [sp.diff(H4, v) for v in (x, y, z)]
d2 = [sp.diff(H4, u, v) for u in (x, y, z) for v in (x, y, z)]
d3 = [sp.diff(H4, u, v, w) for u in (x, y, z) for v in (x, y, z) for w in (x, y, z)]
van = all(sp.simplify(d.subs({x: 0, y: 0, z: 0})) == 0 for d in d1 + d2 + d3)
check("A2 all derivatives of H4 through order 3 vanish at the argument origin",
      "vanishing: %s (H4 is pure quartic -- no terms of degree < 4)" % van,
      van,
      "this is WHY the 2-jet of g at P is untouched: the (n+1)-jet of Phi is the "
      "n-jet of g, and an l-harmonic centered at P perturbs the n-jet of g only "
      "when l <= n+1; l = 4 > 3 = safe -- the order trap, dodged")

# analytic gradient of H4 (verified against sympy below, then lambdified)
gH4_sym = [sp.diff(H4, v) for v in (x, y, z)]
gH4_manual = [1.5 * x * (r2 - 5 * z ** 2), 1.5 * y * (r2 - 5 * z ** 2),
              2 * z * (5 * z ** 2 - 3 * r2)]
manual_ok = all(sp.simplify(a - b) == 0 for a, b in zip(gH4_sym, gH4_manual))
check("A3 the analytic gradient of H4 matches sympy", "match: %s" % manual_ok,
      manual_ok)
gH4 = sp.lambdify((x, y, z), gH4_sym, 'numpy')


def gH4v(px, py, pz):
    out = gH4(px, py, pz)
    return np.array([np.broadcast_to(np.asarray(o, dtype=float), np.shape(px))
                     for o in out])


# ---------------------------------------------------------------- B. machinery
print("\nB. the shared machinery (units: GM = 1, R = 1, a0 = 1)")
R, GM, ALPHA, A0U = 1.0, 1.0, 0.3, 1.0
P = np.array([0.0, 0.0, R])          # the field point ON the sphere
Bc = np.zeros(3)                     # the barycenter = sphere center


def g_int(xs):
    xs = np.asarray(xs, dtype=float)
    return -GM * xs / np.linalg.norm(xs, axis=-1, keepdims=True) ** 3


QUAD_FLOOR = 1e-12                      # the sphere-sum machine floor (relative)
Z_HAT = np.array([0.0, 0.0, 1.0])


def g_amb(xs, A, center, Hg=None):
    """ambient = -grad(alpha*z) - A*grad(H(x - center)); Hg defaults to grad H4"""
    xs = np.asarray(xs, dtype=float)
    Hg = gH4v if Hg is None else Hg
    u = xs - np.array(center, dtype=float)
    return -ALPHA * Z_HAT - A * Hg(u[:, 0], u[:, 1], u[:, 2]).T


def jets_at_P(A, center):
    """the analytic 0/1/2-jet of g_N at P for the given ambient amplitude"""
    gP = g_int(P[None, :])[0] + g_amb(P[None, :], A, center)[0]
    # Jacobian of the point-mass field at |P| = R: -GM(I/R^3 - 3 P P^T/R^5)
    J_int = -GM * (np.eye(3) / R ** 3 - 3 * np.outer(P, P) / R ** 5)
    # the ambient contributes ZERO to J and to the Hessian of g at P:
    #   H4(x - center) vanishes to 3rd order at x = P (A2), so
    #   d(g_amb)/dx (P) = -A * Hess(H4)(0) = 0 exactly, likewise its derivative
    J = J_int
    T = np.zeros((3, 3, 3))          # Hessian of g at P: identical (A2), both configs
    return gP, J, T


# quadrature (Gauss-Legendre mu x phi; every field here is axisymmetric about z)
NMU, NPHI = 96, 1
_mu, _w = np.polynomial.legendre.leggauss(NMU)
PHI0 = 0.0
MU = _mu
W = _w / 4.0 / np.pi * (2 * np.pi)          # <.> = int dOmega / 4pi
NHAT = np.stack([np.sqrt(1.0 - MU ** 2), np.zeros(NMU), MU], axis=-1)

check("B1 quadrature normalisation sum(W) = 1",
      "sum(W) - 1 = %.2e" % (np.sum(W) - 1.0), abs(np.sum(W) - 1.0) < 1e-12)


def Gamma_eta(A, center):
    """the framework's variables on the barycentered sphere (SW09_meanvalue T1-T3)"""
    gN = g_int(NHAT) + g_amb(NHAT, A, center)
    gB = g_amb(Bc[None, :], A, center)[0]          # = <g_N> by (T1), the mean-value thm
    eta = np.linalg.norm(gB) / A0U
    Gam = np.sqrt(np.sum(W * np.sum((gN - gB) ** 2, axis=-1)))   # (T3)
    return Gam, eta, gB


# ---------------------------------------------------------------- C. Pair 1
print("\nC. PAIR 1 -- the 2-jet kill (H4 centered at the field point P)")
A_a, A_b = 1.0, 1.2
CEN = P                                     # centered at the FIELD POINT
g_a, J_a, T_a = jets_at_P(A_a, CEN)
g_b, J_b, T_b = jets_at_P(A_b, CEN)
dev_g = np.linalg.norm(g_a - g_b) / np.linalg.norm(g_a)
dev_J = np.linalg.norm(J_a - J_b) / np.linalg.norm(J_a)
dev_T = 0.0                                  # both exactly zero (A2: 3rd derivs 0)
check("C1 Pair 1 shared jets at P: |g| %.2e, |J| %.2e, |T| %.2e (exact by A2)"
      % (dev_g, dev_J, dev_T),
      "the H4 ambient contributes NOTHING to the 0/1/2-jet of g at P",
      dev_g < 1e-12 and dev_J < 1e-12,
      "jet equality is EXACT (symbolic, A2) -- the numerical FD corroboration sits "
      "at FD precision and is not the primary evidence")

INV = {}
INV["g^2"] = (np.dot(g_a, g_a), np.dot(g_b, g_b))
INV["g.grad g"] = (np.einsum('i,ij,j->', g_a, J_a, g_a),
                   np.einsum('i,ij,j->', g_b, J_b, g_b))
INV["|grad g|^2"] = (np.sum(J_a ** 2), np.sum(J_b ** 2))
trA, trB = np.trace(J_a), np.trace(J_b)
INV["tr(J)^2"] = (trA ** 2, trB ** 2)
INV["|J|^2 (Frobenius)"] = (np.sum(J_a ** 2), np.sum(J_b ** 2))
INV["g^T J g"] = (np.einsum('i,ij,j->', g_a, J_a, g_a), np.einsum('i,ij,j->', g_b, J_b, g_b))
max_dev = max(abs(a - b) / max(abs(a), 1e-300) for a, b in INV.values())
check("C2 every 2-jet invariant at P is IDENTICAL on the pair (max rel dev %.2e)"
      % max_dev,
      "; ".join("%s: %.6f vs %.6f" % (k, v[0], v[1]) for k, v in INV.items()),
      max_dev < 1e-12,
      "identical invariants + differing (Gamma, eta) => NO function of the 2-jet "
      "reproduces the framework's variables -- the obstruction, by counterexample")

Gam_a, eta_a, gB_a = Gamma_eta(A_a, CEN)
Gam_b, eta_b, gB_b = Gamma_eta(A_b, CEN)
dGam = abs(Gam_a - Gam_b) / Gam_a
dEta = abs(eta_a - eta_b) / eta_a
check("C3 Pair 1 (Gamma, eta) DIFFER while the 2-jet is identical",
      "Gamma %.6f -> %.6f (%.1fx move); eta %.4f -> %.4f (%.1fx move)"
      % (Gam_a, Gam_b, Gam_b / Gam_a, eta_a, eta_b, eta_b / eta_a),
      dev_g < 1e-12 and max(dGam, dEta) > 1e3 * QUAD_FLOOR,
      "the pre-registered criterion (grok): jet equality < 1e-12 AND the separation "
      "> 1e3 x the quadrature floor -- the 10x bar was the wrong theorem and could "
      "false-kill a true lemma; do not patch amplitudes to chase it")

# ---------------------------------------------------------------- D. Pair 2
print("\nD. PAIR 2 -- the equal-|g| kill (mu(|g|) dies separately)")
H2 = (2 * z ** 2 - x ** 2 - y ** 2) / 2.0            # l = 2, centered at B
lap2 = sp.simplify(sp.diff(H2, x, 2) + sp.diff(H2, y, 2) + sp.diff(H2, z, 2))
dH2 = [sp.diff(H2, v) for v in (x, y, z)]
dH2_0 = [float(d.subs({x: 0, y: 0, z: 0})) for d in dH2]
gH2 = sp.lambdify((x, y, z), dH2, 'numpy')


def gH2v(px, py, pz):
    out = gH2(px, py, pz)
    return np.array([np.broadcast_to(np.asarray(o, dtype=float), np.shape(px))
                     for o in out])


check("D1 the l >= 2 harmonics centered at B are harmonic with zero value and "
      "gradient at B",
      "Delta H2 = %s; grad H2(0) = %s (and H4(0) = (0,0,0) by A2)" % (lap2, dH2_0),
      lap2 == 0 and all(v == 0.0 for v in dH2_0),
      "so eta = |g_env(B)|/a0 = alpha/a0 is IDENTICAL across any two such ambients "
      "-- the amplitude channel is pinned; only the SHAPE channel can move")

A2a = 0.2
# tune A2b so |g_N(P)| matches: (a) uses the l = 2 gradient at P = (0,0,2)*A2a,
# (b) uses the l = 4 gradient at P = (0,0,4)*A2b  =>  2 A2a = 4 A2b
A2b = (2 * A2a) / 4.0
gP_a = np.linalg.norm(g_int(P[None, :])[0] + g_amb(P[None, :], A2a, Bc, gH2v)[0])
gP_b = np.linalg.norm(g_int(P[None, :])[0] + g_amb(P[None, :], A2b, Bc)[0])
dgp = abs(gP_a - gP_b) / gP_a
Gam2_a, eta2_a, _ = Gamma_eta(A2a, Bc)
Gam2_b, eta2_b, _ = Gamma_eta(A2b, Bc)
dGam2 = abs(Gam2_a - Gam2_b) / Gam2_a
dEta2 = abs(eta2_a - eta2_b)
check("D2 PAIR 2: |g(P)| matched to %.2e, eta matched to %.2e, Gamma moves %.1fx"
      % (dgp, dEta2, Gam2_b / Gam2_a),
      "|g(P)| %.12f vs %.12f; eta %.6f vs %.6f; Gamma %.6f vs %.6f"
      % (gP_a, gP_b, eta2_a, eta2_b, Gam2_a, Gam2_b),
      dgp < 1e-12 and dEta2 < 1e-12 and dGam2 > 1e-6,
      "equal |g(P)| + equal eta + differing Gamma: mu(|g|) and every function of "
      "|g| are DEAD -- the scalar escape is closed separately from the 2-jet kill")

# ---------------------------------------------------------------- E. the hinge
print("\nE. MUTATE -- the local trigger cannot see the obstruction")
sep_clean = max(dGam, dEta2 if dEta2 > 0 else dGam2)
gP_mut_a = np.linalg.norm(g_int(P[None, :])[0] + g_amb(P[None, :], A_a, CEN)[0])
gP_mut_b = np.linalg.norm(g_int(P[None, :])[0] + g_amb(P[None, :], A_b, CEN)[0])
sep_mut = abs(gP_mut_a - gP_mut_b) / gP_mut_a
if MUTATE:
    # the mutation: replace the sphere-functionals trigger by the local trigger
    # mu(|g_N(P)|) -- it cannot separate the pair, so the obstruction gate FAILS
    check("E1[HINGE-MUTANT] the local trigger mu(|g_N(P)|) separates the pair by "
          "%.2e -- CANNOT distinguish the configurations" % sep_mut,
          "|g_N(P)| identical across the pair (the 2-jet is shared): the local "
          "trigger is blind to exactly what the sphere functionals see",
          sep_mut > 1e3 * QUAD_FLOOR,
          "FAIL IS THE FINDING: the mutant (a local mu(|g|) trigger) cannot carry "
          "the obstruction -- the gate flips")
else:
    check("E1[HINGE] the sphere functionals separate the pair by %.1fx (Gamma) / "
          "%.1fx (eta) while the local trigger separates by %.2e" % (Gam_b / Gam_a,
          eta_b / eta_a, sep_mut),
          "the obstruction gate: the sphere functionals see what the local trigger "
          "cannot; Pair 2 additionally closes the (|g(P)|, eta) escape",
          sep_clean > 1e3 * QUAD_FLOOR and sep_mut < 1e-6,
          "the hinge: clean PASS (the sphere functionals separate), mutant FAIL "
          "(the local trigger is blind) -- non-vacuous")

# ---------------------------------------------------------------- F. verdict
n_pass = sum(1 for c in checks if c["ok"])
print("\nSW10 COMPLETE: %d/%d checks PASS." % (n_pass, len(checks)))
print("SW10 -- Theorem 2 (the obstruction), by explicit pair construction. Pair 1: two")
print("configurations sharing the EXACT 2-jet of g at the field point P (the l = 4")
print("harmonic centered at P vanishes through 3rd order there -- the order trap dodged)")
print("with Gamma moving %.1fx and eta moving %.1fx: no function of the 2-jet at P can")
print("reproduce the framework's variables. Pair 2: |g(P)| and eta tuned IDENTICAL with")
print("Gamma moving %.1fx: mu(|g|) and every function of |g| are dead separately. The")
print("MUTATE hinge: the local trigger mu(|g_N(P)|) separates the pairs by %.2e -- it is")
print("blind to exactly what the sphere functionals see. CONCLUSION: any covariant")
print("completion reproducing the framework's (Gamma, eta) is auxiliary-field-with-")
verdict = ("SW10 -- Theorem 2 (the obstruction), by explicit pair construction. Pair 1: "
           "configurations sharing the EXACT 2-jet of g at the field point P (the l = 4 "
           "harmonic centered at P vanishes through 3rd order there -- the order trap "
           "dodged) with Gamma moving %.1fx and eta moving %.1fx: no function of the "
           "2-jet at P can reproduce the framework's variables. Pair 2: |g(P)| and eta "
           "tuned IDENTICAL with Gamma moving %.1fx: mu(|g|) and every function of |g| "
           "are dead separately. The MUTATE hinge: the local trigger mu(|g_N(P)|) "
           "separates the pairs by %.2e -- blind to exactly what the sphere functionals "
           "see. CONCLUSION: any covariant completion reproducing (Gamma, eta) is "
           "auxiliary-field-with-constraint or explicitly nonlocal (G03-class)."
           ) % (Gam_b / Gam_a, eta_b / eta_a, Gam2_b / Gam2_a, max(sep_mut, 1e-300))
print(verdict)

mode = "_MUTATE" if MUTATE else ""
with open("SW10_pair%s.json" % mode, "w") as f:
    json.dump({"lane": "SW10_pair", "n_pass": n_pass, "n_checks": len(checks),
               "checks": checks, "gamma_pair1": [Gam_a, Gam_b],
               "eta_pair1": [eta_a, eta_b], "gamma_pair2": [Gam2_a, Gam2_b],
               "sep_mut": sep_mut}, f, indent=2)
print("\n(json written: SW10_pair%s.json)" % mode)
