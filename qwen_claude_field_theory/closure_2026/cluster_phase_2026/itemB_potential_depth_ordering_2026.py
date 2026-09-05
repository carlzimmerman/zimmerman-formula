#!/usr/bin/env python3
"""
ITEM B -- THE ORDERING BY POTENTIAL DEPTH |Phi|/c^2 (cluster-phase workflow, 2026-09-01)
=======================================================================================
QUESTION. The density no-go (CLUSTER_RESIDUAL_DENSITY_NOGO.md Sec.3) shows galaxy disks are DENSER
than cluster cores, so density-keyed clumping lands in galaxies first.  Here we compute the POTENTIAL
DEPTH |Phi|/c^2 instead, self-consistently with the framework kernel g_obs = sqrt(g_bar^2 + g_bar a0)
(the potential felt is the MOND one, phantom included), for
   (i)   real SPARC disks (175 galaxies, Ups_disk = 0.70, the repo's RAR footing),
   (ii)  a Milky-Way-like galaxy,
   (iii) a rich cluster core (eROSITA/Bulbul-type beta-model + BCG, M500 = 1e15, R500 = 1.56 Mpc --
         the SAME profile the no-go paper's Helmholtz solve used),
   (iv)  a group (M500 = 1e14),
and ask: does |Phi| put clusters ABOVE galaxies, by what factor?  Then, for the SPECIFIC Helmholtz
response of the AeST +mu^2 Phi mass term, rho_resp = -A Phi/(4 pi G), A = mu^2 (linear in the depth):
does a galaxy-safe amplitude (SPARC RAR shift < 0.1 dex) deliver >= 50% of the cluster-core residual?
Both footings (a0 = 9.36e-11 canonical / 1.128e-10 alt).

DEPTH / BOUNDARY CONVENTION (stated; sensitivity scanned).  With the kernel the potential has a
logarithmic tail (g -> sqrt(G M a0)/r) so "Phi -> 0 at infinity" does not exist; and the +A Phi
operator is oscillatory (wavelength 2 pi/sqrt(A)) so the outer boundary carries a PHASE.  Inside
sqrt(A) R_cut < pi the Dirichlet problem Phi(R_cut) = 0 has a UNIQUE solution (the map
Phi(0) -> Phi(R_cut) is monotone; checked), so we fix the depth by  Phi(R_cut) = 0  with
R_cut = kR / sqrt(A), kR in {1, pi/2} (both inside the unique branch).  At A = mu^2, kR = 1 this is
R_cut = 1/mu = 1 Mpc.  This is ONE FIXED PHASE (the sign that boosts).  Whether the time-dependent
evolution PINS it is Item A's question; this item settles the ORDERING and the galaxy-safe cluster
yield AT FIXED PHASE.

SELF-CONSISTENCY.  rho_resp is a SOURCE of the MOND operator, div[mu grad Phi] = 4 pi G (rho_b +
rho_resp), and it deepens Phi which raises rho_resp: we solve the fixed point (integral form, iterated
to convergence) on every system, and cross-check the cluster against the repo's exact canonical-
momentum ODE solver (aest_phi_cluster_solve.py) with the kernel made switchable (framework kernel
primary; the DS24 'simple' M(x) the repo solver used is reported as a kernel-sensitivity row).
Yield = Delta M_dyn(<420 kpc) = (g_obs' - g_obs) r^2 / G against the banked core residual (1.0e14 Msun
paper value; 1.5e14 harsher); galaxy cost = SPARC per-point shift log10(g_obs'/g_obs) and the change
in RAR scatter.

CHECKS THAT CAN FAIL (exit 1): analytic point-mass depth and the deep-MOND log tail; A -> 0 gives
zero; linearity of the source; fixed-point convergence; fixed-point == ODE solve (two methods) on the
cluster AND on the MW galaxy; Phi(R_cut)=0 satisfied by the shot; A=0 ODE reproduces analytic MOND;
uniqueness (monotone map) on the branch used; depth ordering cluster > group > EVERY galaxy at every
kR (both footings); density ordering the REVERSE (mutation control on the key); the density-keyed
response (mutation control on the response) reported against the same 50% bar.  The depth-keyed
50%/galaxy-safe verdict is PRINTED from the numbers, not asserted.
"""
import os, sys, glob, json
import numpy as np
from scipy.integrate import cumulative_trapezoid, solve_ivp
from scipy.optimize import brentq

c = 2.99792458e8; G = 6.674e-11; Msun = 1.989e30; kpc = 3.0857e19; Mpc = 3.0857e22
H0 = 67.4e3/Mpc; Om, OL, Ob = 0.315, 0.685, 0.0493
rho_crit0 = 3*H0**2/(8*np.pi*G)
FOOTINGS = {"canon": 9.36e-11, "alt": 1.128e-10}
INV_MU = 1.0*Mpc; MU2 = 1.0/INV_MU**2            # CMB-pinned 1/mu = 1 Mpc; natural A = mu^2
R_CORE = 420*kpc
M_TARGET = {"paper_1e14": 1.0e14, "harsh_1.5e14": 1.5e14}
HERE = os.path.dirname(os.path.abspath(__file__))
SPARC = os.path.join(HERE, "..", "..", "..", "real_research", "data", "sparc_data")
KR_LIST = [1.0, np.pi/2]

FAIL = []; NCHK = [0]
def check(cond, label, detail=""):
    NCHK[0] += 1; ok = bool(cond)
    print(f"  [{'ok' if ok else 'FAIL'}] {label}" + (f"   {detail}" if detail else ""))
    if not ok: FAIL.append(label)
    return ok

KERNEL = {"framework": lambda gs, a0: np.sqrt(gs**2 + gs*a0),          # g_obs = sqrt(g^2 + g a0)
          "DS24_simple": lambda gs, a0: gs + np.sqrt(np.abs(gs)*a0)}    # x = q + sqrt(q): repo solver's M(x)

# ------------------------------------------------------------------ profiles
def cluster_profile(M500, R500, beta=0.67, rc_frac=0.12, fgas=0.13, fstar=0.012, a_bcg_kpc=30.0):
    """IDENTICAL to aest_phi_cluster_solve.make_baryons_A2029 (eROSITA/Bulbul-type)."""
    rc = rc_frac*R500; a_bcg = a_bcg_kpc*kpc
    M_bcg = fstar*M500*Msun; M_gas = fgas*M500*Msun
    rho_un = lambda r: (1.0 + (r/rc)**2)**(-1.5*beta)
    rr = np.geomspace(1e-3*rc, R500, 200000)
    rho_g0 = M_gas/np.trapz(4*np.pi*rr**2*rho_un(rr), rr)
    rtab = np.geomspace(1e-4*rc, 80*Mpc, 8000)
    integ = 4*np.pi*rtab**2*rho_g0*rho_un(rtab)
    Mg_tab = np.concatenate([[0.0], np.cumsum(0.5*(integ[1:]+integ[:-1])*np.diff(rtab))])
    Menc = lambda r: np.interp(r, rtab, Mg_tab) + M_bcg*(r**2/(r+a_bcg)**2)
    rho_b = lambda r: rho_g0*rho_un(r) + M_bcg*a_bcg/(2*np.pi)/(r*(r+a_bcg)**3)
    return Menc, rho_b

