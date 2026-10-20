"""CFG882 -- clump retention in the cold-energy equations.  Criteria: FROZEN_CRITERIA.md (3a10f28a8, committed alone first).
Run:  OMP_NUM_THREADS=1 nice -n 10 python3 cfg882.py          -> cfg882.out, cfg882_results.json
      CFG882_MUTATE=1 OMP_NUM_THREADS=1 nice -n 10 python3 cfg882.py  -> cfg882_MUTATE.out, cfg882_results_MUTATE.json (exit 1 by design)
Density sub-flow of the record's settling drift (CFG541 E3/E4, CFG544 FIX-1 two-sided psi, CFG638), spherical, static baryons and
phantom; gated variant = CFG639 HG (G = 1 iff d = rho_ph - rho_c > 0).  kappa = 1/2 FITTED; footings never pooled; not theory closed."""
import os, json, math, time
import numpy as np
import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__)); LANES = os.path.dirname(HERE)
MUT = os.environ.get("CFG882_MUTATE", "") == "1"; SUF = "_MUTATE" if MUT else ""
OUT = []
def P(s=""):
    print(s, flush=True); OUT.append(str(s))

# ---------------------------------------------------------------- units: pc, Msun, Myr
PC, MSUN, MYR, G_SI = 3.0857e16, 1.989e30, 3.15576e13, 6.674e-11
G = G_SI * MSUN * MYR ** 2 / PC ** 3                       # pc^3 Msun^-1 Myr^-2
KMS = 1e3 * MYR / PC                                       # (km/s) -> pc/Myr
A0 = {"canonical": 9.3603e-11 * MYR ** 2 / PC, "alt": 1.1312e-10 * MYR ** 2 / PC}
FOOTS = ("canonical", "alt")
RC = 104.0                                                 # pc, CFG870/877 core radius
T_RET, T_ALT = 12000.0, 13500.0                            # Myr
ALPHA_FLOOR, ALPHA_GAL = 0.05, 0.5
HOSTS = {"H1": (1e4, 30.0), "H2": (3e5, 200.0), "H3": (2e7, 700.0)}
NF, RMIN, ROUT, CFL = 800, 0.5, 2.0e4, 0.3
R877 = json.load(open(os.path.join(LANES, "CFG877_finite_cold_clump", "cfg877_results.json")))
CL = {f: dict(Vx=R877[f]["Vx"] * KMS, Mcl=R877[f]["Mcl_Msun"], rt=R877[f]["rt_pc"]) for f in FOOTS}
nu = lambda y: 1.0 / (-np.expm1(-np.sqrt(np.maximum(y, 1e-300))))
RES = dict(lane="CFG882", mutate=MUT, criteria="3a10f28a8", settings=dict(T_ret_Myr=T_RET, alpha_floor=ALPHA_FLOOR, alpha_gal=ALPHA_GAL,
           hosts=HOSTS, grid=dict(NF=NF, rmin_pc=RMIN, rout_pc=ROUT, CFL=CFL), clump={f: dict(Vx_kms=R877[f]["Vx"], Mcl=R877[f]["Mcl_Msun"],
           rt_pc=R877[f]["rt_pc"], rc_pc=RC) for f in FOOTS}))
T0 = time.time()

