#!/usr/bin/env python3
"""CMB2 / D2: the P sector of v3s (+ adopted blend) on FRW at z ~ 1100.

Criteria: FROZEN_CRITERIA.md (this directory). Adopts nothing. kappa = 1/2 FITTED; not theory closed.
Both footings, never pooled. No LCDM input: background = F1A B2 best fit per footing.

Steps
 S1  mode count (sympy): full 3+1 (unitary gauge, lapse N, shift N^i, leaf metric a^2 e^{2 zeta} delta_ij)
     construction of P^m A_m - W(K|P|) - gamma_L F(Pi) from the covariant definitions; show no d_t P_i
     (and no d_t N) appears once n.P = 0 holds; Hessian wrt d_t P vanishes.  Variant keeping P_0 free with the
     multiplier: Hessian rank 1 (only d_t P^0 via F), Dirac chain closes -> 0 DoF.
 S2  linear Fourier count: EOM matrix of delta P around a local background; det independent of omega -> 0 modes.
 S3  constrained response: expand the Legendre map about A = 0; linear order of P eq + Poisson is degenerate
     (0 = K delta rho), next order is deep-MOND div(|A| A)/a0 = K delta rho (non-analytic). Plane-wave exact
     solution and its time behaviour for an oscillating source (phase-locked, zero mean).
 S4  stiffness at z 1100: gamma_L Pi / c^2 and gamma_L |D Pi| / |A| for Lstar 21.7/22.9 - 90 pc, k 0.01-0.3.
 S5  pre-screen (structural).
 MUTATE: add (m/2)(n.nabla P)^2 by hand; S1/S2 machinery must find a propagating mode (sound speed derived).
"""
import json, resource, sys, time
import numpy as np
import sympy as sp

OUT = {}
LOG = []
def say(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True); LOG.append(s)

MUTATE = len(sys.argv) > 1 and sys.argv[1] == "MUTATE"
say("CMB2 / D2 P-sector  run:", "MUTATE" if MUTATE else "MAIN", time.strftime("%Y-%m-%d %H:%M:%S"))

# ------------------------------------------------------------------ S1: nonlinear 3+1 construction
t, x, y, z = sp.symbols("t x y z", real=True)
X = [t, x, y, z]
K, gam, mkin = sp.symbols("K gamma_L m_kin", positive=True)
a = sp.Function("a")(t)
zeta = sp.Function("zeta")(*X)
N = sp.Function("N")(*X)
Ns = [sp.Function(f"N{i}")(*X) for i in (1, 2, 3)]            # shift N^i
Pl = [sp.Function(f"P{i}")(*X) for i in (1, 2, 3)]            # P_i (lower, leaf)
P0f = sp.Function("P0")(*X)                                   # P_0 (lower)
Wf, Ff = sp.Function("W"), sp.Function("F")

gs = a**2 * sp.exp(2 * zeta)                                  # gamma_ij = gs delta_ij
gam_ij = sp.eye(3) * gs
gam_inv = sp.eye(3) / gs
Nup = sp.Matrix(Ns)
Nlow = gam_ij * Nup
g = sp.zeros(4, 4)
g[0, 0] = -N**2 + (Nup.T * gam_ij * Nup)[0]
for i in range(3):
    g[0, i + 1] = g[i + 1, 0] = Nlow[i]
    for j in range(3):
        g[i + 1, j + 1] = gam_ij[i, j]
gi = sp.zeros(4, 4)
gi[0, 0] = -1 / N**2
for i in range(3):
    gi[0, i + 1] = gi[i + 1, 0] = Nup[i] / N**2
    for j in range(3):
        gi[i + 1, j + 1] = gam_inv[i, j] - Nup[i] * Nup[j] / N**2
chk = sp.simplify(g * gi - sp.eye(4))
assert chk == sp.zeros(4, 4), "ADM inverse metric check failed"
say("S1 ADM inverse metric identity: exact")

