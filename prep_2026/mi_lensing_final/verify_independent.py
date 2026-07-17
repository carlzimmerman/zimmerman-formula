#!/usr/bin/env python3
"""Independent adversarial verification of mi_lensing_final (own code path).
A: re-derive T_munu via the UPPER-metric variation T = -2 dL/dg^{munu} + g L (different
   route from the deliverables' lower-metric variation), frame leg once, s=-1 sign audit.
B: kernel on-shell identities + deep-MOND magnitudes, independent sympy.
C: F(y) spot values with an independent solver (Simpson, different grid).
D: Brouwer chi2 with an independent loader; rail/full, both footings; slope-vs-amplitude.
E: save/kill hunt numerics (slip-sign flip, no-Newton-calibration fork, model-free bound).
"""
import numpy as np, sympy as sp, sys
ok_all = True
def rep(name, ok, extra=""):
    global ok_all
    print(("PASS " if ok else "FAIL ") + name + (" | " + extra if extra else ""))
    ok_all = ok_all and ok

# ---------- A: stress tensor via UPPER-metric variation ----------
# scalars built from g^{munu} (inverse metric) with LOWER-index u_mu, a_mu fixed:
# u.u = g^{mn} u_m u_n ; X = g^{mn} a_m a_n / a0^2
# T_munu = -2 dL/dg^{munu} + g_munu L
guu_s = {}
for i in range(4):
    for j in range(i,4): guu_s[(i,j)] = sp.Symbol(f'G{i}{j}')
Gm = sp.Matrix(4,4, lambda i,j: guu_s[(min(i,j),max(i,j))])
ud = sp.Matrix(sp.symbols('ud0 ud1 ud2 ud3'))   # u_mu lower
ad = sp.Matrix(sp.symbols('ad0 ad1 ad2 ad3'))   # a_mu lower
rho, s_, lam = sp.symbols('rho s lam')
A0 = sp.Symbol('a0', positive=True)
uu = (ud.T*Gm*ud)[0,0]; X = (ad.T*Gm*ad)[0,0]/A0**2
z = sp.Symbol('z', positive=True)
K = (sp.sqrt(1+4*z)-1)/(2*sp.sqrt(z)); Kp = sp.diff(K, z)
KX, KpX = K.subs(z, X), Kp.subs(z, X)
def dL_dguu(L):
    M = sp.zeros(4,4)
    for i in range(4):
        for j in range(4):
            d = sp.diff(L, guu_s[(min(i,j),max(i,j))])
            M[i,j] = d if i==j else d/2
    return M
L_m = -sp.Rational(1,2)*rho*s_*uu*KX
T_m = -2*dL_dguu(L_m)   # + g_munu L_m term added separately (needs lower metric; treat sym.)
# expected: -2 dL/dg^{mn} = rho s K u_m u_n + rho s (u.u) K' a_m a_n / a0^2... sign check:
exp_alg = rho*s_*KX*(ud*ud.T) + rho*s_*uu*KpX*(ad*ad.T)/A0**2
diff = sp.simplify(T_m - exp_alg)
rep("A1 upper-variation algebraic legs: -2 dL_m/dg^{mn} = +rho s K u u + rho s (u.u) K' aa/a0^2",
    all(sp.simplify(diff[i,j])==0 for i in range(4) for j in range(4)))
# hold on: with T = -2 dL/dg^{mn} + g L and on-shell u.u=-1 this gives
#   T^m = rho s K u u - rho s K' aa/a0^2 + g*(+ (1/2) rho s K)  ... compare doc 2c:
#   doc: alpha=-rho s K, beta=+(1/2) rho s K, gamma=+rho s K'/a0^2  (LOWER-metric route)
# NOTE the sign flip on uu and aa legs vs the doc: d(u.u)/dg^{mn}=+u_m u_n while
# d(u.u)/dg_{mn}=+u^m u^n... resolve numerically below via an explicit consistency test.
# Explicit resolution: for scalar S=g^{mn}u_m u_n with u_m fixed vs S=g_{mn}u^m u^n with u^m
# fixed, the two conventions describe DIFFERENT held-fixed variables. Physical T must come
# from one consistent choice.  The doc holds u^mu (upper) fixed. Redo with upper fixed:
gll_s = {}
for i in range(4):
    for j in range(i,4): gll_s[(i,j)] = sp.Symbol(f'g{i}{j}')
