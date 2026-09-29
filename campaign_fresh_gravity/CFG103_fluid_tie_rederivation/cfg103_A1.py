"""
CFG103-A1 -- independent re-derivation of CFG43-A1 (own code).  FROZEN criteria are in FROZEN_DOCSTRING.txt (sha256 in FROZEN_HASH.txt).
Action  S = Int{ sqrt(-g)[(Mp2/2)R - Mp2 L] + Mp2 L d_m T^m - sqrt(-g) rho(n;L) + J^m d_m theta },
        n = sqrt(-g_mn J^m J^n)/sqrt(-g),  rho = m n + Pcap x atan x,  x = m n/(nu* Mp2 L),  Pcap = eps Mp2 L,  eps = kappa^2/8pi.
(i)   sympy Euler-Lagrange in 3+1 with a diagonal metric; metric variation checked against the perfect fluid, P = n rho_n - rho.
(ii)  linearised dispersion (flat, 1+1): gcd of the maximal minors of the plane-wave matrix -> the propagating modes.
(iii) Dirac-Bergmann on a periodic lattice of N sites (own numerical Poisson-bracket rank code): fluid, fluid+HT, MUTATE1 scalar.
MUTATE=1: the multiplier sector is replaced by a dynamical scalar psi (L=U(psi)), fluid still reads U(psi): expect extra local dof.
MUTATE=2: tie dropped (cap reads an independent constant Lc): H-TIE (a0^2 = kappa^2 L/8pi) and the clock identity must FAIL.
"""
import os, sys, itertools
import numpy as np, sympy as sp
from scipy.optimize import least_squares
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cfg103_common import Log, MUTATE

log = Log(__file__)
rng = np.random.default_rng(20260929)

# ---------------------------------------------------------------- symbols / EOS
Mp2, m, nus, kap = sp.symbols("Mp2 m nu_s kappa", positive=True)
eps = kap**2 / (8 * sp.pi)
nn, LL = sp.symbols("nn LL", positive=True)          # dummy arguments of rho(n; Lambda)
Lc = sp.Symbol("Lc", positive=True)                  # MUTATE2: independent constant read by the cap
Lcap = Lc if MUTATE == 2 else LL                     # what the cap reads
Pcap = eps * Mp2 * Lcap
xx = m * nn / (nus * Mp2 * Lcap)
rho = m * nn + Pcap * xx * sp.atan(xx)
rho_n = sp.diff(rho, nn)
Pex = sp.simplify(nn * rho_n - rho)
rho_L = sp.diff(rho, LL)

# ---------------------------------------------------------------- (i) covariant EL
t, x, y, z = coords = sp.symbols("t x y z")
def F(nm): return sp.Function(nm)(*coords)
Lam = F("Lam"); T = [F("T%d" % i) for i in range(4)]; th = F("th"); J = [F("J%d" % i) for i in range(4)]
A_, B_, C_, D_ = F("A"), F("B"), F("C"), F("D")      # metric diag(-A^2, B^2, C^2, D^2)
sg = A_ * B_ * C_ * D_
s2 = A_**2 * J[0]**2 - B_**2 * J[1]**2 - C_**2 * J[2]**2 - D_**2 * J[3]**2
sroot = sp.sqrt(s2)
nfield = sroot / sg
Lag = (Mp2 * Lam * sum(sp.diff(T[i], coords[i]) for i in range(4)) - sg * Mp2 * Lam
       - sg * rho.subs({nn: nfield, LL: Lam}) + sum(J[i] * sp.diff(th, coords[i]) for i in range(4)))
from sympy.calculus.euler import euler_equations
fields = [Lam] + T + [th] + J
EL = euler_equations(Lag, fields, coords)
EL = [e.lhs - e.rhs for e in EL]

def numsub(expr, seed):
    """replace every Derivative and applied function by random numbers (consistent within one call), Mp2 etc. by numbers"""
    r = np.random.default_rng(seed)
    ders = sorted(expr.atoms(sp.Derivative), key=str)
    rep = {d: float(r.uniform(0.3, 1.3)) for d in ders}
    e = expr.xreplace(rep)
    funcs = sorted(e.atoms(sp.core.function.AppliedUndef), key=str)
    rep2 = {f: float(r.uniform(0.6, 1.4)) for f in funcs}
    return e.xreplace(rep2)

