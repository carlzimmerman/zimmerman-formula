#!/usr/bin/env python3
"""CFG191_s5b_pipeline_tier2 -- item (e), tier 2: the P2 merge value in the DR4 Arm A geometry, with my own code.
PRE-DECLARED (before the first run of this script):
  * WHAT IS MINE: the boost-table solvers (one-field AQUAL by Picard, and the QUMOND fork) for a point mass in a uniform external field,
    for a chosen kernel nu and Newtonian external field y_ext; the exact isolated QUMOND two-body benchmark f_tm(y); the population generator
    with 3-D geometry; the composition grades (total-mass 'floor', benchmark-corrected 'top'); the debias control.
  * WHAT IS THE PREREGISTRATION'S (imported read-only from prep_2026/gaia_dr4_prep/wide_binary_pipeline.py, sys.dont_write_bytecode): the frozen
    estimator (bin_medians, model_medians, fit_gamma, GRID), the error model (sigma_pm, sigma_plx), the master population (make_population)
    and constants.  The estimator's transition shape uses the pipeline's own y_extN(a0) (P2 inversion at g_ext = 1.778e-10) in ALL cases: the
    pipeline is frozen; only the INJECTED physics changes.
  * CONTROL (load-bearing): my nu_RAR runs (Route A kernel, y_extN from x = y nu(y), g_ext 1.778e-10) reproduce the registered Arm A anchors
    1.1614 / 1.1814 (canonical) and 1.1917 / 1.2267 (alt) as the mean of the seed battery within 0.020 (registered rms 0.0083-0.0148).
    If it fails the P2 numbers are UNVERIFIED and stay in the file as such.
  * The P2 numbers are then reported beside the nu_RAR numbers, kernel x footing x g_ext (1.778e-10 primary; 2.146e-10 labelled variant).
  * Not done: the pipeline MC at the frozen N with the real DR4 catalogue; AQUAL for the isolated two-body (QUMOND used for the benchmark, as in the preregistration's own benchmark).
MUTATE=1: the control is run with P2 in place of nu_RAR (Arm A's kernel swapped): the control must FAIL -> exit 1.
Time: ~10-14 min."""
import warnings; warnings.filterwarnings("ignore")
import sys, os, math, time
import numpy as np
from scipy.optimize import brentq
from CFG191_common import Run, REPO, rel, HERE
np.seterr(all="ignore")
sys.dont_write_bytecode = True
R = Run("CFG191_s5b_pipeline_tier2", "item (e) tier 2: P2 merge value through the frozen wide-binary estimator")
MUT = R.mutate
sys.path.insert(0, str(REPO/"prep_2026/gaia_dr4_prep"))
import wide_binary_pipeline as wbp          # read-only import of the frozen pipeline
R.p(f"frozen pipeline imported read-only from {rel(REPO/'prep_2026/gaia_dr4_prep/wide_binary_pipeline.py')}")
A0 = {"canonical": wbp.A0_CAN, "alt": wbp.A0_ALT}
FULL = os.environ.get("CFG191_QUICK", "") == ""
NSEED = 6 if FULL else 2

# ---------------------------------------------------------------- kernels
def nu_p2(y): return np.sqrt(1.0 + 1.0/np.asarray(y, float))
def nu_rar(y): return 1.0/(1.0 - np.exp(-np.sqrt(np.asarray(y, float))))
_YT = np.logspace(-12, 12, 60001)
class Kernel:
    def __init__(self, name, nu):
        self.name, self.nu = name, nu
        xt = _YT*nu(_YT); assert np.all(np.diff(xt) > 0)
        self._lx, self._ly = np.log(xt), np.log(_YT)
    def y_of_x(self, x): return np.exp(np.interp(np.log(x), self._lx, self._ly))
    def mu_of_x(self, x): x = np.asarray(x, float); return self.y_of_x(x)/x
    def dnu(self, y):
        h = 1e-5*np.asarray(y, float); return (self.nu(y+h) - self.nu(y-h))/(2*h)
KP2, KRAR = Kernel("P2", nu_p2), Kernel("nu_RAR", nu_rar)

