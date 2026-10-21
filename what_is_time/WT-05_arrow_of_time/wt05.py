"""WT-05: the arrow of time in the cold-energy dynamics.
Criteria: FROZEN_CRITERIA.md (c4b3626f73; amendment A1 8051303f39 pre-result; A2 9cac89ddad post-smoke, pre-graded-result).
Run:  OMP_NUM_THREADS=1 nice -n 10 python3 wt05.py            -> wt05.out, wt05_results.json
      WT05_MUTATE=1 OMP_NUM_THREADS=1 nice -n 10 python3 wt05.py -> wt05_MUTATE.out, wt05_results_MUTATE.json
Readings: R1 = CFG638 OU velocity relaxation (drift off); R2 = CFG955 K-T (BGK to M[rho,u,T_J]); R3 = CFG638 full (drift + OU).
kappa = 1/2 FITTED; footings never pooled; cold energy is gravitating mass, no particle species; not theory closed."""
import os, sys, json, math, time, resource
os.environ.setdefault("OMP_NUM_THREADS", "1")
import numpy as np
import sympy as sp
from scipy.integrate import solve_ivp, quad
from scipy.interpolate import PchipInterpolator
from scipy.optimize import minimize
from scipy.special import erf

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
MUT = os.environ.get("WT05_MUTATE", "0") == "1"
TAG = "_MUTATE" if MUT else ""
OUT = []
T_START = time.time()
TOTAL_CAP = 45 * 60
RUN_CAP = 300.0


def P(s=""):
    print(s, flush=True)
    OUT.append(str(s))


def rss_mb():
    r = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    return r / (1024 * 1024) if sys.platform == "darwin" else r / 1024


def guard():
    if rss_mb() > 1000:
        P(f"RSS GUARD: {rss_mb():.0f} MB > 1 GB, abort"); dump({}, final=False); sys.exit(4)
    if time.time() - T_START > TOTAL_CAP:
        P("TOTAL WALL CAP reached, abort"); dump({}, final=False); sys.exit(4)


RES = dict(lane="WT-05", criteria="c4b3626f73", amendment_A1="8051303f39", amendment_A2="9cac89ddad", mutate=MUT)


def dump(extra, final=True):
    RES.update(extra)
    RES["peak_rss_MB"] = rss_mb(); RES["wall_s"] = time.time() - T_START
    with open(os.path.join(HERE, f"wt05_results{TAG}.json"), "w") as fh:
        json.dump(RES, fh, indent=1, default=lambda o: float(o) if isinstance(o, (np.floating,)) else (int(o) if isinstance(o, np.integer) else str(o)))
    with open(os.path.join(HERE, f"wt05{TAG}.out"), "w") as fh:
        fh.write("\n".join(OUT) + "\n")


# =====================================================================================================================
# Part 1: sympy (S1-S9, K2)
# =====================================================================================================================
def sympy_checks():
    ok, info = {}, {}
    x, v, t = sp.symbols('x v t', real=True)
    # ---- S1 Liouville: C'(f)(v f_x - Phi' f_v) = d_x(v C) - d_v(Phi' C), so Vlasov conserves int C(f) for every C, Phi
    f = sp.Function('f')(x, v); Phi = sp.Function('Phi')(x)
    fs = sp.Symbol('fs', positive=True); q = sp.Symbol('q', positive=True)
    good = True
    for C in (-fs * sp.log(fs), -fs ** 2, -fs ** q):
        Cf = C.subs(fs, f)
        lhs = sp.diff(v * Cf, x) - sp.diff(sp.diff(Phi, x) * Cf, v)
        rhs = sp.diff(C, fs).subs(fs, f) * (v * sp.diff(f, x) - sp.diff(Phi, x) * sp.diff(f, v))
        good &= sp.simplify(lhs - rhs) == 0
    ok['S1_liouville'] = bool(good)
    # ---- S2 BGK Clausius: matched rho,u: int (f-M) ln M = -(1/T) int (f-M) v^2/2 ; sign lemma (a-b)(ln a - ln b) >= 0
    m0, m1, m2, If, tau, T, u, rho = sp.symbols('m0 m1 m2 I_f tau T u rho', real=True)
    a_ = sp.log(rho / sp.sqrt(2 * sp.pi * T)) - u ** 2 / (2 * T); b_ = u / T; c_ = -1 / (2 * T)
    int_fM_lnM = (a_ * m0 + b_ * m1 + c_ * m2).subs({m0: 0, m1: 0})
    sdot = If / tau; qr = -m2 / 2 / tau                      # sdot = (1/tau) int (f-M) ln f ; q = -(1/tau) int (f-M) v^2/2
    target = (If - int_fM_lnM) / tau                          # (1/tau) int (f-M)(ln f - ln M)
    s_ = sp.Symbol('s', real=True)
    lemma = sp.solveset(sp.Lt((sp.exp(s_) - 1) * s_, 0), s_, sp.S.Reals) == sp.S.EmptySet
    ok['S2_bgk_clausius'] = bool(sp.simplify(int_fM_lnM + m2 / (2 * T)) == 0 and sp.simplify(sdot - qr / T - target) == 0 and lemma)
    # ---- S3 OU Clausius: -C ln f - (C v^2/2)/T = (g/T) J^2/f + (g u/T) J + d_v[...], J=(v-u)f + T f_v, int J dv = 0
    g_ = sp.Symbol('gamma', positive=True); Tp = sp.Symbol('T', positive=True); uu = sp.Symbol('u', real=True)
    fv = sp.Function('f')(v)
    J = (v - uu) * fv + Tp * sp.diff(fv, v); Cop = g_ * sp.diff(J, v)
    lhs = -Cop * sp.log(fv) - (Cop * v ** 2 / 2) / Tp
    Gt = -g_ * J * sp.log(fv) - (g_ / Tp) * J * v ** 2 / 2
    rhs = (g_ / Tp) * J ** 2 / fv + (g_ * uu / Tp) * J + sp.diff(Gt, v)
    ok['S3_ou_clausius'] = bool(sp.simplify(sp.expand(lhs - rhs)) == 0)
    # ---- S4 T-parity: g(x,v,t) = f(x,-v,-t); term[g] = p * term[f](x,-v,-t); T-even iff p = -1 (same as d_t)
    A = sp.symbols('A1:8', real=True); B = sp.symbols('B1:5', real=True); Cc = sp.symbols('C1:3', real=True); D = sp.symbols('D1:4', real=True)
    gam, TJ, al = sp.symbols('gamma T_J alpha', positive=True)
    fe = sp.exp(-v ** 2 + A[0] * v + A[1] * x * v + A[2] * t * v + A[3] * t + A[4] * x ** 2 + A[5] * v ** 3 * t + A[6] * x * t)
    Ue = B[0] + B[1] * x + B[2] * t + B[3] * x * t
    Phe = Cc[0] * x ** 2 + Cc[1] * x ** 3
    Vse = D[0] + D[1] * x + D[2] * t
    Re = sp.exp(x * D[0] + t * D[1])                                   # a density field rho(x,t)
    refl = {v: -v, t: -t}

    def terms(ff, U, Vs, rh):
        Mx = rh / sp.sqrt(2 * sp.pi * TJ) * sp.exp(-(v - U) ** 2 / (2 * TJ))
        return {"d_t f": sp.diff(ff, t), "v d_x f": v * sp.diff(ff, x), "-Phi' d_v f": -sp.diff(Phe, x) * sp.diff(ff, v),
                "drift d_x(v_s f)": sp.diff(Vs * ff, x),
                "OU -gamma d_v[(v-u)f + T d_v f]": -gam * sp.diff((v - U) * ff + TJ * sp.diff(ff, v), v),
                "BGK (f - M)/tau": (ff - Mx) / tau}
    tf = terms(fe, Ue, Vse, Re)
    ge = fe.subs(refl, simultaneous=True)
    tg = terms(ge, -Ue.subs(t, -t), Vse.subs(t, -t), Re.subs(t, -t))
    par = {}
    for k in tf:
        fr = tf[k].subs(refl, simultaneous=True)
        if sp.simplify(tg[k] + fr) == 0:
            par[k] = -1
        elif sp.simplify(tg[k] - fr) == 0:
            par[k] = +1
        else:
            par[k] = 0
    info['S4_parity'] = {k: ("T-even (reversible)" if p == -1 else ("T-odd (irreversible)" if p == 1 else "mixed")) for k, p in par.items()}
    ok['S4_parity_as_expected'] = (par["d_t f"] == -1 and par["v d_x f"] == -1 and par["-Phi' d_v f"] == -1
                                   and par["drift d_x(v_s f)"] == 1 and par["OU -gamma d_v[(v-u)f + T d_v f]"] == 1
                                   and par["BGK (f - M)/tau"] == 1)
    # ---- S5 cooling counterexample: S of a 1-D Maxwellian and -int M^q rise with T
    vv = sp.Symbol('v', real=True); Tt = sp.Symbol('T', positive=True); rr = sp.Symbol('rho', positive=True)
    Mx = rr / sp.sqrt(2 * sp.pi * Tt) * sp.exp(-vv ** 2 / (2 * Tt))
    Smax = sp.simplify(-sp.integrate(sp.expand_log(Mx * sp.log(Mx), force=True), (vv, -sp.oo, sp.oo)))
    dS = sp.simplify(sp.diff(Smax, Tt))
    w = sp.Symbol('w', positive=True)
    Iq = sp.simplify(sp.integrate(Mx ** (1 + w), (vv, -sp.oo, sp.oo), conds='none'))
    dSq = sp.simplify(sp.diff(-Iq, Tt))
    ok['S5_cooling_lowers_S_and_casimir'] = bool(sp.simplify(dS - rr / (2 * Tt)) == 0 and dSq.is_positive)
    info['S5'] = dict(S_of_T=str(Smax), dS_dT=str(dS), dCasimir_dT=str(dSq))
    # ---- S6 drift identity (uniform T) + deficit state + super-Jeans sign
    rho_ = sp.Function('rho')(x); vs_ = sp.Function('v_s')(x); Ph_ = sp.Function('Phi')(x)
    ident = rho_ * sp.diff(vs_, x) - rho_ * vs_ * sp.diff(Ph_, x) / Tp - (-rho_ * vs_ * sp.diff(sp.log(rho_) + Ph_ / Tp, x) + sp.diff(rho_ * vs_, x))
    Phi0 = sp.Function('Phi0')(x); dPhi = sp.Function('dPhi')(x); eps, Am, tauS, Gs = sp.symbols('epsilon A tau G', positive=True)
    rph = Am * sp.exp(-Phi0 / Tp); rc = (1 - eps) * rph
    vsd = al * tauS * sp.diff(dPhi, x)                            # psi = -dPhi => v_s = -alpha tau psi' = alpha tau dPhi'
    integrand = -rc * vsd * sp.diff(sp.log(rc) + (Phi0 + dPhi) / Tp, x)
    deficit = sp.simplify(integrand + al * tauS * rc * sp.diff(dPhi, x) ** 2 / Tp)
    # coherent partner (B-REC / B-COH): drift entropy -int v_s rho_c' with v_s = alpha tau dPhi'
    sdrift_coh = sp.simplify(-vsd * sp.diff(rc, x))               # = -alpha tau dPhi' * (1-eps) rho_ph' ; dPhi'<0, rho_ph'<0 for x>0 => < 0
    kk, r0 = sp.symbols('k rho0', positive=True)
    e2 = sp.Symbol('e2', positive=True)
    dr = e2 * sp.cos(kk * x)
    psi_p = sp.diff(4 * sp.pi * Gs * e2 * sp.cos(kk * x) / kk ** 2, x)          # psi'' = -4 pi G e2 cos
    dPh_p = sp.diff(-4 * sp.pi * Gs * e2 * sp.cos(kk * x) / kk ** 2, x)          # dPhi'' = +4 pi G e2 cos
    muT_p = sp.diff(sp.log(r0 + dr), x) + dPh_p / Tp
    rate = al * tauS * (r0 + dr) * psi_p * muT_p                                 # Sdot_tot density (B-TJ) = alpha tau rho psi' muT'
    rate2 = sp.series(rate, e2, 0, 3).removeO()
    avg = sp.simplify(sp.integrate(rate2, (x, 0, 2 * sp.pi / kk)) * kk / (2 * sp.pi))
    target_sj = 2 * sp.pi * Gs * al * tauS * e2 ** 2 * (1 - 4 * sp.pi * Gs * r0 / (kk ** 2 * Tp))
    ok['S6_drift_identity'] = bool(sp.simplify(ident) == 0)
    ok['S6_deficit_negative'] = bool(deficit == 0)
    ok['S6_superJeans_sign'] = bool(sp.simplify(avg - target_sj) == 0)
    info['S6'] = dict(deficit_rate="-alpha tau int rho_c |dPhi'|^2 / T", coherent_drift_entropy=str(sdrift_coh),
                      superJeans_avg=str(avg))
    # ---- S7 fluctuation-dissipation temperatures
    info['S7'] = dict(OU="flux -gamma[(v-u) f + T_J f_v]: mobility gamma, diffusion gamma T_J -> temperature T_J",
                      drift="flux rho v_s = -alpha tau rho grad psi: mobility alpha tau, diffusion 0 -> temperature 0")
    ok['S7_fdt'] = True
    # ---- S8 boundedness of F_T: 3-D sphere unbounded below; 1-D slab bounded below
    R_, h_, M_, Sg = sp.symbols('R h M Sigma', positive=True)
    F3 = -sp.Rational(3, 5) * Gs * M_ ** 2 / R_ - Tp * 3 * M_ * sp.log(R_)
    F1 = sp.pi * Gs * Sg ** 2 * h_ / 3 - Tp * Sg * sp.log(h_)
    hstar = sp.solve(sp.diff(F1, h_), h_)[0]
    ok['S8_3D_unbounded'] = bool(sp.limit(F3, R_, 0, '+') == -sp.oo)
    ok['S8_1D_bounded'] = bool(sp.limit(F1, h_, 0, '+') == sp.oo and sp.limit(F1, h_, sp.oo) == sp.oo
                               and sp.simplify(sp.diff(F1, h_, 2).subs(h_, hstar)) .is_positive)
    info['S8'] = dict(F3="-(3/5) G M^2/R - 3 M T ln R -> -oo as R->0", F1_min_at=str(hstar))
    # ---- S9 rate elasticities
    rL, kap, cc, Mm, rad = sp.symbols('rho_L kappa c M r', positive=True)
    a0 = kap * cc * sp.sqrt(Gs * rL)
    Vf = (Gs * Mm * a0) ** sp.Rational(1, 4)
    tau_deep = 1 / sp.sqrt(4 * sp.pi * Gs * Vf ** 2 / (4 * sp.pi * Gs * rad ** 2))
    tau_newt = 1 / sp.sqrt(4 * sp.pi * Gs * a0 / (2 * sp.pi * Gs * rad))
    e_deep = sp.simplify(sp.diff(sp.log(tau_deep), rL) * rL)
    e_newt = sp.simplify(sp.diff(sp.log(tau_newt), rL) * rL)
    TJ_deep = Vf ** 2 / 2
    eT_deep = sp.simplify(sp.diff(sp.log(TJ_deep), rL) * rL)
    ok['S9_elasticities'] = bool(e_deep == -sp.Rational(1, 8) and e_newt == -sp.Rational(1, 4) and eT_deep == sp.Rational(1, 4))
    info['S9'] = dict(e_deep=str(e_deep), e_newtonian_point_mass=str(e_newt), eT_deep=str(eT_deep),
                      bound="e = -(1/4)(rho_ph/rho_m) * (dln rho_ph/dln a0); |e| <= 1/4 when that elasticity is in [1/2, 1]")
    # ---- K2: CFG638 K7 in an SIS
    Vs, alp = sp.symbols('V alpha', positive=True)
    rho_sis = Vs ** 2 / (4 * sp.pi * Gs * rad ** 2)
    tff = sp.simplify(1 / sp.sqrt(4 * sp.pi * Gs * rho_sis)); tpi = tff / (2 * alp)
    sig = Vs / sp.sqrt(2); nu = sp.simplify(sig ** 2 * tpi)
    Kn = sp.simplify(sig * tpi / rad); Re_ = sp.simplify(Vs * rad / nu)
    ok['K2_cfg638_sis'] = bool(sp.simplify(tff - rad / Vs) == 0 and sp.simplify(tpi - rad / (2 * alp * Vs)) == 0
                               and sp.simplify(Kn - sp.sqrt(2) / (4 * alp)) == 0 and sp.simplify(Re_ - 4 * alp) == 0)
    info['K2'] = dict(tau_ff=str(tff), tau_pi=str(sp.simplify(tpi)), Kn=str(Kn), Re=str(Re_))
    return ok, info


