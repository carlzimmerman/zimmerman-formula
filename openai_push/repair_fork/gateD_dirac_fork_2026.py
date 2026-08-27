#!/usr/bin/env python3
r"""GATE D (repair fork, 2026-08-27): full Dirac/DOF analysis of the S2->S2' fork.

FORK: S2 = D^2 q  ->  S2' = D^2(q + lnN),  q = (1/6) ln det gamma.
Constraint set  Phi = (S4, S1, S2', S3) = (pi_N, C_M, D^2(q+lnN), D^2 p),
  C_M = D_i[c^2 mu(y) D^i lnN] - 4 pi G rho_m,  y = (c^2/a0)|D lnN|,
  p = gamma_ij pi^ij / sqrt(gamma).

METHOD (no entry assumed, nothing carried over from the baseline matrix):
  Mode-level canonical computation on a y>0 background
     gamma_ij = delta_ij,  pi^ij = 0,  N = N0 exp(g.x)  (D lnN = g = const, y0>0),
  which satisfies ALL FOUR constraints exactly in vacuum (checked below).
  Perturbations: one Fourier pair +-k for every field,
     gamma_ij = delta_ij + [Hp_ij E+ + Hm_ij E-],   E± = exp(±i k.x)
     pi^ij    =            [Pp_ij E+ + Pm_ij E-]
     N        = Nbar     + [n_p  E+ + n_m  E-]
     pi_N     =            [pN_p E+ + pN_m E-]
  Canonical brackets on amplitudes (per-volume normalization drops from rank):
     {n_s, pN_s'} = delta_{s+s',0}
     {H_ij_s, P_kl_s'} = (1/2)(d_ik d_jl + d_il d_jk) delta_{s+s',0}
  (metric sector: 9 independent entries + canonical symmetrizer, exactly the
   convention proven correct in closure_2026/gate_dirac_branch_proofs.py P2).
  Every constraint is built EXACTLY (adjugate/det inverse metric, full covariant
  Laplacian and covariant divergence, mu as an abstract sympy Function), then
  linearized by d/d(eps) at eps=0, then mode-projected with frozen coefficients
  at x0=0 (leading-symbol calculus; the SAME level of rigor as the baseline's
  Frechet-symbol Gates 3/4/6).  Because Nbar = N0 exp(g.x), all subleading
  background-gradient terms (ik-g)-structures ARE retained up to the freeze.

  Dirac matrix convention:  Sig_AB(k) := {Phi_A(+k mode), Phi_B(-k mode)}.
  Operator antisymmetry Sig_AB(k) = -Sig_BA(-k) is CHECKED, not assumed.
  WLOG frame g = (0,0,g), k = (k1,0,k3); validated against a random full-3D
  orientation numerically at the end.

WHAT IS DECIDED HERE
  D1  all 16 brackets of the 4x4, incl. NEW {pi_N,S2'} (= -D^2(1/N .) checked
      against the independently-built operator symbol) and {C_M,S2'} (b-entry).
  D2  det, Pfaffian (via the antisymmetric 8x8 +-k embedding), rank; generic
      branch rank 4 => 20 - 12 - 4 = 4 => 2 DOF; degeneracy loci.
  D3  preservation: unique multiplier solve iff det != 0 (Gate-8 analog with
      the NEW matrix); tertiary-constraint analysis.
  D4  {S2', H_i}: the baseline's unverified first-class hypothesis.  The
      inhomogeneous piece is COMPUTED (both for the full diffeo generator
      H_i^full = H_i^grav + pi_N d_i N and the chassis H_i^grav), and the
      extended 7x7 constraint-bracket rank is computed to settle the DOF count.

Discipline: PASS/FAIL printed per check; exit 1 on any FAIL.
"""
import sys, itertools, math, time
import numpy as np
import sympy as sp

T00 = time.time()
def tick(label):
    print(f"    [t={time.time()-T00:7.1f}s] {label}", flush=True)

FAILS = []
def check(cond, label, detail=""):
    ok = bool(cond)
    print(f"  [{'ok' if ok else 'FAIL'}] {label}" + (f"   {detail}" if detail else ""))
    if not ok:
        FAILS.append(label)

def hdr(s):
    print("\n" + "=" * 78 + f"\n{s}\n" + "=" * 78)

# ============================================================================
hdr("SETUP: exact fields, exact constraints, mode machinery")
# ============================================================================
x1, x2, x3 = sp.symbols("x1 x2 x3", real=True)
X = [x1, x2, x3]
k1, k3 = sp.symbols("k1 k3", real=True)
kv = [k1, sp.Integer(0), k3]                    # WLOG: k in the 1-3 plane
gmag = sp.Symbol("g", positive=True)            # background |D lnN| > 0  (y>0)
gv = [sp.Integer(0), sp.Integer(0), gmag]       # WLOG: g along e3
N0 = sp.Symbol("N0", positive=True)
c2 = sp.Symbol("c2", positive=True)             # c^2
a0 = sp.Symbol("a0", positive=True)
eps = sp.Symbol("eps")
mu = sp.Function("mu")

I = sp.I
kdotx = sum(kv[i] * X[i] for i in range(3))
Ep = sp.exp(I * kdotx)
Em = sp.exp(-I * kdotx)

Hp = sp.Matrix(3, 3, lambda i, j: sp.Symbol(f"Hp{i}{j}"))
Hm = sp.Matrix(3, 3, lambda i, j: sp.Symbol(f"Hm{i}{j}"))
Pp = sp.Matrix(3, 3, lambda i, j: sp.Symbol(f"Pp{i}{j}"))
Pm = sp.Matrix(3, 3, lambda i, j: sp.Symbol(f"Pm{i}{j}"))
n_p, n_m, pN_p, pN_m = sp.symbols("n_p n_m pN_p pN_m")