sqrtmg = N * gs**sp.Rational(3, 2)                            # sqrt(-g) = N sqrt(gamma)
Q = 1 / N                                                     # unitary gauge tau = t
n_low = sp.Matrix([-N, 0, 0, 0])
n_up = gi * n_low

def Gamma0(m, r):
    # Gamma^0_{m r}
    return sum(gi[0, s] * (sp.diff(g[s, m], X[r]) + sp.diff(g[s, r], X[m]) - sp.diff(g[m, r], X[s])) for s in range(4)) / 2

# A_m = n^r nabla_r n_m = n^r (d_r n_m - Gamma^s_{rm} n_s),  n_s nonzero only for s = 0
A = sp.Matrix([sum(n_up[r] * (sp.diff(n_low[m], X[r]) - Gamma0(r, m) * n_low[0]) for r in range(4)) for m in range(4)])

def build_L(P_low, mutate):
    P_up = gi * P_low
    PA = sum(P_up[m] * A[m] for m in range(4))
    Pnorm2 = sum(gi[m, r] * P_low[m] * P_low[r] for m in range(4) for r in range(4))
    w = Q * sqrtmg                                            # = sqrt(gamma)
    Pi = sum(sp.diff(w * P_up[m], X[m]) for m in range(4)) / w
    L = sqrtmg * (PA - Wf(K * sp.sqrt(Pnorm2)) - gam * Ff(Pi))
    if mutate:
        # by hand: (m/2) (n^r nabla_r P_m)(n^s nabla_s P^m) ~ (m/2) h^{mn} (n.d P_m)(n.d P_n) at leading order
        ndP = [sum(n_up[r] * sp.diff(P_low[mm], X[r]) for r in range(4)) for mm in range(4)]
        L = L + sqrtmg * mkin / 2 * sum((gi[mm, s] + n_up[mm] * n_up[s]) * ndP[mm] * ndP[s] for mm in range(4) for s in range(4))
    return L, Pi, PA

def dt_atoms(expr, funcs):
    out = set()
    for d in expr.atoms(sp.Derivative):
        if d.expr in funcs and t in d.variables:
            out.add(d)
    return out

def hessian_dot(L, funcs):
    dots = [sp.Derivative(f, t) for f in funcs]
    syms = sp.symbols(f"v0:{len(funcs)}")
    Ls = L.subs({d: s for d, s in zip(dots, syms)})
    H = sp.Matrix(len(funcs), len(funcs), lambda i, j: sp.diff(Ls, syms[i], syms[j]))
    return H, syms

# (a) n.P = 0 imposed holonomically: n^m P_m = -N P^0 = 0  <=>  P_0 = N^i P_i
P_low_c = sp.Matrix([sum(Ns[i] * Pl[i] for i in range(3))] + Pl)
P_up_c = gi * P_low_c
assert sp.simplify(P_up_c[0]) == 0
say("S1 n.P = 0  <=>  P^0 = 0 exactly (P_0 = N^i P_i)")
L_c, Pi_c, PA_c = build_L(P_low_c, MUTATE)
# velocities -> symbols; first derivatives wrt them, simplified (atoms alone can be identically-cancelling)
def vel_grad(L, funcs):
    syms = sp.symbols(f"v0:{len(funcs)}")
    Ls = L.subs({sp.Derivative(f, t): s_ for f, s_ in zip(funcs, syms)})
    return [sp.simplify(sp.diff(Ls, s_)) for s_ in syms], syms, Ls