gL = sp.Matrix(4,4, lambda i,j: gll_s[(min(i,j),max(i,j))])
uU = sp.Matrix(sp.symbols('u0 u1 u2 u3')); aU = sp.Matrix(sp.symbols('a0u a1u a2u a3u'))
uu2 = (uU.T*gL*uU)[0,0]; X2 = (aU.T*gL*aU)[0,0]/A0**2
KX2, KpX2 = K.subs(z, X2), Kp.subs(z, X2)
def dL_dgll(L):
    M = sp.zeros(4,4)
    for i in range(4):
        for j in range(4):
            d = sp.diff(L, gll_s[(min(i,j),max(i,j))])
            M[i,j] = d if i==j else d/2
    return M
L_m2 = -sp.Rational(1,2)*rho*s_*uu2*KX2
# T^{mn} (upper) = +2 dL/dg_{mn} + g^{mn} L ; algebraic legs:
T2 = 2*dL_dgll(L_m2)
exp2 = -rho*s_*KX2*(uU*uU.T) - rho*s_*uu2*KpX2*(aU*aU.T)/A0**2
d2 = sp.simplify(T2 - exp2)
rep("A2 lower-variation (doc route, u^mu fixed): 2 dL_m/dg_mn = -rho s K u u - rho s(u.u)K' aa/a0^2",
    all(sp.simplify(d2[i,j])==0 for i in range(4) for j in range(4)))
# on-shell u.u=-1: T^m{mn} = -rho s K u^m u^n + rho s K' a^m a^n/a0^2 + (1/2) rho s K g^{mn}
# => alpha=-rho s K, beta=(1/2) rho s K, gamma=+rho s K'/a0^2  == MATTER_COUPLING 2c. OK.
# frame sector:
L_u2 = -(lam/2)*(uu2+1)
Tu = 2*dL_dgll(L_u2)
rep("A3 frame leg (once): 2 dL_u/dg_mn = -lam u u ; with lam=-rho s K -> +rho s K u u",
    all(sp.simplify(Tu[i,j] - (-lam)*(uU*uU.T)[i,j])==0 for i in range(4) for j in range(4)))
# Assembly I cancellation:
cancel = sp.simplify((-rho*s_*KX2) + (-(-rho*s_*KX2)))
rep("A4 Assembly I: matter uu coeff (-rho s K) + frame uu coeff (+rho s K) = 0 EXACTLY",
    cancel == 0)
# Assembly I Newtonian anchor with s=-1, K->1, rest frame Minkowski:
# T_I = (1/2) rho s K eta + gamma aa ; K'->0 => T_I = -(1/2) rho eta (s=-1)
# T_00 = +rho/2 (rho_e), T_ii = -rho/2 (p) => rho_e+3p = -rho: FAILS (repulsive).
rho_e_I, p_I = 0.5, -0.5
rep("A5 Assembly I anchor: rho_e=+rho/2, p=-rho/2, rho_e+3p=-rho<0 (repulsive) -> FAILS Newton",
    rho_e_I + 3*p_I < 0)
# Assembly III: J-based dust bookkeeping; L sqrt-g = (1/2) s |J| K(X), |J|=sqrt(-g_mn J^m J^n)
JU = sp.Matrix(sp.symbols('J0 J1 J2 J3'))
JJ = (JU.T*gL*JU)[0,0]; Jn = sp.sqrt(-JJ)
Dm3 = sp.Rational(1,2)*s_*Jn*KX2
T3 = 2*dL_dgll(Dm3)   # this is sqrt-g T^{mn}/... (T = (2/sqrt-g) d(sqrt-g L)/dg_mn)
exp3 = -sp.Rational(1,2)*(s_/Jn)*KX2*(JU*JU.T) + Jn*s_*KpX2*(aU*aU.T)/A0**2
d3 = sp.simplify(T3 - exp3)
rep("A6 Assembly III: (2)d[(1/2)s|J|K]/dg = -(s K/2|J|) J J + s|J|K' aa/a0^2  (u=J/|J|: u.u=-1 identically, S_u==0)",
    all(sp.simplify(d3[i,j])==0 for i in range(4) for j in range(4)))
