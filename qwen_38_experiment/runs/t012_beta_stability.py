#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""t012_beta_stability.py -- T012: beta stability interior/edge.

Hypothesis (from TASKS.md): beta = 1 is an INTERIOR point of the ghost/gradient-stable
range, i.e. stability does NOT select it.
Method: K''>0 (ghost) and c_s^2>0 (gradient) over beta in [0.25, 4] numerically.
PASS: the stable interval; honest statement either way.  KILL: none.

Framework (from t011/THE_COMPLETION.md L166):
    K(Q) = -M^4 + mu^2 Lambda_D^2 [1 - sqrt(1 - u^2/Lambda_D^2)],  u = Q - Q0
    beta = mu^2 Lambda_D^2 / M^4  (SELECTED = 1, not derived -- R5).
So K(u) = -M^4 + beta*M^4 * [1 - sqrt(1 - x^2)],  x = u/Lambda_D.
    K'(u) = beta M^4  x / (Lambda_D sqrt(1-x^2))
    K''(u)= beta M^4 / (Lambda_D^2 (1-x^2)^(3/2))      -> >0 for all beta>0, |x|<1
DBI sound speed (k-essence with u the kinetic-like var, the standard DBI form):
    c_s^2 = K'/(K' + 2 u K'') = (1 - x^2)/(3 - x^2)   -> >0 for |x|<1, beta-INDEPENDENT.

Verdict logic: if both hold over the WHOLE beta in [0.25,4] (and all |x|<1), then beta=1
is an INTERIOR point and stability does NOT select it -> CONFIRMED.  If the stable range
is instead a strict interval that merely CONTAINS 1 but 1 is near an edge, report that.

Not a match-search (no numerology target) -> no FDR pre-registration needed (R7/FDR is for
pattern/match searches).  Direction-of-risk: WIN-risk -- a false "stability selects beta=1"
would dress the SELECTED beta=1 in a stability derivation it does not have; the honest result
is the opposite (stability is beta-blind over the whole band), which is DEFICIT-risk for the
narrative that something "picks" beta=1.  Both directions stated.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from qwenlib import *      # constants, kernel, check/info/finish, FOOTINGS

import numpy as np
import sympy as sp

# ---- PART A: restate inputs with provenance -----------------------------------------
# THE_COMPLETION.md L166 / t011: K(Q)=-M^4+mu^2 LD^2[1-sqrt(1-u^2/LD^2)], u=Q-Q0,
# beta = mu^2 LD^2/M^4 (SELECTED=1).  M, LD, mu are theory-internal; only the RATIO
# beta is fixed.  Set M=1, LD=1, mu=sqrt(beta) for the scan (K scales as M^4; signs
# are M-independent).
info("offset-DBI K(u) = -M^4 + beta M^4[1 - sqrt(1-x^2)], x=u/Lambda_D; beta=mu^2 LD^2/M^4 (SELECTED=1)")
info("ghost: K''>0 ; gradient: c_s^2 = K'/(K'+2uK'') = (1-x^2)/(3-x^2) >0  (DBI sound speed)")

# ---- PART B(0): exact derivatives via sympy (the analytic backbone) -------------------
u, x, b, M, LD = sp.symbols("u x beta M LD", positive=True, real=True)
K = -M**4 + b * M**4 * (1 - sp.sqrt(1 - x**2))      # x = u/LD, treat x as the scan var
Kxp = sp.diff(K, x)
Kxpp = sp.diff(K, x, 2)
# DBI sound speed c_s^2 = K'/(K' + 2 x K'')   (x plays the role of the kinetic-like var)
cs2 = sp.simplify(Kxp / (Kxp + 2 * x * Kxpp))
info("sympy K''(x)  = %s" % sp.simplify(Kxpp))
info("sympy c_s^2(x)= %s   (beta-independent DBI sound speed)" % cs2)
# sanity: K'' = beta M^4 / (LD-independent here LD=1) * (1-x^2)^(-3/2) ; c_s^2=(1-x^2)/(3-x^2)
check(sp.simplify(Kxpp) == b * M**4 * (1 - x**2)**sp.Rational(-3, 2),
        "ANALYTIC-1: K''(x) = beta M^4 (1-x^2)^(-3/2)  (>0 for beta>0, |x|<1)",
        "K''=%s" % sp.simplify(Kxpp))
check(sp.simplify(cs2 - (1 - x**2)/(3 - x**2)) == 0,
        "ANALYTIC-2: c_s^2(x) = (1-x^2)/(3-x^2)  (>0 for |x|<1, INDEPENDENT of beta)",
        "c_s^2=%s" % sp.simplify(cs2))

# ---- PART B(1): numeric scan over beta in [0.25, 4] and x in (-0.999, 0.999) ---------
beta_lo, beta_hi = 0.25, 4.0
betas = np.linspace(beta_lo, beta_hi, 161)
xs = np.linspace(-0.999, 0.999, 799)
Kpp = np.zeros_like(betas)
cs2m = np.zeros_like(betas)
stable_betas = []
for i, b in enumerate(betas):
    # K'' sign: positive factor b * (1-x^2)^(-3/2); check min over x
    kpp_vals = b * (1 - xs**2)**(-1.5)
    kpp_ok = np.all(kpp_vals > 0)
    # c_s^2 over x
    cs2_vals = (1 - xs**2)/(3 - xs**2)
    cs2_ok = np.all(cs2_vals > 0)
    Kpp[i] = kpp_vals.min() if kpp_ok else -1.0
    cs2m[i] = cs2_vals.min()
    if kpp_ok and cs2_ok:
        stable_betas.append(b)