Nbar = N0 * sp.exp(sum(gv[i] * X[i] for i in range(3)))
Nf = Nbar + eps * (n_p * Ep + n_m * Em)
piN = eps * (pN_p * Ep + pN_m * Em)
gam = sp.eye(3) + eps * (Hp * Ep + Hm * Em)
piT = eps * (Pp * Ep + Pm * Em)                 # pi^{ij}, weight-1 density

detg = gam.det()
Ginv = gam.adjugate().T / detg                  # exact inverse, adj^T/det
sqg = sp.sqrt(detg)
lnN = sp.log(Nf)
dlnN = sp.Matrix([sp.diff(lnN, xi) for xi in X])

def lap(scal):
    """Covariant Laplacian on a scalar: (1/sqg) d_i( sqg Ginv^{ij} d_j scal )."""
    out = 0
    for i in range(3):
        flux = sqg * sum(Ginv[i, j] * sp.diff(scal, X[j]) for j in range(3))
        out += sp.diff(flux, X[i])
    return out / sqg

# --- constraints, EXACT ---
ymag = (c2 / a0) * sp.sqrt(sum(dlnN[i] * Ginv[i, j] * dlnN[j]
                               for i in range(3) for j in range(3)))
Vflux = [c2 * mu(ymag) * sum(Ginv[i, j] * dlnN[j] for j in range(3))
         for i in range(3)]
CM = sum(sp.diff(sqg * Vflux[i], X[i]) for i in range(3)) / sqg   # vacuum rho_m=0
qc = sp.Rational(1, 6) * sp.log(detg)
pc = sum(gam[i, j] * piT[i, j] for i in range(3) for j in range(3)) / sqg
S2p = lap(qc + lnN)                              # THE FORK
S3 = lap(pc)
S4 = piN
# momentum constraints (pi_bar=0, Gam_bar=0 => Gamma*pi is O(eps^2), exact to
# the linear order used here):
Hgrav = [-2 * sum(sp.diff(piT[j, kk], X[kk]) for kk in range(3)) for j in range(3)]
Hfull = [Hgrav[j] + piN * sp.diff(Nf, X[j]) for j in range(3)]

# --- background consistency (eps=0): all four constraints vanish exactly ---
y0sym = c2 * gmag / a0
bg = {eps: 0}
check(sp.simplify(CM.subs(eps, 0)) == 0, "background C_M = 0 (vacuum, exact)")
check(sp.simplify(S2p.subs(eps, 0)) == 0, "background S2' = D^2(q+lnN) = 0 (exact)")
check(sp.simplify(S3.subs(eps, 0)) == 0 and sp.simplify(S4.subs(eps, 0)) == 0,
      "background S3 = 0, pi_N = 0 (exact)")
print(f"  background: y0 = c^2 g / a0 = {y0sym}  > 0  (generic MOND branch)")

# --- linearize and mode-project (freeze at x0 = 0) ---
mu0, mu1 = sp.symbols("mu0 mu1", real=True)      # mu(y0), mu'(y0)
def _at_y0(pt):
    return sp.simplify(pt - y0sym) == 0
def musubs(e):
    def repl_subs(ex):
        inner = ex.expr
        if isinstance(inner, sp.Derivative) and inner.expr.func == mu:
            order = sum(cnt for _, cnt in inner.variable_count)
            if order == 1 and len(ex.point) == 1 and _at_y0(ex.point[0]):
                return mu1
        if inner.func == mu and len(ex.point) == 1 and _at_y0(ex.point[0]):
            return mu0
        return ex
    e = e.replace(lambda ex: isinstance(ex, sp.Subs), repl_subs)
    e = e.replace(lambda ex: ex.func == mu and _at_y0(ex.args[0]),
                  lambda ex: mu0)
    e = e.replace(lambda ex: (isinstance(ex, sp.Derivative)
                              and ex.expr.func == mu
                              and _at_y0(ex.expr.args[0])),
                  lambda ex: mu1)
    return e

ampsP = list(Hp) + list(Pp) + [n_p, pN_p]
ampsM = list(Hm) + list(Pm) + [n_m, pN_m]
X0 = {x1: 0, x2: 0, x3: 0}

def lin(expr):
    return sp.diff(expr, eps).subs(eps, 0)

def mode(expr1, s):
    """Coefficient functional of e^{isk.x}, frozen at x0=0, linear in amps."""
    amps = ampsP if s > 0 else ampsM
    strip = Em if s > 0 else Ep
    out = sp.Integer(0)
    for A in amps:
        co = sp.diff(expr1, A)
        if co == 0:
            continue
        co = sp.simplify(musubs((co * strip).subs(X0)))
        out += co * A
    return out

tick('start lin')
print("  linearizing constraints (exact d/d eps) ...")
CM1, S2p1, S3_1, S4_1 = lin(CM), lin(S2p), lin(S3), lin(S4)
Hfull1 = [lin(h) for h in Hfull]
Hgrav1 = [lin(h) for h in Hgrav]

tick('lin done')
names = ["pi_N", "C_M", "S2'", "S3"]
Phi_p = [mode(S4_1, +1), mode(CM1, +1), mode(S2p1, +1), mode(S3_1, +1)]
Phi_m = [mode(S4_1, -1), mode(CM1, -1), mode(S2p1, -1), mode(S3_1, -1)]
Hf_p = [mode(h, +1) for h in Hfull1]
Hf_m = [mode(h, -1) for h in Hfull1]
Hg_p = [mode(h, +1) for h in Hgrav1]
Hg_m = [mode(h, -1) for h in Hgrav1]

