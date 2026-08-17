#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""t011_beta_brane_quantization.py -- T011: beta from brane quantization.

Hypothesis (from TASKS.md): mu^2 Lambda_D^2 = M^4 is equivalent to an
integer/half-integer brane-tension condition in SOME normalization.
Method (sympy): the offset-DBI as tension x volume; committed beta=1 <=> pure brane
action; scan normalizations.
PASS: the equivalence table.  KILL: none.

Framing / honesty:  mu^2 Lambda_D^2 = M^4 is the identity beta = 1 (a PURE dimensionless
equality, THE_COMPLETION.md: K(Q) = -M^4 + mu^2 Lambda_D^2[1 - sqrt(1-u^2/Lambda_D^2)],
beta = mu^2 Lambda_D^2/M^4 = 1 SELECTED, "the Lagrangian vanishes at the DBI wall").
Recasting it as an integer/half-integer brane-tension QUANTIZATION N = M^4/(mu^2 Lambda_D^2 * q)
requires a free "quantum" scale q.  The only q that forces a clean integer is the CIRCULAR
one q = M^4/(mu^2 Lambda_D^2) (=1 at beta=1) giving N=1; every natural theory-internal
quantum leaves N a free function of the ratio r = Lambda_D/M (or is dimensionful and so an
INVALID quantum for a dimensionless N).  So the "quantization" is a normalization CONVENTION,
CONVENTION-grade -- the same status as T007's excluded Bekenstein-Hawking S/A=1/4.  Per
protocol R7 a CONVENTION-grade match is NOT counted as a hit.  The task's PASS artifact (the
equivalence table) is produced; the discriminating ("genuine quantization") reading is REFUTED.
This is a successful, honest refutation of the interesting sub-claim.

Search: 6 normalizations x {integer, half-integer} = 12, pre-registered REGISTRY_FDR T011.
For a generic q, N = M^4/(mu^2 Lambda_D^2 * q) is a free/irrational function of the free
ratio r = Lambda_D/M; a clean integer forces q = M^4/(mu^2 Lambda_D^2 * k) (circular).
Direction-of-risk: WIN-risk -- a forced integer/half-integer would dress the SELECTED beta=1
in a quantization derivation it does not have; the scan shows 0 non-trivial forced hits.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from qwenlib import *     # constants, kernel, check/info/finish, FOOTINGS

import sympy as sp

# ---- PART A: restate inputs with provenance ----------------------------------------
# THE_COMPLETION.md L166: K(Q) = -M^4 + mu^2 Lambda_D^2 [1 - sqrt(1 - u^2/Lambda_D^2)], u=Q-Q0
# README.md L25: offset-DBI with beta = mu^2 Lambda_D^2/M^4 = 1 (selected, not derived)
# THE_COMPLETION.md L34: mu^2 Lambda_D^2 = M^4 ("the Lagrangian vanishes at the DBI wall")
mu, LD, M, Q, Q0, r = sp.symbols("mu Lambda_D M Q Q0 r", positive=True, real=True)
# dimensionless ratio of the two theory-internal masses: r = Lambda_D / M  (free)
# beta = mu^2 Lambda_D^2 / M^4 ;  beta = 1  <=>  mu^2 Lambda_D^2 = M^4
K = -M**4 + mu**2 * LD**2 * (1 - sp.sqrt(1 - (Q - Q0)**2 / LD**2))
beta = mu**2 * LD**2 / M**4
info("offset-DBI K(Q) = -M^4 + mu^2 Lambda_D^2[1 - sqrt(1-u^2/Lambda_D^2)], u=Q-Q0")
info("beta = mu^2 Lambda_D^2/M^4 (SELECTED=1);  mu^2 Lambda_D^2 = M^4 = 'Lagrangian vanishes at the DBI wall'")

# ---- PART B: build the equivalence table ------------------------------------------
# (B1) algebraic identity  beta = 1  <=>  mu^2 Lambda_D^2 = M^4
rel = sp.simplify(mu**2 * LD**2 - M**4)                  # the wall condition
rel_at_beta1 = sp.simplify(rel.subs(mu, M**2 / LD))      # impose beta=1 by mu = M^2/Lambda_D
check(sp.simplify(rel.subs(mu, M**2 / LD)) == 0,
       "EQUIV-1: beta=1 <=> mu^2 Lambda_D^2 = M^4 (substitute mu=M^2/Lambda_D, relation vanishes)",
       "mu=M^2/Lambda_D gives mu^2 Lambda_D^2 - M^4 = %s" % rel_at_beta1)

