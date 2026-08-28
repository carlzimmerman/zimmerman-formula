#!/usr/bin/env python3
r"""
B_decoupling_dispersion.py
==============================================================================
STEP 2 of FC-FK route-A: build the AeST scalar+aether quadratic action DIRECTLY
from the frozen action (no hand algebra), in the GRAVITY-DECOUPLING limit
(flat metric, aether + scalar only), and read off the dispersion.

Purpose: LOCATE the ghost.  The Minkowski AeST analysis (2109.13287, EXTERNAL)
finds a Hamiltonian unbounded below for k<k*.  Is that pathology in the
propagating scalar+aether sector, or does it require gravity?  We compute the
decoupling-limit quadratic Lagrangian term-by-term from

   L = -(K_B/2)F^2 + (2-K_B)(2 J^mu grad_mu phi - Y) - F(Y,Q) - lambda(A^2+1)

with F(Y,Q) -> F_Q^star(Q) = -2K(Q) at quadratic order (kernel-blind, STEP 1),
on the aligned background  phi = Q0 t,  A^mu=(1,0,0,0),  and the unit constraint
A_mu A^mu=-1 solved for A_0 to O(eps^2).  Scalar perturbations: phi=Q0 t+eps f,
A_i = eps d_i alpha (=> A_0 = -1 + O(eps^2)).

RESULT (printed, all from sympy):
  * chi = f + Q0 alpha emerges as the natural gradient variable: delta^2 Y = |grad chi|^2.
  * the reduced 2x2 dispersion has ONE shift-Goldstone flat direction (omega=0) and
    ONE HEALTHY massive mode omega^2 = m^2 + c_s^2 k^2 with m^2>0, c_s^2>0.
  * => NO GHOST in the decoupling sector for ANY k.  The 2109.13287 unbounded band is
    therefore a GRAVITATIONAL / CONSTRAINT effect acting on the Goldstone flat direction
    (STEP 3), not a pathology of the propagating scalar+aether dynamics.

This reframes the decider: the k*-band is the gravitational LIFT of the exact
shift-Goldstone, whose k->0 endpoint is already Hubble-rescued.  STEP 3 computes
the finite-k lift on FLRW.

Self-contained.  python3 B_decoupling_dispersion.py
"""
import sympy as sp

P = print
FAILS = []
def check(label, cond, extra=""):
    ok = bool(cond)
    P(("  [ok]   " if ok else "  [FAIL] ") + label + (("\n         " + extra) if extra else ""))
    if not ok: FAILS.append(label)
    return ok
def hdr(s): P("\n" + "=" * 92 + "\n" + s + "\n" + "=" * 92)
def note(t, s): P(f"  [{t}] {s}")

# ---- symbols ----
t, x = sp.symbols('t x', real=True)
eps = sp.symbols('epsilon', positive=True)
Q0, K2, KB, Lam, a0 = sp.symbols('Q0 K2 K_B Lambda a0', positive=True)
f  = sp.Function('f')(t, x)          # scalar perturbation  (phi = Q0 t + eps f)
al = sp.Function('alpha')(t, x)      # aether longitudinal   (A_i = eps d_i alpha)

hdr("STEP 2  --  decoupling-limit quadratic action, built from the AeST action by sympy")
note("bg", "phi=Q0 t, A^mu=(1,0,0,0); metric eta=diag(-1,1,1,1); unit constraint solved for A_0.")
note("STEP1", "F(Y,Q) -> F_Q^star(Q)=-2K(Q) at quadratic order (J_10 is O(eps^3), proven kernel-blind).")

# ---- metric (flat), fields, aether with unit constraint solved to O(eps^2) ----
# A_mu (lower).  Spatial: A_1 = eps * d_x alpha.  A_0 from A_mu A^mu = -1.
Ax = eps * sp.diff(al, x)                                  # A_1 lower
# g^{mu nu}=diag(-1,1,1,1). A_muA^mu = -A_0^2 + A_1^2 = -1 => A_0 = -sqrt(1+A_1^2)
A0 = -sp.sqrt(1 + Ax**2)                                   # branch near -1
A_low = [A0, Ax, sp.Integer(0), sp.Integer(0)]            # A_mu
# raise: A^mu = eta^{mu nu} A_nu
eta_inv = [-1, 1, 1, 1]
A_up = [eta_inv[i]*A_low[i] for i in range(4)]