# =====================================================================================================================
# Part 2: K3 Emden thresholds (canonical 32.1, microcanonical 709)
# =====================================================================================================================
def emden_thresholds():
    def rhs(xi, y):
        return [y[1], math.exp(-y[0]) - 2 * y[1] / xi]
    xi0 = 1e-6
    sol = solve_ivp(rhs, (xi0, 400.0), [xi0 ** 2 / 6, xi0 / 3], rtol=1e-12, atol=1e-14, dense_output=True)
    xi = np.geomspace(1.0, 300.0, 300001)
    ps, dps = sol.sol(xi)
    eta = xi * dps
    Lam = (1.5 - xi * np.exp(-ps) / dps) / (xi * dps)
    i_c = int(np.argmax(eta)); i_m = int(np.argmax(Lam))
    return dict(canonical_xi=float(xi[i_c]), canonical_contrast=float(np.exp(ps[i_c])), eta_max=float(eta[i_c]),
                micro_xi=float(xi[i_m]), micro_contrast=float(np.exp(ps[i_m])), Lambda_max=float(Lam[i_m]))


# =====================================================================================================================
# Part 3: rates (part e) for CFG847's five systems and NGC 3198, both footings
# =====================================================================================================================
G_SI, MSUN, KPC, C_SI = 6.674e-11, 1.989e30, 3.0857e19, 2.99792458e8
HBAR, KB, EV = 1.054571817e-34, 1.380649e-23, 1.602176634e-19
GYR = 3.15576e16; MYR = GYR / 1e3
KAPPA, ZED = 0.5, math.sqrt(32 * math.pi / 3)
FOOT = {"canonical": 9.3603e-11, "alt": 1.1312e-10}
SYS847 = [("dwarf", 1e7, 0.3), ("MW disc", 6e10, 10.0), ("MW outer", 6e10, 100.0), ("group", 1e12, 300.0), ("cluster", 1.5e14, 1000.0)]


def law(gN, a0, kern):
    if kern == "simple":
        return 0.5 * (gN + np.sqrt(gN * gN + 4 * gN * a0))
    y = gN / a0
    return gN / (-np.expm1(-np.sqrt(y)))


def pm_mtot(r, M, a0, kern):
    gN = G_SI * M / r ** 2
    return r ** 2 * law(gN, a0, kern) / G_SI


def pm_rho(r, M, a0, kern):
    h = 1e-5
    dm = (pm_mtot(r * (1 + h), M, a0, kern) - pm_mtot(r * (1 - h), M, a0, kern)) / (2 * h * r)
    return dm / (4 * math.pi * r * r)              # rho_m = rho_ph for a point mass (r > 0)


def pm_TJ(r, M, a0, kern):
    def integrand(s):
        rp = math.exp(s)
        return pm_rho(rp, M, a0, kern) * law(G_SI * M / rp ** 2, a0, kern) * rp
    val, _ = quad(integrand, math.log(r), math.log(r) + 40, limit=400, epsabs=0, epsrel=1e-10)
    return val / pm_rho(r, M, a0, kern)


def ngc3198_profiles(a0, kern):
    d = np.genfromtxt(os.path.join(REPO, "real_research", "data", "sparc_data", "NGC3198_rotmod.dat"), comments="#")
    R = d[:, 0] * KPC; Vg, Vd, Vb = d[:, 3] * 1e3, d[:, 4] * 1e3, d[:, 5] * 1e3
    gbar = (Vg * np.abs(Vg) + 0.61 * Vd * np.abs(Vd) + 0.61 * Vb * np.abs(Vb)) / R
    mN = R ** 2 * gbar / G_SI
    mT = R ** 2 * law(gbar, a0, kern) / G_SI
    lnR = np.log(R)
    dmT = PchipInterpolator(lnR, mT).derivative()(lnR) / R
    dmN = PchipInterpolator(lnR, mN).derivative()(lnR) / R
    rho_m = dmT / (4 * math.pi * R ** 2); rho_b = dmN / (4 * math.pi * R ** 2)
    return R, rho_m, rho_b, rho_m - rho_b, gbar, mN, mT