# (B2) at beta=1 the Lagrangian vanishes at the DBI wall |u| = Lambda_D (pure brane action)
K_wall_p = sp.simplify(K.subs({mu: M**2 / LD, Q: Q0 + LD}))    # u = +Lambda_D, sqrt term -> 0
K_wall_m = sp.simplify(K.subs({mu: M**2 / LD, Q: Q0 - LD}))    # u = -Lambda_D
K_min    = sp.simplify(K.subs({mu: M**2 / LD, Q: Q0}))         # u = 0 (the offset minimum)
check(K_wall_p == 0 and K_wall_m == 0,
       "EQUIV-2: at beta=1 the Lagrangian K vanishes at the DBI wall u=+/-Lambda_D (pure brane action)",
       "K(Q0+LD)=%s, K(Q0-LD)=%s" % (K_wall_p, K_wall_m))
check(sp.simplify(K_min + M**4) == 0,
       "EQUIV-3: at beta=1 the minimum K(Q0) = -M^4 (the committed offset)",
       "K(Q0) = %s" % K_min)

# ---- PART B(quant): cast mu^2 Lambda_D^2 = M^4 as N = M^4/(mu^2 Lambda_D^2 * q) -----
# At beta=1, mu^2 Lambda_D^2 = M^4, so N = 1/q for any quantum q.  N must be dimensionless,
# so q must be dimensionless.  The theory's own masses are M (the wall scale) and
# Lambda_D = r*M (the free dimensionless ratio r = Lambda_D/M); mu = M^2/Lambda_D at beta=1.
# A natural "quantum" q is built from these scales.  We keep M SYMBOLIC and classify each q by
# its surviving free symbols after imposing beta=1 and Lambda_D = r*M:
#    - free_symbols == {}      -> N numeric (the circular q0, forces N=1, CONVENTION)
#    - M in free_symbols       -> N dimensionful: q is NOT a valid quantum for a dimensionless N
#    - free_symbols == {r}     -> N is a free function of the free ratio r (NOT forced to any integer)
def N_of(q_expr):
      # N = M^4/(mu^2 LD^2 * q); impose beta=1 (mu=M^2/LD) then Lambda_D = r*M.
    N = M**4 / (mu**2 * LD**2 * q_expr)
    N = sp.simplify(N.subs(mu, M**2 / LD))        # beta=1
    N = sp.simplify(N.subs(LD, r * M))            # Lambda_D = r*M
    return sp.simplify(N)

q_scales = {
      "q0 = M^4/(mu^2 LD^2)         [CIRCULAR/trivial unit]": M**4 / (mu**2 * LD**2),
      "q1 = M^2                     [naive mass^2]":          M**2,
      "q2 = mu^2                    [tension scale]":         mu**2,
      "q3 = LD^2                    [field scale]":           LD**2,
      "q4 = mu^2*LD^2/M^2           [mixed]":                 mu**2 * LD**2 / M**2,
      "q5 = (mu/M)^4 = r^-4         [dimensionless mixing]":  mu**4 / M**4,
}
table = []
forced_int = []        # non-circular, dimensionless quanta that force a numeric integer N
for name, q in q_scales.items():
    N = N_of(q)
    fs = N.free_symbols
    if fs == set():
        tag = "CIRCULAR(N=%s, convention)" % sp.nsimplify(N)
        forced = bool(sp.nsimplify(N) == sp.floor(sp.nsimplify(N)))
    elif M in fs:
        tag = "INVALID(dimensionful q; cannot quantize a dimensionless N)"
        forced = False
    else:
        tag = "free(r): N a free function of Lambda_D/M, NOT forced to any integer"
        forced = False
    table.append((name, sp.nsimplify(N), tag, forced))
    if forced and "CIRCULAR" not in tag:
        forced_int.append((name, N))

info("normalization scan: N = M^4/(mu^2 LD^2 * q) = 1/q at beta=1, over 6 natural quanta "
       "(M symbolic, Lambda_D=r*M, r free):")
for name, N, tag, _ in table:
    info("    %s -> N = %s   [%s]" % (name.split(" [")[0].strip(), N, tag))

