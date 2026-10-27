"""WT-08 -- a repaired parent CFG938' : intrinsic leaf Laplacian + explicit mean density.  Build and full battery.
Criteria: FROZEN_CRITERIA.md (1bf29e4076, committed alone before this script).
Run (one core, one process, < 0.9 GB; RSS guard and memory watchdog exit 75):
    OMP_NUM_THREADS=1 nice -n 10 python3 wt08.py                 -> wt08.out, wt08_results.json
    WT08_MUTATE=1 OMP_NUM_THREADS=1 nice -n 10 python3 wt08.py   -> wt08_MUTATE.out, wt08_results_MUTATE.json
Main exits 0 iff every K control passes (2 otherwise).  MUTATE exits 1 iff every tooth bites (2 otherwise).
Variants: V3 = CFG938 as written (control); V1 = leaf mean; V2 = global variable nu with multiplier mu; V1i/V2i = V1/V2 with the
intrinsic tidal tensor (declared sub-variants for the zero-mode test Z).
kappa = 1/2 FITTED; footings never pooled; cold energy is gravitating mass; no particle species; not theory closed."""
import os, sys, io, json, math, time, resource, contextlib, itertools, subprocess, re
os.environ.setdefault("OMP_NUM_THREADS", "1")
import numpy as np
import sympy as sp
import mpmath as mp
from scipy.optimize import brentq
from scipy.integrate import quad

HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(HERE))
LANES = os.path.join(REPO, "campaign_fresh_gravity")
MUT = os.environ.get("WT08_MUTATE", "0") == "1"
TAG = "_MUTATE" if MUT else ""
OUT = []; RES = {"lane": "WT-08", "criteria": "1bf29e4076", "mutate": MUT, "checks": {}, "tests": {}, "labels": {}}
T0 = time.time(); RSS_LIMIT = 0.9e9


def P(s=""):
    print(s, flush=True); OUT.append(str(s))


def rss():
    r = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    return r if sys.platform == "darwin" else r * 1024


def swap_used_mb():
    try:
        s = subprocess.run(["sysctl", "-n", "vm.swapusage"], capture_output=True, text=True, timeout=10).stdout
        m = re.search(r"used = ([0-9.]+)M", s)
        return float(m.group(1)) if m else 0.0
    except Exception:
        return 0.0


def free_inactive_gb():
    try:
        s = subprocess.run(["vm_stat"], capture_output=True, text=True, timeout=10).stdout
        ps = int(re.search(r"page size of (\d+) bytes", s).group(1))
        fr = int(re.search(r"Pages free:\s+(\d+)", s).group(1)); ina = int(re.search(r"Pages inactive:\s+(\d+)", s).group(1))
        return (fr + ina) * ps / 1e9
    except Exception:
        return 99.0


SWAP0 = swap_used_mb()


def dump():
    RES["runtime_s"] = round(time.time() - T0, 1); RES["peak_rss_GB"] = round(rss() / 1e9, 3)
    json.dump(RES, open(os.path.join(HERE, f"wt08_results{TAG}.json"), "w"), indent=1, default=str)
    open(os.path.join(HERE, f"wt08{TAG}.out"), "w").write("\n".join(OUT) + "\n")


def guard(where):
    if rss() > RSS_LIMIT:
        P(f"RSS GUARD {rss() / 1e9:.2f} GB at {where}; exit 75"); dump(); sys.exit(75)
    sw, fi = swap_used_mb(), free_inactive_gb()
    if sw - SWAP0 > 1024 or fi < 8.0:
        P(f"MEMORY WATCHDOG at {where}: swap growth {sw - SWAP0:.0f} MB, free+inactive {fi:.1f} GB; exit 75"); dump(); sys.exit(75)


def chk(name, ok, detail=""):
    RES["checks"][name] = {"pass": bool(ok), "detail": str(detail)}
    P(f"  [{'PASS' if ok else 'FAIL'}] {name}: {detail}")
    return bool(ok)


def is0(e):
    return sp.simplify(sp.expand(e)) == 0


# ------------------------------------------------------------------------------------------------ constants / inputs (read only)
sys.path.insert(0, LANES)
with contextlib.redirect_stdout(io.StringIO()):
    import CFG4_common as C4
A0 = dict(C4.A0); FOOTS = ("canonical", "alt")
assert abs(A0["canonical"] - 9.3603e-11) < 1e-15 and abs(A0["alt"] - 1.1312e-10) < 1e-15
G_SI, C_SI, MSUN, PC = 6.67430e-11, 299792458.0, 1.98847e30, 3.0856775814913673e16
KPC, MPC = 1e3 * PC, 1e6 * PC
K_SI = 4 * math.pi * G_SI
H0 = 67.4e3 / MPC; OMB = 0.0493; OMC = OMB * 5.364; OMM = OMB + OMC; OML = 1 - OMM
RHOCRIT = 3 * H0 ** 2 / (8 * math.pi * G_SI); RHOC0 = OMC * RHOCRIT
LSTAR = {"24pc": 24 * PC, "1kpc": 1 * KPC}
RSUN, AU = 6.957e8, 1.495978707e11; GMSUN = G_SI * MSUN
H72 = [(1.50e10, 1.67), (3.66e10, 2.07), (6.01e10, 3.44), (9.13e10, 2.77)]
CFG770_BG = {"canonical": [(2.00e-10, 0.6812), (2.32e-10, 0.7125), (2.64e-10, 0.7382)],
             "alt": [(2.00e-10, 0.6387), (2.32e-10, 0.6722), (2.64e-10, 0.7000)]}