# ---------------------------------------------------------------- model
class Model:
    """Spherical shells; cell masses m.  rho_b static (Plummer or uniform), m_ph static (round-rule phantom of own baryons)."""
    def __init__(self, foot, host=None, clump=True, uniform=None):
        self.foot = foot; a0 = A0[foot]
        self.rf = np.concatenate([[0.0], np.geomspace(RMIN, ROUT, NF)])
        self.V = 4 * math.pi / 3 * np.diff(self.rf ** 3); self.A = 4 * math.pi * self.rf ** 2; self.n = self.V.size
        r = self.rf
        if uniform is None:
            Mb, a = HOSTS[host]
            Mbr = Mb * r ** 3 / (r ** 2 + a ** 2) ** 1.5
            Mph = np.zeros_like(r); k = r > 0
            Mph[k] = (nu(G * Mbr[k] / (r[k] ** 2 * a0)) - 1.0) * Mbr[k]
            self.rhob = np.diff(Mbr) / self.V; self.mph = np.diff(Mph); self.Mph_f = Mph; self.rhob0 = 3 * Mb / (4 * math.pi * a ** 3)
            self.Mb_f = Mbr
        else:                                            # K6: uniform cold sphere on a uniform baryon background, no phantom
            rho0, R0, rb = uniform
            self.rhob = np.full(self.n, rb); self.mph = np.zeros(self.n); self.Mph_f = np.zeros_like(r); self.rhob0 = rb
            self.Mb_f = rb * 4 * math.pi / 3 * r ** 3
        assert np.all(self.mph >= 0), "negative phantom cell"
        if uniform is not None:
            rho0, R0, _ = uniform
            self.mx = rho0 * 4 * math.pi / 3 * np.diff(np.minimum(r, R0) ** 3)
        elif clump:
            c = CL[foot]; Mx = np.minimum(c["Vx"] ** 2 * r ** 3 / (G * (r ** 2 + RC ** 2)), c["Mcl"]); self.mx = np.diff(Mx)
        else:
            self.mx = np.zeros(self.n)
        self.m0 = self.mph + self.mx
        self.dr = np.diff(self.rf)

    def rhs(self, m, alpha, mode):
        """dm/dt and the CFL time.  mode: 'two' (record, ungated), 'gate' (CFG639), 'gate1' (gated path with G forced to 1, K1),
        'inv' (MUTATE: G = 1 iff d < 0)."""
        rho = m / self.V
        d = self.mph - m                                 # (rho_ph - rho_c) V  (sign test only)
        if mode == "two": Gt = np.ones(self.n)
        elif mode == "gate": Gt = (d > 0).astype(float)
        elif mode == "gate1": Gt = (d > 0).astype(float); Gt[:] = 1.0
        elif mode == "inv": Gt = (d < 0).astype(float)
        else: raise ValueError(mode)
        Mex = np.concatenate([[0.0], np.cumsum(m - self.mph)])        # M_ex(<r_f) = -M_d(<r_f)
        j = np.arange(1, self.n)                                      # interior faces
        s = G * Mex[j] / self.rf[j] ** 2                              # -psi' = G M_ex/r^2 (outward if > 0)
        don = np.where(s > 0, j - 1, j)
        rhom = self.rhob[don] + rho[don]
        tau = np.where(rhom > 0, 1.0 / np.sqrt(4 * math.pi * G * np.maximum(rhom, 1e-300)), 0.0)
        v = alpha * tau * s * Gt[don] * (rho[don] > 0)
        F = v * rho[don] * self.A[j]                                   # outward mass flux through face j
        dm = np.zeros(self.n); dm[:-1] -= F; dm[1:] += F
        mv = np.abs(v) > 0
        dt = CFL * np.min(self.V[don[mv]] / (np.abs(v[mv]) * self.A[j[mv]])) if mv.any() else np.inf
        # stiffness limit: the cumulative excess at a face relaxes at Gamma = alpha 4 pi G tau rho_c (K4), independently of how
        # small it is, so the CFL bound alone does not bound dt*Gamma (correction 1, before any label): dt <= 0.5/max Gamma
        rm = self.rhob + rho
        gam = np.where((Gt > 0) & (rho > 0), alpha * 4 * math.pi * G * rho / np.sqrt(4 * math.pi * G * np.maximum(rm, 1e-300)), 0.0)
        if gam.max() > 0: dt = min(dt, 0.5 / gam.max())
        return dm, dt, v

    def Mex_at(self, m, r):
        Mex = np.concatenate([[0.0], np.cumsum(m - self.mph)]); return float(np.interp(r, self.rf, Mex))

    def run(self, alpha, mode, T, m=None, record=False, rt=None):
        m = self.m0.copy() if m is None else m.copy()
        t, nstep, cap = 0.0, 0, (10.0 / alpha if alpha > 0 else 10.0)
        ser = []
        rt = CL[self.foot]["rt"] if rt is None else rt
        Mex0 = self.Mex_at(self.m0, rt)
        minm = 0.0
        while t < T - 1e-12:
            dm, dtc, _ = self.rhs(m, alpha, mode)
            dt = min(dtc, cap, T - t)
            for _ in range(80):                          # SSP-RK2 (Heun); both stages must satisfy the CFL bound
                m1 = m + dt * dm
                dm1, dtc1, _ = self.rhs(m1, alpha, mode)
                mn = 0.5 * (m + m1 + dt * dm1)
                if dt <= dtc1 * (1 + 1e-12) and m1.min() >= 0.0 and mn.min() >= 0.0: break
                dt *= 0.5
            m = mn
            t += dt; nstep += 1
            minm = min(minm, float(m.min()))
            if record: ser.append((alpha * t, self.Mex_at(m, rt) / Mex0, (m[0] - self.mph[0]) / self.V[0]))
        return dict(m=m, t=t, steps=nstep, minm=minm, R=self.Mex_at(m, rt) / Mex0, ser=ser)

