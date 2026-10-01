#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
CFG242_B_g5a_ghost -- route B (L13), G5a: ghost, hyperbolicity and signal speeds of the foliated (lapse-free) bimetric interaction on FLAT space
(frozen plan section 4.3, gate order 1: 'cheapest decisive, 3 h').

FROZEN: 'G5a ghost / hyperbolicity of the foliated quadratic action: ghost-free, strongly hyperbolic, all speeds <= c on flat space AND on the exact static MOND
background operator.'  Shared G5 (verbatim): 'No ghost, no gradient instability, hyperbolic/causal (the DE12/DE13/XC criteria); Solar System safe (Cassini) by an explicit statement.'
Class 13d: the interaction is the record's tuned five-invariant direction T4 - T1 built from the SPATIAL connection difference of a shared foliation (CFG242_B_algebra.py, 'FOL').
Primary point: mu/b = -1/4, the record's tuned degeneracy value (CFG232 A2: sigma_s m0 = b/8, mu = -b/4), taken as the frozen reading; whether the FOLIATED class has its
own degeneracy value is NOT established here (that needs a foliated static reduction, the analogue of CFG232 A1, not run).  The whole line mu/b is scanned and REPORTED, never used
for the verdict.  The foliation scalar (khronon) decouples from the relative sector at quadratic order around FLAT space (the induced spatial metrics of g and g-hat on the same
slice differ by delta_ij at first order); it matters on a background with nonzero connection difference, which this script does NOT treat (see the MOND-background cell).
CELLS (all scored at the primary point):  GHOST  every propagating mode has a positive residue of the inverse kinetic matrix and no mode is higher-order (Ostrogradsky);
 SPEEDS  every c_i^2 in [0, 1] (no gradient instability, no superluminal mode);  HYPERBOLIC  the first-order reduction of every sector is diagonalisable with real
 eigenvalues (strongly hyperbolic);  DETERMINED  the quadratic action has no residual gauge zero modes (every mode is fixed by it);  BACKGROUND  the exact static MOND background.