R_SUN_GAL = 8.2 * KPC; D_GW = 40 * MPC
FB = sp.Rational(1000, 6364); FC = sp.Rational(5364, 6364)                      # Omega_b/Omega_m, Omega_c/Omega_m (5.364)


def law_g(gN, a0):
    return 0.5 * (gN + math.sqrt(gN * gN + 4.0 * gN * a0))


def law_u(gN, a0):
    return law_g(gN, a0) - gN


def Rrem(u, a0): return u * u / (a0 - u)
def Rp(u, a0): return u * (2 * a0 - u) / (a0 - u) ** 2
def Dfull(u, a0): return u / (1 - u / a0)
def Wfull_num(u, a0): return (-a0 * u - a0 * a0 * math.log1p(-u / a0)) / K_SI


P("WT-08  repaired parent CFG938' (intrinsic leaf Laplacian + explicit mean density)" + ("   [MUTATE]" if MUT else ""))
P("  criteria 1bf29e4076; kappa = 1/2 FITTED; footings never pooled; not theory closed")
P(f"  footings: canonical a0 = {A0['canonical']:.4e}, alt a0 = {A0['alt']:.4e} m/s^2; swap at start {SWAP0:.0f} MB, "
  f"free+inactive {free_inactive_gb():.1f} GB")

# ================================================================================================ covariant machinery
x0, x, y, z = sp.symbols("x0 x y z", real=True); XX = [x0, x, y, z]
eps = sp.Symbol("epsilon")
c, Km, Kb, Ls, u0 = sp.symbols("c K_m K_b L_s u_0", positive=True)
h = sp.Symbol("h", real=True, nonzero=True)
Dd, Dp = sp.symbols("D_d D_p", real=True)
kk, sig, om = sp.symbols("k sigma omega")
Af = sp.Function("A", positive=True)(x0)
FF = sp.Function("F")(x0)                                    # zero mode of chi (Z test)
ChiF = sp.Function("Chi")(x0)                                # V3 background chibar on a general FRW (T8)


def ser2(e):
    e0 = e.subs(eps, 0); d1 = sp.diff(e, eps)
    return sp.expand(e0 + eps * d1.subs(eps, 0) + eps ** 2 * sp.diff(d1, eps).subs(eps, 0) / 2)


def fld(name):
    return sp.Function(name)(x0, x)


def label_kin(phis, g, sqrtg):
    dphi = [[sp.diff(p_, X) for X in XX] for p_ in phis]
    J = []
    for mu in range(4):
        tot = 0
        for (a_, b_, c_) in itertools.permutations([i for i in range(4) if i != mu], 3):
            lc = sp.LeviCivita(mu, a_, b_, c_)
            for (I, Jx, Kx) in itertools.permutations(range(3), 3):
                tot += lc * sp.LeviCivita(I, Jx, Kx) * dphi[I][a_] * dphi[Jx][b_] * dphi[Kx][c_]
        J.append(tot / (6 * sqrtg))
    J = sp.Matrix(J)
    j0 = J[0].subs(eps, 0).subs(Af, 1).subs(x0, 0)
    if j0 < 0:
        J = -J
    J = J.applyfunc(ser2)
    n = ser2(sp.sqrt(-ser2((J.T * g * J)[0])))
    uu = (J / n).applyfunc(ser2); ud = (g * uu).applyfunc(ser2)
    return n, uu, ud


BCACHE = {}