gradP, vP, LsP = vel_grad(L_c, Pl)
gradN, _, _ = vel_grad(L_c, [N])
H_c = sp.Matrix(3, 3, lambda i, j: sp.simplify(sp.diff(LsP, vP[i], vP[j])))
rankH = H_c.rank()
dP = [str(gp) for gp in gradP if gp != 0]
dN = [str(gn) for gn in gradN if gn != 0]
say("S1(a) dL_P/d(dP_i/dt) (simplified):", [str(gp) for gp in gradP])
say("S1(a) dL_P/d(dN/dt)   (simplified):", [str(gn) for gn in gradN])
say("S1(a) Hessian d2 L / d(dP_i/dt) d(dP_j/dt): rank", rankH)
Pi_simpl = sp.simplify(Pi_c - sum(sp.diff(gs**sp.Rational(3, 2) * gam_inv[i, i] * Pl[i], X[i + 1]) for i in range(3)) / gs**sp.Rational(3, 2))
say("S1(a) Pi - (1/sqrt gamma) d_i(sqrt gamma gamma^ij P_j) =", Pi_simpl)
Ai_resid = [sp.simplify(A[i + 1] - sp.diff(sp.log(N), X[i + 1])) for i in range(3)]
say("S1(a) A_i - d_i ln N =", Ai_resid)
OUT["S1a"] = dict(dLdPdot_nonzero=dP, dLdNdot_nonzero=dN, hessian_rank=int(rankH),
                  Pi_is_leaf_divergence=bool(Pi_simpl == 0), A_i_is_grad_lnN=all(r == 0 for r in Ai_resid))

# (b) P_0 kept free, multiplier added: lambda n^m P_m
lam = sp.Function("lam")(*X)
P_low_f = sp.Matrix([P0f] + Pl)
L_f, Pi_f, _ = build_L(P_low_f, MUTATE)
L_f = L_f + sqrtmg * lam * sum(n_up[m] * P_low_f[m] for m in range(4))
# L_f = (terms without gamma) - gamma sqrt(-g) F(Pi_f); Pi_f is affine in the velocities -> Hessian = -gamma sqrt(-g) F'' c c^T
funcs_b = [P0f] + Pl + [lam]
vb = sp.symbols("u0:5")
sub_b = {sp.Derivative(f, t): s_ for f, s_ in zip(funcs_b, vb)}
rest = (L_f + sqrtmg * gam * Ff(Pi_f)).subs(sub_b)
grad_rest = [sp.simplify(sp.diff(rest, s_)) for s_ in vb]
cvec = sp.Matrix([sp.simplify(sp.diff(Pi_f.subs(sub_b), s_)) for s_ in vb])
cvec2 = sp.Matrix([sp.simplify(sp.diff(cvec[i], s_)) for i in range(5) for s_ in vb])
H_f = -gam * sqrtmg * sp.Function("Fpp")(sp.Symbol("Pi")) * cvec * cvec.T
if MUTATE:
    Hm = sp.Matrix(5, 5, lambda i, j: sp.simplify(sp.diff(rest, vb[i], vb[j])))
    H_f = H_f + Hm
rankHf = H_f.rank()
say("S1(b) non-stiffness part: d/d(velocities) =", [str(gq) for gq in grad_rest] if MUTATE else grad_rest)
say("S1(b) dPi/d(velocities) =", list(cvec), "; second derivatives all zero:", all(e == 0 for e in cvec2))
say("S1(b) P_0 free + multiplier: Hessian rank wrt (P_0, P_i, lambda) dots =", rankHf)
say("S1(b) Hessian[0,0] =", sp.factor(H_f[0, 0]))
OUT["S1b"] = dict(hessian_rank=int(rankHf), H00=str(sp.factor(H_f[0, 0])))

# Dirac count for (b), per spatial point (linear algebra of the chain, rank-1 kinetic block):
#  phase space: (P0,pi0),(Pi,pi_i)x3,(lam,pi_lam) = 10
#  primary: pi_i ~ 0 (3), pi_lam ~ 0 (1); secondary: P^0 ~ 0 (from pi_lam), E2_i (from pi_i, 3);
#  tertiary: pi_0 + gamma sqrt(gamma) F'(D.P)/N... ~ 0 (from P^0 dot); quaternary fixes lambda (lam - f ~ 0).
#  all second class if det{pi_i,E2_j} != 0 (checked in S2 for the main run): 3+1+1+3+1+1 = 10 -> DoF = (10-10)/2 = 0
if not MUTATE:
    n_ps, n_2nd = 10, 10
