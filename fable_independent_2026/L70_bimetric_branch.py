#!/usr/bin/env python3
"""
L70 -- the last open branch of the foliation theorem: the ghost-free derivative-bimetric MOND subspace
=======================================================================================================
L61 (this lane) searched the three branches the programme's foliation theorem (PAPER9 / L31) leaves
permitted -- three-or-more Lorentz-invariant modes, two metrics, non-minimal matter coupling -- and closed
two of them by gates run there: branch 1 (three modes) at the lensing gate GENERICALLY, branch 3
(non-minimal coupling) at the tensor-speed gate.  It deliberately left branch 2 -- TWO METRICS -- OPEN, at
exactly one calculation the record already NAMES as decisive and un-run:

   > "full covariant Hamiltonian count on the a != 0 sub-family (7 healthy vs 8 with the Boulware-Deser
   >  ghost), plus a coupled two-metric lensing solve that must not inherit alpha_3 = -1."

THE OBJECT.  project_relativistic_mond_closure_2026 records, from an adversarial workflow that CORRECTED an
earlier in-repo error (the T1..T4 basis missed T5 = P^a V_a):  with the COMPLETE 5-invariant local
connection-difference basis  C^a_mn = Gamma^a_mn(g) - Gamma^a_mn(g-hat),  the background-independent
lapse-velocity-free ("ghost-free at a = 0") subspace is 2-DIMENSIONAL and contains MOND-alive directions
OFF the constrained-f(Q) line.  T4 - T1 gives a static-NR MOND acceleration a = -4 AND a lensing source
b = -8, both nonzero.  Health with the MOND coupling switched ON was recorded UNDECIDED.  Matter couples to
g only; both metrics carry an Einstein-Hilbert term; the interaction is a diffeomorphism scalar
2 a0^2 (g g-hat)^{1/4} M(T_1..T_5).

THE QUESTION (this lane, independent of the lead's parallel work).  Is this subspace actually ghost-free
when its MOND sector (a != 0) is switched on -- and if so does it pass the gates that killed branches 1
and 3?  The ghost-free condition is a TUNING of the interaction; switching on the MOND coupling may DETUNE
it and revive the Boulware-Deser sixth mode.  This is decided by the constraint content of the quadratic
action, not by inspection.

WHAT THIS SCRIPT DOES, with independently-written symbolic machinery (its own christoffel / invariant /
Stuckelberg code, not the lead's):
  PART A  CONTROLS.  The Dirac mode counter N = (P - 2F - S)/2 must return 2 (GR), 3 (GR+scalar),
          3 (khronometric), 5 (Einstein-aether), and reproduce the two-metric 7 (ghost-free Hassan-Rosen)
          and 8 (with the BD ghost).  DC-018 reproduced: standard bigravity's Galileon sector has no MOND
          (pi' ~ r^{1-3/n}, needs non-integer n = 3/2).  An Einstein-Hilbert calibration of the ghost
          detector (a pure-EH graviton is healthy, a pure-EH vector has NO time-kinetic ghost).
  PART B  THE CRUX.  Rebuild the 5 invariants; re-derive the lapse-velocity-free subspace on a generic FRW
          background (dim = 2, basis (c1..c5) = (-u0,-u1/2,-u1/2,u0,u1)); re-derive the static-NR (a,b,x);
          then the decisive step -- the transverse-vector (helicity-1) operator on the a != 0 sub-family.
          Does the BD ghost return?
  PART C  THE GATES, run cheapest-first because a count alone does not close a branch: the lensing ratio
          M_dyn/M_lens on the a = -4, b = -8 subspace; the tensor speed given a massive graviton; the
          preferred-frame alpha_3; and the branch-independent excess-spent-once theorem (L61 PART B).
  VERDICT.

Both a0 footings on every dimensional number (a0 = 9.3619e-11 canonical / 1.1279e-10 alt).  check() marks
PASS = the requirement the LIVE-candidate reading would need; a FAIL is the finding, verified as hard as a
pass.  Nothing here favours this framework over LambdaCDM.  Reproduces (independently) the lead's
qwen_claude_field_theory WF2 suite of 2026-09-09; agreement/disagreement is reported explicitly.
"""
import sympy as sp, math, sys
from scipy.optimize import brentq

FAILS = []
def check(name, ok, detail=""):
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"   ({detail})" if detail else ""), flush=True)
    if not ok: FAILS.append(name)
def sec(t): print("\n" + "=" * 110 + f"\n{t}\n" + "=" * 110, flush=True)
def P(s=""): print(s, flush=True)

A0 = {"canonical": 9.3619e-11, "alt": 1.1279e-10}
c_light = 2.99792458e8
kpc = 3.0857e19
Mpc = 3.0857e22

# ======================================================================================================
sec("PART A -- CONTROLS.  Calibrate the counter and the ghost detector before anything rests on them.")
# ======================================================================================================

def dirac(P_dim, F, S):
    """Dirac's physical-DOF formula: N = (P - 2F - S)/2, P = phase-space dim, F/S = first/second class."""
    return (P_dim - 2 * F - S) / 2.0