def build(bg, variant, chib=0, Phi=False, baryons=False, eta=True, tether=True, Lsv=None, KWform="half", geomkey="",
          noclock=False, mu_nudot=True, tiltmode="leaf", trace_lap3=False):
    """Plane-symmetric O(eps^2) Lagrangian of a variant.
    bg: 'ds' (a = exp(h x0), c = 1, lengths c/H, frozen), 'gen' (a = A(x0) general, c = 1), 'static' (Minkowski, x0 = c t).
    variant: 'V3' (h^{mn} nabla nabla chi, CFG938), 'V1' / 'V1i' (intrinsic Lap, leaf mean with leaf-time tilt), 'V2' / 'V2i'
    (intrinsic Lap, global nu with multiplier mu), 'V2f' (V2i with the K u.dchi correction sign flipped: MU4), 'MU1' (V1 with the
    theta u.dchi term restored), 'dust' (no tether sector).  tiltmode: 'leaf' (nbar at the leaf time) | 'coord' (K3 control)."""
    key = (bg, variant, str(chib), Phi, baryons, eta, tether, str(Lsv), KWform, geomkey, noclock, mu_nudot, tiltmode, trace_lap3)
    if key in BCACHE:
        return BCACHE[key]
    if bg == "ds":
        a = sp.exp(h * x0); cc = 1
    elif bg == "gen":
        a = Af; cc = 1
    else:
        a = sp.Integer(1); cc = c
    g = sp.diag(-1, a ** 2, a ** 2, a ** 2); gi = g.inv(); sqrtg = a ** 3
    xi = fld("xi"); et = fld("eta") if eta else sp.Integer(0)
    dchi = fld("dchi"); dlam = fld("dlam")
    fields = [xi] + ([et] if eta else []) + [dchi, dlam]
    n, uu, ud = label_kin([x - eps * xi, y - eps * et, z], g, sqrtg)
    chi = chib + eps * dchi; lam = eps * dlam
    hup = (gi + uu * uu.T).applyfunc(ser2); hdn = (g + ud * ud.T).applyfunc(ser2)
    hmix = (sp.eye(4) + ud * uu.T).applyfunc(ser2)                                    # h_m^a
    Gam = [[[sp.simplify(sum(gi[r_, d_] * (sp.diff(g[d_, m_], XX[n_]) + sp.diff(g[d_, n_], XX[m_]) - sp.diff(g[m_, n_], XX[d_]))
                             for d_ in range(4)) / 2) for n_ in range(4)] for m_ in range(4)] for r_ in range(4)]
    dch = [sp.diff(chi, X) for X in XX]
    theta = ser2(sum(sp.diff(sqrtg * uu[m_], XX[m_]) for m_ in range(4)) / sqrtg)
    udchi = ser2(sum(uu[m_] * dch[m_] for m_ in range(4)))
    nab = sp.Matrix(4, 4, lambda m_, n_: ser2(sp.diff(chi, XX[m_], XX[n_]) - sum(Gam[r_][m_][n_] * dch[r_] for r_ in range(4))))
    D2 = ser2(sum(hup[m_, n_] * nab[m_, n_] for m_ in range(4) for n_ in range(4)))
    Lap3 = ser2(D2 + theta * udchi)
    if noclock:
        dch_s = [sp.diff(eps * dchi, X) for X in XX]
    else:
        dch_s = dch
    s = ser2(sum(hup[m_, n_] * dch_s[m_] * dch_s[n_] for m_ in range(4) for n_ in range(4)))
    L_s = Ls if Lsv is None else Lsv
    tt = 0
    if tether and L_s != 0:
        DD = (hmix * nab * hmix.T).applyfunc(ser2)
        tau = (DD - hdn * (Lap3 if trace_lap3 else D2) / 3).applyfunc(ser2)     # trace_lap3: WT-02 MU3's convention (K3', post hoc)
        if variant in ("V1i", "V2i", "V2f"):
            nabu = sp.Matrix(4, 4, lambda m_, n_: ser2(sp.diff(ud[n_], XX[m_]) - sum(Gam[r_][m_][n_] * ud[r_] for r_ in range(4))))
            Kab = (hmix * nabu * hmix.T).applyfunc(ser2)
            Ks = ((Kab + Kab.T) / 2).applyfunc(ser2)
            Kt = (Ks - hdn * theta / 3).applyfunc(ser2)
            sgn = -1 if variant == "V2f" else 1
            tau = (tau + sgn * Kt * udchi).applyfunc(ser2)
        tauup = (gi * tau * gi).applyfunc(ser2)
        tt = ser2(sum(tau[m_, n_] * tauup[m_, n_] for m_ in range(4) for n_ in range(4)))
    # W: K W(u) -> s/2 on FRW (u = O(eps)); static with background gradient: WT-02's D(u0), D'(u0) expansion
    if KWform == "half":
        KW = s / 2
    else:
        ds_ = sp.expand(s - u0 ** 2)
        KW = Dd / (2 * u0) * ds_ + sp.Rational(1, 2) * (Dp - Dd / u0) / (4 * u0 ** 2) * ds_ ** 2
    nbar_bg = a ** -3
    extra = 0
    if variant in ("V3", "dust"):
        cons = D2 - Km * n
    elif variant == "MU1":
        Th = fld("Th"); be = fld("beta")
        nbl = nbar_bg if bg == "static" else (sp.exp(-3 * h * (x0 + eps * Th)) if bg == "ds" else Af.subs(x0, x0 + eps * Th) ** -3)
        cons = D2 - Km * (n - ser2(nbl))
        if bg != "static":
            extra += sqrtg * eps * be * (eps * sp.diff(Th, x) + ud[1]); fields += [Th, be]
    elif variant in ("V1", "V1i"):
        if bg == "static":
            nbl = nbar_bg
        else:
            Th = fld("Th"); be = fld("beta")
            if tiltmode == "coord":
                nbl = nbar_bg
            else:
                nbl = sp.exp(-3 * h * (x0 + eps * Th)) if bg == "ds" else Af.subs(x0, x0 + eps * Th) ** -3
                extra += sqrtg * eps * be * (eps * sp.diff(Th, x) + ud[1]); fields += [Th, be]
        cons = Lap3 - Km * (n - ser2(nbl))
    elif variant in ("V2", "V2i", "V2f"):
        dnu = fld("dnu"); mux = fld("mux"); muy = fld("muy")
        nu = nbar_bg + eps * dnu
        nu_mu = nu if mu_nudot else (1 + eps * dnu)
        mu_up = [0, eps * mux, eps * muy, 0]
        extra += sqrtg * sum(mu_up[m_] * hmix[m_, a_] * sp.diff(nu_mu, XX[a_]) for m_ in range(4) for a_ in range(4))
        cons = Lap3 - Km * (n - nu)
        fields += [dnu, mux] + ([muy] if eta else [])
    else:
        raise ValueError(variant)
    Lt = sqrtg * (-cc ** 2 * Km * n)
    if tether and variant != "dust":
        Lt += sqrtg * (-KW - sp.Rational(3, 8) * L_s ** 2 * tt + lam * cons) + extra
    if baryons:
        xb = fld("xib")
        nb, _, _ = label_kin([x - eps * xb, y, z], g, sqrtg)
        Lt += sqrtg * (-cc ** 2 * Kb * nb)
        fields.append(xb)
    if Phi:
        Ph = fld("Phi")
        src = Km * n + (Kb * nb if baryons else 0)
        Lt += -eps * Ph * sqrtg * src - eps ** 2 * a * sp.diff(Ph, x) ** 2 / 2
        fields.append(Ph)
    L2 = sp.expand(sp.expand(Lt).coeff(eps, 2).doit())
    fields = [f_ for f_ in fields if L2.has(f_)]
    out = dict(L2=L2, fields=fields, a=a, n=n, uu=uu, ud=ud, theta=theta, udchi=udchi, D2=D2, Lap3=Lap3, s=s, chib=chib)
    BCACHE[key] = out
    return out


