"""K1_braneworld_weyl (criteria e78d6d2516, amendments 7d3710054d): the owner's idea "cold energy is kind of like a black hole,
a dip into another dimension", read as the braneworld projected Weyl term E_mu_nu (a traceless 'Weyl fluid').
Part A (sympy): static spherical brane equations with the Weyl fluid (U, P); non-closure count; low-energy source; universal
slip; closures P = 0 (Tolman), P = wU (Mak-Harko / Harko-Cheng), P = -2U (DMPR brane black hole); FRW a^-4; DGP spherical root.
Part B: one constant per closure calibrated on F1 MID only (F1 PRIMARY, F1's measurement cache copied read-only, argv[1]);
predictions F1 OUTER, isolated galaxies (F2 masses), dwarf satellites (E3 CSV), Solar System (C6 bounds), BBN (A78).
Bulk-supplied lines: RS2 linear (Garriga-Tanaka) and DGP.  Literature equations are EXTERNAL, not verified on disk.
--mutate: the Weyl radial pressure is dropped from the rr equation (K1 and K3 must FAIL).
Deterministic, no network, single thread."""
import os, sys, json, time, pickle, hashlib, resource, csv, re
import numpy as np
import sympy as sp
_trap = getattr(np, "trapezoid", None) or np.trapz
T0 = time.time()
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(HERE))
MUT = "--mutate" in sys.argv; CACHE = [a for a in sys.argv[1:] if not a.startswith("--")][0]; TAG = "_MUTATE" if MUT else ""
OUTF = open(os.path.join(HERE, f"k1_braneworld_weyl{TAG}.out"), "w")
def say(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); OUTF.write(s + "\n"); OUTF.flush()
RES = {"mutate": MUT, "criteria_commit": "e78d6d2516", "amendments_commit": "7d3710054d"}; CHECKS = []
def check(name, ok, val, thr):
    CHECKS.append((name, bool(ok))); say(f"{name} {'PASS' if ok else 'FAIL'} {val} {thr}")
    RES.setdefault("checks", {})[name] = dict(pass_=bool(ok), value=str(val), threshold=str(thr))
def mem(tag):
    pk = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss; say(f"  [mem] {tag}: max RSS so far {pk/1e9 if sys.platform == 'darwin' else pk/1e6:.3f} GB, t = {time.time()-T0:.0f} s")
def iszero(e): return sp.simplify(e) == 0
import ctypes, gc
try: _LIBC = ctypes.CDLL(None); _LIBC.malloc_zone_pressure_relief.restype = ctypes.c_size_t
except Exception: _LIBC = None
def relieve():                                                 # macOS: hand freed blocks back to the OS (RSS hygiene only, as H2)
    gc.collect()
    if _LIBC is not None and sys.platform == "darwin": _LIBC.malloc_zone_pressure_relief(None, ctypes.c_size_t(0))
np.seterr(divide="ignore", over="ignore", invalid="ignore")   # Accelerate BLAS raises spurious FP flags in matmul; finiteness is asserted below

# ======================================================================================= PART A (sympy)
say("=== PART A: static spherical brane equations with the projected Weyl term (sympy) ===")
t_, r, th, ph = sp.symbols("t r theta phi", positive=True)
cS, GS = sp.symbols("c G", positive=True)
kap = 8*sp.pi*GS/cS**4
nu = sp.Function("nu")(r); la = sp.Function("lambda")(r)
XC = [t_, r, th, ph]
def einstein_mixed(gm):
    gi = gm.inv(); n = 4
    Gam = [[[sp.simplify(sum(gi[a, d]*(sp.diff(gm[d, b], XC[cc]) + sp.diff(gm[d, cc], XC[b]) - sp.diff(gm[b, cc], XC[d])) for d in range(n))/2)
             for cc in range(n)] for b in range(n)] for a in range(n)]
    Ric = sp.zeros(n)
    for b in range(n):
        for d in range(n):
            Ric[b, d] = sp.simplify(sum(sp.diff(Gam[a][b][d], XC[a]) for a in range(n)) - sum(sp.diff(Gam[a][b][a], XC[d]) for a in range(n))
                                    + sum(Gam[a][a][e]*Gam[e][b][d] for a in range(n) for e in range(n))
                                    - sum(Gam[a][d][e]*Gam[e][b][a] for a in range(n) for e in range(n)))
    Rs = sp.simplify(sum(gi[b, d]*Ric[b, d] for b in range(n) for d in range(n)))
    return sp.simplify(gi*(Ric - gm*Rs/2)), Gam
GMX, GAM = einstein_mixed(sp.diag(-sp.exp(nu)*cS**2, sp.exp(la), r**2, r**2*sp.sin(th)**2))
def div_r(Tm, Gam=None):
    Gm_ = Gam or GAM; n = 4; b = 1
    return sp.simplify(sum(sp.diff(Tm[m, b], XC[m]) for m in range(n)) + sum(Gm_[m][m][l]*Tm[l, b] for m in range(n) for l in range(n))
                       - sum(Gm_[l][m][b]*Tm[m, l] for m in range(n) for l in range(n)))
rho = sp.Function("rho")(r); p = sp.Function("p")(r); U = sp.Function("U")(r); P = sp.Function("P")(r)
prW = (U + 2*P)*cS**2/3; ptW = (U - P)*cS**2/3
prW_used = sp.Integer(0) if MUT else prW                      # MUTATE: Weyl radial pressure dropped from the rr equation
TW = sp.diag(-U*cS**2, prW_used, ptW, ptW); TB = sp.diag(-rho*cS**2, p, p, p); TT = TW + TB
E = GMX - kap*TT
bian = div_r(GMX)
ident = sp.simplify(div_r(E) - (sp.diff(E[1, 1], r) + sp.diff(nu, r)/2*(E[1, 1] - E[0, 0]) + 2/r*(E[1, 1] - E[2, 2])))
weyl_cons = div_r(TW)
frozen_cons = cS**2*(sp.diff(U + 2*P, r)/3 + sp.diff(nu, r)*(4*U + 2*P)/6 + 2*P/r)
res_cons = sp.simplify(weyl_cons - frozen_cons)
m = sp.Function("m")(r)
lam_m = -sp.log(1 - 2*GS*m/(r*cS**2))
Ett = sp.simplify(E[0, 0].subs({U: 0, P: 0}).subs(la, lam_m).doit().subs(sp.Derivative(m, r), 4*sp.pi*r**2*rho))
nup_tov = 2*GS*(m + 4*sp.pi*r**3*p/cS**2)/(r**2*cS**2*(1 - 2*GS*m/(r*cS**2)))
Err = sp.simplify(E[1, 1].subs({U: 0, P: 0}).subs(la, lam_m).doit().subs(sp.Derivative(nu, r), nup_tov))
say(f"  Bianchi div(G)_r = {bian};  divergence identity residual = {ident}")
say(f"  TOV limit (U = P = 0): tt residual {Ett}, rr residual {Err} (with e^-lambda = 1 - 2Gm/rc^2, m' = 4 pi r^2 rho, nu' = TOV)")
say(f"  Weyl conservation  div(T_W)_r  =  c^2 [ (U+2P)'/3 + nu'(4U+2P)/6 + 2P/r ]  residual: {res_cons}")
say("  unknowns {nu, lambda, U, P} (matter rho, p given with its own conservation); independent equations {tt, rr, Weyl conservation};")
say("  the theta-theta equation follows from them by the divergence identity (Bianchi). Free functions: 4 - 3 = 1 (the non-closure).")
k1_ok = bian == 0 and ident == 0 and Ett == 0 and Err == 0 and res_cons == 0
check("K1", k1_ok, f"Bianchi {bian}, identity {ident}, TOV tt {Ett} rr {Err}, Weyl conservation residual {sp.simplify(res_cons)}; unknowns-equations = 1",
      "all residuals 0")
RES["A1"] = dict(unknowns=["nu", "lambda", "U", "P"], equations=["tt", "rr", "Weyl conservation"], free_functions=1,
                 weyl_conservation="(U+2P)'/3 + nu'(4U+2P)/6 + 2P/r = 0",
                 closure_needed="one function (P, or an equation of state P(U)) must come from the bulk solution or be POSTULATED")
