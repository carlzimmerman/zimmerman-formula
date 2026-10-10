#!/usr/bin/env python3
"""CFG550: the velocity part of the settling dynamics, derived from a principle (no knobs). FROZEN_CRITERIA.md (2717e0197).

Routes: (a0) strict kinetic GENERIC (Casimir entropy); (a1) reference-measure lift (KL to the law's phase-space phantom,
OU/Fokker-Planck toward T_ph at alpha/tau); (b) Lynden-Bell with T as a Lagrange multiplier; (c) phase-space inside-out
fill (bathtub f_ph Theta(E_t - E), E_t from M_cat).
Bench = CFG544's spherical N-body toy, imported unchanged from ../CFG544_settling_kinetic_consistency/cfg544.py (read only).
kappa = 1/2 FITTED; footings 9.3603e-11 / 1.1312e-10 never pooled; cold energy mass required; not "theory closed".
CFG550_MUTATE=1 -> MT (target temperature x 2), MS (entropy sign flipped), MK (sink removed).
Run: OMP_NUM_THREADS=1 nice -n 10 python3 cfg550.py
"""
import os, sys, json, math, time, importlib.util
os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ["CFG544_MUTATE"] = "0"
import numpy as np
import sympy as sp
from multiprocessing import Pool

HERE = os.path.dirname(os.path.abspath(__file__))
_spec = importlib.util.spec_from_file_location("cfg544", os.path.join(HERE, "..", "CFG544_settling_kinetic_consistency", "cfg544.py"))
T544 = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(T544)
J544 = json.load(open(os.path.join(HERE, "..", "CFG544_settling_kinetic_consistency", "cfg544_results.json")))
J541 = T544.J541
MUT = os.environ.get("CFG550_MUTATE", "0") == "1"
TAG = "_MUTATE" if MUT else ""
NPROC = 4
C_SI = 2.99792458e8
RMIN, EPS, NB, ALPHA, NPART = T544.RMIN, T544.EPS, T544.NB, T544.ALPHA, T544.NPART
Mb_enc, Mph_enc = T544.Mb_enc, T544.Mph_enc
OUT, RES = [], {"lane": "CFG550", "mutate": MUT, "criteria_commit": "2717e0197",
                "settings": dict(kappa=0.5, footings=T544.FOOT, toy="CFG544 cfg544.py imported unchanged", N=NPART, alpha=ALPHA,
                                 seed=T544.SEED, inputs="CFG541/CFG544 JSON (read only)")}
C2_544 = {"MW_can": 0.255, "MW_alt": 0.333, "cluster_can": 0.445, "cluster_alt": 0.539}   # frozen in FROZEN_CRITERIA.md


def log(s=""):
    print(s, flush=True); OUT.append(s)


# ================================================================================================ law profiles and targets
def I2(x):
    from scipy.special import erf
    return math.sqrt(math.pi / 2) * erf(x / math.sqrt(2)) - x * np.exp(-x ** 2 / 2)


def law_profiles(c):
    """Untruncated phantom in the law's (softened, as in the toy) field: T_ph(r) = (1/rho_ph) int_r^inf rho_ph g_law dr'
    (= second moment of the isotropic Eddington DF), Phi_law(r); route (c) bathtub target with E_t fixed by M_cat."""
    r = np.geomspace(RMIN * 0.5, 1e3, 60001)
    Mph = Mph_enc(c, r); rho = np.gradient(Mph, r) / (4 * math.pi * r ** 2)
    Mt = Mb_enc(c, r) + Mph
    g = Mt * r / (r ** 2 + EPS ** 2) ** 1.5
    fP = rho * g
    P = np.concatenate([np.cumsum((0.5 * (fP[1:] + fP[:-1]) * np.diff(r))[::-1])[::-1], [0.0]]) + 1.0 / (8 * math.pi * r[-1] ** 2)
    T = P / np.maximum(rho, 1e-300)
    phi = np.concatenate([[0.0], np.cumsum(0.5 * (g[1:] + g[:-1]) * np.diff(r))])
    sel = (r >= RMIN) & (r <= c["rta"])
    rr, rh, TT, ph = r[sel], rho[sel], T[sel], phi[sel]
    def mass(Et):
        x = np.sqrt(2 * np.maximum(Et - ph, 0.0) / TT)
        fr = I2(x) / math.sqrt(math.pi / 2)
        rt = rh * fr
        M = np.concatenate([[0.0], np.cumsum(0.5 * (4 * math.pi * rr[1:] ** 2 * rt[1:] + 4 * math.pi * rr[:-1] ** 2 * rt[:-1]) * np.diff(rr))])
        return M, rt, x
    lo, hi = ph[0], ph[-1]
    if mass(hi)[0][-1] < c["Mcat"]:
        Et = None
    else:
        for _ in range(100):
            mid = 0.5 * (lo + hi)
            if mass(mid)[0][-1] < c["Mcat"]: lo = mid
            else: hi = mid
        Et = 0.5 * (lo + hi)
    out = dict(r=r, T=T, phi=phi, rho=rho)
    if Et is not None:
        M, rt, x = mass(Et)
        Tt = TT * np.where(x > 1e-6, (3 * I2(x) - x ** 3 * np.exp(-x ** 2 / 2)) / np.maximum(3 * I2(x), 1e-300), 0.0)
        re = float(np.interp(0.0, -(ph - Et), rr)) if (ph > Et).any() else float(rr[-1])
        out.update(Et=Et, rt=rr, rhot=rt, Mt=M, Tt=Tt, r_e=re, r99_t=float(np.interp(0.99 * M[-1], M, rr)), Mt_tot=float(M[-1]))
    return out