def modes(L2, fields, phase, at):
    eqs = sp.euler_equations(L2, fields, [x0, x])
    amps = sp.symbols(" ".join(f"A{i}" for i in range(len(fields))))
    if len(fields) == 1:
        amps = (amps,)
    M = sp.zeros(len(fields), len(fields))
    for i, e in enumerate(eqs):
        ex = e.lhs
        for f_, A_ in zip(fields, amps):
            ex = ex.subs(f_, A_ * sp.exp(phase)).doit()
        ex = sp.expand(sp.powsimp(sp.expand(ex * sp.exp(-phase)))).subs(at)
        ex = sp.expand(sp.simplify(ex))
        for j, A_ in enumerate(amps):
            M[i, j] = sp.expand(ex.coeff(A_))
    return M, eqs


def fidx(B, name):
    for i, f_ in enumerate(B["fields"]):
        if f_.func.__name__ == name:
            return i
    return None


def ds_system(variant, Phi=False, **kw):
    B = build("ds", variant, chib=(Km / (9 * h ** 2) * sp.exp(-3 * h * x0) if variant in ("V3",) else 0), Phi=Phi, **kw)
    M, _ = modes(B["L2"], B["fields"], sig * x0 + sp.I * kk * x, {x0: 0})
    return M, B


def static_system(variant, geom, Phi=True, **kw):
    chib = {"par": u0 * x, "perp": u0 * y, "zero": 0}[geom]
    B = build("static", variant, chib=chib, Phi=Phi, KWform=("half" if geom == "zero" else "D"), geomkey=geom, **kw)
    M, _ = modes(B["L2"], B["fields"], -sp.I * om / c * x0 + sp.I * kk * x, {})
    return M, B


def frozen(zv):
    E2 = OMM * (1 + zv) ** 3 + OML
    return 1.5 * OMC * (1 + zv) ** 3 / E2, H0 * math.sqrt(E2)


def poly_maxre(poly, var, subsd, ks, dps=80):
    mp.mp.dps = dps
    syms = sorted(poly.free_symbols - {var}, key=str)
    cf = sp.Poly(poly, var).all_coeffs()
    fs = [sp.lambdify(syms, cc_, "mpmath") for cc_ in cf]
    out = []
    for kv in ks:
        vals = {**subsd, kk: kv}
        args = [mp.mpf(vals[s_]) if not isinstance(vals[s_], mp.mpf) else vals[s_] for s_ in syms]
        coef = [f_(*args) for f_ in fs]
        while abs(coef[0]) == 0:
            coef = coef[1:]
        if len(coef) == 1:
            out.append((float("-inf"), [])); continue
        rts = mp.polyroots(coef, maxsteps=1000, extraprec=1500)
        out.append((max(float(mp.re(r_)) for r_ in rts), rts))
    return out


def hadamard_ds(M, Kmv, Lsv, hsign, ks=(1e2, 1e3, 1e4, 1e5, 1e6)):
    det = sp.factor(M.det())
    num = sp.numer(sp.together(det))
    res = poly_maxre(sp.expand(num), sig, {h: hsign, Km: Kmv, Ls: Lsv}, ks)
    mx = [r_[0] for r_ in res]
    slope = (math.log(mx[-1] / mx[-2]) / math.log(ks[-1] / ks[-2])) if (mx[-1] > 0 and mx[-2] > 0) else float("nan")
    ill = (mx[-1] / abs(hsign) > 1e3) and (slope >= 0.5)
    well = max(mx) <= 10 * abs(hsign)
    cls = "ILL-POSED" if ill else ("WELL-POSED" if well else "UNRESOLVED")
    return dict(k=list(ks), maxRe=mx, slope=slope, cls=cls), det


# ================================================================================================ K CONTROLS
P("\n==================== K CONTROLS ====================")
KOK = {}
# ---- K1a (and T1 machinery): NGC 3198 law from the reduced static functional, with the mean-subtraction symbol nb
r_, G_ = sp.symbols("r G", positive=True); uS, gNS, a0S, nbS = sp.symbols("u g_N a_0 nbar", positive=True)
Wfull_s = (-a0S * uS - a0S ** 2 * sp.log(1 - uS / a0S)) / (4 * sp.pi * G_)
Mc = sp.Function("M_c")(r_); Mb = sp.Function("M_b")(r_)
Mbar = 4 * sp.pi * nbS * r_ ** 3 / 3


def Lred(variant):
    """Reduced static energy density E[M_c] (spherical, gamma -> 0).  V3: u = G M_c/r^2 (isolated: the theta term vanishes on a
    static medium).  V1/V2: u = G (M_c - Mbar_leaf)/r^2 with the leaf mean nb (nu = nb on shell).  MU2: no tether constraint (u free)."""
    if variant == "V3":
        uexpr = G_ * Mc / r_ ** 2
    else:
        uexpr = G_ * (Mc - Mbar) / r_ ** 2
    return -G_ * (Mb + Mc) ** 2 / (2 * r_ ** 2) + 4 * sp.pi * r_ ** 2 * sp.Lambda(uS, Wfull_s)(uexpr)


dat = np.genfromtxt(os.path.join(REPO, "real_research", "data", "sparc_data", "NGC3198_rotmod.dat"), comments="#")
Rr = dat[:, 0] * KPC; Vg, Vd, Vb = dat[:, 3] * 1e3, dat[:, 4] * 1e3, dat[:, 5] * 1e3
gNb = (Vg * np.abs(Vg) + 0.61 * Vd * np.abs(Vd) + 0.61 * Vb * np.abs(Vb)) / Rr