# ---------------------------------------------------------------- K2: closures
w = sp.symbols("w", real=True); C1s, Qs, Ms = sp.symbols("C1 Q M")
lead = frozen_cons.subs(sp.Derivative(nu, r), 0)/cS**2                          # leading order in Phi/c^2
s0 = sp.dsolve(sp.Eq(sp.solve(frozen_cons.subs(P, 0), sp.Derivative(U, r))[0] - sp.Derivative(U, r), 0), U)
k2a = not sp.simplify(s0.rhs*sp.exp(2*nu)).has(r)
sw = sp.dsolve(sp.Eq(lead.subs(P, w*U).doit(), 0), U)
expo = sp.simplify(sp.diff(sp.log(sw.rhs), r)*r)
k2b = iszero(expo + 6*w/(1 + 2*w)) and expo.subs(w, 1) == -2 and expo.subs(w, -2) == -4
f_ = 1 - 2*GS*Ms/(r*cS**2) + Qs/r**2
gd = sp.diag(-f_*cS**2, 1/f_, r**2, r**2*sp.sin(th)**2)
GD, _ = einstein_mixed(gd)
Ud = sp.simplify(-GD[0, 0]/(kap*cS**2)); prd = sp.simplify(GD[1, 1]/kap); ptd = sp.simplify(GD[2, 2]/kap)
Pd = sp.simplify((3*prd/cS**2 - Ud)/2)
k2c = iszero(prd + 2*ptd - Ud*cS**2) and iszero(Pd + 2*Ud) and iszero(Ud - Qs*cS**2/(8*sp.pi*GS*r**4))
say(f"  C0 (P = 0, exact): U = {s0.rhs}   [Tolman radiation; linear: dU = -4 U_inf psi / c^2]")
say(f"  C1 (P = wU, leading order): U = {sw.rhs};  r dlnU/dr = {expo}  -> w = 1 gives {expo.subs(w, 1)} (flat rotation, HC), w = -2 gives {expo.subs(w, -2)}")
say(f"  C2 (DMPR, e^nu = e^-lambda = 1 - 2GM/rc^2 + Q/r^2, vacuum): U = {Ud}, P = {Pd}, traceless {sp.simplify(prd + 2*ptd - Ud*cS**2)}")
kk = sp.symbols("k", positive=True); rr_ = sp.symbols("rr", positive=True)
ft_inv_r2 = sp.integrate(4*sp.pi*rr_**2*sp.sin(kk*rr_)/(kk*rr_)/rr_**2, (rr_, 0, sp.oo))
say(f"  C2 kernel (A2): FT of 1/r^2 in 3D = {sp.simplify(ft_inv_r2)}  -> Phi_W,k = -G l (2 pi^2/k) rho_k, rho_eff = (pi l/2)(-Lap)^(1/2) rho_b (density-gradient-like)")
check("K2", k2a and k2b and k2c, f"P=0: U ~ exp(-2 nu) {k2a}; P=wU: r^(-6w/(1+2w)) {k2b}; DMPR P=-2U, U = Qc^2/(8 pi G r^4) exactly {k2c}", "all True")
RES["A4"] = dict(C0="U = U_ref exp(-2(nu - nu_ref)); dU = -4 U_inf psi/c^2", C1_exponent=str(expo), C2_U=str(Ud), C2_P=str(Pd),
                 C2_kernel_FT=str(sp.simplify(ft_inv_r2)), C2_rho_eff="(pi l_Q/2)(-Lap)^(1/2) rho_b")
# ---------------------------------------------------------------- K3: slip and the C0 mass term
TrrW = TW[1, 1]; cons_lo = sp.simplify(weyl_cons.subs(sp.Derivative(nu, r), 0))
dMdyn = 4*sp.pi*r**2*(rho + U) + 4*sp.pi*sp.diff(r**3*TrrW, r)/cS**2
solP = sp.solve(cons_lo, sp.Derivative(P, r)) if cons_lo.has(sp.Derivative(P, r)) else []
if solP: dMdyn = dMdyn.subs(sp.Derivative(P, r), solP[0])
dMlens = (dMdyn + 4*sp.pi*r**2*(rho + U))/2
coef_dyn = sp.simplify(dMdyn.subs(rho, 0)/(4*sp.pi*r**2*U)); coef_lens = sp.simplify(dMlens.subs(rho, 0)/(4*sp.pi*r**2*U))
Uinf = sp.symbols("U_inf", positive=True)
mu2 = sp.simplify(4*sp.pi*GS*coef_dyn*4*Uinf/cS**2)
k3 = coef_dyn == 2 and coef_lens == sp.Rational(3, 2) and iszero(mu2 - 32*sp.pi*GS*Uinf/cS**2)
say(f"  slip: dM_dyn/dr = 4 pi r^2 x {coef_dyn} U, dM_lens/dr = 4 pi r^2 x {coef_lens} U, dM_lambda/dr = 4 pi r^2 x 1 U  (Weyl lensing/dynamics = {sp.simplify(coef_lens/coef_dyn)})")
say(f"  C0 linearised: Lap psi + mu_W^2 psi = 4 pi G rho_b with mu_W^2 = {mu2}  (relativistic Jeans wavenumber of the dark radiation)")
check("K3", k3, f"coefficients dyn {coef_dyn}, lens {coef_lens}; mu_W^2 = {mu2}", "2, 3/2; 32 pi G U_inf / c^2")
RES["A3"] = dict(coef_dyn=str(coef_dyn), coef_lens=str(coef_lens), coef_curv="1", lens_over_dyn=str(sp.simplify(coef_lens/coef_dyn)), mu_W2=str(mu2))
# ---------------------------------------------------------------- K4: FRW + A78 factor
tt = sp.symbols("t"); a_ = sp.Function("a")(tt); rw = sp.Function("rho_W")(tt)
sfrw = sp.dsolve(sp.Eq(sp.diff(rw, tt) + 3*sp.diff(a_, tt)/a_*(rw + rw/3), 0), rw)
k4a = iszero(sp.diff(sp.log(sfrw.rhs), tt) + 4*sp.diff(a_, tt)/a_)
XW = 7/8*(4/11)**(4/3); NEFF = 3.046; DNEFF_BND = 0.30; OMG_H2 = 2.469e-5
fac = (1 + XW*NEFF)/XW
a78 = open(os.path.join(REPO, "deepseek_push", "DS_FINAL_2026_10_21", "A78_beta_closure", "a78.out")).read()
fa78 = float(re.search(r"Delta N_eff = \(f-1\)\(1\+x N_eff\)/x = ([0-9.]+) \(f-1\)", a78).group(1))
say(f"  FRW: traceless conserved isotropic Weyl term: rho_W = {sfrw.rhs}  (w = 1/3, dark radiation; it cannot be the growth dust)")
check("K4", k4a and abs(fac - fa78) < 1e-4, f"rho_W ~ a^-4 {k4a}; (1 + x N_eff)/x = {fac:.5f} vs A78 {fa78}", "True; |diff| < 1e-4")
RES["A5"] = dict(rho_W=str(sfrw.rhs), w="1/3", dust="no: a w = 1/3 term cannot be the CDM-like dust; v4's dust is still required", A78_factor=fac)
# ---------------------------------------------------------------- DGP spherical root (B2, external equation)
bb, rc_, GMs, phs = sp.symbols("beta r_c GM phip", positive=True)
lhs_op = lambda f: 3*bb*(sp.diff(f, r, 2) + 2*sp.diff(f, r)/r) + (rc_**2/cS**2)*((sp.diff(f, r, 2) + 2*sp.diff(f, r)/r)**2 - (sp.diff(f, r, 2)**2 + 2*sp.diff(f, r)**2/r**2))
phf = sp.Function("phi")(r)
first_int = 3*bb*r**2*sp.diff(phf, r) + 2*(rc_**2/cS**2)*r*sp.diff(phf, r)**2
dgp_id = sp.simplify(sp.diff(first_int, r) - r**2*lhs_op(phf))
root = [s_ for s_ in sp.solve(sp.Eq(3*bb*r**2*phs + 2*(rc_**2/cS**2)*r*phs**2, 2*GMs), phs) if sp.simplify(s_.subs({bb: 1, rc_: 1, cS: 1, GMs: 1, r: 1})) > 0][0]
say(f"  DGP (decoupling limit, EXTERNAL): d/dr[3 beta r^2 phi' + 2 (r_c/c)^2 r phi'^2] - r^2 x operator = {dgp_id}; phi' = {root}")
RES["DGP_root"] = str(root)

# ---------------------------------------------------------------- A2: low-energy source ratio rho / lambda_b
MEVJ = 1.602176634e-13; HBARC = 197.3269804*1e-15                                  # MeV m
LAMB = (1e6)**4/(HBARC**3)*MEVJ/(2.998e8)**2                                        # (1 TeV)^4 as a mass density, kg/m^3
RES["lambda_b_kg_m3"] = LAMB

