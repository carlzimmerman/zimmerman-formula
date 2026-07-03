#!/usr/bin/env python3
"""
laneA_nonlinear_boundary.py
Lane A, part 3: the BOUNDARY of the state-blindness theorem. Show explicitly that
the free/linear assumptions are load-bearing:

  A (symbolic): quadratic coupling q*x^2 -> the second-order response kernel is
     <[x^2(t), x^2(s)]> = 4 * kappa(t,s) * S(t,s):  commutator (c-number) TIMES the
     state-dependent symmetric correlator -> STATE-DEPENDENT and NON-STATIONARY
     (contains t+s terms for squeezed states).
  B (numeric): ANHARMONIC bath mode (H = w a'a + lam x^4) with LINEAR coupling ->
     even the commutator expectation <[x(t),x(s)]> becomes state-dependent.
  C (numeric): q^2*x coupling (multiplicative noise) -> the oscillation frequency
     of <q(t)> depends on the bath state (vacuum vs squeezed) -> state-dependent
     effective stiffness/inertia at second order.

=> If the non-stationary door is open anywhere, it is ONLY in structured/nonlinear
   baths -- handed to lanes B/C. Exit 0 iff all assertions pass.
"""
import math
import numpy as np
import sympy as sp

# macOS Accelerate BLAS raises spurious FP flags inside matmul (known numpy issue);
# silence them and guard every load-bearing result with explicit isfinite asserts.
np.seterr(all='ignore')

# ==================================================================
# PART A: operator identity [X^2, Y^2] = 2*kappa*(XY + YX) when [X,Y]=kappa central
# ==================================================================
X, Y = sp.symbols('X Y', commutative=False)
kap = sp.Symbol('kappa')

def normal_order(expr):
    expr = sp.expand(expr)
    if expr.is_Add:
        return sp.expand(sp.Add(*[normal_order(a) for a in expr.args]))
    c_part, nc_raw = expr.args_cnc()
    coeff = sp.Mul(*c_part)
    nc = []
    for f in nc_raw:                                  # flatten X**n -> [X]*n
        if f.is_Pow and f.exp.is_Integer and f.exp > 0:
            nc.extend([f.base] * int(f.exp))
        else:
            nc.append(f)
    for i in range(len(nc) - 1):
        if nc[i] == Y and nc[i + 1] == X:
            swapped = nc[:i] + [X, Y] + nc[i + 2:]
            reduced = nc[:i] + nc[i + 2:]
            return normal_order(coeff * (sp.Mul(*swapped) - kap * sp.Mul(*reduced)))
    return expr

lhs = normal_order(X * X * Y * Y - Y * Y * X * X)
rhs = normal_order(2 * kap * (X * Y + Y * X))
assert sp.simplify(lhs - rhs) == 0
print("PART A  operator identity verified: [X^2,Y^2] = 2*[X,Y]*(XY+YX) for central [X,Y].")

# With X = x(t), Y = x(s) (free mode): kappa(t,s) = i*hbar*sin(w(s-t))/w (c-number,
# laneA_symbolic script), and <XY+YX> = 2 S(t,s). So the q*x^2 response kernel is
#   K2(t,s) = <[x^2(t), x^2(s)]> = 4 * kappa(t,s) * S(t,s)   -- Wick/Gaussian exact.
t, s, w, hb = sp.symbols('t s omega hbar', positive=True)
A, B, C = sp.symbols('A B C', real=True)
S = (A * sp.cos(w * t) * sp.cos(w * s) + B * sp.sin(w * t) * sp.sin(w * s) / w**2
     + C * (sp.cos(w * t) * sp.sin(w * s) + sp.sin(w * t) * sp.cos(w * s)) / w)
kappa_ts = sp.I * hb * sp.sin(w * (s - t)) / w
K2 = sp.expand(4 * kappa_ts * S)
# state dependence: derivative wrt squeezing parameters is nonzero
assert sp.simplify(sp.diff(K2, A)) != 0 and sp.simplify(sp.diff(K2, C)) != 0
# non-stationarity: depends on T=(t+s)/2 unless vacuum/thermal (B=A w^2, C=0)
T_, tau_ = sp.symbols('T tau', real=True)
K2T = sp.expand_trig(K2.subs([(t, T_ + tau_ / 2), (s, T_ - tau_ / 2)]))
dK2dT = sp.simplify(sp.diff(K2T, T_))
assert sp.simplify(dK2dT.subs([(B, A * w**2), (C, 0)])) == 0
assert sp.simplify(dK2dT.subs([(A, 2), (B, w**2), (C, 0),
                               (tau_, 1), (T_, sp.pi / (5 * w))])) != 0
