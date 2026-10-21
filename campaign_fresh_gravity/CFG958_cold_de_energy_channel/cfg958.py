"""CFG958 -- one energy channel, cold energy <-> dark energy (interacting vacuum), for SCT's body energy (C-E), CFG935's settling
sink and CFG955's relaxation reservoir.
Criteria: FROZEN_CRITERIA.md (8d7764d74, committed alone first); AMENDMENT_A1_pre_result.md (11e0bdd4b, pre-result);
AMENDMENT_A2_weff_line.md (84c9ebd9c, before any script, after a disclosed hand check).
Run (one core, one process, < 1 GB):
    CFG958_STAGE=K OMP_NUM_THREADS=1 nice -n 10 python3 cfg958.py     -> cfg958_K.out, cfg958_K.json      (exit 0 iff K passes)
    CFG958_MUTATE=1 OMP_NUM_THREADS=1 nice -n 10 python3 cfg958.py    -> cfg958_MUTATE.out, cfg958_MUTATE.json (exit 1 iff every tooth bites)
    OMP_NUM_THREADS=1 nice -n 10 python3 cfg958.py                    -> cfg958.out, cfg958.json          (K + main)
CFG689 numbers are TRANSCRIBED from its committed cfg689.json with the Read tool (the brief limits CFG689 access to the Read tool);
no process opens a CFG689 file. Machinery copied verbatim, with attribution, from cfg953.py (census, domain_sct, kernels, NGC 3198
loader, S-En recipe, the N-body toy). kappa = 1/2 FITTED; footings never pooled; cold energy, no particle species; not theory closed."""
import os, sys, io, json, math, time, resource, contextlib
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"):
    os.environ.setdefault(_v, "1")
import numpy as np
import sympy as sp
from scipy.optimize import brentq
from scipy.special import erf

HERE = os.path.dirname(os.path.abspath(__file__)); LANES = os.path.dirname(HERE); REPO = os.path.dirname(LANES)
MUT = os.environ.get("CFG958_MUTATE", "0") == "1"
STAGE = os.environ.get("CFG958_STAGE", "MAIN").upper()
TAG = "_MUTATE" if MUT else ("_K" if STAGE == "K" else "")
CRIT, AM1, AM2 = "8d7764d74", "11e0bdd4b", "84c9ebd9c"
OUT = []; RES = {"lane": "CFG958", "criteria": CRIT, "A1": AM1, "A2": AM2, "mutate": MUT, "stage": STAGE, "checks": {}}
T0 = time.time(); RSS_LIMIT = 1.0e9


def P(s=""):
    print(s, flush=True); OUT.append(str(s))


def rss_val():
    r = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    return r if sys.platform == "darwin" else r * 1024


def dump():
    RES["runtime_s"] = round(time.time() - T0, 2); RES["peak_rss_GB"] = round(rss_val() / 1e9, 3)
    json.dump(RES, open(os.path.join(HERE, f"cfg958{TAG}.json"), "w"), indent=1,
              default=lambda o: o.tolist() if isinstance(o, np.ndarray) else (float(o) if isinstance(o, (np.floating,)) else str(o)))
    open(os.path.join(HERE, f"cfg958{TAG}.out"), "w").write("\n".join(OUT) + "\n")


def rss_guard(where=""):
    r = rss_val()
    if r > RSS_LIMIT:
        P(f"RSS GUARD: {r / 1e9:.2f} GB > 1 GB at {where}; aborting"); dump(); sys.exit(3)
    return r


def chk(name, ok, detail=""):
    RES["checks"][name] = {"pass": bool(ok), "detail": str(detail)}
    P(f"  [{'PASS' if ok else 'FAIL'}] {name}: {detail}")
    return bool(ok)


# ================================================================================================ inputs (read-only)
sys.path.insert(0, LANES)
with contextlib.redirect_stdout(io.StringIO()):
    import CFG4_common as C4                                          # footings, nu_mono (read-only)
A0 = dict(C4.A0); FOOTS = ("canonical", "alt")
assert abs(A0["canonical"] - 9.3603e-11) < 1e-15 and abs(A0["alt"] - 1.1312e-10) < 1e-15
G_SI, C_SI, MSUN, PC, KPC = C4.G_SI, C4.C_SI, C4.MSUN, C4.PC, C4.KPC
MPC = 1e3 * KPC; GYR = 1e9 * 365.25 * 86400.0

# ---- cfg953.py census constants and functions (verbatim; cfg947 lineage)
OM_B, OM_C = 0.02237, 0.1200; FB = OM_B / (OM_B + OM_C)
GE, MSE, MPCE, HE = 6.674e-11, 1.989e30, 3.0857e22, 0.674
RMIN = 0.78125
_dta = json.load(open(os.path.join(LANES, "CFG654_independent_inputs", "cfg654_delta_ta.json")))
DTA0 = float(_dta["D"][0]); assert abs(_dta["z"][0]) < 1e-12
RHOM_H = 0.315 * 2.775e11


def fret_of(lM):
    if lM < 12.5: f = 0.10
    elif lM < 13.5: f = 0.10 + 0.45 * (lM - 12.5)
    else: f = min(0.55 + 0.30 * (lM - 13.5), 0.90)
    return min(f, 1.0)


def M_ta(R, D):
    return (4 * math.pi / 3) * R ** 3 * D * RHOM_H


def census(Mb_msun):
    f = lambda lR: fret_of(math.log10(M_ta(math.exp(lR), DTA0))) * FB * M_ta(math.exp(lR), DTA0) / HE - Mb_msun
    lR = brentq(f, math.log(1e-6), math.log(1e3), xtol=1e-14, rtol=1e-14)
    R = math.exp(lR); Mh = M_ta(R, DTA0); fr = fret_of(math.log10(Mh))
    return dict(R=R, fr=fr, Mta_h=Mh, Mta=Mh / HE)


def law_simple(gN, a0):
    gN = np.asarray(gN, float)
    return 0.5 * (gN + np.sqrt(gN * gN + 4.0 * gN * a0))


def law_mono(gN, a0):
    gN = np.asarray(gN, float)
    return gN * C4.nu_mono(gN / a0)


KERN = {"simple": law_simple, "mono": law_mono}


def Mph_pt(r, M, a0, kern):
    gn = G_SI * M / r ** 2
    return r * r * (float(KERN[kern](gn, a0)) - gn) / G_SI


def root_pt(M, Mc, a0, kern):
    rM = math.sqrt(G_SI * M / a0)
    return math.exp(brentq(lambda lr: Mph_pt(math.exp(lr), M, a0, kern) - Mc, math.log(1e-4 * rM), math.log(1e4 * rM),
                           xtol=1e-15, rtol=1e-15))


def domain_sct(Mb_msun, a0, kern="simple"):
    c = census(Mb_msun); Mc = (1 - FB) * c["Mta"]
    M = Mb_msun * MSUN; rM = math.sqrt(G_SI * M / a0)
    re = root_pt(M, Mc * MSUN, a0, kern)
    return dict(c, Mc=Mc, N=Mc / Mb_msun, r_on=c["R"] / HE * MPCE, r_e=re, rM=rM, yE=(rM / re) ** 2)


# ---- NGC 3198 (record SPARC file, Upsilon 0.61; cfg953.py verbatim)
_d = np.genfromtxt(os.path.join(REPO, "real_research", "data", "sparc_data", "NGC3198_rotmod.dat"), comments="#")
R_N = _d[:, 0] * KPC
GN_N = (_d[:, 3] * 1e3 * np.abs(_d[:, 3] * 1e3) + 0.61 * _d[:, 4] * 1e3 * np.abs(_d[:, 4] * 1e3)
        + 0.61 * _d[:, 5] * 1e3 * np.abs(_d[:, 5] * 1e3)) / R_N
MBR_N = GN_N * R_N ** 2 / G_SI
MB_N = MBR_N[-1] / MSUN


def sen_row(Mb, a0):
    """CFG953 S-En recipe (cfg953.py lines 1008-1017, verbatim arithmetic): dust uniform within r_ON -> body inside r_e."""
    dom = domain_sct(float(Mb), a0, "simple"); M = Mb * MSUN; Mc = dom["Mc"] * MSUN; ron = dom["r_on"]; re = dom["r_e"]
    Wi = -0.6 * G_SI * Mc ** 2 / ron - 1.5 * G_SI * M * Mc / ron
    rg = np.geomspace(1e-6 * dom["rM"], re, 6000)
    Ms = np.array([Mph_pt(x_, M, a0, "simple") for x_ in rg]); Ms = np.minimum(Ms, Mc)
    dM = np.diff(Ms); rm = np.sqrt(rg[1:] * rg[:-1]); Mm = 0.5 * (Ms[1:] + Ms[:-1])
    Wf = -G_SI * float(np.sum(Mm * dM / rm)) - G_SI * M * float(np.sum(dM / rm))
    Erel = Wi - Wf
    vf2 = math.sqrt(G_SI * M * a0)
    return dict(Mb=float(Mb), N=dom["N"], re_over_ron=re / ron, Erel_over_Wf=Erel / abs(Wf), Erel_over_Mcc2=Erel / (Mc * C_SI ** 2),
                Erel_over_Mcvf2=Erel / (Mc * vf2), Erel=Erel, absWf=abs(Wf), Mc_kg=Mc, r_e=re, r_on=ron, rM=dom["rM"], vf2=vf2)


# ---- CFG689 primary (TRANSCRIBED with the Read tool from CFG689's committed cfg689.json; keys named)
CFG689_TRANSCRIBED = {
    "source": "CFG689 cfg689.json (committed in 6c064b83a); keys BAO+SN.P2.{nodes_free, omega_c, omega_b, omega_k}, BAO+SN.P1.<z>.sqrtX_q "
              "(percentiles 2.5/16/50/84/97.5), BAO+SN.posterior.{node_mean, node_std}, P3.H0_q[2]",
    "nodes_z": [0.0, 0.4, 0.7, 1.0, 1.5, 2.33],
    "omega_DE_best": [0.3116063332228203, 0.3245293417306382, 0.3928896049649603, 0.262104173545215, 0.2799425757675178, 0.26283929581363],
    "omega_c": 0.12019539890307804, "omega_b": 0.022360124758721615, "omega_k": 0.003891598696282198,
    "sqrtX_q": {"1.0": [0.5523699064452342, 0.7624306938344106, 0.9132283482966455, 1.0272172949247862, 1.116681787899383],
                "1.2": [0.5264896371694601, 0.7621156899497521, 0.9247646892417826, 1.0477960870456662, 1.1422771966386507],
                "1.5": [0.26957931364156335, 0.7064862315571994, 0.9420018196773202, 1.1154894642281235, 1.2498313738255078],
                "2.33": [0.0, 0.3247049655284417, 0.9093594712388365, 1.2116496391902274, 1.4220192639773874]},
    "node_mean": [0.31048520097761617, 0.3220876822715694, 0.39084700396553157, 0.25838160813406835, 0.27610060181700163, 0.25626644329330733],
    "node_std": [0.023343161479677126, 0.03947073279698555, 0.06270859657062676, 0.08905415942982488, 0.13066607319481163, 0.22732946960447414],
    "H0_median": 67.69554675810943}