# ======================================================================================= PART B (numbers)
say("\n=== PART B: calibration on F1 MID, predictions with no refit ===")
G = 6.674e-11; C = 2.998e8; MSUN = 1.989e30; MPC = 3.0857e22; KG_PC2 = MSUN/(3.0857e16)**2; KPC = MPC/1e3; PC = 3.0857e16; AU = 1.495978707e11
A0 = {"canonical": 9.3603e-11, "alt": 1.1312e-10}                                    # kappa = 1/2 FITTED
FEET = ("canonical", "alt")
RHOC100 = 3*(100e3/MPC)**2/(8*np.pi*G)                                               # kg/m^3 per h^2
from scipy.interpolate import PchipInterpolator
# --- F1 conventions (copied from rebuild_2026_10_22/F1_cluster_cores/f1_cluster_cores.py, read-only)
zb_ = [0.510, 0.706, 0.934, 1.321, 1.484, 2.330]; DMr = [13.588, 17.351, 21.576, 27.601, 30.512, 38.988]
DHb = 21.863 + (21.863 - 19.455)/(0.706 - 0.510)*(0.510 - 0.295); DMb = np.sqrt(7.942**3/(0.295*DHb))
PCH = PchipInterpolator(np.r_[0, 0.295, zb_], np.r_[0, DMb, DMr]); HRD = 101.54
def DM(z, h): return PCH(np.minimum(np.asarray(z, float), 2.33))*HRD/h
def DA_lcdm(z, H0=70.0, Om=0.3):
    zz = np.linspace(0, z, 600); E_ = np.sqrt(Om*(1 + zz)**3 + 1 - Om); return _trap(1/E_, zz)*C/1e3/H0/(1 + z)
HS = {"h0672": 0.672, "h0686": 0.686}
EDGES = np.logspace(np.log10(0.15), np.log10(3.0), 9); RC = np.sqrt(EDGES[1:]*EDGES[:-1])
BANDS = {"INNER": [0, 1, 2], "MID": [3, 4, 5], "OUTER": [6, 7]}
RG = np.logspace(-3, np.log10(30), 3000); RF = np.logspace(np.log10(2e-3), np.log10(3.5), 90); UU = np.linspace(0, 1, 2001)
RGm = RG*MPC
def g_aqual_sph(gN, a0): return 0.5*gN + np.sqrt(0.25*gN**2 + gN*a0)
def project(rho_, r_=RG):
    lr = np.log(r_); pos = rho_ > 0; lrho = np.log(np.where(pos, rho_, 1e-300))
    umax = np.arccosh(r_[-1]/RF); u = UU[None, :]*umax[:, None]; rr = RF[:, None]*np.cosh(u)
    Sig = 2*_trap(np.exp(np.interp(np.log(rr), lr[pos], lrho[pos]))*rr*MPC, u, axis=1)
    cum = np.r_[0.5*Sig[0]*RF[0]**2, 0.5*Sig[0]*RF[0]**2 + np.cumsum(0.5*(Sig[1:]*RF[1:] + Sig[:-1]*RF[:-1])*np.diff(RF))]
    return Sig, 2*cum/RF**2 - Sig
def offset(Sig, d):
    if d <= 1e-4: return Sig
    ph_ = np.linspace(0, np.pi, 181); Rp = np.sqrt(RF[:, None]**2 + d**2 + 2*RF[:, None]*d*np.cos(ph_[None, :]))
    return _trap(np.exp(np.interp(np.log(Rp), np.log(RF), np.log(Sig))), ph_, axis=1)/np.pi
def dsig_from_sig(Sig):
    cum = np.r_[0.5*Sig[0]*RF[0]**2, 0.5*Sig[0]*RF[0]**2 + np.cumsum(0.5*(Sig[1:]*RF[1:] + Sig[:-1]*RF[:-1])*np.diff(RF))]
    return 2*cum/RF**2 - Sig
def at_bins(ds): return np.exp(np.interp(np.log(RC), np.log(RF), np.log(np.maximum(ds, 1e-30))))
def gas_mass(Mg500, R500):                                                           # F1 shape G0 (beta = 2/3, rc = 0.15 R500, to 3 Mpc)
    rc = 0.15*R500; sh = (1 + (RG/rc)**2)**(-1.0); sh[RG > 3.0] = 0
    dm = 4*np.pi*(RG*MPC)**2*sh; M = np.r_[0, np.cumsum(0.5*(dm[1:] + dm[:-1])*np.diff(RG*MPC))]
    return M*(Mg500*MSUN/np.interp(R500, RG, M))
# --- F1's measurement (read-only copy)
PKL = os.path.join(CACHE, "f1_meas.pkl"); SHA = hashlib.sha256(open(PKL, "rb").read()).hexdigest()
MEAS = pickle.load(open(PKL, "rb")); N = len(MEAS)
order = np.argsort([o["ra"] for o in MEAS]); PATCH = np.empty(N, int); PATCH[order] = np.arange(N)*30//N
def arr(key, f): return np.array([o[key][f] for o in MEAS])
def A_band(D, P_, W, sel): return {b: float((W[sel][:, j]*D[sel][:, j]).sum()/(W[sel][:, j]*P_[sel][:, j]).sum()) for b, j in BANDS.items()}
def jk(D, P_, W):
    full = A_band(D, P_, W, np.ones(N, bool)); reps = [A_band(D, P_, W, PATCH != q) for q in range(30)]
    return {b: (full[b], float(np.sqrt(29/30*np.sum((np.array([x[b] for x in reps]) - np.mean([x[b] for x in reps]))**2)))) for b in full}
DAT = {}
for hk in HS:
    Eh = arr(hk, "E"); DAT[hk] = dict(D=arr(hk, "D"), W=np.where(Eh < 1e8, 1/Eh**2, 0), B=arr(hk, "den").sum(0)/arr(hk, "den_r").sum(0))
def Dd(hk, boost=True): return DAT[hk]["D"]*(DAT[hk]["B"][None, :] if boost else 1.0)
PB = [3, 4, 5, 6, 7]; HARTLAP = (30 - len(PB) - 2)/29
def chi2_prof(hk, P_, boost=True):
    Dx = Dd(hk, boost); W = DAT[hk]["W"]
    f = lambda sel: (W[sel][:, PB]*(Dx[sel][:, PB] - P_[sel][:, PB])).sum(0)/W[sel][:, PB].sum(0)
    s0 = f(np.ones(N, bool)); reps = np.array([f(PATCH != q) for q in range(30)]); Cv = 29/30*(reps - reps.mean(0)).T @ (reps - reps.mean(0))
    return float(HARTLAP*s0 @ np.linalg.solve(Cv, s0))
# --- baryons and the law, F1 PRIMARY (AQUAL, native h, gas rescaled, beta-model, f* 0.20, miscentring)
MB, MISD = {}, {}
for hk, h in HS.items():
    mb, mis = [], []
    for o in MEAS:
        q = (float(DM(o["z"], h))/(1 + o["z"]))/DA_lcdm(o["z"]); mb.append(gas_mass(o["Mgas500"]*q**2.5, o["R500"]*q)*1.20)
        mis.append(np.radians(o["off_deg"])*float(DM(o["z"], h))/(1 + o["z"]))
    MB[hk], MISD[hk] = np.array(mb), np.array(mis)
GL, LAWP = {}, {}
for hk in HS:
    for f in FEET:
        g = g_aqual_sph(G*MB[hk]/RGm**2, A0[f]); GL[(hk, f)] = g; out = []
        for i in range(N):
            ML = g[i]*RGm**2/G; rho_ = np.gradient(ML, RGm)/(4*np.pi*RGm**2); Sig, ds = project(rho_)
            out.append(at_bins(dsig_from_sig(offset(Sig, MISD[hk][i])))/KG_PC2)
        LAWP[(hk, f)] = np.array(out)
F1J = json.load(open(os.path.join(REPO, "rebuild_2026_10_22", "F1_cluster_cores", "f1_cluster_cores_results.json")))
dev = []
for hk in HS:
    for f in FEET:
        a = jk(Dd(hk), LAWP[(hk, f)], DAT[hk]["W"]); ref = F1J["rows"][f"PRIMARY {hk}"][f]
        dev += [abs(a["MID"][0]/ref["MID"][0] - 1), abs(a["OUTER"][0]/ref["OUTER"][0] - 1)]
        say(f"  law {hk} {f:9s}: A_MID {a['MID'][0]:.4f}+-{a['MID'][1]:.4f} (F1 {ref['MID'][0]:.4f})  A_OUTER {a['OUTER'][0]:.4f}+-{a['OUTER'][1]:.4f} (F1 {ref['OUTER'][0]:.4f})  chi2_prof {chi2_prof(hk, LAWP[(hk, f)]):.1f}")