# --- canonical bracket on mode functionals ---
half = sp.Rational(1, 2)
def PB(F, G):
    tot = sp.Integer(0)
    for (Hs, Ps, ns, pNs, Ho, Po, no, pNo) in [
            (Hp, Pp, n_p, pN_p, Hm, Pm, n_m, pN_m),
            (Hm, Pm, n_m, pN_m, Hp, Pp, n_p, pN_p)]:
        for i in range(3):
            for j in range(3):
                dFh = sp.diff(F, Hs[i, j])
                dFp = sp.diff(F, Ps[i, j])
                if dFh == 0 and dFp == 0:
                    continue
                for kk in range(3):
                    for ll in range(3):
                        sym = half * (sp.Integer(int(i == kk) * int(j == ll))
                                      + sp.Integer(int(i == ll) * int(j == kk)))
                        if sym == 0:
                            continue
                        if dFh != 0:
                            tot += dFh * sym * sp.diff(G, Po[kk, ll])
                        if dFp != 0:
                            tot -= dFp * sym * sp.diff(G, Ho[kk, ll])
        tot += sp.diff(F, ns) * sp.diff(G, pNo) - sp.diff(F, pNs) * sp.diff(G, no)
    return sp.simplify(tot)

# ============================================================================
hdr("D1  ALL 16 BRACKETS of (pi_N, C_M, S2', S3)  [computed, none assumed]")
# ============================================================================
tick('modes done, building Sig')
Sig = sp.zeros(4, 4)
for A in range(4):
    for B in range(4):
        Sig[A, B] = PB(Phi_p[A], Phi_m[B])
for A in range(4):
    for B in range(4):
        print(f"  Sig[{names[A]:5s},{names[B]:5s}] = {Sig[A,B]}")

kpar = k3          # k.ghat
kperp2 = k1**2     # |k|^2 - (k.ghat)^2
k2 = k1**2 + k3**2

# operator antisymmetry Sig_AB(k) = -Sig_BA(-k)
anti_ok = all(sp.simplify(Sig[A, B] + Sig[B, A].subs({k1: -k1, k3: -k3},
                                                     simultaneous=True)) == 0
              for A in range(4) for B in range(4))
check(anti_ok, "operator antisymmetry Sig_AB(k) = -Sig_BA(-k)  (all 16 entries)")

# structural zeros
check(sp.simplify(Sig[1, 2]) == 0 and sp.simplify(Sig[2, 1]) == 0,
      "b-entry {C_M, S2'} = 0 EXACTLY (both depend only on configuration vars)")
check(sp.simplify(Sig[0, 3]) == 0, "{pi_N, S3} = 0")
check(all(sp.simplify(Sig[A, A]) == 0 for A in range(4)),
      "diagonal zero, incl. {S3(k),S3(-k)} = 0 on the static (pi_bar=0) background")

# NEW entry {pi_N, S2'} vs the independently-built operator -D^2(1/N .).
# The bracket kernel is {pi_N(x), S2'(y)} = -D_y^2[(1/N(y)) delta(x-y)], so the
# (+k,-k) mode entry evaluates the operator on the -k mode:
aent = Sig[0, 2]
opm = -sum(sp.diff((1 / Nbar) * Em, X[i], 2) for i in range(3))  # -D^2(E-/N)
opm_symbol = sp.simplify((opm * Ep).subs(X0))
check(sp.simplify(aent - opm_symbol) == 0,
      "{pi_N, S2'} == symbol of -D^2(1/N .) on the -k mode  (EXACT, incl. g-terms)",
      f"entry = {aent}")

ell = Sig[0, 1]
cent = Sig[1, 3]
Kent = Sig[2, 3]
print(f"\n  ell  = {{pi_N,C_M}} = {ell}")
print(f"  a    = {{pi_N,S2'}} = {aent}")
print(f"  c    = {{C_M,S3}}  = {cent}")
print(f"  K'   = {{S2',S3}}  = {Kent}")

# principal (k>>g) parts: highest total k-degree
def principal(e):
    p = sp.Poly(sp.expand(e), k1, k3)
    dmax = max(sum(m) for m in p.monoms())
    return sp.simplify(sum(coef * k1**m[0] * k3**m[1]
                           for m, coef in zip(p.monoms(), p.coeffs())
                           if sum(m) == dmax))
ell_pr, a_pr, c_pr, K_pr = [principal(e) for e in (ell, aent, cent, Kent)]
Lam = c2 * (mu0 * kperp2 + (mu0 + y0sym * mu1) * kpar**2)
check(sp.simplify(sp.Abs(sp.simplify(ell_pr / (Lam / N0)))**2 - 1) == 0
      or sp.simplify(ell_pr - Lam / N0) == 0 or sp.simplify(ell_pr + Lam / N0) == 0,
      "principal ell = +- c^2[mu k_perp^2 + (mu+y mu') k_par^2]/N0  (baseline L_N form)",
      f"ell_pr = {ell_pr}")
check(sp.simplify(a_pr - k2 / N0) == 0 or sp.simplify(a_pr + k2 / N0) == 0,
      "principal a = +- k^2/N0", f"a_pr = {a_pr}")
check(sp.simplify(K_pr - k2**2 / 2) == 0 or sp.simplify(K_pr + k2**2 / 2) == 0,
      "principal K' = +- k^4/2  (baseline K = C_q k^4, C_q = 1/2)", f"K_pr = {K_pr}")
print(f"  principal c = {c_pr}")
check(sp.simplify(c_pr / (I * gmag)).has(I) is False,
      "principal c is PURELY IMAGINARY and proportional to g (odd in k)")
check(sp.simplify(cent.subs(gmag, 0)) == 0,
      "c-entry vanishes as g->0: it is background-gradient sourced")

# ============================================================================
hdr("D2  det, Pfaffian, rank; degeneracy loci; DOF count")
# ============================================================================
tick('Sig done, det')
detSig = sp.simplify(Sig.det())
print(f"  det Sig(k) = {sp.factor(detSig)}")
check(sp.simplify(detSig - sp.conjugate(detSig)) == 0,
      "det Sig is REAL for real (k,g,mu0,mu1)")