# ================================================================================================ bench (toy imported unchanged)
class Toy550(T544.Toy):
    def __init__(self, c, rule, mode, scale, prof):
        super().__init__(c, rule, ou=(mode in ("fix2", "a1", "c")), ou_scale=(scale if mode == "fix2" else 1.0), drift=(rule != "none"))
        self.mode, self.scale, self.prof = mode, scale, prof
        self.Tgt = np.interp(self.rc, prof["r"], prof["T"])
        if mode == "c":
            Mt_f = np.interp(self.rf, prof["rt"], prof["Mt"], right=prof["Mt"][-1])
            self.rhoph = np.maximum(np.diff(Mt_f), 0.0) / self.V          # deficit target = density marginal of the bathtub
            self.Tgt = np.interp(self.rc, prof["rt"], prof["Tt"], right=0.0)

    def vel_step(self, r, vr, vt, dt, g, rng):
        if self.mode == "fix2":
            return self.ou_step(r, vr, vt, dt, g, rng)
        c = self.c; pr = self.prof
        mc = self.m * np.histogram(r, self.rf)[0]; rho = mc / self.V
        k = np.clip(np.searchsorted(self.rf, r) - 1, 0, NB - 1)
        inside = r < c["rta"]
        gam = ALPHA * np.sqrt(4 * math.pi * (self.rhob + rho))[k]
        a = np.exp(-gam * dt)
        s2 = np.interp(r, pr["r"], pr["T"]) * self.scale
        b = np.sqrt(s2 * (1 - a ** 2))
        K0 = 0.5 * self.m * np.sum(vr ** 2 + vt ** 2)
        x1, x2, x3 = rng.standard_normal((3, r.size))
        pr_r = a * vr + b * x1; vtx = a * vt + b * x2; vty = b * x3; pr_t = np.hypot(vtx, vty)
        if self.mode == "a1":
            vr_n = np.where(inside, pr_r, vr); vt_n = np.where(inside, pr_t, vt)
        else:   # route c: Gaussian-reversible OU proposal, rejection outside |v| < v_t(r); pure friction where v_t = 0
            vt2 = 2 * np.maximum(pr["Et"] - np.interp(r, pr["r"], pr["phi"]), 0.0)
            zero = vt2 <= 0
            vo2 = vr ** 2 + vt ** 2; vn2 = pr_r ** 2 + pr_t ** 2
            ok = (vn2 < vt2) | (vo2 >= vt2)
            nr = np.where(zero, a * vr, np.where(ok, pr_r, vr)); nt = np.where(zero, a * vt, np.where(ok, pr_t, vt))
            vr_n = np.where(inside, nr, vr); vt_n = np.where(inside, nt, vt)
        K1 = 0.5 * self.m * np.sum(vr_n ** 2 + vt_n ** 2)
        return vr_n, vt_n, K1 - K0

    def diag550(self, r, vr, L):
        d = self.diag(r, vr, L)
        c = self.c; vt = L / r
        mc = self.m * np.histogram(r, self.rf)[0]; rho = mc / self.V
        Menc_c = Mb_enc(c, self.rc) + np.concatenate([[0.0], np.cumsum(mc)[:-1]]) + 0.5 * mc
        gb = Menc_c * self.rc / (self.rc ** 2 + EPS ** 2) ** 1.5
        Pf = np.concatenate([np.cumsum((rho * gb * self.dr)[::-1])[::-1], [0.0]]); Pc = 0.5 * (Pf[1:] + Pf[:-1])
        s2J = np.where(rho > 0, Pc / np.maximum(rho, 1e-300), 0.0)
        k = np.clip(np.searchsorted(self.rf, r) - 1, 0, NB - 1)
        sh = (r > 0.1) & (r < 0.9)
        XJ = float(np.sum(vr[sh] ** 2 + vt[sh] ** 2) / 3 / np.sum(s2J[k[sh]])) if sh.sum() > 10 else float("nan")
        # F (two-sided, this variant's deficit target) and the velocity-KL proxy F_v (Gaussian second moments)
        dd = self.rhoph - rho
        Md = np.concatenate([[0.0], np.cumsum(dd * self.V)])
        integ = Md ** 2 / (2 * self.rf ** 2)
        F = float(np.sum(0.5 * (integ[1:] + integ[:-1]) * self.dr) + Md[-1] ** 2 / (2 * self.rf[-1]))
        n = np.histogram(r, self.rf)[0]
        sv = np.histogram(r, self.rf, weights=vr ** 2 + vt ** 2)[0] / np.maximum(3 * n, 1)
        ok = (n >= 5) & (self.Tgt > 0) & (sv > 0)
        q = sv[ok] / self.Tgt[ok]
        Fv = float(np.sum(self.m * n[ok] * self.Tgt[ok] * 1.5 * (q - 1 - np.log(q))))
        d.update(logXJ=float(np.log10(XJ)) if XJ > 0 else -99.0, F=F, Fv=Fv,
                 vmax=float(np.max(np.sqrt(vr ** 2 + vt ** 2))))
        return d