par = {Mp2: 1.3, m: 0.9, nus: 2.7, kap: 0.5, Lc: 0.37}
def numeq(a, b, seed, tol=1e-9, extra=None):
    d = (a - b)
    # force a common substitution: build one dict from the union of atoms
    U = sp.Add(a, b)
    r = np.random.default_rng(seed)
    ders = sorted(U.atoms(sp.Derivative), key=str); rep = {d_: float(r.uniform(0.3, 1.3)) for d_ in ders}
    e = d.xreplace(rep)
    Uf = sp.Add(a.xreplace(rep), b.xreplace(rep))
    funcs = sorted(Uf.atoms(sp.core.function.AppliedUndef), key=str); rep2 = {f: float(r.uniform(0.6, 1.4)) for f in funcs}
    e = e.xreplace(rep2)
    val = complex(sp.N(e.subs(par)))
    return abs(val), abs(complex(sp.N(a.xreplace(rep).xreplace(rep2).subs(par))))

def relerr(a, b, seeds=(1, 2, 3)):
    worst = 0.0
    for s in seeds:
        ab, sc = numeq(a, b, s); worst = max(worst, ab / max(1.0, sc))
    return worst

# E_T:  Mp2 d_m Lam = 0   (EL for T^m gives -Mp2 d_m Lam)
ET = EL[1:5]
errT = max(relerr(ET[i], -Mp2 * sp.diff(Lam, coords[i])) for i in range(4))
log.check("E_T: d_m Lam = 0 (EL wrt T^m)", errT < 1e-10, "max err %.2e" % errT)

# E_Lam:  Mp2 d_mT^m - sg Mp2 - sg rho_L|_n = 0 ;  claim  rho_L|_n = -P/Lam  =>  d_mT^m = sg (1 - P/(Mp2 Lam))
EL_Lam = EL[0]
Pf = Pex.subs({nn: nfield, LL: Lam})
divT = sum(sp.diff(T[i], coords[i]) for i in range(4))
expect_clock = Mp2 * divT - sg * Mp2 * (1 - Pf / (Mp2 * Lam))
errL = relerr(EL_Lam, expect_clock)
log.check("H-CLOCK: E_Lam <=> d_mT^m = sg(1-P/(Mp2 Lam))", errL < 1e-9, "max err %.2e   (rho_L|_n = -P/Lam identity, MUTATE=%d)" % (errL, MUTATE))
# symbolic homogeneity identity  rho_L|_n = -P/Lam  (only true when the cap reads the HT Lambda)
hom = sp.simplify((rho_L + Pex / LL)) if MUTATE != 2 else sp.simplify(rho_L + Pex / LL)
log.check("rho_Lam|_n = -P/Lam (symbolic)", hom == 0 if MUTATE != 2 else hom == 0, "residual: %s" % str(hom)[:60])

# E_theta / E_J
Eth = EL[5]; errth = relerr(Eth, -sum(sp.diff(J[i], coords[i]) for i in range(4)))
log.check("E_theta: d_m J^m = 0", errth < 1e-10, "%.2e" % errth)
metric = [-A_**2, B_**2, C_**2, D_**2]
rn_f = rho_n.subs({nn: nfield, LL: Lam})
uL = [metric[i] * J[i] / sroot for i in range(4)]        # u_m = g_mn J^n / s
errJ = max(relerr(EL[6 + i], sp.diff(th, coords[i]) + rn_f * uL[i]) for i in range(4))
log.check("E_J: d_m theta = -rho_n u_m (irrotational)", errJ < 1e-9, "%.2e" % errJ)