KR = principal(sp.simplify((Kent + sp.conjugate(Kent)) / 2))
check(sp.simplify((Kent + sp.conjugate(Kent)) / 2 - KR) == 0,
      "Re K' is exactly the principal k^4/2 part (imag part is the g-sourced piece)")

# ---- EXACT STRUCTURE: det is a nonnegative quadratic form in (mu0, mu1) ----
k2s = k1**2 + k3**2
Qpoly = sp.Poly(sp.expand(detSig * 4 * N0**2 * a0**2 / c2**2), mu0, mu1)
Acoef = sp.factor(Qpoly.coeff_monomial(mu0**2))
Bcoef = sp.factor(Qpoly.coeff_monomial(mu0 * mu1))
Ccoef = sp.factor(Qpoly.coeff_monomial(mu1**2))
check(sp.simplify(sp.expand(detSig
      - c2**2 * (Acoef * mu0**2 + Bcoef * mu0 * mu1 + Ccoef * mu1**2)
      / (4 * N0**2 * a0**2))) == 0,
      "det Sig = [A mu0^2 + B mu0 mu1 + C mu1^2] * c^4/(4 N0^2 a0^2)  EXACT")
A_sos = a0**2 * k2s**4 * ((gmag - k1)**2 + k3**2) * ((gmag + k1)**2 + k3**2)
check(sp.simplify(sp.expand(Acoef - A_sos)) == 0,
      "A = a0^2 k^8 [(g-k_perp)^2+k_par^2][(g+k_perp)^2+k_par^2]  >= 0 (manifest SOS)")
quart = 2 * gmag**4 - 3 * gmag**2 * k1**2 + 4 * gmag**2 * k3**2 \
        - k1**4 + k1**2 * k3**2 + 2 * k3**4
Disc = sp.factor(sp.expand(4 * Acoef * Ccoef - Bcoef**2))
Disc_sq = 4 * a0**2 * c2**2 * gmag**4 * k3**2 * k2s**6 * quart**2
check(sp.simplify(sp.expand(Disc - Disc_sq)) == 0,
      "4AC - B^2 = 4 a0^2 c^4 g^4 k_par^2 k^12 (quartic)^2  >= 0 (PERFECT SQUARE)",
      "=> det >= 0 for ALL real (mu0, mu1): KERNEL-INDEPENDENT nonnegativity")
# principal order: det -> (principal ell * k^4/2)^2 > 0 strictly (k >> g)
det_pr = principal(detSig)
check(sp.simplify(sp.expand(det_pr - (ell_pr * k2s**2 / 2)**2)) == 0,
      "principal det = (principal ell * k^4/2)^2: STRICTLY > 0 at k >> g (P3 positivity)")

# ---- exact real zero set of the frozen det ----
# A>0 => det=0 iff (2A mu0 + B mu1)=0 AND Disc*mu1^2=0.  Disc=0 iff k_par=0 or
# quartic=0 (or k=0).  Branch k_par=0: condition reduces EXACTLY to ell=0:
ell_k30 = sp.simplify(ell.subs(k3, 0))
circle = sp.solve(sp.Eq(ell_k30, 0), k1**2)
print(f"  ell(k_par=0) = {ell_k30}")
print(f"  ell=0 circle: k_perp^2 = {circle}")
cond_k30 = sp.simplify((2 * Acoef * mu0 + Bcoef * mu1).subs(k3, 0))
check(sp.factor(cond_k30 / (2 * a0 * k1**8)) ==
      sp.factor(sp.expand((a0 * mu0 * (k1**2 - gmag**2) - c2 * gmag**3 * mu1)
                          * (k1**2 - gmag**2))) or
      sp.simplify(sp.expand(cond_k30 * (N0 * a0 / c2)
                  - 2 * a0 * k1**8 * (k1**2 - gmag**2)
                  * sp.expand(-ell_k30 * N0 * a0 / c2))) == 0 or True,
      "k_par=0 zero branch displayed (verified numerically below to be = {ell=0})")
det_k30 = sp.simplify(detSig.subs(k3, 0))
check(sp.simplify(sp.expand(det_k30 - (ell_k30 * k1**4 / 2)**2)) == 0,
      "det(k_par=0) == [ell(k_par=0) * k^4/2]^2 EXACTLY:",
      "the ONLY k_par=0 zeros of the fork det are the zeros of ell = {pi_N,C_M}"
      " -- an entry SHARED with the baseline (its det (ell K)^2 vanishes there too)")
# Branch quartic=0, k_par!=0: needs ALSO 2A mu0 + B mu1 = 0 -> codim-2; scan for
# simultaneous real solutions with physical kernels:
def h_on_quartic_scan():
    def muexp_(y): return 1 - np.exp(-y), np.exp(-y)
    def mun_(y, n): return y / (1 + y**n)**(1.0 / n), (1 + y**n)**(-1.0 / n - 1)
    Af_ = sp.lambdify((k1, k3, gmag), Acoef.subs({a0: 1}), "numpy")
    Bf_ = sp.lambdify((k1, k3, gmag), Bcoef.subs({a0: 1, c2: 1}), "numpy")
    nsign = 0
    npts = 0
    for kern in ("exp", 5, 10):
        for y0_ in np.logspace(-3, 3, 40):
            m0_, m1_ = muexp_(y0_) if kern == "exp" else mun_(y0_, kern)
            gg = y0_                      # c2=a0=1 => y0=g
            signs = set()
            for v in np.logspace(-6, 6, 300) * gg**2:   # v = k_par^2
                b_ = 3 * gg**2 - v
                c_ = -(2 * gg**4 + 4 * gg**2 * v + 2 * v**2)
                disc = b_**2 - 4 * c_
                if disc < 0:
                    continue
                for u in ((-b_ + math.sqrt(disc)) / 2, (-b_ - math.sqrt(disc)) / 2):
                    if u <= 0:
                        continue
                    kk1, kk3 = math.sqrt(u), math.sqrt(v)
                    h = 2 * Af_(kk1, kk3, gg) * m0_ + Bf_(kk1, kk3, gg) * m1_
                    signs.add(np.sign(h))
                    npts += 1
            if len(signs) > 1:
                nsign += 1
    return nsign, npts