def run(job):
    c, name, ic, rule, mode, T_Gyr = job["c"], job["name"], job["ic"], job["rule"], job["mode"], job["T"]
    prof = law_profiles(c)
    rng = np.random.default_rng(T544.SEED)
    r, vr, L, m = T544.make_ic(c, ic, rng, sig2_scale=job.get("sig2", 1.0), inject=job.get("inject", False))
    toy = Toy550(c, rule, mode, job.get("scale", 1.0), prof); toy.m = m
    n0 = r.size
    dt = c["dt"]; nsteps = int(round(T_Gyr / (dt * c["tu_Gyr"])))
    every = max(1, int(round(0.25 / (dt * c["tu_Gyr"]))))
    K0, W0 = toy.energy(r, vr, L)
    W_drift = 0.0; W_ou = 0.0
    snaps = []; t0 = time.time(); nsub_max = 0
    for it in range(nsteps + 1):
        if it % every == 0 or it == nsteps:
            dg = toy.diag550(r, vr, L); K, W = toy.energy(r, vr, L)
            dg.update(t_Gyr=it * dt * c["tu_Gyr"], E=K + W, sink_cum=-(W_drift + W_ou) / c["Mcat"],
                      drift_out=-W_drift / c["Mcat"], relax_in=W_ou / c["Mcat"],
                      integ_err=(K + W - K0 - W0 - W_drift - W_ou) / abs(K0 + W0), dEmatter=(K + W - K0 - W0) / abs(K0 + W0))
            snaps.append(dg)
        if it == nsteps: break
        r, vr, ns = T544.vlasov_step(toy, r, vr, L, dt)
        nsub_max = max(nsub_max, ns)
        if toy.drift:
            vt = L / r
            g, _ = toy.gravity(r)
            _, Wb = toy.energy(r, vr, L)
            rn, _w = toy.drift_step(r, dt, g)
            Ln = rn * vt
            _, Wa = toy.energy(rn, vr, Ln)
            W_drift += Wa - Wb
            L = Ln; r = rn
            if toy.ou:
                vr, vt, dk = toy.vel_step(r, vr, vt, dt, g, rng)
                W_ou += dk; L = r * vt
    E0 = K0 + W0; fin = snaps[-1]
    ref = min(snaps, key=lambda s: abs(s["t_Gyr"] - (fin["t_Gyr"] - 2.0)))
    F0 = snaps[0]["F"]; L0 = snaps[0]["F"] + snaps[0]["Fv"]
    dF = [snaps[i + 1]["F"] - snaps[i]["F"] for i in range(len(snaps) - 1)]
    dL = [(snaps[i + 1]["F"] + snaps[i + 1]["Fv"]) - (snaps[i]["F"] + snaps[i]["Fv"]) for i in range(len(snaps) - 1)]
    res = dict(name=name, sys=c["sys"], foot=c["foot"], ic=ic, rule=rule, mode=mode, T_Gyr=T_Gyr, steps=nsteps,
               n_particles=n0, mass_exact=bool(r.size == n0), dE_over_E=float((fin["E"] - E0) / abs(E0)), final=fin,
               d_logX_last2=float(fin["logX"] - ref["logX"]), d_logXJ_last2=float(fin["logXJ"] - ref["logXJ"]),
               d_D_last2=float(fin["D"] - ref["D"]), limited_frac=toy.n_lim / max(toy.n_mv, 1),
               series=[dict(t=s["t_Gyr"], logX=s["logX"], logXJ=s["logXJ"], D=s["D"], r99=s["r99"], sink=s["sink_cum"],
                            F=s["F"], Fv=s["Fv"], drift_out=s["drift_out"], relax_in=s["relax_in"]) for s in snaps],
               wall_s=time.time() - t0, nsub_max=nsub_max, integ_err_final=fin["integ_err"],
               integ_err_maxabs=float(max(abs(s["integ_err"]) for s in snaps)),
               dEmatter_final=fin["dEmatter"], vmax_code=float(max(s["vmax"] for s in snaps)),
               max_rise_F_over_F0=float(max(dF) / F0) if F0 > 0 else None,
               max_rise_FplusFv_over_L0=float(max(dL) / L0) if L0 > 0 else None)
    res["gate550_end"] = bool(abs(fin["D"]) <= 0.1 and abs(fin["logXJ"]) <= 0.1)
    res["gate550_steady"] = bool(abs(res["d_D_last2"]) <= 0.05 and abs(res["d_logXJ_last2"]) <= 0.05)
    res["gate550"] = res["gate550_end"] and res["gate550_steady"]
    res["gate544"] = bool(abs(fin["logX"]) <= 0.1 and abs(fin["D"]) <= 0.1 and abs(res["d_logX_last2"]) <= 0.05 and abs(res["d_D_last2"]) <= 0.05)
    res["sink_rate_last2"] = float((fin["sink_cum"] - ref["sink_cum"]) / max(fin["t_Gyr"] - ref["t_Gyr"], 1e-9))
    res["relax_in_rate_last2"] = float((fin["relax_in"] - ref["relax_in"]) / max(fin["t_Gyr"] - ref["t_Gyr"], 1e-9))
    return res