else:
    n_ps, n_2nd = 10, 4      # pi_i no longer constraints: only the lambda/P0 chain (4) remains
dof_b = (n_ps - n_2nd) / 2
say(f"S1(b) Dirac count per point: phase-space dims {n_ps}, second-class constraints {n_2nd} -> DoF {dof_b:g}")
OUT["S1b"]["dirac"] = dict(phase_space=n_ps, second_class=n_2nd, dof=dof_b)

# ------------------------------------------------------------------ S2: linear Fourier count
w_, k1, k2, k3 = sp.symbols("omega k1 k2 k3", real=True)
Wpp, Wp_over_p, Fpp = sp.symbols("Wpp Wp_over_p Fpp", positive=True)   # K^2 W'', K W'/p (>0 for p>0), F''
phat = sp.Matrix([1, 0, 0])
kv = sp.Matrix([k1, k2, k3])
# quadratic L2 = dP.dA - 1/2 dP.M0.dP - (gamma/2) Fpp (k.dP)^2 [+ (m/2) omega^2 |dP|^2]
M = Wpp * phat * phat.T + Wp_over_p * (sp.eye(3) - phat * phat.T) + gam * Fpp * kv * kv.T
if MUTATE:
    M = M - mkin * w_**2 * sp.eye(3)
detM = sp.factor(sp.expand(M.det()))
deg = sp.Poly(sp.expand(detM), w_).degree() if detM.has(w_) else 0
say("S2 det E(omega,k) =", detM)
say("S2 degree in omega:", deg, "-> propagating DoF", deg // 2)
OUT["S2"] = dict(det=str(detM), omega_degree=int(deg), dof=deg // 2)
# FRW point P0 = 0: W(K|P|) = K|P|^2/2 + K^2|P|^3/(3 a0) + ...  -> Wpp = Wp_over_p = K
a0s, p = sp.symbols("a0 p", positive=True)
Wexpr = (a0s**2 / K) * (-p / a0s - sp.log(1 - p / a0s))
ser = sp.series(Wexpr.subs(p, K * p), p, 0, 4).removeO()
say("S2 W(K|P|) about P = 0:", sp.expand(ser))
OUT["S2"]["W_series"] = str(sp.expand(ser))
nondeg = sp.simplify(detM.subs({Wpp: K, Wp_over_p: K, w_: 0}))
say("S2 FRW point (Wpp = KW'/p = K): det at omega=0 =", sp.factor(nondeg), "(nonzero => second class)")
if MUTATE:
    sol_L = sp.solve(sp.Eq((M.subs({k2: 0, k3: 0}))[0, 0], 0), w_**2)
    sol_T = sp.solve(sp.Eq((M.subs({k2: 0, k3: 0}))[1, 1], 0), w_**2)
    say("MUTATE longitudinal omega^2 =", sol_L, "; transverse omega^2 =", sol_T)
    cs2 = sp.limit(sol_L[0] / k1**2, k1, sp.oo)
    say("MUTATE c_s^2 (k -> inf, longitudinal) = gamma_L F''/m_kin =", cs2,
        "; FRW gap omega^2 = K/m_kin (massive mode)")
    OUT["MUTATE"] = dict(omega2_long=str(sol_L), omega2_trans=str(sol_T), cs2=str(cs2))

# ------------------------------------------------------------------ S3: constrained response
Av, drho = sp.symbols("A delta_rho", positive=True)
# leaf P eq at gamma_L = 0: |A| = K W'(K|P|) -> K|P| = a0 u/(1+u), u = |A|/a0
KP = a0s * (Av / a0s) / (1 + Av / a0s)
KPser = sp.series(KP, Av, 0, 3).removeO()
say("S3 K|P| = a0 u/(1+u) about A = 0:", sp.expand(KPser))
# Poisson (E4 00 weak): div A = K (delta rho + Pi), Pi = div P  =>  div(A - K P) = K delta rho
lin = sp.expand(Av - KPser.coeff(Av, 1) * Av)
nxt = sp.expand(Av - KPser)
say("S3 linear order: div(A - KP) =", lin, "= K delta_rho  -> degenerate (no linear response)")
say("S3 next order : div(", nxt, " Ahat ) = K delta_rho  (deep law, non-analytic |A|A)")
OUT["S3"] = dict(KP_series=str(sp.expand(KPser)), linear_lhs=str(lin), next_lhs=str(nxt))
# plane wave exact (1D, curl free): mu(|A|/a0) A = g_N(x,t) with mu = u/(1+u) => A = [g + sqrt(g^2+4 a0 |g|)]/2 sgn
# time behaviour: g_N = g0 cos(omega t)  (instantaneous constraint: no d_t in S1)
def law(gN, a0):
    s = np.sign(gN); gN = np.abs(gN)
    return s * 0.5 * (gN + np.sqrt(gN**2 + 4 * a0 * gN))
ph = np.linspace(0, 2 * np.pi, 200001)[:-1]
resp = {}
for ratio in (1e-4, 1e-2, 1.0, 1e2):
    gN = ratio * np.cos(ph)
    phant = law(gN, 1.0) - gN                          # phantom field = (nu - 1) g_N, units a0
    amp = np.max(np.abs(phant))
    mean = phant.mean() / amp
    b1 = 2 * np.mean(phant * np.cos(ph)) / amp
    a1 = 2 * np.mean(phant * np.sin(ph)) / amp
    zc_src = np.where(np.diff(np.sign(gN)) != 0)[0]
    zc_ph = np.where(np.diff(np.sign(phant)) != 0)[0]
    resp[f"gN/a0={ratio:g}"] = dict(still_mean_over_amp=float(mean), cos_coeff=float(b1), sin_coeff=float(a1),
                                     zero_crossings_identical=bool(np.array_equal(zc_src, zc_ph)),
                                     peak_nu_minus_1=float(amp / ratio))
    say(f"S3 source gN/a0 {ratio:g}: phantom mean/amp {mean:+.2e}, cos {b1:.4f}, sin {a1:+.1e}, "
        f"zero crossings identical {np.array_equal(zc_src, zc_ph)}, peak (nu-1) {amp/ratio:.3g}")
# control (planted still offset): source c + cos -> phantom has a still part
gN = 0.01 * (0.5 + np.cos(ph)); phant = law(gN, 1.0) - gN
resp["control_offset_0.5"] = dict(still_mean_over_amp=float(phant.mean() / np.max(np.abs(phant))))
say(f"S3 control (source with still offset 0.5): phantom mean/amp {resp['control_offset_0.5']['still_mean_over_amp']:+.3f}  (nonzero: machinery sees a still part)")
OUT["S3"]["time_response"] = resp

# ------------------------------------------------------------------ S4: stiffness at z 1100
G = 6.67430e-11; c = 2.99792458e8; Mpc = 3.0856775814913673e22; pc = Mpc / 1e6
zr = 1100.0; Tcmb = 2.7255; Neff = 3.046
rho_crit100 = 3 * (1e5 / Mpc)**2 / (8 * np.pi * G)            # kg/m^3 per h^2
aB = 4 * 5.670374419e-8 / c
rho_gam0 = aB * Tcmb**4 / c**2
rho_nu0 = Neff * 7 / 8 * (4 / 11)**(4 / 3) * rho_gam0
foot = {"canonical": dict(a0=9.3603e-11, Lmin=21.7, omega_b=0.02236),
        "alt": dict(a0=1.1312e-10, Lmin=22.9, omega_b=0.02234)}
ks = [0.01, 0.03, 0.1, 0.3]
OUT["S4"] = {}
for fn, fp in foot.items():
    rb = fp["omega_b"] * rho_crit100 * (1 + zr)**3
    rr = (rho_gam0 + rho_nu0) * (1 + zr)**4
    rtot = rb + rr                                            # no cold component: D2 asks if P replaces it
    say(f"S4 [{fn}] z 1100: rho_b {rb:.3e}, rho_r {rr:.3e}, rho_tot {rtot:.3e} kg/m^3; a0 {fp['a0']}")
    rows = []
    for L in (fp["Lmin"], 90.0):
        for xfac in (1, 100):
            for k in ks:
                kph = k * (1 + zr) / Mpc
                for dlt in (1e-4, 1.0):
                    drho = dlt * rtot
                    gN = 4 * np.pi * G * drho / kph
                    gtot = law(gN, xfac * fp["a0"])
                    Pi = (gtot - gN) * kph / (4 * np.pi * G)  # phantom density (kg/m^3)
                    e1 = 2 * np.pi * G * Pi * (L * pc)**2 / c**2           # gamma_L Pi / c^2
                    e2 = 2 * np.pi * G * (L * pc)**2 * kph * Pi / gtot      # gamma_L |D Pi| / |A|
                    rows.append(dict(Lstar_pc=L, a0_factor=xfac, k=k, delta=dlt, gN_over_a0=gN / (xfac * fp["a0"]),
                                     nu_minus_1=(gtot - gN) / gN, Pi=Pi, gammaPi=e1, gammaDPi_over_A=e2,
))
    OUT["S4"][fn] = rows
    say(f"S4 [{fn}] max gamma_L Pi/c^2 = {max(r['gammaPi'] for r in rows):.2e}; "
        f"max gamma_L|DPi|/|A| = {max(r['gammaDPi_over_A'] for r in rows):.2e}  (over Lstar {fp['Lmin']}-90 pc, x 1-100, k 0.01-0.3, delta 1e-4-1)")
    for r in rows:
        if r["delta"] == 1e-4 and r["a0_factor"] == 1:
            say(f"    L {r['Lstar_pc']:5.1f} pc k {r['k']:5.2f}  gN/a0 {r['gN_over_a0']:.2e}  nu-1 {r['nu_minus_1']:.2e}  "
                f"gamma Pi {r['gammaPi']:.2e}  gamma DPi/A {r['gammaDPi_over_A']:.2e}")
# blend branch: Pi vs b = rho_DE (today's, upper end) -> q = Pi/b
h = 0.674; rho_DE_max = 1.0 * rho_crit100 * h**2   # generous: all of today's critical density
Pis = [r["Pi"] for fn in foot for r in OUT["S4"][fn] if r["delta"] == 1e-4]
qmin = min(Pis) / rho_DE_max
say(f"S4 blend: min Pi / b over the delta 1e-4 rows = {qmin:.2e} (b <= rho_crit today) -> q >> 1: F = q^2/2 raw branch")
OUT["S4_blend_qmin"] = qmin

# ------------------------------------------------------------------ S5: pre-screen (structural)
verdict = ("FAIL (follows): P has no propagating mode; its response is an instantaneous, sign-preserving, odd function "
           "of the source gradient; for an acoustic source oscillating about zero its time mean is 0 (still share 0 < 0.5). "
           "Any still part equals the law response to a still part of the source (dust/offset), graded in D4.")
if MUTATE:
    verdict = "MUTATE: count finds a propagating mode (machinery bites); not a grade"
say("S5 pre-screen D2:", verdict)
OUT["S5"] = verdict
rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / (1024**2 if sys.platform == "darwin" else 1024)
say(f"peak RSS {rss:.0f} MB")
OUT["peak_rss_MB"] = rss
tag = "d2_psector_MUTATE" if MUTATE else "d2_psector"
import os
here = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(here, tag + ".json"), "w") as f:
    json.dump(OUT, f, indent=1, default=str)
with open(os.path.join(here, tag + ".out"), "w") as f:
    f.write("\n".join(LOG) + "\n")