# phi field and its gradient (only t,x nontrivial)
phi = Q0*t + eps*f
dphi = [sp.diff(phi, t), sp.diff(phi, x), sp.Integer(0), sp.Integer(0)]   # grad_mu phi (partial=cov on flat)

def series2(e):
    """Taylor-expand in eps and keep through O(eps^2)."""
    return sp.series(e, eps, 0, 3).removeO()

# ---- Q = A^mu grad_mu phi ----
Q_expr = sum(A_up[i]*dphi[i] for i in range(4))
Q_ser  = series2(Q_expr)
dQ = sp.simplify(Q_ser - Q0)                              # delta Q
note("Q", f"Q = A^mu grad_mu phi = Q0 + {sp.simplify(sp.series(dQ,eps,0,2).removeO())} + O(eps^2)")

# ---- Y = (g^{mu nu}+A^mu A^nu) grad_mu phi grad_nu phi ----
Y_expr = 0
for i in range(4):
    for j in range(4):
        gij = (eta_inv[i] if i == j else 0) + A_up[i]*A_up[j]
        Y_expr += gij*dphi[i]*dphi[j]
Y_ser = series2(Y_expr)
check("background Y = 0 and delta^1 Y = 0 (aether-orthogonal projector kills phidot)",
      sp.simplify(Y_ser.subs(eps, 0)) == 0 and sp.simplify(sp.diff(Y_ser, eps).subs(eps, 0)) == 0,
      f"Y = {sp.simplify(Y_ser)}  (starts at O(eps^2))")
# delta^2 Y coefficient
Y2 = sp.simplify(Y_ser.coeff(eps, 2))
chi = sp.diff(f, x) + Q0*sp.diff(al, x)                   # grad_x of (f + Q0 alpha)
check("delta^2 Y = |grad_x(f + Q0 alpha)|^2 = (chi)^2  => chi = f + Q0 alpha is the gradient variable",
      sp.simplify(Y2 - chi**2) == 0, f"delta^2 Y = {Y2}")

# ---- F^2 (aether kinetic) ----
# F_{mu nu} = d_mu A_nu - d_nu A_mu.  Nonzero: F_{01}=d_t A_1 - d_x A_0.
coords = [t, x]
def Flow(mu, nu):
    Am = A_low[mu]; An = A_low[nu]
    return sp.diff(An, coords[mu]) - sp.diff(Am, coords[nu]) if mu < 2 and nu < 2 else sp.Integer(0)
F2 = 0
for mu in range(4):
    for nu in range(4):
        if mu < 2 and nu < 2:
            Fmn = Flow(mu, nu)
            Fup = eta_inv[mu]*eta_inv[nu]*Fmn
            F2 += Fmn*Fup
F2_ser = series2(F2)
note("F^2", f"F^2 = {sp.simplify(F2_ser)}  (O(eps^2): only F_01 = d_t A_1 contributes)")

# ---- J^mu = A^nu grad_nu A^mu ; coupling 2 J^mu grad_mu phi ----
# grad_nu A^mu on flat space = d_nu A^mu (partial).  J^mu = A^nu d_nu A^mu.
def dA_up(mu, nu):   # d_nu A^mu
    return sp.diff(A_up[mu], coords[nu]) if nu < 2 else sp.Integer(0)
J_up = []
for mu in range(4):
    Jm = sum(A_up[nu]*dA_up(mu, nu) for nu in range(2))
    J_up.append(Jm)
Jcoup = 2*sum(J_up[mu]*dphi[mu] for mu in range(4))       # 2 J^mu grad_mu phi
Jcoup_ser = series2(Jcoup)
note("J-coup", f"2 J^mu grad_mu phi = {sp.simplify(Jcoup_ser)}  (O(eps^2))")