# metric variation: T^{mn} = (2/sqrt(-g)) dL_m/dg_mn, L_m = -sqrt(-g) rho(n;Lam), 10 independent components
gs = sp.Matrix(4, 4, lambda i, j: sp.Symbol("g%d%d" % (min(i, j), max(i, j))))
Js = sp.symbols("j0:4"); detg = gs.det(); sgm = sp.sqrt(-detg)
sJ = sp.sqrt(-sum(gs[i, j] * Js[i] * Js[j] for i in range(4) for j in range(4)))
nm = sJ / sgm
Lm = -sgm * rho.subs({nn: nm})
gval = np.diag([-1.0, 1, 1, 1]) + 0.05 * rng.standard_normal((4, 4)); gval = (gval + gval.T) / 2
jval = [1.1, 0.2, -0.15, 0.1]
sub = {gs[i, j]: gval[i, j] for i in range(4) for j in range(i, 4)}; sub.update({Js[i]: jval[i] for i in range(4)}); sub.update({LL: 0.8, **par})
Tmn_var = sp.zeros(4, 4)
for i in range(4):
    for j in range(i, 4):
        d = sp.diff(Lm, sp.Symbol("g%d%d" % (i, j)))
        fac = 2 if i == j else 1                       # off-diagonal symbol appears twice
        Tmn_var[i, j] = Tmn_var[j, i] = complex(sp.N((fac * d / sgm).subs(sub))).real if False else float(sp.N((fac * d / sgm).subs(sub)))
ginv = np.linalg.inv(gval); s_num = np.sqrt(-np.einsum("i,ij,j", jval, gval, jval)); sg_num = np.sqrt(-np.linalg.det(gval))
n_num = float(s_num / sg_num); u_up = np.array(jval) / s_num
rho_num = float(rho.subs({nn: n_num, **par, LL: 0.8})); P_num = float(Pex.subs({nn: n_num, **par, LL: 0.8}))
Tperf = (rho_num + P_num) * np.outer(u_up, u_up) + P_num * ginv
errg = np.max(np.abs(np.array(Tmn_var, dtype=float) - Tperf))
log.check("metric variation = perfect fluid, P=n rho_n-rho", errg < 1e-9, "max |dT| = %.2e" % errg)

# EOS statement (Lean): P = Pcap x^2/(1+x^2)
P_claim = Pcap * xx**2 / (1 + xx**2)
log.check("EOS: P = Pcap x^2/(1+x^2) (symbolic)", sp.simplify(Pex - P_claim) == 0, "")

# ---------------------------------------------------------------- tie / H-TIE
G = sp.Symbol("G", positive=True); Lam_s = sp.Symbol("Lam_s", positive=True)
Pcap_here = (kap**2 / (8 * sp.pi)) * (1 / (8 * sp.pi * G)) * (Lc if MUTATE == 2 else Lam_s)   # Mp2 = 1/(8 pi G)
a0sq = 8 * sp.pi * G * Pcap_here
tie = sp.simplify(a0sq - kap**2 * Lam_s / (8 * sp.pi))
log.check("H-TIE: a0^2 = 8piG Pcap = kappa^2 L/(8pi)", tie == 0, "difference: %s" % tie)

# ---------------------------------------------------------------- (ii) dispersion (flat 1+1)
w, k, e = sp.symbols("omega k e")
n0, mu, tau = sp.symbols("nbar mu tau", positive=True)
r_n, r_nn, r_L, r_LL, r_nL, Lb = sp.symbols("r_n r_nn r_L r_LL r_nL Lbar")
tt, xs = sp.symbols("tt xs")
def f2(nm): return sp.Function(nm)(tt, xs)
lam, dT0, dT1, dth, j0, j1, dpsi = [f2(s) for s in ("lam", "dT0", "dT1", "dth", "j0", "j1", "dpsi")]
dn = e * j0 - e**2 * j1**2 / (2 * n0)
dLam = e * lam
rho2 = r_n * dn + r_L * dLam + sp.Rational(1, 2) * (r_nn * dn**2 + 2 * r_nL * dn * dLam + r_LL * dLam**2)
if MUTATE != 1:
    L_full = (Mp2 * (Lb + e * lam) * (tau + e * (sp.diff(dT0, tt) + sp.diff(dT1, xs))) - Mp2 * (Lb + e * lam) - rho2
              + (n0 + e * j0) * (mu + e * sp.diff(dth, tt)) + e * j1 * e * sp.diff(dth, xs))
    flds = [lam, dT0, dT1, dth, j0, j1]