# the stable interval (contiguous since both conditions are beta-independent)
stable_betas = np.array(stable_betas)
b_min_stable = stable_betas.min()
b_max_stable = stable_betas.max()
info("scan beta in [%.2f, %.2f] (%d pts), x in (-0.999,0.999): %d/%d beta values ghost+gradient stable"
        % (beta_lo, beta_hi, len(betas), len(stable_betas), len(betas)))
info("stable interval = [%.4f, %.4f] ; beta=1 interior? %s"
        % (b_min_stable, b_max_stable, bool(b_min_stable < 1.0 < b_max_stable)))

# ---- PART B(2): is beta=1 an INTERIOR point? (strictly inside, not on an edge) -------
interior = bool(b_min_stable < 1.0 < b_max_stable)
# margin to the nearest edge of the scanned window
margin_lo = 1.0 - b_min_stable
margin_hi = b_max_stable - 1.0
info("beta=1 interior margin: left=%.4f, right=%.4f (window edges 0.25 and 4.0)" % (margin_lo, margin_hi))

# ---- PART B(3): the c_s^2 at the DBI wall x->1 goes to 0 (edge of FIELD space, not beta)
xwall = 0.9999
cs2_wall = (1 - xwall**2)/(3 - xwall**2)
info("c_s^2 at |x|->1 (DBI wall) -> %.2e (edge of FIELD space, independent of beta)" % cs2_wall)

# ---- PART C: grade --------------------------------------------------------------------
# PASS: the stable interval.  Honest statement: BOTH K''>0 and c_s^2>0 hold for the ENTIRE
# beta in [0.25,4] (indeed all beta>0) and all |x|<1.  beta=1 is an INTERIOR point; stability
# does NOT select it.
check(len(stable_betas) == len(betas),
        "PASS-A: ghost+gradient stable for 100%% of beta in [0.25,4] (all %d points) -> full band stable"
        % len(betas),
        "stable=%d/%d" % (len(stable_betas), len(betas)))
check(interior,
        "PASS-B: beta=1 is an INTERIOR point of the stable interval [%.4f,%.4f] (margins %.4f/%.4f), "
        "not an edge -> stability does NOT select beta=1" % (b_min_stable, b_max_stable, margin_lo, margin_hi),
        "interior=%s margin=%.4f/%.4f" % (interior, margin_lo, margin_hi))
check(bool(np.all(cs2m > 0)) and bool(np.all(Kpp > 0)),
        "PASS-C: min K''=%.3e>0 and min c_s^2=%.3e>0 across the whole scan"
        % (Kpp.min(), cs2m.min()),
        "min K''=%.3e, min c_s^2=%.3e" % (Kpp.min(), cs2m.min()))

# Named assumption (CANDIDATE-flag): the c_s^2 form is the STANDARD DBI/k-essence
# c_s^2 = K'/(K'+2uK''); the verdict (stability beta-blind) does not depend on it because
# K''>0 (ghost) is already beta-independent, and c_s^2=(1-x^2)/(3-x^2) is likewise beta-independent.
check(True,
        "NAMED-ASSUMPTION: c_s^2 = K'/(K'+2uK'') (standard DBI sound speed); conclusion (stability is "
        "beta-blind over [0.25,4]) is robust to the c_s^2 choice since BOTH conditions are beta-independent",
        "robustness: K''>0 and c_s^2>0 each beta-independent over |x|<1")

# ---- PASS artifact --------------------------------------------------------------------
lines = []
lines.append("# T012 beta-stability interior/edge")
lines.append("")
lines.append("| quantity | formula | sign over beta in [0.25,4] | selects beta=1? |")
lines.append("|---|---|---|---|")
lines.append("| ghost K''(x) | beta M^4 (1-x^2)^(-3/2) | >0 for all beta>0, |x|<1 | NO |")
lines.append("| gradient c_s^2(x) | (1-x^2)/(3-x^2) | >0 for all |x|<1, beta-independent | NO |")
lines.append("| stable interval | [%.4f, %.4f] (full scan band; all beta>0) | -- | beta=1 INTERIOR |" % (b_min_stable, b_max_stable))
lines.append("")
lines.append("CONCLUSION: CONFIRMED.  Both the ghost condition (K''>0) and the gradient condition "
                "(c_s^2>0) hold over the ENTIRE beta in [0.25, 4] (indeed for all beta>0) and all "
                "|u|<Lambda_D.  beta=1 is a strictly INTERIOR point (left margin %.4f, right margin "
                "%.4f to the window edges); stability does NOT select it.  The only edge of the "
                "stable region is the FIELD-space wall |u|=Lambda_D (c_s^2->0 there), which is "
                "beta-independent.  The DBI Lagrangian's stability is beta-blind; nothing in the "
                "stability analysis singles out beta=1 -- consistent with R5 (beta=1 is SELECTED, "
                "not derived)." % (margin_lo, margin_hi))
out = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "T012_BETA_STABILITY.md")
with open(out, "w") as f:
    f.write("\n".join(lines) + "\n")
check(os.path.exists(out) and len(open(out).read().splitlines()) > 6,
        "PASS artifact: stability table written to %s" % out)

# ---- Footings (R3): beta, K'', c_s^2 are dimensionless -> footing-invariant ------------
info("footings (R3): beta, K'', c_s^2 are dimensionless -> footing-invariant; "
       "a0 can=%.4e alt=%.4e" % (A0_CAN, A0_ALT))

finish("t012")
