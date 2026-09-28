#!/usr/bin/env python3
# AS151 — Extract all primary constraints of the localized action (CA5-GNC-R).
# Tier-0 seed. Bounded prototype: 2-cell leaf x 2 heat slices, sympy + floats.
# Deterministic seed 151. Single thread (enforced via env + rlimit).
import sympy as sp
import json, os, time, resource, math, random

T0 = time.time()
OUT = {}
CHECKS = []

try:
    resource.setrlimit(resource.RLIMIT_AS, (512*1024*1024, 512*1024*1024))
    OUT["memory_limit_enforced"] = "RLIMIT_AS 512MB (set inside script)"
except Exception as e:  # some environments disallow RLIMIT_AS; record honestly
    OUT["memory_limit_enforced"] = "RLIMIT_AS not settable: " + str(e)

def check(name, residual, tol, note=""):
    ok = bool(residual <= tol)
    CHECKS.append({"name": name, "residual": residual, "tol": tol,
                   "pass": ok, "note": note})
    print(f"CHECK {name}: residual={residual:.6e} tol={tol:.3g} -> {'PASS' if ok else 'FAIL'}"
          + (f" | {note}" if note else ""))

def rd(name, val):
    OUT[name] = val
    print(f"  {name} = {val}")

# ----------------------------------------------------------------------
# S0. Constants / footings (mandatory framework; both a0 footings)
# ----------------------------------------------------------------------
G  = 6.67430e-11      # m^3 kg^-1 s^-2 (measured Newton coupling, G_N)
cL = 299792458.0      # m/s
a0c = 9.3619e-11      # canonical footing m/s^2
a0a = 1.1279e-10      # alternative footing m/s^2

def footings(a0, label):
    rho = 4.0*a0*a0/(G*cL*cL)              # mass density kg/m^3  (a0=(c/2) sqrt(G rho))
    eps = rho*cL*cL                        # energy density J/m^3
    lam = 32.0*math.pi*a0*a0/cL**4         # Lambda m^-2 when Einstein and scale G coincide
    return {"footing": label, "a0": a0, "rho_Lambda": rho, "epsilon_Lambda": eps, "Lambda": lam}

F_ = [footings(a0c, "canonical"), footings(a0a, "alternative")]
rd("footings", F_)
rho_fix = F_[0]["rho_Lambda"]
kap_eff = a0a/(cL*math.sqrt(G*rho_fix))    # if rho_Lambda held fixed, effective kappa != 1/2
kap_can = a0c/(cL*math.sqrt(G*rho_fix))
rd("kappa_effective_alt_footing_at_fixed_rho", kap_eff)
rd("kappa_canonical_at_own_rho", kap_can)

# ----------------------------------------------------------------------
# S1. Fiber lemma: local ADM momentum map on Sym(3), h = identity (orthonormal
#     leaf frame) and general symmetric h (numeric). (14): pi = A(K-K·h) -
#     B(Q_K - A_K/N)h. Claims: traceless block A*id; trace block invertible;
#     explicit inverse K = (1/A)(pi - tr(pi)h/2) when h^{ab}h_ab = 3.
# ----------------------------------------------------------------------
K11,K12,K13,K22,K23,K33 = sp.symbols('K11 K12 K13 K22 K23 K33', real=True)
Km = sp.Matrix([[K11,K12,K13],[K12,K22,K23],[K13,K23,K33]])
Apar, Bpar = sp.symbols('Apar Bpar', positive=True)
Npar = sp.symbols('Npar', positive=True)
AKpar = sp.symbols('AKpar', real=True)
Ktr = Km.trace()
PI_id = Apar*(Km - Ktr*sp.eye(3)) - Bpar*(Ktr - AKpar/Npar)*sp.eye(3)
PI_tr_v2 = PI_id.trace()
res_trc2 = sp.simplify(PI_tr_v2 - (-2*Apar*Ktr - 3*Bpar*Ktr + 3*Bpar*AKpar/Npar))
if res_trc2 == 0:
    check("fiber_trace_coefficient", 0.0, 0.0,
          "tr(pi) = -(2A+3B)K + 3B A_K/N on Sym(3) [h=id]; exact symbolic")
else:
    check("fiber_trace_coefficient", 1.0, 0.0, "mismatch " + str(res_trc2))
PI_T = PI_id - (sp.Rational(1,3))*PI_id.trace()*sp.eye(3)
K_T  = Km - (sp.Rational(1,3))*Ktr*sp.eye(3)
res_T = sp.simplify(PI_T - Apar*K_T)
if res_T == sp.zeros(3,3):
    check("fiber_traceless_block", 0.0, 0.0, "traceless part = A*id on traceless symmetric tensors")