# ---------------------------------------------------------------- solver
NR, NTH, LMAX = 1000, 128, 40
RMIN, RMAX = 1e-3, 3e4
r = np.logspace(np.log10(RMIN), np.log10(RMAX), NR); lnr = np.log(r)
u, wu = np.polynomial.legendre.leggauss(NTH); sinth = np.sqrt(1 - u*u)
P = np.zeros((LMAX+1, NTH)); P[0] = 1; P[1] = u
for l in range(1, LMAX): P[l+1] = ((2*l+1)*u*P[l] - l*P[l-1])/(l+1)
dPdu = np.zeros_like(P)
for l in range(1, LMAX+1): dPdu[l] = l*(u*P[l] - P[l-1])/(u*u - 1)
D = -sinth[None, :]*dPdu                    # dP_l/dtheta
lidx = np.arange(LMAX+1)
R2 = r[:, None]**2
def proj_scalar(S): return np.einsum("lt,t,rt->lr", P, wu, S)*(lidx + 0.5)[:, None]
def proj_theta(Wt):
    out = np.einsum("lt,t,rt->lr", D, wu, Wt)
    fac = np.zeros(LMAX+1); fac[1:] = (2*lidx[1:]+1)/(2*lidx[1:]*(lidx[1:]+1))
    return out*fac[:, None]
def divergence_l(Wr, Wt):
    wl = proj_scalar(Wr); sl = proj_theta(Wt)
    T = np.zeros_like(wl)
    for l in range(LMAX+1):
        T[l] = np.gradient(r**2*wl[l], lnr)/r**3 - l*(l+1)*sl[l]/r
    return T
def poisson_grad(Tl):
    """lap chi' = T  -> (chi_r, chi_theta) fields (chi = grad chi')."""
    chr_l = np.zeros_like(Tl); chp_l = np.zeros_like(Tl)
    for l in range(LMAX+1):
        f_in = Tl[l]*r**(l+3); f_out = Tl[l]*r**(2-l)
        I_in = np.concatenate([[0.0], np.cumsum(0.5*(f_in[1:]+f_in[:-1])*np.diff(lnr))])
        c = np.concatenate([[0.0], np.cumsum(0.5*(f_out[1:]+f_out[:-1])*np.diff(lnr))]); I_out = c[-1] - c
        chp_l[l] = -(I_in/r**(l+1) + I_out*r**l)/(2*l+1)
        chr_l[l] = -(-(l+1)*I_in/r**(l+2) + l*r**(l-1)*I_out)/(2*l+1)
    chi_r = np.einsum("lr,lt->rt", chr_l, P)
    chi_t = np.einsum("lr,lt->rt", chp_l, D)/r[:, None]
    return chi_r, chi_t
def solve_qumond(ker, ye):
    gr = -1/R2 + ye*u[None, :]; gt = -ye*sinth[None, :] + 0*R2
    gm = np.hypot(gr, gt); w = ker.nu(gm) - 1
    nu0 = float(ker.nu(ye)); wb = (nu0 - 1)*ye
    Wr = w*gr - wb*u[None, :]; Wt = w*gt + wb*sinth[None, :]
    return poisson_grad(divergence_l(Wr, Wt))
def solve_aqual(ker, ye, n_iter=140, relax=0.55, tol=2e-4):
    xe = ye*float(ker.nu(ye)); w0 = 1 - float(ker.mu_of_x(xe))
    chi_r, chi_t = solve_qumond(ker, ye)
    conv = np.inf
    for it in range(n_iter):
        Gr = xe*u[None, :] - 1/R2 + chi_r; Gt = -xe*sinth[None, :] + chi_t
        gm = np.maximum(np.hypot(Gr, Gt), 1e-14); w = 1 - ker.mu_of_x(gm)
        Wr = w*Gr - w0*xe*u[None, :]; Wt = w*Gt + w0*xe*sinth[None, :]
        nr, nt = poisson_grad(divergence_l(Wr, Wt))
        msk = (r > 1e-2) & (r < 1e2)
        conv = float(np.max(np.abs((nr-chi_r)*R2)[msk]))     # max change of the radial boost (dimensionless), 1e-2 < r < 1e2 r_M
        chi_r = (1-relax)*chi_r + relax*nr; chi_t = (1-relax)*chi_t + relax*nt
        if conv < tol: break
    return chi_r, chi_t, conv, it+1