def rate_row(rho_m, rho_ph, a0, alpha=1.0):
    tff = 1 / math.sqrt(4 * math.pi * G_SI * rho_m)
    tS = tff / (2 * alpha)
    tD = (1 / (alpha * (rho_ph / rho_m) * math.sqrt(4 * math.pi * G_SI * rho_m))) if rho_ph > 0 else float('nan')
    return tff, tS, tD


def rates():
    out = {"systems": {}, "ngc3198": {}, "tvac_Gyr": {}, "class_inputs": []}
    dlt = 1e-4
    for foot, a0 in FOOT.items():
        tvac = KAPPA * C_SI / a0
        out["tvac_Gyr"][foot] = tvac / GYR
        H_L = ZED * a0 / C_SI
        kTdS = HBAR * H_L / (2 * math.pi)
        out.setdefault("dS", {})[foot] = dict(H_Lambda=H_L, kB_TdS_J=kTdS, TdS_K=kTdS / KB)
        for kern in ("simple", "mono"):
            for name, Mb, rk in SYS847:
                r = rk * KPC; M = Mb * MSUN

                def tt(a):
                    rm = pm_rho(r, M, a, kern)
                    return rate_row(rm, rm, a)
                tff, tS, tD = tt(a0)
                tp = tt(a0 * math.sqrt(1 + dlt)); tm = tt(a0 * math.sqrt(1 - dlt))
                den = math.log(1 + dlt) - math.log(1 - dlt)
                eS = (math.log(tp[1]) - math.log(tm[1])) / den
                eD = (math.log(tp[2]) - math.log(tm[2])) / den
                TJ = pm_TJ(r, M, a0, kern)
                eT = (math.log(pm_TJ(r, M, a0 * math.sqrt(1 + dlt), kern)) - math.log(pm_TJ(r, M, a0 * math.sqrt(1 - dlt), kern))) / den
                vc = math.sqrt(law(G_SI * M / r ** 2, a0, kern) * r) / 1e3
                row = dict(r_kpc=rk, vc_kms=vc, tau_ff_Myr=tff / MYR, tS_Myr=tS / MYR, tD_Myr=tD / MYR, tS_over_tvac=tS / tvac,
                           tD_over_tvac=tD / tvac, e_tS=eS, e_tD=eD, T_J_m2s2=TJ, e_TJ=eT, efolds_10Gyr=10 * GYR / tS,
                           m_star_kg=kTdS / TJ, m_star_eV=kTdS / TJ * C_SI ** 2 / EV)
                out["systems"][f"{foot}|{kern}|{name}"] = row
                if kern == "simple":
                    out["class_inputs"].append((f"{foot}|{name}", eS, tS / tvac, eD, tD / tvac))
            # NGC 3198
            R, rm, rb, rp, gbar, mN, mT = ngc3198_profiles(a0, kern)
            Rp, rmp, rbp, rpp, *_ = ngc3198_profiles(a0 * math.sqrt(1 + dlt), kern)
            Rm, rmm, rbm, rpm, *_ = ngc3198_profiles(a0 * math.sqrt(1 - dlt), kern)
            den = math.log(1 + dlt) - math.log(1 - dlt)
            rows, skipped_S, skipped_D = [], [], []
            for i in range(len(R)):
                if rm[i] <= 0 or rmp[i] <= 0 or rmm[i] <= 0:
                    skipped_S.append(float(R[i] / KPC)); continue
                tff, tS, tD = rate_row(rm[i], rp[i], a0)
                eS = (math.log(rate_row(rmp[i], rpp[i], a0)[1]) - math.log(rate_row(rmm[i], rpm[i], a0)[1])) / den
                okD = rp[i] > 0 and rpp[i] > 0 and rpm[i] > 0
                eD = ((math.log(rate_row(rmp[i], rpp[i], a0)[2]) - math.log(rate_row(rmm[i], rpm[i], a0)[2])) / den) if okD else float('nan')
                if not okD:
                    skipped_D.append(float(R[i] / KPC))
                rows.append(dict(r_kpc=float(R[i] / KPC), rho_ph_over_rho_m=float(rp[i] / rm[i]), tau_ff_Myr=tff / MYR, tS_Myr=tS / MYR,
                                 tD_Myr=tD / MYR, tS_over_tvac=tS / tvac, tD_over_tvac=tD / tvac, e_tS=eS, e_tD=eD))
                if kern == "simple":
                    out["class_inputs"].append((f"{foot}|NGC3198|{R[i] / KPC:.2f}", eS, tS / tvac, eD if okD else None,
                                                (tD / tvac) if okD else None))
            out["ngc3198"][f"{foot}|{kern}"] = dict(rows=rows, skipped_tS_radii_kpc=skipped_S, skipped_tD_radii_kpc=skipped_D)
    return out


def rate_class(inp, which):
    es, rs = [], []
    for row in inp:
        e, r = (row[1], row[2]) if which == "tS" else (row[3], row[4])
        if e is None or (isinstance(e, float) and math.isnan(e)):
            continue
        es.append(e); rs.append(r)
    es, rs = np.array(es), np.array(rs)
    local = bool(np.all(np.abs(es) <= 0.30) and np.all(rs <= 0.1))
    vac = bool(np.all(np.abs(es + 0.5) <= 0.1))
    cls = "RATE LOCAL" if local else ("RATE VACUUM-SET" if vac else "MIXED")
    return dict(cls=cls, n=int(len(es)), e_min=float(es.min()), e_max=float(es.max()), ratio_max=float(rs.max()),
                n_abs_e_gt_0p30=int(np.sum(np.abs(es) > 0.30)), n_e_within_0p1_of_minus_half=int(np.sum(np.abs(es + 0.5) <= 0.1)))


# =====================================================================================================================
# Part 4: the 1-D self-gravitating phase-space toy
# =====================================================================================================================
GT = 1.0
ALPHA = 1.0