# ---------------------------------------------------------------- analytic pieces
def I_bound(rho, b):
    """I(rho) = int_rho^inf sqrt(b + x)/(sqrt(4 pi G) x^2) dx (closed form; b = central baryon density)."""
    s = math.sqrt(b + rho)
    val = s / rho + (math.atanh(math.sqrt(b) / s) / math.sqrt(b) if b > 0 else 1.0 / s)
    return val / math.sqrt(4 * math.pi * G)
def rho_star(svalue, b):
    """initial-condition-free upper bound on the centre overfill after alpha*t = svalue: I(rho*) = svalue."""
    lo, hi = 1e-30, 1e30
    for _ in range(140):
        mid = math.sqrt(lo * hi)
        if I_bound(mid, b) > svalue: lo = mid
        else: hi = mid
    return math.sqrt(lo * hi)
def tau_of(rho): return 1.0 / math.sqrt(4 * math.pi * G * rho)

# ================================================================ K4/K5/K7 sympy
P("CFG882  clump retention in the cold-energy equations" + ("   [MUTATE: inverted gate]" if MUT else ""))
P("  kappa = 1/2 FITTED; footings never pooled; density sub-flow of the record's drift; not theory closed.\n")
r, t, s_, alpha, Gs, rho_c, rho0, rhob_s, q, sig2, p, rhox = sp.symbols("r t s alpha G rho_c rho0 rho_b q sigma2 p rho_x", positive=True)
mfun = sp.Function("m"); taufun = sp.Function("tau")
# K4: Poisson for the two-sided deficit, d = -m'/(4 pi r^2): r^2 psi' = int_0^r 4 pi G s^2 d(s) ds = -G m(r) (m(0) = 0)
r2psi = sp.integrate(4 * sp.pi * Gs * s_ ** 2 * (-sp.Derivative(mfun(s_), s_) / (4 * sp.pi * s_ ** 2)), (s_, 0, r))
r2psi = r2psi.subs(mfun(0), 0)
psi_p = sp.simplify(r2psi / r ** 2)
v_s = -alpha * taufun(r) * psi_p                       # v_s = -alpha tau psi'
dMc_dt = -4 * sp.pi * r ** 2 * rho_c * v_s             # drift flux through r; rho_ph static -> dM_ex/dt = dM_c/dt
K4_res = sp.simplify(dMc_dt - (-alpha * 4 * sp.pi * Gs * taufun(r) * rho_c * mfun(r)))
K4 = K4_res == 0
P(f"  K4 (sympy) dM_ex(<r)/dt = -alpha 4 pi G tau rho_c M_ex(<r): residual {K4_res} -> {'PASS' if K4 else 'FAIL'}")
# K5: centre law, uniform solution, bound integral
c5, t2 = sp.symbols("c5 tau2", real=True); tau0 = sp.symbols("tau0", positive=True)
mser = sp.Rational(4, 3) * sp.pi * rho0 * r ** 3 + c5 * r ** 5
tser = tau0 + t2 * r ** 2
vser = alpha * tser * Gs * mser / r ** 2
divv0 = sp.limit(sp.diff(r ** 2 * vser, r) / r ** 2, r, 0)
K5a = sp.simplify(divv0 - 4 * sp.pi * Gs * alpha * tau0 * rho0) == 0
rt_ = rho0 / (1 + alpha * t / (2 * (1 / sp.sqrt(4 * sp.pi * Gs * rho0)))) ** 2
K5b = sp.simplify(sp.diff(rt_, t) + alpha * sp.sqrt(4 * sp.pi * Gs) * rt_ ** sp.Rational(3, 2)) == 0
x = sp.symbols("x", positive=True)
Icl = (sp.sqrt(rhob_s + x) / x + sp.atanh(sp.sqrt(rhob_s) / sp.sqrt(rhob_s + x)) / sp.sqrt(rhob_s)) / sp.sqrt(4 * sp.pi * Gs)
K5c = sp.simplify(sp.diff(Icl, x) + sp.sqrt(rhob_s + x) / (sp.sqrt(4 * sp.pi * Gs) * x ** 2)) == 0
K5d = sp.simplify(sp.limit(Icl, rhob_s, 0) - 2 / sp.sqrt(4 * sp.pi * Gs * x)) == 0
K5 = bool(K5a and K5b and K5c and K5d)
P(f"  K5 (sympy) centre div v_s -> 4 pi G alpha tau0 rho_ex0: {K5a}; uniform rho0/(1+alpha t/2tau0)^2 solves it: {K5b};"
  f" I(rho) closed form: {K5c}; I -> 2 tau at rho_b = 0: {K5d} -> {'PASS' if K5 else 'FAIL'}")