check("K5", SHA.startswith("961ea4fc") and SHA.endswith("e720") and max(dev) <= 1e-6, f"sha {SHA[:8]}...{SHA[-4:]}, max rel dev {max(dev):.1e} over 4 cells x MID/OUTER", "sha 961ea4fc...e720; <= 1e-6")
relieve(); mem("law built")
# --- signed linear operators (rho on RG -> binned DeltaSigma), my implementation of F1's projector with linear interpolation
def interp_weights(xq, xg):
    xq = np.clip(xq, xg[0], xg[-1]); i = np.clip(np.searchsorted(xg, xq) - 1, 0, len(xg) - 2); return i, (xq - xg[i])/(xg[i + 1] - xg[i])
def build_P():
    lr = np.log(RG); Pm = np.zeros((len(RF), len(RG))); umax = np.arccosh(RG[-1]/RF); wu = np.full(len(UU), UU[1] - UU[0]); wu[[0, -1]] *= 0.5
    for j in range(len(RF)):
        u = UU*umax[j]; rr = RF[j]*np.cosh(u); wgt = 2*wu*umax[j]*rr*MPC
        i, t = interp_weights(np.log(rr), lr); np.add.at(Pm[j], i, wgt*(1 - t)); np.add.at(Pm[j], i + 1, wgt*t)
    return Pm
def build_O(d):
    n = len(RF)
    if d <= 1e-4: return np.eye(n)
    O = np.zeros((n, n)); ph_ = np.linspace(0, np.pi, 181); wp = np.full(181, ph_[1] - ph_[0]); wp[[0, -1]] *= 0.5
    for j in range(n):
        Rp = np.sqrt(RF[j]**2 + d**2 + 2*RF[j]*d*np.cos(ph_)); i, t = interp_weights(np.log(Rp), np.log(RF))
        np.add.at(O[j], i, wp*(1 - t)/np.pi); np.add.at(O[j], i + 1, wp*t/np.pi)
    return O
def interp_matrix(xq, xg):
    Mx = np.zeros((len(xq), len(xg))); i, t = interp_weights(xq, xg); Mx[np.arange(len(xq)), i] += 1 - t; Mx[np.arange(len(xq)), i + 1] += t; return Mx
Pm = build_P(); Dm = np.stack([dsig_from_sig(c_) for c_ in np.eye(len(RF))], 1); Bm = interp_matrix(np.log(RC), np.log(RF)); BD = Bm @ Dm
TOP = {}
for hk in HS:
    T_ = np.empty((N, len(RC), len(RG)))
    for i, d in enumerate(MISD[hk]): T_[i] = BD @ build_O(d) @ Pm
    TOP[hk] = T_; relieve()
assert np.isfinite(Pm).all() and np.isfinite(BD).all() and all(np.isfinite(TOP[hk]).all() for hk in HS)
def predW(hk, rhoL): return np.matmul(TOP[hk], np.asarray(rhoL)[..., None])[..., 0]/KG_PC2
def rho_from_M(Mr): return np.gradient(Mr, RGm, axis=-1)/(4*np.pi*RGm**2)
dk6 = []
for hk in HS:
    for f in FEET:
        PL = predW(hk, rho_from_M(GL[(hk, f)]*RGm**2/G)); a1 = jk(Dd(hk), PL, DAT[hk]["W"]); a0_ = jk(Dd(hk), LAWP[(hk, f)], DAT[hk]["W"])
        dk6 += [abs(a1[b][0]/a0_[b][0] - 1) for b in ("MID", "OUTER")]
check("K6", max(dk6) <= 0.005, f"linear vs F1 projector, max rel band deviation {max(dk6):.2e}", "<= 0.005")
mem("operators built")

# ---------------------------------------------------------------- closure machinery
_BUF = {}
IREF = int(np.argmin(np.abs(RG - 3.0))); IREF10 = int(np.argmin(np.abs(RG - 10.0))); HX = np.diff(np.log(RGm))
def c0_bvp(gl, Uinf, iref=IREF, reuse=False):
    """exact linear BVP (feedback): psi' = g_law + 2 G m/r^2, m' = 4 pi r^2 dU, dU = -4 U psi/c^2 (r <= r_ref), m(r0) = 0, psi(r_ref) = 0.
    Heun in ln r on RG; particular (psi(r0) = 0) + homogeneous (psi(r0) = 1) solutions, contiguous step-major buffers (RSS hygiene).
    Returns psi (n, Nr, zero beyond r_ref), dU (n, Nr), m_W (n, Nr)."""
    gl = np.atleast_2d(gl); n = gl.shape[0]; k = 16*np.pi*Uinf/C**2
    if _BUF.get("key") != (n, iref):
        _BUF.clear(); relieve(); _BUF.update(key=(n, iref), ps=np.empty((iref + 1, 2, n)), mm=np.empty((iref + 1, 2, n)), src=np.empty((iref + 1, 2, n)),
                                             T1=np.empty((n, iref + 1)), PSI=np.zeros((n, len(RG))), dU=np.zeros((n, len(RG))))
    ps, mm, src = _BUF["ps"], _BUF["mm"], _BUF["src"]; ps[...] = 0; mm[...] = 0; ps[0, 1] = 1.0; src[:, 0] = gl[:, :iref + 1].T; src[:, 1] = 0
    for i in range(iref):
        r0, r1, h = RGm[i], RGm[i + 1], HX[i]
        f0p = r0*(src[i] + (2*G/r0**2)*mm[i]); f0m = (-k*r0**3)*ps[i]
        pp = ps[i] + h*f0p; mp = mm[i] + h*f0m
        f1p = r1*(src[i + 1] + (2*G/r1**2)*mp); f1m = (-k*r1**3)*pp
        ps[i + 1] = ps[i] + 0.5*h*(f0p + f1p); mm[i + 1] = mm[i] + 0.5*h*(f0m + f1m)
    cc = -ps[iref, 0]/ps[iref, 1]
    if reuse:                                                   # calibration scan: write into persistent buffers (no fresh large arrays)
        PSI, dU, T1 = _BUF["PSI"], _BUF["dU"], _BUF["T1"]; PSI[:, :iref + 1] = ps[:, 0].T
        np.multiply(ps[:, 1].T, cc[:, None], out=T1); PSI[:, :iref + 1] += T1; np.multiply(PSI, -4*Uinf/C**2, out=dU); return PSI, dU, None
    PSI = np.zeros((n, len(RG))); PSI[:, :iref + 1] = (ps[:, 0] + cc[None, :]*ps[:, 1]).T; dU = -4*Uinf*PSI/C**2
    MW = np.empty((n, len(RG))); MW[:, :iref + 1] = (mm[:, 0] + cc[None, :]*mm[:, 1]).T; MW[:, iref + 1:] = MW[:, iref:iref + 1]
    return PSI, dU, MW
def c0_testfluid_psi(gl, iref=IREF):
    gl = np.atleast_2d(gl); Q = np.concatenate([np.zeros((gl.shape[0], 1)), np.cumsum(0.5*(gl[:, 1:] + gl[:, :-1])*np.diff(RGm), axis=1)], axis=1)
    psi = -(Q[:, iref:iref + 1] - Q); psi[:, iref + 1:] = 0; return psi
SMID = np.r_[RG[0]/2, np.sqrt(RG[1:]*RG[:-1])]*MPC
KMAT = np.empty((len(RG), len(SMID)))
for i0 in range(0, len(RG), 200):
    Ri = RGm[i0:i0 + 200, None]; KMAT[i0:i0 + 200] = (1/(2*Ri*SMID[None, :]))*np.log((Ri + SMID[None, :])/np.abs(Ri - SMID[None, :]))
assert np.isfinite(KMAT).all(); relieve()
def c2_fields(Mr, ell):
    """tidal-charge kernel: Phi_W = -G ell sum dm K(r,s); returns Phi_W, M_dyn,W = r^2 dPhi/dr / G, lensing density 0.75 rho_dyn."""
    Mr = np.atleast_2d(Mr); dm = np.concatenate([Mr[:, :1], np.diff(Mr, axis=1)], axis=1); PhiW = np.empty_like(dm)
    for i0 in range(0, len(dm), 64): PhiW[i0:i0 + 64] = -G*ell*(dm[i0:i0 + 64] @ KMAT.T)
    gin = np.gradient(PhiW, RGm, axis=1); Mdyn = gin*RGm**2/G
    return PhiW, Mdyn, 0.75*rho_from_M(Mdyn)
# K7: homogeneous solution and test-fluid limit
mu_t = 1.0/MPC; U_t = mu_t**2*C**2/(32*np.pi*G)
k = 16*np.pi*U_t/C**2; ph_ = np.zeros(IREF + 1); mh_ = np.zeros(IREF + 1); ph_[0] = 1.0
for i in range(IREF):
    r0, r1, h = RGm[i], RGm[i + 1], HX[i]; f0p = r0*2*G*mh_[i]/r0**2; f0m = -k*r0**3*ph_[i]; pp = ph_[i] + h*f0p; mp = mh_[i] + h*f0m
    ph_[i + 1] = ph_[i] + 0.5*h*(f0p + r1*2*G*mp/r1**2); mh_[i + 1] = mh_[i] + 0.5*h*(f0m - k*r1**3*pp)