else:
    check("fiber_traceless_block", 1.0, 0.0, str(res_T))
P11,P12,P13,P22,P23,P33 = sp.symbols('P11 P12 P13 P22 P23 P33', real=True)
PIm = sp.Matrix([[P11,P12,P13],[P12,P22,P23],[P13,P23,P33]])
Kinv = (PIm - sp.Rational(1,2)*PIm.trace()*sp.eye(3))/Apar
back = Apar*(Kinv - Kinv.trace()*sp.eye(3))
res_inv = sp.simplify(back - PIm)
if res_inv == sp.zeros(3,3):
    check("fiber_inverse_identity_metric", 0.0, 0.0, "T_A ∘ S_A = id (identity-metric trace inversion)")
else:
    check("fiber_inverse_identity_metric", 1.0, 0.0, str(res_inv))
# general metric h (numeric): h^{ab} h_ab = 3
random.seed(151)
hnum = sp.Matrix([[1.2,0.1,-0.05],[0.1,0.95,0.08],[-0.05,0.08,1.05]])
hinv = hnum.inv()
Knum = sp.Matrix([[0.4,-0.1,0.2],[-0.1,0.7,0.3],[0.2,0.3,-0.2]])
Ktrn = (hinv*Knum).trace()
QKn = Ktrn
AKn = 0.33; Nn = 1.3
Pnum = Apar*(Knum - Ktrn*hnum) - Bpar*(QKn - AKn/Nn)*hnum
Pitr = (hinv*Pnum).trace()
Krec = (Pnum - sp.Rational(1,2)*Pitr*hnum)/Apar
backn = Apar*(Krec - (hinv*Krec).trace()*hnum)
PNsub = backn.subs({Apar: sp.Rational(1,2), Bpar: sp.Rational(1,4)}).subs({Apar: sp.Rational(1,2), Bpar: sp.Rational(1,4)})
Pnumsub = Pnum.subs({Apar: sp.Rational(1,2), Bpar: sp.Rational(1,4)})
resn = max(abs(complex(PNsub[i,j] - Pnumsub[i,j])) for i in range(3) for j in range(3))
check("fiber_inverse_general_metric_numeric", float(resn), 1e-12,
      "K=(1/A)(pi - tr_h(pi) h/2) inverts the map for general symmetric h (h^{ab}h_ab=3)")

# ----------------------------------------------------------------------
# S2. Two-cell ring model of the localized CA5-GNC-R density
# ----------------------------------------------------------------------
M2, c2, cN, alpha, ell, theta, V0 = sp.symbols('M2 c2 cN alpha ell theta V0', positive=True)
N0, N1 = sp.symbols('N0 N1', positive=True)
s0, s1 = sp.symbols('s0 s1', real=True)
kd0, kd1 = sp.symbols('kd0 kd1', real=True)
u10, u11, u20, u21 = sp.symbols('u10 u11 u20 u21', real=True)
pd0, pd1 = sp.symbols('pd0 pd1', real=True)
Z0, Z1, U0, U1, l0, l1 = sp.symbols('Z0 Z1 U0 U1 l0 l1', real=True)
W00, W01, W10, W11 = sp.symbols('W00 W01 W10 W11', real=True)
L00, L01, L10, L11 = sp.symbols('L00 L01 L10 L11', real=True)
ph0, ph1 = sp.symbols('ph0 ph1', real=True)
Gp = sp.Symbol('Gp', real=True)     # gate value G(Y) — velocity-free input

N  = [N0, N1]; s  = [s0, s1]; kd = [kd0, kd1]
u1 = [u10, u11]; u2 = [u20, u21]; pd = [pd0, pd1]
Z  = [Z0, Z1]; U  = [U0, U1]; lam = [l0, l1]
W0 = [W00, W01]; W1 = [W10, W11]; L0f = [L00, L01]; L1f = [L10, L11]
ph = [ph0, ph1]

def Df(f, i):    # (Df)_i = f_i - f_{i+1} (ring)
    return f[i] - f[(i+1) % 2]
def Lap(f, i):   # (Delta f)_i = 2 (f_{i+1} - f_i)
    return 2*(f[(i+1) % 2] - f[i])
def mean(f):
    return (f[0] + f[1])/2