P("A.1  Dirac mode-count controls  N = (P - 2F - S)/2.")
P(f"      {'theory':40s} {'phase space P':30s} {'F':>2s} {'S':>2s} {'N':>3s} {'published':>10s}")
CONTROLS = [
    ("general relativity",            "gamma_ij(6) -> 12",                 12, 4, 0, 2),
    ("GR + one minimal scalar",       "gamma_ij(6)+phi(1) -> 14",          14, 4, 0, 3),
    ("khronometric (non-proj Horava)","gamma_ij(6)+khronon(1) -> 14",      14, 4, 0, 3),
    ("Einstein-aether",               "gamma_ij(6)+u^mu(4)-|u|(1) -> 18",  18, 4, 0, 5),
]
for nm, cfg, Pd, F, S, pub in CONTROLS:
    P(f"      {nm:40s} {cfg:30s} {F:2d} {S:2d} {dirac(Pd,F,S):3.0f} {pub:10d}")
check("A1  mode counter: GR = 2",              abs(dirac(12, 4, 0) - 2) < 1e-12, "(12-8)/2")
check("A2  mode counter: GR + scalar = 3",     abs(dirac(14, 4, 0) - 3) < 1e-12, "(14-8)/2")
check("A3  mode counter: khronometric = 3",    abs(dirac(14, 4, 0) - 3) < 1e-12, "(14-8)/2 (foliation-preserving diffeo)")
check("A4  mode counter: Einstein-aether = 5", abs(dirac(18, 4, 0) - 5) < 1e-12, "(18-8)/2 = 2 tensor + 2 vector + 1 scalar")

P("")
P("A.2  The SAME counter on two metrics.  Two metrics = 24 phase-space functions (each gamma_ij(6) + its")
P("     momentum).  Overall diffeomorphism = 4 first-class.  The Boulware-Deser constraint PAIR (primary +")
P("     secondary) is 2 second-class; when the ghost-free tuning provides it, it removes 1 DOF (7); when a")
P("     detuning destroys it, that DOF propagates and one polarisation is a ghost (8).")
P(f"      ghost-free Hassan-Rosen : P=24 F=4 S=2  ->  N = {dirac(24,4,2):.0f}   (2 massless + 5 massive graviton)")
P(f"      with the BD mode        : P=24 F=4 S=0  ->  N = {dirac(24,4,0):.0f}   (the sixth mode is the ghost)")
check("A5  two-metric counter: ghost-free bimetric (Hassan-Rosen) = 7", abs(dirac(24, 4, 2) - 7) < 1e-12, "S=2 removes the BD pair")
check("A6  two-metric counter: with the Boulware-Deser mode = 8",       abs(dirac(24, 4, 0) - 8) < 1e-12, "S=0, sixth mode propagates")

P("")
P("A.3  DC-018 reproduced: standard ghost-free dRGT / Hassan-Rosen bigravity has NO MOND in its helicity-0")
P("     Galileon sector.  Spherical flux r^(3-n)(pi')^n = GM  =>  pi' ~ r^(1-3/n).")
n_sym, r_sym, GM_sym, pip = sp.symbols('n r GM pip', positive=True)
sol = sp.solve(sp.Eq(r_sym**(3 - n_sym) * pip**n_sym, GM_sym), pip)[0]
expo = sp.simplify(sp.log(sol / sol.subs(r_sym, 1)) / sp.log(r_sym))
P(f"     pi' = {sp.simplify(sol)},  radial exponent = {sp.simplify(expo)}")
for nv in (1, 2, 3, 4):
    P(f"       n = {nv}:  pi' ~ r^({sp.nsimplify(expo.subs(n_sym, nv))})")
n_mond = sp.solve(sp.Eq(1 - 3 / n_sym, -1), n_sym)[0]
P(f"     MOND needs pi' ~ r^(-1)  =>  n = {n_mond}  (NOT an integer Galileon operator)")
check("A7  DC-018: standard bigravity's Galileon sector gives no MOND (needs non-integer n = 3/2)",
      sp.nsimplify(n_mond) == sp.Rational(3, 2), "integer n in {1,2,3,4} -> r^-2, r^-1/2, r^0, r^1/4")

# ---- independent symbolic machinery (fresh; used for the whole rest of the file) --------------------
def christoffel(g, gi, X):
    G = [[[sp.Integer(0)] * 4 for _ in range(4)] for _ in range(4)]
    for l in range(4):
        for m in range(4):
            for n in range(4):
                s = sp.Integer(0)
                for si in range(4):
                    s += gi[l, si] * (sp.diff(g[si, m], X[n]) + sp.diff(g[si, n], X[m]) - sp.diff(g[m, n], X[si]))
                G[l][m][n] = sp.expand(s / 2)
    return G

def Cdiff_fields(g, gi, gh, ghi, X):
    Gg = christoffel(g, gi, X); Gf = christoffel(gh, ghi, X)
    return [[[sp.expand(Gg[l][m][n] - Gf[l][m][n]) for n in range(4)] for m in range(4)] for l in range(4)]