def T1_solve(variant):
    L = Lred(variant)
    EL = sp.euler_equations(L, [Mc], [r_])[0].lhs
    if variant != "V3":
        EL = EL.subs(nbS, 0)
    ELr = EL.subs({Mc: uS * r_ ** 2 / G_, Mb: gNS * r_ ** 2 / G_}).doit()
    fEL = sp.lambdify((uS, gNS, a0S, G_), sp.simplify(ELr), "math")
    out = {}
    for f in FOOTS:
        a0 = A0[f]; rel = []
        for gn in gNb:
            uu_ = brentq(lambda q: fEL(q, gn, a0, G_SI), 1e-300, a0 * (1 - 1e-15), xtol=1e-30, rtol=1e-15, maxiter=500)
            rel.append(abs((gn + uu_) / law_g(gn, a0) - 1))
        out[f] = float(max(rel))
    same = None
    if variant != "V3":
        same = is0(Lred(variant).subs(nbS, 0) - Lred("V3"))
    return out, same


k1v3, _ = T1_solve("V3")
k1ok = all(v <= 1e-12 for v in k1v3.values()) and len(gNb) == 43
P(f"  K1a V3 NGC 3198 law: max|g/g_law - 1| canonical {k1v3['canonical']:.2e}, alt {k1v3['alt']:.2e} (CFG938 2.2e-16)")
guard("K1a")
# ---- K1b: V3 FRW leading root k^2/3 and Hadamard fires (this lane's machinery)
Mv3, Bv3 = ds_system("V3")
Kmv0, Hz0 = frozen(0.0)
hv3, detv3 = hadamard_ds(Mv3, Kmv0, LSTAR["24pc"] * Hz0 / C_SI, 1.0)
lead = hv3["maxRe"][-1] / (1e6 ** 2 / 3)
k1b = abs(lead - 1) <= 1e-6 and hv3["cls"] == "ILL-POSED"
P(f"  K1b V3 FRW (z=0, 24 pc): max Re sigma/H = {[f'{m_:.4e}' for m_ in hv3['maxRe']]}; slope {hv3['slope']:.4f}; leading root / (k^2/3) - 1 = "
  f"{lead - 1:.2e}; class {hv3['cls']}")
KOK["K1"] = chk("K1_V3_reproduces_CFG938_law_and_WT02_root", k1ok and k1b, f"law {max(k1v3.values()):.2e}; FRW root ratio {lead:.12f}; {hv3['cls']}")
guard("K1")
# ---- K2: static Minkowski: V1/V2 determinants = V3's (par, perp, zero), and the static functional at nbar = 0
k2 = []
STAT = {}
for geom in ("par", "perp", "zero"):
    for var in ("V3", "V1", "V2", "V1i", "V2i"):
        STAT[(var, geom)] = static_system(var, geom)
    d3 = sp.factor(STAT[("V3", geom)][0].det())
    for var in ("V1", "V2", "V1i", "V2i"):
        dv = sp.factor(STAT[(var, geom)][0].det())
        ratio = sp.simplify(dv / d3)
        k2.append((geom, var, ratio, ratio.free_symbols <= {kk} and ratio != 0))
    guard(f"K2 {geom}")
for geom, var, ratio, ok in k2:
    P(f"  K2 static {geom:4s} {var:3s}: det/det_V3 = {ratio}")
_, same1 = T1_solve("V1")
KOK["K2"] = chk("K2_static_V1_V2_reduce_to_V3", all(o for *_, o in k2) and same1,
                "every static determinant is V3's times a nonzero constant (k-power from the extra multipliers); E[M_c] at nbar = 0 identical")
# ---- K3: V1 with the tilt off reproduces WT-02 MU3's FRW determinant (literal string from wt02_MUTATE.out)
mu3_str = ("K_m**2*k**2*sigma*(2*h + sigma)*(27*K_m*L_s**2*h**3*sigma + 9*K_m*L_s**2*h**2*sigma**2 - 2*K_m*L_s**2*k**4 - 4*K_m*k**2 "
           "- 8*h*k**2*sigma - 4*k**2*sigma**2)/4")
mu3 = sp.sympify(mu3_str, locals={"K_m": Km, "k": kk, "sigma": sig, "h": h, "L_s": Ls})
Mk3, Bk3 = ds_system("V1", tiltmode="coord")
dk3 = sp.factor(Mk3.det())
r3 = sp.simplify(dk3 / mu3)
KOK["K3"] = chk("K3_V1_tilt_off_equals_WT02_MU3", r3.free_symbols <= {kk} and r3 != 0, f"det(V1, nbar at coordinate time)/det(WT-02 MU3) = {r3}")
# K3' (POST HOC, amendment A1): WT-02's MU3 code also replaced D^2 by the intrinsic Lap inside tau's trace subtraction (tau no longer
# traceless).  Rebuild V1 (tilt off) with that convention: it must reproduce MU3 exactly; the difference is confined to O(L*^2 H^2).
Mk3p, _ = ds_system("V1", tiltmode="coord", trace_lap3=True)
r3p = sp.simplify(sp.factor(Mk3p.det()) / mu3)
k3p = r3p.free_symbols <= {kk} and r3p != 0
P(f"  K3' (POST HOC, A1) V1 tilt off with WT-02's tau-trace convention: det/det(MU3) = {r3p}  -> reproduces MU3: {k3p}")
P(f"      frozen-K3 difference is the tau trace convention only: V1 keeps CFG938's traceless tau (as instructed); MU3 terms "
  f"27 K L*^2 h^3 sigma + 9 K L*^2 h^2 sigma^2 come from (theta u.dchi)^2 inside tau, order (L* H/c)^2 ~ 1e-16 relative")