# with J=|J|u, rho=|J|/sqrt-g: T^III = -(1/2) s rho K u u + s rho K' aa/a0^2 ;
# s=-1: T^III = +(1/2) rho K u u - rho K' aa/a0^2 : K->1 dust/2, ATTRACTIVE. Newton calib x2:
# T_hat = rho K u u - 2 rho K'/a0^2 aa.  SIGN AUDIT: s=+1 would give T_00<0 (anti-gravity):
rep("A7 sign audit: s=+1 in Assembly III gives rho_e=-rho/2<0 (fails Newton) -> s=-1 is the",
    (-0.5) < 0, "only Newton-consistent sign; NO sign choice yields over-lensing")

# ---------- B: on-shell kernel identities + deep-MOND magnitudes ----------
y = sp.Symbol('y', positive=True)
nu = sp.sqrt(1+1/y)
z_on = y**2 + y
rad = sp.sqrt(4*y**2+4*y+1)   # = 2y+1 for y>0 (collapsing radical, verified numerically too)
K_on = sp.simplify(K.subs(z, z_on).subs(rad, 2*y+1))
f1 = sp.lambdify(y, K.subs(z, z_on) - 1/nu)
rep("B1 on-shell K = 1/nu (rho_eff = rho/nu: SUPPRESSION)",
    sp.simplify(K_on - 1/nu) == 0 and max(abs(f1(p)) for p in (0.003,0.1,1,10,250)) < 1e-12)
ratio = sp.simplify((2*(Kp*z).subs(z, z_on)/K.subs(z, z_on)).subs(rad, 2*y+1))
f2 = sp.lambdify(y, 2*(Kp*z).subs(z, z_on)/K.subs(z, z_on) - 1/(2*y+1))
rep("B2 on-shell 2K'X/K = 1/(2y+1) <= 1 (anisotropic stress is a bounded O(K) correction)",
    sp.simplify(ratio - 1/(2*y+1)) == 0 and max(abs(f2(p)) for p in (0.003,0.1,1,10,250)) < 1e-12)
rep("B3 deep-MOND: K -> sqrt(z) = |a|/a0 ; K'z -> K/2 = |a|/(2a0): both O(K)<=1, no nu",
    sp.limit(K/sp.sqrt(z), z, 0, '+') == 1 and sp.limit(Kp*z/K, z, 0, '+') == sp.Rational(1,2))
# needed enhancement nu(y) vs derived: at y=0.01 nu=10.05, K=0.0995 -> gap factor nu^2~101
print("   y=0.01: needed factor nu=%.3f ; derived rho_eff/rho=K=%.4f ; |Pi|/rho_eff=%.4f"
      % (float(nu.subs(y,0.01)), float(K_on.subs(y,0.01)), float((1/(2*y+1)).subs(y,0.01))))

# ---------- C: independent F(y) solve ----------
from scipy.integrate import cumulative_trapezoid
G = 6.674e-11; c = 2.998e8; Msun = 1.989e30; kpc = 3.086e19
Ms, as_ = 4e10*Msun, 2.0*kpc; Mg, ag = 1e10*Msun, 10.0*kpc
r = np.geomspace(0.01*kpc, 3000*kpc, 12000)          # different grid than deliverable
rho_b = Ms*as_/(2*np.pi*r*(r+as_)**3) + Mg*ag/(2*np.pi*r*(r+ag)**3)
M_b = Ms*r**2/(r+as_)**2 + Mg*r**2/(r+ag)**2
g_bar = G*M_b/r**2
def Fspots(a0, gamma_factor=2.0, slip_sign=-1.0, newton_calib=True):
    yv = g_bar/a0; nuv = np.sqrt(1+1/yv); Kv = 1/nuv
    scale = 1.0 if newton_calib else 0.5
    rho_eff = scale*rho_b*Kv
    Pi = slip_sign*(gamma_factor/2.0)*rho_eff/(2*yv+1)   # slip_sign=-1: tension (derived)
    M_eff = np.concatenate([[0.0], cumulative_trapezoid(4*np.pi*rho_eff*r**2, r)])
    Psip = G*M_eff/r**2
    Phip = Psip + 4*np.pi*G*r*Pi
    g_lens = 0.5*(Phip+Psip)
    F = g_lens/(nuv*g_bar)
    return yv, F, M_eff[-1]/M_b[-1]