def boost_r(chi_r): return 1.0 - chi_r*R2        # radial force boost toward the star

# ---------------------------------------------------------------- exact isolated QUMOND two-body benchmark (own)
def exact_two_body(ker, y_tot, q, nR=700, nu_=300):
    """Isolated QUMOND two-body relative force, own implementation.  Phantom density 4 pi rho_ph = S = -(grad nu).g_N (off the stars).
    The phantom field at each star is integrated in spherical coordinates CENTRED ON THAT STAR (Newton's shell theorem then makes the
    slowly-decaying P2 a0/2 tail cancel exactly instead of by luck): g_z(x*) = +(1/2) int dR int du S(x*+R n) u."""
    Mt = 1.0; M1, M2 = Mt/(1+q), q*Mt/(1+q); r0 = math.sqrt(Mt/y_tot); zs = (-r0/2, r0/2); Ms = (M1, M2)
    def S_at(rho, z):
        gr = gz = 0.0; H = [0.0, 0.0, 0.0]
        for zi, Mi in zip(zs, Ms):
            dz = z - zi; sq = np.sqrt(rho**2 + dz**2)
            gr = gr - Mi*rho/sq**3; gz = gz - Mi*dz/sq**3
            H[0] = H[0] + Mi*(1/sq**3 - 3*rho**2/sq**5); H[1] = H[1] + Mi*(1/sq**3 - 3*dz**2/sq**5); H[2] = H[2] + Mi*(-3*rho*dz/sq**5)
        gm = np.hypot(gr, gz)
        dgm_r = -(H[0]*gr + H[2]*gz)/np.maximum(gm, 1e-300); dgm_z = -(H[2]*gr + H[1]*gz)/np.maximum(gm, 1e-300)
        return -ker.dnu(gm)*(dgm_r*gr + dgm_z*gz)
    xg, xw = np.polynomial.legendre.leggauss(nu_)
    lR = np.linspace(np.log(1e-4*r0), np.log(1e3*max(r0, 1.0)), nR); Rr = np.exp(lR); wR = np.gradient(lR)*Rr
    def gph(zstar):
        RR, UU = np.meshgrid(Rr, xg, indexing="ij")
        val = S_at(RR*np.sqrt(1 - UU**2), zstar + RR*UU)*UU
        return 0.5*np.sum(wR[:, None]*xw[None, :]*val)
    a_rel = Mt/r0**2 + (gph(zs[0]) - gph(zs[1]))
    return a_rel/(Mt/r0**2) - 1.0, float(ker.nu(y_tot)) - 1.0