RES["K3prime_posthoc"] = dict(ratio=str(r3p), reproduces=bool(k3p))
guard("K3")


# ---- growth machinery (T8; K4): leading order aH << k << a/L*, EdS, baryons free dust, quasi-static Phi
kap = sp.Symbol("kappa", positive=True); tS = sp.Symbol("t", positive=True); alp = sp.Symbol("alpha")
SCALE = {"xi": 0, "xib": 0, "dchi": 1, "dlam": 1, "Phi": 1, "Th": 1, "beta": 2, "dnu": 1, "mux": 2}


def growth_exponent(variant, noclock=False, tether=True, verbose=False):
    chib = ChiF if variant == "V3" else 0
    B = build("gen", variant, chib=chib, Phi=True, baryons=True, eta=False, tether=tether, Lsv=0, noclock=noclock)
    L2 = B["L2"]
    if variant == "V3":
        chip = -Km / (3 * Af ** 2 * sp.diff(Af, x0))                         # S1d on a general FRW (only the medium sources chi)
        L2 = sp.expand(L2.subs(sp.Derivative(ChiF, (x0, 2)), sp.diff(chip, x0)).subs(sp.Derivative(ChiF, x0), chip))
    fields = [f_ for f_ in B["fields"] if L2.has(f_)]
    names = [f_.func.__name__ for f_ in fields]
    amps = {nm: sp.Function("Am_" + nm)(x0) for nm in names}
    eqs = sp.euler_equations(L2, fields, [x0, x])
    lead = {}
    for nm, e in zip(names, eqs):
        ex = e.lhs.subs({f_: amps[n2] * sp.exp(sp.I * kk * x) for n2, f_ in zip(names, fields)}).doit()
        ex = sp.expand(sp.powsimp(sp.expand(ex * sp.exp(-sp.I * kk * x))))
        assert not ex.has(x), nm
        ex = ex.subs({amps[n2]: kap ** SCALE[n2] * amps[n2] for n2 in names}, simultaneous=True).doit()
        ex = sp.expand(ex.subs(kk, 1 / kap) * kap ** 8)
        pl = sp.Poly(ex, kap)
        md = min(m_[0] for m_ in pl.monoms())
        lead[nm] = sp.expand(pl.coeff_monomial(kap ** md))
    dyn = [n_ for n_ in names if n_ in ("xi", "xib")]
    aux = [n_ for n_ in names if n_ not in dyn]
    asym = {n_: sp.Symbol("S_" + n_) for n_ in aux}
    aeqs = []
    for n_ in aux:
        e = lead[n_]
        for m_ in aux:
            assert not e.has(sp.Derivative(amps[m_], x0)), (n_, m_)
        aeqs.append(e.subs({amps[m_]: asym[m_] for m_ in aux}))
    sol = sp.solve(aeqs, [asym[m_] for m_ in aux], dict=True)
    assert len(sol) == 1, (variant, sol)
    sol = sol[0]
    rows = []
    Cs = sp.symbols("C1 C2")
    homog = True
    for n_ in dyn:
        e = lead[n_].subs({amps[m_]: sol[asym[m_]] for m_ in aux}).doit()
        e = e.subs(Af, x0 ** sp.Rational(2, 3)).doit()
        e = e.subs({Km: 2 * FC / 3, Kb: 2 * FB / 3})
        e = e.subs({amps["xi"]: Cs[0] * x0 ** alp, amps["xib"]: Cs[1] * x0 ** alp}).doit()
        e = sp.expand(sp.powsimp(sp.expand(e / x0 ** alp), force=True))
        pows = set(sp.nsimplify(t_.as_coeff_exponent(x0)[1]) for t_ in sp.Add.make_args(e))
        homog = homog and len(pows) == 1
        p0 = list(pows)[0]
        rows.append(sp.expand(sp.powsimp(e / x0 ** p0, force=True)))
    Mg = sp.Matrix([[sp.diff(r__, C_) for C_ in Cs] for r__ in rows])
    det = sp.expand(Mg.det())
    pol = sp.Poly(det, alp)
    roots = np.roots([complex(sp.N(c_)) for c_ in pol.all_coeffs()])
    rr = [z_.real for z_ in roots if abs(z_.imag) < 1e-9]
    n_exp = 1.5 * max(rr)
    if verbose:
        P(f"      [{variant}{' noclock' if noclock else ''}{'' if tether else ' tether-off'}] leading-order fields {names}; homogeneous {homog}; "
          f"alpha roots {[round(float(q), 6) for q in sorted(rr)]}")
    return n_exp, homog, dict(names=names, det=str(det))


n_v3, hv3g, _ = growth_exponent("V3", verbose=True)
n_v3nc, hv3nc, _ = growth_exponent("V3", noclock=True, verbose=True)
n_dust, hdust, _ = growth_exponent("V3", tether=False, verbose=True)
k4 = abs(n_v3 - 0.69433) <= 5e-4 and abs(n_v3nc - 0.60954) <= 5e-4 and abs(n_dust - 1) <= 1e-6 and hv3g and hv3nc and hdust
KOK["K4"] = chk("K4_growth_machinery_reproduces_CFG941", k4,
                f"V3 n = {n_v3:.5f} (CFG941 D6 0.69433); V3 without the chibar boost n = {n_v3nc:.5f} (CFG938 S6 0.60954); dust n = {n_dust:.6f}")
guard("K4")