# ================================================================================================ sympy
def sympy_items():
    R = {}
    G, Vf, T, A, r0 = sp.symbols("G V_f T A r_0", positive=True)
    r, v = sp.symbols("r v", positive=True)
    # A1: SIS. f = A exp(-(v^2/2 + Phi)/T), Phi = Vf^2 ln(r/r0): rho = A (2 pi T)^(3/2) (r/r0)^(-Vf^2/T)
    rho_f = A * (2 * sp.pi * T) ** sp.Rational(3, 2) * (r / r0) ** (-Vf ** 2 / T)
    rho_ph = Vf ** 2 / (4 * sp.pi * G * r ** 2)
    sol_T = sp.solve(sp.Eq(sp.diff(sp.log(rho_f), r) * r, sp.diff(sp.log(rho_ph), r) * r), T)
    R["A1_T_from_shape"] = str(sol_T)
    Tval = sol_T[0]
    sol_A = sp.solve(sp.Eq(rho_f.subs(T, Tval), rho_ph), A)
    R["A1_amplitude_A"] = str(sp.simplify(sol_A[0]))
    vint = sp.integrate(4 * sp.pi * v ** 2 * sp.exp(-v ** 2 / (2 * T)), (v, 0, sp.oo))
    R["A1_velocity_integral_check"] = bool(sp.simplify(vint - (2 * sp.pi * T) ** sp.Rational(3, 2)) == 0)
    rp = sp.symbols("rp", positive=True)
    jeans = sp.integrate((Vf ** 2 / (4 * sp.pi * G * rp ** 2)) * (Vf ** 2 / rp), (rp, r, sp.oo)) / rho_ph * G   # G M(<r)/r^2 = Vf^2/r
    R["A1_Jeans_sigma2"] = str(sp.simplify(jeans / G))
    R["A1_pass"] = bool(sp.simplify(Tval - Vf ** 2 / 2) == 0 and sp.simplify(jeans / G - Vf ** 2 / 2) == 0)
    R["A1_note"] = ("the law's own (rho_ph, Phi_law) fix the phase-space phantom f_ph = A exp(-E/T) with T = V_f^2/2 and its "
                    "amplitude; no temperature is inserted. Input level: the same rho_ph class A already takes.")
    # A2: discrete velocity cells at one x, pairs (i,j) with partner compensation
    n = 3
    vv = sp.symbols("v0:3", real=True); f = sp.symbols("f0:3", positive=True); p = sp.symbols("p0:3", positive=True)
    Th, m01, m12, m02 = sp.symbols("Theta m01 m12 m02", positive=True)
    dE = sp.Matrix([vv[i] ** 2 / 2 for i in range(n)] + [1])
    S = -(T / Th) * sum(f[i] * sp.log(f[i] / p[i]) - f[i] for i in range(n))
    dS = sp.Matrix([sp.diff(S, f[i]) for i in range(n)] + [0])
    def w(i, j):
        e = [0] * (n + 1); e[i] = -1; e[j] = 1; e[n] = -(vv[j] ** 2 - vv[i] ** 2) / 2
        return sp.Matrix(e)
    M = m01 * w(0, 1) * w(0, 1).T + m12 * w(1, 2) * w(1, 2).T + m02 * w(0, 2) * w(0, 2).T
    R["A2_M_symmetric"] = bool(sp.simplify(M - M.T) == sp.zeros(n + 1, n + 1))
    R["A2_M_dE_zero"] = bool(sp.simplify(M * dE) == sp.zeros(n + 1, 1))
    dSdt = sp.expand((dS.T * M * dS)[0])
    sos = sum(mm * ((w(i, j).T * dS)[0]) ** 2 for mm, (i, j) in ((m01, (0, 1)), (m12, (1, 2)), (m02, (0, 2))))
    R["A2_dSdt_is_sum_of_squares"] = bool(sp.simplify(dSdt - sp.expand(sos)) == 0)
    zdot = M * dS
    R["A2_dEdt_zero"] = bool(sp.simplify((dE.T * zdot)[0]) == 0)
    R["A2_mass_conserved"] = bool(sp.simplify(sum(zdot[i] for i in range(n))) == 0)
    # stationary iff ln(f_i/p_i) equal: w.dS = -(T/Theta)(ln(f_j/p_j) - ln(f_i/p_i))
    R["A2_stationary_condition"] = str(sp.simplify((w(0, 1).T * dS)[0]))
    # continuum: mu = T ln(f/p_ph), p_ph ~ exp(-v^2/2T); flux -gamma f d_v mu = -gamma (T f' + v f)
    vs_ = sp.symbols("v", real=True); gam = sp.symbols("gamma", positive=True); fn = sp.Function("f")(vs_)
    mu = T * sp.log(fn) + vs_ ** 2 / 2
    J = -gam * fn * sp.diff(mu, vs_)
    R["A2_continuum_flux"] = str(sp.simplify(J))
    R["A2_continuum_is_OU"] = bool(sp.simplify(J + gam * (T * sp.diff(fn, vs_) + vs_ * fn)) == 0)
    # moments of OU (1-D) on a Gaussian test state N(m, s)
    mm_, s_ = sp.symbols("m s", positive=True)
    fg = sp.exp(-(vs_ - mm_) ** 2 / (2 * s_)) / sp.sqrt(2 * sp.pi * s_)
    ft = sp.diff(gam * (T * sp.diff(fg, vs_) + vs_ * fg), vs_)
    d1 = sp.simplify(sp.integrate(vs_ * ft, (vs_, -sp.oo, sp.oo)))
    d2 = sp.simplify(sp.integrate(vs_ ** 2 * ft, (vs_, -sp.oo, sp.oo)))
    R["A2_dmean_dt"] = str(d1); R["A2_dv2_dt"] = str(d2)
    R["A2_pass"] = all(R[k] for k in ("A2_M_symmetric", "A2_M_dE_zero", "A2_dSdt_is_sum_of_squares", "A2_dEdt_zero",
                                      "A2_mass_conserved", "A2_continuum_is_OU"))
    # A3: exchange sign: energy into matter = -d eps_phi/dt = gamma (T - <v^2>) per dof; dS >= 0 either way (sum of squares)
    R["A3_energy_into_matter_per_dof"] = str(sp.simplify(d2 / 2).subs(mm_, 0))
    R["A3_two_way"] = ("M is symmetric PSD with M dE = 0; dS/dt is a sum of squares for any state, hot or cold, so the partner "
                       "may give energy (cold matter, <v^2> < 3T) or take it (hot matter): two-way exchange is allowed by M")
    # A0: strict GENERIC (Casimir S = -sum C(f)) with partner transfers: stationarity C'(f_i) = C'(f_j) for all pairs
    Cf = sp.Function("C")
    dS0 = sp.Matrix([-sp.diff(Cf(f[i]), f[i]) for i in range(n)] + [0])
    R["A0_stationarity"] = str(sp.simplify((w(0, 1).T * dS0)[0]))
    R["A0_note"] = ("Casimir entropy + partner: stationary iff C'(f) is the same in every velocity cell -> f uniform in v "
                    "(C strictly convex), not normalisable on unbounded v: no finite temperature (T -> infinity), energy flows "
                    "from phi into matter without bound. Without the partner (energy-conserving Landau pairs) the equilibrium "
                    "is the Maxwellian at the local kinetic temperature: a cold (sigma = 0) element is already stationary -> "
                    "T stays at the source value 0.")
    a0_test = sp.integrate(1, (vs_, -sp.oo, sp.oo))
    R["A0_uniform_f_normalisable"] = bool(a0_test.is_finite)
    # b1: GENERIC equilibrium d(S - beta E)/d eps_phi = 0 with dS/d eps_phi = 0 (zero-entropy partner)
    beta = sp.symbols("beta", real=True)
    R["B1_beta"] = str(sp.solve(sp.Eq(0 - beta * 1, 0), beta))
    # A5: Lyapunov
    x = sp.symbols("x", real=True)
    Phi, PhiL, Ff = sp.Function("Phi")(x), sp.Function("PhiL")(x), sp.Function("F")
    gfun = sp.log(Ff(vs_ ** 2 / 2 + PhiL))
    vl = vs_ * sp.diff(gfun, x) - sp.diff(Phi, x) * sp.diff(gfun, vs_)
    target = sp.diff(Ff(vs_ ** 2 / 2 + PhiL), PhiL) / Ff(vs_ ** 2 / 2 + PhiL) * vs_ * (sp.diff(PhiL, x) - sp.diff(Phi, x))
    R["A5_phase_space_KL_Vlasov_rate_identity"] = bool(sp.simplify(vl - target) == 0)
    R["A5_phase_space_KL_note"] = ("d/dt int f ln(f/f_ph)|Vlasov = -int f (F'/F) v.grad(Phi_law - Phi): vanishes only where the "
                                   "real potential equals the law's (psi = Phi_law - Phi = 0)")
    # family L_c = F - c sigma^2 H (isothermal): Vlasov rate (1 - c) int rho u.grad psi. c = 1 is Vlasov-invariant;
    # its drift rate on a mode delta = eps cos(k x) about rho_ph:
    k, eps, rho0, sig2, al, tau = sp.symbols("k epsilon rho_0 sigma2 alpha tau", positive=True)
    dl = eps * sp.cos(k * x)
    psi = 4 * sp.pi * G * rho0 * dl / k ** 2
    integrand = rho0 * al * tau * (sp.diff(psi, x) ** 2 - sig2 * sp.diff(psi, x) * sp.diff(dl, x))
    rate = sp.simplify(sp.integrate(integrand, (x, 0, 2 * sp.pi / k)) * k / (2 * sp.pi))
    R["A5_c1_drift_rate_mode"] = str(sp.factor(rate))
    kJ = sp.sqrt(4 * sp.pi * G * rho0 / sig2)
    R["A5_c1_rises_for_k_below_kJ"] = bool(sp.simplify(rate.subs(k, kJ / 2)) > 0 and sp.simplify(rate.subs(k, 2 * kJ)) < 0)
    # c != 1: Vlasov term first order in bulk velocity lambda, dissipation O(alpha): dL/dt = lambda A - alpha (B + lambda^2 C)
    lam, Aa, Bb, Cc = sp.symbols("lambda A B C", positive=True)
    dL = lam * Aa - al * (Bb + lam ** 2 * Cc)
    lstar = sp.solve(sp.diff(dL, lam), lam)[0]
    mx = sp.simplify(dL.subs(lam, lstar))
    R["A5_cne1_max_rate"] = str(mx)
    R["A5_cne1_positive_if_alpha_below"] = str(sp.solve(sp.Eq(mx, 0), al))
    R["A5_other_candidates"] = {
        "E_N + Casimirs (incl. E_N - T S_B)": "Vlasov-invariant; drift rate -alpha int rho tau grad psi.grad Phi (indefinite, CFG544) and the relaxation heats cold matter (dE_N > 0): not monotone",
        "F + c F_v (c >= 0)": "Vlasov rate int rho u.grad psi + c(...) first order in u, dissipation O(alpha): fails for small alpha",
        "phase-space KL to f_ph": "Vlasov rate vanishes only where Phi = Phi_law (identity above)"}
    R["A5_full_system_Lyapunov"] = "NOT ESTABLISHED"
    # A6: angular momentum: d<v>/dt = -gamma <v> in the region frame
    R["A6_total_momentum_decay"] = str(d1)
    R["A6_note"] = ("the relaxation pulls each bin's mean velocity to zero in the region's baryon frame: total j decays at "
                    "alpha/tau unless already zero, and the stochastic kicks change each element's j: NOT CONSERVED. "
                    "A reference centred on the local mean velocity would conserve momentum (d<v>/dt = 0) but was not "
                    "frozen and is not run.")
    R["A7_note"] = ("the velocity relaxation acts at fixed x (an ODE in v per point): no spatial propagation, no new speed; "
                    "alpha keeps only CFG542's stability bound (alpha beta q < 1)")
    return R