# K7: steady counter-flow u = -v_s with isotropic p: Pi_ik d_k u_j + Pi_jk d_k u_i = -(2 alpha/tau)(Pi - rho sigma_J^2)
tau_s = sp.symbols("tau", positive=True)
divvs = alpha * q / tau_s                               # div v_s = alpha tau 4 pi G rho_ex = alpha q / tau
psol = sp.solve(sp.Eq(2 * p * (-divvs / 3), -(2 * alpha / tau_s) * (p - rho_c * sig2)), p)[0]
K7_form = sp.simplify(psol - rho_c * sig2 / (1 - q / 3)) == 0
K7_neq = sp.simplify(psol - rho_c * sig2) != 0
K7 = bool(K7_form and K7_neq)
P(f"  K7 (sympy) steady counter-flow pressure p = {sp.simplify(psol)}  (= rho sigma_J^2/(1 - q/3), not hydrostatic for q > 0)"
  f" -> {'PASS' if K7 else 'FAIL'}: no stationary counter-flow; the drift-only density evolution is the record's to O(1)")
RES["K_sympy"] = dict(K4=bool(K4), K5=K5, K7=K7, K7_p=str(sp.simplify(psol)))

# ================================================================ numeric K-tests
P("\n  numeric K-tests")
mh = Model("canonical", "H2")
# K1: gated path with G forced to 1 == two-sided path, bit for bit (run 300 Myr at alpha = 1)
a1 = mh.run(1.0, "two", 300.0); b1 = mh.run(1.0, "gate1", 300.0)
K1d = float(np.max(np.abs(a1["m"] - b1["m"]))); K1 = K1d == 0.0
P(f"  K1 gated solver with G = 1 vs two-sided: max |dm| = {K1d:.1e} Msun -> {'PASS' if K1 else 'FAIL'}")
# K3: alpha = 0
c3 = mh.run(0.0, "two", 2000.0); K3d = float(np.max(np.abs(c3["m"] - mh.m0))); K3 = K3d == 0.0
P(f"  K3 alpha = 0 (2 Gyr): max |dm| = {K3d:.1e} -> {'PASS' if K3 else 'FAIL'}")
# K8: time rescaling
k8a = mh.run(0.5, "two", 1000.0); k8b = mh.run(1.0, "two", 500.0)
K8d = float(np.max(np.abs(k8a["m"] - k8b["m"]) / np.maximum(k8b["m"], 1e-300))); K8 = K8d <= 1e-9
P(f"  K8 alpha 0.5 to 1 Gyr vs alpha 1 to 0.5 Gyr: max rel |dm| = {K8d:.1e} -> {'PASS' if K8 else 'FAIL'}")
# K6: uniform cold sphere vs the centre ODE
rho_x0 = {f: 3 * CL[f]["Vx"] ** 2 / (4 * math.pi * G * RC ** 2) for f in FOOTS}
r0 = rho_x0["canonical"]; rb6 = 0.01 * r0; tau6 = tau_of(r0)
mu = Model("canonical", uniform=(r0, 100.0, rb6))
T6 = 4 * tau6
k6 = mu.run(1.0, "two", T6)
def centre_ode(rho_init, b, T, n=200000):
    f = lambda y: -4 * math.pi * G * y * y / math.sqrt(4 * math.pi * G * (b + y))
    y, h = rho_init, T / n
    for _ in range(n):
        k1 = f(y); k2 = f(y + 0.5 * h * k1); k3 = f(y + 0.5 * h * k2); k4 = f(y + h * k3); y += h * (k1 + 2 * k2 + 2 * k3 + k4) / 6
    return y
y6 = centre_ode(r0, rb6, T6); n6 = k6["m"][0] / mu.V[0]; K6d = abs(n6 / y6 - 1); K6 = K6d <= 0.01
P(f"  K6 uniform sphere, alpha t = 4 tau0 = {T6:.1f} Myr: centre cell {n6:.5f} vs centre ODE {y6:.5f} Msun/pc^3 "
  f"(rel {K6d:.2e}; analytic cold-only {r0 / (1 + T6 / (2 * tau6)) ** 2:.5f}) -> {'PASS' if K6 else 'FAIL'}")