print("        q*x^2 response kernel K2 = 4*kappa(t,s)*S(t,s): dK2/dA != 0, dK2/dC != 0")
print("        (STATE-DEPENDENT) and dK2/dT != 0 for squeezed states (NON-STATIONARY),")
print("        while dK2/dT == 0 for vacuum/thermal. The nonlinear-coupling kernel can")
print("        oscillate in lab time -- exactly the structure a transient mechanism needs,")
print("        but it requires NONLINEAR coupling. Sign/magnitude budget -> lanes B/C.")

# ==================================================================
# PART B: anharmonic bath mode, LINEAR coupling -> commutator itself state-dependent
# ==================================================================
def fock_ops(d):
    a = np.diag(np.sqrt(np.arange(1, d)), 1)
    return a, a.conj().T

def x_heis(H, x, tt):
    ev, V = np.linalg.eigh(H)
    ph = np.exp(1j * ev * tt)
    Ut = (V * ph) @ V.conj().T
    return Ut @ x @ Ut.conj().T

def squeezed_vec(d, r):
    a, ad = fock_ops(d)
    M = -1j * (r / 2) * (ad @ ad - a @ a)        # K = (r/2)(a'^2 - a^2) = i M, M hermitian
    ev, V = np.linalg.eigh(M)
    Sq = (V * np.exp(1j * ev)) @ V.conj().T
    v = np.zeros(d, complex); v[0] = 1.0
    return Sq @ v

def comm_expect(lam, d, t1, s1, states):
    a, ad = fock_ops(d)
    x = (a + ad) / np.sqrt(2)
    H = ad @ a + lam * np.linalg.matrix_power(x, 4)
    xt, xs = x_heis(H, x, t1), x_heis(H, x, s1)
    Cop = xt @ xs - xs @ xt
    out = {}
    for name, rho in states.items():
        out[name] = np.trace(rho @ Cop).imag
    return out

d = 70
nbar = 1.0
pn = (nbar / (1 + nbar))**np.arange(d) / (1 + nbar); pn /= pn.sum()
sv = squeezed_vec(d, 0.6)
sts = {'vacuum': np.diag([1.0] + [0.0] * (d - 1)).astype(complex),
       'thermal_n1': np.diag(pn).astype(complex),
       'squeezed_r0.6': np.outer(sv, sv.conj())}
t1, s1 = 2.0, 0.5
harm = comm_expect(0.0, d, t1, s1, sts)
anh = comm_expect(0.05, d, t1, s1, sts)
anh80 = comm_expect(0.05, 90, t1, s1,
                    {'vacuum': np.diag([1.0] + [0.0] * 89).astype(complex)})
h_spread = max(harm.values()) - min(harm.values())
a_spread = max(anh.values()) - min(anh.values())
print(f"PART B  Im<[x(t),x(s)]> at (t,s)=({t1},{s1}):")
print(f"        harmonic  (lam=0)   : " + "  ".join(f"{k}={v:+.6f}" for k, v in harm.items()))
print(f"        anharmonic(lam=0.05): " + "  ".join(f"{k}={v:+.6f}" for k, v in anh.items()))
print(f"        spread: harmonic {h_spread:.2e} (state-blind), anharmonic {a_spread:.2e}")
print(f"        truncation check d=70 vs 90 (vacuum, anharm): "
      f"{abs(anh['vacuum'] - anh80['vacuum']):.2e}")
assert h_spread < 1e-10, "harmonic control failed"
assert a_spread > 1e3 * max(h_spread, 1e-12), "anharmonic state dependence not found"
assert abs(anh['vacuum'] - anh80['vacuum']) < 1e-6, "Fock truncation not converged"
print("        PASS: an ANHARMONIC bath makes even the commutator state-dependent --")
print("        linear coupling to a NON-free field escapes the theorem.")