README689 = {"1.0": (0.913, 0.762, 1.027), "1.2": (0.925, 0.762, 1.048), "1.5": (0.942, 0.706, 1.115), "2.33": (0.909, 0.325, 1.212)}
ZN = np.array(CFG689_TRANSCRIBED["nodes_z"]); WDE = np.array(CFG689_TRANSCRIBED["omega_DE_best"])
OMC = CFG689_TRANSCRIBED["omega_c"]


def omega_DE(z):
    return float(np.interp(z, ZN, WDE))


H100 = 1e5 / MPC
RHO_CRIT100 = 3 * H100 ** 2 / (8 * math.pi * G_SI)
RHO_DE0 = omega_DE(0.0) * RHO_CRIT100
VBAR = RHO_DE0 * C_SI ** 2                                             # J/m^3
H0_SI = CFG689_TRANSCRIBED["H0_median"] * 1e3 / MPC

# ---- record constants used as lines or inputs (provenance)
SLIP953 = 1.3548e-5                     # CFG953 (d) worst slip, alt cluster (README / DERIVATION (d))
SLIP_LINE = 1.9e-5
DELTA_C = 0.082                         # CFG874 / CFG945 satellite EFE room (dex), as cfg953.py
Q2_CEIL = 5.2e-27                       # Park+2026 Cassini Q2 ceiling (s^-2), via CFG770 (LEDGER)
Q2_770 = 3.5e-6                         # CFG770 |Q2|/ceiling, upper end at L* = 5.75 pc (LEDGER)
HOST = 6e10; RHOST = (50.0, 100.0, 250.0)
HOSTS882 = [("H1", 1e4, 30.0), ("H2", 3e5, 200.0), ("H3", 2e7, 700.0)]
MERGE_FRAC = 0.20693377084340647        # CFG953 toy M merge draw / |E0| (cfg953_results.json e.toyM)
CLASSES = [("UFD-c", 5e3, 0.039), ("UFD-e", 3e4, 0.31), ("Draco-like", 5e5, 0.29), ("Fornax-like", 4e7, 0.93),
           ("SPARC dwarf", 1e9, 5.0), ("MW-like", 6e10, 8.0), ("group", 1e12, 100.0), ("cluster", 1e14, 500.0)]   # A1 item 2
FSW = {"canonical": {0.0: 0.1621, 0.5: 0.1552, 1.0: 0.1377}, "alt": {0.0: 0.1317, 0.5: 0.1453, 1.0: 0.1307}}   # CFG630 K6, N512
CW630 = {"canonical": {"MW": 0.7698, "cluster": 0.9859}, "alt": {"MW": 0.7905, "cluster": 1.0125}}            # CFG630 header line
M_RES_H = 100 * 5.19e9                  # CFG630 K6: route H counts > 100 m_p, m_p 5.19e9 Msun/h (N512)

P("CFG958  one energy channel: cold energy <-> dark energy (interacting vacuum)" + ("   [MUTATE]" if MUT else "") + f"   stage={STAGE}")
P(f"  criteria {CRIT}; A1 {AM1}; A2 {AM2}; kappa = 1/2 FITTED; footings never pooled; cold energy (no particle species); not theory closed")
P(f"  footings: canonical a0 = {A0['canonical']:.4e}, alt a0 = {A0['alt']:.4e};  native Delta_ta(0) = {DTA0:.6f};  engine f_b = {FB:.6f}")
P(f"  CFG689 (transcribed): omega_DE(0) = {omega_DE(0):.5f}, omega_c = {OMC:.6f}; rho_DE0 = {RHO_DE0:.4e} kg/m^3; Vbar = {VBAR:.4e} J/m^3; "
  f"H0 = {CFG689_TRANSCRIBED['H0_median']:.3f} km/s/Mpc")
P(f"  NGC 3198: {len(R_N)} radii to {R_N[-1] / KPC:.2f} kpc, M_b(< last) = {MB_N:.4e} M_sun (Upsilon 0.61)")
RES["inputs"] = dict(VBAR=VBAR, RHO_DE0=RHO_DE0, H0_SI=H0_SI, MB_NGC3198=MB_N, CFG689=CFG689_TRANSCRIBED)

# ================================================================================================ sympy structure
P("\n==================== SYMPY STRUCTURE ====================")
SY = {}


def christoffel(g, X):
    n = len(X); gi = g.inv()
    return [[[sp.simplify(sum(gi[a, d] * (sp.diff(g[d, b], X[c]) + sp.diff(g[d, c], X[b]) - sp.diff(g[b, c], X[d])) for d in range(n)) / 2)
              for c in range(n)] for b in range(n)] for a in range(n)]


def cov_div_T(T, g, X):
    n = len(X); Gm = christoffel(g, X)
    return [sp.simplify(sum(sp.diff(T[m, nu], X[m]) for m in range(n)) + sum(Gm[m][m][l] * T[l, nu] for m in range(n) for l in range(n))
                        + sum(Gm[nu][m][l] * T[m, l] for m in range(n) for l in range(n))) for nu in range(n)]


x0, x1, x2, x3 = sp.symbols("x0 x1 x2 x3", real=True); XX = [x0, x1, x2, x3]
Vfun = sp.Function("V")(*XX)
eta = sp.diag(-1, 1, 1, 1)
af = sp.Function("a")(x0)
gfrw = sp.diag(-1, af ** 2, af ** 2, af ** 2)
t1a = True; t1a_detail = []
for name, g in (("Minkowski", eta), ("flat FRW", gfrw)):
    gi = g.inv(); T = -Vfun * gi
    div = cov_div_T(T, g, XX)
    target = [-sum(gi[nu, m] * sp.diff(Vfun, XX[m]) for m in range(4)) for nu in range(4)]
    ok = all(sp.simplify(div[nu] - target[nu]) == 0 for nu in range(4))
    t1a = t1a and ok; t1a_detail.append(f"{name}: div(-V g) + grad V = 0 in all 4 components: {ok}")
SY["T1a"] = chk("T1a_vacuum_exchange_identity", t1a, "; ".join(t1a_detail) + " (Q^nu = -grad^nu V; matter receives +grad V)")

# T1b event algebra
Mb_, mb_ = sp.symbols("M m", positive=True)
Vv = sp.Matrix(sp.symbols("V1:4", real=True)); vv = sp.Matrix(sp.symbols("v1:4", real=True))
Vn = (Mb_ * Vv + mb_ * vv) / (Mb_ + mb_)
Kloss = (Mb_ * Vv.dot(Vv) + mb_ * vv.dot(vv) - (Mb_ + mb_) * Vn.dot(Vn)) / 2
kl_ok = sp.simplify(Kloss - Mb_ * mb_ / (2 * (Mb_ + mb_)) * (vv - Vv).dot(vv - Vv)) == 0
mom_ok = sp.simplify((Mb_ + mb_) * Vn - (Mb_ * Vv + mb_ * vv)) == sp.zeros(3, 1)
K_, W_, EV_, dW_ = sp.symbols("K W E_V dW", real=True)
E_before = K_ + W_ + EV_
E_after = (K_ - Kloss) + (W_ + dW_) + (EV_ + (Kloss - dW_))       # the vacuum books the CFG953 E_int increment
ev_ok = sp.simplify(E_after - E_before) == 0
dWs = sp.symbols("dW_shape", real=True)
rs_ok = sp.simplify((W_ + dWs) + (EV_ - dWs) - (W_ + EV_)) == 0
SY["T1b"] = chk("T1b_event_algebra", kl_ok and mom_ok and ev_ok and rs_ok,
                f"capture/merge K-loss = mu|dv|^2/2 >= 0: {kl_ok}; momentum adds: {mom_ok}; Delta(K + W + E_V) = 0 at an event: {ev_ok}; "
                f"reshape (E_V -= dW_shape): {rs_ok}")

# T1c momentum: boost invariance of the vacuum stress; zero net force and torque of any compact deposit
eta_r = sp.symbols("eta", real=True)
Lb = sp.Matrix([[sp.cosh(eta_r), sp.sinh(eta_r), 0, 0], [sp.sinh(eta_r), sp.cosh(eta_r), 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]])
Vs = sp.symbols("V", positive=True)
Tb = sp.simplify(Lb * (-Vs * eta.inv()) * Lb.T)
boost_ok = all(sp.simplify(Tb[0, i]) == 0 for i in (1, 2, 3)) and sp.simplify(Tb + Vs * eta.inv()) == sp.zeros(4, 4)
xs, ys, zs = sp.symbols("x y z", real=True); ax_, ay_, bz_ = sp.symbols("a_x a_y b", positive=True)
fV = sp.exp(-(xs - ax_) ** 2 - 2 * (ys - ay_) ** 2 - (zs ** 2) / bz_)       # a deliberately non-spherical, off-centre compact-ish deposit
lim = (-sp.oo, sp.oo)
I = lambda e: sp.integrate(sp.integrate(sp.integrate(e, (xs, *lim)), (ys, *lim)), (zs, *lim))
force = [sp.simplify(I(sp.diff(fV, v_))) for v_ in (xs, ys, zs)]
torque = [sp.simplify(I(ys * sp.diff(fV, zs) - zs * sp.diff(fV, ys))), sp.simplify(I(zs * sp.diff(fV, xs) - xs * sp.diff(fV, zs))),
          sp.simplify(I(xs * sp.diff(fV, ys) - ys * sp.diff(fV, xs)))]
ftq_ok = all(f_ == 0 for f_ in force) and all(t_ == 0 for t_ in torque)
# spherical compact profile with a jump at r_e (P-U): the shell term integrates to zero too
rr_, th_, ph_, re_s, A_s = sp.symbols("r theta phi r_e A", positive=True)
shell = sp.integrate(sp.integrate(A_s * sp.cos(th_) * sp.sin(th_) * re_s ** 2, (th_, 0, sp.pi)), (ph_, 0, 2 * sp.pi))
stm_ok = ftq_ok and shell == 0
SY["T1c"] = chk("T1c_momentum_and_S-TM", boost_ok and stm_ok,
                f"T_V^(0i) = 0 in every boosted frame and T_V boost-invariant: {boost_ok}; net force and torque of the reaction +grad(dV) for a "
                f"non-spherical off-centre deposit: {force} / {torque}; P-U edge shell term {shell} => the body's centroid law R4 and "
                f"CFG953's relocation term R = 0 are unchanged (per-owner holding)")