RES["K_numeric"] = dict(K1=K1, K1_maxdm=K1d, K3=K3, K3_maxdm=K3d, K8=K8, K8_maxrel=K8d, K6=K6, K6_rel=K6d, K6_centre=n6, K6_ode=y6)
mass_err = []                                            # K2 collected over every run below
def k2(mod, res, label):
    e = abs(res["m"].sum() - mod.m0.sum()) / mod.m0.sum(); mass_err.append((label, e)); return e
for lab_, mod, res in (("K1 two", mh, a1), ("K1 gate1", mh, b1), ("K3", mh, c3), ("K8 a", mh, k8a), ("K8 b", mh, k8b), ("K6", mu, k6)):
    k2(mod, res, lab_)

# ================================================================ V1: two-sided retention
P("\n  V1  record two-sided drift (FIX-1 psi, ungated): clump drain")
V1 = {}; K9_ok = True; K9_worst = 0.0; sers = {}
for f in FOOTS:
    V1[f] = {}
    for h in HOSTS:
        md = Model(f, h)
        res = md.run(1.0, "two", T_RET, record=True); k2(md, res, f"V1 {f} {h}")
        S = np.array(res["ser"]); sv, Rv, cv = S[:, 0], S[:, 1], S[:, 2]
        def s_at(level):
            k = np.where(Rv <= level)[0]
            if not k.size: return float("inf")
            i = k[0]
            if i == 0: return float(sv[0])
            return float(np.exp(np.interp(level, [Rv[i], Rv[i - 1]], [math.log(sv[i]), math.log(sv[i - 1])])))
        s50, s90 = s_at(0.5), s_at(0.9)
        Rat = lambda sval: float(np.interp(sval, sv, Rv))
        kk = np.unique(np.geomspace(1, len(sv), 400).astype(int) - 1)
        bnd = np.array([rho_star(x_, md.rhob0) for x_ in sv[kk]])
        ratio = float(np.max(cv[kk] / bnd)); K9_worst = max(K9_worst, ratio); K9_ok &= ratio <= 1.01
        rx0 = rho_x0[f]; ac = I_bound(0.5 * rx0, md.rhob0) / T_RET; ac_full = I_bound(rx0, md.rhob0) / T_RET
        # D5 quantities at t = 0, alpha = 1
        _, _, v0 = md.rhs(md.m0, 1.0, "two")
        Mex_f = np.concatenate([[0.0], np.cumsum(md.m0 - md.mph)])
        integrand = G * Mex_f[1:] / md.rf[1:] ** 2
        psi0 = float(np.sum(0.5 * (integrand[1:] + integrand[:-1]) * np.diff(md.rf[1:])) + integrand[0] * md.rf[1]
                     + G * Mex_f[-1] / md.rf[-1])
        rhoc_rt = float(np.interp(CL[f]["rt"] * 0.99, 0.5 * (md.rf[1:] + md.rf[:-1]), (md.m0 / md.V)))
        V1[f][h] = dict(s50_Myr=s50, s90_Myr=s90, alpha50=s50 / T_RET, alpha90=s90 / T_RET, alpha50_T13p5=s50 / T_ALT,
                        alpha_c=ac, alpha_c_target_full=ac_full, alpha_c_T13p5=I_bound(0.5 * rx0, md.rhob0) / T_ALT,
                        R_at_alpha_floor=Rat(ALPHA_FLOOR * T_RET), R_at_alpha_0p5=Rat(0.5 * T_RET), R_at_alpha_1=Rat(T_RET),
                        R_at_alpha_1e3=Rat(1e-3 * T_RET), R_at_alpha_1e2=Rat(1e-2 * T_RET),
                        K9_max_ratio=ratio, steps=res["steps"], minm=res["minm"], rhob0=md.rhob0,
                        rho_ph_centre_cell=float(md.mph[0] / md.V[0]), rho_c_near_rt=rhoc_rt,
                        tau_centre_Myr=tau_of(rx0), tau_near_rt_Myr=tau_of(rhoc_rt + float(np.interp(CL[f]["rt"], md.rf[1:], md.rhob))),
                        psi_ex_centre_kms2=psi0 / KMS ** 2, vmax_alpha1_kms=float(np.max(np.abs(v0))) / KMS)
        sers[f"{f}|{h}"] = [(float(a), float(b)) for a, b, _ in S[np.unique(np.geomspace(1, len(S), 60).astype(int) - 1)]]
        P(f"    [{f:9s} {h}] s50 = alpha t50 = {s50:8.2f} Myr -> alpha_50 = {s50 / T_RET:.2e} (alpha_90 {s90 / T_RET:.2e}); "
          f"central bound alpha_c = {ac:.2e} (target rho_x0/2; {ac_full:.2e} at rho_x0); R(alpha 0.05) = {Rat(ALPHA_FLOOR * T_RET):.3f}, "
          f"R(alpha 0.5) = {Rat(0.5 * T_RET):.3f}; steps {res['steps']}")
    mx_ = max(max(V1[f][h]["alpha50"], V1[f][h]["alpha_c"]) for h in HOSTS)
    comp = any(V1[f][h]["alpha50"] >= ALPHA_GAL for h in HOSTS)
    lab = "COMPATIBLE" if comp else ("EXCLUDED" if mx_ < ALPHA_FLOOR else ("TENSION" if mx_ < ALPHA_GAL else "UNCLASSIFIED"))
    V1[f]["max_alpha"] = mx_; V1[f]["label"] = lab
    P(f"    -> [{f}] max over hosts of max(alpha_50, alpha_c) = {mx_:.2e}  (floor {ALPHA_FLOOR}, galaxy side {ALPHA_GAL}) -> {lab}")