# ---------------------------------------------------------------- population with 3-D geometry (own, mirroring the frozen generator)
def make_pop_3d(N, rng):
    M1 = rng.uniform(0.45, 1.25, N); q = rng.uniform(0.30, 1.00, N); M2 = np.clip(q*M1, 0.15, None); Mt = M1 + M2
    d = (rng.uniform(25.**3, 250.**3, N))**(1/3.)
    p = -0.6; lo, hi = (2*0.5)**p, (30*2.0)**p
    a_sma = (rng.uniform(hi, lo, N))**(1/p)*wbp.KAU
    e = np.sqrt(rng.uniform(0, 1, N)); Ma = rng.uniform(0, 2*np.pi, N); E = Ma.copy()
    for _ in range(60): E -= (E - e*np.sin(E) - Ma)/(1 - e*np.cos(E))
    n_ = np.sqrt(wbp.G*Mt*wbp.MSUN/a_sma**3); b_ = a_sma*np.sqrt(1-e**2)
    xo, yo = a_sma*(np.cos(E)-e), b_*np.sin(E); Ed = n_/(1-e*np.cos(E))
    vxo, vyo = -a_sma*np.sin(E)*Ed, b_*np.cos(E)*Ed
    Om, w = rng.uniform(0, 2*np.pi, N), rng.uniform(0, 2*np.pi, N); ci = rng.uniform(-1, 1, N); si = np.sqrt(1-ci**2)
    cO, sO, cw, sw = np.cos(Om), np.sin(Om), np.cos(w), np.sin(w)
    Pv = np.stack([cO*cw - ci*sO*sw, sO*cw + ci*cO*sw, si*sw]); Qv = np.stack([-cO*sw - ci*sO*cw, -sO*sw + ci*cO*cw, si*cw])
    r3 = xo*Pv + yo*Qv; v3 = vxo*Pv + vyo*Qv; r3d = np.linalg.norm(r3, axis=0); s_proj = np.hypot(r3[0], r3[1])
    g_true = wbp.G*Mt*wbp.MSUN/r3d**2
    eh = rng.standard_normal((3, N)); eh /= np.linalg.norm(eh, axis=0)
    psi = np.arccos(np.clip(np.sum(r3*eh, axis=0)/r3d, -1, 1))
    G1 = wbp.MG_of_mass(M1) + 5*np.log10(d/10.); G2 = wbp.MG_of_mass(M2) + 5*np.log10(d/10.)
    spm = np.sqrt(wbp.sigma_pm(G1, True)**2 + wbp.sigma_pm(G2, True)**2)
    splx = 1/np.sqrt(wbp.sigma_plx(G1, True)**-2 + wbp.sigma_plx(G2, True)**-2)
    plx = 1000./d; d_obs = 1000./(plx + splx*rng.standard_normal(N)); dkpc = d/1000.
    pmx, pmy = v3[0]/(4.74e3*dkpc), v3[1]/(4.74e3*dkpc)
    npmx, npmy = spm*rng.standard_normal(N), spm*rng.standard_normal(N)
    s_obs = s_proj*(d_obs/d); M_obs = Mt*(1 + 0.05*rng.standard_normal(N))
    sel = ((s_obs > 2*wbp.KAU) & (s_obs < 30*wbp.KAU) & (d < 250.) & (np.maximum(G1, G2) < 17.) & (d_obs > 0) & (M_obs > 0.2))
    out = dict(pmx=pmx, pmy=pmy, npmx=npmx, npmy=npmy, d_obs=d_obs, s_obs=s_obs, M_obs=M_obs, g_true=g_true, psi=psi, M1=M1, M2=M2, Mt=Mt, r3d=r3d)
    out = {k: v[sel] for k, v in out.items()}
    out["g_proj"] = wbp.G*out["M_obs"]*wbp.MSUN/out["s_obs"]**2
    out["vc_obs"] = np.sqrt(wbp.G*out["M_obs"]*wbp.MSUN/out["s_obs"])
    return out
def vt_injected(pop, gam):
    vX = (gam*pop["pmx"] + pop["npmx"])*4.74e3*(pop["d_obs"]/1000.); vY = (gam*pop["pmy"] + pop["npmy"])*4.74e3*(pop["d_obs"]/1000.)
    return np.hypot(vX, vY)/pop["vc_obs"]

# ---------------------------------------------------------------- boost interpolation and grades
TH = np.arccos(u)[::-1]
def make_itp(Br):
    Bt = Br[:, ::-1]; ly = np.log10(1.0/r**2)[::-1]; Bq = Bt[::-1]
    def f(lyq, thq):
        lyq = np.clip(lyq, ly[0], ly[-1]); thq = np.clip(thq, TH[0], TH[-1])
        i = np.clip(np.searchsorted(ly, lyq)-1, 0, len(ly)-2); j = np.clip(np.searchsorted(TH, thq)-1, 0, len(TH)-2)
        fy = (lyq-ly[i])/(ly[i+1]-ly[i]); ft = (thq-TH[j])/(TH[j+1]-TH[j])
        return (1-fy)*(1-ft)*Bq[i, j] + fy*(1-ft)*Bq[i+1, j] + (1-fy)*ft*Bq[i, j+1] + fy*ft*Bq[i+1, j+1]
    return f
def gamma_grade(pop, itp, a0, grade, FTM):
    y1 = wbp.G*pop["M1"]*wbp.MSUN/pop["r3d"]**2/a0; y2 = wbp.G*pop["M2"]*wbp.MSUN/pop["r3d"]**2/a0
    yt = np.maximum(y1+y2, 1e-12); B = itp(np.log10(yt), pop["psi"])
    if grade == "top":
        f = np.where(yt >= FTM[0][0], np.interp(np.log10(yt), np.log10(FTM[0]), FTM[1]), 1.0); B = 1.0 + (B-1.0)/f
    return np.sqrt(np.maximum(B, 0.0))