xh = mu_t*RGm[:IREF + 1]; dh = np.max(np.abs(ph_ - np.sin(xh)/xh))
Usmall = (1e-3/(3*MPC))**2*C**2/(32*np.pi*G); gtest = GL[("h0672", "canonical")][:5]
_, dUe, _ = c0_bvp(gtest, Usmall); dUt = -4*Usmall*c0_testfluid_psi(gtest)/C**2
dtf = np.max(np.abs(dUe[:, :IREF] - dUt[:, :IREF]))/np.max(np.abs(dUt))
check("K7", dh <= 1e-4 and dtf <= 1e-3, f"homogeneous vs sin(mu r)/(mu r): {dh:.1e}; exact vs test fluid at mu r_ref = 1e-3: {dtf:.1e}", "<= 1e-4; <= 1e-3")
# K8: tidal kernel far field for a Plummer sphere (A1: r >= 100 b; 50 b printed)
bpl = 5*KPC; Mpl = 1e10*MSUN; Mplum = Mpl*RGm**3/(RGm**2 + bpl**2)**1.5
PhiP, MdP, _ = c2_fields(Mplum[None, :], MPC); ratio = PhiP[0]/(-G*Mpl*MPC/RGm**2)
sel100 = (RGm >= 100*bpl) & (RG <= 10); sel50 = (RGm >= 50*bpl) & (RG <= 10)
d100 = float(np.max(np.abs(ratio[sel100] - 1))); d50 = float(np.max(np.abs(ratio[sel50] - 1)))
check("K8", d100 <= 1e-3, f"max |Phi_W/(-GMl/r^2) - 1| at r >= 100 b: {d100:.1e} (at >= 50 b: {d50:.1e})", "<= 1e-3 (A1)")
relieve(); mem("closure machinery")

# ---------------------------------------------------------------- calibration on F1 MID
J = BANDS["MID"]
def amid(hk, Ptot, boost=True):
    W = DAT[hk]["W"]; return float((W[:, J]*Dd(hk, boost)[:, J]).sum()/(W[:, J]*Ptot[:, J]).sum())
def lin_cal(hk, f, P1, boost=True):
    W = DAT[hk]["W"]; return float(((W[:, J]*Dd(hk, boost)[:, J]).sum() - (W[:, J]*LAWP[(hk, f)][:, J]).sum())/(W[:, J]*P1[:, J]).sum())
MBTOT = {hk: MB[hk][:, IREF] for hk in HS}
CAL = {}; TEMPL = {}
for hk in HS:
    _, MdC2, rhoC2 = c2_fields(MB[hk], MPC); TEMPL[(hk, "C2")] = predW(hk, rhoC2); TEMPL[(hk, "C2_Mdyn")] = MdC2
    for f in FEET:
        vW2 = np.sqrt(G*MBTOT[hk]*A0[f])                                              # xi = 1 (MB in kg)
        rhoC1 = np.where(RG[None, :] <= RG[IREF], 0.75*vW2[:, None]/(4*np.pi*G*RGm[None, :]**2), 0.0); TEMPL[(hk, f, "C1")] = predW(hk, rhoC1)
        psi_tf = c0_testfluid_psi(GL[(hk, f)]); TEMPL[(hk, f, "C0tf")] = predW(hk, 1.5*(-4*psi_tf/C**2))   # per unit U_inf (kg/m^3)
        for cl in ("C1", "C2"):
            P1 = TEMPL[(hk, f, "C1")] if cl == "C1" else TEMPL[(hk, "C2")]
            CAL[(cl, hk, f)] = dict(const=lin_cal(hk, f, P1), const_clipped=lin_cal(hk, f, P1, boost=False))
        CAL[("C0tf", hk, f)] = dict(const=lin_cal(hk, f, TEMPL[(hk, f, "C0tf")]), const_clipped=lin_cal(hk, f, TEMPL[(hk, f, "C0tf")], boost=False))
relieve(); mem("linear calibrations")
def c0_amid(hk, f, Uinf, boost=True, iref=IREF):
    _, dU, _ = c0_bvp(GL[(hk, f)], Uinf, iref, reuse=True); dU *= 1.5; return amid(hk, LAWP[(hk, f)] + predW(hk, dU), boost)
LG = np.arange(-8, 12.0001, 0.1)
def c0_root(hk, f, boost=True, iref=IREF):
    rc0 = RHOC100*HS[hk]**2; prev = None
    for lg in LG:
        a = c0_amid(hk, f, rc0*10**lg, boost, iref); relieve()
        if prev is not None and (prev[1] - 1)*(a - 1) <= 0 and np.isfinite(a):
            lo, hi = prev[0], lg
            for _ in range(40):
                md = 0.5*(lo + hi); am = c0_amid(hk, f, rc0*10**md, boost, iref)
                (lo, hi) = (lo, md) if (prev[1] - 1)*(am - 1) <= 0 else (md, hi)
            return rc0*10**(0.5*(lo + hi))
        prev = (lg, a)
    return None
for hk in HS:
    for f in FEET:
        CAL[("C0", hk, f)] = dict(const=c0_root(hk, f), const_clipped=c0_root(hk, f, boost=False), const_rref10=c0_root(hk, f, iref=IREF10))
        say(f"  CAL {hk} {f:9s}: C0 U_inf = {CAL[('C0', hk, f)]['const']:.3e} kg/m^3 (test fluid {CAL[('C0tf', hk, f)]['const']:.3e}); "
            f"C1 xi = {CAL[('C1', hk, f)]['const']:.4f}; C2 l_Q = {CAL[('C2', hk, f)]['const']:.4f} Mpc")
relieve(); mem("C0 calibration")

# ---------------------------------------------------------------- predictions on the stack: O1
def stack_pred(cl, hk, f, const):
    if cl == "C0":
        _, dU, mW = c0_bvp(GL[(hk, f)], const); return LAWP[(hk, f)] + predW(hk, 1.5*dU), 1.5*mW, dU
    if cl == "C0tf": return LAWP[(hk, f)] + const*TEMPL[(hk, f, "C0tf")], None, None
    if cl == "C1":
        vW2 = const*np.sqrt(G*MBTOT[hk]*A0[f]); ML = np.where(RG[None, :] <= RG[IREF], 0.75*vW2[:, None]*RGm[None, :]/G, 0.75*vW2[:, None]*RGm[IREF]/G)
        return LAWP[(hk, f)] + const*TEMPL[(hk, f, "C1")], ML, None
    return LAWP[(hk, f)] + const*TEMPL[(hk, "C2")], 0.75*const*TEMPL[(hk, "C2_Mdyn")], None
O1 = {}; COMPACT = {}
for cl in ("C0", "C1", "C2", "C0tf"):
    for hk in HS:
        for f in FEET:
            cst = CAL[(cl, hk, f)]["const"]
            if cst is None or not np.isfinite(cst) or cst <= 0:
                O1[(cl, hk, f)] = dict(cal=False); say(f"  O1 {cl} {hk} {f}: CAL FAILS (no root)"); continue
            Pt, MLW, dU = stack_pred(cl, hk, f, cst); a = jk(Dd(hk), Pt, DAT[hk]["W"]); c2v = chi2_prof(hk, Pt)
            zo = (a["OUTER"][0] - 1)/a["OUTER"][1]; ok = abs(zo) <= 2 and c2v <= 11.07
            perbin = (Dd(hk)*DAT[hk]["W"]).sum(0)/(Pt*DAT[hk]["W"]).sum(0)
            O1[(cl, hk, f)] = dict(cal=True, const=cst, A=a, Z_OUTER=zo, chi2_prof=c2v, passes=ok, data_over_pred_per_bin=perbin.tolist(),
                                   A_MID_clipped=amid(hk, Pt, boost=False))
            say(f"  O1 {cl:4s} {hk} {f:9s}: A_INNER {a['INNER'][0]:.3f}  A_MID {a['MID'][0]:.3f}  A_OUTER {a['OUTER'][0]:.3f}+-{a['OUTER'][1]:.3f} (Z {zo:+.1f})  chi2_prof {c2v:.1f}  -> {'PASS' if ok else 'FAIL'}"
                + "   data/pred per bin " + " ".join(f"{x:.2f}" for x in perbin))
            if MLW is not None and hk == "h0672":
                gas = MB[hk]/1.2; out = {}
                for rr_v in (0.5, 1.0, 2.0, 3.0):
                    jx = int(np.argmin(np.abs(RG - rr_v))); out[f"{rr_v}"] = float(np.median(MLW[:, jx]/gas[:, jx]))
                tot = MLW[:, IREF]; half = [RG[np.argmax(MLW[i, :IREF + 1] >= 0.5*tot[i])] if tot[i] > 0 else np.nan for i in range(N)]
                ghalf = [RG[np.argmax(gas[i, :IREF + 1] >= 0.5*gas[i, IREF])] for i in range(N)]
                jh = int(np.argmin(np.abs(RG - 0.5))); inner = float(np.median(np.abs(MLW[:, 0])/np.abs(MLW[:, jh])))
                COMPACT[(cl, f)] = dict(ML_W_over_gas=out, r_half_W_median=float(np.nanmedian(half)), r_half_gas_median=float(np.median(ghalf)), inner_1kpc_over_0p5Mpc=inner)
                say(f"     A2 compactness {cl} {f}: M_lens,W/M_gas (median) at 0.5/1/2/3 Mpc = " + " / ".join(f"{v:.2f}" for v in out.values())
                    + f";  r_half(Weyl excess <3 Mpc) {np.nanmedian(half):.2f} Mpc vs gas {np.median(ghalf):.2f} Mpc; |M_W(<1 kpc)|/M_W(<0.5 Mpc) {inner:.1e}")