M2 = all(V1[f][h]["R_at_alpha_0p5"] < 0.5 for f in FOOTS for h in HOSTS)
P(f"  K9 centre overfill <= initial-condition-free bound rho*(alpha t): worst ratio {K9_worst:.4f} -> {'PASS' if K9_ok else 'FAIL'}")
P(f"  M2 (gate removed, alpha = 0.5): R < 0.5 in every cell -> {'BITES' if M2 else 'DOES NOT BITE'}")
RES["V1"] = V1; RES["K9"] = dict(pass_=bool(K9_ok), worst=K9_worst); RES["M2_bites"] = bool(M2); RES["V1_series_alpha1"] = sers

# ================================================================ V2: gated retention (MUTATE: inverted gate)
mode2 = "inv" if MUT else "gate"
P(f"\n  V2  deficit-gated mobility (CFG639 HG){' -- MUTATE M1: INVERTED gate (G = 1 iff d < 0)' if MUT else ''}: smooth settled halo + clump, T_ret = {T_RET / 1e3:.0f} Gyr")
V2 = {}
for f in FOOTS:
    for h in HOSTS:
        md = Model(f, h)
        for al in (0.5, 1.0, 1.186):
            res = md.run(al, mode2, T_RET); k2(md, res, f"V2 {f} {h} {al}")
            ngate_on = int((md.rhs(md.m0, al, mode2)[2] != 0).sum())
            V2[f"{f}|{h}|{al}"] = dict(R=res["R"], steps=res["steps"], minm=res["minm"], faces_moving_t0=ngate_on)
            P(f"    [{f:9s} {h} alpha {al:5.3f}] R(T_ret) = {res['R']:.6f}   moving faces at t=0: {ngate_on}   steps {res['steps']}")
fails2 = [k for k, v in V2.items() if v["R"] < 0.5]
lab2 = "GATED RETAINS" if not fails2 else "GATED FAILS"
P(f"    -> {lab2}" + (f" (failing cells: {', '.join(fails2)})" if fails2 else ""))
RES["V2"] = V2; RES["V2_label"] = lab2; RES["V2_mode"] = mode2
if MUT:
    M1 = all(V2[f"{f}|{h}|0.5"]["R"] < 0.5 for f in FOOTS for h in HOSTS)
    RES["M1_bites"] = bool(M1)
    P(f"  M1 (inverted gate, alpha = 0.5): R < 0.5 in every host x footing -> {'BITES' if M1 else 'DOES NOT BITE (V2 NOT DIAGNOSTIC)'}")