# ================================================================================================ discrete velocity model (A2 numeric, MS)
def vel_cells(sign=+1.0, T=1.0, nv=41, steps=5000, dt=2e-4, s0=0.05):
    v = np.linspace(-6, 6, nv); dv = v[1] - v[0]
    p = np.exp(-v ** 2 / (2 * T)); p /= p.sum()
    f = np.exp(-v ** 2 / (2 * s0 * T)); f /= f.sum()
    eps_phi = 0.0
    def KL(f): return float(np.sum(f * np.log(f / p)))
    E0 = float(np.sum(f * v ** 2 / 2)) + eps_phi
    KLs = [KL(f)]; Es = []
    for _ in range(steps):
        mu = T * np.log(f / p)
        mob = np.where(np.abs(f[1:] - f[:-1]) > 1e-300, (f[1:] - f[:-1]) / (np.log(f[1:]) - np.log(f[:-1]) + 1e-300), f[1:])
        J = sign * mob * (mu[:-1] - mu[1:]) / dv ** 2           # flux i -> i+1
        df = np.zeros_like(f); df[:-1] -= J; df[1:] += J
        dEk = np.sum(J * (v[1:] ** 2 - v[:-1] ** 2) / 2)
        fn = f + dt * df
        if (fn <= 0).any() or not np.isfinite(fn).all():
            break
        f = fn; eps_phi -= dt * dEk
        KLs.append(KL(f)); Es.append(float(np.sum(f * v ** 2 / 2)) + eps_phi)
    return dict(KL_start=KLs[0], KL_end=KLs[-1], KL_monotone_down=bool(np.all(np.diff(KLs) <= 1e-15)),
                KL_monotone_up=bool(np.all(np.diff(KLs) >= -1e-15)), steps_done=len(KLs) - 1,
                max_dE_total=float(max(abs(e - E0) for e in Es)) if Es else None, partner_energy_end=eps_phi,
                mass_err=float(abs(f.sum() - 1)))