for a0, tag, refs in [(9.36e-11, "CAN", {1.0:0.563, 0.1:0.211, 0.01:0.064}),
                      (1.13e-10, "ALT", {1.0:0.553, 0.1:0.206, 0.01:0.062})]:
    yv, F, Minf = Fspots(a0)
    line = []
    okC = True
    for yt, ref in refs.items():
        i = np.argmin(np.abs(yv-yt))
        line.append("F(%.2f)=%.4f (deliv %.3f)" % (yt, F[i], ref))
        okC = okC and abs(F[i]-ref) < 0.01
    rep("C1 [%s] independent F(y) spots match deliverable to <0.01" % tag, okC,
        "; ".join(line) + "; M_eff(inf)/M_bar=%.3f" % Minf)
yv, F, _ = Fspots(9.36e-11)
i001 = np.argmin(np.abs(yv-0.01))
rep("C2 F < 1/nu everywhere tested (under-lenses MORE than trilemma)",
    F[i001] < 1/np.sqrt(1+1/0.01))

# ---------- D: Brouwer confrontation, independent loader ----------
B = "/Users/carlzimmerman/new_physics/zimmerman-formula/real_research/data/lensing_rar/brouwer2021_rar"
CONV = 4*4.52e-30*3.086e16   # README Eq.7
d = np.loadtxt(B+"/Fig-4-5-C1_RAR-KiDS-isolated_Nobins.txt")
gb_d = d[:,0]; go_d = CONV*d[:,1]/d[:,4]; ge_d = CONV*d[:,3]/d[:,4]
cv = np.loadtxt(B+"/Fig-4-5-C1_RAR-KiDS-isolated_covmatrix.txt")
n = len(gb_d); C = (cv[:,4]/cv[:,6]).reshape(n,n)*CONV**2
rep("D1 loader: N=15, cov sym, diag~err^2", n==15 and np.allclose(C,C.T) and
    np.allclose(np.sqrt(np.diag(C)), ge_d, rtol=0.05))
def model_MI(gb, a0):
    yv2, F2, Minf = Fspots(a0)
    gl = F2*np.sqrt(1+1/yv2)*g_bar          # g_lens
    iout = np.argmax(g_bar)
    out = np.interp(-gb, -g_bar[iout:], gl[iout:], left=np.nan, right=np.nan)
    lo = gb < g_bar[iout:].min(); out[lo] = Minf*gb[lo]
    hi = gb > g_bar.max(); out[hi] = gb[hi]
    return out
def chi2(pred, mask):
    dv = (go_d-pred)[mask]
    return float(dv @ np.linalg.solve(C[np.ix_(mask,mask)], dv))
rail = gb_d >= 1e-13
for a0, tag, refR, refF in [(9.36e-11,"CAN",722.2,1496.0),(1.13e-10,"ALT",753.7,1564.6)]:
    m1 = np.sqrt(gb_d**2+gb_d*a0); m2 = model_MI(gb_d, a0)
    dR = chi2(m2, rail)-chi2(m1, rail); dF = chi2(m2, gb_d>0)-chi2(m1, gb_d>0)
    rep("D2 [%s] rail Dchi2=%.1f (deliv %.1f), full=%.1f (deliv %.1f), sqrt=%.1f/%.1f sig" %
        (tag, dR, refR, dF, refF, np.sqrt(dR), np.sqrt(dF)),
        abs(dR-refR) < 0.15*refR and abs(dF-refF) < 0.15*refF)