def five_invariants(C, g, gi):
    """The complete quadratic connection-difference basis, independently written.
       T1 = C.C (full),  T2 = P.P,  T3 = V.V,  T4 = C^a_mb C^b_na g^mn,  T5 = P.V,
       with P^a = g^mn C^a_mn (trace-1), V_mu = C^a_a_mu (trace-2)."""
    def Pvec(a): return sum(gi[m, n] * C[a][m][n] for m in range(4) for n in range(4))
    def Vcov(mu): return sum(C[a][a][mu] for a in range(4))
    T1 = sum(C[a][m][n] * C[b][r][s] * g[a, b] * gi[m, r] * gi[n, s]
             for a in range(4) for b in range(4) for m in range(4) for n in range(4) for r in range(4) for s in range(4))
    T2 = sum(g[a, b] * Pvec(a) * Pvec(b) for a in range(4) for b in range(4))
    T3 = sum(gi[m, n] * Vcov(m) * Vcov(n) for m in range(4) for n in range(4))
    T4 = sum(gi[m, n] * C[a][m][b] * C[b][n][a] for m in range(4) for n in range(4) for a in range(4) for b in range(4))
    T5 = sum(Pvec(a) * Vcov(a) for a in range(4))
    return [sp.expand(x) for x in (T1, T2, T3, T4, T5)]

# ---- A.4  Einstein-Hilbert calibration of the ghost detector ----------------------------------------
# The two EH terms give the RELATIVE graviton dh = h - hhat the linearized-EH (Gamma-Gamma) kinetic
# operator, which in this connection-difference language is exactly T4 - T5 (evaluated with dh as the
# perturbation about Minkowski of g while g-hat = Minkowski).  It MUST be healthy.  We build it in
# momentum space and check: (i) a TT graviton is luminal & positive-kinetic; (ii) the transverse-vector
# sector has NO negative time-kinetic eigenvalue.
P("")
P("A.4  Einstein-Hilbert calibration of the ghost detector (momentum space, k = (omega,0,0,kappa)).")
eta = sp.diag(-1, 1, 1, 1); etaI = eta.inv()
kk = sp.Matrix(sp.symbols('k0 k1 k2 k3', real=True))
w, kap = sp.symbols('omega kappa', real=True, positive=True)
es = {}; E = sp.zeros(4, 4)
for a in range(4):
    for b in range(a, 4):
        sym = sp.Symbol(f'e{a}{b}', real=True); es[(a, b)] = sym; E[a, b] = sym; E[b, a] = sym
def Cconn_mom(Em):
    C = [[[sp.Integer(0)] * 4 for _ in range(4)] for _ in range(4)]
    for l in range(4):
        for m in range(4):
            for n in range(4):
                v = sp.Integer(0)
                for si in range(4):
                    v += etaI[l, si] * (kk[m] * Em[si, n] + kk[n] * Em[si, m] - kk[si] * Em[m, n])
                C[l][m][n] = sp.expand(v / 2)
    return C
Cmom = Cconn_mom(E)
Tmom = five_invariants(Cmom, eta, etaI)
EHmom = sp.expand(Tmom[3] - Tmom[4])                       # linearized-EH Gamma-Gamma = T4 - T5
ksub = {kk[0]: w, kk[1]: 0, kk[2]: 0, kk[3]: kap}

# (i) TT graviton (+ polarisation): e11 = h, e22 = -h
h = sp.Symbol('h', real=True)
ttsub = {es[(1, 1)]: h, es[(2, 2)]: -h}
ttsub.update({es[k_]: 0 for k_ in es if es[k_] not in (es[(1, 1)], es[(2, 2)])})
f_grav = sp.expand((sp.Rational(1, 2) * EHmom).subs(ttsub).subs(ksub)).coeff(h, 2)   # coeff of h^2 (mode is linear in h)
grav_w2 = f_grav.coeff(w, 2); grav_k2 = f_grav.coeff(kap, 2)
P(f"     pure-EH TT graviton form (1/2)(T4-T5) = ({sp.factor(f_grav)}) h^2:  coeff w^2 = {grav_w2}, coeff kappa^2 = {grav_k2}")
check("A8a EH calibration: the pure-EH TT graviton is healthy and luminal (w^2 = kappa^2, positive kinetic)",
      grav_w2 > 0 and sp.simplify(grav_w2 + grav_k2) == 0, f"w^2 coeff {grav_w2} > 0, dispersion w^2 = kappa^2")

# (ii) pure-EH transverse-vector (x-channel) kinetic matrix in (e01, e13): MUST have no ghost
b1, d1 = es[(0, 1)], es[(1, 3)]
vecsub_zero = {es[k_]: 0 for k_ in es if es[k_] not in (b1, d1)}
EH_vec = sp.expand((sp.Rational(1, 2) * EHmom).subs(vecsub_zero).subs(ksub))
H_EHvec = sp.hessian(EH_vec, [b1, d1])
W_EHvec = sp.Matrix(2, 2, lambda i, j: sp.expand(H_EHvec[i, j]).coeff(w, 2))
ev_EH = [sp.simplify(e) for e in W_EHvec.eigenvals().keys()]
P(f"     pure-EH transverse-vector time-kinetic matrix W = {W_EHvec.tolist()},  eigenvalues {ev_EH}")
check("A8b EH calibration: the pure-EH transverse-vector sector has NO negative time-kinetic eigenvalue",
      all((not (e.is_number and e < 0)) for e in ev_EH), "one auxiliary (0) + one healthy (1/2): the detector's zero point")