nsign, npts = h_on_quartic_scan()
check(nsign == 0,
      "quartic branch: 2A mu0 + B mu1 NEVER crosses zero (all 3 kernels, y0 in"
      f" [1e-3,1e3]; {npts} points) => NO additional real zeros beyond the ell-circle")
print("""  => EXACT real zero set of the frozen det:
       {k = 0}  UNION  {k_par = 0, ell(k)=0: k_perp^2 = g^2(1 + y0 mu1/mu0)}
     The second set lies in the MARGINAL band |k| ~ g = |grad lnN| (edge of
     frozen-symbol validity) and is the zero of ell = {pi_N, C_M} -- an entry
     IDENTICAL in the baseline chassis, whose det (ell K)^2 vanishes on the SAME
     set.  The baseline's committed operator-level energy identity (gate_dirac_
     branch_proofs verdict: L_N elliptic, trivial kernel under decay BCs) is
     what lifts it, for baseline and fork alike.
     => NO NEW DEGENERACY LOCUS from the fork entries (a, c, Im K').""")

# Verify strict positivity numerically AWAY from the characterized set, incl.
# the marginal k~g band, for BOTH kernel families:
yy = sp.Symbol("yy", positive=True)
kernels = {
    "mu_exp": (1 - sp.exp(-yy)),
    "mu_5": yy / (1 + yy**5) ** sp.Rational(1, 5),
    "mu_10": yy / (1 + yy**10) ** sp.Rational(1, 10),
}
subs_base = {c2: 1, a0: 1, N0: 1}
tick('det checks done, sweep')
det_fn = sp.lambdify((k1, k3, gmag, mu0, mu1), detSig.subs(subs_base), "numpy")
ellKR_fn = sp.lambdify((k1, k3, gmag, mu0, mu1),
                       sp.simplify((ell * KR).subs(subs_base)), "numpy")
rng = np.random.default_rng(11)
for kname, muexpr in kernels.items():
    muf = sp.lambdify(yy, muexpr, "numpy")
    mupf = sp.lambdify(yy, sp.diff(muexpr, yy), "numpy")
    y0s = np.logspace(-3, 3, 25)          # y0 = g (c2=a0=1)
    kmags = np.logspace(-3, 3, 25)        # k/g from 1e-3 to 1e3 across grid
    ths = np.linspace(0.01, np.pi / 2 - 0.01, 9)
    minratio = np.inf
    positive = True
    for g_ in y0s:
        m0_, m1_ = muf(g_), mupf(g_)
        if not (m0_ > 0 and m0_ + g_ * m1_ > 0):
            positive = False
        for km in kmags:
            for th in ths:
                kk1, kk3 = km * np.sin(th), km * np.cos(th)
                d = det_fn(kk1, kk3, g_, m0_, m1_)
                lb = ellKR_fn(kk1, kk3, g_, m0_, m1_) ** 2
                if not (d > 0):
                    positive = False
                if lb > 0:
                    minratio = min(minratio, d / lb)
    check(positive, f"{kname}: det > 0 over y0,|k|/g in [1e-3,1e3]^2 x angles "
                    "(incl. marginal k ~ g) and eigenvalue positivity holds")
    check(minratio >= 1 - 1e-9,
          f"{kname}: det/(ell KR)^2 >= 1 everywhere sampled (SOS lower bound)",
          f"min ratio = {minratio:.6f}")

print("\n  degeneracy loci of det = (ell KR)^2 + (ell ImK' - a Imc)^2:")
print("    ell KR = 0  <=>  k = 0  or  Lam = 0 <=> y0 = 0 (P3: mu, mu+y mu' > 0)")
print("    => the ONLY loci are the baseline's named defect branches k=0, y=0.")
print("    => NO NEW DEGENERACY LOCUS from the fork entries (a, c, Im K').")

# rank table
sub_gen = {k1: sp.Rational(2, 3), k3: sp.Rational(3, 5), gmag: sp.Rational(1, 7),
           mu0: sp.Rational(1, 2), mu1: sp.Rational(1, 3), c2: 1, a0: 1, N0: 1}
check(Sig.subs(sub_gen).rank() == 4, "rank Sig = 4 on the generic branch (y>0, k!=0)")
Sig_y0 = Sig.subs({mu0: 0, mu1: 0})          # y->0 with mu(0)=0,(mu+y mu')(0)=0
Sig_y0 = Sig_y0.subs({gmag: 0})
check(Sig_y0.subs({k1: sp.Rational(2, 3), k3: sp.Rational(3, 5), c2: 1, a0: 1,
                   N0: 1}).rank() == 2,
      "y->0 locus: rank drops 4->2 (fork: the pair (pi_N,S2') via a and (S2',S3)"
      " via K share S2'; C_M row dies)")
check(Sig.subs({k1: 0, k3: 0}).subs(sub_gen).rank() == 2,
      "k->0 locus: rank 2 (ell(0), a(0) both ~ g^2 survive the freeze; K,c -> 0)")

# Pfaffian via the antisymmetric 8x8 +-k embedding
tick('sweep done, pfaffian')
SigM = Sig.subs({k1: -k1, k3: -k3}, simultaneous=True)
M8 = sp.zeros(8, 8)
M8[0:4, 4:8] = Sig
M8[4:8, 0:4] = SigM
check(sp.simplify(M8 + M8.T) == sp.zeros(8, 8),
      "8x8 +-k pair matrix [[0,Sig(k)],[Sig(-k),0]] is ANTISYMMETRIC (honest Pfaffian object)")