relieve(); mem("O1")

# ---------------------------------------------------------------- R1 isolated galaxies (F2 masses)
LMB = [10.36, 10.83, 11.01, 11.18]; BPL = 5*KPC
RB = {"O1": np.logspace(np.log10(0.4), np.log10(1.1), 25), "O2": np.logspace(np.log10(1.1), np.log10(2.6), 25)}
GOP = Dm @ Pm; SAMP = {b: interp_matrix(np.log(R_), np.log(RF)) for b, R_ in RB.items()}
MGAL = np.array([10**lm*MSUN*RGm**3/(RGm**2 + BPL**2)**1.5 for lm in LMB])
def band_int(rho_rows, Min):
    ds = rho_rows @ GOP.T + np.asarray(Min)[:, None]/(np.pi*(RF*MPC)**2)          # A3: mass inside RG[0] as a central point
    return {b: _trap(ds @ SAMP[b].T, np.log(RB[b]), axis=1) for b in RB}
_, MdGal2, rhoGal2 = c2_fields(MGAL, MPC)
def r1_ratios(cl, f, cst):
    gl = g_aqual_sph(G*MGAL/RGm**2, A0[f]); law = band_int(rho_from_M(gl*RGm**2/G), gl[:, 0]*RGm[0]**2/G)
    if cl == "C0": _, dU, _ = c0_bvp(gl, cst); wr = band_int(1.5*dU, np.zeros(len(LMB)))
    elif cl == "C1":
        vW2 = cst*np.sqrt(G*np.array([10**lm*MSUN for lm in LMB])*A0[f]); wr = band_int(np.where(RG[None, :] <= RG[IREF], 0.75*vW2[:, None]/(4*np.pi*G*RGm[None, :]**2), 0.0), 0.75*vW2*RGm[0]/G)
    else: wr = band_int(cst*rhoGal2, 0.75*cst*MdGal2[:, 0])
    return {b: (wr[b]/law[b]).tolist() for b in RB}
R1 = {}
for cl in ("C0", "C1", "C2"):
    for hk in HS:
        for f in FEET:
            if not O1[(cl, hk, f)]["cal"]: continue
            rat = r1_ratios(cl, f, CAL[(cl, hk, f)]["const"]); proj = None
            if cl == "C2":                                       # A3 (post-result): the projector cannot resolve C2's core/envelope cancellation
                gl_ = g_aqual_sph(G*MGAL/RGm**2, A0[f]); law_ = band_int(rho_from_M(gl_*RGm**2/G), gl_[:, 0]*RGm[0]**2/G); Mg_ = np.array([10**lm*MSUN for lm in LMB])
                proj = rat; rat = {b: (_trap((9/16)*Mg_[:, None]*CAL[(cl, hk, f)]['const']*MPC/(RB[b][None, :]*MPC)**3, np.log(RB[b]), axis=1)/law_[b]).tolist() for b in RB}
                say(f"     C2 projector value (not graded, A3): O1 " + " ".join(f"{x:.3f}" for x in proj["O1"]) + "  O2 " + " ".join(f"{x:.3f}" for x in proj["O2"]))
            mx = max(max(abs(x) for x in rat[b]) for b in rat)
            R1[(cl, hk, f)] = dict(ratios=rat, max=mx, passes=mx <= 0.14, projector_value_not_graded=proj)
            say(f"  R1 {cl} {hk} {f:9s}: Weyl/law O1 " + " ".join(f"{x:.3f}" for x in rat["O1"]) + "  O2 " + " ".join(f"{x:.3f}" for x in rat["O2"])
                + f"  -> {'PASS' if mx <= 0.14 else 'FAIL'} (max {mx:.3f} vs 0.14)")
mem("R1")
RQ = np.logspace(np.log10(0.05), np.log10(3.4), 700)
def dsig_projpot(PhiW, Mtot):
    umax = np.arccosh(RG[-1]/RQ); u = UU[None, :]*umax[:, None]; rr = RQ[:, None]*np.cosh(u)
    P2 = 2*_trap(np.interp(np.log(rr), np.log(RG), PhiW)*rr*MPC, u, axis=1)
    z1 = RQ*np.sinh(umax); P2 += -2*G*Mtot*(np.pi/2 - np.arctan(z1/RQ))/(RQ*MPC)             # analytic tail beyond 30 Mpc
    dP = np.gradient(P2, RQ*MPC); Mc = RQ*MPC*dP/(2*G); Sg = np.gradient(RQ*MPC*dP, RQ*MPC)/(4*np.pi*G*RQ*MPC)
    return np.interp(np.log(RC), np.log(RQ), Mc/(np.pi*(RQ*MPC)**2) - Sg)
XC2 = []
for i in range(0, N, 33):
    PhiW, MdW, rhoW = c2_fields(MB["h0672"][i:i + 1], MPC)
    tail = 1.0*MB["h0672"][i, -1]*MPC                                  # Phi_W -> -G l M_b/r^2 beyond 30 Mpc (l = 1 Mpc here)
    a_ = 0.75*dsig_projpot(PhiW[0], tail); b_ = (BD @ Pm @ rhoW[0])
    XC2.append((b_[3:]/a_[3:]).tolist())
XC2 = np.array(XC2); say("  A3 cross-check, cluster C2 template: projector / projected-potential, median over 10 clusters, bins 3-7: " + " ".join(f"{x:.3f}" for x in np.median(XC2, 0)))
RES["A3_C2_cluster_crosscheck"] = np.median(XC2, 0).tolist()

# ---------------------------------------------------------------- hosts (MW, M31) for C0 and the Solar System
MWM, M31M, AH, R0 = 6.0e10*MSUN, 1.0e11*MSUN, 3*KPC, 8.122*KPC
MHOST = {"MW": MWM*RGm**2/(RGm + AH)**2, "M31": M31M*RGm**2/(RGm + AH)**2}
# ---------------------------------------------------------------- R3 dwarf satellites (E3 CSV, A1 baseline)
E3R = list(csv.DictReader(open(os.path.join(REPO, "doors_push_2026_10_22", "E3_dwarf_excess", "e3_per_system.csv"))))
LVD = {}
for fn in ("lvd_dwarf_mw.csv", "lvd_dwarf_m31.csv", "lvd_dwarf_local_field.csv"):
    for x in csv.DictReader(open(os.path.join(REPO, "real_research", "data", "dsph", fn))):
        def fl(v):
            try: return float(v)
            except Exception: return np.nan
        LVD[x["name"]] = (fl(x["distance_gc"]), fl(x["distance_m31"]))
E3MC = {"canonical": 0.886, "alt": 0.846}
DW = {}
for f in FEET:
    rows = [x for x in E3R if x["footing"] == f]
    Ms_ = 10**np.array([float(x["logMstar"]) for x in rows]); r12 = (4/3)*np.array([float(x["rh_pc"]) for x in rows])*PC
    Md = np.array([float(x["M_dyn"]) for x in rows]); Bs = np.array([float(x["B_scr_L24"]) for x in rows]); Mp = Bs*Ms_/2
    host = [x["host"] for x in rows]; dist = np.array([LVD[x["name"]][1] if x["host"] == "M31" else LVD[x["name"]][0] for x in rows])*KPC
    DW[f] = dict(names=[x["name"] for x in rows], Ms=Ms_, r12=r12, Md=Md, Mp=Mp, host=host, dist=dist, base=np.log10(Md/Mp))