def R500_of(M500_Msun, z=0.0):
    return (3*M500_Msun*Msun/(4*np.pi*500*rho_crit0*(Om*(1+z)**3+OL)))**(1/3.)

def mw_profile():
    """MW-like: Hernquist bulge 0.9e10 a=0.6 kpc; stellar disk 4.5e10 Rd=2.6; gas 1.2e10 Rd=7 (spherical-
    equivalent enclosed masses)."""
    Mb, ab = 0.9e10*Msun, 0.6*kpc; Md, Rd = 4.5e10*Msun, 2.6*kpc; Mg, Rg = 1.2e10*Msun, 7.0*kpc
    exp_enc = lambda r, M, R: M*(1.0 - (1.0 + r/R)*np.exp(-r/R))
    Menc = lambda r: Mb*(r**2/(r+ab)**2) + exp_enc(r, Md, Rd) + exp_enc(r, Mg, Rg)
    def rho_b(r):
        dM = Mb*2*ab*r/(r+ab)**3 + Md*(r/Rd**2)*np.exp(-r/Rd) + Mg*(r/Rg**2)*np.exp(-r/Rg)
        return dM/(4*np.pi*r**2)
    return Menc, rho_b

def load_sparc(Ups=0.70):
    out = []
    for f in sorted(glob.glob(os.path.join(SPARC, "*_rotmod.dat"))):
        try: dat = np.loadtxt(f, comments="#")
        except Exception: continue
        if dat.ndim != 2 or dat.shape[1] < 6: continue
        R = dat[:,0]*kpc; Vobs = dat[:,1]*1e3; Vgas = dat[:,3]*1e3; Vd = dat[:,4]*1e3; Vb = dat[:,5]*1e3
        Vbar2 = Vgas*np.abs(Vgas) + Ups*Vd*np.abs(Vd) + 1.4*Ups*Vb*np.abs(Vb)
        gbar = np.clip(Vbar2, 0, None)/R; gobs = Vobs**2/R
        m = (R > 0) & (gbar > 0) & (gobs > 0) & np.isfinite(gbar) & np.isfinite(gobs)
        if m.sum() < 3: continue
        o = np.argsort(R[m])
        out.append((os.path.basename(f).replace("_rotmod.dat",""), R[m][o], gbar[m][o], gobs[m][o]))
    return out

def sparc_gbar_on_grid(R, gbar, r):
    """log-log interpolation inside the data; g ~ r inside r_min; Newtonian point-mass tail beyond r_max."""
    g = np.exp(np.interp(np.log(r), np.log(R), np.log(gbar)))
    g = np.where(r < R[0], gbar[0]*r/R[0], g)
    g = np.where(r > R[-1], gbar[-1]*(R[-1]/r)**2, g)
    return g

# ------------------------------------------------------------------ self-consistent fixed point
def depth(r, g):
    """|Phi(r)| = int_r^{R_cut} g dr' on the grid, Phi(R_cut) = 0."""
    I = cumulative_trapezoid(g, r, initial=0.0); return I[-1] - I

def resp_mass(r, absPhi, A):
    """M_resp(<r) = (A/G) int_0^r |Phi| r'^2 dr'   (rho_resp = A|Phi|/(4 pi G), Phi < 0)."""
    return (A/G)*(absPhi[0]*r[0]**3/3.0 + cumulative_trapezoid(absPhi*r**2, r, initial=0.0))

def fixed_point(r, gbar, A, a0, kern, itmax=400, tol=1e-7):
    """Iterate  g_s = g_bar + G M_resp/r^2 ;  g = kern(g_s) ;  |Phi| = depth(g) ;  M_resp = (A/G) int |Phi| r^2
    to convergence.  Returns (|Phi|, g_obs', g_obs0, M_resp, n_iter, last_change)."""
    g0 = kern(gbar, a0); Mr = np.zeros_like(r); g = g0
    for it in range(itmax):
        d = depth(r, g); Mr_new = resp_mass(r, d, A)
        g_new = kern(gbar + G*Mr_new/r**2, a0)
        chg = float(np.max(np.abs(np.log10(g_new/g)))) if it > 0 else 1.0
        g, Mr = g_new, Mr_new
        if chg < tol: break
    return depth(r, g), g, g0, Mr, it+1, chg

# ------------------------------------------------------------------ exact ODE solver (repo form, kernel switchable)
def ode_march(A, rho_b, Menc, a0, kern, r0, r1, Phi0, n=4000):
    """canonical-momentum march: P = r^2 mu(x) Phi' = G M_total(<r);  Phi' = kern(P/r^2);  P' = r^2(4piG rho_b - A Phi)."""
    def f(r, y):
        gs = y[1]/r**2
        return [np.sign(gs)*kern(abs(gs), a0), r**2*(-A*y[0] + 4*np.pi*G*rho_b(r))]
    sol = solve_ivp(f, [r0, r1], [Phi0, G*Menc(r0)], t_eval=np.geomspace(r0, r1, n),
                    rtol=1e-11, atol=1e-16, method="DOP853", max_step=(r1-r0)/4000)
    r = sol.t; P = sol.y[1]; gs = P/r**2
    return r, sol.y[0], np.sign(gs)*kern(np.abs(gs), a0)

def ode_shoot(A, rho_b, Menc, a0, kern, r0, R_cut):
    fn = lambda Phi0: float(np.interp(R_cut, *ode_march(A, rho_b, Menc, a0, kern, r0, R_cut, Phi0, n=1500)[:2]))
    Phi0 = brentq(fn, -1e14, 1e14, xtol=1e5)
    return ode_march(A, rho_b, Menc, a0, kern, r0, R_cut, Phi0, n=6000)

# ==================================================================================================
print("="*100); print("ITEM B -- ORDERING BY POTENTIAL DEPTH |Phi|/c^2, framework kernel, self-consistent, both footings"); print("="*100)
R500_cl = 1.56*Mpc; Menc_cl, rho_cl = cluster_profile(1e15, R500_cl)
R500_gr = R500_of(1e14); Menc_gr, rho_gr = cluster_profile(1e14, R500_gr, fgas=0.11, fstar=0.02)
Menc_mw, rho_mw = mw_profile()
sparc = load_sparc()
print(f"cluster: M500=1e15, R500={R500_cl/Mpc:.2f} Mpc, M_b(<420kpc)={Menc_cl(R_CORE)/Msun:.3e}, M_b(<R500)={Menc_cl(R500_cl)/Msun:.3e} Msun")
print(f"group  : M500=1e14, R500={R500_gr/Mpc:.2f} Mpc, M_b(<R500)={Menc_gr(R500_gr)/Msun:.3e}")
print(f"MW-like: M_b(<30kpc)={Menc_mw(30*kpc)/Msun:.3e} Msun;  SPARC: {len(sparc)} galaxies, {sum(len(s[1]) for s in sparc)} points")