# T1d composite: vacuum lump + holding stress = dust; a rigidly translating lump is conserved (1+1, c = 1)
dVs = sp.symbols("dV", positive=True)
u_rest = sp.Matrix([1, 0, 0, 0])
Tcomp = -dVs * eta.inv() + dVs * (eta.inv() + u_rest * u_rest.T)
comp_ok = sp.simplify(Tcomp - dVs * u_rest * u_rest.T) == sp.zeros(4, 4)
tt, xx, vb = sp.symbols("t x v", real=True); gam = 1 / sp.sqrt(1 - vb ** 2)
lump = sp.Function("L")(xx - vb * tt); uu = [gam, gam * vb]
div_lump = [sp.simplify(sp.diff(lump * uu[0] * uu[nu], tt) + sp.diff(lump * uu[1] * uu[nu], xx)) for nu in (0, 1)]
SY["T1d"] = chk("T1d_composite_is_dust", comp_ok and all(d_ == 0 for d_ in div_lump),
                f"-dV g + dV (g + u u) = dV u u: {comp_ok}; d_mu(L(x - vt) u^mu u^nu) = {div_lump}: the composite has no stress (no slip) "
                f"and gravitates as dust of energy dV, exactly as CFG953's E_int would")

# T-S entropy
fu, fl, dd = sp.symbols("f_u f_l d", positive=True)
H_before = -(fu + fl) * sp.log(fu + fl); H_after = -((fu - dd) + (fl + dd)) * sp.log((fu - dd) + (fl + dd))
s1_ok = sp.simplify(H_after - H_before) == 0
Elab, Slab = sp.symbols("E_lab S_lab", positive=True)
Ebook_lab = Elab - Elab                                                   # labelled dust: T_c,lab cancelled by -T_c,lab in S
T_lab = sp.diff(Ebook_lab, Elab)                                           # book energy independent of state => zero temperature store
Dd, TR = sp.symbols("D T_R", positive=True)
dS_zero_ent = 0; dS_heat = -Dd / TR
s2_ok = (dS_zero_ent == 0) and bool(sp.ask(sp.Q.negative(dS_heat)))
sA = sp.symbols("s_A", real=True)
s3_ok = sp.simplify((EV_ - sA) + sA - EV_) == 0                           # reshape there and back returns E_V exactly (work)
rho_, Tk, TJ, tau_ = sp.symbols("rho T T_J tau", positive=True)
s_d = rho_ * (sp.Rational(3, 2) * sp.log(Tk) - sp.log(rho_))
Tdot = (TJ - Tk) / tau_
Qkt = sp.Rational(3, 2) * rho_ * (TJ - Tk) / tau_
sdot = sp.diff(s_d, Tk) * Tdot
k6_expr = sp.simplify(sdot - Qkt / TJ - sp.Rational(3, 2) * (rho_ / tau_) * (TJ - Tk) ** 2 / (Tk * TJ))
xq = sp.symbols("x", positive=True)
s4_cool = sp.simplify(sdot.subs(Tk, TJ * (1 + xq)))
s4_ok = (k6_expr == 0) and bool(sp.ask(sp.Q.negative(s4_cool)))
SY["T-S"] = dict(S1=s1_ok, T_lab=str(T_lab), S2=s2_ok, S3=s3_ok, S4=s4_ok, S4_cooling_dSdt=str(s4_cool))
TS_SCT = chk("T-S_SCT_events_need_no_entropy", s1_ok and s2_ok and s3_ok and T_lab == 0,
             f"S1 conversion: total dust H unchanged by relabelling: {s1_ok}; labelled sector's book energy is identically 0 (T_lab = {T_lab}): a "
             f"zero-temperature entropy store; S2 merger draw D: zero-entropy DE dS = 0, heat bath dS = {dS_heat} < 0: {s2_ok}; S3 reshape is "
             f"reversible work: {s3_ok}")
K6 = chk("K6_CFG955_L7_Clausius", s4_ok,
         f"dS_d/dt - Q/T_J - (3/2)(rho/tau)(T_J - T)^2/(T T_J) = {k6_expr}; cooling branch T = T_J(1 + x): dS_d/dt = {s4_cool} < 0, so a zero-entropy "
         f"receiver gives dS_tot < 0 (S4: K-T and the CFG935 bath cannot use a coherent dark energy)")
V2 = "ONLY WHERE NO ENTROPY IS EXCHANGED" if (TS_SCT and s4_ok) else ("YES" if TS_SCT else "NO")
P(f"  V2 (one channel for SCT + CFG935 + CFG955): {V2}  [SCT events and the class-A drift (CFG542 Pb, coherent partner) admissible; "
  f"CFG955 K-T and CFG935's bath need a heat bath]")
RES["V2"] = V2

# T4 structure: IV has no kinetic term; R-phi friction; R-F inertia
Vsym = sp.Symbol("V0", positive=True); dVf = sp.Function("dV")(x0, x1)
T_IV = -(Vsym + dVf) * eta.inv()
has_deriv = any(e_.has(sp.Derivative) for e_ in T_IV)
dVt = sp.Function("dV")(x0)                                                # at a fixed point: d_t dV = S_events, homogeneous part
sol = sp.dsolve(sp.Eq(sp.diff(dVt, x0), 0))                                # dV = const: no wave, no k-dependent frequency
no_wave = not sol.rhs.has(sp.Derivative) and not sol.rhs.has(x0)
tsym, Hs, Qs, kk, ep = sp.symbols("t H Q k epsilon", real=True)
phi0 = sp.Function("phi0")(tsym); dphi = sp.Function("dphi")(tsym); Vp = sp.Function("Vp")
phi = phi0 + ep * dphi
eq = sp.diff(phi, tsym, 2) + 3 * Hs * sp.diff(phi, tsym) + kk ** 2 * ep * dphi + Vp(phi) - Qs / sp.diff(phi, tsym)
lin = sp.expand(sp.series(eq, ep, 0, 2).removeO().coeff(ep, 1))
fric = sp.simplify(lin.coeff(sp.diff(dphi, tsym)))
rphi_ok = sp.simplify(fric - (3 * Hs + Qs / sp.diff(phi0, tsym) ** 2)) == 0
w_, rho0_, vc_, v_, gp_ = sp.symbols("w rho_0 v_c v grad_dp", real=True)
vdot = sp.solve(sp.Eq((1 + w_) * rho0_ * sp.Symbol("vdot"), Qs * (vc_ - (1 + w_) * v_) - gp_), sp.Symbol("vdot"))[0]
coef_vc = sp.simplify(sp.diff(vdot, vc_))
lim_vc = sp.limit(coef_vc.subs({Qs: 1, rho0_: 1}), w_, -1, "+")
SY["T4"] = dict(IV_has_derivative=has_deriv, IV_homog_solution=str(sol), Rphi_friction=str(fric), Rphi_ok=rphi_ok,
                RF_vdot=str(vdot), RF_coef_vc=str(coef_vc), RF_limit_w_to_minus1=str(lim_vc))
P(f"  T4 structure: IV stress has no derivative of V: {not has_deriv}; homogeneous dV evolution {sol} (no propagating mode); "
  f"R-phi perturbation friction = {fric} (sympy, = 3H + Q/phidot^2: {rphi_ok}); R-F dv/dt = {vdot}, d/dv_c = {coef_vc} -> {lim_vc} as w -> -1+")

# ================================================================================================ numerics shared by K and MAIN
P("\n==================== K CONTROLS ====================")
J953 = json.load(open(os.path.join(LANES, "CFG953_source_changing_theory", "cfg953_results.json")))
SEN = {}
k1_dev = 0.0
for foot in FOOTS:
    rows = []
    for i, Mb in enumerate(np.logspace(3, 15, 13)):
        r_ = sen_row(float(Mb), A0[foot]); rows.append(r_)
        ref = J953["S-En"][foot][i]
        for key in ("Erel_over_Wf", "Erel_over_Mcc2", "Erel_over_Mcvf2", "N", "re_over_ron"):
            k1_dev = max(k1_dev, abs(r_[key] / ref[key] - 1))
    SEN[foot] = rows
K1 = chk("K1_CFG953_S-En_reproduced", k1_dev <= 1e-9,
         f"max relative difference over 13 masses x 2 footings x 5 columns = {k1_dev:.2e}; E_rel/(M_c c^2) canonical "
         + ", ".join(f"{r_['Erel_over_Mcc2']:.3e}" for r_ in SEN["canonical"][::4]) + " (M_b 1e3, 1e7, 1e11, 1e15)")
RES["S-En"] = {f: [{k: v for k, v in r_.items()} for r_ in SEN[f]] for f in FOOTS}

k3_dev = 0.0
for z, (m_, lo, hi) in README689.items():
    q = CFG689_TRANSCRIBED["sqrtX_q"][z]
    k3_dev = max(k3_dev, abs(q[2] - m_), abs(q[1] - lo), abs(q[3] - hi))
k3_956 = None
p956k = os.path.join(LANES, "CFG956_a0z_wave_bound", "cfg956_K.json")
if os.path.exists(p956k):
    try:
        b956 = json.load(open(p956k))["checks"]["K4"]["band"]
        k3_956 = max(abs(np.array(b956[z]["q"])[[1, 2, 3]] - np.array(CFG689_TRANSCRIBED["sqrtX_q"][z])[[1, 2, 3]]).max() for z in README689)
    except Exception as ex:                                                    # reported only
        k3_956 = f"unreadable ({type(ex).__name__})"
K3 = chk("K3_CFG689_band_nodes", k3_dev <= 5e-4,
         f"transcribed sqrtX 16/50/84 at z 1.0/1.2/1.5/2.33 vs README/THEORY_CANONICAL: max |diff| {k3_dev:.1e}; vs CFG956's independent K4 "
         f"re-implementation (MC): {k3_956 if isinstance(k3_956, str) or k3_956 is None else f'{k3_956:.1e}'} (reported)")

NG = {}
k4_ok = True; k4_txt = []
for foot in FOOTS:
    a0 = A0[foot]
    for kz in KERN:
        dom = domain_sct(MB_N, a0, kz); law = KERN[kz]
        glaw = law(GN_N, a0); Mph = R_N ** 2 * (glaw - GN_N) / G_SI
        dev = float(np.max(np.abs((GN_N + G_SI * np.minimum(Mph, dom["Mc"] * MSUN) / R_N ** 2) / glaw - 1)))
        NG[f"{foot}|{kz}"] = dict(dom=dom, glaw=glaw, Mph=Mph, dev0=dev)
        ref = {"canonical": 453.9, "alt": 412.9}[foot]
        okk = dev <= 1e-12 and abs(dom["r_e"] / KPC - ref) <= 0.1
        k4_ok = k4_ok and okk; k4_txt.append(f"{foot}/{kz} dev {dev:.1e}, r_e {dom['r_e'] / KPC:.1f} kpc")
K4 = chk("K4_CFG953_NGC3198_law_no_channel", k4_ok, "; ".join(k4_txt))

etaF = 1 - math.exp(-1.0)
k5 = dict(reaction=etaF, rest200=etaF * (2e5 / C_SI) ** 2, rest1000=etaF * (1e6 / C_SI) ** 2)
K5 = chk("K5_sol61_local_reaction_numbers", abs(k5["reaction"] - 0.63212) < 5e-6 and abs(k5["rest200"] / 2.8133e-7 - 1) < 5e-5
         and abs(k5["rest1000"] / 7.0333e-6 - 1) < 5e-5,
         f"eta F at t = tau {k5['reaction']:.5f}; deposited/rest {k5['rest200']:.5e} (200 km/s), {k5['rest1000']:.5e} (1000 km/s)")