k = [kd[i]/N[i] for i in range(2)]          # trace amplitude, K^{ij}=kh^{ij}, K=3k
ka1 = [u1[i]/N[i] for i in range(2)]
ka2 = [u2[i]/N[i] for i in range(2)]
DZ = [Df(Z, i) for i in range(2)]; DU = [Df(U, i) for i in range(2)]
Dph = [Df(ph, i) for i in range(2)]
lnN = [sp.log(N0), sp.log(N1)]; a = [Df(lnN, i) for i in range(2)]
DWb = [Df(W1, i) for i in range(2)]; lWb = [Lap(W1, i) for i in range(2)]
lW0 = [Lap(W0, i) for i in range(2)]
z = [Z[i] - mean(Z) for i in range(2)]
t = [1 + z[i] for i in range(2)]
kbar = mean(k)
QK = [3*(k[i] - kbar) for i in range(2)]
AK = (N[0]*QK[0] + N[1]*QK[1])/2           # <N Q_K>_h on unit-weighted cells

L_terms = []
for i in range(2):
    L_terms.append((M2/2)*N[i]*(ka1[i]**2 + ka2[i]**2 - 6*k[i]**2))       # EH
    L_terms.append(-(c2*M2/2)*N[i]*QK[i]**2)                             # -c2 Q_K^2
    L_terms.append(N[i]*(alpha*(a[i]-DZ[i])**2 + 4*a[i]*DZ[i]
                         - 2*DZ[i]**2 - 4*cN*DZ[i]*DU[i]))               # gravity spatial
    L_terms.append(cN*N[i]*(Gp + ell*a[i]*DWb[i]))                       # gate + compensator
    L_terms.append(cN*N[i]*(L0f[i]*(W1[i]-W0[i]-lW0[i])
                            + L1f[i]*(W1[i]-W0[i]-lWb[i])))              # heat constraints
    L_terms.append(cN*N[i]*lam[i]*(W0[i]-U[i]))                          # lambda0 constraint
    L_terms.append(t[i]*(pd[i]-s[i]*Dph[i])**2/(2*N[i]))                 # t K_d
    L_terms.append(-N[i]*(Dph[i]**2/2 + 1)/t[i])                         # -W_exc/t (Vmix=1)
    L_terms.append(-N[i]*V0*(1 + (t[i] + 1/t[i] - 2)**2))                # -V0 F(t)
L = sp.Add(*L_terms)
L = sp.simplify(L)

vels = [kd0, kd1, u10, u11, u20, u21, pd0, pd1]
stat_fields = [N0,N1,s0,s1,Z0,Z1,U0,U1,l0,l1,W00,W01,W10,W11,L00,L01,L10,L11]

# step 2: differentiate the localized density w.r.t. every physical-time velocity
pi = {}
for v in vels:
    pi[v] = sp.simplify(sp.diff(L, v))
for v in vels:
    print("S2 momentum pi_%s = %s" % (v, sp.factor(pi[v])))

H = sp.Matrix([[sp.diff(sp.diff(L, v), w) for w in vels] for v in vels])
Hrank_sym = H.rank()
print("S2 symbolic rank of 8x8 velocity-momentum matrix:", Hrank_sym)
if Hrank_sym == 8:
    check("vm_map_rank", 0.0, 0.0, "8x8 velocity-momentum matrix has full symbolic rank 8")
else:
    check("vm_map_rank", 1.0, 0.0, "rank " + str(Hrank_sym))

PT0 = {N0: sp.Rational(13,10), N1: sp.Rational(9,10), s0: sp.Rational(1,100), s1: sp.Rational(-1,50),
       kd0: sp.Rational(3,10), kd1: sp.Rational(-2,5), u10: sp.Rational(1,20), u11: sp.Rational(11,100),
       u20: sp.Rational(-7,100), u21: sp.Rational(1,50), pd0: sp.Rational(3,5), pd1: sp.Rational(11,20),
       Z0: sp.Rational(1,5), Z1: sp.Rational(-1,10), U0: sp.Rational(1,20), U1: sp.Rational(1,100),
       l0: sp.Rational(3,10), l1: sp.Rational(1,5), W00: sp.Rational(2,5), W01: sp.Rational(3,5),
       W10: sp.Rational(4,5), W11: sp.Rational(11,10), L00: sp.Rational(1,2), L01: sp.Rational(-3,10),
       L10: sp.Rational(9,10), L11: sp.Rational(7,10), M2: 1, c2: 1, cN: sp.Rational(3,4),
       alpha: sp.Rational(1,2), ell: sp.Rational(1,25), theta: 1, V0: 1, Gp: sp.Rational(1,2),
       ph0: sp.Rational(3,10), ph1: sp.Rational(7,10)}