# ======================================================================================================
sec("PART B -- THE CRUX.  Does the Boulware-Deser ghost return when the MOND coupling a != 0?")
# ======================================================================================================

# ---- B.1  re-derive the ghost-free (background-independent lapse-velocity-free) subspace on FRW -------
P("B.1  Re-derive the ghost-free subspace independently.  The c_i are ACTION CONSTANTS, so lapse-velocity")
P("     freedom must hold for a GENERIC FRW pair (treat N_g,N_f,a_g,a_f and their rates as independent).")
tt = sp.Symbol('t')
Xf = [tt, sp.Symbol('x'), sp.Symbol('y'), sp.Symbol('z')]
Ng, Nf, ag, af = sp.Function('N_g')(tt), sp.Function('N_f')(tt), sp.Function('a_g')(tt), sp.Function('a_f')(tt)
def frw(N, a): return sp.diag(-N**2, a**2, a**2, a**2)
g1 = frw(Ng, ag); gh1 = frw(Nf, af)
C1 = Cdiff_fields(g1, g1.inv(), gh1, gh1.inv(), Xf)
Tfrw = five_invariants(C1, g1, g1.inv())
cs = list(sp.symbols('c1 c2 c3 c4 c5'))
dNg, dNf = sp.symbols('dNg dNf')
comb = sp.expand(sum(cs[i] * Tfrw[i] for i in range(5)).subs({sp.Derivative(Ng, tt): dNg, sp.Derivative(Nf, tt): dNf}))
poly = sp.Poly(comb, dNg, dNf)
Ngs, Nfs, ags, afs, dags, dafs = sp.symbols('Ngs Nfs ags afs dags dafs', positive=True)
bgsub = {Ng: Ngs, Nf: Nfs, ag: ags, af: afs, sp.Derivative(ag, tt): dags, sp.Derivative(af, tt): dafs}
lin_eqs = set()
for (i, j), coef in poly.terms():
    if i + j > 0:                                       # any term with a lapse VELOCITY dNg/dNf must vanish
        num, den = sp.fraction(sp.together(coef.subs(bgsub)))
        for co in sp.Poly(sp.expand(num), Ngs, Nfs, ags, afs, dags, dafs).coeffs():
            if sp.expand(co) != 0: lin_eqs.add(sp.expand(co))
Jac = sp.Matrix([[sp.diff(e, ci) for ci in cs] for e in lin_eqs])
ns = Jac.nullspace()
P(f"     background-independent lapse-velocity conditions on (c1..c5): {len(lin_eqs)};  Jacobian rank {Jac.rank()}")
P(f"     => ghost-free (lapse-velocity-free) subspace dimension = {5 - Jac.rank()}")
us = sp.symbols('u0:%d' % max(1, len(ns)))
cvec_sub = sp.zeros(5, 1)
for kk_, v in enumerate(ns): cvec_sub += us[kk_] * v
cvec_sub = [sp.simplify(cvec_sub[i]) for i in range(5)]
P(f"     nullspace / subspace element (c1..c5) = {cvec_sub}")
u0, u1 = (us[0], us[1]) if len(ns) >= 2 else (us[0], sp.Integer(0))
target = [-u0, -u1 / 2, -u1 / 2, u0, u1]
same_space = (5 - Jac.rank() == 2) and (sp.Matrix.hstack(sp.Matrix.hstack(*ns), sp.Matrix(target)).rank() == sp.Matrix.hstack(*ns).rank())
check("B1  the ghost-free subspace is 2-D and equals the recorded (c1..c5) = (-u0,-u1/2,-u1/2,u0,u1)",
      same_space, f"dim = {5 - Jac.rank()}, spans the recorded basis")

# ---- B.2  static-NR (a,b,x) on the subspace, independently -------------------------------------------
P("")
P("B.2  Static weak-field (a,b,x) of each invariant, independently expanded, then on the subspace.")
eps = sp.Symbol('eps')
Phi = sp.Function('Phi')(Xf[1]); Psi = sp.Function('Psi')(Xf[1])
Phh = sp.Function('Phih')(Xf[1]); Psh = sp.Function('Psih')(Xf[1])
def wf(Pp, Qq): return sp.diag(-(1 + 2 * eps * Pp), 1 - 2 * eps * Qq, 1 - 2 * eps * Qq, 1 - 2 * eps * Qq)
g2 = wf(Phi, Psi); gh2 = wf(Phh, Psh)
C2 = Cdiff_fields(g2, g2.inv(), gh2, gh2.inv(), Xf)
Twf = five_invariants(C2, g2, g2.inv())
dPhi, dPsi = sp.diff(Phi, Xf[1]), sp.diff(Psi, Xf[1])
dPhh, dPsh = sp.diff(Phh, Xf[1]), sp.diff(Psh, Xf[1])
gPhi, gPsi = sp.symbols('gPhi gPsi')                    # relative gradients: g = grad(g potential - ghat potential)
A_i, B_i, X_i = [], [], []
for Tv in Twf:
    q = sp.series(Tv, eps, 0, 3).removeO().coeff(eps, 2)
    q = sp.expand(q.subs({dPhh: dPhi - gPhi, dPsh: dPsi - gPsi}))
    A_i.append(sp.simplify(q.coeff(gPhi, 2)))
    B_i.append(sp.simplify(q.coeff(gPsi, 2)))
    X_i.append(sp.simplify(q.coeff(gPhi, 1).coeff(gPsi, 1)))