# ==================================================================
# PART C: q^2 * x coupling (multiplicative noise): bath state shifts <q> frequency
# ==================================================================
ds, db = 14, 48
bq, bqd = fock_ops(ds)                      # system
ba, bad = fock_ops(db)                      # bath mode
qop = (bq + bqd) / np.sqrt(2)
xop = (ba + bad) / np.sqrt(2)
Id_s, Id_b = np.eye(ds), np.eye(db)
Om0, wb, g, r_sq = 1.0, 3.0, 0.2, 0.7
H_nl = (np.kron(bqd @ bq, Id_b) * Om0 + np.kron(Id_s, bad @ ba) * wb
        + g * np.kron(qop @ qop, xop))                 # NONLINEAR (q^2 x)
H_li = (np.kron(bqd @ bq, Id_b) * Om0 + np.kron(Id_s, bad @ ba) * wb
        + g * np.kron(qop, xop))                       # LINEAR control (q x)

alpha = 0.6
cs = np.exp(-abs(alpha)**2 / 2) * alpha**np.arange(ds) / np.sqrt(
    [math.factorial(n) for n in range(ds)])
sv_b = squeezed_vec(db, r_sq)
vac_b = np.zeros(db, complex); vac_b[0] = 1.0
tail = np.sum(np.abs(sv_b[-6:])**2)          # Fock-truncation tail (breaks exact linearity)
assert tail < 1e-9, f"squeezed state truncation tail too large: {tail:.1e}"

tsC = np.linspace(0.0, 150.0, 3000)
Qfull = np.kron(qop, Id_b)

def traj(H, bath_vec):
    ev, V = np.linalg.eigh(H)
    psi0 = np.kron(cs.astype(complex), bath_vec)
    c0 = V.conj().T @ psi0
    out = np.empty(len(tsC))
    QV = V.conj().T @ Qfull @ V
    for i, tt in enumerate(tsC):
        ph = np.exp(-1j * ev * tt) * c0
        out[i] = np.real(ph.conj() @ (QV @ ph))
    assert np.all(np.isfinite(out))
    return out

def fit_freq(y):
    best = (None, np.inf)
    for nuv in np.linspace(0.90, 1.10, 4001):
        M = np.column_stack([np.cos(nuv * tsC), np.sin(nuv * tsC), np.ones_like(tsC)])
        r = y - M @ np.linalg.lstsq(M, y, rcond=None)[0]
        val = r @ r
        if val < best[1]:
            best = (nuv, val)
    return best[0]

q_vac, q_sq = traj(H_nl, vac_b), traj(H_nl, sv_b)
l_vac, l_sq = traj(H_li, vac_b), traj(H_li, sv_b)
nu_vac, nu_sq = fit_freq(q_vac), fit_freq(q_sq)
d_nl = np.max(np.abs(q_sq - q_vac))
d_li = np.max(np.abs(l_sq - l_vac))
print(f"PART C  <q(t)> with bath vacuum vs squeezed(r={r_sq}), same coupling g={g}"
      f" (truncation tail {tail:.1e}):")
print(f"        LINEAR   q*x   control: max traj difference = {d_li:.3e}  (state-blind)")
print(f"        NONLINEAR q^2*x       : max traj difference = {d_nl:.3e}  (state-DEPENDENT)")
print(f"        fitted <q> frequency: vacuum nu={nu_vac:.5f}, squeezed nu={nu_sq:.5f}"
      f" (bare Om0={Om0}); shift difference {abs(nu_sq - nu_vac):.1e}")
assert d_li < 1e-6, "linear control shows state dependence beyond truncation floor -- bug"
assert d_nl > 1e3 * max(d_li, 1e-13), "no state dependence found in q^2 x case"
assert abs(nu_sq - nu_vac) > 1e-4    # measurable state-induced stiffness shift
print("        PASS: identical states, identical g -- linear coupling gives ZERO mean-")
print("        trajectory state dependence; multiplicative (q^2 x) coupling lets the state")
print("        re-enter the mean dynamics (noise-mean coupling) -> state-dependent")
print("        effective stiffness/inertia at second order.")

print()
print("BOUNDARY VERDICT: state-blindness is EXACTLY as wide as (linear coupling) x (free")
print("bath) -- break either and the response kernel becomes state-dependent and can be")
print("non-stationary. The non-stationary door, if open at all, lives ONLY in structured/")
print("nonlinear baths (lanes B/C); free fields + dS vacuum are closed at ALL times.")
print()
print("laneA_nonlinear_boundary: ALL ASSERTIONS PASS")