else:
    mpsi = sp.Symbol("m_psi2", positive=True)                       # U = U0 + m_psi2 psi^2/2 (static background, U'(psi0)=0)
    dLam_m = sp.Rational(1, 2) * mpsi * e**2 * dpsi**2
    rho2m = r_n * dn + r_L * dLam_m + sp.Rational(1, 2) * r_nn * dn**2
    L_full = (Mp2 * e**2 * sp.Rational(1, 2) * (sp.diff(dpsi, tt)**2 - sp.diff(dpsi, xs)**2) - Mp2 * dLam_m - rho2m
              + (n0 + e * j0) * (mu + e * sp.diff(dth, tt)) + e * j1 * e * sp.diff(dth, xs))
    flds = [dpsi, dth, j0, j1]
L2 = sp.expand(sp.diff(L_full, e, 2).subs(e, 0) / 2)
ELs = [q.lhs - q.rhs for q in euler_equations(L2, flds, [tt, xs])]
amps = sp.symbols("a0:%d" % len(flds)); wave = sp.exp(sp.I * (k * xs - w * tt))
Msys = sp.zeros(len(flds), len(flds))
for r_i, eq in enumerate(ELs):
    ex = eq.subs({f: a * wave for f, a in zip(flds, amps)}).doit()
    ex = sp.expand(sp.simplify(ex / wave))
    for c_i, a in enumerate(amps): Msys[r_i, c_i] = sp.expand(ex.coeff(a))
N_ = len(flds)
minors = []
for rows in itertools.combinations(range(N_), N_ - 1):
    for cols in itertools.combinations(range(N_), N_ - 1):
        mn_ = sp.factor(Msys.extract(list(rows), list(cols)).det())
        if mn_ != 0: minors.append(mn_)
detM = sp.factor(Msys.det())
if detM != 0:
    g = detM                                           # regular (gauge-free) system: propagating polynomial = det
else:
    g = minors[0]                                      # gauge-degenerate system (HT): gcd of the maximal non-vanishing minors
    for mn_ in minors[1:]: g = sp.gcd(g, mn_)
g = sp.factor(g)
cs2 = n0 * r_nn / r_n
w_roots = sorted(set(sp.solve(sp.Poly(sp.together(g), w), w)), key=str) if g.has(w) else []
log.p("   MUTATE=%d  gcd of maximal minors (propagating-mode polynomial): %s" % (MUTATE, g))
log.p("   roots in omega:", w_roots)
nroot_w = sp.degree(sp.Poly(sp.together(g), w), w) if g.has(w) else 0
log.check("propagating modes = the fluid sound pair only", nroot_w == 2 and sp.simplify(g.subs(w, sp.sqrt(cs2) * k)) == 0,
          "omega-degree %d (2 = one sound mode); c_s^2 = nbar r_nn/r_n (independent of r_L, r_LL, r_nL)" % nroot_w)
if MUTATE != 1:
    degs = [sp.Poly(Msys[r_i, 0], w, k).total_degree() if Msys[r_i, 0] != 0 else 0 for r_i in range(N_)]
    degs_row = [sp.Poly(Msys[0, c_i], w, k).total_degree() if Msys[0, c_i] != 0 else 0 for c_i in range(N_)]
    log.check("delta Lambda: no wave operator", max(degs + degs_row) <= 1 and Msys[0, 0] == -r_LL,
              "max (omega,k)-degree in the delta-Lambda row/column = %d (first order only); (lam,lam) entry = %s" % (max(degs + degs_row), Msys[0, 0]))