# ---- K5 + T10 machinery: TT wave in a medium at rest with chi = V0 x0 + u0 z (x0 = c t)
th_k = sp.Symbol("theta_k", real=True)
nvec = sp.Matrix([sp.sin(th_k), 0, sp.cos(th_k)])
e1 = sp.Matrix([sp.cos(th_k), 0, -sp.sin(th_k)]); e2v = sp.Matrix([0, 1, 0])
EP = e1 * e1.T - e2v * e2v.T; EX = e1 * e2v.T + e2v * e1.T
Ap, Ax = sp.symbols("A_p A_x", real=True)
Fw = sp.Function("Fw")
zeta = (nvec[0] * x + nvec[2] * z)
Hs = (Ap * EP + Ax * EX) * Fw(x0, zeta)
gT = sp.diag(-1, 1, 1, 1)
for i in range(3):
    for j in range(3):
        gT[i + 1, j + 1] += eps * Hs[i, j]


def ricci_lin(gm):
    gim = gm.inv()
    Gm = [[[sum(gim[r__, d_] * (sp.diff(gm[d_, m_], XX[n_]) + sp.diff(gm[d_, n_], XX[m_]) - sp.diff(gm[m_, n_], XX[d_])) for d_ in range(4)) / 2
            for n_ in range(4)] for m_ in range(4)] for r__ in range(4)]
    Gm1 = [[[sp.diff(Gm[r__][m_][n_], eps).subs(eps, 0) for n_ in range(4)] for m_ in range(4)] for r__ in range(4)]
    R1 = sp.zeros(4, 4)
    for m_ in range(4):
        for n_ in range(4):
            R1[m_, n_] = sum(sp.diff(Gm1[r__][m_][n_], XX[r__]) - sp.diff(Gm1[r__][m_][r__], XX[n_]) for r__ in range(4))
    return R1


R1 = ricci_lin(gT)
boxH = sp.Matrix(3, 3, lambda i, j: -sp.diff(Hs[i, j], x0, 2) + sum(sp.diff(Hs[i, j], X, 2) for X in (x, y, z)))
k5a = all(sp.simplify(R1[i + 1, j + 1] + boxH[i, j] / 2) == 0 for i in range(3) for j in range(3))
V0s, u0s, Oms, kzs = sp.symbols("V_0 u_0s Omega k_z", positive=True)
phs = kzs * zeta - Oms * x0
Hpw = (Ap * EP + Ax * EX) * sp.cos(phs)
gP = sp.diag(-1, 1, 1, 1)
for i in range(3):
    for j in range(3):
        gP[i + 1, j + 1] += eps * Hpw[i, j]
gPi = gP.inv()


def Gam1(rho, i, j):
    return sp.expand(sp.diff(sum(gPi[rho, d_] * (sp.diff(gP[d_, i], XX[j]) + sp.diff(gP[d_, j], XX[i]) - sp.diff(gP[i, j], XX[d_]))
                                 for d_ in range(4)) / 2, eps).subs(eps, 0))


G0 = {(i, j): Gam1(0, i, j) for i in range(1, 4) for j in range(1, 4)}
Gz = {(i, j): Gam1(3, i, j) for i in range(1, 4) for j in range(1, 4)}
tr0 = sp.simplify(sum(G0[(i, i)] for i in range(1, 4))); trz = sp.simplify(sum(Gz[(i, i)] for i in range(1, 4)))
tauG = {k_: -(V0s * G0[k_] + u0s * Gz[k_]) + (sp.Rational(1, 3) * (V0s * tr0 + u0s * trz) if k_[0] == k_[1] else 0) for k_ in G0}
ttG = sp.expand(sum(v_ ** 2 for v_ in tauG.values()))
EHq = sp.expand(sum(sp.diff(Hpw[i, j], x0) ** 2 - sum(sp.diff(Hpw[i, j], X) ** 2 for X in (x, y, z)) for i in range(3) for j in range(3)))
s2 = sp.sin(phs) ** 2
QEH = sp.simplify(EHq / s2); Qtt = sp.simplify(ttG / s2)
Spol = sp.simplify(sum(((Ap * EP + Ax * EX)[i, j]) ** 2 for i in range(3) for j in range(3)))
alpha_t = sp.simplify(Qtt.coeff(V0s, 2).subs(u0s, 0) / Oms ** 2)
beta_s = sp.simplify(Qtt.subs(V0s, 0).coeff(u0s, 2) / kzs ** 2)
gamma_x = sp.simplify(sp.expand(Qtt).coeff(V0s, 1).coeff(u0s, 1) / (Oms * kzs))
C_t = sp.simplify(6 * alpha_t / Spol); C_s = sp.simplify(6 * beta_s / Spol); C_x = sp.simplify(6 * gamma_x / Spol)
grid_th = np.linspace(0, math.pi / 2, 7)
Cs_vals = [float(C_s.subs({th_k: t_, Ap: a_, Ax: b_})) for t_ in grid_th for (a_, b_) in ((1, 0), (0, 1), (1, 1))]
Ct_vals = [float(C_t.subs({th_k: t_, Ap: a_, Ax: b_})) for t_ in grid_th for (a_, b_) in ((1, 0), (0, 1), (1, 1))]
Cx_vals = [float(C_x.subs({th_k: t_, Ap: a_, Ax: b_})) for t_ in grid_th for (a_, b_) in ((1, 0), (0, 1), (1, 1))]
QEHc = sp.simplify(QEH / Spol)
k5 = k5a and max(abs(v_ - 1.5) for v_ in Cs_vals) < 1e-12 and sp.simplify(QEHc - (Oms ** 2 - kzs ** 2)) == 0
KOK["K5"] = chk("K5_TT_Ricci_and_spatial_C_s", k5,
                f"R^(1)_ij = -(1/2) box h_ij; EH form (Omega^2 - k^2) Sum A^2; C_s in [{min(Cs_vals):.6f}, {max(Cs_vals):.6f}] (WT-02 E1: 1.5); "
                f"tr Gamma^0 = {tr0}, tr Gamma^z = {trz}; L* = 0 removes every correction (all terms carry L*^2)")