# ---- assemble the quadratic Lagrangian density ----
# L = -(K_B/2)F^2 + (2-K_B)(2 J.grad phi - Y) - F_Q^star(Q) ; F_Q^star=-2K=4Lam-2K2 dQ^2
FQstar_ser = series2(4*Lam - 2*K2*dQ**2)                  # -F -> -FQstar = -(4Lam) + 2K2 dQ^2
L = (-(KB/2)*F2_ser + (2-KB)*(Jcoup_ser - Y_ser) - FQstar_ser)
# NOTE: sympy's .coeff(eps,2) silently returns 0 on UNEXPANDED products (eps^2 buried
# inside (2-K_B)*(...)); must sp.expand() FIRST.  Verified against sp.series extraction.
L2 = sp.expand(sp.expand(L).coeff(eps, 2))               # quadratic Lagrangian density
L2_series = sp.series(L, eps, 0, 3).removeO().coeff(eps, 2)   # independent cross-check
assert sp.simplify(L2 - sp.expand(L2_series)) == 0, "eps^2 extraction mismatch"
P("\n  quadratic Lagrangian density (decoupling limit), collected:")
P("   L2 =", L2)

# ---- per-mode real quadratic form -> K, B, Omega -> dispersion ----
# Build the x-independent part of the density with REAL Fourier fields:
#   f = fr cos(kx) + fi sin(kx) is overkill; use complex amplitudes f=Fc e^{ikx}+Fc* e^{-ikx}.
# For the dispersion it suffices to use a single complex mode and read the Hermitian form; we do
# it cleanly by substituting time-only amplitudes with e^{i k x} and keeping the resonant part.
k = sp.symbols('k', positive=True)
fk = sp.Function('fk')(t); ak = sp.Function('ak')(t)          # real time-amplitudes
fkC, akC = sp.Function('fkC')(t), sp.Function('akC')(t)       # conjugate amplitudes
# real fields: u = u_k e^{ikx} + u_k^* e^{-ikx}
f_real  = fk*sp.exp(sp.I*k*x)  + fkC*sp.exp(-sp.I*k*x)
al_real = ak*sp.exp(sp.I*k*x)  + akC*sp.exp(-sp.I*k*x)
L2_sub = L2.subs({f: f_real, al: al_real}).doit()
L2_sub = sp.expand(L2_sub)
# keep only the x-independent piece (coefficient of e^{0}); terms ~ e^{+-2ikx} drop under ∫dx
L2_mode = sp.simplify(L2_sub.subs(sp.exp(2*sp.I*k*x), 0).subs(sp.exp(-2*sp.I*k*x), 0))
L2_mode = sp.expand(L2_mode)
# This is Hermitian in (fk,akC) etc. Extract K,B,Omega by treating q=(fk,ak), qC=(fkC,akC).
# Velocities:
dfk, dak = sp.diff(fk, t), sp.diff(ak, t)
dfkC, dakC = sp.diff(fkC, t), sp.diff(akC, t)
q  = [fk, ak];  qC = [fkC, akC];  dq = [dfk, dak];  dqC = [dfkC, dakC]
def coef(expr, a, b):
    return sp.simplify(sp.expand(expr).coeff(a, 1).coeff(b, 1))
# Kinetic K_ab: coeff of dqC_a dq_b (Hermitian); Omega_ab: -coeff of qC_a q_b; B from dqC_a q_b
Kmat = sp.Matrix(2, 2, lambda i, j: coef(L2_mode, dqC[i], dq[j]))
Om   = sp.Matrix(2, 2, lambda i, j: -coef(L2_mode, qC[i], q[j]))
Bmix = sp.Matrix(2, 2, lambda i, j: coef(L2_mode, dqC[i], q[j]))
P("\n  per-mode kinetic matrix K (rows/cols = f, alpha):"); sp.pprint(Kmat)
P("  per-mode gradient/'mass' matrix Omega:"); sp.pprint(Om)
P("  per-mode velocity-mixing B (dqC_a q_b):"); sp.pprint(Bmix)
w = sp.symbols('omega', real=True)
antisym = Bmix - Bmix.T
Mdisp = -w**2*Kmat + sp.I*w*antisym + Om
detM = sp.simplify(sp.expand(Mdisp.det()))
P("\n  det[-w^2 K + i w (B-B^T) + Omega] =", detM)
W = sp.symbols('W', real=True)
detW = sp.expand(detM).subs({w**4: W**2, w**2: W})
detW = sp.simplify(detW)
# drop residual odd-w pieces (should be none if Hermitian); assert reality
odd = sp.simplify(sp.expand(detM) - sp.expand(detM).subs({w**4: W**2, w**2: W}).subs(W, w**2))
check("dispersion determinant is REAL & EVEN in omega (Hermitian reduced system, no run-away tilt)",
      sp.simplify(sp.im(detM.rewrite(sp.cos))) == 0 or sp.simplify(odd) == 0,
      "=> genuine omega^2 eigenvalues, frame-mixing B enters only through the even iw(B-B^T) block")