# ---------------------------------------------------------------- (iii) Dirac-Bergmann lattice
def dirac_count(N, mode):
    """mode 'fluid' | 'HT' | 'scalar'.  periodic 1-D lattice, flat background, unit lapse.  Returns dict of counts."""
    q, v = [], []
    S = lambda nm, i: sp.Symbol("%s_%d" % (nm, i))
    Mp2v, mv, nusv, epsv, Lc0, lam_ = 1.0, 1.0, 3.0, 0.02, 0.9, 0.7
    Ux = lambda ps: Lc0 * sp.exp(-lam_ * ps)
    for i in range(N):
        for nm in (["T0", "T1", "Lam"] if mode == "HT" else (["psi"] if mode == "scalar" else [])) + ["th", "J0", "J1"]:
            q.append(S(nm, i)); v.append(S("v" + nm, i))
    Lag_ = 0
    for i in range(N):
        i1 = (i + 1) % N
        J0, J1, thi, thn = S("J0", i), S("J1", i), S("th", i), S("th", i1)
        if mode == "HT":
            Lamx = S("Lam", i)
            Lag_ += Mp2v * Lamx * (S("vT0", i) + S("T1", i1) - S("T1", i)) - Mp2v * Lamx
        elif mode == "scalar":
            Lamx = Ux(S("psi", i))
            Lag_ += Mp2v / 2 * S("vpsi", i)**2 - Mp2v / 2 * (S("psi", i1) - S("psi", i))**2 - Mp2v * Lamx
        else:
            Lamx = Lc0; Lag_ += -Mp2v * Lamx
        nx = sp.sqrt(J0**2 - J1**2)
        xr = mv * nx / (nusv * Mp2v * Lamx)
        rh = mv * nx + epsv * Mp2v * Lamx * xr * sp.atan(xr)
        Lag_ += -rh + J0 * S("vth", i) + J1 * (thn - thi)
    nq = len(q); p = [sp.Symbol("p" + str(qq)) for qq in q]
    pexpr = [sp.diff(Lag_, vv) for vv in v]
    prim, Hc = [], 0
    subs_v0 = {}
    for qq, vv, pp, pe in zip(q, v, p, pexpr):
        if not pe.has(vv): prim.append(pp - pe); subs_v0[vv] = 0
    for qq, vv, pp, pe in zip(q, v, p, pexpr):
        if pe.has(vv):        # regular momentum: p = Mp2 v  (scalar)
            subs_v0[vv] = pp / Mp2v
    Hc = sum(pp * subs_v0.get(vv, 0) for pp, vv, pe in zip(p, v, pexpr) if pe.has(vv)) - Lag_.subs(subs_v0)
    Hc = sp.expand(Hc) if False else Hc
    X = q + p
    Om = np.zeros((2 * nq, 2 * nq)); Om[:nq, nq:] = np.eye(nq); Om[nq:, :nq] = -np.eye(nq)
    def jac(exprs): return sp.Matrix(exprs).jacobian(X)
    fJ = lambda M_: sp.lambdify(X, M_, "numpy")
    Jphi_s = jac(prim); Jphi = fJ(Jphi_s)
    gradH = fJ(sp.Matrix([sp.diff(Hc, xx_) for xx_ in X]))
    phi_f = sp.lambdify(X, prim, "numpy")
    npr = len(prim)
    def randq():
        vals = {}
        for i in range(N):
            for nm in ["T0", "T1", "Lam", "th", "psi"]:
                if S(nm, i) in q: vals[S(nm, i)] = rng.uniform(0.3, 1.2)
            vals[S("J0", i)] = rng.uniform(1.0, 2.0); vals[S("J1", i)] = rng.uniform(-0.4, 0.4)
        return np.array([vals[qq] for qq in q])
    def full_x(qv):
        pv = np.zeros(nq)
        ph = np.array(phi_f(*(list(qv) + [0.0] * nq)), dtype=float)   # phi(q,p=0) = -c(q)
        for j, pr in enumerate(prim):
            idx = [pi for pi, pp in enumerate(p) if pr.has(pp)][0]; pv[idx] = -ph[j]      # p = c(q)
        for idx, (vv, pe) in enumerate(zip(v, pexpr)):
            if pe.has(vv): pv[idx] = rng.uniform(-0.5, 0.5)
        return np.concatenate([qv, pv])
    # stage 1: primary bracket matrix (must be point-independent to define constant null vectors)
    Mpp = []
    for _ in range(3):
        xv = full_x(randq()); Jp = np.array(Jphi(*xv), dtype=float); Mpp.append(Jp @ Om @ Jp.T)
    const = max(np.max(np.abs(Mpp[0] - Mpp[j])) for j in (1, 2)) < 1e-12
    uu, ss, vt = np.linalg.svd(Mpp[0]); null = vt[np.sum(ss > 1e-9):]                # null vectors nu (rows)
    hphi = jac(prim) * sp.Matrix(Om) * sp.Matrix([sp.diff(Hc, xx_) for xx_ in X])   # {phi_a, Hc}
    sec = [sp.simplify(sum(float(nu_[a]) * hphi[a] for a in range(npr))) for nu_ in null]
    sec = [s_ for s_ in sec if s_ != 0]
    # numerically distinct nonzero secondaries: drop identically-vanishing ones by sampling
    secf = [sp.lambdify(X, s_, "numpy") for s_ in sec]
    keep = []
    for s_, f_ in zip(sec, secf):
        vals = [abs(float(f_(*full_x(randq())))) for _ in range(4)]
        if max(vals) > 1e-9: keep.append(s_)
    sec = keep
    C = prim + sec
    JC_s = jac(C); JC = fJ(JC_s)
    resid_ter_all, Dvals, FCs, rJs, Rs, frees = [], [], [], [], [], []
    for trial in range(4):
        # find a point on the secondary surface
        secf2 = [sp.lambdify(X, s_, "numpy") for s_ in sec]
        def resfun(qv):
            xv = full_x(qv); return np.array([float(f_(*xv)) for f_ in secf2]) if secf2 else np.zeros(1)
        sol = least_squares(resfun, randq(), xtol=1e-14, ftol=1e-14, gtol=1e-14)
        if np.max(np.abs(resfun(sol.x))) > 1e-9: continue
        xv = full_x(sol.x)
        JCv = np.array(JC(*xv), dtype=float); Mv = JCv @ Om @ JCv.T
        hv = JCv @ Om @ np.array(gradH(*xv), dtype=float).ravel()
        rJ = np.linalg.matrix_rank(JCv, tol=1e-8)
        R = np.linalg.matrix_rank(Mv, tol=1e-8)
        A = Mv[:, :npr]
        u, *_ = np.linalg.lstsq(A, -hv, rcond=None)
        resid = np.linalg.norm(A @ u + hv)
        resid_ter_all.append(resid); rJs.append(rJ); Rs.append(R); FCs.append(rJ - R)
        Dvals.append(2 * nq - 2 * rJ + R); frees.append(npr - np.linalg.matrix_rank(A, tol=1e-8))
    ok = len(Dvals) > 0
    return dict(N=N, mode=mode, nq=nq, n_primary=npr, n_secondary=len(sec), Mpp_const=const, D=Dvals, FC=FCs, rJ=rJs, R=Rs,
                free_mult=frees, tertiary_resid=resid_ter_all, ok=ok)