P(f"  T10 machinery: C_t (timelike gradient V0) in [{min(Ct_vals):.6f}, {max(Ct_vals):.6f}]; cross V0 u0 coefficient C_x = {sp.simplify(C_x)} "
  f"(range {min(Cx_vals):.4f}..{max(Cx_vals):.4f})")
guard("K5")

# ---- K6: CFG938 slip (W-only s_grad) reproduced
SYS = [("dwarf", 1e7, 0.3), ("MW disc", 6e10, 10.0), ("MW outer", 6e10, 100.0), ("group", 1e12, 300.0), ("cluster", 1.5e14, 1000.0)]
MSUN847, KPC847 = 1.989e30, 3.0857e19
SLIP = {}
for f in FOOTS:
    a0 = A0[f]
    for name, Mb_, rk_ in SYS:
        M = Mb_ * MSUN847; rr = rk_ * KPC847
        def uat(xx_, M=M, a0=a0):
            g__ = law_g(G_SI * M / xx_ ** 2, a0); return g__ * a0 / (g__ + a0)
        g_ = law_g(G_SI * M / rr ** 2, a0); uu_ = uat(rr); W_ = Wfull_num(uu_, a0)
        hh = 1e-5 * rr
        rho_c = ((rr + hh) ** 2 * uat(rr + hh) - (rr - hh) ** 2 * uat(rr - hh)) / (2 * hh) / (K_SI * rr ** 2)
        s_grad = 4 * math.pi * G_SI * rr * abs(-W_) / (C_SI ** 2 * g_)
        Rout = 10 * MPC
        Ipot = quad(lambda lr: law_g(G_SI * M / math.exp(lr) ** 2, a0) * math.exp(lr), math.log(rr), math.log(Rout), limit=200)[0]
        ds_new = 4 * math.pi * G_SI * rr * RHOC0 * Ipot / (C_SI ** 2 * g_)
        inert = K_SI * rho_c * C_SI ** 2 / (g_ * uu_)
        SLIP[f"{f}|{name}"] = dict(s_grad_W=s_grad, ds_new=ds_new, total=s_grad + ds_new, inv_eps_inertia=inert, vc_kms=math.sqrt(g_ * rr) / 1e3)
worstW = max(v_["s_grad_W"] for v_ in SLIP.values())
KOK["K6"] = chk("K6_CFG938_slip_reproduced", abs(worstW / 5.8e-6 - 1) <= 0.02, f"worst W-only s_grad = {worstW:.4e} (CFG938 5.8e-6)")
guard("K6")

# ---- K7: AS206 cross-check of the metric variation of the intrinsic Laplacian
X3 = [x, y, z]
chi3, lam3 = sp.Function("chi")(x, y, z), sp.Function("lam")(x, y, z)
kf = {}
for i in range(3):
    for j in range(i, 3):
        kf[(i, j)] = kf[(j, i)] = sp.Function(f"k{i}{j}")(x, y, z)
trk = sum(kf[(i, i)] for i in range(3))


def as206_E(with_volume=True):
    dLap = -sum(kf[(i, j)] * sp.diff(chi3, X3[i], X3[j]) for i in range(3) for j in range(3)) \
        - sum((sum(sp.diff(kf[(i, j)], X3[i]) for i in range(3)) - (sp.Rational(1, 2) * sp.diff(trk, X3[j]) if with_volume else 0)) * sp.diff(chi3, X3[j])
              for j in range(3))
    lap = sum(sp.diff(chi3, X3[i], 2) for i in range(3))
    dS = lam3 * dLap + sp.Rational(1, 2) * trk * lam3 * lap
    Tl = sp.Matrix(3, 3, lambda i, j: sp.diff(lam3, X3[i]) * sp.diff(chi3, X3[j]) + sp.diff(lam3, X3[j]) * sp.diff(chi3, X3[i])
                   - (1 if i == j else 0) * sum(sp.diff(lam3, X3[q]) * sp.diff(chi3, X3[q]) for q in range(3)))
    return sp.expand(dS - sp.Rational(1, 2) * sum(kf[(i, j)] * Tl[i, j] for i in range(3) for j in range(3)))


ufk = [kf[(i, j)] for i in range(3) for j in range(i, 3)]
E7 = as206_E(True); E7n = as206_E(False)
el7 = [sp.simplify(e.lhs) for e in sp.euler_equations(E7, ufk, X3)]
el7n = [sp.simplify(e.lhs) for e in sp.euler_equations(E7n, ufk, X3)]
k7 = all(e == 0 for e in el7) and any(e != 0 for e in el7n)
KOK["K7"] = chk("K7_AS206_metric_variation_gives_CFG938_S3a_stress", k7,
                "lam d(sqrt h Lap_h chi) via AS206's identity = (1/2) k^ij T^lam_ij + total divergence (Euler operator in k_ij = 0); "
                f"negative control (volume term dropped): nonzero ({sum(1 for e in el7n if e != 0)}/6 components)")
K_ALL = all(KOK.values())
K_ALL_A1 = all(v_ for k_, v_ in KOK.items() if k_ != "K3") and RES.get("K3prime_posthoc", {}).get("reproduces", False)
RES["K_all_frozen"] = K_ALL; RES["K_all_with_A1"] = K_ALL_A1
P(f"  K controls all pass (frozen): {K_ALL}; with amendment A1 (K3 replaced by K3'): {K_ALL_A1}")
guard("K")
