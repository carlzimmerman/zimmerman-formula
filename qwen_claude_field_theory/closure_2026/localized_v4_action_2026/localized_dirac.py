"""Finite-mode Dirac audit for the localized V4 action.

The localized fields carry no velocities by construction.  This file does not
declare them nondynamical: it feeds the full quadratic blocks to the existing
constraint engine and returns the actual bracket matrices.
"""
import sympy as sp

from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
CONSTRUCTION = HERE.parent / "clock_constitutive_construction_2026"
if str(CONSTRUCTION) not in sys.path:
    sys.path.insert(0, str(CONSTRUCTION))
from construct import canonical_constraints

from localized_action import C, ell, eta_U, eta_X, eta_V, eta_TT


def _scalar_nonzero():
    k = sp.symbols("k", positive=True)
    k2 = k**2
    z, n, B, chi, lam = sp.symbols("z n B chi lambda_chi", real=True)
    zd, nd, Bd, chid, lamd = sp.symbols(
        "zd nd Bd chid lambdad", real=True
    )
    Ktrace = -3*zd + k2*B
    U = Ktrace - chi
    base = (-6*zd**2 + 4*k2*zd*B
            - ell*(3*zd-k2*B)**2
            + k2*(2*z**2 - 4*n*z + (2-C)*n**2))
    local = eta_U*U**2 + eta_X*U*chi + lam*(chi + zd - k2*B)
    return {
        "L": sp.expand(base + local),
        "qs": [z, n, B, chi, lam],
        "vs": [zd, nd, Bd, chid, lamd],
        "k": k,
        "variables": [str(x) for x in [z, n, B, chi, lam]],
    }


def _scalar_zero():
    z, n, chi, lam = sp.symbols("z n chi lambda_chi", real=True)
    zd, nd, chid, lamd = sp.symbols("zd nd chid lambdad", real=True)
    # Homogeneous leaves have no inverse-Laplacian source: W=U=0.  The
    # localizer is retained only as its zero-mode constraint chi=0, enforced
    # by lambda, so this rank is not inferred by k -> 0.
    L = -3*C*zd**2 + lam*chi
    return {
        "L": sp.expand(L),
        "qs": [z, n, chi, lam],
        "vs": [zd, nd, chid, lamd],
        "k": sp.Integer(0),
        "variables": [str(x) for x in [z, n, chi, lam]],
    }


def _vector_block():
    k = sp.symbols("k", positive=True)
    S, A = sp.symbols("S A", real=True)
    Sd, Ad = sp.symbols("Sd Ad", real=True)
    V = k**2*S/2
    L = k**2*S**2/2 + eta_V*(2*A*V-k**2*A**2)
    return {"L": sp.expand(L), "qs": [S, A], "vs": [Sd, Ad]}


def _tensor_block():
    k = sp.symbols("k", positive=True)
    h, Q = sp.symbols("h Q", real=True)
    hd, Qd = sp.symbols("hd Qd", real=True)
    R = k**2*h/2
    Ktt2 = hd**2/2
    L = (hd**2-k**2*h**2)/2 + eta_TT*(Ktt2-2*Q*R+k**2*Q**2)
    return {"L": sp.expand(L), "qs": [h, Q], "vs": [hd, Qd]}


def flat_scalar_blocks():
    nonzero = _scalar_nonzero()
    zero = _scalar_zero()
    return {
        "k_nonzero": {
            "kernel_dimension": 0,
            "scalar": nonzero,
            "vector": _vector_block(),
            "tensor": _tensor_block(),
        },
        "k_zero": {
            "kernel_dimension": 1,
            "scalar": zero,
            "vector": None,
            "tensor": None,
        },
    }


def _audit_block(block):
    return canonical_constraints(block["L"], block["qs"], block["vs"])


def constraint_matrix(block):
    # The canonical engine serializes the actual matrix.  Expose a SymPy
    # matrix for callers that need an independent rank calculation.
    report = _audit_block(block)
    return sp.Matrix(sp.sympify(report["poisson_matrix"]))


def dirac_report(mode):
    blocks = flat_scalar_blocks()
    if mode not in blocks:
        raise ValueError("mode must be 'k_nonzero' or 'k_zero'")
    scalar = _audit_block(blocks[mode]["scalar"])
    result = {
        "mode": mode,
        "scalar": scalar,
        "poisson_matrix": scalar["poisson_matrix"],
        "rank": scalar["poisson_rank"],
        "closure": scalar["generations"],
    }
    if mode == "k_nonzero":
        result["vector"] = _audit_block(blocks[mode]["vector"])
        result["tensor"] = _audit_block(blocks[mode]["tensor"])
    return result