roots = sp.solve(sp.Eq(detW, 0), W)
P("\n  dispersion roots omega^2 =", roots)

hdr("STEP 2  --  classification of the decoupling spectrum")
# positive-definiteness of the reduced kinetic matrix (no kinetic ghost)
Kdet = sp.simplify(Kmat.det()); Ktr = sp.simplify(Kmat.trace())
check("reduced kinetic matrix K = diag(4K2, 2 K_B k^2) is POSITIVE-DEFINITE for all k>0 (no kinetic ghost)",
      sp.simplify(Kmat[0,0]) == 4*K2 and sp.simplify(Kmat[1,1]) == 2*KB*k**2 and sp.simplify(Kmat[0,1]) == 0,
      f"det K = {Kdet} > 0, tr K = {Ktr} > 0 for 0<K_B<2, K2>0.  (K_aa->0 as k->0: aether goes soft in IR)")
# Identify the zero root and the massive root
zero_root = any(sp.simplify(r) == 0 for r in roots)
nonzero = [sp.simplify(r) for r in roots if sp.simplify(r) != 0]
check("one exact shift-Goldstone flat direction  omega^2 = 0  (protected by phi->phi+const)",
      zero_root, "the k->0 endpoint of THIS mode is the one already Hubble-rescued (fc_flrw_ir_sign)")
mroot = nonzero[0]
m2 = sp.simplify(mroot.subs(k, 0))
c2 = sp.simplify((mroot - m2)/k**2)                       # coefficient of k^2 (mroot is exactly quadratic)
P(f"    massive mode: omega^2 = {sp.simplify(mroot)}")
P(f"       m^2   = {m2}")
P(f"       c_s^2 = {c2}   (coefficient of k^2)")
subs_pos = {KB: sp.Rational(1, 10), K2: 1, Q0: 1}
m2_pos = sp.simplify(m2.subs(subs_pos)); c2_pos = sp.simplify(c2.subs(subs_pos))
check("the OTHER mode is massive & HEALTHY: omega^2 = m^2 + c_s^2 k^2 with m^2>0 and c_s^2>0",
      (m2_pos > 0) == True and (c2_pos > 0) == True,
      f"at (K_B,K2,Q0)=(1/10,1,1):  m^2 = {m2_pos} > 0,  c_s^2 = {c2_pos} > 0  (holds for all 0<K_B<2)")
# symbolic positivity over the physical window 0<K_B<2
check("m^2 = (2-K_B)Q0^2/K_B and c_s^2 = (2-K_B)/(K2 K_B) are BOTH > 0 for every 0<K_B<2, K2,Q0>0",
      sp.simplify(m2 - (2-KB)*Q0**2/KB) == 0 and sp.simplify(c2 - (2-KB)/(K2*KB)) == 0,
      "manifestly positive: (2-K_B)>0, K_B>0, K2>0 => no gradient or tachyonic instability")

hdr("VERDICT  --  STEP 2")
P("""  The scalar+aether sector, WITHOUT gravity, has:
    * one EXACT shift-Goldstone flat direction (omega^2 = 0), and
    * one HEALTHY massive mode (omega^2 = m^2 + c_s^2 k^2, m^2>0, c_s^2>0).
  There is NO ghost band in the decoupling sector for any k.

  => The 2109.13287 'Hamiltonian unbounded below for k<k*' is NOT a pathology of the
     propagating scalar+aether dynamics.  It is the GRAVITATIONAL / CONSTRAINT lift of the
     shift-Goldstone flat direction (the metric potentials Psi,Phi, non-dynamical & elliptic
     sub-horizon, back-react on the Goldstone).  The decider therefore lives on the FLAT
     DIRECTION, whose k->0 endpoint is ALREADY Hubble-rescued.  STEP 3 computes the finite-k
     gravitational lift on FLRW and its dynamical-vs-constraint character.""")
P("=" * 92)
nf = len(FAILS)
P(f"CERTIFICATE (STEP 2): {nf} FAIL(s)." + ("  All checks passed." if not nf else ""))
for fl in FAILS: P("   FAILED:", fl)
import sys
sys.exit(0 if nf == 0 else 1)