K_ALL = K1 and K3 and K4 and K5 and K6
RES["K"] = dict(K1=K1, K3=K3, K4=K4, K5=K5, K6=K6, K_all=K_ALL)
P(f"  K overall (K1, K3-K6; K2 in the main stage): {'PASS' if K_ALL else 'FAIL'}")
if STAGE == "K" and not MUT:
    dump(); sys.exit(0 if K_ALL else 1)


# ================================================================================================ CFG953 N-body toy (verbatim copy)
# cfg953.py lines 505-853, copied verbatim; the only change: log["E"] books LEDGER * E_int (the channel's vacuum energy E_V), and the
# per-sample E_int sums and mechanical energies are returned so that the MUTATE ledgers can be formed from the same run.
TOY_EPS = 0.05; TOY_HS = 0.02
RGT = np.geomspace(1e-3, 400.0, 320)
SHR = np.sqrt(RGT[1:] * RGT[:-1])
GLX32, GLW32 = np.polynomial.legendre.leggauss(32)


def lawT(gn):
    return 0.5 * (gn + np.sqrt(gn * gn + 4.0 * gn))


def enc_frac(rr, d, h):
    d = np.maximum(d, 1e-9); s2 = math.sqrt(2.0) * h
    A = 0.5 * (erf((rr - d) / s2) + erf((rr + d) / s2))
    B = h / (d * math.sqrt(2 * math.pi)) * (np.exp(-(rr - d) ** 2 / (2 * h * h)) - np.exp(-(rr + d) ** 2 / (2 * h * h)))
    return np.clip(A - B, 0.0, 1.0)


def body_profile(Mc, d_own, m_own):
    if Mc <= 0 or len(m_own) == 0:
        z = np.zeros_like(RGT)
        return dict(Ms=z, g=z.copy(), Phi=z.copy(), Mtot=0.0, nonmono=False, deficit=float(Mc), re=0.0)
    Mb = (enc_frac(RGT[:, None], d_own[None, :], TOY_HS) * m_own[None, :]).sum(1)
    gn = Mb / RGT ** 2
    Mph = RGT ** 2 * (lawT(gn) - gn)
    nonmono = bool(np.any(np.diff(Mph) < -1e-12 * max(Mph.max(), 1e-300)))
    Mph = np.maximum.accumulate(Mph)
    Ms = np.minimum(Mph, Mc)
    g = Ms / np.maximum(RGT, TOY_EPS) ** 2
    integ = np.concatenate(([0.0], np.cumsum(0.5 * (g[1:] + g[:-1]) * np.diff(RGT))))
    Phi = -Ms[-1] / RGT[-1] - (integ[-1] - integ)
    j = np.searchsorted(Mph, Mc)
    return dict(Ms=Ms, g=g, Phi=Phi, Mtot=float(Ms[-1]), nonmono=nonmono, deficit=float(Mc - Ms[-1]),
                re=float(RGT[min(j, len(RGT) - 1)]))


def g_at(pr, dd):
    out = np.interp(dd, RGT, pr["g"])
    far = dd > RGT[-1]
    if far.any():
        out = np.where(far, pr["Mtot"] / np.maximum(dd, 1e-300) ** 2, out)
    return out


def phi_at(pr, dd):
    out = np.interp(dd, RGT, pr["Phi"])
    far = dd > RGT[-1]
    if far.any():
        out = np.where(far, -pr["Mtot"] / np.maximum(dd, 1e-300), out)
    return out


def shells(pr):
    dm = np.diff(pr["Ms"]); k = dm > 0
    return SHR[k], dm[k]


def bb_force_on_p(prp, Xp, prq, Xq):
    Dv = Xp - Xq; D = float(np.sqrt(np.sum(Dv * Dv)))
    if D < 1e-12:
        return np.zeros(3)
    s, dm = shells(prp)
    if len(s) == 0 or prq["Mtot"] <= 0:
        return np.zeros(3)
    rho = np.sqrt(np.maximum(D * D + s[:, None] ** 2 + 2 * D * s[:, None] * GLX32[None, :], 1e-30))
    ax = g_at(prq, rho) * (D + s[:, None] * GLX32[None, :]) / rho
    avg = 0.5 * (ax * GLW32[None, :]).sum(1)
    return -(Dv / D) * float(np.sum(dm * avg))


def bb_energy(prp, Xp, prq, Xq):
    Dv = Xp - Xq; D = float(np.sqrt(np.sum(Dv * Dv)))
    s, dm = shells(prp)
    if len(s) == 0 or prq["Mtot"] <= 0:
        return 0.0
    rho = np.sqrt(np.maximum(D * D + s[:, None] ** 2 + 2 * D * s[:, None] * GLX32[None, :], 1e-30))
    return float(np.sum(dm * 0.5 * (phi_at(prq, rho) * GLW32[None, :]).sum(1)))


def self_energy(pr):
    s, dm = shells(pr)
    return 0.5 * float(np.sum(dm * phi_at(pr, s))) if len(s) else 0.0


def sample_plummer(rng, n, M, a, center, vbulk, Mc_own):
    uu = rng.uniform(0, 0.99, n); rr = a / np.sqrt(uu ** (-2.0 / 3.0) - 1.0)
    nv = rng.normal(size=(n, 3)); nv /= np.linalg.norm(nv, axis=1)[:, None]
    x = center[None, :] + rr[:, None] * nv
    Menc = M * rr ** 3 / (rr * rr + a * a) ** 1.5
    vc = np.sqrt(rr * lawT(Menc / rr ** 2))
    v = rng.normal(size=(n, 3)) * (0.5 * vc)[:, None]
    v -= v.mean(0)
    v += vbulk[None, :]
    return x, v, np.full(n, M / n)