def fit_case(pop, gam, mod, a0, rng):
    vt = vt_injected(pop, gam); logy = np.log10(pop["g_proj"]/a0)
    med, sig, _ = wbp.bin_medians(logy, vt, boot=200, rng=rng)
    g, sg, chi2, nb, kap = wbp.fit_gamma(med, sig, mod, wbp.GRID)
    return g, sg, kap

# ---------------------------------------------------------------- run
t0 = time.time()
KERNS = [("nu_RAR", KRAR), ("P2", KP2)]
if MUT:
    R.p("MUTATE: the CONTROL (Arm A reproduction) is run with P2 in place of nu_RAR")
R.sec("solver controls (own code)")
# V1 Newtonian: trivial; V2 isolated limit
for kn, ker in KERNS:
    Bq = boost_r(solve_qumond(ker, 1e-6)[0]); mask = (r > 5e-3) & (r < 50)
    e_q = np.max(np.abs(Bq[mask]/ker.nu(1/R2)[mask] - 1))
    ch, ct, cv, it = solve_aqual(ker, 1e-6, n_iter=100); Ba = boost_r(ch); e_a = np.max(np.abs(Ba[mask]/ker.nu(1/R2)[mask] - 1))
    R.p(f"  {kn:7s} isolated limit (y_ext=1e-6): QUMOND max|B/nu-1| = {e_q:.2e}, AQUAL {e_a:.2e} (Picard {it} its, max dB {cv:.1e})")
    R.check(f"S1 {kn}: isolated-limit reproduction of B(y) = nu(y): QUMOND < 3e-3, AQUAL < 6e-3 over 5e-3 < r < 50 r_M", e_q < 3e-3 and e_a < 6e-3)
def tens(ker, ye):
    n0 = float(ker.nu(ye)); L = float((np.log(ker.nu(ye*1.0001)) - np.log(ker.nu(ye*0.9999)))/(np.log(1.0001) - np.log(0.9999)))
    dxdy = n0*(1+L); L0 = n0/dxdy - 1; return n0, L0
TAB = {}
def get_table(kn, ker, foot, gext):
    key = (kn, foot, gext)
    if key in TAB: return TAB[key]
    a0 = A0[foot]; xe = gext/a0; ye = float(ker.y_of_x(xe))
    ch, ct, cv, it = solve_aqual(ker, ye); Br = boost_r(ch)
    n0, L0 = tens(ker, ye); i_sat = np.argmin(np.abs(r-300.0))
    Bpar = Br[i_sat, np.argmax(u)]; Bperp = Br[i_sat, np.argmin(np.abs(u))]
    ok = abs(Bpar/n0-1) < 0.02 and abs(Bperp/(n0/np.sqrt(1+L0))-1) < 0.02
    R.p(f"  table {kn:7s} {foot:9s} g_ext={gext:.3e}: y_extN={ye:.4f} nu0={n0:.4f} L0={L0:.4f}; Picard {it} its max dB {cv:.1e}; saturated B_par {Bpar:.4f} (analytic {n0:.4f}), B_perp {Bperp:.4f} (analytic {n0/np.sqrt(1+L0):.4f})")
    TAB[key] = (Br, ye, n0, L0, ok, cv)
    return TAB[key]
R.sec("exact isolated QUMOND two-body benchmark f_tm(y) (own)")
YB = np.array([3.162, 5.62, 10.0, 17.8, 31.6]); FTM = {}
for kn, ker in KERNS:
    val = []
    for yv in (1.0, 10.0):
        e_ex, e_tm = exact_two_body(ker, yv, 1e-6); val.append(abs((1+e_ex)/float(ker.nu(yv)) - 1))
    rows = []
    for yv in YB:
        rr = []
        for q in (0.3, 0.5, 0.7, 1.0):
            e_ex, e_tm = exact_two_body(ker, yv, q); rr.append(e_tm/e_ex)
        rows.append(np.median(rr))
    FTM[kn] = (YB, np.maximum(np.array(rows), 1.0))
    R.p(f"  {kn:7s}: quadrature control (q->0): |exact/nu-1| = {val[0]:.4f} (y=1), {val[1]:.4f} (y=10); f_tm(y) = " + ", ".join(f"{v:.2f}" for v in FTM[kn][1]) + f" at y = {', '.join(f'{v:g}' for v in YB)}")
    R.check(f"S2 {kn}: two-body quadrature control within 1% (y=1) and 5% (y=10), f_tm > 1 at the anchor", val[0] < 0.01 and val[1] < 0.05 and FTM[kn][1][0] > 1.0)