# ================================================================================================ Eddington existence (A4)
def eddington_check(c):
    rM = c["Mb"]
    r = np.geomspace(1e-4 * rM, 1e7 * rM, 200001)
    Mph = Mph_enc(c, r); rho = np.gradient(Mph, r) / (4 * math.pi * r ** 2)
    Mt = Mb_enc(c, r) + Mph
    g = Mt / r ** 2
    Phi = np.concatenate([[0.0], np.cumsum(0.5 * (g[1:] + g[:-1]) * np.diff(r))])
    Psi = Phi[-1] - Phi                                   # decreasing in r
    drho = np.diff(rho)
    mono = bool((drho <= 0).all())
    imax = int(np.argmax(rho))
    out = dict(rho_monotone_in_r=mono, r_of_rho_max_over_rM=float(r[imax] / rM), frac_cells_increasing=float(np.mean(drho > 0)))
    # numeric Eddington (lower limit at the far tail; the tail integrand falls ~1e-2 per decade)
    Ps = Psi[::-1]; rs = rho[::-1]
    d1 = np.gradient(rs, Ps); d2 = np.gradient(d1, Ps)
    Eg = np.interp(np.linspace(0.02, 0.98, 60), np.linspace(0, 1, Ps.size), Ps)   # sample energies inside the range
    fE = []
    for E in Eg:
        smax = math.sqrt(E - Ps[0]); s = np.linspace(0, smax, 4001)
        fE.append(float(np.trapz(2 * np.interp(E - s ** 2, Ps, d2), s) / (math.sqrt(8) * math.pi ** 2)))
    fE = np.array(fE)
    out.update(f_min_over_max=float(fE.min() / np.abs(fE).max()), f_negative_frac=float(np.mean(fE < 0)))
    out["isotropic_lift_exists"] = bool(mono and fE.min() >= -1e-6 * np.abs(fE).max())
    return out