def run_toy(which, dt, t_end, glued=False, seed=953, label="", ledger=1.0):
    rng = np.random.default_rng(seed)
    X_ = []; V_ = []; M_ = []; KIND = []; OWN = []
    bodies = []
    conv_sched = []
    if which == "E":
        xa, va, ma = sample_plummer(rng, 200, 1.0, 1.0, np.zeros(3), np.zeros(3), 20.0)
        X_ += list(xa); V_ += list(va); M_ += list(ma); KIND += [0] * 200; OWN += [0] * 200
        xb, vb, mb = sample_plummer(rng, 60, 0.02, 0.1, np.array([0.0, 12.0, 0.0]), np.array([0.6, 0.0, 0.0]), 0.4)
        i0b = len(X_); X_ += list(xb); V_ += list(vb); M_ += list(mb); KIND += [0] * 60; OWN += [1] * 60
        rc = 10.0 * rng.uniform(0, 1, 200) ** (1 / 3); nv = rng.normal(size=(200, 3)); nv /= np.linalg.norm(nv, axis=1)[:, None]
        ic0 = len(X_); X_ += list(rc[:, None] * nv); V_ += [np.zeros(3)] * 200; M_ += [0.1] * 200; KIND += [1] * 200; OWN += [-1] * 200
        perm = rng.permutation(200)
        conv_sched = [(0.5 + 5.0 * (k + 1) / 200.0, ic0 + int(perm[k])) for k in range(200)]
        xs_ = rng.uniform(30, 40, 60); ph = rng.uniform(0, 2 * math.pi, 60); rr_ = np.sqrt(rng.uniform(0, 1, 60))
        is0 = len(X_)
        X_ += [np.array([xs_[k], 3.0 + rr_[k] * math.cos(ph[k]), rr_[k] * math.sin(ph[k])]) for k in range(60)]
        V_ += [np.array([-0.8, 0.0, 0.0])] * 60; M_ += [2.0 / 60] * 60; KIND += [1] * 60; OWN += [-1] * 60
        stream = set(range(is0, is0 + 60))
        bodies = [dict(Mc=0.0, X=np.zeros(3), V=np.zeros(3), S=np.zeros(3), active=False),
                  dict(Mc=0.4, X=np.mean(xb, 0), V=np.array([0.6, 0.0, 0.0]), S=np.zeros(3), active=True)]
    else:
        xa, va, ma = sample_plummer(rng, 150, 1.0, 1.0, np.array([-4.0, 0, 0]), np.zeros(3), 20.0)
        xc, vc, mc = sample_plummer(rng, 150, 1.0, 1.0, np.array([4.0, 0, 0]), np.zeros(3), 20.0)
        X_ += list(xa) + list(xc); V_ += list(va) + list(vc); M_ += list(ma) + list(mc)
        KIND += [0] * 300; OWN += [0] * 150 + [1] * 150; stream = set()
        bodies = [dict(Mc=20.0, X=np.mean(xa, 0), V=np.zeros(3), S=np.zeros(3), active=True),
                  dict(Mc=20.0, X=np.mean(xc, 0), V=np.zeros(3), S=np.zeros(3), active=True)]
    x = np.array(X_, float); v = np.array(V_, float); m = np.array(M_, float); kind = np.array(KIND); own = np.array(OWN)
    nb = len(bodies)
    prof = [None] * nb
    eint = {"conversion": 0.0, "reshape": 0.0, "merge": 0.0}
    log = dict(t=[], P=[], L=[], E=[], Emech=[], Pscale=[], Lscale=[], off=[], Eint=[])
    events = dict(conversions=0, merges=[], nonmono=0, deficit_max=0.0)

    def own_sel(q):
        return (kind == 0) & (own == q) & (m > 0)

    def centroid_b(q):
        s = own_sel(q); w = m[s]
        return (w[:, None] * x[s]).sum(0) / w.sum(), (w[:, None] * v[s]).sum(0) / w.sum()

    def make_prof(q):
        b = bodies[q]
        if glued and b["Mc"] > 0:
            b["X"], b["V"] = centroid_b(q)
        s = own_sel(q)
        pr = body_profile(b["Mc"] if b["active"] else 0.0, np.linalg.norm(x[s] - b["X"], axis=1), m[s])
        events["nonmono"] += int(pr["nonmono"]); events["deficit_max"] = max(events["deficit_max"], abs(pr["deficit"]))
        return pr

    def forces():
        alive = m > 0
        dx = x[:, None, :] - x[None, :, :]
        r2 = (dx * dx).sum(-1) + TOY_EPS ** 2
        inv3 = r2 ** -1.5; np.fill_diagonal(inv3, 0.0)
        acc = -(dx * (m[None, :, None] * inv3[:, :, None])).sum(1)
        Fb = np.zeros((nb, 3))
        for q in range(nb):
            if not bodies[q]["active"] or prof[q]["Mtot"] <= 0:
                continue
            dq = x - bodies[q]["X"]; dd = np.maximum(np.linalg.norm(dq, axis=1), 1e-12)
            aq = -(g_at(prof[q], dd) / dd)[:, None] * dq
            acc += aq
            Fb[q] += -(m[alive, None] * aq[alive]).sum(0)
        for p in range(nb):
            for q in range(p + 1, nb):
                if bodies[p]["active"] and bodies[q]["active"]:
                    F = bb_force_on_p(prof[p], bodies[p]["X"], prof[q], bodies[q]["X"])
                    Fb[p] += F; Fb[q] -= F
        return acc, Fb

    def W_shape():
        Wv = 0.0
        for q in range(nb):
            if not bodies[q]["active"]:
                continue
            al_ = m > 0
            Wv += float(np.sum(m[al_] * phi_at(prof[q], np.linalg.norm(x[al_] - bodies[q]["X"], axis=1))))
            Wv += self_energy(prof[q])
            for p in range(q + 1, nb):
                if bodies[p]["active"]:
                    Wv += bb_energy(prof[p], bodies[p]["X"], prof[q], bodies[q]["X"])
        return Wv

    def W_full():
        al_ = m > 0
        xa_ = x[al_]; ma_ = m[al_]
        dx = xa_[:, None, :] - xa_[None, :, :]
        r_ = np.sqrt((dx * dx).sum(-1) + TOY_EPS ** 2); np.fill_diagonal(r_, np.inf)
        return -0.5 * float(np.sum(ma_[:, None] * ma_[None, :] / r_)) + W_shape()

    def kin():
        return 0.5 * float(np.sum(m * (v * v).sum(1))) + sum(0.5 * b["Mc"] * float(np.sum(b["V"] * b["V"])) for b in bodies if b["active"])

    def momenta():
        P_ = (m[:, None] * v).sum(0); L_ = (m[:, None] * np.cross(x, v)).sum(0)
        Ps = float(np.sum(m * np.linalg.norm(v, axis=1))); Ls = float(np.sum(m * np.linalg.norm(np.cross(x, v), axis=1)))
        for b in bodies:
            if b["active"]:
                P_ = P_ + b["Mc"] * b["V"]; Ps += b["Mc"] * float(np.linalg.norm(b["V"]))
                if not glued:
                    L_ = L_ + b["Mc"] * np.cross(b["X"], b["V"]) + b["S"]
                    Ls += b["Mc"] * float(np.linalg.norm(np.cross(b["X"], b["V"]))) + float(np.linalg.norm(b["S"]))
                else:
                    L_ = L_ + b["Mc"] * np.cross(b["X"], b["V"])
        return P_, L_, Ps, Ls

    def convert(i, q):
        b = bodies[q]
        W0 = W_full(); K0 = kin()
        mi, xi, vi = m[i], x[i].copy(), v[i].copy()
        if not glued:
            if not b["active"]:
                b.update(Mc=mi, X=xi.copy(), V=vi.copy(), S=np.zeros(3), active=True)
            else:
                Mn = b["Mc"] + mi
                Xn = (b["Mc"] * b["X"] + mi * xi) / Mn; Vn = (b["Mc"] * b["V"] + mi * vi) / Mn
                b["S"] = b["S"] + b["Mc"] * np.cross(b["X"] - Xn, b["V"] - Vn) + mi * np.cross(xi - Xn, vi - Vn)
                b.update(Mc=Mn, X=Xn, V=Vn)
        else:
            b["Mc"] += mi; b["active"] = True
        m[i] = 0.0; v[i] = 0.0; kind[i] = -1
        prof[q] = make_prof(q)
        W1 = W_full(); K1_ = kin()
        if not glued:
            eint["conversion"] += (K0 - K1_) - (W1 - W0)
        events["conversions"] += 1

    def merge(p, q):
        bp, bq = bodies[p], bodies[q]
        W0 = W_full(); K0 = kin()
        Xb_p = centroid_b(p)[0]; Xb_q = centroid_b(q)[0]
        g_before = None
        Mn = bp["Mc"] + bq["Mc"]
        if not glued:
            Xn = (bp["Mc"] * bp["X"] + bq["Mc"] * bq["X"]) / Mn; Vn = (bp["Mc"] * bp["V"] + bq["Mc"] * bq["V"]) / Mn
            Sn = bp["S"] + bq["S"] + bp["Mc"] * np.cross(bp["X"] - Xn, bp["V"] - Vn) + bq["Mc"] * np.cross(bq["X"] - Xn, bq["V"] - Vn)
            Mb5 = float(np.sum(m[(kind == 0) & (m > 0) & (np.linalg.norm(x - Xn, axis=1) < 5.0)]))
            g_before = (Mb5 + float(np.interp(5.0, RGT, prof[p]["Ms"])) + float(np.interp(5.0, RGT, prof[q]["Ms"]))) / 25.0
            bq.update(Mc=Mn, X=Xn, V=Vn, S=Sn)
        else:
            bq["Mc"] = Mn
        own[(own == p)] = q
        bp.update(active=False, Mc=0.0)
        prof[p] = body_profile(0.0, np.zeros(0), np.zeros(0)); prof[q] = make_prof(q)
        W1 = W_full(); K1_ = kin()
        g_after = None
        if g_before is not None:
            Mb5 = float(np.sum(m[(kind == 0) & (m > 0) & (np.linalg.norm(x - bq["X"], axis=1) < 5.0)]))
            g_after = (Mb5 + float(np.interp(5.0, RGT, prof[q]["Ms"]))) / 25.0
        dE = (K0 - K1_) - (W1 - W0)
        if not glued:
            eint["merge"] += dE
        events["merges"].append(dict(p=p, q=q, sep_b=float(np.linalg.norm(Xb_p - Xb_q)), dEint=dE, Kloss=K0 - K1_, dW=W1 - W0,
                                     g5_before=g_before, g5_after=g_after))

    def bound_fraction(q):
        s = own_sel(q); idx = np.where(s)[0]
        if len(idx) == 0:
            return 0.0
        xs_ = x[idx]; ms_ = m[idx]
        dx = xs_[:, None, :] - xs_[None, :, :]
        r_ = np.sqrt((dx * dx).sum(-1) + TOY_EPS ** 2); np.fill_diagonal(r_, np.inf)
        phi = -(ms_[None, :] / r_).sum(1) + phi_at(prof[q], np.linalg.norm(xs_ - bodies[q]["X"], axis=1))
        Vq = bodies[q]["V"] if not glued else centroid_b(q)[1]
        e = 0.5 * ((v[idx] - Vq) ** 2).sum(1) + phi
        return float(np.mean(e < 0))

    for q in range(nb):
        prof[q] = make_prof(q)
    acc, Fb = forces()
    nsteps = int(round(t_end / dt)); sched_k = 0; t = 0.0
    E0 = None
    for step in range(nsteps + 1):
        if step % 20 == 0:
            P_, L_, Ps, Ls = momenta(); Wm = W_full(); Km = kin(); Ei = sum(eint.values())
            if E0 is None:
                E0 = Km + Wm
            log["t"].append(t); log["P"].append(P_.tolist()); log["L"].append(L_.tolist())
            log["E"].append(Km + Wm + ledger * Ei); log["Emech"].append(Km + Wm); log["Pscale"].append(Ps); log["Lscale"].append(Ls)
            log["Eint"].append(dict(eint))
            offs = []
            for q in range(nb):
                if bodies[q]["active"] and own_sel(q).any():
                    offs.append(float(np.linalg.norm(centroid_b(q)[0] - bodies[q]["X"])))
                else:
                    offs.append(float("nan"))
            log["off"].append(offs)
        if step == nsteps:
            break
        if step % 1000 == 0:
            rss_guard(f"toy {label} step {step}")
        v += 0.5 * dt * acc
        for q in range(nb):
            if bodies[q]["active"] and bodies[q]["Mc"] > 0 and not glued:
                bodies[q]["V"] = bodies[q]["V"] + 0.5 * dt * Fb[q] / bodies[q]["Mc"]
        x += dt * v
        for q in range(nb):
            if bodies[q]["active"] and not glued:
                bodies[q]["X"] = bodies[q]["X"] + dt * bodies[q]["V"]
        t += dt
        Wa = W_shape()
        for q in range(nb):
            prof[q] = make_prof(q)
        Wb = W_shape()
        if not glued:
            eint["reshape"] -= (Wb - Wa)
        while sched_k < len(conv_sched) and conv_sched[sched_k][0] <= t + 1e-12:
            convert(conv_sched[sched_k][1], 0); sched_k += 1
        if which == "E" and bodies[0]["active"]:
            for i in list(stream):
                if m[i] > 0 and np.linalg.norm(x[i] - bodies[0]["X"]) < 25.0:
                    convert(i, 0); stream.discard(i)
            if bodies[1]["active"] and step % 200 == 0:
                bf = bound_fraction(1)
                sep = np.linalg.norm(centroid_b(1)[0] - centroid_b(0)[0])
                if bf < 0.5 or sep <= 1.305:
                    merge(1, 0)
        if which == "M" and bodies[1]["active"]:
            if np.linalg.norm(centroid_b(1)[0] - centroid_b(0)[0]) <= 1.305:
                merge(1, 0)
        acc, Fb = forces()
        v += 0.5 * dt * acc
        for q in range(nb):
            if bodies[q]["active"] and bodies[q]["Mc"] > 0 and not glued:
                bodies[q]["V"] = bodies[q]["V"] + 0.5 * dt * Fb[q] / bodies[q]["Mc"]
        if glued:
            for q in range(nb):
                if bodies[q]["active"]:
                    bodies[q]["X"], bodies[q]["V"] = centroid_b(q)
    Pa = np.array(log["P"]); La = np.array(log["L"]); Ea = np.array(log["E"]); Em = np.array(log["Emech"])
    Psc = max(log["Pscale"]); Lsc = max(log["Lscale"])
    Esum = np.array([sum(e_.values()) for e_ in log["Eint"]])
    res = dict(which=which, dt=dt, t_end=t_end, glued=glued, ledger=ledger,
               dP=float(np.max(np.linalg.norm(Pa - Pa[0], axis=1)) / Psc), dL=float(np.max(np.linalg.norm(La - La[0], axis=1)) / Lsc),
               dE=float(np.max(np.abs(Ea - Ea[0])) / abs(E0)), dEmech=float(np.max(np.abs(Em - Em[0])) / abs(E0)),
               dE_wrong=float(np.max(np.abs((Em - Esum) - (Em[0] - Esum[0]))) / abs(E0)),
               E0=float(E0), Pscale=Psc, Lscale=Lsc, eint_final=dict(eint),
               eint_over_E0={k: v_ / abs(E0) for k, v_ in eint.items()}, n_conversions=events["conversions"], n_merges=len(events["merges"]),
               off_final=[float(log["off"][-1][q]) for q in range(nb)])
    return res


def toy_line(tr, name):
    P(f"     {name} (ledger {tr['ledger']:+.0f}): dP/P_scale {tr['dP']:.2e}, dL/L_scale {tr['dL']:.2e}, |dE_booked|/|E0| {tr['dE']:.3e}, "
      f"|dE_mech|/|E0| {tr['dEmech']:.3e}, wrong-sign ledger {tr['dE_wrong']:.3e} (E0 {tr['E0']:.3f}); E_int/|E0|: "
      + ", ".join(f"{k} {v:+.5f}" for k, v in tr["eint_over_E0"].items()) + f"; conversions {tr['n_conversions']}, merges {tr['n_merges']}")