R.p("  the registered (Route A) benchmark, for comparison, is f_tm ~ 1.4-1.8 (Amendment 10); mine is the nu_RAR row above.")

results = {}
cases = [("nu_RAR", KRAR, 1.778e-10), ("P2", KP2, 1.778e-10)] if FULL and not MUT else [("nu_RAR", KRAR, 1.778e-10), ("P2", KP2, 1.778e-10)]
if FULL and not MUT: cases += [("nu_RAR", KRAR, 2.146e-10), ("P2", KP2, 2.146e-10)]
if MUT: cases = [("P2", KP2, 1.778e-10)]     # control kernel swapped: Arm A 'reproduced' with P2
feet = ["canonical", "alt"]
SEEDS = [4242, 1111, 2222, 3333, 5555, 7777][:NSEED]
R.sec(f"solver tables for {len(cases)} cases x 2 footings")
for kn, ker, gx in cases:
    for foot in feet:
        get_table(kn, ker, foot, gx)
R.check("S3 saturated solver tensors match the linear-response analytic tensors (par to 2%, perp to 2%) in every table", all(v[4] for v in TAB.values()))
R.p(f"  elapsed {time.time()-t0:.0f} s")

R.sec("pipeline runs (frozen estimator, my injection); one master + model per footing per seed")
raw = {}
for foot in feet:
    a0 = A0[foot]
    for si, s in enumerate(SEEDS):
        rng = np.random.default_rng(s + (0 if foot == "canonical" else 1))
        pop_d = make_pop_3d(140000, rng); keep = rng.permutation(len(pop_d["pmx"]))[:30000]; pop_d = {k: v[keep] for k, v in pop_d.items()}
        pop_m = wbp.make_population(400000, rng, dr4=True)
        mod = wbp.model_medians(pop_m, a0, wbp.GRID, rng)
        for kn, ker, gx in cases:
            Br, ye, n0, L0, ok, cv = TAB[(kn, foot, gx)]; itp = make_itp(Br)
            # debias control: isotropic registered-shape injection at the kernel's own point-field target
            tgt = float(np.sqrt(n0))
            gC = wbp.gamma_of_y(pop_d["g_true"]/a0, tgt, wbp.y_extN(a0))
            gC1, sC1, kC1 = fit_case(pop_d, gC, mod, a0, rng); bias = gC1 - tgt
            out = dict(bias=bias, target=tgt)
            for grade in ("floor", "top"):
                gam = gamma_grade(pop_d, itp, a0, "top" if grade == "top" else "floor", FTM[kn])
                g_, s_, k_ = fit_case(pop_d, gam, mod, a0, rng)
                out[grade] = (g_ - bias, s_, k_)
            raw[(kn, foot, gx, s)] = out
        R.p(f"  {foot:9s} seed {s}: done ({time.time()-t0:.0f} s elapsed)")
summ = {}
R.sec("RESULTS: debiased gamma-hat (mean over seeds; rms), floor = total-mass grade, top = benchmark-corrected grade")
R.p(f"  {'kernel':7s} {'footing':9s} {'g_ext':>9s} | {'floor':>7s} {'rms':>6s} | {'top':>7s} {'rms':>6s} | point sqrt(nu0) | kappa range")
for kn, ker, gx in cases:
    for foot in feet:
        rows = [raw[(kn, foot, gx, s)] for s in SEEDS]
        fl = np.array([x["floor"][0] for x in rows]); tp = np.array([x["top"][0] for x in rows])
        kp = [x[g][2] for x in rows for g in ("floor", "top")]
        n0 = TAB[(kn, foot, gx)][2]
        summ[(kn, foot, gx)] = dict(floor=float(fl.mean()), floor_rms=float(fl.std(ddof=1) if len(fl) > 1 else 0), top=float(tp.mean()), top_rms=float(tp.std(ddof=1) if len(tp) > 1 else 0), point=float(np.sqrt(n0)), bias=float(np.mean([x["bias"] for x in rows])))
        R.p(f"  {kn:7s} {foot:9s} {gx:9.3e} | {fl.mean():7.4f} {summ[(kn,foot,gx)]['floor_rms']:6.4f} | {tp.mean():7.4f} {summ[(kn,foot,gx)]['top_rms']:6.4f} | {np.sqrt(n0):.4f} | {min(kp):.3f}-{max(kp):.3f}")