# ================================================================ diagnostics (main run only for D1)
D = {}
if not MUT:
    P("\n  D1  gated drift with a fluctuating settled halo (no verdict weight; fluctuation level not derived)")
    rng = np.random.default_rng(882)
    for f in FOOTS:
        base = Model(f, "H2"); xi = np.clip(rng.standard_normal(base.n), -3, 3)
        for eps in (0.01, 0.1):
            for withcl in (True, False):
                md = Model(f, "H2", clump=withcl)
                m0 = md.mph * (1 + eps * xi) + md.mx
                md.m0 = m0                                 # noisy start is the reference state
                res = md.run(1.0, "gate", T_RET); k2(md, res, f"D1 {f} {eps} {withcl}")
                rt = CL[f]["rt"]; rcell = 0.5 * (md.rf[1:] + md.rf[:-1]); zone = (rcell > rt) & (rcell < 2000.0)
                empt = float(np.mean(res["m"][zone] < 1e-6 * md.mph[zone]))
                gate0 = float(np.mean((md.mph - m0)[zone] > 0))
                Mex = lambda mm, rr: md.Mex_at(mm, rr)
                Mcl = CL[f]["Mcl"]
                row = dict(R=(res["R"] if withcl else None), frac_zone_d_pos_t0=gate0, frac_zone_emptied=empt,
                           Mex_over_Mcl_end={str(rr): Mex(res["m"], rr) / Mcl for rr in (rt, 500.0, 1000.0, 2000.0)},
                           Mex_over_Mcl_start={str(rr): Mex(m0, rr) / Mcl for rr in (rt, 500.0, 1000.0, 2000.0)},
                           steps=res["steps"], minm=res["minm"])
                D[f"D1|{f}|eps{eps}|{'clump' if withcl else 'noclump'}"] = row
                P(f"    [{f:9s} H2 eps {eps:4.2f} {'clump   ' if withcl else 'no clump'}] R(r_t) = "
                  f"{(format(res['R'], '.4f') if withcl else '   -  ')}; zone (r_t, 2 kpc): d>0 at t0 {gate0:.2f}, emptied at end {empt:.2f}; "
                  f"M_ex/M_cl at r_t/0.5/1/2 kpc: start " + "/".join(f"{v:+.3f}" for v in row["Mex_over_Mcl_start"].values())
                  + "  end " + "/".join(f"{v:+.3f}" for v in row["Mex_over_Mcl_end"].values()))

P("\n  D2  tides: clump keeps its identity outside D_crit = sqrt(2 V_h^2 r_t^3/(G m)) (flat host; estimate)")
for f in FOOTS:
    a0 = A0[f]; c = CL[f]; md = Model(f, "H2")
    m_extra = float(np.interp(c["rt"], md.rf, md.Mb_f) + np.interp(c["rt"], md.rf, md.Mph_f))
    for Mh in (6e10, 1e11):
        Vh = (G * Mh * a0) ** 0.25
        for lab_, mm in (("clump only", c["Mcl"]), ("clump + H2 baryons + phantom", c["Mcl"] + m_extra)):
            Dc = math.sqrt(2 * Vh ** 2 * c["rt"] ** 3 / (G * mm))
            D[f"D2|{f}|Mh{Mh:.0e}|{lab_}"] = dict(Vh_kms=Vh / KMS, m=mm, Dcrit_kpc=Dc / 1e3)
            P(f"    [{f:9s}] host M_b {Mh:.0e} (V_h {Vh / KMS:5.1f} km/s), {lab_:28s} m = {mm:.2e}: D_crit = {Dc / 1e3:.2f} kpc")

P("\n  D3  one clump's pull on a point-baryon host, Delta g / g_law (CFG877 capped shape)")
for f in FOOTS:
    a0 = A0[f]; c = CL[f]
    for Mb in (1e7, 1e8, 1e9, 1e10, 1e11):
        row = {}
        for rr in (200.0, 500.0, 1000.0, 2000.0, 5000.0):
            gN = G * Mb / rr ** 2; gl = float(nu(gN / a0) * gN)
            Mx = min(c["Vx"] ** 2 * rr ** 3 / (G * (rr ** 2 + RC ** 2)), c["Mcl"]); row[str(rr)] = G * Mx / rr ** 2 / gl
        D[f"D3|{f}|Mb{Mb:.0e}"] = row
        P(f"    [{f:9s}] M_b {Mb:.0e}: " + "  ".join(f"r {float(k) / 1e3:.1f} kpc {v:.2e}" for k, v in row.items()))