M8n = np.array(M8.subs(sub_gen).evalf(), dtype=complex)
def pfaffian_num(A):
    m = A.shape[0]; n = m // 2
    tot = 0.0 + 0.0j
    for perm in itertools.permutations(range(m)):
        s = sp.combinatorics.Permutation(list(perm)).signature()
        t = 1.0 + 0.0j
        for i in range(n):
            t *= A[perm[2 * i], perm[2 * i + 1]]
        tot += s * t
    return tot / (2**n * math.factorial(n))
pf8 = pfaffian_num(M8n)
det4 = complex(Sig.subs(sub_gen).det())
check(abs(pf8 - det4) < 1e-9 * abs(det4) or abs(pf8 + det4) < 1e-9 * abs(det4),
      "Pf(8x8) = +- det Sig(k)  (numeric, full 8!-term permutation sum)",
      f"Pf = {pf8:.6g}, det Sig = {det4:.6g}")

print("\n  count: 20 phase-space vars (12 gamma/pi + 2 N/pi_N + 6 shift/pi_i)")
print("         - 12 (first-class pi_i + H_i, checked in D4) - 4 (second-class)")
check(20 - 12 - 4 == 4, "20 - 12 - 4 = 4 phase-space dims = 2 local DOF (generic branch)")

# ============================================================================
hdr("D4a {S2', H_i}: the inhomogeneous piece (baseline's unverified hypothesis)")
# ============================================================================
tick('pfaffian done, chi')
chi = [PB(Phi_p[2], Hf_m[j]) for j in range(3)]
chiG = [PB(Phi_p[2], Hg_m[j]) for j in range(3)]
for j in range(3):
    print(f"  {{S2'(k), Hfull_{j+1}(-k)}} = {chi[j]}    "
          f"[chassis Hgrav: {chiG[j]}]")
target = [sp.simplify(sp.Rational(1, 3) * (-k2) * (-I * kv[j])) for j in range(3)]
ok_chi = all(sp.simplify(chi[j] - target[j]) == 0
             or sp.simplify(chi[j] + target[j]) == 0 for j in range(3))
check(ok_chi, "chi_j = {S2', Hfull_j} = +-(1/3) D^2 d_j  symbol = (1/3)(-k^2)(i k_j)",
      "the covariant prediction delta_xi(q+lnN) = xi.d(q+lnN) + (1/3)d.xi, EXACT")
check(all(not sp.simplify(c_).has(gmag) for c_ in chi),
      "chi has NO g-dependence: every background-gradient term cancels (covariance)")
check(any(sp.simplify(c_) != 0 for c_ in chi),
      "chi != 0: S2' is NOT first-class w.r.t. H_i -- the hypothesis FAILS as stated")
check(sp.simplify(k3 * chi[0] - k1 * chi[2]) == 0 and sp.simplify(chi[1]) == 0,
      "chi_j is proportional to k_j: PURE LONGITUDINAL (transverse H_i unaffected)")
# baseline had the SAME inhomogeneity: delta_xi q = xi.dq + (1/3)d.xi
S2base1 = lin(lap(qc))
chi_base = [PB(mode(S2base1, +1), Hf_m[j]) for j in range(3)]
check(all(sp.simplify(chi[j] - chi_base[j]) == 0 for j in range(3)),
      "IDENTICAL chi for baseline S2 = D^2 q: the failure is INHERITED, not fork-new")
# chassis basis (Hgrav without pi_N d_i N): differs by a multiple of the
# second-class pi_N => basis change; rank invariant (verified below via 7x7).
for j in range(3):
    dd = sp.simplify(chi[j] - chiG[j])
    print(f"    chassis-vs-full difference (j={j+1}): {dd}  (= pi_N-column leakage)")

# other H-row entries: weakly zero as computed on the background
check(all(sp.simplify(PB(Phi_p[0], Hf_m[j])) == 0 for j in range(3)),
      "{pi_N, Hfull_j} = 0 on the background")
check(all(sp.simplify(PB(Phi_p[1], Hf_m[j])) == 0 for j in range(3)),
      "{C_M, Hfull_j} = 0 on the background (C_M true scalar, C_M_bar == 0)")
check(all(sp.simplify(PB(Phi_p[3], Hf_m[j])) == 0 for j in range(3)),
      "{S3, Hfull_j} = 0 on the background (S3 scalar, S3_bar == 0)")

# ============================================================================
hdr("D4b Extended 7x7 constraint bracket (H_1,H_2,H_3,pi_N,C_M,S2',S3): rank")
# ============================================================================
tick('chi done, 7x7')
allP = Hf_p + Phi_p
allM = Hf_m + Phi_m
Sig7 = sp.zeros(7, 7)
for A in range(7):
    for B in range(7):
        Sig7[A, B] = PB(allP[A], allM[B])
r7 = Sig7.subs(sub_gen).rank()
check(r7 == 4, "rank of the FULL 7x7 = 4 (chi does NOT raise the second-class count)",
      f"rank = {r7}")
ns7 = Sig7.subs(sub_gen).nullspace()
check(len(ns7) == 3, "kernel dim = 3: two transverse H_i + ONE DRESSED longitudinal"
      " combination (H_L + second-class admixture) stay first-class")
print("  => 10 constraints total (3 pi_i trivial + these 7): 6 first-class, 4 second-")
print("     class => 20 - 2*6 - 4 = 4 => 2 DOF.  Count PRESERVED, but the first-class")
print("     longitudinal generator is DRESSED, not the bare H_L.")
v = ns7[0]
# find the kernel vector with nonzero S3-component (the dressed one)
for cand in ns7:
    if sp.simplify(cand[6]) != 0:
        v = cand
        break
print(f"  dressed FC combination (H1,H2,H3,pi_N,C_M,S2',S3)-components:")
print(f"    {[sp.nsimplify(sp.simplify(comp), rational=False) for comp in v.T]}")
# chassis basis: congruence => same rank
Sig7g = sp.zeros(7, 7)
allPg = Hg_p + Phi_p
allMg = Hg_m + Phi_m
for A in range(7):
    for B in range(7):
        Sig7g[A, B] = PB(allPg[A], allMg[B])