k9 = {f: float(np.median(DW[f]["base"])) for f in FEET}
check("K9", all(abs(k9[f] - E3MC[f]) <= 0.10 for f in FEET), f"central baseline median canonical {k9['canonical']:+.3f} / alt {k9['alt']:+.3f} vs E3 MC +0.886 / +0.846 (diff {k9['canonical']-0.886:+.3f} / {k9['alt']-0.846:+.3f}); N {len(DW['canonical']['Md'])}/{len(DW['alt']['Md'])}", "|diff| <= 0.10")
# unit Plummer for C2 (b = 1 Mpc, M = 1 Msun, l = 1 Mpc): M_dyn,W(<x b) = l M f(x)/b
_, MdU, _ = c2_fields((MSUN*RG**3/(RG**2 + 1)**1.5)[None, :], MPC); FX = float(np.interp(1.305, RG, MdU[0]/MSUN))
def dwarf_MW(cl, f, cst):
    d = DW[f]; out = np.zeros(len(d["Md"]))
    if cl == "C0":
        sol = {}
        for hn in ("MW", "M31"):
            gl = g_aqual_sph(G*MHOST[hn]/RGm**2, A0[f]); psi, _, _ = c0_bvp(gl[None, :], cst); sol[hn] = psi[0]
        for i in range(len(out)):
            hn = "M31" if d["host"][i] == "M31" else "MW"; psi_d = np.interp(d["dist"][i], RGm, sol[hn]) if d["dist"][i] < RGm[IREF] else 0.0
            dU = -4*cst*psi_d/C**2; own = 4*cst*G*d["Ms"][i]*MSUN/C**2*4*np.pi*(d["r12"][i]**2)      # own-potential bound: 4U GM/(r c^2) integrated (x2 dyn)
            out[i] = (2*(4*np.pi/3)*d["r12"][i]**3*dU + own)/MSUN
    elif cl == "C1":
        for i in range(len(out)):
            Mh = M31M if d["host"][i] == "M31" else MWM
            own = cst*np.sqrt(G*d["Ms"][i]*MSUN*A0[f])*d["r12"][i]/G
            hst = (4*np.pi/3)*d["r12"][i]**3*cst*np.sqrt(G*Mh*A0[f])/(4*np.pi*G*d["dist"][i]**2)
            out[i] = (own + hst)/MSUN
    else:
        for i in range(len(out)):
            Mh = M31M if d["host"][i] == "M31" else MWM; b_ = d["r12"][i]/1.305
            own = cst*MPC*d["Ms"][i]*MSUN*FX/b_
            hst = (4*np.pi/3)*d["r12"][i]**3*(-cst*MPC*Mh/(2*np.pi*d["dist"][i]**4))
            out[i] = (own + hst)/MSUN
    return out
R3 = {}
for cl in ("C0", "C1", "C2"):
    for hk in HS:
        for f in FEET:
            if not O1[(cl, hk, f)]["cal"]: continue
            MWd = dwarf_MW(cl, f, CAL[(cl, hk, f)]["const"]); d = DW[f]
            arg = 1 + MWd/d["Mp"]; rnew = d["base"] - np.log10(np.where(arg > 0, arg, np.nan)); med = float(np.nanmedian(rnew))
            R3[(cl, hk, f)] = dict(median=med, median_MW=float(np.median(MWd)), median_MW_over_Mpred=float(np.median(MWd/d["Mp"])), passes=abs(med) <= 0.26, n_nan=int(np.isnan(rnew).sum()))
            say(f"  R3 {cl} {hk} {f:9s}: median Weyl mass in r12 {np.median(MWd):.3e} Msun (x{np.median(MWd/d['Mp']):.2e} of the screened prediction); residual {np.median(d['base']):+.3f} -> {med:+.3f} dex -> {'PASS' if abs(med) <= 0.26 else 'FAIL'}")
mem("R3")

# ---------------------------------------------------------------- R5 Solar System (C6 bounds)
PLB = {"Earth": (1.0*AU, 8.7e-15), "Mars": (1.524*AU, 1.4e-15), "Saturn": (9.58*AU, 7.0e-15)}
c6src = open(os.path.join(REPO, "covariant_push_2026_10_22", "C6_literal_cassini", "c6_literal_cassini.py")).read()
assert '"Mars": (1.524 * AU, 1.4e-15)' in c6src and '"Earth": (1.0 * AU, 8.7e-15)' in c6src and '"Saturn": (9.58 * AU, 7.0e-15)' in c6src
def sun_acc(cl, f, cst, rr):
    if cl == "C0":
        gl = g_aqual_sph(G*MHOST["MW"]/RGm**2, A0[f]); psi, _, _ = c0_bvp(gl[None, :], cst); dUl = -4*cst*np.interp(R0, RGm, psi[0])/C**2
        return (8*np.pi/3)*G*dUl*rr + 16*np.pi*G**2*cst*MSUN/C**2
    if cl == "C1":
        return cst*np.sqrt(G*MSUN*A0[f])/rr + (4*np.pi/3)*G*rr*cst*np.sqrt(G*MWM*A0[f])/(4*np.pi*G*R0**2)
    return 2*G*MSUN*cst*MPC/rr**3
R5 = {}
for cl in ("C0", "C1", "C2"):
    for hk in HS:
        for f in FEET:
            if not O1[(cl, hk, f)]["cal"]: continue
            cst = CAL[(cl, hk, f)]["const"]; rats = {n_: float(sun_acc(cl, f, cst, rr)/bd) for n_, (rr, bd) in PLB.items()}
            aAU = sun_acc(cl, f, cst, AU); gam = -0.5*(aAU*AU**2/G)/MSUN
            R5[(cl, hk, f)] = dict(ratios=rats, gamma_minus_1=float(gam), passes=all(v < 1 for v in rats.values()))
            say(f"  R5 {cl} {hk} {f:9s}: a_W/bound Earth {rats['Earth']:.2e} Mars {rats['Mars']:.2e} Saturn {rats['Saturn']:.2e}; gamma-1 (slip, M_dyn,W(<1 AU)) {gam:.1e} -> {'PASS' if R5[(cl, hk, f)]['passes'] else 'FAIL'}")
mem("R5")

# ---------------------------------------------------------------- R4 BBN (C0 LINK only) and the BBN-capped native prediction
R4 = {}
for hk in HS:
    for f in FEET:
        cst = CAL[("C0", hk, f)]["const"]
        if cst is None: R4[(hk, f)] = dict(cal=False); continue
        om = cst/RHOC100; dn = om/(XW*OMG_H2); mu = np.sqrt(32*np.pi*G*cst/C**2)*MPC
        Umax = DNEFF_BND*XW*OMG_H2*RHOC100; _, dUm, _ = c0_bvp(GL[(hk, f)], Umax); PWm = predW(hk, 1.5*dUm); W = DAT[hk]["W"]
        frac = float((W[:, J]*PWm[:, J]).sum()/(W[:, J]*LAWP[(hk, f)][:, J]).sum()); need = amid(hk, LAWP[(hk, f)]) - 1
        R4[(hk, f)] = dict(U_cal=cst, Omega_W_h2=om, U_over_rhocrit=cst/(RHOC100*HS[hk]**2), dNeff=dn, mu_W_per_Mpc=mu, mu_r_ref=mu*3.0, passes=abs(dn) <= DNEFF_BND,
                           U_max_BBN=Umax, MID_excess_at_BBN_cap=frac, MID_excess_needed=need, shortfall_factor=need/frac if frac > 0 else np.inf,
                           U_cal_rref10=CAL[("C0", hk, f)]["const_rref10"], U_cal_clipped=CAL[("C0", hk, f)]["const_clipped"])
        say(f"  R4 C0 {hk} {f:9s}: U_inf = {cst/(RHOC100*HS[hk]**2):.3e} rho_crit -> Omega_W h^2 {om:.3e}, Delta N_eff {dn:.3e} (bound 0.30) -> {'PASS' if abs(dn) <= 0.3 else 'FAIL'}; "
            f"mu_W = {mu:.3f}/Mpc (mu r_ref {mu*3:.2f}); at the BBN cap the MID excess is {frac:.2e} of the law vs {need:.3f} needed (short by {need/frac:.2e})")
mem("R4")

# ---------------------------------------------------------------- bulk-supplied lines
needA = {f: F1J["rows"]["PRIMARY h0672"][f]["MID"][0] - 1 for f in FEET}
ELL = 1e-4; rB = 0.808*MPC
dyn_rs2 = 2*ELL**2/(3*rB**2); lens_rs2 = 0.5*ELL**2/rB**2; lens_rs2_log = lens_rs2*100
ell_need = rB*np.sqrt(needA["canonical"]/0.5)
B1 = dict(dyn=dyn_rs2, lens=lens_rs2, lens_with_log_factor_100=lens_rs2_log, needed=needA, shortfall=needA["canonical"]/lens_rs2_log,
          ell_needed_Mpc=ell_need/MPC, ell_needed_over_AU=ell_need/AU, ell_needed_over_bound=ell_need/ELL, passes=False)