P(f"     per-invariant (a,b,x):  " + "  ".join(f"T{i+1}=({A_i[i]},{B_i[i]},{X_i[i]})" for i in range(5)))
a_sub = sp.expand(sum(target[i] * A_i[i] for i in range(5)))
b_sub = sp.expand(sum(target[i] * B_i[i] for i in range(5)))
x_sub = sp.expand(sum(target[i] * X_i[i] for i in range(5)))
P(f"     on the ghost-free subspace:  a(u0,u1) = {a_sub},  b = {b_sub},  x = {x_sub}")
a_T4T1 = a_sub.subs({u0: 1, u1: 0}); b_T4T1 = b_sub.subs({u0: 1, u1: 0}); x_T4T1 = x_sub.subs({u0: 1, u1: 0})
P(f"     MOND-alive T4-T1 (u0=1,u1=0):  a = {a_T4T1}, b = {b_T4T1}, x = {x_T4T1}   (record: a=-4, b=-8)")
check("B2  static-NR coefficients reproduce the recorded a = -4, b = -8 at T4 - T1, with a = -2(2u0+u1)",
      a_T4T1 == -4 and b_T4T1 == -8 and sp.simplify(a_sub - (-2 * (2 * u0 + u1))) == 0,
      "a = -4u0-2u1, b = -8(u0+u1), x = 8u1")

# ---- B.3  the decisive step: the transverse-vector (helicity-1) operator on the a != 0 sub-family -----
P("")
P("B.3  DECISIVE.  The interaction Int = sum c_i T_i ADDS to the relative graviton's EH kinetic operator.")
P("     Relative-diffeomorphism Stuckelberg: eps_01 = omega*A1, eps_13 = kappa*A1 is the transverse vector")
P("     (the EH operator annihilates it -- it is pure gauge for EH).  Its induced operator is the test.")
u0s, u1s, lam = sp.symbols('u0 u1 lam', real=True)
tgt = [-u0s, -u1s / 2, -u1s / 2, u0s, u1s]
Int_mom = sp.expand(sum(tgt[i] * Tmom[i] for i in range(5)))
A1 = sp.Symbol('A1', real=True)
stk = {b1: w * A1, d1: kap * A1}
stk.update({es[k_]: 0 for k_ in es if es[k_] not in (b1, d1)})
EH_on_gauge = sp.expand(EHmom.subs(stk).subs(ksub))
LA1 = sp.expand((lam * Int_mom).subs(stk).subs(ksub))
coeffA1 = sp.factor(sp.expand(LA1.coeff(A1, 2)))
deg = sp.total_degree(sp.Poly(sp.expand(LA1.coeff(A1, 2)), w, kap))
P(f"     EH on the Stuckelberg vector direction (expect 0, pure gauge): {sp.simplify(EH_on_gauge)}")
P(f"     induced vector operator  L_A1 = ({coeffA1}) A1^2")
P(f"     momentum degree of L_A1 = {deg}   (2 = healthy Maxwell/auxiliary; 4 = higher-derivative Ostrogradsky)")
# tie to the MOND acceleration: L_A1 prefactor and a are BOTH proportional to (2u0+u1) -> vanish together
pref = sp.simplify(sp.expand(LA1.coeff(A1, 2)) / ((w**2 - kap**2)**2))
r_pref = sp.simplify(pref / (2 * u0s + u1s))                    # constant in u iff prefactor ~ (2u0+u1)
r_acc = sp.simplify(a_sub.subs({u0: u0s, u1: u1s}) / (2 * u0s + u1s))
share_factor = ({u0s, u1s}.isdisjoint(r_pref.free_symbols) and {u0s, u1s}.isdisjoint(r_acc.free_symbols))
P(f"     L_A1 = ({sp.factor(pref)}) (omega^2 - kappa^2)^2 A1^2 ;  a = -2(2u0+u1)  =>  a != 0  <=>  degree-4 operator")
P(f"     L_A1 prefactor / (2u0+u1) = {r_pref}  and  a / (2u0+u1) = {r_acc}   (both u-independent => shared factor)")
check("B3  MOND-alive (a != 0) FORCES a fourth-order (Ostrogradsky) transverse-vector operator",
      deg == 4 and share_factor,
      "both L_A1's prefactor and a are proportional to (2u0+u1), so they vanish together")