results = {}
modes = ["fluid", "scalar"] if MUTATE == 1 else ["fluid", "HT"]
if MUTATE == 2: modes = ["fluid", "HT"]
out = {}
for N in (3, 4, 5):
    for md in modes:
        r = dirac_count(N, md)
        out[(N, md)] = r
        log.p("   N=%d %-6s n_q=%d primary=%d secondary=%d  D=%s  first-class=%s  rank(J)=%s rank(bracket)=%s  free multipliers=%s  max consistency residual=%.1e" %
              (N, md, r["nq"], r["n_primary"], r["n_secondary"], sorted(set(r["D"])), sorted(set(r["FC"])), sorted(set(r["rJ"])), sorted(set(r["R"])), sorted(set(r["free_mult"])), max(r["tertiary_resid"]) if r["tertiary_resid"] else -1))
for N in (3, 4, 5):
    Df = set(out[(N, "fluid")]["D"]); other = "scalar" if MUTATE == 1 else "HT"; Do = set(out[(N, other)]["D"])
    log.check("N=%d: D(fluid)=2N" % N, Df == {2 * N}, str(sorted(Df)))
    log.check("N=%d: D(total) = D(fluid)+2 (no new local dof)" % N, Do == {2 * N + 2}, "D(total)=%s, D(fluid)=%s (HT: 2N+2; scalar would give 4N=%d)" % (sorted(Do), sorted(Df), 4 * N))
    if MUTATE != 1:
        log.check("N=%d: no tertiary constraint" % N, max(out[(N, "HT")]["tertiary_resid"]) < 1e-8, "consistency residual %.1e" % max(out[(N, "HT")]["tertiary_resid"]))

results["dirac"] = {"%d_%s" % k_: {kk: (list(map(int, vv)) if isinstance(vv, list) and vv and isinstance(vv[0], (int, np.integer)) else vv) for kk, vv in v_.items() if kk in ("D", "FC", "rJ", "R", "free_mult", "n_primary", "n_secondary")} for k_, v_ in out.items()}
log.finish(results)