# ---- C0: analytic controls
r_pm = np.geomspace(1*kpc, 1000*kpc, 4000); M_pm = 1e11*Msun; gb_pm = G*M_pm/r_pm**2
dN = depth(r_pm, gb_pm); exact = G*M_pm*(1/r_pm[0] - 1/r_pm[-1])
check(abs(dN[0]/exact - 1) < 2e-3, "C0a point-mass Newtonian depth = GM(1/r - 1/R_cut)", f"num/exact = {dN[0]/exact:.5f}")
dM_ = depth(r_pm, KERNEL['framework'](gb_pm, 9.36e-11)); v2 = np.sqrt(G*M_pm*9.36e-11)
rt = dM_[np.argmin(np.abs(r_pm-100*kpc))]/(v2*np.log(10.0))
check(abs(rt-1) < 0.05, "C0b deep-MOND depth tail = v_flat^2 ln(R_cut/r) (point mass 1e11, 100 kpc -> 1 Mpc)", f"num/analytic = {rt:.4f}")

RESULTS = {}
for foot, a0 in FOOTINGS.items():
    kern = KERNEL['framework']
    print("\n" + "#"*100); print(f"# FOOTING {foot}: a0 = {a0:.3e} m/s^2   (kernel: framework g_obs = sqrt(g^2 + g a0))"); print("#"*100)
    RES = RESULTS[foot] = {}

    # ================================================================ PART 1: depth ordering (A = mu^2)
    print("\nPART 1 -- |Phi|/c^2 at A = mu^2 (self-consistent), R_cut = kR/mu; 'bare' = baryons+kernel only; 'N' = Newtonian control")
    order_ok = True
    for kR in KR_LIST:
        R_cut = kR*INV_MU; rows = {}
        for name, Menc, rin, rchar in [("cluster", Menc_cl, 1*kpc, [50*kpc, 200*kpc, R_CORE]),
                                       ("group", Menc_gr, 1*kpc, [50*kpc, 200*kpc, R500_gr]),
                                       ("MW", Menc_mw, 0.05*kpc, [1*kpc, 8*kpc, 20*kpc])]:
            r = np.geomspace(rin, R_cut, 4000); gb = G*Menc(r)/r**2
            d_sc, g_sc, g0, Mr, nit, chg = fixed_point(r, gb, MU2, a0, kern)
            d_bare = depth(r, g0); d_N = depth(r, gb)
            rows[name] = dict(max=d_sc[0]/c**2, bare=d_bare[0]/c**2, N=d_N[0]/c**2,
                              at=[float(np.interp(x, r, d_sc))/c**2 for x in rchar], rchar=rchar)
        sp_max, sp_bare, sp_N, sp_pts, names = [], [], [], [], []
        for name, R, gbar, gobs in sparc:
            r = np.geomspace(0.1*R[0], R_cut, 2500); gb = sparc_gbar_on_grid(R, gbar, r)
            d_sc, g_sc, g0, Mr, nit, chg = fixed_point(r, gb, MU2, a0, kern)
            sp_max.append(d_sc[0]/c**2); sp_bare.append(depth(r, g0)[0]/c**2); sp_N.append(depth(r, gb)[0]/c**2)
            sp_pts.append(np.interp(R, r, d_sc)/c**2); names.append(name)
        sp_max = np.array(sp_max); sp_all = np.concatenate(sp_pts); i_deep = int(np.argmax(sp_max))
        rows["SPARC"] = dict(max=float(sp_max.max()), bare=float(max(sp_bare)), N=float(max(sp_N)), deepest=names[i_deep],
                             median_max=float(np.median(sp_max)), pts_median=float(np.median(sp_all)), pts_max=float(sp_all.max()))
        print(f"\n  kR = {kR:.3f}  (R_cut = {R_cut/Mpc:.2f} Mpc)      |Phi|/c^2")
        print(f"    {'system':>8} {'max(selfc)':>11} {'max(bare)':>10} {'max(N)':>10}  depth at characteristic radii (self-consistent)")
        for name in ["cluster", "group", "MW"]:
            rr = rows[name]; ats = "  ".join(f"{x:.2e}@{rc/kpc:.0f}kpc" for x, rc in zip(rr['at'], rr['rchar']))
            print(f"    {name:>8} {rr['max']:>11.3e} {rr['bare']:>10.3e} {rr['N']:>10.3e}  {ats}")
        rr = rows["SPARC"]
        print(f"    {'SPARC':>8} {rr['max']:>11.3e} {rr['bare']:>10.3e} {rr['N']:>10.3e}  deepest={rr['deepest']}; median(max)={rr['median_max']:.2e}; "
              f"RAR-point median={rr['pts_median']:.2e}, max={rr['pts_max']:.2e}")
        gal_max = max(rows['SPARC']['max'], rows['MW']['max'])
        f_deep = rows['cluster']['max']/rows['SPARC']['max']; f_med = rows['cluster']['max']/rows['SPARC']['median_max']
        f_mw = rows['cluster']['max']/rows['MW']['max']; f_420 = rows['cluster']['at'][2]/rows['SPARC']['pts_max']
        fN = rows['cluster']['N']/max(rows['SPARC']['N'], rows['MW']['N']); fb = rows['cluster']['bare']/max(rows['SPARC']['bare'], rows['MW']['bare'])
        print(f"    RATIOS (max depth): cluster/deepest-SPARC = {f_deep:.1f}x; cluster/median-SPARC = {f_med:.0f}x; cluster/MW = {f_mw:.1f}x; "
              f"group/deepest-galaxy = {rows['group']['max']/gal_max:.1f}x;  bare-kernel control {fb:.1f}x; Newtonian control {fN:.1f}x")
        print(f"    RATIO where the mass sits: cluster@420kpc / deepest SPARC RAR point = {f_420:.1f}x   (convention-sensitive: 420 kpc is near R_cut)")
        ok = rows['cluster']['max'] > rows['group']['max'] > gal_max
        order_ok &= ok
        RES[f"depth_kR_{kR:.2f}"] = dict(R_cut_Mpc=R_cut/Mpc, cluster_max=rows['cluster']['max'], group_max=rows['group']['max'],
                                        MW_max=rows['MW']['max'], SPARC_max=rows['SPARC']['max'], SPARC_deepest=rows['SPARC']['deepest'],
                                        SPARC_median_max=rows['SPARC']['median_max'], cluster_at_420=rows['cluster']['at'][2],
                                        SPARC_pt_max=rows['SPARC']['pts_max'], ratio_cl_deepest=f_deep, ratio_cl_median=f_med,
                                        ratio_cl_MW=f_mw, ratio_cl420_pt=f_420, ratio_bare=fb, ratio_newton=fN, ordered=bool(ok))
    check(order_ok, "C1 depth ordering cluster > group > EVERY galaxy (deepest SPARC and MW) at every kR (max depth, self-consistent)")
    print(f"    note: the deepest SPARC spiral ({rows['SPARC']['deepest']}) is deeper than the MW-like model -- the MW model is lighter than the most massive SPARC spirals; ordering vs ALL galaxies is what is checked.")

    # density (the no-go's key) -- mutation control on the key
    rho_core_loc = float(np.mean(rho_cl(np.linspace(100*kpc, 300*kpc, 200))))
    rho_core_mean = Menc_cl(R_CORE)/(4*np.pi/3*R_CORE**3)
    rho_mw_disk = Menc_mw(2.2*2.6*kpc)/(4*np.pi/3*(2.2*2.6*kpc)**3)
    sp_rho = np.array([gbar[max(1, len(R)//3)]*R[max(1, len(R)//3)]**2/G/(4*np.pi/3*R[max(1, len(R)//3)]**3) for _, R, gbar, _ in sparc])
    print(f"\n  DENSITY (kg/m^3): cluster core local 100-300 kpc = {rho_core_loc:.2e}, mean(<420 kpc) = {rho_core_mean:.2e};  "
          f"MW mean(<2.2Rd) = {rho_mw_disk:.2e};  SPARC mean(<inner third) median = {np.median(sp_rho):.2e}")
    check(rho_mw_disk > rho_core_loc and np.median(sp_rho) > rho_core_loc,
          "C2 MUTATION CONTROL on the key: density ordering REVERSED (galaxy disk > cluster core)",
          f"MW/cluster-local = {rho_mw_disk/rho_core_loc:.0f}x, SPARC-median/cluster-local = {np.median(sp_rho)/rho_core_loc:.0f}x  [paper: 3.7x with its own conventions]")
    RES["density_ratio_MW_over_cluster_local"] = rho_mw_disk/rho_core_loc
    RES["density_ratio_SPARCmed_over_cluster_local"] = float(np.median(sp_rho)/rho_core_loc)

    # ================================================================ PART 2: Helmholtz response, self-consistent
    print("\nPART 2 -- Helmholtz p=1 response, self-consistent, R_cut = kR/sqrt(A): cluster yield vs galaxy cost")
    def cluster_yield(A, kR):
        R_cut = kR/np.sqrt(A); r = np.geomspace(1*kpc, R_cut, 4000); gb = G*Menc_cl(r)/r**2
        d, g, g0, Mr, nit, chg = fixed_point(r, gb, A, a0, kern)
        dM = float(np.interp(R_CORE, r, (g - g0)*r**2/G))/Msun
        return dM, float(np.interp(R_CORE, r, Mr))/Msun, float(np.interp(R_CORE, r, g/g0)), nit, chg, float(np.interp(R_CORE, r, d))
    def group_eta(A, kR):
        R_cut = kR/np.sqrt(A); r = np.geomspace(1*kpc, R_cut, 4000); gb = G*Menc_gr(r)/r**2
        d, g, g0, Mr, nit, chg = fixed_point(r, gb, A, a0, kern)
        rq = min(R500_gr, 0.999*R_cut); return float(np.interp(rq, r, g/g0)) - 1.0, rq
    def mw_shift(A, kR):
        R_cut = kR/np.sqrt(A); r = np.geomspace(0.05*kpc, R_cut, 4000); gb = G*Menc_mw(r)/r**2
        d, g, g0, Mr, nit, chg = fixed_point(r, gb, A, a0, kern)
        sel = (r >= 5*kpc) & (r <= 30*kpc); return float(np.max(np.log10(g[sel]/g0[sel])))
    def sparc_stats(A, kR):
        R_cut = kR/np.sqrt(A); shifts, res0, resA, worst = [], [], [], 0.0
        for name, R, gbar, gobs in sparc:
            r = np.geomspace(0.1*R[0], R_cut, 2500); gb = sparc_gbar_on_grid(R, gbar, r)
            d, g, g0, Mr, nit, chg = fixed_point(r, gb, A, a0, kern); worst = max(worst, chg)
            gp = np.interp(R, r, g); gz = np.interp(R, r, g0)
            shifts.append(np.log10(gp/gz)); res0.append(np.log10(gobs/gz)); resA.append(np.log10(gobs/gp))
        s = np.concatenate(shifts); r0_ = np.concatenate(res0); rA = np.concatenate(resA)
        mad = lambda x: 1.4826*np.median(np.abs(x - np.median(x)))
        return dict(max=float(s.max()), p95=float(np.percentile(s, 95)), median=float(np.median(s)),
                    scatter0=float(mad(r0_)), scatterA=float(mad(rA)), worst_conv=worst)
    # controls
    y1 = cluster_yield(MU2, 1.0); check(y1[3] < 60 and y1[4] < 1e-7, "C3a cluster fixed point CONVERGED at A=mu^2", f"{y1[3]} iterations, last change {y1[4]:.1e} dex")
    def cluster_yield_fixedR(A, R_cut):
        r = np.geomspace(1*kpc, R_cut, 4000); gb = G*Menc_cl(r)/r**2
        d, g, g0, Mr, nit, chg = fixed_point(r, gb, A, a0, kern)
        return float(np.interp(R_CORE, r, (g - g0)*r**2/G))/Msun, nit, chg
    ys = cluster_yield_fixedR(1e-3*MU2, INV_MU)[0]; yb = cluster_yield_fixedR(MU2, INV_MU)[0]
    check(0 < ys < 2e-3*yb, "C3b A -> 0 gives zero yield, linearly (fixed R_cut = 1 Mpc)", f"yield(1e-3 mu^2)/yield(mu^2) = {ys/yb:.2e}")
    # linearity of the SOURCE map at fixed |Phi| (the response definition), not of the self-consistent yield
    rlin = np.geomspace(1*kpc, INV_MU, 4000); dlin = depth(rlin, kern(G*Menc_cl(rlin)/rlin**2, a0))
    check(abs(resp_mass(rlin, dlin, 2*MU2)[-1]/resp_mass(rlin, dlin, MU2)[-1] - 2) < 1e-12, "C3c source map linear in A at fixed |Phi|")
    Mdyn0 = float(kern(G*Menc_cl(R_CORE)/R_CORE**2, a0)*R_CORE**2/G)/Msun
    print(f"  cluster MOND dynamical mass inside 420 kpc (no response): {Mdyn0:.3e} Msun; targets {M_TARGET}")
    RES["Mdyn_mond_core"] = Mdyn0
    table = []
    for kR in KR_LIST:
        A_max_core = (kR*INV_MU/R_CORE)**2*MU2     # beyond this the core radius exceeds R_cut (the core straddles the oscillation)
        print(f"\n  kR = {kR:.3f}: R_cut = {kR:.2f}/sqrt(A); the 420-kpc core stays inside R_cut for A <= {A_max_core/MU2:.2f} mu^2")
        print(f"  {'A/mu^2':>7} {'1/sqrtA[Mpc]':>12} {'M_resp(<420)':>13} {'dM_dyn(<420)':>13} {'eta420':>7} {'f(1e14)':>8} {'f(1.5e14)':>9} "
              f"{'SPARC max':>10} {'p95':>8} {'median':>9} {'scatter':>14} {'MW':>7} {'group':>7}")
        ks = [0.5, 1.0, 1.5, 2.0, 3.0, 4.0, 5.0] + ([7.0, 10.0, 14.0] if kR > 1.2 else [])
        for k in ks:
            if k*MU2 > A_max_core*1.0001: continue
            A = k*MU2; dM, Mr, eta, nit, chg, d420 = cluster_yield(A, kR); st = sparc_stats(A, kR); ge, rq = group_eta(A, kR)
            row = dict(kR=kR, k=k, inv_sqrtA_Mpc=1/np.sqrt(A)/Mpc, M_resp=Mr, dM=dM, eta420=eta, f1=dM/1e14, f15=dM/1.5e14,
                       sp_max=st['max'], sp_p95=st['p95'], sp_med=st['median'], sc0=st['scatter0'], scA=st['scatterA'],
                       mw=mw_shift(A, kR), group=ge, group_r_kpc=rq/kpc, conv=max(chg, st['worst_conv']))
            table.append(row)
            print(f"  {k:>7.2f} {row['inv_sqrtA_Mpc']:>12.3f} {Mr:>13.3e} {dM:>13.3e} {eta:>7.3f} {row['f1']:>8.3f} {row['f15']:>9.3f} "
                  f"{st['max']:>10.4f} {st['p95']:>8.4f} {st['median']:>9.5f} {st['scatter0']:.4f}->{st['scatterA']:.4f} {row['mw']:>7.4f} {ge:>+7.3f}")
        check(all(rw['conv'] < 1e-6 for rw in table if rw['kR'] == kR), f"C3d all fixed points converged (kR={kR:.2f})")
        # galaxy-safe amplitude (worst SPARC point = 0.1 / 0.05 dex) within the unique-branch range
        for crit, val in [("0.1dex", 0.1), ("0.05dex", 0.05)]:
            fn = lambda lk: sparc_stats(10**lk*MU2, kR)['max'] - val
            lo, hi = np.log10(0.3), np.log10(A_max_core/MU2)
            if fn(hi) < 0:
                A_safe = 10**hi*MU2; note = "(galaxy-safe over the WHOLE unique-branch range; capped at core=R_cut)"
            else:
                A_safe = 10**brentq(fn, lo, hi, xtol=1e-4)*MU2; note = ""
            dM, Mr, eta, nit, chg, d420 = cluster_yield(A_safe, kR); st = sparc_stats(A_safe, kR)
            RES[f"A_safe_{crit}_kR{kR:.2f}"] = dict(A_over_mu2=A_safe/MU2, f1=dM/1e14, f15=dM/1.5e14, eta420=eta, sp_max=st['max'],
                                                   scatter0=st['scatter0'], scatterA=st['scatterA'], mw=mw_shift(A_safe, kR), capped=bool(note))
            print(f"  GALAXY-SAFE ({crit} worst SPARC point) kR={kR:.2f}: A = {A_safe/MU2:.2f} mu^2 (1/sqrtA = {1/np.sqrt(A_safe)/Mpc:.2f} Mpc) -> "
                  f"cluster dM_dyn(<420) = {dM:.3e} = {dM/1e14*100:.0f}% of 1e14 / {dM/1.5e14*100:.0f}% of 1.5e14; eta(420)={eta:.3f}; "
                  f"SPARC scatter {st['scatter0']:.4f}->{st['scatterA']:.4f}; MW {mw_shift(A_safe, kR):.4f} dex {note}")
        for fr in [0.5, 1.0]:
            fn = lambda lk: cluster_yield(10**lk*MU2, kR)[0]/1e14 - fr
            lo, hi = np.log10(0.3), np.log10(A_max_core/MU2)
            if fn(hi) < 0:
                print(f"  AMPLITUDE for {fr*100:.0f}% of 1e14 (kR={kR:.2f}): NOT REACHED inside the unique branch (core <= R_cut); "
                      f"max yield at A={A_max_core/MU2:.2f} mu^2 is {cluster_yield(A_max_core, kR)[0]/1e14*100:.0f}%")
                RES[f"A_for_{int(fr*100)}pct_kR{kR:.2f}"] = dict(reached=False, max_frac=cluster_yield(A_max_core, kR)[0]/1e14)
                continue
            A_need = 10**brentq(fn, lo, hi, xtol=1e-4)*MU2; st = sparc_stats(A_need, kR); ge, rq = group_eta(A_need, kR)
            RES[f"A_for_{int(fr*100)}pct_kR{kR:.2f}"] = dict(reached=True, A_over_mu2=A_need/MU2, inv_sqrtA_Mpc=1/np.sqrt(A_need)/Mpc,
                                                            sp_max=st['max'], sp_p95=st['p95'], sp_med=st['median'],
                                                            scatter0=st['scatter0'], scatterA=st['scatterA'], mw=mw_shift(A_need, kR), group=ge)
            print(f"  AMPLITUDE for {fr*100:.0f}% of 1e14 (kR={kR:.2f}): A = {A_need/MU2:.2f} mu^2 (1/sqrtA = {1/np.sqrt(A_need)/Mpc:.2f} Mpc) -> "
                  f"SPARC worst {st['max']:.4f} dex, p95 {st['p95']:.4f}, median {st['median']:.5f}, scatter {st['scatter0']:.4f}->{st['scatterA']:.4f}; "
                  f"MW {mw_shift(A_need, kR):.4f} dex; group eta-1 = {ge:+.3f} @ {rq/kpc:.0f} kpc")
    RES["response_table"] = table

    # ---------------------------------------------------------------- PART 2b: FIXED R_cut, amplitude toward the Dirichlet resonance
    print("\nPART 2b -- FIXED R_cut = 1 Mpc, amplitude A raised: the yield vs sqrt(A) R_cut / pi (the Dirichlet Helmholtz resonance at pi)")
    print("  (cluster by exact ODE shoot; galaxies by fixed point; the growth toward pi IS the phase/boundary tune -- the galaxy stays far from it)")
    print(f"  {'sqrtA*Rcut/pi':>13} {'A/mu^2':>7} {'dM_dyn(<420)':>13} {'eta420':>7} {'f(1e14)':>8} {'SPARC worst':>11} {'p95':>8} {'median':>9} {'scatter':>14} {'MW':>7} {'gal conv':>9}")
    def cluster_yield_ode_fixedR(A, R_cut):
        r_n, Phi_n, g_n = ode_shoot(A, rho_cl, Menc_cl, a0, kern, 1*kpc, R_cut)
        gM_n = kern(G*Menc_cl(r_n)/r_n**2, a0)
        return float(np.interp(R_CORE, r_n, (g_n - gM_n)*r_n**2/G))/Msun, float(np.interp(R_CORE, r_n, g_n/gM_n))
    def sparc_stats_fixedR(A, R_cut):
        shifts, res0, resA, worst = [], [], [], 0.0
        for name, R, gbar, gobs in sparc:
            r = np.geomspace(0.1*R[0], R_cut, 2500); gb = sparc_gbar_on_grid(R, gbar, r)
            d, g, g0, Mr, nit, chg = fixed_point(r, gb, A, a0, kern); worst = max(worst, chg)
            gp = np.interp(R, r, g); gz = np.interp(R, r, g0)
            shifts.append(np.log10(gp/gz)); res0.append(np.log10(gobs/gz)); resA.append(np.log10(gobs/gp))
        s_ = np.concatenate(shifts); r0_ = np.concatenate(res0); rA = np.concatenate(resA)
        mad = lambda x: 1.4826*np.median(np.abs(x - np.median(x)))
        return dict(max=float(s_.max()), p95=float(np.percentile(s_, 95)), median=float(np.median(s_)), scatter0=float(mad(r0_)), scatterA=float(mad(rA)), worst_conv=worst)
    def mw_shift_fixedR(A, R_cut):
        r_n, Phi_n, g_n = ode_shoot(A, rho_mw, Menc_mw, a0, kern, 0.05*kpc, R_cut)
        gM_n = kern(G*Menc_mw(r_n)/r_n**2, a0); sel = (r_n >= 5*kpc) & (r_n <= 30*kpc)
        return float(np.max(np.log10(g_n[sel]/gM_n[sel])))
    res_tab = []
    for frac_pi in [0.318, 0.5, 0.636, 0.8, 0.9, 0.95]:
        A = (frac_pi*np.pi/INV_MU)**2
        dM, eta = cluster_yield_ode_fixedR(A, INV_MU); st = sparc_stats_fixedR(A, INV_MU); mw = mw_shift_fixedR(A, INV_MU)
        row = dict(frac_pi=frac_pi, k=A/MU2, dM=dM, eta420=eta, f1=dM/1e14, sp_max=st['max'], sp_p95=st['p95'], sp_med=st['median'], sc0=st['scatter0'], scA=st['scatterA'], mw=mw, conv=st['worst_conv'])
        res_tab.append(row)
        print(f"  {frac_pi:>13.3f} {A/MU2:>7.2f} {dM:>13.3e} {eta:>7.3f} {dM/1e14:>8.3f} {st['max']:>11.4f} {st['p95']:>8.4f} {st['median']:>9.5f} {st['scatter0']:.4f}->{st['scatterA']:.4f} {mw:>7.4f} {st['worst_conv']:>9.1e}")
    RES["resonance_table"] = res_tab
    # the amplitude at which 50% / 100% of 1e14 is reached at fixed R_cut, and where that sits relative to the resonance
    for fr in [0.5, 1.0]:
        fn = lambda lf: cluster_yield_ode_fixedR((lf*np.pi/INV_MU)**2, INV_MU)[0]/1e14 - fr
        if fn(0.97) < 0:
            print(f"  {fr*100:.0f}% of 1e14 at fixed R_cut=1 Mpc: NOT reached below sqrtA R_cut = 0.97 pi (max there {cluster_yield_ode_fixedR((0.97*np.pi/INV_MU)**2, INV_MU)[0]/1e14*100:.0f}%)")
            RES[f"fixedR_{int(fr*100)}pct"] = dict(reached=False); continue
        f_pi = brentq(fn, 0.3, 0.97, xtol=1e-4); A = (f_pi*np.pi/INV_MU)**2; st = sparc_stats_fixedR(A, INV_MU); mw = mw_shift_fixedR(A, INV_MU)
        RES[f"fixedR_{int(fr*100)}pct"] = dict(reached=True, frac_pi=f_pi, A_over_mu2=A/MU2, sp_max=st['max'], sp_p95=st['p95'], sp_med=st['median'], scatter0=st['scatter0'], scatterA=st['scatterA'], mw=mw, gal_conv=st['worst_conv'])
        print(f"  {fr*100:.0f}% of 1e14 at fixed R_cut=1 Mpc: reached at sqrtA R_cut = {f_pi:.3f} pi (A = {A/MU2:.2f} mu^2) -> SPARC worst {st['max']:.4f} dex, p95 {st['p95']:.4f}, "
              f"median {st['median']:.5f}, scatter {st['scatter0']:.4f}->{st['scatterA']:.4f}; MW {mw:.4f} dex; galaxy FP conv {st['worst_conv']:.1e}")
    # resonance diagnostic: the homogeneous Dirichlet mode -- galaxy shift vs cluster yield both grow, ratio stays
    r5 = res_tab[1]; r9 = res_tab[-2]
    check(r9['f1'] > r5['f1'] and r9['sp_max'] > r5['sp_max'],
          "C7 toward the resonance BOTH the cluster yield and the galaxy cost grow (the boundary/phase lever is shared, not cluster-only)",
          f"cluster f: {r5['f1']:.3f} -> {r9['f1']:.3f}; SPARC worst: {r5['sp_max']:.4f} -> {r9['sp_max']:.4f} dex")

    # decomposition of the discriminant at A = mu^2, kR = 1
    r = np.geomspace(1*kpc, INV_MU, 4000); gb = G*Menc_cl(r)/r**2; d_c, g_c, g0c, _, _, _ = fixed_point(r, gb, MU2, a0, kern)
    dc420 = float(np.interp(R_CORE, r, d_c)); v2c = float(np.interp(R_CORE, r, g0c*r))
    dg, v2g = [], []
    for name, R, gbar, gobs in sparc:
        rr = np.geomspace(0.1*R[0], INV_MU, 2500); gbb = sparc_gbar_on_grid(R, gbar, rr)
        d_, g_, g0_, _, _, _ = fixed_point(rr, gbb, MU2, a0, kern); rq = min(20*kpc, R[-1])
        dg.append(np.interp(rq, rr, d_)); v2g.append(np.interp(rq, rr, g0_)*rq)
    dg = float(np.median(dg)); v2g = float(np.median(v2g))
    print(f"\n  DECOMPOSITION (fractional phantom ~ A|Phi|R^2/v^2): depth ratio cluster@420kpc / SPARC-median@<=20kpc = {dc420/dg:.1f}x; "
          f"v^2 ratio = {v2c/v2g:.1f}x; (R ratio)^2 = {(R_CORE/(20*kpc))**2:.0f}x  =>  dimensionless depth key |Phi|/v^2 ratio = {(dc420/v2c)/(dg/v2g):.2f}x; "
          f"the discriminating power is the geometric (sqrt(A) R)^2 envelope, NOT the depth per se.")
    RES["decomp"] = dict(depth_ratio=dc420/dg, v2_ratio=v2c/v2g, R2_ratio=(R_CORE/(20*kpc))**2, depth_over_v2_ratio=(dc420/v2c)/(dg/v2g))

    # ================================================================ PART 3: density-keyed mutation control
    print("\nPART 3 -- MUTATION CONTROL on the response: density-keyed rho_resp = B rho_b^p (p=1,2), galaxy-safe B (worst SPARC point 0.1 dex)")
    r_c = np.geomspace(1*kpc, INV_MU, 4000); gb_c = G*Menc_cl(r_c)/r_c**2
    gbar_all = np.concatenate([s[2] for s in sparc]); R_all = np.concatenate([s[1] for s in sparc])
    for p in [1, 2]:
        rho_c = rho_cl(r_c); Mp_c = 4*np.pi*cumulative_trapezoid(rho_c**p*r_c**2, r_c, initial=0.0); norm = (1e-24)**(p-1)
        def cl_yield_dens(B):
            gp = kern(gb_c + G*B*Mp_c/norm/r_c**2, a0); g0 = kern(gb_c, a0)
            return float(np.interp(R_CORE, r_c, (gp-g0)*r_c**2/G))/Msun
        Mp_list = []
        for name, R, gbar, gobs in sparc:
            rr = np.geomspace(0.1*R[0], R[-1], 1500); gbb = sparc_gbar_on_grid(R, gbar, rr)
            rho = np.clip(np.gradient(gbb*rr**2/G, rr)/(4*np.pi*rr**2), 0, None)
            Mp_list.append(np.interp(R, rr, 4*np.pi*cumulative_trapezoid(rho**p*rr**2, rr, initial=0.0)))
        Mp_all = np.concatenate(Mp_list)
        sp_max_dens = lambda B: float(np.max(np.log10(kern(gbar_all + G*B*Mp_all/norm/R_all**2, a0)/kern(gbar_all, a0))))
        B = 10**brentq(lambda l: sp_max_dens(10**l) - 0.1, -12, 12, xtol=1e-4); dM = cl_yield_dens(B)
        print(f"    p={p}: galaxy-safe B -> cluster dM_dyn(<420 kpc) = {dM:.3e} Msun = {dM/1e14*100:.1f}% of 1e14 ({dM/1.5e14*100:.1f}% of 1.5e14)")
        RES[f"density_keyed_p{p}_frac_1e14"] = dM/1e14
        check(dM/1e14 < 0.5, f"C4 density-keyed p={p} response does NOT reach 50% at a galaxy-safe amplitude", f"{dM/1e14*100:.1f}%")
    st1 = sparc_stats(MU2, 1.0); y = cluster_yield(MU2, 1.0)
    print(f"    depth-keyed at A=mu^2, kR=1: cluster core boost {np.log10(y[2]):.4f} dex vs SPARC worst {st1['max']:.5f} / median {st1['median']:.6f} dex "
          f"-> response lands in the cluster FIRST by {np.log10(y[2])/st1['max']:.0f}x (worst) / {np.log10(y[2])/st1['median']:.0f}x (median)")
    RES["response_ordering_cl_over_SPARC_worst"] = np.log10(y[2])/st1['max']; RES["response_ordering_cl_over_SPARC_median"] = np.log10(y[2])/st1['median']

    # ================================================================ PART 4: ODE cross-checks
    print("\nPART 4 -- CROSS-CHECK: exact canonical-momentum ODE (repo solver form) vs the fixed point, same boundary Phi(R_cut)=0")
    # A=0 -> analytic MOND
    r_z, Phi_z, g_z = ode_march(0.0, rho_cl, Menc_cl, a0, kern, 1*kpc, INV_MU, -1e12)
    gM = kern(G*Menc_cl(r_z)/r_z**2, a0); i5 = np.argmin(np.abs(r_z - R_CORE))
    check(abs(g_z[i5]/gM[i5] - 1) < 1e-6, "C5a ODE at A=0 reproduces the analytic kernel (cluster, 420 kpc)", f"ratio = {g_z[i5]/gM[i5]:.8f}")
    for kR in KR_LIST:
        R_cut = kR*INV_MU
        r_n, Phi_n, g_n = ode_shoot(MU2, rho_cl, Menc_cl, a0, kern, 1*kpc, R_cut)
        gM_n = kern(G*Menc_cl(r_n)/r_n**2, a0); dM_ode = float(np.interp(R_CORE, r_n, (g_n - gM_n)*r_n**2/G))/Msun
        dM_fp, Mr, eta, nit, chg, d420 = cluster_yield(MU2, kR)
        check(abs(float(np.interp(R_cut, r_n, Phi_n))) < 1e-4*abs(Phi_n[0]), f"C5b shot satisfies Phi(R_cut)=0 (kR={kR:.2f})",
              f"|Phi(R_cut)|/|Phi(0)| = {abs(float(np.interp(R_cut, r_n, Phi_n)))/abs(Phi_n[0]):.1e}")
        check(abs(dM_ode/dM_fp - 1) < 0.02, f"C5c ODE == fixed point on the cluster core yield (kR={kR:.2f})",
              f"ODE {dM_ode:.4e} vs FP {dM_fp:.4e} Msun, ratio {dM_ode/dM_fp:.4f}; |Phi(420)| ODE {-float(np.interp(R_CORE, r_n, Phi_n)):.4e} vs FP {d420:.4e}")
        Phi0s = np.linspace(-6e12, 6e12, 7)
        vals = [float(np.interp(R_cut, *ode_march(MU2, rho_cl, Menc_cl, a0, kern, 1*kpc, R_cut, p0, n=1500)[:2])) for p0 in Phi0s]
        check(np.all(np.diff(vals) > 0), f"C5d Phi(0) -> Phi(R_cut) monotone at sqrt(A) R_cut = {kR:.2f} rad: the Phi(R_cut)=0 branch is UNIQUE")
        RES[f"ode_check_kR{kR:.2f}"] = dict(dM_ode=dM_ode, dM_fp=dM_fp, ratio=dM_ode/dM_fp)
    # MW galaxy: ODE vs fixed point
    r_n, Phi_n, g_n = ode_shoot(MU2, rho_mw, Menc_mw, a0, kern, 0.05*kpc, INV_MU)
    gM_n = kern(G*Menc_mw(r_n)/r_n**2, a0); sel = (r_n >= 5*kpc) & (r_n <= 30*kpc)
    mw_ode = float(np.max(np.log10(g_n[sel]/gM_n[sel]))); mw_fp = mw_shift(MU2, 1.0)
    check(abs(mw_ode/mw_fp - 1) < 0.05, "C5e ODE == fixed point on the MW galaxy shift (5-30 kpc)", f"ODE {mw_ode:.5f} vs FP {mw_fp:.5f} dex")
    # kernel sensitivity: DS24 'simple' M(x) (the repo solver's) at A=mu^2, kR=1
    kern2 = KERNEL['DS24_simple']
    r = np.geomspace(1*kpc, INV_MU, 4000); gb = G*Menc_cl(r)/r**2; d2, g2, g02, _, _, _ = fixed_point(r, gb, MU2, a0, kern2)
    dM2 = float(np.interp(R_CORE, r, (g2 - g02)*r**2/G))/Msun
    print(f"    kernel sensitivity: DS24 'simple' M(x) (repo solver) at A=mu^2,kR=1 -> dM_dyn(<420) = {dM2:.3e} Msun ({dM2/1e14*100:.0f}% of 1e14) "
          f"vs framework kernel {y1[0]:.3e} ({y1[0]/1e14*100:.0f}%)")
    RES["kernel_sens_DS24_frac_1e14"] = dM2/1e14
    # the paper's inner-anchor convention (DIFFERENT phase): Phi(20kpc) = -a0 x0 r0, DS24 kernel, march to 8 Mpc
    r0 = 20*kpc; q0 = G*Menc_cl(r0)/(a0*r0**2); Phi0_nat = -a0*(q0 + np.sqrt(q0))*r0
    r_p, Phi_p, g_p = ode_march(MU2, rho_cl, Menc_cl, a0, kern2, r0, 8*Mpc, Phi0_nat, n=8000)
    gM_p = kern2(G*Menc_cl(r_p)/r_p**2, a0)
    dM_paper = float(np.interp(R_CORE, r_p, (g_p - gM_p)*r_p**2/G))/Msun; eta500 = float(np.interp(R500_cl, r_p, g_p/gM_p))
    print(f"    reference -- the paper's 'natural' inner-anchor convention (dPhi0=0, DS24 kernel, march to 8 Mpc): dM_dyn(<420) = {dM_paper:+.3e} Msun, "
          f"eta(R500) = {eta500:+.3f}  [reproduces the paper's deficit branch: a DIFFERENT phase; whether dynamics picks it is Item A]")
    RES["paper_anchor"] = dict(dM=dM_paper, eta500=eta500)

json_path = os.path.join(HERE, "itemB_potential_depth_ordering_2026.json")
with open(json_path, "w") as fh: json.dump(RESULTS, fh, indent=1, default=float)
print(f"\nresults -> {json_path}")

print("\n" + "="*100); print("SUMMARY"); print("="*100)
for foot in FOOTINGS:
    R = RESULTS[foot]; d1 = R["depth_kR_1.00"]; d2 = R["depth_kR_1.57"]
    print(f"[{foot}] DEPTH ORDERING (self-consistent, A=mu^2): kR=1: cluster {d1['cluster_max']:.2e} > group {d1['group_max']:.2e} > deepest SPARC {d1['SPARC_max']:.2e} "
          f"({d1['SPARC_deepest']}) > MW {d1['MW_max']:.2e}; cluster/deepest-galaxy = {d1['ratio_cl_deepest']:.1f}x (kR=pi/2: {d2['ratio_cl_deepest']:.1f}x), "
          f"cluster/median-SPARC = {d1['ratio_cl_median']:.0f}x, Newtonian control {d1['ratio_newton']:.1f}x; cluster@420kpc / deepest RAR point = "
          f"{d1['ratio_cl420_pt']:.1f}x (kR=1) / {d2['ratio_cl420_pt']:.1f}x (kR=pi/2). DENSITY ordering REVERSED (MW/cluster {R['density_ratio_MW_over_cluster_local']:.0f}x).")
    t = [rw for rw in R['response_table'] if rw['kR'] == 1.0 and rw['k'] == 1.0][0]
    s1 = R["A_safe_0.1dex_kR1.00"]; s2 = R["A_safe_0.1dex_kR1.57"]; f1 = R["A_for_50pct_kR1.00"]; f2 = R["A_for_50pct_kR1.57"]
    print(f"[{foot}] HELMHOLTZ p=1 (self-consistent): natural A=mu^2 (1/mu=1 Mpc), kR=1 -> {t['f1']*100:.0f}% of 1e14 ({t['f15']*100:.0f}% of 1.5e14), eta(420)={t['eta420']:.3f}, "
          f"SPARC worst {t['sp_max']:.4f} / median {t['sp_med']:.5f} dex, MW {t['mw']:.4f} dex. "
          f"Galaxy-safe(0.1 dex) A = {s1['A_over_mu2']:.2f} mu^2 -> {s1['f1']*100:.0f}% of 1e14 (kR=1{', capped by core=R_cut' if s1['capped'] else ''}); "
          f"kR=pi/2: A = {s2['A_over_mu2']:.2f} mu^2 -> {s2['f1']*100:.0f}%{' (capped)' if s2['capped'] else ''}. "
          f"50% of 1e14: kR=1 " + (f"A={f1['A_over_mu2']:.2f} mu^2 (1/sqrtA={f1['inv_sqrtA_Mpc']:.2f} Mpc) at SPARC worst {f1['sp_max']:.4f} dex" if f1['reached'] else f"NOT reached (max {f1['max_frac']*100:.0f}%)")
          + "; kR=pi/2 " + (f"A={f2['A_over_mu2']:.2f} mu^2 (1/sqrtA={f2['inv_sqrtA_Mpc']:.2f} Mpc) at SPARC worst {f2['sp_max']:.4f} dex" if f2['reached'] else f"NOT reached (max {f2['max_frac']*100:.0f}%)")
          + f". FIXED R_cut=1 Mpc toward resonance: 50% " + (f"at sqrtA R_cut = {R['fixedR_50pct']['frac_pi']:.2f} pi (A={R['fixedR_50pct']['A_over_mu2']:.1f} mu^2) with SPARC worst {R['fixedR_50pct']['sp_max']:.4f} dex" if R['fixedR_50pct']['reached'] else "NOT reached")
          + "; 100% " + (f"at {R['fixedR_100pct']['frac_pi']:.2f} pi (A={R['fixedR_100pct']['A_over_mu2']:.1f} mu^2), SPARC worst {R['fixedR_100pct']['sp_max']:.4f} dex" if R['fixedR_100pct']['reached'] else "NOT reached")
          + f". Density-keyed mutation p=1/p=2 at galaxy-safe: {R['density_keyed_p1_frac_1e14']*100:.0f}% / {R['density_keyed_p2_frac_1e14']*100:.1f}%. "
          f"ODE/FP = {R['ode_check_kR1.00']['ratio']:.3f}. Paper-anchor phase: dM = {R['paper_anchor']['dM']:+.2e} (eta500 {R['paper_anchor']['eta500']:+.2f}).")

if FAIL:
    print(f"\n*** {len(FAIL)} CHECK(S) FAILED ***")
    for f in FAIL: print("   -", f)
    sys.exit(1)
print(f"\nALL {NCHK[0]} CHECKS PASSED (incl. mutation controls C2, C4 and two-method checks C5)")
sys.exit(0)