# ================================================================================================ physical helpers
def sigma_pt(r, M, Mc, a0, h=1e-4):
    """point-mass body density sigma = dM_sigma/dV, M_sigma = min(Mph_pt, M_c) (CFG953 R3 with point baryons)."""
    f = lambda rr: min(Mph_pt(rr, M, a0, "simple"), Mc)
    return (f(r * (1 + h)) - f(r * (1 - h))) / (2 * r * h) / (4 * math.pi * r * r)


def Msig_pt(r, M, Mc, a0):
    return min(Mph_pt(r, M, a0, "simple"), Mc)


def law_dex_shift(gN, a0, frac):
    return float(np.log10(law_simple(gN, a0 * math.sqrt(1 + frac)) / law_simple(gN, a0)))


def class_rows(a0):
    rows = []
    for name, Mb, rh in CLASSES:
        s_ = sen_row(Mb, a0); M = Mb * MSUN; Mc = s_["Mc_kg"]; re = s_["r_e"]; r = rh * KPC
        Vol = 4 * math.pi / 3 * re ** 3
        sg = sigma_pt(r, M, Mc, a0) if r < re else 0.0
        dV_sig = s_["Erel"] * sg / Mc; dV_U = s_["Erel"] / Vol
        draw = MERGE_FRAC * s_["absWf"]
        rows.append(dict(name=name, Mb=Mb, r_half_kpc=rh, eps=s_["Erel_over_Mcc2"], r_e_kpc=re / KPC, N=s_["N"],
                         dV_sigma_over_V=dV_sig / VBAR, dV_U_over_V=dV_U / VBAR,
                         draw_sigma_over_V=draw * sg / Mc / VBAR, draw_U_over_V=draw / Vol / VBAR,
                         C_U=VBAR * Vol / s_["Erel"], C_sigma_rhalf=(VBAR / dV_sig) if dV_sig > 0 else float("inf"),
                         rho_body_mean_over_rhoDE=(Mc / Vol) / RHO_DE0, Erel=s_["Erel"], absWf=s_["absWf"], Mc_kg=Mc, r_e=re))
    return rows


def ngc_deposit(foot, kz="simple"):
    a0 = A0[foot]; s_ = sen_row(MB_N, a0); ng = NG[f"{foot}|{kz}"]
    Mc = ng["dom"]["Mc"] * MSUN; re = ng["dom"]["r_e"]; Mph = ng["Mph"]
    sig = np.gradient(Mph, R_N) / (4 * math.pi * R_N ** 2)
    E = s_["Erel"]
    return dict(E=E, eps=E / (Mc * C_SI ** 2), Mc=Mc, re=re, sig=sig, Mph=Mph, absWf=s_["absWf"],
                dV={"P-sigma": E * sig / Mc, "P-U": np.full_like(R_N, E / (4 * math.pi / 3 * re ** 3))},
                dM={"P-sigma": (E / C_SI ** 2) * Mph / Mc, "P-U": (E / C_SI ** 2) * (R_N / re) ** 3})


# ================================================================================================ MUTATE
if MUT:
    P("\n==================== MUTATE ====================")
    MU = {}
    P("  MU1 / MU2: CFG953 toys with the exchange OFF (no E_V booking); the wrong-sign ledger is formed from the same run")
    tE = run_toy("E", 2e-3, 40.0, label="E off", ledger=0.0); toy_line(tE, "run E, exchange off")
    tM = run_toy("M", 2e-3, 30.0, label="M off", ledger=0.0); toy_line(tM, "run M, exchange off")
    on_res = {"E": 1.4737217698205474e-4, "M": 2.4611852597853685e-5}       # CFG953 E_int-booked residuals (= channel-on, T1e)
    mu1 = tE["dE"] >= 0.2 and tM["dE"] >= 0.2
    mu2 = tE["dE_wrong"] >= 100 * on_res["E"] and tM["dE_wrong"] >= 100 * on_res["M"]
    MU["MU1"] = dict(bites=mu1, E=tE["dE"], M=tM["dE"])
    MU["MU2"] = dict(bites=mu2, E=tE["dE_wrong"], M=tM["dE_wrong"], on_residual=on_res)
    P(f"  MU1 exchange off: |dE|/|E0| E {tE['dE']:.3f}, M {tM['dE']:.3f} (line >= 0.2; CFG953 Mu5 0.249 / 0.217) -> {'BITES' if mu1 else 'does not bite'}")
    P(f"  MU2 wrong sign: |dE|/|E0| E {tE['dE_wrong']:.3f}, M {tM['dE_wrong']:.3f} vs 100 x on-residual {100 * on_res['E']:.4f} / "
      f"{100 * on_res['M']:.4f} -> {'BITES' if mu2 else 'does not bite'} (conservation broken)")
    # MU3: R-phi anti-friction on the draw / wrong-sign branch (A1 item 1)
    mu3 = {}
    for foot in FOOTS:
        a0 = A0[foot]; dep = ngc_deposit(foot)
        cl = [r_ for r_ in class_rows(a0) if r_["name"] == "cluster"][0]
        Qs_ = {"NGC 3198": {"P-sigma": float(np.max(dep["dV"]["P-sigma"])) / GYR, "P-U": float(dep["dV"]["P-U"][0]) / GYR},
               "cluster": {"P-sigma": cl["dV_sigma_over_V"] * VBAR / GYR, "P-U": cl["dV_U_over_V"] * VBAR / GYR}}
        for cls, d_ in Qs_.items():
            for opw in (0.01, 0.1):
                rates = {pf: q_ / (opw * VBAR) - 3 * H0_SI for pf, q_ in d_.items()}
                mu3[f"{foot}|{cls}|1+w={opw}"] = dict(rates_over_H0={pf: r_ / H0_SI for pf, r_ in rates.items()},
                                                      unstable_any=any(r_ > H0_SI for r_ in rates.values()))
    mu3_bite = all(v_["unstable_any"] for v_ in mu3.values())
    MU["MU3"] = dict(bites=mu3_bite, cases=mu3)
    for k_, v_ in mu3.items():
        P(f"    MU3 {k_:28s}: (|Q|/((1+w)Vbar) - 3H0)/H0 = " + ", ".join(f"{pf} {r_:+.3e}" for pf, r_ in v_["rates_over_H0"].items())
          + f"  -> {'UNSTABLE' if v_['unstable_any'] else 'stable'}")
    P(f"  MU3 (literal: all four (class, 1+w) cases unstable for at least one profile, both footings): {'BITES' if mu3_bite else 'does NOT bite'}")
    # MU4: reaction not held (A1 item 3)
    mu4 = {}
    for foot in FOOTS:
        dep = ngc_deposit(foot); glaw = NG[f"{foot}|simple"]["glaw"]
        gradV = np.abs(np.gradient(dep["dV"]["P-sigma"], R_N))
        ratio = gradV / (np.maximum(dep["sig"], 1e-300) * glaw)
        mu4[foot] = dict(median=float(np.median(ratio)), min=float(np.min(ratio)), max=float(np.max(ratio)))
    mu4_bite = all(v_["median"] >= 0.1 for v_ in mu4.values())
    MU["MU4"] = dict(bites=mu4_bite, ratio=mu4)
    P("  MU4 reaction NOT held (P-sigma, NGC 3198): |grad dV|/(sigma g_law) median " + ", ".join(f"{f} {v_['median']:.3f} [{v_['min']:.3f}, {v_['max']:.3f}]"
                                                                                           for f, v_ in mu4.items())
      + f" (line >= 0.1) -> {'BITES' if mu4_bite else 'does not bite'} (the sol61 O(1) reaction returns)")
    # reported: IV wrong sign effect on stability / ordering; shared reaction on satellites
    rep = {}
    for foot in FOOTS:
        a0 = A0[foot]; cr = class_rows(a0)
        rep[foot] = dict(IV_wrong_sign_stability="no degree of freedom: unchanged (no tooth)",
                         IV_wrong_sign_ordering_minC=min(r_["C_U"] for r_ in cr),
                         IV_wrong_sign_cosmic_sign="Delta rho_DE < 0, a0(z)/a0(0) - 1 > 0 (sign flips; magnitude unchanged)")
        dh = sen_row(HOST, a0); Mh = HOST * MSUN; Mch = dh["Mc_kg"]
        sh = []
        for (nm, Ms_, apc) in HOSTS882:
            for D in RHOST:
                r = D * KPC; h = 1e-3
                dVh = lambda rr: dh["Erel"] * sigma_pt(rr, Mh, Mch, a0) / Mch
                grad = abs(dVh(r * (1 + h)) - dVh(r * (1 - h))) / (2 * r * h)
                ss = sen_row(Ms_, a0); sig_s = ss["Mc_kg"] / (4 * math.pi / 3 * ss["r_e"] ** 3)
                gh = G_SI * Mh / r ** 2 + G_SI * Msig_pt(r, Mh, Mch, a0) / r ** 2      # host field: baryons + body
                sh.append(dict(sat=nm, D_kpc=D, a_over_ghost=grad / sig_s / gh))
        rep[foot]["shared_reaction_satellites"] = sh
        P(f"  reported ({foot}): IV wrong sign -> stability unchanged (no DOF), min capacity C_U {rep[foot]['IV_wrong_sign_ordering_minC']:.2e} "
          f"(ordering unchanged); shared reaction: a_sat/g_host " + ", ".join(f"{d_['sat']}@{d_['D_kpc']:.0f} {d_['a_over_ghost']:.2e}" for d_ in sh))
    MU["reported"] = rep
    RES["MUTATE"] = MU
    allbite = mu1 and mu2 and mu3_bite and mu4_bite
    P(f"\n  MUTATE: MU1 {'bites' if mu1 else 'NO'}, MU2 {'bites' if mu2 else 'NO'}, MU3 {'bites' if mu3_bite else 'NO'}, MU4 {'bites' if mu4_bite else 'NO'}"
      f" -> exit {1 if allbite else 2}")
    dump(); sys.exit(1 if allbite else 2)


# ================================================================================================ MAIN
P("\n==================== MAIN ====================")
# ---- T1e + K2: the toy with E_V booked
P("  T1e / K2: CFG953 toys with the vacuum ledger E_V (= CFG953's E_int increments)")
tE = run_toy("E", 2e-3, 40.0, label="E", ledger=1.0); toy_line(tE, "run E, dt 2e-3")
rss_guard("toy E")
tM = run_toy("M", 2e-3, 30.0, label="M", ledger=1.0); toy_line(tM, "run M, dt 2e-3")
rss_guard("toy M")
r953 = J953["e"]
k2_dev = max(abs(tE["eint_over_E0"][k] - r953["toyE1"]["eint_over_E0"][k]) for k in tE["eint_over_E0"])
k2_dev = max(k2_dev, max(abs(tM["eint_over_E0"][k] - r953["toyM"]["eint_over_E0"][k]) for k in tM["eint_over_E0"]))
for key in ("dE", "dEmech"):
    k2_dev = max(k2_dev, abs(tE[key] - r953["toyE1"][key]), abs(tM[key] - r953["toyM"][key]))