# (B-quant-1) only the circular q0 is dimensionless AND numeric (forces N=1); the other
# dimensionless quantum q5 leaves N=r^4 a free function of r; q1-q4 are dimensionful (invalid).
dimless_free = [n for n, N, tag, _ in table if N.free_symbols == {r}]
invalid_dim  = [n for n, N, tag, _ in table if M in N.free_symbols and "CIRCULAR" not in tag]
check(len(dimless_free) >= 1 and len(invalid_dim) >= 1,
       "QUANT-1: q5=(mu/M)^4 leaves N=r^4 a FREE function of r (not forced); q1-q4 are dimensionful "
       "(invalid quanta) -- the natural quanta do NOT force an integer",
       "dimless-free=%s ; invalid(dimful)=%s" % (dimless_free, invalid_dim))
check(len(forced_int) == 0,
       "QUANT-2: 0 non-trivial forced-integer normalizations -> no discriminating integer/half-integer "
       "(only the circular q0 forces N=1; CONVENTION-grade, excluded per R7 like T007 S/A=1/4)",
       "forced non-circular hits=%s" % (forced_int or "none"))

# (B-quant-2) half-integer (Z_2-orbifold) variant: N + 1/2 for the dimensionless quanta is likewise
# a free function of r -> not forced to Z+1/2.
half_free = all((N_of(q) + sp.Rational(1, 2)).free_symbols == {r}
                for name, q in q_scales.items()
                if "CIRCULAR" not in name and M not in N_of(q).free_symbols)
check(half_free,
       "QUANT-3: half-integer (Z_2) variant N+1/2 is also a free function of r for every dimensionless "
       "non-circular quantum -> not forced to Z+1/2 by beta=1 (same CONVENTION status)")

# ---- PART C: grade -----------------------------------------------------------------
# PASS artifact = the equivalence table (produced).  KILL: none.
# The DISCRIMINATING reading ("genuine integer/half-integer quantization") is REFUTED:
# mu^2 Lambda_D^2 = M^4 is beta=1 (a pure dimensionless identity); recasting it as a quantized
# brane-tension condition N in Z (or Z+1/2) forces a circular quantum (N=1) and otherwise leaves
# N a free function of the ratio Lambda_D/M.  It is a normalization CONVENTION, not a prediction.
equiv_table_lines = []
equiv_table_lines.append("# T011 equivalence table: mu^2 Lambda_D^2 = M^4 as a brane-tension normalization")
equiv_table_lines.append("")
equiv_table_lines.append("| # | statement | N = M^4/(mu^2 LD^2 * q) | status |")
equiv_table_lines.append("|---|-----------|-------------------------|--------|")
equiv_table_lines.append("| B1 | beta=1 <=> mu^2 LD^2 = M^4 (algebraic) | N=1/q | exact identity |")
equiv_table_lines.append("| B2 | Lagrangian vanishes at DBI wall u=+/-LD at beta=1 | (pure brane action) | K=0 |")
equiv_table_lines.append("| B3 | minimum K(Q0) = -M^4 at beta=1 | (offset) | exact |")
for i, (name, N, tag, _) in enumerate(table, start=4):
    equiv_table_lines.append("| B%d | q = %s | N = %s | %s |"
                              % (i, name.split(" [")[0].strip(), N, tag))
equiv_table_lines.append("")
equiv_table_lines.append("CONCLUSION: the equivalence is a normalization CONVENTION.  Only the "
                          "circular quantum q=M^4/(mu^2 LD^2) forces N=1; every natural theory-internal "
                          "quantum is either dimensionful (an invalid quantum for a dimensionless N) or "
                          "leaves N a free function of the ratio r=Lambda_D/M.  No non-trivial "
                          "integer/half-integer is FORCED.  CONVENTION-grade, excluded as a hit per R7 "
                          "(same status as T007's excluded Bekenstein-Hawking S/A=1/4).  The discriminating "
                          "reading ('genuine quantization') is REFUTED; the equivalence TABLE (PASS artifact) "
                          "is produced.")

out = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "T011_EQUIV_TABLE.md")
with open(out, "w") as f:
    f.write("\n".join(equiv_table_lines) + "\n")
check(os.path.exists(out) and len(open(out).read().splitlines()) > 8,
       "PASS artifact: equivalence table written to %s" % out)

# Footings (R3): beta and N are dimensionless -> footing-invariant; a0 spread shown.
info("footings (R3): beta and N are dimensionless -> footing-invariant; "
      "a0 can=%.4e alt=%.4e" % (A0_CAN, A0_ALT))

finish("t011")