class Toy:
    def __init__(self, variant, N=512):
        self.variant = variant
        self.Lx = 32.0; self.Nx = N; self.dx = 2 * self.Lx / N
        self.x = -self.Lx + (np.arange(N) + 0.5) * self.dx
        self.Sb = 1.0 if variant == "N" else 0.0; self.wb = 0.5; self.Sph = 5.364; self.H = 2.0
        x = self.x
        self.rho_b = (self.Sb / (math.sqrt(2 * math.pi) * self.wb)) * np.exp(-x ** 2 / (2 * self.wb ** 2)) if self.Sb > 0 else np.zeros(N)
        self.rho_ph = (self.Sph / (2 * self.H)) / np.cosh(x / self.H) ** 2
        # T_J: untruncated Jeans temperature of rho_ph in the target field (baryons + rho_ph)
        X = np.linspace(0.0, 80.0, 800001)
        rph = (self.Sph / (2 * self.H)) / np.cosh(X / self.H) ** 2
        gt = 2 * math.pi * GT * (self.Sb * erf(X / (math.sqrt(2) * self.wb)) + self.Sph * np.tanh(X / self.H))
        integ = rph * gt
        seg = 0.5 * (integ[1:] + integ[:-1]) * np.diff(X)
        I = np.concatenate([np.cumsum(seg[::-1])[::-1], [0.0]])     # reverse cumulative sum (no cancellation in the tail)
        Tn = I / rph
        self.TJ_numeric = np.interp(np.abs(x), X, Tn)
        if variant == "U":
            self.Tuni = math.pi * GT * self.Sph * self.H
            self.TJ = np.full(N, self.Tuni)
        else:
            self.Tuni = None
            self.TJ = self.TJ_numeric.copy()
        self.V = 7 * math.sqrt(2 * float(self.TJ.max()))
        self.Nv = N; self.dv = 2 * self.V / N
        self.v = -self.V + (np.arange(N) + 0.5) * self.dv
        rho0 = (self.Sb / (math.sqrt(2 * math.pi) * self.wb) if self.Sb > 0 else 0.0) + self.Sph / (2 * self.H)
        self.tau_ff0 = 1 / math.sqrt(4 * math.pi * GT * rho0)
        self.dt = 0.02 * self.tau_ff0
        self.rmask = np.abs(x) < 12.0
        self.dmask = np.abs(x) < 8.0
        self.rcols = np.where(self.rmask)[0]
        self.Dabs = np.abs(x[:, None] - x[None, :])
        self.Phib = 2 * math.pi * GT * self.Sb * (x * erf(x / (math.sqrt(2) * self.wb)) + self.wb * math.sqrt(2 / math.pi) * np.exp(-x ** 2 / (2 * self.wb ** 2)))
        self.gb = -2 * math.pi * GT * self.Sb * erf(x / (math.sqrt(2) * self.wb))

    # ---------- moments, energies, entropies ----------
    def rho(self, f):
        return f.sum(1) * self.dv

    def field(self, rho):
        m = rho * self.dx; cum = np.cumsum(m); Ml = cum - m / 2; Mt = cum[-1]
        return -2 * math.pi * GT * (2 * Ml - Mt) + self.gb

    def W(self, rho):
        m = rho * self.dx
        with np.errstate(all='ignore'):                    # macOS BLAS raises spurious FP flags in matmul; value checked finite
            w = float(np.sum(m * self.Phib) + 0.5 * 2 * math.pi * GT * np.dot(m, np.dot(self.Dabs, m)))
        if not math.isfinite(w):
            raise FloatingPointError("W not finite")
        return w

    def K(self, f):
        return float(np.sum(f * self.v[None, :] ** 2 / 2) * self.dx * self.dv)

    def S(self, f):
        fp = f[f > 0]
        return float(-np.sum(fp * np.log(fp)) * self.dx * self.dv)

    def S2(self, f):
        return float(-np.sum(f * f) * self.dx * self.dv)

    def mass(self, f):
        return float(np.sum(f) * self.dx * self.dv)

    def maxw(self, rho, u, T):
        v = self.v[None, :]
        us = np.array(u, dtype=float).copy()
        for _ in range(4):
            E = np.exp(-(v - us[:, None]) ** 2 / (2 * T[:, None]))
            Z = E.sum(1); m = (E * v).sum(1) / Z
            us = us + (u - m)
        E = np.exp(-(v - us[:, None]) ** 2 / (2 * T[:, None])); Z = E.sum(1)
        return rho[:, None] * E / (Z[:, None] * self.dv)

    def local_mom(self, fc):
        rho = fc.sum(1) * self.dv
        u = np.where(rho > 0, (fc * self.v[None, :]).sum(1) * self.dv / np.maximum(rho, 1e-300), 0.0)
        return rho, u

    def KL_cols(self, f):
        fc = f[self.rcols]; rho, u = self.local_mom(fc)
        M = self.maxw(rho, u, self.TJ[self.rcols])
        with np.errstate(divide='ignore', invalid='ignore'):
            t = np.where(fc > 0, fc * np.log(fc / M), 0.0)
        return t.sum(1) * self.dv * self.dx           # per column, KL in nats (mass-weighted)

    def psi_prime(self, rho):
        D = (self.rho_ph - rho) * self.dmask
        m = D * self.dx; cum = np.cumsum(m); Ml = cum - m / 2; Dt = cum[-1]
        return 2 * math.pi * GT * (2 * Ml - Dt)

    def Fpsi(self, rho):
        pp = self.psi_prime(rho)
        return float(np.sum(pp * pp) * self.dx / (8 * math.pi * GT))

    # ---------- Vlasov sub-steps: conservative positive flux-form semi-Lagrangian, van Leer, periodic ----------
    @staticmethod
    def shift_rows(F, s, block=64):
        """Row-blocked wrapper (identical arithmetic; caps temporaries for the 1 GB RSS rule)."""
        out = np.empty_like(F)
        for i0 in range(0, F.shape[0], block):
            out[i0:i0 + block] = Toy._shift_block(F[i0:i0 + block], s[i0:i0 + block])
        return out

    @staticmethod
    def _shift_block(F, s):
        N = F.shape[1]
        n = np.floor(s).astype(np.int64); th = (s - n)[:, None]
        a = np.roll(F, -1, axis=1) - F; b = F - np.roll(F, 1, axis=1)
        ab = a * b
        with np.errstate(divide='ignore', invalid='ignore'):
            sig = np.where(ab > 0, 2 * ab / (a + b), 0.0)
        Rp = th * F + sig * (th * (1 - th) / 2)
        Lp = F - Rp
        idx = (np.arange(N)[None, :] - n[:, None]) % N
        return np.take_along_axis(Lp, idx, axis=1) + np.take_along_axis(Rp, (idx - 1) % N, axis=1)

    def stream(self, f, dt):
        return self.shift_rows(f.T, self.v * dt / self.dx).T

    def kick(self, f, dt):
        g = self.field(self.rho(f))
        return self.shift_rows(f, g * dt / self.dv)

    # ---------- dissipative sub-steps ----------
    def tauff(self, rho):
        return 1 / np.sqrt(4 * math.pi * GT * (self.rho_b + rho))

    def bgk(self, f, anti=False):
        c = self.rcols; fc = f[c]; rho, u = self.local_mom(fc)
        M = self.maxw(rho, u, self.TJ[c])
        tau = 1 / np.sqrt(4 * math.pi * GT * (self.rho_b[c] + rho)) / (2 * ALPHA)        # T1: tau_ff/(2 alpha)
        lam = np.exp((+1 if anti else -1) * self.dt / tau)
        fn = M + (fc - M) * lam[:, None]
        q = ((fn - fc) * self.v[None, :] ** 2 / 2).sum(1) * self.dv / self.dt
        def colS(F):
            with np.errstate(divide='ignore', invalid='ignore'):
                return -np.where(F > 0, F * np.log(np.where(F > 0, F, 1.0)), 0.0).sum(1) * self.dv * self.dx
        dS_col = colS(fn) - colS(fc)
        f = f.copy(); f[c] = fn
        return f, q, dS_col

    def ou(self, f, Tfac=1.0):
        c = self.rcols; fc = f[c]; rho, u = self.local_mom(fc)
        T = self.TJ[c] * Tfac
        gam = ALPHA * np.sqrt(4 * math.pi * GT * (self.rho_b[c] + rho))      # alpha / tau_ff
        Vp = (self.v[None, :] - u[:, None]) ** 2 / 2
        w = (Vp[:, 1:] - Vp[:, :-1]) / T[:, None]
        def Bf(z):
            with np.errstate(divide='ignore', invalid='ignore', over='ignore'):
                return np.where(np.abs(z) < 1e-8, 1 - z / 2, z / np.expm1(z))
        Bp, Bm = Bf(w), Bf(-w)
        cc = (gam * T * self.dt / self.dv ** 2)[:, None]
        nC, n = fc.shape
        diag = np.ones((nC, n)); low = np.zeros((nC, n)); up = np.zeros((nC, n))
        diag[:, :-1] += cc * Bp; diag[:, 1:] += cc * Bm
        up[:, :-1] = -cc * Bm; low[:, 1:] = -cc * Bp
        # vectorised Thomas along v (loop over n, vector over columns); arrays transposed for contiguity
        dT, lT, uT, rT = diag.T.copy(), low.T.copy(), up.T.copy(), fc.T.copy()
        cp = np.zeros_like(dT); dp = np.zeros_like(dT)
        cp[0] = uT[0] / dT[0]; dp[0] = rT[0] / dT[0]
        for j in range(1, n):
            m = dT[j] - lT[j] * cp[j - 1]
            cp[j] = uT[j] / m
            dp[j] = (rT[j] - lT[j] * dp[j - 1]) / m
        xs = np.zeros_like(dT); xs[-1] = dp[-1]
        for j in range(n - 2, -1, -1):
            xs[j] = dp[j] - cp[j] * xs[j + 1]
        fn = xs.T
        q = ((fn - fc) * self.v[None, :] ** 2 / 2).sum(1) * self.dv / self.dt
        f = f.copy(); f[c] = fn
        return f, q

    def drift(self, f, sign=1.0):
        rho = self.rho(f)
        pp = self.psi_prime(rho)
        vs = -ALPHA * self.tauff(rho) * pp * self.dmask * sign
        vcap = 0.5 * self.dx / self.dt                    # A2.1: CFG544's limiter |v_s dt| <= 0.5 bin width
        lim = np.abs(vs) > vcap
        lim_frac = float(np.sum(rho[lim & self.dmask]) / max(np.sum(rho[self.dmask]), 1e-300))
        vs = np.clip(vs, -vcap, vcap)
        g = self.field(rho)
        qd = -rho * vs * g                               # rho_c v_s d_x Phi (energy into matter per length per time)
        W0 = self.W(rho)
        vf = 0.5 * (vs + np.roll(vs, -1))               # face i+1/2
        vmax = float(np.max(np.abs(vf)))
        nsub = max(1, int(math.ceil(vmax * self.dt / (0.25 * self.dx))))   # CFL 0.25 (frozen: <= 0.5)
        dts = self.dt / nsub
        F = f.copy()
        nu = vf * dts / self.dx
        for _ in range(nsub):
            a = np.roll(F, -1, axis=0) - F; b = F - np.roll(F, 1, axis=0)
            ab = a * b
            with np.errstate(divide='ignore', invalid='ignore'):
                sig = np.where(ab > 0, 2 * ab / (a + b), 0.0)
            fL = F + 0.5 * sig * (1 - nu[:, None])                          # upwind value from cell i (v_f > 0)
            Fr = np.roll(F, -1, axis=0); sr = np.roll(sig, -1, axis=0)
            fR = Fr - 0.5 * sr * (1 + nu[:, None])                          # from cell i+1 (v_f < 0); 1 - |nu| = 1 + nu
            ff = np.where(vf[:, None] > 0, fL, fR)
            flux = nu[:, None] * ff
            F = F - (flux - np.roll(flux, 1, axis=0))
        dW = self.W(self.rho(F)) - W0
        return F, qd, dW, nsub, float(F.min()), lim_frac

    # ---------- initial conditions ----------
    def ic(self, name):
        x = self.x
        rho = self.rho_ph.copy(); u = np.zeros_like(x); T = self.TJ.copy()
        if name == "IC-H":
            T = 2 * self.TJ
        elif name == "IC-C":
            T = 0.25 * self.TJ
        elif name == "IC-E":
            pass
        elif name == "IC-U":
            u = 0.5 * math.sqrt(self.TJ[np.argmin(np.abs(x))]) * np.sin(math.pi * x / (2 * self.H)) * np.exp(-x ** 2 / (8 * self.H ** 2))
        elif name == "IC-D":
            rho = 0.7 * self.rho_ph
        elif name == "IC-O":
            rho = 1.3 * self.rho_ph
        else:
            raise ValueError(name)
        return self.maxw(rho, u, T)


# ------------------------------------------------------------------------------------------------------------------
def largest_drop(arr):
    a = np.asarray(arr, dtype=float)
    if a.size < 2:
        return 0.0
    run = np.maximum.accumulate(a)
    return float(np.max(run - a))


def largest_rise(arr):
    return largest_drop(-np.asarray(arr, dtype=float))