K2 = chk("K2_CFG953_toy_E_int_reproduced", k2_dev <= 1e-9, f"max |difference| in units of |E0| = {k2_dev:.2e} (conversion "
         f"{tE['eint_over_E0']['conversion']:+.5f}, merge {tM['eint_over_E0']['merge']:+.5f})")
t1e = (tE["dE"] <= 1e-3 and tM["dE"] <= 1e-3 and abs(tE["dE"] - r953["toyE1"]["dE"]) <= 1e-9 and abs(tM["dE"] - r953["toyM"]["dE"]) <= 1e-9
       and max(tE["dP"], tE["dL"], tM["dP"], tM["dL"]) <= 1e-13)
SY["T1e"] = chk("T1e_toy_total_energy_with_vacuum_ledger", t1e,
                f"|d(K + W + E_V)|/|E0| E {tE['dE']:.3e}, M {tM['dE']:.3e} (line 1e-3; equal to CFG953's E_int-booked residual); dP, dL <= "
                f"{max(tE['dP'], tE['dL'], tM['dP'], tM['dL']):.1e}; without the ledger |dE_mech|/|E0| {tE['dEmech']:.3f} / {tM['dEmech']:.3f}")
RES["toys"] = dict(E=tE, M=tM)
T1 = all(SY[k] for k in ("T1a", "T1b", "T1c", "T1d", "T1e"))
P(f"  T1 exchange: {'PASS' if T1 else 'FAIL'}.  Locality: Q^nu = -grad^nu V is a pointwise identity; WHERE V changes is a non-local, "
  f"retarded functional of each body (CH-L) or of the whole cosmic volume (CH-G): the channel is non-local, as SCT's source is")

# ---- T2a cosmic
P("\n  T2a cosmic size (hard ceiling; CFG689 primary band)")
T2A = {}; t2a_ok = True
for foot in FOOTS:
    eps_max = max(r_["Erel_over_Mcc2"] for r_ in SEN[foot])
    ceil0 = eps_max * OMC / omega_DE(0.0)
    rows = {}
    for z in ("1.0", "1.2", "1.5", "2.33"):
        zf = float(z); ceil = eps_max * OMC * (1 + zf) ** 3 / omega_DE(zf)
        bound = 0.5 * max(ceil, ceil0)
        q = CFG689_TRANSCRIBED["sqrtX_q"][z]; hw = 0.5 * (q[3] - q[1])
        ok = bound < 0.1 * hw; t2a_ok = t2a_ok and ok
        rows[z] = dict(ceiling_drho=ceil, dlna0_bound=bound, half_width68=hw, ratio=bound / hw, ok=ok)
        P(f"    {foot:9s} z {z:4s}: ceiling drho/rho {ceil:.2e}; |d ln a0(z) - d ln a0(0)| <= {bound:.2e} vs 0.1 x half-width "
          f"{0.1 * hw:.3f} (ratio to half-width {bound / hw:.1e}) -> {'PASS' if ok else 'FAIL'}")
    # native PM-anchored bracket (reported)
    lgM = np.log10([r_["Mb"] for r_ in SEN[foot]]); lge = np.log10([r_["Erel_over_Mcc2"] for r_ in SEN[foot]])
    Mb_res = fret_of(math.log10(M_RES_H)) * FB * M_RES_H / HE
    eps_res = 10 ** float(np.interp(math.log10(Mb_res), lgM, lge)); eps_cl = 10 ** float(np.interp(14.0, lgM, lge))
    nat = {str(z): [FSW[foot][z] * OMC * (1 + z) ** 3 / omega_DE(z) * e_ for e_ in (eps_res, eps_cl)] for z in (0.0, 0.5, 1.0)}
    P(f"    {foot:9s} native PM-anchored (CFG424 switch-on fraction x S-En eps at M_b {Mb_res:.2e} .. 1e14): drho/rho at z 0 / 0.5 / 1 = "
      + "; ".join(f"[{v_[0]:.1e}, {v_[1]:.1e}]" for v_ in nat.values()))
    T2A[foot] = dict(eps_max=eps_max, ceil0=ceil0, nodes=rows, native_bracket=nat, Mb_res=Mb_res, eps_res=eps_res, eps_cluster=eps_cl)
# CFG630 native-anchored ledger, rescaled by SCT's E_rel/(M_c V_f^2) over CFG630's c_W
J630 = json.load(open(os.path.join(LANES, "CFG630_settling_feeds_dark_energy", "cfg630_results.json")))["native_anchored"]
rs630 = {}
for foot, fk in (("canonical", "can"), ("alt", "alt")):
    s_mw = sen_row(6e10, A0[foot])["Erel_over_Mcvf2"]; s_cl = sen_row(1e14, A0[foot])["Erel_over_Mcvf2"]
    sc = [s_mw / CW630[foot]["MW"], s_cl / CW630[foot]["cluster"]]
    lo = J630[f"{fk}|alpha0.5"]; hi = J630[f"{fk}|alpha1.186"]
    rs630[foot] = dict(scale=sc, drho_z1=[lo["drho_over_rho0"]["1.0"] * min(sc), hi["drho_over_rho0"]["1.0"] * max(sc)],
                       a0ratm1={z: [hi["a0_ratio_minus_1"][z] * max(sc), lo["a0_ratio_minus_1"][z] * min(sc)] for z in ("1.0", "2.0", "3.0")})
    P(f"    {foot:9s} CFG630 native-anchored ledger x SCT/c_W ({sc[0]:.3f}, {sc[1]:.3f}): drho/rho0 since z = 1 in "
      f"[{rs630[foot]['drho_z1'][0]:.2e}, {rs630[foot]['drho_z1'][1]:.2e}]; a0(z)/a0(0) - 1 at z 1/2/3: "
      + ", ".join(f"[{v_[0]:.1e}, {v_[1]:.1e}]" for v_ in rs630[foot]["a0ratm1"].values()))
# CFG956 (read only; uncommitted at run time if so)
c956 = None
p956 = os.path.join(LANES, "CFG956_a0z_wave_bound", "cfg956.json")
if os.path.exists(p956):
    try:
        J956 = json.load(open(p956))
        c956 = {br: dict(eps95_min=J956[f"summary_{br}"]["eps95_min"], P_at_min=J956[f"summary_{br}"]["P_at_eps95_min"],
                         eps95_max=J956[f"summary_{br}"]["eps95_max"]) for br in ("S", "C")}
        P(f"    CFG956 wave bound (read from its cfg956.json as found at run time): 95% amplitude bound eps95 in "
          + "; ".join(f"branch {br} [{v_['eps95_min']:.4f} (P {v_['P_at_min']}), {v_['eps95_max']:.4f}]" for br, v_ in c956.items())
          + f"; the channel's monotone shift is <= {max(max(r_['dlna0_bound'] for r_ in T2A[f]['nodes'].values()) for f in FOOTS):.1e}")
    except Exception as ex:
        c956 = f"unreadable ({type(ex).__name__})"; P(f"    CFG956 cfg956.json unreadable: {c956}")
else:
    P("    CFG956 result not found at run time")
RES["T2a"] = dict(per_footing=T2A, cfg630_rescaled=rs630, cfg956=c956,
                  sign="formation releases (S-En > 0 for every M_b): rho_DE grows toward today, a0(z)/a0(0) - 1 < 0 (phantom-side, as CFG630)")
SY["T2a"] = chk("T2a_cosmic_within_CFG689_band", t2a_ok, "hard ceiling below 0.1 x the CFG689 68% half-width at every node, both footings")

# ---- T2b local
P("\n  T2b local size: NGC 3198 (43 radii), slip, EFE, Cassini, headroom; CH-L P-sigma / P-U, CH-G; a0-cos / a0-loc")
T2B = {}; NGCROWS = {}
for foot in FOOTS:
    a0 = A0[foot]
    for kz in KERN:
        dep = ngc_deposit(foot, kz); law = KERN[kz]; glaw = NG[f"{foot}|{kz}"]["glaw"]; Mph = dep["Mph"]
        for prof in ("P-sigma", "P-U"):
            dV = dep["dV"][prof]; dM = dep["dM"][prof]
            dev_cos = float(np.max(np.abs((GN_N + G_SI * (Mph + dM) / R_N ** 2) / glaw - 1)))
            a0r = a0 * np.sqrt(1 + dV / VBAR)
            Mloc = R_N ** 2 * (law(GN_N, a0r) - GN_N) / G_SI
            dev_loc = float(np.max(np.abs((GN_N + G_SI * (Mloc + dM) / R_N ** 2) / glaw - 1)))
            draw = MERGE_FRAC * dep["absWf"] * (dep["sig"] / dep["Mc"] if prof == "P-sigma" else np.full_like(R_N, 1.0 / (4 * math.pi / 3 * dep["re"] ** 3)))
            NGCROWS[f"{foot}|{kz}|CH-L {prof}"] = dict(eps=dep["eps"], E_int=dep["E"], dV_over_V_max=float(np.max(dV / VBAR)),
                                                        dV_over_V_min=float(np.min(dV / VBAR)), dev_cos=dev_cos, dev_loc=dev_loc,
                                                        headroom_min=float(np.min(1 - draw / VBAR)))
        for tP in (1.0, 10.0):
            Pw = dep["E"] / (tP * GYR)
            dMt = 2 * Pw * R_N / C_SI ** 3
            dev_g = float(np.max(np.abs((GN_N + G_SI * (Mph + dMt) / R_N ** 2) / glaw - 1)))
            u_tr = Pw / (4 * math.pi * R_N ** 2 * C_SI)
            s_tr = float(np.max(u_tr / (np.maximum(dep["sig"], 1e-300) * C_SI ** 2)))
            NGCROWS[f"{foot}|{kz}|CH-G tP={tP:g}"] = dict(dev_cos=dev_g, dev_loc=dev_g, slip_transit=s_tr, headroom_min=1.0)
for k_, v_ in NGCROWS.items():
    P(f"    {k_:34s}: " + (f"eps {v_['eps']:.3e}, dV/Vbar [{v_['dV_over_V_min']:.2e}, {v_['dV_over_V_max']:.2e}], " if "eps" in v_ else
                           f"transit slip {v_['slip_transit']:.1e}, ")
      + f"max |g/g_law - 1|: a0-cos {v_['dev_cos']:.2e}, a0-loc {v_['dev_loc']:.2e}; headroom min (Vbar - draw)/Vbar {v_['headroom_min']:.4f}")