P("\n  D4  Chandrasekhar sinking time of one clump in a flat host (lnLambda = 5; estimate)")
for f in FOOTS:
    Vh = (G * 6e10 * A0[f]) ** 0.25; c = CL[f]
    row = {str(rr): 1.17 * rr ** 2 * Vh / (G * c["Mcl"] * 5.0) / 1e3 for rr in (1000.0, 3000.0, 10000.0)}
    D[f"D4|{f}"] = row
    P(f"    [{f:9s}] host M_b 6e10 (V_h {Vh / KMS:.0f} km/s): t_df = " + ", ".join(f"{float(k) / 1e3:.0f} kpc {v:.1f} Gyr" for k, v in row.items()))

P("\n  D5  clump scales (t = 0, alpha = 1, two-sided)")
for f in FOOTS:
    x_ = V1[f]["H2"]
    P(f"    [{f:9s}] rho_x0 = {rho_x0[f]:.3f} Msun/pc^3, tau(rho_x0) = {x_['tau_centre_Myr']:.2f} Myr, tau near r_t = {x_['tau_near_rt_Myr']:.1f} Myr;"
      f" psi_ex(0) = {x_['psi_ex_centre_kms2']:.1f} (km/s)^2; max |v_s| = {x_['vmax_alpha1_kms']:.1f} alpha km/s (H2);"
      f" T_ret 13.5 Gyr: alpha_50 {max(V1[f][h]['alpha50_T13p5'] for h in HOSTS):.2e}, alpha_c {max(V1[f][h]['alpha_c_T13p5'] for h in HOSTS):.2e} (max over hosts)")
    D[f"D5|{f}"] = dict(rho_x0=rho_x0[f])

P("\n  D6  big-galaxy condition under the smooth gate: overfill mass conserved (F_ret = 1) -> phi <= F_max (CFG881, massive, primary)")
try:
    R881 = json.load(open(os.path.join(LANES, "CFG881_sparc_clump_overfill_bound", "cfg881_results.json")))
    for f in FOOTS:
        row = {sh: R881[f]["summary"]["massive"][sh]["primary"]["F_med"] for sh in ("CORE1", "CORE3", "BARYON", "FLAT")}
        D[f"D6|{f}"] = row
        P(f"    [{f:9s}] phi_max = " + ", ".join(f"{k} {v:.2f}" for k, v in row.items()))
except (OSError, KeyError) as e:
    P(f"    CFG881 JSON not readable ({e}); D6 not computed")
RES["D"] = D

# ================================================================ summary
K2lab, K2max = max(mass_err, key=lambda z: z[1]); K2 = K2max <= 1e-12
RES["K2"] = dict(pass_=bool(K2), max_rel=K2max, worst_run=K2lab, n_runs=len(mass_err), per_run=dict(mass_err))
P(f"\n  K2 mass conservation over {len(mass_err)} runs: max |dM|/M = {K2max:.1e} ({K2lab}) -> {'PASS' if K2 else 'FAIL'}")
Kall = bool(K1 and K2 and K3 and K4 and K5 and K6 and K7 and K8 and K9_ok)
RES["K_all_pass"] = Kall
v1lab = {f: V1[f]["label"] for f in FOOTS}
if all(v == "EXCLUDED" for v in v1lab.values()) and lab2 == "GATED RETAINS" and M2 and not MUT:
    cls = "RETENTION REQUIRES THE GATE"
elif all(v == "COMPATIBLE" for v in v1lab.values()):
    cls = "TWO-SIDED RETAINS"
elif all(v == "EXCLUDED" for v in v1lab.values()) and lab2 == "GATED FAILS":
    cls = "NO RETENTION"
else:
    cls = f"MIXED (V1 {v1lab}, V2 {lab2}, M2 {'bites' if M2 else 'does not bite'})"
RES["class"] = cls
P(f"\n  V1: canonical {v1lab['canonical']}, alt {v1lab['alt']};  V2 ({mode2}): {lab2};  K all: {'PASS' if Kall else 'FAIL'}")
P(f"  CLASS: {cls}" + ("   [MUTATE run; the class is the control's, not the lane's]" if MUT else ""))
code = 0
if MUT:
    if RES.get("M1_bites"):
        P("  MUTATE: tooth M1 bites (inverted gate drains the clump) -> exit 1 as designed"); code = 1
    else:
        P("  MUTATE: tooth M1 DID NOT BITE")
P(f"  wall {time.time() - T0:.0f} s")
json.dump(RES, open(os.path.join(HERE, f"cfg882_results{SUF}.json"), "w"), indent=1, default=float)
open(os.path.join(HERE, f"cfg882{SUF}.out"), "w").write("\n".join(OUT) + "\n")
raise SystemExit(code)