def run_toy(toy, icname, reading, legs=1, t_legs=10.0, mut=None, record_every=1, label=""):
    """reading: CTRL | BGK | OU | OUD (OU + drift).  mut: None | 'anti' | 'fdt2' | 'driftflip'."""
    t0 = time.time()
    f = toy.ic(icname); f0 = f.copy()
    M0 = toy.mass(f); E0 = toy.K(f) + toy.W(toy.rho(f)); S0 = toy.S(f)
    nsteps = int(round(t_legs * toy.tau_ff0 / toy.dt))
    TJr = toy.TJ[toy.rcols]; TJd = toy.TJ
    SR_TJ = 0.0; SR_REC = 0.0; Qnet = 0.0; vlasov_abs = 0.0
    ser = {k: [] for k in ("t", "S", "S2", "KL", "Fpsi", "Fv", "E", "SR_TJ", "SR_REC", "Qnet", "release", "vabs", "vabs2")}
    vlasov_abs2 = 0.0
    k5_min = float('inf'); drift_info = dict(nsub_max=0, fmin=0.0, dW_vs_qd=[], lim=[])
    neg_mass = 0.0; capped = False; tcur = 0.0; nrec = 0

    def record(release):
        rho = toy.rho(f)
        ser["t"].append(tcur / toy.tau_ff0); ser["S"].append(toy.S(f)); ser["S2"].append(toy.S2(f))
        if reading == "CTRL":                          # Vlasov-only controls: KL bookkeeping not used by any rule (memory)
            ser["KL"].append(float('nan')); ser["Fv"].append(float('nan'))
        else:
            klc = toy.KL_cols(f)
            ser["KL"].append(float(klc.sum())); ser["Fv"].append(float(np.sum(TJr * klc)))
        ser["Fpsi"].append(toy.Fpsi(rho)); ser["E"].append(toy.K(f) + toy.W(rho))
        ser["SR_TJ"].append(SR_TJ); ser["SR_REC"].append(SR_REC); ser["Qnet"].append(Qnet); ser["release"].append(release)
        ser["vabs"].append(vlasov_abs); ser["vabs2"].append(vlasov_abs2)
    record(True)
    S_leg1 = None
    for leg in range(legs):
        if leg == 1:
            S_leg1 = toy.S(f)
            f = f[:, ::-1].copy()
        for step in range(nsteps):
            Sb = toy.S(f); S2b = toy.S2(f)
            f = toy.stream(f, toy.dt / 2); f = toy.kick(f, toy.dt); f = toy.stream(f, toy.dt / 2)
            vlasov_abs += abs(toy.S(f) - Sb); vlasov_abs2 += abs(toy.S2(f) - S2b)
            release = False
            thr = -1e-12 * abs(E0)
            if reading == "OUD":
                f, qd, dW, nsub, fmin, lf = toy.drift(f, sign=(-1.0 if mut == "driftflip" else 1.0))
                drift_info["lim"].append(lf)
                drift_info["nsub_max"] = max(drift_info["nsub_max"], nsub); drift_info["fmin"] = min(drift_info["fmin"], fmin)
                inc = float(np.sum((qd / TJd)[toy.dmask]) * toy.dx * toy.dt)
                SR_TJ -= inc
                Qnet += dW
                qsum = float(np.sum(qd) * toy.dx * toy.dt)
                if abs(qsum) > 1e-14:
                    drift_info["dW_vs_qd"].append(dW / qsum)
                if np.any(qd * toy.dx * toy.dt < thr):
                    release = True
            if reading == "BGK":
                Sb2 = toy.S(f)
                f, q, dS_col = toy.bgk(f, anti=(mut == "anti"))
                k5 = dS_col - q * toy.dt * toy.dx / TJr
                k5_min = min(k5_min, float(k5.min()))
                inc = float(np.sum(q / TJr) * toy.dx * toy.dt)
                SR_TJ -= inc; SR_REC -= inc
                Qnet += float(np.sum(q) * toy.dx * toy.dt)
                if np.any(q * toy.dx * toy.dt < thr):
                    release = True
                if mut == "anti":
                    neg_mass = max(neg_mass, float(-np.sum(np.minimum(f, 0)) * toy.dx * toy.dv))
            if reading in ("OU", "OUD"):
                f, q = toy.ou(f, Tfac=(2.0 if mut == "fdt2" else 1.0))
                inc = float(np.sum(q / TJr) * toy.dx * toy.dt)
                SR_TJ -= inc; SR_REC -= inc
                Qnet += float(np.sum(q) * toy.dx * toy.dt)
                if np.any(q * toy.dx * toy.dt < thr):
                    release = True
            tcur += toy.dt
            nrec += 1
            if nrec % record_every == 0 or step == nsteps - 1:
                record(release)
            if mut == "anti" and neg_mass > 1e-3 * M0:
                break
            if time.time() - t0 > RUN_CAP:
                capped = True; break
            if step % 50 == 0:
                guard()
        if capped or (mut == "anti" and neg_mass > 1e-3 * M0):
            break
    S = np.array(ser["S"]); eps_num = vlasov_abs + 1e-10 * M0
    out = dict(TJmax=float(toy.TJ.max()), label=label, variant=toy.variant, ic=icname, reading=reading, mut=mut, legs=legs, capped=capped,
               t_reached=tcur / toy.tau_ff0, steps=nrec, wall_s=time.time() - t0, M0=M0, E0=E0, S0=S0,
               mass_rel_err=abs(toy.mass(f) - M0) / M0, E_err_max=float(np.max(np.abs(np.array(ser["E"]) - E0))),
               eps_num=eps_num, vlasov_abs_dS=vlasov_abs, K5_min=(k5_min if reading == "BGK" else None),
               edge_mass=float(np.sum(f[np.abs(toy.x) > 30]) * toy.dx * toy.dv),
               drift=(dict(nsub_max=drift_info["nsub_max"], fmin=drift_info["fmin"], limited_mass_frac_mean=(float(np.mean(drift_info["lim"])) if drift_info["lim"] else None), limited_mass_frac_max=(float(np.max(drift_info["lim"])) if drift_info["lim"] else None),
                           dW_over_qd_median=(float(np.median(drift_info["dW_vs_qd"])) if drift_info["dW_vs_qd"] else None)) if reading == "OUD" else None),
               neg_mass=neg_mass, S_end_leg1=(S_leg1 if S_leg1 is not None else toy.S(f)))
    Stj = S + np.array(ser["SR_TJ"]); Src = S + np.array(ser["SR_REC"])
    out["drops"] = dict(S=largest_drop(S), S2=largest_drop(ser["S2"]), S_TJ=largest_drop(Stj), S_REC=largest_drop(Src))
    # POST HOC (added after run 1; no class weight): windowed rule, drop within a window vs 10x the Vlasov |dS| accumulated in it
    Vc = np.array(ser["vabs"]); Vc2 = np.array(ser["vabs2"])
    out["posthoc_windowed"] = dict(S=largest_drop(S + 10 * Vc), S2=largest_drop(np.array(ser["S2"]) + 10 * Vc2),
                                   S_TJ=largest_drop(Stj + 10 * Vc), S_REC=largest_drop(Src + 10 * Vc))
    out["vlasov_abs_dS2"] = vlasov_abs2
    out["rises"] = dict(KL=largest_rise(ser["KL"]), Fpsi=largest_rise(ser["Fpsi"]), Fpsi_Fv=largest_rise(np.array(ser["Fpsi"]) + np.array(ser["Fv"])))
    out["start"] = dict(KL=ser["KL"][0], Fpsi=ser["Fpsi"][0], Fv=ser["Fv"][0], W=toy.W(toy.rho(f0)))
    out["maxval"] = dict(KL=float(np.max(ser["KL"])), Fpsi=float(np.max(ser["Fpsi"])), Fpsi_Fv=float(np.max(np.array(ser["Fpsi"]) + np.array(ser["Fv"]))))
    out["net"] = dict(dS=float(S[-1] - S[0]), dS_TJ=float(Stj[-1] - Stj[0]), dS_REC=float(Src[-1] - Src[0]))
    Q = np.array(ser["Qnet"]); out["Qnet_max_rise"] = float(np.max(Q - np.minimum.accumulate(Q)))
    # B-SPLIT: zero-release intervals of >= 5 recorded steps, largest S drop inside one
    rel = np.array(ser["release"]); worst = 0.0; nint = 0; i = 0
    while i < len(rel):
        if not rel[i]:
            j = i
            while j < len(rel) and not rel[j]:
                j += 1
            if j - i >= 5:
                nint += 1; worst = max(worst, largest_drop(S[max(i - 1, 0):j]))
            i = j
        else:
            i += 1
    out["split"] = dict(zero_release_intervals=nint, worst_drop_in_zero_release=worst, frac_steps_with_release=float(np.mean(rel)))
    if toy.variant == "U":
        Tu = toy.Tuni
        FT = np.array(ser["E"]) - Tu * S
        out["F_T"] = dict(rise=largest_rise(FT), start=float(FT[0]), end=float(FT[-1]),
                          L1_to_target_end=float(np.sum(np.abs(toy.rho(f) - toy.rho_ph)) * toy.dx / np.sum(toy.rho_ph * toy.dx)))
    if legs == 2:
        fb = f[:, ::-1]
        out["echo_L1"] = float(np.sum(np.abs(fb - f0)) * toy.dx * toy.dv / M0)
    # NESS slope (last 30%)
    tt = np.array(ser["t"]); n0 = int(0.7 * len(tt))
    if len(tt) - n0 > 5:
        out["late_slope_S_TJ_per_tauff0_per_M"] = float(np.polyfit(tt[n0:], Stj[n0:], 1)[0] / M0)
    out["series_end"] = dict(S=float(S[-1]), S_TJ=float(Stj[-1]), KL=float(ser["KL"][-1]), Fpsi=float(ser["Fpsi"][-1]))
    out["Fpsi_at_1tauff0_over_0"] = (float(np.interp(1.0, tt, ser["Fpsi"]) / ser["Fpsi"][0]) if ser["Fpsi"][0] > 0 else None)
    out["_series"] = {k: (np.asarray(vv, dtype=float)[::max(1, len(vv) // 200)].tolist() if k != "release" else None) for k, vv in ser.items()}
    return out


def k1_homogeneous():
    """Plain BGK and OU without gravity (single column): closed and thermostatted H-theorems."""
    res = {}
    Nv, V = 512, 30.0; dv = 2 * V / Nv; v = -V + (np.arange(Nv) + 0.5) * dv     # run 1 used V = 12: truncation (disclosed)
    f0 = 0.6 * np.exp(-(v + 2) ** 2 / (2 * 0.25)) / math.sqrt(2 * math.pi * 0.25) + 0.4 * np.exp(-(v - 3) ** 2 / 2) / math.sqrt(2 * math.pi)
    f0 = f0 / (f0.sum() * dv)

    def S(f):
        fp = f[f > 0]; return float(-np.sum(fp * np.log(fp)) * dv)

    def maxw(rho, u, T):
        us = u
        for _ in range(4):
            E = np.exp(-(v - us) ** 2 / (2 * T)); m = (E * v).sum() / E.sum(); us += (u - m)
        E = np.exp(-(v - us) ** 2 / (2 * T)); return rho * E / (E.sum() * dv)
    tau, dt = 1.0, 0.05
    for mode in ("closed", "thermo"):
        f = f0.copy(); St = S(f); worst = 0.0
        for _ in range(600):
            rho = f.sum() * dv; u = (f * v).sum() * dv / rho; Tf = ((f * (v - u) ** 2).sum() * dv) / rho
            T = Tf if mode == "closed" else 2.0
            M = maxw(rho, u, T); fn = M + (f - M) * math.exp(-dt / tau)
            q = ((fn - f) * v ** 2 / 2).sum() * dv
            Snew = S(fn); d = (Snew - S(f)) - (0.0 if mode == "closed" else q / T)
            worst = min(worst, d); f = fn
        rho = f.sum() * dv; u = (f * v).sum() * dv / rho; Tf = ((f * (v - u) ** 2).sum() * dv) / rho
        M = maxw(rho, u, Tf if mode == "closed" else 2.0)
        kl = float(np.sum(np.where(f > 0, f * np.log(f / M), 0)) * dv)
        res[f"BGK_{mode}"] = dict(min_step=worst, final_KL=kl, ok=bool(worst >= -1e-12 and kl <= 1e-6))
    # OU (Scharfetter-Gummel implicit) homogeneous
    for mode in ("closed", "thermo"):
        f = f0.copy(); worst = 0.0
        for _ in range(600):
            rho = f.sum() * dv; u = (f * v).sum() * dv / rho; Tf = ((f * (v - u) ** 2).sum() * dv) / rho
            T = Tf if mode == "closed" else 2.0
            Vp = (v - u) ** 2 / 2; w = (Vp[1:] - Vp[:-1]) / T
            Bp = np.where(np.abs(w) < 1e-8, 1 - w / 2, w / np.expm1(w)); Bm = np.where(np.abs(w) < 1e-8, 1 + w / 2, -w / np.expm1(-w))
            c = 1.0 * T * dt / dv ** 2
            A = np.zeros((Nv, Nv)); i = np.arange(Nv)
            A[i, i] = 1.0
            A[i[:-1], i[:-1]] += c * Bp; A[i[1:], i[1:]] += c * Bm
            A[i[:-1], i[1:]] = -c * Bm; A[i[1:], i[:-1]] = -c * Bp
            fn = np.linalg.solve(A, f)
            q = ((fn - f) * v ** 2 / 2).sum() * dv
            d = (S(fn) - S(f)) - (0.0 if mode == "closed" else q / T)
            worst = min(worst, d); f = fn
        rho = f.sum() * dv; u = (f * v).sum() * dv / rho; Tf = ((f * (v - u) ** 2).sum() * dv) / rho
        M = maxw(rho, u, Tf if mode == "closed" else 2.0)
        kl = float(np.sum(np.where(f > 0, f * np.log(f / M), 0)) * dv)
        res[f"OU_{mode}"] = dict(min_step=worst, final_KL=kl, ok=bool(worst >= -1e-10 and kl <= 1e-6))
    return res


def bsplit_search(toy, seed=505):
    """Instantaneous search (reported only): drawing-only drift states (q_d >= 0 in the drift region) with Sdot_drift < 0."""
    rng = np.random.default_rng(seed)
    x = toy.x; dm = toy.dmask; M0 = float(np.sum(toy.rho_ph) * toy.dx)

    def evalstate(a, b):
        ex = sum(a[k] * np.cos((k + 1) * math.pi * x / 16) for k in range(len(a)))
        ex = ex + sum(b[k] * np.sin((k + 1) * math.pi * x / 16) for k in range(len(b)))
        rho = toy.rho_ph * np.exp(np.clip(ex, -30, 30))
        pp = toy.psi_prime(rho); vs = np.clip(-ALPHA * toy.tauff(rho) * pp * dm, -0.5 * toy.dx / toy.dt, 0.5 * toy.dx / toy.dt)   # A2.1 limiter
        g = toy.field(rho); qd = -rho * vs * g
        drho = np.gradient(rho, toy.dx)
        sdot = float(-np.sum(vs * drho) * toy.dx)
        act = dm & (np.abs(vs) > 0) & (rho > 1e-12)
        scale = float(np.sum(np.abs(qd[act])) * toy.dx) + 1e-300
        viol = float(np.sum(np.maximum(0.0, -qd[act])) * toy.dx) / scale
        return sdot / M0, viol, rho
    best = []
    for i in range(5000):
        a = rng.normal(0, 0.5, 6); b = rng.normal(0, 0.5, 3) if i >= 4000 else np.zeros(0)
        sd, viol, _ = evalstate(a, b)
        best.append((sd + 1e3 * viol, sd, viol, a, b))
    best.sort(key=lambda z: z[0])
    feas = [z for z in best if z[2] <= 1e-12]
    found = []
    for z in best[:20]:
        a0, b0 = z[3], z[4]
        na = len(a0)
        def obj(p):
            sd, viol, _ = evalstate(p[:na], p[na:])
            return sd + 1e3 * viol
        r = minimize(obj, np.concatenate([a0, b0]), method="Nelder-Mead", options=dict(maxiter=1500, xatol=1e-6, fatol=1e-12))
        sd, viol, _ = evalstate(r.x[:na], r.x[na:])
        found.append((sd, viol, r.x.tolist(), na))
    fe = [z for z in found if z[1] <= 1e-12]
    return dict(n_draws=5000, n_feasible_draws=len(feas), min_sdot_feasible_draw=(min(z[1] for z in feas) if feas else None),
                min_sdot_feasible_optimised=(min(z[0] for z in fe) if fe else None),
                best_state=(min(fe, key=lambda z: z[0]) if fe else None))


# =====================================================================================================================
# Main
# =====================================================================================================================
def main():
    P("WT-05  arrow of time in the cold-energy dynamics" + ("   [MUTATE]" if MUT else ""))
    P("criteria c4b3626f73, amendments A1 8051303f39, A2 9cac89ddad.  kappa = 1/2 FITTED; footings never pooled; not theory closed.")
    if MUT:
        return mutate()
    # ---------------- sympy ----------------
    P("\n== Part 1: sympy (S1-S9, K2) ==")
    ok, info = sympy_checks()
    for k, v in ok.items():
        P(f"  {k:32s} {'PASS' if v else 'FAIL'}")
    P("  S4 T-parity:")
    for k, v in info['S4_parity'].items():
        P(f"     {k:36s} {v}")
    RES["sympy"] = dict(ok=ok, info=info)
    # ---------------- K3 ----------------
    P("\n== K3: isothermal sphere in a box (Emden) ==")
    em = emden_thresholds()
    k3 = abs(em["canonical_contrast"] / 32.1 - 1) <= 0.01 and abs(em["micro_contrast"] / 709 - 1) <= 0.01
    P(f"  canonical: xi = {em['canonical_xi']:.3f}, contrast = {em['canonical_contrast']:.2f} (eta_max {em['eta_max']:.4f});"
      f"  microcanonical: xi = {em['micro_xi']:.3f}, contrast = {em['micro_contrast']:.1f} (Lambda_max {em['Lambda_max']:.4f})  -> K3 {'PASS' if k3 else 'FAIL'}")
    RES["K3"] = dict(em, ok=bool(k3))
    # ---------------- rates ----------------
    P("\n== Part 2: rates (both footings; simple kernel graded, nu_mono reported) ==")
    rt = rates()
    for foot in FOOT:
        P(f"  [{foot}] t_vac = 1/sqrt(G rho_L) = kappa c/a0 = {rt['tvac_Gyr'][foot]:.2f} Gyr (identity);"
          f"  T_dS = {rt['dS'][foot]['TdS_K']:.3e} K")
        for name, _, _ in SYS847:
            r = rt["systems"][f"{foot}|simple|{name}"]
            P(f"     {name:9s} v_c {r['vc_kms']:7.1f} km/s  tau_ff {r['tau_ff_Myr']:8.1f} Myr  t_S {r['tS_Myr']:8.1f} Myr  t_S/t_vac {r['tS_over_tvac']:.2e}"
              f"  e_tS {r['e_tS']:+.4f}  e_tD {r['e_tD']:+.4f}  e_TJ {r['e_TJ']:+.4f}  m* {r['m_star_eV']:.1e} eV")
        rows = rt["ngc3198"][f"{foot}|simple"]["rows"]
        eS = [z["e_tS"] for z in rows]; eD = [z["e_tD"] for z in rows if not math.isnan(z["e_tD"])]
        rS = [z["tS_over_tvac"] for z in rows]
        P(f"     NGC 3198 ({len(rows)} radii): t_S {min(z['tS_Myr'] for z in rows):.1f}-{max(z['tS_Myr'] for z in rows):.1f} Myr;"
          f"  t_S/t_vac <= {max(rS):.2e};  e_tS [{min(eS):+.4f}, {max(eS):+.4f}];  e_tD [{min(eD):+.4f}, {max(eD):+.4f}]"
          f"  (t_D skipped at {len(rt['ngc3198'][f'{foot}|simple']['skipped_tD_radii_kpc'])} radii with rho_ph <= 0)")
    rcS = rate_class(rt["class_inputs"], "tS"); rcD = rate_class(rt["class_inputs"], "tD")
    P(f"  RATE CLASS (t_S, relaxation): {rcS['cls']}  e in [{rcS['e_min']:+.4f}, {rcS['e_max']:+.4f}], max t_S/t_vac {rcS['ratio_max']:.2e}")
    P(f"  RATE CLASS (t_D, drift):      {rcD['cls']}  e in [{rcD['e_min']:+.4f}, {rcD['e_max']:+.4f}], max t_D/t_vac {rcD['ratio_max']:.2e};"
      f" {rcD['n_e_within_0p1_of_minus_half']}/{rcD['n']} rows within 0.1 of -1/2")
    clk = {foot: dict(lo=(0.72 if foot == 'canonical' else 0.83) / rt['tvac_Gyr'][foot], hi=3.47 / rt['tvac_Gyr'][foot]) for foot in FOOT}
    P(f"  CFG763 formation clock / t_vac: canonical {clk['canonical']['lo']:.3f}-{clk['canonical']['hi']:.3f}; alt {clk['alt']['lo']:.3f}-{clk['alt']['hi']:.3f} (report only)")
    k6 = (abs(rt["systems"]["canonical|simple|dwarf"]["vc_kms"] - 21) <= 1 and abs(rt["systems"]["canonical|simple|cluster"]["vc_kms"] - 1314) <= 1)
    P(f"  K6 (CFG847 v_c dwarf 21, cluster 1314 km/s): {rt['systems']['canonical|simple|dwarf']['vc_kms']:.2f}, "
      f"{rt['systems']['canonical|simple|cluster']['vc_kms']:.2f} -> {'PASS' if k6 else 'FAIL'}")
    rt.pop("class_inputs")
    RES["rates"] = dict(rt, class_tS=rcS, class_tD=rcD, cfg763_over_tvac=clk); RES["K6"] = bool(k6)
    dump({})
    # ---------------- K1 ----------------
    P("\n== K1: homogeneous BGK / OU without gravity ==")
    k1 = k1_homogeneous()
    for k, v in k1.items():
        P(f"  {k:12s} min step {v['min_step']:+.2e}  final KL {v['final_KL']:.2e}  {'PASS' if v['ok'] else 'FAIL'}")
    RES["K1"] = k1
    # ---------------- toy ----------------
    P("\n== Part 3: toy (1-D self-gravitating phase space, code units, footing-free) ==")
    TN, TU = Toy("N"), Toy("U")
    for T_ in (TN, TU):
        P(f"  variant {T_.variant}: T_J range [{T_.TJ.min():.3f}, {T_.TJ.max():.3f}] (numeric untruncated [{T_.TJ_numeric[np.abs(T_.x) < 12].min():.4f}, {T_.TJ_numeric.max():.4f}]);"
          f" V = {T_.V:.2f}; dx = {T_.dx:.4f}; dv = {T_.dv:.4f}; tau_ff0 = {T_.tau_ff0:.5f}; dt = {T_.dt:.6f}")
    RES["toy_setup"] = {T_.variant: dict(TJ_min=float(T_.TJ.min()), TJ_max=float(T_.TJ.max()), V=T_.V, tau_ff0=T_.tau_ff0, dt=T_.dt,
                                         U_TJ_numeric_max_rel_dev=(float(np.max(np.abs(T_.TJ_numeric[np.abs(T_.x) < 12] / T_.Tuni - 1))) if T_.Tuni else None))
                        for T_ in (TN, TU)}
    plan = [  # (key, toy, ic, reading, legs, t)
        ("CTRL|N|IC-H|2", TN, "IC-H", "CTRL", 2, 10), ("CTRL|N|IC-C|1", TN, "IC-C", "CTRL", 1, 10), ("CTRL|N|IC-U|1", TN, "IC-U", "CTRL", 1, 10),
        ("CTRL|N|IC-E|1", TN, "IC-E", "CTRL", 1, 10), ("CTRL|N|IC-D|2", TN, "IC-D", "CTRL", 2, 10), ("CTRL|N|IC-O|1", TN, "IC-O", "CTRL", 1, 10),
        ("CTRL|U|IC-H|2", TU, "IC-H", "CTRL", 2, 10), ("CTRL|U|IC-D|1", TU, "IC-D", "CTRL", 1, 10),
        ("R2|N|IC-H|2", TN, "IC-H", "BGK", 2, 10), ("R2|N|IC-C|1", TN, "IC-C", "BGK", 1, 10), ("R2|N|IC-U|1", TN, "IC-U", "BGK", 1, 10),
        ("R2|N|IC-E|NESS", TN, "IC-E", "BGK", 1, 80), ("R2|U|IC-H|2", TU, "IC-H", "BGK", 2, 10),
        ("R1|N|IC-H|2", TN, "IC-H", "OU", 2, 10), ("R1|N|IC-C|1", TN, "IC-C", "OU", 1, 10), ("R1|N|IC-U|1", TN, "IC-U", "OU", 1, 10),
        ("R3|N|IC-D|2", TN, "IC-D", "OUD", 2, 10), ("R3|N|IC-O|1", TN, "IC-O", "OUD", 1, 10), ("R3|N|IC-U|1", TN, "IC-U", "OUD", 1, 10),
        ("R3|N|IC-H|1", TN, "IC-H", "OUD", 1, 10), ("R3|U|IC-D|1", TU, "IC-D", "OUD", 1, 10),
    ]
    runs = {}
    for key, T_, ic, rd, legs, tl in plan:
        guard()
        r = run_toy(T_, ic, rd, legs=legs, t_legs=tl, label=key, record_every=(5 if tl > 20 else 1))
        runs[key] = r
        d = r["drops"]; rs = r["rises"]
        P(f"  {key:16s} t={r['t_reached']:6.1f}{' CAPPED' if r['capped'] else ''}  wall {r['wall_s']:5.1f}s  eps_num {r['eps_num']:.2e}"
          f"  dM {r['mass_rel_err']:.1e}  dE {r['E_err_max'] / abs(r['E0']):.1e}  dS {r['net']['dS']:+.4f}"
          f"  drop[S {d['S']:.2e} S2 {d['S2']:.2e} S_TJ {d['S_TJ']:.2e} S_REC {d['S_REC']:.2e}]"
          f"  rise[KL {rs['KL']:.2e} Fpsi {rs['Fpsi']:.2e}]  Qrise {r['Qnet_max_rise']:.2e}"
          + (f"  echo {r['echo_L1']:.3f}" if 'echo_L1' in r else "") + (f"  K5 {r['K5_min']:+.1e}" if r['K5_min'] is not None else ""))
        RES.setdefault("runs", {})[key] = {k: v for k, v in r.items() if k != "_series"}
        RES.setdefault("series", {})[key] = r["_series"]
        dump({})
    # K4 resolution check
    guard()
    T2 = Toy("N", N=1024)
    hi = run_toy(T2, "IC-H", "CTRL", legs=1, t_legs=10, label="CTRL|N1024|IC-H|1")
    lo_dS = abs(runs["CTRL|N|IC-H|2"]["S_end_leg1"] - runs["CTRL|N|IC-H|2"]["S0"])
    hi_dS = abs(hi["net"]["dS"])
    ratio = hi_dS / lo_dS if lo_dS > 0 else float('nan')
    P(f"  K4 resolution: control IC-H dS(t1): 512^2 {lo_dS:.4e}, 1024^2 {hi_dS:.4e}, ratio {ratio:.3f}")
    RES["runs"]["CTRL|N1024|IC-H|1"] = {k: v for k, v in hi.items() if k != "_series"}
    del T2
    ctrl = {k: v for k, v in runs.items() if k.startswith("CTRL")}
    k4_mass = all(v["mass_rel_err"] <= 1e-12 for v in runs.values()) and hi["mass_rel_err"] <= 1e-12
    k4_edge = all(v["edge_mass"] <= 1e-6 * v["M0"] for v in runs.values())
    k4_E = all(v["E_err_max"] / abs(v["E0"]) <= 5e-3 for v in ctrl.values())
    k4_res = bool(ratio <= 0.9)
    k5 = all(v["K5_min"] >= -1e-11 * v["M0"] for k, v in runs.items() if v["K5_min"] is not None and v["mut"] is None)
    P(f"  K4: mass {'PASS' if k4_mass else 'FAIL'} (max {max(v['mass_rel_err'] for v in runs.values()):.1e}); edge {'PASS' if k4_edge else 'FAIL'}"
      f" (max {max(v['edge_mass'] / v['M0'] for v in runs.values()):.1e}); energy {'PASS' if k4_E else 'FAIL'}"
      f" (max {max(v['E_err_max'] / abs(v['E0']) for v in ctrl.values()):.1e}); resolution {'PASS' if k4_res else 'FAIL'}")
    P(f"  K5 discrete BGK Clausius: {'PASS' if k5 else 'FAIL'} (min {min(v['K5_min'] / v['M0'] for v in runs.values() if v['K5_min'] is not None):+.2e} M)")
    RES["K4"] = dict(mass=k4_mass, edge=k4_edge, energy=k4_E, resolution=k4_res, res_ratio=ratio, dS_512=lo_dS, dS_1024=hi_dS)
    RES["K5"] = bool(k5)
    # B-SPLIT search
    guard()
    bs = bsplit_search(TN)
    P(f"  B-SPLIT instantaneous search (R3, N-variant): feasible draws {bs['n_feasible_draws']}/{bs['n_draws']};"
      f" min Sdot_drift/M (draws) {bs['min_sdot_feasible_draw']}; optimised {bs['min_sdot_feasible_optimised']}")
    RES["bsplit_search"] = {k: v for k, v in bs.items()}
    # ---------------- grading ----------------
    Kall = all(ok[k] for k in ("S1_liouville", "S2_bgk_clausius", "S3_ou_clausius", "K2_cfg638_sis")) and k3 and k6 and all(v["ok"] for v in k1.values()) \
        and k4_mass and k4_edge and k4_E and k4_res and k5
    RES["K_all_pass"] = bool(Kall)
    grade(runs, ok, Kall)
    dump({})
    return 0 if Kall else 1


def ctrl_key(key, runs=None):
    p = key.split("|")
    legs = "2" if p[3] == "2" else "1"
    k = f"CTRL|{p[1]}|{p[2]}|{legs}"
    if runs is not None and k not in runs:
        k = f"CTRL|{p[1]}|{p[2]}|{'1' if legs == '2' else '2'}"
    return k


def grade(runs, ok, Kall):
    P("\n== Part 4: classes (frozen sec. 7) ==")
    readings = {"R1": [k for k in runs if k.startswith("R1|")], "R2": [k for k in runs if k.startswith("R2|")], "R3": [k for k in runs if k.startswith("R3|")]}
    proofs = {"R1": dict(B_TJ=ok["S1_liouville"] and ok["S3_ou_clausius"], B_REC=ok["S1_liouville"] and ok["S3_ou_clausius"],
                         B_SPLIT=ok["S1_liouville"] and ok["S3_ou_clausius"]),
              "R2": dict(B_TJ=ok["S1_liouville"] and ok["S2_bgk_clausius"], B_REC=ok["S1_liouville"] and ok["S2_bgk_clausius"],
                         B_SPLIT=ok["S1_liouville"] and ok["S2_bgk_clausius"]),
              "R3": dict(B_TJ=False, B_REC=False, B_SPLIT=False)}
    analytic_cex = dict(M1=ok["S5_cooling_lowers_S_and_casimir"], M2=ok["S5_cooling_lowers_S_and_casimir"], M3=True, M4=True, M5=True,
                        B_COH=ok["S5_cooling_lowers_S_and_casimir"], B_dS=True,
                        B_TJ_R3=ok["S6_deficit_negative"] and ok["S6_superJeans_sign"], B_REC_R3=ok["S6_drift_identity"])
    classes = {}
    for R, keys in readings.items():
        cand = {}
        def ent_type(name, field):
            viol = False; passm = True; worst = []
            for k in keys:
                r = runs[k]; e = r["eps_num"]; dr = r["drops"][field]
                worst.append((k, dr / r["M0"], e / r["M0"]))
                if dr >= 10 * e + 1e-8 * r["M0"]:
                    viol = True
                if dr > e:
                    passm = False
            return dict(verified_violation=viol, monotone_pass=passm, worst=max(worst, key=lambda z: z[1]))
        cand["M1_S"] = ent_type("M1", "S"); cand["M2_S2"] = ent_type("M2", "S2")
        cand["B_TJ"] = ent_type("B_TJ", "S_TJ"); cand["B_REC"] = ent_type("B_REC", "S_REC")
        # M3-M5 rises from zero
        def rise_from_zero(field, startkey, thr_fn):
            viol = False; best = None
            for k in keys:
                r = runs[k]
                st = r["start"][startkey] if startkey in r["start"] else None
                if field == "Fpsi_Fv":
                    st = r["start"]["Fpsi"] + r["start"]["Fv"]
                z = abs(st) <= 1e-12 * max(1.0, r["M0"]) if field != "Fpsi" else abs(st) <= 1e-12 * abs(r["start"]["W"])
                rise = r["rises"][field]
                thr = thr_fn(r)
                if z and rise >= thr:
                    viol = True
                best = max(best or 0.0, rise / thr) if z else best
            return dict(verified_violation=viol, monotone_pass=False if viol else None, max_rise_over_threshold=best)
        cand["M3_KL"] = rise_from_zero("KL", "KL", lambda r: 1e-4 * r["M0"])
        cand["M4_Fpsi"] = rise_from_zero("Fpsi", "Fpsi", lambda r: 1e-4 * abs(r["start"]["W"]))
        cand["M5_Fpsi_Fv"] = rise_from_zero("Fpsi_Fv", "Fv", lambda r: 1e-4 * max(r["M0"] * r["TJmax"], abs(r["start"]["W"])))
        # B-dS
        viol = False; worst = 0.0
        for k in keys:
            r = runs[k]; ck = ctrl_key(k, runs)
            tol = 10 * runs[ck]["E_err_max"] if ck in runs else 10 * r["E_err_max"]
            worst = max(worst, r["Qnet_max_rise"] / (tol if tol > 0 else 1e-300))
            if r["Qnet_max_rise"] > tol:
                viol = True
        cand["B_dS"] = dict(verified_violation=viol, monotone_pass=not viol, max_Qrise_over_tol=worst)
        # B-SPLIT
        viol = False; passm = True; wz = 0.0
        for k in keys:
            r = runs[k]; e = r["eps_num"]; wd = r["split"]["worst_drop_in_zero_release"]
            wz = max(wz, wd / e)
            if wd >= 10 * e + 1e-8 * r["M0"]:
                viol = True
            if wd > e:
                passm = False
        cand["B_SPLIT"] = dict(verified_violation=viol, monotone_pass=passm, worst_drop_over_eps=wz,
                               zero_release_intervals=sum(runs[k]["split"]["zero_release_intervals"] for k in keys))
        # analytic statements attached
        cand["M1_S"]["analytic"] = analytic_cex["M1"]; cand["M2_S2"]["analytic"] = analytic_cex["M2"]
        for m in ("M3_KL", "M4_Fpsi", "M5_Fpsi_Fv"):
            cand[m]["analytic"] = True
        cand["B_TJ"]["proof"] = proofs[R]["B_TJ"]; cand["B_REC"]["proof"] = proofs[R]["B_REC"]; cand["B_SPLIT"]["proof"] = proofs[R]["B_SPLIT"]
        cand["B_dS"]["proof"] = False
        if R == "R3":
            cand["B_TJ"]["analytic"] = analytic_cex["B_TJ_R3"]; cand["B_REC"]["analytic"] = analytic_cex["B_REC_R3"]
        else:
            cand["B_TJ"]["analytic"] = False; cand["B_REC"]["analytic"] = False
        cand["B_dS"]["analytic"] = True; cand["B_SPLIT"]["analytic"] = False
        Ms = ["M1_S", "M2_S2", "M3_KL", "M4_Fpsi", "M5_Fpsi_Fv"]; Bs = ["B_TJ", "B_REC", "B_dS", "B_SPLIT"]
        # B-COH == M1
        intrinsic = False                                                  # no M-candidate has a proof (none is claimed)
        Mviol_all = all(cand[m]["verified_violation"] and cand[m].get("analytic", False) for m in Ms)
        Bqual = [b for b in Bs if cand[b].get("proof") and cand[b]["monotone_pass"]]
        # B-dS and B-SPLIT carry their own frozen violation rules (sec. 6); the others need the matching analytic sign statement
        Bviol_all = all(cand[b]["verified_violation"] and (cand[b].get("analytic", False) or b in ("B_dS", "B_SPLIT")) for b in Bs)
        if intrinsic:
            cls = "INTRINSIC ARROW"
        elif Mviol_all and Bqual:
            q = "[finite-T bath]" if ("B_TJ" in Bqual or "B_REC" in Bqual) else "[T->0 sink only]"
            cls = f"BATH ARROW {q}"
        elif Mviol_all and Bviol_all:
            cls = "NO ARROW"
        else:
            cls = "UNDERDETERMINED"
        vac = [b for b in Bqual if b in ("B_dS", "B_SPLIT")]
        if not Bqual:
            ident = "none qualifies"
        elif vac and "B_TJ" in Bqual:
            ident = "EITHER (B-TJ and a vacuum bath both qualify)"
        elif vac and set(Bqual) <= {"B_dS", "B_SPLIT"}:
            ident = "VACUUM"
        elif Bqual == ["B_TJ"] or set(Bqual) <= {"B_TJ", "B_REC"}:
            ident = "NOT VACUUM"
        else:
            ident = ",".join(Bqual)
        coh_ok = ("B_REC" in Bqual) if R == "R3" else (None if not cand["M1_S"]["verified_violation"] else False)
        ph = {}
        for fld in ("S", "S2", "S_TJ", "S_REC"):
            vals = [(k, runs[k]["posthoc_windowed"][fld] / runs[k]["M0"]) for k in keys]
            w = max(vals, key=lambda z: z[1])
            ph[fld] = dict(any_window_verified=bool(w[1] > 1e-8), worst_run=w[0], worst_over_M=w[1])
        classes[R] = dict(cls=(cls if Kall else f"VOID ({cls})"), qualifying_baths=Bqual, bath_identity=ident,
                          record_coherent_partner_sufficient=coh_ok, candidates=cand, posthoc_windowed_NO_CLASS_WEIGHT=ph)
        P(f"  {R}: {classes[R]['cls']};  qualifying baths {Bqual};  bath identity {ident};  record's coherent partner sufficient: {bool(coh_ok)}")
        for c, d in cand.items():
            P(f"       {c:11s} violation {str(d['verified_violation']):5s} monotone {str(d.get('monotone_pass')):5s} proof {str(d.get('proof', False)):5s}"
              f" analytic {str(d.get('analytic', False)):5s}  " + ", ".join(f"{kk}={vv}" for kk, vv in d.items()
                                                                       if kk not in ('verified_violation', 'monotone_pass', 'proof', 'analytic')))
    P("\n  POST HOC (added after run 1, no class weight): windowed drop - 10 x Vlasov |dS| in the same window, per M (> 1e-8 = verified)")
    for R in classes:
        P(f"     {R}: " + "; ".join(f"{fld} {d['any_window_verified']} ({d['worst_over_M']:+.3e}, {d['worst_run']})" for fld, d in classes[R]["posthoc_windowed_NO_CLASS_WEIGHT"].items()))
    P(f"\n  HEADLINE (R3, the full CFG638 law): {classes['R3']['cls']};  R2 (CFG955 K-T): {classes['R2']['cls']};  R1 (OU relaxation): {classes['R1']['cls']}")
    P(f"  RATE: relaxation {RES['rates']['class_tS']['cls']}; drift {RES['rates']['class_tD']['cls']}")
    RES["classes"] = classes


def mutate():
    P("\n== MUTATE ==")
    TN = Toy("N")
    teeth = {}
    r1 = run_toy(TN, "IC-H", "BGK", legs=1, t_legs=2, mut="anti", label="Mu1")
    b1 = r1["drops"]["S_TJ"] >= 10 * r1["eps_num"] + 1e-8 * r1["M0"]
    teeth["Mu1_antiBGK"] = dict(bites=bool(b1), drop_S_TJ=r1["drops"]["S_TJ"], eps_num=r1["eps_num"], t=r1["t_reached"], neg_mass=r1["neg_mass"])
    P(f"  Mu1 anti-relaxation BGK (IC-H): B-TJ drop {r1['drops']['S_TJ']:.3e} vs 10 eps {10 * r1['eps_num']:.3e} (t {r1['t_reached']:.2f}, neg mass {r1['neg_mass']:.1e}) -> {'BITES' if b1 else 'no bite'}")
    r2 = run_toy(TN, "IC-E", "OU", legs=1, t_legs=10, mut="fdt2", label="Mu2")
    b2 = r2["drops"]["S_TJ"] >= 10 * r2["eps_num"] + 1e-8 * r2["M0"]
    teeth["Mu2_fdt_mismatch"] = dict(bites=bool(b2), drop_S_TJ=r2["drops"]["S_TJ"], eps_num=r2["eps_num"])
    P(f"  Mu2 OU diffusion at 2T_J, bath at T_J (IC-E): B-TJ drop {r2['drops']['S_TJ']:.3e} vs 10 eps {10 * r2['eps_num']:.3e} -> {'BITES' if b2 else 'no bite'}")
    r3m = run_toy(TN, "IC-D", "OUD", legs=1, t_legs=1.0, mut="driftflip", label="Mu3")
    r3 = run_toy(TN, "IC-D", "OUD", legs=1, t_legs=1.0, mut=None, label="Mu3-ref")
    fm = r3m["series_end"]["Fpsi"] / r3m["start"]["Fpsi"]; fr = r3["series_end"]["Fpsi"] / r3["start"]["Fpsi"]
    b3 = fm > 1 and fr < 1
    teeth["Mu3_driftflip"] = dict(bites=bool(b3), Fpsi_ratio_flipped=fm, Fpsi_ratio_ref=fr)
    P(f"  Mu3 drift sign flipped (IC-D): F_psi(1 tau_ff0)/F_psi(0) flipped {fm:.4f} vs unmutated {fr:.4f} -> {'BITES' if b3 else 'no bite'}")
    allb = all(t["bites"] for t in teeth.values())
    P(f"  MUTATE: {'ALL TEETH BITE (exit 1)' if allb else 'SOME TOOTH DID NOT BITE (exit 2)'}")
    RES["mutate_teeth"] = teeth
    dump({})
    return 1 if allb else 2


if __name__ == "__main__":
    code = main()
    P(f"\npeak RSS {rss_mb():.0f} MB; wall {time.time() - T_START:.0f} s")
    dump({})
    sys.exit(code)