# ================================================================================================ main
def main():
    cells = {f"{s}_{f}": T544.make_cell(s, f) for s in T544.SYS for f in T544.FOOT}
    keys = list(cells)
    RES["cells"] = {}
    log("CFG550 velocity part of the settling dynamics" + (" [MUTATE]" if MUT else ""))
    for k, c in cells.items():
        pr = law_profiles(c)
        sh = (pr["r"] > 0.1) & (pr["r"] < 0.9)
        e = dict(Vf_kms=c["Vf_kms"], rstar_kpc=c["rstar_kpc"], Mcat=c["Mcat"], r99_analytic=T544.r99_analytic(c),
                 A1_deep_T_over_Vf2=T544.jeans_controls(c),
                 T_ph_shell_min=float(pr["T"][sh].min()), T_ph_shell_max=float(pr["T"][sh].max()),
                 route_c=dict(Et=pr.get("Et"), r_e=pr.get("r_e"), r99_t=pr.get("r99_t"), Mt_over_Mcat=pr.get("Mt_tot", 0) / c["Mcat"]))
        if pr.get("r99_t"):
            e["route_c"]["dln_r99_t_vs_analytic"] = float(math.log(pr["r99_t"] / e["r99_analytic"]))
            rc = np.geomspace(0.1, 0.9, 16)
            e["route_c"]["D_t_shell_median"] = float(np.median(np.log10(np.interp(rc, pr["rt"], pr["rhot"]) / np.interp(rc, pr["r"], pr["rho"]))))
        jj = J541["one_d"][c["foot"]][c["sys"]]
        e["CFG541_dW_over_Vf2"] = jj["dW_per_mass"] / c["Vf2_SI"]; e["CFG541_Kf_over_Vf2"] = jj["Kf_per_mass"] / c["Vf2_SI"]
        e["B2_closed_sigma2_over_required_dex"] = float(math.log10(jj["dW_per_mass"] / jj["Kf_per_mass"]))
        e["B3_beta0_uniform_fraction_D"] = float(math.log10(c["Mcat"] / Mph_enc(c, np.array([c["rta"]]))[0]))
        if not MUT:
            e["A4_eddington"] = eddington_check(c)
        RES["cells"][k] = e
        log(f"{k}: V_f {c['Vf_kms']:.1f} km/s; deep T_ph/V_f^2 {e['A1_deep_T_over_Vf2']:.4f}; T_ph shell {e['T_ph_shell_min']:.3f}-{e['T_ph_shell_max']:.3f}; "
            f"route c: r_e {e['route_c']['r_e']}, r99_t {e['route_c']['r99_t']}, D_t {e['route_c'].get('D_t_shell_median')}; "
            f"B2 closed sigma^2 off by {e['B2_closed_sigma2_over_required_dex']:+.3f} dex; B3 beta=0 D {e['B3_beta0_uniform_fraction_D']:+.3f}"
            + (f"; A4 {e['A4_eddington']}" if not MUT else ""))
    A1_num = all(abs(RES["cells"][k]["A1_deep_T_over_Vf2"] / 0.5 - 1) <= 0.02 for k in keys)
    if not MUT:
        RES["sympy"] = sympy_items()
        log("\nSympy:")
        for kk, vv in RES["sympy"].items():
            log(f"  {kk}: {vv}")
        RES["vel_cells_plus"] = vel_cells(+1.0)
        log(f"\nDiscrete velocity model (+M): {RES['vel_cells_plus']}")
    else:
        RES["vel_cells_flipped"] = vel_cells(-1.0, steps=2000, dt=1e-5, s0=0.7)
        Th = sp.symbols("Theta", positive=True); a_ = sp.symbols("a", real=True); m_ = sp.symbols("m", positive=True)
        # flipped S: dS'/dt along the true flow = -(sum of squares)
        RES["MS_sympy_dSdt_flipped"] = str(sp.simplify(-m_ * a_ ** 2))
        log(f"MS: velocity model with S flipped: {RES['vel_cells_flipped']}")

    jobs = []
    for k, c in cells.items():
        if not MUT:
            jobs += [dict(c=c, name=f"{k}|C2_vlasov_eq", ic="E", rule="none", mode="none", T=2.0),
                     dict(c=c, name=f"{k}|C5_fix2_C", ic="C", rule="two", mode="fix2", T=5.0)]
            for md in ("a1", "c"):
                jobs += [dict(c=c, name=f"{k}|{md}_B", ic="B", rule="two", mode=md, T=10.0),
                         dict(c=c, name=f"{k}|{md}_C", ic="C", rule="two", mode=md, T=5.0),
                         dict(c=c, name=f"{k}|{md}_over_base", ic="E", rule="two", mode=md, T=5.0),
                         dict(c=c, name=f"{k}|{md}_over_inj", ic="E", rule="two", mode=md, T=5.0, inject=True)]
        else:
            for md in ("a1", "c"):
                jobs += [dict(c=c, name=f"{k}|MT_{md}_C_x2", ic="C", rule="two", mode=md, T=5.0, scale=2.0)]
    if MUT:
        jobs += [dict(c=cells["MW_can"], name="MW_can|MK_a1_C_2Gyr", ic="C", rule="two", mode="a1", T=2.0)]
    jobs.sort(key=lambda j: -j["T"] / j["c"]["dt"] / j["c"]["tu_Gyr"])
    with Pool(NPROC) as pool:
        out = pool.map(run, jobs, chunksize=1)
    runs = {o["name"]: o for o in out}
    RES["runs"] = runs
    log("\nRuns (end state; shell 0.1-0.9 r_*):")
    for nm in sorted(runs):
        o = runs[nm]; f = o["final"]
        log(f"  {nm:30s} {o['T_Gyr']:4.1f} Gyr logXJ {f['logXJ']:+.3f} logX544 {f['logX']:+.3f} D {f['D']:+.3f} last2 dXJ/dD {o['d_logXJ_last2']:+.3f}/{o['d_D_last2']:+.3f}"
            f" r99 {f['r99']:.3f} beta {f['beta']:+.2f} out {f['drift_out']:+.3f} in {f['relax_in']:+.3f} sink {f['sink_cum']:+.3f} (rate {o['sink_rate_last2']:+.4f}/Gyr)"
            f" integ {o['integ_err_maxabs']:.1e} riseF {o['max_rise_F_over_F0']} G550 {o['gate550']} G544 {o['gate544']} ({o['wall_s']:.0f}s)")
        log("       s(r) bins: " + " ".join("nan" if (x != x) else f"{x:.2f}" for x in f["s_bins"]))

    if MUT:
        mt = {f"{k}|{md}": (not runs[f"{k}|MT_{md}_C_x2"]["gate550"]) for k in keys for md in ("a1", "c")}
        mk = runs["MW_can|MK_a1_C_2Gyr"]
        mk_bite = abs(mk["dEmatter_final"]) - abs(mk["integ_err_final"]) > 1e-2
        ms = RES["vel_cells_flipped"]
        ms_bite = bool(ms["KL_end"] > ms["KL_start"] and ms["KL_monotone_up"])
        bite = dict(MT=all(mt.values()), MS=ms_bite, MK=bool(mk_bite))
        RES["mutate_teeth"] = dict(MT_fails=mt, MK_dEmatter=mk["dEmatter_final"], MK_integ_err=mk["integ_err_final"], MS=ms, bite=bite)
        log(f"\nMUTATE: MT fails {mt}; MK matter dE/E {mk['dEmatter_final']:+.3e} (integ {mk['integ_err_final']:+.1e}); MS {ms}; bite {bite}")
        return 1 if all(bite.values()) else 0

    # controls
    c2 = {k: runs[f"{k}|C2_vlasov_eq"]["gate544"] or (abs(runs[f"{k}|C2_vlasov_eq"]["final"]["logX"]) <= 0.1 and abs(runs[f"{k}|C2_vlasov_eq"]["final"]["D"]) <= 0.1) for k in keys}
    c5 = {}
    for k in keys:
        a = runs[f"{k}|C5_fix2_C"]["final"]; b = J544["runs"][f"{k}|fix2_C"]["final"]
        c5[k] = dict(dlogX=abs(a["logX"] - b["logX"]), dD=abs(a["D"] - b["D"]), ok=bool(abs(a["logX"] - b["logX"]) <= 1e-6 and abs(a["D"] - b["D"]) <= 1e-6))
    mass = all(o["mass_exact"] for o in runs.values())
    ctrl = A1_num and all(c2.values()) and all(v["ok"] for v in c5.values()) and mass
    RES["controls"] = dict(A1_numeric_deep=A1_num, C2_end_gate=c2, C5_reproduce_CFG544_fix2=c5, mass_exact_all=mass, all_pass=ctrl)
    log(f"\nControls: A1 deep {A1_num}; C2 {c2}; C5 {c5}; mass {mass} -> {'PASS' if ctrl else 'FAIL'}")

    sy = RES["sympy"]
    lyap = sy["A5_full_system_Lyapunov"]
    A4_all = all(RES["cells"][k]["A4_eddington"]["isotropic_lift_exists"] for k in keys)
    routes = {}
    for md in ("a1", "c"):
        gB = {k: runs[f"{k}|{md}_B"]["gate550"] for k in keys}; gC = {k: runs[f"{k}|{md}_C"]["gate550"] for k in keys}
        g544 = {k: dict(B=runs[f"{k}|{md}_B"]["gate544"], C=runs[f"{k}|{md}_C"]["gate544"]) for k in keys}
        gate_ok = all(gB.values()) and all(gC.values())
        P = {}
        for k in keys:
            inj = runs[f"{k}|{md}_over_inj"]; base = runs[f"{k}|{md}_over_base"]
            Mi = (inj["n_particles"] - base["n_particles"]) * cells[k]["Mcat"] / NPART
            P[k] = (inj["final"]["excess_in_rstar"] - base["final"]["excess_in_rstar"]) / Mi
        over_ok = all(v <= 0.2 for v in P.values())
        edge = {}
        for k in keys:
            for ic in ("B", "C"):
                edge[f"{k}|{ic}"] = float(math.log(runs[f"{k}|{md}_{ic}"]["final"]["r99"] / RES["cells"][k]["r99_analytic"]))
        edge_ok = all(-0.1 <= edge[f"{k}|{ic}"] <= C2_544[k] + 0.1 for k in keys for ic in ("B", "C"))
        en = {}
        for k in keys:
            oB = runs[f"{k}|{md}_B"]; oC = runs[f"{k}|{md}_C"]
            en[k] = dict(B_net=oB["final"]["sink_cum"], B_out=oB["final"]["drift_out"], B_in=oB["final"]["relax_in"], B_rate_last2=oB["sink_rate_last2"],
                         C_net=oC["final"]["sink_cum"], C_out=oC["final"]["drift_out"], C_in=oC["final"]["relax_in"], C_rate_last2=oC["sink_rate_last2"],
                         C_whole_history=RES["cells"][k]["CFG541_dW_over_Vf2"] + oC["final"]["sink_cum"],
                         B_relax_in_rate_last2=oB["relax_in_rate_last2"])
        en_ok = all(0 <= en[k]["B_net"] <= 1.0 and 0 <= en[k]["C_whole_history"] <= 1.0 for k in keys)
        rises = {nm: (runs[nm]["max_rise_F_over_F0"], runs[nm]["max_rise_FplusFv_over_L0"]) for nm in runs if nm.split("|")[1].startswith(md + "_")}
        open_items = [n for n, okk in (("overfill", over_ok), ("edge", edge_ok), ("A4 Eddington existence", A4_all),
                                       ("angular momentum", False), ("Lyapunov", lyap == "ESTABLISHED")) if not okk]
        if not (sy["A1_pass"] and sy["A2_pass"] and A1_num):
            lab = "POSITED"
        elif not gate_ok:
            lab = "INCONSISTENT (the derived target fails G550)"
        elif not en_ok:
            lab = "INCONSISTENT? energy not COMPATIBLE (A1, A2, G550 pass)"
        elif not open_items:
            lab = "DERIVED"
        else:
            lab = "DERIVED WITH OPEN ITEMS (" + ", ".join(open_items) + ")"
        lab = lab + f"; Lyapunov {lyap}"
        routes[md] = dict(G550_B=gB, G550_C=gC, G544=g544, gate_pass=gate_ok, overfill_P=P, overfill="HANDLED" if over_ok else "NOT HANDLED",
                          edge_dln_r99=edge, edge="PRESERVED" if edge_ok else "NOT PRESERVED", energy=en, energy_compatible=en_ok,
                          lyapunov_numeric_rises=rises, label=lab if ctrl else "NO LABEL (controls fail)")
        log(f"\nRoute {md}: G550 B {gB} C {gC}; G544 {g544}")
        log(f"  overfill P {P} -> {routes[md]['overfill']}; edge {edge} -> {routes[md]['edge']}")
        log(f"  energy {en} -> compatible {en_ok}")
        log(f"  LABEL {routes[md]['label']}")
    routes["a0"] = dict(label="INCONSISTENT (Casimir entropy: no finite temperature with the partner, T -> infinity; Landau pairs without it keep sigma = 0)")
    b2 = {k: RES["cells"][k]["B2_closed_sigma2_over_required_dex"] for k in keys}
    routes["b"] = dict(B1="beta = 0 with the zero-entropy partner: temperature undetermined -> POSITED",
                       B2_closed_dex=b2, B2="INCONSISTENT (closed: sigma^2 too hot)" if all(abs(v) > 0.1 for v in b2.values()) else "closed: within 0.1 dex in some cell",
                       B3_beta0_D={k: RES["cells"][k]["B3_beta0_uniform_fraction_D"] for k in keys}, B3_betainf="= route c",
                       label="POSITED (with the sink the multiplier is undetermined)")
    RES["routes"] = routes
    RES["labels"] = {md: routes[md]["label"] for md in routes}
    log(f"\nLABELS: {RES['labels']}")
    return 0 if ctrl else 1


if __name__ == "__main__":
    rc = main()
    with open(os.path.join(HERE, f"cfg550{TAG}.out"), "w") as fh:
        fh.write("\n".join(OUT) + "\n")
    with open(os.path.join(HERE, f"cfg550_results{TAG}.json"), "w") as fh:
        json.dump(RES, fh, indent=1, default=lambda o: o.tolist() if hasattr(o, "tolist") else str(o))
    sys.exit(rc)