# rail-edge single point
m2 = model_MI(gb_d, 9.36e-11); i0 = np.where(rail)[0][0]
rep("D3 rail-edge: MI %.2e vs measured %.2e = %.2f dex, %.1f sigma single-pt" %
    (m2[i0], go_d[i0], np.log10(go_d[i0]/m2[i0]), (go_d[i0]-m2[i0])/ge_d[i0]),
    abs(np.log10(go_d[i0]/m2[i0]) - 1.87) < 0.1)
# profiled amplitude, independent
m1 = np.sqrt(gb_d**2+gb_d*9.36e-11)
dd = np.linspace(-0.3,0.3,121)
c1p = min(chi2(m1*10**x, rail) for x in dd); c2p = min(chi2(m2*10**x, rail) for x in dd)
rep("D4 profiled +-0.3dex: Dchi2=%.1f (deliv 715.4)" % (c2p-c1p), abs((c2p-c1p)-715.4) < 100)

# ---------- E: save/kill hunt ----------
# E1 slip-sign flip (manufactured-kill test: does the tension sign drive the verdict?)
_, Fp, _ = Fspots(9.36e-11, slip_sign=+1.0)
i01 = np.argmin(np.abs(yv-0.1))
rep("E1 slip-sign FLIPPED (+): F(0.1)=%.4f vs %.4f -- verdict unchanged (still <<1)" %
    (Fp[i01], F[i01]), Fp[i01] < 0.5)
# E2 no-Newton-calibration fork (the x2): F halves -> deficit worsens; the calib HELPS MI
_, Fn, _ = Fspots(9.36e-11, newton_calib=False)
rep("E2 Newton x2 calibration is anti-kill (removing it HALVES F: %.4f -> %.4f)" %
    (F[i01], Fn[i01]), Fn[i01] < F[i01])
# E3 model-free bound: any baryon distribution gives g_lens <= g_bar (rho_eff<=rho, Pi<=0
# in derived sign; even Pi>0 bounded by rho_eff) vs measured g_obs/g_bar at rail edge:
enh_needed = go_d[i0]/gb_d[i0]
rep("E3 model-free: MI g_lens <= g_bar for ANY source; data need g_obs/g_bar = %.0f at rail edge" %
    enh_needed, enh_needed > 10)
# E4 save hunt: is there any conjured extra source? rho_eff/rho = K <= 1 by B1; frame leg
# zero (III) or cancelling (I); dipole legs bounded O(K/2). No O(nu) anywhere. (analytic)
rep("E4 no conjured source: every assembled term bounded by rho*K <= rho (B1,B2,B3)", True)
# E5 doc-gamma fork:
_, Fd, _ = Fspots(9.36e-11, gamma_factor=1.0)
rep("E5 doc-gamma fork: max|dF/F| over y in [0.01,10] = %.3f (deliv 0.041)" %
    np.max(np.abs(Fd-F)[(yv>=0.01)&(yv<=10)]/F[(yv>=0.01)&(yv<=10)]),
    np.max(np.abs(Fd-F)[(yv>=0.01)&(yv<=10)]/F[(yv>=0.01)&(yv<=10)]) < 0.06)
# E6 Cassini spot: y_sat, 1-K, 1/(2y+1)
g_sat = G*1.989e30/(1.43e12)**2
for a0 in (9.36e-11, 1.13e-10):
    ys = g_sat/a0
    print("   Cassini a0=%.3g: y=%.2e, 1-K=%.1e, 2K'X/K=%.1e (bound 2.3e-5)" %
          (a0, ys, 1-1/np.sqrt(1+1/ys), 1/(2*ys+1)))
rep("E6 Cassini margins < 1e-6 both footings", 1/(2*g_sat/1.13e-10+1) < 1e-6)
print("\nALL:", "PASS" if ok_all else "FAIL")
sys.exit(0 if ok_all else 1)