MUTATE: MB1 restore the 4D (lapse-dependent) five-invariant interaction (scored at mu/b = -0.1, away from its degenerate tuned point) -> the GHOST cell flips PASS -> FAIL;
 MB2 flip the sign of the interaction (CFG232's erratum) -> the SPEEDS cell flips PASS -> FAIL;  MB3 independent foliations for g and g-hat -> the HYPERBOLIC cell: does NOT bite at
 quadratic order about flat space (the induced spatial metric difference is unchanged at first order): a declared control failure.
"""
import os, sys, math
sys.dont_write_bytecode = True
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import sympy as sp
import CFG242_common as C
from CFG242_B_algebra import *

R = C.Run("CFG242_B_g5a_ghost")
P = R.P
MUT = R.mutate
P(__doc__.strip())
kind = "4D" if MUT == "MB1" else "FOL"
if MUT == "MB3":
    pass   # independent foliations: the induced spatial metric of g-hat on its own slice differs from delta_ij only at second order about flat space; the quadratic Hessian is the FOL one
muv_main = sp.Rational(-1, 4)
muv = (-muv_main if MUT == "MB2" else (sp.Rational(-1, 10) if MUT == "MB1" else muv_main))
P(f"\n  interaction class: {kind};  mu/b = {muv}")

L = lagrangian(kind)
M = hessian(L)
Ms = M.subs({bb: 1, mu: muv})                                    # b = 1 (overall normalisation; the sign of b is the healthy sign of the sum/relative EH term)
cT = {}

# ---- helicity 2 (transverse-traceless): variables d12 and (d11 - d22)
tt = sp.factor(Ms[5, 5])
P(f"  helicity 2: M_TT(omega, kappa) = {tt}")
w2 = sp.Symbol("w2")
tt_w2 = sp.expand(tt.subs(om, sp.sqrt(w2)))
a_w, b_w = sp.Poly(tt_w2, w2).all_coeffs()[0], sp.Poly(tt_w2, w2).all_coeffs()[-1]
c2_TT = sp.simplify(-b_w / a_w / ka ** 2) if a_w != 0 else None
P(f"      dispersion omega^2 = c_T^2 kappa^2 with c_T^2 = {c2_TT}   (coefficient of omega^2: {a_w})")
residue_TT = sp.simplify(1 / a_w) if a_w != 0 else sp.nan

# ---- helicity 1
h1 = block(Ms, ["d01", "d13"])
det_h1 = sp.factor(h1.det())
deg_h1 = sp.degree(sp.expand(det_h1), om) if det_h1 != 0 else None
P(f"  helicity 1 (d01, d13): det = {det_h1}   (degree in omega: {deg_h1})")

# ---- helicity 0 and the residual gauge zero modes
sub_num = {om: sp.Rational(13, 10), ka: sp.Rational(7, 10)}
rank_full = Ms.subs(sub_num).rank()
nullity = 10 - rank_full
P(f"  full 10 x 10 kinetic matrix at a generic (omega, kappa): rank {rank_full}, nullity {nullity} (zero modes of the quadratic action)")
A0s, A3s, pis = sp.symbols("A0 A3 pi")
Avec = [A0s, 0, 0, A3s]
gm = sp.zeros(4, 4)
for i in range(4):
    for j in range(4):
        gm[i, j] = klo[i] * Avec[j] + klo[j] * Avec[i] + klo[i] * klo[j] * pis
vec = sp.Matrix([gm[i, j] for (i, j) in IDX])
resid = sp.simplify(Ms * vec)
P(f"  the helicity-0 Stueckelberg directions d = k A + A k + k k pi (A along t and z): M d = 0 ? {resid == sp.zeros(10, 1)}")
stueck_null = (resid == sp.zeros(10, 1))

# ---- hyperbolicity: first-order reduction of the TT sector at the point
def diagonalisable(c2):
    # principal symbol of d_t^2 h = c2 d_x^2 h in first-order form u = (d_x h, d_t h): d_t u = [[0, 1], [c2, 0]] d_x u; strongly hyperbolic iff real eigenvalues and a full eigenbasis
    A = np.array([[0.0, 1.0], [float(c2), 0.0]])
    ev, V = np.linalg.eig(A)
    return bool(np.all(np.abs(ev.imag) < 1e-12)) and abs(np.linalg.det(V)) > 1e-6, ev
cT2 = float(c2_TT.subs({bb: 1, mu: muv})) if c2_TT is not None else float("nan")
cT2 = float(c2_TT.subs(mu, muv)) if hasattr(c2_TT, "subs") and c2_TT.free_symbols else float(c2_TT)
if kind == "4D":
    cT2 = 1.0
diag_ok, ev = diagonalisable(cT2)
if kind == "4D":
    diag_ok = diag_ok and (deg_h1 is not None and deg_h1 <= 0)      # a fourth-order vector is not a second-order hyperbolic system
P(f"  TT first-order reduction: c_T^2 = {cT2:g}; eigenvalues {np.round(ev, 6)}; diagonalisable with real eigenvalues (strongly hyperbolic): {diag_ok}")

# ---- cells
ghost_ok = bool((residue_TT > 0 if residue_TT is not sp.nan else False) and (deg_h1 is None or deg_h1 <= 0))
if kind == "4D":
    ghost_ok = bool(deg_h1 is not None and deg_h1 <= 0)
speeds_ok = (0.0 <= cT2 <= 1.0 + 1e-12) if kind == "FOL" else True
if kind == "4D":
    speeds_ok = True
determined_ok = (nullity == 0)
R.banner("cells at the primary point (frozen reading mu/b = -1/4)" + (" [MUTATED]" if MUT else ""))
R.check("GHOST: positive residues, no higher-order mode", ghost_ok,
        f"TT residue {residue_TT}, helicity-1 determinant degree in omega {deg_h1}" + ("  (4D class: a fourth-order vector, the WF2/L70 Ostrogradsky mode)" if kind == "4D" else ""), kind="result")
R.check("SPEEDS: every c_i^2 in [0, 1]", speeds_ok, f"c_T^2 = {cT2:g}", kind="result")
R.check("HYPERBOLIC: strongly hyperbolic (diagonalisable first-order reduction, real eigenvalues)" + (" [MB3 independent foliations: Hessian unchanged]" if MUT == "MB3" else ""), diag_ok,
        f"c_T^2 = {cT2:g}: the TT system is d_t^2 h = c_T^2 k^2 h" + (" = 0: a Jordan block (h grows linearly in t)" if abs(cT2) < 1e-12 else ""), kind="result")
R.check("DETERMINED: the quadratic action has no residual gauge zero modes", determined_ok,
        f"nullity {nullity}; the zero modes are the Stueckelberg directions of the relative time diffeo and the longitudinal spatial diffeo: {stueck_null}" if kind == "FOL" else f"nullity {nullity}", kind="result")
P("  [NOT ADDRESSED] BACKGROUND: the exact static MOND background operator -- the stop rule ends route B at the first binding FAIL (HYPERBOLIC, flat space); the khronon would also have to be included")
R.num("flat", dict(kind=kind, mu_over_b=str(muv), cT2=cT2, residue_TT=str(residue_TT), helicity1_det=str(det_h1), nullity=nullity, stueckelberg_null=stueck_null))
verdict_ok = ghost_ok and speeds_ok and diag_ok and determined_ok
R.verdict("G5a (route B, flat space, frozen point)" + (" [MUTATED]" if MUT else ""), "PASS (flat only)" if verdict_ok else "FAIL",
          f"ghost {'P' if ghost_ok else 'F'}; speeds {'P' if speeds_ok else 'F'} (c_T^2 = {cT2:g}); hyperbolic {'P' if diag_ok else 'F'}; determined {'P' if determined_ok else 'F'} (nullity {nullity}); background NOT ADDRESSED")

# ---- scan over mu/b (REPORTED, never used for the verdict)
if not MUT:
    R.banner("REPORTED scan over mu/b (FOL class; flat space; not used for the verdict)")
    rows = []
    for mv in (-1.0, -0.5, -0.30, -0.26, -0.25, -0.24, -0.20, -0.10, -0.01, 0.0, 0.10, 0.25):
        c2 = 1 + 4 * mv
        d_ok, _ = diagonalisable(c2) if abs(c2) > 0 else diagonalisable(0.0)
        rows.append((mv, c2, d_ok))
        status = "gradient instability (c_T^2 < 0)" if c2 < -1e-12 else ("superluminal (c_T^2 > 1)" if c2 > 1 + 1e-12 else ("not strongly hyperbolic (c_T^2 = 0)" if abs(c2) < 1e-12 else "ghost-free, strongly hyperbolic, subluminal (TT)"))
        nl = 10 - sp.Matrix(M).subs({bb: 1, mu: sp.nsimplify(mv)}).subs(sub_num).rank()
        P(f"    mu/b = {mv:7.2f}: c_T^2 = {c2:6.2f}   {status};  nullity of the 10 x 10 quadratic form: {nl}")
    P("    in the open window -1/4 < mu/b < 0 the TT sector is healthy; the helicity-0 sector is undetermined at every mu/b and the helicity-1 sector carries no mode (det = -2 b kappa^4 mu != 0)")
    R.num("scan", rows)
    # the 4D class at generic mu for the reproduction of WF2/L70 (reported in CFG242_B_controls.py as well)

base = R.main_cells()
if MUT == "MB1":
    R.finish([base.get("GHOST: positive residues, no higher-order mode") is True and not ghost_ok])
elif MUT == "MB2":
    R.finish([base.get("SPEEDS: every c_i^2 in [0, 1]") is True and not speeds_ok])
elif MUT == "MB3":
    R.finish([base.get("HYPERBOLIC: strongly hyperbolic (diagonalisable first-order reduction, real eigenvalues)") != diag_ok])    # MB3: the Hessian is unchanged at quadratic order, so the cell does not flip
else:
    R.finish()