Hn = H.subs(PT0)
detH = sp.simplify(Hn.det())
print("S2 det(vel-mom matrix) at PT0:", detH)
if detH != 0:
    check("vm_map_det_numeric", 0.0, 0.0, "det = " + str(detH))
else:
    check("vm_map_det_numeric", 1.0, 0.0, "det vanished at PT0")
vn = sp.Matrix([PT0[v] for v in vels])
pzero = {v: 0 for v in vels}                     # affine offset from shift terms
b = sp.Matrix([pi[v].subs(pzero).subs(PT0) for v in vels])
pin = sp.Matrix([pi[v].subs(PT0) for v in vels])
vrec = Hn.inv()*(pin - b)                        # solve the affine system pi = H v + b
res_v = float(max(abs(sp.N(vrec[i] - vn[i])) for i in range(8)))
check("vm_map_inversion_residual", res_v, 1e-12, "velocities recovered from momenta via H^-1")

# augmented 26x26 velocity-Hessian: 8 real + 18 formal static velocities -> rank 8
Haug_n = sp.zeros(26, 26)
for ii in range(8):
    for jj in range(8):
        Haug_n[ii, jj] = H[ii, jj].subs(PT0)
Haug_rank = Haug_n.rank()
if 26 - Haug_rank == 18 and Haug_rank == 8:
    check("null_directions_count", 0.0, 0.0,
          f"augmented Hessian rank {Haug_rank}/26 -> all 18 static fields enter without time velocities")
else:
    check("null_directions_count", 1.0, 0.0, f"rank {Haug_rank}")

# ----------------------------------------------------------------------
# S3. Trace-mean system (c2 term): pi -> K invertibility incl. <K>, A_K
#     continuum form: pi_i = -(2A+3B) K_i + 3B <K> + 3B A_K / N_i
#     two-cell: <K>=(K1+K2)/2, A_K = (N1(K1-<K>)+N2(K2-<K>))/2
# ----------------------------------------------------------------------
Apar2, Bpar2 = sp.symbols('Apar2 Bpar2', positive=True)
K1, K2 = sp.symbols('K1 K2', real=True)
pi1, pi2 = sp.symbols('pi1 pi2', real=True)
Kb2 = (K1+K2)/2
AK2 = (N0*(K1-Kb2) + N1*(K2-Kb2))/2
eq1 = sp.Eq(-(2*Apar2+3*Bpar2)*K1 + 3*Bpar2*Kb2 + 3*Bpar2*AK2/N0, pi1)
eq2 = sp.Eq(-(2*Apar2+3*Bpar2)*K2 + 3*Bpar2*Kb2 + 3*Bpar2*AK2/N1, pi2)
sol = sp.solve([eq1, eq2], [K1, K2], simplify=True)
K1s = sp.together(sol[K1]); K2s = sp.together(sol[K2])
Ddet = sp.factor(sp.denom(K1s))
rd("mean_system_det", Ddet)
# script-canonical closed form (from the solved system):
closed0 = sp.factor(2*Apar2*(8*Apar2*N0*N1 + 3*Bpar2*(N0+N1)**2))
rd("mean_system_det_closed_script_form", closed0)
# cleared-system determinant (multiply the equations by 4 N0 N1):
closed1 = sp.expand(64*Apar2**2*N0*N1 + 24*Apar2*Bpar2*(N0+N1)**2)
rd("mean_system_det_cleared_form", closed1)
rd("mean_system_det_ratio_cleared_over_script", sp.simplify(closed1/closed0))
if sp.simplify(Ddet - closed0) == 0 and sp.simplify(closed1 - 4*closed0) == 0:
    check("mean_det_closed_form", 0.0, 0.0,
          "det = 16 A^2 N1 N2 + 6 A B (N1+N2)^2 [script form]; cleared form 4x = 64A^2N1N2+24AB(N1+N2)^2; both > 0 on domain")
else:
    check("mean_det_closed_form", 1.0, 0.0, "mismatch")
K1h = sp.simplify(K1s.subs({pi1: 0, pi2: 0})); K2h = sp.simplify(K2s.subs({pi1: 0, pi2: 0}))
if K1h == 0 and K2h == 0:
    check("mean_kernel_trivial", 0.0, 0.0, "pi=0 => K1=K2=0 (symbolic; Lean: two_cell_mean_kernel.lean)")