# EFE (a0-loc) and Cassini, from the 6e10 host's lump
EFE = {}; CAS = {}
for foot in FOOTS:
    a0 = A0[foot]; dh = sen_row(HOST, a0); Mh = HOST * MSUN; Mch = dh["Mc_kg"]; reh = dh["r_e"]; Volh = 4 * math.pi / 3 * reh ** 3
    for prof in ("P-sigma", "P-U"):
        dVh = (lambda rr: dh["Erel"] * sigma_pt(rr, Mh, Mch, a0) / Mch) if prof == "P-sigma" else (lambda rr: dh["Erel"] / Volh if rr < reh else 0.0)
        dMh = (lambda rr: dh["Erel"] / C_SI ** 2 * Msig_pt(rr, Mh, Mch, a0) / Mch) if prof == "P-sigma" else \
              (lambda rr: dh["Erel"] / C_SI ** 2 * min(rr / reh, 1.0) ** 3)
        efe = []
        for (nm, Ms_, apc) in HOSTS882:
            for D in RHOST:
                frac = dVh(D * KPC) / VBAR
                gN = G_SI * Ms_ * MSUN / 2 ** 1.5 / (apc * PC) ** 2
                efe.append(dict(sat=nm, D_kpc=D, dV_over_V=frac, dex=law_dex_shift(gN, a0, frac)))
        EFE[f"{foot}|{prof}"] = efe
        R8 = 8.0 * KPC; dM8 = dMh(R8); drho8 = dVh(R8) / C_SI ** 2
        tid = max(abs(-2 * G_SI * dM8 / R8 ** 3 + 8 * math.pi / 3 * G_SI * drho8), abs(G_SI * dM8 / R8 ** 3 - 4 * math.pi / 3 * G_SI * drho8))
        da = math.sqrt(1 + dVh(R8) / VBAR) - 1
        CAS[f"{foot}|{prof}"] = dict(tidal=tid, tidal_over_ceiling=tid / Q2_CEIL, da0_over_a0_sun=da, Q2_scaled=Q2_770 * (1 + da) ** 3)
        P(f"    {foot:9s} {prof:7s}: EFE (a0-loc) max |dlog g| {max(abs(e_['dex']) for e_ in efe):.2e} dex (line {DELTA_C}); Cassini lump tidal "
          f"{tid:.2e} s^-2 ({tid / Q2_CEIL:.1e} of ceiling); a0-loc at the Sun da0/a0 {da:.2e} -> CFG770 |Q2|/ceiling {Q2_770 * (1 + da) ** 3:.2e}")
# grade T2b per (variant, reading); simple kernel graded, both footings
VARS = ["CH-L P-sigma", "CH-L P-U", "CH-G"]
T2B_GRADE = {}
for var in VARS:
    for rd in ("a0-cos", "a0-loc"):
        ok = True; why = []
        for foot in FOOTS:
            keys = [k_ for k_ in NGCROWS if k_.startswith(f"{foot}|simple|{var}")]
            for k_ in keys:
                v_ = NGCROWS[k_]
                dv = v_["dev_cos"] if rd == "a0-cos" else v_["dev_loc"]
                if dv >= 1e-6: ok = False; why.append(f"{k_} NGC 3198 {dv:.1e}")
                if rd == "a0-loc" and v_["headroom_min"] <= 0: ok = False; why.append(f"{k_} headroom {v_['headroom_min']:.2f}")
                s_tot = SLIP953 + v_.get("slip_transit", 0.0)
                if s_tot > SLIP_LINE: ok = False; why.append(f"{k_} slip {s_tot:.2e}")
            if var.startswith("CH-L"):
                prof = var.split()[1]
                if rd == "a0-loc" and max(abs(e_["dex"]) for e_ in EFE[f"{foot}|{prof}"]) > DELTA_C: ok = False; why.append("EFE")
                c_ = CAS[f"{foot}|{prof}"]
                if c_["tidal"] > Q2_CEIL or (rd == "a0-loc" and c_["Q2_scaled"] >= 1): ok = False; why.append("Cassini")
        T2B_GRADE[f"{var}|{rd}"] = dict(ok=ok, why=why)
        P(f"    T2b {var:13s} {rd}: {'PASS' if ok else 'FAIL'}" + (f"  ({'; '.join(why[:4])})" if why else ""))
RES["T2b"] = dict(rows=NGCROWS, EFE=EFE, Cassini=CAS, grade=T2B_GRADE, slip="CH-L composite stress = 0 (T1d): slip = CFG953's 1.3548e-5")

# ---- T3 sign and ordering
P("\n  T3 sign and ordering: capacity C = Vbar (4pi/3) r_e^3 / E_rel per class (the analogue of CFG930's E_SN/dE)")
T3 = {}; t3_ok = True
for foot in FOOTS:
    cr = class_rows(A0[foot]); T3[foot] = cr
    minC = min(r_["C_U"] for r_ in cr); t3_ok = t3_ok and minC >= 10
    for r_ in cr:
        P(f"    {foot:9s} {r_['name']:12s} M_b {r_['Mb']:.0e}: eps {r_['eps']:.2e}, r_e {r_['r_e_kpc']:.1f} kpc, <rho_body>/rho_DE "
          f"{r_['rho_body_mean_over_rhoDE']:.1f}; C_U {r_['C_U']:.2e}; at r_half {r_['r_half_kpc']} kpc: dV/Vbar P-sigma {r_['dV_sigma_over_V']:.2e} "
          f"(C {r_['C_sigma_rhalf']:.1e}), P-U {r_['dV_U_over_V']:.2e}; merger draw/Vbar P-sigma {r_['draw_sigma_over_V']:.2e}")
    P(f"    {foot}: min C_U {minC:.2e} -> {'AVOIDS (never energy-limited, no mass ordering)' if minC >= 10 else 'LIMITED somewhere'}")
SY["T3"] = chk("T3_sign_and_ordering", t3_ok, "the channel is never energy-limited (min C_U >= 10, both footings), so it cannot reproduce CFG930/932's "
               "backward ordering; it also selects nothing (no handle on the excess family). Sign: formation cold -> DE, mergers DE -> cold, net "
               "= -Delta(K + W) >= 0 (S-En)")
RES["T3"] = T3

# ---- T4 stability
P("\n  T4 stability (primary IV)")
weff = {}
for foot in FOOTS:
    eps_max = T2A[foot]["eps_max"]
    weff[foot] = {z: eps_max * OMC * (1 + float(z)) ** 3 / (3 * omega_DE(float(z))) for z in ("0.0", "1.0", "1.2", "1.5", "2.33")}
frac_min = min(s_ / m_ for s_, m_ in zip(CFG689_TRANSCRIBED["node_std"], CFG689_TRANSCRIBED["node_mean"]))
line_A2 = 0.1 * frac_min / 3
w_frozen = all(v_ <= 1e-4 for f in FOOTS for v_ in weff[f].values())
w_A2 = all(v_ <= line_A2 for f in FOOTS for v_ in weff[f].values())
iv_struct = (not has_deriv) and no_wave and SY["T1d"]
cross = int(np.sum(np.diff(np.sign(np.diff(WDE))) != 0))
P(f"    IV structure: no derivative of V in T_V: {not has_deriv}; no propagating mode: {no_wave}; composite = dust (T1d): {SY['T1d']}; "
  f"energy density +V, bounded below while Vbar + dV > 0 (headroom)")
for foot in FOOTS:
    P(f"    {foot:9s} ceiling |1 + w_eff| at z 0/1/1.2/1.5/2.33: " + ", ".join(f"{v_:.2e}" for v_ in weff[foot].values())
      + f"  (frozen line 1e-4; A2 record-based line {line_A2:.2e})")
P(f"    CFG630 native 1 + w(0): -2.2e-7 .. -2.6e-7 (README); R-phi friction 3H + Q/phidot^2 (anti-damped on draws, singular at w = -1); "
  f"R-F response Q/((1+w) rho) -> infinity at w = -1; CFG689 best-fit rho_DE nodes change direction {cross} times (w crosses -1)")
T4_frozen = iv_struct and w_frozen
T4_A2 = iv_struct and w_A2
SY["T4_frozen"] = chk("T4_stability_frozen_rule", T4_frozen, f"IV structure {iv_struct}; w_eff ceiling <= 1e-4 at every node: {w_frozen}")
SY["T4_A2"] = chk("T4_stability_A2_reading", T4_A2, f"IV structure {iv_struct}; w_eff ceiling <= {line_A2:.2e} (A2): {w_A2}")
RES["T4"] = dict(weff_ceiling=weff, line_frozen=1e-4, line_A2=line_A2, frac_min=frac_min, IV_structure=iv_struct, cfg689_w_crossings=cross, sympy=SY["T4"])

# ---- T5 and the class
P("\n  T5 verdict on C-E and the class")


def classify(T4ok):
    passing = [k_ for k_, v_ in T2B_GRADE.items() if v_["ok"]]
    if not (T1 and TS_SCT) or not (SY["T2a"] and SY["T3"] and T4ok) or not passing:
        return "NOT CLOSED", passing, []
    derived = [v for v in ("CH-L P-sigma", "CH-L P-U") if T2B_GRADE[f"{v}|a0-cos"]["ok"] and T2B_GRADE[f"{v}|a0-loc"]["ok"]]
    if derived:
        return "DERIVED", passing, []
    conds = []
    if any(k_.startswith("CH-L") for k_ in passing):
        conds.append("C-A0: a0 reads the cosmic-mean vacuum, not the local one (CH-L fails NGC 3198 under a0-loc)")
    if any(k_.startswith("CH-G") for k_ in passing):
        conds.append("C-G: a new cosmic relocation current carries the deposit to the cosmic mean (CH-G)")
    return "CONVERTED", passing, conds


def klass(t5):
    if t5 == "DERIVED" and V2 == "YES":
        return "CHANNEL CLOSES THE BOOKS"
    if t5 in ("DERIVED", "CONVERTED"):
        return "CONDITIONAL"
    return "FAILS"


T5f, pass_f, cond_f = classify(T4_frozen)
T5a, pass_a, cond_a = classify(T4_A2)
CL_f, CL_a = klass(T5f), klass(T5a)
why_f = [] if CL_f != "FAILS" else [n_ for n_, ok_ in (("T1", T1), ("T-S", TS_SCT), ("T2a", SY["T2a"]), ("T3", SY["T3"]),
                                                       ("T4 (w_eff ceiling vs 1e-4)", T4_frozen)) if not ok_]
P(f"    FROZEN RULE: T5 = {T5f}; class = {CL_f}" + (f" (at {', '.join(why_f)})" if why_f else "") + f"; passing (variant|reading): {pass_f}")
P(f"    A2 READING (set after a disclosed hand check): T5 = {T5a}; class = {CL_a}; conditions: {cond_a}; passing: {pass_a}")
P(f"    V2 (one channel for all three): {V2}")
RES["verdict"] = dict(frozen=dict(T5=T5f, klass=CL_f, failing=why_f, passing=pass_f, conditions=cond_f),
                      A2=dict(T5=T5a, klass=CL_a, passing=pass_a, conditions=cond_a), V2=V2,
                      T=dict(T1=T1, TS_SCT=TS_SCT, T2a=SY["T2a"], T3=SY["T3"], T4_frozen=T4_frozen, T4_A2=T4_A2))
RES["K"]["K2"] = K2
RES["K"]["K_all_main"] = K_ALL and K2
P(f"\n  K overall incl. K2: {'PASS' if (K_ALL and K2) else 'FAIL'}")
dump()
sys.exit(0 if (K_ALL and K2) else 1)