say(f"\n  B1 RS2 (bulk-supplied, l <= 0.1 mm): dyn {dyn_rs2:.1e}, lens {lens_rs2:.1e} (x100 extended-source log factor: {lens_rs2_log:.1e}) at 0.808 Mpc vs needed {needA['canonical']:.3f}/{needA['alt']:.3f}"
    f" -> FAIL by {needA['canonical']/lens_rs2_log:.1e}. l needed ~ {ell_need/MPC:.2f} Mpc = {ell_need/ELL:.1e} x the table-top bound; gravity would be 5D below it (Solar System off by ~l/AU = {ell_need/AU:.1e})")
H0n = 67.9e3/MPC; rcD = C/H0n
froot = sp.lambdify((bb, rc_, cS, GMs, r), root, "numpy")
B2 = {}
for be in (1.0, 3.0):
    dc = float(froot(be, rcD, C, G*7.0e13*MSUN, rB))/2/(G*7.0e13*MSUN/rB**2); dg = float(froot(be, rcD, C, G*10**10.83*MSUN, rB))/2/(G*10**10.83*MSUN/rB**2)
    rv_c = (16*rcD**2*G*7.0e13*MSUN/(9*be**2*C**2))**(1/3)/MPC; rv_g = (16*rcD**2*G*10**10.83*MSUN/(9*be**2*C**2))**(1/3)/MPC
    B2[f"beta{be:g}"] = dict(delta_cluster=dc, delta_galaxy=dg, selector_ratio=dc/dg, r_V_cluster_Mpc=rv_c, r_V_galaxy_Mpc=rv_g, saturation=1/(3*be),
                            passes=dc >= 0.5*needA["canonical"])
    say(f"  B2 DGP beta {be:g} (r_c = c/H0): fractional boost at 0.808 Mpc: cluster 7e13 Msun {dc:.3f} (r_V {rv_c:.2f} Mpc), galaxy 10^10.83 {dg:.3f} (r_V {rv_g:.2f} Mpc);"
        f" cluster/galaxy {dc/dg:.2f} (<1 = anti-selector); max 1/(3 beta) = {1/(3*be):.3f} vs needed {needA['canonical']:.3f} -> {'PASS' if dc >= 0.5*needA['canonical'] else 'FAIL'}")
# ---------------------------------------------------------------- A2 numbers (low-energy source)
rho_cl = float(np.max(rho_from_M(MB["h0672"])[:, 1])); rho_gal = 3*10**11.18*MSUN/(4*np.pi*BPL**3); rho_sun = 1.5e5
say(f"\n  A2 low-energy source pi/T ~ rho/lambda_b (lambda_b = (1 TeV)^4 = {LAMB:.2e} kg/m^3): cluster centre {rho_cl/LAMB:.1e}, galaxy centre {rho_gal/LAMB:.1e}, solar centre {rho_sun/LAMB:.1e}")
RES["A2"] = dict(lambda_b=LAMB, cluster=rho_cl/LAMB, galaxy=rho_gal/LAMB, sun_centre=rho_sun/LAMB)

# ---------------------------------------------------------------- Part C (J1) and A2 (variables)
say("\n=== PART C / A2: what each closure's Weyl mass tracks ===")
PARTC = {}
for f in FEET:
    hk = "h0672"; cst = CAL[("C0", hk, f)]["const"]
    if cst is None: continue
    psi, dU, _ = c0_bvp(GL[(hk, f)], cst); med_psi = {rv: float(np.median(-psi[:, int(np.argmin(np.abs(RG - rv)))]/C**2)) for rv in (0.1, 0.5, 1.0, 2.0)}
    PARTC[f] = dict(C0_psi_over_c2_median=med_psi,
                    C0_galaxy_O2=R1[("C0", hk, f)]["ratios"]["O2"] if ("C0", hk, f) in R1 else None,
                    C0_dwarf_MW_over_Mpred=R3[("C0", hk, f)]["median_MW_over_Mpred"] if ("C0", hk, f) in R3 else None,
                    C0_sun_aW_over_gN_1AU=float(sun_acc("C0", f, cst, AU)/(G*MSUN/AU**2)))
    say(f"  {f:9s} C0: |psi|/c^2 median at 0.1/0.5/1/2 Mpc = " + " / ".join(f"{v:.2e}" for v in med_psi.values())
        + f"  (flat, like J1's |Phi|); Sun a_W/g_N(1 AU) {PARTC[f]['C0_sun_aW_over_gN_1AU']:.1e}")
RES["partC"] = PARTC
RES["variables"] = dict(C0="potential psi relative to r_ref (Tolman: dU = -4 U_inf psi/c^2); satellites: host depth (J1: wrong variable)",
                        C1="fixed power law r^-2 per object, amplitude from the object's own baryon mass (sqrt(G M_b a0)); satellites: own mass",
                        C2="baryon density gradient: rho_eff = (pi l_Q/2)(-Lap)^(1/2) rho_b; satellites: own structure l_Q/r12",
                        B1="kernel l^2/r^3 (scale selector, not depth)", B2="brane bending: fractional boost ~ (r^3/(r_c^2 r_g))^(1/2) inside r_V, larger for lighter objects")
RES["J1_commit"] = "3d75573e2c"

# ---------------------------------------------------------------- verdict (frozen rule)
say("\n=== VERDICT (frozen rule) ===")
VER = {}
for cl in ("C0", "C1", "C2"):
    for f in FEET:
        cal = all(O1[(cl, hk, f)]["cal"] for hk in HS)
        o1 = cal and all(O1[(cl, hk, f)]["passes"] for hk in HS)
        r1 = cal and all(R1[(cl, hk, f)]["passes"] for hk in HS)
        r3 = cal and all(R3[(cl, hk, f)]["passes"] for hk in HS)
        r5 = cal and all(R5[(cl, hk, f)]["passes"] for hk in HS)
        r4 = (cal and all(R4[(hk, f)]["passes"] for hk in HS)) if cl == "C0" else None
        others = [r1, r3, r5] + ([r4] if r4 is not None else [])
        st = "WORKS" if (cal and o1 and all(others)) else ("PARTIAL" if (cal and o1 and sum(bool(x) for x in others) >= 2) else "FAILS")
        VER[f"{cl}|{f}"] = dict(CAL=cal, O1=o1, R1=r1, R3=r3, R5=r5, R4=r4, status=st)
        say(f"  {cl} {f:9s}: CAL {cal}  O1 {o1}  R1 {r1}  R3 {r3}  R5 {r5}  R4 {r4 if r4 is not None else 'NOT LINKED'}  -> {st}")
anyW = any(v["status"] == "WORKS" for v in VER.values()); anyP = any(v["status"] == "PARTIAL" for v in VER.values())
bulk_fail = (not B1["passes"]) and all(not v["passes"] for v in B2.values())
OVER = "WORKS" if anyW else ("PARTIAL" if anyP else ("FAILS" if bulk_fail else "UNDECIDED"))
say(f"  bulk-supplied: B1 RS2 {'FAIL' if not B1['passes'] else 'PASS'}, B2 DGP {'FAIL' if all(not v['passes'] for v in B2.values()) else 'PASS'}")
say(f"OVERALL VERDICT: {OVER}")
# ---------------------------------------------------------------- output
def key(k): return "|".join(k) if isinstance(k, tuple) else k
RES.update(cache_sha256=SHA, N=N, CAL={key(k): v for k, v in CAL.items()}, O1={key(k): v for k, v in O1.items()}, R1={key(k): v for k, v in R1.items()},
           R3={key(k): v for k, v in R3.items()}, R5={key(k): v for k, v in R5.items()}, R4={key(k): v for k, v in R4.items()},
           compactness={key(k): v for k, v in COMPACT.items()}, B1=B1, B2=B2, needed_MID_excess=needA, verdict_per_closure=VER, verdict=OVER,
           K8_50b=d50, K9_baseline=k9, unit_plummer_FX=FX)
npass = sum(ok for _, ok in CHECKS); mem("end")
say(f"K1_BRANEWORLD_WEYL COMPLETE: {npass}/{len(CHECKS)} checks PASS.")
json.dump(RES, open(os.path.join(HERE, f"k1_braneworld_weyl_results{TAG}.json"), "w"), indent=1,
          default=lambda o: o.tolist() if hasattr(o, "tolist") else (float(o) if isinstance(o, (np.floating, np.integer)) else str(o)))
sys.exit(0 if npass == len(CHECKS) else 1)