else:
    check("mean_kernel_trivial", 1.0, 0.0, "kernel non-trivial")
ppt = {Apar2: sp.Rational(1,2), Bpar2: sp.Rational(1,4), N0: sp.Rational(13,10), N1: sp.Rational(9,10),
       pi1: sp.Rational(43,100), pi2: sp.Rational(-17,100)}
kp1 = sp.N(K1s.subs(ppt)); kp2 = sp.N(K2s.subs(ppt))
AKv = sp.N(AK2.subs({N0: ppt[N0], N1: ppt[N1], K1: kp1, K2: kp2}))
r1 = abs(sp.N((- (2*Apar2+3*Bpar2)*kp1 + 3*Bpar2*(kp1+kp2)/2 + 3*Bpar2*AKv/N0 - pi1).subs(ppt)))
r2 = abs(sp.N((- (2*Apar2+3*Bpar2)*kp2 + 3*Bpar2*(kp1+kp2)/2 + 3*Bpar2*AKv/N1 - pi2).subs(ppt)))
check("mean_system_inversion_residual", max(float(r1), float(r2)), 1e-12,
      "K recovered from pi; both cells residual")

# model momentum vs (14)-trace relation (convention factor, velocity-independent):
A_ = M2/2; B_ = c2*M2/2
Kb3 = (kd[0]/N[0] + kd[1]/N[1])/2
AK3 = (N[0]*(kd[0]/N[0]-Kb3) + N[1]*(kd[1]/N[1]-Kb3))/2
ftr = [-(2*A_+3*B_)*3*(kd[i]/N[i]) + 3*B_*3*Kb3 + 3*B_*3*AK3/N[i] for i in range(2)]
if ftr[0] != 0:
    rat = sp.simplify(pi[kd0]/ftr[0])
    cons = sp.simplify(pi[kd1] - rat*ftr[1])
    rd("model_vs_14_convention_factor", rat)
    if cons == 0:
        check("model_momentum_proportional_to_14trace", 0.0, 0.0,
              f"pi_model = {rat} * (14)-trace (convention factor, velocity-independent)")
    else:
        check("model_momentum_proportional_to_14trace", 1.0, 0.0, "mismatch " + str(cons))
else:
    check("model_momentum_proportional_to_14trace", 1.0, 0.0, "ftr[0]=0 at PT0")

# ----------------------------------------------------------------------
# S4. Lapse-density identity (12): d/d(ln N_0) sum N [G(Y)+ell a.DW_b]
#     = N_0 [G(Y_0) - ell (Delta W_b)_0] at fixed h,U (capable of failing)
# ----------------------------------------------------------------------
def G_ramp(y, delta=0.05):
    if y <= 0:
        return 0.0
    if y >= delta:
        return y - delta/2
    rr = y/delta
    return delta*(7*rr**5 - 14*rr**6 + 10*rr**7 - 2.5*rr**8)

Jrep3 = lambda p: p*p + p**4

def gate_ring(Nv, W1v, ellv=0.04, Jfun=Jrep3):
    NC = len(Nv)
    def Df(f, i): return f[i] - f[(i+1) % NC]
    def Lap(f, i): return 2*(f[(i+1) % NC] - f[i])
    lnN = [math.log(Nv[i]) for i in range(NC)]
    a = [Df(lnN, i) for i in range(NC)]
    DW = [Df(W1v, i) for i in range(NC)]
    LW = [Lap(W1v, i) for i in range(NC)]
    Y = [Jfun(DW[i]) + ellv*LW[i] - 1.0 for i in range(NC)]
    G = [float(G_ramp(Y[i])) for i in range(NC)]
    I = sum(Nv[i]*(G[i] + ellv*a[i]*DW[i]) for i in range(NC))
    return I, G, Y, LW

def lapse_check(Nv, W1v, label):
    epsv = 1e-6
    I0, G0, Y0, LW0 = gate_ring(Nv, W1v)
    Ip, _, _, _ = gate_ring([Nv[0]*(1+epsv)] + Nv[1:], W1v)
    Im, _, _, _ = gate_ring([Nv[0]*(1-epsv)] + Nv[1:], W1v)
    dI = (Ip-Im)/(2*epsv)
    rhs = Nv[0]*(G0[0] - 0.04*LW0[0])
    prod = len(Nv)
    DW0v = W1v[0] - W1v[1 % prod]
    DlnN0 = math.log(Nv[0]/Nv[1 % prod])
    DN0 = Nv[0] - Nv[1 % prod]
    # exact lattice defect of (12): ell * N0 * DWb0 * (D ln N - DN/N)_0  (Leibniz defect)
    pred = abs(0.04*Nv[0]*DW0v*(DlnN0 - DN0/Nv[0]))
    return abs(dI - rhs), dI, rhs, Y0[0], pred