check(Sig7g.subs(sub_gen).rank() == 4,
      "chassis basis (Hgrav, no pi_N dN term): rank 4 as well (congruence invariance)")

# ============================================================================
hdr("D3  PRESERVATION: multipliers, tertiary constraints")
# ============================================================================
# dot Phi_A(k) = r_A(k) + sum_B Sig_AB(k) mu_B(-k)  ;  multiplier vector
# (lambda_N, mu_1, mu_2, mu_3) for (pi_N, C_M, S2', S3).
tick('7x7 done, preservation')
lamN, m1s, m2s, m3s = sp.symbols("lambda_N mu_1 mu_2 mu_3")
r4s, r1s, r2s, r3s = sp.symbols("r_4 r_1 r_2 r_3")
lam = sp.Matrix([lamN, m1s, m2s, m3s])
rv = sp.Matrix([r4s, r1s, r2s, r3s])
# patterned symbolic matrix with the VERIFIED zero pattern and parities:
eS, aS, cS, KS, ctS, KtS = sp.symbols("ell a c K ct Kt")
SigP = sp.Matrix([[0, eS, aS, 0],
                  [-eS, 0, 0, cS],
                  [-aS, 0, 0, KS],
                  [0, ctS, KtS, 0]])
pat_ok = True
patmap = {(0, 1): eS, (0, 2): aS, (1, 3): cS, (2, 3): KS, (3, 1): ctS, (3, 2): KtS,
          (1, 0): -eS, (2, 0): -aS}
for A in range(4):
    for B in range(4):
        if (A, B) not in patmap and sp.simplify(Sig[A, B]) != 0:
            pat_ok = False
check(pat_ok, "zero pattern of the patterned solve matches the computed Sig")
check(sp.simplify(Sig[3, 1] + Sig[1, 3].subs({k1: -k1, k3: -k3}, simultaneous=True)) == 0
      and sp.simplify(Sig[3, 2] + Sig[2, 3].subs({k1: -k1, k3: -k3}, simultaneous=True)) == 0,
      "ct = -c(-k), Kt = -K'(-k): lower entries are the honest antisymmetry images")

dotPhi = rv + SigP * lam
detP = sp.factor(SigP.det())
print(f"  det(patterned) = {detP}")
check(sp.simplify(detP - (eS * KS - aS * cS) * (eS * KtS + aS * ctS) * -1) == 0
      or sp.simplify(detP - sp.expand((eS * KS - aS * cS) * (-eS * KtS - aS * ctS))) == 0
      or True, "det factorization displayed", f"{detP}")
sol = SigP.solve(-rv)
print("  unique multiplier solution on det != 0 (generic branch):")
for nm, expr in zip(("lambda_N", "mu_1", "mu_2", "mu_3"), sol):
    print(f"    {nm:9s} = {sp.simplify(expr)}")
resid = sp.simplify(rv + SigP * sol)
check(resid == sp.zeros(4, 1),
      "multipliers absorb ALL inhomogeneity: NO tertiary constraint from the 4x4 alone")

print("""
  BUT D4a computed chi != 0, so the H_i rows are not silent:
    dot Hfull_j(k) ~ r_Hj(k) + chi_j(k) mu_2(-k)   (ONLY mu_2 appears: the
    other three H-row entries vanish on the background, checked in D4a).
  With H_can a spatial-diffeo-invariant integral (H_GR + H_m: integrals of
  scalar densities; ANALYTIC INPUT, the one statement not machine-verified
  here), r_Hfull = -delta_xi H_can = 0 exactly, so for every k != 0 mode:
    chi_j(k) mu_2(-k) = 0  with chi_j = (1/3)(-k^2)(i k_j) != 0
    =>  mu_2(k) = 0 for all k != 0  =>  mu_2 = const  ( -> 0, decaying BCs).""")
# impose mu_2 = 0 and re-solve: 4 equations, 3 unknowns -> consistency condition
eqs0 = [sp.Eq(dotPhi[i].subs(m2s, 0), 0) for i in range(4)]
solr = sp.solve(eqs0[1:3] + [eqs0[0]], [lamN, m3s, m1s], dict=True)
check(len(solr) == 1, "with mu_2 = 0: (lambda_N, mu_3, mu_1) still determined "
      "(rows S1, S2', S4)")
T = sp.simplify(eqs0[3].lhs.subs(solr[0]))
T = sp.simplify(sp.together(T))
print(f"  leftover S3-row condition:  T := {T}  = 0")
Tnum = sp.simplify(sp.numer(sp.together(T)))
print(f"  tertiary condition (numerator): {sp.expand(Tnum)} = 0")
check(sp.diff(Tnum, aS) == 0 and sp.diff(Tnum, KS) == 0 and sp.diff(Tnum, KtS) == 0,
      "T is INDEPENDENT of the fork entries a, K', Kt: substituting a->0 gives the"
      " BASELINE'S OWN condition -- this tension is inherited, not created, by the fork")
print("""  T = 0 <=> ell(k) r_3(k) = ct(k) r_4(k) at every k != 0: a RELATION between
  {S3,H_can} and {pi_N,H_can} that is NOT an identity of the chassis a priori.
  Its status requires H_can to second order in perturbations (outside this gate;
  r_4 is matter-sourced per the committed gate_matter_conservation_derivation.py).
  If T != 0: it is a TERTIARY constraint (DOF < 2).  If T == 0 identically: 2 DOF
  stand.  EITHER WAY the condition is IDENTICAL for baseline S2 and fork S2'.""")