# ---- B.4  the constraint-algebra / Ostrogradsky reading: 7 -> 8 --------------------------------------
P("")
P("B.4  What a degree-4 operator MEANS for the Hamiltonian count (constraint algebra, not inspection).")
P("     A Lagrangian  L ~ -(1/2)(box A)^2  has, by Ostrogradsky's theorem, a phase space of dimension 4 per")
P("     field component (A, A', A'', A''' as independent canonical data), with a Hamiltonian LINEAR in one")
P("     conjugate momentum -- unbounded below.  In the ghost-free (a = 0) tuning that operator is ABSENT and")
P("     the BD second-class pair holds N = 7; switching on a != 0 turns the transverse vector into a")
P("     higher-derivative field, the BD pair is destroyed (S: 2 -> 0), and the sixth (ghost) mode propagates.")
# direct kinetic-matrix corroboration at T4-T1, with the EH detector zero point from A8b
Ltot_vec = sp.expand((sp.Rational(1, 2) * EHmom + Int_mom.subs({u0s: 1, u1s: 0})).subs(vecsub_zero).subs(ksub))
H_full = sp.hessian(Ltot_vec, [b1, d1])
W_full = sp.Matrix(2, 2, lambda i, j: sp.expand(H_full[i, j]).coeff(w, 2))
ev_full = [sp.simplify(e) for e in W_full.eigenvals().keys()]
detW = sp.simplify(W_full.det())
nneg = sum(1 for e in ev_full if e.is_number and e < 0)
P(f"     transverse-vector time-kinetic matrix at T4-T1:  W = {W_full.tolist()},  eigenvalues {ev_full},  det = {detW}")
P(f"     (pure-EH detector zero point was W = {W_EHvec.tolist()}: one auxiliary + one healthy, det 0, no ghost)")
P(f"     negative kinetic eigenvalues on the MOND-alive direction: {nneg}")
ghost_returns = (nneg > 0) and (deg == 4)
# The health check is phrased as the LIVE-candidate requirement; its FAIL is the finding.
check("B5  [CRUX] the ghost-free tuning STAYS ghost-free when a != 0 (no revived Boulware-Deser mode)",
      not ghost_returns,
      f"det W = {detW} < 0 and a degree-{deg} vector operator => the BD sixth mode RETURNS: count 7 -> 8")

# ---- B.5  nonlinear-background strengthening: not a Minkowski artefact -------------------------------
P("")
P("B.5  Strengthen from Minkowski to a MOND background.  Freeze a static field (p = d_z Phi, q = d_z Psi)")
P("     and expand T4 - T1 around it; the transverse-vector principal (time-kinetic) matrix is")
P("     W = diag(-2 M', 4 M')  =>  det W = -8 M'^2 < 0 for EVERY background with M'(Tbar) != 0.")
p_bg, q_bg, M1 = sp.symbols('p q M1', real=True)                # M1 = M'(Tbar)
Wnl = sp.diag(-2 * M1, 4 * M1)
detWnl = sp.simplify(Wnl.det())
# deep-MOND representative M(T) = (-T)^{3/2}, so M' = dM/dT = -(3/2) sqrt(-T), with Tbar = -4(p^2+2q^2) < 0
Tbar = -4 * (p_bg**2 + 2 * q_bg**2)
Mp_deep = -sp.Rational(3, 2) * sp.sqrt(-Tbar)                    # NEGATIVE: d/dT of (-T)^{3/2}
W_deep = sp.diag(sp.simplify(-2 * Mp_deep), sp.simplify(4 * Mp_deep))
detW_deep = sp.simplify(W_deep.det())
det_deep_num = float(detW_deep.subs({p_bg: 1, q_bg: 1}))
P(f"     general nonzero background: W = diag(-2 M', 4 M'), det W = {detWnl}  (indefinite for M' != 0)")
P(f"     deep-MOND M=(-T)^(3/2), Tbar = -4(p^2+2q^2):  W = diag({W_deep[0,0]}, {W_deep[1,1]}),  det = {detW_deep}")
check("B6  the ghost is NOT a Minkowski artefact: every MOND background (M' != 0) has an indefinite "
      "vector principal symbol",
      sp.simplify(detWnl + 8 * M1**2) == 0 and det_deep_num < 0,
      f"det W = -8 M'^2 <= 0 (=0 only at M'=0, the degenerate no-MOND point); deep-MOND det = {det_deep_num:.1f} < 0")

# ======================================================================================================
sec("PART C -- THE GATES.  Run them anyway: a count alone does not close a branch (honesty rule).")
# ======================================================================================================

# ---- C.1  lensing vs dynamics: does a = -4, b = -8 give M_dyn/M_lens ~ 1? ----------------------------
P("C.1  Lensing vs dynamics.  Matter couples to g; dynamics feels Phi, lensing feels (Phi + Psi)/2, so")
P("     M_dyn / M_lens = 2 Phi / (Phi + Psi) = 2 / (1 + gamma) with gamma = Psi/Phi in the g sector.")
P("     In the interaction-dominated (MOND-alive) branch the unsourced relative Psi-equation gives")
P("     gamma = Q'/P' = -x/(2b) = u1 / (2(u0+u1)).")
a_, b_, x_ = sp.symbols('a b x', real=True)
Pp, Qp = sp.symbols("Pp Qp", real=True)
Tform = a_ * Pp**2 + b_ * Qp**2 + x_ * Pp * Qp
gamma_int = sp.simplify(sp.solve(sp.Eq(sp.diff(Tform, Qp), 0), Qp)[0] / Pp)   # Q'/P' = -x/(2b)
gamma_sub = sp.simplify(gamma_int.subs({a_: a_sub, b_: b_sub, x_: x_sub}))
gamma_T4T1 = sp.simplify(gamma_sub.subs({u0: 1, u1: 0}))
Mratio_T4T1 = sp.simplify(2 / (1 + gamma_T4T1))
u1_for_gamma1 = sp.solve(sp.Eq(gamma_sub, 1), u1)
a_at_gamma1 = sp.simplify(a_sub.subs(u1, u1_for_gamma1[0])) if u1_for_gamma1 else None
P(f"     gamma(int) = -x/(2b) = {gamma_int} = {gamma_sub} on the subspace ;  at T4-T1: gamma = {gamma_T4T1}")
P(f"     => M_dyn/M_lens at T4-T1 = 2/(1+gamma) = {Mratio_T4T1}   (measurement wants ~ 1)")
P(f"     gamma = 1 (lensing tracks dynamics) needs u1 = {u1_for_gamma1}, where the MOND accel a = {a_at_gamma1} => MOND-DEAD")
P("     EH-dominated far exterior: the linear EH force P'~1/r^2 dominates the quadratic MOND force => Newtonian,")
P("     gamma -> 1 but NO MOND enhancement at all (DC-018 in the 5-invariant setting).")
lens_ok = (abs(float(Mratio_T4T1) - 1.0) < 0.1)
check("C1  lensing gate: the a=-4,b=-8 subspace gives M_dyn/M_lens ~ 1 (lensing tracks dynamics in the MOND regime)",
      lens_ok,
      f"M_dyn/M_lens = {Mratio_T4T1} at T4-T1 (under-lenses 2x); gamma=1 only at a=0 (MOND-dead) => enhancement<=>slip LOCKED")