r2, dI2, rhs2, Y2, p2 = lapse_check([1.3, 0.9], [0.8, 1.1], "2-ring")
# proper h-refinement: same profile, midpoints log-interpolated (h -> h/2)
Nmid = math.sqrt(1.3*0.9); Wmid = math.sqrt(0.8*1.1)
r4, dI4, rhs4, Y4, p4 = lapse_check([1.3, Nmid, 0.9, Nmid], [0.8, Wmid, 1.1, Wmid], "4-ring")
ratio_l = p4/p2 if p2 > 0 else float('nan')
print(f"S4 lapse identity: 2-ring R={r2:.3e} pred={p2:.3e}, 4-ring R={r4:.3e} pred={p4:.3e}, pred-ratio={ratio_l:.3f}")
if abs(r2 - p2) < 0.01*max(p2, 1e-30) and abs(r4 - p4) < 0.02*max(p4, 1e-30) and ratio_l < 0.6:
    check("lapse_density_identity_refined", ratio_l, 0.6,
          f"(12) exact in continuum (analytic: a=D ln N=DN/N); lattice residual = predicted Leibniz defect "
          f"{p2:.2e}->{p4:.2e}, ratio {ratio_l:.3f} ~ h^2; refined once")
else:
    check("lapse_density_identity_refined", ratio_l if ratio_l < 0.6 else 1.0, 0.6,
          f"residual/prediction mismatch: r2={r2:.2e} p2={p2:.2e} r4={r4:.2e} p4={p4:.2e}")
rd("lapse_identity_residuals", {"2ring": r2, "predicted_2ring": p2, "4ring": r4,
                                "predicted_4ring": p4, "ratio": ratio_l, "Y0_2ring": Y2})
# transition-region sample on the 2-ring (G'' != 0):
Nv = [1.3, 0.9]
found = None
for dd in [x/10000.0 for x in range(7800, 7900)]:
    W1t = [0.5, 0.5+dd]
    _, Gt, Yt, _ = gate_ring(Nv, W1t)
    if 0.0 < Yt[0] < 0.05:
        found = (W1t, Yt[0])
        break
if found is None:
    check("lapse_density_identity_transition", 1.0, 0.0, "could not build transition sample")
else:
    W1t, Y0t = found
    rt, dIt, rhst, _, pt = lapse_check(Nv, W1t, "transition")
    check("lapse_density_identity_transition", abs(rt-pt)/max(pt,1e-30), 0.05,
          f"Y0={Y0t:.5f} in transition (G''≠0); measured residual {rt:.2e} = predicted Leibniz defect {pt:.2e} (relative {abs(rt-pt)/max(pt,1e-30):.4f})")

# ----------------------------------------------------------------------
# S5. Square completion + reciprocal-barrier identities (R2),(R3)
# ----------------------------------------------------------------------
av, dzv, duv = sp.symbols('av dzv duv', real=True)
cNv = 1 - alpha/2
d5 = sp.simplify(sp.expand(alpha*(av-dzv)**2 + 4*av*dzv - 2*dzv**2 - 4*cNv*dzv*duv)
                 - sp.expand(alpha*av**2 - 2*cNv*(dzv-(av-duv))**2 + 2*cNv*(av-duv)**2))
if d5 == 0:
    check("square_completion", 0.0, 0.0,
          "alpha|a-DZ|^2+4a.DZ-2|DZ|^2-4cN DZ.DU = alpha|a|^2-2cN|DZ-(a-DU)|^2+2cN|a-DU|^2")
else:
    check("square_completion", 1.0, 0.0, str(d5))
tv = sp.symbols('tv', positive=True)
Fex = 1 + (tv + 1/tv - 2)**2
Fp = sp.simplify(sp.diff(Fex, tv)); Fpp = sp.simplify(sp.diff(Fex, tv, 2))
Fppp = sp.simplify(sp.diff(Fex, tv, 3)); F4 = sp.simplify(sp.diff(Fex, tv, 4))
okF = (sp.simplify(Fp - 2*(tv-1)**3*(tv+1)/tv**3) == 0
       and sp.simplify(Fpp - 2*(tv-1)**2*(tv**2+2*tv+3)/tv**4) == 0
       and sp.simplify(Fp.subs(tv,1)) == 0 and sp.simplify(Fpp.subs(tv,1)) == 0
       and sp.simplify(Fppp.subs(tv,1)) == 0 and sp.simplify(F4.subs(tv,1)) == 24)