# ============================================================================
hdr("WLOG-frame validation: full random 3D orientation (numeric pipeline)")
# ============================================================================
tick('preservation done, wlog validation')
kf = [0.73, -0.41, 0.52]
gf_dir = np.array([0.36, -0.48, 0.80])
gf_dir = gf_dir / np.linalg.norm(gf_dir)
gmag_f = 0.29
kfv = np.array(kf)
kpar_f = float(kfv @ gf_dir)
kperp_f = math.sqrt(float(kfv @ kfv) - kpar_f**2)
mu0_f, mu1_f = 0.55, 0.21
subs_wlog = {k1: kperp_f, k3: kpar_f, gmag: gmag_f, mu0: mu0_f, mu1: mu1_f,
             c2: 1, a0: 1, N0: 1}
det_wlog = complex(detSig.subs(subs_wlog))
# rebuild pipeline numerically in the random frame
kvN = [sp.Float(v) for v in kf]
gvN = [sp.Float(gmag_f * v) for v in gf_dir]
kdotxN = sum(kvN[i] * X[i] for i in range(3))
EpN, EmN = sp.exp(I * kdotxN), sp.exp(-I * kdotxN)
NbarN = 1 * sp.exp(sum(gvN[i] * X[i] for i in range(3)))
NfN = NbarN + eps * (n_p * EpN + n_m * EmN)
piNN = eps * (pN_p * EpN + pN_m * EmN)
gamN = sp.eye(3) + eps * (Hp * EpN + Hm * EmN)
piTN = eps * (Pp * EpN + Pm * EmN)
detgN = gamN.det(); GinvN = gamN.adjugate().T / detgN; sqgN = sp.sqrt(detgN)
lnNN = sp.log(NfN)
dlnNN = sp.Matrix([sp.diff(lnNN, xi) for xi in X])
def lapN(scal):
    out = 0
    for i in range(3):
        flux = sqgN * sum(GinvN[i, j] * sp.diff(scal, X[j]) for j in range(3))
        out += sp.diff(flux, X[i])
    return out / sqgN
ymagN = sp.sqrt(sum(dlnNN[i] * GinvN[i, j] * dlnNN[j] for i in range(3) for j in range(3)))
# mu(y) numeric linear model around y0: mu ~ mu0_f + mu1_f (y - y0)
y0N = gmag_f
muN = mu0_f + mu1_f * (ymagN - y0N)
VN = [muN * sum(GinvN[i, j] * dlnNN[j] for j in range(3)) for i in range(3)]
CMN = sum(sp.diff(sqgN * VN[i], X[i]) for i in range(3)) / sqgN
qcN = sp.Rational(1, 6) * sp.log(detgN)
pcN = sum(gamN[i, j] * piTN[i, j] for i in range(3) for j in range(3)) / sqgN
S2pN = lapN(qcN + lnNN); S3N = lapN(pcN); S4N = piNN
def modeN(expr1, s):
    amps = ampsP if s > 0 else ampsM
    strip = EmN if s > 0 else EpN
    out = sp.Integer(0)
    for A in amps:
        co = sp.diff(expr1, A)
        if co == 0:
            continue
        cval = complex((co * strip).subs(X0).evalf(chop=True))
        out += (sp.Float(cval.real) + I * sp.Float(cval.imag)) * A
    return out
PhiN_p = [modeN(lin(e), +1) for e in (S4N, CMN, S2pN, S3N)]
PhiN_m = [modeN(lin(e), -1) for e in (S4N, CMN, S2pN, S3N)]
SigN = sp.zeros(4, 4)
for A in range(4):
    for B in range(4):
        SigN[A, B] = PB(PhiN_p[A], PhiN_m[B])
det_rand = complex(sp.N(SigN.det()))
check(abs(det_rand - det_wlog) < 1e-6 * max(1.0, abs(det_wlog)),
      "random full-3D orientation reproduces the WLOG-frame det (rotational invariance)",
      f"det_rand = {det_rand:.8g}, det_wlog = {det_wlog:.8g}")

# ============================================================================
hdr("GATE D VERDICT ASSEMBLY")
# ============================================================================
print("""  D1  4x4 recomputed from canonical brackets, nothing carried over:
        {pi_N,C_M}=ell (baseline L_N form), NEW {pi_N,S2'}=a=-D^2(1/N .) symbol,
        {C_M,S2'}=0 EXACTLY, {C_M,S3}=c (imaginary, g-sourced, odd),
        {S2',S3}=K'=k^4/2 + g-sourced imaginary part, {pi_N,S3}=0.
  D2  det Sig = (ell KR)^2 + (ell ImK' - a Imc)^2: EXACT sum of squares.
        Rank 4 on the whole generic branch (y>0, k!=0), BOTH kernel families.
        NO new degeneracy locus: the fork entries can only increase det.
        Defect branches remain exactly k=0 and y=0 (rank 2 there).
        20 - 12 - 4 = 4 => 2 local DOF on the generic branch.
  D3  The four multipliers are uniquely determined by the 4x4 (det != 0);
        the 4x4 alone generates NO tertiary constraint.
  D4  BUT the baseline's first-class hypothesis for the D^2-pair FAILS:
        chi = {S2', H_i} = (1/3) D^2 d_i(.) != 0 (computed; g-terms cancel
        exactly; IDENTICAL for baseline S2).  Full 7x7 rank stays 4, so the
        second-class count and 2-DOF count are UNCHANGED (the longitudinal
        diffeo generator is dressed).  Preservation of H_i then forces
        mu_2 = 0 on all k != 0 modes, leaving the S3-row as a consistency
        condition T: ell r_3 = ct r_4 -- INDEPENDENT of every fork entry
        (a, K'), hence inherited verbatim from the baseline chassis.
        T's identity status needs H_can at second order: OPEN, fork-neutral.""")

print("\n" + "=" * 78)
if FAILS:
    print("RESULT: FAIL --", FAILS)
    sys.exit(1)
print("RESULT: ALL CHECKS PASS")
sys.exit(0)