R.data["summary"] = {f"{k[0]}|{k[1]}|{k[2]}": v for k, v in summ.items()}
R.data["seeds"] = SEEDS

R.sec("CONTROL: reproduction of the registered Arm A anchors (nu_RAR, g_ext 1.778e-10)" + (" -- MUTATE: with P2 in place of nu_RAR" if MUT else ""))
reg = {"canonical": (1.1614, 1.1814), "alt": (1.1917, 1.2267)}
ckey = "P2" if MUT else "nu_RAR"
dev = []
for foot in feet:
    s_ = summ[(ckey, foot, 1.778e-10)]
    dev += [s_["floor"] - reg[foot][0], s_["top"] - reg[foot][1]]
    R.p(f"  {foot:9s}: mine floor {s_['floor']:.4f} / top {s_['top']:.4f}  vs registered {reg[foot][0]} / {reg[foot][1]}   (deviations {s_['floor']-reg[foot][0]:+.4f} / {s_['top']-reg[foot][1]:+.4f})")
R.check("C-ARM-A my nu_RAR runs reproduce the four registered Arm A anchors within 0.020 (mean of the battery)" + (" [MUTATE: with the P2 kernel this must FAIL]" if MUT else ""), max(abs(d) for d in dev) <= 0.020)
R.data["control_dev"] = dev
if not MUT:
    R.sec("THE P2 MERGE VALUE (small table)")
    R.p("  kernel = P2 = sqrt(1 + a0/g_N); nu_RAR beside it for the kernel dependence; Arm A registered band: canonical 1.1614-1.1814, alt 1.1917-1.2267")
    R.p(f"  {'kernel':7s} {'a0 footing':10s} {'g_ext [m/s2]':>13s} {'floor':>7s} {'top':>7s} {'sqrt(nu0) point':>16s}   distance of floor/top below Arm A floor (sigma_fit 0.019)")
    for gx in (1.778e-10, 2.146e-10):
        for foot in feet:
            for kn in ("P2", "nu_RAR"):
                if (kn, foot, gx) not in summ: continue
                s_ = summ[(kn, foot, gx)]
                R.p(f"  {kn:7s} {foot:10s} {gx:13.3e} {s_['floor']:7.4f} {s_['top']:7.4f} {s_['point']:16.4f}   {(reg[foot][0]-s_['floor'])/0.019:+.1f} / {(reg[foot][0]-s_['top'])/0.019:+.1f}")
    p2c = summ[("P2", "canonical", 1.778e-10)]; p2a = summ[("P2", "alt", 1.778e-10)]
    R.check("T2-a P2 merge (canonical, primary g_ext) sits below Arm A's floor 1.1614 by more than 1 sigma_fit (0.019)", reg["canonical"][0] - p2c["top"] > 0.019, "if this fails the crude-transfer flag of s5 is not supported", lb=True)
    R.check("T2-b P2 merge (alt, primary g_ext) sits below Arm A's alt floor 1.1917 by more than 1 sigma_fit", reg["alt"][0] - p2a["top"] > 0.019, lb=True)
    R.finding("(e) tier 2 P2 merge value", "COMPUTED" if all(c["ok"] for c in R.checks if c["label"].startswith("C-ARM-A")) else "UNVERIFIED (control failed)",
              f"P2 at g_ext 1.778e-10: canonical {p2c['floor']:.4f}-{p2c['top']:.4f}, alt {p2a['floor']:.4f}-{p2a['top']:.4f}; nu_RAR (control kernel) canonical {summ[('nu_RAR','canonical',1.778e-10)]['floor']:.4f}-{summ[('nu_RAR','canonical',1.778e-10)]['top']:.4f}, alt {summ[('nu_RAR','alt',1.778e-10)]['floor']:.4f}-{summ[('nu_RAR','alt',1.778e-10)]['top']:.4f}.")
R.p(f"  total elapsed {time.time()-t0:.0f} s")
R.finish()