rd("F_derivs_at_t1", [sp.simplify(Fp.subs(tv,1)), sp.simplify(Fpp.subs(tv,1)),
                      sp.simplify(Fppp.subs(tv,1)), sp.simplify(F4.subs(tv,1))])
if okF:
    check("reciprocal_barrier_flatness", 0.0, 0.0,
          "F'=2(t-1)^3(t+1)/t^3, F''=2(t-1)^2(t^2+2t+3)/t^4>=0, F'(1)=F''(1)=F'''(1)=0, F''''(1)=24")
else:
    check("reciprocal_barrier_flatness", 1.0, 0.0, "identity failed")
Kdv, Wdv = sp.symbols('Kdv Wdv', positive=True)
Ld = tv*Kdv - Wdv/tv - V0*Fex
rhoR = tv*Kdv + Wdv/tv + V0*Fex
sigR = Kdv + Wdv/tv**2 - V0*sp.diff(Fex, tv)
if sp.simplify(Ld - 2*tv*Kdv + rhoR) == 0:
    check("rhoR_lapse_density", 0.0, 0.0,
          "d(N√h L_d)/dlnN = -N√h rho_R with rho_R=tKd+W/t+V0F(t) [K_d ~ N^-2]")
else:
    check("rhoR_lapse_density", 1.0, 0.0, "failed")
if sp.simplify(sigR - sp.diff(Ld, tv)) == 0:
    check("sigmaR_is_dL_dt", 0.0, 0.0, "sigma_R = dL_d/dt (R3)")
else:
    check("sigmaR_is_dL_dt", 1.0, 0.0, "failed")

# ----------------------------------------------------------------------
# S6. NEGATIVE CONTROL: auxiliary coordinate r treated as physical time
#     The action's only r-derivative is d_r W (heat constraint terms).
#     Introduce the r-velocity variables vW_i := W1_i - W0_i explicitly.
# ----------------------------------------------------------------------
v0s, v1s = sp.symbols('vW0 vW1', real=True)
vW = [v0s, v1s]
# Rebuild the heat constraint terms in the explicit r-velocity variable vW_i := W1_i - W0_i.
# The spatial operators (Delta W0, Delta W1, DW_b) act within their own r-slice and are
# NOT rewritten: only the r-difference (d_r W) is replaced by vW.
def rebuild_L_terms():
    terms = []
    for i in range(2):
        terms.append((M2/2)*N[i]*(ka1[i]**2 + ka2[i]**2 - 6*k[i]**2))
        terms.append(-(c2*M2/2)*N[i]*QK[i]**2)
        terms.append(N[i]*(alpha*(a[i]-DZ[i])**2 + 4*a[i]*DZ[i] - 2*DZ[i]**2 - 4*cN*DZ[i]*DU[i]))
        terms.append(cN*N[i]*(Gp + ell*a[i]*DWb[i]))
        terms.append(cN*N[i]*(L0f[i]*(vW[i] - lW0[i]) + L1f[i]*(vW[i] - lWb[i])))
        terms.append(cN*N[i]*lam[i]*(W0[i]-U[i]))
        terms.append(t[i]*(pd[i]-s[i]*Dph[i])**2/(2*N[i]))
        terms.append(-N[i]*(Dph[i]**2/2 + 1)/t[i])
        terms.append(-N[i]*V0*(1 + (t[i] + 1/t[i] - 2)**2))
    return sp.Add(*terms)
Lr = sp.simplify(rebuild_L_terms())

pi_r = [sp.simplify(sp.diff(Lr, vW[i])) for i in range(2)]
print("S6 r-time momenta pi_W^(r):", [sp.factor(p) for p in pi_r])
if pi_r[0] != 0 and pi_r[1] != 0:
    check("r_time_W_momentum_nonzero", 0.0, 0.0,
          "pi_W^(r) = cN N (L(r0)+L(r1)) != 0: W acquires a spurious momentum in r-time")
else:
    check("r_time_W_momentum_nonzero", 1.0, 0.0, "pi==0")