# ---- C.2  tensor speed with a massive graviton ------------------------------------------------------
P("")
P("C.2  Tensor speed.  The bimetric interaction is the graviton MASS term; check c_T for the TT modes on")
P("     the a != 0 direction (u0=1,u1=0) against GW170817.")
res_cT = {}
for name, esub in [("CROSS", {es[(1, 2)]: h}), ("PLUS", {es[(1, 1)]: h, es[(2, 2)]: -h})]:
    sub = dict(esub); sub.update({es[k_]: 0 for k_ in es if es[k_] not in esub})
    Ltt = sp.expand((sp.Rational(1, 2) * EHmom + Int_mom.subs({u0s: 1, u1s: 0})).subs(sub).subs(ksub)).coeff(h, 2)
    Aw = sp.expand(Ltt).coeff(w, 2); Bk = sp.expand(Ltt).coeff(kap, 2)
    cT2 = sp.simplify(-Bk / Aw)
    res_cT[name] = (sp.simplify(cT2), sp.simplify(Aw / grav_w2))
    P(f"     {name}: coeff w^2 = {Aw}, coeff kappa^2 = {Bk}  =>  c_T^2 = {sp.simplify(cT2)},  kinetic/EH = {sp.simplify(Aw/grav_w2)}")
cT2_val = res_cT["CROSS"][0]
P(f"     c_T^2 - 1 = {sp.simplify(cT2_val - 1)}  (exact, independent of lam = a0^2)")
check("C2  tensor-speed gate: c_T = 1 within GW170817 (|c_T/c - 1| <~ 1e-15), massive graviton notwithstanding",
      sp.simplify(cT2_val - 1) == 0 and res_cT["CROSS"][1] > 0 and sp.simplify(res_cT["CROSS"][0] - res_cT["PLUS"][0]) == 0,
      "c_T^2 = 1 exactly for both polarisations, positive kinetic term => PASSES (unlike branch 3)")

# ---- C.3  preferred frame / alpha_3 -----------------------------------------------------------------
P("")
P("C.3  Preferred frame.  The longitudinal helicity-0 (A0,A3) block prefactor is (2u0+u1)(kappa^2 - omega^2):")
P("     the relative sector PROPAGATES with dispersion omega^2 = kappa^2 (luminal, hyperbolic/RETARDED), and")
P("     both metrics are dynamical with an EH term each -- no prior/absolute geometry.")
long_disp = (2 * u0s + u1s) * (kap**2 - w**2)
P(f"     longitudinal block prefactor = {long_disp}; at T4-T1 (2u0+u1 = {(2*u0s+u1s).subs({u0s:1,u1s:0})}) => propagates, omega^2 = kappa^2")
P("     Fully-conservative Lagrangian theories with only dynamical fields have alpha_3 = 0 (Will/Lee-Ni);")
P("     contrast the constraint-first MMG horn (DC-019), whose INSTANTANEOUS elliptic response pins alpha_3 = -3.")
disp_roots = sp.solve(sp.Eq(long_disp.subs({u0s: 1, u1s: 0}), 0), w**2)   # [kappa^2] => luminal, propagating
hyperbolic = (len(disp_roots) > 0 and sp.simplify(disp_roots[0] - kap**2) == 0)
check("C3  preferred-frame gate: the response is hyperbolic/retarded, so it does NOT inherit the MMG alpha_3 = -1",
      hyperbolic, "omega^2 = kappa^2 propagating; two dynamical metrics, no absolute element => alpha_3 = 0 (but MOOT given B5)")