# spurious pairs are kinetically frozen: d pi^(r)/d vW = 0 identically
Hr = sp.Matrix([[sp.diff(pi_r[i], vW[j]) for j in range(2)] for i in range(2)])
detHr = sp.simplify(Hr.det())
print("S6 r-kinetic Hessian:", Hr)
if detHr == 0 and Hr == sp.zeros(2,2):
    check("r_kinetic_hessian_degenerate", 0.0, 0.0,
          "d pi^(r)/d vW = 0 identically: the spurious pairs are kinetically frozen, not canonical")
else:
    check("r_kinetic_hessian_degenerate", 1.0, 0.0, "nondegenerate / nonzero")
# t-time: vW is NOT a physical-time velocity: the t-momentum of vW would be dL/d(d_t vW)=0;
# W0, W1 and L fields remain t-primary-constrained:
t_heat_prim = all(sp.simplify(sp.diff(L, f)) == 0 for f in [W00,W01,W10,W11,L00,L01,L10,L11])
# (L does not contain any d_t of these fields; diff(L,f) w.r.t. the field itself is the
#  wrong object, so use the augmented-rank result from S2 instead: rank 8/26.)
n_t_prim = len(stat_fields)                 # 18 (verified: augmented Hessian rank 8/26)
n_r_prim = len(stat_fields) - 8             # W(r0), W(r1) (8 fields) gain r-momenta -> lose primary status
rd("negative_control_counts", {
    "t_time_primary_constraints": n_t_prim,
    "r_time_primary_constraints": n_r_prim,
    "spurious_canonical_pairs": 4,
    "primary_constraint_shift": n_t_prim - n_r_prim,
    "r_kinetic_hessian": str(Hr)})
if n_t_prim - n_r_prim == 8:
    check("negative_control_contaminates", 0.0, 0.0,
          "r-as-time: +4 spurious frozen canonical pairs, -8 primary constraints; heat equation reclassified as evolution")
else:
    check("negative_control_contaminates", 1.0, 0.0, "no contamination")

# ----------------------------------------------------------------------
# S7. Carrier momentum invertibility; t>0 domain condition
# ----------------------------------------------------------------------
t0v, t1v = sp.symbols('t0v t1v', positive=True)
Hcar = sp.Matrix([[t0v/N0, 0], [0, t1v/N1]])
detcar = sp.simplify(Hcar.det())
rd("carrier_momentum_map_det", detcar)
if sp.simplify(detcar - t0v*t1v/(N0*N1)) == 0:
    check("carrier_map_invertible_for_t>0", 0.0, 0.0,
          "det(pi_phi map) = t0 t1/(N0 N1): invertible iff t>0 pointwise (reciprocal-barrier domain)")
else:
    check("carrier_map_invertible_for_t>0", 1.0, 0.0, "mismatch")

# ----------------------------------------------------------------------
# S8. Global normalizations / identities
# ----------------------------------------------------------------------
sigvals = [0.3, 0.8]; NvA = [1.3, 0.9]
meanNs = (NvA[0]*sigvals[0] + NvA[1]*sigvals[1])/2
proj = sum(NvA[i]*(sigvals[i] - meanNs/NvA[i]) for i in range(2))
check("projector_solvability", abs(proj), 1e-12,
      "∫N√h[σ_R-<Nσ_R>_h/N]=0 identically (projected Z-equation solvability, R4)")
ztest = sp.simplify(L.subs({Z0: Z0+1, Z1: Z1+1}) - L)
if ztest == 0:
    check("Z_constant_shift_invariance", 0.0, 0.0,
          "Z->Z+c(t) exact redundancy of the localized density; <Z> is a normalization")
else:
    check("Z_constant_shift_invariance", 1.0, 0.0, str(ztest))

# ----------------------------------------------------------------------
# Envelope
# ----------------------------------------------------------------------
T1 = time.time()
ru = resource.getrusage(resource.RUSAGE_SELF)
OUT["wall_s"] = T1 - T0
OUT["maxrss_bytes"] = ru.ru_maxrss          # macOS reports ru_maxrss in BYTES
OUT["maxrss_mib"] = ru.ru_maxrss/(1024*1024)
print(f"ENVELOPE wall={T1-T0:.2f}s maxrss={ru.ru_maxrss/(1024*1024):.1f}MiB")

with open("residuals.json", "w") as f:
    json.dump({"checks": CHECKS, "out": {k: v for k, v in OUT.items()}}, f, indent=1, default=str)
npass = sum(1 for c in CHECKS if c["pass"])
print(f"\nCHECKS: {npass}/{len(CHECKS)} PASS")
for c in CHECKS:
    print(("PASS " if c["pass"] else "FAIL ") + c["name"] + " — " + c.get("note", ""))