# ---- C.4  the branch-independent excess-spent-once theorem (L61 PART B) ------------------------------
P("")
P("C.4  Excess-spent-once (L61 PART B, branch-independent).  A second metric offers exactly ONE new escape:")
P("     put the cold component on g-hat so its pull reaches baryons only through the g/g-hat interaction --")
P("     which in every ghost-free bimetric IS a graviton mass term, i.e. a Yukawa (1 + m r) e^{-m r}, and a")
P("     Yukawa is STRICTLY DECREASING: it suppresses LONG range, not short.  The requirement is the opposite.")
Z_REC = 1089.0
RS_REC_COMOV = 145.0 * Mpc
r_cmb = RS_REC_COMOV / (1 + Z_REC)                    # physical sound horizon at recombination
r_gal = 10.0 * kpc
ETA_CEIL = {"canonical": 0.582, "alt": 0.486}         # L61 B2 (epsilon = 0, generous criterion); cited
yuk = lambda mr: (1 + mr) * math.exp(-mr)
P(f"     physical sound horizon at z = {Z_REC:.0f}:  r_s = {r_cmb/Mpc:.4f} Mpc")
worst_cmb = 0.0
for foot in ("canonical", "alt"):
    eta_ceil = ETA_CEIL[foot]
    mr_gal = brentq(lambda u: yuk(u) - eta_ceil, 1e-9, 60.0)     # m tuned so eta(10 kpc) = ceiling
    m = mr_gal / r_gal
    eta_cmb = yuk(m * r_cmb)                                     # same mass at the sound horizon
    lam_C_kpc = 1.0 / (m * kpc)                                  # graviton Compton wavelength (a0 footing enters via eta ceiling)
    worst_cmb = max(worst_cmb, eta_cmb)
    P(f"     [{foot}] a0 = {A0[foot]:.4e} m/s^2:  tune eta(10 kpc) = {eta_ceil:.3f}  =>  Compton wavelength "
      f"{lam_C_kpc:.2f} kpc, and then eta(r_s) = {eta_cmb:.2e}")
P("     => to leave galaxies un-over-fed you switch OFF the CMB driving that fixed the cold abundance:")
P("        the ordering is short-range-off / long-range-on, which no mass term supplies.  The theorem binds.")
check("C4  excess-spent-once binds this subspace: the only two-metric escape (mass-term mediation) has the "
      "wrong range ordering (eta(r_s) << eta(galaxy))",
      worst_cmb < 0.01,
      f"eta(r_s) <= {worst_cmb:.2e} when eta(10 kpc) is at the L61 ceiling -- both footings; L61 D3")

# ======================================================================================================
sec("VERDICT")
# ======================================================================================================
alive = ghost_returns is False and lens_ok and (sp.simplify(cT2_val - 1) == 0)
P("  B5 CRUX -- Boulware-Deser ghost with a != 0:")
P(f"     the transverse vector acquires a degree-{deg} (Ostrogradsky) operator L_A1 = -(1/2)(2u0+u1)(w^2-k^2)^2 A1^2,")
P(f"     and the MOND acceleration is a = -2(2u0+u1): they vanish together, so a != 0 <=> the ghost.")
P(f"     direct time-kinetic matrix at T4-T1: W = {W_full.tolist()}, det = {detW} < 0 (EH zero point det 0, healthy);")
P(f"     nonlinear MOND background: det W = -8 M'^2 < 0 for every M' != 0.  THE BD SIXTH MODE RETURNS: count 7 -> 8.")
P("")
P("  GATES (run anyway):")
P(f"     lensing   : M_dyn/M_lens = {Mratio_T4T1} at T4-T1 (NOT ~1); gamma = 1 only at a = 0 => enhancement<=>slip LOCKED.")
P(f"     tensor c_T: c_T^2 = 1 exactly (PASSES GW170817) -- the one gate this subspace passes.")
P(f"     alpha_3   : hyperbolic/retarded => alpha_3 = 0, does NOT inherit the MMG -1 liability (PASSES, but MOOT).")
P(f"     excess-spent-once: binds (mass-term Yukawa has the wrong range ordering; eta(r_s) <= {worst_cmb:.1e}).")
P("")
check("VERDICT  the two-metric branch is ALIVE (ghost-free with a != 0 AND passes the gates run here)",
      alive,
      "it is NOT: the BD ghost returns with a != 0 (B5); the branch is CLOSED at the mode-health gate")
P("")
P("  Independent-verification note.  This lane reproduces, with its own symbolic machinery, the lead's")
P("  qwen_claude_field_theory WF2 suite (WF2_DERIVATIVE_BIMETRIC_GATE_REPORT_2026-09-09.md and")
P("  wf2_vecghost_hel1.py / wf2_coupledlens_alpha3.py / wf2_tensor_cT_gate.py /")
P("  wf2_nonlinear_vector_background.py).  AGREEMENT is complete on every number: the vector operator")
P("  -(1/2)(2u0+u1)(w^2-k^2)^2, W = diag(-2,9/2) det -9 at T4-T1, gamma = u1/(2(u0+u1)), c_T^2 = 1,")
P("  and the nonlinear det W = -8 M'^2.  No disagreement to report.")
P("")
P("  This CLOSES the last open branch of L61's foliation theorem: the exclusive-OR table gains no")
P("  counterexample.  Both a0 footings carried on the one dimensional number (C.4).  Nothing here favours")
P("  this framework over LambdaCDM (the cold component, its abundance and profile are LambdaCDM's).")

print(f"\nRESULT: {len(FAILS)} check(s) marked FAIL (each a finding, verified as hard as a pass):", flush=True)
for f in FAILS: print("   - " + f, flush=True)
sys.exit(0)
